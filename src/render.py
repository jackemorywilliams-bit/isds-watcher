"""Render classified items into an annotated-bibliography HTML digest, and write
a dated, browsable archive folder (one Markdown file per surfaced article)."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

logger = logging.getLogger("isds.render")

FOLDER_SUFFIX = "ISDS-Thematic-Watch"

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
                  folder_url: str | None = None) -> str:
    """Render the annotated-bibliography digest (used as the email body)."""
    tmpl = _env.get_template("digest.html.j2")
    return tmpl.render(
        items=items,
        generated_at=generated_at,
        since=since,
        stats=stats,
        repo_url=config.REPO_URL,
        site_url=config.SITE_URL,
        theme=config.THEME_ONE_LINER,
        date_str=generated_at.strftime("%Y-%m-%d"),
        folder_url=folder_url,
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
        f"- **Source:** {it.source.replace('_', ' ').title()} — [Read the original ↗]({it.url})",
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
    if quote:
        lines += ["", "## Notable line (from source)", f"> “{quote}”"]
    lines += ["", "---", f"Source: {it.source.replace('_', ' ').title()}. Methodology: METHODOLOGY.md"]
    return "\n".join(lines) + "\n"


def write_digest_folder(html: str, items, generated_at: datetime, stats: dict,
                        out_root: str = "digests") -> str:
    """Write digests/<DATE>_ISDS-Thematic-Watch/ with the digest, a README index,
    and one Markdown file per surfaced article. Returns the folder path."""
    date_str = generated_at.strftime("%Y-%m-%d")
    folder = os.path.join(out_root, folder_name(date_str))
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

    # Per-digest machine-readable summary.
    screened = stats.get("total_candidates", 0)
    accepted = stats.get("above_threshold", 0)
    surfaced = len(items)
    threshold = stats.get("threshold")
    meta = {
        "date": date_str,
        "screened": screened,
        "accepted": accepted,
        "surfaced": surfaced,
    }
    with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")

    # README index — browsable on GitHub.
    rd = [
        f"# ISDS Thematic Watch — {date_str}",
        "",
        f"**Accepted (≥ threshold {threshold}): {accepted} · "
        f"Screened: {screened} · Surfaced incl. watch-list: {surfaced}**",
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
        ttl = it.title.replace("|", "\\|")
        rd.append(f"| {i} | {it.relevance_score} | {it.source.replace('_',' ')} "
                  f"| [{ttl}](articles/{fn}) | {q} |")
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


def write_digest(html: str, date_str: str, out_dir: str = "digests") -> str:
    """Also write a flat digests/<DATE>.html for quick access / backward-compat."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{date_str}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path
