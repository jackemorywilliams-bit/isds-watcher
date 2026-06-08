"""UNCTAD ISDS Navigator — HTML source (scout got 403; degrade gracefully).

base: https://investmentpolicy.unctad.org/investment-dispute-settlement

The scout's probing context received consistent HTTP 403 (likely UA/WAF;
robots.txt also Disallows ClaudeBot specifically). We make ONE polite GET
(respecting robots for our UA) and, if it fails or yields no parseable items,
log a clear warning and return []. We NEVER evade anti-bot.

A best-effort primary + fallback parse is implemented so this works IF the
production crawler with a browser-like UA can reach the page.
"""

from __future__ import annotations

import logging
from datetime import datetime
from urllib.parse import urljoin

from .base import (
    CandidateItem,
    Source,
    fetch_html,
    utcnow,
)

logger = logging.getLogger("isds.sources.unctad_isds")

BASE_URL = "https://investmentpolicy.unctad.org/investment-dispute-settlement"
CASE_HREF_SUBSTR = "/investment-dispute-settlement/cases/"

_DROP_MSG = (
    "unctad_isds: dropped, source returned no parseable content "
    "(likely 403/anti-bot)"
)


class UNCTADISDSSource(Source):
    name = "unctad_isds"
    priority = "secondary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        soup = fetch_html(BASE_URL)
        if soup is None:
            logger.warning(_DROP_MSG)
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning("unctad_isds: primary selector yielded 0 items, using fallback strategy")
            items = self._parse_fallback(soup)

        if not items:
            logger.warning(_DROP_MSG)
            return []

        logger.info("unctad_isds: %d items (since %s)", len(items), since)
        return items

    def _build_item(self, href: str, title: str) -> CandidateItem:
        url = urljoin(BASE_URL, href)
        return CandidateItem(
            source=self.name,
            source_id=url,
            url=url,
            title=title,
            published=utcnow(),
            summary="",
            raw_text=title,
            metadata={"date_inferred": True},
        )

    def _collect(self, anchors, min_len: int) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for anchor in anchors:
            try:
                href = anchor.get("href")
                if not href or CASE_HREF_SUBSTR not in href:
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) < min_len:
                    continue
                url = urljoin(BASE_URL, href)
                if url in seen:
                    continue
                seen.add(url)
                items.append(self._build_item(href, text))
            except Exception as exc:
                logger.warning("unctad_isds: skipping anchor (%s)", exc)
                continue
        return items

    def _parse_primary(self, soup) -> list[CandidateItem]:
        # Primary: case links with a reasonably substantial title.
        return self._collect(soup.find_all("a", href=True), min_len=10)

    def _parse_fallback(self, soup) -> list[CandidateItem]:
        # Fallback: looser threshold, same structural href rule.
        return self._collect(soup.find_all("a", href=True), min_len=3)
