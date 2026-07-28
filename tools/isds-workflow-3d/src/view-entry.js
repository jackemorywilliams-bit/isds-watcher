// ISDS Thematic Watcher — animated swimlane flowchart (post-audit rebuild).
// Runs inside Dataview's dv.view() scope (`dv`/`input` host-provided).
// Document-native SVG: six lane columns, stages flow top->bottom, natural 1:1
// scale (text is exact pixels by construction — no camera, no zoom, no WebGL).
// The flow ANIMATES via native SMIL dots traveling every edge; feedback dots
// visibly loop back up the right margin. Zero runtime dependencies.
import { LANE_ORDER, GRID, CARD, CAPTION_PX, EDGES, FLOW } from "./render-config.mjs";

const LANE_COLOR = {
  control: "#8892b0", core: "#64b5f6", digest: "#81c784",
  council: "#ba9ffb", verification: "#ffd54f", feedback: "#f48fb1",
};
const EDGE_COLOR = {
  core: "#64b5f6", control: "#7a86a8", council: "#9d86d9",
  gate: "#e6b83f", delivery: "#81c784", feedback: "#f48fb1",
};
const LANE_CAPTION = {
  control: "CONTROL", core: "CORE PIPELINE", digest: "DELIVERABLES",
  council: "COUNCIL", verification: "VERIFICATION", feedback: "FEEDBACK",
};
const NS = "http://www.w3.org/2000/svg";

function el(name, attrs, parent) {
  const e = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}

async function main() {
  const container = dv.container;
  container.querySelectorAll(".isds-workflow-flow-host").forEach((n) => n.remove());
  const manifest = JSON.parse(await dv.io.load(input.data));

  const laneX = (lane) => GRID.marginX + LANE_ORDER.indexOf(lane) * GRID.laneWidth;
  const stages = manifest.nodes.map((n) => n.stage);
  const maxStage = Math.max(...stages);
  const width = GRID.marginX * 2 + LANE_ORDER.length * GRID.laneWidth;
  const height = GRID.headerH + (maxStage + 1) * GRID.stagePitch + 40;

  const host = document.createElement("div");
  host.className = "isds-workflow-flow-host";
  host.style.cssText = "width:100%;overflow-x:auto;border-radius:10px;background:#0B1020;";
  container.appendChild(host);

  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, width: "100%",
                          style: `min-width:${Math.min(width, 900)}px;display:block;` }, host);

  // defs: arrowheads per edge kind
  const defs = el("defs", {}, svg);
  for (const [kind, color] of Object.entries(EDGE_COLOR)) {
    const m = el("marker", { id: `arrow-${kind}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
                             markerWidth: EDGES.arrow, markerHeight: EDGES.arrow, orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: color }, m);
  }

  // Lane bands + captions
  for (const lane of LANE_ORDER) {
    const x = laneX(lane);
    el("rect", { x, y: GRID.headerH, width: GRID.laneWidth - 8, height: height - GRID.headerH - 8,
                 fill: LANE_COLOR[lane], opacity: 0.045, rx: 10 }, svg);
    const cap = el("text", { x: x + (GRID.laneWidth - 8) / 2, y: GRID.headerH - 22,
                             fill: LANE_COLOR[lane], "font-size": CAPTION_PX, "font-weight": 700,
                             "text-anchor": "middle", "font-family": "var(--font-interface, sans-serif)",
                             opacity: 0.9 }, svg);
    cap.textContent = LANE_CAPTION[lane];
  }

  // Node positions (card centers)
  const pos = {};
  for (const n of manifest.nodes) {
    const x = laneX(n.lane) + (GRID.laneWidth - 8) / 2 + n.depth * GRID.depthDX;
    const y = GRID.headerH + n.stage * GRID.stagePitch + GRID.stagePitch / 2 + n.depth * GRID.depthDY;
    pos[n.id] = { x, y, n };
  }

  // Edges first (under the cards)
  const edgeLayer = el("g", {}, svg);
  const flowLayer = el("g", {}, svg);
  for (const e of manifest.edges) {
    const s = pos[e.source], t = pos[e.target];
    if (!s || !t) continue;
    const color = EDGE_COLOR[e.kind] ?? "#888";
    let d;
    if (e.kind === "feedback") {
      // Loop up the right margin so the return path reads as a return.
      const mx = width - GRID.marginX / 2 + 26;
      d = `M ${s.x + CARD.w / 2} ${s.y} C ${mx} ${s.y}, ${mx} ${t.y}, ${t.x + CARD.w / 2} ${t.y}`;
    } else if (t.y > s.y) {
      // Downstream: leave bottom edge, enter top edge.
      const y1 = s.y + CARD.h / 2, y2 = t.y - CARD.h / 2;
      const bend = Math.min(60, (y2 - y1) / 2 + 20);
      d = `M ${s.x} ${y1} C ${s.x} ${y1 + bend}, ${t.x} ${y2 - bend}, ${t.x} ${y2}`;
    } else {
      // Same stage row: side to side.
      const sx = s.x < t.x ? s.x + CARD.w / 2 : s.x - CARD.w / 2;
      const tx = s.x < t.x ? t.x - CARD.w / 2 : t.x + CARD.w / 2;
      d = `M ${sx} ${s.y} C ${(sx + tx) / 2} ${s.y - 26}, ${(sx + tx) / 2} ${t.y - 26}, ${tx} ${t.y}`;
    }
    el("path", { d, fill: "none", stroke: color, "stroke-width": EDGES.width,
                 "stroke-opacity": 0.55, "marker-end": `url(#arrow-${e.kind})` }, edgeLayer);
    // The animated flow: dots traveling the same path, staggered via negative begin.
    const f = FLOW[e.kind] ?? FLOW.core;
    for (let i = 0; i < f.dots; i++) {
      const dot = el("circle", { r: f.r, fill: color, opacity: 0.9 }, flowLayer);
      const am = el("animateMotion", { dur: `${f.dur}s`, repeatCount: "indefinite",
                                       begin: `${-(i * f.dur / f.dots).toFixed(2)}s`, path: d }, dot);
    }
  }

  // Cards
  const cardLayer = el("g", {}, svg);
  for (const { x, y, n } of Object.values(pos)) {
    const g = el("g", { style: "cursor:pointer;" }, cardLayer);
    const isGate = n.kind === "gate";
    el("rect", { x: x - CARD.w / 2, y: y - CARD.h / 2, width: CARD.w, height: CARD.h, rx: CARD.r,
                 fill: "#131a30", stroke: LANE_COLOR[n.lane] ?? "#999",
                 "stroke-width": isGate ? 2.5 : 1.4,
                 ...(isGate ? { "stroke-dasharray": "" } : {}) }, g);
    el("rect", { x: x - CARD.w / 2, y: y - CARD.h / 2, width: 5, height: CARD.h,
                 rx: 2, fill: LANE_COLOR[n.lane] ?? "#999" }, g);
    // Label: up to two lines, exact pixels.
    const words = String(n.label).split(" ");
    const lines = [""];
    for (const w of words) {
      const cur = lines[lines.length - 1];
      if ((cur + " " + w).trim().length > 19 && lines.length < 2) lines.push(w);
      else lines[lines.length - 1] = (cur + " " + w).trim();
    }
    lines.forEach((line, i) => {
      const t = el("text", { x: x + 3, y: y + (lines.length === 1 ? 4 : i === 0 ? -4 : 12),
                             fill: "#e8ecf8", "font-size": CARD.textPx, "text-anchor": "middle",
                             "font-family": "var(--font-interface, sans-serif)" }, g);
      t.textContent = line;
    });
    if (isGate) {
      const badge = el("text", { x: x + CARD.w / 2 - 10, y: y - CARD.h / 2 + 13,
                                 fill: LANE_COLOR[n.lane], "font-size": 11, "font-weight": 700,
                                 "text-anchor": "middle" }, g);
      badge.textContent = "⛨";
    }
    const tip = el("title", {}, g);
    tip.textContent = `${n.label} — ${n.summary}\n\nevidence:\n` +
      (n.evidence || []).map((e) => "• " + e).join("\n");
    g.addEventListener("click", () => {
      if (n.target) dv.app.workspace.openLinkText(n.target, dv.current().file.path);
    });
  }

  const cleanup = () => { try { host.remove(); } catch {} };
  if (dv.component && typeof dv.component.register === "function") dv.component.register(cleanup);
}

main().catch((err) => {
  const el2 = document.createElement("pre");
  el2.textContent = "ISDS workflow view failed: " + (err && err.message || err);
  dv.container.appendChild(el2);
});
