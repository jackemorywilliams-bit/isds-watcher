"""Source-fetching layer for the ISDS thematic watcher.

Public API:
    all_sources(config=None) -> list[Source]
        Independent source instances, ordered by priority. The pipeline is
        expected to try/except per source; no source's fetch() ever raises.
"""

from __future__ import annotations

import logging

from .base import CandidateItem, Source, parse_date
from .iisd_itn import IISDITNSource
from .google_alerts import GoogleAlertsSource
from .gmail_scholar import GmailScholarSource
from .google_news_rss import GoogleNewsRSSSource
from .italaw import ItalawSource
from .icsid import ICSIDSource
from .iareporter_headlines import IAReporterHeadlinesSource
from .unctad_isds import UNCTADISDSSource
from .pca_press import PCAPressSource
from .press_business import IndependentBusinessSource, StandardBusinessSource

logger = logging.getLogger("isds.sources")

__all__ = [
    "CandidateItem",
    "Source",
    "parse_date",
    "all_sources",
    "IISDITNSource",
    "GoogleAlertsSource",
    "GmailScholarSource",
    "GoogleNewsRSSSource",
    "ItalawSource",
    "ICSIDSource",
    "IAReporterHeadlinesSource",
    "UNCTADISDSSource",
    "PCAPressSource",
    "IndependentBusinessSource",
    "StandardBusinessSource",
]


def all_sources(config=None) -> list[Source]:
    """Return one fresh instance of every usable source, in priority order.

    High-signal / reliable sources first (iisd_itn, google_news_rss, italaw,
    icsid, iareporter_headlines), then the best-effort / likely-blocked
    sources (unctad_isds, pca_press). ``config`` is accepted for forward
    compatibility and currently unused.
    """
    return [
        IISDITNSource(),
        GoogleAlertsSource(),
        GmailScholarSource(),
        GoogleNewsRSSSource(),
        ItalawSource(),
        ICSIDSource(),
        IAReporterHeadlinesSource(),
        UNCTADISDSSource(),
        PCAPressSource(),
        IndependentBusinessSource(),
        StandardBusinessSource(),
    ]
