"""Parser regression tests against trimmed LIVE snapshots (fetched 2026-07-27).

Each fixture in tests/fixtures/ is a trimmed copy of the real page/feed as it
was served on 2026-07-27, so these tests pin the parsers to the CURRENT site
structure. They also pin the window-boundary fix: date-only publication stamps
(midnight UTC) must be compared against a day-floored ``since``, or items
published on the cutoff's calendar day after the run's clock time are lost
forever (the root cause of pca_press's zero weeks: every missed item was
Monday-dated, and the weekly run fires Mondays 13:00 UTC).

No network access: fetch_html / fetch_rss are monkeypatched to serve fixtures.
"""

import datetime
import os

import feedparser
from bs4 import BeautifulSoup

from src.sources.base import day_floor

UTC = datetime.timezone.utc
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

LONG_AGO = datetime.datetime(2000, 1, 1, tzinfo=UTC)


def _soup(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as fh:
        return BeautifulSoup(fh.read(), "html.parser")


def _feed(name):
    with open(os.path.join(FIXTURES, name), "rb") as fh:
        return feedparser.parse(fh.read())


# --- day_floor ---------------------------------------------------------------
def test_day_floor_floors_to_utc_midnight():
    dt = datetime.datetime(2026, 7, 20, 13, 0, tzinfo=UTC)
    assert day_floor(dt) == datetime.datetime(2026, 7, 20, tzinfo=UTC)


def test_day_floor_normalizes_timezone():
    est = datetime.timezone(datetime.timedelta(hours=-5))
    dt = datetime.datetime(2026, 7, 20, 22, 30, tzinfo=est)  # 03:30 UTC on the 21st
    assert day_floor(dt) == datetime.datetime(2026, 7, 21, tzinfo=UTC)


# --- pca_press ---------------------------------------------------------------
def test_pca_press_parses_live_structure(monkeypatch):
    import src.sources.pca_press as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: _soup("pca_news.html"))
    items = mod.PCAPressSource().fetch(LONG_AGO)
    assert len(items) == 3
    titles = [it.title for it in items]
    assert any("Somalia" in t for t in titles)
    assert any("Elliott Associates" in t for t in titles)
    somalia = next(it for it in items if "Somalia" in it.title)
    assert somalia.published == datetime.datetime(2026, 7, 20, tzinfo=UTC)
    assert not somalia.metadata.get("date_inferred")
    assert somalia.url.startswith("https://pca-cpa.org/en/news/")


def test_pca_press_keeps_midnight_item_on_cutoff_day(monkeypatch):
    """The regression that caused the zero weeks: an item stamped Monday 00:00
    must survive a since cutoff of Monday 13:00 (the weekly run time)."""
    import src.sources.pca_press as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: _soup("pca_news.html"))
    since = datetime.datetime(2026, 7, 20, 13, 0, tzinfo=UTC)  # Mon 13:00 UTC
    items = mod.PCAPressSource().fetch(since)
    assert any("Somalia" in it.title for it in items), \
        "Monday-midnight item was dropped by the since filter"
    # But items from clearly earlier days stay filtered out.
    assert not any("Kingdom of Spain" in it.title for it in items)


def test_pca_press_degrades_to_empty(monkeypatch):
    import src.sources.pca_press as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: None)
    assert mod.PCAPressSource().fetch(LONG_AGO) == []


# --- icsid -------------------------------------------------------------------
def test_icsid_parses_live_structure(monkeypatch):
    import src.sources.icsid as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: _soup("icsid_news_events.html"))
    items = mod.ICSIDSource().fetch(LONG_AGO)
    assert len(items) == 3
    honduras = next(it for it in items if "Honduras Ratifies" in it.title)
    assert honduras.published == datetime.datetime(2026, 7, 17, tzinfo=UTC)
    assert honduras.url == ("https://icsid.worldbank.org/news-and-events/"
                            "comunicados/honduras-ratifies-icsid-convention")


def test_icsid_since_uses_day_floor(monkeypatch):
    import src.sources.icsid as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: _soup("icsid_news_events.html"))
    since = datetime.datetime(2026, 7, 17, 13, 0, tzinfo=UTC)
    items = mod.ICSIDSource().fetch(since)
    assert any("Honduras Ratifies" in it.title for it in items)
    assert not any("Contract-Based" in it.title for it in items)


def test_icsid_degrades_to_empty(monkeypatch):
    import src.sources.icsid as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: None)
    assert mod.ICSIDSource().fetch(LONG_AGO) == []


# --- iisd_itn ----------------------------------------------------------------
def test_iisd_itn_parses_live_feed(monkeypatch):
    import src.sources.iisd_itn as mod
    monkeypatch.setattr(mod, "fetch_rss", lambda url, **kw: _feed("iisd_itn_feed.xml"))
    items = mod.IISDITNSource().fetch(LONG_AGO)
    assert len(items) == 2
    assert items[0].title == "ITN Issue 2, 2026"
    assert items[0].url == "https://www.iisd.org/itn/2026/04/21/itn-issue-2-2026/"
    assert items[0].published.date() == datetime.date(2026, 4, 21)
    assert items[0].raw_text  # substantive description present


def test_iisd_itn_since_filter(monkeypatch):
    """A 7-day window after the last (April) issue yields zero items — the feed
    is HEALTHY but the journal is quarterly. Not a parser failure."""
    import src.sources.iisd_itn as mod
    monkeypatch.setattr(mod, "fetch_rss", lambda url, **kw: _feed("iisd_itn_feed.xml"))
    since = datetime.datetime(2026, 7, 20, tzinfo=UTC)
    assert mod.IISDITNSource().fetch(since) == []


def test_iisd_itn_degrades_to_empty(monkeypatch):
    import src.sources.iisd_itn as mod
    monkeypatch.setattr(mod, "fetch_rss", lambda url, **kw: None)
    assert mod.IISDITNSource().fetch(LONG_AGO) == []


# --- google_alerts -----------------------------------------------------------
def test_google_alerts_empty_feed_is_healthy_zero(monkeypatch):
    """Live alert feeds currently serve valid Atom with ZERO entries (Google
    only keeps recent results in the feed). That must parse cleanly to zero
    items — an empty week, not an error."""
    parsed = _feed("google_alert_empty.xml")
    assert not parsed.bozo and len(parsed.entries) == 0
    import src.sources.google_alerts as mod
    monkeypatch.setattr(mod, "_load_feed_urls", lambda: ["https://www.google.com/alerts/feeds/x/y"])
    monkeypatch.setattr(mod, "fetch_rss", lambda url, **kw: parsed)
    assert mod.GoogleAlertsSource().fetch(LONG_AGO) == []


def test_google_alerts_no_feeds_inactive(monkeypatch):
    import src.sources.google_alerts as mod
    monkeypatch.setattr(mod, "_load_feed_urls", lambda: [])
    assert mod.GoogleAlertsSource().fetch(LONG_AGO) == []


# --- italaw ------------------------------------------------------------------
def test_italaw_degrades_to_empty_when_challenged(monkeypatch):
    """www.italaw.com now serves a Cloudflare managed challenge (403,
    Cf-Mitigated: challenge) to non-browser clients on every path; fetch_html
    returns None and the source must degrade to [] without raising. The
    zero-streak guard (src/source_health.py) is what surfaces the outage."""
    import src.sources.italaw as mod
    monkeypatch.setattr(mod, "fetch_html", lambda url: None)
    assert mod.ItalawSource().fetch(LONG_AGO) == []
