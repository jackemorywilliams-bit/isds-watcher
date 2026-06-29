---
tags: [multi-agent, frameworks]
---
# 20 — Options: frameworks, scored against our constraints

Surveyed from the GitHub `multi-agent-systems` topic + the leading frameworks. None *require* a
standing server for core agent logic, but each fails at least one hard filter ([[00 - The question]]).

| Option | Cron + repo, no server? | Daily heavy work on Max (no API $)? | Verdict |
|---|---|---|---|
| [[30 - The Max plus Agent SDK path\|Claude Agent SDK subagents]] | Yes | **Yes** | The real fit |
| Cross-model verifier | Yes (weekly, API) | n/a | Cheapest endorsed win — do first |
| LangGraph (library) | Partial (durability = the Platform server) | No — per-token API | Impressive, poor fit |
| AutoGen / AG2 (group-chat/debate) | Partial (debate state in-memory) | No — API | Defer |
| CrewAI (role crews) | Yes-ish | No — API | Skip (re-implements what we have) |
| OpenAI Agents SDK | Yes | No — OpenAI-native | Skip (wrong ecosystem) |
| Claude Managed Agents | No (Anthropic-side sessions) | No | Only if always-on monitoring |

Notes: legacy **AutoGen** is in maintenance → AG2 / Microsoft Agent Framework. **MetaGPT** is
stale. The topic's top repos are mostly Claude-Code harnesses + file-based planning — which
*validate* the repo-as-state + Claude-subagents pattern rather than pointing elsewhere.

Sources are listed in `MULTI_AGENT_ROADMAP.md`. Next: [[30 - The Max plus Agent SDK path]]
#multi-agent #frameworks
