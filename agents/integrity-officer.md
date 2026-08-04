---
aliases: [Integrity Officer]
tags: [agent, council]
hub: Council
---
# Integrity Officer

**Role.** The security and verification gate before anything is published — it flags
fabrication risk, overreach, inflated relevance, and quote/access violations in the
analyst's memo, and its vetting note is binding on the editor.

**Definition.** `.claude/agents/integrity-officer.md`

**Model.** `claude-opus-4-8` — declared `model: opus` in the definition; corresponds to
`UTILITY_MODEL` in `src/models.py`, whose docstring names the "integrity helper" among the
utility sub-agents.

## Canonical training (binding)

1. `prompts/council_security.txt` — the contract verbatim: flag every instance of
   FABRICATION RISK, OVERREACH, INFLATED RELEVANCE, and QUOTE / ACCESS INTEGRITY, and
   output a short bulleted VETTING NOTE naming the required fix for each.
2. [[council_calibration]] (`prompts/council_calibration.md`) — the checklist it enforces
   in full, on every member.
3. `prompts/carrying_span_rule.md` — **the Carrying-Span Rule**, adopted by the council
   2026-08-03 as amended, added to this seat's definition on 2026-08-04. The rule's
   mechanical tiers (R5) are this seat's to enforce: entry count equals
   verification-statement count; `P`/`Q`/`D`/`V` present and non-empty; every `Q` carrying
   a quotation pair **and** a pinpoint; every case carded with an outcome *on the point
   cited* in `D`. **Amendment 2 is this seat's own contribution and the highest-value check
   in the set** — every screened term with a nonzero count must be either the source of `Q`
   or given a referent clause, because a nonzero count otherwise reads as corroboration.
   `scripts/check_marks.py` carries part of this; **its module docstring is the single
   statement of what it checks and its coverage is conditional** — read it there rather
   than trust any restatement, including this one. Whatever the script does not exercise on
   a given run is this seat's by hand, and as of 2026-08-04 that is most of it, because all
   33 entries in `lit-review/` are in the legacy form. Two traps from the same session are
   carried in this seat's own findings as well: **a zero-hit screen is not substantive
   absence until the synonym is tried**, and **a grep establishes absence from the
   repository, never from the project.**
4. `src/integrity_gate.py` and `scripts/verify.py` — the deterministic machinery that owns
   ASSERTION decisions by exact claim-id lookup against Emory's append-only ledger. The
   officer vets what code cannot: judgment-level overreach and inflation.

## Discipline highlights

- "flag anything that reads as a plausible-but-unconfirmed citation."
  (`prompts/council_security.txt`)
- "Do NOT rewrite the memo — only flag. The editor is bound to honor your note." If the
  memo is clean, say so explicitly in one line.
- Default skeptical: "verified" requires a retrieved source, and secondary "adopted/held"
  language is distrusted — "'adopted' vs 'referred back' vs 'noted' are different
  holdings."
- "Never soften an objection for harmony." The definition cites the project's strongest
  precedent for this: the title-mined Hela Schwarz characterization the officer resisted
  was later contradicted by the primary source and operator-rejected.

## Adopted method rules (session-derived, binding)

- **Positive control before any HTTP-status objection** — adopted 2026-07-31, from this
  seat's own self-disclosure. Before filing an objection that rests on an HTTP status, fetch
  a resource *known to exist* on the same host and path family, and vary the user agent. On
  2026-07-31 the officer's first-pass 403 on `uncitral.un.org` would have produced "a false
  binding objection against a correct finding"; only the positive control exposed it as an
  instrument artifact. Source: Observation 5 in
  `analytics/daily-research/2026-07-31.md`, committed in `15c8131`.
- **The Carrying-Span Rule's mechanical tiers** — adopted 2026-08-03, into this seat's
  definition 2026-08-04. Stated in full as canonical training item 3 above rather than
  repeated here. In short: this seat owns R5 tiers 2, 3, 4 and 5; `scripts/check_marks.py`
  carries part of them and its own docstring is the authority on which part, since coverage
  depends on whether entries use the four marks. Tier 4 (span-in-source) is always by hand.
  Amendment 2 — nonzero-referent parity — is this seat's own and the record calls it the
  highest-value mechanical addition in the session. Source:
  `analytics/council-sessions/2026-08-03-proposition-rule.md` R5 (`56cbb75`, merged
  `b76f6c3`).
- **The user-agent-gating finding** — the substantive result of that control, and the
  session's most consequential instrument finding. `uncitral.un.org` gates on user agent:
  under a default curl UA every path returns a 919-byte CloudFront 403 regardless of
  existence, while under a browser UA the same paths return 200 (2,104,033 b) or a genuine
  404. **A 403 from that host carries no information about resource existence.** The
  project's standing "403-blocked" characterizations for the host are access artifacts, at
  least one of them retrievable. Source: Observation 4, same commit; consequences flagged to
  the chairman as retrospective on the whole record.

### Fabrication taxonomy — the canonical table

**Read this table; do not recite the taxonomy from memory.** The reason this table exists is
recorded plainly: on 2026-08-02, 08-03 and 08-04 the in-session recitation of the "running
taxonomy" listed the ten entries as of 2026-07-31 and omitted every entry this seat had
adopted since — `analytics/daily-research/2026-08-02.md:196`, `2026-08-03.md:185` and
`2026-08-04.md:535` each open their extension section from the same stale ten-item list. The
extensions themselves were correct and were adopted; only the recitation was short. A seat
whose mandate is to check every memo against the *full* taxonomy cannot carry the full
taxonomy in a restated sentence.

**24 entries as of 2026-08-04.** Each cites the record that adopted it.

| # | Entry | Adopted | Source |
|---|---|---|---|
| 1 | Unsourced precision | pre-2026-07-31 | Definition's self-training mandate |
| 2 | Inverted dispositions | pre-2026-07-31 | Definition's self-training mandate |
| 3 | Snippet-as-fact | pre-2026-07-31 | Definition's self-training mandate |
| 4 | Title-as-holding | pre-2026-07-31 | Definition's self-training mandate |
| 5 | Memory-file reconstruction | pre-2026-07-31 | Definition's self-training mandate |
| 6 | Image-embedded primary text | pre-2026-07-31 | Recited as standing at `2026-07-31` vetting |
| 7 | Tool-status-as-source-state | 2026-07-31 | `15c8131` |
| 8 | Summarizer-render-as-full-access | 2026-07-31 | `15c8131` |
| 9 | Selective-flag reporting | 2026-07-31 | `15c8131` |
| 10 | Superseded-formulation restatement | 2026-07-31 | `15c8131` |
| 11 | Status-as-record-artifact | 2026-08-01 | `analytics/daily-research/2026-08-01.md:410`, `4d5c562` |
| 12 | Capability-as-corroboration | 2026-08-02 | `analytics/daily-research/2026-08-02.md:198`, `82692a2` |
| 13 | Absolutized heuristic | 2026-08-02 | `analytics/daily-research/2026-08-02.md:199`, `82692a2` |
| 14 | Silent class truncation | 2026-08-02 | `analytics/daily-research/2026-08-02.md:200`, `82692a2` |
| 15 | Control-inside-the-suspect-set | 2026-08-03 | `analytics/daily-research/2026-08-03.md:187`, `e9716c8` |
| 16 | Second-instrument corroboration fallacy | 2026-08-03 | `analytics/daily-research/2026-08-03.md:188`, `e9716c8` |
| 17 | Mis-dated internal-authority citation | 2026-08-03 | `analytics/daily-research/2026-08-03.md:189`, `e9716c8` |
| 17a | — extended to **mis-located** (right date, adjacent line) | 2026-08-04 | `analytics/daily-research/2026-08-04.md:537`, `51bb7a2` |
| 18 | Selective-quotation supersession | 2026-08-04 | `analytics/daily-research/2026-08-04.md:538`, `51bb7a2` |
| 19 | Codebook-free label ordering | 2026-08-04 | `analytics/daily-research/2026-08-04.md:539`, `51bb7a2` |
| 20 | Tier-parity claim | 2026-08-04 | `analytics/daily-research/2026-08-04.md:540`, `51bb7a2` |
| 21 | Constant-length determinism inference | 2026-08-04 | `analytics/daily-research/2026-08-04.md:541`, `51bb7a2` |
| 22 | Unverified control design | 2026-08-04 | `analytics/daily-research/2026-08-04.md:542`, `51bb7a2` |
| 23 | Echoed-find / self-confirming query | 2026-08-04 | `analytics/daily-research/2026-08-04.md:543`, `51bb7a2` — named by the analyst, adopted under his formulation |
| 24 | Amendment-stripping | 2026-08-04 | integrity-officer vetting note, 2026-08-04 implementation session (in-session; not a committed artifact) |

Entries 7–10, in the officer's own 2026-07-31 wording (`15c8131`):

- **Tool-status-as-source-state** — a fetch layer's or CDN's HTTP status reported as a
  fact about the resource. Countermeasure: positive control on the same host and path
  family, and vary the user agent, before recording any status finding.
- **Summarizer-render-as-full-access** — a model-mediated render treated as
  `access_status: full` and as the basis for character-exact quotation. Countermeasure:
  quote claims require raw HTML or a PDF text layer; renders support substance, never
  characters.
- **Selective-flag reporting** (access-integrity family) — citing a verification record's
  favorable flags while omitting the adverse flag from the same event; here `quote_ok: true`
  reported and `scope_ok: false` omitted.
- **Superseded-formulation restatement** — restating an earlier, looser version of a
  proposition the project's own record has since tightened. Countermeasure: when restating a
  record proposition, search for its **latest dated refinement**, not its first statement.
  This entry became the chairman's delegation rule the same day.

Entries 11–23, countermeasures as adopted:

- **11 · Status-as-record-artifact** — a tool status correctly withheld from the claim text
  but converted into a *record object* (a gap slug, an escalation counter, an
  `access_status: "blocked"` field) whose existence asserts the inaccessibility the status
  cannot establish. Countermeasure: any record artifact predicated on inaccessibility needs
  the same same-host positive control as a status claim; absent a control the item is "not
  attempted under a passing UA", never "blocked", and no slug opens.
- **12 · Capability-as-corroboration** — crediting a past finding with corroboration from a
  channel that was merely *available* that day. Countermeasure: count channels the record
  shows were used, never channels that were working.
- **13 · Absolutized heuristic** — a condition-specific instrument finding restated in a
  method note as an exceptionless rule. Countermeasure: a self-training rule carries the
  conditions of the observation that produced it.
- **14 · Silent class truncation** (sibling of 9) — restating an enumerated class with fewer
  members than the record holds, and fixing the short count as the standing figure.
  Countermeasure: re-enumerate any class from the record at URL level before re-queueing it.
- **15 · Control-inside-the-suspect-set** — a positive control drawn from the same host or
  instrument class as the item under test, so it cannot separate the suspected artifact from
  a general instrument failure. Countermeasure: every positive control pairs a suspect-host
  probe with a neutral-host probe on the same instrument.
- **16 · Second-instrument corroboration fallacy** — treating a second tool's identical
  failure as independent corroboration when the second tool was never shown functional.
  Countermeasure: prove the instrument alive before reading its failures as evidence.
- **17 · Mis-dated (2026-08-04: and mis-located) internal-authority citation** — citing the
  project's own record by date, or by line, for a proposition that date or line does not
  contain. Countermeasure: grep the cited date and the cited line before citing it.
- **18 · Selective-quotation supersession** — declaring a record formulation superseded by
  quoting only the part of the governing line that supports the ruling. Countermeasure: when
  ruling that the record has changed position, quote the **whole** governing line.
- **19 · Codebook-free label ordering** — ranking a controlled vocabulary's values on a
  permissive/restrictive scale without the vocabulary's codebook. Countermeasure: a
  database's labels may be reported and compared for identity, never ordered, absent its
  codebook.
- **20 · Tier-parity claim** — asserting a newly retrieved item occupies "the same
  evidentiary tier" as an operator-verified ledger entry when it has no claim-id, no
  operator verification and no preserved snapshot. Countermeasure: tier statements name the
  ledger status explicitly or are not made.
- **21 · Constant-length determinism inference** — reading equal byte length as proof of
  unchanged content, and counting near-simultaneous same-run fetches as independent
  observations. Countermeasure: count time points, not rows.
- **22 · Unverified control design** (extends 15) — proposing a control whose negativity or
  branch-bypass is assumed rather than established. Countermeasure: state what makes a
  control negative, and treat the control block as uninterpreted until the positive control
  fires.
- **23 · Echoed-find / self-confirming query** (instrument family) — a `find` string the
  target page can generate from the request URL, so `find_matched` reports a property of the
  request. Countermeasure: never choose as `find` a string the target page can generate from
  your own request.

*Counting note.* `analytics/daily-research/2026-08-04.md:535` introduces its list as "fresh
instances and five extensions" and then sets out seven bullets — one extension of entry 17
and six new entries. The table above counts the entries as written, not the header, and says
so rather than reconciling the header silently.

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- Flowchart box: `integrity-officer`, in the Emory-checks column (row 11), added by
  flowchart v3.0 (`21f0240`) — "Vets every memo for fabrication, overreach and inflation;
  objections binding." Card model reads "Model: Claude Opus 4.8", matching the definition.
  It sits in that column rather than the council column because it is drawn beside the two
  deterministic halves of the same verification function.
- Those deterministic halves are `claim-gate` ("Claim gate (automatic)") and
  `citation-check`. This is the design recorded in `COUNCIL.md`: the deterministic gate
  "Replaces the former LLM security officer for assertion decisions." The LLM seat still
  speaks inside the council's dialogue (`prompts/council_roundtable.txt`,
  `prompts/daily_council_protocol.md` Rule 2); the box records the seat, not a pipeline
  stage.
- The seat's own edges: fed by `analyst` ("daily meetings: the integrity-officer subagent
  vets the analyst memo"); feeds `packet` ("vetting flags reach Emory through the meeting
  record and Monday packet"). Both are `check`-kind edges.
- `claim-gate` is fed by `analyst` ("candidate_claims into integrity_gate") and by `ledger`
  ("integrity_gate replays the ledger"); it feeds `editor` ("`_gate_note` handed to the
  editor").
- `citation-check` is fed by `analyst` ("`_verify_citations` over the memo") and feeds both
  `editor` and `packet` (unverifiable or URL-less citations become verification debt in
  Emory's Monday packet).

## Self-training mandate

Rewritten in the definition on 2026-08-04. It now reads, in substance: *maintain a running
taxonomy of fabrication patterns caught in this project and check every memo against the
**full** taxonomy, extending it whenever a new pattern appears. The taxonomy's home is
`agents/integrity-officer.md` in the vault — read it there; do not work from a list
enumerated in the definition, because an enumeration there goes stale silently.*

The mandate names its own instance: council R8 found the definition still enumerating five
patterns while this note's taxonomy stood at ten, and recorded that the same-day sync the
council had called "the cheapest mechanical win in the session" did not bind within the day,
in the single file it named.

**What the rewrite costs and what it buys.** The definition no longer carries the patterns,
so an instantiated prompt no longer contains them; the seat must read this note. That trades
a list that silently drifts for a read that can be silently skipped. The trade is only worth
making if this note stays current — which is why the count is in the heading and the change
log below dates every extension.

*The superseded text, for the record:* "Maintain a running taxonomy of fabrication patterns
caught in this project (unsourced precision, inverted dispositions, snippet-as-fact,
title-as-holding, memory-file reconstruction) and check every memo against the full
taxonomy, extending it whenever a new pattern appears." Five patterns named against a
taxonomy of ten.

## Change log

- **2026-08-04** — The canonical taxonomy table landed here, 23 entries, one citation per
  entry, replacing the "extended to ten" section that had been current since 2026-07-31.
  Thirteen entries adopted by this seat on 2026-08-01 (`4d5c562`), 2026-08-02 (`82692a2`),
  2026-08-03 (`e9716c8`) and 2026-08-04 (`51bb7a2`) had never reached this note. **The
  2026-08-03 archivist session recorded that it had made exactly this fix — audit slice item
  4 of [[obsidian-archivist]] — and the change did not reach `main`:** `git log 6a5cd2e..HEAD
  -- agents/` shows no commit adding 08-0x content to this note. The recitation defect that
  fix was meant to close therefore recurred on 08-03 and 08-04. Model, definition and prompt
  bindings unchanged.
  *Audited against `b76f6c3`; paths: `.claude/agents/integrity-officer.md`,
  `prompts/council_security.txt`, `prompts/council_calibration.md`,
  `analytics/daily-research/`, `views/isds-workflow-3d/workflow.json`.*
- **2026-07-31** — Two drifts fixed. (1) The "no box of its own" statement was stale: this
  seat gained the `integrity-officer` box in flowchart v3.0 (`21f0240`), with two edges
  (`analyst → integrity-officer`, `integrity-officer → packet`). (2) The taxonomy recorded
  here was four entries short. Added the positive-control rule, the user-agent-gating
  finding, and the four new taxonomy entries, all from the 2026-07-31 vetting note
  (`15c8131`). Session disposition that day: **FLAGGED** — four binding objections and eight
  hedges, all accepted by the chairman without modification (`f03a90e`). Model and
  definition unchanged (`model: opus`; no commit touched `.claude/agents/` between `ede0f32`
  and `e153ce3`). Threads: [[Workflow Threads]].
- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].


### Entry 24 — added 2026-08-04

- **Amendment-stripping** — a rule lifted out of a session record **in its pre-vetting draft
  form**, carrying the adoption date and the word *binding*, with every objection that
  conditioned adoption silently absent. The artifact is authentic, the attribution is
  correct, and the date is right; what is missing is the amendments that were the price of
  adoption, so the published rule is weaker than the rule the council actually adopted and
  nothing on its face says so. Distinct from *superseded-formulation restatement*, which
  restates an older proposition of the project's own record; here the *governing* text is
  replaced by a draft of itself. Countermeasure: **lift from the ruling, never from the
  member's return** — and when a record marks a text "as amended", the carrier names which
  amendments are folded in and where the superseded draft sits, so a reader can tell the two
  apart.
  - **Instance, 2026-08-04.** In the change set that implemented the Carrying-Span Rule, the
    draft at Part 3 §1 of `analytics/council-sessions/2026-08-03-proposition-rule.md` — the
    systems designer's return, written before the officer's four amendments — is a
    near-complete rule text sitting under the heading "THE RULE", 1,150 lines above the
    ruling that supersedes it. Taking it would have shipped a binding rule missing step 3's
    same-matter exit, the `V`-mark referent clause and its parity check, the
    no-rigid-designator label, and item 5's finality condition. **Caught in vetting.** The
    guard the catch produced is now standing, at `prompts/carrying_span_rule.md:3-7`: *"do
    not lift the draft at Part 3 §1 of that record, which predates the amendments."*
    Recorded from the integrity officer's vetting note for the 2026-08-04 implementation
    session — that note is in-session and is not itself a committed artifact, which is
    stated here rather than left for a reader to discover.

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
