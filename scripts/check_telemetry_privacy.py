#!/usr/bin/env python3
"""Fail the build if the candidate telemetry ever contains candidate TEXT.

WHY THIS EXISTS. ``analytics/candidate_telemetry.jsonl`` is written every run and
grows without anyone reading it. That is precisely the shape of file that
acquires a field nobody intended: someone debugging a scoring question adds
``"title"`` "just to see which item this is", the run is green, the line is
committed, and the repo now holds a scraped corpus of other people's prose in an
analytics file — quietly outside the polite-crawler rules the fetchers follow.
The rule (no text, only lengths and hashes) is stated in ``src/telemetry.py``.
A stated rule is not a control. This is the control.

WHAT IT CHECKS, at any depth in any record:

  1. FORBIDDEN FIELD NAMES — ``raw_text``, ``summary``, ``body``, ``title``.
     Matched exactly, never as a substring: ``text_len_title`` and
     ``title_sha256`` are the intended way to describe a title and must pass,
     while ``title`` itself must not.
  2. OVER-LONG STRINGS — any string over 200 characters in a field outside the
     hash/id allowlist. This is the backstop for text smuggled under a name the
     first check does not know: an excerpt called ``context`` is still an
     excerpt. Short strings are left alone because outcomes, hosts, and reasons
     are legitimately short strings.
  3. EXCERPTS FROM HEADLINE-ONLY SOURCES — any ``evidence_excerpt`` field on a
     record whose ``access.headline_only`` is true. A headline-only source is one
     whose body we deliberately never fetch; an excerpt on such a record could
     only have come from the headline, and passing a headline off as an excerpt
     from the source is the same misrepresentation the digest's notable-line rule
     already forbids.

WHAT IT CANNOT DO. It cannot tell you that a hash was computed over the right
string, and it cannot recognise text under 200 characters in a field it does not
know about. Check 1 is the specific rule; check 2 is the general net; neither
replaces reading a new field's name before adding it.

THE SECOND STREAM — ``analytics/tail_audit.jsonl`` (added 2026-09-13, council
Ruling 4(c), in the same change that created the file). The tail audit appends
one row per audited item, for ever, and that is the same shape of file as the
telemetry: append-only, rarely read, and one debugging session away from
carrying a title "just to see which item this is". A new stream outside this
guard is a hole, so it is inside it from its first line.

The tail-audit ledger gets a STRICTER check than the telemetry, because it can:
its schema is nine fields fixed by the ruling, so this asserts the key set
EXACTLY against ``src.tail_audit.LEDGER_FIELDS``. A tenth field fails the build
whatever it is called. That is the difference between a guard that catches the
fields it was told about and one that catches the field nobody declared — and
the tail audit is small enough to afford the strict version.

CLI:
    python scripts/check_telemetry_privacy.py [--path FILE]
                                              [--tail-audit-path FILE]

Both streams are checked by default; a missing file is not a violation. Exit 0
clean, 1 on any violation, 2 if a file exists but cannot be read.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO))

from src.tail_audit import LEDGER_FIELDS, LEDGER_PATH  # noqa: E402
from src.telemetry import (  # noqa: E402
    FORBIDDEN_FIELDS,
    LONG_STRING_ALLOWLIST,
    MAX_STRING_LEN,
    TELEMETRY_PATH,
)

EXCERPT_FIELD = "evidence_excerpt"


def _walk(node, path: str, problems: list[str], lineno: int) -> None:
    """Depth-first over one record, recording every violation it finds.

    Reports every problem rather than stopping at the first: a run that
    introduced one leaking field has usually introduced it on every record, and
    the operator should see the shape of the leak, not one instance of it.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key in FORBIDDEN_FIELDS:
                problems.append(
                    f"line {lineno}: field `{here}` — `{key}` is candidate text; "
                    f"record its length and sha256 instead")
            if isinstance(value, str) and len(value) > MAX_STRING_LEN \
                    and key not in LONG_STRING_ALLOWLIST:
                problems.append(
                    f"line {lineno}: field `{here}` holds a {len(value)}-character "
                    f"string (limit {MAX_STRING_LEN}) and is not a hash/id field — "
                    "this is prose, not telemetry")
            _walk(value, here, problems, lineno)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            _walk(value, f"{path}[{i}]", problems, lineno)


def _has_field(node, name: str) -> bool:
    """Whether ``name`` appears as a key anywhere in the record."""
    if isinstance(node, dict):
        return any(k == name or _has_field(v, name) for k, v in node.items())
    if isinstance(node, list):
        return any(_has_field(v, name) for v in node)
    return False


def check_record(rec: dict, lineno: int) -> list[str]:
    problems: list[str] = []
    _walk(rec, "", problems, lineno)
    headline_only = bool((rec.get("access") or {}).get("headline_only"))
    if headline_only and _has_field(rec, EXCERPT_FIELD):
        problems.append(
            f"line {lineno}: record carries `{EXCERPT_FIELD}` while "
            "`access.headline_only` is true — we never read that source's body, "
            "so the excerpt can only be its headline")
    return problems


def check_tail_audit_record(rec: dict, lineno: int) -> list[str]:
    """The ledger row checks: the general ones, plus an EXACT schema match."""
    problems = _walk_record(rec, lineno)
    keys = set(rec)
    expected = set(LEDGER_FIELDS)
    for extra in sorted(keys - expected):
        problems.append(
            f"line {lineno}: field `{extra}` is not one of the tail audit's "
            f"nine declared fields {LEDGER_FIELDS}. The ledger's schema was "
            "fixed by the ruling that created it; a new field must be added to "
            "src.tail_audit.LEDGER_FIELDS deliberately, which is what makes "
            "adding candidate text to this stream a decision rather than a slip")
    for missing in sorted(expected - keys):
        problems.append(
            f"line {lineno}: field `{missing}` is missing — a partial row "
            "cannot be read back as a pair")
    return problems


def _walk_record(rec: dict, lineno: int) -> list[str]:
    problems: list[str] = []
    _walk(rec, "", problems, lineno)
    return problems


def check(path: Path, *, record_check=check_record) -> tuple[int, list[str]]:
    """Returns (records checked, problems)."""
    problems: list[str] = []
    checked = 0
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except ValueError as exc:
                problems.append(f"line {lineno}: not valid JSON ({exc})")
                continue
            if not isinstance(rec, dict):
                problems.append(f"line {lineno}: record is not a JSON object")
                continue
            checked += 1
            problems.extend(record_check(rec, lineno))
    return checked, problems


def _check_stream(path: Path, label: str, record_check) -> tuple[int, int]:
    """Check one stream. Returns (exit code, problems found)."""
    if not path.exists():
        print(f"No {label} at {path} — nothing to check.")
        return 0, 0

    try:
        checked, problems = check(path, record_check=record_check)
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr)
        return 2, 0

    print(f"Checked {checked} {label} records in {path}.")
    for p in problems:
        print(f"  FAIL {p}")
    return (1 if problems else 0), len(problems)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="check_telemetry_privacy")
    ap.add_argument("--path", default=str(REPO / TELEMETRY_PATH),
                    help="telemetry jsonl to check")
    ap.add_argument("--tail-audit-path", default=str(REPO / LEDGER_PATH),
                    help="tail-audit ledger jsonl to check")
    args = ap.parse_args(argv[1:])

    codes = []
    problems = 0
    for path, label, record_check in (
            (Path(args.path), "telemetry", check_record),
            (Path(args.tail_audit_path), "tail-audit", check_tail_audit_record)):
        code, found = _check_stream(path, label, record_check)
        codes.append(code)
        problems += found

    if 2 in codes:
        return 2
    if problems:
        print("\nCandidate telemetry records our own processing — lengths, hashes, "
              "rings, outcomes.\nIt must never accumulate the sources' text.",
              file=sys.stderr)
        return 1
    print("  ok — no candidate text, no over-long strings, no excerpts from "
          "headline-only sources, and the tail-audit ledger carries exactly its "
          "nine declared fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
