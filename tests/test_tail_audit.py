"""The stratified tail audit — its boundaries, its draw, and its ledger.

The audit measures a FLIP, not a truth: whether the instrument says something
different about one item when it is given a body. These tests are about the
properties that make such a measurement worth reading at all — that the strata
are where the ruling put them, that the draw is a function of the candidate set
and a recorded seed, that a short stratum is reported short rather than padded,
and above all that the cross-run ledger never lets the same item be measured
twice. A flip rate computed over a file that re-audits its favourites is not a
rate.
"""

import json

import pytest

from src import config, tail_audit
from src.classify import PRESENT_FLOOR, ClassifyOutcome, OUTCOME_KEY


# --------------------------------------------------------------------------- #
# Stand-ins
# --------------------------------------------------------------------------- #
class _Item:
    def __init__(self, sid, source="iisd_itn"):
        self.source = source
        self.source_id = sid
        self.title = f"title {sid}"
        self.raw_text = ""
        self.metadata = {}


class _Classified:
    def __init__(self, score, outcome=ClassifyOutcome.OK.value):
        self.relevance_score = score
        self.metadata = {OUTCOME_KEY: outcome}


def _cand(sid, subtotal, score=10, outcome=ClassifyOutcome.OK.value):
    return tail_audit.tail_candidate(
        _Item(sid), lexical_subtotal=subtotal,
        classified=_Classified(score), outcome=outcome)


# --------------------------------------------------------------------------- #
# The strata
# --------------------------------------------------------------------------- #
def test_the_stratum_boundaries_are_zero_and_the_present_floor():
    """The ruling's boundaries, at the values where they actually decide."""
    assert PRESENT_FLOOR == 12, \
        "the audit stratifies on the scorer's own floor; this test pins the pair"
    assert tail_audit.stratum_of(0) == tail_audit.STRATUM_A
    assert tail_audit.stratum_of(1) == tail_audit.STRATUM_B
    assert tail_audit.stratum_of(11) == tail_audit.STRATUM_B
    assert tail_audit.stratum_of(12) == tail_audit.STRATUM_C
    assert tail_audit.stratum_of(13) == tail_audit.STRATUM_C


def test_a_missing_or_negative_subtotal_is_stratum_a_not_a_fourth_case():
    assert tail_audit.stratum_of(None) == tail_audit.STRATUM_A
    assert tail_audit.stratum_of(-3) == tail_audit.STRATUM_A


def test_the_per_stratum_draw_is_derived_from_the_configured_total():
    """6 in total and 2 per stratum must not be two numbers that can drift."""
    assert config.TAIL_AUDIT_N == 6
    assert tail_audit.per_stratum_n() == 2
    assert tail_audit.per_stratum_n(0) == 0
    assert tail_audit.per_stratum_n(3) == 1


def test_the_bands_come_from_fingerprint_yaml_not_from_a_literal_here():
    assert tail_audit.band_of(70) == "HIGH"
    assert tail_audit.band_of(69) == "MEDIUM"
    assert tail_audit.band_of(40) == "MEDIUM"
    assert tail_audit.band_of(39) == "LOW"
    assert tail_audit.band_of(0) == "LOW"


# --------------------------------------------------------------------------- #
# The draw
# --------------------------------------------------------------------------- #
def test_two_are_drawn_from_each_stratum_under_the_seed():
    pool = ([_cand(f"a{i}", 0) for i in range(5)]
            + [_cand(f"b{i}", 6) for i in range(5)]
            + [_cand(f"c{i}", 30) for i in range(5)])
    chosen, shortfalls = tail_audit.select_sample(pool, seed="run-1")
    assert shortfalls == {}
    for stratum in tail_audit.STRATA:
        assert len(chosen[stratum]) == 2
        assert {c.stratum for c in chosen[stratum]} == {stratum}


def test_the_draw_is_a_function_of_the_seed_and_not_of_fetch_order():
    pool = [_cand(f"a{i}", 0) for i in range(8)]
    forward, _ = tail_audit.select_sample(pool, seed="run-1")
    backward, _ = tail_audit.select_sample(list(reversed(pool)), seed="run-1")
    assert ([c.item_id for c in forward[tail_audit.STRATUM_A]]
            == [c.item_id for c in backward[tail_audit.STRATUM_A]])
    other, _ = tail_audit.select_sample(pool, seed="run-2")
    assert ([c.item_id for c in other[tail_audit.STRATUM_A]]
            != [c.item_id for c in forward[tail_audit.STRATUM_A]]), \
        "two different runs drew the identical sample; the seed is not reaching " \
        "the draw"


def test_a_short_stratum_takes_what_exists_and_the_shortfall_is_recorded():
    """Neither refusing to run nor pretending it drew two."""
    pool = [_cand("a0", 0), _cand("b0", 5), _cand("b1", 5), _cand("c0", 20)]
    chosen, shortfalls = tail_audit.select_sample(pool, seed="run-1")
    assert len(chosen[tail_audit.STRATUM_A]) == 1
    assert len(chosen[tail_audit.STRATUM_B]) == 2
    assert len(chosen[tail_audit.STRATUM_C]) == 1
    assert shortfalls == {tail_audit.STRATUM_A: 1, tail_audit.STRATUM_C: 1}


def test_an_empty_stratum_is_a_shortfall_of_the_whole_draw():
    chosen, shortfalls = tail_audit.select_sample([_cand("a0", 0), _cand("a1", 0)],
                                                  seed="run-1")
    assert chosen[tail_audit.STRATUM_B] == []
    assert shortfalls[tail_audit.STRATUM_B] == 2
    assert shortfalls[tail_audit.STRATUM_C] == 2


# --------------------------------------------------------------------------- #
# The audit
# --------------------------------------------------------------------------- #
def _enrich(item):
    item.raw_text = "a fetched body"
    item.metadata = {**(item.metadata or {}), "enriched": True}
    return item


def test_a_pair_records_both_bands_and_the_delta(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    pool = [_cand("a0", 0, score=10)]
    result = tail_audit.run_audit(
        pool, run_id="2026-09-13-abc", enrich=_enrich,
        classify=lambda item: _Classified(75), per_stratum=1)
    assert result.calls == 1
    assert len(result.rows) == 1
    row = result.rows[0]
    assert set(row) == set(tail_audit.LEDGER_FIELDS)
    assert row["band_unenriched"] == "LOW"
    assert row["band_enriched"] == "HIGH"
    assert row["score_delta"] == 65
    assert row["stratum"] == tail_audit.STRATUM_A
    assert row["seed"] == "2026-09-13-abc"
    assert row["run_id"] == "2026-09-13-abc"


def test_the_ledger_row_carries_no_candidate_text_of_any_kind(tmp_path,
                                                              monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = tail_audit.run_audit(
        [_cand("a0", 0)], run_id="r1", enrich=_enrich,
        classify=lambda item: _Classified(50), per_stratum=1)
    blob = json.dumps(result.rows)
    assert "title" not in blob
    assert "a fetched body" not in blob
    # The item is named by the same hash the telemetry uses, never by its id.
    from src.telemetry import candidate_id
    assert result.rows[0]["item_id"] == candidate_id("iisd_itn", "a0")
    assert "a0" not in result.rows[0]["item_id"].split(":")[1]


@pytest.mark.parametrize("unenriched,enriched", [
    (ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR.value, ClassifyOutcome.OK.value),
    (ClassifyOutcome.OK.value, ClassifyOutcome.KEYWORD_AFTER_PROVIDER_ERROR.value),
    (ClassifyOutcome.OK.value, ClassifyOutcome.KEYWORD_ONLY_BY_DESIGN.value),
])
def test_a_pair_that_is_half_keyword_score_is_not_recorded_as_a_flip(
        tmp_path, monkeypatch, unenriched, enriched):
    """The precondition the ruling attached to the audit.

    A flip between a model reading and a lexicon reading measures the outage,
    not the enrichment cut. The item is left unaudited — it stays in the pool
    for a later run — and counted, so the absence is visible.
    """
    monkeypatch.chdir(tmp_path)
    result = tail_audit.run_audit(
        [_cand("a0", 0, outcome=unenriched)], run_id="r1", enrich=_enrich,
        classify=lambda item: _Classified(90, outcome=enriched), per_stratum=1)
    assert result.rows == []
    assert result.skipped_not_measurable == 1
    assert result.calls == 1, "the call was still made and must still be priced"


def test_a_raising_classifier_never_takes_the_run_down(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def boom(item):
        raise RuntimeError("provider down")

    result = tail_audit.run_audit([_cand("a0", 0)], run_id="r1", enrich=_enrich,
                                  classify=boom, per_stratum=1)
    assert result.rows == []
    assert result.skipped_not_measurable == 1


# --------------------------------------------------------------------------- #
# The cross-run ledger
# --------------------------------------------------------------------------- #
def test_no_item_is_audited_twice_across_runs(tmp_path, monkeypatch):
    """The property the whole cross-run ledger exists for."""
    monkeypatch.chdir(tmp_path)
    pool = [_cand(f"a{i}", 0) for i in range(4)]

    first = tail_audit.run_audit(pool, run_id="r1", enrich=_enrich,
                                 classify=lambda item: _Classified(50),
                                 per_stratum=2)
    tail_audit.append_rows(first.rows)
    assert len(first.rows) == 2

    ledger = tail_audit.read_ledger()
    second = tail_audit.run_audit(
        pool, run_id="r2", enrich=_enrich,
        classify=lambda item: _Classified(50), per_stratum=2,
        already_audited=tail_audit.audited_item_ids(ledger))
    tail_audit.append_rows(second.rows)

    audited_first = {r["item_id"] for r in first.rows}
    audited_second = {r["item_id"] for r in second.rows}
    assert audited_first & audited_second == set(), \
        "an item was audited in two runs; a flip rate over this file is not a rate"

    all_rows = tail_audit.read_ledger()
    assert len(all_rows) == 4
    ids = [r["item_id"] for r in all_rows]
    assert len(ids) == len(set(ids))

    # The pool is exhausted: a third run has nothing left to draw and says so.
    third = tail_audit.run_audit(
        pool, run_id="r3", enrich=_enrich,
        classify=lambda item: _Classified(50), per_stratum=2,
        already_audited=tail_audit.audited_item_ids(tail_audit.read_ledger()))
    assert third.rows == []
    assert third.calls == 0
    assert third.shortfalls[tail_audit.STRATUM_A] == 2


def test_the_ledger_is_append_only(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tail_audit.append_rows([{"run_id": "r1", "item_id": "x"}])
    tail_audit.append_rows([{"run_id": "r2", "item_id": "y"}])
    rows = tail_audit.read_ledger()
    assert [r["run_id"] for r in rows] == ["r1", "r2"], \
        "the second write replaced the first instead of appending to it"


def test_a_corrupt_ledger_line_is_skipped_not_fatal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tail_audit.append_rows([{"run_id": "r1", "item_id": "x"}])
    with open(tail_audit.LEDGER_PATH, "a", encoding="utf-8") as fh:
        fh.write("{not json\n")
    assert len(tail_audit.read_ledger()) == 1


# --------------------------------------------------------------------------- #
# The privacy guard covers the new stream
# --------------------------------------------------------------------------- #
def _guard():
    import importlib
    import os
    import sys

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    return importlib.import_module("check_telemetry_privacy")


def test_the_privacy_guard_passes_a_well_formed_ledger(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = tail_audit.run_audit([_cand("a0", 0)], run_id="r1", enrich=_enrich,
                                  classify=lambda item: _Classified(50),
                                  per_stratum=1)
    tail_audit.append_rows(result.rows)
    assert _guard().main(["check_telemetry_privacy",
                          "--path", "nonexistent.jsonl",
                          "--tail-audit-path", tail_audit.LEDGER_PATH]) == 0


@pytest.mark.parametrize("planted,why", [
    ({"title": "Patent invalidated by the Federal Court"}, "a forbidden field"),
    ({"note": "x" * 400}, "an over-long string"),
    ({"context": "a short but undeclared extra"}, "an undeclared field"),
])
def test_the_privacy_guard_fails_a_ledger_carrying_anything_extra(
        tmp_path, monkeypatch, planted, why):
    """The guard's own test: a planted violation must fail the build."""
    monkeypatch.chdir(tmp_path)
    row = {f: "" for f in tail_audit.LEDGER_FIELDS}
    row.update(planted)
    tail_audit.append_rows([row])
    assert _guard().main(["check_telemetry_privacy",
                          "--path", "nonexistent.jsonl",
                          "--tail-audit-path", tail_audit.LEDGER_PATH]) == 1, why


def test_the_privacy_guard_fails_a_ledger_row_missing_a_declared_field(
        tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    row = {f: "" for f in tail_audit.LEDGER_FIELDS}
    row.pop("band_enriched")
    tail_audit.append_rows([row])
    assert _guard().main(["check_telemetry_privacy",
                          "--path", "nonexistent.jsonl",
                          "--tail-audit-path", tail_audit.LEDGER_PATH]) == 1


def test_the_guard_covers_the_ledger_with_no_arguments_at_all(capsys):
    """A guard nobody has to remember to point at the new file.

    This is the invocation CI actually runs (`python
    scripts/check_telemetry_privacy.py`, no flags) against the real repository.
    A new stream that only gets checked when someone passes a flag is not
    covered; it is discoverable.
    """
    guard = _guard()
    assert guard.main(["check_telemetry_privacy"]) == 0
    out = capsys.readouterr().out
    assert "tail_audit.jsonl" in out, \
        "the default invocation never looked at the tail-audit ledger"
    assert "candidate_telemetry.jsonl" in out, \
        "covering the new stream must not have stopped covering the old one"


# --------------------------------------------------------------------------- #
# The reporting surface
# --------------------------------------------------------------------------- #
def test_the_only_reporting_surface_reads_the_ledger(tmp_path, monkeypatch,
                                                     capsys):
    import importlib
    import os
    import sys

    monkeypatch.chdir(tmp_path)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    query = importlib.import_module("telemetry_query")

    rows = [
        {"run_id": "r1", "item_id": "i1", "source": "s", "seed": "r1",
         "stratum": tail_audit.STRATUM_A, "lexical_subtotal": 0,
         "band_unenriched": "LOW", "band_enriched": "HIGH", "score_delta": 65},
        {"run_id": "r1", "item_id": "i2", "source": "s", "seed": "r1",
         "stratum": tail_audit.STRATUM_A, "lexical_subtotal": 0,
         "band_unenriched": "LOW", "band_enriched": "LOW", "score_delta": 2},
        {"run_id": "r1", "item_id": "i3", "source": "s", "seed": "r1",
         "stratum": tail_audit.STRATUM_C, "lexical_subtotal": 30,
         "band_unenriched": "MEDIUM", "band_enriched": "LOW", "score_delta": -8},
    ]
    tail_audit.append_rows(rows)

    assert query.main(["telemetry_query", "--tail-audit",
                       "--tail-audit-path", tail_audit.LEDGER_PATH]) == 0
    out = capsys.readouterr().out
    assert "3 tail-audit pairs" in out
    assert "TOTAL" in out
    # The disclaimer is part of the output, not an optional footnote.
    assert "NOT evidence that either reading was correct" in out
