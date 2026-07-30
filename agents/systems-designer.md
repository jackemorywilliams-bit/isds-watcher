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

- This seat has **no box** on the flowchart: it is not a stage of the weekly run. It builds
  the stages. The machine-column boxes are the artifacts of its work — `collect`,
  `skip-repeats`, `first-score`, `read-doc`, `ai-check`, `quality-bar` — as are the
  automatic checks in the Emory column, `claim-gate` and `citation-check`, and the flowchart
  view itself.
- Fed by: operator directives and council-identified defects.
- Feeds: the committed machinery every other agent's box runs on.

## Self-training mandate

The definition states no explicit self-training clause. Its operative equivalent is the
fail-closed rule: each deliverable must arrive with the validator that would have caught
its own failure mode, so the guard set grows with every build. Recorded as the definition
stands — no mandate is invented here.

## Change log

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `a852b80` ("feat(agents): durable project agent definitions
  — systems-designer + site-experience"; identical content committed earlier as `1c885b2`
  on the flowchart branch), the commit that also unignored `.claude/agents/` so agent
  definitions became durable, tracked project artifacts. Roster and history:
  [[Agent Registry]] · [[Project Change Log]].
