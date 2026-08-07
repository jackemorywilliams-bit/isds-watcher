"""Make verifying a digest entry a thirty-second job, so the count can move.

WHY THIS EXISTS. The website carries this sentence:

    "No digest entry and no sentence on this website has been checked by a human
    against its original source; every archived digest entry to date is
    machine-screened only."

That is true, and it has been true for every day this project has run. The response
to it so far has been to word the disclosure more carefully. That is not a fix. A
disclosure that never changes is a permanent confession, and polishing its grammar
is how a gap gets admitted instead of closed.

The reason the count is zero is not that the operator refuses. It is that nothing
made it cheap. There are **thirteen distinct published entries** across eleven runs.
That is an evening's work if each one is a single screen and a single keypress, and
it is unbounded work if it means hand-diffing markdown against a browser tab.

So this is the tool that makes it a keypress. It does not verify anything itself —
it cannot, and any version of it that tried would be the machine grading its own
homework. It puts the annotation and the source URL side by side, asks the one
question that matters, and records the operator's answer in the append-only ledger
that already exists.

WHAT IT ASKS. For each entry, exactly one question: **does the source at this URL
support the annotation this project wrote about it?** Not "is the link alive." Not
"is it on theme." Whether the sentence the project published is carried by the
document it names.

WHAT IT WRITES. Nothing of its own. Every verdict goes through
`scripts/verify.py::mark`, which is append-only and refuses automated callers — so
this tool is a presentation layer over the operator's own signature, and a claim it
records is indistinguishable from one marked by hand.

    python3 scripts/verify_digest.py            # walk the unverified entries
    python3 scripts/verify_digest.py --status   # the count, and what is left
    python3 scripts/verify_digest.py --all      # revisit entries already marked
"""

from __future__ import annotations

import argparse
import glob
import importlib.util
import os
import re
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_spec = importlib.util.spec_from_file_location(
    "verify", os.path.join(REPO, "scripts", "verify.py"))
verify = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify)

FIELD = re.compile(r"^- \*\*(?P<k>[^*]+):\*\*\s*(?P<v>.*)$", re.M)
SECTION = re.compile(r"^## (?P<h>.+?)\n(?P<body>.*?)(?=\n## |\n---|\Z)", re.M | re.S)


def _clean(s: str) -> str:
    s = re.sub(r"\[Read the original ↗\]\([^)]*\)", "", s)
    s = re.sub(r"^\s*>\s?", "", s, flags=re.M)
    return re.sub(r"\s+", " ", s).strip()


def entries() -> list[dict]:
    """Every published digest article, newest run first, deduplicated by URL.

    Deduplicated because `italaw.com/cases/12153` was published on two consecutive
    days and the classifier gave it contradictory verdicts. Asking the operator the
    same question twice about one document would be a defect of this tool, not a
    feature of the archive.
    """
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(REPO, "digests", "*", "articles", "*.md")),
                       reverse=True):
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        fields = {m.group("k").strip(): _clean(m.group("v")) for m in FIELD.finditer(body)}
        url = fields.get("Link", "")
        if not url or url in out:
            continue
        secs = {m.group("h").strip(): _clean(m.group("body")) for m in SECTION.finditer(body)}
        title = body.splitlines()[0].lstrip("# ").strip() if body.strip() else "(untitled)"
        out[url] = {
            "path": os.path.relpath(path, REPO),
            "run": os.path.basename(os.path.dirname(os.path.dirname(path)))[:10],
            "title": title,
            "url": url,
            "source": fields.get("Source", ""),
            "relevance": fields.get("Relevance", ""),
            "rings": fields.get("Rings matched", ""),
            "annotation": secs.get("Annotation", ""),
            "notable": secs.get("Notable line (from source)", ""),
        }
    return list(out.values())


def claim_for(e: dict) -> tuple[str, str, str]:
    """(claim_id, claim_text, source_locator) for one entry.

    The claim is the annotation — the sentence the project published about the
    document. Not the headline, not the score. The annotation is what a reader
    takes away and it is the thing that can be wrong.
    """
    text = e["annotation"] or e["title"]
    return verify.claim_id(text, e["url"]), text, e["url"]


def status_counts() -> tuple[int, int, int, list[dict]]:
    claims = verify.replay()
    ents = entries()
    ok = rejected = 0
    pending = []
    for e in ents:
        cid, _, _ = claim_for(e)
        st = verify.current_status(cid, claims) if cid in claims else None
        if st == "operator_verified":
            ok += 1
        elif st == "operator_rejected":
            rejected += 1
        else:
            pending.append(e)
    return ok, rejected, len(ents), pending


def _show(e: dict, n: int, total: int) -> None:
    w = 78
    print("\n" + "=" * w)
    print(f"  {n} of {total}   ·   digest {e['run']}   ·   {e['source']}")
    print("=" * w)
    print(textwrap.fill(e["title"], w))
    print()
    print(f"  OPEN THIS:  {e['url']}")
    print(f"  scored {e['relevance']}   rings: {e['rings'] or '—'}")
    print()
    print("  THE PROJECT WROTE:")
    for line in textwrap.wrap(e["annotation"] or "(no annotation)", w - 4):
        print(f"    {line}")
    if e["notable"] and e["notable"].upper() != "N/A":
        print()
        print("  QUOTED AS FROM THE SOURCE:")
        for line in textwrap.wrap(e["notable"], w - 4):
            print(f"    {line}")
    print()
    print("  Does the source at that URL support what the project wrote?")
    print("    [y] yes        [n] no, it does not")
    print("    [u] source unreachable / paywalled     [s] skip     [q] quit")


def walk(revisit: bool) -> int:
    ok, rejected, total, pending = status_counts()
    todo = entries() if revisit else pending
    if not todo:
        print(f"Nothing to do — all {total} entries carry an operator verdict.")
        return 0

    print(f"\n{total} distinct published entries. "
          f"{ok} verified, {rejected} rejected, {len(pending)} unreviewed.")
    print("Each one is a URL and a question. Answers are appended to the ledger "
          "under your git identity and cannot be rewritten.")

    for i, e in enumerate(todo, 1):
        _show(e, i, len(todo))
        try:
            ans = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nStopped. Everything answered so far is recorded.")
            return 0
        if ans == "q":
            print("Stopped. Everything answered so far is recorded.")
            return 0
        if ans in ("", "s"):
            continue

        cid, text, loc = claim_for(e)
        claims = verify.replay()
        if cid not in claims:
            verify.create_claim(text, loc, source_authority="primary",
                                claim_type="digest_annotation")
        if ans == "y":
            note = input("  note (optional): ").strip()
            verify.mark(cid, "operator_verified", note=note or
                        "digest annotation checked against source",
                        quote_ok=True, scope_ok=True, _operator_cli=True)
            print("  recorded: VERIFIED")
        elif ans == "n":
            note = input("  what is wrong with it: ").strip()
            if not note:
                print("  a rejection needs a reason. Skipped.")
                continue
            verify.mark(cid, "operator_rejected", note=note,
                        quote_ok=False, scope_ok=False, _operator_cli=True)
            print("  recorded: REJECTED")
        elif ans == "u":
            verify.record_metadata(cid, "access", {"status": "unreachable",
                                                    "url": loc})
            print("  recorded: source unreachable — left unverified, not rejected")

    ok, rejected, total, pending = status_counts()
    print(f"\n{ok} of {total} verified, {rejected} rejected, {len(pending)} left.")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--status", action="store_true", help="counts only")
    p.add_argument("--all", action="store_true",
                   help="revisit entries that already carry a verdict")
    args = p.parse_args(argv)

    ok, rejected, total, pending = status_counts()
    if args.status:
        print(f"digest entries: {total} distinct")
        print(f"  operator_verified: {ok}")
        print(f"  operator_rejected: {rejected}")
        print(f"  unreviewed:        {len(pending)}")
        if pending:
            print("\nunreviewed:")
            for e in pending:
                print(f"  {e['run']}  {e['title'][:62]}")
        if ok == 0:
            print("\nWhile this is 0 the website's disclosure is accurate and should")
            print("stay exactly as it is. It is a fact about the record, not wording")
            print("to be softened.")
        return 0
    return walk(args.all)


if __name__ == "__main__":
    sys.exit(main())
