"""The numbers this project states about itself are written down more than once.

Three of them had drifted by 2026-08-04: the backtest corpus listed 8 of 16 labelled
negatives (so the site said 12 cases / 0.92 while the holdout harness said 20 / 0.95),
fingerprint.yaml's combination_rules described a "subtotal >= 30" bar the code has
never had, and all seven few-shot expected_score values were wrong under a test that
asserted only the band. These tests pin that the guard catches that shape, that it
fails rather than skips when a declared claim goes missing, and that it does not
report clean because it could not read its inputs.
"""

from __future__ import annotations

import pytest

from scripts import check_claims
from scripts.check_claims import Fact, Ref


# --- the repository as it stands --------------------------------------------

# Two disagreements are live on main, both owned by seats other than the guard's
# author, both named by the guard with file:line. Naming them here rather than
# asserting a clean run means FIXING either one keeps this test green, while any NEW
# drift fails it. Asserting the exact problem list instead would have to be edited on
# the way to a green tree, which is how a baked-in defect becomes permanent.
KNOWN = {
    "digest threshold",                 # src/config.py _DEFAULT_THRESHOLD = 60 vs 40
    "completed human-review cycles",    # HUMAN_REVIEW.md contradicts its own log
}


def _failing_facts(problems: list[str]) -> set[str]:
    return {p.split(":", 1)[0] for p in problems}


def test_no_disagreement_beyond_the_two_that_are_known_and_owned_elsewhere():
    assert _failing_facts(check_claims.check()) <= KNOWN, check_claims.check()


def test_the_holdout_numbers_agree_everywhere():
    """The 2026-08-04 defect, made impossible: the corpus must list every labelled
    holdout item, so the backtest page and the holdout harness score the same set."""
    problems = [p for p in check_claims.check() if p.startswith("holdout")]
    assert problems == []


def test_the_two_harnesses_report_the_same_holdout():
    """Stated directly, not only through the registry, because this is the invariant
    the site's headline metric rests on."""
    a = check_claims._holdout_metrics()
    b = check_claims._backtest_metrics()
    assert a["n"] == b["n"] == 20
    assert a["n_pos"] == b["n_pos"] == 4
    assert a["n_neg"] == b["n_neg"] == 16
    for metric in ("precision", "recall", "accuracy", "f1"):
        assert round(a[metric], 2) == round(b[metric], 2), metric


# --- scope discipline, made mechanical --------------------------------------

def test_the_registry_stays_small():
    """A guard that grew until it needed its own reviewer would be the thing it was
    built to prevent. Fifteen is the declared ceiling; passing it is a decision."""
    assert len(check_claims.REGISTRY) <= 15


def test_every_fact_names_exactly_one_authority_and_at_least_one_mirror():
    for fact in check_claims.REGISTRY:
        assert isinstance(fact.authority, Ref), fact.name
        assert fact.mirrors, f"{fact.name}: an authority nothing restates checks nothing"


def test_no_two_facts_share_a_name():
    names = [f.name for f in check_claims.REGISTRY]
    assert len(names) == len(set(names))


# --- reading values ----------------------------------------------------------

@pytest.mark.parametrize("word,expected", [
    ("twelve", 12), ("forty", 40), ("twenty-five", 25), ("Four", 4), ("sixteen", 16),
    ("40", 40), ("0.86", 0.86),
])
def test_numbers_are_read_from_digits_and_from_words(word, expected):
    assert check_claims._number(word, "x") == expected


def test_a_number_word_the_table_does_not_know_fails_rather_than_passing_unread():
    with pytest.raises(check_claims.Unreadable):
        check_claims._number("a dozen", "METHODOLOGY.md:47")


# --- the drift shape, replayed in a miniature repo ---------------------------

@pytest.fixture()
def repo(tmp_path):
    """A miniature project: one constant, one YAML restatement, one line of prose."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "classify.py").write_text(
        "# header\nPRESENT_FLOOR = 12\n", encoding="utf-8")
    (tmp_path / "fingerprint.yaml").write_text(
        "rules:\n  - \"reaches the present floor (12)\"\n", encoding="utf-8")
    (tmp_path / "METHODOLOGY.md").write_text(
        "It counts once its subtotal reaches a floor of twelve.\n", encoding="utf-8")
    return tmp_path


FLOOR = Fact(
    "present floor",
    Ref("src/classify.py", r"(?m)^PRESENT_FLOOR = (\d+)"),
    (Ref("fingerprint.yaml", r"present floor \((\d+)\)"),
     Ref("METHODOLOGY.md", r"reaches a floor of ([a-z]+)")),
)


def test_a_consistent_repo_passes(repo):
    assert check_claims.check((FLOOR,), repo) == []


def test_a_yaml_restatement_that_drifts_from_the_code_fails(repo):
    (repo / "fingerprint.yaml").write_text(
        "rules:\n  - \"reaches the present floor (30)\"\n", encoding="utf-8")
    problems = check_claims.check((FLOOR,), repo)
    assert len(problems) == 1
    assert "src/classify.py:2 says 12" in problems[0]
    assert "fingerprint.yaml:2 says 30" in problems[0]


def test_prose_that_drifts_from_the_code_fails(repo):
    (repo / "METHODOLOGY.md").write_text(
        "It counts once its subtotal reaches a floor of thirty.\n", encoding="utf-8")
    problems = check_claims.check((FLOOR,), repo)
    assert len(problems) == 1
    assert "METHODOLOGY.md:1 says 30" in problems[0]


def test_a_declared_claim_that_vanished_fails_rather_than_passing_on_an_empty_search(repo):
    """Prose gets rewritten. A registry entry that now matches nothing has stopped
    checking anything, and reporting that as clean is tool-status-as-source-state."""
    (repo / "METHODOLOGY.md").write_text(
        "A ring must earn its place before it counts.\n", encoding="utf-8")
    problems = check_claims.check((FLOOR,), repo)
    assert len(problems) == 1
    assert "nothing in METHODOLOGY.md matches the declared pattern" in problems[0]


def test_an_authority_that_contradicts_itself_fails(repo):
    (repo / "src" / "classify.py").write_text(
        "PRESENT_FLOOR = 12\nPRESENT_FLOOR = 18\n", encoding="utf-8")
    problems = check_claims.check((FLOOR,), repo)
    assert any("authority disagrees with itself" in p for p in problems)


def test_every_occurrence_is_checked_not_just_the_first(repo):
    """A number restated twice in one file can drift on the second mention."""
    (repo / "METHODOLOGY.md").write_text(
        "It reaches a floor of twelve. Later: it reaches a floor of thirty.\n",
        encoding="utf-8")
    problems = check_claims.check((FLOOR,), repo)
    assert len(problems) == 1 and "says 30" in problems[0]


# --- the non-regex modes -----------------------------------------------------

def test_count_mode_counts_matches_and_asserts_mode_reads_a_standing_sentence(tmp_path):
    (tmp_path / "LOG.md").write_text(
        "_Nothing has been logged yet._\n\n### 2026-07-18 — COMPLETED\n",
        encoding="utf-8")
    fact = Fact(
        "cycles",
        Ref("LOG.md", r"(?m)^###[^\n]*\bCOMPLETED\b", mode="count"),
        (Ref("LOG.md", r"_Nothing has been logged yet", asserts=0),),
    )
    problems = check_claims.check((fact,), tmp_path)
    assert len(problems) == 1
    assert "says 1" in problems[0] and "says 0" in problems[0]

    # The stale sentence is not repaired by qualifying it — the pattern still matches
    # and still asserts 0, which is the point: the words have to go.
    (tmp_path / "LOG.md").write_text(
        "_Nothing has been logged yet_ was true until July.\n\n"
        "### 2026-07-18 — COMPLETED\n", encoding="utf-8")
    assert len(check_claims.check((fact,), tmp_path)) == 1

    # Removed outright, the registry entry now matches nothing and says so rather than
    # passing: a person must re-point it at whatever sentence replaced it.
    (tmp_path / "LOG.md").write_text(
        "One cycle is complete.\n\n### 2026-07-18 — COMPLETED\n", encoding="utf-8")
    problems = check_claims.check((fact,), tmp_path)
    assert len(problems) == 1
    assert "nothing in LOG.md matches the declared pattern" in problems[0]


def test_files_mode_counts_the_archive_on_disk(tmp_path):
    (tmp_path / "digests").mkdir()
    for name in ("2026-06-09.html", "2026-06-10.html", "README.md"):
        (tmp_path / "digests" / name).write_text("x", encoding="utf-8")
    (tmp_path / "report.md").write_text("Across **3** archived runs.\n", encoding="utf-8")
    fact = Fact(
        "archived runs",
        Ref("digests/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html", mode="files"),
        (Ref("report.md", r"Across \*\*(\d+)\*\* archived run"),),
    )
    problems = check_claims.check((fact,), tmp_path)
    assert len(problems) == 1 and "says 2" in problems[0] and "says 3" in problems[0]


# --- failure modes of the checker itself -------------------------------------

def test_a_missing_file_is_an_error_not_a_pass(repo):
    (repo / "METHODOLOGY.md").unlink()
    with pytest.raises(check_claims.Unreadable):
        check_claims.check((FLOOR,), repo)


def test_a_harness_that_will_not_run_is_an_error_not_a_pass(monkeypatch):
    def boom():
        raise RuntimeError("holdout_set.json is gone")
    monkeypatch.setitem(check_claims._HARNESS, "scripts/eval_holdout.py", boom)
    fact = Fact("holdout items",
                Ref("scripts/eval_holdout.py", "n", mode="harness"),
                (Ref("scripts/backtest.py", "n", mode="harness"),))
    with pytest.raises(check_claims.Unreadable):
        check_claims.check((fact,), check_claims.REPO)


def test_cli_exit_codes(repo, monkeypatch):
    monkeypatch.setattr(check_claims, "REPO", repo)
    monkeypatch.setattr(check_claims, "REGISTRY", (FLOOR,))
    assert check_claims.main(["check_claims"]) == 0

    (repo / "fingerprint.yaml").write_text(
        "rules:\n  - \"reaches the present floor (30)\"\n", encoding="utf-8")
    assert check_claims.main(["check_claims"]) == 1

    (repo / "src" / "classify.py").unlink()
    assert check_claims.main(["check_claims"]) == 2
