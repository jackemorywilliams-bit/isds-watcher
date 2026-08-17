---
aliases: [Workflow Threads]
tags: [agent, council]
hub: Council
---
# Workflow Threads

Every open thread in the project as **one linear chain**: what it is → where it stands →
where that is recorded → who owns the next action. One thread, one chain, no branching. If
a thread is not here, either it is closed or it could not be sourced — and an entry that
cannot be sourced is not written.

Nothing in this note is new information. It is the same record the daily meetings, the
research log, and the optimization log already hold, laid out end to end so the state of the
work can be read in one pass instead of reconstructed from five files.

Roster and models: [[Agent Registry]] · dated history: [[Project Change Log]].

**Snapshot refreshed:** **2026-08-13**, at `8ea2ee1` on `main`, clean tree, against a
**complete** history (`git fetch --unshallow`; 584 commits). Sources read for this pass:
`git cherry origin/main <branch>` over every remote branch, the two
`analytics/verification_ledger.jsonl` blobs on `main` and
`origin/chore/operator-marks-2026-07-27` replayed through `scripts/verify.py`,
`src/integrity_gate.py`, `scripts/holdout_set.json`, all nine `.claude/agents/` definitions
against all nine `agents/` seat notes, `src/models.py`, `.gitignore`,
`.github/workflows/pipeline-guards.yml`, `HANDOFF.md`, `views/isds-workflow-3d/workflow.json`,
and live runs of `pytest` (**562 passed / 1 failed / 3 skipped / 5 xfailed** — see the note on
the failure below), `scripts/check_currency.py` (**9 claims, 3 failed**),
`scripts/check_models.py` (exit 0, 12 cards), `scripts/check_lock.py` (exit 0),
`scripts/check_headline_lane.py` (exit 0), `scripts/check_claims.py` (exit 0),
`scripts/check_seen_integrity.py` (exit 0), `scripts/check_telemetry_privacy.py` (exit 0),
`node tools/isds-workflow-3d/validate.mjs` (exit 0, 30 cards / 9 chips / 44 edges) and
`scripts/build_graph.py --dry-run`.

**Two measurements from this pass correct standing conventions rather than threads.**
(1) `pytest` and `scripts/check_sources.py` **cannot pass in a clean clone**: both assert the
presence of files under `seeds/`, which `.gitignore:2` excludes as private source material.
`tests/test_one_pagers.py:73` fails and `check_sources.py` reports 5 failures here for that
reason alone, and CI never catches it because
`.github/workflows/pipeline-guards.yml` runs only named test files, never the whole suite. Every
"N passed" figure in this vault is therefore a reading from Emory's machine, and should be read
as one. (2) The orphan convention in this note — `git merge-base --is-ancestor <tip> origin/main`
— reports **45** unlanded branches at `8ea2ee1`, while `git cherry` (patch equivalence) reports
**6**. The difference is squash-merged branches, whose tips are correctly not ancestors. The
ancestor test is kept for *content* questions like F1, where the blob itself is compared; for
"did this branch land", `git cherry` is the honest query.

**Superseded, retained — snapshot of 2026-08-09**, at `2686422` **plus the uncommitted working
tree of the 2026-08-08 repair session and the 2026-08-09 audit-response session, on branch
`fix/restore-council-label`**. Said in those words
because most of that work is not committed, and a thread whose state rests on an
uncommitted file is citing a path on a branch, not a hash. Sources read for this pass:
`git status --short`, `src/config.py`, `src/main.py`, `src/rings.py`, `src/headline_lane.py`,
`src/triage.py`, `scripts/check_site_sync.py`, `.github/workflows/pipeline-guards.yml`,
`analytics/state-space-resolution-2026-08-09.md`, `analytics/locked_set/RETRIEVAL_LEDGER.md`,
`working/benavides-comment-replies-2026-08-08.md`, `seeds/`, `METHODOLOGY.md`, `README.md`,
`fingerprint.yaml`, `scripts/site_templates/index.html.j2`, `HANDOFF.md`,
`views/isds-workflow-3d/workflow.json`, and live runs of `pytest` (**564 passed / 5 xfailed**),
`scripts/check_currency.py` (9 claims, 0 failed), `scripts/check_lock.py` (exit 0),
`scripts/check_headline_lane.py` (exit 0), `node tools/isds-workflow-3d/validate.mjs` (exit 0)
and `scripts/build_graph.py --dry-run`.

**What this pass changed.** **B6 is rewritten** — D/E, F and G are **built**, not designed, so
the thread that existed to stop anyone reading them as shipped now exists to record what
shipped and which flags hold it off. **B8 closes** on `.github/workflows/pipeline-guards.yml`.
**B7** gains its written `check_lock.py`. **B5 shrinks from eight statements to three** and
gains a successor divergence pointing the other way. **D3 closes** on a green
`check_currency`. **B9** (a check that mutates the repository) and **D4** (a scoped clause that
breaks if a list grows) are new. Nothing in A was touched.

**One thread did not close that this pass was briefed to close.** **B5** / [[Claim Map]] **C15**
was reported resolved. Five of its eight statements are repaired; **three are not**, and one of
the three had *moved* to a different line number, so only re-reading the file found it. The
rule that governs this note held and was load-bearing today: **no thread is closed on the
strength of a session report** — every closure below was re-read in the file, and the one that
could not be verified stayed open.

**Superseded snapshot:** 2026-08-08, at `2686422` plus that day's working tree. Before it,
2026-08-04, at `b76f6c3` (merge of PR #49). Sources read for that pass:
`analytics/daily-research/2026-08-01.md` through `2026-08-04.md`,
`analytics/council-sessions/`, `analytics/verification_ledger.jsonl`,
`state/source_health.json`, `digests/2026-08-03_ISDS-Thematic-Watch/meta.json`,
`src/source_health.py`, `views/isds-workflow-3d/workflow.json`, and the branch-ancestry check
described in F1. The previous snapshot was 2026-07-31 at `e153ce3`.

**Refreshed 2026-08-04.** The A- and C-series states below are carried from the 2026-07-31
pass except where a section says otherwise; the council's own close-outs, not this note, are
their source of truth. What this pass changed: B1 closes, C9 closes, C7 and C8 are
re-verified open, and section F is new.

---

## A · Research threads — the analyst leads

### A1 · A/81/17 publication window

- **State** — **Refreshed 2026-08-06 (was stale at the 2026-07-31 snapshot).** The window
  **opened 2026-08-01** and is open; A/81/17 is **not published** as at day 6. The check is no
  longer a web-search query but a **fetch-relay row against the Commission Sessions posting
  location** (`https://uncitral.un.org/en/commission`), in the same-page positive-control form —
  target symbol `A/81/17` plus control `A/80/17`, which matches. Days 1–6 all null. The page has
  been byte-identical (832,338 bytes, `sha256 ca87a113…`) at **five sampled time points** spanning
  2026-08-03T18:25:23Z → 2026-08-06T11:38:46Z; that is five samples, **not** a continuous interval
  and **not** N independent confirmations (objection 0806-B3). Two standing qualifications: the
  null is about **rendered text** only, since the relay strips attributes and a symbol appearing
  only inside an `href` is invisible to it; and the `undocs.org` / `docs.un.org` symbol route was
  **RETIRED 2026-08-04** as carrying no existence information at the reduction level. **Four**
  questions now ride on publication, not three: the adopted Supplementary Provision numbering,
  the TPF SP10/SP11 inconsistency, whether DP 19's ex officio dismissal power survived, and — 
  folded in 2026-08-05 — the ASIL SP-subject-matter delta (see A8).
- **Recorded** — `analytics/daily-research/2026-07-31.md` Task 3 and Next Step 1 (`f03a90e`);
  daily records 2026-08-01 through 2026-08-06 Task 1; `state/research_log.json` open thread 3.
- **Next** — Continue the daily relay row with its same-page control; escalate to lead status on
  publication. Do not use `undocs.org`.
- **Owner** — [[research-analyst]].

### A2 · UA-controlled 403 re-audit

- **State** — Newly opened by the integrity officer's user-agent-gating finding: a 403 from
  `uncitral.un.org` carries **no** information about whether a resource exists, so every
  item the record carries as "403-blocked" on that host may be an access artifact rather
  than a fact. At least one such item is in fact retrievable.
- **Recorded** — Observation 4 in the 2026-07-31 vetting note (`15c8131`); Next Step 2 in the
  close-out (`f03a90e`).
- **Next** — Bounded pass, next session: enumerate the standing "403-blocked" items on
  `uncitral.un.org` **only**, re-test each once under a browser UA with a positive control,
  and reclassify each as retrievable / origin-absent / genuinely gated. Other hosts only
  after this pass proves the method's yield.
- **Owner** — [[research-analyst]], protocol from [[integrity-officer]].

### A3 · China–France BIT (2007) Protocol text — ordinary residual

- **State** — The escalation is **closed**; this is what is left of it. The forum question is
  answered at provision level by Emory's own verified ledger action (`da33a30be92ab234`,
  `operator_verified` 2026-07-27: domestic courts / ICSID / UNCITRAL, fork-in-the-road, no
  mapped administrative-review or domestic-litigation prerequisite). The French Protocol's
  full text remains unread, so the mapping-level answer is unconfirmed against the
  instrument. Marker: `GAP-UNRESOLVED: china-france-bit-2007-protocol-text`. **Zero
  escalation** — this is an ordinary open item, not a standing escalation, and it does not
  inherit the 23-session priority the closed one had.
- **Recorded** — Gap-marker dispositions in the 2026-07-31 close-out (`f03a90e`);
  `state/research_log.json` open thread 5.
- **Next** — Confirm against the Protocol text when budget allows. Every statement of the
  finding carries both flags in the meantime: `quote_ok: true`, `scope_ok: false`.
- **Owner** — [[research-analyst]].

### A4 · China–Switzerland forum relationship

- **State** — **Refreshed 2026-08-06 (was stale at the 2026-07-31 snapshot, which predates two
  closures).** The original gap `GAP-UNRESOLVED: china-switzerland-forum-relationship` is
  **CLOSED at mapping level 2026-08-04**: UNCTAD's IIA Mapping records treaty 978's "Relationship
  between forums" as *"Preserving right to arbitration after domestic court proceedings"*,
  retrieved twice through the relay with controls, excerpt window byte-identical across runs. The
  "fork-in-the-road vs. no-U-turn" framing the entry was opened on was a **false dichotomy** and is
  dissolved rather than answered — the record carries three labels, not two, and they classify
  drafting structure without predicting tribunal application. **Identification of the retrieved
  record was DISCHARGED to database-record level 2026-08-06** by a pre-registered false-slug
  control (`…/978/zzz---zzz-bit-1900-`; reduction held at `a8c5ad9c`), which bears on *which*
  record was retrieved and **not** on what it says. What remains open is content, not
  identification: the cell is mapping-level from an expressly student-mapped, "purely informative"
  database; **not ledger-grade** (no claim id, no operator verification, no preserved
  `source_snapshot`); **not ranked** against China–Germany or China–France, there being no codebook
  in the record; and the **mapper attribution and vintage for treaty 978 remain unretrieved**.
  Live residual: `GAP: china-switzerland-bit-2009-forum-provision-text` — the treaty and Protocol
  texts are unread, and that gap was ruled **structurally unreachable through the relay** on
  2026-08-05 and re-routed to the operator as a manual retrieval.
- **Recorded** — Gap-marker dispositions in the 2026-07-31 close-out (`f03a90e`); the closure in
  `analytics/daily-research/2026-08-04.md`; the re-routing in the 2026-08-05 close-out; the
  identification discharge in `analytics/daily-research/2026-08-06.md` Part 2 Task 2 and Part 6;
  `STATE_OF_THE_ANSWER.md:44` and `:88`.
- **Next** — Not analyst work. The provision text is with **Emory**, to be executed in one pass
  with the treaty-978 mapper-attribution and vintage retrieval, capturing a preserved
  `source_snapshot`. Optional and unscheduled: the converse false-*id* control, which would close
  the identification residual.
- **Owner** — Emory (operator) for the provision text and the mapper attribution;
  [[research-analyst]] retains the cell's wording in `STATE_OF_THE_ANSWER.md`.

### A5 · Huawei v. Sweden (ICSID ARB/22/2) — award watch

- **State** — Converted this session from schedule inference to **docket fact**. ICSID's
  case-detail page lists Procedural Orders 1–8 only, no PO 9 or later and no award; status
  Pending; registered 21 January 2022, so the 2006 Rules govern by default. Baseline for the
  watch: **last docket activity 2025-07-10** (each party files a reply submission on costs).
  Both costs rounds slipped from PO 8's scheduled 6 and 20 June 2025 dates. The proposed
  `huawei-arb-22-2-rules-vintage` marker was deliberately **not opened** — substantially
  answered in vetting by ICSID's own citation of "ICSID Arbitration Rule 37(2)" for 2024
  events, which is 2006-vintage numbering.
- **Recorded** — Task 1 and the standing-docket status block in
  `analytics/daily-research/2026-07-31.md` (`f03a90e`); `state/research_log.json` open
  thread 4, which carries this alongside Hela Schwarz and Einarsson.
- **Next** — Watch for an award or a PO 9 against the 2025-07-10 baseline. A PO 1 read is
  optional and no longer queued.
- **Owner** — [[research-analyst]].

### A6 · First-application tracker — next cycle

- **State** — **Adopted** 2026-07-31 after the four-lens review: when a codified
  early-determination mechanism enters the record as a named open thread (2026 ICC Art. 30,
  ICSID Rule 41 / AF Rule 51(1), the UNCITRAL Supplementary Provisions early-dismissal
  provision), a standing item watches for the first reported application of it in any
  investment case touching IP, data, or trade secrets. Baseline is the officer-verified null
  against ICSID's manifest-lack-of-merit decisions table; the withdrawn FY2025 "3 decisions
  within 60 days" statistic stays barred from that baseline.
- **Recorded** — `analytics/optimization-log.md`, entry dated 2026-07-29, status "adopted
  2026-07-31" (`de7b0fc`); Next Step 5 in the close-out (`f03a90e`).
- **Next** — First monthly cycle, **late August 2026**. Two or three targeted searches. Zero
  budget until then; it was explicitly not searched on adoption day.
- **Owner** — [[research-analyst]].

### A7 · Codified manifest-lack-of-merit gates — standing question

- **State** — Open standing question, no movement recorded: will the spread of codified
  manifest-lack-of-merit gates (2026 ICC Art. 30; ICSID AF Rule 51(1)) produce any
  disposition touching IP-as-investment, as distinct from abuse-of-right admissibility?
  A6 is the operational tracker this question feeds.
- **Recorded** — `state/research_log.json` open thread 2.
- **Next** — Carried; answered through A6's monthly cycles rather than searched directly.
- **Owner** — [[research-analyst]].

### A8 · ASIL ILIB reconciliation — split; **entered in this register 2026-08-06**

- **Why this entry exists.** The thread was **re-inherited four times as an un-executable plan**
  because it lived only in `state/research_log.json` and the archival council-log line, and never
  in this register — the one file that assigns owners. That is the whole mechanism of the failure,
  and writing the entry is the fix. Standing rule it produced: *a next action that cannot be
  executed is worse than an open question, because it reads as a plan and defers the seat that
  reads it.*
- **State** — **RULED UN-EXECUTABLE AS FRAMED 2026-08-05, and SPLIT.** The next action it carried
  named "the officer's saved raw HTML" (`asil_target.html`) — an artefact written to a per-session
  scratchpad on the operator's **local** machine (`analytics/daily-research/2026-08-01.md:362-363`)
  and **never committed**; it exists on no branch. Both `asil.org` and `unis.unvienna.org` are
  absent from the relay's `ALLOWED_HOSTS`, so neither limb is relay-reachable, and direct fetch is
  dead in the scheduled cloud session class. The thread was un-executable from the moment the
  2026-08-01 session closed.
- **Disposition — two limbs, neither with the analyst.**
  1. **SP-subject-matter delta — FOLDED into A1.** Fully stated in the record already and
     resolvable only by the adopted Supplementary Provisions text. It needs no ASIL retrieval ever,
     and rides on A/81/17's publication. **Owner:** [[research-analyst]], via A1.
  2. **The unisl398 limb — ESCALATED to the operator.** It is not housekeeping: the record's
     confirmation of UNCITRAL adoption rests on unisl400, **whose body is 403-blocked with only the
     title confirmed** (`STATE_OF_THE_ANSWER.md:105`), so a third party citing a UNIS release the
     record does not carry is a question about the record's own foundation. No allowlist change is
     proposed. **Owner:** Emory (operator).
- **Recorded** — `state/research_log.json` open thread 7; the ruling and split in the 2026-08-05
  close-out; this entry per Next Step 5 of that close-out, discharged 2026-08-06.
- **Next** — Nothing for the analyst. Limb 1 waits on A1; limb 2 waits on Emory.
- **Owner** — Split as above; **no unassigned action remains.**

---

## B · Instrument threads

### B1 · Silent-decay source-health guard — first live run

- **State** — Merged and tested, **not yet exercised**. `src/source_health.py` plus
  `tests/test_source_health.py` track per-source consecutive zero-item runs in
  `state/source_health.json`; an ACTIVE source hitting three consecutive zero runs is
  reported `DEGRADED (N zero runs)` in `meta.json`, the digest README and the digest header,
  and an all-but-one-zero run raises `COLLECTION ANOMALY`. Nothing in it ever raises.
  Evidence it has not run: `state/source_health.json` does not exist, and the newest archived
  run (`digests/2026-07-27_ISDS-Thematic-Watch/meta.json`) carries a `source_health` table
  with statuses but no streak data.
- **Recorded** — `e31e0c6`, merged to main by `8178f1f` (PR #23 — **not** PR #32).
- **CLOSED 2026-08-04 — it ran.** The first live run was 2026-08-03 as predicted.
  `state/source_health.json` now exists and carries per-source streaks (`italaw`,
  `iisd_itn`, `google_alerts`, `bing_news`, `gmail_scholar` all at `zero_streak: 1`;
  `icsid`, `iareporter_headlines`, `unctad_isds`, `pca_press` at 0), and
  `digests/2026-08-03_ISDS-Thematic-Watch/meta.json` is the first archived run to carry them.
  `health_warnings` is `[]`, and that is a **cold-start artefact, not a statement of source
  health** — with `DEGRADED_AFTER = 3` at `src/source_health.py:33` and a weekly cron, no source
  can be flagged before **2026-08-17**.
- **Successor** — Two defects in the guard, both found by the systems seat on 2026-08-04 and
  both dated: `NOT-READ (reason)` is absent from `_EXEMPT_STATUSES`
  (`src/source_health.py:50`), so on 2026-08-17 the guard will overwrite a refused source's
  honest status with `DEGRADED` and publish a causal claim about fetchers that the standing
  blocked-vs-quiet rule forbids; and `bing_news` is absent from `ACTIVE_SOURCES`
  (`src/source_health.py:39-47`) though `HANDOFF.md:115` documents it as active, so it can
  never be flagged at all. Escalations 3 and 4 of `analytics/daily-research/2026-08-04.md`
  (`51bb7a2`), verified against the source by this seat.
- **Owner** — [[systems-designer]] on Emory's go-ahead; `src/` is outside every agent's
  unilateral reach.

### B2 · `source_analytics.py` same-window patch

- **State** — Diagnosed, patched, tested, and **held**. The receptivity report mixes windows:
  10 archived runs in the denominator against per-source counts from 5 of them, so
  `analytics/source-receptivity.md:15` currently reads `italaw | 2 | 4 | 200%`. The patch
  corrects italaw 200%→50% and iareporter 17%→≈10% while preserving the lifetime figure of 13
  the council actually cites; four tests pass on the patched copy and fail on the current one.
  Not applied — **edits to `scripts/` require Emory's sign-off**.
- **Recorded** — Part 5 §2 of `analytics/daily-research/2026-07-31.md` (patch text) and Next
  Step 4 (`e05f834`, `f03a90e`); escalation 2 in the same close-out.
- **Next** — Blocked on **C2**. On sign-off: apply the patch and tests, regenerate
  `analytics/source-receptivity.md` in the same commit, and qualify the `COUNCIL.md:25`
  receptivity prose as same-window.
- **Owner** — Emory decides; [[systems-researcher]] executes.

### B3 · Health column in the receptivity report

- **State** — *Proposed*, dedup-checked, sourced to dbt's source-freshness pattern. The
  receptivity ledger — the artifact the council actually reads to judge which sources earn
  their place — never sees the health data `src/source_health.py` already computes and
  persists, which forces the analytics seat to re-derive zero-streaks by hand against a seat
  rule that exists precisely because hand-copying is error-prone.
- **Recorded** — `analytics/optimization-log.md`, entry dated 2026-07-31 (`f03a90e`).
- **Next** — **Sequenced behind B2** — land after, never bundled with, the same-window patch.
  Adoption condition, stated as a condition and not a nicety: the column must carry an
  explicit "as of &lt;latest run date&gt;" label, or it reintroduces the window-mixing failure
  B2 removes, one column over.
- **Owner** — [[systems-researcher]], after Emory's B2 sign-off.

---

### B4 · The retired Ring 3 formulation survived in four files — **CLOSED 2026-08-06**

- **State** — `ae1f04b` converted twelve of the fifteen Definition-B surfaces [[Claim Map]] C13
  had listed. Four survived, and the serious one was `prompts/research_analyst.txt:18`: the fix
  replaced the tail of the sentence and left the head, so the analyst prompt asserted **both**
  definitions at once and did not parse. Every analyst session read it. Also
  `METHODOLOGY.md:26` (the defining sentence, while its own heading already said Dimension),
  `working/02c-framework-rings.original.txt:7` (the retired definition as a heading, plus a
  claim false of two of the three seeds), and `working/one-pagers/philip-morris-v-australia.md`
  at `:18`, `:22` and `:30`.
- **Closed** — `373cce6`, PR #59. All four converted.
- **Why it is worth keeping in the record** — a partial find-and-replace is more dangerous than
  no replace at all: it leaves a sentence that reads as corrected and asserts the opposite.
  The lesson for any future definitional change is to grep for the *retired* phrasing after
  the sweep, not only for the new one.
- **Owner** — closed; no action.

### B5 · `check_currency.py` covers 5 of 13 anchored notes, and nothing runs it

- **State** — Opened 2026-08-07. `scripts/check_currency.py` (`fb1c04e`, 2026-08-06) mechanises
  the snapshot-anchor convention: it parses `Audited against <sha>`, checks the sha exists and is
  an ancestor of HEAD, and lists every commit that has touched the note's declared paths since.
  Two gaps. **(a) Coverage.** Its `TRACKED` map at `scripts/check_currency.py:62-71` holds five
  entries — the four index notes and `STATE_OF_THE_ANSWER.md` — while `grep -l "Audited against"
  agents/*.md` returns **thirteen**. The nine seat notes, which are the files an agent loads
  before working, are unguarded. **(b) Nothing runs it.** `grep -rn check_currency
  .github/workflows/` returns nothing, where `scripts/check_models.py` and
  `scripts/check_marks.py` are each wired to a workflow. A guard that has to be remembered is the
  control class the systems seat itself ruled fails silently.
- **Why it is worth doing** — the defect this session found is precisely in the uncovered set:
  all nine seat notes were three days and fourteen adopted rules stale, and one of them caused a
  taxonomy numbering collision (C11). A guard pointed at the indexed notes rather than the read
  notes cannot see that.
- **Recorded** — [[obsidian-archivist]], audit slice 2026-08-07, finding 1;
  [[Project Change Log]] 2026-08-07.
- **(c) A third gap, found by running the guard against `main` after the audit landed.** An audit
  session writes `Audited against <sha>` where `<sha>` is the commit it audited — necessarily the
  commit *before* its own. Landing that change set then touches the declared paths, so the guard
  immediately reports the two notes the session just refreshed as STALE by exactly one commit:
  their own. Verified at `3d474e0`, where `agents/Project Change Log.md` and
  `agents/Workflow Threads.md` each report *"1 commit(s) touched its declared paths since
  `7c08dcf`"*, and that commit is `8a40a4a`, the audit itself. **The anchors were deliberately not
  chased**, because bumping them would produce the same result on the next commit — the loop is the
  finding, not a thing to edit around. Consequence for a reader: a STALE line naming only the
  session's own landing commit is an artifact, not drift. A guard that cannot distinguish the two
  will be learned to be ignored, which is how a control dies.
- **Next** — Three things, (a) and (b) first. (a) Add the nine seat notes to `TRACKED` with their
  declared paths. (b) Wire the script into a workflow beside `model-consistency.yml`. (c) Decide
  how a note's own landing commit is treated — the narrow options are to exclude commits that
  touch *only* the tracked note itself, or to report self-reference as a distinct third status
  rather than as STALE.
- **Owner** — [[systems-designer]] on Emory's go-ahead; `scripts/` and `.github/` are outside the
  archivist's paths.

---

### B5 · The prose statements the publication gates left behind — **OPENED 2026-08-08; five closed, THREE OPEN, and five NEW ones in the opposite direction (2026-08-09)**

> **Re-read in the files, 2026-08-09. This pass was briefed that the thread was resolved; it is
> not.** Of the eight statements below, **five are repaired** — `METHODOLOGY.md:49` (by inline
> amendment, keeping the original sentence as the design record), `README.md:80-86`,
> `HANDOFF.md:100`, the homepage flow step, and the already-unreachable
> `templates/digest.html.j2` clause. **Three are untouched:** `fingerprint.yaml:4-6`, the
> `quality-bar` card at `views/isds-workflow-3d/workflow.json:177`, and the `src/main.py`
> comment — **which moved from `:497-500` to `:687-690`**, so the line number in the original
> entry below no longer finds it and only the quoted text did. All three are the ones needing
> an owner other than the seat doing the repair, which is the predicted survivor set.
>
> **And the repair created its mirror image on the same day.** `VALIDATION_STATUS_ONLY`
> (2026-08-09) holds item publication **including items at or above 40**, so four of the five
> sentences just repaired — each of which now says items at or above the threshold *are*
> surfaced — are stale again, pointing the other way. `METHODOLOGY.md:49` and `:69` contradict
> each other twenty lines apart: the same defect, in the same file, reintroduced by the fix for
> it. That set is [[Claim Map]] **C16**, and **the two must be fixed as one change set** —
> `fingerprint.yaml` and `METHODOLOGY.md:49` appear on both lists.
>
> **The generalizable rule this thread now argues for:** when a change adds a gate *upstream*
> of an existing gate, every sentence describing the downstream gate silently becomes a claim
> about the pair. Prose that names a flag is not enough; prose must name **both flags and which
> is on**, or it will be wrong again at the next flip.

*The original 2026-08-08 entry follows, corrected in place only where a line number moved.*


- **State** — **The sharpest live divergence in the project.** `FILL_FLOOR_SUSPENDED` defaults
  ON (`src/config.py:31-39`), so sub-40 items no longer surface. **Eight** files still describe
  the fill as operative or quote the retired quiet-week wording: `METHODOLOGY.md:49`,
  `README.md:79-86`, `HANDOFF.md:99-101`, `fingerprint.yaml:4-6`,
  `scripts/site_templates/index.html.j2:186` (**the public homepage**),
  the `quality-bar` card in `views/isds-workflow-3d/workflow.json`, and
  `src/main.py:497-500` *(now `:687-690` — the comment moved on 2026-08-09 and its text did
  not)* (a code comment naming a "never-empty rule" and quoting text the same
  function no longer emits). **The numbers did not move** — `RELEVANCE_FLOOR` is still 25,
  `MIN_DIGEST_ITEMS` still 6 — so every numeric guard passes and every behavioural sentence is
  wrong. `scripts/check_claims.py` carries no fact for the fill. **The worst instance is inside
  one file:** `METHODOLOGY.md:49` says the digest is filled toward six; `METHODOLOGY.md:67`
  says that rule is suspended. Eighteen lines apart, in the document that goes to
  Dr. Benavides.
- **Recorded** — [[Claim Map]] **C15**, which lists all eight with quoted text; `src/config.py`,
  `src/main.py`, `src/render.py` on `fix/restore-council-label` (uncommitted).
- **Next** — **One coordinated change set, or none.** There is no partial version of this fix
  that is not a relocation of the contradiction. The durable wording names the **flag** rather
  than describing one of its settings as the behaviour — because if the fill is ever restored
  by setting `FILL_FLOOR_SUSPENDED=0`, the eight statements become true again and
  `METHODOLOGY.md:67` becomes the false one.
- **Owner** — split, which is why it needs coordinating: `METHODOLOGY.md` and `README.md` are
  **Emory's**; the `quality-bar` card is a manifest edit by [[systems-designer]] on Emory's
  go-ahead; `scripts/site_templates/` and the `docs/` rebuild are [[site-experience]]'s;
  `src/main.py:687-690` and `fingerprint.yaml` are [[systems-designer]]'s.
- **Next, as of 2026-08-09** — one change set covering **C15**'s three survivors **and C16**'s
  five. `HANDOFF.md` is [[obsidian-archivist]]'s and was corrected in this pass, which is why
  it no longer appears on either open list.

---

### B6 · D/E ring contract, F semantic triage, G headline lane — **ALL BUILT 2026-08-09; each off by default**

- **State** — **Rewritten 2026-08-09: these are code now, not designs.** The thread's original
  job was to stop anyone reading the 08-08 session as having shipped them; its job now is the
  inverse and narrower — **to record that "built" is not "on"**, because four separate flags
  stand between this machinery and anything a professor sees, and every one of them is off or
  holding.
  - **D/E — the ring-evidence contract is real.** `src/rings.py` derives, in shadow on every
    cycle, per-ring strengths, a deterministic treaty nexus, evidence location and validity,
    and a lane. A match requires the IP ring **plus** a second doctrinal ring **plus** a
    supported nexus **plus** valid evidence, so a no-IP judicial case can never be a match
    whatever it scores. `STATE_MODEL_V2="on"` is **refused** until
    `STATE_MODEL_V2_PUBLICATION_READY`, which is `False` (`src/config.py:98`, `:109-111`).
  - **The semantic V2 path is built end to end** — `src/classify_v2.py`,
    `prompts/classifier_v2.txt` — and **`V2_SHADOW_CALLS` defaults off**
    (`src/config.py:154-195`), so every default-run verdict is labelled `lexical_only` and
    `V2_SHADOW_CALLS=replace` is refused outright. Verdicts carry `claims_source` provenance,
    and **`guard_demoted` fires on every V1 ring claim** — not a defect but the honest reading
    of V1, which supplies no spans to check.
  - **F — `src/triage.py` + `prompts/triage.txt`**, `TRIAGE_ENABLED` off by default
    (`src/config.py:220`), deterministic sort, provider absence **recorded rather than
    misreported**, adversarial tests.
  - **G — `src/headline_lane.py`**, a closed grammar with **three location-keyed limitation
    clauses**, not one (`:81-85`). The reason is a real error a single clause would have
    produced: a comparator whose body *was* retrieved must not tell the reader it is paywalled.
    `scripts/check_headline_lane.py` holds the output byte-identical.
  - **The state space grew because a gap closed.** The 7-vs-4 outcome question resolved
    losslessly — seven logical states onto four operational outcomes plus metadata — and the
    enumeration went from 12,288 to **21,504** (`src/rings.py:112`). **Tail provider failures
    are now counted**; they had been under-counted by exactly the size of the tail.
- **The one piece that is NOT built, said plainly** — R2.1 **design (c), the stratified tail
  audit, is a configuration stub**: `TAIL_AUDIT_N = 0` (`src/config.py:229-243`), expressly
  unimplemented. It is named here so the workstream is never reported complete on the strength
  of F and G.
- **Recorded** — `src/rings.py`, `src/classify_v2.py`, `src/triage.py`, `src/headline_lane.py`,
  `src/config.py`, `prompts/classifier_v2.txt`, `prompts/triage.txt`,
  `scripts/check_headline_lane.py`, `tests/test_rings.py`, `METHODOLOGY.md:69`,
  `analytics/state-space-resolution-2026-08-09.md` (all uncommitted,
  `fix/restore-council-label`).
- **Next** — (1) the tail-audit stub; (2) **the validation decision** that could ever set
  `STATE_MODEL_V2_PUBLICATION_READY` — which is gated on the locked set (**B7**) and therefore
  on retrieval (**C13**), so it is not a build task; (3) primary retrievals; (4) operator
  labelling. **Nothing here should be turned on to see what happens** — each flag's default is
  the deliverable.
- **Owner** — [[systems-designer]] for the stub; Emory for every flag flip; agenda from
  [[council-chairman]].

---

### B7 · The locked validation set — created empty, on purpose

- **State** — `analytics/locked_set/` holds `SCHEMA.md` and `RETRIEVAL_LEDGER.md` and **zero
  items, by design**. The 54-item, 9-category production-path set is specified, together with a
  five-step commit order that makes blindness provable from git history: `items.json` first,
  then a SHA-256 lock, then `labels.json` in a separate file with **no score field**, then its
  lock — "only now may any scorer touch the set." ~~A `scripts/check_lock.py` is **proposed, not
  written**.~~ **Written 2026-08-09** — see below. The reason the directory is empty is stated in it: the candidate matters named in
  the R2.1 record are *leads*, several dockets and dates unverified, and per the carrying-span
  rule **no item enters the set on a memo's authority**.
- **2026-08-09 update — the cheap half is done, and it got the empty case right.**
  `scripts/check_lock.py` exists and is wired into CI. Run today it exits 0 with
  "*no LOCK.md and no locked files: the set is deliberately empty
  (`analytics/locked_set/SCHEMA.md`), which is the **designed current state and not an
  error**.*" That distinction is the whole value of the guard: a naive implementation would
  either fail on an empty set (crying wolf until retrieval finishes) or pass silently on a
  *deleted* one. It also means the guard will start doing real work the moment the first item
  lands, with no second change needed.
- **The set is still empty of items, and retrieval has not moved today.**
  `RETRIEVAL_LEDGER.md` re-read 2026-08-09: **2 RETRIEVED** (both Vanda CFC slip opinions),
  **3 BLOCKED**, **8 QUEUED** — identical to 2026-08-08. The H&H documents retrieved this
  session went into `seeds/` for the comment package and **have never had a row in this
  ledger**, so they neither advance nor appear in these counts. Recorded so the day's genuine
  retrieval is not mistaken for progress on the locked set.
- **Recorded** — `analytics/locked_set/SCHEMA.md:1-11` and the file table; `RETRIEVAL_LEDGER.md`;
  `scripts/check_lock.py`; `.github/workflows/pipeline-guards.yml:130-131` (all uncommitted,
  `fix/restore-council-label`).
- **Next** — Nothing may be added until the corresponding primary document is retrieved and its
  pinpoint verified; retrieval is **C13** below and is Emory's. The guard half is complete.
- **Owner** — [[research-analyst]] for item drafting **after** retrieval; Emory for retrieval.

---

### B8 · Three guards exist and none of them runs in CI — **OPENED 2026-08-08, CLOSED 2026-08-09**

- **State** — **CLOSED on the file, not on a report.** `.github/workflows/pipeline-guards.yml`
  exists and was read line by line this pass. It runs the two guards this thread was opened
  for and three more: telemetry-privacy (`:121-122`), seen-integrity (`:124-125`),
  headline-lane (`:127-128`), lock (`:130-131`), and currency in **its own job with
  `fetch-depth: 0`** (`:138-154`) — without that fetch depth the currency check cannot see the
  history it asserts against, which is the kind of detail that makes the difference between a
  guard and a green tick.
- **It closed better than it was written.** The thread asked for wiring. What landed also runs
  **each guard's own planted-violation tests** (`:101-111`) — the telemetry guard against a
  planted text field, the seen-integrity guard against a planted missing ledger line, the lane
  guard against planted conclusions, the lock guard against a planted tamper. **The guards are
  now themselves guarded**, which answers the failure mode this thread named: a fail-closed
  check that has silently stopped checking is worse than none, and only a planted violation
  catches that.
- **Recorded** — `.github/workflows/pipeline-guards.yml` (untracked, `fix/restore-council-label`).
- **What remains, and it is not this thread** — the workflow file is **uncommitted**, so
  nothing fails a pull request yet. Authorizing that is **C11**, Emory's, because it changes
  what blocks a merge. The build half is done; the decision half is not.
- **Owner** — closed; residual decision at **C11**.

---

### B9 · `check_site_sync.py` is a mutating command wearing the name of a check — **OPENED 2026-08-09**

- **State** — **Open defect, found by it doing the damage.** `scripts/check_site_sync.py`
  **rebuilds `docs/` in place**: `:25` invokes `scripts/build_site.py` with no temporary
  directory, and `:31` then runs `git diff -- docs/` against the working tree. So a command
  every seat treats as read-only **writes to the repository as its first act**. This session it
  reverted `docs/` to HEAD, the designer having read it as stamp-only. The output message even
  says "OK: `docs/` is in sync with source (only the build stamp differs)" — reassuring, and
  produced by a run that has already overwritten the directory it is reporting on.
- **Why it matters beyond the one revert** — the vault's standing rule is "`docs/` is never the
  fix; change the source, rebuild, and let `check_site_sync.py` prove it" ([[Claim Map]]
  maintenance rule 5). That rule tells every seat to run this script, and the script is not
  safe to run on a dirty tree. The rule and the tool disagree, and the tool wins silently.
- **Recorded** — `scripts/check_site_sync.py:25`, `:31`, `:47`; `HANDOFF.md` 2026-08-09
  checkpoint carries the warning; designer deviation of record for 2026-08-09.
- **Next** — Build the site into a temporary directory and compare, so the check is genuinely
  read-only; or, at minimum, refuse to run when `docs/` is dirty. Until then `docs/` is rebuilt
  from source in the integrator's final battery, and **no seat should run this script to
  "check" anything.**
- **Owner** — [[systems-designer]] (`scripts/` is that seat's); [[site-experience]] is the
  affected surface.

---

## C · Awaiting Emory

These are the operator's, and no agent may execute them. Each is stated with what
specifically unblocks it.

### C1 · Ledger snapshot amendment for `da33a30be92ab234`

- **State** — The China–France escalation closed on this mark, but the ledger's preserved
  `source_snapshot` omits the two load-bearing elements — the no-prerequisite line and the
  FET characterization — which exist only in the table Emory pasted in chat on 2026-07-27.
  Until amended, every statement of those two elements in the living memory must carry:
  *sourced to the operator's chat-supplied table (supporting_locator); not in the ledger's
  preserved source_snapshot; the record cannot self-verify these two elements.* This is the
  B2 objection the chairman accepted and escalated rather than executed — the ledger is
  operator-owned.
- **Recorded** — Escalation 1 and ruling B2 in `analytics/daily-research/2026-07-31.md`
  (`f03a90e`).
- **Next** — A one-minute action: re-run the mark with a fuller snapshot, or append a
  snapshot-amendment note quoting those two rows. Also confirm whether `scope_ok: false` was
  intended to stand.
- **Owner** — **Emory.**

### C2 · `scripts/` sign-off for the `source_analytics.py` patch

- **State** — Verified against the real digests tree, four tests passing on the patched copy
  and failing on the current one, patch text supplied in full. Awaiting authorization only.
- **Recorded** — Escalation 2 in `analytics/daily-research/2026-07-31.md` (`f03a90e`).
- **Next** — Sign off or decline. Unblocks **B2**, and then **B3**.
- **Owner** — **Emory.**

### C3 · `unctad_isds` keep-or-retire

- **State** — Standing decision, carried unchanged from 2026-07-30 and deliberately not
  re-argued. The evidence: `unctad_isds` fetches 25 items and dedupes to 0 on every recorded
  run — a fetch spent per run on a static page, 0 surfaced ever. New datum from 2026-07-31:
  the day's one settled fact of record came by hand from the **IIA Mapping Navigator, a
  sibling database on the same host** (`investmentpolicy.unctad.org`) that nothing polls,
  while the source's own `BASE_URL` points at the ISDS Navigator case list
  (`src/sources/unctad_isds.py:29`). The analytics officer flagged this explicitly as a
  decision datum and explicitly declined to inflate it into a proposal — treaty-mapping
  records are reference data, not events. `google_news_rss` (disabled, 0 in 10) rides with
  the same decision.
- **Recorded** — Escalation 3 in `analytics/daily-research/2026-07-31.md` (`f03a90e`); the
  observation in Part 4 §3 of the same record; escalation 2 of the 2026-07-30 close-out
  (`754ce32`).
- **Next** — Retire, repurpose, or keep. No build without sign-off.
- **Owner** — **Emory.**

### C4 · Emailer CONSISTENCY WARNING — confirm what was received

- **State** — Unanswered across two sessions. The 07-28 and 07-29 records breached the Rule 1
  protocol sentence, so the emailer plausibly printed a visible CONSISTENCY WARNING on those
  sends; the 07-30 record was the first compliant one. The question is what Emory actually
  received for the **07-21 through 07-29** sends — the record cannot determine this from
  inside the repository.
- **Recorded** — Escalation 3 in the 2026-07-31 close-out (`f03a90e`); escalation 3 of the
  2026-07-30 close-out (`754ce32`); the rule itself in `prompts/daily_council_protocol.md`.
- **Next** — Confirm which of those sends carried a warning banner.
- **Owner** — **Emory.**

### C5 · Talkwalker alert URLs

- **State** — Setup step never completed. `alerts.yaml` records that the Google Alerts feeds
  "have been returning zero entries since mid-July 2026" and documents Talkwalker as the
  free replacement, with instructions to paste RSS URLs under `feeds:` alongside or instead
  of the Google ones — the poller treats every URL identically. The `feeds:` list at
  `alerts.yaml:30-42` still contains **only Google URLs** — twelve of them, zero
  non-Google entries when the file is parsed. Corroboration that the lane is dry: `google_alerts` returns 0 in
  `digests/2026-07-27_ISDS-Thematic-Watch/meta.json`. Creating the alerts requires a browser
  and an account, so no agent can do it.
- **Recorded** — `alerts.yaml:12-17` (instructions) and `alerts.yaml:29-42` (the feed list as
  it stands).
- **Next** — Create the Talkwalker alerts, choose RSS delivery, paste the URLs under
  `feeds:`. No code change is needed. Until then `google_alerts` is a live source polling
  feeds that return nothing.
- **Owner** — **Emory.**

### C6 · Delegated-session cadence and budget

- **State** — Standing decision, carried unchanged and not re-argued. The first delegated
  session hit the account's monthly spend limit mid-meeting. The chairman's return-path
  protocol and spend checkpoint have since removed both transport-fault classes and made a
  mid-session termination survivable, but the underlying cost question — daily, or reserved
  for substantive days — is still Emory's.
- **Recorded** — Escalation 3 in the 2026-07-31 close-out (`f03a90e`); escalation 1 of the
  2026-07-30 close-out (`754ce32`).
- **Next** — Set the cadence.
- **Owner** — **Emory.**

### C7 · Two flowchart cards assert a model no config file carries — **CLOSED 2026-08-05**

- **State** — Raised by this seat 2026-07-31: the `systems-designer` and `site-experience`
  cards in `views/isds-workflow-3d/workflow.json` named a model while neither definition
  declared a `model:` key, so the chart stated an assignment nothing configured. **Closed at
  `c25ea64`** by Emory's first option. Verified at `eac8ed9` on 2026-08-05: **all nine**
  `.claude/agents/*.md` files declare a `model:` key, and `python scripts/check_models.py`
  reports *"Checked 12 flowchart cards against `.claude/agents/`, `agents/` and
  `src/models.py` … ok — every card names a configured model, backed by a declared `model:`
  key, and no vault note contradicts its card."*
- **Recorded** — [[Claim Map]] C12 (corrected to CLOSED 2026-08-05),
  `analytics/vault-sessions/2026-08-05.md` Part C.
- **What replaces it, and it is smaller** — `model:` selects a **tier**, not a version
  (`scripts/check_models.py:36-38`), so the frontmatter can never disagree with a card about
  Opus 5 vs Opus 4.8. The version check rests on card ↔ `src/models.py` ↔ vault note, and the
  vault-note leg is conditional on the note stating a model in the ``**Model.** `…` `` form
  that `_VAULT_MODEL_RE` (`check_models.py:63`) matches. **Reformatting those notes would
  silently remove one leg of a CI guard.** No action open; recorded so nobody reformats
  blind.
- **Owner** — closed; [[obsidian-archivist]] holds the formatting constraint.

### C8 · `build_graph` block replacement spans a prose-quoted marker

- **State** — Found 2026-07-31 by actually running the script rather than reasoning about it.
  `scripts/build_graph.py:195` builds its replacement pattern from the **first** start marker
  in a file, so a note that quotes that marker in prose is destroyed on the second run — run 1
  appends the real block, run 2 spans from the prose marker to it and deletes everything
  between. `agents/obsidian-archivist.md` lost 92 lines this way and was restored from
  `689a9e7`; its prose no longer reproduces the delimiters. The vault is byte-stable today
  (two consecutive runs verified identical across 123 markdown files), but only because no
  note quotes the marker.
- **Recorded** — [[obsidian-archivist]] audit slice item 6, and the Open drift section of
  [[Project Change Log]].
- **Next** — Anchor to the last start marker, or skip markers inside code spans and fences
  (`_CODE_FENCE` is already compiled in the module), or fail loudly on a duplicate start
  marker. Wants a regression test whose fixture is a note that quotes the marker.
- **Owner** — **Emory** authorizes; [[systems-designer]] implements. Machinery, not vault.

### C9 · PR #33 — METHODOLOGY Parts III and VIII — **CLOSED**

- **State** — **Closed 2026-08-04.** `984f5eb` is an ancestor of `origin/main`, and no pull
  request is open on the repository. What the merge did *not* carry was the rest of that
  branch — the archivist's vault work — which is thread D1's story below.
- **Recorded** — `984f5eb`; branch tip `f195e21` recovered separately by PR #44 (`cb12a2d`).
- **Owner** — none; no action.

---

### C11 · CI wiring of the guards — **OPENED 2026-08-08; BUILT 2026-08-09, decision still Emory's**

- **State** — **The work is done and the decision is not.** `.github/workflows/pipeline-guards.yml`
  now exists and wires **five** guards plus their planted-violation tests (**B8**, closed). But
  it is an **untracked file on `fix/restore-council-label`**, so nothing fails a pull request
  today. Wiring guards into CI changes what blocks a merge, and that remains an operator
  decision rather than a seat's — the build being finished does not convert it into one.
- **Recorded** — `.github/workflows/pipeline-guards.yml` (untracked,
  `fix/restore-council-label`); `HANDOFF.md` 2026-08-09 checkpoint.
- **Next** — Emory says yes or no, and the yes is now cheaper than it was: the file is written
  and its own tests pass, so authorization is a merge rather than a project. **What it costs if
  deferred:** unchanged and now sharper — the telemetry privacy guard is the only thing between
  the telemetry stream and article text, and until this merges it still runs only when someone
  remembers to run it.
- **Owner** — Emory.

### C12 · Merge-or-skip before the Monday 13:00 UTC run — **OPENED 2026-08-08; ~1 DAY REMAINING as of 2026-08-09 (Sunday)**

- **State** — The whole two-session body of work is uncommitted on `fix/restore-council-label`.
  The weekly workflow fires `cron: '0 13 * * 1'` — **tomorrow**. **This is the only thread in
  this register with a deadline set by a machine, and it is now inside a day.**
- **The stakes changed on 2026-08-09 and the change is not small.** The 08-08 statement of this
  thread weighed "status-only cycle if nothing reaches 40" against "publishes under the old
  fill rule". `VALIDATION_STATUS_ONLY` replaces the first limb with something stronger: if this
  merges, Monday sends **no items at all** — not sub-40 leads, and not a match either if one
  appears — plus **no Research Brief**, and a status note carrying a held count. So:
  - **Merge** → Dr. Benavides receives, with no prior notice, an email containing zero items
    and new wording, and the weekly brief she may be expecting does not arrive. The instrument
    is behaving correctly and the recipient has not been told the behaviour changed.
  - **Skip** → Monday publishes under the old fill rule: sub-40 items, in the week the project
    concluded it should stop sending them, with the classifier's off-theme-at-55 hole still
    open.
  - **Third option, recorded on 08-08 and now more attractive:** merge, and disable the Monday
    run for one week, so the first item-less email is sent deliberately rather than by cron —
    and can be sent with a sentence of explanation.
- **Recorded** — `.github/workflows/weekly.yml`; `src/config.py:42-74`; `src/main.py:727-737`
  (the brief is skipped under the gate); `HANDOFF.md` 2026-08-09 checkpoint.
- **Next** — Emory decides. This seat records the options and does not recommend one; it does
  record that **all three options now send or withhold something the recipient has not been
  warned about**, which was not true of the 08-08 framing.
- **Owner** — Emory.

### C13 · Eleven externally gated retrievals — **OPENED 2026-08-08**

- **State** — `analytics/locked_set/RETRIEVAL_LEDGER.md` carries thirteen rows: **two
  RETRIEVED** (both *Vanda* Fed. Cl. slip opinions, in hand and verified) and **eleven not** —
  three BLOCKED (Tethyan Copper ¶¶ 1283/1288/1327–1333, paywalled at IIC 1603 (2019);
  Thailand—Cigarettes ¶¶ 7.410–7.411, PDF text layer will not extract; Lord Falconer's 2006
  Manchester speech, absent from the UK Government web archive) and eight QUEUED (the
  15 J. Marshall bound volume on the 999-vs-228 pagination; *Philip Morris v. Uruguay*
  Decision on Jurisdiction ¶ 185; the Vanda **Federal Circuit** docket; the Landreau award;
  the EMA Policy 0070 post-2023 sequence; Lentner, 34 ICSID Rev. 569 (2019); the
  *OI European Group v. Venezuela* award; and the IBA/ICC/Aceris evidence instruments).
- **Recorded** — `analytics/locked_set/RETRIEVAL_LEDGER.md` (uncommitted,
  `fix/restore-council-label`).
- **Next** — Library access, one pass, capturing a preserved `source_snapshot` for each. **None
  of these may be converted to verified by inference, and none has been.** The three BLOCKED
  rows need a decision rather than effort: a paywall and a broken text layer are not solved by
  trying again.
- **Owner** — Emory (operator), as the only seat with library access.

### C14 · The 13-item retrospective labelling protocol — **OPENED 2026-08-08**

- **State** — Designed and unrun. Label the 13 distinct published items against
  `L_theme ∈ {0,1}` **from the source page, not the annotation**, recording the label before
  reading the annotation, with a one-sentence written reason naming which rings are present and
  absent. **Blindness cannot be claimed retrospectively and the protocol does not claim it** —
  the machine scores are already on the page. Ten of the 13 rest on paywalled bodies, so
  `cannot_assess` is the expected outcome for most; the informative sample may be **3–4 items**,
  and the protocol says to report it with that limit stated **or not at all**.
- **Recorded** — `analytics/retrospective-audit-2026-08-08.md` §6 (uncommitted).
- **Next** — Emory's, 13 codings, recorded through `scripts/verify_digest.py` so each lands in
  the append-only ledger under the operator's identity. **One defect to route around:** that
  script's URL-dedupe presents only the 2026-06-10 Telefónica verdict, and the 06-09 verdict
  must be assessed too. **Why it is worth doing before the 54-item locked set:** it measures the
  real production distribution at the cost of 13 codings and moves no holdout label, so it
  cannot disturb [[Claim Map]] C1.
- **Owner** — Emory (operator).

---

## F · Branch hygiene — what is committed but not landed

### C10 · Published counts on the live site count events, not distinct things — **CLOSED 2026-08-06**

- **State** — `9bd112e` published "seven of the fourteen items published to date"
  (`base.html.j2`, 16 pages) and "11 runs across 347 candidates" (`index.html.j2`, 19 pages).
  Measured from the committed archive: 14 article files, **13 distinct URLs**.
  `https://www.italaw.com/cases/12153` (Telefónica v. Colombia) appears in both the 06-09 and
  06-10 runs.
- **Not a dedup bug** — `8e1cc48` ("chore: reset seen-state for final full-digest send")
  emptied `state/seen.json`, so `is_seen()` had nothing to match. `src/state.py` is correct and
  was not touched.
- **The real defect** — the classifier returned **contradictory verdicts on identical input**:
  relevance 32 with ring `judicial_or_regulatory_measure` on 06-09, relevance 28 with no rings
  on 06-10, same URL and same source text. The duplicate therefore falls on **both sides** of
  the ring split and cannot be assigned to either without arbitrarily preferring one of the two
  verdicts the instrument itself gave it. First recorded as "7 one-ring / 6 zero-ring", which
  made exactly that arbitrary choice; corrected at `9efafb0` to the honest form — twelve of
  thirteen carry a single verdict, six with a ring and six with none, and the thirteenth is the
  duplicate.
- **Closed** — `9efafb0`, PR #59. "347" now reads as 347 **screenings** across a window
  containing two manual state resets, which is what it is.
- **`tests/test_site_claims.py` needed no change** — runs/screened/matches/surfaced are counts
  of runs, screenings and entries, and all four remain correct. The defect was the prose
  labelling them.
- **Owner** — closed; no action.

### C11 · Taxonomy entry 27 was adopted twice, for two different patterns

- **State** — Opened 2026-08-07. The chairman adopted **27 · scope-mixed screen** on 2026-08-06
  (`analytics/daily-research/2026-08-06.md:940`, `aa48406`) and **27 · manufactured residual** on
  2026-08-07 (`analytics/daily-research/2026-08-07.md:975`, `7adfd68`). Both rulings are on the
  record; neither is wrong on its own terms.
- **Cause, and it is the archivist's** — `agents/integrity-officer.md` is the taxonomy's
  canonical home and the integrity officer's mandate directs it to read that table rather than
  recite from memory. The table's heading read *"24 entries as of 2026-08-04"* on 2026-08-07,
  with 25, 26 and 27 adopted and unwritten. The officer opened the table exactly as directed,
  found the last number it could see, and took the next. It flagged the staleness in the same
  note: "the vault table is stale again, in the single file the mandate names"
  (`analytics/daily-research/2026-08-07.md:713`).
- **What the archivist did and did not do** — all three missing entries plus the colliding fourth
  are now in the table, each under the number its ruling gives it, with the collision named. The
  archivist has **not** renumbered: doing so would change what two council rulings say.
- **Next** — The chairman and the integrity officer settle which pattern keeps 27 and which
  becomes 28, in a ruling that can be cited. Until then, cite entry 27 by name, never by number.
- **Owner** — [[council-chairman]] with [[integrity-officer]]; Emory only if they disagree.

### C12 · `build_graph` is whole-vault, and the archivist's merge authority is not

- **State** — Opened 2026-08-07 as a structural fact behind a pending item four sessions old.
  `build_graph --dry-run` at `7c08dcf` plans managed-block edits to seven files:
  `BOUNDED_CHANGE_PROTOCOL.md`, `agents/Claim Map.md`, `prompts/carrying_span_rule.md`,
  `lit-review/BIBLIOGRAPHY_TEMPLATE.md`, `analytics/daily-research/2026-08-06.md`,
  `analytics/daily-research/2026-08-07.md`, `analytics/vault-sessions/2026-08-04-council.md`.
  Three are inside the archivist's self-merge set (`analytics/`, `agents/`, `moc/`,
  `HANDOFF.md`); four are outside it. The script has no path filter.
- **Consequence** — a full `build_graph` run can never land under archivist authority, which is
  why the pending list has been carried since 2026-08-04 and has been described as a scope
  preference rather than what it is.
- **Next** — Either Emory runs it and merges, or the script gains a `--paths` filter so the
  archivist can discharge its own share. The second is [[systems-designer]] work.
- **Owner** — **Emory**, to pick between the two.

---

### D2 · The literature layer has never entered the verification ledger

- **State** — `analytics/verification_ledger.jsonl` holds 58 entries and
  `grep -ciE "kim|ferguson|marshall|proportional"` returns **0**, while
  `moc/Evidence Ledger.md:3-4` tells a reader that what the project knows lives in that ledger.
  For the two documents the research question rests on, it describes an empty set.
- **Why it stayed open for three months** — the articles were not on disk anywhere the tooling
  looked, so nothing could check them and nothing did. They were on the operator's desktop the
  whole time, and no seat asked. When they were finally read on 2026-08-06 the audits found
  nine substantive defects across the two memos, including an inverted disposition
  (Philip Morris v. Uruguay), a risk category absent from Ferguson entirely, and an unfounded
  adverse charge against Kim.
- **Partly addressed** — `scripts/check_sources.py` (`ae42639`, PR #60) now fails closed if a
  memo's declared source PDF is absent, so the silent-absence state cannot recur. The PDFs live
  in gitignored `seeds/` because they are copyrighted, which is why the guard is an operator
  gate rather than a CI check.
- **Still open** — whether the substantive Kim and Ferguson propositions get ledger entries at
  all. That is a scope decision about what the deterministic gate is for, and it is not an
  agent's to make.
- **Owner** — **Emory.**

---

### F1 · Seventeen operator ledger marks never merged

- **State** — Found 2026-08-04 by testing every remote branch tip with
  `git merge-base --is-ancestor <tip> origin/main`.
  `origin/chore/operator-marks-2026-07-27` (`6f9e1da`, 2026-07-27) fails that test and is the
  only unmerged branch carrying content the record needs. Its
  `analytics/verification_ledger.jsonl` holds 38 operator marks and 40 claims against `main`'s
  21 and 37 — **17 marks and 3 claims that `main` has never held**, all made by Emory in the
  2026-07-27 chat-verification sweep. Two of them are named as still-pending in
  `HANDOFF.md:147-152`: `5c25faf36673d6f3` (China–Germany BIT Art. 1(d), `--verified` against
  the official treaty text) and `7dd2f272f130f859` (*Hela Schwarz*, `--rejected` — the A&O
  Shearman page says jurisdiction *and merits*, not the failure-to-withdraw framing). The
  rejected framing does **not** appear in `STATE_OF_THE_ANSWER.md` today, so the living memory
  is not carrying a rejected claim; what is missing is the ledger's own record that Emory
  ruled on it.
- **Re-measured 2026-08-13, and nothing has moved in seventeen days.** The 2026-08-11 change-log
  entry said these marks reached `main`; they did not, and that line is struck above. Counted
  from the two blobs directly, not from any report:

  | | `claim_created` | `verification_changed` (marks) | distinct claim ids |
  |---|---|---|---|
  | `origin/main` | 37 | **21** | 37 |
  | `origin/chore/operator-marks-2026-07-27` | 40 | **38** | 40 |

  These are the **same figures F1 recorded on 2026-08-04**. `main`'s ledger is blob `f3dbbf6`,
  last written by `8891c21` (2026-07-27); no commit has touched it since.

- **What the gap costs, demonstrated rather than asserted.** `src/integrity_gate.py:150-177`
  replays the ledger and resolves each candidate by **exact claim-id lookup**
  (`verify.replay` → `verify.current_status`). Replaying both blobs and querying the three
  missing ids:

  | claim id (first 12) | subject | against `main` | against the branch |
  |---|---|---|---|
  | `7511d41b67ec` | *Hela Schwarz v. China*, final award dismissing all claims | `unverified` | `operator_verified` |
  | `f4375b9fb9f4` | UNCITRAL WG III 53rd session, provisions 1–9/11/12 as one package | `unverified` | `operator_verified` |
  | `f40761bdb9b0` | Svea Court of Appeal annulment, *Okuashvili v. Georgia* | `unverified` | `operator_verified` |

  All three carry `actor: Jack Emory Williams`, `quote_ok: true`, **`scope_ok: false`**, marked
  2026-07-27T21:58Z. Against `main` the gate cannot see that Emory ruled on them at all, so each
  is assertable only as an unverified lead. The `scope_ok: false` half is the adverse half named
  as [[research-analyst]]'s standing watch item — it is stranded together with the favourable half.
- **Not corrected here, deliberately.** The ledger is append-only and operator-owned; this seat
  does not write to it, and the `actor` field is a dated record, not a live statement, so the
  house rule against "Jack" in vault artifacts does not reach it.
- **Next** — Emory's call, and no agent should make it: `git merge origin/chore/operator-marks-2026-07-27`
  on a branch, or re-run the marks. The ledger is operator-owned and this seat does not write
  to it.
- **Re-measured 2026-08-16 against `d997c32`, on a complete 621-commit history. Day twenty, and
  nothing has moved.** `git merge-base --is-ancestor origin/chore/operator-marks-2026-07-27
  origin/main` still fails; `git cherry origin/main origin/chore/operator-marks-2026-07-27`
  reports **2** unlanded commits. Counted again from the two blobs: `main` 37 / **21** / 37 and
  the branch 40 / **38** / 40 — the same three numbers recorded on 2026-08-04 and 2026-08-13.
  `main`'s ledger is still blob `f3dbbf6`, still last written by `8891c21` (2026-07-27).
  **A caution for the next session that runs this query:** on the shallow clone this container
  started with (201 commits), `git log -- analytics/verification_ledger.jsonl` reported the
  last-touching commit as `cf7d99b` (2026-08-05) — wrong, and wrong in the direction that makes
  the ledger look *more* current than it is. Unshallow before reading history, every time.
- **Owner** — **Emory.**

### F2 · The 2026-08-03 standing-rules council record is lost

- **State** — The 2026-08-03 archivist session escalated `3d31de8` /
  `analytics/council-sessions/2026-08-03-standing-rules.md` (887 lines) as sitting on a
  worktree branch and not an ancestor of `main`. On 2026-08-04 the object is gone:
  `git cat-file -t 3d31de8` returns "Not a valid object name", no remote branch carries the
  file, and the worktree it lived in belonged to an ephemeral container. The two rules it
  adopted — third-party retrieval, and blocked-vs-quiet source status — are implemented on
  `main` (`0091ade`, `fe02f39`) and are cited by later sessions, so the project runs on them;
  their reasoning and the objections they answer are not recoverable from git.
- **Re-tested 2026-08-13 on a complete history, which the 2026-08-04 test did not have.** The
  container's clone was shallow (`.git/shallow` present, 577 commits); the earlier "not a valid
  object" could therefore have been an artefact of a partial object set rather than a real loss.
  After `git fetch --unshallow` (**584 commits**, back to the `0460699` scaffold of 2026-06-08):
  `git cat-file -t 3d31de8` still returns "Not a valid object name",
  `git log --all -- analytics/council-sessions/2026-08-03-standing-rules.md` is **empty**, and
  `git fetch origin 3d31de8` returns "couldn't find remote ref" — origin does not have it either.
  The loss is confirmed against the full history, not merely against a truncated one.
- **Next** — Nothing recovers it from the repository. If a transcript or scratchpad copy
  exists outside git it should be committed; otherwise the two rules should be restated from
  the sessions that cite them, which is council work, not vault work.
- **Owner** — **Emory** decides whether to reconstruct; [[council-chairman]] would execute.

### F0 · `fetch-relay` triggers on documentation edits, not just requests

- **State** — Found 2026-08-04 by this seat's own commit firing it.
  `.github/workflows/fetch-relay.yml:16-18` triggers on
  `paths: 'analytics/fetch-requests/**'`, which includes that directory's `README.md`. A
  four-line managed `Map:` block written there by `scripts/build_graph.py` fired a relay
  runner on PR #51. Harmless this time — no request file was added, so nothing was fetched —
  but it spends a runner on a documentation edit and puts a relay run in the history with no
  request behind it.
- **Next** — Scope the filter to request files, e.g. `analytics/fetch-requests/*.json`.
- **Owner** — [[systems-designer]] on Emory's go-ahead; `.github/` is outside this seat's
  paths.

### F3 · Three non-canonical cloud-run branches still on origin

- **State** — `origin/claude/sweet-mccarthy-8mouy6` (07-30), `-i95s3k` (07-31) and `-d5kgmw`
  (08-01) each carry a complete parallel council record for a date `main` also has a record
  for. They are **not** orphaned by accident: `analytics/daily-research/2026-08-01.md:452`
  rules them "preserved verbatim … as a non-canonical parallel artifact", on the ground that
  they ran `claude-sonnet-4-6` in seats assigned other models. Their one substantive lead was
  queued through canonical vetting rather than adopted.
- **Recorded** — `4d5c562`, rulings (a) and (b) and escalation item 2 (`:487`).
- **Next** — The close-out's own recommendation, unactioned since 2026-08-01: archive or
  delete the branches so a parallel record cannot later be mistaken for canon. Every check of
  this kind has to re-derive their status from a ruling buried in one day's close-out, which
  is the cost of leaving them.
- **Owner** — **Emory.**

### F4 · Seventeen branches share no merge-base with `main`

- **State** — Found 2026-08-07 by running the orphan check over all 65 remote heads instead of
  the recent ones. Seventeen branches, dated 2026-06-22 through 2026-07-20, are neither ancestors
  of `origin/main` **nor** connected to it: `git merge-base origin/main
  origin/fix/notable-line-integrity` returns empty. `origin/main` has five root commits, the
  oldest 2026-07-22; that branch roots at `0460699` on 2026-06-08. The histories are disjoint.
- **What this does and does not mean** — ancestry cannot answer whether these branches hold work
  that never reached `main`, because there is no common point to diff against. Their file-level
  content may be entirely superseded, or may not be. **This thread asserts neither.** It exists
  so that a future orphan check does not re-derive the disjointness and mistake it for
  seventeen new orphans, and so the question is asked once by someone who can answer it.
- **The four genuine orphans are unchanged** and are F1 (17 operator ledger marks) and F3 (the
  three non-canonical cloud-run records).
- **Next** — A decision on whether the pre-rewrite branches are archival or live. If archival,
  delete or tag them so the orphan check stops returning twenty-one results where four are real.
- **Owner** — **Emory.**

---

## D · Vault threads

### D1 · Agent memory currency

- **State** — Audited 2026-07-31 against `.claude/agents/`, `src/models.py`, the prompts each
  note cites, and `views/isds-workflow-3d/workflow.json`. Definitions themselves are
  unchanged since the registry was built — `git log ede0f32..e153ce3 -- .claude/agents/
  prompts/` returns no commits. Five notes claimed their seat had no flowchart box and all
  five were wrong after v3.0; the adopted method rules existed only in the daily records.
  Both fixed.
- **Recorded** — [[obsidian-archivist]], audit slice 2026-07-31.
- **2026-08-04 update** — The 07-31 work was orphaned off `main` for three days and recovered
  by PR #44 (`cb12a2d`); the council, not this seat, caught it (`4d5c562`). The 2026-08-03
  change set then repeated the failure in a subtler form: its own note landed, and three of
  its claims about other notes did not. Corrected 2026-08-04, with the measured consequence
  recorded rather than asserted. The countermeasure adopted: a vault change is not made until
  it is on `main`, and the session claiming it verifies it there.
- **2026-08-08 update — the countermeasure worked, and it was aimed at the wrong failure.**
  The currency query did its job: `git log 373cce6..HEAD -- .claude/agents/ prompts/` is
  **empty**, `git status` shows nothing modified under either path, so **no definition or
  prompt changed on 08-07 or 08-08** and every seat note's model and binding is current. But
  three seat notes were still wrong about the repository, and none of the errors was of a kind
  the query can see:
  - [[systems-designer]] said its flowchart box sat at **machine row 7**. It has been at row 9
    since manifest v2.2, dated 2026-08-03; [[Agent Registry]] recorded the move on 2026-08-04
    and the seat note did not. **The registry and the seat note disagreed about where the seat
    sits for four days**, and the maintenance rule that is supposed to prevent exactly that
    ("the table and the corresponding note change in the same commit") only binds when a
    *definition* changes — the manifest is not a definition.
  - The same note bound the seat to a **zero-cost constraint** that the seat's own code
    reading disproved on 2026-08-08.
  - [[Claim Map]] carried **C13 as an open definitional split for two days after the council
    ruled**, and carried it under a heading that invited a reader to think the question was
    still live.
  **The corrected statement of this thread:** the risk is no longer "seat notes lag the
  definitions". It is **"vault notes lag the tree"** — the manifest, the code, the archive —
  and a query scoped to `.claude/agents/ prompts/` cannot detect it by construction.
- **Next** — Keep the currency query, and add a second query that the 2026-08-08 pass had to
  improvise: for each seat note, re-read the **non-definition** artifacts it asserts facts
  about — the manifest row, the guard it claims exists, the constraint it claims to be bound
  by. Concretely, per session: `views/isds-workflow-3d/workflow.json` rows against every
  "Place in the workflow" section, and one grep for each operating constraint a note names.
  All twelve notes carry a snapshot anchor; that remains necessary and is not sufficient.
- **Owner** — [[obsidian-archivist]].

- **2026-08-07 update — the failure recurred, in the form the countermeasure does not reach.**
  Nothing was orphaned this time: every council branch in the window landed, and the archivist's
  own 08-04 and 08-05 work is on `main`. What failed is the *other* half. Between 2026-08-05 and
  2026-08-07 the council adopted fourteen rules, and `grep -c "2026-08-0[567]" agents/*.md`
  returned **0** for all nine seat notes bar `systems-designer.md`. The cost is C11: the integrity
  officer read a stale count in the taxonomy's canonical home and gave two patterns the same
  number. **"A vault change is not made until it is on `main`" does not bind a vault change that
  was never written.** All fourteen rules landed 2026-08-07.
- **Next** — Two, and the first is now mechanical rather than a habit. (1) B5 — extend
  `scripts/check_currency.py` to the nine seat notes and wire it into CI, so "the seat notes are
  current" stops being a claim a session makes about itself. (2) Until then, each session's first
  act stays the currency query: `git log <anchor>..HEAD -- <paths>`, plus
  `grep -c "2026-08-0[0-9]" agents/*.md` against the dates of every council session since the
  last deployment.
- **Owner** — [[obsidian-archivist]]; B5 is [[systems-designer]]'s.

---

### D3 · `STATE_OF_THE_ANSWER.md` fails the currency guard, and today made it worse — **OPENED 2026-08-08, CLOSED 2026-08-09**

> **CLOSED on a re-run of the guard, by the seat that owns the file.** Both defects are gone.
> `STATE_OF_THE_ANSWER.md:10` now reads "**Last updated: 2026-08-09** — audited against
> `2686422` plus the uncommitted 2026-08-08/09 working-tree changes (manifest:
> `analytics/session-manifest-2026-08-09.md`)", so the file carries an anchor for the first
> time *and* its timestamp matches its content. `scripts/check_currency.py`, re-run by this
> seat, reports **9 currency claims across 5 notes, 0 failed**, exit 0 — down from 1 failure at
> the close of 08-08 and 5 at that session's start.
>
> **Two things worth keeping from how this closed.** First, the fix came from
> [[research-analyst]], the seat that owns the file, exactly as the thread routed it — the
> archivist's refusal to silently restamp another seat's living memory was the right call and
> cost one day. Second, the anchor the analyst wrote **says what an anchor can and cannot
> prove**: "The anchor records what state this file was checked against; it does not by itself
> prove the content above it accurate." That sentence is the honest form of the snapshot-anchor
> convention this vault adopted on 2026-08-03, and it belongs in the convention rather than in
> one file.

*The original 2026-08-08 entry follows, unaltered.*


- **State** — `scripts/check_currency.py` run against the working tree reports **8 currency
  claims checked, 1 failed**, and the one is `STATE_OF_THE_ANSWER.md`: *no `audited against
  <sha>` anchor*. Down from three failures at the start of this session — [[Claim Map]] and
  [[Project Change Log]] were both STALE and are now anchored — and down from the five the
  day's handoff recorded. **Two distinct defects in this one file, and the second is new
  today.** (1) It carries no anchor at all, so it claims currency against nothing; this
  predates today. (2) `STATE_OF_THE_ANSWER.md:10` reads "**Last updated: 2026-08-06**" while
  `:5` was materially edited on **2026-08-08** — the Kim police-powers correction and the
  third-stance correction. **A living-memory file whose own timestamp is two days behind its
  own content is the exact failure this vault exists to prevent**, and it was introduced by an
  otherwise careful correction pass.
- **Recorded** — `scripts/check_currency.py` output, 2026-08-08; `STATE_OF_THE_ANSWER.md:5`
  and `:10` (uncommitted, `fix/restore-council-label`); `git diff STATE_OF_THE_ANSWER.md`.
- **Next** — Restamp `:10` to 2026-08-08 and add an `Audited against <sha>` anchor with the
  paths the file claims to describe. **Deliberately not done by this seat:** the file is
  [[research-analyst]]'s canonical living memory, it was being edited during this session, and
  an archivist silently restamping another seat's record would assert a currency this seat did
  not establish. Escalated instead.
- **Owner** — [[research-analyst]].

---

### D4 · A clause in `STATE_OF_THE_ANSWER.md` that is true only while a list stays short — **OPENED 2026-08-09**

- **State** — **Not a defect today; a scheduled one.** `STATE_OF_THE_ANSWER.md:28` reasons from
  Kim's footnote-23 remedy mismatch to the distribution the record shows: "every disclosure case
  in the Kim memo's bibliography (InterMune, T-73/13 R; AbbVie, T-44/13; PTC Therapeutics,
  C-175/18 P; **Vanda, D.D.C.**) was **brought in a court to prevent or restrict disclosure**,
  not in arbitration to be compensated for it." **As scoped to those four, it holds.** But the
  project also holds the **Vanda Court of Federal Claims takings matter** (No. 23-629C, both
  slip opinions retrieved into `seeds/`), and a CFC takings action is **not** a suit to prevent
  disclosure — it seeks compensation after the fact, which is the very posture the sentence
  contrasts against. Add that matter to the list and the sentence becomes false *by the
  addition*, not by any edit to it.
- **Why it is recorded rather than fixed** — the clause is correct as written, the file is
  [[research-analyst]]'s canonical living memory, and an archivist rewording a true sentence in
  another seat's file to pre-empt a hypothetical is exactly the overreach this register exists
  to avoid. It is also a genuinely interesting point on the merits: a Vanda CFC row would be
  *evidence against* the remedy-mismatch explanation's strongest form, so whoever adds it
  should expect to rewrite the inference, not just the parenthesis.
- **Recorded** — `STATE_OF_THE_ANSWER.md:28`; the retrieved opinions at
  `seeds/Vanda_v_US_23-629C_FedCl_2024-01-18_slip_op.pdf` and `…_2025-01-22_slip_op.pdf`;
  observation raised by [[research-analyst]] during the 2026-08-09 parity round.
- **Next** — When (and only when) the CFC takings matter is added to that list, reword the
  clause and re-examine the inference it supports. No action until then.
- **Owner** — [[research-analyst]].

### D5 · Adopted method rules are recorded where the seat that must obey them never reads

- **State** — Opened 2026-08-13. Every seat note carries a section of rules the council adopted
  in session and marked **binding** — `agents/research-analyst.md:59-142` ("Adopted method
  rules (session-derived, binding)", eleven rules), `agents/council-chairman.md:46-133`
  ("Adopted session protocol (session-derived, binding)"),
  `agents/analytics-officer.md:40-62` ("Standing observations"). A seat's actual read path is
  its definition in `.claude/agents/` plus the `prompts/` files that definition enumerates.
  **Eight of the nine definitions never name the seat's own vault note**, so those rules sit
  outside the context of the agent bound by them.
- **Measured, not assumed.** Each of the analyst's eleven rules was grepped against its full
  read path (`.claude/agents/research-analyst.md`, `prompts/research_analyst.txt`,
  `prompts/council_calibration.md`, `prompts/carrying_span_rule.md`). Only **the carrying-span
  rule** is present — and it is present because the council gave it its own prompt file. Absent
  from the read path: *fetch-first*, *docket page before document hunt*, the four *relay method
  rules*, *no search-synthesis figures*, *a mis-anchored row is not a null*, *`find_matched` has
  three states*, *a deliberately false URL is a control*, and *every citation to a relay
  reduction carries its sha*. (Bare-word matches on "docket" in the prompt files are the
  ordinary noun, not the rule.)
- **This is the generalisation of a failure already recorded twice.** [[integrity-officer]] is
  the one seat whose definition does point at its vault note, and
  `.claude/agents/integrity-officer.md:56-62` says why in its own words: "an enumeration here
  goes stale silently … council R8 found this definition still naming five patterns while the
  vault's taxonomy stood at ten." **C11** in this note records the same defect from the other
  direction — a stale vault table caused two different patterns to be adopted as entry 27. The
  fix was applied to one seat and never generalised to the other eight.
- **The 2026-08-03 holdout failure fits the pattern exactly.** The analyst asserted a case was
  new to the project when it is one of the four out-of-sample holdout positives
  (`scripts/holdout_set.json`: `loewen_v_us`, `mondev_v_us`, `apotex_v_us`, `pm_v_uruguay`,
  the four rows with `label: 1` among twenty). Grepping `holdout|hold-out|out-of-sample` across
  the analyst's entire read path returns **nothing**. The set is documented in `METHODOLOGY.md`,
  in this note, and in six analytics files — none of them in the analyst's context. The seat was
  not careless about a fact it held; it never held the fact.
- **Not fixed here.** Editing `.claude/agents/` is a contract change and is **Emory's** — the
  same boundary that has held `systems-designer.md:17`'s "zero-cost" line open since 2026-08-08.
  The one-line remedy per seat is the sentence the integrity officer's definition already
  carries, pointed at each seat's own note.
- **Next** — Emory adds that pointer to the eight definitions that lack it, or rules that the
  adopted-rules sections should live in `prompts/` instead. Either resolves it; leaving both
  copies unlinked does not.
- **Owner** — **Emory**, with [[council-chairman]] on whether adopted rules belong in `prompts/`.
- **Re-tested 2026-08-16 against `d997c32` — unchanged, three days on.** `git log 8ea2ee1..HEAD
  -- .claude/agents/ prompts/ src/models.py` returns **no commit**. Scripted the check this time
  rather than reading: for each of the nine definitions, does it name its own vault note either
  as `agents/<seat>.md` or as a `[[<seat>]]` wikilink? **Eight NO, one YES** — the YES remains
  [[integrity-officer]]. Identical result, now re-runnable.

---

### D6 · The model a seat runs on is not the model any file in the repository names

- **State** — Opened 2026-08-16. All nine definitions declare `model: opus`. That frontmatter key
  selects a **tier, not a version**, and `scripts/check_models.py`'s own docstring says so: "a
  card naming a version is describing a choice the frontmatter does not itself pin." The runtime
  resolves the alias to the platform's current Opus. The five seats documented as **Claude Opus
  4.8** — `systems-researcher`, `editor`, `analytics-officer`, `obsidian-archivist`,
  `integrity-officer` — are therefore pinned to 4.8 by **nothing**: not the definition, not
  `src/models.py`, not the flowchart card.
- **Observed from two seats, not inferred.** [[integrity-officer]] self-reported `REQUESTED
  claude-opus-4-8 → ACTUAL claude-opus-5`, unasked, on **2026-08-12**
  (`analytics/daily-research/2026-08-12.md:750`), **2026-08-14** (`:576`), **2026-08-15**
  (`:693`) and **2026-08-16** (`:731`). On **2026-08-16** [[obsidian-archivist]] queried its own
  session runtime and got `session_context.model` = `claude-opus-5`,
  `last_served_model` = `claude-opus-5`, against a note pinning `claude-opus-4-8`. Two seats,
  same result: the anomaly is structural, not particular to the officer.
- **Every mechanism built to surface this is on a path no seat enters.** `src/models.py:18`
  requires that a runtime substitution be recorded in `HANDOFF.md` via `record_fallback()`.
  That function's **only** caller is `src/research_brief.py:161`. `grep -n "Model runtime
  fallbacks" HANDOFF.md` returns nothing — the section has never been written. Meanwhile
  `scripts/check_models.py` exits **0**, correctly: it compares three declarations to one
  another and has no view of a runtime, which its docstring states plainly.
- **The vault's own failure, recorded against itself.** On 2026-08-13 this seat wrote "**No
  model drift exists**", citing that exit 0. The integrity officer's first report was dated
  2026-08-12 and sat in `analytics/daily-research/`, a directory the same session read. A guard's
  exit 0 was allowed to stand in for a fact the guard does not test.
- **Fixed here** — [[Agent Registry]] carries a qualification block under the roster;
  [[obsidian-archivist]] and [[integrity-officer]] carry the observation at their Model blocks.
  The roster rows and Model lines are **left unchanged**: they state the operator's directive,
  and rewriting them to "Claude Opus 5" would silently ratify a substitution nobody authorised.
- **Next** — Emory decides which is true, then one of two things happens: the definitions and
  cards are corrected to Opus 5, or the definitions pin `claude-opus-4-8` explicitly so the
  directive binds. Separately, `record_fallback()` needs a caller on the council path, or
  `check_models.py` needs a companion that reads a runtime.
- **Owner** — **Emory** for the contract decision (`.claude/agents/`, `src/models.py`);
  [[systems-designer]] for the `record_fallback()` wiring and the `workflow.json` cards.

---

### C17 · `check_currency.py` flags every landed archivist session as drift against itself

- **State** — Opened 2026-08-16, immediately after the 2026-08-16 session merged as `5138312`.
  The guard went from **1 failed to 3** on that merge, and the two new failures are
  [[Project Change Log]] and this note, each reported stale *against the very commit that
  wrote them*. This is a false positive, and it has now happened twice unnoticed.
- **The guard already anticipated the problem; the fix is narrower than its own rationale.**
  `scripts/check_currency.py:93-105` (`_is_maintenance`) excludes a commit "whose every changed
  file is itself a tracked note", and its docstring gives exactly the right reason: "anchors live
  inside the notes they date, so the commit that moves an anchor always touches a tracked note —
  counted naively, no fully committed tree can ever pass this guard." But the implementation
  tests `files <= set(TRACKED)`, and `TRACKED` holds only the four index notes plus
  `STATE_OF_THE_ANSWER.md`.
- **A real archivist session commit can never satisfy that.** By design it also writes its
  session record under `analytics/vault-sessions/`, the per-seat notes it corrected, and
  `HANDOFF.md` — none of them tracked. Measured on both cycles:

  | Session commit | Files touched | In `TRACKED` | Exemption fires? |
  |---|---|---|---|
  | `5138312` (2026-08-16) | 8 | 4 | **no** — `HANDOFF.md`, 2 seat notes, session record |
  | `67c80f7` (2026-08-13) | 7 | 3 | **no** — `HANDOFF.md`, 2 seat notes, session record |

- **Why it matters more than a cosmetic count.** The 2026-08-13 run of this guard showed
  `agents/Project Change Log.md ... since 8ea2ee1 / 67c80f7 vault: archivist session 2026-08-13`
  and that line was read as ordinary staleness and restamped, rather than as the guard misfiring.
  A guard that cries drift on its own maintenance trains its only reader to skim it — which is
  the failure this guard was built to prevent, arriving through the front door.
- **Not fixed here.** `scripts/` is outside this seat's merge authority. The anchors are
  deliberately **not** restamped to the merge commit: an anchor must name the commit the audit
  was performed against, and `5138312` did not exist when the audit ran. Restamping to hide a
  false positive would be the more serious defect.
- **Next** — [[systems-designer]] widens the exemption to match its own stated rationale: treat a
  commit as maintenance when every changed file is a vault record surface
  (`agents/`, `analytics/vault-sessions/`, `moc/`, `HANDOFF.md`), not merely one of the five
  tracked notes. A commit touching any substantive path still counts, which preserves the guard.
- **Owner** — [[systems-designer]]; **Emory** to confirm the widened set is the right one.

---

## E · Explicitly zero budget

Recorded so that "not worked on" is never mistaken for "forgotten". Each was given zero
search budget by the chairman's agenda and honored.

| Item | Disposition | Recorded |
|---|---|---|
| Wingtech / Nexperia ICSID registration | Downgraded to **monthly** on 2026-07-28 (Day 104, no registration in a 104-day window); next check late August | `state/research_log.json` open thread 1 |
| Roberts / EJIL:Talk monitored-author check | **Subsumed** by the chairman's 2026-07-30 Part 6 ruling; zero budget | `f03a90e` |
| IISD ITN / EJIL:Talk polling | Zero budget | `f03a90e` |
| `sps.pdf` two-paths question | **CLOSED** — access artifact, resolved; prior 403s were CDN user-agent gating, origin reports 404, hypothesis retired unfounded | Ruling B4, `f03a90e` |
| `china-france-bit-2007-protocol-exhaustion` | **RETIRED** — resolved at provision level; 23-session escalation ended | `f03a90e` |
| `huawei-arb-22-2-rules-vintage` | **NOT OPENED** — substantially answered in vetting (Rule 37(2) on-page evidence) | `f03a90e` |
| Escalated gaps generally | Zero search budget by standing rule; they are Emory's manual action items | `prompts/council_chairman.txt` |

---

## Maintenance

This note is rewritten from the record, never edited from memory. It is refreshed when the
council's close-out changes a thread's state — which means the close-out, not this note, is
the source of truth, and a disagreement between them is a defect in this note.

## Change log

- **2026-08-17 (source-outage repair)** — audited against `df3a8ef`; the drift since
  `d997c32` is sixteen council-session and fetch-relay commits touching analytics and
  agents. New thread: the retired Google Alerts queries need per-alert Talkwalker
  replacements (owner: operator). The italaw access path is NOT-READ (403) pending a
  relay decision (owner: council/systems-designer).
- **2026-08-16** — Refreshed against `d997c32` (`main`, clean tree) on a complete **621-commit**
  history; the container's clone arrived shallow at 201 commits and every ancestry result below
  was derived after `git fetch --unshallow`. **One thread opened, three re-measured, none
  closed.** **D6** is new and is this session's finding: the five seats documented as Claude
  Opus 4.8 are pinned to 4.8 by no file in the repository, because `model: opus` selects a tier
  rather than a version — observed from two seats, [[integrity-officer]] four times unasked
  (2026-08-12, 08-14, 08-15, 08-16) and [[obsidian-archivist]] first-person on 2026-08-16.
  **F1** is re-measured at **day twenty** with the same three blob counts, and now carries the
  warning that the shallow clone misreported the ledger's last-touching commit as `cf7d99b`
  when it is `8891c21`. **D5** is re-tested three days on and is unchanged — eight of nine
  definitions, this time by a scripted check rather than by reading. **C12**'s arithmetic
  re-derived: `build_graph.py --dry-run` now plans **27** notes, of which **3** lie outside the
  archivist's merge set (`BOUNDED_CHANGE_PROTOCOL.md`, `prompts/carrying_span_rule.md`,
  `lit-review/BIBLIOGRAPHY_TEMPLATE.md`) — unchanged from 2026-08-13. Orphan check found **no
  new** stranded work and confirmed all three prior `vault/*` branches are ancestors of `main`.
  *Audited against `d997c32`; paths: `analytics/verification_ledger.jsonl`,
  `analytics/daily-research/`, `analytics/council-log.md`, `.claude/agents/`, `agents/`,
  `prompts/`, `scripts/`, `src/models.py`, `views/isds-workflow-3d/workflow.json`,
  `HANDOFF.md`, and every remote branch tip.*
- **2026-08-13** — Refreshed against `8ea2ee1` (`main`, clean tree) on a complete history.
  **One change-log entry retracted, two threads re-measured, one thread opened.** The
  2026-08-11 claim that F1's marks reached `main` is **struck as false** — `0a67756` did not
  touch `analytics/verification_ledger.jsonl`, whose blob on `main` is still `f3dbbf6` from
  `8891c21` (2026-07-27). **F1** gains the counts from both blobs (21 marks on `main` vs 38 on
  the branch) and a demonstration through `verify.replay` that its three stranded claim ids
  resolve `unverified` against `main`. **F2** is re-tested after `git fetch --unshallow` and the
  loss is confirmed against the full 584-commit history rather than a truncated one. **D5** is
  new: adopted method rules are recorded in seat notes that eight of the nine definitions never
  tell the seat to read, which is the pattern behind the 2026-08-03 holdout failure. Snapshot
  block records the clean-clone test caveat and the `--is-ancestor` vs `git cherry` correction.
  *Audited against `8ea2ee1`; paths: `analytics/verification_ledger.jsonl`, `.claude/agents/`,
  `agents/`, `prompts/`, `scripts/`, `src/`, `.github/workflows/`,
  `views/isds-workflow-3d/workflow.json`, `HANDOFF.md`.*
- **2026-08-11** — Integration to `main`: audited against `0a67756` — the merge of the
  integration branch (which carries the formerly uncommitted 2026-08-08/09 work the entry
  below describes) with the 2026-08-11 council session, plus the fetch-relay results the
  cron committed onto the integration branch itself mid-flight. The drift counted since `2686422`
  is the council's own 2026-08-08..11 session and ledger commits plus the integration's
  reviewable commits; no thread moved outside them. ~~F1's seventeen verification marks
  reach `main` with this merge; the thread closes on the operator's confirmation, not on
  the merge itself.~~ — **false, corrected 2026-08-13.** The marks did not reach `main`
  with that merge or any other. `git show --stat 0a67756 -- analytics/verification_ledger.jsonl`
  is **empty**: the integration did not touch the ledger. The file on `main` is still
  blob `f3dbbf6`, last written by `8891c21` on **2026-07-27**, and
  `git merge-base --is-ancestor origin/chore/operator-marks-2026-07-27 origin/main` still
  fails. The line is struck rather than deleted so the correction stays legible, per this
  note's own convention. See F1.
- **2026-08-09** — Refreshed against `2686422` plus the uncommitted working trees of the
  2026-08-08 repair session and the 2026-08-09 audit-response session, on
  `fix/restore-council-label`. **Two threads closed, one rewritten, two opened, three
  materially restated.** Closed: **B8** (the guards are in
  `.github/workflows/pipeline-guards.yml`, with planted-violation tests the thread never asked
  for) and **D3** (`check_currency` green, 9 claims / 0 failed, fixed by the seat that owns the
  file). Rewritten: **B6**, because D/E, F and G are built rather than designed and the thread's
  job inverted — it now records that *built is not on*, and names the one piece that genuinely
  is not built (the tail-audit stub, `TAIL_AUDIT_N = 0`). Opened: **B9**
  (`check_site_sync.py` rebuilds `docs/` in place — a mutating command named as a check, which
  is how it reverted `docs/` this session) and **D4** (a true clause in
  `STATE_OF_THE_ANSWER.md:28` that a future list addition would falsify). Restated: **B5**,
  **B7**, **C11**, **C12**.
  **The finding of this pass is a thread that did not close.** B5 / [[Claim Map]] **C15** was
  briefed as resolved; five of eight statements are repaired and **three are not**, one of them
  having moved from `src/main.py:497-500` to `:687-690` so that only its quoted text located it.
  Worse, the same session's second gate (`VALIDATION_STATUS_ONLY`) made four of the five repairs
  stale in the opposite direction — items at or above 40 are now held, and every repaired
  sentence says they publish. That successor divergence is the new [[Claim Map]] **C16**, and
  `METHODOLOGY.md` again contradicts itself twenty lines apart. **A repair pass that is not
  checked against the same session's other changes reintroduces the defect it closed.**
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `src/`, `scripts/`, `tests/`, `prompts/`, `.github/workflows/`, `analytics/`, `seeds/`,
  `working/`, `views/isds-workflow-3d/workflow.json`, `fingerprint.yaml`, `HANDOFF.md`,
  `METHODOLOGY.md`, `README.md`, `PLAN.md`, `STATE_OF_THE_ANSWER.md`, `agents/`, `moc/`.*
- **2026-08-08** — Refreshed against `2686422` plus the uncommitted working tree of the
  master-prompt repair session on `fix/restore-council-label`. **Eight threads added, none
  closed, one rewritten.** Added: **B5** (the eight prose statements the fill suspension left
  behind — the sharpest live divergence in the project, and the only new *defect* of the day);
  **B6** (D/E, F, G designed and expressly not production); **B7** (the locked set, empty by
  design); **B8** (three fail-closed guards, none wired to CI); **C11**–**C14** (Emory's four
  decisions, one of which — C12 — expires at the Monday 13:00 UTC cron). Rewritten: **D1**,
  because the drift it tracks turned out not to be the drift it was written for. **Nothing was
  closed on the strength of a session report**: the one item the day's handoff listed as open
  and routed — the `digest.html.j2:120` overclaim — was re-read in the file, found already
  repaired, and recorded closed in [[site-experience]] on the file's authority rather than the
  report's.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `src/`, `scripts/`, `analytics/`, `templates/`, `views/isds-workflow-3d/workflow.json`,
  `fingerprint.yaml`, `HANDOFF.md`, `METHODOLOGY.md`, `README.md`, `.claude/agents/`,
  `prompts/`, `agents/`.*

- **2026-08-07** — Four threads added and one updated, all from the archivist's every-3-days
  session. **B5** — `scripts/check_currency.py` tracks 5 of 13 anchored notes and is wired into no
  workflow. **C11** — taxonomy entry 27 adopted twice for two patterns, caused by a stale count in
  the vault file the integrity officer is directed to read. **C12** — `build_graph` is whole-vault
  and four of its seven pending files sit outside the archivist's merge authority, which is why
  that run has never happened. **F4** — seventeen remote branches share no merge-base with `main`
  and cannot be assessed by ancestry. **D1** updated: nothing was orphaned in this window, and the
  failure took the other form — fourteen adopted rules never written into the seat notes.
  F1 and F3 re-verified open and unchanged; A8 confirmed on `main`, discharging the chairman's
  2026-08-06 warning that it existed only off it.
  *Audited against `7c08dcf`; paths: `analytics/`, `agents/`, `.claude/agents/`, `prompts/`,
  `scripts/check_currency.py`, `scripts/build_graph.py`, `.github/workflows/`, and every remote
  branch tip.*
- **2026-08-04** — Refreshed against `b76f6c3`. B1 closed — the source-health guard ran live
  on 2026-08-03 and `state/source_health.json` exists — with two dated successor defects
  recorded from the systems seat's escalations and verified against `src/source_health.py`.
  C9 closed: `984f5eb` is on `main` and no PR is open. C7 and C8 re-verified open against the
  manifest and `scripts/build_graph.py`. Section **F** added for branch hygiene, carrying the
  three findings of this session's orphan check: 17 unmerged operator ledger marks (F1), the
  lost standing-rules record (F2), and the three ruled-non-canonical cloud branches whose
  archival was recommended on 2026-08-01 and never done (F3). The A- and C-series are carried
  from the council's own close-outs and not re-argued here.
  *Audited against `b76f6c3`; paths: `analytics/`, `state/source_health.json`,
  `src/source_health.py`, `views/isds-workflow-3d/workflow.json`, `HANDOFF.md`, `alerts.yaml`,
  and every remote branch tip.*
- **2026-07-31** — Note created by operator directive: linearize the vault's threads, all
  threads included. Every chain verified against the repository before writing. Two
  corrections to the brief that produced it: the silent-decay guard reached main through
  PR #23 (`8178f1f`), not PR #32; and "Talkwalker URLs" is sourceable to `alerts.yaml`
  rather than to any council escalation, so it is recorded with that provenance. Six threads
  not named in the brief were found open in the record and added: A2, A7, B3, C6, C7, C9,
  D1. One more (C8) was found by running `scripts/build_graph.py` during this pass rather
  than by reading the record — it is a live defect, not a documented one.

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
