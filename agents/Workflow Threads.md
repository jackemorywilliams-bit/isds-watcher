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

**Snapshot taken:** 2026-08-04, at `b76f6c3` (merge of PR #49). Sources read for this pass:
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
- **Next** — Add the nine seat notes to `TRACKED` with their declared paths, and wire the script
  into a workflow beside `model-consistency.yml`.
- **Owner** — [[systems-designer]] on Emory's go-ahead; `scripts/` and `.github/` are outside the
  archivist's paths.

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
- **Next** — Emory's call, and no agent should make it: `git merge origin/chore/operator-marks-2026-07-27`
  on a branch, or re-run the marks. The ledger is operator-owned and this seat does not write
  to it.
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
