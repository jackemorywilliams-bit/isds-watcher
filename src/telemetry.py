"""Per-candidate run telemetry — one JSON line per candidate per run.

WHY THIS EXISTS. The pipeline's own record of a run is a handful of counters:
screened, classified, above threshold, surfaced. Those counters cannot answer the
questions the council actually keeps asking. Which source's items reach
enrichment and then die there? How many items were model-classified versus
keyword-scored, and did the model path *work*? When a run screens 80 and surfaces
1, what happened to the other 79? Every one of those questions has been answered
from memory, or from re-reading a digest folder and guessing. This file makes the
run answer them itself: one record per candidate, written every run, queryable
after the fact by ``scripts/telemetry_query.py``.

WHAT IT IS NOT. It is not an event log. A candidate accumulates ONE record across
the whole run — observed at intake, then annotated as it passes through ranking,
enrichment, classification, selection, and dedup. A dict keyed by candidate_id is
what enforces that: a second ``observe`` of the same candidate returns the record
already there, so "exactly one record per candidate per run" is a property of the
data structure and not of anyone remembering to call the right function once.

PRIVACY — THE HARD RULE. No candidate TEXT is ever written here. Not the title,
not the summary, not the body, not an excerpt of any of them. This file is
analytics about our own processing, and our own processing is describable in
lengths, hashes, ring subtotals, and enumerated outcomes. What we hold about a
source is already governed by the polite-crawler rules; a growing side-channel of
scraped prose in analytics/ would quietly evade them. So the record carries
``text_len_body`` and ``body_sha256`` and never ``body``. The hash still supports
the thing we actually need it for — telling whether the body we classified this
run is the same body we classified last run — without retaining the text.
``scripts/check_telemetry_privacy.py`` makes a violation a build failure rather
than something a reader has to notice.

DETERMINISM. Nothing here reads the wall clock. ``run_date`` is supplied by the
caller (the run already has one), and ``run_id`` is derived from that date plus a
hash of the candidate set, so the same candidates on the same date produce the
same run_id and byte-identical output. Records are sorted by candidate_id before
writing for the same reason: a dict's insertion order depends on fetch order, and
fetch order is not something we want the bytes to depend on.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

logger = logging.getLogger("isds.telemetry")

# 2 adds the `verdict_v2` section (the STATE_MODEL_V2 shadow derivation). Bumped
# rather than slipped in, because a query that assumes a shape is entitled to know
# when the shape changed; records written before this carry schema 1 and simply
# have no verdict.
#
# 3 adds `triage` (the Workstream F pre-enrichment ranking pass) and `v2_call`
# (whether a V2-prompt classification call was actually made for this candidate,
# and what came back). It also widens `verdict_v2` with `v2_basis`,
# `claims_source`, `classification_state` and per-ring span provenance. The
# widening is the reason for the bump on its own: a schema-2 reader that saw
# `verdict_v2.rings` and assumed the old six keys would silently ignore the
# fields that say whether a model produced the verdict at all.
SCHEMA = 3

TELEMETRY_PATH = "analytics/candidate_telemetry.jsonl"

# Field names that must never appear anywhere in a record, at any depth. These
# are the names the pipeline uses for raw candidate text; if one of them shows up
# in the telemetry it means someone attached the text itself.
FORBIDDEN_FIELDS = frozenset({"raw_text", "summary", "body", "title"})

# Above this, a string is long enough to be prose rather than an identifier.
MAX_STRING_LEN = 200

# The only fields allowed to hold a long string — all of them hex digests or ids
# we generate ourselves, none of them derived-but-readable source text.
LONG_STRING_ALLOWLIST = frozenset({
    "run_id", "candidate_id", "source_id_hash", "url_hash",
    "title_sha256", "body_sha256",
})


def sha256_hex(text: str) -> str:
    """Hex sha256 of a string; "" hashes like any other string (never special-cased)."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def candidate_id(source: str, source_id: str) -> str:
    """``source:<first 16 hex of sha256(source_id)>``.

    The source name stays in the clear because per-source analysis is the whole
    point and the source names are ours. The source_id is frequently the item's
    URL, so it is hashed — a truncation to 16 hex chars is 64 bits, which is far
    more than enough to keep a few hundred candidates per run distinct while
    keeping the id short enough to read in a terminal.
    """
    return f"{source}:{sha256_hex(source_id)[:16]}"


def compute_run_id(run_date: str, candidate_ids: Iterable[str]) -> str:
    """``<run_date>-<12 hex>`` over the sorted candidate set.

    Deterministic on purpose: re-running the same day over the same candidates
    must produce the same run_id, so a duplicated run is visible as a duplicate
    rather than looking like two different runs.
    """
    joined = "\n".join(sorted(candidate_ids))
    return f"{run_date}-{sha256_hex(joined)[:12]}"


def _iso(value: Any) -> str:
    """A datetime as ISO-8601, anything else as its string form ("" for None)."""
    if isinstance(value, datetime):
        return value.isoformat()
    return "" if value is None else str(value)


def _host(url: str) -> str:
    """The netloc of a URL, or "" if it has none. Never raises on junk input."""
    try:
        return urlparse(url or "").netloc
    except ValueError:
        return ""


def _blank_record(run_date: str, item) -> dict:
    """The full record shape, with every field present and at its null value.

    Every field exists from the start — an absent field and a field that is
    honestly "we did not do that" are different statements, and a query that has
    to distinguish ``.get(k)`` returning None from a real False is a query that
    will get it wrong.
    """
    source = getattr(item, "source", "") or ""
    source_id = getattr(item, "source_id", "") or ""
    url = getattr(item, "url", "") or ""
    return {
        "schema": SCHEMA,
        "run_id": "",                 # filled at flush, once the set is known
        "run_date": run_date,
        "candidate_id": candidate_id(source, source_id),
        "source": source,
        "source_id_hash": sha256_hex(source_id),
        "url_host": _host(url),
        "url_hash": sha256_hex(url),
        "published": _iso(getattr(item, "published", None)),
        "access": {
            "headline_only": False,
            "body_fetched": False,
            "fetch_outcome": "not_attempted",
            "text_len_title": 0,
            "text_len_summary": 0,
            "text_len_body": 0,
            "title_sha256": "",
            "body_sha256": "",
        },
        "lexical": {
            "per_ring_subtotal": {},
            "hits": [],
            "negative_signal": False,
            "rank": -1,
        },
        # The Workstream F pre-enrichment triage pass (src/triage.py). `ran` is
        # False and `basis` is "not_run" unless a triage model response was
        # actually parsed for this candidate — a skipped or failed triage is
        # recorded as the named skip it was, never as an absence.
        "triage": {
            "ran": False,
            "basis": "not_run",
            "model": "",
            "prompt_version": "",
            "outcome": "",
            "attempts": 0,
            "semantic_rank": 0,
            "strengths": {},
        },
        # Whether a V2-prompt classification call was made for this candidate
        # (src/classify_v2.py). Separate from `verdict_v2`, which is the
        # DERIVATION: the derivation happens every run in shadow mode, the call
        # happens only when config.V2_SHADOW_CALLS asks for it and only for the
        # sampled candidates.
        "v2_call": {
            "mode": "off",
            "called": False,
            "basis": "lexical_only",
            "model": "",
            "prompt_version": "",
            "outcome": "",
            "attempts": 0,
            "retried_strict": False,
            "model_nexus_advisory": "",
        },
        "entered_enrichment": False,
        "classification": {
            "ran": False,
            "path": "none",
            "model": "",
            "prompt_version": "",
            "outcome": "",
            "attempts": 0,
            "retried_strict": False,
            "model_score_advisory": None,
        },
        "surfacing": {
            "surfaced": False,
            "reason": "not_selected",
            "digest": "",
            "position": -1,
        },
        "dedup": {
            "seen_before": False,
            "marked_seen": False,
            "deferred": False,
            "abandoned": False,
        },
        # The STATE_MODEL_V2 shadow derivation (src/rings.py). Present on every
        # record with `derived: False` when the flag is off or the derivation did
        # not run — the same reason every other section is present from the start.
        # Bounded values only: enumerated constants, small integers, hex digests,
        # and our own ring names. No spans, no excerpts; `evidence_span` is
        # candidate text and is dropped by RingFinding.to_dict, which keeps only
        # the span's sha256 and length, before it can reach here.
        #
        # `v2_basis` is the field that stops this section from being read as a
        # model's work when it is not: "lexical_only" means no model response
        # contributed, and the only values that name a model are produced on the
        # one path where a model response was parsed and used.
        "verdict_v2": {
            "mode": "off",
            "derived": False,
            "lane": "",
            "lane_reason": "",
            "public_label": "",
            "nexus": "",
            "evidence_location": "",
            "evidence_validity": "",
            "path": "",
            "classification_state": "",
            "classification_outcome": "",
            "guard_demoted": False,
            "v2_basis": "lexical_only",
            "claims_source": "none",
            "model_score_advisory": None,
            "rings": {},
        },
    }


class RunTelemetry:
    """The run's candidate records, accumulated in memory and written once.

    Held in memory for the whole run rather than appended as we go because a
    candidate's record is not complete until selection has happened, and a
    half-written line that a later stage has to go back and amend is exactly the
    kind of thing that ends up amended in some runs and not others.
    """

    def __init__(self, run_date: str):
        self.run_date = run_date
        self._records: dict[str, dict] = {}
        self._flushed = False

    # -- intake ------------------------------------------------------------- #
    def observe(self, item) -> str:
        """Register a candidate (idempotently) and return its candidate_id."""
        cid = candidate_id(getattr(item, "source", "") or "",
                           getattr(item, "source_id", "") or "")
        if cid not in self._records:
            self._records[cid] = _blank_record(self.run_date, item)
        return cid

    def get(self, cid: str) -> Optional[dict]:
        return self._records.get(cid)

    def __len__(self) -> int:
        return len(self._records)

    def _section(self, cid: str, name: str) -> Optional[dict]:
        """The named sub-dict of a record, or None if the candidate is unknown.

        A note about a candidate we never observed is a bug in the caller, but it
        must not take the run down — telemetry is instrumentation, and
        instrumentation that can crash the thing it measures is worse than none.
        """
        rec = self._records.get(cid)
        if rec is None:
            logger.warning("telemetry: note for unobserved candidate %s", cid)
            return None
        return rec[name]

    # -- annotations -------------------------------------------------------- #
    def note_access(self, cid: str, item, *, headline_only: bool,
                    body_fetched: bool, fetch_outcome: str) -> None:
        """What we were able to read of this item — in lengths and hashes only."""
        acc = self._section(cid, "access")
        if acc is None:
            return
        title = getattr(item, "title", "") or ""
        summary = getattr(item, "summary", "") or ""
        raw = getattr(item, "raw_text", "") or ""
        acc.update({
            "headline_only": bool(headline_only),
            "body_fetched": bool(body_fetched),
            "fetch_outcome": fetch_outcome,
            "text_len_title": len(title),
            "text_len_summary": len(summary),
            "text_len_body": len(raw),
            "title_sha256": sha256_hex(title),
            "body_sha256": sha256_hex(raw),
        })

    def note_lexical(self, cid: str, *, per_ring_subtotal: dict, hits: list,
                     negative_signal: bool, rank: int) -> None:
        """The keyword pre-score, in the detail the score itself throws away."""
        lex = self._section(cid, "lexical")
        if lex is None:
            return
        lex.update({
            "per_ring_subtotal": {str(k): int(v)
                                  for k, v in sorted((per_ring_subtotal or {}).items())},
            "hits": sorted(str(h) for h in (hits or [])),
            "negative_signal": bool(negative_signal),
            "rank": int(rank),
        })

    def note_triage(self, cid: str, section: dict) -> None:
        """The Workstream F triage result for this candidate.

        Taken as the whole section `src/triage.py` built rather than field by
        field, for the same reason `note_verdict_v2` is: the shape belongs to the
        module that owns the pass, and a field added there should appear here
        without a second edit in a second file that someone has to remember.
        """
        rec = self._records.get(cid)
        if rec is None:
            logger.warning("telemetry: note for unobserved candidate %s", cid)
            return
        rec["triage"] = dict(section)

    def note_v2_call(self, cid: str, section: dict) -> None:
        """Whether a V2-prompt call was made for this candidate, and its result."""
        rec = self._records.get(cid)
        if rec is None:
            logger.warning("telemetry: note for unobserved candidate %s", cid)
            return
        rec["v2_call"] = dict(section)

    def note_enrichment(self, cid: str, entered: bool) -> None:
        rec = self._records.get(cid)
        if rec is None:
            logger.warning("telemetry: note for unobserved candidate %s", cid)
            return
        rec["entered_enrichment"] = bool(entered)

    def note_classification(self, cid: str, *, ran: bool, path: str, model: str,
                            prompt_version: str, outcome: str, attempts: int,
                            retried_strict: bool,
                            model_score_advisory: Optional[int]) -> None:
        """What the classifier did, including when what it did was fail.

        ``model_score_advisory`` is the score the run declined to publish — the
        keyword number behind a provider error. Recording it is how we can later
        ask what an outage actually cost without ever having published it.
        """
        cls = self._section(cid, "classification")
        if cls is None:
            return
        cls.update({
            "ran": bool(ran),
            "path": path,
            "model": model or "",
            "prompt_version": prompt_version or "",
            "outcome": outcome or "",
            "attempts": int(attempts),
            "retried_strict": bool(retried_strict),
            "model_score_advisory": (None if model_score_advisory is None
                                     else int(model_score_advisory)),
        })

    def note_surfacing(self, cid: str, *, surfaced: bool, reason: str,
                       digest: str, position: int) -> None:
        surf = self._section(cid, "surfacing")
        if surf is None:
            return
        surf.update({
            "surfaced": bool(surfaced),
            "reason": reason,
            "digest": digest or "",
            "position": int(position),
        })

    def note_verdict_v2(self, cid: str, verdict, *, mode: str = "shadow") -> None:
        """Record the V2 lane derivation for this candidate.

        ``verdict`` is a ``rings.RingVerdict``; its own ``to_telemetry`` decides
        what is safe to keep, so the privacy rule is enforced next to the data it
        governs rather than here. Taken as a whole dict rather than field by
        field because the shape is the contract's, and a field added there should
        appear here without a second edit.
        """
        rec = self._records.get(cid)
        if rec is None:
            logger.warning("telemetry: note for unobserved candidate %s", cid)
            return
        rec["verdict_v2"] = verdict.to_telemetry(mode)

    def note_dedup(self, cid: str, *, seen_before: bool, marked_seen: bool,
                   deferred: bool, abandoned: bool) -> None:
        ded = self._section(cid, "dedup")
        if ded is None:
            return
        ded.update({
            "seen_before": bool(seen_before),
            "marked_seen": bool(marked_seen),
            "deferred": bool(deferred),
            "abandoned": bool(abandoned),
        })

    # -- output ------------------------------------------------------------- #
    def records(self) -> list[dict]:
        """Every record, sorted by candidate_id, with run_id resolved."""
        rid = compute_run_id(self.run_date, self._records.keys())
        out = []
        for cid in sorted(self._records):
            rec = dict(self._records[cid])
            rec["run_id"] = rid
            out.append(rec)
        return out

    def flush(self, path: str = TELEMETRY_PATH) -> int:
        """Append this run's records to ``path``; return how many were written.

        Refuses to write twice. A second flush would double every candidate for
        the run, and "exactly one record per candidate per run" is the invariant
        every query downstream is entitled to assume.
        """
        if self._flushed:
            logger.warning("telemetry: flush called twice; ignoring the second")
            return 0
        self._flushed = True
        rows = self.records()
        if not rows:
            return 0
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            for rec in rows:
                fh.write(json.dumps(rec, sort_keys=True, ensure_ascii=True,
                                    separators=(",", ":")))
                fh.write("\n")
        logger.info("telemetry: wrote %d candidate records to %s", len(rows), path)
        return len(rows)


def load_records(path: str = TELEMETRY_PATH) -> list[dict]:
    """Every parseable record in the file (a corrupt line is skipped, not fatal)."""
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError:
                logger.warning("telemetry: unparseable line %d in %s", lineno, path)
                continue
            if isinstance(rec, dict):
                out.append(rec)
    return out
