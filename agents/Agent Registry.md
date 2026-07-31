---
aliases: [Agent Registry]
tags: [agent, council]
hub: Council
---
# Agent Registry

The roster at a glance: every durable agent definition in `.claude/agents/`, the model it
runs on, the canonical prompt files it binds, and its vault note. Nine agents, all
established on or before 2026-07-30 (`a852b80`, `16836d1`).

Model ids are the ones in `src/models.py` — the single model-configuration location — read
together with each definition's frontmatter. Where a definition declares no model, that is
recorded as "none declared" rather than inferred.

Open work by thread and owner: [[Workflow Threads]]. Dated history: [[Project Change Log]].

**Definitions audited 2026-07-31 and unchanged since the registry was created:**
`git log ede0f32..e153ce3 -- .claude/agents/ prompts/` returns no commits, so every model,
contract, and prompt binding in the table below still reads as committed. What *did* change
is each seat's working context — the method rules the council adopted in session — and the
flowchart, which now carries a card for all nine seats.

## Roster

| Agent | Model | Canonical prompts | Definition | Vault note |
|---|---|---|---|---|
| Council chairman | `claude-fable-5` (`CHAIRMAN_MODEL`) | `prompts/council_chairman.txt`, `prompts/council_reconvene.txt`, `prompts/council_calibration.md` | `.claude/agents/council-chairman.md` | [[council-chairman]] |
| Research analyst | `claude-fable-5` (`HEAVY_MODEL`) | `prompts/research_analyst.txt`, `prompts/council_calibration.md` | `.claude/agents/research-analyst.md` | [[research-analyst]] |
| Integrity officer | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/council_security.txt`, `prompts/council_calibration.md` | `.claude/agents/integrity-officer.md` | [[integrity-officer]] |
| Analytics officer | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/council_roundtable.txt`, `prompts/daily_council_protocol.md` | `.claude/agents/analytics-officer.md` | [[analytics-officer]] |
| Systems researcher | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/systems_researcher.txt` | `.claude/agents/systems-researcher.md` | [[systems-researcher]] |
| Research editor | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/research_editor.txt` | `.claude/agents/research-editor.md` | [[research-editor]] |
| Obsidian archivist | `claude-opus-4-8` | none — canon is the vault, `scripts/build_graph.py`, `scripts/build_site.py` | `.claude/agents/obsidian-archivist.md` | [[obsidian-archivist]] |
| Systems designer | none declared — inherits the invoking session | none — canon is the repository's machinery and `src/models.py` | `.claude/agents/systems-designer.md` | [[systems-designer]] |
| Site & correspondence experience | none declared — inherits the invoking session | none — canon is `scripts/build_site.py`, `site_templates/`, `src/render.py` | `.claude/agents/site-experience.md` | [[site-experience]] |

Not an agent, but bound by the same model config: the digest classifier runs on
`claude-haiku-4-5-20251001` (`DIGEST_CLASSIFIER_MODEL`, read by `src/classify.py`), and the
runtime-fallback rule requires any REQUESTED-vs-ACTUAL discrepancy to be written into
`HANDOFF.md` rather than silently substituted.

## Flowchart cards → notes (click-through map)

As of flowchart **v3.0** (`21f0240`, "all nine subagents on the chart, cards link to their
vault training notes"), every one of the nine agents has its own card. Each role card's
`target` is an Obsidian link text that `views/isds-workflow-3d/view.js` hands to
`dv.app.workspace.openLinkText`, so `target: "agents/<name>"` must match a note filename
exactly. **All nine resolve** — verified 2026-07-31 against
`views/isds-workflow-3d/workflow.json` (28 nodes, 40 edges).

| Card (`workflow.json` id) | Column · row | `target` | Card model | Note |
|---|---|---|---|---|
| `chairman` | council · 7 | `agents/council-chairman` | Claude Fable 5 | [[council-chairman]] |
| `minutes` | council · 11 | `agents/council-chairman` | Claude Fable 5 | [[council-chairman]] — the reconvene output of the same seat |
| `analyst` | council · 8 | `agents/research-analyst` | Claude Fable 5 | [[research-analyst]] |
| `systems-researcher` | council · 9 | `agents/systems-researcher` | Claude Opus 4.8 | [[systems-researcher]] |
| `editor` | council · 10 | `agents/research-editor` | Claude Opus 4.8 | [[research-editor]] |
| `analytics-officer` | council · 12 | `agents/analytics-officer` | Claude Opus 4.8 | [[analytics-officer]] |
| `obsidian-archivist` | council · 14 | `agents/obsidian-archivist` | Claude Opus 4.8 | [[obsidian-archivist]] |
| `integrity-officer` | Emory checks · 11 | `agents/integrity-officer` | Claude Opus 4.8 | [[integrity-officer]] |
| `systems-designer` | machine · 7 | `agents/systems-designer` | Claude Fable 5 ⚠ | [[systems-designer]] |
| `site-experience` | machine · 8 | `agents/site-experience` | Claude Fable 5 ⚠ | [[site-experience]] |

⚠ **Card asserts a model no configuration file carries.** Neither
`.claude/agents/systems-designer.md` nor `.claude/agents/site-experience.md` declares a
`model:` key, and `src/models.py` does not cover repository-side seats — yet both cards read
"Model: Claude Fable 5". Escalated to Emory; the resolution is either a `model: fable` line
in each definition or a card that says "inherits the invoking session". The chart is not
hand-edited to make the discrepancy disappear.

Non-agent cards, unchanged:

| Card | Column | Resolves to |
|---|---|---|
| `daily-researcher` | council | `COUNCIL.md` — the daily routine that convenes the full council; the substantive seat in it is [[research-analyst]] |
| `next-week` | council | `STATE_OF_THE_ANSWER.md` — no single owner: the living-memory files written by the analyst and the chairman's minutes |
| `claim-gate`, `citation-check` | Emory checks | The deterministic half of the verification function (`src/integrity_gate.py`, `scripts/check_citations.py`); the judgment half is [[integrity-officer]] |
| `collect` … `quality-bar` | machine | Code, not agent seats — built by [[systems-designer]]; `ai-check` runs the digest classifier on Haiku 4.5 |
| `daily-email` … `packet` | deliverables | Owned by [[site-experience]] |
| `emory-checks`, `ledger` | Emory checks | Emory — human judgment and the append-only ledger; no agent owns these |

## Graph note

This is an index note. Its outgoing links exceed the four-link cap for spokes in
`scripts/build_graph.py` (`MAX_DIRECT_LINKS_PER_NOTE`), so a `build_graph` run prints one
WARN naming this file. That is expected for a roster and is recorded here so the warning is
never mistaken for drift.

As of 2026-07-31 a `build_graph` run prints **two** WARNs from this area — this note (11
direct links) and [[Workflow Threads]] (9). Both are index notes and both are expected; the
cap exists to keep ordinary spokes from becoming hubs, which is not what these are. A third
WARN, `think-tank/multi-agent/_MOC.md`, predates the agent-memory area. Any WARN naming a
per-agent note *would* be drift, and there are none.

The notes under `agents/` carry their managed `Map:` blocks as of 2026-07-31, when
`build_graph` was first run over this area after the `807666f` scan-boundary fix. Those
blocks are generated: they are never hand-edited, and a run must leave them byte-identical.

## Maintenance

When any agent's prompt, model, or contract changes, this table and the corresponding note
change in the same commit, and the change is dated and cited in [[Project Change Log]].

## Adopted method rules by seat

Rules the council adopted in session that are now part of a seat's working context. Full
statements live in the seat's own note.

| Seat | Rule | Adopted | Commit |
|---|---|---|---|
| [[research-analyst]] | Fetch-first — attempt the direct fetch before reconstructing from search results | 2026-07-30 | `754ce32` (re-sequenced `e05f834`) |
| [[research-analyst]] | Docket page before document hunt — for any ICSID question, fetch the case-detail page first | 2026-07-31 | `f03a90e` |
| [[integrity-officer]] | Positive control before any HTTP-status objection | 2026-07-31 | `15c8131` |
| [[integrity-officer]] | Fabrication taxonomy extended from six entries to ten | 2026-07-31 | `15c8131` |
| [[council-chairman]] | Member return-path protocol (SendMessage to launcher; route via "main" on bounce) | 2026-07-30, first applied 07-31 | `de7b0fc` |
| [[council-chairman]] | Spend checkpoint immediately after the vetting round | 2026-07-30, first applied 07-31 | `de7b0fc` / `15c8131` |
| [[council-chairman]] | Name the proposition's latest dated refinement when delegating | 2026-07-31 | `f03a90e` |

## Change log

- **2026-07-31** — Registry audited against `.claude/agents/`, `src/models.py`, and
  `views/isds-workflow-3d/workflow.json`. Definitions unchanged (`ede0f32..e153ce3` touches
  neither `.claude/agents/` nor `prompts/`). Two corrections: the flowchart mapping was
  rewritten for **v3.0** (`21f0240`), which gave all nine seats a card and made the previous
  "two seats have no box at all" sentence wrong; and the model conflict on the
  `systems-designer` / `site-experience` cards is now recorded and escalated. Adopted method
  rules added by seat. Threads note added: [[Workflow Threads]].
- **2026-07-30** — Registry created with all nine agents, in the vault's inaugural
  agent-memory build. Sources: `16836d1` (seven council definitions) and `a852b80`
  (systems-designer, site-experience).

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
