#!/usr/bin/env node
// Fail-closed validator for views/isds-workflow-3d/workflow.json.
// Rules: 18-24 nodes; unique ids; every edge endpoint exists; normal edges move
// forward or stay in stage; feedback edges return to a strictly earlier stage;
// every node/edge carries evidence; lanes and kinds from the closed vocabularies.
import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const manifestPath = resolve(here, "../../views/isds-workflow-3d/workflow.json");
const m = JSON.parse(readFileSync(manifestPath, "utf8"));

const LANES = new Set(["control", "core", "digest", "council", "verification", "feedback"]);
const NODE_KINDS = new Set(["input", "process", "gate", "output", "feedback"]);
const EDGE_KINDS = new Set(["core", "control", "council", "gate", "delivery", "feedback"]);
const errors = [];

if (!(m.nodes.length >= 18 && m.nodes.length <= 24))
  errors.push(`node count ${m.nodes.length} outside 18-24`);

const ids = new Map();
for (const n of m.nodes) {
  if (ids.has(n.id)) errors.push(`duplicate node id: ${n.id}`);
  ids.set(n.id, n);
  if (!LANES.has(n.lane)) errors.push(`${n.id}: bad lane ${n.lane}`);
  if (!NODE_KINDS.has(n.kind)) errors.push(`${n.id}: bad kind ${n.kind}`);
  if (!Number.isInteger(n.stage) || n.stage < 0) errors.push(`${n.id}: bad stage`);
  if (!Number.isInteger(n.depth) || n.depth < 0) errors.push(`${n.id}: bad depth`);
  if (!n.label || !n.summary) errors.push(`${n.id}: missing label/summary`);
  if (!n.target) errors.push(`${n.id}: missing markdown target`);
  if (!Array.isArray(n.evidence) || n.evidence.length === 0)
    errors.push(`${n.id}: no evidence`);
}

// No two nodes may share (lane, stage, depth) — they would occupy one 3D point.
const cells = new Map();
for (const n of m.nodes) {
  const key = `${n.lane}|${n.stage}|${n.depth}`;
  if (cells.has(key)) errors.push(`coordinate collision: ${n.id} and ${cells.get(key)} both at ${key}`);
  cells.set(key, n.id);
}

const edgeSeen = new Set();
for (const e of m.edges) {
  const key = `${e.source}->${e.target}`;
  if (edgeSeen.has(key)) errors.push(`duplicate edge: ${key}`);
  edgeSeen.add(key);
  const s = ids.get(e.source), t = ids.get(e.target);
  if (!s) { errors.push(`edge ${key}: unknown source`); continue; }
  if (!t) { errors.push(`edge ${key}: unknown target`); continue; }
  if (!EDGE_KINDS.has(e.kind)) errors.push(`edge ${key}: bad kind ${e.kind}`);
  if (!e.evidence) errors.push(`edge ${key}: no evidence`);
  if (e.kind === "feedback") {
    if (t.stage >= s.stage) errors.push(`feedback edge ${key} must return to an earlier stage (${s.stage} -> ${t.stage})`);
  } else if (t.stage < s.stage) {
    errors.push(`edge ${key} moves backward (${s.stage} -> ${t.stage}) without kind=feedback`);
  }
}

// Every node must be connected.
const touched = new Set(m.edges.flatMap((e) => [e.source, e.target]));
for (const n of m.nodes) if (!touched.has(n.id)) errors.push(`orphan node: ${n.id}`);

if (errors.length) {
  console.error(`VALIDATION FAILED (${errors.length}):`);
  for (const e of errors) console.error("  - " + e);
  process.exit(1);
}
console.log(`OK: ${m.nodes.length} nodes, ${m.edges.length} edges, all rules pass.`);

// ---- Legibility invariants (guard for the 2026-07-27 microscopic-smudge class) ----
// The render constants are checked against the manifest's REAL bounding box: a
// future edit that shrinks text/spheres relative to node spacing fails the build.
const rc = await import("./src/render-config.mjs");
const legErrors = [];
const stages = m.nodes.map((n) => n.stage);
const stageSpan = (Math.max(...stages) - Math.min(...stages)) || 1;

// Labels: at least 5.5% of inter-stage spacing (old failure: 9/220 = 4.1%).
const labelRatio = rc.TEXT.nodeLabelHeight / rc.SPACING.stageX;
if (labelRatio < 0.055)
  legErrors.push(`label/stage-spacing ratio ${labelRatio.toFixed(3)} < 0.055 — labels will be microscopic at full framing`);

// Spheres: at least 2.8% of inter-stage spacing (old failure: 6/220 = 2.7%).
const minRadius = Math.min(...Object.values(rc.NODE_RADIUS));
if (minRadius / rc.SPACING.stageX < 0.028)
  legErrors.push(`min sphere radius ${minRadius} too small for stage spacing ${rc.SPACING.stageX} — dust particles`);

// Spacing floors (operator-ordered minimums).
if (rc.SPACING.stageX < 350) legErrors.push(`stageX ${rc.SPACING.stageX} < 350`);
if (rc.SPACING.laneY < 250) legErrors.push(`laneY ${rc.SPACING.laneY} < 250`);
if (rc.SPACING.depthZ < 180) legErrors.push(`depthZ ${rc.SPACING.depthZ} < 180`);

// Arrows must scale with the layout (visible against stage spacing).
if (rc.ARROWS.length / rc.SPACING.stageX < 0.035)
  legErrors.push(`arrow length ${rc.ARROWS.length} invisible at stage spacing ${rc.SPACING.stageX}`);

// The flow must actually animate: every edge kind carries particles.
for (const kind of EDGE_KINDS)
  if (!rc.PARTICLES[kind] || rc.PARTICLES[kind].count < 1)
    legErrors.push(`edge kind '${kind}' has no flow particles — the animated-flow requirement`);

// Camera must use zoomToFit framing, not a guessed fixed position.
if (!(rc.CAMERA.zoomFitMs >= 0 && rc.CAMERA.zoomFitPadding >= 0))
  legErrors.push("CAMERA zoomToFit parameters missing");

if (legErrors.length) {
  console.error(`LEGIBILITY GUARD FAILED (${legErrors.length}):`);
  for (const e of legErrors) console.error("  - " + e);
  process.exit(1);
}
console.log(`Legibility guard OK (stage span ${stageSpan}, label ratio ${labelRatio.toFixed(3)}, min radius ${minRadius}).`);
