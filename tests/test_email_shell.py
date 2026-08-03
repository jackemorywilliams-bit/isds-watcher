"""The non-digest emails must read as well as the digest does.

The Monday packet and the daily record used to ship bare unstyled tags, which is
why the packet read as cryptic beside the digest. These tests pin the structure
the shell must produce — and, more importantly, that it never alters the author's
content while restyling it.
"""

from __future__ import annotations

from src import email_shell


def test_headings_become_sections():
    out = email_shell.md_to_html("## What needs you this week")
    assert "<h2>What needs you this week</h2>" in out


def test_tables_render_as_tables():
    md = "| Claim | Source |\n|---|---|\n| Rule 51 reaches admissibility | ICSID |"
    out = email_shell.md_to_html(md)
    assert "<table>" in out and "<th>Claim</th>" in out
    assert "<td>Rule 51 reaches admissibility</td>" in out


def test_ordered_and_unordered_lists_are_distinguished():
    assert "<ul>" in email_shell.md_to_html("- one\n- two")
    assert "<ol>" in email_shell.md_to_html("1. one\n2. two")


def test_blockquote_and_rule_and_code():
    assert "<blockquote>" in email_shell.md_to_html("> Coverage is a floor.")
    assert "<hr>" in email_shell.md_to_html("---")
    assert "<code>x</code>" in email_shell.md_to_html("`x`")


def test_action_lines_get_a_callout():
    """A line the operator must act on must not look like a line that informs."""
    out = email_shell.md_to_html("NEEDS VERIFICATION: the notice of arbitration.")
    assert 'class="act"' in out
    assert "NEEDS VERIFICATION" in out
    assert "the notice of arbitration." in out


def test_ordinary_prose_is_not_a_callout():
    out = email_shell.md_to_html("The council met four times this week.")
    assert 'class="act"' not in out


def test_links_and_bare_urls_are_clickable():
    out = email_shell.md_to_html("See [the docket](https://icsid.worldbank.org/x).")
    assert '<a href="https://icsid.worldbank.org/x">the docket</a>' in out

    bare = email_shell.md_to_html("Source: https://uncitral.un.org/en/commission")
    assert '<a href="https://uncitral.un.org/en/commission">' in bare


def test_html_in_content_is_escaped_not_executed():
    out = email_shell.md_to_html("A claim about <script>alert(1)</script> tags.")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_content_words_survive_restyling():
    """Presentation may change; the author's words may not."""
    md = ("## Ring 3\n\nThe six-month cooling-off period is an admissibility gate.\n\n"
          "- Wingtech filed a notice of arbitration\n")
    out = email_shell.md_to_html(md)
    for phrase in ("Ring 3", "six-month cooling-off period",
                   "admissibility gate", "Wingtech filed a notice of arbitration"):
        assert phrase in out


def test_render_produces_a_full_document_with_masthead():
    doc = email_shell.render("Body text.", title="Monday Review Packet",
                             kicker="ISDS Thematic Watcher", issue="2026-08-03",
                             lede="What needs your eyes.", footer="Footer note.")
    assert doc.startswith("<!doctype html>")
    assert "Monday Review Packet" in doc
    assert "ISDS Thematic Watcher" in doc
    assert "2026-08-03" in doc
    assert "What needs your eyes." in doc
    assert "Footer note." in doc
    assert "class='sheet'" in doc


def test_render_is_safe_with_empty_optional_fields():
    doc = email_shell.render("Body.", title="T")
    assert "<h1>T</h1>" in doc
    assert "class='kicker'" not in doc
