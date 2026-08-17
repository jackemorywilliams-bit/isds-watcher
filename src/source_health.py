"""Silent-decay guard: per-source consecutive-zero-run tracking.

The per-source try/except in the pipeline means a fetcher whose site changed
(selector rot, feed expiry, a new bot-challenge) does not fail — it just
returns [] forever, and a broken source silently reads as a quiet week. This
module makes that decay visible:

- ``state/source_health.json`` persists, per source, how many consecutive runs
  yielded zero raw items (``zero_streak``) and when it last yielded any.
- When a source documented as ACTIVE hits ``DEGRADED_AFTER`` (3) consecutive
  zero runs, its status in the run's source-health table becomes
  ``"DEGRADED (N zero runs)"`` — surfaced in meta.json, the digest README, and
  the digest header.
- When all-but-one of the active sources return zero raw items in a single
  run, a ``COLLECTION ANOMALY`` warning is raised as well.

Nothing here ever raises: a missing or corrupt health file is treated as empty,
exactly like state/seen.json.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger("isds.source_health")

HEALTH_PATH = "state/source_health.json"

# A source is flagged DEGRADED after this many consecutive zero-item runs.
DEGRADED_AFTER = 3

# Sources documented as active collectors (HANDOFF.md): a zero-streak from one
# of these is a real degradation signal. Excluded by design:
#   - google_news_rss: robots-blocked, reported DISABLED — always zero.
#   - gmail_scholar:   credential-gated; inactive without GMAIL_ALERT_* env.
ACTIVE_SOURCES = {
    "iisd_itn",
    "google_alerts",
    "italaw",
    "icsid",
    "iareporter_headlines",
    "unctad_isds",
    "pca_press",
    "gdelt",
}

# Statuses that already explain a zero and must never be overwritten.
_EXEMPT_STATUSES = {"DISABLED", "FAILED"}


# ---------------------------------------------------------------------------
# Zero-streak refinement probes (added 2026-08-17).
#
# The 2026-08-17 run flagged iisd_itn, google_alerts and italaw as "DEGRADED —
# fetchers likely no longer match the live site". All three diagnoses were
# wrong: ITN's feed was live with its newest article from April (a quarterly
# publication in a quiet quarter), the Google Alerts feeds were live but served
# empty by the platform (dead since mid-July, as alerts.yaml documents), and
# italaw returned HTTP 403 from a bot-challenge — unreachable, not mismatched.
# One label for three different diseases meant the operator could not tell
# which needed repair, which needed replacement, and which needed nothing.
#
# When a documented-active source crosses the streak threshold, its probe (if
# one exists) makes one cheap check and refines the label:
#   "QUIET (feed live; newest item YYYY-MM-DD)"  -> not degradation; the feed
#       works and simply has nothing in the window. Excluded from the alarm.
#   "PLATFORM-EMPTY (...)" / "NOT-READ (HTTP NNN ...)" -> confirmed access
#       failure with its cause; alarmed with repair-or-replace language.
#   None -> probe could not improve on the generic label; the original
#       "fetchers likely no longer match" alarm stands (fail toward alarm).
# Probes never raise; a probe crash falls back to the generic DEGRADED label.
# ---------------------------------------------------------------------------

_PROBE_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36")


def _probe_iisd_itn() -> "str | None":
    from .sources.base import fetch_rss, parse_date
    from .sources.iisd_itn import FEED_URL
    feed = fetch_rss(FEED_URL)
    entries = getattr(feed, "entries", None) if feed is not None else None
    if not entries:
        return None
    dates = [d for d in (parse_date(getattr(e, "published", None)
                                    or getattr(e, "updated", None))
                         for e in entries) if d is not None]
    if not dates:
        return None
    return f"QUIET (feed live; newest item {max(dates).date().isoformat()})"


def _probe_google_alerts() -> "str | None":
    from .sources.base import fetch_rss
    from .sources.google_alerts import _load_feed_urls
    urls = _load_feed_urls()
    if not urls:
        return "DISABLED (no feeds configured)"
    live = entries = 0
    for u in urls:
        feed = fetch_rss(u, check_robots=False)
        if feed is None:
            continue
        live += 1
        entries += len(getattr(feed, "entries", []) or [])
    if live == 0:
        return None
    if entries == 0:
        return (f"PLATFORM-EMPTY ({live}/{len(urls)} feed(s) live, "
                "zero entries served)")
    return f"QUIET (feeds live; {entries} entries, none in the run window)"


def _probe_italaw() -> "str | None":
    import urllib.error
    import urllib.request
    from .sources.italaw import BASE_URL
    req = urllib.request.Request(BASE_URL, headers={"User-Agent": _PROBE_UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            code = getattr(resp, "status", 200)
    except urllib.error.HTTPError as exc:
        code = exc.code
    except Exception:  # noqa: BLE001 - network trouble: no refinement
        return None
    if code == 200:
        return None      # reachable yet the fetcher parsed nothing: real rot
    if code == 403:
        return "NOT-READ (HTTP 403 bot-challenge at the origin)"
    return f"NOT-READ (HTTP {code})"


def _probe_gdelt() -> "str | None":
    from .sources.base import polite_get
    resp = polite_get("https://api.gdeltproject.org/api/v2/doc/doc"
                      "?query=ICSID&mode=artlist&maxrecords=1&format=json")
    if resp is None:
        return None
    body = getattr(resp, "text", "") or ""
    if body.lstrip().startswith("{"):
        return "QUIET (API live; combined query returned nothing in window)"
    return "NOT-READ (rate-limited by the GDELT API)"


PROBES = {
    "iisd_itn": _probe_iisd_itn,
    "google_alerts": _probe_google_alerts,
    "italaw": _probe_italaw,
    "gdelt": _probe_gdelt,
}


def _empty() -> dict:
    return {"sources": {}}


def load(path: str = HEALTH_PATH) -> dict:
    """Load the health file; missing or corrupt files are treated as empty."""
    if not os.path.exists(path):
        return _empty()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("health root is not an object")
        data.setdefault("sources", {})
        if not isinstance(data["sources"], dict):
            data["sources"] = {}
        return data
    except Exception as exc:  # noqa: BLE001 - corrupt state must not crash
        logger.warning("source_health: could not read %s (%s); treating as empty",
                       path, exc)
        return _empty()


def save(health: dict, path: str = HEALTH_PATH) -> None:
    """Persist the health file, creating the parent dir if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    health.setdefault("sources", {})
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(health, fh, indent=2, sort_keys=True)
        fh.write("\n")


def update_streaks(health: dict, counts: dict[str, int], run_date: str) -> None:
    """Advance each source's zero-streak with this run's raw item counts.

    ``counts`` maps source name -> raw items yielded this run (the
    source-health ``count``, before dedup — a source whose items all deduped
    as already-seen is healthy and resets its streak).
    """
    sources = health.setdefault("sources", {})
    for name, count in counts.items():
        rec = sources.setdefault(name, {"zero_streak": 0, "last_nonzero": None})
        if count > 0:
            rec["zero_streak"] = 0
            rec["last_nonzero"] = run_date
        else:
            rec["zero_streak"] = int(rec.get("zero_streak", 0)) + 1
        rec["last_run"] = run_date


def zero_streak(health: dict, name: str) -> int:
    return int(health.get("sources", {}).get(name, {}).get("zero_streak", 0))


def apply_to_source_health(source_health: list[dict], health: dict,
                           threshold: int = DEGRADED_AFTER) -> list[str]:
    """Mark documented-active sources with long zero-streaks as DEGRADED.

    Mutates the run's ``source_health`` entries in place (status becomes
    ``"DEGRADED (N zero runs)"``) and returns the list of degraded source
    names. Statuses that already explain the zero (DISABLED, FAILED) are left
    alone, as are sources not documented active.
    """
    degraded: list[str] = []
    for sh in source_health:
        name = sh.get("name")
        if name not in ACTIVE_SOURCES:
            continue
        if sh.get("status") in _EXEMPT_STATUSES:
            continue
        if sh.get("count", 0) != 0:
            continue
        streak = zero_streak(health, name)
        if streak < threshold:
            continue
        refined = None
        probe = PROBES.get(name)
        if probe is not None:
            try:
                refined = probe()
            except Exception as exc:  # noqa: BLE001 - probe must never kill the guard
                logger.warning("source_health: probe for %s failed (%s)", name, exc)
                refined = None
        if refined is not None and refined.startswith("QUIET"):
            # The feed is demonstrably alive; the zero is the world being
            # quiet, not the instrument being blind. Recorded, not alarmed.
            sh["status"] = refined
        elif refined is not None:
            sh["status"] = f"{refined}; {streak} zero runs"
            degraded.append(name)
        else:
            sh["status"] = f"DEGRADED ({streak} zero runs)"
            degraded.append(name)
    return degraded


def collection_anomaly(source_health: list[dict]) -> bool:
    """True when all documented-active sources but at most one yielded zero.

    An anomaly like the 2026-07-27 run — every active feed but one empty — is
    far likelier collection-side breakage than a genuinely silent week, so it
    must be called out, never passed off as quiet.
    """
    active = [sh for sh in source_health
              if sh.get("name") in ACTIVE_SOURCES
              and sh.get("status") not in _EXEMPT_STATUSES]
    if len(active) < 2:
        return False
    nonzero = sum(1 for sh in active if sh.get("count", 0) > 0)
    return nonzero <= 1


def build_warnings(source_health: list[dict], degraded: list[str]) -> list[str]:
    """Human-readable warning lines for the digest README and header."""
    warnings: list[str] = []
    if degraded:
        confirmed = []   # probe named the disease (NOT-READ / PLATFORM-EMPTY)
        unknown = []     # probe could not improve on the generic diagnosis
        for sh in source_health:
            if sh["name"] not in degraded:
                continue
            label = f"{sh['name']} ({sh['status']})"
            if sh["status"].startswith(("NOT-READ", "PLATFORM-EMPTY", "DISABLED")):
                confirmed.append(label)
            else:
                unknown.append(label)
        if confirmed:
            warnings.append(
                "SOURCE ACCESS FAILURE — probes confirmed these sources cannot "
                "currently deliver items: " + ", ".join(confirmed)
                + ". The access path needs repair or replacement; zero items "
                  "from them is NOT evidence of a quiet week.")
        if unknown:
            warnings.append(
                "SOURCE DEGRADATION WARNING — documented-active sources with "
                f"{DEGRADED_AFTER}+ consecutive zero-item runs: "
                + ", ".join(unknown)
                + ". Their fetchers likely no longer match the live site; "
                  "zero items from them is NOT evidence of a quiet week.")
    if collection_anomaly(source_health):
        warnings.append(
            "COLLECTION ANOMALY — all active sources but at most one returned "
            "zero items this run. Treat this week's (near-)empty digest as a "
            "collection failure signal, not a quiet week.")
    return warnings


def record_run(source_health: list[dict], run_date: str,
               path: str = HEALTH_PATH,
               threshold: int = DEGRADED_AFTER) -> list[str]:
    """One-call guard for the pipeline: update streaks, persist, flag, warn.

    Takes the run's source-health entries (name/status/count), advances the
    persisted zero-streaks, rewrites statuses to DEGRADED where warranted, and
    returns the warning lines (possibly empty). Never raises.
    """
    try:
        health = load(path)
        update_streaks(health,
                       {sh["name"]: sh.get("count", 0) for sh in source_health},
                       run_date)
        degraded = apply_to_source_health(source_health, health, threshold)
        save(health, path)
        warnings = build_warnings(source_health, degraded)
        for w in warnings:
            logger.warning("source_health: %s", w)
        return warnings
    except Exception as exc:  # noqa: BLE001 - the guard must never kill a run
        logger.error("source_health: guard failed (%s)", exc)
        return []
