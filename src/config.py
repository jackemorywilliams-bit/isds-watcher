"""Configuration for the ISDS thematic watcher.

Recipients and the repo URL are hard-coded. Everything secret (SMTP creds,
LLM API keys) and the model provider come from the environment so nothing
sensitive lands in the repo.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

logger = logging.getLogger("isds.config")

# Hard-coded digest recipients. Temporarily narrowed to a single recipient on
# request; restore ximena.s.benavides@gmail.com here to resume sending to both.
RECIPIENTS = [
    "jackemorywilliams@icloud.com",
]

# Hybrid digest size. Report every item at or above `threshold` (a match); there is
# no upper cap, so a strong week shows all of them. When fewer items match, fill up
# to MIN_DIGEST_ITEMS with the closest near-misses, but only those at or above
# RELEVANCE_FLOOR. With the floor at 25 a genuinely quiet week may send only 0–3
# items rather than padding the digest to the minimum with weak near-misses.
MIN_DIGEST_ITEMS = 6
RELEVANCE_FLOOR = 25

# Enrich at most this many top-ranked candidates by fetching their source page
# (bounds polite-fetch volume per run).
ENRICH_TOP_N = 24

# Sources whose body we cannot read (paywalled / headline-only feeds). A
# "notable line" from one of these is necessarily headline text, never a
# verbatim quote from the source body, so the digest shows "N/A" for it rather
# than presenting the headline as a quotation.
HEADLINE_ONLY_SOURCES = {"iareporter_headlines"}

REPO_URL = "https://github.com/jackemorywilliams-bit/isds-watcher"
SITE_URL = "https://jackemorywilliams-bit.github.io/isds-watcher/"

# One-line description of the watch theme, surfaced in the digest footer.
THEME_ONE_LINER = (
    "ISDS at the intersection of IP-as-investment, regulatory/judicial measures "
    "as the disputed conduct, and jurisdictional/admissibility doctrines "
    "(abuse of right, treaty-shopping, denial of justice)."
)

_DEFAULT_THRESHOLD = 60


def _threshold_from_fingerprint(path: str = "fingerprint.yaml") -> int:
    """Read the threshold from fingerprint.yaml; fall back to 60."""
    try:
        import yaml  # lazy: keep import-time deps minimal
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        val = data.get("threshold", _DEFAULT_THRESHOLD)
        return int(val)
    except Exception as exc:  # noqa: BLE001 - never crash on config
        logger.warning("config: could not read threshold from %s (%s); using %d",
                        path, exc, _DEFAULT_THRESHOLD)
        return _DEFAULT_THRESHOLD


@dataclass
class Config:
    model_provider: str | None = None
    gemini_api_key: str | None = None
    anthropic_api_key: str | None = None
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str | None = None
    smtp_pass: str | None = None
    threshold: int = _DEFAULT_THRESHOLD


def load_config() -> Config:
    """Build a Config from the environment."""
    raw_pass = os.getenv("SMTP_PASS")
    smtp_pass = raw_pass.replace(" ", "") if raw_pass else raw_pass

    try:
        smtp_port = int(os.getenv("SMTP_PORT", "465"))
    except ValueError:
        logger.warning("config: SMTP_PORT not an int; defaulting to 465")
        smtp_port = 465

    return Config(
        model_provider=os.getenv("MODEL_PROVIDER"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=smtp_port,
        smtp_user=os.getenv("SMTP_USER"),
        smtp_pass=smtp_pass,
        threshold=_threshold_from_fingerprint(),
    )


def missing_email_secrets(cfg: Config) -> list[str]:
    """Return the names of any required SMTP secrets that are empty."""
    missing = []
    if not cfg.smtp_user:
        missing.append("SMTP_USER")
    if not cfg.smtp_pass:
        missing.append("SMTP_PASS")
    return missing
