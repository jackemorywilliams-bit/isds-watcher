# Locked validation set — schema and lock procedure (no items yet, by design)

This directory will hold the 54-item, 9-category production-path validation set
specified in the R2.1 record. **It is created empty of items on purpose.** The
named candidate matters in that record are leads drawn from this repository's
own corpus; several docket numbers and dates are unverified against primary
sources, and per the carrying-span rule **no item enters this set on a memo's
authority**. Primary retrieval is a library task and is recorded as externally
gated in `RETRIEVAL_LEDGER.md`. Building the set from memory would contaminate
the only clean validation instrument this project will get.

## Files, and the commit order that proves blindness

| Step | File | Rule |
|---|---|---|
| 1 | `items.json` | Item content only — the schema **contains no label fields**. Committed first. |
| 2 | `LOCK.md` | SHA-256 of `items.json` + the commit SHA recording it. |
| 3 | `labels.json` | Labels keyed by item id, in a separate file. No score field exists; no scorer is run before this commit. |
| 4 | `LOCK.md` (append) | SHA-256 of `labels.json` + its commit SHA. |
| 5 | — | Only now may any scorer touch the set. Git history is the evidence that labels preceded scores. |

A proposed `scripts/check_lock.py` recomputes both hashes and fails closed if
either file changed after its lock entry.

## `items.json` — one object per item

```json
{
  "id": "cat1-01",
  "category": 1,
  "tier": "P",
  "source_url": "…",
  "document_title": "…",
  "document_date": "…",
  "pinpoint": "…",
  "text": "…",
  "access_status": "full | partial | paywalled | blocked",
  "rationale_authority": "optional Ferguson/Kim pointer — never article text"
}
```

Tier rules (the copyright constraint is hard: `seeds/` is gitignored because a
commit is publication):

- **P (public primary)** — ICSID, PCA, italaw, Curia, BAILII, UN RIAA, WTO.
  `text` is a verbatim excerpt **capped at 600 characters**, selected **by
  position, never by content**: the first 600 characters of the body as
  `src/enrich.py::_extract_body` would extract it, after the caption block. A
  coder who picks the passage picks the passage that scores; position selection
  is the anti-contamination rule that matters most.
- **S (paywalled/headline-only)** — `text` is the headline only. That is
  fidelity, not degradation: `raw_text=title` is what production sees.
- **C (copyrighted secondary — Ferguson, Kim)** — never item text; labelling
  authority only, read locally from `seeds/`.

## `labels.json` — one object per item id

```json
{
  "id": "cat1-01",
  "L_theme": 0,
  "L_theme_reason": "one sentence naming which rings are present and absent",
  "L_band": "LOW | MEDIUM | HIGH",
  "L_band_clause": "the prompts/classifier.txt clause relied on"
}
```

`L_theme` (reaches the three-ring research question) and `L_band` (what the
operator's own scoring grammar assigns) are recorded independently and **never
reconciled** — the gap between them is a measurement. Single coder, permanently
disclosed; no inter-rater statistic is computed, reported, or proposed.

## The nine categories (6 items each; 20 positives total)

1. IP + ISDS + administrative state measure
2. IP + ISDS with a negative investment/jurisdiction holding
3. IP dispute, no investment-treaty claim
4. ISDS administrative-measure claim, no IP
5. Domestic trade-secret litigation, no state/treaty nexus
6. Court enforcement / set-aside that is not a denial-of-justice claim
7. Jurisdiction/admissibility decision, no IP
8. Headline-only / paywalled candidates
9. Paraphrase-heavy trade-secret / clinical-data / regulatory-data reporting

Candidate matters per category are listed in the R2.1 record; each is a lead
until its primary document is retrieved with a pinpoint and logged in
`RETRIEVAL_LEDGER.md`. Disjointness is at the level of the **matter**, not the
document: no case in the development set (the retired 20-item holdout, the 14
frozen probes, the 13 published items) may appear here in any form.

## Evaluation (once locked): production path, not `keyword_score`

Replay through `src/main.py` steps 2–4 as production runs them; the reported
decision is **surfaced / not surfaced**. Batch-shape to the observed run-size
distribution (78, 79, 14, 80, 11, 12, 13, 23, 14, 10, 13; median 14) under a
recorded seed; run the same item in a 10-item and an 80-item batch and report
any publication-status difference as a first-class finding. Metrics:
publication precision and recall with exact Clopper-Pearson intervals,
floor-band composition on [25, 40), threshold-band count, grammar fidelity
(band vs `L_band`), always per-category. Stability: 20 items × 10 runs;
blocking thresholds per the R2.1 record (decision flip > 0.10, mean score range
> 10, any range > 20, silent-fallback rate > 0.05). Acceptance V1–V6 and
stop-publication S1–S4 per the R2.1 record; S4 (zero positives reach 40 on the
production path) is the current state of the system and the reason the
fill-floor is suspended.
