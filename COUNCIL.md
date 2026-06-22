# The ISDS Research Council

The "council" is how this project organizes the work of turning raw ISDS developments
into interpreted research. It is **not** a set of standing background agents — it is a
set of clearly-defined **roles**, realized as coordinated stages in the weekly run
(`python -m src.main`). Each role is a prompt or a pipeline component; the chairman
coordinates them. This keeps the work auditable and reproducible (every role's output is
archived) while giving the project the multi-perspective rigor of a council.

## Members

| Role | Realized as | Responsibility |
|------|-------------|----------------|
| **Data-scraping agents** ("scouts") | `src/sources/*` + `src/enrich.py` | Fetch and enrich candidate developments from the open sources (italaw, UNCTAD, ICSID, IISD ITN, IAReporter, Google Alerts, …). |
| **Classifier** | `src/classify.py` + `fingerprint.yaml` | Score each candidate against the three-ring thematic fingerprint; produce the digest. |
| **Chairman** | `prompts/council_chairman.txt` | Opens each weekly session. Reads the carried open threads + this week's items and **sets the agenda** — priority focus, what to verify, which threads are live. Steward of continuity. |
| **Research analyst** | `prompts/research_analyst.txt` (+ Claude web search) | Interprets the week's items against the research question and **escalates to web search** for supplemental contemporary findings (always, on a quiet week), working to the chairman's agenda. |
| **Security / integrity officer** | `prompts/council_security.txt` | Vets the analyst's memo before publication: flags fabricated/unverifiable sources, overreach, **inflated relevance**, and quote/access-integrity problems. Its vetting note is binding on the editor. |
| **Autoprompt engineer (through the chairman)** | `src/research_state.py` + the open-threads loop | Each issue's open threads are persisted and fed back into next week's chairman agenda, so the prompting adapts and the research compounds rather than restarting cold. |
| **Editor** | `prompts/research_editor.txt` | Turns the vetted memo into the structured, professional **ISDS Research Brief** (the second weekly email), honoring the security officer's note. |

## The weekly flow

```
scouts → classifier → DIGEST email (Thematic Watch, unchanged)
                         │
                         └─► chairman (agenda)
                               → analyst (interpret + web search)
                                 → security officer (vet)
                                   → editor → RESEARCH BRIEF email (interpretive)
                                       └─ open threads ─┐
                                                        └─► carried to next week's chairman
```

- The **digest** (annotated bibliography) is unchanged and primary.
- The **brief** is a separate, interpretive Monday email (`briefs/<date>.html`), with the
  full council deliberation preserved at `briefs/<date>-memo.md` (agenda + analyst memo +
  vetting note) as the audit trail.
- The brief requires the Anthropic provider (web search is an Anthropic server tool) and
  is skipped otherwise; set `RESEARCH_BRIEF_ENABLED=0` to suppress it. Model via
  `RESEARCH_MODEL` (default `claude-opus-4-8`).

## On the MCP overlay this was modeled on
The structure was adapted from a Claude "council/overlay" layout. We deliberately did
**not** install the third-party MCP plugin that inspired it (it wires auto-running
session hooks, usage telemetry to an external service, and an embedded token). The
council instead lives entirely in-repo. If a *trusted* MCP toolset is ever wanted, it can
be attached to the analyst via the Messages API `mcp_servers` parameter without changing
the council's structure.
