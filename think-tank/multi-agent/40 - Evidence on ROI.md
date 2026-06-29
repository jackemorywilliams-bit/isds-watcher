---
tags: [multi-agent, evidence, roi]
---
# 40 — Evidence on ROI (when multi-agent helps, and when it does not)

The honest, cited finding: for **this** task — solo, narrow-domain, scheduled
**research-and-verify** over an already-narrowed candidate set — full multi-agent mostly does
**not** improve output, and can hurt it.

- Multi-agent earns its keep on **parallel breadth** (many independent directions at once). Ours is
  **sequential depth**. Anthropic: multi-agent uses **~15× the tokens** of chat and is **a poor fit
  when agents share context or have many dependencies** — which describes this pipeline.
- Cognition: read-only research/verify subagents "mostly resemble tool calls rather than true
  multi-agent collaboration"; what works keeps **writes single-threaded**, adding *intelligence not
  actions*. Parallel-writer swarms fail.
- Berkeley **MAST**: multi-agent gains are "often minimal" with a documented failure taxonomy.
- Strong single-agent baselines match multi-agent at far lower cost; apparent gains are mostly
  **extra compute**, not architecture.

**Implication:** the highest-ROI next move is *not* more agents — it is the cheap, single-threaded
**generator–verifier** (a different model checking the work), plus a sharper eval gate. The genuine
multi-agent step ([[30 - The Max plus Agent SDK path]]) is now cost-free on Max, but the evidence
says it likely won't move the output much beyond the verifier.

Decide with eyes open: [[70 - Decisions]]. Sources in `MULTI_AGENT_ROADMAP.md`.
#multi-agent #evidence
