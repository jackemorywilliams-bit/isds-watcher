#!/usr/bin/env python3
"""Fail the build if the seen-state records an ending it cannot account for.

WHY THIS EXISTS. ``state/seen.json`` is the file that decides an item will never
be looked at again, and until now it recorded that decision as a bare timestamp.
Every ending looked identical: classified cleanly, classification failed and a
keyword score went out under the model's name, or indexed by the bootstrap and
never read at all. The pipeline now writes an outcome with each entry. An
outcome nothing checks is a comment, so this checks it.

WHAT IT CHECKS.

  1. TERMINAL OUTCOME. Every non-legacy entry must carry an outcome from
     ``state.TERMINAL_SEEN_OUTCOMES``. An entry with no outcome, or with a
     non-terminal one like `parse_failed`, means something marked an item seen
     that had not finished — which is the exact defect the deferred queue exists
     to prevent, so it must fail rather than sit there.
  2. ABANDONMENTS ARE LEDGERED. Every entry with outcome "abandoned" must have a
     matching line in ``analytics/abandoned_candidates.jsonl``. Abandoning an
     item is a real editorial loss — a candidate we could not read and stopped
     trying to read — and it is only ever visible if the two records agree. One
     without the other means either a silent abandonment or a ledger claiming
     something the state does not.

LEGACY ENTRIES ARE EXEMPT. The live file holds hundreds of pre-2026-08 bare
strings whose endings genuinely are unknown; ``src/state.py`` migrates them at
read time to outcome "legacy". Failing them would be demanding a fact that no
longer exists. They are counted and reported, never failed, and the count
shrinks on its own as items are re-marked.

CLI:
    python scripts/check_seen_integrity.py [--state FILE] [--ledger FILE]

Exit 0 clean, 1 on any disagreement, 2 if an input cannot be read.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO))

from src.state import (  # noqa: E402
    ABANDONED_PATH,
    LEGACY_OUTCOME,
    STATE_PATH,
    TERMINAL_SEEN_OUTCOMES,
)


def load_ledger(path: Path) -> set[tuple[str, str]]:
    """``{(source, source_id)}`` for every abandonment recorded in the ledger."""
    if not path.exists():
        return set()
    out: set[tuple[str, str]] = set()
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if isinstance(rec, dict):
                out.add((str(rec.get("source", "")), str(rec.get("source_id", ""))))
    return out


def check(state_path: Path, ledger_path: Path) -> tuple[int, int, list[str]]:
    """Returns (entries checked, legacy entries, problems)."""
    with open(state_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    sources = (data or {}).get("sources") or {}
    ledger = load_ledger(ledger_path)

    problems: list[str] = []
    checked = 0
    legacy = 0
    for source in sorted(sources):
        entries = sources[source]
        if not isinstance(entries, dict):
            problems.append(f"{source}: entries are not an object")
            continue
        for source_id in sorted(entries):
            value = entries[source_id]
            checked += 1
            if isinstance(value, str):
                legacy += 1     # pre-migration bare timestamp; exempt by design
                continue
            if not isinstance(value, dict):
                problems.append(
                    f"{source} / {source_id}: entry is neither a legacy timestamp "
                    f"nor an object ({type(value).__name__})")
                continue
            outcome = str(value.get("outcome", ""))
            if outcome == LEGACY_OUTCOME:
                legacy += 1
                continue
            if outcome not in TERMINAL_SEEN_OUTCOMES:
                problems.append(
                    f"{source} / {source_id}: marked seen with outcome "
                    f"{outcome or '(none)'!r}, which is not terminal — an item we "
                    "did not finish must be deferred, not retired")
                continue
            if outcome == "abandoned" and (source, source_id) not in ledger:
                problems.append(
                    f"{source} / {source_id}: seen as \"abandoned\" but no matching "
                    f"line in {ledger_path.name} — an abandonment nobody can count")
    return checked, legacy, problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="check_seen_integrity")
    ap.add_argument("--state", default=str(REPO / STATE_PATH))
    ap.add_argument("--ledger", default=str(REPO / ABANDONED_PATH))
    args = ap.parse_args(argv[1:])
    state_path, ledger_path = Path(args.state), Path(args.ledger)

    if not state_path.exists():
        print(f"No seen-state at {state_path} — nothing to check.")
        return 0

    try:
        checked, legacy, problems = check(state_path, ledger_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot run the seen-state check: {exc}", file=sys.stderr)
        return 2

    print(f"Checked {checked} seen entries in {state_path} "
          f"({legacy} legacy, exempt) against {ledger_path.name}.")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print("\nA seen entry is the decision never to look at an item again. It has "
              "to say how\nthe item ended, and an abandonment has to be ledgered "
              "where it can be counted.", file=sys.stderr)
        return 1
    print("  ok — every non-legacy entry carries a terminal outcome, and every "
          "abandonment is\n       ledgered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
