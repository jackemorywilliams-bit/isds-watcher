# Human Review Checkpoint

The research pipeline is automated, but its output is offered as **research leads to be
verified before they are relied upon, not as adjudications** (METHODOLOGY.md Part IX). This
file formalizes that stance into a logged, recurring human check: a person periodically
spot-audits a sample of the period's cited claims, records pass/fail, and clears verification
debt. It is the human-in-the-loop gate the methodology already calls for, made into an
auditable record rather than an assumption.

## What gets reviewed

- The **insight ledger** (`analytics/insights.jsonl`) — the durable claims the research stands on.
- The **state-of-the-answer synthesis** (`STATE_OF_THE_ANSWER.md`) — especially its
  "Verification debt" section and anything marked `[unverified]`.
- The period's **daily records** (`analytics/daily-research/`) and any **research briefs**
  (`briefs/`) issued in the window.

## Cadence

- **Monthly** — the standing checkpoint. Spot-audit a sample of cited claims from the month's
  records (default **N = 5** claims, chosen to cover each ring and the trade-secret / clinical-
  data sub-question where the month produced material on them).
- **On escalation** — out of cadence, audit immediately when a flagged event lands (e.g. the
  *Einarsson* award issuing), before the new claim is folded into the state-of-the-answer as
  verified.

## How to run a review (the procedure)

1. Pick the sample: prefer claims that are load-bearing, recently added, or marked
   `[unverified]`; cover the three rings and the sub-question where possible.
2. For each sampled claim, open the cited source(s) and check that the source exists, says what
   the claim says, and supports the date / holding / figure as stated. A claim with no openable
   source, or one the source does not support, is a **FAIL**.
3. Record the result in the log below. For any FAIL, note the fix taken (corrected, marked
   `[unverified]`, or removed from `STATE_OF_THE_ANSWER.md` and the ledger).
4. Clear or update the "Verification debt" section of `STATE_OF_THE_ANSWER.md` for items
   audited this round; promote a confirmed `[unverified]` claim to verified.

## What a review cycle entails

The procedure above is the shape of a cycle. This section spells out, step by step, what the
operator actually does at the keyboard so a cycle is reproducible and leaves an honest record.

1. **Run the assisted first pass.** Regenerate the draft with `python scripts/review_prep.py`. It
   samples cited claims from the period's digests and briefs and runs the deterministic URL check
   (`scripts/verify_citations.py`) over the sampled sources. This produces the Cycle draft below —
   reachability only, no judgement about substance.
2. **Open each sampled cited source by hand.** For every sampled claim, open the cited source and
   read it. The question is not whether the URL resolves — the assisted pass already answered that —
   but whether the source **actually supports the claim**: the date, the holding, the figure, the
   characterisation as stated. A URL that loads but does not say what the claim says is a **FAIL**.
3. **Mark each pass or fail.** Fill in the "Human final pass/fail" field for every sampled claim.
   Be specific about what failed (wrong date, source does not reach the holding, paywall obscures
   the point cited, etc.).
4. **Record any correction made.** Where a claim was wrong or overstated, note the fix taken —
   corrected in place, marked `[unverified]`, or removed from `STATE_OF_THE_ANSWER.md` and
   `analytics/insights.jsonl` — in the "Corrections made" field.
5. **List what could not be confirmed as standing verification debt.** Any sampled source that is
   paywalled, unreachable, or that you could not personally confirm supports the claim stays in the
   "Verification debt" list and is carried forward, not silently cleared. Verification debt is only
   cleared by a human who has read the source and confirmed it.
6. **Sign and date the entry.** Complete the "Operator ratification" fields — reviewer, date, final
   pass rate, debt cleared, corrections — and sign off. The cycle is not a review until this is done.

**Standing rule.** Until a review cycle is logged for the period, the system's outputs for that
period are described as **"machine-assisted research leads," not "validated findings."** The
assisted first pass establishes only that cited URLs resolve; it never substitutes for the human
read. A claim becomes a validated finding only after a person has opened its source, confirmed it
supports the claim, and signed the entry below.

## Review log

Append one entry per review. Template:

```
### YYYY-MM-DD — monthly review (reviewer: NAME)
- Window covered: YYYY-MM-DD to YYYY-MM-DD
- Sample size: N
- Claims audited:
  1. <claim / source> — PASS | FAIL — <note; fix if FAIL>
  2. ...
- Verification-debt items cleared: <list, or "none">
- Pass rate: X / N
- Notes / follow-ups:
```

---

_No human review has been logged yet. The first monthly checkpoint is due one month after the
first daily record (2026-06-23). Standing verification debt to clear at that review is listed in
`STATE_OF_THE_ANSWER.md` (the China NMPA 2026 Measures, the Jason Yu Song award particulars, and
the Einarsson Article 1121 waiver characterization)._

_Ahead of that human checkpoint, the council has prepared an **assisted first pass** (Cycle 1,
below) to make the human's job concrete: it samples the period's cited claims and runs the
deterministic source-checker over their URLs so a person can ratify rather than start from a blank
page. **It is a DRAFT, not a review** — no human has reviewed these claims; the draft's blank
fields and sign-off remain to be completed by the operator._

## Assisted first passes (council-prepared drafts — NOT human reviews)

Generated by `scripts/review_prep.py`. Each cycle below is a **DRAFT** the council prepares for the
operator to ratify: it samples cited claims/URLs from the most recent digests and briefs, runs the
deterministic citation checker (`scripts/verify_citations.py`) over the sampled URLs, and records the
automated source-check outcome plus a verification-debt list. The automated check confirms only that
a URL **resolves and is openable** — it does **not** confirm the source supports the claim, which is
the human judgement the monthly checkpoint above still requires. A cycle becomes a real review only
when a person completes the "Operator ratification" fields and signs off. To regenerate a draft:
`python scripts/review_prep.py`.

### 2026-06-29 — Cycle 1 — DRAFT (council-prepared, pending operator ratification)

> This is an ASSISTED FIRST PASS produced mechanically by `scripts/review_prep.py`.
> It is NOT a human review and asserts no human has reviewed anything. The automated
> source-check confirms only whether a cited URL resolves and is openable — it does
> NOT confirm the source supports the claim. The operator (Jack) must complete the
> blank fields and sign off before any of this counts as reviewed.

- Automated source-check tally: 4 sampled — 4 reachable, 0 paywalled, 0 unreachable, 0 unchecked

#### Sampled claims and automated source-check outcomes

1. **Okuashvili v. Georgia**
   - URL: https://www.italaw.com/cases/9965
   - Origin: digest 2026-06-29 — digests/2026-06-29_ISDS-Thematic-Watch/articles/01_okuashvili-v-georgia.md
   - Item date (as stated): 26 June 2026
   - auto: reachable (PASS-candidate, substance unverified) [HTTP 200]
   - Human final pass/fail: __________   Corrections made: __________

2. **Court of Appeal of Santiago sets aside salmon venture award on ultra petita grounds**
   - URL: https://www.iareporter.com/articles/court-of-appeal-of-santiago-sets-aside-salmon-venture-award-on-ultra-petita-grounds/
   - Origin: digest 2026-06-29 — digests/2026-06-29_ISDS-Thematic-Watch/articles/02_court-of-appeal-of-santiago-sets-aside-salmon.md
   - Item date (as stated): 29 June 2026
   - auto: reachable (PASS-candidate, substance unverified) [HTTP 200]
   - Human final pass/fail: __________   Corrections made: __________

3. **Swedish Supreme Court finds that claimant in Okuashvili v. Georgia can use MFN detour to access arbitration under SCC Arbitration Rules**
   - URL: https://www.iareporter.com/articles/swedish-supreme-court-finds-that-claimant-in-okuashvili-v-georgia-could-use-mfn-detour-to-access-arbitration-under-scc-arbitration-rules/
   - Origin: digest 2026-06-29 — digests/2026-06-29_ISDS-Thematic-Watch/articles/03_swedish-supreme-court-finds-that-claimant-in.md
   - Item date (as stated): 29 June 2026
   - auto: reachable (PASS-candidate, substance unverified) [HTTP 200]
   - Human final pass/fail: __________   Corrections made: __________

4. **(brief citation) T05 (priority — UNCITRAL 59th session). I can confirm the pre-session posture but must flag the post-session outcome as unverified. The d...**
   - URL: https://uncitral.un.org/sites/default/files/2026-04/agenda_for_59th_session_of_the_commission-calendar_format_16_april_website_version.pdf
   - Origin: brief — briefs/2026-06-29-memo.md
   - auto: reachable (PASS-candidate, substance unverified) [HTTP 200]
   - Human final pass/fail: __________   Corrections made: __________

#### Verification debt (claims whose sources could not be machine-confirmed — NEEDS HUMAN EYES)

- **Okuashvili v. Georgia** — https://www.italaw.com/cases/9965
    - URL resolves but source-supports-claim NOT machine-verifiable — needs human read
- **Court of Appeal of Santiago sets aside salmon venture award on ultra petita grounds** — https://www.iareporter.com/articles/court-of-appeal-of-santiago-sets-aside-salmon-venture-award-on-ultra-petita-grounds/
    - item body self-reported as paywalled (holding not in record)
    - URL resolves but source-supports-claim NOT machine-verifiable — needs human read
- **Swedish Supreme Court finds that claimant in Okuashvili v. Georgia can use MFN detour to access arbitration under SCC Arbitration Rules** — https://www.iareporter.com/articles/swedish-supreme-court-finds-that-claimant-in-okuashvili-v-georgia-could-use-mfn-detour-to-access-arbitration-under-scc-arbitration-rules/
    - item body self-reported as paywalled (holding not in record)
    - URL resolves but source-supports-claim NOT machine-verifiable — needs human read
- **(brief citation) T05 (priority — UNCITRAL 59th session). I can confirm the pre-session posture but must flag the post-session outcome as unverified. The d...** — https://uncitral.un.org/sites/default/files/2026-04/agenda_for_59th_session_of_the_commission-calendar_format_16_april_website_version.pdf
    - URL resolves but source-supports-claim NOT machine-verifiable — needs human read

#### Operator ratification (to be completed by the human)

- Reviewer: __________________________
- Date reviewed: ______________________
- Final pass rate: ______ / 4
- Verification-debt items cleared this cycle: __________________________
- Corrections made (to `STATE_OF_THE_ANSWER.md` / `analytics/insights.jsonl`): __________________________
- Sign-off (operator confirms the above is reviewed and accurate): __________________________
