"""Relevance classifier for the ISDS thematic watcher.

Three execution paths, selected by the ``MODEL_PROVIDER`` env var:

* ``gemini``           -> Google Generative AI (lazy import).
* ``claude``/``anthropic`` -> Anthropic Messages API (lazy import).
* unset / no API key / import failure -> offline keyword fallback.

The offline keyword path is the critical one for local dry-runs: it works
with NO API key and no third-party packages installed, scoring items purely
from ``fingerprint.yaml``.

``classify_item`` never raises -- on any provider error it falls back to the
keyword scorer so the pipeline always produces output.
"""

from __future__ import annotations

import hashlib
import json
import logging
import inspect
import os
import time
import re
from dataclasses import dataclass, field, fields
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from .sources.base import CandidateItem

logger = logging.getLogger("isds.classify")


# --------------------------------------------------------------------------- #
# Outcomes
# --------------------------------------------------------------------------- #
class ClassifyOutcome(str, Enum):
    """What actually happened to an item in the classifier.

    WHY THIS EXISTS. ``classify_item`` never raises, which is right — one bad
    item must not take a run down. But "never raises" was implemented as "always
    returns something publishable", and those are different promises. A provider
    outage returned a keyword score with an extra tag nobody reads, the item was
    marked seen, and the run reported it as classified. The failure left no trace
    anywhere a person or a guard would look. These five values are the trace.

      OK                     — the model classified it and we parsed the answer.
      KEYWORD_ONLY_BY_DESIGN — no model was expected and NONE WAS CALLED. Either
                               the caller asked for the keyword path, or no
                               provider/key is configured at all (the offline
                               dry-run case). A keyword score here is the
                               intended result, not a degraded one, so it
                               publishes and the item is marked seen. It carries
                               ``classify_attempts == 0``, always: nothing on
                               this route can make a call.
      KEYWORD_AFTER_PROVIDER_ERROR
                             — a model call WAS made for this item and it failed,
                               and the caller did not require a model answer, so
                               the keyword score it fell back to is where the
                               item was going anyway. TERMINAL for exactly the
                               reason KEYWORD_ONLY_BY_DESIGN is, and a separate
                               value because the EVENT is different: the
                               consequence is "publishes as a keyword score" and
                               the event is "an outage hit this item". Carries
                               ``classify_attempts >= 1`` on a live failure and
                               0 on the PROVIDER_DOWN canary route, where the run
                               had already proved no call could succeed.
      PARSE_FAILED           — the model answered and we could not parse it, even
                               after the strict retry.
      PROVIDER_ERROR         — the call itself failed on an item we intended to
                               model-classify.

    The first three are TERMINAL: the run is finished with the item. The last two
    are not, and ``src/main.py`` defers them rather than marking them seen — an
    item we failed to classify has not been processed, and recording it as
    processed is how a failure becomes permanent silently.

    WHY THE FIFTH VALUE EXISTS (added 2026-09-10, council special session row C).
    Across 2026-08-24, 08-31 and 09-07 the run record accumulated 141 tail items
    labelled KEYWORD_ONLY_BY_DESIGN, and every one of them carries
    ``classify_attempts == 1``: a call was made, it failed, and the record called
    it by design. NOT ONE record in the whole file carries ``attempts == 0``, so
    not one of them was ever in the genuine by-design state. The label was right
    about the consequence and wrong about the event, and it is the event that
    tells a reader an outage happened.

    THE 141 ARE NOT BACK-FILLED. The run record is append-only; the discrepancy
    is disclosed, not erased. ``src/rings.py::classification_state`` therefore
    keeps its existing rule that ``keyword_only_by_design`` with ``attempts > 0``
    is a PROVIDER_FAILURE, which is what keeps those 141 countable, and gains a
    second, direct rule for the new value. Nothing about the SCORE on this path
    changes: whether a tail item's keyword number should be published during an
    outage is policy, and policy is the operator's.

    AND THE COUNTER CANNOT CARRY THIS ON ITS OWN, which is the argument for a
    value rather than a convention. The PROVIDER_DOWN canary (added 2026-09-07)
    short-circuits before the first attempt is counted, so a tail item skipped by
    the canary would record ``keyword_only_by_design`` with ``attempts == 0`` —
    byte-identical to a genuine offline dry-run and invisible to the
    ``attempts > 0`` rule. No run has yet been archived on that route, so no
    historical record is affected; the hole was there to be fallen into.

    A str-valued Enum so the value serialises into metadata, telemetry, and
    ``state/seen.json`` without a conversion step at each boundary.
    """

    OK = "ok"
    KEYWORD_ONLY_BY_DESIGN = "keyword_only_by_design"
    KEYWORD_AFTER_PROVIDER_ERROR = "keyword_after_provider_error"
    PARSE_FAILED = "parse_failed"
    PROVIDER_ERROR = "provider_error"


# Outcomes after which the run is genuinely done with an item.
#
# KEYWORD_AFTER_PROVIDER_ERROR is here for the same reason KEYWORD_ONLY_BY_DESIGN
# is and for no other: the item got the result it was always going to get, so
# deferring it would re-fetch and re-score it every run forever to reach the same
# number. Naming the failure does not make the item unfinished. Whatever is added
# here must also be added to ``src.state.TERMINAL_SEEN_OUTCOMES`` or
# ``scripts/check_seen_integrity.py`` will (correctly) fail the build on the first
# item marked seen with it.
TERMINAL_OUTCOMES = frozenset({
    ClassifyOutcome.OK,
    ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN,
    ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR,
})

# THE authoritative location for an item's outcome: one key, in the metadata of
# the ClassifiedItem the classifier returns. Not a second return value, because
# every existing caller unpacks a single item; not a field on ClassifiedItem,
# because that dataclass is copied field-by-field in several places and a new
# field would have to be threaded through each of them.
OUTCOME_KEY = "outcome"


def outcome_of(ci) -> ClassifyOutcome:
    """The outcome recorded on a classified item.

    Defaults to OK for an item that carries none — anything constructed outside
    ``classify_item`` (tests, backtests, the research brief's own items) predates
    this and behaved as a success.
    """
    meta = getattr(ci, "metadata", None) or {}
    try:
        return ClassifyOutcome(meta.get(OUTCOME_KEY, ClassifyOutcome.OK.value))
    except ValueError:
        logger.warning("classify: unknown outcome %r on a classified item",
                       meta.get(OUTCOME_KEY))
        return ClassifyOutcome.OK

# The three valid ring keys. The LLM (and the keyword scorer) must only ever
# emit these. Kept here as the single source of truth for validation.
VALID_RINGS = (
    "ip_as_investment",
    "judicial_or_regulatory_measure",
    "jurisdictional_admissibility",
)

# Ring whose key carries "extra weight" -- a strong hit alone reaches MEDIUM.
EXTRA_WEIGHT_RING = "judicial_or_regulatory_measure"

# A ring counts as genuinely "present" once its keyword subtotal reaches this
# floor (i.e. at least one substantive keyword, not an incidental partial hit).
# Calibrated against fingerprint.yaml's few-shot examples: real two-ring cases
# clear 12+ per ring, while negative cases (mining, solar) only ever scrape
# single weak hits below it and therefore stay LOW.
PRESENT_FLOOR = 12

# A "strong" single-ring subtotal that, alone, justifies promotion to MEDIUM.
STRONG_SUBTOTAL = 18

# Truncate raw text before sending to an LLM to control token spend.
MAX_TEXT_CHARS = 6000

# Default model IDs (overridable via env).
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
# Anthropic Haiku 4.5 -- current fast/cheap model (full ID form).
from .models import DIGEST_CLASSIFIER_MODEL as DEFAULT_ANTHROPIC_MODEL  # single config location


def _resolved_model(provider) -> "Optional[str]":
    """The concrete model ID that would be used for a normalized provider name."""
    if provider == "gemini":
        return os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    if provider == "anthropic":
        return os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
    return None

_FINGERPRINT_PATH = Path(__file__).resolve().parent.parent / "fingerprint.yaml"

# Module-level cache for the parsed fingerprint.
_FINGERPRINT_CACHE: Optional[dict] = None


# --------------------------------------------------------------------------- #
# Data contract
# --------------------------------------------------------------------------- #
@dataclass
class ClassifiedItem(CandidateItem):
    """A CandidateItem enriched with classification output."""

    relevance_score: int = 0
    matched_rings: list[str] = field(default_factory=list)
    thematic_tags: list[str] = field(default_factory=list)
    digest_summary: str = ""


def from_candidate(
    item: CandidateItem,
    score: int,
    rings: list[str],
    tags: list[str],
    summary: str,
) -> ClassifiedItem:
    """Build a ClassifiedItem from a CandidateItem plus classification fields.

    Copies every field declared on CandidateItem so we never lose source data.
    """
    base_kwargs: dict[str, Any] = {
        f.name: getattr(item, f.name) for f in fields(CandidateItem)
    }
    return ClassifiedItem(
        relevance_score=int(score),
        matched_rings=list(rings),
        thematic_tags=list(tags),
        digest_summary=summary,
        **base_kwargs,
    )


# --------------------------------------------------------------------------- #
# Fingerprint loading
# --------------------------------------------------------------------------- #
def load_fingerprint(path: str | os.PathLike[str] = _FINGERPRINT_PATH) -> dict:
    """Load and cache ``fingerprint.yaml``.

    Uses PyYAML if available; otherwise falls back to a minimal parser is NOT
    attempted -- yaml is a hard dependency of the project, but we import it
    lazily so this module still imports cleanly if yaml is absent.
    """
    global _FINGERPRINT_CACHE
    if _FINGERPRINT_CACHE is not None:
        return _FINGERPRINT_CACHE

    import yaml  # lazy: keeps module import light and tolerant

    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    _FINGERPRINT_CACHE = data or {}
    return _FINGERPRINT_CACHE


def _snake_case(phrase: str) -> str:
    """Convert a keyword phrase into a snake_case thematic tag."""
    s = phrase.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s


# --------------------------------------------------------------------------- #
# Keyword pre-scorer (offline / dry-run path)
# --------------------------------------------------------------------------- #
def _item_text(item: CandidateItem) -> str:
    """Concatenate the searchable text fields of a candidate, lower-cased."""
    parts = [
        getattr(item, "title", "") or "",
        getattr(item, "summary", "") or "",
        getattr(item, "raw_text", "") or "",
    ]
    return " ".join(parts).lower()


def keyword_score(item: CandidateItem) -> dict:
    """Score an item against the keyword fingerprint (offline path).

    Returns a dict with keys: relevance_score (int), matched_rings (list),
    thematic_tags (list), digest_summary (str). Tags always include the
    ``keyword_fallback`` marker so downstream code can tell this came from the
    offline path.

    MATCHED IS NOT TOUCHED, and until 2026-09-10 it was (SD-3, council special
    session row E). ``matched_rings`` used to hold every ring with ANY nonzero
    hit — including a single 1-point brush on a phrase appearing in the clause
    that DENIES the ring — while the scoring grammar right below it counted a
    ring only from ``PRESENT_FLOOR``. So the published predicate "Rings matched"
    was looser than the predicate that produced the score beside it, and the
    mining example, which engages no ring substantively and scores 7, listed two
    rings. The fingerprint's own note called this out on 2026-08-04 and left it,
    on the stated ground that the digest archive had been published under the
    looser predicate. That ground has since expired: all sixteen archived runs
    ran ``classifier: claude``, so every published ring label came from the LLM
    path, and the string "Keyword-matched rings:" appears in zero published
    files. Nothing was published under it, so nothing is restated by fixing it.

      matched_rings  — rings at or above PRESENT_FLOOR. The PREDICATE. This is
                       what the score is computed from and it is now what the
                       label says. A strict subset of:
      touched_rings  — rings with any nonzero subtotal at all. The WORKING
                       DETAIL, kept because "no ring was anywhere near this" and
                       "one ring brushed it and fell short" are different facts
                       about a negative, and the second one is what a lexicon
                       re-weighting needs to see.

    The SCORE is not touched by this. ``present_rings`` was already the only
    thing the combination rules read; the change is that the reported set is now
    the same set, not a wider one.
    """
    fp = load_fingerprint()
    rings: dict = fp.get("rings", {}) or {}
    haystack = _item_text(item)

    per_ring_subtotal: dict[str, int] = {}
    matched_tags: list[str] = []

    for ring_key, ring_def in rings.items():
        subtotal = 0
        for kw in (ring_def or {}).get("keywords", []) or []:
            phrase = (kw.get("phrase") or "").lower().strip()
            if not phrase:
                continue
            if phrase in haystack:
                subtotal += int(kw.get("weight", 0))
                tag = _snake_case(phrase)
                if tag and tag not in matched_tags:
                    matched_tags.append(tag)
        if subtotal > 0:
            per_ring_subtotal[ring_key] = min(subtotal, 100)

    # Every ring the text brushed at all, in fingerprint order. NOT the reported
    # predicate — see the docstring. `matched_rings` is derived from
    # `present_rings` below, once the floor has been applied.
    touched_rings = list(per_ring_subtotal.keys())

    # Negative-signal detection.
    negative_present = False
    for sig in fp.get("negative_signals", []) or []:
        # Negative signals are descriptive phrases; match on their salient
        # tokens (split on slashes/commas) rather than the whole string.
        for token in re.split(r"[/,]", str(sig)):
            token = token.strip().lower()
            # Require a reasonably specific token to avoid spurious matches.
            if len(token) >= 5 and token in haystack:
                negative_present = True
                break
        if negative_present:
            break

    # A ring is genuinely "present" only at/above PRESENT_FLOOR; this filters
    # out incidental single-keyword hits so negative cases (mining, solar) that
    # merely brush one keyword don't get promoted into a ring intersection.
    present_rings = [r for r, s in per_ring_subtotal.items() if s >= PRESENT_FLOOR]

    # THE REPORTED PREDICATE IS THE SCORED PREDICATE. One assignment, and it is
    # the whole of SD-3: what we say we matched is what the score was computed
    # from. A separate list (rather than an alias) because `present_rings` is
    # read below and a caller holding the returned list must not be able to
    # mutate what the scorer is still using.
    matched_rings = list(present_rings)

    # --- Apply combination_rules in code ---------------------------------- #
    score = 0

    if len(present_rings) >= 2:
        # Intersection of two or more rings -> HIGH (spec: any two rings -> HIGH).
        combined = sum(per_ring_subtotal[r] for r in present_rings)
        score = min(95, 70 + combined // 12)
    elif len(present_rings) == 1:
        only = present_rings[0]
        sub = per_ring_subtotal[only]
        # Is there a real-but-sub-floor second ring also in play?
        second = any(r != only and s > 0 for r, s in per_ring_subtotal.items())
        if only == EXTRA_WEIGHT_RING:
            # Judicial/regulatory measure alone -> at least MEDIUM (extra weight).
            score = min(69, 45 + (sub - PRESENT_FLOOR) // 2 + (4 if second else 0))
        elif sub >= STRONG_SUBTOTAL or second:
            # Strong single ring, or one ring + a weaker second tie -> MEDIUM.
            score = min(66, 40 + (sub - STRONG_SUBTOTAL) // 2 + (4 if second else 0))
        else:
            # Single ring, present but modest, no second ring -> high-LOW.
            score = min(39, 28 + (sub - PRESENT_FLOOR))
    elif per_ring_subtotal:
        # Only sub-floor incidental hits -> LOW (roughly the largest subtotal).
        score = min(39, max(per_ring_subtotal.values()))
    else:
        score = 0

    # Negative signal forces LOW unless a ring is genuinely PRESENT to rescue it
    # (an incidental sub-floor keyword does NOT rescue a mining/debt/energy case).
    if negative_present:
        rescued = (
            "ip_as_investment" in present_rings
            or EXTRA_WEIGHT_RING in present_rings
        )
        if not rescued:
            score = min(score, 35)

    matched_tags.append("keyword_fallback")

    title = getattr(item, "title", "") or "(untitled)"
    # The prose label reads off the PREDICATE, not the brushes. Before SD-3 this
    # sentence could say "Keyword-matched rings: ip_as_investment,
    # judicial_or_regulatory_measure" about the mining example — a score of 7,
    # both rings sub-floor, and one of them lit by a phrase in the clause that
    # denies it. "none" is now a thing this sentence can truthfully say.
    ring_label = ", ".join(matched_rings) if matched_rings else "none"
    digest = (
        f"{title}. Keyword-matched rings: {ring_label}."
    )

    return {
        "relevance_score": int(score),
        "matched_rings": matched_rings,
        "thematic_tags": matched_tags,
        "digest_summary": digest,
        # The working detail behind the score, which the score itself discards.
        # A single number cannot tell you whether a 41 came from two rings barely
        # clearing the floor or one strong ring plus a brush, and that difference
        # is the whole question when the lexicon is re-weighted. Additive keys —
        # every existing caller reads the four above by name.
        "per_ring_subtotal": dict(per_ring_subtotal),
        "negative_signal": negative_present,
        # The broader set `matched_rings` used to be. Kept rather than dropped
        # because narrowing the predicate must not destroy the evidence for
        # widening it again: `matched_rings ⊆ touched_rings` always, and the
        # difference is exactly the sub-floor brushes. Derivable from
        # `per_ring_subtotal`, and named anyway, because a caller that has to
        # re-apply the floor to find out what the floor excluded is a caller that
        # will re-apply it slightly differently.
        "touched_rings": touched_rings,
    }


# --------------------------------------------------------------------------- #
# Prompt building
# --------------------------------------------------------------------------- #
_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "classifier.txt"
_PROMPT_CACHE: Optional[str] = None


def _load_prompt_template() -> str:
    global _PROMPT_CACHE
    if _PROMPT_CACHE is None:
        with open(_PROMPT_PATH, "r", encoding="utf-8") as fh:
            _PROMPT_CACHE = fh.read()
    return _PROMPT_CACHE


def prompt_version() -> str:
    """A short content hash of the classifier prompt.

    Scores are only comparable across runs that asked the same question. The
    prompt is edited from time to time and nothing has ever recorded which
    version produced a given score, so a shift in the score distribution has
    always been indistinguishable from a shift in the prompt. Hashing the file
    is enough: it changes exactly when the prompt changes, needs no version
    number anyone has to remember to bump, and costs one read per process.
    Returns "unknown" if the prompt cannot be read — telemetry must never be the
    reason a run fails.
    """
    try:
        return hashlib.sha256(
            _load_prompt_template().encode("utf-8")).hexdigest()[:12]
    except OSError:
        return "unknown"


def build_prompt(item: CandidateItem) -> str:
    """Render the classifier prompt with the candidate item's fields."""
    template = _load_prompt_template()

    title = getattr(item, "title", "") or ""
    source = getattr(item, "source", "") or ""
    url = getattr(item, "url", "") or ""

    text = getattr(item, "raw_text", "") or getattr(item, "summary", "") or ""
    if len(text) > MAX_TEXT_CHARS:
        text = text[:MAX_TEXT_CHARS]

    return (
        template.replace("{{TITLE}}", title)
        .replace("{{SOURCE}}", source)
        .replace("{{URL}}", url)
        .replace("{{TEXT}}", text)
    )


# --------------------------------------------------------------------------- #
# Response parsing
# --------------------------------------------------------------------------- #
def parse_json_response(text: str) -> Optional[dict]:
    """Parse a strict-JSON classifier response.

    Strips markdown fences, extracts the first ``{...}`` block, validates the
    required keys and types, and coerces ``matched_rings`` to the valid set.
    Returns None if the response is unusable.
    """
    if not text:
        return None

    cleaned = text.strip()

    # Strip a leading/trailing markdown code fence if present.
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1).strip()
    else:
        # Strip stray backticks.
        cleaned = cleaned.strip("`").strip()

    # Find the first balanced-ish JSON object.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    blob = cleaned[start : end + 1]

    try:
        data = json.loads(blob)
    except (ValueError, TypeError):
        return None

    if not isinstance(data, dict):
        return None

    # Validate required keys / types.
    score = data.get("relevance_score")
    rings = data.get("matched_rings")
    tags = data.get("thematic_tags")
    summary = data.get("digest_summary")

    if not isinstance(score, int) or isinstance(score, bool):
        # Allow numeric strings / floats by coercion.
        try:
            score = int(score)
        except (ValueError, TypeError):
            return None
    if not isinstance(rings, list):
        return None
    if not isinstance(tags, list):
        return None
    if not isinstance(summary, str):
        return None

    # Coerce rings to the three valid keys only.
    coerced_rings = [r for r in rings if r in VALID_RINGS]
    coerced_tags = [str(t) for t in tags]

    # Clamp score into [0, 100].
    score = max(0, min(100, int(score)))

    # Optional: a verbatim, citable notable line the model lifted from the text.
    quote = data.get("notable_quote")
    quote = quote.strip().strip('"').strip() if isinstance(quote, str) else ""

    return {
        "relevance_score": score,
        "matched_rings": coerced_rings,
        "thematic_tags": coerced_tags,
        "digest_summary": summary,
        "notable_quote": quote,
    }


# --------------------------------------------------------------------------- #
# LLM provider paths (lazy imports)
# --------------------------------------------------------------------------- #
def _call_gemini(prompt: str) -> str:
    """Call Google Generative AI and return the raw text response."""
    import google.generativeai as genai  # lazy import

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model_name = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt, generation_config={"temperature": 0})
    return getattr(resp, "text", "") or ""


def _call_anthropic(prompt: str) -> str:
    """Call the Anthropic Messages API and return the raw text response."""
    import anthropic  # lazy import

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    model_name = os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
    resp = client.messages.create(
        **_anthropic_create_kwargs(client.messages.create, model_name, prompt))
    # resp.content is a list of content blocks; the first is the text block.
    if resp.content and getattr(resp.content[0], "text", None) is not None:
        return resp.content[0].text or ""
    return ""


def _anthropic_create_kwargs(create, model_name: str, prompt: str) -> dict:
    """Build the ``Messages.create()`` kwargs the INSTALLED SDK actually accepts.

    2026-09-07 incident. The anthropic 1.x SDK removed ``temperature`` (and
    ``top_p``/``top_k``) from ``Messages.create()``. requirements.txt pinned
    ``anthropic>=0.40`` with no ceiling, the runner installed 1.4.0, and every
    classify call died with "got an unexpected keyword argument 'temperature'"
    — 24 of 110 candidates at the 18:02 UTC run, 28 of 28 at 20:54 — while the
    local SDK (0.107.x) still accepted the kwarg, so nothing failed locally.
    Sixteen deferred items sat one failure from abandonment.

    ``temperature=0`` was a nicety: the classifier's real guarantees are the
    JSON contract and the fail-closed parse. So it is passed only when the
    signature has it, and the test suite checks this builder against the real
    installed SDK in CI, where the break would have been caught before a run.
    """
    kwargs = {
        "model": model_name,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        params = inspect.signature(create).parameters
    except (TypeError, ValueError):  # builtins / C-implemented callables
        params = {}
    if "temperature" in params:
        kwargs["temperature"] = 0
    return kwargs


def _normalize_provider(provider: Optional[str]) -> Optional[str]:
    if not provider:
        return None
    p = provider.strip().lower()
    if p in ("claude", "anthropic"):
        return "anthropic"
    if p == "gemini":
        return "gemini"
    return None


def _provider_ready(provider: str) -> bool:
    """True if the required API key env var for the provider is present."""
    if provider == "gemini":
        return bool(os.environ.get("GEMINI_API_KEY"))
    if provider == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    return False


# Smart/curly quote and dash characters normalized to their ASCII equivalents
# before the substring check, so a quote that only differs by typography still
# verifies against the source.
_QUOTE_TRANSLATE = str.maketrans({
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "–": "-", "—": "-", "−": "-",
    " ": " ",
})


def _normalize_for_match(s: str) -> str:
    """Lower-case, collapse whitespace, and fold smart quotes/dashes to ASCII."""
    s = (s or "").translate(_QUOTE_TRANSLATE)
    return re.sub(r"\s+", " ", s).strip().lower()


def _quote_in_source(quote: str, item: CandidateItem) -> bool:
    """True if ``quote`` is a normalized substring (>=20 chars) of item text.

    Guards against the LLM paraphrasing a "verbatim" notable_quote: we only
    trust the quote if it actually appears in the item's source text. Whitespace
    and quote/dash typography are normalized first so a genuine quote isn't
    rejected over a curly-vs-straight quote mark.
    """
    if not quote:
        return False
    q = _normalize_for_match(quote)
    hay = _normalize_for_match(
        getattr(item, "raw_text", "")
        + " "
        + getattr(item, "summary", "")
        + " "
        + getattr(item, "title", "")
    )
    return len(q) >= 20 and q in hay


# --------------------------------------------------------------------------- #
# Main entry point
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# Provider canary (2026-09-07)
# --------------------------------------------------------------------------- #
# Set by main() for the duration of one run when the canary fails. While it is
# set, classify_item makes NO model call and returns the same PROVIDER_ERROR
# outcome a live failure would, with attempts=0 — so a dead provider costs the
# run nothing per item and, in main, charges no item an attempt.
PROVIDER_DOWN: Optional[str] = None
CANARY_PROMPT = "Reply with the single word OK."
# Back-off between canary attempts for API-side errors (overload, rate limit,
# network). Tests set this to (0, 0).
CANARY_BACKOFF_S = (2.0, 5.0)


def provider_canary(provider: Optional[str]) -> tuple[bool, str]:
    """One trivial model call before the run fetches or charges anything.

    Returns ``(True, note)`` when a model answered — or when no provider is
    configured, which is the designed keyword-fallback state and not an outage.
    Returns ``(False, detail)`` when no call can succeed this run:

    * a ``TypeError``/``AttributeError`` is a CONTRACT error — our code and the
      installed SDK disagree (the 2026-09-07 case: anthropic 1.x dropped
      ``temperature``). Retrying cannot help, so it fails at once and says so.
    * any other exception is treated as an API-side outage and retried
      ``len(CANARY_BACKOFF_S)`` more times with back-off before giving up.

    Never raises.
    """
    norm = _normalize_provider(provider if provider is not None
                               else os.environ.get("MODEL_PROVIDER"))
    if norm is None or not _provider_ready(norm):
        return True, "no provider/key configured; keyword fallback by design"
    caller = _call_gemini if norm == "gemini" else _call_anthropic
    last: Optional[BaseException] = None
    tries = 1 + len(CANARY_BACKOFF_S)
    for i in range(tries):
        try:
            caller(CANARY_PROMPT)
            return True, f"{norm} answered the canary (attempt {i + 1})"
        except (TypeError, AttributeError) as exc:
            return False, (f"contract error between src/classify.py and the installed "
                           f"{norm} SDK — not retried: {exc}")
        except Exception as exc:  # noqa: BLE001 - the canary never raises
            last = exc
            if i < len(CANARY_BACKOFF_S):
                time.sleep(CANARY_BACKOFF_S[i])
    return False, f"{norm} failed the canary {tries} times: {last!r}"


def classify_item(
    item: CandidateItem,
    provider: Optional[str] = None,
    *,
    intended_model: bool = True,
) -> ClassifiedItem:
    """Classify a single candidate. Never raises.

    Falls back to the offline keyword scorer when no provider/key is available
    or when the LLM path errors out. Every return path records its
    ``ClassifyOutcome`` under ``metadata["outcome"]``; see that enum for why.

    ``intended_model`` says whether the CALLER required a model classification
    for this item. It changes nothing about which path runs — only what a
    provider failure means. For the enriched top set the answer is yes, so a
    provider error is a real failure and the keyword number behind it is NOT
    published (it is kept as ``metadata["keyword_score_advisory"]`` so telemetry
    can later cost out an outage without the digest ever having shown it). For
    the tail, where a keyword score was always the expected result, a provider
    error just lands where the item was going anyway and publishes normally.

    A note on routing, since the difference has bitten before: passing
    ``provider=None`` does NOT force the keyword path — it falls through to the
    ``MODEL_PROVIDER`` environment variable, so with a provider configured, the
    "tail" is model-classified too. That is existing behaviour and this change
    deliberately leaves it alone; ``intended_model`` is about how we treat a
    failure, not about suppressing a call.
    """
    raw_provider = provider if provider is not None else os.environ.get("MODEL_PROVIDER")
    norm = _normalize_provider(raw_provider)

    # No provider configured / unknown -> offline fallback. This is a designed
    # state, not a degradation: it is how --dry-run works with no API key.
    if norm is None or not _provider_ready(norm):
        logger.info("classify: using keyword fallback (no provider/key)")
        result = keyword_score(item)
        ci = from_candidate(
            item,
            result["relevance_score"],
            result["matched_rings"],
            result["thematic_tags"],
            result["digest_summary"],
        )
        ci.metadata = {
            **(ci.metadata or {}),
            "model": "keyword",
            "classify_path": "keyword",
            "classify_attempts": 0,
            "retried_strict": False,
            OUTCOME_KEY: ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN.value,
        }
        return ci

    caller = _call_gemini if norm == "gemini" else _call_anthropic
    model_id = _resolved_model(norm)
    attempts = 0
    retried_strict = False

    try:
        if PROVIDER_DOWN:
            # The run's canary already proved no model call can succeed. Do not
            # make one per item: the except-branch below turns this into the
            # same PROVIDER_ERROR outcome a live failure would, attempts=0.
            raise RuntimeError(f"skipped, provider down this run: {PROVIDER_DOWN}")
        prompt = build_prompt(item)
        attempts += 1
        text = caller(prompt)
        parsed = parse_json_response(text)

        if parsed is None:
            # Retry once with a stricter instruction appended.
            strict_prompt = (
                prompt
                + "\n\nReturn ONLY the raw JSON object, no prose, no code fences."
            )
            retried_strict = True
            attempts += 1
            text = caller(strict_prompt)
            parsed = parse_json_response(text)

        if parsed is None:
            logger.warning(
                "classify: JSON parse failed after retry for %s",
                getattr(item, "url", "") or getattr(item, "title", ""),
            )
            ci = from_candidate(
                item,
                0,
                [],
                ["classification_failed"],
                "Classification failed after retry.",
            )
            ci.metadata = {
                **(ci.metadata or {}),
                "model": model_id,
                "classify_path": "llm",
                "classify_attempts": attempts,
                "retried_strict": retried_strict,
                OUTCOME_KEY: ClassifyOutcome.PARSE_FAILED.value,
            }
            return ci

        ci = from_candidate(
            item,
            parsed["relevance_score"],
            parsed["matched_rings"],
            parsed["thematic_tags"],
            parsed["digest_summary"],
        )
        # Record the concrete model ID that produced this classification.
        ci.metadata = {
            **(ci.metadata or {}),
            "model": model_id,
            "classify_path": "llm",
            "classify_attempts": attempts,
            "retried_strict": retried_strict,
            OUTCOME_KEY: ClassifyOutcome.OK.value,
        }
        # The model selects the single most citable verbatim line; prefer it
        # over the keyword heuristic when present.
        nq = parsed.get("notable_quote") or ""
        if nq and _quote_in_source(nq, item):
            ci.metadata = {**(ci.metadata or {}), "notable_quote": nq}
        elif nq:
            logger.info(
                "classify: rejecting LLM notable_quote as unverifiable "
                "(not a verbatim substring of source) for %s",
                getattr(item, "url", "") or getattr(item, "title", ""),
            )
        return ci

    except Exception as exc:  # noqa: BLE001 - never let the pipeline crash
        logger.warning(
            "classify: provider error (%s) for %s: %s",
            norm,
            getattr(item, "url", "") or getattr(item, "title", ""),
            exc,
        )
        result = keyword_score(item)
        tags = list(result["thematic_tags"])
        tags.append("classification_error_fallback")
        if intended_model:
            # We meant to ask the model and could not. The keyword number is a
            # measurement of a different instrument, and publishing it under the
            # model's name is what made four weeks of outage look like four weeks
            # of low-scoring news. Score 0 so it cannot be surfaced even if a
            # caller forgets to check the outcome; the number is kept as advisory.
            ci = from_candidate(item, 0, result["matched_rings"], tags,
                                result["digest_summary"])
            ci.metadata = {
                **(ci.metadata or {}),
                "model": model_id,
                "classify_path": "llm",
                "classify_attempts": attempts,
                "retried_strict": retried_strict,
                "keyword_score_advisory": int(result["relevance_score"]),
                OUTCOME_KEY: ClassifyOutcome.PROVIDER_ERROR.value,
            }
            return ci
        ci = from_candidate(
            item,
            result["relevance_score"],
            result["matched_rings"],
            tags,
            result["digest_summary"],
        )
        ci.metadata = {
            **(ci.metadata or {}),
            "model": "keyword",
            "classify_path": "keyword",
            "classify_attempts": attempts,
            "retried_strict": retried_strict,
            # NOT KEYWORD_ONLY_BY_DESIGN. We are in the except branch: the run
            # tried to model-classify this item and could not. The keyword score
            # still publishes and the item is still terminal — that is the
            # CONSEQUENCE, and it is unchanged — but the record now names the
            # EVENT instead of calling an outage a design.
            #
            # `attempts` is 1 or 2 on a live provider failure and 0 on the
            # PROVIDER_DOWN canary short-circuit above, which raises before the
            # first increment because the run already proved no call can succeed.
            # That zero is the reason this value has to exist rather than being
            # inferred: `rings.classification_state` recovers an outage from
            # `keyword_only_by_design` + `attempts > 0`, and on the canary route
            # there is no attempt to count, so the old label was
            # indistinguishable from a genuine offline run. The outcome says it
            # now; nothing has to be inferred from a counter.
            OUTCOME_KEY: ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR.value,
        }
        return ci


def classify_all(
    items: list[CandidateItem], provider: Optional[str] = None
) -> list[ClassifiedItem]:
    """Classify a list of candidates."""
    return [classify_item(item, provider=provider) for item in items]
