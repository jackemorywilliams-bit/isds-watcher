"""Seen-state persistence with first-run bootstrap.

The state file records, per source, which source_ids we have already
processed so we never re-classify or re-send the same item. It must NEVER
crash the pipeline: a missing or corrupt file is treated as empty state.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger("isds.state")

STATE_PATH = "state/seen.json"


def _empty_state() -> dict:
    return {"sources": {}}


def load_state(path: str = STATE_PATH) -> dict:
    """Load state; bootstrap to {"sources": {}} if missing or unparseable."""
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


def mark_seen(state: dict, source: str, source_id: str, when=None) -> None:
    """Record a (source, source_id) as processed with an ISO timestamp."""
    if when is None:
        when = datetime.now(timezone.utc)
    if isinstance(when, datetime):
        when = when.isoformat()
    state.setdefault("sources", {}).setdefault(source, {})[source_id] = when
