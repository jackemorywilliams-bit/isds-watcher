"""The Monday review packet must never mail an empty claim, and the daily email
must never restate digest numbers that contradict meta.json.

Regression tests for the 2026-07-27 defects:
  1. the packet's brief-memo URL scraping captioned URLs from embedded JSON blocks,
     mailing the operator '(brief citation) "sourceurl": ""' with no claim text —
     claims now sample from the verification ledger (full sentence + id + quote);
  2. the daily record said 'One screened item' while the digest header said
     'Screened: 10' and nothing machine-checked the prose before it was emailed.
"""

import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import verify  # noqa: E402

_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _load(name):
    path = os.path.join(_ROOT, "scripts", f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- packet claims come from the ledger with full text ----------------------------

def test_ledger_sampling_yields_full_claim_text(tmp_path, monkeypatch):
    rp = _load("review_prep")
    ledger = tmp_path / "analytics" / "verification_ledger.jsonl"
    monkeypatch.setattr(verify, "LEDGER_PATH", str(ledger))
    monkeypatch.setattr(rp, "_REPO_ROOT", str(tmp_path))
    cid = verify.create_claim(
        "In Eli Lilly v. Canada, the tribunal dismissed the claim in its entirety.",
        "https://example.org/award", source_snapshot="claim is dismissed in its entirety",
        supporting_locator="Decision, item (2)", path=str(ledger))
    monkeypatch.setattr(rp.verify if hasattr(rp, "verify") else verify, "LEDGER_PATH",
                        str(ledger), raising=False)
    claims = rp.sample_ledger_claims(str(tmp_path), limit=5)
    assert len(claims) == 1
    c = claims[0]
    assert c["claim"].startswith("In Eli Lilly v. Canada")
    assert c["claim_id"] == cid
    assert c["quote"] == "claim is dismissed in its entirety"


def test_empty_claims_are_dropped_not_mailed(tmp_path, monkeypatch):
    rp = _load("review_prep")
    monkeypatch.setattr(rp, "sample_digest_claims", lambda *a, **k: [
        {"claim": "(brief citation)", "url": "https://x.org", "origin": "digest",
         "item_date": "", "source": "", "self_reported_paywalled": False,
         "digest_matches": None},
        {"claim": "", "url": "https://y.org", "origin": "digest", "item_date": "",
         "source": "", "self_reported_paywalled": False, "digest_matches": None},
        {"claim": "A real claim sentence.", "url": "https://z.org", "origin": "digest",
         "item_date": "", "source": "", "self_reported_paywalled": False,
         "digest_matches": None},
    ])
    monkeypatch.setattr(rp, "sample_ledger_claims", lambda *a, **k: [])
    monkeypatch.setattr(rp, "check_url", lambda url: {"verdict": "ok", "status": 200,
                                                      "detail": ""})
    draft = rp.build_draft(str(tmp_path), max_claims=8, n_digests=1)
    assert draft["dropped_empty"] == 2
    assert [c["claim"] for c in draft["sampled"]] == ["A real claim sentence."]
    rendered = rp.render(draft)
    assert "(brief citation)" not in rendered
    assert "malformed claim record" in rendered


def test_render_carries_quote_and_mark_command(tmp_path, monkeypatch):
    rp = _load("review_prep")
    monkeypatch.setattr(rp, "sample_digest_claims", lambda *a, **k: [])
    monkeypatch.setattr(rp, "sample_ledger_claims", lambda *a, **k: [
        {"claim": "The tribunal dismissed the claim.", "claim_id": "a" * 64,
         "url": "https://example.org/a", "locator": "https://example.org/a",
         "quote": "is dismissed", "pinpoint": "para. 590", "origin": "verification ledger",
         "item_date": "2026-07-27", "source": "primary",
         "self_reported_paywalled": False, "digest_matches": None}])
    monkeypatch.setattr(rp, "check_url", lambda url: {"verdict": "ok", "status": 200,
                                                      "detail": ""})
    rendered = rp.render(rp.build_draft(str(tmp_path), max_claims=8, n_digests=1))
    assert "The tribunal dismissed the claim." in rendered
    assert 'Look for this exact line in the source: "is dismissed" (para. 590)' in rendered
    assert f"verify.py mark {'a' * 16} --verified --quote-ok" in rendered


# ---- daily email consistency guard ------------------------------------------------

def _daily_with_digest(tmp_path, monkeypatch, evaluated, matches, leads):
    sd = _load("send_daily_update")
    d = tmp_path / "digests" / "2026-07-27_ISDS-Thematic-Watch"
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps(
        {"screened": evaluated, "matches": matches, "watch_list_leads": leads}),
        encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return sd


def test_consistency_header_prints_numbers_of_record(tmp_path, monkeypatch):
    sd = _daily_with_digest(tmp_path, monkeypatch, 10, 0, 0)
    header = sd._consistency_header("A quiet day with nothing to report.")
    assert "10 candidates evaluated" in header
    assert "0 items surfaced" in header
    assert "CONSISTENCY WARNING" not in header


def test_consistency_header_flags_contradicting_screened_count(tmp_path, monkeypatch):
    sd = _daily_with_digest(tmp_path, monkeypatch, 10, 0, 0)
    header = sd._consistency_header(
        "This week's digest (July 20, 2026): One screened item — IAReporter.")
    assert "CONSISTENCY WARNING" in header
    assert "One screened" in header


def test_consistency_header_accepts_matching_counts(tmp_path, monkeypatch):
    sd = _daily_with_digest(tmp_path, monkeypatch, 14, 0, 1)
    # 14 = evaluated, 1 = surfaced (0 matches + 1 lead): both usages are consistent.
    header = sd._consistency_header("Of 14 screened candidates, one screened item surfaced.")
    assert "CONSISTENCY WARNING" not in header
