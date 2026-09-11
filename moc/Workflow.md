# Workflow

How the instrument works, end to end: sources -> enrich -> three-ring fingerprint ->
classification cascade -> digest, with the council layered on top.

<!-- workflow-3d:start -->
## The whole machine, moving

```dataviewjs
await dv.view("views/isds-workflow-3d", {
  data: "views/isds-workflow-3d/workflow.json"
});
```
<!-- workflow-3d:end -->

- [[METHODOLOGY]] — the full methodology memo (the canonical description).
- [[PLAN]] — the per-ring seed extraction underlying the fingerprint.
- [[FINGERPRINT_DRIFT]] — proposed Ring 1 reweighting awaiting operator approval.
- analytics/instrument-map-2026-08-08.md — how the instrument *actually* runs, read off the
  code, with every claim tagged `[keyword-path]`, `[model-path]` or `[mixed]`. Read this
  alongside the methodology, not instead of it: where the two differ, this one was measured.

**Publication is constrained by TWO gates as of 2026-08-09, and neither can disable the
other.** Read them as a pair (`src/config.py:59-62`):

1. `FILL_FLOOR_SUSPENDED` (`src/config.py:31-39`, default ON, since 2026-08-08) — items
   scoring 25–39 no longer surface.
2. `VALIDATION_STATUS_ONLY` (`src/config.py:73-74`, default ON, since 2026-08-09) — **every**
   item-level entry is held, **including items at or above 40**, and so is the Research Brief.
   The cycle sends one status note carrying the count of what it held.

**So the instrument currently publishes no items at all.** Anything in this vault or the
repository that says a match at or above 40 reaches the digest is describing the machinery,
not today's behaviour.

Prose that describes *a setting* rather than naming *both flags and which is on* has already
drifted twice. The live divergences, with the file list and owner for each, are
`agents/Claim Map.md` **C15** (three files still stating the fill as operative) and **C16**
(five files stating that items at or above the threshold publish). Do not restate either rule
from any of them.

- `src/rings.py` — the R2.1 ring-evidence contract, deriving rings, treaty nexus, evidence
  location/validity and a lane **in shadow on every cycle** since 2026-08-09. It decides
  nothing publicly: `STATE_MODEL_V2="on"` is refused until `STATE_MODEL_V2_PUBLICATION_READY`,
  which is `False`. Two further lanes exist and are off by default — `src/triage.py`
  (`TRIAGE_ENABLED`) and the semantic `src/classify_v2.py` (`V2_SHADOW_CALLS`, so every
  default-run verdict is labelled `lexical_only`).
  - **2026-09-10 — read "the R2.1 contract" as the code, never as a document you can open.**
    The **R2.1 record** that `src/rings.py` and three other production files cite is **not a
    file in this repository and never has been on any branch** — 56 occurrences of the literal
    across 17 tracked files at `948947b`, naming a document nobody here can read. The code is
    real and runs; the specification it fails closed against is not in version control. A grep
    establishes absence **from the repository**, never from the project: no seat may restate
    this as "the R2.1 record does not exist." See [[Workflow Threads]] **S1** and
    analytics/daily-research/2026-09-10-special-session.md:128-174.
  - **And the V2 lane's "shadow" has never made a model call.** `v2_basis` is `lexical_only`
    and `v2_call` is `{"called": false, …}` on **all 328** rows of
    analytics/candidate_telemetry.jsonl. The instrument is scrupulously honest about it — that
    is why the number is knowable — but "V2 runs in shadow on every cycle" means the lexical
    half runs. Turning `V2_SHADOW_CALLS` on is a recurring cost decision and is Emory's.
    Source: analytics/daily-research/2026-09-10-special-session.md:500-508.
