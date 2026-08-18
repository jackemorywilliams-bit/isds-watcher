// Pure chart construction for the ISDS workflow flowchart — geometry, ports,
// text wrapping, edge paths, SMIL dot timing, and the legend. No DOM, no I/O:
// everything arrives via (manifest, config, factory), so the SAME code paints
// the vault view (DOM factory, dark theme, click-through) and the standalone
// site/README SVG (string factory, light theme, CSS dark overrides).
//
// Factory contract (the only capabilities the core may use):
//   el(name, attrs, parent) -> node   — create an element, set attributes,
//                                       append to parent when given
//   setText(node, str)                — set the node's text content
//
// Theming contract: every color is a named token resolved from
// config.THEMES[opts.theme]. paint() writes the resolved color as a
// presentation attribute (light-first robustness — renders even where CSS is
// ignored) AND tags the element with wf-f-<token> / wf-s-<token> classes so a
// stylesheet can re-skin the whole chart (the static renderer's
// prefers-color-scheme dark override).
//
// Structural classes (the validator counts these — keep them stable):
//   wf-card (card group) · wf-chip (source chip group) · wf-edge (edge path)
//   wf-dot (animated flow dot) · wf-legend (legend group)
//
// Determinism is the contract: identical (manifest, config, opts) must yield
// an identical element tree, byte-for-byte after serialization.

export function flattenTheme(theme) {
  const tokens = {};
  for (const [k, v] of Object.entries(theme)) {
    if (k === "col" || k === "edge") {
      for (const [k2, v2] of Object.entries(v)) tokens[`${k}-${k2}`] = v2;
    } else {
      tokens[k] = v;
    }
  }
  return tokens;
}

export function wrap(str, maxChars, maxLines) {
  const words = String(str).split(" ");
  const lines = [""];
  for (const w of words) {
    const cur = lines[lines.length - 1];
    if ((cur + " " + w).trim().length > maxChars && lines.length < maxLines) lines.push(w);
    else lines[lines.length - 1] = (cur + " " + w).trim();
  }
  return lines;
}

export function buildChart(manifest, config, factory, opts = {}) {
  const { COLUMNS, COL_TITLE, EDGE_STYLE, GRID, CARD, CHIP, FLOW, EDGES, THEMES } = config;
  const m = manifest;
  const { el, setText } = factory;
  const themeName = opts.theme || "dark";
  const theme = THEMES[themeName];
  if (!theme) throw new Error(`chart-core: unknown theme '${themeName}'`);
  const tokens = flattenTheme(theme);
  const FONT = opts.font || "-apple-system, sans-serif";
  const hooks = opts.hooks || {};

  // Fail closed on palette gaps — a missing token is a build error, not a
  // silently-black shape.
  const tok = (name) => {
    const v = tokens[name];
    if (v === undefined) throw new Error(`chart-core: theme '${themeName}' has no token '${name}'`);
    return v;
  };
  const paint = (attrs, fillTok, strokeTok) => {
    const cls = [];
    if (fillTok) { attrs.fill = tok(fillTok); cls.push(`wf-f-${fillTok}`); }
    if (strokeTok) { attrs.stroke = tok(strokeTok); cls.push(`wf-s-${strokeTok}`); }
    if (cls.length) attrs.class = attrs.class ? `${attrs.class} ${cls.join(" ")}` : cls.join(" ");
    return attrs;
  };
  const text = (parent, x, y, str, px, fillTok, o = {}) => {
    const t = el("text", paint({ x, y, "font-size": px, "font-family": FONT,
                                 "text-anchor": o.anchor || "middle",
                                 ...(o.weight ? { "font-weight": o.weight } : {}),
                                 ...(o.italic ? { "font-style": "italic" } : {}),
                                 ...(o.opacity ? { opacity: o.opacity } : {}) }, fillTok), parent);
    setText(t, str);
    return t;
  };

  const width = GRID.marginX * 2 + COLUMNS.length * GRID.colWidth;
  const maxRow = Math.max(...m.nodes.map((n) => n.row));
  // The chips lay out in ceil(chips/cols) rows; the fixed GRID.bannerH was
  // sized for 3 rows (9 chips). A 10th chip adds a 4th row that would overflow
  // the banner and collide with the columns band below. Grow the banner to the
  // actual chip-row height when that exceeds the fixed floor; Math.max keeps
  // <=3-row layouts byte-identical to before.
  const chipRows = Math.ceil(m.chips.length / CHIP.cols);
  const bannerH = Math.max(GRID.bannerH, 46 + chipRows * (CHIP.h + CHIP.gapY) + 24);
  const gridTop = bannerH + GRID.headerH;
  const gridH = (maxRow + 1) * GRID.rowPitch;
  const height = gridTop + gridH + GRID.legendH + 24;

  const svg = el("svg", { viewBox: `0 0 ${width} ${height}` });
  // Self-carried background: the chart stays internally consistent on ANY
  // surrounding page, whichever color scheme the media query resolves to.
  el("rect", paint({ x: 0, y: 0, width, height, rx: 10 }, "bg"), svg);

  const defs = el("defs", {}, svg);
  for (const kind of Object.keys(EDGE_STYLE)) {
    const mk = el("marker", { id: `arrow-${kind}`, viewBox: "0 0 10 10", refX: 9, refY: 5,
                              markerWidth: EDGES.arrow, markerHeight: EDGES.arrow,
                              orient: "auto-start-reverse" }, defs);
    el("path", paint({ d: "M 0 0 L 10 5 L 0 10 z" }, `edge-${kind}`), mk);
  }

  // ---- Sources banner: all fetchers as individual chips (rows grow the banner) ----
  const bannerW = CHIP.cols * CHIP.w + (CHIP.cols - 1) * CHIP.gapX + 32;
  const bannerX = (width - bannerW) / 2;
  el("rect", paint({ x: bannerX, y: 12, width: bannerW, height: bannerH - 34, rx: 12,
                     opacity: 0.06 }, "bannerTint"), svg);
  el("rect", paint({ x: bannerX, y: 12, width: bannerW, height: bannerH - 34, rx: 12,
                     fill: "none", "stroke-opacity": 0.35 }, null, "bannerTint"), svg);
  text(svg, width / 2, 34, "WHERE WE LOOK — THE 10 SOURCES, CHECKED EVERY RUN", 13, "bannerTitle", { weight: 700 });
  m.chips.forEach((c, i) => {
    const cx = bannerX + 16 + (i % CHIP.cols) * (CHIP.w + CHIP.gapX);
    const cy = 46 + Math.floor(i / CHIP.cols) * (CHIP.h + CHIP.gapY);
    const off = /off —|off:/.test(c.tag);
    const g = el("g", { class: "wf-chip" }, svg);
    el("rect", paint({ x: cx, y: cy, width: CHIP.w, height: CHIP.h, rx: CHIP.r,
                       "stroke-opacity": off ? 0.25 : 0.7,
                       ...(off ? { "stroke-dasharray": "4 3" } : {}) }, "chip", "bannerTint"), g);
    text(g, cx + CHIP.w / 2, cy + 18, c.name, CHIP.namePx, off ? "chipNameOff" : "chipName", { weight: 600 });
    text(g, cx + CHIP.w / 2, cy + 34, c.tag, CHIP.tagPx, off ? "chipTagOff" : "chipTag");
    const tip = el("title", {}, g);
    setText(tip, `${c.name} — ${c.tag}\nevidence: ${(c.evidence || []).join(", ")}`);
  });
  const bannerBottom = { x: width / 2, y: 46 + chipRows * (CHIP.h + CHIP.gapY) + 4 };

  // ---- Column headers + bands ----
  const colX = (col) => GRID.marginX + COLUMNS.indexOf(col) * GRID.colWidth;
  for (const col of COLUMNS) {
    const x = colX(col);
    el("rect", paint({ x: x + 2, y: gridTop - 6, width: GRID.colWidth - 12, height: gridH + 12, rx: 12,
                       opacity: 0.05 }, `col-${col}`), svg);
    text(svg, x + (GRID.colWidth - 12) / 2 + 2, bannerH + 22, COL_TITLE[col], 12.5,
         `col-${col}`, { weight: 700 });
  }

  // ---- Card positions from the explicit grid ----
  const pos = {};
  for (const n of m.nodes) {
    pos[n.id] = { x: colX(n.col) + (GRID.colWidth - 12) / 2 + 2,
                  y: gridTop + n.row * GRID.rowPitch + GRID.rowPitch / 2, n };
  }

  // ---- Edges (under cards), purpose-colored, downward/sideways only ----
  // PORTS (operator fix 2026-07-29): every edge leaves and enters through its
  // own slot along the card border, ordered left-to-right toward its
  // destination — two arrows can never overlap, so a line is always one color.
  const edgeLayer = el("g", {}, svg);
  const flowLayer = el("g", {}, svg);
  const outsOf = {}, insOf = {};
  for (const e of m.edges) {
    (outsOf[e.source] = outsOf[e.source] || []).push(e);
    (insOf[e.target] = insOf[e.target] || []).push(e);
  }
  const xOf = (id) => id === "__sources" ? bannerBottom.x : (pos[id] ? pos[id].x : 0);
  const portOffset = (list, e, keyFn) => {
    const sorted = list.slice().sort((a, b) => keyFn(a) - keyFn(b));
    const i = sorted.indexOf(e);
    const nSlots = sorted.length;
    const span = Math.min(CARD.w - 40, nSlots * 44);
    return nSlots <= 1 ? 0 : (i - (nSlots - 1) / 2) * (span / (nSlots - 1));
  };
  const anchors = (s, t, e) => {
    const outOff = portOffset(outsOf[e.source] || [e], e, (x) => xOf(x.target));
    const inOff = portOffset(insOf[e.target] || [e], e, (x) => xOf(x.source));
    if (Math.abs(t.y - s.y) < GRID.rowPitch / 2) {      // same row: side to side
      const dir = t.x > s.x ? 1 : -1;
      return { x1: s.x + dir * CARD.w / 2, y1: s.y + outOff / 3,
               x2: t.x - dir * CARD.w / 2, y2: t.y + inOff / 3, side: true };
    }
    return { x1: s.x + outOff, y1: s.y + CARD.h / 2,
             x2: t.x + inOff, y2: t.y - CARD.h / 2, side: false };
  };
  for (const e of m.edges) {
    const kind = EDGE_STYLE[e.kind] ? e.kind : "flow";
    const s = e.source === "__sources" ? bannerBottom
            : pos[e.source] && { x: pos[e.source].x, y: pos[e.source].y };
    const t = pos[e.target];
    if (!s || !t) continue;
    let d;
    if (e.source === "__sources") {
      const inOff = portOffset(insOf[e.target] || [e], e, (x) => xOf(x.source));
      d = `M ${s.x} ${s.y} C ${s.x} ${s.y + 40}, ${t.x + inOff} ${t.y - CARD.h / 2 - 40}, ${t.x + inOff} ${t.y - CARD.h / 2}`;
    } else {
      const a = anchors(pos[e.source], t, e);
      if (a.side) {
        d = `M ${a.x1} ${a.y1} C ${(a.x1 + a.x2) / 2} ${a.y1 - 22}, ${(a.x1 + a.x2) / 2} ${a.y2 - 22}, ${a.x2} ${a.y2}`;
      } else {
        const bend = Math.min(56, Math.max(24, (a.y2 - a.y1) / 2));
        d = `M ${a.x1} ${a.y1} C ${a.x1} ${a.y1 + bend}, ${a.x2} ${a.y2 - bend}, ${a.x2} ${a.y2}`;
      }
    }
    el("path", paint({ d, fill: "none", "stroke-width": EDGES.width, "stroke-opacity": 0.75,
                       "marker-end": `url(#arrow-${kind})`, class: "wf-edge" }, null, `edge-${kind}`), edgeLayer);
    const f = FLOW[kind] ?? FLOW.flow;
    for (let i = 0; i < f.dots; i++) {
      const dot = el("circle", paint({ r: f.r, opacity: 0.9, class: "wf-dot" }, `edge-${kind}`), flowLayer);
      el("animateMotion", { dur: `${f.dur}s`, repeatCount: "indefinite",
                            begin: `${-(i * f.dur / f.dots).toFixed(2)}s`, path: d }, dot);
    }
  }

  // ---- Cards: title + plain-language description, always visible ----
  const cardLayer = el("g", {}, svg);
  const KIND_BADGE = { gate: "AUTO CHECK", auto: "AUTOMATIC", send: "✉ SENT", human: "HUMAN", role: "AI ROLE", process: "" };
  for (const { x, y, n } of Object.values(pos)) {
    const g = el("g", { class: "wf-card" }, cardLayer);
    const colTok = `col-${n.col}`;
    const heavy = n.kind === "gate" || n.kind === "human";
    el("rect", paint({ x: x - CARD.w / 2, y: y - CARD.h / 2, width: CARD.w, height: CARD.h, rx: CARD.r,
                       "stroke-width": heavy ? 2.4 : 1.3 }, "card", colTok), g);
    el("rect", paint({ x: x - CARD.w / 2, y: y - CARD.h / 2, width: 5, height: CARD.h, rx: 2 }, colTok), g);
    // Badge gets its OWN reserved top strip (no collision with the title — the
    // operator's overlap complaint), title sits on the next line, then up to
    // three description lines, then the model/mechanism line.
    const top = y - CARD.h / 2;
    const badge = KIND_BADGE[n.kind];
    if (badge) text(g, x + CARD.w / 2 - 9, top + 13, badge, 8, colTok,
                    { anchor: "end", weight: 700, opacity: 0.9 });
    text(g, x + 2, top + 31, n.title, CARD.titlePx, "cardTitle", { weight: 650 });
    wrap(n.desc, CARD.descChars, CARD.descLines).forEach((line, i) => {
      text(g, x + 2, top + 47 + i * 13, line, CARD.descPx, "cardDesc");
    });
    if (n.meta) {
      const metaLines = wrap(n.meta, 52, 1);
      text(g, x + 2, top + CARD.h - 9, metaLines[0], CARD.metaPx, colTok,
           { opacity: 0.85, italic: true });
    }
    const tip = el("title", {}, g);
    setText(tip, `${n.title} — ${n.desc}\n\nevidence:\n` +
      (n.evidence || []).map((e2) => "• " + e2).join("\n"));
    if (hooks.card) hooks.card(g, n);   // interactivity is the consumer's business
  }

  // ---- Legend: what the colors mean ----
  const legend = el("g", { class: "wf-legend" }, svg);
  const ly = gridTop + gridH + 18;
  el("rect", paint({ x: GRID.marginX, y: ly, width: width - GRID.marginX * 2, height: GRID.legendH - 12,
                     rx: 10, opacity: 0.03 }, "legendBg"), legend);
  text(legend, GRID.marginX + 14, ly + 20, "KEY", 12, "legendTitle", { anchor: "start", weight: 700 });
  const lx = GRID.marginX + 14;
  Object.entries(EDGE_STYLE).forEach(([kind, st], i) => {
    const yy = ly + 42 + (i % 2) * 22;
    const xx = lx + Math.floor(i / 2) * (width / 2 - 40);
    el("line", paint({ x1: xx, y1: yy - 4, x2: xx + 34, y2: yy - 4, "stroke-width": 3,
                       "marker-end": `url(#arrow-${kind})` }, null, `edge-${kind}`), legend);
    text(legend, xx + 44, yy, st.label, 11, "legendText", { anchor: "start" });
  });
  text(legend, GRID.marginX + 14, ly + 96, "moving dots = work flowing right now · box colors = who does it: ", 11,
       "legendText", { anchor: "start" });
  let cx2 = GRID.marginX + 14;
  COLUMNS.forEach((col) => {
    el("circle", paint({ cx: cx2 + 6, cy: ly + 112, r: 5 }, `col-${col}`), legend);
    text(legend, cx2 + 16, ly + 116, COL_TITLE[col].split(" (")[0].toLowerCase(), 10.5,
         "legendText", { anchor: "start" });
    cx2 += 16 + COL_TITLE[col].split(" (")[0].length * 6.4 + 26;
  });

  return { svg, width, height };
}
