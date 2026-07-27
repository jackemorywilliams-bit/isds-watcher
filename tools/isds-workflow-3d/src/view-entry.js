// Deterministic 3D workflow view for the ISDS Thematic Watcher.
// Runs inside Dataview's dv.view() scope: `dv` and `input` are provided by the
// host; this bundle is the async function body (no window globals).
// Layout is FIXED: x = stage*220, y = laneOffset*150, z = depth*110 — no force
// drift, no DAG mode. Data comes exclusively from workflow.json (evidence-backed).
import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";
import { Group, Mesh, SphereGeometry, MeshLambertMaterial } from "three";

const LANE_Y = { control: -2.5, digest: -1.5, core: -0.5, council: 0.5, verification: 1.5, feedback: 2.5 };
const LANE_COLOR = {
  control: "#8892b0",       // slate — orchestration
  core: "#64b5f6",          // blue — the deterministic spine
  digest: "#81c784",        // green — deliverables
  council: "#ba9ffb",       // violet — the interpretive council
  verification: "#ffd54f",  // gold — the operator's evidence layer
  feedback: "#f48fb1",      // rose — the loops that make it cumulative
};
const EDGE_COLOR = {
  core: "#64b5f6", control: "#5c6784", council: "#9d86d9",
  gate: "#ffd54f", delivery: "#81c784", feedback: "#f48fb1",
};
const KIND_SHAPE_RADIUS = { input: 7, process: 6, gate: 8, output: 7, feedback: 6 };

async function main() {
  const container = dv.container;
  // Idempotent re-render: never stack a second canvas in this block.
  container.querySelectorAll(".isds-workflow-3d-host").forEach((el) => el.remove());
  const host = document.createElement("div");
  container.appendChild(host);
  host.className = "isds-workflow-3d-host";
  host.style.cssText = "width:100%;height:540px;border-radius:8px;overflow:hidden;position:relative;";

  const manifest = JSON.parse(await dv.io.load(input.data));

  const nodes = manifest.nodes.map((n) => {
    const x = n.stage * 220;
    const y = (LANE_Y[n.lane] ?? 0) * 150;
    const z = n.depth * 110;
    return { ...n, x, y, z, fx: x, fy: y, fz: z };
  });
  const links = manifest.edges.map((e) => ({ ...e }));

  const graph = ForceGraph3D()(host)
    .width(host.clientWidth || container.clientWidth || 800)
    .height(540)
    .backgroundColor("#0B1020")
    .graphData({ nodes, links })
    .enableNodeDrag(false)
    .cooldownTicks(0)
    .nodeThreeObject((node) => {
      const g = new Group();
      const r = KIND_SHAPE_RADIUS[node.kind] ?? 6;
      const color = LANE_COLOR[node.lane] ?? "#cccccc";
      g.add(new Mesh(new SphereGeometry(r, 16, 16),
                     new MeshLambertMaterial({ color, transparent: true, opacity: node.kind === "gate" ? 1 : 0.85 })));
      const label = new SpriteText(node.label, 9, "#e8ecf8");
      label.backgroundColor = "rgba(11,16,32,0.55)";
      label.padding = 1.5;
      label.borderRadius = 2;
      label.position.set(0, r + 11, 0);
      g.add(label);
      return g;
    })
    .linkColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkOpacity(0.55)
    .linkWidth((l) => (l.kind === "core" || l.kind === "gate" ? 1.6 : 0.8))
    .linkDirectionalArrowLength(6.5)
    .linkDirectionalArrowRelPos(0.58)
    .linkDirectionalArrowColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkCurvature((l) => (l.kind === "feedback" ? 0.35 : 0))
    .nodeLabel((n) => `<div style="max-width:340px"><b>${n.label}</b><br/>${n.summary}<br/>` +
      `<i>evidence: ${(n.evidence || []).join(" · ")}</i></div>`)
    .onNodeClick((node) => {
      if (node.target) dv.app.workspace.openLinkText(node.target, dv.current().file.path);
    });

  // Frame the whole pipeline: camera pulled back along z, centred on the spine.
  const xs = nodes.map((n) => n.x);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
  graph.cameraPosition({ x: cx, y: -40, z: 1450 }, { x: cx, y: 0, z: 0 }, 0);

  const ro = new ResizeObserver(() => {
    const w = host.clientWidth;
    if (w) graph.width(w);
  });
  ro.observe(host);

  // WebGL teardown when the block re-renders or the note closes.
  const cleanup = () => {
    try { ro.disconnect(); } catch {}
    try { graph._destructor && graph._destructor(); } catch {}
    try { host.remove(); } catch {}
  };
  if (dv.component && typeof dv.component.register === "function") {
    dv.component.register(cleanup);
  }
}

main().catch((err) => {
  // Fail closed and visibly: an honest error beats a blank block.
  const el = document.createElement("pre");
  el.textContent = "ISDS 3D workflow view failed: " + (err && err.message || err);
  dv.container.appendChild(el);
});
