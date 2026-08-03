# Fingerprint gap report — the trade-secret / administrative-measure false negative

**Council session (one-off), fingerprint-gap analyst. Discipline: no-source-no-claim.**
Every number below is produced by the repository's own deterministic scorer
(`src/classify.py::keyword_score`) run over `analytics/fingerprint_probes.json`.
The canonical `fingerprint.yaml` was **not** modified; proposed weights were
measured against an in-memory temporary copy. Reproduce with the harness in the
appendix.

---

## 1. The gap, restated with evidence

The operator-acknowledged risk (METHODOLOGY.md Part X) is that the lexical
fingerprint — calibrated on patent/trademark seeds and a NAFTA/denial-of-justice
holdout — will **false-negative a pure trade-secret / clinical-data case whose
challenged measure is administrative, not judicial** (the *Einarsson v. Canada*
shape; a China data-exclusivity dispute). The July 2026 Ring 1 reweight toward
trade-secret vocabulary (`working/FINGERPRINT_DRIFT.md`) is reasoned but untested.

This report builds a 14-probe suite that isolates that shape and measures it. The
headline finding: **the gap is real and the holdout already contains its
fingerprint.** The one on-theme item the live holdout misses — `apotex_v_us`,
scored **8/100** — is exactly the administrative-rights-rejection shape (FDA ANDAs
asserted as a covered investment, held not to qualify). My synthetic negative-space
probe `E4` reproduces that miss independently (score 33). The instrument's blind
spot is not hypothetical; it is measured, in-sample, today.

A second, sharper finding the probes expose: **the discriminating signal that
separates an on-theme ISDS claim from off-theme pharma news lives in no ring.**
Probe `E2` (a real Einarsson-shaped *claim*) and probe `N1` (a pharma regulatory
*news item* with no arbitration at all) both score **33** on identical Ring 1
vocabulary. The scorer literally cannot tell them apart.

---

## 2. How scoring works (the four levers that matter here)

From `keyword_score`:

- Each ring sums the weights of its phrases found as **substrings** (lower-cased),
  capped at 100/ring.
- `PRESENT_FLOOR = 12` — a ring is "present" only at subtotal ≥ 12.
- `STRONG_SUBTOTAL = 18` — a single non-extra-weight ring reaches MEDIUM at ≥ 18.
- Band logic: **≥ 2 present rings → HIGH**; one present ring ≥ 18 (or any ring +
  a weaker second ring with subtotal > 0) → **MEDIUM (≥ 40)**; one present ring in
  [12, 17] with no second ring → **high-LOW (28–33)**; negative signals force ≤ 35
  unless Ring 1 or Ring 2 is present.

The trade-secret weights that matter: `trade secret` 9, `clinical trial data` 8,
`covered investment` 8, `data exclusivity` 6, `unfair commercial use` 5,
`trips article 39` 4, `regulatory data protection` 3. Ring 2 is **almost entirely
judicial** — the only non-judicial phrases are `Plain Packaging Measures` (4),
`public-interest legislation` (4), and the FET-family `minimum standard of
treatment` (6) / `manifest arbitrariness` (5) / `arbitrary or discriminatory` (5).
**There is no administrative-measure vocabulary and no `fair and equitable
treatment` phrase** (the term real awards actually use).

---

## 3. Probe suite results under the CURRENT fingerprint

14 probes: 5 Einarsson-shaped (E), 3 China-regime (C), 4 near-miss negatives (N),
2 seed controls (S). Pass = achieved band meets the theme-implied `expected_band`
(HIGH ≥ 70, MEDIUM ≥ 40, LOW < 40).

| Probe | Category | Expected | Score | Band | R1 | R2 | R3 | Result |
|---|---|---|---:|---|---:|---:|---:|---|
| E1_einarsson_dense | einarsson | HIGH | 76 | HIGH | 39 | 6 | 34 | **pass** |
| E2_einarsson_admin_fet | einarsson | MEDIUM | **33** | LOW | 17 | 0 | 0 | **FAIL (FN)** |
| E3_einarsson_msot_second_ring | einarsson | MEDIUM | 51 | MEDIUM | 32 | 6 | 5 | pass |
| E4_einarsson_negative_space | einarsson | MEDIUM | **33** | LOW | 17 | 0 | 0 | **FAIL (FN)** |
| E5_einarsson_lexical_brittle | einarsson | HIGH | **0** | LOW | 0 | 0 | 0 | **FAIL (FN)** |
| C1_china_data_exclusivity | china | MEDIUM | 45 | MEDIUM | 28 | 0 | 0 | pass |
| C2_china_marketing_loose | china | MEDIUM | **0** | LOW | 0 | 0 | 0 | **FAIL (FN)** |
| C3_china_dense_plus_jurisdiction | china | HIGH | 75 | HIGH | 34 | 0 | 32 | pass |
| N1_pharma_news_no_isds | negative | LOW | 33 | LOW | 17 | 0 | 0 | pass |
| N2_domestic_trade_secret_suit | negative | LOW | 33 | LOW | 17 | 0 | 0 | pass |
| N3_mining_concession | negative | LOW | 4 | LOW | 4 | 0 | 0 | pass |
| N4_investment_dispute_no_ip | negative | LOW | 5 | LOW | 0 | 0 | 5 | pass |
| S1_seed_eli_lilly | seed | HIGH | 75 | HIGH | 22 | 48 | 0 | pass |
| S2_seed_bridgestone_pm | seed | HIGH | 79 | HIGH | 26 | 38 | 48 | pass |

**Four false negatives: E2, E4, E5, C2.** No false positives. Seeds and negatives
behave. The reweight *works* when reporting happens to use the exact fingerprint
terms densely (E1, E3, C1, C3 all clear threshold) — but that is precisely the
condition a real Einarsson-shaped item cannot be relied on to meet.

---

## 4. Diagnosis — exactly what fell short, per false negative

### E2 (score 33) — the canonical miss: strong Ring 1, no administrative Ring 2
Matched: Ring 1 = `trade secret`(9) + `clinical trial data`(8) = **17**. Ring 2 = **0**,
Ring 3 = **0**. The claim pleads FET as `fair and equitable treatment` and
`arbitrary and unreasonable` — **neither is in the fingerprint** (Ring 2 has
`minimum standard of treatment` and `arbitrary or discriminatory`). The challenged
act is an "administrative decision" — **no Ring 2 phrase covers administrative
measures at all.** Ring 1 stalls one point short of `STRONG_SUBTOTAL` (17 < 18) and,
with no second ring to trigger the tie-rule, lands in the high-LOW branch
(`28 + (17−12) = 33`). **A single missing point of Ring 1 weight, or any
administrative-measure Ring 2 hit, would have crossed the threshold.**

### E4 (score 33) — the negative-space / *Apotex* / *Hela Schwarz* miss
Matched: Ring 1 = `trade secret`(9) + `clinical trial data`(8) = **17**, Ring 2/3 = 0.
This is a *decided rejection* of trade-secret-as-investment against an
administrative measure — the outer-limit ruling the watcher explicitly wants
(METHODOLOGY.md Part VI.B). The report never says `covered investment` or
`definition of investor` (it says "was not an investment", "not... a qualifying
investment"), so **Ring 1 has no negation-space phrasing to catch the rejection**,
and Ring 2 again has no administrative vocabulary. **This is the same shape as the
live holdout's only miss, `apotex_v_us` (score 8).**

### E5 (score 0) — register-level lexical brittleness
Matched: **nothing.** Squarely on-theme (pharmaceutical regulatory data as covered
investment; administrative measure; jurisdiction contested) but written in the
vocabulary secondary reporting actually uses: `confidential business information`,
`clinical data` (not `clinical trial data`), `regulatory data` (not `regulatory
data protection`), `data package`, `marketing-approval`, `fair and equitable
treatment`. **Not one is an exact fingerprint phrase.** A substring matcher against
a fixed lexicon scores this at zero. This is the theoretical ceiling of the
instrument, made concrete.

### C2 (score 0) — the same brittleness, on the China front
Matched: **nothing.** `regulatory data` (not `regulatory data protection`),
`exclusivity` (not `data exclusivity`), `data protection` (not a phrase),
`marketing-approval`, `creeping expropriation`, `denial of fair treatment`. The
2026 China regime described in loose journalistic terms is invisible to the scorer.

### Cross-cutting: the missing ISDS-nexus signal
`E2` and `N1` both score 33 on `trade secret`(9)+`clinical trial data`(8). `E2` is a
tribunal claim; `N1` is a news item with "no litigation, arbitration, or treaty
dispute." **The words that distinguish them — arbitration, tribunal, claimant,
treaty, investor-state — carry zero weight in any ring.** Any remediation that
raises Ring 1 to fix E2 will lift N1 in lock-step. This is the central constraint
on the fix (§5).

---

## 5. Proposed remediation (NOT applied) — measured before/after

The naive fix — raise trade-secret weights — is **wrong**: it converts the pharma-news
negatives (N1, N2, both at Ring 1 = 17) into false positives one-for-one with any
lift. The evidence-backed fix is **two small, ring-sum-preserving clusters plus a
structural gate**, so that on-theme claims gain a genuine *second* signal
(administrative-measure Ring 2) rather than just louder Ring 1.

### 5a. Ring 1 — near-miss variants (sum stays 100)
Add register-level variants; fund by trimming seed-specific patent/trademark
phrasings that (per `FINGERPRINT_DRIFT.md`) "match little beyond seed retellings."

| Phrase | Now | Proposed | Δ | Justified by |
|---|---:|---:|---:|---|
| clinical data | — | 4 | +4 | E5 |
| confidential business information | — | 4 | +4 | E5 |
| regulatory data | — | 2 | +2 | E5, C1, C3 |
| data package | — | 2 | +2 | E1, E5 |
| promise utility doctrine | 8 | 5 | −3 | seed-only |
| utility requirement | 6 | 3 | −3 | seed-only |
| patent invalidation | 4 | 2 | −2 | seed-only |
| exploitation of the trademark | 3 | 1 | −2 | seed-only |
| brand value | 2 | 1 | −1 | weak discriminator |
| copyright | 1 | 0 | −1 | weak discriminator |

### 5b. Ring 2 — administrative-route cluster (sum stays 100)
The structural gap the drift memo did not address: Ring 2 cannot see a regulatory
measure. Add an administrative/FET cluster; fund by trimming deep seed-verbatim
denial-of-justice long phrases. **Calibrated so the cluster alone (max
`fair and equitable treatment` 6 + `administrative measure` 5 = 11) stays below the
PRESENT_FLOOR of 12** — it can supply the weak-second-ring tie that rescues a
strong Ring 1, but cannot by itself manufacture a present ring out of common FET
boilerplate.

| Phrase | Now | Proposed | Δ | Justified by |
|---|---:|---:|---:|---|
| fair and equitable treatment | — | 6 | +6 | E2, E5 |
| administrative measure | — | 5 | +5 | E1, E3, E4, C1 |
| administrative act | — | 2 | +2 | E4 |
| arbitrary and unreasonable | — | 2 | +2 | E2 |
| denial of justice | 14 | 10 | −4 | seed-verbatim |
| judicial propriety | 6 | 4 | −2 | seed-verbatim |
| manifestly unjust judgment | 6 | 4 | −2 | seed-verbatim |
| shocks a sense of judicial propriety | 5 | 2 | −3 | seed-verbatim |
| egregiously wrong that no honest or competent court could | 5 | 2 | −3 | seed-verbatim |
| systemic failure in the administration of justice | 4 | 3 | −1 | seed-verbatim |

### 5c. Measured effect — every probe, before → after

| Probe | Expected | Current | Proposed | Effect |
|---|---|---:|---:|---|
| E1_einarsson_dense | HIGH | 76 | 76 | held |
| **E2_einarsson_admin_fet** | MEDIUM | **33** | **43** | **FIXED** |
| E3_einarsson_msot_second_ring | MEDIUM | 51 | 51 | held |
| **E4_einarsson_negative_space** | MEDIUM | **33** | **43** | **FIXED** |
| **E5_einarsson_lexical_brittle** | HIGH | **0** | **41** | **crosses threshold** (MEDIUM, not HIGH) |
| C1_china_data_exclusivity | MEDIUM | 45 | 50 | held/up |
| **C2_china_marketing_loose** | MEDIUM | **0** | **2** | **still missed (residual)** |
| C3_china_dense_plus_jurisdiction | HIGH | 75 | 75 | held |
| N1_pharma_news_no_isds | LOW | 33 | 33 | **held LOW** |
| N2_domestic_trade_secret_suit | LOW | 33 | 33 | **held LOW** |
| N3_mining_concession | LOW | 4 | 4 | held LOW |
| N4_investment_dispute_no_ip | LOW | 5 | 5 | held LOW |
| S1_seed_eli_lilly | HIGH | 75 | 75 | **held HIGH** |
| S2_seed_bridgestone_pm | HIGH | 79 | 78 | **held HIGH** |

The phrase/weight change recovers **3 of the 4** false negatives (E2, E4 fully to
MEDIUM; E5 from invisible-0 to a threshold-crossing 41) **while leaving every
negative LOW and every seed HIGH.**

### 5d. Holdout is not regressed by the proposal

| | TP | FP | TN | FN | Precision | Recall | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| Current | 3 | 0 | 16 | 1 | 1.00 | 0.75 | 0.95 |
| Proposed | 3 | 0 | 16 | 1 | 1.00 | 0.75 | 0.95 |

Seed-verbatim holdout items dip only within margin (`loewen` 56→53, `mondev` 62→60;
both stay well above 40). No off-theme item is promoted (**FP stays 0**). `apotex`
stays 8 under the proposal — the phrase fix does **not** reach the negation-space /
loose-vocabulary residuals (see §6). This is stated, not hidden.

### 5e. The structural piece the fingerprint alone cannot do — an ISDS-nexus gate
`E2` and `N1` remain lexically identical after §5a–b. The only durable separator is
an **investor-state-nexus precondition**: require at least one of {`arbitration`,
`tribunal`, `investor-state`, `bilateral investment treaty`/`BIT`, `claimant` +
`respondent`, `ICSID`/`UNCITRAL`} before a Ring-1-driven item is promoted past
high-LOW. This is a **code change to `keyword_score` (a gate), not a fingerprint
edit**, so it is proposed here for operator approval rather than measured against a
temp YAML. Its predicted effect: N1 (news, no nexus) is pinned LOW regardless of
Ring 1 lift, which is what makes it safe to raise Ring 1 further in a future round.
C2 would still need §5a-style loose-vocabulary variants to be seen at all.

---

## 6. Red-team — why this suite might give false comfort

1. **Synthetic text ≠ real reporting.** I wrote these probes knowing the lexicon.
   Even the "brittle" probes (E5, C2) are my *guess* at how real reporting drifts
   from the seed vocabulary; a real Einarsson award or a Reuters item on the China
   regime may drift in ways I did not anticipate — different near-misses, or, worse,
   accidental exact hits that flatter the scorer. The suite proves the failure
   *modes* exist; it does **not** estimate their real-world base rate. Corroboration
   is limited to one real in-sample case (`apotex_v_us`), which agrees with E4.
2. **I tuned the proposal to the probes I wrote.** The +2/+4 weights in §5 were
   chosen because they move *my* probes across the line at minimal cost. This is
   curve-fitting to a 14-point synthetic set. The holdout (§5d) is the only
   out-of-sample check, and it is tiny (4 on-theme items) and contains no
   trade-secret/administrative case at all — so it can confirm "no regression" but
   **cannot confirm the fix generalizes** to real trade-secret cases. There are none
   to test against; that is the whole predicament.
3. **The negatives are close.** N1 and N2 sit at 33 — seven points under threshold
   on the same Ring 1 vocabulary the proposal touches. The proposal keeps them at 33
   only because it adds no phrase they contain. A future Ring 1 raise *without* the
   §5e gate would convert them to false positives. The margin is thin and the report
   should not be read as "safe to keep raising Ring 1."
4. **Adding `fair and equitable treatment` to Ring 2 is double-edged.** FET is
   boilerplate in nearly every investment claim. It is deliberately sub-floor (6 <
   12), but it now supplies a weak-second-ring tie to *any* IP-adjacent item that
   pleads FET — a small, systematic upward pressure on the MEDIUM band that this
   suite is too small to price.

### What would falsify the proposal
- **A real trade-secret / clinical-data ISDS item** (Einarsson award; a filed China
  data-exclusivity claim) that scores **< 40 under the proposed weights** — proving
  the fix does not generalize past my synthetic probes.
- **Any off-theme pharma or FET-boilerplate item** that scores **≥ 40 under the
  proposed weights** — proving the administrative/FET cluster over-triggers.
- **A holdout expansion** (even 5–10 real trade-secret/administrative items, labelled
  by the operator) on which proposed recall does **not** beat current recall.
- The **ISDS-nexus gate (§5e) failing to hold N1-class news LOW** on real feeds once
  implemented.

Until a decided trade-secret ISDS case exists, **none of these can be fully run** —
which is itself the finding: the instrument is being asked to detect a case shape
that has never been observed, and no amount of synthetic probing closes that gap.
The honest posture is the operator's current one — **hold the reweight, keep the
probe suite as a standing tripwire, and revisit when real case law lands.**

---

## 7. Recommendation

1. **Do not apply** the §5 weights yet (operator gate; consistent with
   `FINGERPRINT_DRIFT.md` "revisit when Einarsson converts the pathway to case law").
2. **Adopt the probe suite as a regression harness** (`tests/test_fingerprint_probes.py`),
   with the four current false negatives marked `xfail(reason="pending
   operator-approved reweight")` so the day the reweight lands, the harness reports
   xpass and the guardrail flips automatically.
3. **Prioritize the §5e ISDS-nexus gate** over any further Ring 1 raise — it is the
   only change that decouples on-theme recall from pharma-news false positives.
4. **Treat E5/C2/apotex as the semantic-scoring case**: register-level paraphrase and
   negation-space rejections are beyond a fixed substring lexicon. The LLM path
   (`MODEL_PROVIDER=claude`) is the proper instrument for those; the keyword scorer
   should be understood as a recall floor, not a ceiling.

---

## Appendix — reproduction

```
# scorer over the probe suite, current + proposed weights, per-ring breakdown:
python3 scratchpad/measure.py          # (harness used for this report)
# baseline holdout gate:
python3 scripts/eval_holdout.py
# standing regression harness:
python3 -m pytest tests/test_fingerprint_probes.py -v
```

Authoritative scores come from `src.classify.keyword_score`; the per-ring subtotal
breakdown is diagnostic instrumentation that mirrors the same substring loop.
Proposed weights were applied to an in-memory deep copy of the fingerprint via the
module cache; **`fingerprint.yaml` on disk was never edited.**

<!-- graph:auto start -->
Map: [[Evidence Ledger]]
<!-- graph:auto end -->
