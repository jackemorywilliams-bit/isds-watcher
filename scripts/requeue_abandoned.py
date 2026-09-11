#!/usr/bin/env python3
"""Return abandoned candidates to the retry queue when the abandonment was OURS.

WHY THIS EXISTS. ``state/seen.json`` marks an item "abandoned" after
``MAX_CLASSIFY_ATTEMPTS`` failed classifications, and ``analytics/
abandoned_candidates.jsonl`` ledgers the decision. That is right when the item
is the problem. On 2026-09-07 it was not: the Anthropic classifier had been
unable to make a single call since 08-24 (SDK contract regression), and eight
candidates were abandoned after three attempts that were all the instrument's
own failure. Editing the state by hand would be invisible; this script makes
the reversal a counted decision with its own record.

WHAT IT DOES, for every ledger line whose ``run`` and ``last_outcome`` match:
  1. removes the seen entry — only if it still says "abandoned";
  2. queues the item in ``state/deferred.json`` at attempts=0, carrying the
     ledger's identity and URL (title/summary were not kept by the ledger, so the
     next run rebuilds the item from the URL — the honest position to retry from);
  3. appends one line to ``analytics/requeued_candidates.jsonl`` saying why.
The abandoned ledger is append-only and is NOT edited: it still records that the
abandonment happened; the requeued ledger records that it was reversed.
Idempotent: a second run finds no "abandoned" seen entries and changes nothing.
``scripts/check_seen_integrity.py`` passes on the result (it checks that every
"abandoned" seen entry is ledgered; a ledgered line without a seen entry is a
reversed decision, and the requeued ledger explains it).

CLI:
    python scripts/requeue_abandoned.py --run 2026-09-07 --last-outcome provider_error \\
        --because "anthropic 1.x removed temperature; every call raised TypeError" \\
        --fix "<commit or PR>" [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from src import state  # noqa: E402

REQUEUED_PATH = "analytics/requeued_candidates.jsonl"


def _load_jsonl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def reopen_unread(args) -> int:
    """Reverse a requeue that the pipeline consumed without reading.

    2026-09-11: the eight items requeued on 2026-09-07 carried no title or
    summary (the abandoned ledger keeps only identity and URL), scored 0
    lexically, never reached enrichment, were classified on an empty haystack
    and marked seen "ok" — retired unread. src/main.py now reads textless
    rebuilt items unconditionally; this mode puts such items back in the queue
    so the next run reads them. Criterion, from telemetry, never from memory:
    the seen entry is "ok" AND the run's telemetry row for the item shows
    dedup.marked_seen true (the row that retired it) AND access.text_len_title == 0
    AND access.text_len_body == 0 (nothing to classify on). Reopening only helps items
    whose URL can yield a body: not sources in enrich.NO_BODY_FETCH, and not PDF
    endpoints with no extractable HTML — those need a terminal 'unreadable' outcome,
    which is a separate gap.
    """
    import hashlib
    rows = _load_jsonl(args.requeued)
    tel = _load_jsonl(args.telemetry)
    by_hash: dict[tuple[str, str], list[dict]] = {}
    for t in tel:
        by_hash.setdefault((t.get("source", ""), t.get("source_id_hash", "")), []).append(t)
    st = state.load_state(args.state)
    dq = state.load_deferred(args.deferred)
    now = datetime.now(timezone.utc).isoformat()
    done, skipped = [], []
    for r in rows:
        if r.get("reopened"):
            continue
        key = (r.get("source", ""), r.get("source_id", ""))
        entry = (st.get("sources", {}).get(key[0]) or {}).get(key[1])
        if not (isinstance(entry, dict) and entry.get("outcome") == "ok"):
            skipped.append((key, "seen entry is not 'ok' (not consumed, or already reopened)"))
            continue
        h = hashlib.sha256((key[1] or "").encode("utf-8")).hexdigest()
        # A date is not a run: 2026-09-07 carries three run_ids in telemetry.
        # The row that retired the item is the one whose dedup.marked_seen is
        # true on the seen entry's run date; a same-date row that only deferred
        # the item says nothing about what it was retired on.
        # The abandonment row of the same date also carries marked_seen (an
        # abandoned item is marked seen as "abandoned") and still has the
        # title from before — it is not the row that retired the item as "ok".
        # The retiring row: marked seen, not abandoned, and its classification
        # outcome equals the seen entry's outcome.
        trows = [t for t in by_hash.get((key[0], h), [])
                 if t.get("run_date") == entry.get("run")
                 and (t.get("dedup") or {}).get("marked_seen")
                 and not (t.get("dedup") or {}).get("abandoned")
                 and (t.get("classification") or {}).get("outcome") == entry.get("outcome")]
        # "Unread" is a fact about the text the classifier saw, not about the
        # enrichment cut: on the 2026-09-07 23:25 run all eight entered
        # enrichment, but for five of them no body could be fetched, so they
        # were classified on an empty haystack and marked ok. Criterion: no
        # title and no body on the retiring row (every one, if several).
        unread = bool(trows) and all(
            int((t.get("access") or {}).get("text_len_title", 1) or 0) == 0
            and int((t.get("access") or {}).get("text_len_body", 1) or 0) == 0
            for t in trows)
        if not unread:
            skipped.append((key, "telemetry does not show it retired unread"))
            continue
        del st["sources"][key[0]][key[1]]
        dq.setdefault(key[0], {})[key[1]] = {
            "first_deferred": now, "attempts": 0, "last_outcome": "reopened_unread",
            "url": r.get("url", ""), "title": "", "published": "", "summary": "",
            "reopened_unread": {"at": now, "consumed_run": entry.get("run"),
                                "because": args.because, "fix": args.fix},
        }
        done.append((key, entry.get("run")))
    for key, why in skipped:
        print(f"  skip  {key[0]} / {key[1][:70]} — {why}")
    for key, run in done:
        print(f"  reopen  {key[0]} / {key[1][:70]}  (consumed unread on {run})")
    print(f"{len(done)} reopened, {len(skipped)} skipped"
          + (" — DRY RUN, nothing written" if args.dry_run else ""))
    if args.dry_run or not done:
        return 0
    state.save_state(st, args.state)
    state.save_deferred(dq, args.deferred)
    with open(args.requeued, "a", encoding="utf-8") as fh:
        for key, run in done:
            fh.write(json.dumps({
                "schema": 1, "at": now, "source": key[0], "source_id": key[1],
                "reopened": True, "consumed_run": run, "because": args.because, "fix": args.fix,
            }, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", required=False, help="abandonment run date to match, e.g. 2026-09-07")
    ap.add_argument("--last-outcome", required=False, help="e.g. provider_error")
    ap.add_argument("--because", required=True, help="why the abandonment was the instrument's fault")
    ap.add_argument("--fix", default="", help="commit / PR that fixed the cause")
    ap.add_argument("--state", default=state.STATE_PATH)
    ap.add_argument("--deferred", default=state.DEFERRED_PATH)
    ap.add_argument("--ledger", default=state.ABANDONED_PATH)
    ap.add_argument("--requeued", default=REQUEUED_PATH)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reopen-unread", action="store_true",
                    help="reverse a previous requeue that was consumed unread: for each "
                         "requeued-ledger row whose seen entry is 'ok' but whose telemetry "
                         "row shows it was never enriched and had no title, reopen it")
    ap.add_argument("--telemetry", default="analytics/candidate_telemetry.jsonl")
    args = ap.parse_args(argv)
    if args.reopen_unread:
        if not args.because:
            ap.error("--because is required")
        return reopen_unread(args)
    if not (args.run and args.last_outcome):
        ap.error("--run and --last-outcome are required unless --reopen-unread is given")

    rows = [r for r in _load_jsonl(args.ledger)
            if r.get("run") == args.run and r.get("last_outcome") == args.last_outcome]
    if not rows:
        print(f"nothing in {args.ledger} matches run={args.run} last_outcome={args.last_outcome}")
        return 0

    st = state.load_state(args.state)
    dq = state.load_deferred(args.deferred)
    now = datetime.now(timezone.utc).isoformat()
    done, skipped = [], []
    for r in rows:
        key = (r.get("source", ""), r.get("source_id", ""))
        entry = (st.get("sources", {}).get(key[0]) or {}).get(key[1])
        if not (isinstance(entry, dict) and entry.get("outcome") == "abandoned"):
            skipped.append((key, "seen entry is not 'abandoned' (already requeued or re-marked)"))
            continue
        del st["sources"][key[0]][key[1]]
        dq.setdefault(key[0], {})[key[1]] = {
            "first_deferred": r.get("first_deferred") or now,
            "attempts": 0,
            "last_outcome": r.get("last_outcome", ""),
            "url": r.get("url", ""),
            "title": "",
            "published": "",
            "summary": "",
            "requeued_from_abandoned": {
                "run": r.get("run"), "at": now, "because": args.because,
                "fix": args.fix, "attempts_before": int(r.get("attempts", 0) or 0),
            },
        }
        done.append((key, r))

    for key, why in skipped:
        print(f"  skip  {key[0]} / {key[1][:70]} — {why}")
    for key, r in done:
        print(f"  requeue  {key[0]} / {key[1][:70]}  (abandoned {r.get('run')} after "
              f"{r.get('attempts')} × {r.get('last_outcome')})")
    print(f"{len(done)} requeued, {len(skipped)} skipped"
          + (" — DRY RUN, nothing written" if args.dry_run else ""))
    if args.dry_run or not done:
        return 0

    state.save_state(st, args.state)
    state.save_deferred(dq, args.deferred)
    parent = os.path.dirname(args.requeued)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(args.requeued, "a", encoding="utf-8") as fh:
        for key, r in done:
            fh.write(json.dumps({
                "schema": 1, "at": now, "source": key[0], "source_id": key[1],
                "url": r.get("url", ""), "abandoned_run": r.get("run"),
                "abandoned_after_attempts": int(r.get("attempts", 0) or 0),
                "last_outcome": r.get("last_outcome", ""),
                "because": args.because, "fix": args.fix,
            }, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
