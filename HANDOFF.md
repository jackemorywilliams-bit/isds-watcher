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
  `src/models.py` (chairman `claude-fable-5`; heavy/utility `claude-opus-4-8`; digest
  classifier unchanged in `src/classify.py`); `RESEARCH_MODEL` remains an explicit
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
- **Vocabulary / weights**: edit `fingerprint.yaml` rings (within-ring weights should sum to
  100). `tests/test_pipeline.py::test_scorer_matches_fingerprint_examples` guards the bands —
  update the `few_shot_examples` if you change the model and re-run `pytest`.
- **LLM prompt**: `prompts/classifier.txt` (few-shot examples + strict-JSON contract). The
  pipeline substitutes `{{TITLE}} {{SOURCE}} {{URL}} {{TEXT}}`.

## Sources — current reality (from the build-time scout)
| Source | Status |
|--------|--------|
| `iisd_itn` | RSS, working (substantive descriptions). |
| `italaw` | HTML homepage "Newly Posted" feed, working (titles + dates). |
| `icsid` | Case DB is JS-only; falls back to `/news-events` announcements. |
| `iareporter_headlines` | Homepage **headlines only** (paywalled — no body fetch). |
| `unctad_isds` | Worked from the build host; may 403 from some IPs (robots disallows ClaudeBot, not our UA). Degrades to `[]` + log. |
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

- chairman: `claude-fable-5` · analyst: `claude-fable-5` (operator directive 2026-07-29:
  the researcher gets the most advanced model) · one-pager drafting: `claude-opus-4-8` ·
  utility (integrity helper, editor, graph classifier): `claude-opus-4-8` · digest
  classifier: unchanged `claude-haiku-4-5-20251001` (kept in `src/classify.py`, outside
  the change manifest). Any runtime fallback appends a REQUESTED vs ACTUAL line below
  automatically (`src/models.py record_fallback`). This session's one-pager drafting ran
  on Opus 4.8 subagents as assigned; the orchestrating session itself runs on
  `claude-fable-5` (requested and actual).
