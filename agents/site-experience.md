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

- **2026-08-09** — **One queued item landed, one new hazard aimed straight at this seat's
  surface.** Uncommitted, `fix/restore-council-label`. Model, definition and prompt bindings
  unchanged.
  - **The homepage near-miss copy is repaired.** `scripts/site_templates/index.html.j2`, flow
    step 5, now reads "While the classifier is under validation the near-miss fill is suspended:
    items below the threshold are not published at all, and a cycle with none at or above it
    sends a status note reporting the screening count — a note about the instrument's output,
    not a finding that nothing happened." That closes this seat's row in [[Claim Map]] **C15**.
  - **And it was stale again within the same day.** The step still opens "Those that meet the
    threshold make the digest." As of 2026-08-09 `VALIDATION_STATUS_ONLY` holds items **at or
    above** the threshold too, so **the public homepage now overstates what reaches the
    professor** — the opposite direction from the error just fixed. New row: [[Claim Map]]
    **C16**, and this seat owns the template half. **Fix it in the same change set as the
    `METHODOLOGY.md` and `README.md` lines**, or the contradiction simply moves.
  - **⚠ `scripts/check_site_sync.py` is not safe to run, and this seat's surface is what it
    damages.** It **rebuilds `docs/` in place** (`:25` invokes `build_site.py` with no temporary
    directory; `:31` then diffs the working tree), so the command the vault's own maintenance
    rule tells every seat to run as proof is in fact a **write**. On 2026-08-09 it reverted
    `docs/` to HEAD. `docs/` will be rebuilt from source in the integrator's final battery.
    Tracked as [[Workflow Threads]] **B9**; the fix is [[systems-designer]]'s (`scripts/` is
    that seat's), but the consequence lands here, which is why it is recorded in this note too.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `scripts/site_templates/`, `scripts/build_site.py`, `scripts/check_site_sync.py`, `docs/`,
  `src/render.py`, `templates/`, `README.md`.*
- **2026-08-08** — **Nothing landed on this seat's surfaces from the repair session, and four
  things are now queued on it.** Recorded so the queue is not lost between sessions. Model,
  definition and prompt bindings unchanged (`git log 373cce6..HEAD -- .claude/agents/` is
  empty).
  1. **The `digest.html.j2:120` site overclaim — routed here open, and CLOSED while this
     record was being written.** The repair session logged it as outstanding. Re-read at the
     end of the archivist pass, `scripts/site_templates/digest.html.j2:120` no longer says
     "No thematically relevant developments this cycle." It now says: "**No candidate reached
     the match threshold this cycle. This reports the instrument's output on the text
     available to it, and does not establish that no relevant development exists.**" That is
     the same correction `src/render.py:59` made on the email side — one claim, two surfaces,
     now agreeing. **Uncommitted, on `fix/restore-council-label`.** Recorded as closed because
     the file says so, not because a session report did; the handoff note that still lists it
     open is the stale copy.
  2. **The `docs/` rebuild is now load-bearing for four separate claims.** Until this session
     is committed and `scripts/build_site.py` re-run, the published site still shows: the
     Apotex **"Holdings"** caption on `docs/backtest.html` (source fixed 2026-08-06 at
     `373cce6`, two days stale on the page); the **uncorrected Gazprom annotation**; the
     `METHODOLOGY.md` §VI.B correction and §IX addition, absent; and the eight archive
     corrections. `scripts/check_site_sync.py` correctly reports the gap — it is expected,
     not drift, and it becomes drift the moment the session is committed without a rebuild.
  3. **[[Claim Map]] C15 puts one of this seat's strings in a coordinated fix.**
     `scripts/site_templates/index.html.j2:186` tells the reader that "Near-misses at or above
     the relevance floor of 25 are shown separately as watch-list leads" — **false by default
     as of 2026-08-08**, because the fill is suspended. The second half of the same sentence
     ("a genuinely quiet week reports zero items and says so") is now *more* true than before.
     **Do not fix this string alone**: it is one of eight statements of the same rule, listed
     at C15, and a lone template edit relocates the contradiction rather than closing it.
  4. **What this seat's earlier work now carries.** Two of the divergences this note's
     predecessors escalated are closed on the published surfaces and the closure is verified
     here: the homepage's **"never empty"** promise is gone from the template tree, and the
     digest index's **"11 weekly runs … fell from 78 to 13 as deduplication matured"** now
     reads "11 **archived** runs … **no steady trend**" ([[Claim Map]] C5, C8).
  *Recorded against the working tree of `fix/restore-council-label` (uncommitted); paths:
  `templates/digest.html.j2`, `scripts/site_templates/`, `docs/`, `scripts/build_site.py`,
  `scripts/check_site_sync.py`.*
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
