// Shared render constants — imported by BOTH view-entry.js and validate.mjs so the
// legibility guard and the renderer can never drift apart. Every value here is
// checked by validate.mjs against ratio invariants derived from the manifest's
// real bounding box (the 2026-07-27 "microscopic smudge" regression class).
export const SPACING = { stageX: 380, laneY: 250, depthZ: 180 };
export const LANE_Y = { control: -2.5, digest: -1.5, core: -0.5, council: 0.5, verification: 1.5, feedback: 2.5 };
export const TEXT = { nodeLabelHeight: 22, laneCaptionHeight: 46 };
export const NODE_RADIUS = { input: 13, process: 11, gate: 15, output: 13, feedback: 11 };
export const ARROWS = { length: 16, relPos: 0.55 };
export const PARTICLES = {
  // The "actively animates the flow" layer: directional particles per edge kind.
  core: { count: 4, speed: 0.006, width: 4 },
  control: { count: 2, speed: 0.004, width: 2.5 },
  council: { count: 3, speed: 0.005, width: 3 },
  gate: { count: 3, speed: 0.005, width: 3.5 },
  delivery: { count: 3, speed: 0.005, width: 3 },
  feedback: { count: 2, speed: 0.003, width: 3 },
};
export const CANVAS = { height: 620, background: "#0B1020" };
export const CAMERA = { zoomFitMs: 1000, zoomFitPadding: 100 };
