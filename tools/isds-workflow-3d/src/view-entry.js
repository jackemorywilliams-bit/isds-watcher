// ISDS Thematic Watcher — animated workflow flowchart, v2.
// Plain-language cards WITH descriptions, all 9 sources visualized, four
// labelled columns, purpose-colored arrows + legend, no feedback arcs.
// Document-native SVG at 1:1 scale; flow animates via native SMIL dots.
import { COLUMNS, COL_TITLE, COL_COLOR, EDGE_STYLE, GRID, CARD, CHIP, FLOW, EDGES } from "./render-config.mjs";

const NS = "http://www.w3.org/2000/svg";
const FONT = "var(--font-interface, -apple-system, sans-serif)";

function el(name, attrs, parent) {
  const e = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
  if (parent) parent.appendChild(e);
  return e;
}
function text(parent, x, y, str, px, fill, opts = {}) {
  const t = el("text", { x, y, fill, "font-size": px, "font-family": FONT,
                         "text-anchor": opts.anchor || "middle",
                         ...(opts.weight ? { "font-weight": opts.weight } : {}),
                         ...(opts.opacity ? { opacity: opts.opacity } : {}) }, parent);
  t.textContent = str;
  return t;
}
function wrap(str, maxChars, maxLines) {
  const words = String(str).split(" ");
  const lines = [""];
  for (const w of words) {
    const cur = lines[lines.length - 1];
    if ((cur + " " + w).trim().length > maxChars && lines.length < maxLines) lines.push(w);
    else lines[lines.length - 1] = (cur + " " + w).trim();
  }
  return lines;
}

async function main() {
  const container = dv.container;
  container.querySelectorAll(".isds-workflow-flow-host").forEach((n) => n.remove());
  const m = JSON.parse(await dv.io.load(input.data));

  const width = GRID.marginX * 2 + COLUMNS.length * GRID.colWidth;
  const maxRow = Math.max(...m.nodes.map((n) => n.row));
  const gridTop = GRID.bannerH + GRID.headerH;
  const gridH = (maxRow + 1) * GRID.rowPitch;
  const height = gridTop + gridH + GRID.legendH + 24;

  const host = document.createElement("div");
  host.className = "isds-workflow-flow-host";
  host.style.cssText = "width:100%;overflow-x:auto;border-radius:10px;background:#0B1020;";
  container.appendChild(host);
  const svg = el("svg", { viewBox: `0 0 ${width} ${height}`, width: "100%",
                          style: `min-width:${Math.min(width, 920)}px;display:block;` }, host);

  const defs = el("defs", {}, svg);
  for (const [kind, st] of Object.entries(EDGE_STYLE)) {
    const mk = el("marker", { id: `arrow-${kind}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
                              markerWidth: EDGES.arrow, markerHeight: EDGES.arrow,
                              orient: "auto-start-reverse" }, defs);
    el("path", { d: "M 0 0 L 10 5 L 0 10 z", fill: st.color }, mk);
  }

  // ---- Sources banner: all 9 fetchers as individual chips ----
  const bannerW = CHIP.cols * CHIP.w + (CHIP.cols - 1) * CHIP.gapX + 32;
  const bannerX = (width - bannerW) / 2;
  el("rect", { x: bannerX, y: 12, width: bannerW, height: GRID.bannerH - 34, rx: 12,
               fill: "#64b5f6", opacity: 0.06 }, svg);
  el("rect", { x: bannerX, y: 12, width: bannerW, height: GRID.bannerH - 34, rx: 12,
               fill: "none", stroke: "#64b5f6", "stroke-opacity": 0.35 }, svg);
  text(svg, width / 2, 34, "WHERE WE LOOK — THE 9 SOURCES, CHECKED EVERY RUN", 13, "#9fc6f5", { weight: 700 });
  const chipRows = Math.ceil(m.chips.length / CHIP.cols);
  m.chips.forEach((c, i) => {
    const cx = bannerX + 16 + (i % CHIP.cols) * (CHIP.w + CHIP.gapX);
    const cy = 46 + Math.floor(i / CHIP.cols) * (CHIP.h + CHIP.gapY);
    const off = /off —|off:/.test(c.tag);
    const g = el("g", {}, svg);
    el("rect", { x: cx, y: cy, width: CHIP.w, height: CHIP.h, rx: CHIP.r,
                 fill: "#131a30", stroke: "#64b5f6", "stroke-opacity": off ? 0.25 : 0.7,
                 ...(off ? { "stroke-dasharray": "4 3" } : {}) }, g);
    text(g, cx + CHIP.w / 2, cy + 18, c.name, CHIP.namePx, off ? "#7c88a8" : "#e8ecf8", { weight: 600 });
    text(g, cx + CHIP.w / 2, cy + 34, c.tag, CHIP.tagPx, off ? "#66718e" : "#9aa7c7");
    const tip = el("title", {}, g);
    tip.textContent = `${c.name} — ${c.tag}\nevidence: ${(c.evidence || []).join(", ")}`;
  });
  const bannerBottom = { x: width / 2, y: 46 + chipRows * (CHIP.h + CHIP.gapY) + 4 };

  // ---- Column headers + bands ----
  const colX = (col) => GRID.marginX + COLUMNS.indexOf(col) * GRID.colWidth;
  for (const col of COLUMNS) {
    const x = colX(col);
    el("rect", { x: x + 2, y: gridTop - 6, width: GRID.colWidth - 12, height: gridH + 12, rx: 12,
                 fill: COL_COLOR[col], opacity: 0.05 }, svg);
    text(svg, x + (GRID.colWidth - 12) / 2 + 2, GRID.bannerH + 22, COL_TITLE[col], 12.5,
         COL_COLOR[col], { weight: 700 });
  }

  // ---- Card positions from the explicit grid ----
  const pos = {};
  for (const n of m.nodes) {
    pos[n.id] = { x: colX(n.col) + (GRID.colWidth - 12) / 2 + 2,
                  y: gridTop + n.row * GRID.rowPitch + GRID.rowPitch / 2, n };
  }

  // ---- Edges (under cards), purpose-colored, downward/sideways only ----
  const edgeLayer = el("g", {}, svg);
  const flowLayer = el("g", {}, svg);
  const anchors = (s, t) => {
    if (Math.abs(t.y - s.y) < GRID.rowPitch / 2) {      // same row: side to side
      const dir = t.x > s.x ? 1 : -1;
      return { x1: s.x + dir * CARD.w / 2, y1: s.y, x2: t.x - dir * CARD.w / 2, y2: t.y, side: true };
    }
    return { x1: s.x, y1: s.y + CARD.h / 2, x2: t.x, y2: t.y - CARD.h / 2, side: false };
  };
  for (const e of m.edges) {
    const st = EDGE_STYLE[e.kind] ?? EDGE_STYLE.flow;
    let s = e.source === "__sources" ? bannerBottom : pos[e.source] && { x: pos[e.source].x, y: pos[e.source].y }
    ;
    const t = pos[e.target];
    if (!s || !t) continue;
    let d;
    if (e.source === "__sources") {
      d = `M ${s.x} ${s.y} C ${s.x} ${s.y + 40}, ${t.x} ${t.y - CARD.h / 2 - 40}, ${t.x} ${t.y - CARD.h / 2}`;
    } else {
      const a = anchors(pos[e.source], t);
      if (a.side) {
        d = `M ${a.x1} ${a.y1} C ${(a.x1 + a.x2) / 2} ${a.y1 - 22}, ${(a.x1 + a.x2) / 2} ${a.y2 - 22}, ${a.x2} ${a.y2}`;
      } else {
        const bend = Math.min(56, Math.max(24, (a.y2 - a.y1) / 2));
        d = `M ${a.x1} ${a.y1} C ${a.x1} ${a.y1 + bend}, ${a.x2} ${a.y2 - bend}, ${a.x2} ${a.y2}`;
      }
    }
    el("path", { d, fill: "none", stroke: st.color, "stroke-width": EDGES.width,
                 "stroke-opacity": 0.5, "marker-end": `url(#arrow-${e.kind})` }, edgeLayer);
    const f = FLOW[e.kind] ?? FLOW.flow;
    for (let i = 0; i < f.dots; i++) {
      const dot = el("circle", { r: f.r, fill: st.color, opacity: 0.9 }, flowLayer);
      el("animateMotion", { dur: `${f.dur}s`, repeatCount: "indefinite",
                            begin: `${-(i * f.dur / f.dots).toFixed(2)}s`, path: d }, dot);
    }
  }

  // ---- Cards: title + plain-language description, always visible ----
  const cardLayer = el("g", {}, svg);
  const KIND_BADGE = { gate: "AUTO CHECK", auto: "AUTOMATIC", send: "✉ SENT", human: "HUMAN", role: "AI ROLE", process: "" };
  for (const { x, y, n } of Object.values(pos)) {
    const g = el("g", { style: "cursor:pointer;" }, cardLayer);
    const color = COL_COLOR[n.col] ?? "#999";
    const heavy = n.kind === "gate" || n.kind === "human";
    el("rect", { x: x - CARD.w / 2, y: y - CARD.h / 2, width: CARD.w, height: CARD.h, rx: CARD.r,
                 fill: "#131a30", stroke: color, "stroke-width": heavy ? 2.4 : 1.3 }, g);
    el("rect", { x: x - CARD.w / 2, y: y - CARD.h / 2, width: 5, height: CARD.h, rx: 2, fill: color }, g);
    text(g, x + 2, y - CARD.h / 2 + 19, n.title, CARD.titlePx, "#e8ecf8", { weight: 650 });
    wrap(n.desc, CARD.descChars, 3).forEach((line, i) => {
      text(g, x + 2, y - CARD.h / 2 + 35 + i * 13, line, CARD.descPx, "#9aa7c7");
    });
    const badge = KIND_BADGE[n.kind];
    if (badge) text(g, x + CARD.w / 2 - 8, y - CARD.h / 2 + 11, badge, 8, color,
                    { anchor: "end", weight: 700, opacity: 0.9 });
    const tip = el("title", {}, g);
    tip.textContent = `${n.title} — ${n.desc}\n\nevidence:\n` +
      (n.evidence || []).map((e2) => "• " + e2).join("\n");
    g.addEventListener("click", () => {
      if (n.target) dv.app.workspace.openLinkText(n.target, dv.current().file.path);
    });
  }

  // ---- Legend: what the colors mean ----
  const ly = gridTop + gridH + 18;
  el("rect", { x: GRID.marginX, y: ly, width: width - GRID.marginX * 2, height: GRID.legendH - 12,
               rx: 10, fill: "#ffffff", opacity: 0.03 }, svg);
  text(svg, GRID.marginX + 14, ly + 20, "KEY", 12, "#e8ecf8", { anchor: "start", weight: 700 });
  let lx = GRID.marginX + 14;
  Object.entries(EDGE_STYLE).forEach(([kind, st], i) => {
    const yy = ly + 42 + (i % 2) * 22;
    const xx = lx + Math.floor(i / 2) * (width / 2 - 40);
    el("line", { x1: xx, y1: yy - 4, x2: xx + 34, y2: yy - 4, stroke: st.color,
                 "stroke-width": 3, "marker-end": `url(#arrow-${kind})` }, svg);
    text(svg, xx + 44, yy, st.label, 11, "#9aa7c7", { anchor: "start" });
  });
  text(svg, GRID.marginX + 14, ly + 96, "moving dots = work flowing right now · box colors = who does it: ", 11,
       "#9aa7c7", { anchor: "start" });
  let cx2 = GRID.marginX + 14;
  COLUMNS.forEach((col) => {
    el("circle", { cx: cx2 + 6, cy: ly + 112, r: 5, fill: COL_COLOR[col] }, svg);
    const t = text(svg, cx2 + 16, ly + 116, COL_TITLE[col].split(" (")[0].toLowerCase(), 10.5,
                   "#9aa7c7", { anchor: "start" });
    cx2 += 16 + COL_TITLE[col].split(" (")[0].length * 6.4 + 26;
  });

  const cleanup = () => { try { host.remove(); } catch {} };
  if (dv.component && typeof dv.component.register === "function") dv.component.register(cleanup);
}

main().catch((err) => {
  const p = document.createElement("pre");
  p.textContent = "ISDS workflow view failed: " + (err && err.message || err);
  dv.container.appendChild(p);
});
