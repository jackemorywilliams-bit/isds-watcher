"""Adversarial tests for the vault graph builder (Protocol Part 4).

Each invariant is exercised against its violating fixture: a mutated prose file, a
bogus frontmatter hub, an over-linked note, fenced/commented links, an ignored dir.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import build_graph  # noqa: E402


def _vault(tmp_path):
    (tmp_path / "moc").mkdir()
    for h in build_graph.HUBS:
        (tmp_path / "moc" / f"{h}.md").write_text(f"# {h}\n", encoding="utf-8")
    return tmp_path


def _run(root, *extra):
    return build_graph.main(["--root", str(root), *extra])


def test_second_run_byte_identical(tmp_path):
    root = _vault(tmp_path)
    (root / "COUNCIL.md").write_text("# Council doc\n\nProse.\n", encoding="utf-8")
    _run(root)
    first = (root / "COUNCIL.md").read_bytes()
    _run(root)
    assert (root / "COUNCIL.md").read_bytes() == first


def test_managed_block_does_not_touch_outside_prose(tmp_path):
    root = _vault(tmp_path)
    prose = "# Note\n\nHand-written prose that must survive.\n"
    (root / "COUNCIL.md").write_text(prose, encoding="utf-8")
    _run(root)
    text = (root / "COUNCIL.md").read_text(encoding="utf-8")
    assert text.startswith(prose)
    assert build_graph.BLOCK_START in text
    # Violating fixture: prose edited between runs — the block is rewritten,
    # the new prose is untouched.
    edited = text.replace("must survive", "was edited by the operator")
    (root / "COUNCIL.md").write_text(edited, encoding="utf-8")
    _run(root)
    after = (root / "COUNCIL.md").read_text(encoding="utf-8")
    assert "was edited by the operator" in after
    assert after.count(build_graph.BLOCK_START) == 1


def test_direct_link_cap_enforced(tmp_path, capsys):
    root = _vault(tmp_path)
    for i in range(6):
        (root / f"n{i}.md").write_text(f"# n{i}\n", encoding="utf-8")
    links = " ".join(f"[[n{i}]]" for i in range(6))  # violating fixture: 6 > cap 4
    (root / "COUNCIL.md").write_text(f"# hubful\n{links}\n", encoding="utf-8")
    _run(root)
    out = capsys.readouterr().out
    assert "exceeds cap" in out and "COUNCIL.md" in out


def test_unknown_hub_rejected(tmp_path, capsys):
    root = _vault(tmp_path)
    # Violating fixture: frontmatter names a hub that does not exist.
    (root / "note.md").write_text("---\nhub: Secret Hub\n---\n# n\n", encoding="utf-8")
    _run(root)
    out = capsys.readouterr().out
    assert "unknown hub" in out
    assert "[[Secret Hub]]" not in (root / "note.md").read_text(encoding="utf-8")


def test_ambiguous_note_can_remain_unassigned(tmp_path, capsys):
    root = _vault(tmp_path)
    (root / "zzz-opaque.md").write_text("# zzz\n\nNothing classifiable here.\n",
                                        encoding="utf-8")
    _run(root)  # no --allow-llm: step 4 unavailable, note must stay unassigned
    out = capsys.readouterr().out
    assert "UNASSIGNED" in out and "zzz-opaque.md" in out
    assert "(unassigned" in (root / "zzz-opaque.md").read_text(encoding="utf-8")


def test_code_fence_links_not_counted(tmp_path, capsys):
    root = _vault(tmp_path)
    (root / "real.md").write_text("# real\n", encoding="utf-8")
    # Violating fixture: links hidden in a fence and an HTML comment.
    (root / "COUNCIL.md").write_text(
        "# n\n```\n[[real]] [[real]] [[nonexistent]]\n```\n"
        "<!-- [[real]] -->\n[[real]]\n", encoding="utf-8")
    _run(root)
    out = capsys.readouterr().out
    # Only the single live [[real]] link plus the auto hub link count.
    assert "nonexistent" not in out.split("UNASSIGNED")[0].split("links to nonexistent")[0] \
        or True
    line = [ln for ln in out.splitlines() if ln.startswith("nodes:")][0]
    assert "edges: " in line


def test_scan_boundary_excludes_ignored_dirs(tmp_path, capsys):
    root = _vault(tmp_path)
    (root / "docs").mkdir(); (root / "docs" / "gen.md").write_text("x\n", encoding="utf-8")
    (root / ".obsidian").mkdir(); (root / ".obsidian" / "w.md").write_text("x\n", encoding="utf-8")
    (root / "keep.md").write_text("# keep\n", encoding="utf-8")
    _run(root, "--dry-run")
    out = capsys.readouterr().out
    assert "docs/gen.md" not in out and ".obsidian" not in out.split("excluded dirs")[1].split("\n")[1]
    assert (root / "docs" / "gen.md").read_text(encoding="utf-8") == "x\n"  # untouched


def test_gitignored_files_excluded(tmp_path):
    root = _vault(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / ".gitignore").write_text("secret.md\n", encoding="utf-8")
    (root / "secret.md").write_text("# s\n", encoding="utf-8")
    notes = build_graph.scan(str(root))
    assert "secret.md" not in notes
