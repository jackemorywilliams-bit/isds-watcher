"""The fetch relay must answer with a reduction and never with a document.

The repository is public, so a commit is publication. The relay therefore ships
url, status, size, sha256 and a short excerpt — never a body (council standing
rule, 2026-08-03). These tests pin that, plus the guards that keep the relay a
retrieval instrument rather than an open proxy.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from scripts import fetch_relay


# --- what may be fetched ----------------------------------------------------

@pytest.mark.parametrize("url", [
    "http://icsid.worldbank.org/x",          # not https
    "https://evil.example.org/x",            # host not on the allowlist
    "https://127.0.0.1/x",                   # loopback
    "https://169.254.169.254/latest/meta",   # cloud metadata endpoint
    "https://10.0.0.5/internal",             # RFC1918
])
def test_disallowed_urls_are_refused_before_any_request(url):
    assert fetch_relay.validate(url) is not None


@pytest.mark.parametrize("url", [
    "https://icsid.worldbank.org/cases/case-database",
    "https://investmentpolicy.unctad.org/international-investment-agreements",
    "https://uncitral.un.org/en/commission",
])
def test_record_hosts_are_allowed(url):
    assert fetch_relay.validate(url) is None


def test_refused_url_still_gets_a_record(monkeypatch):
    """A URL that is never attempted must appear in the manifest, not vanish."""
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: None)
    rec = fetch_relay.fetch_one("https://evil.example.org/x")
    assert rec["url"] == "https://evil.example.org/x"
    assert rec["outcome"] == "host_not_allowed"
    assert rec["sha256"] is None


# --- what comes back --------------------------------------------------------

class _Resp:
    def __init__(self, body: bytes, content_type="text/html", status=200, url=None):
        self.content = body
        self.text = body.decode("utf-8", "replace")
        self.status_code = status
        self.headers = {"content-type": content_type}
        self.url = url or "https://example.com/"


def test_excerpt_is_capped_and_strips_markup():
    long_text = "<p>" + ("Tribunal reasoning. " * 200) + "</p>"
    out = fetch_relay.excerpt_of(long_text, "text/html")
    assert len(out) <= fetch_relay.EXCERPT_CHARS
    assert "<p>" not in out


def test_scripts_and_styles_are_not_excerpted():
    html = "<style>.a{color:red}</style><script>var x=1;</script><p>Real text here.</p>"
    out = fetch_relay.excerpt_of(html, "text/html")
    assert "Real text here." in out
    assert "color:red" not in out and "var x" not in out


def test_binary_content_yields_no_excerpt():
    assert fetch_relay.excerpt_of("%PDF-1.7 ...", "application/pdf") == ""


def test_record_carries_hash_and_size_but_no_body(monkeypatch):
    body = b"<p>" + b"x" * 5000 + b"</p>"
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: _Resp(body))
    monkeypatch.setattr(fetch_relay, "get_fetch_log", lambda: [])
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)

    rec = fetch_relay.fetch_one("https://icsid.worldbank.org/x")

    assert rec["outcome"] == "ok"
    assert rec["bytes"] == len(body)
    assert len(rec["sha256"]) == 64
    assert len(rec["excerpt"]) <= fetch_relay.EXCERPT_CHARS
    # The body itself must not appear anywhere in the record.
    assert "x" * 1000 not in json.dumps(rec)


def test_failure_layer_is_preserved(monkeypatch):
    """A timeout must not be recorded as an origin answer."""
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: None)
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)
    monkeypatch.setattr(fetch_relay, "get_fetch_log",
                        lambda: [{"outcome": "no_contact", "detail": "timeout"}])

    rec = fetch_relay.fetch_one("https://uncitral.un.org/x")
    assert rec["outcome"] == "no_contact"
    assert rec["status"] == "timeout"


# --- batch behaviour --------------------------------------------------------

def _write_request(tmp_path: pathlib.Path, urls) -> pathlib.Path:
    p = tmp_path / "2026-08-03-1.json"
    p.write_text(json.dumps({"urls": urls, "note": "test"}))
    return p


def test_failed_control_voids_the_whole_batch(tmp_path, monkeypatch):
    """If the control fails the runner is suspect, so nothing may be read."""
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: None)
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)
    monkeypatch.setattr(fetch_relay, "get_fetch_log",
                        lambda: [{"outcome": "no_contact", "detail": "timeout"}])

    req = _write_request(tmp_path, ["https://icsid.worldbank.org/x"])
    manifest = fetch_relay.run(req, tmp_path / "out")

    assert manifest["void"] is True
    assert manifest["control_ok"] is False
    assert manifest["records"][1]["outcome"] == "not_attempted"


def test_every_requested_url_appears_in_the_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: _Resp(b"<p>ok</p>"))
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)
    monkeypatch.setattr(fetch_relay, "get_fetch_log", lambda: [])

    urls = ["https://icsid.worldbank.org/a", "https://www.italaw.com/b"]
    manifest = fetch_relay.run(_write_request(tmp_path, urls), tmp_path / "out")

    recorded = [r["url"] for r in manifest["records"]]
    for u in urls:
        assert u in recorded
    assert manifest["requested"] == 2


def test_oversized_batch_is_truncated_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: _Resp(b"<p>ok</p>"))
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)
    monkeypatch.setattr(fetch_relay, "get_fetch_log", lambda: [])

    urls = [f"https://icsid.worldbank.org/{i}" for i in range(fetch_relay.MAX_URLS + 5)]
    manifest = fetch_relay.run(_write_request(tmp_path, urls), tmp_path / "out")

    assert manifest["truncated"] is True
    assert manifest["requested"] == fetch_relay.MAX_URLS


def test_manifest_is_written_to_disk(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch_relay, "polite_get", lambda url: _Resp(b"<p>ok</p>"))
    monkeypatch.setattr(fetch_relay, "reset_fetch_log", lambda: None)
    monkeypatch.setattr(fetch_relay, "get_fetch_log", lambda: [])

    out = tmp_path / "out"
    fetch_relay.run(_write_request(tmp_path, ["https://icsid.worldbank.org/a"]), out)
    written = json.loads((out / "2026-08-03-1.json").read_text())
    assert written["excerpt_chars"] == fetch_relay.EXCERPT_CHARS
    assert written["fetched_at"].endswith("+00:00")


def test_environment_is_detected_never_asserted(monkeypatch):
    """A local run must not claim it happened on a runner."""
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    assert fetch_relay._environment() == "local"

    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_RUN_ID", "12345")
    assert "github-actions-runner" in fetch_relay._environment()
    assert "12345" in fetch_relay._environment()
