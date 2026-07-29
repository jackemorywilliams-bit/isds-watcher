"""General-press business desks that still permit identified crawlers — RSS sources.

Added 2026-07-29 after the operator surfaced Press Gazette's AI-crawler survey:
most named outlets are irrelevant or (like Politico, now Cloudflare-walled)
inaccessible, but the Independent and Evening Standard business feeds were
LIVE-VERIFIED to serve valid, fresh RSS to this project's identified UA, and
both desks have carried ISDS-adjacent stories (the Nexperia/Wingtech class).
These are broad business feeds by design: the deterministic scorer and the
digest quality bar do the relevance filtering — that is the architecture.
"""

from __future__ import annotations

import logging
from datetime import datetime

from .base import CandidateItem, Source, fetch_rss, parse_date, strip_html

logger = logging.getLogger("isds.sources.press_business")


class _RSSBusinessSource(Source):
    """Shared implementation: plain RSS feed, entries filtered by ``since``."""

    feed_url: str = ""
    priority = "secondary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        feed = fetch_rss(self.feed_url)
        if feed is None:
            logger.warning("%s: feed unavailable, returning []", self.name)
            return []
        items: list[CandidateItem] = []
        for entry in getattr(feed, "entries", []) or []:
            try:
                item = self._to_item(entry)
            except Exception as exc:  # noqa: BLE001 - one bad entry never kills the source
                logger.warning("%s: skipping unparseable entry (%s)", self.name, exc)
                continue
            if item is None:
                continue
            if item.published is not None and item.published < since:
                continue
            items.append(item)
        logger.info("%s: %d items after filtering since %s", self.name, len(items), since)
        return items

    def _to_item(self, entry) -> CandidateItem | None:
        link = getattr(entry, "link", None)
        if not link:
            return None
        title = (getattr(entry, "title", "") or "").strip()
        published = parse_date(
            getattr(entry, "published", None)
            or getattr(entry, "updated", None)
            or getattr(entry, "pubDate", None))
        summary_html = getattr(entry, "summary", "") or ""
        summary = strip_html(summary_html)
        return CandidateItem(
            source=self.name,
            source_id=link,
            url=link,
            title=title,
            published=published,
            summary=summary,
            raw_text=summary,
            metadata={},
        )


class IndependentBusinessSource(_RSSBusinessSource):
    name = "independent_business"
    feed_url = "https://www.independent.co.uk/news/business/rss"


class StandardBusinessSource(_RSSBusinessSource):
    name = "standard_business"
    feed_url = "https://www.standard.co.uk/business/rss"
