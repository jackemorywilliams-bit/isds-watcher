"""Google Alerts (RSS) source.

Operator-created Google Alerts, delivered as RSS feeds, are polled here. Feed
URLs live in the repo-root ``alerts.yaml`` (``feeds:`` list) so they can be added
or changed without touching code. This is fully autonomous: once the feed URLs
are in place, every scheduled run polls them with no credentials and no inbox
access. An empty/absent list simply makes the source inactive.

Google Alerts entries are Atom; each ``link`` is a google.com/url?...&url=<real>
redirect, which we resolve to the underlying publisher URL for the id/url.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from .base import (
    CandidateItem,
    Source,
    fetch_rss,
    parse_date,
    strip_html,
)

logger = logging.getLogger("isds.sources.google_alerts")

_ALERTS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "alerts.yaml",
)


def _load_feed_urls() -> list[str]:
    """Read feed URLs from alerts.yaml. Never raises; returns [] on any problem."""
    try:
        import yaml
        with open(_ALERTS_FILE, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        feeds = data.get("feeds") or []
        return [str(u).strip() for u in feeds if str(u).strip()]
    except FileNotFoundError:
        return []
    except Exception as exc:  # noqa: BLE001 - config issue must not crash the run
        logger.warning("google_alerts: could not read %s (%s)", _ALERTS_FILE, exc)
        return []


def resolve_redirect(link: str) -> str:
    """Extract the real publisher URL from a Google Alerts redirect link."""
    if not link:
        return link
    try:
        q = parse_qs(urlparse(link).query)
        for key in ("url", "q"):
            if q.get(key):
                return q[key][0]
    except Exception:  # noqa: BLE001
        pass
    return link


class GoogleAlertsSource(Source):
    name = "google_alerts"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        urls = _load_feed_urls()
        if not urls:
            logger.info("google_alerts: no feeds configured (alerts.yaml), inactive")
            return []

        items: list[CandidateItem] = []
        seen: set[str] = set()
        for feed_url in urls:
            # check_robots=False is used ONLY here: a Google Alerts feed is a
            # personal feed the operator created and subscribed to, served by
            # Google for polling in a feed reader (its intended use). Google's
            # site-wide robots.txt disallows it as it does all crawling, but
            # reading one's own subscribed alert feed is not the third-party
            # site crawling that rule governs. The identifying User-Agent and
            # the >=3s/domain rate limit still apply.
            feed = fetch_rss(feed_url, check_robots=False)
            if feed is None:
                logger.warning("google_alerts: feed unavailable %s", feed_url[:60])
                continue
            for entry in getattr(feed, "entries", []) or []:
                try:
                    item = self._to_item(entry)
                except Exception as exc:  # one bad entry must not kill the feed
                    logger.warning("google_alerts: skipping entry (%s)", exc)
                    continue
                if item is None or item.source_id in seen:
                    continue
                if item.published is not None and item.published < since:
                    continue
                seen.add(item.source_id)
                items.append(item)

        logger.info("google_alerts: %d items across %d feed(s)", len(items), len(urls))
        return items

    def _to_item(self, entry) -> "CandidateItem | None":
        raw_link = getattr(entry, "link", None)
        if not raw_link:
            return None
        url = resolve_redirect(raw_link)
        title = strip_html(getattr(entry, "title", "") or "").strip()
        published = parse_date(
            getattr(entry, "published", None) or getattr(entry, "updated", None)
        )
        summary = strip_html(getattr(entry, "summary", "") or "")
        return CandidateItem(
            source=self.name,
            source_id=url,
            url=url,
            title=title,
            published=published,
            summary=summary,
            raw_text=summary or title,
            metadata={"via": "google_alerts"},
        )
