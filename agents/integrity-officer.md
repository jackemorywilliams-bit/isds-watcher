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

## Place in the workflow

Source of truth: `views/isds-workflow-3d/workflow.json`.

- The LLM security seat has **no box of its own**: it speaks inside the council's dialogue
  (`prompts/council_roundtable.txt`, `prompts/daily_council_protocol.md` Rule 2). What the
  flowchart draws is the deterministic half of the same function — the `claim-gate`
  ("Claim gate (automatic)") and `citation-check` boxes in the Emory column. This is the
  design recorded in `COUNCIL.md`: the deterministic gate "Replaces the former LLM security
  officer for assertion decisions."
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

- **2026-07-30** — Note created in the vault's inaugural agent-memory build. Records the
  agent definition committed in `16836d1`. Roster and history: [[Agent Registry]] ·
  [[Project Change Log]].
