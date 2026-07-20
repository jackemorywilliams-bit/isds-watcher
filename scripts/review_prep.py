#!/usr/bin/env python3
"""Assisted first pass for the human-review checkpoint (HUMAN_REVIEW.md, WS6).

This is NOT a human review and it does not pretend to be one. It is a council-
prepared DRAFT: it mechanically samples cited claims (case/claim + URL) from the
recent record — the most recent digest folders (``digests/<date>_*/articles/*.md``
and their ``meta.json``) and any research briefs (``briefs/*.md``) — and runs the
existing deterministic citation checker (``scripts/verify_citations.py``) over the
sampled URLs, classifying each ``ok`` / ``paywalled`` / ``unreachable``.

The automated source-check answers only one narrow question: *does the cited URL
resolve, and is it openable or gated?* It does NOT and CANNOT confirm that the
source says what the claim says, supports the date/holding/figure, or that the
claim is true. Those are exactly the judgements a human must still make. Every URL
that does not come back a clean ``ok`` — and every ``ok`` URL too, on the substance —
is logged as **verification debt** for human eyes. The whole point of this file is
to hand the operator a pre-filled sample and a short, honest debt list, not to
discharge the review.

The checker import is guarded: if ``scripts/verify_citations.py`` is absent or a
function it needs is missing, this degrades to recording the sample with every URL
marked ``unchecked`` (and therefore as verification debt) rather than crashing — a
broken checker must never block preparing the human's worksheet.

CLI:
    python scripts/review_prep.py                  # prints the draft review-log entry
    python scripts/review_prep.py --max-claims 8   # cap the sample size (default 8)
    python scripts/review_prep.py --digests 1      # how many recent digest folders to sample (default 1)
"""

from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import re
import sys

# Make the repo root importable so we can pull in scripts/verify_citations.py the
# same way the other scripts in this repo do (sys.path + package import).
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# --- Guarded import of the deterministic citation checker -------------------------
# verify_citations is the anti-hallucination control. We need verify_text (or, as a
# fallback, _check_one) from it. Guard every name: a missing module OR a missing
# function must degrade gracefully, never raise to the operator preparing a review.
_CHECKER_AVAILABLE = False
_CHECKER_DETAIL = ""
verify_text = None  # type: ignore[assignment]
_check_one = None  # type: ignore[assignment]
try:
    from scripts import verify_citations as _vc  # type: ignore

    verify_text = getattr(_vc, "verify_text", None)
    _check_one = getattr(_vc, "_check_one", None)
    if callable(verify_text) or callable(_check_one):
        _CHECKER_AVAILABLE = True
    else:
        _CHECKER_DETAIL = "verify_citations imported but exposes no usable checker function"
except Exception as exc:  # noqa: BLE001 - a checker import problem must not block review prep
    _CHECKER_DETAIL = f"could not import verify_citations ({type(exc).__name__})"


# --- Parsing the recent record into (claim, url) sampled-claim records ------------

_DIGEST_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_")
# In an article .md: "# 1. Okuashvili v. Georgia" — the heading is the case/claim.
_ARTICLE_TITLE_RE = re.compile(r"^#\s+\d+\.\s+(.*\S)\s*$", re.MULTILINE)
# "- **Link:** https://..." is the canonical cited URL for the item.
_ARTICLE_LINK_RE = re.compile(r"^-\s+\*\*Link:\*\*\s+(https?://\S+)\s*$", re.MULTILINE)
# "- **Date:** 26 June 2026"
_ARTICLE_DATE_RE = re.compile(r"^-\s+\*\*Date:\*\*\s+(.*\S)\s*$", re.MULTILINE)
# "- **Source:** Italaw — ..."
_ARTICLE_SOURCE_RE = re.compile(r"^-\s+\*\*Source:\*\*\s+([^—\n]+?)\s*(?:—|$)", re.MULTILINE)

_URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+", re.IGNORECASE)
_TRAILING = ".,;:!?—–'\"”’)]>"


def _recent_digest_dirs(repo_root: str, n: int) -> list[tuple[str, str]]:
    """Return the ``n`` most recent ``digests/<date>_*/`` folders as (date, path),
    newest first."""
    found: list[tuple[str, str]] = []
    for path in glob.glob(os.path.join(repo_root, "digests", "*_*")):
        if not os.path.isdir(path):
            continue
        m = _DIGEST_DIR_RE.match(os.path.basename(path))
        if m:
            found.append((m.group(1), path))
    found.sort(key=lambda t: t[0], reverse=True)
    return found[:n]


def _read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def _norm_url(raw: str) -> str:
    return (raw or "").rstrip(_TRAILING)


def sample_digest_claims(repo_root: str, n_digests: int) -> list[dict]:
    """Sample cited claims from the most recent digest folder(s).

    Each article .md is one cited claim: the heading is the case/claim, the
    **Link:** line is the cited URL. Returns claim records with source provenance."""
    claims: list[dict] = []
    for date, dpath in _recent_digest_dirs(repo_root, n_digests):
        # Optional context from meta.json (counts only; no URLs live here).
        meta = {}
        meta_raw = _read(os.path.join(dpath, "meta.json"))
        if meta_raw:
            try:
                meta = json.loads(meta_raw)
            except Exception:  # noqa: BLE001
                meta = {}
        article_paths = sorted(glob.glob(os.path.join(dpath, "articles", "*.md")))
        for apath in article_paths:
            text = _read(apath)
            if not text:
                continue
            t = _ARTICLE_TITLE_RE.search(text)
            link = _ARTICLE_LINK_RE.search(text)
            adate = _ARTICLE_DATE_RE.search(text)
            asource = _ARTICLE_SOURCE_RE.search(text)
            title = t.group(1).strip() if t else os.path.basename(apath)
            url = _norm_url(link.group(1)) if link else ""
            paywalled_note = "source paywalled" in text.lower()
            claims.append({
                "claim": title,
                "url": url,
                "origin": f"digest {date} — {os.path.relpath(apath, repo_root)}",
                "item_date": adate.group(1).strip() if adate else "",
                "source": asource.group(1).strip() if asource else "",
                "self_reported_paywalled": paywalled_note,
                "digest_matches": meta.get("matches"),
            })
    return claims


def sample_brief_claims(repo_root: str, limit: int) -> list[dict]:
    """Sample cited URLs from the most recent research brief memo.

    A brief is prose, not structured per-claim, so we treat each distinct cited URL
    as a sampled citation, captioned with a short snippet of its surrounding line so
    the human knows what claim the URL is backing."""
    memos = sorted(glob.glob(os.path.join(repo_root, "briefs", "*-memo.md")), reverse=True)
    if not memos:
        memos = sorted(glob.glob(os.path.join(repo_root, "briefs", "*.md")), reverse=True)
    claims: list[dict] = []
    if not memos:
        return claims
    memo = memos[0]
    text = _read(memo)
    seen: set[str] = set()
    for line in text.splitlines():
        for raw in _URL_RE.findall(line):
            url = _norm_url(raw)
            if not url or url in seen:
                continue
            seen.add(url)
            # Caption the URL with the prose around it, minus the URL itself and
            # markdown bold/heading markers, so the human sees what the citation backs.
            snippet = line.replace(raw, "").strip()
            snippet = re.sub(r"[*_#`>]+", "", snippet).strip(" -—:")
            snippet = re.sub(r"\s+", " ", snippet)
            if len(snippet) > 140:
                snippet = snippet[:137].rstrip() + "..."
            claims.append({
                "claim": f"(brief citation) {snippet}" if snippet else "(brief citation)",
                "url": url,
                "origin": f"brief — {os.path.relpath(memo, repo_root)}",
                "item_date": "",
                "source": "research brief",
                "self_reported_paywalled": False,
                "digest_matches": None,
            })
            if len(claims) >= limit:
                return claims
    return claims


# --- Running the deterministic checker over the sampled URLs -----------------------

def check_url(url: str) -> dict:
    """Run the deterministic citation checker on a single URL. Returns a normalized
    ``{"verdict", "status", "detail"}``. If the checker is unavailable, returns the
    ``unchecked`` verdict rather than guessing — an unchecked URL is verification debt."""
    if not url:
        return {"verdict": "unchecked", "status": None, "detail": "no URL on the cited claim"}
    if not _CHECKER_AVAILABLE:
        return {"verdict": "unchecked", "status": None, "detail": _CHECKER_DETAIL or "checker unavailable"}
    try:
        if callable(_check_one):
            r = _check_one(url)
        else:  # verify_text path: feed it the bare URL and take the single result
            results = verify_text(url)  # type: ignore[misc]
            r = results[0] if results else {}
        verdict = r.get("verdict") or "unchecked"
        return {"verdict": verdict, "status": r.get("status"), "detail": r.get("detail", "")}
    except Exception as exc:  # noqa: BLE001 - the checker promises never to raise, but belt-and-suspenders
        return {"verdict": "unchecked", "status": None, "detail": f"checker raised {type(exc).__name__}"}


def build_draft(repo_root: str, max_claims: int, n_digests: int) -> dict:
    """Sample the record, run the deterministic source-check, and assemble the draft.

    Classifies each sampled claim's automated outcome as a PASS-candidate (the URL
    resolved ``ok``) or a FLAG (paywalled / unreachable / unchecked). A FLAG, and any
    claim whose body is self-reported paywalled, becomes verification debt. Note: even
    an ``ok`` URL only clears the *reachability* check — the human still must confirm the
    source substantiates the claim. This draft never marks a claim verified."""
    digest_claims = sample_digest_claims(repo_root, n_digests)
    remaining = max(0, max_claims - len(digest_claims))
    brief_claims = sample_brief_claims(repo_root, remaining) if remaining else []
    sampled = (digest_claims + brief_claims)[:max_claims]

    for c in sampled:
        c["check"] = check_url(c["url"])

    debt: list[dict] = []
    for c in sampled:
        verdict = c["check"]["verdict"]
        reasons = []
        if verdict != "ok":
            reasons.append(f"automated source-check: {verdict}")
        if c.get("self_reported_paywalled"):
            reasons.append("item body self-reported as paywalled (holding not in record)")
        # An ok URL is reachable, NOT substantiated — always owe the human a substance check.
        if verdict == "ok":
            reasons.append("URL resolves but source-supports-claim NOT machine-verifiable — needs human read")
        if reasons:
            debt.append({"claim": c["claim"], "url": c["url"], "reasons": reasons})

    n = len(sampled)
    ok = sum(1 for c in sampled if c["check"]["verdict"] == "ok")
    pay = sum(1 for c in sampled if c["check"]["verdict"] == "paywalled")
    un = sum(1 for c in sampled if c["check"]["verdict"] == "unreachable")
    unchecked = sum(1 for c in sampled if c["check"]["verdict"] == "unchecked")

    return {
        "generated": datetime.date.today().isoformat(),
        "checker_available": _CHECKER_AVAILABLE,
        "checker_detail": _CHECKER_DETAIL,
        "sampled": sampled,
        "debt": debt,
        "tally": {"n": n, "ok": ok, "paywalled": pay, "unreachable": un, "unchecked": unchecked},
    }


# --- Rendering ---------------------------------------------------------------------

def _verdict_to_automated(verdict: str) -> str:
    """The automated, reachability-only outcome label. Deliberately not 'PASS/FAIL' —
    only a human assigns the real pass/fail."""
    return {
        "ok": "auto: reachable (PASS-candidate, substance unverified)",
        "paywalled": "auto: gated/paywalled (FLAG)",
        "unreachable": "auto: unreachable (FLAG)",
        "unchecked": "auto: NOT CHECKED (FLAG)",
    }.get(verdict, f"auto: {verdict} (FLAG)")


def render(draft: dict) -> str:
    """Render the draft as a PLAIN-LANGUAGE operator review packet with two buckets:
    what the operator can check themselves (open sources) and what to forward (paywalled).
    No jargon, and it never asks the operator to verify something behind a paywall they
    cannot open — per the operator's standing constraint (no paywalled-site access)."""
    today = draft["generated"]
    sampled = draft["sampled"]

    def _openable(c: dict) -> bool:
        # Reachable AND not self-reported paywalled = the operator can actually open it.
        return c["check"]["verdict"] == "ok" and not c.get("self_reported_paywalled")

    openable = [c for c in sampled if _openable(c)]
    gated = [c for c in sampled if not _openable(c)]

    out: list[str] = []
    out.append(f"## Your review packet — {today}")
    out.append("")
    out.append("A few of this period's cited claims, sorted by what you can actually do. "
               "Nothing here is a settled finding — these are research leads, and this is the "
               "one place a human checks them before the project relies on them.")
    out.append("")

    out.append("### You can check these yourself (open sources, ~2 min each)")
    out.append("Open the link and confirm the source really says what the claim says, then "
               "mark it good or wrong.")
    out.append("")
    if not openable:
        out.append("- Nothing openable in this sample.")
    else:
        for i, c in enumerate(openable, 1):
            out.append(f"{i}. **Claim:** {c['claim']}")
            out.append(f"   - Check here: {c['url']}")
            out.append("   - Does the source say this?  [ ] yes   [ ] no — note: __________")
            out.append("")

    out.append("### Forward these to your professor (paywalled — you can't verify them)")
    out.append("These sit behind a paywall or login you don't have, so don't spend time on "
               "them — send them to Dr. Benavides, who can check them.")
    out.append("")
    if not gated:
        out.append("- Nothing paywalled in this sample.")
    else:
        for i, c in enumerate(gated, 1):
            v = c["check"]["verdict"]
            why = ("paywalled" if (v == "paywalled" or c.get("self_reported_paywalled"))
                   else "link didn't resolve" if v == "unreachable"
                   else "not machine-checkable")
            out.append(f"{i}. **Claim:** {c['claim']}")
            out.append(f"   - Source ({why}): {c['url'] or '(no link on record)'}")
            out.append("")

    out.append("### Sign-off (one line)")
    out.append(f"- Reviewed by: __________   Date: __________   "
               f"Open items confirmed good: ____ / {len(openable)}   "
               "Anything wrong to fix: __________")
    out.append("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Council-prepared DRAFT first pass for the human-review checkpoint.")
    ap.add_argument("--max-claims", type=int, default=8, help="cap on sampled claims (default 8)")
    ap.add_argument("--digests", type=int, default=1, help="how many recent digest folders to sample (default 1)")
    ap.add_argument("--json", action="store_true", help="emit the raw draft as JSON instead of the rendered log entry")
    args = ap.parse_args(argv[1:])

    draft = build_draft(_REPO_ROOT, max_claims=args.max_claims, n_digests=args.digests)
    if args.json:
        print(json.dumps(draft, indent=2, ensure_ascii=False))
    else:
        print(render(draft))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
