"""Google News RSS search feeds — fingerprint-derived queries.

8 hard-coded query feeds from specs/google_news_rss.yaml. Feeds include
historical items, so filtering by ``since`` is important. entry.link is a
Google redirect URL; dedupe by guid/id within the source.
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

logger = logging.getLogger("isds.sources.google_news_rss")

# (query_label, feed_url) — labels mirror the encoded query for traceability.
FEEDS: list[tuple[str, str]] = [
    (
        '"abuse of right" investment arbitration',
        "https://news.google.com/rss/search?q=%22abuse%20of%20right%22%20investment%20arbitration&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        '"denial of justice" ICSID',
        "https://news.google.com/rss/search?q=%22denial%20of%20justice%22%20ICSID&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        '"promise utility doctrine"',
        "https://news.google.com/rss/search?q=%22promise%20utility%20doctrine%22&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        "patent ISDS",
        "https://news.google.com/rss/search?q=patent%20ISDS&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        "trademark BIT arbitration",
        "https://news.google.com/rss/search?q=trademark%20BIT%20arbitration&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        '"reasonably foreseeable" treaty arbitration',
        "https://news.google.com/rss/search?q=%22reasonably%20foreseeable%22%20treaty%20arbitration&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        '"manifest arbitrariness" investment tribunal',
        "https://news.google.com/rss/search?q=%22manifest%20arbitrariness%22%20investment%20tribunal&hl=en-US&gl=US&ceid=US:en",
    ),
    (
        "plain packaging investment arbitration",
        "https://news.google.com/rss/search?q=plain%20packaging%20investment%20arbitration&hl=en-US&gl=US&ceid=US:en",
    ),
]


class GoogleNewsRSSSource(Source):
    name = "google_news_rss"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()  # dedupe by source_id (guid/id) within source

        for query_label, url in FEEDS:
            feed = fetch_rss(url)
            if feed is None:
                logger.warning("google_news_rss: feed unavailable for query %r", query_label)
                continue
            entries = getattr(feed, "entries", []) or []
            for entry in entries:
                try:
                    item = self._to_item(entry, query_label)
                except Exception as exc:
                    logger.warning(
                        "google_news_rss: skipping unparseable entry for %r (%s)",
                        query_label,
                        exc,
                    )
                    continue
                if item is None:
                    continue
                if item.source_id in seen:
                    continue
                # Filter by since — these feeds include old items.
                if item.published is not None and item.published < since:
                    continue
                seen.add(item.source_id)
                items.append(item)

        logger.info("google_news_rss: %d unique items after filtering since %s", len(items), since)
        return items

    def _to_item(self, entry, query_label: str) -> "CandidateItem | None":
        link = getattr(entry, "link", None)
        guid = getattr(entry, "id", None)
        source_id = guid or link
        if not source_id:
            return None

        title = (getattr(entry, "title", "") or "").strip()
        published = parse_date(
            getattr(entry, "published", None) or getattr(entry, "updated", None)
        )
        summary_html = getattr(entry, "summary", "") or ""
        summary = strip_html(summary_html)

        return CandidateItem(
            source=self.name,
            source_id=source_id,
            url=link or source_id,
            title=title,
            published=published,
            summary=summary,
            raw_text=summary or title,
            metadata={"query": query_label},
        )
