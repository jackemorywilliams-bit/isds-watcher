"""The weekly interpretive **ISDS Research Brief** — a small research-team prompt
pipeline run inside the weekly job, one stage handing off to the next:

    analyst  (Claude + web search)   →   editor  (Claude, structured JSON)

The analyst reads this week's classified items and the open threads carried from
prior weeks, interprets them against the project's research question, and escalates
to web search for supplemental contemporary findings — always on a quiet week. The
editor turns that memo into a structured, professional newsletter and emits the
open threads for next week (the "autoprompt" continuity loop in research_state).

This is the project's "team," morphed for an autonomous pipeline: instead of an
interactive MCP/skills plugin, the team is a deterministic chain of role prompts
(prompts/research_analyst.txt, prompts/research_editor.txt) driven through the
Anthropic API with the server-side web-search tool. It is also MCP-extensible —
a trusted MCP server can be attached later via the Messages API ``mcp_servers``
parameter without changing this structure.

Requires the Anthropic provider + key (web search is an Anthropic server tool). On
any error or when unavailable, ``generate_brief`` returns ``None`` and the caller
simply skips the brief — it never raises.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger("isds.research_brief")

_PROMPTS = Path(__file__).resolve().parent.parent / "prompts"

# Interpretive work warrants the most capable model; override with RESEARCH_MODEL.
DEFAULT_MODEL = "claude-opus-4-8"
# Anthropic server-side web search (latest tool version; runs its own loop).
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 6}
# Cap the server-tool continuation loop (pause_turn) so a run can't spin forever.
MAX_CONTINUATIONS = 6
# Bound the per-item source text handed to the analyst, to control token spend.
MAX_ITEM_EXCERPT = 1500

EDITOR_SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string"},
        "dek": {"type": "string"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"heading": {"type": "string"}, "body": {"type": "string"}},
                "required": ["heading", "body"],
                "additionalProperties": False,
            },
        },
        "supplemental": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["title", "url", "note"],
                "additionalProperties": False,
            },
        },
        "open_threads": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["headline", "dek", "sections", "supplemental", "open_threads"],
    "additionalProperties": False,
}


def _model() -> str:
    return os.environ.get("RESEARCH_MODEL", DEFAULT_MODEL)


def _read_prompt(name: str) -> str:
    return (_PROMPTS / name).read_text(encoding="utf-8")


def _items_block(items) -> str:
    if not items:
        return ("(No items cleared the relevance floor this week — a quiet week. "
                "Advance the research with a contemporary, research-question-relevant "
                "development you locate via web search.)")
    out = []
    for i, it in enumerate(items, 1):
        meta = it.metadata or {}
        if meta.get("notable_quote"):
            quote = meta["notable_quote"]
        elif meta.get("notable_unavailable"):
            quote = "N/A — source paywalled (headline only)"
        else:
            quote = "—"
        rings = ", ".join(it.matched_rings) if it.matched_rings else "none"
        excerpt = (getattr(it, "raw_text", "") or it.summary or "")[:MAX_ITEM_EXCERPT]
        out.append(
            f"{i}. {it.title}\n"
            f"   source: {it.source} | relevance: {it.relevance_score} | rings: {rings}\n"
            f"   url: {it.url}\n"
            f"   annotation: {it.digest_summary}\n"
            f"   notable line: {quote}\n"
            f"   excerpt: {excerpt}\n"
        )
    return "\n".join(out)


def _threads_block(threads) -> str:
    if not threads:
        return ("(No prior threads — this is the first brief. Establish the initial "
                "research threads worth tracking.)")
    return "\n".join(f"- {t}" for t in threads)


def _client():
    import anthropic  # lazy import
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def _text_of(resp) -> str:
    return "".join(
        b.text for b in resp.content if getattr(b, "type", None) == "text"
    ).strip()


def _run_chairman(client, items, prior_threads, week_str, screened) -> str:
    """Chairman: opens the session and sets the week's agenda from carried threads
    and this week's items. Steward of continuity (the autoprompt loop runs through
    the chair)."""
    prompt = (
        _read_prompt("council_chairman.txt")
        .replace("{{PRIOR_THREADS}}", _threads_block(prior_threads))
        .replace("{{ITEMS}}", _items_block(items))
    )
    resp = client.messages.create(
        model=_model(),
        max_tokens=1200,
        system="You are the chairman of an investor-State dispute settlement research council.",
        messages=[{"role": "user", "content": prompt}],
    )
    return _text_of(resp)


def _run_analyst(client, items, prior_threads, week_str, screened, agenda) -> str:
    """Research analyst: interprets the week's items against the research question and
    escalates to web search for supplemental contemporary findings, working to the
    chairman's agenda."""
    prompt = (
        _read_prompt("research_analyst.txt")
        .replace("{{AGENDA}}", agenda or "(No agenda set — use your judgement.)")
        .replace("{{WEEK}}", week_str)
        .replace("{{SCREENED}}", str(screened))
        .replace("{{PRIOR_THREADS}}", _threads_block(prior_threads))
        .replace("{{ITEMS}}", _items_block(items))
    )
    messages = [{"role": "user", "content": prompt}]
    resp = None
    for _ in range(MAX_CONTINUATIONS):
        resp = client.messages.create(
            model=_model(),
            max_tokens=8000,
            system="You are a meticulous investor-State dispute settlement research analyst.",
            tools=[WEB_SEARCH_TOOL],
            messages=messages,
        )
        # The web-search server loop pauses with pause_turn when it hits its
        # internal iteration cap; re-send to let it resume.
        if resp.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": resp.content})
            continue
        break
    return _text_of(resp) if resp else ""


def _run_security(client, analyst_memo: str) -> str:
    """Security officer: vets the memo for fabrication, overreach, inflated relevance,
    and quote/access integrity before publication."""
    prompt = _read_prompt("council_security.txt").replace("{{ANALYST_MEMO}}", analyst_memo)
    resp = client.messages.create(
        model=_model(),
        max_tokens=1500,
        system="You are the security and integrity officer of an ISDS research council.",
        messages=[{"role": "user", "content": prompt}],
    )
    return _text_of(resp)


def _run_editor(client, analyst_memo: str, security_note: str) -> dict:
    """Editor: turns the vetted memo into the structured, professional brief, honoring
    the security officer's vetting note."""
    prompt = (
        _read_prompt("research_editor.txt")
        .replace("{{SECURITY_NOTE}}", security_note or "(No issues flagged.)")
        .replace("{{ANALYST_MEMO}}", analyst_memo)
    )
    resp = client.messages.create(
        model=_model(),
        max_tokens=4000,
        system=("You are the editor of a professional ISDS research newsletter. "
                "Return only valid JSON matching the provided schema."),
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": EDITOR_SCHEMA}},
    )
    return json.loads(_text_of(resp))


def generate_brief(items, *, prior_threads, week_str, screened,
                   provider) -> Optional[dict]:
    """Convene the council: chairman → analyst (web search) → security → editor.

    Returns the structured brief dict (with ``_memo``/``_agenda``/``_security`` keys
    holding each stage's raw output for the archive), or ``None`` if the research
    provider is unavailable or any step fails. Never raises."""
    norm = (provider or "").strip().lower()
    if norm not in ("claude", "anthropic") or not os.environ.get("ANTHROPIC_API_KEY"):
        logger.info("research_brief: skipped (needs Anthropic provider + ANTHROPIC_API_KEY)")
        return None
    try:
        client = _client()
        agenda = _run_chairman(client, items, prior_threads, week_str, screened)
        logger.info("research_brief: chairman set the agenda (%d chars)", len(agenda))
        memo = _run_analyst(client, items, prior_threads, week_str, screened, agenda)
        if not memo:
            logger.warning("research_brief: analyst produced no text; skipping")
            return None
        security = _run_security(client, memo)
        logger.info("research_brief: security officer vetted the memo (%d chars)", len(security))
        brief = _run_editor(client, memo, security)
        brief["_memo"] = memo
        brief["_agenda"] = agenda
        brief["_security"] = security
        logger.info("research_brief: built '%s' (%d sections, %d supplemental, %d threads)",
                    brief.get("headline", "?"), len(brief.get("sections", [])),
                    len(brief.get("supplemental", [])), len(brief.get("open_threads", [])))
        return brief
    except Exception as exc:  # noqa: BLE001 - brief failure must not crash the run
        logger.error("research_brief: failed (%s)", exc)
        return None
