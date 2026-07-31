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
3. `src/integrity_gate.py` and `scripts/verify.py` — the deterministic machinery that owns
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
- **The user-agent-gating finding** — the substantive result of that control, and the
  session's most consequential instrument finding. `uncitral.un.org` gates on user agent:
  under a default curl UA every path returns a 919-byte CloudFront 403 regardless of
  existence, while under a browser UA the same paths return 200 (2,104,033 b) or a genuine
  404. **A 403 from that host carries no information about resource existence.** The
  project's standing "403-blocked" characterizations for the host are access artifacts, at
  least one of them retrievable. Source: Observation 4, same commit; consequences flagged to
  the chairman as retrospective on the whole record.

### Fabrication taxonomy — extended to ten

The running taxonomy this seat maintains under its self-training mandate stood at six —
*unsourced precision, inverted dispositions, snippet-as-fact, title-as-holding, memory-file
reconstruction, image-embedded primary text*. Four entries were added on 2026-07-31
(`15c8131`):

- **Tool-status-as-source-state** (new) — a fetch layer's or CDN's HTTP status reported as a
  fact about the resource. Countermeasure: positive control on the same host and path
  family, and vary the user agent, before recording any status finding.
- **Summarizer-render-as-full-access** (new) — a model-mediated render treated as
  `access_status: full` and as the basis for character-exact quotation. Countermeasure:
  quote claims require raw HTML or a PDF text layer; renders support substance, never
  characters.
- **Selective-flag reporting** (extension of the access-integrity family) — citing a
  verification record's favorable flags while omitting the adverse flag from the same event;
  here `quote_ok: true` reported and `scope_ok: false` omitted.
- **Superseded-formulation restatement** (new) — restating an earlier, looser version of a
  proposition the project's own record has since tightened. Countermeasure: when restating a
  record proposition, search for its **latest dated refinement**, not its first statement.
  This entry became the chairman's delegation rule the same day.

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

"Maintain a running taxonomy of fabrication patterns caught in this project (unsourced
precision, inverted dispositions, snippet-as-fact, title-as-holding, memory-file
reconstruction) and check every memo against the full taxonomy, extending it whenever a
new pattern appears."

## Change log

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
