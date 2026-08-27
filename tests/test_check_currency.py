"""Tests for the fifth guard.

The guard exists because "everything is up to date" was asserted repeatedly and was
repeatedly false. These tests encode the four claim shapes it checks and the two ways
a currency guard can itself lie: by passing a note that makes no claim, and by
skipping a check it cannot perform.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "check_currency", os.path.join(REPO, "scripts", "check_currency.py"))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)


def _head() -> str:
    return subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


# --- the four claim shapes it must recognise --------------------------------

def test_anchor_regex_matches_the_form_the_vault_actually_uses():
    body = "*Audited against `b76f6c3`; paths: `.claude/agents/`, `prompts/`.*"
    assert cc.ANCHOR_RE.findall(body) == ["b76f6c3"]


def test_anchor_regex_matches_unbackticked_and_capitalised():
    assert cc.ANCHOR_RE.findall("Audited against d43c8d0 (main, clean)") == ["d43c8d0"]


def test_last_updated_regex():
    assert cc.UPDATED_RE.findall("**Last updated:** 2026-08-05") == ["2026-08-05"]


def test_pr_cite_regex_matches_the_form_that_was_wrong():
    """`373cce6`, PR #60 — it merged via PR #59. This is the shape that lied."""
    assert cc.PR_CITE_RE.findall("- **Closed** — `373cce6`, PR #59.") == [("373cce6", "59")]


# --- git predicates must be real, not assumed -------------------------------

def test_head_is_an_ancestor_of_itself():
    assert cc._is_ancestor(_head())


def test_a_fabricated_sha_is_not_a_commit():
    assert not cc._exists("deadbee")


def test_a_fabricated_sha_is_not_an_ancestor():
    assert not cc._is_ancestor("deadbee")


def test_commits_since_head_is_empty():
    assert cc._commits_since(_head(), ["METHODOLOGY.md"]) == []


def test_commits_since_an_older_sha_is_not_empty():
    """A guard that always returns 'no drift' would pass everything silently."""
    parent = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD~5"],
                            capture_output=True, text=True).stdout.strip()
    if parent:
        assert cc._commits_since(parent, ["."]) != []


# --- fail-closed ------------------------------------------------------------

def test_every_tracked_note_declares_at_least_one_path():
    """An empty path list makes drift detection vacuous — it can never fail."""
    for note, paths in cc.TRACKED.items():
        assert paths, f"{note} declares no audit paths; its anchor would check nothing"


def test_tracked_notes_exist():
    for note in cc.TRACKED:
        assert os.path.exists(os.path.join(REPO, note)), \
            f"{note} is tracked for currency but does not exist"


def test_declared_paths_exist():
    """Fail-closed: a path that has moved means the anchor measures nothing."""
    for note, paths in cc.TRACKED.items():
        for p in paths:
            assert os.path.exists(os.path.join(REPO, p)), \
                f"{note} declares audit path {p!r}, which does not exist"


# --- maintenance / bookkeeping commits do not count as drift ----------------

def _with_fake_show(monkeypatch, files: str):
    """Make _is_maintenance see `files` as the commit's changed-file list."""
    monkeypatch.setattr(cc, "_git", lambda *a: files)


def test_a_notes_only_commit_is_maintenance(monkeypatch):
    """The close-out re-anchor commit touches only tracked notes; excluded."""
    _with_fake_show(monkeypatch, "STATE_OF_THE_ANSWER.md\nagents/Claim Map.md")
    assert cc._is_maintenance("x") is True


def test_a_sent_marker_only_commit_is_maintenance(monkeypatch):
    """daily-update.yml commits .sent/ markers to main several times a day; a
    marker-only commit records that an email went out and stales nothing."""
    _with_fake_show(monkeypatch, "analytics/daily-research/.sent/2026-08-27")
    assert cc._is_maintenance("x") is True


def test_markers_mixed_with_notes_is_still_maintenance(monkeypatch):
    _with_fake_show(monkeypatch,
                    "STATE_OF_THE_ANSWER.md\nanalytics/daily-research/.sent/2026-08-27")
    assert cc._is_maintenance("x") is True


def test_one_real_file_among_markers_still_counts(monkeypatch):
    """A commit touching even one file of substance is not maintenance."""
    _with_fake_show(monkeypatch,
                    "analytics/daily-research/.sent/2026-08-27\nsrc/main.py")
    assert cc._is_maintenance("x") is False


def test_an_empty_commit_is_not_maintenance(monkeypatch):
    _with_fake_show(monkeypatch, "")
    assert cc._is_maintenance("x") is False


def test_a_substantive_analytics_commit_is_not_maintenance(monkeypatch):
    """A real analytics record (not a .sent/ marker) must still count as drift."""
    _with_fake_show(monkeypatch, "analytics/daily-research/2026-08-27-record.json")
    assert cc._is_maintenance("x") is False


def test_check_returns_a_nonzero_claim_count():
    """If the guard checked nothing it would report 0 failures and mean nothing —
    the exact failure mode check_sources.py shipped with."""
    checked, _failed, _msgs = cc.check()
    assert checked > 0, "the guard checked zero claims; it would pass vacuously"


# --- the maintenance exclusion, and the deadlock it resolves ----------------

def test_a_note_only_commit_is_maintenance():
    """Anchors live inside the notes they date, so counted naively the anchor
    would have to name its own commit and no committed tree could ever pass.
    A commit changing nothing but tracked notes cannot alter audited substance."""
    sha = subprocess.run(
        ["git", "-C", REPO, "log", "--format=%h",
         "--diff-filter=M", "--", *cc.TRACKED],
        capture_output=True, text=True).stdout.split()
    note_only = None
    for s in sha:
        changed = subprocess.run(
            ["git", "-C", REPO, "show", "--name-only", "--format=", s],
            capture_output=True, text=True).stdout.split("\n")
        files = {l.strip() for l in changed if l.strip()}
        if files and files <= set(cc.TRACKED):
            note_only = s
            break
    if note_only is None:
        return  # history holds no such commit yet; nothing to assert against
    assert cc._is_maintenance(note_only)


def test_a_substantive_commit_is_not_maintenance():
    """A commit touching any file outside the tracked notes must still count."""
    head = _head()
    changed = subprocess.run(
        ["git", "-C", REPO, "show", "--name-only", "--format=", head],
        capture_output=True, text=True).stdout.split("\n")
    files = {l.strip() for l in changed if l.strip()}
    if files and not (files <= set(cc.TRACKED)):
        assert not cc._is_maintenance(head)
