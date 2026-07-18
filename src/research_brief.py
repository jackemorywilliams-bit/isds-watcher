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
import sys
from pathlib import Path
from typing import Optional

from . import config, integrity_gate
from .integrity_gate import verify  # the append-only ledger (scripts/verify.py)


def _gate_note(gated: dict) -> str:
    """Render the deterministic gate outcome as the vetting note the editor honors:
    what may be asserted, what stays a lead, what routes for library access."""
    lines = ["INTEGRITY GATE (deterministic, ledger-backed): " + gated["header"], ""]
    if gated["asserted"]:
        lines.append("May be ASSERTED (operator-verified):")
        lines += [f"- {c['claim_text']}" for c in gated["asserted"]]
    if gated["leads"]:
        lines.append("UNVERIFIED LEADS only — present with explicit unverified framing, "
                     "never as established holdings/facts:")
        lines += [f"- {c['claim_text']}" for c in gated["leads"]]
    if gated["library"]:
        lines.append("FOR PROFESSOR / LIBRARY ACCESS only (paywalled or blocked):")
        lines += [f"- {c['claim_text']}" for c in gated["library"]]
    if gated["rejected"]:
        lines.append("OPERATOR-REJECTED — must not appear in the brief at all:")
        lines += [f"- {c['claim_text']}" for c in gated["rejected"]]
    return "\n".join(lines)

logger = logging.getLogger("isds.research_brief")

_PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
# scripts/ holds the deterministic, model-free citation verifier; import it lazily-ish
# by adding scripts/ to the path (it is not a package).
_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

# Interpretive work warrants the most capable model; override with RESEARCH_MODEL.
DEFAULT_MODEL = "claude-opus-4-8"
# Anthropic server-side web search (latest tool version; runs its own loop).
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 6}
# Cap the server-tool continuation loop (pause_turn) so a run can't spin forever.
MAX_CONTINUATIONS = 6
# Bound the per-item source text handed to the analyst, to control token spend.
MAX_ITEM_EXCERPT = 1500
# How many recent daily research notes to feed the weekly analyst, and the total
# character budget for them (so the weekly brief builds on the daily work rather
# than redoing it — and searches less, lowering the weekly API cost).
DAILY_NOTES_DIR = Path("analytics") / "daily-research"
MAX_DAILY_NOTES = 7
MAX_DAILY_NOTES_CHARS = 9000

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

# The chairman's weekly reconvene minutes: status, next steps, per-member
# accountability, and items to escalate to the principal.
RECONVENE_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "next_steps": {"type": "array", "items": {"type": "string"}},
        "accountability": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"member": {"type": "string"}, "assessment": {"type": "string"}},
                "required": ["member", "assessment"],
                "additionalProperties": False,
            },
        },
        "escalations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["status", "next_steps", "accountability", "escalations"],
    "additionalProperties": False,
}


def _model() -> str:
    return os.environ.get("RESEARCH_MODEL", DEFAULT_MODEL)


def _read_prompt(name: str) -> str:
    return (_PROMPTS / name).read_text(encoding="utf-8")


def _calibration() -> str:
    """The binding anti-hallucination / behavioral calibration checklist shared by
    the council (council_calibration.md)."""
    try:
        return _read_prompt("council_calibration.md")
    except OSError:
        return "(calibration checklist unavailable)"


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


def _daily_notes_block() -> str:
    """The most recent daily-researcher notes (committed by the Max routine), so the
    weekly analyst builds on the week's daily work instead of redoing it."""
    if not DAILY_NOTES_DIR.is_dir():
        return "(No daily research notes this week.)"
    files = sorted(
        (p for p in DAILY_NOTES_DIR.glob("*.md")), reverse=True)[:MAX_DAILY_NOTES]
    if not files:
        return "(No daily research notes this week.)"
    chunks, total = [], 0
    for p in files:  # newest first
        try:
            text = p.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        block = f"### {p.stem}\n{text}"
        if total + len(block) > MAX_DAILY_NOTES_CHARS:
            block = block[: max(0, MAX_DAILY_NOTES_CHARS - total)] + "\n…(truncated)"
        chunks.append(block)
        total += len(block)
        if total >= MAX_DAILY_NOTES_CHARS:
            break
    return "\n\n".join(chunks) if chunks else "(No daily research notes this week.)"


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
        .replace("{{CALIBRATION}}", _calibration())
        .replace("{{AGENDA}}", agenda or "(No agenda set — use your judgement.)")
        .replace("{{WEEK}}", week_str)
        .replace("{{SCREENED}}", str(screened))
        .replace("{{PRIOR_THREADS}}", _threads_block(prior_threads))
        .replace("{{ITEMS}}", _items_block(items))
        .replace("{{DAILY_NOTES}}", _daily_notes_block())
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


# The LLM security-officer stage was replaced by the deterministic integrity gate
# (src/integrity_gate.py) — assertion decisions now come from exact claim_id lookup
# against the operator verification ledger, not from a model verdict.


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


def _run_reconvene(client, agenda, memo, security, brief) -> dict:
    """Chairman reconvenes: reviews the week against the agenda and produces the
    minutes — status, next steps, per-member accountability, and escalations to the
    principal."""
    issue = (f"Headline: {brief.get('headline','')}\nDek: {brief.get('dek','')}\n"
             f"Open threads: " + "; ".join(brief.get("open_threads", [])))
    prompt = (
        _read_prompt("council_reconvene.txt")
        .replace("{{AGENDA}}", agenda or "(none)")
        .replace("{{MEMO}}", memo or "(none)")
        .replace("{{SECURITY}}", security or "(none)")
        .replace("{{ISSUE}}", issue)
    )
    resp = client.messages.create(
        model=_model(),
        max_tokens=1500,
        system=("You are the chairman of an ISDS research council writing the weekly "
                "accountability minutes. Return only valid JSON for the schema."),
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": RECONVENE_SCHEMA}},
    )
    return json.loads(_text_of(resp))


def _brief_citation_text(brief: dict, memo: str) -> str:
    """Assemble the prose whose citations the INTEGRITY-CHECK stage scans: the editor's
    supplemental link URLs/titles/notes, the structured section bodies, and the raw analyst
    memo. The section bodies and notes carry the bibliographic authorities (law-review
    articles, treatises, awards by case number) that a bare-URL scan would miss."""
    bits: list[str] = []
    for s in brief.get("supplemental", []) or []:
        s = s or {}
        bits.append(f"{s.get('title','')} {s.get('url','')} {s.get('note','')}")
    for sec in brief.get("sections", []) or []:
        sec = sec or {}
        bits.append(sec.get("body", "") or "")
    bits.append(memo or "")
    return "\n".join(b for b in bits if b)


def _verify_citations(brief: dict, memo: str) -> None:
    """INTEGRITY-CHECK stage. After the security officer, run the model-free hallucination
    checker (scripts/check_citations.py) over the brief's OWN citations — resolving every
    cited URL AND recording URL-less bibliographic authorities (law-review articles,
    treatises, awards by case number) as "needs human verification". This extends the
    earlier URL-only verification to cover the kind of citations the methodology memo and
    the brief carry, not just bare digest URLs.

    Attaches, for the brief/ledger to surface:
      * ``brief["citation_check"]``   — per-URL results (unchanged shape; render/ledger read it)
      * ``brief["citation_summary"]`` — one-line tally across URLs + bibliographic citations
      * ``brief["citation_verdict"]`` — structured {clean, flagged_urls, needs_human, counts}
      * ``brief["_integrity_clean"]`` — boolean verdict (clean unless a URL looks fabricated)

    Model-free and fully guarded: a missing dependency or any failure degrades to an empty
    verdict and NEVER breaks the brief. ``check_citations`` falls back to the URL-only
    verifier internally, so this remains the deterministic, no-model integrity gate."""
    if not getattr(config, "BRIEF_INTEGRITY_CHECK", True) \
            and not getattr(config, "CITATION_VERIFY", True):
        brief["citation_check"] = []
        brief["citation_summary"] = "Citation integrity check disabled."
        brief["citation_verdict"] = {"clean": True, "flagged_urls": [],
                                     "needs_human": [], "counts": {}}
        brief["_integrity_clean"] = True
        return
    try:
        import check_citations  # from scripts/ (added to sys.path above)
        report = check_citations.check_text(_brief_citation_text(brief, memo))
        # Keep the per-URL list render.py/council_log already consume (same shape).
        brief["citation_check"] = report.get("url_results", [])
        brief["citation_summary"] = report.get("summary", "")
        flagged = [r for r in report.get("url_results", [])
                   if r.get("verdict") == check_citations.FABRICATION]
        needs_human = [b.get("citation", "") for b in report.get("bibliographic", [])]
        clean = not report.get("fabrication_suspected", False)
        brief["citation_verdict"] = {
            "clean": clean,
            "flagged_urls": [r.get("url", "") for r in flagged],
            "needs_human": needs_human,
            "counts": report.get("counts", {}),
        }
        brief["_integrity_clean"] = clean
        if flagged:
            logger.warning("research_brief: integrity check FLAGGED %d cited URL(s) "
                            "as possibly fabricated — %s",
                            len(flagged), brief["citation_summary"])
        else:
            logger.info("research_brief: integrity check clean — %s (%d need human review)",
                        brief["citation_summary"], len(needs_human))
    except Exception as exc:  # noqa: BLE001 - integrity check must never break the brief
        logger.warning("research_brief: citation integrity check failed (%s)", exc)
        brief["citation_check"] = []
        brief["citation_summary"] = "Citation integrity check unavailable."
        brief["citation_verdict"] = {"clean": True, "flagged_urls": [],
                                     "needs_human": [], "counts": {}}
        brief["_integrity_clean"] = True


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
        # INTEGRITY GATE (deterministic; replaces the LLM security officer for
        # assertion decisions). The analyst proposes candidate claims; the operator
        # verification ledger — exact claim_id lookup only — decides what may be
        # asserted. Malformed analyst output FAILS this stage with a structured
        # error artifact; it is never converted into a successful empty brief.
        try:
            candidates = integrity_gate.parse_candidate_claims(memo)
        except integrity_gate.MalformedAnalystOutput as exc:
            logger.error("research_brief: analyst output violated the candidate-claims "
                         "contract (%s); error artifact: %s", exc, exc.artifact_path)
            return None
        for c in candidates:  # ledger the proposals (claim_created only; never a status)
            try:
                verify.create_claim(
                    c["claim_text"], c["source_url"],
                    supporting_locator=c.get("supporting_locator"),
                    access_status=c["access_status"],
                    source_authority=c["source_authority"])
            except Exception as exc:  # noqa: BLE001 - ledgering must not kill the brief
                logger.warning("research_brief: could not ledger claim (%s)", exc)
        gated = integrity_gate.classify(candidates)
        integrity_gate.gate_brief(gated["asserted"])  # invariant: asserted ⇒ verified
        security_note = _gate_note(gated)
        logger.info("research_brief: integrity gate — %s", gated["header"])
        brief = _run_editor(client, memo, security_note)
        brief["_memo"] = memo
        brief["_agenda"] = agenda
        # The deterministic gate note stands where the LLM vetting note used to.
        brief["_security"] = security_note
        brief["_security_clean"] = not gated["rejected"]
        brief["_security_issues"] = [
            f"operator-rejected claim resurfaced: {c['claim_text'][:120]}"
            for c in gated["rejected"]]
        # INTEGRITY-CHECK stage (after the security officer): the deterministic, model-free
        # hallucination check over the brief's own citations — URLs resolved, URL-less
        # bibliographic authorities recorded for human verification. The integrity control
        # no model gives.
        _verify_citations(brief, memo)
        # Chairman reconvenes to take stock and hold the council accountable.
        try:
            brief["minutes"] = _run_reconvene(client, agenda, memo, security_note, brief)
            logger.info("research_brief: chairman filed weekly minutes (%d escalations)",
                        len(brief["minutes"].get("escalations", [])))
        except Exception as exc:  # noqa: BLE001 - minutes are best-effort
            logger.warning("research_brief: reconvene failed (%s)", exc)
            brief["minutes"] = None
        logger.info("research_brief: built '%s' (%d sections, %d supplemental, %d threads)",
                    brief.get("headline", "?"), len(brief.get("sections", [])),
                    len(brief.get("supplemental", [])), len(brief.get("open_threads", [])))
        return brief
    except Exception as exc:  # noqa: BLE001 - brief failure must not crash the run
        logger.error("research_brief: failed (%s)", exc)
        return None
