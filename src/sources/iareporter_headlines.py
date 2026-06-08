"""IAReporter — HTML source, HEADLINES ONLY (paywalled site).

Homepage: https://www.iareporter.com/
Collect <a> whose href contains '/articles/' (slug links), text length > 20.
Capture title + URL ONLY. NEVER fetch article bodies (paywall).
No date on homepage -> published = now(utc), metadata={"headline_only": True}.

PRIMARY: anchors in headline headings (h1-h4) with /articles/ href.
FALLBACK (logged): all <a href*="/articles/"> with text > 20.
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

logger = logging.getLogger("isds.sources.iareporter_headlines")

BASE_URL = "https://www.iareporter.com/"
ARTICLE_SUBSTR = "/articles/"


class IAReporterHeadlinesSource(Source):
    name = "iareporter_headlines"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        soup = fetch_html(BASE_URL)
        if soup is None:
            logger.warning("iareporter_headlines: homepage unavailable, returning []")
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning(
                "iareporter_headlines: primary selector yielded 0 items, using fallback strategy"
            )
            items = self._parse_fallback(soup)

        # No reliable date on the homepage: every item is inferred-now, so we
        # do not date-filter here; the pipeline dedupes by source_id (URL).
        logger.info("iareporter_headlines: %d headline items (since %s)", len(items), since)
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
            metadata={"headline_only": True, "date_inferred": True},
        )

    def _collect(self, anchors) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for anchor in anchors:
            try:
                href = anchor.get("href")
                if not href or ARTICLE_SUBSTR not in href:
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) <= 20:
                    continue
                url = urljoin(BASE_URL, href)
                if url in seen:
                    continue
                seen.add(url)
                items.append(self._build_item(href, text))
            except Exception as exc:
                logger.warning("iareporter_headlines: skipping anchor (%s)", exc)
                continue
        return items

    def _parse_primary(self, soup) -> list[CandidateItem]:
        anchors = []
        for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
            try:
                anchors.extend(heading.find_all("a", href=True))
            except Exception:
                continue
        return self._collect(anchors)

    def _parse_fallback(self, soup) -> list[CandidateItem]:
        return self._collect(soup.find_all("a", href=True))
