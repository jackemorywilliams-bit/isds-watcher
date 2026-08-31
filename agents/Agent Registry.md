---
aliases: [Agent Registry]
tags: [agent, council]
hub: Council
---
# Agent Registry

**Currency anchor.** *Audited against `7ac387b`.* Machine-owned; `scripts/reanchor.py` moves the sha to the session's last substantive commit in a notes-only close-out commit that `scripts/check_currency.py` excludes from drift as maintenance. Do not hand-edit the sha; the dated snapshot-anchor narrative below is preserved unedited as history.

The roster at a glance: every durable agent definition in `.claude/agents/`, the model it
runs on, the canonical prompt files it binds, and its vault note. Nine agents, all
established on or before 2026-07-30 (`a852b80`, `16836d1`).

Model ids are the ones in `src/models.py` — the single model-configuration location — read
together with each definition's frontmatter. Where a definition declares no model, that is
recorded as "none declared" rather than inferred.

Open work by thread and owner: [[Workflow Threads]]. Dated history: [[Project Change Log]].

**Definitions re-audited against `8ea2ee1` — 2026-08-13.** `git log 667772c..HEAD --
.claude/agents/ prompts/ src/models.py` returns **no commit**, and no file under
`.claude/agents/` has changed since before 2026-08-07. Every model, prompt binding and contract
in the roster below therefore reads exactly as committed, and `scripts/check_models.py` exits 0
over twelve cards ("every card names a configured model, backed by a declared `model:` key, and
no vault note contradicts its card"). `src/models.py` is unchanged: `CHAIRMAN_MODEL` and
`HEAVY_MODEL` at `claude-opus-5`, `UTILITY_MODEL` and `FALLBACK_MODEL` at `claude-opus-4-8`,
`DIGEST_CLASSIFIER_MODEL` at `claude-haiku-4-5-20251001`. **No model drift exists.**

**What the model check cannot see, and this pass measured instead.** `check_models.py` verifies
that each seat's *declared* model matches its card and its note. It does not ask whether the
rules a seat has adopted are inside that seat's context — and they are mostly not. A seat's read
path is its `.claude/agents/` definition plus the `prompts/` files that definition enumerates.
**Eight of the nine definitions never name the seat's own vault note**, while those notes carry
sections explicitly marked binding: `agents/research-analyst.md:59-142` (eleven adopted method
rules), `agents/council-chairman.md:46-133` (adopted session protocol),
`agents/analytics-officer.md:40-62` (standing observations). Ten of the analyst's eleven rules
are absent from its read path; so are the four `label: 1` rows of `scripts/holdout_set.json`,
which is the mechanism behind the 2026-08-03 holdout failure. The exception is
[[integrity-officer]], whose definition points at its note and says why
(`.claude/agents/integrity-officer.md:56-62`) — a remedy adopted for one seat after council R8
and never generalised. **Editing `.claude/agents/` is a contract change and is Emory's**, so
this is escalated, not corrected: [[Workflow Threads]] **D5**.

**Definitions audited against `667772c` — 2026-08-11, at integration.** The only commit
touching this note's declared paths since `2686422` is the integration's own `667772c`,
which adds `prompts/classifier_v2.txt` and `prompts/triage.txt` — the prompt files for the
semantic and triage lanes that ship off by default (`V2_SHADOW_CALLS`, `TRIAGE_ENABLED`).
No seat's model, contract or prompt binding changed. Anchor for the next currency query:
`git log 667772c..HEAD -- .claude/agents/ prompts/ src/models.py`.

**Definitions re-audited 2026-08-08 against `2686422` plus the uncommitted working tree of the
master-prompt repair session, branch `fix/restore-council-label`.** `git log 373cce6..HEAD --
.claude/agents/ prompts/` returns **no commit**, and `git status --short` shows **no modified
file** under either path. **No seat's model, prompt binding or contract changed on 2026-08-07
or 2026-08-08**, so the roster below stands as committed. `scripts/check_models.py` re-run the
same day exits 0 over twelve flowchart cards. That is a measurement, not an inheritance from
the previous pass. Anchor for the next currency query: `git log 2686422..HEAD --
.claude/agents/ prompts/`.

**One definition-level statement is now falsified by a repo finding, and it is not a drift
this seat may fix.** `.claude/agents/systems-designer.md:17` binds that seat to "the
**zero-cost** constraint". On 2026-08-08 a code reading established that
`classify_item(item, provider=None)` falls through to `os.environ["MODEL_PROVIDER"]` rather
than forcing the keyword path, so the below-cutoff tail has been **model-classified in
production all along** (`analytics/instrument-map-2026-08-08.md` §4); `README.md:3-9` was
corrected the same day to say the instrument is "low-cost, roughly cents per run, not free."
The definition still says zero-cost. **Editing `.claude/agents/` is a contract change and
belongs to Emory**, so this is recorded and escalated, not corrected here; the vault note
[[systems-designer]] carries the same entry. The parallel line in that seat note — its
canonical-training item 3 — **is** this seat's surface and has been corrected.

**Definitions re-audited 2026-08-07 against `7c08dcf`.** `git log 373cce6..HEAD --
.claude/agents/ prompts/` returns exactly one commit, `33861fd`, and it is **not** a contract
change: it appends a live-verification-count block to `prompts/daily_council_protocol.md`. No
`.claude/agents/*.md` file has changed since `ae1f04b` (2026-08-05, the chairman's research
question). Every model, contract and prompt binding in the table below reads as committed, and
`python3 scripts/check_models.py` exits 0 over all twelve model-bearing cards.

**One correction to the 2026-08-06 audit immediately below, and it is this note's own.** That
paragraph credits `373cce6` with correcting `prompts/research_analyst.txt:18`. It did not:
`git show --stat 373cce6 -- prompts/` is empty, and the commit that repaired the sentence is
**`9efafb0`** ("fix(counts): the duplicate cannot be assigned to either side of the ring
split"), whose own message states the fix. This is the integrity officer's taxonomy 17a,
*mis-located internal-authority citation*, committed by the seat that maintains the taxonomy's
home. The paragraph is corrected in place rather than rewritten, so the correction stays
legible.

**Superseded, retained — audited 2026-08-06 against `373cce6`.** The 2026-08-04 statement below was
true when written and false by the following day. `git log 939deaa..HEAD -- .claude/agents/
prompts/` then returned five commits, and one **is** a contract change: `ae1f04b` rewrote the
research question at `.claude/agents/council-chairman.md:31-32` to "a live, litigated
jurisdictional/admissibility doctrine, whether or not it disposes of the case," together with
six prompt files. Under this note's own maintenance rule that change required the registry to
move in the same change set, and it did not. ~~`373cce6` additionally corrected
`prompts/research_analyst.txt:18`~~ — *false; it was `9efafb0`, see the correction above* —
which `ae1f04b` had left asserting **both** Ring 3
definitions in one ungrammatical sentence.

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

⚠ **reads "this row was once the defect", not "this row is wrong".** Both cards asserted a model
no configuration file carried, from `21f0240` until `c25ea64` declared the two missing `model:`
keys on 2026-08-04. The mark is kept because the history is what makes `scripts/check_models.py`
legible; the rows themselves are correct and the guard exits 0 over them, re-verified 2026-08-07.

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

⚑ **2026-08-16 — the "Claude Opus 4.8" in the five rows above is a statement of intent, not an
observation of what runs.** All nine definitions declare `model: opus`. That frontmatter key
selects a **tier, not a version** — `scripts/check_models.py`'s own docstring says so ("a card
naming a version is describing a choice the frontmatter does not itself pin"). The runtime
resolves the alias to the platform's current Opus. So for `systems-researcher`, `editor`,
`analytics-officer`, `obsidian-archivist` and `integrity-officer` — the five rows reading
Claude Opus 4.8 — nothing in the repository makes 4.8 the model that actually serves the seat.

This is now observed twice, from two seats, and is no longer an inference:

- [[integrity-officer]] self-reported `REQUESTED claude-opus-4-8 → ACTUAL claude-opus-5` on
  **2026-08-12** (`analytics/daily-research/2026-08-12.md:750`), **2026-08-14**
  (`:576`), **2026-08-15** (`:693`) and **2026-08-16** (`:731`), each time unasked. The
  2026-08-14 council recorded the gap as escalation-grade; `analytics/council-log.md:23`
  carries it as "second consecutive day"; the 08-16 record calls it "owed a third time".
- **[[obsidian-archivist]] — this seat — confirmed it first-person on 2026-08-16.** The session
  runtime reports `session_context.model` = `claude-opus-5` and `last_served_model` =
  `claude-opus-5`, against `agents/obsidian-archivist.md:14`, which pins `claude-opus-4-8`.
  **REQUESTED `claude-opus-4-8` → ACTUAL `claude-opus-5`.** Observed, not assumed.

**`scripts/check_models.py` cannot catch this and is not failing.** It exits 0 over twelve cards
because it compares three *declarations* to each other; it has no view of a runtime. Its docstring
states the limit honestly ("It cannot tell you a seat is running on the model it *should*"). The
guard is sound; the coverage gap is real. `src/models.py:18` requires a runtime fallback be
recorded in `HANDOFF.md` via `record_fallback()`; that function's only caller is
`src/research_brief.py:161`, a path no council seat enters, and `HANDOFF.md` has no
"Model runtime fallbacks" section — verified 2026-08-16.

**The rows are left as written, deliberately.** They record the operator's directive, which is
what the registry is for, and rewriting them to "Claude Opus 5" would silently ratify a
substitution nobody authorised. What was missing was the qualification, not a different number.
Escalated to Emory: the five `.claude/agents/` definitions, the five `workflow.json` cards and
`src/models.py` are all outside this seat's authority.

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

**Re-measured 2026-08-09, before and after this session's vault edits.** Before:
**125 notes, 253 edges, 0 orphans, 9 WARNs, 15 planned edits.** After: **127 notes, 265 edges,
0 orphans, 11 WARNs, 17 planned edits**, hub degrees `Evidence Ledger=69, Council=27,
Workflow=11, Research Question=8, Digest Archive=7, 00 - Project Map=3`. Both numbers are given
because a single post-edit measurement would attribute this seat's own additions to the rest of
the vault.

**The +2 notes decompose, and only one of them is this seat's.**
`analytics/vault-sessions/2026-08-09.md` is this pass's own record. The other,
`working/claude-chat-final-review-prompt-2026-08-09.md`, appeared **mid-pass** — timestamped
11:47, untracked, not gitignored, written by **another process** while this reconciliation was
running, and out of bounds for this seat. It is named because the before/after convention only
tells the truth if concurrent writes are named; read as vault work it would inflate this seat's
footprint by a note and a planned edit.

**Both new WARNs are this seat's own, and both were predicted.** The 2026-08-08 entry recorded
eight and said "so that the ninth WARN, whenever it appears, is legible as new." The ninth
arrived with `analytics/vault-sessions/2026-08-08.md`; the **tenth** is [[Claim Map]], pushed
over the cap (5 direct links) by the **C16** row added this session; the **eleventh** is this
session's own record (8 links), for the same reason the 08-08 record crossed it — a session note
cites the seats it audited. [[systems-designer]] also rose 5 → 6. None is drift: each exceeds
the cap by pointing at other seats' notes, which is the linkage the vault is for. **A session
record will cross the cap every time**, which is now stated as a standing expectation rather
than rediscovered each month.

Expected-WARN set as it now stands — **eleven**, up from eight on 2026-08-08 and four on
2026-08-04. The three added since are marked:

| WARN | Direct links (2026-08-09 pre → post) | Reading |
|---|---|---|
| `agents/Agent Registry.md` | 12 → 12 | Expected — index note (11 on 08-04) |
| [[Workflow Threads]] | 10 → 10 | Expected — index note |
| [[Project Change Log]] | 9 → 9 | Expected — index note; crossed the cap by accumulating wiki-link citations, which is the note doing its job |
| `think-tank/multi-agent/_MOC.md` | 8 → 8 | Expected — predates the agent-memory area |
| [[obsidian-archivist]] | 8 → 8 | Known, carried since 2026-08-04 |
| [[integrity-officer]] | 5 → 5 | Carried since 2026-08-08 |
| [[site-experience]] | 5 → 5 | Carried since 2026-08-08 |
| [[systems-designer]] | 5 → **6** | Carried since 2026-08-08; rose this session |
| `analytics/vault-sessions/2026-08-08.md` | 5 → 5 | **The predicted ninth.** A session record citing the seats it audited |
| [[Claim Map]] | — → **5** | **New this session — the predicted tenth.** Pushed over by the **C16** row |
| `analytics/vault-sessions/2026-08-09.md` | — → **8** | **New this session — the eleventh.** This pass's own record. Session records cross the cap by construction |

The 2026-07-31 rule — *any WARN naming a per-agent note is drift* — is broken by **four** seat
notes, unchanged in kind since 2026-08-08. The honest reading is that the rule was written for a
vault where seat notes were short, and the notes have since become the place where a seat's
cross-seat history is recorded; each exceeds the cap by pointing at other seats' notes, which is
the linkage the vault is for. **The cap is not raised here** — that is a
`scripts/build_graph.py` change and belongs to [[systems-designer]]. The set is kept named so
that the **eleventh** WARN, whenever it appears, is legible as new; the convention has now
called its own next two exceptions correctly.

> **A finding this seat produced by walking into the trap it maintains.** A first draft of the
> row above wrote the doubled-square-bracket link syntax inside a backtick code span, to name
> the thing being counted. The next `--dry-run` reported a **new broken link** from this note
> to a note named `…`. `scripts/build_graph.py` scans link syntax **inside inline code spans**;
> it strips fenced blocks but not backticks. This is a sibling of the open C8 defect
> ([[Workflow Threads]]), which concerns markers inside prose, and it is worth recording
> separately: **you cannot quote wiki-link syntax anywhere in this vault without minting a
> broken link.** The draft was rewritten to say "wiki-link citations" in words. Any future
> note explaining the link syntax must do the same until the scanner skips inline code.

✔ **The `Project Machinery` broken link is gone.** The 2026-08-04 run reported one broken link
from `agents/obsidian-archivist.md` to a note of that name, which never existed. The 2026-08-08
run's broken-link list is `think-tank/README.md`, `think-tank/multi-agent/20 - Options -
frameworks.md`, and `think-tank/website/interactive-upgrade-spec.md` — none of them in the
agent-memory area. The reference survives in that note only as prose recording that the note
was never created, which is the correct disposition.

**Seventeen notes are awaiting their managed block**, against thirteen on 2026-08-08 and eleven
on 2026-08-04. `build_graph --dry-run` on 2026-08-09 plans edits to:
`BOUNDED_CHANGE_PROTOCOL.md`, **`agents/Claim Map.md`**,
`working/benavides-comment-replies-2026-08-08.md`,
`working/claude-chat-final-review-prompt-2026-08-08.md`,
`working/claude-chat-final-review-prompt-2026-08-09.md`, `prompts/carrying_span_rule.md`,
`lit-review/BIBLIOGRAPHY_TEMPLATE.md`, `analytics/instrument-map-2026-08-08.md`,
`analytics/retrospective-audit-2026-08-08.md`, `analytics/session-manifest-2026-08-09.md`,
`analytics/state-space-resolution-2026-08-09.md`,
`analytics/vault-sessions/2026-08-04-council.md`,
`analytics/vault-sessions/2026-08-08.md`, `analytics/vault-sessions/2026-08-09.md`,
`analytics/daily-research/2026-08-06.md`, `analytics/locked_set/RETRIEVAL_LEDGER.md`,
`analytics/locked_set/SCHEMA.md`. **`agents/Claim Map.md` is still the one that should sting** —
the map has been in the vault since 2026-08-04, has never carried its block, and is therefore
invisible to the graph while being the note most often cited by the others.

**The write-mode run was NOT performed for the third consecutive session, and the cause is
structural rather than circumstantial.** Fourteen of the seventeen planned files are out of
bounds for this pass — `working/`, `prompts/`, `lit-review/`, `analytics/locked_set/` and the
session's own analytics artifacts — and `build_graph.py` offers **no path filter**: it is
whole-vault or nothing. **A managed block is never hand-written**, so no partial run is lawful
either.

**This is now escalated as a defect in `scripts/build_graph.py` rather than carried as a
backlog.** The reasoning: every archivist session operates under scope boundaries, and a tool
that can only run when *no* file in the vault is out of bounds is a tool that can never run.
Three sessions is enough evidence that the backlog will not clear itself. A `--paths` filter (or
a `--only-missing` mode restricted to an explicit list) would make the run lawful in any session.
**Owner:** [[systems-designer]], on Emory's go-ahead.

**Re-measured 2026-08-07 at `7c08dcf`.** `python3 scripts/build_graph.py --dry-run` reports
**117 notes, 231 edges, 0 orphans, 7 files awaiting a managed block, and 7 WARNs.** Three of
the seven WARNs are new since 2026-08-04, and none of them is drift in the sense the
2026-07-31 rule meant:

| WARN | Direct links / cap 4 | Reading |
|---|---|---|
| `agents/Agent Registry.md` | 12 | Expected — index note, and the count rose from 11 as rows were added |
| `agents/Workflow Threads.md` | 9 | Expected — index note |
| `agents/Project Change Log.md` | 8 | **New** — index note; it was under the cap on 2026-08-04 and is not now |
| `agents/obsidian-archivist.md` | 6 | Carried from 2026-08-04 |
| `agents/integrity-officer.md` | 5 | **New** |
| `agents/systems-designer.md` | 5 | **New** |
| `think-tank/multi-agent/_MOC.md` | 8 | Predates the agent-memory area |

The 2026-07-31 rule — *any WARN naming a per-agent note is drift* — is now false three times
over and is **retired here** rather than left to be re-discovered. The honest replacement: the
cap keeps ordinary spokes from becoming hubs, and three seat notes have crossed it because
their adopted-rules sections grew. That is a cap-versus-purpose question for the graph
machinery, not a defect in the notes, and it is escalated in [[Workflow Threads]] rather than
answered by deleting links a reader needs.

✔ **Closed 2026-08-07.** The broken link from `agents/obsidian-archivist.md` to a note named
`Project Machinery` — recorded here on 2026-08-04 — no longer appears. The dry run's
"links to nonexistent notes" list names only three files, all under `think-tank/`, and none
under `agents/`. The dead link was removed in the 2026-08-04 change set; this note carried it
as live for three days.

**Seven notes are awaiting their managed block, not eleven.** The 2026-08-07 dry run plans
edits to `BOUNDED_CHANGE_PROTOCOL.md`, `agents/Claim Map.md`, `prompts/carrying_span_rule.md`,
`lit-review/BIBLIOGRAPHY_TEMPLATE.md`, `analytics/daily-research/2026-08-06.md`,
`analytics/daily-research/2026-08-07.md`, and `analytics/vault-sessions/2026-08-04-council.md`.
Four of the eleven files listed on 2026-08-04 have since received their block through other
change sets; three of today's seven are new files.

**Why the run keeps not happening, stated as a structural fact rather than a preference.**
Four of the seven files — `BOUNDED_CHANGE_PROTOCOL.md`, `prompts/carrying_span_rule.md`,
`lit-review/BIBLIOGRAPHY_TEMPLATE.md`, and (on any future run) anything under `think-tank/` —
sit **outside the archivist's self-merge authority**, which covers `analytics/`, `agents/`,
`moc/` and `HANDOFF.md`. `build_graph` is a whole-vault operation with no path filter, so the
archivist can never land a full run under its own authority: every run needs Emory or a seat
with wider paths. That is why the pending list has been carried forward across four sessions
instead of being discharged, and it is escalated in [[Workflow Threads]] C12.

The notes under `agents/` carry their managed `Map:` blocks as of 2026-07-31, when
`build_graph` was first run over this area after the `807666f` scan-boundary fix. Those
blocks are generated: they are never hand-edited, and a run must leave them byte-identical.

## Maintenance

When any agent's prompt, model, or contract changes, this table and the corresponding note
change in the same commit, and the change is dated and cited in [[Project Change Log]].

## Adopted method rules by seat

Rules the council adopted in session that are now part of a seat's working context. Full
statements live in the seat's own note.

> **Qualification added 2026-08-13, because the sentence above overstates what is true.** "Part
> of a seat's working context" describes where these rules are *recorded*, not where the seat
> *reads*. A seat's read path is its `.claude/agents/` definition plus the `prompts/` files that
> definition enumerates, and eight of the nine definitions never name the seat's own note. Of the
> [[research-analyst]] rules below, only the Carrying-Span Rule is inside that seat's read path,
> and only because it was given its own file in `prompts/`. The [[integrity-officer]] rows are
> the exception that proves it: that seat's definition points at its note by name. Recorded as
> [[Workflow Threads]] **D5**; the remedy is a contract edit and therefore Emory's.

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
| [[systems-researcher]] · [[analytics-officer]] | **Path-tagging** — every claim about the instrument carries `[keyword-path]`, `[model-path]` or `[mixed]`; "a claim that cannot be path-tagged is not asserted." Adopted because the costliest error of the R1 session was reasoning from one path's arithmetic about the other path's output | 2026-08-08 | `analytics/instrument-map-2026-08-08.md:3-7` (uncommitted, `fix/restore-council-label`) |
| [[analytics-officer]] | **Re-derive denominators from the files, never from a council record** — two records disagreed with the archive, and the audit reports 14 files / 13 URLs / 12 matters rather than one number | 2026-08-08 | `analytics/retrospective-audit-2026-08-08.md:3-19` (uncommitted) |
| [[integrity-officer]] · [[research-editor]] | **Humanizer output is fail-closed** — a rewriting pass is run with every quotation, citation and pinpoint sentinel-masked, and its output is rejected outright on fabricated quotation, flipped negation, hallucinated rule, or sentinel destruction. On 2026-08-08: 7 substantive replies run, **2 passed and were repaired, 5 rejected, 2 exempt**. **Round 2, 2026-08-09**, on the parity-repair revisions: 3 passages, **0 adopted** — 1 exempt *by construction* (masked, it is a near-pure sentinel chain with nothing to rewrite), 2 rejected at the gate (one dropped two sentences and turned the court's opinions into "the author's opinions"; one destroyed a sentinel). **Cumulative: 10 run, 2 adopted** | 2026-08-09 | `working/benavides-comment-replies-2026-08-08.md:5-6` (uncommitted) |
| [[research-analyst]] | **No item enters the locked validation set on a memo's authority** — primary retrieval only, recorded as externally gated; the set is created **empty of items on purpose** | 2026-08-08 | `analytics/locked_set/SCHEMA.md:1-11`, `analytics/locked_set/RETRIEVAL_LEDGER.md` (uncommitted) |
| [[integrity-officer]] | Taxonomy entry 25 — mutable-reduction citation; every reduction citation carries a commit sha | 2026-08-05 | `3ff5498` / `2026-08-05.md:616`, `:976` |
| [[research-analyst]] | `find` selects a position, not a proposition (house rule 2) | 2026-08-05 | `3ff5498` / `2026-08-05.md:977` |
| [[research-analyst]] | A mis-anchored row is not a null; a PDF `find_matched: false` is a gate artefact; a false URL is a control | 2026-08-05 | `3ff5498` / `2026-08-05.md:978-980` |
| [[council-chairman]] | Before Part 1 asserts anything about the repository, **run the command and paste the output** (fourth iteration) | 2026-08-05 | `3ff5498` / `2026-08-05.md:1012`, `:1026` |
| [[council-chairman]] | Intermediate council part-commits carry `[skip ci]`; the final commit does not — adopted as a stopgap with its own defect stated | 2026-08-05 | `3ff5498` / `2026-08-05.md:981` |
| [[integrity-officer]] | Taxonomy entry 26 — tautological instrument check | 2026-08-06 | `aa48406` / `2026-08-06.md:919` |
| [[integrity-officer]] | Taxonomy entry 27 — scope-mixed screen | 2026-08-06 | `aa48406` / `2026-08-06.md:940` |
| [[council-chairman]] | A grep establishes absence from the repository, never from the project | 2026-08-06 | `aa48406` / `2026-08-06.md:943` |
| [[council-chairman]] | Every relay null carries the entity-blind qualification alongside attribute-stripping | 2026-08-06 | `aa48406` / `2026-08-06.md:955` |
| [[council-chairman]] | Before acting on any instruction that names a file and a line, **open the line** — extended from the chairman to **every seat** | 2026-08-07 | `7adfd68` / `2026-08-07.md:968` |
| [[integrity-officer]] | Taxonomy entry 27 ⚠ — manufactured residual; **same number as scope-mixed screen** | 2026-08-07 | `7adfd68` / `2026-08-07.md:975` |
| [[council-chairman]] | Elapsed intervals are truncated, never rounded | 2026-08-07 | `7adfd68` / `2026-08-07.md:984` |
| [[research-analyst]] | `find_matched` has three states, not two — the third is *asked nothing* | 2026-08-07 | `7adfd68` / `2026-08-07.md:1000` |
| [[integrity-officer]] | A zero-hit screen is not absence until the synonym is tried | 2026-08-07 | `7adfd68` / `2026-08-07.md:1029` |

The taxonomy's canonical statement is the table in [[integrity-officer]], one
citation per entry. It exists because the in-session recitation of the taxonomy was four to
thirteen entries short on 2026-08-02, 08-03 and 08-04 — the seat is directed to read the
table rather than restate the list from memory.

## Change log

- **2026-08-25** — Registry re-audited against `ad66a96` (`main`, clean tree, complete
  804-commit history after `git fetch --unshallow`; the container's clone arrived shallow a
  third consecutive time, at 188 commits). **No roster change and no contract change:**
  `git log c4f6825..HEAD -- .claude/agents/ prompts/ src/models.py` returns **no commit** across
  56 commits; `src/models.py` is unchanged (`CHAIRMAN_MODEL`/`HEAVY_MODEL` `claude-opus-5`,
  `UTILITY_MODEL`/`FALLBACK_MODEL` `claude-opus-4-8`, `DIGEST_CLASSIFIER_MODEL`
  `claude-haiku-4-5-20251001`); `check_models.py` exits 0 over twelve cards, which licenses only
  the claim that three declarations agree with one another. **D6 is at day thirteen**, and this
  seat's own runtime was queried for the third time: `session_context.model` and
  `last_served_model` both `claude-opus-5`, against `.claude/agents/obsidian-archivist.md:24`,
  which states Claude Opus 4.8. The officer continued to report it unasked at
  `analytics/daily-research/2026-08-23.md:723` and `2026-08-25.md:791`. The qualification block
  under the roster stands and **the roster rows and Model lines are again left unchanged**, for
  the reason given on 2026-08-16: rewriting them would ratify a substitution nobody authorised.
  **D5 unchanged after twelve days** — re-tested by script, eight of nine definitions still
  never name their seat's own vault note; [[integrity-officer]] remains the one that does.
  **D8 unchanged** — both "Zero-cost" bindings live. **D9 opened**:
  `scripts/check_currency.py:30-32` documents a bare-sha commit-citation check that
  `:184` does not implement, which is why an unresolvable citation on this seat's own
  `agents/Project Change Log.md:1021` passed the guard for a month. All contract items are
  Emory's; escalated, not edited. *Audited against `ad66a96`; paths: `.claude/agents/`,
  `prompts/`, `src/models.py`, `agents/`, `views/isds-workflow-3d/workflow.json`,
  `scripts/check_models.py`, `scripts/check_currency.py`, `HANDOFF.md`.*
- **2026-08-22** — Registry re-audited against `c4f6825` (`main`, clean tree, complete
  748-commit history after `git fetch --unshallow`; the container's clone arrived shallow again,
  at 196 commits). **No roster change:** `git log d997c32..HEAD -- .claude/agents/ prompts/
  src/models.py` returns **no commit**, `src/models.py` is unchanged, and `check_models.py`
  exits 0 over twelve cards — which, per the rule adopted 2026-08-16, licenses only the claim
  that three declarations agree with one another. **D6 is at day ten and is now the finding.**
  [[integrity-officer]] has self-reported `REQUESTED claude-opus-4-8 → ACTUAL claude-opus-5` on
  ten consecutive days, six of them since the last registry pass:
  `analytics/daily-research/2026-08-17.md:719`, `2026-08-18.md`, `2026-08-19.md:1148`,
  `2026-08-20.md:1113`, `2026-08-21.md:1024`, `2026-08-22.md:1080`. The qualification block
  under the roster stands and the rows are again left unchanged, for the reason given on
  2026-08-16. **D5 unchanged after nine days** — re-tested this session, eight of nine
  definitions still never name their seat's note; [[integrity-officer]] remains the one that
  does. **D8 opened**: `.claude/agents/site-experience.md:20` carries a second, previously
  unrecorded "Zero-cost" binding alongside `systems-designer.md:17`. All three are Emory's;
  escalated, not edited. *Audited against `c4f6825`; paths: `.claude/agents/`, `prompts/`,
  `src/models.py`, `agents/`, `views/isds-workflow-3d/workflow.json`,
  `scripts/check_models.py`, `HANDOFF.md`.*
- **2026-08-16** — Registry re-audited against `d997c32` (`main`, clean tree, complete history —
  621 commits after `git fetch --unshallow`; the container's clone arrived shallow again at 201
  commits, and a shallow clone misreported the verification ledger's last-touching commit as
  `cf7d99b` when it is `8891c21`). **No roster change and no model drift in the bookkeeping
  sense:** `git log 8ea2ee1..HEAD -- .claude/agents/ prompts/ src/models.py` returns **no
  commit**, and `check_models.py` exits 0 over twelve cards. **The finding is that the
  bookkeeping is not the fact.** All nine definitions declare `model: opus`, a tier alias; the
  five roster rows reading "Claude Opus 4.8" assert a version nothing in the repository pins.
  Confirmed by observation from two seats — [[integrity-officer]] four times unasked, and this
  seat's own runtime reporting `claude-opus-5` on 2026-08-16. A qualification block now stands
  under the roster table; the rows themselves are unchanged, because they record the operator's
  directive and rewriting them would ratify a substitution nobody authorised. **D5 unchanged**
  after three days: eight of nine definitions still never name their seat's note, re-tested this
  session. *Audited against `d997c32`; paths: `.claude/agents/`, `prompts/`, `src/models.py`,
  `agents/`, `views/isds-workflow-3d/workflow.json`, `scripts/check_models.py`, `HANDOFF.md`.*
- **2026-08-13** — Registry re-audited against `8ea2ee1` (`main`, clean tree).
  `git log 667772c..HEAD -- .claude/agents/ prompts/ src/models.py` returns **no commit**;
  **no roster change, and no model drift** — `check_models.py` exits 0 over twelve cards and
  `src/models.py` is unchanged. The finding is not in the roster but beside it: the
  "Adopted method rules by seat" section says those rules are "part of a seat's working
  context", which describes where they are recorded and not where the seat reads. Eight of nine
  definitions never name their seat's note; ten of [[research-analyst]]'s eleven rules and all
  four `label: 1` rows of `scripts/holdout_set.json` are outside that seat's read path. A
  qualification block now says so at the head of the section, and the finding is escalated to
  Emory as [[Workflow Threads]] **D5** because `.claude/agents/` is a contract surface.
  Also repaired: a stray blank line had split the adopted-rules table into two fragments from
  the `locked_set` row onward, so the last thirteen rows rendered without headers.
  *Audited against `8ea2ee1`; paths: `.claude/agents/`, `prompts/`, `src/models.py`,
  `agents/`, `scripts/holdout_set.json`, `views/isds-workflow-3d/workflow.json`.*
- **2026-08-09** — Registry re-audited against `2686422` plus the uncommitted working trees of
  the 2026-08-08 and 2026-08-09 sessions on `fix/restore-council-label`. **No roster change,
  and for the second consecutive session that is itself the finding:** a day that added
  `src/rings.py`, `src/classify_v2.py`, `src/triage.py`, `src/headline_lane.py`, two publication
  gates, a CI workflow and two guard scripts changed **no agent's model, prompt binding or
  contract**. `.claude/agents/` and `prompts/` are untouched in `git status`. Recorded:
  (a) the `.claude/agents/systems-designer.md:17` **zero-cost** line remains falsified and
  remains **Emory's** to edit — second consecutive session escalated;
  (b) the graph re-measured before and after — **125 → 127 notes, 253 → 265 edges, 9 → 11
  WARNs**, 0 orphans throughout — with both new WARNs ([[Claim Map]], pushed over by the new
  **C16** row, and this pass's own session record) **correctly predicted** by the expected set
  adopted on 08-08;
  (c) a note appeared **mid-pass from another process**
  (`working/claude-chat-final-review-prompt-2026-08-09.md`, 11:47) and is named so it is not
  counted as vault work;
  (d) the managed-block backlog grew to **seventeen** and write mode was blocked a **third**
  time — now escalated as a `scripts/build_graph.py` defect (no path filter) rather than
  re-recorded as a backlog;
  (e) the humanizer rule row extended with **round 2** (3 passages, 0 adopted; cumulative 10 run
  / 2 adopted);
  (f) the click-through map **re-verified clean** — v2.2, 30 nodes, 44 edges, all ten targets
  resolve, `systems-designer` at machine row 9 agreeing with its seat note for the first time
  since the 08-08 correction.
  Seat notes updated in the same change set: [[systems-designer]] (D/E, F, G built and each off
  by default; the `check_site_sync` deviation of record; the chart gap), [[research-analyst]]
  (H&H closed by retrieval, and the two claims the retrieval *corrected*), [[integrity-officer]]
  (Walter round 2), [[site-experience]] (homepage repaired, then stale again within the day),
  [[obsidian-archivist]] (audit slice). Session record:
  `analytics/vault-sessions/2026-08-09.md`.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `.claude/agents/`, `prompts/`, `agents/`, `moc/`, `views/isds-workflow-3d/workflow.json`,
  `src/`, `scripts/`, `.github/workflows/`, `analytics/`, `seeds/`, `working/`, `HANDOFF.md`,
  `METHODOLOGY.md`, `README.md`, `PLAN.md`, `fingerprint.yaml`, `STATE_OF_THE_ANSWER.md`.*
- **2026-08-08** — Registry re-audited against `2686422` plus the uncommitted master-prompt
  repair session on `fix/restore-council-label`. **No roster change**, and that is the
  finding: `git log 373cce6..HEAD -- .claude/agents/ prompts/` is empty and `git status`
  shows nothing modified under either path, so a session that added ~1,400 lines of code,
  three guards and nine archive corrections changed **no agent's contract**. Recorded:
  (a) the `.claude/agents/systems-designer.md:17` **zero-cost** constraint is falsified by
  the day's classifier finding and is escalated to Emory as a contract change, while its
  vault-note twin is corrected; (b) `build_graph --dry-run` now prints **seven** WARNs, not
  four — three of them per-agent notes, which retires the 2026-07-31 "any per-agent WARN is
  drift" rule and replaces it with a named expected set; (c) the `Project Machinery` broken
  link is **gone**; (d) the managed-block backlog is **twelve** notes and now includes
  [[Claim Map]], with the write-mode run blocked on out-of-bounds files rather than deferred
  by choice. Seat notes updated in the same change set: [[systems-designer]] (Phase 0/1/H,
  the root-cause fix, machine row **9** not 7, zero-cost), [[research-analyst]] (Vanda
  retrieval and the two withdrawn claim classes), [[integrity-officer]] (five fail-closed
  rejections and the ring-at-25 substantive review), [[council-chairman]] (a 2026-08-08
  ruling overcounted by one, corrected from the files), [[site-experience]] (the routed site
  overclaim), [[obsidian-archivist]].
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `.claude/agents/`, `prompts/`, `src/`, `scripts/`, `analytics/`, `agents/`,
  `views/isds-workflow-3d/workflow.json`, `README.md`, `METHODOLOGY.md`.*

- **2026-08-07** — Fourteen adopted rules from the 2026-08-05, 08-06 and 08-07 sessions added to
  the table above, and each landed in the seat note that will actually be read. **The registry's
  own 2026-08-06 paragraph was found to carry a false commit citation** — `373cce6` credited with
  a `prompts/research_analyst.txt` fix that was `9efafb0`'s — and is corrected in place.
  Graph measurements re-run rather than restated: 117 notes / 231 edges / 0 orphans / 7 WARNs /
  7 pending managed blocks, against the 4 WARNs and 11 pending blocks this note carried since
  2026-08-04. The `Project Machinery` broken link is confirmed closed. The 2026-07-31 rule that
  any WARN naming a per-agent note is drift is **retired**, being false three times over.
  `scripts/check_models.py` exits 0; the ⚠ marks on the two builder-seat card rows are retained
  as historical markers with the closure they point to stated at the row.
  *Audited against `7c08dcf`; paths: `.claude/agents/`, `prompts/`, `src/models.py`,
  `views/isds-workflow-3d/workflow.json`, `agents/`.*
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
