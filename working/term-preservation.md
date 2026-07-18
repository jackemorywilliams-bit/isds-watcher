# Term-preservation list — ISDS Thematic Watcher methodology

Every term below was verified against this repository's actual code and docs (file
paths cited per item), not from memory. These are the terms that MUST survive a Walter
Writes humanization pass verbatim. Paste the relevant blocks inline into each Block B
repair subagent.

> Corrections to the original Cowork prompt's term list (that prompt described a
> *different* system): this repo runs **Monday 13:00 UTC**, not "Sunday 6 PM Eastern";
> it uses **HIGH / MEDIUM / LOW** bands and 0–100 scores, not "priority-4/priority-5"
> tiers; it **fetches / retrieves** source pages (it is a scraper), so do **not** impose
> "synthesizes, not scrapes"; and it references **only the Bridgestone 2020 Award** — there
> is no "2017 Expedited Objections" moment anywhere in this repo, so do not introduce one.
> Sources are ICSID/UNCTAD/italaw/IISD/IAReporter, not Google Alerts/Scholar/SSRN/Kluwer/Westlaw.

## 1. Case names and dockets (verbatim; dockets are invariant)
Source: `METHODOLOGY.md` §II.B, `PLAN.md`, `seeds/` filenames.
- *Philip Morris Asia Ltd v. Commonwealth of Australia* (short form used: *Philip Morris Asia Ltd v. Australia*), **PCA Case No. 2012-12**, Award on Jurisdiction and Admissibility (17 Dec. 2015).
- *Eli Lilly & Co. v. Government of Canada* (short form used: *Eli Lilly & Co. v. Canada*), **ICSID Case No. UNCT/14/2**, Final Award (16 Mar. 2017).
- *Bridgestone Licensing Servs., Inc. & Bridgestone Ams., Inc. v. Republic of Panama* (short form used: *Bridgestone Licensing Servs. v. Panama*), **ICSID Case No. ARB/16/34**, Award (14 Aug. 2020).
- *Salini Costruttori S.p.A. v. Morocco*, **ICSID Case No. ARB/00/4** (Decision on Jurisdiction, 2001).

The four docket strings — `PCA Case No. 2012-12`, `ICSID Case No. UNCT/14/2`, `ICSID Case No. ARB/16/34`, `ICSID Case No. ARB/00/4` — must appear character-for-character. Italicized case names must stay italicized.

## 2. Source names (verbatim; these are the actual sources)
Source: `src/sources/*.py` `name=` fields; `METHODOLOGY.md` §III.A.
Internal identifiers: `iisd_itn`, `italaw`, `icsid`, `unctad_isds`, `iareporter_headlines`, `google_news_rss`, `pca_press`.
Human-facing names that must survive in the prose:
- the **ICSID** docket
- **UNCTAD**'s **Investment Dispute Settlement Navigator** and **World Investment Report**
- the **italaw** primary-document archive
- **IISD**'s **Investment Treaty News**
- **IAReporter** (read at headline level only)
- **Google News RSS** (currently disallowed by `robots.txt`, therefore inactive)
Do not let Walter Writes invent, merge, or substitute source names (e.g. no "Westlaw," "Kluwer," "Google Alerts," "Google Scholar," "SSRN").

## 3. Schedule (verbatim)
Source: `.github/workflows/weekly.yml` → `cron: "0 13 * * 1"`.
- The watcher runs **every Monday at 13:00 UTC**. Not Sunday, not 6 PM Eastern.

## 4. Classification bands and parameters (as implemented)
Source: `fingerprint.yaml` (`threshold: 40`, `high: 70`, `medium: 40`, `low: 0`); `src/classify.py` (`PRESENT_FLOOR = 12`, `STRONG_SUBTOTAL = 18`, `EXTRA_WEIGHT_RING = "judicial_or_regulatory_measure"`); `src/config.py` (`MIN_DIGEST_ITEMS = 10`, `RELEVANCE_FLOOR = 15`, `ENRICH_TOP_N = 24`).
- Bands: **HIGH (≥ 70)**, **MEDIUM (40–69)**, **LOW (< 40)**. Scores are integers **0–100**.
- Digest **threshold is 40** (lowered from an initial 60).
- A ring counts as "present" only at a lexical subtotal of **≥ 12**; a "strong" single-ring subtotal is **≥ 18**.
- The **weighted** ring is the judicial/regulatory one; it can reach MEDIUM on its own.
- There are **no** "priority-4/priority-5 items" and no "source tiers" in this system — do not introduce them.

## 5. Ring keys and names (verbatim)
Source: `src/classify.py` `VALID_RINGS`, `fingerprint.yaml`.
- Exact keys: `ip_as_investment`, `judicial_or_regulatory_measure`, `jurisdictional_admissibility`.
- Human names: "IP as a protected investment" (Ring 1); "a regulatory or judicial measure as the disputed conduct" (Ring 2, weighted); "a jurisdictional or admissibility doctrine" (Ring 3).

## 6. Models and provider switch (verbatim)
Source: `src/classify.py`.
- Default models: **`gemini-2.0-flash`** and **`claude-haiku-4-5-20251001`**.
- Provider selected at runtime by **`MODEL_PROVIDER`** (`claude` | `gemini`). Classification is **few-shot, strict-JSON**, with one retry then a `classification_failed` zero.

## 7. File and artifact names (verbatim, keep in backticks)
Source: repo tree.
- `fingerprint.yaml`, `state/seen.json`, `PLAN.md`, `tests/test_pipeline.py`, `robots.txt`, and the tags `theme_extension` and `classification_failed`.

## 8. Doctrinal trigger phrases (verbatim; do NOT paraphrase or flatten)
Source: `fingerprint.yaml` keyword phrases.
Ring 1: "covered investment", "promise utility doctrine", "promise doctrine", "utility requirement", "patent invalidation", "intellectual property", "trademark", "exploitation of the trademark", "licenses that constitute its investment", "licensor", "licensee", "brand value", "geographical indication", "data exclusivity", "copyright".
Ring 2: "denial of justice", "judicial measure", "domestic court", "Supreme Court", "judicial conduct", "judicial propriety", "manifestly unjust judgment", "shocks a sense of judicial propriety", "egregiously wrong that no honest or competent court could", "systemic failure in the administration of justice", "gross denial of justice, manifest arbitrariness, blatant unfairness", "minimum standard of treatment", "manifest arbitrariness", "arbitrary or discriminatory", "Plain Packaging Measures", "public-interest legislation", "dramatic change in the utility requirement", "NAFTA Article 1105".
Ring 3: "abuse of right", "abuse of process", "treaty shopping", "corporate restructuring", "restructure its investment to gain Treaty protection", "reasonably foreseeable", "pre-existing or reasonably foreseeable dispute", "critical date", "treaty protection", "shell subsidiary", "abusive tactics", "definition of investor", "standing of licensor vs licensee", "standing to claim denial of justice when not a party", "exhaustion of local remedies", "denial of benefits", "substantial business activities", "Salini criteria".
Hard rule: **"denial of justice" must never be flattened to "injustice" or "unfair treatment."**

## 9. Author / citation names (verbatim, with years and reporters)
Source: `METHODOLOGY.md` §X.
- Methodological: Saldaña, *The Coding Manual for Qualitative Researchers* (3d ed.); Linos & Carlson, *Qualitative Methods for Law Review Writing*, 84 U. Chi. L. Rev. 213 (2017); *A Practical Framework for Conducting a Literature Review*, The Qualitative Report; AALL *Law Library Journal*; The Chicago Manual of Style §§ 14.61–14.305; CUNY School of Law; Columbia Law School; Eric E. Johnson (2023); Salton & McGill (1983); Manning, Raghavan & Schütze (2008); Brown et al., *Language Models are Few-Shot Learners*, NeurIPS 33 (2020); Koster, Illyes, Zeller & Sassman, RFC 9309 (2022).
- Doctrinal: Paulsson, *Denial of Justice in International Law* (2005); Baumgartner, *Treaty Shopping in International Investment Law* (2016); Byers, 47 McGill L.J. 389 (2002); Mercurio, 15 J. Int'l Econ. L. 871 (2012); Correa & Viñuales, 19 J. Int'l Econ. L. 91 (2016); Kingsbury & Schill (IILJ Working Paper 2009/6); Dolzer & Schreuer (2d ed. 2012); McLachlan, Shore & Weiniger (2d ed. 2017).

<!-- graph:auto start -->
Map: [[Workflow]]
<!-- graph:auto end -->
