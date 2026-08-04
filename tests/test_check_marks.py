"""The Carrying-Span Rule has to break something, or it is prose that does not bind.

On 2026-08-03 three entries cited sources for propositions those sources do not
contain, under a rule that already existed. R5's finding was that rules bind in this
project when attached to an artifact that fails. These tests pin what that artifact
catches — R5 tiers 2, 3 and 5 — and, just as important, what it does not, so a green
run is never read as a verified bibliography.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from scripts import check_marks

REPO = Path(__file__).resolve().parent.parent


def _doc(*entries: str, note: str = "Each entry carries a verification statement.") -> str:
    body = "\n\n".join(entries)
    return (
        "# Memo\n\n## I. Scope\n\nProse that is not an entry.\n\n"
        f"## VII. Backsourced Annotated Bibliography\n\n{note}\n\n{body}\n"
    )


LEGACY = (
    "### Salini v. Morocco\n\n"
    "ICSID Case No. ARB/00/4, Decision on Jurisdiction (July 23, 2001).\n\n"
    "**Descriptive annotation.** The four-criteria test.\n\n"
    "**Backsourcing verification.** Located on italaw; ¶ 52 verified.\n\n"
    "**Relevance to the project.** The definitional baseline.\n"
)

# The four-mark form. Screened terms are all zero, so Amendment 2 is satisfied
# vacuously here; the nonzero branch gets its own tests below.
FOUR_MARK = (
    "### Some Tribunal v. Some State\n\n"
    "ICSID Case No. ARB/00/1, Award (Jan. 1, 2001).\n\n"
    "**P —** The tribunal treated municipal recognition as a precondition.\n\n"
    "**Q —** \"the right must first exist under municipal law\" ¶ 249\n\n"
    "**D —** Award, 1 Jan. 2001; a contract dispute; merits; decided against the "
    "claimant on this point.\n\n"
    "**V —** Checked 2026-08-04 at italaw. Screened: \"trade secret\": 0; "
    "\"TRIPS\": 0; \"municipal\": 0.\n"
)


def _swap(entry: str, old: str, new: str) -> str:
    assert old in entry, old
    return entry.replace(old, new)


# --- tier 2: mark parity --------------------------------------------------

def test_the_real_memos_pass():
    """The corpus this rule was written for must pass, or the check is unusable."""
    for name, expected in (("ferguson-memo.md", 21), ("kim-memo.md", 12)):
        r = check_marks.check_file(str(REPO / "lit-review" / name))
        assert r["violations"] == [], r["violations"]
        assert r["entries"] == expected
        assert r["with_statement"] == expected


def test_an_entry_with_no_verification_statement_fails():
    doc = _doc(LEGACY, "### Vanda Pharmaceuticals v. FDA\n\nD.D.C. 2021.\n\n"
                       "**Descriptive annotation.** A disclosure case.\n")
    r = check_marks.check_text(doc)
    assert len(r["violations"]) == 1
    assert "no verification statement" in r["violations"][0]["problem"]
    assert r["violations"][0]["entry"] == "Vanda Pharmaceuticals v. FDA"


def test_two_verification_statements_for_one_entry_fails():
    """A reader cannot tell which of two statements was the one actually checked."""
    doubled = LEGACY + "\n**Backsourcing verification.** Also checked elsewhere.\n"
    r = check_marks.check_text(_doc(doubled))
    assert len(r["violations"]) == 1
    assert "expected exactly 1" in r["violations"][0]["problem"]


def test_both_statement_forms_count_for_parity():
    """The memos predate the rule; their form is the promised statement too."""
    r = check_marks.check_text(_doc(LEGACY, FOUR_MARK))
    assert r["violations"] == []
    assert (r["entries"], r["with_statement"]) == (2, 2)
    assert (r["four_mark"], r["legacy"]) == (1, 1)


def test_the_violation_carries_a_line_number():
    """A failure a person cannot navigate to gets ignored."""
    doc = _doc("### Orphan\n\nNo statement here.\n")
    v = check_marks.check_text(doc)["violations"][0]
    assert doc.splitlines()[v["line"] - 1].strip() == "### Orphan"


@pytest.mark.parametrize("mark", ["P", "Q", "D", "V"])
def test_a_four_mark_entry_missing_any_mark_fails(mark):
    entry = "\n\n".join(p for p in FOUR_MARK.split("\n\n")
                        if not p.startswith(f"**{mark} —**"))
    r = check_marks.check_text(_doc(entry))
    assert any(f"missing the {mark} mark" in v["problem"] for v in r["violations"]), \
        r["violations"]


def test_dropping_p_does_not_escape_the_other_checks():
    """Gating the strict branch on P would let the author opt out of it.

    An entry that drops P and keeps a bare Q must still be held to Q's requirements —
    otherwise the strictness is elective by exactly the person it constrains.
    """
    entry = ("### Bare\n\nICSID Case No. ARB/00/2, Award (2002).\n\n"
             "**Q —** the tribunal said something\n")
    problems = " ".join(v["problem"] for v in check_marks.check_text(_doc(entry))["violations"])
    assert "missing the P mark" in problems
    assert "missing the D mark" in problems
    assert "no quoted span" in problems


@pytest.mark.parametrize("mark", ["P", "Q", "D", "V"])
def test_an_empty_mark_fails(mark):
    entry = FOUR_MARK
    for part in FOUR_MARK.split("\n\n"):
        if part.startswith(f"**{mark} —**"):
            entry = entry.replace(part, f"**{mark} —**")
    r = check_marks.check_text(_doc(entry))
    assert any(f"{mark} mark is empty" in v["problem"] for v in r["violations"]), \
        r["violations"]


# --- tier 2: the span itself ----------------------------------------------

def test_a_pinpoint_without_a_quoted_span_fails():
    """R5.2 requires a quotation pair AND a pinpoint. A locator with no words says
    where something is without saying what it was."""
    entry = _swap(FOUR_MARK, '**Q —** "the right must first exist under municipal law" ¶ 249',
                  "**Q —** see the discussion of municipal law ¶ 249")
    r = check_marks.check_text(_doc(entry))
    assert any("no quoted span" in v["problem"] for v in r["violations"]), r["violations"]


def test_a_quoted_span_without_a_pinpoint_fails():
    """A pinpoint alone is not compliance — and neither is a span alone."""
    entry = _swap(FOUR_MARK, '"the right must first exist under municipal law" ¶ 249',
                  '"the right must first exist under municipal law"')
    r = check_marks.check_text(_doc(entry))
    assert any("no pinpoint" in v["problem"] for v in r["violations"]), r["violations"]


@pytest.mark.parametrize("pin", ["¶ 249", "at 231", "p. 14", "art. 39(3)", "[abstract]",
                                 "paras. 12-14", "§ 4"])
def test_the_pinpoint_forms_this_corpus_uses_are_accepted(pin):
    entry = _swap(FOUR_MARK, "¶ 249", pin)
    assert check_marks.check_text(_doc(entry))["violations"] == []


@pytest.mark.parametrize("q", [
    "**Q —** *No span located.* Exit (i) taken: another document in the same matter.",
    "**Q —** The source could not be retrieved; it is unread and nothing is asserted from it.",
])
def test_a_named_exit_is_compliance_not_a_violation(q):
    """Clause 3's exits are the honest outcome, not a failure to be flagged."""
    entry = _swap(FOUR_MARK,
                  '**Q —** "the right must first exist under municipal law" ¶ 249', q)
    assert check_marks.check_text(_doc(entry))["violations"] == []


@pytest.mark.parametrize("q", [
    "**Q —** no exit was needed here",
    "**Q —** the exit sign was not relevant",
])
def test_the_word_exit_alone_does_not_buy_a_way_out(q):
    """A bare "exit" token would let a sentence that takes no exit bypass BOTH the
    quotation and the pinpoint check."""
    entry = _swap(FOUR_MARK,
                  '**Q —** "the right must first exist under municipal law" ¶ 249', q)
    problems = " ".join(v["problem"]
                        for v in check_marks.check_text(_doc(entry))["violations"])
    assert "no quoted span" in problems
    assert "no pinpoint" in problems


@pytest.mark.parametrize("pin", ["[TBD]", "[TK]", "[cite]", "[???]"])
def test_a_placeholder_is_not_a_pinpoint(pin):
    """"[TBD]" says a locator is owed, not where the words are."""
    entry = _swap(FOUR_MARK, "¶ 249", pin)
    r = check_marks.check_text(_doc(entry))
    assert any("no pinpoint" in v["problem"] for v in r["violations"]), r["violations"]


# --- tier 3: Amendment 2, nonzero-referent parity -------------------------

def test_a_nonzero_screened_term_with_no_referent_clause_fails():
    """The branch on which the 2026-08-03 failure actually occurred.

    Without this, "recognition: 2" reads as corroboration when both occurrences are
    about enforcement of arbitral awards.
    """
    entry = _swap(FOUR_MARK, '"municipal": 0', '"recognition": 2')
    r = check_marks.check_text(_doc(entry))
    assert any("nonzero count" in v["problem"] and "recognition" in v["problem"]
               for v in r["violations"]), r["violations"]


def test_a_referent_clause_satisfies_amendment_2():
    """The worked V line from the rule itself must pass."""
    entry = _swap(
        FOUR_MARK,
        '**V —** Checked 2026-08-04 at italaw. Screened: "trade secret": 0; '
        '"TRIPS": 0; "municipal": 0.',
        "**V —** Checked 2026-08-04 at italaw. Screened: TRIPS 0; intellectual "
        "property 0; recognition 2 — both occurrences concern recognition and "
        "enforcement of arbitral awards, not municipal recognition of a protected asset.",
    )
    assert check_marks.check_text(_doc(entry))["violations"] == []


def test_a_nonzero_term_that_is_the_source_of_q_needs_no_clause():
    """If the hit produced the span, the referent is already on the page."""
    entry = _swap(FOUR_MARK, '"municipal": 0', '"municipal": 3')
    assert check_marks.check_text(_doc(entry))["violations"] == []


def test_zero_counts_never_require_a_clause():
    assert check_marks.check_text(_doc(FOUR_MARK))["violations"] == []


def test_terms_after_the_first_dash_are_still_parsed():
    """Stopping at the first dash silently drops every later term — and the rule's own
    worked line puts a referent clause mid-line, so that is where terms will be."""
    terms = check_marks._screen_terms(
        "Screened: TRIPS 0 — nothing there; recognition 2.")
    assert ("recognition", 2) in terms


def test_the_rules_own_worked_v_line_parses():
    terms = check_marks._screen_terms(
        "checked 2026-08-04 at italaw; screened: TRIPS 0; intellectual property 0; "
        "recognition 2 — both occurrences concern recognition and enforcement of "
        "arbitral awards, not municipal recognition of a protected asset.")
    assert terms == [("TRIPS", 0), ("intellectual property", 0), ("recognition", 2)]


def test_a_citation_inside_the_screen_sentence_is_not_a_screened_term():
    """"Mem. Op. (D.D.C. May 6, 2021)" must not parse as the term "D.D.C" with count
    2021 — a phantom nonzero term would flag a compliant entry, and a checker that
    cries wolf is a checker nobody runs."""
    terms = check_marks._screen_terms(
        "Screened the document originally cited, 436 F. Supp. 3d 256: trade secret 0; "
        "confidential 0; proprietary 0; disclosure 0.")
    assert terms == [("trade secret", 0), ("confidential", 0),
                     ("proprietary", 0), ("disclosure", 0)]


def test_a_nonzero_term_on_a_continuation_line_is_still_caught():
    """Amendment 2 must not be defeated by a line break. Both the rule and the
    template display the V mark wrapped, so this is the normal case, not an edge."""
    entry = _swap(FOUR_MARK,
                  '**V —** Checked 2026-08-04 at italaw. Screened: "trade secret": 0; '
                  '"TRIPS": 0; "municipal": 0.',
                  "**V —** Checked 2026-08-04 at italaw. Screened: \"trade secret\": 0;\n"
                  "\"TRIPS\": 0; \"recognition\": 2.")
    r = check_marks.check_text(_doc(entry))
    assert any("recognition" in v["problem"] for v in r["violations"]), r["violations"]


def test_a_referent_clause_on_a_continuation_line_is_accepted():
    """The mirror failure: a compliant entry flagged because its clause wrapped."""
    entry = _swap(FOUR_MARK,
                  '**V —** Checked 2026-08-04 at italaw. Screened: "trade secret": 0; '
                  '"TRIPS": 0; "municipal": 0.',
                  "**V —** Checked 2026-08-04 at italaw. Screened: TRIPS 0;\n"
                  "recognition 2 — both occurrences concern recognition and\n"
                  "enforcement of arbitral awards, not the municipal kind.")
    assert check_marks.check_text(_doc(entry))["violations"] == []


def test_a_pinpoint_on_a_continuation_line_is_accepted():
    entry = _swap(FOUR_MARK,
                  '**Q —** "the right must first exist under municipal law" ¶ 249',
                  '**Q —** "the right must first exist under\nmunicipal law" ¶ 249')
    assert check_marks.check_text(_doc(entry))["violations"] == []


def test_a_blank_line_ends_a_mark():
    """Prose after a blank line belongs to the entry, not to the mark above it."""
    marks = check_marks._fold_marks(
        ["**P —** The proposition.", "continued here.", "",
         "**Descriptive annotation.** Unrelated prose with numbers 5."])
    assert marks["P"] == ["The proposition. continued here."]


@pytest.mark.parametrize("q", [
    "**Q —** Exit: dropped — the source carries nothing.",
    "**Q —** I took the fourth exit; the source was dropped.",
])
def test_the_other_exit_phrasings_are_accepted(q):
    """Exit (iv) had no recognised form of words, so an honest drop was flagged."""
    entry = _swap(FOUR_MARK,
                  '**Q —** "the right must first exist under municipal law" ¶ 249', q)
    assert check_marks.check_text(_doc(entry))["violations"] == []


@pytest.mark.parametrize("line,expected", [
    # The rule's own two worked rigid designators must be readable, or the check
    # cannot see a nonzero on the very term it tells the writer to screen.
    ("Screened: Art. 39(3) 4; TRIPS 0.", [("Art. 39(3)", 4), ("TRIPS", 0)]),
    ('Screened: "fork in the road (FITR)" 6.', [("fork in the road (FITR)", 6)]),
    # Ordinary English for a count.
    ("Screened: TRIPS 0; recognition 2 occurrences.", [("TRIPS", 0), ("recognition", 2)]),
    ("Screened: recognition: 2 hits.", [("recognition", 2)]),
    # Dates and citations are not screened terms, in any of their shapes.
    ("Screened in Mem. Op. (D.D.C. May 6, 2021): trade secret 0.", [("trade secret", 0)]),
    ("Screened 436 F. Supp. 3d 256: trade secret 0.", [("trade secret", 0)]),
    ("Screened: TRIPS 0. Read via govinfo, checked 2026-08-03.", [("TRIPS", 0)]),
    # A clause is not a term of art, however it ends.
    ("Screened: TRIPS 0. Annotation. The tribunal held at 249", [("TRIPS", 0)]),
])
def test_the_screen_parser_reads_terms_and_only_terms(line, expected):
    assert check_marks._screen_terms(line) == expected


def test_a_bold_disposition_is_not_dropped_from_the_d_mark():
    """"joined to the merits" is the phrase most likely to be bolded in a D mark —
    it is the disposition the rule exists to surface. Terminating a mark on any "**"
    would drop it silently and leave the entry passing."""
    folded = check_marks._fold_marks(
        ["**D —** Award, 2014; resort management; jurisdiction;",
         "**joined to the merits**, not decided."])
    assert "joined to the merits" in folded["D"][0]


def test_a_labelled_paragraph_does_end_the_mark():
    """"**Descriptive annotation.**" is a new paragraph, not a continuation — its
    prose must not be swallowed into the V mark and parsed for screened terms."""
    folded = check_marks._fold_marks(
        ["**V —** Checked. Screened: TRIPS 0.",
         "**Descriptive annotation.** The tribunal held at 249"])
    assert folded["V"] == ["Checked. Screened: TRIPS 0."]


def test_every_template_exemplar_can_be_read_by_amendment_2():
    """The synthetic exemplar's whole job is to demonstrate a nonzero term with a
    referent clause. If Amendment 2 cannot read it, it demonstrates nothing — which
    is how it first passed: vacuously."""
    blocks = _template_blocks()
    parsed = []
    for b in blocks:
        v = check_marks._fold_marks(b.splitlines())["V"]
        parsed.append(check_marks._screen_terms(v[0]) if v else [])
    assert any(count > 0 for terms in parsed for _, count in terms), \
        "no exemplar exercises the nonzero branch"
    assert check_marks.check_text(_doc(*blocks))["violations"] == []


def test_a_v_mark_with_no_screen_record_is_not_flagged():
    """Documented limit: step 2 is not policed here, so a V mark recording no screen
    passes. Pinned so the docstring's claim stays true."""
    entry = _swap(FOUR_MARK,
                  '**V —** Checked 2026-08-04 at italaw. Screened: "trade secret": 0; '
                  '"TRIPS": 0; "municipal": 0.',
                  "**V —** Checked 2026-08-04 at italaw.")
    r = check_marks.check_text(_doc(entry))
    assert r["violations"] == []
    assert r["screen_records"] == 0


# --- tier 5: degenerate uniformity ----------------------------------------

def test_identical_v_lines_across_entries_fail():
    """The only check in the set that detects performance directly (R5.5)."""
    second = _swap(FOUR_MARK, "### Some Tribunal v. Some State", "### Another v. Another")
    r = check_marks.check_text(_doc(FOUR_MARK, second))
    assert any("degenerate uniformity" in v["problem"] for v in r["violations"]), \
        r["violations"]


def test_identical_d_lines_across_entries_fail():
    """Two entries carding the same document, date, stage and outcome verbatim is
    the same signal: one card was written and reused."""
    second = _swap(_swap(FOUR_MARK, "### Some Tribunal v. Some State", "### Another v. Another"),
                   "Checked 2026-08-04 at italaw", "Checked 2026-08-04 at the ICSID site")
    r = check_marks.check_text(_doc(FOUR_MARK, second))
    assert [v["problem"] for v in r["violations"]] == [
        'D mark is byte-identical to the one on "Some Tribunal v. Some State" '
        "— degenerate uniformity (R5.5)"
    ]


def test_genuinely_distinct_entries_pass():
    second = _swap(
        _swap(_swap(FOUR_MARK, "### Some Tribunal v. Some State", "### Another v. Another"),
              "Checked 2026-08-04 at italaw", "Checked 2026-08-04 at the ICSID site"),
        "**D —** Award, 1 Jan. 2001; a contract dispute; merits; decided against the "
        "claimant on this point.",
        "**D —** Decision on Jurisdiction, 3 Mar. 2003; a concession dispute; "
        "jurisdiction; objection joined to the merits.")
    assert check_marks.check_text(_doc(FOUR_MARK, second))["violations"] == []


# --- scope: what this must NOT do -----------------------------------------

def test_prose_outside_the_bibliography_is_not_an_entry():
    """§§ I-VI are argument, not citations; flagging their headings would be noise."""
    assert check_marks.check_text(_doc(LEGACY))["entries"] == 1


def test_the_section_note_is_not_an_entry():
    r = check_marks.check_text(_doc(LEGACY, note="A note about verification, with no ###."))
    assert r["entries"] == 1


def test_a_following_section_ends_the_bibliography():
    doc = _doc(LEGACY) + "\n## VIII. Appendix\n\n### Not A Citation\n\nA table.\n"
    r = check_marks.check_text(doc)
    assert r["entries"] == 1
    assert r["violations"] == []


def test_fenced_examples_are_not_entries():
    """The template teaches the form in code fences; parsing those as real entries
    would make the template fail its own rule."""
    doc = _doc(LEGACY) + "\n```markdown\n### Illustrative Entry\n\nNo statement.\n```\n"
    r = check_marks.check_text(doc)
    assert r["entries"] == 1
    assert r["violations"] == []


def test_the_shipped_template_is_not_reported_as_checked():
    """It has a bibliography-shaped title and zero real entries."""
    r = check_marks.check_file(str(REPO / "lit-review" / "BIBLIOGRAPHY_TEMPLATE.md"))
    assert r["entries"] == 0
    assert r["violations"] == []


def _template_blocks() -> list[str]:
    src = (REPO / "lit-review" / "BIBLIOGRAPHY_TEMPLATE.md").read_text(encoding="utf-8")
    return [b for b in re.findall(r"```markdown\n(.*?)```", src, re.S)
            if b.lstrip().startswith("###")]


def test_the_templates_own_examples_pass_the_checker_they_teach():
    """Fence-skipping exempts the template's exemplars from the gate that will judge
    every copy of them. If an exemplar could not pass, the template teaches a form
    that fails — so unfence them and run the check for real."""
    blocks = _template_blocks()
    assert len(blocks) >= 2, "the template should carry at least two entry exemplars"
    r = check_marks.check_text(_doc(*blocks))
    assert r["violations"] == [], r["violations"]
    assert r["entries"] == len(blocks)


def test_the_templates_examples_pass_for_the_RIGHT_reason():
    """The test above passed vacuously once, when marks were read one physical line
    at a time: two-thirds of each wrapped mark was never read, so the exemplars
    cleared a gate that had not looked at them. Assert the marks were actually seen.
    """
    blocks = _template_blocks()
    wrapped = [b for b in blocks if "436 F. Supp. 3d 256" in b]
    assert wrapped, "expected the Vanda exemplar"
    marks = check_marks._fold_marks(wrapped[0].splitlines())
    # The V mark wraps across several lines; its last sentence must be in the content.
    assert "pending confirmation" in marks["V"][0]
    # And the screen record must parse to the four terms the memo attests.
    assert check_marks._screen_terms(marks["V"][0]) == [
        ("trade secret", 0), ("confidential", 0),
        ("proprietary", 0), ("disclosure", 0)]
    # The Q mark's exit language survives the fold rather than being truncated.
    assert "not yet recorded" in marks["Q"][0]


def test_a_bibliography_opened_at_h3_does_not_swallow_its_siblings():
    """Closing only on h2 would report "### III.C Something Else" as an entry with no
    verification statement — a false failure in a document that never had a
    bibliography at all."""
    doc = ("# Memo\n\n## III. Sources\n\n### A. Bibliography of works consulted\n\n"
           "Prose.\n\n### B. Research Methods\n\nMore prose.\n")
    r = check_marks.check_text(doc)
    assert r["violations"] == []


def test_a_memo_with_no_bibliography_is_out_of_scope_not_a_failure():
    r = check_marks.check_text("# Memo\n\n## I. Scope\n\nProse.\n")
    assert (r["entries"], r["violations"], r["has_section"]) == (0, [], False)


# --- failure modes of the checker itself ----------------------------------

def test_an_unreadable_file_is_a_violation_not_a_pass():
    """Reporting a file clean because it could not be opened is the failure mode
    this project has actually had (tool-status-as-source-state)."""
    r = check_marks.check_file(str(REPO / "lit-review" / "does-not-exist.md"))
    assert r["violations"] and "cannot read" in r["violations"][0]["problem"]


def test_an_empty_examination_is_not_reported_as_ok(tmp_path, capsys):
    """A zero-entry file must not print the same word a checked file prints."""
    f = tmp_path / "empty.md"
    f.write_text("# Notes\n\nNo bibliography here.\n", encoding="utf-8")
    assert check_marks.main(["check_marks", str(f)]) == 0
    out = capsys.readouterr().out
    assert "nothing checked" in out
    assert "ok —" not in out


def test_cli_exits_nonzero_on_violation_and_zero_when_clean(tmp_path):
    clean = tmp_path / "clean.md"
    clean.write_text(_doc(LEGACY), encoding="utf-8")
    assert check_marks.main(["check_marks", str(clean)]) == 0

    dirty = tmp_path / "dirty.md"
    dirty.write_text(_doc("### Orphan\n\nNothing.\n"), encoding="utf-8")
    assert check_marks.main(["check_marks", str(dirty)]) == 1


def test_cli_with_no_arguments_is_a_usage_error():
    assert check_marks.main(["check_marks"]) == 2


def test_the_count_is_not_called_verified(tmp_path, capsys):
    """R6 leaves entailment untouched; a field named "verified" would say otherwise,
    and the corpus it counts contains a statement that was itself wrong."""
    f = tmp_path / "m.md"
    f.write_text(_doc(LEGACY), encoding="utf-8")
    check_marks.main(["check_marks", str(f)])
    out = capsys.readouterr().out
    assert "carry a verification statement" in out
    assert "verified" not in out


# --- the limit, pinned ----------------------------------------------------

def test_a_pass_does_not_mean_the_spans_carry_their_propositions():
    """The limit of this check, pinned so a green run is never read as more.

    The entry below is well-formed under every mechanical tier implemented here and
    is still wrong on the point that matters: R6 records entailment as not closed,
    and annotation vagueness as having no mechanism at all. The checker passes it,
    and must — otherwise the report could be mistaken for substantive verification.
    """
    unfalsifiable = (
        "### A Law Review Article\n\n"
        "42 Some J. Int'l L. 231 (2021).\n\n"
        "**P —** This article is the strongest external critique of the "
        "recognition–enforceability gap.\n\n"
        "**Q —** \"tribunals inevitably apply domestic law\" p. 243\n\n"
        "**D —** Law review article, 2021; not a case; no procedural history.\n\n"
        "**V —** Checked 2026-08-04 at the publisher's repository. Screened: "
        "\"trade secret\": 0; \"TRIPS\": 0; \"patent\": 0.\n"
    )
    r = check_marks.check_text(_doc(unfalsifiable))
    assert r["violations"] == []
    assert r["four_mark"] == 1
    # The span says nothing about being strongest, or about a recognition-
    # enforceability gap. Nothing here detects that. R6: "leaves the judgement at the
    # centre exactly where it was."
