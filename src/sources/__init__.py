"""Source-fetching layer for the ISDS thematic watcher.

Public API:
    all_sources(config=None) -> list[Source]
        Independent source instances, ordered by priority. The pipeline is
        expected to try/except per source; no source's fetch() ever raises.
"""

from __future__ import annotations

import logging

from .base import CHANNELS, READ_DEPTHS, CandidateItem, Source, parse_date
from .iisd_itn import IISDITNSource
from .google_alerts import GoogleAlertsSource
from .gmail_scholar import GmailScholarSource
from .italaw import ItalawSource
from .icsid import ICSIDSource
from .iareporter_headlines import IAReporterHeadlinesSource
from .unctad_isds import UNCTADISDSSource
from .pca_press import PCAPressSource
from .bing_news import BingNewsSource
from .gdelt import GDELTSource

logger = logging.getLogger("isds.sources")

__all__ = [
    "CandidateItem",
    "Source",
    "parse_date",
    "all_sources",
    "IISDITNSource",
    "GoogleAlertsSource",
    "GmailScholarSource",
    "ItalawSource",
    "ICSIDSource",
    "IAReporterHeadlinesSource",
    "UNCTADISDSSource",
    "PCAPressSource",
    "BingNewsSource",
    "GDELTSource",
]


# --------------------------------------------------------------------------- #
# THE CATALOGUE — the roster, and everything every public surface says about it.
#
# One list. Before 2026-09-10 there were four: this constructor list, a sentence
# on the how-it-works page, a paragraph in the README, and the digest email's
# lede — and three of the four said "nine" over a roster of ten. A count written
# in prose beside a list it is not derived from will drift, and it did.
#
# (class, label, channel, read_depth). Order is priority order and is the order
# every surface prints. Nothing else may enumerate sources.
# --------------------------------------------------------------------------- #
_CATALOGUE: tuple[tuple[type, str, str, str], ...] = (
    # The one feed that carries article bodies at intake.
    (IISDITNSource,            "IISD ITN",        "open-repository",  "full-text"),
    # Emory's own Google account. A third party cannot re-run either of these and
    # cannot audit what they did or did not deliver; that is why they are not
    # described as public sources anywhere on this project's surfaces.
    (GoogleAlertsSource,       "Google Alerts",   "operator-mailbox", "listing-then-body"),
    (GmailScholarSource,       "Scholar Alerts",  "operator-mailbox", "listing-then-body"),
    (ItalawSource,             "italaw",          "open-repository",  "listing-then-body"),
    (ICSIDSource,              "ICSID",           "open-repository",  "listing-then-body"),
    # Paywalled body, never fetched: config.HEADLINE_ONLY_SOURCES and
    # enrich.NO_BODY_FETCH. tests/test_source_catalogue.py asserts all three agree.
    (IAReporterHeadlinesSource, "IAReporter",     "open-repository",  "headline-only"),
    (UNCTADISDSSource,         "UNCTAD",          "open-repository",  "listing-then-body"),
    (PCAPressSource,           "PCA",             "open-repository",  "listing-then-body"),
    (BingNewsSource,           "Bing News",       "open-repository",  "listing-then-body"),
    (GDELTSource,              "GDELT",           "open-repository",  "listing-then-body"),
)

# Fail closed at import: a typo in the vocabulary above must break the run, not
# reach a reader as an unrecognised word in a sentence about access.
for _cls, _label, _channel, _depth in _CATALOGUE:
    if not _label:
        raise ValueError(f"{_cls.__name__}: catalogue label must not be empty")
    if _channel not in CHANNELS:
        raise ValueError(f"{_cls.__name__}: channel {_channel!r} not in {CHANNELS}")
    if _depth not in READ_DEPTHS:
        raise ValueError(f"{_cls.__name__}: read_depth {_depth!r} not in {READ_DEPTHS}")
del _cls, _label, _channel, _depth


def all_sources(config=None) -> list[Source]:
    """Return one fresh instance of every usable source, in priority order.

    High-signal / reliable sources first (iisd_itn, italaw,
    icsid, iareporter_headlines), then the best-effort / likely-blocked
    sources (unctad_isds, pca_press). ``config`` is accepted for forward
    compatibility and currently unused.

    Each instance carries its catalogue fields (``label``, ``channel``,
    ``read_depth``) from ``_CATALOGUE`` above. This function is the ONLY
    authority on what the roster is: the site, the README, the digest email and
    the workflow chart's source count are all generated from it.
    """
    sources: list[Source] = []
    for cls, label, channel, read_depth in _CATALOGUE:
        src = cls()
        src.label = label
        src.channel = channel
        src.read_depth = read_depth
        sources.append(src)
    return sources
