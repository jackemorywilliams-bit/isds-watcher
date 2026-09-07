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
