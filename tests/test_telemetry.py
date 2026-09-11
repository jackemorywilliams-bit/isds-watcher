"""Tests for the per-candidate run telemetry and its privacy guard.

The four properties that matter here are the ones the rest of the system will
quietly assume: the record has the shape it claims, the same input writes the
same bytes, a candidate appears exactly once per run, and candidate TEXT can
never reach the file without the build failing.
"""

import datetime
import importlib
import json
import os
import sys

from src import telemetry
from src.sources.base import CandidateItem

UTC = datetime.timezone.utc

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
privacy_guard = importlib.import_module("check_telemetry_privacy")

# A fixed instant: the telemetry must not read the clock, and a test that passed
# a `now()` would not be able to tell whether it did.
FIXED = datetime.datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def _item(source="italaw", sid="http://x/1", title="Case A", summary="s",
          raw="body text"):
    return CandidateItem(source, sid, "https://italaw.com/cases/1", title,
                         FIXED, summary, raw, {})


def _fully_annotated(run_date="2026-08-01", items=None):
    """A RunTelemetry with every annotation applied — the shape a real run writes."""
    tel = telemetry.RunTelemetry(run_date)
    for i, it in enumerate(items or [_item()]):
        cid = tel.observe(it)
        tel.note_access(cid, it, headline_only=False, body_fetched=True,
                        fetch_outcome="ok")
        tel.note_lexical(cid, per_ring_subtotal={"ip_as_investment": 14},
                         hits=["patent", "abuse_of_right"], negative_signal=False,
                         rank=i)
        tel.note_enrichment(cid, True)
        tel.note_classification(cid, ran=True, path="llm",
                                model="claude-haiku-4-5-20251001",
                                prompt_version="abc123def456", outcome="ok",
                                attempts=1, retried_strict=False,
                                model_score_advisory=None)
        tel.note_surfacing(cid, surfaced=True, reason="at_or_above_threshold",
                           digest="digests/2026-08-01_ISDS-Thematic-Watch", position=i)
        tel.note_dedup(cid, seen_before=False, marked_seen=True, deferred=False,
                       abandoned=False)
    return tel


# --- schema conformance ------------------------------------------------------
def test_record_carries_the_whole_declared_schema(tmp_path):
    path = str(tmp_path / "t.jsonl")
    assert _fully_annotated().flush(path) == 1
    rec = json.loads(open(path, encoding="utf-8").read().strip())

    # 3 since `triage` and `v2_call` were added and `verdict_v2` widened with the
    # fields that say what produced it. Records written at 1 or 2 are still valid
    # and simply carry less.
    assert rec["schema"] == telemetry.SCHEMA == 3
    for key in ("run_id", "run_date", "candidate_id", "source", "source_id_hash",
                "url_host", "url_hash", "published", "access", "lexical",
                "triage", "v2_call", "entered_enrichment", "classification",
                "surfacing", "dedup", "verdict_v2"):
        assert key in rec, f"missing top-level field {key}"

    assert set(rec["access"]) == {
        "headline_only", "body_fetched", "fetch_outcome", "text_len_title",
        "text_len_summary", "text_len_body", "title_sha256", "body_sha256"}
    assert set(rec["lexical"]) == {
        "per_ring_subtotal", "hits", "negative_signal", "rank"}
    assert set(rec["classification"]) == {
        "ran", "path", "model", "prompt_version", "outcome", "attempts",
        "retried_strict", "model_score_advisory"}
    assert set(rec["surfacing"]) == {"surfaced", "reason", "digest", "position"}
    assert set(rec["dedup"]) == {"seen_before", "marked_seen", "deferred", "abandoned"}
    assert set(rec["triage"]) == {
        "ran", "basis", "model", "prompt_version", "outcome", "attempts",
        "semantic_rank", "strengths"}
    assert set(rec["v2_call"]) == {
        "mode", "called", "basis", "model", "prompt_version", "outcome",
        "attempts", "retried_strict", "model_nexus_advisory"}
    assert set(rec["verdict_v2"]) == {
        "mode", "derived", "lane", "lane_reason", "public_label", "nexus",
        "evidence_location", "evidence_validity", "path",
        "classification_state", "classification_outcome", "guard_demoted",
        "v2_basis", "claims_source", "model_score_advisory", "rings"}
    # A record that did not run either optional pass says so, in the vocabulary
    # of each pass, and names no model anywhere.
    assert rec["triage"]["ran"] is False and rec["triage"]["basis"] == "not_run"
    assert rec["v2_call"]["called"] is False
    assert rec["verdict_v2"]["v2_basis"] == "lexical_only"
    assert rec["verdict_v2"]["claims_source"] == "none"
    # Never present, at any mode: the span itself is candidate text. Its length
    # and sha256 are, and are named so as not to collide with this check.
    assert '"evidence_span"' not in json.dumps(rec)

    # candidate_id is source-qualified and the source_id itself is hashed away.
    assert rec["candidate_id"].startswith("italaw:")
    assert "http://x/1" not in json.dumps(rec)
    assert rec["source_id_hash"] == telemetry.sha256_hex("http://x/1")
    # Lengths and hashes stand in for the text; the text is nowhere.
    assert rec["access"]["text_len_body"] == len("body text")
    assert rec["access"]["body_sha256"] == telemetry.sha256_hex("body text")
    assert "body text" not in json.dumps(rec)
    assert "Case A" not in json.dumps(rec)


def test_blank_record_has_every_field_before_any_annotation(tmp_path):
    # An unannotated candidate still writes a complete record: "we did not do
    # that" and "the field is missing" must not be the same thing to a query.
    tel = telemetry.RunTelemetry("2026-08-01")
    tel.observe(_item())
    path = str(tmp_path / "t.jsonl")
    tel.flush(path)
    rec = json.loads(open(path, encoding="utf-8").read().strip())
    assert rec["classification"]["ran"] is False
    assert rec["classification"]["outcome"] == ""
    assert rec["lexical"]["rank"] == -1
    assert rec["dedup"]["marked_seen"] is False
    assert rec["surfacing"]["reason"] == "not_selected"


# --- determinism -------------------------------------------------------------
def test_identical_input_writes_identical_bytes(tmp_path):
    a, b = str(tmp_path / "a.jsonl"), str(tmp_path / "b.jsonl")
    items = [_item(sid=f"http://x/{i}", title=f"Case {i}") for i in range(5)]
    _fully_annotated(items=items).flush(a)
    _fully_annotated(items=items).flush(b)
    assert open(a, "rb").read() == open(b, "rb").read()
    assert open(a, "rb").read()  # and it is not trivially empty


def test_output_order_does_not_depend_on_intake_order(tmp_path):
    # Fetch order varies run to run; the bytes must not.
    items = [_item(sid=f"http://x/{i}", title=f"Case {i}") for i in range(5)]
    a, b = str(tmp_path / "a.jsonl"), str(tmp_path / "b.jsonl")
    _fully_annotated(items=items).flush(a)
    _fully_annotated(items=list(reversed(items))).flush(b)
    # The rank annotation is positional, so strip it before comparing: what is
    # being asserted is that the SET of records and their ORDER on disk are
    # stable, not that a reversed run scores the same.
    def _ranks_stripped(p):
        out = []
        for line in open(p, encoding="utf-8"):
            rec = json.loads(line)
            rec["lexical"]["rank"] = 0
            rec["surfacing"]["position"] = 0
            out.append(json.dumps(rec, sort_keys=True))
        return out
    assert _ranks_stripped(a) == _ranks_stripped(b)


def test_run_id_is_the_date_plus_the_candidate_set(tmp_path):
    items = [_item(sid="a"), _item(sid="b")]
    rid = _fully_annotated(items=items).records()[0]["run_id"]
    assert rid.startswith("2026-08-01-")
    # Same date, same candidates -> same run_id.
    assert _fully_annotated(items=list(reversed(items))).records()[0]["run_id"] == rid
    # A different candidate set is a different run.
    assert _fully_annotated(items=[_item(sid="a")]).records()[0]["run_id"] != rid
    # So is a different date.
    assert _fully_annotated(run_date="2026-08-02",
                            items=items).records()[0]["run_id"] != rid


# --- one record per candidate per run ----------------------------------------
def test_exactly_one_record_per_candidate_per_run(tmp_path):
    tel = telemetry.RunTelemetry("2026-08-01")
    it = _item()
    first = tel.observe(it)
    # Observed again mid-run (the pipeline touches a candidate at several stages)
    # and observed again as a distinct object with the same identity.
    assert tel.observe(it) == first
    assert tel.observe(_item()) == first
    tel.observe(_item(sid="http://x/2"))
    assert len(tel) == 2

    path = str(tmp_path / "t.jsonl")
    assert tel.flush(path) == 2
    lines = [ln for ln in open(path, encoding="utf-8").read().splitlines() if ln]
    assert len(lines) == 2
    assert len({json.loads(ln)["candidate_id"] for ln in lines}) == 2


def test_flush_refuses_to_write_twice(tmp_path):
    path = str(tmp_path / "t.jsonl")
    tel = _fully_annotated()
    assert tel.flush(path) == 1
    assert tel.flush(path) == 0
    assert len([ln for ln in open(path, encoding="utf-8").read().splitlines() if ln]) == 1


def test_flush_appends_across_runs(tmp_path):
    path = str(tmp_path / "t.jsonl")
    _fully_annotated(run_date="2026-08-01").flush(path)
    _fully_annotated(run_date="2026-08-02").flush(path)
    recs = telemetry.load_records(path)
    assert len(recs) == 2
    assert {r["run_date"] for r in recs} == {"2026-08-01", "2026-08-02"}
    # Same candidate, two runs, two records — the invariant is per RUN.
    assert len({r["candidate_id"] for r in recs}) == 1


# --- the privacy guard -------------------------------------------------------
def _run_guard(path):
    return privacy_guard.main(["check_telemetry_privacy", "--path", str(path)])


def test_privacy_guard_passes_a_real_record(tmp_path):
    path = tmp_path / "t.jsonl"
    _fully_annotated(items=[_item(sid=f"x{i}") for i in range(3)]).flush(str(path))
    assert _run_guard(path) == 0


def test_privacy_guard_fails_on_a_planted_text_field(tmp_path):
    # The exact defect it exists for: someone attaches the item's text.
    for planted in ("title", "summary", "body", "raw_text"):
        path = tmp_path / f"{planted}.jsonl"
        tel = _fully_annotated()
        rec = tel.records()[0]
        rec[planted] = "The tribunal found the measure arbitrary."
        path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
        assert _run_guard(path) == 1, f"guard passed a planted `{planted}` field"


def test_privacy_guard_fails_on_text_nested_deep(tmp_path):
    path = tmp_path / "t.jsonl"
    rec = _fully_annotated().records()[0]
    rec["access"]["title"] = "Telefónica v. Colombia"
    path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    assert _run_guard(path) == 1


def test_privacy_guard_does_not_fail_the_legitimate_lookalike_fields(tmp_path):
    # text_len_title / title_sha256 / body_sha256 are how a title and a body are
    # SUPPOSED to be described. A substring match would break the whole design.
    path = tmp_path / "t.jsonl"
    _fully_annotated().flush(str(path))
    text = path.read_text(encoding="utf-8")
    assert "title_sha256" in text and "text_len_body" in text
    assert _run_guard(path) == 0


def test_privacy_guard_fails_on_an_over_long_string_under_a_new_name(tmp_path):
    # Text smuggled under a field name the first check has never heard of.
    path = tmp_path / "t.jsonl"
    rec = _fully_annotated().records()[0]
    rec["classification"]["context"] = "x" * (telemetry.MAX_STRING_LEN + 1)
    path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    assert _run_guard(path) == 1

    # ...but a long value in an allowlisted hash/id field is fine.
    ok = tmp_path / "ok.jsonl"
    rec2 = _fully_annotated().records()[0]
    rec2["classification"]["context"] = "x" * telemetry.MAX_STRING_LEN
    ok.write_text(json.dumps(rec2) + "\n", encoding="utf-8")
    assert _run_guard(ok) == 0


def test_privacy_guard_fails_on_an_excerpt_from_a_headline_only_source(tmp_path):
    path = tmp_path / "t.jsonl"
    rec = _fully_annotated().records()[0]
    rec["access"]["headline_only"] = True
    rec["evidence_excerpt"] = "a short line"
    path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    assert _run_guard(path) == 1

    # The same short excerpt on a source whose body we DID read is not this
    # guard's business (it is short and legitimately sourced).
    ok = tmp_path / "ok.jsonl"
    rec2 = _fully_annotated().records()[0]
    rec2["evidence_excerpt"] = "a short line"
    ok.write_text(json.dumps(rec2) + "\n", encoding="utf-8")
    assert _run_guard(ok) == 0


def test_privacy_guard_is_silent_on_a_missing_file(tmp_path):
    assert _run_guard(tmp_path / "nothing.jsonl") == 0


# --- the query surface -------------------------------------------------------
def test_source_yield_query_counts_the_funnel(tmp_path, capsys):
    query = importlib.import_module("telemetry_query")
    path = tmp_path / "t.jsonl"
    tel = telemetry.RunTelemetry("2026-08-01")
    for i in range(3):
        it = _item(source="italaw", sid=f"x{i}")
        cid = tel.observe(it)
        tel.note_enrichment(cid, i < 2)
        tel.note_classification(cid, ran=True, path="llm", model="m",
                                prompt_version="p", outcome="ok", attempts=1,
                                retried_strict=False, model_score_advisory=None)
        tel.note_surfacing(cid, surfaced=i == 0, reason="at_or_above_threshold",
                           digest="d", position=i)
    tel.flush(str(path))
    assert query.main(["telemetry_query", "--path", str(path), "--source-yield"]) == 0
    out = capsys.readouterr().out
    assert "italaw" in out
    # 3 candidates, 2 enriched, 3 classified, 1 surfaced.
    assert "3" in out and "2" in out and "1" in out


def test_source_yield_still_counts_a_tail_item_an_outage_fell_back_on(tmp_path, capsys):
    """The "classified" column is every TERMINAL outcome, derived, not listed.

    It used to be the hand-written pair ("ok", "keyword_only_by_design"). Adding
    `keyword_after_provider_error` on 2026-09-10 without touching this query
    would have made an outage read as a COLLAPSE IN YIELD — the tail still
    published, and the funnel would have reported it as never classified. That is
    a worse misreading than the one the new outcome fixes, so the set is derived
    from `classify.TERMINAL_OUTCOMES` and this test proves the derivation bites.
    """
    query = importlib.import_module("telemetry_query")
    from src.classify import TERMINAL_OUTCOMES

    assert query.CLASSIFIED_OUTCOMES == {o.value for o in TERMINAL_OUTCOMES}
    assert "keyword_after_provider_error" in query.CLASSIFIED_OUTCOMES

    path = tmp_path / "outage.jsonl"
    tel = telemetry.RunTelemetry("2026-09-10")
    for i in range(2):
        cid = tel.observe(_item(source="italaw", sid=f"tail{i}"))
        tel.note_enrichment(cid, False)
        tel.note_classification(
            cid, ran=True, path="keyword", model="keyword", prompt_version="p",
            outcome="keyword_after_provider_error", attempts=1,
            retried_strict=False, model_score_advisory=None)
    tel.flush(str(path))
    assert query.main(["telemetry_query", "--path", str(path), "--source-yield"]) == 0
    row = [ln for ln in capsys.readouterr().out.splitlines()
           if ln.startswith("italaw")][0]
    # source, candidates, enriched, classified, surfaced
    assert row.split() == ["italaw", "2", "0", "2", "0"]


# --- the enumerated outcome vocabulary ---------------------------------------
def test_the_outcome_vocabulary_is_derived_from_the_classifier(tmp_path):
    """The module docstring promises "enumerated outcomes". This is the enumeration.

    Derived rather than restated: a hand-written second copy of the outcome list
    is how `keyword_only_by_design` came to mean two different events in the
    first place. The only value that is not a `ClassifyOutcome` is `main.py`'s
    `pipeline_error` sentinel, which the classifier cannot produce because
    `classify_item` never raises.
    """
    from src.classify import ClassifyOutcome

    assert telemetry.CLASSIFICATION_OUTCOME_VALUES == (
        {o.value for o in ClassifyOutcome} | {telemetry.PIPELINE_ERROR_OUTCOME})
    assert "keyword_after_provider_error" in telemetry.CLASSIFICATION_OUTCOME_VALUES
    # "" is the untouched default and is deliberately NOT in the set: an absent
    # fact is not an unrecognised one, and it must not warn.
    assert "" not in telemetry.CLASSIFICATION_OUTCOME_VALUES


def test_every_committed_telemetry_record_carries_a_recognised_outcome():
    """The build failure behind the vocabulary. Run over the real file.

    An outcome value that reaches this file without being in the enumeration is
    either a typo or a code path nobody declared, and both are the kind of thing
    that is discovered a month later while counting a bad week. Includes the 141
    records that spell a failed tail call `keyword_only_by_design`: they stay in
    the vocabulary precisely because they are not back-filled.
    """
    path = os.path.join(REPO, telemetry.TELEMETRY_PATH)
    if not os.path.exists(path):
        return                              # no data is not a violation
    unknown: dict[str, int] = {}
    checked = 0
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            checked += 1
            outcome = (json.loads(line).get("classification") or {}).get("outcome", "")
            if outcome and outcome not in telemetry.CLASSIFICATION_OUTCOME_VALUES:
                unknown[outcome] = unknown.get(outcome, 0) + 1
    assert not unknown, (
        f"{checked} records checked; unenumerated classification outcomes: "
        f"{sorted(unknown.items())}")


def test_an_unenumerated_outcome_is_warned_and_still_recorded_verbatim(tmp_path, caplog):
    """Telemetry never edits what the run says happened.

    Normalising or dropping an unrecognised outcome would destroy the one record
    saying the vocabulary drifted — and telemetry must never take a run down, so
    it warns rather than raising. The build failure is the test above.
    """
    tel = telemetry.RunTelemetry("2026-09-10")
    cid = tel.observe(_item())
    with caplog.at_level("WARNING", logger="isds.telemetry"):
        tel.note_classification(cid, ran=True, path="llm", model="m",
                                prompt_version="p", outcome="invented_outcome",
                                attempts=1, retried_strict=False,
                                model_score_advisory=None)
    assert any("invented_outcome" in r.getMessage() for r in caplog.records)
    path = tmp_path / "t.jsonl"
    tel.flush(str(path))
    rec = json.loads(open(path, encoding="utf-8").read().strip())
    assert rec["classification"]["outcome"] == "invented_outcome"
