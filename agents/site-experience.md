---
aliases: [Site & Correspondence Experience]
tags: [agent, council]
hub: Council
---
# Site & Correspondence Experience

**Role.** Owns every surface a human actually reads — the professor-facing website, the
email renderings of the digest, brief, daily update, and Monday packet, and the README.

**Definition.** `.claude/agents/site-experience.md`

**Model.** None declared. The definition's frontmatter carries no `model:` key, so this
agent inherits the invoking session's model; `src/models.py` does not assign a model to
this repository-side seat. Recorded as-is rather than inferred.

## Canonical training (binding)

This seat binds no `prompts/*.txt` contract. Its canon is the generated site's own
toolchain, named in its definition:

1. `scripts/build_site.py` plus `scripts/site_templates/` — the generator; `docs/` is its
   output, published to GitHub Pages.
2. `scripts/check_site_sync.py` — the guard that must pass after every change.
3. `src/render.py` and the small `_md_to_html` converters behind the digest, brief, daily,
   and packet emails; and `docs/assets/style.css` for the site's palette and typography.

## Discipline highlights

- "The site is a professor-facing academic surface for Dr. Ximena Benavides: clean, light,
  credible; match the existing palette and typography in `docs/assets/style.css`."
- "The site is GENERATED: every change goes through `scripts/build_site.py` and
  `site_templates/`, then `python scripts/check_site_sync.py` must pass — never hand-edit
  `docs/`."
- "Emails must render in plain email clients (the small `_md_to_html` converters); the
  README must render correctly on GitHub in BOTH light and dark themes."
- "The operator is Emory (never 'Jack' in artifacts). Zero-cost, no new services."
- "Commit in your worktree with a full explanatory message; never push."

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- This seat has **no council box**, but it owns the entire deliverables column — the boxes
  that carry the project to its readers: `daily-email` ("Daily research email"),
  `digest-email` ("Weekly digest email"), `website` ("Public website"), `brief-email`
  ("Research brief email"), and `packet` ("Monday review packet").
- Fed by: `quality-bar → digest-email`, `editor → brief-email`,
  `daily-researcher → daily-email`, and `minutes`, `ledger`, `systems-researcher`, and
  `citation-check` into `packet`.
- Feeds: `digest-email → website` ("site built from digest folders") — and, past the last
  box, Dr. Benavides and Emory.

## Self-training mandate

The definition states no explicit self-training clause. Its operative equivalent is the
sync guard: `scripts/check_site_sync.py` must pass on every change, so a hand-edited or
stale `docs/` is caught rather than discovered by a reader. Recorded as the definition
stands — no mandate is invented here.

## Change log

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `a852b80` ("feat(agents): durable project agent definitions
  — systems-designer + site-experience"; identical content committed earlier as `1c885b2`
  on the flowchart branch). Roster and history: [[Agent Registry]] · [[Project Change Log]].
