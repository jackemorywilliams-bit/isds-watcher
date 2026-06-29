---
tags: [multi-agent, plan]
---
# 50 — Staged plan

- **Stage 0 (done, keep):** integrity layer — citation verification, `STATE_OF_THE_ANSWER.md`, the
  dedup insight ledger, the eval gate. The real quality wins; non-agentic.
- **Stage 1 (do first — ~1 line, real value):** **cross-model verifier** — security/integrity
  officer runs on a *different* model from the analyst (analyst Opus 4.8; verifier Haiku 4.5 or
  Sonnet 4.6). The single-threaded generator–verifier pattern the literature endorses
  ([[40 - Evidence on ROI]]). Implement as a `SECURITY_MODEL` env var defaulting to the analyst
  model (no behavior change until flipped).
- **Stage 2 (the genuine multi-agent step, if wanted):** **Agent-SDK subagents on Max in cron**
  ([[30 - The Max plus Agent SDK path]]) — chairman → researcher subagent + isolated-context
  verifier subagent; repo as state. Real independence, free on Max, serverless.
- **Stage 3 (optional — validate first):** weekly **debate** (analyst vs. devil's advocate). Test
  manually; ship only if the brief measurably improves. Use Batch API (−50%) + caching if so.
- **Stop here.** LangGraph Platform / Managed Agents are justified only if scope becomes always-on
  monitoring or a live human+agent dashboard.

Open items to settle before each stage: [[60 - Open questions]]. Choices logged in [[70 - Decisions]].
#multi-agent #plan
