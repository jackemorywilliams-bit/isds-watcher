"""The council's accountability ledger.

Every council session (weekly reconvene, and daily researcher check-ins once that
cadence is enabled) appends a tracked entry here, so the workflow is auditable and the
chairman can hold members accountable against a written record rather than relying on a
single model's recollection. Stored machine-readably in state/council_log.json and
rendered human-readably to analytics/council-log.md.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime

logger = logging.getLogger("isds.council_log")

_JSON = os.path.join("state", "council_log.json")
_MD = os.path.join("analytics", "council-log.md")
_KEEP = 200


def _load() -> list:
    try:
        with open(_JSON, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def _save(entries: list) -> None:
    os.makedirs(os.path.dirname(_JSON), exist_ok=True)
    tmp = _JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, _JSON)


def _security_verdict(security: str) -> str:
    s = (security or "").lower()
    if not s:
        return "no note"
    # The officer says so explicitly when the memo is clean.
    return "clean" if "clean" in s[:160] else "flagged issues"


def append_weekly(date_str: str, seq: int, brief: dict, generated_at: datetime) -> None:
    """Record the weekly council session: deterministic per-member status plus the
    chairman's reconvene minutes (accountability, next steps, escalations)."""
    minutes = brief.get("minutes") or {}
    entry = {
        "ts": generated_at.isoformat(),
        "date": date_str,
        "type": "weekly-council",
        "issue": seq,
        "members": {
            "chairman": "agenda set" if brief.get("_agenda") else "no agenda",
            "analyst": f"memo {len(brief.get('_memo') or '')} chars",
            "security": _security_verdict(brief.get("_security", "")),
            "editor": (f"{len(brief.get('sections') or [])} sections, "
                       f"{len(brief.get('open_threads') or [])} threads"),
        },
        "status": minutes.get("status", ""),
        "accountability": minutes.get("accountability", []),
        "next_steps": minutes.get("next_steps", []),
        "escalations": minutes.get("escalations", []),
    }
    _write(entry)


def append_daily(date_str: str, note: str, detail: dict, generated_at: datetime) -> None:
    """Record a daily researcher check-in with the chairman."""
    entry = {
        "ts": generated_at.isoformat(),
        "date": date_str,
        "type": "daily-checkin",
        "note": note,
        **(detail or {}),
    }
    _write(entry)


def _write(entry: dict) -> None:
    entries = _load()
    entries.insert(0, entry)
    entries = entries[:_KEEP]
    _save(entries)
    _render_md(entries)
    logger.info("council_log: recorded %s entry for %s", entry.get("type"), entry.get("date"))


def _render_md(entries: list) -> None:
    lines = [
        "# Council log — accountability ledger",
        "",
        "Each council session is recorded here, newest first: the weekly reconvene "
        "(per-member assessment, next steps, escalations) and daily researcher check-ins. "
        "This is the chairman's written record for holding the council accountable.",
        "",
    ]
    for e in entries[:60]:
        if e.get("type") == "weekly-council":
            lines.append(f"## {e['date']} — weekly council (issue #{e.get('issue', '?')})")
            if e.get("status"):
                lines.append(f"**Status.** {e['status']}")
            members = e.get("members") or {}
            if members:
                lines.append("**Members.** " + "; ".join(f"{k}: {v}" for k, v in members.items()))
            for a in e.get("accountability", []):
                lines.append(f"- {a.get('member', '?')}: {a.get('assessment', '')}")
            if e.get("next_steps"):
                lines.append("**Next steps.** " + "; ".join(e["next_steps"]))
            if e.get("escalations"):
                lines.append("**Escalations.** " + "; ".join(e["escalations"]))
        else:
            lines.append(f"## {e['date']} — daily check-in")
            lines.append(f"- {e.get('note', '')}")
        lines.append("")
    os.makedirs(os.path.dirname(_MD), exist_ok=True)
    with open(_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
