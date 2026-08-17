"""italaw Internet-Archive fallback — hermetic (network faked at polite_get)."""
import datetime
import json
import types

import sys
sys.path.insert(0, ".")
from src.sources import italaw  # noqa: E402
from src.enrich import enrich  # noqa: E402
from src.sources.base import CandidateItem  # noqa: E402

UTC = datetime.timezone.utc
SINCE = datetime.datetime(2026, 8, 1, tzinfo=UTC)

_CDX = json.dumps([
    ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"],
    ["com,italaw)/cases/9990", "20260814120907", "https://www.italaw.com/cases/9990", "text/html", "200", "d", "1"],
    ["com,italaw)/cases/9990", "20260701000000", "https://www.italaw.com/cases/9990", "text/html", "200", "d", "1"],  # older dup
    ["com,italaw)/browse/economic-sector", "20260814120907", "https://www.italaw.com/browse/economic-sector", "text/html", "200", "d", "1"],  # not a case
    ["com,italaw)/cases/documents/528", "20260810000000", "https://www.italaw.com/cases/documents/528", "text/html", "200", "d", "1"],
])

def _snap(title, body="Respondent Argentina. Applicable treaty BIT. Trade secret disclosure."):
    marker = italaw._WB_TOOLBAR_END
    return types.SimpleNamespace(
        text=f"<html><head><title>{title} | italaw</title></head>"
             f"{marker}<body><h1>{title}</h1><p>{body}</p></body></html>")


def _fake_get(url, **kw):
    if "cdx/search" in url:
        return types.SimpleNamespace(text=_CDX)
    if "/cases/9990" in url:
        return _snap("Newco v. Republic of Ruritania, ICSID Case No. ARB/26/1")
    if "/cases/documents/528" in url:
        return _snap("Oldco v. State, UNCITRAL")
    return None


def test_wayback_fallback_yields_deduped_case_items(monkeypatch):
    monkeypatch.setattr(italaw, "polite_get", _fake_get)
    items = italaw.ItalawSource()._fetch_via_wayback(SINCE)
    urls = [it.url for it in items]
    # two distinct case pages, the browse page excluded, the older dup collapsed
    assert urls == ["https://www.italaw.com/cases/9990",
                    "https://www.italaw.com/cases/documents/528"]
    it = items[0]
    assert it.title == "Newco v. Republic of Ruritania, ICSID Case No. ARB/26/1"
    assert it.source == "italaw"
    assert it.metadata["retrieved_via"] == "internet-archive"
    assert it.metadata["body_final"] is True
    assert "Respondent Argentina" in it.raw_text


def test_fetch_falls_back_when_origin_challenged(monkeypatch):
    monkeypatch.setattr(italaw, "fetch_html", lambda url: None)   # origin 403
    monkeypatch.setattr(italaw, "polite_get", _fake_get)
    items = italaw.ItalawSource().fetch(SINCE)
    assert len(items) == 2 and all(i.source == "italaw" for i in items)


def test_cdx_unavailable_is_empty_never_raises(monkeypatch):
    monkeypatch.setattr(italaw, "polite_get", lambda url, **kw: None)
    assert italaw.ItalawSource()._fetch_via_wayback(SINCE) == []


def test_generic_title_snapshot_skipped(monkeypatch):
    def g(url, **kw):
        if "cdx" in url:
            return types.SimpleNamespace(text=_CDX)
        return _snap("View case details")   # generic → no title → dropped
    monkeypatch.setattr(italaw, "polite_get", g)
    assert italaw.ItalawSource()._fetch_via_wayback(SINCE) == []


def test_enrich_keeps_body_final_without_refetch(monkeypatch):
    called = {"n": 0}
    def boom(url):
        called["n"] += 1
        raise AssertionError("enrich must not re-fetch a body_final item")
    monkeypatch.setattr("src.enrich.fetch_html", boom)
    it = CandidateItem(source="italaw", source_id="u", url="https://www.italaw.com/cases/1",
                       title="X v. Y", published=None, summary="s",
                       raw_text="Respondent Argentina. Trade secret.",
                       metadata={"body_final": True})
    out = enrich(it)
    assert called["n"] == 0
    assert out.raw_text == "Respondent Argentina. Trade secret."
    assert out.metadata["enriched"] is True
