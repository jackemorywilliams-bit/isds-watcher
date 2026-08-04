#!/usr/bin/env python3
"""Historical backtest of the deterministic scorer, reported in three buckets.

This is a small, candid, *exploratory* backtest — not a comprehensive
validation. It assembles ~12-15 KNOWN cases entirely from text already in the
repository (nothing is fabricated) and scores each one with the *same*
deterministic keyword scorer the production pipeline uses
(``src.classify.keyword_score``), at the same digest threshold (40).

The audit lesson baked into this rewrite: a single blended confusion matrix
that folds the in-sample seed awards in with the out-of-sample holdout inflates
the headline. The seeds *trained* the lexicon, so recovering them proves only
that the fingerprint recognises what generated it — circular, not predictive.
So the cases are split into three clearly-labelled buckets, each reported
separately:

* **SEED RECOVERY** — the three development SEED cases only (Eli Lilly v.
  Canada, Philip Morris v. Australia, Bridgestone v. Panama). Their text is the
  verbatim doctrinal vocabulary extracted from each award and tagged to that
  seed in ``fingerprint.yaml`` — the same phrases that *define* the
  fingerprint. This bucket is strictly *in-sample*: it confirms the scorer
  recovers the cases it was built on, and is NOT predictive evidence. Its
  numbers never enter any headline.

* **OUT-OF-SAMPLE HOLDOUT** — the four holdout positives (Loewen, Mondev,
  Apotex, Philip Morris v. Uruguay) plus the clear off-theme NEGATIVES (real
  live listings — ICSID hearings, ITN headlines, OECD guidance, etc.), all
  pulled by id from ``scripts/holdout_set.json``. None of these were used in
  development, so this bucket is the headline generalisation metric:
  precision / recall / accuracy / F1 are computed on it *alone*. It keeps the
  candid Apotex miss. The corpus lists EVERY labelled holdout item, so this
  bucket and ``scripts/eval_holdout.py`` score the same set and must report the
  same numbers; ``scripts/check_claims.py`` makes a divergence fail the build.

* **LIVE PROSPECTIVE** — not numbers from this corpus. The honest prospective
  test is the live weekly digest archive, whose current status is reported in
  prose (see ``live_prospective`` below).

Holdout items are referenced by id rather than copied so the holdout stays the
single source of truth. The exclusion branches below are a guard against a
dangling id, NOT a curation rule: every labelled holdout item is listed in the
corpus and every one resolves, so nothing is excluded today. Until 2026-08-04
eight labelled negatives were simply absent from the corpus, and the smaller N
that produced was explained on the site by an exclusion that had never happened.
An id that stops resolving must be fixed, not tolerated — the exclusion prints a
line and the count check in ``scripts/check_claims.py`` fails the build.

Run standalone:   python scripts/backtest.py
As a library:     from scripts.backtest import run_backtest
"""

from __future__ import annotations

import datetime
import json
import sys
from dataclasses import asdict, dataclass, field
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
class SeedRecovery:
    """In-sample seed bucket. Confirms recovery, not generalisation.

    Reported as a simple recovered/total count, never as headline P/R/F1: the
    seeds defined the lexicon, so any precision/recall here would be circular.
    """
    cases: list[dict] = field(default_factory=list)
    recovered: int = 0          # seeds scoring >= THRESHOLD
    total: int = 0


@dataclass
class HoldoutMetrics:
    """Out-of-sample bucket: the headline generalisation metric."""
    cases: list[dict] = field(default_factory=list)
    tp: int = 0
    fp: int = 0
    fn: int = 0
    tn: int = 0
    total: int = 0
    n_pos: int = 0
    n_neg: int = 0
    precision: float = 1.0
    recall: float = 1.0
    accuracy: float = 0.0
    f1: float = 0.0
    false_positives: list[dict] = field(default_factory=list)
    false_negatives: list[dict] = field(default_factory=list)


@dataclass
class LiveProspective:
    """The true prospective test: the live weekly digest archive.

    Not derived from this corpus. Honest current status only.
    """
    status: str = ""            # one-line summary
    detail: str = ""            # short paragraph of candid framing


@dataclass
class BacktestResult:
    """Everything the build needs to render the three-bucket backtest page."""
    threshold: int
    seed: SeedRecovery
    holdout: HoldoutMetrics
    live: LiveProspective


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


def _make_case(cid: str, name: str, group: str, label: int, text: str,
               miss_reasons: dict) -> dict:
    """Score one case and tag any miss with a one-line reason."""
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
    return asdict(CaseResult(
        id=cid, name=name, group=group, label=label, score=score,
        band=_band_from_score(score), pred=pred, correct=correct,
        miss_kind=miss_kind, reason=reason,
    ))


def _build_seed(corpus: dict, miss_reasons: dict) -> SeedRecovery:
    """In-sample seed recovery bucket."""
    cases: list[dict] = []
    for s in corpus.get("seed_cases", []):
        cases.append(_make_case(
            s["id"], s["name"], "seed", int(s["label"]), s["text"], miss_reasons))
    # Highest score first — most legible for a reader scanning recovery.
    cases.sort(key=lambda c: (-c["score"], c["name"]))
    recovered = sum(1 for c in cases if c["pred"] == 1)
    return SeedRecovery(cases=cases, recovered=recovered, total=len(cases))


def _build_holdout(corpus: dict, holdout: dict, display: dict,
                   miss_reasons: dict) -> HoldoutMetrics:
    """Out-of-sample holdout bucket: the headline metric.

    Computes the confusion matrix and precision/recall/accuracy/F1 on the
    holdout positives + negatives ALONE — no seeds folded in.
    """
    cases: list[dict] = []

    for cid in corpus.get("holdout_positive_ids", []):
        it = holdout.get(cid)
        if not it or not it.get("text"):
            print(f"  ! holdout positive {cid!r} not found in holdout_set.json; excluding")
            continue
        cases.append(_make_case(
            cid, display.get(cid, cid), "holdout-positive", 1, it["text"], miss_reasons))

    for cid in corpus.get("holdout_negative_ids", []):
        it = holdout.get(cid)
        if not it or not it.get("text"):
            print(f"  ! holdout negative {cid!r} not found in holdout_set.json; excluding")
            continue
        cases.append(_make_case(
            cid, display.get(cid, cid), "holdout-negative", 0, it["text"], miss_reasons))

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

    # Display order: positives first, then negatives; within each, high score first.
    order = {"holdout-positive": 0, "holdout-negative": 1}
    cases.sort(key=lambda c: (order.get(c["group"], 9), -c["score"], c["name"]))

    false_positives = [c for c in cases if c["miss_kind"] == "false positive"]
    false_negatives = [c for c in cases if c["miss_kind"] == "false negative"]

    return HoldoutMetrics(
        cases=cases,
        tp=tp, fp=fp, fn=fn, tn=tn, total=total,
        n_pos=tp + fn, n_neg=tn + fp,
        precision=precision, recall=recall, accuracy=accuracy, f1=f1,
        false_positives=false_positives, false_negatives=false_negatives,
    )


def _build_live(corpus: dict) -> LiveProspective:
    """Live prospective status — prose, not corpus numbers."""
    lp = corpus.get("live_prospective", {})
    return LiveProspective(
        status=lp.get(
            "status",
            "Zero direct thematic matches to date."),
        detail=lp.get(
            "detail",
            "The live weekly digest archive is the true prospective test. To "
            "date it has produced no direct thematic hit; what it has shown is "
            "disciplined negative filtering and watch-list triage."),
    )


def run_backtest() -> BacktestResult:
    """Assemble, score and tabulate the three-bucket backtest.

    Pure / deterministic. The headline precision/recall/accuracy/F1 live on the
    ``holdout`` bucket alone; seed recovery is reported separately as in-sample.
    """
    corpus = _load_corpus()
    holdout = _load_holdout_by_id()
    display = corpus.get("display_names", {})
    miss_reasons = corpus.get("miss_reasons", {})

    return BacktestResult(
        threshold=THRESHOLD,
        seed=_build_seed(corpus, miss_reasons),
        holdout=_build_holdout(corpus, holdout, display, miss_reasons),
        live=_build_live(corpus),
    )


def main(argv=None) -> int:
    res = run_backtest()

    print("=== SEED RECOVERY (in-sample — confirms recovery, NOT predictive) ===")
    print(f"Seeds recovered: {res.seed.recovered}/{res.seed.total} "
          f"at threshold {res.threshold} (these numbers never enter a headline)")
    for c in res.seed.cases:
        mark = "ok" if c["pred"] == 1 else "X "
        print(f"  {mark} score={c['score']:>3} band={c['band']:<6}  {c['name']}")

    h = res.holdout
    print("\n=== OUT-OF-SAMPLE HOLDOUT (the headline generalisation metric) ===")
    print(f"Holdout: {h.total} cases ({h.n_pos} on-theme, {h.n_neg} off-theme) | "
          f"threshold = {res.threshold}")
    for c in h.cases:
        mark = "ok" if c["correct"] else "X "
        print(f"  {mark} label={c['label']} score={c['score']:>3} "
              f"band={c['band']:<6} [{c['group']}]  {c['name']}")
    print(f"\nConfusion: TP={h.tp} FP={h.fp} FN={h.fn} TN={h.tn}")
    print(f"Precision={h.precision:.2f}  Recall={h.recall:.2f}  "
          f"Accuracy={h.accuracy:.2f}  F1={h.f1:.2f}")
    if h.false_negatives:
        print("\nFalse negatives:")
        for c in h.false_negatives:
            print(f"  - {c['name']} (score {c['score']}): {c['reason']}")
    if h.false_positives:
        print("\nFalse positives:")
        for c in h.false_positives:
            print(f"  - {c['name']} (score {c['score']}): {c['reason']}")
    if not h.false_negatives and not h.false_positives:
        print("\nNo misses on the holdout bucket.")

    print("\n=== LIVE PROSPECTIVE (the true prospective test — not corpus numbers) ===")
    print(res.live.status)
    print(res.live.detail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
