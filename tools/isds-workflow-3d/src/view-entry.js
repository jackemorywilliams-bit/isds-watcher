// ISDS Thematic Watcher — animated workflow flowchart, v2 (vault adapter).
// ALL chart construction (geometry, ports, wrapping, edge paths, SMIL dot
// timing, legend) lives in chart-core.mjs; this file only supplies what is
// vault-specific: the DOM element factory, the dark theme + Obsidian font,
// the host <div>, click-through to markdown targets, and dv lifecycle.
// render-static.mjs feeds the SAME core a string factory for the site SVG.
import * as config from "./render-config.mjs";
import { buildChart } from "./chart-core.mjs";

const NS = "http://www.w3.org/2000/svg";
const factory = {
  el(name, attrs, parent) {
    const e = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
    if (parent) parent.appendChild(e);
    return e;
  },
  setText(node, str) { node.textContent = str; },
};

async function main() {
  const container = dv.container;
  container.querySelectorAll(".isds-workflow-flow-host").forEach((n) => n.remove());
  const manifest = JSON.parse(await dv.io.load(input.data));

  const host = document.createElement("div");
  host.className = "isds-workflow-flow-host";
  host.style.cssText = `width:100%;overflow-x:auto;border-radius:10px;background:${config.THEMES.dark.bg};`;
  container.appendChild(host);

  const { svg, width } = buildChart(manifest, config, factory, {
    theme: "dark",
    font: "var(--font-interface, -apple-system, sans-serif)",
    hooks: {
      // Click-through into the vault is DOM-only — the static SVG never gets it.
      card(g, n) {
        g.setAttribute("style", "cursor:pointer;");
        g.addEventListener("click", () => {
          if (n.target) dv.app.workspace.openLinkText(n.target, dv.current().file.path);
        });
      },
    },
  });
  svg.setAttribute("width", "100%");
  svg.setAttribute("style", `min-width:${Math.min(width, 920)}px;display:block;`);
  host.appendChild(svg);

  const cleanup = () => { try { host.remove(); } catch {} };
  if (dv.component && typeof dv.component.register === "function") dv.component.register(cleanup);
}

main().catch((err) => {
  const p = document.createElement("pre");
  p.textContent = "ISDS workflow view failed: " + (err && err.message || err);
  dv.container.appendChild(p);
});
