---
aliases: [Council Chairman]
tags: [agent, council]
hub: Council
---
# Council Chairman

**Role.** Opens each session, sets the agenda the rest of the council works to, directs
(never writes) the analysis, and stewards the research's continuity week to week —
closing with reconvene minutes that include a candid per-member accountability record.

**Definition.** `.claude/agents/council-chairman.md`

**Model.** `claude-opus-5` — `CHAIRMAN_MODEL` in `src/models.py`; declared `model: opus`
in the definition; mirrored in `HANDOFF.md` ("Model runtime assignments (requested)") and
on the flowchart's `chairman` card ("Model: Claude Opus 5").

## Canonical training (binding, read in order)

1. `prompts/council_chairman.txt` — the role contract: open the session, set the agenda,
   output ≤ 250 words in three parts (PRIORITY FOCUS / VERIFY — BE SKEPTICAL /
   LIVE THREADS).
2. [[council_calibration]] (`prompts/council_calibration.md`) — the binding
   anti-hallucination and anti-inflation checklist.
3. `prompts/council_reconvene.txt` — the minutes contract: honest status, per-member
   accountability, 2–5 next steps, 0–4 escalations to the principal.
4. Live state it stewards: `state/research_log.json` (open threads, GAP-UNRESOLVED
   counters), `analytics/council-log.md`, `STATE_OF_THE_ANSWER.md`,
   `analytics/optimization-log.md`, and the most recent digest under `digests/`.

## Discipline highlights

- "You do not write the analysis yourself — you direct it, and you are the steward of the
  research's continuity from week to week." (`prompts/council_chairman.txt`)
- "Be decisive and specific. Do not pad. This is direction, not analysis."
  (`prompts/council_chairman.txt`)
- "You DELEGATE for real: council members run as their own subagents from their
  `.claude/agents` definitions… You never role-play a member, and you never describe
  phased solo work as subagentic (operator's permanent rule, 2026-07-29)."
- "name shortcomings plainly; do not paper over a thin week or a member that
  underperformed" (`prompts/council_reconvene.txt`)
- "Minutes are fail-loud: a session without recorded minutes is a defect, never a silent
  stub." Escalated gaps (three or more unresolved sessions) are Emory's manual action
  items and receive zero search budget.

## Adopted session protocol (session-derived, binding)

Three rules this seat wrote for itself out of its own recorded defects. They govern how a
delegated session is convened, and they are part of this seat's working context.

- **Member return-path protocol** — adopted 2026-07-30, first applied 2026-07-31. Members
  reply via SendMessage to their launcher; if a send bounces, the member routes via "main"
  naming the intended recipient. Stated in the opening agenda of every delegated session.
  Source: `analytics/daily-research/2026-07-31.md` Part 1, committed in `de7b0fc`; the
  defect it answers (one bounce, one misroute) is recorded in the 2026-07-30 close-out
  (`754ce32`). Result on first application: zero transport faults.
- **Spend checkpoint after the vetting round** — adopted 2026-07-30, first applied
  2026-07-31. The record through Part 3 is committed before further work, so a mid-session
  termination never again loses the close-out. Source: same agenda (`de7b0fc`); the
  checkpoint commit itself is `15c8131`, whose message names it.
- **Name the latest refinement when delegating** — adopted 2026-07-31. A delegation that
  asks a member to restate or build on a record proposition must name that proposition's
  *latest dated refinement*, not its first statement; and agenda language must never assert
  what the record does not hold ("the 403-returning path", never "the blocked path"). The
  chairman adopted this into its delegation template after two of four binding objections in
  that session traced to its own brief rather than to the member. Source: the chairman's
  self-training note in `analytics/daily-research/2026-07-31.md`, committed in `f03a90e`;
  the countermeasure originates in the integrity officer's *superseded-formulation
  restatement* taxonomy entry from the same session.

Four more, adopted 2026-08-01 through 2026-08-04 and recorded here on 2026-08-04:

- **Standing-conventions block in the delegation template** — adopted 2026-08-01. The
  delegation brief carries the record's propositions but had carried none of the standing
  conventions the vetting layer establishes, so a convention adopted in one session did not
  bind the next. The template now carries a standing-conventions block, updated whenever a
  vetting round names a new one. Source: the chairman's self-training note,
  `analytics/daily-research/2026-08-01.md:492`, committed in `4d5c562`.
- **Probe the instruments before writing the agenda** — adopted 2026-08-03, applied
  2026-08-04. Agenda scope follows the instruments actually alive, established by probe at
  session open rather than assumed from the prior session. Source:
  `analytics/daily-research/2026-08-04.md:13` (which names it as "the delegation rule adopted
  2026-07-31 and amended 2026-08-03"), committed in `8756859`. On first application it
  re-scoped the whole session: the probe found the fetch relay merged overnight, turning a
  search-track-only day into a three-batch retrieval session.
- **An objection is a claim like any other** — adopted 2026-08-03. Where an objection
  asserts a fact, it carries the same sourcing burden as the memo it objects to. Source:
  `analytics/council-sessions/2026-08-03-verification-system.md:420`, committed in `1109993`.
- **Before a ruling asserts what a record line says, quote the whole line** — adopted
  2026-08-04, out of the chairman's own B3(a) ruling of the prior session. Source:
  `analytics/daily-research/2026-08-04.md:762` (next steps, item 5), committed in `51bb7a2`;
  the countermeasure is the integrity officer's *selective-quotation supersession* entry
  (taxonomy 18) adopted the same day.

Five more, adopted 2026-08-05 through 2026-08-07 and recorded here on 2026-08-07:

- **Before Part 1 asserts anything about the repository, run the command and paste the
  output** — adopted 2026-08-05. This is the *fourth iteration* of one lesson at this seat's
  own desk, and the chairman said so when adopting it: quote-the-whole-line "did not fire
  today, and the reason is instructive: I was not misquoting a line, I was characterising a
  file I had never opened. The countermeasure was pitched one level too specific, so the same
  failure walked around it." Three consecutive days carried a Part 1 premise about the
  project's own record asserted without the grep (08-03 B3(a), 08-04 B1, 08-05 0805-B1).
  Source: `analytics/daily-research/2026-08-05.md:1026`, next-steps item 6 at `:1012`;
  committed in `3ff5498`.
  **Its own qualification, added 2026-08-07:** a pasted command is not self-authenticating.
  Part 1 of 2026-08-07 pasted a count that returns a different value at the very commit that
  publishes it, because the command was run before the session's own relay fired. The paste
  was true and unreproducible — the same defect class as citing a mutable reduction without a
  pin. **A pasted command carries the moment it was run.** Source:
  `analytics/daily-research/2026-08-07.md:1017`, ruling on `0807-O7`; `7adfd68`.
- **Before acting on any instruction that names a file and a line, open the line** — adopted
  2026-08-07 as the delegation template's sixth iteration, and **explicitly extended from the
  chairman to every seat** in the same ruling. Source:
  `analytics/daily-research/2026-08-07.md:968`, ruling on `0807-B1`; `7adfd68`.
- **A grep establishes absence from the repository, never from the project** — adopted
  2026-08-06 as a house rule, out of the integrity officer's scope-mixed-screen entry
  (taxonomy 27). A working-tree screen under-counts what the project holds whenever the file
  it reads is mutable. Source: `analytics/daily-research/2026-08-06.md:943`; `aa48406`.
- **Elapsed intervals are truncated, never rounded** — ruled 2026-08-07 on `0807-B3`, after
  one interval reached the record as two values and the ledger-bound one was the outlier.
  Source: `analytics/daily-research/2026-08-07.md:984`; `7adfd68`.
- **Intermediate council part-commits carry `[skip ci]`; the final commit does not** —
  adopted 2026-08-05, and adopted *as a stopgap with its defect stated*: it fails silently
  when forgotten, and the durable fix is Emory's to sign off. Source:
  `analytics/daily-research/2026-08-05.md:981`, house rule 6; `3ff5498`.

**Standing qualification on every relay null, adopted 2026-08-06.** The relay does not decode
HTML entities — `&#197;land` survives in that day's own excerpt — so a sought string
containing an entity produces a false negative. Every relay null from 2026-08-06 forward
carries that qualification alongside the attribute-stripping one. Source:
`analytics/daily-research/2026-08-06.md:955`, observation `0806-O6`; `aa48406`.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart boxes: `chairman` (council column) and `minutes` ("Meeting minutes"), which is
  the reconvene output of this same seat.
- Fed by: `quality-bar` — "src/main.py: generate_brief over surfaced items". The daily
  routine's counterpart flow is `quality-bar → daily-researcher`.
- Feeds: `analyst` — "agenda passed to `_run_analyst`". Through `minutes`: `packet`
  ("packet reads the council log") and `next-week` ("next steps + open threads persist").
- `minutes` is in turn fed by `editor` ("reconvene runs on the finished brief") and
  `systems-researcher` ("improvement queue lands in the close-out").

## Self-training mandate

"Close every session by noting one concrete way your agenda-setting could have been
sharper (misprioritization, wasted search budget, unclear delegation) — and apply the
prior session's note. Periodically research how strong research-team leads run standing
meetings and fold in what fits."

## Change log

- **2026-08-07** — Five session-protocol rules and one standing relay qualification, adopted
  2026-08-05 through 2026-08-07, recorded here for the first time: run-the-command-and-paste
  with its 08-07 qualification (`3ff5498`, `7adfd68`), open-the-line extended to every seat
  (`7adfd68`), grep-establishes-absence-from-the-repository-never-the-project (`aa48406`),
  truncate-never-round for elapsed intervals (`7adfd68`), the `[skip ci]` part-commit stopgap
  (`3ff5498`), and the entity-blind relay-null qualification (`aa48406`). Before this entry the
  protocol section ended at 2026-08-04, so a chairman reading its own seat note carried none of
  the six — including the rule its own accountability paragraph calls the fourth iteration of a
  lesson it keeps re-learning. Model unchanged (`claude-opus-5`, `CHAIRMAN_MODEL`); the
  definition changed once in the window, at `ae1f04b`, which rewrote the research question at
  `.claude/agents/council-chairman.md:31-32` — already recorded in [[Agent Registry]] and
  reflected in `STATE_OF_THE_ANSWER.md:5`, and re-verified identical in both today.
  *Audited against `7c08dcf`; paths: `.claude/agents/council-chairman.md`,
  `prompts/council_chairman.txt`, `prompts/council_reconvene.txt`,
  `prompts/council_calibration.md`, `analytics/daily-research/`,
  `views/isds-workflow-3d/workflow.json`.*
- **2026-08-04** — Four session-protocol rules adopted 2026-08-01 through 2026-08-04 recorded
  here for the first time: the standing-conventions block (`4d5c562`), probe-the-instruments
  (`8756859`), an-objection-is-a-claim (`1109993`), and quote-the-whole-line (`51bb7a2`).
  Before this entry the note's protocol section ended at 2026-07-31, so a chairman reading
  its own seat note carried none of the four. Model unchanged (`claude-opus-5`,
  `CHAIRMAN_MODEL`); definition unchanged since `939deaa`.
  *Audited against `b76f6c3`; paths: `.claude/agents/council-chairman.md`,
  `prompts/council_chairman.txt`, `prompts/council_reconvene.txt`,
  `prompts/council_calibration.md`, `analytics/daily-research/`,
  `analytics/council-sessions/`, `src/models.py`.*
- **2026-07-31** — Adopted session protocol recorded: return-path protocol and spend
  checkpoint (`de7b0fc`, checkpoint commit `15c8131`) and the name-the-latest-refinement
  delegation rule (`f03a90e`). The 2026-07-31 session was the first in which every seat sat
  and returned, run manually on the operator's standing order after the scheduled routine
  did not fire (`analytics/daily-research/2026-07-31.md`, procedural caveat). Model,
  definition, and prompt contract unchanged: `.claude/agents/council-chairman.md` still
  declares `model: fable` against `CHAIRMAN_MODEL = "claude-fable-5"` in `src/models.py`,
  and no commit touched `.claude/agents/` or `prompts/` between `ede0f32` and `e153ce3`.
  Threads this seat directs: [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1` ("feat(agents): complete trained council roster
  — 7 expert agent definitions bound to their canonical prompts"). Chairman's
  `claude-fable-5` assignment is unchanged by `4f8f981`, which moved only the analyst.
  Roster and history: [[Agent Registry]] · [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
