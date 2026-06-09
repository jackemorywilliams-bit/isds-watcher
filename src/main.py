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
from .classify import classify_item, keyword_score
from .email_send import send_digest
from .enrich import enrich, notable_quote as enrich_notable
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

    # 2. Cheap keyword pre-score to rank candidates, then enrich the most
    #    promising ones (fetch their source page) so the LLM and the digest have
    #    real substance to work with. Bounds polite fetches to ENRICH_TOP_N.
    ranked = sorted(new_candidates,
                    key=lambda it: keyword_score(it)["relevance_score"],
                    reverse=True)
    enrich_set = set(id(it) for it in ranked[:config.ENRICH_TOP_N])
    for it in ranked[:config.ENRICH_TOP_N]:
        enrich(it)

    # 3. Classify. LLM-classify the enriched top set; keyword-score the tail
    #    (keeps LLM volume bounded). Mark every new item seen either way.
    classified = []
    for it in new_candidates:
        try:
            if id(it) in enrich_set:
                ci = classify_item(it, provider=provider)
            else:
                ci = classify_item(it, provider=None)  # forces keyword fallback
            if not it.metadata.get("notable_quote"):
                it.metadata["notable_quote"] = enrich_notable(
                    it.raw_text or it.summary or it.title)
            ci.metadata = it.metadata
        except Exception as exc:  # noqa: BLE001 - belt & braces
            logger.error("classify failed for %s: %s", it.source_id, exc)
            continue
        classified.append(ci)
        state.mark_seen(st, it.source, it.source_id, when=generated_at)
    stats["classified"] = len(classified)

    # 4. Select what to surface: everything at/above threshold, but never an
    #    empty digest — backfill with the next-highest items down to the floor.
    ordered = sorted(classified, key=lambda c: c.relevance_score, reverse=True)
    above = [c for c in ordered if c.relevance_score >= cfg.threshold]
    stats["above_threshold"] = len(above)
    surfaced = list(above)
    if len(surfaced) < config.MIN_DIGEST_ITEMS:
        for c in ordered:
            if c in surfaced:
                continue
            if c.relevance_score >= config.RELEVANCE_FLOOR:
                surfaced.append(c)
            if len(surfaced) >= config.MIN_DIGEST_ITEMS:
                break

    # 5. Render + write the dated archive folder (one file per surfaced item).
    date_str = generated_at.strftime("%Y-%m-%d")
    folder_rel = f"digests/{render.folder_name(date_str)}"
    folder_url = f"{config.REPO_URL}/tree/main/{folder_rel}"
    html = render.render_digest(surfaced, generated_at, since, stats, folder_url=folder_url)
    folder_path = render.write_digest_folder(html, surfaced, generated_at, stats)
    digest_path = render.write_digest(html, date_str)

    # 6. Email (unless dry-run / no-email).
    email_status = "skipped"
    if not (args.dry_run or args.no_email):
        subject = (f"ISDS Thematic Watch — {date_str} "
                   f"({len(surfaced)} item{'' if len(surfaced)==1 else 's'}, "
                   f"{len(above)} at threshold)")
        email_status = "sent" if send_digest(html, subject, cfg) else "failed"

    # 7. Persist state.
    state.save_state(st)

    # 8. Summary.
    print("\n=== ISDS Watcher run summary ===")
    print(f"window since:     {since.isoformat()}")
    print(f"provider:         {provider or 'keyword-fallback'}")
    for s, n in stats["per_source"].items():
        print(f"  source {s:<22} new={n}")
    if stats["dropped_sources"]:
        print(f"dropped/empty:    {', '.join(stats['dropped_sources'])}")
    print(f"new candidates:   {stats['total_candidates']}")
    print(f"classified:       {stats['classified']}")
    print(f"at/above threshold ({cfg.threshold}): {stats['above_threshold']}")
    print(f"surfaced in digest: {len(surfaced)}")
    print(f"folder:           {folder_path}")
    print(f"digest:           {digest_path}")
    print(f"email:            {email_status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
