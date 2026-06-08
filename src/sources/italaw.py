"""italaw — HTML source (homepage "Newly Posted Awards, Decisions & Materials").

PRIMARY: homepage <a> whose href matches ^/cases/[0-9]+$, anchor text > 15,
dedupe by href, read an adjacent date heading (e.g. '2 Jun 2026') for published.
FALLBACK (logged): all <a href^="/cases/"> with text length > 10.

NOTE: https://www.italaw.com/cases is 404 — only the homepage feed works.
No body fetch on the listing; raw_text = title.
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

logger = logging.getLogger("isds.sources.italaw")

BASE_URL = "https://www.italaw.com/"

# Strict case-profile path: /cases/<digits> only.
CASE_RE = re.compile(r"^/cases/[0-9]+$")
# Looser path for fallback: anything under /cases/.
CASE_PREFIX_RE = re.compile(r"^/cases/")

# Date-ish heading like "2 Jun 2026" or "12 December 2025".
DATE_TEXT_RE = re.compile(
    r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b",
    re.IGNORECASE,
)


class ItalawSource(Source):
    name = "italaw"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        soup = fetch_html(BASE_URL)
        if soup is None:
            logger.warning("italaw: homepage unavailable, returning []")
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning("italaw: primary selector yielded 0 items, using fallback strategy")
            items = self._parse_fallback(soup)

        # Filter by since when a real date is available; keep fallback-dated
        # (now) items so the pipeline can dedupe.
        filtered: list[CandidateItem] = []
        for item in items:
            has_real_date = not item.metadata.get("date_inferred", False)
            if has_real_date and item.published is not None and item.published < since:
                continue
            filtered.append(item)

        logger.info("italaw: %d items (since %s)", len(filtered), since)
        return filtered

    def _find_nearby_date(self, anchor) -> "datetime | None":
        """Look at the anchor's ancestors / preceding siblings for a date heading."""
        try:
            # 1) Check text within a couple of ancestor containers.
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
            # 2) Check preceding elements for a standalone date heading.
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
            logger.debug("italaw: date lookup failed (%s)", exc)
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
        for anchor in soup.find_all("a", href=True):
            try:
                href = anchor["href"]
                if not CASE_RE.match(href):
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) <= 15:
                    continue
                if href in seen:
                    continue
                seen.add(href)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, text, published))
            except Exception as exc:
                logger.warning("italaw: skipping anchor in primary parse (%s)", exc)
                continue
        return items

    def _parse_fallback(self, soup) -> list[CandidateItem]:
        items: list[CandidateItem] = []
        seen: set[str] = set()
        for anchor in soup.find_all("a", href=True):
            try:
                href = anchor["href"]
                if not CASE_PREFIX_RE.match(href):
                    continue
                text = anchor.get_text(" ", strip=True)
                if len(text) <= 10:
                    continue
                if href in seen:
                    continue
                seen.add(href)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, text, published))
            except Exception as exc:
                logger.warning("italaw: skipping anchor in fallback parse (%s)", exc)
                continue
        return items
