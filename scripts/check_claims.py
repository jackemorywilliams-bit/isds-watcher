#!/usr/bin/env python3
"""Cross-check the numbers this project states about itself.

WHY THIS EXISTS. This is the third guard of one shape. `scripts/check_models.py` puts
the principle plainly: two records of one fact that disagree mean at least one is
wrong. It found five cards naming a retired model. `scripts/check_marks.py` made the
Carrying-Span Rule countable. Both exist because a person caught the drift by reading
carefully, and reading carefully does not scale to every number in a public repo.

The numbers here are the SELF-DESCRIPTIVE ones — the constants the scorer runs on and
the measurements the methodology reports. They are written down in more than one place
by construction: a constant in `src/`, a line of YAML, a sentence of prose for
Dr. Benavides, a generated analytics file. Nothing compared them, and on 2026-08-04
three had drifted:

  * `scripts/backtest_corpus.json` listed 8 of the 16 labelled negatives, so the site
    reported the holdout as 12 cases at accuracy 0.92 while `scripts/eval_holdout.py`
    scored all 20 at 0.95 — and the page explained its smaller N with an exclusion
    rule that was not the operative rule.
  * `fingerprint.yaml`'s `combination_rules` described a "subtotal >= 30" bar that
    exists nowhere in `src/classify.py`, whose real constants are 12 and 18.
  * All seven `expected_score` values in `fingerprint.yaml` were wrong, under a test
    that asserted only the band.

WHAT IT CHECKS. A DECLARED registry, below: each fact names exactly ONE authority and
the places that restate it. Every restatement must equal its authority. That is all.

WHAT IT DELIBERATELY IS NOT. It does no NLP, reads no prose it was not pointed at, and
makes no attempt at completeness. A guard that tried to catch every claim would need
to understand English, and would become the unreviewable thing it was built to
prevent. It checks fourteen facts because fourteen were worth the coupling; a
fifteenth is a decision, not a default.

TWO CONSEQUENCES OF FAILING CLOSED, both intended:

  * A declared pattern that matches NOTHING is a FAILURE, not a skip. Prose gets
    rewritten; when the sentence this registry points at is gone, the registry entry
    must be re-pointed by a person, not silently satisfied by an empty search. That is
    the tool-status-as-source-state pattern `check_marks.py` records.
  * A number written in words must be in `_WORDS`. An unrecognised word fails rather
    than passing unread.

The registry holds PRESENT-TENSE claims only. "The first completed review cycle" is a
dated historical statement, true when written and not drift when superseded, so it is
not a mirror.

WHAT IT CANNOT DO. It cannot tell you a number is RIGHT — only that the project's
several statements of it agree, and that the ones derived from code or data are
derived from the code and data that are actually here. Choosing the threshold, and
judging whether a holdout of twenty items supports what the memo says it supports, are
Emory's.

CLI:
    python scripts/check_claims.py

Exit 0 clean, 1 on any disagreement, 2 if an input cannot be read.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Allow ``python scripts/check_claims.py`` from anywhere: the harness readings import
# ``scripts.eval_holdout`` and ``scripts.backtest`` as modules, which needs the repo
# root on the path, not scripts/.
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

# The number-words this project actually writes. An unlisted word is a failure, not a
# skip: "a floor of a dozen" must break the build rather than quietly stop being read.
_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "twenty-five": 25, "thirty": 30,
    "forty": 40, "fifty": 50, "sixty": 60,
}


class Unreadable(Exception):
    """An input could not be read or parsed at all — exit 2, never a silent pass."""


@dataclass(frozen=True)
class Ref:
    """One place a fact is written down.

    ``mode``:
      ``regex``     — every match of ``pattern`` in ``path`` is a reading. Group 1
                      holds the value, unless ``asserts`` is set, in which case the
                      match's mere presence asserts that value.
      ``count``     — the NUMBER of matches of ``pattern`` in ``path`` is the value.
      ``files``     — the number of files matching the glob ``path`` is the value.
      ``harness``   — the value comes from running a harness; ``pattern`` names the
                      metric (see ``_HARNESS``).
    """
    path: str
    pattern: str = ""
    mode: str = "regex"
    asserts: float | None = None
    note: str = ""


@dataclass(frozen=True)
class Fact:
    """One self-descriptive number, its single authority, and every restatement."""
    name: str
    authority: Ref
    mirrors: tuple[Ref, ...] = field(default_factory=tuple)


# --------------------------------------------------------------------------- #
# Harness readings — measurements, not literals
# --------------------------------------------------------------------------- #
def _holdout_metrics() -> dict[str, float]:
    """What ``scripts/eval_holdout.py`` reports, computed the way it computes it."""
    from scripts.eval_holdout import evaluate
    prec, rec, acc, f1, _rows, (tp, fp, tn, fn, n) = evaluate()
    return {"n": n, "n_pos": tp + fn, "n_neg": tn + fp,
            "precision": prec, "recall": rec, "accuracy": acc, "f1": f1}


def _backtest_metrics() -> dict[str, float]:
    """What the backtest page's holdout bucket reports."""
    from scripts.backtest import run_backtest
    h = run_backtest().holdout
    return {"n": h.total, "n_pos": h.n_pos, "n_neg": h.n_neg,
            "precision": h.precision, "recall": h.recall,
            "accuracy": h.accuracy, "f1": h.f1}


_HARNESS = {
    "scripts/eval_holdout.py": _holdout_metrics,
    "scripts/backtest.py": _backtest_metrics,
}


# --------------------------------------------------------------------------- #
# THE REGISTRY — fourteen facts. Each names exactly one authority.
# --------------------------------------------------------------------------- #
_METHODOLOGY = "METHODOLOGY.md"
_FINGERPRINT = "fingerprint.yaml"
_CLASSIFY = "src/classify.py"
_CONFIG = "src/config.py"
_EVAL = "scripts/eval_holdout.py"
_BACKTEST = "scripts/backtest.py"

REGISTRY: tuple[Fact, ...] = (
    # --- the scorer's own constants ---------------------------------------- #
    Fact(
        "present floor (the subtotal at which a ring counts as matched)",
        Ref(_CLASSIFY, r"(?m)^PRESENT_FLOOR = (\d+)"),
        (Ref(_FINGERPRINT, r"(?:present floor \(|floor of |PRESENT_FLOOR = )(\d+)"),
         Ref(_METHODOLOGY, r"lexical subtotal reaches a floor of ([a-z]+)")),
    ),
    Fact(
        "strong single-ring subtotal",
        Ref(_CLASSIFY, r"(?m)^STRONG_SUBTOTAL = (\d+)"),
        (Ref(_FINGERPRINT,
             r"(?:strong-single-ring floor \(|STRONG_SUBTOTAL = |below )(\d+)"),),
    ),
    # --- the digest gate ---------------------------------------------------- #
    Fact(
        "digest threshold",
        Ref(_FINGERPRINT, r"(?m)^threshold: (\d+)"),
        (Ref(_CONFIG, r"(?m)^_DEFAULT_THRESHOLD = (\d+)",
             note="the fallback used when fingerprint.yaml cannot be read; a fallback "
                  "that differs from the authority silently scores a run at a value "
                  "the project abandoned"),
         Ref(_EVAL, r"(?m)(?:^THRESHOLD = |digest threshold \()(\d+)"),
         Ref(_BACKTEST, r"(?m)(?:^THRESHOLD = |digest threshold \()(\d+)"),
         Ref(_METHODOLOGY, r"digest threshold of ([a-z]+)"),
         Ref(_METHODOLOGY, r"item scoring ([a-z]+) or higher")),
    ),
    Fact(
        "relevance floor (the lowest score a watch-list lead may carry)",
        Ref(_CONFIG, r"(?m)^RELEVANCE_FLOOR = (\d+)"),
        (Ref(_CONFIG, r"floor at (\d+)"),
         Ref(_METHODOLOGY, r"scoring below ([a-z-]+) will ever be presented")),
    ),
    Fact(
        "minimum digest items",
        Ref(_CONFIG, r"(?m)^MIN_DIGEST_ITEMS = (\d+)"),
        (Ref(_METHODOLOGY, r"fewer than ([a-z]+) matches"),
         Ref(_METHODOLOGY, r"filled toward ([a-z]+) with")),
    ),
    # --- the holdout, measured ---------------------------------------------- #
    # The authority is the harness OUTPUT, not any number written down. The backtest
    # mirror is the one that would have caught 2026-08-04: it scores the corpus, so a
    # corpus that stops listing every labelled item shrinks this reading and fails.
    Fact(
        "holdout items",
        Ref(_EVAL, "n", mode="harness"),
        (Ref(_BACKTEST, "n", mode="harness"),
         Ref(_METHODOLOGY, r"holdout of ([a-z]+) items"),
         Ref(_METHODOLOGY, r"[—-] ([a-z]+) items, only")),
    ),
    Fact(
        "holdout on-theme positives",
        Ref(_EVAL, "n_pos", mode="harness"),
        (Ref(_BACKTEST, "n_pos", mode="harness"),
         Ref(_METHODOLOGY, r"([A-Za-z]+) of the twenty were on-theme positives"),
         Ref(_METHODOLOGY, r"items, only ([a-z]+) positives")),
    ),
    Fact(
        "holdout off-theme negatives",
        Ref(_EVAL, "n_neg", mode="harness"),
        (Ref(_BACKTEST, "n_neg", mode="harness"),
         Ref(_METHODOLOGY, r"compared against ([a-z]+) other awards")),
    ),
    Fact(
        "holdout precision",
        Ref(_EVAL, "precision", mode="harness"),
        (Ref(_BACKTEST, "precision", mode="harness"),
         Ref(_METHODOLOGY, r"precision of ([0-9.]+)")),
    ),
    Fact(
        "holdout recall",
        Ref(_EVAL, "recall", mode="harness"),
        (Ref(_BACKTEST, "recall", mode="harness"),
         Ref(_METHODOLOGY, r"recall of ([0-9.]+)")),
    ),
    Fact(
        "holdout accuracy",
        Ref(_EVAL, "accuracy", mode="harness"),
        (Ref(_BACKTEST, "accuracy", mode="harness"),
         Ref(_METHODOLOGY, r"accuracy of ([0-9.]+)")),
    ),
    Fact(
        "holdout F1",
        Ref(_EVAL, "f1", mode="harness"),
        (Ref(_BACKTEST, "f1", mode="harness"),
         Ref(_METHODOLOGY, r"F1 of ([0-9.]+)")),
    ),
    # --- the record of what has actually been run and reviewed --------------- #
    Fact(
        "archived runs",
        Ref("digests/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].html", mode="files"),
        (Ref("analytics/source-receptivity.md",
             r"Across \*\*(\d+)\*\* archived run"),),
    ),
    Fact(
        "completed human-review cycles",
        Ref("HUMAN_REVIEW.md", r"(?m)^###[^\n]*\bCOMPLETED\b", mode="count"),
        (Ref("HUMAN_REVIEW.md", r"_No human review has been logged yet", asserts=0,
             note="the log's own standing statement, which stops being true the "
                  "moment a cycle is marked COMPLETED"),),
    ),
)


# --------------------------------------------------------------------------- #
# Reading a reference
# --------------------------------------------------------------------------- #
def _number(raw: str, where: str) -> float:
    """A captured value as a number. Digits, or a word from ``_WORDS``."""
    token = raw.strip().lower()
    try:
        return float(token)
    except ValueError:
        pass
    if token in _WORDS:
        return float(_WORDS[token])
    raise Unreadable(f"{where}: cannot read \"{raw}\" as a number — add it to _WORDS "
                     "if it is a number this project writes in words")


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _read(ref: Ref, repo: Path) -> list[tuple[float, str]]:
    """Every ``(value, "file:line")`` reading this reference yields."""
    if ref.mode == "files":
        n = len(list(repo.glob(ref.path)))
        return [(float(n), f"{ref.path} ({n} matching files)")]

    if ref.mode == "harness":
        fn = _HARNESS.get(ref.path)
        if fn is None:
            raise Unreadable(f"{ref.path}: no harness registered")
        try:
            metrics = fn()
        except Exception as exc:  # noqa: BLE001 — a harness that will not run is an
            # unreadable input, not a clean check
            raise Unreadable(f"{ref.path}: harness would not run: "
                             f"{type(exc).__name__}: {exc}") from exc
        if ref.pattern not in metrics:
            raise Unreadable(f"{ref.path}: harness reports no metric "
                             f"{ref.pattern!r}")
        return [(float(metrics[ref.pattern]), f"{ref.path} ({ref.pattern}, measured)")]

    path = repo / ref.path
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Unreadable(f"{ref.path}: cannot read: {exc}") from exc

    matches = list(re.finditer(ref.pattern, text))

    if ref.mode == "count":
        first = f":{_line_of(text, matches[0].start())}" if matches else ""
        return [(float(len(matches)), f"{ref.path}{first} ({len(matches)} matching)")]

    out: list[tuple[float, str]] = []
    for m in matches:
        where = f"{ref.path}:{_line_of(text, m.start())}"
        if ref.asserts is not None:
            out.append((float(ref.asserts), where))
        else:
            out.append((_number(m.group(1), where), where))
    return out


def _same(a: float, b: float) -> bool:
    """Equal at the precision the project publishes (two decimals)."""
    return round(a, 2) == round(b, 2)


def _fmt(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:.2f}"


# --------------------------------------------------------------------------- #
# The check
# --------------------------------------------------------------------------- #
def check(registry: tuple[Fact, ...] | None = None,
          repo: Path | None = None) -> list[str]:
    """Every disagreement, as a list of human-readable problems.

    Raises ``Unreadable`` when an input cannot be read at all — a checker that reports
    clean because it could not open its inputs is worse than no checker. Both
    arguments resolve at CALL time so a test can point the whole check at a miniature
    repository.
    """
    registry = REGISTRY if registry is None else registry
    repo = REPO if repo is None else repo
    problems: list[str] = []

    for fact in registry:
        auth = _read(fact.authority, repo)
        if not auth:
            problems.append(
                f"{fact.name}: the authority {fact.authority.path} no longer states "
                "it — the registry entry points at nothing and must be re-pointed")
            continue
        # An authority that contradicts itself has no single value to compare against.
        base, base_where = auth[0]
        for value, where in auth[1:]:
            if not _same(value, base):
                problems.append(
                    f"{fact.name}: the authority disagrees with itself — "
                    f"{base_where} says {_fmt(base)}, {where} says {_fmt(value)}")

        for mirror in fact.mirrors:
            readings = _read(mirror, repo)
            if not readings:
                problems.append(
                    f"{fact.name}: nothing in {mirror.path} matches the declared "
                    "pattern — the claim was rewritten or removed, and the registry "
                    "must be re-pointed by a person rather than pass on an empty "
                    "search")
                continue
            for value, where in readings:
                if _same(value, base):
                    continue
                tail = f" ({mirror.note})" if mirror.note else ""
                problems.append(
                    f"{fact.name}: {base_where} says {_fmt(base)}, "
                    f"{where} says {_fmt(value)}{tail}")

    return problems


def main(argv: list[str]) -> int:
    try:
        problems = check()
    except Unreadable as exc:
        print(f"cannot run the claims check: {exc}", file=sys.stderr)
        return 2

    mirrors = sum(len(f.mirrors) for f in REGISTRY)
    print(f"Checked {len(REGISTRY)} self-descriptive facts against {mirrors} declared "
          "restatements.")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print("\nA number this project states about itself is written down in more than "
              "one place.\nThey must agree, and the authority named in "
              "scripts/check_claims.py is the one that decides.", file=sys.stderr)
        return 1
    print("  ok — every restatement equals its authority.")
    print("\nThis establishes AGREEMENT only. That a number is correct, and that the "
          "holdout it\ncomes from supports what the methodology says it supports, are "
          "not checked here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
