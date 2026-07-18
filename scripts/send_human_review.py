#!/usr/bin/env python3
"""Email the council-prepared human-review DRAFT to the operator for ratification.

Human review is offered as a delivered artifact, not a file to hunt for: this runs the
assisted first pass (scripts/review_prep.py) over the recent record — sampling cited
claims and running the deterministic citation check — renders the draft log entry, and
emails it over SMTP. It is explicitly a council-prepared DRAFT pending the operator's
sign-off; the automated check confirms only that a URL resolves, never that it
substantiates the claim. SMTP only — no model API, so no API cost.

Run:        python scripts/send_human_review.py
Weekly:     fired every Monday by .github/workflows/human-review.yml (and on demand).
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

from src import config  # noqa: E402
from src.email_send import send_digest  # noqa: E402
import review_prep  # noqa: E402  scripts/review_prep.py — the assisted first pass

# Reuse the daily updater's small, safe Markdown -> HTML converter for a consistent look.
try:  # noqa: SIM105
    from send_daily_update import _md_to_html  # type: ignore  # noqa: E402
except Exception:  # noqa: BLE001 - fall back to a trivial converter if unavailable
    import html as _html

    def _md_to_html(md: str) -> str:  # type: ignore
        return "<pre style='white-space:pre-wrap;font-family:inherit'>" + _html.escape(md) + "</pre>"


def _latest_record(dirname: str) -> tuple[str, str] | None:
    """Newest (date, contents) markdown record in analytics/<dirname>/, or None.
    Records are committed by the Monday/daily Max routine; absence must never
    block the email — the packet simply says the section is pending."""
    d = os.path.join(_ROOT, "analytics", dirname)
    try:
        names = sorted(n for n in os.listdir(d) if n.endswith(".md"))
    except OSError:
        return None
    if not names:
        return None
    path = os.path.join(d, names[-1])
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return names[-1][:-3], fh.read().strip()
    except OSError:
        return None


def _state_of_answer_snapshot(max_chars: int = 1500) -> str:
    """The head of STATE_OF_THE_ANSWER.md (question, seeds, last-updated) as the
    packet's research-question status anchor."""
    try:
        with open(os.path.join(_ROOT, "STATE_OF_THE_ANSWER.md"), encoding="utf-8") as fh:
            head = fh.read(max_chars)
        return head.rsplit("\n", 1)[0]
    except OSError:
        return "(STATE_OF_THE_ANSWER.md unavailable)"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Email the operator's Monday review packet.")
    ap.add_argument("--max-claims", type=int, default=8, help="cap on sampled claims (default 8)")
    ap.add_argument("--digests", type=int, default=2, help="recent digest folders to sample (default 2)")
    args = ap.parse_args(argv)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    draft = review_prep.build_draft(_ROOT, args.max_claims, args.digests)
    review_md = review_prep.render(draft)

    # Assemble the Monday packet the operator asked for: roundtable overview,
    # workflow-optimization suggestions, research-question status, then review buckets.
    parts: list[str] = [
        f"# ISDS Monday Review Packet — {date_str}\n",
        "Everything that needs your eyes this week, in plain language: what the council "
        "discussed, how the instrument can improve, where the research question stands, "
        "and the few checks only you can do. Sent to you only — the digest for "
        "Dr. Benavides goes separately.\n\n---\n",
    ]

    rt = _latest_record("roundtable")
    if rt:
        parts.append(f"## 1. This week's council roundtable ({rt[0]})\n\n{rt[1]}\n\n---\n")
    else:
        parts.append("## 1. This week's council roundtable\n\nNo roundtable record has "
                     "landed yet this week — the Monday council session runs before this "
                     "email; if this keeps happening, the routine needs attention.\n\n---\n")

    sysres = _latest_record("systems-research")
    if sysres:
        parts.append(f"## 2. Workflow improvement suggestions ({sysres[0]})\n\n{sysres[1]}\n\n---\n")
    else:
        parts.append("## 2. Workflow improvement suggestions\n\nNo systems-research note "
                     "yet this week.\n\n---\n")

    parts.append(f"## 3. Where the research question stands\n\n{_state_of_answer_snapshot()}\n\n"
                 "Full detail: STATE_OF_THE_ANSWER.md in the repository.\n\n---\n")

    parts.append(f"## 4. Your checks\n\n{review_md}")

    subject = f"ISDS Monday Review Packet — {date_str}"
    body_html = _md_to_html("\n".join(parts))

    cfg = config.load_config()
    ok = send_digest(body_html, subject, cfg)
    print(f"subject:    {subject}")
    print(f"recipients: {config.RECIPIENTS}")
    print(f"sent:       {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
