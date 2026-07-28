// Shared render constants — imported by BOTH view-entry.js and validate.mjs.
// ARCHITECTURE (post-audit 2026-07-27): document-native vertical swimlane
// flowchart in SVG. Six lane columns across the pane, stages flow top->bottom,
// everything at natural 1:1 scale — text size is EXACT pixels, guaranteed by
// construction, with no camera, no zoom, no WebGL. Flow animates via native
// SMIL motion dots on every edge.
export const LANE_ORDER = ["control", "core", "digest", "council", "verification", "feedback"];
export const GRID = {
  laneWidth: 172,       // px per lane column
  stagePitch: 132,      // px per stage row
  marginX: 16,
  headerH: 64,          // lane caption band
  depthDX: 16,          // small in-cell offset per depth level (layering)
  depthDY: 12,
};
export const CARD = { w: 142, h: 48, r: 9, textPx: 13, titlePx: 15 };
export const CAPTION_PX = 14;
export const EDGES = { width: 2, arrow: 7 };
export const FLOW = {
  // The animated-flow layer: SMIL dots per edge kind (count, seconds per traversal).
  core: { dots: 3, dur: 3.2, r: 4 },
  control: { dots: 2, dur: 4.5, r: 3 },
  council: { dots: 2, dur: 3.8, r: 3.5 },
  gate: { dots: 3, dur: 3.6, r: 4 },
  delivery: { dots: 2, dur: 3.8, r: 3.5 },
  feedback: { dots: 2, dur: 6.0, r: 3.5 },
};
