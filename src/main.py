"""ISDS thematic watcher — orchestrator.

Run: python -m src.main [--dry-run] [--since 7d] [--no-email] [--provider gemini|claude]

The whole run is defensive: a failing source or item is logged and skipped,
never fatal. With no network the sources return []; with no API key the
classifier uses its keyword fallback — so --dry-run works fully offline.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from datetime import datetime, timedelta, timezone

from . import config, render, state
from .classify import classify_item
from .email_send import send_digest
from .sources import all_sources

logger = logging.getLogger("isds.main")


def parse_since(spec: str) -> datetime:
    """Parse '7d', '14d', '48h', '30m' into a tz-aware UTC cutoff."""
    now = datetime.now(timezone.utc)
    m = re.fullmatch(r"\s*(\d+)\s*([dhmw])\s*", spec.lower())
    if not m:
        logger.warning("main: bad --since %r; defaulting to 7d", spec)
        return now - timedelta(days=7)
    n, unit = int(m.group(1)), m.group(2)
    delta = {"d": timedelta(days=n), "h": timedelta(hours=n),
             "m": timedelta(minutes=n), "w": timedelta(weeks=n)}[unit]
    return now - delta


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="isds-watcher")
    p.add_argument("--dry-run", action="store_true", help="don't send email; still write digest")
    p.add_argument("--since", default="7d", help="window, e.g. 7d / 14d / 48h / 1w (default 7d)")
    p.add_argument("--no-email", action="store_true", help="skip sending email")
    p.add_argument("--provider", default=None, help="override MODEL_PROVIDER (gemini|claude)")
    p.add_argument("--limit-sources", default=None, help="CSV of source names to run (testing)")
    p.add_argument("--verbose", action="store_true", help="DEBUG logging")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    cfg = config.load_config()
    st = state.load_state()
    since = parse_since(args.since)
    generated_at = datetime.now(timezone.utc)
    provider = args.provider or cfg.model_provider

    only = set(s.strip() for s in args.limit_sources.split(",")) if args.limit_sources else None

    stats = {
        "total_candidates": 0, "classified": 0, "above_threshold": 0,
        "per_source": {}, "dropped_sources": [], "threshold": cfg.threshold,
        "provider": provider,
    }

    # 1. Fetch + dedupe (per-source failure is non-fatal).
    new_candidates = []
    for src in all_sources(cfg):
        if only and src.name not in only:
            continue
        try:
            items = src.fetch(since)
        except Exception as exc:  # noqa: BLE001
            logger.error("source %s failed: %s", src.name, exc)
            items = []
        fresh = [it for it in items if not state.is_seen(st, src.name, it.source_id)]
        stats["per_source"][src.name] = len(fresh)
        if not items:
            stats["dropped_sources"].append(src.name)
        new_candidates.extend(fresh)
    stats["total_candidates"] = len(new_candidates)
    logger.info("main: %d new candidates across sources", len(new_candidates))

    # 2. Classify (per-item failure is non-fatal); mark every new item seen.
    classified = []
    for it in new_candidates:
        try:
            ci = classify_item(it, provider=provider)
        except Exception as exc:  # noqa: BLE001 - classify_item shouldn't raise, belt+braces
            logger.error("classify failed for %s: %s", it.source_id, exc)
            continue
        classified.append(ci)
        state.mark_seen(st, it.source, it.source_id, when=generated_at)
    stats["classified"] = len(classified)

    # 3. Filter + sort.
    matches = sorted(
        [c for c in classified if c.relevance_score >= cfg.threshold],
        key=lambda c: c.relevance_score, reverse=True,
    )
    stats["above_threshold"] = len(matches)

    # 4. Render + write.
    date_str = generated_at.strftime("%Y-%m-%d")
    html = render.render_digest(matches, generated_at, since, stats)
    digest_path = render.write_digest(html, date_str)

    # 5. Email (unless dry-run / no-email).
    email_status = "skipped"
    if not (args.dry_run or args.no_email):
        subject = f"ISDS Thematic Watch — {date_str} ({len(matches)} match{'' if len(matches)==1 else 'es'})"
        email_status = "sent" if send_digest(html, subject, cfg) else "failed"

    # 6. Persist state.
    state.save_state(st)

    # 7. Summary.
    print("\n=== ISDS Watcher run summary ===")
    print(f"window since:     {since.isoformat()}")
    print(f"provider:         {provider or 'keyword-fallback'}")
    for s, n in stats["per_source"].items():
        print(f"  source {s:<22} new={n}")
    if stats["dropped_sources"]:
        print(f"dropped/empty:    {', '.join(stats['dropped_sources'])}")
    print(f"new candidates:   {stats['total_candidates']}")
    print(f"classified:       {stats['classified']}")
    print(f"above threshold ({cfg.threshold}): {stats['above_threshold']}")
    print(f"digest:           {digest_path}")
    print(f"email:            {email_status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
