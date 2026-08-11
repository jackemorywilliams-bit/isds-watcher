"""Seen-state persistence, the deferred-retry queue, and the abandoned ledger.

The state file records, per source, which source_ids we have already
processed so we never re-classify or re-send the same item. It must NEVER
crash the pipeline: a missing or corrupt file is treated as empty state.

WHAT A SEEN ENTRY NOW HOLDS. It used to be a bare ISO timestamp — the moment we
finished with an item and nothing about how. That made every ending look the
same: an item the model classified cleanly, an item whose classification failed
and got a keyword score published in its place, and an item indexed by the
first-run bootstrap without ever being read were three different events written
identically, and once written there was no way back to which had happened. An
entry is now ``{"at": iso, "outcome": str, "run": date}``. ``is_seen`` is
unchanged and still means exactly "this key is present".

LEGACY VALUES ARE MIGRATED AT READ TIME. The live state file holds hundreds of
bare-string entries and rewriting it wholesale would be a large unreviewable diff
over data we cannot regenerate. ``load_state`` converts a bare string to
``{"at": <the string>, "outcome": "legacy"}`` in memory. "legacy" is a truthful
label — we genuinely do not know how those items ended — and it is the one
outcome the integrity guard exempts from its terminal-outcome rule. New writes
use the new shape, so the file converts gradually as items are re-marked.

THE DEFERRED QUEUE. An item whose classification failed has not been processed,
and marking it seen makes that failure permanent and invisible. Such items go to
``state/deferred.json`` instead: identity, attempt count, and last outcome, so a
later run can pick them up before it looks for anything new. After
``MAX_CLASSIFY_ATTEMPTS`` the item is given up on — marked seen with outcome
"abandoned" and recorded in ``analytics/abandoned_candidates.jsonl``, because
giving up is a decision and decisions should leave a record someone can count.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger("isds.state")

STATE_PATH = "state/seen.json"
DEFERRED_PATH = "state/deferred.json"
ABANDONED_PATH = "analytics/abandoned_candidates.jsonl"

# How many runs may fail to classify one item before we stop carrying it. Three
# is two more chances than the old behaviour gave (which was none — the first
# failure was final and silent), and few enough that a permanently unparseable
# item cannot accumulate in the queue for months.
MAX_CLASSIFY_ATTEMPTS = 3

# Outcomes after which an item is legitimately finished with. "bootstrap" is the
# first-run indexing path: never classified, deliberately, and never to be.
# "legacy" is the pre-migration shape and is exempt rather than terminal.
TERMINAL_SEEN_OUTCOMES = frozenset({
    "ok", "keyword_only_by_design", "abandoned", "bootstrap",
})
LEGACY_OUTCOME = "legacy"


def _empty_state() -> dict:
    return {"sources": {}}


def _iso(when) -> str:
    if when is None:
        when = datetime.now(timezone.utc)
    if isinstance(when, datetime):
        return when.isoformat()
    return str(when)


def _migrate_entry(value):
    """A seen value in the current shape, whatever shape it arrived in.

    A bare string is a pre-2026-08 timestamp. A dict is already current and is
    returned as-is (including any keys we do not know about — a value we do not
    understand is not ours to drop).
    """
    if isinstance(value, str):
        return {"at": value, "outcome": LEGACY_OUTCOME}
    if isinstance(value, dict):
        return value
    # Anything else is corrupt; keep the key (dedup still works off presence)
    # and say honestly that we cannot describe how it ended.
    return {"at": "", "outcome": LEGACY_OUTCOME}


def load_state(path: str = STATE_PATH) -> dict:
    """Load state; bootstrap to {"sources": {}} if missing or unparseable.

    Legacy bare-string values are migrated to the entry shape in memory. The
    file on disk is left exactly as it was until something writes to it.
    """
    if not os.path.exists(path):
        logger.info("state: %s not found, bootstrapping empty state", path)
        return _empty_state()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("state root is not an object")
        data.setdefault("sources", {})
        if not isinstance(data["sources"], dict):
            data["sources"] = {}
        migrated = 0
        for source, entries in data["sources"].items():
            if not isinstance(entries, dict):
                data["sources"][source] = {}
                continue
            for sid, value in list(entries.items()):
                if not isinstance(value, dict):
                    migrated += 1
                entries[sid] = _migrate_entry(value)
        if migrated:
            logger.info("state: migrated %d legacy seen entries in memory", migrated)
        return data
    except Exception as exc:  # noqa: BLE001 - corrupt state must not crash
        logger.warning("state: could not read %s (%s); treating as empty",
                       path, exc)
        return _empty_state()


def save_state(state: dict, path: str = STATE_PATH) -> None:
    """Persist state as pretty JSON, creating the parent dir if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    state.setdefault("sources", {})
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")


def is_empty(state: dict) -> bool:
    """True on a genuinely first run: no sources recorded yet."""
    return not state.get("sources")


def seen_ids(state: dict, source: str) -> set[str]:
    return set(state.get("sources", {}).get(source, {}).keys())


def is_seen(state: dict, source: str, source_id: str) -> bool:
    return source_id in state.get("sources", {}).get(source, {})


def seen_outcome(state: dict, source: str, source_id: str) -> str:
    """The recorded outcome for a seen item, or "" if it is not seen."""
    entry = state.get("sources", {}).get(source, {}).get(source_id)
    if isinstance(entry, dict):
        return str(entry.get("outcome", ""))
    if isinstance(entry, str):
        return LEGACY_OUTCOME
    return ""


def mark_seen(state: dict, source: str, source_id: str, when=None,
              outcome: str = "ok", run: str | None = None) -> None:
    """Record a (source, source_id) as processed, with HOW it ended.

    ``outcome`` must be one a reader can act on; the integrity guard rejects a
    seen entry carrying anything outside ``TERMINAL_SEEN_OUTCOMES``. ``run``
    defaults to the date part of ``when``, which is the run's identity elsewhere
    in the pipeline (digest folders, meta.json, telemetry).
    """
    at = _iso(when)
    state.setdefault("sources", {}).setdefault(source, {})[source_id] = {
        "at": at,
        "outcome": outcome,
        "run": run or at[:10],
    }


# --------------------------------------------------------------------------- #
# Deferred queue
# --------------------------------------------------------------------------- #
def load_deferred(path: str = DEFERRED_PATH) -> dict:
    """Load the deferred queue; a missing or corrupt file reads as empty.

    Shape: ``{source: {source_id: {first_deferred, attempts, last_outcome, url,
    title, published, summary}}}``. Identity and the little bit of text needed
    to reconstruct a candidate whose source has since dropped it from the feed —
    never ``raw_text``, which can run to thousands of characters of somebody
    else's article and has no business persisting between runs.
    """
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("deferred root is not an object")
        return {s: e for s, e in data.items() if isinstance(e, dict)}
    except Exception as exc:  # noqa: BLE001 - corrupt state must not crash
        logger.warning("state: could not read %s (%s); treating as empty",
                       path, exc)
        return {}


def save_deferred(deferred: dict, path: str = DEFERRED_PATH) -> None:
    """Persist the deferred queue (removing sources whose queue emptied)."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    pruned = {s: e for s, e in deferred.items() if e}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(pruned, fh, indent=2, sort_keys=True)
        fh.write("\n")


def deferral_attempts(deferred: dict, source: str, source_id: str) -> int:
    entry = deferred.get(source, {}).get(source_id)
    return int(entry.get("attempts", 0)) if isinstance(entry, dict) else 0


def record_deferral(deferred: dict, item, outcome: str, when=None) -> int:
    """Queue an item for retry (or bump its attempt count); return the count."""
    at = _iso(when)
    bucket = deferred.setdefault(getattr(item, "source", ""), {})
    entry = bucket.get(getattr(item, "source_id", ""))
    if not isinstance(entry, dict):
        entry = {"first_deferred": at, "attempts": 0}
    entry["attempts"] = int(entry.get("attempts", 0)) + 1
    entry["last_outcome"] = outcome
    entry["url"] = getattr(item, "url", "") or ""
    entry["title"] = getattr(item, "title", "") or ""
    published = getattr(item, "published", None)
    entry["published"] = published.isoformat() if isinstance(published, datetime) \
        else (str(published) if published else "")
    entry["summary"] = getattr(item, "summary", "") or ""
    bucket[getattr(item, "source_id", "")] = entry
    return int(entry["attempts"])


def clear_deferral(deferred: dict, source: str, source_id: str) -> None:
    """Drop an item from the queue — it reached a terminal outcome."""
    bucket = deferred.get(source)
    if isinstance(bucket, dict):
        bucket.pop(source_id, None)


def deferred_entries(deferred: dict):
    """``(source, source_id, entry)`` for every queued item, in stable order."""
    for source in sorted(deferred):
        bucket = deferred.get(source) or {}
        for source_id in sorted(bucket):
            entry = bucket[source_id]
            if isinstance(entry, dict):
                yield source, source_id, entry


def append_abandoned(item, outcome: str, attempts: int, run: str,
                     first_deferred: str = "",
                     path: str = ABANDONED_PATH) -> None:
    """Record that we gave up on an item, one JSON line per abandonment.

    The seen entry says "abandoned"; this says which item, after how many tries,
    and failing how. ``scripts/check_seen_integrity.py`` requires the two to
    agree, so an abandonment cannot be recorded in the state file alone where
    nobody would ever see it.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    rec = {
        "schema": 1,
        "run": run,
        "source": getattr(item, "source", "") or "",
        "source_id": getattr(item, "source_id", "") or "",
        "url": getattr(item, "url", "") or "",
        "attempts": int(attempts),
        "last_outcome": outcome,
        "first_deferred": first_deferred,
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True, ensure_ascii=True,
                            separators=(",", ":")))
        fh.write("\n")
