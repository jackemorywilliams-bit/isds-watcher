"""GDELT source: hermetic tests — the network is faked at polite_get."""
import datetime
import json
import sys
import types

sys.path.insert(0, ".")
from src.sources import gdelt  # noqa: E402

UTC = datetime.timezone.utc
SINCE = datetime.datetime(2026, 8, 10, tzinfo=UTC)


def _resp(text):
    r = types.SimpleNamespace()
    r.text = text
    return r


def test_parses_articles_and_filters_since(monkeypatch):
    body = json.dumps({"articles": [
        {"url": "https://ex.com/a", "title": "New ICSID award enforced",
         "seendate": "20260816T120000Z", "domain": "ex.com"},
        {"url": "https://ex.com/old", "title": "Old story",
         "seendate": "20260701T120000Z", "domain": "ex.com"},
        {"url": "https://ex.com/a", "title": "Duplicate URL dropped",
         "seendate": "20260816T130000Z", "domain": "ex.com"},
        {"url": "", "title": "No URL dropped", "seendate": "20260816T120000Z"},
    ]})
    monkeypatch.setattr(gdelt, "polite_get", lambda url, **kw: _resp(body))
    items = gdelt.GDELTSource().fetch(SINCE)
    assert [it.title for it in items] == ["New ICSID award enforced"]
    assert items[0].source == "gdelt"
    assert items[0].published == datetime.datetime(2026, 8, 16, 12, 0, tzinfo=UTC)
    assert items[0].metadata["via"] == "gdelt-doc-2.0"


def test_rate_limit_text_yields_empty_never_raises(monkeypatch):
    monkeypatch.setattr(gdelt, "polite_get",
                        lambda url, **kw: _resp("Please limit requests to one every 5 seconds"))
    assert gdelt.GDELTSource().fetch(SINCE) == []


def test_fetch_failure_yields_empty(monkeypatch):
    monkeypatch.setattr(gdelt, "polite_get", lambda url, **kw: None)
    assert gdelt.GDELTSource().fetch(SINCE) == []


def test_unparseable_seendate_survives(monkeypatch):
    body = json.dumps({"articles": [
        {"url": "https://ex.com/x", "title": "Dateless survives",
         "seendate": "garbage", "domain": "ex.com"}]})
    monkeypatch.setattr(gdelt, "polite_get", lambda url, **kw: _resp(body))
    items = gdelt.GDELTSource().fetch(SINCE)
    assert len(items) == 1 and items[0].published is None
