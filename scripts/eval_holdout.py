"""Out-of-sample validation harness for the ISDS Thematic Watcher.

Loads a labelled holdout (scripts/holdout_set.json) of items NOT used in
development, scores each with the deterministic keyword scorer, and reports the
confusion matrix and precision/recall/accuracy at the digest threshold (40).
Run: python scripts/eval_holdout.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime
from src.classify import keyword_score
from src.sources.base import CandidateItem

THRESHOLD = 40


def main():
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

    print(f"Holdout: {len(hs['items'])} items "
          f"({tp+fn} on-theme, {tn+fp} off-theme) | threshold = {THRESHOLD}")
    for cid, lab, score, pred in rows:
        mark = "ok" if lab == pred else "X "
        print(f"  {mark} label={lab} score={score:>3} pred={pred}  {cid}")
    print(f"\nConfusion: TP={tp} FP={fp} TN={tn} FN={fn}")
    print(f"Precision={prec:.2f}  Recall={rec:.2f}  Accuracy={acc:.2f}  F1={f1:.2f}")
    return prec, rec, acc, f1


if __name__ == "__main__":
    main()
