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

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1` ("feat(agents): complete trained council roster
  — 7 expert agent definitions bound to their canonical prompts"). Chairman's
  `claude-fable-5` assignment is unchanged by `4f8f981`, which moved only the analyst.
  Roster and history: [[Agent Registry]] · [[Project Change Log]].
