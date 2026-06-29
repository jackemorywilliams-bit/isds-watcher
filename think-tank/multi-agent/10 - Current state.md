---
tags: [multi-agent, current-state]
---
# 10 — Current state

The "council" today is **personas in a pipeline**, not independent agents:
- **Weekly:** a Python process makes sequential Anthropic API calls — chairman → analyst (web
  search) → security → editor → reconvene — all the **same model, one rubric**. Real process
  separation, but one mind.
- **Daily:** one Claude Code routine on the **Max plan** role-plays the **full council** in a
  single session, reading/writing the repo (`STATE_OF_THE_ANSWER.md`, `insights.jsonl`,
  `optimization-log.md`, the latest digest) and emailing the record.

What is already genuinely strong (and **not** multi-agent): programmatic citation verification,
compounding memory + dedup ledger, the eval gate, reliability/heartbeat. These were the real
quality wins. See `MULTI_AGENT_ROADMAP.md`.

So the question in [[00 - The question]] is the **next increment**, not a prerequisite.
Options: [[20 - Options - frameworks]] · [[30 - The Max plus Agent SDK path]]
#multi-agent
