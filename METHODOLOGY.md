# Methodology

This document specifies, granularly, how the ISDS Thematic Watcher identifies and
ranks investor–state dispute settlement (ISDS) developments, and grounds each design
decision in the relevant scholarly and technical literature. It is written to be
auditable: every stage states *what* it does, *why*, and *on whose authority*.

Full citations are collected in [§9 References](#9-references); in-text pointers use
author–year. The pipeline this document describes lives in `src/` and is exercised by
`tests/`.

---

## 1. Research design and rationale

The Watcher is a **standing thematic-surveillance instrument**. Its object is not "all
ISDS news" but a narrowly specified doctrinal phenomenon: the convergence of
intellectual-property-as-investment claims, challenges to regulatory or judicial
measures, and the jurisdictional/admissibility doctrines that increasingly dispose of
such claims. Because the target is a *theme* rather than a keyword, the design follows
the logic of **qualitative thematic analysis** (Braun & Clarke, 2006): a theme is built
from a corpus of exemplars, codified into a reusable analytic frame, and then applied
to new material with explicit, revisable criteria.

The three "seed" awards — *Philip Morris v. Australia* (2015), *Eli Lilly v. Canada*
(2017), and *Bridgestone v. Panama* (2020) — function as the **coding corpus** from
which the theme is induced. This is a deliberate analogue of Braun & Clarke's (2006)
recursive move between data and codes: the doctrinal vocabulary used by the tribunals
is extracted verbatim and promoted to analytic categories (the "rings," §2). Using the
parties' and tribunals' *own language* as the unit of coding follows the
information-retrieval principle that the most discriminating index terms are those that
actually occur in relevant documents (Salton & McGill, 1983; Manning, Raghavan &
Schütze, 2008).

---

## 2. Theoretical framework: the three-ring thematic fingerprint

The theme is operationalised as the **intersection of three doctrinal rings**. Each ring
is independently grounded in the investment-law literature; the watcher's novelty is
treating their *overlap* as the signal.

### Ring 1 — IP-as-investment
That intellectual property (patents, trademarks/licences, copyrights, geographical
indications, data exclusivity, goodwill) can constitute a "covered investment" is now an
established but contested proposition (Mercurio, 2012; Correa & Viñuales, 2016). Mercurio
(2012) documents how investment treaties were drafted broadly enough to capture IP, while
Correa & Viñuales (2016) interrogate *how open the gates are* — precisely the standing and
characterisation questions the seeds raise (e.g., the *Bridgestone* licensor/licensee
split). Verbatim triggers (`promise utility doctrine`, `covered investment`,
`exploitation of the trademark`) are drawn from the seed awards.

### Ring 2 — Regulatory or judicial measure as the disputed conduct (extra weight)
Two of three seeds challenge a **domestic court judgment** rather than executive or
legislative action, invoking the **denial-of-justice** standard. Paulsson's (2005)
canonical treatment supplies the doctrinal yardstick the tribunals apply — that state
responsibility for judicial acts attaches only at a high threshold of "manifest
injustice," not mere error. The seed tribunals' formulations (`egregious and shocking`,
`manifestly unjust judgment`, `egregiously wrong that no honest or competent court
could` have reached it) are Paulsson's standard in operation, and are encoded verbatim.
Because judicial-measure cases are both doctrinally distinctive and over-represented in
the seeds, this ring is given **extra weight**: a credible challenge to a court judgment
reaches at least the MEDIUM band on its own (§6). This is a deliberate, documented
recall bias, justified by the corpus composition (Braun & Clarke, 2006, on prevalence as
a coding criterion).

### Ring 3 — Jurisdictional and admissibility doctrines
The seeds are united less by their merits than by the **threshold doctrines** that
decided them: abuse of right, treaty-shopping, foreseeability of the dispute, corporate
restructuring to obtain treaty protection, the definition of "investor," and standing to
plead denial of justice. The governing scholarship is Baumgartner (2016) on treaty
shopping and the abuse-of-right limitation, building on the general doctrine of abuse of
rights in international law (Byers, 2002). *Philip Morris*' "reasonably foreseeable
dispute"/"critical date" reasoning and *Bridgestone*'s "shell subsidiary" abuse
allegation are textbook instances (Dolzer & Schreuer, 2012; McLachlan, Shore & Weiniger,
2017), and supply the ring's verbatim triggers.

### Combination logic
- **HIGH (≥70):** intersection of any two rings — the defining signature of the theme.
- **MEDIUM (40–69):** one strong ring plus a weaker tie, *or* any judicial-measure case
  alone (Ring 2 extra weight).
- **LOW (<40):** a single weak ring or none; vanilla expropriation, extractives,
  sovereign debt, and intra-EU energy default here absent an IP or judicial-measure
  angle.

The full machine-readable frame, with per-keyword weights summing to 100 within each
ring, is `fingerprint.yaml`.

---

## 3. Source selection and corpus construction

Sources were chosen to **triangulate** the disputed event-space across institutional,
practitioner, and press channels (the multiple-sources logic of Denzin, 1978): the ICSID
docket, UNCTAD's Investment Dispute Settlement Navigator, italaw's primary-document
repository, IISD's Investment Treaty News, and practitioner headlines (IAReporter).
UNCTAD's Navigator and *World Investment Report* series are the field's standard
open-data references (UNCTAD, annual).

Selection constraints, each operationalised in `src/sources/base.py`:
1. **Open access only.** Paywalled or authentication-gated content is excluded; IAReporter
   is read at **headline level only** and article bodies are never fetched.
2. **Respectful crawling.** The crawler honours the Robots Exclusion Protocol
   (Koster, Illyes, Zeller & Sassman, 2022 — RFC 9309), sends an identifying
   User-Agent linking to this repository, and rate-limits to ≥3 s per domain. Where a
   host's `robots.txt` disallows a path (e.g., Google News `/rss/`), the source is
   dropped and logged rather than circumvented.
3. **Graceful degradation.** Every source uses a primary selector plus a structural
   fallback and returns an empty result (logged) rather than failing the run, reflecting
   standard robustness practice for web-scale extraction (Manning, Raghavan & Schütze,
   2008, ch. 20 on web crawling).

---

## 4. Candidate extraction and enrichment

Each source yields `CandidateItem`s (source, stable id, URL, title, publication date,
summary, raw text). Listing pages typically expose only a case name; to give the
classifier and the reader genuine substance, the top-ranked candidates are **enriched**
(`src/enrich.py`): the source page is fetched politely, body paragraphs are extracted,
and a **notable line** is selected as the sentence with the highest density of doctrinal
terms (a term-frequency heuristic in the spirit of Salton & McGill, 1983). Enrichment is
capped per run (`ENRICH_TOP_N`) to bound fetch volume, consistent with the politeness
constraints in §3. Paywalled sources are never body-fetched.

---

## 5. Classification procedure

Classification is a **two-stage cascade**, mirroring the retrieve-then-rank architecture
standard in information retrieval (Manning, Raghavan & Schütze, 2008):

1. **Keyword pre-scoring (cheap, deterministic).** Every candidate is scored against the
   `fingerprint.yaml` lexicon by summing matched per-keyword weights within each ring.
   This is classical weighted term matching (Salton & McGill, 1983) and serves both as a
   ranking signal for enrichment (§4) and as an **offline fallback** when no LLM is
   configured — guaranteeing the system degrades to a transparent, auditable scorer.

2. **LLM classification (contextual).** The top candidates are classified by a large
   language model (Anthropic Claude or Google Gemini, selected at runtime) using a
   **few-shot prompt** (`prompts/classifier.txt`) that supplies the ring definitions and
   worked HIGH/MEDIUM/LOW exemplars, including negative cases. Few-shot in-context
   prompting is used because it materially improves task adherence without fine-tuning
   (Brown et al., 2020). The model must return strict JSON (score, matched rings,
   thematic tags, two-sentence annotation); on a parse failure the pipeline retries once
   with a stricter instruction, then fails soft to a zero score tagged
   `classification_failed`. A provider/quota error falls back to the keyword score, so a
   classification is always produced.

The two stages are complementary: the lexicon guarantees recall on the exact doctrinal
vocabulary, while the LLM supplies precision and paraphrase tolerance on enriched text.

---

## 6. Scoring model, thresholds, and validation

- **Within-ring weights** sum to 100, with the heaviest weights on the most
  discriminating verbatim phrases (e.g., `abuse of right`, `denial of justice`,
  `promise utility doctrine`).
- **Band promotion** follows the combination logic in §2. The keyword scorer treats a
  ring as genuinely *present* only above a floor (subtotal ≥ 12), which suppresses
  incidental single-keyword hits — a precision safeguard analogous to a minimum
  term-frequency cut-off (Manning, Raghavan & Schütze, 2008).
- **Threshold.** The digest gate is set at **40** (lowered from an initial 60 to widen
  recall). Because a narrow theme produces many empty weeks, the pipeline additionally
  guarantees a non-empty digest by surfacing the top *N* most-relevant items down to a
  relevance floor (`MIN_DIGEST_ITEMS`, `RELEVANCE_FLOOR`). This is an explicit
  recall-over-precision choice for a monitoring (as opposed to adjudicative) instrument.
- **Validation.** The keyword scorer is regression-tested against the labelled few-shot
  set in `fingerprint.yaml` (`tests/test_pipeline.py`): it reproduces the expected
  HIGH/MEDIUM/LOW band on 7/7 gold examples, and the three seed awards themselves score
  MEDIUM–HIGH on their own text. This is a face-validity check against the coding corpus
  from which the theme was induced (Braun & Clarke, 2006).

---

## 7. Deduplication, state, and reproducibility

A persistent `state/seen.json` records every `(source, source_id)` processed, so each
item is classified and reported once; the store bootstraps to an empty object on first
run and treats corruption as empty (never fatal). Runs are idempotent over their input
window, and the weekly GitHub Actions job commits the digest archive and updated state
back to the repository, giving a complete, time-stamped audit trail.

---

## 8. Limitations and threats to validity

- **Construct validity.** The theme is induced from three awards; it may under-represent
  doctrinal variants absent from the seeds (mitigated by `theme_extension` keywords for
  cognate doctrines such as denial of benefits and substantial business activities).
- **Coverage.** Open-source and robots constraints (§3) exclude paywalled reporting and
  some listings; Google News RSS is currently robots-disallowed and therefore inactive.
  Coverage is thus a lower bound, not a census.
- **Thin metadata.** Listing sources expose bare case names; enrichment (§4) mitigates
  but cannot recover content behind authentication.
- **LLM variance.** Model outputs are non-deterministic; the strict-JSON contract,
  one-retry policy, deterministic keyword fallback, and regression tests bound this risk.
- **Recall bias by design.** The extra weight on Ring 2 and the non-empty-digest
  guarantee deliberately favour recall; readers should treat MEDIUM/WATCH items as leads,
  not conclusions.

---

## 9. References

- Baumgartner, J. (2016). *Treaty Shopping in International Investment Law.* Oxford University Press.
- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology, 3*(2), 77–101.
- Brown, T. B., et al. (2020). Language Models are Few-Shot Learners. *Advances in Neural Information Processing Systems (NeurIPS) 33.*
- Byers, M. (2002). Abuse of Rights: An Old Principle, A New Age. *McGill Law Journal, 47*(2), 389–431.
- Correa, C. M., & Viñuales, J. E. (2016). Intellectual Property Rights as Protected Investments: How Open are the Gates? *Journal of International Economic Law, 19*(1), 91–120.
- Denzin, N. K. (1978). *The Research Act: A Theoretical Introduction to Sociological Methods.* McGraw-Hill.
- Dolzer, R., & Schreuer, C. (2012). *Principles of International Investment Law* (2nd ed.). Oxford University Press.
- Koster, M., Illyes, G., Zeller, H., & Sassman, L. (2022). *Robots Exclusion Protocol.* RFC 9309, IETF.
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press.
- McLachlan, C., Shore, L., & Weiniger, M. (2017). *International Investment Arbitration: Substantive Principles* (2nd ed.). Oxford University Press.
- Mercurio, B. (2012). Awakening the Sleeping Giant: Intellectual Property Rights in International Investment Agreements. *Journal of International Economic Law, 15*(3), 871–915.
- Paulsson, J. (2005). *Denial of Justice in International Law.* Cambridge University Press.
- Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval.* McGraw-Hill.
- UNCTAD (annual). *World Investment Report* and *Investment Dispute Settlement Navigator.* United Nations Conference on Trade and Development.

> **Note on seed awards.** *Philip Morris Asia Ltd v. Commonwealth of Australia*, PCA Case
> No. 2012-12, Award on Jurisdiction and Admissibility (17 Dec 2015); *Eli Lilly and Co. v.
> Government of Canada*, ICSID Case No. UNCT/14/2, Final Award (16 Mar 2017); *Bridgestone
> Licensing Services, Inc. and Bridgestone Americas, Inc. v. Republic of Panama*, ICSID Case
> No. ARB/16/34, Award (14 Aug 2020). Doctrinal vocabulary was extracted verbatim from these
> awards; see `PLAN.md` for the per-ring extraction.
