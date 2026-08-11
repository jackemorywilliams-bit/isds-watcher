#!/usr/bin/env python3
"""Fixed queries over the candidate telemetry.

WHY FIXED QUERIES. The telemetry exists to answer a few recurring questions, and
a general query language would mean each answer is phrased slightly differently
each time it is asked — which is how "italaw yields nothing" became a thing the
council believed for four weeks without a number behind it. These are the
questions, each with one definition, printed the same way every time.

    --source-yield   per source: candidates, how many reached enrichment, how
                     many classified cleanly, how many surfaced. The funnel.
    --deferred       candidates this file says were deferred rather than marked
                     seen — the items a failed classification is holding.
    --abandoned      candidates that exhausted their attempts. Each one is a
                     thing we gave up on, and giving up should be countable.

CLI:
    python scripts/telemetry_query.py --source-yield [--run RUN_ID] [--path FILE]

Exit 0 always when the file is readable (a query is a report, not a gate); 2 if
the file cannot be read.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO))

from src.telemetry import TELEMETRY_PATH, load_records  # noqa: E402


def _filtered(records: list[dict], run: str | None) -> list[dict]:
    if not run:
        return records
    return [r for r in records if r.get("run_id") == run or r.get("run_date") == run]


def source_yield(records: list[dict]) -> None:
    rows: dict[str, dict] = {}
    for r in records:
        row = rows.setdefault(r.get("source", "?"), {
            "candidates": 0, "enriched": 0, "classified_ok": 0, "surfaced": 0})
        row["candidates"] += 1
        if r.get("entered_enrichment"):
            row["enriched"] += 1
        if (r.get("classification") or {}).get("outcome") in ("ok", "keyword_only_by_design"):
            row["classified_ok"] += 1
        if (r.get("surfacing") or {}).get("surfaced"):
            row["surfaced"] += 1
    print(f"{'source':<24} {'cands':>6} {'enriched':>9} {'classified':>11} {'surfaced':>9}")
    for name in sorted(rows):
        r = rows[name]
        print(f"{name:<24} {r['candidates']:>6} {r['enriched']:>9} "
              f"{r['classified_ok']:>11} {r['surfaced']:>9}")
    total = len(records)
    print(f"{'TOTAL':<24} {total:>6}")


def _outcome_rows(records: list[dict], key: str, label: str) -> None:
    hits = [r for r in records if (r.get("dedup") or {}).get(key)]
    print(f"{label}: {len(hits)}")
    print(f"  {'run_date':<12} {'candidate_id':<40} {'outcome':<22} attempts")
    for r in sorted(hits, key=lambda r: (r.get("run_date", ""), r.get("candidate_id", ""))):
        cls = r.get("classification") or {}
        print(f"  {r.get('run_date', ''):<12} {r.get('candidate_id', ''):<40} "
              f"{cls.get('outcome', ''):<22} {cls.get('attempts', 0)}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="telemetry_query")
    p.add_argument("--path", default=str(REPO / TELEMETRY_PATH))
    p.add_argument("--run", default=None, help="limit to one run_id or run_date")
    p.add_argument("--source-yield", action="store_true", help="the per-source funnel")
    p.add_argument("--deferred", action="store_true", help="candidates held for retry")
    p.add_argument("--abandoned", action="store_true", help="candidates given up on")
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])
    try:
        records = _filtered(load_records(args.path), args.run)
    except OSError as exc:
        print(f"cannot read {args.path}: {exc}", file=sys.stderr)
        return 2

    if not (args.source_yield or args.deferred or args.abandoned):
        build_parser().print_help()
        return 0

    print(f"{len(records)} records from {args.path}"
          + (f" (run {args.run})" if args.run else ""))
    if args.source_yield:
        print()
        source_yield(records)
    if args.deferred:
        print()
        _outcome_rows(records, "deferred", "deferred")
    if args.abandoned:
        print()
        _outcome_rows(records, "abandoned", "abandoned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
