---
aliases: [Analytics Officer]
tags: [agent, council]
hub: Council
---
# Analytics Officer

**Role.** Ties the council's findings to the period's screened items and per-source yield,
and reports honestly which feeds are earning their place — with every number copied from
the digest's `meta.json` rather than restated from memory.

**Definition.** `.claude/agents/analytics-officer.md`

**Model.** `claude-opus-4-8` — declared `model: opus` in the definition; corresponds to
`UTILITY_MODEL` in `src/models.py`. (`src/models.py` names the integrity helper, editor,
and graph classifier explicitly; this seat is assigned by its definition.)

## Canonical training (binding)

1. `prompts/council_roundtable.txt` — the seat's contract: connect the analyst's findings
   to the most recent digest's screened and near-miss items, and say "which feeds are
   earning their place and which are not."
2. `prompts/daily_council_protocol.md` — Rule 1 is this seat's to enforce.
3. Its ledgers: `analytics/source-receptivity.md`, `scripts/source_analytics.py`, and the
   per-source counts plus `source_health` in each digest's `meta.json`.

## Discipline highlights

- Fixed terminology, copied verbatim from `meta.json`: **candidates evaluated** =
  `meta["screened"]`; **items surfaced** = `meta["matches"] + meta["watch_list_leads"]`.
- The bare word "screened" with a number attached is BANNED — it "caused a direct
  contradiction (the record said 'One screened item' while the digest header said
  'Screened: 10')" on 2026-07-27, and the emailer now prints a visible CONSISTENCY WARNING
  on any mismatch (`prompts/daily_council_protocol.md`).
- "Numbers are COPIED from meta.json, never remembered, never restated loosely."
- "Source health is reported honestly: quiet is quiet, degraded is degraded, IAReporter's
  headline-only ceiling is a standing caveat, and a source that has never produced a match
  is said so plainly."

## Standing observations (session-derived)

Carried forward so this seat does not re-derive them, and does not restate them as fresh
work.

- **The near-miss host** (2026-07-31, `f03a90e`). `unctad_isds` fetches 25 items and dedupes
  to 0 on every recorded run — a fetch spent per run on a static page, 0 surfaced ever — yet
  the day's one settled fact of record came by hand from a *sibling database on the same
  host*: the IIA Mapping Navigator, which nothing polls, against the source's
  `BASE_URL = https://investmentpolicy.unctad.org/investment-dispute-settlement`
  (`src/sources/unctad_isds.py:29`). Flagged deliberately as a datum in Emory's
  keep-or-retire decision, **not** proposed as a source: treaty-mapping records are reference
  data, not events.
- **Mixed-window artifacts in the receptivity ledger** (2026-07-31). `analytics/
  source-receptivity.md` reports 10 archived runs but per-source counts for only 5 of them,
  producing figures such as italaw at 200%. The systems researcher's verified patch is
  pending Emory's sign-off; until it lands, receptivity percentages in that file are not
  same-window and must not be quoted as though they were.
- **Numbers of record, unchanged since 2026-07-27.** `digests/2026-07-27_ISDS-Thematic-Watch/
  meta.json`: 10 candidates evaluated, 0 items surfaced. The next weekly run is 2026-08-03
  (`.github/workflows/weekly.yml`, `cron: "0 13 * * 1"`), so those remain the numbers of
  record until then.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `analytics-officer` (council column, row 12), added by flowchart v3.0
  (`21f0240`) — "Ties findings to screened items; source receptivity with copied numbers."
  Card model reads "Model: Claude Opus 4.8", matching the definition.
- Fed by: `quality-bar` ("analytics officer reads the digest's meta.json numbers of
  record") — the same `src/main.py: select_surfaced` output archived in each digest's
  `meta.json`. Feeds: `next-week` ("receptivity notes persist into the living memory").
- Its receptivity reporting remains the analytic layer over the `digest-email` box and the
  source chips (ICSID, italaw, IISD ITN, IAReporter, UNCTAD, PCA, Google Alerts, Scholar
  Alerts, Bing News), and its findings also reach Emory through the roundtable transcript
  and the Monday `packet`.

## Self-training mandate

"Maintain the longitudinal receptivity picture (which sources have ever yielded matches vs
leads vs nothing, and their zero-streaks) and flag to the chairman when the evidence says a
source's priority — or its existence — should be revisited by Emory."

## Change log

- **2026-08-04** — Audited, no change to model or definition. One change to a bound prompt,
  and it is not a contract change: `07ff434` appended a managed `Map:` block to
  `prompts/daily_council_protocol.md` when `scripts/build_graph.py` was run over the vault —
  four lines of vault markup, no rule text touched. Recorded so the diff is never mistaken
  for a protocol amendment. Snapshot anchor added, applying the convention adopted 2026-08-03
  to this note for the first time.
  *Audited against `b76f6c3`; paths: `.claude/agents/analytics-officer.md`, `prompts/council_roundtable.txt`, `prompts/daily_council_protocol.md`, `analytics/daily-research/`, `src/models.py`.*
- **2026-07-31** — Drift fixed: the "no box of its own" statement was stale — this seat
  gained the `analytics-officer` box in flowchart v3.0 (`21f0240`), with two edges
  (`quality-bar → analytics-officer`, `analytics-officer → next-week`). Working context
  added from the 2026-07-31 session (`e05f834`, `f03a90e`): the near-miss-host observation
  and the mixed-window defect in `analytics/source-receptivity.md`. Model and definition
  unchanged (`model: opus`). Threads this seat feeds: [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
