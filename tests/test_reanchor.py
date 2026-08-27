"""Tests for the mechanical re-anchor.

The point of reanchor.py is to end the two-year-old failure mode where the anchor
was moved by a model that was *told* to move it. So these tests pin the two ways a
mechanical mover could still be wrong: touching more than the first anchor (the
notes keep historical anchors below the current one), and drifting from the guard's
own notion of what an anchor and a date look like.
"""

from __future__ import annotations

import importlib.util
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(REPO, "scripts", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ra = _load("reanchor")
cc = _load("check_currency")


def test_shares_the_guards_regexes_not_a_copy():
    # If these were restated instead of imported, a change to the guard's anchor
    # form would silently desync the mover. reanchor must use the very objects of
    # the check_currency it imports (identity), and that module must be the guard
    # (same pattern). Cross-instance identity can't be used — the test loads its
    # own copy of the guard — so identity is checked against reanchor's own import.
    assert ra.ANCHOR_RE is ra._cc.ANCHOR_RE
    assert ra.UPDATED_RE is ra._cc.UPDATED_RE
    assert ra.TRACKED is ra._cc.TRACKED
    assert ra.ANCHOR_RE.pattern == cc.ANCHOR_RE.pattern
    assert ra.UPDATED_RE.pattern == cc.UPDATED_RE.pattern
    assert ra.TRACKED == cc.TRACKED


def test_moves_first_anchor_and_first_date():
    body = ("**Last updated:** 2026-08-01.\n"
            "*Audited against `aaaaaaa`.*\n")
    new, moved = ra._reanchor_body(body, "bbbbbbb", "2026-08-27")
    assert "`bbbbbbb`" in new
    assert "2026-08-27" in new
    assert "aaaaaaa" not in new and "2026-08-01" not in new
    assert len(moved) == 2


def test_leaves_historical_anchors_below_the_first_untouched():
    body = ("*Audited against `1111111`.*  <- current\n"
            "*Audited against `2222222`.*  <- history, must not move\n")
    new, _ = ra._reanchor_body(body, "9999999", "2026-08-27")
    assert new.count("9999999") == 1
    assert "2222222" in new           # the historical anchor is preserved
    assert "1111111" not in new       # only the first moved


def test_is_idempotent_once_at_head():
    body = "*Audited against `abcdef0`.*\n**Last updated:** 2026-08-27.\n"
    new, moved = ra._reanchor_body(body, "abcdef0", "2026-08-27")
    assert new == body
    assert moved == []


def test_reports_a_note_with_no_anchor_rather_than_inventing_one():
    body = "a note that forgot to say against what.\n"
    new, moved = ra._reanchor_body(body, "abcdef0", "2026-08-27")
    assert new == body
    assert any("NO ANCHOR" in m for m in moved)


def test_anchor_target_skips_maintenance_commits(monkeypatch):
    """The re-anchor commit is itself maintenance; if the target were HEAD, a
    re-run would chase its own commit forever. The target is the newest
    SUBSTANTIVE commit — which is exactly what the guard reads."""
    order = ["ccccccc", "bbbbbbb", "aaaaaaa"]  # rev-list is newest-first

    def fake_git(*a):
        if a[0] == "rev-list":
            return "\n".join(order)
        if a[:2] == ("rev-parse", "--short"):
            return a[2][:7]
        return ""

    monkeypatch.setattr(ra, "_git", fake_git)
    # The two newest are re-anchor (maintenance) commits; the third is real work.
    monkeypatch.setattr(ra._cc, "_is_maintenance",
                        lambda sha: sha in ("ccccccc", "bbbbbbb"))
    assert ra._anchor_target() == "aaaaaaa"
