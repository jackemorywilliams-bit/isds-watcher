**MEMORANDUM**

**TO:** Dr. Ximena Benavides, Department of Legal Studies, Terry College of Business
**FROM:** Emory Williams, Undergraduate Research Assistant
**DATE:** 06/08/2026
**RE:** Methodology Memo — The ISDS Thematic Watcher: design, justification, and validation of an automated thematic-surveillance instrument for the IP-as-investment / judicial-measure / jurisdictional-admissibility intersection

---

## I. Research Question & Scope

This memo documents the operational methodology of the ISDS Thematic Watcher, the automated monitoring instrument I developed for this project, and it grounds each design decision in the literature we have reviewed so far. Underneath the project's substantive questions sits an operational one, and that is the question the instrument actually answers. Across the open record of investor-State practice, how does one identify new developments at a specific doctrinal intersection: where an intellectual property right is asserted as a covered investment, where a governmental act or a court judgment is challenged as a violation of that right, and where the case is disposed of at the jurisdictional or admissibility stage rather than on the merits; and how can that identification be done repeatedly and uniformly, without paid databases?

The scope of this memo is methodological rather than substantive. It does not re-argue whether trade secrets or clinical trial data qualify as protected investments; for those arguments, see the Ferguson and Kim memos. What it describes is how the instrument takes that doctrinal frame and turns it into a repeatable process with multiple points of auditability, and of contestation where that is warranted. The memo proceeds from the theoretical basis of the instrument (Part II), through the source architecture and the collection mechanism (Part III), candidate identification and enrichment (Part IV), a two-stage classification cascade (Part V), scoring, calibration, and validation (Part VI), the reporting standard for the digest (Part VII), reproducibility (Part VIII), and a candid statement of limitations (Part IX), before collecting the authorities on which the instrument rests (Part X).

## II. Theoretical Framework — The Three-Ring Thematic Fingerprint

### A. Why a thematic instrument, and not a keyword search

The object of surveillance is not a single term but a relationship among three doctrines, and a relationship of that kind cannot be reduced to a keyword without discarding the very thing that defines it. A case may invoke the word "patent" a hundred times and remain irrelevant; a case that never once uses the phrase "abuse of right" may sit squarely within the theme. The methodological problem is therefore interpretive rather than lexical, and it is the kind of problem qualitative method was developed to solve: how to train an instrument to recognize a category it has seen only three times.

I treated the construction of the fingerprint as an exercise in theoretically informed sampling and most-similar-case design, the techniques Linos and Carlson recommend importing into legal scholarship precisely because legal writers tend to select examples unsystematically and then analyze them with doctrinal tools alone (Linos & Carlson, *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017)). I did not assemble the seed corpus to be representative of all ISDS. I assembled it for structural similarity along the dimension of interest, which is the logic of a most-similar-case design. The coding itself — extracting the operative doctrinal phrases, grouping them into categories, and refining those categories against the data — follows the first- and second-cycle coding and analytic-memo procedure of Saldaña, *The Coding Manual for Qualitative Researchers* (3d ed.).

### B. The seed corpus

Three awards were chosen because, across very different subject matter, each exhibits the structural signature the project tracks:

- *Philip Morris Asia Ltd v. Commonwealth of Australia*, PCA Case No. 2012-12, Award on Jurisdiction and Admissibility (17 Dec. 2015). Philip Morris challenged Australia's tobacco plain-packaging legislation, which required cigarettes to be sold without brand or logo livery, as a taking of its trademark rights. The tribunal never reached that question. It dismissed the claim on abuse of right, because Philip Morris had restructured into a Hong Kong entity to acquire treaty protection over a dispute that was already reasonably foreseeable.
- *Eli Lilly & Co. v. Government of Canada*, ICSID Case No. UNCT/14/2, Final Award (16 Mar. 2017). Eli Lilly challenged the invalidation of its Zyprexa and Strattera patents by the Canadian courts under the "promise utility doctrine," advancing the court rulings as a judicial measure that breached the NAFTA Article 1105 minimum standard of treatment and amounted to denial of justice.
- *Bridgestone Licensing Servs., Inc. & Bridgestone Ams., Inc. v. Republic of Panama*, ICSID Case No. ARB/16/34, Award (14 Aug. 2020). Bridgestone alleged that a judgment of Panama's Supreme Court, in a trademark-opposition dispute, was a denial of justice; Panama, for its part, alleged a "shell subsidiary" abuse of process echoing the *Philip Morris* allegation.

The coding unit was the tribunals' own language: the operative phrases were taken directly from the awards (the full per-ring extraction is preserved in `PLAN.md`) and promoted to index terms. The selection is intentional, and it is consistent with a basic principle of information retrieval, that the index terms which best distinguish relevant documents are the ones that appear in those documents themselves (Salton & McGill, *Introduction to Modern Information Retrieval* (1983); Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (2008)). A subsequent report describing a like case tends to reproduce the language the tribunal used, and the fingerprint is constructed to detect that echo.

### C. The three rings

**Ring 1 — Intellectual property as a protected investment.** Whether, and on what conditions, intellectual property qualifies as a covered "investment" is the threshold definitional question that recurs throughout the project's reading (Mercurio, *Awakening the Sleeping Giant*, 15 J. Int'l Econ. L. 871 (2012); Correa & Viñuales, *Intellectual Property Rights as Protected Investments: How Open are the Gates?*, 19 J. Int'l Econ. L. 91 (2016)). The ring is most acute where the asset is informational, or where ownership is split between a holding entity and an operating one, as in *Bridgestone*, and it reflects the same structural vulnerability the Ferguson and Kim memos identify for trade secrets and clinical trial data. The threshold also imports the Salini criteria — contribution, duration, risk, and contribution to the host economy — on which tribunals retain considerable latitude (cf. *Salini Costruttori S.p.A. v. Morocco*, ICSID Case No. ARB/00/4). Verbatim triggers: `covered investment`, `promise utility doctrine`, `exploitation of the trademark`.

**Ring 2 — A regulatory or judicial measure as the disputed conduct (weighted).** Of the three seeds, two were brought against domestic courts rather than against an executive act, and both pleaded denial of justice. The standard for when a State is responsible for its judiciary is set out in Paulsson, *Denial of Justice in International Law* (2005): a State answers for its courts only on a showing of manifest injustice, and mere error does not meet that test. The seed tribunals reproduce that standard almost verbatim, describing conduct "egregious and shocking," a "manifestly unjust judgment," and a ruling "egregiously wrong that no honest or competent court could" have reached. Because the seed corpus emphasizes this ring, the weight assigned to it is correspondingly high, and a credible challenge to a court judgment reaches the MEDIUM band on its own. Prevalence within a coding corpus is a recognized ground for weighting a category (Saldaña, *Coding Manual*). Verbatim triggers: `denial of justice`, `manifestly unjust judgment`, `minimum standard of treatment`.

**Ring 3 — The case is decided at the threshold, not on the merits.** The three seeds share a procedural signature: none of the tribunals reached the public-interest merits, because each case was disposed of on jurisdiction or admissibility before the merits could be heard — abuse of right, treaty shopping, foreseeability of the dispute, restructuring for treaty protection, and the contested definition of "investor." The controlling synthesis is Baumgartner, *Treaty Shopping in International Investment Law* (2016), which rests on the older abuse-of-rights principle (Byers, *Abuse of Rights: An Old Principle, A New Age*, 47 McGill L.J. 389 (2002)) and on the standard treatises (Dolzer & Schreuer, *Principles of International Investment Law* (2d ed. 2012); McLachlan, Shore & Weiniger, *International Investment Arbitration: Substantive Principles* (2d ed. 2017)). Verbatim triggers: `abuse of right`, `reasonably foreseeable`, `critical date`, `shell subsidiary`.

### D. The scoring grammar

The signal the instrument is built to detect is the intersection of the rings, and the scoring grammar follows from that. HIGH (≥70) requires two rings. MEDIUM (40–69) requires either one strong ring with a weaker second tie, or a judicial-measure case standing on its own. LOW (<40) is one weak ring or none, with extractives, sovereign debt, and intra-EU energy defaulting to LOW absent an IP or judicial angle. The full machine-readable frame — every phrase and weight, summing to 100 within each ring — is maintained in `fingerprint.yaml`.

## III. Source Architecture & Research Methods

### A. Source selection and triangulation

I selected sources to triangulate the event-space across several different kinds of channel: institutional dockets, primary-document archives, analytical writing, and the practitioner press. The specific open repositories are the ICSID docket; UNCTAD's Investment Dispute Settlement Navigator and *World Investment Report*; the italaw primary-document archive; IISD's Investment Treaty News; and IAReporter at headline level. The principle behind reading several at once is triangulation, a basic feature of research design: when two or more independent sources agree, what you have found is more likely to reflect a real development and less likely to be an artifact of one channel's idiosyncrasies (the triangulation logic discussed in *A Practical Framework for Conducting a Literature Review*, The Qualitative Report (Nova Southeastern Univ.)). These are the same repositories I use for manual backsourcing elsewhere in the project; the only difference is that the instrument reads all of them on a schedule rather than one case at a time.

### B. Collection method — an automated analog of our backsourcing workflow

The collection method mirrors the backsourcing-and-verification routine we adopted for the literature review, under which a substantive claim is traced back to its source in an official repository rather than accepted on the strength of a citation. The instrument retrieves each source's listing and extracts the candidate items. Where a listing exposes only a case name, it then retrieves the underlying page from that source's own repository, so that it has the substantive text to work with rather than a caption (Part IV). For every item it records provenance — the source, a stable identifier, the URL, and the access timestamp — so that any line in any digest can be traced back to the document that produced it. The recovered primary text, not the listing summary, governs the classification.

### C. Collection ethics

The instrument reads open sources only and does not circumvent access controls. It honors the Robots Exclusion Protocol (RFC 9309; Koster, Illyes, Zeller & Sassman, 2022): where a host's `robots.txt` disallows a path, as Google News presently disallows its RSS endpoint, the source is dropped and the omission is logged rather than evaded. It sends an identifying User-Agent that links back to the repository, waits at least three seconds between requests to any one domain, and never retrieves the body of a paywalled article (IAReporter is read at headline level only). Where a page layout shifts, a structural fallback selector takes over and the fallback is logged, and a source that fails returns an empty result rather than aborting the run. These constraints are the crawler analog of the access limitations I flag by hand in the bibliographies, stated openly rather than omitted.

## IV. Candidate Identification & Enrichment

A listing that shows only a case name, scored as-is, produces noise. Before classification, therefore, the most promising candidates are enriched: the instrument retrieves the source document, reduces it to its readable body, and selects a single **notable line**, the sentence carrying the highest density of doctrinal vocabulary, which is a term-frequency selection in the sense of Salton and McGill (1983). Much as a well-placed pin-cite lets a researcher locate the relevant passage in a backsourced bibliography, that line does two jobs: it gives the classifier enough substantive text to evaluate, and it gives the reader the one sentence worth seeing. Enrichment is capped per run to respect the collection-ethics budget of Part III.C, and paywalled sources are never opened.

## V. Classification Procedure — A Two-Stage Cascade

Classification proceeds in two stages, because recall and precision pull in opposite directions and each is better served by a different instrument.

**Stage one — lexical coding (deterministic, transparent).** Every candidate is scored against the vocabulary defined in `fingerprint.yaml` by summing the matched per-keyword weights within each ring, which is classical weighted term matching (Salton & McGill, 1983). This stage ranks candidates so that enrichment is spent on the highest-ranked, and it runs independently of whether a language model is available, so that even with no model the instrument still returns an ordered, inspectable, scored result.

**Stage two — contextual classification (paraphrase-tolerant).** The top-ranked candidates are then evaluated by a language model, Anthropic Claude or Google Gemini, selected at runtime, under a few-shot prompt that supplies the ring definitions and worked HIGH/MEDIUM/LOW exemplars, negatives included, so that the boundary is learned rather than merely the target. Few-shot prompting is used because it improves task adherence without fine-tuning (Brown et al., *Language Models are Few-Shot Learners*, NeurIPS 33 (2020)). The model must return strict JSON: a relevance score, the matched rings, thematic tags, a two-sentence annotation, and a verbatim citable line. On malformed output the pipeline retries once under a stricter instruction; on a second failure it records a zero tagged `classification_failed`; and on a quota or network error it falls back to the lexical score, so that a verdict is always produced.

## VI. Scoring, Calibration & Validation

### A. Calibration decisions

Three calibration decisions are worth stating plainly, because each is a judgment rather than a neutral fact.

First, a ring must earn its place. A ring counts as "present" only once its lexical subtotal reaches a floor of 12, which requires a substantive hit on the ring's vocabulary rather than a glancing brush against a single word. The purpose is to suppress the false intersection in which, for example, a mining claim mentions "investment" and is mistaken for the theme. In substance this is a deliberate minimum-term-frequency cut-off (Manning, Raghavan & Schütze, 2008).

Second, the digest threshold was lowered on purpose, from an initial 60 to 40, a reduction of twenty. A monitoring instrument is not an adjudicative one; its job is to surface leads, and the recall-for-precision trade was made consciously.

Third, the digest carries a minimum of six items each week, with no upper limit. Every item at or above the threshold is reported as a match, so a strong week reports all of them. When fewer than six items clear the threshold, the instrument fills the digest up to six with the closest near-misses, ranked by relevance and labeled as watch-list leads rather than matches. (A match is an item at or above the threshold; a watch-list item is one of the nearest misses, surfaced so that the digest is never thin.) This preference for recall over precision suits a surveillance instrument and would be wrong in an adjudicative one, and the watch-list label is there so that no reader mistakes a lead for a holding.

### B. Validation

I regression-tested the lexical scorer against the labeled exemplars in `fingerprint.yaml` (`tests/test_pipeline.py`), and it reproduces the intended band on all seven, the three negative examples included. The three seed awards, scored on their own text, return MEDIUM to HIGH. The instrument recognizes the cases that generated it, which is a face-validity check against the corpus from which the theme was induced (Saldaña; Linos & Carlson).

## VII. The Reporting Standard — The Digest as Annotated Bibliography

The weekly digest is structured as an annotated bibliography rather than a list of links, because the project's standard for a research deliverable is interpretive rather than merely descriptive. Each entry follows the annotated-bibliography conventions of the AALL *Law Library Journal* guidelines: a citation, followed by an annotation that is at once descriptive and evaluative, kept within the 50–200-word range those guidelines specify, with citation form per The Chicago Manual of Style (§§ 14.61–14.305) and URLs supplied liberally to aid retrieval. Consistent with the analytically engaged bibliography described in The Qualitative Report framework, each entry also reflects on fit — which rings the development implicates, and why it matters to the project — so that the bibliography performs interpretive work rather than functioning as a collection of references. Every entry names its source, links to the original, and quotes a verbatim notable line, which is what lets a reader proceed directly to backsourcing in the manner described in Part III.B. Where a source is paywalled, or a listing exposes only metadata, that limitation is stated rather than concealed.

## VIII. Reproducibility & State

Every processed item is recorded by source and stable identifier in `state/seen.json`, so that no item is ever classified or reported twice. The store bootstraps on the first run and treats a corrupt file as an empty slate rather than letting the corruption take the pipeline down with it. Each scheduled run commits its dated digest archive and its updated state back to the repository under version control, producing a complete, timestamped, replayable record of what was observed, when, and how it was scored — the automated analog of preserving the manual annotations as the project's "source of truth."

## IX. Limitations

Consistent with the project's practice of stating access and coverage limits openly rather than omitting them:

- **Construct validity.** The theme is induced from three awards and may under-represent doctrinal variants the seeds do not raise. This is mitigated, though not eliminated, by lightly weighted `theme_extension` terms for adjacent doctrines such as denial of benefits and substantial business activities.
- **Coverage is a lower bound.** Paywalls and `robots.txt` (Part III.C) place real material out of reach, and Google News RSS is presently disallowed and therefore inactive. The instrument reports a floor on what exists, not a complete census.
- **Thin metadata.** Where content sits behind authentication, a bare case name is the only available input, and the score can reflect only that.
- **Model variance.** Model outputs are non-deterministic; the strict-JSON contract, the single retry, the deterministic fallback, and the test suite together bound the variance without abolishing it.
- **A deliberate thumb on the scale.** Ring 2's weighting and the never-empty rule both favor recall, so MEDIUM and watch-list items are leads to run down rather than conclusions to cite.

## X. Methodological & Doctrinal Authorities

### A. Methodological authorities (instrument design and reporting standards)

- Saldaña, J., *The Coding Manual for Qualitative Researchers* (3d ed., SAGE) — coding cycles and analytic-memo framework underlying the fingerprint induction.
- Linos, K. & Carlson, M., *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017) — theoretically informed sampling and most-similar-case design, adapting qualitative method to legal writing.
- *A Practical Framework for Conducting a Literature Review*, The Qualitative Report (Nova Southeastern Univ.) — triangulation and the analytically engaged, project-fit-reflective bibliography.
- American Association of Law Libraries, *Law Library Journal* — *General Instructions & Sample Entries for Bibliographies* — annotated-bibliography standard (descriptive-and-evaluative annotations, approximately 50–200 words; citation per The Chicago Manual of Style §§ 14.61–14.305).
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
