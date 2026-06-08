"""Source-fetching base layer for the ISDS thematic watcher.

Defines the data contract (CandidateItem), the Source ABC, and a polite
module-level fetcher used by every source: per-domain rate limiting,
robots.txt respect, and defensive HTTP GETs that never raise.

NOTE: requests / feedparser / bs4 / dateutil are runtime dependencies and may
not be installed at lint time. They are imported lazily so that `py_compile`
and static analysis work without them.
"""

from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib import robotparser

logger = logging.getLogger("isds.sources.base")

USER_AGENT = "isds-watcher/1.0 (+https://github.com/jackemorywilliams-bit/isds-watcher)"

# Minimum seconds between requests to the same domain (netloc).
MIN_INTERVAL_SECONDS = 3.0

# Per-domain bookkeeping. Guarded by _lock so concurrent sources stay polite.
_last_request_at: dict[str, float] = {}
_robots_cache: dict[str, "robotparser.RobotFileParser | None"] = {}
_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Data contract
# ---------------------------------------------------------------------------
@dataclass
class CandidateItem:
    source: str
    source_id: str          # stable unique ID within source
    url: str
    title: str
    published: datetime     # tz-aware UTC
    summary: str
    raw_text: str
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Source abstract base class
# ---------------------------------------------------------------------------
class Source(ABC):
    """Abstract base for every source.

    Subclasses set ``name`` and ``priority`` and implement ``fetch``.
    ``fetch`` MUST NEVER raise: on total failure it returns [] and logs.
    """

    name: str = "base"
    priority: str = "secondary"

    @abstractmethod
    def fetch(self, since: datetime) -> list[CandidateItem]:
        """Return items at/after ``since`` (tz-aware UTC cutoff).

        Sources should filter to items at/after ``since`` when a date is
        available; when no date is available the item should be included and
        the downstream pipeline will dedupe.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------
def parse_date(s) -> "datetime | None":
    """Parse an arbitrary date string into a tz-aware UTC datetime.

    Returns None on empty/garbage input. Naive datetimes are assumed UTC.
    """
    if not s:
        return None
    if isinstance(s, datetime):
        dt = s
    else:
        try:
            from dateutil import parser as _dateparser
        except Exception:  # pragma: no cover - dependency missing
            logger.warning("parse_date: dateutil not available")
            return None
        try:
            dt = _dateparser.parse(str(s))
        except (ValueError, OverflowError, TypeError) as exc:
            logger.debug("parse_date: could not parse %r (%s)", s, exc)
            return None
        if dt is None:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def utcnow() -> datetime:
    """Current time as a tz-aware UTC datetime."""
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Robots
# ---------------------------------------------------------------------------
def _domain(url: str) -> str:
    return urlparse(url).netloc


def robots_allowed(url: str) -> bool:
    """Return True if our USER_AGENT may fetch ``url`` per robots.txt.

    robots.txt is fetched once per domain and cached. If robots.txt itself
    errors / 404s / is unreachable, we treat the URL as ALLOWED (fail-open).
    The rule is evaluated for our USER_AGENT, falling back to '*'.
    """
    parsed = urlparse(url)
    domain = parsed.netloc
    if not domain:
        return True

    with _lock:
        cached = _robots_cache.get(domain, "__miss__")
    if cached == "__miss__":
        rp: "robotparser.RobotFileParser | None"
        robots_url = f"{parsed.scheme or 'https'}://{domain}/robots.txt"
        rp = None
        # Fetch robots.txt with OUR identifying UA via requests. urllib's own
        # RobotFileParser.read() is blocked/403'd by Cloudflare on several of
        # these hosts and then mis-treats the 403 as "disallow all" — so we
        # fetch the real file ourselves and parse it explicitly. On 404/empty
        # or any error we fail OPEN (no robots restriction).
        try:
            import requests
            resp = requests.get(robots_url, headers={"User-Agent": USER_AGENT}, timeout=20)
            if resp.status_code == 200 and resp.text.strip():
                rp = robotparser.RobotFileParser()
                rp.parse(resp.text.splitlines())
            else:
                logger.debug("robots_allowed: %s -> HTTP %s; allowing",
                             robots_url, resp.status_code)
        except Exception as exc:  # network error, malformed, requests missing
            logger.debug("robots_allowed: could not read %s (%s); allowing", robots_url, exc)
            rp = None  # treat as allowed
        with _lock:
            _robots_cache[domain] = rp
        cached = rp

    if cached is None:
        return True

    try:
        # Check our explicit UA first; robotparser checks '*' automatically
        # when the named agent has no matching group.
        return bool(cached.can_fetch(USER_AGENT, url))
    except Exception as exc:  # defensive: malformed robots parse
        logger.debug("robots_allowed: can_fetch errored for %s (%s); allowing", url, exc)
        return True


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
def _respect_rate_limit(domain: str) -> None:
    """Sleep as needed so this domain isn't hit more than once per interval."""
    with _lock:
        last = _last_request_at.get(domain)
        now = time.monotonic()
        if last is not None:
            wait = MIN_INTERVAL_SECONDS - (now - last)
        else:
            wait = 0.0
        # Reserve the slot now (set to projected request time) so concurrent
        # callers serialize their waits instead of all firing at once.
        _last_request_at[domain] = now + max(wait, 0.0)
    if wait > 0:
        logger.debug("rate-limit: sleeping %.2fs for %s", wait, domain)
        time.sleep(wait)


# ---------------------------------------------------------------------------
# Polite GET
# ---------------------------------------------------------------------------
def polite_get(url: str, timeout: int = 30):
    """GET ``url`` politely. Returns a requests.Response or None.

    Returns None (and logs a warning) on robots-disallow, non-200, timeout,
    or any exception. NEVER raises.
    """
    try:
        import requests
    except Exception:  # pragma: no cover - dependency missing
        logger.warning("polite_get: requests not available; cannot fetch %s", url)
        return None

    if not robots_allowed(url):
        logger.warning("polite_get: robots.txt disallows %s for %s", url, USER_AGENT)
        return None

    domain = _domain(url)
    _respect_rate_limit(domain)

    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        logger.warning("polite_get: timeout fetching %s", url)
        return None
    except requests.exceptions.RequestException as exc:
        logger.warning("polite_get: request error fetching %s (%s)", url, exc)
        return None
    except Exception as exc:  # truly defensive
        logger.warning("polite_get: unexpected error fetching %s (%s)", url, exc)
        return None

    if resp.status_code != 200:
        logger.warning("polite_get: non-200 (%s) for %s", resp.status_code, url)
        return None
    return resp


# ---------------------------------------------------------------------------
# RSS / HTML helpers
# ---------------------------------------------------------------------------
def fetch_rss(url: str):
    """Fetch and parse an RSS/Atom feed. Returns a feedparser result or None."""
    resp = polite_get(url)
    if resp is None:
        return None
    try:
        import feedparser
    except Exception:  # pragma: no cover - dependency missing
        logger.warning("fetch_rss: feedparser not available for %s", url)
        return None
    try:
        parsed = feedparser.parse(resp.content)
    except Exception as exc:
        logger.warning("fetch_rss: could not parse feed %s (%s)", url, exc)
        return None
    if getattr(parsed, "bozo", 0) and not getattr(parsed, "entries", None):
        logger.warning("fetch_rss: feed %s is malformed and has no entries", url)
        return None
    return parsed


def fetch_html(url: str):
    """Fetch a page and parse it with BeautifulSoup. Returns soup or None."""
    resp = polite_get(url)
    if resp is None:
        return None
    try:
        from bs4 import BeautifulSoup
    except Exception:  # pragma: no cover - dependency missing
        logger.warning("fetch_html: bs4 not available for %s", url)
        return None
    try:
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as exc:
        logger.warning("fetch_html: could not parse HTML %s (%s)", url, exc)
        return None


def strip_html(value: str) -> str:
    """Return plain text from an HTML fragment. Falls back to raw on error."""
    if not value:
        return ""
    try:
        from bs4 import BeautifulSoup
    except Exception:  # pragma: no cover - dependency missing
        return str(value).strip()
    try:
        return BeautifulSoup(str(value), "html.parser").get_text(separator=" ", strip=True)
    except Exception:
        return str(value).strip()
