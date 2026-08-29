---
aliases: [Project Change Log]
tags: [agent, council]
hub: Council
---
# Project Change Log

**Currency anchor.** *Audited against `a24b9a9`.* Machine-owned; `scripts/reanchor.py` moves the sha to the session's last substantive commit in a notes-only close-out commit that `scripts/check_currency.py` excludes from drift as maintenance. Do not hand-edit the sha; the dated snapshot-anchor narrative below is preserved unedited as history.

Dated entries for material changes to the project's agents, models, sources, workflow, and
vault. **Every line cites a commit hash** — or, where a change is recorded before it is
committed, the exact file path *and* the branch it sits on, said in those words rather than
left to be inferred. Anything that can be cited neither way is not written here. Newest
first; dates are commit dates on the mainline of history.

Roster: [[Agent Registry]]. Open work by thread and owner: [[Workflow Threads]].

## 2026-08-25 (archivist session — eleventh deployment)

*Audited against `ad66a96` (`main`, clean tree, complete history after `git fetch --unshallow`
— 804 commits; the container's clone arrived shallow at 188 again); paths: `agents/`,
`prompts/`, `.claude/agents/`, `src/models.py`, `src/sources/`, `HANDOFF.md`, `METHODOLOGY.md`,
`README.md`, `scripts/`, `docs/`, `views/isds-workflow-3d/workflow.json`.*

- **No contract surface moved.** `git log c4f6825..HEAD -- .claude/agents/ prompts/
  src/models.py` returns **no commit** across 56 commits. Every model, prompt binding and seat
  contract is as it was on 2026-08-22.
- **An ORPHANED-COMMIT CITATION on this seat's own surface.** `agents/Project Change Log.md:1021`
  cited `80ad250` as the commit that froze the vault graph on 2026-07-21. `git cat-file -e
  80ad250^{commit}` fails and no commit on any branch carries that message; the only commits
  dated 2026-07-21 in the whole history are a daily council meeting and a sent marker. The entry
  is annotated in place, not rewritten — see below. Found by applying the taxonomy entry the
  council routed to this seat the same morning (`analytics/daily-research/2026-08-25.md:1375`).
- **`scripts/check_currency.py`'s docstring promises a check its code does not implement.**
  Lines 30-32 describe check **3, COMMITS**: "Any `` `<sha>` `` cited as closing or landing
  something must exist and be an ancestor of HEAD." The implementation at `:184` iterates only
  `PR_CITE_RE`, which is `` `<sha>`, PR #N `` — a **bare** sha citation is never checked. That is
  the guard-level reason the 2026-08-25 orphaned citation and this seat's `80ad250` both went
  uncaught. [[Workflow Threads]] **D9**.
- **`scripts/build_graph.py`'s block-replacement defect is wider than C8 recorded.** C8 says the
  pattern anchors to the *first* start marker. `:198` is `pat.sub(block, text)` with **no count
  argument**, so it replaces **every** start→end span in the file, and `:195-196` compiles the
  span non-greedy under `re.DOTALL`. A note that quotes the delimiters in prose loses everything
  from the quoted marker to the next end marker — each time. C8 refined, citation added.
- **A stale live sentence in D6, corrected.** The thread asserted that `grep -n "Model runtime
  fallbacks" HANDOFF.md` "returns nothing — the section has never been written." It now returns
  `HANDOFF.md:202`, written by hand by this seat on 2026-08-16 — in the same session that opened
  D6. The original finding is preserved as the dated observation it was; the live claim is
  corrected. The half that is still true — `record_fallback()`'s only caller is
  `src/research_brief.py:161` — is stated separately.
- **Anchors restamped to `ad66a96`** on [[Agent Registry]], [[Claim Map]], [[Project Change Log]]
  and [[Workflow Threads]].
- **Carried, unchanged, with dates:** **D6** model gap at day thirteen; **D5** at day twelve
  (eight of nine definitions still never name their own vault note); **D7** METHODOLOGY counts;
  **D8** second "Zero-cost" binding; **C11** the site's nine-vs-ten, now nine days live;
  **F1** the operator-marks branch at day twenty-nine; **C17** the currency false positive,
  with `pipeline-guards` red on `main` for eight days across thirteen consecutive runs.

## 2026-08-22 (archivist session — tenth deployment)

*Audited against `c4f6825` (`main`, clean tree, complete history after `git fetch --unshallow`
— 748 commits); paths: `agents/`, `prompts/`, `.claude/agents/`, `src/models.py`,
`src/sources/`, `HANDOFF.md`, `METHODOLOGY.md`, `README.md`, `scripts/site_templates/`,
`docs/`, `views/isds-workflow-3d/workflow.json`.*

- **The public site tells the professor there are nine sources, directly above a chart that
  says ten.** `docs/how-it-works.html:58` reads "the first band is the nine public sources
  checked"; the SVG inlined at `:96` of the same page renders "WHERE WE LOOK — THE 10 SOURCES,
  CHECKED EVERY RUN" with ten chips. `:7`'s meta description also says nine. The source strings
  are `scripts/site_templates/how_it_works.html.j2:3` and `:27`. Live since `44550ca`
  (2026-08-17). `check_site_sync.py` cannot see it — template and built page agree, and both are
  wrong. Owner **[[site-experience]]**; escalated, not edited. [[Claim Map]] **C11**.
- **`METHODOLOGY.md:33` describes a nine-source fleet and an eight-query Bing lane.**
  `src/sources.all_sources()` returns **10** (GDELT absent from the memo's enumeration);
  `src/sources/bing_news.py:23` defines `QUERIES` with **12** entries. Both read from the code,
  not from `44550ca`'s message. Emory's own document — escalated as [[Workflow Threads]] **D7**.
- **[[Claim Map]] C11 corrected, and the correction is against this seat.** The 2026-08-17
  snapshot-anchor block wrote that the source-count row was "satisfied by that same commit (ten
  stated once, everywhere)". Two errors: the source-count row is **C11**, not C12 (C12 is Model
  assignments); and the row was **not** satisfied. That sentence was taken from `44550ca`'s
  commit message instead of from a reading of the files. Struck in place with the original
  wording quoted, and C11 re-read cell by cell at `c4f6825`. **The rule this deployment adopts:
  a commit message is a claim about a change, never a reading of the files after it — a claim-map
  row is closed only by re-reading every cell it names.** This is the 2026-08-16 rule
  ("a guard's exit 0 licenses only the claim the guard actually tests") in a second form.
- **`HANDOFF.md` sources table did not carry GDELT** five days after the module landed, under a
  heading reading "current reality". Added the `gdelt` row (`src/sources/gdelt.py`, `44550ca`),
  corrected the `bing_news` row to record **12** queries, and added a measured count line naming
  all ten instances returned by `all_sources()` and stating which two the table's inherited
  build-time-scout scope omits. Mine, fixed here.
- **D6 re-measured at day ten.** [[integrity-officer]] has self-reported `REQUESTED
  claude-opus-4-8 → ACTUAL claude-opus-5` on ten consecutive days — six of them since the last
  archivist pass (`analytics/daily-research/2026-08-17.md:719`, `2026-08-18.md`,
  `2026-08-19.md:1148`, `2026-08-20.md:1113`, `2026-08-21.md:1024`, `2026-08-22.md:1080`).
  `git log d997c32..HEAD -- .claude/agents/ src/models.py` returns **no commit**. Emory's.
- **F1 re-measured at day twenty-six**, identical counts a fourth time: `origin/main` 37
  `claim_created` / 21 `verification_changed` / 37 ids; `origin/chore/operator-marks-2026-07-27`
  40 / 38 / 40. `main`'s ledger last written by `8891c21` (2026-07-27). Emory's.
- **D8 opened** — `.claude/agents/site-experience.md:20` carries a second "Zero-cost" binding
  beside the known `systems-designer.md:17`, both falsified by `README.md:6` on 2026-08-08.
  Contract surface; escalated.
- **A broken wikilink in this seat's own note, fixed.** `agents/obsidian-archivist.md:706` wrapped
  `[[Workflow Threads]]` across a line break, so Obsidian resolved nothing and
  `build_graph.py --dry-run` listed it under "links to nonexistent notes". Rewrapped; the dry run
  no longer lists this note.
- **A guard hazard recorded for the next session.** This container's clone arrived **shallow**
  (196 commits). Against it `check_currency.py` reported **7** failures including three hard
  `FAIL`s — `373cce6`, `9efafb0`, `ae42639` "is not a commit". All three exist. After
  `git fetch --unshallow` the same guard reports the true count with zero `FAIL`s. CI is
  unaffected (`.github/workflows/pipeline-guards.yml:172` sets `fetch-depth: 0`). Written into
  [[Workflow Threads]]' snapshot block.
- **Currency: 4 failed → 2.** [[Agent Registry]], [[Claim Map]], [[Workflow Threads]] and this
  note restamped to `c4f6825`. `STATE_OF_THE_ANSWER.md` left stale by decision — it is
  [[research-analyst]]'s living memory and the 2026-08-08 rule against restamping another seat's
  file governs.
- **The 2026-08-19 session of this standing every-3-days series did not run.** Last record before
  this one is `analytics/vault-sessions/2026-08-16.md` (`5138312`); `git log --all` finds no
  2026-08-19 vault session on any branch. Six days, not three.

## 2026-08-17 (second entry — source outage repair)

*Audited against `d669688`.*

- **The weekly run emailed a status cycle, then crashed its own commit-back, and its
  degradation diagnosis was wrong three ways.** The archive validator refused the first
  gate-held match in the project's history (meta matches=1, disk 0 — the arithmetic sent
  watch_list_leads to -1), so the run died after sending and the digest folder, telemetry
  and seen-state never reached main; the held item is recovered by the re-run. The three
  DEGRADED labels: iisd_itn was a live quarterly feed in a quiet quarter, google_alerts
  was three platform-dead Google feeds polled as husks, italaw is a hard 403 bot-challenge.
  Fixes: gate-aware meta and validator (held_for_review reconciles), zero-streak refinement
  probes (QUIET / PLATFORM-EMPTY / NOT-READ vs generic DEGRADED), [SOURCE ALERT] subject
  prefix whenever health warnings exist, dead Google feeds retired in alerts.yaml.
  OPERATOR: per-alert Talkwalker feeds are still needed to replace the retired queries.

## 2026-08-16

*Audited against `d997c32` (`main`, clean tree, complete history after `git fetch --unshallow`
— 621 commits); paths: `.claude/agents/`, `agents/`, `prompts/`, `src/models.py`,
`scripts/check_models.py`, `scripts/check_currency.py`, `scripts/build_graph.py`,
`analytics/daily-research/`, `analytics/council-log.md`, `analytics/verification_ledger.jsonl`,
`views/isds-workflow-3d/workflow.json`, `HANDOFF.md`, and every remote branch tip.*

- **No commit touched a contract surface in this window.** `git log 8ea2ee1..HEAD --
  .claude/agents/ prompts/ src/models.py METHODOLOGY.md README.md scripts/site_templates/
  views/isds-workflow-3d/workflow.json` returns **no commit**. The 44 commits since `8ea2ee1`
  are the 2026-08-14, 08-15 and 08-16 council sessions (`dc4ba93`, `3a9d2f1`, `ba6b7ec` and
  their parts) plus fetch-relay and sent-marker chores. No agent definition, prompt, model
  constant or flowchart card changed.
- **The five seats documented as Claude Opus 4.8 are pinned to it by nothing.** All nine
  definitions declare `model: opus`; that key selects a tier, not a version, as
  `scripts/check_models.py`'s own docstring states. Recorded as [[Workflow Threads]] **D6**,
  qualified under the roster in [[Agent Registry]], and at the Model blocks of
  `agents/obsidian-archivist.md` and `agents/integrity-officer.md`.
- **The discrepancy is observed, not inferred, from two seats.** [[integrity-officer]]
  self-reported `REQUESTED claude-opus-4-8 → ACTUAL claude-opus-5` unasked in
  `analytics/daily-research/2026-08-12.md:750`, `2026-08-14.md:576`, `2026-08-15.md:693` and
  `2026-08-16.md:731`; `analytics/council-log.md:23` carries it as "second consecutive day".
  On 2026-08-16 [[obsidian-archivist]] queried its own session runtime and read
  `claude-opus-5` against a note pinning `claude-opus-4-8`.
- **`record_fallback()` has never fired on a council path.** `src/models.py:18` requires a
  runtime substitution be written to `HANDOFF.md` through it; its only caller is
  `src/research_brief.py:161`, and `HANDOFF.md` has no "Model runtime fallbacks" section.
  Escalated — `src/` is not this seat's to edit.
- **A 2026-08-13 vault claim is corrected.** That session wrote "No model drift exists", citing
  `check_models.py` exit 0. The guard cannot observe a runtime and says so in its docstring, and
  the integrity officer's first report predated the session by a day in a directory the session
  read. Corrected in `agents/obsidian-archivist.md`; the original sentence stands in
  `analytics/vault-sessions/2026-08-13.md` as the dated record it is.
- **`prompts/council_roundtable.txt:73` instructs an agent to write "Jack".** The line reads
  "anything needing Jack's decision or sign-off". The house rule is that Emory is the operator
  in project artifacts; this is a live instruction, not a dated record. `prompts/` is a contract
  surface — escalated to Emory, not edited.
- **`.claude/agents/systems-designer.md:17` still says "zero-cost"**, eight days after
  `README.md:6` was corrected to record that the classifier makes paid model calls. Carried
  unchanged from 2026-08-13; contract surface, Emory's.
- **`scripts/check_currency.py` flags every landed archivist session as drift against itself.**
  Found on landing: the guard went from 1 failed to 3 the moment `5138312` merged, reporting
  [[Project Change Log]] and [[Workflow Threads]] stale against the commit that wrote them. Its
  `_is_maintenance` exemption (`scripts/check_currency.py:93-105`) tests `files <= set(TRACKED)`,
  and a real session commit always also touches `HANDOFF.md`, seat notes and its own session
  record — none tracked — so the exemption never fires. The same misfire occurred at `67c80f7`
  on 2026-08-13 and was restamped as though it were real drift. Opened as **C17**; escalated to
  [[systems-designer]]. Anchors deliberately **not** restamped to the merge commit.
- **Orphan check: no new stranded work.** `git cherry` against `origin/main` reports six
  branches with unlanded commits, the same six as 2026-08-13 and with the same dispositions.
  All three `vault/*` branches — `vault/archivist-2026-08-13`,
  `vault/archivist-2026-08-07-followup`, `vault/recover-orphaned-work` — are confirmed ancestors
  of `origin/main`. **F1 is unchanged at day twenty.**

## 2026-08-13

*Audited against `8ea2ee1` (`main`, clean tree, complete history after `git fetch --unshallow`
— 584 commits); paths: `.claude/agents/`, `agents/`, `prompts/`, `src/models.py`,
`src/integrity_gate.py`, `scripts/`, `analytics/verification_ledger.jsonl`,
`.github/workflows/`, `views/isds-workflow-3d/workflow.json`, `HANDOFF.md`.*

- **A change-log claim is retracted, and it is this note's sister file.** [[Workflow Threads]]'s
  2026-08-11 entry stated "F1's seventeen verification marks reach `main` with this merge."
  They did not. `git show --stat 0a67756 -- analytics/verification_ledger.jsonl` is empty;
  the ledger on `main` is blob `f3dbbf6`, last written by `8891c21` on **2026-07-27**, and
  `origin/chore/operator-marks-2026-07-27` is still not an ancestor of `main`. The line is
  struck in place, not deleted. Counted from both blobs: `main` holds 37 claims / **21 marks**,
  the branch holds 40 / **38** — the same figures F1 recorded on 2026-08-04, seventeen days ago.
- **The three stranded claims are demonstrably invisible to the integrity gate.**
  `src/integrity_gate.py:150-177` resolves candidates by exact claim-id lookup through
  `verify.replay` / `verify.current_status`. Replaying both blobs: `7511d41b67ec`
  (*Hela Schwarz v. China*), `f4375b9fb9f4` (UNCITRAL WG III 53rd session) and `f40761bdb9b0`
  (Svea Court of Appeal, *Okuashvili v. Georgia*) each return `unverified` against `main` and
  `operator_verified` against the branch. All three carry `quote_ok: true` and `scope_ok: false`.
  Recorded in [[Workflow Threads]] **F1**; the ledger is operator-owned and was not touched.
- **Adopted method rules are recorded outside the read path of the seats they bind.** Eight of
  nine `.claude/agents/` definitions never name the seat's own vault note, while those notes
  carry sections marked binding (`agents/research-analyst.md:59-142`,
  `agents/council-chairman.md:46-133`, `agents/analytics-officer.md:40-62`). Ten of the
  analyst's eleven rules, and all four `label: 1` rows of `scripts/holdout_set.json`, are absent
  from that seat's read path — the mechanism behind the 2026-08-03 holdout assertion. Opened as
  [[Workflow Threads]] **D5** and recorded in [[research-analyst]] and [[Agent Registry]];
  **not fixed**, because `.claude/agents/` is a contract surface and Emory's.
- **No agent, model or prompt change.** `git log 667772c..HEAD -- .claude/agents/ prompts/
  src/models.py` returns no commit; `scripts/check_models.py` exits 0 over twelve cards.
- **`scripts/build_graph.py` write mode not run — thirteenth consecutive session, and the
  arithmetic has shifted.** `--dry-run` at `8ea2ee1` plans managed-block edits to **23** notes.
  **20 are inside this seat's self-merge set** (`analytics/` ×19, `agents/Claim Map.md`); three
  are not — `BOUNDED_CHANGE_PROTOCOL.md`, `prompts/carrying_span_rule.md`,
  `lit-review/BIBLIOGRAPHY_TEMPLATE.md`. The script has no path filter, so a full run still
  cannot land under archivist authority ([[Workflow Threads]] **C12**), but the out-of-bounds
  share has fallen from 14-of-17 to 3-of-23.
- **Two measurement conventions corrected.** `pytest` and `scripts/check_sources.py` cannot pass
  in a clean clone — both require files under gitignored `seeds/` (`.gitignore:2`), and CI never
  runs the full suite (`.github/workflows/pipeline-guards.yml` invokes named test files only), so
  every "N passed" figure in this vault is a reading from Emory's machine. And the orphan test
  `git merge-base --is-ancestor` reports 45 unlanded branches where `git cherry` reports 6; the
  difference is squash merges, and `git cherry` is the honest query for "did this branch land".

## 2026-08-11

*Audited against `bffe79a`.*

- **Integration to `main`.** The 2026-08-08/09 repair and audit work, until now uncommitted
  on `fix/restore-council-label`, was merged with the 2026-08-10 council record and pushed
  as reviewable commits: runtime/tests (`667772c`), documentation/vault (`bffe79a`), the
  site rebuild (`60f2a5b`), the check_currency maintenance-exclusion fix (`9a6f3e8`), and a
  currency-anchor pass across the five tracked notes. Desktop packets, seeds, detector
  receipts and the private reply record were excluded by design.

## 2026-08-09

*Audited against `2686422`* plus the uncommitted working tree on branch
`fix/restore-council-label`; paths: `src/`, `tests/`, `scripts/`, `prompts/`,
`.github/workflows/`, `analytics/`, `seeds/`, `working/`, `agents/`, `moc/`,
`views/isds-workflow-3d/workflow.json`, `METHODOLOGY.md`, `README.md`, `HANDOFF.md`,
`PLAN.md`, `STATE_OF_THE_ANSWER.md`, `fingerprint.yaml`.

**Everything in this section is UNCOMMITTED, on branch `fix/restore-council-label`**, cited
by file path and branch under this note's rule for changes recorded before they are committed.
**Test suite: 564 passed, 5 xfailed** — re-run by this seat at the head of this pass, not
copied from a report.

- **The independent audit was answered, and one of its answers was a relabelling.** The
  previous session's "live e2e" verification was re-described as what it actually was, a
  **fixture-backed simulation**, and `STATE_OF_THE_ANSWER.md` gained the currency anchor it
  had never carried — `STATE_OF_THE_ANSWER.md:10` now reads "audited against 2686422". The
  effect is mechanical and this seat re-measured it: `scripts/check_currency.py` now reports
  **9 currency claims across 5 notes, 0 failed**, exit 0, where on 2026-08-08 it reported one
  failure and that failure was this file. [[Workflow Threads]] **D3** closes on that run.
  *(`STATE_OF_THE_ANSWER.md`, `analytics/session-manifest-2026-08-09.md`.)*
- **A second and stronger publication gate, and it is the one that closes the hole the fill
  suspension left open.** `VALIDATION_STATUS_ONLY` (`src/config.py:42-74`, **default ON**)
  holds **all** item-level publication — *including items at or above 40* — and the research
  brief, until production-path validation authorizes it. The reasoning is in the config
  comment and is worth repeating because it is the whole point: `prompts/classifier.txt`
  Example 4 teaches the model to score an off-theme judicial case at **55**, and
  `select_surfaced` publishes on score alone, "so that item publishes today with the fill
  suspended… a gate that only holds back the scores it already distrusts is not a validation
  gate." It is deliberately a separate flag rather than a stronger setting of
  `FILL_FLOOR_SUSPENDED` (`src/config.py:59-62`), so restoring the fill cannot reopen item
  publication as a side effect, and the fill flag cannot bypass it. A gated cycle reports the
  **held count** rather than an absence (`src/main.py:615-618`, `:700-706`, `:809-811`).
  **This creates a new claim divergence and it has a row: [[Claim Map]] C16.**
  *(`src/config.py`, `src/main.py`, `src/render.py`.)*
- **STATE_MODEL_V2 stopped being prose and became code.** `src/rings.py` derives, in shadow on
  every cycle, per-ring strengths, a deterministic treaty-nexus finding, evidence location and
  validity, and a lane. The semantic V2 path is built end to end — `src/classify_v2.py` with
  `prompts/classifier_v2.txt` wired for shadow — but `V2_SHADOW_CALLS` defaults **off**
  (`src/config.py:154-195`), so **every default-run verdict is labelled `lexical_only`**, and
  `V2_SHADOW_CALLS=replace` is refused outright (`V2_SHADOW_CALLS_FORBIDDEN`,
  `src/config.py:156`). Verdicts carry `claims_source` provenance, and `guard_demoted` fires on
  **every V1 ring claim**, because V1 supplies no spans — a demotion that is the correct
  reading of V1 rather than a defect in V2. `STATE_MODEL_V2="on"` is refused until
  `STATE_MODEL_V2_PUBLICATION_READY` (`src/config.py:98`, `:109-111`), which is `False`.
  *(`src/rings.py`, `src/classify_v2.py`, `prompts/classifier_v2.txt`, `src/config.py`.)*
- **The 7-vs-4 outcome question was resolved losslessly, and the enumeration grew by the size
  of the thing that had been missed.** Seven logical states map onto four operational outcome
  values plus recorded metadata; the exhaustive state space in `tests/test_rings.py` moves from
  12,288 to **21,504** (64 ring configurations × 4 nexus × 4 evidence locations × 3 validities
  × 7). `src/rings.py:112` states the arithmetic. **Tail provider failures are now counted** —
  they were under-counted by exactly the size of the tail. Rationale:
  `analytics/state-space-resolution-2026-08-09.md`. *(`src/rings.py`, `tests/test_rings.py`.)*
- **Workstream F shipped, off by default.** `src/triage.py` + `prompts/triage.txt`, a
  pre-enrichment semantic lane that lets a paraphrase the keyword fingerprint cannot see reach
  enrichment on model rank. `TRIAGE_ENABLED` defaults **0** (`src/config.py:220`); the sort is
  deterministic; a provider absence is **recorded, not misreported**. Adversarial tests
  accompany it. **Design (c), the stratified tail audit, is a config stub only** —
  `TAIL_AUDIT_N = 0` (`src/config.py:243`), expressly unimplemented, and recorded that way
  rather than as shipped. *(`src/triage.py`, `prompts/triage.txt`, `src/config.py`,
  `tests/test_triage.py`.)*
- **Workstream G shipped, and its grammar has three limitation clauses rather than one.** The
  headline lane (`src/headline_lane.py`) generates from a closed grammar with no slot for a
  legal or thematic conclusion. The clause is **keyed on evidence location**
  (`src/headline_lane.py:81-85`), and the reason is a real error the single-clause design would
  have produced: a comparator whose body *was* retrieved may not claim its body is paywalled.
  Hence `LIMITATION_PAYWALLED` / `LIMITATION_UNRETRIEVED` / `LIMITATION_RETRIEVED`, a closed
  set the guard enforces membership against. `scripts/check_headline_lane.py` holds the output
  byte-identical. The public-label mapping was corrected so
  `HEADLINE_ONLY_LIBRARY_LEAD` is not the name given to an accessible-body item.
  *(`src/headline_lane.py`, `scripts/check_headline_lane.py`, `src/rings.py`.)*
- **The guards became guards.** `.github/workflows/pipeline-guards.yml` wires
  telemetry-privacy, seen-integrity, headline-lane, lock and currency — the currency job with
  **`fetch-depth: 0`**, without which the check cannot see the history it asserts against
  (`:143`) — plus each guard's own **planted-violation tests** (`:101-111`), so the guards are
  themselves tested rather than merely run. `scripts/check_lock.py` was written; run today it
  reports the empty set as **the designed current state, not an error**, and exits 0.
  [[Workflow Threads]] **B8** closes on the file. *(`.github/workflows/pipeline-guards.yml`,
  `scripts/check_lock.py`.)*
- **The comment package's five audit contradictions were closed, and one of them was closed by
  going and reading the document.** **H&H v. Egypt (ICSID ARB/09/15) is CLOSED BY RETRIEVAL:**
  the Decision on Jurisdiction of 5 June 2012 (`ita1012.pdf`) and the Award's Rule 48(4)
  excerpts of 6 May 2014 (`italaw7979.pdf`) are in `seeds/` — this seat confirmed both files on
  disk — with **21 spans verified**. The retrieval **corrected two claims rather than
  confirming them**: the "want of causal link" disposition was true of the corruption claim
  only (¶ 399), denial of justice having failed on "manifestly unjust" (¶ 403); and the
  economic-sector attribution was **deleted** rather than re-attributed a third time. The dead
  `italaw.com/cases/542` URL — a 404 — was replaced with the real document URLs. Also:
  "structural" became **"a deliberate scope boundary"** (Ferguson draws it himself, at 340,
  in the sentence whose note 37 cites Kim); Item 6's balancing claim was narrowed; the
  disclosure categorical was qualified; Part 5 items 5, 13 and 15 updated. **The full Award
  remains unpublished** — every quotation and the zero-occurrence IP screen are scoped to the
  published excerpts and the Decision on Jurisdiction. That is recorded as a **permanent scope
  limit, not a gap slug**, which is the correct disposition and the distinction is the point.
  *(`working/benavides-comment-replies-2026-08-08.md:340`, `:433`, `:446`, `:459`;
  `seeds/HH_v_Egypt_ARB-09-15_*`; `lit-review/ferguson-memo.md`.)*
- **Walter Writes round 2: three passages, zero adopted.** One exempt by construction (masked,
  it is a near-pure sentinel chain with nothing to work on); two run and **rejected at the
  gate** — the first dropped the passage's final two sentences and converted "the opinions"
  (the court's) into "the author's opinions"; the second destroyed a sentinel and garbled the
  triple-identity sentence. Canonical text stands for all three. The fail-closed humanizer rule
  has now been exercised twice and has adopted an output only where the mechanical gate passed.
  *(`working/benavides-comment-replies-2026-08-08.md:6`.)*
- **METHODOLOGY §IX updated** to 21,504, the three off-by-default capabilities, and the CI
  wiring (`METHODOLOGY.md:69`). Not this seat's file; recorded, not edited.
- **A designer deviation of record, and it is a live hazard.** `scripts/check_site_sync.py`
  **rebuilds `docs/` in place** — `scripts/check_site_sync.py:25` runs `build_site.py` with no
  temporary directory and then diffs the working tree (`:31`). It is therefore **a mutating
  command wearing the name of a check**, and it reverted `docs/` to HEAD on the belief that it
  was stamp-only. `docs/` will be rebuilt from source in the integrator's final battery.
  Logged as an open defect: [[Workflow Threads]] **B9**. *(`scripts/check_site_sync.py`.)*
- **Recorded, deliberately not fixed.** `STATE_OF_THE_ANSWER.md:28`'s clause "every disclosure
  case … was **brought in a court** to prevent or restrict disclosure" holds **as scoped** to
  the four cases it names (InterMune, AbbVie, PTC Therapeutics, Vanda D.D.C.), but the sentence
  would need rewording if the **Vanda CFC takings matter** were ever added to that list — a
  Court of Federal Claims takings action is not a suit to prevent disclosure. Recorded as
  [[Workflow Threads]] **D4**; the file is [[research-analyst]]'s and is not edited here.
- **Still Emory's, still not edited.** `.claude/agents/systems-designer.md:17` binds that seat
  to "the zero-cost constraint" that 2026-08-08's code reading falsified. Editing
  `.claude/agents/` is a contract change. Recorded for the second consecutive session.

## 2026-08-08

*Audited against `2686422`* plus the uncommitted working tree on branch
`fix/restore-council-label`; paths: `src/`, `scripts/`, `tests/`, `templates/`, `analytics/`,
`digests/`, `lit-review/`, `working/`, `.claude/agents/`, `prompts/`, `agents/`, `moc/`,
`views/isds-workflow-3d/`, `METHODOLOGY.md`, `README.md`, `HANDOFF.md`,
`STATE_OF_THE_ANSWER.md`, `fingerprint.yaml`.

**Everything in this section is UNCOMMITTED, on branch `fix/restore-council-label`**, and is
cited by file path and branch under this note's own rule for changes recorded before they are
committed. Test suite green **as that session left it**: **414 passed, 5 xfailed, 32 tests
new**. *(Dated reading, not a current one — see the 2026-08-09 section above, where the suite
stands at **564 passed, 5 xfailed**. The 414 is kept as the record of what 08-08 measured.)*

- **The Telefónica double-publication had a mechanism, and it was found.** `research_brief.generate_brief`
  had **no exception handler and ran BEFORE `save_state`** in `src/main.py`, so a failure in
  the brief step discarded the run's entire seen-state *after* the digest had already been
  written. The same italaw case page therefore came back as unseen on the following day and was
  published twice, with **contradictory verdicts — 32 with a ring on 06-09, 28 with none on
  06-10, from the same URL and the same source text**. Fixed, with the regression test
  `test_a_failing_research_brief_cannot_unwrite_the_seen_state`. **This is the entry to reread
  before the next "harmless ordering" change:** nothing about a brief-generation step looks
  like it can reach the archive, and it silently governed it. Both archive entries now carry
  dated cross-references to each other. *(`src/main.py`, `tests/test_pipeline.py`, branch
  `fix/restore-council-label`.)*
- **Publication is constrained by default, and eight files did not get the message.**
  `FILL_FLOOR_SUSPENDED` now defaults ON (`src/config.py:31-39`): items scoring 25–39 are no
  longer surfaced, and a cycle in which nothing reaches 40 sends a status note whose single
  authoritative wording lives at `src/render.py:59` and is asserted verbatim by
  `tests/test_pipeline.py:951`. **The floor was not raised and the numbers did not move**,
  which is what makes the resulting drift invisible to every numeric guard: `RELEVANCE_FLOOR`
  is still 25 and `MIN_DIGEST_ITEMS` still 6, so `scripts/check_claims.py` passes while eight
  statements of the old behaviour stand, one of them the public homepage
  (`scripts/site_templates/index.html.j2:186`) and one of them `METHODOLOGY.md:49`, **eighteen
  lines above the addition at `:67` that suspends the rule it describes.** Recorded as a new
  row, [[Claim Map]] **C15**, and as [[Workflow Threads]] **B5**. *(`src/config.py`,
  `src/main.py`, `src/render.py`, `templates/digest.html.j2`.)*
- **The instrument has never been zero-cost, and the README now says so.**
  `classify_item(item, provider=None)` does **not** force the keyword path; it falls through to
  `os.environ["MODEL_PROVIDER"]`, so the below-cutoff tail has been model-classified in
  production throughout (`analytics/instrument-map-2026-08-08.md` §4). `README.md:3-9`
  corrected: "low-cost, roughly cents per run, not free." **The vault cascade this triggered is
  the reason it is logged here rather than only in the code notes:**
  `.claude/agents/systems-designer.md:17` binds that seat to "the zero-cost constraint" and is
  now falsified. The **vault note** [[systems-designer]] is corrected; the **definition** is
  not, because editing `.claude/agents/` is a contract change and belongs to Emory. Escalated.
- **Per-candidate telemetry, and an admission about what cannot be recovered.**
  `src/telemetry.py` writes one record per candidate per run — hashes and bounded structured
  values, **never article text**, enforced by `scripts/check_telemetry_privacy.py`, which fails
  the build on any planted text field. The path a candidate took, including *which classifier
  actually scored it*, is reconstructible for the first time. For every archived run before
  this date it is not: per-item classifier identity was computed and discarded, and for **five
  of the fourteen** published entries it is **unrecoverable**
  (`analytics/retrospective-audit-2026-08-08.md` §4). Nine of the fourteen are recoverable by
  arithmetic rather than by record — they score **25**, which the deterministic scorer cannot
  emit, its reachable set in [20,40] being {28,29,30,31,32,33,40} plus 35 via the
  negative-signal cap.
- **Seen-state is now outcome-gated, and abandonment is loud.** Every entry records *why* it is
  there — classified, keyword-scored by design, bootstrap-indexed, or abandoned after three
  attempts — and a candidate whose classification fails is no longer marked seen at all. It
  goes to a retry queue (`state/deferred.json`) with an attempt count, and a third failure
  writes a durable line to `analytics/abandoned_candidates.jsonl` that
  `scripts/check_seen_integrity.py` cross-checks, failing the build on a missing record.
  Legacy state is migrated at read time. *(`src/state.py`, `src/classify.py`, `src/main.py`.)*
- **Three new guards exist; none of them runs in CI.** `check_telemetry_privacy.py`,
  `check_seen_integrity.py` and `telemetry_query.py` are **untracked files with no workflow
  entry**. A fail-closed guard that is not wired is a script. [[Workflow Threads]] **B8**,
  blocked on Emory (**C11**).
- **The archive was audited against itself and two council records lost.** `analytics/retrospective-audit-2026-08-08.md`
  re-derives every figure from `digests/*/articles/*.md` and `digests/*/meta.json` rather than
  from any council record, "**because two of those records disagree with the files**". Findings:
  14 article files are **13 distinct URLs and 12 distinct underlying matters**; **four** entries
  display a ring at score 25, not five — the chairman's 2026-08-08 ruling had included
  Okuashvili, which sits at 28; **five** annotations state a negative thematic conclusion about
  their own item and **one** states it cannot assess, so **6 of 14 published entries disclaim
  themselves**, and all were mailed as watch-list leads. Two of the four ring-at-25 entries are
  substantively **unsupported** and additionally contradict the classifier contract. **Nine
  dated corrections were appended to the archive and nothing was rewritten.**
- **A gap closed on primary sources; two claim classes withdrawn for lack of them.** The two
  *Vanda Pharmaceuticals Inc. v. United States* opinions, No. 23-629C (Fed. Cl.), slip ops of
  18 Jan. 2024 and 22 Jan. 2025, were retrieved 2026-08-06 and are held at `seeds/` — which is
  **gitignored, so they will never appear in a commit**; the retrieval ledger carries the paths
  for that reason. The gap at `lit-review/kim-memo.md:206` is **CLOSED on slip-op-only
  citations**, with reporter page pins and appellate status **expressly excluded** and the
  Federal Circuit docket still QUEUED. Withdrawn and kept withdrawn: the claim that the
  *Saluka* and *Bovine Hides* passages "have now been extracted and verified", which had **no
  source anywhere in the repository**. Two readings of Kim corrected against her own text — she
  raises the institutional question **in her abstract**, and her footnote 23 had **already**
  qualified provisional relief at `STATE_OF_THE_ANSWER.md` line 28, verified 6 August. *(The
  project's own record refuted its own later premise.)*
- **A rewriting pass was run fail-closed and rejected five times out of seven.** All seven
  substantive replies went through a humanizer with **every quotation, citation and pinpoint
  sentinel-masked**; two passed and were surgically repaired, **five were rejected outright**
  for fabricated quotation, flipped negation, hallucinated rule, and two sentinel
  destructions; two were exempt. Entered as a binding rule for [[integrity-officer]] and
  [[research-editor]] in [[Agent Registry]].
- **Methodology disclosure.** `METHODOLOGY.md:54` adds the exact Clopper–Pearson 95% intervals
  — **[0.19, 0.99]** on three-of-four — and records that the harness evaluates at forty, a
  boundary **no candidate has crossed in 347 screenings**. `:67` adds Part IX describing the
  implemented Phase 0/1/H behaviour and says in terms that D/E, F and G are "**development work
  behind a disabled flag and are not production behaviour as of this date**". The Apotex
  caption repair of 2026-08-06 is disclosed by **amendment** — `:52` was not rewritten, which
  is what preserved the nine declared mirrors that point into it.
- **Vault.** [[Claim Map]] re-pointed against the current tree and gains **C15**; nine rows
  recorded as closed with their tables retained; the snapshot anchor moves to `2686422` + branch.
  [[Workflow Threads]] gains B5–B8 and C11–C14 and rewrites D1. [[Agent Registry]] re-audited,
  no roster change, with the expected-WARN set restated at seven and the managed-block backlog
  at twelve notes — one of them [[Claim Map]] itself, which has never carried its block.
  Session record: `analytics/vault-sessions/2026-08-08.md`.

## 2026-08-07

**Recorded 2026-08-08. This section was missing entirely** — four commits landed on 2026-08-07
and this note's newest entry was 2026-08-06, so a day of committed work had no dated line. It
is written now from `git log`, with each line carrying its hash.

- **The site's human-review disclosure became a number that can move.** `33861fd` ("feat: make
  the 'no human has checked this' disclosure a number that can move") replaced the universal
  safeguard claim on `how_it_works` — "no claim is published as fact without a human check
  against its original source", which neither the review log nor the ledger supported — with a
  **counted** disclosure rendered from the ledger. This closes the second leg of [[Claim Map]]
  **C6**, whose first leg (the intra-file contradiction in `HUMAN_REVIEW.md`) is also gone.
  `9352b0f` rebuilt `docs/` for it.
- **The council framing was restored on the flowchart.** `2686422` ("fix(chart): restore 'THE
  AI RESEARCH COUNCIL' — the seats are real agents"). Recorded here because it moves in the
  *opposite* direction from the `METHODOLOGY.md` rewrite that retired the phrase "standing
  council", and the two are compatible only on a distinction worth stating: **the seats are
  genuine agent invocations, and they are not standing background processes.** [[Claim Map]]
  C7 now records both.
- **The third Vanda matter was recorded as a gap rather than summarised.** `25dfdd0`
  ("docs(kim): record the third Vanda matter as a gap, not a summary") marked it
  `[PENDING — citation recorded, source not retrieved, no holding asserted here.]`. **That
  restraint is what made the 2026-08-08 closure clean**: when the slip opinions were read, there
  was no prior summary to reconcile against, only a gap to close.

## 2026-08-07

*Audited against `7c08dcf`; paths: `.claude/agents/`, `agents/`, `prompts/`, `src/models.py`,
`views/isds-workflow-3d/workflow.json`, `HANDOFF.md`, `COUNCIL.md`, `README.md`,
`METHODOLOGY.md`, `scripts/site_templates/`, `docs/`, `scripts/check_currency.py`,
`scripts/check_models.py`, `scripts/build_graph.py`, `.github/workflows/`,
`analytics/daily-research/`, `analytics/vault-sessions/`, and every remote branch tip.*

- **Fourteen adopted rules reached the seat notes three days late, and the lateness cost the
  council a taxonomy number.** Between 2026-08-05 and 2026-08-07 the council adopted taxonomy
  entries 25, 26 and 27, six chairman rules, six analyst relay rules and one standing relay
  qualification. `grep -c "2026-08-0[567]" agents/*.md` returned **0** for all nine seat notes
  bar `systems-designer.md`. The measurable consequence: `agents/integrity-officer.md` — the
  taxonomy's canonical home, which the officer's own mandate directs it to read rather than
  recite — carried the heading *"24 entries as of 2026-08-04"* while entry **27**
  (*scope-mixed screen*) had been adopted on 2026-08-06 at `analytics/daily-research/2026-08-06.md:940`
  and never written down. On 2026-08-07 the officer numbered *manufactured residual* as 27, and
  the chairman adopted it under that number (`analytics/daily-research/2026-08-07.md:975`,
  `7adfd68`). **Two council rulings assign one number to two patterns.** All fourteen rules are
  now in their seat notes; both entry-27 rows stand as adopted, and the renumbering is escalated
  in [[Workflow Threads]] C11 because it changes what a ruling says. Commits carrying the
  adoptions: `3ff5498` (08-05), `aa48406` (08-06), `7adfd68` (08-07).
- **A false commit citation in [[Agent Registry]], written by the archivist on 2026-08-06.** The
  note credited `373cce6` with correcting `prompts/research_analyst.txt:18`; `git show --stat
  373cce6 -- prompts/` is empty and the fix is **`9efafb0`**, whose commit message states it.
  Taxonomy 17a, *mis-located internal-authority citation*, committed by the seat that maintains
  the taxonomy's home. Corrected in place at the registry's 2026-08-06 paragraph.
- **`HANDOFF.md:164` attributed the analyst's Opus 5 assignment to the operator directive of
  2026-07-29.** That directive set `HEAVY_MODEL = "claude-fable-5"` (`4f8f981`, verified by
  `git show 4f8f981:src/models.py`); Opus 5 came from the 2026-08-03 directive (`939deaa`). It is
  the blanket-replacement defect this log recorded as a standing rule on 2026-08-03, alive in a
  live file for four days. Fixed. **`COUNCIL.md:66` carries the identical misattribution**, and
  `:68` still places the digest classifier "in `src/classify.py`" when `src/models.py:32` defines
  `DIGEST_CLASSIFIER_MODEL` and `src/classify.py:58` imports it — the same locution escalated on
  2026-08-04. Not this seat's file; escalated again, now four days open.
- **The snapshot-anchor convention became a program, and it does not cover the notes agents
  read.** `scripts/check_currency.py` (`fb1c04e`, 2026-08-06) parses `Audited against <sha>`,
  verifies the sha is an ancestor of HEAD, and lists every commit touching the note's declared
  paths since. Its `TRACKED` map holds **five** notes; **thirteen** vault notes carry an anchor.
  The nine seat notes are unguarded — exactly where this session found three days of missing
  rules. And `grep -rn check_currency .github/workflows/` returns **nothing**, where
  `check_models.py` and `check_marks.py` are both wired. Running it today: 8 claims checked,
  6 failed. [[Workflow Threads]] B5.
- **Graph measurements re-run rather than restated.** `build_graph --dry-run` at `7c08dcf`:
  117 notes, 231 edges, 0 orphans, **7 WARNs** and **7 files awaiting a managed block**, against
  the 4 and 11 [[Agent Registry]] had carried since 2026-08-04. The `Project Machinery` broken
  link is confirmed closed. Three new WARNs are seat notes crossing the four-link cap as their
  adopted-rules sections grew, which retires the 2026-07-31 rule that any WARN naming a per-agent
  note is drift.
- **Why the managed-block run keeps not happening, stated structurally.** `build_graph` is
  whole-vault with no path filter, and four of the seven pending files —
  `BOUNDED_CHANGE_PROTOCOL.md`, `prompts/carrying_span_rule.md`,
  `lit-review/BIBLIOGRAPHY_TEMPLATE.md` and any future `think-tank/` file — sit outside the
  archivist's self-merge authority (`analytics/`, `agents/`, `moc/`, `HANDOFF.md`). The run can
  never land under that authority. Carried across four sessions as a preference; recorded now as
  a structural fact. [[Workflow Threads]] C12.
- **Orphan check: four true orphans, and seventeen branches with no merge-base at all.** Across
  65 remote heads, `git merge-base --is-ancestor <tip> origin/main` fails for four:
  `chore/operator-marks-2026-07-27` (17 operator ledger marks, eleven days unmerged — F1
  unchanged) and the three `claude/sweet-mccarthy-*` records ruled non-canonical on 2026-08-01
  (F3 unchanged). **Seventeen further branches share no common ancestor with `main`** —
  `git merge-base origin/main origin/fix/notable-line-integrity` is empty, `main` has five root
  commits with the oldest at 2026-07-22, and those branches root at 2026-06-08. They predate a
  history rewrite; ancestry cannot say whether they hold anything unrecovered, and this log does
  not assert either way. New: [[Workflow Threads]] F4.
- **Everything the council committed in the audit window landed.** `council/2026-08-06`,
  `council/2026-08-06-postscript`, `council/register-2026-08-06`,
  `council/threads-2026-08-06-source-audit` and `council/2026-08-07` are all ancestors of
  `origin/main`, which discharges the chairman's 2026-08-06 warning that A8 existed only off
  `main`. No new orphan was created between 2026-08-04 and today.
- **Post-merge addendum, found by re-running the guard against `main` at `3d474e0`.**
  `check_currency.py` reports an audit session's own landing commit as staleness. A session anchors
  its notes to the commit it audited — necessarily the one before its own — and landing the change
  set then touches those notes' declared paths, so `agents/Project Change Log.md` and
  `agents/Workflow Threads.md` each read *"1 commit(s) … since `7c08dcf`"*, that commit being
  `8a40a4a`, the audit itself. The anchors were **not** chased: bumping them reproduces the result
  on the next commit, and the loop is the finding. Recorded so a future reader does not mistake a
  self-referential STALE line for drift, and folded into [[Workflow Threads]] B5 as its third gap.
- **The merged branch `vault/archivist-2026-08-07` could not be deleted from origin.**
  `git push origin :refs/heads/vault/archivist-2026-08-07` returns *"fatal: the remote end hung up
  unexpectedly"* on three attempts through this environment's proxy. It is **not** an orphan —
  `git merge-base --is-ancestor 8a40a4a origin/main` succeeds — but it will show in a branch listing
  until deleted by hand. Stated rather than left for the next orphan check to re-derive.
- **Clean, and said plainly.** `scripts/check_models.py` exits 0 over all twelve model-bearing
  cards; `node tools/isds-workflow-3d/validate.mjs` exits 0 at 30 cards / 9 chips / 44 edges with
  zero `Jack` tokens; no live statement anywhere in the repository still names Fable 5 — every
  remaining occurrence is dated history, which is what the standing rule requires; and the site
  isolation check holds, with zero occurrences of any vault note name under `docs/` and the two
  `obsidian-archivist` hits being the chart's `.claude/agents/` evidence tooltips, by design.

## 2026-08-06

- **The memos credited Kim with an analysis she expressly declines, in eleven places.** `c02773a`,
  `9efafb0`, `373cce6` on `fix/ring3-dimension`. Kim *names* the proportionality question at her
  Part III.B.2 and states the article "does not intend to analyse how the concept of
  proportionality should be implied in balancing the rights of investors and public interests."
  Her load-bearing argument is evidentiary — the counterfactual an investor cannot establish.
  Corrected at `lit-review/kim-memo.md:41` (correction note), `:42`, `:49`, `:52`, `:56`, `:62`,
  `:92`, `:186`; `lit-review/ferguson-memo.md:267`; `METHODOLOGY.md:21`;
  `STATE_OF_THE_ANSWER.md:8`. **The remedy is promote-and-demote, never assert-absence** — she
  does discuss proportionality, and writing that she does not would be the same error mirrored.
  The correction imports nothing: `kim-memo.md:36` already called the evidentiary argument "the
  single strongest piece of analysis in her article" twenty lines before `:56` crowned
  proportionality. Two superlatives, same article. A sweep of `agents/`, `moc/`, `prompts/`,
  `.claude/agents/`, `views/`, `think-tank/`, `working/` returns **one** proportionality hit and
  it is correct (`working/10-authorities.original.txt:21`, Kingsbury & Schill), so **no agent
  prompt, definition, registry entry or flowchart card inherited the ranking** and no vault
  cascade was needed.
- **Kim's footnote 23 written in — a fifth reason the project never carried.** A remedy mismatch:
  the investor wants the disclosure stopped; an investment tribunal's ordinary remedy is
  compensation. A selection effect, not a merits prediction — it explains why the case is never
  filed. It predicts the distribution already in the repo: every disclosure case in the Kim memo's
  bibliography (InterMune T-73/13 R, AbbVie T-44/13, PTC Therapeutics C-175/18 P, Vanda D.D.C.)
  was brought in a **court** to stop disclosure, not in arbitration to be paid for it. Four for
  four. Recorded **operator-supplied**: Kim's article is unreachable from this project's tooling
  (UIC serves the landing page, returns 403/202 on every full-text endpoint), so the council
  verified nothing about her text and must not be cited as having done so.
- **The retired Ring 3 formulation survived `ae1f04b` in four places; all four closed at `373cce6`.**
  `prompts/research_analyst.txt:18` is the one that mattered — the fix had replaced the tail and
  left the head, so the sentence asserted **both** definitions and did not parse, in the prompt of
  the seat the project calls its deepest thinker. Also `METHODOLOGY.md:26` (the defining sentence,
  while its own heading said Dimension), `working/02c-framework-rings.original.txt:7` (retired
  definition as a heading, plus a claim false of two of three seeds), and
  `working/one-pagers/philip-morris-v-australia.md:18`, `:22`.
- **The ruling survived a falsification attempt on the project's own seed case.** In *Philip Morris
  Asia v. Australia* four threshold questions were separately adjudicated and exactly one disposed:
  control under Art. 1(e) (¶509), admission (¶523), temporal scope (¶534), abuse of rights (¶588).
  **Corrections to how this was first stated, both material:** ¶509 went against the **Claimant**,
  on the Claimant's own argument that continuous control since 2001 "eliminates every objection
  raised by the Respondent" (¶186) — not against the State; and Australia lost exactly **one**
  objection outright (¶523), because ratione temporis and abuse of rights are two limbs of a single
  objection (¶¶9, 184) and ¶534 finds jurisdiction "without prejudice to its later finding on abuse
  of rights". **The finding that matters most is the fifth question.** Australia's Third Objection —
  "that neither the shares in PML nor PML's assets constitute investments for the purposes of the
  Treaty" (¶184) — was raised and **never decided**. That is this project's own central question,
  put to a tribunal in terms and left unanswered; the phrase occurs exactly once in the award. A
  disposition-keyed Ring 3 is **blind by construction** to raised-and-never-reached questions,
  because a question never answered can never dispose of anything. That is stronger vindication of
  the dimension ruling than any count.
- **Published counts were wrong on the live site for one day.** `9bd112e` published "seven of the
  fourteen items" (`base.html.j2`, 16 pages) and "347 candidates" (`index.html.j2`, 19 pages).
  Measured from the committed archive: 14 article files, **13 distinct URLs**;
  `https://www.italaw.com/cases/12153` appears in both the 06-09 and 06-10 runs. **Not a dedup
  bug** — `8e1cc48` ("chore: reset seen-state for final full-digest send") emptied
  `state/seen.json`, so `is_seen()` had nothing to match; `src/state.py` is correct and untouched.
  The defect is that the classifier returned **contradictory verdicts on identical input**: 32 with
  ring `judicial_or_regulatory_measure` on 06-09, 28 with no rings on 06-10, same URL and same
  source text. The duplicate therefore lands on **both sides** of the ring split and cannot be
  assigned to either without arbitrarily preferring one verdict. Accurate statement: **thirteen
  distinct items; twelve carry a single verdict, six with a ring and six with none; the thirteenth
  was screened twice and classified contradictorily.** "347" is the sum of per-run `screened`
  across a window containing two manual state resets — 347 **screenings**. Corrected at `9efafb0`.
  `tests/test_site_claims.py` needed no change: runs/screened/matches/surfaced are counts of runs,
  screenings and entries, and all four remain correct; the defect was the prose labelling them.
- **The wrong Kim pincite was published for thirteen days, and this log never recorded it.**
  "15 J. Marshall Rev. Intell. Prop. L. **999** (2016)" stood in `METHODOLOGY.md` — the memo
  addressed to Dr. Benavides — and in the generated `docs/methodology.html` on the public site from
  `a819266` (2026-06-16) to `a208f53` (2026-06-29); also in `STATE_OF_THE_ANSWER.md` and
  `analytics/insights.jsonl` at `2bb5bad`. **228 is and always was correct** and reads correctly
  today; nothing is to be "fixed" to 999. One clean negative: the email channel never carried it,
  `RECIPIENTS` in `src/config.py` having been narrowed before the error was introduced. Recorded
  because this log's rule is that every material change is dated and commit-cited, and a
  thirteen-day publication of a wrong citation in the professor's own memo is material.
- **Three further defects closed at `373cce6`.** `kim-memo.md:102` was a "Backsourcing
  verification" block attesting that Kim's citations are accurate against the Eli Lilly Final Award
  of 16 March 2017 — which Kim, writing in 2016, could not have read; it verified pin cites to a
  document the cited author never saw, under the word "verification".
  `working/one-pagers/eli-lilly-v-canada.md:18` pinned the phrase *investments at issue in this
  arbitration* to ¶167; that phrase occurs nowhere in the award and ¶167 is the ratione temporis
  paragraph. `scripts/check_claims.py:31,143` said "fourteen facts" against a registry of thirteen
  (`len(REGISTRY) == 13`, verified).
- **Apotex caption corrected; metrics unmoved.** The holdout text describes ANDAs and the
  not-an-investor holding, which is *Apotex Inc. v. United States of America*, UNCT/10/2, 14 June
  2013 — not *Apotex Holdings* (ARB(AF)/12/1, 2014), the FDA import-alert case.
  `scripts/holdout_set.json`, `scripts/backtest_corpus.json`. Confusion matrix before and after:
  **TP=3 FP=0 FN=1 TN=16**.
- **Vault self-audit.** [[Agent Registry]] recorded the systems-designer / site-experience model
  defect as open for a full day after `c25ea64` closed it, while [[Claim Map]] C12 and
  [[Workflow Threads]] C7 both recorded it CLOSED — three notes, one fact, and the roster was the
  wrong one. It also asserted no definition had changed since `939deaa`, when `ae1f04b` rewrote the
  research question at `.claude/agents/council-chairman.md:31-32` — a contract change this vault's
  own maintenance rule required to move the registry in the same change set. `moc/Council.md` named
  six seats while linking "the nine agents". All corrected in place so the corrections stay legible.
- **Open and escalated, not closed.** `analytics/verification_ledger.jsonl` holds 58 entries and
  **none** touch Kim, Ferguson, Marshall or proportionality, while `moc/Evidence Ledger.md:3-4`
  tells a reader that what the project knows lives in that ledger. For the literature layer that
  describes an empty set.

## 2026-08-05

*Audited against `eac8ed9` (`main`, clean tree); paths: `prompts/`, `.claude/agents/`,
`agents/`, `moc/`, `fingerprint.yaml`, `src/`, `scripts/`, `tests/`, `templates/`,
`scripts/site_templates/`, `docs/`, `think-tank/`, `working/`, `lit-review/`, `analytics/`,
`state/`, `views/isds-workflow-3d/workflow.json`, `.github/workflows/`.*

- **The claim map gains the two rows the council was about to decide without.** [[Claim Map]]
  **C13** ("What Ring 3 *is*: a doctrinal dimension, or a disposition") and **C14** ("The
  holdout's composition, and the Apotex item's identity"), written as a continuity gate
  *before* the 2026-08-05 council ruled on either. C13 lists 15 files stating Ring 3 as a
  disposition and 12 stating it as a dimension, with the mixed paragraph at
  `METHODOLOGY.md:26` that currently states both. C14 lists 21 locations restating the
  holdout's composition, the Apotex item's two captions, and the guards that hold them.
  **In the working tree at `eac8ed9`, not committed**, per this log's rule about recording a
  change before it lands. Reasoning and both blast radii:
  `analytics/vault-sessions/2026-08-05.md`.
- **The largest Ring 3 surface in the project was found in a JavaScript string, and it is
  false under both candidate definitions.** `scripts/site_templates/base.html.j2:162` reads
  "the threshold on which **the seed cases were decided**" — plural, when only *Philip Morris*
  was so decided (`think-tank/methodology/ring3-reconciliation.md:16-22`). `base.html.j2` is
  inherited by all six page templates, so it renders on **sixteen** published pages
  (`docs/index.html:385`, `docs/methodology.html:260`, `docs/how-it-works.html:350`,
  `docs/backtest.html:603`, `docs/digests/index.html:450`, and eleven
  `docs/digests/<date>.html`). It is the exact sentence the 2026-06-29 correction (`8909390`)
  removed from `METHODOLOGY.md`; it survived because no prose sweep reaches a string inside a
  JS object literal in a base template. **`docs/` is generated — the fix is the template and a
  rebuild, and it belongs to [[site-experience]], not this seat.**
- **Three claim-map rows were stale, and one of them had been stale for a single day.**
  Corrected in place at `eac8ed9`, so the corrections stay legible:
  **C1 DIVERGENT → CLOSED** — the 20-vs-12 / 0.95-vs-0.92 split was closed at `7959777` on
  2026-08-04, the same day the row was written calling it open; `backtest_corpus.json` now
  carries 4 positives and **16** negatives and `docs/backtest.html` renders 20 cases, TN 16,
  accuracy 0.95. **C7 counts corrected** — the row said ten flowchart cards, ten definitions
  and twelve vault notes; measured, it is **twelve** model-bearing cards, **nine**
  `.claude/agents/*.md` and **nine** seat notes among thirteen `agents/*.md` files, and no
  file ever carried the number ten. **C12 open → CLOSED** — the row asked whether
  `scripts/check_models.py` (`c25ea64`) covers the two seats that declared no `model:` key;
  it does, and the guard was run to prove it.
- **Workflow thread C7 closes with it.** [[Workflow Threads]] C7 still described the two cards
  as reading "Model: Claude Fable 5" with no declaring definition. Closed and replaced with
  the constraint that survives it: `model:` selects a tier, so the version check rests on the
  vault note's ``**Model.** `…` `` line, which `scripts/check_models.py:63` matches by regex —
  reformatting those notes would silently remove a leg of a CI guard.
- **A third sense of "Ring 3" is in daily use and matches neither candidate definition.** The
  research layer carries a five-mechanism "Ring 3 taxonomy" — abuse-of-right/critical-date,
  administrative-review prerequisite, fork-in-the-road, MFN-forum-access, first-generation-BIT
  scope limitation — across 17 lines of `analytics/insights.jsonl`,
  `STATE_OF_THE_ANSWER.md:114-124`, `state/research_log.json:111`/`:171`/`:201`/`:211`, and
  `analytics/optimization-log.md:34`. **None of the four newer mechanisms appears in
  `fingerprint.yaml:81-102`.** Escalated to Emory rather than reconciled by this seat:
  `analytics/vault-sessions/2026-08-05.md`, Part F.
- **Recorded for the systems designer, outside this seat's paths.**
  `scripts/check_claims.py:31` and `:143` say the tool "checks fourteen facts"; the registry
  holds **13** and the tool prints 13 — a fourteenth was retired in place at `:246-263` and
  the prose was not updated. And `.github/workflows/claims-consistency.yml` lists
  `scripts/check_claims.py` and `tests/test_check_claims.py` in its **pull_request** paths
  (`:30-31`) but not its **push** paths (`:36-47`), so a direct push to `main` editing only
  the guard does not re-run the guard.

## 2026-08-04

*Audited against `b76f6c3`; paths: `agents/`, `.claude/agents/`, `prompts/`,
`src/models.py`, `src/source_health.py`, `views/isds-workflow-3d/workflow.json`,
`HANDOFF.md`, `analytics/`, and every remote branch tip.*

- **A claim map enters the vault, and it exists because eight contradictions were one fact
  stated twice.** [[Claim Map]] — twelve rows, one per factual claim the project makes about
  itself, each listing every file that states it, what each currently says at `file:line`,
  and the twin list a fix must change in the same change set. Written during the council
  session on external reviewer feedback of 2026-08-04; the session's reasoning and the
  item-by-item remit analysis are at `analytics/vault-sessions/2026-08-04-council.md`.
  **Both files are in the working tree at `c9050e6` and not yet committed**, per this log's
  rule about recording a change before it lands. The map's own anchor is `c9050e6`. Rows
  C1, C2, C5, C6, C7 and C8 are recorded DIVERGENT against files on `main` today; C3 and
  C12 restate drift this log already carries under **Open drift**.
- **A fourth false claim found in the 2026-08-03 entry below, and it is not corrected here.**
  `agents/obsidian-archivist.md:237-238` cites this note for "Escalated 2026-08-03 by the
  deliverable-drift sweep". **No such section exists in this file**, and no commit anywhere
  carries the sweep's findings — `grep -rn "deliverable-drift" agents/ analytics/` returns
  only the two lines inside `agents/obsidian-archivist.md` itself. The 2026-08-04 currency
  audit tested three of that entry's claims and stopped short of this one. Escalated rather
  than tidied: `analytics/vault-sessions/2026-08-04-council.md`, §1.3.

- **The Carrying-Span Rule is implemented — a rule that failed in prose now has an artifact
  that fails.** The chain, in the order the record establishes it: three bibliography entries
  cited sources for propositions those sources do not contain (*Vanda*, H&H's trade-secret
  use, Bonnitcha's subject-matter use; corrected entries at `5b51cd9`, merged `42374f8`) →
  **R1 found the rule that already existed COVERED them and was not applied**, overturning
  the chairman's own scope-defect framing, so this is a discipline failure and writing the
  rule again would not fix it → **R5 found rules bind here only when attached to an artifact
  that fails**, with the officer's correction that the remedy is enforcement *and* a carrier
  → the rule now has both. `prompts/carrying_span_rule.md` (R3 as amended, not the Part 3 §1
  draft); `lit-review/BIBLIOGRAPHY_TEMPLATE.md`; `scripts/check_marks.py` with
  `tests/test_check_marks.py`; `.github/workflows/lit-review.yml`. Three definitions in
  `.claude/agents/` gained one canonical-training clause each, and the officer's
  self-training mandate stopped enumerating a stale five patterns and now points at this
  vault's taxonomy table. **On branch `feat/carrying-span-rule`, PR #52 — not on `main` at
  the time of writing**, per this log's own rule about recording a change before it lands.
- **What that enforcement establishes, and what it does not.** `scripts/check_marks.py`
  implements R5 tiers 2, 3 and 5, but **coverage is conditional and its module docstring is
  the single authority on what it checks**; the CLI reports what it actually *exercised* on
  a run, which is not what it implements. All 33 entries are in the legacy form, so the
  strict tiers currently run on nothing and the tool says so. It establishes entry **shape**
  only — never that a span exists in its source, and never that a span carries its
  proposition. Per R8 the rule is **adopted and unvalidated**; it becomes validated when
  `N changed / M screened` is reported, read the officer's way, where M > 0 with N = 0 is a
  positive detection of performance rather than evidence of clean work.
- **Taxonomy entry 24 — *amendment-stripping*.** A rule lifted from a session record in its
  pre-vetting draft form, carrying the adoption date and the word *binding* with every
  objection that conditioned adoption silently absent. Caught in vetting on the change set
  above, which was itself the instance. Standing guard at `prompts/carrying_span_rule.md:3-7`.
  Full entry in [[integrity-officer]].
- **The fetch relay — the architecture change the vault had not recorded.** A council session
  running in the scheduled cloud environment has no network egress of its own. The relay
  closes that: the session commits a small JSON request under `analytics/fetch-requests/`, the
  push fires a GitHub Actions runner that *does* have egress
  (`.github/workflows/fetch-relay.yml`), the runner fetches each URL through the project's own
  `polite_get` — same user agent, same robots evaluation, same per-domain interval — and
  commits back a reduction to `analytics/fetch-results/`: status, final URL, content-type,
  byte length, sha256, timestamp, and a capped excerpt. The document body never travels,
  because the repository is public and a commit is publication. `fe02f39`
  ("feat(relay): fetch relay for the network-less council session"), excerpt targeting in
  `7fbbabf`, on the flowchart as `relay-request` / `relay-answer` in `0e7d0f7`. It answered a
  standing research gap the day it landed.
- **Four method rules and six taxonomy entries adopted.** Relay method rules binding on every
  seat, and the chairman's quote-the-whole-line amendment (`51bb7a2`); fabrication taxonomy
  entries 18–23 plus entry 17 extended from mis-dated to mis-located (`51bb7a2`). All now in
  the seat notes; see [[Agent Registry]]'s adopted-rules table.
- **Vault: the 2026-08-03 archivist change set was found to have landed only in part.** Its
  own note's audit slice reached `main` through the conflict resolution of `8705f7a`; the
  `Project Machinery` note it recorded creating exists in no commit; and no 2026-08 content
  ever reached the chairman, analyst or integrity-officer notes. Consequence, measured rather
  than asserted: the taxonomy-recitation defect that change set reported closing recurred at
  `analytics/daily-research/2026-08-03.md:185` and `2026-08-04.md:535`. Corrected and landed
  2026-08-04; full statement in [[obsidian-archivist]], audit slice 2026-08-04.
- **`HANDOFF.md` — three false statements corrected.** The heavy tier read `claude-opus-4-8`
  at line 29 against `HEAVY_MODEL = "claude-opus-5"` in `src/models.py` and against its own
  line 163, the half of `939deaa` that was never applied; the digest classifier was placed
  "in `src/classify.py`" when `src/models.py` defines `DIGEST_CLASSIFIER_MODEL` and
  `src/classify.py:58` imports it; and the `italaw` row asserted in the present tense that the
  zero-streak guard flags it `DEGRADED`, when `state/source_health.json` records
  `zero_streak: 1` and `src/source_health.py:121-130` puts the earliest possible flag at
  2026-08-17.

## 2026-08-03

- **The fetch relay's two standing rules implemented, and their council record lost.** The
  session that adopted them wrote `analytics/council-sessions/2026-08-03-standing-rules.md`
  (887 lines) on a worktree branch as `3d31de8`. That commit was never pushed: it is not an
  ancestor of `origin/main`, no remote branch carries it, and `git cat-file -t 3d31de8` now
  returns "Not a valid object name". The rules themselves are in the code — `0091ade` ("a
  refused source can no longer report as healthy") and `fe02f39` — so the machinery is on
  `main` and its reasoning is not recoverable from git. Escalated 2026-08-03 as orphaned;
  recorded 2026-08-04 as lost.
- **Two special council sessions recorded and merged.** The deterministic pre-ledger
  verification system (`1109993`, `analytics/council-sessions/2026-08-03-verification-system.md`)
  and the carrying-span rule for the proposition problem (`56cbb75`,
  `analytics/council-sessions/2026-08-03-proposition-rule.md`). The second records its own
  rule as **adopted and unvalidated** against the session's base rate, and that qualification
  is carried into [[research-analyst]] rather than dropped.
- **Chairman and research analyst moved from Claude Fable 5 to Claude Opus 5.** Operator
  directive: the Fable 5 credit balance is exhausted, so both top seats move to Opus 5.
  Applied in `src/models.py` (`CHAIRMAN_MODEL` and `HEAVY_MODEL` now `claude-opus-5`), the
  two agent definitions' `model:` keys (`.claude/agents/council-chairman.md`,
  `.claude/agents/research-analyst.md`), the six flowchart cards in
  `views/isds-workflow-3d/workflow.json`, `COUNCIL.md`, `HANDOFF.md`, `METHODOLOGY.md`
  Part VIII, and this vault's registry and per-agent notes. The other seats are unchanged
  on Opus 4.8. The dated history below is left as written — the July 29 promotion to
  Fable 5 happened and stays recorded. **Two qualifications added 2026-08-04:** `939deaa`
  did *not* reach `HANDOFF.md:29`, which kept the old heavy-tier id for a day (fixed above);
  and it rewrote the two disputed flowchart cards from "Fable 5" to "Opus 5", which leaves
  the card-model defect intact while making it read as a legitimate assignment.
- **First live run of the silent-decay source-health guard.** `state/source_health.json` now
  exists with per-source streaks; `digests/2026-08-03_ISDS-Thematic-Watch/meta.json` is the
  first archived run to carry them. `health_warnings` is `[]`, which is a cold-start artefact
  and not a statement of source health — no source can reach the three-run threshold before
  2026-08-17. Closes the "not yet exercised" state carried in [[Workflow Threads]] B1 since
  2026-07-30.

## 2026-08-02

- **Fabrication taxonomy entries 12–14 adopted** — capability-as-corroboration, absolutized
  heuristic, silent class truncation — each anchored to a filed objection. `82692a2`,
  `analytics/daily-research/2026-08-02.md:198-200`.

## 2026-08-01

- **The vault's orphaned 07-31 work was caught by the council, not by the archivist.** The
  close-out's escalation 1 states it plainly: the archivist session's vault work existed only
  on `feat/methodology-source-council-sync` and "until then the vault's workflow memory is
  invisible to main" (`4d5c562`, `analytics/daily-research/2026-08-01.md:487`). Recovered
  2026-08-03 by PR #44 (`cb12a2d`).
- **Three cloud-run council records ruled non-canonical.** The scheduled runs of 2026-07-30,
  07-31 and 08-01 sit on `origin/claude/sweet-mccarthy-8mouy6`, `-i95s3k` and `-d5kgmw`. They
  ran `claude-sonnet-4-6` in seats assigned other models, so the close-out ruled them
  "preserved verbatim … as a non-canonical parallel artifact" and recommended archiving or
  deleting the branches so they cannot later be mistaken for canon
  (`analytics/daily-research/2026-08-01.md:452` and `:487`, `4d5c562`). Still unactioned.
- **Fabrication taxonomy entry 11 adopted** — status-as-record-artifact. `4d5c562`,
  `analytics/daily-research/2026-08-01.md:410`.

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
  > **ORPHANED-COMMIT CITATION, annotated 2026-08-25 — the entry stands, the citation does
  > not.** `git cat-file -e 80ad250^{commit}` fails; `git log --all` finds no commit carrying
  > that message; the only commits dated 2026-07-21 in the complete 804-commit history are
  > `7723f98` (daily council meeting) and `433f0a5` (sent marker). `80ad250` was never pushed.
  > **The work itself did land** — `moc/` and `scripts/build_graph.py` are present and the
  > 2026-07-18 entry's `b87c838` resolves — so what is unrecoverable is which commit performed
  > the freeze, not whether it happened. The original wording is left exactly as written,
  > per the vault's supersede-never-overwrite convention. Taxonomy entry routed from
  > `analytics/daily-research/2026-08-25.md:1375`.

## 2026-07-18

- **The vault's mapping machinery created.** `scripts/build_graph.py` plus the curated
  `moc/` hubs — hub-and-spoke, managed blocks, idempotent. `b87c838`.

## Open drift

Nothing here is a to-do list for an agent: these are discrepancies between two repository
artifacts that only Emory can settle. Threads with a named agent owner live in
[[Workflow Threads]].

- ✔ **CLOSED at `c25ea64` (2026-08-05); struck here 2026-08-08, three days late.** *Two
  flowchart cards assert a model no configuration file carries.* All nine `.claude/agents/*.md`
  declare `model: opus`, both cards read "Model: Claude Opus 5", and `scripts/check_models.py`
  — re-run 2026-08-08, exit 0 over twelve cards — fails the build on card/definition/vault-note
  drift. **This is the fourth place that carried this closed defect as open**, after
  [[Agent Registry]] (corrected 08-06), [[systems-designer]] (corrected 08-06) and
  [[site-experience]] (corrected 08-04). The entry is struck rather than deleted because *how
  long one fact took to die in four places* is the record's most useful datum about itself.
- **NEW 2026-08-08 — a seat definition binds a constraint the repository has disproved.**
  `.claude/agents/systems-designer.md:17` binds that seat to "the **zero-cost** constraint".
  A code reading on 2026-08-08 established that the below-cutoff tail is model-classified in
  production, and `README.md:3-9` was corrected the same day to "low-cost, roughly cents per
  run, not free". Resolution is Emory's because it is a contract edit: either strike the word
  from the definition, or replace it with the cost bound the project actually intends. The
  vault note [[systems-designer]] is corrected and carries the escalation; the definition is
  untouched.
- **`build_graph`'s block replacement spans a prose-quoted start marker.**
  `scripts/build_graph.py:195` anchors to the first start marker in the file rather than the
  managed one, so any note quoting that marker is gutted on the second run. Demonstrated and
  contained on 2026-07-31 (see the entry above); the vault is safe only because no note now
  quotes it. Narrow fixes, any one of which closes it: anchor to the **last** start marker,
  skip markers inside code spans and fences (`_CODE_FENCE` is already compiled in the
  module), or fail loudly on a duplicate start marker instead of silently spanning it. Wants
  a regression test with a note that quotes the marker. Machinery work — [[systems-designer]]
  on Emory's go-ahead. **Re-verified 2026-08-04: still open.**
- **Seventeen of Emory's own verification marks have never reached `main`.** Raised
  2026-08-04. `origin/chore/operator-marks-2026-07-27` ("chore(ledger): operator
  chat-verification sweep — 37/40 verified, Hela Schwarz characterization rejected and
  corrected", `6f9e1da`, dated 2026-07-27) is not an ancestor of `origin/main`. Its
  `analytics/verification_ledger.jsonl` holds **38** operator marks and 40 claims; `main`'s
  holds **21** marks (`8891c21`) and 37 claims. The 17 missing marks include the `--rejected`
  mark on `7dd2f272f130f859` (the *Hela Schwarz* framing) and the `--verified` mark on
  `5c25faf36673d6f3` (China–Germany BIT Art. 1(d) against the official treaty text) — both of
  which `HANDOFF.md:147-152` still lists as "awaiting your CLI mark", true against `main`'s
  ledger and false against the work Emory actually did. Not merged by this seat: the ledger is
  operator-owned, and its integrity is the project's foundation. Emory's call.
- **The chart's `quality-bar` card is now wrong twice — about a file, and about the
  behaviour.** (1) Its evidence reads `src/config.py: threshold 40 / floor 25`; the threshold
  lives at `fingerprint.yaml:10` (`threshold: 40`). Raised 2026-08-03, re-verified 2026-08-04
  and **2026-08-08**. (2) **New 2026-08-08:** its `desc` reads "Near-misses (25+) **may fill a
  quiet week**, always labeled as leads" and its `meta` "Emory's fixed rule — 40 pass, 25
  floor". The fill is suspended by default as of this date. **Both defects must be fixed in the
  same manifest edit**, or the second fix will look like the whole fix. The card is one of the
  eight statements listed at [[Claim Map]] **C15**. [[systems-designer]] regenerates from the
  manifest; not hand-edited.
- **`views/isds-workflow-3d/view.js` has no freshness guard** where the generated SVG has a
  fail-closed one. Raised 2026-08-03, re-verified 2026-08-04. [[systems-designer]].

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
