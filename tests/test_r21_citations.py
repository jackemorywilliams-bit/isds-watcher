"""The citation guard for the superseded validation record.

WHAT THIS IS. Production code, tests and scripts used to fail closed against a
document that has never existed as a file on any branch: the uncommitted record
the constant ``MARK`` below names. The council's ruling of 2026-09-13 held that
record superseded — not silently renamed — by
``analytics/locked_set/VALIDATION_RECORD.md``, cited in prose as *the validation
record*, and ordered every citation re-pointed with the loss stated on the face
of each file that carries one.

THE CLASSIFICATION IS THE ACCEPTANCE TEST. The ruling required every occurrence
to be classified, and required the classification itself to be the thing that
gets checked. ``TABLE`` below is that classification, committed as data:

  class ``a``  cites the candidate list or the design of the locked set
  class ``b``  cites a number or a threshold
  class ``c``  cites a design rationale or narrative

Classes ``a`` and ``c`` are re-pointed at the validation record. Class ``b`` is
NOT: a number is re-pointed at the number's surviving home in this repository —
``src/config.py``'s ``TRIAGE_COST_PER_CALL_USD``, ``rings.ClassifyState``, or
``analytics/state-space-resolution-2026-08-09.md`` — because pointing a live
number at a record that does not carry it is how the first citation rotted.

FAIL-CLOSED BEHAVIOUR, which is the whole point of the file:

  1. A new bare citation of the lost record anywhere under ``src/``, ``tests/``,
     ``scripts/`` or in ``PLAN.md`` fails the build. The only permitted
     occurrences of that name are inside the verbatim supersession note.
  2. A file that cites the validation record without carrying the supersession
     note, or that carries it more than once, fails.
  3. A class-``b`` anchor that stops resolving — the constant renamed, the enum
     moved, the memo deleted — fails.
  4. Any drift between ``TABLE`` and what the files actually say fails, in
     either direction: a citation added without a table row, or a row whose
     count no longer matches.

Nothing here asserts anything about runtime behaviour. Every occurrence it
covers is a comment or a docstring; none is a string compared, a path opened or
a guard key.
"""

import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]

# The verbatim supersession note the ruling fixed. The first occurrence in each
# file carries it; later occurrences in that file read "the validation record".
MARK = 'supersedes the uncommitted "R2.1 record", 2026-09-13'

# The citation's short form, and the new record's path.
PHRASE = "the validation record"
RECORD_PATH = "analytics/locked_set/VALIDATION_RECORD.md"

# The name of the lost record, as a pattern. Written as a regex so that this
# file does not itself contain the literal name outside MARK -- which is what
# lets the scanner below cover its own source without an exemption.
LOST_NAME = re.compile(r"R2\.1")

# Where a bare citation of the lost record is a build failure.
SCOPE_DIRS = ("src", "scripts", "tests")
SCOPE_FILES = ("PLAN.md",)

# The surviving homes a class-(b) citation may point at, and the check that each
# one still resolves. A dead anchor is as bad as the lost record.
ANCHORS = {
    "TRIAGE_COST_PER_CALL_USD": lambda: _defines("src/config.py",
                                                 "TRIAGE_COST_PER_CALL_USD"),
    "rings.ClassifyState": lambda: _defines("src/rings.py",
                                            "class ClassifyState"),
    "analytics/state-space-resolution-2026-08-09.md":
        lambda: (REPO / "analytics"
                 / "state-space-resolution-2026-08-09.md").is_file(),
}

# --------------------------------------------------------------------------- #
# THE CLASSIFICATION TABLE — one row per file in the systems-designer's scope.
#
#   path, class-(a) count, class-(b) count, class-(c) count,
#   the class-(b) anchors that file must carry
#
# (a) + (c) is the number of times that file cites the validation record; one of
# those citations carries MARK. (b) citations name no record at all.
# --------------------------------------------------------------------------- #
TABLE = (
    # path,                      a, b,  c, anchors
    ("PLAN.md",                  0, 0,  1, ()),
    ("scripts/check_lock.py",    1, 0,  0, ()),
    ("src/classify_v2.py",       0, 0,  1, ()),
    ("src/config.py",            0, 2,  2, ("TRIAGE_COST_PER_CALL_USD",)),
    ("src/headline_lane.py",     0, 0,  1, ()),
    ("src/main.py",              0, 1,  2, ("rings.ClassifyState",)),
    ("src/rings.py",             0, 5, 11,
     ("analytics/state-space-resolution-2026-08-09.md",)),
    ("src/triage.py",            0, 1,  2, ("TRIAGE_COST_PER_CALL_USD",)),
    ("tests/test_pipeline.py",   0, 0,  1, ()),
    ("tests/test_rings.py",      0, 1,  3,
     ("analytics/state-space-resolution-2026-08-09.md",)),
)

# The measurement this branch was cut from, recorded so a drift is legible
# rather than mysterious: 35 occurrences across 10 files in this scope, from
# `grep -rno -i "R2\.1" src tests scripts PLAN.md` at 66df2d2.
MEASURED_TOTAL = 35


def _defines(rel: str, needle: str) -> bool:
    path = REPO / rel
    return path.is_file() and needle in path.read_text(encoding="utf-8")


def _flatten(text: str) -> str:
    """Line wrapping must not hide a citation. Join wrapped comment lines.

    A citation that spans two comment lines is the same citation; a test that
    could not see it would be a test that rewards wrapping the note in half.
    """
    joined = re.sub(r"\s*\n\s*#?\s*", " ", text)
    return re.sub(r"\s+", " ", joined)


def _scope_files():
    """Every text file a bare citation could hide in, this file included."""
    out = []
    for name in SCOPE_FILES:
        path = REPO / name
        if path.is_file():
            out.append(path)
    for directory in SCOPE_DIRS:
        for path in sorted((REPO / directory).rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            out.append(path)
    return out


def _read(path: pathlib.Path):
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def test_the_scope_this_guard_claims_to_cover_actually_exists():
    """A guard pointed at a moved directory silently guards nothing."""
    for directory in SCOPE_DIRS:
        assert (REPO / directory).is_dir(), directory
    for name in SCOPE_FILES:
        assert (REPO / name).is_file(), name
    files = _scope_files()
    assert len(files) > 20, "scope collapsed to almost nothing"


def test_no_bare_citation_of_the_lost_record_survives_in_code():
    """The fail-closed half: a new bare citation is a BUILD failure.

    The lost record's name may appear in exactly one shape inside this scope --
    the verbatim supersession note, which exists to say the document was never
    committed. Anywhere else it is a live citation of a document nobody can
    read, and that is the defect this branch closed.

    Historical narrative is deliberately out of scope: `analytics/` and the
    vault keep the old name verbatim, because editing the record of a loss
    falsifies the record of the loss.
    """
    offenders = []
    for path in _scope_files():
        text = _read(path)
        if text is None or not LOST_NAME.search(text):
            continue
        flat = _flatten(text)
        bare = (len(LOST_NAME.findall(flat))
                - flat.lower().count(MARK.lower()))
        if bare:
            offenders.append(f"{path.relative_to(REPO)}: {bare} bare")
    assert not offenders, (
        "bare citations of the uncommitted record: " + "; ".join(offenders)
        + f" -- re-point them at {RECORD_PATH} (or, for a number, at the "
        "number's surviving home) per the ruling of 2026-09-13")


@pytest.mark.parametrize("rel,n_a,n_b,n_c,anchors", TABLE,
                         ids=[row[0] for row in TABLE])
def test_each_classified_file_cites_as_its_classes_require(
        rel, n_a, n_b, n_c, anchors):
    """The classification, enforced row by row.

    Three assertions per file, one per thing the ruling fixed: the citation
    count matches the classes claimed for it, the supersession note appears
    exactly once, and every number this file re-pointed has a home that still
    exists.
    """
    path = REPO / rel
    assert path.is_file(), rel
    flat = _flatten(path.read_text(encoding="utf-8")).lower()

    expected_citations = n_a + n_c
    assert flat.count(PHRASE) == expected_citations, (
        f"{rel}: expected {expected_citations} citations of the validation "
        f"record (class a={n_a}, c={n_c}), found {flat.count(PHRASE)}")

    if expected_citations:
        assert flat.count(MARK.lower()) == 1, (
            f"{rel}: the supersession note must appear exactly once -- on the "
            "first citation in the file; later ones read 'the validation "
            "record'")
        assert RECORD_PATH.lower() in flat, (
            f"{rel}: the citation must name {RECORD_PATH}")
    else:
        assert flat.count(MARK.lower()) == 0, (
            f"{rel}: carries the supersession note but cites nothing")

    assert len(anchors) == len(set(anchors))
    if n_b:
        assert anchors, f"{rel}: {n_b} class-(b) citations and no anchor named"
    for anchor in anchors:
        assert anchor.lower() in flat, f"{rel}: lost its anchor {anchor}"
        assert ANCHORS[anchor](), (
            f"{anchor} no longer resolves -- a class-(b) citation in {rel} "
            "now points at nothing, which is the failure this branch fixed")


def test_the_table_accounts_for_every_measured_occurrence():
    """The table is the measurement, not a summary of it.

    If the classification and the count disagree, the classification is wrong,
    and the ruling made the classification the acceptance test.
    """
    total = sum(row[1] + row[2] + row[3] for row in TABLE)
    assert total == MEASURED_TOTAL
    assert len(TABLE) == len({row[0] for row in TABLE})
    # Class (a) is the candidate list. Exactly one file in this scope cites it:
    # the lock checker, whose empty-state note explains why no item has been
    # recorded yet.
    assert sum(row[1] for row in TABLE) == 1
    assert [row[0] for row in TABLE] == sorted(row[0] for row in TABLE)


@pytest.mark.xfail(strict=True, reason=(
    "WHAT TO DO ABOUT THIS RESULT, in one line: if you are reading this as an "
    "XPASS(strict) FAILURE, analytics/locked_set/VALIDATION_RECORD.md has "
    "landed -- delete this @pytest.mark.xfail decorator (the decorator only, "
    "not the test) and the build goes green with the check now permanent. "
    "WHY IT IS HERE: the record is written by another seat on branch "
    "council/validation-record, so on the branch that re-pointed the citations "
    "the file it cites is not yet present and this test cannot pass. STRICT on "
    "purpose: the moment the record merges, this xfails no longer -- it "
    "XPASSes, a strict xfail turns an xpass into a FAILURE, and the build "
    "stops until the decorator is removed. That is the forcing function. A "
    "non-strict xfail would go quiet in both states, and an existence check "
    "that can never fail is the same defect this whole file exists to close, "
    "wearing a test's name."))
def test_the_record_every_citation_points_at_exists():
    """The citation must resolve to a real file, not to another absent memo.

    This is the assertion whose absence caused the defect. Every class-(a) and
    class-(c) row in TABLE points at one path; nothing checked that the path
    led anywhere, and for the record this one supersedes it never did.
    """
    record = REPO / RECORD_PATH
    assert record.is_file(), (
        f"{RECORD_PATH} does not exist, so every class-(a) and class-(c) "
        "citation listed in TABLE points at nothing -- exactly the defect this "
        "file was written to close. Either commit the record at that path, or "
        "re-point the citations at whatever superseded it and update TABLE.")

    text = record.read_text(encoding="utf-8")
    assert text.strip(), f"{RECORD_PATH} exists but is empty"
    assert MARK.split('"')[1] in text, (
        f"{RECORD_PATH} must name the record it supersedes in its provenance "
        "header. The citations in TABLE say this document replaces a record "
        "that was never committed; if the document itself does not say so, the "
        "supersession is undocumented at the only place a reader lands.")


def test_every_file_that_carries_the_note_is_in_the_table():
    """The other direction: no citation may exist off the books."""
    listed = {row[0] for row in TABLE}
    found = set()
    for path in _scope_files():
        text = _read(path)
        if text is None:
            continue
        rel = str(path.relative_to(REPO))
        if rel == str(pathlib.Path(__file__).relative_to(REPO)):
            continue  # the guard itself holds MARK as a constant
        if PHRASE in _flatten(text).lower():
            found.add(rel)
    assert found == listed, (
        f"unclassified citations: {sorted(found - listed)}; "
        f"table rows with no citation left: {sorted(listed - found)}")
