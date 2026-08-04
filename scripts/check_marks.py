#!/usr/bin/env python3
"""Mechanical checks for backsourced bibliographies — the enforcement surface of the
Carrying-Span Rule (``prompts/carrying_span_rule.md``, adopted 2026-08-03 as amended).

WHY THIS EXISTS. A rule already existed when three entries cited sources for
propositions those sources do not contain, and it did not stop them. The council's
finding (R5) was that rules bind in this project when attached to an artifact that
fails — with the officer's correction that because this was a discipline failure, the
remedy is enforcement AND a carrier, not a carrier instead of enforcement. This is
the carrier.

WHAT IT IMPLEMENTS. R5 ranks five mechanisms in descending strength. Tier 1,
transcription, needs no code — a carrying span cannot be produced without opening the
source at that place. This module implements tiers 2, 3 and 5:

  * tier 2, MARK PARITY — one verification statement per entry; P/Q/D/V present and
    non-empty; Q carrying a quotation pair and a pinpoint token.
  * tier 3, NONZERO-REFERENT PARITY (the officer's Amendment 2, "the highest-value
    mechanical addition in the session") — every screened term with a nonzero count
    must be either the source of Q or given a referent clause. Set membership over
    one line.
  * tier 5, DEGENERATE UNIFORMITY — string equality across V lines and across D
    lines. The only check in the set that detects performance directly rather than
    inferring it.

Tier 4, span-in-source, is not implemented: it needs the source document, which this
process does not have.

THIS DOCSTRING IS THE SINGLE STATEMENT OF WHAT THE SCRIPT CHECKS. `prompts/`, the
template and the agent definitions point here rather than restate it — four
paraphrases of one scope is how a reader ends up hand-checking what CI already gates,
or trusting a gate that does not exist.

COVERAGE IS CONDITIONAL, AND THE CLI REPORTS IT PER RUN — read the run, not this
paragraph, for how much was checked. An entry written in the legacy
`**Backsourcing verification.**` form has no P/Q/D/V, so tier 2 reduces to statement
presence and tiers 3 and 5 do not run on it at all. When the council adopted the rule
every entry in `lit-review/` was in that form, so the strict checks were exercised on
nothing; whether that is still true is a question for the summary line, which is why
no count is written here. (A number in a file nothing updates is the staleness R8
recorded, and this change fixed exactly that pattern elsewhere.) Tier 3 additionally
requires a screen record in the V mark; a V mark that records no screen is not
flagged, because the rule locates that obligation in step 2 and this module does not
police step 2.

WHAT IT CANNOT DO — stated here rather than discovered later, because overstating a
check is how a green run comes to mean more than it should.

It cannot tell whether a span carries its proposition. That is entailment, the rule's
declared load, and R6 leaves it exactly where it was. It cannot see a quote truncated
before its limiting clause; R6 records carrying and truncation as independent classes
that do not see each other's failures. It does not read the D mark's contents, so a
case carded without its disposition passes the presence check. And it makes no claim
about the three 2026-08-03 entries: R9 established those never existed in version
control, so what form they took is not a fact this repository holds.

What the check buys is narrower and still worth having: the shape the rule produces
becomes countable by someone who is not the author. A file that passes has satisfied
the countable part and nothing more — the enforcement surface for the failure that
actually occurred was Dr. Benavides's margin, and it still is.

CLI:
    python scripts/check_marks.py lit-review/*.md

Exit 0 clean, 1 on any violation, 2 on usage error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# The rule governs cited sources, not the memo's argument, so the check is scoped to
# the section that holds entries.
_BIB_HEADING_RE = re.compile(r"^(#{1,3})\s+.*\bbibliograph", re.IGNORECASE)
_HEADING_RE = re.compile(r"^(#{1,6})\s+")
_ENTRY_RE = re.compile(r"^###\s+(.*\S)\s*$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")

# A verification statement, in either accepted form. The rule specifies what this
# statement must CONTAIN; it did not invent the statement, which both memos already
# promised in their §VII methodological note.
_V_LEGACY_RE = re.compile(r"^\s*\*\*(?:Backsourcing\s+)?[Vv]erification\.?\*\*")
_V_MARK_RE = re.compile(r"^\s*\*{0,2}V\s*[—–-]\s*\**")

_MARK_RES = {
    "P": re.compile(r"^\s*\*{0,2}P\s*[—–-]\s*\**"),
    "Q": re.compile(r"^\s*\*{0,2}Q\s*[—–-]\s*\**"),
    "D": re.compile(r"^\s*\*{0,2}D\s*[—–-]\s*\**"),
    "V": _V_MARK_RE,
}

# R5.2's adopted tier-2 test is "Q carrying a quotation pair AND a pinpoint token" —
# both halves, because a pinpoint with no quoted words says where something is
# without saying what it was.
_QUOTE_PAIR_RE = re.compile(r"[\"“][^\"”]{3,}[\"”]")
_PINPOINT_RE = re.compile(
    r"¶|\bparas?\.?\s*\d|\bpp?\.\s*\d|\bat\s+\d|§|\bart\.?\s*\d|\[[^\]]+\]",
    re.IGNORECASE,
)

# A named exit under clause 3 — the honest outcome when nothing carries the
# proposition. An entry that took an exit is compliant and must not be flagged for
# lacking a span. Deliberately NOT a bare "exit": "no exit was needed here" would
# then buy a writer out of both the quotation and the pinpoint check.
_EXIT_RE = re.compile(
    r"no span (?:located|found)|exits?\s*\(?[i1-4]|exits?\s*:|exit taken|"
    r"took (?:the )?(?:first|second|third|fourth|another )?exit|"
    r"(?:first|second|third|fourth) exit|"
    r"proposition (?:narrowed|rewritten)|source (?:was )?dropped|"
    r"unread|could not (?:be )?retriev|not (?:been )?read",
    re.IGNORECASE,
)

# One item of a screen record: "term: 4", '"trade secret": 0', "TRIPS 0". The colon is
# optional because the rule's own worked line omits it. ANCHORED AT THE END of its
# chunk: in a screen item the count is the last thing said, whereas in prose a number
# is followed by more words. That one property separates "recognition 2" from "both
# occurrences concern Article 39 of the Agreement" — and the second is not a
# hypothetical, it is the shape of the referent clause Amendment 2 demands, so without
# the anchor the check fires on the sentence written to satisfy it.
_SCREEN_ITEM_RE = re.compile(
    r"[\"“«]?([A-Za-z][A-Za-z0-9 .'’/()-]{2,40}?)[\"”»]?\s*:?\s*(\d{1,3})"
    r"(?:\s+(?:occurrences?|hits?|times|results?|matches))?\s*[.)]?\s*$")
# A screened term is a term of art, not a clause. These two guards keep swallowed
# prose out: "The tribunal held at 249" ends in a final count and would otherwise
# parse as a term. Parentheses stay ALLOWED in a term because the rule's own worked
# rigid designators are "Art. 39(3)" and "fork in the road (FITR)" — disqualifying
# them would mean the check cannot read the very terms it tells the writer to screen.
_TERM_STOPWORDS = {"the", "a", "an", "this", "that", "these", "those", "both", "it",
                   "its", "their", "there", "and", "but", "for", "with", "at", "on",
                   "no", "ecf", "op", "mem", "v"}
_MAX_TERM_WORDS = 5
_SCREENED_AT_RE = re.compile(r"screen(?:ed)?\b", re.IGNORECASE)
# Chunk separators, including a sentence boundary, so "disclosure 0. P's rigid
# designator is ..." yields the item rather than losing it to the sentence after it.
_CHUNK_SPLIT_RE = re.compile(r"[;,]|[—–]|\.\s+(?=[A-Z])")
# A date is not a screened term: "(D.D.C. May 6, 2021)" splits to "...May 6", whose
# count IS final. Month names and parentheses are the two tells.
_MONTH_RE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\w*\.?$", re.IGNORECASE)
# A four-digit run inside a term is a year — "checked 2026-08-03" would otherwise
# parse as the term "checked 2026-08-" with a count of 3. Rigid designators with
# numbers ("Art. 39(3)") carry no four-digit run and survive this.
_YEAR_RE = re.compile(r"\d{4}")
# Bracketed placeholders are not pinpoints. "[TBD]" says a locator is owed, not where
# the words are.
_PLACEHOLDER_RE = re.compile(r"^\[(tbd|tk|todo|cite|xx+|\.\.\.|\?+)\]$", re.IGNORECASE)


def _bibliography_lines(text: str) -> list[tuple[int, str]]:
    """The ``(lineno, line)`` pairs inside the bibliography section, 1-indexed.

    Fenced code is skipped so a template's illustrative blocks are not read as real
    entries. Empty when the file has no bibliography heading — the caller reports
    that as "not checked", never as "ok"."""
    lines = text.splitlines()
    start: int | None = None
    depth = 2
    in_fence = False
    for i, line in enumerate(lines):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        m = _BIB_HEADING_RE.match(line)
        if not in_fence and m:
            start = i + 1
            depth = len(m.group(1))
            break
    if start is None:
        return []
    out: list[tuple[int, str]] = []
    in_fence = False
    for i in range(start, len(lines)):
        if _FENCE_RE.match(lines[i]):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # The section ends at the next heading of the SAME level or higher. Closing
        # only on h2 would let a bibliography opened at h3 swallow its sibling h3
        # subsections and report each as an entry with no verification statement.
        h = _HEADING_RE.match(lines[i])
        if h and len(h.group(1)) <= depth:
            break
        out.append((i + 1, lines[i]))
    return out


def _entries(text: str) -> list[dict]:
    """Split the bibliography into entries: ``{title, line, body:[str]}``.

    Content before the first ``###`` is the section's methodological note, not an
    entry, and is deliberately dropped."""
    out: list[dict] = []
    current: dict | None = None
    for lineno, line in _bibliography_lines(text):
        m = _ENTRY_RE.match(line)
        if m:
            current = {"title": m.group(1), "line": lineno, "body": []}
            out.append(current)
        elif current is not None:
            current["body"].append(line)
    return out


_BLOCK_END_RE = re.compile(r"^\s*(---+|\*\*\*+|___+)\s*$")
# A LABELLED paragraph ends a mark — "**Descriptive annotation.**", "**Relevance to
# the project.**". Inline emphasis does NOT: "**joined to the merits**, not decided"
# is a continuation, and it is the single phrase most likely to be bolded in a D mark
# because it is the disposition the rule exists to surface. Terminating on any "**"
# would drop it silently and leave the entry passing.
_LABEL_RE = re.compile(r"^\s*\*\*[^*]+\.\*\*")


def _fold_marks(body: list[str]) -> dict[str, list[str]]:
    """``{mark: [content, ...]}``, with continuation lines folded into their mark.

    A mark runs from its ``X —`` prefix until a blank line, another mark, a heading,
    a legacy verification statement, a blockquote or a rule. Reading marks one
    physical line at a time would be a live defect rather than a limitation: both
    `prompts/carrying_span_rule.md` and the template display the V mark wrapped over
    four lines, so a per-line reader sees a fragment. Amendment 2 would then pass a
    non-compliant entry whose nonzero term sits on line 2, and fail a compliant one
    whose referent clause wrapped — the check defeated by a line break."""
    out: dict[str, list[str]] = {m: [] for m in _MARK_RES}
    current: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, buf
        if current is not None:
            joined = " ".join(part.strip() for part in buf if part.strip())
            out[current].append(joined.strip().strip("*").strip())
        current, buf = None, []

    for line in body:
        started = next((m for m, rx in _MARK_RES.items() if rx.match(line)), None)
        if started is not None:
            flush()
            current = started
            buf = [_MARK_RES[started].sub("", line, count=1)]
            continue
        if current is None:
            continue
        stripped = line.strip()
        if (not stripped or _ENTRY_RE.match(line) or _V_LEGACY_RE.match(line)
                or _HEADING_RE.match(line) or _BLOCK_END_RE.match(line)
                or _LABEL_RE.match(line) or stripped.startswith(">")):
            flush()
            continue
        buf.append(line)
    flush()
    return out


def _screen_terms(v_line: str) -> list[tuple[str, int]]:
    """``(term, count)`` pairs from a V mark's screen record, in order.

    Only the part of the line at/after "screened" is parsed, so a citation earlier in
    the V mark is not mistaken for a screened term. The WHOLE tail is scanned, not
    just the part before the first dash: the rule's own worked line puts a referent
    clause mid-line, and stopping at the first dash silently drops every term after
    it — which would make a missing referent clause undetectable exactly where it is
    most likely."""
    m = _SCREENED_AT_RE.search(v_line)
    if not m:
        return []
    out: list[tuple[str, int]] = []
    for chunk in _CHUNK_SPLIT_RE.split(v_line[m.end():]):
        hit = _SCREEN_ITEM_RE.search(chunk)
        if not hit:
            continue
        term = hit.group(1).strip().strip(".'’")
        words = term.split()
        if _MONTH_RE.search(term) or _YEAR_RE.search(term):
            continue  # a date, not a screened term: "checked 2026-08-03" is not a term
        if not words or words[0].lower() in _TERM_STOPWORDS or len(words) > _MAX_TERM_WORDS:
            continue  # a clause, not a term of art
        if term.lower() in _TERM_STOPWORDS or len(term) <= 2:
            continue
        out.append((term, int(hit.group(2))))
    return out


def check_text(text: str, path: str = "") -> dict:
    """Check one document. Never raises."""
    violations: list[dict] = []
    four_mark = 0
    legacy = 0
    with_statement = 0
    screen_records = 0
    has_section = bool(_bibliography_lines(text))

    entries = _entries(text)
    seen_v: dict[str, str] = {}
    seen_d: dict[str, str] = {}

    for e in entries:
        body = e["body"]
        title = e["title"]
        line = e["line"]

        def flag(problem: str) -> None:
            violations.append({"line": line, "entry": title, "problem": problem})

        v_lines = [ln for ln in body if _V_LEGACY_RE.match(ln) or _V_MARK_RE.match(ln)]
        if not v_lines:
            flag("no verification statement — §VII promises one per entry, and the "
                 "rule's V mark is that statement")
        elif len(v_lines) > 1:
            # Parity is the countable property; two statements for one entry means a
            # reader cannot tell which one was checked.
            flag(f"{len(v_lines)} verification statements — expected exactly 1")
        else:
            with_statement += 1

        # An entry is in the rule's form if ANY of the four marks appears. Gating on
        # P alone would let an author drop P and silently escape the Q/D/V checks.
        present = _fold_marks(body)
        if any(present.values()):
            four_mark += 1
            for mark in ("P", "Q", "D", "V"):
                if not present[mark]:
                    flag(f"four-mark entry missing the {mark} mark")
                elif not any(present[mark]):
                    flag(f"the {mark} mark is empty")

            for content in present["Q"]:
                if not content or _EXIT_RE.search(content):
                    continue  # a named exit is compliance, not a violation
                if not _QUOTE_PAIR_RE.search(content):
                    flag("Q mark has no quoted span and names no exit "
                         "(rule clause 3: the span is the evidence)")
                pin = _PINPOINT_RE.search(content)
                if not pin or _PLACEHOLDER_RE.match(pin.group(0)):
                    flag("Q mark has no pinpoint and names no exit "
                         "(rule clause 3: a span without a locator is not checkable)")

            # Amendment 2 — nonzero-referent parity.
            q_text = " ".join(present["Q"]).lower()
            for content in present["V"]:
                terms = _screen_terms(content)
                if terms:
                    screen_records += 1
                for term, count in terms:
                    if count == 0:
                        continue
                    if term.lower() in q_text:
                        continue  # the nonzero term is the source of Q
                    # A referent clause is a second occurrence of the term in the V
                    # mark, outside its own "term: count" token.
                    occurrences = len(re.findall(re.escape(term), content, re.IGNORECASE))
                    if occurrences < 2:
                        flag(f'screened term "{term}" has a nonzero count ({count}) '
                             "but is neither the source of Q nor given a referent "
                             "clause (rule, Amendment 2)")

            for key in present["V"]:
                if key and key in seen_v and seen_v[key] != title:
                    flag(f"V mark is byte-identical to the one on \"{seen_v[key]}\" "
                         "— degenerate uniformity (R5.5)")
                elif key:
                    seen_v.setdefault(key, title)
            for key in present["D"]:
                if key and key in seen_d and seen_d[key] != title:
                    flag(f"D mark is byte-identical to the one on \"{seen_d[key]}\" "
                         "— degenerate uniformity (R5.5)")
                elif key:
                    seen_d.setdefault(key, title)
        elif v_lines:
            legacy += 1

    return {
        "path": path,
        "has_section": has_section,
        "entries": len(entries),
        "with_statement": with_statement,
        "four_mark": four_mark,
        "legacy": legacy,
        "screen_records": screen_records,
        "violations": violations,
    }


def check_file(path: str) -> dict:
    """Read and check ``path``. An unreadable file is itself a violation — silence
    here would report a file clean because it could not be opened."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return {"path": path, "has_section": False, "entries": 0, "with_statement": 0,
                "four_mark": 0, "legacy": 0,
                "violations": [{"line": 0, "entry": "", "problem": f"cannot read: {exc}"}]}
    return check_text(text, path)


def main(argv: list[str]) -> int:
    paths = argv[1:]
    if not paths:
        print("usage: python scripts/check_marks.py <file.md> [file.md ...]",
              file=sys.stderr)
        return 2

    failed = False
    totals = {"entries": 0, "four_mark": 0, "legacy": 0, "screen_records": 0}
    for path in paths:
        r = check_file(path)
        for k in totals:
            totals[k] += r.get(k, 0)
        if r["entries"] == 0 and not r["violations"]:
            # NOT "ok" — nothing was examined, and reporting a clean run over an
            # empty examination is the tool-status-as-source-state pattern this
            # project already has on record. A file with no bibliography section and
            # a file whose section holds no entries are different facts; say which.
            why = ("no bibliography section found" if not r["has_section"]
                   else "bibliography section holds no entries")
            print(f"{r['path']}: {why} — nothing checked")
            continue
        print(f"{r['path']}: {r['entries']} entries, {r['with_statement']} carry a "
              f"verification statement ({r['four_mark']} in the rule's four-mark form, "
              f"{r['legacy']} legacy)")
        for v in r["violations"]:
            failed = True
            where = f"{r['path']}:{v['line']}" if v["line"] else r["path"]
            entry = f" [{v['entry']}]" if v["entry"] else ""
            print(f"  FAIL {where}{entry} — {v['problem']}")
        if not r["violations"]:
            print("  ok — mark parity holds")

    if failed:
        print("\nMechanical checks failed. See prompts/carrying_span_rule.md.",
              file=sys.stderr)
        return 1

    # Report what was EXERCISED, not what is implemented. Naming a tier as passing
    # when it ran on zero entries is tool-status-as-source-state in the summary line —
    # the pattern this module's docstring says it is guarding against.
    print("\nMechanical checks pass. Exercised:")
    print(f"  mark parity          {totals['entries']} entries"
          + (f" — {totals['legacy']} in the legacy form, where this reduces to "
             "verification-statement\n                       presence, because "
             "P/Q/D/V are absent" if totals["legacy"] else ""))
    print(f"  nonzero-referent     {totals['screen_records']} screen records"
          + ("  (nothing to check)" if not totals["screen_records"] else ""))
    print(f"  degenerate uniformity {totals['four_mark']} four-mark entries"
          + ("  (nothing to check)" if not totals["four_mark"] else ""))
    print("\nThis establishes entry SHAPE only — not that any span exists in its "
          "source, and not\nthat any span carries its proposition. Transcription "
          "(R5 tier 1) and span-in-source\n(tier 4) are not checked here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
