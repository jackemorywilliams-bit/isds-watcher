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


# A FROZEN fixture: the eleven archived runs as of 2026-08-03, in date order. Kept
# literal so the expected readout sentences below can be asserted verbatim. It is
# NOT the live archive — that is read by collect_digests(), and any test about what
# the site currently states must use the live archive, never this list.
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

    # The per-source chart counts FRESH candidates, not screening events, and its
    # aria-labels say so: "63 candidates evaluated" here would report the wrong
    # quantity to the one reader who cannot see the legend.
    src, _ = bs._build_source_svg(
        [{"key": "iareporter_headlines", "fresh": 63, "accepted": 1},
         {"key": "icsid", "fresh": 4, "accepted": 0}])
    assert "63 fresh candidates, 1 item surfaced" in src
    assert "4 fresh candidates, 0 items surfaced" in src
    assert "evaluated" not in src


def test_chart_titles_do_not_say_weekly(bs):
    """Eleven runs span 55 days and several fall on adjacent days."""
    svg, _ = bs._build_trend_svg(ARCHIVE)
    title = re.search(r"<title id=\"trend-title\">(.*?)</title>", svg, re.S).group(1)
    assert "eekly" not in title
    assert "archived run" in title


# --------------------------------------------------------------------------- #
# The archive counters
#
# Every number the site states about the archive comes from archive_status(), and
# every one of them was, until 2026-09-10, ALSO written by hand somewhere else.
# The hand-written copies said eleven runs and 347 screenings: true through
# 2026-08-03, wrong from 2026-08-10, and published on the same page as the live
# 16/492 for five weeks. These tests hold the two halves together — the function
# must measure the committed archive, and no template may state the answer itself.
# --------------------------------------------------------------------------- #
def _entry(bs, url, rings):
    return bs.Entry(
        number=1, title="t", source="s", read_original_url=url, date="",
        url=url, relevance=25, band="WATCH", rings=list(rings), ring_labels=[],
        tags=[], citation="", annotation="", notable_line="")


def _digest(bs, date, screened, matches, accepted, entries=()):
    return bs.Digest(
        date=date, slug=f"{date}_ISDS-Thematic-Watch", title="", summary_html="",
        entries=list(entries), surfaced=len(entries), accepted=accepted,
        matches=matches, screened=screened)


# Measured from the archive as committed, 2026-09-10 — sixteen meta.json files and
# seventeen article files. Written out so a reader can check the numbers against
# the repository rather than against the function that computes them.
COMMITTED = {"runs": 16, "screened": 492, "matches": 0, "surfaced": 17,
             "distinct": 16, "rings_zero": 7, "rings_one": 8, "contradictory": 1}


def test_archive_status_measures_the_committed_archive(bs):
    """The eight numbers, on the real archive. The council's Rule 1 figures are
    16 runs / 492 screened / 0 matches / 17 surfaced; the ring split is 7 with no
    ring, 8 with one, and one development published twice with different rings
    (italaw.com/cases/12153, 2026-06-09 and 2026-06-10)."""
    status = bs.archive_status(bs.collect_digests())
    assert {k: status[k] for k in COMMITTED} == COMMITTED
    # The five item buckets partition the distinct developments exactly: nothing
    # is double-counted and nothing falls out.
    assert (status["rings_zero"] + status["rings_one"] + status["rings_many"]
            + status["contradictory"]) == status["distinct"]
    # 'surfaced' counts published ENTRIES (meta.json), 'distinct' counts the
    # developments they describe. The gap is the duplicate, and it is exactly one.
    assert status["surfaced"] - status["distinct"] == 1


def test_archive_status_sums_the_run_counts(bs):
    digests = [_digest(bs, r["date"], r["screened"], r["matches"], r["accepted"])
               for r in ARCHIVE]
    status = bs.archive_status(digests)
    assert (status["runs"], status["screened"], status["matches"],
            status["surfaced"]) == (11, 347, 0, 14)
    empty = bs.archive_status([])
    assert all(v == 0 for v in empty.values())
    # A run whose counts were never recorded must not crash the status line.
    assert bs.archive_status([_digest(bs, "2026-01-01", None, None, None)])["screened"] == 0


def test_a_page_published_twice_with_different_rings_is_contradictory_not_counted_twice(bs):
    """The instrument's own published evidence on classification stability. It
    must not be resolved by preferring a reading, and it must not be counted in
    both ring buckets — which is what 'six with a ring and six with none' out of
    thirteen did before this function existed."""
    url = "https://example.test/case/1"
    a = _digest(bs, "2026-01-01", 10, 0, 1, [_entry(bs, url, ["judicial_or_regulatory_measure"])])
    b = _digest(bs, "2026-01-02", 10, 0, 1, [_entry(bs, url, [])])
    status = bs.archive_status([a, b])
    assert status["distinct"] == 1
    assert status["contradictory"] == 1
    assert status["rings_zero"] == status["rings_one"] == status["rings_many"] == 0
    # The same page twice with the SAME reading is one settled development.
    c = _digest(bs, "2026-01-02", 10, 0, 1,
                [_entry(bs, url, ["judicial_or_regulatory_measure"])])
    agreed = bs.archive_status([a, c])
    assert (agreed["distinct"], agreed["contradictory"], agreed["rings_one"]) == (1, 0, 1)


def test_two_rings_do_not_land_in_the_one_ring_bucket(bs):
    status = bs.archive_status([_digest(bs, "2026-01-01", 5, 0, 1, [
        _entry(bs, "https://example.test/a", ["ip_as_investment",
                                              "judicial_or_regulatory_measure"])])])
    assert (status["rings_many"], status["rings_one"], status["rings_zero"]) == (1, 0, 0)


# The counter literals that were live on 2026-09-10, with the run they stopped
# being true on. A template may not contain any of them again, in any page: they
# are answers, and the template's job is to ask.
STALE_COUNTERS = [
    ("347", "screenings through 2026-08-03; 492 by 2026-09-07"),
    ("11 runs", "runs archived through 2026-08-03; 16 by 2026-09-07"),
    ("eleven", "the run count in words"),
    ("thirteen", "distinct developments through 2026-08-03; 16 by 2026-09-07"),
    ("fourteen", "published entries through 2026-08-03; 17 by 2026-09-07"),
]


@pytest.mark.parametrize("literal,why", STALE_COUNTERS)
def test_no_template_writes_an_archive_count_by_hand(literal, why):
    hits = []
    for path in sorted(TEMPLATES.glob("*.j2")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if literal in line.lower():
                hits.append(f"{path.relative_to(REPO)}:{i}: {line.strip()[:120]}")
    assert not hits, (
        f"a template states an archive count by hand ({literal} — {why}); render it "
        f"from `status` so it cannot drift:\n" + "\n".join(hits))


# --------------------------------------------------------------------------- #
# The binding itself: every archive count on the site must MOVE when the archive
# moves. A literal that happens to be right today passes every other test in this
# file; only a render against a different archive tells the two apart.
# --------------------------------------------------------------------------- #
def _render_with_status(bs, template_name, status, **ctx):
    env = bs.make_env()
    env.globals["status"] = status
    return env.get_template(template_name).render(**ctx)


FICTION = {"runs": 7654, "screened": 8765, "matches": 9876, "surfaced": 6543,
           "distinct": 5432, "rings_zero": 4321, "rings_one": 3219,
           "rings_many": 2198, "contradictory": 1987}


def test_index_counts_follow_the_archive_and_are_not_written_in(bs):
    real = bs.archive_status(bs.collect_digests())
    page = _render_with_status(bs, "index.html.j2", FICTION,
                               active="home", root="", digests=[],
                               ring_labels=bs.RING_LABELS)
    # Every fabricated number must reach the page …
    for key in ("runs", "screened", "matches"):
        assert str(FICTION[key]) in page, f"index.html.j2 does not render status.{key}"
    # … and no real archive number may survive a render that was never given it.
    assert f"{real['runs']} runs across {real['screened']}" not in page
    assert f"{real['screened']} screenings" not in page


def test_the_shared_score_legend_follows_the_archive(bs):
    """base.html.j2 carries the band explainer inlined into EVERY page — the
    audit missed it twice because it is inside a <script> block."""
    page = _render_with_status(bs, "index.html.j2", FICTION,
                               active="home", root="", digests=[],
                               ring_labels=bs.RING_LABELS)
    assert f"of the {FICTION['distinct']} distinct developments" in page
    assert f"{FICTION['rings_zero']} are in this state" in page
    assert f"{FICTION['rings_one']} others carry one ring" in page
    assert f"three rings in {FICTION['runs']} runs across {FICTION['screened']}" in page


def test_backtest_screening_count_follows_the_archive(bs):
    real = bs.archive_status(bs.collect_digests())
    page = _render_with_status(bs, "backtest.html.j2", FICTION,
                               active="backtest", root="", bt=bs.run_backtest())
    assert f"no item has reached 40 in {FICTION['screened']} screenings" in page
    assert f"{real['screened']} screenings" not in page


# --------------------------------------------------------------------------- #
# Two denominators, two names
#
# meta.json's `screened` counts every candidate a run evaluated. `per_source`
# counts only the ones the seen-state had never seen (src/main.py:
# `per_source = len(fresh)`). Over the eleven runs that carry per-source data they
# are 191 and 230 — and the archive page printed both under one heading,
# "Candidates evaluated", on the same page. That is the protocol's fixed term for
# meta["screened"], so the per-source figure is the one that had to be renamed.
# --------------------------------------------------------------------------- #
PER_SOURCE_LABELS_BANNED = ["candidates evaluated", "candidate evaluated",
                            "screened", "evaluated"]


def test_the_two_denominators_really_do_differ(bs):
    """Stated as a measurement so the rename cannot quietly become cosmetic: if
    these ever coincide, the distinction still exists and the labels still must."""
    digests = bs.collect_digests()
    with_per_source = [d for d in digests if d.per_source]
    assert len(with_per_source) == 11
    assert sum(sum(d.per_source.values()) for d in with_per_source) == 191
    assert sum(d.screened or 0 for d in with_per_source) == 230
    assert sum(d.screened or 0 for d in digests) == 492


def test_per_source_rows_are_keyed_fresh_so_a_template_cannot_call_them_screened(bs):
    rows = bs.build_archive_charts(bs.collect_digests()).source_rows
    assert rows, "the archive carries per-source data; this test is not vacuous"
    for row in rows:
        assert "fresh" in row
        assert "screened" not in row, (
            "a per_source figure must not be reachable in a template as .screened — "
            "that name belongs to meta.json's run total")


def test_the_per_source_chart_is_never_labelled_candidates_evaluated(bs):
    """The chart, its accessible name, its per-row aria-labels and its worded
    readout are all per_source-derived, and none of them may borrow the run
    total's vocabulary."""
    rows = bs.build_archive_charts(bs.collect_digests()).source_rows
    svg, summary = bs._build_source_svg(rows)
    for blob, what in ((svg, "the per-source SVG"), (summary, "the worded readout")):
        low = blob.lower()
        for banned in PER_SOURCE_LABELS_BANNED:
            assert banned not in low, f"{what} calls a per_source figure '{banned}'"
    assert "fresh candidate" in svg.lower()


def test_the_archive_pages_source_block_says_fresh(bs):
    """The template half. The source figure is rendered in three places on the
    archive page — legend, caption, and the screen-reader data table — and the
    trend block directly above it legitimately says 'Candidates evaluated', so
    the scan is scoped to the source block rather than the file."""
    text = (TEMPLATES / "digest_index.html.j2").read_text(encoding="utf-8")
    start = text.index("{% if charts.has_source %}")
    block = text[start:text.index("{% endif %}", start)]
    # Only the LABELS — the legend key, the caption title and the data-table
    # column heads. Prose that contrasts the two quantities has to be able to
    # name the other one.
    labels = [ln.strip() for ln in block.splitlines()
              if "chart-key " in ln or "chart-caption-title" in ln
              or '<th scope="col">' in ln]
    assert labels, "the per-source block has no labels to check — the scan broke"
    for line in labels:
        assert "candidates evaluated" not in line.lower(), (
            f"a per-source label reads {line!r}; 'candidates evaluated' names "
            "meta.json's run total, which is a different and larger number")
    assert "r.screened" not in block, "a per_source figure is bound as .screened"
    assert "Fresh candidates" in block
    assert "r.fresh" in block
    # And the page must SAY they are different, not merely use two words.
    assert "never seen before" in block


def test_the_homepage_defines_its_own_denominator(bs):
    page = _render_with_status(bs, "index.html.j2", FICTION, active="home", root="",
                               digests=[], ring_labels=bs.RING_LABELS)
    for fragment in ("candidates evaluated</strong> summed over",
                     "digests/*/meta.json",
                     "not a count of pipeline runs",
                     "distinct candidates"):
        assert fragment in page, f"the status strip no longer defines 492: {fragment!r}"
    assert f"{FICTION['screened']} is the number of" in page


def test_one_run_reads_as_one_run(bs):
    """'1 runs' is read aloud verbatim by a screen reader."""
    one = dict(FICTION, runs=1)
    page = _render_with_status(bs, "index.html.j2", one, active="home", root="",
                               digests=[], ring_labels=bs.RING_LABELS)
    assert "in 1 run across" in page and "in 1 runs across" not in page


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


# --------------------------------------------------------------------------- #
# The backtest page's vocabulary
#
# "Out-of-sample" describes a sampling relationship the holdout does not have: the
# twenty items were chosen by hand from cases the author already knew, not drawn
# from the population the instrument screens. "Held-out" is the claim that is
# actually supported — these were kept out of development. And "on-theme" /
# "off-theme" named the LABEL as though it were a property of the case, when it is
# a judgement someone recorded in scripts/holdout_set.json.
# --------------------------------------------------------------------------- #
RETIRED_BACKTEST_WORDS = ["out-of-sample", "on-theme", "off-theme"]


@pytest.mark.parametrize("word", RETIRED_BACKTEST_WORDS)
def test_the_backtest_page_does_not_reclaim_a_sampling_property(word):
    text = (TEMPLATES / "backtest.html.j2").read_text(encoding="utf-8")
    hits = [f"{i}: {ln.strip()[:110]}"
            for i, ln in enumerate(text.splitlines(), 1) if word in ln.lower()]
    assert not hits, f"backtest.html.j2 says '{word}':\n" + "\n".join(hits)


def test_the_backtest_page_still_binds_every_measured_value(bs):
    """The wording change must not have touched a single number. Every bt.*
    binding the page had before is still there, and the page still renders."""
    text = (TEMPLATES / "backtest.html.j2").read_text(encoding="utf-8")
    for binding in ("bt.threshold", "bt.holdout.total", "bt.holdout.tp",
                    "bt.holdout.fp", "bt.holdout.tn", "bt.holdout.fn",
                    "bt.holdout.n_pos", "bt.holdout.n_neg", "bt.holdout.cases",
                    "c.label", "c.score", "c.band", "c.miss_kind"):
        assert binding in text, f"backtest.html.j2 lost the {binding} binding"
    page = _render_with_status(bs, "backtest.html.j2",
                               bs.archive_status(bs.collect_digests()),
                               active="backtest", root="", bt=bs.run_backtest())
    assert "Labelled positive" in page and "Labelled negative" in page
    assert "exploratory" in page


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
    svg = (TEMPLATES / "assets" / "workflow.svg.j2").read_text(encoding="utf-8")
    assert "council" not in svg.lower()
    assert "officer" not in svg.lower()


# --------------------------------------------------------------------------- #
# The delivery disclosure
# --------------------------------------------------------------------------- #
def test_the_delivery_pause_is_disclosed_and_matches_the_configuration():
    """A page describing weekly deliverables implies they arrive somewhere. They
    do not: the recipient list was narrowed by hand to the operator while the
    status-only gate holds. The disclosure is prose, so this test pins it to the
    configuration it describes — restore the second recipient, or turn the gate
    off, and the sentence has to be rewritten before the tree goes green."""
    from src import config
    assert len(config.RECIPIENTS) == 1, (
        "the recipient list has changed; the delivery disclosure on the "
        "how-it-works page and in README.md now describes a state that has passed")
    assert config.VALIDATION_STATUS_ONLY, (
        "item-level publication has resumed; the delivery disclosure must be "
        "rewritten rather than left standing")
    for path in (TEMPLATES / "how_it_works.html.j2", REPO / "README.md"):
        # Both files hard-wrap their prose, so the sentence is matched with
        # whitespace collapsed rather than line by line.
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
        assert "delivered to the operator alone" in text, path.name
        assert "paused until the classifier has been validated" in text, path.name
        assert "deliberate" in text, path.name


def test_no_public_surface_says_a_deliverable_goes_to_a_named_person():
    """The recipient is a private individual, and until 2026-09-10 the workflow
    chart said two of the weekly emails were "sent to Dr. Benavides" — inlined
    into the how-it-works page, four times, directly above a column headed WHAT
    GETS SENT, while nothing was in fact being sent to her.

    The surname may still appear as the name of the PROJECT this instrument was
    built for, which is not a delivery claim and is already public. It may not
    appear any other way. Checked on the templates, the README and the BUILT
    pages, because the chart reaches a reader only through the build."""
    # docs/methodology.html is excluded, and only it: it is a rendering of
    # METHODOLOGY.md, a memo the operator wrote and addressed to its reader by
    # name, on purpose. A memo's own TO: line is not a claim that an automated
    # email is arriving, and that file is the operator's, not this workstream's.
    surfaces = [TEMPLATES / "how_it_works.html.j2", TEMPLATES / "index.html.j2",
                REPO / "README.md", TEMPLATES / "assets" / "workflow.svg.j2"]
    surfaces += [p for p in sorted((REPO / "docs").rglob("*.html"))
                 if p.name != "methodology.html"]
    surfaces += [REPO / "docs" / "assets" / "workflow.svg"]
    for path in surfaces:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        assert "ximena" not in text.lower(), f"{path.name} names the recipient"
        for m in re.finditer(r"Benavides", text):
            tail = text[m.end():m.end() + 13]
            assert tail.startswith(" ISDS project"), (
                f"{path.relative_to(REPO)} names the recipient outside the phrase "
                f"'the Benavides ISDS project': …{text[m.start()-60:m.end()+30]}…")
        # No email address of any shape. (README names `smtp.gmail.com` as a
        # server host, which is configuration and not a person; an address needs
        # the @.)
        addresses = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
        assert not addresses, f"{path.relative_to(REPO)} carries an address: {addresses}"


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
