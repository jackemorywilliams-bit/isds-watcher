// Shared render constants — imported by view-entry.js, chart-core.mjs,
// render-static.mjs, and validate.mjs.
// v2 (operator feedback 2026-07-28): explicit-grid swimlane flowchart with a
// sources banner, four labelled columns, purpose-colored arrows + legend, and
// descriptions ON every card. Natural 1:1 scale — text is exact pixels.
//
// FRESHNESS GUARD: this file is one of the two hashed inputs of the committed
// site SVG (with views/isds-workflow-3d/workflow.json). Any change here —
// layout OR palette — makes scripts/site_templates/assets/workflow.svg stale;
// validate.mjs fails until 'npm run render-static' re-renders it.
export const COLUMNS = ["machine", "deliverables", "council", "jack"];
export const COL_TITLE = {
  machine: "THE MACHINE (runs itself)",
  deliverables: "WHAT GETS SENT",
  council: "THE AI RESEARCH COUNCIL",
  jack: "EMORY — RESEARCHER CHECKS",
};
export const COL_COLOR = { machine: "#64b5f6", deliverables: "#81c784", council: "#ba9ffb", jack: "#ffd54f" };
// Arrow colors mean the ACTION, not the lane (operator: editor->brief email must
// read as a SEND). Legend rendered from this table.
export const EDGE_STYLE = {
  flow:    { color: "#64b5f6", label: "the machine moving items — through scoring and into the council" },
  send:    { color: "#81c784", label: "the machine delivering — the digest email and public site" },
  check:   { color: "#e6b83f", label: "verification and fact-checking (Emory\u2019s column)" },
  council: { color: "#ba9ffb", label: "the council producing — hand-offs, the brief, minutes, Emory\u2019s packet" },
};
export const GRID = { colWidth: 258, rowPitch: 130, marginX: 14, bannerH: 210, headerH: 40, legendH: 128 };
export const CARD = { w: 236, h: 104, r: 10, titlePx: 13, descPx: 11, descChars: 42, descLines: 3, metaPx: 9.5 };
export const CHIP = { w: 214, h: 44, r: 8, cols: 3, gapX: 16, gapY: 12, namePx: 12, tagPx: 10 };
export const FLOW = {
  flow: { dots: 3, dur: 3.2, r: 4 },
  send: { dots: 2, dur: 3.6, r: 3.5 },
  check: { dots: 2, dur: 3.4, r: 3.5 },
  council: { dots: 2, dur: 3.8, r: 3.5 },
};
export const EDGES = { width: 2, arrow: 7 };

// Named color tokens per theme, consumed by chart-core.buildChart via
// flattenTheme (col/edge sub-objects expand to col-<name> / edge-<name>).
export const THEMES = {
  // The vault's operator-accepted dark look (host background #0B1020) — the
  // exact values of flowchart v2.6, now table-driven instead of inline.
  dark: {
    bg: "#0B1020", card: "#131a30", chip: "#131a30",
    cardTitle: "#e8ecf8", cardDesc: "#9aa7c7",
    chipName: "#e8ecf8", chipTag: "#9aa7c7", chipNameOff: "#7c88a8", chipTagOff: "#66718e",
    bannerTitle: "#9fc6f5", bannerTint: "#64b5f6",
    legendBg: "#ffffff", legendTitle: "#e8ecf8", legendText: "#9aa7c7",
    col: { ...COL_COLOR },
    edge: Object.fromEntries(Object.entries(EDGE_STYLE).map(([k, v]) => [k, v.color])),
  },
  // Light variant for the professor-facing site + GitHub README, harmonized
  // with docs/assets/style.css (cream #faf9f6, paper cards, ink text, the
  // site's gold #9a7b2e and badge green #1a6b3a). The four edge semantics —
  // steel navy / green / ochre / purple — pass the dataviz six-check palette
  // validator on the light surface (lightness band, chroma floor, CVD ΔE,
  // normal-vision floor, 3:1 contrast); the site navy #0b3d5c itself fails
  // the lightness band, so lines use the snapped step #2a6496 while headings
  // keep the true site navy.
  light: {
    bg: "#faf9f6", card: "#ffffff", chip: "#ffffff",
    cardTitle: "#1c2530", cardDesc: "#3a4654",
    chipName: "#1c2530", chipTag: "#6a7280", chipNameOff: "#6a7280", chipTagOff: "#9aa3ad",
    bannerTitle: "#0b3d5c", bannerTint: "#2a6496",
    legendBg: "#1c2530", legendTitle: "#0b3d5c", legendText: "#3a4654",
    col: { machine: "#2a6496", deliverables: "#1a6b3a", council: "#6b4fa1", jack: "#9a7b2e" },
    edge: { flow: "#2a6496", send: "#1a6b3a", check: "#9a7b2e", council: "#6b4fa1" },
  },
};
