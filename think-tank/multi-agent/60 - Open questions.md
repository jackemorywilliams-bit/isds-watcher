---
tags: [multi-agent, open-questions]
---
# 60 — Open questions (think-tank these)

1. **Is the verifier alone enough?** After [[50 - Staged plan|Stage 1]], run a holdout test: does a
   cross-model verifier catch errors the same-model one missed? If not, Stage 2's value is doubtful.
2. **What is the Max headless weekly budget?** Stage 2 lives or dies on the separate post-2026-06-15
   pool ([[30 - The Max plus Agent SDK path]]). Measure a single Agent-SDK daily run's cost against it.
3. **Where does the "breakthrough" actually come from** — better *reasoning* (agents) or better
   *inputs* (a real full-text intake source)? The evidence ([[40 - Evidence on ROI]]) leans inputs.
   Should source acquisition outrank multi-agent on the roadmap?
4. **Does an isolated-context verifier reduce hallucination more than the programmatic citation
   check already does?** If the deterministic URL-fetch check already gates the worst failures, the
   marginal gain from a verifier *agent* may be small.
5. **Failure modes:** if we add subagents, which MAST failure patterns (mis-coordination,
   error-compounding) would we watch for, and how would the eval gate catch them?

Move resolved questions to [[70 - Decisions]].
#multi-agent #open-questions

<!-- graph:auto start -->
Map: [[Council]]
<!-- graph:auto end -->
