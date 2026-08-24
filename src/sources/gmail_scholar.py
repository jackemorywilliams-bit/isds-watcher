"""Google Scholar alert emails (Gmail / IMAP) source.

Google Scholar emails the operator a digest of new papers matching their saved
Scholar alerts. This source reads those emails from a dedicated Gmail label via
IMAP (read scope), parses each alert email into the several papers it lists, and
yields one CandidateItem per paper.

Fully autonomous and INACTIVE-SAFE: with no GMAIL_ALERT_USER / GMAIL_ALERT_PASS
in the environment the source logs once and returns []. It never raises: IMAP
errors, a bad message, or a parse failure are logged and skipped, and the IMAP
connection is always closed in a finally.

The HTML->entries parsing lives in the module-level ``parse_scholar_email`` so it
is unit-testable with no network and no credentials.
"""

from __future__ import annotations

import email
import imaplib
import logging
import os
from datetime import datetime
from email.header import decode_header, make_header
from urllib.parse import urlparse, parse_qs

from .base import (
    CandidateItem,
    Source,
    parse_date,
    strip_html,
)

logger = logging.getLogger("isds.sources.gmail_scholar")

# Sender variants Google Scholar uses for alert emails.
_SCHOLAR_SENDERS = (
    "scholaralerts-noreply@google.com",
    "scholaralerts-noreply",
    "scholar-noreply",
)


def resolve_redirect(link: str) -> str:
    """Extract the real publisher URL from a Google Scholar redirect link.

    Scholar wraps result links as scholar.google.com/scholar_url?url=<REAL>&...
    or google.com/url?...&url=<REAL>. Pull the underlying URL out of the query.
    Returns the link unchanged if it carries no such parameter.
    """
    if not link:
        return link
    try:
        q = parse_qs(urlparse(link).query)
        for key in ("url", "q"):
            if q.get(key):
                return q[key][0]
    except Exception:  # noqa: BLE001 - never let a malformed URL crash a run
        pass
    return link


def parse_scholar_email(html: str) -> list[dict]:
    """Parse a Scholar alert email body into a list of paper entries.

    Each Scholar result is an <h3> containing an <a href="..."> with the paper
    title; the href is a Google redirect we resolve to the publisher URL. The
    text immediately following the title (author/snippet lines) is captured as
    the snippet. Returns a list of dicts: {title, url, snippet}.

    Never raises; returns [] on any problem.
    """
    if not html:
        return []
    try:
        from bs4 import BeautifulSoup
    except Exception:  # pragma: no cover - dependency missing
        logger.warning("parse_scholar_email: bs4 not available")
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception as exc:  # noqa: BLE001
        logger.warning("parse_scholar_email: could not parse HTML (%s)", exc)
        return []

    entries: list[dict] = []
    for h3 in soup.find_all("h3"):
        try:
            anchor = h3.find("a", href=True)
            if anchor is None:
                continue
            title = anchor.get_text(separator=" ", strip=True)
            url = resolve_redirect(anchor["href"])
            if not title or not url:
                continue

            # The snippet/author lines follow the <h3>. Walk forward over the
            # next siblings, gathering text until the next result heading.
            snippet_parts: list[str] = []
            for sib in h3.find_next_siblings():
                if getattr(sib, "name", None) == "h3":
                    break
                text = sib.get_text(separator=" ", strip=True) if hasattr(sib, "get_text") else str(sib).strip()
                if text:
                    snippet_parts.append(text)
            snippet = strip_html(" ".join(snippet_parts)).strip()

            entries.append({"title": title, "url": url, "snippet": snippet})
        except Exception as exc:  # noqa: BLE001 - one bad result must not kill the rest
            logger.warning("parse_scholar_email: skipping a result (%s)", exc)
            continue

    return entries


def _decode_header(value) -> str:
    """Best-effort decode of a possibly RFC2047-encoded header. Never raises."""
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:  # noqa: BLE001
        return str(value)


def _get_html_body(msg) -> str:
    """Return the text/html body of an email.message.Message, else ''."""
    try:
        if msg.is_multipart():
            html = ""
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        return payload.decode(charset, errors="replace")
            return html
        if msg.get_content_type() == "text/html":
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="replace")
    except Exception as exc:  # noqa: BLE001
        logger.warning("gmail_scholar: could not extract HTML body (%s)", exc)
    return ""


class GmailScholarSource(Source):
    name = "gmail_scholar"
    priority = "primary"

    def fetch(self, since: datetime) -> list[CandidateItem]:
        user = os.environ.get("GMAIL_ALERT_USER", "").strip()
        password = os.environ.get("GMAIL_ALERT_PASS", "").strip()
        if not user or not password:
            logger.info("gmail_scholar: no credentials, inactive")
            return []

        label = os.environ.get("GMAIL_ALERT_LABEL", "scholar-alerts").strip() or "scholar-alerts"
        host = os.environ.get("GMAIL_IMAP_HOST", "imap.gmail.com").strip() or "imap.gmail.com"

        conn = None
        try:
            conn = imaplib.IMAP4_SSL(host)
            conn.login(user, password)

            # Find the Scholar alerts wherever they live. Gmail exposes labels as
            # IMAP mailboxes, but the operator's alerts are not guaranteed to carry
            # the dedicated label — that requires a Gmail filter the operator may
            # never have set up, so the label mailbox reads empty even while the
            # alerts are arriving. "[Gmail]/All Mail" contains every message, so a
            # sender-scoped search there catches the alerts whether or not they are
            # labeled; the configured label and INBOX are tried as fallbacks in case
            # All Mail is not selectable (e.g. a localized mailbox name). The search
            # is always scoped to the Scholar sender, so no unrelated mail is read.
            uids: list[bytes] = []
            used_mailbox = None
            for mailbox in ('"[Gmail]/All Mail"', f'"{label}"', "INBOX"):
                status, _ = conn.select(mailbox, readonly=True)
                if status != "OK":
                    continue
                found = self._search_uids(conn, since)
                if found:
                    uids = found
                    used_mailbox = mailbox
                    break
            if not uids:
                logger.info(
                    "gmail_scholar: no matching Scholar messages (searched All Mail, label %r, INBOX)",
                    label,
                )
                return []
            logger.info("gmail_scholar: %d message(s) via %s", len(uids), used_mailbox)

            items: list[CandidateItem] = []
            seen: set[str] = set()
            for uid in uids:
                try:
                    new_items = self._fetch_message(conn, uid, since)
                except Exception as exc:  # noqa: BLE001 - one bad message must not kill the run
                    logger.warning("gmail_scholar: skipping message %r (%s)", uid, exc)
                    continue
                for item in new_items:
                    if item.url in seen:
                        continue
                    if item.published is not None and item.published < since:
                        continue
                    seen.add(item.url)
                    items.append(item)

            logger.info("gmail_scholar: %d items from %d message(s)", len(items), len(uids))
            return items
        except Exception as exc:  # noqa: BLE001 - total failure: log and return []
            logger.warning("gmail_scholar: fetch failed (%s)", exc)
            return []
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:  # noqa: BLE001
                    pass
                try:
                    conn.logout()
                except Exception:  # noqa: BLE001
                    pass

    def _search_uids(self, conn, since: datetime) -> list[bytes]:
        """SEARCH the selected mailbox for Scholar alerts SINCE ``since``.

        IMAP SINCE has day granularity; the per-item date filter in fetch()
        applies the precise cutoff. Tries each known sender variant and unions
        the results. Returns a de-duplicated, ordered list of message ids.
        """
        date_str = since.strftime("%d-%b-%Y")
        found: list[bytes] = []
        seen_ids: set[bytes] = set()
        for sender in _SCHOLAR_SENDERS:
            try:
                status, data = conn.search(None, "SINCE", date_str, "FROM", sender)
            except Exception as exc:  # noqa: BLE001
                logger.warning("gmail_scholar: search failed for %r (%s)", sender, exc)
                continue
            if status != "OK" or not data:
                continue
            for raw in (data[0] or b"").split():
                if raw not in seen_ids:
                    seen_ids.add(raw)
                    found.append(raw)
        return found

    def _fetch_message(self, conn, uid: bytes, since: datetime) -> list[CandidateItem]:
        """Fetch one message, parse its Scholar entries into CandidateItems."""
        status, data = conn.fetch(uid, "(RFC822)")
        if status != "OK" or not data or not data[0]:
            logger.warning("gmail_scholar: fetch returned %s for %r", status, uid)
            return []

        raw_bytes = data[0][1]
        if not raw_bytes:
            return []
        msg = email.message_from_bytes(raw_bytes)

        published = parse_date(_decode_header(msg.get("Date")))
        html = _get_html_body(msg)
        entries = parse_scholar_email(html)

        items: list[CandidateItem] = []
        for entry in entries:
            url = entry.get("url") or ""
            title = entry.get("title") or ""
            snippet = entry.get("snippet") or ""
            if not url or not title:
                continue
            items.append(
                CandidateItem(
                    source=self.name,
                    source_id=url,
                    url=url,
                    title=title,
                    published=published,
                    summary=snippet,
                    raw_text=snippet,
                    metadata={"via": "google_scholar"},
                )
            )
        return items
