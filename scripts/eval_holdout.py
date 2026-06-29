"""Out-of-sample validation harness for the ISDS Thematic Watcher.

Loads a labelled holdout (scripts/holdout_set.json) of items NOT used in
development, scores each with the deterministic keyword scorer, and reports the
confusion matrix and precision/recall/accuracy at the digest threshold (40).

As a CI gate it can also FAIL (nonzero exit) when precision or recall fall below
a floor, so a scorer change that regresses classification quality breaks the
build instead of silently shipping. The defaults are conservative — set well
below the current scores (precision 1.00, recall 0.75) so normal variation
passes but a real regression trips the gate.

Run:        python scripts/eval_holdout.py
CI gate:    python scripts/eval_holdout.py --fail-under-precision 0.9 --fail-under-recall 0.6
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
from src.classify import keyword_score
from src.sources.base import CandidateItem

THRESHOLD = 40

# Conservative CI floors. The holdout currently scores precision 1.00 / recall
# 0.75; these floors sit below that so ordinary churn passes but a genuine
# regression (e.g. a missed on-theme item or a new false positive) fails the
# build. Tighten them as the holdout and scorer mature.
DEFAULT_FAIL_UNDER_PRECISION = 0.90
DEFAULT_FAIL_UNDER_RECALL = 0.60


def evaluate():
    """Score the holdout and return (precision, recall, accuracy, f1, rows, counts)."""
    hs = json.load(open(os.path.join(os.path.dirname(__file__), "holdout_set.json")))
    now = datetime.datetime.now(datetime.timezone.utc)
    tp = fp = tn = fn = 0
    rows = []
    for it in hs["items"]:
        ci = CandidateItem("holdout", it["id"], "u", it["text"][:80], now,
                           it["text"], it["text"], {})
        score = keyword_score(ci)["relevance_score"]
        pred = 1 if score >= THRESHOLD else 0
        lab = it["label"]
        tp += pred == 1 and lab == 1
        fp += pred == 1 and lab == 0
        tn += pred == 0 and lab == 0
        fn += pred == 0 and lab == 1
        rows.append((it["id"][:34], lab, score, pred))

    prec = tp / (tp + fp) if (tp + fp) else 1.0
    rec = tp / (tp + fn) if (tp + fn) else 1.0
    acc = (tp + tn) / len(hs["items"])
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return prec, rec, acc, f1, rows, (tp, fp, tn, fn, len(hs["items"]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fail-under-precision", type=float,
                    default=DEFAULT_FAIL_UNDER_PRECISION,
                    help="fail (exit 1) if precision is below this floor")
    ap.add_argument("--fail-under-recall", type=float,
                    default=DEFAULT_FAIL_UNDER_RECALL,
                    help="fail (exit 1) if recall is below this floor")
    ap.add_argument("--no-gate", action="store_true",
                    help="report only; never fail on the floors (exit 0)")
    args = ap.parse_args(argv)

    prec, rec, acc, f1, rows, (tp, fp, tn, fn, n) = evaluate()

    print(f"Holdout: {n} items "
          f"({tp+fn} on-theme, {tn+fp} off-theme) | threshold = {THRESHOLD}")
    for cid, lab, score, pred in rows:
        mark = "ok" if lab == pred else "X "
        print(f"  {mark} label={lab} score={score:>3} pred={pred}  {cid}")
    print(f"\nConfusion: TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"Precision={prec:.2f}  Recall={rec:.2f}  Accuracy={acc:.2f}  F1={f1:.2f}")

    if args.no_gate:
        return 0

    failures = []
    if prec < args.fail_under_precision:
        failures.append(f"precision {prec:.2f} < floor {args.fail_under_precision:.2f}")
    if rec < args.fail_under_recall:
        failures.append(f"recall {rec:.2f} < floor {args.fail_under_recall:.2f}")
    if failures:
        print("\nGATE FAILED — " + "; ".join(failures))
        return 1
    print(f"\nGATE PASSED — precision floor {args.fail_under_precision:.2f}, "
          f"recall floor {args.fail_under_recall:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
