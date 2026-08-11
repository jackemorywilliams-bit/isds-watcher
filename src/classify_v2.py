"""The V2 (ring-contract) classification call: per-ring strength AND evidence.

WHY THIS EXISTS. `src/rings.py` shipped able to check evidence spans, and
nothing was giving it any. Production runs `prompts/classifier.txt`, which
returns a bare list of ring names with no evidence for any of them, so every
model-claimed ring reached `merged_finding` with an empty span, failed
verification by construction, and recorded as `SEMANTIC_UNVERIFIED` at ABSENT
strength. Every operative strength therefore came from the lexical subtotals
alone. That is a lexical derivation, and it was being written to telemetry in a
section called `verdict_v2` beside a model id — which reads as though a model
produced it. Lexical-only shadowing sold as parity is the audit's core
objection and it was a fair one.

This module is the other half. It asks `prompts/classifier_v2.txt` — which
demands a strength and a VERBATIM SPAN per ring — parses the answer strictly,
and hands the spans to `rings.verify_span`, which checks them in code against
the item's own fields. A span that is not in the document contributes nothing,
and the fact that it contributed nothing is recorded as a demotion.

THE THING THIS MODULE MUST NEVER DO is the thing it was built to fix. If no
provider is configured, or the call fails, or the answer will not parse, the
derivation falls back to lexical — and it must then be LABELLED lexical.
`v2_basis` is that label, it is computed here next to the event it describes,
and `RingVerdict.to_telemetry` writes it on every record. A silent fallback
reported under the requested model's identity is the named defect; the basis
values are constructed so that the model id literally cannot appear on a record
whose findings a model did not produce, and `tests/test_classify_v2.py` asserts
it over every failure route.

COST. A V2 call is a SECOND paid call for an item production has already paid
to classify once, so this module is off unless asked for: see
`config.V2_SHADOW_CALLS`, default "off". Nothing here is reached in a default
run and no default run's cost changes by a cent.

DETERMINISM. No wall clock and no randomness. The sampling decision is made by
the caller from the run's own deterministic rank order, and the parser is a
closed grammar — every accepted field is one of a fixed set of literals or a
string, and anything else is a parse failure rather than a coercion.
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
from .classify import MAX_TEXT_CHARS, VALID_RINGS, ClassifyOutcome
from .rings import RINGS, V2_BASIS_LEXICAL_ONLY, Nexus, Strength

# The provider plumbing is reached through the MODULE, never imported by name.
# `from .classify import _call_anthropic` would bind the function object at
# import time, so a test that patches `src.classify._call_anthropic` — which is
# how every existing test in this repo stubs a provider — would patch a name
# this module no longer reads, and the stub would silently not apply. One
# convention, one patch point.

logger = logging.getLogger("isds.classify_v2")

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "classifier_v2.txt"
_PROMPT_CACHE: Optional[str] = None

# The four strength words, mapped to the ladder. A closed list: the prompt says
# "no 'moderate', no 'medium', no numbers", and this is where that is enforced
# rather than hoped for.
STRENGTH_WORDS = {
    "absent": Strength.ABSENT,
    "weak": Strength.WEAK,
    "present": Strength.PRESENT,
    "strong": Strength.STRONG,
}

NEXUS_WORDS = {n.value: n for n in Nexus}


# --------------------------------------------------------------------------- #
# v2_basis — what produced the verdict, recorded next to the event
# --------------------------------------------------------------------------- #
# V2_BASIS_LEXICAL_ONLY is imported from `src/rings.py`, which owns the field it
# is written to. It is the honest description of a run in which no V2 model
# response contributed anything: the flag is off, or this item was not in the
# sample, or no provider is configured at all.
#
# A call was made and failed at the transport/provider level.
V2_BASIS_PROVIDER_ERROR = "semantic_unavailable_provider_error"
# A call was made, the provider answered, and the answer would not parse even
# after the strict retry. R2.1 relies on malformed-vs-provider-failure being a
# binding distinction (see rings.ClassifyState), so it is not collapsed into the
# line above: one of these is somebody else's infrastructure and the other is
# our prompt, and a week of each looks identical if they share a label.
V2_BASIS_MALFORMED = "semantic_unavailable_malformed_output"

_SEMANTIC_PREFIX = "semantic:"


def semantic_basis(model_id: str) -> str:
    """``semantic:<MODELID>`` — the ONLY basis value that names a model.

    Reachable from exactly one place in this file: the branch in which a V2
    response was received, parsed, and used. That is the whole point of routing
    every basis value through named constants — a model id cannot get onto a
    record by a fallback path, because no fallback path can construct one.
    """
    return f"{_SEMANTIC_PREFIX}{model_id}"


def basis_names_a_model(basis: str) -> bool:
    return str(basis or "").startswith(_SEMANTIC_PREFIX)


def basis_is_semantic(basis: str) -> bool:
    """Whether the findings actually rest on a parsed model response."""
    return basis_names_a_model(basis)


# --------------------------------------------------------------------------- #
# Prompt
# --------------------------------------------------------------------------- #
def load_v2_prompt() -> str:
    global _PROMPT_CACHE
    if _PROMPT_CACHE is None:
        with open(_PROMPT_PATH, "r", encoding="utf-8") as fh:
            _PROMPT_CACHE = fh.read()
    return _PROMPT_CACHE


def v2_prompt_version() -> str:
    """A short content hash of the V2 prompt, for the same reason V1 has one:
    strengths are only comparable across runs that asked the same question."""
    try:
        return hashlib.sha256(load_v2_prompt().encode("utf-8")).hexdigest()[:12]
    except OSError:
        return "unknown"


def build_v2_prompt(item) -> str:
    """Render the V2 prompt for one candidate.

    Same substitution as `classify.build_prompt`, and the same trap: the item
    text token appears exactly ONCE in `prompts/classifier_v2.txt` and
    `str.replace` replaces every occurrence, so a second mention would inline a
    second copy of the body. The prompt's own header says so and a test counts
    the occurrences.
    """
    template = load_v2_prompt()
    text = getattr(item, "raw_text", "") or getattr(item, "summary", "") or ""
    if len(text) > MAX_TEXT_CHARS:
        text = text[:MAX_TEXT_CHARS]
    return (
        template.replace("{{TITLE}}", getattr(item, "title", "") or "")
        .replace("{{SOURCE}}", getattr(item, "source", "") or "")
        .replace("{{URL}}", getattr(item, "url", "") or "")
        .replace("{{TEXT}}", text)
    )


# --------------------------------------------------------------------------- #
# Strict parser
# --------------------------------------------------------------------------- #
_FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)


def parse_v2_response(text: str) -> Optional[dict]:
    """Parse a V2 answer, or return None. STRICT — it coerces nothing.

    The V1 parser is permissive by design: it coerces a numeric string to an
    int, drops ring names it does not recognise, and accepts whatever is left.
    That is the right shape for a parser whose output is a score nobody checks.
    It is the wrong shape here, because the output of this one is fed to an
    evidence rule, and a coercion is a small invention. So:

      * all three ring keys must be present, and NO fourth key may be — a model
        inventing a ring is exactly the event worth catching, and silently
        dropping it hides it;
      * every strength must be one of the four literal words, lower case after
        stripping. "medium" is a parse failure, not a guess;
      * every evidence_span must be a string (possibly "");
      * isds_nexus must be one of the four literal words;
      * a ring at present or strong with no span is a parse failure. The prompt
        requires one, and a strength with no evidence is precisely the V1 defect
        this contract exists to end — accepting it here would reintroduce it
        under a new field name.

    Returns a dict with normalised, closed-vocabulary values. Never raises.
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

    raw_rings = data.get("rings")
    if not isinstance(raw_rings, dict):
        return None
    if set(raw_rings) != set(VALID_RINGS):
        logger.info("classify_v2: ring key set %s is not the three rings",
                    sorted(raw_rings))
        return None

    parsed_rings: dict[str, dict] = {}
    for ring in RINGS:
        entry = raw_rings.get(ring)
        if not isinstance(entry, dict):
            return None
        word = entry.get("strength")
        if not isinstance(word, str):
            return None
        strength = STRENGTH_WORDS.get(word.strip().lower())
        if strength is None:
            logger.info("classify_v2: %r is not one of the four strength words",
                        word)
            return None
        span = entry.get("evidence_span", "")
        if not isinstance(span, str):
            return None
        span = span.strip()
        if strength >= Strength.PRESENT and not span:
            logger.info("classify_v2: %s claimed %s with no evidence span",
                        ring, word)
            return None
        parsed_rings[ring] = {"strength": strength, "evidence_span": span}

    nexus_word = data.get("isds_nexus")
    if not isinstance(nexus_word, str):
        return None
    nexus = NEXUS_WORDS.get(nexus_word.strip().lower())
    if nexus is None:
        return None

    nexus_evidence = data.get("nexus_evidence", "")
    if not isinstance(nexus_evidence, str):
        return None

    tags = data.get("thematic_tags", [])
    if not isinstance(tags, list):
        return None
    summary = data.get("digest_summary", "")
    if not isinstance(summary, str):
        return None

    return {
        "rings": parsed_rings,
        "isds_nexus": nexus,
        "nexus_evidence": nexus_evidence.strip(),
        "thematic_tags": [str(t) for t in tags],
        "digest_summary": summary,
    }


# --------------------------------------------------------------------------- #
# The result
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class V2Result:
    """One V2 classification attempt, successful or not.

    ``basis`` is the load-bearing field and is never inferred by a caller: it is
    set on the same line as the outcome it describes. ``ok`` is defined as
    "basis names a model", not as "no exception was raised", so there is no way
    to read this object as a success while its basis says otherwise.
    """

    basis: str
    outcome: ClassifyOutcome
    model: str = ""
    prompt_version: str = ""
    attempts: int = 0
    retried_strict: bool = False
    strengths: dict = field(default_factory=dict)      # ring -> Strength
    spans: dict = field(default_factory=dict)          # ring -> str
    model_nexus: Optional[Nexus] = None
    nexus_evidence: str = ""
    thematic_tags: tuple = ()
    digest_summary: str = ""

    @property
    def ok(self) -> bool:
        return basis_is_semantic(self.basis)


def _lexical_only(reason_basis: str, outcome: ClassifyOutcome, *, model: str = "",
                  attempts: int = 0, retried_strict: bool = False) -> V2Result:
    """A result that contributed nothing, labelled with why.

    ``model`` is recorded for the operational question "which model was down"
    and is deliberately NOT folded into ``basis``: the basis is what produced
    the findings, and on this path nothing did.
    """
    return V2Result(basis=reason_basis, outcome=outcome, model=model,
                    prompt_version=v2_prompt_version(), attempts=attempts,
                    retried_strict=retried_strict)


def classify_item_v2(item, provider: Optional[str] = None) -> V2Result:
    """Run the V2 prompt over one candidate. Never raises.

    Retry-once on an unparseable answer, exactly as `classify.classify_item`
    does, so the two paths fail the same way and `retried_strict` means the same
    thing in both records.
    """
    raw_provider = provider if provider is not None else os.environ.get("MODEL_PROVIDER")
    norm = _classify._normalize_provider(raw_provider)

    # No provider is not a failure — it is the offline state, and the honest
    # label for a derivation made in it is "lexical_only". KEYWORD_ONLY_BY_DESIGN
    # says the same thing in the outcome vocabulary.
    if norm is None or not _classify._provider_ready(norm):
        return _lexical_only(V2_BASIS_LEXICAL_ONLY,
                             ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN)

    def caller(text: str) -> str:
        fn = (_classify._call_gemini if norm == "gemini"
              else _classify._call_anthropic)
        return fn(text)

    model_id = _classify._resolved_model(norm) or ""
    attempts = 0
    retried_strict = False

    try:
        prompt = build_v2_prompt(item)
        attempts += 1
        parsed = parse_v2_response(caller(prompt))
        if parsed is None:
            retried_strict = True
            attempts += 1
            parsed = parse_v2_response(caller(
                prompt + "\n\nReturn ONLY the raw JSON object, no prose, "
                         "no code fences."))
        if parsed is None:
            logger.warning("classify_v2: unparseable after retry for %s",
                           getattr(item, "url", "") or getattr(item, "title", ""))
            return _lexical_only(V2_BASIS_MALFORMED, ClassifyOutcome.PARSE_FAILED,
                                 model=model_id, attempts=attempts,
                                 retried_strict=retried_strict)
    except Exception as exc:  # noqa: BLE001 - shadow work is never fatal
        logger.warning("classify_v2: provider error (%s) for %s: %s", norm,
                       getattr(item, "url", "") or getattr(item, "title", ""), exc)
        return _lexical_only(V2_BASIS_PROVIDER_ERROR, ClassifyOutcome.PROVIDER_ERROR,
                             model=model_id, attempts=attempts,
                             retried_strict=retried_strict)

    return V2Result(
        basis=semantic_basis(model_id),
        outcome=ClassifyOutcome.OK,
        model=model_id,
        prompt_version=v2_prompt_version(),
        attempts=attempts,
        retried_strict=retried_strict,
        strengths={r: parsed["rings"][r]["strength"] for r in RINGS},
        spans={r: parsed["rings"][r]["evidence_span"] for r in RINGS},
        model_nexus=parsed["isds_nexus"],
        nexus_evidence=parsed["nexus_evidence"],
        thematic_tags=tuple(parsed["thematic_tags"]),
        digest_summary=parsed["digest_summary"],
    )


def telemetry_section(result: Optional[V2Result], *, mode: str) -> dict:
    """The bounded record of a V2 call. No spans, no summary, no tags.

    The model's own nexus value is recorded as ADVISORY and is read by nothing:
    `rings.derive_nexus` is the authority, because a nexus asserted by the same
    model whose ring claims we are checking is not an independent check of them.
    Keeping it costs one enumerated string and lets a later query ask how often
    the two disagreed.
    """
    if result is None:
        return {
            "mode": mode,
            "called": False,
            "basis": V2_BASIS_LEXICAL_ONLY,
            "model": "",
            "prompt_version": "",
            "outcome": "",
            "attempts": 0,
            "retried_strict": False,
            "model_nexus_advisory": "",
        }
    return {
        "mode": mode,
        "called": True,
        "basis": result.basis,
        "model": result.model,
        "prompt_version": result.prompt_version,
        "outcome": result.outcome.value,
        "attempts": int(result.attempts),
        "retried_strict": bool(result.retried_strict),
        "model_nexus_advisory": ("" if result.model_nexus is None
                                 else result.model_nexus.value),
    }
