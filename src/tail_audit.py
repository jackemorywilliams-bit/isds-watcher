"""The stratified tail audit — measuring what the enrichment cut throws away.

THE QUESTION IT EXISTS TO ANSWER. `src/main.py` enriches the top
`config.ENRICH_TOP_N` candidates and leaves the rest un-enriched. Everything
below that line is scored on a headline and a feed summary. Nobody has ever
measured what that costs, and the external audit's point (3) is that the
instrument's false-negative rate is not merely unmeasured but UNMEASURABLE while
the gate is unexamined. This is the measurement.

THE METHOD, AND WHY IT IS BUILDABLE TODAY: PAIRED WITHIN-ITEM
ENRICHED-VS-UNENRICHED RE-CLASSIFICATION. The run has already classified every
tail item un-enriched. The audit takes a sample of them, enriches each one, and
classifies it AGAIN. The two bands are the pair. A difference is a FLIP — the
enrichment cut changed what the instrument said about this exact item — and a
flip needs NO HUMAN LABEL to detect. That is the whole reason this can be built
before `analytics/locked_set/` is coded: it measures a flip, not a truth. It
says nothing about whether either band was right.

THE STRATIFICATION IS ON `lexical_subtotal`, NOT ON RANK. Rank is a position in
a queue whose ordering changed the day triage was enabled; the subtotal is the
raw lexical evidence the item carries, which is the thing the gate is actually
selecting on. Three strata:

    A  subtotal == 0                 the items the lexicon cannot see at all
    B  0 < subtotal < PRESENT_FLOOR  seen, but below the "ring is present" floor
    C  subtotal >= PRESENT_FLOOR     at least one ring's worth of lexical weight

`PRESENT_FLOOR` is imported from `src/classify.py` rather than written here as
12: the boundary the audit stratifies on IS the boundary the scorer uses, and
two copies of it would silently diverge.

THE LEDGER IS CROSS-RUN AND APPEND-ONLY (`analytics/tail_audit.jsonl`). Two
properties depend on it and neither is optional. (1) The strata are not re-drawn
from scratch every run: an item already audited is excluded from the pool, so
the audit accumulates coverage instead of re-measuring the same six items in
perpetuity. (2) No item is ever audited twice, so no item can contribute two
flips to a rate computed over the file.

NO CANDIDATE TEXT. EVER. The ledger carries `LEDGER_FIELDS` and nothing else:
identifiers, an enumerated stratum, three integers and two band names. The item
is identified by the same hash `src/telemetry.py` uses, not by its title or its
URL. `scripts/check_telemetry_privacy.py` enforces the field set exactly — a
field added here without being added there fails the build.

WHAT IS NOT PUBLISHED. A tail-audit flip rate is an internal measurement of the
instrument, not a finding about ISDS. Publishing one to the recipient would be
the instrument grading itself in her inbox. The reporting surface is
`scripts/telemetry_query.py` and nothing else; `PUBLICATION_KEYS` below is what
`tests/test_publication_quarantine.py` enforces that with.

Council rulings session of 2026-09-13, Ruling 4(c).
"""

from __future__ import annotations

import json
import logging
import os
import random
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from . import config
from .classify import PRESENT_FLOOR, ClassifyOutcome, outcome_of
from .telemetry import candidate_id

logger = logging.getLogger("isds.tail_audit")

LEDGER_PATH = "analytics/tail_audit.jsonl"

# The ledger's schema, exactly. Ruling 4(c) named these nine fields and no
# others; `scripts/check_telemetry_privacy.py` asserts the key set matches this
# tuple, so a tenth field is a build failure rather than a quiet widening of an
# append-only stream that nobody reads until it matters.
LEDGER_FIELDS = (
    "run_id",
    "item_id",
    "source",
    "stratum",
    "lexical_subtotal",
    "band_unenriched",
    "band_enriched",
    "score_delta",
    "seed",
)

# The strata. Named, not numbered: "A" alone in a query result says nothing, and
# the boundary is the interesting part of each name.
STRATUM_A = "A_lexically_invisible"
STRATUM_B = "B_below_present_floor"
STRATUM_C = "C_at_or_above_present_floor"
STRATA = (STRATUM_A, STRATUM_B, STRATUM_C)

# Band names. The instrument's own bands, from `fingerprint.yaml`'s `scoring`
# block; see `_band_thresholds`.
BAND_HIGH = "HIGH"
BAND_MEDIUM = "MEDIUM"
BAND_LOW = "LOW"

# The identifiers by which a tail-audit MEASUREMENT can be reached. Deliberately
# NOT `TAIL_AUDIT_N` or `tail_audit_cost_usd`: the first is a configuration
# value and the second is a COST, which Ruling 4(c) requires in `meta.json` and
# the run summary. What may not be published is the measurement — the ledger and
# the paired bands in it.
PUBLICATION_KEYS = frozenset({
    "tail_audit.jsonl",
    "band_unenriched",
    "band_enriched",
    "score_delta",
    "read_ledger",
    "audited_item_ids",
})


def _band_thresholds(path: str = "fingerprint.yaml") -> tuple[int, int]:
    """(high, medium) from `fingerprint.yaml`, which is the authority.

    Read rather than hard-coded for the same reason `src/config.py` reads the
    threshold from the same file: a band boundary written twice is a band
    boundary that will eventually disagree with itself. The fallback matches the
    committed values and is used only when the file cannot be read at all.
    """
    try:
        import yaml  # lazy: keep import-time deps minimal

        with open(path, "r", encoding="utf-8") as fh:
            scoring = (yaml.safe_load(fh) or {}).get("scoring") or {}
        return int(scoring.get("high", 70)), int(scoring.get("medium", 40))
    except Exception as exc:  # noqa: BLE001 - a measurement must not crash a run
        logger.warning("tail_audit: could not read bands from %s (%s); using 70/40",
                       path, exc)
        return 70, 40


def band_of(score, *, thresholds: Optional[tuple[int, int]] = None) -> str:
    """The band a relevance score falls in. HIGH / MEDIUM / LOW."""
    high, medium = thresholds if thresholds is not None else _band_thresholds()
    value = int(score or 0)
    if value >= high:
        return BAND_HIGH
    if value >= medium:
        return BAND_MEDIUM
    return BAND_LOW


def stratum_of(lexical_subtotal: int) -> str:
    """Which stratum a candidate's lexical subtotal puts it in.

    The boundaries are 0 and `classify.PRESENT_FLOOR` (12): a subtotal of 0 is
    stratum A, 11 is B, and 12 is C. A negative subtotal cannot occur — the
    per-ring subtotals are sums of non-negative weights — and is treated as 0
    rather than as a fourth, unnamed case.
    """
    value = int(lexical_subtotal or 0)
    if value <= 0:
        return STRATUM_A
    if value < PRESENT_FLOOR:
        return STRATUM_B
    return STRATUM_C


def per_stratum_n(total: Optional[int] = None) -> int:
    """How many items to draw from each stratum, for a total of ``total``.

    DERIVED from `config.TAIL_AUDIT_N` rather than written beside it, so the two
    numbers the ruling gave (6 in total, 2 per stratum) cannot drift apart: the
    second is the first divided by the number of strata. Integer division, so a
    total that is not a multiple of three draws fewer rather than more.
    """
    n = config.TAIL_AUDIT_N if total is None else int(total)
    return max(0, int(n) // len(STRATA))


@dataclass(frozen=True)
class TailCandidate:
    """One un-enriched tail item, as the audit needs to see it.

    `item` is the live candidate object (the audit enriches and re-classifies
    it); everything else is what the run already knows about it and what the
    ledger records.
    """

    item_id: str
    source: str
    lexical_subtotal: int
    score_unenriched: int
    outcome_unenriched: str
    item: object

    @property
    def stratum(self) -> str:
        return stratum_of(self.lexical_subtotal)


@dataclass(frozen=True)
class AuditResult:
    """What one run's audit did. `rows` is what reaches the ledger."""

    rows: list
    calls: int
    seed: str
    shortfalls: dict          # stratum -> how many fewer than asked for
    skipped_not_measurable: int   # sampled, called, and not usable as a pair


# --------------------------------------------------------------------------- #
# The ledger
# --------------------------------------------------------------------------- #
def read_ledger(path: str = LEDGER_PATH) -> list[dict]:
    """Every parseable row (a corrupt line is skipped, never fatal)."""
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                logger.warning("tail_audit: unparseable line %d in %s", lineno, path)
                continue
            if isinstance(row, dict):
                out.append(row)
    return out


def audited_item_ids(rows: Iterable[dict]) -> set:
    """The items already audited. The whole point of a cross-run ledger."""
    return {str(r.get("item_id", "")) for r in rows if r.get("item_id")}


def append_rows(rows: list, path: str = LEDGER_PATH) -> int:
    """Append rows to the ledger. Append-only: nothing here rewrites a line."""
    if not rows:
        return 0
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True, ensure_ascii=True,
                                separators=(",", ":")))
            fh.write("\n")
    return len(rows)


# --------------------------------------------------------------------------- #
# The sample
# --------------------------------------------------------------------------- #
def select_sample(candidates: Iterable[TailCandidate], *, seed: str,
                  already_audited: Optional[set] = None,
                  per_stratum: int = 2) -> tuple[dict, dict]:
    """``({stratum: [candidate, ...]}, {stratum: shortfall})`` under ``seed``.

    DETERMINISTIC TWICE OVER. Each stratum's pool is sorted by `item_id` before
    anything is drawn, so the draw does not depend on fetch order; and the draw
    itself runs on a `random.Random` seeded with the run's own id, so the same
    run over the same candidates selects the same items. The seed is recorded on
    every row, which is what makes the selection checkable rather than merely
    reproducible in principle.

    A SHORT STRATUM TAKES WHAT EXISTS AND THE SHORTFALL IS RECORDED. Most runs
    will not have two un-enriched items in every stratum; refusing to audit
    anything when one stratum is thin would mean the audit almost never runs,
    and silently taking one would make "2 per stratum" a claim the data does not
    support. The shortfall is returned so the run can say so.
    """
    audited = already_audited or set()
    pools: dict = {s: [] for s in STRATA}
    for cand in candidates:
        if cand.item_id in audited:
            continue
        pools[cand.stratum].append(cand)

    rnd = random.Random(seed)
    chosen: dict = {}
    shortfalls: dict = {}
    for stratum in STRATA:
        pool = sorted(pools[stratum], key=lambda c: c.item_id)
        take = min(per_stratum, len(pool))
        chosen[stratum] = rnd.sample(pool, take) if take else []
        if take < per_stratum:
            shortfalls[stratum] = per_stratum - take
    return chosen, shortfalls


# --------------------------------------------------------------------------- #
# The audit
# --------------------------------------------------------------------------- #
def run_audit(candidates: Iterable[TailCandidate], *, run_id: str,
              enrich: Callable, classify: Callable,
              per_stratum: int = 2,
              already_audited: Optional[set] = None) -> AuditResult:
    """Enrich and re-classify the sample; return the rows for the ledger.

    `enrich` and `classify` are injected rather than imported so that the audit
    can be exercised without a provider: the pipeline passes its own enrichment
    and classification, and a test passes a stub, and the code under test is the
    same code either way.

    WHAT IS NOT RECORDED, AND WHY. A pair is written only when BOTH
    classifications are genuine model answers (`ClassifyOutcome.OK`). If either
    side fell back to a keyword score — whether by design or after a failed
    provider call — the "flip" would be a flip between a model reading and a
    lexicon reading, which measures the outage and not the enrichment cut. That
    item is left unaudited (it stays in the pool for a later run) and counted as
    `skipped_not_measurable`. This is the precondition Ruling 4(c) attached to
    the audit: `KEYWORD_AFTER_PROVIDER_ERROR` exists precisely so that this
    distinction can be made at all.
    """
    seed = str(run_id)
    chosen, shortfalls = select_sample(candidates, seed=seed,
                                       already_audited=already_audited,
                                       per_stratum=per_stratum)
    thresholds = _band_thresholds()
    rows: list = []
    calls = 0
    skipped = 0
    for stratum in STRATA:
        for cand in chosen[stratum]:
            try:
                enrich(cand.item)
                classified = classify(cand.item)
                calls += 1
            except Exception as exc:  # noqa: BLE001 - a measurement is never fatal
                logger.error("tail_audit: re-classification failed for %s: %s",
                             cand.item_id, exc)
                calls += 1
                skipped += 1
                continue
            outcome = outcome_of(classified).value
            if (outcome != ClassifyOutcome.OK.value
                    or cand.outcome_unenriched != ClassifyOutcome.OK.value):
                logger.info("tail_audit: %s not measurable as a pair "
                            "(unenriched=%s, enriched=%s)", cand.item_id,
                            cand.outcome_unenriched, outcome)
                skipped += 1
                continue
            score_enriched = int(getattr(classified, "relevance_score", 0) or 0)
            rows.append({
                "run_id": str(run_id),
                "item_id": cand.item_id,
                "source": cand.source,
                "stratum": stratum,
                "lexical_subtotal": int(cand.lexical_subtotal),
                "band_unenriched": band_of(cand.score_unenriched,
                                           thresholds=thresholds),
                "band_enriched": band_of(score_enriched, thresholds=thresholds),
                "score_delta": score_enriched - int(cand.score_unenriched),
                "seed": seed,
            })
    return AuditResult(rows=rows, calls=calls, seed=seed, shortfalls=shortfalls,
                       skipped_not_measurable=skipped)


def tail_candidate(item, *, lexical_subtotal: int, classified,
                   outcome: str) -> TailCandidate:
    """Build a `TailCandidate` from what the run already holds about an item."""
    return TailCandidate(
        item_id=candidate_id(getattr(item, "source", "") or "",
                             getattr(item, "source_id", "") or ""),
        source=getattr(item, "source", "") or "",
        lexical_subtotal=int(lexical_subtotal or 0),
        score_unenriched=int(getattr(classified, "relevance_score", 0) or 0),
        outcome_unenriched=str(outcome or ""),
        item=item,
    )
