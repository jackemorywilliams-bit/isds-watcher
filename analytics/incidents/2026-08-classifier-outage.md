# Incident — the classifier was dead from 2026-08-24 to 2026-09-07

**Owner:** analytics officer (row K, council special session of 2026-09-10).
**Status:** closed as an incident; two consequences remain open (§1.6, §3.4).
**Baseline:** every figure below was copied from `digests/*/meta.json`,
`analytics/candidate_telemetry.jsonl`, `analytics/abandoned_candidates.jsonl`,
`analytics/requeued_candidates.jsonl`, `state/seen.json`, `git show`, or
`gh run view <id> --log`, against `origin/main` at `61152d5`. The locator sits beside
each number. Nothing here is restated from memory, and nothing here is recomputed from
a figure stated elsewhere in the project.

**Terminology (daily council protocol, Rule 1).** CANDIDATES EVALUATED is
`meta["screened"]`. ITEMS SURFACED is `meta["matches"]` plus `meta["watch_list_leads"]`.
The bare word "screened" with a number attached is not used in this file except as the
name of a JSON field.

---

## 1. The outage

### 1.1 What failed

`Messages.create() got an unexpected keyword argument 'temperature'`, raised on every
Anthropic call. The anthropic 1.x SDK removed `temperature` from `Messages.create()`;
`requirements.txt` pinned `anthropic>=0.40` with no ceiling, the runner installed 1.4.0,
and `src/classify.py` passed `temperature=0`. The local SDK (0.107.1) still accepted it,
so nothing failed locally.

Locator: commit body of `d88f325` (2026-09-07 17:21:14 -0400,
*"fix(classifier): dead since 08-24 — anthropic 1.x compat, a provider canary that charges
no item, 8 abandonments reversed"*), and the error string itself in the logs of each run
in §1.2.

### 1.2 Three consecutive weekly dates, five failed run executions, 2026-09-07 PARTIAL

Six executions of `.github/workflows/weekly.yml` fall inside the window. Five of them made
no successful model call. The sixth, at 2026-09-07 23:25:35Z, ran behind `d88f325` and
classified every candidate with the model.

Each row's digest commit is tied to its workflow run by `git log -1 --format=%P` on the
commit: **the commit's parent is exactly that run's `headSha`** in every one of the six
cases. Each row's telemetry `run_id` is tied to the same commit by the fact that the
commit is the one that appended that `run_id`'s block to
`analytics/candidate_telemetry.jsonl` (verified by `git show <sha>:analytics/candidate_telemetry.jsonl`
and differencing the `run_id` sets commit by commit).

| # | GH run id | Started (UTC) | Event | Digest commit | Telemetry `run_id` | `meta["screened"]` at that commit | Classifier |
|---|---|---|---|---|---|---|---|
| 1 | `32734655573` | 2026-08-24 13:46:21Z | schedule | `719a9fc` (13:50:01Z) | `2026-08-24-7c2124e4bf83` | 26 | DEAD |
| 2 | `32749425086` | 2026-08-24 16:11:57Z | workflow_dispatch | `dc7b207` (16:15:26Z) | `2026-08-24-060f85762ff1` | 30 | DEAD |
| 3 | `33430080838` | 2026-08-31 19:21:11Z | schedule | `4cfc45a` (19:29:12Z) | `2026-08-31-5a790d2846ed` | 67 | DEAD |
| 4 | `34150055790` | 2026-09-07 18:02:56Z | schedule | `08d67d1` (18:06:47Z) | `2026-09-07-5a8ae4cd79d2` | 110 | DEAD |
| 5 | `34161164724` | 2026-09-07 20:54:34Z | workflow_dispatch | `2adb925` (21:02:29Z) | `2026-09-07-8e4019975861` | 28 | DEAD |
| 6 | `34169997179` | 2026-09-07 23:25:35Z | workflow_dispatch | `238f0f4` (23:32:09Z) | `2026-09-07-b5eef5795701` | 30 | **ALIVE — the repair** |

Run 6 is the run that fixed it. Its log carries no `!! DEGRADED` line, no occurrence of
`unexpected keyword argument 'temperature'` (`grep -c` returns 0), and
`classified: 30` / `new candidates: 30`.

**2026-09-07 is therefore a PARTIAL date**, and it is partial in a specific direction that
matters to anyone reading the archive: the surviving artefact for 2026-09-07 is the output
of the healthy run, because a same-day re-run overwrites the digest folder in place. The
two failed executions of that date survive only in git history and in telemetry.

### 1.3 Why the record says "four" and why "four" is wrong

`d88f325`'s own commit body names *"the 08-24, 08-31, 09-07 18:02 and 09-07 20:54 runs —
the classifier had made no successful call for four weekly runs"*. It omits run
`32734655573`, the **scheduled** 2026-08-24 13:46:21Z execution, whose log shows
`!! DEGRADED: 24 of 26 candidates could not be classified (provider_error=24)` and 26
occurrences of the SDK error. `HANDOFF.md:63` then converted the commit's "four" into
"four weekly runs (08-24 → 09-07)", an interval containing three Mondays.

The correct statement is **three consecutive weekly dates, five failed run executions,
2026-09-07 partial**. It is reproducible from `gh run list --workflow=weekly.yml`, from the
six digest-commit parents, and from the nine `run_id`s in `analytics/candidate_telemetry.jsonl`.
It is not reproducible from any artefact that says four.

### 1.4 The marker that must NOT be used

`meta["validation_status_only"]` is `true` on exactly four archived digests —
**2026-08-17, 2026-08-24, 2026-08-31, 2026-09-07** (read from the sixteen `meta.json`
files). It is a tempting outage marker because it, too, returns four. It is wrong in both
directions:

- It includes **2026-08-17**, which was healthy: three telemetry `run_id`s
  (`2026-08-17-32091aeb6475` 13 rows, `…-c9d5cdf3762d` 17, `…-d2d2221eaa54` 7), all 37
  records `path: llm`, `outcome: ok`, `model: claude-haiku-4-5-20251001`.
- It includes **2026-09-07**, whose surviving artefact came from the repaired run.
- It excludes nothing and marks nothing about the classifier. It is a publication gate,
  printed as `!! VALIDATION_STATUS_ONLY: item-level publication is gated` — it appears in
  run 6's log too, the healthy one.

The coincidence of "four" is the trap. Use §5's list.

### 1.5 What each execution did with intake

`deferred` and `abandoned` per run are copied from the run log's own summary lines
(`!! deferred for retry (NOT marked seen): N`, `!! ABANDONED after 3 attempts: N`) and
independently recounted from `analytics/candidate_telemetry.jsonl` by `dedup.deferred` and
`dedup.abandoned`. The two sources agree on every row.

| GH run id | `meta["screened"]` | Enriched (telemetry `entered_enrichment`) | Tail (telemetry, not `entered_enrichment`) | `!! DEGRADED` line | Deferred | Abandoned | Retried from the deferred queue |
|---|---|---|---|---|---|---|---|
| `32734655573` | 26 | 24 | 2 | `24 of 26 … (provider_error=24)` | 24 | 0 | 0 |
| `32749425086` | 30 | 24 | 6 | `24 of 30 … (provider_error=24)` | 24 | 0 | 24 |
| `33430080838` | 67 | 24 | 43 | `24 of 67 … (provider_error=24)` | 8 | **16** | 24 |
| `34150055790` | 110 | 24 | 86 | `24 of 110 … (provider_error=24)` | 19 | **5** | 8 |
| `34161164724` | 28 | 24 | 4 | `24 of 28 … (provider_error=24)` | 21 | **3** | 19 |
| `34169997179` | 30 | 24 | 6 | *(none)* | 0 | 0 | 29 |

"Retried from the deferred queue" is the run log's own
`N new candidates across sources (M retried from the deferred queue)` line.

Two arithmetic facts that fall out of this table and are worth keeping, because both are
checkable and neither is an inference:

- **Every candidate was charged a model call on a failed run, not only the enriched 24.**
  The count of `unexpected keyword argument 'temperature'` lines in each failed run's log
  equals that run's `meta["screened"]`: 26, 30, 67, 110, 28 — total **261**. Telemetry for
  the same five runs holds 120 records at `classification.outcome: provider_error` and 141
  at `keyword_only_by_design`; 120 + 141 = 261. The 141 are the tail, and they carry
  `attempts: 1`, which is why they are mislabelled as by-design. (This is the defect row C
  repairs. It is recorded here only as the outage's fingerprint, not re-argued.)
- **The enriched set is capped at 24 on every one of the six runs** (`src/config.py:200`, `ENRICH_TOP_N = 24`), so `provider_error=24`
  is a property of the enrichment cap, not a measure of the outage's size.

### 1.6 The abandonment ledger: 24 abandoned, 8 requeued, 16 still abandoned (as of `61152d5`)

- `analytics/abandoned_candidates.jsonl` holds **24** rows. All 24 carry
  `last_outcome: provider_error` and `attempts: 3`. By the `run` field: **16 stamped
  `2026-08-31`, 8 stamped `2026-09-07`** (the 8 split 5 + 3 across runs `34150055790` and
  `34161164724`, matching those runs' `!! ABANDONED` lines exactly). By source: 11
  `iareporter_headlines`, 6 `gdelt`, 6 `gmail_scholar`, 1 `google_alerts`.
- `analytics/requeued_candidates.jsonl` holds **8** rows, every one `abandoned_run:
  2026-09-07`, every one stamped `at: 2026-09-07T21:15:22…`, with `because` reading
  *"anthropic 1.x SDK removed temperature from Messages.create(); every classify call since
  2026-08-24 raised TypeError — all three attempts were the instrument's failure, not the
  item's"*. The 8 are a strict subset of the 24.
- **16 remain.** `state/seen.json` holds exactly **16** entries at `outcome: "abandoned"`
  (4 `gdelt`, 11 `iareporter_headlines`, 1 `google_alerts`), and the set is
  **identical** to the 24-minus-8 remainder — checked pair by pair on
  `(source, source_id)`, not by count. Every one is an instrument failure, not a judgement
  about the item: three attempts that were all the same `TypeError`.

**Still open.** As of `origin/main` at `61152d5` the 16 are unreversed. A local branch
`council/requeue-0831-abandonments` carries `e10fec6`
*"fix(state): requeue the sixteen 2026-08-31 abandonments the dead classifier caused"*;
`git merge-base --is-ancestor e10fec6 HEAD` returns false and no remote branch contains
it. Until that lands, the figure to publish is 16.

### 1.7 What the archive does not show

All three dead dates' READMEs read `classifier: claude`, because `src/render.py:290` prints
the *configured* provider rather than whether a model answered. `digests/2026-08-24…/README.md:5`
and `digests/2026-09-07…/README.md:7` both read
`(screened from 30 candidates; classifier: claude; threshold 40)`. `grep -rl "keyword-fallback" digests/`
returns nothing. The outage left no self-evident trace in the published archive, which is
why this file exists and why §5 gives the site a marker to render.

---

## 2. The denominator

### 2.1 The sentence row G can render

> **492 is the number of CANDIDATES EVALUATED summed over the 16 archived runs — the sum of
> `meta["screened"]` across the sixteen `digests/*/meta.json` files on `main` — so it counts
> screening events in the surviving archive, and it is not a count of pipeline runs, of
> evaluation events recorded in telemetry, or of distinct candidates.**

### 2.2 The four counts side by side

| Denominator | Count | What it counts | Locator |
|---|---|---|---|
| **Archived digests** | **16** | Digest folders on `main` carrying a `meta.json`. One per *date*, because a same-day re-run overwrites the folder in place. | `ls digests/*/meta.json \| wc -l` → 16 |
| — CANDIDATES EVALUATED across them | **492** | `sum(meta["screened"])` over those 16 files. ITEMS SURFACED across them: 17 (0 matches + 17 watch-list leads). | the sixteen `digests/*/meta.json`; per-run: 06-09 78, 06-10 79, 06-15 14, 06-16 80, 06-22 11, 06-29 12, 07-06 13, 07-13 23, 07-20 14, 07-27 10, 08-03 13, 08-10 11, 08-17 7, 08-24 30, 08-31 67, 09-07 30 |
| **Pipeline run executions** | **33** | Executions of `.github/workflows/weekly.yml` recorded by GitHub Actions, 2026-06-08T23:00:31Z → 2026-09-07T23:25:35Z, dispatches included: 20 `workflow_dispatch` + 13 `schedule`; 30 concluded `success`, 3 `failure`. The 30 successes correspond one-to-one with the 30 commits whose subject is exactly `chore: weekly digest + state update [skip ci]`. Seventeen distinct UTC dates. | `gh run list --workflow=weekly.yml --limit 200`; `git log --format=%s --grep='weekly digest'` |
| **Evaluation events in telemetry** | **328** | Records in `analytics/candidate_telemetry.jsonl`, one per candidate per run execution, across **9** `run_id`s on **4** run dates only (2026-08-17 ×3, 08-24 ×2, 08-31 ×1, 09-07 ×3). Telemetry begins at 2026-08-17; it does not cover the first twelve archived runs. | `wc -l analytics/candidate_telemetry.jsonl` → 328; `run_id` counts 13/17/7, 26/30, 67, 110/28/30 |
| **Distinct candidates** | **not established** | No cross-run de-duplicated total has ever been computed, and none is computed here. BLOCKING 1 of the 2026-09-10 special session bars publishing any de-duplicated figure. Telemetry could only ever answer it for 4 of the 16 dates in any case. | BLOCKING 1; telemetry's 4-date coverage above |

### 2.3 The three traps in that table

1. **16 ≠ 33.** The archive is date-keyed, so four dates in the outage window alone carry
   more executions than folders. Any surface that says "16 runs" is saying *sixteen
   archived digests*, which is true, and is not saying *sixteen times the pipeline ran*,
   which is false.
2. **492 counts the surviving artefact of each date.** Telemetry records more evaluation
   events for 2026-09-07 than the archive does (110 + 28 + 30 = 168 records against
   `meta["screened"] = 30`), because the archive kept the last run of the date. This is not
   loss or suppression — the path is date-keyed. No de-duplicated or higher total may be
   derived from it.
3. **328 is not a project total.** It starts at 2026-08-17. A ratio with 492 as its
   denominator and 328 as its numerator would be meaningless, and no rate, accuracy, or
   trend of any kind may be derived from the 16 runs — 0 matches across 492 CANDIDATES
   EVALUATED is a negative result about an unvalidated instrument, not a measurement of one.

---

## 3. `per_source` vs `source_health[].count` — GAP-UNRESOLVED: per-source-count-semantics, RESOLVED

### 3.1 The rule, in one sentence

> **`per_source[src]` counts the items from that source this run that the seen-state had
> never seen before (the receptivity denominator); `source_health[].count` counts every
> item the fetch returned from that source, seen or not (the readability signal) — so
> `source_health[].count` ≥ `per_source[src]` wherever both fields are present (`digests/2026-06-29_ISDS-Thematic-Watch/meta.json` carries `per_source` but no `source_health`), and neither one sums to
> `meta["screened"]`.**

### 3.2 The code, with locators

`src/main.py`, inside the per-source fetch loop:

- `:254` `items = src.fetch(since)` — everything the source returned.
- `:266` `fresh = [it for it in items if not state.is_seen(st, src.name, it.source_id)]`
- `:267` `stats["per_source"][src.name] = len(fresh)` — **`per_source` is `len(fresh)`.**
- `:285` `entry = {"name": src.name, "status": status, "count": len(items)}` —
  **`source_health[].count` is `len(items)`.**

Archive recovery writes both fields again, keeping the same distinction:

- `:312` `recovered = source_recovery.recover(entry["name"], since)`
- `:316` `fresh_rec = [it for it in recovered if not state.is_seen(…)]`
- `:319` `entry["count"] = len(recovered)` — all pages recovered.
- `:321` `stats["per_source"][entry["name"]] = len(fresh_rec)` — the unseen ones.

Both are persisted verbatim into `meta.json` by `src/render.py:264` and `:266`. The
`per_source` meaning was already documented at `src/render.py:240-241` —
*"per_source = fresh candidates fetched per source this run (the denominator for
receptivity over time)"*. What had never been written down is that it is a **different
denominator** from `source_health[].count`, and that neither is CANDIDATES EVALUATED.

### 3.3 The three disagreements in `digests/2026-09-07_ISDS-Thematic-Watch/meta.json`, resolved

| Source | `per_source` | `source_health[].count` | `status` | Reading |
|---|---|---|---|---|
| `italaw` | 0 | 12 | `RECOVERED (Internet Archive)` | 12 pages recovered from the Archive; all 12 already in the seen-state, so 0 new. |
| `unctad_isds` | 0 | 5 | `RECOVERED (Internet Archive)` | 5 recovered; all 5 already seen. |
| `pca_press` | 2 | 3 | `RETURNED` | 3 items fetched live; 1 already seen; 2 new. |

Both numbers are correct and they were never in conflict. The recovery guard worked as
designed: it reached content the live origin refused, and the seen-state correctly declined
to re-screen pages the instrument had already screened. `italaw` and `unctad_isds` at
`per_source` 0 on this run are **not** evidence of a quiet or failed source.

**Why the three totals differ (all three are right):**

- `sum(per_source)` = 14 — items never seen before, from the live fetch and from recovery.
- `sum(source_health[].count)` = 32 — every item every source returned, seen or not.
- `meta["screened"]` = 30 — `stats["total_candidates"]`, set at `src/main.py:343` after
  `:341` `new_candidates = returning + new_candidates`, where `returning`
  (`:337`) is the backlog rebuilt from the deferred queue.

So **`meta["screened"] − sum(per_source)` = the count of items rebuilt from the deferred
queue**: 30 − 14 = 16 on 2026-09-07. The run's own log corroborates it —
`30 new candidates across sources (29 retried from the deferred queue)`, where 29 is
`len(returning) + carried` (`:342`), i.e. 16 rebuilt from the queue plus 13 that the source
still listed and that carried an attempt count forward. The identity holds on the other
runs too: 08-31, 67 − 44 = 23 rebuilt with 24 retried (23 + 1 carried); 08-24 (`dc7b207` / run `32749425086`), 30 − 30 = 0
rebuilt with 24 retried (0 rebuilt + 24 carried — the same date's other execution, `719a9fc` / run `32734655573`, had 0 retried).

### 3.4 What this releases, and the one thing it does not

BLOCKING 1's bar on publishing from `per_source` is discharged **for surfaces that carry the
rule in §3.1**. One live surface does not carry it and must be corrected before the site is
rebuilt — this is handed to row G, not actioned here:

- `scripts/build_site.py:928` and `:936` aggregate `per_source` into a variable named
  `screened_by`, emitted at `:946` as `{"screened": …}`, and
  `scripts/site_templates/digest_index.html.j2:81` and `:93` label that column
  **"Candidates evaluated"** — the daily council protocol's fixed term for
  `meta["screened"]`. Across the 11 archived runs that carry `per_source`, that column sums
  to **191**, while `meta["screened"]` over the same 11 runs sums to **230** and over all 16
  to 492. The same page shows both labels for two different quantities.
- `analytics/source-receptivity.md` is already correct: it calls the column
  **"Fresh candidates"** and states its own coverage ("per-source candidate counts available
  for **11** of them"). Its per-source column also sums to 191.

The fix is a label, not a number: the per-source column is **fresh candidates**, never
CANDIDATES EVALUATED.

---

## 4. Runs whose published figures were produced with the classifier dead

Do not read performance, yield, receptivity, or a quiet week out of these. In each case
`meta["matches"] = 0` and ITEMS SURFACED = 0, and in each case the model contributed
nothing to those zeros.

**Live on `main` in the archive — 2 of the 16 archived digests:**

| Archived digest | `meta["screened"]` | ITEMS SURFACED | Telemetry for the run behind it |
|---|---|---|---|
| `digests/2026-08-24_ISDS-Thematic-Watch/` | 30 | 0 | `2026-08-24-060f85762ff1` — 24 `provider_error`, 6 `keyword_only_by_design`, 0 `ok` |
| `digests/2026-08-31_ISDS-Thematic-Watch/` | 67 | 0 | `2026-08-31-5a790d2846ed` — 24 `provider_error`, 43 `keyword_only_by_design`, 0 `ok` |

**In git history only, overwritten by a later same-day run — 3 more:**

| Commit | Date | `meta["screened"]` at that commit | Telemetry |
|---|---|---|---|
| `719a9fc` | 2026-08-24 | 26 | `2026-08-24-7c2124e4bf83` — 24 `provider_error`, 2 `keyword_only_by_design` |
| `08d67d1` | 2026-09-07 | 110 | `2026-09-07-5a8ae4cd79d2` — 24 `provider_error`, 86 `keyword_only_by_design` |
| `2adb925` | 2026-09-07 | 28 | `2026-09-07-8e4019975861` — 24 `provider_error`, 4 `keyword_only_by_design` |

**Explicitly NOT on this list, and both are easy to put there by mistake:**

- **`digests/2026-09-07_ISDS-Thematic-Watch/`** — its `meta.json` was written by `238f0f4`
  from run `34169997179`, telemetry `2026-09-07-b5eef5795701`: **30 records, all
  `path: llm`, `outcome: ok`, `model: claude-haiku-4-5-20251001`**. The classifier was
  alive. The date is still marked in §5 as `partial`, for a different and narrower reason:
  its intake is outage-shaped. Sixteen of its 30 CANDIDATES EVALUATED were rebuilt from the
  deferred queue (§3.3), the 8 items abandoned earlier that day were requeued into it at
  21:15:22Z, and the 16 abandoned on 2026-08-31 were not (§1.6) — so this run evaluated a
  backlog the outage created, minus 16 items the outage removed.
- **`digests/2026-08-17_ISDS-Thematic-Watch/`** — healthy. 37 telemetry records across three
  `run_id`s, all `path: llm`, `outcome: ok`. It carries `validation_status_only: true`,
  which is why it keeps being swept in. It does not belong here.

---

## 5. Machine-readable marker

For a per-archived-digest badge. `state` is the state of the **archived artefact** at that
date, which is not always the state of the date: `2026-09-07` is `partial` because two of
its three executions failed and its intake carries the outage's backlog, even though the
surviving `meta.json` came from the repaired run.

```json
{
  "incident": "anthropic-1x-temperature",
  "record": "analytics/incidents/2026-08-classifier-outage.md",
  "cause": "anthropic 1.x SDK removed temperature from Messages.create(); anthropic>=0.40 pinned with no ceiling",
  "fixed_by": "d88f325",
  "outage_dates": ["2026-08-24", "2026-08-31", "2026-09-07"],
  "failed_executions": 5,
  "evidence_note": "the six executions on the three dates, oldest first; the sixth is the repaired 09-07 23:25 UTC run, so failed_executions counts the first five",
  "evidence": [
    "32734655573",
    "32749425086",
    "33430080838",
    "34150055790",
    "34161164724",
    "34169997179"
  ],
  "per_digest": {
    "2026-08-24": {
      "state": "classifier_dead",
      "note": "Archived figures were produced with no successful model call.",
      "workflow_runs": ["32734655573", "32749425086"],
      "archived_from_run": "32749425086",
      "archived_from_commit": "dc7b207",
      "telemetry_run_id": "2026-08-24-060f85762ff1"
    },
    "2026-08-31": {
      "state": "classifier_dead",
      "note": "Archived figures were produced with no successful model call.",
      "workflow_runs": ["33430080838"],
      "archived_from_run": "33430080838",
      "archived_from_commit": "4cfc45a",
      "telemetry_run_id": "2026-08-31-5a790d2846ed"
    },
    "2026-09-07": {
      "state": "partial",
      "note": "Two of three executions failed; the archived figures came from the repaired run, but its intake is the outage's backlog and 16 items abandoned on 2026-08-31 were not requeued into it.",
      "workflow_runs": ["34150055790", "34161164724", "34169997179"],
      "archived_from_run": "34169997179",
      "archived_from_commit": "238f0f4",
      "telemetry_run_id": "2026-09-07-b5eef5795701"
    }
  },
  "abandonment": {
    "abandoned": 24,
    "requeued": 8,
    "still_abandoned": 16,
    "as_of_commit": "61152d5",
    "still_abandoned_all_from_run": "2026-08-31",
    "locator": "analytics/abandoned_candidates.jsonl, analytics/requeued_candidates.jsonl, state/seen.json outcome=abandoned"
  },
  "do_not_use_as_marker": "meta.validation_status_only — true on 2026-08-17 (healthy) and 2026-09-07 (repaired); it is a publication gate, not a classifier state"
}
```

---

## 6. Bounds on this record

- No sensitivity, specificity, precision, recall, or temporal claim is derived from the 16
  archived runs, and none may be. The instrument has never produced a match, and it has
  never been validated against a labelled set.
- No candidate total other than 492 is published, and no de-duplicated total is computed
  (BLOCKING 1).
- The 110-candidate execution of 2026-09-07 is not lost, failed, or suppressed. It was
  superseded on a date-keyed path.
- `analytics/candidate_telemetry.jsonl`'s 141 `keyword_only_by_design` records at
  `attempts: 1` are named here as the outage's fingerprint only. Their mislabelling is a
  separate defect with a separate owner.
