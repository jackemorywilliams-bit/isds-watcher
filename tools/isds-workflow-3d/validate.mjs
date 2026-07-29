#!/usr/bin/env node
// Fail-closed validator for the v2 plain-language workflow manifest + render
// config. Encodes every operator complaint from 2026-07-28 as a rule:
// overlap impossible (unique grid cells), no upward arrows (feedback arcs
// banned), plain-language descriptions required, all 9 sources present,
// purpose-colored edge kinds only, legend/config sanity.
import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const m = JSON.parse(readFileSync(resolve(here, "../../views/isds-workflow-3d/workflow.json"), "utf8"));
const rc = await import("./src/render-config.mjs");
const errors = [];

const NODE_KINDS = new Set(["auto", "process", "gate", "send", "role", "human"]);
const EDGE_KINDS = new Set(Object.keys(rc.EDGE_STYLE));

// -- professor-facing naming: the operator goes by EMORY; 'Jack' is banned --
for (const blob of [JSON.stringify(m.nodes), JSON.stringify(m.chips)])
  if (/\bJack\b/.test(blob)) errors.push("professor-facing text contains 'Jack' — he goes by Emory");

// -- chips: all nine sources, individually visualized --
if (m.chips.length !== 9) errors.push(`expected 9 source chips, got ${m.chips.length}`);
for (const c of m.chips) {
  if (!c.name || !c.tag) errors.push(`chip ${c.id}: missing name/tag`);
  if (!Array.isArray(c.evidence) || !c.evidence.length) errors.push(`chip ${c.id}: no evidence`);
}

// -- nodes: plain language, evidence, explicit unique grid cells --
if (!(m.nodes.length >= 20 && m.nodes.length <= 32))
  errors.push(`node count ${m.nodes.length} outside 20-32`);
const ids = new Map();
const cells = new Map();
for (const n of m.nodes) {
  if (ids.has(n.id)) errors.push(`duplicate id: ${n.id}`);
  ids.set(n.id, n);
  if (!rc.COLUMNS.includes(n.col)) errors.push(`${n.id}: unknown column ${n.col}`);
  if (!Number.isInteger(n.row) || n.row < 0) errors.push(`${n.id}: bad row`);
  if (!NODE_KINDS.has(n.kind)) errors.push(`${n.id}: bad kind ${n.kind}`);
  if (!n.title) errors.push(`${n.id}: missing title`);
  if (!n.desc) errors.push(`${n.id}: missing plain-language description`);
  else if (n.desc.length > rc.CARD.descChars * 3)
    errors.push(`${n.id}: desc too long for the card (${n.desc.length} > ${rc.CARD.descChars * 3})`);
  if (/\b(dedup|lexical|prescore|frontmatter|jsonl|SMIL|regex)\b/i.test(n.title))
    errors.push(`${n.id}: title contains jargon ('${n.title}')`);
  if (!n.target) errors.push(`${n.id}: missing markdown target`);
  if (!Array.isArray(n.evidence) || !n.evidence.length) errors.push(`${n.id}: no evidence`);
  if (!n.meta) errors.push(`${n.id}: missing meta line (model / mechanism attribution)`);
  else if (n.meta.length > 104) errors.push(`${n.id}: meta line too long (${n.meta.length})`);
  const cell = `${n.col}|${n.row}`;
  if (cells.has(cell)) errors.push(`OVERLAP: ${n.id} and ${cells.get(cell)} share cell ${cell}`);
  cells.set(cell, n.id);
}

// -- edges: endpoints exist, purpose kinds only, NEVER upward --
const seen = new Set();
for (const e of m.edges) {
  const key = `${e.source}->${e.target}`;
  if (seen.has(key)) errors.push(`duplicate edge ${key}`);
  seen.add(key);
  if (!EDGE_KINDS.has(e.kind)) errors.push(`edge ${key}: kind '${e.kind}' not in the legend vocabulary`);
  if (!e.evidence) errors.push(`edge ${key}: no evidence`);
  const s = e.source === "__sources" ? { row: -1 } : ids.get(e.source);
  const t = ids.get(e.target);
  if (!s) { errors.push(`edge ${key}: unknown source`); continue; }
  if (!t) { errors.push(`edge ${key}: unknown target`); continue; }
  if (t.row < s.row) errors.push(`UPWARD ARROW banned: ${key} (row ${s.row} -> ${t.row})`);
}

// -- connectivity: no floating cards --
const touched = new Set(m.edges.flatMap((e) => [e.source, e.target]));
for (const n of m.nodes) if (!touched.has(n.id)) errors.push(`floating card: ${n.id}`);

// -- render config sanity: exact-pixel guarantees at 1:1 --
if (rc.CARD.titlePx < 12) errors.push(`card title ${rc.CARD.titlePx}px < 12px`);
if (rc.CARD.descPx < 10) errors.push(`card desc ${rc.CARD.descPx}px < 10px`);
if (rc.CARD.w > rc.GRID.colWidth - 16) errors.push("card wider than its column");
if (rc.GRID.rowPitch < rc.CARD.h + 20) errors.push("row pitch too tight — cards would collide");
const totalW = rc.GRID.marginX * 2 + rc.COLUMNS.length * rc.GRID.colWidth;
if (totalW > 1100) errors.push(`total width ${totalW}px exceeds the 1100px pane budget`);
for (const kind of EDGE_KINDS) {
  const f = rc.FLOW[kind];
  if (!f || f.dots < 1) errors.push(`edge kind '${kind}' has no animated flow dots`);
}
// Every column used must have a title + color (feeds the legend).
for (const col of rc.COLUMNS)
  if (!rc.COL_TITLE[col] || !rc.COL_COLOR[col]) errors.push(`column '${col}' missing title/color`);

if (errors.length) {
  console.error(`VALIDATION FAILED (${errors.length}):`);
  for (const e of errors) console.error("  - " + e);
  process.exit(1);
}
console.log(`OK: 9 source chips, ${m.nodes.length} cards (all described, no overlaps), ` +
            `${m.edges.length} edges (no upward arrows), width ${totalW}px, animated dots on all ${EDGE_KINDS.size} edge kinds.`);
