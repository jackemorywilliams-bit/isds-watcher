"""Tests for the fourth guard.

Encoded here are the three defects the guard was built against and the two
defects the guard itself had while being built. Both sets matter: a guard that
cries wolf is discarded, and a discarded guard verifies nothing.
"""

from __future__ import annotations

import importlib.util
import os

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "check_sources", os.path.join(REPO, "scripts", "check_sources.py"))
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)


# --- the alteration forms legal writing uses, which are not fabrication ----

@pytest.mark.parametrize("span,source_form", [
    ("[e]ven if it were so", "Even if it were so"),
    ("[t]he legal characterization", "The legal characterization"),
    ("the [ICSID] Convention", "the Convention"),
    ("were discontinued pursuant to the applicants' requests,",
     "were discontinued pursuant to the applicants' requests"),
    ("A quoted sentence.", "a quoted sentence"),
])
def test_lawful_alterations_still_match(span, source_form):
    assert cs._for_match(span) in cs._for_match(source_form)


def test_substance_change_does_not_match():
    """The allowances are for form. A changed word must still fail."""
    assert cs._for_match("the tribunal granted relief") not in \
        cs._for_match("the tribunal denied relief")


# --- the two bugs the guard itself shipped with -------------------------

def test_curly_quotes_are_delimiters_not_content():
    """First version normalised the source but not the memo, so every curly
    quote shifted the pairing and it reported 51 of 51 missing."""
    spans, warns = cs.quoted_spans(
        '“this is a sufficiently long quoted span here”')
    assert [s for s, _ in spans] == \
        ["this is a sufficiently long quoted span here"]
    assert not warns


def test_unbalanced_line_is_warned_not_silently_mispaired():
    spans, warns = cs.quoted_spans('he said "one long enough quoted span here')
    assert spans == []
    assert warns and "odd number of quote marks" in warns[0]


def test_damage_from_one_bad_line_does_not_cross_paragraphs():
    body = ('he said "an unterminated span long enough to count\n'
            '"a genuinely quoted span of sufficient length"\n')
    spans, warns = cs.quoted_spans(body)
    assert [s for s, _ in spans] == \
        ["a genuinely quoted span of sufficient length"]
    assert len(warns) == 1


def test_multi_quote_line_marks_spans_ambiguous():
    """Text between two quotations is indistinguishable, to a regex, from a
    quotation. Such spans must not be asserted as MISSING."""
    body = ('"the first quoted span goes here" and then '
            '"the second quoted span goes here"')
    spans, _ = cs.quoted_spans(body)
    assert spans, "expected spans"
    assert all(certain is False for _, certain in spans)


def test_single_pair_line_is_certain():
    spans, _ = cs.quoted_spans('"the only quoted span on this line here"')
    assert spans == [("the only quoted span on this line here", True)]


# --- fail-closed, which is the whole point ------------------------------

def test_missing_source_fails_and_does_not_skip():
    checked, failed, msgs = cs.check_memo(
        "lit-review/kim-memo.md", "does_not_exist.pdf", "Nonexistent", False)
    assert failed == 1, "a missing source must FAIL, never skip"
    assert checked == 0
    assert any("declared source is missing" in m for m in msgs)


def test_missing_memo_fails():
    _, failed, msgs = cs.check_memo(
        "lit-review/no_such_memo.md", "x.pdf", "X", False)
    assert failed == 1
    assert any("memo not found" in m for m in msgs)


# --- the allowlist must not become a place to bury failures -------------

def test_every_allowlist_entry_states_a_reason():
    for span, reason in cs.ALLOW.items():
        assert len(reason) > 40, f"allowlist entry needs a real reason: {span}"
        assert ".md" in reason, \
            f"allowlist reason must cite where the span lives: {span}"


def test_declared_sources_exist_or_the_guard_would_be_vacuous():
    """Not an assertion that the PDFs are present -- seeds/ is gitignored and
    CI will not have them. It asserts the guard knows about both memos, so a
    memo cannot be quietly dropped from coverage."""
    assert set(cs.SOURCES) == {
        "lit-review/kim-memo.md", "lit-review/ferguson-memo.md"}
