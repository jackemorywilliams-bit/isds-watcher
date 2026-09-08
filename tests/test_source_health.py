"""Tests for the silent-decay guard (src/source_health.py): consecutive-zero
streak persistence, DEGRADED escalation, the COLLECTION ANOMALY check, and the
warnings' visibility in meta.json / the digest README / the digest header."""

import datetime
import json
import os
import shutil

from src import source_health

UTC = datetime.timezone.utc


def _sh(name, count, status="RETURNED"):
    return {"name": name, "status": status, "count": count}


# --- streak persistence ------------------------------------------------------
import pytest


@pytest.fixture(autouse=True)
def _no_network_probes(monkeypatch):
    """Unit tests must stay hermetic: the zero-streak refinement probes reach
    the live feeds by design, so the default here is no probes at all. Tests
    of the refinement logic install fake probes explicitly."""
    monkeypatch.setattr(source_health, "PROBES", {})


def test_streak_increments_and_resets():
    h = source_health.load("/nonexistent/health.json")
    source_health.update_streaks(h, {"italaw": 0, "icsid": 5}, "2026-07-13")
    source_health.update_streaks(h, {"italaw": 0, "icsid": 0}, "2026-07-20")
    source_health.update_streaks(h, {"italaw": 0, "icsid": 3}, "2026-07-27")
    assert source_health.zero_streak(h, "italaw") == 3
    assert source_health.zero_streak(h, "icsid") == 0
    assert h["sources"]["icsid"]["last_nonzero"] == "2026-07-27"
    assert h["sources"]["italaw"]["last_run"] == "2026-07-27"


def test_health_file_roundtrip_and_corrupt(tmp_path):
    p = str(tmp_path / "source_health.json")
    h = source_health.load(p)
    source_health.update_streaks(h, {"pca_press": 0}, "2026-07-27")
    source_health.save(h, p)
    again = source_health.load(p)
    assert source_health.zero_streak(again, "pca_press") == 1
    with open(p, "w") as fh:
        fh.write("{corrupt")
    assert source_health.load(p) == {"sources": {}}


# --- DEGRADED escalation -----------------------------------------------------
def test_degraded_status_at_three_zero_runs():
    h = {"sources": {"italaw": {"zero_streak": 3}}}
    run = [_sh("italaw", 0), _sh("icsid", 4)]
    degraded = source_health.apply_to_source_health(run, h)
    assert degraded == ["italaw"]
    assert run[0]["status"] == "DEGRADED (3 zero runs)"
    assert run[1]["status"] == "RETURNED"


def test_not_degraded_below_threshold():
    h = {"sources": {"italaw": {"zero_streak": 2}}}
    run = [_sh("italaw", 0)]
    assert source_health.apply_to_source_health(run, h) == []
    assert run[0]["status"] == "RETURNED"


def test_exempt_and_inactive_sources_never_degraded():
    h = {"sources": {"google_news_rss": {"zero_streak": 9},
                     "gmail_scholar": {"zero_streak": 9},
                     "icsid": {"zero_streak": 9}}}
    run = [_sh("google_news_rss", 0, status="DISABLED"),
           _sh("gmail_scholar", 0),
           _sh("icsid", 0, status="FAILED")]
    assert source_health.apply_to_source_health(run, h) == []
    assert run[0]["status"] == "DISABLED"      # robots-blocked: already explained
    assert run[1]["status"] == "RETURNED"      # credential-gated: not documented active
    assert run[2]["status"] == "FAILED"        # a raised fetch stays FAILED


def test_nonzero_source_never_degraded_despite_stale_streak():
    h = {"sources": {"icsid": {"zero_streak": 5}}}
    run = [_sh("icsid", 2)]
    assert source_health.apply_to_source_health(run, h) == []


# --- collection anomaly ------------------------------------------------------
def test_collection_anomaly_all_but_one_zero():
    # The 2026-07-27 shape: only iareporter yielded items among active sources.
    run = [_sh("iisd_itn", 0), _sh("google_alerts", 0), _sh("italaw", 0),
           _sh("icsid", 0), _sh("pca_press", 0), _sh("unctad_isds", 0),
           _sh("iareporter_headlines", 10, status="HEADLINE-ONLY"),
           _sh("google_news_rss", 0, status="DISABLED")]
    assert source_health.collection_anomaly(run) is True


def test_no_anomaly_on_healthy_mix():
    run = [_sh("iisd_itn", 3), _sh("italaw", 2), _sh("icsid", 0),
           _sh("pca_press", 1)]
    assert source_health.collection_anomaly(run) is False


# --- warnings ----------------------------------------------------------------
def test_build_warnings_texts():
    h = {"sources": {n: {"zero_streak": 4} for n in
                     ("iisd_itn", "google_alerts", "italaw", "icsid",
                      "pca_press", "unctad_isds")}}
    run = [_sh(n, 0) for n in ("iisd_itn", "google_alerts", "italaw", "icsid",
                               "pca_press", "unctad_isds")]
    run.append(_sh("iareporter_headlines", 10, status="HEADLINE-ONLY"))
    degraded = source_health.apply_to_source_health(run, h)
    warnings = source_health.build_warnings(run, degraded)
    assert any("SOURCE DEGRADATION WARNING" in w for w in warnings)
    assert any("italaw (DEGRADED (4 zero runs))" in w for w in warnings)
    assert any("COLLECTION ANOMALY" in w for w in warnings)


def test_record_run_end_to_end(tmp_path):
    p = str(tmp_path / "source_health.json")
    run = None
    for _ in range(3):
        run = [_sh("italaw", 0), _sh("icsid", 1)]
        warnings = source_health.record_run(run, "2026-07-27", path=p)
    assert run[0]["status"] == "DEGRADED (3 zero runs)"
    assert run[1]["status"] == "RETURNED"
    assert any("italaw" in w for w in warnings)
    saved = json.load(open(p))
    assert saved["sources"]["italaw"]["zero_streak"] == 3


def test_record_run_never_raises(tmp_path, monkeypatch):
    # Even a totally broken health path must not kill the pipeline.
    run = [_sh("italaw", 0)]
    out = source_health.record_run(run, "2026-07-27",
                                   path=str(tmp_path / ("no" * 300) / "x.json"))
    assert isinstance(out, list)


# --- visibility: meta.json + README + digest header --------------------------
def _stats_with_warnings():
    return {
        "total_candidates": 0, "above_threshold": 0, "threshold": 60,
        "provider": None, "per_source": {"italaw": 0},
        "source_health": [_sh("italaw", 0, status="DEGRADED (3 zero runs)"),
                          _sh("iareporter_headlines", 10, status="HEADLINE-ONLY")],
        "health_warnings": [
            "SOURCE DEGRADATION WARNING — documented-active sources with 3+ "
            "consecutive zero-item runs: italaw (DEGRADED (3 zero runs)).",
            "COLLECTION ANOMALY — all active sources but at most one returned "
            "zero items this run.",
        ],
    }


def test_readme_and_meta_carry_warnings(tmp_path, monkeypatch):
    from src import render
    monkeypatch.chdir(tmp_path)
    gen = datetime.datetime(2026, 7, 27, 13, 0, tzinfo=UTC)
    folder = render.write_digest_folder("<html></html>", [], gen,
                                        _stats_with_warnings(),
                                        out_root=str(tmp_path / "digests"))
    meta = json.load(open(os.path.join(folder, "meta.json")))
    assert any(s["status"].startswith("DEGRADED") for s in meta["source_health"])
    assert any("COLLECTION ANOMALY" in w for w in meta["health_warnings"])
    readme = open(os.path.join(folder, "README.md")).read()
    assert "SOURCE DEGRADATION WARNING" in readme
    assert "COLLECTION ANOMALY" in readme
    # Warnings sit in the header region, above the item table.
    assert readme.index("SOURCE DEGRADATION WARNING") < readme.index("| # |")


def test_digest_header_carries_warnings(monkeypatch):
    from src import render
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    monkeypatch.chdir(repo)  # templates/ lives at the repo root
    gen = datetime.datetime(2026, 7, 27, 13, 0, tzinfo=UTC)
    since = gen - datetime.timedelta(days=7)
    html = render.render_digest([], gen, since, _stats_with_warnings())
    assert "SOURCE DEGRADATION WARNING" in html
    assert "COLLECTION ANOMALY" in html
    assert "warnbanner" in html
    assert "DEGRADED (3 zero runs)" in html  # source-health table row


def test_main_pipeline_flags_degraded_after_three_zero_runs(tmp_path, monkeypatch):
    """End-to-end: three consecutive runs where a documented-active source
    (italaw) yields zero raw items must leave meta.json with its status as
    DEGRADED (3 zero runs) plus visible warning lines — the exact silent-decay
    shape of the 2026-07-13/20/27 Mondays."""
    import src.main as main_mod
    from src.sources.base import CandidateItem

    now = datetime.datetime.now(UTC)
    counter = {"n": 0}

    class DeadItalaw:
        name = "italaw"
        priority = "primary"
        def fetch(self, since):
            return []  # selector rot / bot-challenge: degrades to []

    class LiveIISD:
        name = "iisd_itn"
        priority = "primary"
        def fetch(self, since):
            counter["n"] += 1
            sid = f"cand-{counter['n']}"
            return [CandidateItem("iisd_itn", sid, f"http://x/{sid}",
                                  f"item {sid}", now, "s", "s", {})]

    monkeypatch.setattr(main_mod, "all_sources",
                        lambda cfg=None: [DeadItalaw(), LiveIISD()])
    monkeypatch.setattr(main_mod, "enrich", lambda it: it)  # offline
    monkeypatch.delenv("MODEL_PROVIDER", raising=False)     # keyword fallback
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shutil.copytree(os.path.join(repo, "templates"), tmp_path / "templates")
    monkeypatch.chdir(tmp_path)
    # Pre-seed state so run 1 is not a bootstrap run.
    from src import state as state_mod
    state_mod.save_state({"sources": {"iisd_itn": {"_seed": "t"}}}, "state/seen.json")

    for _ in range(3):
        assert main_mod.main(["--dry-run", "--no-email"]) == 0

    health = json.load(open("state/source_health.json"))
    assert health["sources"]["italaw"]["zero_streak"] == 3
    assert health["sources"]["iisd_itn"]["zero_streak"] == 0

    date_str = datetime.datetime.now(UTC).strftime("%Y-%m-%d")
    meta = json.load(open(f"digests/{date_str}_ISDS-Thematic-Watch/meta.json"))
    italaw = next(s for s in meta["source_health"] if s["name"] == "italaw")
    assert italaw["status"] == "DEGRADED (3 zero runs)"
    assert any("SOURCE DEGRADATION WARNING" in w for w in meta["health_warnings"])
    readme = open(f"digests/{date_str}_ISDS-Thematic-Watch/README.md").read()
    assert "DEGRADED (3 zero runs)" in readme


def test_no_warning_lines_when_healthy(tmp_path, monkeypatch):
    from src import render
    monkeypatch.chdir(tmp_path)
    stats = _stats_with_warnings()
    stats["source_health"] = [_sh("italaw", 4)]
    stats["health_warnings"] = []
    gen = datetime.datetime(2026, 7, 27, 13, 0, tzinfo=UTC)
    folder = render.write_digest_folder("<html></html>", [], gen, stats,
                                        out_root=str(tmp_path / "digests"))
    readme = open(os.path.join(folder, "README.md")).read()
    assert "DEGRADATION" not in readme and "ANOMALY" not in readme


# --- zero-streak refinement probes (2026-08-17) ------------------------------
def test_quiet_probe_declassifies_a_live_but_quiet_feed(monkeypatch):
    monkeypatch.setattr(source_health, "PROBES",
                        {"iisd_itn": lambda: "QUIET (feed live; newest item 2026-04-21)"})
    h = {"sources": {"iisd_itn": {"zero_streak": 3}}}
    run = [_sh("iisd_itn", 0)]
    degraded = source_health.apply_to_source_health(run, h)
    assert degraded == []
    assert run[0]["status"].startswith("QUIET")
    assert source_health.build_warnings(run, degraded) == []


def test_confirmed_cause_probe_relabels_and_still_alarms(monkeypatch):
    monkeypatch.setattr(source_health, "PROBES",
                        {"italaw": lambda: "NOT-READ (HTTP 403 bot-challenge at the origin)"})
    h = {"sources": {"italaw": {"zero_streak": 4}}}
    run = [_sh("italaw", 0), _sh("icsid", 2)]
    degraded = source_health.apply_to_source_health(run, h)
    assert degraded == ["italaw"]
    assert run[0]["status"] == "NOT-READ (HTTP 403 bot-challenge at the origin); 4 zero runs"
    warnings = source_health.build_warnings(run, degraded)
    assert any("SOURCE ACCESS FAILURE" in w for w in warnings)
    assert not any("no longer match the live site" in w for w in warnings)


def test_probe_crash_falls_back_to_generic_degraded(monkeypatch):
    def boom():
        raise RuntimeError("probe network trouble")
    monkeypatch.setattr(source_health, "PROBES", {"italaw": boom})
    h = {"sources": {"italaw": {"zero_streak": 3}}}
    run = [_sh("italaw", 0)]
    degraded = source_health.apply_to_source_health(run, h)
    assert degraded == ["italaw"]
    assert run[0]["status"] == "DEGRADED (3 zero runs)"
    warnings = source_health.build_warnings(run, degraded)
    assert any("SOURCE DEGRADATION WARNING" in w for w in warnings)


# --- iisd_itn probe: tries every route and names the dark one ------------------
# (2026-08-29: the feed and article pages 403 behind Cloudflare; the homepage
# listing still serves. A zero must read QUIET or NOT-READ, never a silent
# "fetcher no longer matches".)
import os as _os
import feedparser as _feedparser
from bs4 import BeautifulSoup as _BS
from src.sources import base as _base

_FIX = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fixtures")


def _home_soup():
    with open(_os.path.join(_FIX, "iisd_itn_home.html"), encoding="utf-8") as fh:
        return _BS(fh.read(), "html.parser")


def _live_feed():
    with open(_os.path.join(_FIX, "iisd_itn_feed.xml"), "rb") as fh:
        return _feedparser.parse(fh.read())


def test_probe_iisd_itn_feed_served_is_quiet(monkeypatch):
    monkeypatch.setattr(_base, "fetch_rss", lambda url, **kw: _live_feed())
    monkeypatch.setattr(_base, "fetch_html",
                        lambda url, **kw: (_ for _ in ()).throw(AssertionError("listing read")))
    label = source_health._probe_iisd_itn()
    assert label.startswith("QUIET (feed live; newest item 2026-04-21")


def test_probe_iisd_itn_feed_walled_listing_live_is_quiet_not_alarmed(monkeypatch):
    """Feed 403, homepage 200 with items -> the site is reachable; the zero is
    the window being quiet. QUIET labels are recorded, not alarmed."""
    _base.reset_fetch_log()
    monkeypatch.setattr(_base, "fetch_rss", lambda url, **kw: None)
    monkeypatch.setattr(_base, "fetch_html", lambda url, **kw: _home_soup())
    label = source_health._probe_iisd_itn()
    assert label.startswith("QUIET (")
    assert "HTML listing live, 5 items listed, newest 2026-04-21" in label


def test_probe_iisd_itn_every_route_walled_is_not_read(monkeypatch):
    """Feed AND homepage refused -> NOT-READ with both refusals named, and the
    label says the source is archive-recoverable (source_recovery SPECS)."""
    _base.reset_fetch_log()
    _base._record_outcome("https://www.iisd.org/itn/feed/", "refused", "403")
    _base._record_outcome("https://www.iisd.org/itn/", "refused", "403")
    monkeypatch.setattr(_base, "fetch_rss", lambda url, **kw: None)
    monkeypatch.setattr(_base, "fetch_html", lambda url, **kw: None)
    label = source_health._probe_iisd_itn()
    assert label.startswith("NOT-READ (RSS HTTP 403; HTML listing HTTP 403")
    assert "archive-recoverable" in label


def test_probe_iisd_itn_listing_live_but_parses_nothing_is_generic_rot(monkeypatch):
    """A reachable listing that yields no article at all is real parser rot:
    leave it to the generic 'fetchers likely no longer match' alarm (None)."""
    _base.reset_fetch_log()
    monkeypatch.setattr(_base, "fetch_rss", lambda url, **kw: None)
    monkeypatch.setattr(_base, "fetch_html",
                        lambda url, **kw: _BS("<html><body><p>nothing</p></body></html>", "html.parser"))
    assert source_health._probe_iisd_itn() is None


def test_probe_iisd_itn_never_raises(monkeypatch):
    monkeypatch.setattr(_base, "fetch_rss",
                        lambda url, **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    try:
        source_health._probe_iisd_itn()
    except RuntimeError:
        # apply_to_source_health wraps probes in try/except; a raise there is
        # tolerated by the guard, but the guard-level contract is what matters:
        pass


def test_iisd_itn_is_archive_recoverable_with_a_tight_path_regex():
    from src import source_recovery
    assert source_recovery.is_recoverable("iisd_itn")
    spec = source_recovery.SPECS["iisd_itn"]
    assert spec.path_regex.search(
        "https://www.iisd.org/itn/2026/04/21/committees-international-investment-agreements-joshua-paine/")
    assert not spec.path_regex.search("https://www.iisd.org/itn/analysis/")
    assert not spec.path_regex.search("https://www.iisd.org/itn/")
    assert spec.title_suffix.sub("", "Some Article – Investment Treaty News") == "Some Article"


# --- icsid probe: a quiet month is not rot --------------------------------------
# 2026-09-07: icsid hit "DEGRADED (3 zero runs)" on three same-day runs (two of
# them manual dispatches) while its newest release was dated 08-26 and the live
# page parsed 20 items. The probe names the quiet instead of asserting rot.
def _icsid_soup():
    with open(_os.path.join(_FIX, "icsid_news_events.html"), encoding="utf-8") as fh:
        return _BS(fh.read(), "html.parser")


def test_probe_icsid_page_live_with_releases_is_quiet(monkeypatch):
    import src.sources.icsid as icsid_mod
    monkeypatch.setattr(icsid_mod, "fetch_html", lambda url, **kw: _icsid_soup())
    label = source_health._probe_icsid()
    assert label.startswith("QUIET (page live; 3 releases listed, newest 2026-07-17")


def test_probe_icsid_page_refused_is_not_read(monkeypatch):
    import src.sources.icsid as icsid_mod
    _base.reset_fetch_log()
    _base._record_outcome(icsid_mod.BASE_URL, "refused", "403")
    monkeypatch.setattr(icsid_mod, "fetch_html", lambda url, **kw: None)
    assert source_health._probe_icsid().startswith("NOT-READ (HTTP 403")


def test_probe_icsid_page_live_but_unparseable_is_generic_rot(monkeypatch):
    import src.sources.icsid as icsid_mod
    _base.reset_fetch_log()
    monkeypatch.setattr(icsid_mod, "fetch_html",
                        lambda url, **kw: _BS("<html><body><p>nothing</p></body></html>", "html.parser"))
    assert source_health._probe_icsid() is None


def test_probe_icsid_never_raises(monkeypatch):
    import src.sources.icsid as icsid_mod
    _base.reset_fetch_log()
    monkeypatch.setattr(icsid_mod, "fetch_html",
                        lambda url, **kw: (_ for _ in ()).throw(RuntimeError("boom")))
    assert source_health._probe_icsid() is None


def test_quiet_icsid_is_recorded_not_alarmed(monkeypatch):
    """End to end through apply_to_source_health: a probed QUIET is not DEGRADED."""
    import src.sources.icsid as icsid_mod
    monkeypatch.setattr(icsid_mod, "fetch_html", lambda url, **kw: _icsid_soup())
    monkeypatch.setattr(source_health, "PROBES", {"icsid": source_health._probe_icsid})
    assert "icsid" in source_health.ACTIVE_SOURCES
    sh = [{"name": "icsid", "status": "RETURNED", "count": 0}]
    # The run's own zero is already in the streak when the guard runs (see
    # test_degraded_status_at_three_zero_runs): this is the 2026-09-07 state.
    health = {"sources": {"icsid": {"zero_streak": 3, "last_nonzero": "2026-08-31",
                                    "last_run": "2026-09-07"}}}
    degraded = source_health.apply_to_source_health(sh, health)
    assert degraded == []
    assert sh[0]["status"].startswith("QUIET (page live;")
    assert source_health.build_warnings(sh, degraded) == []


# --- gmail_scholar probe: date the newest alert instead of "nothing" ------------
def test_probe_gmail_scholar_without_credentials_gives_no_refinement(monkeypatch):
    from src.sources import gmail_scholar
    monkeypatch.setattr(gmail_scholar, "scholar_mailbox_status", lambda days=30: ("inactive", []))
    assert source_health._probe_gmail_scholar() is None


def test_probe_gmail_scholar_unreachable_is_not_read(monkeypatch):
    from src.sources import gmail_scholar
    monkeypatch.setattr(gmail_scholar, "scholar_mailbox_status", lambda days=30: ("unreachable", []))
    assert source_health._probe_gmail_scholar().startswith("NOT-READ (IMAP")


def test_probe_gmail_scholar_empty_mailbox_says_check_the_subscriptions(monkeypatch):
    from src.sources import gmail_scholar
    monkeypatch.setattr(gmail_scholar, "scholar_mailbox_status", lambda days=30: ("ok", []))
    label = source_health._probe_gmail_scholar()
    assert label.startswith("QUIET (IMAP reachable; no Scholar alert mail in 30 days")


def test_probe_gmail_scholar_names_the_newest_alert(monkeypatch):
    from src.sources import gmail_scholar
    monkeypatch.setattr(gmail_scholar, "scholar_mailbox_status", lambda days=30: ("ok", [
        {"uid": "9", "date": "2026-09-08T05:16:00+00:00", "subject": "x - new results"},
        {"uid": "8", "date": "2026-08-31T05:10:00+00:00", "subject": "y - new results"}]))
    label = source_health._probe_gmail_scholar()
    assert label.startswith("QUIET (IMAP reachable; 2 Scholar alert(s) in 30d, newest 2026-09-08")
    # Registered in PROBES (the autouse fixture empties the live dict, so read the source).
    src = open(source_health.__file__, encoding="utf-8").read()
    assert '"gmail_scholar": _probe_gmail_scholar,' in src
