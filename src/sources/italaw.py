"""italaw — HTML source (homepage "Newly Posted Awards, Decisions & Materials").

Each listing row carries a "View case details" link to /cases/<id> AND a
sibling /node/<id> link whose anchor text is the real case name (same id), e.g.
/cases/9748 ("View case details") + /node/9748 ("Windstream Energy v. Canada
(II)"). We key on the /cases/<id> profile URL but take the TITLE from the
matching /node/<id> link, falling back to the row's leading text. Generic anchor
labels ("View case details", "Read more", …) are never used as a title.

NOTE: https://www.italaw.com/cases is 404 — only the homepage feed works.
The case profile is body-fetched downstream (enrich) so the classifier scores on
real content, not just the case name.

ACCESS PATH (2026-08-17). The italaw origin serves a Cloudflare managed
challenge (HTTP 403) to every non-browser client on every path, and we never
evade anti-bot, so the live path returns nothing. This source stays honest —
it returns [] on the 403 — and the pipeline's autonomous archive-recovery guard
(``src/source_recovery.py``) reads the same case pages from the Internet
Archive, which captures them within days. That guard fires for any confirmed
NOT-READ source in its registry, italaw included, and reverts to this live path
the moment the origin stops challenging us.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from urllib.parse import urljoin

from .base import (
    CandidateItem,
    Source,
    day_floor,
    fetch_html,
    parse_date,
    utcnow,
)

logger = logging.getLogger("isds.sources.italaw")

BASE_URL = "https://www.italaw.com/"

# When the origin 403s, the pipeline's archive-recovery guard reads these case
# pages from the Internet Archive (src/source_recovery.py, spec "italaw").

# Strict case-profile path: /cases/<digits> only.
CASE_RE = re.compile(r"^/cases/[0-9]+$")
# Looser path for fallback: anything under /cases/.
CASE_PREFIX_RE = re.compile(r"^/cases/")
# The case id, shared by the /cases/<id> profile link and the /node/<id> title link.
CASE_ID_RE = re.compile(r"^/cases/([0-9]+)")

# Generic link labels that are never a real case title.
GENERIC_LABELS = {
    "view case details", "view details", "case details", "details",
    "read more", "more", "view document", "view", "download",
}


def _is_generic(text: str) -> bool:
    return (text or "").strip().lower() in GENERIC_LABELS

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
            # The italaw origin serves a Cloudflare managed challenge (HTTP 403)
            # to every non-browser client on every path, though robots.txt allows
            # 'User-agent: *'. We never evade anti-bot. Instead of going dark, we
            # read the same case pages through the Internet Archive, which serves
            # them 200 and captures them within days. When the origin stops
            # challenging us, this branch is never taken and the live path resumes
            # automatically.
            logger.warning("italaw: origin challenged (403); returning [] "
                           "(the pipeline's archive-recovery guard reads these "
                           "case pages from the Internet Archive)")
            return []

        items = self._parse_primary(soup)
        if not items:
            logger.warning("italaw: primary selector yielded 0 items, using fallback strategy")
            items = self._parse_fallback(soup)

        # Filter by since when a real date is available; keep fallback-dated
        # (now) items so the pipeline can dedupe. Dates here are date-only
        # (midnight UTC), so compare against the day-floored cutoff to avoid
        # losing items stamped on the cutoff's calendar day.
        cutoff = day_floor(since)
        filtered: list[CandidateItem] = []
        for item in items:
            has_real_date = not item.metadata.get("date_inferred", False)
            if has_real_date and item.published is not None and item.published < cutoff:
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

    def _resolve_title(self, anchor, case_id: str) -> str | None:
        """Find the real case name for a /cases/<id> anchor.

        Prefers the sibling /node/<id> link's text; otherwise reads the row's
        leading text (before the generic "View case details" label). Returns None
        when nothing usable is found, so the caller can skip the row.
        """
        # Walk up to the listing row container (Drupal 'views-row').
        row = anchor
        for _ in range(6):
            row = getattr(row, "parent", None)
            if row is None:
                break
            cls = row.get("class") if hasattr(row, "get") else None
            if cls and any("views-row" in c for c in cls):
                break
        if row is None or not hasattr(row, "find_all"):
            row = None

        # 1) The /node/<id> sibling carries the clean case name.
        if row is not None:
            node = row.find("a", href=re.compile(rf"/node/{case_id}$"))
            if node is not None:
                t = node.get_text(" ", strip=True)
                if t and not _is_generic(t) and len(t) > 6:
                    return t

        # 2) Fall back to the row's leading text, minus any date and the label.
        if row is not None:
            text = row.get_text(" ", strip=True)
            text = DATE_TEXT_RE.sub("", text, count=1).strip()
            text = re.split(r"\bView case details\b", text)[0].strip(" ,;–-")
            if len(text) > 10:
                return text[:200]
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
                m = CASE_RE.match(href)
                if not m:
                    continue
                if href in seen:
                    continue
                case_id = CASE_ID_RE.match(href).group(1)
                title = self._resolve_title(anchor, case_id)
                if not title:  # no real case name found in this row — skip
                    continue
                seen.add(href)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, title, published))
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
                if href in seen:
                    continue
                text = anchor.get_text(" ", strip=True)
                idm = CASE_ID_RE.match(href)
                title = None
                if idm:
                    title = self._resolve_title(anchor, idm.group(1))
                if not title:
                    # last resort: use this anchor's own text if it is not generic
                    title = text if (len(text) > 10 and not _is_generic(text)) else None
                if not title:
                    continue
                seen.add(href)
                published = self._find_nearby_date(anchor)
                items.append(self._build_item(href, title, published))
            except Exception as exc:
                logger.warning("italaw: skipping anchor in fallback parse (%s)", exc)
                continue
        return items
