# ISDS Thematic Watcher

A zero-cost, weekly watcher for **investor–state dispute settlement (ISDS)** developments
at a specific doctrinal intersection — three overlapping "rings":

1. **IP-as-investment** — patents, trademarks/licenses, copyrights, GIs, data exclusivity, brand value as a covered investment.
2. **Regulatory or judicial measure as the disputed conduct** — public-interest legislation, a domestic court judgment, or judicial conduct itself (this ring carries extra weight).
3. **Jurisdictional / admissibility doctrines** — abuse of right, treaty-shopping, foreseeability of dispute, shell/restructuring for treaty protection, denial of benefits, the definition of "investor", standing to claim denial of justice.

The fingerprint was mined verbatim from three seed awards: **Philip Morris v Australia**,
**Eli Lilly v Canada**, and **Bridgestone v Panama** (see `PLAN.md`).

It runs every Monday on GitHub Actions, classifies new items with an LLM (Gemini Flash free
tier, or Claude Haiku), renders an HTML digest, and emails it to the recipients.

## How it works

```
sources/*  →  dedupe (state/seen.json)  →  classify.py (LLM or keyword fallback)
           →  filter ≥ threshold  →  render.py → digests/<date>.html  →  email_send.py
```

- **Sources** (`src/sources/`): `iisd_itn` (RSS), `italaw`, `icsid`, `iareporter_headlines`
  (HTML headlines), `unctad_isds`, `pca_press`, and `google_news_rss`. Each is defensive:
  primary + fallback selectors for HTML, robots.txt honored, ≥3 s/domain rate limit,
  identifying User-Agent. A failing source returns `[]` and logs — it never crashes the run.
- **Classifier** (`src/classify.py`): picks Gemini or Anthropic via `MODEL_PROVIDER`. On a
  JSON parse failure it retries once with a stricter prompt, then scores 0 +
  `classification_failed`. With **no API key it falls back to an offline keyword scorer**
  built from `fingerprint.yaml` (so dry-runs work fully offline).
- **Scoring**: HIGH ≥70 (two rings), MEDIUM 40–69 (one strong ring + weak tie, or any
  judicial-measure case alone), LOW <40. Threshold to appear in the digest: **60**.

## Run locally

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Fully offline (no key, no email) — uses the keyword fallback classifier:
python -m src.main --dry-run --since 7d --no-email

# With an LLM and email (needs a .env — see .env.example):
python -m src.main --since 7d
pytest tests/
```

`--since` accepts `7d`, `14d`, `48h`, `1w`, `30m`.

## Configuration

Runtime config comes from the environment (locally via `.env`, in CI via Secrets/Variables):

| Name | Where | Purpose |
|------|-------|---------|
| `MODEL_PROVIDER` | Actions **variable** | `gemini` (default) or `claude` |
| `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` | Secret | classifier key (match the provider) |
| `SMTP_HOST` / `SMTP_PORT` | Secret | `smtp.gmail.com` / `465` |
| `SMTP_USER` / `SMTP_PASS` | Secret | Gmail address + 16-char App Password |

Optional overrides: `GEMINI_MODEL` (default `gemini-1.5-flash`), `ANTHROPIC_MODEL`
(default `claude-haiku-4-5-20251001`).

Recipients are hard-coded in `src/config.py`.

## Cost

Public repo → unlimited GitHub Actions minutes. Gemini Flash free tier → $0. Claude Haiku
≈ $1/month if you prefer it. No paid data sources — open feeds and pages only.

## Notes / limitations

- **Google News RSS is currently robots-disallowed** (`news.google.com/robots.txt` disallows
  `/rss/` for `*`). The watcher honors it: the source returns `[]` and logs. It is wired up
  and will activate automatically if that policy changes — no evasion.
- Listing sources (UNCTAD, ICSID, italaw, iareporter) expose mostly bare case names/headlines.
  The LLM classifies from the title + any summary; the offline keyword fallback needs
  doctrinal text and is intentionally conservative on thin metadata.
- `iareporter` is paywalled — only homepage **headlines** are read; article bodies are never fetched.

See `HANDOFF.md` for operations, troubleshooting, and tuning.
