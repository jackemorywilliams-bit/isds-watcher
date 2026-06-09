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

import json
import logging
import os
import re
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Optional

from .sources.base import CandidateItem

logger = logging.getLogger("isds.classify")

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
DEFAULT_ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"

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

    matched_rings = list(per_ring_subtotal.keys())

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
    ring_label = ", ".join(matched_rings) if matched_rings else "none"
    digest = (
        f"{title}. Keyword-matched rings: {ring_label}."
    )

    return {
        "relevance_score": int(score),
        "matched_rings": matched_rings,
        "thematic_tags": matched_tags,
        "digest_summary": digest,
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
    resp = model.generate_content(prompt)
    return getattr(resp, "text", "") or ""


def _call_anthropic(prompt: str) -> str:
    """Call the Anthropic Messages API and return the raw text response."""
    import anthropic  # lazy import

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    model_name = os.environ.get("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL)
    resp = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    # resp.content is a list of content blocks; the first is the text block.
    if resp.content and getattr(resp.content[0], "text", None) is not None:
        return resp.content[0].text or ""
    return ""


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


# --------------------------------------------------------------------------- #
# Main entry point
# --------------------------------------------------------------------------- #
def classify_item(
    item: CandidateItem, provider: Optional[str] = None
) -> ClassifiedItem:
    """Classify a single candidate. Never raises.

    Falls back to the offline keyword scorer when no provider/key is available
    or when the LLM path errors out.
    """
    raw_provider = provider if provider is not None else os.environ.get("MODEL_PROVIDER")
    norm = _normalize_provider(raw_provider)

    # No provider configured / unknown -> offline fallback.
    if norm is None or not _provider_ready(norm):
        logger.info("classify: using keyword fallback (no provider/key)")
        result = keyword_score(item)
        return from_candidate(
            item,
            result["relevance_score"],
            result["matched_rings"],
            result["thematic_tags"],
            result["digest_summary"],
        )

    caller = _call_gemini if norm == "gemini" else _call_anthropic

    try:
        prompt = build_prompt(item)
        text = caller(prompt)
        parsed = parse_json_response(text)

        if parsed is None:
            # Retry once with a stricter instruction appended.
            strict_prompt = (
                prompt
                + "\n\nReturn ONLY the raw JSON object, no prose, no code fences."
            )
            text = caller(strict_prompt)
            parsed = parse_json_response(text)

        if parsed is None:
            logger.warning(
                "classify: JSON parse failed after retry for %s",
                getattr(item, "url", "") or getattr(item, "title", ""),
            )
            return from_candidate(
                item,
                0,
                [],
                ["classification_failed"],
                "Classification failed after retry.",
            )

        ci = from_candidate(
            item,
            parsed["relevance_score"],
            parsed["matched_rings"],
            parsed["thematic_tags"],
            parsed["digest_summary"],
        )
        # The model selects the single most citable verbatim line; prefer it
        # over the keyword heuristic when present.
        nq = parsed.get("notable_quote") or ""
        if nq:
            ci.metadata = {**(ci.metadata or {}), "notable_quote": nq}
        return ci

    except Exception as exc:  # noqa: BLE001 - never let the pipeline crash
        logger.warning(
            "classify: provider error (%s), falling back to keywords: %s",
            norm,
            exc,
        )
        result = keyword_score(item)
        tags = list(result["thematic_tags"])
        tags.append("classification_error_fallback")
        return from_candidate(
            item,
            result["relevance_score"],
            result["matched_rings"],
            tags,
            result["digest_summary"],
        )


def classify_all(
    items: list[CandidateItem], provider: Optional[str] = None
) -> list[ClassifiedItem]:
    """Classify a list of candidates."""
    return [classify_item(item, provider=provider) for item in items]
