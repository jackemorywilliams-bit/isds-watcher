"""Bing News keyword search — RSS source (council-approved alerts lane, 2026-07-29).

Replaces the retired Google News channel. Bing's robots.txt permits generic
agents on /news/search (live-verified), and each fingerprint-derived query below
returns a valid RSS result set to this project's identified UA. Queries mirror
the live research question (trade secrets / clinical data as investments; the
jurisdictional gate; the standing case dockets). Results are relevance-sorted
and can be old — the ``since`` filter and seen-state dedup handle that.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from urllib.parse import quote_plus

from .base import CandidateItem, Source, fetch_rss, parse_date, strip_html

logger = logging.getLogger("isds.sources.bing_news")

# One polite request per query per run, 3s apart (site-wide courtesy delay).
QUERIES = [
    '"investor-state" "trade secret"',
    '"investor-state" "clinical trial data"',
    '"data exclusivity" China pharmaceutical',
    'ICSID arbitration intellectual property',
    'Wingtech OR Nexperia arbitration Netherlands',
    'Einarsson Canada arbitration',
    '"Hela Schwarz" China',
    'UNCITRAL ISDS reform',
]
_REQUEST_GAP_S = 3.0


class BingNewsSource(Source):
    name = "bing_news"
    priority = "secondary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen_links: set[str] = set()
        for i, q in enumerate(QUERIES):
            if i:
                time.sleep(_REQUEST_GAP_S)
            url = f"https://www.bing.com/news/search?q={quote_plus(q)}&format=rss"
            feed = fetch_rss(url)
            if feed is None:
                logger.warning("bing_news: feed unavailable for query %r", q)
                continue
            for entry in getattr(feed, "entries", []) or []:
                try:
                    item = self._to_item(entry, q)
                except Exception as exc:  # noqa: BLE001 - one entry never kills the source
                    logger.warning("bing_news: skipping unparseable entry (%s)", exc)
                    continue
                if item is None or item.source_id in seen_links:
                    continue
                if item.published is not None and item.published < since:
                    continue
                seen_links.add(item.source_id)
                items.append(item)
        logger.info("bing_news: %d items across %d queries since %s",
                    len(items), len(QUERIES), since)
        return items

    def _to_item(self, entry, query: str) -> CandidateItem | None:
        link = getattr(entry, "link", None)
        if not link:
            return None
        title = (getattr(entry, "title", "") or "").strip()
        published = parse_date(
            getattr(entry, "published", None) or getattr(entry, "updated", None))
        summary = strip_html(getattr(entry, "summary", "") or "")
        return CandidateItem(
            source=self.name,
            source_id=link,
            url=link,
            title=title,
            published=published,
            summary=summary,
            raw_text=summary,
            metadata={"query": query},
        )
