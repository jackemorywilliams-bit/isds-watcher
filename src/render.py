"""Render classified items into an email-friendly HTML digest."""

from __future__ import annotations

import logging
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

logger = logging.getLogger("isds.render")

_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml", "j2"]),
)


def render_digest(items, generated_at: datetime, since: datetime, stats: dict) -> str:
    """Render items (already filtered >= threshold, sorted desc) to HTML."""
    high = [i for i in items if i.relevance_score >= 70]
    medium = [i for i in items if 40 <= i.relevance_score < 70]
    tmpl = _env.get_template("digest.html.j2")
    return tmpl.render(
        high=high,
        medium=medium,
        items=items,
        generated_at=generated_at,
        since=since,
        stats=stats,
        repo_url=config.REPO_URL,
        theme=config.THEME_ONE_LINER,
        date_str=generated_at.strftime("%Y-%m-%d"),
    )


def write_digest(html: str, date_str: str, out_dir: str = "digests") -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{date_str}.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    logger.info("render: wrote %s", path)
    return path
