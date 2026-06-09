"""Candidate enrichment: fetch a source page, extract readable body text, and
pull a "notable one-liner" (the highest doctrine-density sentence) for the
digest. Polite and defensive — failures fall back to existing metadata.

Paywalled sources (e.g. iareporter_headlines) are never body-fetched.
"""

from __future__ import annotations

import logging
import re

from .classify import load_fingerprint
from .sources.base import CandidateItem, fetch_html, strip_html

logger = logging.getLogger("isds.enrich")

# Sources whose article bodies must NOT be fetched (paywalled / headlines-only).
NO_BODY_FETCH = {"iareporter_headlines"}

_KEYWORDS: list[str] | None = None


def _doctrine_keywords() -> list[str]:
    global _KEYWORDS
    if _KEYWORDS is None:
        fp = load_fingerprint()
        kws: list[str] = []
        for ring in (fp.get("rings") or {}).values():
            for kw in (ring or {}).get("keywords", []) or []:
                p = (kw.get("phrase") or "").lower().strip()
                if p and kw.get("seed") != "theme_extension":
                    kws.append(p)
        _KEYWORDS = kws
    return _KEYWORDS


def _split_sentences(text: str) -> list[str]:
    # Lightweight sentence splitter; good enough for quote selection.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“])", text)
    return [s.strip() for s in parts if s.strip()]


# Verbs that signal a holding, finding, or doctrinal statement — the kind of
# sentence a researcher would quote.
_HOLDING_VERBS = (
    "held", "found", "concluded", "ruled", "decided", "determined", "considered",
    "observed", "noted", "reasoned", "dismissed", "rejected", "upheld", "annulled",
    "declined", "constituted", "amounted", "amounts to", "breached", "violated",
    "awarded", "ordered", "alleged", "claims that", "argued",
)
_EVALUATIVE = (
    "egregious", "manifest", "abuse", "shock", "unjust", "arbitrary", "denial",
    "wrongful", "unprecedented", "controvers", "bad faith", "expropriat",
    "legitimate expectation", "fair and equitable",
)


def notable_quote(text: str, max_len: int = 300) -> str:
    """Heuristic fallback for the citable line: the sentence most likely to be
    quoted (a holding, doctrinal statement, or evaluative judgment). Used only
    when the classifier does not supply one."""
    if not text:
        return ""
    kws = _doctrine_keywords()
    best, best_score = "", -1.0
    for sent in _split_sentences(text):
        n = len(sent)
        if n < 55 or n > max_len:          # full, substantive sentences only
            continue
        digits = sum(c.isdigit() for c in sent)
        if digits > n * 0.12:              # skip date/paragraph-number lines
            continue
        caps = sum(c.isupper() for c in sent)
        if caps > n * 0.4:                 # skip headline/ALL-CAPS lines
            continue
        low = sent.lower()
        score = 3.0 * sum(1 for k in kws if k in low)
        score += 2.0 * sum(1 for v in _HOLDING_VERBS if v in low)
        score += 1.0 * sum(1 for w in _EVALUATIVE if w in low)
        # Mild preference for a quotable length (roughly 12-45 words).
        words = sent.count(" ") + 1
        if 12 <= words <= 45:
            score += 1.0
        if score > best_score:
            best, best_score = sent, score
    if best_score <= 0:
        # Nothing doctrinally salient: take the first full sentence, or "".
        best = next((s for s in _split_sentences(text)
                     if 55 <= len(s) <= max_len), "")
    return best


def _extract_body(soup) -> str:
    if soup is None:
        return ""
    for tag in soup(["script", "style", "nav", "header", "footer", "form"]):
        tag.decompose()
    node = (soup.find("article") or soup.find("main")
            or soup.find(attrs={"role": "main"}) or soup.body or soup)
    paras = [strip_html(str(p)) for p in node.find_all("p")]
    paras = [p for p in paras if len(p) > 40]
    text = "\n".join(paras)
    if len(text) < 200:  # fallback: whole-node text
        text = strip_html(str(node))
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def enrich(item: CandidateItem, max_chars: int = 5000) -> CandidateItem:
    """Fetch the item's page, enriching raw_text and metadata['notable_quote'].
    Never raises; on any failure the item is returned with its existing text."""
    if item.source in NO_BODY_FETCH:
        item.metadata["notable_quote"] = notable_quote(
            item.summary or item.title)
        item.metadata["enriched"] = False
        return item
    try:
        soup = fetch_html(item.url)
        body = _extract_body(soup)
    except Exception as exc:  # noqa: BLE001
        logger.warning("enrich: failed for %s (%s)", item.url, exc)
        body = ""
    if body:
        item.raw_text = body[:max_chars]
        if not item.summary:
            item.summary = body[:300]
        item.metadata["enriched"] = True
        logger.info("enrich: %s -> %d chars", item.source, len(item.raw_text))
    else:
        item.metadata["enriched"] = False
    item.metadata["notable_quote"] = notable_quote(
        item.raw_text or item.summary or item.title)
    return item
