**TO:** Dr. Ximena Benavides, Department of Legal Studies, Terry College of Business
**FROM:** Emory Williams, Undergraduate Research Assistant
**DATE:** 06/08
**RE:** Methodology Memo — The ISDS Thematic Watcher: design, justification, and validation of an automated thematic-surveillance instrument for the IP-as-investment / judicial-measure / jurisdictional-admissibility intersection

---

## I. Research Question & Scope

This memo sets out how the ISDS Thematic Watcher works, and why I built each part of it the way I did. The Watcher is the automated monitoring tool I put together for this project. Underneath the substantive questions we have been chasing in the literature review sits a smaller, more practical one, and that is the question the tool actually answers. Across the open record of investor-State practice, which new developments fall inside the narrow intersection we care about, where intellectual property is asserted as a covered investment, where the disputed conduct is a regulatory or judicial measure, and where the case is decided on jurisdiction or admissibility? And how do you keep checking for them, week after week, without a Westlaw or a Kluwer subscription? That second half matters as much as the first.

I should be clear about what this memo is not. It does not relitigate whether trade secrets or clinical data qualify as protected investments; that argument belongs to the Ferguson and Kim memos, not here. What it does is explain how the tool turns our doctrinal frame into a repeatable detection procedure, one you can audit and, if you disagree with a call, push back on. The order I follow is the order the tool runs in: the theoretical frame (Part II), then the sources and how I collect from them (Part III), candidate identification and enrichment (Part IV), the two-stage classification cascade (Part V), scoring and validation (Part VI), the reporting standard for the digest itself (Part VII), reproducibility (Part VIII), and an honest account of the limits (Part IX). The authorities I relied on are gathered at the end (Part X).

## II. Theoretical Framework — The Three-Ring Thematic Fingerprint

### A. Why a thematic instrument, and not a keyword search

What we are watching for is not a word. It is a relationship among three doctrines, and you cannot collapse a relationship into a search term without throwing away the thing that makes it interesting. A case can use the word "patent" thirty times and be beside the point. Another can never once say "abuse of right" and sit right in the middle of the theme. So the problem is interpretive before it is technical, and it is genuinely hard, because I was asking the tool to recognize a pattern it had only seen three times.

The discipline that handles exactly this problem is qualitative coding, so that is where I started. I built the fingerprint the way Linos and Carlson tell legal writers to choose their examples, through theoretically informed sampling and a most-similar-case design, the very techniques they say law scholars neglect when they grab examples at random and then run only doctrinal analysis over them (Linos & Carlson, *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017)). I was not trying to assemble a representative sample of all ISDS. I was trying to assemble three cases that look alike along the one dimension I care about, which is the whole point of a most-similar-case design. The coding came next. I pulled the operative phrases out of the awards, sorted them into categories, and kept refining those categories against the text, which is the first- and second-cycle coding and analytic-memo procedure in Saldaña, *The Coding Manual for Qualitative Researchers* (3d ed.).

### B. The seed corpus

I chose three awards. On their facts they have nothing to do with one another, yet they share the structural signature the project tracks:

- *Philip Morris Asia Ltd v. Commonwealth of Australia*, PCA Case No. 2012-12, Award on Jurisdiction and Admissibility (17 Dec. 2015) — tobacco plain-packaging legislation aimed at trademark rights, thrown out on abuse of right after the claimant restructured to pick up treaty protection over a dispute that was already "reasonably foreseeable."
- *Eli Lilly & Co. v. Government of Canada*, ICSID Case No. UNCT/14/2, Final Award (16 Mar. 2017) — pharmaceutical patents struck down under the "promise utility doctrine," which Lilly turned into a challenge to a judicial measure under the NAFTA Article 1105 minimum standard, pleaded as denial of justice.
- *Bridgestone Licensing Servs., Inc. & Bridgestone Ams., Inc. v. Republic of Panama*, ICSID Case No. ARB/16/34, Award (14 Aug. 2020) — a trademark licensor/licensee structure, a denial-of-justice claim over a Supreme Court judgment, and a "shell subsidiary" abuse-of-process allegation that reads like an echo of *Philip Morris*.

My coding unit was the tribunals' own language. I extracted the operative phrases verbatim and promoted them to index terms; the full per-ring extraction is in `PLAN.md`. That choice is deliberate. It follows the oldest rule in information retrieval, which is that the index terms that best separate relevant documents from the rest are the ones that actually appear in the relevant documents (Salton & McGill, *Introduction to Modern Information Retrieval* (1983); Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (2008)). When a news write-up describes a case like these, it tends to reach for the same vocabulary the tribunal used. The fingerprint is built to hear that echo.

### C. The three rings

**Ring 1 — Intellectual property as a protected investment.** Whether intellectual property counts as a covered "investment," and on what conditions, is the threshold question that keeps recurring in our reading (Mercurio, *Awakening the Sleeping Giant*, 15 J. Int'l Econ. L. 871 (2012); Correa & Viñuales, *Intellectual Property Rights as Protected Investments: How Open are the Gates?*, 19 J. Int'l Econ. L. 91 (2016)). It bites hardest where the asset is informational, or where ownership is split across a holding entity and an operating one. That is the *Bridgestone* posture exactly, and it is the same vulnerability the Ferguson and Kim memos flag for trade secrets and clinical data. The threshold also drags in the Salini criteria, contribution, duration, risk, and contribution to the host economy, on which tribunals keep a good deal of discretion (cf. *Salini Costruttori S.p.A. v. Morocco*, ICSID Case No. ARB/00/4). Verbatim triggers: `covered investment`, `promise utility doctrine`, `exploitation of the trademark`.

**Ring 2 — A regulatory or judicial measure as the disputed conduct (weighted).** Two of my three seeds do not go after an executive act at all. They go after a court, and they plead denial of justice. Paulsson is the governing source here, and his line is a demanding one: a State answers for its judiciary only at the far end, for manifest injustice, not for ordinary error (Paulsson, *Denial of Justice in International Law* (2005)). You can hear his standard in the seed tribunals almost word for word, in conduct "egregious and shocking," in a "manifestly unjust judgment," in a ruling so "egregiously wrong that no honest or competent court could" have reached it. Because the corpus leans on this ring, I let the tool lean on it too. A credible attack on a court judgment clears the MEDIUM band by itself. Weighting a category by how often it shows up in the coding corpus is a recognized move, not a thumb on the scale I am hiding (Saldaña, *Coding Manual*). Verbatim triggers: `denial of justice`, `manifestly unjust judgment`, `minimum standard of treatment`.

**Ring 3 — The case is decided at the threshold, not on the merits.** Here is the quiet thing the three seeds share. Nobody ever reached the merits. The public-interest questions everyone cared about went unanswered, because each case died on jurisdiction and admissibility, on abuse of right, treaty shopping, the foreseeability of the dispute, restructuring to capture treaty protection, and the contested meaning of "investor." Baumgartner is the synthesis I leaned on (Baumgartner, *Treaty Shopping in International Investment Law* (2016)), and she rests in turn on the older abuse-of-rights principle (Byers, *Abuse of Rights: An Old Principle, A New Age*, 47 McGill L.J. 389 (2002)) and on the standard treatises (Dolzer & Schreuer, *Principles of International Investment Law* (2d ed. 2012); McLachlan, Shore & Weiniger, *International Investment Arbitration: Substantive Principles* (2d ed. 2017)). Verbatim triggers: `abuse of right`, `reasonably foreseeable`, `critical date`, `shell subsidiary`.

### D. The scoring grammar

The thing the tool is built to find is the overlap, and the scoring follows from that. Two rings together is HIGH (≥70). One strong ring with a weaker second tie is MEDIUM (40–69), and so is a judicial-measure case that stands on its own. Everything else is LOW (<40): a single weak ring, or none, with extractives, sovereign debt, and intra-EU energy falling to LOW unless an IP or judicial angle pulls them back up. The machine-readable version of all of this, every phrase and weight, summing to 100 inside each ring, lives in `fingerprint.yaml`.

## III. Source Architecture & Research Methods

### A. Source selection and triangulation

I picked sources to triangulate the same event from more than one direction, on the simple principle that when independent channels agree, you are probably looking at signal rather than noise (the triangulation logic in *A Practical Framework for Conducting a Literature Review*, The Qualitative Report (Nova Southeastern Univ.)). The tool reads the ICSID docket, UNCTAD's Investment Dispute Settlement Navigator and *World Investment Report*, the italaw primary-document archive, IISD's Investment Treaty News, and IAReporter at the headline level. These are the same open repositories I already use when I backsource by hand for the project, the difference being that the tool reads them every week instead of one case at a time.

### B. Collection method — an automated analog of our backsourcing workflow

I designed the collection step to mirror the backsourcing routine we settled on at our first meeting, the one where a claim is run back to its source in an official repository rather than taken on trust from a citation. The tool does four things. It pulls each source's listing. It extracts the candidate items. Where a listing gives up only a case name, it goes and fetches the underlying page from that source's own repository so it has real text to work with, not a caption (Part IV). And it records the provenance of everything, the source, a stable identifier, the URL, and a timestamp, so that any line in any digest can be traced straight back to the document it came from. It is the same "source of truth" discipline as the memos. The recovered text governs, not the listing blurb.

### C. Collection ethics

The tool reads open sources only, and it does not work around access controls. It honors the Robots Exclusion Protocol (RFC 9309; Koster, Illyes, Zeller & Sassman, 2022). When a host's `robots.txt` disallows a path, as Google News currently does for its RSS endpoint, the tool drops that source and writes the omission to the log; it does not try to get around it. It sends an identifying User-Agent that links back to the repository, waits at least three seconds between hits on any one domain, and never pulls the body of a paywalled article (IAReporter is read at the headline level, and no further). When a page layout shifts, a structural fallback selector takes over and the fallback gets logged. A source that fails returns nothing and the run continues. All of this is the crawler's version of the access limitations I already flag by hand in the bibliographies, and I have set them down here on purpose.

## IV. Candidate Identification & Enrichment

A listing that hands you "*Ferrer v. Ecuador*" and stops there is not enough to score. Score it as-is and you are scoring noise. So before anything is classified, the tool enriches the strongest candidates: it fetches the source page, strips it down to the readable body, and picks one **notable line**, the sentence carrying the densest cluster of doctrinal vocabulary, which is a term-frequency selection in the Salton and McGill sense (Salton & McGill, 1983). That line earns its keep twice over. It gives the classifier real text to reason over, and it gives the reader the one sentence worth pulling. I capped enrichment per run to stay inside the politeness budget from Part III.C, and paywalled pages are never opened.

## V. Classification Procedure — A Two-Stage Cascade

Classification runs in two stages, and the reason is that recall and precision pull against each other. Rather than split the difference, I gave each one the stage it is good at.

**Stage one — lexical coding (deterministic, transparent).** Every candidate is scored against the `fingerprint.yaml` vocabulary, summing the matched per-keyword weights within each ring. That is classical weighted term matching (Salton & McGill, 1983). It does double duty. It ranks the candidates so enrichment spends its budget on the most promising, and it serves as a fully offline fallback, so that even with no language model the tool still returns a scored, inspectable result.

**Stage two — contextual classification (paraphrase-tolerant).** The enriched front-runners then go to a language model, Anthropic Claude or Google Gemini, chosen at runtime. The prompt is few-shot: it hands the model the ring definitions and worked HIGH/MEDIUM/LOW examples, negatives included, so the model learns the boundary and not just the target. I went with few-shot because it lifts task adherence sharply and costs no fine-tuning (Brown et al., *Language Models are Few-Shot Learners*, NeurIPS 33 (2020)). The model has to return strict JSON, a relevance score, the matched rings, thematic tags, a two-sentence annotation, and a verbatim citable line. If the JSON comes back malformed, the pipeline retries once under a stricter instruction; if it fails a second time, it records a zero tagged `classification_failed`; and if the provider errors or the quota runs out, it drops back to the lexical score. One way or another, a verdict comes out. The two stages cover each other, the lexicon holding recall on the tribunals' exact phrasing while the model catches the same idea in paraphrase.

## VI. Scoring, Calibration & Validation

### A. Three calibration calls, and why each is a judgment

*A ring has to earn its place.* A ring only counts as "present" once its lexical subtotal clears a floor of 12, which I take to mean one real hit rather than a glancing brush against a single word. The point is to kill the false intersection, the one where a mining claim happens to say "investment" and gets mistaken for the theme. In substance it is a minimum-term-frequency cut-off (Manning, Raghavan & Schütze, 2008).

*I lowered the gate on purpose.* The digest threshold sits at 40, down from the 60 I started with. A monitor is not a court. Its job is to surface leads, and I made the recall-for-precision trade with my eyes open.

*The digest should never come back empty.* A theme this narrow goes quiet for stretches, and an empty email is how you teach a reader to stop opening it. So when too few items clear the gate, the tool surfaces the strongest of what is left, down to a relevance floor, and labels it watch-list rather than match. That is recall over precision by design. It suits a surveillance tool and would be wrong in an adjudicative one, and I flag it so nobody reads a lead as a holding.

### B. Validation

I regression-test the lexical scorer against the labeled examples in `fingerprint.yaml` (`tests/test_pipeline.py`), and it lands the intended band on all seven, negatives and all. The three seed awards, scored on their own text, come back MEDIUM to HIGH. In other words, the tool recognizes the cases that produced it. That is a face-validity check against the corpus the theme was induced from, which is how qualitative method treats fit-to-exemplars in the first place (Saldaña; Linos & Carlson).

## VII. The Reporting Standard — The Digest as Annotated Bibliography

I structured the weekly digest as an annotated bibliography, not a list of links, because our standard for a research deliverable has always been interpretive rather than merely descriptive. Each entry follows the annotated-bibliography conventions in the AALL *Law Library Journal* guidelines. The citation comes first. Then an annotation that is at once descriptive and evaluative, kept inside the 50-to-200-word range those guidelines call for, with citation form per The Chicago Manual of Style (§§ 14.61–14.305) and URLs supplied more freely than the minimum, because the point is to make retrieval easy. Following the analytically engaged bibliography described in The Qualitative Report framework, each entry also says something about fit, which rings the development touches and why it matters to us, so the bibliography does interpretive work instead of just collecting references. Every entry names its source, links the original, and quotes a verbatim notable line, which is what lets a reader move straight into backsourcing the way Part III.B describes. Where a source is paywalled, or a listing hands over only metadata, I say so rather than paper over it.

## VIII. Reproducibility & State

Every item the tool has processed is recorded by source and stable identifier in `state/seen.json`, so nothing gets classified or reported twice. The store builds itself on the first run, and it treats a corrupt file as an empty slate rather than letting the corruption take the whole pipeline down with it. Each scheduled run commits its dated digest archive and its updated state back to the repository under version control. What you end up with is a complete, timestamped, replayable record of what was seen, when, and how it scored, which is the automated counterpart of keeping my manual annotations as the project's "source of truth."

## IX. Limitations

In keeping with how we handle access and coverage gaps elsewhere in the project, I state them rather than leave them out:

- **Construct validity.** The theme is induced from three awards, and it may under-represent doctrinal variants the seeds never raised. I mitigate that, though I cannot eliminate it, with lightly weighted `theme_extension` terms for adjacent doctrines such as denial of benefits and substantial business activities.
- **Coverage is a lower bound.** Paywalls and `robots.txt` (Part III.C) keep real material out of reach, and Google News RSS is disallowed at the moment and therefore dark. What the tool reports is a floor on what exists, not a census.
- **Thin metadata.** Where content sits behind authentication, a bare case name is the only input there is, and the score can only reflect that.
- **Model variance.** The model is non-deterministic. The strict-JSON contract, the single retry, the deterministic fallback, and the test suite hold the variance in check without ever abolishing it.
- **A deliberate thumb on the scale.** Ring 2's weighting and the never-empty rule both favor recall, which is why I treat MEDIUM and watch-list items as leads to run down, not conclusions to cite.

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

*Methodological note.* The memo follows the law-office-memorandum conventions we use across the project (CUNY; Columbia; Johnson, 2023). Its reporting standards, the descriptive-and-evaluative annotation, the note on fit, and the explicit statement of verification limits, track the AALL annotated-bibliography guidelines and the analytic-memo framework of Saldaña and Linos & Carlson, and they line up with the backsourcing method I describe in Part III.B.
