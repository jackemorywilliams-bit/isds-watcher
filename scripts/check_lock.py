#!/usr/bin/env python3
"""Fail the build if the locked validation set changed after it was locked.

WHY THIS EXISTS. `analytics/locked_set/SCHEMA.md` specifies a commit order whose
whole purpose is to make blindness PROVABLE rather than promised:

    1. items.json   — item content only; the schema has no label fields.
    2. LOCK.md      — sha256 of items.json, plus the commit that recorded it.
    3. labels.json  — labels, in a separate file, committed second.
    4. LOCK.md      — sha256 of labels.json, plus its commit.
    5. only now may any scorer touch the set.

Git history is the evidence that labels preceded scores. That evidence is worth
exactly as much as the guarantee that neither file was edited after its hash was
written down — and nothing was checking. A validation set that can be quietly
adjusted after the fact is not a validation set; it is a record of what we
wanted the answer to be. This recomputes both hashes and fails closed.

THE EMPTY STATE IS THE DESIGNED STATE. There are no items yet, deliberately:
the candidate matters named in the R2.1 record are leads whose primary documents
have not been retrieved, and per the carrying-span rule no item enters this set
on a memo's authority. So an absent LOCK.md, or an absent items.json, is not a
failure and this exits 0 with a note saying which files are missing. It becomes
a real check the moment the first hash is written, with no further wiring.

WHAT IT CANNOT DO. It cannot tell you the labels are right, and it cannot tell
you the lock entry was written before the labels rather than after. The first is
a human question. The second is answered by `git log`, which is why the schema
requires the commit SHA in the lock entry and why this prints it.

CLI:
    python scripts/check_lock.py [--dir analytics/locked_set]

Exit 0 clean (including the empty state), 1 if a hash disagrees or a lock entry
is malformed, 2 if a file exists but cannot be read.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

LOCKED_SET_DIR = "analytics/locked_set"
LOCK_FILE = "LOCK.md"
LOCKED_FILES = ("items.json", "labels.json")

# A lock entry names a file, gives its sha256, and gives the commit that
# recorded it. Deliberately narrow: a 64-hex digest and a 7-40 hex commit, in a
# markdown table row or a `key: value` line. Anything else is malformed rather
# than interpreted, because a lock entry this guard has to guess at is a lock
# entry that can be written ambiguously on purpose.
_HEX64 = r"[0-9a-f]{64}"
_COMMIT = r"[0-9a-f]{7,40}"
_ENTRY_PATTERNS = (
    # | items.json | <sha256> | <commit> |
    re.compile(r"^\|\s*`?(?P<file>[\w.\-]+)`?\s*\|\s*`?(?P<sha>" + _HEX64 +
               r")`?\s*\|\s*`?(?P<commit>" + _COMMIT + r")`?\s*\|", re.MULTILINE),
    # items.json: <sha256> (commit <commit>)
    re.compile(r"^\s*-?\s*`?(?P<file>[\w.\-]+)`?\s*:\s*`?(?P<sha>" + _HEX64 +
               r")`?\s*\(commit\s+`?(?P<commit>" + _COMMIT + r")`?\)",
               re.MULTILINE),
)


def sha256_file(path: Path) -> str:
    """Hex sha256 of a file's BYTES.

    Bytes, not parsed JSON: the lock is over the artefact that was committed,
    and two byte sequences that parse to the same object are still two different
    commits. Re-serialising before hashing would let a reformat pass unnoticed.
    """
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_lock(text: str) -> dict[str, dict[str, str]]:
    """``{filename: {"sha": ..., "commit": ...}}`` for every entry recognised.

    A file locked twice is an error the caller reports: the schema's step 4
    APPENDS labels.json's entry, it does not rewrite items.json's, so a second
    entry for the same file means the record was edited rather than extended.
    """
    found: dict[str, dict[str, str]] = {}
    duplicates: set[str] = set()
    for pattern in _ENTRY_PATTERNS:
        for m in pattern.finditer(text):
            name = m.group("file")
            if name not in LOCKED_FILES:
                continue
            if name in found and found[name]["sha"] != m.group("sha"):
                duplicates.add(name)
            found[name] = {"sha": m.group("sha"), "commit": m.group("commit")}
    for name in duplicates:
        found[name]["duplicate"] = "1"
    return found


def check(directory: Path) -> tuple[list[str], list[str]]:
    """Returns ``(notes, problems)``."""
    notes: list[str] = []
    problems: list[str] = []

    lock_path = directory / LOCK_FILE
    present = [n for n in LOCKED_FILES if (directory / n).exists()]

    if not lock_path.exists():
        if present:
            problems.append(
                f"{', '.join(present)} exists but {LOCK_FILE} does not — an "
                "unlocked validation set is a set whose contents at labelling "
                "time nobody can demonstrate")
        else:
            notes.append(
                f"no {LOCK_FILE} and no locked files: the set is deliberately "
                "empty (analytics/locked_set/SCHEMA.md), which is the designed "
                "current state and not an error")
        return notes, problems

    entries = parse_lock(lock_path.read_text(encoding="utf-8"))
    if not entries:
        problems.append(
            f"{LOCK_FILE} exists but records no recognisable lock entry — a lock "
            "file that locks nothing reads as protection and provides none")
        return notes, problems

    for name in LOCKED_FILES:
        path = directory / name
        entry = entries.get(name)
        if entry is None:
            if path.exists():
                problems.append(
                    f"{name} exists and has no entry in {LOCK_FILE} — it was "
                    "added to the set without being locked")
            else:
                notes.append(f"{name}: not present and not locked (expected while "
                             "the set is being built in order)")
            continue
        if entry.get("duplicate"):
            problems.append(
                f"{name} has two different hashes in {LOCK_FILE} — step 4 appends "
                "labels.json's entry, it never rewrites an earlier one")
            continue
        if not path.exists():
            problems.append(
                f"{name} is locked in {LOCK_FILE} at {entry['sha'][:12]}… but the "
                "file is gone — the set no longer contains what was labelled")
            continue
        actual = sha256_file(path)
        if actual != entry["sha"]:
            problems.append(
                f"{name} CHANGED after it was locked.\n"
                f"        locked:  {entry['sha']}  (commit {entry['commit']})\n"
                f"        on disk: {actual}\n"
                "        The lock is the evidence that labels preceded scores. "
                "An edit after the lock destroys it.")
        else:
            notes.append(f"{name}: matches its lock entry "
                         f"({actual[:12]}…, commit {entry['commit']})")
    return notes, problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="check_lock")
    ap.add_argument("--dir", default=str(REPO / LOCKED_SET_DIR),
                    help="the locked-set directory")
    args = ap.parse_args(argv[1:])
    directory = Path(args.dir)

    print("check_lock: the locked validation set is what it was when it was locked")
    if not directory.exists():
        print(f"  ok — no {directory} yet; nothing has been locked.")
        return 0

    try:
        notes, problems = check(directory)
    except OSError as exc:
        print(f"cannot read the locked set: {exc}", file=sys.stderr)
        return 2

    for n in notes:
        print(f"  note {n}")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print("\nThe locked set is the only clean validation instrument this "
              "project will get.\nIts hashes are the proof that nothing moved "
              "after labelling.", file=sys.stderr)
        return 1
    print("  ok — nothing locked has changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
