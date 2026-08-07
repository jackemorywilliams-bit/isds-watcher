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
3. `prompts/carrying_span_rule.md` — **the Carrying-Span Rule**,
   adopted by the council 2026-08-03 as amended, added to this seat's definition on
   2026-08-04. It binds every source this seat cites for a proposition, *including sources
   it supplies itself*, and — per R7 — its own returns and the daily research records, not
   only the memos. Write the proposition before opening the source; screen the whole text
   with at least one **rigid designator**; quote the words that carry it, with a pinpoint;
   if nothing carries it, take the exits in order (another document in the same matter
   first, drop last) and name the one taken. It does **not** bind the structured
   `candidate_claims`, which the pre-ledger verification system governs.
4. The living memory embedded in the prompt — `STATE_OF_THE_ANSWER.md` plus the newest
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
- **The carrying-span rule** — adopted 2026-08-03 in special session, and it binds this
  seat's own citations, not only the ones it reviews. Before opening a source, write the one
  sentence you are citing it for; screen the whole retrieved text for the proposition's
  operative terms including at least one rigid designator; then quote the **carrying span** —
  the source's own words that carry the proposition — into the entry, with a pinpoint. The
  load-bearing element is the carrying span, not the proposition-first step. Full adopted
  text: `analytics/council-sessions/2026-08-03-proposition-rule.md:1450` (R3, "final form"),
  committed in `56cbb75`. Recorded status in that same record: **adopted in text and
  unvalidated** — the session declined to record the rule as working against its own base
  rate (`:1617`, R8).
- **Relay method rules** — adopted 2026-08-04, binding on every seat, and this seat is the
  one that fires the batches. (1) Never choose as `find` a string the target page can
  generate from your own request URL — otherwise `find_matched` reports a property of the
  request. (2) Anchor on a neighbouring structural label and read the value out of the
  window. (3) State what makes a control negative before relying on it. (4) Treat a control
  block as uninterpreted until the positive control fires. Source:
  `analytics/daily-research/2026-08-04.md:761` (next steps, item 4), committed in `51bb7a2`.
  Rule (1) is this seat's own catch and was adopted into the integrity officer's taxonomy
  under the analyst's formulation as entry 23, *echoed-find / self-confirming query*.
- **No search-synthesis figures** — restated as a standing rule in the 2026-08-04 agenda: a
  search result set is evidence about an index, never about whether a document exists.
  Source: `analytics/daily-research/2026-08-04.md:50` (Task 3), committed in `8756859`.
Six more, adopted 2026-08-05 through 2026-08-07 and recorded here on 2026-08-07. Five of
them govern the relay, which is this seat's instrument:

- **`find` selects a position, not a proposition** — adopted 2026-08-05 as house rule 2, from
  this seat's own Part 2 §2.1. Request-echo and boilerplate-preemption are one defect with two
  faces. Before firing a row, answer: *is the first occurrence of this string in the
  tag-stripped body the occurrence I want?* Where the honest answer is "I cannot know", the row
  is written up as a **probe**, with what a miss would mean stated in advance. Source:
  `analytics/daily-research/2026-08-05.md:977`; `3ff5498`.
- **A mis-anchored row is not a null** — adopted 2026-08-05, house rule 4. A null says the page
  was asked and did not answer; a mis-anchored row says the question was never put. Recording
  the second as the first enters a false negative about a live source. Source:
  `analytics/daily-research/2026-08-05.md:979`; `3ff5498`.
- **A PDF row's `find_matched: false` is guaranteed by the content-type gate** and is never
  evidence of textual absence — demonstrated, not derived, at `2026-08-03-control.json`
  record 1. Adopted 2026-08-05, house rule 3; `3ff5498`.
- **A deliberately false URL is a control, not discovery** — adopted 2026-08-05, house rule 5.
  Source: `analytics/daily-research/2026-08-05.md:980`; `3ff5498`.
- **`find_matched` has three states, not two** — ruled 2026-08-07 on `0807-B5`: *found*,
  *looked and did not find*, and **asked nothing** (a row fired with `find: ""` records
  `false` having asked nothing). The third is not hypothetical — it is instantiated by the
  `978/zzz---zzz-bit-1900-` row, the single observation the whole 0804-B7 discharge rests on,
  and a future seat pooling on that field would read the discharge row as a null. Source:
  `analytics/daily-research/2026-08-07.md:1000`; `7adfd68`.
- **Every citation to a relay reduction carries the commit sha that holds it** — the integrity
  officer's taxonomy entry 25, adopted 2026-08-05 as house rule 1. A reduction is evidence; a
  path that can be rewritten is not a citation. Source:
  `analytics/daily-research/2026-08-05.md:976`; `3ff5498`.

Two council-wide rules adopted in the same window bind this seat and are stated in full in
[[council-chairman]]: **before acting on any instruction that names a file and a line, open
the line** (2026-08-07, extended from the chairman to every seat), and **a grep establishes
absence from the repository, never from the project** (2026-08-06). The first was adopted out
of `0807-B1`, which is against this seat: the memo quoted two formulations of the
identification caveat that no longer exist anywhere in `STATE_OF_THE_ANSWER.md`, carrying a
quotation forward without re-opening the file after the amendment its own predecessor had
procured. Candidate claim 4's `supporting_quote` was struck; its substance survives and must be
re-quoted against the current file before it enters any ledger.

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

- **2026-08-07** — Six method rules adopted 2026-08-05 through 2026-08-07 recorded here for the
  first time, five of them governing the relay this seat fires: find-selects-a-position,
  mis-anchored-is-not-a-null, the PDF content-type gate, false-URL-is-a-control, the three
  states of `find_matched`, and commit-pinned reduction citations (`3ff5498`, `7adfd68`). Until
  this entry the note's rules section ended at 2026-08-04, so a seat reading its own note before
  the 2026-08-07 session carried none of them — including the two whose absence produced
  `0807-B1` and `0807-B5` in that session. Model unchanged (`claude-opus-5`, `HEAVY_MODEL`);
  **the definition file has not changed since `bfc8ef6`** (2026-08-04). The seat's prompt did:
  `ae1f04b` rewrote Ring 3 at `prompts/research_analyst.txt:18` and left the sentence asserting
  both definitions, and **`9efafb0`** — not `373cce6`, which [[Agent Registry]] credited on
  2026-08-06 and which touches no file under `prompts/` — is the commit that repaired it.
  Corrected in the registry in this same change set.
  *Audited against `7c08dcf`; paths: `.claude/agents/research-analyst.md`,
  `prompts/research_analyst.txt`, `prompts/council_calibration.md`,
  `prompts/carrying_span_rule.md`, `analytics/daily-research/`, `analytics/council-sessions/`,
  `src/models.py`.*
- **2026-08-04** — Three method rules adopted since 2026-07-31 recorded here for the first
  time: the carrying-span rule (`56cbb75`), the four relay method rules (`51bb7a2`), and
  no-search-synthesis-figures (`8756859`). Until this entry the note's rules section ended at
  2026-07-31, so the seat's own note carried none of them. Model is `claude-opus-5`
  (`HEAVY_MODEL`), moved from `claude-fable-5` by operator directive in `939deaa`; the two
  dated entries below are left as written, because they were true of their dates.
  *Audited against `b76f6c3`; paths: `.claude/agents/research-analyst.md`,
  `prompts/research_analyst.txt`, `prompts/council_calibration.md`,
  `analytics/daily-research/`, `analytics/council-sessions/`, `src/models.py`.*
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
