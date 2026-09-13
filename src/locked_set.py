"""Locked validation set — the reservation list the pipeline must not screen.

The council's SUPPLEMENTARY RULING of 2026-09-13, paragraph 5: *"Any item drawn
from an active source is excluded from production screening at the moment of
capture — a single explicit locked-set reservation list consulted by the
pipeline, with the exclusion logged per run so the suppression is visible and
countable rather than silent. Reserving an item is not hiding it; publishing it
is destroying it."*

WHY THIS EXISTS. The locked set is drawn from sources this instrument also
collects from in production — batch 1 is six `iareporter_headlines` items
published 2026-09-09..09-11. If a weekly run screens one of those URLs, the item
carries the instrument's own verdict, and the set's disjointness from production
is broken retroactively by the project's own pipeline. That damage is not
repairable by editing anything afterwards, which is why the exclusion happens at
intake and not at publication.

THE LIST IS DERIVED, NEVER HAND-MAINTAINED. It is exactly the `source_url` of
every item in every `analytics/locked_set/**/items.json` — batch 1 at the top
level today, batches 2-9 at `analytics/locked_set/batch-N/items.json` as the
chairman ruled. A hand-kept parallel list would drift from the set it protects,
which is the same defect one level up: a second copy of the truth.

FAIL-SAFE DIRECTION, stated so nobody has to infer it. A missing or unreadable
locked set yields an EMPTY reservation set and the pipeline runs normally. The
instrument must never stop collecting because a validation artifact is absent.
The cost of that choice is that a broken locked set can let a reserved item
through, so every degraded read is logged at WARNING rather than passed over.

One softening of "empty on any failure": an unreadable file removes only ITS OWN
items, not the items of files that read cleanly. Dropping batch 1's reservations
because batch 7 is malformed would expose six items to protect none.
"""

from __future__ import annotations

import glob
import json
import logging
import os
from urllib.parse import parse_qsl, urlsplit

logger = logging.getLogger("isds.locked_set")

# Where the locked validation set lives, relative to the repo root.
LOCKED_SET_DIR = os.path.join("analytics", "locked_set")

# Every items file under it, at any depth: the top-level batch 1 file and the
# per-batch files. `**` with recursive=True matches zero directories too, so the
# one pattern covers both without a second glob to keep in step with this one.
ITEMS_GLOB = os.path.join(LOCKED_SET_DIR, "**", "items.json")

# A reservation is (identity, required query parameters). `Reservations` maps an
# identity to every parameter-set reserved at it — a tuple, not a set, so the
# structure is ordered and a run over it is deterministic.
Reservations = dict


def identity(url: str) -> tuple[str, frozenset]:
    """``(host+path, query parameters)`` — how a URL is identified for reservation.

    An item in this codebase IS its URL: every source adapter sets
    ``source_id=url`` (src/sources/*.py) and the seen-state dedups on that
    string, so URL identity is already item identity here. What the seen-state
    does NOT do is tolerate the ways one URL is written differently in two
    places, because it only ever compares a source's output against that same
    source's earlier output. A reservation compares a hand-recorded URL in
    `items.json` against whatever a feed emits, so it has to.

    The normalisation, and nothing beyond it:

      * scheme is dropped after being used to resolve the default port, so
        ``http://`` and ``https://`` are the same item;
      * host is lower-cased, a leading ``www.`` is removed, and a default port
        (``:80`` on http, ``:443`` on https) is dropped;
      * a trailing ``/`` is stripped from the path;
      * the fragment is dropped — it never identifies a different document;
      * query parameters are returned as an unordered set, so order does not
        matter, and are compared by the rule in `is_reserved`.

    Deliberately NOT done: case-folding the path (many CMS paths are
    case-sensitive), percent-decoding (two spellings of one path are still one
    path, and decoding can introduce delimiters), and stripping a named list of
    tracking parameters (a hard-coded list is a thing to maintain, and the
    subset rule in `is_reserved` already absorbs added parameters).

    Never raises: junk input yields ``("", frozenset())``, which matches nothing.
    """
    raw = (url or "").strip()
    if not raw:
        return "", frozenset()
    try:
        parts = urlsplit(raw)
    except ValueError:            # malformed IPv6 literal, bad port, etc.
        return "", frozenset()
    scheme = (parts.scheme or "").lower()
    try:
        host = (parts.netloc or "").lower()
    except ValueError:
        return "", frozenset()
    if scheme == "http" and host.endswith(":80"):
        host = host[:-3]
    elif scheme == "https" and host.endswith(":443"):
        host = host[:-4]
    if host.startswith("www."):
        host = host[4:]
    path = (parts.path or "").rstrip("/")
    try:
        params = frozenset(parse_qsl(parts.query or "", keep_blank_values=True))
    except ValueError:
        params = frozenset()
    return f"{host}{path}", params


def _reserve(into: dict, url: str) -> bool:
    ident, params = identity(url)
    if not ident:
        return False
    existing = into.get(ident, ())
    if params not in existing:
        into[ident] = existing + (params,)
    return True


def _items_files(root: str = "") -> list[str]:
    """Every locked-set items file, sorted, so two runs read the same thing."""
    pattern = os.path.join(root, ITEMS_GLOB) if root else ITEMS_GLOB
    try:
        return sorted(glob.glob(pattern, recursive=True))
    except OSError as exc:        # unreadable directory
        logger.warning("locked_set: cannot list %s (%s); reservation set is EMPTY "
                       "and screening proceeds normally", pattern, exc)
        return []


def load_reservations(root: str = "") -> Reservations:
    """Build the reservation set from `analytics/locked_set/**/items.json`.

    Returns ``{identity: (params, ...)}``. Empty when the locked set is absent or
    unreadable — see the fail-safe note in the module docstring. Never raises.
    """
    directory = os.path.join(root, LOCKED_SET_DIR) if root else LOCKED_SET_DIR
    if not os.path.isdir(directory):
        logger.warning("locked_set: %s is absent; reservation set is EMPTY and "
                       "screening proceeds normally", directory)
        return {}
    files = _items_files(root)
    if not files:
        logger.warning("locked_set: no items.json under %s; reservation set is "
                       "EMPTY and screening proceeds normally", directory)
        return {}
    reservations: dict = {}
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            # This file only. A malformed batch must not un-reserve the batches
            # that read cleanly.
            logger.warning("locked_set: %s is unreadable (%s); its items are NOT "
                           "reserved this run", path, exc)
            continue
        # The schema is a list of item objects; a ``{"items": [...]}`` wrapper is
        # accepted too so a future schema revision cannot silently reserve
        # nothing.
        if isinstance(data, dict):
            data = data.get("items")
        if not isinstance(data, list):
            logger.warning("locked_set: %s is not a list of items; its items are "
                           "NOT reserved this run", path)
            continue
        taken = 0
        for entry in data:
            if isinstance(entry, dict) and _reserve(reservations, entry.get("source_url")):
                taken += 1
        if taken != len(data):
            logger.warning("locked_set: %s — %d of %d items have no usable "
                           "source_url and are NOT reserved", path,
                           len(data) - taken, len(data))
        logger.info("locked_set: %s reserved %d item URL(s)", path, taken)
    return reservations


def is_reserved(url: str, reservations: Reservations) -> bool:
    """Is this URL a locked-set item?

    The rule, in one sentence: **the identity must match, and every query
    parameter the reserved URL carries must also be present on the candidate.**

    So a reserved URL with no query reserves the item however a feed decorates
    it (``?utm_source=rss``, a trailing slash, ``http://``, ``www.``), while a
    reserved URL whose query IS its identity (``?p=1234``) does not reserve its
    neighbour at ``?p=1235``. Over-reserving a production item costs one
    unscreened item; under-reserving a locked-set item destroys the set.
    """
    if not reservations:
        return False
    ident, params = identity(url)
    if not ident:
        return False
    for required in reservations.get(ident, ()):
        if required <= params:
            return True
    return False


def reserved_count(reservations: Reservations) -> int:
    """How many distinct URLs the reservation set holds (for logging)."""
    return sum(len(v) for v in reservations.values())
