// Shared render constants — imported by BOTH view-entry.js and validate.mjs so the
// legibility guard and the renderer can never drift apart.
export const SPACING = { stageX: 380, laneY: 250, depthZ: 180 };
export const LANE_Y = { control: -2.5, digest: -1.5, core: -0.5, council: 0.5, verification: 1.5, feedback: 2.5 };
// Labels are CONSTANT SCREEN SIZE (pixels), rescaled every frame from camera
// distance — world-sized text can never stay legible while framing a 13-stage
// pipeline in one pane. LOD: 'process' node labels appear once the camera is
// close enough that a stage column spans >= lodStagePx on screen; inputs, gates,
// outputs, feedback nodes and lane captions are labelled at every distance.
export const LABEL_PX = { node: 13, caption: 15, lodStagePx: 120 };
export const CAMERA = { fov: 45, padWorld: 160 };   // flat, flowchart-like lens; straight-on framing
export const NODE_RADIUS = { input: 13, process: 11, gate: 15, output: 13, feedback: 11 };
export const ARROWS = { length: 16, relPos: 0.55 };
export const PARTICLES = {
  core: { count: 4, speed: 0.006, width: 4 },
  control: { count: 2, speed: 0.004, width: 2.5 },
  council: { count: 3, speed: 0.005, width: 3 },
  gate: { count: 3, speed: 0.005, width: 3.5 },
  delivery: { count: 3, speed: 0.005, width: 3 },
  feedback: { count: 2, speed: 0.003, width: 3 },
};
export const CANVAS = { height: 700, background: "#0B1020" };
