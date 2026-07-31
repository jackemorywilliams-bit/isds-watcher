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
   `graph:auto` blocks (idempotent; a second run is byte-identical; a four-link cap on
   outgoing non-hub links per spoke). **Never write that block's literal HTML start marker
   into a note** — see the hazard recorded in the 2026-07-31 audit slice below; name the
   convention, do not reproduce its delimiters.
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

- Flowchart box: `obsidian-archivist` (council column, row 14), added by flowchart v3.0
  (`21f0240`) — "Keeps the vault's memory current: agent registry, change log, drift
  audits." Card model reads "Model: Claude Opus 4.8", matching the definition.
- Its one edge: fed by `next-week` ("the archivist folds project changes into the vault's
  registry and change log"). It has no outbound edge on the chart, which is right — its
  output is the vault the chart is rendered in, not a downstream pipeline stage.
- Off-chart, it is also fed by the repository's own history (git log), the agent definitions
  under `.claude/agents/`, and the council's records under `analytics/`; and it feeds
  [[Agent Registry]], [[Project Change Log]], [[Workflow Threads]], and the drift
  escalations it raises to Emory.
- `moc/00 - Project Map.md` embeds `views/isds-workflow-3d/` inside the managed
  `<!-- workflow-3d:start -->` block; every role card's `target` is an Obsidian link text
  resolved by `dv.app.workspace.openLinkText` in `views/isds-workflow-3d/view.js`, which is
  why each `agents/<name>` note must exist under exactly that name.

## Self-training mandate

"Each deployment, audit one slice of the vault against the repo's reality (agents vs
registry, flowchart vs pipeline, HANDOFF vs workflows) and fix or escalate drift;
periodically research current Obsidian/PKM practice so the vault's organization stays
state-of-the-art."

**Audit slice, 2026-07-31.** Agents vs registry vs flowchart, plus the click-through check.
Findings, all fixed in this change set except where noted:

1. **Five notes claimed to have no flowchart box, and all five were wrong.** Flowchart v3.0
   (`21f0240`) put every one of the nine agents on the chart. `integrity-officer`,
   `analytics-officer`, `obsidian-archivist`, `systems-designer`, and `site-experience` all
   gained boxes with real edges (40 edges, 28 nodes in
   `views/isds-workflow-3d/workflow.json`). The registry's "two seats have no box at all"
   sentence was wrong for the same reason.
2. **Click-through check: all nine targets resolve.** Every `target` value of the form
   `agents/<name>` in `workflow.json` has a matching note under `agents/`. Card models match
   `src/models.py` and the definition frontmatter for the seven seats that declare a model.
3. **Model conflict on two cards, escalated not resolved.** The `systems-designer` and
   `site-experience` cards read "Model: Claude Fable 5" while neither definition declares a
   `model:` key. The chart asserts an assignment no configuration file carries. Recorded in
   both notes; Emory's call, and the chart is not hand-edited to make the problem disappear.
4. **Both drifts escalated on 2026-07-30 are now closed** by `807666f` — `COUNCIL.md`'s model
   row corrected to `claude-fable-5`, and `.claude` added to `EXCLUDE_DIRS` in
   `scripts/build_graph.py`. A `--dry-run` on 2026-07-31 confirms `.claude` is out of the
   scan boundary and no agent definition appears in the planned edits. The "Open drift,
   escalated not fixed" section of [[Project Change Log]] has been corrected accordingly.
5. **Adopted method rules were nowhere in agent memory.** The fetch-first and
   docket-page-first rules, the positive-control rule, the four new taxonomy entries, and the
   chairman's three session-protocol rules all existed only in the daily records. Each is now
   in the owning seat's note with its commit.
6. **HAZARD, found by running `build_graph` and escalated: a note that quotes the managed
   block's start marker destroys itself on the second run.** `scripts/build_graph.py:195`
   builds its replacement pattern as
   `re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END)` under `re.DOTALL`, which matches
   from the **first** occurrence of the start marker anywhere in the file — including one
   sitting harmlessly inside backticks in prose. Run 1 appends a real block at the end of the
   note; run 2 then matches the prose marker as the opening delimiter and the real block as
   the closing one, and deletes everything in between. This note was the only file in the
   vault that quoted the marker, being the note that documents the convention, and it lost 92
   lines on the second run before being restored from `689a9e7`. Two consequences: the prose
   above no longer reproduces the delimiters, and the idempotence guarantee the vault relies
   on ("a second run is byte-identical") is **conditional** on no note ever quoting the start
   marker. The narrow fix is machinery, so it is escalated rather than done here — anchor the
   pattern to the last start marker, or skip markers inside code spans and fences (the module
   already compiles `_CODE_FENCE`), or fail loudly on a duplicate start marker rather than
   silently spanning it. Verified after the fix: two consecutive `build_graph` runs now leave
   the tree byte-identical.

**Audit slice, 2026-07-30.** Agents vs models. `src/models.py` sets
`HEAVY_MODEL = "claude-fable-5"` and `HANDOFF.md` records the analyst on `claude-fable-5`
(commit `4f8f981`), but `COUNCIL.md`'s "Model assignments" table still reads
"Heavy-reasoning sub-agents (research analyst, one-pager drafting) | `claude-opus-4-8`".
That row is stale relative to the single source of truth. Escalated to Emory rather than
edited here: `COUNCIL.md` is a project-facing document outside this note-building change
set. A second finding from the same pass — `scripts/build_graph.py` would now write managed
blocks into the agent definitions themselves — was recorded with its evidence in
[[Project Change Log]]; `build_graph` was therefore not run during that build. *Both
findings were fixed the same day by `807666f`; see item 4 of the 2026-07-31 slice above.*

## Change log

- **2026-07-31** — Second deployment, by operator directive: linearize the vault's threads
  and verify every agent's recorded context. Own drift fixed: the "no box" statement was
  stale after flowchart v3.0 (`21f0240`), which gave this seat the `obsidian-archivist` box
  and the `next-week → obsidian-archivist` edge. Added [[Workflow Threads]] — every open
  thread as one linear chain with its owner. Both 2026-07-30 escalations confirmed closed by
  `807666f`. Model and definition unchanged (`model: opus`).
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`, which established this seat by operator order:
  "owns the vault as memory palace — per-agent notes, registry, change log, drift audits."

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
