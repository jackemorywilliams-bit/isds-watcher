// Deterministic 3D workflow view for the ISDS Thematic Watcher.
// Runs inside Dataview's dv.view() scope (`dv`/`input` are host-provided).
// Fixed layout (x = stage*SPACING.stageX etc.) — no force drift, no DAG mode.
// The pipeline's MOVEMENT is shown by directional particles flowing along every
// edge (per-kind speed/density), per the operator's flow-chart intent.
// All scale constants live in render-config.mjs, guarded by validate.mjs.
import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";
import { Group, Mesh, SphereGeometry, MeshLambertMaterial } from "three";
import { SPACING, LANE_Y, TEXT, NODE_RADIUS, ARROWS, PARTICLES, CANVAS, CAMERA } from "./render-config.mjs";

const LANE_COLOR = {
  control: "#8892b0", core: "#64b5f6", digest: "#81c784",
  council: "#ba9ffb", verification: "#ffd54f", feedback: "#f48fb1",
};
const EDGE_COLOR = {
  core: "#64b5f6", control: "#5c6784", council: "#9d86d9",
  gate: "#ffd54f", delivery: "#81c784", feedback: "#f48fb1",
};
const LANE_CAPTION = {
  control: "CONTROL", core: "CORE PIPELINE", digest: "DELIVERABLES",
  council: "COUNCIL", verification: "VERIFICATION", feedback: "FEEDBACK",
};

async function main() {
  const container = dv.container;
  container.querySelectorAll(".isds-workflow-3d-host").forEach((el) => el.remove());
  const host = document.createElement("div");
  container.appendChild(host);
  host.className = "isds-workflow-3d-host";
  host.style.cssText = `width:100%;height:${CANVAS.height}px;border-radius:8px;overflow:hidden;position:relative;`;

  const manifest = JSON.parse(await dv.io.load(input.data));

  const nodes = manifest.nodes.map((n) => {
    const x = n.stage * SPACING.stageX;
    const y = (LANE_Y[n.lane] ?? 0) * SPACING.laneY;
    const z = n.depth * SPACING.depthZ;
    return { ...n, x, y, z, fx: x, fy: y, fz: z };
  });
  // Lane captions as pinned pseudo-nodes at the left edge of each populated lane.
  const usedLanes = [...new Set(manifest.nodes.map((n) => n.lane))];
  const minX = Math.min(...nodes.map((n) => n.x));
  for (const lane of usedLanes) {
    const x = minX - SPACING.stageX * 0.9;
    const y = (LANE_Y[lane] ?? 0) * SPACING.laneY;
    nodes.push({ id: `__lane-${lane}`, __laneCaption: lane, x, y, z: 0, fx: x, fy: y, fz: 0 });
  }
  const links = manifest.edges.map((e) => ({ ...e }));

  const graph = ForceGraph3D()(host)
    .width(host.clientWidth || container.clientWidth || 900)
    .height(CANVAS.height)
    .backgroundColor(CANVAS.background)
    .graphData({ nodes, links })
    .enableNodeDrag(false)
    .cooldownTicks(0)
    .nodeThreeObject((node) => {
      if (node.__laneCaption) {
        const cap = new SpriteText(LANE_CAPTION[node.__laneCaption] ?? node.__laneCaption,
                                   TEXT.laneCaptionHeight,
                                   LANE_COLOR[node.__laneCaption] ?? "#8892b0");
        cap.material.depthWrite = false;
        cap.material.depthTest = false;
        cap.material.opacity = 0.5;
        cap.renderOrder = 998;
        return cap;
      }
      const g = new Group();
      const r = NODE_RADIUS[node.kind] ?? 11;
      const color = LANE_COLOR[node.lane] ?? "#cccccc";
      g.add(new Mesh(new SphereGeometry(r, 20, 20),
                     new MeshLambertMaterial({ color, transparent: true, opacity: node.kind === "gate" ? 1 : 0.9 })));
      const label = new SpriteText(node.label, TEXT.nodeLabelHeight, "#e8ecf8");
      label.backgroundColor = "rgba(11,16,32,0.72)";
      label.padding = 3;
      label.borderRadius = 3;
      // Labels always readable: never occluded by geometry, always drawn on top.
      label.material.depthWrite = false;
      label.material.depthTest = false;
      label.renderOrder = 999;
      label.position.set(0, r + TEXT.nodeLabelHeight * 0.9, 0);
      g.add(label);
      return g;
    })
    .linkColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkOpacity(0.5)
    .linkWidth((l) => (l.kind === "core" || l.kind === "gate" ? 2.2 : 1.2))
    .linkDirectionalArrowLength(ARROWS.length)
    .linkDirectionalArrowRelPos(ARROWS.relPos)
    .linkDirectionalArrowColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkCurvature((l) => (l.kind === "feedback" ? 0.3 : 0))
    // The animated flow layer: particles stream along each edge continuously.
    .linkDirectionalParticles((l) => (PARTICLES[l.kind] ?? PARTICLES.core).count)
    .linkDirectionalParticleSpeed((l) => (PARTICLES[l.kind] ?? PARTICLES.core).speed)
    .linkDirectionalParticleWidth((l) => (PARTICLES[l.kind] ?? PARTICLES.core).width)
    .linkDirectionalParticleColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .nodeLabel((n) => n.__laneCaption ? "" :
      `<div style="max-width:360px"><b>${n.label}</b><br/>${n.summary}<br/>` +
      `<i>evidence: ${(n.evidence || []).join(" · ")}</i></div>`)
    .onNodeClick((node) => {
      if (!node.__laneCaption && node.target)
        dv.app.workspace.openLinkText(node.target, dv.current().file.path);
    });

  // Frame the whole pipeline properly once the scene exists, and re-frame on resize.
  const frame = () => graph.zoomToFit(CAMERA.zoomFitMs, CAMERA.zoomFitPadding);
  setTimeout(frame, 60);

  let resizeTimer = null;
  const ro = new ResizeObserver(() => {
    const w = host.clientWidth;
    if (!w) return;
    graph.width(w);
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(frame, 250);
  });
  ro.observe(host);

  const cleanup = () => {
    try { clearTimeout(resizeTimer); ro.disconnect(); } catch {}
    try { graph._destructor && graph._destructor(); } catch {}
    try { host.remove(); } catch {}
  };
  if (dv.component && typeof dv.component.register === "function") {
    dv.component.register(cleanup);
  }
}

main().catch((err) => {
  const el = document.createElement("pre");
  el.textContent = "ISDS 3D workflow view failed: " + (err && err.message || err);
  dv.container.appendChild(el);
});
