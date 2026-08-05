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

**Snapshot anchor.** Audited against `c9050e6` (`main`, 2026-08-04, clean tree). Paths
claimed to be described: `README.md`, `METHODOLOGY.md`, `HUMAN_REVIEW.md`, `HANDOFF.md`,
`COUNCIL.md`, `fingerprint.yaml`, `docs/`, `scripts/site_templates/`, `scripts/`, `src/`,
`digests/`. Staleness is a one-command question:
`git log c9050e6..HEAD -- <those paths>`.

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

## C1 — Holdout size and headline accuracy

**There is no single authoritative evaluation file. There are two datasets.**

| Stated in | What it currently says |
|---|---|
| `scripts/holdout_set.json` | **20 items**, 4 labelled `label: 1`, 16 unlabelled negatives. Consumed by `scripts/eval_holdout.py`. |
| `scripts/backtest_corpus.json` | **12 items** — `holdout_positive_ids` 4, `holdout_negative_ids` 8. Consumed by `scripts/backtest.py`. Its own `_note` says "deliberately small (~12-15 known cases)". |
| `METHODOLOGY.md:52` | "an exploratory holdout of **twenty** items using eval_holdout.py. Four of the twenty were on-theme positives … compared against **sixteen** other awards … a precision of 1.00, a recall of 0.75, and an **accuracy of 0.95**, for an F1 of 0.86" |
| `METHODOLOGY.md:67` | "The small exploratory hold-out set in Part VI.B — **twenty items, only four positives**" |
| `docs/methodology.html:112` / `:126` | The same two sentences, generated. |
| `scripts/site_templates/backtest.html.j2:114` | "{{ bt.holdout.total }} cases in all, none used in development" |
| `docs/backtest.html:155` | Renders as "**12 cases** in all, none used in development" |
| `docs/backtest.html:161` | "Confusion matrix … across **12**" |
| `docs/backtest.html:175-183` | TP 3, FN 1, FP 0, **TN 8** (against METHODOLOGY's 16 negatives) |
| `docs/backtest.html:202-205` | precision 1.00, recall 0.75, **accuracy 0.92**, F1 0.86 |

**Status: DIVERGENT, and the divergence is arithmetic, not editorial.** Both pages are
internally correct for their own dataset — 3/4 + 16/16 = 19/20 = 0.95; 3/4 + 8/8 = 11/12 =
0.92. The site does not tell a reader that two datasets exist. The four positives are
identical in both (`loewen_v_us`, `mondev_v_us`, `apotex_v_us`, `pm_v_uruguay`); only the
negatives differ, 16 vs 8.

**A fix here must also change:** every row above. If the fix is "one authoritative dataset,
both surfaces generated from it," then `METHODOLOGY.md` stops stating metrics in prose and
the number moves into the build — which is a `scripts/build_site.py` change, i.e. a second
seat. **Do not** change 0.95 to 0.92 in `METHODOLOGY.md` alone: that would make the prose
false about `holdout_set.json`, which still holds 20 items.

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
| `views/isds-workflow-3d/workflow.json` | Ten agent cards in a "council column", each naming a model |

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
`COUNCIL.md`, the ten flowchart cards in `views/isds-workflow-3d/workflow.json`, the ten
`.claude/agents/*.md` definitions, the twelve `agents/*.md` vault notes, and this vault's own
`hub: Council`. **That last list is why a wholesale renaming is a far larger change than it
looks, and it is the archivist's to absorb.**

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
| `.claude/agents/*.md` frontmatter | chairman + analyst `opus-5`; four utility seats `opus-4-8`; **`systems-designer` and `site-experience` declare no `model:` key** |
| `views/isds-workflow-3d/workflow.json` | `systems-designer` and `site-experience` cards read "**Model: Claude Opus 5**" — asserted by no configuration file |
| `agents/*.md` (twelve notes) | Verified matching `src/models.py` on 2026-08-04 |
| `HANDOFF.md:29`, `:163` | Corrected 2026-08-04 |
| `COUNCIL.md`, `METHODOLOGY.md` Part VIII | Carry the assignment in prose |

**Status: one open divergence, on record and escalated.** Two flowchart cards assert a model
no file carries. Raised 2026-07-31, re-escalated 2026-08-04
(`analytics/vault-sessions/2026-08-04.md`, both sessions). Emory's call: a `model:` line in
each definition, or a card reading "inherits the invoking session".
`.github/workflows/model-consistency.yml` (`c25ea64`) now makes card/definition drift fail —
**verify whether that guard covers the two undeclared seats or exempts them**; it was added
after the last archivist session and this map has not tested it.

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
