"""Shared visual shell for the project's non-digest emails.

The weekly digest renders through ``templates/digest.html.j2`` and reads like a
publication. The Monday review packet and the daily council record did not: they
shipped bare ``<h1>``/``<p>``/``<ul>`` with no styling at all, which is why the
packet reads as cryptic next to the digest even when its content is good.

This module gives those emails the digest's own design language — same serif
body, same navy and gold, same 680px sheet on a grey field — plus a Markdown
renderer that actually carries structure: section rules, tables, blockquotes,
horizontal rules, and a callout for the lines that need the reader to act.

Content stays exactly as its author wrote it. This changes presentation only.
"""

from __future__ import annotations

import html
import re

# Design tokens lifted from templates/digest.html.j2 so the family reads as one.
INK = "#1b252e"
NAVY = "#0b3d5c"
GOLD = "#9a7b2e"
MUTED = "#5a6672"
FIELD = "#eceef1"
RULE = "#d6dbe1"
HAIRLINE = "#e6e9ed"

_STYLE = f"""
  body {{ margin:0; padding:0; background:{FIELD};
         font-family: Georgia, 'Times New Roman', serif; color:{INK}; line-height:1.6; }}
  .sheet {{ max-width:680px; margin:0 auto; background:#ffffff; }}
  .mast {{ padding:22px 36px 16px; border-bottom:3px double {NAVY}; }}
  .mast .kicker {{ font-family:Arial,Helvetica,sans-serif; font-size:11px; letter-spacing:.22em;
         text-transform:uppercase; color:{GOLD}; margin:0 0 4px; }}
  .mast h1 {{ margin:0; font-size:24px; letter-spacing:.3px; color:{NAVY}; }}
  .mast .issue {{ font-family:Arial,Helvetica,sans-serif; font-size:12px; color:{MUTED};
         margin-top:6px; }}
  .lede {{ padding:18px 36px 2px; font-size:14.5px; color:#33414f; }}
  .lede strong {{ color:{NAVY}; }}
  .body {{ padding:4px 36px 26px; font-size:15px; }}

  /* Headings become section rules, so the eye can find a part at a glance. */
  .body h1, .body h2 {{ font-family:Arial,Helvetica,sans-serif; font-size:11.5px;
         font-weight:700; text-transform:uppercase; letter-spacing:.12em; color:{NAVY};
         margin:26px 0 0; padding-bottom:6px; border-bottom:1px solid {RULE}; }}
  .body h3 {{ font-size:16px; color:{NAVY}; margin:20px 0 2px; }}
  .body h4 {{ font-family:Arial,Helvetica,sans-serif; font-size:12.5px; color:{MUTED};
         margin:16px 0 2px; text-transform:none; letter-spacing:0; }}
  .body p {{ margin:10px 0; }}
  .body ul, .body ol {{ margin:10px 0 10px 0; padding-left:22px; }}
  .body li {{ margin:5px 0; }}
  .body a {{ color:{NAVY}; }}
  .body strong {{ color:{NAVY}; }}
  .body hr {{ border:0; border-top:1px solid {HAIRLINE}; margin:22px 0; }}
  .body code {{ font-family:'SF Mono',Menlo,Consolas,monospace; font-size:13px;
         background:#f4f6f8; padding:1px 4px; border-radius:3px; }}
  .body blockquote {{ margin:12px 0; padding:8px 16px; border-left:3px solid {GOLD};
         background:#faf8f3; color:#3a4651; font-style:italic; }}
  .body table {{ border-collapse:collapse; width:100%; margin:14px 0; font-size:13.5px; }}
  .body th {{ font-family:Arial,Helvetica,sans-serif; font-size:11px; text-transform:uppercase;
         letter-spacing:.08em; color:{NAVY}; text-align:left; padding:7px 8px;
         border-bottom:2px solid {RULE}; }}
  .body td {{ padding:7px 8px; border-bottom:1px solid {HAIRLINE}; vertical-align:top; }}

  /* A line that needs the reader to DO something reads differently from one that
     only informs — the packet's whole purpose is the former. */
  .act {{ margin:14px 0; padding:12px 16px; background:#f6f9fb; border-left:3px solid {NAVY}; }}
  .act .tag {{ font-family:Arial,Helvetica,sans-serif; font-size:10.5px; font-weight:700;
         letter-spacing:.14em; text-transform:uppercase; color:{GOLD}; display:block;
         margin-bottom:3px; }}

  .foot {{ padding:16px 36px 26px; border-top:1px solid {RULE};
         font-family:Arial,Helvetica,sans-serif; font-size:11.5px; color:{MUTED}; }}
  .foot p {{ margin:4px 0; }}
"""

# Lines the reader must act on, marked so they cannot be skimmed past. This is the
# single definition of "a line that needs Emory" — callers that want to COUNT such
# lines must use action_line_count() rather than write their own pattern, or a line
# can be counted in a subject while rendering as ordinary prose in the body.
_ACTION_RE = re.compile(
    r"^\s*(NEEDS? (?:YOU\b|(?:YOUR )?(?:VERIFICATION|DECISION|SIGN-?OFF))|ACTION|"
    r"AWAITING (?:YOU|EMORY)|FOR (?:YOU|EMORY)|OPERATOR ACTION|TO VERIFY)"
    r"\b[:\-—]?\s*(.*)$",
    re.I,
)


def action_line_count(md: str) -> int:
    """How many lines in ``md`` will render as operator-action callouts."""
    return sum(1 for line in md.splitlines() if _ACTION_RE.match(line.strip()))


def _inline(text: str) -> str:
    """Escape, then restore the inline Markdown we support."""
    out = html.escape(text)
    out = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    # Bare URLs become links so nothing is left for the reader to copy by hand.
    out = re.sub(r"(?<!\"|>)(?<![\w@:])(https?://[^\s<)\]]+)", r'<a href="\1">\1</a>', out)
    return out


def _split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def md_to_html(md: str) -> str:
    """Markdown -> HTML for email bodies: headings, lists, tables, quotes, rules."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    list_tag: str | None = None

    def close_list() -> None:
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        # Table: a header row followed by a separator row of dashes.
        if (stripped.startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|[\s\-:|]+\|\s*$", lines[i + 1])):
            close_list()
            head = _split_row(stripped)
            out.append("<table><tr>"
                       + "".join(f"<th>{_inline(c)}</th>" for c in head)
                       + "</tr>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = _split_row(lines[i].strip())
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</table>")
            continue

        if re.match(r"^\s*(---+|\*\*\*+|___+)\s*$", raw):
            close_list()
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            lvl = min(len(m.group(1)), 4)
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_list()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{_inline(' '.join(quote))}</blockquote>")
            continue

        m = re.match(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$", raw)
        if m:
            want = "ol" if re.match(r"^\s*\d+[.)]\s", raw) else "ul"
            if list_tag != want:
                close_list()
                out.append(f"<{want}>")
                list_tag = want
            out.append(f"<li>{_inline(m.group(1))}</li>")
            i += 1
            continue

        close_list()
        act = _ACTION_RE.match(stripped)
        if act:
            label = act.group(1).upper()
            rest = act.group(2).strip()
            out.append(f'<div class="act"><span class="tag">{html.escape(label)}</span>'
                       f'{_inline(rest)}</div>')
        else:
            out.append(f"<p>{_inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


def render(body_md: str, *, title: str, kicker: str = "",
           issue: str = "", lede: str = "", footer: str = "") -> str:
    """Wrap Markdown in the project's email shell and return a full document."""
    parts = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        f"<title>{html.escape(title)}</title>",
        f"<style>{_STYLE}</style></head><body>",
        "<div class='sheet'>",
        "<div class='mast'>",
    ]
    if kicker:
        parts.append(f"<p class='kicker'>{html.escape(kicker)}</p>")
    parts.append(f"<h1>{html.escape(title)}</h1>")
    if issue:
        parts.append(f"<div class='issue'>{html.escape(issue)}</div>")
    parts.append("</div>")
    if lede:
        parts.append(f"<div class='lede'>{_inline(lede)}</div>")
    parts.append(f"<div class='body'>{md_to_html(body_md)}</div>")
    if footer:
        parts.append(f"<div class='foot'>{md_to_html(footer)}</div>")
    parts.append("</div></body></html>")
    return "\n".join(parts)
