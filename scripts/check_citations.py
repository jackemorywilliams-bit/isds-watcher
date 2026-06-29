#!/usr/bin/env python3
"""Hallucination checker for prose with citations — extends the deterministic URL
verifier to cover the BRIEF and the METHODOLOGY memo, not just digest URLs.

The council's existing integrity gate (scripts/verify_citations.py) fetches every
http(s) URL a memo cites and classifies it by what the network says. That is the right
control for digest items, whose authority *is* a URL. But the methodology memo and the
research brief also cite bibliographic authorities that carry NO URL — law-review
articles, treatises, awards by case number — e.g.

    (Linos & Carlson, Qualitative Methods for Law Review Writing, 84 U. Chi. L. Rev. 213 (2017))
    Philip Morris Asia Ltd v. Commonwealth of Australia, PCA Case No. 2012-12

A model-written memo can fabricate one of these as easily as a URL, and no network
fetch can confirm or deny it. The honest engineering response is NOT to assert that
such a citation exists (we cannot confirm it) and NOT to assert it is fake (we cannot
confirm that either) — it is to surface it as "needs human verification" so a person
adjudicates the bibliographic record. This module therefore:

  * extracts every http(s) URL and resolves each one via verify_citations (the same
    deterministic fetch the council already trusts);
  * extracts bibliographic citations that have no URL and records them, unjudged, as
    ``needs-human-check`` — never asserting existence it cannot confirm;
  * emits a structured report with counts (verified / minor-issue / needs-human-check)
    and a fabrication hint when a *URL the memo presented as a live source* does not
    resolve (the one signal a network fetch can legitimately raise).

It is model-free and import-guarded: if ``requests`` (and thus the URL resolver) is
unavailable, URL checks degrade to ``needs-human-check`` rather than crashing, so this
never breaks the brief pipeline that calls it.

CLI:
    python scripts/check_citations.py METHODOLOGY.md
prints a per-citation report, the counts, and exits non-zero (3) when a URL looks
fabricated (unreachable). A clean / human-review-only file exits 0.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Reuse the council's deterministic URL resolver. It lives beside this script (scripts/
# is not a package), so make sure scripts/ is importable however we are invoked.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

try:  # guard: a missing resolver must degrade, never crash the caller.
    import verify_citations as _vc
except Exception:  # noqa: BLE001 - import problems must not break the brief pipeline
    _vc = None  # type: ignore[assignment]


# Report verdict vocabulary. We deliberately use a small, stable set so downstream
# (research_brief, the ledger, the memo archive) can rely on it.
VERIFIED = "verified"            # a cited URL that actually resolves (ok)
MINOR_ISSUE = "minor-issue"      # real and reachable but gated (paywalled / rate-limited)
NEEDS_HUMAN = "needs-human-check"  # bibliographic citation w/ no URL, or URL unresolvable
FABRICATION = "fabricated?"      # a URL presented as a live source that does not resolve

# Map the URL resolver's network verdicts onto this module's vocabulary. ``ok`` is the
# only verdict a deterministic fetch can use to *confirm* a source; paywalled is a real
# source we merely cannot read; unreachable is the one fabrication signal.
_URL_VERDICT = {
    "ok": VERIFIED,
    "paywalled": MINOR_ISSUE,
    "unreachable": FABRICATION,
}

# Maximum bibliographic citations recorded (mirrors verify_citations.MAX_URLS spirit so a
# pathological file cannot produce an unbounded report). Generous; memos sit well under it.
MAX_CITATIONS = 200

# A top-level parenthetical citation, e.g.
#   (Linos & Carlson, Qualitative Methods for Law Review Writing, 84 U. Chi. L. Rev. 213 (2017))
#   (Dolzer and Schreuer, Principles of International Investment Law (2nd edition 2012))
# Legal citations nest a year-parenthetical inside the outer one, so we must match the
# OUTER group and tolerate ONE level of nesting — otherwise we capture only the inner
# "(2017)" and lose the author/title that actually identifies the authority. This is the
# bibliographic-authority signature in this corpus (law reviews, treatises, awards). We
# only keep parentheticals that name a publication year and have NO URL inside them — URLs
# are handled separately by the resolver and would double-count.
_YEAR = r"(?:1[89]|20)\d{2}"  # 1800-2099, the plausible publication-year band
# Outer "(...)" allowing single-depth nested "(...)" runs.
_PAREN_RE = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
_HAS_YEAR = re.compile(r"\b" + _YEAR + r"\b")
# A loose "looks like a citation" filter: a parenthetical is bibliographic only if it
# carries a comma (author, title, ...) or a case/reporter marker. Bare "(2017)" alone,
# or "(weighted)", is not a citation.
_CITATION_HINTS = re.compile(
    r",|\bv\.\b|\bCase No\.|\bL\.\s*Rev\.|\bL\.J\.|\bICSID\b|\bPCA\b|\bNeurIPS\b|\bedition\b",
    re.IGNORECASE,
)
_URL_INSIDE = re.compile(r"https?://", re.IGNORECASE)
# A bare date parenthetical — "(Dec. 17, 2015)", "(June 12, 2017)" — is the award/decision
# DATE that hangs off a case citation, not itself a bibliographic authority. Drop it: the
# case it belongs to is captured as its own citation (or as a resolved URL).
_DATE_MONTHS = (r"Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|"
                r"January|February|March|April|June|July|August|September|October|"
                r"November|December")
_BARE_DATE_RE = re.compile(
    r"^(?:" + _DATE_MONTHS + r")\.?\s+\d{1,2},?\s+" + _YEAR + r"$", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    """The distinct http(s) URLs in ``text`` — delegated to the council's resolver so URL
    extraction stays identical to the digest path. Empty list if the resolver is absent."""
    if _vc is None:
        return []
    try:
        return _vc.extract_urls(text)
    except Exception:  # noqa: BLE001 - extraction must never raise to the caller
        return []


def extract_bibliographic(text: str) -> list[str]:
    """Distinct URL-less bibliographic citations in ``text`` — parentheticals that name a
    publication year and look like a citation (comma / "v." / reporter / case-number /
    "edition"), excluding any parenthetical that itself contains a URL (those are covered
    by the URL resolver). First-seen order, de-duplicated, capped at ``MAX_CITATIONS``.

    NEVER asserts these are real or fake; it only collects what a human must verify."""
    seen: set[str] = set()
    out: list[str] = []
    try:
        candidates = _PAREN_RE.findall(text or "")
    except Exception:  # noqa: BLE001 - extraction must never raise
        return []
    for raw in candidates:
        if _URL_INSIDE.search(raw):
            continue  # the resolver handles URLs; don't double-count
        # The corpus packs several authorities into one parenthetical, separated by ";"
        # (e.g. "(Mercurio, ...; Correa & Viñuales, ...)"). Treat each as its own citation
        # so a person verifies them individually.
        for piece in raw.split(";"):
            cite = " ".join(piece.split()).strip().rstrip(".,;")
            if not cite or cite in seen:
                continue
            if not _HAS_YEAR.search(cite):
                continue  # only year-bearing pieces are bibliographic authorities
            if _BARE_DATE_RE.match(cite):
                continue  # an award/decision date, not an authority of its own
            if not _CITATION_HINTS.search(cite):
                continue  # a bare year / one-word piece is not a citation
            seen.add(cite)
            out.append(cite)
            if len(out) >= MAX_CITATIONS:
                return out
    return out


def check_text(text: str) -> dict:
    """Run the full hallucination check over ``text`` and return a STRUCTURED report:

        {
          "url_results":  [ {"url", "status", "verdict", "detail"}, ... ],
          "bibliographic": [ {"citation", "verdict"="needs-human-check"}, ... ],
          "counts": {"verified", "minor_issue", "needs_human_check", "fabricated"},
          "fabrication_suspected": bool,   # a URL presented as live did not resolve
          "summary": "..."                 # one-line tally
        }

    Model-free. NEVER raises — any internal failure yields an empty-but-valid report so a
    caller (the brief pipeline) can record it without a try/except of its own."""
    try:
        urls = extract_urls(text)
        url_results: list[dict] = []
        for u in urls:
            if _vc is None:
                # No resolver available: we cannot confirm the URL, so it needs a human —
                # NOT a fabrication claim (absence of a fetch is not evidence of a fake).
                url_results.append({"url": u, "status": None,
                                    "verdict": NEEDS_HUMAN, "detail": "resolver unavailable"})
                continue
            net = _vc._check_one(u)  # {"url","status","verdict","detail"} (never raises)
            mapped = _URL_VERDICT.get(net.get("verdict"), NEEDS_HUMAN)
            url_results.append({"url": net.get("url", u), "status": net.get("status"),
                                "verdict": mapped, "detail": net.get("detail", "")})

        biblio = [{"citation": c, "verdict": NEEDS_HUMAN}
                  for c in extract_bibliographic(text)]
    except Exception:  # noqa: BLE001 - the whole check must never raise to the caller
        return {"url_results": [], "bibliographic": [],
                "counts": {"verified": 0, "minor_issue": 0,
                           "needs_human_check": 0, "fabricated": 0},
                "fabrication_suspected": False,
                "summary": "Citation check unavailable."}

    verified = sum(1 for r in url_results if r["verdict"] == VERIFIED)
    minor = sum(1 for r in url_results if r["verdict"] == MINOR_ISSUE)
    fabricated = sum(1 for r in url_results if r["verdict"] == FABRICATION)
    # needs-human covers URL-less citations PLUS any URL we could not resolve at all.
    needs_human = len(biblio) + sum(1 for r in url_results if r["verdict"] == NEEDS_HUMAN)

    report = {
        "url_results": url_results,
        "bibliographic": biblio,
        "counts": {
            "verified": verified,
            "minor_issue": minor,
            "needs_human_check": needs_human,
            "fabricated": fabricated,
        },
        "fabrication_suspected": fabricated > 0,
        "summary": summarize_counts(verified, minor, needs_human, fabricated),
    }
    return report


def summarize_counts(verified: int, minor: int, needs_human: int, fabricated: int) -> str:
    """One-line tally, e.g.
    'Citations checked: 12 — 5 verified, 2 minor-issue, 4 needs-human-check, 1 fabricated?'."""
    total = verified + minor + needs_human + fabricated
    if total == 0:
        return "Citations checked: 0 — none cited."
    parts = [f"{verified} verified", f"{minor} minor-issue",
             f"{needs_human} needs-human-check"]
    if fabricated:
        parts.append(f"{fabricated} fabricated?")
    return f"Citations checked: {total} — " + ", ".join(parts)


def check_file(path: str) -> dict:
    """Read ``path`` and run :func:`check_text` over it. NEVER raises — an unreadable file
    yields an empty-but-valid report with the read error noted in ``summary``."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return {"url_results": [], "bibliographic": [],
                "counts": {"verified": 0, "minor_issue": 0,
                           "needs_human_check": 0, "fabricated": 0},
                "fabrication_suspected": False,
                "summary": f"Citation check unavailable (cannot read {path}: {exc})."}
    return check_text(text)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python scripts/check_citations.py <file.md>", file=sys.stderr)
        return 2
    report = check_file(argv[1])

    url_results = report["url_results"]
    if url_results:
        width = max(len(r["verdict"]) for r in url_results)
        print("URLs:")
        for r in url_results:
            status = r["status"] if r["status"] is not None else "—"
            detail = f"  ({r['detail']})" if r.get("detail") else ""
            print(f"  {r['verdict']:<{width}}  [{status}]  {r['url']}{detail}")

    biblio = report["bibliographic"]
    if biblio:
        print("\nBibliographic citations (no URL — needs human verification):")
        for b in biblio:
            print(f"  needs-human-check  {b['citation']}")

    print()
    print(report["summary"])
    if report["fabrication_suspected"]:
        # A URL the file presented as a live source did not resolve: the one fabrication
        # signal a deterministic fetch can legitimately raise. Non-zero hint for callers.
        print("HINT: at least one cited URL did not resolve — possible fabrication; "
              "verify before relying on it.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
