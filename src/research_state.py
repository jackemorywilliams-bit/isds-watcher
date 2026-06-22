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
