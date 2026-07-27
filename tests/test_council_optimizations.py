"""Council-adopted optimizations (2026-07-27 vote): G23 gap-escalation counters,
G26 monitored-author protocol, G18 cross-BIT consistency rule.

G23's design premise: the MODEL's memory must never be the escalation threshold —
code counts GAP-UNRESOLVED markers across sessions and trips at three, and an
escalated gap is injected back into the prompt as a do-not-search operator item.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import research_brief, research_state  # noqa: E402

_ROOT = os.path.join(os.path.dirname(__file__), "..")
MEMO_WITH_GAP = ("Analysis...\nGAP-UNRESOLVED: china-france-bit-2007-protocol-exhaustion — "
                 "Protocol admin-exhaustion formulation has no accessible primary text.\n")


def test_gap_counter_increments_and_escalates_at_three():
    data = {"seq": 0, "open_threads": [], "history": []}
    for i in range(1, 4):
        seen = research_state.update_gap_counters(data, MEMO_WITH_GAP)
        slug = "china-france-bit-2007-protocol-exhaustion"
        assert seen[slug]["count"] == i
        assert seen[slug]["escalated"] is (i >= research_state.ESCALATION_THRESHOLD)
    gaps = research_state.escalated_gaps(data)
    assert len(gaps) == 1 and gaps[0]["slug"] == slug


def test_gap_counter_clears_when_not_reported():
    data = {"seq": 0, "open_threads": [], "history": []}
    research_state.update_gap_counters(data, MEMO_WITH_GAP)
    research_state.update_gap_counters(data, "quiet week, all threads advanced.")
    assert data["gap_counters"] == {}
    assert research_state.escalated_gaps(data) == []


def test_gap_slug_is_stable_across_dash_variants():
    data = {"seq": 0, "open_threads": [], "history": []}
    research_state.update_gap_counters(
        data, "GAP-UNRESOLVED: my-gap — description with em dash")
    research_state.update_gap_counters(
        data, "GAP-UNRESOLVED: my-gap -- description with double hyphen")
    assert data["gap_counters"]["my-gap"]["count"] == 2


def test_escalated_gaps_block_renders_do_not_search():
    block = research_brief._escalated_gaps_block([
        {"slug": "china-france-bit-2007-protocol-exhaustion",
         "description": "Protocol formulation unconfirmed", "count": 3,
         "escalated": True}])
    assert "china-france-bit-2007-protocol-exhaustion" in block
    assert "Do NOT search this" in block
    assert research_brief._escalated_gaps_block([]) == "(none)"
    assert research_brief._escalated_gaps_block(None) == "(none)"


def test_analyst_prompt_carries_all_three_protocols():
    import re
    text = open(os.path.join(_ROOT, "prompts", "research_analyst.txt"),
                encoding="utf-8").read()
    text = re.sub(r"\s+", " ", text)  # whitespace-tolerant (hard-wrapped prose)
    # G23: escalation placeholder + marker instructions
    assert "{{ESCALATED_GAPS}}" in text
    assert "GAP-UNRESOLVED:" in text
    # G26: monitored author pages, with the WAF honesty note
    assert "ejiltalk.org/author/aroberts/" in text
    assert "never masquerades as a browser" in text
    # G18: the four in-scope China BITs, named, with the absence guardrail
    for bit in ("China–Germany (2003)", "China–Switzerland (2009)",
                "China–France (2007)", "China–Netherlands (2001)"):
        assert bit in text
    assert "not found in accessible sources" in text
