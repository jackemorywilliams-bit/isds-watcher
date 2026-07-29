"""Parser tests for the press-business RSS sources (live-snapshot fixtures,
fetched 2026-07-29 with the project's identified UA — both feeds verified to
serve identified crawlers, unlike the Cloudflare-walled outlets)."""

import os
import sys
from datetime import datetime, timedelta, timezone
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import feedparser  # noqa: E402

from src.sources.press_business import (  # noqa: E402
    IndependentBusinessSource,
    StandardBusinessSource,
)

_FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def _feed(name):
    return feedparser.parse(open(os.path.join(_FIX, name), "rb").read())


def _fetch_with_fixture(source, fixture):
    with mock.patch("src.sources.press_business.fetch_rss", return_value=_feed(fixture)):
        return source.fetch(datetime.now(timezone.utc) - timedelta(days=3650))


def test_independent_business_parses_fixture():
    items = _fetch_with_fixture(IndependentBusinessSource(), "independent_business_feed.xml")
    assert len(items) >= 2
    first = items[0]
    assert first.source == "independent_business"
    assert first.url.startswith("https://www.independent.co.uk/")
    assert first.title and first.published is not None
    assert first.published.tzinfo is not None


def test_standard_business_parses_fixture():
    items = _fetch_with_fixture(StandardBusinessSource(), "standard_business_feed.xml")
    assert len(items) >= 2
    first = items[0]
    assert first.source == "standard_business"
    assert first.url.startswith("https://www.standard.co.uk/")
    assert first.title and first.published is not None


def test_since_filter_and_unavailable_feed_degrade():
    src = IndependentBusinessSource()
    future = datetime.now(timezone.utc) + timedelta(days=1)
    with mock.patch("src.sources.press_business.fetch_rss",
                    return_value=_feed("independent_business_feed.xml")):
        assert src.fetch(future) == []          # everything older than 'since'
    with mock.patch("src.sources.press_business.fetch_rss", return_value=None):
        assert src.fetch(future) == []          # unavailable feed degrades to []


def test_registered_in_all_sources():
    from src.sources import all_sources
    names = [s.name for s in all_sources()]
    assert "independent_business" in names
    assert "standard_business" in names
