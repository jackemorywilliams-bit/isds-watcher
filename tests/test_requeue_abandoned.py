"""scripts/requeue_abandoned.py — reversing an abandonment that was ours."""
import importlib
import json
import os
import sys

import pytest

from src import state

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))


def _setup(tmp_path):
    st = {"sources": {"gmail_scholar": {
        "u1": {"at": "2026-09-07T18:03:18+00:00", "outcome": "abandoned", "run": "2026-09-07"},
        "u2": {"at": "2026-09-07T18:03:18+00:00", "outcome": "abandoned", "run": "2026-09-07"},
        "ok": {"at": "2026-09-07T18:03:18+00:00", "outcome": "ok", "run": "2026-09-07"},
        "old": {"at": "2026-08-01T00:00:00+00:00", "outcome": "abandoned", "run": "2026-08-01"},
    }}}
    state.save_state(st, str(tmp_path / "seen.json"))
    state.save_deferred({}, str(tmp_path / "deferred.json"))
    ledger = tmp_path / "abandoned.jsonl"
    rows = [
        {"schema": 1, "run": "2026-09-07", "source": "gmail_scholar", "source_id": "u1",
         "url": "https://x/u1", "attempts": 3, "last_outcome": "provider_error",
         "first_deferred": "2026-08-24T16:12:21+00:00"},
        {"schema": 1, "run": "2026-09-07", "source": "gmail_scholar", "source_id": "u2",
         "url": "https://x/u2", "attempts": 3, "last_outcome": "provider_error",
         "first_deferred": "2026-08-31T19:21:30+00:00"},
        {"schema": 1, "run": "2026-08-01", "source": "gmail_scholar", "source_id": "old",
         "url": "https://x/old", "attempts": 3, "last_outcome": "parse_failed",
         "first_deferred": "2026-07-01T00:00:00+00:00"},
    ]
    ledger.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return tmp_path


def _args(tmp_path, *extra):
    return ["--run", "2026-09-07", "--last-outcome", "provider_error",
            "--because", "anthropic 1.x removed temperature; every call raised TypeError",
            "--fix", "PR #148",
            "--state", str(tmp_path / "seen.json"),
            "--deferred", str(tmp_path / "deferred.json"),
            "--ledger", str(tmp_path / "abandoned.jsonl"),
            "--requeued", str(tmp_path / "requeued.jsonl"), *extra]


def test_requeue_reverses_only_the_matching_abandonments(tmp_path):
    _setup(tmp_path)
    mod = importlib.import_module("requeue_abandoned")
    assert mod.main(_args(tmp_path)) == 0

    st = state.load_state(str(tmp_path / "seen.json"))
    assert not state.is_seen(st, "gmail_scholar", "u1")
    assert not state.is_seen(st, "gmail_scholar", "u2")
    assert state.seen_outcome(st, "gmail_scholar", "ok") == "ok"          # untouched
    assert state.seen_outcome(st, "gmail_scholar", "old") == "abandoned"  # other run, untouched

    dq = state.load_deferred(str(tmp_path / "deferred.json"))
    assert set(dq["gmail_scholar"]) == {"u1", "u2"}
    e = dq["gmail_scholar"]["u1"]
    assert e["attempts"] == 0 and e["url"] == "https://x/u1"
    assert e["first_deferred"] == "2026-08-24T16:12:21+00:00"
    assert e["requeued_from_abandoned"]["attempts_before"] == 3
    assert e["requeued_from_abandoned"]["fix"] == "PR #148"

    lines = [json.loads(l) for l in (tmp_path / "requeued.jsonl").read_text().splitlines()]
    assert {l["source_id"] for l in lines} == {"u1", "u2"}
    assert all(l["abandoned_run"] == "2026-09-07" and l["because"] for l in lines)
    # The abandoned ledger is append-only: still three lines.
    assert len((tmp_path / "abandoned.jsonl").read_text().splitlines()) == 3


def test_requeue_is_idempotent(tmp_path):
    _setup(tmp_path)
    mod = importlib.import_module("requeue_abandoned")
    assert mod.main(_args(tmp_path)) == 0
    assert mod.main(_args(tmp_path)) == 0
    lines = (tmp_path / "requeued.jsonl").read_text().splitlines()
    assert len(lines) == 2, "a second run must not requeue (or ledger) anything twice"


def test_requeue_dry_run_writes_nothing(tmp_path):
    _setup(tmp_path)
    mod = importlib.import_module("requeue_abandoned")
    assert mod.main(_args(tmp_path, "--dry-run")) == 0
    st = state.load_state(str(tmp_path / "seen.json"))
    assert state.seen_outcome(st, "gmail_scholar", "u1") == "abandoned"
    assert not (tmp_path / "requeued.jsonl").exists()


def test_requeued_state_passes_the_seen_integrity_guard(tmp_path):
    _setup(tmp_path)
    mod = importlib.import_module("requeue_abandoned")
    assert mod.main(_args(tmp_path)) == 0
    guard = importlib.import_module("check_seen_integrity")
    checked, legacy, problems = guard.check(tmp_path / "seen.json", tmp_path / "abandoned.jsonl")
    assert problems == []


# --- 2026-09-11: a requeue must not be consumed unread -------------------------
def test_reopen_unread_uses_telemetry_not_memory(tmp_path):
    """Seen 'ok' + telemetry says no title and no body were seen -> reopened."""
    import hashlib
    state.save_state({"sources": {"gmail_scholar": {
        "https://x/u1": {"at": "2026-09-07T23:30:00+00:00", "outcome": "ok", "run": "2026-09-07"},
        "https://x/u2": {"at": "2026-09-07T23:30:00+00:00", "outcome": "ok", "run": "2026-09-07"},
    }}}, str(tmp_path / "seen.json"))
    state.save_deferred({}, str(tmp_path / "deferred.json"))
    (tmp_path / "requeued.jsonl").write_text("".join(json.dumps(r) + "\n" for r in [
        {"schema": 1, "source": "gmail_scholar", "source_id": "https://x/u1", "url": "https://x/u1",
         "abandoned_run": "2026-09-07"},
        {"schema": 1, "source": "gmail_scholar", "source_id": "https://x/u2", "url": "https://x/u2",
         "abandoned_run": "2026-09-07"},
    ]), encoding="utf-8")
    def tel(sid, run_id, marked_seen, title_len, body_len, outcome="ok", abandoned=False):
        return {"run_id": run_id, "run_date": "2026-09-07", "source": "gmail_scholar",
                "source_id_hash": hashlib.sha256(sid.encode()).hexdigest(),
                "entered_enrichment": True,
                "dedup": {"marked_seen": marked_seen, "deferred": not marked_seen, "abandoned": abandoned},
                "classification": {"outcome": outcome},
                "access": {"text_len_title": title_len, "text_len_body": body_len}}
    # A date is not a run: 2026-09-07 carries three run_ids. u1 was DEFERRED with a
    # 5000-char body on an earlier same-date run and RETIRED on the later run with
    # nothing to read: unread. u2 is the inverse — 0/0 on the earlier run that only
    # deferred it, a body on the run that retired it: NOT unread.
    # The live shape: the same date also holds the ABANDONMENT row (marked_seen,
    # abandoned, provider_error, title still present) — it must be ignored.
    (tmp_path / "telemetry.jsonl").write_text("".join(json.dumps(t) + "\n" for t in [
        tel("https://x/u1", "2026-09-07-a", True, 111, 5000, outcome="provider_error", abandoned=True),
        tel("https://x/u1", "2026-09-07-b", True, 0, 0),
        tel("https://x/u2", "2026-09-07-a", True, 0, 0, outcome="provider_error", abandoned=True),
        tel("https://x/u2", "2026-09-07-b", True, 0, 5000),
    ]), encoding="utf-8")
    mod = importlib.import_module("requeue_abandoned")
    args = ["--reopen-unread", "--because", "consumed unread", "--fix", "PR",
            "--state", str(tmp_path / "seen.json"), "--deferred", str(tmp_path / "deferred.json"),
            "--requeued", str(tmp_path / "requeued.jsonl"), "--telemetry", str(tmp_path / "telemetry.jsonl")]
    assert mod.main(args) == 0
    st = state.load_state(str(tmp_path / "seen.json"))
    assert not state.is_seen(st, "gmail_scholar", "https://x/u1")      # reopened
    assert state.seen_outcome(st, "gmail_scholar", "https://x/u2") == "ok"  # was read; untouched
    dq = state.load_deferred(str(tmp_path / "deferred.json"))["gmail_scholar"]
    assert set(dq) == {"https://x/u1"} and dq["https://x/u1"]["attempts"] == 0
    assert dq["https://x/u1"]["reopened_unread"]["consumed_run"] == "2026-09-07"
    lines = [json.loads(l) for l in (tmp_path / "requeued.jsonl").read_text().splitlines()]
    assert sum(1 for l in lines if l.get("reopened")) == 1
    assert mod.main(args) == 0                                           # idempotent
    assert sum(1 for l in [json.loads(l) for l in (tmp_path / "requeued.jsonl").read_text().splitlines()] if l.get("reopened")) == 1


def test_requeue_mode_still_requires_run_and_outcome(tmp_path):
    mod = importlib.import_module("requeue_abandoned")
    with pytest.raises(SystemExit):
        mod.main(["--because", "x", "--state", str(tmp_path / "s.json"),
                  "--deferred", str(tmp_path / "d.json"), "--ledger", str(tmp_path / "l.jsonl")])
