"""Autonomous Internet-Archive recovery — hermetic (network faked at polite_get)."""
import dataclasses
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
    monkeypatch.setattr(sr.time, "sleep", lambda s: None)
    monkeypatch.setattr(sr, "_CDX_RETRY_BACKOFF_S", ())
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


def test_cdx_retries_then_succeeds_on_transient_refusal(monkeypatch):
    """archive.org refuses the CDX after a snapshot burst; a backoff retry
    clears it. The retry must NOT sleep in the test."""
    calls = {"n": 0}
    def flaky(url, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return None                       # first CDX attempt refused
        if "cdx/search" in url:
            return types.SimpleNamespace(text=ITALAW_CDX)
        if "/cases/9990" in url:
            return _snap("Newco v. Ruritania, ICSID Case No. ARB/26/1 | italaw")
        if "/cases/documents/528" in url:
            return _snap("Oldco v. State, UNCITRAL | italaw")
        return None
    monkeypatch.setattr(sr, "polite_get", flaky)
    monkeypatch.setattr(sr.time, "sleep", lambda s: None)     # no real wait
    # one retry is enough; keep the schedule short and sleepless
    monkeypatch.setattr(sr, "_CDX_RETRY_BACKOFF_S", (0,))
    items = sr.recover("italaw", SINCE)
    assert calls["n"] >= 2                     # retried after the refusal
    assert [it.url for it in items] == [
        "https://www.italaw.com/cases/9990",
        "https://www.italaw.com/cases/documents/528"]


def test_cdx_gives_up_after_retries_never_raises(monkeypatch):
    monkeypatch.setattr(sr, "polite_get", lambda url, **kw: None)
    monkeypatch.setattr(sr.time, "sleep", lambda s: None)
    monkeypatch.setattr(sr, "_CDX_RETRY_BACKOFF_S", (0, 0))
    assert sr.recover("italaw", SINCE) == []


# =============================================================================
# Recovery telemetry (SD-4, council special session 2026-09-10).
#
# A RECOVERED source published one number, the item count. It could not say how
# much of the Archive's offer the per-run politeness cap deferred, nor how old
# the snapshots it read actually were — both already computed inside the
# recovery and both dropped on the floor. `RecoveryReport` carries them out.
#
# The per-run cap and the lookback window are politeness/cost parameters and are
# NOT touched by any of this: the tests below read `spec.max_items` rather than
# setting it, and one of them asserts its value so a change cannot pass quietly.
# =============================================================================

def _many_cases(n, first_ts="20260901000000"):
    """n distinct italaw case pages, capture stamps one day apart, newest first."""
    base = datetime.datetime.strptime(first_ts, "%Y%m%d%H%M%S")
    rows = []
    for i in range(n):
        ts = (base - datetime.timedelta(days=i)).strftime("%Y%m%d%H%M%S")
        url = f"https://www.italaw.com/cases/{9000 + i}"
        rows.append([f"com,italaw)/cases/{9000 + i}", ts, url,
                     "text/html", "200", "d", "1"])
    return rows


def _serve(cdx_json, title="Newco v. Republic of Ruritania | italaw"):
    def g(url, **kw):
        if "cdx/search" in url:
            return types.SimpleNamespace(text=cdx_json)
        return _snap(title)
    return g


def test_recover_is_a_wrapper_over_recover_with_report(monkeypatch):
    """`recover()` keeps its exact signature and return type: the same list the
    reporting call produces, with nothing else in the tuple leaking out."""
    monkeypatch.setattr(sr, "polite_get", _italaw_get)
    plain = sr.recover("italaw", SINCE)
    items, report = sr.recover_with_report("italaw", SINCE)
    assert isinstance(plain, list)
    assert [it.url for it in plain] == [it.url for it in items]
    assert isinstance(report, sr.RecoveryReport)
    assert report.fetched == len(plain) == 2
    assert report.eligible == 2 and report.omitted_by_cap == 0


def test_report_counts_eligible_and_omitted(monkeypatch):
    """20 eligible captures against max_items=12: the report says 20 eligible
    and 8 omitted by the cap — the deferred 8 are disclosed, not invisible."""
    assert sr.SPECS["italaw"].max_items == 12, \
        "this test reads the politeness cap; it must not be changed for telemetry"
    monkeypatch.setattr(sr, "polite_get", _serve(_cdx("italaw", _many_cases(20))))
    items, report = sr.recover_with_report("italaw", SINCE)
    assert report.eligible == 20
    assert report.omitted_by_cap == 8
    assert report.fetched == 12 == len(items)
    assert report.eligible - report.omitted_by_cap - report.fetched == 0


def test_report_drops_are_derivable_without_a_field_of_their_own(monkeypatch):
    """A snapshot whose title is site boilerplate is attempted and dropped, so
    fetched < eligible - omitted_by_cap. The drop count needs no field: it is
    the difference, and the report must make that arithmetic true."""
    rows = _many_cases(3)

    def g(url, **kw):
        if "cdx/search" in url:
            return types.SimpleNamespace(text=_cdx("italaw", rows))
        if "/cases/9001" in url:
            return _snap("View case details | italaw")      # generic -> dropped
        return _snap("Real v. State | italaw")
    monkeypatch.setattr(sr, "polite_get", g)
    items, report = sr.recover_with_report("italaw", SINCE)
    assert report.eligible == 3 and report.omitted_by_cap == 0
    assert report.fetched == 2 == len(items)
    assert report.eligible - report.omitted_by_cap - report.fetched == 1


def test_capture_age_from_frozen_clock(monkeypatch):
    """Capture age is utcnow() minus the CDX stamp, in whole days, over the
    items actually fetched. Freeze the clock and the numbers are exact."""
    frozen = datetime.datetime(2026, 9, 10, 12, 0, 0, tzinfo=UTC)
    monkeypatch.setattr(sr, "utcnow", lambda: frozen)
    # Captures on 09-01, 08-31, 08-30, 08-29, 08-28 -> ages 9, 10, 11, 12, 13.
    monkeypatch.setattr(sr, "polite_get", _serve(_cdx("italaw", _many_cases(5))))
    _items, report = sr.recover_with_report("italaw", SINCE)
    assert report.fetched == 5
    assert report.newest_capture == "20260901000000"
    assert report.oldest_capture == "20260828000000"
    assert report.capture_age_days_max == 13
    assert report.capture_age_days_median == 11


def test_capture_age_median_of_an_even_set_truncates_to_whole_days(monkeypatch):
    """Four items -> the median is the mean of the two central ages, reported as
    whole days. Pinned so the rounding rule cannot drift silently."""
    frozen = datetime.datetime(2026, 9, 10, 12, 0, 0, tzinfo=UTC)
    monkeypatch.setattr(sr, "utcnow", lambda: frozen)
    # Ages 9, 10, 11, 12 -> the median of 10 and 11 is 10.5 -> 10.
    monkeypatch.setattr(sr, "polite_get", _serve(_cdx("italaw", _many_cases(4))))
    _items, report = sr.recover_with_report("italaw", SINCE)
    assert report.fetched == 4
    assert report.capture_age_days_median == 10
    assert report.capture_age_days_max == 12


def test_oldest_capture_is_eligible_basis_while_ages_are_fetched(monkeypatch):
    """The two halves of the report have DIFFERENT bases, on purpose.

    oldest/newest_capture span everything the Archive offered (the ELIGIBLE
    set); the ages describe only what this run read (the FETCHED set). When the
    cap bites, the oldest eligible capture was never fetched, so its age is NOT
    capture_age_days_max. This test exists so nobody "fixes" the divergence into
    agreement without reading the RecoveryReport docstring first.
    """
    frozen = datetime.datetime(2026, 9, 10, 12, 0, 0, tzinfo=UTC)
    monkeypatch.setattr(sr, "utcnow", lambda: frozen)
    # 20 captures, 09-01 back to 08-13; the cap fetches the newest 12 (to 08-21).
    monkeypatch.setattr(sr, "polite_get", _serve(_cdx("italaw", _many_cases(20))))
    _items, report = sr.recover_with_report("italaw", SINCE)
    assert report.oldest_capture == "20260813000000"      # eligible, not fetched
    oldest_eligible_age = sr._capture_age_days(report.oldest_capture, frozen)
    assert oldest_eligible_age == 28
    assert report.capture_age_days_max == 20              # the oldest FETCHED
    assert report.capture_age_days_max < oldest_eligible_age


def test_malformed_capture_stamp_is_dropped_not_fatal(monkeypatch):
    """One unparseable CDX stamp must not poison the age statistics or raise."""
    frozen = datetime.datetime(2026, 9, 10, 12, 0, 0, tzinfo=UTC)
    monkeypatch.setattr(sr, "utcnow", lambda: frozen)
    rows = _many_cases(2)
    rows.append(["com,italaw)/cases/9500", "not-a-timestamp",
                 "https://www.italaw.com/cases/9500", "text/html", "200", "d", "1"])
    monkeypatch.setattr(sr, "polite_get", _serve(_cdx("italaw", rows)))
    _items, report = sr.recover_with_report("italaw", SINCE)
    assert report.eligible == 3 and report.fetched == 3
    assert report.capture_age_days_max == 10              # the two real stamps
    assert sr._capture_age_days("20261399000000", frozen) is None   # month 13
    assert sr._capture_age_days("", frozen) is None


def test_empty_recoveries_report_the_empty_state_never_none(monkeypatch):
    """No spec, an unavailable CDX index and a non-JSON CDX body all return a
    real RecoveryReport, so a caller never has to guard for None."""
    assert sr.recover_with_report("icsid", SINCE) == ([], sr.RecoveryReport())
    monkeypatch.setattr(sr, "polite_get", lambda url, **kw: None)
    monkeypatch.setattr(sr.time, "sleep", lambda s: None)
    monkeypatch.setattr(sr, "_CDX_RETRY_BACKOFF_S", ())
    assert sr.recover_with_report("italaw", SINCE) == ([], sr.RecoveryReport())
    monkeypatch.setattr(sr, "polite_get",
                        lambda url, **kw: types.SimpleNamespace(text="<html>"))
    items, report = sr.recover_with_report("italaw", SINCE)
    assert (items, report) == ([], sr.RecoveryReport())
    assert report.eligible == 0 and report.oldest_capture is None


def test_the_report_is_json_serialisable_as_one_nested_meta_key():
    """src/main.py writes asdict(report) under entry["recovery"]. Every field
    must survive json.dumps unchanged, or meta.json fails to write."""
    report = sr.RecoveryReport(eligible=20, fetched=12, omitted_by_cap=8,
                               oldest_capture="20260813000000",
                               newest_capture="20260901000000",
                               capture_age_days_max=20,
                               capture_age_days_median=15)
    blob = dataclasses.asdict(report)
    assert sorted(blob) == ["capture_age_days_max", "capture_age_days_median",
                            "eligible", "fetched", "newest_capture",
                            "oldest_capture", "omitted_by_cap"]
    assert json.loads(json.dumps(blob)) == blob


def test_validate_archive_is_green_on_a_meta_carrying_the_recovery_key(tmp_path):
    """The archive validator must tolerate the new nested key. A synthetic
    digest folder carrying entry["recovery"] validates clean — otherwise SD-4
    would turn every future recovered run into a red build."""
    import os
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(repo, "scripts"))
    from validate_archive import validate_archive

    report = sr.RecoveryReport(eligible=20, fetched=12, omitted_by_cap=8,
                               oldest_capture="20260813000000",
                               newest_capture="20260901000000",
                               capture_age_days_max=20,
                               capture_age_days_median=15)
    folder = tmp_path / "2099-02-02_ISDS-Thematic-Watch"
    (folder / "articles").mkdir(parents=True)
    (folder / "articles" / "01_real.md").write_text(
        "# 1. Real Case v. State\n- **Relevance:** 30 (WATCH)\n", encoding="utf-8")
    (folder / "meta.json").write_text(json.dumps({
        "date": "2099-02-02", "screened": 12, "matches": 0,
        "watch_list_leads": 1, "accepted": 1,
        "source_health": [{"name": "italaw",
                           "status": "RECOVERED (Internet Archive)",
                           "count": 12,
                           "recovery": dataclasses.asdict(report)}],
    }), encoding="utf-8")
    assert validate_archive(str(tmp_path)) == []


def test_source_health_guard_tolerates_the_extra_nested_key(tmp_path):
    """The zero-streak guard reads name/status/count and must ignore the rest.
    Run the real apply/persist path over an entry carrying entry["recovery"]."""
    from src import source_health as sh_mod
    report = sr.RecoveryReport(eligible=3, fetched=3, capture_age_days_max=9,
                               capture_age_days_median=9,
                               oldest_capture="20260901000000",
                               newest_capture="20260903000000")
    entries = [{"name": "italaw", "status": "RECOVERED (Internet Archive)",
                "count": 3, "recovery": dataclasses.asdict(report)},
               {"name": "icsid", "status": "RETURNED", "count": 2}]
    path = str(tmp_path / "source_health.json")
    warnings = sh_mod.record_run(entries, "2026-09-10", path=path)
    assert warnings == []
    assert entries[0]["status"] == "RECOVERED (Internet Archive)"
    assert entries[0]["recovery"]["omitted_by_cap"] == 0
    persisted = json.loads(open(path, encoding="utf-8").read())
    assert persisted["sources"]["italaw"]["zero_streak"] == 0
    assert persisted["sources"]["italaw"]["last_nonzero"] == "2026-09-10"
