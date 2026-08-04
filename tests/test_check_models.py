"""A seat's model is asserted in three places; nothing compared them until now.

Two failures happened for real. `939deaa` moved seats off Fable and updated the
roster table but not the card mirror, so five cards read "Claude Fable 5" for days.
And `systems-designer` / `site-experience` carried cards asserting "Claude Opus 5"
while declaring no `model:` key at all — accidentally true, because the invoking
session happened to be Opus 5. Both were caught by a person reading carefully. These
tests pin that the guard catches them instead, and that it does not cry wolf on the
card that legitimately names a family where the code pins a dated build.
"""

from __future__ import annotations

import json

import pytest

from scripts import check_models


# --- the repository as it stands --------------------------------------------

def test_the_repo_is_consistent_today():
    assert check_models.check() == []


def test_both_seats_the_operator_named_now_declare_a_model():
    """Emory's 2026-08-04 answer: both are on opus, version Opus 5."""
    for seat in ("systems-designer", "site-experience"):
        assert check_models.declared_model(seat) == "opus", seat


def test_every_card_seat_that_is_a_subagent_declares_a_model():
    for node, _ in check_models.card_models().items():
        seat = check_models.NODE_TO_SEAT.get(node, node)
        if (check_models.DEFS_DIR / f"{seat}.md").exists():
            assert check_models.declared_model(seat) is not None, seat


# --- normalisation and matching ---------------------------------------------

@pytest.mark.parametrize("prose,expected", [
    ("Claude Opus 4.8", "claude-opus-4-8"),
    ("Claude Opus 5", "claude-opus-5"),
    ("Claude Haiku 4.5", "claude-haiku-4-5"),
    ("  Claude   Fable 5  ", "claude-fable-5"),
])
def test_prose_model_names_normalise_to_code_ids(prose, expected):
    assert check_models.normalise(prose) == expected


def test_a_card_may_name_the_family_where_the_code_pins_a_dated_build():
    """The classifier card reads "Claude Haiku 4.5" against
    claude-haiku-4-5-20251001. That is a description, not drift."""
    known = {"claude-haiku-4-5-20251001", "claude-opus-5"}
    assert check_models.names_a_known_model("claude-haiku-4-5", known)


def test_a_prefix_must_stop_at_a_hyphen_boundary():
    """Otherwise "claude-opus-4" would silently satisfy "claude-opus-4-8" and a card
    naming the wrong minor version would pass."""
    known = {"claude-opus-4-8"}
    assert check_models.names_a_known_model("claude-opus-4-8", known)
    assert not check_models.names_a_known_model("claude-opus-4", known)


def test_a_retired_model_matches_nothing():
    """The Fable case: the name is well-formed and configured nowhere."""
    known = {"claude-opus-5", "claude-opus-4-8"}
    assert not check_models.names_a_known_model("claude-fable-5", known)


# --- the two historical failures, replayed ----------------------------------

@pytest.fixture()
def repo(tmp_path, monkeypatch):
    """A miniature project with one seat, wired the way the real one is."""
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    (tmp_path / "agents").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "views" / "isds-workflow-3d").mkdir(parents=True)
    (tmp_path / "src" / "models.py").write_text(
        'CHAIRMAN_MODEL = "claude-opus-5"\nUTILITY_MODEL = "claude-opus-4-8"\n',
        encoding="utf-8")
    monkeypatch.setattr(check_models, "REPO", tmp_path)
    monkeypatch.setattr(check_models, "DEFS_DIR", tmp_path / ".claude" / "agents")
    monkeypatch.setattr(check_models, "VAULT_DIR", tmp_path / "agents")
    monkeypatch.setattr(check_models, "MODELS_PY", tmp_path / "src" / "models.py")
    monkeypatch.setattr(check_models, "FLOWCHART",
                        tmp_path / "views" / "isds-workflow-3d" / "workflow.json")
    return tmp_path


def _wire(repo, *, card: str, frontmatter: str | None, vault: str | None = None):
    fm = f"name: seat\n{f'model: {frontmatter}' if frontmatter else ''}\n"
    (repo / ".claude" / "agents" / "seat.md").write_text(
        f"---\n{fm}---\n\nBody.\n", encoding="utf-8")
    if vault is not None:
        (repo / "agents" / "seat.md").write_text(
            f"# Seat\n\n**Model.** `{vault}` — declared in the definition.\n",
            encoding="utf-8")
    (repo / "views" / "isds-workflow-3d" / "workflow.json").write_text(
        json.dumps({"nodes": [{"id": "seat", "meta": f"Model: {card}"}]}),
        encoding="utf-8")


def test_a_card_naming_a_retired_model_fails(repo):
    """939deaa: the roster moved off Fable and the card mirror did not."""
    _wire(repo, card="Claude Fable 5", frontmatter="opus")
    problems = check_models.check()
    assert any("appears nowhere in src/models.py" in p for p in problems), problems


def test_a_card_asserting_a_model_with_no_declared_key_fails(repo):
    """The systems-designer / site-experience case: an assertion true only while the
    invoking session happens to match."""
    _wire(repo, card="Claude Opus 5", frontmatter=None)
    problems = check_models.check()
    assert any("no mechanism" in p for p in problems), problems


def test_a_vault_note_contradicting_its_card_fails(repo):
    _wire(repo, card="Claude Opus 5", frontmatter="opus", vault="claude-opus-4-8")
    problems = check_models.check()
    assert any("disagreeing" in p for p in problems), problems


def test_a_consistent_seat_passes(repo):
    _wire(repo, card="Claude Opus 5", frontmatter="opus", vault="claude-opus-5")
    assert check_models.check() == []


def test_a_card_for_something_that_is_not_a_seat_is_not_flagged(repo):
    """Machine cards (the relay, the emailer) name no subagent and must not be held
    to a definition that does not exist."""
    _wire(repo, card="Claude Opus 5", frontmatter="opus")
    (repo / ".claude" / "agents" / "seat.md").unlink()
    assert check_models.check() == []


# --- failure modes of the checker itself ------------------------------------

def test_an_unreadable_flowchart_is_an_error_not_a_pass(repo, capsys):
    (repo / "views" / "isds-workflow-3d" / "workflow.json").write_text(
        "{not json", encoding="utf-8")
    assert check_models.main(["check_models"]) == 2


def test_a_models_file_with_no_ids_does_not_report_clean(repo):
    """Reporting every card fine because the reference set came back empty is
    tool-status-as-source-state."""
    (repo / "src" / "models.py").write_text("# nothing here\n", encoding="utf-8")
    _wire(repo, card="Claude Opus 5", frontmatter="opus")
    problems = check_models.check()
    assert problems and "cannot check" in problems[0]


def test_cli_exit_codes(repo):
    _wire(repo, card="Claude Opus 5", frontmatter="opus")
    assert check_models.main(["check_models"]) == 0
    _wire(repo, card="Claude Fable 5", frontmatter="opus")
    assert check_models.main(["check_models"]) == 1
