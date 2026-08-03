#!/usr/bin/env python3
"""Email the archivist's vault-session work log.

The Obsidian archivist runs on its own cadence as a scheduled cloud session: it
audits the vault against the repo, fixes drift it owns, and commits a session
record to ``analytics/vault-sessions/<YYYY-MM-DD>.md``. This script is the other
half — it notices a record that has not been sent and emails it to Emory, so a
session that finds something needing him does not sit unread in the repository.

Why a cron and not a push trigger: bot commits here carry ``[skip ci]``, which
GitHub honours by skipping workflows, so a push-triggered emailer would never
fire on the archivist's own commit. This follows the pattern
``scripts/send_daily_update.py`` already proves — run often, send once, and
record the send with a marker committed back to the repo so the next run on a
fresh checkout can see it.

Run:  python scripts/send_vault_log.py [--dry-run]
Exit: 0 when a log was sent, when there is nothing new to send, or on a clean
      no-op. Non-zero only when a send was attempted and failed.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from src import config  # noqa: E402
from src import email_shell  # noqa: E402
from src.email_send import send_digest  # noqa: E402

VAULT_DIR = os.path.join("analytics", "vault-sessions")
SENT_MARKER_DIR = os.path.join(VAULT_DIR, ".sent")



def _sessions() -> list[str]:
    """Dates of every committed vault-session record, oldest first."""
    try:
        names = os.listdir(VAULT_DIR)
    except OSError:
        return []
    dates = [n[:-3] for n in names
             if n.endswith(".md") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", n[:-3])]
    return sorted(dates)


def _already_sent(date_str: str) -> bool:
    return os.path.exists(os.path.join(SENT_MARKER_DIR, date_str))


def _mark_sent(date_str: str) -> None:
    """Record the send. A failed marker must not crash the run."""
    try:
        os.makedirs(SENT_MARKER_DIR, exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with open(os.path.join(SENT_MARKER_DIR, date_str), "w", encoding="utf-8") as fh:
            fh.write(stamp + "\n")
    except OSError as exc:  # noqa: BLE001
        print(f"warning:    could not write sent marker ({exc})", file=sys.stderr)


def _read(date_str: str) -> str | None:
    try:
        with open(os.path.join(VAULT_DIR, f"{date_str}.md"), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def _unsent() -> list[str]:
    """Every session record with no sent marker, oldest first.

    A backlog is sent oldest-first rather than collapsed to the newest: a session
    that found drift is a record in its own right, and skipping it would lose the
    only notice Emory gets that it happened.
    """
    return [d for d in _sessions() if not _already_sent(d)]


def _needs_attention(record: str) -> int:
    """Count lines the email shell will render as operator-action callouts.

    Delegated to email_shell so the subject-line count can never disagree with
    what the body actually highlights.
    """
    return email_shell.action_line_count(record)


def _lede(record: str, date_str: str) -> str:
    n = _needs_attention(record)
    if n:
        return (f"The archivist audited the vault on {date_str} and flagged "
                f"<strong>{n} item{'s' if n != 1 else ''}</strong> that need you. "
                "Those are marked in the body.")
    return (f"The archivist audited the vault on {date_str}. Nothing needs you — "
            "this is the record that it ran and what it found.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="send-vault-log")
    ap.add_argument("--dry-run", action="store_true",
                    help="render and report, but do not send or mark")
    args = ap.parse_args(argv)

    pending = _unsent()
    if not pending:
        print("state:      NOTHING-NEW")
        print(f"sessions:   {len(_sessions())} on file, all sent")
        return 0

    cfg = config.load_config()
    failures = 0

    for date_str in pending:
        record = _read(date_str)
        if not record:
            print(f"state:      UNREADABLE ({date_str}) — skipped")
            continue

        n = _needs_attention(record)
        subject = f"ISDS Vault Session — {date_str}"
        if n:
            subject += f" ({n} need{'s' if n == 1 else ''} you)"

        body_html = email_shell.render(
            record,
            title="Vault Session",
            kicker="ISDS Thematic Watcher",
            issue=date_str,
            lede=_lede(record, date_str),
            footer=("The archivist keeps every agent's recorded context current. "
                    "It fixes what it owns and escalates what it does not."),
        )

        if args.dry_run:
            print(f"state:      DRY-RUN ({date_str}); {n} attention item(s); "
                  f"{len(body_html)} bytes rendered")
            continue

        ok = send_digest(body_html, subject, cfg)
        print(f"state:      {'SENT' if ok else 'FAILED'} ({date_str})")
        print(f"subject:    {subject}")
        if ok:
            _mark_sent(date_str)
        else:
            failures += 1

    print(f"recipients: {config.RECIPIENTS}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
