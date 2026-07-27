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


def _latest_weekly_council(root: str = None, max_age_days: int = 7) -> dict:
    """The council roundtable section, read DETERMINISTICALLY from the council's own
    accountability record (state/council_log.json) — the record the weekly pipeline
    actually writes — never from a side-channel directory that nothing populates.

    Returns {"markdown": str, "fresh": bool, "complete": bool}. Three explicit states,
    each rendered loudly rather than silently degrading (the 2026-07-20 regression:
    the packet read analytics/roundtable/, which nothing has ever written, so the
    council session never reached the operator):
      * fresh + complete  — the full minutes render (status, members, per-member
        accountability, next steps, escalations).
      * fresh + stub      — the session ran but the chairman minutes failed; the
        packet says so and points at the workflow logs.
      * stale/absent      — no weekly entry within ``max_age_days``; the packet
        flags the pipeline itself.
    """
    import json as _json

    root = root or _ROOT
    try:
        with open(os.path.join(root, "state", "council_log.json"), encoding="utf-8") as fh:
            entries = _json.load(fh)
    except (OSError, ValueError):
        entries = []
    weekly = next((e for e in entries if isinstance(e, dict)
                   and e.get("type") == "weekly-council"), None)
    if weekly:
        try:
            age = (datetime.date.today()
                   - datetime.date.fromisoformat(weekly.get("date", "1970-01-01"))).days
        except ValueError:
            age = 10_000
    if not weekly or age > max_age_days:
        return {"fresh": False, "complete": False, "markdown": (
            "**No weekly council session found in the accountability record for the "
            "past week.** The Monday council either did not run or did not record — "
            "check the weekly workflow before trusting this packet's coverage.")}
    md: list[str] = [f"Weekly council of {weekly['date']} (issue #{weekly.get('issue', '?')})."]
    members = weekly.get("members") or {}
    if members:
        md.append("**Members.** " + "; ".join(f"{k}: {v}" for k, v in members.items()))
    complete = not weekly.get("minutes_missing") and bool(
        weekly.get("status") or weekly.get("accountability"))
    if not complete:
        md.append("**The chairman's minutes are MISSING for this session** — the "
                  "reconvene stage failed, so per-member assessment, next steps, and "
                  "escalations were not recorded. The session's substance is still in "
                  f"briefs/{weekly['date']}-memo.md; the failure needs attention in "
                  "the weekly workflow logs.")
        return {"fresh": True, "complete": False, "markdown": "\n\n".join(md)}
    if weekly.get("status"):
        md.append(f"**Status.** {weekly['status']}")
    for a in weekly.get("accountability", []):
        md.append(f"- **{a.get('member', '?')}**: {a.get('assessment', '')}")
    if weekly.get("next_steps"):
        md.append("**Next steps.** " + " ".join(f"({i}) {s}" for i, s in
                                                enumerate(weekly["next_steps"], 1)))
    if weekly.get("escalations"):
        md.append("**Escalations for you.** " + " ".join(
            f"({i}) {s}" for i, s in enumerate(weekly["escalations"], 1)))
    return {"fresh": True, "complete": True, "markdown": "\n\n".join(md)}


def _optimization_snapshot(max_ideas: int = 3, max_chars_each: int = 900) -> str:
    """The newest ideas from analytics/optimization-log.md (dated bullets, newest
    first), each truncated for email length. Empty string when the log is absent."""
    try:
        with open(os.path.join(_ROOT, "analytics", "optimization-log.md"),
                  encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return ""
    ideas: list[str] = []
    current: list[str] = []
    in_ideas = False
    for line in text.splitlines():
        if line.startswith("## Ideas"):
            in_ideas = True
            continue
        if not in_ideas:
            continue
        if line.startswith("- "):
            if current:
                ideas.append("\n".join(current))
            current = [line]
        elif current and line.strip():
            current.append(line)
    if current:
        ideas.append("\n".join(current))
    out = []
    for idea in ideas[:max_ideas]:
        if len(idea) > max_chars_each:
            idea = idea[:max_chars_each].rsplit(" ", 1)[0] + " … (truncated; full text in analytics/optimization-log.md)"
        out.append(idea)
    return "\n".join(out)


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

    # Council roundtable: the accountability record (state/council_log.json) is the
    # source of truth; an analytics/roundtable/ note, if one ever lands, is appended
    # as a supplement rather than being the only (never-populated) source.
    council = _latest_weekly_council()
    parts.append(f"## 1. This week's council roundtable\n\n{council['markdown']}\n")
    rt = _latest_record("roundtable")
    if rt:
        parts.append(f"\nSupplemental roundtable note ({rt[0]}):\n\n{rt[1]}\n")
    parts.append("\n---\n")

    # Workflow improvements: systems-research notes if present, otherwise the
    # optimization log + the newest daily research note — records that DO exist.
    sysres = _latest_record("systems-research")
    if sysres:
        parts.append(f"## 2. Workflow improvement suggestions ({sysres[0]})\n\n{sysres[1]}\n\n---\n")
    else:
        opt = _optimization_snapshot()
        daily = _latest_record("daily-research")
        parts.append("## 2. Workflow improvement suggestions\n\n")
        if opt:
            parts.append(f"From the optimization log:\n\n{opt}\n")
        if daily:
            parts.append(f"\nLatest daily research note ({daily[0]}):\n\n{daily[1]}\n")
        if not opt and not daily:
            parts.append("No optimization-log entries or daily research notes were "
                         "found — the daily routine needs attention.\n")
        parts.append("\n---\n")

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
