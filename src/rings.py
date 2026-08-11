"""STATE_MODEL_V2 — the ring contract, as enforcement rather than as prose.

WHY THIS EXISTS. The instrument has always had three rings, and they have always
been the right three: IP-as-investment, a judicial or regulatory measure as the
disputed conduct, and jurisdictional/admissibility doctrine. What it has never
had is a rule connecting them to a decision. `src/classify.py` derives a number
on the keyword path and simply *accepts* one on the model path — the parser
"checks no consistency between score and rings, and requires no evidence for any
ring" (`analytics/instrument-map-2026-08-08.md` §5) — and `select_surfaced` then
publishes on the number. So the rings are, operationally, decoration on a score.

That is not a theoretical complaint. `prompts/classifier.txt` Example 4 teaches a
55 for a construction denial-of-justice case with no IP ring and no
jurisdictional ring: two of the three rings absent, and over the publication
threshold. The score is the whole decision, and the score can be off-theme.

This module is the replacement, and it replaces the DERIVATION, not the
instrument. The three rings are preserved exactly as named and are never
interchangeable — a jurisdictional ring is not an IP ring with a different label,
and the central failure this module prevents is the arithmetic that lets any two
present rings stand in for any other two. What changes is that a decision is
derived from findings, each finding carries its own evidence and the record of
how that evidence was checked, and the model's score is demoted to what it has
always actually been: advisory shadow data with no authority over any predicate.

THE FOUR RULES THAT DO THE WORK

  1. ABSENCE IS A FINDING, NOT A GAP. A verdict always carries exactly three
     findings. "We found no IP ring" and "we did not look for an IP ring" are
     different statements and the second one is not allowed to masquerade as the
     first. This is why `RingVerdict.findings` is length-3 by invariant.

  2. A NEGATIVE CONCLUSION REQUIRES HAVING READ SOMETHING. `isds_nexus` can only
     be ABSENT if an accessible body was actually read; on a headline, or after a
     failed fetch, the honest value is INDETERMINATE. The archive contains an
     annotation that reached a negative thematic conclusion about a body it never
     read (the Gazprom entry, §7 of the instrument map). Here that construction
     raises rather than rendering.

  3. EVIDENCE HAS A LOCATION AND THE LOCATION BINDS. A span found only in a title
     cannot carry a ring to present or strong; a headline-only source can never
     produce a MATCH. `_quote_in_source` in `src/classify.py` searches
     `raw_text + summary + title` as one string, and `iareporter_headlines` sets
     `raw_text = title`, so a headline currently verifies as a body quote. Here
     the fields are checked separately and named in the finding.

  4. THE MODEL'S NUMBER CANNOT OVERRIDE A PREDICATE. `model_score_advisory` is
     recorded and is read by nothing in `derive_lane`. A 95 with no IP ring is
     still not a MATCH; a 55 for Example 4 is still not a MATCH.

THE LANE PARTITION (R2.1), as one ordered, total, single-valued procedure:

    RETRY                       the classification did not terminate
    HEADLINE_ONLY_LIBRARY_LEAD  nothing can be concluded from what we hold
    REJECTED_CLASSIFICATION     off-theme, on a record adequate to say so
    MATCH                       IP present AND a second ring present AND nexus
                                AND evidence valid at a permitted location
    ADJACENT_LEAD               near the theme but missing a MATCH predicate

A note on the name HEADLINE_ONLY_LIBRARY_LEAD: it is one of the five lane values
R2.1 fixes, and it is the library lane — the destination for everything recorded
without an assertion attached, whether that is a headline we could not read past,
a domestic comparator with no treaty nexus, or a single non-IP ring. Its name
comes from the case that motivated it, not from the whole of its meaning, so
every verdict also carries `lane_reason`, which is precise.

STATUS. Behind `config.STATE_MODEL_V2`, default "shadow": the derivation runs and
is written to telemetry, and it decides nothing. "on" — publication-lane
authority — requires the validation decision and does not yet have publication
wiring; `config` refuses it while `STATE_MODEL_V2_PUBLICATION_READY` is False.

DETERMINISM. No wall clock, no network, no fuzzy matching. Every closed list in
this file is a literal, every regex is anchored to a documented citation format,
and the strength ladder is read from the same two constants the keyword scorer
uses, so the two paths cannot drift apart.
"""

from __future__ import annotations

import functools
import hashlib
import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Optional

from .classify import (PRESENT_FLOOR, STRONG_SUBTOTAL, TERMINAL_OUTCOMES,
                       VALID_RINGS, ClassifyOutcome, _normalize_for_match)

logger = logging.getLogger("isds.rings")

# The three rings, in their canonical order. Imported, not restated: a second
# copy of this tuple is a second thing to keep in step with `fingerprint.yaml`.
RINGS = tuple(VALID_RINGS)
RING_IP, RING_JRM, RING_JA = RINGS

# The outcome VALUES after which a classification is finished (see
# ClassifyOutcome). Compared as strings because the enum members hash by
# identity — the same trap `src/main.py:TERMINAL_VALUES` documents.
TERMINAL_OUTCOME_VALUES = frozenset(o.value for o in TERMINAL_OUTCOMES)
ALL_OUTCOME_VALUES = frozenset(o.value for o in ClassifyOutcome)


# --------------------------------------------------------------------------- #
# The classification state space (R2.1's seven, resolved against the four)
# --------------------------------------------------------------------------- #
class ClassifyState(str, Enum):
    """The SEVEN classification states R2.1 enumerates over.

    WHY THIS EXISTS, AND WHAT IT IS NOT. R2.1 names seven classification
    outcomes and enumerates 64 x 4 x 4 x 3 x 7 = 21,504 tuples. The
    implementation imported four (`ClassifyOutcome`) and enumerated 12,288.
    That was an undisclosed deviation, and the fix is NOT to change the
    advertised number: it is to say which space is the real one and prove the
    other is recoverable from it.

    The resolution, in full in `analytics/state-space-resolution-2026-08-09.md`:
    the four `ClassifyOutcome` values are the OPERATIONAL record — what
    `classify_item` did, written at the moment it did it. These seven are the
    LOGICAL states R2.1's rules are stated in terms of, and every one of them is
    a total function of the operational record plus metadata the pipeline
    already keeps (`classify_attempts`, `retried_strict`, the deferred-queue
    abandonment flag, and — for the last one — this module's own evidence rules).
    `classification_state` below is that function. It is a projection, not a
    bijection, and the two facts it projects away (`retried_strict` under a
    demotion, and the raw outcome under an abandonment) are BOTH still written
    to telemetry beside it, so nothing is lost from the record.

      OK_FIRST_PASS     the model answered and parsed on attempt 1.
      OK_AFTER_RETRY    it answered and parsed only after the strict retry.
      MALFORMED_OUTPUT  it answered and we could not parse it, retry included.
                        Distinct from a provider failure: the provider WORKED.
      PROVIDER_FAILURE  the call itself failed on an item we tried to classify.
      KEYWORD_ONLY      no model was expected and none was called.
      RETRY_ABANDONED   we stopped trying. Terminal for the run, and yet nothing
                        was ever read — the one state that is finished AND
                        unknowable, which is why it is not in CLASSIFIED_STATES.
      GUARD_DEMOTED     the classification parsed, and this module's evidence
                        rules cut at least one ring below what was claimed for
                        it. R2.1 lists it among the seven because a demotion is
                        a different event from a clean pass and has to be
                        countable; it is the only one of the seven that no
                        classifier could report, because the classifier is the
                        thing being checked.
    """

    OK_FIRST_PASS = "ok_first_pass"
    OK_AFTER_RETRY = "ok_after_retry"
    MALFORMED_OUTPUT = "malformed_output"
    PROVIDER_FAILURE = "provider_failure"
    KEYWORD_ONLY = "keyword_only"
    RETRY_ABANDONED = "retry_abandoned"
    GUARD_DEMOTED = "guard_demoted"


ALL_STATE_VALUES = frozenset(s.value for s in ClassifyState)

# What produced a verdict's ring findings, in a closed vocabulary.
#
# `v2_basis` answers "did a V2 model response contribute?" and `claims_source`
# answers "whose ring claims are recorded here?". They are separate because the
# combination that used to be invisible — a model asserting rings while the
# operative strengths came from the lexicon — is exactly the one the audit
# objected to, and a single field cannot say both halves of it.
#
# V2_BASIS_LEXICAL_ONLY lives here rather than in `src/classify_v2.py` so that
# the module which WRITES the field owns its default; classify_v2 imports it
# back, which keeps one definition and lets rings stay free of the import cycle
# that would otherwise run rings -> classify_v2 -> rings.
V2_BASIS_LEXICAL_ONLY = "lexical_only"

CLAIMS_NONE = "none"                    # no model spoke about any ring
CLAIMS_LEGACY_V1 = "legacy_v1_ring_list"  # a bare ring list, no spans, ever
CLAIMS_V2_PROMPT = "v2_prompt"          # per-ring strengths with spans to check
ALL_CLAIMS_SOURCES = frozenset({CLAIMS_NONE, CLAIMS_LEGACY_V1, CLAIMS_V2_PROMPT})

# The states in which a classification actually completed and its findings are
# entitled to a reading.
#
# RETRY_ABANDONED is deliberately NOT here, and it is the subtle one. An
# abandoned item IS finished — `src/main.py` marks it seen and the deferred
# queue lets it go — but it is finished WITHOUT ever having been read. Letting
# it into this set would let an abandoned item with an accessible body and three
# absent lexical rings reach REJECTED_CLASSIFICATION, i.e. reach the conclusion
# "we read this and it is off-theme" about an item whose classification never
# once succeeded. It lands at Lane.RETRY instead, under its own reason code, so
# the lane says "nothing is knowable" and the reason says which kind of nothing.
CLASSIFIED_STATES = frozenset({
    ClassifyState.OK_FIRST_PASS,
    ClassifyState.OK_AFTER_RETRY,
    ClassifyState.KEYWORD_ONLY,
    ClassifyState.GUARD_DEMOTED,
})

CLASSIFIED_STATE_VALUES = frozenset(s.value for s in CLASSIFIED_STATES)


def classification_state(*, outcome: str, attempts: int = 0,
                         retried_strict: bool = False, abandoned: bool = False,
                         guard_demoted: bool = False) -> ClassifyState:
    """The R2.1 logical state, from the operational record. Total; ordered.

    Every input reaches exactly one branch. The order IS the resolution and each
    step is a decision that is argued rather than assumed:

      1. ABANDONMENT OUTRANKS ITS CAUSE. Why we gave up (a parse failure, an
         outage) is still in ``outcome`` and still in telemetry; that we gave up
         is the fact that changes what may be concluded, so it is the state.

      2. MALFORMED IS NOT A PROVIDER FAILURE. R2.1 relies on the distinction and
         so does any reading of a bad week: a provider outage is somebody else's
         infrastructure, an unparseable answer is our prompt. They are separate
         `ClassifyOutcome` values already, so this step is a rename, not a
         judgment.

      3. A FAILED CALL ON A TAIL ITEM IS STILL A PROVIDER FAILURE. This is the
         one genuinely contestable step. `classify_item(intended_model=False)`
         records a provider error as KEYWORD_ONLY_BY_DESIGN, because for the
         tail a keyword score is where the item was going anyway. That is right
         about the CONSEQUENCE and wrong about the EVENT: a call was made and it
         failed, and an outage that is only counted on the enriched top set is an
         outage under-counted by however large the tail is. `attempts > 0` on the
         keyword path happens on no other route — the no-provider path never
         calls anything and records 0 — so the two are separable, and they are
         separated here. Consequence is not lost: it is `intended_model`, and it
         is what `TERMINAL_OUTCOMES` already encodes.

      4. A DEMOTION OUTRANKS A CLEAN PASS. GUARD_DEMOTED and OK_AFTER_RETRY can
         both be true of one item. The demotion wins the single state slot
         because it is the rarer and more consequential fact, and `retried_strict`
         is written to telemetry beside the state, so the retry is still
         countable. This is the projection referred to in the class docstring.
    """
    if abandoned:
        return ClassifyState.RETRY_ABANDONED
    if outcome == ClassifyOutcome.PARSE_FAILED.value:
        return ClassifyState.MALFORMED_OUTPUT
    if outcome == ClassifyOutcome.PROVIDER_ERROR.value:
        return ClassifyState.PROVIDER_FAILURE
    if outcome == ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN.value:
        return (ClassifyState.PROVIDER_FAILURE if int(attempts) > 0
                else ClassifyState.KEYWORD_ONLY)
    if outcome == ClassifyOutcome.OK.value:
        if guard_demoted:
            return ClassifyState.GUARD_DEMOTED
        return (ClassifyState.OK_AFTER_RETRY if retried_strict
                else ClassifyState.OK_FIRST_PASS)
    # Anything else is a state the classifier does not produce — `main.py`'s
    # "pipeline_error" is the live example. It never finished, and the honest
    # reading of an unrecognised ending is that nothing is knowable, which is
    # what MALFORMED_OUTPUT buys us: non-terminal, retried, recorded.
    logger.warning("rings: unrecognised classification outcome %r; treating it "
                   "as malformed output (non-terminal)", outcome)
    return ClassifyState.MALFORMED_OUTPUT

# A claimed evidence span shorter than this verifies against almost anything, so
# it is not evidence. Same threshold, and the same reasoning, as
# `classify._quote_in_source`.
MIN_EVIDENCE_SPAN_CHARS = 20

# Fetch-log outcomes (`src/sources/base._record_outcome`) that mean we tried to
# read a body and did not get one. "not_attempted" is deliberately NOT here: not
# trying is not the same as being refused.
FETCH_FAILURE_OUTCOMES = frozenset({
    "no_client", "robots_disallowed", "no_contact", "refused"})


class InvariantViolation(ValueError):
    """A construction the contract forbids.

    A ValueError subclass so existing `except ValueError` handlers still catch
    it, and its own type so a test can assert that the contract — rather than
    some incidental type error on the way to it — is what rejected the input.
    """


# --------------------------------------------------------------------------- #
# Vocabulary
# --------------------------------------------------------------------------- #
@functools.total_ordering
class Strength(Enum):
    """How strongly one ring is present. Ordered; ABSENT is a real finding.

    A plain Enum rather than a str-Enum on purpose: `str` supplies a full set of
    comparison operators, and inheriting them would order these alphabetically —
    "present" < "strong" < "weak" — which is exactly backwards in the middle and
    would silently corrupt every `>=` in the lane rule.
    """

    ABSENT = 0
    WEAK = 1
    PRESENT = 2
    STRONG = 3

    @property
    def label(self) -> str:
        return self.name.lower()

    def __lt__(self, other):
        if not isinstance(other, Strength):
            return NotImplemented
        return self.value < other.value


class Basis(str, Enum):
    """What a finding rests on."""

    LEXICAL = "lexical"                        # fingerprint phrases in the text
    SEMANTIC = "semantic"                      # a model span that verified
    BOTH = "both"                              # both, and the span verified
    SEMANTIC_UNVERIFIED = "semantic_unverified"  # a model claim we could not check


class Nexus(str, Enum):
    """Whether this is an investor-State matter at all."""

    ESTABLISHED = "established"        # an ISDS source, or a case identifier
    ASSERTED = "asserted"              # proceeding language, unconfirmed
    INDETERMINATE = "indeterminate"    # we cannot tell from what we hold
    ABSENT = "absent"                  # we read the body and it is not there


class EvidenceLocation(str, Enum):
    """Where the best evidence we hold actually lives."""

    ACCESSIBLE_BODY = "accessible_body"
    SUMMARY = "summary"
    TITLE = "title"
    UNAVAILABLE_BODY = "unavailable_body"   # we tried to read a body and failed


class EvidenceValidity(str, Enum):
    """Whether the evidence base can be checked at all."""

    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    UNVERIFIABLE_IN_PRINCIPLE = "unverifiable_in_principle"   # NO_BODY_FETCH


class Lane(str, Enum):
    """The five R2.1 dispositions. Publication authority attaches to MATCH only."""

    MATCH = "MATCH"
    ADJACENT_LEAD = "ADJACENT_LEAD"
    HEADLINE_ONLY_LIBRARY_LEAD = "HEADLINE_ONLY_LIBRARY_LEAD"
    REJECTED_CLASSIFICATION = "REJECTED_CLASSIFICATION"
    RETRY = "RETRY"


class DerivationPath(str, Enum):
    """Which path produced the findings."""

    DETERMINISTIC = "deterministic"
    MODEL = "model"
    MERGED = "merged"


# Locations at which evidence may support a MATCH. A title is a headline and a
# failed body is nothing; neither is a document.
MATCH_PERMITTED_LOCATIONS = frozenset({
    EvidenceLocation.ACCESSIBLE_BODY, EvidenceLocation.SUMMARY})

# Locations from which no conclusion — positive or negative — may be drawn.
INCONCLUSIVE_LOCATIONS = frozenset({
    EvidenceLocation.TITLE, EvidenceLocation.UNAVAILABLE_BODY})


# --------------------------------------------------------------------------- #
# The strength ladder — encoded ONCE, shared by both paths
# --------------------------------------------------------------------------- #
def strength_for_subtotal(subtotal: int) -> Strength:
    """The ladder: 0 absent, 1..11 weak, 12..17 present, 18+ strong.

    The two boundaries are `classify.PRESENT_FLOOR` and
    `classify.STRONG_SUBTOTAL`, imported rather than repeated. The keyword path
    and the model path must be able to disagree about an item; they must not be
    able to disagree about what "present" means, which is what happens the moment
    this ladder exists in two places.
    """
    if subtotal <= 0:
        return Strength.ABSENT
    if subtotal < PRESENT_FLOOR:
        return Strength.WEAK
    if subtotal < STRONG_SUBTOTAL:
        return Strength.PRESENT
    return Strength.STRONG


# --------------------------------------------------------------------------- #
# ISDS nexus — is this an investor-State matter at all?
# --------------------------------------------------------------------------- #
# Sources that only ever carry investor-State material. Membership is the nexus.
NEXUS_ESTABLISHED_SOURCES = frozenset({"icsid", "italaw", "pca_press", "unctad_isds"})

# Closed list of case-identifier formats. Deliberately narrow: an identifier is
# either one of these shapes or it is not an identifier. Applied to text already
# run through `_normalize_for_match`, hence lower case throughout.
NEXUS_IDENTIFIER_PATTERNS = (
    r"icsid case no\.?\s*arb/\d+/\d+",
    r"icsid case no\.?\s*arb\(af\)/\d+/\d+",
    r"arb\(af\)/\d+/\d+",
    r"pca case no\.?\s*20\d\d-\d+",
    r"unct/\d+/\d+",
)
_NEXUS_IDENTIFIERS = tuple(re.compile(p) for p in NEXUS_IDENTIFIER_PATTERNS)

# Closed list of proceeding lexemes. These ASSERT a nexus rather than
# establishing one: an article can say "investor-State" about someone else's
# case. `_normalize_for_match` folds en/em dashes to "-", so "investor–State"
# and "investor-State" both reach the entry below.
NEXUS_PROCEEDING_LEXEMES = (
    "notice of arbitration",
    "investor-state",
    "bit claim",
    "treaty arbitration",
    "annulment committee",
    "icsid arbitration",
)


def derive_nexus(*, source: str, text: str,
                 location: EvidenceLocation) -> Nexus:
    """Whether this is an ISDS matter, and how confidently we can say so.

    ABSENT is reachable only from ACCESSIBLE_BODY. Everywhere else the answer to
    "is there a treaty nexus here?" when we have found none is INDETERMINATE,
    because we have read a headline. Absence is a finding and a finding requires
    reading; this is rule 2 of the module docstring, applied at its source.
    """
    hay = _normalize_for_match(text)
    if source in NEXUS_ESTABLISHED_SOURCES:
        return Nexus.ESTABLISHED
    if any(rx.search(hay) for rx in _NEXUS_IDENTIFIERS):
        return Nexus.ESTABLISHED
    if any(lex in hay for lex in NEXUS_PROCEEDING_LEXEMES):
        return Nexus.ASSERTED
    if location is EvidenceLocation.ACCESSIBLE_BODY:
        return Nexus.ABSENT
    return Nexus.INDETERMINATE


# --------------------------------------------------------------------------- #
# Evidence: where it is, and whether it is real
# --------------------------------------------------------------------------- #
def verify_span(span: str, *, title: str = "", summary: str = "",
                raw_text: str = "", headline_only: bool = False
                ) -> tuple[bool, str]:
    """Locate a claimed evidence span in the item's own text.

    Returns ``(verified, source_field)`` where ``source_field`` is the FIRST of
    ``raw_text``, ``summary``, ``title`` that contains it, or ``""`` when it
    verifies nowhere. Naming the field is the point: `_quote_in_source` in
    `src/classify.py` concatenates all three and returns a bare bool, so it
    cannot tell a body quote from a headline — and for `iareporter_headlines`,
    where the fetcher sets ``raw_text = title``, the two are literally the same
    string. For those sources this function looks at the title and nothing else,
    so the span is named as what it is and the title cap in `RingFinding` bites.

    Matching reuses `classify._normalize_for_match` (case, whitespace, and smart
    quote/dash folding), so a genuine span is not rejected over typography and no
    fuzzy comparison is introduced.
    """
    needle = _normalize_for_match(span)
    if len(needle) < MIN_EVIDENCE_SPAN_CHARS:
        return False, ""
    if headline_only:
        fields: tuple[tuple[str, str], ...] = (("title", title),)
    else:
        fields = (("raw_text", raw_text), ("summary", summary), ("title", title))
    for name, value in fields:
        if needle in _normalize_for_match(value):
            return True, name
    return False, ""


def derive_location(*, headline_only: bool, body_fetched: bool = False,
                    fetch_outcome: str = "not_attempted", title: str = "",
                    summary: str = "", raw_text: str = "") -> EvidenceLocation:
    """The best evidence location we actually reached for this item.

    Keyed on the TEXT WE HOLD, not on whether we fetched it, because those come
    apart in both directions and the sources make a mess of the field names.
    ``raw_text`` is a body for `iisd_itn` (the feed carries the article) and for
    anything `enrich` fetched; it is a copy of the TITLE for `icsid`, `italaw`,
    `unctad_isds`, `pca_press` and `iareporter_headlines`; and it is a copy of the
    SUMMARY for `bing_news`, `gmail_scholar` and `google_alerts`. Trusting the
    field name would classify five sources' headlines as bodies and let a
    negative conclusion be drawn from one — which is exactly the defect this
    module exists to make impossible, arriving through the back door.

    So a body is text we fetched ourselves, or text that is neither the title nor
    a restatement of the summary. Everything else falls to the summary or the
    title, whichever we actually have. A failed fetch is reported only when there
    is no body to fall back on: a refusal on top of a feed that already carried
    the article is a failure to get MORE, not an absence of evidence.
    """
    if headline_only:
        # NO_BODY_FETCH by policy. Not a failure and never re-tried.
        return EvidenceLocation.TITLE
    body = (raw_text or "").strip()
    normalized = _normalize_for_match(body)
    echoes_a_shorter_field = normalized in (_normalize_for_match(title),
                                            _normalize_for_match(summary))
    if body and (body_fetched or not echoes_a_shorter_field):
        return EvidenceLocation.ACCESSIBLE_BODY
    if fetch_outcome in FETCH_FAILURE_OUTCOMES:
        return EvidenceLocation.UNAVAILABLE_BODY
    if (summary or "").strip():
        return EvidenceLocation.SUMMARY
    return EvidenceLocation.TITLE


def derive_validity(*, headline_only: bool,
                    location: EvidenceLocation) -> EvidenceValidity:
    """Whether the evidence base admits of checking.

    A property of what we hold, not of what any model claimed about it. An
    unverified model claim is recorded on the ring it was made about, as
    ``Basis.SEMANTIC_UNVERIFIED``, and contributes no strength; it must not also
    poison the validity of an item whose rings rest on code-verified lexical
    hits. UNVERIFIED at ACCESSIBLE_BODY stays constructible and is handled by the
    lane rule (it can never MATCH) — it is the state the V2 prompt will produce
    when it supplies spans that fail to verify against a body we did read.
    """
    if headline_only:
        return EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE
    if location is EvidenceLocation.UNAVAILABLE_BODY:
        return EvidenceValidity.UNVERIFIED
    return EvidenceValidity.VERIFIED


# --------------------------------------------------------------------------- #
# A finding about one ring
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RingFinding:
    """What we found about ONE named ring, and how we know.

    ``evidence_verified`` and ``evidence_source_field`` are set by CODE — by
    `verify_span`, via `merged_finding` — never by a model and never by a caller
    asserting them. A model may claim a span; only this module may say the span
    is in the document.
    """

    ring: str
    basis: Basis
    lexical_subtotal: int
    lexical_hits: tuple[str, ...]
    strength: Strength
    evidence_span: str
    evidence_verified: bool
    evidence_source_field: str      # raw_text | summary | title | ""
    # What a model asserted about this ring, and what the evidence rules
    # actually credited it with. None when no model spoke about the ring at all,
    # which is a different statement from a model saying "absent" — the same
    # distinction rule 1 makes at the level of the verdict, made here about the
    # model's own participation. `semantic_credited` is ABSENT whenever no model
    # spoke; the gap between the two is a demotion (see `guard_demoted`).
    model_claimed_strength: Optional[Strength] = None
    semantic_credited: Strength = Strength.ABSENT

    def __post_init__(self) -> None:
        if self.ring not in RINGS:
            raise InvariantViolation(
                f"{self.ring!r} is not one of the three rings {RINGS}; the rings "
                "are named and are never interchangeable")
        if not isinstance(self.basis, Basis):
            raise InvariantViolation(f"basis must be a Basis, got {self.basis!r}")
        if not isinstance(self.strength, Strength):
            raise InvariantViolation(
                f"strength must be a Strength, got {self.strength!r}")
        if self.lexical_subtotal < 0:
            raise InvariantViolation(
                f"lexical_subtotal {self.lexical_subtotal} is negative")
        if self.evidence_source_field not in ("", "raw_text", "summary", "title"):
            raise InvariantViolation(
                f"evidence_source_field {self.evidence_source_field!r} is not a "
                "field of a candidate item")

        # Verification is a fact about a located span, so the three facts move
        # together or not at all.
        if self.evidence_verified and not self.evidence_span:
            raise InvariantViolation(
                "evidence_verified with no span: nothing was verified")
        if self.evidence_verified and not self.evidence_source_field:
            raise InvariantViolation(
                "evidence_verified without naming the field it was found in")
        if not self.evidence_verified and self.evidence_source_field:
            raise InvariantViolation(
                f"unverified evidence cannot name a source field "
                f"({self.evidence_source_field!r})")

        if self.basis is Basis.LEXICAL and (self.evidence_span
                                            or self.evidence_verified):
            raise InvariantViolation(
                "a lexical finding carries no semantic evidence span")
        if self.basis is Basis.SEMANTIC and not self.evidence_verified:
            raise InvariantViolation(
                "basis=semantic requires a verified span; an unverified claim is "
                "semantic_unverified")
        if self.basis is Basis.SEMANTIC_UNVERIFIED and self.evidence_verified:
            raise InvariantViolation(
                "basis=semantic_unverified contradicts evidence_verified")
        if self.basis is Basis.BOTH and not (self.lexical_subtotal > 0
                                             and self.evidence_verified):
            raise InvariantViolation(
                "basis=both requires lexical support AND a verified span")

        # The merge rule, as an invariant rather than a convention: lexical
        # evidence is a floor (it is code-verified by construction), and only
        # VERIFIED semantic evidence may lift a ring above that floor. This is
        # what stops an unevidenced model assertion from promoting a ring.
        floor = strength_for_subtotal(self.lexical_subtotal)
        if self.strength < floor:
            raise InvariantViolation(
                f"{self.ring}: strength {self.strength.label} is below its own "
                f"lexical evidence ({self.lexical_subtotal} -> {floor.label})")
        if self.strength > floor and not self.evidence_verified:
            raise InvariantViolation(
                f"{self.ring}: strength {self.strength.label} exceeds the lexical "
                f"floor {floor.label} on evidence that did not verify")

        # A headline cannot carry a ring. A span located in the title may lift a
        # ring to WEAK and no further, whatever the body text independently
        # supports.
        if self.evidence_source_field == "title":
            ceiling = max(floor, Strength.WEAK)
            if self.strength > ceiling:
                raise InvariantViolation(
                    f"{self.ring}: a span found only in the title cannot support "
                    f"{self.strength.label} (ceiling {ceiling.label})")

        # The semantic half of the merge, as an invariant of its own.
        if not isinstance(self.semantic_credited, Strength):
            raise InvariantViolation(
                f"semantic_credited must be a Strength, got "
                f"{self.semantic_credited!r}")
        if self.model_claimed_strength is not None and not isinstance(
                self.model_claimed_strength, Strength):
            raise InvariantViolation(
                f"model_claimed_strength must be a Strength or None, got "
                f"{self.model_claimed_strength!r}")
        if self.model_claimed_strength is None \
                and self.semantic_credited is not Strength.ABSENT:
            raise InvariantViolation(
                f"{self.ring}: credited {self.semantic_credited.label} of semantic "
                "strength with no model claim to credit it to")
        if self.semantic_credited is not Strength.ABSENT \
                and not self.evidence_verified:
            raise InvariantViolation(
                f"{self.ring}: semantic strength credited on evidence that did not "
                "verify — an unverified claim contributes nothing")
        if self.model_claimed_strength is not None \
                and self.semantic_credited > self.model_claimed_strength:
            raise InvariantViolation(
                f"{self.ring}: credited {self.semantic_credited.label} against a "
                f"claim of only {self.model_claimed_strength.label}")

    @property
    def guard_demoted(self) -> bool:
        """Whether the evidence rules cut this ring below what was claimed.

        The R2.1 `guard_demoted` state, at the level of the one ring it happened
        to. True in exactly two situations, both of them span verification doing
        its job: the model claimed a ring and its span did not verify at all, or
        the span verified only in the TITLE and the title cap bit. Note that this
        is about the SEMANTIC credit and not about the final strength — a ring
        whose model claim was thrown out but which stands at `present` on its own
        lexical evidence was still demoted, and the demotion is still the fact
        worth counting, because it says the model asserted something it could not
        point to.
        """
        return (self.model_claimed_strength is not None
                and self.semantic_credited < self.model_claimed_strength)

    def to_dict(self) -> dict:
        """Bounded, text-free fields — safe for telemetry.

        Deliberately omits ``evidence_span`` itself: the span is candidate text,
        and `src/telemetry.py` holds text in no form. What survives is the
        PROVENANCE of the span — its sha256, its length, the field it was found
        in, and whether it verified — which is everything needed to ask later
        whether a given model's spans were real, whether a demotion pattern is
        concentrated in one source, or whether the same span reappeared across
        runs, without the analytics directory ever accumulating a line of anyone
        else's prose.
        """
        span = self.evidence_span or ""
        return {
            "ring": self.ring,
            "basis": self.basis.value,
            "strength": self.strength.label,
            "lexical_subtotal": int(self.lexical_subtotal),
            "evidence_verified": bool(self.evidence_verified),
            "evidence_source_field": self.evidence_source_field,
            "evidence_span_len": len(span),
            "evidence_span_sha256": (
                hashlib.sha256(span.encode("utf-8")).hexdigest() if span else ""),
            "model_claimed_strength": (None if self.model_claimed_strength is None
                                       else self.model_claimed_strength.label),
            "semantic_credited": self.semantic_credited.label,
            "guard_demoted": bool(self.guard_demoted),
        }


def lexical_finding(ring: str, subtotal: int,
                    hits: Iterable[str] = ()) -> RingFinding:
    """The deterministic path's finding for one ring."""
    return RingFinding(
        ring=ring,
        basis=Basis.LEXICAL,
        lexical_subtotal=int(subtotal),
        lexical_hits=tuple(sorted(str(h) for h in hits)),
        strength=strength_for_subtotal(int(subtotal)),
        evidence_span="",
        evidence_verified=False,
        evidence_source_field="",
    )


def merged_finding(ring: str, *, lexical_subtotal: int = 0,
                   lexical_hits: Iterable[str] = (),
                   model_claimed: bool = False,
                   model_strength: Strength = Strength.ABSENT,
                   evidence_span: str = "",
                   title: str = "", summary: str = "", raw_text: str = "",
                   headline_only: bool = False) -> RingFinding:
    """One ring's finding with both paths merged.

    THE MERGE RULE (R2.1): per-ring max of the lexical strength and the VERIFIED
    semantic strength. An unverified semantic claim contributes nothing at all —
    it is recorded, as ``Basis.SEMANTIC_UNVERIFIED``, so that the claim and its
    failure to verify are both in the record, and then it is ignored. A model
    that asserts a ring it cannot point to has told us about itself, not about
    the document.

    Merging per RING is what keeps the three rings non-interchangeable. There is
    no total, no average, and no point at which two rings become a quantity.
    """
    verified, source_field = verify_span(
        evidence_span, title=title, summary=summary, raw_text=raw_text,
        headline_only=headline_only) if model_claimed else (False, "")

    lexical = strength_for_subtotal(int(lexical_subtotal))
    semantic = model_strength if verified else Strength.ABSENT
    if verified and source_field == "title":
        semantic = min(semantic, Strength.WEAK)
    strength = max(lexical, semantic)

    # A model rating a ring ABSENT with no span has asserted nothing that could
    # be verified, so it is not an "unverified claim" — it is agreement with
    # silence. Recording it as SEMANTIC_UNVERIFIED would inflate the count of
    # claims the guard threw out with claims nobody made.
    asserted = model_claimed and (model_strength > Strength.ABSENT
                                  or bool(evidence_span))
    if not asserted:
        basis = Basis.LEXICAL
        span = ""
    elif verified:
        basis = Basis.BOTH if lexical_subtotal > 0 else Basis.SEMANTIC
        span = evidence_span
    else:
        basis = Basis.SEMANTIC_UNVERIFIED
        span = evidence_span

    return RingFinding(
        ring=ring,
        basis=basis,
        lexical_subtotal=int(lexical_subtotal),
        lexical_hits=tuple(sorted(str(h) for h in lexical_hits)),
        strength=strength,
        evidence_span=span,
        evidence_verified=verified,
        evidence_source_field=source_field,
        model_claimed_strength=model_strength if model_claimed else None,
        semantic_credited=semantic,
    )


def absent_finding(ring: str) -> RingFinding:
    """A recorded absence — the value a ring takes when nothing supports it."""
    return lexical_finding(ring, 0)


# --------------------------------------------------------------------------- #
# The lane rule
# --------------------------------------------------------------------------- #
# Reason codes. A closed set, short, and stable: they are written to telemetry
# every run and queried later, so they are identifiers rather than sentences.
REASON_NOT_TERMINAL = "classification_not_terminal"
REASON_ABANDONED = "classification_abandoned"
REASON_INCONCLUSIVE_LOCATION = "no_readable_evidence_location"
REASON_OFF_THEME_ON_READ_BODY = "three_rings_absent_on_read_body"
REASON_NO_NEXUS = "no_isds_nexus"
REASON_MATCH = "ip_plus_second_ring_with_nexus"
REASON_IP_WITHOUT_SECOND_RING = "ip_present_without_second_ring"
REASON_IP_BLOCKED_PREDICATE = "ip_plus_second_ring_failed_a_match_predicate"
REASON_JRM_AND_JA_NO_IP = "jurisprudence_both_rings_no_ip"
REASON_SINGLE_NO_IP_RING = "single_non_ip_ring"
REASON_NO_RING_AT_STRENGTH = "no_ring_reaches_present"

ALL_REASON_CODES = frozenset({
    REASON_NOT_TERMINAL, REASON_ABANDONED, REASON_INCONCLUSIVE_LOCATION,
    REASON_OFF_THEME_ON_READ_BODY, REASON_NO_NEXUS, REASON_MATCH,
    REASON_IP_WITHOUT_SECOND_RING, REASON_IP_BLOCKED_PREDICATE,
    REASON_JRM_AND_JA_NO_IP, REASON_SINGLE_NO_IP_RING,
    REASON_NO_RING_AT_STRENGTH,
})


# --------------------------------------------------------------------------- #
# What a lane is CALLED in public, which is not the same as what it IS
# --------------------------------------------------------------------------- #
# HEADLINE_ONLY_LIBRARY_LEAD is one of the five lane values R2.1 fixes and its
# name comes from the case that motivated it, not from the whole of its meaning
# (see the module docstring). That was tolerable while the name stayed inside
# telemetry. It is not tolerable on any surface a reader sees, because the lane
# is also where a fully-read domestic comparator lands — an item whose body we
# DID retrieve — and calling that "headline-only" is a false statement about our
# own access, made by us, in public. A fixture simulation produced exactly that
# pair: lane HEADLINE_ONLY_LIBRARY_LEAD at location accessible_body.
#
# So the internal value is preserved byte for byte (compatibility, and it is the
# key every past telemetry line is written under) and the PUBLIC label is a
# function of where the evidence actually lives. `lane_reason` is untouched by
# any of this and stays the precise machine-readable answer.
PUBLIC_LABEL_LIBRARY_COMPARATOR = "Library comparator"
PUBLIC_LABEL_HEADLINE_ONLY_LEAD = "Headline-only lead"

_PUBLIC_LANE_LABELS = {
    Lane.MATCH: "Match",
    Lane.ADJACENT_LEAD: "Adjacent lead",
    Lane.REJECTED_CLASSIFICATION: "Off-theme on a body we read",
    Lane.RETRY: "Not yet classified",
}

_PUBLIC_LOCATION_LABELS = {
    EvidenceLocation.ACCESSIBLE_BODY: PUBLIC_LABEL_LIBRARY_COMPARATOR,
    EvidenceLocation.SUMMARY: PUBLIC_LABEL_LIBRARY_COMPARATOR,
    EvidenceLocation.TITLE: PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
    EvidenceLocation.UNAVAILABLE_BODY: PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
}

ALL_PUBLIC_LABELS = frozenset(
    set(_PUBLIC_LANE_LABELS.values()) | set(_PUBLIC_LOCATION_LABELS.values()))


def public_lane_label(lane: Lane, location: EvidenceLocation) -> str:
    """The name for a lane that may be shown to a reader.

    Total over Lane x EvidenceLocation: every pair has a label and no pair has
    two. Only the library lane consults the location, because it is the only
    lane whose fixed name asserts something about access.
    """
    if not isinstance(lane, Lane):
        raise InvariantViolation(f"lane must be a Lane, got {lane!r}")
    if not isinstance(location, EvidenceLocation):
        raise InvariantViolation(
            f"location must be an EvidenceLocation, got {location!r}")
    if lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD:
        return _PUBLIC_LOCATION_LABELS[location]
    return _PUBLIC_LANE_LABELS[lane]


def nexus_supports_match(nexus: Nexus, validity: EvidenceValidity) -> bool:
    """Whether the nexus is good enough to carry a MATCH.

    ESTABLISHED always; ASSERTED only on verified evidence. The R2.1 record left
    this as a choice and the choice is recorded here: a proceeding lexeme is text
    an article wrote, and treating "investor-State" appearing somewhere in a page
    as equivalent to an ICSID case number would make the nexus test satisfiable
    by any commentary that mentions the field. Requiring verification of the
    evidence base is the cheapest thing that distinguishes the two.
    INDETERMINATE and ABSENT never support a MATCH.
    """
    if nexus is Nexus.ESTABLISHED:
        return True
    return nexus is Nexus.ASSERTED and validity is EvidenceValidity.VERIFIED


def derive_lane(*, strengths: Mapping[str, Strength], nexus: Nexus,
                location: EvidenceLocation, validity: EvidenceValidity,
                classification_state: ClassifyState) -> tuple[Lane, str]:
    """The R2.1 partition, as one ordered procedure. Total and single-valued.

    Ordered if/elif with a terminal else: every input reaches exactly one branch,
    the first matching one, and there is no input for which two lanes are
    reachable. The order encodes a precedence and each step is a veto:

      1. Did a classification complete? If not — whether because we are still
         retrying or because we abandoned the item — nothing else is knowable.
      2. Can anything be concluded from what we hold? A headline or a failed
         fetch supports no conclusion in EITHER direction — this is the step
         that makes both "headline-only can never MATCH" and "a failed body can
         never support a negative conclusion" true at once, because it fires
         before both the MATCH test and the rejection test.
      3. Off-theme on a body we read: the one place a negative conclusion is
         earned. Requires ACCESSIBLE_BODY specifically.
      4. No treaty nexus: a domestic matter is a comparator, not a lead.
      5. MATCH — all predicates.
      6-8. The near misses, partitioned by which predicate failed.

    ``model_score_advisory`` is not a parameter. It cannot be: there is no step
    at which a number could change the answer, which is the property that makes
    Example 4's taught 55 harmless here.
    """
    r_ip = strengths[RING_IP]
    r_jrm = strengths[RING_JRM]
    r_ja = strengths[RING_JA]

    # 1. No classification completed — no findings are entitled to a reading.
    #    Two ways to get here and they are NOT the same fact, so they carry
    #    different reason codes: we are still trying (main.py defers it), or we
    #    stopped trying. An abandoned item is finished with as far as the run is
    #    concerned and is still unreadable, and the lane must say the second
    #    thing rather than the first — this is the step that stops an item we
    #    gave up on from reaching a conclusion about its own contents at step 3.
    if classification_state is ClassifyState.RETRY_ABANDONED:
        return Lane.RETRY, REASON_ABANDONED
    if classification_state not in CLASSIFIED_STATES:
        return Lane.RETRY, REASON_NOT_TERMINAL

    # 2. A headline, or a body we failed to read. No conclusion either way.
    if location in INCONCLUSIVE_LOCATIONS:
        return Lane.HEADLINE_ONLY_LIBRARY_LEAD, REASON_INCONCLUSIVE_LOCATION

    # 3. Three absent rings on a body we actually read: an earned rejection.
    if (r_ip is Strength.ABSENT and r_jrm is Strength.ABSENT
            and r_ja is Strength.ABSENT
            and location is EvidenceLocation.ACCESSIBLE_BODY):
        return Lane.REJECTED_CLASSIFICATION, REASON_OFF_THEME_ON_READ_BODY

    # 4. No investor-State nexus: domestic litigation, or an unreadable one.
    #    Kept whatever the rings say — a domestic trade-secret suit can light up
    #    the IP ring brightly and is still not an ISDS development.
    if nexus in (Nexus.ABSENT, Nexus.INDETERMINATE):
        return Lane.HEADLINE_ONLY_LIBRARY_LEAD, REASON_NO_NEXUS

    ip_present = r_ip >= Strength.PRESENT
    second_ring = r_jrm >= Strength.PRESENT or r_ja >= Strength.PRESENT

    # 5. MATCH. Every predicate, and no score anywhere in it.
    if (ip_present and second_ring
            and nexus_supports_match(nexus, validity)
            and validity is EvidenceValidity.VERIFIED
            and location in MATCH_PERMITTED_LOCATIONS):
        return Lane.MATCH, REASON_MATCH

    # 6. IP present. Adjacent either way — with a second ring it failed a
    #    non-ring predicate (validity), without one it is IP alone, and the R2.1
    #    partition puts both at ADJACENT_LEAD and neither at MATCH.
    if ip_present:
        return (Lane.ADJACENT_LEAD,
                REASON_IP_BLOCKED_PREDICATE if second_ring
                else REASON_IP_WITHOUT_SECOND_RING)

    # 7. Class B3: both non-IP rings present. Generic ISDS jurisprudence — worth
    #    a lead, never a MATCH, because the research question is about IP.
    if r_jrm >= Strength.PRESENT and r_ja >= Strength.PRESENT:
        return Lane.ADJACENT_LEAD, REASON_JRM_AND_JA_NO_IP

    # 8. Everything else to the library. One non-IP ring (Example 4 lands here
    #    exactly), or nothing reaching present at all.
    if r_jrm >= Strength.PRESENT or r_ja >= Strength.PRESENT:
        return Lane.HEADLINE_ONLY_LIBRARY_LEAD, REASON_SINGLE_NO_IP_RING
    return Lane.HEADLINE_ONLY_LIBRARY_LEAD, REASON_NO_RING_AT_STRENGTH


# --------------------------------------------------------------------------- #
# The verdict
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RingVerdict:
    """Three findings, the context they were made in, and the lane that follows.

    ``findings`` is ALWAYS length 3, one per ring, in `RINGS` order. A verdict
    that mentioned only the rings it found would make "absent" and "not looked
    for" the same shape of silence.

    ``model_score_advisory`` is the legacy relevance score, preserved and
    explicitly NON-authoritative. It is carried so the two derivations can be
    compared during validation, and it is read by nothing that decides anything.
    """

    findings: tuple[RingFinding, ...]
    isds_nexus: Nexus
    evidence_location: EvidenceLocation
    evidence_validity: EvidenceValidity
    classification_state: ClassifyState
    path: DerivationPath
    # The raw `ClassifyOutcome` value the state was resolved FROM, kept beside
    # it so the record is lossless in both directions: the state is a projection
    # (see `classification_state`) and this is the fact it projects away.
    classification_outcome: str = ""
    model_score_advisory: Optional[int] = None
    # How the V2 findings were arrived at. See `v2_basis` values in
    # `src/classify_v2.py`; recorded here because a verdict that does not say
    # what produced it can be read as saying a model produced it.
    v2_basis: str = V2_BASIS_LEXICAL_ONLY
    claims_source: str = CLAIMS_NONE
    lane: Lane = field(init=False)
    lane_reason: str = field(init=False)
    public_label: str = field(init=False)

    def __post_init__(self) -> None:
        findings = tuple(self.findings)
        object.__setattr__(self, "findings", findings)

        if len(findings) != len(RINGS):
            raise InvariantViolation(
                f"a verdict carries exactly {len(RINGS)} findings, one per ring; "
                f"got {len(findings)}. An unmentioned ring is not an absent one.")
        if tuple(f.ring for f in findings) != RINGS:
            raise InvariantViolation(
                f"findings must be one per ring in order {RINGS}; got "
                f"{tuple(f.ring for f in findings)}")
        for name, value, kind in (("isds_nexus", self.isds_nexus, Nexus),
                                  ("evidence_location", self.evidence_location,
                                   EvidenceLocation),
                                  ("evidence_validity", self.evidence_validity,
                                   EvidenceValidity),
                                  ("classification_state",
                                   self.classification_state, ClassifyState),
                                  ("path", self.path, DerivationPath)):
            if not isinstance(value, kind):
                raise InvariantViolation(
                    f"{name} must be a {kind.__name__}, got {value!r}")
        if self.classification_outcome and \
                self.classification_outcome not in ALL_OUTCOME_VALUES:
            raise InvariantViolation(
                f"classification_outcome {self.classification_outcome!r} is not a "
                f"ClassifyOutcome value")

        # A verdict may not claim a demotion its findings do not show, and may
        # not hide one they do. GUARD_DEMOTED is the only state this module can
        # contradict from the inside, so it is the only one worth checking here.
        demoted = any(f.guard_demoted for f in findings)
        if (self.classification_state is ClassifyState.GUARD_DEMOTED) and not demoted:
            raise InvariantViolation(
                "classification_state=guard_demoted but no ring was demoted; the "
                "state names an event and the event is in the findings or it did "
                "not happen")
        if self.claims_source not in ALL_CLAIMS_SOURCES:
            raise InvariantViolation(
                f"claims_source {self.claims_source!r} is not one of "
                f"{sorted(ALL_CLAIMS_SOURCES)}")
        # THE DEFECT, AS AN INVARIANT. A basis that names a model is a statement
        # that a model produced these findings. It may not be made about a
        # verdict whose claims came from the lexicon or from nowhere.
        if self.v2_basis.startswith("semantic:") \
                and self.claims_source != CLAIMS_V2_PROMPT:
            raise InvariantViolation(
                f"v2_basis {self.v2_basis!r} names a model but claims_source is "
                f"{self.claims_source!r}: a lexical derivation may not be reported "
                "under a model's identity")
        if self.claims_source == CLAIMS_V2_PROMPT \
                and not self.v2_basis.startswith("semantic:"):
            raise InvariantViolation(
                f"claims_source is v2_prompt but v2_basis is {self.v2_basis!r}: a "
                "V2 response produced these findings and the record must say which "
                "model gave it")

        # Rule 2, at the level of the verdict: a negative conclusion about the
        # nexus requires having read a body. This is the constructor the Gazprom
        # annotation would not have survived.
        if (self.isds_nexus is Nexus.ABSENT
                and self.evidence_location is not EvidenceLocation.ACCESSIBLE_BODY):
            raise InvariantViolation(
                f"nexus=absent at location {self.evidence_location.value}: absence "
                "is a finding and a finding requires reading an accessible body; "
                "the honest value here is indeterminate")
        if (self.evidence_validity is EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE
                and self.evidence_location is EvidenceLocation.ACCESSIBLE_BODY):
            raise InvariantViolation(
                "unverifiable_in_principle describes a source whose body we never "
                "fetch; an accessible body contradicts it")
        if (self.evidence_validity is EvidenceValidity.VERIFIED
                and self.evidence_location is EvidenceLocation.UNAVAILABLE_BODY):
            raise InvariantViolation(
                "a body we failed to retrieve cannot be a verified evidence base")
        if self.model_score_advisory is not None and not (
                0 <= int(self.model_score_advisory) <= 100):
            raise InvariantViolation(
                f"model_score_advisory {self.model_score_advisory} is outside [0, 100]")

        lane, reason = derive_lane(
            strengths={f.ring: f.strength for f in findings},
            nexus=self.isds_nexus,
            location=self.evidence_location,
            validity=self.evidence_validity,
            classification_state=self.classification_state,
        )
        object.__setattr__(self, "lane", lane)
        object.__setattr__(self, "lane_reason", reason)
        object.__setattr__(self, "public_label",
                           public_lane_label(lane, self.evidence_location))

    # -- accessors ---------------------------------------------------------- #
    def finding(self, ring: str) -> RingFinding:
        for f in self.findings:
            if f.ring == ring:
                return f
        raise KeyError(ring)

    def strength(self, ring: str) -> Strength:
        return self.finding(ring).strength

    @property
    def publishable(self) -> bool:
        """MATCH is the only lane with publication authority — and only once
        `config.STATE_MODEL_V2` is "on", which this session does not reach."""
        return self.lane is Lane.MATCH

    @property
    def guard_demoted(self) -> bool:
        """Whether the evidence rules cut ANY ring below what was claimed."""
        return any(f.guard_demoted for f in self.findings)

    def to_telemetry(self, mode: str = "shadow") -> dict:
        """The verdict as bounded, text-free telemetry.

        No spans, no titles, no excerpts: every value here is an enumerated
        constant, a small integer, or a ring name of ours.
        `scripts/check_telemetry_privacy.py` enforces that this stays true.
        """
        return {
            "mode": mode,
            "derived": True,
            "lane": self.lane.value,
            "lane_reason": self.lane_reason,
            "public_label": self.public_label,
            "nexus": self.isds_nexus.value,
            "evidence_location": self.evidence_location.value,
            "evidence_validity": self.evidence_validity.value,
            "path": self.path.value,
            "classification_state": self.classification_state.value,
            "classification_outcome": self.classification_outcome,
            "guard_demoted": self.guard_demoted,
            # WHAT PRODUCED THIS VERDICT. The named defect this field exists to
            # make impossible is a lexical derivation reported under a model's
            # identity: if no V2 model response contributed, this says
            # "lexical_only" and no model id appears anywhere in the record.
            "v2_basis": self.v2_basis,
            "claims_source": self.claims_source,
            "model_score_advisory": (None if self.model_score_advisory is None
                                     else int(self.model_score_advisory)),
            "rings": {f.ring: f.to_dict() for f in self.findings},
        }


# --------------------------------------------------------------------------- #
# Building a verdict from what the pipeline already has
# --------------------------------------------------------------------------- #
def _derivation_path(model_rings: Iterable[str],
                     per_ring_subtotal: Mapping[str, int]) -> DerivationPath:
    has_model = bool(set(model_rings) & set(RINGS))
    has_lexical = any(int(v) > 0 for v in per_ring_subtotal.values())
    if has_model and has_lexical:
        return DerivationPath.MERGED
    if has_model:
        return DerivationPath.MODEL
    return DerivationPath.DETERMINISTIC


def _legacy_model_claims(classified, classification_outcome: str
                         ) -> tuple[set, str]:
    """Ring claims from the V1 path, and only when a model genuinely made them.

    THE BUG THIS FIXES. The previous version read `classified.matched_rings`
    unconditionally. On the keyword path that attribute holds the rings the
    KEYWORD SCORER found — the same rings whose subtotals are already the
    lexical evidence — so every offline run recorded its own lexical hits a
    second time, as unverified claims by a model that was never called. The
    shadow record then showed `basis: semantic_unverified` on findings no model
    had ever seen. Reading a provider-error item is the same trap with worse
    consequences: `classify_item` fills `matched_rings` from `keyword_score`
    when the call fails, so an outage produced a page of "model claims" too.

    A model claimed a ring only if a model answered: the LLM path AND a clean
    outcome. Returns the claimed rings and the closed-vocabulary name of where
    the claims came from.
    """
    meta = getattr(classified, "metadata", None) or {}
    model_answered = (meta.get("classify_path") == "llm"
                      and classification_outcome == ClassifyOutcome.OK.value)
    if not model_answered:
        return set(), CLAIMS_NONE
    return (set(getattr(classified, "matched_rings", None) or []),
            CLAIMS_LEGACY_V1)


def shadow_verdict(item, *, lexical_result: Mapping, classified,
                   classification_outcome: str, attempts: int = 0,
                   retried_strict: bool = False, abandoned: bool = False,
                   headline_only: bool = False, body_fetched: bool = False,
                   fetch_outcome: str = "not_attempted",
                   v2_strengths: Optional[Mapping[str, Strength]] = None,
                   v2_spans: Optional[Mapping[str, str]] = None,
                   v2_basis: str = V2_BASIS_LEXICAL_ONLY) -> RingVerdict:
    """Build a RingVerdict from one run's per-item data. Two possible bases.

    SEMANTIC (``v2_strengths`` supplied, ``v2_basis`` naming a model). The V2
    prompt returned a strength and a verbatim span per ring;
    `merged_finding` hands each span to `verify_span`, which checks it in CODE
    against the field it claims to come from. A span that verifies lifts its
    ring to the claimed strength (capped at WEAK in a title); a span that does
    not verify contributes nothing and the ring is recorded as demoted. This is
    the path in which the model's reading is genuinely under test.

    LEXICAL (everything else, and the default). No V2 response contributed, so
    the lexical subtotals carry every finding and ``v2_basis`` says
    ``lexical_only``. Legacy V1 ring claims, where a model really did make them,
    are still recorded and still held to the evidence rule — and since
    `prompts/classifier.txt` supplies no spans at all, they are all demoted.
    That is not a bug in this function; it is the measurement the audit asked
    for, and the count of demotions is what "the parser requires no evidence for
    any ring" looks like once something checks.

    THE INVARIANT THAT MATTERS: ``v2_basis`` names a model on the first path and
    on no other. There is no route through this function on which a lexical
    derivation acquires a model's identity.

    ``lexical_hits`` is left empty here: `keyword_score` returns thematic tags
    pooled across rings rather than partitioned by ring, and inventing a
    partition would be exactly the kind of plausible reconstruction this project
    does not do. The flat hit list is already in telemetry under `lexical.hits`.
    """
    per_ring = {k: int(v) for k, v in
                (lexical_result.get("per_ring_subtotal") or {}).items()}
    title = getattr(item, "title", "") or ""
    summary = getattr(item, "summary", "") or ""
    raw_text = getattr(item, "raw_text", "") or ""

    semantic = v2_strengths is not None
    if semantic:
        strengths = {r: v2_strengths.get(r, Strength.ABSENT) for r in RINGS}
        spans = {r: (v2_spans or {}).get(r, "") for r in RINGS}
        claimed_rings = {r for r in RINGS
                         if strengths[r] > Strength.ABSENT or spans[r]}
        claims_source = CLAIMS_V2_PROMPT
    else:
        claimed_rings, claims_source = _legacy_model_claims(
            classified, classification_outcome)
        # A bare ring name in `matched_rings` is a claim that the ring is
        # PRESENT — that is what the V1 prompt's ring list means — and it is
        # read as such and then held to the evidence rule it cannot meet.
        strengths = {r: Strength.PRESENT for r in RINGS}
        spans = {r: "" for r in RINGS}

    location = derive_location(
        headline_only=headline_only, body_fetched=body_fetched,
        fetch_outcome=fetch_outcome, title=title, summary=summary,
        raw_text=raw_text)
    validity = derive_validity(headline_only=headline_only, location=location)
    nexus = derive_nexus(
        source=getattr(item, "source", "") or "",
        text=" ".join((title, summary, raw_text)),
        location=location)

    findings = tuple(
        merged_finding(
            ring,
            lexical_subtotal=per_ring.get(ring, 0),
            model_claimed=ring in claimed_rings,
            model_strength=strengths[ring],
            evidence_span=spans[ring],
            title=title, summary=summary, raw_text=raw_text,
            headline_only=headline_only,
        )
        for ring in RINGS
    )

    state = classification_state(
        outcome=classification_outcome, attempts=attempts,
        retried_strict=retried_strict, abandoned=abandoned,
        guard_demoted=any(f.guard_demoted for f in findings))

    score = getattr(classified, "relevance_score", None)
    return RingVerdict(
        findings=findings,
        isds_nexus=nexus,
        evidence_location=location,
        evidence_validity=validity,
        classification_state=state,
        classification_outcome=classification_outcome,
        path=_derivation_path(claimed_rings, per_ring),
        model_score_advisory=None if score is None else int(score),
        v2_basis=v2_basis,
        claims_source=claims_source,
    )
