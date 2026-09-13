#!/usr/bin/env python3
"""Fixed queries over the candidate telemetry.

WHY FIXED QUERIES. The telemetry exists to answer a few recurring questions, and
a general query language would mean each answer is phrased slightly differently
each time it is asked — which is how "italaw yields nothing" became a thing the
council believed for four weeks without a number behind it. These are the
questions, each with one definition, printed the same way every time.

    --source-yield   per source: candidates, how many reached enrichment, how
                     many the run finished with, how many surfaced. The funnel.
                     "classified" counts every TERMINAL outcome, which includes a
                     keyword score the run fell back to when a call failed — it
                     is "the run is done with this item", not "a model read it".
    --deferred       candidates this file says were deferred rather than marked
                     seen — the items a failed classification is holding.
    --abandoned      candidates that exhausted their attempts. Each one is a
                     thing we gave up on, and giving up should be countable.
    --tail-audit     the stratified tail audit's paired re-classifications, by
                     stratum: how many pairs, how many flipped band, which way,
                     and the mean score delta. Reads
                     `analytics/tail_audit.jsonl`, not the candidate telemetry.

THE TAIL AUDIT IS REPORTED HERE AND NOWHERE ELSE (council ruling of 2026-09-13,
Ruling 4(c)). A flip rate is an internal measurement of the INSTRUMENT, not a
finding about ISDS; putting one in the digest or on the professor-facing site
would be the instrument grading itself in her inbox.
`tests/test_publication_quarantine.py` fails the build if any other surface
starts reading the ledger. It is also not a validation result: a flip says the
enrichment cut changed what the instrument said about an item, and says nothing
about which of the two readings was right. Nothing here is evidence of accuracy.

CLI:
    python scripts/telemetry_query.py --source-yield [--run RUN_ID] [--path FILE]
    python scripts/telemetry_query.py --tail-audit [--run RUN_ID]
                                      [--tail-audit-path FILE]

Exit 0 always when the file is readable (a query is a report, not a gate); 2 if
the file cannot be read.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO))

from src.classify import READ_TERMINAL_OUTCOMES  # noqa: E402
from src.telemetry import TELEMETRY_PATH, load_records  # noqa: E402

# What `--source-yield`'s "classified" column counts: the outcomes after which
# the run was genuinely finished with the item. DERIVED from the classifier's own
# terminal set rather than listed here, because this column was a hand-written
# pair ("ok", "keyword_only_by_design") that would have silently stopped counting
# the tail the moment `keyword_after_provider_error` was added on 2026-09-10 — an
# outage would have read as a drop in yield instead of as an outage.
# 2026-09-13: derived from READ_TERMINAL_OUTCOMES, not TERMINAL_OUTCOMES. The
# two differ by `unreadable`, the terminal outcome in which NOTHING WAS READ.
# Counting it here would put an item that was never looked at into the column
# headed "classified" — the same conflation the outcome was added to end, one
# surface further out.
CLASSIFIED_OUTCOMES = frozenset(o.value for o in READ_TERMINAL_OUTCOMES)


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
        if (r.get("classification") or {}).get("outcome") in CLASSIFIED_OUTCOMES:
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


def tail_audit_report(rows: list[dict]) -> None:
    """Per stratum: pairs, flips, direction, mean delta.

    A "flip" is `band_unenriched != band_enriched` — the enrichment cut changed
    what the instrument said about this exact item. UP and DOWN are counted
    separately because they mean opposite things about the gate: UP is an item
    the cut was hiding, DOWN is an item the headline flattered.
    """
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    buckets: dict[str, dict] = {
        s: {"pairs": 0, "flips": 0, "up": 0, "down": 0, "delta": 0}
        for s in STRATA}
    for r in rows:
        b = buckets.get(str(r.get("stratum", "")))
        if b is None:
            continue
        before = str(r.get("band_unenriched", ""))
        after = str(r.get("band_enriched", ""))
        b["pairs"] += 1
        b["delta"] += int(r.get("score_delta", 0) or 0)
        if before != after:
            b["flips"] += 1
            if order.get(after, -1) > order.get(before, -1):
                b["up"] += 1
            else:
                b["down"] += 1

    print(f"{'stratum':<32} {'pairs':>6} {'flips':>6} {'up':>4} {'down':>5} "
          f"{'mean delta':>11}")
    total = {"pairs": 0, "flips": 0, "up": 0, "down": 0, "delta": 0}
    for name in STRATA:
        b = buckets[name]
        mean = (b["delta"] / b["pairs"]) if b["pairs"] else 0.0
        print(f"{name:<32} {b['pairs']:>6} {b['flips']:>6} {b['up']:>4} "
              f"{b['down']:>5} {mean:>11.1f}")
        for key in total:
            total[key] += b[key]
    mean = (total["delta"] / total["pairs"]) if total["pairs"] else 0.0
    print(f"{'TOTAL':<32} {total['pairs']:>6} {total['flips']:>6} "
          f"{total['up']:>4} {total['down']:>5} {mean:>11.1f}")
    print("\nA flip is a change in what the instrument said about one item when "
          "it was\ngiven a body. It is NOT evidence that either reading was "
          "correct, and it is\nnot a validation result. Internal only — never "
          "the digest, the site or the README.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="telemetry_query")
    p.add_argument("--path", default=str(REPO / TELEMETRY_PATH))
    p.add_argument("--run", default=None, help="limit to one run_id or run_date")
    p.add_argument("--source-yield", action="store_true", help="the per-source funnel")
    p.add_argument("--deferred", action="store_true", help="candidates held for retry")
    p.add_argument("--abandoned", action="store_true", help="candidates given up on")
    p.add_argument("--tail-audit-path", default=str(REPO / LEDGER_PATH))
    p.add_argument("--tail-audit", action="store_true",
                   help="the tail audit's paired re-classifications, by stratum")
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv[1:])

    if args.tail_audit:
        try:
            rows = read_ledger(args.tail_audit_path)
        except OSError as exc:
            print(f"cannot read {args.tail_audit_path}: {exc}", file=sys.stderr)
            return 2
        if args.run:
            rows = [r for r in rows
                    if str(r.get("run_id", "")).startswith(args.run)]
        print(f"{len(rows)} tail-audit pairs from {args.tail_audit_path}"
              + (f" (run {args.run})" if args.run else ""))
        print()
        tail_audit_report(rows)
        if not (args.source_yield or args.deferred or args.abandoned):
            return 0
        print()

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
