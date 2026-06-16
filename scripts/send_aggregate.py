"""Send one aggregated digest of every genuinely-relevant article surfaced across
all archived runs (the "first official" collective digest).

Reads digests/*_ISDS-Thematic-Watch/articles/*.md, de-duplicates by URL (keeping
the highest relevance), keeps only items at/above the relevance floor, renders the
standard digest, and emails it. Reusable: run any time to resend the running total.
"""
import datetime
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dateutil import parser as dateparser  # noqa: E402

from src import config, render  # noqa: E402
from src.classify import ClassifiedItem  # noqa: E402
from src.email_send import send_digest  # noqa: E402

UTC = datetime.timezone.utc
FLOOR = config.RELEVANCE_FLOOR  # only genuinely-relevant findings


def _field(text, label):
    m = re.search(rf"^- \*\*{label}:\*\* (.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def _block(text, header):
    m = re.search(rf"## {re.escape(header)}\s*\n(.+?)(?:\n## |\n---|\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def _display_title(raw, annotation):
    """Generic listing titles (italaw 'View case details', ITN issue headers) are
    useless; derive a real title from the first sentence of the annotation."""
    low = raw.strip().lower()
    if low.startswith(("view case", "itn issue", "itn special")) and annotation:
        first = re.split(r"(?<=[.!?])\s", annotation.strip())[0]
        first = first.rstrip(". ")
        return (first[:110].rstrip() + "…") if len(first) > 110 else (first or raw)
    return raw


def parse_article(path):
    t = open(path, encoding="utf-8").read()
    title = re.search(r"^# \d+\.\s*(.+)$", t, re.M)
    title = title.group(1).strip() if title else "(untitled)"
    url = _field(t, "Link") or ""
    rel = re.search(r"^- \*\*Relevance:\*\* (\d+)", t, re.M)
    relevance = int(rel.group(1)) if rel else 0
    rings_raw = _field(t, "Rings matched")
    rings = [r.strip() for r in rings_raw.split(",")
             if r.strip() and r.strip() != "—"] if rings_raw else []
    src = _field(t, "Source")
    src = re.split(r"\s—|\s\(", src)[0].strip().lower().replace(" ", "_") if src else "archive"
    date = _field(t, "Date")
    try:
        published = dateparser.parse(date).replace(tzinfo=UTC) if date and date != "n.d." else None
    except Exception:
        published = None
    annotation = _block(t, "Annotation")
    quote = _block(t, "Notable line (from source)").strip().strip(">").strip().strip('"“”')
    title = _display_title(title, annotation)
    return {
        "title": title, "url": url, "relevance": relevance, "rings": rings,
        "source": src, "published": published, "annotation": annotation, "quote": quote,
    }


def main():
    arts = sorted(glob.glob("digests/*_ISDS-Thematic-Watch/articles/*.md"))
    by_url = {}
    for p in arts:
        a = parse_article(p)
        if not a["url"]:
            continue
        if a["url"] not in by_url or a["relevance"] > by_url[a["url"]]["relevance"]:
            by_url[a["url"]] = a
    # keep only genuinely-relevant findings, best first
    found = [a for a in by_url.values() if a["relevance"] >= FLOOR]
    found.sort(key=lambda a: a["relevance"], reverse=True)

    items = []
    for a in found:
        ci = ClassifiedItem(a["source"], a["url"], a["url"], a["title"],
                            a["published"] or datetime.datetime.now(UTC),
                            a["annotation"], a["annotation"],
                            relevance_score=a["relevance"], matched_rings=a["rings"],
                            thematic_tags=[], digest_summary=a["annotation"])
        ci.metadata = {"notable_quote": a["quote"]} if a["quote"] else {}
        items.append(ci)

    now = datetime.datetime.now(UTC)
    stats = {
        "total_candidates": len(by_url), "classified": len(by_url),
        "above_threshold": sum(1 for a in found if a["relevance"] >= 40),
        "per_source": {}, "dropped_sources": [], "threshold": 40,
        "provider": "claude (aggregated across runs)",
    }
    for a in found:
        stats["per_source"][a["source"]] = stats["per_source"].get(a["source"], 0) + 1

    folder_url = f"{config.REPO_URL}/tree/main/digests"
    html = render.render_digest(items, now, now - datetime.timedelta(days=365),
                                stats, folder_url=folder_url)
    subject = (f"ISDS Thematic Watch — First Official Digest "
               f"({len(items)} finding{'' if len(items) == 1 else 's'})")
    ok = send_digest(html, subject, config.load_config())
    print(f"aggregated findings: {len(items)} | email: {'sent' if ok else 'FAILED'}")
    print("subject:", subject)
    for a in found:
        print(f"  [{a['relevance']:>3}] {a['title'][:70]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
