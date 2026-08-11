"""The R2.1 ring contract (src/rings.py), tested over its whole state space.

Three kinds of test here, and the first is the one that matters most:

  1. EXHAUSTIVE ENUMERATION. Every combination of 3 rings x 4 strengths (64 ring
     configurations) x 4 nexus values x 4 evidence locations x 3 validity values
     x 4 classification outcomes is constructed, and each is asserted to either
     raise the contract's own exception or derive exactly one lane. Spot-checking
     a decision rule tells you the cases you thought of behave; enumerating it
     tells you there is no case at all in which the rule is silent, ambiguous, or
     lets a MATCH out the side. The safety properties are asserted over the whole
     enumeration rather than on examples, so they are closed statements about the
     rule and not observations about a sample of it.

  2. PARITY. The same findings must produce the same lane whether they arrived
     from the keyword path or from the model. If they do not, the "contract" is
     two contracts and the path is a hidden input to the decision.

  3. THE NAMED BOUNDARY CASES. Each one is a thing that actually happened, or
     that the audit proved could happen, in this repo's own record.
"""

import datetime
import itertools

import pytest

from src import rings
from src.classify import keyword_score
from src.rings import (Basis, ClassifyState, DerivationPath, EvidenceLocation,
                       EvidenceValidity, InvariantViolation, Lane, Nexus,
                       RingFinding, RingVerdict, Strength)
from src.sources.base import CandidateItem

OK = ClassifyState.OK_FIRST_PASS

UTC = datetime.timezone.utc

RING_IP = rings.RING_IP
RING_JRM = rings.RING_JRM
RING_JA = rings.RING_JA

# A lexical subtotal that lands squarely on each rung of the ladder. Chosen from
# the ladder's own boundaries (PRESENT_FLOOR 12, STRONG_SUBTOTAL 18) so that if
# either constant moves, these move with it rather than quietly misclassifying.
SUBTOTAL_FOR = {
    Strength.ABSENT: 0,
    Strength.WEAK: 1,
    Strength.PRESENT: rings.PRESENT_FLOOR,
    Strength.STRONG: rings.STRONG_SUBTOTAL,
}

ALL_STRENGTHS = tuple(Strength)
ALL_NEXUS = tuple(Nexus)
ALL_LOCATIONS = tuple(EvidenceLocation)
ALL_VALIDITIES = tuple(EvidenceValidity)
ALL_STATES = tuple(ClassifyState)


def _findings(ip, jrm, ja):
    """Three lexical findings at the requested strengths, in ring order."""
    return tuple(rings.lexical_finding(ring, SUBTOTAL_FOR[s])
                 for ring, s in ((RING_IP, ip), (RING_JRM, jrm), (RING_JA, ja)))


def _verdict(ip=Strength.ABSENT, jrm=Strength.ABSENT, ja=Strength.ABSENT, *,
             nexus=Nexus.ESTABLISHED, location=EvidenceLocation.ACCESSIBLE_BODY,
             validity=EvidenceValidity.VERIFIED, state=OK,
             path=DerivationPath.DETERMINISTIC, score=None):
    return RingVerdict(
        findings=_findings(ip, jrm, ja),
        isds_nexus=nexus, evidence_location=location, evidence_validity=validity,
        classification_state=state, path=path, model_score_advisory=score)


def _verdict_construction_is_forbidden(nexus, location, validity) -> bool:
    """The contract's three verdict-level invariants, stated independently.

    Written out here rather than imported so the test is a second statement of
    the rule and not a restatement of the implementation: if src/rings.py and
    this predicate ever disagree, the enumeration below fails.
    """
    if nexus is Nexus.ABSENT and location is not EvidenceLocation.ACCESSIBLE_BODY:
        return True   # absence is a finding; a finding requires reading
    if (validity is EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE
            and location is EvidenceLocation.ACCESSIBLE_BODY):
        return True   # a source we never fetch cannot have a fetched body
    if (validity is EvidenceValidity.VERIFIED
            and location is EvidenceLocation.UNAVAILABLE_BODY):
        return True   # a failed fetch is not a verified evidence base
    return False


# =============================================================================
# 1. The whole state space
# =============================================================================
def test_the_ladder_is_the_two_constants_and_nothing_else():
    assert rings.strength_for_subtotal(0) is Strength.ABSENT
    assert rings.strength_for_subtotal(rings.PRESENT_FLOOR - 1) is Strength.WEAK
    assert rings.strength_for_subtotal(rings.PRESENT_FLOOR) is Strength.PRESENT
    assert rings.strength_for_subtotal(rings.STRONG_SUBTOTAL - 1) is Strength.PRESENT
    assert rings.strength_for_subtotal(rings.STRONG_SUBTOTAL) is Strength.STRONG
    assert rings.strength_for_subtotal(10_000) is Strength.STRONG
    # Ordered as the doctrine is ordered, not as the words sort. This is the trap
    # a str-valued enum would have walked into: "present" < "strong" < "weak".
    assert Strength.ABSENT < Strength.WEAK < Strength.PRESENT < Strength.STRONG
    assert max(Strength.WEAK, Strength.STRONG) is Strength.STRONG


def test_there_are_sixty_four_ring_configurations_and_we_enumerate_all_of_them():
    configs = list(itertools.product(ALL_STRENGTHS, repeat=3))
    assert len(configs) == 64
    assert len({_findings(*c) for c in configs}) == 64


def test_the_classification_axis_is_the_seven_r21_states_not_the_four_outcomes():
    """The deviation this file used to encode, stated as an assertion.

    R2.1 enumerates over SEVEN classification states. The implementation
    imported the four `ClassifyOutcome` values and enumerated 12,288 tuples
    instead of 21,504, and nothing said so. The resolution
    (`analytics/state-space-resolution-2026-08-09.md`) is that the seven are the
    logical space and the four are the operational record they are derived from
    — so the enumeration axis is the seven, and the four have to remain
    RECOVERABLE rather than merely renamed.
    """
    assert len(ALL_STATES) == 7
    assert {s.value for s in ALL_STATES} == {
        "ok_first_pass", "ok_after_retry", "malformed_output", "provider_failure",
        "keyword_only", "retry_abandoned", "guard_demoted"}
    # Four operational outcomes; the ratio is exactly why the tuple count moved.
    assert len(rings.ALL_OUTCOME_VALUES) == 4
    assert 64 * 4 * 4 * 3 * 7 == 21_504
    assert 64 * 4 * 4 * 3 * 4 == 12_288


def test_every_state_either_raises_the_contract_or_derives_exactly_one_lane():
    """The enumeration, over the RESOLVED space. 21,504 tuples; all accounted for."""
    constructed = 0
    refused = 0
    lanes_seen = set()

    for ip, jrm, ja in itertools.product(ALL_STRENGTHS, repeat=3):
        findings = _findings(ip, jrm, ja)
        for nexus, location, validity, state in itertools.product(
                ALL_NEXUS, ALL_LOCATIONS, ALL_VALIDITIES, ALL_STATES):
            forbidden = _verdict_construction_is_forbidden(nexus, location, validity)
            # GUARD_DEMOTED asserts an event; these findings are purely lexical
            # so no ring was demoted, and the contract must refuse the claim.
            forbidden = forbidden or state is ClassifyState.GUARD_DEMOTED
            if forbidden:
                with pytest.raises(InvariantViolation):
                    RingVerdict(findings=findings, isds_nexus=nexus,
                                evidence_location=location,
                                evidence_validity=validity,
                                classification_state=state,
                                path=DerivationPath.DETERMINISTIC)
                refused += 1
                continue

            v = RingVerdict(findings=findings, isds_nexus=nexus,
                            evidence_location=location, evidence_validity=validity,
                            classification_state=state,
                            path=DerivationPath.DETERMINISTIC)
            constructed += 1

            # Single-valued: one Lane, one reason, from a closed set.
            assert isinstance(v.lane, Lane)
            assert v.lane_reason in rings.ALL_REASON_CODES
            assert v.public_label in rings.ALL_PUBLIC_LABELS
            # ...and stable: the same state derives the same lane every time.
            again = rings.derive_lane(
                strengths={f.ring: f.strength for f in findings}, nexus=nexus,
                location=location, validity=validity,
                classification_state=state)
            assert again == (v.lane, v.lane_reason)
            lanes_seen.add(v.lane)

            # --- safety properties, asserted over the WHOLE space ------------
            if v.lane is Lane.MATCH:
                assert ip >= Strength.PRESENT, \
                    "a MATCH without the IP ring — the research question is IP"
                assert jrm >= Strength.PRESENT or ja >= Strength.PRESENT
                assert nexus in (Nexus.ESTABLISHED, Nexus.ASSERTED)
                assert validity is EvidenceValidity.VERIFIED
                assert location in rings.MATCH_PERMITTED_LOCATIONS
                assert state in rings.CLASSIFIED_STATES
            if location in rings.INCONCLUSIVE_LOCATIONS \
                    and state in rings.CLASSIFIED_STATES:
                # A headline or a failed body supports NO conclusion, in either
                # direction: not a match, and not a rejection either.
                assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
            if v.lane is Lane.REJECTED_CLASSIFICATION:
                assert location is EvidenceLocation.ACCESSIBLE_BODY, \
                    "a negative conclusion about a body we did not read"
                assert (ip, jrm, ja) == (Strength.ABSENT,) * 3
                assert state in rings.CLASSIFIED_STATES, \
                    "an item we never classified cannot be found off-theme"
            assert (v.lane is Lane.RETRY) == (state not in rings.CLASSIFIED_STATES)

    assert constructed + refused == 64 * 4 * 4 * 3 * 7 == 21_504
    assert refused > 0, "no state was refused — the invariants are not binding"
    assert lanes_seen == set(Lane), "a lane is unreachable from the state space"


# --- the resolution: each of the seven is derivable, and each distinction bites
def test_each_of_the_seven_states_is_reachable_from_the_operational_record():
    """The mapping, exercised value by value. Nothing here is a rename."""
    cs = rings.classification_state
    assert cs(outcome="ok", attempts=1) is ClassifyState.OK_FIRST_PASS
    assert cs(outcome="ok", attempts=2, retried_strict=True) \
        is ClassifyState.OK_AFTER_RETRY
    assert cs(outcome="parse_failed", attempts=2, retried_strict=True) \
        is ClassifyState.MALFORMED_OUTPUT
    assert cs(outcome="provider_error", attempts=1) is ClassifyState.PROVIDER_FAILURE
    assert cs(outcome="keyword_only_by_design", attempts=0) \
        is ClassifyState.KEYWORD_ONLY
    assert cs(outcome="parse_failed", attempts=2, abandoned=True) \
        is ClassifyState.RETRY_ABANDONED
    assert cs(outcome="ok", attempts=1, guard_demoted=True) \
        is ClassifyState.GUARD_DEMOTED
    # Total: every outcome/metadata combination lands somewhere.
    seen = {cs(outcome=o, attempts=a, retried_strict=r, abandoned=b,
               guard_demoted=g)
            for o in set(rings.ALL_OUTCOME_VALUES) | {"pipeline_error"}
            for a in (0, 1, 2) for r in (False, True)
            for b in (False, True) for g in (False, True)}
    assert seen == set(ClassifyState)


def test_first_pass_and_after_retry_are_distinguishable():
    cs = rings.classification_state
    assert cs(outcome="ok", attempts=1, retried_strict=False) \
        is not cs(outcome="ok", attempts=2, retried_strict=True)


def test_malformed_output_is_never_confused_with_a_provider_failure():
    """The provider WORKED in one of these and did not in the other."""
    cs = rings.classification_state
    assert cs(outcome="parse_failed") is ClassifyState.MALFORMED_OUTPUT
    assert cs(outcome="provider_error") is ClassifyState.PROVIDER_FAILURE
    assert ClassifyState.MALFORMED_OUTPUT is not ClassifyState.PROVIDER_FAILURE


def test_a_failed_call_on_a_tail_item_still_counts_as_a_provider_failure():
    """The contestable step of the mapping, pinned so it cannot drift silently.

    `classify_item(intended_model=False)` records a provider error as
    KEYWORD_ONLY_BY_DESIGN because for the tail a keyword score is where the item
    was going anyway. `attempts > 0` is what separates "a call failed" from "no
    call was made", and an outage counted only on the enriched top set is an
    outage under-counted by the size of the tail.
    """
    cs = rings.classification_state
    assert cs(outcome="keyword_only_by_design", attempts=0) \
        is ClassifyState.KEYWORD_ONLY
    assert cs(outcome="keyword_only_by_design", attempts=1) \
        is ClassifyState.PROVIDER_FAILURE


def test_abandoned_is_not_retrying_and_can_conclude_nothing():
    """An item we gave up on is finished, and still unreadable.

    The trap: an abandoned item can perfectly well have an accessible body (a
    parse failure on text we fetched successfully). If abandonment counted as a
    completed classification, three absent lexical rings on that body would
    reach REJECTED_CLASSIFICATION — "we read this and it is off-theme" — about
    an item no classifier ever managed to read.
    """
    assert ClassifyState.RETRY_ABANDONED not in rings.CLASSIFIED_STATES
    abandoned = _verdict(state=ClassifyState.RETRY_ABANDONED)
    still_trying = _verdict(state=ClassifyState.MALFORMED_OUTPUT)
    assert abandoned.lane is Lane.RETRY
    assert still_trying.lane is Lane.RETRY
    # Same lane, and the reason codes keep the two apart.
    assert abandoned.lane_reason == rings.REASON_ABANDONED
    assert still_trying.lane_reason == rings.REASON_NOT_TERMINAL
    assert abandoned.lane_reason != still_trying.lane_reason
    # And it never reaches the rejection it would otherwise have earned.
    assert _verdict(state=OK).lane is Lane.REJECTED_CLASSIFICATION
    assert abandoned.lane is not Lane.REJECTED_CLASSIFICATION


def test_guard_demoted_exists_wherever_a_span_verification_demotes_a_ring():
    """R2.1's seventh state, tied to the event that produces it."""
    body = ("The tribunal considered whether the promise utility doctrine as "
            "applied by the domestic courts breached the minimum standard.")
    # A model claim whose span is simply not in the document.
    invented = rings.merged_finding(
        RING_IP, model_claimed=True, model_strength=Strength.STRONG,
        evidence_span="a sentence that appears nowhere in this document at all",
        raw_text=body)
    assert invented.guard_demoted
    assert invented.semantic_credited is Strength.ABSENT
    assert invented.model_claimed_strength is Strength.STRONG

    # A span that verifies only in the title: the title cap is also a demotion.
    title = "Promise utility doctrine applied by the domestic courts"
    capped = rings.merged_finding(
        RING_IP, model_claimed=True, model_strength=Strength.STRONG,
        evidence_span=title, title=title, headline_only=True)
    assert capped.evidence_verified and capped.evidence_source_field == "title"
    assert capped.semantic_credited is Strength.WEAK
    assert capped.guard_demoted

    # A span that verifies in the body at the claimed strength is NOT a demotion.
    honest = rings.merged_finding(
        RING_IP, model_claimed=True, model_strength=Strength.PRESENT,
        evidence_span="the promise utility doctrine as applied by the domestic "
                      "courts breached the minimum standard",
        raw_text=body)
    assert honest.evidence_verified and not honest.guard_demoted
    assert honest.semantic_credited is Strength.PRESENT

    # And the state follows the event, in both directions.
    assert rings.classification_state(outcome="ok", guard_demoted=True) \
        is ClassifyState.GUARD_DEMOTED
    assert rings.classification_state(outcome="ok", guard_demoted=False) \
        is ClassifyState.OK_FIRST_PASS


def test_a_verdict_cannot_claim_a_demotion_its_findings_do_not_show():
    with pytest.raises(InvariantViolation, match="no ring was demoted"):
        _verdict(state=ClassifyState.GUARD_DEMOTED)


def test_no_ip_ring_can_ever_reach_match_whatever_else_is_true():
    # The single most important closed statement in the file. Example 4 is one
    # point in this space; this is the space.
    for jrm, ja in itertools.product(ALL_STRENGTHS, repeat=2):
        for ip in (Strength.ABSENT, Strength.WEAK):
            for nexus, location, validity in itertools.product(
                    ALL_NEXUS, ALL_LOCATIONS, ALL_VALIDITIES):
                if _verdict_construction_is_forbidden(nexus, location, validity):
                    continue
                v = _verdict(ip, jrm, ja, nexus=nexus, location=location,
                             validity=validity)
                assert v.lane is not Lane.MATCH


def test_the_model_score_is_read_by_nothing_that_decides_anything():
    # Every score from 0 to 100, over every ring configuration, on a state that
    # is otherwise as favourable as it gets. The lane never moves.
    for ip, jrm, ja in itertools.product(ALL_STRENGTHS, repeat=3):
        baseline = _verdict(ip, jrm, ja, score=None)
        for score in (0, 25, 39, 40, 55, 69, 70, 95, 100):
            v = _verdict(ip, jrm, ja, score=score)
            assert (v.lane, v.lane_reason) == (baseline.lane, baseline.lane_reason)
            assert v.model_score_advisory == score      # preserved, not consulted


def test_a_verdict_always_carries_exactly_three_findings_one_per_ring():
    with pytest.raises(InvariantViolation, match="exactly 3 findings"):
        RingVerdict(findings=_findings(Strength.PRESENT, Strength.PRESENT,
                                       Strength.ABSENT)[:2],
                    isds_nexus=Nexus.ESTABLISHED,
                    evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
                    evidence_validity=EvidenceValidity.VERIFIED,
                    classification_state=OK, path=DerivationPath.DETERMINISTIC)
    # Same three strengths, wrong order: still refused. The rings are named, and
    # a jurisdictional finding is not a judicial one that turned up in slot two.
    swapped = _findings(Strength.PRESENT, Strength.WEAK, Strength.ABSENT)
    with pytest.raises(InvariantViolation, match="one per ring in order"):
        RingVerdict(findings=(swapped[1], swapped[0], swapped[2]),
                    isds_nexus=Nexus.ESTABLISHED,
                    evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
                    evidence_validity=EvidenceValidity.VERIFIED,
                    classification_state=OK, path=DerivationPath.DETERMINISTIC)
    # And a ring that is not one of the three cannot be a finding at all.
    with pytest.raises(InvariantViolation, match="never interchangeable"):
        rings.lexical_finding("ip_as_investment_v2", 12)


def test_absence_is_recorded_as_a_finding_not_as_a_missing_entry():
    v = _verdict(Strength.ABSENT, Strength.ABSENT, Strength.ABSENT)
    assert len(v.findings) == 3
    assert all(f.strength is Strength.ABSENT for f in v.findings)
    assert [f.ring for f in v.findings] == [RING_IP, RING_JRM, RING_JA]
    # Read the body, found nothing: that is a conclusion we are entitled to.
    assert v.lane is Lane.REJECTED_CLASSIFICATION
    assert v.lane_reason == rings.REASON_OFF_THEME_ON_READ_BODY


# =============================================================================
# 2. Parity — the path is not an input to the decision
# =============================================================================
PARITY_BODY = (
    "The tribunal held that the promise utility doctrine as applied by the "
    "domestic courts invalidated the claimant's patents. It further held that "
    "the Supreme Court judgment setting aside the award was manifestly unjust "
    "and shocked a sense of judicial propriety. The respondent's objection was "
    "that the claimant restructured its investment to gain treaty protection "
    "against a reasonably foreseeable dispute, an abuse of right."
)
PARITY_SPANS = {
    RING_IP: "the promise utility doctrine as applied by the domestic courts "
             "invalidated the claimant's patents",
    RING_JRM: "the Supreme Court judgment setting aside the award was manifestly "
              "unjust and shocked a sense of judicial propriety",
    RING_JA: "restructured its investment to gain treaty protection against a "
             "reasonably foreseeable dispute, an abuse of right",
}


def test_identical_findings_derive_identical_lanes_on_either_path():
    for ip, jrm, ja in itertools.product(ALL_STRENGTHS, repeat=3):
        findings = _findings(ip, jrm, ja)
        made = {}
        for path in DerivationPath:
            v = RingVerdict(findings=findings, isds_nexus=Nexus.ESTABLISHED,
                            evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
                            evidence_validity=EvidenceValidity.VERIFIED,
                            classification_state=OK, path=path,
                            model_score_advisory=95 if path is DerivationPath.MODEL
                            else None)
            made[path] = (v.lane.value, v.lane_reason)
        assert len(set(made.values())) == 1, \
            f"path changed the lane for {(ip, jrm, ja)}: {made}"


def test_a_stubbed_model_path_and_the_keyword_path_agree_ring_for_ring():
    """Same document, same conclusions, arrived at differently: same lane.

    The deterministic side is built from lexical subtotals at each rung. The
    model side is built from verified evidence spans that really are in
    PARITY_BODY, at the same strengths. Nothing but `path` and `basis` differs,
    and neither is an input to `derive_lane`.
    """
    for strength in (Strength.PRESENT, Strength.STRONG):
        deterministic = RingVerdict(
            findings=_findings(strength, strength, strength),
            isds_nexus=Nexus.ESTABLISHED,
            evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
            evidence_validity=EvidenceValidity.VERIFIED,
            classification_state=OK, path=DerivationPath.DETERMINISTIC)

        model_findings = tuple(
            rings.merged_finding(ring, model_claimed=True, model_strength=strength,
                                 evidence_span=PARITY_SPANS[ring],
                                 raw_text=PARITY_BODY)
            for ring in rings.RINGS)
        # The model side really did verify — otherwise this proves nothing.
        assert all(f.evidence_verified for f in model_findings)
        assert all(f.basis is Basis.SEMANTIC for f in model_findings)
        assert all(f.evidence_source_field == "raw_text" for f in model_findings)
        assert all(f.strength is strength for f in model_findings)

        model = RingVerdict(
            findings=model_findings, isds_nexus=Nexus.ESTABLISHED,
            evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
            evidence_validity=EvidenceValidity.VERIFIED,
            classification_state=OK, path=DerivationPath.MODEL,
            model_score_advisory=55)

        assert (model.lane, model.lane_reason) == \
            (deterministic.lane, deterministic.lane_reason)
        assert model.lane is Lane.MATCH


# =============================================================================
# 3. The named boundary cases
# =============================================================================
def _item(source, title, body="", summary="", enriched=False):
    return CandidateItem(source, f"http://x/{title[:12]}", f"http://x/{title[:12]}",
                         title, datetime.datetime.now(UTC), summary, body,
                         {"enriched": True} if enriched else {})


def _shadow(item, *, model_rings=(), score=None, outcome="ok", attempts=1,
            retried_strict=False, abandoned=False, headline_only=False,
            body_fetched=False, fetch_outcome="not_attempted",
            v2_strengths=None, v2_spans=None, v2_basis=None):
    """Run the real shadow builder over a real item, as main.py does.

    ``metadata`` carries `classify_path="llm"` because a bare `matched_rings`
    list is only a MODEL claim when a model actually answered — see
    `rings._legacy_model_claims`, which used to read the attribute
    unconditionally and so recorded the keyword scorer's own hits as unverified
    model claims on every offline run.
    """
    class _Stub:
        matched_rings = list(model_rings)
        relevance_score = score
        metadata = {"classify_path": "llm"}

    kwargs = {}
    if v2_strengths is not None:
        kwargs["v2_strengths"] = v2_strengths
        kwargs["v2_spans"] = v2_spans or {}
        kwargs["v2_basis"] = v2_basis or "semantic:test-model-id"
    elif v2_basis is not None:
        kwargs["v2_basis"] = v2_basis
    return rings.shadow_verdict(
        item, lexical_result=keyword_score(item), classified=_Stub(),
        classification_outcome=outcome, attempts=attempts,
        retried_strict=retried_strict, abandoned=abandoned,
        headline_only=headline_only, body_fetched=body_fetched,
        fetch_outcome=fetch_outcome, **kwargs)


EXAMPLE_4_BODY = (
    "A construction investor filed an ICSID claim contending that a domestic "
    "Supreme Court judgment setting aside a commercial arbitration award was "
    "manifestly unjust and shocked a sense of judicial propriety, amounting to a "
    "denial of justice and a breach of the minimum standard of treatment. The "
    "dispute concerns infrastructure concessions, not intellectual property, and "
    "raises no abuse-of-right or treaty-shopping issue."
)


def test_example_4_the_taught_55_is_never_a_match():
    """prompts/classifier.txt Example 4, run through the contract.

    The item the audit found: judicial ring only, no IP, no jurisdictional
    doctrine, taught to the model as a 55 — over the publication threshold. V1
    publishes it on the score. Here the score is carried, ignored, and the item
    goes to the library because one non-IP ring is not the theme.
    """
    v = _shadow(_item("unctad_isds", "Investor alleges denial of justice",
                      body=EXAMPLE_4_BODY, enriched=True),
                model_rings=[RING_JRM], score=55, body_fetched=True,
                fetch_outcome="ok")

    assert v.lane is not Lane.MATCH
    assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    assert v.lane_reason == rings.REASON_SINGLE_NO_IP_RING
    assert v.model_score_advisory == 55            # kept, and inert
    assert v.strength(RING_IP) < Strength.PRESENT
    assert v.strength(RING_JRM) >= Strength.PRESENT
    assert v.strength(RING_JA) is Strength.ABSENT
    # The nexus IS established (an ICSID claim in the body) — it fails on the
    # rings, which is the honest reason, not on a technicality about sourcing.
    assert v.isds_nexus is Nexus.ESTABLISHED
    assert not v.publishable


def test_a_domestic_trade_secret_suit_goes_to_the_library_not_the_digest():
    # Red-team probe N2 (instrument map §3): scores 33 on the keyword path, above
    # the operative publication floor of 25. Ring 1 can be genuinely lit up by a
    # domestic case; the nexus is the thing that tells them apart.
    body = ("A specialty chemicals manufacturer filed suit in state court against "
            "a former process engineer, alleging misappropriation of trade "
            "secrets and intellectual property covering its catalyst "
            "formulations. No government measure is at issue.")
    v = _shadow(_item("bing_news", "Chemicals maker sues engineer", body=body,
                      enriched=True),
                model_rings=[RING_IP], score=33, body_fetched=True,
                fetch_outcome="ok")
    assert v.isds_nexus in (Nexus.ABSENT, Nexus.INDETERMINATE)
    assert v.lane is not Lane.MATCH
    assert v.lane_reason in (rings.REASON_NO_NEXUS,
                             rings.REASON_OFF_THEME_ON_READ_BODY)
    # And the nexus finding is only allowed to be ABSENT because a body was read.
    if v.isds_nexus is Nexus.ABSENT:
        assert v.evidence_location is EvidenceLocation.ACCESSIBLE_BODY


def test_pharma_news_with_no_isds_is_not_a_match():
    # Red-team probe N1: also 33 on the keyword path.
    body = ("A pharmaceutical company announced that its patent on a diabetes "
            "treatment had been upheld following a regulatory data exclusivity "
            "review. Shares rose on the news.")
    v = _shadow(_item("bing_news", "Pharma patent upheld", body=body,
                      enriched=True),
                model_rings=[RING_IP], score=33, body_fetched=True,
                fetch_outcome="ok")
    assert v.lane is not Lane.MATCH
    assert v.isds_nexus is not Nexus.ESTABLISHED


def test_generic_jurisdictional_jurisprudence_without_ip_is_a_lead_at_most():
    # Both non-IP rings present (R2.1 class B3): a real ISDS development, and
    # still not this project's question.
    v = _verdict(Strength.ABSENT, Strength.PRESENT, Strength.STRONG,
                 nexus=Nexus.ESTABLISHED)
    assert v.lane is Lane.ADJACENT_LEAD
    assert v.lane_reason == rings.REASON_JRM_AND_JA_NO_IP

    # One of them alone drops to the library.
    alone = _verdict(Strength.ABSENT, Strength.ABSENT, Strength.STRONG,
                     nexus=Nexus.ESTABLISHED)
    assert alone.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    assert alone.lane_reason == rings.REASON_SINGLE_NO_IP_RING

    # IP alone is the mirror image: adjacent, never a match.
    ip_alone = _verdict(Strength.STRONG, Strength.ABSENT, Strength.ABSENT,
                        nexus=Nexus.ESTABLISHED)
    assert ip_alone.lane is Lane.ADJACENT_LEAD
    assert ip_alone.lane_reason == rings.REASON_IP_WITHOUT_SECOND_RING


def test_a_headline_only_item_can_never_match_and_can_never_be_found_absent():
    # iareporter_headlines sets raw_text = title and is in NO_BODY_FETCH; 10 of
    # the 14 published entries came from it.
    headline = "Tribunal issues award in pharmaceutical patent dispute with Colombia"
    v = _shadow(_item("iareporter_headlines", headline, body=headline),
                model_rings=[RING_IP, RING_JRM], score=95, headline_only=True)

    assert v.evidence_location is EvidenceLocation.TITLE
    assert v.evidence_validity is EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE
    assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    assert v.lane_reason == rings.REASON_INCONCLUSIVE_LOCATION
    assert v.isds_nexus is not Nexus.ABSENT, \
        "we concluded there is no treaty nexus from a headline"
    # Even a 95 with two rings claimed cannot lift it.
    assert not v.publishable

    # And the construction the archive actually contains — a negative conclusion
    # about an unread body — is refused outright.
    with pytest.raises(InvariantViolation, match="absence is a finding"):
        _verdict(nexus=Nexus.ABSENT, location=EvidenceLocation.TITLE,
                 validity=EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE)


def test_a_headline_span_cannot_carry_a_ring_past_weak():
    headline = ("Supreme Court judgment on trademark exploitation held a denial "
                "of justice by tribunal")
    # For a headline-only source the fetcher sets raw_text = title, so a
    # concatenating check (classify._quote_in_source) reads the headline as body.
    f = rings.merged_finding(
        RING_JRM, model_claimed=True, model_strength=Strength.STRONG,
        evidence_span="Supreme Court judgment on trademark exploitation held a "
                      "denial of justice",
        title=headline, raw_text=headline, headline_only=True)
    assert f.evidence_verified is True
    assert f.evidence_source_field == "title"
    assert f.strength is Strength.WEAK, "a headline carried a ring to strong"

    # The same span in a real body is not capped.
    body = "Preamble. " + headline + " The tribunal so held."
    g = rings.merged_finding(
        RING_JRM, model_claimed=True, model_strength=Strength.STRONG,
        evidence_span="Supreme Court judgment on trademark exploitation held a "
                      "denial of justice",
        title="Short headline", raw_text=body, headline_only=False)
    assert g.evidence_source_field == "raw_text"
    assert g.strength is Strength.STRONG

    # And the cap is an invariant, not merely a computation: asserting it
    # directly is refused too.
    with pytest.raises(InvariantViolation, match="found only in the title"):
        RingFinding(ring=RING_JRM, basis=Basis.SEMANTIC, lexical_subtotal=0,
                    lexical_hits=(), strength=Strength.STRONG,
                    evidence_span="a span long enough to count as evidence here",
                    evidence_verified=True, evidence_source_field="title")


def test_a_failed_body_retrieval_can_support_no_negative_conclusion():
    body_we_never_got = ""
    v = _shadow(_item("italaw", "Case page", body=body_we_never_got, summary=""),
                model_rings=[], score=0, fetch_outcome="refused")
    assert v.evidence_location is EvidenceLocation.UNAVAILABLE_BODY
    assert v.evidence_validity is EvidenceValidity.UNVERIFIED
    assert v.lane is Lane.HEADLINE_ONLY_LIBRARY_LEAD
    assert v.lane_reason == rings.REASON_INCONCLUSIVE_LOCATION
    assert v.lane is not Lane.REJECTED_CLASSIFICATION

    for validity in (EvidenceValidity.UNVERIFIED,
                     EvidenceValidity.UNVERIFIABLE_IN_PRINCIPLE):
        with pytest.raises(InvariantViolation, match="absence is a finding"):
            _verdict(nexus=Nexus.ABSENT,
                     location=EvidenceLocation.UNAVAILABLE_BODY, validity=validity)
    with pytest.raises(InvariantViolation, match="failed to retrieve"):
        _verdict(location=EvidenceLocation.UNAVAILABLE_BODY,
                 validity=EvidenceValidity.VERIFIED)

    # "not attempted" is not "refused": choosing not to fetch leaves the summary
    # standing as the evidence location, which is a different fact.
    quiet = _shadow(_item("iisd_itn", "Case note", summary="A short RSS summary."),
                    fetch_outcome="not_attempted")
    assert quiet.evidence_location is EvidenceLocation.SUMMARY


def test_evidence_location_reads_the_text_we_hold_not_the_field_it_arrived_in():
    """`raw_text` means three different things depending on the source.

    icsid / italaw / unctad_isds / pca_press / iareporter_headlines set
    `raw_text = title`; bing_news / gmail_scholar / google_alerts set it to the
    feed summary; iisd_itn and anything `enrich` fetched put a real body there.
    A location rule that trusted the field name would treat five sources'
    headlines as read bodies — and a read body is what licenses a negative
    conclusion, so the error would land precisely where it does most damage.
    """
    title = "Tribunal issues award in patent dispute"

    # raw_text == title (icsid, italaw, unctad_isds, pca_press).
    assert rings.derive_location(headline_only=False, title=title, summary="",
                                 raw_text=title) is EvidenceLocation.TITLE
    # raw_text == summary (bing_news, gmail_scholar, google_alerts).
    snippet = "A short syndicated snippet about the award and its parties."
    assert rings.derive_location(headline_only=False, title=title,
                                 summary=snippet, raw_text=snippet) \
        is EvidenceLocation.SUMMARY
    # A real feed body (iisd_itn).
    body = snippet + " The tribunal went on to hold, at length, the following."
    assert rings.derive_location(headline_only=False, title=title,
                                 summary=snippet, raw_text=body) \
        is EvidenceLocation.ACCESSIBLE_BODY
    # A fetched body is a body even if it happens to echo the summary.
    assert rings.derive_location(headline_only=False, body_fetched=True,
                                 title=title, summary=snippet, raw_text=snippet) \
        is EvidenceLocation.ACCESSIBLE_BODY
    # Policy beats everything: the body of a NO_BODY_FETCH source is never read.
    assert rings.derive_location(headline_only=True, body_fetched=True,
                                 title=title, raw_text=body) \
        is EvidenceLocation.TITLE
    # A refusal reports as unavailable only when nothing else stands in for it.
    assert rings.derive_location(headline_only=False, fetch_outcome="refused",
                                 title=title, raw_text=title) \
        is EvidenceLocation.UNAVAILABLE_BODY
    assert rings.derive_location(headline_only=False, fetch_outcome="refused",
                                 title=title, summary=snippet, raw_text=body) \
        is EvidenceLocation.ACCESSIBLE_BODY
    # "not attempted" is not a refusal.
    assert rings.derive_location(headline_only=False,
                                 fetch_outcome="not_attempted", title=title,
                                 raw_text=title) is EvidenceLocation.TITLE

    # The consequence that matters: a headline-shaped item cannot be found to
    # have no treaty nexus, because it was never read.
    v = _shadow(_item("unctad_isds", title, body=title))
    assert v.evidence_location is EvidenceLocation.TITLE
    assert v.isds_nexus is not Nexus.ABSENT


def test_the_merge_rule_is_a_per_ring_max_of_lexical_and_verified_semantic():
    body = ("The tribunal addressed whether the corporate restructuring "
            "constituted an abuse of right in the circumstances of this claim.")
    span = "the corporate restructuring constituted an abuse of right"

    # Model says strong, and can prove it: verified semantic lifts the ring.
    lifted = rings.merged_finding(RING_JA, lexical_subtotal=0, model_claimed=True,
                                  model_strength=Strength.STRONG,
                                  evidence_span=span, raw_text=body)
    assert lifted.strength is Strength.STRONG
    assert lifted.basis is Basis.SEMANTIC

    # Model says strong and cannot prove it: contributes NOTHING. The ring falls
    # back to its lexical evidence, and the failed claim is recorded as such.
    unproven = rings.merged_finding(
        RING_JA, lexical_subtotal=rings.PRESENT_FLOOR - 1, model_claimed=True,
        model_strength=Strength.STRONG,
        evidence_span="the tribunal found a manifest abuse of process throughout",
        raw_text=body)
    assert unproven.strength is Strength.WEAK
    assert unproven.basis is Basis.SEMANTIC_UNVERIFIED
    assert unproven.evidence_verified is False
    assert unproven.evidence_source_field == ""

    # Lexical says more than the model does: the max keeps the lexical reading.
    disagreement = rings.merged_finding(
        RING_JA, lexical_subtotal=rings.STRONG_SUBTOTAL, model_claimed=True,
        model_strength=Strength.WEAK, evidence_span=span, raw_text=body)
    assert disagreement.strength is Strength.STRONG
    assert disagreement.basis is Basis.BOTH

    # A span too short to be evidence is not evidence.
    trivial = rings.merged_finding(RING_JA, model_claimed=True,
                                   model_strength=Strength.STRONG,
                                   evidence_span="abuse", raw_text=body)
    assert trivial.strength is Strength.ABSENT
    assert trivial.basis is Basis.SEMANTIC_UNVERIFIED

    # And the rule holds as an invariant: a strength above the lexical floor
    # with nothing verified cannot be constructed at all.
    with pytest.raises(InvariantViolation, match="did not verify"):
        RingFinding(ring=RING_JA, basis=Basis.SEMANTIC_UNVERIFIED,
                    lexical_subtotal=0, lexical_hits=(), strength=Strength.STRONG,
                    evidence_span="a claimed span that was never verified at all",
                    evidence_verified=False, evidence_source_field="")
    with pytest.raises(InvariantViolation, match="below its own lexical evidence"):
        RingFinding(ring=RING_JA, basis=Basis.LEXICAL,
                    lexical_subtotal=rings.STRONG_SUBTOTAL, lexical_hits=(),
                    strength=Strength.WEAK, evidence_span="",
                    evidence_verified=False, evidence_source_field="")


def test_the_score_25_archive_pattern_never_reaches_match():
    """Nine of the fourteen published entries scored 25.

    25 is unreachable on the keyword path (instrument map §3), so every one of
    them is model output: a LOW score with a thin ring list, published only
    because the fill floor was 25. Under the contract the same finding is a lead
    or a library entry, and there is no configuration of it that is a match.
    """
    for ring in rings.RINGS:
        for nexus in (Nexus.ESTABLISHED, Nexus.ASSERTED):
            findings = tuple(
                rings.merged_finding(
                    r, lexical_subtotal=1 if r == ring else 0,
                    model_claimed=(r == ring), model_strength=Strength.PRESENT,
                    evidence_span="")                       # the prompt gives none
                for r in rings.RINGS)
            v = RingVerdict(findings=findings, isds_nexus=nexus,
                            evidence_location=EvidenceLocation.SUMMARY,
                            evidence_validity=EvidenceValidity.VERIFIED,
                            classification_state=OK,
                            path=DerivationPath.MERGED, model_score_advisory=25)
            assert v.lane is not Lane.MATCH
            assert v.lane in (Lane.HEADLINE_ONLY_LIBRARY_LEAD, Lane.ADJACENT_LEAD)
            assert v.lane_reason == rings.REASON_NO_RING_AT_STRENGTH
            assert v.finding(ring).basis is Basis.SEMANTIC_UNVERIFIED


def test_a_non_terminal_classification_is_retry_and_nothing_else():
    for state in (ClassifyState.MALFORMED_OUTPUT, ClassifyState.PROVIDER_FAILURE):
        v = _verdict(Strength.STRONG, Strength.STRONG, Strength.STRONG,
                     state=state, score=95)
        assert v.lane is Lane.RETRY
        assert v.lane_reason == rings.REASON_NOT_TERMINAL
    with pytest.raises(InvariantViolation,
                       match="must be a ClassifyState"):
        _verdict(state="probably_fine")
    # The raw operational outcome is still validated when one is recorded.
    with pytest.raises(InvariantViolation, match="not a ClassifyOutcome value"):
        RingVerdict(findings=_findings(*(Strength.ABSENT,) * 3),
                    isds_nexus=Nexus.ESTABLISHED,
                    evidence_location=EvidenceLocation.ACCESSIBLE_BODY,
                    evidence_validity=EvidenceValidity.VERIFIED,
                    classification_state=OK, path=DerivationPath.DETERMINISTIC,
                    classification_outcome="probably_fine")


def test_the_nexus_lexicon_is_a_closed_list_matched_after_normalisation():
    body_ip = "The parties are in ICSID Case No. ARB/16/34 before the tribunal."
    assert rings.derive_nexus(source="bing_news", text=body_ip,
                              location=EvidenceLocation.ACCESSIBLE_BODY) \
        is Nexus.ESTABLISHED
    # Smart dashes fold, so investor–State reads as investor-state.
    assert rings.derive_nexus(source="bing_news",
                              text="an investor–State claim was filed",
                              location=EvidenceLocation.ACCESSIBLE_BODY) \
        is Nexus.ASSERTED
    # Membership of an ISDS-only source establishes it without any lexeme.
    assert rings.derive_nexus(source="italaw", text="nothing relevant here",
                              location=EvidenceLocation.TITLE) is Nexus.ESTABLISHED
    # Nothing found, and we read a body: absent. Nothing found on a headline:
    # indeterminate. This is the whole of rule 2, in two lines.
    assert rings.derive_nexus(source="bing_news", text="a domestic contract suit",
                              location=EvidenceLocation.ACCESSIBLE_BODY) \
        is Nexus.ABSENT
    for loc in (EvidenceLocation.TITLE, EvidenceLocation.SUMMARY,
                EvidenceLocation.UNAVAILABLE_BODY):
        assert rings.derive_nexus(source="bing_news",
                                  text="a domestic contract suit", location=loc) \
            is Nexus.INDETERMINATE


def test_an_asserted_nexus_needs_verified_evidence_to_carry_a_match():
    strong = dict(ip=Strength.STRONG, jrm=Strength.STRONG, ja=Strength.STRONG)
    assert _verdict(**strong, nexus=Nexus.ESTABLISHED).lane is Lane.MATCH
    assert _verdict(**strong, nexus=Nexus.ASSERTED,
                    validity=EvidenceValidity.VERIFIED).lane is Lane.MATCH
    # Unverified evidence base: adjacent, and the reason names the failed
    # predicate rather than pretending the rings were the problem.
    blocked = _verdict(**strong, nexus=Nexus.ASSERTED,
                       validity=EvidenceValidity.UNVERIFIED)
    assert blocked.lane is Lane.ADJACENT_LEAD
    assert blocked.lane_reason == rings.REASON_IP_BLOCKED_PREDICATE
    assert not rings.nexus_supports_match(Nexus.ASSERTED,
                                          EvidenceValidity.UNVERIFIED)
    for nexus in (Nexus.INDETERMINATE, Nexus.ABSENT):
        assert not rings.nexus_supports_match(nexus, EvidenceValidity.VERIFIED)


# =============================================================================
# Legacy scoring is untouched
# =============================================================================
def test_the_negative_signal_cap_still_behaves_exactly_as_it_did():
    """src/rings.py adds a layer; it does not reach back into keyword_score.

    No historical score may be recomputed or overwritten, so the legacy scorer's
    own behaviour — including the negative-signal cap at 35 — has to be provably
    unchanged by anything in this session.
    """
    now = datetime.datetime.now(UTC)

    def score(text):
        return keyword_score(CandidateItem("s", "i", "u", "t", now, "", text, {}))

    # A mining/concession item with no rescuing ring is capped.
    mining = score("A foreign mining company launched an arbitration after the "
                   "government revoked its copper mineral concession, claiming "
                   "direct expropriation.")
    assert mining["negative_signal"] is True
    assert mining["relevance_score"] <= 35

    # An IP or judicial ring genuinely PRESENT rescues it — the cap does not
    # apply, and that asymmetry is the pre-existing behaviour.
    rescued = score(
        "A mining company's claim turned on a domestic court judgment said to be "
        "a manifestly unjust judgment that shocks a sense of judicial propriety, "
        "a denial of justice and a breach of the minimum standard of treatment "
        "by the Supreme Court.")
    assert rescued["negative_signal"] is True
    assert rescued["relevance_score"] > 35

    # And the ladder reads those same subtotals without altering them.
    for result in (mining, rescued):
        for ring, subtotal in result["per_ring_subtotal"].items():
            assert rings.strength_for_subtotal(subtotal) in set(Strength)


def test_the_shadow_derivation_is_byte_stable_for_the_same_input():
    item = _item("unctad_isds", "Investor alleges denial of justice",
                 body=EXAMPLE_4_BODY, enriched=True)
    a = _shadow(item, model_rings=[RING_JRM], score=55, body_fetched=True,
                fetch_outcome="ok").to_telemetry()
    b = _shadow(item, model_rings=[RING_JRM], score=55, body_fetched=True,
                fetch_outcome="ok").to_telemetry()
    assert a == b
    # Telemetry-safe: enumerated values, ints, hex digests, and our own ring
    # names. The span TEXT never appears — only its length and its sha256, which
    # is what lets a later query ask whether two runs saw the same span without
    # analytics/ ever holding a line of anyone else's prose.
    import json
    blob = json.dumps(a)
    assert '"evidence_span"' not in blob
    assert "Supreme Court" not in blob
    for ring in a["rings"].values():
        assert set(ring) >= {"evidence_span_len", "evidence_span_sha256"}
        assert ring["evidence_span_sha256"] in ("",) or len(
            ring["evidence_span_sha256"]) == 64
    assert all(len(v) <= 200 for v in (a["lane"], a["lane_reason"], a["nexus"]))
