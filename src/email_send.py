"""Send the HTML digest over SMTP (Gmail SSL on 465 by default)."""

from __future__ import annotations

import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import config
from .config import missing_email_secrets

logger = logging.getLogger("isds.email")


def _html_to_text(html: str) -> str:
    text = re.sub(r"<style.*?</style>", "", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+\n", "\n", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def send_digest(html: str, subject: str, cfg, recipients=None) -> bool:
    """Send the digest. Returns True on success, False otherwise. Never raises."""
    recipients = recipients or config.RECIPIENTS
    missing = missing_email_secrets(cfg)
    if missing:
        logger.error("email: missing secrets %s; cannot send", missing)
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = cfg.smtp_user
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(_html_to_text(html), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP_SSL(cfg.smtp_host, cfg.smtp_port, timeout=30) as server:
            server.login(cfg.smtp_user, cfg.smtp_pass)
            server.sendmail(cfg.smtp_user, recipients, msg.as_string())
        logger.info("email: sent '%s' to %s", subject, recipients)
        return True
    except Exception as exc:  # noqa: BLE001 - email failure must not crash run
        logger.error("email: send failed (%s)", exc)
        return False
