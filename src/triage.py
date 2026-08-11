"""Workstream F — semantic triage, so that ranking stops being purely lexical.

THE PROBLEM, MEASURED RATHER THAN ASSERTED. `src/main.py` ranks every candidate
by `keyword_score` and enriches the top `ENRICH_TOP_N`. Only enriched items are
model-classified. So the model never sees an item the LEXICON could not see, and
the lexicon is a list of phrases. Run this repo's own probe suite through
`keyword_score` and the failure is visible without argument:

    E5_einarsson_lexical_brittle   score   0   expected band HIGH
    C2_china_marketing_loose       score   0   expected band MEDIUM

Both are paraphrase-heavy pharmaceutical-regulatory items — the exact shape of
the research question — and both score zero, which on a busy run means they sort
below every item that happened to contain the word "trademark" and never reach
enrichment at all. The instrument cannot miss them at classification, because it
never gets that far. Ranking is the gate.

WHAT THIS DOES. A compact prompt (`prompts/triage.txt`: three ring definitions
and the strength ladder, no few-shots, no digest_summary, no notable_quote) runs
over every candidate's TITLE AND SUMMARY — text already in hand, so this adds
ZERO new HTTP fetches and touches no source's robots policy. Its three
strengths become a `semantic_rank`, and the enrichment budget is allocated by
the total order `(-semantic_rank, -lexical_subtotal, source, source_id)`.

WHAT IT DOES NOT DO. It does not classify, it does not decide a lane, and it
never reaches the digest. It reorders a queue. A triage strength is a guess made
from a headline; the actual finding is still made downstream from a fetched body
by a prompt that has to show its evidence.

OFF BY DEFAULT (`config.TRIAGE_ENABLED`). It calls the model once per CANDIDATE
rather than once per enriched item, so it is the most cost-sensitive component
in the pipeline: ~$0.0014 a call on the R2.1 table, ~$0.02 on a median run of
14 and ~$0.11 on the largest run observed (80). Enabling it is a decision.

FAILURE IS RECORDED, NEVER INFERRED. No provider, a provider error, or an
unparseable answer all mean the same thing for ranking — that item falls back to
its lexical position — and all three are written to telemetry as distinct,
named skips. The property that makes this safe is proved in the tests rather
than argued here: when NO item gets a triage result, every semantic_rank is 0
and the sort key collapses to `(-lexical_subtotal, source, source_id)`, so a
total provider outage reproduces lexical ranking exactly rather than scrambling
it.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import classify as _classify
from .classify import VALID_RINGS, ClassifyOutcome
from .classify_v2 import STRENGTH_WORDS
from .rings import RINGS, Strength

# Reached through the module for the same reason `src/classify_v2.py` does it:
# so that patching `src.classify._call_anthropic` stubs every provider path in
# the pipeline, including this one.

logger = logging.getLogger("isds.triage")

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "triage.txt"
_PROMPT_CACHE: Optional[str] = None

# Title and summary are sent whole. They are short by construction — a feed
# title and a feed summary — and truncating a summary mid-sentence would change
# the thing being judged for no saving worth having.
MAX_SUMMARY_CHARS = 2000

# Basis vocabulary. Same discipline as `classify_v2`: the ONLY value that names
# a model is the one constructed on the success path.
TRIAGE_BASIS_NOT_RUN = "not_run"                 # the flag is off
TRIAGE_BASIS_NO_PROVIDER = "skipped_no_provider"
TRIAGE_BASIS_PROVIDER_ERROR = "skipped_provider_error"
TRIAGE_BASIS_MALFORMED = "skipped_malformed_output"
_SEMANTIC_PREFIX = "semantic:"

SKIP_BASES = frozenset({TRIAGE_BASIS_NOT_RUN, TRIAGE_BASIS_NO_PROVIDER,
                        TRIAGE_BASIS_PROVIDER_ERROR, TRIAGE_BASIS_MALFORMED})


def semantic_basis(model_id: str) -> str:
    return f"{_SEMANTIC_PREFIX}{model_id}"


def basis_names_a_model(basis: str) -> bool:
    return str(basis or "").startswith(_SEMANTIC_PREFIX)


# --------------------------------------------------------------------------- #
# Prompt
# --------------------------------------------------------------------------- #
def load_triage_prompt() -> str:
    global _PROMPT_CACHE
    if _PROMPT_CACHE is None:
        with open(_PROMPT_PATH, "r", encoding="utf-8") as fh:
            _PROMPT_CACHE = fh.read()
    return _PROMPT_CACHE


def triage_prompt_version() -> str:
    try:
        return hashlib.sha256(load_triage_prompt().encode("utf-8")).hexdigest()[:12]
    except OSError:
        return "unknown"


def build_triage_prompt(item) -> str:
    """Render the triage prompt. TITLE and SUMMARY only — never a body.

    `raw_text` is deliberately not consulted even when it is populated. For five
    of this project's sources `raw_text` IS the title and for three more it is a
    copy of the summary (see `rings.derive_location`), so reading it would send
    duplicate text for some sources and a genuine body for others — making the
    triage question quietly different per source, which is the one thing a
    ranking pass must not be.
    """
    summary = getattr(item, "summary", "") or ""
    if len(summary) > MAX_SUMMARY_CHARS:
        summary = summary[:MAX_SUMMARY_CHARS]
    return (load_triage_prompt()
            .replace("{{TITLE}}", getattr(item, "title", "") or "")
            .replace("{{SUMMARY}}", summary))


# --------------------------------------------------------------------------- #
# Strict parser
# --------------------------------------------------------------------------- #
_FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)


def parse_triage_response(text: str) -> Optional[dict]:
    """``{ring: Strength}`` for all three rings, or None. Coerces nothing.

    Strict for the same reason `classify_v2.parse_v2_response` is: the output
    reorders a queue, and a queue silently reordered by a misparse is a defect
    that leaves no trace anywhere. A missing ring, a fourth ring, or any word
    outside the four is a parse failure, and a parse failure means this item
    keeps its lexical position and the failure is recorded.
    """
    if not text:
        return None
    cleaned = text.strip()
    fence = _FENCE.match(cleaned)
    cleaned = fence.group(1).strip() if fence else cleaned.strip("`").strip()

    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(cleaned[start:end + 1])
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict):
        return None

    raw = data.get("rings")
    if not isinstance(raw, dict) or set(raw) != set(VALID_RINGS):
        return None

    out: dict[str, Strength] = {}
    for ring in RINGS:
        word = raw.get(ring)
        if not isinstance(word, str):
            return None
        strength = STRENGTH_WORDS.get(word.strip().lower())
        if strength is None:
            return None
        out[ring] = strength
    return out


# --------------------------------------------------------------------------- #
# The rank
# --------------------------------------------------------------------------- #
def semantic_rank(strengths: Optional[dict]) -> int:
    """A single integer in [0, 63] ordering candidates by triage strength.

    IP DOMINATES, AND THE OTHER TWO ARE SYMMETRIC:

        rank = ip * 16 + max(jrm, ja) * 4 + min(jrm, ja)

    The shape is the MATCH rule's, not a weighting anyone chose by feel. R2.1
    makes a match "IP present AND at least one of the other two present", so IP
    is lexicographically dominant and the remaining two rings are interchangeable
    with each other — which is exactly what taking their max and then their min
    encodes. Using `jrm * 4 + ja` instead would rank a judicial-ring item above
    an otherwise identical jurisdictional-ring item for no reason in the
    contract.

    A missing triage result is 0, the same value as "absent on all three rings".
    That is what makes the degenerate case safe: if no item was triaged, every
    rank is 0, the first key component is constant, and the sort collapses to
    the lexical order.
    """
    if not strengths:
        return 0
    ip = strengths.get(RINGS[0], Strength.ABSENT).value
    a = strengths.get(RINGS[1], Strength.ABSENT).value
    b = strengths.get(RINGS[2], Strength.ABSENT).value
    return ip * 16 + max(a, b) * 4 + min(a, b)


def lexical_subtotal(lexical_result: Optional[dict]) -> int:
    """The candidate's total lexical weight — the sum of its per-ring subtotals.

    Deliberately NOT `relevance_score`. The score applies combination rules,
    caps and a negative-signal penalty, all of which exist to decide publication
    and none of which are about how promising an item is to READ. The subtotals
    are the raw lexical evidence, and this is a reading queue.
    """
    per_ring = (lexical_result or {}).get("per_ring_subtotal") or {}
    return sum(int(v) for v in per_ring.values())


def triage_sort_key(item, *, lexical_result: Optional[dict],
                    strengths: Optional[dict]) -> tuple:
    """The R2.1 total order: ``(-semantic_rank, -lexical_subtotal, source, source_id)``.

    TOTAL, and that is the point. The existing ranking sorts on one integer and
    leaves ties to Python's stable sort, which means the enrichment cut is
    settled by fetch order — deterministic within a run, but not a function of
    the items. Every component here is a property of the candidate, so the same
    candidate set produces the same queue no matter what order it arrived in.
    """
    return (-semantic_rank(strengths),
            -lexical_subtotal(lexical_result),
            getattr(item, "source", "") or "",
            getattr(item, "source_id", "") or "")


# --------------------------------------------------------------------------- #
# The call
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class TriageResult:
    """One triage attempt. ``strengths`` is empty on every skip route."""

    basis: str
    outcome: ClassifyOutcome
    model: str = ""
    prompt_version: str = ""
    attempts: int = 0
    strengths: dict = field(default_factory=dict)

    @property
    def ran(self) -> bool:
        return basis_names_a_model(self.basis)

    @property
    def rank(self) -> int:
        return semantic_rank(self.strengths if self.ran else None)


def _skipped(basis: str, outcome: ClassifyOutcome, *, model: str = "",
             attempts: int = 0) -> TriageResult:
    return TriageResult(basis=basis, outcome=outcome, model=model,
                        prompt_version=triage_prompt_version(), attempts=attempts)


def triage_item(item, provider: Optional[str] = None) -> TriageResult:
    """Triage one candidate. Never raises.

    NO RETRY, and that is a deliberate difference from the two classification
    paths. A retry doubles the cost of the pass that runs over every candidate,
    to salvage a ranking hint whose absence costs one item its lexical position
    — which is where it would have been anyway. The classifier retries because
    a failure there loses the item; this does not, because a failure here loses
    nothing but a reordering.
    """
    raw_provider = provider if provider is not None else os.environ.get("MODEL_PROVIDER")
    norm = _classify._normalize_provider(raw_provider)
    if norm is None or not _classify._provider_ready(norm):
        return _skipped(TRIAGE_BASIS_NO_PROVIDER,
                        ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN)

    model_id = _classify._resolved_model(norm) or ""
    try:
        caller = (_classify._call_gemini if norm == "gemini"
                  else _classify._call_anthropic)
        parsed = parse_triage_response(caller(build_triage_prompt(item)))
    except Exception as exc:  # noqa: BLE001 - a ranking hint is never fatal
        logger.warning("triage: provider error (%s) for %s: %s", norm,
                       getattr(item, "source_id", ""), exc)
        return _skipped(TRIAGE_BASIS_PROVIDER_ERROR, ClassifyOutcome.PROVIDER_ERROR,
                        model=model_id, attempts=1)
    if parsed is None:
        logger.info("triage: unparseable answer for %s; keeping its lexical rank",
                    getattr(item, "source_id", ""))
        return _skipped(TRIAGE_BASIS_MALFORMED, ClassifyOutcome.PARSE_FAILED,
                        model=model_id, attempts=1)

    return TriageResult(
        basis=semantic_basis(model_id), outcome=ClassifyOutcome.OK,
        model=model_id, prompt_version=triage_prompt_version(), attempts=1,
        strengths=parsed)


def telemetry_section(result: Optional[TriageResult]) -> dict:
    """The bounded per-candidate triage record. Enumerated values only."""
    if result is None:
        return {
            "ran": False,
            "basis": TRIAGE_BASIS_NOT_RUN,
            "model": "",
            "prompt_version": "",
            "outcome": "",
            "attempts": 0,
            "semantic_rank": 0,
            "strengths": {},
        }
    return {
        "ran": bool(result.ran),
        "basis": result.basis,
        "model": result.model,
        "prompt_version": result.prompt_version,
        "outcome": result.outcome.value,
        "attempts": int(result.attempts),
        "semantic_rank": int(result.rank),
        "strengths": ({r: s.label for r, s in sorted(result.strengths.items())}
                      if result.ran else {}),
    }
