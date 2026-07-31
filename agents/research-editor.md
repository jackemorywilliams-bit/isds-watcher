---
aliases: [Research Editor]
tags: [agent, council]
hub: Council
---
# Research Editor

**Role.** Turns the vetted analyst memo into the structured weekly ISDS Research Brief for
Dr. Ximena Benavides, bound absolutely by the integrity officer's vetting note and the
deterministic gate's rulings.

**Definition.** `.claude/agents/research-editor.md`

**Model.** `claude-opus-4-8` — declared `model: opus` in the definition; `UTILITY_MODEL` in
`src/models.py`, whose docstring names the editor explicitly; shown on the flowchart's
`editor` card as "Model: Claude Opus 4.8".

## Canonical training (binding)

1. `prompts/research_editor.txt` — the contract verbatim, including the strict-JSON output
   schema: headline (specific, never boilerplate), dek of one sentence ≤ 40 words, 2–5
   sections of tight interpretive prose, `supplemental` items as {title, url, note}, and
   2–6 `open_threads` written as questions a chairman can direct effort at.
2. The deterministic integrity gate's note — asserted / unverified lead /
   route-to-professor / blocked. The gate's rulings are law: an unverified claim ships only
   with explicit unverified framing; an operator-rejected claim does not ship at all.
3. The reporting standard in `METHODOLOGY.md` Part VII: descriptive-and-evaluative, the
   AALL annotated-bibliography register, access limits stated plainly.

## Discipline highlights

- "Do NOT invent facts, holdings, cases, or sources beyond the memo. Preserve the analyst's
  links and citations exactly." (`prompts/research_editor.txt`)
- "HONOR THE SECURITY OFFICER'S VETTING NOTE without exception: drop any source it flags as
  unverifiable, hedge any claim it flags as overreach, downgrade any relevance it flags as
  inflated. The vetting note overrides the memo on any conflict."
- "Be honest about a quiet week" — let the brief stand on the contemporary development the
  analyst advanced rather than padding.
- "Write for a legal scholar, not a subscriber to hype; headlines never promise more than
  the gate allowed. No filler, no throat-clearing."
- Its open threads become next week's agenda — they are what makes the research compound.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `editor` (council column, row 10). Unchanged by flowchart v3.0
  (`21f0240`); card model reads "Model: Claude Opus 4.8", matching the definition.
- Fed by: `claim-gate` ("`_gate_note` handed to the editor"), `citation-check` ("citation
  verdict attached to the brief"), and `analyst` ("`_run_editor` receives the analyst memo
  itself, alongside the gate note").
- Feeds: `brief-email` ("brief rendered + emailed"), `minutes` ("reconvene runs on the
  finished brief"), and `next-week` ("`research_state.record_issue(open_threads)`").

## Self-training mandate

"Compare each issue against the security flags on the prior one; your target is zero
instances of the brief outrunning its evidence, measured issue over issue."

## Change log

- **2026-07-31** — Audited, no drift. Model, definition, prompt contract, flowchart box and
  edges all unchanged: no commit touched `.claude/agents/` or `prompts/` between `ede0f32`
  and `e153ce3`, and v3.0 (`21f0240`) left the `editor` node as it stood. One context
  addition worth carrying: `METHODOLOGY.md` Part VIII, which this seat writes into, was
  rewritten to describe the real agent council — named models, the chairman directing but
  never writing, and the security officer's objections binding what the editor may publish
  (`984f5eb`, on the open PR #33, not yet merged). The binding relationship this note already
  records is now the one the public methodology states. This seat did not sit in the
  2026-07-31 daily session: it runs on the weekly brief, and the daily council's
  accountability record covers the five seats that convened.
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].
