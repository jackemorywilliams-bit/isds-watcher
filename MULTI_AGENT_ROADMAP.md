# Roadmap — making the council genuinely multi-agent (grounded, evidence-based)

The deferred "big task": moving from the current **personas-in-a-pipeline** design to genuine
multi-agent, with the least grunt work and least cost. This version is grounded in the real
multi-agent ecosystem (the GitHub `multi-agent-systems` topic, LangGraph, AutoGen/AG2, CrewAI,
OpenAI Agents SDK, Anthropic's own engineering) and the published evidence on when multi-agent
helps — researched by a three-member council (ecosystem scout, fit architect, ROI skeptic) on
2026-06-23. Sources are listed at the end. It supersedes the earlier, Anthropic-centric draft.

## The honest bottom line first
For *this* project — a solo, narrow-domain, scheduled **research-and-verify** tool over an
already-pre-filtered candidate set — the published evidence says full multi-agent mostly does
**not** improve the output, and can hurt it (cost, latency, error-compounding). Multi-agent's
wins are for **parallel breadth** (many independent directions at once); your task is
**sequential depth**. The biggest quality wins were the **non-agentic** fixes already shipped
(citation verification, compounding memory, eval gate). So the recommendation is: take the one
cheap multi-agent pattern the literature actually endorses, optionally take the genuine
multi-agent step now that it's cost-free on Max, and stop there unless a measured experiment
says otherwise.

## The correction that reframes the whole question
The earlier roadmap assumed "stay on the Max subscription" and "run genuinely multi-agent in a
GitHub Actions cron" were mutually exclusive. **They are not.** The **Claude Agent SDK
authenticates against a Pro/Max subscription** via `claude setup-token` → the
`CLAUDE_CODE_OAUTH_TOKEN`, and that token **works in GitHub Actions** ([docs](https://code.claude.com/docs/en/github-actions)).
So a cron-triggered Actions job can run the Agent SDK with **real subagents — each with its own
isolated context window and tools — billed to the Max headless pool, not per-token API.**
Caveat (new, 2026-06-15): headless Agent-SDK/Actions usage is metered **separately** from
interactive Claude Code, so the daily budget is finite — keep it lean.

## Why the popular frameworks are a poor fit here
None of the major frameworks *require* a standing server for core agent logic, but each fails at
least one hard constraint (cron + repo-as-state, daily heavy work on Max, solo/cost-sensitive):

| Option | Fits cron + repo, no server? | Daily heavy work on Max (no API $)? | Effort | Verdict |
|---|---|---|---|---|
| **Claude Agent SDK subagents** (cron Actions job, `CLAUDE_CODE_OAUTH_TOKEN`) | Yes — headless run, repo is the state | **Yes** — bills the Max headless pool | Low–Med | **The real multi-agent path that fits.** |
| **Cross-model verifier** (security/verifier on a different model) | Yes (weekly, API) | N/A (weekly API, modest) | ~1 line | **Cheapest endorsed win — do first.** |
| **LangGraph** (library) | Partial — its cron/durability/queues are the *Platform server* you'd avoid | No — per-token API | High | Impressive, poor fit; you'd pay API tokens to get hand-off you already have |
| **AutoGen/AG2** (group-chat/debate) | Partial — debate state is in-memory, lost each cron run | No — per-token API | Med–High | Defer; episodic cron + in-memory state mismatch |
| **CrewAI** (role/task crews) | Yes-ish | No — per-token API | Med | Skip — re-implements the existing pipeline, on API billing, no new capability |
| **OpenAI Agents SDK** | Yes (script) | No — OpenAI-native; Claude only via beta adapter | High | Skip — wrong ecosystem for a Claude/Max project |
| **Claude Managed Agents** | No — Anthropic-side sessions/containers, API + session-hour billing | No | High | Right answer only if this becomes always-on monitoring |

Note on legacy: AutoGen (original) is in maintenance mode — prefer AG2 or Microsoft Agent
Framework if you ever go that route. MetaGPT's releases are stale. The GitHub topic's top
entries are mostly Claude-Code harnesses and file-based-planning repos — i.e. they validate the
repo-as-state + Claude-subagents pattern rather than pointing elsewhere.

## Staged plan
- **Stage 0 (done, keep):** the integrity layer — citation verification, `STATE_OF_THE_ANSWER.md`,
  the dedup insight ledger, the eval gate. These were the real quality wins and are non-agentic.
- **Stage 1 (do first — ~1 line, real value): cross-model verifier.** Run the security/verifier
  on a *different* model from the analyst (analyst Opus 4.8; verifier Haiku 4.5 or Sonnet 4.6).
  This is the single-threaded **generator–verifier** pattern the literature endorses — two
  different reasoners, different blind spots — at near-zero marginal cost. Implement as a
  `SECURITY_MODEL` env var (defaulting to the analyst model, so nothing changes until you flip it).
- **Stage 2 (the genuine multi-agent step, if you want it): Agent-SDK subagents for the DAILY
  meeting, on Max, in cron.** Replace the single role-playing routine with an Agent-SDK run where
  a chairman delegates to a **researcher subagent** (own context + web tools) and a **verifier
  subagent with a fresh, isolated context** that never saw the researcher's reasoning and
  independently checks the day's insight against `insights.jsonl` and the cited sources. State and
  hand-off stay in the repo (read `STATE_OF_THE_ANSWER.md` + recent notes; write the dated note +
  one deduped insight); subagent hand-off is in-process. Runs on Max via `CLAUDE_CODE_OAUTH_TOKEN`
  in a daily Actions cron — no server, no per-token API. Effort: Medium.
- **Stage 3 (optional — validate before automating): weekly debate.** Only if Stages 1–2 leave a
  measured gap. Test a 2–3 turn analyst vs. devil's-advocate exchange *manually* and check the
  brief actually improves before shipping it (use the Batch API −50% + prompt caching if you do).
- **Stop here.** Orchestration frameworks (LangGraph Platform) and Claude Managed Agents are
  justified only if scope changes to always-on monitoring or a live human+agent dashboard — at
  which point you're operating a server anyway and these constraints no longer bind. For a
  cost-sensitive solo researcher, that day may never come, and that's fine.

## What the evidence says about ROI (so the decision is informed, not faith)
- Multi-agent helps **breadth-first, parallelizable, high-value** tasks and works largely by
  spending **~15× the tokens** of a chat (Anthropic) — and is explicitly **a poor fit when agents
  share context or have many dependencies**, which describes this pipeline.
- "Readonly" research/verify subagents "mostly resemble tool calls rather than true multi-agent
  collaboration"; the patterns that work keep **writes single-threaded** with extra agents adding
  *intelligence, not actions* (Cognition). Parallel-writer swarms fail.
- Empirically, multi-agent gains on benchmarks are "often minimal," with a documented failure
  taxonomy (Berkeley MAST), and strong single-agent baselines match multi-agent at far lower cost,
  the apparent gains explained by extra compute rather than architecture.
- Therefore the highest-ROI next move is **not** more agents — it's hardening the **eval gate** so
  it can detect quality regressions, plus the **cross-model verifier** (Stage 1), which is a
  one-config-line experiment you can prove or kill on the holdout set.

## Sources
Anthropic — Building effective agents (https://www.anthropic.com/engineering/building-effective-agents) ·
Anthropic — How we built our multi-agent research system (https://www.anthropic.com/engineering/multi-agent-research-system) ·
Claude Code GitHub Actions / OAuth token (https://code.claude.com/docs/en/github-actions) ·
LangGraph (https://github.com/langchain-ai/langgraph), Platform (https://www.langchain.com/langgraph-platform) ·
AutoGen (https://github.com/microsoft/autogen), AG2 (https://github.com/ag2ai/ag2) ·
CrewAI (https://github.com/crewAIInc/crewAI) ·
OpenAI Agents SDK (https://github.com/openai/openai-agents-python) ·
GitHub multi-agent-systems topic (https://github.com/topics/multi-agent-systems) ·
Cognition — Don't Build Multi-Agents (https://cognition.com/blog/dont-build-multi-agents) and Multi-Agents: What's Actually Working (https://cognition.com/blog/multi-agents-working) ·
MAST — Why Do Multi-Agent LLM Systems Fail? (https://arxiv.org/abs/2503.13657) ·
Strong single-agent baseline (https://arxiv.org/pdf/2601.12307).
Pricing (claude-api skill, cached 2026-06-04): Opus 4.8 $5/$25, Sonnet 4.6 $3/$15, Haiku 4.5 $1/$5 per MTok; Batch −50%; cache reads ~0.1×.

<!-- graph:auto start -->
Map: [[00 - Project Map]]
<!-- graph:auto end -->
