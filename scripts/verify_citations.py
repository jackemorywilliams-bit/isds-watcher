#!/usr/bin/env python3
"""Deterministic citation verifier — the anti-hallucination control for the research
council that no model provides.

The weekly council's only integrity gate is a model self-reporting that its citations
are "verified" plus a same-model security officer reasoning about plausibility from the
memo text — NOTHING in that loop ever fetches a cited URL. This module closes that gap
deterministically: it extracts every http(s) URL from a memo/brief and actually fetches
each one, classifying it by what the network says rather than what a model claims.

No model is involved. It is pure ``requests``: a short-timeout GET per distinct URL with
a real User-Agent, following redirects, catching every exception. It NEVER raises to the
caller — failures are returned as structured ``unreachable`` results so a verifier
problem can never break brief generation.

CLI:
    python scripts/verify_citations.py <file.md>
prints a per-URL report and the one-line summary.
"""

from __future__ import annotations

import re
import sys

try:  # requests is a hard dependency (requirements.txt); degrade gracefully if absent.
    import requests
except Exception:  # noqa: BLE001 - never let an import problem break the caller
    requests = None  # type: ignore[assignment]

# A short, polite per-request timeout (connect, read). The verifier runs inline in the
# weekly job, so it must be fast and must never hang the run.
TIMEOUT = (5, 8)
# A real browser-ish UA: many publishers reject the bare python-requests default.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 ISDS-Watcher/citation-verify"
)
# Cap the number of distinct URLs checked per run so a memo full of links can't blow up
# the run's wall-clock time. The memo + a handful of supplemental links sit well under it.
MAX_URLS = 25

# Match http(s) URLs in markdown/prose. Trailing punctuation and a wrapping ")" / "]" /
# ">" (markdown link / angle-bracket autolink) are trimmed below so we fetch the bare URL.
_URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+", re.IGNORECASE)
_TRAILING = ".,;:!?—–'\"”’)]>"


def extract_urls(text: str) -> list[str]:
    """Return the distinct http(s) URLs in ``text``, in first-seen order, with trailing
    prose punctuation stripped. De-duplicated, capped at ``MAX_URLS``."""
    seen: set[str] = set()
    out: list[str] = []
    for raw in _URL_RE.findall(text or ""):
        url = raw.rstrip(_TRAILING)
        if not url or url in seen:
            continue
        seen.add(url)
        out.append(url)
        if len(out) >= MAX_URLS:
            break
    return out


def _classify(status: int) -> str:
    if 200 <= status < 300:
        return "ok"
    if status in (401, 403, 429):
        # 401/403 = login/blocked; 429 = rate-limited. The URL is real and reachable —
        # treat as paywalled/gated, not a fabrication signal.
        return "paywalled"
    return "unreachable"


def _check_one(url: str) -> dict:
    """Fetch a single URL and classify it. Never raises — any failure is ``unreachable``."""
    if requests is None:
        return {"url": url, "status": None, "verdict": "unreachable",
                "detail": "requests unavailable"}
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    try:
        resp = requests.get(url, timeout=TIMEOUT, allow_redirects=True,
                            headers=headers, stream=True)
        status = resp.status_code
        try:
            resp.close()
        except Exception:  # noqa: BLE001
            pass
        return {"url": url, "status": status, "verdict": _classify(status), "detail": ""}
    except Exception as exc:  # noqa: BLE001 - timeout / DNS / connection / anything
        return {"url": url, "status": None, "verdict": "unreachable",
                "detail": type(exc).__name__}


def verify_text(text: str) -> list[dict]:
    """Extract every distinct http(s) URL in ``text`` and fetch each, returning a list of
    ``{"url", "status", "verdict", "detail"}`` dicts (``verdict`` in {ok, paywalled,
    unreachable}). Sequential and polite. NEVER raises — returns ``[]`` if anything in
    the extraction step itself fails."""
    try:
        urls = extract_urls(text)
    except Exception:  # noqa: BLE001 - extraction must never raise to the caller
        return []
    return [_check_one(u) for u in urls]


def summarize(results: list[dict]) -> str:
    """One-line tally, e.g. 'Citations checked: 7 — 5 ok, 1 paywalled, 1 unreachable'."""
    n = len(results or [])
    if n == 0:
        return "Citations checked: 0 — none cited."
    ok = sum(1 for r in results if r.get("verdict") == "ok")
    pay = sum(1 for r in results if r.get("verdict") == "paywalled")
    un = sum(1 for r in results if r.get("verdict") == "unreachable")
    return f"Citations checked: {n} — {ok} ok, {pay} paywalled, {un} unreachable"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python scripts/verify_citations.py <file.md>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 2
    results = verify_text(text)
    width = max((len(r["verdict"]) for r in results), default=0)
    for r in results:
        status = r["status"] if r["status"] is not None else "—"
        detail = f"  ({r['detail']})" if r.get("detail") else ""
        print(f"  {r['verdict']:<{width}}  [{status}]  {r['url']}{detail}")
    print(summarize(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
