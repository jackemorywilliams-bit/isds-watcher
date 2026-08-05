---
aliases: [Claim Map]
tags: [agent, council, claims]
hub: Evidence Ledger
---
# Claim Map

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

**Snapshot anchor.** Rows C1–C12 were audited against `c9050e6` (`main`, 2026-08-04, clean
tree). **Rows C13 and C14 were added 2026-08-05 and are audited against `eac8ed9`** (`main`,
clean tree), together with the corrections to C7 and C12 noted in their rows. Paths claimed
to be described: `README.md`, `METHODOLOGY.md`, `HUMAN_REVIEW.md`, `HANDOFF.md`,
`COUNCIL.md`, `fingerprint.yaml`, `prompts/`, `.claude/agents/`, `moc/`, `working/`,
`think-tank/`, `docs/`, `scripts/site_templates/`, `scripts/`, `src/`, `templates/`,
`tests/`, `digests/`. Staleness is a one-command question:
`git log eac8ed9..HEAD -- <those paths>`.

**Line numbers are as of `c9050e6`** and will drift as files are edited. Where a line moves,
the quoted text is the durable identifier — search for it rather than trusting the number.

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
| `METHODOLOGY.md:67` | "The small exploratory hold-out set in Part VI.B — **twenty items, only four positives**" |
| `docs/methodology.html:118` / `:126` | The same two sentences, generated. *(`:112` at `c9050e6`; the line moved — quoted text is the durable identifier.)* |
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

---

## C2 — Ring-presence floor and strong subtotal

| Stated in | What it currently says |
|---|---|
| `src/classify.py:47` | `PRESENT_FLOOR = 12` |
| `src/classify.py:50` | `STRONG_SUBTOTAL = 18` |
| `src/classify.py:200-225` | The bands actually computed from those two constants |
| `fingerprint.yaml:100` | "two or more rings with at least one strong (ring keyword-weight subtotal **>= 30**) keyword hit each -> HIGH (>=70)" |
| `fingerprint.yaml:103` | "one ring strong (subtotal **>= 30**) + a weak hit (subtotal < 30) in a second ring -> MEDIUM (40-69)" |
| `fingerprint.yaml:104` | "single non-extra-weight ring, weak hit (subtotal < 30) -> LOW (<40)" |
| `METHODOLOGY.md:47` | States the **floor of twelve** (agrees with `PRESENT_FLOOR`) and the **threshold of forty**. **Never states a strong subtotal at all.** |
| `docs/methodology.html:115` | Same sentence, generated. |

**Status: DIVERGENT between `fingerprint.yaml` and `src/classify.py` — 30 vs 18.** The
public methodology is silent rather than wrong, so a reader who checks `fingerprint.yaml`
against the code (as the reviewer did) finds the conflict; a reader who reads only
`METHODOLOGY.md` finds no statement to conflict with. **The silence is itself a gap:**
`METHODOLOGY.md` documents one of the two constants that decide banding.

**A fix here must also change:** all three `fingerprint.yaml` lines together — they are one
rule stated three times — plus `METHODOLOGY.md:47` if the chosen value is to be documented,
plus a rebuild of `docs/methodology.html`. **Watch for a new divergence:** `fingerprint.yaml`
also carries `threshold: 40` at `:5` and the scoring bands at `:6-9`; changing the subtotal
without re-deriving the bands would put `fingerprint.yaml` at odds with itself.

---

## C3 — Digest threshold and relevance floor

| Stated in | What it currently says |
|---|---|
| `fingerprint.yaml:5` | `threshold: 40` (with a comment at `:1-4` recording the move from 60) |
| `src/config.py:77-86` | `_threshold_from_fingerprint()` reads it from `fingerprint.yaml`, falling back to **60** |
| `src/config.py:27-28` | `MIN_DIGEST_ITEMS = 6`, `RELEVANCE_FLOOR = 25` |
| `README.md:72-75` | "fills up to a minimum of six items with the closest near-misses, but only those at or above a relevance floor of 25 (`MIN_DIGEST_ITEMS=6`, `RELEVANCE_FLOOR=25` in `src/config.py`)" |
| `HANDOFF.md:101` | "only down to `RELEVANCE_FLOOR=25`, so a quiet week may carry only 0–3 items" |
| `METHODOLOGY.md:47` | "The digest threshold of forty … sits twenty below the original figure." |
| `views/isds-workflow-3d/workflow.json`, `quality-bar` card | Cites **`src/config.py: threshold 40 / floor 25`** — the threshold does not live there |

**Status: CONSISTENT on the numbers; ONE wrong file citation, already on record.** The
`quality-bar` card's citation is open drift, raised 2026-08-03, re-verified 2026-08-04
(`agents/Project Change Log.md`, Open drift; `agents/obsidian-archivist.md` slice item 4).
It is a systems-designer fix on Emory's go-ahead, regenerated from the manifest, never
hand-edited.

---

## C4 — Matching method

| Stated in | What it currently says |
|---|---|
| `src/classify.py` | Literal case-insensitive substring containment over normalised text; no stemmer, no lemmatiser, no token boundaries |
| `METHODOLOGY.md:29` | "searched for within each field of an item … as a **case insensitive substring rather than as a whole word**. Therefore, the trigger will fire regardless of what words are immediately before and after … the fingerprint identifies variations of terms which exhibit heavy truncation via **stem forms such as expropriat-**; however, the fingerprint **does not identify variations through lemmatization or via regular expression pattern matching**." |
| `METHODOLOGY.md:67` | "The lexical matcher uses **case-insensitive substrings and a limited set of truncated stems** instead of every possible lemma in a dictionary" |
| `docs/methodology.html:106` / `:126` | Same, generated. |
| `fingerprint.yaml` | The phrase entries themselves — where a "stem" is a truncated literal, e.g. the trailing-hyphen forms |

**Status: NOT DIVERGENT — a wording hazard, and it should be recorded as that and not more.**
`METHODOLOGY.md` describes substring matching accurately and *expressly disclaims*
lemmatisation and regex. The reviewer read the word "stem" as implying an algorithmic
stemmer. The defect is that "stem form" is a term of art the file uses in a non-standard
sense (a truncated literal), one clause away from a correct disclaimer.

**A fix here must also change:** both `METHODOLOGY.md` sentences (`:29` and `:67`) in the
same edit — they are the same claim twice — then rebuild `docs/`. **Watch for a new
divergence:** do not "correct" this to say the matcher does no truncation. It does; the
truncated literals are real fingerprint entries. The accurate substitute for "stem forms" is
*truncated literal prefixes*, and it must be changed in both places or the two sentences will
disagree with each other.

---

## C5 — Empty-report behaviour

| Stated in | What it currently says |
|---|---|
| `src/main.py:53-69` (`select_surfaced`) | "No item scoring below `floor` is ever surfaced, so a genuinely quiet week yields" a short list. **This is the behaviour.** |
| `src/main.py:272` (comment) | "an empty digest contradicts the **never-empty** / watch-list-floor rule" |
| `src/main.py:276-286` | Zero candidates → nothing sent; candidates but none above floor → "no thematically relevant developments, N screened" |
| `scripts/site_templates/index.html.j2:165` | "the strongest are always included so the report is **never empty**" |
| `docs/index.html:197` | Same sentence, generated — **this is the homepage** |
| `fingerprint.yaml:2-3` | "The pipeline additionally **guarantees a non-empty digest** by surfacing the top most-relevant items even when few clear this gate (see src/config.py)." |
| `README.md:76-78` | "Honesty is preferred over **padding**: a genuinely quiet week may carry only **0–3 items**, and a week with nothing above 25 sends a one-sentence note … rather than weak filler." |
| `HANDOFF.md:89` | "A green run **always sends an email**, even a quiet week" |
| `digests/2026-07-27_ISDS-Thematic-Watch/meta.json` | `screened: 10, matches: 0, watch_list_leads: 0, accepted: 0` |
| `digests/2026-07-27_ISDS-Thematic-Watch/README.md:3`, `:11` | "Screened: 10 · Matches (≥40): 0 · Watch-list leads: 0 · Watch-list leads shown (total): **0**" — and the table's only row: "_**No items met the relevance floor this cycle.**_" |
| `digests/2026-06-15_ISDS-Thematic-Watch/meta.json` | `screened: 14, matches: 0, watch_list_leads: 0, accepted: 0` |

**Status: DIVERGENT, and the code sides with the README. The archive settles it empirically.**
The floor is real and unconditional (`src/main.py:53-69`); **two archived runs published zero
items**, one of them saying so in the digest's own table; so "never empty" is false on the
homepage, false in `fingerprint.yaml`'s header comment, and false in the `src/main.py`
comment that names a rule the code does not implement. This is not a matter of interpretation
— the promise is contradicted by two files the site itself publishes.

**A fix here must also change:** the template *and* `fingerprint.yaml:2-3` *and*
`src/main.py:272`. The last one is the trap: it is a code comment, it will not appear in any
prose sweep, and it is the only place the phrase "never-empty … rule" is stated as though a
rule of that name exists. `HANDOFF.md:89` is compatible with removal (an email is always sent;
its contents may be a one-sentence note) and should be left alone unless the sending
behaviour itself changes.

---

## C6 — Human-review status

| Stated in | What it currently says |
|---|---|
| `HUMAN_REVIEW.md:89` | "_**No human review has been logged yet.** The first monthly checkpoint is due one month after the first daily record (2026-06-23)._" |
| `HUMAN_REVIEW.md:94-98` | The Cycle 1 draft "**is a DRAFT, not a review** — no human has reviewed these claims" |
| `HUMAN_REVIEW.md:111` | "### 2026-06-29 — Cycle 1 — **DRAFT** (council-prepared, pending operator ratification)" |
| `HUMAN_REVIEW.md:172` | "### 2026-07-18 — Cycle 1 — **COMPLETED** (operator review, conducted in-session)" |
| `HUMAN_REVIEW.md:174-212` | A real operator review: reviewer named, three items, "Final pass rate: 1 verified + 1 partial / 3 assigned", "Sign-off: operator confirmation received in-session, 2026-07-18" |
| `HUMAN_REVIEW.md:65` | "**Standing rule.** Until a review cycle is logged for the period, the system's outputs for that" period are provisional |
| `STATE_OF_THE_ANSWER.md:56` | "**Operator-verified 2026-07-18** … (**first completed human-review cycle**, `HUMAN_REVIEW.md`)" |
| `scripts/site_templates/how_it_works.html.j2:35-36` | "**no claim is published as fact without a human check against its original source**" |
| `docs/how-it-works.html:66-67` | Same sentence, generated — **this is the site's strongest safeguard claim** |
| `METHODOLOGY.md:41` | "they do not remove the need for human-in-the-loop review, and the digest annotations **are meant to be verified by a reader** before they are relied upon" |
| `analytics/verification_ledger.jsonl` (`main`) | **21 operator marks, 37 claims**. A further **17 marks and 3 claims** exist only on `origin/chore/operator-marks-2026-07-27` and have never reached `main` |

**Status: DIVERGENT — and the sharpest contradiction is inside one file, 83 lines apart.**
`HUMAN_REVIEW.md:89` says no review has been logged; `HUMAN_REVIEW.md:172` logs one, dated
three weeks earlier than today, with a sign-off. Both are on the page. The reviewer
attributed the completed-cycle statement to "elsewhere in the repository"; it is in fact the
same document, which is worse.

Separately, `docs/how-it-works.html:66-67` asserts a **universal** safeguard ("no claim …
without a human check") that neither the review log nor the ledger supports: one cycle,
three assigned items, one verified and one partial.

**A fix here must also change:** `HUMAN_REVIEW.md:89` (the "none logged yet" paragraph) **and**
`scripts/site_templates/how_it_works.html.j2:35-36` **and** a `docs/` rebuild **and**
`STATE_OF_THE_ANSWER.md:56` if the characterisation of 2026-07-18 changes. **Watch for a new
divergence in either direction:** deleting the site's safeguard sentence while leaving
`:89` saying "no human review has been logged" would contradict `:172`, which logs one;
updating `:89` to acknowledge the completed cycle while leaving the site's universal claim
would leave the universal claim unsupported. Both edits, or neither.

**Also here:** `HUMAN_REVIEW.md:116` reads "The operator (**Jack**) must complete the blank
fields". The operator is **Emory** everywhere else in the project. `:174` correctly reads
"Jack Emory Williams (operator)". This is a naming inconsistency in a file a reader reaches
from the public repository.

---

## C7 — Agent architecture ("research council")

| Stated in | What it currently says |
|---|---|
| `README.md:85-87` | "the brief is produced by what the project calls its research council: **not a set of standing background agents, but a set of clearly-defined roles realized as coordinated stages of the same weekly run**" |
| `README.md:95` | "**Each role is a prompt or pipeline component**" |
| `METHODOLOGY.md:59` | "A **standing council of research agents** produces this brief. Each member is a **separately running AI agent** bound to its own instruction prompt and a named model … **convened daily** by the chairman" |
| `docs/methodology.html` (Part VIII) | Same sentence, generated |
| `scripts/site_templates/how_it_works.html.j2` / `docs/how-it-works.html:63-64` | "**the AI research council** — the research agents, each box naming the model it runs on" |
| `docs/how-it-works.html:7` (meta description) | "the AI research council" |
| `COUNCIL.md` | The seat-by-seat contract; `.claude/agents/*.md` are the definitions; `analytics/daily-research/` are the session records |
| `views/isds-workflow-3d/workflow.json` | **Twelve** model-bearing cards — the **nine** council seats plus `ai-check`, `daily-researcher` and `minutes`, which are stages rather than seats *(corrected 2026-08-05 against `eac8ed9`; this row said "ten" and no file carried that number)* |

**Status: DIVERGENT — README and METHODOLOGY state opposite things about the same
architecture.** README says *not standing agents, roles as stages*; METHODOLOGY says
*standing council, separately running agents*. Both are published (METHODOLOGY as
`docs/methodology.html`; README as the linked repository front page).

**Second divergence inside the same claim, which the reviewer did not name: cadence.**
`METHODOLOGY.md:59` says the council is "**convened daily**"; `README.md:87` places the same
roles inside "**the same weekly run**"; the brief itself is weekly. `analytics/daily-research/`
holds daily records, so "daily" is defensible for the *sessions* and wrong for the *brief
pipeline*. Whichever description is adopted, this distinction has to be made explicitly or
the two files will still disagree after the fix.

**A fix here must also change:** `README.md:85-87` and `:95`, `METHODOLOGY.md:59`, the how-it-works
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
| `scripts/build_site.py:766` | `f"Across {len(rows)} weekly runs from {first['date']} to {last['date']}, "` — the word "**weekly**" is hard-coded; the count is derived |
| `docs/digests/index.html:68-69` | "Across **11 weekly runs** from 2026-06-09 to 2026-08-03, items screened **fell from 78 to 13 as deduplication matured**, while matches stayed at zero throughout and watch-list leads shown were a steady trickle totalling 14." |
| `docs/digests/index.html:68` (chart markers) | The actual series: 78, 79, 14, 80, 11, 12, 13, **23**, 14, 10, 13 |
| `scripts/site_templates/digest_index.html.j2:3`, `:17`, `:50` | "Every **weekly run**", "Each **weekly run** is archived below", "**Weekly run counts**" |
| `.github/workflows/weekly.yml` | `cron: '0 13 * * 1'` — Mondays |

**Status: DIVERGENT on two counts, both in one generated sentence.**
(a) **"Weekly."** Four of the eleven runs are adjacent-day pairs (06-09/06-10, 06-15/06-16),
and 06-22 → 06-29 → 07-06 is weekly. Eleven runs did not occur on eleven distinct Mondays.
(b) **"Fell from 78 to 13 as deduplication matured"** asserts a monotone decline and a cause.
The series is not monotone (80 at position 4, 23 at position 8), and the readout's own chart
data proves it. No isolation of deduplication from source failure, source volume, query
change or schedule change exists anywhere in the repository.

**A fix here must also change:** `scripts/build_site.py:766` — the sentence is **generated**,
so the four `digest_index.html.j2` strings and the `build_site.py` f-string are the only
editable surfaces; `docs/digests/index.html` must be rebuilt, never hand-edited. This is the
one row in this map where the fix is a code change and the `.j2` change alone is
insufficient.

---

## C9 — Target construct: what counts as a positive

| Stated in | What it currently says |
|---|---|
| `scripts/site_templates/index.html.j2:9-13` | "at one **precise doctrinal intersection**: where intellectual property is asserted as a protected investment, a regulatory or judicial measure is the disputed conduct, and the case turns on jurisdiction and admissibility" |
| `docs/index.html` (hero) | Same, generated |
| `scripts/site_templates/index.html.j2:31-34` | "not a word but a *relationship between three doctrines* … operationalised as the **overlap** of three doctrinal 'rings'" |
| `METHODOLOGY.md:19` | The seed corpus "arranges the same three elements" |
| `METHODOLOGY.md:25` | Ring Two is **weighted** so "a claimant alleging a wrongfully rendered court ruling could possibly reach MEDIUM on this ring alone … This ring, however, will only ever reach MEDIUM on its own, and never HIGH" |
| `METHODOLOGY.md:67` | "the hold out set is likely skewed toward NAFTA and ICSID denial-of-justice awards (**Loewen and Mondev utilize more of the judicial measure ring than the full IP-as-investment intersection**)" |
| `scripts/holdout_set.json` / `scripts/backtest_corpus.json` | The four `label: 1` positives are Loewen, Mondev, Apotex, PM v. Uruguay |
| `src/classify.py:219-225` | One ring at/above `STRONG_SUBTOTAL`, or one ring plus an incidental second, reaches the 40-69 MEDIUM band — i.e. the digest threshold |
| `fingerprint.yaml:103-104` | The same rule in prose |

**Status: the site claims an intersection; the label set and the scorer both admit one-ring
items.** METHODOLOGY already concedes the holdout skew at `:67` and already discloses the
Ring-Two weighting at `:25` — so this is **not** a case of a hidden defect; it is a case of
**the homepage stating a narrower construct than the methodology, the labels and the code
implement.** The homepage is where a reader forms the claim, and the homepage says
"intersection" with no qualifier.

**A fix here must also change:** if the project adopts the reviewer's three-tier scheme
(direct / adjacent / background), it lands in **`scripts/holdout_set.json` labels,
`scripts/backtest_corpus.json` ids, `src/classify.py` bands, `fingerprint.yaml:100-104`,
`METHODOLOGY.md:29`+`:47`+`:52`+`:67`, both site templates, and every future digest entry's
status field** — and it invalidates the current precision/recall/accuracy numbers in **C1**,
because the positive class changes. **This is the row most likely to create new divergence:
any relabelling silently falsifies C1 unless C1 is regenerated in the same change set.**

---

## C10 — Publication floor: what reaches the public digest

| Stated in | What it currently says |
|---|---|
| `src/config.py:28` | `RELEVANCE_FLOOR = 25` |
| `README.md:72-78` | Fills to six items with near-misses at or above 25 |
| `digests/2026-08-03_ISDS-Thematic-Watch/README.md:11` | The run's sole entry: score **25**, rings matched "**N/A**" |
| `digests/2026-08-03_ISDS-Thematic-Watch/articles/01_gazprom-affiliate-receives-shares-in-linde-s.md:14` | Its own annotation: "it **does not** engage intellectual property as a covered investment, **challenge a judicial measure** under treaty law, or raise **jurisdictional/admissibility** doctrines … **no ISDS thematic intersection**" |
| `digests/2026-08-03_ISDS-Thematic-Watch/index.html:145` | The same annotation, published |
| `scripts/site_templates/index.html.j2:9-13` | The homepage's "precise doctrinal intersection" |

**Status: the published record contains an item whose own published annotation says it
matches nothing.** This is not a drift between two files — it is a single artifact
contradicting itself on one page, and it is the most visible instance of C9 on the live site.

**A fix here must also change:** `src/config.py:28` or the surfacing rule in
`src/main.py:53-69`, plus `README.md:72-78`, plus `HANDOFF.md:101`, plus C5's "never empty"
row — **raising the floor and keeping "never empty" would be a direct contradiction.** C5 and
C10 must be decided together.

---

## C11 — Source count

| Stated in | What it currently says |
|---|---|
| `README.md:52` | "the **nine** sources" |
| `scripts/site_templates/how_it_works.html.j2:27` / `docs/how-it-works.html:58` | "the first band is the **nine public sources** checked" |
| `docs/how-it-works.html:7` | meta description: "the **nine** public sources" |
| `views/isds-workflow-3d/workflow.json` | The source band on the flowchart |
| `alerts.yaml:12-17` vs `:29-42` | Talkwalker documented as the intended replacement lane; the `feeds:` list contains **only Google URLs and zero Talkwalker entries** — recorded open at `agents/Workflow Threads.md` C5 |

**Status: unverified this session.** The count is asserted in three places from one flowchart
band; the archivist's 2026-08-03 sweep escalated "README's source and email counts" and the
escalation's full statement was written to a destination that does not exist (see the session
record). **This row is a placeholder with a known open lane, not a clean bill.**

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

**Watch for a new divergence, and it is a real one:** because `model:` is a **tier**, the
frontmatter cannot disagree with a card about *version*. The guard's version check therefore
rests entirely on card ↔ `src/models.py` ↔ vault note. **If a seat's vault note stops stating
a model in the `**Model.** \`…\`` form that `_VAULT_MODEL_RE` (`check_models.py:63`) matches,
that leg of the check silently has nothing to compare** — the archivist's formatting is
load-bearing for a CI guard, which is worth knowing before anyone reformats these notes.

---

## C13 — What Ring 3 *is*: a doctrinal dimension, or a disposition

**Added 2026-08-05, before the council ruled, because this is the row that decides whether
the ruling is cheap or expensive.** Two incompatible tests are in the tree at the same time.

- **Definition A — DIMENSION.** Ring 3 is engaged when jurisdiction/admissibility doctrines
  are *live and litigated in the case*, whatever the outcome.
- **Definition B — DISPOSITION.** Ring 3 requires that the tribunal actually *disposed of the
  case* at the threshold, without reaching the merits.

### Stated as B (disposition)

| Stated in | What it currently says |
|---|---|
| `prompts/research_analyst.txt:18-20` | "(3) the tribunal **disposes of the case** at the JURISDICTIONAL / ADMISSIBILITY stage … **without reaching the merits**" |
| `prompts/research_analyst.txt:113` | "attacked through a measure, and **disposed of at the jurisdictional gate**" |
| `prompts/council_chairman.txt:8-9` | "(3) **disposal at the jurisdictional/admissibility stage**" |
| `.claude/agents/council-chairman.md:31-32` | "(3) **disposal at the jurisdictional/admissibility gate**" |
| `prompts/council_calibration.md:20-23` | "…and **disposal at the jurisdictional/admissibility stage** — not surface keyword matches". Injected into every analyst run at `prompts/research_analyst.txt:7` (`{{CALIBRATION}}`), so it binds every seat |
| `prompts/systems_researcher.txt:18-19` | "Ring 3 **jurisdictional/admissibility disposal**" |
| `prompts/research_editor.txt:28` | "or for the **jurisdictional/admissibility gate**" (weak B) |
| `prompts/classifier.txt:12-14` | "(3) jurisdictional / admissibility doctrines **decide the case**" — contradicts `:60-61` in the same file |
| `moc/Research Question.md:3-5` | "…and **disposed of at the jurisdictional/admissibility gate?**" — the vault's own statement of the question |
| `METHODOLOGY.md:10` (Part I) → `docs/methodology.html:96` | "a rule of law applied at the jurisdictional or admissibility level **determines that the case cannot proceed**" |
| `STATE_OF_THE_ANSWER.md:4` | "…and **disposed of at the jurisdictional or admissibility stage**" — the living-memory header |
| `scripts/site_templates/index.html.j2:13` → `docs/index.html:45` | "**the case turns on** jurisdiction and admissibility" — the homepage hero (also carried at C9) |
| `scripts/site_templates/base.html.j2:162` | "the threshold **on which the seed cases were decided**" |
| `working/02c-framework-rings.original.txt:7` | "**Ring 3 — The case is decided at the threshold, not on the merits.** … each case **died on** jurisdiction and admissibility" |
| `working/one-pagers/philip-morris-v-australia.md:18`, `:22`, `:30` | "Ring 3 (**jurisdictional disposal**)"; "**is disposed of** at the jurisdictional gate"; "**survives** the jurisdictional gate" — B, and true of *this* seed |

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

### Mixed — one paragraph carrying both

| Stated in | What it currently says |
|---|---|
| `METHODOLOGY.md:26` → `docs/methodology.html:105` | Heading: "Threshold Questions … as a Potentially Dispositive **Dimension**" (A). Defining sentence: "This ring observes **the ground on which a case may be denied disposition prior to having its merits addressed**" (B-shaped). Closing: "these preliminary questions **may** act as dispositive issues — and did in Philip Morris — **even though all three seeds were not decided based on these issues**" (A). **The seed facts here are correct.** This is the adopted 2026-06-29 fix, and it is *not* the memo's own recommended wording at `ring3-reconciliation.md:133`, which was cleanly A |

### A third sense, in live use, that neither definition covers

| Stated in | What it currently says |
|---|---|
| `analytics/insights.jsonl` (17 lines), `STATE_OF_THE_ANSWER.md:114-124`, `state/research_log.json:111`, `:171`, `:201`, `:211`, `analytics/optimization-log.md:34`, `analytics/council-log.md:50` | A **"Ring 3 taxonomy"** grown by the research layer, now at **five mechanisms**: abuse-of-right/critical-date, administrative-review prerequisite, fork-in-the-road, MFN-forum-access, first-generation-BIT scope limitation. **Not one of the four new mechanisms appears in `fingerprint.yaml:81-102`.** The research layer's Ring 3 and the classifier's Ring 3 have different contents |

**Status: DIVERGENT, and the split runs through single files and single pages.**
`scripts/site_templates/base.html.j2` states B at `:162` and A at `:169`, seven lines apart,
in one JavaScript object; `prompts/classifier.txt` states B at `:12-14` and operates on A at
`:26-28`/`:60-61`/`:149`; `docs/index.html` renders the A card at `:100-105` and the B readout
at `:383-385`.

**The asymmetry that should decide the cost question.** Nothing in the machine implements B.
`fingerprint.yaml`'s Ring 3 is seventeen doctrinal phrases with no outcome term;
`src/classify.py` never sees a disposition; ring presence is a keyword subtotal. If **A** is
adopted, the edit list is the B table above and no scoring artifact moves — which is the
position `ring3-reconciliation.md` already took and `METHODOLOGY.md:26` already implements.
If **B** is adopted, every A statement above becomes false, **and B is still not
implementable** by the deterministic layer — it could only ever be applied by
`prompts/classifier.txt` and by prose.

**A fix here must also change** — beyond its own table — **`scripts/site_templates/base.html.j2:162`
regardless of which definition wins**, because that sentence is false today on the project's
own verified facts (Eli Lilly and Bridgestone were decided on the merits;
`ring3-reconciliation.md:16-22`), and because `base.html.j2` is inherited by all six page
templates, so it renders on **sixteen published pages**: `docs/index.html:385`,
`docs/methodology.html:260`, `docs/how-it-works.html:350`, `docs/backtest.html:603`,
`docs/digests/index.html:450`, and all eleven `docs/digests/<date>.html`. **This is the
largest single surface in the map and no prose sweep finds it** — it is a string inside a JS
object literal inside a base template.

**Watch for a new divergence:** adopting **B** would leave 26 of Ring 3's 100 weight points
sourced from Bridgestone — `shell subsidiary` (6), `definition of investor` (5),
`abusive tactics` (4), `standing of licensor vs licensee` (4), `standing to claim denial of
justice when not a party` (4), `exhaustion of local remedies` (3), all tagged
`seed: bridgestone` at `fingerprint.yaml:94-100` — i.e. a quarter of the ring drawn from a
case that under B does not engage the ring at all. Adopting **A** requires
`METHODOLOGY.md:26`'s *defining* sentence to move, not only its heading, and requires a
decision on the Eli Lilly clause: `METHODOLOGY.md:26` says Ring 3 "did not form part of the
reasoning in Eli Lilly", while `working/one-pagers/eli-lilly-v-canada.md:22` records a time-bar
objection that was raised and rejected — which under A *is* a live Ring 3 engagement.

---

## C14 — The holdout's composition, and the Apotex item's identity

| Stated in | What it currently says |
|---|---|
| `scripts/holdout_set.json` (`apotex_v_us`) | `"label": 1, "prov": "partial"`, text opening **"Apotex Holdings v. United States."** and reciting FDA abbreviated new drug applications plus "**does not qualify as an investor who has made an investment** … disposing of the case on the **definition of investor and jurisdiction**" — the **2013 Apotex Inc.** award's holding under the **2014 Apotex Holdings** caption |
| `scripts/backtest_corpus.json` | `apotex_v_us` in `holdout_positive_ids`; the miss reason recorded in the same file |
| `METHODOLOGY.md:52` → `docs/methodology.html:118` | One physical line carrying **all of**: "holdout of **twenty** items", "**Four** of the twenty were on-theme positives", the four names, "compared against **sixteen** other awards", "the item captioned Apotex v. United States **recites the jurisdictional holding of the 2013 Apotex Inc. award rather than that of the 2014 Apotex Holdings award its caption names**", "the Apotex item as **partial**", "precision of **1.00**" (×2), "recall of **0.75**", "accuracy of **0.95**", "F1 of **0.86**" (×2) |
| `METHODOLOGY.md:67` | "— **twenty items, only four positives** —" |
| `scripts/check_claims.py:195-238` | Facts 6–12 (`holdout items`, `holdout on-theme positives`, `holdout off-theme negatives`, `precision`, `recall`, `accuracy`, `F1`). Authorities are **live harness runs** of `scripts/eval_holdout.py` and `scripts/backtest.py`; mirrors are regex substrings on `METHODOLOGY.md:52` and `:67`. **Nine of the registry's twenty-nine mirrors point into `METHODOLOGY.md:52` alone** |
| `tests/test_check_claims.py:53-55` | `assert a["n"] == b["n"] == 20`; `a["n_pos"] == b["n_pos"] == 4`; `a["n_neg"] == b["n_neg"] == 16` — asserted independently of the registry |
| `agents/systems-researcher.md:28` / `.claude/agents/systems-researcher.md` / `prompts/systems_researcher.txt` | The seat's standing weak-point list names "the deterministic scorer's **'not-a-covered-investment' miss (Apotex)**" |
| `scripts/backtest_corpus.json:57` (`display_names`) | "**Apotex Holdings v. United States**" — the caption the *published site* renders, and it is a **second, independent** copy of the wrong caption. Fixing `holdout_set.json` alone leaves the site still saying "Holdings" |
| `scripts/backtest_corpus.json:52` (`miss_reasons`) | "Apotex turns on a **negative jurisdictional finding** — the tribunal held the claimant was not an investor and the FDA filings were not a covered investment…" |
| `docs/backtest.html:267`, `:270`, `:272`, `:275`, `:459` | The published table row: caption "Apotex Holdings v. United States", score **8**, band **LOW**, "**false negative**", and the miss-reason paragraph — all generated from `backtest_corpus.json` |
| `lit-review/kim-memo.md:72-80` | **The only citation of the case anywhere in the repo**: "Apotex Holdings Inc. & Apotex Inc. v. United States, **ICSID Case No. ARB(AF)/12/1, Award (Aug. 25, 2014)**", annotated as the FDA **import-alert** dispute — i.e. the 2014 case, correctly cited, and **a different dispute from the ANDA holding in `holdout_set.json`** |
| `METHODOLOGY.md:21` → `docs/methodology.html:102` | "The **Apotex v. United States** case defines the outer limit of what would be considered an 'investment'" — caption used without a year, so it is true of the 2013 award and reads as though it were the cited 2014 one |
| `think-tank/methodology/ring3-reconciliation.md:94` | "the holdout's lone false negative, **Apotex Holdings v. United States**, is precisely a case **decided on a Ring-3 disposition**" — **false as written**: it is the 2013 *Apotex Inc.* award that was so decided |
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

**Consequence for the repair, stated as a fork:**

1. **Caption-only repair** (fix the caption to the 2013 *Apotex Inc.* award, whose holding the
   text already recites): **metrics-neutral and guard-neutral.** Score stays 8, the item stays
   the false negative, precision/recall/accuracy/F1 stay 1.00/0.75/0.95/0.86, Facts 6–12 stay
   green, `tests/test_check_claims.py:53-55` stays green. The only prose that must move is the
   candor clause on `METHODOLOGY.md:52` — and moving it means rewriting the one line that
   nine declared mirrors point into.
2. **Substitution repair** (replace the text with the real 2014 *Apotex Holdings* award):
   changes the scored text, therefore possibly `recall`/`accuracy`/`f1`, therefore Facts 10–12,
   therefore the four figures on `METHODOLOGY.md:52`, therefore `docs/` — and it would
   **destroy the empirical prop under C13's Definition A**, because
   `ring3-reconciliation.md` §3.3 relies on this item being the *jurisdiction-disposed* case
   that the scorer misses. *Apotex Holdings* (ARB(AF)/12/1, 2014) was not disposed that way.

**A fix here must also change:** `METHODOLOGY.md:52` **and** `:67` if any count moves, a
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
