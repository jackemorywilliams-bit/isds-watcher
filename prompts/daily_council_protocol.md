# Daily council meeting — binding format protocol (operator-mandated, 2026-07-27)

The daily meeting record committed to `analytics/daily-research/<DATE>.md` is emailed
to the operator verbatim. The rules below are BINDING; each exists because a real
defect reached the operator.

## Rule 0 — SIZE. Two convened seats, and one optimization item. (2026-08-07)

The daily meeting is **the researcher, the chairman, and one optimization suggestion.**
That is the whole meeting.

**Convene exactly two agents:** `research-analyst` and `council-chairman`. Nothing else.

- The **integrity challenge stays**, as a required voice inside the Part V dialogue per
  Rule 2. It is not a separately convened seat and does not file its own return.
- The **one optimization item** is written by the chairman in a single short paragraph.
  Do **not** convene `systems-researcher` for it. Its daily note and
  `analytics/systems-research/<DATE>.md` are not part of this meeting.
- Do **not** convene `analytics-officer`. The digest sentence required by Rule 1 is two
  lines the chairman copies from `meta.json`.

**Banned from the daily record, all of it:** an instrument-probe table; a "Priority
focus" agenda section; a "Budgets" section; a carrying-span ledger with per-term
occurrence counts and parity arithmetic; a "Verify / be skeptical" section; a
"Repository facts" section. Those belong to the weekly council and to the standing
verification rules. They are not the daily meeting, and reproducing them turns a
check-in into a document nobody reads.

**Why.** On 2026-08-07 the daily record ran to five convened seats with a probe table, a
pre-registered decision-rule adjudication, and a four-entry carrying-span ledger showing
occurrence sums. The operator's correction, verbatim: *"the daily council meetings are
meant to be the researcher + the chairman + one optimization suggestion or whatever."*
A daily check-in that costs a weekly council is a daily check-in that stops being read,
and an unread record verifies nothing.

**Precedence note.** `COUNCIL.md` lists the systems researcher and the analytics officer
as daily seats. For the **daily meeting** this file overrides that, per Precedence below.
Their weekly and roundtable roles are unaffected.

## Rule 1 — digest numbers: fixed terminology, copied, never restated

The word "screened" alone is BANNED with a number attached — it caused a direct
contradiction (the record said "One screened item" while the digest header said
"Screened: 10"; both were readings of the same ambiguous word). Use only these two
terms, with values copied verbatim from the digest's `meta.json`:

- **candidates evaluated** — `meta["screened"]`: everything the instrument looked at.
- **items surfaced** — `meta["matches"] + meta["watch_list_leads"]`: what actually
  appeared in the digest.

Any Part IV / analytics discussion of the digest MUST open with:
`Digest <date>: <N> candidates evaluated, <M> items surfaced (<matches> matches,
<leads> watch-list leads).` The emailer independently prints the same numbers from
`meta.json` and flags any mismatching "N screened" phrase with a visible
CONSISTENCY WARNING — write it right the first time.

## Rule 2 — the council discussion (Part V) is a real dialogue, not a summary

The operator's instruction: the council discussion "should be expanded moving
forward." Minimum standard for Part V:

- Attributed, multi-turn dialogue (**Chairman:**, **Researcher:**, **Integrity
  check:** at minimum), at least six substantive exchanges on a normal day, at
  least three even on a quiet day.
- The integrity voice must challenge at least one concrete assertion (verified vs
  inferred, naming the source) and the challenged party must answer on the record.
- End with the chairman's one-paragraph close-out: what is SOLID, what is OPEN,
  what must NOT be asserted, and anything for the principal's attention.
- Quiet days are stated plainly, but the dialogue still happens — "nothing new"
  is a finding the council discusses, not a reason to skip the discussion.

## Precedence

These rules bind the daily routine regardless of any other prompt wording. If the
routine's own instructions ever conflict, THIS file wins, and the conflict itself
is worth a line in the record's procedural caveat.

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
