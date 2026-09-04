---
aliases: [Research Analyst]
tags: [agent, council]
hub: Council
---
# Research Analyst

**Role.** Interprets each session's screened items against the three-ring research
question, advances the carried open threads with strictly bounded web research, and
proposes evidence-cited candidate claims that only the operator's ledger may promote to
asserted fact.

**Definition.** `.claude/agents/research-analyst.md`

**Model.** `claude-opus-5` — `HEAVY_MODEL` in `src/models.py`; declared `model: opus` in
the definition; mirrored in `HANDOFF.md` and on the flowchart's `analyst` card ("Model:
Claude Opus 5"). Promoted from `claude-opus-4-8` by operator directive 2026-07-29
(commit `4f8f981`), on the ground that "the researcher requires the most thinking and the
most advanced capabilities available."

## Canonical training (binding)

1. `prompts/research_analyst.txt` — the full contract: interpret rather than list; advance
   the carried threads; bounded web search that builds on the daily researcher's notes;
   backsourcing from titles; the `candidate_claims` JSON contract; `GAP-UNRESOLVED` markers
   with stable slugs; the monitored-author standing check (Anthea Roberts); the cross-BIT
   consistency rule across the four in-scope China BITs.
2. [[council_calibration]] (`prompts/council_calibration.md`) — the anti-fabrication
   checklist in full.
3. `prompts/carrying_span_rule.md` — **the Carrying-Span Rule**,
   adopted by the council 2026-08-03 as amended, added to this seat's definition on
   2026-08-04. It binds every source this seat cites for a proposition, *including sources
   it supplies itself*, and — per R7 — its own returns and the daily research records, not
   only the memos. Write the proposition before opening the source; screen the whole text
   with at least one **rigid designator**; quote the words that carry it, with a pinpoint;
   if nothing carries it, take the exits in order (another document in the same matter
   first, drop last) and name the one taken. It does **not** bind the structured
   `candidate_claims`, which the pre-ledger verification system governs.
4. The living memory embedded in the prompt — `STATE_OF_THE_ANSWER.md` plus the newest
   `analytics/insights.jsonl` entries — which is "the canonical baseline; never report it
   absent, never reconstruct it, never re-assert what it already records."

## Discipline highlights

- "a few well-chosen queries beat many" — web search "is NOT a general news channel and NOT
  a way to introduce unrelated material." (`prompts/research_analyst.txt`)
- BACKSOURCE FROM THE TITLE: a paywalled headline is a lead, and "never state the contents
  of a body you could not actually read."
- "A claim you cannot source you do not make; flag it as unverified." Every substantive
  claim carries an inline source (name + URL).
- Insights are uncapped but never padded: on a quiet day the honest output is "no new
  insight; standing watch" with a one-line note of what was checked; "a thin or absent
  nexus is reported honestly, never manufactured into a 'finding.'"
- It proposes only: "the operator-controlled verification ledger decides what may be
  asserted — you do not decide verification status, and any status you emit is ignored."
  Escalated gaps get zero search budget; absence is recorded as "not found in accessible
  sources", never as non-existence.

## Adopted method rules (session-derived, binding)

Rules the council adopted in session. They bind alongside the prompt contract, and they are
recorded here because they are now part of this seat's working context.

> **Audit finding, 2026-08-13 — this section is binding on a seat that is never told to read
> it, and that gap has already cost the project once.** This seat's read path is
> `.claude/agents/research-analyst.md` plus the three `prompts/` files that definition
> enumerates. It does **not** include this file. Each rule below was grepped against that full
> read path: only **the carrying-span rule** appears there, and only because the council gave it
> its own prompt file (`prompts/carrying_span_rule.md`). The other ten are recorded here and
> nowhere the seat reads.
>
> **Where this note would have prevented a recorded failure.** On 2026-08-03 this seat asserted
> that a case was new to the project when it is one of the four out-of-sample holdout positives
> validating the fingerprint — `scripts/holdout_set.json` carries twenty rows, four with
> `label: 1`: `loewen_v_us`, `mondev_v_us`, `apotex_v_us`, `pm_v_uruguay`. Grepping
> `holdout|hold-out|out-of-sample` across this seat's entire read path returns **nothing**. The
> holdout set is documented in `METHODOLOGY.md`, in [[Workflow Threads]] and in six analytics
> files — none of them in this seat's context. The seat did not forget a fact it held; the fact
> was never in front of it. Had the pointer existed, the four ids are one grep away.
>
> [[integrity-officer]] is the only seat whose definition points at its own vault note, and
> `.claude/agents/integrity-officer.md:56-62` states the reason in its own words: "an
> enumeration here goes stale silently." That remedy was applied to one seat and never
> generalised. Recorded as [[Workflow Threads]] **D5**; the fix is a contract edit and
> therefore **Emory's**, not this seat's and not the archivist's.
>
> **The same failure recurred on 2026-09-04, thirty-two days later, in seven instances — and it
> is now a named taxonomy entry. Archivist, 2026-09-04.** The 2026-08-03 failure above is one
> shape: *asserting something is new to the project when the project's own record already holds
> it.* On 2026-09-04 that shape fired **seven** times in a single day's record — four of them the
> chairman's, **the fourth committed inside the correction of the third** and self-filed
> (`0904-C1`), and **three self-reported by this seat**, the worst of them against
> `STATE_OF_THE_ANSWER.md:17` *on an author the previous analyst had recorded learning this exact
> rule on, the previous day* (`analytics/optimization-log.md:65`, `1fcc1ab`). The council adopted
> it as [[integrity-officer]] **fabrication taxonomy entry 28 — unscreened first-ness claim** —
> proposed at `analytics/daily-research/2026-09-04.md:968` (`51a2bae`), adopted at `:1148`
> (`687cfde`), landed at `e3d0255` — and routed it to the archivist for this vault, which is how
> it reaches this note.
>
> **Stated plainly, because it is the point rather than a coincidence.** 2026-08-03 and 2026-09-04
> are the same defect at two altitudes. In 2026-08-03 the record that would have refuted the claim
> (`scripts/holdout_set.json`) was outside the seat's read path. In 2026-09-04 the record that
> would have refuted each claim was inside the repository and simply **not queried** — the
> optimization log prices it exactly: the one screen that *was* run cost a single command and
> returned a better finding than the claim it refuted, while the four unscreened claims cost three
> blocking objections, two rewritten sections, and a gap disposition pointing the wrong way. The
> countermeasure is mechanical and this seat should carry it into every memo: **a first-ness claim
> states the literals tried, the synonyms tried, the file count, the scope and the commit, in the
> sentence that makes the claim.** The instrument is `wsgrep_at.py` at a base commit, validated
> against a known positive before its zero is trusted.
>
> **And the honest limit, which the council named itself:** this is a writing discipline, and it
> does not touch the structural cause — a corpus of **452 tracked files** and **36,683** non-blank
> daily-record lines growing roughly **750 lines a day** against a session-length context. No
> writing rule fixes that; it needs an index or a retrieval gate, which is a build and is
> **Emory's** (`analytics/optimization-log.md:65`). This note records the rule; it does not
> pretend the rule is sufficient.

- **Fetch-first** — adopted 2026-07-30. Attempt the direct fetch before reconstructing a
  document from search results; fall back to quoted-phrase reconstruction only once a fetch
  has actually failed. A search snippet is never cited in place of a document an unattempted
  fetch would have produced. Source: `analytics/daily-research/2026-07-30.md`, close-out
  next steps 2–3, committed in `754ce32`; re-sequenced from "substitute" to
  "fallback-after-attempted-fetch" by the systems researcher's correction in
  `analytics/optimization-log.md` (`e05f834`).
- **Docket page before document hunt** — adopted 2026-07-31, extending fetch-first. For any
  ICSID case question, fetch the case-detail page before searching for or guessing document
  URLs; hunt blob URLs only for documents the docket actually lists. Source: the session
  method note in `analytics/daily-research/2026-07-31.md`, committed in `f03a90e`. In
  practice it collapsed a planned four-attempt blob hunt into two fetches and answered three
  questions at once.
- **The carrying-span rule** — adopted 2026-08-03 in special session, and it binds this
  seat's own citations, not only the ones it reviews. Before opening a source, write the one
  sentence you are citing it for; screen the whole retrieved text for the proposition's
  operative terms including at least one rigid designator; then quote the **carrying span** —
  the source's own words that carry the proposition — into the entry, with a pinpoint. The
  load-bearing element is the carrying span, not the proposition-first step. Full adopted
  text: `analytics/council-sessions/2026-08-03-proposition-rule.md:1450` (R3, "final form"),
  committed in `56cbb75`. Recorded status in that same record: **adopted in text and
  unvalidated** — the session declined to record the rule as working against its own base
  rate (`:1617`, R8).
- **Relay method rules** — adopted 2026-08-04, binding on every seat, and this seat is the
  one that fires the batches. (1) Never choose as `find` a string the target page can
  generate from your own request URL — otherwise `find_matched` reports a property of the
  request. (2) Anchor on a neighbouring structural label and read the value out of the
  window. (3) State what makes a control negative before relying on it. (4) Treat a control
  block as uninterpreted until the positive control fires. Source:
  `analytics/daily-research/2026-08-04.md:761` (next steps, item 4), committed in `51bb7a2`.
  Rule (1) is this seat's own catch and was adopted into the integrity officer's taxonomy
  under the analyst's formulation as entry 23, *echoed-find / self-confirming query*.
- **No search-synthesis figures** — restated as a standing rule in the 2026-08-04 agenda: a
  search result set is evidence about an index, never about whether a document exists.
  Source: `analytics/daily-research/2026-08-04.md:50` (Task 3), committed in `8756859`.
Six more, adopted 2026-08-05 through 2026-08-07 and recorded here on 2026-08-07. Five of
them govern the relay, which is this seat's instrument:

- **`find` selects a position, not a proposition** — adopted 2026-08-05 as house rule 2, from
  this seat's own Part 2 §2.1. Request-echo and boilerplate-preemption are one defect with two
  faces. Before firing a row, answer: *is the first occurrence of this string in the
  tag-stripped body the occurrence I want?* Where the honest answer is "I cannot know", the row
  is written up as a **probe**, with what a miss would mean stated in advance. Source:
  `analytics/daily-research/2026-08-05.md:977`; `3ff5498`.
- **A mis-anchored row is not a null** — adopted 2026-08-05, house rule 4. A null says the page
  was asked and did not answer; a mis-anchored row says the question was never put. Recording
  the second as the first enters a false negative about a live source. Source:
  `analytics/daily-research/2026-08-05.md:979`; `3ff5498`.
- **A PDF row's `find_matched: false` is guaranteed by the content-type gate** and is never
  evidence of textual absence — demonstrated, not derived, at `2026-08-03-control.json`
  record 1. Adopted 2026-08-05, house rule 3; `3ff5498`.
- **A deliberately false URL is a control, not discovery** — adopted 2026-08-05, house rule 5.
  Source: `analytics/daily-research/2026-08-05.md:980`; `3ff5498`.
- **`find_matched` has three states, not two** — ruled 2026-08-07 on `0807-B5`: *found*,
  *looked and did not find*, and **asked nothing** (a row fired with `find: ""` records
  `false` having asked nothing). The third is not hypothetical — it is instantiated by the
  `978/zzz---zzz-bit-1900-` row, the single observation the whole 0804-B7 discharge rests on,
  and a future seat pooling on that field would read the discharge row as a null. Source:
  `analytics/daily-research/2026-08-07.md:1000`; `7adfd68`.
- **Every citation to a relay reduction carries the commit sha that holds it** — the integrity
  officer's taxonomy entry 25, adopted 2026-08-05 as house rule 1. A reduction is evidence; a
  path that can be rewritten is not a citation. Source:
  `analytics/daily-research/2026-08-05.md:976`; `3ff5498`.

Two council-wide rules adopted in the same window bind this seat and are stated in full in
[[council-chairman]]: **before acting on any instruction that names a file and a line, open
the line** (2026-08-07, extended from the chairman to every seat), and **a grep establishes
absence from the repository, never from the project** (2026-08-06). The first was adopted out
of `0807-B1`, which is against this seat: the memo quoted two formulations of the
identification caveat that no longer exist anywhere in `STATE_OF_THE_ANSWER.md`, carrying a
quotation forward without re-opening the file after the amendment its own predecessor had
procured. Candidate claim 4's `supporting_quote` was struck; its substance survives and must be
re-quoted against the current file before it enters any ledger.

- **Standing watch item.** Two consecutive sessions have paired this seat's strongest
  reasoning with the most binding objections, both times ledger-fidelity failures — reporting
  the favorable half of an operator mark (`quote_ok: true`) while omitting the adverse half
  (`scope_ok: false`). Named by the chairman as the seat's standing watch item in the
  2026-07-31 accountability record (`f03a90e`).

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `analyst` (council column). The daily-cadence counterpart box is
  `daily-researcher`, which runs the same substantive seat in the daily Claude Max routine.
- Fed by: `chairman` ("agenda passed to `_run_analyst`") and `daily-researcher`
  ("src/research_brief.py: `_daily_notes_block`").
- Feeds: `claim-gate` ("candidate_claims into integrity_gate"), `ledger` ("candidate_claims
  are recorded into the ledger as unverified claim_created events"), `citation-check`
  ("`_verify_citations` over the memo"), and `editor` ("`_run_editor` receives the analyst
  memo itself, alongside the gate note").

## Self-training mandate

"Track which query formulations actually produce findings (the 2026-07-26 lesson:
author-name+title beat keyword search) and record the session's method note; study one
primary award or doctrinal source in depth each week so your three-ring judgment keeps
sharpening beyond the seed corpus."

## Change log

- **2026-08-13** — **Read-path audit: this seat's binding adopted rules are not in its
  context.** Ten of the eleven rules in "Adopted method rules" appear nowhere in
  `.claude/agents/research-analyst.md`, `prompts/research_analyst.txt`,
  `prompts/council_calibration.md` or `prompts/carrying_span_rule.md`; only the carrying-span
  rule does, because it has its own prompt file. `scripts/holdout_set.json`'s four `label: 1`
  positives are likewise absent from the read path, which is the mechanism behind the
  2026-08-03 holdout assertion. Recorded as a block at the head of that section and as
  [[Workflow Threads]] **D5**; escalated to Emory as a contract edit. Nothing in this seat's
  rules was reworded — the finding is about where they live, not what they say.
  Separately, three of this seat's own 2026-07-27 operator marks carry `scope_ok: false` and are
  stranded on an unmerged branch (**F1**), so the adverse half of the seat's standing watch item
  is not visible to the gate on `main`.
  *Audited against `8ea2ee1`; paths: `.claude/agents/research-analyst.md`, `prompts/`,
  `scripts/holdout_set.json`, `analytics/verification_ledger.jsonl`.*
- **2026-08-09** — **The parity round: five audit contradictions closed, and the largest closed
  by going and reading the document.** Uncommitted, `fix/restore-council-label`; package
  `working/benavides-comment-replies-2026-08-08.md`.
  - **H&H v. Egypt (ICSID ARB/09/15) — CLOSED BY RETRIEVAL, and the retrieval changed the
    answer.** The Decision on Respondent's Objections to Jurisdiction of 5 June 2012
    (`ita1012.pdf`) and the Award's Rule 48(4) excerpts of 6 May 2014 (`italaw7979.pdf`) are in
    `seeds/`, with **21 spans verified**. Until this session the H&H propositions rested on **no
    primary text in the record at all**. The tribunal's own words now carry the approach
    (Award ¶¶ 364, 368), the outcome (¶ 385), the posture (Award ¶ 25 / Decision ¶ 80) and
    Ferguson's ¶ 42 pin. **Two claims were corrected rather than confirmed** — which is the
    argument for retrieval in one line: (1) the memo said the corruption, denial-of-justice and
    denial-of-effective-means claims all failed "for want of causal link"; that is the
    corruption claim only (¶ 399), denial of justice having failed on "manifestly unjust"
    (¶ 403); (2) the economic-sector attribution was **deleted**, not re-attributed a third
    time, and replaced with the document's own description of the dispute. The dead
    `italaw.com/cases/542` URL (404) was replaced with the real document URLs; the case page is
    `/cases/1460`.
  - **The scope limit that comes with it, recorded as permanent rather than pending.** The full
    H&H Award **is unpublished**. Every quotation, and the zero-occurrence screen for
    intellectual-property vocabulary, is scoped to the published Rule 48(4) excerpts and the
    Decision on Jurisdiction — **not** to the whole text. That is a **permanent scope limit, not
    a gap slug**: no future retrieval closes it, so it must not sit in a queue pretending to be
    actionable. The annulment history still comes from the ICSID case record rather than a
    retrieved document, and says so.
  - **Four further contradictions closed.** "Structural" became **"a deliberate scope
    boundary"** — Ferguson draws the boundary himself at 340, in the very sentence whose note 37
    reads "See Kim (n 16)", so the corrected wording is not a softening but the accurate cause.
    Item 6's balancing claim narrowed; the disclosure categorical qualified; Part 5 items 5, 13
    and 15 updated.
  - **`STATE_OF_THE_ANSWER.md` gained its currency anchor**, closing [[Workflow Threads]] **D3**
    — the last failure in `scripts/check_currency.py`, which now reports 9 claims, 0 failed.
    The anchor's own wording is the model for the convention: it "records what state this file
    was checked against; it does not by itself prove the content above it accurate."
  - **One observation raised and deliberately left unedited.** `STATE_OF_THE_ANSWER.md:28`'s
    clause that every disclosure case in Kim's bibliography "was brought in a court to prevent
    or restrict disclosure" **holds as scoped** to the four named — but the **Vanda CFC takings
    matter** this seat itself retrieved is a compensation action, not a suit to prevent
    disclosure, so adding it to that list would falsify the sentence *by addition*. Recorded as
    [[Workflow Threads]] **D4** for whoever adds it, because the inference would need rewriting
    and not just the parenthesis. **Raising it rather than pre-emptively hedging a true sentence
    is the disposition this seat should keep.**
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `working/benavides-comment-replies-2026-08-08.md`, `lit-review/ferguson-memo.md`,
  `lit-review/kim-memo.md`, `seeds/`, `STATE_OF_THE_ANSWER.md`,
  `analytics/locked_set/RETRIEVAL_LEDGER.md`.*
- **2026-08-08** — **A gap closed on primary sources, and two claim classes withdrawn for
  having none.** All uncommitted, branch `fix/restore-council-label`; the audited package is
  `working/benavides-comment-replies-2026-08-08.md` (9 items).
  - **Vanda, closed.** The two *Vanda Pharmaceuticals Inc. v. United States* opinions,
    No. 23-629C (Fed. Cl.), slip ops of **18 January 2024** and **22 January 2025**, were
    retrieved 2026-08-06 into the session workspace and are now held with the seed materials
    (`seeds/Vanda_v_US_23-629C_FedCl_2024-01-18_slip_op.pdf` and the 2025 twin; `seeds/` is
    gitignored, so these are **local-only and will not appear in any commit** — that is by
    design and is the reason the ledger row carries the path). Every span was re-verified and
    the gap at `lit-review/kim-memo.md:206` is **CLOSED on slip-op-only citations**, with
    **reporter page pins and appellate status expressly excluded** — 169 Fed. Cl. 196 is named
    as the reported cite and *not* pinned, and the Federal Circuit docket stays **QUEUED** at
    `analytics/locked_set/RETRIEVAL_LEDGER.md`. The prior entry, recorded at `25dfdd0` as a
    PENDING gap rather than a summary, was the right call and is what made the closure clean.
  - **Withdrawn, and kept withdrawn.** The claim that the *Saluka* ¶¶ 471–480/504 and *Bovine
    Hides* ¶¶ 11.100–11.101 passages "have now been extracted and verified" had **no source
    anywhere in the repository**. It stays withdrawn. This is the carrying-span rule doing
    what it is for: a claim about the project's own evidentiary state is a proposition and
    needs its own span.
  - **Two readings of Kim corrected against her text.** She raises the institutional question
    **herself, in her abstract** — "whether investor-state arbitration is an apt instrument to
    protect originators' data against disclosure by drug regulatory authorities" — so the
    project's "third stance" independence claim was wrong and is corrected. And her footnote 23
    had **already** qualified provisional relief, recorded at `STATE_OF_THE_ANSWER.md` line 28
    and verified against the article on 6 August: **the project's own record refuted its own
    later premise**, which is an argument for reading the record before extending it.
  - **Ferguson note 46** cites H&H for **asset characterisation**, not fork-in-the-road.
  - Canonical memos edited surgically — `lit-review/kim-memo.md` ~12 lines,
    `lit-review/ferguson-memo.md` ~10 lines, `STATE_OF_THE_ANSWER.md` line 8.
  - **New standing constraint, entered in [[Agent Registry]]:** no item enters the 54-item
    locked validation set on a memo's authority. `analytics/locked_set/` is created **empty of
    items on purpose**; **eleven** retrievals are externally gated and are Emory's, not this
    seat's (`analytics/locked_set/RETRIEVAL_LEDGER.md`).
  *Recorded against the working tree of `fix/restore-council-label` (uncommitted); paths:
  `working/benavides-comment-replies-2026-08-08.md`, `lit-review/kim-memo.md`,
  `lit-review/ferguson-memo.md`, `STATE_OF_THE_ANSWER.md`, `analytics/locked_set/`, `seeds/`.*

- **2026-08-07** — Six method rules adopted 2026-08-05 through 2026-08-07 recorded here for the
  first time, five of them governing the relay this seat fires: find-selects-a-position,
  mis-anchored-is-not-a-null, the PDF content-type gate, false-URL-is-a-control, the three
  states of `find_matched`, and commit-pinned reduction citations (`3ff5498`, `7adfd68`). Until
  this entry the note's rules section ended at 2026-08-04, so a seat reading its own note before
  the 2026-08-07 session carried none of them — including the two whose absence produced
  `0807-B1` and `0807-B5` in that session. Model unchanged (`claude-opus-5`, `HEAVY_MODEL`);
  **the definition file has not changed since `bfc8ef6`** (2026-08-04). The seat's prompt did:
  `ae1f04b` rewrote Ring 3 at `prompts/research_analyst.txt:18` and left the sentence asserting
  both definitions, and **`9efafb0`** — not `373cce6`, which [[Agent Registry]] credited on
  2026-08-06 and which touches no file under `prompts/` — is the commit that repaired it.
  Corrected in the registry in this same change set.
  *Audited against `7c08dcf`; paths: `.claude/agents/research-analyst.md`,
  `prompts/research_analyst.txt`, `prompts/council_calibration.md`,
  `prompts/carrying_span_rule.md`, `analytics/daily-research/`, `analytics/council-sessions/`,
  `src/models.py`.*
- **2026-08-04** — Three method rules adopted since 2026-07-31 recorded here for the first
  time: the carrying-span rule (`56cbb75`), the four relay method rules (`51bb7a2`), and
  no-search-synthesis-figures (`8756859`). Until this entry the note's rules section ended at
  2026-07-31, so the seat's own note carried none of them. Model is `claude-opus-5`
  (`HEAVY_MODEL`), moved from `claude-fable-5` by operator directive in `939deaa`; the two
  dated entries below are left as written, because they were true of their dates.
  *Audited against `b76f6c3`; paths: `.claude/agents/research-analyst.md`,
  `prompts/research_analyst.txt`, `prompts/council_calibration.md`,
  `analytics/daily-research/`, `analytics/council-sessions/`, `src/models.py`.*
- **2026-07-31** — Adopted method rules recorded: fetch-first (`754ce32`, re-sequenced in
  `e05f834`) and docket-page-before-document-hunt (`f03a90e`), plus the ledger-fidelity
  standing watch item from the same close-out. Model, definition, and prompt contract are
  unchanged — `git log ede0f32..e153ce3 -- .claude/agents/ prompts/` returns nothing, and
  `.claude/agents/research-analyst.md` still declares `model: fable` against
  `HEAVY_MODEL = "claude-fable-5"` in `src/models.py`. Open threads this seat owns:
  [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`, and the model promotion to `claude-fable-5`
  committed in `4f8f981` ("feat(models): research analyst promoted to Claude Fable 5
  (operator directive)"). Roster and history: [[Agent Registry]] · [[Project Change Log]].

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
