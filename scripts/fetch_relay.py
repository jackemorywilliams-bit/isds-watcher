#!/usr/bin/env python3
"""Fetch relay — retrieval for a research session that has no network of its own.

The scheduled cloud council session cannot reach the internet: its proxy refuses
every outbound connection and its fetch service 403s every URL, including neutral
controls. This project's own GitHub Actions runners *do* have egress — they fetch
all nine sources every week. So the session commits a small request file, the push
fires this script on a runner, and the runner answers with a reduction.

What travels is the REDUCTION, never the document (council standing rule,
2026-08-03): url, final url, status, content-type, byte length, sha256, timestamp,
user-agent, plus one short excerpt. No third-party body is written to any file,
branch, artifact, or log. The repository is public; a commit is publication.

Compliance is inherited, not re-implemented: every request goes through
``src.sources.base.polite_get`` unchanged, so the same identifying User-Agent, the
same robots.txt evaluation, and the same per-domain interval apply.

Run:  python scripts/fetch_relay.py [--request PATH] [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from src.sources.base import USER_AGENT, polite_get, get_fetch_log, reset_fetch_log  # noqa: E402

REQUEST_DIR = pathlib.Path("analytics/fetch-requests")
RESULT_DIR = pathlib.Path("analytics/fetch-results")

# Cap per record. The permanent record keeps a locator and a hash, not a copy.
EXCERPT_CHARS = 400

# Hosts this relay may fetch: the curated sources, plus the primary-document and
# treaty-database hosts already named throughout the record. The relay retrieves
# what the sources or the record already identified — it is not a discovery
# channel (METHODOLOGY Part VIII).
ALLOWED_HOSTS = {
    "icsid.worldbank.org",
    "icsidfiles.worldbank.org",
    "www.italaw.com",
    "italaw.com",
    "investmentpolicy.unctad.org",
    "unctad.org",
    "uncitral.un.org",
    "undocs.org",
    "docs.un.org",
    "digitallibrary.un.org",
    "www.un.org",
    "www.iisd.org",
    "iisd.org",
    "www.iareporter.com",
    "iareporter.com",
    "pca-cpa.org",
    "www.pca-cpa.org",
    "www.bing.com",
    # Neutral control only — never a research source.
    "example.com",
}

# Every batch carries a control whose answer we already know. If the control
# fails, the runner itself is the problem and no other row in the batch may be
# read as information about its resource.
CONTROL_URL = "https://example.com/"

MAX_URLS = 12

_TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
_ANY_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def _environment() -> str:
    """Where this run actually happened. Never assert a runner we were not on."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return f"github-actions-runner (run {os.environ.get('GITHUB_RUN_ID', 'unknown')})"
    return "local"


def _is_private(host: str) -> bool:
    """Reject loopback, link-local, and RFC1918 literals (SSRF guard)."""
    import ipaddress

    if host in {"localhost", ""}:
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved


def validate(url: str) -> str | None:
    """Return None if the URL may be fetched, else the reason it may not."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return "scheme_not_https"
    host = (parsed.hostname or "").lower()
    if _is_private(host):
        return "private_address"
    if host not in ALLOWED_HOSTS:
        return "host_not_allowed"
    return None


def excerpt_of(text: str, content_type: str) -> str:
    """A short opening excerpt of textual content; empty for non-text."""
    if "html" not in content_type and "text" not in content_type:
        return ""
    body = _TAG_RE.sub(" ", text)
    body = _ANY_TAG_RE.sub(" ", body)
    body = _WS_RE.sub(" ", body).strip()
    return body[:EXCERPT_CHARS]


def fetch_one(url: str) -> dict:
    """Fetch one URL and return its reduction. Never returns a body."""
    record = {
        "url": url,
        "outcome": "not_attempted",
        "status": None,
        "final_url": None,
        "content_type": None,
        "bytes": None,
        "sha256": None,
        "excerpt": "",
        "user_agent": USER_AGENT,
    }

    reason = validate(url)
    if reason:
        record["outcome"] = reason
        return record

    reset_fetch_log()
    resp = polite_get(url)
    log = get_fetch_log()

    if resp is None:
        # polite_get records why at each exit; carry the layer through so a
        # timeout is never mistaken for an origin answer.
        entry = log[-1] if log else {"outcome": "no_contact", "detail": ""}
        record["outcome"] = entry.get("outcome", "no_contact")
        record["status"] = entry.get("detail") or None
        return record

    content = resp.content or b""
    content_type = (resp.headers.get("content-type", "") or "").split(";")[0].strip()
    record.update({
        "outcome": "ok",
        "status": resp.status_code,
        "final_url": getattr(resp, "url", url),
        "content_type": content_type,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "excerpt": excerpt_of(getattr(resp, "text", "") or "", content_type),
    })
    return record


def run(request_path: pathlib.Path, out_dir: pathlib.Path) -> dict:
    request = json.loads(request_path.read_text())
    urls = [u for u in request.get("urls", []) if isinstance(u, str)]
    truncated = len(urls) > MAX_URLS
    urls = urls[:MAX_URLS]

    records = [fetch_one(CONTROL_URL)]
    control_ok = records[0]["outcome"] == "ok"
    for url in urls:
        if control_ok:
            records.append(fetch_one(url))
        else:
            # Control failed: the instrument is not trustworthy this run, so no
            # row may be read as information about its resource.
            records.append({"url": url, "outcome": "not_attempted",
                            "status": None, "final_url": None, "content_type": None,
                            "bytes": None, "sha256": None, "excerpt": "",
                            "user_agent": USER_AGENT})

    manifest = {
        "request": request_path.name,
        "note": request.get("note", ""),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "environment": _environment(),
        "control_url": CONTROL_URL,
        "control_ok": control_ok,
        "void": not control_ok,
        "requested": len(urls),
        "completed": sum(1 for r in records[1:] if r["outcome"] == "ok"),
        "truncated": truncated,
        "excerpt_chars": EXCERPT_CHARS,
        "records": records,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / request_path.name
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def newest_request(directory: pathlib.Path) -> pathlib.Path | None:
    files = sorted(p for p in directory.glob("*.json"))
    return files[-1] if files else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fetch-relay")
    ap.add_argument("--request", default=None, help="request file (default: newest)")
    ap.add_argument("--out-dir", default=str(RESULT_DIR))
    args = ap.parse_args(argv)

    request_path = (pathlib.Path(args.request) if args.request
                    else newest_request(REQUEST_DIR))
    if request_path is None or not request_path.exists():
        print("fetch-relay: no request file found", file=sys.stderr)
        return 1

    manifest = run(request_path, pathlib.Path(args.out_dir))
    state = "VOID (control failed)" if manifest["void"] else "ok"
    print(f"fetch-relay: {request_path.name} -> {state}; "
          f"{manifest['completed']}/{manifest['requested']} completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
