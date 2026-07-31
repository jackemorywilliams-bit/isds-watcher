---
aliases: [Systems Researcher]
tags: [agent, council]
hub: Council
---
# Systems Researcher

**Role.** The second daily researcher — it studies the instrument rather than the disputes,
producing sourced, component-specific proposals for making the collection and
classification pipeline more efficient and more effective.

**Definition.** `.claude/agents/systems-researcher.md`

**Model.** `claude-opus-4-8` — declared `model: opus` in the definition; corresponds to
`UTILITY_MODEL` in `src/models.py`; shown on the flowchart's `systems-researcher` card as
"Model: Claude Opus 4.8".

## Canonical training (binding)

1. `prompts/systems_researcher.txt` — the contract verbatim: survey open-source
   scraper/monitor/legal-tech projects, information-retrieval and text-classification
   literature, LLM tooling, and GitHub Actions practice; separate QUICK WINS from LARGER
   MOVES with effort and risk; commit the daily note to
   `analytics/systems-research/<DATE>.md`.
2. The known weak points it targets, named in the prompt: three-seed fingerprint recall;
   case-insensitive substring matching rather than lemmatization; no cross-feed dispute
   dedup; headline-only sources under-scoring on-theme cases; the deterministic scorer's
   "not-a-covered-investment" miss (Apotex).
3. `analytics/optimization-log.md` — the idea bank; dedup against all of it before
   proposing, under a deliberate at-most-one-new-idea-per-day anti-padding cap.
4. The adoption record (the 2026-07-27 four-lens majority vote and the statuses in the
   log) — "ideas move by evidence and cost, not enthusiasm."

## Discipline highlights

- Every suggestion must "(a) name the exact component it touches, (b) cite a REAL
  retrievable source with a URL, and (c) state the concrete change and expected effect. No
  vague advice ('use better AI'); no unsourced claims." (`prompts/systems_researcher.txt`)
- "One excellent, sourced, component-specific suggestion beats five vague ones."
- Hard constraints honored: free GitHub Actions plus Claude Max only; OPEN sources only;
  robots.txt honored and never evaded; the three-ring theme and its seed grounding are
  fixed.
- Integrity guardrails belong in the proposal itself, not as an afterthought — the G22
  title-mining near-veto is the model case.
- "On a dry day, say so in one line — do not pad."

## First seating — 2026-07-31

This seat had a definition before it had a session. It was first actually convened on
2026-07-31 (`analytics/daily-research/2026-07-31.md` Part 5; commits `e05f834`, `f03a90e`),
against a three-item queue set by the 2026-07-30 close-out. All three were discharged:

1. **`scripts/source_analytics.py` same-window defect — diagnosed and patched, sign-off
   gated.** The report mixes windows: 10 archived runs in the denominator, per-source counts
   from 5 of them, so `italaw` reads 200%. The patch preserves the lifetime figures the
   council actually cites rather than naively restricting the window; four tests pass on the
   patched copy and fail on the current one. **Edits to `scripts/` require Emory's sign-off**
   — the patch text sits in Part 5 §2 and has not been applied. Conditions attached:
   regenerate `analytics/source-receptivity.md` in the same commit, and re-read
   `COUNCIL.md:25`.
2. **Two corrections applied to `analytics/optimization-log.md`** (`e05f834`) — the
   2026-07-01 quoted-phrase technique re-sequenced from *substitute* to
   *fallback-after-attempted-fetch*, and the 2026-06-30 ODS-route entry's access premise
   corrected as partly falsified (the recommendation stands on its independent
   symbol-archiving ground).
3. **One new proposal, dedup-checked** (`f03a90e`) — a `Health` column in the receptivity
   report carrying each source's status and consecutive-zero streak from
   `state/source_health.json`, on dbt's source-freshness pattern. Status: *proposed*.
   Guardrail attached as a condition of adoption, not a nicety: the report is longitudinal
   and health is point-in-time, so the column must carry an explicit "as of <latest run
   date>" label. Sequencing: land **after** the same-window patch, never bundled with it.

The seat also recorded a self-training note about a false hypothesis it killed with two
git-log calls before it could become a false finding.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `systems-researcher` (council column, row 9). Unchanged by flowchart v3.0
  (`21f0240`); card model reads "Model: Claude Opus 4.8", matching the definition.
- Fed by: `daily-researcher` ("daily optimization ideas feed the systems log").
- Feeds: `minutes` ("improvement queue lands in the close-out") and `packet`
  ("send_human_review.py section 2: workflow-improvement ideas from the optimization log
  reach Emory's briefing").

## Self-training mandate

"Revisit your past proposals' fates each session (adopted, rejected, rotting) and let that
record recalibrate what you propose; keep current on the scraper/RSS/LLM-tooling ecosystem
so your sourcing stays contemporary."

## Change log

- **2026-07-31** — First seating recorded (`e05f834`, `f03a90e`): the `source_analytics.py`
  same-window patch proposed and gated on Emory's sign-off, two optimization-log corrections
  applied, one new health-column proposal added. Also confirms the `analytics/
  optimization-log.md` idea bank is now this seat's live working record, not just a dedup
  target. Model and definition unchanged (`model: opus`). Its one open thread:
  [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
