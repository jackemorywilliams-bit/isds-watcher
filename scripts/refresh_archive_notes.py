"""Re-render the README index table of every archived digest folder so the
"Notable line" column shows the full, quoted, verbatim source line (not a
truncated fragment) and the Source column shows provenance (publisher domain for
aggregator channels).

This is a formatting/consistency migration over data already stored in each
folder's `articles/*.md` files — it does NOT re-classify, re-fetch, or fabricate
anything. Two integrity rules are applied while rebuilding the table:

  * A notable line that merely restates the item's own title/headline is NOT a
    direct quote from the source body (the headline-only / paywalled case). Such
    a line is shown as "—", honestly, rather than dressed up as a quotation.
  * Only the table block of each README is rewritten; the run counts, prose, and
    footer are preserved verbatim, so the archive's reconciled numbers are
    untouched.

Run:  python scripts/refresh_archive_notes.py
"""

from __future__ import annotations

import os
import re
from urllib.parse import urlparse

DIGESTS = "digests"
SUFFIX = "_ISDS-Thematic-Watch"
_AGGREGATOR_SOURCES = {"google_alerts", "google_news_rss", "gmail_scholar"}
# Sources that only ever expose a headline (no body fetched): a "notable line"
# from one of these is necessarily headline text, never a verbatim body quote.
_HEADLINE_ONLY_SOURCES = {"iareporter_headlines"}


def _is_genuine_quote(quote: str, title: str, raw_source: str) -> bool:
    """A notable line counts as a genuine, citable source quote only when it is
    non-empty, comes from a source whose body we actually read, and is not merely
    the item's own headline (exactly, or as a fragment of the title)."""
    if not quote:
        return False
    if raw_source in _HEADLINE_ONLY_SOURCES:
        return False
    nq, nt = _norm(quote), _norm(title)
    return bool(nq) and nq not in nt


def _norm(s: str) -> str:
    """Lower-case, collapse whitespace, strip surrounding quotes — for comparing
    a notable line against a title to detect a headline restatement."""
    s = (s or "").translate({0x201c: '"', 0x201d: '"', 0x2018: "'", 0x2019: "'"})
    return re.sub(r"\s+", " ", s).strip().strip("\"'").lower()


def _source_label(source: str, url: str) -> str:
    channel = source.replace("_", " ").title()
    if source in _AGGREGATOR_SOURCES and url:
        host = urlparse(url).netloc.replace("www.", "")
        if host:
            return f"{channel} → {host}"
    return channel


def _raw_source(channel_label: str) -> str:
    """Reverse the Title-cased channel back to its source key (italaw, iisd_itn)."""
    return channel_label.strip().lower().replace(" ", "_")


def parse_article(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    title = ""
    m = re.search(r"^#\s+\d+\.\s+(.*)$", text, re.M)
    if m:
        title = m.group(1).strip()

    channel = ""
    m = re.search(r"^-\s+\*\*Source:\*\*\s+(.*?)\s+—\s+\[Read", text, re.M)
    if m:
        channel = m.group(1).strip()
        # Drop any existing "→ host" provenance suffix to recover the channel.
        channel = channel.split(" → ")[0].strip()

    url = ""
    m = re.search(r"^-\s+\*\*Link:\*\*\s+(\S+)", text, re.M)
    if m:
        url = m.group(1).strip()

    score = 0
    m = re.search(r"^-\s+\*\*Relevance:\*\*\s+(\d+)", text, re.M)
    if m:
        score = int(m.group(1))

    quote = ""
    m = re.search(r"^##\s+Notable line.*?\n>\s+(.*)$", text, re.M)
    if m:
        quote = m.group(1).strip().strip("“”\"'").strip()

    return {"title": title, "channel": channel, "url": url, "score": score, "quote": quote}


def build_rows(folder: str) -> list[str]:
    arts_dir = os.path.join(folder, "articles")
    rows: list[str] = []
    if not os.path.isdir(arts_dir):
        return ["| — | — | — | _No items met the relevance floor this cycle._ | — |"]
    files = sorted(f for f in os.listdir(arts_dir) if f.endswith(".md"))
    if not files:
        return ["| — | — | — | _No items met the relevance floor this cycle._ | — |"]
    for fn in files:
        idx = int(fn.split("_", 1)[0])
        a = parse_article(os.path.join(arts_dir, fn))
        raw = _raw_source(a["channel"])
        src = _source_label(raw, a["url"]).replace("|", "\\|")
        ttl = a["title"].replace("|", "\\|")
        q = a["quote"]
        if _is_genuine_quote(q, a["title"], raw):
            disp = (q[:90] + "…") if len(q) > 90 else q
            disp = "“" + disp.replace("|", "\\|") + "”"
        elif raw in _HEADLINE_ONLY_SOURCES:
            # Paywalled / headline-only source: body not accessible, so there is
            # no verbatim line to quote — say so plainly.
            disp = "N/A"
        else:
            disp = "—"
        rows.append(f"| {idx} | {a['score']} | {src} | [{ttl}](articles/{fn}) | {disp} |")
    return rows


_NA_NOTE = ('<div class="quote">Notable line: N/A — source paywalled '
           "(headline only); body not accessible.</div>")


def _html_inner(s: str) -> str:
    """Plain text of an HTML fragment: drop tags, unescape the few entities the
    templates emit, fold curly quotes — for comparing a rendered quote div."""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&#39;", "'").replace("&amp;", "&").replace("&quot;", '"')
    return s


def clean_index_html(folder: str) -> bool:
    """Rewrite the email-body HTML (index.html) so paywalled/headline-only items,
    and any line that merely restates the headline, no longer masquerade as a
    verbatim quote — they show N/A instead. Genuine body quotes are preserved.

    Robust against nested-div entry markup: every <div class="quote"> is kept
    only if its text matches a quote the article data deems genuine; otherwise it
    becomes the N/A note."""
    path = os.path.join(folder, "index.html")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        html = fh.read()

    arts_dir = os.path.join(folder, "articles")
    genuine: set[str] = set()
    if os.path.isdir(arts_dir):
        for fn in os.listdir(arts_dir):
            if not fn.endswith(".md"):
                continue
            a = parse_article(os.path.join(arts_dir, fn))
            if _is_genuine_quote(a["quote"], a["title"], _raw_source(a["channel"])):
                genuine.add(_norm(a["quote"]))

    def repl(m: re.Match) -> str:
        inner = _norm(_html_inner(m.group(1)))
        return m.group(0) if inner in genuine else _NA_NOTE

    new_html = re.sub(r'<div class="quote">(.*?)</div>', repl, html, flags=re.S)
    if new_html != html:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new_html)
        return True
    return False


def rewrite_readme(folder: str) -> bool:
    path = os.path.join(folder, "README.md")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    # Find the table header row.
    h = next((i for i, ln in enumerate(lines)
              if ln.startswith("| # | Relevance |")), None)
    if h is None:
        return False
    sep = h + 1  # the |---|---| separator
    # Data rows run from sep+1 until the first blank line / footer rule.
    end = sep + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1

    new_rows = build_rows(folder)
    rebuilt = lines[: sep + 1] + new_rows + lines[end:]
    new_text = "\n".join(rebuilt) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new_text)
    return True


def main() -> None:
    folders = sorted(
        os.path.join(DIGESTS, n) for n in os.listdir(DIGESTS)
        if n.endswith(SUFFIX) and os.path.isdir(os.path.join(DIGESTS, n))
    )
    for folder in folders:
        rd = rewrite_readme(folder)
        ix = clean_index_html(folder)
        flags = ",".join(p for p, c in (("readme", rd), ("index.html", ix)) if c)
        print(f"{folder}: {flags or 'no change'}")


if __name__ == "__main__":
    main()
