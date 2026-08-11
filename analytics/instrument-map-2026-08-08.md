# The instrument as it actually runs — audit map, 2026-08-08

Every claim below carries its evidence and a **path tag** — `[keyword-path]`, `[model-path]`,
or `[mixed]` — because the costliest error of the R1 council session was reasoning from one
path's arithmetic about the other path's output. A claim that cannot be path-tagged is not
asserted here. This file is the Workstream A artifact of the 2026-08-08 master-prompt repair;
methodological language written later must check against it.

## 1. Intake

Nine sources under `src/sources/`; per-source failures isolated and surfaced in
`meta.json["source_health"]`. Two structural facts dominate everything downstream:

- `src/sources/iareporter_headlines.py:62` sets `raw_text=title`, `summary=""`. For this
  source, the classifier's `{{TEXT}}` **is the headline string**. 10 of the 14 published
  entries came from it. `[model-path]`
- `iareporter_headlines` is in both `HEADLINE_ONLY_SOURCES` (`src/config.py:62`) and
  `NO_BODY_FETCH` (`src/enrich.py:19-20`): the body is never fetched, by policy, and no
  transition can violate that (state U2 of the R2.1 model).

## 2. Deduplication and seen-state

`state/seen.json` is `{sources: {source: {source_id: iso-timestamp}}}` (`src/state.py:60-70`),
176 entries. `src/main.py:139` drops any seen id **before classification, permanently,
with no record**. Bootstrap runs mark items seen without classifying (`src/main.py:191`).

**Defect (REPAIRED 2026-08-08, Phase 1 — retained as the record of the pre-repair state):** `classify_item` never raises (`src/classify.py:466`),
so the `except` at `src/main.py:247-249` — the only path that skips `mark_seen` — is
effectively dead code. A parse failure returns normally (score 0, tag
`classification_failed`, `src/classify.py:505-518`) and is marked seen; a provider
exception silently substitutes a keyword score (tag `classification_error_fallback`,
`src/classify.py:542-559`) for **every enriched item in the window** and marks them all
seen. One bad API window permanently converts a run, invisibly. `[mixed]`

## 3. Lexical scoring

`keyword_score` (`src/classify.py:155-255`): per-ring subtotals from `fingerprint.yaml`
phrase weights; `PRESENT_FLOOR = 12` (`:47`), `STRONG_SUBTOTAL = 18` (`:50`), weighted ring
`judicial_or_regulatory_measure` (`:40`).

- **Reachable output set in [20,40] is {28,29,30,31,32,33,40}, plus 35 via the
  negative-signal cap. 25 is unreachable.** (Brute-force enumeration, R2.1.) Therefore
  every published score of 25 is model output. `[keyword-path]`
- `matched_rings` (`:184`) is every ring with any nonzero hit; `present_rings` (`:203`) is
  the thresholded set used for arithmetic; **the permissive set is what gets published**
  (`:252`). `[keyword-path]`
- Known blind spots (red-team probes, which test THIS path only — their own `_note` says
  so): E2/E4 (administrative-measure phrasing) stall at 33; E5 and C2 (paraphrase) score 0.
  N1 (pharma news, no ISDS) and N2 (domestic trade-secret suit) also score 33 — above the
  operative publication floor of 25. `[keyword-path]`
- Ring-1 calibration: `analytics/fingerprint-gap-report.md:99` — Ring 1's realistic
  subtotal stalls at 17, one point under `STRONG_SUBTOTAL`, so it can never carry an item
  to MEDIUM alone; it can only ever be a passenger. `[keyword-path]`

## 4. Enrichment selection

`ENRICH_TOP_N = 24` (`src/config.py:32`); ranking is lexical (`src/main.py:211-216`).
**Correction, 2026-08-08 (designer finding):** the tail was believed to be forced through
keyword scoring via `provider=None` — it is not. `classify_item(it, provider=None)` falls
through to `os.environ["MODEL_PROVIDER"]`, so in production the tail is model-classified
too; the code comment promising bounded LLM volume has been false, and the "zero-cost"
README claim is wrong on the tail as well. Recorded here; routing deliberately unchanged
this session because changing it changes production scoring and cost. What the lexical
rank therefore actually gates is **enrichment, not model access**: tail items reach the
model too, but with title/summary only, never a fetched body. The recall deprivation for a
paraphrase-heavy candidate is body text, and for headline-only sources it is total by
policy. Whether the three large early runs' ~165 tail candidates were model-classified
depends on the `MODEL_PROVIDER` environment of those runs, which no record preserves —
one more thing Phase 0 telemetry now records. The last seven runs (≤ 24 screened) have
**zero tail** either way. `[mixed]` — this selection is the boundary between the paths.

## 5. Model classification

`classify_item` (`src/classify.py:463+`): prompt from `prompts/classifier.txt` via
`build_prompt` (`:273-290`).

- **Defect (open):** `build_prompt` uses `str.replace` and `{{TEXT}}` occurs **five times**
  in the template (lines 3, 95, 101, 107, 195 — line 3 is a header comment *about* the
  template, and `_load_prompt_template` does a raw read with no comment stripping). The
  article body is inlined five times per call, spliced into the output-contract and
  quote-rule instructions; enriched calls run ~10.3k input tokens where ~5.3k would do.
  Fixing the template alone cuts enriched-call cost ~43%. `[model-path]`
- **Contract contradiction (open, decided in R2.1 but not yet encoded):**
  `prompts/classifier.txt:81` permits LOW with "one ring weakly, or none," while `:58-59`,
  `:79-80`, `:85` state three times that a judicial-measure ring alone is at least MEDIUM.
  All three published judicial-ring entries (32, 25, 25) sit under 40. `[model-path]`
- The parser (`:296-363`) validates types, coerces ring names to `VALID_RINGS`, clamps the
  score — and checks **no consistency** between score and rings, and requires **no
  evidence** for any ring. The model's score and ring list are accepted as independent
  fields (`:520-528`). `[model-path]`
- Quotation guard: `_quote_in_source` (`:439-457`) requires the notable quote to be a
  normalized substring of `raw_text + summary + title` — so for a headline-only source a
  quote lifted from the headline passes; the separate check at `src/main.py:240` papers
  over exactly that. `[model-path]`

## 6. Score/band derivation

There was none, in the shared sense — the keyword path derived (`:206-240`), the model
path accepted. **As of 2026-08-09 the shared derivation exists in shadow:** `src/rings.py`
derives a lane for every candidate from ring strengths + nexus + evidence + outcome;
legacy scores still govern the (gated) legacy surfaces; the model score is advisory only. Bands HIGH ≥ 70 / MEDIUM ≥ 40 / LOW < 40 (`fingerprint.yaml`). The R2.1 named
state model (64 ring configurations × nexus × evidence location × validity × outcome,
deriving `MATCH / ADJACENT_LEAD / HEADLINE_ONLY_LIBRARY_LEAD / REJECTED / RETRY`) is the
approved-for-development-behind-flag replacement. **Correction, 2026-08-09: as of the
2026-08-08 session `STATE_MODEL_V2` existed only in design prose, not in code — this
file previously implied an implemented flag. Implementation landed 2026-08-09: `STATE_MODEL_V2` defaults to "shadow" (publication
mode coerced off until `STATE_MODEL_V2_PUBLICATION_READY`), `src/rings.py` derives the
lane on every cycle into telemetry, and `VALIDATION_STATUS_ONLY` (independent of the
fill flag) holds all item publication and the brief. 449 tests green.**

## 7. Publication selection

`select_surfaced` (`src/main.py:53-73`): everything ≥ threshold 40; then fill to
`MIN_DIGEST_ITEMS = 6` from items ≥ `RELEVANCE_FLOOR = 25` (`src/config.py:27-28`).

- **The documented threshold has never fired: 0 matches across 347 screenings in 11 runs**
  (every `digests/*/meta.json`, `matches: 0`). **Every published item in the project's
  history was floor-fill.** The operative publication boundary is 25, not 40. `[mixed]`
- `RELEVANCE_FLOOR = 25` sits inside the keyword path's unreachable band [12,27]: the floor
  can only ever bite on model output. Under provider fallback it is inert (everything is
  ≤ 11 or ≥ 28). `[mixed]`
- The zero-state surface exists and has fired twice: 2026-06-15 (14 screened, 0 surfaced)
  and 2026-07-27 (10 screened, 0 surfaced).
- Annotations disclaiming their own item, per the coding rule (explicit negative thematic
  conclusion; hedges excluded; cannot-assess coded separately): **5** — Hydro 28,
  Telefónica-06-10 28, Okuashvili 28, Santiago 25, Gazprom 25 — plus **1** cannot-assess
  (UK High Court 25). Re-derived 2026-08-08 with the widened phrase list; the earlier count
  of 3 was an undercount. The Gazprom annotation reaches its negative conclusion about a
  body it never read. Root cause of the Telefónica double-publication (32/ring then
  28/no-ring): an unhandled research-brief exception discarded the run's seen-state after
  the digest was written — found and fixed with a regression test in the 2026-08-08 Phase 1
  work (`test_a_failing_research_brief_cannot_unwrite_the_seen_state`).

## 8. Rendering and public surfaces

- "Rings matched" as displayed = the model's unvalidated ring list `[model-path]`, or the
  permissive lexical list `[keyword-path]`. Neither means "cleared a threshold."
- `scripts/site_templates/digest.html.j2:62` renders **"no ring matched"** for an empty
  ring list — on a paywalled item this is itself a negative conclusion about an unread
  body.
- `templates/digest.html.j2:106-108` (9 archived issues): "not a gap in coverage" —
  asserts what the instrument cannot know.
- Dates: five sources set `metadata["date_inferred"]`; **no renderer reads it** — inferred
  dates print as source-stated facts.
- `docs/` is generated; the archive pages are regenerated from current markdown, not
  copies of what was mailed (`scripts/build_site.py:1089-1096`).

## 9. Archive integrity

Three maintenance commits rewrote already-sent material without disclosure: `228793c`
(deleted 10 article files from the 06-09/06-10 archives; created those runs' `meta.json`
by hand — 157 of the 347 screenings, 45%, are backfilled numbers), `9153704` (replaced
headlines published as quotations), `a6dd3d8` (replaced case captions). The 06-09 email
carried 4 items, its archive shows 2; 06-10 carried 10, shows 2. No surface discloses
this. Correction policy going forward: append, dated, never replace.

## 10. Verification record

`analytics/verification_ledger.jsonl` (append-only, refuses automated callers): digest
entries **13 distinct by URL** (14 files; Telefónica published twice — with contradictory
verdicts, 32/one-ring vs 28/no-ring, of which `verify_digest.py`'s URL dedupe silently
presents only the newer). **0 verified, 0 rejected, 13 unreviewed.** 10 of 13 rest on
paywalled bodies and are unverifiable without library access.

## 11. Validation (what exists today measures the wrong thing)

`scripts/eval_holdout.py` scores `keyword_score` in isolation at threshold 40 —
`[keyword-path]`, a boundary that has never fired. 20 items, 4 positives (2 with no IP
limb), all 16 negatives score exactly 0; positives are content-selected (its own `_note`
concedes paraphrase). Published figures 1.00/0.75/0.95/0.86 are deterministic-component
descriptive statistics; the exact CP 95% interval on the 3/4 recall is **[0.19, 0.99]**.
The 14 probes test the same path — frozen as regression, not validation. The replacement
design (54-item locked set, 9 boundary categories, blind-labelled by commit order,
production-path replay with batch shaping, stability at 20×10) is specified in the R2.1
record; primary retrieval for it is externally gated.

## 12. Telemetry

None before the 2026-08-08 repair: `classify_all` returned in-memory objects, `main.py`
printed aggregates, per-item model identity was computed and discarded. Consequence: the
archive cannot say which classifier scored 5 of the 14 published entries (the nine 25s
are provably model output — 25 is keyword-unreachable; the 28/32/35 are formally
ambiguous). Phase 0 (in flight) adds the per-candidate record.
