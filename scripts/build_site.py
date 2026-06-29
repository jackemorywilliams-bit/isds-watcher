#!/usr/bin/env python3
"""Build the ISDS Thematic Watcher static website into ``docs/``.

Pure standard library + Jinja2 (no other third-party deps). Regenerates the
landing page, the methodology page, the digest-archive index, and one page per
dated digest, plus the shared stylesheet and the ``.nojekyll`` marker.

Run from the repository root:

    python scripts/build_site.py          # or:  python -m scripts.build_site

The script is idempotent: re-running overwrites the generated files in place.
It never fabricates digest content; if a digest folder has an unexpected shape
it degrades gracefully and prints a warning.
"""

from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# The backtest harness lives alongside this script. Ensure its directory is
# importable whether the build is launched as ``python scripts/build_site.py``
# (dir already on sys.path) or as ``python -m scripts.build_site`` (it is not).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from backtest import run_backtest  # noqa: E402

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "scripts" / "site_templates"
DOCS = REPO_ROOT / "docs"
DIGESTS_SRC = REPO_ROOT / "digests"
METHODOLOGY_MD = REPO_ROOT / "METHODOLOGY.md"

REPO_URL = "https://github.com/jackemorywilliams-bit/isds-watcher"

# Mapping from the fingerprint ring keys to short human labels for badges.
RING_LABELS = {
    "ip_as_investment": "IP-as-investment",
    "judicial_or_regulatory_measure": "Judicial / regulatory measure",
    "jurisdictional_admissibility": "Jurisdictional / admissibility",
}


# --------------------------------------------------------------------------- #
# Minimal Markdown -> HTML conversion
# --------------------------------------------------------------------------- #
def _inline(text: str) -> str:
    """Convert inline Markdown (links, bold, italic, code) to safe HTML.

    The input is HTML-escaped first, then a small set of inline constructs are
    re-introduced as tags. Only what METHODOLOGY.md and the article files use is
    handled — this is deliberately not a full Markdown engine.
    """
    text = html.escape(text, quote=False)

    # Links: [label](url)
    def link_sub(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{html.escape(url, quote=True)}"{ext}>{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_sub, text)

    # Inline code: `code`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Bold: **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text* (single asterisks, not part of a bold run)
    text = re.sub(r"(?<!\*)\*(?!\s)([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    return text


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


@dataclass
class TocItem:
    level: int      # 2 for ##, 3 for ###
    text: str
    anchor: str


def markdown_to_html(md: str, collect_toc: bool = False):
    """Convert a Markdown document to an HTML fragment.

    Supports: ATX headings (#..######), unordered lists (- / *), blockquotes
    (>), horizontal rules (---), paragraphs, and the inline constructs above.
    Tables are rendered as simple HTML tables. Returns ``(html, toc)`` where
    ``toc`` is a list of :class:`TocItem` for level-2/3 headings (empty unless
    ``collect_toc``).
    """
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    toc: list[TocItem] = []

    i = 0
    n = len(lines)

    def close_para(buf: list[str]) -> None:
        if buf:
            out.append("<p>" + _inline(" ".join(buf).strip()) + "</p>")
            buf.clear()

    para: list[str] = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line ends a paragraph.
        if not stripped:
            close_para(para)
            i += 1
            continue

        # Horizontal rule.
        if re.fullmatch(r"-{3,}", stripped):
            close_para(para)
            out.append("<hr>")
            i += 1
            continue

        # Headings.
        hm = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if hm:
            close_para(para)
            level = len(hm.group(1))
            htext = hm.group(2).strip()
            anchor = _slugify(htext)
            if collect_toc and level in (2, 3):
                toc.append(TocItem(level=level, text=re.sub(r"[*`]", "", htext), anchor=anchor))
            inner = _inline(htext)
            if level in (2, 3) and collect_toc:
                out.append(f'<h{level} id="{anchor}">{inner}</h{level}>')
            else:
                out.append(f"<h{level}>{inner}</h{level}>")
            i += 1
            continue

        # Blockquote (one or more consecutive > lines).
        if stripped.startswith(">"):
            close_para(para)
            quote_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote><p>" + _inline(" ".join(quote_lines).strip()) + "</p></blockquote>")
            continue

        # Table (pipe-delimited with a separator row).
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            close_para(para)
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{_inline(c)}</th>" for c in header)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        # Unordered list.
        if re.match(r"^[-*]\s+", stripped):
            close_para(para)
            items: list[str] = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            li = "".join(f"<li>{_inline(it.strip())}</li>" for it in items)
            out.append(f"<ul>{li}</ul>")
            continue

        # Otherwise accumulate into the current paragraph.
        para.append(stripped)
        i += 1

    close_para(para)
    return "\n".join(out), toc


# --------------------------------------------------------------------------- #
# Methodology parsing (memo header split out)
# --------------------------------------------------------------------------- #
@dataclass
class Memo:
    fields: list[tuple[str, str]]  # (label, value) e.g. ("TO", "Dr. ...")
    body_html: str
    toc: list[TocItem]


def parse_methodology(md_path: Path) -> Memo | None:
    if not md_path.exists():
        print(f"  ! METHODOLOGY.md not found at {md_path}; skipping methodology page")
        return None
    raw = md_path.read_text(encoding="utf-8")

    # The memo header is the run of leading "**LABEL:** value" lines before the
    # first "---" rule. Split it from the body.
    lines = raw.replace("\r\n", "\n").split("\n")
    fields: list[tuple[str, str]] = []
    body_start = 0
    for idx, line in enumerate(lines):
        s = line.strip()
        m = re.match(r"^\*\*([A-Z/ ]+):\*\*\s*(.*)$", s)
        if m:
            fields.append((m.group(1).strip(), m.group(2).strip()))
            continue
        if s == "" and fields and idx + 1 < len(lines):
            # allow a blank line then the closing rule
            continue
        if re.fullmatch(r"-{3,}", s) and fields:
            body_start = idx + 1
            break
        if fields and s and not s.startswith("**"):
            # header ended without a rule; treat from here as body
            body_start = idx
            break

    body_md = "\n".join(lines[body_start:]).lstrip("\n")
    body_html, toc = markdown_to_html(body_md, collect_toc=True)

    # Render the memo field values with inline markdown (RE field has italics).
    fields = [(label, _inline(value)) for label, value in fields]
    return Memo(fields=fields, body_html=body_html, toc=toc)


# --------------------------------------------------------------------------- #
# Digest / article parsing
# --------------------------------------------------------------------------- #
@dataclass
class Entry:
    number: int
    title: str
    source: str
    read_original_url: str
    date: str
    url: str
    relevance: int
    band: str           # HIGH / MEDIUM / LOW / WATCH
    rings: list[str]    # raw ring keys (or labels if not recognised)
    ring_labels: list[str]
    tags: list[str]
    citation: str
    annotation: str
    notable_line: str


@dataclass
class Digest:
    date: str           # YYYY-MM-DD
    slug: str           # folder name
    title: str
    summary_html: str
    entries: list[Entry] = field(default_factory=list)
    surfaced: int = 0
    candidates: int | None = None
    classifier: str | None = None
    threshold: int | None = None
    # Run counts, defined identically to the email and meta.json:
    #   screened = candidates scored that cycle; matches = items >= threshold;
    #   accepted = matches + watch-list leads actually shown. Any may be None.
    accepted: int | None = None
    matches: int | None = None
    screened: int | None = None
    # Per-source fresh-candidate and surfaced counts from meta.json. Older runs
    # predate per-source counting, so these are empty dicts there (guarded for).
    per_source: dict[str, int] = field(default_factory=dict)
    accepted_by_source: dict[str, int] = field(default_factory=dict)

    @property
    def accepted_str(self) -> str:
        return str(self.accepted) if self.accepted is not None else "—"

    @property
    def matches_str(self) -> str:
        return str(self.matches) if self.matches is not None else "—"

    @property
    def screened_str(self) -> str:
        return str(self.screened) if self.screened is not None else "—"

    @property
    def sources(self) -> str:
        """Distinct catalogue source(s) the accepted items came from — shown in
        place of the classifier, so a reader sees which feed surfaced the week's
        developments (e.g. "Italaw, Iareporter Headlines")."""
        seen: list[str] = []
        for e in self.entries:
            ch = (e.source or "").split(" → ")[0].strip()
            if ch and ch not in seen:
                seen.append(ch)
        return ", ".join(seen)


def _field_value(body: str, label: str) -> str:
    """Pull a '- **Label:** value' line value from an article body."""
    m = re.search(rf"^- \*\*{re.escape(label)}:\*\*\s*(.*)$", body, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _section(body: str, header: str) -> str:
    """Return the text of a '## Header' section up to the next '## ' or rule."""
    pat = rf"^##\s+{re.escape(header)}\s*$(.*?)(?=^##\s+|^---\s*$|\Z)"
    m = re.search(pat, body, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def parse_article(path: Path) -> Entry | None:
    body = path.read_text(encoding="utf-8")

    h1 = re.search(r"^#\s+(.*)$", body, re.MULTILINE)
    if not h1:
        print(f"    ! {path.name}: no H1 title; skipping")
        return None
    raw_title = h1.group(1).strip()
    nm = re.match(r"^(\d+)\.\s*(.*)$", raw_title)
    number = int(nm.group(1)) if nm else 0
    title = nm.group(2).strip() if nm else raw_title

    # Source line: "Source Name — [Read the original ↗](url)"
    source_raw = _field_value(body, "Source")
    src_name = source_raw
    read_url = ""
    sm = re.match(r"^(.*?)\s*—\s*\[[^\]]*\]\(([^)]+)\)\s*$", source_raw)
    if sm:
        src_name = sm.group(1).strip()
        read_url = sm.group(2).strip()

    date = _field_value(body, "Date")
    url = _field_value(body, "Link")
    if not read_url:
        read_url = url

    rel_raw = _field_value(body, "Relevance")
    rm = re.match(r"^(\d+)\s*(?:\(([^)]+)\))?", rel_raw)
    relevance = int(rm.group(1)) if rm else 0
    band = (rm.group(2).strip() if rm and rm.group(2) else "").upper()

    rings_raw = _field_value(body, "Rings matched")
    rings: list[str] = []
    if rings_raw and rings_raw != "—":
        rings = [r.strip() for r in rings_raw.split(",") if r.strip() and r.strip() != "—"]
    ring_labels = [RING_LABELS.get(r, r.replace("_", " ")) for r in rings]

    tags_raw = _field_value(body, "Tags")
    tags: list[str] = []
    if tags_raw and tags_raw != "—":
        tags = [t.strip() for t in tags_raw.split(",") if t.strip() and t.strip() != "—"]

    citation = _section(body, "Citation").lstrip("> ").strip()
    # Strip blockquote markers from the citation lines.
    citation = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in citation.split("\n")).strip()

    annotation = _section(body, "Annotation")

    notable = _section(body, "Notable line (from source)")
    notable = "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in notable.split("\n")).strip()
    notable = notable.strip().strip("“”\"")

    return Entry(
        number=number,
        title=title,
        source=src_name,
        read_original_url=read_url,
        date=date,
        url=url,
        relevance=relevance,
        band=band or _band_from_score(relevance),
        rings=rings,
        ring_labels=ring_labels,
        tags=tags,
        citation=citation,
        annotation=annotation,
        notable_line=notable,
    )


def _band_from_score(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def _ordered_article_paths(digest_dir: Path) -> list[Path]:
    """Determine which article files belong to this digest, in order.

    The digest's own README.md is authoritative about which files belong (a
    folder can accumulate stale files from an earlier run of the same day). We
    parse the README's links to ``articles/<file>.md``; if that fails, fall back
    to all numbered article files sorted by leading number.
    """
    articles_dir = digest_dir / "articles"
    if not articles_dir.is_dir():
        return []

    readme = digest_dir / "README.md"
    ordered: list[Path] = []
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        seen: set[str] = set()
        for m in re.finditer(r"\(articles/([^)]+\.md)\)", text):
            name = m.group(1)
            if name in seen:
                continue
            seen.add(name)
            p = articles_dir / name
            if p.exists():
                ordered.append(p)
        if ordered:
            return ordered

    # Fallback: every numbered article, sorted by its leading number.
    print(f"    ! {digest_dir.name}: README article list unavailable; "
          "falling back to all numbered articles")
    files = [p for p in articles_dir.glob("*.md") if re.match(r"^\d+_", p.name)]

    def sort_key(p: Path):
        m = re.match(r"^(\d+)_", p.name)
        return (int(m.group(1)) if m else 9999, p.name)

    return sorted(files, key=sort_key)


def _parse_digest_summary(digest_dir: Path) -> tuple[str, int | None, str | None, int | None]:
    """Extract a short run-summary from the digest README (graceful if absent)."""
    readme = digest_dir / "README.md"
    candidates = classifier = threshold = None
    summary_html = ""
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        m = re.search(
            r"Annotated digest of \*\*(\d+)\*\* surfaced items \(screened from (\d+) "
            r"candidates; classifier: (\w+); threshold (\d+)\)",
            text,
        )
        if m:
            candidates = int(m.group(2))
            classifier = m.group(3)
            threshold = int(m.group(4))
        # Use the first descriptive sentence as a summary paragraph.
        for line in text.split("\n"):
            s = line.strip()
            if s.lower().startswith("annotated digest"):
                summary_html, _ = markdown_to_html(s)
                break
    return summary_html, candidates, classifier, threshold


def _resolve_counts(digest_dir: Path, fallback_screened: int | None,
                    fallback_accepted: int) -> tuple[int | None, int | None, int | None,
                                                     dict[str, int], dict[str, int]]:
    """Resolve ``(accepted, matches, screened, per_source, accepted_by_source)`` for a
    digest, defined identically to the email and meta.json: ``screened`` = candidates
    scored; ``matches`` = items at/above threshold; ``accepted`` = matches plus
    watch-list leads shown. ``per_source`` / ``accepted_by_source`` map each catalogue
    source to its fresh-candidate / surfaced count (empty for runs that predate
    per-source counting).

    Order of preference:
    1. ``meta.json`` (schema {"date","screened","matches","watch_list_leads","accepted",
       optionally "per_source","accepted_by_source"}).
    2. The folder's ``index.html`` footer (current "Screened:" / "Matches (>=N):",
       or legacy "Candidates screened:" / "At or above threshold (N):").
    3. README-derived fallbacks (candidate count for screened, surfaced-entry count
       for accepted; matches defaults to 0 when otherwise unknown).

    Robust by design: a missing or malformed source is skipped, never fatal.
    """
    accepted: int | None = None
    matches: int | None = None
    screened: int | None = None
    per_source: dict[str, int] = {}
    accepted_by_source: dict[str, int] = {}

    # 1. meta.json (authoritative when present).
    meta_path = digest_dir / "meta.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if "matches" in meta:  # current schema: accepted = shown, matches = >= thr
                if isinstance(meta.get("accepted"), int):
                    accepted = meta["accepted"]
                if isinstance(meta.get("matches"), int):
                    matches = meta["matches"]
            else:  # legacy schema: accepted == matches, surfaced == shown
                if isinstance(meta.get("surfaced"), int):
                    accepted = meta["surfaced"]
                if isinstance(meta.get("accepted"), int):
                    matches = meta["accepted"]
            if isinstance(meta.get("screened"), int):
                screened = meta["screened"]
            # Per-source maps are optional (absent in older runs); keep only int values.
            ps = meta.get("per_source")
            if isinstance(ps, dict):
                per_source = {str(k): v for k, v in ps.items() if isinstance(v, int)}
            abs_ = meta.get("accepted_by_source")
            if isinstance(abs_, dict):
                accepted_by_source = {str(k): v for k, v in abs_.items() if isinstance(v, int)}
        except (ValueError, OSError) as exc:
            print(f"    ! {digest_dir.name}: meta.json unreadable ({exc}); "
                  "falling back to index.html footer")

    # 2. index.html footer (fill any gaps left by meta.json).
    if matches is None or screened is None:
        index_html = digest_dir / "index.html"
        if index_html.exists():
            try:
                text = index_html.read_text(encoding="utf-8")
            except OSError:
                text = ""
            if screened is None:
                ms = re.search(r"(?:Candidates screened|Screened):\s*(\d+)", text)
                if ms:
                    screened = int(ms.group(1))
            if matches is None:
                mm = re.search(
                    r"(?:At or above threshold\s*\(\d+\)|Matches\s*\(\D*\d+\)):\s*(\d+)",
                    text)
                if mm:
                    matches = int(mm.group(1))

    # 3. README-derived fallbacks.
    if screened is None:
        screened = fallback_screened
    if matches is None:
        matches = 0
    if accepted is None:
        accepted = fallback_accepted  # surfaced-entry count = matches + leads shown

    return accepted, matches, screened, per_source, accepted_by_source


def parse_digest(digest_dir: Path) -> Digest | None:
    m = re.match(r"^(\d{4}-\d{2}-\d{2})_", digest_dir.name)
    if not m:
        print(f"  ! {digest_dir.name}: unexpected folder name; skipping")
        return None
    date = m.group(1)

    # A folder with no article files is a valid 0-article cycle, not an error:
    # it still gets its own page and a clean "no developments" empty state.
    paths = _ordered_article_paths(digest_dir)

    entries: list[Entry] = []
    for p in paths:
        e = parse_article(p)
        if e:
            entries.append(e)

    # Renumber sequentially in case source numbering is inconsistent.
    for idx, e in enumerate(entries, start=1):
        e.number = idx

    summary_html, candidates, classifier, threshold = _parse_digest_summary(digest_dir)

    accepted, matches, screened, per_source, accepted_by_source = _resolve_counts(
        digest_dir,
        fallback_screened=candidates,
        fallback_accepted=len(entries),
    )

    return Digest(
        date=date,
        slug=digest_dir.name,
        title=f"ISDS Thematic Watch, {date}",
        summary_html=summary_html,
        entries=entries,
        surfaced=len(entries),
        candidates=candidates,
        classifier=classifier,
        threshold=threshold,
        accepted=accepted,
        matches=matches,
        screened=screened,
        per_source=per_source,
        accepted_by_source=accepted_by_source,
    )


def collect_digests() -> list[Digest]:
    if not DIGESTS_SRC.is_dir():
        return []
    dirs = sorted(
        (d for d in DIGESTS_SRC.glob("*_ISDS-Thematic-Watch") if d.is_dir()),
        key=lambda d: d.name,
        reverse=True,  # newest first
    )
    digests: list[Digest] = []
    for d in dirs:
        dg = parse_digest(d)
        if dg:
            digests.append(dg)
    return digests


# --------------------------------------------------------------------------- #
# Archive charts (Upgrade C): build-time inline SVG from per-digest data.
#
# All coordinate math lives here in Python; the template only drops the finished
# SVG markup in place and carries the same numbers in a visually-hidden table for
# the accessible / no-JS path. JS (archiveChartInit) only adds a hover readout and
# an IntersectionObserver draw-in, so the charts read fully without it.
# --------------------------------------------------------------------------- #

# Palette tokens, mirrored from style.css.j2 so the SVG fills match the stylesheet.
_CHART = {
    "navy": "#0b3d5c",        # var(--navy)      — screened series
    "gold_bright": "#b8860b", # var(--gold-bright)— accepted series
    "line": "#e3ddd1",        # var(--line)      — axes / gridlines
    "muted": "#6a7280",       # var(--muted)     — annotation text
    "ink_soft": "#3a4654",    # var(--ink-soft)  — axis labels
}


def _src_label(key: str) -> str:
    """Human label for a per-source key, consistent with the rest of the site
    (the digest 'sources' line and the .source-name capitalize rule)."""
    return key.replace("_", " ").strip().capitalize()


def _fmt_num(value: float) -> str:
    """Trim trailing zeros from a coordinate for compact, stable SVG output."""
    return f"{value:.1f}".rstrip("0").rstrip(".")


@dataclass
class ChartData:
    """Numeric series + ready-to-drop inline SVG for the two archive charts.

    Every field is template-safe: ``trend_svg`` / ``source_svg`` are pre-escaped
    SVG strings, and the ``*_rows`` lists feed the visually-hidden data tables.
    ``has_source`` is False when no run carries per-source counts (older archives),
    in which case the source figure is omitted entirely rather than faked.
    """
    trend_svg: str
    trend_rows: list[dict]          # [{date, screened, accepted}]
    trend_summary: str              # worded summary for the chart's aria description
    source_svg: str
    source_rows: list[dict]         # [{label, screened, accepted}]
    source_summary: str
    has_source: bool
    source_runs: int                # how many runs contributed per-source data


def _build_trend_svg(rows: list[dict]) -> tuple[str, str]:
    """A weekly trend chart (screened area+line and accepted line) with the
    matches==0 baseline annotated. Returns ``(svg, worded_summary)``."""
    W, H = 640, 240
    pad_l, pad_r, pad_t, pad_b = 44, 16, 18, 40
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    n = len(rows)

    screened_vals = [r["screened"] or 0 for r in rows]
    accepted_vals = [r["accepted"] or 0 for r in rows]
    y_max = max(screened_vals + accepted_vals + [1])
    # Round the top gridline up to a clean number for readable ticks.
    step = 20 if y_max > 40 else (5 if y_max > 10 else 2)
    y_top = ((y_max // step) + 1) * step if y_max % step else y_max

    def x(i: int) -> float:
        return pad_l if n <= 1 else pad_l + plot_w * i / (n - 1)

    def y(v: float) -> float:
        return pad_t + plot_h * (1 - (v / y_top if y_top else 0))

    # Gridlines + y-axis tick labels.
    grid: list[str] = []
    ticks = list(range(0, y_top + 1, step))
    for tv in ticks:
        gy = _fmt_num(y(tv))
        grid.append(
            f'<line class="chart-grid" x1="{pad_l}" y1="{gy}" '
            f'x2="{W - pad_r}" y2="{gy}" />')
        grid.append(
            f'<text class="chart-axis-label" x="{pad_l - 8}" y="{gy}" '
            f'text-anchor="end" dominant-baseline="middle">{tv}</text>')

    # x-axis date labels (short MM-DD).
    xlabels: list[str] = []
    for i, r in enumerate(rows):
        short = r["date"][5:]  # MM-DD
        xlabels.append(
            f'<text class="chart-axis-label" x="{_fmt_num(x(i))}" '
            f'y="{H - pad_b + 16}" text-anchor="middle">{html.escape(short)}</text>')

    # Screened: filled area under a line.
    pts_scr = [(x(i), y(v)) for i, v in enumerate(screened_vals)]
    line_scr = " ".join(f"{_fmt_num(px)},{_fmt_num(py)}" for px, py in pts_scr)
    area_d = (f"M {_fmt_num(pts_scr[0][0])},{_fmt_num(y(0))} "
              + " ".join(f"L {_fmt_num(px)},{_fmt_num(py)}" for px, py in pts_scr)
              + f" L {_fmt_num(pts_scr[-1][0])},{_fmt_num(y(0))} Z")

    pts_acc = [(x(i), y(v)) for i, v in enumerate(accepted_vals)]
    line_acc = " ".join(f"{_fmt_num(px)},{_fmt_num(py)}" for px, py in pts_acc)

    # Matches==0 baseline, explicitly annotated (matches has been 0 throughout).
    zero_y = _fmt_num(y(0))
    zero_line = (
        f'<line class="chart-zero" x1="{pad_l}" y1="{zero_y}" '
        f'x2="{W - pad_r}" y2="{zero_y}" />'
        f'<text class="chart-zero-label" x="{W - pad_r}" y="{float(zero_y) - 6:.1f}" '
        f'text-anchor="end">matches = 0 throughout</text>')

    # Hover/focus targets: one transparent marker group per date (JS reads data-*).
    markers: list[str] = []
    for i, r in enumerate(rows):
        sx, sy = x(i), y(screened_vals[i])
        ax, ay = x(i), y(accepted_vals[i])
        markers.append(
            f'<g class="chart-marker" tabindex="0" role="listitem" '
            f'data-date="{html.escape(r["date"])}" '
            f'data-screened="{screened_vals[i]}" '
            f'data-accepted="{accepted_vals[i]}" '
            f'aria-label="{html.escape(r["date"])}: {screened_vals[i]} screened, '
            f'{accepted_vals[i]} watch-list leads shown, 0 matches">'
            f'<rect class="chart-hit" x="{_fmt_num(x(i) - plot_w / (2 * max(n - 1, 1)))}" '
            f'y="{pad_t}" width="{_fmt_num(plot_w / max(n - 1, 1))}" height="{plot_h}" />'
            f'<circle class="chart-dot chart-dot-screened" cx="{_fmt_num(sx)}" '
            f'cy="{_fmt_num(sy)}" r="3.5" />'
            f'<circle class="chart-dot chart-dot-accepted" cx="{_fmt_num(ax)}" '
            f'cy="{_fmt_num(ay)}" r="3.5" />'
            f'</g>')

    svg = (
        f'<svg class="chart chart-trend" viewBox="0 0 {W} {H}" '
        f'role="img" aria-labelledby="trend-title trend-desc" '
        f'preserveAspectRatio="xMidYMid meet">'
        f'<title id="trend-title">Weekly screened and watch-list leads trend</title>'
        f'<desc id="trend-desc">{html.escape(_trend_summary_text(rows))}</desc>'
        + "".join(grid)
        + f'<path class="chart-area chart-area-screened" d="{area_d}" />'
        + f'<polyline class="chart-line chart-line-screened" points="{line_scr}" />'
        + f'<polyline class="chart-line chart-line-accepted" points="{line_acc}" />'
        + zero_line
        + f'<g class="chart-markers" role="list">' + "".join(markers) + "</g>"
        + "".join(xlabels)
        + "</svg>"
    )
    return svg, _trend_summary_text(rows)


def _trend_summary_text(rows: list[dict]) -> str:
    if not rows:
        return "No runs archived yet."
    first, last = rows[0], rows[-1]
    accepted_total = sum(r["accepted"] or 0 for r in rows)
    return (
        f"Across {len(rows)} weekly runs from {first['date']} to {last['date']}, "
        f"items screened fell from {first['screened']} to {last['screened']} as "
        f"deduplication matured, while matches stayed at zero throughout and "
        f"watch-list leads shown were a steady trickle totalling {accepted_total}.")


def _build_source_svg(rows: list[dict]) -> tuple[str, str]:
    """A horizontal per-source bar chart: screened vs accepted per source, sorted
    by screened volume. Returns ``(svg, worded_summary)``."""
    W = 640
    pad_l, pad_r, pad_t, pad_b = 150, 40, 14, 28
    row_h, bar_h, gap = 30, 9, 3
    n = len(rows)
    H = pad_t + pad_b + n * row_h
    plot_w = W - pad_l - pad_r
    x_max = max([r["screened"] for r in rows] + [1])

    def bar_w(v: int) -> float:
        return plot_w * v / x_max if x_max else 0

    parts: list[str] = []
    # A light baseline axis at the left of the bars.
    parts.append(
        f'<line class="chart-grid" x1="{pad_l}" y1="{pad_t}" '
        f'x2="{pad_l}" y2="{H - pad_b}" />')

    for i, r in enumerate(rows):
        top = pad_t + i * row_h
        cy = top + row_h / 2
        label = _src_label(r["key"])
        # Source label (left gutter).
        parts.append(
            f'<text class="chart-axis-label chart-src-label" x="{pad_l - 10}" '
            f'y="{_fmt_num(cy)}" text-anchor="end" dominant-baseline="middle">'
            f'{html.escape(label)}</text>')
        sw = bar_w(r["screened"])
        aw = bar_w(r["accepted"])
        y_scr = top + (row_h - (2 * bar_h + gap)) / 2
        y_acc = y_scr + bar_h + gap
        group = (
            f'<g class="chart-srcrow" tabindex="0" role="listitem" '
            f'data-source="{html.escape(label)}" '
            f'data-screened="{r["screened"]}" data-accepted="{r["accepted"]}" '
            f'aria-label="{html.escape(label)}: {r["screened"]} screened, '
            f'{r["accepted"]} watch-list leads shown">'
            f'<rect class="chart-hit" x="{pad_l}" y="{_fmt_num(top + 2)}" '
            f'width="{_fmt_num(plot_w)}" height="{row_h - 4}" />'
            f'<rect class="chart-bar chart-bar-screened" x="{pad_l}" '
            f'y="{_fmt_num(y_scr)}" width="{_fmt_num(sw)}" height="{bar_h}" rx="1.5" />'
            f'<rect class="chart-bar chart-bar-accepted" x="{pad_l}" '
            f'y="{_fmt_num(y_acc)}" width="{_fmt_num(max(aw, 1) if r["accepted"] else 0)}" '
            f'height="{bar_h}" rx="1.5" />'
            f'<text class="chart-bar-value" x="{_fmt_num(pad_l + max(sw, aw) + 6)}" '
            f'y="{_fmt_num(cy)}" dominant-baseline="middle">'
            f'{r["screened"]}/{r["accepted"]}</text>'
            f'</g>')
        parts.append(group)

    svg = (
        f'<svg class="chart chart-source" viewBox="0 0 {W} {H}" '
        f'role="img" aria-labelledby="source-title source-desc" '
        f'preserveAspectRatio="xMidYMid meet">'
        f'<title id="source-title">Per-source screened and watch-list leads totals</title>'
        f'<desc id="source-desc">{html.escape(_source_summary_text(rows))}</desc>'
        + "".join(parts)
        + "</svg>"
    )
    return svg, _source_summary_text(rows)


def _source_summary_text(rows: list[dict]) -> str:
    if not rows:
        return "No per-source data is available yet."
    active = [r for r in rows if r["screened"] > 0]
    if not active:
        return "No source surfaced fresh candidates in the runs with per-source data."
    top = active[0]
    accepted_total = sum(r["accepted"] for r in rows)
    feeders = ", ".join(f"{_src_label(r['key'])} ({r['screened']})" for r in active)
    return (
        f"Of the catalogue sources, {feeders} contributed fresh candidates; "
        f"{_src_label(top['key'])} dominated the screened volume, and "
        f"{accepted_total} item(s) were shown as watch-list leads across all sources.")


def build_archive_charts(digests: list[Digest]) -> ChartData:
    """Aggregate the per-digest series and emit both inline SVGs (build-time)."""
    # Trend rows in chronological order (digests arrive newest-first).
    ordered = sorted(digests, key=lambda d: d.date)
    trend_rows = [
        {"date": d.date,
         "screened": d.screened if d.screened is not None else 0,
         "accepted": d.accepted if d.accepted is not None else 0,
         "matches": d.matches if d.matches is not None else 0}
        for d in ordered
    ]
    trend_svg, trend_summary = (_build_trend_svg(trend_rows) if trend_rows
                                else ("", _trend_summary_text(trend_rows)))

    # Per-source aggregation across every run that carries per-source data.
    screened_by: dict[str, int] = {}
    accepted_by: dict[str, int] = {}
    source_runs = 0
    for d in digests:
        if not d.per_source:
            continue  # older runs predate per-source counting — guarded.
        source_runs += 1
        for k, v in d.per_source.items():
            screened_by[k] = screened_by.get(k, 0) + v
        for k, v in d.accepted_by_source.items():
            accepted_by[k] = accepted_by.get(k, 0) + v

    keys = sorted(
        set(screened_by) | set(accepted_by),
        key=lambda k: (-screened_by.get(k, 0), -accepted_by.get(k, 0), k),
    )
    source_rows = [
        {"key": k, "label": _src_label(k),
         "screened": screened_by.get(k, 0), "accepted": accepted_by.get(k, 0)}
        for k in keys
    ]
    has_source = bool(source_rows)
    # The chart shows only sources that surfaced fresh candidates (the ones that
    # "earn their place"); the visually-hidden table below keeps every source,
    # including the dead/quiet ones at zero, as the authoritative record.
    chart_rows = [r for r in source_rows if r["screened"] > 0] or source_rows
    if has_source:
        source_svg, source_summary = _build_source_svg(chart_rows)
    else:
        source_svg, source_summary = "", _source_summary_text(source_rows)

    return ChartData(
        trend_svg=trend_svg,
        trend_rows=trend_rows,
        trend_summary=trend_summary,
        source_svg=source_svg,
        source_rows=source_rows,
        source_summary=source_summary,
        has_source=has_source,
        source_runs=source_runs,
    )


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def _build_stamp() -> dict:
    """When the site was generated, and the commit it was built from — so a stale
    GitHub Pages deploy is obvious at a glance (compare to the repo's HEAD)."""
    import datetime
    import subprocess
    commit = ""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True,
            stderr=subprocess.DEVNULL).strip()
    except Exception:  # noqa: BLE001 - missing git must not break the build
        commit = ""
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return {"at": at, "commit": commit}


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["repo_url"] = REPO_URL
    env.globals["build_stamp"] = _build_stamp()

    def band_class(band: str) -> str:
        b = (band or "").upper()
        if b == "HIGH":
            return "high"
        if b == "MEDIUM":
            return "med"
        if b == "WATCH":
            return "watch"
        return "low"

    env.filters["band_class"] = band_class
    return env


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  + {path.relative_to(REPO_ROOT)}")


def build() -> int:
    print("Building ISDS Thematic Watcher site -> docs/")
    env = make_env()

    digests = collect_digests()
    print(f"  parsed {len(digests)} digest(s)")

    memo = parse_methodology(METHODOLOGY_MD)

    DOCS.mkdir(parents=True, exist_ok=True)

    # 1. Landing page (root => active nav 'home', depth 0).
    index_tpl = env.get_template("index.html.j2")
    write(
        DOCS / "index.html",
        index_tpl.render(
            active="home",
            root="",
            digests=digests,
            ring_labels=RING_LABELS,
        ),
    )

    # 2. Methodology page.
    if memo:
        meth_tpl = env.get_template("methodology.html.j2")
        write(
            DOCS / "methodology.html",
            meth_tpl.render(
                active="methodology",
                root="",
                memo=memo,
            ),
        )

    # 3. Digest archive index (under docs/digests/, depth 1 -> root "../").
    charts = build_archive_charts(digests)
    archive_tpl = env.get_template("digest_index.html.j2")
    write(
        DOCS / "digests" / "index.html",
        archive_tpl.render(
            active="digests",
            root="../",
            digests=digests,
            charts=charts,
        ),
    )

    # 4. One page per digest.
    digest_tpl = env.get_template("digest.html.j2")
    for dg in digests:
        write(
            DOCS / "digests" / f"{dg.date}.html",
            digest_tpl.render(
                active="digests",
                root="../",
                digest=dg,
            ),
        )

    # 5. Backtest page (root => same depth as home; deterministic, no I/O on
    #    docs/). run_backtest() assembles a focused labelled set from in-repo
    #    text and scores it with the same deterministic scorer the pipeline uses.
    backtest_tpl = env.get_template("backtest.html.j2")
    write(
        DOCS / "backtest.html",
        backtest_tpl.render(
            active="backtest",
            root="",
            bt=run_backtest(),
        ),
    )

    # 6. Stylesheet.
    css_tpl = env.get_template("style.css.j2")
    write(DOCS / "assets" / "style.css", css_tpl.render())

    # 7. .nojekyll marker.
    write(DOCS / ".nojekyll", "")

    print("Done.")
    return 0


def main() -> int:
    try:
        return build()
    except Exception as exc:  # pragma: no cover - surfaced to the operator
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
