"""Analytics member of the ISDS research council.

Analyzes which catalogue sources are most *receptive* to the project's thematic
intersection — i.e. which feeds actually surface developments that reach the digest —
so the system can be tuned over time toward sources that yield genuinely on-theme
articles (and away from dead or permanently-capped ones).

It is deterministic (no API): it reads each archived run's meta.json, which records
per-source fresh candidates (`per_source`) and per-source surfaced items
(`accepted_by_source`), plus the surfaced articles themselves. It writes a single
report to analytics/source-receptivity.md.

Honest about its denominator: older runs predate per-source counting, so receptivity
ratios are computed only where the data exists; everywhere else the report falls back
to surfaced-contribution counts and says so.

Run:  python scripts/source_analytics.py
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict

DIGESTS = "digests"
SUFFIX = "_ISDS-Thematic-Watch"
OUT_DIR = "analytics"
OUT = os.path.join(OUT_DIR, "source-receptivity.md")

# Known structural facts about sources, surfaced so the analysis is actionable.
_NOTES = {
    "iareporter_headlines": "headline-only (paywalled body) — capped at watch-list leads.",
    "google_alerts": "operator RSS alerts; quiet but live.",
    "iisd_itn": "only fetch-time full-text feed; intermittently empty.",
}


def _folders() -> list[str]:
    if not os.path.isdir(DIGESTS):
        return []
    return sorted(
        (n for n in os.listdir(DIGESTS)
         if n.endswith(SUFFIX) and os.path.isdir(os.path.join(DIGESTS, n))),
        reverse=True,
    )


def _load_meta(folder: str) -> dict:
    try:
        with open(os.path.join(DIGESTS, folder, "meta.json"), encoding="utf-8") as fh:
            return json.load(fh) or {}
    except (OSError, ValueError):
        return {}


_SRC_RE = re.compile(r"^-\s+\*\*Source:\*\*\s+(.*?)\s+—\s+\[Read", re.M)


def _surfaced_by_source(folder: str) -> dict[str, int]:
    """Count surfaced items per source from the article files (ground truth for
    every archived run, including those predating per-source recording)."""
    out: dict[str, int] = defaultdict(int)
    arts = os.path.join(DIGESTS, folder, "articles")
    if not os.path.isdir(arts):
        return out
    for fn in os.listdir(arts):
        if not fn.endswith(".md"):
            continue
        try:
            with open(os.path.join(arts, fn), encoding="utf-8") as fh:
                m = _SRC_RE.search(fh.read())
        except OSError:
            continue
        if m:
            raw = m.group(1).split(" → ")[0].strip().lower().replace(" ", "_")
            out[raw] += 1
    return out


def main() -> None:
    fetched = defaultdict(int)        # per-source fresh candidates (where recorded)
    surfaced = defaultdict(int)       # per-source surfaced items (where recorded)
    have_fetched = defaultdict(int)   # runs with per_source data, per source
    runs = 0
    runs_with_persource = 0

    for folder in _folders():
        meta = _load_meta(folder)
        if not meta:
            continue
        runs += 1
        ps = meta.get("per_source") or {}
        if ps:
            runs_with_persource += 1
        for src, n in ps.items():
            fetched[src] += int(n or 0)
            have_fetched[src] += 1
        # Surfaced-per-source from the article files (works for every run); fall
        # back to the recorded accepted_by_source only if no articles are present.
        sbs = _surfaced_by_source(folder)
        if not sbs:
            sbs = {s: int(n or 0) for s, n in (meta.get("accepted_by_source") or {}).items()}
        for src, n in sbs.items():
            surfaced[src] += int(n or 0)

    all_sources = sorted(set(fetched) | set(surfaced))

    lines = [
        "# Source receptivity — analytics",
        "",
        f"Across **{runs}** archived run(s); per-source candidate counts available for "
        f"**{runs_with_persource}** of them (older runs predate per-source recording).",
        "",
        "_Receptivity = surfaced ÷ fresh candidates, where per-source fresh counts exist._",
        "",
        "| Source | Fresh candidates | Surfaced | Receptivity | Note |",
        "|--------|------------------|----------|-------------|------|",
    ]
    for src in all_sources:
        f = fetched.get(src, 0)
        s = surfaced.get(src, 0)
        ratio = f"{(s / f * 100):.0f}%" if f else "n/a"
        note = _NOTES.get(src, "")
        lines.append(f"| {src} | {f if have_fetched.get(src) else '—'} | {s} | {ratio} | {note} |")
    if not all_sources:
        lines.append("| — | — | — | — | _No per-source data yet._ |")

    lines += [
        "",
        "## Reading this",
        "- **Surfaced** counts items that reached the digest — the clearest signal of a "
        "source's on-theme yield to date.",
        "- **Receptivity** needs per-source fresh counts; it populates as runs accrue "
        "under the per-source-recording build.",
        "- Sources flagged capped (`iareporter_headlines`) "
        "are structural limits, not tuning targets — prioritise full-text feeds that "
        "reach the IP-as-investment / judicial-measure / jurisdictional intersection.",
        "",
        "_Generated by the analytics member (scripts/source_analytics.py); deterministic, "
        "no model calls._",
    ]

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {OUT} ({len(all_sources)} sources, {runs} runs)")


if __name__ == "__main__":
    main()
