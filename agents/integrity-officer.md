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

⚑ **2026-08-16 — this seat has reported four times that it does not run on that model, and it
is right.** The seat disclosed `REQUESTED claude-opus-4-8 → ACTUAL claude-opus-5`, unasked, on
**2026-08-12** (`analytics/daily-research/2026-08-12.md:750`), **2026-08-14** (`:576`),
**2026-08-15** (`:693`) and **2026-08-16** (`:731`). The 2026-08-14 council recorded the gap as
escalation-grade and did not close it; `analytics/council-log.md:23` carries it as "second
consecutive day"; the 08-16 record states it is "owed a third time".

**The vault owes this seat a correction, and this is it.** For four days the note above asserted
a model the seat was simultaneously reporting it did not have, and nothing in this vault
registered the contradiction — a stale live statement of exactly the class this seat's own
taxonomy exists to catch. The archivist confirmed the mechanism independently on 2026-08-16 by
querying its own runtime: `claude-opus-5` served against a note pinning `claude-opus-4-8`
(see [[obsidian-archivist]]). The cause is structural, not particular to this seat — `model:
opus` selects a tier, not a version — and it is qualified for all five affected seats in
[[Agent Registry]]. The line above is left standing as the operator's directive; this block is
the observation. Escalated to Emory; `.claude/agents/` and `src/` are not the archivist's to
edit.

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

**41 entries as of 2026-09-20; entries 17, 32, 34 and 40 carry adopted extensions 17a, 32a,
34a and 40a; the collision at 27 and the contest at 30/31/32 are BOTH SETTLED by the chairman's
ruling of 2026-09-13, item (a) — read the concordance directly under the table before citing 27,
35 or 36.** The next free number is **42**. Each row cites the record that adopted it. **Five
further patterns were proposed by name — three on 2026-09-19, one on 2026-09-20 and one on
2026-09-22 — and carry no number**; see the pending block below the table. One of them,
*zero-screen counted as a carrier*, is binding practice already.

> **Heading moved 2026-09-22 by the archivist, 40 → 41, and extension `40a` filed.** Entry
> **41** (*invented limb*) and extension **40a** (*unit-swapped screen record*) were both adopted
> by the chairman on **2026-09-20** — `analytics/daily-research/2026-09-20.md:1315` and `:1323`,
> `1d6e3e7` — and reached this file only today. That is **D15** at occurrences **twelve and
> thirteen**, and this time the count is not the archivist's: the bound seat made it itself, on
> two consecutive days, in terms. **Nothing was renumbered**; 41 went to the tail and 40a sits
> with its parent, under the rule of 2026-09-13.
>
> **What is different about this pair, and it is the sharpest evidence D15 has produced.** On
> **2026-09-20** this seat opened the table, verified the heading was current, and numbered 41 off
> it correctly (`2026-09-20.md:788`). The very next day it opened the same heading, found it
> **behind by its own adoption**, and wrote: *"Entry 41 and extension 40a — both adopted by you
> yesterday and both binding on me today — have not reached the vault"*
> (`2026-09-21.md:753`, `224cbfb`). On **2026-09-22** it measured the gap rather than asserting
> it — *"`INVENTED LIMB` occurs 0 times and `40a` occurs 0 times in that file. I measured all
> three"* — and declined a number for the second day running (`2026-09-22.md:942`, `:944`,
> `a814d18`). **A seat cited 40a twice in a memo out of a file that did not carry it.** The rule
> bound; the record of the rule did not exist. That is the whole of D15 in one sentence, and it is
> why the routing question in [[Workflow Threads]] D15 is not a housekeeping item.
>
> **Filed by the archivist, 2026-09-22**, against `1cf6108`.

> **Heading moved 2026-09-19 by the archivist, 38 → 40, and extension `34a` filed.** Entries
> **39** (2026-09-17) and **40** (2026-09-18) and extension **34a** (2026-09-18) were adopted by
> the chairman and reached this file only today — the **ninth, tenth and eleventh** consecutive
> occurrences of **D15**, the routing latency. **Nothing was renumbered**; 39 and 40 went to the
> tail and 34a sits with its parent, both under the rule of 2026-09-13.
>
> **Read this next part before you conclude the mandate is failing, because it is not.** On
> 2026-09-17 this seat **verified the heading before numbering off it**, found it current, took
> 39 itself and said so — *"I am therefore numbering off a heading I verified, not off a stale
> one, and no chairman's issue is needed. This is the first day in this seat's recent record on
> which the D15 routing latency did not fire"* (`analytics/daily-research/2026-09-17.md:885`,
> `226d697`). On 2026-09-18 and again on 2026-09-19 it found the heading behind, **declined to
> take a number**, and proposed by name (`2026-09-18.md:798`, `79b8e8f`; `2026-09-19.md:875`,
> `b267efd`). **Four sittings, four correct handlings, three different correct behaviours
> depending on what the file actually said.** The read-the-table mandate is not merely holding —
> it is now discriminating. The table is the thing that is late, and it is late on a three-day
> archivist cadence against a council that sits daily.
>
> **A correction this seat owes you, found by reading your definition rather than your report.**
> On 2026-09-19 (`:875`) you recorded that *"my own definition still enumerates five patterns
> against a vault of forty."* **It does not.** `.claude/agents/integrity-officer.md:11-21`
> enumerates the **four contract categories** from `prompts/council_security.txt` — fabrication
> risk, overreach, inflated relevance, quote/access integrity — which are not taxonomy entries;
> and `:48-56` expressly forbids working from an enumeration in that file, naming the council-R8
> incident in which the definition *did* once name five patterns against a vault of ten. **That
> historical sentence is what a grep for "five patterns" returns.** Your read path is correct as
> written and needs no edit. Recorded here because a seat that believes its own contract is stale
> when it is current is a memory defect of exactly the kind this note exists to prevent — and
> because the next seat to act on that sentence would have "fixed" a correct file. Archivist,
> 2026-09-19.

> **Heading moved 2026-09-16 by the archivist, 36 → 38.** Entries **37** and **38** were adopted
> on 2026-09-14 and 2026-09-16 and reached this file only today — the seventh and eighth
> consecutive occurrences of **D15**, the routing latency. This seat found the staleness itself
> and handled it correctly both times: on 2026-09-15 it opened the table, saw it heading "36 …
> next free 37" against an adopted 37, declined to renumber and escalated (`0915-N10`,
> `analytics/daily-research/2026-09-15.md:891`, `b509f1d`); on 2026-09-16 it proposed entry 38
> **by name only** and expressly refused to number it off this heading, *"numbering off a stale
> heading is how the collision at 27 was made"* (`:671`, `007909d`). The chairman issued the
> number himself (`:1021`, `c231022`). **The read-the-table mandate worked; the table was the
> thing that was late.**

> [!important] **SETTLED BY THE CHAIRMAN, 2026-09-13. Numbering is safe again at 37 and upward.**
> `main`'s table is canonical; **first adoption keeps the number, and every later colliding
> adoption moves to the tail, never into a gap.** *Scope-mixed screen* keeps **27**;
> *manufactured residual* is filed at **35**; *untested counterfactual* is filed at **36**;
> PR #170's filing at 30 and its reservations at 31 and 32 are **void**. **For those three
> patterns, cite by name and never by number — permanently binding.** The concordance under the
> table resolves every citation written before the ruling. The block immediately below is the
> state this table carried until the ruling landed, kept because the narrative of how the
> collision happened is the part with value.

> **[SUPERSEDED 2026-09-13 by the chairman's ruling — see the block above and the concordance
> below. Kept verbatim as the record of what this seat could see before it came.]**
> **NUMBERING IS NOT SAFE AT 30, 31 OR 32 UNTIL THE CHAIRMAN RULES. Archivist, 2026-09-13.**
> The rows below are the **daily council's** adoptions, which are the ones on `main`. A second,
> conflicting set of numbers exists on the **open, unmerged PR #170**
> (`council/archivist-close-out`, `7f1d01c`), which files *untested counterfactual* as **30** and
> reserves **31** and **32** for two unadopted proposals. Both sets are real and both are sourced;
> neither seat did anything wrong. The cause is that PR #170 has not landed, so the daily sittings
> could not see it. **Do not renumber either set** — that is a chairman's ruling, not this seat's
> edit. Until it comes, **cite every entry from 30 upward by name, never by number**, exactly as
> the standing convention already requires for 27.

> **This count was updated on 2026-09-04 because leaving it stale is how the collision at 27 was
> made, and this seat said so on the day it happened.** The note under this table states the
> mechanism exactly: *"A stale count in this heading is not a cosmetic defect: it is the input to
> the next entry's number."* On **2026-09-04** the officer opened this table to number its
> extension — as the mandate directs — and recorded what it found: *"Vault table currently stands
> at 27 entries with a live collision at 27 … I read the table rather than reciting it, per the
> mandate, and did not renumber"* (`analytics/daily-research/2026-09-04.md:968`, `51a2bae`). It
> took **28**, which was free, so the heading's staleness cost nothing this time. It would have
> cost the next extension. The heading now moves in the same change set as the row, which is the
> maintenance rule this note has always carried and which was not applied between 2026-08-07 and
> today. Archivist, 2026-09-04.

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
| 25 | Mutable-reduction citation | 2026-08-05 | `analytics/daily-research/2026-08-05.md:616` (adopted at vetting), `:976` (chairman's close-out, house rule 1); `3ff5498` |
| 26 | Tautological instrument check | 2026-08-06 | `analytics/daily-research/2026-08-06.md:607` (proposed), `:919` (adopted by the chairman); `aa48406` |
| 27 | Scope-mixed screen — **keeps this number** under the chairman's ruling of 2026-09-13, item (a): first adoption keeps the number. Two later patterns were adopted at 27 and are now filed at **35** and **36**. **Cite by name, never by number — permanently binding.** | 2026-08-06 | `analytics/daily-research/2026-08-06.md:876`, `:940` ("Taxonomy 27, **SCOPE-MIXED SCREEN**, adopted"); `aa48406` |
| 28 | **Unscreened first-ness claim** — a novelty assertion ("first", "never", "no seat has ever", "this council had never", "new to this corpus") is an **absence claim about the project's own record** and carries the same burden as any other absence claim: a whitespace-normalised, case-insensitive, emphasis-stripped screen at a named commit, run **before** the claim rather than after the challenge. Distinguished from entry 14 (silent class truncation), which shortens an enumerated class, and from entry 10 (superseded-formulation restatement), which restates an older version of a live proposition. **Mechanical carrier, adopted with it:** no memo may carry such a phrase without an adjacent line stating the literals tried, the synonyms tried, the file count, the scope and the commit | 2026-09-04 | `analytics/daily-research/2026-09-04.md:968` (proposed by this seat, `51a2bae`), `:1040` (mechanical carrier), `:1111`, `:1148` (adopted by the chairman, `687cfde`); landed on `main` at `e3d0255` |
| 29 | **Off-read-path carrier** — an absence, uniqueness or "only carrier" claim screened over the scope a seat *habitually reads* (the prose record) and then stated over the scope where the fact actually lives. The blind spot is systematic, not incidental: the machine-readable and configuration trees (`specs/`, `state/`, `tests/fixtures/`, `.github/`) sit outside every seat's default screen roots **and** outside the sweeps that measure "uncarried knowledge", so a fact stored there is invisible in both directions at once and reads as absent twice over. **Distinguished from entry 27 (scope-mixed screen)**, where the *referent clause* is populated more widely than the screen annotating it: here the *claim* is stated more widely than the screen, and the omitted roots are the same two or three every time. **Countermeasure, mechanical and deliberately tool-free:** any screen supporting an unqualified claim about "the tree" or "the repository" enumerates candidate files with `git ls-tree -r <commit>` and **no path argument**, whatever instrument reads them; a narrower root set is named in the sentence and the claim narrowed to match. **The tool-free wording was adopted on challenge** — the officer's first draft keyed the countermeasure to `scripts/wsgrep_at.py`, the chairman objected that a countermeasure keyed to a non-existent file inherits the exact defect entry 28 was adopted on, and the officer rewrote it: `git ls-tree` is git, not a project script, so it cannot go missing. **Four instances, three seats, one day**, all 2026-09-05 and all verified: `0905-B1` (chairman, `specs/` and `tests/fixtures/`), `0905-B2` (chairman, `state/council_log.json:460`), `0905-B9` (analyst, `JS-rendered` → 6 hits in 6 files, not "0 anywhere"), `0905-B12` (analyst, the `Ecuador` and `Upreti` "full tree" clauses, `state/`) | 2026-09-05 | `analytics/daily-research/2026-09-05.md:1321` (adopted with the officer's own amendment), `:1421` (binding form, both `d969ca4`); `analytics/optimization-log.md:71` (`7fa1ef4`, on `main`) |
| 30 | **Re-implementation drift** — a seat measures a code path's effect by **re-implementing** the function rather than executing it, the re-implementation differs from the original in one operation, and the resulting figure is published as what that function produces. The citation names executable code the figure cannot come from, so it is uncheckable against the thing it cites **while looking maximally checkable**. **Distinguished from entry 26** (tautological instrument check), where the instrument runs but cannot discriminate; here the instrument never runs. **Countermeasure: execute the function against a scratch copy and read its return; if re-implementation is unavoidable, publish the diff from the original and the figure under both.** **Instance, verified:** `0911-B1` — the chair's 82,274 is the un-`rstrip`ed slice; `_handwritten_sections` (`src/council_log.py:145`) returns 82,257 | 2026-09-11 | `analytics/daily-research/2026-09-11.md:702` (proposed by this seat, `3f25b7f`), `:962` (adopted by the chairman, `28c0db8`) |
| 31 | **Assumed-remedy claim** — asserting that a repair path *would* restore a record (a render, a rebuild, a replay) where the path **has never been executed** and in fact produces an empty or degraded artifact. The harm exceeds the unfixed defect, because the record now says a loss is recoverable and a later seat closes the escalation on that basis. **Distinguished from entry 22** (unverified control design), which concerns a control's assumed negativity; here it is a *remedy's* assumed sufficiency. **Countermeasure: a remedy claim is run, in a scratch copy, and its output is quoted — or it is stated as untested.** **Instance, verified:** `0911-B2` — "a successful `_render_md` would make them appear"; executed, it emits 32-character stubs and would make the ledger falsely assert that six unlogged sittings were logged | 2026-09-11 | `analytics/daily-research/2026-09-11.md:704` (proposed by this seat, `3f25b7f`), `:962` (adopted by the chairman, `28c0db8`) |
| 32 | **Single-window referent clause** — an Amendment 2 referent clause stating **where a screened term's occurrences lie**, written from an instrument that can only return the **first** match. The clause reads as a statement about the term in the document; the instrument only ever saw one occurrence, chosen by construction. It is corrosive precisely where Amendment 2 is meant to bite: a nonzero count annotated with a confident referent reads as *excluded*. **Distinguished from entry 26**, where the instrument's construction guarantees the *result* — here it guarantees the *sample*; **and from entry 27** (scope-mixed screen), where the clause is populated at a wider scope than the screen — here at a wider scope than the **instrument's reach on that same screen**. **Countermeasure: a referent clause written from a first-match-only instrument names that limit inside the clause and never states where the term does not occur.** **Instance, verified:** `0912-N5` — "`Manifest` matched — that occurrence is … not the table body", contradicted by the analyst's own span, `excerpt_of` being centred on `body.lower().find(...)` (`scripts/fetch_relay.py:131`) | 2026-09-12 | `analytics/daily-research/2026-09-12.md:1102` (proposed by this seat, `3828137`), `:1376` (adopted by the chairman, `639c16e`) |
| 32a | **Boolean-as-count screen record** — adopted as an **extension of 32, not a new number**, expressly because of this table's collision history. A `find_matched` **boolean** written into a `V` mark's `<term:count>` slot as a numeral, converting "at least one occurrence" into "exactly one", after which Amendment 2's referent clause reads as exhaustive. **Distinguished from 32 proper**, which governs the *clause's* reach; this governs the *numeral*. **Countermeasure: a screen record from a boolean instrument writes `matched` / `not matched`, never a count.** **Instance, verified and disproved by the project's own same-day artefact:** `"Award" 1` in Entry 1, against ≥3 occurrences visible in `2026-09-13-zz-docket-chronology.json` `records[4]` | 2026-09-13 | `analytics/daily-research/2026-09-13.md:812` (proposed by this seat, `e256de2`), `:1005` (adopted by the chairman as an extension, `203dbf6`) |
| 33 | **Self-contradicting adjacent enumeration** — a count stated in a headline sentence that disagrees with the enumeration in the **adjacent** sentence, so the defect is detectable without leaving the paragraph and without opening any file. **Distinguished from entry 14** (silent class truncation), where the short enumeration is the *only* statement and the fuller class lives elsewhere in the record; here both the count and the fuller enumeration are on the page, disagreeing. **Countermeasure: any count of a set the same paragraph enumerates is read back against that enumeration before the paragraph closes** — the cheapest check in the set, requiring no file, no tool and no second reader. **Proposed as a sub-number (`17b/14a`) and adopted as its own entry** because it had three verified instances in one session and a mechanical countermeasure of its own — and because the gate committed it *in the very paragraph proposing it*. **Three instances, one session, two seats, all verified:** `0912-B2` (forecast tally), `0912-B6` (row-fragment count), `0912-B3` (median correction, "published twice" against eight live occurrences) | 2026-09-12 | `analytics/daily-research/2026-09-12.md:1112` (proposed by this seat as `17b/14a`, `3828137`), `:1377` (adopted by the chairman **as entry 33**, `639c16e`) |
| 34 | **Premise-in-the-pre-registration** — a follow-up batch's note restates the prior batch's *inference* as established fact, so the inference is frozen into a **committed artefact ahead of vetting** and inherits the epistemic authority of a pre-registration. **Distinguished from entry 25** (mutable-reduction citation): the defect is not the citation's mutability but the **premise's firmness**. **Countermeasure: a follow-up note states its premise in the hedged form the prior batch's spans actually carry, or marks it "inferred, unvetted".** **Instance, verified:** `2026-09-13-zz-docket-chronology.json` states an objection "was filed pursuant to ICSID Arbitration Rule 41(1) **and fully briefed**" — an attribution that is inferred (`0913-B11`) and a completeness claim the batch's **own row 1** then falsified (`0913-B9`). The chairman recorded the instance as against himself | 2026-09-13 | `analytics/daily-research/2026-09-13.md:811` (proposed by this seat, `e256de2`), `:1005` (adopted by the chairman, `203dbf6`) |
| 34a | **Licence-in-the-pre-registration** — adopted as an **extension of 34, not a new number**, expressly because this table's collision history argues against new numbers where an extension will do. A pre-registration states what an outcome *"decisively"* or *"conclusively"* establishes at a strength the row cannot carry; because a pre-registration is never edited, the overstatement is **frozen and can only be withdrawn, never corrected**. **Distinguished from 34 proper**, which governs the firmness of a *premise*; this governs the strength of a *licence*. **Countermeasure: a pre-registered licence is written at the weakest form that still makes the row a test — "would materially weaken X" without "decisive" — because a falsification condition does its work by being pre-committed, not by being strong.** **Instance, verified, and recorded by the chairman against himself as much as against the analyst:** the committed note's *"maintained"* and the memo's *"controlled"*, both too strong. **Proposed by name only**, the officer again declining to take a number off this heading. | 2026-09-18 | `analytics/daily-research/2026-09-18.md:904` (proposed by name, `af479da`), `:1203` (adopted by the chairman as an extension, `018c1f1`) |
| 35 | **Manufactured residual** — reporting a bucket as UNACCOUNTED under an anti-rounding rule when the split in fact reconciles exactly, so a rule written to stop smoothing instead plants a phantom irreducible remainder that later seats inherit and cannot dissolve. **Countermeasure: an UNACCOUNTED declaration carries the per-file enumeration that failed to close; if the enumeration is not shown, the residual is not established.** **Adopted 2026-08-07 as 27**, one day after *scope-mixed screen* took that number and before it reached this table; **filed at 35 by the chairman's ruling of 2026-09-13**, under which first adoption keeps the number and every later colliding adoption moves to the tail. **Cite by name, never by number — permanently binding.** | 2026-08-07 (adopted) · 2026-09-13 (numbered) | `analytics/daily-research/2026-08-07.md:710` (proposed), `:975` (adopted by the chairman); `7adfd68`. Numbering: chairman's rulings of 2026-09-13, item (a), transcribed verbatim in the concordance below |
| 36 | **Untested counterfactual** — asserting what an alternative code path would produce without executing it. **Countermeasure, in the officer's own words: _"a counterfactual over code is executed or it is not filed."_** **Instance, verified:** the analyst's claim that neutralising `EXTRA_WEIGHT_RING` drops holdout recall from 3/4 to 1/4; run rather than reasoned, Loewen scores 48 and Mondev 54, both still clearing 40 through the `sub >= STRONG_SUBTOTAL or second` branch at `src/classify.py:293-295`, and recall is unchanged at 3/4 — the counterfactual was struck from the record. **Adopted 2026-09-10 as 27** at the operator-mandated special session; filed at **30** on PR #170 while that branch sat unmerged; **filed at 36 by the chairman's ruling of 2026-09-13**, the PR #170 filing being void. **Cite by name, never by number — permanently binding.** | 2026-09-10 (adopted) · 2026-09-13 (numbered) | `analytics/daily-research/2026-09-10-special-session.md:552` (opened and numbered in session), `:1213`; landed on `main` at `188cabe` (PR #170, merged `3099610`). Numbering: chairman's rulings of 2026-09-13, item (a), transcribed verbatim in the concordance below |
| 37 | **Cross-boundary window attribution** — a fixed-width window straddles a section boundary the window does not mark, and content belonging to the section **after** the boundary is attributed to the subject of the section **before** it. The window is entirely accurate; the defect is in the attribution, which adjacency makes almost automatic and which no part of the span contradicts. **Distinguished from entry 3** (snippet-as-fact), where the snippet is read as establishing a fact it does not state — here the snippet states everything it appears to state and the error is *whose* fact it is; **and from entry 32** (single-window referent clause), where first-match construction limits the *sample* — here the fixed 400-character width crosses a boundary the excerpt does not render. **Countermeasure: a window containing a section heading is split at the heading, and no span after the heading is attributed to the subject of the span before it, unless a second independently-centred window carries the boundary's other side.** **Instance, verified:** blob `c67c112e…` `records[1]` places `Latest Development: August 28, 2026 - The ad hoc Committee issues Procedural Order No. 3 …` adjacent to `(a) Original Proceeding Published Decisions … Procedural Order No. 3`, where the listed order is dated 30 April 2025 by blob `02d1ff14…` `records[4]` and sits under a heading naming the **original** proceeding. **Prior art screened by the proposing seat** at `8803908` over 714 blobs, the zeros validated against known positives in the same run. | 2026-09-14 | `analytics/daily-research/2026-09-14.md:623` (proposed by this seat, `48d43ca`), `:769` (adopted by the chairman, `0390fe3`), `:941` (binding form) |
| 38 | **Exact-match screen generalised to a pattern claim** — a seat screens the record by **exact-URL or exact-string equality**, gets a correct and complete answer *at that key*, and then states the result at the level of a **pattern**: a path class, a URL shape, a spelling family. The screen is sound; the claim is one abstraction level wider than the key, so the absence claim is unscreened at the scope asserted **while looking maximally screened** — a clean exact-match zero reads exactly like a clean pattern zero and is not one. **Distinguished from entry 27** (scope-mixed screen), where the referent *clause* is wider than the screen; **and from entry 29** (off-read-path carrier), where the omitted scope is the machine-readable and configuration trees. Here the root is the same and correct; only the **key** is wrong. **Countermeasure, mechanical: an absence claim about a class of locator is screened by the class predicate, never by equality on one member — and the sentence names the predicate it screened.** **Instance, verified:** `0916-B1`. **Proposed by name only and expressly not numbered by the proposing seat**, which cited this table's stale heading as the reason and declined to number off it; the chairman issued the number. | 2026-09-16 | `analytics/daily-research/2026-09-16.md:669` (proposed by name, `007909d`), `:1021` (number issued by the chairman, `c231022`), `:1129` (binding form) |
| 39 | **Dedup-screen referent inversion** — a seat runs the required duplication screen against `analytics/insights.jsonl` and `STATE_OF_THE_ANSWER.md`, **the screen returns the prior entry**, and the seat characterises the hit as immaterial — *"appears only as X, never as Y"* — when the hit is the same finding. The new entry is filed as novel **and** the record reports the project as having *missed* what it in fact recorded on the day. Two harms compound: a permanent duplicate in the ledger, and a false self-assessment that inverts the project's actual memory performance and is then built on rhetorically. **Distinguished from entry 32** (single-window referent clause), where the instrument could only ever see one occurrence and the seat is defeated by construction — here the seat had the whole line in front of it; **from entry 28** (unscreened first-ness claim), which is the bare novelty assertion with no screen — 39 is the screen that ran, hit, and was written up as a miss; **and from entry 5** (memory-file reconstruction), where the memory file replaces a retrieval — here the retrieval is genuine and the memory file is the thing misread. **Countermeasure: a dedup screen is discharged by quoting the headline of every line the screen returned, never by characterising them** — *"X appears only as A, never as B"* over a ledger is an Amendment 2 referent clause about an entry's content and carries the same burden as any other. **Aggravating condition found the same day:** the duplicated entry's own citation is unresolvable (`0917-N9`) — a ledger whose blob ids do not resolve cannot police its own duplicates. **Instance, verified:** `analytics/insights.jsonl:149` (2026-09-07) and `STATE_OF_THE_ANSWER.md:154` both carry the `/cases/recent` vs `/cases/pending` `ARB/` asymmetry, correctly scoped as *"the unit is the URL, not the host"*; both contain the literal `/cases/recent`. **Numbered off a heading the proposing seat verified rather than a stale one, and no chairman's issue was needed** — the first day in this seat's recent record on which the D15 latency did not fire. | 2026-09-17 | `analytics/daily-research/2026-09-17.md:887` (proposed by this seat, `226d697`), `:1275` (adopted by the chairman, `710842c`) |
| 40 | **Stale-population screen record** — a screen's *population* figure (the file count, the corpus size, the denominator) is carried from an earlier session and restated as counted at the commit the screen names, **while the derived hit counts are genuinely recomputed**. The hits being right is what makes the defect invisible: nothing on the page contradicts the figure, and it cannot be seen without opening the repository at the named commit. The screen's *completeness* claim is unsupported at the scope asserted. **Distinguished from entry 27** (scope-mixed screen), where the referent clause is populated more widely than the screen — here the screen's scope is correct and only its stated size is wrong; **from entry 25** (mutable-reduction citation) — this screen is commit-pinned and still wrong; **and from entry 33** (self-contradicting adjacent enumeration) — nothing adjacent disagrees. **Countermeasure, as proposed and then tightened by the analyst and adopted in the tightened form: the population is printed by the pass that produces the hits, in the same output, adjacent to them — never re-derived in a second command and never carried between sessions.** The tightening is load-bearing: *"a count re-derived in a second command is a second observation of a tree that may have moved, which is how this one moved."* **Instance, verified twice in one document:** `0918-B1`, population restated as 67 / 68. **Corroborated the same day by a second failure of the same shape:** three seats produced three numbers for one screen — *"twelve loci"*, *"twelve files, eighteen occurrences"*, *"eleven records"* — and on the chairman's re-run with the unit declared, **13 occurrences in 9 files**. *"No seat was wrong about the world. Three seats were silent about the unit."* **Proposed by name only**, the officer declining to take a number off a heading it had verified was one behind. | 2026-09-18 | `analytics/daily-research/2026-09-18.md:906` (proposed by name, `af479da`), `:1195` (adopted by the chairman, `018c1f1`) |
| 40a | **Unit-swapped screen record** — adopted as an **extension of 40, not a new number**, on the proposing seat's own reasoning that *"this table's collision history argues against new numbers where an extension will do"* — the **third** time that precedent has governed. A screen publishes per-file or per-corpus **line** counts under an explicit *"occurrences"* label, or the reverse. The population and the scope are correct and the instrument ran; only the **unit** is misdeclared, so the figure is **unfalsifiable from the page** and the error propagates into exclusion arithmetic and into banked claims. **Distinguished from 40 proper**, which governs the screen's *population*; this governs the **unit of its hits**. **The harm clause as the analyst amended it, and the chairman called the amendment the sharper half of the entry:** a unit-swapped screen does not merely publish an uncheckable figure, it **can silently retire a correction the council has already sustained** — two files published at 1/1 under *"occurrence"* where the live `0919-N2` correction depends on their being 2/2 — so a unit swap **can read as substantive news**. **Countermeasure, as amended and adopted: a screen record names its unit and its flag in the same clause as its number** (`git grep -c` = lines; `git grep -o | wc -l` = occurrences), **exclusion arithmetic is done in the unit it was measured in, and where a screen restates figures on which a prior sustained correction depends it states expressly whether that correction is unchanged.** **Instance, verified:** `0920-B2`. **It fired twice within two days of adoption, both times against figures nobody had flagged** — `0922-N6`, where `www.italaw.com` yields 6 PDF-suffixed rows, 5 distinct URLs and 4 distinct byte-streams with no unit declared (`2026-09-22.md:880`), and `0922-B3`, where *"five path shapes"* is unreachable at any unit the officer could construct (`:816`). | 2026-09-20 | `analytics/daily-research/2026-09-20.md:995` (proposed by name as an extension, `1d6e3e7`), `:1240` (analyst's harm-clause amendment), `:1323` (adopted as an extension by the chairman, `1d6e3e7`), `:1508` (binding form) |
| 41 | **Invented limb** — a seat attributes to a **cited internal authority** a proposition that authority does not contain, typically by imposing a *"first limb / second limb"* structure on a document that has neither, and then reports that manufactured limb as *contradicted*, *in doubt* or *tested*. **The citation's locator is correct and checkable, which is what makes it pass:** a reader who follows the pinpoint finds the right document and does not notice that the quoted structure is absent from it. The damage is that a committed internal authority enters the record as having been **weakened, when nothing touched it**. **Distinguished from entries 17 / 17a** (mis-dated, mis-located), where the locator is wrong and the content right — here the locator is right and the content is invented; **from entry 10** (superseded-formulation restatement), which restates a real earlier version; **and from entry 3** (snippet-as-fact), which over-reads a real span rather than supplying an absent one. **Countermeasure, mechanical, in the form the chairman adopted with the analyst's amendment — and the amendment is not cosmetic: a sentence that puts a cited internal authority in doubt quotes verbatim, at a pinpoint, the LIMB, PREMISE, GROUND, PRONG OR BRANCH it contests, before contesting it; where the authority carries no such sentence, the seat states the proposition in its own name instead of the authority's.** The widening from *limb* alone was adopted because **the instance that generated the entry did it with the word *premise*** — an entry keyed to *limb* would have been evaded by its own instance. **The mechanical test is one line: the contested structure must appear inside a quotation pair.** **Instance, verified:** `0920-B4` — *"the first limb of escalation 2 — that no allowlisted host carries a NAFTA Chapter 11 locator"* against `2026-09-19.md` §6.6 item 2, which contains no limb structure and no such proposition; the nearest real statement, `:1004` / `:1090`, is scoped to locators **carried in this repository** at three named hosts. **Numbered off a heading the proposing seat opened and verified current** (`2026-09-20.md:788`) — the second such day in this seat's record, and the last before the heading went behind again on its own adoption. | 2026-09-20 | `analytics/daily-research/2026-09-20.md:991` (proposed by this seat, `1d6e3e7`), `:1238` (analyst's amendment), `:1315` (adopted by the chairman with the amendment in full, `1d6e3e7`), `:1508` (binding form) |

> [!note] **PENDING — proposed by name, no number taken. Three on 2026-09-19, one on 2026-09-20,
> one on 2026-09-22.** Filed here rather than in the table because **no seat numbered them and it
> is not the archivist's place to**. The first three were proposed at
> `analytics/daily-research/2026-09-19.md:877-882` (`b267efd`) and carried forward by the
> chairman's close-out without numbers (`:1318-1326`); the fourth at `2026-09-20.md:1334`
> (`1d6e3e7`); the fifth at `2026-09-22.md:946` (`a814d18`), which the chairman then adopted
> **alongside the analyst's narrower mechanical variant of it, both expressly unnumbered and both
> routed here** (`2026-09-22.md` §6.4, `67ef197`). **The next free number is 42 and none of these
> has taken it.**
>
> | Name | What it is | Status in the close-out that carried it |
> | --- | --- | --- |
> | **Zero-screen counted as a carrier** | A seat supports a proposition with an occurrence count over its own record, and the occurrences it counts are *prior screens that returned zero on that very term* — the record's report of the term's **absence** becomes, to a grep, the term's **presence**. Arithmetically correct and epistemically inverted. **Countermeasure: any occurrence count offered in support of a proposition excludes loci whose content is a screen record for the same term, and states how many were excluded.** **Instance:** `0919-B2` — `Achmea` 4 files / 8 occurrences, of which `2026-08-24.md:359` ×2 report `Achmea` → 0. | **ADOPTED AS BINDING PRACTICE, UNNUMBERED** (close-out item 6, `:1323-1326`). It fired on the analyst the day it was named. |
> | **Selective self-quotation deflation** | A seat correctly discounts an occurrence count as *"this council quoting itself"* where the count would inflate someone else's object, and banks a structurally identical count as substantive engagement where it carries the seat's own headline. The method is sound; its application is asymmetric, **and the asymmetry tracks the seat's conclusion**. **Countermeasure: the self-quotation test is applied to every nonzero count in the memo or to none, and its result is written next to each.** **Instance:** `0919-N2`. | Proposed by name; no number taken. |
> | **Own screen unread as evidence for a second proposition** | An enumeration built for one proposition is evidence for others, and nothing in any seat's procedure re-reads it. Proposed by the **analyst**, by name. **Instance:** the Spentech row sat inside the seat's own five-URL enumeration and was written out of existence four sections later. | Proposed by name (close-out item 5, `:1319-1322`); no number taken. |
> | **One-pass artefact read** | A search or fetch artefact is read **once**, against the question of the call that produced it, and never again — so rows inside a seat's own committed enumeration are evidence for other propositions the same memo advances and nothing in any seat's procedure re-reads them. **Countermeasure: a search artefact is read twice — once per call against that call's question, and once WHOLE, against every proposition the memo advances, before the memo is filed.** **Instance:** `0920-N5`. | Proposed by name, 2026-09-20 (`:1334`, `1d6e3e7`). **The chairman declined the number in terms and gave the reason**: *"`agents/` is outside this session's merge scope, I am already issuing 41 into a table I cannot edit, and a second number issued blind into the same unwritable table is how the entry-27 collision happened."* **That sentence is D15 stated by the seat the latency binds.** |
> | **Screen-record self-falsification** | An absence claim about the project's **own tree** is falsified **by the act of filing it**: once the screen record is committed, the term it reports as absent is present in the repository, and the standing sentence asserting the absence is false at the next commit. The next seat to re-run the screen gets a nonzero result **composed entirely of prior screen records** and must either contradict the standing sentence or explain it away. **Distinguished from the unnumbered *zero-screen counted as a carrier***, which governs an occurrence **count offered in support of a proposition**; this governs a standing **absence sentence about the repository**, which no count accompanies and which nothing re-checks. **Countermeasure: an absence claim about the tracked tree carries its exclusion inside the sentence — "no carrier other than this council's own screen records" — and names the screen-record loci, so re-running it returns the same verdict instead of a contradiction.** **Instance, verified:** `0922-N7` — *"No spelling of it appears anywhere in the tracked repository"* against `1110(7)` at 9 files / 48 occurrences, every carrier a screen record or escalation. | Proposed by name, 2026-09-22 (`:946`, `a814d18`); **adopted by the chairman unnumbered and routed here** (§6.4, `67ef197`). **It fired inside the record that proposed it, within one commit** — see the row below. |
> | **Dedup screen record carries its line count** (the analyst's narrower variant, adopted with the above) | The mechanical half of *screen-record self-falsification*, narrowed to **the artefact this council files daily**: a dedup screen record carries the line count of `analytics/insights.jsonl` **at which it was run**, and states that filing the entry falsifies it. The analyst proposed it against its own artefact after finding that its §3.5 screen reported **eight** terms at 0 lines in `insights.jsonl` while the insight about to be appended **contained all eight** — *"the moment it is appended, every one of those eight zeros is false in the very file they were screened against"* (`2026-09-22.md:1218`). Executed in the same record: `AT 202 LINES BEFORE THIS ENTRY IS APPENDED`. | Proposed by name, 2026-09-22 (`:1218`, `a9bc44f`), **taking no number, as the officer did**; adopted by the chairman alongside the officer's wider form (§6.4, `67ef197`). |
>
> **Why they are unnumbered and why that is correct.** The proposing seat's stated reason is
> `:875`: *"the entry-27 collision is still open and `agents/` is outside this session's merge
> scope."* The collision is in fact **settled** — by your ruling of 2026-09-13, transcribed in the
> concordance below — so the live reason is the merge scope alone, which is **D15**. Archivist,
> 2026-09-19.
>
> **Archivist, 2026-09-22 — the reason has now been given in the chairman's own words, and it is
> narrower and worse than the 2026-09-19 reading.** Declining a second number on 2026-09-20, the
> chair wrote: *"a second number issued blind into the same unwritable table is how the entry-27
> collision happened"* (`2026-09-20.md:1334`, `1d6e3e7`). Not merely *out of scope* —
> **unwritable**, and the seat named the exact historical failure that scope produces. Two days
> later the officer declined for the same reason having **measured** the gap rather than asserting
> it (`2026-09-22.md:942`, `a814d18`). **Five patterns now sit unnumbered in this block, three of
> them binding practice, because the seats that adopt them cannot write the file that carries
> them.** That is the whole argument for the one-file scope widening put to Emory in
> [[Workflow Threads]] **D15**, and it is now made by the bound seats rather than by this one.

> [!important] **THE TAXONOMY CONCORDANCE — number-as-adopted → number-as-filed. Chairman's
> ruling of 2026-09-13, item (a); executed by the archivist in one change set, 2026-09-13.**
>
> Every citation of these three patterns written before the ruling resolves through this table.
> **Nothing already correctly numbered was renumbered and no row was displaced** to make room for
> anything.
>
> | Pattern | Number as adopted | Date of that adoption | Number as filed | What it resolves |
> | --- | --- | --- | --- | --- |
> | **Scope-mixed screen** | 27 | 2026-08-06 (`aa48406`) | **27 — unchanged** | every "27" / "entry 27" / "taxonomy 27" in the record, unless the citation is marked `27 ⚠` or names *manufactured residual* |
> | **Manufactured residual** | 27 (colliding) | 2026-08-07 (`7adfd68`) | **35** | every "27 ⚠", and every "27" that names *manufactured residual* |
> | **Untested counterfactual** | 27 (colliding) | 2026-09-10 (`…special-session.md:552`) | **36** | the special session's "27", **and** the branch-era "30" filed on PR #170, which is void |
> | *unqueried configuration assertion* — **proposed, not adopted** | — | proposed 2026-09-11 (PR #160, row D) | **none**; the PR #170 reservation at 31 is **VOID** | any branch-era "reserved at 31" |
> | *same-date execution conflation* — **proposed, not adopted** | — | proposed 2026-09-11 (PR #163, row K) | **none**; the PR #170 reservation at 32 is **VOID** | any branch-era "reserved at 32" |
>
> **30, 31, 32, 32a, 33 and 34 are occupied on `main` by the daily sittings and do not move** —
> re-implementation drift (30), assumed-remedy claim (31), single-window referent clause (32) with
> its extension 32a, self-contradicting adjacent enumeration (33), premise-in-the-pre-registration
> (34). **The next free number is 37.** *(Archivist, 2026-09-16: that sentence was true when the
> ruling was executed on 2026-09-13 and is kept unaltered as part of the dated record. **37 and 38
> have since been issued** — cross-boundary window attribution, 2026-09-14, `0390fe3`; exact-match
> screen generalised to a pattern claim, 2026-09-16, `c231022`. **The live next free number is at
> the top of this section and is 39.** Neither new entry collides and nothing here is renumbered.)*
> *(Archivist, 2026-09-19: the 2026-09-16 parenthetical above is kept unaltered as a dated record.
> **39 and 40 have since been issued and extension 34a filed** — dedup-screen referent inversion,
> 2026-09-17, `710842c`; stale-population screen record, 2026-09-18, `018c1f1`;
> licence-in-the-pre-registration as `34a`, 2026-09-18, `018c1f1`. **The live next free number is
> 41**, and it is at the top of this section, which is the only place it is ever live. None of the
> three collides and nothing here is renumbered.)*
> *(Archivist, 2026-09-22: the two parentheticals above are kept unaltered as dated records.
> **Entry 41 has since been issued and extension 40a filed** — invented limb, 2026-09-20,
> `1d6e3e7`; unit-swapped screen record as `40a`, 2026-09-20, `1d6e3e7`. **The live next free
> number is 42**, and it is at the top of this section, which is the only place it is ever live.
> Neither collides and nothing here is renumbered. **40a is the third adoption filed as an
> extension rather than a new number** — after 32a and 34a — and all three cite this concordance's
> own collision history as the reason, which is the clearest evidence available that the ruling of
> 2026-09-13 is not merely settled but operating.)*
>
> **Cite-by-name is permanently binding for scope-mixed screen, manufactured residual and untested
> counterfactual.** Three sittings issued the number 27 for three different patterns across
> thirty-five days. A number that has meant three things is not made safe by a table; it is only
> made *resolvable* by one — and the citations already written into the daily records cannot be
> reached by any edit this vault is allowed to make, because those records are not rewritten.
>
> **The ruling's operative holding, transcribed verbatim**, because the rulings record of
> 2026-09-13 is not itself a file under version control in this repository at the time of this
> filing and this note is therefore its citable carrier:
>
> > **Principle:** `main`'s table is canonical, because it is the merged and citable record;
> > **first adoption keeps the number; every later colliding adoption moves to the tail, never
> > into a gap.**
> >
> > - **27 = Scope-mixed screen** (2026-08-06, `aa48406`) — **unchanged.**
> > - **Manufactured residual** (2026-08-07, `7adfd68`, currently `27 ⚠`) → **35.**
> > - **Untested counterfactual** (special session 2026-09-10, adopted-as-27, filed-as-30 on the
> >   unmerged branch) → **36.**
> > - **PR #170's filing at 30 and its reservations at 31 and 32 are VOID** — 30, 31, 32, 32a, 33
> >   and 34 are occupied on `main` by the daily sittings and those entries do not move.

> **[SETTLED 2026-09-13 — the ruling came the same day. See the disposition at the foot of this
> block; the side-by-side table is kept unaltered because it is the record of the failure.]**
> **THE COLLISION AT 30/31/32, STATED IN FULL BEFORE THE FILING NOTE. Archivist, 2026-09-13.**
> Two sittings issued the same three numbers for different patterns, and neither could see the
> other:
>
> | Number | On `main` (daily council, filed above) | On open PR #170 (`7f1d01c`, unmerged) |
> | --- | --- | --- |
> | 30 | Re-implementation drift (2026-09-11, `28c0db8`) | *Untested counterfactual* — adopted in session as **27**, filed at the next free number |
> | 31 | Assumed-remedy claim (2026-09-11, `28c0db8`) | RESERVED, **not adopted** — *unqueried configuration assertion* (proposed) |
> | 32 | Single-window referent clause (2026-09-12, `639c16e`) | RESERVED, **not adopted** — *same-date execution conflation* (proposed) |
>
> **The mechanism is the one this note already describes, one level up.** The 2026-08-07 collision
> was caused by a stale *heading*; the fix — move the heading in the same change set as the row —
> held, and is not what failed here. What failed is that **the change set itself never landed**:
> PR #170 carries the 2026-09-10 special session's entire record
> (`analytics/daily-research/2026-09-10-special-session.md`, 1,267 lines) and its vault close-out,
> and has been open since 2026-09-11. Nothing on `main` so much as names that sitting. So the daily
> council read a heading that was accurate *for `main`* and numbered off it correctly, three days
> running. **A stale heading produced one collision; an unlanded branch has now produced three.**
>
> **This seat files, it does not renumber.** Both sets are recorded, neither is altered, and the
> ruling is the chairman's — alongside the C11 ruling open since 2026-08-07. Escalated in
> [[Workflow Threads]] as **D17**, and to Emory in `analytics/vault-sessions/2026-09-13.md`, where
> the operative request is simply: **land or close PR #170.**
>
> **DISPOSITION — 2026-09-13, the same day. PR #170 landed and the chairman ruled.** The merge is
> `3099610` (2026-09-13 17:52 -0400); the special session's 1,267-line record reached `main` at
> `188cabe` and the branch's vault close-out at `c894a4b`. **D17's owner was reassigned from Emory
> to this seat by the ruling** — a sitting `main` cannot see is a hole in the project's memory and
> closing it is not the operator's errand. The chairman then ruled item (a): `main`'s table is
> canonical, first adoption keeps the number, every later colliding adoption moves to the tail.
> **The right-hand column of the table above is void** — the branch's filing at 30 and its
> reservations at 31 and 32 have no effect — and the three colliding patterns are filed at **27**
> (unchanged), **35** and **36** per the concordance above. **Both sets are still recorded here
> unaltered**, because the record of how one unlanded branch produced three two-way collisions in
> three days is the part of this note a later seat needs. Archivist, 2026-09-13, executing the
> ruling.

> **Filed 2026-09-13 by the archivist. Five adoptions, four sessions, and this is the routing
> failure the council escalated rather than the archivist being late.** Entries **30** and **31**
> were adopted 2026-09-11 (`28c0db8`), **32** and **33** on 2026-09-12 (`639c16e`), **34** and
> **32a** on 2026-09-13 (`203dbf6`). None could be written by the sitting that adopted it, because
> `agents/` is outside the daily council's merge scope; this seat runs every three days, and the
> 2026-09-10 session did not run at all. **The cost is recorded by seats that are not the
> archivist, and it is no longer hypothetical:**
>
> - On **2026-09-12** the officer opened this table, found it heading "29 entries as of
>   2026-09-07" while the council stood at 31, and **numbered from the council's adoptions rather
>   than from the heading** — stating that it had done so before numbering
>   (`analytics/daily-research/2026-09-12.md:1096`, `3828137`). That is the correct handling **and
>   the proof of the defect**: the file the officer's mandate names could not be trusted for the
>   one fact the mandate needs from it.
> - The chairman ruled the same day that he escalates *"the routing, not the archivist"*
>   (`:1374`, `639c16e`), and again on 2026-09-13 at `:1162` (`203dbf6`), where he records the
>   routing as **five consecutive adoptions into a directory the daily session cannot merge**.
>
> **Had this table been current, entry 32 would have been numbered off a table that agreed with
> the council** and the officer would not have had to explain, twice, which authority it was
> counting from. That is the concrete prevention claim for this note, and it is the reason D15 is
> a defect about *routing latency* rather than about diligence.

> **Filed 2026-09-07 by the archivist, two days late, and the delay had already been paid for.**
> Entry 29 was adopted 2026-09-05 and routed to this seat because `agents/` is outside the daily
> council's merge scope (`analytics/optimization-log.md:71`, `7fa1ef4`). It reached no note for two
> days. On **2026-09-06** the officer numbered its next proposal **30** off this table's stale
> "28" heading, and the chairman declined to adopt by number for exactly that reason — the cost is
> recorded, by a seat that is not the archivist, at `analytics/daily-research/2026-09-07.md:750`
> (`34b3970`): *"`agents/integrity-officer.md` — the single file my mandate names — still reads
> '28 entries as of 2026-09-04' … Today's Part I trap 2 and the frozen pre-registration both cite
> 'entry 29' correctly against the council's ruling and **uncheckably against the file the mandate
> names**."*
>
> **This is the second consecutive occurrence of one failure mode, and it is the one this seat's
> own table already describes.** Entry 28 was routed here on 2026-09-04 and filed the same day only
> because that session went looking for it; entry 29 was routed on 2026-09-05 and sat. **A rule the
> council adopts and routes to `agents/` is invisible to the seat bound by it until an archivist
> session lands — and those run every three days.** That latency is the defect, not the individual
> miss. Escalated in [[Workflow Threads]] as **D15**.
>
> **Companion recommendation, adopted with entry 29 and NOT executed here because it is a contract
> change:** add `specs/` and `state/` to the record-screening scope in the analyst and officer
> definitions under `.claude/agents/`. That is one line per definition and it is the operator's.

**The collision, and why it is this note's fault.** Two distinct patterns were adopted as
entry 27, one day apart, and neither seat did anything wrong given what it could read. On
2026-08-06 the chairman adopted *scope-mixed screen* as 27 in his close-out and it was never
written here. On 2026-08-07 this seat opened this table to check its numbering — exactly as
the mandate directs — found the heading reading "24 entries as of 2026-08-04", knew of 25 and
26 from the live agenda, and numbered the next free slot 27. The chairman then adopted
*manufactured residual* under that number. **A stale count in this heading is not a cosmetic
defect: it is the input to the next entry's number.** The seat said so itself in the same
note — "the vault table is stale again, in the single file the mandate names"
(`analytics/daily-research/2026-08-07.md:713`).

Both rows stand as adopted, under the numbers the record actually gives them. **Renumbering
is not the archivist's to do** — it changes what two council rulings say — and it is escalated
in [[Workflow Threads]] C11 for the chairman and this seat to settle. Until they do, cite
entry 27 by name, never by number.

**RULED 2026-09-13, thirty-seven days after it opened, and C11 is CLOSED.** The chairman settled
it in the rulings session of 2026-09-13, item (a): `main`'s table is canonical, **first adoption
keeps the number, and every later colliding adoption moves to the tail, never into a gap.**
*Scope-mixed screen* keeps **27**; *manufactured residual* is filed at **35**; the third pattern
adopted under the same number, *untested counterfactual*, is filed at **36**. Renumbering was
never this seat's to do and it still is not — it is done here on the chairman's ruling and on
nothing else, in one change set touching every citation, carrying the concordance above. **The one
thing that survives the ruling is the convention the collision grew:** cite *scope-mixed screen*,
*manufactured residual* and *untested counterfactual* by name, never by number — **permanently
binding**, not an interim measure.

> **Still unsettled at 2026-09-04 — day twenty-eight, and this seat re-raised it unasked.** In
> its own accountability section the officer recorded the collision as *"escalated at
> `Workflow Threads` C11 since 2026-08-07 — 28 days open"* and stated that it *"cited entry 27 by
> name, never by number, as the vault directs"* (`analytics/daily-research/2026-09-04.md`,
> "Reported against myself", item 3, `51a2bae`). The convention is holding. The ruling that would
> retire it has not come. **Owner: [[council-chairman]] with this seat.**

> **A third entry was adopted under the number 27, and this time the heading was not stale —
> 2026-09-11, at the special session's close-out.** At the operator-mandated special session of
> 2026-09-10 the officer opened *untested counterfactual* and numbered it **27**
> (`analytics/daily-research/2026-09-10-special-session.md:552`). The previous entry in this
> note's collision narrative blames a stale heading for the 2026-08-07 collision, and the fix
> that followed was to move the heading in the same change set as the row. **That fix held and
> was not the failure here.** The heading read *"29 entries as of 2026-09-07"* at `4eb3fc9`,
> committed three days before the session, and the only occurrence of the string
> "24 entries as of 2026-08-04" anywhere in this file is inside the 2026-08-07 narrative
> immediately above — a quotation of what that session found, not a live heading. The number
> issued in session therefore came from a count this file does not carry.
>
> **Filed at the next free number; nothing renumbered.** *Untested counterfactual* is filed as
> **30**, because adopting at an occupied number does not vacate the row already there, and
> because the disposition this note has held since 2026-08-07 is that **renumbering is not the
> archivist's to do** — it changes what a council ruling says. So the record now holds a
> number-as-adopted (27) and a number-as-filed (30) for one entry, which is a defect of the
> same family as the collision it sits under. **Wanted:** one chairman's ruling settling both,
> alongside the C11 ruling that had been open since 2026-08-07. **It came on 2026-09-13 and it
> settled both — see immediately below.** (The clause that used to end this paragraph was left
> severed when the merge-time correction was spliced into it; it is repaired here rather than
> left dangling.)
>
> **RULED AND FILED — 2026-09-13, the chairman's rulings session, item (a). This replaces the
> correction this seat wrote at the merge of PR #170; the narrative it carried is kept here
> because how the collision happened is the part with value.** What happened, in order: the filing
> at **30** did not survive the branch. While PR #170 sat unmerged from 2026-09-11, the daily
> sittings of 09-11, 09-12 and 09-13 adopted six other patterns at **30, 31, 32, 32a, 33 and 34**,
> and those are the rows in the table above — they are on `main`, and the branch was rebased onto
> them. At the merge (`3099610`) this seat recorded *untested counterfactual* as **adopted in
> session and unfiled**, because renumbering is not the archivist's to do and it would not write a
> row the chairman had not authorised. **The chairman ruled the same day, and the entry is no
> longer unfiled.** `main`'s table is canonical; first adoption keeps the number; every later
> colliding adoption moves to the tail, never into a gap. **_Untested counterfactual_ is filed at
> 36**, and **PR #170's filing at 30 is void**, as are its reservations at 31 and 32. Nothing on
> `main` was renumbered and no row was displaced to make room for anything. The concordance under
> the table resolves both the session's "27" and the branch's "30". **Cite it by name, never by
> number — permanently binding.** Archivist, 2026-09-13, executing the ruling.
>
> **Two further patterns were proposed on 2026-09-11 and are NOT adopted.** They were reserved at
> **31** and **32** on PR #170 so that the next entry would not take a number a proposal was
> already using; **the chairman's ruling of 2026-09-13 voids both reservations.** 31 and 32 are
> occupied on `main` by *assumed-remedy claim* and *single-window referent clause*, and the two
> proposals hold **no number at all**. They were reported to this seat at the row L close-out,
> arising on PR #160 (row D) and PR #163 (row K); no committed council artifact records an
> adoption for either, and this seat does not write an entry it cannot source. If either is
> adopted it takes the next free number, which is **37**. **Owner: [[council-chairman]]** — adopt,
> amend, or decline. Archivist, 2026-09-11; reservations voided by the ruling of 2026-09-13.
> *(Archivist, 2026-09-16: 37 and 38 were issued to other patterns on 2026-09-14 and 2026-09-16.
> **If either of these two is ever adopted it takes 39**, and the sentence above is kept as written
> because it dates the offer rather than states today's number. Both remain unadopted; still the
> chairman's.)*

**Entry 28 came to this table by a routing, and the routing is why it is here today.** The
2026-09-04 optimization log closes its entry with: *"routed to the archivist for the vault table
because `agents/` is outside this session's merge scope"* (`analytics/optimization-log.md:65`,
`1fcc1ab`). The council could adopt the rule and could not record it where this seat reads it.
That gap between adoption and recording is the whole of the archivist's job, and on this occasion
the council named the seat that had to close it. It is closed in this change set.

**What entry 28 caught, and why this seat should read the next paragraph rather than the
countermeasure alone.** Seven live instances in one day's record, four of them the chairman's,
**the fourth committed inside the correction of the third** (`0904-C1`, self-filed), and three
self-reported by the analyst. The chairman's accountability line reads: *"four unscreened
first-ness claims in one document, the fourth committed while correcting the third"*
(`state/council_log.json:475`). **None of the seven is a fabrication** — the optimization log is
explicit: *"each is true about the world and false about the record."* That is the distinguishing
mark of this entry against the rest of the table, and it is what makes it hard to see: the seat
making the claim is not being careless about the world, it is being careless about the project's
memory of itself. Which is this vault's subject matter, and this seat's.

- **25 · Mutable-reduction citation** (instrument family) — a citation to a relay reduction
  given as a path, when the file at that path can be overwritten in place. Countermeasure:
  every citation to a reduction carries the commit sha that holds it. A reduction is evidence;
  a path that can be rewritten is not a citation.
- **26 · Tautological instrument check** — a verification step whose result is guaranteed by
  the instrument's construction, reported as though it discriminated. Instance: `excerpt_of`
  centres its window on the *first* match by construction, so offset arithmetic cannot
  certify first-occurrence. Countermeasure: before reporting a check as evidence, ask what
  result the instrument was capable of returning.
- **27 · Scope-mixed screen** — a referent clause populated at a wider scope than the screen
  it annotates, so the clause cannot be checked by re-running the command it cites.
  Countermeasure: state each scope separately. Its standing corollary, adopted as a house
  rule the same day: **a grep establishes absence from the repository, never from the
  project** (`analytics/daily-research/2026-08-06.md:943`). **Keeps 27** under the ruling of
  2026-09-13; **cite by name.**
- **35 · Manufactured residual** — reporting a bucket as UNACCOUNTED under an anti-rounding
  rule when the split in fact reconciles exactly, so a rule written to stop smoothing instead
  plants a phantom irreducible remainder that later seats inherit and cannot dissolve.
  Countermeasure: an UNACCOUNTED declaration must be accompanied by the per-file enumeration
  that failed to close; if the enumeration is not shown, the residual is not established.
  **Adopted 2026-08-07 as 27; filed at 35 by the ruling of 2026-09-13; cite by name.**
- **36 · Untested counterfactual** — asserting what an alternative code path would produce
  without executing it. Countermeasure, in the officer's own words: **a counterfactual over
  code is executed or it is not filed. Adopted 2026-09-10 as 27, filed at 30 on the unmerged
  PR #170, and filed at 36 by the ruling of 2026-09-13; cite by name.**

**One further standing rule for this seat, adopted 2026-08-07 out of its own near-miss and
recorded here because it is a screening discipline, not a fabrication pattern:** *a zero-hit
screen is not absence until the synonym is tried.* The seat's `grep -c EGRESS_BLOCKED` over
the daily records hit today's file only and would have carried a false objection; the synonym
screen (`CONNECT tunnel`, `egress`) showed all six sessions. The chairman ruled it a standing
rule of the council beside the grep-before-asserting rule
(`analytics/daily-research/2026-08-07.md:1029`).

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

- **2026-09-22** — **Entry 41 and extension 40a filed; the heading moved 40 → 41; the pending
  block grew from three patterns to five.** Both numbered adoptions are from **2026-09-20**
  (`analytics/daily-research/2026-09-20.md:1315` and `:1323`, `1d6e3e7`) and reached this file two
  days late — **D15** at occurrences twelve and thirteen. The two new pending patterns are
  *one-pass artefact read* (2026-09-20, `:1334`) and *screen-record self-falsification*
  (2026-09-22, `:946`, `a814d18`), the latter adopted unnumbered together with the analyst's
  narrower variant (`:1218`, `a9bc44f`).
  **Where this note would have prevented a recorded failure, stated because the mandate asks for
  it.** On **2026-09-21** this seat had to write a vault-currency caveat into its own memo — *"Entry
  41 and extension 40a … have not reached the vault"* (`2026-09-21.md:753`, `224cbfb`) — and on
  **2026-09-22** it spent a measurement establishing the same thing (`:942`, `a814d18`) and then
  **cited 40a twice in the memo out of a file that did not carry it** (`:816`, `:880`). Had this
  note been current on either morning, neither paragraph would have been written and neither
  citation would have been unsourceable at its own authority. **No objection was wrong and no
  ruling was affected** — the cost was paid entirely in the seats' own verification time and in a
  record that documents its own memory failing. That is the failure mode this note exists to
  prevent, and it did not prevent it.
  *Audited against `1cf6108`; paths: `.claude/agents/integrity-officer.md`,
  `prompts/council_security.txt`, `analytics/daily-research/`, `agents/integrity-officer.md`.*
- **2026-09-13** — **The numbering ruled, and the collision closed in one change set,
  thirty-seven days after it opened.** The chairman's rulings session of 2026-09-13, item (a),
  settled C11 (open since 2026-08-07) and D17 (opened 2026-09-13) together: `main`'s table is canonical, **first adoption
  keeps the number, every later colliding adoption moves to the tail, never into a gap.**
  *Scope-mixed screen* keeps **27**; *manufactured residual*, adopted 2026-08-07 under the same
  number (`7adfd68`), is filed at **35**; *untested counterfactual*, adopted 2026-09-10 under the
  same number again (`analytics/daily-research/2026-09-10-special-session.md:552`) and filed at
  **30** on the then-unmerged PR #170, is filed at **36**. **PR #170's filing at 30 and its
  reservations at 31 and 32 are void**; 30, 31, 32, 32a, 33 and 34 are occupied on `main` and did
  not move. A **dated concordance** was added under the table so that every pre-ruling citation —
  every "27", every "27 ⚠", the branch-era "30", and the "reserved at 31 and 32" language —
  resolves to the right pattern; the ruling's operative holding is transcribed verbatim there,
  because the rulings record is not itself a file under version control in this repository and
  this note is its citable carrier. **Cite-by-name is permanently binding for all three.** The
  heading moved from "34 entries" to "36 entries" **in the same change set as the rows**, which is
  this table's own maintenance rule. Nothing already correctly numbered was renumbered. Enabling
  facts: PR #170 merged at `3099610`, the special session's 1,267-line record landing on `main` at
  `188cabe` and its vault close-out at `c894a4b`. **Two certifications this seat now owes, both
  from rulings of the same day and both recorded in [[Workflow Threads]]:** the band-clause sheet
  `analytics/locked_set/BAND_CLAUSES.md` must be certified **unreordered, unabridged and carrying
  no emphasis favouring any band** before the coding packet ships (**S13**), and the candidate
  list's **disjointness certificate at the level of the MATTER, not the document** must be
  certified before a single row is committed (**S10**). A supplementary ruling also binds the item
  pool: **no item may be drawn from a pool carrying the instrument's own verdict on that item** —
  the archived digests are exactly such a pool — with the live draw accepted under a
  capture-witness requirement and every captured item excluded from production screening through a
  reservation list, logged per run. Gap **G-3** is open and **unruled** (**S15**). *Recorded on
  `vault/taxonomy-concordance`; the rulings record itself is not in this repository at the time of
  filing.*

- **2026-08-09** — **Round two: three passages, zero adopted, and the exemption is the
  interesting one.** Uncommitted, `fix/restore-council-label`; recorded at
  `working/benavides-comment-replies-2026-08-08.md:6`. The humanizer was re-run over the three
  materially revised passages from the parity round.
  - **One exempt by construction.** The H&H descriptive annotation, once masked, is a **near-pure
    sentinel chain** — there is essentially nothing left for a rewriting pass to act on. This is
    worth naming as a category rather than a one-off: **when a passage is almost entirely
    protected spans, the masking step has already answered the question**, and running the pass
    would produce a diff consisting of connective tissue. Exemption here is a finding about the
    passage's density of sourced material, not a waiver.
  - **Two run and rejected at the gate.** The Ferguson *Vanda* paragraph **dropped the passage's
    final two sentences and converted "the opinions" — the court's — into "the author's
    opinions"**, which is a change of who is speaking, not of style. The H&H relevance paragraph
    **destroyed a sentinel and garbled the triple-identity sentence**. Canonical text stands for
    all three passages.
  - **The cumulative record now reads: ten passages run across two rounds, two adopted.** Every
    rejection in both rounds was for one of the same four failures — fabricated quotation,
    flipped negation, hallucinated rule, destroyed sentinel — and **none was repairable by
    splicing**, which is why the fail-closed rule is a rule rather than a preference. A pass
    that rewrites *who said a thing* (round 2) sits in the same family as one that rewrites
    *whether a thing was denied* (round 1): both are meaning changes that read as fluent prose.
  *Audited against `2686422` + working tree on `fix/restore-council-label`; paths:
  `working/benavides-comment-replies-2026-08-08.md`, `lit-review/ferguson-memo.md`, `seeds/`.*
- **2026-08-08** — **The gate held five times, and the number is the point.** All
  uncommitted, branch `fix/restore-council-label`.
  - **Fail-closed on a rewriting pass.** A humanizer was run over all seven substantive
    replies in `working/benavides-comment-replies-2026-08-08.md`, with **every quotation,
    citation and pinpoint sentinel-masked** before it saw the text. **Two** outputs passed the
    mechanical gate and were surgically repaired (Items 2 and 4.1); **five were rejected
    outright** — fabricated quotation, flipped negation, hallucinated rule, and two sentinel
    destructions; **two** were exempt as short mechanical replies. A 5-of-7 rejection rate on
    a style pass over already-verified text is the strongest available evidence for the rule
    this seat has been asserting since 2026-08-04: **a rewriting step is a fabrication
    surface, not a formatting step.** Entered as a binding rule in [[Agent Registry]].
  - **Substantive review of the ring-at-25 entries.** Four published entries display a ring at
    score 25 and this seat assessed each against its own annotation
    (`analytics/retrospective-audit-2026-08-08.md` §2). **Two are unsupported**: the 2026-06-22
    Cour de cassation entry (ICC-award enforcement, the forum's own act, no investor-State
    proceeding in the item) and the 2026-06-29 Santiago set-aside (whose annotation applies
    the wrong test on its face — "by virtue of being a court judgment"). Both additionally
    **contradict the classifier contract**, under which a judicial ring implies at least
    MEDIUM. All four now carry dated corrections in the archive.
  - **Two negative conclusions withdrawn as unsupported by their own evidence.** The Gazprom
    entry concluded "no ISDS thematic intersection" about a **body the instrument never
    read**; the correction records the honest status as "not assessed — body not retrieved,"
    which is neither a positive nor a negative finding. This is taxonomy entry 11
    (status-as-record-artifact) in a new dress: **an access limit was reported as a
    substantive result.**
  - **Nine dated appends, zero rewrites.** Every archive correction was appended under a dated
    heading with the original text left intact above it.
  - **What was NOT converted.** Nothing PENDING became verified by inference. The *Saluka* and
    *Bovine Hides* "extracted and verified" claims had no repo source and **stayed withdrawn**;
    the eleven externally gated retrievals at `analytics/locked_set/RETRIEVAL_LEDGER.md` remain
    QUEUED or BLOCKED; reporter page pins and appellate status for Vanda were **expressly
    excluded** from the closure.
  *Recorded against the working tree of `fix/restore-council-label` (uncommitted); paths:
  `working/benavides-comment-replies-2026-08-08.md`,
  `analytics/retrospective-audit-2026-08-08.md`, `analytics/locked_set/RETRIEVAL_LEDGER.md`,
  `digests/2026-06-22_…`, `digests/2026-06-29_…`, `digests/2026-07-06_…`,
  `digests/2026-08-03_…`, `digests/2026-06-09_…`, `digests/2026-06-10_…`.*

- **2026-08-07** — Three sessions of adopted entries reached this note: **25** (mutable-reduction
  citation, 2026-08-05), **26** (tautological instrument check, 2026-08-06) and **27** (scope-mixed
  screen, 2026-08-06), plus the 2026-08-07 *manufactured residual* recorded under the colliding
  number it was actually given. The count in the heading was three days and three entries stale,
  and the cost is measurable rather than hypothetical: this seat read the stale heading on
  2026-08-07 while numbering a new entry and the collision is the result. Also recorded: the
  zero-hit-screen-needs-a-synonym rule (`7adfd68`). The trade this note's own "what the rewrite
  costs and what it buys" paragraph named — a list that drifts silently, exchanged for a read that
  can be silently skipped — failed on the *third* term nobody priced: the read happened, and what
  was read was out of date. Model, definition and prompt bindings unchanged (`git log
  b76f6c3..HEAD -- .claude/agents/integrity-officer.md prompts/council_security.txt
  prompts/council_calibration.md` returns only `bfc8ef6`, which predates this note's own anchor).
  *Audited against `7c08dcf`; paths: `.claude/agents/integrity-officer.md`,
  `prompts/council_security.txt`, `prompts/council_calibration.md`,
  `analytics/daily-research/`, `views/isds-workflow-3d/workflow.json`.*
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
