#!/usr/bin/env python3
"""Vault graph builder — an on-demand mapping SCRIPT, not a council agent.

Curated MOC hubs (moc/) + one spoke-to-hub wikilink per note: hub-and-spoke, not
all-to-all, so the Obsidian graph reads as a map instead of a hairball.

Idempotent: links are inserted only inside a managed block
    <!-- graph:auto start --> ... <!-- graph:auto end -->
appended at the end of each note; only that block is ever rewritten; prose outside
it is never touched; a second run is byte-identical.

Hub assignment hierarchy (deterministic first):
    1. exact path rule        2. explicit frontmatter ``hub:``
    3. filename/content classifier
    4. LLM (ONLY with --allow-llm + ANTHROPIC_API_KEY; returns one of the six hub
       names or "AMBIGUOUS"; never forced to pick)
    5. otherwise LEFT UNASSIGNED and reported.

Run:  python scripts/build_graph.py --dry-run     # plan + scan boundary, no writes
      python scripts/build_graph.py               # apply
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

HUBS = [
    "00 - Project Map", "Workflow", "Research Question",
    "Council", "Evidence Ledger", "Digest Archive",
]

MAX_DIRECT_LINKS_PER_NOTE = 4  # outgoing non-hub links; hub links don't count

BLOCK_START, BLOCK_END = "<!-- graph:auto start -->", "<!-- graph:auto end -->"

# Site-source files: rendered to the public site by build_site.py, so they never
# receive a managed block (its "Map:" line would leak into the published page).
# They still count as nodes and get their edges from the hubs' own links to them.
SPOKE_BLOCK_EXEMPT = {"METHODOLOGY.md"}

# Scan boundary. Excludes generated output, caches, deps, and .gitignore matches.
EXCLUDE_DIRS = {".git", "docs", ".obsidian", "node_modules", ".venv", "venv",
                "__pycache__", ".pytest_cache", "state", "seeds", ".claude"}
EXCLUDE_TOP = {"digests"}  # generated digest archive: mapped via its hub, not per-file

# 1) Exact path rules (first match wins; paths are repo-relative, "/"-separated).
PATH_RULES: list[tuple[str, str]] = [
    ("moc/", ""),  # hubs themselves are never spokes
    ("lit-review/", "Research Question"),
    ("STATE_OF_THE_ANSWER.md", "Research Question"),
    ("think-tank/multi-agent/", "Council"),
    ("think-tank/", "Research Question"),
    ("COUNCIL.md", "Council"),
    ("prompts/", "Council"),
    ("analytics/", "Evidence Ledger"),
    ("HUMAN_REVIEW.md", "Evidence Ledger"),
    ("REVIEW.md", "Evidence Ledger"),
    ("briefs/", "Digest Archive"),
    ("digests/", "Digest Archive"),
    ("METHODOLOGY.md", "Workflow"),
    ("PLAN.md", "Workflow"),
    ("working/", "Workflow"),
    ("HANDOFF.md", "00 - Project Map"),
    ("README.md", "00 - Project Map"),
    ("MULTI_AGENT_ROADMAP.md", "00 - Project Map"),
]

# 3) Deterministic content classifier: keyword -> hub (checked in order).
CONTENT_RULES: list[tuple[str, str]] = [
    (r"research question|ferguson|kim memo|state of the answer", "Research Question"),
    (r"council|chairman|analyst|roundtable", "Council"),
    (r"digest|annotated bibliograph", "Digest Archive"),
    (r"ledger|verification|human review", "Evidence Ledger"),
    (r"pipeline|workflow|fingerprint|classifier|methodolog", "Workflow"),
]

_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def _rel(path: str, root: str) -> str:
    return os.path.relpath(path, root).replace(os.sep, "/")


def _git_ignored(paths: list[str], root: str) -> set[str]:
    if not paths or not os.path.isdir(os.path.join(root, ".git")):
        return set()
    try:
        out = subprocess.run(["git", "-C", root, "check-ignore", "--stdin"],
                             input="\n".join(paths), capture_output=True, text=True)
        return set(out.stdout.splitlines())
    except OSError:
        return set()


def scan(root: str) -> list[str]:
    """All in-boundary markdown notes, repo-relative. The boundary is printed by
    --dry-run so exclusions are visible, never silent."""
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = _rel(dirpath, root)
        parts = [] if rel_dir == "." else rel_dir.split("/")
        if parts and (parts[0] in EXCLUDE_TOP or any(p in EXCLUDE_DIRS for p in parts)):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS
                       and not (not parts and d in EXCLUDE_TOP)]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                found.append(_rel(os.path.join(dirpath, fn), root))
    ignored = _git_ignored(found, root)
    return [f for f in found if f not in ignored]


def _frontmatter_hub(text: str) -> str | None:
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fm = re.search(r"^hub:\s*(.+?)\s*$", m.group(1), re.MULTILINE)
    return fm.group(1).strip().strip('"') if fm else None


def _llm_hub(rel: str, text: str) -> str | None:
    """Step 4 — only when explicitly allowed. Returns a hub name or None
    (AMBIGUOUS / unavailable / invalid all mean None: never forced to pick)."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic

        from src import models  # centralized model config
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=models.UTILITY_MODEL, max_tokens=16,
            system=("Classify a research-vault note into exactly one hub. Reply with "
                    "ONLY one of: " + "; ".join(HUBS) + "; or AMBIGUOUS."),
            messages=[{"role": "user", "content": f"Note path: {rel}\n\n{text[:1500]}"}],
        )
        answer = "".join(b.text for b in resp.content if b.type == "text").strip()
        return answer if answer in HUBS else None
    except Exception:  # noqa: BLE001 - classifier failure means unassigned, not a crash
        return None


def assign_hub(rel: str, text: str, allow_llm: bool) -> tuple[str | None, str]:
    """Returns (hub | None, how). Unknown frontmatter hubs are REJECTED (reported),
    never silently accepted."""
    for prefix, hub in PATH_RULES:
        if rel == prefix or rel.startswith(prefix):
            return (hub or None), "path"
    fm = _frontmatter_hub(text)
    if fm is not None:
        if fm in HUBS:
            return fm, "frontmatter"
        return None, f"frontmatter-rejected({fm!r})"
    head = (rel + "\n" + text[:2000]).lower()
    for pat, hub in CONTENT_RULES:
        if re.search(pat, head):
            return hub, "content"
    if allow_llm:
        hub = _llm_hub(rel, text)
        if hub:
            return hub, "llm"
    return None, "unassigned"


def _countable_links(text: str, rel: str, existing: set[str]) -> tuple[list[str], list[str]]:
    """Outgoing wikilinks that count toward metrics: not in code fences or HTML
    comments, not self, deduped. Links to nonexistent notes are returned separately."""
    body = _HTML_COMMENT.sub("", _CODE_FENCE.sub("", text))
    stem = os.path.splitext(os.path.basename(rel))[0]
    seen, real, broken = set(), [], []
    for m in _WIKILINK.finditer(body):
        target = m.group(1).strip()
        if not target or target == stem or target in seen:
            continue
        seen.add(target)
        (real if target in existing else broken).append(target)
    return real, broken


def _managed_block(hub: str | None) -> str:
    inner = f"[[{hub}]]" if hub else "(unassigned — see build_graph.py report)"
    return f"{BLOCK_START}\nMap: {inner}\n{BLOCK_END}\n"


def apply_block(text: str, hub: str | None) -> str:
    """Rewrite ONLY the managed block; append one if absent; prose untouched."""
    block = _managed_block(hub)
    pat = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n?",
                     re.DOTALL)
    if pat.search(text):
        return pat.sub(block, text)
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return text + sep + block


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the vault hub-and-spoke graph.")
    ap.add_argument("--root", default=".")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-llm", action="store_true",
                    help="permit the step-4 LLM classifier for still-ambiguous notes")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    notes = scan(root)
    stems = {os.path.splitext(os.path.basename(n))[0] for n in notes} | set(HUBS)
    if args.dry_run:
        print("SCAN BOUNDARY")
        print(f"  root: {root}")
        print(f"  excluded dirs: {sorted(EXCLUDE_DIRS | EXCLUDE_TOP)} + .gitignore matches")
        print(f"  notes in scope: {len(notes)}")

    edges = 0
    degree: dict[str, int] = {h: 0 for h in HUBS}
    linked: dict[str, int] = {}
    warnings: list[str] = []
    broken_all: dict[str, list[str]] = {}
    unassigned: list[str] = []
    changed: list[str] = []

    for rel in notes:
        path = os.path.join(root, rel)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        is_hub = rel.startswith("moc/")
        exempt = rel in SPOKE_BLOCK_EXEMPT
        hub, how = (None, "hub") if is_hub else assign_hub(rel, text, args.allow_llm)
        if how.startswith("frontmatter-rejected"):
            warnings.append(f"{rel}: unknown hub in frontmatter {how}")
        new_text = text if (is_hub or exempt) else apply_block(text, hub)
        if not is_hub and not exempt and hub is None:
            unassigned.append(f"{rel} ({how})")

        real, broken = _countable_links(new_text, rel, stems)
        if broken:
            broken_all[rel] = broken
        direct = [t for t in real if t not in HUBS]
        hub_links = [t for t in real if t in HUBS]
        edges += len(real)
        linked[rel] = len(real)
        for t in hub_links:
            degree[t] += 1
        if not is_hub and len(direct) > MAX_DIRECT_LINKS_PER_NOTE:
            warnings.append(f"{rel}: {len(direct)} direct links exceeds cap "
                            f"{MAX_DIRECT_LINKS_PER_NOTE}")

        if new_text != text:
            changed.append(rel)
            if not args.dry_run:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new_text)

    orphans = [n for n, k in linked.items() if k == 0
               and not any(f"[[{os.path.splitext(os.path.basename(n))[0]}]]" in
                           open(os.path.join(root, m), encoding="utf-8").read()
                           for m in notes if m != n)]
    for h in HUBS:
        if degree[h] == 0:
            warnings.append(f"MOC orphaned (no spokes yet): {h}")

    verb = "would update" if args.dry_run else "updated"
    print(f"\nnodes: {len(notes)}  edges: {edges}  orphans: {len(orphans)}  "
          f"{verb}: {len(changed)}")
    print("hub degree: " + ", ".join(f"{h}={degree[h]}" for h in HUBS))
    if unassigned:
        print("UNASSIGNED (left unlinked, by design):")
        for u in unassigned:
            print(f"  - {u}")
    if broken_all:
        print("links to nonexistent notes (not counted as edges):")
        for rel, targets in sorted(broken_all.items()):
            print(f"  - {rel}: {targets}")
    for w in warnings:
        print(f"WARN: {w}")
    if args.dry_run and changed:
        print("planned edits (managed block only):")
        for c in changed:
            print(f"  - {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
