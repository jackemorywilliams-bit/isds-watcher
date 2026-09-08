"""scripts/scholar_intake.py — daily capture of Scholar alerts into the queue."""
import datetime
import importlib
import json
import os
import sys

import pytest

from src import state
from src.sources import gmail_scholar
from src.sources.base import CandidateItem

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
UTC = datetime.timezone.utc


def _paper(url, title="A paper about trade secrets in ISDS"):
    return CandidateItem("gmail_scholar", url, url, title,
                         datetime.datetime(2026, 9, 8, 5, 16, tzinfo=UTC),
                         "snippet", "snippet", {"via": "google_scholar"})


@pytest.fixture
def mailbox(monkeypatch, tmp_path):
    """Credentials present; the source returns three papers: one already seen,
    one already queued, one new. The mailbox holds two alerts in 30 days."""
    monkeypatch.setenv("GMAIL_ALERT_USER", "u@gmail.com")
    monkeypatch.setenv("GMAIL_ALERT_PASS", "app-password")
    papers = [_paper("https://x/seen"), _paper("https://x/queued"), _paper("https://x/new")]
    monkeypatch.setattr(gmail_scholar.GmailScholarSource, "fetch", lambda self, since: list(papers))
    monkeypatch.setattr(gmail_scholar, "scholar_mailbox_status", lambda days=30: ("ok", [
        {"uid": "2", "date": "2026-09-08T05:16:00+00:00",
         "subject": '("trade secret" OR "trade secrets") ("investment arbitration" OR ISDS OR ICSID) - new results'},
        {"uid": "1", "date": "2026-08-31T05:10:00+00:00", "subject": "older alert"},
    ]))
    state.save_state({"sources": {"gmail_scholar": {
        "https://x/seen": {"at": "2026-08-31T00:00:00+00:00", "outcome": "ok", "run": "2026-08-31"}}}},
        str(tmp_path / "seen.json"))
    state.save_deferred({"gmail_scholar": {"https://x/queued": {
        "first_deferred": "2026-09-07T00:00:00+00:00", "attempts": 1, "last_outcome": "provider_error",
        "url": "https://x/queued", "title": "t", "published": "", "summary": ""}}},
        str(tmp_path / "deferred.json"))
    return tmp_path


def _args(tmp_path, *extra):
    return ["--days", "3", "--state", str(tmp_path / "seen.json"),
            "--deferred", str(tmp_path / "deferred.json"),
            "--out", str(tmp_path / "intake"), *extra]


def test_intake_queues_only_the_new_paper_and_records_the_mailbox(mailbox, capsys):
    mod = importlib.import_module("scholar_intake")
    assert mod.main(_args(mailbox)) == 0
    dq = state.load_deferred(str(mailbox / "deferred.json"))["gmail_scholar"]
    assert set(dq) == {"https://x/queued", "https://x/new"}
    new = dq["https://x/new"]
    assert new["attempts"] == 0 and new["last_outcome"] == "intake"
    assert new["title"].startswith("A paper") and new["published"].startswith("2026-09-08")
    assert new["intake"]["by"] == "scholar-intake" and new["intake"]["window_days"] == 3
    assert dq["https://x/queued"]["attempts"] == 1, "an existing queue entry was touched"

    rec = json.loads((mailbox / "intake" / "2026-09-08.json").read_text()) \
        if (mailbox / "intake" / "2026-09-08.json").exists() else \
        json.loads(next((mailbox / "intake").glob("*.json")).read_text())
    assert rec["mailbox"]["alerts_30d"] == 2
    assert rec["mailbox"]["newest_alert_date"].startswith("2026-09-08")
    assert "trade secret" in rec["mailbox"]["newest_alert_subject"]
    assert rec["mailbox"]["alert_dates"] == ["2026-09-08", "2026-08-31"]
    assert rec["papers_in_window"] == 3 and rec["queued_new"] == 1
    assert rec["already_seen"] == 1 and rec["already_queued"] == 1
    assert rec["queued_urls"] == ["https://x/new"]
    assert "title" not in json.dumps(rec["queued_urls"])   # no paper text in the record
    out = capsys.readouterr().out
    assert "newest 2026-09-08" in out and "1 queued" in out
    assert "alert days (30d, newest first): 2026-09-08, 2026-08-31" in out


def test_intake_is_idempotent(mailbox):
    mod = importlib.import_module("scholar_intake")
    assert mod.main(_args(mailbox)) == 0
    assert mod.main(_args(mailbox)) == 0
    dq = state.load_deferred(str(mailbox / "deferred.json"))["gmail_scholar"]
    assert len(dq) == 2
    assert dq["https://x/new"]["attempts"] == 0


def test_intake_dry_run_writes_nothing(mailbox):
    mod = importlib.import_module("scholar_intake")
    assert mod.main(_args(mailbox, "--dry-run")) == 0
    assert "https://x/new" not in state.load_deferred(str(mailbox / "deferred.json"))["gmail_scholar"]
    assert not (mailbox / "intake").exists()


def test_intake_without_credentials_is_a_loud_configuration_failure(monkeypatch, tmp_path):
    for var in ("GMAIL_ALERT_USER", "GMAIL_ALERT_PASS"):
        monkeypatch.delenv(var, raising=False)
    mod = importlib.import_module("scholar_intake")
    assert mod.main(_args(tmp_path)) == 2


def test_the_weekly_run_rebuilds_an_intake_queued_paper(mailbox):
    """The queue entry carries what deferred_candidates needs, so Monday's run
    classifies the paper even if the mailbox window has moved past it."""
    from src.main import deferred_candidates
    mod = importlib.import_module("scholar_intake")
    assert mod.main(_args(mailbox)) == 0
    dq = state.load_deferred(str(mailbox / "deferred.json"))
    rebuilt = {it.source_id: it for it in deferred_candidates(dq, set())}
    it = rebuilt["https://x/new"]
    assert it.source == "gmail_scholar" and it.title.startswith("A paper")
    assert it.metadata["from_deferred"] is True and it.metadata["deferred_attempts"] == 0
    assert it.published.date() == datetime.date(2026, 9, 8)


def test_the_workflow_runs_after_scholar_sends_and_commits_the_queue():
    text = open(os.path.join(REPO, ".github", "workflows", "scholar-intake.yml"), encoding="utf-8").read()
    assert 'cron: "30 6 * * *"' in text
    assert "GMAIL_ALERT_USER" in text and "GMAIL_ALERT_PASS" in text
    assert "python scripts/scholar_intake.py" in text
    assert "git add state/deferred.json analytics/scholar-intake/" in text
    assert "[skip ci]" in text and "group: isds-watcher" in text
