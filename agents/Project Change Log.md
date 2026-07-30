---
aliases: [Project Change Log]
tags: [agent, council]
hub: Council
---
# Project Change Log

Dated entries for material changes to the project's agents, models, sources, workflow, and
vault. **Every line cites a commit hash.** Anything that cannot be cited is not written
here. Newest first; dates are commit dates on the `feat/agent-operations` line of history.

## 2026-07-30

- **Council roster completed — seven expert agent definitions.** Chairman, research
  analyst, integrity officer, analytics officer, systems researcher, research editor, and
  obsidian archivist became durable, invocable agents, each bound to its canonical prompt
  lineage, its operator-assigned model, and a standing self-training mandate. `16836d1`
  ("feat(agents): complete trained council roster — 7 expert agent definitions bound to
  their canonical prompts").
- **Workflow flowchart accepted and merged — PR #30.** Merge of
  `feat/isds-workflow-3d` into the main line, carrying the animated workflow flowchart, the
  Bing News source, the Google News retirement, and the analyst's move to Fable 5.
  `0788e12` ("Merge pull request #30 from jackemorywilliams-bit/feat/isds-workflow-3d").

## 2026-07-29

- **First durable project agent definitions — systems designer and site experience.**
  `.claude/agents/` was unignored for exactly this purpose, making agent definitions
  tracked project artifacts rather than local settings. `a852b80` (identical content
  committed as `1c885b2` on the flowchart branch).
- **Research analyst promoted to Claude Fable 5.** Operator directive: the researcher
  requires the most advanced capabilities available. `HEAVY_MODEL` moved from
  `claude-opus-4-8` to `claude-fable-5` in `src/models.py`, mirrored in `HANDOFF.md` and on
  the flowchart's analyst card. Chairman stays Fable 5; editor and utility roles stay Opus
  4.8; the digest classifier is unchanged on Haiku. `4f8f981`.
- **Bing News in, Google News retired, press sources removed.** `bing_news` added as an
  approved lane with live-verified robots permission and eight fingerprint-derived queries;
  `google_news_rss` retired everywhere (source, registry, spec, HANDOFF, PLAN, README,
  METHODOLOGY, site); the Independent/Standard `press_business` sources removed after the
  operator's scope ruling that only presentation-approved lanes integrate. `b7d0925`.
- **Flowchart revisions v2.1 through v2.6.** v2.1, operator's seven revisions including
  "Emory, not Jack" enforced by the validator (`b7d0925`); v2.2, box-specific one-liners and
  named models on every agent card (`e4a0476`); v2.3, "Emory's ___" one-liners and the daily
  meeting on Fable 5 (`f3c3489`); v2.4, six gap-closing edges to meet the operator's
  "interconnected" standard (`21f3d16`); v2.5, port-routed arrows and the insight-cap
  correction (`03e5466`); v2.6, direction-true colors — council output purple, machine input
  blue (`d7f8f5c`).

## 2026-07-28

- **Workflow flowchart v2.** Plain language throughout, all sources plus the council and
  the deliverables represented, purpose-colored arrows. `cc1d556`.

## 2026-07-27

- **3D engine stripped; rebuilt as an animated swimlane flowchart.** A breaking change made
  on the council's audit verdict. `8a36d31`.
- **Deterministic 3D workflow view first shipped** (`dv.view` plus 3d-force-graph, fixed
  layout), then rescaled and reframed on council review. `bab8e23`, `c8a2587`, `7c5f3a3`.

## 2026-07-21

- **Vault graph frozen.** Dual-view topology applied, aliases and numbered hubs settled.
  `80ad250` ("feat(graph): final pass — apply dual-view topology, aliases, numbered hubs,
  freeze").

## 2026-07-18

- **The vault's mapping machinery created.** `scripts/build_graph.py` plus the curated
  `moc/` hubs — hub-and-spoke, managed blocks, idempotent. `b87c838`.

## Open drift, escalated not fixed

- **`COUNCIL.md` model table is stale.** Its "Model assignments" row still reads
  "Heavy-reasoning sub-agents (research analyst, one-pager drafting) | `claude-opus-4-8`",
  while `src/models.py` and `HANDOFF.md` record the analyst on `claude-fable-5` as of
  `4f8f981`. Raised for Emory's decision; not edited as part of the vault build.
- **`build_graph.py` would now write into the agent definitions.** Unignoring
  `.claude/agents/` (`a852b80`: `.claude/*` with `!.claude/agents/`) brought nine agent
  definition files inside `scripts/build_graph.py`'s scan boundary. A `build_graph` run
  would append a managed `Map: [[Council]]` block to each one — vault markup injected into
  the prompts those agents are trained on. `--dry-run` on 2026-07-30 lists all nine under
  "planned edits". The narrow fix is to add `.claude` to `EXCLUDE_DIRS` in
  `scripts/build_graph.py`, with a test; that is machinery work, so it is escalated rather
  than done here, and `build_graph` was deliberately **not** run during this build. The
  consequence to know: the notes in `agents/` carry no managed block yet, by design.

Roster: [[Agent Registry]].
