---
aliases: [Claim Map]
tags: [agent, council, claims]
hub: Evidence Ledger
---
# Claim Map

**Currency anchor.** *Audited against `057185a`.* Machine-owned; `scripts/reanchor.py` moves the sha to the session's last substantive commit in a notes-only close-out commit that `scripts/check_currency.py` excludes from drift as maintenance. Do not hand-edit the sha; the dated snapshot-anchor narrative below is preserved unedited as history.

**What this is.** One row per factual claim the project makes *about itself*, listing
**every file that states it** and **what each file currently says**. It exists because the
external review of 2026-08-04 found ten contradictions, and **eight of them were the same
fact stated differently in two places** — not a wrong fact, a fact that had drifted between
its twins. Nothing in this vault indexed claims, so nothing could catch that class. The
agent registry indexes *seats*; the change log indexes *changes*; this note indexes
*assertions*.

**How to use it, and the rule that makes it worth maintaining.**

> **A claim is not changed until every file listed against it is changed in the same change
> set.** If you fix a number in one file and this note lists five, you have not fixed the
> claim — you have moved the contradiction.

Before editing any file in a **Stated in** column, read that claim's row. After editing,
update the row in the same change set. A row whose file list is stale is worse than no row,
because it licenses a partial fix.

**Snapshot anchor — moved 2026-08-25 at the archivist session.** *Audited against `ad66a96`;
paths: `METHODOLOGY.md`, `STATE_OF_THE_ANSWER.md`, `lit-review`, `prompts`, `.claude/agents`,
`scripts/site_templates`.*

**C11 re-read cell by cell again, and it is still DIVERGENT — nine days live now.** Every cell
opened at `ad66a96`, not inferred from the previous reading and not from any commit message:

| Cell | Reads | State |
|---|---|---|
| `scripts/site_templates/how_it_works.html.j2:3` | "the **nine** public sources" | still nine |
| `scripts/site_templates/how_it_works.html.j2:27` | "the first band is the **nine** public sources checked" | still nine |
| `docs/how-it-works.html:7` (meta description) | "the **nine** public sources" | still nine |
| `docs/how-it-works.html:58` | "the first band is the **nine** public sources checked" | still nine |
| `docs/how-it-works.html:96` (inlined SVG banner) | "THE **10** SOURCES, CHECKED EVERY RUN", ten chips | ten |
| `README.md:56` | "the **ten** sources" | ten |
| `views/isds-workflow-3d/workflow.json` | `chips` = **10** | ten |
| `src/sources.all_sources()` | returns **10** instances | ten |

**One fact worth more than the repetition: `docs/` was rebuilt twice in this window and carried
the error through both.** `git log c4f6825..HEAD -- docs/how-it-works.html` returns `dc7b207`
and `719a9fc`, both "chore: weekly digest + state update". The build is faithful and the
template is the defect, exactly as recorded on 2026-08-22 — so this will survive every future
rebuild until two sentences in the `.j2` change. Owner remains **[[site-experience]]**;
escalated, not edited, for the third session.

**Previous snapshot anchor — moved 2026-08-22 at the archivist session.** *Audited against `c4f6825`;
paths: `METHODOLOGY.md`, `STATE_OF_THE_ANSWER.md`, `lit-review`, `prompts`, `.claude/agents`,
`scripts/site_templates`.* **C11 re-read cell by cell and found DIVERGENT** — see the row. The
public site's prose still says nine sources while the chart on the same page says ten.

**CORRECTION, applied here 2026-08-22 to the block below.** The 2026-08-17 anchor block asserted:
*"C12's source-count row is satisfied by that same commit (ten stated once, everywhere)."* That
sentence is wrong twice, and both errors are this seat's.
**(1) Wrong row.** The source-count row is **C11**; **C12** is Model assignments.
**(2) Wrong fact.** The row was **not** satisfied. `44550ca` moved `README.md`, `workflow.json`
and both SVGs to ten and left `scripts/site_templates/how_it_works.html.j2:3` and `:27` — and
therefore `docs/how-it-works.html:7` and `:58` — saying nine. "Ten stated once, everywhere" was
taken from `44550ca`'s commit message rather than from a reading of the files, which is the exact
substitution this map exists to prevent. The original wording is quoted above and the erroneous
sentence is struck below rather than deleted.

**Snapshot anchor — moved again 2026-08-17 at the fleet rebuild.** *Audited against `44550ca`* —
the ten-sources commit regenerated the workflow SVG under `scripts/site_templates`, a declared
path of this map; ~~C12's source-count row is satisfied by that same commit (ten stated once,
everywhere)~~ — **struck 2026-08-22: the row is C11, and it was not satisfied. See the correction
above.**

**Snapshot anchor — moved 2026-08-17 at the source-outage repair.** *Audited against `2576896`.* The drift since `d997c32` is the 2026-08-17 council session's own
commits; no claim moved.

**Snapshot anchor — moved 2026-08-16.** *Audited against `d997c32`* (`main`, clean tree,
complete 621-commit history). This restamp is narrow and earned, and the reasoning is given so
the next session can judge it rather than trust it. The 2026-08-13 session deliberately left the
anchor stale, saying it had not re-read the rows; this pass did the reading, and it was cheap
because the drift surface turned out to be one file.

- **Of this map's declared paths, exactly one moved.** `git log a22f4cb..HEAD --
  .claude/agents/ prompts/ METHODOLOGY.md lit-review/ scripts/site_templates/ src/config.py
  README.md` returns **zero commits**. Every C-row pinned to those paths — which is nearly all
  of them, including all of **C15** and **C16** — therefore cannot have drifted, and this is a
  proof rather than a spot check.
- **All ten stale commits touched `STATE_OF_THE_ANSWER.md` and nothing else**, and this map
  cites that file in four places. All four were re-read at their quoted text on 2026-08-16.
  Two were correct as written (`:4` "live, litigated", `:8` "Apotex outer limit"). **Two had
  drifted and are fixed in place:** the operator-verification quote moved `:58` → **`:66`**,
  and the Ring 3 taxonomy heading is at **`:122`**, not the range `:114-124`, which now opens
  inside the Day 11/12 UNCITRAL entries. In both cases the *text* is unchanged and only the
  position moved — a pinpoint going stale, not a claim going false.
- **What this restamp does not assert.** It does not assert that C15's three survivors or
  C16's five are re-argued or closed; they are open and unmoved. It asserts that no declared
  path changed under them, which is the only thing the anchor is for.

**Superseded — snapshot anchor moved 2026-08-11 at integration.** *Audited against `a22f4cb`*, the
merge of the integration branch with the 2026-08-11 council session. The commits since
`2686422` that touched this map's declared paths are the integration's own (the vault
surfaces, the lit-review memos, the regenerated workflow SVG) and the council's
2026-08-08..11 session records, including the session's STATE_OF_THE_ANSWER update. C15
and C16 stand as written; the divergence lists are unchanged by the merge.

**Snapshot anchor — moved 2026-08-09.** *Audited against `2686422`* plus the uncommitted
working tree of the 2026-08-08 repair session **and the 2026-08-09 audit-response session**,
on branch `fix/restore-council-label`. **C15 was re-read row by row against the tree in this
pass, and C16 is new.**
Superseded anchors, retained so the history of the map reads straight: the previous anchor was
2026-08-08 at the same `2686422` plus that day's tree; rows C1–C12 were
originally audited against `c9050e6` (`main`, 2026-08-04), and C13 and C14 were added
2026-08-05 against `eac8ed9`. The branch is named — said in those words
because most of that session is *not committed*, and a row citing an uncommitted line is
citing a file path on a branch, not a hash. Paths claimed to be described: `README.md`,
`METHODOLOGY.md`, `HUMAN_REVIEW.md`, `HANDOFF.md`, `COUNCIL.md`, `fingerprint.yaml`,
`prompts/`, `.claude/agents/`, `moc/`, `working/`, `think-tank/`, `docs/`,
`scripts/site_templates/`, `scripts/`, `src/`, `templates/`, `tests/`, `digests/`,
`views/isds-workflow-3d/`. Staleness is a one-command question:
`git log 2686422..HEAD -- <those paths>` **plus** `git status --short` while the session
remains uncommitted.

> ⚠ **KNOWN STALE as of 2026-08-07, and deliberately not re-anchored.** The archivist's session
> of 2026-08-07 ran `python3 scripts/check_currency.py` and this note reports **27 commits**
> touching its declared paths since `c9050e6`. Fourteen of the sixteen rows were **not** re-audited
> that day — a re-audit means re-opening every file in every **Stated in** column, and the session
> did not have the budget to do it honestly. **The anchor below was left untouched on purpose:**
> bumping an anchor without re-reading the files is the precise defect `check_currency.py` was
> written to catch, and a row that reads as fresh while being stale is the thing this note warns
> about in its own second paragraph. Treat every row as last-verified at its stated anchor and
> re-check the file before relying on it. Refreshing this note is the next archivist session's
> first substantive task.

**Snapshot anchor.** Rows C1–C12 were audited against `c9050e6` (`main`, 2026-08-04, clean
tree). **Rows C13 and C14 were added 2026-08-05 and are audited against `eac8ed9`** (`main`,
clean tree), together with the corrections to C7 and C12 noted in their rows. Paths claimed
to be described: `README.md`, `METHODOLOGY.md`, `HUMAN_REVIEW.md`, `HANDOFF.md`,
`COUNCIL.md`, `fingerprint.yaml`, `prompts/`, `.claude/agents/`, `moc/`, `working/`,
`think-tank/`, `docs/`, `scripts/site_templates/`, `scripts/`, `src/`, `templates/`,
`tests/`, `digests/`. Staleness is a one-command question:
`git log eac8ed9..HEAD -- <those paths>`.

**What the 2026-08-09 re-pointing found, before any individual row.** Two things, and the
second is the reason this map exists.

1. **C15 is five-eighths repaired, not resolved — and this pass was briefed that it was
   resolved.** Each of the eight ⚠ rows was re-read in the file rather than taken from the
   session report. Five now carry the suspension (`METHODOLOGY.md:49` by inline amendment,
   `README.md:80-86`, `HANDOFF.md:100`, `scripts/site_templates/index.html.j2` step 5, and the
   `templates/digest.html.j2` clause that was already unreachable). **Three do not:**
   `fingerprint.yaml:5-6`, the `quality-bar` card at `views/isds-workflow-3d/workflow.json:177`,
   and the `src/main.py` comment that names a "never-empty / watch-list-floor rule" — which
   moved from `:497-500` to **`:687-690`**, so a line-number search would have missed it. The
   row is corrected below rather than closed. **A row is closed by the files, not by a report
   that the work is done.**
2. **The repair created its own successor divergence, in the same shape, on the same day.**
   `VALIDATION_STATUS_ONLY` now holds item publication **including items at or above 40**.
   Every sentence repaired in (1) says the opposite — that items at or above the threshold are
   surfaced — so the five files that were just brought current with the *first* gate are
   already stale against the *second*. `METHODOLOGY.md` carries both readings twenty lines
   apart, which is precisely the C6 failure shape the 08-08 pass recorded and resolved to stop
   producing. That is **C16**, new below.

**What the 2026-08-08 re-pointing found, before any individual row.** Between `eac8ed9` and
this pass the map went three days without an audit while two rulings landed, and the map did
not move with either:

1. **C13 is CLOSED and this note was the last file still describing it as open.** The Ring 3
   dimension/disposition split was decided for **Definition A** and implemented across the
   tree at `ae1f04b` and `373cce6` (2026-08-06), with the site strings at `9bd112e`. Thirteen
   of the fifteen B statements this row tabled are gone; the row is corrected in place below.
2. **A new divergence was created on 2026-08-08 and it is the largest live one in the map:**
   the fill-toward-six rule is suspended by default in code and is still stated as operative
   in **seven** other places, one of them the public homepage and one of them
   `METHODOLOGY.md` eighteen lines above the addition that suspends it. That is **C15**, new
   below.
3. The `docs/*.html` lines in every row lag their sources until this session is committed and
   `scripts/build_site.py` is re-run; `scripts/check_site_sync.py` correctly reports the gap.
   Per the generation rule below, that is expected, not drift.

**Line numbers are as of the 2026-08-08 pass** and will drift as files are edited. Where a
line moves, the quoted text is the durable identifier — search for it rather than trusting
the number.

---

## The generation rule that governs half of these rows

`docs/` is **generated** from `METHODOLOGY.md`, `digests/` and `scripts/site_templates/*.j2`
by `scripts/build_site.py`. `scripts/check_site_sync.py` (gate:
`.github/workflows/site-sync.yml`) rebuilds and **fails the PR** if `docs/` differs by
anything other than the build-stamp footer.

Consequence for every row below: a `docs/*.html` line is **never** the place to fix a claim.
Fix the `.j2` template or `METHODOLOGY.md`, then rebuild. Editing `docs/` directly produces a
change that the next build silently reverts, and the gate will reject it. Rows list the
`docs/` locations anyway, because they are what a reader — and the reviewer — actually saw.

---

## C1 — Holdout size and headline accuracy — **CLOSED 2026-08-04, re-verified 2026-08-05**

**This row was written DIVERGENT against `c9050e6` and the divergence was closed the same
day at `7959777` ("fix(claims): close the reviewer's contradictions, and stop stating one
fact two ways"). Re-measured against `eac8ed9` on 2026-08-05, every figure below now agrees.**
The stale version of this row survived one full day in this note, which is the failure mode
the map's own §2 warns about: *a row whose file list is stale is worse than no row, because
it licenses a partial fix.* It is corrected in place rather than deleted, so the correction
is legible.

| Stated in | What it currently says |
|---|---|
| `scripts/holdout_set.json` | **20 items**, 4 labelled `label: 1`, 16 unlabelled negatives. Consumed by `scripts/eval_holdout.py`. |
| `scripts/backtest_corpus.json` | **20 items** — `holdout_positive_ids` **4**, `holdout_negative_ids` **16**, `display_names` **20**. Consumed by `scripts/backtest.py`. Its `_holdout_invariant` now requires the two id lists to name **every** labelled item in `holdout_set.json`. *(Was 4 + 8 and a "~12-15 known cases" note at `c9050e6`.)* |
| `METHODOLOGY.md:52` | "an exploratory holdout of **twenty** items using eval_holdout.py. Four of the twenty were on-theme positives … compared against **sixteen** other awards … a precision of 1.00, a recall of 0.75, and an **accuracy of 0.95**, for an F1 of 0.86" |
| `METHODOLOGY.md:71` | "The small exploratory hold-out set in Part VI.B — **twenty items, only four positives**" *(was `:67`; moved by the §VI.B and §IX additions of 2026-08-08)* |
| `METHODOLOGY.md:54` | **New 2026-08-08, uncommitted on `fix/restore-council-label`.** A dated correction under the same paragraph, adding the exact Clopper–Pearson 95% intervals — **[0.19, 0.99]** on three-of-four, **[0.79, 1.00]** on sixteen-of-sixteen, **[0.29, 1.00]** on three-of-three — and stating that "no derived rate from this set should be quoted as instrument-level performance". It does **not** change any of the four figures, so C1 stays CONSISTENT |
| `docs/methodology.html:118` / `:126` | The same two sentences, generated. *(`:112` at `c9050e6`; the line moved — quoted text is the durable identifier.)* **Lags the source until the 2026-08-08 session is committed and `docs/` rebuilt** |
| `scripts/site_templates/backtest.html.j2:114` | "{{ bt.holdout.total }} cases in all, none used in development" |
| `docs/backtest.html:155` | Renders as "**20 cases** in all, none used in development" |
| `docs/backtest.html:161` | "Confusion matrix … across **20**" |
| `docs/backtest.html:175-183` | TP 3, FN 1, FP 0, **TN 16** |
| `docs/backtest.html:202-205` | precision **1.00**, recall **0.75**, accuracy **0.95**, F1 **0.86** |
| `scripts/check_claims.py:195-238` | Facts 6–12 now hold this agreement mechanically, harness against prose |
| `tests/test_check_claims.py:53-55` | `assert a["n"] == b["n"] == 20`, `n_pos == 4`, `n_neg == 16` — the two harnesses are asserted equal independently of the registry |

**Status: CONSISTENT. One dataset, twenty items, 0.95 on every surface.** 3/4 + 16/16 =
19/20 = 0.95. The `0.92` figure now exists only as history — in `check_claims.py:16-19` and
`.github/workflows/claims-consistency.yml:7-10`, both of which describe it as the drift the
guard was built to prevent.

**A fix here must also change:** nothing — there is nothing to fix. **Watch for a new
divergence:** the agreement is now *mechanical*, so the hazard has inverted. Anything that
changes the holdout's size, labels, or scores — including the `apotex_v_us` repair in
**C14** — moves the harness figures and puts `METHODOLOGY.md:52` out of agreement, and
`check_claims.py` fails the build rather than letting the prose drift. Read **C14** before
touching `scripts/holdout_set.json`.

**Added 2026-08-08 — the qualifier that belongs on every future use of these figures.** The
`METHODOLOGY.md:54` correction records that the harness evaluates at a score of **forty**,
and that across 347 screenings in eleven runs **no candidate has ever reached forty**. The
0.95 is therefore measured at a boundary the production path has never crossed. The figures
in this row are internally consistent, which is all C1 ever claimed; they are not evidence
about what the instrument publishes. That question is **C15**, and the locked set designed to
answer it (`analytics/locked_set/SCHEMA.md`) holds **zero items by design**.

---

## C2 — Ring-presence floor and strong subtotal

| Stated in | What it currently says |
|---|---|
| `src/classify.py:118` | `PRESENT_FLOOR = 12` *(was `:47`; Phase 0/1 additions of 2026-08-08 moved it)* |
| `src/classify.py:121` | `STRONG_SUBTOTAL = 18` *(was `:50`)* |
| `src/classify.py:271-308` | The bands actually computed from those two constants *(was `:200-225`)* |
| `fingerprint.yaml:110-118` (`combination_rules`) | ✔ **The 30 is gone.** The rules now name "the present floor (**12**)" and "the strong-single-ring floor (**18**)", i.e. the two constants in the code *(was `:100`, `:103`, `:104`)* |
| `fingerprint.yaml:104-109` (header) | The provenance note, added with the fix: "**DESCRIPTIVE ONLY** — nothing in the codebase reads these strings. `src/classify.py` is the authority… `scripts/check_claims.py` fails the build if the two disagree. **Before 2026-08-04 these rules described a 'subtotal >= 30' bar that appears nowhere in the code and had never changed a score.**" |
| `fingerprint.yaml:119-121` | Worked boundaries "measured against the live scorer on 2026-08-04" |
| `METHODOLOGY.md:47` | States the **floor of twelve** (agrees with `PRESENT_FLOOR`) and the **threshold of forty**. **Still never states a strong subtotal at all.** |
| `docs/methodology.html:115` | Same sentence, generated. |

**Status re-measured 2026-08-08: CLOSED, and mechanically held.** `fingerprint.yaml` and
`src/classify.py` now name the same two constants, the file says in its own header that it is
descriptive rather than authoritative, and `scripts/check_claims.py` fails the build if they
part company. The retained note about the retired "30" is the right shape of fix: it records
that the bar existed and that **it had never changed a score**, which is the fact a reader
needs in order not to re-derive the old numbers from an archived digest.

**The gap that is not closed, and should not be read as closed:** `METHODOLOGY.md:47` still
documents only one of the two constants that decide banding. The public methodology is
*silent* on `STRONG_SUBTOTAL`, not wrong about it. **A fix here must change** `METHODOLOGY.md:47`
plus a rebuild of `docs/methodology.html` — and nothing in `fingerprint.yaml`, which is now
correct. **Watch for a new divergence:** the `combination_rules` block is prose that no code
reads. Its only defence is `check_claims.py`; if a boundary is changed in `src/classify.py`
and the guard has no fact covering it, this block goes quietly false again.

---

## C3 — Digest threshold and relevance floor

| Stated in | What it currently says |
|---|---|
| `fingerprint.yaml:10` | `threshold: 40` (with a comment at `:2-9` recording the move from 60) *(was `:5`)* |
| `src/config.py:94` | `_threshold_from_fingerprint()` reads it from `fingerprint.yaml`, falling back to **60** *(was `:77-86`)* |
| `src/config.py:27-28` | `MIN_DIGEST_ITEMS = 6`, `RELEVANCE_FLOOR = 25` — **both unchanged 2026-08-08.** The suspension did not move either number; it gates whether the fill runs at all (`src/config.py:31-39`), which is why a numbers-only sweep finds nothing wrong. See **C15** |
| `README.md:79-82` | "fills up to a minimum of six items with the closest near-misses, but only those at or above a relevance floor of 25 (`MIN_DIGEST_ITEMS=6`, `RELEVANCE_FLOOR=25` in `src/config.py`)" *(was `:72-75`)* — **the numbers are right and the behaviour it describes is suspended; see C15** |
| `HANDOFF.md:99-101` | "only down to `RELEVANCE_FLOOR=25`, so a quiet week may carry only 0–3 items" — **same qualifier; see C15** |
| `METHODOLOGY.md:47` | "The digest threshold of forty … sits twenty below the original figure." |
| `views/isds-workflow-3d/workflow.json`, `quality-bar` card | Cites **`src/config.py: threshold 40 / floor 25`** — the threshold does not live there |

**Status: CONSISTENT on the numbers; ONE wrong file citation, already on record.** The
`quality-bar` card's citation is open drift, raised 2026-08-03, re-verified 2026-08-04
(`agents/Project Change Log.md`, Open drift; `agents/obsidian-archivist.md` slice item 4).
It is a systems-designer fix on Emory's go-ahead, regenerated from the manifest, never
hand-edited.

**Second defect on the same card, found 2026-08-08 and not previously recorded.** The
`quality-bar` card's `desc` reads "Items scoring 40+ enter the digest. **Near-misses (25+) may
fill a quiet week**, always labeled as leads," and its `meta` reads "Emory's fixed rule — 40
pass, 25 floor". Both describe the fill as operative; it is suspended by default as of
2026-08-08. The card is therefore wrong on *behaviour* as well as on *file location*, and the
two must be fixed in the same manifest edit or the second fix will look like the whole fix.
Same owner, same rule: manifest edit by [[systems-designer]] on Emory's go-ahead, never a
hand-edit of the generated chart.

---

## C4 — Matching method

| Stated in | What it currently says |
|---|---|
| `src/classify.py` | Literal case-insensitive substring containment over normalised text; no stemmer, no lemmatiser, no token boundaries |
| `METHODOLOGY.md:29` | "searched for within each field of an item … as a **case insensitive substring rather than as a whole word**. Therefore, the trigger will fire regardless of what words are immediately before and after … **The fingerprint holds no truncated stems**, and it does not identify variations through lemmatization or regular-expression pattern matching; **a phrase is found only where it appears literally.**" *(Re-read 2026-08-08. The "stem forms such as **expropriat-**" clause this row quoted from `c9050e6` **no longer exists**; it was removed at `f565407`.)* |
| `METHODOLOGY.md:71` | "The lexical matcher uses **case-insensitive substrings** rather than lemmas, **and holds no truncated stems**" *(was `:67`; the sentence itself was rewritten before this pass and now says the matcher holds **no** truncated stems — see the divergence warning below)* |
| `docs/methodology.html:106` / `:126` | Same, generated. |
| `fingerprint.yaml` | The phrase entries themselves — where a "stem" is a truncated literal, e.g. the trailing-hyphen forms |

**Status: CLOSED 2026-08-08 — the wording hazard is gone, and the resolution went the
opposite way from the one this row predicted.** `METHODOLOGY.md` no longer uses "stem form"
at all: both `:29` and `:71` now say the fingerprint holds **no** truncated stems, and that
is **true of the file as it stands** — a scan of `fingerprint.yaml` for phrases ending in a
hyphen returns **zero**. The trailing-hyphen entries the row was written around are not in
the tree. The two sentences agree with each other and with the data.

**A fix here must also change:** both `METHODOLOGY.md` sentences (`:29` and `:71`) in the
same edit — they are the same claim twice — then rebuild `docs/`. **Watch for a new
divergence, restated for the state the file is actually in:** the two sentences are now
*conditional on the data*. Adding a single trailing-hyphen phrase to `fingerprint.yaml`
makes both of them false at once, and nothing mechanical checks it — `scripts/check_claims.py`
carries no fact for truncation. The row stays in the map for that reason, closed rather than
deleted.

---

## C5 — Empty-report behaviour — **CLOSED on the published surfaces 2026-08-08; ONE residual, and it is the one this row predicted**

| Stated in | What it currently says |
|---|---|
| `src/main.py:92-120` (`select_surfaced`) | "No item below `floor` is ever surfaced under either setting," and the fill above it is now conditional. **This is the behaviour.** *(was `:53-69`)* |
| `src/main.py:497` (comment) | **RESIDUAL — still says** "an empty digest contradicts the **never-empty** / watch-list-floor rule" *(was `:272`)* |
| `src/main.py:500` (same comment) | **RESIDUAL — still says** the honest quiet-week note is "no thematically relevant developments, N screened". The code twelve lines below no longer emits that string: `src/main.py:510-518` builds a *status-only* subject, and the body comes from `src/render.py:59` |
| `scripts/site_templates/index.html.j2` | ✔ **"never empty" is gone.** A grep of the whole `scripts/site_templates/` tree for "never empty" / "never-empty" returns nothing |
| `docs/index.html` | ✔ Gone, generated from the repaired template |
| `fingerprint.yaml:2-9` | ✔ **Reversed.** Now reads "There is **NO non-empty-digest guarantee**… A week in which nothing reaches the relevance floor **produces an empty digest**, and the digest says so plainly along with the number of candidates screened" |
| `README.md:83-86` | "Honesty is preferred over **padding**: a genuinely quiet week may carry only **0–3 items**, and a week with nothing above 25 sends a one-sentence note (**"no thematically relevant developments this week — N candidates screened"**)" — the *sentiment* survives; the **quoted wording is now wrong**, see **C15** *(was `:76-78`)* |
| `HANDOFF.md:89` | "A green run **always sends an email**, even a quiet week" — still true, and still compatible |
| `digests/2026-07-27_ISDS-Thematic-Watch/meta.json` | `screened: 10, matches: 0, watch_list_leads: 0, accepted: 0` |
| `digests/2026-07-27_ISDS-Thematic-Watch/README.md:3`, `:11` | "Screened: 10 · Matches (≥40): 0 · Watch-list leads: 0 · Watch-list leads shown (total): **0**" — and the table's only row: "_**No items met the relevance floor this cycle.**_" |
| `digests/2026-06-15_ISDS-Thematic-Watch/meta.json` | `screened: 14, matches: 0, watch_list_leads: 0, accepted: 0` |

**Status re-measured 2026-08-08: the promise is retired everywhere a reader can see it.** The
homepage sentence, the template that generated it, and `fingerprint.yaml`'s header comment
have all been corrected — the header comment now states the opposite proposition, which is
the strongest form of the fix. The two archived zero-item runs are unchanged and still settle
the question empirically.

**What is left is exactly the trap the previous version of this row named**, which is worth
saying plainly because the row called it and it still happened: **`src/main.py:497` is a code
comment, it appears in no prose sweep, and it is now the only place in the repository where a
"never-empty … rule" is spoken of as though a rule of that name exists.** Three days and two
correction passes went over the published copies and left it. It has since acquired a second
defect — the sentence at `:500` quotes wording the same function no longer emits.

**A fix here must also change:** `src/main.py:497-500` as one edit — the stale rule name and
the stale quoted note text are in the same comment block — and `README.md:85-86`, which
quotes that same retired note text to the reader. Both are **C15** work and should land in
that change set, not separately. **Watch for a new divergence:** do not repair the comment by
deleting it. It is the only in-code explanation of why an *empty run* (zero candidates
screened) sends nothing at all while a *zero-match cycle* sends a status note — two different
paths, four lines apart, that look identical from outside.

---

## C6 — Human-review status

| Stated in | What it currently says |
|---|---|
| `HUMAN_REVIEW.md:89` | ✔ **Gone.** The "_No human review has been logged yet_" paragraph is no longer in the file; `:87-91` now carries the standing verification-debt note instead |
| `HUMAN_REVIEW.md:96` | The Cycle 1 draft "**is a DRAFT, not a review** — no human has reviewed these claims" *(was `:94-98`)* |
| `HUMAN_REVIEW.md:172` | "### 2026-07-18 — Cycle 1 — COMPLETED (operator review, conducted in-session)" |
| `HUMAN_REVIEW.md:173-212` | A real operator review: reviewer named, three items, "Final pass rate: 1 verified + 1 partial / 3 assigned", "Sign-off: operator confirmation received in-session, 2026-07-18" |
| `HUMAN_REVIEW.md:65` | "**Standing rule.** Until a review cycle is logged for the period, the system's outputs for that" period are provisional |
| `STATE_OF_THE_ANSWER.md:66` | "**Operator-verified 2026-07-18** … (**first completed human-review cycle**, `HUMAN_REVIEW.md`)" *(was `:56`, then `:58`; **re-pinned to `:66` on 2026-08-16** — the quoted text is unchanged and was re-read at the new line, only its position moved as the council edited the living memory across ten commits)* |
| `scripts/site_templates/how_it_works.html.j2:50-61` | ✔ **The universal safeguard claim is gone**, replaced at `33861fd` ("make the 'no human has checked this' disclosure a number that can move") by a **counted** disclosure: "One operator review… one verified against a primary source, one partially," and a rendered count of entries "**opened by the operator and checked against the original source**" |
| `docs/how-it-works.html` | Same, generated |
| `METHODOLOGY.md:41` | "they do not remove the need for human-in-the-loop review, and the digest annotations **are meant to be verified by a reader** before they are relied upon" |
| `analytics/verification_ledger.jsonl` (`main`) | **21 operator marks, 37 claims**. A further **17 marks and 3 claims** exist only on `origin/chore/operator-marks-2026-07-27` and have never reached `main` — see [[Workflow Threads]] F1 |

**Status re-measured 2026-08-08: CLOSED on both legs.** The intra-file contradiction is gone
(the "none logged yet" paragraph no longer exists, so nothing in the file contradicts the
logged cycle at `:172`), and the site's universal safeguard claim has been replaced by a
counted one that the ledger can actually support. `33861fd` is the commit that did the second
half; the first half is not attributable to a single commit from this pass and is recorded as
"verified absent 2026-08-08" rather than assigned a hash it may not have earned.

**Watch for a new divergence:** the site's disclosure is now a **rendered number**, so it can
go stale the way a sentence cannot — it moves whenever the ledger moves, including if the 17
unmerged marks in F1 ever land. That is a feature, but it means the claim's authority is the
ledger file, and the ledger file has a seventeen-mark gap sitting on a branch.

**Also here, and still open:** `HUMAN_REVIEW.md:115` reads "The operator (**Jack**) must
complete the blank fields". The operator is **Emory** everywhere else in the project; `:173`
correctly reads "Jack Emory Williams (operator)". Unchanged since this row was written, in a
file a reader reaches from the public repository. *(Line was `:116` at `c9050e6`.)*

---

## C7 — Agent architecture ("research council")

| Stated in | What it currently says |
|---|---|
| `README.md:91-93` | "the brief is produced by what the project calls its research council: **not a set of standing background agents, but a set of clearly-defined roles realized as coordinated stages of the same weekly run**" *(was `:85-87`)* |
| `README.md:102` | "**Each role is a prompt or pipeline component**" *(was `:95`)* |
| `METHODOLOGY.md:61` | **Rewritten since this row was drafted.** No longer "a standing council of research agents". Now: "This brief is produced by a **multi-stage AI-assisted classification and review workflow**. **Each stage is a separately invoked agent** bound to its own instruction prompt and to the model configured in `src/models.py` … **convened daily** by the chairman" — and, later in the same paragraph, "**The full council meets every day**" *(was `:59`)* |
| `docs/methodology.html` (Part VIII) | Same sentence, generated |
| `scripts/site_templates/how_it_works.html.j2` / `docs/how-it-works.html:63-64` | "**the AI research council** — the research agents, each box naming the model it runs on" |
| `docs/how-it-works.html:7` (meta description) | "the AI research council" |
| `COUNCIL.md` | The seat-by-seat contract; `.claude/agents/*.md` are the definitions; `analytics/daily-research/` are the session records |
| `views/isds-workflow-3d/workflow.json` | **Twelve** model-bearing cards — the **nine** council seats plus `ai-check`, `daily-researcher` and `minutes`, which are stages rather than seats *(corrected 2026-08-05 against `eac8ed9`; this row said "ten" and no file carried that number)* |

**Status re-measured 2026-08-08: the architecture leg is CONVERGED; the cadence leg is still
DIVERGENT.**

*Architecture.* `METHODOLOGY.md:61` no longer claims standing agents. "Each stage is a
separately invoked agent" and README's "roles realized as coordinated stages" are now the
same proposition in different words, and both are true of how the seats actually run. The
opposition the 2026-08-04 reviewer found is gone. **Note the countervailing move, so this is
not read as a one-way retreat:** `2686422` ("fix(chart): restore 'THE AI RESEARCH COUNCIL' —
the seats are real agents") put the council framing *back* on the flowchart, on the ground
that the seats are genuine `Agent` invocations. Nothing in that commit contradicts either
sentence above; "separately invoked" and "real agents" are compatible, and "standing" was the
only word that was not.

*Cadence — unchanged and still wrong in one direction.* `METHODOLOGY.md:61` says the council
is "**convened daily**" and, later in the same paragraph, "The full council meets every day";
`README.md:93` places the same roles inside "**the same weekly run**"; the brief itself is
weekly. `analytics/daily-research/` holds daily records, so "daily" is right for the
*sessions* and wrong for the *brief pipeline*. This distinction has to be made explicitly or
the two files will still disagree after any fix.

**A fix here must also change:** `README.md:91-93` and `:102`, `METHODOLOGY.md:61`, the how-it-works
template, a `docs/` rebuild, and — if the word "council" is retired rather than qualified —
`COUNCIL.md`, the **twelve** model-bearing cards in `views/isds-workflow-3d/workflow.json`,
the **nine** `.claude/agents/*.md` definitions, the **nine** seat notes among the thirteen
`agents/*.md` files (the other four — `Agent Registry`, `Claim Map`, `Project Change Log`,
`Workflow Threads` — are index notes), and this vault's own `hub: Council`. **That last list
is why a wholesale renaming is a far larger change than it looks, and it is the archivist's
to absorb.** *(Counts corrected 2026-08-05 against `eac8ed9`; this paragraph previously said
ten, ten and twelve, and all three were wrong.)*

---

## C8 — Run count and the deduplication narrative

| Stated in | What it currently says |
|---|---|
| `digests/` | **11** archived run folders: 06-09, 06-10, 06-15, 06-16, 06-22, 06-29, 07-06, 07-13, 07-20, 07-27, 08-03 |
| `scripts/build_site.py:823` | `f"Across {len(rows)} archived runs from {first['date']} to {last['date']}, "` — ✔ **"weekly" is gone from the hard-coded string** *(was `:766`)* |
| `docs/digests/index.html:72-73` | ✔ **Both defects repaired:** "Across **11 archived runs** from 2026-06-09 to 2026-08-03, candidates evaluated **ranged from 80 to 10 with no steady trend**, the last seven between 10 and 23; matches stayed at zero and **items surfaced totalled 14**." *(was `:68-69`)* |
| `scripts/site_templates/digest_index.html.j2` | ✔ A grep of the template for "weekly" returns nothing |
| `.github/workflows/weekly.yml` | `cron: '0 13 * * 1'` — Mondays |
| `analytics/retrospective-audit-2026-08-08.md:10-19` | **New, 2026-08-08, uncommitted on `fix/restore-council-label`.** Re-derives the denominators from the files: **14** article files, **13** distinct URLs, **12** distinct underlying matters, 347 screenings as *events*. "**Any figure published with 14 as its denominator needs the 13/12 qualifier.**" |

**Status re-measured 2026-08-08: the two divergences this row was opened on are CLOSED; a
third is open in the replacement sentence.**
(a) **"Weekly"** — repaired in the generator, so the site now says "archived runs".
(b) **"Fell from 78 to 13 as deduplication matured"** — repaired; the readout now reports a
range and expressly says "no steady trend", asserting neither monotonicity nor cause.
(c) **NEW: "items surfaced totalled 14"** is a count of *article files*. The audit run this
morning establishes that those 14 files are **13 distinct URLs** (Telefónica v. Colombia,
`italaw.com/cases/12153`, published 2026-06-09 **and** 2026-06-10) and **12 distinct
underlying matters** (the Okuashvili/Swedish Supreme Court entries of 2026-06-29 are one
dispute through two fora). The site states the event count with no qualifier.

**A fix here must also change:** `scripts/build_site.py:823` and whatever computes the "items
surfaced" figure it interpolates — the sentence is **generated**, so the template strings and
the `build_site.py` f-string are the only editable surfaces; `docs/digests/index.html` must be
rebuilt, never hand-edited.

**Where the qualifier already exists, so no one "fixes" it twice.** `METHODOLOGY.md:49` states
"all fourteen items published to date" **and then qualifies it in the same paragraph**: "Both
figures count events rather than distinct things… one italaw case page was published on two
consecutive days, which makes the fourteen published entries **thirteen distinct
developments**." The professor-facing methodology is already correct on this point. **The
site is the only surface carrying the bare 14.** *(One caution on reading across the two: the
audit's "12 distinct underlying matters" is an **Okuashvili/Swedish-Supreme-Court merge**;
`METHODOLOGY.md:49`'s "twelve of the thirteen" is a **ring count**. Two different twelves.)*

---

## C9 — Target construct: what counts as a positive

| Stated in | What it currently says |
|---|---|
| `scripts/site_templates/index.html.j2:9-13` | "A **low-cost**, weekly monitor … at one **precise doctrinal intersection**: where intellectual property is asserted as a protected investment, a regulatory or judicial measure is the disputed conduct, and **a jurisdiction or admissibility doctrine is live and litigated**" — *two changes since this row was written: the Ring 3 clause moved to Definition A (C13), and the cost word is now "low-cost", matching the `README.md:5` correction of 2026-08-08* |
| `docs/index.html` (hero) | Same, generated |
| `scripts/site_templates/index.html.j2` (three-rings section) | "not a word but a *relationship between three doctrines* … operationalised as the **overlap** of three doctrinal 'rings'" *(no longer at `:31-34`; `:31-36` is now the status strip)* |
| `METHODOLOGY.md:19` | The seed corpus "arranges the same three elements" |
| `METHODOLOGY.md:25` | Ring Two is **weighted** so a claimant alleging a wrongfully rendered court ruling can reach MEDIUM on this ring alone, and never HIGH |
| `METHODOLOGY.md:71` | "the hold out set is likely skewed toward NAFTA and ICSID denial-of-justice awards (**Loewen and Mondev utilize more of the judicial measure ring than the full IP-as-investment intersection**)" *(was `:67`)* |
| `scripts/holdout_set.json` / `scripts/backtest_corpus.json` | The four `label: 1` positives are Loewen, Mondev, Apotex, PM v. Uruguay |
| `src/classify.py:279-296` | One ring at/above `STRONG_SUBTOTAL`, or one ring plus an incidental second, reaches the 40-69 MEDIUM band — i.e. the digest threshold *(was `:219-225`)* |
| `fingerprint.yaml:113-114` | The same rule in prose *(was `:103-104`)* |
| `analytics/instrument-map-2026-08-08.md` §3 | **New, 2026-08-08.** The *reachable* output set of the deterministic scorer in [20,40] is **{28,29,30,31,32,33,40}**, plus 35 via the negative-signal cap — **25 is unreachable**. And two off-theme red-team probes (N1 pharma news with no ISDS, N2 a domestic trade-secret suit) also score **33** |

**Status: OPEN, and 2026-08-08 sharpened it rather than resolving it.** The site claims an
intersection; the label set and the scorer both admit one-ring items. METHODOLOGY already
concedes the holdout skew at `:71` and already discloses the Ring-Two weighting at `:25` — so
this is **not** a hidden defect; it is **the homepage stating a narrower construct than the
methodology, the labels and the code implement.** The homepage is where a reader forms the
claim, and the homepage says "intersection" with no qualifier.

**What this morning's audit adds, and it cuts against the homepage twice over.** First, two
*deliberately off-theme* probes score 33 — above the operative publication floor of 25 — so
the construct the machine implements admits material with no ring at all in the intended
sense. Second, the retrospective audit found that of the 14 published entries, **7 display no
ring**, `ip_as_investment` appears as a displayed ring **zero times**, and **6 entries state
in their own annotation that they are off-theme or unassessable**
(`analytics/retrospective-audit-2026-08-08.md` §§2–3). The published record is now direct
evidence for this row, where before it was an inference from the labels and the code.

**A fix here must also change:** if the project adopts the reviewer's three-tier scheme
(direct / adjacent / background), it lands in **`scripts/holdout_set.json` labels,
`scripts/backtest_corpus.json` ids, `src/classify.py` bands, `fingerprint.yaml:110-118`,
`METHODOLOGY.md:29`+`:47`+`:52`+`:71`, both site templates, and every future digest entry's
status field** — and it invalidates the current precision/recall/accuracy numbers in **C1**,
because the positive class changes. **This is the row most likely to create new divergence:
any relabelling silently falsifies C1 unless C1 is regenerated in the same change set.**
**As of 2026-08-08 there is a cheaper first step on the table and it is not this one:** the
13-item operator labelling protocol at `analytics/retrospective-audit-2026-08-08.md` §6
measures the *published* distribution without touching a label in the holdout, and therefore
without moving C1 at all. It is owned by Emory, not by any seat.

---

## C10 — Publication floor: what reaches the public digest

| Stated in | What it currently says |
|---|---|
| `src/config.py:28` | `RELEVANCE_FLOOR = 25` — **unchanged** |
| `src/config.py:31-39` | **New 2026-08-08.** `FILL_FLOOR_SUSPENDED`, **default ON**. The floor is not raised; the *fill* is switched off, so nothing between 25 and 39 is surfaced at all |
| `src/main.py:92-120` | The fill is now conditional on that flag *(was `:53-69`)* |
| `README.md:79-86` | Still describes the fill as operative, and still quotes the retired one-sentence note. **See C15** *(was `:72-78`)* |
| `digests/2026-08-03_ISDS-Thematic-Watch/README.md:11` | The run's sole entry: score **25**, rings matched "**N/A**" |
| `digests/2026-08-03_ISDS-Thematic-Watch/articles/01_gazprom-affiliate-receives-shares-in-linde-s.md:14` | Its own annotation: "it **does not** engage intellectual property as a covered investment, **challenge a judicial measure** under treaty law, or raise **jurisdictional/admissibility** doctrines … **no ISDS thematic intersection**" |
| same file, **Correction (2026-08-08)** appended at `:21-29` | **New, uncommitted on `fix/restore-council-label`.** "A negative thematic conclusion cannot be established from a headline the instrument could not read past; the honest status of this item is '**not assessed — body not retrieved**,' not a finding either way. This entry was also the entire content of its digest, **surfaced by the fill-toward-six rule at the relevance floor rather than by the match threshold.**" |
| `digests/2026-08-03_ISDS-Thematic-Watch/index.html:145` | The same annotation, published — **the correction is appended to the Markdown entry, and the published HTML will not carry it until `docs/` is rebuilt** |
| `scripts/site_templates/index.html.j2:9-13` | The homepage's "precise doctrinal intersection" |

**Status: the defect is now DISCLOSED in the archive and PREVENTED going forward — and it is
still visible on the live site.** Three distinct things happened on 2026-08-08 and they should
not be collapsed:

1. **Prevented.** With `FILL_FLOOR_SUSPENDED` on by default, an item like the Gazprom entry
   is no longer surfaced. This is the fix the previous version of this row asked for, and it
   was made **without touching `RELEVANCE_FLOOR`** — which matters, because C5 warned that
   raising the floor while "never empty" stood would be a direct contradiction. Suspending the
   fill avoids that trap entirely: nothing promises a non-empty digest any more (C5), so
   nothing has to be padded.
2. **Disclosed.** The entry now carries a dated correction naming both defects — the negative
   conclusion drawn from an unread body, and the fill provenance. Correction by amendment, not
   rewrite; the original annotation is untouched above it.
3. **Not yet undone on the site.** The published HTML still renders the uncorrected
   annotation, and will until this session is committed and `scripts/build_site.py` re-run.

**A fix here must also change:** nothing further in the *code* — the surfacing rule is done.
What remains is prose: `README.md:79-86`, `HANDOFF.md:99-101`, `fingerprint.yaml:2-9`,
`scripts/site_templates/index.html.j2:186`, the `quality-bar` card, and `METHODOLOGY.md:49`.
All six are **C15**, and C10 should not be closed until C15 is.

---

## C11 — Source count

| Stated in | What it currently says |
|---|---|
**Row re-read cell by cell 2026-08-22 at `c4f6825`. It has DIVERGED, and the site is the half
that is wrong.** Every cell below is quoted from the file as it stands today, not carried
forward.

| Stated in | What it currently says |
|---|---|
| `README.md:56` | "the **ten** sources" — **moved to ten** at `44550ca` (2026-08-17) |
| `views/isds-workflow-3d/workflow.json` | **10** source chips; `node tools/isds-workflow-3d/validate.mjs` exits 0 reporting "10 source chips, 30 cards, 44 edges" |
| `docs/assets/workflow.svg` / `scripts/site_templates/assets/workflow.svg` | Banner text renders **"WHERE WE LOOK — THE 10 SOURCES, CHECKED EVERY RUN"**; GDELT chip present |
| `src/sources/` | **Ten** source modules; `src/sources.all_sources()` returns **10** instances — `iisd_itn`, `google_alerts`, `gmail_scholar`, `italaw`, `icsid`, `iareporter_headlines`, `unctad_isds`, `pca_press`, `bing_news`, `gdelt` |
| `scripts/site_templates/how_it_works.html.j2:27` / `docs/how-it-works.html:58` | **STILL "the first band is the nine public sources checked"** — not moved |
| `scripts/site_templates/how_it_works.html.j2:3` / `docs/how-it-works.html:7` | **STILL** meta description "the **nine** public sources" — not moved |
| `METHODOLOGY.md:33` | Enumerates **nine** channels and omits GDELT; also says Bing News is polled through "**eight** fixed, fingerprint-derived queries" where `src/sources/bing_news.py:23` defines **12**. Emory's document — [[Workflow Threads]] **D7** |
| `alerts.yaml:29-42` | **Corrected 2026-08-08.** The `feeds:` list is no longer Google-only; two Talkwalker RSS entries present at this reading |

**Status: DIVERGENT as of 2026-08-22 — and the divergence is visible to Dr. Benavides on a
single screen.** On `docs/how-it-works.html`, line **58** tells the reader "the first band is the
nine public sources checked"; the chart inlined at line **96** of the same page renders the
banner "**THE 10 SOURCES**" with ten chips. The prose and the picture it introduces contradict
each other, roughly forty lines apart, and have done since `44550ca` landed on **2026-08-17** —
five days. `check_site_sync.py` cannot catch it: the template and the built page agree with each
other perfectly, and both are wrong.

**Why this row failed to catch it, recorded against this seat.** `44550ca`'s commit message
states "Every nine-sources surface moves to ten in the same change ... README, rebuilt
view.js/SVG/site." Two surfaces did not move — the two hand-written strings in the Jinja
template — and this map's own snapshot-anchor block accepted that sentence, writing that the
source-count row was "satisfied by that same commit (ten stated once, everywhere)". **It was
not satisfied, and this row was never re-read to check.** A commit message is a claim about a
change, not a reading of the files after it; this map exists precisely to be the reading. The
anchor block is corrected in place above, with its original wording quoted.

**Owner of the fix: [[site-experience]]**, which owns `scripts/site_templates/` and `docs/`.
Both strings are hand-written English in the template, so this is a two-string edit plus a site
rebuild — not a regeneration problem. Escalated, not edited: this seat does not write to
`scripts/site_templates/` or `docs/`.

**What remains unverified, and must not be read as verified:** that the ten *modules* correspond
one-to-one with the ten *sources* the site names, and that all ten are currently returning.
`analytics/instrument-map-2026-08-08.md` §1 records that **10 of the 14 published entries came
from a single one of them** (`iareporter_headlines`) — a concentration the flat count conceals
on every surface that states it, at nine or at ten.

<details><summary>Superseded reading — 2026-08-08, kept as the dated record it was</summary>

| Stated in | What it said then |
|---|---|
| `README.md:56` | "the **nine** sources" *(was `:52`)* |
| `scripts/site_templates/how_it_works.html.j2:27` / `docs/how-it-works.html:58` | "the first band is the **nine public sources** checked" |
| `docs/how-it-works.html:7` | meta description: "the **nine** public sources" |
| `views/isds-workflow-3d/workflow.json` | The source band on the flowchart |
| `src/sources/` | Nine source modules; `analytics/instrument-map-2026-08-08.md` §1 confirms "**Nine sources under `src/sources/`**" from a direct reading of the tree |

Status then: partially verified 2026-08-08 — the count of nine corroborated from a second,
independent direction (a path-tagged reading of `src/sources/`) rather than asserted three times
from one flowchart band.

</details>

---

## C12 — Model assignments

| Stated in | What it currently says |
|---|---|
| `src/models.py` | `CHAIRMAN_MODEL` and `HEAVY_MODEL` = `claude-opus-5`; utility seats `claude-opus-4-8` |
| `.claude/agents/*.md` frontmatter | **All nine seats now declare `model: opus`** — closed at `c25ea64`. The key selects a **tier, not a version** (`scripts/check_models.py:36-38`), so the frontmatter never distinguishes Opus 5 from Opus 4.8; the version lives in `src/models.py` and on the card *(re-measured 2026-08-05 against `eac8ed9`; this row previously recorded two seats with no key)* |
| `views/isds-workflow-3d/workflow.json` | `systems-designer` and `site-experience` cards read "Model: Claude Opus 5" — **now backed by a declared `model:` key and checked** |
| `scripts/check_models.py:24-31`, `.github/workflows/model-consistency.yml:50` | The three rules it enforces: a card naming a model must belong to a seat that declares a `model:` key; the named model must normalise to an id present in `src/models.py`; a seat's vault note must name the same model as its card |
| `agents/*.md` — **nine seat notes**, not twelve | Verified matching `src/models.py` on 2026-08-04; count corrected 2026-08-05 |
| `HANDOFF.md:29`, `:163` | Corrected 2026-08-04 |
| `COUNCIL.md`, `METHODOLOGY.md` Part VIII | Carry the assignment in prose |

**Status: CLOSED — tested this session, which is what this row asked for.** The open
divergence was "two flowchart cards assert a model no file carries", raised 2026-07-31,
re-escalated 2026-08-04 (`analytics/vault-sessions/2026-08-04.md`, both sessions). `c25ea64`
resolved it by Emory's first option: every one of the nine `.claude/agents/*.md` files now
carries a `model:` key, and `scripts/check_models.py` makes card/definition/vault-note drift
fail the build. **This row previously asked whether the guard covers the two formerly
undeclared seats or exempts them; measured 2026-08-05 against `eac8ed9`, it covers them** —
they declare, so rule 1 has something to check rather than nothing.

**Re-run 2026-08-08:** `scripts/check_models.py` exits **0** — "Checked **12** flowchart cards
against `.claude/agents/`, `agents/` and `src/models.py`… every card names a configured model,
backed by a declared `model:` key, and no vault note contradicts its card." No definition file
under `.claude/agents/` and no file under `prompts/` was modified by the 2026-08-08 session
(`git status --short`), so **no seat's model, prompt binding or contract changed today**, and
the roster in [[Agent Registry]] needed no model edit. That is a measurement, not an
assumption.

**Watch for a new divergence, and it is a real one:** because `model:` is a **tier**, the
frontmatter cannot disagree with a card about *version*. The guard's version check therefore
rests entirely on card ↔ `src/models.py` ↔ vault note. **If a seat's vault note stops stating
a model in the `**Model.** \`…\`` form that `_VAULT_MODEL_RE` (`check_models.py:63`) matches,
that leg of the check silently has nothing to compare** — the archivist's formatting is
load-bearing for a CI guard, which is worth knowing before anyone reformats these notes.

---

## C13 — What Ring 3 *is*: a doctrinal dimension, or a disposition — **RULED FOR DEFINITION A 2026-08-06; IMPLEMENTED; row closed 2026-08-08**

> **Closure, recorded 2026-08-08.** The council adopted **Definition A (DIMENSION)** and it
> was implemented across the tree at `ae1f04b` ("fix(ring3): Ring 3 is a dimension, not a
> disposition — one definition, everywhere"), completed at `373cce6`, with the sixteen-page
> site-template surface repaired at `9bd112e` ("fix(site): the band explainer was false in
> three places, on sixteen pages") and the residual four files closed at `3f6e19d`.
> **Re-measured file by file on 2026-08-08: thirteen of the fifteen B statements below no
> longer exist, and the two that remain are true of their own subject matter.** The row is
> corrected in place rather than deleted, because the B table is the only surviving inventory
> of what had to move, and because this note carried the row as live for two days after the
> ruling — the same failure it has now recorded three times (C1, C12, and the registry's
> "three vault notes, one fact").
>
> **The cost prediction held.** This row said that if A were adopted, "no scoring artifact
> moves". None did: `fingerprint.yaml`'s Ring 3 is the same seventeen doctrinal phrases with
> no outcome term, and `src/classify.py` still has no representation of a disposition. The
> whole ruling was a prose change, exactly as priced.

**Added 2026-08-05, before the council ruled, because this is the row that decides whether
the ruling is cheap or expensive.** Two incompatible tests were in the tree at the same time.

- **Definition A — DIMENSION.** Ring 3 is engaged when jurisdiction/admissibility doctrines
  are *live and litigated in the case*, whatever the outcome.
- **Definition B — DISPOSITION.** Ring 3 requires that the tribunal actually *disposed of the
  case* at the threshold, without reaching the merits.

### Stated as B (disposition) — **all fifteen re-read 2026-08-08**

| Stated in | Was (at `eac8ed9`) | State on 2026-08-08 |
|---|---|---|
| `prompts/research_analyst.txt:18-20` | "the tribunal **disposes of the case** … without reaching the merits" | ✔ **Gone.** `:20` now carries "whether or not" |
| `prompts/research_analyst.txt:113` | "**disposed of at the jurisdictional gate**" | ✔ Gone |
| `prompts/council_chairman.txt:8-9` | "**disposal at the jurisdictional/admissibility stage**" | ✔ Gone; `:8` now reads "**live, litigated**" |
| `.claude/agents/council-chairman.md:31-32` | "**disposal at the jurisdictional/admissibility gate**" | ✔ Gone; `:31-32` now "**live, litigated** … whether or not" (this is the contract change `ae1f04b` made, recorded in [[Agent Registry]]) |
| `prompts/council_calibration.md:20-23` | "**disposal at the jurisdictional/admissibility stage**" | ✔ Gone; `:22` now "**live, litigated**". **This is the one that mattered most** — it is injected into every analyst run at `prompts/research_analyst.txt:7` (`{{CALIBRATION}}`), so it binds every seat |
| `prompts/systems_researcher.txt:18-19` | "Ring 3 **jurisdictional/admissibility disposal**" | ✔ Gone; `:19` now "**live, litigated**" |
| `prompts/research_editor.txt:28` | "the **jurisdictional/admissibility gate**" (weak B) | ✔ Gone |
| `prompts/classifier.txt:12-14` | "doctrines **decide the case**" — contradicted `:60-61` in the same file | ✔ Gone; `:12-13` now "**live and litigated** in the case, **whether or not they decide it**". **The intra-file contradiction is resolved** |
| `moc/Research Question.md:3-5` | "**disposed of at the jurisdictional/admissibility gate?**" | ✔ **Gone — the vault's own statement of the question is now A**, at `:5`: "litigating a jurisdictional/admissibility doctrine, **whether or not that doctrine ends the case**" |
| `METHODOLOGY.md:10` (Part I) | "**determines that the case cannot proceed**" | ✔ **Reframed to A in place.** `:10` now reads "a jurisdictional or admissibility doctrine is **live and litigated in the case, whether or not it determines that the case cannot proceed**." The B words survive **inside an A clause** — a grep for the old string still hits, which is why this row records the whole sentence |
| `STATE_OF_THE_ANSWER.md:4` | "**disposed of at the jurisdictional or admissibility stage**" | ✔ Gone; `:4` now "met with a **live, litigated** jurisdictional…" |
| `scripts/site_templates/index.html.j2:13` → `docs/index.html` | "**the case turns on** jurisdiction and admissibility" | ✔ Gone; the hero now reads "a jurisdiction or admissibility doctrine is **live and litigated**" |
| `scripts/site_templates/base.html.j2:162` | "the threshold **on which the seed cases were decided**" — *this row's single largest surface, rendering on sixteen published pages* | ✔ **Repaired at `9bd112e`.** Now at `:160-164`: "the threshold doctrines a case **litigates, whether or not they end it** — dispositive in Philip Morris v. Australia, **contested and resolved at the threshold in Bridgestone v. Panama, which was then decided on the merits**" |
| `working/02c-framework-rings.original.txt:7` | "The case is **decided at the threshold**… each case **died on** jurisdiction" | ✔ Gone; `:7` now carries "whether or not" |
| `working/one-pagers/philip-morris-v-australia.md:18`, `:22`, `:30` | "Ring 3 (jurisdictional disposal)"; "is disposed of at the jurisdictional gate"; "survives the jurisdictional gate" | **RETAINED, and correctly so.** `:18` now reads "Ring 3 (**threshold doctrines litigated**)" and records that four threshold questions were separately adjudicated and exactly one disposed of the case, with a fifth raised and never reached. The surviving "jurisdictional disposal" at `:22` describes **what happened in this case** — a fact about the seed, not a definition of the ring — and `:18` says so expressly: "under the retired test that counted only the doctrine which disposes, **four of these five would not have registered as Ring 3 at all**, and the fifth could never register" |

### Stated as A (dimension)

| Stated in | What it currently says |
|---|---|
| `think-tank/methodology/ring3-reconciliation.md:48`, `:56`, `:59`, `:115`, `:133`, `:139` | The decided council note (2026-06-29, `8909390`): justifying a dimension by a disposition statistic is "a **category mistake**"; the salience test is "recurring and **live** across the seed corpus — **not whether it was the disposition**"; Bridgestone's Ring 3 was "**live, litigated, and partly dispositive**"; "the instrument **keys on doctrinal engagement, not on a jurisdiction/admissibility disposition**"; and a standing rule at `:139` — "**Never justify a fingerprint dimension by a disposition statistic again**" |
| `scripts/site_templates/index.html.j2:74-77` → `docs/index.html:100-105` | "the threshold **dimension** anchored by *Philip Morris*, **dispositive there** and a recurring doctrinal **risk** across the broader seed pattern" |
| `scripts/site_templates/base.html.j2:169` → `docs/index.html:392` | "a **live** jurisdiction-and-admissibility **question**" — **seven lines below the B statement at `:162`, in the same JavaScript object** |
| `prompts/council_roundtable.txt:19-23` | "a jurisdictional/admissibility rule … that **can** dispose of the case BEFORE the merits. Seed awards: Philip Morris (disposed on Ring 3), Eli Lilly (merits), **Bridgestone v. Panama (Ring 3 present, decided on merits)**" — the only prompt carrying the corrected seed scorecard |
| `prompts/classifier.txt:26-28`, `:60-61`, `:149`, `:172-186` | Bridgestone is assigned "**Rings 1 + 2 + 3**" although decided on the merits; few-shot Example 2 fires Ring 3 on a *contested, undecided* standing objection and scores HIGH; the negative few-shots frame Ring-3 absence as "no jurisdictional **objection**", never as "reached the merits" |
| `fingerprint.yaml:81-102`, `:110-115`, `:162-172` | Seventeen doctrinal phrases and **zero outcome terms**; "a ring counts as PRESENT once its keyword subtotal reaches the present floor (12)"; the Bridgestone few-shot scores HIGH on a "jurisdiction **fight**" |
| `src/classify.py:33-37`, `:155-263` | `VALID_RINGS` and `keyword_score`. **`grep -niE "disposit\|outcome\|dismiss\|merits\|holding" src/classify.py src/config.py` returns nothing.** The deterministic scorer has no representation of a disposition |
| `README.md:8-9`, `:31-33` | "where threshold questions of jurisdiction and admissibility **may be in play**"; "**A jurisdictional or admissibility doctrine** — abuse of right, treaty shopping, …" |
| `working/one-pagers/bridgestone-v-panama.md:18`, `:22`, `:24` | "the hardest gatekeeping issue **surviving to the merits**"; "**it cuts against reading jurisdictional dismissals as the primary filter**"; "a jurisdictional dismissal is best read as **only the outermost of several available filters** rather than as the characteristic fate of an IP claim" |
| `working/one-pagers/eli-lilly-v-canada.md:22`, `:26`, `:34` | "The only gate raised was the time bar, and it failed … **No jurisdictional disposal occurred**"; "the **jurisdictional-exit pattern is not universal**" |
| `src/config.py:68-72` (`THEME_ONE_LINER`, rendered in every digest footer); `templates/digest.html.j2:104-106` | "…and **jurisdictional/admissibility doctrines**" — doctrine, no disposal (A-leaning) |

### Mixed — one paragraph carrying both — **resolved**

| Stated in | What it currently says |
|---|---|
| `METHODOLOGY.md:26` → `docs/methodology.html:105` | ✔ **No longer mixed.** The heading is unchanged ("Threshold Questions … as a Potentially Dispositive **Dimension**"), and the defining sentence — the B-shaped one this row was opened on — has been replaced: "This ring observes **the doctrines a case litigates at the jurisdictional and admissibility stage, whether or not they end it**: abuse of right, treaty shopping, foreseeability of the dispute, restructuring for treaty protection, and the disputed definitions of 'the investor' and/or 'the investment.'" Heading and definition now agree, and both are A. The Eli Lilly clause this row flagged as needing a decision **survives**: `:26` still says Ring 3 "did not form part of the reasoning in Eli Lilly — which was decided on the merits", while `working/one-pagers/eli-lilly-v-canada.md:22` records a time-bar objection raised and rejected, which under A **is** a live Ring 3 engagement. *One residual, named below.* |

### A third sense, in live use, that neither definition covers

| Stated in | What it currently says |
|---|---|
| `analytics/insights.jsonl` (17 lines), `STATE_OF_THE_ANSWER.md:122` *(re-pinned 2026-08-16 from `:114-124`, a range that now opens inside the Day 11/12 UNCITRAL entries; the taxonomy heading itself is at `:122`)*, `state/research_log.json:111`, `:171`, `:201`, `:211`, `analytics/optimization-log.md:34`, `analytics/council-log.md:50` | A **"Ring 3 taxonomy"** grown by the research layer, now at **five mechanisms**: abuse-of-right/critical-date, administrative-review prerequisite, fork-in-the-road, MFN-forum-access, first-generation-BIT scope limitation. **Not one of the four new mechanisms appears in `fingerprint.yaml:81-102`.** The research layer's Ring 3 and the classifier's Ring 3 have different contents |

**Status 2026-08-08: CONVERGED on Definition A. Two residuals, neither of them a
definition conflict.**

*What the ruling cost, measured rather than estimated.* This row predicted that adopting A
would move the B table and no scoring artifact. Confirmed: `fingerprint.yaml:81-102` still
carries the same seventeen doctrinal phrases with **zero** outcome terms, and
`src/classify.py` still has no representation of a disposition. The 26 of Ring 3's 100 weight
points sourced from Bridgestone (`shell subsidiary` 6, `definition of investor` 5, `abusive
tactics` 4, `standing of licensor vs licensee` 4, `standing to claim denial of justice when
not a party` 4, `exhaustion of local remedies` 3, all tagged `seed: bridgestone` at
`fingerprint.yaml:94-100`) were the hostage under B; under A they are simply correct, since
Bridgestone litigated those doctrines and was then decided on the merits — which is now what
`base.html.j2:160-164` says on all sixteen published pages.

**Residual 1 — the Eli Lilly clause, still undecided.** `METHODOLOGY.md:26` says Ring 3 "did
not form part of the reasoning in Eli Lilly"; `working/one-pagers/eli-lilly-v-canada.md:22`
records a time-bar objection raised and rejected, and under A a raised-and-rejected threshold
objection **is** a live Ring 3 engagement. This is the one place where the A ruling has not
been carried through to its consequence. Owner: whoever next edits Part II of
`METHODOLOGY.md`; it is a one-clause change and it should not be made silently, because
`ring3-reconciliation.md` relies on the Eli Lilly characterisation.

**Residual 2 — the third sense, unchanged.** See the table immediately below. The research
layer's five-mechanism Ring 3 taxonomy and the classifier's seventeen-phrase Ring 3 still have
different contents, and adopting A did not touch that: A settled *what makes a ring engage*,
not *which doctrines count as being in the ring*. Verified 2026-08-08 —
`fingerprint.yaml:81-102` contains no phrase for administrative-review prerequisite,
fork-in-the-road, MFN forum access, or first-generation-BIT scope limitation.

**A fix here must also change** — for either residual — `docs/` by rebuild, never by hand.

---

## C14 — The holdout's composition, and the Apotex item's identity — **REPAIRED 2026-08-06 by option 1 (caption-only); disclosure updated 2026-08-08**

> **Outcome, recorded 2026-08-08.** The fork below was resolved in favour of **option 1, the
> caption-only repair**, at `373cce6`. It was metrics-neutral and guard-neutral exactly as
> priced: `scripts/check_claims.py` re-run on 2026-08-08 reports "Checked 13 self-descriptive
> facts against 29 declared restatements — every restatement equals its authority", exit 0,
> and the full suite was green that day at 414 passed / 5 xfailed *(the 2026-08-08 reading;
> the suite stands at **564 passed / 5 xfailed** as of 2026-08-09)*. **`METHODOLOGY.md:52` was not
> rewritten**, which is why the nine declared mirrors that point into it still match; the
> disclosure was instead updated by *appending* the dated correction at `METHODOLOGY.md:54`,
> whose third clause records that the data file has since been repaired and that the sentence
> above it "records a historical state of the file, kept per the correction-by-amendment rule
> rather than rewritten." That is the pattern to reuse: **the fail-closed mirror check made
> amendment the cheap path and rewriting the expensive one.**

| Stated in | What it currently says |
|---|---|
| `scripts/holdout_set.json` (`apotex_v_us`) | ✔ **Repaired at `373cce6`.** `"label": 1, "prov": "partial"`; the text now opens **"Apotex Inc. v. United States of America, ICSID Case No. UNCT/10/2, Award on Jurisdiction and Admissibility, 14 June 2013"** — the 2013 caption, docket and date matching the 2013 holding the text recites |
| `scripts/backtest_corpus.json:57` (`display_names`) | ✔ **Repaired in the same commit** — "**Apotex Inc. v. United States of America (UNCT/10/2, 2013)**". This was the second, independent copy the row warned about; fixing `holdout_set.json` alone would have left the site saying "Holdings" |
| `scripts/backtest_corpus.json` | `apotex_v_us` in `holdout_positive_ids`; the miss reason recorded in the same file |
| `METHODOLOGY.md:52` → `docs/methodology.html:118` | **Unchanged, deliberately.** One physical line carrying **all of**: "holdout of **twenty** items", "**Four** of the twenty were on-theme positives", the four names, "compared against **sixteen** other awards", "the item captioned Apotex v. United States **recites the jurisdictional holding of the 2013 Apotex Inc. award rather than that of the 2014 Apotex Holdings award its caption names**", "the Apotex item as **partial**", "precision of **1.00**" (×2), "recall of **0.75**", "accuracy of **0.95**", "F1 of **0.86**" (×2). It now describes a **past** state of the data file, and `:54` says so |
| `METHODOLOGY.md:71` | "— **twenty items, only four positives** —" *(was `:67`)* |
| `scripts/check_claims.py:195-238` | Facts 6–12 (`holdout items`, `holdout on-theme positives`, `holdout off-theme negatives`, `precision`, `recall`, `accuracy`, `F1`). Authorities are **live harness runs** of `scripts/eval_holdout.py` and `scripts/backtest.py`; mirrors are regex substrings on `METHODOLOGY.md:52` and `:67`. **Nine of the registry's twenty-nine mirrors point into `METHODOLOGY.md:52` alone** |
| `tests/test_check_claims.py:53-55` | `assert a["n"] == b["n"] == 20`; `a["n_pos"] == b["n_pos"] == 4`; `a["n_neg"] == b["n_neg"] == 16` — asserted independently of the registry |
| `agents/systems-researcher.md:28` / `.claude/agents/systems-researcher.md` / `prompts/systems_researcher.txt` | The seat's standing weak-point list names "the deterministic scorer's **'not-a-covered-investment' miss (Apotex)**" |
| `scripts/backtest_corpus.json:52` (`miss_reasons`) | "Apotex turns on a **negative jurisdictional finding** — the tribunal held the claimant was not an investor and the FDA filings were not a covered investment…" |
| `docs/backtest.html:267`, `:270`, `:272`, `:275`, `:459` | The published table row: score **8**, band **LOW**, "**false negative**", and the miss-reason paragraph — all generated from `backtest_corpus.json`. **The published caption still reads "Apotex Holdings" until `docs/` is rebuilt**; the source is correct and the generated page lags |
| `METHODOLOGY.md:54` | **New 2026-08-08.** "the Apotex caption defect described above **has since been repaired in the data file itself**: `scripts/holdout_set.json` now captions the item as the 2013 Apotex Inc. Award on Jurisdiction and Admissibility and recites that award's holding" |
| `lit-review/kim-memo.md:72-80` | **The only citation of the case anywhere in the repo**: "Apotex Holdings Inc. & Apotex Inc. v. United States, **ICSID Case No. ARB(AF)/12/1, Award (Aug. 25, 2014)**", annotated as the FDA **import-alert** dispute — i.e. the 2014 case, correctly cited, and **a different dispute from the ANDA holding in `holdout_set.json`** |
| `METHODOLOGY.md:21` → `docs/methodology.html:102` | "The **Apotex v. United States** case defines the outer limit of what would be considered an 'investment'" — caption used without a year, so it is true of the 2013 award and reads as though it were the cited 2014 one |
| `think-tank/methodology/ring3-reconciliation.md:94` | Was "the holdout's lone false negative, **Apotex Holdings v. United States**, is precisely a case **decided on a Ring-3 disposition**" — **false as written**. **Corrected 2026-08-08** (uncommitted, `fix/restore-council-label`); one of three dated corrections this session added to that file |
| `think-tank/methodology/ring3-reconciliation.md:101-108`, `:117`, `:141` | The pasted harness run (20 items, TP=3 FP=0 TN=16 FN=1, 1.00/0.75/0.95/0.86) and the argument built on it |
| `analytics/fingerprint-gap-report.md:23`, `:104`, `:112`, `:212-215`, `:243` | "the one on-theme item the live holdout misses — `apotex_v_us`"; the E4 "negative-space / *Apotex* / *Hela Schwarz* miss"; the before/after metrics table |
| `analytics/fingerprint_probes.json:30` (`E4_einarsson_negative_space`) | "The **Apotex / Hela Schwarz negative-space shape**: a decided REJECTION of trade-secret/clinical-data-as-investment against an administrative measure" |
| `tests/test_fingerprint_probes.py:38-40` | `E4_einarsson_negative_space` is in `KNOWN_FALSE_NEGATIVES`, xfailed "pending operator-approved reweight" |
| `tests/test_one_pagers.py:74-77` | Asserts **neither** `seeds/Apotex_v_USA.pdf` **nor** `working/one-pagers/apotex-v-usa.md` exists |
| `working/FINGERPRINT_DRIFT.md:41` | "'not-a-covered-investment' *rejections* (the **Apotex outer limit**; now also the *Hela Schwarz* shape)" |
| `STATE_OF_THE_ANSWER.md:8` | "Apotex outer limit" in the Kim-memo summary |

**Status: the caption defect is DISCLOSED, not hidden** (`METHODOLOGY.md:52`), which changes
what a repair is for. **Measured this session against `eac8ed9`:** the item scores **8**,
matching `ip_as_investment` and `jurisdictional_admissibility` as sub-floor brushes only
(both below `PRESENT_FLOOR = 12`), so it is the false negative and it registers **no ring at
all**. Re-scoring the item with the caption changed to *Apotex Inc. v. United States*, with
and without the 2013 docket and date, returns **8 in every variant** — the caption words
carry no fingerprint weight.

**Consequence for the repair, stated as a fork — option 1 was taken:**

1. ✔ **TAKEN. Caption-only repair** (fix the caption to the 2013 *Apotex Inc.* award, whose
   holding the text already recites): **metrics-neutral and guard-neutral.** Score stays 8,
   the item stays the false negative, precision/recall/accuracy/F1 stay 1.00/0.75/0.95/0.86,
   Facts 6–12 stay green, `tests/test_check_claims.py:53-55` stays green — **all four
   confirmed by re-run on 2026-08-08.** The candor clause on `METHODOLOGY.md:52` was **not**
   rewritten; a dated correction was appended at `:54` instead, which is what let the nine
   declared mirrors survive untouched.
2. **Substitution repair** (replace the text with the real 2014 *Apotex Holdings* award):
   changes the scored text, therefore possibly `recall`/`accuracy`/`f1`, therefore Facts 10–12,
   therefore the four figures on `METHODOLOGY.md:52`, therefore `docs/` — and it would
   **destroy the empirical prop under C13's Definition A**, because
   `ring3-reconciliation.md` §3.3 relies on this item being the *jurisdiction-disposed* case
   that the scorer misses. *Apotex Holdings* (ARB(AF)/12/1, 2014) was not disposed that way.

**Still to do, and it is the only thing left in this row:** a `docs/` rebuild. The published
`docs/backtest.html` table still renders "Apotex Holdings v. United States" from a
`backtest_corpus.json` that has said "Apotex Inc." since 2026-08-06. **The wrong caption is
live on the site right now**, two days after the source was fixed, and it will stay there
until the next `scripts/build_site.py` run — which is gated on this session being committed.
Owner: [[site-experience]], on the same rebuild that clears every other `docs/` lag in this
map. `agents/systems-researcher.md:28` and its two twins were **not** re-characterised (the
miss is still the "not-a-covered-investment" miss) and needed no edit.

**A fix here must also change:** `METHODOLOGY.md:52` **and** `:71` if any count moves, a
`docs/` rebuild (`docs/methodology.html:118`), `agents/systems-researcher.md:28` and its two
twins if the miss is re-characterised, **and `think-tank/methodology/ring3-reconciliation.md`
§3.3 if the item ceases to be the jurisdiction-disposed miss.** **Watch for a new divergence:**
`scripts/check_claims.py` is **fail-closed on a pattern that matches nothing**
(`check_claims.py:356-361` for authorities, `:371-378` for mirrors) — a rewritten
`METHODOLOGY.md:52` that drops any of the nine declared substrings **fails the build with
"the claim was rewritten or removed"** rather than passing quietly. The em-dash in
`[—-] ([a-z]+) items, only` (`check_claims.py:200`) is part of the pattern; replacing that
dash with a comma breaks the match. **C1 is now consistent and mechanically held**, so this
repair is the thing most likely to break it: any change to the item's *scored text* moves
`recall`/`accuracy`/`f1` and puts `METHODOLOGY.md:52` out of agreement with the harness.
**And `tests/test_one_pagers.py:74-77` forbids two artifacts the repair might reach for** —
it asserts that neither `seeds/Apotex_v_USA.pdf` nor `working/one-pagers/apotex-v-usa.md`
exists.

---

## C15 — The fill-toward-six rule, and what a zero-match cycle publishes — **NEW 2026-08-08; PARTIALLY REPAIRED 2026-08-09 — five of eight closed, THREE STILL OPEN**

**Added the day the divergence was created, which is what maintenance rule 4 asks for.** On
2026-08-08 the fill-toward-six rule was suspended by default in code. Seven other files still
state it as operative, and a second claim rides along with it: the *wording* a zero-match
cycle sends. Everything in this row except the `docs/` line is **uncommitted, on branch
`fix/restore-council-label`**.

> **Re-read row by row, 2026-08-09, and the row does not close.** This pass was briefed that
> C15 was resolved. Five of the eight ⚠ rows are genuinely repaired and are marked ✔ below.
> **Three are not**, and are marked ⚠ **STILL OPEN**: `fingerprint.yaml:5-6`, the `quality-bar`
> card, and the `src/main.py` comment — which **moved from `:497-500` to `:687-690`**, so the
> row's own line number no longer finds it and the durable-text rule at the head of this note
> is what located it. Two of the three are the two the 08-08 row already flagged as sitting
> outside any one seat's surface, which is the predicted failure: **the rows that need another
> owner are the rows that survive a repair pass.** Note also that repairing five of them
> against the *first* gate left all five stale against the *second* — see **C16**.

| Stated in | What it currently says |
|---|---|
| `src/config.py:31-39` | **THE AUTHORITY.** `FILL_FLOOR_SUSPENDED = os.getenv("FILL_FLOOR_SUSPENDED", "1")…` — **default ON**, i.e. the fill is off unless the operator sets `0`. The comment gives the reason: filling a thin week means "publishing, to a professor, items the instrument itself declined to call matches — and doing it precisely when the instrument found least" |
| `src/main.py:92-120` (`select_surfaced`) | The behaviour: every item at or above `threshold` is included; the fill runs only `if not fill_floor_suspended`; "No item below `floor` is ever surfaced under either setting" |
| `src/render.py:59-79` (`status_only_body`) | **THE AUTHORITY for the wording**, described in its own docstring as "THE single authoritative copy". It replaced "No thematically relevant developments this week", "which asserted something we are not in a position to assert: that nothing relevant happened" |
| `templates/digest.html.j2:146-159` | Renders `{{ status_only_body|safe }}` for the no-items case; the comment records that the tests assert the string verbatim |
| `src/main.py:510-518` | The subject line: "ISDS Thematic Watch — *date* (**status-only cycle: N screened, none at/above 40**)". Its comment: "The subject must not assert what the body is careful not to" |
| `METHODOLOGY.md:67` (§IX addition) | "the fill-toward-six rule described in Part VI.A **is suspended by default** (FILL_FLOOR_SUSPENDED), so an item below the match threshold of forty is not surfaced at all while the classifier is under validation" |
| ✔ `METHODOLOGY.md:49` (Part VI.A) | **REPAIRED 2026-08-09 by inline amendment**, not by rewriting: the fill sentence stands as the design record and is followed in the same paragraph by "(Suspended, 2026-08-08: while the classifier is under validation the fill toward six is off by default — FILL_FLOOR_SUSPENDED — and only items at or above forty are surfaced…)". The contradiction with `:67` is gone. **But the added clause is itself now false against C16** — items at or above forty are *not* surfaced |
| ✔ `README.md:79-86` | **REPAIRED 2026-08-09.** `:80-86` now reads "…though as of 2026-08-08 that fill is suspended by default while the classifier is under validation (`FILL_FLOOR_SUSPENDED`): below-threshold items are not published and a cycle with nothing at or above 40 sends a status note instead". The retired body text is gone. **Stale against C16** for the same reason |
| ✔ `HANDOFF.md:99-101` | **REPAIRED 2026-08-09** — `:100` now carries "(fill suspended by default since 2026-08-08 — FILL_FLOOR_SUSPENDED)" inline |
| ⚠ **STILL OPEN** `fingerprint.yaml:4-6` | Re-read 2026-08-09, **unchanged**: "Items BELOW this gate but at or above RELEVANCE_FLOOR **may be surfaced as watch-list LEADS** … and **only until the digest reaches MIN_DIGEST_ITEMS**". Names neither flag |
| ✔ `scripts/site_templates/index.html.j2` → `docs/index.html` | **REPAIRED 2026-08-09.** The flow step 5 copy now reads "While the classifier is under validation the near-miss fill is suspended: items below the threshold are not published at all, and a cycle with none at or above it sends a status note reporting the screening count — a note about the instrument's output, not a finding that nothing happened." **Stale against C16**: "Those that meet the threshold make the digest" still opens the step. `docs/` follows by rebuild |
| ⚠ **STILL OPEN** `views/isds-workflow-3d/workflow.json:177`, `quality-bar` card | Re-read 2026-08-09, **unchanged**: `desc` "**Near-misses (25+) may fill a quiet week**, always labeled as leads." A manifest edit, [[systems-designer]]'s on Emory's go-ahead — and the same card still carries the `src/config.py`-vs-`fingerprint.yaml` threshold-location defect open since 2026-08-03, which is why it must be one edit |
| ⚠ **STILL OPEN** `src/main.py:687-690` (comment) | Re-read 2026-08-09, **unchanged in substance and moved in position** (was `:497-500`): still names a "**never-empty** / watch-list-floor rule" and still quotes the retired "no thematically relevant developments, N screened" note text that `src/render.py:59` replaced. The surrounding code at `:700-706` is correct — it is the comment that lies |
| `templates/digest.html.j2:105-107` | "No item reached a full match this period; those below are watch-list near-misses" — fires only on `{% if matches == 0 and items %}`. With the fill suspended, `items` is empty on a status-only cycle, so this clause is now **unreachable rather than false**. Leave it; it is still correct for a cycle that has matches-plus-leads if the fill is ever restored |
| `tests/test_pipeline.py:951` | `assert expected in html, "the status-only body is not emitted verbatim"` — the wording is mechanically held on the code side |

**Status as of 2026-08-09: PARTIALLY REPAIRED — five closed, three open.** The original
reading stands for the three that remain: the numbers did not move — `RELEVANCE_FLOOR` is
still 25 and `MIN_DIGEST_ITEMS` is still 6 — so every consistency check that compares
*numbers* passes, and every sentence that describes *behaviour* is wrong.
`scripts/check_claims.py` carries no fact for the fill, so nothing fails the build. **That is
still true on 2026-08-09**, which is why five files being repaired by hand is not the same as
the class being closed.

**The sharpest instance was inside one file, and it is fixed — by amendment rather than by
rewriting.** `METHODOLOGY.md:49` said the digest is filled toward six while `:67` said the rule
was suspended, eighteen lines apart in the document that goes to Dr. Benavides. The repair
appended the suspension to `:49` in its own parenthesis and kept the original sentence "as the
design record of the rule", which is the same correction-by-amendment pattern C14 recorded as
the cheap path. **The pattern held twice; it is now the house style for this file.**

**A fix here must still change** the three ⚠ **STILL OPEN** rows in one change set. All three
sit outside any one seat's surface — `fingerprint.yaml` and `src/main.py:687-690` are
[[systems-designer]]'s, and the `quality-bar` card is a manifest edit by that seat **on Emory's
go-ahead** — so this needs the coordinated pass it needed on 08-08, now smaller. **Do not
describe the fill suspension as fully documented until those three are done**, and do not
describe C15 as closed on the strength of the five that are.

**Watch for a new divergence, in the opposite direction:** `FILL_FLOOR_SUSPENDED` is an
environment variable with a default, not a constant. If the fill is ever restored by setting
`FILL_FLOOR_SUSPENDED=0` in a workflow file, every sentence above becomes true again and the
`METHODOLOGY.md:67` addition becomes the false one. **Whichever way the flag is set, one of
these two sets of statements is wrong**, and the only durable fix is prose that names the flag
rather than describing one of its settings as the behaviour.

---

## C16 — What a cycle publishes while `VALIDATION_STATUS_ONLY` is on — **NEW 2026-08-09, DIVERGENT**

**Added the day the divergence was created, per maintenance rule 4 — and the day *five other
files were repaired into it*.** On 2026-08-09 a second, stronger publication gate went in.
`VALIDATION_STATUS_ONLY` (`src/config.py:73-74`, **default ON**) holds **all** item-level
publication *and* the research brief. Every prose statement in the tree — including the five
repaired the same day for **C15** — says that items at or above 40 are surfaced. **They are
not.** Everything in this row is **uncommitted, on branch `fix/restore-council-label`**.

| Stated in | What it currently says |
|---|---|
| `src/config.py:42-74` | **THE AUTHORITY.** "while VALIDATION_STATUS_ONLY is on, **NO item-level entry is published or emailed at all** — not the near-misses the fill used to carry, **and not items at or above the threshold either**. The cycle reports itself and nothing else." Default ON; `=0` to publish again |
| `src/config.py:59-62` | **Why it is a second flag and not a stronger setting of the first:** "the fill flag exists to be turned off when the fill is reinstated, and turning it off must not, as a side effect, reopen item-level publication. **The two are read independently and neither can disable the other**" |
| `src/main.py:615-618` | The behaviour: `held` is the counterfactual publication set minus the actual one; `stats["held_for_review"]` records its size |
| `src/main.py:700-706` | The subject line when the gate held something: "**N held for operator review**" instead of "none at/above 40", because the latter "would be false, and false in the direction that hides a real match" |
| `src/main.py:727-737` | The Research Brief is skipped under the gate — `brief_status = "skipped (VALIDATION_STATUS_ONLY)"` — because it "would either say nothing or reach past the gate to the held items" |
| `src/render.py` (`status_only_body`) | The status note reports the held count, so a genuine candidate is recorded rather than silently absorbed |
| `METHODOLOGY.md:69` (§IX addition, 2026-08-09) | States the gate correctly and in terms: it "holds every item-level publication — **including items at or above forty** — and the research brief" |
| ⚠ `METHODOLOGY.md:49` (Part VI.A, as amended 2026-08-09) | **Contradicts `:69`, twenty lines above it.** The suspension parenthesis added *today* says "**only items at or above forty are surfaced**". True of `FILL_FLOOR_SUSPENDED` alone; false of the system. **The C6 failure shape, reproduced by the repair that removed it** |
| ⚠ `README.md:80-86` | "below-threshold items are not published and **a cycle with nothing at or above 40 sends a status note instead**" — the natural reading is that a cycle *with* something at or above 40 sends items. It does not |
| ⚠ `scripts/site_templates/index.html.j2` step 5 → `docs/index.html` | "**Those that meet the threshold make the digest.**" — **the public homepage**, and now false in the direction that overstates what reaches the professor |
| ✔ `HANDOFF.md:99-101` ("Tuning the theme / threshold") | Described "every match at/above threshold with no cap" and named only `FILL_FLOOR_SUSPENDED`. **Corrected in this change set** — this file is [[obsidian-archivist]]'s — to name both flags and say which is on |
| ⚠ `fingerprint.yaml:1-3` | "An item at or above it is **reported as a MATCH**, with no upper cap on how many" — already open under **C15** for a different sentence; the same edit should carry both |

**Status: DIVERGENT — one behaviour, five stale statements, and two of them are the pages a
professor reads.** The direction of the error matters and is the reverse of C15's: C15's stale
sentences **overstated what is published at the bottom** of the range; C16's overstate what is
published **at the top**. A reader of the homepage today would expect a match to arrive; the
instrument would hold it and email a count.

**The finding this row exists to carry.** C15 was repaired on 2026-08-09 by editing five files
to describe `FILL_FLOOR_SUSPENDED`. On the same day, in the same session, a second flag was
added that falsifies four of those five edits. **Both changes were correct; the pair was not
coordinated** — which is exactly the failure mode maintenance rule 3 (same-change-set) exists
to prevent, occurring inside a single session rather than across days. The lesson is narrower
than "coordinate better": **when a change adds a gate upstream of an existing gate, every
sentence describing the downstream gate becomes a claim about the pair**, and the row for the
old gate is the place that has to notice.

**A fix here must also change** all five ⚠ rows in one change set, **together with C15's three
remaining rows** — the two lists overlap at `fingerprint.yaml`, and `METHODOLOGY.md:49` is a
single sentence that must satisfy both. `METHODOLOGY.md` and `README.md` are Emory's;
`scripts/site_templates/` plus the `docs/` rebuild are [[site-experience]]'s; `HANDOFF.md` is
[[obsidian-archivist]]'s and is **corrected in this change set**; `fingerprint.yaml` is
[[systems-designer]]'s. Tracked as [[Workflow Threads]] **B5**.

**Watch for the same trap the C15 row named,** now doubled: both flags are environment
variables with defaults, not constants. Prose that describes *a setting* rather than *naming
the flag and its default* will be wrong again the moment either is flipped. The durable
wording names both flags and says which is on.

---

## Rows this map deliberately does not carry

Stated so the map's silence is never read as a clean bill.

- **Legal-holding precision** (e.g. whether *Bridgestone* is restated as a categorical
  proposition that trademarks are covered investments). That is a per-proposition question
  governed by the Carrying-Span Rule (`prompts/carrying_span_rule.md`,
  `analytics/council-sessions/2026-08-03-proposition-rule.md` R3), enforced entry-by-entry,
  not a same-fact-in-two-files question. It belongs to the analyst and integrity seats.
- **Citation-system consistency** (Bluebook vs Chicago vs raw links). One convention stated
  in many places is a style question, not a claim divergence.
- **Headline-only / paywalled item labelling.** `agents/Workflow Threads.md:154` records that
  `NOT-READ (reason)` is absent from `_EXEMPT_STATUSES` and that the site can never render
  that status — an open defect with an owner, tracked there, not duplicated here.

---

## Maintenance contract

1. **Anchor first.** Re-run `git log <anchor>..HEAD -- <the paths in the anchor>` before
   trusting any row.
2. **Row-before-edit.** Any seat editing a file named in a **Stated in** column reads that
   row first.
3. **Same-change-set rule.** The claim and every twin change together, or the change is not
   made.
4. **New claims get rows.** A new factual self-description stated in more than one file
   gets a row when it is written, not when it drifts.
5. **`docs/` is never the fix.** Change the source, rebuild, let
   `scripts/check_site_sync.py` prove it.
6. **An uncommitted session is still a change set — added 2026-08-08.** The rule in §2 says a
   claim is not changed until every file listed against it is changed *in the same change
   set*. A working tree is a change set. **C15** exists because a behaviour change was made,
   tested and documented in one place while eight statements of the old behaviour stayed in
   the tree, and none of it was committed yet — so no commit-scoped review would have caught
   it either. When a row cites uncommitted work, it names the **branch**, as the anchor block
   at the top of this note does.
7. **A closed row is corrected, never deleted — added 2026-08-08.** C1, C2, C4, C5, C6, C8,
   C12, C13 and C14 all now record a closure. Each keeps its original table so the shape of
   the defect stays legible, because the recurring failure in this vault is not a wrong fact,
   it is a **stale row that licenses a partial fix** — and three of those nine rows were
   carried as open for a day or more after they closed.
