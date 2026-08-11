"""The analyst's living memory must be embedded in the prompt, never assumed on disk.

Regression tests for the recurring weekly escalation: "the living-memory files were
not present in this session's environment and were reconstructed" — the analyst runs
as a Messages-API call with no filesystem, while prompts/research_analyst.txt told it
to *read files*. The canonical contents are now embedded via {{LIVING_MEMORY}}, and a
missing file renders a loud MISSING marker instead of silence.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import research_brief  # noqa: E402

_ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_prompt_template_carries_living_memory_placeholder():
    text = open(os.path.join(_ROOT, "prompts", "research_analyst.txt"),
                encoding="utf-8").read()
    assert "{{LIVING_MEMORY}}" in text
    # The old file-reading instruction must not survive — the session has no disk.
    assert "Begin every session by reading `STATE_OF_THE_ANSWER.md`" not in text


def test_block_embeds_canonical_contents(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    open("STATE_OF_THE_ANSWER.md", "w", encoding="utf-8").write(
        "# State of the Answer\nRing 3 is codifying.\n")
    os.makedirs("analytics")
    with open(os.path.join("analytics", "insights.jsonl"), "w", encoding="utf-8") as fh:
        fh.write('{"seq": 1, "insight": "first"}\n{"seq": 2, "insight": "second"}\n')
    block = research_brief._living_memory_block()
    assert "Ring 3 is codifying." in block
    assert '"seq": 2' in block
    assert "MISSING" not in block


def test_block_truncates_long_state(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    open("STATE_OF_THE_ANSWER.md", "w", encoding="utf-8").write("x" * 20000)
    os.makedirs("analytics")
    open(os.path.join("analytics", "insights.jsonl"), "w", encoding="utf-8").write("{}\n")
    block = research_brief._living_memory_block()
    assert "truncated for length" in block
    assert len(block) < 12000


def test_block_caps_insight_lines(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    open("STATE_OF_THE_ANSWER.md", "w", encoding="utf-8").write("state\n")
    os.makedirs("analytics")
    with open(os.path.join("analytics", "insights.jsonl"), "w", encoding="utf-8") as fh:
        for i in range(100):
            fh.write('{"seq": %d}\n' % i)
    block = research_brief._living_memory_block()
    assert '"seq": 99' in block          # newest kept
    assert '"seq": 5}' not in block      # oldest dropped
    assert "newest 30 of 100" in block


def test_missing_files_render_loud_markers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    block = research_brief._living_memory_block()
    assert block.count("MISSING") >= 2
    assert "procedural caveat" in block


def test_real_repo_block_is_complete():
    cwd = os.getcwd()
    os.chdir(_ROOT)
    try:
        block = research_brief._living_memory_block()
    finally:
        os.chdir(cwd)
    # Match the assembler's exact sentinel ("\nMISSING — ..."), not the bare
    # word: the council's 2026-08-10 insight legitimately contains "MISSING
    # FILTER" in prose, which made this assertion fail on an intact checkout.
    assert "\nMISSING — " not in block
    assert "STATE_OF_THE_ANSWER.md" in block
    assert "insights.jsonl" in block
