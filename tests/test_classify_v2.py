"""The V2 semantic shadow path, and the one property it exists to guarantee.

THE PROPERTY: a lexical derivation is never reported under a model's identity.
It is asserted here over EVERY route that can fail — no provider, a provider
error, an unparseable answer, an answer that parses but claims a fourth ring,
the flag being off, and the item simply not being in the sample — rather than on
the happy path plus a hopeful comment. That is the named defect, so it gets an
exhaustive test and not an example.
"""

import datetime
import json

import pytest

from src import classify as classify_mod
from src import classify_v2, config, rings
from src.classify_v2 import V2Result
from src.rings import ClassifyState, EvidenceLocation, Nexus, Strength
from src.sources.base import CandidateItem

UTC = datetime.timezone.utc
FIXED = datetime.datetime(2026, 8, 1, 12, 0, tzinfo=UTC)

RING_IP = rings.RING_IP
RING_JRM = rings.RING_JRM
RING_JA = rings.RING_JA

BODY = (
    "In ICSID Case No. ARB/16/34 the claimant argued that the invalidation of "
    "its patents under the promise utility doctrine by the domestic courts was "
    "a judicial measure breaching the minimum standard of treatment. The "
    "respondent replied that the claimant had restructured its investment to "
    "gain treaty protection against a reasonably foreseeable dispute, an abuse "
    "of right.")


def _item(source="italaw", title="Patent invalidation challenged", body=BODY,
          summary=""):
    return CandidateItem(source, f"http://x/{title[:10]}", f"http://x/{title[:10]}",
                         title, FIXED, summary, body, {})


def _good_payload(ip="strong", jrm="strong", ja="strong"):
    return json.dumps({
        "rings": {
            RING_IP: {"strength": ip,
                      "evidence_span": "the invalidation of its patents under "
                                       "the promise utility doctrine"},
            RING_JRM: {"strength": jrm,
                       "evidence_span": "a judicial measure breaching the "
                                        "minimum standard of treatment"},
            RING_JA: {"strength": ja,
                      "evidence_span": "restructured its investment to gain "
                                       "treaty protection against a reasonably "
                                       "foreseeable dispute"},
        },
        "isds_nexus": "established",
        "nexus_evidence": "ICSID Case No. ARB/16/34",
        "thematic_tags": ["patent", "abuse_of_right"],
        "digest_summary": "A patent invalidation is challenged. All three rings "
                          "are engaged.",
    })


@pytest.fixture
def provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "claude")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_MODEL", "test-model-id")


def _respond_with(monkeypatch, *replies):
    """Stub the provider with a scripted sequence of replies."""
    calls = []

    def responder(prompt):
        calls.append(prompt)
        reply = replies[min(len(calls) - 1, len(replies) - 1)]
        if isinstance(reply, Exception):
            raise reply
        return reply

    monkeypatch.setattr(classify_mod, "_call_anthropic", responder)
    return calls


# =============================================================================
# The prompt
# =============================================================================
def test_the_item_text_token_appears_exactly_once_in_the_v2_prompt():
    """Five copies of the body per request is what the V1 prompt does."""
    template = classify_v2.load_v2_prompt()
    assert template.count("{{TEXT}}") == 1
    for token in ("{{TITLE}}", "{{SOURCE}}", "{{URL}}"):
        assert template.count(token) == 1, f"{token} appears more than once"


def test_the_v2_prompt_carries_no_relevance_score_contract():
    template = classify_v2.load_v2_prompt().lower()
    assert "relevance_score" in template  # only to say it is removed
    assert "there is no relevance_score" in template


def test_the_built_prompt_substitutes_the_candidates_own_fields():
    prompt = classify_v2.build_v2_prompt(_item())
    assert "{{TEXT}}" not in prompt and "{{TITLE}}" not in prompt
    assert BODY in prompt
    assert prompt.count(BODY) == 1, "the body was inlined more than once"


# =============================================================================
# The strict parser
# =============================================================================
def test_a_well_formed_answer_parses_to_closed_vocabulary_values():
    parsed = classify_v2.parse_v2_response(_good_payload())
    assert parsed is not None
    assert set(parsed["rings"]) == set(rings.RINGS)
    assert parsed["rings"][RING_IP]["strength"] is Strength.STRONG
    assert parsed["isds_nexus"] is Nexus.ESTABLISHED


def test_the_parser_accepts_a_fenced_answer():
    assert classify_v2.parse_v2_response(
        "```json\n" + _good_payload() + "\n```") is not None


@pytest.mark.parametrize("payload,why", [
    ("", "empty"),
    ("not json at all", "not json"),
    ('{"rings": {}}', "no rings"),
    (json.dumps({"rings": {RING_IP: {"strength": "strong",
                                     "evidence_span": "x" * 40}},
                 "isds_nexus": "established"}), "only one ring"),
])
def test_the_parser_rejects_a_malformed_answer(payload, why):
    assert classify_v2.parse_v2_response(payload) is None, why


def test_the_parser_rejects_a_fourth_ring_rather_than_dropping_it():
    """V1 coerces unknown rings away. A model inventing a ring is the event."""
    data = json.loads(_good_payload())
    data["rings"]["ip_as_a_service"] = {"strength": "strong",
                                        "evidence_span": "x" * 40}
    assert classify_v2.parse_v2_response(json.dumps(data)) is None


def test_the_parser_rejects_a_strength_word_outside_the_four():
    for word in ("medium", "moderate", "MEDIUM-HIGH", "3"):
        data = json.loads(_good_payload())
        data["rings"][RING_IP]["strength"] = word
        assert classify_v2.parse_v2_response(json.dumps(data)) is None, word


def test_the_parser_rejects_a_present_ring_with_no_evidence_span():
    """A strength with no evidence is the V1 defect under a new field name."""
    data = json.loads(_good_payload())
    data["rings"][RING_IP]["evidence_span"] = ""
    assert classify_v2.parse_v2_response(json.dumps(data)) is None
    # ...but "absent" with no span is exactly right.
    data["rings"][RING_IP] = {"strength": "absent", "evidence_span": ""}
    assert classify_v2.parse_v2_response(json.dumps(data)) is not None


# =============================================================================
# The call, and the basis it records
# =============================================================================
def test_a_parsed_answer_is_the_only_route_that_names_a_model(provider,
                                                              monkeypatch):
    _respond_with(monkeypatch, _good_payload())
    result = classify_v2.classify_item_v2(_item())
    assert result.ok
    assert result.basis == "semantic:test-model-id"
    assert classify_v2.basis_names_a_model(result.basis)


def test_no_provider_is_lexical_only_and_names_nothing(monkeypatch):
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = classify_v2.classify_item_v2(_item())
    assert not result.ok
    assert result.basis == classify_v2.V2_BASIS_LEXICAL_ONLY
    assert not classify_v2.basis_names_a_model(result.basis)
    assert result.model == ""


def test_a_provider_error_is_labelled_as_one_and_names_no_model_in_the_basis(
        provider, monkeypatch):
    _respond_with(monkeypatch, RuntimeError("connection reset"))
    result = classify_v2.classify_item_v2(_item())
    assert not result.ok
    assert result.basis == classify_v2.V2_BASIS_PROVIDER_ERROR
    assert not classify_v2.basis_names_a_model(result.basis)
    # The model is still recorded as an operational fact — "which model was
    # down" is a real question — but it is not the BASIS of anything.
    assert result.model == "test-model-id"
    assert result.outcome.value == "provider_error"


def test_a_malformed_answer_is_retried_once_and_then_labelled_malformed(
        provider, monkeypatch):
    calls = _respond_with(monkeypatch, "nonsense", "still nonsense")
    result = classify_v2.classify_item_v2(_item())
    assert len(calls) == 2, "the strict retry did not happen"
    assert "Return ONLY the raw JSON object" in calls[1]
    assert result.retried_strict and result.attempts == 2
    assert result.basis == classify_v2.V2_BASIS_MALFORMED
    assert not classify_v2.basis_names_a_model(result.basis)
    # Malformed is NOT a provider failure. The provider answered.
    assert result.basis != classify_v2.V2_BASIS_PROVIDER_ERROR
    assert result.outcome.value == "parse_failed"


def test_the_retry_recovers_a_first_attempt_that_would_not_parse(provider,
                                                                 monkeypatch):
    _respond_with(monkeypatch, "here you go: nonsense", _good_payload())
    result = classify_v2.classify_item_v2(_item())
    assert result.ok and result.retried_strict and result.attempts == 2


def test_every_failure_route_refuses_to_name_a_model_in_its_basis(provider,
                                                                  monkeypatch):
    """The named defect, closed over the whole failure space."""
    failures = [
        RuntimeError("boom"),
        "not json",
        json.dumps({"rings": {}}),
        json.dumps({"rings": {RING_IP: {"strength": "medium",
                                        "evidence_span": "x" * 40}}}),
        "",
    ]
    for reply in failures:
        _respond_with(monkeypatch, reply, reply)
        result = classify_v2.classify_item_v2(_item())
        assert not result.ok, reply
        assert not classify_v2.basis_names_a_model(result.basis), reply
        assert result.strengths == {} and result.spans == {}


# =============================================================================
# The derivation the call feeds
# =============================================================================
def _verdict_from(result, item, **kw):
    kwargs = dict(v2_basis=result.basis)
    if result.ok:
        kwargs.update(v2_strengths=result.strengths, v2_spans=result.spans)
    return rings.shadow_verdict(
        item, lexical_result=classify_mod.keyword_score(item),
        classified=type("S", (), {"matched_rings": [], "relevance_score": None,
                                  "metadata": {"classify_path": "llm"}})(),
        classification_outcome="ok", attempts=1, body_fetched=True,
        fetch_outcome="ok", **kwargs, **kw)


def test_verified_spans_actually_carry_rings_which_is_the_whole_point(provider,
                                                                      monkeypatch):
    """Parity, genuinely: the strengths come from the model and survive checking."""
    _respond_with(monkeypatch, _good_payload())
    item = _item()
    result = classify_v2.classify_item_v2(item)
    v = _verdict_from(result, item)

    assert v.claims_source == rings.CLAIMS_V2_PROMPT
    assert v.v2_basis == "semantic:test-model-id"
    for ring in rings.RINGS:
        f = v.finding(ring)
        assert f.evidence_verified, ring
        assert f.evidence_source_field == "raw_text", ring
        assert f.semantic_credited is Strength.STRONG, ring
        assert not f.guard_demoted, ring
    assert v.lane is rings.Lane.MATCH


def test_an_invented_span_contributes_nothing_and_is_recorded_as_a_demotion(
        provider, monkeypatch):
    payload = json.loads(_good_payload())
    payload["rings"][RING_IP]["evidence_span"] = (
        "a sentence the tribunal never wrote anywhere in this document")
    _respond_with(monkeypatch, json.dumps(payload))
    item = _item()
    v = _verdict_from(classify_v2.classify_item_v2(item), item)

    ip = v.finding(RING_IP)
    assert not ip.evidence_verified
    assert ip.semantic_credited is Strength.ABSENT
    assert ip.model_claimed_strength is Strength.STRONG
    assert ip.guard_demoted
    assert v.guard_demoted


def test_a_lexical_derivation_can_never_carry_a_model_basis():
    """The invariant, asserted at the constructor rather than by convention."""
    item = _item()
    with pytest.raises(rings.InvariantViolation, match="under a model's identity"):
        rings.shadow_verdict(
            item, lexical_result=classify_mod.keyword_score(item),
            classified=type("S", (), {"matched_rings": [], "relevance_score": None,
                                      "metadata": {}})(),
            classification_outcome="ok",
            v2_basis="semantic:some-model-we-did-not-call")


def test_the_keyword_path_does_not_record_its_own_hits_as_model_claims():
    """The bug `_legacy_model_claims` fixes, pinned.

    On the offline path `matched_rings` holds the KEYWORD scorer's rings. Read
    unconditionally, they were recorded as unverified claims by a model that was
    never called, so every offline run produced a page of `semantic_unverified`
    findings about a model that had not run.
    """
    item = _item()
    lexical = classify_mod.keyword_score(item)
    assert lexical["matched_rings"], "the probe must light up some ring"

    keyword_side = type("S", (), {
        "matched_rings": lexical["matched_rings"], "relevance_score": 40,
        "metadata": {"classify_path": "keyword"}})()
    v = rings.shadow_verdict(
        item, lexical_result=lexical, classified=keyword_side,
        classification_outcome="keyword_only_by_design", attempts=0,
        body_fetched=True, fetch_outcome="ok")

    assert v.claims_source == rings.CLAIMS_NONE
    assert v.v2_basis == "lexical_only"
    for ring in rings.RINGS:
        f = v.finding(ring)
        assert f.basis is rings.Basis.LEXICAL, ring
        assert f.model_claimed_strength is None, ring
        assert not f.guard_demoted, ring
    assert v.classification_state is ClassifyState.KEYWORD_ONLY


def test_a_provider_error_does_not_launder_keyword_rings_into_model_claims():
    """`classify_item` fills matched_rings from keyword_score on an outage."""
    item = _item()
    lexical = classify_mod.keyword_score(item)
    outage_side = type("S", (), {
        "matched_rings": lexical["matched_rings"], "relevance_score": 0,
        "metadata": {"classify_path": "llm"}})()
    v = rings.shadow_verdict(
        item, lexical_result=lexical, classified=outage_side,
        classification_outcome="provider_error", attempts=1,
        body_fetched=True, fetch_outcome="ok")
    assert v.claims_source == rings.CLAIMS_NONE
    assert v.classification_state is ClassifyState.PROVIDER_FAILURE
    assert v.lane is rings.Lane.RETRY


def test_the_legacy_v1_ring_list_is_recorded_and_wholly_demoted():
    """The measurement the audit asked for: V1 claims rings it cannot evidence."""
    item = _item()
    v1_side = type("S", (), {
        "matched_rings": [RING_IP, RING_JRM], "relevance_score": 70,
        "metadata": {"classify_path": "llm"}})()
    v = rings.shadow_verdict(
        item, lexical_result=classify_mod.keyword_score(item), classified=v1_side,
        classification_outcome="ok", attempts=1, body_fetched=True,
        fetch_outcome="ok")

    assert v.claims_source == rings.CLAIMS_LEGACY_V1
    assert v.v2_basis == "lexical_only", \
        "a V1 ring list is not a V2 semantic basis"
    for ring in (RING_IP, RING_JRM):
        f = v.finding(ring)
        assert f.model_claimed_strength is Strength.PRESENT, ring
        assert f.semantic_credited is Strength.ABSENT, ring
        assert f.guard_demoted, ring
    assert v.classification_state is ClassifyState.GUARD_DEMOTED


# =============================================================================
# The cost gate
# =============================================================================
def test_v2_shadow_calls_defaults_to_off():
    assert config._v2_shadow_calls("") == ("off", 0)
    assert config._v2_shadow_calls("off") == ("off", 0)
    # And the module-level resolution, as a default run sees it.
    assert config.V2_SHADOW_CALLS_MODE == config.V2_SHADOW_CALLS_OFF
    assert config.V2_SHADOW_CALLS_SPEC == "off"


def test_replace_is_refused_rather_than_honoured():
    """It would stop the legacy call, which is what production still gates on."""
    assert config._v2_shadow_calls("replace") == ("off", 0)


@pytest.mark.parametrize("raw,expected", [
    ("sample:3", ("sample", 3)),
    ("sample:1", ("sample", 1)),
    ("SAMPLE:5", ("sample", 5)),
    ("sample:0", ("off", 0)),
    ("sample:-2", ("off", 0)),
    ("sample:many", ("off", 0)),
    ("on", ("off", 0)),
    ("yes please", ("off", 0)),
])
def test_v2_shadow_calls_fails_closed_on_anything_it_does_not_understand(
        raw, expected):
    assert config._v2_shadow_calls(raw) == expected


def test_the_telemetry_section_names_no_model_when_no_call_was_made():
    section = classify_v2.telemetry_section(None, mode="off")
    assert section["called"] is False
    assert section["basis"] == "lexical_only"
    assert section["model"] == ""


def test_the_telemetry_section_of_a_failed_call_is_not_a_semantic_basis():
    failed = V2Result(basis=classify_v2.V2_BASIS_PROVIDER_ERROR,
                      outcome=classify_mod.ClassifyOutcome.PROVIDER_ERROR,
                      model="test-model-id", attempts=1)
    section = classify_v2.telemetry_section(failed, mode="sample:3")
    assert section["called"] is True
    assert not classify_v2.basis_names_a_model(section["basis"])
    assert section["model"] == "test-model-id"      # operational fact, not basis
