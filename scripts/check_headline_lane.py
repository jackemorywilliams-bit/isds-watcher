#!/usr/bin/env python3
"""Fail the build if a constrained-lane entry says anything its slots do not.

WHY THIS EXISTS. `src/headline_lane.py` renders library-lane records from a
closed grammar with no free-text slot, so that a record about an item we did not
read cannot contain an assertion about it. A grammar enforced only at render
time protects nothing once the output is a file: the file gets hand-corrected,
or a later stage appends a sentence, or a model is asked to "polish" it, and the
constraint that made the record safe is gone with no trace. This re-derives
every entry FROM ITS OWN SLOTS and requires the bytes to match.

WHAT IT CHECKS, per entry:

  1. BYTE IDENTITY. Re-render from the recorded slots; the result must equal the
     recorded text byte for byte. This is the check that subsumes most others —
     any inserted word, any deleted clause, any reordering fails here.
  2. EVERY CHARACTER IS ACCOUNTED FOR. The rendering decomposes into segments
     that are either a slot value or a literal from `headline_lane.FIXED_LITERALS`.
     A fixed segment outside that set means the template itself was edited.
  3. THE SLOTS ARE LEGAL. Source is an identifier, date is YYYY-MM-DD, nexus is
     one of three enum words, and the limitation clause is one of the three
     fixed sentences. Enforced by reconstructing the entry, whose constructor
     holds these invariants — one definition, checked twice.
  4. THE POSTURE CLAUSE IS THE HEADLINE'S OWN WORDS, consecutively and in order.
     Also a constructor invariant; it fails here as a reportable problem rather
     than as a traceback.
  5. NO FORBIDDEN TOKENS outside the quoted title. `held`, `found that`,
     `concludes`, `reasoning`, `no ISDS`, `does not engage`, `straightforward`,
     `routine`, `intersection` — the vocabulary of a conclusion. The quoted
     title is exempt because it is the source's sentence in quotation marks;
     the posture clause is not exempt, because that one is ours.
  6. THE LABEL MATCHES THE ACCESS. An entry carrying the retrieved-body
     limitation may not be publicly labelled "Headline-only lead", and one
     carrying the paywalled limitation may not be labelled "Library comparator".
     This is the mismatch the fixture simulation actually produced — lane
     HEADLINE_ONLY_LIBRARY_LEAD at evidence location accessible_body — and it is
     the reason the public label is a mapping rather than the lane's own name.

WHAT IT DOES NOT DO. It does not touch the archive. Entries written before this
grammar existed are covered by their own dated corrections; re-deriving them
here would either fail loudly for a reason already recorded elsewhere or, worse,
invite someone to rewrite a corrected record to make a guard green.

CLI:
    python scripts/check_headline_lane.py [--path FILE ...]

Reads JSONL (one entry object per line) or a JSON list. Exit 0 clean — including
when no file exists yet, which is the current state and is not a violation — 1
on any violation, 2 if a named file exists but cannot be read.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO))

from src.headline_lane import (  # noqa: E402
    FIXED_LITERALS,
    LIMITATION_PAYWALLED,
    LIMITATION_RETRIEVED,
    LIMITATION_UNRETRIEVED,
    SLOT_NAMES,
    HeadlineLaneEntry,
    forbidden_tokens_in,
    from_record,
)
from src.rings import (  # noqa: E402
    PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
    PUBLIC_LABEL_LIBRARY_COMPARATOR,
    InvariantViolation,
)

# Where a constrained-lane file would live once anything writes one. Nothing
# does yet; the guard runs anyway so the day something does, it is already
# guarded rather than guarded later.
DEFAULT_PATHS = ("analytics/headline_lane.jsonl",)

# Which public label each fixed limitation sentence is compatible with.
_LABEL_FOR_LIMITATION = {
    LIMITATION_PAYWALLED: PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
    LIMITATION_UNRETRIEVED: PUBLIC_LABEL_HEADLINE_ONLY_LEAD,
    LIMITATION_RETRIEVED: PUBLIC_LABEL_LIBRARY_COMPARATOR,
}


def check_entry(rec: dict, where: str) -> list[str]:
    """Every problem with one entry. Returns [] when it is clean."""
    problems: list[str] = []

    if not isinstance(rec, dict):
        return [f"{where}: entry is not an object"]

    missing = [s for s in SLOT_NAMES if s not in rec]
    if missing:
        problems.append(
            f"{where}: entry is missing slot(s) {', '.join(missing)} — an entry "
            "that does not record its slots cannot be re-derived from them")
        return problems
    if "text" not in rec:
        problems.append(f"{where}: entry records no rendered text to check")
        return problems

    try:
        entry: HeadlineLaneEntry = from_record(rec)
    except InvariantViolation as exc:
        return [f"{where}: slots rejected by the grammar — {exc}"]

    # 1. Byte identity between the recorded text and a fresh render.
    recorded = rec.get("text")
    if not isinstance(recorded, str):
        problems.append(f"{where}: `text` is not a string")
    elif recorded != entry.text:
        problems.append(
            f"{where}: the recorded text is not what its own slots render.\n"
            f"        recorded: {recorded!r}\n"
            f"        re-derived: {entry.text!r}")

    # 2. Every character came from a slot or an allowed literal.
    for kind, value in entry.segments():
        if kind == "fixed" and value not in FIXED_LITERALS:
            problems.append(
                f"{where}: fixed segment {value!r} is not one of the grammar's "
                "literals — the template itself has been edited")

    # 5. Forbidden tokens outside the quoted title.
    found = forbidden_tokens_in(entry)
    if found:
        problems.append(
            f"{where}: forbidden token(s) {', '.join(repr(f) for f in found)} "
            "outside the quoted title — this lane records an item, it does not "
            "reach a conclusion about one")

    # 6. The public label must agree with the access the limitation states.
    expected = _LABEL_FOR_LIMITATION[entry.limitation]
    if entry.public_label != expected:
        problems.append(
            f"{where}: public_label {entry.public_label!r} contradicts the "
            f"limitation clause, which describes a body we "
            f"{'did' if expected == PUBLIC_LABEL_LIBRARY_COMPARATOR else 'did not'}"
            f" retrieve (expected {expected!r})")

    return problems


def load_entries(path: Path) -> list[tuple[dict, str]]:
    """``[(entry, where)]`` from a JSONL file or a JSON list."""
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if raw.lstrip().startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("top-level JSON is not a list of entries")
        return [(rec, f"{path.name}[{i}]") for i, rec in enumerate(data)]
    out: list[tuple[dict, str]] = []
    for lineno, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        out.append((json.loads(line), f"{path.name} line {lineno}"))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="check_headline_lane")
    ap.add_argument("--path", action="append", default=None,
                    help="constrained-lane file to check (repeatable)")
    args = ap.parse_args(argv[1:])
    paths = [Path(p) for p in (args.path or [str(REPO / p) for p in DEFAULT_PATHS])]

    problems: list[str] = []
    checked = 0
    present = 0
    for path in paths:
        if not path.exists():
            continue
        present += 1
        try:
            entries = load_entries(path)
        except (OSError, ValueError) as exc:
            print(f"cannot read {path}: {exc}", file=sys.stderr)
            return 2
        for rec, where in entries:
            checked += 1
            problems.extend(check_entry(rec, where))

    if not present:
        print("check_headline_lane: no constrained-lane output on disk — "
              "nothing to check.")
        return 0

    print(f"check_headline_lane: re-derived {checked} entries from their slots.")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print("\nA constrained-lane entry is a record of an item, not a statement "
              "about it.\nIts text must be exactly what its slots render and "
              "nothing else.", file=sys.stderr)
        return 1
    print("  ok — every entry is byte-identical to its own slots, every "
          "character\n       is accounted for, and no entry reaches a conclusion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
