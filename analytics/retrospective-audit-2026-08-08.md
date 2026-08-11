# Retrospective audit of the published archive — re-derived from the files, 2026-08-08

Workstream I, first deliverable. Every figure below was recomputed from
`digests/*/articles/*.md` and `digests/*/meta.json` on 2026-08-08 — not carried
forward from any council record, because two of those records disagree with the
files (both corrections noted below). Gate: chairman's ledger #18.

## 1. The denominators

| Count | Value | Basis |
|---|---|---|
| Article files | **14** | glob over `digests/*/articles/*.md` |
| Distinct URLs | **13** | Telefónica v. Colombia (italaw.com/cases/12153) published 2026-06-09 **and** 2026-06-10 |
| Distinct underlying matters | **12** | Okuashvili/Swedish Supreme Court are one dispute through two fora (2026-06-29, entries 01 and 03) |
| Runs | 11 | `meta.json` files |
| Screenings | 347 | Σ `meta["screened"]`; events, not distinct items; 157 of the 347 (06-09, 06-10) were backfilled by hand in commit `228793c` |
| Items ≥ threshold 40, ever | **0** | every `meta.json`, `matches: 0` |

**Any figure published with 14 as its denominator needs the 13/12 qualifier.**

## 2. Ring display, re-derived

7 of 14 entries display a ring; 7 display none. Scores of ring-displaying
entries: 25, 25, 25, 25, 28, 32, 35. `ip_as_investment`: **0 occurrences as a
displayed ring**; 3 occurrences in annotations, every one a negation.

**Entries displaying a ring at score 25: FOUR** (not five — the chairman's
2026-08-08 ruling overcounted by including Okuashvili, which sits at 28):

| Run | Entry | Ring | Substantive support (integrity-officer review) |
|---|---|---|---|
| 2026-06-22 | Cour de cassation | judicial_or_regulatory_measure | **Unsupported** — ICC-award enforcement; forum's own act; no investor-State proceeding in the item |
| 2026-06-29 | Santiago set-aside | judicial_or_regulatory_measure | **Unsupported** — annotation itself applies the wrong test ("by virtue of being a court judgment") |
| 2026-06-29 | Swedish Supreme Court | jurisdictional_admissibility | Supported (MFN detour); "upheld" overstates the headline |
| 2026-07-06 | Suez retrospective | jurisdictional_admissibility | Supported; "exhaustion" paraphrase defect |

The two judicial-ring entries additionally contradict the classifier contract
(judicial ring ⇒ at least MEDIUM). All four now carry dated corrections in the
archive. The pair at 32/28 with contradictory verdicts (Telefónica) is
cross-referenced in both entries.

## 3. Annotations disclaiming their own item, re-derived

Coding rule (unchanged from R2.1): **A** = explicit negative thematic conclusion
about this item; hedges excluded; **B** = states it cannot assess.

**Category A: FIVE entries** (R2.1's count of three used too narrow a phrase
list; the chairman's "at least five" is confirmed exactly):

| Run | Score | Phrase |
|---|---|---|
| 2026-06-10 (Hydro) | 28 | "fails to trigger the three-ring theme because there is no intellectual property at stake" |
| 2026-06-10 (Telefónica) | 28 | "raises no IP-as-investment angle … falls below the thematic intersection" |
| 2026-06-29 (Okuashvili) | 28 | "outside the thematic intersection" |
| 2026-06-29 (Santiago) | 25 | "does not align with the thematic focus" |
| 2026-08-03 (Gazprom) | 25 | "no ISDS thematic intersection" — asserted about a body never read |

**Category B: ONE** — 2026-06-22 (UK High Court), "impossible to assess."

So 6 of 14 published entries state, in their own text, that they are off-theme
or unassessable. All were mailed as watch-list leads.

## 4. Classifier provenance

Nine entries score 25, which the deterministic scorer cannot emit (reachable
set in [20,40] is {28,29,30,31,32,33,40}, plus 35 via the negative-signal cap):
those nine are model-path output with certainty. The five at 28/32/35 are
formally ambiguous — the archive records no per-item model identity. Telemetry
(Phase 0, in flight) closes this for future runs; for these five it is
unrecoverable.

## 5. Stability evidence the project already owns

Telefónica, same URL, same source date, consecutive runs: **32 with a ring →
28 with no ring.** A 4-point score delta and a ring flip on unchanged input,
already on the public record. The R2.1 stability design (20 items × 10 runs)
remains worth running; this single data point already demonstrates the failure
mode it is designed to measure, and is recorded in both archive entries.

## 6. Operator labelling protocol — the 13-item retrospective audit

The cheap step before the 54-item locked set: label the 13 distinct published
items against `L_theme` ∈ {0,1} (does the item reach the three-ring research
question?) under these rules:

1. Label from the item's **source page**, not from the annotation; read the
   annotation only after the label is recorded.
2. Machine scores are on the page and in the archive; **blindness cannot be
   claimed retrospectively and is not claimed** — the protocol's protection is
   the ordering rule above plus a one-sentence written reason per label naming
   which rings are present and absent.
3. Ten of the 13 rest on paywalled bodies; where the body cannot be read,
   record `L_theme = cannot_assess` — do not infer from the headline.
4. The Telefónica pair is one item with two published verdicts; label the item
   once, and record separately which of the two verdicts (if either) the label
   supports.
5. Record labels through `scripts/verify_digest.py` so each lands in the
   append-only ledger under the operator's identity. Note its URL-dedupe
   presents only the 2026-06-10 Telefónica verdict; the 06-09 verdict must be
   assessed too (defect recorded in the R2 integrity audit).
6. Expected yield: a retrospective published-precision estimate on the real
   production distribution, at the cost of 13 codings. With ten
   `cannot_assess` likely, the informative sample may be ~3-4 items —
   report it with that limit stated, or not at all.

## 7. What this audit does not establish

No label here says anything about the unsurfaced population (no per-candidate
record exists before Phase 0); nothing here validates the classifier (that is
the locked set's job, `analytics/locked_set/`); and the single-coder limitation
is permanent and disclosed wherever these results are reported.
