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

⚑ **That is the intended model, and on 2026-08-16 this seat observed that it is not the model
running.** The declared `model: opus` selects a tier, not a version. Queried directly during the
2026-08-16 session, the runtime reported `session_context.model` = **`claude-opus-5`** and
`external_metadata.last_served_model` = **`claude-opus-5`**.
**REQUESTED `claude-opus-4-8` → ACTUAL `claude-opus-5`.** Observed, not assumed; recorded here
per the never-substitute-silently rule at `src/models.py:18` rather than passed over.

⚑ **Re-observed from this seat 2026-08-22, six days later, unchanged.** The runtime again reports
`session_context.model` = **`claude-opus-5`** and `external_metadata.last_served_model` =
**`claude-opus-5`**. Two observations from this seat, ten consecutive days of them from
[[integrity-officer]] (2026-08-12 through 2026-08-22), and no commit on `.claude/agents/` or
`src/models.py` in between. The Model line above is **left as written**: it states the operator's
directive of 2026-08-03, and editing it to `claude-opus-5` would ratify a substitution nobody
authorised. [[Workflow Threads]] **D6**.

⚑ **Re-observed a third time 2026-08-25, thirteen days after the officer's first report.**
Runtime again: `session_context.model` = **`claude-opus-5`**,
`external_metadata.last_served_model` = **`claude-opus-5`**, against a Model line stating
Claude Opus 4.8. `git log c4f6825..HEAD -- .claude/agents/ src/models.py` returns **no commit**
across 56 commits. The Model line stays as written, for the third time and the same reason.
**What has changed is only the count, and the count is now the whole finding:** three
observations from this seat, and the officer still disclosing it unasked at
`analytics/daily-research/2026-08-23.md:723` and `2026-08-25.md:791`. Recorded in
`HANDOFF.md`'s fallback table, which this seat maintains by hand because nothing else does.

This makes the seat the **second independent confirmation** of the discrepancy
[[integrity-officer]] has self-reported four times (2026-08-12, 08-14, 08-15, 08-16), and it
closes the question of whether that seat's report was peculiar to it: it is not. Five seats are
documented as Claude Opus 4.8 and none of the five is pinned to it by any file in the
repository. The mechanism `src/models.py:18` specifies for surfacing exactly this —
`record_fallback()` writing REQUESTED vs ACTUAL into `HANDOFF.md` — has never fired on this
path; its only caller is `src/research_brief.py:161`. Fixing that is not this seat's to do:
`.claude/agents/`, `src/` and `views/` are all outside its authority. Recorded, qualified in
[[Agent Registry]], and escalated to Emory. **The line above is left standing because it states
the directive; this block states the observation. Both are true and they disagree, which is the
finding.**

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

### Adopted method rules — read the artefact, not the description of the artefact

Three rules this seat adopted from three separate failures. They are one rule in three costumes,
and each was learned only after the previous one failed to generalise:

1. **2026-08-16** — *A guard's exit 0 licenses only the claim the guard actually tests.* Learned
   when this seat wrote "no model drift exists" on the strength of `check_models.py` exiting 0,
   while the integrity officer's contrary report sat in a directory the same session read.
2. **2026-08-22** — *A commit message is a claim about a change, never a reading of the files
   after it; a claim-map row is closed only by re-reading every cell it names.* Learned when
   [[Claim Map]] C11 was recorded as fixed from `44550ca`'s message, and the public site went on
   saying "nine sources" for five more days.
3. **2026-08-25** — *A guard's documented check is not a performed check. Before citing a guard
   as cover for a class of defect, read the code that implements it.* Learned when
   `scripts/check_currency.py`'s docstring was found to promise a bare-sha citation check
   (`:30-32`) that the implementation (`:184`) does not perform — and an unresolvable citation
   sat inside a **tracked** note for a month, on a surface that read as guarded.

**Supersede, never overwrite.** A correction sits beside the original with the original wording
preserved and dated; dated records are not rewritten to match a later fact. Live statements are
corrected in place with the correction dated. This convention is also the remedy for
ORPHANED-COMMIT CITATION (the taxonomy entry routed here 2026-08-25): when a cited commit no
longer resolves, name the live sha, name the superseded one, and say which is which — do not
delete the citation and do not silently swap it.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `obsidian-archivist` (council column, row 14), added by the build committed
  as `21f0240` — "Keeps the vault's memory current: agent registry, change log, drift
  audits." Card model reads "Model: Claude Opus 4.8", matching the definition.
- Its one edge: fed by `next-week` ("the archivist folds project changes into the vault's
  registry and change log"). It has no outbound edge on the chart, which is right — its
  output is the vault the chart is rendered in, not a downstream pipeline stage.
- Off-chart, it is also fed by the repository's own history (git log), the agent definitions
  under `.claude/agents/`, and the council's records under `analytics/`; and it feeds
  [[Agent Registry]], [[Project Change Log]], [[Workflow Threads]], the session records under
  `analytics/vault-sessions/`, and the drift escalations it raises to Emory. (A
  `Project Machinery` note was named here on 2026-08-03 as though it existed; it never did —
  see item 1 of the 2026-08-04 slice. The dead link is removed rather than papered over.)
- `moc/00 - Project Map.md` embeds `views/isds-workflow-3d/` inside a managed
  `workflow-3d` block; every role card's `target` is an Obsidian link text resolved by
  `dv.app.workspace.openLinkText` in `views/isds-workflow-3d/view.js`, which is why each
  `agents/<name>` note must exist under exactly that name.

## Self-training mandate

"Each deployment, audit one slice of the vault against the repo's reality (agents vs
registry, flowchart vs pipeline, HANDOFF vs workflows) and fix or escalate drift;
periodically research current Obsidian/PKM practice so the vault's organization stays
state-of-the-art."

**Audit slice, 2026-08-13 (eighth deployment): where a seat's binding rules actually live —
and one thread this vault reported discharged that was not.**

The 2026-08-09 slice adopted the rule that "a reconciliation brief is a source like any other,
and it is checked against the tree before it is written into the vault." This deployment applied
it to the vault's own change log, and the change log failed the check.

1. **[[Workflow Threads]] said F1's marks had landed. They had not, and nothing had moved in
   seventeen days.** The 2026-08-11 entry read "F1's seventeen verification marks reach `main`
   with this merge." `git show --stat 0a67756 -- analytics/verification_ledger.jsonl` is empty —
   the integration never touched the ledger. `main`'s copy is blob `f3dbbf6`, last written by
   `8891c21` on 2026-07-27, and `origin/chore/operator-marks-2026-07-27` is still not an ancestor
   of `main`. Counted from the two blobs: 37 claims / **21 marks** on `main`, 40 / **38** on the
   branch — *the same figures F1 recorded on 2026-08-04.* The line is struck in place; **F1**
   now carries the counts and the demonstration, and the three stranded claim ids were replayed
   through `verify.replay` to show them resolving `unverified` against `main`. This is exactly
   the failure this seat's standing session exists to catch, and it was found in this seat's own
   file — a vault note that had converted an expectation into a completed fact.

2. **The generalisation of the 2026-08-03 holdout failure is structural, and it is not this
   seat's to fix.** Every seat note carries a section marked binding; a seat's read path is its
   `.claude/agents/` definition plus the `prompts/` files that definition enumerates; **eight of
   the nine definitions never name the seat's own note.** Grepped rule by rule, ten of
   [[research-analyst]]'s eleven adopted rules are outside its read path, and so are the four
   `label: 1` rows of `scripts/holdout_set.json`. The analyst that called a holdout positive
   "new to the project" was not being careless with a fact it held — the fact was never in front
   of it. [[integrity-officer]] is the one seat where this was fixed, after council R8, and the
   fix was never generalised. Opened as **D5**, escalated to Emory, recorded in three notes.

3. **What this seat got wrong about its own orphan convention.** The container's clone was
   **shallow**, and the orphan query ran against a truncated object set before that was noticed.
   Re-run after `git fetch --unshallow` (584 commits): `--is-ancestor` reports **45** unlanded
   branches, `git cherry` reports **6**, and the difference is squash merges. Three of the six
   (`claude/sweet-mccarthy-*`) carry content `main` already holds in longer form — 247, 506 and
   496 lines against the branches' 164, 166 and 246 — so they are superseded, not stranded. The
   convention is kept for content questions like F1, where blobs are compared directly; for "did
   this branch land", `git cherry` is the honest query. **A shallow clone silently weakens every
   ancestry claim this seat makes, and checking for one is now part of the query.**

4. **Not restamped, deliberately.** [[Claim Map]]'s anchor (`a22f4cb`) is three commits stale on
   its declared paths, and all three touch `STATE_OF_THE_ANSWER.md` only — `.claude/agents/`,
   `prompts/`, `METHODOLOGY.md`, `lit-review/` and `scripts/site_templates/` are untouched. This
   pass did **not** re-read the C-rows against the amended living memory, so the anchor is left
   stale rather than moved. Moving an anchor is an assertion that the note was re-verified; a
   restamp this pass had not earned would be the precise defect `check_currency.py` exists to
   catch. `STATE_OF_THE_ANSWER.md`'s own stale anchor is [[research-analyst]]'s, and the
   2026-08-08 decision not to restamp another seat's living memory still governs.

**The rule this deployment adopts.**

> **A vault note may record that work is *expected* to land; it may not record that it *did*
> until the blob is read on the target branch.** The 2026-08-11 entry was written at merge time
> and stated a consequence of the merge as an accomplished fact. It was wrong the moment it was
> written, and it then sat unchallenged for two days, on the one thread whose whole subject is
> work that never landed. Where a note asserts that something reached `main`, the citation is the
> blob or the `git cherry` line — never the merge that was supposed to carry it.

**Audit slice, 2026-08-09 (seventh deployment): the threads a session reports as CLOSED.**
The 2026-08-08 slice found that this seat's currency query is scoped to `.claude/agents/` and
`prompts/` and therefore cannot see the drift that actually occurs, and specified a second
per-session query over the artifacts a note asserts facts about. This deployment ran that
second query for the first time as a **discipline against its own briefing**, and that is the
finding.

1. **The remove-stale brief this seat was given was itself partly stale, and the vault would
   have inherited it.** The briefing listed, among items to remove, "any statement that C15 is
   unresolved." Applying the standing rule — *no thread is closed on the strength of a session
   report* — each of C15's eight ⚠ rows was re-read in its file. **Five are repaired. Three are
   not:** `fingerprint.yaml:5-6`, the `quality-bar` card at
   `views/isds-workflow-3d/workflow.json:177`, and the `src/main.py` comment, **which had moved
   from `:497-500` to `:687-690`** — so a line-number check would have reported it gone, and
   only the row's quoted text located it. Had this seat accepted the brief, the vault would
   have recorded a divergence as closed while the public-facing manifest card still stated the
   retired rule. **The rule earned its keep on the first occasion it was tested against an
   instruction rather than against an absence.** The three survivors are exactly the rows whose
   owners sit outside the seat doing the repair, which is now a predictor rather than an
   observation.
2. **The repair pass created its mirror image inside the same session, and nothing in the
   vault would have caught it.** `VALIDATION_STATUS_ONLY` (2026-08-09) holds item publication
   **including items at or above 40**. Four of the five sentences repaired that same day for
   C15 now say the opposite. `METHODOLOGY.md:49` — repaired today — and `METHODOLOGY.md:69`
   contradict each other **twenty lines apart in the document that goes to Dr. Benavides**,
   which is the identical defect the 08-08 pass recorded and resolved to stop producing.
   Recorded as the new [[Claim Map]] **C16**. The generalizable rule adopted here:
   **when a change adds a gate upstream of an existing gate, every sentence describing the
   downstream gate silently becomes a claim about the pair** — so the Claim Map row for the old
   gate is where the new one must be noticed, and prose must name *both* flags and which is on
   rather than describing a setting as the behaviour.
3. **Two threads did close, and both closed on files rather than reports.** **B8** — the three
   guards with no CI — closes on `.github/workflows/pipeline-guards.yml`, read line by line;
   it closed *beyond its terms*, wiring five guards plus each guard's **planted-violation
   tests**, which answers the failure mode the thread named (a fail-closed check that has
   silently stopped checking). **D3** closes on a re-run of `scripts/check_currency.py`: **9
   claims across 5 notes, 0 failed**, the `STATE_OF_THE_ANSWER.md` anchor having been added by
   [[research-analyst]], the seat that owns the file. The 08-08 decision *not* to restamp
   another seat's living memory cost one day and was correct.
4. **A check in this repository is a write, and the vault's own maintenance rule points every
   seat at it.** `scripts/check_site_sync.py:25` runs `build_site.py` with **no temporary
   directory** and `:31` diffs the working tree, so the command reverts or rewrites `docs/` as
   its first act; it reverted `docs/` to HEAD this session. [[Claim Map]] maintenance rule 5
   says "`docs/` is never the fix — change the source, rebuild, and let
   `scripts/check_site_sync.py` prove it." **The rule instructs every seat to run a script that
   is unsafe on a dirty tree.** Opened as [[Workflow Threads]] **B9** and flagged in
   `HANDOFF.md`; the fix is [[systems-designer]]'s.
5. **The flowchart did not move while four subsystems were built.** Manifest re-read: still
   **v2.2, 30 nodes, 44 edges**, `node tools/isds-workflow-3d/validate.mjs` exit 0, and
   `systems-designer` still at machine row 9 — so that seat note's row is **re-verified, not
   corrected**, which is the first time this check has come back clean since it was adopted.
   `src/rings.py`, `src/classify_v2.py`, `src/triage.py` and `src/headline_lane.py` appear
   nowhere on the chart. Recorded in [[systems-designer]] as a gap **deliberately not asserted
   as urgent**: all four are off or shadow-only, so drawing them as pipeline stages would
   overstate what runs. The `quality-bar` card, however, is now wrong on a third count and its
   long-open correction should answer the question in the same edit.
6. **A real retrieval that advances no ledger, recorded so it is not double-counted.** The H&H
   v. Egypt Decision on Jurisdiction and Award Rule 48(4) excerpts were retrieved into `seeds/`
   with 21 spans verified — this seat confirmed both files on disk — but that matter has never
   had a row in `analytics/locked_set/RETRIEVAL_LEDGER.md`, whose counts are **unchanged today:
   2 RETRIEVED, 3 BLOCKED, 8 QUEUED**. The day's genuine retrieval is therefore *not* progress
   on the locked set, and [[Workflow Threads]] **B7** and `moc/Evidence Ledger.md` say so
   explicitly. The related discipline worth preserving: the unpublished full Award is recorded
   as a **permanent scope limit, not a gap slug** — a queue entry that no retrieval can ever
   close is a lie about the queue.
7. **Write mode was again not run, for the third consecutive session and the same reason.**
   `build_graph --dry-run` plans edits to **seventeen** notes, of which only four are this
   seat's; the other thirteen are `working/`, `prompts/`, `lit-review/`,
   `analytics/locked_set/`, `analytics/daily-research/`, `BOUNDED_CHANGE_PROTOCOL.md` and this
   session's out-of-bounds analytics artifacts. The script is whole-vault or nothing, **a
   managed block is never hand-written**, so there is again no lawful partial run. This is no
   longer a scheduling accident: it is a **structural defect in the tool** that has now blocked
   three sessions, and it is escalated as such rather than re-noted.

**Observation from the periodic-research half of the mandate.** No web research this session;
stated as an internal finding rather than dressed as external practice. The convention this
deployment argues for concerns *inputs*, not notes. Every prior slice guarded against stale
**files**; this one had to guard against a stale **instruction** — a briefing that stated a
thread was resolved when three of its eight rows were untouched. The vault's existing rules all
point outward at the repository, and none of them says what to do when the report you are
reconciling *from* is wrong. The rule adopted here: **a reconciliation brief is a source like
any other, and it is checked against the tree before it is written into the vault** — with the
corollary that when a brief and a file disagree, the disagreement itself is recorded, because
it tells the next session which reports to distrust. That is why this pass ends with C15 open
against its own instructions, and why it says so in five places rather than one.

**Audit slice, 2026-08-07 (sixth deployment).** Agent-context currency, run as the query rather
than the judgement: `git log b76f6c3..HEAD -- .claude/agents/ agents/ prompts/ src/models.py
views/isds-workflow-3d/workflow.json`, plus `python3 scripts/check_currency.py`,
`scripts/check_models.py`, `scripts/build_graph.py --dry-run`, and
`node tools/isds-workflow-3d/validate.mjs`. Findings:

1. **The convention this seat adopted in prose is now a program, and this seat did not write it.**
   `scripts/check_currency.py` (`fb1c04e`, 2026-08-06) mechanises the snapshot anchor: it parses
   `Audited against <sha>`, checks the sha exists and is an ancestor of HEAD, and reports every
   commit that has touched the note's declared paths since. Its docstring says plainly why it
   exists, and the reason is this project's recurring one. **Two gaps, both this seat's to raise
   because it owns what the notes claim.** (a) Its `TRACKED` map holds **five** entries — the four
   index notes and `STATE_OF_THE_ANSWER.md` — while **thirteen** vault notes carry an anchor. The
   nine seat notes, the ones an agent actually reads before working, are unguarded, which is
   precisely where this session found three days of missing rules. (b) **Nothing runs it:**
   `grep -rn check_currency .github/workflows/` returns nothing, where `check_models.py` and
   `check_marks.py` are both wired to workflows. A guard that must be remembered is the class of
   control the systems seat itself ruled fails silently. Escalated, not edited — `scripts/` and
   `.github/` are outside this seat's paths.
2. **Not one of the nine seat notes carried a single line from 2026-08-05, 08-06 or 08-07, and
   the cost is a numbering collision in the council's own taxonomy.** Measured before writing:
   `grep -c "2026-08-0[567]" agents/*.md` returned **0** for all nine seat notes except
   `systems-designer.md`. In that window three full council sessions adopted fourteen rules. The
   consequence is not hypothetical. `agents/integrity-officer.md` is the taxonomy's canonical
   home and its heading read *"24 entries as of 2026-08-04"*; entries 25, 26 and 27 had been
   adopted since. On 2026-08-07 the integrity officer opened that table to number a new entry —
   doing exactly what its mandate directs — and, missing entry 27 (*scope-mixed screen*, adopted
   in the 08-06 close-out and never written here), numbered *manufactured residual* as 27 too.
   The chairman adopted it under that number (`2026-08-07.md:975`). **Two council rulings now
   assign one number to two patterns, and the input to that error was a stale count in a file
   this seat maintains.** The officer said so in the same note — "the vault table is stale again,
   in the single file the mandate names" (`2026-08-07.md:713`). All fourteen rules are landed in
   this change set; the collision is recorded under both numbers and escalated for the chairman
   and the officer to settle, because renumbering would change what two rulings say.
3. **A false commit citation in the registry, written by this seat.**
   [[Agent Registry]]'s 2026-08-06 paragraph credited `373cce6` with correcting
   `prompts/research_analyst.txt:18`. `git show --stat 373cce6 -- prompts/` is empty; the fix is
   **`9efafb0`**, whose own message states it. This is taxonomy 17a, *mis-located
   internal-authority citation*, committed by the seat that maintains the taxonomy's home.
   Corrected in place.
4. **Orphan check — four true orphans, and a category the vault has never recorded.** Fetching
   every remote head (65 refs) and testing `git merge-base --is-ancestor <tip> origin/main`:
   **4 branches are true orphans** — `chore/operator-marks-2026-07-27` (still 17 operator marks
   short of `main`, now eleven days unmerged) and the three ruled-non-canonical
   `claude/sweet-mccarthy-*` records. **17 further branches share no merge-base with `main` at
   all.** `git merge-base origin/main origin/fix/notable-line-integrity` returns empty; `main`
   has five root commits, the oldest 2026-07-22, while that branch roots at 2026-06-08. They are
   pre-history-rewrite artefacts, and ancestry cannot say whether anything in them is lost.
   Recorded rather than asserted either way. **Everything committed by the council in the audit
   window did land:** `council/2026-08-06`, `-postscript`, `register-2026-08-06`,
   `threads-2026-08-06-source-audit` and `council/2026-08-07` are all ancestors of `origin/main`,
   which discharges the chairman's 2026-08-06 warning that A8 existed only off `main`.
5. **The graph measurements this note's registry carried were stale in three of four numbers.**
   Re-run: 117 notes, 231 edges, 0 orphans, **7** WARNs (not 4), **7** files awaiting a managed
   block (not 11). The `Project Machinery` broken link is gone. And the reason the managed-block
   run keeps not happening is structural rather than discretionary: `build_graph` has no path
   filter, and four of the seven pending files sit outside this seat's self-merge authority, so
   a full run can never land under it. Escalated.
6. **`HANDOFF.md:164` still attributed the analyst's Opus 5 assignment to the operator directive
   of 2026-07-29.** That directive (`4f8f981`) set `HEAVY_MODEL = "claude-fable-5"`; Opus 5 came
   from the 2026-08-03 directive (`939deaa`). This is the exact defect this note's own standing
   rule was written for — *a model rename is never a blanket replacement over the vault; live
   statements change, dated records do not* — surviving in a live file for four days. Fixed here,
   because `HANDOFF.md` is this seat's path. `COUNCIL.md:66` carries the same misattribution and
   `:68` still locates the digest classifier "in `src/classify.py`" — the identical locution
   escalated on 2026-08-04 and still open. Escalated again with its age, not edited.

**Observation from the periodic-research half of the mandate.** No web research this session, and
it is named as an internal finding rather than dressed as external practice. The finding is about
the anchor convention this seat invented. It now has a program behind it, which is the outcome the
convention was argued for — and the program would not have caught this session's central defect,
because the notes it does not track are the notes agents read. The generalizable form: **a currency
guard must cover the artifacts that are read, not the artifacts that are indexed.** The four index
notes are the ones a human browses; the nine seat notes are the ones an agent loads before working.
The guard was pointed at the first set. Second, and narrower: **a count in a heading is an input,
not a label.** "24 entries as of 2026-08-04" reads like metadata and functioned as an argument to
the next entry's number. Any note whose contents are numbered sequentially by a downstream reader
is a load-bearing artifact, and its staleness has a cost that is not merely informational.

**Audit slice, 2026-08-04 (fourth deployment).** The currency check the 2026-08-03 slice
adopted, run for the first time as a query rather than a judgement:
`git log 6a5cd2e..b76f6c3 -- .claude/agents/ agents/ src/models.py
views/isds-workflow-3d/workflow.json analytics/daily-research/ analytics/council-log.md`.
Findings:

1. **Three of the 2026-08-03 slice's own claims are false against `main`, and the seat notes
   they describe were never changed.** The currency query above returns, under `agents/`,
   only `8705f7a` — the merge that recovered the *2026-07-31* work — and nothing that adds
   2026-08 content to any seat note. Verified per note by grepping for any `2026-08-0x`
   string: `council-chairman.md`, `research-analyst.md`, `integrity-officer.md`,
   `research-editor.md`, `site-experience.md`, `systems-designer.md` and
   `systems-researcher.md` each returned **zero**. Specifically:
   (a) the 08-03 change-log line recording a new `Project Machinery` note is false — that
   note exists in no commit in the repository (`git log --all -- 'agents/Project Machinery.md'` is empty),
   yet three places in this note linked to it, so the vault carried three dead links for a
   day;
   (b) "brought the chairman, analyst, integrity officer and analytics officer notes current
   with three sessions of adopted rules" is false for three of the four — only
   `analytics-officer.md` carries any 2026-08 content;
   (c) slice item 4's "the canonical seventeen-entry table now lives in [[integrity-officer]]"
   is false — that note's taxonomy section read "extended to ten" until today.
   **The consequence is measurable, not hypothetical:** the recitation defect item 4 was
   written to close recurred twice after it, at `analytics/daily-research/2026-08-03.md:185`
   and `2026-08-04.md:535`, both opening from the stale ten-item list. All three claims are
   corrected in the 08-03 change-log entry below, and the substance is landed here for real.
2. **The snapshot-anchor convention was adopted vault-wide and applied to one note.** The
   08-03 slice says "see the anchor line at the foot of each note's change log"; on `main`,
   `grep -c "Audited against" agents/*.md` returned 1 of 12 — this note. An anchor on one
   note makes one note's staleness checkable. Anchors added to every note in this change set,
   which is what makes step 1 of this session's own contract executable next time.
3. **The flowchart moved and no vault note noticed.** [[Agent Registry]] records "28 nodes,
   40 edges" verified 2026-07-31 and the 08-03 slice repeats it. The manifest today is **30
   nodes, 44 edges** — `0e7d0f7` / `16ab9d9` added the two fetch-relay cards and moved the
   two builder seats from machine rows 7–8 to 9–10. `node tools/isds-workflow-3d/validate.mjs`
   exits 0 and confirms the counts, all ten `agents/<name>` targets still resolve, and the
   overflow defect escalated on 08-03 is closed (`1476821`: "all described, no overlaps").
   Registry corrected. Also corrected: the vault calls the chart "v3.0" while
   `views/isds-workflow-3d/workflow.json` `meta.version` reads **2.2** — the vault was using
   the commit-message naming of `21f0240` as if it were the manifest's own version.
4. **Two of the three flowchart defects escalated on 08-03 are still open, verified today.**
   The `quality-bar` card still cites `src/config.py: threshold 40 / floor 25` for a
   threshold that lives at `fingerprint.yaml:5`; `views/isds-workflow-3d/view.js` still has
   no freshness guard where the SVG has a fail-closed one. Both remain [[systems-designer]]
   work on Emory's go-ahead. Not hand-edited.
5. **Orphan check — one genuine orphan, and it is the operator's own work.**
   `origin/chore/operator-marks-2026-07-27` is not an ancestor of `origin/main` and carries
   **20 lines of `analytics/verification_ledger.jsonl` that `main` has never held**: 17
   operator verification marks and 3 claims. `main`'s ledger holds 21 marks (`8891c21`); that
   branch holds 38. Escalated, not merged — the ledger is operator-owned.
6. **The 2026-08-03 standing-rules council record is gone from version control.** The 08-03
   slice escalated `3d31de8` / `analytics/council-sessions/2026-08-03-standing-rules.md` (887
   lines) as sitting on a worktree branch. `git cat-file -t 3d31de8` now returns *"Not a valid
   object name"*, and no remote branch carries the file. The two rules it adopted are in the
   code (`0091ade`, `fe02f39`, both on `main`); their reasoning is not. Escalated as
   unrecoverable-from-git rather than as pending.
7. **Three unmerged `claude/*` branches are deliberately unmerged, not orphaned.** Checked
   before writing them up, and the check changed the finding:
   `analytics/daily-research/2026-08-01.md:452` rules the cloud-run records
   **non-canonical parallel artifacts, preserved by reference on their origin branches**,
   because they ran `claude-sonnet-4-6` in seats assigned other models. The same close-out
   (`:487`, item 2) recommends archiving or deleting them, and that recommendation is still
   unactioned. Recorded in [[Workflow Threads]] as Emory's, not as drift.
8. **`HANDOFF.md` still carried the two false statements the 08-03 slice reported fixing**,
   plus one the systems seat found on 08-04. Fixed here, because `HANDOFF.md` is this seat's
   path: the heavy tier read `claude-opus-4-8` at line 29 against `claude-opus-5` in
   `src/models.py` and against its own line 163 — the self-contradiction `939deaa` left when
   it updated one and not the other; the digest classifier was located "in `src/classify.py`"
   when `src/models.py` defines `DIGEST_CLASSIFIER_MODEL` and `src/classify.py:58` imports
   it; and the `italaw` row asserted the zero-streak guard "flags it `DEGRADED`" in the
   present tense when `state/source_health.json` records `zero_streak: 1` and the earliest
   possible flag is 2026-08-17. `COUNCIL.md:68` carries the same classifier locution and is
   escalated rather than edited — it is not this seat's file.

**Observation from the periodic-research half of the mandate.** No web research this
session; stated as an internal finding, not dressed as external practice. The snapshot-anchor
convention worked exactly as intended the moment it was actually run — one `git log` command
produced findings 1 and 3 in seconds, where the previous three deployments had to
reconstruct them by reading. But finding 2 shows the convention's own failure mode: a
convention adopted in prose and applied to one file is indistinguishable from a convention
not adopted. The generalizable rule this deployment argues for is narrower and harder than
the anchor itself: **a vault change is not made until it is on `main`, and the session that
claims it must verify it there.** Every one of this deployment's findings 1, 2, 5 and 6 is
the same failure in a different costume — work that was really done, really recorded, and
really invisible. The countermeasure adopted here: this session's record ends with the
merge, and the next session's first act is to re-run the currency query against what this
one claims.

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
   [[Project Change Log]], [[Workflow Threads]]) and **zero**
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

- **2026-08-28 (twelfth deployment)** — Standing every-3-days session, audited against
  `b7d973d` (`main`, clean tree, complete history — 846 commits after `git fetch --unshallow`;
  the clone arrived shallow at 186 for the **fourth** consecutive session, which is now the
  expected state and not an anomaly). Cadence held at three days. **The currency guard is green
  on `main` for the first time since 2026-08-17**, ending a seventeen-run red streak — fixed by
  `scripts/reanchor.py` (`a8bccbb`) and its CI wiring (`93a69f7`), not by this seat, and not by
  C17's actual remedy: `_is_maintenance("cb762ed")` still returns `False`, so the false positive
  is masked rather than removed. **New finding, [[Workflow Threads]] D10** — the fail-closed
  humanizer rule, recorded as binding on two seats, cites
  `working/benavides-comment-replies-2026-08-08.md:5-6`, a path absent from the working tree and
  from every object reachable from every ref. Marked at the registry row; rule left standing,
  citation flagged. **Twelve stale "(uncommitted)" citations corrected** across
  `agents/Agent Registry.md:430,431,433` and `agents/Workflow Threads.md` B6, B7, C13 and C14 —
  all twelve paths landed at `667772c` (2026-08-11), with
  `.github/workflows/pipeline-guards.yml` at `e8931ac`; each was resolved individually precisely
  because the thirteenth is the D10 file, and a blanket replacement would have asserted that a
  file which has never existed had landed. **Three ambiguous thread IDs** (`B5`, `C11`, `C12` each
  head two threads; [[Claim Map]] runs a third `C11`) disambiguated with a table rather than
  renumbered, since the IDs are cited across the record. **D9 sharpened**: all 35 unresolvable
  bare-sha tokens in the tracked notes are *correctly written* — blobs, run ids, ledger claims, or
  orphans the notes declare as orphans — so the fix must key on citation modality, not on every
  hex token. **A claim written this session was withdrawn before merge**: that `93a69f7` was a
  counter-example to D5. Opening `.claude/agents/council-chairman.md` falsified it — the chairman's
  definition does not enumerate `prompts/daily_council_protocol.md`, and only
  `.claude/agents/analytics-officer.md:15` does — making that commit a fresh **instance** of D5.
  The error and its correction are both recorded in D5, because the shortcut that produced it
  (asserting a read path without opening the file) is the behaviour D5 exists to catch.
  Orphan check: 7 of 100 branches, one new (`origin/council/2026-08-26`), carrying a `.sent/`
  marker only — **no substantive work stranded**. No external PKM research this session; the
  budget went to the agent-context audit and the citation sweep, and that is recorded rather than
  dressed up as outside practice.

- **2026-08-25 (eleventh deployment)** — Standing every-3-days session, audited against
  `ad66a96` (`main`, clean tree, complete history — 804 commits after `git fetch --unshallow`;
  the clone arrived shallow at 188 for the third consecutive session). **Cadence recovered:
  three days, not six.** Headline: an **ORPHANED-COMMIT CITATION on this seat's own surface** —
  `agents/Project Change Log.md:1021` has cited `80ad250` as the commit that froze the vault
  graph on 2026-07-21 since the entry was written; the commit resolves nowhere and no commit on
  any branch carries its message. Found by applying, to this vault, the taxonomy entry the
  council adopted and routed to this seat the same morning
  (`analytics/daily-research/2026-08-25.md:1375`). Annotated in place, never rewritten.
  **The guard-level cause, opened as D9:** `scripts/check_currency.py:30-32` documents a check
  on bare `` `<sha>` `` citations that the code at `:184` does not implement — it resolves a sha
  only when `, PR #N` follows it — so `agents/Project Change Log.md`, a *tracked* note, passed
  the guard with an unresolvable citation for a month. **Rule adopted: a guard's documented
  check is not a performed check; before citing a guard as cover for a class of defect, read the
  code that implements it.** This is the third form of the same rule — 2026-08-16's "a guard's
  exit 0 licenses only the claim the guard actually tests" and 2026-08-22's "a commit message is
  a claim about a change, never a reading of the files after it" — and all three reduce to:
  *read the artefact, not the description of the artefact.* Also: **C8 refined at the code**
  (`apply_block` calls `pat.sub` with no count, so it replaces **every** marker span, not the
  first — the blast radius is per-occurrence); a stale live sentence in **D6** corrected (the
  `HANDOFF.md` fallbacks section it says "has never been written" was written by this seat on
  2026-08-16 and sits at `:202`); and a false broken-link report traced to `build_graph.py`
  reading wikilinks inside inline code spans as live links. Full record:
  `analytics/vault-sessions/2026-08-25.md`.
- **2026-08-22 (tenth deployment)** — Standing every-3-days session, audited against `c4f6825`
  (`main`, clean tree, complete history — 748 commits after `git fetch --unshallow`). **Six days
  since the previous session, not three: the 2026-08-19 session did not run**, and no
  2026-08-19 vault record exists on any branch. Headline: the professor-facing site says "nine
  public sources" forty lines above a chart saying ten, live since `44550ca` (2026-08-17) —
  escalated to [[site-experience]]. **The finding against this seat:** [[Claim Map]]'s
  2026-08-17 anchor block closed the source-count row by quoting `44550ca`'s commit message
  instead of re-reading the files it names, and got the row id wrong as well (C11, not C12).
  Rule adopted: **a commit message is a claim about a change, never a reading of the files after
  it — a claim-map row is closed only by re-reading every cell it names.** Also fixed: a
  `[[Workflow Threads]]` wikilink in this note broken across a line wrap at `:706`, which
  `build_graph.py --dry-run` had been listing as a link to a nonexistent note. Full record:
  `analytics/vault-sessions/2026-08-22.md`.
- **2026-08-16 (ninth deployment)** — Standing every-3-days session, audited against `d997c32`
  (`main`, clean tree, complete history — 621 commits after `git fetch --unshallow`). Full
  record: `analytics/vault-sessions/2026-08-16.md`.

  **The audit slice was the agent-context audit, and it returned a first-person finding.** This
  seat queried its own runtime rather than restating its own note, and found
  `claude-opus-5` serving against a note pinning `claude-opus-4-8` — recorded at the Model
  block above. That corroborates four unasked self-reports from [[integrity-officer]] and
  converts a single seat's anomaly into a structural fact about all five seats documented as
  Claude Opus 4.8. Qualified in [[Agent Registry]] under the roster; escalated to Emory.

  **The lesson this deployment adopts, stated against itself.** On 2026-08-13 this seat wrote
  "**No model drift exists**" and cited `check_models.py` exiting 0. That sentence was wrong on
  2026-08-13 — the integrity officer had already reported the discrepancy on 2026-08-12, in
  `analytics/daily-research/`, a directory this seat read that same session. The guard's own
  docstring says it cannot see a runtime; the seat quoted its exit code as though it could.
  **The rule: a guard's exit 0 licenses only the claim the guard actually tests. Where a seat
  has reported a fact about itself, that report outranks a checker that never observed it.**
  This is the same shape as the 2026-08-13 finding that a rule can be real, correct and outside
  the reader's path — here the report was real, correct, and inside this seat's path, and was
  passed over anyway.

  **Also re-tested, unchanged:** F1 (day 20 stranded), D5 (three days, eight of nine
  definitions), C12, the "zero-cost" line, F2. No new orphaned branches; all three prior vault
  branches confirmed landed on `main`.
  *Audited against `d997c32`; paths: `.claude/agents/`, `agents/`, `prompts/`, `src/models.py`,
  `scripts/check_models.py`, `scripts/check_currency.py`, `scripts/build_graph.py`,
  `analytics/daily-research/`, `analytics/council-log.md`, `HANDOFF.md`,
  `views/isds-workflow-3d/workflow.json`.*

- **2026-08-09 (seventh deployment)** — Final reconciliation of the vault with the completed
  2026-08-09 audit-response work. Audited against `2686422` plus the uncommitted working tree
  on `fix/restore-council-label`. **No commit, no push, no branch change**; no edit to `src/`,
  `tests/`, `scripts/`, `prompts/`, `lit-review/`, `working/`, `METHODOLOGY.md`, `README.md`,
  `docs/`, `digests/`, `seeds/`, `.github/`, or this session's analytics artifacts. Full
  record: `analytics/vault-sessions/2026-08-09.md`.

  **Brought current:** the day's eleven-item delta into [[Project Change Log]] (new
  2026-08-09 section, every line citing a path); the test count from **414 to 564 passed / 5
  xfailed** in all five places it was stated as current, with each dated occurrence preserved
  as a dated reading rather than overwritten; [[Workflow Threads]] refreshed to a 2026-08-09
  snapshot — **B8** and **D3** closed on files, **B6** rewritten from "designed" to "built and
  switched off", **B7**/**C11**/**C12** restated, **B9** and **D4** opened; [[Claim Map]] C15
  corrected row by row and **C16** added; `HANDOFF.md` given a 2026-08-09 checkpoint with the
  08-08 one superseded by pointer rather than rewritten; `moc/Workflow.md`, `moc/Evidence
  Ledger.md` and `PLAN.md`'s post-build deviations brought current on the two gates; seat notes
  updated for [[systems-designer]], [[research-analyst]], [[integrity-officer]] and
  [[site-experience]].

  **Audit slice this deployment: the threads a session reports as CLOSED — and the finding is
  against the briefing, not the notes.** This pass was instructed to remove any statement that
  [[Claim Map]] **C15** is unresolved. Re-read in the files, **five of its eight rows are
  repaired and three are not**, one of them having moved from `src/main.py:497-500` to
  `:687-690` so that only its quoted text found it. C15 therefore stays open, against the
  brief, and the disagreement is recorded in five places. **Worse, the same session's second
  publication gate falsified four of the five repairs** — `METHODOLOGY.md:49` and `:69` now
  contradict each other twenty lines apart, the exact defect the 08-08 pass resolved to stop
  producing. That is **C16**, new.

  **Own drift fixed.** `HANDOFF.md:99-101` is this seat's file and was on C16's divergent list;
  it is corrected here to name **both** flags and which is on, rather than describing one
  setting as the behaviour. The seat's flowchart-row check came back **clean for the first
  time** — `systems-designer` verified at machine row 9 against the manifest, matching both the
  roster and the seat note.

  **Recorded and not fixed, with the reason in each case.** The
  `.claude/agents/systems-designer.md:17` zero-cost contract line (Emory's, second consecutive
  session); `STATE_OF_THE_ANSWER.md:28`'s scoped clause, which is *true today* and would be
  falsified only by a future addition ([[research-analyst]]'s, recorded as **D4** rather than
  pre-emptively hedged); the `quality-bar` card's now-three defects (a manifest edit,
  [[systems-designer]] on Emory's go-ahead); `scripts/check_site_sync.py`'s in-place rebuild
  (**B9**); and the managed-block backlog, now **seventeen** notes — **`build_graph` write mode
  was again not run**, because thirteen of the seventeen planned files are out of bounds for
  this session and the script offers no path filter. Third consecutive session blocked the same
  way; escalated as a tool defect rather than re-noted as a backlog.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `src/`, `scripts/`, `tests/`, `prompts/`, `.github/workflows/`, `analytics/`, `seeds/`,
  `working/`, `agents/`, `moc/`, `views/isds-workflow-3d/workflow.json`, `fingerprint.yaml`,
  `HANDOFF.md`, `METHODOLOGY.md`, `README.md`, `PLAN.md`, `STATE_OF_THE_ANSWER.md`.*
- **2026-08-08 (sixth deployment)** — Reconcile the vault with the master-prompt repair
  session. Audited against `2686422` plus the uncommitted working tree on
  `fix/restore-council-label`. No commit, no push, no branch change; no edit to
  `lit-review/`, `working/`, `METHODOLOGY.md`, `README.md`, `src/`, `scripts/`, `tests/`,
  `digests/`, `docs/`, or the session's analytics artifacts. Full record:
  `analytics/vault-sessions/2026-08-08.md`.

  **Audit slice this deployment: seat notes against the *tree*, not against the definitions.**
  The currency query came back clean — `git log 373cce6..HEAD -- .claude/agents/ prompts/` is
  empty, no contract changed — and three seat notes were wrong anyway. That is the finding, and
  it is a finding about this seat's method rather than about the notes: **the query this seat
  has run at the start of every deployment since 2026-08-03 is scoped to two directories, and
  none of the three errors lived there.** [[systems-designer]] placed its own flowchart box at
  machine row 7 when the manifest has said row 9 since v2.2 on 2026-08-03 — and
  [[Agent Registry]] recorded the move on 2026-08-04, so **the roster and the seat note
  disagreed about where the seat sits for four days** while every currency check passed. The
  same note bound the seat to a *zero-cost* constraint the day's code reading disproved. And
  [[Claim Map]] carried C13 as an open definitional split for two days after the council ruled
  it. [[Workflow Threads]] D1 is rewritten around the corrected statement of the risk: **vault
  notes lag the tree, not the definitions**, and a second per-session query is now specified
  for the artifacts a note asserts facts about.

  **Own drift fixed.** This note's [[Agent Registry]] entry claimed a `build_graph --dry-run`
  prints four WARNs and one broken link from this file to a nonexistent `Project Machinery`
  note. Re-measured: **seven** WARNs, and **the broken link is gone** — the reference survives
  only as prose recording that the note was never created, which is the correct disposition and
  had never been re-verified. The three new WARNs are all per-agent notes, which retires the
  rule this seat wrote on 2026-07-31 that any per-agent WARN is drift; it is replaced by a named
  expected set, so the eighth WARN is legible as new.

  **Recorded and not fixed, with the reason in each case.** The `.claude/agents/systems-designer.md:17`
  zero-cost constraint (a contract edit, Emory's); the `quality-bar` card's two defects (a
  manifest edit, [[systems-designer]] on Emory's go-ahead); the eight-file fill-suspension
  divergence, [[Claim Map]] **C15**, whose owners are split three ways; and the managed-block
  backlog, now **twelve** notes including [[Claim Map]] itself — **`build_graph` write mode was
  not run, because four of the twelve planned files are this session's out-of-bounds
  substantive work and the script offers no path filter.** A managed block is never
  hand-written, so there was no lawful partial run.

  **One thing closed on the file's authority rather than a report's.** The day's handoff listed
  the `digest.html.j2:120` site overclaim as open and routed to [[site-experience]]. Re-read at
  the end of this pass, `scripts/site_templates/digest.html.j2:120` already carries the repaired
  wording. Recorded closed in that seat note **because the file says so**; the handoff note is
  the stale copy. The inverse discipline applies throughout this pass: no PENDING or
  externally-gated item was converted to verified, and the eleven open rows in
  `analytics/locked_set/RETRIEVAL_LEDGER.md` are recorded as QUEUED or BLOCKED exactly as the
  ledger states them.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `.claude/agents/`, `prompts/`, `agents/`, `moc/`, `views/isds-workflow-3d/workflow.json`,
  `src/`, `scripts/`, `analytics/`, `fingerprint.yaml`, `HANDOFF.md`, `METHODOLOGY.md`,
  `README.md`, `templates/`, `lit-review/kim-memo.md`, `STATE_OF_THE_ANSWER.md`.*

- **2026-08-07** — Sixth deployment, standing every-3-days session. Fourteen adopted rules from
  the 2026-08-05, 08-06 and 08-07 councils landed in the seat notes that will read them —
  taxonomy 25, 26 and 27 into [[integrity-officer]] (`3ff5498`, `aa48406`), six chairman rules
  and the entity-blind relay qualification into [[council-chairman]], six relay method rules into
  [[research-analyst]] (`7adfd68`). The 08-07 taxonomy **numbering collision** recorded under both
  numbers and escalated rather than silently renumbered. Own drift fixed: a false commit citation
  in [[Agent Registry]] (`373cce6` credited with `9efafb0`'s fix), the registry's stale graph
  measurements (4 WARNs → 7, 11 pending blocks → 7), the closed `Project Machinery` broken link,
  and `HANDOFF.md:164`'s attribution of Opus 5 to the 2026-07-29 directive that produced Fable 5.
  Four escalations raised: the taxonomy collision, `check_currency.py` tracking 5 of 13 anchored
  notes and wired into no workflow, `build_graph`'s path-filterless run versus this seat's merge
  authority, and `COUNCIL.md`'s two stale statements now four days past their first escalation.
  **Two entries missing from this log are added below, dated to when the work happened.**
  *Audited against `7c08dcf`; paths: `.claude/agents/`, `agents/`, `prompts/`, `src/models.py`,
  `views/isds-workflow-3d/workflow.json`, `HANDOFF.md`, `COUNCIL.md`,
  `analytics/daily-research/`, `analytics/vault-sessions/`, `scripts/check_currency.py`,
  `.github/workflows/`, and every remote branch tip.*
- **2026-08-06 — recorded retrospectively on 2026-08-07, because this log did not carry it.**
  Vault corrections landed at `9971b52` ("docs(vault): the vault contradicted the repo on four
  facts") and `3f6e19d` ("fix: the corrections of 2026-08-06 were themselves partial, in six
  places"), touching [[Agent Registry]], [[Project Change Log]], [[systems-designer]] and
  `moc/Council.md`. **This note received none of it**, so the seat that owns the vault's memory
  was the one seat whose memory of two days' work was blank — the failure this note's 2026-08-04
  observation names, in its own file. Written from `git log`, not from recall.
- **2026-08-05 — recorded retrospectively on 2026-08-07.** Session record at
  `analytics/vault-sessions/2026-08-05.md`: [[Claim Map]] rows C13 and C14 written as a continuity
  gate before the council ruled on either; three stale claim-map rows corrected;
  [[Workflow Threads]] C7 closed; the five-mechanism third sense of "Ring 3" escalated to Emory. Full
  statement in [[Project Change Log]], 2026-08-05.
- **2026-08-04 (council session — fifth deployment, same date)** — Standing seat in the
  council convened on external reviewer feedback. **The finding is against this seat.** The
  reviewer's ten contradictions were tested one by one against this note's own remit: three
  (holdout size, empty-report behaviour, agent architecture) were inside the scope this seat
  declared for itself in the 2026-08-03 slice item 8 and were missed; two more were adjacent
  to surfaces it had just audited; five are genuinely outside every clause. Applying R1 of
  `analytics/council-sessions/2026-08-03-proposition-rule.md`, the first three are a
  discipline failure and are not repaired by widening a rule. Worse, item 8's own evidence
  citation is false — it points at a section of `agents/Project Change Log.md` that has never
  existed, making the deliverable-drift sweep's findings unrecoverable; that is the fourth
  false claim in the 08-03 entry and the 08-04 currency audit tested only three. **Not
  corrected in place here**, deliberately: it is escalated so Emory sees it uncorrected.
  Built `agents/Claim Map.md` — twelve claims, every file that states each, the twin list a
  fix must change together — as the artifact the registry and change log never provided.
  Referenced by path rather than wikilink, because this note already carries 6 direct links
  against a cap of 4 and a seventh would deepen a defect the registry records. Session
  record: `analytics/vault-sessions/2026-08-04-council.md`.
  *Audited against `c9050e6`; paths: `.claude/agents/obsidian-archivist.md`, `agents/`,
  `README.md`, `METHODOLOGY.md`, `HUMAN_REVIEW.md`, `fingerprint.yaml`, `src/classify.py`,
  `src/main.py`, `src/config.py`, `scripts/site_templates/`, `scripts/build_site.py`,
  `scripts/holdout_set.json`, `scripts/backtest_corpus.json`, `docs/`, `digests/`.*
- **2026-08-04** — Fourth deployment, standing every-3-days session. Ran the currency query
  the previous deployment adopted, and it caught that deployment's own unlanded work: three
  false claims in the 08-03 entry below, corrected in place; the canonical fabrication
  taxonomy landed in [[integrity-officer]] for real (23 entries, one citation each); four
  chairman rules and three analyst rules recorded in their seat notes for the first time;
  snapshot anchors added to all twelve notes instead of one; the flowchart's move to 30
  nodes / 44 edges reflected in [[Agent Registry]]; three `HANDOFF.md` statements corrected
  against `src/models.py`, `src/classify.py:58` and `state/source_health.json`. Two
  escalations raised: 17 unmerged operator ledger marks on
  `origin/chore/operator-marks-2026-07-27`, and the 2026-08-03 standing-rules council record
  now unrecoverable from git.
  *Audited against `b76f6c3`; paths: `.claude/agents/`, `agents/`, `src/models.py`,
  `src/source_health.py`, `views/isds-workflow-3d/workflow.json`, `HANDOFF.md`,
  `analytics/daily-research/`, `analytics/council-sessions/`,
  `analytics/verification_ledger.jsonl`.*
- **2026-08-03** — *Three claims in this entry are false against `main` and are corrected
  here on 2026-08-04; see slice item 1 above. What did land: this note's own 08-03 audit
  slice, via the conflict resolution of `8705f7a`. What did not: `Project Machinery` (never
  created), the chairman/analyst/integrity-officer note updates (no 08-0x content reached
  them), and the snapshot anchors on the other eleven notes. The entry is corrected rather
  than rewritten, because what it claimed is part of the record of how this failed.* Third
  deployment, by operator directive: verify that no agent carries old
  context. Recovered the orphaned 2026-07-31 vault build (`f195e21`) into the mainline,
  corrected two records `939deaa` had retroactively falsified, brought the chairman,
  analyst, integrity officer and analytics officer notes current with three sessions of
  adopted rules, added `Project Machinery` *(never created — see the 2026-08-04 correction
  at the head of this entry)*, and rebuilt [[Workflow Threads]] against the
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
