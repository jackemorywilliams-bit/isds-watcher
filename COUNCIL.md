# The ISDS Research Council

The "council" is how this project organizes the work of turning raw ISDS developments
into interpreted research. It is **not** a set of standing background agents — it is a
set of clearly-defined **roles**, realized as coordinated stages in the weekly run
(`python -m src.main`). Each role is **trained to its task** — by a dedicated instruction
prompt (with few-shot exemplars and the binding calibration checklist below) or implemented
as a deterministic pipeline component — and the chairman coordinates them. This keeps the work
auditable and reproducible (every role's output is archived) while giving the project the
multi-perspective rigor of a council.

## Members

| Role | Realized as | Responsibility |
|------|-------------|----------------|
| **Data-scraping agents** ("scouts") | `src/sources/*` + `src/enrich.py` | Fetch and enrich candidate developments from the open sources (italaw, UNCTAD, ICSID, IISD ITN, IAReporter, Google Alerts, …). |
| **Classifier** | `src/classify.py` + `fingerprint.yaml` | Score each candidate against the three-ring thematic fingerprint; produce the digest. |
| **Chairman** | `prompts/council_chairman.txt` | Opens each weekly session. Reads the carried open threads + this week's items and **sets the agenda** — priority focus, what to verify, which threads are live. Steward of continuity. |
| **Research analyst** | `prompts/research_analyst.txt` (+ Claude web search) | Interprets the week's items against the research question and **escalates to web search** for supplemental contemporary findings (always, on a quiet week), working to the chairman's agenda. |
| **Security / integrity officer** | `prompts/council_security.txt` | Vets the analyst's memo before publication: flags fabricated/unverifiable sources, overreach, **inflated relevance**, and quote/access-integrity problems. Its vetting note is binding on the editor. |
| **Citation / hallucination checker** | `scripts/check_citations.py` | Deterministic backstop to the security officer: machine-verifies every citation and high-risk claim in the brief — and, on demand, this methodology memo — against a real source, recording a structured clean/flagged verdict before publication. |
| **Autoprompt engineer (through the chairman)** | `src/research_state.py` + the open-threads loop | Each issue's open threads are persisted and fed back into next week's chairman agenda, so the prompting adapts and the research compounds rather than restarting cold. |
| **Editor** | `prompts/research_editor.txt` | Turns the vetted memo into the structured, professional **ISDS Research Brief** (the second weekly email), honoring the security officer's note. |
| **Systems researcher** | `prompts/systems_researcher.txt` | Second daily researcher, working in parallel with the research analyst but studying the **instrument itself**: mines open GitHub scraper/monitor projects, IR and text-classification literature, and LLM/automation tooling for concrete, sourced, component-specific ways to make this pipeline more efficient and effective. Daily note committed to `analytics/systems-research/<DATE>.md`; the week's notes feed the Monday roundtable's workflow-improvement question. |
| **Analytics officer** | `scripts/source_analytics.py` + per-source counts in `meta.json` | Tracks which catalogue sources are receptive to the thematic intersection (surfaced yield now; receptivity = surfaced ÷ fresh candidates as per-source counts accrue), to tune coverage toward feeds that yield genuinely on-theme articles. Output: `analytics/source-receptivity.md`. |

**Calibration (binding).** Every member applies the council calibration checklist
(`prompts/council_calibration.md`) — a pre-publication, anti-hallucination behavioral
calibration adapted from the documented "self-awareness" pre-response framework to this
project: uncertainty handling, citation/quote/number verification, goal alignment,
relevance honesty (anti-inflation), no sycophancy/filler, brevity, and constraint
compliance. The **security officer** enforces it in full before anything is published.

**Bounded web search.** The analyst's web search is *not* a collection channel. It is
used only to deepen insight on the already-screened developments and to synthesize
research around the research question; every web finding must connect back to a screened
item or the question.

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

## Cadence & accountability

- **Daily — the full council meets.** Every day the whole council convenes (chairman
  presiding; research analyst; security/integrity officer; editor; analytics officer): the
  chairman sets the agenda, the analyst researches and the security officer vets, the
  analytics officer relates the findings to that week's screened digest items, and the
  council discusses how to advance the research question — raising at most one genuinely
  new system/method improvement (deduped into `analytics/optimization-log.md`) toward a
  breakthrough. This runs as a **scheduled Claude Code routine on the operator's Claude Max
  plan** (not the API-billed GitHub Actions pipeline), with a deliberately small daily
  budget so it does not eat into Max usage. The meeting record is committed to `analytics/daily-research/`
  and emailed each day by a free GitHub Actions job (`daily-update.yml`, SMTP only).
  The **systems researcher** runs in the same daily routine, in parallel, committing its
  sourced improvement note to `analytics/systems-research/<DATE>.md`.
  **Daily writing standard (binding).** The daily record is written for the operator as a
  standalone, plain-language professional note: a reader with no prior context must be able
  to follow it. Complete sentences and a short through-line — never fragmented mini-paragraphs
  that presume the previous days' context; jargon spelled out on first use; a one-line
  "where this leaves the research question" close. Honesty over volume: a quiet day is one
  clean paragraph, not padding.
- **Monday — the roundtable, before the operator's email.** Each Monday, before the
  13:00 UTC review email fires, the routine convenes the **full-council roundtable**
  (`prompts/council_roundtable.txt`): a genuine multi-role dialogue over three questions —
  the researcher's findings (challenged by the security officer, tied to screened items by
  the analytics officer), workflow improvements (presented by the systems researcher from
  the week's notes), and the status of the research question. The transcript plus the
  chairman's close-out is committed to `analytics/roundtable/<DATE>.md`, and the Monday
  review packet (`scripts/send_human_review.py`) places its overview at the top of the
  operator's email. The digest for the faculty mentor remains a separate email; the two are
  never merged.
- **Weekly — the council reconvenes.** The weekly run convenes the full council and ends
  with the chairman's **reconvene minutes**: a candid status, next steps, a per-member
  **accountability** assessment, and **escalations to the principal** (surfaced in the
  brief's "Chairman's note"). This runs in GitHub Actions against the API key. The weekly
  analyst **builds on the week's daily notes** (`analytics/daily-research/`) rather than
  redoing the research, so the daily Max work feeds the weekly brief and the weekly run
  searches less (lower API cost).
- **Accountability ledger.** Every session is recorded in `state/council_log.json` and
  rendered to `analytics/council-log.md` — the chairman's written record for holding
  members accountable, so quality is tracked over time rather than living in one model's
  recollection.

## Compounding memory, dedup, and human review

Three controls keep the research cumulative, non-repetitive, and verifiable — so days build on
each other instead of starting cold, and "new" is measured rather than assumed.

- **State-of-the-answer synthesis (`STATE_OF_THE_ANSWER.md`).** A living, structured document —
  the project's cumulative best answer-so-far, organized by the three rings + the trade-secret /
  clinical-data sub-question, each claim tied to its source(s), with an open-questions section.
  The analyst reads it first each session and updates it after, so the research visibly
  compounds. Unverifiable claims are marked `[unverified]` rather than asserted.
- **Insight ledger (`analytics/insights.jsonl`).** An append-only, deduplicated record of each
  genuinely new insight, one JSON object per line ({date, thread_id, ring, insight, sources,
  confidence} — schema documented in `STATE_OF_THE_ANSWER.md`, since JSONL has no comment
  syntax). It is the baseline against which "new" is judged: a session checks a candidate
  insight against the ledger and, if already recorded, does not re-log it. On a quiet day the
  honest output is "no new insight; standing watch" — this enforces the anti-inflation rule so
  the one-insight-per-day mandate never degrades into padding on the quiet weeks the methodology
  expects to be the norm.
- **Human-review checkpoint (`HUMAN_REVIEW.md`).** A logged, recurring human spot-audit
  (monthly, and on escalation) of a sample of cited claims from the period's records — pass/fail
  recorded, verification debt cleared. This turns the methodology's "leads to be verified before
  relied upon" stance into an auditable checkpoint rather than an assumption.

## On the MCP overlay this was modeled on
The structure was adapted from a Claude "council/overlay" layout. We deliberately did
**not** install the third-party MCP plugin that inspired it (it wires auto-running
session hooks, usage telemetry to an external service, and an embedded token). The
council instead lives entirely in-repo. If a *trusted* MCP toolset is ever wanted, it can
be attached to the analyst via the Messages API `mcp_servers` parameter without changing
the council's structure.

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
