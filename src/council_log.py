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
import re
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


def _security_verdict(brief: dict) -> str:
    """The ledger's security verdict, read from the officer's STRUCTURED boolean
    (``brief["_security_clean"]``) rather than substring-sniffing the free-text note.
    Reports the issue count when the memo was flagged."""
    clean = brief.get("_security_clean")
    if clean is None:
        # No structured verdict recorded (older brief / verdict step skipped).
        return "no verdict" if not brief.get("_security") else "note only"
    if clean:
        return "clean"
    n = len(brief.get("_security_issues") or [])
    return f"flagged ({n} issue{'' if n == 1 else 's'})" if n else "flagged issues"


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
            "security": _security_verdict(brief),
            "editor": (f"{len(brief.get('sections') or [])} sections, "
                       f"{len(brief.get('open_threads') or [])} threads"),
        },
        "status": minutes.get("status", ""),
        "accountability": minutes.get("accountability", []),
        "next_steps": minutes.get("next_steps", []),
        "escalations": minutes.get("escalations", []),
        # A stub entry (reconvene stage failed) must be self-describing, so every
        # downstream reader — this log's md render, the Monday review packet —
        # can surface the failure instead of silently showing nothing.
        "minutes_missing": not minutes,
    }
    if entry["minutes_missing"]:
        logger.error("council_log: weekly entry for %s recorded WITHOUT chairman "
                     "minutes (reconvene stage failed)", date_str)
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


_SECTION_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — ", re.M)


def _handwritten_sections(path: str, generated_dates: set) -> list[str]:
    """Return `## <date> — …` sections of the existing .md that this run would destroy.

    WHY THIS EXISTS. `_render_md` rewrites the file from `state/council_log.json`,
    which keeps only `_KEEP` entries and only those the pipeline itself wrote. On
    2026-08-06 the JSON held 7 sessions and the .md held 16: nine daily sittings had
    been written by hand, directly into the .md, and the next successful weekly run
    would have silently deleted all nine. The file is the chairman's accountability
    record — the one artifact whose whole purpose is that it cannot be quietly
    rewritten.

    So: any dated section already in the file whose date the generator is not about
    to emit is human-authored, and is carried through verbatim. Generated sections
    are refreshed from the JSON as before, because the JSON is authoritative for
    those.
    """
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    marks = list(_SECTION_RE.finditer(body))
    kept = []
    for i, m in enumerate(marks):
        if m.group(1) in generated_dates:
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        kept.append(body[m.start():end].rstrip())
    return kept


def _render_md(entries: list) -> None:
    generated_dates = {e.get("date") for e in entries[:60]}
    carried = _handwritten_sections(_MD, generated_dates)
    if carried:
        logger.info("council_log: carrying %d hand-written section(s) through the rewrite",
                    len(carried))
    lines = [
        "# Council log — accountability ledger",
        "",
        "Each council session is recorded here, newest first: the weekly reconvene "
        "(per-member assessment, next steps, escalations) and daily researcher check-ins. "
        "This is the chairman's written record for holding the council accountable.",
        "",
        "Sections whose date appears in `state/council_log.json` are regenerated from it "
        "on every run. Sections written by hand are preserved verbatim — see "
        "`_handwritten_sections` in `src/council_log.py`.",
        "",
    ]
    for e in entries[:60]:
        if e.get("type") == "weekly-council":
            lines.append(f"## {e['date']} — weekly council (issue #{e.get('issue', '?')})")
            if e.get("minutes_missing"):
                lines.append("**MINUTES MISSING.** The chairman reconvene stage failed "
                             "this run; per-member assessment, next steps, and "
                             "escalations were not recorded. See the weekly workflow "
                             "logs for the error.")
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
    for section in carried:
        lines.append(section)
        lines.append("")
    os.makedirs(os.path.dirname(_MD), exist_ok=True)
    with open(_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
