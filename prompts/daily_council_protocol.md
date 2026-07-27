# Daily council meeting — binding format protocol (operator-mandated, 2026-07-27)

The daily meeting record committed to `analytics/daily-research/<DATE>.md` is emailed
to the operator verbatim. Two format rules are BINDING; both exist because a real
defect reached the operator.

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
