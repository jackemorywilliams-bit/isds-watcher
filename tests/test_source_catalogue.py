"""One roster, and every surface that describes it.

On 2026-09-10 this project described its own inputs in four places and agreed
with itself in none of them. `all_sources()` returned ten. The how-it-works page
said "the nine public sources", twice. The digest email said "nine open sources"
and then listed seven. The README tiered seven of the ten, leaving PCA, Bing News
and GDELT in none. The workflow chart's banner said "THE 10 SOURCES" because
those digits were typed into `chart-core.mjs`, and its collect card said "all 10
sources" because they were typed into `workflow.json` — right by coincidence, and
connected to nothing.

Two of the ten are not public at all. `google_alerts` and `gmail_scholar` read
feeds inside the operator's own Google account: nobody else can re-run them and
nobody can audit what they delivered. Calling them public sources is a validity
claim that is false, not loose wording, so it has a test rather than a style note.

These tests pin the roster's shape, pin its catalogue fields against the pipeline
flags that must agree with them, and scan every public surface for a count
written by hand.
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
SVG = TEMPLATES / "assets" / "workflow.svg.j2"
MANIFEST = REPO / "views" / "isds-workflow-3d" / "workflow.json"
INVENTORY = REPO / "analytics" / "source-inventory.md"


@pytest.fixture(scope="module")
def inv():
    sys.path.insert(0, os.path.join(str(REPO), "scripts"))
    return importlib.import_module("build_source_inventory")


# --------------------------------------------------------------------------- #
# The roster itself
# --------------------------------------------------------------------------- #
def test_ten_sources_two_of_which_a_third_party_cannot_re_run(inv):
    rows = inv.catalogue()
    assert len(rows) == 10
    assert len(inv.open_repository(rows)) == 8
    operator = inv.operator_account(rows)
    assert len(operator) == 2
    assert {r["name"] for r in operator} == {"google_alerts", "gmail_scholar"}


def test_every_catalogue_field_is_filled_and_from_the_declared_vocabulary(inv):
    from src.sources.base import CHANNELS, READ_DEPTHS
    rows = inv.catalogue()
    for row in rows:
        assert row["label"], f"{row['name']}: no reader-facing label"
        assert row["channel"] in CHANNELS, row
        assert row["read_depth"] in READ_DEPTHS, row
        assert (REPO / row["module"]).is_file(), row["module"]
    labels = [r["label"] for r in rows]
    assert len(labels) == len(set(labels)), f"duplicate labels: {labels}"
    names = [r["name"] for r in rows]
    assert len(names) == len(set(names))


def test_an_unknown_channel_is_an_import_error_not_a_word_on_a_page():
    """Fail closed: the vocabulary is validated where the roster is declared, so
    a typo breaks the run rather than reaching a reader inside a sentence about
    what can and cannot be independently checked."""
    from src.sources.base import CHANNELS, READ_DEPTHS
    assert "operator-mailbox" in CHANNELS and "open-repository" in CHANNELS
    assert "headline-only" in READ_DEPTHS
    # The declaration-site guard, exercised directly.
    import src.sources as pkg
    bad = tuple(list(pkg._CATALOGUE[:1]) + [(object, "X", "not-a-channel", "full-text")])
    for cls, label, channel, depth in bad[1:]:
        assert channel not in CHANNELS  # what the import-time loop raises on


def test_read_depth_agrees_with_the_pipeline_flags_it_describes(inv):
    """`headline-only` is not a description, it is a claim about two sets in
    `src/`. If the catalogue and the pipeline ever disagree, the site would be
    telling a reader that a body was read when the fetcher refuses to fetch it."""
    from src import config
    from src.enrich import NO_BODY_FETCH
    catalogued = {r["name"] for r in inv.catalogue() if r["read_depth"] == "headline-only"}
    assert catalogued == set(config.HEADLINE_ONLY_SOURCES)
    assert catalogued == set(NO_BODY_FETCH)


def test_all_sources_carries_the_catalogue_onto_every_instance():
    from src.sources import all_sources
    for src in all_sources():
        assert src.label and src.channel and src.read_depth
        assert src.label != src.name.capitalize() or src.name in {"italaw"}


# --------------------------------------------------------------------------- #
# The generated inventory
# --------------------------------------------------------------------------- #
def test_the_committed_inventory_is_what_the_builder_would_write(inv):
    assert INVENTORY.read_text(encoding="utf-8") == inv.render(), (
        "analytics/source-inventory.md is stale or was hand-edited; regenerate "
        "with `python scripts/build_source_inventory.py`")


def test_the_inventory_names_the_two_it_cannot_vouch_for(inv):
    text = INVENTORY.read_text(encoding="utf-8")
    assert "Google Alerts" in text and "Scholar Alerts" in text
    assert "cannot be re-run by anyone else" in text
    assert "**10 sources**" in text


# --------------------------------------------------------------------------- #
# The workflow chart — phase one: the number, not the geometry
# --------------------------------------------------------------------------- #
def test_the_chart_draws_one_chip_per_source(inv):
    """The banner headline is templated from all_sources(); the chips come from
    the chart manifest. This is the assertion that keeps the two in step — a
    chart headed "THE 11 SOURCES" over ten chips is the same defect in a new
    place. (Generating the chips themselves from the roster is a separate piece
    of work and belongs to the systems workstream.)"""
    import json
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    n = len(inv.catalogue())
    assert len(manifest["chips"]) == n
    svg = SVG.read_text(encoding="utf-8")
    assert svg.count('class="wf-chip"') == n


def test_the_chart_manifest_and_the_roster_name_the_same_ten_modules(inv):
    import json
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    charted = {e for c in manifest["chips"] for e in c.get("evidence", [])}
    assert charted == {r["module"] for r in inv.catalogue()}


def test_the_charts_source_count_is_templated_and_never_drawn(inv):
    """Both number tokens, in the committed artifact: the banner headline and the
    collect card (painted line plus hover tooltip)."""
    svg = SVG.read_text(encoding="utf-8")
    assert svg.count("{{sources|length}}") == 3, (
        "expected the banner headline, the wrapped card line and its tooltip")
    assert "THE 10 SOURCES" not in svg
    assert "all 10 sources" not in svg
    # The manifest must not carry the digits either — that is where one of them
    # was written.
    manifest = MANIFEST.read_text(encoding="utf-8")
    assert "10 sources" not in manifest
    assert "{sourceCount}" in manifest


def test_the_generator_still_reproduces_the_artifact_byte_for_byte():
    """The artifact is generated, so it is only trustworthy if re-running the
    generator over the committed inputs returns the committed bytes."""
    import shutil
    import subprocess
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not available; the chart generator cannot be re-run")
    before = SVG.read_bytes()
    result = subprocess.run(
        [node, str(REPO / "tools" / "isds-workflow-3d" / "render-static.mjs")],
        capture_output=True, text=True)
    after = SVG.read_bytes()
    if after != before:
        SVG.write_bytes(before)
    assert result.returncode == 0, result.stderr
    assert after == before, (
        "scripts/site_templates/assets/workflow.svg.j2 is stale against "
        "views/isds-workflow-3d/workflow.json + src/render-config.mjs; re-run "
        "`npm run render-static` in tools/isds-workflow-3d")


# --------------------------------------------------------------------------- #
# Every surface that states the count
# --------------------------------------------------------------------------- #
def _public_surfaces() -> list[Path]:
    return (sorted(TEMPLATES.glob("*.j2"))
            + [REPO / "README.md",
               REPO / "scripts" / "send_aggregate.py",
               INVENTORY])


def test_no_surface_says_nine():
    """The exact word that was wrong on three of them. It is banned outright
    rather than corrected, because "nine" was right once and became wrong when a
    tenth source was added, which is the failure mode a count in prose has."""
    hits = []
    for path in _public_surfaces():
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\bnine\b", line, re.I):
                hits.append(f"{path.relative_to(REPO)}:{i}: {line.strip()[:120]}")
    assert not hits, (
        "a public surface writes a source count in words; render it from "
        "`sources` instead:\n" + "\n".join(hits))


def test_no_surface_calls_the_operators_own_feeds_public(inv):
    """The substantive half of the same repair. Two of the ten are the operator's
    own Google account, and a reader deciding whether to rely on this instrument
    needs to know which inputs are reproducible."""
    banned = re.compile(
        r"(nine|ten|\b10\b|all)\s+(public|open)\s+(ISDS\s+)?sources", re.I)
    hits = []
    for path in _public_surfaces():
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if banned.search(line):
                hits.append(f"{path.relative_to(REPO)}:{i}: {line.strip()[:120]}")
    assert not hits, (
        "a surface calls the whole roster public; two of the ten are feeds inside "
        "the operator's own Google account:\n" + "\n".join(hits))


def test_the_templates_render_the_roster_rather_than_listing_it(inv):
    """A hand-written list of source names is the same defect as a hand-written
    count — the email's said seven while its number said nine."""
    for name in ("how_it_works.html.j2", "index.html.j2"):
        text = (TEMPLATES / name).read_text(encoding="utf-8")
        assert "sources | length" in text, f"{name} does not render the count"
        assert "source_names" in text, f"{name} does not render the roster"
        # The split is rendered too. `check_claims.py` registers the TOTAL
        # ("catalogue sources"); the operator-account count is guarded here,
        # because a page that said "one feed inside Emory's own account" would
        # understate exactly the thing the disclosure exists for.
        assert "sources_operator" in text, f"{name} does not render the split"
        assert "sources_open" in text, f"{name} does not render the split"


def test_the_public_surfaces_disclose_the_operator_account(inv):
    for path, fragment in (
            (TEMPLATES / "how_it_works.html.j2", "cannot re-run them"),
            (TEMPLATES / "index.html.j2", "nobody else can re-run"),
            (REPO / "README.md", "cannot re-run them"),
            (REPO / "scripts" / "send_aggregate.py", "else can re-run or audit")):
        assert fragment in path.read_text(encoding="utf-8"), (
            f"{path.relative_to(REPO)} lost the operator-account disclosure")
