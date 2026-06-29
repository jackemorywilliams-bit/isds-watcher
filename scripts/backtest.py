#!/usr/bin/env python3
"""Historical backtest of the deterministic scorer on a focused labelled set.

This is a small, candid, *exploratory* backtest — not a comprehensive
validation. It assembles ~12-15 KNOWN cases entirely from text already in the
repository (nothing is fabricated) and scores each one with the *same*
deterministic keyword scorer the production pipeline uses
(``src.classify.keyword_score``), at the same digest threshold (40). From the
predictions it computes a confusion matrix (TP / FP / FN / TN), precision,
recall, accuracy and F1, and the explicit lists of false positives and false
negatives with a one-line reason for each miss.

The labelled corpus (``scripts/backtest_corpus.json``) is three groups:

* the three development SEED cases (Eli Lilly v. Canada, Philip Morris v.
  Australia, Bridgestone v. Panama). Their text is the verbatim doctrinal
  vocabulary extracted from each award and tagged to that seed in
  ``fingerprint.yaml`` — the same phrases that *define* the fingerprint;
* four OUT-OF-SAMPLE holdout positives (Loewen, Mondev, Apotex, Philip Morris
  v. Uruguay), pulled by id from ``scripts/holdout_set.json``;
* clear off-theme NEGATIVES, also pulled by id from the holdout file (real
  live listings — ICSID hearings, ITN headlines, OECD guidance, etc.).

Because the seeds are *in-sample* (they trained the lexicon) and the holdout
positives/negatives are *out-of-sample*, the set deliberately mixes both: it
shows the scorer recovers the cases it was built on AND generalises to known
out-of-sample ones — while honestly surfacing where it misses (Apotex).

Run standalone:   python scripts/backtest.py
As a library:     from scripts.backtest import run_backtest
"""

from __future__ import annotations

import datetime
import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Allow ``python scripts/backtest.py`` from anywhere (repo root on sys.path).
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.classify import keyword_score  # noqa: E402
from src.sources.base import CandidateItem  # noqa: E402

THRESHOLD = 40

_CORPUS_PATH = Path(__file__).resolve().parent / "backtest_corpus.json"
_HOLDOUT_PATH = Path(__file__).resolve().parent / "holdout_set.json"


def _band_from_score(score: int) -> str:
    """Same band cut-offs the site uses (HIGH >=70, MEDIUM >=40, else LOW)."""
    if score >= 70:
        return "HIGH"
    if score >= THRESHOLD:
        return "MEDIUM"
    return "LOW"


@dataclass
class CaseResult:
    """One scored case in the backtest."""
    id: str
    name: str
    group: str          # "seed" | "holdout-positive" | "holdout-negative"
    label: int          # 1 = on-theme, 0 = off-theme
    score: int
    band: str           # predicted band (HIGH/MEDIUM/LOW)
    pred: int           # 1 if score >= THRESHOLD else 0
    correct: bool
    miss_kind: str      # "" | "false positive" | "false negative"
    reason: str         # one-line reason for a miss (empty when correct)


@dataclass
class BacktestResult:
    """Everything the build needs to render the backtest page."""
    threshold: int
    cases: list[dict]           # [CaseResult as dict], ordered for display
    tp: int
    fp: int
    fn: int
    tn: int
    total: int
    n_pos: int
    n_neg: int
    precision: float
    recall: float
    accuracy: float
    f1: float
    false_positives: list[dict]  # subset of cases (misses)
    false_negatives: list[dict]  # subset of cases (misses)


def _load_corpus() -> dict:
    return json.loads(_CORPUS_PATH.read_text(encoding="utf-8"))


def _load_holdout_by_id() -> dict:
    hs = json.loads(_HOLDOUT_PATH.read_text(encoding="utf-8"))
    return {it["id"]: it for it in hs["items"]}


def _score_text(case_id: str, text: str) -> int:
    """Score a single text with the production deterministic scorer."""
    now = datetime.datetime.now(datetime.timezone.utc)
    ci = CandidateItem("backtest", case_id, "u", text[:80], now, text, text, {})
    return int(keyword_score(ci)["relevance_score"])


def _assemble_cases() -> list[dict]:
    """Build the focused labelled set from in-repo text only.

    Seeds carry their text inline (verbatim seed-tagged phrases from
    fingerprint.yaml); holdout items are looked up by id in holdout_set.json.
    Any case whose text cannot be resolved in-repo is *excluded*, never faked.
    """
    corpus = _load_corpus()
    holdout = _load_holdout_by_id()
    display = corpus.get("display_names", {})
    miss_reasons = corpus.get("miss_reasons", {})

    raw: list[tuple[str, str, str, int, str]] = []  # (id, name, group, label, text)

    for s in corpus.get("seed_cases", []):
        raw.append((s["id"], s["name"], "seed", int(s["label"]), s["text"]))

    for cid in corpus.get("holdout_positive_ids", []):
        it = holdout.get(cid)
        if not it or not it.get("text"):
            print(f"  ! holdout positive {cid!r} not found in holdout_set.json; excluding")
            continue
        raw.append((cid, display.get(cid, cid), "holdout-positive", 1, it["text"]))

    for cid in corpus.get("holdout_negative_ids", []):
        it = holdout.get(cid)
        if not it or not it.get("text"):
            print(f"  ! holdout negative {cid!r} not found in holdout_set.json; excluding")
            continue
        raw.append((cid, display.get(cid, cid), "holdout-negative", 0, it["text"]))

    cases: list[dict] = []
    for cid, name, group, label, text in raw:
        score = _score_text(cid, text)
        pred = 1 if score >= THRESHOLD else 0
        correct = pred == label
        miss_kind = ""
        reason = ""
        if not correct:
            if pred == 1 and label == 0:
                miss_kind = "false positive"
                reason = miss_reasons.get(
                    cid, "Off-theme listing scored at or above threshold.")
            else:
                miss_kind = "false negative"
                reason = miss_reasons.get(
                    cid, "On-theme case scored below threshold.")
        cases.append(asdict(CaseResult(
            id=cid, name=name, group=group, label=label, score=score,
            band=_band_from_score(score), pred=pred, correct=correct,
            miss_kind=miss_kind, reason=reason,
        )))
    return cases


def run_backtest() -> BacktestResult:
    """Assemble, score and tabulate the focused backtest. Pure / deterministic."""
    cases = _assemble_cases()

    tp = sum(1 for c in cases if c["label"] == 1 and c["pred"] == 1)
    fp = sum(1 for c in cases if c["label"] == 0 and c["pred"] == 1)
    fn = sum(1 for c in cases if c["label"] == 1 and c["pred"] == 0)
    tn = sum(1 for c in cases if c["label"] == 0 and c["pred"] == 0)
    total = len(cases)

    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 1.0
    accuracy = (tp + tn) / total if total else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) else 0.0)

    # Display order: positives first (seeds, then holdout positives), then
    # negatives — most legible for a reader scanning the per-case table.
    order = {"seed": 0, "holdout-positive": 1, "holdout-negative": 2}
    cases.sort(key=lambda c: (order.get(c["group"], 9), -c["score"], c["name"]))

    false_positives = [c for c in cases if c["miss_kind"] == "false positive"]
    false_negatives = [c for c in cases if c["miss_kind"] == "false negative"]

    return BacktestResult(
        threshold=THRESHOLD,
        cases=cases,
        tp=tp, fp=fp, fn=fn, tn=tn, total=total,
        n_pos=tp + fn, n_neg=tn + fp,
        precision=precision, recall=recall, accuracy=accuracy, f1=f1,
        false_positives=false_positives,
        false_negatives=false_negatives,
    )


def main(argv=None) -> int:
    res = run_backtest()
    print(f"Backtest: {res.total} known cases "
          f"({res.n_pos} on-theme, {res.n_neg} off-theme) | "
          f"threshold = {res.threshold}")
    for c in res.cases:
        mark = "ok" if c["correct"] else "X "
        print(f"  {mark} label={c['label']} score={c['score']:>3} "
              f"band={c['band']:<6} [{c['group']}]  {c['name']}")
    print(f"\nConfusion: TP={res.tp} FP={res.fp} FN={res.fn} TN={res.tn}")
    print(f"Precision={res.precision:.2f}  Recall={res.recall:.2f}  "
          f"Accuracy={res.accuracy:.2f}  F1={res.f1:.2f}")
    if res.false_negatives:
        print("\nFalse negatives:")
        for c in res.false_negatives:
            print(f"  - {c['name']} (score {c['score']}): {c['reason']}")
    if res.false_positives:
        print("\nFalse positives:")
        for c in res.false_positives:
            print(f"  - {c['name']} (score {c['score']}): {c['reason']}")
    if not res.false_negatives and not res.false_positives:
        print("\nNo misses on this focused set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
