"""Autonomous access-failure recovery via the Internet Archive.

When a documented-active source's origin refuses the runner — a *confirmed*
NOT-READ, i.e. we attempted HTTP, were refused (a Cloudflare 403), and yielded
nothing — the pipeline does not accept the blackout. It reads the same content
pages from the Internet Archive, which captures them within days. This module
is the shared engine; the pipeline guard in ``src/main.py`` invokes it for any
zero-and-NOT-READ source listed in ``SPECS``.

Adding archive resilience to a new source is one ``SPEC`` entry — no bespoke
fetcher, no new code path. Verified live 2026-08-17: italaw (18 case pages) and
unctad_isds (recent cases with real slugs) both recover this way.

WHEN A SOURCE BELONGS IN ``SPECS``. Only when a live zero *reliably* means
BLOCKED, never quiet: a content database behind a hard wall. italaw and
unctad_isds 403 unconditionally and always have content, so a live zero from
them is always a block. A genuinely quiet feed (iisd_itn — a quarterly
publication) must NOT be listed: recovering it would surface stale archived
pages on a legitimately empty week. The pipeline guard's trigger is doubly
safe — it fires only when the fetch loop already recorded a NOT-READ refusal,
not on a plain zero.

Guarantees: never raises (any CDX/snapshot failure logs and yields whatever was
gathered, possibly []); polite (all requests go through ``polite_get`` — robots
and the per-domain rate limit apply, and web.archive.org is a distinct domain
from the walled origin); honest (candidates are keyed to the REAL origin URL so
the operator's link is canonical, the capture lag is disclosed and logged, and
any per-run cap logs its overflow rather than silently cutting).
"""

from __future__ import annotations

import html as _html
import json
import logging
import re
from dataclasses import dataclass
from datetime import timedelta

from .sources.base import CandidateItem, polite_get, utcnow

logger = logging.getLogger("isds.source_recovery")

_CDX_URL = (
    "http://web.archive.org/cdx/search/cdx"
    "?url={prefix}&matchType=prefix"
    "&filter=statuscode:200&filter=mimetype:text/html"
    "&collapse=urlkey&output=json&from={frm}&limit=400"
)
_WB_SNAPSHOT = "http://web.archive.org/web/{ts}/{url}"
_WB_TOOLBAR_END = "<!-- End Wayback Rewrite JS Include -->"

_GENERIC_TITLES = {
    "", "view case details", "view details", "case details", "details",
    "read more", "more", "view document", "view", "download",
}


@dataclass(frozen=True)
class RecoverySpec:
    """How to recover one source from the Internet Archive.

    ``cdx_prefix``   Wayback CDX url-prefix for the source's content pages.
    ``path_regex``   which captured URL paths are real content pages (excludes
                     index/browse/list pages that would add noise).
    ``title_suffix`` trailing site-name boilerplate to strip from <title>.
    ``lookback_days` how far back on CAPTURE date to look (the Archive lags
                     publication; seen-state prevents re-surfacing).
    ``max_items``    per-run snapshot-fetch cap; overflow is logged, not cut.
    """
    cdx_prefix: str
    path_regex: "re.Pattern[str]"
    title_suffix: "re.Pattern[str]"
    lookback_days: int = 45
    max_items: int = 25


SPECS: dict[str, RecoverySpec] = {
    "italaw": RecoverySpec(
        cdx_prefix="italaw.com/cases",
        path_regex=re.compile(r"/cases/(?:documents/)?[0-9]+$"),
        title_suffix=re.compile(r"\s*\|\s*italaw\s*$", re.I),
    ),
    "unctad_isds": RecoverySpec(
        cdx_prefix="investmentpolicy.unctad.org/investment-dispute-settlement/cases",
        path_regex=re.compile(r"/cases/[0-9]+/[^/?#]+$"),
        title_suffix=re.compile(
            r"\s*\|\s*Investment Dispute Settlement Navigator.*$", re.I),
    ),
}


def is_recoverable(name: str) -> bool:
    return name in SPECS


def _canonical(url: str) -> str:
    url = re.sub(r"^http://", "https://", url)
    return re.sub(r"^https://italaw\.com", "https://www.italaw.com", url)


def _title(html_text: str, spec: RecoverySpec) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.S | re.I)
    if not m:
        return ""
    raw = re.sub(r"\s+", " ", m.group(1)).strip()
    raw = spec.title_suffix.sub("", raw).strip()
    return "" if raw.lower() in _GENERIC_TITLES else raw


def _body(html_text: str) -> str:
    end = html_text.find(_WB_TOOLBAR_END)
    if end > 0:
        html_text = html_text[end + len(_WB_TOOLBAR_END):]
    html_text = re.sub(r"<script.*?</script>", " ", html_text, flags=re.S | re.I)
    html_text = re.sub(r"<style.*?</style>", " ", html_text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html_text)
    try:
        text = _html.unescape(text)
    except Exception:  # noqa: BLE001
        pass
    return re.sub(r"\s+", " ", text).strip()


def _snapshot_item(name: str, spec: RecoverySpec, ts: str, original: str
                   ) -> "CandidateItem | None":
    resp = polite_get(_WB_SNAPSHOT.format(ts=ts, url=original))
    if resp is None:
        return None
    html_text = getattr(resp, "text", "") or ""
    title = _title(html_text, spec)
    if not title:
        return None
    body = _body(html_text)
    canonical = _canonical(original)
    return CandidateItem(
        source=name,
        source_id=canonical,
        url=canonical,
        title=title,
        published=None,                    # capture date != decision date
        summary=body[:300],
        raw_text=(title + "\n\n" + body)[:4000],
        metadata={
            "date_inferred": True,         # unknown; rely on seen-state
            "retrieved_via": "internet-archive",
            "wayback_capture": ts,
            # The origin will 403 a re-fetch; the snapshot body IS the body, so
            # enrich must keep it rather than throw it away on a certain 403.
            "body_final": True,
        },
    )


def recover(name: str, since=None) -> list[CandidateItem]:
    """Read a blocked source's content pages from the Internet Archive.

    Returns candidates keyed to the real origin URL. Never raises. ``since`` is
    accepted for signature symmetry with ``Source.fetch`` and is not used to
    filter (capture date is not decision date); seen-state dedups downstream.
    """
    spec = SPECS.get(name)
    if spec is None:
        return []
    frm = (utcnow() - timedelta(days=spec.lookback_days)).strftime("%Y%m%d")
    resp = polite_get(_CDX_URL.format(prefix=spec.cdx_prefix, frm=frm))
    if resp is None:
        logger.warning("%s: CDX index unavailable, no recovery this run", name)
        return []
    try:
        rows = json.loads(getattr(resp, "text", "") or "[]")
    except ValueError:
        logger.warning("%s: CDX returned non-JSON, no recovery this run", name)
        return []
    if rows and rows[0] and rows[0][0] == "urlkey":
        rows = rows[1:]

    captures: dict[str, tuple[str, str]] = {}
    for r in rows:
        try:
            ts, original = r[1], r[2]
        except (IndexError, TypeError):
            continue
        if not spec.path_regex.search(original):
            continue
        key = original.rstrip("/")
        if key not in captures or ts > captures[key][0]:
            captures[key] = (ts, original)

    ordered = sorted(captures.values(), key=lambda t: t[0], reverse=True)
    if len(ordered) > spec.max_items:
        logger.info("%s: %d captured content pages; fetching the %d most "
                    "recently archived (the rest wait for a later run)",
                    name, len(ordered), spec.max_items)
        ordered = ordered[:spec.max_items]

    items: list[CandidateItem] = []
    for ts, original in ordered:
        item = _snapshot_item(name, spec, ts, original)
        if item is not None:
            items.append(item)
    logger.info("%s: recovered %d content page(s) from the Internet Archive "
                "(capture lag applies; not a live read)", name, len(items))
    return items
