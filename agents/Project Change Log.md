---
aliases: [Project Change Log]
tags: [agent, council]
hub: Council
---
# Project Change Log

Dated entries for material changes to the project's agents, models, sources, workflow, and
vault. **Every line cites a commit hash.** Anything that cannot be cited is not written
here. Newest first; dates are commit dates on the mainline of history.

Roster: [[Agent Registry]]. Open work by thread and owner: [[Workflow Threads]].

## 2026-07-31

- **PR #32 merged to main.** `e153ce3` ("Merge pull request #32 from
  jackemorywilliams-bit/feat/agent-operations — council record 2026-07-30 (Part 5 + pending
  close-out) + workflow chart on site/README"). It carries every 2026-07-30 and 2026-07-31
  entry below that is not separately attributed to PR #23 or PR #31.
- **The 2026-07-31 council session — first fully-seated delegated meeting.** Recorded
  incrementally in four commits rather than one, which is the point: `de7b0fc` (Part 1
  agenda + first-application tracker adopted), `e05f834` (Parts 2, 4, 5 verbatim + the
  systems researcher's two optimization-log corrections), `15c8131` (Part 3 vetting note —
  the spend checkpoint, taken *as* a commit), `f03a90e` (Part 6 rulings and close-out written
  in-session, with the full ripple into `STATE_OF_THE_ANSWER.md`, `analytics/insights.jsonl`,
  `state/research_log.json` seq 36, `analytics/council-log.md`, and
  `analytics/optimization-log.md`). Record: `analytics/daily-research/2026-07-31.md`.
- **China–France BIT (2007) escalation CLOSED at provision level.** Open 23 sessions, closed
  on Emory's own verified action — ledger claim `da33a30be92ab234`, `operator_verified`
  2026-07-27: the UNCTAD IIA Mapping records ISDS forum options of domestic courts / ICSID /
  UNCITRAL, a fork-in-the-road relationship, and no mapped administrative-review or
  domestic-litigation prerequisite. The gap marker
  `china-france-bit-2007-protocol-exhaustion` is RETIRED. Two ordinary residuals opened in
  its place (Protocol text; China–Switzerland forum relationship). `f03a90e`.
- **Huawei v. Sweden (ICSID ARB/22/2) — pendency converted from inference to docket fact.**
  ICSID's case-detail page lists Procedural Orders 1–8 only, no PO 9 and no award; latest
  development July 10, 2025 (costs replies); registered January 21, 2022, so the 2006 Rules
  govern by default. Both costs rounds slipped from PO 8's schedule. The proposed
  `huawei-arb-22-2-rules-vintage` marker was NOT opened — substantially answered in vetting
  by ICSID's own citation of "ICSID Arbitration Rule 37(2)" for 2024 events. `f03a90e`.
- **Integrity officer's vetting FLAGGED — four binding objections, eight hedges, all
  accepted.** `15c8131` (the note) and `f03a90e` (the rulings). The officer also disclosed
  that its own first-pass 403 would have produced a false binding objection against a correct
  finding, caught only by a positive control.
- **Instrument finding: `uncitral.un.org` gates on user agent.** A 403 from that host carries
  **no** information about resource existence — under a default curl UA every path returns a
  919-byte CloudFront 403 regardless of existence, while a browser UA returns 200 or a genuine
  404. The project's standing "403-blocked" characterizations for that host are access
  artifacts. Consequence: the `sps.pdf` two-paths item is CLOSED as an access artifact, and a
  bounded UA-controlled re-audit of the record's 403 items is queued to the analyst.
  `15c8131`, ruled `f03a90e`.
- **Fabrication taxonomy extended from six entries to ten** — tool-status-as-source-state,
  summarizer-render-as-full-access, selective-flag reporting, superseded-formulation
  restatement. The last of these became the chairman's delegation rule the same day.
  `15c8131`.
- **Systems researcher first seated.** Three-item queue fully discharged: the
  `scripts/source_analytics.py` same-window patch diagnosed, patched and tested but **not
  applied** (edits to `scripts/` are gated on Emory's sign-off); two optimization-log
  corrections applied (`e05f834`); one new dedup-checked proposal, a `Health` column in the
  receptivity report, status *proposed* (`f03a90e`).
- **First-application tracker ADOPTED.** Monthly cadence, analyst executes, next cycle late
  August 2026, against the officer-verified baseline of ICSID's manifest-lack-of-merit
  decisions table. Recorded in `analytics/optimization-log.md`; `de7b0fc`.
- **Workflow chart column id `jack` → `emory`, end to end.** 25 `wf-*-col-jack` class
  occurrences in the generated SVG, `"col": "jack"` on five manifest nodes, the
  `meta.columns` vocabulary, and the node id `jack-checks` — all renamed, with a fail-closed
  token guard so the internal name cannot come back. Raised by the site-experience owner
  review. `c06d8c8`.
- **How-it-works page brought to house standard — site-experience owner review.** Review of
  the workflow-chart integration shipped in `665b3e7`: architecture accepted, page surface
  fixed, and the operator-name check performed explicitly ("every on-chart label and tooltip
  says Emory"). `3f6a6f8`, merged `784bd01`.
- **The vault's managed blocks regenerated across `agents/` for the first time.** With the
  `807666f` scan-boundary fix in place, `scripts/build_graph.py` was run over the vault: 99
  notes in scope, 201 edges, 0 orphans, 33 files receiving their managed `Map:` block —
  including all twelve notes under `agents/`, which had carried none since the area was
  created. `.claude` is confirmed outside the scan boundary, so no agent definition was
  touched. Verified afterwards: two consecutive runs leave all 123 markdown files
  byte-identical, `scripts/check_site_sync.py` passes, and no managed markup appears anywhere
  under `docs/`.
- **HAZARD found by that run, and escalated: quoting the managed block's start marker in a
  note destroys the note.** `scripts/build_graph.py:195` matches from the **first** start
  marker in a file to the first following end marker, under `re.DOTALL`. A note that quotes
  the marker in prose therefore survives run 1 (which appends a real block at the end) and is
  gutted by run 2, which treats the prose marker as the opening delimiter. `agents/
  obsidian-archivist.md` — the one note that documents the convention — lost 92 lines this
  way and was restored from `689a9e7`. The prose no longer reproduces the delimiters, so the
  vault is safe today, but the guarantee the vault relies on ("a second run is
  byte-identical") is **conditional on no note ever quoting the start marker**, which is a
  fragile guarantee for a convention every archivist is expected to document. Machinery fix
  escalated, not done here.
- **METHODOLOGY Parts III and VIII revised — on the open PR #33, not yet merged.**
  `984f5eb` ("docs(methodology): close source + council gaps surgically"), branch
  `feat/methodology-source-council-sync`. Part III's live-source list gains the PCA press
  page and Bing News (eight fixed fingerprint-derived queries, deduplicated across queries)
  and adds both to the full-read tier. Part VIII now describes the real agent council rather
  than "predetermined stages": separately running agents on named models — chairman and
  research analyst on Claude Fable 5, remaining seats on Claude Opus 4.8 — convened daily by
  a chairman who directs but never writes any member's contribution, with a security officer
  whose objections bind what the editor may publish. Recorded here as pending, and it is the
  first professor-facing surface to state the council as it actually runs.

## 2026-08-03

- **Chairman and research analyst moved from Claude Fable 5 to Claude Opus 5.** Operator
  directive: the Fable 5 credit balance is exhausted, so both top seats move to Opus 5.
  Applied in `src/models.py` (`CHAIRMAN_MODEL` and `HEAVY_MODEL` now `claude-opus-5`), the
  two agent definitions' `model:` keys (`.claude/agents/council-chairman.md`,
  `.claude/agents/research-analyst.md`), the six flowchart cards in
  `views/isds-workflow-3d/workflow.json`, `COUNCIL.md`, `HANDOFF.md`, `METHODOLOGY.md`
  Part VIII, and this vault's registry and per-agent notes. The other seats are unchanged
  on Opus 4.8. The dated history above is left as written — the July 29 promotion to
  Fable 5 happened and stays recorded.

## 2026-07-30

- **Both drifts this log escalated were fixed the same day.** `807666f` ("fix: archivist's
  two escalated drifts — COUNCIL.md model row + build_graph scan boundary"): `COUNCIL.md`'s
  model table corrected to `claude-fable-5` for the research analyst (one-pager drafting
  stays Opus 4.8), and `.claude` added to `EXCLUDE_DIRS` in `scripts/build_graph.py` so the
  agent definitions can never receive an injected managed block. Suite 122 passed + 4
  xfailed. Verified 2026-07-31: `COUNCIL.md`'s "Model assignments" row now reads
  "Heavy-reasoning sub-agents (research analyst) | `claude-fable-5` (operator directive
  2026-07-29…)", and a `build_graph --dry-run` lists `.claude` among the excluded dirs with
  no agent definition in the planned edits.
- **Flowchart v3.0 — all nine subagents on the chart.** Every agent seat gained a card, and
  each role card's `target` is the vault training note for that seat, opened through
  `dv.app.workspace.openLinkText`. `21f0240`. Regenerated with the artifact machinery and
  manifest-derived guard counts in `0942d3f`.
- **One chart core, two surfaces.** The entire chart construction — geometry, port
  allocation, text wrapping, edge paths, SMIL dot timing, legend — extracted into a pure
  module (`tools/isds-workflow-3d/src/chart-core.mjs`) that feeds both the Obsidian renderer
  and a standalone SVG for the professor-facing site and the README, behind a fail-closed
  freshness guard. `6ab7c05`.
- **Silent-decay source-health guard merged — PR #23.** `8178f1f` (merge) carrying `e31e0c6`
  ("fix(sources): repair the collection layer and end silent source decay"), which added
  `src/source_health.py` plus `tests/test_source_health.py` and `tests/test_source_fixtures.py`.
  Per-source consecutive-zero-run tracking persisted in `state/source_health.json`; a source
  documented as ACTIVE that hits three consecutive zero runs is reported `DEGRADED (N zero
  runs)` in `meta.json`, the digest README and the digest header; an all-but-one-zero run
  raises `COLLECTION ANOMALY`. Nothing in it ever raises. *Correction to the operator's
  briefing: this reached main through PR #23, not PR #32.* The guard has not yet run live —
  `state/source_health.json` does not exist, and the newest archived run is
  `digests/2026-07-27_ISDS-Thematic-Watch`, whose `meta.json` carries a `source_health` table
  with no streak data. First live run: the next weekly cron, 2026-08-03
  (`.github/workflows/weekly.yml`, `cron: "0 13 * * 1"`).
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

## Open drift

Nothing here is a to-do list for an agent: these are discrepancies between two repository
artifacts that only Emory can settle. Threads with a named agent owner live in
[[Workflow Threads]].

- **Two flowchart cards assert a model no configuration file carries.** The
  `systems-designer` and `site-experience` cards in `views/isds-workflow-3d/workflow.json`
  read "Model: Claude Fable 5" (`21f0240`), while neither `.claude/agents/systems-designer.md`
  nor `.claude/agents/site-experience.md` declares a `model:` key, and `src/models.py` covers
  only the pipeline's LLM stages. Resolution is either a `model: fable` line in each
  definition or a card reading "inherits the invoking session" — an operator call. Raised
  2026-07-31; recorded in [[systems-designer]], [[site-experience]] and [[Agent Registry]].
  The generated chart is not hand-edited to hide it.
- **`build_graph`'s block replacement spans a prose-quoted start marker.**
  `scripts/build_graph.py:195` anchors to the first start marker in the file rather than the
  managed one, so any note quoting that marker is gutted on the second run. Demonstrated and
  contained on 2026-07-31 (see the entry above); the vault is safe only because no note now
  quotes it. Narrow fixes, any one of which closes it: anchor to the **last** start marker,
  skip markers inside code spans and fences (`_CODE_FENCE` is already compiled in the
  module), or fail loudly on a duplicate start marker instead of silently spanning it. Wants
  a regression test with a note that quotes the marker. Machinery work — [[systems-designer]]
  on Emory's go-ahead.

### Closed

- **`COUNCIL.md` model table stale** — raised 2026-07-30, **fixed the same day by `807666f`**.
- **`build_graph.py` would write managed blocks into the agent definitions** — raised
  2026-07-30 after `a852b80` unignored `.claude/agents/`, **fixed the same day by `807666f`**
  (`.claude` added to `EXCLUDE_DIRS`). With the hazard gone, `scripts/build_graph.py` was run
  on 2026-07-31 and the `agents/` notes now carry their managed `Map:` blocks like every
  other spoke.

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
