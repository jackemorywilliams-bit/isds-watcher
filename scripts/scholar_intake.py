#!/usr/bin/env python3
"""Daily Google Scholar intake: capture alert papers the morning they arrive.

WHY THIS EXISTS. Google Scholar alerts are email-only and arrive around 05:00
UTC. Until 2026-09-08 the only thing that read that mailbox was the weekly run
on Monday 13:00 UTC, so a paper alerted on a Tuesday sat unseen for six days,
and three zero-item weekly runs read as "no Scholar mail in 7 days" while the
operator was holding a fresh alert. This script runs every morning after the
alerts land (``.github/workflows/scholar-intake.yml``).

WHAT IT DOES.
  1. Reads the Scholar alerts of the last ``--days`` days through the same
     source the weekly run uses (``GmailScholarSource.fetch``), so parsing and
     the sender scope are identical.
  2. Queues every paper that is neither already seen nor already queued in
     ``state/deferred.json`` at attempts=0 with an ``intake`` marker. The weekly
     run works the deferred queue FIRST ("ahead of the day's news"), rebuilding
     items the source no longer lists, so nothing captured here can be lost to
     the window and everything is classified by the same model path.
  3. Writes ``analytics/scholar-intake/<date>.json`` — the mailbox evidence:
     how many alerts the account holds in the last 30 days, the newest one's
     date and subject (the operator's own query string), and the URLs queued
     today. No paper titles or snippets here; those live in the queue.

Exit 0 on a clean run (including "nothing new"), 2 when the credentials are
missing — in CI that is a configuration failure and must be loud.

CLI:
    python scripts/scholar_intake.py [--days 3] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from src import state  # noqa: E402
from src.sources import gmail_scholar  # noqa: E402

OUT_DIR = "analytics/scholar-intake"
SOURCE = "gmail_scholar"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Daily Google Scholar intake into the retry queue.")
    ap.add_argument("--days", type=int, default=3, help="alert window in days (default 3)")
    ap.add_argument("--state", default=state.STATE_PATH)
    ap.add_argument("--deferred", default=state.DEFERRED_PATH)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not (os.environ.get("GMAIL_ALERT_USER", "").strip()
            and os.environ.get("GMAIL_ALERT_PASS", "").strip()):
        print("scholar_intake: GMAIL_ALERT_USER / GMAIL_ALERT_PASS are not set; nothing read")
        return 2

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    status, alerts = gmail_scholar.scholar_mailbox_status(30)
    items = gmail_scholar.GmailScholarSource().fetch(since)

    st = state.load_state(args.state)
    dq = state.load_deferred(args.deferred)
    bucket = dq.setdefault(SOURCE, {})
    queued, already_seen, already_queued = [], 0, 0
    for it in items:
        if state.is_seen(st, SOURCE, it.source_id):
            already_seen += 1
            continue
        if it.source_id in bucket:
            already_queued += 1
            continue
        bucket[it.source_id] = {
            "first_deferred": now.isoformat(),
            "attempts": 0,
            "last_outcome": "intake",
            "url": it.url,
            "title": it.title,
            "published": it.published.isoformat() if it.published else "",
            "summary": it.summary or "",
            "intake": {"by": "scholar-intake", "at": now.isoformat(),
                       "window_days": args.days},
        }
        queued.append(it.url)

    newest = alerts[0] if alerts else None
    report = {
        "schema": 1,
        "date": now.strftime("%Y-%m-%d"),
        "at": now.isoformat(),
        "window_days": args.days,
        "mailbox": {
            "status": status,
            "alerts_30d": len(alerts),
            "newest_alert_date": (newest or {}).get("date", ""),
            "newest_alert_subject": (newest or {}).get("subject", ""),
            # Every alert's arrival day, newest first: the direct answer to
            # "did anything arrive between the weekly runs" (2026-09-08).
            "alert_dates": [a["date"][:10] for a in alerts if a.get("date")],
        },
        "papers_in_window": len(items),
        "queued_new": len(queued),
        "already_seen": already_seen,
        "already_queued": already_queued,
        "queued_urls": queued,
    }

    print(f"scholar_intake {report['date']}: mailbox {status}; {len(alerts)} alert(s) in 30d"
          + (f", newest {report['mailbox']['newest_alert_date'][:10]} "
             f"{report['mailbox']['newest_alert_subject']!r}" if newest else "")
          + f"; {len(items)} paper(s) in the last {args.days}d -> "
          f"{len(queued)} queued, {already_seen} already seen, {already_queued} already queued")
    if alerts:
        print("  alert days (30d, newest first): "
              + ", ".join(report["mailbox"]["alert_dates"]))
    for u in queued:
        print(f"  queued  {u}")
    if args.dry_run:
        print("DRY RUN: nothing written")
        return 0

    if queued:
        state.save_deferred(dq, args.deferred)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{report['date']}.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
