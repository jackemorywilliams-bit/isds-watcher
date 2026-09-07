"""IISD Investment Treaty News (ITN) — RSS source with a self-healing fallback.

Routes, tried in order on every run:

1. RSS  https://www.iisd.org/itn/feed/  — the original route. Valid RSS 2.0
   with substantive descriptions when it is served.
2. HTML listing  https://www.iisd.org/itn/  — the ITN homepage. Since
   ~August 2026 the feed (every variant: /feed/, ?feed=rss2, /feed/atom/,
   /itn/news/, /itn/archives/, and the article pages themselves) answers with a
   Cloudflare bot-challenge, HTTP 403 "Just a moment...", while the homepage
   still serves real HTML. Nine consecutive zero-item runs were flagged
   DEGRADED before this was understood. The listing carries each article's
   title, canonical URL and date (both in the card footer, "News | April 21,
   2026", and in the URL path /itn/YYYY/MM/DD/slug/), so it yields
   headline-level items — like iareporter_headlines — never bodies, and says
   so in ``metadata["listing_only"]``.
3. Internet Archive — when BOTH routes are refused the pipeline records
   NOT-READ and ``src/source_recovery.py`` (SPECS["iisd_itn"]) reads the
   article pages from the Wayback Machine. That guard fires only on a
   confirmed refusal, never on a plain zero, so a quiet quarter never surfaces
   stale archived pages.

A zero from this source therefore means one of exactly two things, and the
source-health probe tells them apart: the site is reachable and quiet, or
every route is walled. "The fetcher no longer matches the live site" is no
longer a possible silent state for the feed — the listing route is tried
unconditionally.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from urllib.parse import urljoin

from .base import (
    CandidateItem,
    Source,
    day_floor,
    fetch_html,
    fetch_rss,
    parse_date,
    strip_html,
)

logger = logging.getLogger("isds.sources.iisd_itn")

FEED_URL = "https://www.iisd.org/itn/feed/"
HOME_URL = "https://www.iisd.org/itn/"

# A real ITN article lives at /itn/YYYY/MM/DD/slug/ (optionally under /en/).
# Category, language and nav links (/itn/analysis/, /itn/fr/, /itn/news/) do not.
ARTICLE_PATH_RE = re.compile(r"/itn/(?:en/)?(\d{4})/(\d{2})/(\d{2})/[^/?#]+/?$")


class IISDITNSource(Source):
    name = "iisd_itn"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        # Route 1: RSS.
        feed = fetch_rss(FEED_URL)
        entries = getattr(feed, "entries", []) if feed is not None else []
        if entries:
            items = self._from_feed(entries, since)
            logger.info("iisd_itn: %d items via RSS after filtering since %s",
                        len(items), since)
            return items
        logger.warning("iisd_itn: RSS feed unavailable or empty; trying the HTML listing")

        # Route 2: the homepage listing (headline-level).
        soup = fetch_html(HOME_URL)
        if soup is None:
            logger.warning("iisd_itn: HTML listing unavailable too; returning [] "
                           "(a confirmed refusal on both routes makes this source "
                           "archive-recoverable — see src/source_recovery.py)")
            return []
        items = self._from_listing(soup, since)
        logger.info("iisd_itn: %d items via HTML listing after filtering since %s "
                    "(RSS walled; headline-level only)", len(items), since)
        return items

    # -- route 1: RSS ---------------------------------------------------------

    def _from_feed(self, entries, since: datetime) -> list[CandidateItem]:
        items: list[CandidateItem] = []
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
            metadata={"route": "rss"},
        )

    # -- route 2: HTML listing -------------------------------------------------

    def _from_listing(self, soup, since: datetime) -> list[CandidateItem]:
        """Parse the ITN homepage: ``article.card`` tiles and ``header.entry-header``
        blocks. Headline-level only — the origin walls the article pages."""
        # Listing dates are date-only ("April 21, 2026"), i.e. midnight UTC, so
        # compare against a day-floored window or items published on the
        # cutoff's calendar day after the run's clock time are lost forever.
        floor = day_floor(since) if since is not None else None
        seen: set[str] = set()
        items: list[CandidateItem] = []

        candidates = []
        for card in soup.select("article.card"):
            a = card.select_one("a.card-link[href]") or card.select_one("a[href]")
            h = card.select_one("h2, h3")
            f = card.select_one("footer")
            if a is None or h is None:
                continue
            candidates.append((a.get("href", ""), h.get_text(" ", strip=True),
                               f.get_text(" ", strip=True) if f else ""))
        for hdr in soup.select("header.entry-header"):
            a = hdr.select_one(".entry-title a[href], h1 a[href], h2 a[href]")
            f = hdr.select_one("footer")
            if a is None:
                continue
            candidates.append((a.get("href", ""), a.get_text(" ", strip=True),
                               f.get_text(" ", strip=True) if f else ""))

        for href, title, footer in candidates:
            url = urljoin(HOME_URL, href)
            m = ARTICLE_PATH_RE.search(url)
            if not m or not title or url in seen:
                continue
            seen.add(url)
            published = self._listing_date(footer, m)
            if floor is not None and published is not None and published < floor:
                continue
            items.append(CandidateItem(
                source=self.name,
                source_id=url,
                url=url,
                title=title,
                published=published,
                summary=title,
                raw_text=title,
                metadata={"route": "html-listing", "listing_only": True,
                          "listing_footer": footer},
            ))
        return items

    @staticmethod
    def _listing_date(footer: str, path_match) -> "datetime | None":
        """Date from the card footer ("News | April 21, 2026"), else the URL path."""
        if footer:
            tail = footer.split("|")[-1].strip()
            d = parse_date(tail)
            if d is not None:
                return d
        try:
            y, mo, da = (int(path_match.group(i)) for i in (1, 2, 3))
            return datetime(y, mo, da, tzinfo=timezone.utc)
        except Exception:  # noqa: BLE001 - a bad path date is just "no date"
            return None
