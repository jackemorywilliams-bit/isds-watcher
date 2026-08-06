---
aliases: [Agent Registry]
tags: [agent, council]
hub: Council
---
# Agent Registry

The roster at a glance: every durable agent definition in `.claude/agents/`, the model it
runs on, the canonical prompt files it binds, and its vault note. Nine agents, all
established on or before 2026-07-30 (`a852b80`, `16836d1`).

Model ids are the ones in `src/models.py` — the single model-configuration location — read
together with each definition's frontmatter. Where a definition declares no model, that is
recorded as "none declared" rather than inferred.

Open work by thread and owner: [[Workflow Threads]]. Dated history: [[Project Change Log]].

**Definitions re-audited 2026-08-06 against `373cce6`.** The 2026-08-04 statement below was
true when written and false by the following day. `git log 939deaa..HEAD -- .claude/agents/
prompts/` now returns five commits, and one **is** a contract change: `ae1f04b` rewrote the
research question at `.claude/agents/council-chairman.md:31-32` to "a live, litigated
jurisdictional/admissibility doctrine, whether or not it disposes of the case," together with
six prompt files. Under this note's own maintenance rule that change required the registry to
move in the same change set, and it did not. `373cce6` additionally corrected
`prompts/research_analyst.txt:18`, which `ae1f04b` had left asserting **both** Ring 3
definitions in one ungrammatical sentence. Anchor for the next currency query:
`git log 373cce6..HEAD -- .claude/agents/ prompts/`.

**Superseded, retained so the correction stays legible — audited 2026-08-04.**
`git log 6a5cd2e..b76f6c3 -- .claude/agents/ prompts/`
returns two commits, and neither is a contract change: both are the same four-line managed
`Map:` block appended to `prompts/daily_council_protocol.md` by `scripts/build_graph.py`
(`07ff434`, carried through `8705f7a`). No definition file has changed since `939deaa` moved
the chairman and analyst to Opus 5. Every model, contract and prompt binding in the table
below still reads as committed. What *did* change is each seat's working context — the method
rules the council adopted in session, now recorded in the seat notes — and the flowchart.

## Roster

| Agent | Model | Canonical prompts | Definition | Vault note |
|---|---|---|---|---|
| Council chairman | `claude-opus-5` (`CHAIRMAN_MODEL`) | `prompts/council_chairman.txt`, `prompts/council_reconvene.txt`, `prompts/council_calibration.md` | `.claude/agents/council-chairman.md` | [[council-chairman]] |
| Research analyst | `claude-opus-5` (`HEAVY_MODEL`) | `prompts/research_analyst.txt`, `prompts/council_calibration.md`, `prompts/carrying_span_rule.md` | `.claude/agents/research-analyst.md` | [[research-analyst]] |
| Integrity officer | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/council_security.txt`, `prompts/council_calibration.md`, `prompts/carrying_span_rule.md` | `.claude/agents/integrity-officer.md` | [[integrity-officer]] |
| Analytics officer | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/council_roundtable.txt`, `prompts/daily_council_protocol.md` | `.claude/agents/analytics-officer.md` | [[analytics-officer]] |
| Systems researcher | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/systems_researcher.txt` | `.claude/agents/systems-researcher.md` | [[systems-researcher]] |
| Research editor | `claude-opus-4-8` (`UTILITY_MODEL`) | `prompts/research_editor.txt`, `prompts/carrying_span_rule.md` | `.claude/agents/research-editor.md` | [[research-editor]] |
| Obsidian archivist | `claude-opus-4-8` | none — canon is the vault, `scripts/build_graph.py`, `scripts/build_site.py` | `.claude/agents/obsidian-archivist.md` | [[obsidian-archivist]] |
| Systems designer | `claude-opus-5` — card-asserted; `model: opus` (tier) declared since `c25ea64` | none — canon is the repository's machinery and `src/models.py` | `.claude/agents/systems-designer.md` | [[systems-designer]] |
| Site & correspondence experience | `claude-opus-5` — card-asserted; `model: opus` (tier) declared since `c25ea64` | none — canon is `scripts/build_site.py`, `site_templates/`, `src/render.py` | `.claude/agents/site-experience.md` | [[site-experience]] |

Not an agent, but bound by the same model config: the digest classifier runs on
`claude-haiku-4-5-20251001` (`DIGEST_CLASSIFIER_MODEL`, read by `src/classify.py`), and the
runtime-fallback rule requires any REQUESTED-vs-ACTUAL discrepancy to be written into
`HANDOFF.md` rather than silently substituted.

## Flowchart cards → notes (click-through map)

Every one of the nine agents has its own card, since the build committed as `21f0240` ("all
nine subagents on the chart, cards link to their vault training notes"). Each role card's
`target` is an Obsidian link text that `views/isds-workflow-3d/view.js` hands to
`dv.app.workspace.openLinkText`, so `target: "agents/<name>"` must match a note filename
exactly. **All ten role cards resolve** — verified 2026-08-04 against
`views/isds-workflow-3d/workflow.json`, which now reads **30 nodes, 44 edges**;
`node tools/isds-workflow-3d/validate.mjs` exits 0 and reports the same counts against both
the manifest and the generated SVG.

*Version naming, corrected 2026-08-04.* This registry previously called the chart "v3.0",
which is the naming in `21f0240`'s commit message, not the manifest's own. The manifest's
`meta.version` reads **2.2** (`views/isds-workflow-3d/workflow.json`), whose `meta.note`
dates v2.2 to 2026-08-03: the fetch relay added to the machine lane, and the two builder
seats moved from machine rows 7–8 to rows **9–10** to clear the corridor its answer crosses.
The registry now follows the manifest.

Card models below are re-read from `views/isds-workflow-3d/workflow.json` on 2026-08-04.

| Card (`workflow.json` id) | Column · row | `target` | Card model | Note |
|---|---|---|---|---|
| `chairman` | council · 7 | `agents/council-chairman` | Claude Opus 5 | [[council-chairman]] |
| `minutes` | council · 11 | `agents/council-chairman` | Claude Opus 5 | [[council-chairman]] — the reconvene output of the same seat |
| `analyst` | council · 8 | `agents/research-analyst` | Claude Opus 5 | [[research-analyst]] |
| `systems-researcher` | council · 9 | `agents/systems-researcher` | Claude Opus 4.8 | [[systems-researcher]] |
| `editor` | council · 10 | `agents/research-editor` | Claude Opus 4.8 | [[research-editor]] |
| `analytics-officer` | council · 12 | `agents/analytics-officer` | Claude Opus 4.8 | [[analytics-officer]] |
| `obsidian-archivist` | council · 14 | `agents/obsidian-archivist` | Claude Opus 4.8 | [[obsidian-archivist]] |
| `integrity-officer` | Emory checks · 11 | `agents/integrity-officer` | Claude Opus 4.8 | [[integrity-officer]] |
| `systems-designer` | machine · **9** | `agents/systems-designer` | Claude Opus 5 ⚠ | [[systems-designer]] |
| `site-experience` | machine · **10** | `agents/site-experience` | Claude Opus 5 ⚠ | [[site-experience]] |

Rows and card models re-read from the manifest 2026-08-04. The two builder seats moved down
two rows in v2.2 to make room for the relay; the chairman, analyst, systems-researcher,
editor, minutes, analytics-officer, obsidian-archivist and integrity-officer cards are at
the rows shown above, unchanged.

✔ **Closed 2026-08-05 at `c25ea64`; corrected here 2026-08-06.** This note carried the defect
as open — "a card asserts a model no configuration file carries" — for a full day after it was
closed, while [[Claim Map]] C12 and [[Workflow Threads]] C7 both recorded it CLOSED. Three
vault notes, one fact, and the roster — the note an agent reads first — was the one that was
wrong. Verified 2026-08-06: all nine `.claude/agents/*.md` declare `model: opus`, including
`systems-designer.md` and `site-experience.md`, and `scripts/check_models.py` fails the build
on card/definition/vault-note drift.

**The constraint that replaces it, because it is a live trap rather than a closed one:**
`model:` selects a *tier*, not a version, so the version check rests on card ↔ `src/models.py`
↔ vault note, and the vault-note leg matches only the ``**Model.** `…` `` form at
`check_models.py:63`. **Reformatting a seat note silently removes a leg of a CI guard.** The
chart is generated from its manifest and is not hand-edited to make a discrepancy disappear.

**Two non-agent cards added in v2.2** — `relay-request` and `relay-answer`, machine rows 7–8,
the fetch relay the council uses for retrieval. They are code, not seats: evidence cites
`.github/workflows/fetch-relay.yml` and `scripts/fetch_relay.py` (`fe02f39`, targeted-excerpt
refinement `7fbbabf`). No agent owns them; [[systems-designer]] built them.

Non-agent cards, unchanged:

| Card | Column | Resolves to |
|---|---|---|
| `daily-researcher` | council | `COUNCIL.md` — the daily routine that convenes the full council; the substantive seat in it is [[research-analyst]] |
| `next-week` | council | `STATE_OF_THE_ANSWER.md` — no single owner: the living-memory files written by the analyst and the chairman's minutes |
| `claim-gate`, `citation-check` | Emory checks | The deterministic half of the verification function (`src/integrity_gate.py`, `scripts/check_citations.py`); the judgment half is [[integrity-officer]] |
| `collect` … `quality-bar` | machine | Code, not agent seats — built by [[systems-designer]]; `ai-check` runs the digest classifier on Haiku 4.5 |
| `daily-email` … `packet` | deliverables | Owned by [[site-experience]] |
| `emory-checks`, `ledger` | Emory checks | Emory — human judgment and the append-only ledger; no agent owns these |

## Graph note

This is an index note. Its outgoing links exceed the four-link cap for spokes in
`scripts/build_graph.py` (`MAX_DIRECT_LINKS_PER_NOTE`), so a `build_graph` run prints one
WARN naming this file. That is expected for a roster and is recorded here so the warning is
never mistaken for drift.

As of 2026-08-04 a `build_graph --dry-run` prints **four** WARNs. Two are expected: this note
(11 direct links) and [[Workflow Threads]] (9) are index notes, and the cap exists to keep
ordinary spokes from becoming hubs, which is not what these are. A third,
`think-tank/multi-agent/_MOC.md` (8), predates the agent-memory area.

**The fourth is drift, and it is new:** `agents/obsidian-archivist.md` now reports 6 direct
links against the cap of 4. The rule this note stated on 2026-07-31 — *any WARN naming a
per-agent note would be drift, and there are none* — no longer holds, and the exception is
the archivist's own note. The same run reports one broken link from that file, to a
note named `Project Machinery`, which does not exist in the vault. Both are recorded rather
than fixed by inventing the missing note; the archivist's note is the next slice due for
audit.

**Eleven notes are awaiting their managed block.** `build_graph --dry-run` on 2026-08-04
plans edits to `prompts/carrying_span_rule.md`, `lit-review/BIBLIOGRAPHY_TEMPLATE.md`, both
`analytics/council-sessions/2026-08-03-*.md` records, `analytics/vault-sessions/README.md`,
`analytics/vault-sessions/2026-08-04.md`, `analytics/fetch-requests/README.md`, and the four
`analytics/daily-research/2026-08-0*.md` records — every one of them a file created since the
last full run. The run was **not** performed this session: it is a whole-vault operation and
would put nine files unrelated to the rule into a branch scoped to it. The list is recorded
here so the pending run is not lost.

The notes under `agents/` carry their managed `Map:` blocks as of 2026-07-31, when
`build_graph` was first run over this area after the `807666f` scan-boundary fix. Those
blocks are generated: they are never hand-edited, and a run must leave them byte-identical.

## Maintenance

When any agent's prompt, model, or contract changes, this table and the corresponding note
change in the same commit, and the change is dated and cited in [[Project Change Log]].

## Adopted method rules by seat

Rules the council adopted in session that are now part of a seat's working context. Full
statements live in the seat's own note.

| Seat | Rule | Adopted | Commit |
|---|---|---|---|
| [[research-analyst]] | Fetch-first — attempt the direct fetch before reconstructing from search results | 2026-07-30 | `754ce32` (re-sequenced `e05f834`) |
| [[research-analyst]] | Docket page before document hunt — for any ICSID question, fetch the case-detail page first | 2026-07-31 | `f03a90e` |
| [[integrity-officer]] | Positive control before any HTTP-status objection | 2026-07-31 | `15c8131` |
| [[integrity-officer]] | Fabrication taxonomy extended from six entries to ten | 2026-07-31 | `15c8131` |
| [[research-analyst]] | **Carrying-Span Rule** — every source cited for a proposition, its own included; binds returns and daily research records (R7), not `candidate_claims` | 2026-08-03, into the definition 2026-08-04 | `56cbb75` / `prompts/carrying_span_rule.md` |
| [[research-editor]] | **Carrying-Span Rule clause 6** — relational and superlative claims about a source are propositions and need their own span | 2026-08-03, into the definition 2026-08-04 | `56cbb75` / `prompts/carrying_span_rule.md` |
| [[integrity-officer]] | **Carrying-Span Rule R5 tiers** — mark parity, nonzero-referent parity (its own Amendment 2), degenerate uniformity; tier 4 by hand | 2026-08-03, into the definition 2026-08-04 | `56cbb75` / `scripts/check_marks.py` |
| [[integrity-officer]] | Taxonomy entry 24 — *amendment-stripping* | 2026-08-04 | integrity-officer vetting note, 2026-08-04 implementation session (in-session; not a committed artifact) |
| [[integrity-officer]] | Self-training mandate points at the vault taxonomy instead of enumerating patterns | 2026-08-04 | `.claude/agents/integrity-officer.md` |
| [[council-chairman]] | Member return-path protocol (SendMessage to launcher; route via "main" on bounce) | 2026-07-30, first applied 07-31 | `de7b0fc` |
| [[council-chairman]] | Spend checkpoint immediately after the vetting round | 2026-07-30, first applied 07-31 | `de7b0fc` / `15c8131` |
| [[council-chairman]] | Name the proposition's latest dated refinement when delegating | 2026-07-31 | `f03a90e` |
| [[integrity-officer]] | Taxonomy entry 11 — status-as-record-artifact | 2026-08-01 | `4d5c562` |
| [[council-chairman]] | Standing-conventions block in the delegation template | 2026-08-01 | `4d5c562` |
| [[integrity-officer]] | Taxonomy entries 12–14 — capability-as-corroboration, absolutized heuristic, silent class truncation | 2026-08-02 | `82692a2` |
| [[integrity-officer]] | Taxonomy entries 15–17 — control-inside-the-suspect-set, second-instrument corroboration fallacy, mis-dated internal-authority citation | 2026-08-03 | `e9716c8` |
| [[council-chairman]] | Probe the instruments before writing the agenda | 2026-08-03, first applied 08-04 | `8756859` |
| [[council-chairman]] | An objection is a claim like any other | 2026-08-03 | `1109993` |
| [[research-analyst]] | The carrying-span rule (adopted in text, recorded **unvalidated**) | 2026-08-03 | `56cbb75` |
| [[integrity-officer]] | Taxonomy entries 18–23 + entry 17 extended to mis-located | 2026-08-04 | `51bb7a2` |
| [[research-analyst]] | Four relay method rules (binding on every seat) | 2026-08-04 | `51bb7a2` |
| [[council-chairman]] | Before a ruling asserts what a record line says, quote the whole line | 2026-08-04 | `51bb7a2` |

The taxonomy's canonical statement is the 23-entry table in [[integrity-officer]], one
citation per entry. It exists because the in-session recitation of the taxonomy was four to
thirteen entries short on 2026-08-02, 08-03 and 08-04 — the seat is directed to read the
table rather than restate the list from memory.

## Change log

- **2026-08-04** — Registry brought current with the flowchart and with eleven method rules
  adopted 2026-08-01 through 2026-08-04. Corrections: the chart is **30 nodes / 44 edges**,
  not the 28/40 recorded here since 2026-07-31 (`0e7d0f7`, `16ab9d9`); the two builder cards
  sit at machine rows 9 and 10, not 7 and 8; the chart's version is the manifest's **2.2**,
  not the commit-message "v3.0" this note had been using; the two disputed cards now read
  "Model: Claude Opus 5" after `939deaa`, which left the underlying defect intact while
  making it look legitimate; and two new non-agent cards, `relay-request` and `relay-answer`,
  are recorded. Definitions themselves unchanged — the only commit under `.claude/agents/` or
  `prompts/` since `6a5cd2e` appends a managed `Map:` block to one prompt file.
  *Audited against `b76f6c3`; paths: `.claude/agents/`, `prompts/`, `src/models.py`,
  `views/isds-workflow-3d/workflow.json`, `agents/`.*
- **2026-07-31** — Registry audited against `.claude/agents/`, `src/models.py`, and
  `views/isds-workflow-3d/workflow.json`. Definitions unchanged (`ede0f32..e153ce3` touches
  neither `.claude/agents/` nor `prompts/`). Two corrections: the flowchart mapping was
  rewritten for **v3.0** (`21f0240`), which gave all nine seats a card and made the previous
  "two seats have no box at all" sentence wrong; and the model conflict on the
  `systems-designer` / `site-experience` cards is now recorded and escalated. Adopted method
  rules added by seat. Threads note added: [[Workflow Threads]].
- **2026-07-30** — Registry created with all nine agents, in the vault's inaugural
  agent-memory build. Sources: `16836d1` (seven council definitions) and `a852b80`
  (systems-designer, site-experience).

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
