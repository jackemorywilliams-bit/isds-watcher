# The classification state space: R2.1's seven against the implementation's four

**Date:** 2026-08-09  **Author:** systems designer (council)  **Status:** resolved and encoded

## The discrepancy

R2.1 names **seven** classification outcomes and enumerates the ring contract's
state space over them:

    64 ring configurations x 4 nexus x 4 evidence locations x 3 validities x 7 = 21,504

`src/rings.py` imported the **four** values of `classify.ClassifyOutcome` and
`tests/test_rings.py` enumerated:

    64 x 4 x 4 x 3 x 4 = 12,288

The ratio is exactly 7/4. Nothing in the code, the tests or the commit messages
disclosed the substitution — the test asserted `== 12_288` as though that were
the specified number. That is the defect: not that four was wrong, but that a
narrower space was advertised as the space.

## The resolution

**The seven are the logical space and the enumeration axis. The four are the
operational record they are derived from.** Both are kept, and the derivation is
a function with tests (`rings.classification_state`), not a paragraph.

The two are different kinds of thing, which is why neither could simply replace
the other:

- `ClassifyOutcome` is written **at the moment the classifier returns**, by the
  code that knows what just happened to one HTTP call. It cannot know whether
  the item will later be abandoned, and it certainly cannot know whether the
  ring contract will demote one of the model's claims — the contract has not run
  yet, and it is the thing checking the classifier.
- R2.1's seven are the states the **rules** are stated in terms of. Three of them
  (`ok_first_pass`, `ok_after_retry`, `retry_abandoned`) are facts about a
  sequence rather than about a call, and one (`guard_demoted`) is a fact about
  the evidence check.

So the four are not a lossy compression of the seven. They are one input to them.

## The mapping

`rings.classification_state(outcome, attempts, retried_strict, abandoned, guard_demoted)`.
Ordered; total; every input reaches exactly one branch.

| # | R2.1 state | Derived from | Terminal? | Lane consequence |
|---|---|---|---|---|
| 1 | `retry_abandoned` | `abandoned=True` (the deferred queue hit `state.MAX_CLASSIFY_ATTEMPTS`) | run is finished — but **not** in `CLASSIFIED_STATES` | `RETRY` / `classification_abandoned` |
| 2 | `malformed_output` | `outcome == parse_failed` | no | `RETRY` / `classification_not_terminal` |
| 3 | `provider_failure` | `outcome == provider_error`, **or** `outcome == keyword_only_by_design` with `attempts > 0` | no | `RETRY` / `classification_not_terminal` |
| 4 | `keyword_only` | `outcome == keyword_only_by_design` with `attempts == 0` | yes | normal derivation |
| 5 | `guard_demoted` | `outcome == ok` and any ring's `semantic_credited < model_claimed_strength` | yes | normal derivation |
| 6 | `ok_after_retry` | `outcome == ok`, `retried_strict=True` | yes | normal derivation |
| 7 | `ok_first_pass` | `outcome == ok`, `retried_strict=False` | yes | normal derivation |

Anything unrecognised — `main.py` writes `"pipeline_error"` when the enrichment
merge around the classifier raises — falls to `malformed_output`, i.e.
non-terminal, retried, and recorded. An ending we cannot name is not an ending we
may conclude from.

### The four judgment calls, each argued

**1. Abandonment outranks its cause.** *Why* we gave up (a parse failure, an
outage) is still in `outcome` and still in telemetry. *That* we gave up is what
changes what may be concluded, so it takes the state slot.

**2. `retry_abandoned` is terminal for the run and NOT in `CLASSIFIED_STATES`.**
This is the subtle one and it is a real safety property. An abandoned item can
have a perfectly accessible body — a parse failure on text we fetched
successfully. If abandonment counted as a completed classification, three absent
*lexical* rings on that body would reach `REJECTED_CLASSIFICATION`, which reads
"we read this and it is off-theme" about an item no classifier ever managed to
read. That is the Gazprom failure mode arriving through a new door. It lands at
`Lane.RETRY` under its own reason code `classification_abandoned`, so the lane
says "nothing is knowable" and the reason says which kind of nothing. R2.1 fixes
five lanes and no sixth was invented.

**3. A failed call on a TAIL item is still a provider failure.** The contestable
step. `classify_item(intended_model=False)` records a provider error as
`KEYWORD_ONLY_BY_DESIGN`, because for the tail a keyword score is where the item
was going anyway. That is right about the *consequence* and wrong about the
*event*: a call was made and it failed, and an outage counted only on the
enriched top set is an outage under-counted by the whole size of the tail. The
two are separable because `attempts > 0` on the keyword path happens on no other
route — the no-provider path calls nothing and records 0. Consequence is not
lost; it is `intended_model`, which `TERMINAL_OUTCOMES` already encodes.

**4. A demotion outranks a clean pass.** `guard_demoted` and `ok_after_retry` can
both be true of one item. The demotion takes the single state slot because it is
the rarer and more consequential fact. This is the one place the mapping is a
**projection** rather than a bijection, and it is made lossless by the record
rather than by the state: `classification.retried_strict` and
`classification.attempts` are written to telemetry beside
`verdict_v2.classification_state`, and `verdict_v2.guard_demoted` is written as
its own boolean. Every one of the seven remains countable from a single record.

## Losslessness, stated precisely

The requirement is that each of the seven be **derivable** from the operational
record. It is, and `tests/test_rings.py` asserts it value by value, plus:

- totality — every `(outcome, attempts, retried_strict, abandoned, guard_demoted)`
  combination maps to a state, and all seven are reached;
- first-pass vs after-retry distinguishable;
- malformed vs provider failure distinguishable, in both directions;
- abandoned vs still-retrying distinguishable, and the abandoned item proved
  unable to reach `REJECTED_CLASSIFICATION`;
- `guard_demoted` present wherever a span verification demotes a ring — both
  when the span does not verify at all and when the title cap bites — and absent
  when a span verifies at its claimed strength.

The reverse direction (state → raw outcome) is not claimed and is not needed:
`verdict_v2.classification_outcome` carries the raw value anyway, so a single
telemetry record holds both.

## `guard_demoted` needed new state to exist at all

It could not be derived before this session, because nothing recorded what a
model had *claimed*. `RingFinding` now carries `model_claimed_strength` and
`semantic_credited`; a demotion is `semantic_credited < model_claimed_strength`,
which is true in exactly two situations, both of them span verification working:

1. the model claimed a ring and its span did not verify against the item's text;
2. the span verified **only in the title**, and the title cap cut it to `weak`.

Note this is about the *semantic credit*, not the final strength. A ring whose
model claim was thrown out but which stands at `present` on its own lexical
evidence was still demoted, and that is still the fact worth counting: the model
asserted something it could not point to.

## What this makes visible immediately

Running the legacy V1 path through the contract now produces `guard_demoted` on
**every** model-classified item with any ring. That is not noise. `prompts/classifier.txt`
returns a bare ring list with no evidence for any ring, so every V1 ring claim
fails verification by construction. The count of demotions is the audit's
objection expressed as a number the run produces about itself.

## Changes encoded

| File | Change |
|---|---|
| `src/rings.py` | `ClassifyState` (7), `CLASSIFIED_STATES`, `classification_state()`, `REASON_ABANDONED`; `derive_lane` and `RingVerdict` key on the state; `RingFinding.model_claimed_strength` / `.semantic_credited` / `.guard_demoted` |
| `src/main.py` | disposition decided **before** the shadow derivation, so `abandoned` is known when the verdict is built |
| `src/telemetry.py` | `verdict_v2.classification_state`, `.classification_outcome`, `.guard_demoted`; schema 2 → 3 |
| `tests/test_rings.py` | enumeration 12,288 → **21,504**; one test per binding distinction |

`analytics/instrument-map-2026-08-08.md` is the integrator's file and was **not**
edited. This note is the record of the resolution.
