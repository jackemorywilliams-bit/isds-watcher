"""Persistent state for the weekly Research Brief.

Holds two things that make the brief a *continuous* research effort rather than a
series of cold starts:

  * ``seq``         — a monotonic issue number, surfaced in the subject/masthead.
  * ``open_threads`` — the questions/leads the editor carried out of the last issue.
                       They are fed back into next week's analyst prompt, so each
                       brief builds on the previous one (the "autoprompt" loop).

Stored as ``state/research_log.json``. Like the seen-state, this never crashes the
run: a missing or corrupt file is treated as an empty log.
"""

from __future__ import annotations

import json
import logging
import os

logger = logging.getLogger("isds.research_state")

_PATH = os.path.join("state", "research_log.json")


def load(path: str = _PATH) -> dict:
    """Load the research log; return an empty log on any problem."""
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            data.setdefault("seq", 0)
            data.setdefault("open_threads", [])
            data.setdefault("history", [])
            return data
    except (FileNotFoundError, ValueError, OSError) as exc:
        logger.info("research_state: starting fresh (%s)", exc)
    return {"seq": 0, "open_threads": [], "history": []}


def save(data: dict, path: str = _PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def record_issue(data: dict, date_str: str, headline: str,
                 open_threads: list[str]) -> int:
    """Advance the issue number, replace the carried threads, and prepend a
    history entry. Returns the new issue number."""
    data["seq"] = int(data.get("seq", 0)) + 1
    data["open_threads"] = [t.strip() for t in (open_threads or []) if t and t.strip()][:8]
    data.setdefault("history", []).insert(
        0, {"seq": data["seq"], "date": date_str, "headline": headline})
    data["history"] = data["history"][:60]
    return data["seq"]


# --- Gap counters (council optimization G23: Navigator escalation protocol) --------
#
# The analyst emits machine-readable "GAP-UNRESOLVED: <slug> — <description>" lines
# for any named provision/document gap that a session again failed to resolve. This
# code — not the model's memory — counts consecutive unresolved sessions per slug,
# and at ESCALATION_THRESHOLD the gap becomes a standing operator-action item:
# injected into the next analyst prompt as escalated (STOP searching; the operator
# runs the UNCTAD IIA Mapping Navigator / equivalent manual query) and surfaced in
# the Monday review packet. Slugs absent from a session's memo are considered
# resolved and their counters clear.

ESCALATION_THRESHOLD = 3
_GAP_RE = None  # compiled lazily to keep module import light


def update_gap_counters(data: dict, analyst_memo: str) -> dict:
    """Parse GAP-UNRESOLVED lines from the memo and update per-slug counters.
    Returns {slug: {"count", "description", "escalated"}} for this session."""
    global _GAP_RE
    if _GAP_RE is None:
        import re
        _GAP_RE = re.compile(r"^GAP-UNRESOLVED:\s*([a-z0-9][a-z0-9-]*)\s*(?:—|--|-)\s*(.+)$",
                             re.MULTILINE | re.IGNORECASE)
    counters = data.setdefault("gap_counters", {})
    seen = {}
    for m in _GAP_RE.finditer(analyst_memo or ""):
        slug, desc = m.group(1).lower(), m.group(2).strip()
        entry = counters.get(slug, {"count": 0, "description": desc})
        entry["count"] = int(entry.get("count", 0)) + 1
        entry["description"] = desc or entry.get("description", "")
        entry["escalated"] = entry["count"] >= ESCALATION_THRESHOLD
        counters[slug] = entry
        seen[slug] = entry
    for slug in list(counters):
        if slug not in seen:               # not reported this session -> resolved
            logger.info("research_state: gap %s cleared (not reported)", slug)
            del counters[slug]
    return seen


def escalated_gaps(data: dict) -> list[dict]:
    """Gaps at/over threshold, for the analyst prompt and the Monday packet."""
    return [{"slug": s, **e} for s, e in (data.get("gap_counters") or {}).items()
            if e.get("escalated")]
