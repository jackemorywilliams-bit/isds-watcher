# The validation record (2026-09-13)

Cited as **the validation record (2026-09-13)**. This file is
`analytics/locked_set/VALIDATION_RECORD.md`.

---

## 0. Provenance — what this replaces, and why it does not wear its name

This record **replaces** the document this repository cites throughout as **"the
R2.1 record"**: the stated source of the locked validation set's design — its nine
categories, its 54 named candidate matters, its tier rules, its acceptance criteria
V1–V6, its stop-publication rules S1–S4, its stability thresholds and its triage
costing table.

**The R2.1 record has never existed as a file on any branch of this repository.**

The check, run at the commit this record was drafted against:

```
git log --all --diff-filter=A --name-only --pretty=format: | sort -u | grep -i r2
```

returns **nothing** — no path ever added to this repository, on any branch, in the
whole of the reachable history, has `r2` in its name. The coordinating seat also
searched the working tree, this project's session transcripts, the cloud routines
and the operator's document folders. It is not there either. The document was
reasoned from and cited; it was never committed.

**The loss is not concealed and the name is not reused.** A document that never
existed must not be silently satisfied by a different document wearing its name:
that would convert a documented absence into an undetectable substitution, and the
record of the loss is itself evidence this project needs. "R2.1" therefore survives
in two places only — inside historical narrative (`analytics/daily-research/*`,
`analytics/*-2026-08-*.md`, the special-session record), which is **not edited**,
because editing a record of what was lost falsifies the record of the loss; and
inside this provenance header.

### The authority for re-deriving it

The operator's delegation of 2026-09-13, quoted verbatim, typographical errors
included, as the written authority:

> "dont be fucking lazy whatever is lost isw lost becuase of you, figrue it outr and
> bridge tghe gaps, make the judgement calls by convening the councl and undertsand to do
> it as efficiently as possible maximizing token usage and update me when all is updated,
> use your judgement to make the required fixes dont tell me to do soemthing myself that
> you yourself a. fucked up and b. orginally took on to begin wiht proactivley"

Under that delegation the council ruled (RULING 1, rulings of the chair,
2026-09-13) that it re-derives the candidate list rather than reconstructing the
lost record.

### On the face of this record

1. **A seat chose the candidate matters in §3 under delegated authority.** They are
   one analyst's nominations, not the operator's, and not a recovered list.
2. **The operator may substitute any row freely, at any time, without stating a
   reason.** No row in §3 has standing against his substitution.
3. **The original R2.1 record was never under version control on any branch.**
4. **No row in §3 is a label, a score, or a finding.** Every row is a LEAD. Per
   §3's binding constraints, no item enters `items.json` on this record's authority.
5. **The set is short of its design target, and by how much, per category.** The
   target is nine categories × six matters = 54. **Thirty-eight rows are nominated:
   category 1 — 6 of 6; category 2 — 2 of 6; category 3 — 6 of 6; category 4 — 6 of
   6; category 5 — 6 of 6; category 6 — 6 of 6; category 7 — 6 of 6; category 8 — 0
   of 6; category 9 — 0 of 6.** Sixteen rows are open, under gaps `G-1` and `G-2`
   (§3.12). Categories 8 and 9 are empty **by decision**: their item text *is* the
   headline, so nominating one from memory would fabricate the field the coder reads.
   Category 2 is short because every matter this repository knows in it is in a
   development set. **Nothing was padded to reach six.**
6. **THE REMOVAL OF THE SIX ANCHOR MATTERS IS A FINDING, NOT A CASUALTY OF
   BOOKKEEPING.** *Eli Lilly and Company v. Government of Canada*, *Bridgestone
   Licensing Services, Inc. v. Panama*, *Philip Morris Asia Limited v. Commonwealth
   of Australia*, *Philip Morris Brands SARL and others v. Uruguay*, *Apotex Inc. v.
   United States* and *Hela Schwarz GmbH v. People's Republic of China* are
   unavailable to this validation set **precisely because they are the classifier's
   development seeds and probe referents** — the instrument was built on them, so
   they cannot be used to test it. It follows, and it is stated here rather than
   inferred later, that **this set can never evidence the instrument's performance on
   the six matters the project most cares about.** That limitation attaches to
   **every grade this set ever moves**, and belongs in the limitations of any such
   grade — on its face, not in a footnote.

---

## 1. What survives in the repository — verified line by line, not re-derived

Re-deriving something the repository already holds is fabrication dressed as
recovery. Each survivor below was opened and read at
`origin/main` = `66df2d2`, and is quoted with its own pinpoint. **The line numbers
in this section are as of `66df2d2`**. Two amendments on this same branch lengthen
the tier-P bullet — RULING 2 (¶ 1 anchor) takes it from 6 printed lines to 14, and
the chairman's G-3 ruling (tier P redefined by criterion; the structural-ordinal
anchor) takes it to 32 — so every `SCHEMA.md` citation below line 51 shifts by
**+26** in total. Both the original and the final numbers are given where the shift
applies, and every final number below was re-read against the amended file.

| Element | Status | Pinpoint (at `66df2d2`) | Pinpoint (after RULING 2 + the G-3 ruling) |
|---|---|---|---|
| Nine categories, with definitions | **SURVIVES** | `SCHEMA.md:74` (heading), `:76-84` (the nine) | `:100`, `:102-110` |
| Six-each / twenty-positives structure | **SURVIVES** | `SCHEMA.md:74` | `:100` |
| P / S / C tier rules | **SURVIVES** | `SCHEMA.md:43-55` (P at `:46-51`, as twice amended; S at `:52-53`; C at `:54-55`) | `:43-81` (P at `:46-77`; S at `:78-79`; C at `:80-81`) |
| `labels.json` field set | **SURVIVES** | `SCHEMA.md:57-72` (JSON block `:59-67`) | `:83-98` (JSON block `:85-93`) |
| Blind commit order | **SURVIVES** | `SCHEMA.md:14-20`, enforced by `scripts/check_lock.py` (wired at `.github/workflows/pipeline-guards.yml:140,160`, per `SCHEMA.md:22-24`) | unchanged / `:22-24` |
| Disjointness constraints | **SURVIVES** | `SCHEMA.md:86-94` | `:112-120` |
| 20×10 stability design + four blocking thresholds | **SURVIVES VERBATIM** | `SCHEMA.md:105-107` | `:131-133` |
| S4 stop-publication rule | **SURVIVES IN SUBSTANCE** | `SCHEMA.md:107-109` | `:133-135` |
| Triage per-call cost | **SURVIVES AS A COMMITTED CONSTANT** | `src/config.py`, `TRIAGE_COST_PER_CALL_USD = 0.0014` | unchanged |
| **The 54 named candidate matters** | **LOST** | — | — |
| **V1–V6 acceptance criteria; S1–S3** | **LOST** | — | — |

**Correction to the ruling's own citations, filed against this seat's instruction
rather than around it.** RULING 1's survivor table cites `SCHEMA.md:75-83`,
`:45-54`, `:14-20`/`:56-71`, `:87-89`, `:106-107` and `:108-109`. Re-measured at
`66df2d2`, four of those ranges are off by one line or truncate the element they
name (the nine categories run `:76-84`, not `:75-83`; the tier rules run `:43-55`;
the `labels.json` section runs `:57-72`; the disjointness paragraph runs `:86-94`;
the stability sentence begins at `:105`, not `:106`; S4's sentence begins at
`:107`). The **content** the ruling identified survives in every case and no
survivor was lost or added by the correction. The ranges above are the measured
ones and supersede the ruling's, per taxonomy entry 25 — work from a freshly
measured list at the executing commit, never from a remembered one.

### The four blocking thresholds, transcribed verbatim

From `SCHEMA.md:105-107`:

> Stability: 20 items × 10 runs; blocking thresholds per the R2.1 record (decision
> flip > 0.10, mean score range > 10, any range > 20, silent-fallback rate > 0.05).

These four numbers are **carried, not re-derived**: they are read off a committed
file, not remembered. The clause "per the R2.1 record" attributes them to the lost
document; the numbers themselves are in `SCHEMA.md` and are therefore preserved.
The 20×10 design is preserved by the same sentence.

### S4, in substance

From `SCHEMA.md:107-109`:

> Acceptance V1–V6 and stop-publication S1–S4 per the R2.1 record; S4 (zero
> positives reach 40 on the production path) is the current state of the system and
> the reason the fill-floor is suspended.

S4's **content** — zero positives reach 40 on the production path — is preserved on
the face of `SCHEMA.md`. Its identifier, its ordering among S1–S3, and any threshold
or tolerance it carried are not.

---

## 2. What is LOST and is NOT reconstructed

**The 54 named candidate matters are lost.** §3 below is a new list drafted by a
seat in 2026, not a recovery of theirs. No claim is made that any row in §3 was in
the lost record, and no claim is made that any row of the lost record is absent
from §3. Those two lists cannot be compared, because one of them no longer exists.

**V1–V6 and S1–S3 are lost and are not re-derived under their own names.**

Rebuilding six acceptance criteria and three stop-publication rules from a
remembered number set **would fabricate the acceptance bar itself.** That is
strictly worse than having no acceptance bar at all: an instrument with no bar
reports an uncalibrated result and says so, while an instrument that passes a
fabricated bar produces a *validated-looking* result with no provenance, and no
later reader — the operator, the recipient, an external auditor — could tell the
difference from the artefact. The number that decides whether this project's
classifier is fit to publish must not be a number someone remembered.

### The replacement schedule — drafted by another seat, not here

A new, smaller, pre-registered schedule is being drafted under **new prefixes that
cannot be confused with the originals**:

- **`ACC-1 … ACC-n`** — acceptance criteria.
- **`HALT-1 … HALT-n`** — stop-publication rules. `HALT-1` carries S4's preserved
  content, because that content is *preserved* (`SCHEMA.md:107-109`), not
  remembered.

The 20×10 stability design and its four thresholds are transcribed into that
schedule from `SCHEMA.md:105-107` and marked **carried, not re-derived**.

**Seat: systems-researcher drafts. Integrity-officer reviews. Chairman adopts.**
It is committed **before the first label is coded**, as a pre-registration, and per
taxonomy entry 34 it states only what the repository supports and marks anything
inferred as inferred.

### PLACEHOLDER — reserved, deliberately empty

> ### 2.1 `ACC-1 … ACC-n` and `HALT-1 … HALT-n`
>
> **Not written here. Reserved for the systems-researcher's pre-registered
> schedule.** This analyst seat drafted the candidate list in §3 and therefore holds
> a stake in what the acceptance bar says; it does not write the bar. Any criteria
> appearing in this section that are not the systems-researcher's committed,
> integrity-reviewed, chairman-adopted schedule are void.
>
> Until that schedule is committed, **this instrument has no acceptance criteria**,
> and no seat may report the locked set as passing or failing anything.

---

## 3. The candidate list — nine categories, six matters each (design target)

**Seat: research-analyst drafted this section under the delegated authority quoted
in §0. Integrity-officer certifies before a single row is committed to
`items.json`. Chairman adopts.**

### 3.0 Binding constraints on every row in this section

- Each row carries **only**: category, matter caption, forum/tribunal, candidate
  primary locator, tier (P/S/C), and which ring the matter exercises. Descriptive.
  Nothing else.
- **No label. No score. No band.** No `L_theme`, no `L_band` — not provisionally,
  not in a comment, not "for review". **No rationale that argues toward a verdict.**
  **No content-selected excerpt.**
- **No item enters `items.json` on this record's authority.** Every row is a **LEAD**.
  A lead becomes an item only when its primary document is retrieved with a pinpoint
  and logged in `RETRIEVAL_LEDGER.md`.
- The carrying-span rule (2026-08-03 as amended) is untouched by this section and
  binds every proposition later drawn from any of these documents.
- Rows whose host is absent from `scripts/fetch_relay.py` `ALLOWED_HOSTS` are marked
  **unverified locator** — this council cannot confirm the URL resolves.
- "Ring exercised" is a **descriptive** note of which of the three rings
  (`prompts/classifier.txt:35` R1 IP-as-investment; R2 judicial/regulatory measure;
  R3 jurisdiction/admissibility) the matter's own subject touches. It is not a
  prediction, not a score, and not a label.

### 3.1 Tier assignment — gap `G-3`, raised by this drafting and RULED THE SAME DAY

This drafting found that `SCHEMA.md`'s tier P enumerated seven **host families** —
ICSID, PCA, italaw, Curia, BAILII, UN RIAA, WTO — in which United States federal and
state court opinions appeared nowhere, while being neither S (paywalled/headline-only)
nor C (Ferguson/Kim). Category 5 ("Domestic trade-secret litigation, no state/treaty
nexus") is composed almost entirely of such documents. Nine rows were committed
`UNASSIGNED` and the defect was filed as gap **`G-3`** rather than papered over by
stretching tier P to a host the schema did not name.

**The chairman ruled `G-3` on 2026-09-13 and it is implemented here. Tier P is
redefined BY CRITERION, not extended by host list — the enumeration was the defect.**
Tier P is now the text of a public primary legal instrument issued by a court,
tribunal or treaty body and published by that body or by an authorised public
repository; the host list is expressly **non-exhaustive**; and **authorship governs,
not host**, so commentator-authored material is C or S wherever it is hosted
(`SCHEMA.md:46-77`). The anchor generalises in the same ruling to the document's
**first printed structural ordinal** under a fixed three-limb priority.

**The nine rows are therefore committed at tier P**, each carrying
`anchor: undetermined — resolved at retrieval`. Which limb governs is a fact about
the document, knowable only with the document in hand. **A row may not be moved to
tier S before retrieval: falling to limb (3) is a finding, not a forecast.**

**The chairman's copyright basis, recorded as he instructed.** His ground for US
opinions is that they are government edicts carrying no copyright, **citing by name
*Banks v. Manchester* and *Georgia v. Public.Resource.Org***. **Both citations are
his, both are UNVERIFIED against any source in hand, and neither is presented here as
verified** — they are to be verified at retrieval, and until then the criterion in
`SCHEMA.md` stands on its own terms without them. He notes, and this record carries
it, that tier P's most exposed members on access terms are actually **BAILII and
italaw**, which impose their own terms of use independent of copyright.

### 3.2 Category 1 — IP + ISDS + administrative state measure

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 1-01 | Theodore David Einarsson, Harold Paul Einarsson and Russell John Einarsson (on behalf of Geophysical Services Incorporated) v. Government of Canada | ICSID (NAFTA ch. 11), Case No. UNCT/20/6 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=UNCT/20/6` | P | R1 (copyright in seismic data as the asserted investment), R2 (regulatory disclosure regime and Canadian court judgments), R3 |
| 1-02 | Les Laboratoires Servier, S.A.S. and others v. Republic of Poland | UNCITRAL (ad hoc) | `italaw.com` — case page for this caption (numeric case id **not verified**) | P | R1 (pharmaceutical marketing authorisations pleaded as the investment), R2 (administrative withdrawal) |
| 1-03 | Merck & Co., Inc. v. Republic of Ecuador | PCA Case No. 2012-10 (US–Ecuador BIT, UNCITRAL) | `pca-cpa.org` — case page for this caption | P | R1 (trademark), R2 (domestic court judgment), R3 |
| 1-04 | Shell Brands International AG and Shell Overseas Holdings Ltd v. Republic of Nicaragua | ICSID Case No. ARB/06/14 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/06/14` | P | R1 (trademark seized in execution), R2 (judicial/administrative measure) |
| 1-05 | Huawei Technologies Co., Ltd. v. Kingdom of Sweden | ICSID Case No. ARB/22/2 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/22/2` | P | R1 (telecommunications licences; ICSID's own subject label is "Telecommunication license agreements"), R2 (regulatory exclusion and its judicial review) |
| 1-06 | Grand River Enterprises Six Nations, Ltd. and others v. United States of America | UNCITRAL (NAFTA ch. 11) | `italaw.com` — case page for this caption (numeric case id **not verified**) | P | R1 limb is brand/goodwill rather than a registered IP right; R2 (state regulatory escrow statutes) |

### 3.3 Category 2 — IP + ISDS with a negative investment/jurisdiction holding

**This category cannot be filled, and the reason is the finding.** Every matter this
repository knows that fits it — *Apotex Inc. v. United States* (2013 jurisdictional
award), *Philip Morris Asia v. Australia* (abuse of right), *Philip Morris Brands v.
Uruguay*, *Eli Lilly v. Canada*, *Hela Schwarz GmbH v. China* — is in a development
set and is named as a collision in §3.11. They are **replaced, not dropped**, so far
as replacements exist; two licence-as-investment matters below carry the category's
structural shape with an **expressly weak Ring 1**, and four slots are left open
under gap **`G-1`** rather than filled with matters this seat cannot source.

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 2-01 | Emmis International Holding, B.V. and others v. Hungary | ICSID Case No. ARB/12/2 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/12/2` | P | R1 limb is a radio broadcasting licence, **not an IP right**; R3 (whether the licence is a covered investment) |
| 2-02 | Cortec Mining Kenya Ltd and others v. Republic of Kenya | ICSID Case No. ARB/15/29 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/15/29` | P | R1 limb is a mining licence, **not an IP right**; R3 (legality/investment definition) |
| 2-03 … 2-06 | — | — | — | — | **OPEN — gap `G-1`** |

### 3.4 Category 3 — IP dispute, no investment-treaty claim

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 3-01 | InterMune UK Ltd. and others v. European Medicines Agency | General Court of the European Union, Case T-73/13 | `curia.europa.eu` — **unverified locator** | P | R1 vocabulary (clinical-trial data, commercial confidentiality); **no R2 treaty measure, no R3** |
| 3-02 | AbbVie Inc. and AbbVie Ltd v. European Medicines Agency | General Court of the European Union, Case T-44/13 | `curia.europa.eu` — **unverified locator** | P | R1 vocabulary (clinical-trial data disclosure); no R2, no R3 |
| 3-03 | PTC Therapeutics International Ltd v. European Medicines Agency | General Court of the EU, Case T-718/15; Court of Justice, Case C-175/18 P | `curia.europa.eu` — **unverified locator** | P | R1 vocabulary (regulatory data, Policy 0070); no R2, no R3 |
| 3-04 | Vanda Pharmaceuticals, Inc. v. Food & Drug Administration | US District Court for the District of Columbia / DC Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (clinical data, exclusivity); no R2, no R3 |
| 3-05 | Vanda Pharmaceuticals, Inc. v. United States, No. 23-629C | US Court of Federal Claims | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (patent/regulatory data as property); no R2, no R3 |
| 3-06 | Matalia v. Warwickshire County Council | Court of Appeal of England and Wales (Civil Division) | `bailii.org` — **unverified locator** | P | R1 (copyright); no R2, no R3 |

### 3.5 Category 4 — ISDS administrative-measure claim, no IP

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 4-01 | Tethyan Copper Company Pty Limited v. Islamic Republic of Pakistan | ICSID Case No. ARB/12/1 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/12/1` | P | R2 (mining-licence refusal as an administrative measure), R3; **no R1** |
| 4-02 | Burlington Resources Inc. v. Republic of Ecuador | ICSID Case No. ARB/08/5 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/08/5` | P | R2 (windfall-levy legislation), R3; no R1 |
| 4-03 | Saluka Investments B.V. v. Czech Republic | UNCITRAL (PCA-administered) | `pca-cpa.org` — case page for this caption | P | R2 (banking regulation and forced administration); no R1 |
| 4-04 | Eugenio Montenero v. People's Republic of China | ICSID (China–Switzerland BIT) — case number **not verified** | `icsid.worldbank.org/cases/case-database` — caption search; **case number unverified** | P | R2 (administrative measure), R3; no R1 |
| 4-05 | Franco-Nevada Corporation v. Republic of Panama | ICSID — case number **not verified** | `icsid.worldbank.org/cases/case-database` — caption search; **case number unverified** | P | R2 (mine closure as a state measure), R3; no R1 |
| 4-06 | Ntega Holding Burundi S.A. v. Republic of Burundi | ICSID Case No. ARB(AF)/26/1 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB(AF)/26/1` | P | R2 (administrative measure); no R1 |

### 3.6 Category 5 — Domestic trade-secret litigation, no state/treaty nexus

Every row in this category is a United States court document. Under the chairman's
`G-3` ruling (§3.1) **all six are tier P** — a US court opinion is a public primary
legal instrument issued by a court and published by it or by an authorised public
repository — each carrying `anchor: undetermined — resolved at retrieval`. **All six
remain unverified locators**, which is a separate defect: no US court host is in
`scripts/fetch_relay.py` `ALLOWED_HOSTS`, and the relay allowlist is untouched by the
tier ruling.

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 5-01 | Celgard, LLC v. Shenzhen Senior Technology Material Co. Ltd | US Court of Appeals for the Federal Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; **no R2, no R3, no state party** |
| 5-02 | E.I. du Pont de Nemours & Co. v. Kolon Industries, Inc. | US Court of Appeals for the Fourth Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; no R2, no R3 |
| 5-03 | Motorola Solutions, Inc. v. Hytera Communications Corp. Ltd. | US District Court, Northern District of Illinois / Seventh Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; no R2, no R3 |
| 5-04 | Waymo LLC v. Uber Technologies, Inc. | US District Court, Northern District of California | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; no R2, no R3 |
| 5-05 | Epic Systems Corp. v. Tata Consultancy Services Ltd. | US Court of Appeals for the Seventh Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; no R2, no R3 |
| 5-06 | Title Source, Inc. v. HouseCanary, Inc. | Court of Appeals of Texas, Fourth District | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R1 vocabulary (trade secret) only; no R2, no R3 |

### 3.7 Category 6 — Court enforcement / set-aside that is not a denial-of-justice claim

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 6-01 | Infrastructure Services Luxembourg S.à r.l. and Energia Termosolar B.V. v. Kingdom of Spain (enforcement) | Supreme Court of the United Kingdom | `bailii.org` — **unverified locator** | P | R2 present only as the *forum* (a domestic court), **not as the disputed conduct**; R3 (state immunity / ICSID Convention arts. 54, 55); no R1 |
| 6-02 | Micula and others v. Romania (enforcement) | Supreme Court of the United Kingdom | `bailii.org` — **unverified locator** | P | R2 as forum only; R3 (enforcement obligation vs EU law); no R1 |
| 6-03 | Malicorp Limited v. Government of the Arab Republic of Egypt (enforcement) | High Court of Justice of England and Wales (Commercial Court) | `bailii.org` — **unverified locator** | P | R2 as forum only; R3 (recognition/enforcement grounds); no R1 |
| 6-04 | OI European Group B.V. v. Bolivarian Republic of Venezuela (annulment) | ICSID ad hoc committee, Case No. ARB/11/25 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/11/25` | P | R3 (annulment grounds, ICSID Convention art. 52); no R1, no R2 |
| 6-05 | NextEra Energy Global Holdings B.V. and NextEra Energy Spain Holdings B.V. v. Kingdom of Spain (enforcement) | US Court of Appeals for the District of Columbia Circuit | US court records host — **unverified locator** | P — `anchor: undetermined — resolved at retrieval` | R2 as forum only; R3 (FSIA arbitration exception); no R1 |
| 6-06 | Unión Fenosa Gas, S.A. v. Arab Republic of Egypt (annulment) | ICSID ad hoc committee, Case No. ARB/14/4 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/14/4` | P | R3 (annulment grounds); no R1, no R2 |

### 3.8 Category 7 — Jurisdiction/admissibility decision, no IP

| # | Matter caption | Forum / tribunal | Candidate primary locator | Tier | Ring exercised |
|---|---|---|---|---|---|
| 7-01 | Salini Costruttori S.p.A. and Italstrade S.p.A. v. Kingdom of Morocco | ICSID Case No. ARB/00/4 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/00/4` | P | R3 (the Salini criteria; investment definition); no R1, no R2 |
| 7-02 | Fedax N.V. v. Republic of Venezuela | ICSID Case No. ARB/96/3 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/96/3` | P | R3 (investment definition, promissory notes); no R1, no R2 |
| 7-03 | Bayview Irrigation District and others v. United Mexican States | ICSID (Additional Facility) Case No. ARB(AF)/05/1 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB(AF)/05/1` | P | R3 (investor in the territory of another Party); no R1, no R2 |
| 7-04 | Alps Finance and Trade AG v. Slovak Republic | UNCITRAL (ad hoc) | `italaw.com` — case page for this caption (numeric case id **not verified**) | P | R3 (investment and investor definition); no R1, no R2 |
| 7-05 | H&H Enterprises Investments, Inc. v. Arab Republic of Egypt | ICSID Case No. ARB/09/15 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/09/15` | P | R3 (jurisdiction ratione materiae, assignment); no R1, no R2 |
| 7-06 | ACP Axos Capital GmbH v. Republic of Kosovo | ICSID Case No. ARB/15/22 | `icsid.worldbank.org/cases/case-database/case-detail?CaseNo=ARB/15/22` | P | R3 (jurisdiction/admissibility, legality); no R1, no R2 |

### 3.9 Category 8 — Headline-only / paywalled candidates

**Not nominated in advance, and that is a decision, not an omission.** A category-8
item **is** its headline (`SCHEMA.md:52-53`: `raw_text=title` is what production
sees). Nominating six paywalled headlines from a seat's memory would **fabricate the
item text itself** — the one field the coder reads. The repository holds no pool of
unpublished paywalled headlines to draw from: every IAReporter URL anywhere in
`digests/` is one of the 13 already published (`grep -rho
"https://www.iareporter.com/articles/[a-z0-9-]*" digests/ | sort -u | wc -l` → 13),
`state/seen.json` stores URLs without titles, and `state/deferred.json` carries
exactly one non-empty title (`grep -o '"title": "[^"]\{25,\}"' state/deferred.json |
sort -u | wc -l` → 1).

**Category 8's six rows are therefore RETRIEVAL-GENERATED**: the seat building batch
1 under RULING 3 takes the six headlines **as fetched, verbatim, in feed order**,
checks each against §3.11's exclusion list at matter level, and logs each in
`RETRIEVAL_LEDGER.md` before it enters `items.json`. Gap **`G-2`** stands until
those six are logged.

### 3.10 Category 9 — Paraphrase-heavy trade-secret / clinical-data / regulatory-data reporting

**Not nominated in advance, for the same reason and one more.** The category is
defined by *how a source paraphrases*, which is a property of the retrieved text and
cannot be known from a caption. The one instance the repository holds — "A panoramic
overview of China's pharmaceutical IP protection system" (Managing IP, via Bing
News) — is in the published set and is a collision (§3.11).

**Category 9's six rows are RETRIEVAL-GENERATED** on the same terms as category 8.
Gap **`G-2`** covers both.

### 3.11 Disjointness certificate — at the level of the MATTER, not the document

Binding. Proved against all three development sets. Every collision is **named**;
none is quietly dropped.

#### Counts, each with the command that produced it

| Development set | Count | Command |
|---|---|---|
| Retired holdout | **20 items**, of which **11 are named matters** and 9 are non-matter editorial/institutional listings | `python3 -c "import json;print(len(json.load(open('scripts/holdout_set.json'))['items']))"` |
| Frozen probes | **14 probes**, of which **11 are synthetic** (invented parties and states) and **3 reference real matters** | `python3 -c "import json;print(len(json.load(open('analytics/fingerprint_probes.json'))['probes']))"` |
| Published corpus | **17 article files**, **16 distinct captions and 16 distinct locators**, **15 distinct matters** | `ls digests/*/articles/*.md \| wc -l` → 17; `grep -h -o 'Read the original ↗](\([^)]*\)' digests/*/articles/*.md \| sed 's/.*](//' \| sort -u \| wc -l` → 16; `grep -h '^# ' digests/*/articles/*.md \| sed 's/^# [0-9]*\. //' \| sort -u \| wc -l` → 16; `grep -l -i okuashvili digests/*/articles/*.md \| wc -l` → 2 |

**Which published number this certificate uses, and why: 15.** RULING 1 states "the
**16 distinct published matters** (17 files; one Telefónica duplicate,
`italaw.com/cases/12153`, published 06-09 and 06-10)". Re-measured here, **16 is the
distinct-*document* count, not the distinct-*matter* count**: the Telefónica
duplicate takes 17 files to 16 distinct captions and locators, and then
*Okuashvili v. Georgia* is reported by **two different documents** — the italaw case
page `italaw.com/cases/9965` (2026-06-29 art. 01) and the IAReporter headline
"Swedish Supreme Court finds that claimant in Okuashvili v. Georgia can use MFN
detour to access arbitration under SCC Arbitration Rules" (2026-06-29 art. 03) —
which takes 16 distinct documents to **15 distinct matters**. That is also what
`SCHEMA.md:86-94` already records ("the 15 published matters — 17 article files, of
which one is a duplicate of another … and two report the same matter, Okuashvili v.
Georgia, through different forums"). **This certificate is at matter level, so it
uses 15.** The earlier analyst's figure of 15 distinct matters is confirmed; the
ruling's 16 is correct as a document count and is corrected here as a matter count.

#### The exclusion list (matter level) and the collisions found

**From the holdout (11 matters).** The Loewen Group v. United States; Mondev
International v. United States; Apotex Inc. v. United States; Philip Morris Brands
v. Uruguay; Chevron Corporation and Texaco Petroleum Corporation v. Ecuador (II),
PCA Case No. 2009-23; Spentech Engineering Limited v. United Arab Emirates; Smurfit
Holdings B.V. v. Venezuela, ICSID Case No. ARB/18/49; Rockhopper v. Italy
(resubmission); Gabriel Resources Ltd. and Gabriel Resources (Jersey) v. Romania,
ICSID Case No. ARB/15/31; Angel Samuel Seda and others v. Colombia, ICSID Case No.
ARB/19/6; Kurt Harald Grüninger, Alexandra Grüninger and Sascha Spittel v. Costa
Rica, ICSID Case No. ARB/23/16. *(The remaining nine holdout items — ITN issue
listings, an OECD Guidelines note, an ICSID office announcement, a staff vacancy —
name no matter and exclude nothing.)*

**From the frozen probes (3 real matters, reached through the probe texts).** Eleven
probes invent their parties and respondent states and exclude nothing.
`S1_seed_eli_lilly` is captioned "Eli Lilly-type claim" and `S2_seed_bridgestone_pm`
"Bridgestone / Philip Morris-type claim"; `E4_einarsson_negative_space` is an
anonymised award summary whose shape `agents/Claim Map.md:858` identifies as "the
**Apotex / Hela Schwarz negative-space shape**". Those texts make the matters appear
in the development set **"in any form"**, which is the standard `SCHEMA.md:89` sets.
They are further excluded as the instrument's three **development seeds** at
`prompts/classifier.txt:26-33`. Excluded: **Eli Lilly and Company v. Government of
Canada; Bridgestone Licensing Services, Inc. and Bridgestone Americas, Inc. v.
Panama; Philip Morris Asia Limited v. Commonwealth of Australia; Philip Morris
Brands SARL and others v. Uruguay; Apotex Inc. v. United States; Hela Schwarz GmbH
v. People's Republic of China.**

**From the published corpus (15 matters).** Individual gambling investors v. Ecuador
(ICSID, following an UNCITRAL dismissal); Telefónica, S.A. v. Republic of Colombia,
ICSID Case No. ARB/18/3; Hydro S.r.l. and others v. Republic of Albania (I), ICSID
Case No. ARB/15/28; the ICSID sanctions-related Ukraine provisional-measures matter
(**unnamed on the face of the published headline**); the UK High Court set-aside
amendment matter (**unnamed**); the French Cour de cassation shipyard-investor /
Greek growthfund enforcement matter; Okuashvili v. Georgia (two documents, one
matter); the Court of Appeal of Santiago salmon-venture set-aside; Suez v. Argentina
(1); B-Mex v. Mexico; the ICSID ad hoc committee / Peru MST annulment (**unnamed**);
the Gazprom-affiliate / Linde Russian-subsidiary enforcement matter; the UK High
Court / Bahrain state oil company guarantees matter; the Swiss Federal Tribunal
set-aside of an award declining jurisdiction over a mining company's multi-billion
claim against Australia (**unnamed**); and one article that names no matter at all
("A panoramic overview of China's pharmaceutical IP protection system").

#### Collisions found, named, and disposed of

| # | Colliding nomination | Set collided with | Disposition |
|---|---|---|---|
| C-1 | Eli Lilly and Company v. Government of Canada | probes `S1`; development seed `prompts/classifier.txt:26-33` | **Named and excluded.** Category 1's replacement: row 1-01 (Einarsson/GSI). |
| C-2 | Bridgestone Licensing Services, Inc. v. Panama | probes `S2`; development seed | **Named and excluded.** Replacement: row 1-03 (Merck v. Ecuador — trademark + domestic court judgment). |
| C-3 | Philip Morris Asia Limited v. Commonwealth of Australia | probes `S2`; development seed | **Named and excluded.** Replacement: row 2-01 (Emmis v. Hungary — licence-as-investment, negative). |
| C-4 | Philip Morris Brands SARL and others v. Uruguay | holdout `pm_v_uruguay`; probes `S2` | **Named and excluded.** Replacement: row 1-04 (Shell Brands v. Nicaragua). |
| C-5 | Apotex Inc. v. United States | holdout `apotex_v_us`; probe `E4` shape | **Named and excluded.** Replacement: row 2-02 (Cortec v. Kenya). |
| C-6 | Hela Schwarz GmbH v. People's Republic of China | probe `E4` shape, per `agents/Claim Map.md:858` | **Named and excluded.** No replacement available; counted in gap `G-1`. |
| C-7 | Chevron Corporation and Texaco Petroleum Corporation v. Ecuador (II) | holdout `iisd_itn:Chevron…` | **Named; never nominated.** No replacement needed. |
| C-8 | Tethyan Copper Company Pty Limited v. Pakistan (enforcement/annulment framing) | none — the **award** is in no development set | **Not a collision.** Nominated once only, at row 4-01, and deliberately **not** re-nominated in category 6, which would have collided with itself at matter level. |
| C-9 | "A panoramic overview of China's pharmaceutical IP protection system" | published corpus, 2026-08-10 art. 01 | **Named; excluded from category 9**, which is why category 9 is retrieval-generated. |
| C-10 | Zeph Investments Pte Ltd v. Commonwealth of Australia | **possible** collision with the published 2026-08-10 art. 03 Swiss Federal Tribunal headline, which does not name its matter | **Not nominated.** The published headline names no matter, so the collision can be neither proved nor excluded; nominating Zeph would risk an unprovable collision. Filed under gap `G-4`. |

**Cross-check performed.** Every nominated caption in §3.2–§3.8 was checked against
all three sets. Beyond C-1 … C-6, which were caught before nomination and are listed
because the ruling requires collisions to be named rather than quietly avoided, **no
nominated row collides with any development-set matter.**

#### Two matters deliberately NOT nominated, and why

- ***Wingtech Technology Co. v. Kingdom of the Netherlands*** and ***Nexperia v.
  Netherlands***. This project's own standing watch records that an ICSID
  registration of a Wingtech proceeding is **NOT FOUND IN ACCESSIBLE SOURCES, and it
  is never stated that none exists** (`STATE_OF_THE_ANSWER.md:62`, `:73`, `:96`).
  Nominating a matter whose existence this record expressly does not establish would
  assert, by the act of nominating it, the very thing the record declines to assert.

### 3.12 Gaps opened by this section — stable slugs

| Slug | What is open | Closure condition |
|---|---|---|
| `G-1` `locked-set-cat2-negative-ip-holding-unfillable` | Category 2 has 2 of 6 rows. Every matter the repository knows in this category is in a development set (C-1 … C-6). | Four IP-as-investment matters with a negative investment or jurisdiction holding, none in any development set, each with a retrievable primary document. |
| `G-2` `locked-set-cat8-cat9-retrieval-generated` | Categories 8 and 9 have 0 of 6 rows each, by decision: their item text cannot be nominated without fabricating it. | Twelve headlines retrieved verbatim from the live feeds, matter-checked against §3.11, logged in `RETRIEVAL_LEDGER.md`. |
| `G-3` `schema-tier-p-omits-domestic-court-hosts` — **CLOSED 2026-09-13** | Nine rows carried `UNASSIGNED` tier: US federal and state court opinions were in none of `SCHEMA.md`'s P, S or C tiers, yet category 5 is defined by them. | **Closed by the chairman's ruling of 2026-09-13**: tier P redefined by criterion rather than by host enumeration, authorship governing over host; the nine rows are committed at tier P with `anchor: undetermined — resolved at retrieval` (§3.1). The relay-allowlist defect is NOT closed by it and is carried in §3.14. |
| `G-4` `published-swiss-federal-tribunal-matter-unnamed` | The 2026-08-10 art. 03 headline names no matter, so it cannot be excluded from or admitted to the exclusion list; *Zeph Investments v. Australia* is un-nominated on that account. | The underlying Swiss Federal Tribunal judgment read, and its caption recorded. |

**Filled tally, stated plainly: 38 of the 54 design-target rows are nominated
(cat 1: 6, cat 2: 2, cat 3: 6, cat 4: 6, cat 5: 6, cat 6: 6, cat 7: 6, cat 8: 0,
cat 9: 0). Sixteen rows are open under `G-1` and `G-2`.** Six-per-category remains
the design target; `RETRIEVAL_LEDGER.md:26` already records that "54 is a design
target, not a queue". Padding the sixteen would have produced a full-looking table
whose missing rows no later reader could find.

### 3.13 Provenance index — where each caption came from

Not a row field; recorded separately so the row constraint in §3.0 is not breached.
Two classes only.

**(a) Sourced from this repository's own corpus** — the caption appears at the
pinpoint given, and the row's docket number, where stated, is quoted from there:

| Row | Pinpoint |
|---|---|
| 1-01 | `analytics/daily-research/2026-06-23.md:39` |
| 1-02 | `lit-review/ferguson-memo.md:38` ("Les Laboratoires Servier v Poland (Award) (14 February 2012") |
| 1-05 | `analytics/insights.jsonl:31` |
| 3-01 | `lit-review/kim-memo.md:158` |
| 3-02 | `lit-review/kim-memo.md:170` |
| 3-03 | `lit-review/kim-memo.md:182` |
| 3-04 | `lit-review/kim-memo.md:194` |
| 3-05 | `analytics/locked_set/RETRIEVAL_LEDGER.md:18-19` (RETRIEVED 2026-08-06, verified 2026-08-08) |
| 3-06 | `lit-review/ferguson-memo.md:233` |
| 4-01 | `lit-review/ferguson-memo.md:271` |
| 4-02 | `lit-review/ferguson-memo.md:185` |
| 4-03 | `lit-review/ferguson-memo.md:123` |
| 4-04 | `analytics/daily-research/2026-07-19.md:130` |
| 4-05 | `analytics/insights.jsonl:102` |
| 4-06 | `analytics/fetch-results/2026-09-09-daily.json:49` |
| 5-01 | `lit-review/ferguson-memo.md:221` |
| 6-03 | `analytics/council-sessions/2026-08-03-proposition-rule.md:120` |
| 6-04 | `analytics/locked_set/RETRIEVAL_LEDGER.md:23` |
| 7-01 | `lit-review/ferguson-memo.md:99`; `lit-review/kim-memo.md:110` |
| 7-02 | `lit-review/ferguson-memo.md:111` |
| 7-03 | `lit-review/ferguson-memo.md:135` |
| 7-04 | `lit-review/ferguson-memo.md:159` |
| 7-05 | `lit-review/ferguson-memo.md:171` |
| 7-06 | `lit-review/ferguson-memo.md:147` |

**(b) Analyst knowledge, unverified against any source in hand** — rows **1-03,
1-04, 1-06, 2-01, 2-02, 5-02, 5-03, 5-04, 5-05, 5-06, 6-01, 6-02, 6-05, 6-06**.
Fourteen rows. **The caption, the forum and any docket number in these rows are
this seat's recollection and are asserted as nothing more than a lead to be
checked.** This is disclosed rather than smoothed over: under the carrying-span
rule none of these may be relied on for any proposition until its primary document
is retrieved and read. If any of them proves not to exist, the honest record is that
this record nominated it and retrieval found nothing — not that the matter was
dropped.

### 3.14 Locator status, counted

**The tier ruling does not touch the relay allowlist, and the two must not be
conflated. Sixteen of the 38 nominated rows carry "unverified locator"** — their host is
absent from `scripts/fetch_relay.py` `ALLOWED_HOSTS` (18 hosts, one of which,
`example.com`, is a neutral control only), so this council cannot confirm the URL
resolves: rows **3-01, 3-02, 3-03, 3-04, 3-05, 3-06, 5-01, 5-02, 5-03, 5-04, 5-05,
5-06, 6-01, 6-02, 6-03, 6-05** — `curia.europa.eu` (3), `bailii.org` (4) and US
court record hosts (9). RULING 1 anticipated Curia, BAILII, WTO and `legal.un.org`;
**US court hosts are a fifth off-allowlist family this drafting found**, and they
carry nine of the sixteen. No WTO or `legal.un.org` row was nominated.

Two further rows carry an allowlisted host but an **unverified case number** (4-04,
4-05) and three carry an allowlisted host with an **unverified numeric case id**
(1-02, 1-06, 7-04). Those are not "unverified locator" in the ruling's sense — the
host resolves — and they are recorded separately so the two defects are not
conflated.

---
