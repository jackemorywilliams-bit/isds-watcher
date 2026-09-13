"""The publication quarantine — what may NOT reach a reader, enforced.

THE RULE, from the council's rulings session of 2026-09-13 (Ruling 4(b)):

    No V2 shadow figure may be published, cited or compared in any digest,
    memo, brief or site surface until the locked set produces a calibration.
    The lane is instrumented, not consulted.

WHY THIS IS A TEST AND NOT A PARAGRAPH IN A MEMO. The V2 shadow derivation runs
on every candidate of every run and writes a lane, a band-shaped verdict and a
basis into telemetry. It is uncalibrated by construction — `analytics/locked_set/`
holds no coded labels, so nothing has ever measured what a V2 lane means. A
number of exactly that kind is the easiest thing in this repository to publish by
accident: it is already computed, it is already on the record, it has a
confident-looking name, and the site build and the brief both walk over run
artefacts looking for things to show. A rule written in a comment is obeyed by
whoever read the comment. This is the control.

HOW IT FAILS CLOSED. It does not check a list of known publication surfaces —
that list would be complete only until someone added a file to it. It checks the
COMPLEMENT: every file under `src/`, `scripts/`, `templates/` and `prompts/` is
scanned, and a hit on any `classify_v2.V2_SHADOW_KEYS` identifier is a failure
unless the file is on a short allowlist that this test spells out with a reason
per entry. A new publication surface is therefore scanned the moment it exists,
and a deliberate new consumer of the shadow lane has to be argued for here.

The ruling's own enumeration of the publication surfaces (`src/render.py`,
`templates/`, `src/research_brief.py`, `scripts/build_site.py`,
`scripts/send_aggregate.py`, `scripts/send_daily_update.py`) is asserted
separately, so that a rename which quietly removes one of them from the scan
fails rather than passing vacuously.
"""

import os

import pytest

from src import classify_v2, tail_audit

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The directories that hold everything the instrument runs and everything it
# renders. `docs/` and `digests/` are generated OUTPUT — they are checked by the
# surface assertions below via the generators that write them, because a guard
# that only inspects output tells you after the fact.
SCANNED_DIRS = ("src", "scripts", "templates", "prompts")
SCANNED_SUFFIXES = (".py", ".j2", ".html", ".txt", ".md", ".yaml", ".yml", ".json")

# The only files permitted to name a V2 shadow identifier, each with the reason.
# Adding to this list is a decision about the quarantine, which is why it is a
# list of reasons rather than a list of paths.
ALLOWED = {
    # Produces the shadow call and owns the key list itself.
    "src/classify_v2.py": "the V2 call; owns V2_SHADOW_KEYS",
    # Owns the verdict, the basis field and `shadow_verdict`.
    "src/rings.py": "the lane derivation the shadow records",
    # Resolves the switch and documents the ruling.
    "src/config.py": "resolves V2_SHADOW_CALLS / STATE_MODEL_V2",
    # Runs the sampled call and writes the telemetry sections.
    "src/main.py": "the run; samples the call and records it",
    # Stores the sections. Storage is not publication.
    "src/telemetry.py": "the append-only record the shadow is written to",
    # Imports STRENGTH_WORDS from classify_v2 — the module name, nothing more.
    "src/triage.py": "imports the strength vocabulary from classify_v2",
    # The prompt the V2 call sends. Not a reader of anything.
    "prompts/classifier_v2.txt": "the V2 prompt itself",
}

# Deliberately NOT allowlisted, though both would be defensible entries:
# `scripts/telemetry_query.py` (the internal reporting surface) and
# `scripts/check_telemetry_privacy.py` (the privacy guard) do not read a V2
# shadow key today. An allowlist entry granted in advance is a permission nobody
# reviews; if either needs one later, that is an argument to make then.

# The ruling's own enumeration. Asserted to EXIST so that a rename cannot empty
# the scan silently, and asserted to be clean as the named requirement.
PUBLICATION_SURFACES = (
    "src/render.py",
    "src/research_brief.py",
    "scripts/build_site.py",
    "scripts/send_aggregate.py",
    "scripts/send_daily_update.py",
)


def _scanned_files():
    for d in SCANNED_DIRS:
        root = os.path.join(REPO, d)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(n for n in dirnames
                                 if n not in ("__pycache__", ".git"))
            for name in sorted(filenames):
                if not name.endswith(SCANNED_SUFFIXES):
                    continue
                full = os.path.join(dirpath, name)
                yield os.path.relpath(full, REPO).replace(os.sep, "/"), full


def _hits(path: str, keys=None) -> list[str]:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    return sorted(k for k in (keys or classify_v2.V2_SHADOW_KEYS) if k in text)


# --------------------------------------------------------------------------- #
# The tail audit (Ruling 4(c)): the MEASUREMENT is internal; the COST is not
# --------------------------------------------------------------------------- #
# "Reporting surface: scripts/telemetry_query.py ONLY. Never the digest, never
# the professor-facing site, never the README. A tail-audit flip rate is an
# internal measurement of the instrument, not a finding about ISDS; publishing
# it to the recipient would be the instrument grading itself in her inbox."
#
# The scan therefore reaches further than the V2 one: past the code and the
# templates into the GENERATED site (`docs/`), the committed digest archive
# (`digests/`) and `README.md`, because those are the places the ruling names
# and because a leak that already shipped is exactly what a guard should find.
#
# `tail_audit_cost_usd` and `TAIL_AUDIT_N` are deliberately NOT quarantined
# identifiers — the same ruling REQUIRES the cost in `meta.json` and the run
# summary. What may not be published is the measurement: the ledger and the
# paired bands in it. See `src.tail_audit.PUBLICATION_KEYS`.
TAIL_SCANNED_DIRS = SCANNED_DIRS + ("docs", "digests")
TAIL_SCANNED_FILES = ("README.md",)

TAIL_ALLOWED = {
    "src/tail_audit.py": "the audit itself; owns PUBLICATION_KEYS",
    "src/main.py": "the run; draws the sample and appends to the ledger",
    "src/config.py": "documents the audit and its cost derivation",
    "scripts/check_telemetry_privacy.py": "the guard on the ledger's schema",
    "scripts/telemetry_query.py": "the ONE reporting surface the ruling allows",
}

# `src/render.py` is deliberately absent and must stay absent: it writes the
# digest, the article files and meta.json, so it is the surface this ruling is
# most about. It reports the audit's COST (a required field) and names neither
# the ledger nor a band.


def _tail_scanned_files():
    for d in TAIL_SCANNED_DIRS:
        root = os.path.join(REPO, d)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(n for n in dirnames
                                 if n not in ("__pycache__", ".git"))
            for name in sorted(filenames):
                if not name.endswith(SCANNED_SUFFIXES):
                    continue
                full = os.path.join(dirpath, name)
                yield os.path.relpath(full, REPO).replace(os.sep, "/"), full
    for rel in TAIL_SCANNED_FILES:
        full = os.path.join(REPO, rel)
        if os.path.exists(full):
            yield rel, full


def test_the_tail_audit_key_list_names_the_measurement_and_not_the_cost():
    keys = tail_audit.PUBLICATION_KEYS
    assert {"tail_audit.jsonl", "band_unenriched", "band_enriched",
            "score_delta"} <= keys
    # The cost is required in meta.json by the same ruling. Quarantining it
    # would make the ruling contradict itself and the guard unsatisfiable.
    assert "tail_audit_cost_usd" not in keys
    assert "TAIL_AUDIT_N" not in keys


def test_the_readme_and_the_generated_site_are_actually_scanned():
    scanned = {rel for rel, _ in _tail_scanned_files()}
    assert "README.md" in scanned
    assert any(rel.startswith("docs/") for rel in scanned),         "the professor-facing site is named in Ruling 4(c) and was not scanned"
    assert any(rel.startswith("digests/") for rel in scanned),         "the digest archive is named in Ruling 4(c) and was not scanned"


def test_the_tail_audit_measurement_reaches_no_surface_outside_its_allowlist():
    """Never the digest, never the site, never the README."""
    offenders = {}
    for rel, full in _tail_scanned_files():
        if rel in TAIL_ALLOWED:
            continue
        hits = _hits(full, tail_audit.PUBLICATION_KEYS)
        if hits:
            offenders[rel] = hits
    assert not offenders, (
        f"the tail audit's measurement is read outside its allowlist: "
        f"{offenders}. Ruling 4(c) of 2026-09-13: the reporting surface is "
        "scripts/telemetry_query.py and nothing else. A flip rate is an "
        "internal measurement of the instrument, not a finding about ISDS.")


def test_the_tail_audit_allowlist_has_no_stale_entries():
    for rel in TAIL_ALLOWED:
        full = os.path.join(REPO, rel)
        assert os.path.exists(full), f"allowlisted {rel} no longer exists"
        assert _hits(full, tail_audit.PUBLICATION_KEYS), (
            f"{rel} is allowlisted for the tail audit but no longer references "
            "any of its keys; remove it from TAIL_ALLOWED")


def test_the_key_list_is_not_empty_and_names_the_fields_it_claims_to():
    """A guard that scans for nothing passes everything."""
    keys = classify_v2.V2_SHADOW_KEYS
    assert {"verdict_v2", "v2_call", "v2_basis", "claims_source"} <= keys
    assert "V2_SHADOW_CALLS" in keys and "STATE_MODEL_V2" in keys


def test_every_publication_surface_the_ruling_names_still_exists():
    """A rename must fail this test, not quietly shrink the scan."""
    scanned = {rel for rel, _ in _scanned_files()}
    for rel in PUBLICATION_SURFACES:
        assert os.path.exists(os.path.join(REPO, rel)), \
            f"{rel} is named in Ruling 4(b) and is not where the guard looks"
        assert rel in scanned, f"{rel} exists but the guard is not scanning it"
    assert any(rel.startswith("templates/") for rel in scanned), \
        "the digest templates are a publication surface and were not scanned"


@pytest.mark.parametrize("rel", PUBLICATION_SURFACES)
def test_no_named_publication_surface_reads_a_v2_shadow_field(rel):
    """The ruling, at the surfaces it names, one failure message per file."""
    hits = _hits(os.path.join(REPO, rel))
    assert not hits, (
        f"{rel} references V2 shadow field(s) {hits}. Ruling 4(b) of 2026-09-13: "
        "no V2 shadow figure may be published, cited or compared in any digest, "
        "memo, brief or site surface until the locked set calibrates it. The "
        "lane is instrumented, not consulted.")


def test_no_file_outside_the_allowlist_reads_a_v2_shadow_field():
    """The complement, which is what makes this guard survive a new surface."""
    offenders = {}
    for rel, full in _scanned_files():
        if rel in ALLOWED:
            continue
        hits = _hits(full)
        if hits:
            offenders[rel] = hits
    assert not offenders, (
        f"V2 shadow fields are read outside the allowlist: {offenders}. Either "
        "the file must stop reading them, or it must be added to ALLOWED in this "
        "test with a reason — which is a decision about the quarantine Ruling "
        "4(b) imposed, and is meant to be made deliberately.")


def test_the_allowlist_has_no_stale_entries():
    """An allowlist that outlives its reason is a hole nobody is watching."""
    for rel in ALLOWED:
        full = os.path.join(REPO, rel)
        assert os.path.exists(full), f"allowlisted {rel} no longer exists"
        assert _hits(full), (
            f"{rel} is allowlisted but no longer references any V2 shadow key; "
            "remove it from ALLOWED so the allowlist keeps meaning something")
