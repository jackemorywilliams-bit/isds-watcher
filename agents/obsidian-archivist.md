---
aliases: [Obsidian Archivist]
tags: [agent, council]
hub: Council
---
# Obsidian Archivist

**Role.** The librarian-scholar of the vault — it keeps the project's memory palace
accurate and navigable, owning the per-agent notes, the agent registry, the project change
log, and the audits that catch drift between the vault and the repository's reality.

**Definition.** `.claude/agents/obsidian-archivist.md`

**Model.** `claude-opus-4-8` ("Claude Opus 4.8" in the definition's discipline block);
declared `model: opus`; corresponds to `UTILITY_MODEL` in `src/models.py`. (`src/models.py`
governs the pipeline's LLM stages; this seat is a repository-side agent assigned by its
definition.) Unchanged by the 2026-08-03 model move (`939deaa`).

## Canonical training (binding)

This seat binds no `prompts/*.txt` contract — its canon is the vault itself and the craft
rules written into its definition:

1. The vault structure: the `moc/` hubs, the workflow flowchart
   (`moc/00 - Project Map.md` plus `views/isds-workflow-3d/`), `HANDOFF.md`, and the
   `agents/` memory area it owns.
2. `scripts/build_graph.py` — the hub-and-spoke mapping script that owns the managed
   `graph:auto` blocks (idempotent; a second run is byte-identical; a four-link cap on
   outgoing non-hub links per spoke). **Never write that block's literal HTML start marker
   into a note** — see the hazard recorded in the 2026-07-31 audit slice below; name the
   convention, do not reproduce its delimiters.
3. `scripts/build_site.py` — verified, not assumed, at each deployment: the public site is
   generated from `METHODOLOGY.md` and `digests/` only.

## Discipline highlights

- "Accuracy over completeness-theater: every registry and changelog line cites its commit
  hash or file path. An entry you cannot source you do not write."
- "When ANY agent's prompt, model, or contract changes, the corresponding vault note and
  the registry update in the same change set — stale agent memory is a defect you own."
- "managed blocks stay regenerable and are never hand-edited; frontmatter/alias conventions
  respected; vault-internal metadata never leaks to the public site (build_site strips it —
  verify, don't assume)."
- "Emory is the operator (never 'Jack' in vault artifacts); professor-facing surfaces stay
  clean of internal jargon."

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `obsidian-archivist` (council column, row 14), added by flowchart v3.0
  (`21f0240`) — "Keeps the vault's memory current: agent registry, change log, drift
  audits." Card model reads "Model: Claude Opus 4.8", matching the definition.
- Its one edge: fed by `next-week` ("the archivist folds project changes into the vault's
  registry and change log"). It has no outbound edge on the chart, which is right — its
  output is the vault the chart is rendered in, not a downstream pipeline stage.
- Off-chart, it is also fed by the repository's own history (git log), the agent definitions
  under `.claude/agents/`, and the council's records under `analytics/`; and it feeds
  [[Agent Registry]], [[Project Change Log]], [[Workflow Threads]], [[Project Machinery]],
  and the drift escalations it raises to Emory.
- `moc/00 - Project Map.md` embeds `views/isds-workflow-3d/` inside a managed
  `workflow-3d` block; every role card's `target` is an Obsidian link text resolved by
  `dv.app.workspace.openLinkText` in `views/isds-workflow-3d/view.js`, which is why each
  `agents/<name>` note must exist under exactly that name.

## Self-training mandate

"Each deployment, audit one slice of the vault against the repo's reality (agents vs
registry, flowchart vs pipeline, HANDOFF vs workflows) and fix or escalate drift;
periodically research current Obsidian/PKM practice so the vault's organization stays
state-of-the-art."

**Audit slice, 2026-08-03 (third deployment).** Agent context currency — every
`.claude/agents/` definition and every `agents/` vault note against `src/models.py`, the
council records of 2026-08-01 through 2026-08-03, and the flowchart manifest. Findings:

1. **The 2026-07-31 vault build never reached `main`, and has been silently absent from
   every agent's context for three days.** `agents/Workflow Threads.md` and the audited
   versions of all eleven other notes live on `feat/methodology-source-council-sync`
   (`689a9e7`, `ea8bdf2`, `d6cd84c`, `07ff434`, merged there by `40b76da`, branch tip
   `f195e21`). `git merge-base --is-ancestor f195e21 main` is **false**. The council itself
   caught this on 2026-08-01 and escalated it — "the archivist's vault work (Workflow
   Threads.md + agent-memory audit) is orphaned off main" (`4d5c562`,
   `analytics/council-log.md` 2026-08-01) — and the escalation was never actioned. The
   content is recovered into this change set. **This is the single largest cause of stale
   agent memory in the project, and it is mine.** A note that exists only on an unmerged
   branch is a note no agent has.
2. **`939deaa` retroactively falsified two dated historical records.** The Fable→Opus 5
   move was applied as a blanket string replacement that ran through *dated history* as well
   as live statements. It rewrote this note's 2026-07-30 audit slice to assert that
   `src/models.py` set `HEAVY_MODEL = "claude-opus-5"` as of commit `4f8f981` — false;
   `4f8f981` set it to `claude-fable-5`, and `git show 4f8f981` proves it. It made the same
   substitution in [[research-analyst]], attaching the Opus 5 assignment to a 2026-07-29
   commit that produced Fable 5. The commit message says "The dated history above is left as
   written"; the diff shows otherwise for these two files. Both are corrected in this change
   set, with the two-step model history stated explicitly rather than flattened. **Standing
   rule adopted from this: a model rename is never a blanket replacement over the vault —
   live statements change, dated records do not.**
3. **The card-model conflict on two seats changed character and got harder to see.** The
   `systems-designer` and `site-experience` cards asserted "Model: Claude Fable 5" against
   definitions that declare no model. `939deaa` rewrote both to "Model: Claude Opus 5". The
   defect is identical, but it now reads as a legitimate assignment because two other seats
   genuinely hold it. Re-recorded in both notes and escalated to Emory, still unresolved.
4. **The integrity officer's in-session taxonomy recitation is four entries stale against
   its own record.** The recitations at `analytics/daily-research/2026-08-02.md:196` and
   `2026-08-03.md:185` both list the ten entries as of 2026-07-31 and omit entries 11–14,
   which that seat itself adopted on 08-01 and 08-02. The canonical seventeen-entry table
   now lives in [[integrity-officer]] with a commit per entry, and the note directs the seat
   to read it rather than recite from memory.
5. **The council's own standing-rules record is also orphaned.** `3d31de8` ("council: adopt
   two standing rules — third-party retrieval, and blocked-vs-quiet source status") created
   `analytics/council-sessions/2026-08-03-standing-rules.md` (887 lines) and exists only on
   a worktree branch; it is not an ancestor of `main`. The two rules it adopts *were*
   implemented (`0091ade`, `fe02f39`), so the machinery is on main while its reasoning is
   not. Escalated — this is not vault work and I have not moved it.
6. **Three flowchart defects, none of them model-related.** The `quality-bar` card cites
   `src/config.py` for a threshold of 40 that lives in `fingerprint.yaml:5` (that file's own
   default is 60); two card descriptions overflow their card width because the wrapper
   appends rather than truncates, and the validator's total-length bound cannot catch it;
   and `views/isds-workflow-3d/view.js` has no freshness guard where the SVG has a
   fail-closed one. All three recorded in [[systems-designer]]. Everything else on the chart
   verified clean: 28 nodes, 9 chips, 40 edges, all ten `agents/<name>` targets resolve to
   real notes, every other file-and-symbol citation resolves, and
   `node tools/isds-workflow-3d/validate.mjs` exits 0.
7. **Site isolation re-verified, and the earlier statement of it sharpened.**
   `scripts/build_site.py` reads only `METHODOLOGY.md` and `digests/`. Grepping `docs/`
   directly: **zero** occurrences of any vault note name ([[Agent Registry]],
   [[Project Change Log]], [[Workflow Threads]], [[Project Machinery]]) and **zero**
   occurrences of any card `target` value. What *does* appear in `docs/how-it-works.html`
   and `docs/assets/workflow.svg` is the `.claude/agents/*.md` **definition** paths, inside
   the chart's `<title>` tooltips, as evidence citations alongside `prompts/*.txt` and
   `src/*.py` — which is the chart's deliberate evidence convention, not a vault leak. The
   distinction matters and the old phrasing blurred it.

8. **Deliverable-drift sweep (scope extension, same deployment).** Widened from the vault to
   every surface that describes the system to a human: `README.md`, the built `docs/`,
   `scripts/site_templates/`, `METHODOLOGY.md`, `HANDOFF.md`, `COUNCIL.md`, `prompts/`, and
   `.claude/agents/`. Fixed here, because they are agent memory or my own domain: five stale
   or false statements across four agent definitions, and two false statements in
   `HANDOFF.md` (the heavy tier's model id, self-contradicted 134 lines later; and the
   digest classifier located in `src/classify.py` when `src/models.py` defines it). Escalated
   with file:line, because they belong to other seats: two professor-facing defects in the
   digest template — the site can never render a `NOT-READ` status, and the source table's
   Items column contradicts its own caption and is wrong on the page published today —
   plus README's source and email counts, the flowchart's total absence of the relay, three
   false statements in `COUNCIL.md`, two prompt-level drifts, and two gaps in `METHODOLOGY.md`
   Parts IX and X. Full statements with evidence: [[Project Change Log]], "Escalated
   2026-08-03 by the deliverable-drift sweep".
9. **One relayed claim did not survive checking, and is recorded as not-done rather than
   done.** The sweep was briefed to reflect "the first Talkwalker feed replacing the dark
   Google lane." `alerts.yaml` documents Talkwalker at lines 12–17 as the intended
   replacement, but the `feeds:` list at lines 29–42 contains only Google URLs and **zero**
   Talkwalker entries. The lane is still dark. Recorded as open in [[Workflow Threads]] C5,
   with the verification stated, rather than written up as progress.

**Observation from the periodic-research half of the mandate.** Stated as what it is: not a
literature survey — I did no web research this session — but a generalizable convention
this deployment's failures argue for. Every failure above is a *currency* failure, and the
vault has no mechanical way to detect one: a note asserts things about the repository but
carries nothing that says which repository state it was true of. Exactly one note in the
vault does carry it — [[Workflow Threads]] opens with "**Snapshot taken:** 2026-07-31, at
`e153ce3`" — and that single line is what makes its staleness checkable instead of
guessable. The convention worth generalizing is a **snapshot anchor** in every agent note:
the commit the note was audited against, plus the paths it claims to describe. Staleness
then becomes a one-command question (`git log <anchor>..HEAD -- <paths>`) rather than a
judgement call, and the next archivist inherits a checkable claim instead of a confident
paragraph. Adopted here as of this deployment — see the anchor line at the foot of each
note's change log — and it is the concrete answer to "no agent has old context": the notes
now say when they were last true.

**Audit slice, 2026-07-31.** Agents vs registry vs flowchart, plus the click-through check.
Findings, all fixed in that change set except where noted:

1. **Five notes claimed to have no flowchart box, and all five were wrong.** Flowchart v3.0
   (`21f0240`) put every one of the nine agents on the chart. `integrity-officer`,
   `analytics-officer`, `obsidian-archivist`, `systems-designer`, and `site-experience` all
   gained boxes with real edges. The registry's "two seats have no box at all" sentence was
   wrong for the same reason.
2. **Click-through check: all nine targets resolve.** Every `target` value of the form
   `agents/<name>` in `workflow.json` has a matching note under `agents/`.
3. **Model conflict on two cards, escalated not resolved.** See item 3 of the 2026-08-03
   slice for its current state.
4. **Both drifts escalated on 2026-07-30 are closed** by `807666f` — `COUNCIL.md`'s model
   row corrected, and `.claude` added to `EXCLUDE_DIRS` in `scripts/build_graph.py`.
   Re-verified 2026-08-03: `.claude` is still in `EXCLUDE_DIRS` at `scripts/build_graph.py:47`.
5. **Adopted method rules were nowhere in agent memory.** The fetch-first and
   docket-page-first rules, the positive-control rule, the four new taxonomy entries, and the
   chairman's three session-protocol rules all existed only in the daily records. Each was
   moved into the owning seat's note with its commit.
6. **HAZARD, found by running `build_graph` and escalated: a note that quotes the managed
   block's start marker destroys itself on the second run.** `scripts/build_graph.py:195`
   builds its replacement pattern as `re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END)`
   under `re.DOTALL`, which matches from the **first** occurrence of the start marker
   anywhere in the file — including one sitting harmlessly inside backticks in prose. Run 1
   appends a real block at the end of the note; run 2 then matches the prose marker as the
   opening delimiter and the real block as the closing one, and deletes everything in
   between. This note was the only file in the vault that quoted the marker, being the note
   that documents the convention, and it lost 92 lines on the second run before being
   restored from `689a9e7`. The prose above no longer reproduces the delimiters, and the
   idempotence guarantee the vault relies on is **conditional** on no note ever quoting the
   start marker. Machinery fix escalated: [[systems-designer]] open item 1.

**Audit slice, 2026-07-30.** Agents vs models. `src/models.py` set
`HEAVY_MODEL = "claude-fable-5"` and `HANDOFF.md` recorded the analyst on `claude-fable-5`
(commit `4f8f981`), while `COUNCIL.md`'s "Model assignments" table still read
"Heavy-reasoning sub-agents (research analyst, one-pager drafting) | `claude-opus-4-8`" —
stale relative to the single source of truth, and escalated rather than edited because
`COUNCIL.md` sat outside that change set. A second finding from the same pass —
`scripts/build_graph.py` would then have written managed blocks into the agent definitions
themselves — was recorded with its evidence in [[Project Change Log]]; `build_graph` was
therefore not run during that build. *Both findings were fixed the same day by `807666f`.*
*(This paragraph was retroactively falsified by `939deaa`, which replaced its two
`claude-fable-5` readings with `claude-opus-5`; restored to what the record actually said —
see item 2 of the 2026-08-03 slice.)*

## Change log

- **2026-08-03** — Third deployment, by operator directive: verify that no agent carries old
  context. Recovered the orphaned 2026-07-31 vault build (`f195e21`) into the mainline,
  corrected two records `939deaa` had retroactively falsified, brought the chairman,
  analyst, integrity officer and analytics officer notes current with three sessions of
  adopted rules, added [[Project Machinery]], and rebuilt [[Workflow Threads]] against the
  present record. Own drift fixed: this note's 2026-07-30 slice had been rewritten to assert
  a model assignment that commit never made. Two escalations raised: the orphaned
  standing-rules record, and the still-unresolved card-model conflict. Snapshot-anchor
  convention adopted.
  *Audited against `6a5cd2e`; paths: `.claude/agents/`, `agents/`, `src/models.py`,
  `views/isds-workflow-3d/workflow.json`, `analytics/daily-research/`, `analytics/council-log.md`.*
- **2026-07-31** — Second deployment, by operator directive: linearize the vault's threads
  and verify every agent's recorded context. Own drift fixed: the "no box" statement was
  stale after flowchart v3.0 (`21f0240`), which gave this seat the `obsidian-archivist` box
  and the `next-week → obsidian-archivist` edge. Added [[Workflow Threads]]. Both 2026-07-30
  escalations confirmed closed by `807666f`. Model and definition unchanged (`model: opus`).
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`, which established this seat by operator order:
  "owns the vault as memory palace — per-agent notes, registry, change log, drift audits."

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
