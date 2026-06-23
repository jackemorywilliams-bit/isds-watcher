# State of the Answer

This is the project's living, cumulative best answer-so-far to the research question.
It is the artifact the daily and weekly research is meant to **grow** — not a log of what
was done, but a structured synthesis of what the project currently believes, each claim
tied to its source(s), with what remains open held separately at the bottom.

**The research question.** ISDS cases in which (Ring 1) an intellectual-property right —
patent, trademark, copyright, geographical indication, and centrally for this project
**trade secrets and clinical-trial data** — is asserted as a "covered investment"; (Ring 2)
a **regulatory or judicial measure** is challenged as the violating conduct (often framed as
denial of justice or breach of the minimum standard of treatment); and (Ring 3) the tribunal
disposes of the case at the **jurisdictional / admissibility** stage (abuse of right,
treaty-shopping, the critical-date / reasonably-foreseeable-dispute test, shell-subsidiary
restructuring) without reaching the merits. Seed awards: *Philip Morris v Australia*,
*Eli Lilly v Canada*, *Bridgestone v Panama*; conceptual seeds: the Ferguson and Kim memos.

**How to read this document.** Every substantive claim carries an inline source. Claims the
project can state confidently from a named source are unmarked; claims that are inferred,
reconstructed from secondary coverage, or not yet verified against a primary document are
marked **[unverified]** with the reason. This is the anti-hallucination discipline applied to
the synthesis itself: a claim that cannot be sourced is not stated.

**Status:** seeded 2026-06-23 from the seed cases and the day-one daily record. Last updated:
2026-06-23.

---

## How this document and the insight ledger work (the compounding-memory controls)

The research compounds through two coupled artifacts:

1. **This document (`STATE_OF_THE_ANSWER.md`)** — the synthesis. Each session reads it first,
   then revises it: a genuinely new finding is folded into the relevant ring or sub-question
   (with its source), an open question that has been answered is moved up into the body, and
   the "Last updated" line is bumped. It is meant to get more complete and more precise over
   time, not longer for its own sake.

2. **The insight ledger (`analytics/insights.jsonl`)** — an append-only, deduplicated record
   of each genuinely new insight, one JSON object per line. It is the baseline against which
   "new" is measured: before claiming a new insight, a session checks it against the ledger,
   and if the point is already recorded, it does **not** re-log it. On a quiet day the honest
   output is "no new insight; standing watch" rather than a padded restatement of the ledger.

**Insight-ledger schema (`analytics/insights.jsonl`).** One JSON object per line (JSONL has no
comment syntax, so the schema lives here):

| Field | Type | Meaning |
|-------|------|---------|
| `date` | string `YYYY-MM-DD` | the session date the insight was first recorded |
| `thread_id` | string | the related open thread (e.g. `T01`), or `null` if none yet |
| `ring` | string | `R1`, `R2`, `R3`, `cross`, or `meta` (which part of the answer it advances) |
| `insight` | string | the durable finding, stated once, concisely |
| `sources` | array of strings | each as `"Name — URL"`; `[]` only if genuinely unsourced (then say so) |
| `confidence` | string | `verified` (primary/named source read) or `unverified` (reason in the insight text) |

A line is appended only when the insight is **new relative to every existing line**. Editing
or restating an existing line is not appending. The ledger is the dedup boundary; this
document is the synthesis the ledger feeds.

---

## Ring 1 — IP (incl. trade secrets / clinical-trial data) as a covered investment

- **The seed pattern.** Tribunals will entertain IP as a "covered investment," but whether a
  given right qualifies turns on the treaty's investment definition and, where applied, the
  *Salini* criteria (contribution, duration, risk, contribution to the host economy). The
  gates are open in principle but not automatic. (Correa & Viñuales, *Intellectual Property
  Rights as Protected Investments: How Open are the Gates?*, 19 J. Int'l Econ. L. 91 (2016);
  Mercurio, *Awakening the Sleeping Giant*, 15 J. Int'l Econ. L. 871 (2012); *Salini v
  Morocco*, ICSID Case No. ARB/00/4.)
- **Patents (seed).** In *Eli Lilly v Canada* (ICSID Case No. UNCT/14/2, Final Award 16 Mar.
  2017), pharmaceutical patents were treated as covered investments; the claim failed, but not
  for want of the IP qualifying as an investment. (METHODOLOGY.md Part II.B, citing the award.)
- **Trademarks (seed).** *Philip Morris v Australia* (PCA Case No. 2012-12, Award on
  Jurisdiction and Admissibility 17 Dec. 2015) framed trademark/brand rights as the investment;
  it was disposed of at Ring 3 (below) before the IP-as-investment merits were reached.
  (METHODOLOGY.md Part II.B.)
- **Data as IP-investment — the leading contemporary instance.** *Einarsson v Canada* (ICSID
  Case No. UNCT/20/6) is the first publicly documented ISDS case to rest a claim centrally on
  **proprietary data protected as copyright / trade secret** (offshore marine seismic data) as
  the covered investment. This extends Ring 1 from the classic registered-IP categories toward
  information-based assets — the same category the Ferguson/Kim memos flag for trade secrets
  and clinical data. (Upreti, *Data, Copyright, and Investor-State Arbitration: Insights from
  Einarsson v. Canada*, SSRN 2023 — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4328312;
  EFILA Blog, Oct. 2024 — https://efilablog.org/2024/10/06/data-as-protected-investment-in-the-background-of-einarsson-v-canada/.)
  **Caveat:** Einarsson's data is industrial seismic data in an oil-and-gas context (a
  fingerprint negative signal); it is a *structural analogue*, not a pharma/clinical-data case.
- **A new regulatory foundation for clinical data as a tradable entitlement.** China's NMPA, by
  Implementation Measures for Drug Trial Data Protection effective 15 May 2026, makes
  undisclosed clinical-trial data and marketing-authorization registration certificates formal,
  protectable, and assignable entitlements (data exclusivity up to six years; longer for rare-
  disease and pediatric drugs). This is a Ring 1 *precursor* — it creates the kind of legal
  entitlement a future claimant could assert as a covered investment — not itself a dispute.
  **[unverified]** sourced only from search-summary secondary coverage (Ropes & Gray; Arnold &
  Porter; Bird & Bird; IAM Media), no primary regulation read; see daily record 2026-06-23 §F.

## Ring 2 — A regulatory or judicial measure as the challenged conduct (weighted)

- **The seed pattern.** Two of the three seeds challenged a **court decision** (not an
  executive act) as the violating measure, framed as denial of justice / breach of the minimum
  standard of treatment. State responsibility for the judiciary requires manifest injustice;
  mere error does not meet the test. (Paulsson, *Denial of Justice in International Law* (2005);
  METHODOLOGY.md Part II.C.)
- **Judicial measure (seed).** *Eli Lilly v Canada* challenged the Canadian courts' application
  of the "promise utility doctrine" invalidating its patents, under NAFTA Article 1105, as a
  denial of justice. (METHODOLOGY.md Part II.B.)
- **Judicial measure (seed).** *Bridgestone v Panama* (ICSID Case No. ARB/16/34, Award 14 Aug.
  2020) challenged a Panama Supreme Court judgment as a denial of justice. (METHODOLOGY.md
  Part II.B.)
- **Regulatory measure (contemporary).** *Einarsson*'s challenged measure is primarily the
  regulatory regime (Canada Petroleum Resources Act and related provisions permitting forced
  disclosure of proprietary seismic data), with a Federal Court judgment (2020 FC 984) also in
  the record — so it sits closer to the regulatory than the judicial end of Ring 2. (Jusmundi,
  Judgment 2020 FC 984; daily record 2026-06-23 §A.)
- **The doctrine is live but not always IP-linked.** Denial-of-justice findings continue to
  issue (e.g. *Bachar Kiwan v Kuwait*, ICSID Case No. ARB/20/53, Award 10 Mar. 2025, France–
  Kuwait BIT), confirming Ring 2 is active — but that award has **no IP nexus** and is Ring 2
  only; it does not advance the three-ring intersection. (Jusmundi, Award 10 Mar. 2025 —
  https://jusmundi.com/en/document/decision/en-bachar-kiwan-v-state-of-kuwait-award-monday-10th-march-2025.)

## Ring 3 — Disposal at the jurisdictional / admissibility stage

- **The seed pattern.** All three seeds were disposed of before the merits — on jurisdiction
  and/or admissibility. The controlling cluster is abuse of right / treaty-shopping and the
  critical-date / reasonably-foreseeable-dispute test. (Baumgartner, *Treaty Shopping in
  International Investment Law* (2016); Byers, *Abuse of Rights* (2002); METHODOLOGY.md
  Part II.C.)
- **Abuse of right (seed).** *Philip Morris v Australia* was dismissed for abuse of right:
  the claimant restructured into a Hong Kong entity to acquire treaty rights over a reasonably
  foreseeable dispute. (METHODOLOGY.md Part II.B.)
- **Shell-subsidiary / restructuring (seed).** *Bridgestone* also raised shell-subsidiary
  misuse allegations of the *Philip Morris* type. (METHODOLOGY.md Part II.B.)
- **A different jurisdictional doctrine in the contemporary analogue.** *Einarsson*'s threshold
  objection is a **NAFTA Article 1121 waiver** defect — an admissibility-type bar of a
  *different* doctrinal character than the abuse-of-right / treaty-shopping cluster that anchors
  the *Philip Morris* line. So the contemporary near-case fits Ring 3 by *kind* (threshold
  disposal) but not by *doctrine*. **[unverified]** the Article 1121 characterization is sourced
  to Jusmundi/UNCTAD, not confirmed against the treaty text; daily record 2026-06-23 §A.
- **An emerging gap adjacent to the abuse-of-right doctrine.** *Jason Yu Song v China* (PCA Case
  No. 2019-39, Final Award 24 Jan. 2025, China–UK BIT) extends the abuse-of-right inquiry to
  **natural-person nationality planning** and exposes that Denial-of-Benefits clauses, built for
  corporate third-country nationality, do not address natural persons who change citizenship to
  access a treaty. The same structural argument could recur in an IP-as-investment restructuring.
  Not an IP case; relevant for Ring 3 doctrine only. **[unverified]** search-summary sourced (HFW;
  IFILA Blog; Jusmundi docket), no primary award read; daily record 2026-06-23 §G.

## Sub-question — Trade secrets / clinical-trial data specifically

- **The core finding to date: still no litigated case.** No publicly known ISDS case has yet
  asserted **pharmaceutical trade secrets or clinical-trial data** as the *primary* covered
  investment. The Ferguson/Kim framework remains theoretical — a prospective, structurally
  contingent risk, not a live dispute. This is an honest negative result, confirmed against the
  UNCTAD ISDS Navigator (through July 2024), italaw, and practitioner commentary. (Daily record
  2026-06-23 §C; Kim, 15 J. Marshall Rev. Intell. Prop. L. 999 (2016); Ferguson, *Trade Secrets
  at Risk*.)
- **The nearest analogue is structural, not direct.** *Einarsson* (proprietary data / trade-
  secret layer + regulatory measure + threshold objection) is the closest real case, but the
  asset is industrial seismic data, not pharmaceutical clinical data, and the regulatory
  mechanism differs fundamentally. (Daily record 2026-06-23 §§A, C.)
- **The unresolved doctrinal questions if such a case arises.** How a tribunal would (a)
  characterize pharmaceutical test data as a "covered investment," (b) value it, and (c) treat a
  regulatory measure permitting generic reliance on that data as the "violation," all remain
  unanswered in the public case law. (Daily record 2026-06-23 §C.)
- **A treaty hook exists but is unused.** USMCA Chapter 20 test-data-exclusivity obligations
  could in principle underpin such a claim, but none has been filed. (CRS, *USMCA: Intellectual
  Property Rights (IPR)*, IF11314 — https://www.congress.gov/crs-product/IF11314; daily record
  2026-06-23 §C.)

## Cross-cutting — the forum landscape

- **The flagship North-American forum is closing.** USMCA (in force 1 July 2020) eliminated
  ISDS between Canada and the United States; the three-year legacy period expired **30 June
  2023**. No successor to *Eli Lilly v Canada* can now be filed under the principal North-
  American framework; pre-existing legacy claims (e.g. *Einarsson*) remain pending. Mexico
  retains a narrowed ISDS under USMCA Chapter 14 (mainly covered-sector government contracts;
  local-remedy exhaustion and a 30-month wait otherwise). (CRS, *USMCA: Investment Provisions*,
  IF11167 — https://www.congress.gov/crs-product/IF11167; Kluwer Arbitration Blog, *ISDS Under
  the USMCA: The First Three Years at a Glance*, Nov. 2023 —
  https://arbitrationblog.kluwerarbitration.com/2023/11/25/isds-under-the-usmca-the-first-three-years-at-a-glance/;
  Norton Rose Fulbright, *Major changes for ISDS in USMCA*; daily record 2026-06-23 §B.)
- **The trigger doctrine that animated *Eli Lilly* is itself largely gone.** Canada's Supreme
  Court relaxed the promise utility doctrine in *AstraZeneca Canada Inc. v Apotex Inc.*, [2017] 1
  SCR 536 (30 June 2017), so the regulatory condition behind that claim has substantially
  receded. (SSRN, Baker & Geddes, *The Incredible Shrinking Victory: Eli Lilly v. Canada* —
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3012538; daily record 2026-06-23 §B.)
- **Consequence for the research question.** If the three-ring structure recurs in pharma, it
  will most likely arise under **older BITs or the CPTPP**, against non-North-American states —
  not under NAFTA/USMCA. (Daily record 2026-06-23 §B.)

---

## Open questions (the live research agenda)

These map to the open threads in `state/research_log.json`. Move an item up into the body above
when it is answered with a source.

1. **The *Einarsson* award (T01).** Pending since the 3–13 March 2025 merits hearing (Calgary).
   When it issues: how does the tribunal define data/trade-secrets as a covered investment; does
   the Article 1121 waiver objection succeed; and how is the regulatory measure characterized?
   Escalate immediately on issuance. (Daily record 2026-06-23 §A, Part III.)
2. **First litigated trade-secret / clinical-data case (T02).** Track any new filing under a BIT
   or the CPTPP that asserts pharmaceutical trade secrets or clinical-trial data as the primary
   investment. This is the project's central prospective question.
3. **Surviving pharma-IP forums (T03).** Identify whether any non-North-American BIT or CPTPP
   three-ring case has been filed since 2020; monitor Mexico / USMCA Art. 20.48 clinical-data
   non-implementation for Chapter 31 or Annex 14-D proceedings. (UNCTAD Navigator advanced
   search is the right tool.)
4. **China NMPA aftermath (T04).** Watch whether the new 2026 data-exclusivity entitlements are
   later restricted or unevenly applied in a way that could seed a Ring 1 claim under China's BIT
   network. Verify the 2026 Measures against a primary source before relying on the detail.
5. **Denial-of-Benefits reform (T05).** Track UNCITRAL Working Group III Draft Article 17
   (denial of benefits, extended scope) and any IP-related case that triggers the abuse-of-right
   / nationality-planning doctrine surfaced by *Jason Yu Song*.

## Verification debt (to clear at the next human review)

Items currently carried as **[unverified]** that should be confirmed against a primary source:
the China NMPA 2026 Measures (Ring 1, sub-question hook); the *Jason Yu Song* award particulars
(Ring 3); and the *Einarsson* Article 1121 waiver characterization (Ring 3), to be confirmed
against the NAFTA text and the award when it issues. The human-review checkpoint
(`HUMAN_REVIEW.md`) is where this debt is audited and logged.
