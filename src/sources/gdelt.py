"""GDELT DOC 2.0 — full-text news search source (added 2026-08-17).

Replaces the coverage the retired Google Alerts queries provided (the three
Google feed URLs went live-but-empty in mid-July 2026 and were retired from
``alerts.yaml``), and backstops the italaw outage with news coverage of new
awards and decisions. GDELT's DOC API is free, keyless, and intended for
programmatic use; it indexes worldwide news with ~15-minute latency.

Design constraints, honored deliberately:
- ONE request per run. GDELT rate-limits shared IPs hard (one request per 5s,
  and GitHub-runner IPs share a pool), so the queries are combined into a
  single OR expression rather than looped. A rate-limit response is plain text
  rather than JSON; it is logged and yields [] — never an exception.
- artlist mode returns title/url/domain/seendate only. ``raw_text`` is the
  title; the enrich stage fetches the article body for classification, exactly
  as it does for the ICSID and PCA listing sources.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from urllib.parse import quote

from .base import CandidateItem, Source, polite_get

logger = logging.getLogger("isds.sources.gdelt")

# One combined expression: the fingerprint's core vocabulary plus the intent of
# the three retired Google Alerts queries (treaty shopping; IP as a covered
# investment; the promise doctrine) in GDELT's query syntax.
QUERY = ('("investor-state arbitration" OR "investment treaty arbitration" OR '
         '"ICSID tribunal" OR "arbitral award" OR "treaty shopping" OR '
         '"covered investment" OR "promise doctrine") sourcelang:english')

API_URL = ("https://api.gdeltproject.org/api/v2/doc/doc?query={q}"
           "&mode=artlist&maxrecords=75&timespan=8d&sort=datedesc&format=json")


def _parse_seendate(s: str) -> "datetime | None":
    # GDELT seendate: "20260817T131500Z"
    try:
        return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


class GDELTSource(Source):
    name = "gdelt"
    priority = "secondary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        url = API_URL.format(q=quote(QUERY, safe=""))
        resp = polite_get(url)
        if resp is None:
            logger.warning("gdelt: request failed, returning []")
            return []
        body = getattr(resp, "text", "") or ""
        try:
            data = json.loads(body)
        except ValueError:
            # The rate limiter answers 200 with plain text. Log the head so the
            # run summary shows WHY the source was empty, and yield nothing.
            logger.warning("gdelt: non-JSON response (rate-limited?): %s",
                           body[:120].replace("\n", " "))
            return []

        items: list[CandidateItem] = []
        seen: set[str] = set()
        for art in data.get("articles", []) or []:
            link = (art.get("url") or "").strip()
            title = (art.get("title") or "").strip()
            if not link or not title or link in seen:
                continue
            published = _parse_seendate(art.get("seendate", ""))
            if published is not None and published < since:
                continue
            seen.add(link)
            items.append(CandidateItem(
                source=self.name,
                source_id=link,
                url=link,
                title=title,
                published=published,
                summary="",
                raw_text=title,
                metadata={"domain": art.get("domain", ""), "via": "gdelt-doc-2.0"},
            ))
        logger.info("gdelt: %d items from one combined query since %s",
                    len(items), since)
        return items
