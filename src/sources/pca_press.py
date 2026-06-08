"""PCA (Permanent Court of Arbitration) press/news — HTML source, LOW priority.

base: https://pca-cpa.org/en/news/

The scout's probing context received HTTP 403 (likely UA/WAF). We make ONE
polite GET (respecting robots for our UA); on failure or no parseable items we
log "pca_press: dropped" and return []. We NEVER evade anti-bot.

A best-effort primary + fallback parse is implemented so this works IF the
production crawler with a browser-like UA can reach the page.
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

logger = logging.getLogger("isds.sources.pca_press")

BASE_URL = "https://pca-cpa.org/en/news/"
# News article links typically live under /en/news/<slug> or /en/cases/<slug>.
NEWS_HREF_RE = re.compile(r"/en/(?:news|cases)/", re.IGNORECASE)

DATE_TEXT_RE = re.compile(
    r"\b(?:\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}"
    r"|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})\b",
    re.IGNORECASE,
)

_DROP_MSG = "pca_press: dropped, source returned no parseable content (likely 403/anti-bot)"


class PCAPressSource(Source):
    name = "pca_press"
    priority = "low"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        soup = fetch_html(BASE_URL)
        if soup is None:
            logger.warning(_DROP_MSG)
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning("pca_press: primary selector yielded 0 items, using fallback strategy")
            items = self._parse_fallback(soup)

        if not items:
            logger.warning(_DROP_MSG)
            return []

        filtered: list[CandidateItem] = []
        for item in items:
            has_real_date = not item.metadata.get("date_inferred", False)
            if has_real_date and item.published is not None and item.published < since:
                continue
            filtered.append(item)

        logger.info("pca_press: %d items (since %s)", len(filtered), since)
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
        except Exception as exc:
            logger.debug("pca_press: date lookup failed (%s)", exc)
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

    def _collect(self, anchors, min_len: int) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for anchor in anchors:
            try:
                href = anchor.get("href")
                if not href or not NEWS_HREF_RE.search(href):
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) < min_len:
                    continue
                url = urljoin(BASE_URL, href)
                if url in seen:
                    continue
                seen.add(url)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, text, published))
            except Exception as exc:
                logger.warning("pca_press: skipping anchor (%s)", exc)
                continue
        return items

    def _parse_primary(self, soup) -> list[CandidateItem]:
        return self._collect(soup.find_all("a", href=True), min_len=15)

    def _parse_fallback(self, soup) -> list[CandidateItem]:
        return self._collect(soup.find_all("a", href=True), min_len=8)
