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

**Snapshot taken:** 2026-07-31, at `e153ce3` (merge of PR #32) plus the open PR #33
(`984f5eb`). Sources read for this pass: `state/research_log.json` (seq 36),
`analytics/daily-research/2026-07-31.md`, `analytics/optimization-log.md`, `alerts.yaml`,
`digests/2026-07-27_ISDS-Thematic-Watch/meta.json`, `.github/workflows/weekly.yml`.

---

## A · Research threads — the analyst leads

### A1 · A/81/17 publication window

- **State** — Not indexed as of 2026-07-31; the one-query daily check returned only A/80/17
  (58th session) and general UNCITRAL pages. The publication window **opens 2026-08-01**. On
  publication it is the immediate lead, and three questions ride on it: the adopted
  Supplementary Provision numbering, the TPF SP10/SP11 inconsistency, and whether DP 19's
  ex officio dismissal power survived.
- **Recorded** — `analytics/daily-research/2026-07-31.md` Task 3 and Next Step 1 (`f03a90e`);
  `state/research_log.json` open thread 3.
- **Next** — Continue the one-query daily check; escalate to lead status on publication.
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

- **State** — Opened 2026-07-31 as an ordinary gap. The fork-in-the-road vs. no-U-turn
  characterization for the China–Switzerland BIT (2009) is missing, and it is the piece
  needed to complete the three-way treaty-selection comparison. Marker:
  `GAP-UNRESOLVED: china-switzerland-forum-relationship`.
- **Recorded** — Gap-marker dispositions in the 2026-07-31 close-out (`f03a90e`).
- **Next** — One bounded search-track attempt when budget allows. If inaccessible, it becomes
  a candidate for the July 23 operator IIA-mapping protocol — **not yet an escalation**.
- **Owner** — [[research-analyst]]; may route to Emory only if the bounded attempt fails.

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
- **Next** — **First live run 2026-08-03**, the next weekly cron
  (`.github/workflows/weekly.yml`, `cron: "0 13 * * 1"`). The output to read is the
  `source_health` block in that run's `meta.json`.
- **Owner** — Automatic; [[analytics-officer]] reads the result into the council's numbers of
  record.

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

### C7 · Two flowchart cards assert a model no config file carries

- **State** — Raised by this seat 2026-07-31. The `systems-designer` and `site-experience`
  cards in `views/isds-workflow-3d/workflow.json` read "Model: Claude Fable 5", while neither
  definition declares a `model:` key and `src/models.py` covers only the pipeline's LLM
  stages. The chart states an assignment nothing configures.
- **Recorded** — [[systems-designer]], [[site-experience]], [[Agent Registry]], and the Open
  drift section of [[Project Change Log]].
- **Next** — Either add `model: fable` to both definitions, or change the cards to read
  "inherits the invoking session". The chart is regenerated from its manifest, never
  hand-edited to hide the discrepancy.
- **Owner** — **Emory** decides; [[systems-designer]] regenerates.

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

### C9 · PR #33 — METHODOLOGY Parts III and VIII

- **State** — Open, one commit, not merged. Part III's live-source list gains the PCA press
  page and Bing News; Part VIII is rewritten from "predetermined stages" to the real agent
  council — named models, a chairman who directs but never writes, and a security officer
  whose objections bind the editor. It is the first professor-facing surface to describe the
  council as it actually runs.
- **Recorded** — `984f5eb`, branch `feat/methodology-source-council-sync`.
- **Next** — Review and merge.
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
- **Next** — Next deployment audits a different slice. Standing rule: when any agent's
  prompt, model, or contract changes, its note and [[Agent Registry]] change in the same
  change set.
- **Owner** — [[obsidian-archivist]].

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
