"""Autonomous Internet-Archive recovery — hermetic (network faked at polite_get)."""
import datetime
import json
import types

import sys
sys.path.insert(0, ".")
from src import source_recovery as sr  # noqa: E402
from src.enrich import enrich  # noqa: E402
from src.sources.base import CandidateItem  # noqa: E402

UTC = datetime.timezone.utc
SINCE = datetime.datetime(2026, 8, 1, tzinfo=UTC)


def _cdx(prefix, rows):
    header = ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"]
    return json.dumps([header] + rows)


def _snap(title, body="Respondent Argentina. Applicable treaty BIT. Trade secret disclosure."):
    marker = sr._WB_TOOLBAR_END
    return types.SimpleNamespace(
        text=f"<html><head><title>{title}</title></head>"
             f"{marker}<body><p>{body}</p></body></html>")


ITALAW_CDX = _cdx("italaw", [
    ["com,italaw)/cases/9990", "20260814120907", "https://www.italaw.com/cases/9990", "text/html", "200", "d", "1"],
    ["com,italaw)/cases/9990", "20260701000000", "https://www.italaw.com/cases/9990", "text/html", "200", "d", "1"],   # older dup
    ["com,italaw)/browse/economic-sector", "20260814120907", "https://www.italaw.com/browse/economic-sector", "text/html", "200", "d", "1"],  # not a case
    ["com,italaw)/cases/documents/528", "20260810000000", "https://www.italaw.com/cases/documents/528", "text/html", "200", "d", "1"],
])
UNCTAD_CDX = _cdx("unctad", [
    ["org,unctad...)/cases/1417/all", "20260809183502", "https://investmentpolicy.unctad.org/investment-dispute-settlement/cases/1417/all", "text/html", "200", "d", "1"],
])


def _italaw_get(url, **kw):
    if "cdx/search" in url:
        return ITALAW_CDX and types.SimpleNamespace(text=ITALAW_CDX)
    if "/cases/9990" in url:
        return _snap("Newco v. Republic of Ruritania, ICSID Case No. ARB/26/1 | italaw")
    if "/cases/documents/528" in url:
        return _snap("Oldco v. State, UNCITRAL | italaw")
    return None


def test_italaw_recovers_deduped_case_pages(monkeypatch):
    monkeypatch.setattr(sr, "polite_get", _italaw_get)
    items = sr.recover("italaw", SINCE)
    assert [it.url for it in items] == [
        "https://www.italaw.com/cases/9990",
        "https://www.italaw.com/cases/documents/528"]
    it = items[0]
    assert it.title == "Newco v. Republic of Ruritania, ICSID Case No. ARB/26/1"
    assert it.source == "italaw"
    assert it.metadata["retrieved_via"] == "internet-archive"
    assert it.metadata["body_final"] is True
    assert "Respondent Argentina" in it.raw_text


def test_unctad_recovers_and_strips_navigator_suffix(monkeypatch):
    def g(url, **kw):
        if "cdx/search" in url:
            return types.SimpleNamespace(text=UNCTAD_CDX)
        return _snap("L1bre v. Mexico (II) | Investment Dispute Settlement Navigator | UNCTAD Investment Policy Hub")
    monkeypatch.setattr(sr, "polite_get", g)
    items = sr.recover("unctad_isds", SINCE)
    assert len(items) == 1
    assert items[0].title == "L1bre v. Mexico (II)"
    assert items[0].url.endswith("/cases/1417/all")


def test_unknown_source_is_noop():
    assert sr.recover("icsid", SINCE) == []
    assert sr.is_recoverable("icsid") is False
    assert sr.is_recoverable("italaw") is True


def test_cdx_unavailable_is_empty_never_raises(monkeypatch):
    monkeypatch.setattr(sr, "polite_get", lambda url, **kw: None)
    assert sr.recover("italaw", SINCE) == []


def test_generic_title_snapshot_skipped(monkeypatch):
    def g(url, **kw):
        if "cdx" in url:
            return types.SimpleNamespace(text=ITALAW_CDX)
        return _snap("View case details | italaw")
    monkeypatch.setattr(sr, "polite_get", g)
    assert sr.recover("italaw", SINCE) == []


def test_enrich_keeps_body_final_without_refetch(monkeypatch):
    def boom(url):
        raise AssertionError("enrich must not re-fetch a body_final item")
    monkeypatch.setattr("src.enrich.fetch_html", boom)
    it = CandidateItem(source="italaw", source_id="u", url="https://www.italaw.com/cases/1",
                       title="X v. Y", published=None, summary="s",
                       raw_text="Respondent Argentina. Trade secret.",
                       metadata={"body_final": True})
    out = enrich(it)
    assert out.raw_text == "Respondent Argentina. Trade secret."
    assert out.metadata["enriched"] is True
