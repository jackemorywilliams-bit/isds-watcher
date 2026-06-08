"""ICSID — HTML source (news-events page; static HTML).

base: https://icsid.worldbank.org/news-events  (NOT /news-and-events which 404s)
PRIMARY: 'h3 a' items with an adjacent date 'MMMM DD, YYYY' (e.g. 'March 06, 2026').
FALLBACK (logged): all <a> with href containing '/news-and-events/' and text > 20.

The case database (/cases/case-database) is JS-rendered and unusable with a
plain GET; this source covers the static news page only.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from urllib.parse import urljoin

from .base import (
    CandidateItem,
    Source,
    fetch_html,
    parse_date,
    utcnow,
)

logger = logging.getLogger("isds.sources.icsid")

BASE_URL = "https://icsid.worldbank.org/news-events"

# 'March 06, 2026' style date.
DATE_TEXT_RE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b",
    re.IGNORECASE,
)

NEWS_HREF_SUBSTR = "/news-and-events/"


class ICSIDSource(Source):
    name = "icsid"
    priority = "secondary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        soup = fetch_html(BASE_URL)
        if soup is None:
            logger.warning("icsid: news-events page unavailable, returning []")
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning("icsid: primary selector yielded 0 items, using fallback strategy")
            items = self._parse_fallback(soup)

        filtered: list[CandidateItem] = []
        for item in items:
            has_real_date = not item.metadata.get("date_inferred", False)
            if has_real_date and item.published is not None and item.published < since:
                continue
            filtered.append(item)

        logger.info("icsid: %d items (since %s)", len(filtered), since)
        return filtered

    def _find_nearby_date(self, anchor) -> "datetime | None":
        try:
            node = anchor
            for _ in range(4):
                node = getattr(node, "parent", None)
                if node is None:
                    break
                text = node.get_text(" ", strip=True) if hasattr(node, "get_text") else ""
                m = DATE_TEXT_RE.search(text or "")
                if m:
                    dt = parse_date(m.group(0))
                    if dt is not None:
                        return dt
            prev = anchor
            for _ in range(6):
                prev = getattr(prev, "find_previous", lambda *a, **k: None)(True)
                if prev is None:
                    break
                ptext = prev.get_text(" ", strip=True) if hasattr(prev, "get_text") else ""
                m = DATE_TEXT_RE.search(ptext or "")
                if m:
                    dt = parse_date(m.group(0))
                    if dt is not None:
                        return dt
        except Exception as exc:
            logger.debug("icsid: date lookup failed (%s)", exc)
        return None

    def _build_item(self, href: str, title: str, published) -> CandidateItem:
        url = urljoin(BASE_URL, href)
        metadata: dict = {}
        if published is None:
            published = utcnow()
            metadata["date_inferred"] = True
        return CandidateItem(
            source=self.name,
            source_id=url,
            url=url,
            title=title,
            published=published,
            summary="",
            raw_text=title,
            metadata=metadata,
        )

    def _parse_primary(self, soup) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for h3 in soup.find_all("h3"):
            try:
                anchor = h3.find("a", href=True)
                if anchor is None:
                    continue
                href = anchor["href"]
                text = anchor.get_text(" ", strip=True)
                if not text:
                    continue
                url = urljoin(BASE_URL, href)
                if url in seen:
                    continue
                seen.add(url)
                published = self._find_nearby_date(h3)
                items.append(self._build_item(href, text, published))
            except Exception as exc:
                logger.warning("icsid: skipping h3 in primary parse (%s)", exc)
                continue
        return items

    def _parse_fallback(self, soup) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for anchor in soup.find_all("a", href=True):
            try:
                href = anchor["href"]
                if NEWS_HREF_SUBSTR not in href:
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) <= 20:
                    continue
                url = urljoin(BASE_URL, href)
                if url in seen:
                    continue
                seen.add(url)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, text, published))
            except Exception as exc:
                logger.warning("icsid: skipping anchor in fallback parse (%s)", exc)
                continue
        return items
