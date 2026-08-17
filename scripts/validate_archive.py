"""Validate every archived digest for internal consistency and methodology
compliance. This is the guardrail for the three failure modes we hit in
development, so they fail loudly instead of shipping:

  1. Sub-floor items in the archive. The methodology says nothing below
     RELEVANCE_FLOOR is ever surfaced; an old run had surfaced 5–15 scorers.
  2. Placeholder / parse-failure titles ("View case details", "(untitled)",
     empty) — a source-parser bug that reached the digest.
  3. Counts that disagree across surfaces — meta.json vs the article files vs
     the email footer for the same run.

Run:        python scripts/validate_archive.py   (exit 1 on any problem)
Import:     from validate_archive import validate_archive  -> list[str]
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config  # noqa: E402

FLOOR = config.RELEVANCE_FLOOR
THRESHOLD = config.load_config().threshold

GENERIC_TITLES = {
    "", "(untitled)", "view case details", "view details", "case details",
    "details", "read more", "more",
}


def _score(text: str) -> int | None:
    m = re.search(r"\*\*Relevance:\*\* (\d+)", text)
    return int(m.group(1)) if m else None


def _title(text: str) -> str:
    m = re.search(r"^# \d+\.\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def validate_archive(root: str = "digests") -> list[str]:
    """Return a list of human-readable problems; empty means the archive is clean."""
    problems: list[str] = []
    for folder in sorted(glob.glob(os.path.join(root, "*_ISDS-Thematic-Watch"))):
        name = os.path.basename(folder)
        arts = sorted(glob.glob(os.path.join(folder, "articles", "*.md")))
        scores: list[int] = []
        for a in arts:
            t = open(a, encoding="utf-8").read()
            s, title = _score(t), _title(t)
            base = os.path.basename(a)
            if s is None:
                problems.append(f"{name}/{base}: no parseable relevance score")
            else:
                scores.append(s)
                if s < FLOOR:
                    problems.append(
                        f"{name}/{base}: scores {s} < floor {FLOOR} "
                        "(methodology: never surfaced)")
            if title.strip().lower() in GENERIC_TITLES:
                problems.append(f"{name}/{base}: placeholder title {title!r}")

        accepted = len(arts)
        matches = sum(1 for s in scores if s >= THRESHOLD)
        leads = accepted - matches

        meta_path = os.path.join(folder, "meta.json")
        if not os.path.exists(meta_path):
            problems.append(f"{name}: missing meta.json")
        else:
            try:
                meta = json.load(open(meta_path, encoding="utf-8"))
            except (ValueError, OSError) as exc:
                problems.append(f"{name}: meta.json unreadable ({exc})")
                meta = None
            if meta is not None:
                if meta.get("accepted") != accepted:
                    problems.append(
                        f"{name}: meta accepted={meta.get('accepted')} but "
                        f"{accepted} article file(s) on disk")
                # Matches the validation gate held for operator review are
                # counted in meta but deliberately absent from disk. meta must
                # still reconcile: disk matches + held = screened matches.
                # Folders written before the gate carry no held field (0), so
                # the check stays exactly as strict for them.
                held = int(meta.get("held_for_review", 0) or 0)
                if meta.get("matches") != matches + held:
                    problems.append(
                        f"{name}: meta matches={meta.get('matches')} but "
                        f"{matches} item(s) >= {THRESHOLD} on disk"
                        + (f" plus {held} held for review" if held else ""))
                if meta.get("watch_list_leads") != leads:
                    problems.append(
                        f"{name}: meta watch_list_leads="
                        f"{meta.get('watch_list_leads')} but computed {leads}")

        ix = os.path.join(folder, "index.html")
        if os.path.exists(ix):
            h = re.sub(r"\s+", " ", open(ix, encoding="utf-8").read())
            fm = re.search(r"Matches \(&ge;\d+\): (\d+)", h)
            fa = re.search(r"Accepted \(shown\): (\d+)", h)
            if fm and int(fm.group(1)) != matches:
                problems.append(
                    f"{name}: email footer matches={fm.group(1)} != {matches}")
            if fa and int(fa.group(1)) != accepted:
                problems.append(
                    f"{name}: email footer accepted={fa.group(1)} != {accepted}")
    return problems


def main() -> int:
    problems = validate_archive()
    if problems:
        print(f"ARCHIVE VALIDATION FAILED — {len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print("Archive OK: every digest obeys the relevance floor, titles are real, "
          "and meta/article/email counts reconcile.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
