"""The Monday review packet's council section must NEVER silently show nothing.

Regression tests for the 2026-07-20 failure, which had three independent causes:
  1. the packet read analytics/roundtable/ — a directory nothing writes — so the
     council session never reached the operator (every Monday, silently);
  2. the chairman reconvene stage failed and the "best-effort" catch swallowed it,
     leaving a stub accountability entry with no marker;
  3. human-review.yml fired at the same cron minute as weekly.yml, racing the very
     session it reports (the 07-20 council finished at 15:07 UTC, two hours after
     the packet had already been emailed).

Each cause now has a guard, and each guard has a test.
"""

import importlib.util
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_send_human_review():
    path = os.path.join(os.path.dirname(__file__), "..", "scripts", "send_human_review.py")
    spec = importlib.util.spec_from_file_location("send_human_review", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_council_log(root, entries):
    os.makedirs(os.path.join(root, "state"), exist_ok=True)
    with open(os.path.join(root, "state", "council_log.json"), "w", encoding="utf-8") as fh:
        json.dump(entries, fh)


def _weekly_entry(date_str, **over):
    entry = {
        "ts": f"{date_str}T15:00:00+00:00",
        "date": date_str,
        "type": "weekly-council",
        "issue": 25,
        "members": {"chairman": "agenda set", "analyst": "memo 17437 chars",
                    "security": "clean", "editor": "4 sections, 6 threads"},
        "status": "A quiet but honest week.",
        "accountability": [{"member": "analyst", "assessment": "disciplined"}],
        "next_steps": ["Recheck IISD ITN."],
        "escalations": ["Verification infrastructure gap."],
        "minutes_missing": False,
    }
    entry.update(over)
    return entry


def test_full_weekly_entry_renders_minutes(tmp_path):
    import datetime
    today = datetime.date.today().isoformat()
    mod = _load_send_human_review()
    _write_council_log(tmp_path, [_weekly_entry(today)])
    out = mod._latest_weekly_council(root=str(tmp_path))
    assert out["fresh"] and out["complete"]
    md = out["markdown"]
    assert "A quiet but honest week." in md
    assert "analyst" in md and "disciplined" in md
    assert "Recheck IISD ITN." in md
    assert "Verification infrastructure gap." in md


def test_stub_entry_is_flagged_loudly_not_silently(tmp_path):
    """The 2026-07-20 shape: session ran, minutes empty. The packet must say so."""
    import datetime
    today = datetime.date.today().isoformat()
    mod = _load_send_human_review()
    _write_council_log(tmp_path, [_weekly_entry(
        today, status="", accountability=[], next_steps=[], escalations=[],
        minutes_missing=True)])
    out = mod._latest_weekly_council(root=str(tmp_path))
    assert out["fresh"] and not out["complete"]
    assert "MISSING" in out["markdown"]
    assert f"briefs/{today}-memo.md" in out["markdown"]


def test_legacy_stub_without_marker_still_flagged(tmp_path):
    """Pre-fix stub entries carry no minutes_missing key; emptiness alone must trip
    the incomplete path (the historical 07-20 entry must never render as fine)."""
    import datetime
    today = datetime.date.today().isoformat()
    mod = _load_send_human_review()
    entry = _weekly_entry(today, status="", accountability=[], next_steps=[],
                          escalations=[])
    del entry["minutes_missing"]
    _write_council_log(tmp_path, [entry])
    out = mod._latest_weekly_council(root=str(tmp_path))
    assert not out["complete"]
    assert "MISSING" in out["markdown"]


def test_stale_or_absent_entry_flags_the_pipeline(tmp_path):
    mod = _load_send_human_review()
    _write_council_log(tmp_path, [_weekly_entry("2026-01-05")])  # far in the past
    out = mod._latest_weekly_council(root=str(tmp_path))
    assert not out["fresh"]
    assert "did not run or did not record" in out["markdown"]
    # And with no log at all:
    out2 = mod._latest_weekly_council(root=str(tmp_path / "nowhere"))
    assert not out2["fresh"]


def test_council_log_marks_and_renders_missing_minutes(tmp_path, monkeypatch):
    from datetime import datetime, timezone
    from src import council_log
    monkeypatch.chdir(tmp_path)
    brief = {"_agenda": "set", "_memo": "x" * 100, "_security_clean": True,
             "sections": [1, 2], "open_threads": [1], "minutes": None}
    council_log.append_weekly("2026-07-27", 32, brief, datetime.now(timezone.utc))
    entries = json.load(open(os.path.join("state", "council_log.json"), encoding="utf-8"))
    assert entries[0]["minutes_missing"] is True
    md = open(os.path.join("analytics", "council-log.md"), encoding="utf-8").read()
    assert "MINUTES MISSING" in md


def test_council_log_full_minutes_not_marked(tmp_path, monkeypatch):
    from datetime import datetime, timezone
    from src import council_log
    monkeypatch.chdir(tmp_path)
    brief = {"_agenda": "set", "_memo": "x" * 100, "_security_clean": True,
             "sections": [1, 2], "open_threads": [1],
             "minutes": {"status": "good week", "accountability": [],
                         "next_steps": ["a"], "escalations": []}}
    council_log.append_weekly("2026-07-27", 32, brief, datetime.now(timezone.utc))
    entries = json.load(open(os.path.join("state", "council_log.json"), encoding="utf-8"))
    assert entries[0]["minutes_missing"] is False
    md = open(os.path.join("analytics", "council-log.md"), encoding="utf-8").read()
    assert "MINUTES MISSING" not in md
    assert "good week" in md


def test_review_email_fires_after_weekly_council():
    """The human-review cron must be strictly later on Monday than weekly.yml's."""
    import re
    root = os.path.join(os.path.dirname(__file__), "..")

    def cron_of(path):
        text = open(os.path.join(root, ".github", "workflows", path), encoding="utf-8").read()
        m = re.search(r'cron:\s*"(\d+) (\d+) \* \* 1"', text)
        assert m, f"no Monday cron in {path}"
        return int(m.group(2)) * 60 + int(m.group(1))

    weekly = cron_of("weekly.yml")
    review = cron_of("human-review.yml")
    assert review >= weekly + 120, (
        "human-review.yml must fire at least 2h after weekly.yml so the council's "
        f"committed record exists (weekly={weekly}min, review={review}min)")


def test_optimization_snapshot_reads_real_log():
    mod = _load_send_human_review()
    snap = mod._optimization_snapshot()
    # The repo's real optimization log has dated bullets; the snapshot must carry
    # at least one and stay email-sized.
    assert snap.startswith("- 20")
    assert len(snap) < 4000
