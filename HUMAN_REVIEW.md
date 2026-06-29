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
