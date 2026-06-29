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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Email the council-prepared human-review draft.")
    ap.add_argument("--max-claims", type=int, default=8, help="cap on sampled claims (default 8)")
    ap.add_argument("--digests", type=int, default=2, help="recent digest folders to sample (default 2)")
    args = ap.parse_args(argv)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    draft = review_prep.build_draft(_ROOT, args.max_claims, args.digests)
    body_md = review_prep.render(draft)

    preamble = (
        f"# ISDS Human-Review Draft — {date_str}\n\n"
        "Council-prepared assisted first pass, sent for your ratification. The automated "
        "source check confirms only that a cited URL resolves — not that it substantiates "
        "the claim. Every sampled claim is listed as verification debt until you sign it off "
        "in HUMAN_REVIEW.md.\n\n---\n\n"
    )
    subject = f"ISDS Human Review — {date_str} (draft for your ratification)"
    body_html = _md_to_html(preamble + body_md)

    cfg = config.load_config()
    ok = send_digest(body_html, subject, cfg)
    print(f"subject:    {subject}")
    print(f"recipients: {config.RECIPIENTS}")
    print(f"sent:       {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
