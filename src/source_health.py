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
}

# Statuses that already explain a zero and must never be overwritten.
_EXEMPT_STATUSES = {"DISABLED", "FAILED"}


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
        if streak >= threshold:
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
        parts = []
        for sh in source_health:
            if sh["name"] in degraded:
                parts.append(f"{sh['name']} ({sh['status']})")
        warnings.append(
            "SOURCE DEGRADATION WARNING — documented-active sources with "
            f"{DEGRADED_AFTER}+ consecutive zero-item runs: " + ", ".join(parts)
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
