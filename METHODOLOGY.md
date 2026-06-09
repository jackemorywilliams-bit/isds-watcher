**TO:** Dr. Ximena Benavides, Department of Legal Studies, Terry College of Business
**FROM:** Emory Williams, Undergraduate Research Assistant
**DATE:** 06/08
**RE:** Methodology Memo — The ISDS Thematic Watcher: design, justification, and validation of an automated thematic-surveillance instrument for the IP-as-investment / judicial-measure / jurisdictional-admissibility intersection

---

## I. Research Question & Scope

This memo documents the methodology of the ISDS Thematic Watcher, the automated monitoring instrument I built for this project, and grounds each design decision in the methodological and doctrinal literature we have been using throughout the literature review. The instrument answers an operational question that sits underneath the substantive ones: across the open record of investor-State practice, which new developments fall within the specific doctrinal intersection the project tracks — intellectual property asserted as a covered investment, a regulatory or judicial measure as the disputed conduct, and a jurisdictional or admissibility doctrine disposing of the claim — and how can that determination be made continuously, reproducibly, and without paid databases?

The scope of this memo is methodological rather than substantive. It does not re-argue whether trade secrets or clinical data qualify as protected investments; it explains how the instrument operationalizes that doctrinal frame into a detection procedure that can be independently audited and, where appropriate, contested. The memo proceeds from the theoretical frame (Part II), through source architecture and the backsourcing-derived collection method (Part III), candidate identification and enrichment (Part IV), the two-stage classification cascade (Part V), scoring, calibration, and validation (Part VI), the reporting standard governing the digest (Part VII), reproducibility (Part VIII), and a candid statement of limitations (Part IX), before collecting the methodological and doctrinal authorities on which the instrument rests (Part X).

## II. Theoretical Framework — The Three-Ring Thematic Fingerprint

### A. Why a thematic instrument, and not a keyword search

The object of surveillance is not a word but a *relationship between three doctrines*, and a relationship cannot be reduced to a keyword without discarding the very thing that defines it. A case may say "patent" a hundred times and be irrelevant; a case may never say "abuse of right" and sit squarely within the theme. The methodological problem is therefore interpretive, not lexical: how does one teach an instrument to recognize a category it has seen only three times?

The discipline that solves this is qualitative coding. I treated the construction of the fingerprint as an exercise in theoretically informed sampling and most-similar-case design — the techniques Linos and Carlson recommend importing into legal scholarship precisely because legal writers tend to pick examples unsystematically and analyze them with doctrinal tools alone (Linos & Carlson, *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017)). The seed corpus was not assembled for representativeness of all ISDS; it was assembled for *structural similarity along the dimension of interest*, which is the logic of a most-similar-case design. The coding itself — extracting the operative doctrinal phrases, grouping them into categories, and refining those categories against the data — follows the first- and second-cycle coding and analytic-memo procedure of Saldaña, *The Coding Manual for Qualitative Researchers* (3d ed.).

### B. The seed corpus

Three awards were selected because, despite unrelated subject matter, they share the structural signature the project tracks:

- *Philip Morris Asia Ltd v. Commonwealth of Australia*, PCA Case No. 2012-12, Award on Jurisdiction and Admissibility (17 Dec. 2015) — tobacco plain-packaging legislation attacking trademark rights; dismissed on abuse of right where the claimant restructured to obtain treaty protection over a "reasonably foreseeable" dispute.
- *Eli Lilly & Co. v. Government of Canada*, ICSID Case No. UNCT/14/2, Final Award (16 Mar. 2017) — pharmaceutical patents invalidated under the "promise utility doctrine"; a challenge to a judicial measure under the NAFTA Article 1105 minimum standard, framed as denial of justice.
- *Bridgestone Licensing Servs., Inc. & Bridgestone Ams., Inc. v. Republic of Panama*, ICSID Case No. ARB/16/34, Award (14 Aug. 2020) — a trademark licensor/licensee structure; denial of justice over a Supreme Court judgment; a "shell subsidiary" abuse-of-process allegation echoing *Philip Morris*.

The coding unit was the tribunals' own language: the operative phrases were extracted verbatim from the awards (the per-ring extraction is preserved in `PLAN.md`) and promoted to index terms. This is deliberate and tracks the foundational principle of information retrieval — that the most discriminating index terms are those that actually occur in the relevant documents (Salton & McGill, *Introduction to Modern Information Retrieval* (1983); Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (2008)). A future report describing a like case will tend to reproduce that language; the fingerprint is built to catch the echo.

### C. The three rings

**Ring 1 — Intellectual property as a protected investment.** Whether, and on what conditions, intellectual property qualifies as a covered "investment" is the threshold definitional question that recurs across the project's reading (Mercurio, *Awakening the Sleeping Giant*, 15 J. Int'l Econ. L. 871 (2012); Correa & Viñuales, *Intellectual Property Rights as Protected Investments: How Open are the Gates?*, 19 J. Int'l Econ. L. 91 (2016)). The ring is most acute where the asset is informational or split across holding and operating entities — the *Bridgestone* licensor/licensee posture, and the same structural vulnerability the Ferguson and Kim memos identify for trade secrets and clinical data. The definitional threshold also imports the Salini criteria (contribution, duration, risk, and contribution to the host economy) on which tribunals exercise discretion (cf. *Salini Costruttori S.p.A. v. Morocco*, ICSID Case No. ARB/00/4). Verbatim triggers: `covered investment`, `promise utility doctrine`, `exploitation of the trademark`.

**Ring 2 — A regulatory or judicial measure as the disputed conduct (weighted).** Two of the three seeds attack not an executive act but a domestic court, pleading denial of justice. The governing standard is Paulsson, *Denial of Justice in International Law* (2005): the State answers for its judiciary only at the outer threshold of manifest injustice, not for ordinary error. The seed tribunals reproduce that standard verbatim — conduct "egregious and shocking," a "manifestly unjust judgment," a ruling so "egregiously wrong that no honest or competent court could" reach it. Because the seed corpus is weighted toward this ring, the instrument is too: a credible challenge to a court judgment reaches the MEDIUM band on its own. Prevalence within the coding corpus is a recognized ground for weighting a category (Saldaña, *Coding Manual*). Verbatim triggers: `denial of justice`, `manifestly unjust judgment`, `minimum standard of treatment`.

**Ring 3 — The case is decided at the threshold, not on the merits.** The seeds share a procedural signature: the public-interest merits were never reached because the cases turned on jurisdiction and admissibility — abuse of right, treaty shopping, foreseeability of the dispute, restructuring for treaty protection, the contested definition of "investor." The controlling synthesis is Baumgartner, *Treaty Shopping in International Investment Law* (2016), resting on the older abuse-of-rights principle (Byers, *Abuse of Rights: An Old Principle, A New Age*, 47 McGill L.J. 389 (2002)) and the standard treatises (Dolzer & Schreuer, *Principles of International Investment Law* (2d ed. 2012); McLachlan, Shore & Weiniger, *International Investment Arbitration: Substantive Principles* (2d ed. 2017)). Verbatim triggers: `abuse of right`, `reasonably foreseeable`, `critical date`, `shell subsidiary`.

### D. The scoring grammar

The signal is the *intersection*. HIGH (≥70) requires two rings; MEDIUM (40–69) requires one strong ring with a weaker second tie, or a judicial-measure case standing alone; LOW (<40) is one weak ring or none, with extractives, sovereign debt, and intra-EU energy defaulting to LOW absent an IP or judicial angle. The full machine-readable frame — every phrase and weight, summing to 100 within each ring — is maintained in `fingerprint.yaml`.

## III. Source Architecture & Research Methods

### A. Source selection and triangulation

Sources were selected to triangulate the event-space across institutional, archival, analytical, and practitioner channels, on the methodological principle that convergence across independent sources distinguishes signal from artifact (the triangulation logic discussed in *A Practical Framework for Conducting a Literature Review*, The Qualitative Report (Nova Southeastern Univ.)). The instrument reads the ICSID docket; UNCTAD's Investment Dispute Settlement Navigator and *World Investment Report*; the italaw primary-document archive; IISD's Investment Treaty News; and IAReporter at headline level. These are the same open repositories I use for manual backsourcing elsewhere in the project (italaw, UNCTAD, and the institutional dockets), now read continuously rather than case-by-case.

### B. Collection method — an automated analog of our backsourcing workflow

The collection method deliberately mirrors the backsourcing-and-verification procedure we adopted for the literature review, under which a substantive claim is traced to its underlying source in an official repository rather than accepted on the strength of a citation. Here the instrument (1) retrieves each source's listing; (2) extracts candidate items; (3) where a listing exposes only a case name, retrieves the underlying page from the source's own repository to recover the substantive text (Part IV); and (4) records provenance — source, stable identifier, URL, and timestamp — for every item, so that any entry in any digest can be traced back to the document that produced it. This is the same "source of truth" discipline as the memos: the recovered primary text, not the listing summary, governs the classification.

### C. Collection ethics

The instrument reads open sources only and never circumvents access controls. It honors the Robots Exclusion Protocol (RFC 9309; Koster, Illyes, Zeller & Sassman, 2022): where a host's `robots.txt` disallows a path — as Google News presently disallows its RSS endpoint — the source is dropped and the omission is logged, not evaded. It transmits an identifying User-Agent linking back to the repository, observes a minimum three-second interval per domain, and never retrieves the body of a paywalled article (IAReporter is read at headline level only). Where a page layout drifts, a structural fallback selector is used and the fallback is logged; a source that fails returns an empty result rather than aborting the run. These constraints are the crawler analog of the access limitations I flag manually in the bibliographies — stated explicitly rather than omitted.

## IV. Candidate Identification & Enrichment

A listing page that yields only "*Ferrer v. Ecuador*" is insufficient input; scored as-is, it produces noise. Before classification, therefore, the most promising candidates are *enriched*: the instrument retrieves the source page, reduces it to its readable body, and selects a single **notable line** — the sentence carrying the highest density of doctrinal vocabulary, a term-frequency selection in the sense of Salton & McGill (1983). The notable line does the work of a well-chosen pin-cite in a backsourced bibliography: it supplies the classifier with substantive text to evaluate, and it gives the reader the one sentence worth seeing. Enrichment is capped per run to respect the collection-ethics budget of Part III.C, and paywalled sources are never opened.

## V. Classification Procedure — A Two-Stage Cascade

Classification proceeds in two stages because recall and precision pull against each other, and each is best served by a different instrument.

**Stage one — lexical coding (deterministic, transparent).** Every candidate is scored against the `fingerprint.yaml` vocabulary by summing matched per-keyword weights within each ring — classical weighted term matching (Salton & McGill, 1983). This stage ranks candidates so that enrichment is spent on the most promising, and it doubles as a fully offline fallback: absent any language model, the instrument still returns a scored, auditable result. No stage is opaque to inspection.

**Stage two — contextual classification (paraphrase-tolerant).** The enriched front-runners are then evaluated by a large language model (Anthropic Claude or Google Gemini, selected at runtime) under a few-shot prompt that supplies the ring definitions and worked HIGH/MEDIUM/LOW exemplars, including negative examples so the boundary is learned, not merely the target. Few-shot prompting is used because it materially improves task adherence without fine-tuning (Brown et al., *Language Models are Few-Shot Learners*, NeurIPS 33 (2020)). The model must return strict JSON — relevance score, matched rings, thematic tags, and a two-sentence annotation. On malformed output the pipeline retries once under a stricter instruction; on a second failure it records a zero tagged `classification_failed`; on a quota or network error it falls back to the lexical score. A verdict is always produced. The stages are complementary: the lexicon guarantees recall on the tribunals' exact phrasing, while the model recognizes the same idea in paraphrase.

## VI. Scoring, Calibration & Validation

### A. Calibration decisions, stated as the value judgments they are

*A ring must earn its place.* A ring counts as "present" only once its lexical subtotal clears a floor (≥12) — one substantive hit, not an incidental brush against a single word — which suppresses the false intersection in which, e.g., a mining claim mentions "investment" and is mistaken for the theme. This is a minimum-term-frequency cut-off in substance (Manning, Raghavan & Schütze, 2008).

*The gate was lowered on purpose.* The digest threshold is set at 40, reduced from an initial 60. A monitoring instrument is not an adjudicative one; its function is to surface leads, and the recall-for-precision trade was made consciously.

*The digest is never empty.* Because a theme this narrow produces silent intervals, and because an empty report trains its reader to stop reading, the instrument surfaces the top-ranked material down to a relevance floor when too few items clear the gate, labeled as watch-list rather than match. This is recall-over-precision by design — appropriate to surveillance, inappropriate to adjudication — and it is flagged so that no reader mistakes a lead for a holding.

### B. Validation

The lexical scorer is regression-tested against the labeled exemplars in `fingerprint.yaml` (`tests/test_pipeline.py`) and reproduces the intended band on all seven, including the negatives; and the three seed awards, scored on their own text, return MEDIUM to HIGH. The instrument recognizes the cases that generated it — a face-validity check against the inducing corpus, in the sense in which qualitative method treats fit-to-exemplars as a validity criterion (Saldaña; Linos & Carlson).

## VII. The Reporting Standard — The Digest as Annotated Bibliography

The weekly digest is deliberately structured as an annotated bibliography rather than a list of links, because the project's standard for a research deliverable is interpretive, not merely descriptive. Each entry follows the annotated-bibliography conventions of the AALL *Law Library Journal* guidelines: a citation, followed by an annotation that is descriptive and evaluative, in the 50–200-word range those guidelines specify, with citation form per The Chicago Manual of Style (§§ 14.61–14.305) and URLs supplied liberally beyond the minimum to facilitate retrieval. Consistent with the analytically engaged bibliography described in The Qualitative Report framework, each entry also reflects on *fit* — which rings the development implicates and why it matters to the project — so that the bibliography performs interpretive work rather than functioning as a collection of references. Every entry names its source and links to the original, and quotes a verbatim notable line, so that the reader can proceed directly to backsourcing in the manner described in Part III.B. Where a source is paywalled or a listing exposes only metadata, that limitation is stated rather than concealed.

## VIII. Reproducibility & State

Every processed item is recorded by source and stable identifier in `state/seen.json`, so nothing is classified or reported twice; the store bootstraps on first run and treats corruption as an empty slate, never taking the pipeline down with it. Each scheduled run commits its dated digest archive and its updated state back to the repository under version control, producing a complete, timestamped, replayable record of what was observed, when, and how it was scored — the reproducibility analog of retaining the manual annotations as the project's "source of truth."

## IX. Limitations

Consistent with the project's practice of stating access and coverage limits explicitly rather than omitting them:

- **Construct validity.** The theme is induced from three awards and may under-represent doctrinal variants the seeds do not raise; this is mitigated, not eliminated, by lightly weighted `theme_extension` terms for adjacent doctrines (denial of benefits, substantial business activities).
- **Coverage is a lower bound.** Paywalls and `robots.txt` (Part III.C) place real material out of reach; Google News RSS is presently disallowed and therefore inactive. The instrument reports a floor on what exists, not a census.
- **Thin metadata.** Where content sits behind authentication, a bare case name is the only input, and the score reflects that poverty of input.
- **Model variance.** Outputs are non-deterministic; the strict-JSON contract, one-retry rule, deterministic fallback, and test suite bound the variance without abolishing it.
- **A deliberate thumb on the scale.** Ring 2's weighting and the never-empty rule favor recall; MEDIUM and watch-list items are leads to run down, not conclusions to cite.

## X. Methodological & Doctrinal Authorities

### A. Methodological authorities (instrument design and reporting standards)

- Saldaña, J., *The Coding Manual for Qualitative Researchers* (3d ed., SAGE) — coding cycles and analytic-memo framework underlying the fingerprint induction.
- Linos, K. & Carlson, M., *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017) — theoretically informed sampling and most-similar-case design, adapting qualitative method to legal writing.
- *A Practical Framework for Conducting a Literature Review*, The Qualitative Report (Nova Southeastern Univ.) — triangulation and the analytically engaged, project-fit-reflective bibliography.
- American Association of Law Libraries, *Law Library Journal* — *General Instructions & Sample Entries for Bibliographies* — annotated-bibliography standard (descriptive-and-evaluative annotations, ~50–200 words; citation per The Chicago Manual of Style §§ 14.61–14.305).
- CUNY School of Law, *Drafting a Law Office Memorandum*; Columbia Law School, *Memo Writing Checklist*; Eric E. Johnson, *Memo to Student Research Assistants re Research Deliverables* (2023) — memorandum structure and research-deliverable conventions.
- Salton, G. & McGill, M.J., *Introduction to Modern Information Retrieval* (1983); Manning, C.D., Raghavan, P. & Schütze, H., *Introduction to Information Retrieval* (2008) — weighted term matching, term-frequency selection, crawling practice.
- Brown, T.B., et al., *Language Models are Few-Shot Learners*, NeurIPS 33 (2020) — few-shot in-context classification.
- Koster, M., Illyes, G., Zeller, H. & Sassman, L., *Robots Exclusion Protocol*, RFC 9309 (IETF 2022) — collection ethics.

### B. Doctrinal authorities (the substance the fingerprint encodes)

- Paulsson, J., *Denial of Justice in International Law* (Cambridge Univ. Press 2005).
- Baumgartner, J., *Treaty Shopping in International Investment Law* (Oxford Univ. Press 2016).
- Byers, M., *Abuse of Rights: An Old Principle, A New Age*, 47 McGill L.J. 389 (2002).
- Mercurio, B., *Awakening the Sleeping Giant: Intellectual Property Rights in International Investment Agreements*, 15 J. Int'l Econ. L. 871 (2012).
- Correa, C.M. & Viñuales, J.E., *Intellectual Property Rights as Protected Investments: How Open are the Gates?*, 19 J. Int'l Econ. L. 91 (2016).
- Kingsbury, B. & Schill, S., *Investor-State Arbitration as Governance: Fair and Equitable Treatment, Proportionality and the Emerging Global Administrative Law* (IILJ Working Paper 2009/6) — proportionality and public-law review.
- Dolzer, R. & Schreuer, C., *Principles of International Investment Law* (2d ed. 2012); McLachlan, C., Shore, L. & Weiniger, M., *International Investment Arbitration: Substantive Principles* (2d ed. 2017).
- *Salini Costruttori S.p.A. v. Morocco*, ICSID Case No. ARB/00/4 (Decision on Jurisdiction, 2001) — the Salini criteria for "investment."
- UNCTAD, *World Investment Report* and *Investment Dispute Settlement Navigator* (annual).
- Seed awards: *Philip Morris Asia Ltd v. Australia*, PCA Case No. 2012-12 (17 Dec. 2015); *Eli Lilly & Co. v. Canada*, ICSID Case No. UNCT/14/2 (16 Mar. 2017); *Bridgestone Licensing Servs. v. Panama*, ICSID Case No. ARB/16/34 (14 Aug. 2020).

---

*Methodological note.* This memo follows the law-office-memorandum conventions used throughout the project (CUNY; Columbia; Johnson, 2023), and its reporting standards — descriptive-and-evaluative annotation, project-fit reflection, and explicit statement of verification limits — follow the AALL annotated-bibliography guidelines and the analytic-memo framework of Saldaña and Linos & Carlson, consistent with the backsourcing methodology described in Part III.B.
