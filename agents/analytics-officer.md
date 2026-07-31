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

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- This seat has **no box of its own** on the flowchart. It reads what the machine column
  produces and speaks in the council's dialogue: the numbers it is bound to come from the
  `quality-bar` box's output (`src/main.py: select_surfaced`) as archived in each digest's
  `meta.json`, and its receptivity reporting is the analytic layer over the `digest-email`
  box and the source chips (ICSID, italaw, IISD ITN, IAReporter, UNCTAD, PCA, Google
  Alerts, Scholar Alerts, Bing News).
- Its findings surface to Emory through the roundtable transcript and the `packet`
  ("Monday review packet") rather than through a dedicated edge.

## Self-training mandate

"Maintain the longitudinal receptivity picture (which sources have ever yielded matches vs
leads vs nothing, and their zero-streaks) and flag to the chairman when the evidence says a
source's priority — or its existence — should be revisited by Emory."

## Change log

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].
