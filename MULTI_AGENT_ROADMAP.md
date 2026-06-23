# Roadmap — making the council genuinely multi-agent (cheapest, lowest-effort path)

This is the deferred "big task": moving from the current **personas-in-a-pipeline** design
to a genuinely multi-agent council, with the least grunt work and least cost from where the
project is today. Produced by the research council (a `claude-code-guide` agent) on
2026-06-23. Cost figures below are **indicative**, drawn partly from secondary sources —
verify against current Anthropic pricing before committing spend.

## Where we are now (honest baseline)
- **Weekly:** a Python process (GitHub Actions) makes sequential Anthropic API calls —
  chairman → analyst (web_search) → security → editor → reconvene — all the **same model,
  one rubric**. Real process separation (separate calls on frozen artifacts), but not
  independent agents.
- **Daily:** one Claude Code routine on the **Max plan** role-plays chairman + researcher
  in a single session. One model talking to itself.
- The programmatic fixes already shipped (citation verification, structured memory, eval
  gate, reliability) close the biggest *integrity and reliability* gaps **without** going
  multi-agent. Multi-agent mainly buys **independent parallel analysis** and **adversarial
  cross-checking** — not, by itself, better facts.

## Options (cost / effort / what it actually adds)

| Option | Cost | Effort | Multi-agent value |
|---|---|---|---|
| **1. Separate Claude Code routines on Max** (researcher, security, editor as distinct staggered routines handing off via repo files) | **$0 — Max subscription** | Low (~2h) | Real async independence + separate session state; each role re-runnable on its own |
| **2. Cross-model verifier** (security officer on a different/cheaper model, e.g. Sonnet/Haiku, vs analyst on Opus) | ~$ negligible–$20/mo | Low (1 line) | Two models, different blind spots — the cheapest real integrity gain |
| **3. Weekly debate via an Agent Team** (spawn teammates in one session for live adversarial discussion) | Max (if it fits limits); ~4–7× tokens | Med (8–12h); experimental | Real-time disagreement/iteration — only worth it if debate measurably improves briefs |
| **4. Claude Managed Agents** (server-managed coordinator + subagent threads, native message passing) | API per-token + session-hour fee (~hundreds/mo) | High (40h+ SDK refactor) | True orchestration; overkill for episodic weekly/daily work |
| **5. MCP server as shared memory/tools** | $0 self-host – ~$50/mo | Med | Cleaner hand-offs; only worth it when integrating external systems (Slack/Linear) |

## Recommended staged path
- **Stage 1 (do first):** split the daily meeting into **separate Max routines** (researcher → security → editor), handing off via committed files — staggered (e.g. 08:00 / 09:00 / 10:00 UTC). **$0, ~2h, genuine async multi-agent.** This is the single highest-leverage, lowest-cost step and keeps the daily work on Max.
- **Stage 2:** make the **security/verifier a different model** than the analyst (weekly, and the daily security routine). Cheap, real cross-checking.
- **Stage 3 (optional, validate first):** a weekly **Agent-Team debate** — but run one or two manual debate sessions and confirm the brief is actually better before automating. If it isn't, stop here.
- **Stage 4 (only if scaling to always-on / a live dashboard):** Managed Agents. For a solo research project this is almost certainly overkill.

## Honest verdict
Stages 1 + 2 deliver real multi-agent value for roughly **$0–20/mo and ~3 hours** of work,
and keep the heavy daily work on the Max subscription. Beyond Stage 2 you are paying for
research-quality gains (debate, orchestration) whose benefit must be demonstrated, not
assumed — the cost/benefit stops being worth it for a single-researcher project unless the
scope grows to always-on monitoring or human+agent collaboration. The biggest near-term
wins were the **non-agentic** fixes already shipped (real citation verification, compounding
memory, reliability); multi-agent is the next increment, not a prerequisite.
