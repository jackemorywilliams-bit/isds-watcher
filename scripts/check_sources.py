"""Fourth guard: every quotation in a memo must exist in the source it names.

WHY THIS EXISTS. For three months this project verified award paragraphs,
treaty texts, court dockets and journal pagination, and never once verified
the two articles the entire research question rests on. Nothing checked them
because nothing could: the PDFs were not in the repo, so every claim about
what Kim and Ferguson argue was carried on memory of a reading done in April.
On 2026-08-06 the articles were finally read and the memos were audited
against them. The audit found nine substantive defects, including a risk
category that does not appear in Ferguson at all, an inverted disposition, an
authority base understated by roughly an order of magnitude, and a quotation
attributed to the wrong proposition.

WHAT IT CHECKS. For each memo with a declared source, every quoted span of
MIN_SPAN characters or more must appear verbatim in that source's extracted
text. A span that does not appear is a FAILURE.

WHAT IT DELIBERATELY DOES NOT DO. It does not judge whether a quotation is
used for the right proposition -- no program can. What it does instead is
print the source context around every match, so that "the string is present"
can never again be mistaken for "the attribution is correct." That distinction
is the one defect this guard cannot catch by itself and the one the operator
must eyeball, so it is surfaced rather than hidden.

FAIL-CLOSED, AND THIS IS THE POINT. A declared source whose PDF is absent is a
FAILURE, not a skip. The original defect was silent absence of verification;
a guard that skips when the source is missing would reproduce it exactly. If
the PDF cannot be found, or pdftotext is unavailable, this guard fails and
says why.

Sources live in seeds/, which is gitignored -- the articles are copyrighted and
must never enter a public repo. So this guard cannot run in CI, and is not
wired into the workflows. It is an operator gate: run it before a memo is sent.

    python3 scripts/check_sources.py
    python3 scripts/check_sources.py --context   # print match context too
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = os.path.join(REPO, "seeds")

# Minimum quoted-span length to check. Below this, quotation marks are mostly
# scare quotes and single terms of art, and the false-positive rate swamps the
# signal. 25 matches the one-pager guard in tests/test_one_pagers.py.
MIN_SPAN = 25

# memo path -> (source PDF basename, human name)
SOURCES: dict[str, tuple[str, str]] = {
    "lit-review/kim-memo.md": (
        "Kim_Protecting_Trade_Secrets_15_JMarshallRevIntellPropL_2016.pdf",
        "Kim, Protecting Trade Secrets under International Investment Law "
        "(15 J. Marshall Rev. Intell. Prop. L. 228, 2016)",
    ),
    "lit-review/ferguson-memo.md": (
        "Ferguson_Trade_Secrets_at_Risk_40_ArbIntl_337_2024.pdf",
        "Ferguson, Trade secrets at risk (40 Arb. Int'l 337, 2024)",
    ),
}

# Spans that quote something other than the memo's own source -- a case, a
# treaty, a second author, or the operator's own earlier wording being
# withdrawn. Each entry needs a reason, so the allowlist cannot quietly become
# a place to bury failures.
ALLOW: dict[str, str] = {
    "the bibliography is a raw input for the production of a finished product,":
        "ferguson-memo.md:65 -- quotes the AALL/law-review cite-checking "
        "standards in the methodological note, not Ferguson.",
    "trade secret as investment":
        "ferguson-memo.md:83 -- the project's own name for the pathway, used "
        "as a term of art in scare quotes. Not attributed to Ferguson.",
}


def _norm(s: str) -> str:
    """Collapse whitespace and normalise the quote characters PDFs mangle."""
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("‐", "-")
    return re.sub(r"\s+", " ", s).strip()


def _for_match(s: str) -> str:
    """Normalise a quoted span down to what can honestly be compared.

    Legal writing alters quotations in ways that are correct citation practice
    and would otherwise read as fabrication to a naive matcher:

      * Bluebook case alteration -- "[e]ven if it were so" for "Even if it
        were so". Brackets around a single letter are unwrapped.
      * Bracketed insertions and omissions -- "[the ICSID] Convention",
        "[...]". Dropped entirely.
      * Trailing punctuation carried inside the closing quote mark, which is
        US convention and is almost never in the source at that position.

    Matching is then case-insensitive, because the only case differences that
    survive this are sentence-initial capitals the alteration brackets exist
    to signal. Everything removed here is form. Nothing removed here is
    substance, so a span that still fails is a span the author did not write.
    """
    s = _norm(s)
    s = re.sub(r"\[(\w)\]", r"\1", s)      # [e]ven -> even
    s = re.sub(r"\s*\[[^\]]*\]\s*", " ", s)  # [the ICSID] / [...] -> gone
    s = s.strip(" ,.;:!?'\"-")
    return re.sub(r"\s+", " ", s).strip().lower()


def extract_pdf(pdf_path: str) -> str:
    """Extract text via pdftotext -layout. Raises on any failure."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as fh:
        out = fh.name
    try:
        subprocess.run(
            ["pdftotext", "-layout", pdf_path, out],
            check=True, capture_output=True,
        )
        with open(out, "r", encoding="utf-8", errors="replace") as fh:
            return _norm(fh.read())
    finally:
        if os.path.exists(out):
            os.unlink(out)


def quoted_spans(body: str) -> tuple[list[str], list[str]]:
    """Return (spans, structural warnings).

    Two lessons from 2026-08-06 are built in here.

    First, normalise the quote characters BEFORE pairing. The memos mix
    straight and curly quotes; if only the source is normalised, every curly
    quote in the memo is treated as content rather than as a delimiter and the
    pairing shifts for everything after it. The first version of this guard
    made exactly that mistake and reported 51 of 51 quotations missing, which
    is the signature of a broken parser rather than a broken memo.

    Second, pair WITHIN a paragraph, never across paragraphs. Sequential
    pairing over a whole file -- the approach in tests/test_one_pagers.py --
    lets a single unbalanced quote mark corrupt every span after it. Confining
    the pairing to one paragraph bounds that damage to the paragraph that
    caused it, and an odd count is reported as a structural warning so the
    operator fixes the source of the drift instead of chasing its symptoms.
    """
    spans: list[tuple[str, bool]] = []
    warnings: list[str] = []
    for n, para in enumerate(body.split("\n"), start=1):
        p = (para.replace("“", '"').replace("”", '"')
                  .replace("‘", "'").replace("’", "'"))
        marks = p.count('"')
        if marks % 2:
            warnings.append(
                f"  WARN     line {n}: odd number of quote marks; spans on "
                "this line are not checked")
            continue
        # With exactly one pair the span is certain. With two or more pairs the
        # pairing is a guess: the text between the close of one quotation and
        # the open of the next is indistinguishable, to a regex, from a
        # quotation. Those are reported as AMBIGUOUS rather than MISSING, so a
        # real failure on an unambiguous line is never buried under parser
        # noise. Getting this wrong is what made the first run of this guard
        # report 51 of 51 and mean nothing.
        certain = marks == 2
        spans.extend((m.group(1), certain)
                     for m in re.finditer(r'"([^"]{%d,})"' % MIN_SPAN, p))
    return spans, warnings


def check_memo(memo_rel: str, pdf_name: str, label: str,
               show_context: bool) -> tuple[int, int, list[str]]:
    """Return (checked, failed, messages) for one memo."""
    msgs: list[str] = []
    memo_path = os.path.join(REPO, memo_rel)
    pdf_path = os.path.join(SEEDS, pdf_name)

    if not os.path.exists(memo_path):
        return 0, 1, [f"FAIL {memo_rel}: memo not found"]

    # Fail closed. A missing source is the original defect, not an excuse.
    if not os.path.exists(pdf_path):
        return 0, 1, [
            f"FAIL {memo_rel}: declared source is missing",
            f"     expected: seeds/{pdf_name}",
            f"     source:   {label}",
            "     This guard fails rather than skips. An unverifiable memo is",
            "     exactly the state that produced the 2026-08-06 audit.",
        ]

    try:
        source_raw = extract_pdf(pdf_path)
        source = _for_match(source_raw)
    except FileNotFoundError:
        return 0, 1, [f"FAIL {memo_rel}: pdftotext not installed "
                      "(brew install poppler)"]
    except subprocess.CalledProcessError as exc:
        return 0, 1, [f"FAIL {memo_rel}: pdftotext failed: "
                      f"{exc.stderr.decode('utf-8', 'replace')[:200]}"]

    with open(memo_path, "r", encoding="utf-8") as fh:
        body = fh.read()

    checked = failed = 0
    spans, warnings = quoted_spans(body)
    msgs.extend(warnings)
    ambiguous = 0
    for span, certain in spans:
        norm = _for_match(span)
        if not norm or _norm(span) in ALLOW:
            continue
        idx = source.find(norm)
        if idx < 0 and not certain:
            ambiguous += 1
            continue
        checked += 1
        if idx < 0:
            failed += 1
            msgs.append(f"  MISSING  {memo_rel}")
            msgs.append(f"           {span[:150]}")
            msgs.append(f"           not found verbatim in {label}")
        elif show_context:
            lo, hi = max(0, idx - 110), idx + len(norm) + 110
            msgs.append(f"  ok       ...{source_raw[lo:hi]}...")
    if ambiguous:
        msgs.append(
            f"  note     {memo_rel}: {ambiguous} span(s) on multi-quote lines "
            "could not be paired unambiguously and were not judged")
    return checked, failed, msgs


def main(argv: list[str]) -> int:
    show_context = "--context" in argv
    total_checked = total_failed = 0
    all_msgs: list[str] = []

    for memo_rel, (pdf_name, label) in sorted(SOURCES.items()):
        checked, failed, msgs = check_memo(memo_rel, pdf_name, label,
                                            show_context)
        total_checked += checked
        total_failed += failed
        all_msgs.extend(msgs)
        if not msgs:
            all_msgs.append(f"  ok       {memo_rel}: {checked} quotations "
                            f"verified against source")

    print("check_sources: every quotation must exist in the source it names")
    print()
    for m in all_msgs:
        print(m)
    print()
    print(f"{total_checked} quotations checked, {total_failed} failed")

    if total_failed:
        print()
        print("A quotation that is not in the source is not a formatting")
        print("problem. It is the memo asserting something the author did")
        print("not write.")
        return 1

    print()
    print("NOTE: a passing run proves the strings are present. It does NOT")
    print("prove each is used for the proposition its source attaches it to.")
    print("On 2026-08-06 a phrase quoted for the wrong exclusion was found in")
    print("this repo -- the string was real and 26 lines away, governing")
    print("something else. Run with --context and read the surrounding")
    print("sentence before a memo goes out.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
