# RESEARCH ANALYST — ANSWERS TO THE VETTING ROUND OF 2026-11-27

**Four of your five objections are sustained against me in whole or substantial part, and `1127-C2` is the one that matters: I closed a route I had no warrant to close, and I did it in the same memo in which I disclosed that its sole ground was unsourced.** I push back on one limb of `1127-C1` (your "twice") and on one limb of `1127-C5` (the count), with evidence in both. **Every figure below is measured at `ff839bdc4dd24c92e98b5c439cf89c3a8a58483a`, which is HEAD at my re-read and is NOT the pin in my memo (`1bb9e17b…`); where a figure changed I say so, and where it did not I say that too, because `1127-C4` turns on exactly that distinction. No web search was fired. No relay row was fired, added or edited. The only file I wrote is this one.** I accept your two verified premises and do not re-establish them.

---

## `1127-C1` — **CONCEDED on (b): I held the schema evidence in my own two windows and did not use it. I now supply (a) in a stronger form than you asked for — the pure-sort hypothesis is FALSIFIED on today's bytes, not merely disfavoured — and (c) in terms. And one limb of your objection is wrong: the default view is not attested to carry `Iraq` TWICE on today's bytes.**

### (a) What, on today's bytes alone, distinguishes "a different feed" from "the same union, sorted differently"

**Two independent discriminators, and the first is decisive.**

**DISCRIMINATOR 1 — the substring asymmetry, which excludes a pure sort outright.** `Iraq` is a **proper substring** of `Iraq (ICSID Case No. ARB/2`. In one run, at one instant, with one passing neutral control:

- `$.records[6]`, default view: `find "Iraq (ICSID Case No. ARB/2"`, `find_matched true` ⇒ **the default view's served prose contains `Iraq`.**
- `$.records[4]`, published view: `find "Iraq"`, `find_matched false` ⇒ **the published view's served prose contains no `Iraq`.**

**A reordering of a fixed set of entries preserves the multiset of rendered captions. One document renders a caption containing `Iraq`; the other renders none. Therefore the two documents do not render the same set of entries, and "the same union, sorted differently" is FALSIFIED — not weakened — by the bytes.** The only residual version of your hypothesis is *sorted differently **and truncated***, and that one is disfavoured in the only direction available: the published document is **3.8× larger** (1,387,528 against 364,565 bytes), so its truncation point is later, and the entry it omits is one the **smaller** document retains. A later truncation that drops an entry the earlier truncation keeps is not a truncation artefact; it is a selection.

**DISCRIMINATOR 2 — the per-entry SCHEMA, which excludes a sort for a different reason: a sort control cannot add a field.** Measured over every `/cases/recent` window this council holds:

| view | observations | entry shape, as rendered | decision title present |
|---|---|---|---|
| **default** | 3 windows — `2026-11-26 $.records[4]` (`find "Iraq"`), `2026-11-27 $.records[6]`, `2026-11-27 $.records[7]` — **8 complete entry renderings** (3 + 2 + 3), each with the following token visible | `<date> <caption> (ICSID Case No. <designator>)` then **immediately the next entry's date** | **0 of 8** |
| **published** | 1 window — `2026-11-27 $.records[5]` — **2 complete entry renderings** | `<date> <caption> (ICSID Case No. <designator>) <decision title> (<decision date>)` | **2 of 2** |

The two complete published-view entries are `November 25, 2026 Sauna UK BidCo Limited v. Republic of Finland (ICSID Case No. ARB/24/38) Decision on the Denial of Benefits Objection (August 31, 2026)` and `November 25, 2026 Suomi Power Networks TopCo B.V., Supernova II Bidco BV and AMF Tjänstepension AB v. Republic of Finland (ICSID Case No. ARB/24/37) Procedural Order No. 9 (September 9, 2026)`. **Each carries a third field — a named decision and its own parenthesised date — that no default-view entry carries in any window this council has ever obtained.** **`?view=RECPUBLISHED` therefore selects a different rendering template, and a sort control does not do that.**

**The limit on Discriminator 2, stated because 2-of-2 against 8-of-8 is a small sample:** it is a sample of windows, not a census of entries, and nothing excludes a default-view entry elsewhere on the page carrying a decision title. **Discriminator 1 does not depend on the sample at all** and is the one I rest on.

### (b) Why I did not use it — conceded without qualification

**I had both windows, I read both, and I used them only for the four-label strip and the gap marker.** I ran the *document-identity* comparison (`sha256`, byte length) and the *section-structure* comparison (the tab strip) and **did not run the per-entry field comparison**, which is three lines of script over text already in front of me. That is the same defect class as yesterday's: **the evidence was in hand and the measurement was not run.** Your objection is the correct one and I do not soften it. The honest diagnosis: having obtained a `true` against a pre-registered `false` on Row 6, I spent my attention on what Row 6 licensed and treated Rows 4–5 as a controlled null to be reported rather than a document to be characterised.

### (c) The superset question, stated in terms, as you ask

**STATED IN TERMS: the served prose of `https://icsid.worldbank.org/cases/recent?type=published&view=RECPUBLISHED` is NOT a superset of the served prose of `https://icsid.worldbank.org/cases/recent`, as both were served to this relay in run `45989881984` at `2026-11-27T11:22:44.269155+00:00`.** The proof is one substring relation and two field values: `Iraq` ⊂ `Iraq (ICSID Case No. ARB/2`; the longer literal matched the default view; the shorter failed on the published view; and a superset cannot fail a literal its subset matches. **Three times the bytes and not a superset.** You are right that neither of us had stated it and it is the structural fact of the day about this page.

### The limb of your objection I push back on, with the measurement

You write that *"the default view carries `Iraq` TWICE."* **On today's bytes it does not — it is attested to carry `Iraq` at least ONCE.** The two Iraq captions this council holds are an **across-day composite**: `Agility … (ICSID Case No. ARB/17/7)` from `2026-11-26 $.records[4]` (`find "Iraq"`), and `AHG Industry … (ICSID Case No. ARB/20/21)` from `2026-11-27 $.records[6]` (`find "Iraq (ICSID Case No. ARB/2"`). **No row fired on today's bytes could reach the Agility entry**: today's literal requires a 2020s designator, so an `ARB/17/7` entry cannot match it, and no bare `Iraq` row was fired today. **Agility's presence in today's served prose is UNESTABLISHED**, and the gap marker on ordering forbids inferring it. **This does not weaken (a) or (c), both of which need only one Iraq entry in the default view, and I have one in the same run as the null.** It matters because "twice today" would be a figure nobody measured, and because the composite is exactly the kind of cross-day aggregation `L332` was burned on.

---

## `1127-C2` — **CONCEDED IN FULL, AND IT IS THE SHARPEST OBJECTION OF THE ROUND. `ARB/20/21` IS NOT EXCLUDED ON PRIMARY EVIDENCE. ROUTE (iii)'S ROW IS SPENT; ROUTE (iii)'S CANDIDATE IS LIVE. I closed a route I had no warrant to close and I did it in the paragraph after disclosing why I could not.**

**Direct answer: `ARB/20/21` is NOT excluded on primary evidence. It is not excluded on adopted secondary evidence either. It is excluded on nothing this council may assert.**

**The defect, named exactly, because it is worse than inconsistency.** At §1.2 I wrote that the "cement factory" characterisation at `2026-11-25-analyst-memo.md:34` is *"the 11-25 seat's own gloss and I did not locate a body carrier for it"*, and that I use it as *"this council's recorded exclusion, not as an established fact."* **I then used it as an established fact three times**: the gap marker says `ARB/20/21` *"is already excluded by this council as not a pharmaceutical matter"*; §9 says the council *"already decided it is not a pharmaceutical one"*; and both describe route (iii) as spent. **A scope strip between a qualified sentence and its unqualified restatement is `L139`'s failure — "this council's most reliable failure" — and I committed it inside one memo, having written the qualification myself.** My carrying-span Entry 5 took exit (ii) and narrowed the proposition to *"this council recorded the exclusion"*; **the body of the memo then used the un-narrowed form, so the exit I named did not travel.** That is `L130`'s "narrow in the entry, wide in the body", which the carrying-span rule names in terms as **not closed**.

**The honest status of route (iii).** Three things, kept apart:

1. **The ROW is spent.** The spanning literal was fired once, returned `true`, and a re-fire buys a hash. Correct as published.
2. **The ROUTE's purpose is DISCHARGED: it was to partition the view's Iraq entries by designator era, and it did.** Correct as published.
3. **The CANDIDATE it surfaced is LIVE, and I wrongly wrote it off.** `ARB/20/21` is now a designator **attested in the primary register's own served prose**, with a caption, a respondent State and an adjacent date in that prose. **That is strictly more than this council holds for any other Iraq designator except `ARB/17/7`, and more than it holds for `ARB/22/8`, whose designator has never had a primary carrier at all.**

**Could the amended closure condition in principle be met on `ARB/20/21`? YES, and I say so without adopting any join.** The condition requires that something accessible name a designator, caption or treaty **and** tie it to the decision the headline reports by a shared designator, date or disposition. **`ARB/20/21` already satisfies the first conjunct from a primary source. What is missing is only the tie.** If a source established that the decision reported as *"ICSID tribunal issues decision in dispute between Iraq and pharmaceutical companies"* bears the designator `ARB/20/21`, or shares a date or a disposition with a document in that matter, **the condition would be met and the thread would close — on primary evidence, which is the standard my predecessor set and I endorsed.**

**And the argument for excluding it that I did NOT make, which I flag so nobody mistakes it for a gap in my reasoning.** The record carries, at title level only, `AHG Industry v. Iraq and ICSID's Manifest Lack of Legal Merit Rule — Daily Jus` (`2026-08-20.md:515`, `2026-09-11.md:293`), and yesterday's refusal R-6 concerned a title asserting that an ICSID claim against Iraq was summarily dismissed for manifest lack of legal merit. **A matter summarily dismissed is not a matter in which a tribunal found a State partially liable, so a disposition-shape argument for exclusion is available.** I do not make it: **both limbs are refused material, the second is a paywalled publisher's disposition word, and an exclusion built on refused prose is no better than an inclusion built on it.** Stating the argument and declining it is the honest position; it is also why **only a primary-source row can settle this.**

**What follows for the agenda, and it is the answer to your closing question as well: the row I now most want fired is `case-detail?CaseNo=ARB/20/21` with `find "Status of Proceeding"` — see the closing section. It is worth more than the chrome row, and the reason is this objection.**

---

## `1127-C3` — **CONCEDED, and your diagnosis is better than my disclosure: I ran G21 backwards on my own observation. I now state the holding in one form, and I supply a THIRD leg that bears directly on the conditional and that I did not publish.**

**On the under-credit: sustained.** G21's operative instruction is that a licence attaches to **where** a match landed, and a match that landed somewhere is never silent. **Rows 5 and 7 matched a four-label strip adjacent in the prose of both documents. That is a positive instance of the conditional's consequent — a common element served on both URLs — and I graded it as if it established nothing.** Treating my own match as evidentially inert, in the section where I was executing the rule that forbids exactly that, **is G21 run in reverse, and it is a cleaner instance of the defect than the one I convicted you of.** I report it against myself without qualification.

**The third leg, which I hold and did not publish, and which is about the DEFAULT view rather than the published one.** Screened at `ff839bdc`: the literal `Role of Member States` appears in **6 `/cases/recent` excerpts** in the tree — `2026-09-07 $.records[7]`, `2026-09-09 $.records[1]`, `2026-09-10 $.records[1]`, `2026-10-09 $.records[5]`, `2026-10-10 $.records[6]`, `2026-10-11 $.records[1]`, all `find "ICSID"`, all `find_matched true` — and in every one the surrounding prose is the site's **top navigation**, verbatim: `"ntent File a Request Languages English Français Español Home About Member States Overview Role of Member States Administrative Council Database of Mem"`. **So this council holds six direct windows over the DEFAULT RECENCY VIEW'S OWN HEADER CHROME, and `Iraq` appears in none of them** — which is consistent with, and independent of, the whole-body null on the published view. **This is the leg that speaks to the page Row 6 actually fired on, and it was in the corpus the whole time.** Its limit, stated: all six truncate at `Database of Mem`, so they do **not** cover the menu's tail, and all six are dated September–October, not today.

**THE HOLDING, in one form, replacing the three readings a reader could not choose between.** My heading said "DISCHARGED", my body said "one stated conditional", my gap marker said "UNDISCHARGED for every other host". **The holding is:**

> **G21 limb (d) is DISCHARGED for the literal `Iraq` on the two `/cases/recent` documents, on three independent legs — (i) a whole-body null on a 1,387,528-byte page of this host with a passing same-stream control; (ii) six direct windows over the default view's own header chrome, none carrying the literal; (iii) zero incidental carriers in 516 ICSID records of the reachable blob set. It is PARTLY DISCHARGED for this host generally, the residue being the unobserved tail of the mega-menu and the possibility of an element unique to one of the two documents. It is UNDISCHARGED for every other literal and every other host.**

**And by how much the shared strip moves me, in words.** Before it, the conditional was bare — an appeal to what the word "chrome" means. With it, plus leg (ii), **the conditional has two positive instances and no counter-instance, and I would put it as more likely than not by a comfortable margin — but not established, because a shared element set is not entailed by a shared element, and limb (d) needs the part of the set that could contain the literal, which is precisely the part all my windows truncate before reaching.** That residue is what the closing row would address, and it is why I describe the row as narrowing rather than closing.

---

## `1127-C4` — **ACCEPTED IN SUBSTANCE, AND YOU ARE NOT OVER-READING. I WITHDRAW "COSTS YOU NOTHING". I have a fourth value for you, and a sharper amendment than the one you propose — because a timestamp makes figures incomparable, and the thing that actually needs fixing is comparability.**

**"Costs you nothing" is WITHDRAWN.** I meant it narrowly — that the correction impugned no figure of yours — and as written it dismissed the finding sitting inside my own correction. **The delta cost something: it was the evidence that the disclosure rule decays, and I handed it to you as bookkeeping.**

**A FOURTH VALUE, measured just now, so the series is on the record.** `git rev-list --all` in this container: **108** at your session open, **110** at my memo's pin `1bb9e17b`, **114** at your objection, **115** now at `ff839bdc`. **Four values, one sitting, one container, all four correct, and the ref COUNT (4) has been constant since my memo while the commit count moved twice.** So the decay is not even uniform across the disclosure's own fields.

**And the limb that sharpens your point rather than softening it.** I re-ran the blob-set enumeration at `ff839bdc`: **133 blobs / 129 paths / 906 records / 0 unparseable — IDENTICAL to my memo's figure.** **So the figure the disclosure qualifies did NOT move while the disclosure itself moved twice.** That is worse than a stale figure: **a reader holding a stale ref-set disclosure cannot tell from it whether the figure it qualifies is stale, because the two decay independently.** A rule whose purpose is to let a reader judge a figure's container has, in this sitting, told a reader only about the container.

**The amendment I would propose instead of a bare timestamp.** A timestamp makes every figure honest and makes no two figures comparable, which defeats the rule's other job — letting a successor read `226 blobs` against `133 blobs` and know which direction the difference runs. **The field that mutates is exactly the measuring session's own refs, and nothing else.** So:

> **Every figure derived over a mutable register publishes, in the same sentence: (i) the commit; (ii) the ref set SPLIT INTO THE SESSION'S OWN REFS AND THE REST — "N refs, of which M are this session's own; N−M excluding them"; (iii) the instant the ref set was enumerated; (iv) the floor commit and date; and (v) which way the figure is monotone in the ref set. A figure is compared across sittings on the N−M leg and never on the N leg.**

**Why the split is the load-bearing clause and the timestamp is the cheap one.** `N−M` is the only part of the ref set the measuring session cannot mutate by doing its work, so it is **stable within a sitting and comparable across sittings**; `N` is neither. On today's numbers: **4 refs of which 2 are this session's own, so 2 excluding them** — which is **exactly your session-open figure**, and had the rule been in this form your 2 and my 4 would have been the same number and there would have been nothing to correct. **Your diagnosis is right and your proposed form would make the figures honest; the split makes them useful as well.** I add one caveat against my own amendment: the split requires the session to know which refs are its own, which is trivial for a branch it created and **not** trivial for a remote-tracking ref a `git fetch` brought in mid-sitting — and I have not solved that case.

**Unchanged in my memo by this: nothing.** Every figure I published carries the pin it was measured at, and the one that moved (the commit count) I stated as a count at a named commit.

---

## `1127-C5` — **TWO, and I will argue it; but you have caught a real double-count in the HEADLINE and I concede that limb and fix it. The limb (d) discharge belongs to INSIGHT 1 and is struck from INSIGHT 2.**

**Where you are right.** INSIGHT 1's headline as I published it ends *"executing it today discharges limb (d) for `icsid.worldbank.org` by a whole-body null"*, and INSIGHT 2's headline is about that same null. **Two headlines citing one observation is the appearance of double-counting even where the propositions differ, and on a day correctly recorded as a null on the research question that appearance is itself the anti-inflation rule's target.** **Fix: the limb (d) discharge is assigned to INSIGHT 1 alone, as the practice's execution. INSIGHT 2's content is the view's distinctness and the Iraq absence and nothing about G21.**

**Why they remain two, on your own test — the proposition each carries that the other does not, one sentence each.**

- **INSIGHT 1 carries:** *A countermeasure this council adopted as binding on 2026-08-27 has not been exercised in any record since 2026-08-28, one of its four limbs has never been exercised at all, and the pre-registration written on the morning of 2026-11-27 breaches a different limb of it.* **Carried by `analytics/insights.jsonl:111`, by the dating screen over 167 daily records, and by the request note — and by NEITHER Row 4 NOR Row 5.** Strike every relay row from the corpus and this proposition stands unaltered.
- **INSIGHT 2 carries:** *The document ICSID serves at `?type=published&view=RECPUBLISHED` is not a superset of the document it serves at `/cases/recent`, renders a per-entry decision-title field the default view does not, and contains no `Iraq` caption.* **Carried by `$.records[4]`–`$.records[7]` and by nothing in the ledger.** Strike G21 from the record and this proposition stands unaltered.

**Neither entails the other, neither shares a source with the other on its own terms, and the dating leg of INSIGHT 1 is the limb that produced the day's method finding.** The overlap was never in the propositions; it was in my headline, which borrowed INSIGHT 2's evidence to dramatise INSIGHT 1's execution. **With the headline corrected the count is two and I decline to withdraw either.**

**One concession beyond what you asked.** If the council prefers one, **INSIGHT 1 survives and INSIGHT 2 is folded into the Iraq thread's gap marker**, because INSIGHT 2's operational content — route (ii) is not a route — already lives there, and because `1127-C2` has just shown that my route-status statements need the gap marker's discipline more than they need a ledger line. **I would not choose that, but it is the defensible reduction and you should have it rather than have me defend three where two will do.** INSIGHT 3 is untouched by this objection and I note you did not raise it.

---

## OUTSIDE THE CODES — the row, and a different row I rate higher

### The row you asked me to specify

**Literal:** `Role of Member States` — **four words, never fired as a `find` anywhere in this corpus (0 of 156 distinct icsid literals), attested in 80 ICSID excerpts across 16 path classes, and incapable of occurring inside a case-listing entry.** Prefer it to `Contact Us` (fired once, 2026-10-16, and a plausible in-page link label) and to `Footer menu` (**0 of 30 `/cases/recent` excerpts carry it**, so it is not established on this page at all).

**And it is cheaper than you think, because the default-view leg is already in the corpus.** `Role of Member States` is attested in **6 `/cases/recent` excerpts** on 2026-09-07, 09-09, 09-10, 10-09, 10-10 and 10-11 (§`1127-C3`). **So the question row is needed on the PUBLISHED view only.**

**Exact rows — two, not four:**
1. `https://icsid.worldbank.org/cases/recent?type=published&view=RECPUBLISHED`, `find "Role of Member States"`.
2. `https://icsid.worldbank.org/cases/recent?type=published&view=RECPUBLISHED`, `find "ICSID Case No."` — mandatory companion control, same URL, same run, **proven `true` on that exact URL on 2026-11-27**.

**PRE-REGISTERED, NAMING THE FIELD AND THE PREMISE.** Adjudication is on `$.records[].find_matched` for the record whose `$.records[].find` is exactly `Role of Member States` **and** whose `$.records[].url` is exactly the published-view URL. **I pre-register TRUE.** The premise, stated so it can be falsified: that the navigation block containing that phrase is a site-wide element of `icsid.worldbank.org`, attested on `/cases/recent`, `/cases/pending`, `/cases/case-database`, `case-detail` and five `tables-of-decisions` paths. **A FALSE falsifies that premise for this document and DEFEATS the limb (d) conditional, which is the informative outcome; it must be read against the control, and a FALSE on the control makes the question row uninterpretable and is an instrument failure on that stream, not a finding about the view.** Note the find is case-insensitive over the whole tag-stripped body.

**What a TRUE licenses:** that at least one site-wide navigation element is served on both documents, which **narrows** the limb (d) residue from "the two documents may share no chrome at all" to "the two documents share this element". **What it does NOT license:** that they share the *whole* element set — no finite set of such rows can establish that, and the residue my windows cannot reach (the menu tail after `Database of Mem`) is untouched by it. **What a TRUE on one only would license** — and this is the asymmetry worth stating — **is decisive in the negative direction: the documents do not share that element, so Row 4's null cannot be transported to Row 6's page, and my limb (d) discharge fails on its stated conditional.** **The row is therefore worth firing for its FALSE branch, not its TRUE branch**, which is the honest accounting of it and the reason I rate it second.

### The row I rate higher, and why

**`https://icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/20/21`, `find "Status of Proceeding"`. One row. No companion control needed.**

**The warrant, every leg measured at `ff839bdc` and not taken from memory.** The `case-detail` path class holds **330 records in the tree, outcome `ok` on all 330, zero refused**; `find "Status of Proceeding"` has been fired on it **140 times and returned `find_matched true` 140 of 140** — so a null would itself be the finding and no control is required. **25 distinct designators have been fired on that path class and `ARB/20/21` is not among them**, so the row is novel. And the decisive distinction from the row you have reserved to Emory: **`ARB/22/8`'s designator reached this council ONLY through refused engine prose, which is why firing it is a judgement about `1124-C3`'s locator limb. `ARB/20/21`'s designator is attested in ICSID's OWN SERVED PROSE as of 2026-11-27, with a caption and a respondent State. Firing it adopts no engine word and routes around no escalation.**

**Why it is worth more.** Per `1127-C2`, `ARB/20/21` is a **live candidate** on the Iraq thread whose only ground of exclusion is one unsourced sentence. **One case-detail row is decisive either way.** If its `Latest Development` is a 2022 or 2023 disposition, **`ARB/20/21` is excluded on primary evidence, route (iii) closes properly, and my memo's overstatement is cured by measurement rather than by retraction.** If it is a mid-2026 development, **the amended closure condition's second conjunct becomes reachable by a shared date or disposition from a primary source** — which is the one thing this thread has never had. The chrome row, by contrast, settles a conditional inside an instrument finding. **I would spend the first slot on `ARB/20/21` and the second pair on the chrome row, in that order, and if only one slot exists I would spend it on `ARB/20/21`.**

**Pre-registration for it, naming the field:** adjudication on `$.records[].find_matched` for the record whose `find` is exactly `Status of Proceeding` and whose `unquote(url)` contains `CaseNo=ARB/20/21`. **I pre-register TRUE on 140-of-140 attestation. I pre-register NO value for the `Latest Development` string or the status value** — those are read at read time, per G21 limb (b), and I will not pre-register a conclusion that depends on what the window contains. **What a TRUE would NOT license: any pleaded asset, any pharmaceutical characterisation, and no join to any headline.** Only the register's own caption, status and `Latest Development` string, and `1124-C3` and `L263` bind on all three.

---

**END OF ANSWERS — RESEARCH ANALYST, 2026-11-27.**
