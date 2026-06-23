#!/usr/bin/env python3
"""Email the day's council meeting record to the configured recipients.

The daily chairman + researcher meeting runs on Claude Max (a scheduled routine) and
commits its record to analytics/daily-research/<DATE>.md. This script, run by a daily
GitHub Actions cron after that, reads the day's record and emails it over SMTP. It uses
no model API, so it adds no API cost; it only needs the SMTP secrets.

If no record is found for today (e.g. the routine could not push its work yet), it sends
a short honest status note instead, so the daily email always tells you where things
stand.

Run:  python scripts/send_daily_update.py
"""

from __future__ import annotations

import datetime
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config  # noqa: E402
from src.email_send import send_digest  # noqa: E402

ROUTINE_URL = "https://claude.ai/code/routines/trig_01S6o2XK2D11Smk8zmNEN1Qt"


def _md_to_html(md: str) -> str:
    """Small, safe Markdown -> HTML for the meeting record (headings, links, bullets)."""
    out, in_list = [], False
    for raw in md.splitlines():
        line = html.escape(raw)
        line = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
                      r'<a href="\2">\1</a>', line)
        line = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", line)
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            if in_list:
                out.append("</ul>"); in_list = False
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
        elif re.match(r"^\s*[-*]\s+", line):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>" + re.sub(r"^\s*[-*]\s+", "", line) + "</li>")
        elif line.strip():
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<p>{line}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def _find_record(date_str: str) -> str | None:
    path = os.path.join("analytics", "daily-research", f"{date_str}.md")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip() or None
    # Fallback: today's section in the council log.
    log = os.path.join("analytics", "council-log.md")
    if os.path.exists(log):
        with open(log, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(rf"^##\s+{re.escape(date_str)}\b.*?(?=^##\s|\Z)", text, re.S | re.M)
        if m:
            return m.group(0).strip()
    return None


def main() -> int:
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    record = _find_record(date_str)

    if record:
        subject = f"ISDS Daily Council Meeting — {date_str}"
        body_html = _md_to_html(record)
    else:
        subject = f"ISDS Daily Council Meeting — {date_str} (no record yet)"
        body_html = _md_to_html(
            f"# ISDS Daily Council Meeting — {date_str}\n\n"
            "No meeting record was found in the repository for today.\n\n"
            "The chairman + researcher meeting runs at 11:00 UTC on Claude Max. If this "
            "keeps happening, the routine most likely cannot push its record back to the "
            "repository yet — grant the Claude GitHub app write access to the repo so its "
            f"work is saved. You can read today's session directly at {ROUTINE_URL} .")

    cfg = config.load_config()
    ok = send_digest(body_html, subject, cfg)
    print(f"subject:    {subject}")
    print(f"record:     {'found' if record else 'NOT found'}")
    print(f"recipients: {config.RECIPIENTS}")
    print(f"sent:       {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
