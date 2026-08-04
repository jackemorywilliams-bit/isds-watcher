---
aliases: [Systems Designer]
tags: [agent, council]
hub: Council
---
# Systems Designer

**Role.** The council's builder — it designs and implements the instrument's machinery
(renderers, generators, validators, pipelines) deterministically, shipping every deliverable
with a guard that turns its known failure modes into build failures.

**Definition.** `.claude/agents/systems-designer.md`

**Model.** None declared. The definition's frontmatter carries no `model:` key, so this
agent inherits the invoking session's model; `src/models.py` assigns models to the
pipeline's LLM stages and does not cover this repository-side seat. Recorded as-is rather
than inferred.

> **Unresolved conflict, recorded not papered over.** Flowchart v3.0 (`21f0240`) gave this
> seat a card whose `meta` field reads "Model: Claude Fable 5"
> (`views/isds-workflow-3d/workflow.json`, node `systems-designer`). The definition declares
> no model at all. The chart therefore asserts an assignment no configuration file carries.
> Either the definition should declare `model: fable` or the card should say "inherits the
> invoking session" — but that is an operator decision about a project artifact, and the
> chart is a generated-alongside artifact this seat does not hand-edit. Escalated to Emory;
> the same conflict exists for [[site-experience]].

## Canonical training (binding)

This seat binds no `prompts/*.txt` contract. Its canon is the repository's own machinery
and the standing constraints its definition names:

1. The artifacts it owns — the generators, validators, and renderers under `scripts/` and
   `src/`, including the flowchart toolchain behind `views/isds-workflow-3d/`.
2. `src/models.py` — the standing model assignments it must honor.
3. The project's operating constraints: zero cost, and the polite-crawler rules (identify,
   honor robots.txt, never evade).

## Discipline highlights

- "Deterministic over clever: no fuzzy matching, no invention; every artifact must be
  regenerable from committed inputs, and second runs must be byte-identical."
- "Fail closed: every deliverable ships with a validator/guard that makes its known failure
  modes a BUILD failure, not a screenshot the operator has to send."
- "Evidence over memory: read the actual repo files before asserting how anything works."
- "The operator is Emory (never 'Jack' in artifacts); professor-facing outputs must be
  presentable to Dr. Ximena Benavides."
- "Commit in your worktree with a full explanatory message; never push."

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `systems-designer` (machine column, row 7), added by flowchart v3.0
  (`21f0240`) — "Builds the machinery: renderers, validators, pipelines — fail-closed,
  tested." It sits in the machine column because that is what it builds, not because it is a
  pipeline stage.
- Its one edge: `systems-designer → site-experience` ("designer builds artifacts the site
  agent publishes"). It has no inbound edge on the chart — it is fed by operator directives
  and council-identified defects, which the chart does not draw.
- The rest of the machine column is still the artifact of its work rather than its
  successor: `collect`, `skip-repeats`, `first-score`, `read-doc`, `ai-check`,
  `quality-bar`, plus `claim-gate` and `citation-check` in the Emory column, and the
  flowchart view itself.

## Self-training mandate

The definition states no explicit self-training clause. Its operative equivalent is the
fail-closed rule: each deliverable must arrive with the validator that would have caught
its own failure mode, so the guard set grows with every build. Recorded as the definition
stands — no mandate is invented here.

## Change log

- **2026-08-04** — Audited, no change to model, definition or prompt bindings; the currency query `git log 6a5cd2e..b76f6c3` returns no commit touching this seat's definition or prompts. Snapshot anchor added, applying the convention adopted 2026-08-03 to this note for the first time.
  *Audited against `b76f6c3`; paths: `.claude/agents/systems-designer.md`, `views/isds-workflow-3d/`, `tools/isds-workflow-3d/`, `scripts/build_graph.py`, `src/models.py`.*
- **2026-07-31** — Two drifts fixed. (1) The "no box" statement was stale: this seat gained
  the `systems-designer` box in flowchart v3.0 (`21f0240`), with the edge
  `systems-designer → site-experience`. (2) The card's "Model: Claude Fable 5" conflicts with
  a definition that declares no model; recorded above and escalated rather than resolved
  here. Machinery landed in this seat's domain since the last audit, all fail-closed as the
  contract requires: the chart's artifact machinery merged and regenerated for v3.0 with
  manifest-derived guard counts (`0942d3f`, whose message names "systems-designer artifact
  machinery"); the one-core / two-surface static workflow SVG — `tools/isds-workflow-3d/src/
  chart-core.mjs` as a pure module feeding both the vault renderer and the site/README SVG —
  with a freshness guard (`6ab7c05`); and the column-id `jack → emory` rename end to end
  with a fail-closed token guard (`c06d8c8`, raised by the site-experience review). Definition
  file itself unchanged. Threads: [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `a852b80` ("feat(agents): durable project agent definitions
  — systems-designer + site-experience"; identical content committed earlier as `1c885b2`
  on the flowchart branch), the commit that also unignored `.claude/agents/` so agent
  definitions became durable, tracked project artifacts. Roster and history:
  [[Agent Registry]] · [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
