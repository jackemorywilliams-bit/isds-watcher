# HANDOFF — operating the ISDS watcher

## What runs, when
- GitHub Actions workflow `.github/workflows/weekly.yml`, cron `0 13 * * 1` (Mondays 13:00 UTC),
  plus manual `workflow_dispatch`. Concurrency group `isds-watcher` prevents overlap.
- The job: fail-fast on missing secrets → install deps → `python -m src.main --since 7d` →
  commit `state/` + `digests/` back as `github-actions[bot]`.

## Secrets / variables (set on the repo)
Secrets: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, and `GEMINI_API_KEY` **or**
`ANTHROPIC_API_KEY`. Variable: `MODEL_PROVIDER` (`gemini` or `claude`).

```bash
gh secret set SMTP_HOST --body "smtp.gmail.com"
gh secret set SMTP_PORT --body "465"
gh secret set SMTP_USER --body "you@gmail.com"
gh secret set SMTP_PASS --body "your16charapppassword"
gh secret set GEMINI_API_KEY --body "AIza..."      # or ANTHROPIC_API_KEY sk-ant-...
gh variable set MODEL_PROVIDER --body "gemini"      # or claude
```

## Trigger / observe
```bash
gh workflow run weekly.yml
gh run list --workflow=weekly.yml --limit 1
gh run watch
gh run view --log-failed      # if it fails
```

## Recipients
Hard-coded in `src/config.py`: `ximena.s.benavides@gmail.com`, `jackemorywilliams@icloud.com`.
Edit that list and push to change them.

## If no email arrives
1. **Check spam/junk** on first send (new sender).
2. Confirm the run was green and the logs show `email: sent ...`. If they show
   `email: missing secrets` → a secret is empty. If `email: send failed (...534...)` →
   the Gmail App Password is wrong/expired or 2FA isn't enabled on that account.
3. A green run with **0 matches still sends** a "No new matches this week" digest, so an
   empty inbox usually means a delivery/secret issue, not "nothing matched".
4. Re-run manually with `gh workflow run weekly.yml`.

## Tuning the theme / threshold
- **Threshold** lives in `fingerprint.yaml` (`threshold: 60`) and is read by `src/config.py`.
  Raise it if the digest is noisy; lower it if real cases are being missed.
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
| `google_news_rss` | **robots-disallowed** for `*` → honored, returns `[]`. Re-enables if Google changes robots. |
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
