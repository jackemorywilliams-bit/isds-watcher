# Council Decision Session — 2026-08-03 — The Proposition Rule

**Convened** by the operator (Emory Williams) as a DECISION session with one deliverable: a
standing rule and procedure that prevents "the proposition problem" from recurring. Standing
instruction: a rule, not a discussion, and it must bind the way the earlier standing rules bind.

**Seats convened.** Two. A decision session, not a daily.

| Seat | Subagent | Model | Commission |
|---|---|---|---|
| Chairman | (presiding) | Claude Opus 5 | Direct, rule, record |
| Systems designer | `systems-designer` | `opus` | Design the procedure — PLAN AND RULE TEXT ONLY |
| Integrity officer | `integrity-officer` | `opus` | Phase 1 premise check + pre-stated criteria; Phase 2 adversarial vet. Objections bind |

The analyst, editor, systems researcher and analytics officer were not seated. Neither the design
nor the vetting required a sourced external development or a screened-item tie-in. Not a procedural
failure — a seat convenes when its queue has work only it can do.

**Scope discipline.** Nothing under `src/`, `scripts/`, `tests/`, `.github/`, `prompts/`,
`lit-review/` or `METHODOLOGY.md` was created or modified by any seat. No branch pushed, no PR
opened. This record is the whole artifact.

---

## Part 1 — The failure, and the premise the commission rested on

Dr. Benavides returned Emory's two literature-review memos with margin comments. Three of them were
corrections of the same kind. Each was verified against primary sources by the operator before this
session and is **operator-attested** — none of the three is checkable from repository state, for a
reason that turns out to matter (Part 2).

1. **H&H Enterprises v. Egypt (ICSID ARB/09/15)** — cited in the bibliography for the
   fork-in-the-road doctrine and for a trade-secret proposition. It is a resort management and
   operation dispute. The published Rule 48(4) award excerpts contain no occurrence of *trade
   secret*, *intellectual property*, *confidential information*, *know-how* or *patent*. The pin
   cite was to a Decision on Jurisdiction that expressly **joined** the fork-in-the-road objection
   to the merits rather than deciding it. Disposition mixed — three claims dismissed on the merits —
   and an annulment application was discontinued in 2016 for non-payment, so the award was neither
   annulled nor upheld. Two distinct failures in one entry.
2. **Vanda Pharmaceuticals v. FDA, 436 F. Supp. 3d 256 (D.D.C. 2020)** — cited as an FDA
   disclosure / Trade Secrets Act case. It is an Administrative Procedure Act challenge to a partial
   clinical hold, with no occurrence of *trade secret*, *confidential*, *proprietary* or *disclos*.
   The disclosure opinion he wanted exists **on the same docket**, dated 6 May 2021.
3. **Bonnitcha & Aisbett, "Against Balancing"** — annotated as "the strongest external critical
   perspective on the doctrinal architecture inside which Ferguson is working," meaning the
   recognition–enforceability gap. Whole-text counts: zero occurrences of *intellectual property*,
   *trade secret*, *patent*, *trademark*, *TRIPS*. Both occurrences of *recognition* concern
   recognition and enforcement of arbitral awards.

**The shape.** In each case a proposition was formed that is true or defensible on other authority,
and a source was then attached that was apt in **topic** but did not **contain** the proposition.
Verification stopped at *the source exists and is retrievable* and never reached *the source says
this*. Nothing here is fabricated. Every source is real, correctly cited, and retrievable. This is a
**recruitment** failure, and it is invisible to every check that asks whether a citation is genuine.

## Part 2 — Chairman's own verification, run before the commission went out

The rule I adopted at the close of the last session was: *verify what I assert first — the
chairman's premise is the first claim in the session, and it gets checked before the agenda goes
out, not at Part 5.* I applied it here, and it changed the commission.

**The premise I was given.** That both memos' §VII methodological notes already commit each entry to
a verification statement covering "(a) whether the source can be independently located; (b) whether
the citation format used matches the underlying source; and (c) whether the cited paragraphs support
the proposition for which they are used" — limb (c) being exactly the check that failed. On that
premise the diagnosis writes itself: the rule exists and was applied asymmetrically.

**What the repository actually contains.**

- `grep -rn "independently located"` — **zero hits repo-wide.** The three-limb text is not in
  repository state.
- `grep -rn "support the proposition"` — **one hit**, `lit-review/kim-memo.md:33`, and it is
  substantive prose about Kim's use of Philip Morris v. Uruguay, not a methodological limb.
- Both §VII sections are **stubs**. `lit-review/ferguson-memo.md:64` and `lit-review/kim-memo.md:65`
  are single italicized paragraphs promising that entries "follow the project's annotated-
  bibliography template (Bluebook + liberal URLs; ~80–200 word descriptive/evaluative annotations
  with a verification statement per entry)," naming the pedagogical sources for that template. **No
  limbs are stated and not one bibliography entry is present.**
- `grep -rin "H&H\|ARB/09/15"` — **zero hits.** `grep -rln "Bonnitcha\|Against Balancing"` — **zero
  hits.** `Vanda` appears in three files: both memos, and `alerts.yaml:47`, which is a correctly
  scoped Google Alerts watch feed carrying no proposition.

**What I inferred from that, and where I was wrong.** I sent both seats a correction reading: *the
limbs do not exist; the rule was never written down.* That inference was wrong, and the coordinating
session corrected me mid-session. **The limbs do exist** — in the document Dr. Benavides annotated,
which the operator supplied in chat and which is not in this repository. The annotated document
carries the full bibliographies and the methodological note; the repo's `lit-review/*.md` §VII
sections are stubs of it. The annotated document is the authoritative artifact for this session.

Verbatim, Ferguson §VII: "each entry contains a verification statement indicating (a) whether the
source can be independently located; (b) whether the citation format used **in Ferguson's article**
matches the underlying source; and (c) whether the cited paragraphs support the proposition for
which they are used." Kim §VII is identical but for "**in Kim's article**." Both strings are
**operator-attested from a document the council cannot open**, and are recorded as such.

**What survives the correction, and it is the finding that matters.** The repo-versus-document gap
is real and stands: the failing artifact — the annotated bibliography holding the H&H, Vanda and
Bonnitcha entries — **is not in this repository and never was.** It lives in a word processor,
outside every mechanical guard this project owns. Any rule that assumes a repo, a CLI, a ledger or
an agent is a rule aimed at the wrong document.

**And the diagnosis changes.** Read limb (b): "the citation format used **in Ferguson's article**" /
"**in Kim's article**." The verification statement was drafted to verify the citations *of the
article under review*. It never pointed at the citations Emory supplied himself. So this is **not a
rule he failed to follow. It is a rule whose stated scope excluded the population that failed** — a
scope defect in the drafting, not a discipline failure in the execution. That is a materially
different design target: one designs against inattention, the other against scope.

**I tested that reading against repository state before sending it to the seats, because an
exculpatory diagnosis is exactly the kind a council should distrust.** It holds, and the confirmation
is stronger than I expected. **All three failed citations are author-supplied additions, not
inherited from the article under review:**

- `lit-review/ferguson-memo.md:41` — Ferguson "doesn't mention Vanda Pharmaceuticals or the FDA
  Disclosure cases by name."
- `lit-review/kim-memo.md:22` — Kim, writing in 2016, "did not cover Vanda Pharmaceuticals v. FDA."
- H&H Enterprises and Bonnitcha & Aisbett return **zero hits repo-wide** and appear in neither
  memo's enumeration of the authors' authorities (Ferguson: Tethyan Copper, Saluka, Bayview,
  Landreau, Siag, Burlington, A11Y, Celgard, Matalia, Lemley; Kim: Apotex, Philip Morris v. Uruguay,
  Eli Lilly, the EMA/InterMune/AbbVie/PTC line, Malicorp v. Egypt).

> **CORRECTED LATER IN THIS SESSION — read R1 and R2 before relying on the two paragraphs above.**
> The integrity officer checked my method and it does not hold. `ferguson-memo.md:21` reads "just a
> handful of tribunals, **including** Tethyan Copper…" and `:28` reads "(Siag, Burlington, A11Y,
> **etc.**)" — I verified both after the objection. **Absence from an expressly non-exhaustive list
> proves nothing.** Only Vanda is *verified* author-supplied. H&H and Bonnitcha are *strongly
> indicated* on better grounds the officer supplied. The record reads **1 verified, 2 strongly
> indicated, 0 excluded** — not 3/3.
>
> And the scope-defect diagnosis itself is **overturned** at R1. The officer, reading the limb text,
> found limb (c) **unscoped**: for a source the article never cited there is no "citation format used
> in Ferguson's article," so if (b)'s scoping governed the whole sentence the verification statement
> would be inapplicable to every self-recruited entry while the same sentence demands that "each
> entry" carry one. Limb (c) reached these citations. **This is a discipline failure, with limb (b)'s
> scoping and the "Backsourced" heading as a drafting aggravator.** The two paragraphs above are kept
> as written because the chain of correction is the honest record of how this session reached its
> finding — three successive framings, each verified and each wrong in a different way.

**The outward application was real, and it worked** — which is why the scope defect is the whole
story rather than half of it. In §III.B and after, the same discipline is applied to the authors'
citations and catches real defects:

- `lit-review/ferguson-memo.md:28` — "I utilized the AI to systematically cross-reference
  **Ferguson's** footnotes against official digital archives to ensure the citations supported his
  specific legal arguments." That is limb (c), aimed outward, working. In the same paragraph, on his
  own bibliography: "the brief descriptions in the bibliography were checked against the actual
  **metadata and page numbers**" — limbs (a) and (b) only. The seam is visible in a single sentence.
- `lit-review/kim-memo.md:29` — items flagged where Kim "cited a case for a particular proposition
  while failing to tell the reader what the outcome was." The subject-and-disposition check,
  invented and applied to Kim.
- `lit-review/kim-memo.md:45` (§IV.E) — "the research project should perform its own verification of
  the procedural histories cited by Kim prior to accepting her characterization of each case."
- `lit-review/kim-memo.md:59` (§VI.B) — Kim's "most glaring weak point" is that she "cites a case to
  establish the proposition... however, in those same instances, she fails to advise the reader
  whether the decision was based upon the rationale cited."

The knowledge was never missing. Emory formulated the disposition check himself, named its absence
as a scholarly defect in another author's work, and recommended it as project policy — and the
verification statement he drafted pointed it at everyone's citations but his own.

- `lit-review/ferguson-memo.md:28` — "I utilized the AI to systematically cross-reference
  **Ferguson's** footnotes against official digital archives to ensure the citations supported his
  specific legal arguments." That is limb (c), aimed outward. In the same paragraph, on his own
  work: "This hybrid method ensured that the brief descriptions in the bibliography were checked
  against the actual **metadata and page numbers** found in these official repositories." Metadata
  and page numbers are limbs (a) and (b). Limb (c) is not claimed for the bibliography, and the
  sentence is the exact seam the three failures fell through.
- `lit-review/kim-memo.md:29` — items were flagged where Kim "cited a case for a particular
  proposition while failing to tell the reader what the outcome was." That is the
  subject-and-disposition check, invented and applied to Kim.
- `lit-review/kim-memo.md:45` (§IV.E) — "the research project should perform its own verification of
  the procedural histories cited by Kim prior to accepting her characterization of each case."
- `lit-review/kim-memo.md:59` (§VI.B) — Kim's "most glaring weak point" is that she "cites a case to
  establish the proposition... however, in those same instances, she fails to advise the reader
  whether the decision was based upon the rationale cited."

So the precise finding is worse than "a rule was applied asymmetrically," and better for designing
against. **The check that would have caught both H&H failures is a check Emory formulated himself,
named as a scholarly defect in another author's work, and recommended as project policy — in the
same memo whose own bibliography then failed it.** The knowledge was not missing. The direction of
application was.

**Two governance facts I verified because they answer the operator's hardest question.**

*First.* The two standing rules adopted this morning (commit `3d31de8`,
`analytics/council-sessions/2026-08-03-standing-rules.md`) are **not on `main`** — that record sits
on an unmerged worktree branch. Yet the rules themselves are on `main` and are operative:
`README.md:116` ("the standing rule is that the reduction travels, never the document"),
`scripts/fetch_relay.py:10` (the same rule, in the module docstring of the function that would
violate it), and `tests/test_source_not_read.py:11` (the source-status rule, in a test that goes
red). **The adoption record never landed and the rules bind anyway, because they were attached to
artifacts that fail.** Limb (c) had the opposite fate: it lived only in prose, in a section that is
a stub, attached to nothing that could break. That is the empirical answer to "what makes this rule
different from the one that already existed" — not emphasis, carrier.

*Second.* There is **no memo template file in this repository.** `templates/` holds
`digest.html.j2` and `research_brief.html.j2` only; no annotated-bibliography template exists
anywhere. The operator's instruction that the rule be liftable "into `prompts/` and the memo
template" therefore names one artifact that exists and one that must be created. That is an Emory
item, recorded in Part 7.

*Third.* The check already exists in this project's practice, performed correctly, with a name for
the failure mode. `analytics/methodology-citation-audit.md` (2026-06-29) audited all 21 authorities
in `METHODOLOGY.md`. Section A is limbs (a) and (b) — exists, cited accurately, field-by-field
against publisher and docket records. **Section B is limb (c)**, and it is titled "Spot-check of
substantive claims attached to load-bearing citations." Its verdict language is the vocabulary this
session needs: Paulsson is "**Supported, not a topical drive-by**"; Brown et al. is "exactly on
point, **not a stretch**"; and the summary at §C states that the substantive claims "are faithful to
their sources, **not topical filler**." The audit's seed-case bullet is the subject-and-disposition
check performed properly — Philip Morris inadmissible for abuse of right with the merits never
reached; Eli Lilly dismissed on the merits; Bridgestone resolved largely for claimants at the
expedited-objections stage with denial-of-justice and FET dismissed. That bullet is the exact form
that, applied to H&H, closes both halves of instance 1. **The council owns a working instance of
limb (c) and a name for its failure — "topical drive-by" — and neither has ever been made
standing.** The rule's job is to convert a one-off audit of one document into a per-entry
requirement on the writer.

**One live-thread observation.** `state/research_log.json` (seq 39) carries an open thread on the
China–Switzerland BIT (2009) forum-relationship mapping — *fork-in-the-road vs. no-U-turn*,
`GAP-UNRESOLVED` since 2026-07-31. H&H was recruited for fork-in-the-road. The council is actively
researching the doctrine that produced one half of instance 1, which bears directly on the scope
ruling in Part 6.

## Part 3 — Systems Designer's Return (verbatim)

*Delivered as its final report to the chairman as launcher, reproduced verbatim; headings demoted
for record nesting, text otherwise unedited. Rulings in Part 6.*

### Verifications the designer ran before writing

I confirm your Part 2 corrections independently: `grep -rn "independently located"` returns zero
repo-wide; `grep -rni "support the proposition"` returns exactly one hit, `lit-review/kim-memo.md:33`,
substantive prose about Philip Morris, not a limb; `grep -rni "H&H Enterprises\|ARB/09/15"` and
`grep -rni "bonnitcha\|Against Balancing"` return zero. Two small corrections to your Part 2, neither
of which changes the ruling. First, case-insensitively `Vanda` appears in **four** files, not three —
`state/seen.json:11` carries a lowercase `vanda` in a BioSpace press-release URL. `grep -c "Vanda"
state/seen.json` is 0; the capitalized form is what your count saw. A seen-URL carries no
proposition, so the conclusion holds. Second, and this one matters:

**Limb (c) is in repository state. It is in `HUMAN_REVIEW.md`, and it is aimed at the instrument,
not at the operator's own citations.** `HUMAN_REVIEW.md:49-51`, in the operator's own monthly
checkpoint procedure: *"The question is not whether the URL resolves — the assisted pass already
answered that — but whether the source **actually supports the claim**: the date, the holding, the
figure, the characterisation as stated. A URL that loads but does not say what the claim says is a
**FAIL**."* And `:31-33`: *"open the cited source(s) and check that the source exists, says what the
claim says... A claim with no openable source, or one the source does not support, is a **FAIL**."*

That is limb (c), written in operative form, committed, and running monthly. So your asymmetry
finding is not two instances, it is three, and the third is the most damning: **outward to Kim's
procedural histories (`kim-memo.md:29, 45, 59`), outward to Ferguson's footnotes
(`ferguson-memo.md:28`), and outward to the pipeline's own output (`HUMAN_REVIEW.md:49-51`) — never
inward to the citations Emory supplies.** The rule was not missing from the repository. It was
missing a direction. I designed against that, and it decides the enforcement section.

### 1. THE RULE

**THE CARRYING-SPAN RULE** — applies to every source cited for a proposition in a memo,
bibliography, or council record.

1. **Proposition first.** Before opening the source, write the one sentence you intend to cite it
   for. That sentence is what gets verified. If it changes, it is a new proposition and the rule
   restarts.
2. **Screen the whole text.** Search the retrieved document for the proposition's operative terms —
   at least three, one of them a term of art the field cannot paraphrase away, one a truncated stem.
   A zero is not a verdict; a nonzero is not a pass. Zero on a descriptive word: try its synonym. A
   hit: go read the hit.
3. **Quote the carrying span.** Put the words that carry it into the entry, with a pinpoint. A
   pinpoint alone is not compliance. If nothing carries it, take one exit and name it: narrow the
   proposition to the span, find another source, or drop it. If you cannot retrieve enough to look,
   the source is unread: say so and assert nothing from it.
4. **Cite the document, not the case.** Name the opinion, award or decision you read, and its date.
5. **Card every case:** what the dispute was about, the stage cited, how it came out **on the point
   you cite** — "joined to the merits" and "undecided" are outcomes — and what happened after.
6. **Annotation claims are propositions.** Any relational or superlative claim about a source —
   strongest, closest, most on point — needs its own span, or rewrite it as your judgement.
7. **Record the rejects.** List what you screened and did not use, and why.

*(248 words. Spine, in order: Proposition, Screen, Span, Document, Disposition, Annotation,
Rejects.)*

**The entry shape the rule produces**, four marks, so compliance is countable:

```
P — <the one sentence>
Q — "<span>" [pinpoint]
D — <document + date>; <dispute about>; <stage>; <outcome on this point>; <after>
V — checked <date> at <where retrieved>; screened <terms + counts>; <exit taken, if any>
```

This adds no field the memos have not already promised. `ferguson-memo.md:64` and `kim-memo.md:65`
both commit each entry to "a verification statement per entry." The rule states what that statement
must contain. `V` is the promised line; `P`/`Q`/`D` are what makes it checkable.

### 2. RULINGS

**(a) Proposition-first — ADOPTED, but it is NOT the load-bearing element, and the illustration
understates what it does.**

It is load-bearing in one specific respect that is worth separating from the rest: **it fixes the
object of verification.** Without a written proposition, "does the source support this?" has no
determinate referent, and the writer's memory of what he meant silently expands to fit whatever the
source turns out to say. That expansion *is* the recruitment mechanism. So step 1 is not a
discipline about sequence; it is the definition of the test that steps 2-3 then run.

**The load-bearing element is the carrying span** — the requirement that the source's own words,
transcribed into the entry with a pinpoint, contain the proposition. Two reasons, both from the
failures:

- The span requirement alone kills three of the four failures. In H&H (trade-secret half), Vanda,
  and Bonnitcha, the operative term does not occur anywhere in the document, so **no span could have
  been written.** Not "would have been hard to write" — could not exist.
- **A pinpoint alone would have caught none of them.** H&H had a pin cite. It was to a Decision on
  Jurisdiction that joined the objection to the merits. A pinpoint is a promise; a transcribed span
  is evidence. I therefore reject the "or pinpoint" half of your illustration: quotation is
  required, pinpoint alone is not compliance.

One replacement I am making to the mechanism as you framed it. A proposition about an *absence*
("the tribunal did not decide X") admits no carrying span by construction. Rather than exempt it,
step 3's exits handle it: you quote the disposition line that shows the non-decision — that is what
"joined to the merits" is, a quotable act — and if no such line exists, the source does not carry the
proposition and you take an exit.

**What decides this ruling in the rule's favour is the shape of the exits.** Under the old check the
cheapest escape from "the source exists" was to keep going. Under this rule the cheapest escape is
**narrow the proposition to what the span carries** — which is the honest exit. That satisfies the
integrity officer's standing criterion from the prior session (is the cheapest escape route also the
honest one). It is the strongest property this design has and it is why I would keep step 1 even
though step 1 is unenforceable.

**(b) The whole-text screen — ADOPTED as a router, never a verdict; the guard is the
rigid-designator test.**

The screen's status must be stated before its content: **it directs reading; it never substitutes
for it.** The guard has to be two-sided because both sides failed this session, on different
entries.

*The zero side — synonym blindness.* Your integrity officer's catch is the general case: `municipal
law` returns 0 in Bonnitcha, `domestic law` returns 5 and carries the proposition. A zero on a
*descriptive* term is worthless, because descriptive terms have synonyms. But a zero is not always
worthless, and the difference is mechanical:

> **A zero is reportable only when the screened set includes at least one rigid designator — a term
> of art with no synonym: a treaty or statute name (TRIPS, the Trade Secrets Act), an article number
> (Art. 39(3)), a doctrine's proper name ("fork in the road"), a party name — and at least one
> truncated stem.** A zero on descriptive words alone means "not found by this screen," which is not
> a finding about the source.

This is exactly the discrimination the three failures require. `trade secret`, `intellectual
property`, `patent`, `TRIPS` are rigid in this field — they do not have paraphrases a court uses
instead. Zero across five of them in H&H, and zero across four (including the stem `disclos`) in
Vanda, are near-decisive. `municipal law` is descriptive; its zero is noise. The rule as written
makes the distinction operable without asking the writer to know linguistics: *is there a name for
this thing that a court could not have avoided using?* Search that.

*The nonzero side — and this is the half your illustration omits.* H&H's fork-in-the-road entry
almost certainly screens nonzero: the Decision on Jurisdiction discusses the objection at length.
The term is there; the proposition is not, because the tribunal declined to decide it. **A hit is a
location, not a verdict.** The rule therefore says "go read the hit," and the only thing that
converts a hit into a citation is step 3's span. I flag this as the more dangerous side of the two,
because a nonzero count *feels* like confirmation in a way a zero does not.

I reject any version of the screen that produces a count written into the entry as a reason. The `V`
line records what you screened and what you read; the count is provenance, never justification.

**(c) Subject and disposition — ADOPTED, with two changes that are what actually catch the H&H and
Vanda failures.**

Your framing is case-level ("how it came out"). Case-level would have passed both. Two corrections:

**Point-level, not case-level.** H&H's case-level disposition is "mixed — three claims dismissed on
the merits." That is true, it is retrievable, and it licenses the citation. The point-level
disposition is *"the fork-in-the-road objection was joined to the merits and not decided at this
stage"* — which destroys it. **The disposition must be stated for the point you cite, not for the
case.** "Joined to the merits," "undecided," "assumed without deciding," "reserved" are
dispositions, and they are the ones that matter to a doctrinal citation.

**Document-level, not case-level.** This is what catches Vanda, and nothing in your illustration
reaches it. *Vanda v. FDA* the case contains the disclosure opinion Emory wanted. *436 F. Supp. 3d
256 (D.D.C. 2020)* the document is an APA challenge to a partial clinical hold. The failure is not
that the case was wrong; it is that **the case and the document were treated as the same object.**
Step 4 is a separate numbered item for that reason — it is the cheapest item in the rule and it is
the one that catches an entire failure on its own.

**Minimum form**, one `D` line, roughly 35-50 words, five slots in fixed order: *document and date ·
what the dispute was about, in the tribunal's own subject terms · the stage · the outcome on the
point cited · what happened after.* H&H's compliant `D` line reads:

> Decision on Jurisdiction (2010) and Rule 48(4) award excerpts; resort management and operation
> dispute; jurisdiction; fork-in-the-road objection **joined to the merits, not decided**; three
> claims later dismissed on the merits; annulment application discontinued 2016 for non-payment —
> award neither annulled nor upheld.

Writing that line is not possible while believing the entry is sound. That is the whole point of the
item.

For non-case sources there is no `D` line, and the work is done by step 6 instead — see below.

**A cheap contribution back to the 08-03 design.** Its `DISPOSITION_ADVERSE` lexicon (`dismissed`,
`declined jurisdiction`, `lacked jurisdiction`, `no violation`, `rejected the claim`) contains **no
token for a non-decision**. An objection joined to the merits produces no adverse token because
nothing was decided; the screen passes. If increment 5 ships, add `joined to the merits`, `not
decided`, `assumed without deciding`, `reserved`, `left open`. One list edit.

**(d) Determinism.**

Stated plainly, and the honest headline first: **three of the four failures fall to a purely
mechanical test, and one does not.** The mechanical test is "does the proposition's operative term
occur anywhere in the document." H&H (trade-secret half), Vanda, and Bonnitcha all fail it. H&H
(fork-in-the-road half) passes it, and is caught only by item 5, which is judgement-assisted. That
ratio is unusually favourable and I want it on the record before the table, because it means the
rule is not mostly exhortation — most of this failure class is reachable by Ctrl-F.

| Mechanical — a machine runs it without a model's cooperation, and a person runs it with Ctrl-F | Irreducibly judgement |
|---|---|
| Term counts over the retrieved document (step 2) | **Whether the span carries the proposition.** The entailment. This is the residue and it is the whole rule's load |
| Verbatim occurrence of the transcribed span back in the source — paste it into Ctrl-F, it hits or it does not (step 3) | Whether a zero means concept-absent or synonym-blind. The rigid-designator test *guides* this; it does not resolve it |
| **The span contains at least one screened operative term** — the one mechanical bridge from proposition to quote. Weak (a term is not a proposition), and it fails all three term-absent entries | Which disposition is the disposition *for the point cited* (step 5) |
| Presence of each mark `P`/`Q`/`D`/`V` in an entry; parity of mark count against entry count | Whether a relational or superlative annotation claim is fair (step 6) |
| `Q` contains a quotation-mark pair and a pinpoint token (`¶`, `at`, `p.`, `§`) | Whether the *narrowed* proposition still does the work the argument needed |
| Agreement between the cited reporter/date/docket and the caption and date printed on the retrieved document (step 4) — string comparison a person makes by eye | Finding the right source once the wrong one dies |
| Presence and non-emptiness of the reject list (step 7) | Whether the writer applied the rule at all rather than reconstructing the marks afterward |

**The sequence in step 1 is not in either column, because it is not checkable at all.** No artifact
records the order in which two sentences were written. I am not going to dress it up. Its value is
that it costs nothing and it changes the default; its enforcement is the shape of the artifact it
produces, not the sequence that produced it.

### 3. COMPOSITION WITH THE 2026-08-03 PRE-LEDGER VERIFICATION SYSTEM

**The seam, stated once.** That system binds `claim_created` events in an append-only ledger
produced by a program. This rule binds a document in a word processor. They do not overlap in
enforcement surface at any point. They overlap in exactly one object — the pairing of a proposition
with a quote — and **on that object the 08-03 design declares itself absent.** Its own §4 right
column: *"whether the submitted quote is the quote the reasoning actually rested on (it can quote A
and argue from B)."* Its own §7: *"Quote-versus-reasoning divergence. The system verifies the quote
submitted. It cannot verify that the argument rests on that quote."*

I confirmed the same hole in current code rather than taking the design's word for it:
`supporting_quote` occurs **exactly once** across `src/` and `scripts/` — `src/integrity_gate.py:126`,
where it is copied through — and `claim_text` is only hashed (`:117`) and copied (`:120`). Nothing
anywhere compares them. So the proposition problem is not a gap between the two designs; **it is the
08-03 design's declared residue, and this rule is the human-side procedure for it.**

| Rule step | 08-03 module | Relation |
|---|---|---|
| 3 — span located in the source | `src/quote_integrity.py` (`normalize`, `extract_text`, `locate`) | **COVERED for pipeline claims. Not re-specified.** My step supplies by hand exactly the object that module produces by machine. Same object, different substrate |
| 3 — span not truncated at a limitation | `truncation_verdict` / `continuation` | **COVERED and orthogonal.** Truncation is *the quote drops a limitation the source states*; carrying is *the source never states the proposition*. Two independent ways one quote fails. Neither check sees the other's failure |
| 5 — disposition | `disposition_quote` + `DISPOSITION_ADVERSE` screen + `claim_type` forcing | **PARTIAL.** Covered: that a disposition is stated and quote-backed. **New: point-level rather than case-level, and the non-decision class** — the adverse lexicon has no token for "joined to the merits," so H&H passes it |
| 4 — document, not case | none | **NEW.** In the pipeline this is free: `canonical_source_locator` makes two opinions on one docket two different URLs. A reporter citation with no URL has no such property. `scripts/check_citations.py` already routes URL-less bibliographic citations to `needs-human-check` and asserts nothing about them — **this rule is what the human then does.** That is the cleanest seam available and it needs no new code |
| 2 — whole-text screen | `src/prior_art.py` + `scripts/build_prior_art_index.py` | **SAME SHAPE, DIFFERENT CORPUS, NO OVERLAP.** Prior-art counts terms over the *repository* to test novelty. This screens terms over the *source* to test carrying. Nothing to reuse; nothing to duplicate |
| 1 — proposition fixed, and 3's carrying test | none | **NEW, and it is the declared residue above** |
| 6 — annotation claims | none | **NEW.** The 08-03 design's scope is `candidate_claims` JSON. Nothing in it binds annotation prose, which is where Bonnitcha failed — there was no pin cite to check |
| 7 — reject list | none | **NEW.** Nearest analogue is the recorded `--override-truncation` / `--distinct-claim` reason strings: a disposition that must be named rather than taken silently. Same idea, human substrate |

**One integration that costs nothing now and pays later.** The four marks map onto the ledger's
fields without translation: `P` → `claim_text`, `Q` → `supporting_quote`, `D` → `disposition_quote`
plus locator, `V` → the `precheck` provenance. If a bibliography proposition later becomes a project
claim, it submits without rework. I am not proposing any code for this; I am proposing that the
entry shape be chosen so the hand-off is free.

**What I am explicitly not doing:** re-specifying quote normalization, the continuation lexicon, the
two-block window, the dup-locator block, `verified_against_current_access`, or the prior-art index.
Those are ruled on in R3-R8 and this rule composes with them unchanged.

### 4. PER-ENTRY COST

| Step | Case entry | Article entry |
|---|---|---|
| 1 Proposition | 1 min | 1 min |
| 2 Screen | 2 | 2 |
| 3 Span + transcribe | 3 | 3 |
| 4 Document identity | 1 | — |
| 5 Case card | 4 typical; **10-15 when procedural history needs the docket** | — |
| 6 Annotation claims | 1, only when the annotation makes a relational claim | 1 |
| 7 Reject line | 1 | 1 |
| **Total** | **~12 min typical, ~20 with a docket chase** | **~7 min** |

A 25-entry bibliography with 12 cases: roughly **4 hours**, on top of the reading. That is real and I
am not going to shave it.

**Three properties that decide whether it survives a deadline, in order of importance.**

**It is bounded, and the limb it replaces was not.** `HUMAN_REVIEW.md:49-51` asks whether the source
"actually supports the claim." That is an open-ended reading task with no stopping rule — which is
precisely why it was abandoned under pressure. Steps 2 and 3 give it a stopping rule: you are done
when you have a span, or when a rigid-designator screen comes back empty. Boundedness is what makes
a check survive a deadline; brevity is not.

**The cost is front-loaded onto entries that survive.** All three failing entries die at step 2 —
about two minutes each, before any of the expensive steps. You pay the full twelve minutes only for
work that ends up in the deliverable. A rule that is cheap on the failure path and expensive on the
success path is the right shape; the reverse is what makes people stop.

**Complying is faster than faking.** Transcribing twenty words you are looking at is less work than
composing a plausible annotation from memory. This is the only part of the design that is
self-enforcing.

The expensive tail is item 5's "what happened after," and it is honestly expensive: H&H's
discontinued annulment is a docket lookup, not a document read. I would accept an explicit deferral
there — `V — procedural history after the award: not yet checked` — before I would accept the field
going silent. A named gap is scholarship; an absent one is the failure.

### 5. ENFORCEMENT SURFACE

Your Part 2 finding is the right frame and I am building the section on it: **the rules that bind in
this project bind because they are attached to an artifact that fails** — `README.md:116`,
`scripts/fetch_relay.py:10`, `tests/test_source_not_read.py:11`. Limb (c) lived in prose attached to
nothing that could break, and it broke.

**A word-processor document has no red build.** I cannot manufacture one, and I am not going to
describe something weaker as if I had. What I can do is rank what is available, honestly.

**Enforcement — real:**

1. **The span cannot be produced without opening the source at that place.** Transcription is the
   enforcement. It is not auditable *that* you read; it is not producible *without* having looked.
   This is the strongest mechanism in the design and it works in a word processor with no repo, no
   CLI, no agent.
2. **Missing-mark detection, countable by anyone.** An entry lacking `Q` is visibly incomplete to any
   reader — including Dr. Benavides, who is the person who caught this. Zero judgement required:
   count entries, count `V —`, compare. Ten seconds with Ctrl-F, no tooling.
3. **Span-in-source, on demand.** Any `Q` can be pasted back into the source's find field by anyone
   holding both. A span that does not hit is a fail with no argument available.

**Enforcement — weak:**

4. **The reject list.** A bibliography with 25 entries and zero rejected sources is a question the
   professor can ask. That is a signal, not a gate, and I will call it what it is. Its real value is
   different and better: it turns compliance into content. What you screened and discarded is
   scholarship, and it is the only part of this rule that produces something for the reader rather
   than merely costing the writer.

**Exhortation — and I will not dress these up:**

5. **The ordering in step 1.** No artifact records sequence. Free, valuable, unenforced, permanently
   unenforceable.
6. **Entailment.** Whether the span carries the proposition is checkable only by a reader. Every
   mechanical mark in this design is upstream of the one judgement that matters.

**Two ways to convert marks 1-3 into a real failure. Both need your sign-off; I built neither.**

- **Extend `HUMAN_REVIEW.md`'s scope from pipeline claims to the lit-review bibliography.** One
  paragraph, zero code, and it puts limb (c) in the one committed file that already states it
  operatively at `:49-51`. This is the cheapest item available and it directly corrects the
  asymmetry, because it aims the operator's own existing check inward. Against it: `HUMAN_REVIEW.md`
  is referenced by `scripts/review_prep.py` and `scripts/build_graph.py` and is guarded by **no
  test** — I checked. It is operator discipline with an assist script, not a fail-closed guard.
  Extending it makes the rule *recorded*, not *enforced*.
- **Commit an exported plain-text copy of the bibliography to `lit-review/` and validate the marks**
  in the `scripts/check_site_sync.py` idiom — entry count versus `V —` count, every `Q` carrying a
  quotation pair and a pinpoint token, every case entry carrying a `D`. That converts 2 and 3 into a
  red build. It costs a change of practice (the memo enters version control), not a change of
  architecture. Note the honest limit: the validator can count marks. It cannot check entailment, so
  a compliant-looking entry with a recruited span still passes green.

**Scope.** I recommend the rule bind any writing where Emory attaches a source to a proposition —
the memos, the bibliography, and the council's daily records — and not the pipeline, which the 08-03
system covers. The live thread you flagged (`state/research_log.json` seq 39, China–Switzerland
fork-in-the-road vs. no-U-turn, `GAP-UNRESOLVED` since 07-31) is the immediate case: the council is
researching the doctrine for which H&H was recruited, in records where step 5's point-level
disposition is exactly the check that was missing.

**The one thing I will not claim.** The enforcement surface for the failure that actually occurred
was Dr. Benavides's margin. It still is. This rule makes the target smaller; it does not remove her
from the loop, and any version of this record that implies otherwise is overclaiming.

### 6. WHAT THIS DOES NOT CLOSE, AT THE CLASS LEVEL

**Entailment.** A span can contain the proposition's terms and still not carry it. The rule moves
the failure from *topical aptness* to *span aptness* — a much narrower class, not an empty one.
Everything mechanical here is upstream of that judgement.

**Narrow in the entry, wide in the body.** The predicted successor failure, and I would bet on it.
Step 3's honest exit is to narrow the proposition to what the span carries — and nothing stops the
memo's body prose from arguing the original wide version. The bibliography comes out clean and the
argument overreaches. This is the 08-03 design's "quote-versus-reasoning divergence" reappearing one
level up, on a substrate no rule here binds.

**Annotation vagueness — the way I expect this rule to be complied with and defeated.** When a
source dies at step 2 under deadline, the cheap survival move is not fabrication. It is dilution:
"informs the doctrinal background" instead of "the strongest external critical perspective on the
doctrinal architecture." Vague is not false, so it passes every check in this design including the
reject list, because the entry survives. It is also not scholarship. I have no mechanism for this
and I do not think one exists short of a reader.

**Inaccessible and redacted sources.** A screen over a paywalled or redacted document returns a zero
that means nothing, and the rule's rigid-designator guard cannot tell that zero from a real one.
Ferguson's own memo already carries two such items (`ferguson-memo.md:28`): Tethyan Copper, where
paras [1283], [1288] and [1327]-[1330] are missing from the public italaw version, and the 2006
Falconer speech, absent from the UK archives. Step 3's unread exit buys honesty, not coverage. Same
hole the 08-03 design declared for `seeds/*.pdf`.

**Docket-history recruitment, one level down.** Step 5's "what happened after" is sourced from a
*different* document than the one you quoted, and the rule gives it no carrying span. H&H's
"discontinued in 2016 for non-payment" is exactly that shape. A writer can comply with the entire
rule and recruit at that one field.

**Superseded or overruled authority.** A span can carry the proposition in a decision later
reversed. Out of scope; item 5 touches it only for the document cited.

**The asymmetry itself.** Three instances are now in the record: outward to Kim's procedural
histories, outward to Ferguson's footnotes, outward to the pipeline at `HUMAN_REVIEW.md:49-51`. The
rule can require the inward check. It cannot make the inward check feel necessary, and the evidence
is that the knowledge was never the constraint. **What the rule does structurally is make the inward
check produce an artifact of the same kind Emory demanded from Kim** — a stated subject, a stated
disposition, a stated procedural history, in writing, per entry. That is a change of substrate, not
of motivation, and the distinction should not be blurred in the adoption record.

**Procedural note.** Nothing was created or modified under `src/`, `scripts/`, `tests/`, `.github/`,
`prompts/`, `lit-review/`, or `METHODOLOGY.md`, and nothing was committed.

## Part 4 — Integrity Officer, Phase 1 (verbatim)

*Phase 1 ran before the officer saw the design, so its criteria are pre-stated rather than
reverse-engineered from the proposal. Reproduced verbatim; headings demoted, text otherwise
unedited. **Note for the reader:** the chairman's mid-session correction — that the three limbs
exist in the operator-supplied annotated document — reached this seat late, so §1(a) and §3(v)
below reason from the superseded premise that the limbs exist in no artifact. The repository facts
they report are correct and independently confirmed; the inference drawn in §3(v) is re-run in
Phase 2 and ruled on in Part 6.*

### 1. FACTUAL PREDICATES

Every line below was run from `/Users/emorywilliams/isds-watcher/.claude/worktrees/agent-a5537b81f77583583`
(HEAD `851d63c` = `origin/main`).

**(a) The chairman's premise correction: VERIFIED. He is not wrong.**

| Check | Command | Result |
|---|---|---|
| Three-limb text | `grep -rIn "independently located" . --exclude-dir=.git` | **2 hits, both inside `analytics/council-sessions/2026-08-03-proposition-rule.md` (:63, :70)** — i.e. the chairman's own quotation of the premise and his own refutation of it. **Zero elsewhere.** |
| Limb (c) phrase | `grep -rIic "support the proposition for which" .` | **0 repo-wide.** |
| "support the proposition" | `grep -rIn` | **1 hit**, `lit-review/kim-memo.md:33`, substantive prose on Kim's use of *Philip Morris v. Uruguay*. Not a limb. |
| §VII stubs | Read | Confirmed. `lit-review/ferguson-memo.md:64` and `lit-review/kim-memo.md:65` are each **a single italicized paragraph**. No limbs stated. **Zero bibliography entries in either file.** |
| Ever otherwise? | `git log -- lit-review/` → 2 commits (`aa11338` 2026-06-29, `b87c838` 2026-07-18); `git show aa11338:lit-review/ferguson-memo.md` §VII | **§VII has been a one-paragraph stub in every committed version.** The three-limb text was never in repository history either. |

**The premise correction stands, and it is stronger than stated: not "absent from repository state"
but "absent from repository history."**

**(b) The three failing sources: absence from the repo CONFIRMED; the failures themselves are
OPERATOR-ATTESTED, not verified.**

- `grep -rIiln "H&H Enterprises\|ARB/09/15"` → **0 files.**
- `grep -rIiln "bonnitcha\|aisbett"` → **0 files.** `grep -rIiln "against balancing"` → **0 files.**
- `grep -rIiln "vanda"` → **4 files**, not three. `alerts.yaml:47` (a Google Alerts feed URL),
  `lit-review/ferguson-memo.md:41`, `lit-review/kim-memo.md:22/:45/:62`, and — **the chairman missed
  this one** — `state/seen.json`, one occurrence, a biospace.com investor-summit press release in the
  dedup cache. **Immaterial: it carries no proposition.** Reported because he asked to be checked.

**Marked operator-attested, not verified, and I will not treat any of it as established:** the
margin comments; that H&H is a resort-management dispute; the zero term-counts in the H&H Rule 48(4)
excerpts, in *Vanda* 436 F. Supp. 3d 256, and in Bonnitcha & Aisbett; that the pin cite was to a
Decision on Jurisdiction that joined the fork-in-the-road objection; the mixed disposition and the
2016 annulment discontinuance; the 6 May 2021 opinion on the same docket; the "municipal" 0 /
"domestic" 5 counts in Bonnitcha. **None of it is checkable here.** The failing artifact is not in
this repository and never was — I confirm that independently.

**(c) Three predicates the framing does not state, all verified, all load-bearing.**

**(c1) The project's own deterministic citation machinery has no proposition concept at all.**
`grep -c -i "proposition"` → `scripts/verify_citations.py` **0**, `scripts/check_citations.py` **0**,
`src/integrity_gate.py` **0**, `scripts/verify.py` **0**. `verify_citations.py`'s docstring: it
"extracts every http(s) URL from a memo/brief and actually fetches each one, classifying it by what
the network says." `check_citations.py` records non-URL bibliographic citations "unjudged, as
``needs-human-check`` — never asserting existence it cannot confirm." **The tooling stops at
exists-and-is-retrievable by design.** The habit under remedy is not merely Emory's; it is the shape
of every citation check this project owns.

**(c2) A competing annotated-bibliography standard already exists, and it would not have caught any
of the three.** `METHODOLOGY.md:55-56`, "The Reporting Standard — The Digest as Annotated
Bibliography," requires per entry: citation, 50-200 word descriptive-and-evaluative annotation,
relevance assessment, link-back, access limitations noted, and "**at least one direct verbatim quote
from it**." A real verbatim quote from the H&H award excerpts, from *Vanda* 2020, or from Bonnitcha
satisfies that requirement completely and carries none of the three propositions. **The nearest
existing rule permits the exact failure.** Any new rule must either amend `METHODOLOGY.md:56` or
explain why the project now has two annotated-bibliography standards.

**(c3) No bibliography template exists.** `ls templates/` → `digest.html.j2`,
`research_brief.html.j2`. Confirms the chairman's Part 2 finding.

**(d) Nothing is false in the framing. One thing in it cannot be checked and should not be
asserted.**

The commission says the rule it replaces "was abandoned under time pressure." `grep -rIn "time
pressure"` → **0.** Repository state shows only that §VII has been a stub since 2026-06-29 and that
no entry was ever committed. **Abandoned-under-pressure, never-started, and written-elsewhere are
indistinguishable from here.** This matters for the cost criterion below: if the rule was never
started rather than abandoned, a per-entry time budget is being fitted to a failure mode that has no
measured cost.

### 2. THE ASYMMETRY READING — CORRECT, AND OVERSTATED IN ONE RESPECT THAT CHANGES THE DESIGN

**Supported, in the memos' own words.** Five lines, quoted:

- `ferguson-memo.md:28`, outward: "I utilized the AI to systematically cross-reference Ferguson's
  footnotes against official digital archives **to ensure the citations supported his specific legal
  arguments**."
- `ferguson-memo.md:28`, same paragraph, inward: "This hybrid method ensured that the brief
  descriptions in the bibliography were checked against the **actual metadata and page numbers**
  found in these official repositories."
- `ferguson-memo.md:48`: "nor does he adequately show that the case law cited in support of his
  contention **supports those claims based on holdings rather than mere dicta**."
- `ferguson-memo.md:58`: "the reference to Aplin et al. **provides some support for the
  proposition**, and the UK breach-of-confidence analogy found in footnote 114 is likely providing
  **more rhetorical than legal force**."
- `kim-memo.md:59`: Kim "cites a case to establish the proposition… however, in those same
  instances, she fails to advise the reader whether the decision was **based upon the rationale
  cited by Kim**… or whether the court determined the issue **on a narrower ground that would be
  inconsistent with her argument**."

The seam is inside one paragraph, on one corpus, at two stages. **The reading holds.**

**Three sharpenings, all repo-verifiable.**

1. **The inward failure is not non-retrieval.** `ferguson-memo.md:28` also states "I manually
   verified these references by **retrieving the full texts** directly from the professional
   databases." Retrieval is claimed. Any rule whose operative demand is "retrieve the source" adds
   nothing to what was already asserted.
2. **All three failing sources are self-recruited, not author-cited.** H&H appears in neither memo's
   list of Ferguson's or Kim's authorities. *Vanda* is named in both memos **specifically as a case
   the authors did not cite** — `ferguson-memo.md:41` ("He also doesn't mention Vanda Pharmaceuticals
   or the FDA Disclosure cases by name"), `kim-memo.md:22` ("Because Kim wrote in 2016, her work did
   not cover Vanda"). Bonnitcha is external by construction. **The sharper line is not
   outward-vs-inward on one corpus; it is author-cited vs self-recruited.** That is a more designable
   boundary and the chairman should have it.
3. **Where the reading is overstated: "limb (c)" bundles two different checks, and Emory only ever
   formulated one of them.** What he wrote outward is a *ground-of-decision* check — holdings vs
   dicta, narrower ground, undisclosed outcome. That check maps onto **H&H's fork-in-the-road use and
   nothing else in the set.** *Vanda* and Bonnitcha are a cruder failure: the source does not contain
   the **subject matter**, which is not a holdings-vs-dicta question and which Emory never formulated
   in either direction. **So the knowledge was not entirely present-but-misdirected.** For one of the
   four uses it was present and aimed outward; for the other three it was not formulated at all. A
   design built on "he already knew this check, just point it inward" will be correctly scoped for 1
   of 4 and under-scoped for 3.

### 3. PRE-STATED ADVERSARIAL CRITERIA — Phase 2 is a measurement against exactly these

**(i) REPLAY. The rule must be walked against four uses, not three instances. I score them now.**

Candidate rule of this shape = *proposition-first*: state the proposition; locate in the retrieved
source the text that contains it; record locator + verbatim span; only then admit the citation.

| # | Use | What the writer does under the rule | Where the error surfaces | Verdict |
|---|---|---|---|---|
| 1a | H&H, trade-secret proposition | Opens Rule 48(4) excerpts, searches the proposition's own subject-matter noun | **LOCATE step, zero hits.** Deterministic given the text in hand | **CAUGHT** |
| 1b | H&H, fork-in-the-road proposition | Opens the Decision on Jurisdiction, searches "fork in the road" — **the term is present**, the objection was raised. Finds the passage, quotes it, records the pin cite | **NOT surfaced.** The span exists and is accurately quoted. Only a second step asking what the tribunal *did* with it — decided / joined / deferred — reaches it | **NOT CAUGHT** |
| 2 | *Vanda* 2020 | Opens 436 F. Supp. 3d 256, searches trade secret / confidential / proprietary / disclos | **LOCATE step, zero hits** | **CAUGHT** — but see below |
| 3a | Bonnitcha, IP subject-matter | Searches IP / trade secret / patent / TRIPS | **LOCATE, zero hits** | **CAUGHT** |
| 3b | Bonnitcha, recognition–enforceability annotation | Searches "recognition" — **returns 2, both about recognition and enforcement of arbitral awards** | **NOT surfaced. Actively inverted:** the screen returns confirmation | **CATASTROPHIC PASS** |

**Stated in advance, so it cannot be claimed later:** a proposition-containment rule catches **3 of 5
uses**, misses 1b entirely, and on 3b **manufactures false support**. I will require the design to
walk 1b and 3b by name.

Two further pre-commitments on replay:

- **On 2 (*Vanda*):** the citation `436 F. Supp. 3d 256 (D.D.C. 2020)` is real, correctly formatted,
  and correct for the case named. **Every citation-validity check in this repo passes it.** And the
  correct authority is on the same docket, 6 May 2021. So the rule must specify the remedy branch:
  *drop the source* and *move the pin cite* are different outcomes, and the cheap one (drop) loses
  the right case. If the rule does not name the "same source, wrong opinion/paragraph" branch, I will
  flag it as producing avoidable source loss.
- **On 1b:** the check that catches it is the one Emory wrote at `kim-memo.md:59` and
  `ferguson-memo.md:48`. It is **not** limb (c). If the design covers only containment and the cover
  memo says the three instances are handled, that is the OVERREACH flag and I will file it.

**(ii) THE FOURTH CLASS. Not two classes. THREE. One rule should cover them only under a stated
condition.**

The B1/*Loewen* truncation is documented at
`analytics/council-sessions/2026-08-03-verification-system.md:36`: a quote "cut at a grammatically
complete point, discarding the clause confining the holding," which "was **character-exact as far as
it went**. Substring verification would have PASSED it."

They are **not** the same failure class:

| | Proposition problem | Truncation (B1) | Status (H&H-1b) |
|---|---|---|---|
| Failing operation | **Selection** — wrong source recruited | **Extraction** — right passage, wrong boundary | **Attribution** — right passage, wrong legal weight |
| Detection reads | proposition ↔ source content | span ↔ its own continuation | span ↔ the tribunal's operative act |
| Needs the proposition? | Yes | **No** | Yes |
| Needs a span boundary? | No | **Yes** | No |

A truncation check needs no proposition; a proposition check needs no boundary. They read different
objects and only share a precondition: **the source text must be in hand at the moment of citation.**

**My test:** one rule may cover both **if and only if its unit is "the located span inside the
retrieved source"** and it produces, per entry, *both* a recorded span boundary *and* a recorded
relation to the proposition. If the rule's unit is "the citation," truncation will be bolted on and
will be wrong. If the rule produces only one of the two artifacts, it covers one class and must say
which.

**And the third class must be handled or explicitly disclaimed.** Between "wrong source" and "right
source, cut wrong" sits "right source, right passage, wrong status" — joined to the merits, dicta,
dissent, argument of counsel, vacated, superseded. That is H&H-1b, it is the *Hela Schwarz* class,
and it is the class with the worst outcome history in this project.

**(iii) SYNONYM BLINDNESS. Four tests. A screen failing any of them is a source-discarding machine
or a false-confirmation machine.**

Repo-side corroboration of the vocabulary gap: `ferguson-memo.md` contains "municipal" **1** time
(`:35`, twice in the sentence pair carrying the recognition–enforceability gap) and "domestic" **0**
times. The memo's own term for the proposition is the term the source (attested) does not use.

- **(A) NON-DISCARDING.** A zero count on the writer's chosen term may **never by itself** license
  discarding the source. Zero routes to a widened retry against a **pre-committed** synonym set
  (municipal / domestic / national / internal law; trade secret / confidential information /
  know-how / undisclosed information / proprietary information). Only a zero across the full set is
  reportable, and reportable **only** as "not located under terms T" — never as "the source does not
  contain the proposition."
- **(B) NON-CONFIRMING — the converse, and the more dangerous one.** A nonzero count may **never by
  itself** license the citation. Bonnitcha's two "recognition" hits are the proof: nonzero,
  homonymous, and pointing at award enforcement. The rule must require that at least one located
  occurrence be read in context and **its referent recorded in the entry in the writer's own words**.
  If an entry can be completed without a recorded referent, the screen manufactures support.
- **(C) COST ASYMMETRY, correctly oriented.** A false zero costs a discarded good source —
  recoverable and visible. A false nonzero costs a false citation — unrecoverable and invisible.
  **Any design that hard-blocks on zero and passes silently on nonzero has the asymmetry backwards,
  and I will reject it on that ground alone.**
- **(D) NO SELF-DERIVED VOCABULARY.** If the same writer authors the proposition, picks the terms,
  reads the span and rules it sufficient, the screen verifies self-consistency. Either the term set
  is committed in advance in a project vocabulary file, or the entry records that the writer
  generated it — a weaker verdict that must be labelled as such. **The recorded verdict must always
  name the terms searched**, or the zero is uninterpretable by anyone later.

**(iv) COST UNDER PRESSURE.**

**Budget: 10 minutes per entry**, above what source retrieval already costs, for a source already in
hand and text-searchable. **Above 10 minutes per entry I will judge the rule non-viable and say so.**

Basis, so the chairman can dispute the number rather than the principle: `kim-memo.md:65` enumerates
~11 named authorities to add; `ferguson-memo.md:64` enumerates none but §II.B/§III.B name at least
14. Call the two bibliographies ~25 entries. At 10 min → ~4 hours across both memos, one sitting,
survivable. At 30 min → 12+ hours, which is the cost profile of the thing that gets abandoned.

**Hard constraint on the rule's wording:** every per-entry step must be **bounded** — cost scaling
with the entry count, never with the source's length. "Read the award" is unbounded and will be
abandoned. "Locate the term, read the surrounding two paragraphs, record the referent" is bounded. I
will reject any step written in unbounded form.

**Detecting abandonment after the fact — three detectors, and one disqualifier:**

1. **Entry-count parity.** Entries present vs entries carrying a completed record. Any gap is
   abandonment, countable without reading a word.
2. **Degenerate uniformity.** Recorded spans/referents that are identical, near-identical, or
   template-shaped across different sources. This is the performed-not-executed signature.
3. **Terminal thinning.** Require entries recorded in completion order; abandonment shows as the last
   N thinner than the first N.

**Disqualifier:** if the rule can be satisfied by an entry reading "verified" with no locator, no
span, and no term set, **there is no abandonment detector at all** — compliance and abandonment
produce byte-identical artifacts. I will treat that as fatal, not as a weakness.

**(v) THE HARD ONE — a rule existed and did not bind.**

**First, correct the question.** On repository evidence the three-limb rule **did not exist in any
artifact**. What existed was (i) a stub promising "a verification statement per entry"
(`ferguson-memo.md:64`, `kim-memo.md:65`), (ii) an outward-facing ground-of-decision check in prose
(`ferguson-memo.md:28/:48`, `kim-memo.md:29/:45/:59`), and (iii) `METHODOLOGY.md:56`, which governs a
**different artifact** and permits the failure. **The remedy for disobedience is enforcement; the
remedy for a missing carrier is a carrier.** These are not the same design.

**The empirical answer is already in the repo, and I verified it independently of the chairman.**
`git ls-tree --name-only origin/main -- analytics/council-sessions/` returns **one file**,
`2026-08-03-verification-system.md`. The standing-rules adoption record is **not on main**. Yet both
rules adopted that morning are operative, because each is attached to an artifact that can fail:
`README.md:116` ("The standing rule is that the reduction travels, never the document"),
`scripts/fetch_relay.py:10` (the same rule in the docstring of the function that would violate it),
`tests/test_source_not_read.py:11` (in a test that goes red). All three files confirmed present on
`origin/main`. **The adoption record never landed and the rules bind anyway. Limb (c) lived in
prose, in a section that is a stub, attached to nothing that could fail.** Carrier, not emphasis.
Confirmed.

**Four conditions. A rule missing any one of them is written down, not binding.**

- **C1 — CARRIER.** The rule is written into the artifact whose production it constrains, at the
  point of production. Not a session record; not a memo section that is a promise. **Say the
  consequence honestly:** the artifact here is a bibliography entry in a word processor, outside
  every mechanical guard this project owns, and no bibliography template exists (`templates/` = two
  Jinja files). The carrier must be **created**, and a carrier created inside this repo constrains
  nothing until a memo is actually produced from it. A design that quietly relocates the rule to a
  repo file it can enforce has changed the subject.
- **C2 — FAILURE SHAPE.** There is a state of the artifact that is visibly **wrong**, not merely
  incomplete. Minimum: a blank field. Better: a field that **cannot be filled without the source
  open** — a verbatim span plus a locator. That is the field a writer cannot complete from memory,
  from a title, or from a search-result snippet.
- **C3 — THE CHEAPEST PATH IS THE HONEST PATH.** The test I pre-stated on 2026-08-03 and hold to:
  *what does the writer do when this fires, and is the cheapest escape also the honest one?* Here the
  cheapest dishonest escape is specific and obvious — **paste a real verbatim quote from the source
  that does not carry the proposition.** That is precisely what `METHODOLOGY.md:56` already permits,
  and precisely why it would have caught none of the three. **The rule must bind the quote to the
  proposition, not merely to the source.** If it does not, it is `METHODOLOGY.md:56` with a new name.
- **C4 — DETECTABLE BY SOMEONE OTHER THAN THE AUTHOR, WITHOUT RE-READING THE SOURCE.** If Dr.
  Benavides is the only detector, nothing has changed — she was already the detector; that is how
  these three were found.

**Evidence that distinguishes a rule that binds from one written more emphatically.** I will ask for
exactly this in Phase 2 and, absent it, will record the rule as unvalidated rather than
adopted-and-working:

- **At least one entry in the next bibliography where the rule FIRED and the output CHANGED** — a
  source dropped, a pin cite moved (the *Vanda* 2021 branch), or a proposition rehomed. **A rule that
  has never changed an output has not been tested; it has been complied with in appearance.**
- The entry-count parity number, reported.
- Override/exception count, if the rule has an escape hatch — and if it has none, the count of
  entries silently omitted from the bibliography, which is the escape hatch a rule without one
  creates.

**The failure mode, named for the record: VERIFICATION-STATEMENT-AS-PERFORMANCE.** A per-entry
statement written to look compliant. Signature: (i) it asserts a conclusion ("supports the
proposition for which it is cited") without exhibiting the evidence that produced it — no span, no
locator, no term set; (ii) it is uniform across entries; (iii) **it is composable by someone who
never opened the source.** The operative test is (iii): *can this verification statement be written
from the memo alone?* If yes, it is a performance. I am adding this to the taxonomy now; it is the
citation-side twin of *snippet-as-fact*.

**And the base rate the new rule has to beat, which I raise because it cuts against this session's
purpose.** The previous decision session, earlier today, ruled the taxonomy sync "increment 0 and it
is adopted" and called it the cheapest mechanical win available. `git log -- agents/integrity-officer.md`
→ last modified **2026-07-31** (`07ff434`), nothing since. That file's Self-training mandate at
**`:109-111` still enumerates FIVE patterns**; its own taxonomy section at **`:60-80` enumerates
TEN**; the session record says the record holds thirteen. **My instantiated system prompt this
session carries the five.** So the council's most recently adopted, cheapest, most
emphatically-ruled rule has not bound within the same day, in the single file it names, in a
repository where I can check it with one command. **Any design that does not confront that number is
arguing against a weaker version of this problem than the one the council actually has.**

### 4. THE RESIDUE — what any rule of this shape will miss

1. **TRUE-BUT-NOW-UNSOURCED.** All three propositions are, per the operator, true or defensible on
   other authority. A containment rule removes the wrong support and leaves a correct sentence
   carrying **no** authority — and nothing flags that state. **Worse than a wrong citation, because a
   wrong citation is at least checkable.** If the rule does not force an explicit branch (rehome /
   downgrade / drop the sentence), this is where the failures migrate.
2. **APT-BUT-NOT-AUTHORITY.** The rule verifies containment, not authoritativeness. A blog post
   containing the sentence passes. Emory diagnosed exactly this in Ferguson at `ferguson-memo.md:58`
   ("more rhetorical than legal force"); containment is blind to it.
3. **STATUS.** Joined-to-merits, dicta, dissent, argument of counsel, vacated, superseded — H&H-1b,
   the *Hela Schwarz* class. Unless explicitly designed for, and if it is claimed as covered I will
   file it as OVERREACH.
4. **AGGREGATION.** A proposition supported by no single span but by synthesis across three passages.
   Under a span-per-proposition rule this either fails honestly or gets satisfied by whichever span
   is nearest — **manufacturing a false pin cite**. I expect the latter and will look for it.
5. **THE ANNOTATION, AS DISTINCT FROM THE CITATION.** Bonnitcha's failure lives in a characterization
   of the source **as a whole** ("the strongest external critical perspective on the doctrinal
   architecture inside which Ferguson is working"). **No span-level check reaches a whole-source
   characterization.** This is the purest instance in the set and the one I expect the design to miss
   most completely.
6. **SELF-JUDGED SUFFICIENCY.** One author writes the proposition, picks the terms, reads the span,
   and rules it sufficient. Every step is self-consistency. The only structural breaks available are
   a second reader or a pre-committed vocabulary; nothing else in this project's reach touches it.
7. **THE ARTIFACT IS OUTSIDE THE REPO.** Verified: the bibliography is not here and never was; no
   bibliography template exists. **Every mechanism this project owns fires on commit.** A rule aimed
   at a word-processor document is enforced by the author against himself — the same enforcement that
   produced these three. **I will not accept a design that elides this, and I will not accept
   relocating the rule to an artifact the repo can reach and calling that the same rule.**
8. **ADJACENCY SUBSTITUTION — hypothesis, explicitly unverified, recorded not asserted.**
   `kim-memo.md:65` lists "the *Malicorp v. Egypt* investment-definition language" among entries to
   add. *Malicorp v. Egypt* and *H&H Enterprises v. Egypt* are both ICSID Egypt cases. Whether one
   was substituted for the other **cannot be verified from repository state and I do not assert it.**
   I record it only because if that is what happened, the error occurred at retrieval, **before the
   proposition was written**, and no proposition-first rule reaches backward to it.

### Taxonomy extension (officer's self-training mandate)

- **source-apt-in-topic-not-in-content** — the proposition problem itself; a real, correctly-cited,
  retrievable source attached to a proposition it does not contain. Countermeasure: locate the
  proposition inside the source before admitting the citation; record the span.
- **deferred-ruling-as-holding** — a tribunal's joinder, deferral, or refusal to decide read and
  cited as a decision. Distinct from *inverted dispositions*: not a reversed outcome, a **non**-
  outcome. Countermeasure: record what the tribunal did with the objection, not that the objection
  appears.
- **homonym-hit-as-confirmation** — a nonzero term count read as proposition support where the
  occurrences carry a different referent (Bonnitcha, "recognition"). Countermeasure: record the
  referent of at least one located occurrence, in the writer's own words.
- **synonym-zero-as-refutation** — a zero count on the writer's chosen term read as the source not
  containing the proposition ("municipal" 0 / "domestic" 5). Countermeasure: pre-committed synonym
  set; report as "not located under terms T", never as absence.
- **near-docket substitution** — right case, wrong opinion, correct reporter citation; the authority
  sought sits on the same docket at a different date (*Vanda* 2020 vs 6 May 2021). Countermeasure:
  before dropping, check the docket.
- **verification-statement-as-performance** — a compliance statement composable without opening the
  source. Countermeasure: require the evidence, not the conclusion; test by asking whether the
  statement could be written from the memo alone.

**Nothing was written or modified.** Holding for Phase 2.

## Part 5 — Chairman's verification of the members' assertions

Standing rule, adopted 2026-08-03: *an objection asserting absence from or presence in the record is
verified by grep before ruling.* Applied to both seats. Six checks; all six confirm.

**1. The designer's third instance — CONFIRMED, and it is the most important finding either seat
produced.** `HUMAN_REVIEW.md:49-51`, in the operator's own monthly checkpoint: *"The question is not
whether the URL resolves — the assisted pass already answered that — but whether the source actually
supports the claim: the date, the holding, the figure, the characterisation as stated. A URL that
loads but does not say what the claim says is a FAIL."* And `:31-33`: *"open the cited source(s) and
check that the source exists, says what the claim says... A claim with no openable source, or one the
source does not support, is a FAIL."* That is limb (c), in operative committed form, aimed at the
pipeline's output. So the direction of application has three recorded instances, not two: outward to
Kim, outward to Ferguson, outward to the instrument — and never inward.

**2. The designer's code finding — CONFIRMED.** `grep -rn "supporting_quote" src/ scripts/` returns
exactly one line, `src/integrity_gate.py:126`, where the field is copied into the gated claim record.
`claim_text` at `:117` is passed to `verify.claim_id()` and at `:120` copied. **Nothing in the
codebase compares a quote to the claim it supports.** The proposition problem is therefore not a gap
between two designs; it is the 08-03 system's own declared residue, and this rule is its human-side
counterpart. The designer's composition claim is sound.

**3. The officer's (c1) — CONFIRMED.** `grep -ci "proposition"` returns **0** in all four of
`scripts/verify_citations.py`, `scripts/check_citations.py`, `src/integrity_gate.py`, and
`scripts/verify.py`. `scripts/check_citations.py:60` defines `NEEDS_HUMAN = "needs-human-check"` for
a "bibliographic citation w/ no URL, or URL unresolvable." The officer's characterization is exact:
**every citation check this project owns stops at exists-and-is-retrievable, by design.** The habit
under remedy is the instrument's habit as much as the operator's.

**4. The officer's (c2) — CONFIRMED, and worse than stated.** `METHODOLOGY.md` §VII, "The Reporting
Standard — The Digest as Annotated Bibliography," requires per entry that "Each links back to the
originating document and **includes at least one direct verbatim quote from it, giving the reader
enough to find the source without additional searching.**" The stated purpose of the verbatim-quote
requirement is **findability, not proposition support.** A real quote from the H&H excerpts, from
*Vanda* 2020, or from Bonnitcha satisfies it completely and carries none of the three propositions.
The nearest existing rule in the project does not merely fail to catch the failure — it is aimed at a
different problem entirely. One correction to the officer: §VII governs **the digest**, the
instrument's weekly output, not the lit-review memos, which use a separate CUNY/Columbia/Johnson-
grounded template. So this is not two competing standards for one artifact; it is two artifacts,
each with an annotated-bibliography standard, and **neither carries a proposition-support requirement
in operative form.** The exposure is wider than the officer stated, not narrower.

**5. The officer's base-rate challenge — CONFIRMED, and it is the most serious thing in this
session.** `git log -1 -- agents/integrity-officer.md` returns `07ff434`, **2026-07-31**, and its
subject is a vault-wide managed-block regeneration — not a taxonomy change. The file's taxonomy
section is headed "**Fabrication taxonomy — extended to ten**" and enumerates ten. Its **Self-training
mandate** further down still reads: *"Maintain a running taxonomy of fabrication patterns caught in
this project (unsourced precision, inverted dispositions, snippet-as-fact, title-as-holding,
memory-file reconstruction)"* — **five**. The officer reports its instantiated system prompt carried
the five. This morning's session ruled taxonomy sync "increment 0 ... the cheapest mechanical win in
the session" and it has not bound, within the same day, in the single file it names. **I accept this
as the governing base rate for anything adopted today**, and it changes what I am willing to call
adopted (Part 6, R7).

**6. The officer's correction to my own count — ACCEPTED.** `Vanda` case-insensitively appears in
four files, not three; `state/seen.json` carries a lowercase `vanda` in a BioSpace press-release URL
in the dedup cache. Immaterial — a seen-URL carries no proposition — but the officer was right to
report it, and I was wrong to state a count from a case-sensitive grep. The designer caught the same
thing independently.

**One assertion I could not verify and am not recording as fact.** The officer flags that my
commission's phrase "abandoned under time pressure" is unsupported: `grep -rn "time pressure"`
returns 0, and repository state cannot distinguish abandoned-under-pressure from never-started from
written-elsewhere. It is now established that the limbs were written and the bibliographies exist in
the annotated document, so "never started" is out — but **whether the check was attempted and
abandoned, or simply never pointed at these entries, remains unknown.** I asserted a cause I had not
established, and the officer was right to strike it. The rule below is designed against the failure's
shape, not against a motive I cannot evidence.

## Part 6 — Integrity Officer, Phase 2 (verbatim)

*The officer's adversarial vet, delivered after seeing the design. Reproduced verbatim; headings
demoted, text otherwise unedited. Its disposition is ADOPT subject to four binding amendments, three
strikes, a scope clause, and one Emory item.*

*Both chairman messages arrived after my Phase 1 return and out of order. I have folded the
correction and vetted the design in one pass. **Disclosure that limits what follows: the correction
message asks me to pre-state tests for the required-field candidate "before you see the design." I
have seen the design.** Those tests are therefore post-hoc and I label them as such — they are weaker
as criteria than the ones in my Phase 1 §3, and where they overlap I say which pre-stated criterion
they descend from.*

### PART A — FOLDED PHASE 1 CORRECTIONS

**A1. The limb strings are OPERATOR-ATTESTED, not repository-verified.** I cannot open the annotated
document. Both §VII strings are marked accordingly and I use them as attested premises throughout.
My repo finding stands unchanged and I do not withdraw it: the three-limb text is absent from
repository state **and from repository history** (`git log -- lit-review/` → 2 commits; `git show
aa11338:lit-review/ferguson-memo.md` §VII is the same one-paragraph stub). Repo and document
diverge. That gap is a finding, not a defect in either.

**A2. My §3(v) conclusion is WITHDRAWN IN PART.** "The three-limb rule did not exist in any artifact"
is false on the corrected premise. What survives, and it survives intact: the rule existed **in
prose, in a document with no failure surface**, while the two rules adopted the same morning bind
from `README.md:116`, `scripts/fetch_relay.py:10`, and `tests/test_source_not_read.py:11` despite
their adoption record never reaching `main` (re-verified: `git ls-tree origin/main --
analytics/council-sessions/` returns one file). **Carrier, not emphasis** is unaffected by the
correction. What changes is that the remedy is *both* — enforcement **and** a carrier — not a carrier
instead of enforcement.

**A3. On 2(a) — 3/3 does NOT hold as verified. It is 1/3 verified, 2/3 indicated, and the chairman's
stated method is unsound.**

- **Vanda: VERIFIED author-supplied.** `ferguson-memo.md:41` and `kim-memo.md:22` affirmatively state
  both authors did not use it. Dispositive.
- **H&H and Bonnitcha: NOT verified.** The chairman's evidence is absence from the memos'
  enumerations of the authors' authorities. **Both enumerations are expressly non-exhaustive:**
  `ferguson-memo.md:21` — "he continues to rely heavily upon just a handful of tribunals,
  **including** Tethyan Copper…"; `ferguson-memo.md:28` — "italaw for the primary arbitral awards
  (Siag, Burlington, A11Y, **etc.**)". Absence from a list that says "including" and "etc."
  establishes nothing. If this method is adopted it will produce false negatives elsewhere.
- **Better arguments, offered because the chairman's do not work.** For H&H: `ferguson-memo.md:21`
  records that Ferguson "excludes all other types of claims such as Fair and Equitable Treatment and
  Umbrella Clause Claims as being 'an issue for another time'" — fork-in-the-road is an admissibility
  doctrine outside his stated scope; and `state/research_log.json:9` shows fork-in-the-road is an
  **active project research thread** (`GAP-UNRESOLVED: china-switzerland-forum-relationship`, opened
  2026-07-31). The project has its own demand for the doctrine. For Bonnitcha: the attested annotation
  says "the strongest **external** critical perspective" — external to Ferguson, on its own face. Both
  are strong. Neither is verification.
- **Report it as: 1 verified, 2 strongly indicated, 0 excluded.** Do not write 3/3.

**A4. QUESTION 1 — DIRECT ANSWER: limb (c) is UNSCOPED. The scope-defect reading fails. This is a
discipline failure.** It is too kind, and the text does not bear it.

Three grounds, in order of force:

1. **The scope-carrying reading makes the sentence self-contradictory.** For a source the article
   never cited there is no "citation format used in Ferguson's article" — limb (b) is inapplicable
   **by its own terms**. If (b)'s scoping governed the whole sentence, the entire verification
   statement would be inapplicable to every self-recruited entry, while the same sentence demands that
   "**each entry** contains a verification statement." The only non-contradictory reading is that (a)
   and (c) are unscoped and (b) is conditional on the entry being inherited.
2. **"For which they are used" is passive with no agent.** For an entry the article never cited, the
   only available user is Emory. For **exactly the population that failed**, limb (c) has one possible
   referent and it is inward.
3. **The variation is deliberate on the standard canon.** The qualifier appears in one item of a
   three-item series and is omitted from the others.

**Reconciling my Phase 1 sharpenings, as instructed.**

- **#3 is SUPERSEDED as to §VII and I say so plainly — I reasoned it against the prose because the
  limb text was not available to me.** I found that Emory's *outward prose* formulates a
  ground-of-decision check (`ferguson-memo.md:48`, `kim-memo.md:59`) and never a subject-matter check.
  That is still true of the prose. It does **not** narrow limb (c): "whether the cited paragraphs
  support the proposition for which they are used" plainly covers containment — paragraphs with no
  occurrence of *trade secret* do not support a trade-secret proposition. My #3 does not cut against
  the discipline diagnosis. It was reasoned from an incomplete record and the fuller record defeats it.
- **What survives from #3, and it has a design consequence.** The outward checks Emory demonstrably
  *executed* were ground-of-decision checks. The **containment** limb is one he wrote into his own
  standard and never demonstrated executing in either direction. So the failure is not uniform: it is
  a failure on **the limb with no prior practice behind it**. Design consequence: step 2 (the screen)
  is the step with the least practice and is therefore the step most likely to be performed rather
  than executed. **Its record must be the strongest thing in the rule.** It currently is not — see Q3.
- **#2 survives and changes role.** Author-cited vs self-recruited no longer supports a scope defect;
  it **identifies the population for which (c) is unambiguously inward**, which is the population that
  failed.

**A5. On 2(c) — which diagnosis, and the cost of getting it wrong.** Design against **discipline
failure, with a drafting aggravator named**. The aggravator is real and cheap to fix: limb (b)'s
explicit scoping contaminates the reading of its neighbours, and the section is titled "**Backsourced**
Annotated Bibliography" (`ferguson-memo.md:63`, `kim-memo.md:64`) — a heading that characterises every
entry as inherited, in a section that in fact held self-recruited entries. That heading is where the
scope confusion lives.

- **Designing against scope when it is discipline** (the live error): you ship one clause, behaviour
  is unchanged, the record says it was addressed. The 08-03 base rate predicts that clause does not
  bind.
- **Designing against discipline when it is scope**: you impose ~4 hours per bibliography on a
  population that a one-sentence fix would have corrected.

Since (c) is unscoped, only the first error is live. **Design against discipline; keep the scope
clause anyway** — one sentence, and it removes the reading that made the failure easy.

### PART B — THE DESIGN, AGAINST MY PRE-STATED CRITERIA

**Overall: this is a stronger design than the 08-03 one and it clears the bar that one did not. Three
findings in it are better than my criteria anticipated. Four amendments are conditions of my
approval.**

**Q2 — REPLAY, measured against my five uses**

| # | Under this rule | Verdict vs my pre-stated baseline |
|---|---|---|
| **1a** H&H trade-secret | Step 2, rigid designator *trade secret* → 0. Step 3: no span can exist | **CAUGHT, mechanically** (as predicted) |
| **2** *Vanda* 2020 | Step 2, rigid designator *Trade Secrets Act* → 0 | **CAUGHT** (as predicted) |
| **3a** Bonnitcha IP | Step 2, *TRIPS* / *patent* / *trademark* → 0 | **CAUGHT** (as predicted) |
| **3b** Bonnitcha annotation | See below | **NO LONGER AN INVERSION — the single most valuable ruling in the design** |
| **1b** H&H fork-in-the-road | See below | **NOT CAUGHT. Made legible to a second reader** |

**On 3b — the designer's rigid-designator test defeats my predicted inversion, and I credit it
without reservation.** My Phase 1 prediction was that a screen returning "recognition: 2" would read
as confirmation. Under this rule that outcome is structurally unavailable: *recognition* is a
descriptive word, so a nonzero on it is not a pass ("a nonzero is not a pass"; "the count is
provenance, never justification"), and a zero on it is not a finding either. The screened set must
include a rigid designator — for this proposition, *TRIPS* — which returns 0. **The architecture is
correct and it is the fix for the most dangerous of my five uses.**

**But item 6 does not reach 3b, exactly as my residue item 5 predicted, and the design should stop
implying it does.** "The strongest external critical perspective" is superlative and relational, so
item 6 fires — and **no span can satisfy it**, because no sentence in any source says "this is the
strongest critical perspective on X." The writer therefore takes item 6's second branch and rewrites
it as judgement: *"In my judgement, the strongest external critical perspective on the doctrinal
architecture inside which Ferguson is working."* **That passes item 6 and is still wrong.** Item 6
converts a false factual claim into an honestly-labelled false judgement. It catches the form, not
the error. 3b is reached by **step 2, not item 6** — and only because the entry's underlying
content-proposition is span-checkable even though its superlative is not. Record item 6 as a
labelling rule, not a catch.

**On 1b — item 5 does not catch it. It makes it detectable by a second reader.** The D line is
fillable compliantly, truthfully, and in under a minute by a writer who has not understood the
problem: *"Decision on Jurisdiction, [date]; resort management and operation dispute; jurisdictional
stage; fork-in-the-road objection **joined to the merits, not decided**; award rendered, annulment
discontinued 2016 for non-payment."* Every clause is true and the entry is still wrong. Whether the
writer then sees that a joined objection is not authority for the doctrine is **entailment** — the
designer's own named residue and the rule's own declared load.

**FLAG — OVERREACH, and I require it struck in the R5 idiom.** "Writing that line is not possible
while believing the entry is sound" is a psychological claim presented as a mechanical property. It is
the same species as the *Hela Schwarz* sentence the chairman struck on 08-03. Replace with what is
actually true and is a genuine advance: **item 5 is the first mechanism in this project that satisfies
my C4 for the status class** — a reader holding only the D line, without re-opening the source, sees
"joined to the merits, not decided" sitting beside a proposition that says the tribunal applied the
doctrine. That is real. It is not a catch at the writer.

**FLAG — the §(d) determinism claim is misstated.** "Three of four failures fall to a purely
mechanical test" should read: **three of five *uses* fall to a mechanical test; the fourth (1b) is not
caught but is made third-party-detectable; the fifth (3b's superlative) is not caught by item 6 at
all.** The unit "failures" hides that H&H is two uses with two different fates.

**On the *Vanda* branch — the rule reaches it, but through step 4, not step 3, and step 3's exit list
must be amended.** Step 4 ("cite the document, not the case") is what forces "436 F. Supp. 3d 256
(D.D.C. 2020)" to be named as *the document read*, which is what makes the 6 May 2021 opinion visible
as a different object. The designer's document-level/case-level distinction is correct and is the
second-best finding in the design. **But step 3's exits are: narrow, find another source, drop.** A
writer who has screened one document and found nothing reads "find another source" as *a different
authority*, and the cheapest exit is "drop." **AMENDMENT 1 (binding): step 3 gains a fourth exit,
listed FIRST — "retrieve a different document in the same matter (opinion, order, decision, or award
at another stage or date) and restart at step 2."** One clause. Without it the rule loses the right
case in the one instance where the right case was one docket entry away.

**Q3 — my criteria (iii)(B), (C), (D)**

**(C) — asymmetry orientation: the design has it RIGHT IN PROSE AND BACKWARDS IN THE ARTIFACT.** It
does not hard-block on zero (the rigid-designator test explicitly makes an unqualified zero "not a
finding about the source") and it does not pass silently on nonzero *as a matter of instruction* ("a
nonzero is not a pass"; "go read the hit"). So the stated architecture passes my (C). **But the record
does not.** Every zero produces a named exit written into V. Every nonzero produces a count and
**nothing else**. The cheap side is documented; the expensive side — the side the designer himself
calls "the more dangerous of the two" — leaves no trace. Bonnitcha proves it: the V line under the
rule as drafted reads `screened: TRIPS 0, intellectual property 0, recognition 2`, and **that line is
fully compatible with the failure that actually occurred.**

**(B) — GAP. Must be closed by amendment. AMENDMENT 2 (binding), exact wording:**

> **V** — checked \<date\> at \<where retrieved\>; screened \<term:count\>; **for every screened term
> with a nonzero count whose occurrences are not the source of Q, one clause in your own words stating
> what the source is discussing at that occurrence**; \<exit taken, if any\>.
>
> Worked form: `screened: TRIPS 0; intellectual property 0; recognition 2 — both occurrences concern
> recognition and enforcement of arbitral awards, not municipal recognition of a protected asset.`

**And this amendment is MECHANICAL, which the designer's own column does not currently reflect.** The
check is set membership over one line: **every screened term with a nonzero count must appear either
as the source of Q or in a referent clause.** No judgement, countable by anyone with the entry in
front of them. **The design's mechanical column has no check whatsoever on the nonzero branch; this
puts one there.** I regard it as the highest-value amendment in this note.

**(D) — SUBSTANTIALLY SATISFIED for propositions that have a rigid designator; UNSATISFIED for those
that do not.** I credit the rigid-designator constraint as a substitute for the pre-committed
vocabulary I demanded and did not anticipate: a rigid designator is by construction **not** the
writer's choice — *TRIPS* is *TRIPS* — so it removes the degree of freedom that matters, which is
screening only terms you expect to find. **AMENDMENT 3 (binding):** the recognition–enforceability gap
has no rigid designator of its own, which is exactly the Bonnitcha case. Where none exists, the entry
must say so and the verdict is labelled weaker — `screened: no rigid designator available for this
proposition` — which is my (D)'s labelled-weaker-verdict branch at a cost of one clause.

**Q4 — my disqualifier, and C3**

**Disqualifier: CLEARED. This is the first rule I have vetted on this project that clears it.** An
entry reading "verified" with no locator, span, or term set fails on four independent countable
grounds: mark presence (P/Q/D/V), mark-count parity against entry count, Q's
quotation-pair-and-pinpoint token, and V's non-empty term:count list. Compliance and abandonment
produce different artifacts. That was my stated fatal test and it is met.

**C3 — binding Q to P closes the escape I named for the failures at hand, and does not close it in
general. It is NOT `METHODOLOGY.md:56` with a new name.** §56 requires a quote from **the source**;
this requires a quote **for the proposition**, plus a pinpoint, plus a screen record, plus a
point-level disposition card. On the three instances the difference is dispositive: the operative term
is absent, so there is no quote to paste — the escape has no material. On a topically-correct source
with an adjacent-but-not-carrying passage, the escape survives intact, and the designer is right to
call entailment "the whole rule's load."

**On `METHODOLOGY.md:55-56` — DISTINGUISH. Do not amend, do not supersede.** Reasons: (1) §55-56
governs the **digest**, a machine-generated artifact, where the verbatim quote is an *anchor* for the
reader, not a *support* claim; the carrying-span rule governs hand-written scholarly citation. Two
artifacts, two standards is correct here. (2) Amending §56 to require carrying spans would impose an
entailment predicate on a pipeline that structurally cannot satisfy it — I re-verified the designer's
finding, `grep -rn "supporting_quote" src/ scripts/` returns **exactly one line,
`src/integrity_gate.py:126`**, a copy-through; nothing compares it to anything. Requiring carrying
there creates a standard nothing can meet, which is the ornamental machinery the 08-03 session struck
at R9. (3) The chairman cannot touch METHODOLOGY.md.

**The Emory item, worded so it can be lifted:** *`METHODOLOGY.md:56`'s "at least one direct verbatim
quote" is an anchor requirement for digest entries, not a support requirement, and does not carry the
carrying-span standard. The carrying-span rule governs hand-written citation in memos and
bibliographies.* **One sentence must appear in the new rule's own text**, or the project ships two
annotated-bibliography standards with the stronger silently assumed to cover the weaker's artifact —
and `METHODOLOGY.md:56` is the standard that would have caught none of the three.

**Q5 — COST: VIABLE, WITH ONE NAMED REDUCTION. I release the 10-minute figure and I state the
grounds, because releasing a pre-stated criterion is the thing I said I would not do lightly.**

1. **I was measuring the wrong unit.** My 10 minutes was a uniform per-entry ceiling; the designer's
   figures are per entry *type*, ~7 for articles. My own Phase 1 count of Kim's §VII list (~11 named
   authorities, of which the EMA policy, TRIPS 39(3) and the secondary-literature bucket are non-case
   entries) implies well under half case entries. At the designer's own numbers a 25-entry
   bibliography is **~4 hours — the identical figure I derived at 10 minutes and called survivable.**
   My criterion and his estimate agree on total burden and disagree only on the unit. That is not a
   conflict I can win on the merits.
2. **The boundedness constraint — my hard constraint, on which I said I would reject — is met.** Every
   step scales with entry count, none with source length.
3. **Front-loading is correct in form on the three instances:** all three die at a zero-count
   rigid-designator screen.

**What I do NOT release: the 20-minute docket chase.** It is the rule's **only unbounded operation** —
a docket history has no bound — it is the most expensive step, and its product is the one thing in the
entry that gets **no carrying span**, which is the designer's own DOCKET-HISTORY RECRUITMENT residue.
It is where an abandoned rule will break first.

**AMENDMENT 4 (binding), the named reduction:** item 5's "**what happened after**" becomes
**conditional — required only where the proposition depends on finality** (that the holding stands, was
affirmed, was not annulled or vacated). H&H's "annulment discontinued 2016 for non-payment" is exactly
that case and stays in. Everywhere else it is optional. This removes the only unbounded operation in
the rule and takes the case-entry figure to ~12.

**Q6 — the base rate, and what ADOPTED requires**

**What the adoption record must contain, or I record the rule as UNVALIDATED:**

1. **The entry template, in full, in the record — not a description of it, and not a promise to create
   one.** The 08-03 session ruled increment 0 "adopted" with no carrier and it did not bind within the
   day: `git log -- agents/integrity-officer.md` → last modified **2026-07-31**, and the Self-training
   mandate at `:109-111` still enumerates **five** patterns while the same file's taxonomy section at
   `:60-80` enumerates **ten**. My instantiated prompt this session carries the five. Nothing has
   moved.
2. **The rule's text attached to an artifact that fails.** The proven pattern in this repo is
   `fetch_relay.py:10` / `test_source_not_read.py:11`. The best surface available is the designer's own
   find: **`HUMAN_REVIEW.md:44-51`, which already states limb (c) in operative committed form** — "the
   question is not whether the URL resolves… but whether the source **actually supports the claim**… A
   URL that loads but does not say what the claim says is a **FAIL**." I verified the designer's
   caveat: `grep -rln "HUMAN_REVIEW" tests/` → **nothing**; it is referenced only by
   `scripts/review_prep.py` and `scripts/build_graph.py`. So extending its scope makes the rule
   **recorded, not enforced**. **I want it anyway** — recorded-and-third-party-checkable satisfies my
   C4, and prose-in-a-stub satisfies nothing. Do not let it be sold as a guard.
3. **The scope clause**, per A4/A5: the rule applies to self-recruited sources as well as backsourced
   ones, stated in the rule's own text.
4. **The three strikes**, R5 idiom: "writing that line is not possible while believing the entry is
   sound"; "three of four failures fall to a purely mechanical test"; and any sentence implying item 6
   handles Bonnitcha's superlative.
5. **The four amendments** above as conditions, not suggestions.

**The one number: `N changed / M screened`** — entries where the rule FIRED and the citation CHANGED
(source dropped, proposition narrowed to the span, pin cite moved to another document in the same
matter), over entries screened.

Not the compliance rate: compliance and performance are indistinguishable, which is the entire
problem. **A bibliography reporting M > 0 and N = 0 has been complied with and never tested — that is
the signature of performed-not-executed, and it is precisely what the 08-03 override-rate metric was
reaching for and structurally could not see.** On the three known instances the true rate is at least
3/3, so an early report of 0/25 is a **positive detection of performance**, not evidence of clean work.

### PART C — POST-HOC TESTS FOR THE REQUIRED-FIELD/NULL CANDIDATE (labelled: written after seeing the design)

The V mark plus step 3's exits **are** the chairman's candidate. Three evasion paths, and what makes
each detectable:

1. **Vague statement asserting support without locating it.** Closed on the V mark — Q's
   quotation-pair-and-pinpoint requirement means an assertion with no span fails mark presence,
   countable with Ctrl-F. **Not closed in its surviving form**, which is a vague **P**, not a vague V —
   the designer's own ANNOTATION VAGUENESS residue ("informs the doctrinal background"). Vague is not
   false; it passes every check including the reject list. **I confirm this as the design's strongest
   surviving escape and I have no mechanical answer to it.** Descends from my Phase 1 C3.
2. **The null quietly avoided by deleting the entry.** The reject list is the intended answer and the
   designer correctly calls it "a signal, not a gate." Deletion plus omission from the reject list is
   invisible to everyone. Partial fix: the mechanical column already requires the reject list be
   **non-empty** — but non-emptiness is satisfied by one line. **Require the reject count reported as
   the M in `N/M`.** A bibliography reporting 25 entries and 1 reject is anomalous on its face; the
   three known instances alone would have produced three.
3. **Statements copy-pasted across entries.** This is my Phase 1 degenerate-uniformity detector and it
   is **fully mechanical — string equality across V lines and across D lines** — and it is **not in the
   designer's mechanical column.** Put it there. It costs nothing and it is the only check in the set
   that detects performance directly rather than inferring it.

### Taxonomy — extended (officer's self-training mandate)

- **narrow-in-the-entry-wide-in-the-body** — a verified, correctly narrowed bibliography entry sitting
  beside body prose that argues the original unnarrowed proposition. The entry is clean and the memo is
  wrong. No entry-level check reaches it.
- **annotation-vagueness-as-compliance** — a relational or characterising claim made unfalsifiable to
  survive verification. Passes every check because vague is not false.
- **unscoped-rule-read-as-scoped** — a standard the writer authored, which covers his own work on its
  face, read as governing only the material under review because a neighbouring clause was scoped and
  the section heading named the inherited class. *(Correction to my own Phase 1 taxonomy work: I did
  not have this pattern in Phase 1 because I was reasoning from a repo in which the rule did not
  exist.)*

**DISPOSITION: ADOPT, subject to the four binding amendments (step 3's same-matter exit; the V-mark
referent clause and its mechanical parity check; the no-rigid-designator label; item 5's finality
condition), the three strikes, the scope clause, and the `METHODOLOGY.md:56` distinguishing sentence as
an Emory item. Record as UNVALIDATED until `N/M` is reported with N > 0.**

The rigid-designator test and the document-level/case-level distinction are the two best pieces of work
in this session and both defeat predictions I made in Phase 1 — 3b is no longer an inversion, and the
*Vanda* recovery path exists where I expected only a drop. My objections are to two overclaimed
sentences, one absent mechanical check on the branch the designer himself calls the more dangerous, and
one unbounded step. Not to the rule.

**Nothing was written or modified.**

---

## Part 7 — Chairman's Rulings

### R1 — THE DIAGNOSIS IS A DISCIPLINE FAILURE. My scope-defect framing is OVERTURNED.

I put the scope question to the officer as the single most important question in its Phase 1, and I
asked for a direct answer rather than a balance of considerations. I got one, and it goes against the
framing I carried into the session. **Limb (c) is unscoped and it reached Emory's own citations.**

The officer's first ground is decisive and I adopt it as the council's reasoning: for a source the
article never cited there is no "citation format used in Ferguson's article," so limb (b) is
inapplicable *by its own terms*. If (b)'s scoping governed the whole sentence, the verification
statement would be inapplicable to every self-recruited entry — while the same sentence requires that
"**each entry** contains a verification statement." The only reading that does not contradict itself is
that (a) and (c) are unscoped and (b) is conditional. Add that "for which they are used" is agentless
passive, and for exactly the population that failed, its only possible referent is Emory.

So the corrected chain of this session is: I was handed *the rule was applied asymmetrically*; I
verified it against the repo and reported *the rule does not exist*; I was corrected to *the rule
exists but its scope excluded the failing population*; and the officer, reading the limb text I had
just been given, found that **the scope did not exclude them.** The rule covered these entries and was
not applied to them. That is the finding, and it is the least comfortable of the four.

**One aggravator is real and I record it**, because it is what made the misreading available: limb (b)'s
explicit scoping contaminates its neighbours, and the section heading is "**Backsourced** Annotated
Bibliography" — a title that characterises every entry as inherited, sitting over a section that in
fact held self-recruited entries. That is a drafting defect. It is not a defence, and the rule below
closes it with one sentence anyway.

### R2 — MY OWN 3/3 CLAIM IS CORRECTED TO 1 VERIFIED, 2 INDICATED. The method was unsound.

I told both seats that all three failed citations are author-supplied and that this was verifiable from
repository state. The officer checked and I was wrong on method. `ferguson-memo.md:21` reads "just a
handful of tribunals, **including** Tethyan Copper…" and `:28` reads "(Siag, Burlington, A11Y,
**etc.**)" — I verified both myself after the objection. **Absence from an expressly non-exhaustive list
proves nothing.** Only Vanda is verified author-supplied, on affirmative statements in both memos that
neither author used it. H&H and Bonnitcha are strongly indicated on better arguments the officer
supplied — fork-in-the-road sits outside Ferguson's self-declared scope, and Bonnitcha's own annotation
calls it "**external**." **The record reads 1 verified, 2 strongly indicated, 0 excluded, and I have
corrected Part 2 accordingly.** This is the second time in two sessions that a chairman's premise
reached the seats unverified in one of its limbs, and it is the subject of my self-training note.

### R3 — THE RULE IS ADOPTED, AS AMENDED. Final form.

All four of the officer's amendments are folded in, plus the scope clause and the distinguishing
sentence. This is the text to be lifted into `prompts/` and the memo template.

> ## THE CARRYING-SPAN RULE
>
> **Scope.** Every source cited for a proposition — in a memo, a bibliography, or a council record —
> whether the source is one the work under review cited or one you found yourself. **Your own
> citations are not exempt.** (Separate from `METHODOLOGY.md` §VII, whose "at least one direct
> verbatim quote" is an *anchor* so a digest reader can find the source, not *support* for a
> proposition. That standard does not carry this one.)
>
> 1. **Proposition first.** Before opening the source, write the one sentence you are citing it for.
>    That sentence is what gets verified. If it changes, it is a new proposition: restart.
> 2. **Screen the whole text.** Search the retrieved document for the proposition's operative terms —
>    at least three, including one **rigid designator** (a name the field cannot paraphrase away:
>    TRIPS, the Trade Secrets Act, Art. 39(3), "fork in the road", a party name) and one truncated
>    stem. If the proposition has no rigid designator, **write that down**; the verdict is weaker. A
>    zero is not a verdict; a nonzero is not a pass. Zero on a descriptive word: try its synonym. A
>    hit: go read the hit.
> 3. **Quote the carrying span.** Put the source's own words that carry the proposition into the
>    entry, with a pinpoint. A pinpoint alone is not compliance. If nothing carries it, take one exit
>    and name it, **in this order**: (i) retrieve a different document **in the same matter** —
>    another opinion, order, decision or award, at another stage or date — and restart at 2; (ii)
>    narrow the proposition to what the span does carry; (iii) find another source; (iv) drop it. If
>    you cannot retrieve enough to look, the source is **unread**: say so and assert nothing from it.
> 4. **Cite the document, not the case.** Name the opinion, award or decision you actually read, and
>    its date.
> 5. **Card every case:** what the dispute was about, the stage cited, and how it came out **on the
>    point you cite** — "joined to the merits" and "undecided" are outcomes. Add what happened after
>    **only where your proposition depends on finality.**
> 6. **Annotation claims are propositions.** Any relational or superlative claim about a source —
>    strongest, closest, most on point — needs its own span, or is rewritten as your own judgement.
>    **Labelling it as judgement does not make it true.**
> 7. **Record the rejects.** List what you screened and did not use, and why.
>
> **Every entry carries four marks:**
>
> ```
> P — the one sentence
> Q — "the carrying span" [pinpoint]
> D — document + date; what the dispute was about; stage; outcome on the point cited;
>     [what happened after — only if the proposition depends on finality]
> V — checked <date> at <where retrieved>; screened <term:count>;
>     for every screened term with a nonzero count whose occurrences are NOT the source of Q,
>     one clause in your own words saying what the source is discussing there;
>     <exit taken, if any>
> ```
>
> Worked V line: `screened: TRIPS 0; intellectual property 0; recognition 2 — both occurrences
> concern recognition and enforcement of arbitral awards, not municipal recognition of a protected
> asset.`

The spine, for holding in the head while writing: **Proposition, Screen, Span, Document, Disposition,
Annotation, Rejects.** Seven items, four marks.

### R4 — THE THREE STRIKES ARE APPLIED. The record states what is true, not what is flattering.

The officer's objections bind and I apply all three without softening.

- **STRUCK:** "Writing that line is not possible while believing the entry is sound." That is a claim
  about a writer's mind presented as a property of a mechanism. **Replaced with:** item 5 is the first
  mechanism in this project that makes the status class detectable by a second reader who never opens
  the source — a reader holding only the D line sees "joined to the merits, not decided" sitting beside
  a proposition asserting the tribunal applied the doctrine.
- **STRUCK:** "Three of four failures fall to a purely mechanical test." **Replaced with:** three of
  five *uses* fall to a mechanical test (H&H trade-secret, Vanda, Bonnitcha subject-matter); the fourth
  (H&H fork-in-the-road) is not caught and is made third-party-detectable; the fifth (Bonnitcha's
  superlative) is not caught by item 6 at all. The unit "failures" concealed that H&H is two uses with
  two different fates.
- **STRUCK:** any implication that item 6 handles the Bonnitcha annotation. **Item 6 is a labelling
  rule, not a catch.** The officer's demonstration is unanswerable: the writer prefixes "in my
  judgement" and the claim passes while remaining false. Bonnitcha is reached by step 2, not item 6,
  and only because its underlying content-proposition is span-checkable.

### R5 — THE ENFORCEMENT SURFACE, stated without inflation.

The finding that decides this is mine, verified in Part 2 and re-verified by the officer: **rules bind
in this project when they are attached to an artifact that fails.** `scripts/fetch_relay.py:10` and
`tests/test_source_not_read.py:11` carry this morning's two standing rules and bind although their
adoption record never reached `main`. Limb (c) lived in prose in a section that is a stub. Carrier, not
emphasis — with the officer's correction that the remedy is **both**: this was a discipline failure, so
the rule needs enforcement *and* a carrier, not a carrier instead of enforcement.

**Real, in descending strength:**

1. **Transcription.** A carrying span cannot be produced without opening the source at that place. Not
   auditable that you read; not producible without having looked. Works in a word processor with no
   repo, no CLI, no agent.
2. **Mark parity, countable by anyone.** Entry count against `V —` count, `P`/`Q`/`D`/`V` presence,
   `Q` carrying a quotation pair and a pinpoint token. Ten seconds with Ctrl-F.
3. **Nonzero-referent parity — the officer's Amendment 2, and the highest-value mechanical addition in
   the session.** Every screened term with a nonzero count must appear either as the source of `Q` or
   in a referent clause. Set membership over one line, no judgement. Before this amendment the design
   had **no mechanical check at all** on the branch the designer himself called the more dangerous.
4. **Span-in-source on demand.** Any `Q` pastes back into the source's find field. A span that does not
   hit fails with no argument available.
5. **Degenerate uniformity.** String equality across `V` lines and across `D` lines. Fully mechanical,
   and the only check in the set that detects performance directly rather than inferring it. Adopted
   into the mechanical column per Part C.3.

**Weak, and named as weak:** the reject list is a signal, not a gate; its real value is that it turns
compliance into content.

**Exhortation, and I will not dress it up:** step 1's ordering — no artifact records the sequence in
which two sentences were written; and entailment — whether the span carries the proposition is
checkable only by a reader.

**The sentence the council does not get to avoid.** The enforcement surface for the failure that
actually occurred was Dr. Benavides's margin. It still is. This rule makes her target smaller. It does
not remove her from the loop, and any reading of this record that implies otherwise is overclaiming.

### R6 — WHAT THIS CLOSES AT THE CLASS LEVEL, AND WHAT IT ONLY MAKES VISIBLE.

**Closed at the class level — a proposition whose operative term does not occur in the cited
document.** This is the whole of the Vanda failure, the whole of the H&H trade-secret failure, and the
subject-matter half of Bonnitcha. Under step 2 with a rigid designator these do not survive to become
entries: no span can exist, so no `Q` can be written. It is mechanical, it is cheap (about two minutes),
and it fires before any expensive step. Three of five uses die here.

**Made visible, not closed — the status class.** Right source, right passage, wrong legal weight:
joined to the merits, dicta, dissent, argument of counsel, vacated. Item 5 puts "joined to the merits,
not decided" on the page next to a proposition claiming the doctrine was applied. **A second reader sees
the contradiction; the rule does not stop the writer producing it.** This is the class with the worst
outcome history in the project and it remains open.

**Made visible, not closed — the nonzero/homonym branch.** Amendment 2 forces the referent into the
record. It does not adjudicate the referent.

**Not closed, and named:** entailment, which is the rule's declared load; **annotation vagueness**,
which the officer and designer independently identify as the predicted compliance-and-defeat path and
for which neither has a mechanism; **narrow in the entry, wide in the body**, where the bibliography
comes out clean and the prose argues the unnarrowed version; **aggregation**; **apt-but-not-authority**;
**docket-history recruitment** at item 5's finality field, which gets no carrying span; **inaccessible
and redacted sources**, where a zero means nothing; and **self-judged sufficiency**, against which the
only structural break is a second reader.

I record the honest summary: **the rule closes one failure class outright, makes two detectable by a
third party, and leaves the judgement at the centre exactly where it was.**

### R7 — SCOPE: THE RULE EXTENDS TO THE COUNCIL'S OWN RECORD-WRITING. Both seats recommended it; I adopt it with one boundary.

**It binds** every place a source is attached to a proposition in prose: the memos and bibliography,
the daily research records, session records, `STATE_OF_THE_ANSWER.md`, and analyst and officer returns.

**It does not bind** the pipeline's structured `candidate_claims`, which the 2026-08-03 pre-ledger
system governs. Two rules on one artifact is how the `METHODOLOGY.md:56` confusion arose, and I will
not reproduce it.

Three reasons, in order:

1. **The doctrine that produced half of instance 1 is a live council thread.** `state/research_log.json`
   seq 39 carries the China–Switzerland forum-relationship mapping — fork-in-the-road vs. no-U-turn —
   `GAP-UNRESOLVED` since 2026-07-31. The council is actively researching the doctrine for which H&H was
   recruited. A rule that binds the memo and not the record leaves the same recruitment available in the
   record next week.
2. **The council's record already shows the discipline in structured form and would benefit from it in
   prose.** `analytics/daily-research/2026-07-22.md:128-134` carries the Hela Schwarz fork-in-the-road
   claim with `supporting_quote` set to the article headline and `supporting_locator` reading "article
   title (indexed; body paywalled)." That entry is **honest** — the locator declares exactly what
   carried the proposition, which is what the bibliography never did. It is not an instance of this
   failure. It is the proof that the council already knows how to declare what carried a proposition,
   and the rule generalizes that habit to prose where no locator field exists.
3. **The officer's C4.** A rule detectable only by its author changes nothing. Council records are read
   by other seats and by the operator; extending scope creates the second reader the memo lacks.

### R8 — STATUS: ADOPTED AND UNVALIDATED. The base rate binds me.

The officer's Q6 challenge is the most serious thing in this session and I verified it myself:
`agents/integrity-officer.md` was last modified **2026-07-31**, by a vault-wide managed-block
regeneration; its taxonomy section is headed "extended to ten" while its Self-training mandate still
enumerates **five**; and the officer reports its instantiated prompt this session carried the five. This
morning's council called taxonomy sync "increment 0 ... the cheapest mechanical win in the session" and
**it did not bind within the same day, in the single file it names.**

Against that base rate I will not record this rule as working. **It is ADOPTED in text and UNVALIDATED
in practice.** It becomes validated when one number is reported: **`N changed / M screened`** — entries
where the rule fired and the citation actually changed (source dropped, proposition narrowed, pin cite
moved to another document in the same matter), over entries screened, with the reject count as `M`.

I adopt the officer's reading of that metric in full, because it inverts the naive one: **a bibliography
reporting M > 0 and N = 0 is a positive detection of performance, not evidence of clean work.** On the
three known instances the true rate is at least 3/3. A first report of 0/25 means the rule was complied
with and never executed.

I also honor the officer's first adoption condition here rather than deferring it: **the entry template
is in this record in full, at R3, not described and not promised.** That was its stated test for whether
this session repeats the increment-0 failure.

### R9 — THE ARTIFACT IS NOT IN VERSION CONTROL. The rule gains NO repository precondition.

Measured this session and verified by me before ruling: `grep -c -i "Descriptive annotation"` returns
**0** in both memos; `wc -w` gives **3,351 and 4,429 — 7,780 words total**; each §VII is a single
italicised sentence followed immediately by the managed graph block. **The two bibliographies contain
zero entries in version control.** H&H, Vanda, Bonnitcha and every other entry exist only in a word
processor. Nothing in version control has ever held them.

I commissioned the designer to rule on whether the rule should gain a precondition — that the
deliverable must be in the repository, in a form a check can read, before the rule applies. **The
designer did not return on that follow-up.** Recorded as a procedural fact, not papered over. The
ruling is mine and I make it rather than leave the record open; I do not write it in the designer's
voice.

**RULED: no precondition. The rule applies unconditionally. The enforcement tiers are conditional and
are stated that way.**

1. **A precondition Emory cannot satisfy this week makes the rule inapplicable this week**, and the
   rule's strongest mechanism does not need the repository at all. Transcription constrains the writer
   at the keyboard whether or not any file is ever committed. Gating the rule on version control would
   suspend the one mechanism that works today in exchange for checks that only pay later.
2. **It would reproduce the exact defect this session was convened to fix.** Limb (c) failed because a
   neighbouring clause and a section heading made it read as inapplicable to the entries that broke. A
   precondition keyed to repository presence would make this rule *formally inapplicable to precisely
   the artifact that failed.* I will not adopt a second applicability carve-out in a session convened
   because the first one was misread.
3. **It is adjacent to the relocation the officer refused.** Its C1 is explicit — "a design that
   quietly relocates the rule to a repo file it can enforce has changed the subject" — and residue item
   7 refuses "relocating the rule to an artifact the repo can reach and calling that the same rule." A
   precondition is not relocation, but conditioning applicability on reachability gets to the same
   place by a different road.

**What this fact does change is the enforcement ranking, and the designer's section overstated it.**
It ranked mark parity and span-in-source as real enforcement "countable by anyone." With zero entries
in version control, *anyone* currently means two people: Emory and Dr. Benavides. That still satisfies
the officer's C4 — detectable by someone other than the author, without re-reading the source — because
Dr. Benavides is a genuine second reader. **It is not mechanical, and this record does not call it
mechanical.** Corrected tiering:

- **Works today, no repository required:** transcription (R5.1).
- **Human-countable today, mechanical the day a plain-text export is committed:** mark parity,
  nonzero-referent parity, degenerate uniformity, span-in-source (R5.2–5).

Whether the bibliographies enter version control is Emory's content decision, recorded in Part 8. It
gates the mechanical tier. It does not gate the rule.

### R10 — A NEW STANDING RULE FOR THE COUNCIL ITSELF, because this session's absence produced two independent misreadings.

The same missing artifact defeated two seats reasoning correctly. The integrity officer declined to
attribute the errors because it grepped and found no such citations. I reported that the premise "does
not survive a grep" for the same reason. Neither of us was careless; both of us treated *absent from
the repository* as *absent, full stop*. On a project whose principal deliverables are written outside
version control, that is a standing trap, and it will recur on every artifact that lives in a word
processor.

> **STANDING RULE (adopted).** A report of absence states its domain: **"absent from repository
> state."** It may not be converted into "does not exist" unless the repository is known to hold the
> artifact in full. Where the artifact is known to live outside version control — the lit-review memos
> and their bibliographies today — absence from the repo is **no evidence at all** about the artifact,
> and a seat that needs the artifact must say so and stop rather than infer.

This belongs in the council's procedure, not in the carrying-span rule; it constrains seats reading
the record, not writers attaching sources to propositions. It is cheap, it is mechanical in the sense
that matters (it is a wording requirement on a report), and it would have prevented both of today's
misreadings.

---

## Part 8 — What needs Emory

Nothing was built. `src/`, `scripts/`, `tests/`, `.github/`, `prompts/`, `lit-review/` and
`METHODOLOGY.md` are untouched. These are decisions, in dependency order.

| # | Decision | What it costs you | Council position |
|---|---|---|---|
| **0** | **Report `N changed / M screened`** on the next bibliography pass — entries where the rule fired and the citation actually changed, over entries screened, with the reject count as `M`. | One line. | **The rule is UNVALIDATED until this exists.** Note the officer's inversion: `M > 0, N = 0` is a positive detection of performance, not clean work. On the three known instances the true rate is at least 3/3. |
| **1** | **Do the bibliographies enter version control** — a plain-text export committed to `lit-review/`? | A change of practice: the memo enters git. | Your content, your call. It converts four of five enforcement mechanisms from human-countable to mechanical. Without it the rule still applies (R9) but only transcription and Dr. Benavides enforce it. |
| **2** | **Lift the R3 rule text into `prompts/` and create the bibliography template.** No template exists — `templates/` holds `digest.html.j2` and `research_brief.html.j2` only. | Small. Two files. | Do this. The officer's C1 is that a rule must be written into the artifact whose production it constrains, at the point of production. A rule in a session record constrains nothing. |
| **3** | **Add the distinguishing sentence about `METHODOLOGY.md:56`** — I am forbidden to touch that file. The sentence, ready to lift: *"`METHODOLOGY.md` §VII's 'at least one direct verbatim quote' is an anchor requirement for digest entries, not a support requirement, and does not carry the carrying-span standard."* | One sentence, in the new rule's text, not in METHODOLOGY.md. | Do it. Otherwise the project ships two annotated-bibliography standards with the stronger silently assumed to cover the weaker's artifact — and §56 is the one that would have caught none of the three. |
| **4** | **Extend `HUMAN_REVIEW.md`'s scope from pipeline claims to the lit-review bibliography.** Its `:44-51` already states limb (c) operatively. | One paragraph, zero code. | Approve, with the label the officer demanded: `grep -rln "HUMAN_REVIEW" tests/` returns nothing, so this makes the rule **recorded, not enforced**. Worth doing — prose-in-a-stub satisfies nothing — but do not let it be sold as a guard. |
| **5** | **Taxonomy sync — still unapplied from this morning, now with nine new entries.** `agents/integrity-officer.md` last modified 2026-07-31; taxonomy section says ten, Self-training mandate at `:109-111` still enumerates five, and the officer's instantiated prompt carried the five. | The item this morning called the cheapest mechanical win. | **This is the base rate that made me record today's rule as UNVALIDATED.** Nine patterns were added today: *source-apt-in-topic-not-in-content, deferred-ruling-as-holding, homonym-hit-as-confirmation, synonym-zero-as-refutation, near-docket substitution, verification-statement-as-performance, narrow-in-the-entry-wide-in-the-body, annotation-vagueness-as-compliance, unscoped-rule-read-as-scoped.* They will not bind either unless the file changes. |
| **6** | **If 08-03 increment 5 ships, add non-decision tokens to `DISPOSITION_ADVERSE`:** `joined to the merits`, `not decided`, `assumed without deciding`, `reserved`, `left open`. | One list edit. | Approve. The lexicon has no token for a non-decision, so H&H passes it today. |

**Standing escalations, unchanged and not re-argued:** the ledger snapshot amendment for
`da33a30be92ab234`; the `source_analytics.py` sign-off; the source-architecture decision; the emailer
CONSISTENCY WARNING question; the China–Switzerland IIA-mapping query (treaty 978, forum relationship
— the `GAP-UNRESOLVED` thread that is also this session's live instance of the doctrine H&H was
recruited for); and the routing decision on fetch-dependent work.

**One procedural failure to record.** The systems designer did not return on the R9 follow-up. Its
primary commission was delivered in full and is at Part 3; the precondition ruling is mine at R9.
Recorded because a session without an honest account of a seat's non-return is a defect.

---

## Self-training note (chairman)

**Applied from the prior session.** The rule I adopted on 2026-08-03 — *verify what I assert first;
the chairman's premise is the first claim in the session and it gets checked before the agenda goes
out* — is what produced Part 2. I grepped the premise before either seat started, found the limbs
absent from repository state, and sent the correction ahead of the work rather than at Part 5. That
was right, and it saved both seats from building on a framing that was wrong in its repo-facing half.
I also applied the second note — labelling which of my candidate mechanisms were requirements and
which were illustrations — and the designer used exactly that latitude to reject the "or pinpoint"
half of (a) and to correct my case-level framing of (c) to point-level and document-level. Both
corrections improved the rule. That is the delegation working as intended for the first time in four
sessions.

**Today's sharper failure, and it is a variant of the same one.** I verified my premise and then
**over-read my own verification.** Finding the limbs absent from the repo, I inferred they did not
exist — and told both seats so. They exist; the repo is simply not where the deliverable lives. Then,
after being corrected, I did it a second time in the same session: I asserted 3/3 author-supplied to
both seats on the strength of absence from two enumerations that read "including" and "etc." The
officer had to correct me, and the corrected count is 1 verified, 2 indicated.

The pattern is one step past the rule I adopted last session. Verifying my premise was necessary and
not sufficient, because **the check I ran was sound and the inference I drew from it was not.** A grep
establishes what is in the repository. It establishes nothing about the world, and it establishes
nothing about a document the repository has never held. The rule I add, and it is now also a standing
rule for the council at R10: **state the domain of every absence I report, and never convert "absent
from repository state" into "does not exist" — including when the absence is mine.** I asserted a
negative twice in one session on evidence that could only support a narrower one, and both times a
member caught it.

**One note on delegation.** I sent the officer a Phase 1 commission built on the asymmetry reading,
then corrected it to the scope-defect reading mid-flight, and the correction arrived after it had
finished. It reasoned Phase 1 from a superseded premise and had to withdraw part of §3(v) in Phase 2.
The cost was real but small, because its repository findings were sound independent of the framing.
The template addition: **when I correct a premise mid-session, I state explicitly which parts of the
prior commission are withdrawn and which stand** — I sent the new premise but never said that Task 2
was now a different question until Phase 2, and the officer had to work that out for itself.

---

*Recorded by the chairman. No file under `src/`, `scripts/`, `tests/`, `.github/`, `prompts/`,
`lit-review/` or `METHODOLOGY.md` was created or modified in this session. Both seats were real
subagents (`systems-designer`, `integrity-officer`, model override `opus`); no member's voice was
performed by the chair. This design is not entered in `analytics/optimization-log.md`: it is an
operator-commissioned rule, not the council's one-idea-per-day optimization slot.*
