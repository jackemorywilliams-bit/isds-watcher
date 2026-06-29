#!/usr/bin/env python3
"""Email the day's council meeting record to the configured recipients.

The daily chairman + researcher meeting runs on Claude Max (a scheduled routine) and
commits its record to analytics/daily-research/<DATE>.md. This script, run by a daily
GitHub Actions cron after that, reads the day's record and emails it over SMTP. It uses
no model API, so it adds no API cost; it only needs the SMTP secrets.

The cron fires several times a day because the routine can finish at an unpredictable
hour. The script therefore reports one of THREE states and acts accordingly:

  FOUND       — the day's record exists. Email it (once per day; later crons skip it
                via a marker file so the same record is not mailed repeatedly).
  NOT-YET     — no record yet and it is still early in the day. Send nothing (quiet)
                unless --note is passed, in which case send a low-key "pending" note.
  ESCALATION  — no record and it is late in the day (--escalate, used by the late
                fallback cron). Send an ALERT-subject email so a missing meeting is
                noticed by end of day.

De-duplication: once a record is emailed, a marker file is written under
analytics/daily-research/.sent/<DATE> so the next cron of the day does not re-send.

Run:        python scripts/send_daily_update.py
Late cron:  python scripts/send_daily_update.py --escalate
"""

from __future__ import annotations

import argparse
import datetime
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config  # noqa: E402
from src.email_send import send_digest  # noqa: E402

# Optional citation-check footer. scripts/verify_citations.py is built by a parallel
# workstream and may not exist yet; guard the import so this script works either way.
try:  # noqa: SIM105
    from scripts import verify_citations as _verify_citations  # type: ignore  # noqa: E402
except Exception:  # noqa: BLE001 - absent or broken module must never block the email
    _verify_citations = None

ROUTINE_URL = "https://claude.ai/code/routines/trig_01S6o2XK2D11Smk8zmNEN1Qt"

DAILY_DIR = os.path.join("analytics", "daily-research")
SENT_MARKER_DIR = os.path.join(DAILY_DIR, ".sent")


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
    path = os.path.join(DAILY_DIR, f"{date_str}.md")
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


def _already_sent(date_str: str) -> bool:
    return os.path.exists(os.path.join(SENT_MARKER_DIR, date_str))


def _mark_sent(date_str: str) -> None:
    """Record that today's email went out, so later crons de-duplicate."""
    try:
        os.makedirs(SENT_MARKER_DIR, exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(os.path.join(SENT_MARKER_DIR, date_str), "w", encoding="utf-8") as fh:
            fh.write(stamp + "\n")
    except Exception as exc:  # noqa: BLE001 - a failed marker must not crash the run
        print(f"warning: could not write sent marker ({exc})")


def _citation_footer(record: str) -> str:
    """One-line citation-check footer, only if verify_citations is available."""
    if _verify_citations is None:
        return ""
    for fn_name in ("summarize_line", "summary_line", "check_text", "verify_text"):
        fn = getattr(_verify_citations, fn_name, None)
        if callable(fn):
            try:
                line = str(fn(record)).strip()
                if line:
                    return f"\n\n---\n\n**Citation check:** {line}"
            except Exception as exc:  # noqa: BLE001 - footer is best-effort only
                return f"\n\n---\n\n**Citation check:** unavailable ({exc})"
    return ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Email the daily council meeting record.")
    ap.add_argument("--escalate", action="store_true",
                    help="late fallback: if no record, send an ALERT, not a quiet note")
    ap.add_argument("--note", action="store_true",
                    help="when no record and not escalating, still send a quiet pending note")
    args = ap.parse_args(argv)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    record = _find_record(date_str)

    # State 1 — FOUND.
    if record:
        if _already_sent(date_str):
            print(f"state:      FOUND (already sent today — skipping)")
            print(f"record:     found")
            print(f"sent:       skipped (de-duplicated)")
            return 0
        subject = f"ISDS Daily Council Meeting — {date_str}"
        body_html = _md_to_html(record + _citation_footer(record))
        cfg = config.load_config()
        ok = send_digest(body_html, subject, cfg)
        if ok:
            _mark_sent(date_str)
        print(f"state:      FOUND")
        print(f"subject:    {subject}")
        print(f"record:     found")
        print(f"recipients: {config.RECIPIENTS}")
        print(f"sent:       {ok}")
        return 0 if ok else 1

    # State 3 — ESCALATION (late, still missing).
    if args.escalate:
        subject = f"ISDS Daily Council Meeting — {date_str} — ALERT: no record by end of day"
        body_html = _md_to_html(
            f"# ALERT — no daily council record for {date_str}\n\n"
            "It is late in the day and **no chairman + researcher meeting record** was "
            "found in the repository for today.\n\n"
            "The meeting runs at 11:00 UTC on Claude Max. A missing record by now usually "
            "means the routine did not run, or could not push its work back to the "
            "repository (grant the Claude GitHub app write access if this recurs).\n\n"
            f"You can read today's session directly at {ROUTINE_URL} .")
        cfg = config.load_config()
        ok = send_digest(body_html, subject, cfg)
        print(f"state:      ESCALATION")
        print(f"subject:    {subject}")
        print(f"record:     NOT found")
        print(f"recipients: {config.RECIPIENTS}")
        print(f"sent:       {ok}")
        return 0 if ok else 1

    # State 2 — NOT-YET (early, no record). Quiet by default.
    if not args.note:
        print(f"state:      NOT-YET")
        print(f"record:     NOT found")
        print(f"sent:       nothing (quiet — record may still be on its way)")
        return 0

    subject = f"ISDS Daily Council Meeting — {date_str} (pending)"
    body_html = _md_to_html(
        f"# ISDS Daily Council Meeting — {date_str} (pending)\n\n"
        "No meeting record has landed yet. The chairman + researcher meeting runs at "
        "11:00 UTC on Claude Max; the record is mailed automatically once it is committed. "
        f"You can read today's session directly at {ROUTINE_URL} .")
    cfg = config.load_config()
    ok = send_digest(body_html, subject, cfg)
    print(f"state:      NOT-YET (note)")
    print(f"subject:    {subject}")
    print(f"record:     NOT found")
    print(f"recipients: {config.RECIPIENTS}")
    print(f"sent:       {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
