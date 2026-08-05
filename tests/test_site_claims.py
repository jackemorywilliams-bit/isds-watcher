"""Guards on what the public site is allowed to claim.

Every assertion here corresponds to a statement that was published and was not
true. They are separated from test_pipeline.py deliberately: these do not test
that the machine works, they test that the machine does not overstate itself.

The banned-phrase scan is the important half. Prose drifts back; a wording that
took a review cycle to remove should cost a failing test to reintroduce.
"""

from __future__ import annotations

import importlib
import os
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "scripts" / "site_templates"


@pytest.fixture(scope="module")
def bs():
    sys.path.insert(0, os.path.join(str(REPO), "scripts"))
    return importlib.import_module("build_site")


# The eleven archived runs as of 2026-08-03, in date order. Kept literal so the
# expected sentence below can be read against real numbers rather than fixtures.
ARCHIVE = [
    {"date": "2026-06-09", "screened": 78, "accepted": 2, "matches": 0},
    {"date": "2026-06-10", "screened": 79, "accepted": 2, "matches": 0},
    {"date": "2026-06-15", "screened": 14, "accepted": 0, "matches": 0},
    {"date": "2026-06-16", "screened": 80, "accepted": 1, "matches": 0},
    {"date": "2026-06-22", "screened": 11, "accepted": 2, "matches": 0},
    {"date": "2026-06-29", "screened": 12, "accepted": 3, "matches": 0},
    {"date": "2026-07-06", "screened": 13, "accepted": 1, "matches": 0},
    {"date": "2026-07-13", "screened": 23, "accepted": 1, "matches": 0},
    {"date": "2026-07-20", "screened": 14, "accepted": 1, "matches": 0},
    {"date": "2026-07-27", "screened": 10, "accepted": 0, "matches": 0},
    {"date": "2026-08-03", "screened": 13, "accepted": 1, "matches": 0},
]


# --------------------------------------------------------------------------- #
# The archive readout
# --------------------------------------------------------------------------- #
def test_trend_readout_states_range_not_a_trend_or_a_cause(bs):
    """The series is 78,79,14,80,11,12,13,23,14,10,13 — not monotonic, maximum at
    the fourth run. No meta.json has ever recorded a deduplication quantity, so
    no causal explanation is available from the archive at all."""
    text = bs._trend_summary_text(ARCHIVE)
    assert text == (
        "Across 11 archived runs from 2026-06-09 to 2026-08-03, candidates "
        "evaluated ranged from 80 to 10 with no steady trend, the last seven "
        "between 10 and 23; matches stayed at zero and items surfaced totalled 14.")


def test_trend_readout_reports_matches_from_the_data(bs):
    """'matches stayed at zero' is a claim about the archive, not a constant."""
    rows = [dict(r) for r in ARCHIVE]
    rows[-1]["matches"] = 2
    text = bs._trend_summary_text(rows)
    assert "matches totalled 2" in text
    assert "stayed at zero" not in text


def test_trend_readout_handles_a_short_archive(bs):
    text = bs._trend_summary_text(ARCHIVE[:3])
    assert "3 archived runs" in text
    # With fewer runs than the recent window, the redundant clause is dropped.
    assert "the last" not in text
    assert bs._trend_summary_text([]) == "No runs archived yet."


def test_zero_match_baseline_label_is_conditional(bs):
    """The chart annotates 'matches = 0 throughout'. The first matching run must
    not publish that sentence."""
    svg_zero, _ = bs._build_trend_svg(ARCHIVE)
    assert "matches = 0 throughout" in svg_zero

    rows = [dict(r) for r in ARCHIVE]
    rows[0]["matches"] = 1
    svg_hit, _ = bs._build_trend_svg(rows)
    assert "matches = 0 throughout" not in svg_hit


# --------------------------------------------------------------------------- #
# Screen-reader text
# --------------------------------------------------------------------------- #
def test_chart_aria_labels_name_the_quantity_and_agree_in_number(bs):
    svg, _ = bs._build_trend_svg(ARCHIVE)
    labels = re.findall(r'aria-label="(20\d\d-\d\d-\d\d: [^"]*)"', svg)
    assert len(labels) == len(ARCHIVE)
    assert "2026-08-03: 13 candidates evaluated, 1 item surfaced, 0 matches" in labels
    for label in labels:
        # A bare count of "screened" tells a screen-reader user nothing about
        # what was screened, and "watch-list leads" mislabels matches+near-misses.
        assert "screened" not in label
        assert "watch-list" not in label
        # "1 items surfaced" is read aloud verbatim; \b keeps 11/21 out of it.
        assert not re.search(r"\b1 (items|candidates|matches)\b", label), label

    src, _ = bs._build_source_svg(
        [{"key": "iareporter_headlines", "screened": 63, "accepted": 1},
         {"key": "icsid", "screened": 4, "accepted": 0}])
    assert "63 candidates evaluated, 1 item surfaced" in src
    assert "4 candidates evaluated, 0 items surfaced" in src


def test_chart_titles_do_not_say_weekly(bs):
    """Eleven runs span 55 days and several fall on adjacent days."""
    svg, _ = bs._build_trend_svg(ARCHIVE)
    title = re.search(r"<title id=\"trend-title\">(.*?)</title>", svg, re.S).group(1)
    assert "eekly" not in title
    assert "archived run" in title


# --------------------------------------------------------------------------- #
# The homepage status line
# --------------------------------------------------------------------------- #
def test_archive_status_is_summed_from_the_record(bs):
    class D:
        def __init__(self, s, m, a):
            self.screened, self.matches, self.accepted = s, m, a

    digests = [D(r["screened"], r["matches"], r["accepted"]) for r in ARCHIVE]
    assert bs.archive_status(digests) == {
        "runs": 11, "screened": 347, "matches": 0, "surfaced": 14}
    assert bs.archive_status([]) == {
        "runs": 0, "screened": 0, "matches": 0, "surfaced": 0}
    # A run whose counts were never recorded must not crash the status line.
    assert bs.archive_status([D(None, None, None)])["screened"] == 0


# --------------------------------------------------------------------------- #
# Headline-only entries
# --------------------------------------------------------------------------- #
def test_headline_only_is_detected_from_the_notable_line(bs):
    def entry(notable):
        return bs.Entry(
            number=1, title="t", source="s", read_original_url="u", date="",
            url="u", relevance=25, band="WATCH", rings=[], ring_labels=[],
            tags=[], citation="", annotation="", notable_line=notable)

    assert entry("N/A — source paywalled (headline only); body not accessible.").headline_only
    assert entry("  N/A").headline_only
    assert not entry("The tribunal found that the trademark rights were exploited.").headline_only
    assert not entry("").headline_only


# --------------------------------------------------------------------------- #
# Phrases that must not come back
# --------------------------------------------------------------------------- #
BANNED = [
    # Contradicted by RELEVANCE_FLOOR, select_surfaced, and two archived runs
    # that surfaced nothing at all.
    ("never empty", "the report is guaranteed non-empty"),
    ("always included so", "the strongest are always surfaced"),
    # Product copy, not research reporting.
    ("impossible to miss", "promotional"),
    # Unfalsifiable from the archive: no meta.json records a dedup quantity.
    ("deduplication matured", "unevidenced causal claim"),
    ("steady trickle", "10 of the 14 items came in the first six runs"),
    # One review cycle exists, covering three research-record claims; no digest
    # entry and no site sentence has ever been human-verified.
    ("no claim is published as fact without", "universal human-verification claim"),
    # The public surface describes model passes, not a standing body.
    ("research council", "implies independent expert corroboration"),
    ("AI research council", "implies independent expert corroboration"),
]


def _public_sources() -> list[Path]:
    return sorted(TEMPLATES.glob("*.j2")) + [REPO / "scripts" / "build_site.py"]


@pytest.mark.parametrize("phrase,why", BANNED)
def test_retired_claims_stay_retired(phrase, why):
    hits = []
    for path in _public_sources():
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            # The banned-phrase list in this test file is not itself a claim;
            # only the site sources are scanned.
            if phrase.lower() in line.lower():
                hits.append(f"{path.relative_to(REPO)}:{i}: {line.strip()}")
    assert not hits, f"retired claim reintroduced ({why}):\n" + "\n".join(hits)


@pytest.mark.xfail(
    strict=True,
    reason="KNOWN CONTRADICTION, not yet authorised for repair. The how-it-works "
           "prose now describes model passes, but the workflow chart inlined on "
           "that same page still labels its third column THE AI RESEARCH COUNCIL "
           "and names role cards 'Chairman', 'Integrity officer', 'Analytics "
           "officer' and 'Meeting minutes'. The chart's sources are "
           "views/isds-workflow-3d/workflow.json and "
           "tools/isds-workflow-3d/src/render-config.mjs, which belong to other "
           "seats; regenerating it is 'npm run render-static' + 'npm run build'. "
           "When that is done, delete this marker — strict=True makes the test "
           "fail loudly once it starts passing.")
def test_workflow_chart_agrees_with_the_page_it_sits_on():
    svg = (TEMPLATES / "assets" / "workflow.svg").read_text(encoding="utf-8")
    assert "council" not in svg.lower()
    assert "officer" not in svg.lower()


def test_how_it_works_carries_the_shared_error_caveat():
    """The sentence that makes the rest of the AI-workflow description honest.
    It is required to be present, and required not to be hidden in a footnote."""
    text = (TEMPLATES / "how_it_works.html.j2").read_text(encoding="utf-8")
    assert "not independent researchers" in text
    for element in ("source material", "prompt lineage", "model family",
                    "framing assumptions", "same errors"):
        assert element in text, f"shared-error caveat lost '{element}'"
    assert 'class="caveat"' in text


def test_how_it_works_states_the_real_review_count():
    text = (TEMPLATES / "how_it_works.html.j2").read_text(encoding="utf-8")
    assert "remain provisional" in text
    assert "2026-07-18" in text, "the one logged review cycle must be dated"
    assert "three claims" in text
    assert "No digest entry" in text


def test_homepage_carries_the_status_line():
    text = (TEMPLATES / "index.html.j2").read_text(encoding="utf-8")
    assert "Exploratory research prototype" in text
    assert "Validation is preliminary" in text
    # Generated from the archive, never written by hand.
    for token in ("status.runs", "status.screened", "status.matches"):
        assert token in text, f"status line hardcodes what should be {token}"
