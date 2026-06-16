"""Unit tests for the ISDS watcher: state bootstrap, scoring bands, parsing,
config, and rendering. No network or API key required."""

import datetime
import json
import os

import yaml

from src import config, state
from src.classify import keyword_score, parse_json_response, classify_item
from src.main import parse_since
from src.sources.base import CandidateItem, parse_date

UTC = datetime.timezone.utc


def _item(title="t", summary="", raw=""):
    now = datetime.datetime.now(UTC)
    return CandidateItem("test", title, "http://x", title, now, summary, raw, {})


# --- state -------------------------------------------------------------------
def test_state_bootstrap_when_missing(tmp_path):
    p = tmp_path / "seen.json"
    st = state.load_state(str(p))
    assert st == {"sources": {}}


def test_state_corrupt_treated_empty(tmp_path):
    p = tmp_path / "seen.json"
    p.write_text("{not valid json")
    assert state.load_state(str(p)) == {"sources": {}}


def test_state_mark_and_roundtrip(tmp_path):
    p = tmp_path / "seen.json"
    st = state.load_state(str(p))
    state.mark_seen(st, "iisd_itn", "id-1")
    assert state.is_seen(st, "iisd_itn", "id-1")
    state.save_state(st, str(p))
    again = state.load_state(str(p))
    assert state.is_seen(again, "iisd_itn", "id-1")
    assert not state.is_seen(again, "iisd_itn", "id-2")


# --- since parsing -----------------------------------------------------------
def test_parse_since_units():
    now = datetime.datetime.now(UTC)
    assert (now - parse_since("7d")).days in (6, 7)
    assert (now - parse_since("48h")).total_seconds() >= 47 * 3600
    # bad input falls back to 7d
    assert (now - parse_since("garbage")).days in (6, 7)


def test_parse_since_is_tz_aware():
    assert parse_since("7d").tzinfo is not None


# --- digest selection / padding floor -----------------------------------------
def _classified(score, sid=None):
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    return ClassifiedItem("s", sid or f"id{score}", "u", "t", now, "", "",
                          relevance_score=score)


def test_select_surfaced_never_below_floor():
    from src.main import select_surfaced
    items = [_classified(s) for s in (80, 45, 30, 24, 10, 0)]
    out = select_surfaced(items, threshold=40, min_items=6, floor=25)
    # No item below the floor may ever be surfaced.
    assert all(c.relevance_score >= 25 for c in out)
    # Every match (>= threshold) is included, with no upper cap.
    assert {c.relevance_score for c in out} >= {80, 45}
    # The 30 (>= floor) fills toward the minimum; 24/10/0 never appear.
    assert 24 not in {c.relevance_score for c in out}


def test_select_surfaced_quiet_week_is_empty_not_padded():
    from src.main import select_surfaced
    # Nothing above the floor -> empty digest rather than padding to min_items.
    items = [_classified(s) for s in (24, 10, 0)]
    assert select_surfaced(items, threshold=40, min_items=6, floor=25) == []


# --- date parsing ------------------------------------------------------------
def test_parse_date_to_utc():
    d = parse_date("Tue, 21 Apr 2026 17:02:05 +0000")
    assert d is not None and d.tzinfo is not None
    assert parse_date("not a date") is None
    assert parse_date(None) is None


# --- scoring bands (the calibrated few-shot gold set) ------------------------
def test_scorer_matches_fingerprint_examples():
    fp = yaml.safe_load(open("fingerprint.yaml"))
    for ex in fp["few_shot_examples"]:
        r = keyword_score(_item(ex["title"], ex["summary"], ex["summary"]))
        s = r["relevance_score"]
        band = "HIGH" if s >= 70 else "MEDIUM" if s >= 40 else "LOW"
        assert band == ex["expected_band"], f"{ex['title']}: got {s} ({band})"


def test_scorer_rejects_offtheme():
    r = keyword_score(_item("Ferrer v. Ecuador", "ICSID case registered", ""))
    assert r["relevance_score"] < 40
    assert "keyword_fallback" in r["thematic_tags"]


# --- JSON parsing (LLM response robustness) ----------------------------------
def test_parse_json_strips_fences():
    raw = '```json\n{"relevance_score": 80, "matched_rings": ["ip_as_investment"], ' \
          '"thematic_tags": ["patent"], "digest_summary": "A. B."}\n```'
    out = parse_json_response(raw)
    assert out and out["relevance_score"] == 80
    assert out["matched_rings"] == ["ip_as_investment"]


def test_parse_json_rejects_garbage():
    assert parse_json_response("not json at all") is None


# --- verbatim-quote integrity -------------------------------------------------
def test_quote_in_source_accepts_verbatim_and_curly():
    from src.classify import _quote_in_source
    it = _item("Title", "", "The tribunal found the ruling manifestly unjust and shocking.")
    # exact substring
    assert _quote_in_source("the ruling manifestly unjust and shocking", it)
    # only differs by curly quotes / em dash typography
    it2 = _item("T", "", 'He called it an "abuse of right" — a clear one indeed.')
    assert _quote_in_source('an “abuse of right” — a clear one indeed', it2)


def test_quote_in_source_rejects_paraphrase_and_short():
    from src.classify import _quote_in_source
    it = _item("Title", "", "The tribunal dismissed the claim on abuse of right grounds.")
    # a paraphrase that is not actually in the text
    assert not _quote_in_source("the panel threw out the case for treaty shopping reasons", it)
    # too short to be meaningful
    assert not _quote_in_source("abuse", it)


def test_parse_json_coerces_invalid_rings():
    raw = '{"relevance_score": 50, "matched_rings": ["ip_as_investment", "bogus"], ' \
          '"thematic_tags": [], "digest_summary": "A. B."}'
    out = parse_json_response(raw)
    assert "bogus" not in out["matched_rings"]
    assert "ip_as_investment" in out["matched_rings"]


# --- classify_item offline fallback path (no provider/key) -------------------
def test_classify_item_offline_never_raises(monkeypatch):
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    ci = classify_item(_item("Patent dispute", "promise utility doctrine denial of justice", ""))
    assert ci.relevance_score >= 0
    assert isinstance(ci.matched_rings, list)


def test_classify_records_model_in_metadata(monkeypatch):
    # Offline path records the keyword model; the LLM paths record the model ID.
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)
    ci = classify_item(_item("t", "denial of justice supreme court", ""))
    assert ci.metadata.get("model") == "keyword"


def test_resolved_model_ids():
    from src.classify import _resolved_model, DEFAULT_ANTHROPIC_MODEL, DEFAULT_GEMINI_MODEL
    assert _resolved_model("anthropic") == DEFAULT_ANTHROPIC_MODEL
    assert _resolved_model("gemini") == DEFAULT_GEMINI_MODEL
    assert _resolved_model(None) is None


# --- config ------------------------------------------------------------------
def test_recipients_hardcoded():
    # Temporarily narrowed to a single recipient on request.
    assert config.RECIPIENTS == ["jackemorywilliams@icloud.com"]


def test_missing_email_secrets_detected():
    cfg = config.Config(smtp_user=None, smtp_pass=None)
    miss = config.missing_email_secrets(cfg)
    assert "SMTP_USER" in miss and "SMTP_PASS" in miss


# --- render ------------------------------------------------------------------
def test_render_empty_and_populated():
    from src import render
    from src.classify import ClassifiedItem
    now = datetime.datetime.now(UTC)
    stats = {"total_candidates": 0, "classified": 0, "above_threshold": 0,
             "per_source": {"iisd_itn": 0}, "dropped_sources": [], "threshold": 60,
             "provider": None}
    empty = render.render_digest([], now, now, stats)
    assert "No thematically relevant developments this week" in empty

    ci = ClassifiedItem("iisd_itn", "id", "http://x", "Patent case", now,
                        "s", "r", relevance_score=85,
                        matched_rings=["ip_as_investment"], thematic_tags=["patent"],
                        digest_summary="One. Two.")
    ci.metadata = {"notable_quote": "A notable doctrinal line."}
    stats["above_threshold"] = 1
    html = render.render_digest([ci], now, now, stats)
    assert "Patent case" in html and "85" in html
    assert "notable doctrinal line" in html
