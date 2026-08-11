"""Fifth guard: a note may not claim to be current when it is not.

WHY THIS EXISTS, stated plainly because the reason is embarrassing.

Every time this project audited itself, the audit found that the previous
"everything is up to date" was false. On 2026-08-06 alone: a Ferguson correction
that fixed two of three sites and left the third asserting the opposite fourteen
lines away; an inverted case disposition surviving in the one paragraph every
session reads first; a closed escalation carried as unresolved for two days with
both its predicates false; a registry claiming a 23-entry table against a 24-entry
table; and a note stamped RATIFIED asserting that a script in the repository does
not exist.

None of those were hard to find. Every one was found by a human-directed audit,
after the claim of currency had already been made and believed. The defect is not
that the notes go stale — notes always go stale. The defect is that **the claim of
currency is asserted in prose and nothing checks it**, so "I've updated everything"
and "I believe I've updated everything" are indistinguishable to a reader.

WHAT IT CHECKS. Four kinds of claim that this project's notes actually make, each
of which is mechanically falsifiable:

  1. ANCHORS.   `*Audited against `<sha>`* ...` — the sha must exist, must be an
                ancestor of HEAD, and the note must be flagged if commits have
                touched its declared paths since. A note anchored 14 commits back
                is not current and should not read as though it is.
  2. DATES.     `**Last updated:** YYYY-MM-DD` — must not be older than the last
                commit that touched the file. `STATE_OF_THE_ANSWER.md` said
                2026-08-05 after two commits edited it on 2026-08-06.
  3. COMMITS.   Any `` `<sha>` `` cited as closing or landing something must exist
                and be an ancestor of HEAD. Catches a thread citing a commit from
                an unmerged branch.
  4. PR CITES.  `` `<sha>`, PR #N `` — N must be the PR that actually merged that
                sha. A thread cited `373cce6` to PR #60; it merged via PR #59.

WHAT IT DELIBERATELY DOES NOT DO. It does not check whether a note's *content* is
true. No program can. It checks whether the note's own claims about its currency
survive contact with git. A note can be perfectly current by this guard and still
be wrong about everything it says — which is why the output says so.

FAIL-CLOSED. A declared path that does not exist is a FAILURE, not a skip: it means
the note is auditing something that has moved or been deleted, and the anchor is
measuring nothing.

    python3 scripts/check_currency.py
    python3 scripts/check_currency.py --verbose
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Notes that make currency claims, and the paths each one claims to have audited.
# A note earns a place here by asserting its own freshness; if it makes no such
# claim, this guard has nothing to check and the note does not belong.
TRACKED: dict[str, list[str]] = {
    "agents/Agent Registry.md": [".claude/agents", "prompts", "src/models.py"],
    "agents/Workflow Threads.md": ["analytics", "state", "agents"],
    "agents/Claim Map.md": [
        "METHODOLOGY.md", "STATE_OF_THE_ANSWER.md", "lit-review",
        "prompts", ".claude/agents", "scripts/site_templates",
    ],
    "agents/Project Change Log.md": ["agents", "prompts", ".claude/agents"],
    "STATE_OF_THE_ANSWER.md": ["STATE_OF_THE_ANSWER.md"],
}

ANCHOR_RE = re.compile(r"[Aa]udited against `?([0-9a-f]{7,40})`?")
UPDATED_RE = re.compile(r"\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})")
PR_CITE_RE = re.compile(r"`([0-9a-f]{7,40})`,\s*PR #(\d+)")


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, text=True).stdout.strip()


def _exists(sha: str) -> bool:
    return subprocess.run(["git", "-C", REPO, "cat-file", "-e", f"{sha}^{{commit}}"],
                          capture_output=True).returncode == 0


def _is_ancestor(sha: str) -> bool:
    return subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", sha, "HEAD"],
                          capture_output=True).returncode == 0


def _is_maintenance(sha: str) -> bool:
    """A commit whose every changed file is itself a tracked note.

    Anchors live inside the notes they date, so the commit that moves an anchor
    always touches a tracked note — counted naively, no fully committed tree can
    ever pass this guard (the anchor would have to name its own commit). The
    check survived until 2026-08-11 only because anchor edits sat uncommitted,
    which is exactly the state this guard exists to end. A commit that changes
    nothing but tracked notes cannot alter the substance those notes audit, so
    it is excluded from drift. Any commit touching one other file still counts.
    """
    changed = _git("show", "--name-only", "--format=", sha)
    files = {l.strip() for l in changed.split("\n") if l.strip()}
    return bool(files) and files <= set(TRACKED)


def _commits_since(sha: str, paths: list[str]) -> list[str]:
    out = _git("log", "--format=%h %s", f"{sha}..HEAD", "--", *paths)
    lines = [l for l in out.split("\n") if l.strip()]
    return [l for l in lines if not _is_maintenance(l.split()[0])]


def _pr_for(sha: str) -> str | None:
    """The PR number whose merge commit brought `sha` to HEAD, if discoverable."""
    merge = _git("log", "--merges", "--ancestry-path", "--reverse",
                 "--format=%H %s", f"{sha}..HEAD")
    for line in merge.split("\n"):
        m = re.search(r"Merge pull request #(\d+)", line)
        if m:
            return m.group(1)
    return None


def check() -> tuple[int, int, list[str]]:
    msgs: list[str] = []
    checked = failed = 0

    for note, paths in sorted(TRACKED.items()):
        note_path = os.path.join(REPO, note)
        if not os.path.exists(note_path):
            failed += 1
            msgs.append(f"  FAIL     {note}: tracked note does not exist")
            continue

        # Fail closed on a declared path that has moved or been deleted.
        for p in paths:
            if not os.path.exists(os.path.join(REPO, p)):
                failed += 1
                msgs.append(f"  FAIL     {note}: declared audit path '{p}' does not exist")
                msgs.append("           The anchor is measuring nothing.")

        with open(note_path, encoding="utf-8") as fh:
            body = fh.read()

        # 1 — ANCHORS
        anchors = ANCHOR_RE.findall(body)
        if not anchors:
            failed += 1
            msgs.append(f"  FAIL     {note}: no `audited against <sha>` anchor")
            msgs.append("           A note that claims currency must say against what.")
        else:
            checked += 1
            newest = anchors[0]
            if not _exists(newest):
                failed += 1
                msgs.append(f"  FAIL     {note}: anchor {newest} is not a commit")
            elif not _is_ancestor(newest):
                failed += 1
                msgs.append(f"  FAIL     {note}: anchor {newest} is not an ancestor of HEAD")
                msgs.append("           It points at an unmerged or rewritten branch.")
            else:
                drift = _commits_since(newest, paths)
                if drift:
                    failed += 1
                    msgs.append(f"  STALE    {note}: {len(drift)} commit(s) touched its "
                                f"declared paths since {newest}")
                    for line in drift[:4]:
                        msgs.append(f"           {line}")
                    if len(drift) > 4:
                        msgs.append(f"           … and {len(drift) - 4} more")

        # 2 — DATES
        for stamp in UPDATED_RE.findall(body):
            checked += 1
            last = _git("log", "-1", "--format=%ad", "--date=short", "--", note)
            if last and stamp < last:
                failed += 1
                msgs.append(f"  FAIL     {note}: says 'Last updated: {stamp}' but was "
                            f"last committed {last}")

        # 3 & 4 — COMMIT AND PR CITATIONS
        for sha, pr in PR_CITE_RE.findall(body):
            checked += 1
            if not _exists(sha):
                failed += 1
                msgs.append(f"  FAIL     {note}: cites `{sha}`, which is not a commit")
                continue
            if not _is_ancestor(sha):
                failed += 1
                msgs.append(f"  FAIL     {note}: cites `{sha}` as landed; it is not an "
                            "ancestor of HEAD")
                continue
            actual = _pr_for(sha)
            if actual and actual != pr:
                failed += 1
                msgs.append(f"  FAIL     {note}: cites `{sha}` to PR #{pr}; it merged "
                            f"via PR #{actual}")

    return checked, failed, msgs


def main(argv: list[str]) -> int:
    verbose = "--verbose" in argv
    checked, failed, msgs = check()

    print("check_currency: a note may not claim to be current when it is not")
    print()
    if msgs:
        for m in msgs:
            print(m)
    else:
        print(f"  ok       {len(TRACKED)} notes, {checked} currency claims, all current")
    print()
    print(f"{checked} currency claims checked, {failed} failed")

    if failed:
        print()
        print("A stale anchor is not a formatting problem. It is a note telling the")
        print("next session it was audited against a state of the repository that no")
        print("longer exists — which is how a correction gets believed twice and")
        print("applied once.")
        return 1

    print()
    print("NOTE: this proves each note's claims about its own currency survive git.")
    print("It does NOT prove the note's content is true. A note can pass here and")
    print("be wrong about everything it says.")
    if verbose:
        print()
        for note, paths in sorted(TRACKED.items()):
            print(f"  {note}")
            print(f"    paths: {', '.join(paths)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
