# HANDOFF — operating the ISDS watcher

- **Repository:** https://github.com/jackemorywilliams-bit/isds-watcher
- **Website (GitHub Pages):** https://jackemorywilliams-bit.github.io/isds-watcher/
- **Digest format:** an annotated bibliography (citation + descriptive-and-evaluative
  annotation + a verbatim notable line + matched rings), emailed and archived per run.
- **Recipient:** `jackemorywilliams@icloud.com` (single; `ximena.s.benavides@gmail.com`
  is commented out in `src/config.py` and can be restored).
- **Threshold:** 40. **Default classifier:** Claude Haiku (`MODEL_PROVIDER=claude`).

## What runs, when
- GitHub Actions workflow `.github/workflows/weekly.yml`, cron `0 13 * * 1` (Mondays 13:00 UTC),
  plus manual `workflow_dispatch`. Concurrency group `isds-watcher` prevents overlap.
- `.github/workflows/human-review.yml` (the operator's Monday review packet) fires at
  `30 16 * * 1` — deliberately AFTER the weekly council so the packet's roundtable
  section can read the council's committed record. The section is sourced from
  `state/council_log.json` (never a side-channel directory); a session whose chairman
  minutes failed renders a loud MISSING banner, and a missing/stale weekly entry flags
  the pipeline itself. Guarded by `tests/test_monday_packet.py`, including a test that
  fails if the two crons are ever put back within two hours of each other.
- The job: fail-fast on missing secrets → install deps → `python -m src.main --since 7d` →
  rebuild the website → commit `state/`, `digests/`, `docs/`, and `briefs/` back as
  `github-actions[bot]`.
- Each run sends **two emails**: the **Thematic Watch digest** (annotated bibliography,
  unchanged) and the interpretive **ISDS Research Brief** produced by the research council
  (chairman → analyst+web search → deterministic integrity gate → editor). See `COUNCIL.md`.
  The brief needs the Anthropic provider (web search is an Anthropic server tool); disable
  with `RESEARCH_BRIEF_ENABLED=0`. Model ids come from the single config location
  `src/models.py` (chairman `claude-opus-5`; heavy `claude-opus-5`; utility
  `claude-opus-4-8`; digest classifier id `claude-haiku-4-5-20251001`, defined in
  `src/models.py` and imported by `src/classify.py`); `RESEARCH_MODEL` remains an explicit
  operator override for every stage, and any requested-vs-actual runtime fallback is
  appended to this file automatically. Issues land in `briefs/<date>.html`; the full council deliberation is
  preserved at `briefs/<date>-memo.md`. Continuity: each issue's open threads persist in
  `state/research_log.json` and feed the next week's chairman.

## Website stays in sync with source (guardrail)
The website (`docs/`) is generated from source (`METHODOLOGY.md`, the digest folders, the
site templates) by `scripts/build_site.py`. To stop the site drifting from source — which
recurred because `build_site` stamps each page with a wall-clock footer, masking real
drift — `.github/workflows/site-sync.yml` enforces it both ways: a **PR gate**
(`scripts/check_site_sync.py`, which rebuilds and fails on any change other than the build
stamp) and a **push-to-main auto-sync** that rebuilds and commits `docs/` whenever a source
edit lands directly on main. So editing `METHODOLOGY.md` (or any site source) updates the
website automatically; no manual rebuild needed. Locally: `python scripts/check_site_sync.py`.

## Branch protection (main)
Applied 2026-07-27 after the council found main fully unprotected (force-pushable and
deletable — able to silently rewrite the append-only research record): force pushes and
deletion are blocked for everyone including admins, with NO pull-request or status-check
requirement — deliberately, because daily-update, site-sync, weekly, and the Max routine
all push directly to main (GitHub's one-click default would have broken them all). The
heartbeat workflow re-checks `.protected` daily and emails a BRANCH PROTECTION ALERT if
it ever reads false again.

## Secrets / variables (set on the repo)
Secrets: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, and `ANTHROPIC_API_KEY`
**or** `GEMINI_API_KEY`. Variable: `MODEL_PROVIDER` (`claude` is the live default; `gemini`
is a supported alternate). The available Gemini key had no free-tier quota, which is why
Claude (~$1/mo) runs live.

```bash
gh secret set SMTP_HOST --body "smtp.gmail.com"
gh secret set SMTP_PORT --body "465"
gh secret set SMTP_USER --body "you@gmail.com"
gh secret set SMTP_PASS --body "your16charapppassword"
gh secret set ANTHROPIC_API_KEY --body "sk-ant-..."   # or GEMINI_API_KEY AIza...
gh variable set MODEL_PROVIDER --body "claude"         # default; or gemini
```

## Trigger / observe
```bash
gh workflow run weekly.yml
gh run list --workflow=weekly.yml --limit 1
gh run watch
gh run view --log-failed      # if it fails
```

## Recipients
Hard-coded in `src/config.py`: one recipient, `jackemorywilliams@icloud.com`.
`ximena.s.benavides@gmail.com` is commented out in that file — uncomment it to resume
sending to both. Edit that list and push to change recipients.

## If no email arrives
1. **Check spam/junk** on first send (new sender).
2. Confirm the run was green and the logs show `email: sent ...`. If they show
   `email: missing secrets` → a secret is empty. If `email: send failed (...534...)` →
   the Gmail App Password is wrong/expired or 2FA isn't enabled on that account.
3. A green run **always sends an email**, even a quiet week: a week with nothing above the
   relevance floor (25) sends a one-sentence "no thematically relevant developments this
   week — N candidates screened" note. So an empty inbox usually means a delivery/secret
   issue, not "nothing matched". (The very first run sends only a one-time baseline note
   while it indexes existing items.)
4. Re-run manually with `gh workflow run weekly.yml`.

## Tuning the theme / threshold
- **Threshold** lives in `fingerprint.yaml` (`threshold: 40`, lowered from an initial 60 to
  broaden recall) and is read by `src/config.py`. Raise it if the digest is noisy; lower it
  if real cases are being missed. Digest size is a hybrid (see `src/config.py`): every match
  at/above threshold with no cap, a minimum of six filled from the closest near-misses but
  only down to `RELEVANCE_FLOOR=25`, so a quiet week may carry only 0–3 items.
  **Two flags currently override that description, and both are ON by default** — read them
  as a pair, because neither can disable the other (`src/config.py:59-62`):
  `FILL_FLOOR_SUSPENDED` (since 2026-08-08) stops items scoring 25–39 from surfacing at all;
  `VALIDATION_STATUS_ONLY` (since 2026-08-09, `src/config.py:73-74`) then holds **every**
  item-level entry **including items at or above 40**, plus the Research Brief, and sends a
  single status note carrying the count of what it held. **So the sentence above describes
  the machinery, not what the instrument publishes today: today it publishes no items at
  all.** Set `VALIDATION_STATUS_ONLY=0` to publish items again — that is the validation
  decision, not a runtime convenience. Divergence tracked at `agents/Claim Map.md` **C16**.
- **Vocabulary / weights**: edit `fingerprint.yaml` rings (within-ring weights should sum to
  100). `tests/test_pipeline.py::test_scorer_matches_fingerprint_examples` guards the bands —
  update the `few_shot_examples` if you change the model and re-run `pytest`.
- **LLM prompt**: `prompts/classifier.txt` (few-shot examples + strict-JSON contract). The
  pipeline substitutes `{{TITLE}} {{SOURCE}} {{URL}} {{TEXT}}`.

## Sources — current reality (from the build-time scout)
| Source | Status |
|--------|--------|
| `iisd_itn` | RSS, working (substantive descriptions). |
| `italaw` | HTML homepage "Newly Posted" feed. The origin has served a Cloudflare managed challenge (403, `Cf-Mitigated: challenge`) on every path for non-browser clients since ~2026-07; we never evade anti-bot. **As of 2026-08-17 a 403 no longer goes dark: the pipeline's archive-recovery guard** (`src/source_recovery.py`, spec `italaw`), which captures italaw case pages within days. The guard reads recently-captured case snapshots via the public CDX index (verified live: 18 case pages in one run), keys each candidate to the real italaw URL, and lets seen-state dedup re-crawls; `body_final` metadata tells `enrich` to keep the snapshot body rather than 403 on a re-fetch. This lags live italaw by the Archive's capture latency and is disclosed as such; it auto-reverts to the live parser the moment the origin stops challenging us. Because the source now returns items, the zero-streak guard no longer flags it and no `SOURCE ACCESS FAILURE` line reaches the email. |
| `icsid` | Case DB is JS-only; falls back to `/news-events` announcements. |
| `iareporter_headlines` | Homepage **headlines only** (paywalled — no body fetch). |
| `unctad_isds` | Worked from the build host; may 403 from some IPs (robots disallows ClaudeBot, not our UA). Returns `[]` + log on a block, and the pipeline's **archive-recovery guard** (`src/source_recovery.py`, spec `unctad_isds`) then reads the same case pages from the Internet Archive — so a 403 self-heals instead of going dark. Reverts to live automatically when the origin is reachable. |
| `bing_news` | Keyword news search via Bing RSS (robots-permitted, live-verified 2026-07-29). Replaced the retired `google_news_rss`. |
| `pca_press` | Low priority; degrades to `[]` if unreachable. |

## Design guarantees
- `state/seen.json` bootstraps to `{"sources": {}}` if missing; corrupt state is treated as empty.
- Per-source and per-item failures are logged and skipped — the run always finishes and writes a digest.
- `classify_item` never raises: provider error → keyword fallback; parse error → one retry → score 0.

## Local debugging
```bash
source .venv/bin/activate
python -m src.main --dry-run --since 400d --no-email --verbose     # wide window, offline
python -m src.main --dry-run --since 7d --no-email --limit-sources iisd_itn,italaw
```
Generated digests land in `digests/<YYYY-MM-DD>.html` — open in a browser to preview the email.

<!-- graph:auto start -->
Map: [[00 - Project Map]]
<!-- graph:auto end -->

## Verification ledger & vault graph (July 2026)

- **Ledger:** `analytics/verification_ledger.jsonl` is an append-only event log; state is
  derived by replay. Only you can change a claim's status:
  `python scripts/verify.py list --status unverified` · `python scripts/verify.py mark
  <claim_id> --verified|--rejected --note "..."` · `python scripts/verify.py status`.
  Paywalled/blocked claims are labeled "forward to professor" — never self-verify those.
  Operator convention (2026-07-27): a claim the operator verifies in chat, or whose
  source the operator supplies verbatim (one-pagers, pasted primary text, a freely
  fetchable primary PDF checked by exact substring), is marked by the assistant on the
  operator's behalf with a provenance note; only genuinely operator-only or
  professor-only sources go back as action items, always with live URLs.
- **Seeded claim_ids awaiting your CLI mark** (created as candidates only; your in-chat
  review of 2026-07-18 is logged in HUMAN_REVIEW.md, but the ledger needs your `mark`):
  `721ffab48baf0098ca77…` (USTR 2026 Special 301 characterisation — you verified this),
  `5c25faf36673d6f3d789…` (China–Germany BIT "trade and business secrets" — partial; treaty
  text still with the professor), `7dd2f272f130f859d1d2…` (Hela Schwarz jurisdictional
  dismissal — still open). Run `python scripts/verify.py list` for the full ids.
- **Vault graph:** `python scripts/build_graph.py --dry-run` to preview, then without the
  flag to apply. Hubs live in `moc/`; `.obsidian/` stays untracked/gitignored.
- **One-pagers:** canonical copies in `working/one-pagers/`; the Desktop copies titled
  "(MACHINE-WRITTEN DRAFT)" are exports of those canonicals. The WalterWrites style pass
  did NOT run (runtime permission denial); to apply it manually, paste a canonical into
  the WalterWrites humanizer with quotes/case names/¶ pinpoints protected, then diff
  against the canonical before using — quotes must remain exact substrings.

## Model runtime assignments (requested)

- chairman: `claude-opus-5` · analyst: `claude-opus-5` (**operator directive 2026-08-03**, the
  Fable 5 credit balance being exhausted — `939deaa`. The 2026-07-29 directive, "the researcher
  gets the most advanced model", set `HEAVY_MODEL = "claude-fable-5"` at `4f8f981`; attaching the
  Opus 5 id to that date is the blanket-replacement error the vault records as a standing trap)
  · one-pager drafting: `claude-opus-4-8` ·
  utility (integrity helper, editor, graph classifier): `claude-opus-4-8` · digest
  classifier: unchanged `claude-haiku-4-5-20251001` (id defined in `src/models.py` as
  `DIGEST_CLASSIFIER_MODEL` and imported at `src/classify.py:58`; `src/classify.py` itself
  is outside the change manifest, which is why the *assignment* is "unchanged", but the id
  is not a second config location). ~~Any runtime fallback appends a REQUESTED vs ACTUAL line
  below automatically (`src/models.py record_fallback`).~~ **Struck 2026-08-16 as false.** It
  describes a mechanism that exists but has never run on any council path:
  `record_fallback()`'s only caller is `src/research_brief.py:161`, and no REQUESTED-vs-ACTUAL
  line has ever been appended here. The sentence read as a guarantee that a discrepancy would
  surface itself, which is part of why four separate self-reports of one went unrecorded in this
  file. This session's one-pager drafting ran on Opus 4.8 subagents as assigned; the
  orchestrating session itself runs on `claude-opus-5` (requested and actual).

### Model runtime fallbacks — recorded by hand, 2026-08-16

Written by the archivist, **not** by `record_fallback()`, and labelled so nobody mistakes it for
machine output. The heading is the one `src/models.py:18` directs runtime discrepancies to, so
the facts are filed where the code says to look for them.

| Date | Seat | REQUESTED | ACTUAL | Source |
|---|---|---|---|---|
| 2026-08-12 | integrity-officer | `claude-opus-4-8` | `claude-opus-5` | `analytics/daily-research/2026-08-12.md:750` |
| 2026-08-14 | integrity-officer | `claude-opus-4-8` | `claude-opus-5` | `analytics/daily-research/2026-08-14.md:576` |
| 2026-08-15 | integrity-officer | `claude-opus-4-8` | `claude-opus-5` | `analytics/daily-research/2026-08-15.md:693` |
| 2026-08-16 | integrity-officer | `claude-opus-4-8` | `claude-opus-5` | `analytics/daily-research/2026-08-16.md:731` |
| 2026-08-16 | obsidian-archivist | `claude-opus-4-8` | `claude-opus-5` | session runtime: `session_context.model`, `last_served_model` |
| 2026-08-15 | research-analyst | `claude-opus-5` | `claude-opus-5` | `analytics/daily-research/2026-08-15.md:497` — no discrepancy |
| 2026-08-16 | research-analyst | `claude-opus-5` | `claude-opus-5` | `analytics/daily-research/2026-08-16.md:456` — no discrepancy |

Every seat reporting a discrepancy is one documented as **Claude Opus 4.8**; every seat
documented as **Claude Opus 5** reports REQUESTED = ACTUAL. That is consistent with the cause
being the `model: opus` tier alias resolving to the platform's current Opus, and not with any
per-seat misconfiguration. Three 4.8-documented seats — `systems-researcher`, `editor`,
`analytics-officer` — have not been convened in this window and are unobserved. See
[[Workflow Threads]] **D6**.

## Checkpoint — 2026-08-08 master-prompt repair session (uncommitted, branch fix/restore-council-label)

> **Superseded as a statement of current state — read the 2026-08-09 checkpoint below first.**
> This section is kept as the dated record of what 2026-08-08 completed and measured. Its
> figures are that day's: **the suite stands at 564 passed / 5 xfailed as of 2026-08-09, not
> 414**, `check_currency` is now fully green (9 claims, 0 failed) rather than carrying 5 stale
> anchors, and the comment-reply package described below as "finalized" had five audit
> contradictions still open, all of which were closed on 2026-08-09. Nothing here is rewritten;
> the corrections live in the newer section.

Completed and tested: Phase 0 telemetry + Phase 1 seen-state + Workstream H fill-floor
suspension (414 tests green, 32 new; all guards green except check_currency's 5 known
stale anchors and check_site_sync, which correctly reports docs/ vs HEAD until this
session is committed). Telefónica double-publication root cause fixed
(research-brief exception discarded seen-state; regression test in place). Comment-reply
package audited and finalized (working/benavides-comment-replies-2026-08-08.md); canonical
memos parity-verified; Vanda CFC opinions retrieved into seeds/ and the kim-memo gap
closed on verified spans. Desktop deliverables: revised methodology, reply packet, final
Claude Chat prompt (hashes verified). Archive corrections: 9 dated appends. METHODOLOGY
§VI.B correction + §IX addition; README zero-cost corrected.

Vault reconciled the same day — record at `analytics/vault-sessions/2026-08-08.md`; open work
by thread and owner at `agents/Workflow Threads.md` (B5–B8, C11–C14). **One item this
checkpoint does not carry, and it is the largest:** suspending the fill changed the behaviour
in code and left **eight** files stating the old rule, including `METHODOLOGY.md:49` —
eighteen lines above the §IX addition that suspends it — and the public homepage. The numbers
did not move, so no existing guard catches it. The full list with owners is
`agents/Claim Map.md` **C15**, and it wants one coordinated change set rather than six
separate edits. *(2026-08-09: five of the eight are now repaired and three remain — and the
same day's second gate made four of the five stale again in the opposite direction. See
**C16**.)*

*(A mid-day 2026-08-09 line stood here reporting D/E done at 449 tests with F and G still to
come, and Emory's CI wiring still outstanding. All three have since been overtaken; it is
replaced by the checkpoint below rather than left to be read as current.)*

## Checkpoint — 2026-08-16 archivist session (`main` @ `d997c32`, clean tree)

**Nothing in the runtime changed in this window.** `git log 8ea2ee1..HEAD -- .claude/agents/
prompts/ src/models.py METHODOLOGY.md README.md scripts/site_templates/
views/isds-workflow-3d/workflow.json` returns **no commit**. The 44 commits since the last
checkpoint are the 2026-08-14/15/16 council sessions and fetch-relay chores. Every figure in the
2026-08-13 checkpoint below therefore still stands as measured; nothing was re-measured here that
did not need to be.

**Read the "Model runtime fallbacks" section above before trusting any model statement in this
file.** Five seats are documented as Claude Opus 4.8 and none is pinned to it by any file in the
repository — `model: opus` selects a tier, not a version. Two seats have now observed
`claude-opus-5` serving against a 4.8 note. `scripts/check_models.py` exits 0 over twelve cards
and is correct to: it compares declarations, and cannot see a runtime. **That the guard is green
is not evidence the models are right.**

**Clone hygiene, because it changed an answer.** The container's clone arrived shallow (201
commits). On the shallow object set, `git log -- analytics/verification_ledger.jsonl` reported
the ledger's last-touching commit as `cf7d99b` (2026-08-05); after `git fetch --unshallow` (621
commits) the true answer is `8891c21` (2026-07-27) — nineteen days earlier. The shallow read made
the ledger look **more** current than it is. Unshallow before any history or ancestry query.

**Not re-run this session:** the test suite, `scripts/check_site_sync.py` (rebuilds `docs/` in
place — see **B9**), and `scripts/build_graph.py` in write mode (whole-vault, still 3 of 27
planned files outside archivist merge authority — see **C12**).

## Checkpoint — 2026-08-13 archivist session (`main` @ `8ea2ee1`, clean tree)

**The 2026-08-08/09 work below is no longer uncommitted.** It was integrated to `main` on
2026-08-11 (`667772c` runtime/tests, `bffe79a` documentation/vault, `60f2a5b` site rebuild,
`9a6f3e8` currency fix). The two checkpoints below are kept as dated records of what those
sessions measured; their branch labels are historical, not current.

**Suite, measured in a clean clone: 562 passed, 1 failed, 3 skipped, 5 xfailed.** The failure is
**environmental, not a regression**: `tests/test_one_pagers.py:73` asserts that every one-pager's
source PDF exists under `seeds/`, which `.gitignore:2` excludes as private source material.
`scripts/check_sources.py` fails the same way (5 failures, by design — it fails closed rather
than skipping). Both pass on Emory's machine, where `seeds/` is populated. **CI never runs the
full suite** — `.github/workflows/pipeline-guards.yml` invokes named test files only — so every
"N passed" figure in this repository is a reading from one machine and should be read as one.

Guards re-run this date, all exit 0: `check_models` (12 cards), `check_lock`,
`check_headline_lane`, `check_claims`, `check_seen_integrity`, `check_telemetry_privacy`, and
`node tools/isds-workflow-3d/validate.mjs` (30 cards / 9 chips / 44 edges, manifest v2.2, SVG
fresh). **`check_currency` reports 3 of 9 claims stale**: `STATE_OF_THE_ANSWER.md` (2 commits),
`agents/Claim Map.md` (3), `agents/Workflow Threads.md` (34 — refreshed by this session).
`check_site_sync.py` was **not** run; per **B9** it rebuilds in place and is a write.

**NEEDS EMORY — seventeen of your own ledger marks never reached `main`, and the vault said they
had.** `analytics/verification_ledger.jsonl` on `main` is blob `f3dbbf6`, last written
2026-07-27 by `8891c21`. `origin/chore/operator-marks-2026-07-27` holds 40 claims / 38 marks
against `main`'s 37 / **21**. The 2026-08-11 change-log line claiming the merge carried them is
retracted — `git show --stat 0a67756 -- analytics/verification_ledger.jsonl` is empty. Three
claims are absent outright and read `unverified` to `src/integrity_gate.py`: *Hela Schwarz v.
China*, UNCITRAL WG III's 53rd session, and the Svea Court of Appeal annulment in *Okuashvili v.
Georgia*. The ledger is operator-owned; no agent has touched it. See [[Workflow Threads]] **F1**.

## Checkpoint — 2026-08-09 audit-response session (uncommitted, branch fix/restore-council-label)

**Suite: 564 passed, 5 xfailed.** All guards green, re-run this date: `check_currency`
(9 currency claims across 5 notes, 0 failed — the STATE_OF_THE_ANSWER anchor closed the last
failure), `check_lock` (reports the empty set as the designed state, exit 0),
`check_headline_lane` (no lane output on disk yet, exit 0), `check_models`, `check_claims`,
and `node tools/isds-workflow-3d/validate.mjs` (30 cards / 9 chips / 44 edges).
**One guard is not safe to run** — see the warning below.

Completed and tested this session:

- **Independent-audit correction round.** The previous session's "live e2e" verification is
  relabelled as what it was, a **fixture-backed simulation**; `STATE_OF_THE_ANSWER.md` gained
  the currency anchor it had never carried.
- **VALIDATION_STATUS_ONLY** (`src/config.py:73-74`, default ON) — the second and stronger
  publication gate. Holds **all** item publication *including items at or above 40*, and the
  Research Brief; the status note reports the held count; the fill flag cannot bypass it and
  neither flag can disable the other.
- **STATE_MODEL_V2 is real code, not prose** — `src/rings.py` + shadow derivation on every
  cycle. The semantic V2 path is built end to end (`src/classify_v2.py`,
  `prompts/classifier_v2.txt`), but `V2_SHADOW_CALLS` defaults **off**, so every default-run
  verdict is labelled `lexical_only`; `replace` is refused; verdicts carry `claims_source`
  provenance; `guard_demoted` fires on every V1 ring claim because V1 supplies no spans.
- **7-vs-4 outcomes resolved losslessly** — seven logical states → four operational outcomes
  plus metadata; enumeration **21,504**; rationale at
  `analytics/state-space-resolution-2026-08-09.md`. Tail provider failures are now counted;
  they were under-counted by the size of the tail.
- **Workstream F** — `src/triage.py` + `prompts/triage.txt`, `TRIAGE_ENABLED` off by default,
  deterministic sort, provider-absence recorded rather than misreported, adversarial tests.
  **Design (c) tail audit is a config stub only** (`TAIL_AUDIT_N = 0`), expressly
  unimplemented.
- **Workstream G** — `src/headline_lane.py`, a closed grammar with **three** location-keyed
  limitation clauses rather than one (a retrieved-body comparator may not claim paywall);
  `scripts/check_headline_lane.py` enforces byte-identity; the public-label mapping no longer
  calls an accessible-body item a library lead.
- **CI** — `.github/workflows/pipeline-guards.yml` wires telemetry-privacy, seen-integrity,
  headline-lane, lock and currency (currency in its own job with `fetch-depth: 0`), each with
  its planted-violation tests. `scripts/check_lock.py` written.
- **Comment-package parity round** — five audit contradictions closed. **H&H v. Egypt closed by
  retrieval:** Decision on Jurisdiction (`ita1012.pdf`) and Award Rule 48(4) excerpts
  (`italaw7979.pdf`) now in `seeds/`, 21 spans verified; the retrieval **corrected two claims**
  (causal-link scope narrowed to the corruption claim; the sector attribution deleted, not
  re-attributed) and the dead `italaw.com/cases/542` URL was replaced. "Structural" became "a
  deliberate scope boundary"; Item 6 balancing narrowed; disclosure categorical qualified;
  Part 5 items 5/13/15 updated. **The full Award is unpublished — Rule 48(4) excerpts only,
  recorded as a permanent scope limit, not a gap slug.**
- **Walter round 2** — 3 passages, none adopted: 1 exempt by construction (sentinel chain),
  2 rejected at the gate (content dropped + meaning flip; sentinel destroyed). Canonical stands.
- **METHODOLOGY §IX** updated to 21,504, the three off-by-default capabilities, and the CI
  wiring.

> ⚠ **`scripts/check_site_sync.py` is not safe to run as a read-only check.** It rebuilds
> `docs/` **in place** — `:25` invokes `build_site.py` with no temporary directory and `:31`
> then diffs the working tree — so invoking it *mutates* the repository. It reverted `docs/`
> to HEAD this session on the belief that it was stamp-only. `docs/` will be rebuilt from
> source in the integrator's final battery. Open defect: `agents/Workflow Threads.md` **B9**.

**Still Emory's, and now urgent:** merge-or-skip before the **Monday 13:00 UTC** run — the
weekly cron is `0 13 * * 1`, so this expires in about a day
(`agents/Workflow Threads.md` **C12**). The CI wiring that was outstanding at the start of the
day is **built** and sitting uncommitted; authorizing it is still Emory's, because it changes
what fails a PR (**C11**). Externally gated retrievals remain at
`analytics/locked_set/RETRIEVAL_LEDGER.md`: **2 RETRIEVED, 3 BLOCKED, 8 QUEUED**, unchanged
today — the H&H documents were retrieved into `seeds/` but that matter has never had a row in
that ledger.

**What this checkpoint does not carry, stated because the 08-08 one hid the same thing.**
Repairing five files to describe `FILL_FLOOR_SUSPENDED` and then adding
`VALIDATION_STATUS_ONLY` in the same session left four of those five files **stale again, in
the opposite direction** — they now say items at or above 40 are published, and none are.
`METHODOLOGY.md:49` and `:69` contradict each other twenty lines apart, which is the exact
defect 08-08 recorded and resolved to stop producing. The full list with owners is
`agents/Claim Map.md` **C16**, and it must be fixed in one change set together with the
**three** rows of **C15** that are still open (`fingerprint.yaml`, the `quality-bar` card, and
`src/main.py:687-690`) — C15 is **not** resolved, whatever the session reports say.

Vault reconciled the same day — record at `analytics/vault-sessions/2026-08-09.md`; open work
by thread and owner at `agents/Workflow Threads.md`.
