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

## Roster

| Agent | Model | Canonical prompts | Definition | Vault note |
|---|---|---|---|---|
| Council chairman | `claude-opus-5` (`CHAIRMAN_MODEL`) | `prompts/council_chairman.txt`, `prompts/council_reconvene.txt`, `prompts/council_calibration.md` | `.claude/agents/council-chairman.md` | [[council-chairman]] |
| Research analyst | `claude-opus-5` (`HEAVY_MODEL`) | `prompts/research_analyst.txt`, `prompts/council_calibration.md` | `.claude/agents/research-analyst.md` | [[research-analyst]] |
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

## Flowchart boxes → notes

Every box in the council column of `views/isds-workflow-3d/workflow.json`, and the two
automatic checks, now resolve to a real note. Boxes owned by no single agent say so.

| Box (`workflow.json` id) | Column | Resolves to |
|---|---|---|
| `chairman` | council | [[council-chairman]] |
| `minutes` | council | [[council-chairman]] — the reconvene output of the same seat (`prompts/council_reconvene.txt`) |
| `analyst` | council | [[research-analyst]] |
| `daily-researcher` | council | [[research-analyst]] — the substantive seat in the daily Claude Max routine, which convenes the full council |
| `systems-researcher` | council | [[systems-researcher]] |
| `editor` | council | [[research-editor]] |
| `next-week` | council | No single owner: the living-memory files (`STATE_OF_THE_ANSWER.md`, `analytics/insights.jsonl`, `src/research_state.py`) written by the analyst and the chairman's minutes |
| `claim-gate`, `citation-check` | Emory checks | [[integrity-officer]] — the deterministic half of that function (`src/integrity_gate.py`, `scripts/check_citations.py`) |
| machine column (`collect` … `quality-bar`) | machine | [[systems-designer]] — code, not an agent seat; `ai-check` runs the digest classifier on Haiku 4.5 |
| deliverables column (`daily-email` … `packet`) | deliverables | [[site-experience]] |
| `emory-checks`, `ledger` | Emory checks | Emory — human judgment and the append-only ledger; no agent owns these |

Two seats have no box at all, and that is by design: the analytics officer reads the
machine column's `meta.json` output and speaks in the council's dialogue, and the archivist
curates the vault in which this flowchart is rendered.

## Graph note

This is an index note. Its outgoing links exceed the four-link cap for spokes in
`scripts/build_graph.py` (`MAX_DIRECT_LINKS_PER_NOTE`), so a `build_graph` run prints one
WARN naming this file. That is expected for a roster and is recorded here so the warning is
never mistaken for drift.

## Maintenance

When any agent's prompt, model, or contract changes, this table and the corresponding note
change in the same commit, and the change is dated and cited in [[Project Change Log]].

## Change log

- **2026-07-30** — Registry created with all nine agents, in the vault's inaugural
  agent-memory build. Sources: `16836d1` (seven council definitions) and `a852b80`
  (systems-designer, site-experience).
