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

**Model.** `claude-opus-5` — declared `model: opus` in the definition since 2026-08-04,
on the operator's direct answer ("both are on opus… opus 5 for the version"). Before that
the frontmatter carried no `model:` key at all while the flowchart card asserted "Claude
Opus 5": the card was true only while the invoking session happened to match, and would
have gone silently false the moment it did not. `src/models.py` assigns models to the
pipeline's LLM stages and still does not cover this repository-side seat; the frontmatter
selects the Opus *tier*, and the version is the operator's recorded choice rather than
something the key itself pins. `scripts/check_models.py` now fails if a card asserts a
model that no definition declares.

> **Conflict RESOLVED — closed `c25ea64`, corrected here 2026-08-06.** This block carried the
> defect as unresolved for two days after it was closed, and both of its factual predicates
> are now false: `.claude/agents/systems-designer.md` declares `model: opus`, and the card's
> `meta` in `views/isds-workflow-3d/workflow.json` reads "Model: Claude Opus 5", not
> "Claude Fable 5". [[site-experience]] closed its identical block on 2026-08-04; this one
> was missed. [[Claim Map]] C12 already records the claim CLOSED, and
> `agents/Agent Registry.md` corrected itself on 2026-08-06 while describing it as "three
> vault notes, one fact" — it was four, and this was the fourth.
>
> **Why no guard caught it, which is the part worth keeping.** `scripts/check_models.py`
> matches only the ``**Model.** `…` `` line, which was correct here throughout. Prose that
> contradicts that line is invisible to it. Reformatting or paraphrasing a seat note can
> therefore break a leg of the check without failing it.

## Canonical training (binding)

This seat binds no `prompts/*.txt` contract. Its canon is the repository's own machinery
and the standing constraints its definition names:

1. The artifacts it owns — the generators, validators, and renderers under `scripts/` and
   `src/`, including the flowchart toolchain behind `views/isds-workflow-3d/`.
2. `src/models.py` — the standing model assignments it must honor.
3. The project's operating constraints: **low cost** *(corrected 2026-08-08 — see below)*,
   and the polite-crawler rules (identify, honor robots.txt, never evade).

> **The "zero-cost constraint" is not a true description of this instrument — corrected here
> 2026-08-08, escalated where it is not this seat's to fix.** This note said "zero cost"
> because the definition says it: `.claude/agents/systems-designer.md:17` binds the seat to
> "the **zero-cost** constraint". On 2026-08-08 this seat's own code reading established that
> `classify_item(item, provider=None)` does **not** force the keyword path — it falls through
> to `os.environ["MODEL_PROVIDER"]`, so the below-cutoff tail has been **model-classified in
> production all along** (`analytics/instrument-map-2026-08-08.md` §4). `README.md:3-9` was
> corrected the same day: "the instrument is **low-cost, roughly cents per run, not free**."
>
> Three things follow, and they should not be collapsed. **(1)** This note's line is corrected,
> because the vault is this seat's memory and it must not carry a constraint the repository
> has disproved. **(2)** The definition file is **not** corrected — editing `.claude/agents/`
> is a contract change and belongs to Emory. It is escalated in [[Agent Registry]] and
> [[Workflow Threads]]. **(3)** Until Emory rules, this seat is in the position of holding a
> definition-level constraint it has itself falsified, and the resolution is *not* to design
> as though cost were unbounded — the finding lowers the claim from "free" to "cents per run",
> which is still a constraint, and the polite-crawler rules are untouched.

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

- Flowchart box: `systems-designer` (machine column, **row 9**), added by the build committed
  as `21f0240` — "Builds the machinery: renderers, validators, pipelines — fail-closed,
  tested." It sits in the machine column because that is what it builds, not because it is a
  pipeline stage. *(Corrected 2026-08-08: this note said **row 7** for four days. The seat
  moved to row 9 in manifest **v2.2**, dated 2026-08-03 in `workflow.json`'s own `meta.note`,
  when the fetch relay took machine rows 7–8. [[Agent Registry]] recorded the move on
  2026-08-04 and this note did not — the registry and the seat note disagreed about where
  the seat sits, which is precisely the class of defect the maintenance rule exists to
  prevent. The manifest is the source of truth and was read directly.)*
- Its one edge: `systems-designer → site-experience` ("designer builds artifacts the site
  agent publishes"). It has no inbound edge on the chart — it is fed by operator directives
  and council-identified defects, which the chart does not draw.
- The rest of the machine column is still the artifact of its work rather than its
  successor: `collect`, `skip-repeats`, `first-score`, `read-doc`, `ai-check`,
  `quality-bar`, plus `claim-gate` and `citation-check` in the Emory column, and the
  flowchart view itself.
- **Gap recorded 2026-08-09: the chart has not moved and the machine has.** The manifest is
  still **30 nodes / 44 edges at v2.2**, verified today, while this seat built four subsystems
  that appear nowhere on it — the shadow ring derivation (`src/rings.py`), the semantic
  classification path (`src/classify_v2.py`), the triage lane (`src/triage.py`) and the
  constrained headline lane (`src/headline_lane.py`), plus the two publication gates in
  `src/config.py`. **This is not asserted as a defect to fix immediately**, and the reason is
  the chart's own logic: all four are off or shadow-only by default, so drawing them as pipeline
  stages would overstate what runs. But the `quality-bar` card is now wrong in a second way —
  it describes a near-miss fill that is suspended *and* a threshold that no longer publishes —
  and whenever that card is corrected (it is already open on two counts since 2026-08-03), the
  question of whether the shadow lane earns a card should be answered in the same edit rather
  than deferred again. Recorded in [[Workflow Threads]] **B5**/**B9** context; the manifest is
  not hand-edited and this seat regenerates from it.

## Self-training mandate

The definition states no explicit self-training clause. Its operative equivalent is the
fail-closed rule: each deliverable must arrive with the validator that would have caught
its own failure mode, so the guard set grows with every build. Recorded as the definition
stands — no mandate is invented here.

## Change log

- **2026-08-09** — **Workstreams D/E, F and G all built in one session, and every one of them
  shipped switched off.** Uncommitted, on `fix/restore-council-label`; suite **564 passed /
  5 xfailed**, re-run by [[obsidian-archivist]] rather than copied from the session report.
  - **The ring contract stopped being a flag with nothing behind it.** `src/rings.py` derives —
    in shadow, on every cycle — per-ring strengths, a deterministic treaty nexus, evidence
    location and validity, and a lane. The predicate structure is the substance: a match needs
    the IP ring **plus** a second doctrinal ring **plus** a supported nexus **plus** valid
    evidence, so **a no-IP judicial case can never be a match regardless of its score**, and a
    negative nexus cannot be derived from an unread body. `STATE_MODEL_V2="on"` is refused
    while `STATE_MODEL_V2_PUBLICATION_READY` is `False` (`src/config.py:98`, `:109-111`).
  - **The semantic path exists and is deliberately mute.** `src/classify_v2.py` +
    `prompts/classifier_v2.txt` are wired for shadow, but `V2_SHADOW_CALLS` defaults **off**
    (`src/config.py:154-195`): every default-run verdict is labelled `lexical_only`, a test
    asserts no model identity can appear on one, and `V2_SHADOW_CALLS=replace` is **refused**
    (`V2_SHADOW_CALLS_FORBIDDEN`). Verdicts carry `claims_source` provenance, and
    **`guard_demoted` fires on every V1 ring claim** — correct, not a bug: V1 supplies no spans,
    so there is nothing for the guard to accept.
  - **A counting error was found by resolving a modelling question.** The 7-vs-4 outcome split
    resolved losslessly (seven logical states → four operational outcomes + metadata), and the
    enumeration went 12,288 → **21,504** (`src/rings.py:112`). In the same pass, **tail provider
    failures turned out to be under-counted by exactly the size of the tail** and are now
    counted. Rationale: `analytics/state-space-resolution-2026-08-09.md`.
  - **Workstream F.** `src/triage.py` + `prompts/triage.txt`; `TRIAGE_ENABLED` off by default;
    deterministic sort; **provider absence recorded, not misreported**; adversarial tests.
    **Design (c), the stratified tail audit, is a config stub** — `TAIL_AUDIT_N = 0`
    (`src/config.py:229-243`) — and is recorded as unimplemented rather than counted as shipped.
    That distinction is this seat's discipline working: a stub named as a stub.
  - **Workstream G, and the design decision worth keeping.** `src/headline_lane.py` generates
    from a closed grammar with no slot for a legal or thematic conclusion — and with **three**
    limitation clauses keyed on evidence location (`:81-85`) rather than one. The single-clause
    version would have told readers that a body the instrument *had* retrieved was paywalled;
    the fix is `LIMITATION_PAYWALLED` / `LIMITATION_UNRETRIEVED` / `LIMITATION_RETRIEVED` as a
    closed set whose membership the guard checks. `scripts/check_headline_lane.py` holds output
    byte-identical. The public-label mapping was corrected so an accessible-body item is not
    called `HEADLINE_ONLY_LIBRARY_LEAD`.
  - **The guards became guards.** `.github/workflows/pipeline-guards.yml` wires
    telemetry-privacy, seen-integrity, headline-lane, lock and currency — currency in its own
    job with **`fetch-depth: 0`**, without which the check cannot see the history it asserts
    against — **plus each guard's own planted-violation tests**. This closes
    [[Workflow Threads]] **B8**, and closes it beyond its terms: the thread asked for wiring and
    got wiring *plus* proof that each guard still fails when it should.
    `scripts/check_lock.py` was written and treats the empty set as the designed state.
  - **Deviation of record, and it is this seat's.** `scripts/check_site_sync.py` **rebuilds
    `docs/` in place** — `:25` runs `build_site.py` with no temporary directory, `:31` diffs the
    working tree — so it is a **mutating command wearing the name of a check**. It was run here
    on the belief that it was stamp-only and **reverted `docs/` to HEAD**. `docs/` is rebuilt
    from source in the integrator's final battery. Logged as an open defect, this seat's to fix:
    [[Workflow Threads]] **B9**. The lesson is the seat's own rule turned inward — *read the
    actual repo file before asserting how anything works* — applied to a script this seat wrote.
  - **Still Emory's, recorded for the second consecutive session and not edited:**
    `.claude/agents/systems-designer.md:17` binds this seat to "the zero-cost constraint" that
    2026-08-08's code reading falsified. A definition edit is a contract change.
  - **Flowchart placement re-verified, not assumed** — `views/isds-workflow-3d/workflow.json`
    read directly this date: `systems-designer` is **machine column, row 9**, manifest
    `meta.version` **2.2**, 30 nodes / 44 edges, and
    `node tools/isds-workflow-3d/validate.mjs` exits 0. Unchanged since 08-03; the row is
    re-confirmed rather than restated from the note.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths: `src/`,
  `scripts/`, `tests/`, `prompts/`, `.github/workflows/`, `src/config.py`,
  `views/isds-workflow-3d/workflow.json`, `analytics/state-space-resolution-2026-08-09.md`,
  `.claude/agents/systems-designer.md`.*
- **2026-08-08** — **The largest single build this seat has shipped, and the only one that
  found a defect in the archive it had already published.** All of it is **uncommitted, on
  branch `fix/restore-council-label`**; the suite was green **that day** at **414 passed /
  5 xfailed, 32 tests new** *(dated reading — see the 2026-08-09 entry above for the current
  564 / 5)*.
  - **Phase 0 — telemetry.** `src/telemetry.py`, `scripts/telemetry_query.py`,
    `scripts/check_telemetry_privacy.py`, `tests/test_telemetry.py`. One record per candidate
    per run; hashes and bounded structured values, **never article text**, with a privacy
    guard that fails the build on any planted text field. Before this, per-item classifier
    identity was computed and discarded — for five of the fourteen published entries it is
    **unrecoverable** (`analytics/retrospective-audit-2026-08-08.md` §4).
  - **Phase 1 — outcome-gated seen-state.** `src/state.py`, `src/classify.py`, `src/main.py`;
    a `state/deferred.json` retry queue with attempt counts; loud abandonment after three
    attempts into `analytics/abandoned_candidates.jsonl`, cross-checked by
    `scripts/check_seen_integrity.py`, which fails the build on a missing abandonment record.
    Legacy state is migrated at read time. A candidate whose classification fails is no longer
    marked seen at all.
  - **The root cause, found and fixed.** `research_brief.generate_brief` had **no exception
    handler and ran BEFORE `save_state`**, so a brief failure discarded the run's seen-state
    *after* the digest had been written. That is the mechanism behind the Telefónica
    double-publication — the same italaw URL published on consecutive days with contradictory
    verdicts, **32 with a ring on 06-09, 28 with none on 06-10**. Regression test:
    `test_a_failing_research_brief_cannot_unwrite_the_seen_state`. **This is the entry to
    reread before the next "harmless ordering" change**: nothing about the brief step looked
    like it could touch the archive, and it silently governed it.
  - **Workstream H — publication safety.** `FILL_FLOOR_SUSPENDED` defaults **ON**
    (`src/config.py:31-39`); sub-40 items no longer surface; a zero-surfaced cycle emits the
    approved body from `src/render.py:59` verbatim, asserted character-for-character by
    `tests/test_pipeline.py:951`, and the subject line becomes "status-only cycle: N screened,
    none at/above 40". **The vault consequence is [[Claim Map]] C15**: the behaviour moved and
    **eight** statements of the old behaviour did not, one of them the public homepage.
  - **The live finding, which is a correction to what this seat believed.**
    `classify_item(item, provider=None)` never forced the keyword path; it falls through to
    `os.environ["MODEL_PROVIDER"]`, so the production tail is model-classified. See the
    zero-cost block above.
  - **Not done, still designed:** the D/E ring-evidence contract, F semantic triage and the G
    headline lane are behind a disabled flag and are **not production behaviour** — said in
    those words at `METHODOLOGY.md:67` so the addition cannot be read as claiming them.
  *Recorded against the working tree of `fix/restore-council-label` (uncommitted); paths:
  `src/telemetry.py`, `src/state.py`, `src/classify.py`, `src/main.py`, `src/config.py`,
  `src/render.py`, `templates/digest.html.j2`, `scripts/check_telemetry_privacy.py`,
  `scripts/check_seen_integrity.py`, `scripts/telemetry_query.py`, `tests/test_telemetry.py`,
  `tests/test_pipeline.py`, `analytics/instrument-map-2026-08-08.md`.*
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
