"""IISD Investment Treaty News (ITN) — RSS source.

Feed: https://www.iisd.org/itn/feed/  (use this, NOT /itn/en/feed/ which 403s)
Valid RSS 2.0 with substantive descriptions. Article/newsletter-level.
"""

from __future__ import annotations

import logging
from datetime import datetime

from .base import (
    CandidateItem,
    Source,
    fetch_rss,
    parse_date,
    strip_html,
)

logger = logging.getLogger("isds.sources.iisd_itn")

FEED_URL = "https://www.iisd.org/itn/feed/"


class IISDITNSource(Source):
    name = "iisd_itn"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        feed = fetch_rss(FEED_URL)
        if feed is None:
            logger.warning("iisd_itn: feed unavailable, returning []")
            return []

        entries = getattr(feed, "entries", []) or []
        for entry in entries:
            try:
                item = self._to_item(entry)
            except Exception as exc:  # one bad entry must not kill the source
                logger.warning("iisd_itn: skipping unparseable entry (%s)", exc)
                continue
            if item is None:
                continue
            # Filter by since when a date is available; include otherwise.
            if item.published is not None and item.published < since:
                continue
            items.append(item)

        logger.info("iisd_itn: %d items after filtering since %s", len(items), since)
        return items

    def _to_item(self, entry) -> "CandidateItem | None":
        link = getattr(entry, "link", None)
        if not link:
            return None
        title = (getattr(entry, "title", "") or "").strip()

        published_raw = (
            getattr(entry, "published", None)
            or getattr(entry, "updated", None)
            or getattr(entry, "pubDate", None)
        )
        published = parse_date(published_raw)

        summary_html = getattr(entry, "summary", "") or ""
        # Prefer content body when present for raw_text.
        content = getattr(entry, "content", None)
        if content:
            try:
                content_html = content[0].get("value", "")
            except (IndexError, AttributeError, TypeError):
                content_html = ""
        else:
            content_html = ""

        summary = strip_html(summary_html)
        raw_text = strip_html(content_html or summary_html)

        return CandidateItem(
            source=self.name,
            source_id=link,
            url=link,
            title=title,
            published=published,
            summary=summary,
            raw_text=raw_text,
            metadata={},
        )
