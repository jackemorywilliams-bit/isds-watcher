---
tags: [multi-agent, key-finding]
---
# 30 — The Max + Agent SDK path (the finding that reframes everything)

The earlier roadmap assumed **"stay on Max"** and **"genuine multi-agent in cron"** were mutually
exclusive. They are **not**.

- The **Claude Agent SDK authenticates against a Pro/Max subscription** via `claude setup-token` →
  `CLAUDE_CODE_OAUTH_TOKEN`, and that token **works in GitHub Actions**.
- So a cron-triggered Actions job can run the Agent SDK with **real subagents — each with its own
  isolated context window and tools — billed to the Max headless pool, not per-token API.**

**What this enables (Stage 2 in [[50 - Staged plan]]):** the daily meeting becomes a chairman that
delegates to a **researcher subagent** (own context + web tools) and a **verifier subagent with a
fresh, isolated context** that never saw the researcher's reasoning and independently checks the
day's insight against the cited sources + `insights.jsonl`. State and hand-off stay in the repo;
subagent hand-off is in-process. No server, no per-token API.

**Caveat (2026-06-15):** headless Agent-SDK / Actions usage is metered **separately** from
interactive Claude Code — a finite weekly pool. Keep the daily run lean.

Tension to resolve: is this worth doing over the cheap verifier? See [[40 - Evidence on ROI]].
#multi-agent #key-finding

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
