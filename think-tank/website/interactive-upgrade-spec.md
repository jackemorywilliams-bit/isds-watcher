---
tags: [website, ui, spec, council]
---
# Interactive upgrade spec — making the instrument explorable

Council research deliverable (the research analyst's read-only spec, reviewed by the chairman).
The site is competently built but **entirely static** — the Venn is a dead image, the scoring
grammar is flat text, and the Digest Archive is a list with no analytics despite the project
being *about* trends. This spec is the agreed plan to make it interactive, grounded in real
technique rather than intuition. Companion to the build PRs.

## Governing principles (binding)
1. **Build-time SVG first, JS second.** Every visual is emitted as static inline SVG by
   `scripts/build_site.py` from data already in `meta.json`; JS only *adds* hover/focus/filter.
   With JS off, every chart and diagram still renders and reads — matching the project's
   "defensive, degrades gracefully" ethos.
2. **No dependencies.** No charting library, no framework. Extend the single existing inline
   `<script>` IIFE in `base.html.j2`; do not introduce a build step.
3. **Motion is a guest.** All motion gated behind `@media (prefers-reduced-motion: no-preference)`
   *and* a `matchMedia` early-return in JS. Reduced-motion users get the final state instantly.
4. **Palette discipline.** Reuse existing tokens only (`--navy`, `--gold`, `--cream`, `--ink`,
   the three ring tints slate/gold/sage). No emoji, no new gradients.
5. **[[site-source-sync]]:** these are template/CSS/Python edits — `docs/` must be rebuilt and
   committed in the same change or the live site goes stale.

## Upgrade A — the Venn as an explorable doctrine model (highest priority)
Make each ring hoverable **and** keyboard-focusable (roving tabindex, `role`, `aria-label`). On
hover/focus: the ring lifts (fill-opacity 0.30 → ~0.46, stroke thickens) while the others recede,
and a persistent `aria-live` **reading panel** beside the figure shows that ring's meaning (the
prose from the three `.ring-card`s — uniting the Venn and the cards into one instrument). Focusing
the centre explains the theme; focusing a two-ring lens explains "any two rings already reach
HIGH ≥70" — *visually proving* the scoring grammar. Subtle pointer 3D tilt, reduced-motion-off.
No-JS: the SVG reads exactly as today; the panel ships pre-populated with the THEME definition.
- Files: `index.html.j2` (venn figure + readout), `style.css.j2` (`/* venn */` states + panel),
  `base.html.j2` (`vennInit()`, ~40 lines).

## Upgrade B — live scoring explorer
Three toggles (IP / Judicial-measure *weighted* / Jurisdiction) beside `.scoring-note`; toggling
recomputes the **band** (HIGH/MEDIUM/LOW + range + one-line reason) and highlights the matching
rings in the Venn. Grammar mirrors `_band_from_score`: two rings → HIGH; the weighted
judicial-measure ring alone → MEDIUM; one non-weighted ring or none → LOW. Framed as "how the band
rule works," **not** a claim about findings (no item has scored a true ≥40 match — see
[[score-ceiling-and-dedup-reality]]). Native `<input type=checkbox>` + `<output aria-live>`.
No-JS: the static legend / a small truth-table remains.
- Files: `index.html.j2`, `style.css.j2`, `base.html.j2` (`scoreExplorerInit()`, ~20 lines).

## Upgrade C — Digest Archive: trend + source-receptivity charts (highest data value)
`build_site.py` already parses `screened`/`matches`/`accepted`/`per_source` from each `meta.json`.
Emit two inline SVGs at build time: (1) a weekly **trend** line/area (screened fell 80 → ~12 as
dedup matured; matches 0 throughout — annotate the zero line; accepted a steady trickle); (2) a
horizontal **per-source hit-rate** bar (screened vs accepted per source → which feeds earn their
place; newest data: `iareporter_headlines` and `italaw` dominate). JS adds a hover readout +
IntersectionObserver draw-in. A visually-hidden `<table>` is the authoritative accessible/no-JS
data path.
- Files: `build_site.py` (add `per_source` to `Digest`, aggregate), `digest_index.html.j2`,
  `style.css.j2` (`/* archive charts */` + a `.visually-hidden` utility), `base.html.j2`
  (`archiveChartInit()`). **Requires the per_source emission — do after A/B prove the pattern.**

## Upgrade D — tasteful motion & depth (sitewide polish, lowest priority)
- **Scroll-reveal** on `.band`/`.ring-card`/`.flow-step`/`.entry`/`.archive-card` (12–16px rise +
  fade). Progressive-enhancement rule: **hide via JS, never CSS** — JS adds `.reveal-ready` to
  `<html>`; if JS never runs nothing is hidden. Reduced-motion early-return skips it entirely.
- **Hero depth**: prefer a few-pixel parallax drift on the existing radial-gradient glow; hold the
  low-degree pointer card-tilt as a stretch (tilt on a legal instrument risks gimmick).
- **Depth via shadow**, not animation: extend the existing `.archive-card` hover shadow to
  `.ring-card`/`.entry`. Pure CSS.

## Sequencing
A (Venn explorer) → B (scoring explorer, pairs with A) → C (archive charts, needs the build
change) → D (motion/depth; ship reveal + shadows, soften/hold the tilt). Each is independently
shippable, reversible, and keeps the no-JS site fully functional.

## References (verified)
- A11Y Collective — Accessible SVG elements: https://www.a11y-collective.com/blog/svg-accessibility/
- TPGI — ARIA to enhance SVG accessibility: https://www.tpgi.com/using-aria-enhance-svg-accessibility/
- W3C Wiki — SVG Accessibility/Navigation (roving tabindex): https://www.w3.org/wiki/SVG_Accessibility/Navigation
- Ada Rose Cannon — reveal-on-scroll progressive enhancement: https://medium.com/samsung-internet-dev/building-a-menu-which-reveals-on-scroll-557f92909fd8
- CSS-Tricks — scroll-driven animations (graceful degradation): https://css-tricks.com/unleash-the-power-of-scroll-driven-animations/
- CSS-Tricks — charts with SVG (no-JS inline charts): https://css-tricks.com/how-to-make-charts-with-svg/
- DEV — 3D parallax via CSS variables: https://dev.to/webdiscus/3d-parallax-effect-by-moving-mouse-using-htmlcss-7b2
- Let's Build UI — 3D hover via CSS transforms: https://www.letsbuildui.dev/articles/a-3d-hover-effect-using-css-transforms/
