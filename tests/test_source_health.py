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
