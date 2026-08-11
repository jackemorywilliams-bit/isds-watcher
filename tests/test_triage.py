"""Workstream F — semantic triage, tested against the items it exists to catch.

The adversarial cases are drawn from `analytics/fingerprint_probes.json` rather
than written here, because probes authored for a different purpose are a harder
test than probes authored for this one. Two of them score ZERO under
`keyword_score` while their expected band is HIGH or MEDIUM, and those two are
the entire argument for this workstream.
"""

import datetime
import json
import os

import pytest

from src import classify as classify_mod
from src import config, rings, triage
from src.classify import keyword_score
from src.rings import Strength
from src.sources.base import CandidateItem

UTC = datetime.timezone.utc
FIXED = datetime.datetime(2026, 8, 1, 12, 0, tzinfo=UTC)

RING_IP = rings.RING_IP
RING_JRM = rings.RING_JRM
RING_JA = rings.RING_JA

_PROBES = json.load(open(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "analytics", "fingerprint_probes.json"), encoding="utf-8"))["probes"]
PROBE = {p["id"]: p for p in _PROBES}


def _probe_item(probe_id, source="iisd_itn"):
    """A probe as a candidate. Its text becomes the SUMMARY, which is what
    triage reads — the pass runs before enrichment and never sees a body."""
    p = PROBE[probe_id]
    return CandidateItem(source, f"http://x/{probe_id}", f"http://x/{probe_id}",
                         probe_id.replace("_", " "), FIXED, p["text"], "", {})


def _item(source, sid, title, summary="", body=""):
    return CandidateItem(source, sid, f"http://x/{sid}", title, FIXED, summary,
                         body, {})


def _reply(ip="absent", jrm="absent", ja="absent"):
    return json.dumps({"rings": {RING_IP: ip, RING_JRM: jrm, RING_JA: ja}})


@pytest.fixture
def provider(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "claude")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_MODEL", "test-model-id")


def _respond(monkeypatch, fn):
    monkeypatch.setattr(classify_mod, "_call_anthropic", fn)


# =============================================================================
# The prompt
# =============================================================================
def test_the_triage_prompt_is_compact_and_carries_no_few_shots():
    """~2,000 characters is the spec, and the economics are the reason.

    This prompt runs once per CANDIDATE, not once per enriched item, so its
    length is multiplied by the whole run. The tooling header is excluded from
    the count because `#` lines are documentation for us; they are still sent,
    which is why the whole file is bounded too.
    """
    template = triage.load_triage_prompt()
    body = "\n".join(ln for ln in template.splitlines()
                     if not ln.startswith("#")).strip()
    assert len(body) < 2800, f"the triage prompt body has grown to {len(body)}"
    assert len(template) < 3600, f"the whole triage file is {len(template)}"
    # Checked against the BODY, not the header: the header names these things
    # in order to forbid them, and a test that could not tell the prohibition
    # from the violation would forbid writing the prohibition down.
    lowered = body.lower()
    for banned in ("example 1", "few-shot", "digest_summary", "notable_quote",
                   "relevance_score", "evidence_span"):
        assert banned not in lowered, f"{banned} has crept into the triage prompt"


def test_the_triage_prompt_reads_a_title_and_a_summary_and_no_body():
    template = triage.load_triage_prompt()
    assert template.count("{{TITLE}}") == 1
    assert template.count("{{SUMMARY}}") == 1
    assert "{{TEXT}}" not in template, \
        "triage must never be handed a body: it runs before enrichment"


def test_the_built_prompt_never_reads_raw_text():
    """Five sources set raw_text = title and three set it = summary. Reading it
    would make the triage question quietly different per source."""
    item = _item("italaw", "1", "A title", summary="A summary",
                 body="A BODY THAT MUST NOT BE SENT")
    prompt = triage.build_triage_prompt(item)
    assert "A title" in prompt and "A summary" in prompt
    assert "A BODY THAT MUST NOT BE SENT" not in prompt


# =============================================================================
# The parser
# =============================================================================
def test_a_well_formed_triage_answer_parses():
    parsed = triage.parse_triage_response(_reply("strong", "weak", "absent"))
    assert parsed == {RING_IP: Strength.STRONG, RING_JRM: Strength.WEAK,
                      RING_JA: Strength.ABSENT}


@pytest.mark.parametrize("payload", [
    "", "not json", '{"rings": {}}', '{"rings": {"ip_as_investment": "strong"}}',
    json.dumps({"rings": {RING_IP: "medium", RING_JRM: "weak", RING_JA: "absent"}}),
])
def test_the_triage_parser_rejects_anything_outside_the_grammar(payload):
    assert triage.parse_triage_response(payload) is None


# =============================================================================
# The rank
# =============================================================================
def test_the_rank_puts_ip_first_and_treats_the_other_two_as_interchangeable():
    """The shape is the MATCH rule's, not a weighting chosen by feel."""
    def r(ip, jrm, ja):
        return triage.semantic_rank({RING_IP: ip, RING_JRM: jrm, RING_JA: ja})

    A, W, P, S = Strength.ABSENT, Strength.WEAK, Strength.PRESENT, Strength.STRONG
    # IP dominates: any IP strength beats any amount of the other two.
    assert r(W, A, A) > r(A, S, S)
    # The other two are symmetric with each other.
    assert r(P, S, W) == r(P, W, S)
    # Ordered, and bounded.
    assert r(A, A, A) == 0 and r(S, S, S) == 63
    assert r(S, S, S) > r(P, S, S) > r(W, S, S) > r(A, S, S)


def test_a_missing_triage_result_ranks_as_absent_on_all_three():
    assert triage.semantic_rank(None) == 0
    assert triage.semantic_rank({}) == 0


def test_the_sort_key_is_total_and_is_a_function_only_of_the_candidate():
    a = _item("italaw", "b", "T")
    b = _item("italaw", "a", "T")
    lexical = {"per_ring_subtotal": {RING_IP: 10}}
    ka = triage.triage_sort_key(a, lexical_result=lexical, strengths=None)
    kb = triage.triage_sort_key(b, lexical_result=lexical, strengths=None)
    assert ka != kb and kb < ka, "identical items must still order by source_id"
    # Same inputs, same key, every time.
    assert ka == triage.triage_sort_key(a, lexical_result=lexical, strengths=None)


def test_with_no_triage_results_the_order_collapses_to_the_lexical_one():
    """The property that makes a total provider outage safe.

    Every semantic_rank is 0, so the first key component is constant and the
    sort reduces to (-lexical_subtotal, source, source_id). Ranking falls back
    to lexical exactly, rather than being scrambled by partial data.
    """
    items = [_item("italaw", f"i{i}", f"T{i}") for i in range(5)]
    lex = {id(it): {"per_ring_subtotal": {RING_IP: n}}
           for it, n in zip(items, (5, 30, 0, 12, 30))}
    ranked = sorted(items, key=lambda it: triage.triage_sort_key(
        it, lexical_result=lex[id(it)], strengths=None))
    subtotals = [triage.lexical_subtotal(lex[id(it)]) for it in ranked]
    assert subtotals == sorted(subtotals, reverse=True)
    # Ties broken by source_id, deterministically.
    assert [it.source_id for it in ranked[:2]] == ["i1", "i4"]


# =============================================================================
# The adversarial cases
# =============================================================================
def test_the_paraphrase_heavy_probe_is_invisible_to_the_lexicon():
    """The premise of the whole workstream, verified against the real probe."""
    item = _probe_item("E5_einarsson_lexical_brittle")
    lexical = keyword_score(item)
    assert lexical["relevance_score"] == 0
    assert lexical["per_ring_subtotal"] == {}
    assert PROBE["E5_einarsson_lexical_brittle"]["expected_band"] == "HIGH"


def test_a_paraphrase_heavy_item_is_triage_ranked_into_enrichment(provider,
                                                                  monkeypatch):
    """E5 scores 0 lexically. With triage on it must clear the enrichment cut.

    The competition is deliberately unfair to E5: twenty filler candidates that
    all out-score it lexically. Under lexical ranking with a budget of 3 it is
    21st and never read. Triage rates its IP ring strong and it comes first.
    """
    target = _probe_item("E5_einarsson_lexical_brittle")
    fillers = [_item("bing_news", f"f{i}", f"Trademark dispute {i}",
                     summary="A trademark and patent licence dispute.")
               for i in range(20)]
    candidates = fillers + [target]
    lex = {id(it): keyword_score(it) for it in candidates}
    assert lex[id(target)]["relevance_score"] == 0
    assert all(lex[id(f)]["relevance_score"] > 0 for f in fillers)

    def responder(prompt):
        # The model sees the paraphrase the lexicon cannot. Keyed on a token
        # from the probe that the PROMPT TEMPLATE does not itself contain —
        # "regulatory data" would match every prompt, because it is one of the
        # ring definitions.
        if "biosimilars" in prompt:
            return _reply("strong", "present", "present")
        return _reply("weak", "absent", "absent")

    _respond(monkeypatch, responder)
    results = {id(it): triage.triage_item(it) for it in candidates}
    assert all(r.ran for r in results.values())

    ranked = sorted(candidates, key=lambda it: triage.triage_sort_key(
        it, lexical_result=lex[id(it)],
        strengths=results[id(it)].strengths))
    assert ranked[0] is target, "the paraphrase-heavy item still did not surface"
    assert target in ranked[:3], "it must clear an enrichment budget of 3"

    # And without triage it is dead last but one — the counterfactual.
    lexical_order = sorted(candidates,
                           key=lambda it: lex[id(it)]["relevance_score"],
                           reverse=True)
    assert lexical_order[-1] is target


def test_the_domestic_trade_secret_comparator_is_not_promoted_by_triage(provider,
                                                                        monkeypatch):
    """Triage reorders a reading queue; it must not manufacture relevance.

    N2 is a domestic trade-secret suit with no state measure and no treaty
    nexus. A triage pass that rated it highly would push a comparator into the
    enrichment budget ahead of real ISDS material — and the nexus test that
    catches it downstream cannot run on an item that was never read.
    """
    item = _probe_item("N2_domestic_trade_secret_suit", source="bing_news")
    _respond(monkeypatch, lambda p: _reply("weak", "absent", "absent"))
    result = triage.triage_item(item)
    assert result.ran
    assert result.strengths[RING_IP] is Strength.WEAK
    assert result.rank == triage.semantic_rank(
        {RING_IP: Strength.WEAK, RING_JRM: Strength.ABSENT,
         RING_JA: Strength.ABSENT})
    # Below anything with a present IP ring, whatever its lexical score.
    assert result.rank < triage.semantic_rank(
        {RING_IP: Strength.PRESENT, RING_JRM: Strength.ABSENT,
         RING_JA: Strength.ABSENT})


def test_a_single_judicial_ring_isds_item_ranks_below_any_ip_item(provider,
                                                                  monkeypatch):
    """N4: a real ISDS matter with no IP. Interesting, and not the question."""
    item = _probe_item("N4_investment_dispute_no_ip", source="unctad_isds")
    _respond(monkeypatch, lambda p: _reply("absent", "strong", "weak"))
    result = triage.triage_item(item)
    assert result.ran
    assert result.rank < triage.semantic_rank(
        {RING_IP: Strength.WEAK, RING_JRM: Strength.ABSENT,
         RING_JA: Strength.ABSENT}), \
        "a judicial ring without IP outranked a brushed IP ring"


def test_a_provider_failure_mid_triage_is_recorded_and_the_run_completes(
        provider, monkeypatch):
    """Half the pass fails. Nothing crashes, nothing is misreported."""
    items = [_item("italaw", f"i{i}", f"Title {i}", summary="s") for i in range(6)]
    calls = {"n": 0}

    def flaky(prompt):
        calls["n"] += 1
        if calls["n"] > 3:
            raise RuntimeError("provider went away")
        return _reply("present", "absent", "absent")

    _respond(monkeypatch, flaky)
    results = [triage.triage_item(it) for it in items]

    assert [r.ran for r in results] == [True, True, True, False, False, False]
    for r in results[3:]:
        assert r.basis == triage.TRIAGE_BASIS_PROVIDER_ERROR
        assert not triage.basis_names_a_model(r.basis)
        assert r.rank == 0, "a failed triage must not invent a rank"
        assert r.strengths == {}
    # The skip is recorded as a named skip, never as an absence.
    sections = [triage.telemetry_section(r) for r in results]
    assert sections[4]["ran"] is False
    assert sections[4]["basis"] == "skipped_provider_error"
    assert sections[4]["strengths"] == {}


def test_a_malformed_triage_answer_skips_that_item_only(provider, monkeypatch):
    items = [_item("italaw", f"i{i}", f"Title {i}", summary="s") for i in range(3)]

    def responder(prompt):
        return "I think this one is quite relevant!" if "Title 1" in prompt \
            else _reply("present", "weak", "absent")

    _respond(monkeypatch, responder)
    results = [triage.triage_item(it) for it in items]
    assert [r.ran for r in results] == [True, False, True]
    assert results[1].basis == triage.TRIAGE_BASIS_MALFORMED
    assert results[1].rank == 0
    # Distinct from a provider failure: the provider answered.
    assert results[1].basis != triage.TRIAGE_BASIS_PROVIDER_ERROR
    assert results[1].outcome.value == "parse_failed"


def test_triage_does_not_retry_a_malformed_answer(provider, monkeypatch):
    """One call per candidate. A retry doubles the cost of the whole pass to
    salvage a ranking hint whose absence costs the item nothing."""
    calls = []
    _respond(monkeypatch, lambda p: calls.append(p) or "nonsense")
    result = triage.triage_item(_item("italaw", "1", "T", summary="s"))
    assert len(calls) == 1
    assert result.attempts == 1 and not result.ran


def test_no_provider_means_triage_is_skipped_and_says_so(monkeypatch):
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = triage.triage_item(_item("italaw", "1", "T", summary="s"))
    assert not result.ran
    assert result.basis == triage.TRIAGE_BASIS_NO_PROVIDER
    assert not triage.basis_names_a_model(result.basis)
    assert result.rank == 0


def test_only_a_parsed_answer_names_a_model_in_the_triage_basis(provider,
                                                                monkeypatch):
    for reply, expected in ((_reply("weak"), True),
                            ("nonsense", False),
                            (RuntimeError("down"), False)):
        def responder(p, _r=reply):
            if isinstance(_r, Exception):
                raise _r
            return _r
        _respond(monkeypatch, responder)
        result = triage.triage_item(_item("italaw", "1", "T", summary="s"))
        assert triage.basis_names_a_model(result.basis) is expected


# =============================================================================
# The flags
# =============================================================================
def test_triage_is_off_by_default():
    assert config.TRIAGE_ENABLED is False


def test_the_tail_audit_is_a_documented_stub_and_runs_nothing():
    assert config.TAIL_AUDIT_N == 0
