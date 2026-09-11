"""Tests for the CI wiring itself — which guard runs, in which workflow, in what
order, and triggered by which paths.

WHY THIS FILE EXISTS SEPARATELY. Two defects on 2026-09-10 had the same shape:
a guard that was wired somewhere nobody re-read.

  1. The `currency` job sat in pipeline-guards.yml with no ordering relation to
     reanchor.yml, which moves the anchors it reads. Both fired on the same push,
     so the guard read the anchors while the mover was still computing the commit
     that fixes them, and every council merge went red and green again seconds
     later. A red that is routinely false is a red nobody reads.
  2. NOTHING ran the whole test suite. Every pytest invocation in every workflow
     named specific files. The wiring had already drifted from the path filters in
     two measured places: tests/test_source_recovery.py is in pipeline-guards'
     filters with no step that runs it, and tests/test_source_health.py is in
     neither the filters nor any step of any workflow. A test nothing runs is
     documentation.

These assertions do NOT live in tests/test_reanchor.py, where they started. That
file is run by reanchor.yml's own `reanchor` job, and the `currency` job below it
is skipped — and therefore reported as SUCCESS by GitHub — whenever `reanchor`
does not succeed. So a failure of these assertions there would have disarmed the
currency guard as a side effect of firing. Here they have two independent homes
that are not the mover: pipeline-guards' `suite` job and reanchor.yml's
`currency` job.

PLAIN-TEXT ASSERTIONS, no PyYAML import. reanchor.yml's jobs install only pytest.
"""

from __future__ import annotations

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(REPO, ".github", "workflows")


def _workflow(name: str) -> str:
    with open(os.path.join(WORKFLOWS, name), encoding="utf-8") as fh:
        return fh.read()


# --- the currency guard runs BEHIND the re-anchor, not beside it --------------
def test_currency_guard_is_a_job_of_reanchor_ordered_behind_the_mover():
    """Pins the four things that make the ordering real. Three of them are
    one-line expressions a future edit could "tidy" without seeing what they
    carry."""
    text = _workflow("reanchor.yml")

    # 1 — the job exists here, and `needs` is the first thing it declares.
    parts = text.split("\n  currency:\n", 1)
    assert len(parts) == 2, "reanchor.yml must define a `currency` job"
    job = parts[1]
    assert job.startswith("    needs: reanchor\n"), \
        "the currency job must declare `needs: reanchor` before anything else"

    # 2 — it still runs when the mover was SKIPPED (a fork PR, whose token cannot
    #     push), and never when the mover FAILED. `always()` alone would do both.
    flat = re.sub(r"\s+", " ", job)
    assert ("always() && (needs.reanchor.result == 'success' "
            "|| needs.reanchor.result == 'skipped')") in flat, \
        "the fork-PR path (reanchor skipped) must still be guarded"

    # 3 — it checks out the head BRANCH BY NAME with full history. The default
    #     pull_request checkout is the merge ref computed when the event fired,
    #     which does not contain the re-anchor commit the mover just pushed —
    #     ordering the jobs would fix nothing if this one read the old tree.
    assert "fetch-depth: 0" in job
    assert "github.event.pull_request.head.ref || github.ref_name" in flat, \
        "the currency job must resolve the same head ref the mover pushed to"

    # 4 — the guard itself, unrelaxed: its own tests first, then the guard, and
    #     nothing that lets a failure through.
    assert "python -m pytest tests/test_check_currency.py -q" in job
    assert "python scripts/check_currency.py" in job
    assert "continue-on-error" not in job

    # And it is gone from where it used to be, path filters included — two entries
    # that existed only to trigger a job that no longer lives in that file.
    guards = _workflow("pipeline-guards.yml")
    assert not re.search(r"^  currency:", guards, re.M), \
        "the currency job must not be defined in two workflows"
    assert '- "scripts/check_currency.py"' not in guards
    assert '- "tests/test_check_currency.py"' not in guards


def test_reanchor_has_no_paths_filter_so_the_checkers_tests_always_run():
    """The load-bearing reason deleting those two path entries was safe.

    scripts/check_currency.py and tests/test_check_currency.py were in
    pipeline-guards' filters so that a change to the checker would run the
    checker's own tests. The job moved to a workflow that has NO `paths:` filter
    at all, so it already runs on every PR — the entries were redundant, not
    load-bearing. Add a `paths:` filter to reanchor.yml and that stops being true
    silently: the checker's own tests would no longer run on changes to the
    checker, which is the one change most able to break it."""
    on_block = _workflow("reanchor.yml").split("\njobs:")[0]
    assert not re.search(r"^\s+paths(-ignore)?:", on_block, re.M), \
        ("reanchor.yml must not acquire a paths filter: the currency job's "
         "trigger coverage is what replaced the two deleted path entries")


# --- something runs the whole suite -------------------------------------------
def test_pipeline_guards_runs_the_entire_test_suite():
    text = _workflow("pipeline-guards.yml")

    parts = text.split("\n  suite:\n", 1)
    assert len(parts) == 2, "pipeline-guards.yml must define a `suite` job"
    job = parts[1]

    # The command itself, exactly. A `-k` or a second `--ignore` creeping in here
    # would recreate the named-subset problem in the one job that exists to end it.
    assert "python -m pytest tests -q --ignore=tests/test_one_pagers.py" in job, \
        "the suite job must run the whole tests/ tree"
    assert "-k " not in job, "the suite job must not filter to a named subset"
    assert job.count("--ignore=") == 1, \
        "one exclusion only: tests/test_one_pagers.py needs the gitignored seeds/"
    assert "continue-on-error" not in job

    # Independent of the per-guard job: a suite failure must not hide behind, or
    # wait on, the named steps that exist to say which guard broke.
    assert not re.search(r"^    needs:", job, re.M), \
        "the suite job must not depend on `guards`"

    # It must be able to run the app's tests, not merely collect them; and on full
    # history, because three tests in tests/test_check_currency.py reach for real
    # history and RETURN QUIETLY when they cannot find it — on a shallow checkout
    # they would pass without asserting anything.
    assert "pip install -r requirements.txt pytest pyyaml" in job
    assert "fetch-depth: 0" in job


def test_the_suite_is_triggered_by_the_code_it_covers():
    """Before 2026-09-10, src/source_health.py could change without triggering
    any workflow at all, and the workflow files themselves triggered only one
    another by name."""
    on_block = _workflow("pipeline-guards.yml").split("\njobs:")[0]
    for entry in ('- "src/**"', '- "scripts/**"', '- "tests/**"',
                  '- "templates/**"', '- "requirements.txt"',
                  '- "fingerprint.yaml"', '- ".github/workflows/**"'):
        assert entry in on_block, f"path filter must include {entry}"


def test_every_test_file_is_reachable_by_some_workflow():
    """The defect that produced the suite job, stated as a standing assertion
    rather than a fixed list: every tests/*.py must either be named by a step in
    some workflow or be swept up by the suite job's whole-tree run. This passes
    trivially while the suite job exists — which is the point. It fails the day
    someone narrows the suite back to a named subset and leaves a test file with
    no runner, which is exactly how tests/test_source_health.py came to have
    none."""
    names = {f for f in os.listdir(os.path.join(REPO, "tests"))
             if f.startswith("test_") and f.endswith(".py")}
    assert names, "no test files found; the glob is wrong"

    steps = "\n".join(_workflow(f) for f in sorted(os.listdir(WORKFLOWS))
                      if f.endswith((".yml", ".yaml")))
    sweeps_whole_tree = "python -m pytest tests -q" in steps

    unreachable = sorted(
        n for n in names
        if n != "test_one_pagers.py" and f"tests/{n}" not in steps
    )
    assert sweeps_whole_tree or not unreachable, (
        "these test files are named by no workflow step and no job runs the "
        f"whole tree: {unreachable}"
    )
