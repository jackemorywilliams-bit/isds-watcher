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
