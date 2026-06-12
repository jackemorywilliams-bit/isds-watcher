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
- Starting threshold: 60 (retune in dry-run if 0 or 50+ matches). [Superseded: now 40 — see "Post-build deviations".]

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
- B → fingerprint.yaml (weights summing to 100/ring, threshold 60 [now 40], 5+ few-shot incl. negatives)
- C → prompts/classifier.txt (3+ few-shot)
- D → src/sources/*.py (primary + fallback parse, logs when fallback fires)
- E → src/classify.py (Gemini + Anthropic via MODEL_PROVIDER; 1 retry then score 0 + "classification_failed")
- F → src/main.py, state.py (first-run bootstrap), render.py, templates/digest.html.j2, email_send.py, config.py
- G → .github/workflows/weekly.yml (cron 0 13 * * 1 + manual, concurrency, contents:write, fail-fast on missing secrets, commit state+digests)
- H → README.md, HANDOFF.md, tests/, requirements.txt, .gitignore, .env.example

## Phase 3 dry-run outcomes (verified)
- **robots.txt fix**: `urllib.robotparser` mis-treated Cloudflare-blocked robots fetches as "disallow-all". Switched to fetching robots.txt with our identifying UA via `requests` and failing open on errors/404. After the fix iisd/icsid/italaw/iareporter all return 200.
- **Sources returning data** (clean run, 400-day window): iisd_itn=10, italaw=3, icsid=20, iareporter=10, unctad_isds=25, pca_press=10. `google_news_rss=0` — **robots-disallowed** for `*` (honored, not evaded; auto-re-enables if Google changes policy).
- **Scorer calibration**: keyword fallback now 7/7 on the fingerprint few-shot bands (PRESENT_FLOOR=12, STRONG=18). Seed awards score MEDIUM–HIGH on their own text (Eli Lilly 75/HIGH). Off-theme live items correctly score 0 — so a 0-match week is correct behavior, not a threshold bug. (At this point the threshold was still 60; it was subsequently lowered to 40 to broaden recall — see "Post-build deviations".)
- **Tests**: 15/15 pass.

## Runtime cost posture
Public GitHub repo gives unlimited Actions minutes. Both classifier code paths exist and `MODEL_PROVIDER` selects at runtime: Claude Haiku (~$1/mo) or Gemini Flash. See "Post-build deviations" below for the current live default.

## Post-build deviations (current state)
The original plan above is preserved as written; the following are the changes the build/operation actually settled on, and supersede any conflicting forward-looking statement above.

- **Threshold is 40**, not 60. It was lowered from the initial 60 to broaden recall (`threshold: 40` in `fingerprint.yaml`, read by `src/config.py`).
- **Claude is the live default classifier** (`MODEL_PROVIDER=claude`, model `claude-haiku-4-5-20251001`; ~$1/mo). Gemini (`gemini-2.0-flash`) remains a supported alternate but is not zero-cost in practice — the available Gemini key had no free-tier quota, which is why Claude runs live. The "Gemini Flash free tier (default)" posture above no longer holds.
- **One recipient**: `jackemorywilliams@icloud.com`. `ximena.s.benavides@gmail.com` is commented out in `src/config.py` and can be restored later.
- **Hybrid digest sizing**: report every match at/above threshold (no upper cap), with a minimum of six items filled from the closest near-misses only down to a relevance floor of 25 (`MIN_DIGEST_ITEMS=6`, `RELEVANCE_FLOOR=25`). A quiet week may send only 0–3 items; a week with nothing above 25 sends a one-sentence "no thematically relevant developments this week — N candidates screened" note instead of padding.
- **First-run baseline**: the first run indexes all existing items as a baseline and sends only a baseline note, so ongoing digests contain only genuinely new items.
