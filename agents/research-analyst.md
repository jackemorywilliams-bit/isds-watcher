---
aliases: [Research Analyst]
tags: [agent, council]
hub: Council
---
# Research Analyst

**Role.** Interprets each session's screened items against the three-ring research
question, advances the carried open threads with strictly bounded web research, and
proposes evidence-cited candidate claims that only the operator's ledger may promote to
asserted fact.

**Definition.** `.claude/agents/research-analyst.md`

**Model.** `claude-opus-5` — `HEAVY_MODEL` in `src/models.py`; declared `model: opus` in
the definition; mirrored in `HANDOFF.md` and on the flowchart's `analyst` card ("Model:
Claude Opus 5"). Promoted from `claude-opus-4-8` by operator directive 2026-07-29
(commit `4f8f981`), on the ground that "the researcher requires the most thinking and the
most advanced capabilities available."

## Canonical training (binding)

1. `prompts/research_analyst.txt` — the full contract: interpret rather than list; advance
   the carried threads; bounded web search that builds on the daily researcher's notes;
   backsourcing from titles; the `candidate_claims` JSON contract; `GAP-UNRESOLVED` markers
   with stable slugs; the monitored-author standing check (Anthea Roberts); the cross-BIT
   consistency rule across the four in-scope China BITs.
2. [[council_calibration]] (`prompts/council_calibration.md`) — the anti-fabrication
   checklist in full.
3. The living memory embedded in the prompt — `STATE_OF_THE_ANSWER.md` plus the newest
   `analytics/insights.jsonl` entries — which is "the canonical baseline; never report it
   absent, never reconstruct it, never re-assert what it already records."

## Discipline highlights

- "a few well-chosen queries beat many" — web search "is NOT a general news channel and NOT
  a way to introduce unrelated material." (`prompts/research_analyst.txt`)
- BACKSOURCE FROM THE TITLE: a paywalled headline is a lead, and "never state the contents
  of a body you could not actually read."
- "A claim you cannot source you do not make; flag it as unverified." Every substantive
  claim carries an inline source (name + URL).
- Insights are uncapped but never padded: on a quiet day the honest output is "no new
  insight; standing watch" with a one-line note of what was checked; "a thin or absent
  nexus is reported honestly, never manufactured into a 'finding.'"
- It proposes only: "the operator-controlled verification ledger decides what may be
  asserted — you do not decide verification status, and any status you emit is ignored."
  Escalated gaps get zero search budget; absence is recorded as "not found in accessible
  sources", never as non-existence.

## Adopted method rules (session-derived, binding)

Rules the council adopted in session. They bind alongside the prompt contract, and they are
recorded here because they are now part of this seat's working context.

- **Fetch-first** — adopted 2026-07-30. Attempt the direct fetch before reconstructing a
  document from search results; fall back to quoted-phrase reconstruction only once a fetch
  has actually failed. A search snippet is never cited in place of a document an unattempted
  fetch would have produced. Source: `analytics/daily-research/2026-07-30.md`, close-out
  next steps 2–3, committed in `754ce32`; re-sequenced from "substitute" to
  "fallback-after-attempted-fetch" by the systems researcher's correction in
  `analytics/optimization-log.md` (`e05f834`).
- **Docket page before document hunt** — adopted 2026-07-31, extending fetch-first. For any
  ICSID case question, fetch the case-detail page before searching for or guessing document
  URLs; hunt blob URLs only for documents the docket actually lists. Source: the session
  method note in `analytics/daily-research/2026-07-31.md`, committed in `f03a90e`. In
  practice it collapsed a planned four-attempt blob hunt into two fetches and answered three
  questions at once.
- **Standing watch item.** Two consecutive sessions have paired this seat's strongest
  reasoning with the most binding objections, both times ledger-fidelity failures — reporting
  the favorable half of an operator mark (`quote_ok: true`) while omitting the adverse half
  (`scope_ok: false`). Named by the chairman as the seat's standing watch item in the
  2026-07-31 accountability record (`f03a90e`).

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `analyst` (council column). The daily-cadence counterpart box is
  `daily-researcher`, which runs the same substantive seat in the daily Claude Max routine.
- Fed by: `chairman` ("agenda passed to `_run_analyst`") and `daily-researcher`
  ("src/research_brief.py: `_daily_notes_block`").
- Feeds: `claim-gate` ("candidate_claims into integrity_gate"), `ledger` ("candidate_claims
  are recorded into the ledger as unverified claim_created events"), `citation-check`
  ("`_verify_citations` over the memo"), and `editor` ("`_run_editor` receives the analyst
  memo itself, alongside the gate note").

## Self-training mandate

"Track which query formulations actually produce findings (the 2026-07-26 lesson:
author-name+title beat keyword search) and record the session's method note; study one
primary award or doctrinal source in depth each week so your three-ring judgment keeps
sharpening beyond the seed corpus."

## Change log

- **2026-07-31** — Adopted method rules recorded: fetch-first (`754ce32`, re-sequenced in
  `e05f834`) and docket-page-before-document-hunt (`f03a90e`), plus the ledger-fidelity
  standing watch item from the same close-out. Model, definition, and prompt contract are
  unchanged — `git log ede0f32..e153ce3 -- .claude/agents/ prompts/` returns nothing, and
  `.claude/agents/research-analyst.md` still declares `model: fable` against
  `HEAVY_MODEL = "claude-fable-5"` in `src/models.py`. Open threads this seat owns:
  [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`, and the model promotion to `claude-fable-5`
  committed in `4f8f981` ("feat(models): research analyst promoted to Claude Fable 5
  (operator directive)"). Roster and history: [[Agent Registry]] · [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
