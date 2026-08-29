# Operator-side gap bridge — 2026-08-29 daily council

**What this is.** The scheduled cloud council session has no fetch capability (egress 403 at the
proxy, twenty-eighth consecutive day), and its 2026-08-29 record routes every unreachable gap
"operator-side." This file is that operator-side retrieval: the operator (Emory) ran Claude Code with
live web access — a different client on a different network — and worked the day's open
`GAP-UNRESOLVED` slugs against public primary and secondary sources.

**Status discipline, stated once.** Nothing here is marked verified: §4 of the Bounded Change
Protocol reserves the verification ledger to the operator (`scripts/verify.py mark`), and no automated
path may. Each finding is tagged **OBSERVED** (I read the primary document), **REPORTED** (secondary
source only), or **OPEN** (not reached). A docket line is never a holding; a secondary report of a
disposition is not the disposition's text. These are inputs for the operator to fold into
`STATE_OF_THE_ANSWER.md` and the candidate-claim ledger, not findings self-asserted into either.

---

## icsid-2022-arbitration-rules-rule-41-48-provision-text (N15) — MOVED

The 2026-08-29 window read ICSID's ARB/12/1 docket citing **"ICSID Arbitration Rule 43(1)"** for a
discontinuance-noting order, and flagged that the edition was unidentified.

- **REPORTED.** Under the **2006 ICSID Arbitration Rules**, Rule 43 is "Settlement and Discontinuance";
  Rule 43(1) provides that where the parties agree to discontinue before the award, the Tribunal (or
  the Secretary-General, if the Tribunal is not yet constituted) shall, at the parties' written
  request, take note of the discontinuance in an order. That is exactly a discontinuance-noting order,
  and it confirms the docket's own reading.
- **Which edition.** ICSID Convention Art. 44: the Rules in effect at the date of the parties'
  **consent** apply (not the registration date). A 2012-registered case consented under the 2006
  Rules, so "Rule 43(1)" is the 2006 Rule. In the 2022 Rules, discontinuance renumbers out of Rule 43.
- **Corollary.** This confirms the council's earlier **refusal** of the engine assertion that "Rule 43
  addresses 'Preliminary Objections'" (`analytics/daily-research/2026-08-24.md:530`): false for the
  2006 Rules, where Rule 43 is discontinuance. The refusal stays correct.
- **What is NOT closed.** The full 2022 Rules 41–48 text (the slug's literal target, relevant to the
  MLLM/Rule 41 register work) is public on icsid.worldbank.org but is not pasted here. In the 2022
  Rules, "Manifest lack of legal merit" is **Rule 41**.

Sources: <https://icsid.worldbank.org/procedures/arbitration/convention/process/discontinuance/2006> ·
<https://icsid.worldbank.org/procedures/arbitration/convention/discontinuance/2022>

## tethyan-copper-arb-12-1-annulment-outcome — CLOSED as reported

`STATE_OF_THE_ANSWER.md` had recorded "THE ANNULMENT OUTCOME REMAINS UNOBSERVED." It is now reported.

- **REPORTED.** Pakistan applied for annulment of the 12 July 2019 award on **8 November 2019**. The ad
  hoc Committee held a hearing in May 2021; the annulment proceeding was **suspended 18 April 2022** at
  the parties' agreement, extended 18 July and 18 October 2022. In **December 2022** the parties
  **jointly requested discontinuance**: Pakistan **withdrew** its annulment application and asked the
  Committee to cease drafting its annulment decision. The Committee issued the **Order on
  Discontinuance on 6 January 2023** — the same instrument, date and organ ("The Committee") the
  council's window read.
- **The outcome, stated at its true scope.** The annulment was **abandoned by discontinuance following
  settlement**, not decided on the merits: the award was neither annulled nor upheld on the annulment
  grounds, which were never ruled on. The discontinuance is settlement-driven — the March 2022 Reko
  Diq settlement (Antofagasta paid ~US$900m plus interest and exited the project; the Reko Diq disputes
  agreed finally resolved). So the docket's "discontinuance" **is** the annulment outcome: a
  withdrawal, not a disposition of the annulment application.
- **Still unobserved / not reachable.** The annulment grounds pleaded, and any Committee reasoning
  (there is none — drafting was stopped). The Tethyan award paragraphs (¶¶ 1283, 1288, 1327–1333) stay
  redacted.

Sources: LSE Law Review, "Reflections on Tethyan Copper v Islamic Republic of Pakistan"
<https://lawreview.lse.ac.uk/articles/515/> · Jus Mundi case file · TDM/OGEL doc key 32761.

## icsid-arb-12-1-block-c-header — "(c) Revis…" — OPEN (not reachable by secondary sources)

- **OPEN.** italaw's ARB/12/1 case page lists only the **(a) Original Proceeding** (provisional
  measures 2012; Decision on Jurisdiction and Liability and Decision on the Application to Dismiss,
  both 10 Nov 2017; Award 12 Jul 2019) and **(b) annulment/post-award** documents (enforcement 2019;
  stay decisions; Order on Discontinuance 6 Jan 2023). **No third lettered proceeding beginning
  "Revis" appears in any public secondary source I reached.** By ICSID nomenclature the most likely
  completion is a **Revision Proceeding** (Convention Art. 51), but I cannot confirm one exists.
- The lettered-block structure ("(a)/(b)/(c)") is a feature of the **ICSID case-detail SPA** the
  council reads via its relay; my web tools reached italaw/Jus Mundi but not that page's rendered
  blocks. **This gap is better closed by the council's own row 0829-R1** (`find (c) Revis`), or by an
  operator-side direct read of the ICSID case-detail page. I add nothing that would let a reader treat
  "(c)" as identified.

Source checked: <https://www.italaw.com/cases/1631>

## ejiltalk-roberts-islands-of-persuasion-body-and-date — CLOSED, and retire as off-theme

The title "UNCITRAL and ISDS Reform (Hybrid): Islands of Persuasion" was banked 2026-08-28 as an
undated listing title under G10.

- **OBSERVED (post fetched).** Published **18 March 2022**, by **Anthea Roberts and Taylor St John**,
  on EJIL: Talk!. (The council's prior *search-synthesis* had guessed "March 14, 2022" — the fetched
  post reads 18 March, which is precisely why search-synthesis is barred: the two differ.)
- **Body.** Commentary on the hybrid February 2022 UNCITRAL Working Group III session, applying Nicole
  Deitelhoff's "islands of persuasion" to argue moments of reasoned deliberation emerged (tribunal
  structure, permanent-court comparisons, adjudicator qualifications). **No IP, trade-secret or
  clinical-data nexus** — it is ISDS-reform-process commentary, outside this project's intersection.
- **Disposition of the lead.** Date and authors resolved; content off-theme. Retire as a
  monitored-author artifact with no on-theme content, not as a pending retrieval.

Source: <https://www.ejiltalk.org/uncitral-and-isds-reform-hybrid-islands-of-persuasion/>

## icsid-arb-23-3-no-published-decisions-on-docket — premise FALSIFIED as reported

- **REPORTED.** ARB/23/3 is **JLL Capital, S.A.P.I. de C.V. v. Republic of Honduras** (Central
  America–Mexico FTA 2011; financial/insurance sector). It **has published decisions**: a **Decision
  Dismissing Respondent's Preliminary Objections Pursuant to ICSID Arbitration Rule 41 (21 Dec 2023)**
  and a **Decision on the Respondent's Objection Pursuant to ICSID Arbitration Rule 42(5) (3 Sept
  2024)**; a jurisdiction hearing was set for 19–21 Nov 2025. So "no published decisions on docket" is
  false on the merits as of these dates. (If the slug was scoped to a specific rendered surface, the
  narrow "not found in this surface" form may still stand — but decisions exist.) **Off-theme** for the
  project (financial sector, no IP nexus).

Sources: <https://www.italaw.com/cases/10114> · ICSID news release for ARB/23/3 · Jus Mundi.

## philip-morris-uruguay-arb-10-7-pleaded-covered-investment — CLOSED as reported, and it is on-theme

- **REPORTED.** Claimants (Philip Morris Brands Sàrl, Philip Morris Products S.A., Abal Hermanos S.A.)
  pleaded as covered investments their immovable and movable property, **shares** (the Abal Hermanos
  shareholding), and **intellectual-property rights — the ownership of several tobacco trademarks** and
  the associated brand assets/goodwill — plus manufacturing facilities for the Uruguayan market. The
  Tribunal (Bernardini, Born, Crawford; Award 8 July 2016) **recognised the trademarks/IP as covered
  investments** but **dismissed all claims** (Uruguay's tobacco-control measures were legitimate
  public-health regulation; no FET / legitimate-expectations / expropriation breach).
- **Why it matters here.** This is a tribunal expressly treating **trademarks/IP as a covered
  investment** — squarely the project's intersection — while denying protection on the merits. It is a
  strong on-theme comparator, distinct from Kim's clinical-data line.

Sources: <https://www.italaw.com/cases/460> · UNCTAD ISDS Navigator case 368 · Award (8 Jul 2016).

## hela-schwarz-art9-jurisdiction-or-admissibility (N4) — MOVED materially; open tension resolved in direction

- **OBSERVED (Procedural Order No. 3 read in full).** In Hela Schwarz GmbH v. China (ICSID ARB/17/19,
  2003 China–Germany BIT), China raised four preliminary objections: (1) jurisdiction *ratione
  materiae*; (2) **Art. 9(1)–(2) BIT** (the cooling-off / amicable-settlement clause — an
  admissibility/jurisdiction objection); (3) **Art. 9(a) Protocol**; (4) **Art. 9(c) Protocol** (the
  concurrent-proceedings clause; the Claimant argued it is **not** a fork-in-the-road/no-U-turn clause
  and permits national-court recourse). By **Procedural Order No. 3 (17 December 2018,** President Sir
  Daniel Bethlehem QC): bifurcation **denied**, and "the Respondent's objections to jurisdiction and
  admissibility are **joined to the proceedings on the merits**." So the Art. 9 objections were not
  preliminary knock-outs.
- **REPORTED (Award).** The final **Award issued 10 December 2025**; secondary reporting (SEAL Oct–Dec
  2025 round-up) has the tribunal addressing the jurisdictional objections in detail and then
  **examining the substantive claims** (indirect expropriation, denial of justice, FET).
- **This resolves the STATE tension.** `STATE_OF_THE_ANSWER.md` carried an open question about
  search-engine prose describing the case as dismissed on "jurisdiction **and merits** grounds," i.e.
  that the Art. 9 gates did **not** dispose of the whole case. That direction is now supported: the
  Art. 9 objections were joined to the merits (2018) and the 2025 Award reached the merits.
- **Still open / not reached.** The Award's exact ruling on each Art. 9 objection and the ultimate
  dispositif — the Award text was not cleanly extractable this pass. This is the residue for an
  operator-side read of the 10 Dec 2025 Award (italaw / icsidfiles DS11402).

Sources: PO No. 3, <https://www.italaw.com/cases/documents/6663> (PDF italaw11394) · SEAL round-up
Oct–Dec 2025 · Jus Mundi (Award 10 Dec 2025).

## icsid-mllm-finding-column-value-codebook — CLOSED as reported

The council's MLLM register carries a **"Finding that Claim is Manifestly Without Legal Merit"** column
with observed values **No / Partial / _** (undecoded).

- **REPORTED codebook.** ICSID's own outcome taxonomy for Rule 41(5)/Rule 41 objections is
  upheld-in-full / partially upheld / rejected (its statistics report **7 / 4 / 26** respectively).
  Mapping the column:
  - **"No"** = the tribunal found the claim is **not** manifestly without legal merit → the objection
    was **rejected** (a rejection is without prejudice to a later objection or to the merits).
  - **"Partial"** = objection **partially upheld** → some claims dismissed as manifestly without merit,
    others continue.
  - **"_"** = **no recorded finding** → most plausibly no decision on the objection (withdrawn, case
    discontinued, or pending); undefined, and it is neither "No" nor "Partial." This is the honest
    reading of the fourth state, not a decode of a value ICSID publishes.
- **Note on the council's caution.** "No" does correspond to the objection failing (claim not
  manifestly without merit). The deeper standing caution holds regardless: a register value is a
  docket-summary field, never the decision's text or a holding.

Sources: <https://icsid.worldbank.org/procedures/arbitration/convention/manifest-lack-of-legal-merit/2022>
· UNCITRAL secretariat note on the MLLM procedure · Kluwer/Lexology commentary.

## icsid-subject-of-dispute-vocabulary-enumeration — PARTIAL

- **OPEN/partial.** ICSID's case database uses controlled vocabularies for **Economic Sector** and
  subject matter, enumerated in "The ICSID Caseload — Statistics" (e.g. Oil, Gas & Mining; Electric
  Power & Other Energy; Construction; Transportation; Information & Communication; Finance; Water,
  Sanitation & Flood Protection; Agriculture, Fishing & Forestry; Services & Trade; Tourism; etc.).
  The **full, exact enumeration** is sourceable from that report but I did not pull the complete list
  this pass. Operator can lift it verbatim from the current statistics PDF; I flag it rather than
  paraphrase a partial list as complete.

Source to pull: ICSID, "The ICSID Caseload — Statistics" (current issue), icsid.worldbank.org.

---

### Summary for the operator

| Slug | Status after this pass |
|---|---|
| rule-41-48-provision-text (N15) | Rule 43(1)=2006 discontinuance, edition resolved; 2022 41–48 text still to pull |
| tethyan annulment outcome | CLOSED as reported — discontinued on Pakistan's withdrawal following settlement |
| arb-12-1 block (c) Revis | OPEN — not in secondary sources; use council row 0829-R1 or a direct ICSID-page read |
| ejiltalk islands-of-persuasion | CLOSED — 18 Mar 2022, Roberts & St John, off-theme; retire the lead |
| arb-23-3 no published decisions | premise FALSIFIED — JLL v Honduras has Rule 41 (2023) and 42(5) (2024) decisions |
| philip-morris covered investment | CLOSED — trademarks/IP + Abal shares pleaded and recognised as covered; claims dismissed |
| hela-schwarz art 9 (N4) | MOVED — Art. 9 objections joined to merits (PO No.3, 2018); 2025 Award reached merits; dispositif still to read |
| mllm finding-column codebook | CLOSED — No=objection rejected; Partial=partly upheld; _=no recorded finding |
| subject-of-dispute vocabulary | PARTIAL — sourceable from ICSID Caseload Statistics; full list not pulled |

None of the above is entered in the ledger or in `STATE_OF_THE_ANSWER.md` by this file — that is the
operator's to do, under §4.
