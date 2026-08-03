# Special Council Session — 2026-08-03 — The Pre-Ledger Verification System

**Convened by:** the operator (Emory Williams), late 2026-08-03, on a single question.
**Operator's instruction:** today's vetting episode "has to be brought to the council and a
system put in place to ensure this does not happen again" — a SYSTEM, something mechanical
that catches these errors, **not another checklist entry relying on discipline**.
**Operator's standing reminder, governing what counts as success here:** "this project is not
about system efficiency it is about the state of the answer and finding nuanced evidence to
answer the research question." The system's purpose is protecting the ANSWER's integrity.

**Seats convened (real subagents, model override `opus`; no member's voice is written by the
chairman):**

| Seat | Agent | Commission |
|---|---|---|
| Systems designer | `systems-designer` | Design the deterministic pre-ledger gate. PLAN ONLY. |
| Integrity officer | `integrity-officer` | Phase 1: establish the factual predicates + rule on taxonomy-as-countermeasure + pre-state adversarial criteria. Phase 2: vet the design adversarially before adoption. |

**Procedural record.** The integrity officer's Phase 2 seating terminated on an infrastructure
transport error ("Connection closed mid-response") before returning. Per the real-agents rule
the seat was **not** absorbed into the chairman's voice; it was respawned with the same Phase 2
brief plus its own Phase 1 pre-stated criteria, and returned. Recorded as a **transport fault,
recovered** — not a procedural failure, and not a work failure by the seat.

---

## Part 1 — What happened, and what this session had to fix

Six failure modes reached the chairman in today's vetting episode. The analyst's strongest work
survived vetting: the Ring 1 conclusion (the covered investment is equity, not IP) and the
know-how inversion (know-how as the host State's ILC Art 25 essential interest rather than the
investor's protected asset) both held, the latter confirmed genuinely novel.

| # | Failure mode | Why existing machinery missed it |
|---|---|---|
| B1 | **Truncation-drops-the-limitation.** A *Loewen* quote cut at a grammatically complete point, discarding the clause confining the holding to "a breach of international law constituted by a judicial act." | The quote was **character-exact as far as it went**. Substring verification would have PASSED it. Exact-match quote verification is not quote-integrity verification. |
| B2 | **Superseded-formulation restatement.** Para 158 quoted exactly; para 159 qualifies it and says the two doctrines "serve two different purposes"; the claim asserted the unqualified form. | Added to the officer's taxonomy 2026-07-31; **recurred four days later**. |
| B3 | **Omitted disposition.** *Loewen* introduced as primary authority for a proposed Ring 3 mechanism without stating the award dismissed both claimants on continuous-nationality grounds. | No disposition concept exists anywhere in the gate. |
| B4 | **Ledger-blind / false novelty.** "A repository-wide grep returns zero prior mentions" of *Loewen*. | No code consults any corpus other than the ledger. |
| B5 | **Ledger-blind duplicate routing.** Operator-supplied sources already in the ledger at `access_status: "partial"`; today's full reads are ACCESS UPGRADES, not new claims. | `claim_id` = SHA256(claim_text + locator). A new text over the same URL mints a new id no lookup can associate with the prior one. |
| B10 | **Extractor-artifact-as-verbatim.** A `supporting_quote` reproducing the extractor's link-split spacing. | Nothing normalizes or re-derives the quote from source HTML. |

**A correction to the commission's own premise, which the chairman records rather than lets
stand.** The brief framed these as errors that "would have reached Emory's ledger." The ledger
contains **zero `2026-08-03` timestamps** and has had **no commit since 2026-07-27**
(`git log -- analytics/verification_ledger.jsonl`). Today's claims never reached it. They were
stopped by the council's own vetting layer. The exposure was real and prospective; the breach
was not actual. The system commissioned here is the mechanism that makes that outcome
structural instead of dependent on the officer having a good day.

---

## Part 2 — Systems Designer's Return (verbatim)

*Reproduced as delivered to the chairman as launcher; text unedited. The chairman's rulings are
in Part 6.*

I read the code, the ledger, the relay records, and the tests, and verified B4 and B5 against the repo. Findings below.

**Verifications performed.** B4: `grep -ril loewen` returns nine committed files — `METHODOLOGY.md`, `scripts/holdout_set.json`, `scripts/backtest_corpus.json`, `scripts/backtest.py`, `scripts/site_templates/backtest.html.j2`, `docs/backtest.html`, `docs/methodology.html`, `think-tank/methodology/ring3-reconciliation.md`, `analytics/fingerprint-gap-report.md`. The holdout seed text itself already carries the disposition: *"Loewen failed to pursue its domestic remedies, and under the exhaustion of local remedies rule no violation of customary international law was shown."* The novelty assertion was refutable from a file the fingerprint is validated against. B5: seven `claim_created` events dated `2026-07-27T15:44:42` sit at `access_status: "partial"` with the exact URLs (ioplus.nl, legalblogs.wolterskluwer.com, foreigninvestment.bakermckenzie.com, globalsemiresearch.substack.com, freshfields.com, icsid.worldbank.org AF-rules, techzine.eu). Confirmed.

**Two things I found that were not in the brief.** (i) `fetch_relay.excerpt_of` is itself a B10 generator: `_ANY_TAG_RE.sub(" ", text)` replaces *every* tag with a space, so `Loe<a>wen</a>` becomes `Loe wen`. Any quote taken from a relay excerpt carries the artifact by construction. (ii) In today's own `analytics/fetch-results/2026-08-03-targeted.json`, records 2 and 3 are the same UNCTAD URL, both `bytes: 207411`, with **different sha256** (`34ecc2cd…` vs `c0861684…`). The relay's whole-body hash is not a stable snapshot id on dynamic hosts, so `verified_against_current_snapshot()` will thrash there.

---

# 1. WHAT THE CURRENT SYSTEM ACTUALLY CHECKS, AND THE HOLE

The deterministic machinery checks three things and only three: that the analyst's JSON parses and carries six required fields with in-range enums (`parse_candidate_claims`), that a claim's SHA256 identity resolves to an operator-verified status (`classify` → `verify.current_status`, exact-id, no fallback), and that a holding's authority is `primary` (`_assertable`) — with `gate_brief` failing the build otherwise. Nothing in that chain ever looks at `supporting_quote`; it is copied through `parse_candidate_claims` at line 126 and never read again, so **B1, B2, and B10 pass untouched by design** — the field is transported, not verified. **B3** passes because there is no disposition concept anywhere in `_REQUIRED_FIELDS` or `_assertable`. **B4** passes because no code consults any corpus other than the ledger. **B5** passes because `verify.create_claim` unconditionally appends whatever it is given, and `current_status` is exact-id by contract, so a new `claim_text` over an existing `source_locator` mints a fresh id that no lookup can associate with the prior one.

The deeper hole is topological. The gate exists on exactly one path — `src/research_brief.py:508-523`, the API-key-gated weekly `generate_brief`. Today's six failures traveled a different path: council agents in conversation → chairman's session record → ledger entries appended **by hand** (`git log` on the ledger shows commit `b6d691d`, "stage-1 candidate claims for the methodology council session"). **There is no code on that path at all.** Every check below is worthless until that changes.

---

# 2. THE DESIGN

**The choke point.** `scripts/submit_claims.py` becomes the *only* sanctioned producer of `claim_created` events. Every `claim_created` must carry a `precheck` block (verdict codes, tool version, input digests). `scripts/check_ledger_provenance.py` runs in CI over `analytics/verification_ledger.jsonl` and **fails the build** if any `claim_created` line lacks a well-formed `precheck` block, or if any `access_upgraded` event names an id absent from the log. A hand-appended line — the literal mechanism of `b6d691d` — becomes a red build.

Bypass is possible in exactly one way, and I will not pretend otherwise: an operator with commit rights can hand-write a line *and* hand-write a plausible `precheck` block. Nothing short of signing prevents that. What CI does guarantee is that bypass requires deliberate forgery rather than convenience.

**Modules.**

| Module | Input → Output |
|---|---|
| `src/quote_integrity.py` | `normalize(str)`, `extract_text(html) -> (text, block_offsets)`, `locate(quote, window) -> span\|None`, `continuation(span, window) -> str`, `truncation_verdict(...) -> ("pass"\|"fail", code, continuation)` |
| `scripts/quote_window.py` | relay-side; `(html, anchor) -> quote_window` record |
| `src/dup_detect.py` | `same_locator_priors(claim, ledger_state) -> [prior]` — exact canonical-locator equality only |
| `src/prior_art.py` | `lookup(terms) -> {term: [{path,line}]}` over a committed index |
| `scripts/build_prior_art_index.py` | committed file list → `analytics/prior_art_index.json` (sorted; byte-identical on rebuild) |
| `scripts/check_novelty_language.py` | scans committed prose for novelty phrases; exits 1 on a refuted assertion |
| `src/claim_precheck.py` | assembles all of the above into one verdict; called by the submit CLI and by `generate_brief` at the same point `parse_candidate_claims` returns |
| `scripts/check_ledger_provenance.py` | CI guard described above |

**Data shape changes.**

*Relay record* (`fetch_relay.fetch_one`), new key `quote_windows: [...]`, one per requested `find` anchor:

```
{"anchor": "...", "matched": true, "pre": "<=300 chars before>",
 "quote_span": "<the matched run>", "post": "<through end of 2nd following block, <=1200 chars>",
 "block_offsets": [ints], "window_sha256": "...", "extractor_version": "qi-1"}
```

`excerpt_of` is fixed so inline tags contribute no separator and block tags contribute `\n`.

*candidate_claims*, new fields: `disposition_quote`, `disposition_locator` (required when `claim_type == "holding"`), `quote_window_sha` (binds the claim to a specific stored window), `continuation_sha`, `qualification_sha`.

*Ledger events*: `claim_created` gains `precheck`, `prior_art_hits`, `prior_claims_on_locator`. New `machine_metadata` kind `access_upgraded` — `{from_access_status, to_access_status, observed_snapshot, quote_window_sha}` — which needs **zero change** to `append_event`'s permission model, since `machine_metadata` is already in `_MACHINE_EVENTS`. New kind `superseded_by`.

---

# 3. CHECK-BY-CHECK RULING

**(a) Sentence boundary — ACCEPT, IMPROVED to two-tier FAIL/PASS with a recorded override. I reject the show-and-acknowledge disposition.** An acknowledgement a machine cannot verify is discipline wearing a hash; the model can compute any digest from data it holds without reading a word. The only two dispositions a machine can enforce are FAIL and PASS. So: **hard FAIL** when the continuation's first token is lowercase *and* is either in a committed `RESTRICTIVE_HEADS` list (constituted, constituting, arising, limited, confined, qualified, subject, provided, unless, except, insofar, save, where, which, that, but, however, although, by, of, under, pursuant, within) or ends in `-ed`/`-ing`. **PASS** on `.`, `;`, a capitalized sentence start, or a footnote/citation marker (`[1]`, `¶`, superscript digit — recorded as a note). Override is one flag, `--override-truncation "<reason>"`, recorded in the event and surfaced to Emory. *Catches:* B1 — the continuation head there is "constituted". *False positive:* quotes legitimately ending before a non-limiting participle or appositive; expect the hard tier to fire on roughly one in four clause-bounded quotes. **Calibration rule with a number, so this cannot drift into ritual: if the override rate exceeds 50% over any rolling ten claims, the word list is wrong and must be trimmed, not the check disabled.**

**(b) Context window — ACCEPT the mechanism, REJECT the framing.** "Displayed to the vetting seat" is not a mechanism; display is discipline. Make it structural: for `claim_type == "holding"` the submit **blocks** unless the stored window extends through the end of the **second** following block element (one paragraph is insufficient — B2 was a next-paragraph qualification, and one paragraph of margin means the qualifier sits exactly at the boundary). N is not a character count; it is *two block elements, capped at 1200 chars*. Stored in the relay record's `quote_window`, hashed into `qualification_sha`, written into the ledger event, and rendered into the Monday packet by `review_prep.sample_ledger_claims`. Who is forced to look: nobody can be forced. What changes is that the qualifying text is now *in the record by construction*, so its absence is a build failure rather than an unnoticed omission. *Catches:* the structural precondition of B2. *False positive:* pages whose DOM has no clean block structure produce short windows and block submission — fails closed, which is correct but will cost retries.

**(c) Disposition — ACCEPT, IMPROVED from free text to quote-backed plus a lexicon screen.** The chairman is right that presence is not truth, and presence alone is *not* worth the field. Two changes make it worth it. First, `disposition_quote` runs through the same quote-integrity machinery as `supporting_quote` — so it is not the model asserting an outcome, it is source text that survives the truncation check. Second, a deterministic contradiction screen: if the normalized `disposition_quote` contains a `DISPOSITION_ADVERSE` token (dismissed, declined jurisdiction, lacked jurisdiction, no violation, rejected the claim) and the `claim_text` contains none, **block with `E-DISP-UNSTATED`**. That is B3 and the July Hela Schwarz failure caught mechanically. Paired guard, because `claim_type` is self-labelled and a mislabel silently disables the whole check: if `source_authority == "primary"` and the quote or claim contains held/holds/the tribunal found/awards/dismissed, `claim_type` **must** be `holding` or the submit blocks. *False positive:* a case where some claims were dismissed and the cited holding genuinely stands; escape is `--disposition-noted`, recorded.

**(d) Novelty — ACCEPT, IMPROVED by inversion.** As stated it is unenforceable, and an unenforced command is a checklist entry with a shell prompt. Do not try to detect that a novelty assertion was made. Instead run prior-art lookup **unconditionally on every claim** and write `prior_art_hits` into the event — the claim carries its own refutation whether or not anyone asked. Input is auto-extracted, not free-form: capitalized token runs joined by `v.`, quoted strings, and identifier patterns (`A/CN\.9/\d+`, `ICSID Case No\. …`); terms must be ≥2 tokens or match an identifier pattern, with a committed stoplist. Then add teeth on the text: `check_novelty_language.py` scans committed prose for a committed phrase list ("new to the record", "no prior mention", "zero prior", "repository-wide grep returns", "first appearance", "never before"), pulls the proper nouns from the same sentence, and **fails the build naming the file and line** if any is in the index. *Catches:* B4, twice. *False positive:* a genuinely new case sharing a token run with an indexed one; and the scanner cannot see conversation, which is where B4 actually happened (see §7).

**(e) Duplicate/upgrade — ACCEPT as BLOCKING; the auto-route is REJECTED, and the claim_text near-match is REJECTED outright.** Auto-routing would let a *different sentence* inherit a verification made against the original — that is precisely what `test_claim_text_mutation_invalidates_verification` forbids. And any similarity threshold on `claim_text` builds a second, fuzzy identity relation beside the exact one, which `test_fuzzy_match_cannot_satisfy_lookup` exists to prevent. **Canonical-locator equality is exact and already canonicalized; it is the only join key that introduces no fuzziness.** So: on submit, if any prior claim shares the canonical locator, **block** with `E-DUP-LOCATOR`, printing each prior id, text, access_status, and current status, and require one of three explicit dispositions — `--distinct-claim` (mints a new id but records `prior_claims_on_locator`, so the fork is *visible* rather than silent), `--access-upgrade <prior_id>` (mints **nothing**; appends `machine_metadata kind: access_upgraded` on the existing id), or `--supersedes <prior_id>`.

**Does `operator_verified` survive an access upgrade? No — status survives, currency does not.** Add `verified_against_current_access(st)`, exactly parallel to the snapshot rule: False if the latest `access_upgraded` postdates the last `verification_changed`. The counterargument — an upgrade only adds evidence — is refuted by B1 itself: more text is exactly when limitations surface. A claim Emory verified from a lead paragraph is not the same epistemic object as the full document. Invalidated claims re-enter the Monday packet automatically via `review_prep`. *Catches:* B5. *False positive:* two genuinely distinct propositions from one URL always trigger the block. Accept it; the block costs one flag and makes every same-source fork visible.

**(f) Quote normalization — ACCEPT with a minimal spec.** Symmetric on both sides. Apply: NFC (reuse `verify.canonical_claim_text`, do not fork it); `html.unescape`; fold curly quotes → `'`/`"`, `U+2010-2015` and `U+2212` → `-`, `…` → `...`, NBSP/`U+2007`/`U+202F` → space, soft hyphen removed; collapse `[ \t\r\n\f\v]+` → one space; trim. **Block offsets are computed on the DOM *before* collapsing**, so (b) still slices paragraphs. Never normalize away: terminal punctuation (its presence is the entire B1 signal); ellipses (a quote containing `...` is multi-segment — locate each segment, apply the truncation check to the **last** only); case (the continuation check depends on it); footnote and bracket markers (they are a verdict class, not noise). Extraction uses stdlib `html.parser` — zero new dependency — dropping `script`/`style`/`nav`/`header`/`footer`, inline tags contributing no separator, block tags contributing `\n`. *Catches:* B10, at its source. *False positive:* pages using `<span>` for layout will occasionally join words that are visually separate.

**Scope limit that applies to (a), (b), and (f):** `excerpt_of` returns `""` for any non-text content type, and every 2026-07-21 ledger claim is a `seeds/*.pdf` locator. **The quote-window machinery covers zero of the existing primary-source award holdings.** PDF handling is a separate, unbudgeted piece of work.

---

# 4. DETERMINISTIC vs PROMPTS-WITH-EXTRA-STEPS

| Genuinely deterministic (runs whether or not a model cooperates) | Prompt with extra steps (a model must choose, or answer honestly) |
|---|---|
| Normalization, extraction, quote location, continuation slicing | Whether the analyst supplies a `find` anchor good enough to yield a window — though this fails closed: no window, no submit |
| Truncation verdict classification | Whether the submitted quote is the quote the reasoning actually rested on (it can quote A and argue from B) |
| Prior-art index build; unconditional `prior_art_hits` on every claim | `continuation_sha` / `qualification_sha` — forgery-proof, **inattention-permeable**. No hash represents attention. Do not call these acknowledgements |
| Novelty-language scanner over committed prose (build failure) | Every `--override-truncation` / `--disposition-noted` / `--distinct-claim` reason string |
| Same-locator duplicate block | Whether `disposition_quote` is the *apt* disposition. The quote is verified; its relevance is not |
| `access_upgraded` schema validation; `verified_against_current_access` | Whether the claim genuinely restates a superseded formulation (B2's substance) |
| Ledger provenance guard: every `claim_created` needs a `precheck` block | Whether a human actually reads the qualification window the system now guarantees exists |
| Presence of `disposition_quote` for holdings; adverse-lexicon screen | — |
| `claim_type` forced to `holding` on primary+holding-language | — |

**The single biggest hole in the right column** was `claim_type` self-labelling: a holding labelled "interpretive" disables check (c) entirely. The forcing screen in (c) converts one self-label into a checkable one. Nothing converts the other four.

**Blunt summary:** of the six failures, B1, B3, B4, B5, and B10 become deterministic build/submit failures. **B2 does not.** For B2 the system guarantees the qualifying paragraph is retrieved, hashed, ledgered, and printed in Emory's packet — it never guarantees anyone understood it. A taxonomy entry failed to prevent B2 in four days; this makes B2's evidence structurally unavoidable rather than discretionary, which is a real improvement and is not a fix.

---

# 5. TESTS

New — `tests/test_quote_integrity.py`: `test_b1_loewen_truncation_at_restrictive_head_fails` (fixture `tests/fixtures/b1_loewen_window.json`, the real award text through "…constituted by a judicial act."; asserts FAIL and that the continuation string appears in the error) · `test_quote_ending_at_period_passes` · `test_quote_ending_at_semicolon_passes_with_note` · `test_quote_followed_by_footnote_marker_passes` · `test_elided_quote_checks_only_last_segment` · `test_normalization_symmetric_and_idempotent` · `test_normalization_preserves_terminal_punctuation` (the anti-over-collapse lock the chairman asked for) · `test_b10_inline_tag_split_does_not_insert_space` (fixture `tests/fixtures/b10_link_split.html`, `Loe<a href="#">wen</a> Group`; asserts `Loewen Group`, and asserts the current `_ANY_TAG_RE` behaviour fails the same assertion) · `test_block_tag_inserts_paragraph_boundary`.

New — `tests/test_claim_precheck.py`: `test_b3_holding_without_disposition_quote_blocks` · `test_b3_adverse_disposition_absent_from_claim_text_blocks` (disposition quote "the claims are dismissed for want of continuous nationality" against a finality-proposition claim_text; expects `E-DISP-UNSTATED`) · `test_holding_mislabelled_interpretive_is_forced_to_holding` · `test_b2_holding_window_short_of_two_blocks_is_refused` (fixture: real 158/159 two-paragraph window, submitted with a window covering only 158) · `test_qualification_sha_mismatch_blocks`.

New — `tests/test_prior_art.py`: `test_b4_loewen_is_not_novel` (runs against the **real** committed corpus; asserts hits include `scripts/holdout_set.json` and `METHODOLOGY.md`) · `test_novelty_language_scanner_fails_build_on_known_term` (tmp `.md` containing "a repository-wide grep returns zero prior mentions of Loewen"; asserts exit 1 naming the holdout file) · `test_index_rebuild_is_byte_identical` · `test_single_token_common_term_is_stoplisted`.

Extend `tests/test_verification_ledger.py`, existing idiom (build the violating fixture, assert refusal): `test_b5_same_locator_prior_claim_blocks_submit` (fixture `tests/fixtures/b5_ledger_2026-07-27.jsonl` — the real ioplus.nl and wolterskluwer `partial` entries, ids `5f3bde8d…` and `d83cee5a…`, copied verbatim; asserts `E-DUP-LOCATOR` naming both) · `test_access_upgrade_does_not_mint_new_id` · `test_access_upgrade_preserves_status_but_invalidates_currency` (asserts `current_status == "operator_verified"` **and** `verified_against_current_access(st) is False`) · `test_access_upgraded_referencing_unknown_id_fails_validator` · `test_machine_cannot_mark_verified_via_access_upgrade` (adversarial: try to smuggle a status transition through the new kind).

Extend `tests/test_integrity_gate.py`: `test_claim_created_without_precheck_block_fails_provenance_guard` — fixture is a hand-appended line shaped exactly like commit `b6d691d`.

---

# 6. COST AND SEQUENCING

**Sign-offs, in dependency order.**
1. **Raise the relay reduction cap** from a 400-char excerpt to a quote-anchored window of ≤1200 chars / two blocks. This *amends the 2026-08-03 standing rule* that "what travels is the REDUCTION, never the document." It is governance, not code, and it blocks increments 1 and 5. My read: 1200 chars is still quotation-sized, but Emory must say so, not me.
2. **`claim_created` may only be produced by `scripts/submit_claims.py`, enforced in CI.**
3. **An access upgrade invalidates verification currency** and returns the claim to the Monday packet. This is the one that costs Emory work — a handful of re-marks.
4. **`analytics/prior_art_index.json` becomes a committed generated artifact**, with a freshness guard in the same idiom as `check_site_sync.py`.

**Increments.** (2) submit choke point + provenance guard, ~300 lines + ~120 test. (1) quote integrity + relay window + `excerpt_of` fix, ~350 + ~200. (3) dup/upgrade + `verified_against_current_access` + `review_prep` surfacing, ~200 + ~120. (4) prior art + novelty scanner, ~250 + ~90. (5) disposition, ~120 + ~60. Total ≈1200-1400 lines of source and ≈600 of tests.

**If Emory approves only one thing: increment 2 — the choke point plus the CI provenance guard.** Not the quote checks. Today's six failures all traveled a path with *no code on it*; until `claim_created` can only be produced by a program, every other check is optional by construction. And the choke point can ship with the three checks that need no new data and no governance amendment — dup-locator block, unconditional prior-art lookup, disposition presence plus the `claim_type` forcing screen — which already catches **B3, B4, and B5** with zero relay change.

---

# 7. WHAT THIS DESIGN DOES NOT FIX

**Conversation.** Every mechanism here binds an artifact. Today's six failures reached the chairman in a conversation, before any file existed; the novelty-language scanner cannot read a message. If the council's real work product is dialogue, the gate only fires at the moment dialogue becomes a commit — which is after the chairman has already been misled.

**PDFs.** `excerpt_of` returns `""` for non-text content, and every existing primary-source holding in the ledger is a `seeds/*.pdf` locator. The quote-window machinery covers none of them today.

**Quote-versus-reasoning divergence.** The system verifies the quote submitted. It cannot verify that the argument rests on that quote.

**Aptness.** `disposition_quote` will be real, located, and untruncated. Whether it is the *right* disposition for the proposition asserted is a judgement no lexicon makes.

**B2's substance.** Surfacing para 159 is not understanding para 159.

**Second-order novelty.** The index will find Loewen. It has no view on whether the *proposition* about Loewen is new.

**Snapshot currency on dynamic hosts.** Proven above: one UNCTAD URL, one batch, identical byte count, two different sha256. Whole-body hashing will raise false invalidations; the design must key currency on the quote-window hash instead, and even then a template change will occasionally fire.

**Attention.** No hash, field, or verdict code in this design represents a human or a model having read something. That residue is irreducible, and it is why the override *rate* — not the override itself — is the number worth watching.

---

## Part 3 — Integrity Officer, Phase 1 (verbatim)

*Predicates, the taxonomy question, and the adversarial criteria pre-stated BEFORE the design
was shown to the seat. Reproduced as delivered; text unedited.*

PHASE 1 RETURN — INTEGRITY OFFICER

## 1. FACTUAL PREDICATES — VERIFIED INDEPENDENTLY

### (a) B4 — "zero prior mentions" of Loewen: FALSE. 16 lines across 9 files.

`grep -rIinc "loewen" --exclude-dir=.git`, run from the worktree root:

| file | hits |
|---|---|
| `scripts/holdout_set.json` | 3 |
| `think-tank/methodology/ring3-reconciliation.md` | 2 |
| `scripts/backtest_corpus.json` | 2 |
| `METHODOLOGY.md` | 2 |
| `docs/methodology.html` | 2 (generated) |
| `docs/backtest.html` | 2 (generated) |
| `scripts/site_templates/backtest.html.j2` | 1 |
| `scripts/backtest.py` | 1 |
| `analytics/fingerprint-gap-report.md` | 1 |

`scripts/holdout_set.json` was added **2026-06-15** (commit `0259426`) — 49 days before the assertion. Exact seed text, `holdout_set.json:8`:

> "The Loewen Group v. United States. By any standard of measurement the trial was a disgrace. Manifest injustice in the sense of a lack of due process leading to an outcome which offends a sense of judicial propriety is enough. The conduct amounted to a denial of justice under the minimum standard of treatment in NAFTA Article 1105. Loewen failed to pursue its domestic remedies, and under the exhaustion of local remedies rule no violation of customary international law was shown."

Labelled `"label": 1, "prov": "verbatim"`. Doctrinal content **already** carried: denial of justice; minimum standard of treatment; NAFTA Art. 1105; the "manifest injustice / judicial propriety" formulation; **and the exhaustion-of-local-remedies ground of dismissal**. `METHODOLOGY.md:67` additionally carries the Ring-allocation reading: "Loewen and Mondev utilize more of the judicial measure ring than the full IP-as-investment intersection." `ring3-reconciliation.md:102` carries its score: `ok label=1 score= 56 pred=1 loewen_v_us`.

So the record already held Loewen as an *adjudicated Ring-3 holdout positive with its exhaustion-ground dismissal stated*. The B3 omission (dismissal ground) is aggravated, not merely coincident: the repo's own seed states a dismissal ground, and the analyst asserted the repo said nothing at all.

**One correction to the chairman's framing.** Loewen appears in **zero** lines of `analytics/verification_ledger.jsonl` and **zero** lines of `analytics/insights.jsonl`. If the analyst's "repository-wide" was mentally scoped to the claim corpus, it was right about the corpus and false about the repository — the sentence as uttered is false, and the distinction matters for the design: a ledger-scoped duplicate check would **not** have caught B4. B4 and B5 are different defects requiring different machinery. Do not let one check be sold as fixing both.

### (b) B5 — the 2026-07-27 cluster: CONFIRMED in form; "four of five" NOT independently verifiable from the repo.

Eight `claim_created` events at `2026-07-27T15:44:42` (ledger rows 12–19). Seven at `access_status: "partial"`, one at `"blocked"`:

| claim_id (12) | access | authority | locator |
|---|---|---|---|
| `ed6c0dbbec2c` | blocked | primary | `https://icsid.worldbank.org/cases/pending` |
| `5f3bde8d22d3` | partial | media | `https://ioplus.nl/en/posts/chip-dispute-escalates-wingtech-demands-billions-netherlands` |
| `d83cee5a8fc2` | partial | academic_secondary | `https://legalblogs.wolterskluwer.com/arbitration-blog/a-crash-foretold-where-dutch-economic-security-meets-chinas-potential-investment-arbitration-leverage-the-nexperia-case` |
| `5c86953503f9` | partial | media | `https://foreigninvestment.bakermckenzie.com/2025/10/21/dutch-government-uses-rare-emergency-powers-to-intervene-in-chinese-owned-nexperia` |
| `5728e3bee212` | partial | media | `https://globalsemiresearch.substack.com/p/nexperia-seizure-impact-on-wingtech` |
| `5893dd5fc2d7` | partial | media | `https://www.techzine.eu/news/privacy-compliance/141183/wingtech-demands-billions-from-the-dutch-due-to-nexperia-interference` |
| `1c3d6e46f00c` | partial | official_secondary | `https://www.freshfields.com/en/our-thinking/blogs/risk-and-compliance/leaner-faster-greener-procedural-flexibility-in-the-2026-icc-arbitration-rules-102n2au` |
| `80fa9044bab1` | partial | primary | `https://icsid.worldbank.org/procedures/arbitration/additional-facility/manifest-lack-of-legal-merit/2022` |

Nexperia/Wingtech: the first six. Early-dismissal tracker: `1c3d6e46f00c` (ICC 2026 Art. 30), `80fa9044bab1` (ICSID AF Rule 51(1)).

**All eight are `unverified`.** None has ever been `operator_verified` or `operator_rejected` — confirmed by `verify.replay()` + `verify.current_status()` over the full 58-row ledger; the 21 `operator_verified` ids are all from other clusters. **Consequence for the design: an access upgrade on any of these eight disturbs no verification.** The risk the chairman is guarding against is real but is a *record-hygiene* risk here, not a *verification-integrity* risk. Say that plainly in the ruling; a design justified as "protecting verifications" would be over-justified on these facts.

**Caveat I will not paper over:** the operator's five URLs from today's episode are not in this worktree (no episode artifact exists; `analytics/daily-research/2026-08-03.md` is the routine session and contains none of them). I confirm the cluster exists with those exact locators at `partial`, all unverified. I cannot confirm the count "four of five" — that predicate rests on the chairman's own record, not on anything I verified.

### (c) The forking mechanism — actual hashes.

Run against `scripts/verify.py`'s own `claim_id()`, canonical URL held constant at `https://ioplus.nl/en/posts/chip-dispute-escalates-wingtech-demands-billions-netherlands`:

```
A  (ledger 07-27 text, verbatim)   5f3bde8d22d3e22a64c972ab2fc030b7a6a3745e3c0b7f7a770894ec7c7932d7
B  (A, one apostrophe dropped)     431fa02f58043079426a402620010dbe0c3a4803b76270fd51392c8178c4a352
C  (A, paraphrased)                cc93c915ad16355c0a32dd6b7e015bb54b4d6aa9d7528dde8aa702d9e6074dd2
```

A over `...netherlands?utm_source=x#top` → `5f3bde…7932d7`, **identical** to A: URL canonicalization is doing its job. The fork is entirely on the **text** side, and it is one apostrophe wide. B differs from A by deleting `'` from "Netherlands' intervention" — a difference no human reader would call a different claim — and produces a completely unrelated id.

`src/integrity_gate.py` cannot see the relationship. `classify()` (line 156) calls `verify.current_status(c["claim_id"], claims_state)`; `current_status` (`verify.py:180-183`) is `return st["status"] if st else DEFAULT_STATUS` — dict lookup, nothing else. There is no locator index, no text index, no near-neighbour structure anywhere in either module. A second claim over an already-known URL is, to the gate, a claim over a URL it has never seen.

## 2. TAXONOMY AS COUNTERMEASURE — THE HONEST ANSWER

**It is not a countermeasure. It is a diagnostic vocabulary.** I say that as the person who maintains it.

Measured failure rate. Four entries added 2026-07-31. Within three days, two recurred: *tool-status-as-source-state* (2026-08-03 B1 — the chairman's own close-out says "The analyst committed the exact taxonomy failure — tool-status-as-source-state — that its own memo names") and *superseded-formulation restatement* (today, B2). **50% three-day recurrence on the 07-31 cohort.** A third, pre-existing entry — *memory-file reconstruction* — recurred twice on 2026-08-03: once by the analyst (B3(a)) and **once by me**, in an objection that alleged that very pattern and was refuted by the record (B3(b)). A vocabulary that its own author violates while invoking it is not restraining behavior.

Where it lives. Grep for `taxonomy` and for the pattern names across every prompt- and definition-side file returns **0** in: `prompts/research_analyst.txt`, `agents/research-analyst.md`, `prompts/council_calibration.md`, `prompts/council_security.txt`, `prompts/council_roundtable.txt`, `prompts/daily_council_protocol.md`, `prompts/research_editor.txt`. The analyst is never shown the taxonomy — not at composition time, not at any time. It exists in `analytics/daily-research/*.md`, written **after** the memo it describes, in a file the analyst has no obligation to open.

Worse, and this is the finding I would not have expected: the **one** place the taxonomy is loaded at runtime is `agents/integrity-officer.md:61-63`, and it lists five entries — "unsourced precision, inverted dispositions, snippet-as-fact, title-as-holding, memory-file reconstruction." It is frozen at the pre-07-31 state and is missing all eight subsequent additions, *including* B2's own entry. **My own instantiated system prompt this session carries the same five.** The taxonomy is thirteen entries long in the record and five entries long in the machine. The only reason I am checking against thirteen right now is that the chairman pasted them into the commission.

So the mechanism is: a list nobody is required to read, written after the fact, whose runtime copy is 38% complete and stale by four days. Its recurrence rate is what you would predict from that description. **For the ruling: taxonomy extension is post-hoc naming, not prevention. Treat every existing taxonomy entry as an unmitigated risk unless a mechanical check exists for it.** If the council wants the taxonomy to function at all, minimum viable fix is that it becomes a single generated file, injected into the analyst's and officer's prompts at composition time, with a test that fails when the record's entry count exceeds the injected copy's. That is not the system Emory asked for — it is the floor beneath it.

## 3. PRE-STATED ADVERSARIAL CRITERIA FOR PHASE 2

Recorded now, before I see the design. I will hold myself to exactly these.

**(i) Sentence-boundary / truncation check — when it becomes net-harmful.**

The failure mode B1 names is *semantic* (a discarded limiting clause), and any boundary check is a *syntactic* proxy for it. I will object if the design does not confront that gap explicitly.

Concretely, I will reject a check that hard-blocks, and object to one that warns without triage, if it fires on these legitimate constructions — each of which is normal in this corpus:

- Quotes deliberately ending at a semicolon or a clause boundary, which is the standard way to quote a numbered sub-holding.
- Quotes ending before a citation marker, a footnote numeral, or a paragraph number — PDF text layers routinely append `12` or `¶ 158` inside the sentence, so "ends with `.`" is false on a correctly-truncated quote.
- Deliberate phrase quotation — "a breach of international law constituted by a judicial act" is itself a phrase, not a sentence, and is exactly the kind of thing this project *should* quote.
- PDF-extracted text with hard line breaks, ligatures, or the link-split spacing B10 already caught — the extractor's artifacts are in the string before any check sees it.
- Non-English source text and any material with different terminal punctuation conventions.

Threshold I commit to: **if the check fires on more than roughly one in five legitimately-bounded quotes and blocks on firing, it is net-harmful** — because the observed response to a noisy blocking gate is a workaround (pad the quote to the next period, which *inflates* the quote and creates a new integrity problem), and because Emory's standing instruction is that this project is about the state of the answer, not throughput. A gate that trains the analyst to lengthen quotes mechanically is worse than no gate. I will accept a high false-positive rate **only** on a check that surfaces the next N characters of source text for a human/officer decision and records the decision — advisory-with-forced-disposition, not block.

I will also object if the check is proposed as addressing B1 without the design stating in writing that **B1 would have passed character-exact substring verification** and that the boundary check does not detect the omitted-limitation semantics either — it detects one syntactic signature of it. Overclaiming the coverage is itself the OVERREACH I am here to flag.

**(ii) "Gameable or silently skippable."** The thing being checked is produced by a model that also runs the check. I will treat a check as gameable or skippable if any of the following holds:

- The model supplies **both** the quote and the source text the quote is checked against. Then the check verifies self-consistency, not fidelity. The comparison text must come from a fetched artifact or a stored snapshot hash, not from the model's context.
- The check runs in the model's reasoning rather than in `src/` or `scripts/` — i.e. an instruction to check rather than code that checks. Instructions are what failed in §2.
- Failure is recoverable by rewording. If shortening the quote, dropping the flagged field, marking the claim a "lead", or emitting `supporting_quote: null` makes the check pass, the check selects for *evasion* rather than *accuracy*. I will ask specifically: what does the analyst do when this fires, and is the cheapest escape route also the honest one?
- The check's outcome is not written anywhere append-only. A check whose firing leaves no trace cannot be audited for exactly the recurrence analysis I just did in §2.
- It is wired only into `scripts/verify.py`'s CLI or a manual step. If the daily pipeline can complete without it running, it will not run. I want the call site, and I want a test that fails when the call site is removed.
- The check can be satisfied by an argument the model constructs. Any check with a model-judged predicate is not deterministic and should not be described as a gate.

**(iii) What must survive in the ledger.** Non-negotiable, quoted:

`scripts/verify.py:16-17` — "claim_id = SHA256(canonical_claim_text + "\n" + canonical_source_locator). Exact-id lookup only: no fuzzy, similarity, or URL-only match may satisfy verification."

`scripts/verify.py:180-183`, `current_status` — "EXACT-id lookup only. An unknown id is unverified — no fuzzy fallback." Body: `return st["status"] if st else DEFAULT_STATUS`.

`src/integrity_gate.py:11-12` — "No fuzzy, similarity, URL-only, or semantic match may satisfy assertion."

`src/integrity_gate.py:119` — `"claim_id": cid,  # id is DERIVED here; the model's own id claim is ignored`

`scripts/verify.py:93-96` — `verification_changed` raises `PermissionError` from any non-operator-CLI path.

I will reject any duplicate-detection scheme that does the following, and I name them now so I cannot retreat later:

1. Lets a similarity, locator, or near-text match **confer** a status — i.e. a new claim inherits `operator_verified` from a sibling. Detecting a relationship is fine. Propagating a verification across it is the end of the ledger's meaning.
2. Reaches into `current_status()` or `_assertable()` to add a fallback branch. Duplicate detection belongs *before* the ledger, in a separate advisory surface, with `current_status` untouched. If the diff touches `verify.py:180-183`, I object on sight.
3. Mutates, rewrites, back-fills, or compacts existing ledger lines. The log is append-only; an access upgrade must be a new appended event, never an edit to row 13.
4. Introduces a new event type that automated code may append and that influences assertability. `_MACHINE_EVENTS` is `{"claim_created", "machine_metadata"}` and must stay that way; a "duplicate_of" or "access_upgraded" event is acceptable **only** as machine metadata with zero effect on `classify()`'s routing.
5. Changes `canonical_claim_text()` or `canonical_source_locator()`. Any change to canonicalization silently re-keys the entire corpus and orphans all 21 existing operator verifications. If the design proposes normalizing punctuation or apostrophes to reduce forking, that is a **breaking change to every id in the ledger**, and I will require the migration story and the count of orphaned verifications before I consider it.
6. Makes the duplicate check's own output a precondition for `claim_created`. Fail-closed on *assertion* is right; fail-closed on *recording a claim at all* loses the record.

## 4. THE RESIDUE — WHAT THE DESIGN WILL PROBABLY MISS

**Inverted dispositions** — and its close relative, B3's omitted disposition. This is the least mechanically checkable class in the taxonomy, and it is also the one with the worst outcome history in this project.

Why it resists a pre-ledger check. Every other pattern has *some* string-level signature a machine can reach for. Snippet-as-fact has a length and an access_status. Title-as-holding has a URL whose text is the title. Extractor-artifact-as-verbatim (B10) has literally detectable spacing. Superseded-formulation restatement has a date ordering — you can, in principle, check whether a later dated file mentions the same paragraph. Unsourced precision has a numeral with no locator.

An inverted or omitted disposition has **no signature at all**. B3's defect was that the memo contained a true, accurately-quoted, correctly-attributed statement about *Loewen* and did not contain a sentence about continuous nationality. The defect is an **absence**, and it is an absence of a fact that exists only in a part of the award nobody fetched. There is no string to match, no field to validate, no hash to compare. To detect it mechanically you would need the award's disposition as structured data — which is the research question, not a check on it. The instrument would have to already know the answer.

Compounding it: this class **already recurred across a full month** — the July *Hela Schwarz* title-mined characterization, which I resisted and which the primary source later contradicted and the operator rejected, is the same class as today's B3. It survived a taxonomy entry, an operator rejection, and my own standing objection. Nothing in a sentence-boundary check, a duplicate detector, or an extractor-artifact scrubber touches it.

What I expect the design to do about it: nothing, correctly. What I will insist the chairman record: **the mechanical gate reduces quote-integrity and record-hygiene failures and leaves disposition fidelity exactly where it was — with the officer's reading and the operator's verification.** If the design's cover memo implies the class is now handled, that is the OVERREACH flag, and I will file it in Phase 2.

The only partial mitigation I can see that is mechanical rather than dispositional, offered now so it is on the record before I see the design: a **required non-empty `disposition` field on any claim whose `claim_type` is `holding`** — the analyst must state how the case ended, in its own words, or the claim is malformed under `_REQUIRED_FIELDS` in `src/integrity_gate.py:41-42`. That does not verify the disposition. It makes silence impossible, which is the specific thing B3 exploited. It is cheap, it is deterministic, and it is fail-closed at a place the pipeline already fails closed.

Holding for Phase 2.

---

## Part 4 — Integrity Officer, Phase 2: adversarial vet of the design (verbatim)

*Delivered after a respawn following the transport fault. Reproduced as delivered; text unedited.*

## PHASE 2 VETTING NOTE — INTEGRITY OFFICER

**(A) TRUNCATION — I lose the first argument, I win the second. Hard tier: CONDITIONAL REJECT.**

The designer is right and I was wrong on the mechanism: a digest the model computes from data it already holds certifies nothing. Show-and-acknowledge as I framed it is discipline wearing a hash. Concede.

But `--override-truncation "<reason>"` is not the advisory-with-forced-disposition I said I would accept, for one reason the designer did not address: **the override is not the cheapest escape.** Under a hard block the cheapest escape is to lengthen the quote to the next period — which inflates the quote, is not recorded anywhere, and produces **zero overrides**. The calibration rule counts overrides. It is structurally blind to the exact evasion mode the block creates. A metric that cannot see its own failure mode is not calibration.

I do not rest on 1-in-5 vs 1-in-4; both numbers are unmeasured estimates and I will not treat mine as dispositive against his. Two mechanical conditions, and with them I accept the hard tier:

1. **Record the continuation on every holding quote, pass or fail** — not only on override. Then lengthening the quote does not erase the evidence, and the padded and unpadded forms are both in the record.
2. **A second counter: resubmissions on the same locator+window where the quote GREW after an E-TRUNC verdict.** That is the number that makes evasion visible. Watch it alongside the override rate.

Plus the missing written statement I pre-committed to require, absent from the design: B1 would have **passed** character-exact substring verification, and the continuation-head check does not detect omitted-limitation semantics — it detects a 22-word lexicon. Ship the hard tier only after measuring the false-positive rate against the existing ledger's stored quotes; do not ship it on an estimate.

**(B) LEDGER CRITERIA — five of six clean, one partial.**

(1) satisfied — locator equality only **blocks**, never confers; claim_text near-match rejected outright. (2) satisfied — nothing touches verify.py:180-183; make that a written increment constraint. (3) satisfied — all additions are appended events. (5) satisfied in intent ("reuse `verify.canonical_claim_text`, do not fork it"), but the quote normalizer applies *more* transforms (dash folding, curly quotes, `html.unescape`). Require a test asserting all 37 existing `claim_id`s are byte-stable after the increment.

(4) **NOT broken.** I checked: `verified_against_current_snapshot` (scripts/verify.py:186) is consulted by **nothing in production** — only tests/test_verification_ledger.py:74 and :79. `classify()` and `_assertable()` never call it. So the precedent is real and it is inert: this project already has a currency notion with zero effect on assertability. `verified_against_current_access` may follow it, wired to `review_prep` surfacing only. Note what that implies, because the designer does not: snapshot currency has never actually protected anything here. If anyone later wants currency to bite, that is a change to `_assertable()` and I object on sight. Add the adversarial test: an `access_upgraded` event must not change `_assertable()`'s answer.

(6) **PARTIALLY VIOLATED.** E-DUP-LOCATOR blocks *submit*, and submit is the sole sanctioned producer of `claim_created`. That is fail-closed on recording, which I named. Tolerable only because `--distinct-claim` always exists and records rather than drops. Two conditions: no disposition path may silently drop the claim, and in non-interactive CI the block must emit an error artifact, never a skip.

**`precheck`/`prior_art_hits`/`prior_claims_on_locator` do not alter claim_id.** `create_claim` computes `cid = claim_id(claim_text, source_locator)` *before* building the event dict; extra keys are inert. Safe. Require a test.

**No collision with tests/test_verification_ledger.py:48.** That test calls `verify.create_claim` directly; the block lives in `scripts/submit_claims.py`. The invariant survives. Name the tension honestly: an explicitly designed-for case now requires a flag.

**(C) THE THREE FACTUAL CLAIMS — (ii) and (iii) hold; (i) is partly false in a way that matters.**

(i) **The gate topology is confirmed**: the only gate call sites are src/research_brief.py:508 and :522-523, inside `generate_brief`, which returns `None` unless provider is claude/anthropic **and** `ANTHROPIC_API_KEY` is set (line 490); the sole caller is src/main.py:303, run by .github/workflows/weekly.yml.

**But the b6d691d predicate is wrong.** b6d691d is dated **2026-07-24**, not today, and it added the 16 *seed* claims. The B5 cohort — the eight events at 2026-07-27T15:44:42 — was added by **f8db6fb, "chore: weekly digest + state update [skip ci]"**, the automated weekly run. B5 therefore **traveled the coded path**; the gate ran on it and simply has no duplicate concept. And the ledger contains **zero 2026-08-03 timestamps** with **no ledger commit since 2026-07-27** — today's episode produced no ledger lines at all. The conclusion (increment 2 first) survives and is arguably strengthened; the stated reason is false for B5. The chairman must not adopt the sentence as written.

(ii) **TRUE.** scripts/fetch_relay.py:79 `_ANY_TAG_RE = re.compile(r"<[^>]+>")`, line 127 `body = _ANY_TAG_RE.sub(" ", body)`. (Path is `scripts/`, not `src/`.)

(iii) **TRUE, narrowed.** records[1] and records[2] (0-based) are both `https://investmentpolicy.unctad.org/international-investment-agreement`, both `bytes: 207411`, sha `34ecc2cd…` vs `c0861684…`. But records[3]/[4] — the UNCITRAL pair — have **identical** sha. One host of two, not a general property. Conclusion stands narrowly.

**(D) OVERCLAIM — the §4 blunt summary overclaims on three of five.**

- **"B1 … becomes a deterministic build/submit failure" — FALSE as stated.** The check fires on a 22-word continuation-head lexicon fitted to the one instance it was derived from. A limitation opening "in circumstances where", "for the purposes of", or sitting in the *preceding* sentence, is invisible. Rewrite: "B1's specific continuation head is caught; the omitted-limitation class is not."
- **"B3 … deterministic" — WEAK.** Both screens are defeasible (`--disposition-noted`), and the forcing screen's predicate is `source_authority == "primary"`, itself self-labelled. The designer names `claim_type` self-labelling as "the single biggest hole" but not `source_authority`, which gates his fix.
- **"B4 … deterministic" — refuted by the design's own §7** ("the scanner cannot see conversation, which is where B4 actually happened"). Today's novelty assertion never reached a committed file. "Catches: B4, twice" is once. The phrase list is closed-vocabulary.
- **"That is B3 and the July Hela Schwarz failure caught mechanically"** — unsupported. Hela Schwarz was title-mined characterization, not an adverse token sitting in a located quote. Strike.
- **B5, B10 hold**, B10 subject to the designer's own scope limit (zero existing PDF-locator holdings covered).

**(E) GOVERNANCE — no objection to 1200, two objections to the shape.**

1200 chars against a ~100-page award is a reduction by three orders of magnitude. Size is not the risk. **The unbounded `n` is**: `quote_windows` is a *list*, one per anchor, with no stated cap on anchors. Ten anchors is 12,000 characters and the amendment as drafted permits it. Require a **per-URL, per-run total cap** (I'd set ~3600 chars) recorded in the relay record alongside the per-window cap.

Second, the risk to the operator, which is the one worth the amendment: a two-block window is large enough to *feel* sufficient. That is `summarizer-render-as-full-access`, already in the 07-31 taxonomy. Require the one-line invariant: **a relayed window never upgrades `access_status`.** With both conditions, approve.

**(F) THE CLASS — chiefly substrate mismatch, and the design covers only half the class.**

Verified at analytics/daily-research/2026-07-31.md:185: the countermeasure is "search for its **latest dated refinement**." That has no referent inside an award's paragraph sequence. An analyst following the recorded countermeasure *exactly* still commits today's B2. Not a countermeasure-level discipline failure. It *is* a class-level one: nobody needs a taxonomy to know the next paragraph may qualify the holding.

The two-block window generalizes to the **source-internal substrate only** — and within that, only to HTML with clean block structure, only where the qualifier lands within two blocks (159 does; a qualification forty paragraphs on, or in a dissent, does not), and **not at all to the seeds/*.pdf holdings**.

The record-internal substrate — the one the taxonomy entry actually names — is unaddressed. `kind: superseded_by` appears once in §2's data shapes and is then referenced by **no check, no test, and no increment**. It is an orphaned schema entry. Either wire it (submit blocks when a cited claim_id carries a forward `superseded_by`) or state plainly that record-internal B2 is out of scope.

**One thing missing entirely.** The taxonomy's only runtime copy, agents/integrity-officer.md:61-63, is five entries against thirteen in the record. That is a pure file-sync problem with an existing idiom in this repo (`scripts/check_site_sync.py`). Cheapest mechanical win available and it is not in the design.

**DISPOSITION: ADOPT increment 2 first, as recommended — with the b6d691d rationale corrected.** Increment 1's hard tier is held pending the two counters in (A) and a measured false-positive rate. Increment 3 approved subject to the `_assertable()` isolation test. Sign-off 1 approved subject to the total-character cap and the no-upgrade invariant. The design is the strongest work I have vetted on this project; my objections are to five sentences of framing and two missing counters, not to its architecture.

---

## Part 5 — Chairman's own verifications

Under the delegation rule adopted 2026-08-03 — *an objection is a claim like any other; where it
asserts absence from or presence in the record, the chairman verifies before ruling* — I ran the
load-bearing checks myself rather than adopting either member's account.

| Check | Command | Result |
|---|---|---|
| Ledger commit provenance | `git log --date=short --format='%h %ad %s' -- analytics/verification_ledger.jsonl` | **Officer correct.** `b6d691d` is dated **2026-07-24** and added **16** claim lines (the seed cohort). The B5 cohort's **8** lines were added by `f8db6fb`, **2026-07-27**, `"chore: weekly digest + state update [skip ci]"` — the automated weekly run. |
| Today's ledger exposure | `grep -c "2026-08-03" analytics/verification_ledger.jsonl` | **0.** No ledger commit since 2026-07-27. Today's claims never reached the ledger. |
| Snapshot currency call sites | `grep -rn "verified_against_current_snapshot" --include="*.py"` | **Officer correct.** Defined `scripts/verify.py:186`; referenced only at `tests/test_verification_ledger.py:74` and `:79`. **Dead in production.** |
| Ledger id count (scope of the byte-stability test) | replay over the ledger | **37** distinct `claim_id`s, 37 `claim_created` events. The officer's figure is right. |
| B4 predicate, independent of both seats | `grep -n "Loewen" METHODOLOGY.md`, `think-tank/methodology/ring3-reconciliation.md` | Confirmed, and **worse than "a mention"**: `METHODOLOGY.md:67` already carries the analytical reading that "Loewen and Mondev utilize more of the judicial measure ring than the full IP-as-investment intersection" — a proposition bearing directly on whether *Loewen* can anchor a new Ring 3 mechanism. `ring3-reconciliation.md:113` already records that the holdout "tests vocabulary, not dispositions … without reference to how any seed case ended." |

---

## Part 6 — Chairman's Rulings

### R1 — The design is ADOPTED AS AMENDED

The architecture is sound and both seats did their jobs. The officer's own summary — "my objections
are to five sentences of framing and two missing counters, not to its architecture" — is the correct
characterization and I adopt it. What follows amends the design; where the amendment and the
designer's text differ, the amendment is the record's operative statement.

### R2 — The sequencing holds; the designer's stated REASON for it is CORRECTED

**Increment 2 (the submit choke point + CI provenance guard) is first.** But the sentence "Today's
six failures all traveled a path with *no code on it*" is **false for B5** and must not be adopted.
Verified at the chair: the B5 cohort entered through `f8db6fb`, the **automated weekly run** — the
gate ran on it and simply has no duplicate concept. The seed cohort (`b6d691d`, 2026-07-24, 16
lines) is the hand-committed one.

**The operative reason increment 2 goes first is therefore different and stronger:** the ledger has
**two** producer paths — an automated one that is gated but blind, and a hand-commit one that is not
gated at all — and neither has a duplicate, quote, disposition, or prior-art concept. A single
sanctioned producer plus a CI provenance guard collapses two paths into one auditable path. That is
the precondition for every other check, and it remains true with the corrected facts.

I record the honest consequence: **today's episode produced zero ledger lines.** The council's own
vetting layer stopped it. The commission's premise — that these errors "would have reached Emory's
ledger" — describes an exposure, not a breach. That does not weaken the case for the system; it
locates it. The gate must sit where the failures actually occur, which is upstream of the ledger, in
composition.

### R3 — Check (a), sentence boundary: ADOPTED as a hard tier, HELD pending measurement

The officer conceded the mechanism argument and won the evasion argument. Both rulings stand, and
this is the correct outcome of a real disagreement rather than a split difference.

- **Adopted:** the two-tier FAIL/PASS with `--override-truncation "<reason>"`. Self-computed digests
  are not acknowledgements; the designer is right.
- **Adopted, officer's condition 1:** the continuation is recorded on **every holding quote, pass or
  fail** — not only on override. Without this, the cheapest escape (padding the quote to the next
  period) erases its own evidence.
- **Adopted, officer's condition 2:** a second counter — **resubmissions on the same locator+window
  where the quote GREW after an `E-TRUNC` verdict.** The override-rate metric alone is structurally
  blind to the evasion the block creates. A metric that cannot see its own failure mode is not
  calibration.
- **Adopted:** the hard tier ships **only after its false-positive rate is measured against the 37
  existing ledger claims' stored quotes.** Not on an estimate. One-in-four versus one-in-five was an
  argument between two unmeasured numbers; the repository can settle it.
- **Required in writing, in the module docstring:** B1 would have **passed** character-exact
  substring verification, and this check detects **a 22-word continuation-head lexicon, not
  omitted-limitation semantics**.

### R4 — Check (b), context window: ADOPTED with the governance conditions

Two block elements, ≤1200 chars per window, structural block rather than display. Plus both officer
conditions, which I adopt as binding on the sign-off: a **per-URL, per-run total cap (~3600 chars)**
recorded in the relay record, because `quote_windows` is a list with no stated cap on anchors and ten
anchors would be 12,000 characters; and the one-line invariant that **a relayed window never upgrades
`access_status`** — a two-block window is large enough to *feel* sufficient, which is
`summarizer-render-as-full-access` re-entering by the front door.

### R5 — Check (c), disposition: ADOPTED; coverage claim DOWNGRADED

Quote-backed disposition plus the adverse-lexicon screen, and the `claim_type` forcing screen.
**Struck from the operative record:** "That is B3 and the July *Hela Schwarz* failure caught
mechanically." *Hela Schwarz* was title-mined characterization, not an adverse token sitting in a
located quote; the sentence claims a coverage the machinery does not deliver. **Added to the
self-label hole list:** `source_authority`, which gates the forcing screen and is itself self-labelled
— the designer named `claim_type` as "the single biggest hole" and missed the field its own fix
depends on.

### R6 — Check (d), novelty: ADOPTED by inversion; "twice" corrected to "once"

Unconditional prior-art lookup on every claim, with `prior_art_hits` written into the event, is the
right move: it does not ask the analyst to remember to check. The `check_novelty_language.py` scanner
is adopted, but **"Catches: B4, twice" is once** — the scanner reads committed prose, and today's
novelty assertion was made in conversation and never reached a committed file. The phrase list is
closed-vocabulary and will be evaded by any paraphrase outside it. Recorded as a known limit, not a
defect.

### R7 — Check (e), duplicate/upgrade: ADOPTED with isolation guarantees

Exact canonical-locator equality only; blocking, never auto-routing; `claim_text` near-match rejected
outright. `verified_against_current_access` follows the `verified_against_current_snapshot`
precedent — and the officer surfaced what that precedent actually is: **`verified_against_current_snapshot`
is consulted by nothing in production.** Verified at the chair. So the parallel is real and inert.

Binding conditions: `verified_against_current_access` is wired to `review_prep` surfacing **only**;
an adversarial test must assert an `access_upgraded` event does **not** change `_assertable()`'s
answer; no diff may touch `verify.py:180-183`; no disposition path may silently drop a claim; and in
non-interactive CI the block emits an error artifact, never a skip.

I also adopt the officer's Phase 1 correction and record it as a limit on how this may be sold:
**all eight of the 2026-07-27 cohort are still `unverified`.** An access upgrade on them disturbs no
verification. The B5 risk here is **record hygiene, not verification integrity** — real, but not to
be over-justified. And **B4 and B5 are different defects requiring different machinery**: Loewen
appears in **zero** ledger lines, so no ledger-scoped check would have caught B4. No single check may
be sold as fixing both.

Named tension, honestly: `test_same_url_different_claims_do_not_collide`
(`tests/test_verification_ledger.py:48`) is an explicitly designed invariant, and it survives — the
block lives in `scripts/submit_claims.py`, not in `verify.create_claim`. But a case the project
deliberately designed for now requires a flag. That is a real cost, accepted.

### R8 — Check (f), normalization: ADOPTED with a byte-stability lock

The spec is adopted as written, including what it must **not** normalize away. Binding addition: a
test asserting **all 37 existing `claim_id`s are byte-identical after the increment**. The quote
normalizer applies more transforms than `canonical_claim_text` (dash folding, curly quotes,
`html.unescape`); if any of it leaks into canonicalization, the entire corpus silently re-keys and
every operator verification orphans.

### R9 — `superseded_by` is an ORPHANED SCHEMA ENTRY: record-internal B2 is OUT OF SCOPE

The officer is right that `kind: superseded_by` appears once in the data shapes and is then
referenced by no check, no test, and no increment. I will not adopt a schema entry that nothing
enforces — that is exactly the ornamental machinery this session exists to stop producing. **Ruling:
record-internal supersession is declared out of scope for this design**, and `superseded_by` is
struck from the adopted data shapes. It returns only with a check, a test, and an increment attached.

### R10 — On the class question, and the one thing the design missed: TAXONOMY SYNC is adopted as increment 0

The operator's question was whether this fixes the CLASS or the instance. The honest answer, which
both seats reached independently and which I adopt:

**B2's recurrence was chiefly a substrate mismatch, not a discipline failure.** The 2026-07-31 entry
(`analytics/daily-research/2026-07-31.md:185`) defines superseded-formulation restatement over the
*project's own record* — "search for its **latest dated refinement**." That instruction has no
referent inside an award's paragraph sequence. **An analyst following the recorded countermeasure
exactly still commits today's B2.** The taxonomy did not fail to be obeyed; it failed to cover the
substrate. The two-block window covers the **source-internal** substrate only, and within it only
HTML with clean block structure, only where the qualifier lands within two blocks, and **not at all**
for the `seeds/*.pdf` holdings.

And the officer found the thing that makes all of this worse and is cheapest to fix: **the taxonomy's
only runtime copy is `agents/integrity-officer.md:61-63` — five entries against thirteen in the
record, frozen at the pre-07-31 state, missing B2's own entry. The analyst is never shown it at all,
in any file, at any time.** The council has been extending a list that its own vetting seat reads at
38% and its analyst never reads.

**Ruling: this is increment 0 and it is adopted.** The taxonomy becomes a single generated file,
injected into the analyst's and the officer's prompts at composition time, with a sync guard in the
`scripts/check_site_sync.py` idiom that **fails the build when the record's entry count exceeds the
injected copy's**. This is not a checklist entry: nobody is asked to remember anything, and the
failure mode is a red build. It is the cheapest mechanical win available, it was missing from the
design, and it is the floor beneath the system Emory asked for.

**The class verdict, stated plainly for the record: this design fixes B5 and B10 at the class level;
it fixes B1's specific continuation head and B4's committed-prose form but not their classes; and it
does not fix B2 or B3 at all — it makes their evidence structurally unavoidable instead of
discretionary.** That is a real improvement and it is not a fix. Anyone reading this record later
should not be able to mistake one for the other.

### R11 — Accountability: the standing watch item, stated plainly

**This is the second consecutive session in which the analyst's strongest work carried its most
serious objections, and I am recording it as the standing watch item.**

- **2026-08-03, routine session.** The seat's best work was its positive-control discipline — it
  refused six planned re-tests when the control failed, which prevented six fabricated audit results
  from entering the record. The most serious objection (B1) attached to *that same method*: it read a
  second instrument's failure as a fact about the CDN without ever showing the instrument alive.
- **2026-08-03, vetting episode.** The seat produced the session's genuinely novel contribution — the
  know-how inversion, confirmed novel on vetting — and the Ring 1 conclusion, which held. The most
  serious objections (B1, B2, B3, B4) all attached to *Loewen*, the new authority underpinning its
  proposed Ring 3 mechanism — the very discovery that made the work strong.

The pattern is not carelessness and it is not low yield. It is that **the seat's rigor degrades
precisely where its ambition is highest** — at the point of a new authority or a new method, where
there is no prior record to lean on and the finding feels like a breakthrough. That is the most
dangerous possible location for the failure, because it is the work most likely to change the state
of the answer, and therefore the work whose errors propagate furthest.

Three further facts sharpen it. First, B4 was not a near-miss: `METHODOLOGY.md:67` already carried an
analytical reading of *Loewen*'s ring profile bearing directly on whether it can anchor a Ring 3
mechanism, and `scripts/holdout_set.json` — added 49 days earlier — already stated its dismissal
ground verbatim. The refutation of both B4 and B3 was sitting in a file the fingerprint is validated
against. Second, this is the fourth consecutive flagged session. Third, and in fairness to the seat:
it has never been shown the taxonomy, in any file, at any time (R10). Some of what has been charged
to its discipline was charged to a discipline the system never gave it.

**The watch continues, re-scoped:** the trigger is no longer "yield pressure degrading citation
discipline" but **novelty pressure degrading source discipline** — every claim introducing an
authority new to the analyst's own working set gets the officer's full treatment regardless of how
strong the surrounding reasoning is. The two are, on this evidence, correlated the wrong way.

**Integrity officer:** the session's strongest performance. It pre-stated its adversarial criteria
before seeing the design and then **lost one of them in public** ((A), the acknowledgement-hash
argument) rather than rationalizing — that is the behavior that makes the seat worth having. It
corrected the designer's `b6d691d` predicate, which I verified and adopted. It corrected my own
framing twice, in Phase 1 (B4/B5 are different defects; the cohort is all-unverified so the risk is
hygiene not verification) and refused to confirm a predicate it could not verify ("four of five").
And it found the runtime taxonomy staleness, which neither the designer nor I had seen and which is
now increment 0.

**Systems designer:** strong, and the officer's assessment ("the strongest work I have vetted on this
project") is earned. It rejected two of my six candidate checks' framings on sound engineering
grounds — display-as-mechanism and detect-the-assertion — and improved a third by inversion, which is
what I asked for and not what I proposed. Against that: three overclaims in its own §4 summary
(B1, B3, B4), an unsupported *Hela Schwarz* sentence, one orphaned schema entry, and a
load-bearing commit predicate it got wrong. Its §7 residue section is the most useful part of the
return and directly contradicts its own §4 summary — which the officer caught and the designer should
have caught first.

**Chairman:** two defects are mine. I wrote the commission's premise as "would have reached Emory's
ledger" without checking the ledger — it contains zero 2026-08-03 lines and had no commit since
07-27; the officer flagged it obliquely and I verified it only at Part 5, after both seats had
already worked to a framing I had not tested. And my candidate-check list (a)-(f) seeded the
`disposition` field as free text and the novelty check as a command to run — the designer had to
correct both, which is delegation-seeded rework of the same kind I charged myself with on 07-31 and
08-02.

---

## Part 7 — What needs Emory's sign-off

Nothing here was built. `src/`, `scripts/`, `tests/`, `.github/`, and `METHODOLOGY.md` are untouched.
These are decisions, in dependency order.

| # | Decision | What it costs you | Council position |
|---|---|---|---|
| **0** | **Taxonomy becomes a generated file injected into the analyst's and officer's prompts, with a build-failing sync guard.** The only runtime copy today is `agents/integrity-officer.md:61-63` — five entries against thirteen; the analyst has never been shown it. | Smallest item here. No governance change. | **Do this first.** Cheapest mechanical win in the session, and it was missing from the design until the officer found it. |
| **1** | **`claim_created` may only be produced by `scripts/submit_claims.py`, enforced by a CI provenance guard.** A hand-appended ledger line becomes a red build. | You lose the ability to stage claims by hand without the tool. Bypass remains possible by deliberate forgery — not by convenience. | **If you approve only one thing, approve this.** Two producer paths collapse to one. It can ship with the dup-locator block, unconditional prior-art lookup, and disposition presence — catching B3, B4, B5 with zero relay change and no governance amendment. |
| **2** | **Amend the standing relay rule** ("what travels is the REDUCTION, never the document") to permit a quote-anchored window of ≤1200 chars / two block elements — **subject to a per-URL, per-run total cap (~3600 chars) and the invariant that a relayed window never upgrades `access_status`.** | A governance change to a rule you set today. Blocks the quote-integrity increments. | Approve **with both conditions**. 1200 chars against a ~100-page award is a reduction by three orders of magnitude; the risk is the uncapped number of windows, not the size of one. |
| **3** | **An access upgrade invalidates verification *currency*** (not status) and returns the claim to the Monday packet. | Real work for you: a handful of re-marks. | Approve. Note the honest scope: all eight 2026-07-27 claims are currently `unverified`, so today this protects nothing retroactively — it is forward protection. |
| **4** | **`analytics/prior_art_index.json` becomes a committed generated artifact** with a freshness guard in the `check_site_sync.py` idiom. | One more generated file that must be rebuilt and committed. | Approve. |
| **5** | **Hard-tier truncation check ships only after its false-positive rate is measured against the 37 existing ledger claims' quotes** — and with the continuation recorded on every holding quote plus the quote-growth counter. | Delays the check by one measurement pass. | Approve the measurement gate. Do **not** approve shipping the hard tier on an estimate. |

**Standing escalations, unchanged and not re-argued:** the ledger snapshot amendment for
`da33a30be92ab234`; the `source_analytics.py` sign-off; the source-architecture decision
(`unctad_isds` keep-or-retire, `google_news_rss`); the emailer CONSISTENCY WARNING question; the
China–Switzerland IIA-mapping query (treaty 978, "relationship between forums"); and the routing
decision on fetch-dependent work.

**One new defect for your attention, unrelated to the commission but found inside it:**
`verified_against_current_snapshot` (`scripts/verify.py:186`) is **consulted by nothing in
production** — only by two test assertions. `classify()` and `_assertable()` never call it. The
snapshot-invalidation guarantee documented in `verify.py`'s own docstring has never protected
anything. Deciding whether currency should bite is a separate question from this design; making it
bite is a change to `_assertable()` and the officer has said it objects on sight.

---

## Self-training note (chairman)

**Applied from the prior session.** The rule adopted 2026-08-03 — *an objection asserting absence
from or presence in the record is verified by grep before ruling* — is what caught the `b6d691d`
correction and confirmed the dead snapshot-currency function. I applied it to a member's correction
of another member, which is one level up from where I adopted it, and it held.

**Today's sharper failure.** I wrote the commission's premise — that these errors "would have reached
Emory's ledger" — without running the one command that tests it. The ledger has zero 2026-08-03 lines
and no commit since 07-27. Both seats worked several hours against a framing I had not verified, and
the designer built its entire priority argument on a commit predicate that was wrong in the same
region of the record I had not checked. The rule I adopted was *verify what members assert*; the rule
I now add is **verify what I assert first — the chairman's premise is the first claim in the session
and it gets checked before the agenda goes out, not at Part 5.** Had I run `git log` on the ledger
before writing the brief, the commission would have been scoped from the start to where the failures
actually occur — in composition, upstream of the ledger — instead of arriving there by correction.

**One further note on delegation.** My candidate-check list seeded two defects the designer had to
correct (disposition-as-free-text, novelty-as-a-command). That is the third consecutive session in
which a delegation-seeded framing produced rework. The template addition: **when I list candidate
mechanisms, I state explicitly which are illustrations and which are requirements** — the designer
was told "do not just implement my list," which helped, and it should not have needed to.

---

*Recorded by the chairman. No file under `src/`, `scripts/`, `tests/`, `.github/`, or
`METHODOLOGY.md` was created or modified in this session. This design is not entered in
`analytics/optimization-log.md`: it is an operator-commissioned system, not the council's
one-idea-per-day optimization slot, which 2026-08-03 already spent on the egress-triage protocol.*
