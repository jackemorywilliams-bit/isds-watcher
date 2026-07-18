"""Adversarial tests for the one-pager contract (Protocol Part 2).

Quote integrity is checked against text re-extracted from the seed PDFs (pdftotext);
labeling rules are checked on the repo canonicals and via the export helper, which is
defined here (the sanctioned Desktop export is a one-off operator deliverable, so the
testable logic lives with its tests).
"""

import os
import re
import shutil
import subprocess

import pytest

REPO = os.path.join(os.path.dirname(__file__), "..")
ONE_PAGERS = {
    "philip-morris-v-australia.md": "Philip_Morris_v_Australia_Award_2015-12-17.pdf",
    "eli-lilly-v-canada.md": "Eli_Lilly_v_Canada_Final_Award_2017-03-16.pdf",
    "bridgestone-v-panama.md": "Bridgestone_v_Panama_Award_2020-08-14.pdf",
}

_HAS_PDFTOTEXT = shutil.which("pdftotext") is not None


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def _canonical(md: str) -> str:
    with open(os.path.join(REPO, "working", "one-pagers", md), encoding="utf-8") as fh:
        return fh.read()


def export_machine_written(canonical_text: str, desktop_dir: str, filename: str) -> str | None:
    """The Desktop-export rule, as executable logic: title and filename must carry
    MACHINE-WRITTEN; an unresolvable Desktop returns None instead of raising."""
    if "MACHINE-WRITTEN" not in filename:
        raise ValueError("Desktop export filename must contain MACHINE-WRITTEN")
    lines = canonical_text.split("\n")
    lines[0] = lines[0].replace("# One-Pager —", "# One-Pager (MACHINE-WRITTEN DRAFT) —")
    if "MACHINE-WRITTEN" not in lines[0]:
        lines[0] = "# (MACHINE-WRITTEN DRAFT) " + lines[0].lstrip("# ")
    try:
        os.makedirs(desktop_dir, exist_ok=True)
        path = os.path.join(desktop_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        return path
    except OSError:
        return None  # desktop unresolvable -> the task keeps the repo canonical


@pytest.mark.skipif(not _HAS_PDFTOTEXT, reason="pdftotext (poppler) not installed")
@pytest.mark.parametrize("md,pdf", sorted(ONE_PAGERS.items()))
def test_quote_must_be_exact_substring(md, pdf, tmp_path):
    txt = tmp_path / "award.txt"
    subprocess.run(["pdftotext", "-layout",
                    os.path.join(REPO, "seeds", pdf), str(txt)], check=True)
    award = _norm(txt.read_text(encoding="utf-8"))
    body = _canonical(md)
    quotes = re.findall(r'"([^"]{25,})"', body)
    assert quotes, f"{md}: no verbatim quotes found"
    for q in quotes:
        assert _norm(q) in award, f"{md}: quote not an exact substring: {q[:80]}"


def test_missing_pdf_skips_case(tmp_path):
    # Violating fixture: a case whose PDF is absent must yield a missing-source
    # report, never a reconstructed memo. Encoded as: every shipped one-pager's
    # source PDF exists; a nonexistent PDF path is detectably absent.
    for pdf in ONE_PAGERS.values():
        assert os.path.exists(os.path.join(REPO, "seeds", pdf))
    assert not os.path.exists(os.path.join(REPO, "seeds", "Apotex_v_USA.pdf")), \
        "no one-pager may exist without its PDF present"
    assert not os.path.exists(
        os.path.join(REPO, "working", "one-pagers", "apotex-v-usa.md"))


@pytest.mark.parametrize("md", sorted(ONE_PAGERS))
def test_external_fact_not_presented_as_pdf_fact(md):
    body = _canonical(md)
    for label in ("[SOURCE FACT]", "[FRAMEWORK ANALYSIS]",
                  "[RESEARCH-QUESTION IMPLICATION]"):
        assert label in body, f"{md}: missing epistemic label {label}"
    # Any external-context section must be explicitly tagged as such.
    if "external" in body.lower():
        assert "[UNVERIFIED EXTERNAL CONTEXT]" in body


@pytest.mark.parametrize("md", sorted(ONE_PAGERS))
def test_repo_copy_title_omits_machine_written(md):
    head = _canonical(md)[:400].lower()
    for banned in ("machine-written", "machine-generated", "machine written"):
        assert banned not in head, f"{md}: repo title/header must not say {banned!r}"


def test_desktop_export_title_contains_machine_written(tmp_path):
    path = export_machine_written(_canonical("eli-lilly-v-canada.md"), str(tmp_path),
                                  "Eli Lilly — One-Pager (MACHINE-WRITTEN DRAFT).md")
    assert path and "MACHINE-WRITTEN" in os.path.basename(path)
    first_line = open(path, encoding="utf-8").readline()
    assert "MACHINE-WRITTEN" in first_line
    # Violating fixture: an unlabeled filename is refused outright.
    with pytest.raises(ValueError):
        export_machine_written("# One-Pager — x\n", str(tmp_path), "clean-title.md")


def test_desktop_unresolvable_does_not_fail_task(tmp_path):
    blocked = tmp_path / "not-a-dir"
    blocked.write_text("a file, not a directory", encoding="utf-8")
    out = export_machine_written("# One-Pager — x\n", str(blocked),
                                 "X (MACHINE-WRITTEN DRAFT).md")
    assert out is None  # graceful: canonical copy remains the deliverable


def test_style_derivative_cannot_replace_canonical():
    # The canonical repo copies carry the epistemic labels and clean titles; a
    # derivative (labeled MACHINE-WRITTEN) must never be written back over them.
    for md in ONE_PAGERS:
        body = _canonical(md)
        assert "MACHINE-WRITTEN" not in body
        assert "[SOURCE FACT]" in body
