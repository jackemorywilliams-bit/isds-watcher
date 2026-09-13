# Acceptance schedule and stop-publication rules for the locked validation set

**Pre-registration. Committed before the first label is coded.**

Drafted by the systems-researcher seat under RULING 1 of the council's rulings session of
2026-09-13, which assigned the schedule to this seat because it studies the instrument and
holds no stake in the candidate list. Integrity-officer reviews; chairman adopts.

## 0. What this file is, and what it is not

The instrument's original acceptance criteria (**V1–V6**) and its stop-publication rules
(**S1–S3**) existed only in the uncommitted "R2.1 record". That document was never under
version control on any branch and is gone. The chairman ruled that reconstructing them from
memory would fabricate the acceptance bar itself — strictly worse than having none, because
an instrument that then passes a fabricated bar produces a validated-looking result with no
provenance, and no later reader could tell which numbers were remembered and which were
recorded.

**This file therefore does not reconstruct V1–V6 or S1–S3, does not wear their names, and
uses prefixes that cannot be confused with them: `ACC-1…ACC-5` and `HALT-1…HALT-4`.** It is
smaller than what was lost. That is the point: it contains only what this repository can
support at the commit that adds it.

Nothing here is a label, a score, or a band for any item, and no item is named.

Per taxonomy entry 34 (`agents/integrity-officer.md:178`) — the defect of a follow-up note
freezing an *inference* into a committed artefact that then carries a pre-registration's
authority — **every threshold below is tagged `[CARRIED]`, `[GROUNDED]` or `[CHOSEN]` on its
face**, and an inference is marked as an inference in those words.

- `[CARRIED]` — transcribed from a surviving committed file, cited by line. Not re-derived.
- `[GROUNDED]` — computed or read from a committed artefact of this repository, cited.
- `[CHOSEN]` — a judgment call made by this seat, with the reason stated. No `[CHOSEN]`
  number has provenance older than this file.

## 1. The evidence base this schedule is allowed to draw on

Verified at the commit that adds this file.

| Source | What it supplies | Verified |
|---|---|---|
| `analytics/locked_set/SCHEMA.md:96-109` | the evaluation design: production-path replay, surfaced/not-surfaced as the decision, run-size batching under a recorded seed, Clopper-Pearson intervals, per-category reporting | read at this commit |
| `SCHEMA.md:105-107` | the 20×10 stability design and its **four blocking thresholds**, surviving verbatim | read at this commit |
| `SCHEMA.md:107-109` | **S4**'s content, preserved in substance | read at this commit |
| `SCHEMA.md:74-84`, `:87-94` | nine categories, 6 each, 20 positives; matter-level disjointness | read at this commit |
| `SCHEMA.md:12-24`, `:57-72` | commit order that proves blindness; single coder; `L_theme`/`L_band` never reconciled | read at this commit |
| `scripts/eval_holdout.py:37-42` | CI floors `DEFAULT_FAIL_UNDER_PRECISION = 0.90`, `DEFAULT_FAIL_UNDER_RECALL = 0.60`, set deliberately below the holdout's observed precision 1.00 / recall 0.75 | read at this commit |
| `scripts/eval_holdout.py:14` | the repository's own worked Clopper-Pearson example: 3/4 → [0.19, 0.99] | read at this commit |
| `analytics/candidate_telemetry.jsonl` | 328 records, 9 run ids; `classification.outcome` = 141 `keyword_only_by_design`, 120 `provider_error`, 67 `ok`; all 328 `v2_call.basis = "lexical_only"` | counted at this commit |
| `digests/*/meta.json` | **16 archived runs**; `screened` = 78, 14, 79, 80, 11, 13, 23, 14, 12, 11, 7, 13, 30, 10, 67, 30; **`matches` = 0 in all 16** | counted at this commit |
| `prompts/classifier.txt:77-82` | exactly three bands — HIGH (70–100), MEDIUM (40–69), LOW (0–39) | read at this commit |
| `src/classify.py:89-96`, `:110-111` | `keyword_only_by_design` with `attempts > 0` is a PROVIDER_FAILURE; `keyword_after_provider_error` is the direct value | read at this commit |
| `src/config.py:290` | `_DEFAULT_THRESHOLD = 40` | read at this commit |

## 2. Power, stated before anyone measures anything

This section is placed **before** the criteria deliberately. The set is **54 items with 20
positives**; batch 1 is **6**. A clean result on a set this size is not validation, and
stating so after the number is in hand is too late.

### Intervals computed for this file

Method: **exact Clopper-Pearson two-sided 95%**, the beta-quantile form — lower
= `BetaInv(α/2, x, n−x+1)`, upper = `BetaInv(1−α/2, x+1, n−x)`, α = 0.05; for x = n the
lower bound reduces to `(α/2)^(1/n)`. Computed in Python, no external library.

**Method validated against the repository's own published figure before use:** `x=3, n=4`
reproduces **[0.1941, 0.9937]**, i.e. the [0.19, 0.99] printed at `scripts/eval_holdout.py:14`.

| x / n | 95% Clopper-Pearson | What it means here |
|---|---|---|
| **6 / 6** | **[0.5407, 1.0000]** | batch 1, perfect. Consistent with a true rate as low as **54%**. |
| 5 / 6 | [0.3588, 0.9958] | batch 1, one miss. Consistent with a true rate as low as **36%**. |
| **20 / 20** | **[0.8316, 1.0000]** | all 20 positives, perfect. Consistent with a true rate as low as **83%**. |
| 18 / 20 | [0.6830, 0.9877] | all 20 positives, two misses. Lower bound **68%**. |
| 54 / 54 | [0.9340, 1.0000] | every item, perfect — the most the whole set can ever say. |

The 6/6 figure is the same [0.54, 1.00] the chairman stated in RULING 3(iv); this file
reproduces it independently rather than citing it.

### What each size can and cannot decide — binding

- **Batch 1 (n = 6) measures exactly two things**: grammar fidelity (the band the instrument
  assigns against `L_band`) and whether any tier-S item surfaces at all. **It is not
  precision. It is not recall.** Ruled in RULING 3(iv); restated here because this is the
  file a future seat will read.
- **No seat may report batch 1, or any partial batch, as validation of the instrument**, and
  no grade moves on six items.
- **At n = 20 positives, recall cannot be distinguished from 0.83 even when it is perfect.**
  A recall point estimate at or above the `eval_holdout.py` floor of 0.60 is therefore
  **consistent with** the floor, never a demonstration of exceeding it.
- **Precision's denominator is not fixed in advance** — it is however many items the
  instrument surfaces, which may be zero (see HALT-1, whose measured current state is
  `matches = 0` in 16 of 16 archived runs). **A precision of 1.00 on a denominator of 1 or 2
  is not a result.** Every precision figure is reported with its denominator printed
  adjacent, and with the interval, or it is not reported.
- **Per-category figures are n = 6 by construction** (`SCHEMA.md:74`). No per-category
  criterion below carries a pass/fail threshold, for the reason in the 6/6 row above:
  per-category numbers are **reported**, never **passed**.

## 3. ACC — acceptance criteria

Each is a proposition about the instrument's behaviour on the locked set, with its
statistic, its threshold, and the data it is computed from. Applied after the set is coded
and replayed under `SCHEMA.md:96-105`.

**ACC criteria are evaluated on the full 54-item set only.** None is evaluated on batch 1.

---

### ACC-1 — Grammar fidelity beats a blind guess

- **Proposition.** The band the instrument assigns agrees with the coder's `L_band` at a
  rate that the evidence can distinguish from blind guessing among three bands.
- **Statistic.** Proportion of coded items where the instrument's band equals `L_band`, with
  its exact Clopper-Pearson 95% interval; reported per-category as well, without a threshold.
- **Data.** `labels.json` `L_band` versus the band assigned on the production-path replay.
- **Threshold.** The interval's **lower bound > 0.333**. `[GROUNDED]` in
  `prompts/classifier.txt:77-82`, which defines exactly three bands, so a uniform blind guess
  succeeds at 1/3.
  **Marked inferred:** that a blind guess is *uniform* over the three bands is an
  **inference, unvetted** — the true band distribution of the locked set is unknown until it
  is coded, and if it is skewed, a majority-band guesser beats 1/3. **The replay therefore
  also reports the observed `L_band` distribution and the majority-band baseline alongside
  the statistic**, so a later reader can apply the stricter bar this file could not compute
  in advance. ACC-1 is not claimed to pass against the majority baseline.
- **Cannot decide.** At n = 54 this criterion distinguishes competence from noise. It says
  nothing about *which* band the instrument gets wrong; that is what the per-category
  reporting is for.

### ACC-2 — Publication precision does not fall below the instrument's own committed floor

- **Proposition.** Of the locked-set items the instrument surfaces on the production path,
  the proportion whose `L_theme = 1` does not fall below the floor the repository already
  enforces in CI.
- **Statistic.** Publication precision, point estimate, **printed with its denominator**, and
  with its exact Clopper-Pearson 95% interval.
- **Data.** Surfaced/not-surfaced from the replay; `L_theme` from `labels.json`.
- **Threshold.** Point estimate **≥ 0.90**. `[CARRIED]` from
  `scripts/eval_holdout.py:41` (`DEFAULT_FAIL_UNDER_PRECISION = 0.90`), the floor this
  repository already fails a build against, itself set below the holdout's observed 1.00.
- **Cannot decide.** Per §2, at these sample sizes the interval **cannot exclude** true
  values below 0.90 — 20/20 bottoms out at 0.83. **ACC-2 is a non-inferiority check against a
  committed floor, not a demonstration that precision exceeds it**, and any report of ACC-2
  that omits this sentence is a misreport.

### ACC-3 — Publication recall does not fall below the instrument's own committed floor

- **Proposition.** Of the **20 positives**, the proportion the instrument surfaces does not
  fall below the CI floor.
- **Statistic.** Publication recall over the 20 positives, with its exact Clopper-Pearson 95%
  interval; reported per-category without a threshold.
- **Data.** Surfaced/not-surfaced from the replay; the 20 `L_theme = 1` items.
- **Threshold.** Point estimate **≥ 0.60**. `[CARRIED]` from
  `scripts/eval_holdout.py:42` (`DEFAULT_FAIL_UNDER_RECALL = 0.60`), set below the holdout's
  observed 0.75.
- **Cannot decide.** Same limitation as ACC-2, and sharper: the holdout's 0.75 rests on
  **4 on-theme items** (`scripts/eval_holdout.py:14`, 3/4 → [0.19, 0.99]). Neither the
  holdout nor this set can separate 0.60 from 0.95.

### ACC-4 — Stability, at the thresholds that survived

- **Proposition.** The 20 × 10 stability sweep crosses **none** of the four blocking
  thresholds.
- **Statistic and thresholds.** `[CARRIED]` in full from **`SCHEMA.md:105-107`**, which
  survived the loss verbatim. **They are cited, not restated as new numbers, and this file
  does not reproduce, round, reinterpret or extend them.** Read them at that line range.
- **Data.** The 20 × 10 sweep run under the recorded seed of `SCHEMA.md:99-101`.
- **Note on the silent-fallback limb.** `analytics/candidate_telemetry.jsonl` at this commit
  shows 141 of 328 records at `keyword_only_by_design` and 120 at `provider_error`. **The
  sweep is not merely required to pass the surviving threshold; the four thresholds are
  evaluated on a sweep that itself satisfies ACC-5, or the sweep is re-run.**

### ACC-5 — Every accepted decision rests on an executed classification

- **Proposition.** No item's surfaced/not-surfaced decision in the accepted replay of record
  was produced on a degraded path.
- **Statistic.** Count of replay records whose `classification.outcome` is
  `keyword_after_provider_error`, or is `keyword_only_by_design` with `attempts > 0` — the
  provider-failure signature documented at `src/classify.py:89-96` — or whose `v2_call.basis`
  is `lexical_only` where a V2 verdict was relied on.
- **Data.** The replay's telemetry records, same schema as
  `analytics/candidate_telemetry.jsonl`.
- **Threshold.** **Zero.** `[CHOSEN]` by this seat. **Reason, stated rather than assumed:** a
  stability sweep tolerates a small fallback rate because it measures variance across ten
  runs, where a stray degraded record is noise. The acceptance replay is a **single record of
  record**, and there one degraded record is not noise — it is a wrong decision about a
  specific item, carried into a precision or recall figure as though it were the
  instrument's judgment. The remedy is cheap: re-run the affected items. **This threshold is
  not carried from anything and has no provenance older than this file.** It is deliberately
  *not* the 0.05 of `SCHEMA.md:106-107`; borrowing that number for a different purpose would
  be restating a surviving threshold as a new one, which RULING 1 forbids.
- **Cannot decide.** ACC-5 detects degradation the telemetry *records*. It cannot detect a
  failure mode the telemetry does not yet have a field for.

---

**Nothing below ACC-5 is an acceptance criterion.** This schedule has five. If a future
sitting needs a sixth, it adds it as `ACC-6` under §6's amendment rule — never by
renumbering, and never by reviving a V-number.

## 4. HALT — stop-publication rules

A HALT is not a failed criterion. A HALT stops publication or declares the set unusable.

### HALT-1 — Zero positives reach the threshold on the production path

**This rule carries S4's content, which is *preserved*, not remembered.**
`[CARRIED]` from **`SCHEMA.md:107-109`**: *S4 (zero positives reach 40 on the production
path) is the current state of the system and the reason the fill-floor is suspended.*

- **Trigger.** No `L_theme = 1` item in the locked set reaches the digest threshold
  (`src/config.py:290`, `_DEFAULT_THRESHOLD = 40`) on the production path.
- **Effect.** The fill-floor stays suspended and **no match-grade finding is published**. The
  set's per-category and band-composition figures may still be reported *as measurements of
  the instrument*; a surfaced-item claim may not.
- **Measured current state at this commit, so no reader has to take the rule on faith.** All
  **16** archived runs in `digests/*/meta.json` report `"matches": 0`. HALT-1's trigger
  condition is the system's present state, not a hypothetical.

### HALT-2 — Disjointness breach at the level of the matter

- **Trigger.** Any locked-set matter is found, after locking, to collide with the development
  sets — the retired 20-item holdout, the 14 frozen probes, or the 16 distinct published
  matters — at the level of the **matter**, not the document (`SCHEMA.md:87-94`).
- **Effect.** The affected item is struck; **its category's figures are reported at the
  reduced n with the strike named**, and any already-published figure that included it is
  withdrawn and corrected, not silently recomputed. The replacement row goes through the same
  certification and the category is re-locked as a new batch.

### HALT-3 — The blindness order is broken

- **Trigger.** `python3 scripts/check_lock.py` exits nonzero for any batch directory, or the
  git history fails to show `items.json` locked before `labels.json` and `labels.json` locked
  before any scorer touched the set (`SCHEMA.md:12-24`).
- **Effect.** **Every result computed on the affected batch is void**, not provisional. The
  git history is the only evidence that labels preceded scores; if it does not show that, the
  measurement does not exist. A void batch is disclosed as void and is not re-locked into
  validity — it is re-built from items that were never scored.

### HALT-4 — The coder saw the instrument

- **Trigger.** Any item whose `L_theme` or `L_band` was recorded with sight of the
  instrument's score, band, digest placement, or any seat's characterisation of how the item
  "should" code; or any label produced by a model rather than the single human coder
  (`SCHEMA.md:70-72`; RULING 3(ii): agreement is not corroboration).
- **Effect.** The item is struck and its category reported at reduced n. **If the exposure
  cannot be bounded to specific items, the batch falls under HALT-3 and is void.**

---

**Nothing below HALT-4 is a stop-publication rule.** This schedule has four.

## 5. What this file deliberately does not contain

Recorded so that a later reader can tell absence from oversight.

- **No V1–V6 and no S1–S3, and no criterion numbered in either series.** Lost, declared lost,
  not re-derived. See §0.
- **No restatement of the four stability thresholds.** ACC-4 cites `SCHEMA.md:105-107`.
  Copying four surviving numbers into a new file creates a second home for them that can
  drift from the first.
- **No per-category pass/fail threshold.** n = 6 per category; §2 gives the reason.
- **No floor-band or threshold-band count criterion.** `SCHEMA.md:103-104` requires both to be
  *reported*; this seat found nothing in the repository that grounds a *threshold* on either,
  and declined to invent one.
- **No cost criterion.** The triage per-call constant survives
  (`src/config.py:226`, `TRIAGE_COST_PER_CALL_USD = 0.0014`), but a classification call's real cost is
  ordered re-derived from telemetry under RULING 4(c) and is not yet derived. A criterion
  written against an undelivered number would be a premise-in-the-pre-registration, taxonomy
  entry 34 exactly.
- **No V2 shadow criterion.** All 328 V2 telemetry records are `lexical_only`; RULING 4(b)
  quarantines every V2 shadow figure from publication and comparison until the locked set
  produces a calibration. An acceptance criterion is a publication surface.
- **No inter-rater statistic**, proposed or reserved (`SCHEMA.md:71-72`).
- **No label, score or band for any item, and no item named.**

## 6. Pre-registration discipline

**This file is committed before the first label is coded.** That is a checkable claim, not an
assurance:

- **The commit that proves it** is the commit that adds this file — recover it with
  `git log --diff-filter=A --format=%H -- analytics/locked_set/ACCEPTANCE_SCHEDULE.md`.
- **The test.** That SHA must precede the first commit touching
  `analytics/locked_set/labels.json` (or `analytics/locked_set/batch-N/labels.json`) in the
  history of whatever branch carries the result. **At the commit that adds this file,
  `git log --all -- analytics/locked_set/labels.json` and the same for `items.json` return
  nothing: neither file has ever existed at any commit on any branch**, so there is no label
  in this repository for this schedule to have been fitted to.

**Amendment.** Any change to this file after a label exists is a **disclosed amendment, never
a silent edit**. A disclosed amendment appends a dated row to the table below stating the
identifier touched, the old text, the new text, the reason, and **how many labels existed at
the time** — and the results section that relies on it repeats the disclosure. Editing a
threshold without that row falsifies a pre-registration, which is the defect this file was
written to prevent.

| Date | Identifier | Was | Is | Reason | Labels coded at amendment |
|---|---|---|---|---|---|
| — | — | — | — | none yet | — |

**Provenance of this file's own numbers, in one line:** every threshold is tagged
`[CARRIED]`, `[GROUNDED]` or `[CHOSEN]`; exactly one — ACC-5's zero — is `[CHOSEN]`, and it
says so where it stands.
