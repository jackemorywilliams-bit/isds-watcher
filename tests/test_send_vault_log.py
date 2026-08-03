"""The vault work log must reach Emory, and must stay silent when there is nothing.

The archivist's session records are worthless if they sit unread in the repo —
that is the failure this emailer exists to prevent, and it is the same failure
that lost three days of vault work in early August. These tests pin the two
things that matter: a session that needs him is delivered and says so, and a
week with no session sends nothing rather than a false all-clear.
"""

from __future__ import annotations

import json  # noqa: F401  (kept for parity with sibling test modules)
import os

import pytest

from scripts import send_vault_log


@pytest.fixture()
def vault(tmp_path, monkeypatch):
    """Point the module at a temporary vault-sessions tree."""
    d = tmp_path / "vault-sessions"
    d.mkdir()
    monkeypatch.setattr(send_vault_log, "VAULT_DIR", str(d))
    monkeypatch.setattr(send_vault_log, "SENT_MARKER_DIR", str(d / ".sent"))
    return d


def _write(vault, date_str, body="# Session\n\nNothing to report.\n"):
    (vault / f"{date_str}.md").write_text(body, encoding="utf-8")


# --- what gets sent -------------------------------------------------------

def test_nothing_on_file_sends_nothing(vault, capsys):
    assert send_vault_log.main([]) == 0
    assert "NOTHING-NEW" in capsys.readouterr().out


def test_a_record_with_no_marker_is_pending(vault):
    _write(vault, "2026-08-04")
    assert send_vault_log._unsent() == ["2026-08-04"]


def test_a_sent_record_is_not_resent(vault):
    _write(vault, "2026-08-04")
    send_vault_log._mark_sent("2026-08-04")
    assert send_vault_log._unsent() == []


def test_backlog_is_sent_oldest_first(vault):
    """A session that found drift must not be skipped just because a newer one exists."""
    for d in ("2026-08-07", "2026-08-01", "2026-08-04"):
        _write(vault, d)
    assert send_vault_log._unsent() == ["2026-08-01", "2026-08-04", "2026-08-07"]


def test_non_date_files_are_ignored(vault):
    _write(vault, "2026-08-04")
    (vault / "README.md").write_text("not a session", encoding="utf-8")
    (vault / "notes.txt").write_text("nor this", encoding="utf-8")
    assert send_vault_log._sessions() == ["2026-08-04"]


def test_missing_directory_is_not_an_error(tmp_path, monkeypatch):
    monkeypatch.setattr(send_vault_log, "VAULT_DIR", str(tmp_path / "absent"))
    monkeypatch.setattr(send_vault_log, "SENT_MARKER_DIR", str(tmp_path / "absent/.sent"))
    assert send_vault_log._sessions() == []
    assert send_vault_log.main([]) == 0


# --- attention flagging ---------------------------------------------------

@pytest.mark.parametrize("line", [
    "NEEDS YOU: confirm the treaty text.",
    "ACTION: authorize the fix.",
    "FOR EMORY: the ledger amendment.",
    "TO VERIFY: the Talkwalker URLs.",
    "AWAITING EMORY on the source sign-off.",
    "needs verification: the citation.",
])
def test_operator_lines_are_counted(line):
    assert send_vault_log._needs_attention(f"# Session\n\n{line}\n") == 1


def test_ordinary_prose_is_not_counted():
    body = "# Session\n\nThe registry was rebuilt and the change log extended.\n"
    assert send_vault_log._needs_attention(body) == 0


def test_lede_distinguishes_needs_you_from_all_clear():
    needs = send_vault_log._lede("NEEDS YOU: a thing.\n", "2026-08-04")
    clear = send_vault_log._lede("All quiet.\n", "2026-08-04")
    assert "need you" in needs and "1" in needs
    assert "Nothing needs you" in clear


# --- delivery and marking -------------------------------------------------

def test_send_marks_sent_and_subject_carries_the_count(vault, monkeypatch):
    _write(vault, "2026-08-04", "# Session\n\nNEEDS YOU: confirm the treaty text.\n")
    sent = {}

    def _fake_send(html, subject, cfg, recipients=None):
        sent["subject"] = subject
        sent["html"] = html
        return True

    monkeypatch.setattr(send_vault_log, "send_digest", _fake_send)
    assert send_vault_log.main([]) == 0
    assert "2026-08-04" in sent["subject"]
    assert "needs you" in sent["subject"]
    assert send_vault_log._already_sent("2026-08-04")
    # The operator line must survive into the rendered email as a callout.
    assert 'class="act"' in sent["html"]
    assert "confirm the treaty text." in sent["html"]


def test_a_failed_send_is_not_marked_and_exits_nonzero(vault, monkeypatch):
    _write(vault, "2026-08-04")
    monkeypatch.setattr(send_vault_log, "send_digest",
                        lambda html, subject, cfg, recipients=None: False)
    assert send_vault_log.main([]) == 1
    assert not send_vault_log._already_sent("2026-08-04")


def test_dry_run_neither_sends_nor_marks(vault, monkeypatch):
    _write(vault, "2026-08-04")
    monkeypatch.setattr(send_vault_log, "send_digest",
                        lambda *a, **k: pytest.fail("dry run must not send"))
    assert send_vault_log.main(["--dry-run"]) == 0
    assert not send_vault_log._already_sent("2026-08-04")


def test_marker_directory_is_created_on_demand(vault):
    _write(vault, "2026-08-04")
    assert not os.path.exists(send_vault_log.SENT_MARKER_DIR)
    send_vault_log._mark_sent("2026-08-04")
    assert os.path.exists(send_vault_log.SENT_MARKER_DIR)
