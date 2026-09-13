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

**Amended 2026-09-13, before any label existed, on the chairman's ruling.** The first draft
was written against the design's **54 items with 20 positives** as though those were
properties of the set. They are not. The validation record's candidate list came in at
**38 of the 54 design-target rows**, and the 20-positives figure is a **target the set has
not met**, not a property it has. Every place that assumed otherwise is corrected below, and
the amendment is disclosed in §6's table rather than made silently. **54 and 20 are design
targets. 38 is the set.** See §2.0, and §2.3 for the limitation the same certificate
imposed on what the set can ever evidence.

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
| `SCHEMA.md:74-84`, `:87-94` | nine categories, 6 each, 20 positives — **the design target**; matter-level disjointness | read at this commit |
| the validation record (2026-09-13) §3.12 | **the set as built: 38 of 54 rows** — cat 1: 6, cat 2: 2, cat 3: 6, cat 4: 6, cat 5: 6, cat 6: 6, cat 7: 6, cat 8: 0, cat 9: 0; 16 rows open under gaps `G-1` and `G-2` | read at this commit |
| the validation record (2026-09-13) §3.11, rows `C-1`…`C-6` | the six anchor matters excluded by the disjointness certificate | read at this commit |
| `SCHEMA.md:12-24`, `:57-72` | commit order that proves blindness; single coder; `L_theme`/`L_band` never reconciled | read at this commit |
| `scripts/eval_holdout.py:37-42` | CI floors `DEFAULT_FAIL_UNDER_PRECISION = 0.90`, `DEFAULT_FAIL_UNDER_RECALL = 0.60`, set deliberately below the holdout's observed precision 1.00 / recall 0.75 | read at this commit |
| `scripts/eval_holdout.py:14` | the repository's own worked Clopper-Pearson example: 3/4 → [0.19, 0.99] | read at this commit |
| `analytics/candidate_telemetry.jsonl` | 328 records, 9 run ids; `classification.outcome` = 141 `keyword_only_by_design`, 120 `provider_error`, 67 `ok`; all 328 `v2_call.basis = "lexical_only"` | counted at this commit |
| `digests/*/meta.json` | **16 archived runs**; `screened` = 78, 14, 79, 80, 11, 13, 23, 14, 12, 11, 7, 13, 30, 10, 67, 30; **`matches` = 0 in all 16** | counted at this commit |
| `prompts/classifier.txt:77-82` | exactly three bands — HIGH (70–100), MEDIUM (40–69), LOW (0–39) | read at this commit |
| `src/classify.py:89-96`, `:110-111` | `keyword_only_by_design` with `attempts > 0` is a PROVIDER_FAILURE; `keyword_after_provider_error` is the direct value | read at this commit |
| `src/config.py:290` | `_DEFAULT_THRESHOLD = 40` | read at this commit |

## 2. Power, stated before anyone measures anything

This section is placed **before** the criteria deliberately. A clean result on a set this
size is not validation, and stating so after the number is in hand is too late.

### 2.0 The set as it actually stands — not the design target

**The design target is 54 items with 20 positives. The set is not that set, and this
schedule is written against the set that exists.**

- **38 of the 54 design-target rows are nominated** (the validation record, §3.12): cat 1: 6,
  cat 2: **2**, cat 3: 6, cat 4: 6, cat 5: 6, cat 6: 6, cat 7: 6, cat 8: **0**, cat 9: **0**.
  Sixteen rows are open under gaps `G-1` (category 2 unfillable — every matter the repository
  knows in it collided with a development set) and `G-2` (categories 8 and 9 are
  retrieval-generated by decision: a category-8 item **is** its headline, so nominating one
  from memory would fabricate the single field the coder reads). The refusal to pad was ruled
  correct; padding would have produced a full-looking table whose missing rows no later reader
  could find.
- **The 20-positives figure is a target the set has not met, not a property it has.** It
  survives at `SCHEMA.md:74` as a property of the 54-row *design*. **The number of positives
  in the set as built is not known and cannot be known before coding**, because `L_theme` is
  the single coder's independent determination and no label exists at this commit. Nothing in
  this schedule may assume it is 20, and nothing may assume it is 20 minus the shortfall
  either: **the design's allocation of the 20 positives across the nine categories is not
  recorded in any surviving file**, so the shortfall cannot even be apportioned. Marked
  **inferred, unvetted** would be too generous — it is simply unknown.
- **Notation used below.** **P** = the number of items in the built set the coder records at
  `L_theme = 1`, fixed only when `labels.json` is committed. **N** = the number of items in
  the built set. Every criterion and every interval below is written in P and N, never in
  20 and 54.
- **Per-category n is no longer uniform.** It is 6, **2**, 6, 6, 6, 6, 6, **0**, **0**. Two
  categories contribute nothing at all, and category 2 — IP + ISDS with a negative
  investment/jurisdiction holding, which is the shape the research question is most directly
  about — contributes two rows.
- **N is not frozen, and this schedule does not pretend it is.** The 38 is the *nomination*
  tally at the validation record. Batch 1 has since committed six **retrieval-generated**
  category-8 tier-S items (`5c24077` on `council/locked-set-batch-1`, six rows, no label
  field), which is `G-2`'s closure route rather than a nomination from memory. **Every ACC
  figure therefore names the N and the commit it was computed at**, and a figure that names
  neither is not a result. If further rows are filled, each is a new batch under RULING 3's
  batching rule and is locked as one; this section's figures are re-stated for the set as it
  then stands, as a disclosed amendment under §6.

### 2.1 Intervals computed for this file

Method: **exact Clopper-Pearson two-sided 95%**, the beta-quantile form — lower
= `BetaInv(α/2, x, n−x+1)`, upper = `BetaInv(1−α/2, x+1, n−x)`, α = 0.05; for x = n the
lower bound reduces to `(α/2)^(1/n)`. Computed in Python, no external library.

**Method validated against the repository's own published figure before use:** `x=3, n=4`
reproduces **[0.1941, 0.9937]**, i.e. the [0.19, 0.99] printed at `scripts/eval_holdout.py:14`.

**Read the third column carefully: only the first two rows are about a set that exists.**

**(a) The set that exists today.**

| x / n | 95% Clopper-Pearson | What it means here |
|---|---|---|
| **6 / 6** | **[0.5407, 1.0000]** | **batch 1, perfect — the only row about a set that exists today.** Consistent with a true rate as low as **54%**. |
| 5 / 6 | [0.3588, 0.9958] | batch 1, one miss. Consistent with a true rate as low as **36%**. |

**(b) The set as nominated — 38 rows, computable because N is known.**

| x / n | 95% Clopper-Pearson | What it means here |
|---|---|---|
| **38 / 38** | **[0.9075, 1.0000]** | every nominated row correct — **the most the set as built could ever say about any all-items rate**. Still consistent with a true rate of **91%**. |
| 36 / 38 | [0.8225, 0.9936] | two misses across the built set. Lower bound **82%**. |
| 2 / 2 | [0.1581, 1.0000] | **category 2, perfect.** Consistent with a true rate as low as **16%**. A perfect category-2 result says almost nothing. |

**(c) Sizes the set has NOT reached — what it *would* be able to say if the design target
were met. These are statements about a hypothetical set, not about this one.**

| x / n | 95% Clopper-Pearson | Hypothetical |
|---|---|---|
| 20 / 20 | [0.8316, 1.0000] | *if* P reached the design's 20 and every positive surfaced. Lower bound **83%**. |
| 18 / 20 | [0.6830, 0.9877] | same hypothetical, two misses. Lower bound **68%**. |
| 54 / 54 | [0.9340, 1.0000] | *if* all 54 design-target rows existed and every one were correct. |

**(d) The recall denominator is not computable in advance.** P is fixed only when
`labels.json` is committed, so no recall row can be given here for the set as it stands.
**The general form, so a later seat computes it rather than guesses it:** for a perfect
result at any P, the exact 95% lower bound is `0.025^(1/P)`. It is **0.9075** at P = 38,
**0.8316** at P = 20, **0.5407** at P = 6 — and it falls away fast below that. Whatever P
turns out to be, the interval is reported at that P, printed beside the count.

The 6/6 figure is the same [0.54, 1.00] the chairman stated in RULING 3(iv); this file
reproduces it independently rather than citing it.

### 2.2 What each size can and cannot decide — binding

- **Batch 1 (n = 6) measures exactly two things**: grammar fidelity (the band the instrument
  assigns against `L_band`) and whether any tier-S item surfaces at all. **It is not
  precision. It is not recall.** Ruled in RULING 3(iv); restated here because this is the
  file a future seat will read.
- **No seat may report batch 1, or any partial batch, as validation of the instrument**, and
  no grade moves on six items.
- **Recall's denominator is P, and P is unknown until the set is coded.** Even at the design's
  hypothetical 20 positives, a perfect recall cannot be distinguished from 0.83; **at the
  P this set will actually produce it will be distinguished from less.** A recall point
  estimate at or above the `eval_holdout.py` floor of 0.60 is therefore **consistent with**
  the floor, never a demonstration of exceeding it.
- **Precision's denominator is not fixed in advance** — it is however many items the
  instrument surfaces, which may be zero (see HALT-1, whose measured current state is
  `matches = 0` in 16 of 16 archived runs). **A precision of 1.00 on a denominator of 1 or 2
  is not a result.** Every precision figure is reported with its denominator printed
  adjacent, and with the interval, or it is not reported.
- **Per-category figures are n ≤ 6, and are not uniform.** Six per category was the design
  (`SCHEMA.md:74`); the built set is 6, **2**, 6, 6, 6, 6, 6, **0**, **0**. No per-category
  criterion below carries a pass/fail threshold, for the reason in the 6/6 and 2/2 rows
  above: per-category numbers are **reported**, never **passed**. **Two categories produce no
  figure at all**, and a per-category table that omits them silently would read as though the
  instrument had been tested on nine categories. **Categories 8 and 9 are printed in every
  per-category table with `n = 0` and the gap slug `G-2`, never dropped**, and category 2 is
  printed with `n = 2` and `G-1`.

### 2.3 What the set can never decide — the six anchor matters

**This is not a footnote. It attaches to any grade this set ever moves, and to every ACC
figure below.**

The matter-level disjointness certificate (the validation record, §3.11, rows `C-1`…`C-6`)
removed **every one of the project's anchor matters** from the locked set: **Eli Lilly v.
Canada; Bridgestone v. Panama; Philip Morris Asia v. Australia; Philip Morris Brands v.
Uruguay; Apotex v. United States; Hela Schwarz v. China.** The exclusion is correct and was
not a choice — those six are the classifier's own **development seeds**
(`prompts/classifier.txt:26-33`) and they appear in the frozen probes, `S1_seed_eli_lilly`,
`S2_seed_bridgestone_pm` and `E4_einarsson_negative_space`, which `agents/Claim Map.md:858`
identifies as the Apotex / Hela Schwarz negative-space shape. A matter the instrument was
built on cannot also be the evidence that the instrument works.

**The consequence, in this schedule's own terms:**

- **No ACC criterion below is evidence about the instrument's performance on those six
  matters, and none can ever be made into such evidence.** They are outside N, outside P, and
  outside every interval in §2.1.
- **The set can never evidence the instrument's performance on the six matters the project
  most cares about.** They are the matters the research question is drawn from, the matters
  the digests reach for, and the matters a reader of any grade will assume were tested.
- **Any grade this set moves carries that limitation with it.** A seat reporting an ACC result
  states, in the same breath as the number, that the six anchor matters are excluded by
  construction and that the instrument's behaviour on them remains **unmeasured**. A grade
  reported without that sentence overstates what was measured.
- **This is a permanent property of the set, not a gap to be closed.** There is no future
  retrieval that fixes it: admitting an anchor matter would breach `SCHEMA.md:87-94` and
  trigger **HALT-2**. The honest disposition is disclosure, not repair.
- **It compounds with §2.0.** The anchor matters are exactly the IP + ISDS shapes that
  categories 1 and 2 exist to hold, and category 2 — which `G-1` reports unfillable for the
  same reason, every known matter in it being in a development set — stands at 2 rows. **The
  thinning and the exclusion have one cause**, and a reader who sees only the 38 will not see
  that the missing rows and the missing anchors are the same fact.

## 3. ACC — acceptance criteria

Each is a proposition about the instrument's behaviour on the locked set, with its
statistic, its threshold, and the data it is computed from. Applied after the set is coded
and replayed under `SCHEMA.md:96-105`.

**ACC criteria are evaluated on the complete locked set as actually built — N items, of
which P are positives — never on the 54-row design target and never on batch 1.** N and P
are defined in §2.0 and are printed beside every figure. Every ACC result is reported
together with the §2.3 anchor-matter limitation.

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
- **Cannot decide.** At the built set's N — 38 nominated rows, not 54 — this criterion
  distinguishes competence from noise across the set as a whole. It says nothing about
  *which* band the instrument gets wrong; that is what the per-category reporting is for.
  It says nothing at all about categories 8 and 9, which contribute no rows, and nearly
  nothing about category 2, which contributes two (§2.1(b), 2/2 → [0.1581, 1.0000]).

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
  values below 0.90 — even a perfect result across the whole built set bottoms out at 0.9075
  (§2.1(b), 38/38), and the denominator here is not N but however many items the instrument
  surfaces, which may be far smaller and may be zero. **ACC-2 is a non-inferiority check
  against a committed floor, not a demonstration that precision exceeds it**, and any report
  of ACC-2 that omits this sentence is a misreport.

### ACC-3 — Publication recall does not fall below the instrument's own committed floor

- **Proposition.** Of the **P positives in the set as built**, the proportion the instrument
  surfaces does not fall below the CI floor. **P is not 20.** Twenty was the design target
  (`SCHEMA.md:74`); the set as built is 38 of 54 rows and P is unknown until `labels.json`
  is committed (§2.0).
- **Statistic.** Publication recall over the P positives, **with P printed as a count beside
  it**, and with its exact Clopper-Pearson 95% interval computed at that P; reported
  per-category without a threshold, categories 8 and 9 printed at `n = 0`.
- **Data.** Surfaced/not-surfaced from the replay; the items the coder recorded at
  `L_theme = 1` in `labels.json`.
- **Threshold.** Point estimate **≥ 0.60**. `[CARRIED]` from
  `scripts/eval_holdout.py:42` (`DEFAULT_FAIL_UNDER_RECALL = 0.60`), set below the holdout's
  observed 0.75. **The threshold is carried unchanged; only the denominator it is applied to
  has been corrected.**
- **Cannot decide.** Same limitation as ACC-2, and sharper for two reasons. First, the
  holdout's own 0.75 rests on **4 on-theme items** (`scripts/eval_holdout.py:14`,
  3/4 → [0.19, 0.99]); neither the holdout nor this set can separate 0.60 from 0.95. Second,
  **the set's recall is measured on P, and P falls short of the design's 20 by an amount
  nobody can state in advance** — sixteen rows are absent, and the design's allocation of
  positives across categories is not recorded anywhere surviving, so the shortfall cannot be
  apportioned. **A recall figure from this set is therefore not the recall the design was
  built to measure, and may not be reported as though it were.** Its interval is computed at
  the realised P per §2.1(d) (`0.025^(1/P)` for a perfect result), not at 20.

### ACC-4 — Stability, at the thresholds that survived

- **Proposition.** The 20 × 10 stability sweep crosses **none** of the four blocking
  thresholds.
- **Statistic and thresholds.** `[CARRIED]` in full from **`SCHEMA.md:105-107`**, which
  survived the loss verbatim. **They are cited, not restated as new numbers, and this file
  does not reproduce, round, reinterpret or extend them.** Read them at that line range.
- **Data.** The 20 × 10 sweep run under the recorded seed of `SCHEMA.md:99-101`. **The 20 in
  "20 × 10" is a count of items drawn for the sweep, not the design's 20 positives**, and the
  two must not be conflated now that the latter is a target the set has not met (§2.0). The
  built set has 38 nominated rows, so a 20-item sweep is drawable; **the sweep records which
  items it drew and under which seed**, and if fewer than 20 items are available at the time
  of the sweep, the sweep is reported at the number actually drawn and ACC-4 is reported as
  **not evaluable at the surviving design**, never as passed at a smaller sweep.
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

- **Trigger.** No `L_theme = 1` item in the locked set as built reaches the digest threshold
  (`src/config.py:290`, `_DEFAULT_THRESHOLD = 40`) on the production path. **"Positives" here
  means the P items the coder recorded at `L_theme = 1`, not the design's 20** (§2.0); S4's
  content is carried unchanged and only the population it is read against is stated
  correctly.
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
- **No per-category pass/fail threshold.** n ≤ 6 per category, and 2, 0, 0 in three of them;
  §2.0 and §2.2 give the reason.
- **No criterion, and no interval, written in 54 or 20.** Those are design targets. The set is
  38 nominated rows with an unknown P, and a schedule written against the target would have
  pre-registered a bar the set cannot be measured against — the same defect as reconstructing
  V1–V6, arrived at from the other direction.
- **No apportionment of the missing positives.** Sixteen rows are absent and the design's
  allocation of the 20 positives across the nine categories is not recorded in any surviving
  file. Estimating how many positives are missing would be exactly the fabrication §0 forbids.
- **No criterion that the anchor-matter exclusion could be read to satisfy.** §2.3 states the
  limitation instead: the six matters are outside the set permanently and no ACC figure
  speaks to them.
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
  history of whatever branch carries the result. **At the amending commit,
  `git log --all -- analytics/locked_set/labels.json` returns nothing: `labels.json` has
  never existed at any commit on any branch**, so there is no label in this repository for
  this schedule to have been fitted to. **`items.json` does exist** — six category-8 tier-S
  items at `5c24077` on `council/locked-set-batch-1`, carrying no label field, which is what
  `SCHEMA.md:16` requires of it. Item content is not a label; the pre-registration test is
  and has always been `labels.json`.
- **The 2026-09-13 amendment below is itself pre-label.** It was made on the same branch,
  before `items.json` or `labels.json` existed anywhere, and it is recorded in the table
  regardless — the disclosure rule is not waived because the amendment happened to be early.
  The same `git log --all` check re-run at the amending commit still returns nothing.

**Amendment.** Any change to this file after a label exists is a **disclosed amendment, never
a silent edit**. A disclosed amendment appends a dated row to the table below stating the
identifier touched, the old text, the new text, the reason, and **how many labels existed at
the time** — and the results section that relies on it repeats the disclosure. Editing a
threshold without that row falsifies a pre-registration, which is the defect this file was
written to prevent.

| Date | Identifier | Was | Is | Reason | Labels coded at amendment |
|---|---|---|---|---|---|
| 2026-09-13 | §0, §1, §2 (whole), ACC-1 "Cannot decide", ACC-2 "Cannot decide", ACC-3 (whole), ACC-4 "Data", HALT-1 "Trigger", §5, §6 | the set stated as **54 items with 20 positives**; ACC-3's denominator "the 20 positives"; §2's 20/20 and 54/54 intervals presented as this set's power; "n = 6 by construction" per category; "evaluated on the full 54-item set only" | the set stated as **38 of 54 nominated rows with P unknown until coding**; ACC-3's denominator **P, printed as a count**; the 20/20 and 54/54 intervals **relabelled as a hypothetical set** and rows for 38/38, 36/38 and 2/2 added; per-category n stated as **6, 2, 6, 6, 6, 6, 6, 0, 0**; §2.3 added for the six excluded anchor matters | the chairman ruled that the schedule may not be drafted against a 54-item assumption: the validation record's list came in at **38 of 54**, categories 8 and 9 at 0 of 6 by decision and category 2 at 2 of 6 through development-set collision, and **20 positives is a target the set has not met, not a property it has**. No threshold changed; only the populations they are applied to | **none — `labels.json` and `items.json` still do not exist at any commit on any branch** |

**Provenance of this file's own numbers, in one line:** every threshold is tagged
`[CARRIED]`, `[GROUNDED]` or `[CHOSEN]`; exactly one — ACC-5's zero — is `[CHOSEN]`, and it
says so where it stands.
