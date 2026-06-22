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
                    fallback_accepted: int) -> tuple[int | None, int | None, int | None]:
    """Resolve ``(accepted, matches, screened)`` for a digest, defined identically
    to the email and meta.json: ``screened`` = candidates scored; ``matches`` =
    items at/above threshold; ``accepted`` = matches plus watch-list leads shown.

    Order of preference:
    1. ``meta.json`` (schema {"date","screened","matches","watch_list_leads","accepted"}).
    2. The folder's ``index.html`` footer (current "Screened:" / "Matches (>=N):",
       or legacy "Candidates screened:" / "At or above threshold (N):").
    3. README-derived fallbacks (candidate count for screened, surfaced-entry count
       for accepted; matches defaults to 0 when otherwise unknown).

    Robust by design: a missing or malformed source is skipped, never fatal.
    """
    accepted: int | None = None
    matches: int | None = None
    screened: int | None = None

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

    return accepted, matches, screened


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

    accepted, matches, screened = _resolve_counts(
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
    archive_tpl = env.get_template("digest_index.html.j2")
    write(
        DOCS / "digests" / "index.html",
        archive_tpl.render(
            active="digests",
            root="../",
            digests=digests,
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

    # 5. Stylesheet.
    css_tpl = env.get_template("style.css.j2")
    write(DOCS / "assets" / "style.css", css_tpl.render())

    # 6. .nojekyll marker.
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
