"""Configuration for the ISDS thematic watcher.

Recipients and the repo URL are hard-coded. Everything secret (SMTP creds,
LLM API keys) and the model provider come from the environment so nothing
sensitive lands in the repo.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger("isds.config")

# Hard-coded digest recipients. Temporarily narrowed to a single recipient on
# request; restore ximena.s.benavides@gmail.com here to resume sending to both.
RECIPIENTS = [
    "jackemorywilliams@icloud.com",
]

# Hybrid digest size. Report every item at or above `threshold` (a match); there is
# no upper cap, so a strong week shows all of them. When fewer items match, fill up
# to MIN_DIGEST_ITEMS with the closest near-misses, but only those at or above
# RELEVANCE_FLOOR. With the floor at 25 a genuinely quiet week may send only 0–3
# items rather than padding the digest to the minimum with weak near-misses.
MIN_DIGEST_ITEMS = 6
RELEVANCE_FLOOR = 25

# Publication safety: the fill is SUSPENDED by default while the classifier is
# under validation. Filling a thin week up to MIN_DIGEST_ITEMS with items scoring
# 25–39 means publishing, to a professor, items the instrument itself declined to
# call matches — and doing it precisely when the instrument found least, which is
# when its judgment is least worth borrowing against. No item has yet scored a
# true match (>=40), so nearly every item ever surfaced arrived through this fill.
# Items at or above the threshold are unaffected and publish normally: if a
# candidate genuinely clears, it is reported.
# Set FILL_FLOOR_SUSPENDED=0 to restore the fill.
FILL_FLOOR_SUSPENDED = os.getenv("FILL_FLOOR_SUSPENDED", "1").strip().lower() not in (
    "0", "false", "no", "off")

# Publication safety, the second and stronger gate: while VALIDATION_STATUS_ONLY is
# on, NO item-level entry is published or emailed at all — not the near-misses the
# fill used to carry, and not items at or above the threshold either. The cycle
# reports itself and nothing else.
#
# WHY A SECOND FLAG. Suspending the fill was argued for on the ground that no item
# has ever scored a true match, so the fill was the only path anything reached the
# professor by. That argument protects nothing against the one case it did not
# consider: an item that DOES clear 40. `prompts/classifier.txt` Example 4 teaches
# the model to score a construction denial-of-justice case — judicial ring only, no
# IP, no jurisdictional doctrine, off-theme on two of the three rings the research
# question is about — at 55. `select_surfaced` publishes on the score alone, and 55
# is over 40, so that item publishes today with the fill suspended. The classifier
# is under validation precisely because we cannot yet say what its scores mean; a
# gate that only holds back the scores it already distrusts is not a validation
# gate. This one holds everything.
#
# It is deliberately SEPARATE from FILL_FLOOR_SUSPENDED rather than a stronger
# setting of it: the fill flag exists to be turned off when the fill is
# reinstated, and turning it off must not, as a side effect, reopen item-level
# publication. The two are read independently and neither can disable the other.
#
# What continues while it is on: retrieval, enrichment, scoring, telemetry,
# retries, the deferred queue, archiving, and shadow classification. What stops:
# item-level digest entries and the Research Brief. Exactly one status message per
# cycle goes out (render.status_only_body), and when items were flagged internally
# at or above the threshold it says so, with a count — an operational fact, so a
# real match is held for review rather than silently sat on.
#
# Set VALIDATION_STATUS_ONLY=0 to publish items again. That is the decision the
# validation is for; it is not a runtime convenience.
VALIDATION_STATUS_ONLY = os.getenv(
    "VALIDATION_STATUS_ONLY", "1").strip().lower() not in ("0", "false", "no", "off")

# The R2.1 ring contract (src/rings.py): three named rings, per-ring evidence with
# a recorded location and verification status, an ISDS-nexus finding, and a lane
# derived from those predicates rather than from a score.
#
#   "off"    — not derived at all.
#   "shadow" — derived every run and written to telemetry as `verdict_v2`.
#              Changes NOTHING that is published, emailed, archived, or scored.
#              This is the default, because the only way to learn what the
#              contract would have decided across a real corpus is to run it
#              alongside the instrument for a while, and a derivation that
#              decides nothing costs nothing to be wrong about.
#   "on"     — publication-lane authority.
#
# "on" is not reachable yet, and the refusal below is deliberate rather than an
# oversight to be tidied up later. Two things have to happen first: the locked-set
# validation has to report (`analytics/locked_set/SCHEMA.md`), and the publication
# path has to actually be wired to consult the lane, which it is not. Between
# those, a stray environment variable that silently promoted a shadow derivation
# to publication authority would be the worst failure this repo could have — it
# would change what a professor receives, on the strength of a typo. So it fails
# closed to "shadow" and says so loudly.
STATE_MODEL_V2_MODES = ("off", "shadow", "on")
STATE_MODEL_V2_PUBLICATION_READY = False


def _state_model_v2_mode(raw: str | None = None) -> str:
    """Resolve STATE_MODEL_V2, refusing "on" until publication is wired."""
    value = (raw if raw is not None
             else os.getenv("STATE_MODEL_V2", "shadow")).strip().lower()
    if value not in STATE_MODEL_V2_MODES:
        logger.warning("config: STATE_MODEL_V2=%r is not one of %s; using 'shadow'",
                       value, STATE_MODEL_V2_MODES)
        return "shadow"
    if value == "on" and not STATE_MODEL_V2_PUBLICATION_READY:
        logger.error(
            "config: STATE_MODEL_V2=on asks the V2 lane derivation to decide what "
            "publishes. It has not been validated against the locked set and no "
            "publication path consults it. Running in shadow instead.")
        return "shadow"
    return value


STATE_MODEL_V2 = _state_model_v2_mode()

# --------------------------------------------------------------------------- #
# V2_SHADOW_CALLS — whether the V2 shadow may spend money, and how much
# --------------------------------------------------------------------------- #
# THE PROBLEM THIS SETTING EXISTS TO SOLVE. STATE_MODEL_V2="shadow" derives a
# lane every run. Until now it derived it from lexical subtotals only, because
# `prompts/classifier.txt` returns a bare ring list with no evidence spans, so
# every model-claimed ring failed verification by construction. `src/classify_v2.py`
# can now ask `prompts/classifier_v2.txt` for strengths WITH spans — but that is a
# SECOND paid call for an item production has already paid to classify once, and
# adding one silently is not a thing a shadow derivation gets to do.
#
#   "off"       — default. No V2 call is ever made. The shadow derivation stays
#                 lexical and every telemetry record says so: `v2_basis` is
#                 "lexical_only" and no model id appears on it anywhere.
#   "sample:N"  — at most N enriched candidates per run get a V2 call, taken
#                 from the top of the run's own deterministic rank order. Cost
#                 is bounded by N and measured: attempts land in telemetry.
#
#   "replace"   — FORBIDDEN, and refused below rather than merely undocumented.
#                 It would mean spending the V2 call INSTEAD of the legacy one,
#                 and the legacy record is what production gates on today. A
#                 shadow experiment does not get to stop the instrument's
#                 primary measurement.
#
# WHY THE DEFAULT IS "off" AND NOT "sample:3". Two reasons, and the first is the
# operator's rule rather than my preference. (1) The project runs under a
# standing zero-cost constraint; a recurring per-run charge, however small, is
# Emory's decision to make and not a side effect of a session that was asked to
# build the capability. (2) `analytics/locked_set/` is deliberately empty, so
# there is no validated instrument against which V2 strengths could be read yet
# — semantic shadow data collected now would be uncalibrated data, and the
# argument for collecting it is weaker than the argument for being able to.
# The route is built, wired and tested end to end; enabling it is one
# environment variable and no code change.
V2_SHADOW_CALLS_OFF = "off"
V2_SHADOW_SAMPLE_PREFIX = "sample:"
V2_SHADOW_CALLS_FORBIDDEN = ("replace",)


def _v2_shadow_calls(raw: str | None = None) -> tuple[str, int]:
    """Resolve V2_SHADOW_CALLS to ``(mode, sample_n)``. Fails closed to off."""
    value = (raw if raw is not None
             else os.getenv("V2_SHADOW_CALLS", V2_SHADOW_CALLS_OFF)).strip().lower()
    if value in ("", V2_SHADOW_CALLS_OFF):
        return V2_SHADOW_CALLS_OFF, 0
    if value in V2_SHADOW_CALLS_FORBIDDEN:
        logger.error(
            "config: V2_SHADOW_CALLS=%r would replace the legacy classification "
            "call, which is the one production still gates on. Refusing; the V2 "
            "shadow stays off.", value)
        return V2_SHADOW_CALLS_OFF, 0
    if value.startswith(V2_SHADOW_SAMPLE_PREFIX):
        raw_n = value[len(V2_SHADOW_SAMPLE_PREFIX):]
        try:
            n = int(raw_n)
        except ValueError:
            logger.warning("config: V2_SHADOW_CALLS=%r has a non-integer sample "
                           "size; using off", value)
            return V2_SHADOW_CALLS_OFF, 0
        if n <= 0:
            logger.warning("config: V2_SHADOW_CALLS=%r samples nothing; using off",
                           value)
            return V2_SHADOW_CALLS_OFF, 0
        return V2_SHADOW_SAMPLE_PREFIX.rstrip(":"), n
    logger.warning("config: V2_SHADOW_CALLS=%r is not 'off' or 'sample:N'; "
                   "using off", value)
    return V2_SHADOW_CALLS_OFF, 0


V2_SHADOW_CALLS_MODE, V2_SHADOW_SAMPLE_N = _v2_shadow_calls()

# The resolved setting as one string, for telemetry. "off" or "sample:3" — the
# RESOLVED value, not the raw environment variable, so a record says what the
# run actually did rather than what someone typed.
V2_SHADOW_CALLS_SPEC = (V2_SHADOW_CALLS_OFF
                        if V2_SHADOW_CALLS_MODE == V2_SHADOW_CALLS_OFF
                        else f"{V2_SHADOW_SAMPLE_PREFIX}{V2_SHADOW_SAMPLE_N}")

# Enrich at most this many top-ranked candidates by fetching their source page
# (bounds polite-fetch volume per run).
ENRICH_TOP_N = 24

# --------------------------------------------------------------------------- #
# TRIAGE_ENABLED — Workstream F, the semantic triage pass
# --------------------------------------------------------------------------- #
# A compact prompt (`prompts/triage.txt`) run over EVERY candidate's title and
# summary BEFORE enrichment, so that the ENRICH_TOP_N budget is allocated by
# combined semantic/lexical rank rather than by lexical rank alone. The problem
# it addresses is measurable in this repo's own probe suite: probe
# E5_einarsson_lexical_brittle is a paraphrase-heavy pharmaceutical-regulatory
# item whose expected band is HIGH and whose `keyword_score` is 0 — it can never
# reach enrichment, so it can never reach classification, so the instrument
# cannot see it at all. Ranking is the gate, and the gate is lexical.
#
# OFF BY DEFAULT, and that is a cost decision rather than a doubt about the
# design. Triage calls the model once per CANDIDATE, not once per enriched item:
# on the observed run sizes (median 14, max 80) at the R2.1 table's ~$0.0014 per
# call that is roughly $0.02 on a median run and $0.11 on the largest observed
# one. Small, recurring, and Emory's to authorise. Enabling it is one
# environment variable; nothing else changes.
TRIAGE_ENABLED = os.getenv("TRIAGE_ENABLED", "0").strip().lower() not in (
    "0", "false", "no", "off", "")

# Expected cost per triage call, from the R2.1 costing table (~600 input tokens,
# ~150 output). Recorded as a constant so the run can report what a triage pass
# cost instead of leaving it to be re-derived from memory.
TRIAGE_COST_PER_CALL_USD = 0.0014

# --------------------------------------------------------------------------- #
# TAIL_AUDIT_N — R2.1 design (c), stratified tail audit. STUB.
# --------------------------------------------------------------------------- #
# The full design samples N items from the un-enriched tail per run, classifies
# them, and reports what the enrichment cut is throwing away — the only way to
# measure the false-negative rate of the ranking step rather than assuming it.
#
# NOT BUILT. This session implemented the triage pass (design (a)) and the
# constrained headline lane; the audit loop needs a stratification rule, a
# persisted cross-run sample ledger so the strata are not re-drawn every run,
# and a reporting surface, and building it here would have meant building three
# things badly instead of two things properly. The constant exists so the
# decision is visible in configuration rather than remembered, and it is 0,
# which means no tail audit runs. Anything reading it must treat a non-zero
# value as unimplemented rather than as a request.
TAIL_AUDIT_N = 0

# The interpretive Research Brief (the council's second weekly email). Enabled by
# default; set RESEARCH_BRIEF_ENABLED=0 to suppress it. It requires the Anthropic
# provider (web search is an Anthropic server tool) and is skipped otherwise.
RESEARCH_BRIEF_ENABLED = os.getenv("RESEARCH_BRIEF_ENABLED", "1").strip().lower() not in (
    "0", "false", "no", "off", "")

# Deterministic, model-free citation verification for the Research Brief: after the
# editor runs, every cited URL is actually fetched and classified (ok / paywalled /
# unreachable) — the anti-hallucination control no model provides. Enabled by default;
# set CITATION_VERIFY=0 to skip the network fetches (e.g. offline or rate-limited).
CITATION_VERIFY = os.getenv("CITATION_VERIFY", "1").strip().lower() not in (
    "0", "false", "no", "off", "")

# The brief's INTEGRITY-CHECK stage: after the security officer vets the memo, run the
# model-free hallucination checker (scripts/check_citations.py) over the brief's own
# citations — resolving every cited URL AND recording URL-less bibliographic authorities
# (law-review articles, treatises, awards by case number) as "needs human verification" —
# and record a structured verdict (clean / flagged) the brief and ledger can surface.
# This covers the BRIEF and methodology-style citations, not just bare digest URLs.
# Enabled by default; set BRIEF_INTEGRITY_CHECK=0 to skip it (e.g. offline or
# rate-limited), mirroring the CITATION_VERIFY guard above.
BRIEF_INTEGRITY_CHECK = os.getenv("BRIEF_INTEGRITY_CHECK", "1").strip().lower() not in (
    "0", "false", "no", "off", "")

# Sources whose body we cannot read (paywalled / headline-only feeds). A
# "notable line" from one of these is necessarily headline text, never a
# verbatim quote from the source body, so the digest shows "N/A" for it rather
# than presenting the headline as a quotation.
HEADLINE_ONLY_SOURCES = {"iareporter_headlines"}

REPO_URL = "https://github.com/jackemorywilliams-bit/isds-watcher"
SITE_URL = "https://jackemorywilliams-bit.github.io/isds-watcher/"

# One-line description of the watch theme, surfaced in the digest footer.
THEME_ONE_LINER = (
    "ISDS at the intersection of IP-as-investment, regulatory/judicial measures "
    "as the disputed conduct, and jurisdictional/admissibility doctrines "
    "(abuse of right, treaty-shopping, denial of justice)."
)

# Must track fingerprint.yaml, which is the authority. This is only reached when that
# file cannot be read — and a fallback that differs from the authority does not fail,
# it silently scores a whole run at a threshold the project abandoned. It read 60,
# the pre-2026-07 value, long after the operator lowered the live threshold to 40.
# scripts/check_claims.py now fails if the two drift apart again.
_DEFAULT_THRESHOLD = 40


def _threshold_from_fingerprint(path: str = "fingerprint.yaml") -> int:
    """Read the threshold from fingerprint.yaml; fall back to _DEFAULT_THRESHOLD."""
    try:
        import yaml  # lazy: keep import-time deps minimal
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        val = data.get("threshold", _DEFAULT_THRESHOLD)
        return int(val)
    except Exception as exc:  # noqa: BLE001 - never crash on config
        logger.warning("config: could not read threshold from %s (%s); using %d",
                        path, exc, _DEFAULT_THRESHOLD)
        return _DEFAULT_THRESHOLD


@dataclass
class Config:
    model_provider: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str | None = None
    smtp_pass: str | None = None
    threshold: int = _DEFAULT_THRESHOLD


def load_config() -> Config:
    """Build a Config from the environment."""
    raw_pass = os.getenv("SMTP_PASS")
    smtp_pass = raw_pass.replace(" ", "") if raw_pass else raw_pass

    try:
        smtp_port = int(os.getenv("SMTP_PORT", "465"))
    except ValueError:
        logger.warning("config: SMTP_PORT not an int; defaulting to 465")
        smtp_port = 465

    return Config(
        model_provider=os.getenv("MODEL_PROVIDER"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=smtp_port,
        smtp_user=os.getenv("SMTP_USER"),
        smtp_pass=smtp_pass,
        threshold=_threshold_from_fingerprint(),
    )


def missing_email_secrets(cfg: Config) -> list[str]:
    """Return the names of any required SMTP secrets that are empty."""
    missing = []
    if not cfg.smtp_user:
        missing.append("SMTP_USER")
    if not cfg.smtp_pass:
        missing.append("SMTP_PASS")
    return missing
