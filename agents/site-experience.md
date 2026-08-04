---
aliases: [Site & Correspondence Experience]
tags: [agent, council]
hub: Council
---
# Site & Correspondence Experience

**Role.** Owns every surface a human actually reads — the professor-facing website, the
email renderings of the digest, brief, daily update, and Monday packet, and the README.

**Definition.** `.claude/agents/site-experience.md`

**Model.** `claude-opus-5` — declared `model: opus` in the definition since 2026-08-04,
on the operator's direct answer ("both are on opus… opus 5 for the version").
`src/models.py` still does not assign a model to this repository-side seat; the
frontmatter selects the Opus *tier*, and the version is the operator's recorded choice
rather than something the key itself pins.

> **Conflict RESOLVED 2026-08-04.** Flowchart v3.0 (`21f0240`) gave this seat a card whose
> `meta` field asserted a model — first "Claude Fable 5", later "Claude Opus 5" — while
> the definition declared none, so the chart asserted an assignment no configuration file
> carried. Escalated to Emory on 2026-07-31 and answered on 2026-08-04. The escalation is
> kept rather than deleted because the standing guard it produced is the point:
> `scripts/check_models.py` fails when a card names a model no definition declares, when a
> card names a model absent from `src/models.py` (the "Claude Fable 5" case), or when a
> vault note contradicts its card. The identical conflict for [[systems-designer]] is
> resolved the same way.

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

- Flowchart box: `site-experience` (machine column, row 8), added by flowchart v3.0
  (`21f0240`) — "Owns the professor-facing website, the emails and the README — every
  reader-facing surface."
- Its own edges: fed by `systems-designer` ("designer builds artifacts the site agent
  publishes"); feeds `website` ("site agent owns build_site.py + templates behind the public
  site").
- It still owns the entire deliverables column — `daily-email` ("Daily research email"),
  `digest-email` ("Weekly digest email"), `website` ("Public website"), `brief-email`
  ("Research brief email"), and `packet` ("Monday review packet") — which are fed by
  `quality-bar → digest-email`, `editor → brief-email`, `daily-researcher → daily-email`,
  and by `minutes`, `ledger`, `systems-researcher`, and `citation-check` into `packet`.
  `digest-email → website` ("site built from digest folders") remains the internal link, and
  past the last box sit Dr. Benavides and Emory.

## Self-training mandate

The definition states no explicit self-training clause. Its operative equivalent is the
sync guard: `scripts/check_site_sync.py` must pass on every change, so a hand-edited or
stale `docs/` is caught rather than discovered by a reader. Recorded as the definition
stands — no mandate is invented here.

## Change log

- **2026-08-04** — Audited, no change to model, definition or prompt bindings; the currency query `git log 6a5cd2e..b76f6c3` returns no commit touching this seat's definition or prompts. Snapshot anchor added, applying the convention adopted 2026-08-03 to this note for the first time.
  *Audited against `b76f6c3`; paths: `.claude/agents/site-experience.md`, `scripts/build_site.py`, `scripts/site_templates/`, `docs/`, `README.md`, `views/isds-workflow-3d/workflow.json`.*
- **2026-07-31** — Two drifts fixed. (1) The "no council box" statement was stale: this seat
  gained the `site-experience` box in flowchart v3.0 (`21f0240`), with edges from
  `systems-designer` and into `website`. (2) The card's "Model: Claude Fable 5" conflicts
  with a definition that declares no model; recorded above and escalated. Work on the
  reader-facing surfaces since the last audit: the workflow chart placed on the
  professor-facing site and the README (`665b3e7`), then this seat's **owner review** of that
  integration (`3f6a6f8`, merged `784bd01`) — architecture accepted, page surface brought to
  house standard, with the operator-name check performed explicitly ("every on-chart label
  and tooltip says Emory"). That review is what surfaced the internal `jack` column id the
  systems designer then renamed in `c06d8c8`. Definition file unchanged. Threads:
  [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `a852b80` ("feat(agents): durable project agent definitions
  — systems-designer + site-experience"; identical content committed earlier as `1c885b2`
  on the flowchart branch). Roster and history: [[Agent Registry]] · [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
