# ISDS Thematic Watcher

An automated weekly monitor for investor–State dispute settlement (ISDS) developments at
one narrow doctrinal intersection: cases where intellectual property is asserted as a
protected investment, where the disputed conduct is a regulatory or judicial measure, and
where the outcome turns on jurisdiction and admissibility. It was built as a research
instrument for the Benavides ISDS project and runs at no cost on GitHub Actions.

**Website:** https://jackemorywilliams-bit.github.io/isds-watcher/
**Methodology:** [METHODOLOGY.md](METHODOLOGY.md) · **Digest archive:** [digests/](digests/)

## What it watches

The theme was derived from three seed awards — *Philip Morris v. Australia*, *Eli Lilly v.
Canada*, and *Bridgestone v. Panama* — and expressed as the overlap of three doctrinal
"rings":

1. **IP as a protected investment** — patents, trademarks and licences, copyrights,
   geographical indications, data exclusivity, and brand value treated as a covered
   investment.
2. **A regulatory or judicial measure as the disputed conduct** — public-interest
   legislation, a domestic court judgment, or judicial conduct itself. This ring is
   weighted: a credible challenge to a court judgment reaches at least the MEDIUM band on
   its own.
3. **A jurisdictional or admissibility doctrine** — abuse of right, treaty shopping,
   foreseeability of the dispute, restructuring for treaty protection, or the contested
   definition of "investor."

A development scores HIGH (≥70) when two rings intersect, MEDIUM (40–69) when one strong
ring carries a weaker second tie or a judicial-measure case stands alone, and LOW (<40)
otherwise.

## How it works

Each run fetches new items from the sources, deduplicates them against prior runs,
pre-scores them against a keyword fingerprint, and enriches the most promising candidates
by retrieving their source pages. A language model (Claude or Gemini) then classifies the
enriched items under a few-shot prompt and returns a relevance score, the rings matched,
and a short annotation. Items at or above the threshold are written into a dated archive
folder and an annotated-bibliography email, and the website is rebuilt. Each stage is
defensive: a failing source or item is logged and skipped rather than allowed to stop the
run. With no API key the classifier falls back to the deterministic keyword scorer, so a
dry run works entirely offline. The full method, with its scholarly grounding, is in
[METHODOLOGY.md](METHODOLOGY.md).

## What you receive

Every Monday, an annotated-bibliography digest goes to the configured recipients. Each
surfaced development appears as a citation, a two-sentence descriptive-and-evaluative
annotation, a quoted notable line from the source, and the rings it matched. The same
content is committed to the repository under `digests/YYYY-MM-DD_ISDS-Thematic-Watch/`,
with one Markdown file per entry, and is published to the website.

## Configuration

Runtime configuration comes from the environment — locally through a `.env` file, and in
CI through GitHub Secrets and Variables.

| Name | Where | Purpose |
|------|-------|---------|
| `MODEL_PROVIDER` | Actions variable | `claude` (default) or `gemini` |
| `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` | Secret | classifier key, matched to the provider |
| `SMTP_HOST` · `SMTP_PORT` | Secret | `smtp.gmail.com` · `465` |
| `SMTP_USER` · `SMTP_PASS` | Secret | sending Gmail address and 16-character App Password |

Recipients are set in `src/config.py`. Model overrides: `GEMINI_MODEL` (default
`gemini-2.0-flash`), `ANTHROPIC_MODEL` (default `claude-haiku-4-5-20251001`).

## Running it

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Offline, no key, no email — uses the deterministic keyword classifier:
python -m src.main --dry-run --since 7d --no-email

# Live (language model and email); requires a .env — see .env.example:
python -m src.main --since 7d
pytest tests/          # 15 tests, no network required
```

`--since` accepts forms like `7d`, `14d`, `48h`, `1w`. The weekly workflow also accepts a
manual `since` input for wider one-off windows.

## Cost

A public repository gets unlimited GitHub Actions minutes. Claude Haiku runs about a dollar
a month; Gemini Flash is free. There are no paid data sources — the watcher reads open
feeds and pages only.

## Operations and documentation

- [METHODOLOGY.md](METHODOLOGY.md) — the research-memo write-up: theoretical frame, source
  architecture, classification cascade, calibration, validation, and the authorities
  behind each choice.
- [HANDOFF.md](HANDOFF.md) — secrets, triggering, troubleshooting, and tuning.
- [PLAN.md](PLAN.md) — the per-ring vocabulary extracted from the seed awards.

## Repository layout

```
src/            sources/ (RSS + HTML, defensive), classify.py, enrich.py,
                render.py, email_send.py, state.py, main.py, config.py
prompts/        classifier.txt (the few-shot LLM prompt)
templates/      digest.html.j2 (the annotated-bibliography email)
scripts/        build_site.py + site templates (regenerates the website)
fingerprint.yaml   the three-ring lexicon (weights sum to 100 per ring)
digests/        dated archive folders, committed each run
docs/           the generated website (served via GitHub Pages)
tests/          pytest suite
```

Two coverage notes: Google News RSS is currently disallowed by its `robots.txt` and is
therefore inactive (honored, not circumvented), and IAReporter is read at headline level
only, never the paywalled body.
