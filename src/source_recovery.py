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

WHEN A SOURCE BELONGS IN ``SPECS``. When a confirmed refusal reliably means
BLOCKED: a content database behind a hard wall. italaw and unctad_isds 403
unconditionally and always have content. iisd_itn was deliberately EXCLUDED
until 2026-08-29 because its zeros used to mean "quarterly journal, quiet
quarter" and recovering it would have surfaced stale archived pages on a
legitimately empty week. That premise expired: its feed and article pages now
sit behind a Cloudflare bot-challenge, so a refusal from it is a real block.
It is safe to list because the trigger is doubly gated — the fetcher tries
the (still-served) homepage listing first, and this recovery fires only when
the fetch loop recorded a NOT-READ refusal on every route, never on a plain
zero. A quiet quarter therefore still never reaches the Archive.

Guarantees: never raises (any CDX/snapshot failure logs and yields whatever was
gathered, possibly []); polite (all requests go through ``polite_get`` — robots
and the per-domain rate limit apply, and web.archive.org is a distinct domain
from the walled origin); honest (candidates are keyed to the REAL origin URL so
the operator's link is canonical, the capture lag is disclosed and logged, and
any per-run cap logs its overflow rather than silently cutting).

``recover_with_report`` returns that disclosure as data rather than only as a
log line — see ``RecoveryReport`` — so a run's meta.json can carry how much of
the Archive's offer the cap left behind and how old the snapshots were.
``recover`` is the same read without the report.
"""

from __future__ import annotations

import html as _html
import json
import logging
import re
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .sources.base import CandidateItem, polite_get, utcnow

logger = logging.getLogger("isds.source_recovery")

# web.archive.org rate-limits a single IP hard: a CI runner that has just pulled
# a burst of snapshots (recovering one source) gets its next request refused
# (connection reset / "connection refused") for up to a minute. That is exactly
# what stranded the SECOND recovered source on 2026-08-17 — italaw's 17 snapshots
# exhausted the runner's archive.org goodwill and unctad's CDX call was refused.
# So: the CDX call (the critical one — without it a source recovers nothing)
# retries with backoff, giving archive.org time to un-block; and each source's
# per-run snapshot cap is small enough that two sources fit under the limit,
# with the remainder deferred to a later run (seen-state carries it).
_CDX_RETRY_BACKOFF_S = (20, 40)   # waits before retry 2 and retry 3

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
    max_items: int = 12


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
    # Added 2026-08-29. ITN's feed AND its article pages now answer with a
    # Cloudflare bot-challenge (HTTP 403); only the homepage listing serves.
    # The fetcher reads that listing first (headline-level), so this entry is
    # reached only when BOTH routes are refused — a confirmed NOT-READ, never a
    # quiet quarter — and it is the only route to the article BODIES.
    "iisd_itn": RecoverySpec(
        cdx_prefix="iisd.org/itn/",
        path_regex=re.compile(r"/itn/(?:en/)?[0-9]{4}/[0-9]{2}/[0-9]{2}/[^/?#]+/?$"),
        title_suffix=re.compile(r"\s*(?:\u2013|\u2014|-|\|)\s*Investment Treaty News.*$", re.I),
    ),
}


def is_recoverable(name: str) -> bool:
    return name in SPECS


@dataclass(frozen=True)
class RecoveryReport:
    """What one archive recovery did, and how stale the pages it read are.

    A RECOVERED source used to report a single number — the item count — which
    says nothing about the two things a reader of a recovered digest needs to
    know: how much of the Archive's offer the per-run cap left behind, and how
    old the snapshots actually are. Both are already computed inside
    ``recover_with_report``; this carries them out instead of dropping them.

    ``eligible``          distinct content-page URLs the CDX window offered that
                          matched the spec's ``path_regex`` — everything this
                          run could have read, before the per-run cap.
    ``fetched``           candidates actually produced. A snapshot that was
                          refused, or whose title was generic boilerplate, is
                          attempted and dropped, so ``fetched`` can be lower
                          than ``eligible - omitted_by_cap``; that difference is
                          the drop count and needs no field of its own.
    ``omitted_by_cap``    ``eligible`` minus ``spec.max_items``, or 0. These are
                          deferred to a later run (seen-state carries them), not
                          lost — the cap is politeness, not a filter.
    ``oldest_capture``    CDX timestamps (``YYYYMMDDhhmmss``) spanning the
    ``newest_capture``    ELIGIBLE set — the window the Archive offered.
    ``capture_age_days_max``     whole days between ``utcnow()`` and the capture
    ``capture_age_days_median``  timestamp, over the FETCHED items only.

    **The two halves have different bases, deliberately.** The timestamps
    describe what the Archive had; the ages describe what this run read and put
    in front of the operator. So when the cap bites, ``capture_age_days_max`` is
    NOT the age of ``oldest_capture`` — the oldest eligible capture was never
    fetched. ``test_oldest_capture_is_eligible_basis_while_ages_are_fetched``
    pins that divergence so it cannot be silently "fixed" into agreement.

    Ages are the floor of elapsed days; the median of an even-sized set is the
    mean of the two central values truncated to whole days. A capture dated in
    the future (clock skew, or a malformed CDX row) yields a negative age rather
    than a clamped zero: a number that cannot be true is more useful than one
    that can. All seven fields default to the empty-run state, so a source with
    no spec, an unavailable CDX index, or a non-JSON CDX response reports
    ``RecoveryReport()`` rather than nothing.
    """
    eligible: int = 0
    fetched: int = 0
    omitted_by_cap: int = 0
    oldest_capture: "str | None" = None
    newest_capture: "str | None" = None
    capture_age_days_max: "int | None" = None
    capture_age_days_median: "int | None" = None


_CDX_TS = re.compile(r"^[0-9]{14}")


def _capture_age_days(ts: str, now: datetime) -> "int | None":
    """Whole days from a CDX ``YYYYMMDDhhmmss`` capture stamp to ``now``.

    Returns None for a stamp that is missing, short, or not a real date, so one
    malformed CDX row cannot poison the run's age statistics.
    """
    m = _CDX_TS.match(ts or "")
    if m is None:
        return None
    try:
        captured = datetime.strptime(m.group(0), "%Y%m%d%H%M%S").replace(
            tzinfo=timezone.utc)
    except ValueError:                     # e.g. month 13 in the index
        return None
    return (now - captured).days


def _cdx_get(url: str, name: str, backoff=None):
    """Fetch the CDX index, retrying on a refusal (polite_get -> None).

    archive.org's per-IP block after a snapshot burst is transient; a short
    wait clears it. Returns the response or None after the last attempt.
    ``backoff`` is the wait (seconds) before each retry; resolved from the
    module constant at CALL time (not bound as a def-time default) so a test —
    or a future config — can shorten it. Tests pass () for none.
    """
    if backoff is None:
        backoff = _CDX_RETRY_BACKOFF_S
    resp = polite_get(url)
    for i, wait in enumerate(backoff, start=2):
        if resp is not None:
            return resp
        logger.info("%s: CDX refused (archive.org rate limit?); retry %d in %ds",
                    name, i, wait)
        time.sleep(wait)
        resp = polite_get(url)
    return resp


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


def recover_with_report(name: str, since=None
                        ) -> "tuple[list[CandidateItem], RecoveryReport]":
    """Read a blocked source's content pages from the Internet Archive.

    Returns the candidates (keyed to the real origin URL) and a
    ``RecoveryReport`` describing what the run saw and how stale it is. Never
    raises. ``since`` is accepted for signature symmetry with ``Source.fetch``
    and is not used to filter (capture date is not decision date); seen-state
    dedups downstream.

    ``utcnow()`` is read ONCE here and used for both the CDX lookback floor and
    every capture age, so a run's telemetry is internally consistent and a test
    can freeze the clock at a single monkeypatch point.
    """
    spec = SPECS.get(name)
    if spec is None:
        return [], RecoveryReport()
    now = utcnow()
    frm = (now - timedelta(days=spec.lookback_days)).strftime("%Y%m%d")
    resp = _cdx_get(_CDX_URL.format(prefix=spec.cdx_prefix, frm=frm), name)
    if resp is None:
        logger.warning("%s: CDX index unavailable after retries, no recovery "
                       "this run", name)
        return [], RecoveryReport()
    try:
        rows = json.loads(getattr(resp, "text", "") or "[]")
    except ValueError:
        logger.warning("%s: CDX returned non-JSON, no recovery this run", name)
        return [], RecoveryReport()
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

    # `ordered` stays the full ELIGIBLE set (newest capture first) for the
    # report's span; `to_fetch` is what the per-run politeness cap allows.
    ordered = sorted(captures.values(), key=lambda t: t[0], reverse=True)
    eligible = len(ordered)
    omitted_by_cap = max(0, eligible - spec.max_items)
    to_fetch = ordered[:spec.max_items] if omitted_by_cap else ordered
    if omitted_by_cap:
        logger.info("%s: %d captured content pages; fetching the %d most "
                    "recently archived (the rest wait for a later run)",
                    name, eligible, spec.max_items)

    items: list[CandidateItem] = []
    ages: list[int] = []
    for ts, original in to_fetch:
        item = _snapshot_item(name, spec, ts, original)
        if item is None:
            continue
        items.append(item)
        age = _capture_age_days(ts, now)
        if age is not None:
            ages.append(age)

    report = RecoveryReport(
        eligible=eligible,
        fetched=len(items),
        omitted_by_cap=omitted_by_cap,
        oldest_capture=ordered[-1][0] if ordered else None,
        newest_capture=ordered[0][0] if ordered else None,
        capture_age_days_max=max(ages) if ages else None,
        capture_age_days_median=int(statistics.median(ages)) if ages else None,
    )
    logger.info("%s: recovered %d content page(s) from the Internet Archive "
                "(capture lag applies; not a live read); %d eligible, %d "
                "omitted by the per-run cap, capture age max %s / median %s "
                "day(s)", name, report.fetched, report.eligible,
                report.omitted_by_cap, report.capture_age_days_max,
                report.capture_age_days_median)
    return items, report


def recover(name: str, since=None) -> list[CandidateItem]:
    """``recover_with_report`` without the telemetry — the original contract.

    Kept byte-for-byte compatible in signature and return type for every caller
    that does not want the report.
    """
    return recover_with_report(name, since)[0]
