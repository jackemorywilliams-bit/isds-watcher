"""A refused source must never report as healthy.

`polite_get` returns None for every failure — robots-disallow, timeout, 403,
connection error — so for four consecutive weeks italaw was 403'd from CI and
every digest recorded it as RETURNED, count 0: indistinguishable from a source
that was simply quiet. These tests pin the fix: the fetcher records what
happened at each exit, and the pipeline reads those outcomes.

The status wording is deliberate. NOT-READ says only what WE could read; it
never asserts the source is broken, because a 403 to our runner may be our own
IP class (council standing rule, 2026-08-03).
"""

from __future__ import annotations

import pytest

from src.sources import base


@pytest.fixture(autouse=True)
def _clean_log():
    base.reset_fetch_log()
    yield
    base.reset_fetch_log()


class _Resp:
    def __init__(self, status_code):
        self.status_code = status_code
        self.text = ""
        self.content = b""


def _fake_requests(monkeypatch, *, status=None, raises=None):
    """Install a stub `requests` module for polite_get to import."""
    import sys
    import types

    mod = types.ModuleType("requests")

    class _Timeout(Exception):
        pass

    class _ReqExc(Exception):
        pass

    mod.exceptions = types.SimpleNamespace(Timeout=_Timeout, RequestException=_ReqExc)

    def _get(url, headers=None, timeout=None):
        if raises == "timeout":
            raise _Timeout("timed out")
        if raises == "conn":
            raise _ReqExc("connection refused")
        return _Resp(status)

    mod.get = _get
    monkeypatch.setitem(sys.modules, "requests", mod)
    return mod


def test_non_200_is_recorded_as_refused(monkeypatch):
    _fake_requests(monkeypatch, status=403)
    monkeypatch.setattr(base, "robots_allowed", lambda url: True)
    monkeypatch.setattr(base, "_respect_rate_limit", lambda domain: None)

    assert base.polite_get("https://www.italaw.com/") is None

    log = base.get_fetch_log()
    assert len(log) == 1
    assert log[0]["outcome"] == "refused"
    assert log[0]["detail"] == "403"


def test_success_is_recorded_so_partial_reads_stay_healthy(monkeypatch):
    _fake_requests(monkeypatch, status=200)
    monkeypatch.setattr(base, "robots_allowed", lambda url: True)
    monkeypatch.setattr(base, "_respect_rate_limit", lambda domain: None)

    assert base.polite_get("https://example.com/") is not None
    assert base.get_fetch_log()[0]["outcome"] == "ok"


@pytest.mark.parametrize("raises,detail", [("timeout", "timeout"), ("conn", "_ReqExc")])
def test_no_contact_is_distinguished_from_an_origin_answer(monkeypatch, raises, detail):
    """A timeout is not an origin answer — the layers must stay separable."""
    _fake_requests(monkeypatch, raises=raises)
    monkeypatch.setattr(base, "robots_allowed", lambda url: True)
    monkeypatch.setattr(base, "_respect_rate_limit", lambda domain: None)

    assert base.polite_get("https://example.com/") is None
    entry = base.get_fetch_log()[0]
    assert entry["outcome"] == "no_contact"
    assert entry["detail"] == detail


def test_robots_disallow_is_its_own_outcome(monkeypatch):
    _fake_requests(monkeypatch, status=200)
    monkeypatch.setattr(base, "robots_allowed", lambda url: False)

    assert base.polite_get("https://news.google.com/rss/search?q=x") is None
    assert base.get_fetch_log()[0]["outcome"] == "robots_disallowed"


def test_reset_clears_between_sources():
    base._record_outcome("https://a.test/", "refused", "403")
    assert base.get_fetch_log()
    base.reset_fetch_log()
    assert base.get_fetch_log() == []


# --- pipeline-level: the status a digest actually records -------------------

def _status_for(outcomes, items, *, failed=False, headline_only=False):
    """Mirror of the status decision in src/main.py, exercised directly.

    Kept in lockstep with main.py by test_refused_source_reports_not_read,
    which drives the real pipeline.
    """
    refusals = [o for o in outcomes
                if o["outcome"] in ("refused", "no_contact", "robots_disallowed")]
    reached = any(o["outcome"] == "ok" for o in outcomes)
    if failed:
        return "FAILED"
    if refusals and not reached and not items:
        reason = refusals[0]["detail"] or refusals[0]["outcome"]
        return f"NOT-READ ({reason})"
    if headline_only:
        return "HEADLINE-ONLY"
    return "RETURNED"


def test_blocked_source_is_not_reported_as_returned():
    """The italaw case: every request refused, nothing yielded."""
    outcomes = [{"url": "https://www.italaw.com/", "outcome": "refused", "detail": "403"}]
    assert _status_for(outcomes, items=[]) == "NOT-READ (403)"


def test_genuinely_quiet_source_still_reads_as_returned():
    """A source we reached that simply had nothing new must stay RETURNED."""
    outcomes = [{"url": "https://icsid.worldbank.org/news", "outcome": "ok", "detail": "200"}]
    assert _status_for(outcomes, items=[]) == "RETURNED"


def test_partial_refusal_with_a_successful_read_is_not_not_read():
    """One dead sub-page must not condemn a source we did read."""
    outcomes = [
        {"url": "https://iisd.org/a", "outcome": "refused", "detail": "404"},
        {"url": "https://iisd.org/b", "outcome": "ok", "detail": "200"},
    ]
    assert _status_for(outcomes, items=[]) == "RETURNED"


def test_status_never_asserts_a_source_defect():
    """Wording guard: the label reports our reading, not the source's health."""
    outcomes = [{"url": "https://www.italaw.com/", "outcome": "refused", "detail": "403"}]
    status = _status_for(outcomes, items=[])
    lowered = status.lower()
    assert "not-read" in lowered
    for forbidden in ("blocked", "broken", "down", "dead"):
        assert forbidden not in lowered
