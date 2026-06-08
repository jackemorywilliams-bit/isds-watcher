# ISDS Thematic Watcher — PLAN

Generated in Phase 1 from full-text extraction of the three seed awards. Verbatim
doctrinal phrases below were mined directly from the PDFs (via `pdftotext`) and are
tagged to the seed they came from. These phrases are the highest-stakes signal: they
are the exact language that appears in news writeups and case reports of doctrinally
similar disputes.

## Phase 0 — Preconditions (verified)

- `gh auth status`: ✓ logged in as `jackemorywilliams-bit` (scopes: repo, workflow, gist, read:org)
- `git`: 2.39.5 ✓
- **Python**: system was 3.9.6 (**below 3.11 requirement**) → installed Python **3.12.13** via Homebrew at `/opt/homebrew/bin/python3.12`. Resolved without user intervention.
- `pip`: available (21.x); will use venv pip from 3.12
- `pdftotext`: installed via Homebrew poppler 26.04.0 (preferred extractor)
- Seeds: **3/3 PDFs present**, none missing.

## Seed PDF inventory

| File | Pages | Words |
|------|-------|-------|
| Philip_Morris_v_Australia_Award_2015-12-17.pdf | 198 | 67,707 |
| Eli_Lilly_v_Canada_Final_Award_2017-03-16.pdf | 159 | 55,267 |
| Bridgestone_v_Panama_Award_2020-08-14.pdf | 278 | 87,582 |

No gaps.

## Thematic fingerprint — extracted verbatim vocabulary by ring

Legend: **[PM]** Philip Morris v Australia · **[EL]** Eli Lilly v Canada · **[BR]** Bridgestone v Panama. Parenthetical = approx. occurrence count in that award.

### Ring 1 — IP-as-investment
- "covered investment" [PM][BR(19)]
- "intellectual property" [BR(11)]
- "trademark" / "exploitation of the trademark" / "use of a trademark" [BR(307)]
- "licenses that constitute its investment" [BR]
- licensor/licensee split structure — BSLS (licensor) vs BSAM (licensee) standing [BR]
- "patent" invalidation; "utility requirement" in patent law [EL(633 / 414)]
- "promise utility doctrine" / "promise doctrine" [EL(81 / 10)]
- brand value, GIs, data exclusivity, copyright (theme extension; not all literal in seeds)

### Ring 2 — Regulatory or judicial measure as the disputed conduct (EXTRA WEIGHT: 2/3 seeds are judicial-measure cases)
- "denial of justice" [EL(59)][BR(132)]
- "judicial measure" [EL(15)]; "domestic court(s)" [EL(10)]; "Supreme Court" judgment [BR(360)]
- "Plain Packaging Measures" / public-interest legislation [PM]
- "dramatic change in the utility requirement" / "dramatic change" [EL(32)]
- "minimum standard of treatment" (MST) [EL(19)][BR(5)]
- "arbitrary or discriminatory" / "manifest arbitrariness" [EL]
- High-bar review-of-judicial-conduct language:
  - "egregious and shocking—a gross denial of justice, manifest arbitrariness, blatant unfairness, a complete lack of due process" [EL]
  - "judicial propriety" / "judicial conduct" [EL]
  - "manifestly unjust judgment ... shocks a sense of [judicial propriety]" [BR]
  - "egregiously wrong that no honest or competent court could [have reached it]" [BR]
  - "systemic failure in the administration of justice" [BR]
- Treaty articles seen: NAFTA 1105/1110 [EL]; US–Panama TPA Art. 10.5 (MST/DoJ) [BR]

### Ring 3 — Jurisdictional / admissibility doctrines
- "abuse of right" [PM(71)] / "abuse of process" [PM(15)]
- "reasonably foreseeable" dispute; "pre-existing or reasonably foreseeable dispute" [PM]
- "critical date" [PM(9)]
- "corporate restructuring" / "restructure its investment to gain Treaty protection" [PM(31/197)]
- "treaty shopping" [PM] / "treaty protection" [PM(15)]
- "shell subsidiary" — "channelling funds through a shell subsidiary for purposes of manufacturing a TPA claim" [BR]
- "abusive tactics" [BR]
- definition of "investor"; standing of licensor vs licensee [BR]
- standing to claim denial of justice when "not a party" to the proceedings [BR(4)]
- "exhaustion of local remedies" [BR]
- "denial of benefits"; "substantial business activities" (theme extension; not literal in seeds but same doctrinal family)

## Scoring model (carried into fingerprint.yaml)
- HIGH (70+): intersection of any two rings.
- MEDIUM (40–69): one ring strong + weaker tie to another; OR any judicial-measure case alone (a new case challenging a domestic court judgment scores ≥ MEDIUM even with no other ring — Ring 2 carries extra weight because 2/3 seeds are judicial-measure cases).
- LOW (<40): one ring weakly, or none. Vanilla expropriation / mining / oil & gas / sovereign debt / intra-EU energy → LOW unless a judicial-measure or IP angle is present.
- Starting threshold: 60 (retune in dry-run if 0 or 50+ matches).

## Source list with scrapability confidence
| Source | Type | Priority | Scrapability | Notes |
|--------|------|----------|--------------|-------|
| iisd_itn | RSS | highest | HIGH | structured feed, polite |
| google_news_rss | RSS | secondary | HIGH | fingerprint-derived queries |
| italaw | HTML | primary | MEDIUM | homepage + /browse; needs fallback selectors |
| icsid | HTML | primary | MEDIUM | cases/case-database; may be JS-heavy, verify |
| unctad_isds | HTML | primary | MEDIUM | investment-dispute-settlement listing |
| iareporter_headlines | HTML | primary | LOW-MED | headlines only; paywall — never bypass |
| pca_press | HTML | low | LOW | only if scout finds stable structure |

## Sub-agent DAG (Phase 2)
```
A: source-scout        ─┐
B: fingerprint-architect─┐
C: prompt-engineer      │
                        │
A ──► D: scraper-builder ──┐
B,C ► E: classifier-builder┤
                           ▼
                      F: pipeline-builder ─► G: ci-builder ─► H: docs-and-tests
```
- A → specs/<source>.yaml (primary + fallback selectors per HTML source)
- B → fingerprint.yaml (weights summing to 100/ring, threshold 60, 5+ few-shot incl. negatives)
- C → prompts/classifier.txt (3+ few-shot)
- D → src/sources/*.py (primary + fallback parse, logs when fallback fires)
- E → src/classify.py (Gemini + Anthropic via MODEL_PROVIDER; 1 retry then score 0 + "classification_failed")
- F → src/main.py, state.py (first-run bootstrap), render.py, templates/digest.html.j2, email_send.py, config.py
- G → .github/workflows/weekly.yml (cron 0 13 * * 1 + manual, concurrency, contents:write, fail-fast on missing secrets, commit state+digests)
- H → README.md, HANDOFF.md, tests/, requirements.txt, .gitignore, .env.example

## Phase 3 dry-run outcomes (verified)
- **robots.txt fix**: `urllib.robotparser` mis-treated Cloudflare-blocked robots fetches as "disallow-all". Switched to fetching robots.txt with our identifying UA via `requests` and failing open on errors/404. After the fix iisd/icsid/italaw/iareporter all return 200.
- **Sources returning data** (clean run, 400-day window): iisd_itn=10, italaw=3, icsid=20, iareporter=10, unctad_isds=25, pca_press=10. `google_news_rss=0` — **robots-disallowed** for `*` (honored, not evaded; auto-re-enables if Google changes policy).
- **Scorer calibration**: keyword fallback now 7/7 on the fingerprint few-shot bands (PRESENT_FLOOR=12, STRONG=18). Seed awards score MEDIUM–HIGH on their own text (Eli Lilly 75/HIGH). Off-theme live items correctly score 0 — so a 0-match week is correct behavior, not a threshold bug. Threshold stays 60; will re-confirm against the live LLM in Phase 5.
- **Tests**: 15/15 pass.

## Runtime cost posture
Zero-cost: public GitHub repo (unlimited Actions) + Gemini Flash free tier (default) or Claude Haiku (~$1/mo). Both code paths exist; `MODEL_PROVIDER` selects at runtime.
