// Shared render constants — imported by BOTH view-entry.js and validate.mjs.
// v2 (operator feedback 2026-07-28): explicit-grid swimlane flowchart with a
// sources banner, four labelled columns, purpose-colored arrows + legend, and
// descriptions ON every card. Natural 1:1 scale — text is exact pixels.
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
