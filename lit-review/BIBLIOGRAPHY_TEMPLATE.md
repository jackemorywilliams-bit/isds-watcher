# Backsourced bibliography — entry template

One block per source. The four marks are the Carrying-Span Rule's entry shape
(`prompts/carrying_span_rule.md`, adopted 2026-08-03 as amended); they exist so that
compliance is countable by someone who is not the author, which is the property the
previous verification statement lacked.

**Fill `P` before you open the source.** A proposition written afterwards is a
proposition the source was recruited to.

---

## The block

```markdown
### <Case or work name>

<Full Bluebook citation of THE DOCUMENT YOU READ — not the case in the abstract —
with its date, and a URL.>

**P —** <The one sentence you are citing this source for. Written before opening it.>

**Q —** "<The source's own words that carry P.>" [<pinpoint>]

**D —** <Document + date>; <what the dispute was actually about>; <the stage cited>;
<how it came out ON THE POINT YOU CITE>; <what happened after — ONLY if P depends on
finality>.

**V —** Checked <date> at <where retrieved>. Screened: <term: count; term: count;
term: count>. <For every screened term with a NONZERO count whose occurrences are not
the source of Q, one clause in your own words saying what the source is discussing
there.> <Exit taken, if any.> <Any limitation on access, stated rather than omitted.>

**Descriptive annotation.** <~80–200 words, descriptive and evaluative.>

**Relevance to the project.** <How it fits, and what it cannot be asked to do.>
```

---

## Filling each mark

**P — the proposition.** One sentence. If it changes while you work, it is a new
proposition and the rule restarts on it. A vague `P` defeats everything downstream —
annotation vagueness is the predicted compliance-and-defeat path, and no mechanism in
this project catches it, so it is on you.

**Q — the carrying span.** The source's own words, not your paraphrase, quoted
character-exact and pinpointed. **A pinpoint alone is not compliance** — the span is
the evidence; the pinpoint only says where it is. Check whether the sentence continues
past your closing quotation mark: a quote cut before its limiting clause is a distinct
failure class this rule does not catch, so it is also on you.

If no span carries `P`, take exactly one exit and name it in `V`, **in this order**:

1. **another document in the same matter** — another opinion, order, decision or award,
   at another stage or date — then screen again. This is first because it is the exit
   that recovers a real source, and "drop it" is the cheapest thing to reach for;
2. **narrow** `P` to what the span does carry;
3. **find another source**;
4. **drop it.**

If you could not retrieve enough to look, the source is **unread**. Say so in `V` and
assert nothing from it.

**D — the card.** For any case: the dispute's actual subject matter, the stage, and the
outcome *on the point you cite*. "Joined to the merits" and "undecided" are outcomes.
Add subsequent history **only where your proposition depends on finality** — otherwise
it is an unbounded research obligation, and the finality field gets no carrying span of
its own.

**V — the verification line.** Date, where you got it, and the screen you ran with
counts. At least three terms, including **one rigid designator** — a name the field
cannot paraphrase away: TRIPS, the Trade Secrets Act, Art. 39(3), "fork in the road", a
party name — and one truncated stem. **If your proposition has no rigid designator,
write that down: the verdict is weaker.**

> **A zero is not a verdict and a nonzero is not a pass.** Zero on a descriptive word —
> try its synonym before concluding absence. A hit — go read the hit.

Then the clause that does the most work per character: **for every screened term with a
nonzero count whose occurrences are not the source of your `Q`, say in your own words
what the source is discussing there.** Worked line —

```
screened: TRIPS 0; intellectual property 0; recognition 2 — both occurrences concern
recognition and enforcement of arbitral awards, not municipal recognition of a
protected asset.
```

Without that clause a nonzero count reads as corroboration. That is the branch on which
the 2026-08-03 failure actually occurred.

---

## Worked example 1 — a real entry that took an exit

Every fact about the case below is attested at `lit-review/kim-memo.md:192-202`; the
checked-on date is the writer's own, which is what a `V` mark's date always is. Nothing
here is reconstructed, and **no span is quoted** — because no span from the 6 May 2021
opinion has been transcribed into this repository, and a template that teaches
transcription must not invent one to look complete.

```markdown
### Vanda Pharmaceuticals, Inc. v. Food & Drug Administration

No. 19-cv-301 (JDB), Mem. Op. (D.D.C. May 6, 2021), ECF No. 65
[parallel reporter citation unverified].

**P —** A U.S. court rejected Trade Secrets Act challenges to the FDA's public release
of clinical-trial information.

**Q —** *No span located.* Exit (i) taken: another document in the same matter, the
memorandum opinion of 6 May 2021, and restart at step 2. **The restart's screen and
span are not yet recorded, so this entry is not finished** — see the V mark.

**D —** Memorandum opinion, 6 May 2021; a non-party law firm's motion to intervene and
unseal the administrative record; decided on the motion; intervention permitted and
unsealing partially granted, unsealing DENIED as to the toxicology reports, and Vanda
required to identify specific interests document by document. Finality not reached — P
does not depend on it.

**V —** Screened the document originally cited, 436 F. Supp. 3d 256: trade secret 0;
confidential 0; proprietary 0; disclosure 0. P's rigid designator is "Trade Secrets
Act" and the stem "trade secret" returns nothing, so the zero is a strong verdict; that
opinion is an Administrative Procedure Act challenge to a partial clinical hold on
tradipitant and carries P nowhere. Exit (i) taken. The 6 May 2021 opinion was read as a
slip opinion via govinfo and authenticated against the public docket, checked
2026-08-03; its screen has not been run and no span from it is transcribed, so nothing
is asserted from it beyond the D mark. The parallel reporter citation remains
unverified and the case is cited in docket form pending confirmation.
```

Three things this teaches. The exit taken is the **first** one, not the cheapest — the
proposition was recoverable in the same matter, and "drop it" would have lost a source
the project now uses. The screen that produced the zero is recorded against the document
it was actually run on, not against the case in the abstract. And the entry says out
loud that it is unfinished, rather than presenting a D mark as though a span stood
behind it.

## Worked example 2 — the shape of a finished entry

**Synthetic.** The case, the span and the pinpoint below are placeholders in guillemets;
there is no such tribunal and no such award. It is here to show the shape, and it is
deliberately impossible to mistake for a citation.

```markdown
### «Claimant» v. «Respondent State»

«ICSID Case No. ARB/00/0», Award, ¶ 000 (Jan. 1, 2000), <«url»>.

**P —** «The one sentence, written before the source was opened.»

**Q —** "«the source's own words that carry P, character-exact»" ¶ 000

**D —** Award, 1 Jan. 2000; «what the dispute was about»; merits; «how it came out on
the point cited».

**V —** Checked «date» at «where retrieved». Screened: «rigid designator» 0; «truncated
stem» 0; «third term» 2 — the two occurrences of «third term» are «what the source is
discussing there», not «P».

**Descriptive annotation.** «80–200 words, descriptive and evaluative.»

**Relevance to the project.** «How it fits, and what it cannot be asked to do.»
```

---

## Before you circulate

Confirm every `Q` has a quotation and a pinpoint, every case has an outcome on the cited
point in `D`, every nonzero screened term has either produced the `Q` or been given a
referent clause, and no two entries share a `V` or `D` line verbatim.

Then run `python scripts/check_marks.py lit-review/*.md`. **Read its module docstring
for what it does and does not check** — that docstring is the single statement of the
script's scope, and its coverage depends on whether your entries use the four marks. The
CLI reports what it actually exercised on your files. What it does not exercise is
yours by hand, and whether a span carries its proposition is nobody's but a reader's.
