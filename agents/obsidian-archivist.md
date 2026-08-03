---
aliases: [Obsidian Archivist]
tags: [agent, council]
hub: Council
---
# Obsidian Archivist

**Role.** The librarian-scholar of the vault — it keeps the project's memory palace
accurate and navigable, owning the per-agent notes, the agent registry, the project change
log, and the audits that catch drift between the vault and the repository's reality.

**Definition.** `.claude/agents/obsidian-archivist.md`

**Model.** `claude-opus-4-8` ("Claude Opus 4.8" in the definition's discipline block);
declared `model: opus`; corresponds to `UTILITY_MODEL` in `src/models.py`. (`src/models.py`
governs the pipeline's LLM stages; this seat is a repository-side agent assigned by its
definition.)

## Canonical training (binding)

This seat binds no `prompts/*.txt` contract — its canon is the vault itself and the craft
rules written into its definition:

1. The vault structure: the `moc/` hubs, the workflow flowchart
   (`moc/00 - Project Map.md` plus `views/isds-workflow-3d/`), `HANDOFF.md`, and the
   `agents/` memory area it owns.
2. `scripts/build_graph.py` — the hub-and-spoke mapping script that owns the managed
   `<!-- graph:auto start -->` blocks (idempotent; a second run is byte-identical; a
   four-link cap on outgoing non-hub links per spoke).
3. `scripts/build_site.py` — verified, not assumed: the public site is generated from
   `METHODOLOGY.md` and `digests/` only, so vault-internal notes such as these do not leak
   to the professor-facing surface.

## Discipline highlights

- "Accuracy over completeness-theater: every registry and changelog line cites its commit
  hash or file path. An entry you cannot source you do not write."
- "When ANY agent's prompt, model, or contract changes, the corresponding vault note and
  the registry update in the same change set — stale agent memory is a defect you own."
- "managed blocks stay regenerable and are never hand-edited; frontmatter/alias conventions
  respected; vault-internal metadata never leaks to the public site (build_site strips it —
  verify, don't assume)."
- "Emory is the operator (never 'Jack' in vault artifacts); professor-facing surfaces stay
  clean of internal jargon."

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- This seat has **no box** on the flowchart, by design: it is not a stage of the weekly run.
  It curates the vault in which the flowchart is rendered — `moc/00 - Project Map.md`
  embeds `views/isds-workflow-3d/` inside the managed `<!-- workflow-3d:start -->` block —
  and it maintains the notes every council box now links to.
- Fed by: the repository's own history (git log), the agent definitions under
  `.claude/agents/`, and the council's records under `analytics/`.
- Feeds: [[Agent Registry]] and [[Project Change Log]], and the drift escalations it raises
  to Emory.

## Self-training mandate

"Each deployment, audit one slice of the vault against the repo's reality (agents vs
registry, flowchart vs pipeline, HANDOFF vs workflows) and fix or escalate drift;
periodically research current Obsidian/PKM practice so the vault's organization stays
state-of-the-art."

**Audit slice, 2026-07-30 (this deployment).** Agents vs models. `src/models.py` sets
`HEAVY_MODEL = "claude-opus-5"` and `HANDOFF.md` records the analyst on `claude-opus-5`
(commit `4f8f981`), but `COUNCIL.md`'s "Model assignments" table still reads
"Heavy-reasoning sub-agents (research analyst, one-pager drafting) | `claude-opus-4-8`".
That row is stale relative to the single source of truth. Escalated to Emory rather than
edited here: `COUNCIL.md` is a project-facing document outside this note-building change
set. A second finding from the same pass — `scripts/build_graph.py` would now write managed
blocks into the agent definitions themselves — is recorded with its evidence in
[[Project Change Log]] under "Open drift, escalated not fixed"; `build_graph` was therefore
not run during this build.

## Change log

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`, which established this seat by operator order:
  "owns the vault as memory palace — per-agent notes, registry, change log, drift audits."
