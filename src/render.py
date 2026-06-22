"""Render classified items into an annotated-bibliography HTML digest, and write
a dated, browsable archive folder (one Markdown file per surfaced article)."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

logger = logging.getLogger("isds.render")

FOLDER_SUFFIX = "ISDS-Thematic-Watch"

# Sources that aggregate third-party publishers rather than being the publisher
# themselves. For these, the archive names the underlying publisher (parsed from
# the item URL) alongside the channel, so provenance reads e.g.
# "Google Alerts → reuters.com" rather than a bare "Google Alerts".
_AGGREGATOR_SOURCES = {"google_alerts", "google_news_rss", "gmail_scholar"}


def _source_label(it) -> str:
    """Human-readable provenance: the source channel, plus the underlying
    publisher domain when the channel is an aggregator."""
    channel = it.source.replace("_", " ").title()
    if it.source in _AGGREGATOR_SOURCES and getattr(it, "url", ""):
        host = urlparse(it.url).netloc.replace("www.", "")
        if host:
            return f"{channel} → {host}"
    return channel

_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml", "j2"]),
)


def _slug(text: str, n: int = 52) -> str:
    """Clean, readable, word-boundary slug — never truncates mid-word."""
    s = re.sub(r"[^a-z0-9]+", "-", (text or "item").lower()).strip("-")
    if len(s) <= n:
        return s or "item"
    cut = s[:n]
    if "-" in cut:
        cut = cut.rsplit("-", 1)[0]  # back off to the last whole word
    return cut.strip("-") or "item"


def folder_name(date_str: str) -> str:
    return f"{date_str}_{FOLDER_SUFFIX}"


def render_digest(items, generated_at: datetime, since: datetime, stats: dict,
                  folder_url: str | None = None, lede: str | None = None,
                  cumulative_runs: int | None = None) -> str:
    """Render the annotated-bibliography digest (used as the email body).

    ``lede`` overrides the default one-line summary paragraph when provided.

    ``cumulative_runs`` marks the digest as a *cumulative* artifact pooled across
    that many runs (the aggregate bring-up digest), rather than a single run. When
    set, the masthead and footer counts are relabeled ("cumulative", "collected",
    "distinct findings") so a reader never reads a cumulative "Screened: 251"
    as the same thing as the website's per-run "Screened: 80". Per-run digests
    leave it None and read exactly as before.
    """
    tmpl = _env.get_template("digest.html.j2")
    # Single source of truth for the count split, shared with meta.json:
    # matches score >= threshold; watch-list leads are the rest of the shown set.
    matches = sum(1 for it in items
                  if getattr(it, "relevance_score", 0) >= stats.get("threshold", 40))
    leads = len(items) - matches
    return tmpl.render(
        items=items,
        generated_at=generated_at,
        since=since,
        stats=stats,
        matches=matches,
        leads=leads,
        repo_url=config.REPO_URL,
        site_url=config.SITE_URL,
        theme=config.THEME_ONE_LINER,
        date_str=generated_at.strftime("%Y-%m-%d"),
        folder_url=folder_url,
        lede=lede,
        cumulative_runs=cumulative_runs,
    )


def _citation(it) -> str:
    src = it.source.replace("_", " ")
    date = it.published.strftime("%d %b %Y") if getattr(it, "published", None) else "n.d."
    return f'{src}. "{it.title}." {date}. {it.url}'


def _article_md(it, idx: int) -> str:
    band = "HIGH" if it.relevance_score >= 70 else "MEDIUM" if it.relevance_score >= 40 else "WATCH"
    rings = ", ".join(it.matched_rings) if it.matched_rings else "—"
    tags = [t for t in it.thematic_tags if t != "keyword_fallback"]
    quote = it.metadata.get("notable_quote", "") if isinstance(it.metadata, dict) else ""
    lines = [
        f"# {idx}. {it.title}",
        "",
        f"- **Source:** {_source_label(it)} — [Read the original ↗]({it.url})",
        f"- **Date:** {it.published.strftime('%d %B %Y') if getattr(it, 'published', None) else 'n.d.'}",
        f"- **Link:** {it.url}",
        f"- **Relevance:** {it.relevance_score} ({band})",
        f"- **Rings matched:** {rings}",
        f"- **Tags:** {', '.join(tags) if tags else '—'}",
        "",
        "## Citation",
        f"> {_citation(it)}",
        "",
        "## Annotation",
        it.digest_summary or "(no annotation)",
    ]
    unavailable = it.metadata.get("notable_unavailable") if isinstance(it.metadata, dict) else False
    if quote:
        lines += ["", "## Notable line (from source)", f"> “{quote}”"]
    elif unavailable:
        lines += ["", "## Notable line (from source)",
                  "> N/A — source paywalled (headline only); body not accessible."]
    lines += ["", "---", f"Source: {_source_label(it)}. Methodology: METHODOLOGY.md"]
    return "\n".join(lines) + "\n"


def write_digest_folder(html: str, items, generated_at: datetime, stats: dict,
                        out_root: str = "digests") -> str:
    """Write digests/<DATE>_ISDS-Thematic-Watch/ with the digest, a README index,
    and one Markdown file per surfaced article. Returns the folder path."""
    date_str = generated_at.strftime("%Y-%m-%d")
    folder = os.path.join(out_root, folder_name(date_str))

    # Run identity is keyed by date: one date maps to exactly one record, and a
    # re-run OVERWRITES that date's record. One guarded exception: an *empty*
    # re-run (nothing screened, nothing surfaced — typically a same-day dispatch
    # where every candidate is already deduped against state) must not silently
    # destroy a substantive run already recorded for that date. If a populated
    # record exists and this run produced nothing, preserve the existing record.
    new_screened = stats.get("total_candidates", 0)
    new_accepted = len(items)
    prior_meta = os.path.join(folder, "meta.json")
    if new_screened == 0 and new_accepted == 0 and os.path.exists(prior_meta):
        try:
            with open(prior_meta, encoding="utf-8") as fh:
                prev = json.load(fh)
            if (prev.get("screened") or 0) > 0 or (prev.get("accepted") or 0) > 0:
                print(f"  ! {date_str}: empty re-run; preserving existing record "
                      f"({prev.get('screened')} screened, {prev.get('accepted')} "
                      f"accepted) rather than overwriting it.")
                return folder
        except (ValueError, OSError):
            pass  # unreadable prior record: fall through and write the new one

    arts = os.path.join(folder, "articles")
    # Clear any prior run's article files so stale, differently-slugged entries
    # never accumulate in the same dated folder.
    if os.path.isdir(arts):
        for old in os.listdir(arts):
            if old.endswith(".md"):
                os.remove(os.path.join(arts, old))
    os.makedirs(arts, exist_ok=True)

    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    # Per-digest machine-readable summary — the single source of truth for run
    # counts, read by the email footer and the website. Definitions:
    #   screened = candidates fetched and scored this run (after dedupe)
    #   matches  = items scoring >= threshold
    #   watch_list_leads = sub-threshold items surfaced to meet the minimum floor
    #   accepted = matches + watch_list_leads actually shown in the digest
    screened = stats.get("total_candidates", 0)
    matches = stats.get("above_threshold", 0)
    accepted = len(items)
    watch_list_leads = accepted - matches
    threshold = stats.get("threshold")
    meta = {
        "date": date_str,
        "screened": screened,
        "matches": matches,
        "watch_list_leads": watch_list_leads,
        "accepted": accepted,
    }
    with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")

    # README index — browsable on GitHub.
    rd = [
        f"# ISDS Thematic Watch — {date_str}",
        "",
        f"**Screened: {screened} · Matches (≥{threshold}): {matches} · "
        f"Watch-list leads: {watch_list_leads} · Accepted (shown): {accepted}**",
        "",
        f"Annotated digest of **{len(items)}** surfaced item"
        f"{'' if len(items) == 1 else 's'} "
        f"(screened from {stats.get('total_candidates', 0)} candidates; "
        f"classifier: {stats.get('provider') or 'keyword-fallback'}; "
        f"threshold {stats.get('threshold')}).",
        "",
        "Open `index.html` for the formatted digest, or browse `articles/` for one"
        " file per entry.",
        "",
        "| # | Relevance | Source | Article | Notable line |",
        "|---|-----------|--------|---------|--------------|",
    ]
    files = []
    for i, it in enumerate(items, 1):
        fn = f"{i:02d}_{_slug(it.title)}.md"
        files.append((i, it, fn))
        quote = it.metadata.get("notable_quote", "") if isinstance(it.metadata, dict) else ""
        q = (quote[:80] + "…") if len(quote) > 80 else quote
        q = q.replace("|", "\\|")
        # The notable line is a direct, verbatim quote from the source, so it is
        # always shown in quotation marks (matching the newsletter and the
        # per-article files). A paywalled/headline-only source has no quotable
        # body, so it shows "N/A"; an accessible source with no salient line
        # shows an em dash.
        unavail = it.metadata.get("notable_unavailable") if isinstance(it.metadata, dict) else False
        q_disp = f"“{q}”" if q else ("N/A" if unavail else "—")
        ttl = it.title.replace("|", "\\|")
        src = _source_label(it).replace("|", "\\|")
        rd.append(f"| {i} | {it.relevance_score} | {src} "
                  f"| [{ttl}](articles/{fn}) | {q_disp} |")
    if not items:
        rd.append("| — | — | — | _No items met the relevance floor this cycle._ | — |")
    rd += ["", "---", "_See [/METHODOLOGY.md](../../METHODOLOGY.md) for the workflow and its"
           " scholarly justification._"]
    with open(os.path.join(folder, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rd) + "\n")

    for i, it, fn in files:
        with open(os.path.join(arts, fn), "w", encoding="utf-8") as fh:
            fh.write(_article_md(it, i))

    logger.info("render: wrote folder %s (%d articles)", folder, len(files))
    return folder


def update_digests_index(out_root: str = "digests") -> str:
    """Rewrite digests/README.md as a navigable index of every dated digest."""
    folders = []
    if os.path.isdir(out_root):
        for name in sorted(os.listdir(out_root), reverse=True):
            full = os.path.join(out_root, name)
            if os.path.isdir(full) and name.endswith(FOLDER_SUFFIX):
                date = name.split("_")[0]
                n = 0
                arts = os.path.join(full, "articles")
                if os.path.isdir(arts):
                    n = len([f for f in os.listdir(arts) if f.endswith(".md")])
                folders.append((date, name, n))
    lines = [
        "# ISDS Thematic Watch — Digest Archive",
        "",
        "Each weekly run is archived below, newest first. Open a date to read the formatted",
        "digest (`index.html`) or browse `articles/` for one annotated entry per development.",
        "",
        "| Date | Digest | Entries |",
        "|------|--------|---------|",
    ]
    for date, name, n in folders:
        lines.append(f"| {date} | [{name}](./{name}/) · "
                     f"[README](./{name}/README.md) | {n} |")
    if not folders:
        lines.append("| — | _No digests yet._ | — |")
    lines += ["", "_See [/METHODOLOGY.md](../METHODOLOGY.md) for how entries are selected and scored._"]
    path = os.path.join(out_root, "README.md")
    os.makedirs(out_root, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def render_research_brief(brief: dict, generated_at: datetime, seq: int) -> str:
    """Render the interpretive Research Brief (the council's second weekly email)."""
    tmpl = _env.get_template("research_brief.html.j2")
    return tmpl.render(
        brief=brief,
        seq=seq,
        generated_at=generated_at,
        date_str=generated_at.strftime("%Y-%m-%d"),
        repo_url=config.REPO_URL,
        site_url=config.SITE_URL,
    )


def write_brief(html: str, brief: dict, generated_at: datetime, seq: int,
                out_root: str = "briefs") -> str:
    """Write briefs/<DATE>.html, the analyst memo, and refresh briefs/README.md."""
    os.makedirs(out_root, exist_ok=True)
    date_str = generated_at.strftime("%Y-%m-%d")
    path = os.path.join(out_root, f"{date_str}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    # Preserve the council's raw deliberation alongside the edited issue (audit trail):
    # the chairman's agenda, the analyst memo, and the security officer's vetting note.
    memo = brief.get("_memo")
    if memo:
        parts = [f"# ISDS Research Brief #{seq} — {date_str}", "", f"## {brief.get('headline','')}", ""]
        if brief.get("_agenda"):
            parts += ["## Chairman's agenda", "", brief["_agenda"], ""]
        parts += ["## Analyst memo (raw)", "", memo, ""]
        if brief.get("_security"):
            parts += ["## Security officer's vetting note", "", brief["_security"], ""]
        with open(os.path.join(out_root, f"{date_str}-memo.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(parts) + "\n")
    _update_briefs_index(out_root)
    return path


def _update_briefs_index(out_root: str = "briefs") -> None:
    issues = sorted(
        (f for f in os.listdir(out_root)
         if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.html", f)),
        reverse=True,
    ) if os.path.isdir(out_root) else []
    lines = [
        "# ISDS Research Brief — Archive",
        "",
        "The interpretive companion to the Thematic Watch: each weekly issue reads the",
        "developments against the research question and carries open threads forward.",
        "",
        "| Date | Issue |",
        "|------|-------|",
    ]
    for f in issues:
        d = f[:-5]
        lines.append(f"| {d} | [{d}.html](./{f}) · [memo](./{d}-memo.md) |")
    if not issues:
        lines.append("| — | _No issues yet._ |")
    with open(os.path.join(out_root, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def write_digest(html: str, date_str: str, out_dir: str = "digests") -> str:
    """Also write a flat digests/<DATE>.html for quick access / backward-compat."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{date_str}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path
