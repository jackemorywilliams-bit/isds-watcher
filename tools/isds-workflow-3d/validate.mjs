#!/usr/bin/env node
// Fail-closed validator for the v2 plain-language workflow manifest + render
// config. Encodes every operator complaint from 2026-07-28 as a rule:
// overlap impossible (unique grid cells), no upward arrows (feedback arcs
// banned), plain-language descriptions required, all 9 sources present,
// purpose-colored edge kinds only, legend/config sanity.
// Since 2026-07-30 it ALSO guards the committed site/README SVG
// (scripts/site_templates/assets/workflow.svg): freshness via the embedded
// inputs-sha256, well-formed XML, and structural counts — a stale or broken
// static render is a BUILD failure, not a screenshot Emory has to send.
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const manifestBytes = readFileSync(resolve(here, "../../views/isds-workflow-3d/workflow.json"));
const m = JSON.parse(manifestBytes.toString("utf8"));
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
  // WIDTH-ENFORCED: text must stay inside the card. ~5.3px/char at 9.5px meta,
  // ~6.6px/char at 13px title, against the 236px card (2026-07-29 overflow bug).
  else if (n.meta.length > 40) errors.push(`${n.id}: meta overflows the card (${n.meta.length} > 40 chars)`);
  if (n.title.length > 34) errors.push(`${n.id}: title overflows the card (${n.title.length} > 34 chars)`);
  // Agent cards must name a real model — never a bare 'Claude'.
  if ((n.kind === "role" || n.id === "ai-check") && !/Model: Claude (Fable|Opus|Haiku|Sonnet) [\d.]+/.test(n.meta))
    errors.push(`${n.id}: agent card must name a specific model (got '${n.meta}')`);
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

// -- committed site/README SVG: freshness + well-formedness + structure --
// The static render is a DELIVERABLE; if it drifts from the manifest or the
// render config, the build fails here — never silently on the site.
const svgRel = "scripts/site_templates/assets/workflow.svg";
let svgText = null;
try { svgText = readFileSync(resolve(here, "../../" + svgRel), "utf8"); }
catch { errors.push(`${svgRel} missing — run 'npm run render-static'`); }

// Strict well-formedness scanner for the exact XML subset render-static.mjs
// emits (decl, comments, elements with quoted attributes, escaped text — no
// DOCTYPE/PI/CDATA). Any raw '<'/'&', bad nesting, or truncation fails.
function xmlWellFormedError(s) {
  const nameRe = /[A-Za-z_][A-Za-z0-9_.:-]*/y;
  const entityOk = (chunk, where) =>
    /&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/.test(chunk) ? `bad entity in ${where}` : null;
  let i = 0;
  if (s.charCodeAt(0) === 0xfeff) i = 1;
  if (s.startsWith("<?xml", i)) {
    const e = s.indexOf("?>", i);
    if (e < 0) return "unterminated XML declaration";
    i = e + 2;
  }
  const stack = [];
  let rootSeen = false, rootClosed = false;
  while (i < s.length) {
    if (s[i] === "<") {
      if (s.startsWith("<!--", i)) {
        const e = s.indexOf("-->", i + 4);
        if (e < 0) return "unterminated comment";
        if (s.slice(i + 4, e).includes("--")) return "'--' inside a comment";
        i = e + 3; continue;
      }
      if (s[i + 1] === "/") {
        i += 2; nameRe.lastIndex = i;
        const mm = nameRe.exec(s);
        if (!mm) return `bad closing tag at offset ${i}`;
        i = nameRe.lastIndex;
        while (i < s.length && /\s/.test(s[i])) i++;
        if (s[i] !== ">") return `malformed closing tag </${mm[0]}`;
        i++;
        const open = stack.pop();
        if (open !== mm[0]) return `mismatched tags: <${open}> closed by </${mm[0]}>`;
        if (!stack.length) rootClosed = true;
        continue;
      }
      if (s[i + 1] === "!" || s[i + 1] === "?") return `unexpected markup at offset ${i}`;
      i += 1; nameRe.lastIndex = i;
      const mm = nameRe.exec(s);
      if (!mm) return `bad tag name at offset ${i}`;
      const nm = mm[0];
      i = nameRe.lastIndex;
      if (rootClosed) return "content after the root element";
      if (!stack.length && rootSeen) return "multiple root elements";
      for (;;) {
        while (i < s.length && /\s/.test(s[i])) i++;
        if (i >= s.length) return `unterminated tag <${nm}>`;
        if (s[i] === "/" && s[i + 1] === ">") { i += 2; rootSeen = true; if (!stack.length) rootClosed = true; break; }
        if (s[i] === ">") { i++; stack.push(nm); rootSeen = true; break; }
        nameRe.lastIndex = i;
        const am = nameRe.exec(s);
        if (!am) return `bad attribute in <${nm}> at offset ${i}`;
        i = nameRe.lastIndex;
        if (s[i] !== "=") return `attribute '${am[0]}' without value in <${nm}>`;
        i++;
        const q = s[i];
        if (q !== '"' && q !== "'") return `unquoted attribute value in <${nm}>`;
        const e = s.indexOf(q, i + 1);
        if (e < 0) return `unterminated attribute value in <${nm}>`;
        const val = s.slice(i + 1, e);
        if (val.includes("<")) return `raw '<' in attribute value in <${nm}>`;
        const ent = entityOk(val, `attribute value in <${nm}>`);
        if (ent) return ent;
        i = e + 1;
      }
      continue;
    }
    const nxt = s.indexOf("<", i);
    const chunk = nxt < 0 ? s.slice(i) : s.slice(i, nxt);
    if (!stack.length && chunk.trim()) return "text outside the root element";
    const ent = entityOk(chunk, "text");
    if (ent) return ent;
    i = nxt < 0 ? s.length : nxt;
  }
  if (stack.length) return `unclosed element <${stack[stack.length - 1]}>`;
  if (!rootSeen) return "no root element";
  return null;
}

if (svgText !== null) {
  // Freshness: the SVG must have been rendered from EXACTLY these inputs.
  const inputsSha = createHash("sha256")
    .update(manifestBytes)
    .update(readFileSync(resolve(here, "src/render-config.mjs")))
    .digest("hex");
  const shaMatch = svgText.match(/inputs-sha256: ([0-9a-f]{64})/);
  if (!shaMatch) errors.push(`${svgRel}: no inputs-sha256 comment — regenerate with 'npm run render-static'`);
  else if (shaMatch[1] !== inputsSha)
    errors.push(`${svgRel} is STALE (embedded ${shaMatch[1].slice(0, 12)}…, inputs are ${inputsSha.slice(0, 12)}…) — run 'npm run render-static'`);

  const xmlErr = xmlWellFormedError(svgText);
  if (xmlErr) errors.push(`${svgRel}: not well-formed XML — ${xmlErr}`);

  // Structure: counts pinned to the operator-accepted chart AND synced to the
  // manifest, so neither can drift alone.
  const count = (re) => (svgText.match(re) || []).length;
  const cards = count(/class="wf-card"/g);
  const chips = count(/class="wf-chip"/g);
  const edgePaths = count(/class="wf-edge /g);
  const motions = count(/<animateMotion /g);
  const expectDots = m.edges.reduce((a, e) => a + ((rc.FLOW[e.kind] ?? rc.FLOW.flow).dots), 0);
  if (cards !== m.nodes.length) errors.push(`${svgRel}: expected ${m.nodes.length} cards (manifest-derived), found ${cards}`);
  if (cards !== m.nodes.length) errors.push(`${svgRel}: ${cards} cards out of sync with manifest's ${m.nodes.length} nodes`);
  if (chips !== m.chips.length) errors.push(`${svgRel}: expected ${m.chips.length} source chips (manifest-derived), found ${chips}`);
  if (edgePaths !== m.edges.length) errors.push(`${svgRel}: expected ${m.edges.length} edge paths (manifest-derived), found ${edgePaths}`);
  if (edgePaths !== m.edges.length) errors.push(`${svgRel}: ${edgePaths} edge paths out of sync with manifest's ${m.edges.length} edges`);
  if (motions < 33) errors.push(`${svgRel}: only ${motions} animateMotion dots (need >= 33)`);
  if (motions !== expectDots) errors.push(`${svgRel}: ${motions} animateMotion dots, FLOW config expects ${expectDots}`);
  if (!/class="wf-legend"/.test(svgText)) errors.push(`${svgRel}: legend missing`);
  for (const [kind, st] of Object.entries(rc.EDGE_STYLE))
    if (!svgText.includes(st.label)) errors.push(`${svgRel}: legend label for '${kind}' missing`);
  if (/\bJack\b/.test(svgText)) errors.push(`${svgRel} contains 'Jack' — he goes by Emory`);
}

if (errors.length) {
  console.error(`VALIDATION FAILED (${errors.length}):`);
  for (const e of errors) console.error("  - " + e);
  process.exit(1);
}
console.log(`OK: 9 source chips, ${m.nodes.length} cards (all described, no overlaps), ` +
            `${m.edges.length} edges (no upward arrows), width ${totalW}px, animated dots on all ${EDGE_KINDS.size} edge kinds.`);
console.log(`OK: ${svgRel} fresh (inputs-sha256 match), well-formed, ` +
            `${m.nodes.length} cards / 9 chips / ${m.edges.length} edge paths / legend present, zero 'Jack'.`);
