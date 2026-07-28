// Deterministic 3D workflow view for the ISDS Thematic Watcher.
// Runs inside Dataview's dv.view() scope (`dv`/`input` are host-provided).
// Fixed layout — no force drift. Camera framing is COMPUTED (straight-on at the
// content centroid, fov-aware distance) — never zoomToFit along a stale axis.
// Labels are constant SCREEN pixels via a per-frame rescale (like Obsidian's own
// graph), with level-of-detail so the overview shows the majors and zooming in
// reveals every process label. Directional particles animate the flow.
import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";
import { Group, Mesh, SphereGeometry, MeshLambertMaterial, Vector3 } from "three";
import { SPACING, LANE_Y, LABEL_PX, CAMERA, NODE_RADIUS, ARROWS, PARTICLES, CANVAS } from "./render-config.mjs";

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
  const minX = Math.min(...nodes.map((n) => n.x));
  for (const lane of [...new Set(manifest.nodes.map((n) => n.lane))]) {
    const x = minX - SPACING.stageX * 0.75;
    const y = (LANE_Y[lane] ?? 0) * SPACING.laneY;
    nodes.push({ id: `__lane-${lane}`, __laneCaption: lane, x, y, z: 0, fx: x, fy: y, fz: 0 });
  }
  const links = manifest.edges.map((e) => ({ ...e }));

  // Sprite registry for the per-frame constant-screen-size rescale + LOD.
  const labelSprites = [];

  const graph = ForceGraph3D()(host)
    .width(host.clientWidth || container.clientWidth || 900)
    .height(CANVAS.height)
    .backgroundColor(CANVAS.background)
    .graphData({ nodes, links })
    .enableNodeDrag(false)
    .cooldownTicks(0)
    .nodeThreeObject((node) => {
      if (node.__laneCaption) {
        const cap = new SpriteText(LANE_CAPTION[node.__laneCaption] ?? node.__laneCaption, 10,
                                   LANE_COLOR[node.__laneCaption] ?? "#8892b0");
        cap.material.depthWrite = false;
        cap.material.depthTest = false;
        cap.material.opacity = 0.6;
        cap.renderOrder = 998;
        labelSprites.push({ sprite: cap, kindClass: "caption", baseH: 10 });
        return cap;
      }
      const g = new Group();
      const r = NODE_RADIUS[node.kind] ?? 11;
      const color = LANE_COLOR[node.lane] ?? "#cccccc";
      g.add(new Mesh(new SphereGeometry(r, 20, 20),
                     new MeshLambertMaterial({ color, transparent: true, opacity: node.kind === "gate" ? 1 : 0.9 })));
      const label = new SpriteText(node.label, 10, "#e8ecf8");
      label.backgroundColor = "rgba(11,16,32,0.72)";
      label.padding = 3;
      label.borderRadius = 3;
      label.material.depthWrite = false;
      label.material.depthTest = false;
      label.renderOrder = 999;
      label.position.set(0, r + 16, 0);
      g.add(label);
      labelSprites.push({ sprite: label, kindClass: node.kind === "process" ? "detail" : "major", baseH: 10 });
      return g;
    })
    .linkColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkOpacity(0.5)
    .linkWidth((l) => (l.kind === "core" || l.kind === "gate" ? 2.2 : 1.2))
    .linkDirectionalArrowLength(ARROWS.length)
    .linkDirectionalArrowRelPos(ARROWS.relPos)
    .linkDirectionalArrowColor((l) => EDGE_COLOR[l.kind] ?? "#666")
    .linkCurvature((l) => (l.kind === "feedback" ? 0.3 : 0))
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

  // ---- Deterministic straight-on framing (replaces zoomToFit) ----
  const xs = nodes.map((n) => n.x), ys = nodes.map((n) => n.y), zs = nodes.map((n) => n.z);
  const cx = (Math.min(...xs) + Math.max(...xs)) / 2;
  const cy = (Math.min(...ys) + Math.max(...ys)) / 2;
  const maxZ = Math.max(...zs);
  const camera = graph.camera();
  camera.fov = CAMERA.fov;
  camera.updateProjectionMatrix();
  const frame = () => {
    const w = host.clientWidth || 900, h = CANVAS.height;
    const tanHalf = Math.tan((CAMERA.fov * Math.PI) / 360);
    const aspect = w / h;
    const W = (Math.max(...xs) - Math.min(...xs)) / 2 + CAMERA.padWorld;
    const H = (Math.max(...ys) - Math.min(...ys)) / 2 + CAMERA.padWorld;
    const d = Math.max(W / (tanHalf * aspect), H / tanHalf) + maxZ;
    graph.cameraPosition({ x: cx, y: cy, z: d }, { x: cx, y: cy, z: 0 }, 600);
  };
  setTimeout(frame, 60);

  // ---- Constant-screen-size labels + level-of-detail, every frame ----
  const camPos = new Vector3();
  const spritePos = new Vector3();
  let rafId = 0;
  const tick = () => {
    const h = CANVAS.height;
    const tanHalf = Math.tan((camera.fov * Math.PI) / 360);
    camera.getWorldPosition(camPos);
    // Screen px per world unit at the pipeline plane (z=0), for the LOD decision.
    const dPlane = Math.max(1, camPos.z);
    const ppu = h / (2 * dPlane * tanHalf);
    const showDetail = SPACING.stageX * ppu >= LABEL_PX.lodStagePx;
    for (const entry of labelSprites) {
      const { sprite, kindClass } = entry;
      // Capture the sprite's text aspect ratio once (SpriteText encodes it in scale).
      if (entry.aspect === undefined) {
        entry.aspect = sprite.scale.y ? sprite.scale.x / sprite.scale.y : 1;
      }
      sprite.getWorldPosition(spritePos);
      const dist = Math.max(1, camPos.distanceTo(spritePos));
      const targetPx = kindClass === "caption" ? LABEL_PX.caption : LABEL_PX.node;
      const worldH = (targetPx * 2 * dist * tanHalf) / h;
      sprite.scale.set(worldH * entry.aspect, worldH, 1);
      sprite.visible = kindClass !== "detail" || showDetail;
    }
    rafId = requestAnimationFrame(tick);
  };
  rafId = requestAnimationFrame(tick);

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
    try { cancelAnimationFrame(rafId); } catch {}
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
