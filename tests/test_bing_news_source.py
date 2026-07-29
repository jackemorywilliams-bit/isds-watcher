"""Parser tests for the Bing News keyword source (live-snapshot fixture,
fetched 2026-07-29; robots.txt for /news/search live-verified as permitted
for generic agents)."""

import os
import sys
from datetime import datetime, timedelta, timezone
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import feedparser  # noqa: E402

from src.sources.bing_news import BingNewsSource, QUERIES  # noqa: E402

_FIX = os.path.join(os.path.dirname(__file__), "fixtures", "bing_news_feed.xml")


def _feed():
    return feedparser.parse(open(_FIX, "rb").read())


def test_parses_fixture_and_dedups_across_queries(monkeypatch):
    monkeypatch.setattr("src.sources.bing_news.fetch_rss", lambda url: _feed())
    monkeypatch.setattr("src.sources.bing_news.time", mock.Mock(sleep=lambda s: None))
    items = BingNewsSource().fetch(datetime.now(timezone.utc) - timedelta(days=3650))
    # Same fixture served for every query: dedup must collapse to the fixture's items.
    assert 1 <= len(items) <= 3
    first = items[0]
    assert first.source == "bing_news"
    assert first.url.startswith("http")
    assert first.title
    assert first.metadata.get("query") == QUERIES[0]


def test_unavailable_feed_degrades(monkeypatch):
    monkeypatch.setattr("src.sources.bing_news.fetch_rss", lambda url: None)
    monkeypatch.setattr("src.sources.bing_news.time", mock.Mock(sleep=lambda s: None))
    assert BingNewsSource().fetch(datetime.now(timezone.utc)) == []


def test_queries_cover_the_live_research_fronts():
    joined = " ".join(QUERIES).lower()
    for term in ("trade secret", "clinical trial data", "data exclusivity",
                 "nexperia", "einarsson", "hela schwarz", "uncitral"):
        assert term in joined


def test_registered_in_all_sources():
    from src.sources import all_sources
    names = [s.name for s in all_sources()]
    assert "bing_news" in names
    assert "google_news_rss" not in names
    assert "independent_business" not in names and "standard_business" not in names
