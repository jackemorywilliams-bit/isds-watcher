"""Move each tracked note's currency anchor to HEAD — mechanically, not by hand.

WHY THIS EXISTS. `scripts/check_currency.py` fails a note whose anchor is older
than the last commit touching its declared paths. Every session that edits those
notes therefore has to move the anchor forward, and for two years that was a step
a model was *told* to do in prose — so it was done wrong, repeatedly, and carried
as "escalation 7, unfixed": a note that writes both itself and its ledgers in one
commit cannot name a commit later than itself, so it can never satisfy the guard
"by construction." That framing was wrong. The guard already excludes a commit
that touches nothing but tracked notes (`check_currency._is_maintenance`); the
missing piece was never a smarter guard, it was a **final, notes-only re-anchor
commit that a machine writes unconditionally** — which is this script.

WHAT IT DOES. For each note in `check_currency.TRACKED`, it rewrites the SHA in
the note's FIRST `Audited against <sha>` match to the current HEAD, and the date
in its FIRST `**Last updated:**` match to today. First-match only, because the
notes keep historical anchors below the current one and the guard reads
`anchors[0]`; the two conventions must not diverge, which is why the regexes are
imported from the guard rather than restated here.

    python3 scripts/reanchor.py            # rewrite; print what moved
    python3 scripts/reanchor.py --check    # exit 1 if any note WOULD move (CI)

FAIL-CLOSED. A tracked note with no anchor line, or a declared path that does not
exist, is the guard's problem to report; this script only moves anchors it finds
and says which it could not.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from datetime import date, datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import the guard's own constants so the anchor form, the date form and the set
# of tracked notes are defined in exactly one place. If the guard's regex changes,
# this script changes with it — by construction, not by memory.
_spec = importlib.util.spec_from_file_location(
    "check_currency", os.path.join(REPO, "scripts", "check_currency.py"))
_cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cc)
TRACKED = _cc.TRACKED
ANCHOR_RE = _cc.ANCHOR_RE
UPDATED_RE = _cc.UPDATED_RE


def _git(*args: str) -> str:
    return subprocess.run(["git", "-C", REPO, *args],
                          capture_output=True, text=True).stdout.strip()


def _anchor_target() -> str:
    """The commit the anchor SHOULD name: the newest commit reachable from HEAD
    that is not itself a maintenance commit.

    Targeting HEAD naively would be self-defeating: the re-anchor commit is a
    maintenance commit, so once it becomes HEAD a re-run would want to move the
    anchor onto it, `--check` would disagree with the guard, and the workflow
    would churn. The guard reads zero drift once the anchor names the last
    SUBSTANTIVE commit — everything after it is maintenance and excluded — so
    that is what the anchor names, using the guard's own definition of
    maintenance.
    """
    for sha in _git("rev-list", "--max-count=200", "HEAD").split("\n"):
        if sha and not _cc._is_maintenance(sha):
            return _git("rev-parse", "--short", sha)
    return _git("rev-parse", "--short", "HEAD")


def _today() -> str:
    # SOURCE_DATE_EPOCH keeps CI reproducible; otherwise the runner's UTC date.
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch and epoch.isdigit():
        return datetime.fromtimestamp(int(epoch), timezone.utc).date().isoformat()
    return date.today().isoformat()


def _reanchor_body(body: str, head: str, today: str) -> tuple[str, list[str]]:
    """Return (new_body, notes-on-what-moved). First match only for each form."""
    moved: list[str] = []

    m = ANCHOR_RE.search(body)
    if m and m.group(1) != head:
        moved.append(f"anchor {m.group(1)} -> {head}")
        body = body[:m.start(1)] + head + body[m.end(1):]
    elif not m:
        moved.append("NO ANCHOR (guard will fail this note)")

    d = UPDATED_RE.search(body)
    if d and d.group(1) != today:
        moved.append(f"date {d.group(1)} -> {today}")
        body = body[:d.start(1)] + today + body[d.end(1):]

    return body, moved


def run(check_only: bool) -> int:
    head = _anchor_target()
    today = _today()
    would_move = False

    for note in sorted(TRACKED):
        path = os.path.join(REPO, note)
        if not os.path.exists(path):
            print(f"  MISSING  {note}: tracked note does not exist")
            would_move = True
            continue
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        new_body, moved = _reanchor_body(body, head, today)
        real_moves = [m for m in moved if not m.startswith("NO ANCHOR")]
        if moved:
            would_move = True
            verb = "WOULD MOVE" if check_only else "moved"
            print(f"  {verb:<10} {note}: {'; '.join(moved)}")
        if new_body != body and not check_only:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_body)

    if not would_move:
        print(f"  ok       {len(TRACKED)} notes already anchored at {head}")
        return 0
    if check_only:
        print()
        print("A note's anchor is behind HEAD. The close-out re-anchor commit did not")
        print("run, or ran before the last substantive commit. Run scripts/reanchor.py")
        print("and commit the result as a notes-only maintenance commit.")
        return 1
    return 0


def main(argv: list[str]) -> int:
    print("reanchor: move each tracked note's currency anchor to HEAD")
    print()
    return run("--check" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
