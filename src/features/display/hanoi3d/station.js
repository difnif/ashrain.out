// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 세트 하나(받침 · 기둥 · 원판) (hanoi3d/station.js)
// 모양(Kit)은 원판 수 · 기둥 수가 같으면 모든 세트가 함께 쓰고, 재질은 세트마다 다르다(materials.js 의 styleMaterials).
// 원판은 둥근 모서리 고리(LatheGeometry) — 가운데 구멍으로 기둥이 지나간다. 기둥은 끝이 둥근 막대.
// 세트의 그룹: root(바닥 높이, 세트 자리) ⊃ plinth(로봇 모드 테이블) · top(받침부터 위 — 로봇 모드면 테이블 위로 올라간다)
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { BT, PL, discPose } from "./plan.js";
import { HANOI } from "../hanoi.js";
import { styleMaterials, labelTexture, radialTexture, glowMaterial } from "./materials.js";

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

/** 둥근 모서리 고리 단면(반지름 r, 높이 y) — 안 아래 → 바깥 아래 → 바깥 위 → 안 위 (반시계) */
function ringProfile(ri, ro, t) {
  const b = Math.min(t * 0.32, (ro - ri) * 0.22, 0.006);
  const pts = [];
  const arc = (cx, cy, a0, a1, m) => {
    for (let i = 0; i <= m; i++) { const a = a0 + ((a1 - a0) * i) / m; pts.push(new THREE.Vector2(cx + b * Math.cos(a), cy + b * Math.sin(a))); }
  };
  arc(ri + b, b, Math.PI, 1.5 * Math.PI, 4);
  arc(ro - b, b, 1.5 * Math.PI, 2 * Math.PI, 4);
  arc(ro - b, t - b, 0, 0.5 * Math.PI, 4);
  arc(ri + b, t - b, 0.5 * Math.PI, Math.PI, 4);
  pts.push(pts[0].clone());
  return { pts, b };
}

/** 같은 (원판 수 · 기둥 수 · 품질)의 모든 세트가 함께 쓰는 모양 */
export class Kit {
  constructor(G, tier) {
    this.G = G; this.tier = tier;
    const k = [240, 360, 520][tier] || 360;
    this.discs = []; this.bands = [];
    for (let d = 0; d < G.n; d++) {
      const ro = G.radii[d], segs = clamp(Math.round(ro * k), 32, 128);
      const { pts, b } = ringProfile(G.holeR, ro, G.t);
      const g = new THREE.LatheGeometry(pts, segs);
      g.computeBoundingSphere();
      this.discs.push(g);
      const bh = Math.max(0.0018, (G.t - 2 * b) * 0.42);
      const bg = new THREE.CylinderGeometry(ro + 0.0007, ro + 0.0007, bh, segs, 1, true);
      bg.translate(0, G.t / 2, 0);
      this.bands.push(bg);
    }
    // 기둥: 받침 윗면에서 끝까지, 끝은 반구
    const H = G.pegTop - BT, r = G.pegR, pp = [new THREE.Vector2(0, 0), new THREE.Vector2(r, 0), new THREE.Vector2(r, H - r)];
    for (let i = 1; i <= 8; i++) { const a = (i / 8) * (Math.PI / 2); pp.push(new THREE.Vector2(r * Math.cos(a), H - r + r * Math.sin(a))); }
    this.peg = new THREE.LatheGeometry(pp, 32);
    this.peg.translate(0, BT, 0);
    this.collar = new THREE.CylinderGeometry(r * 2.1, r * 2.5, 0.007, 36);
    this.collar.translate(0, BT + 0.0035, 0);
    this.board = new RoundedBoxGeometry(G.W, BT, G.D, 3, Math.min(0.014, BT / 2.6));
    this.board.translate(0, BT / 2, 0);
    this.label = new THREE.PlaneGeometry(G.W * 0.995, BT * 0.62);
    this.edge = new THREE.BoxGeometry(G.W * 0.96, 0.0035, 0.0035);
    // 로봇 모드 테이블: 얇은 상판 + 가는 다리 넷 + 앞뒤 띠(뒤의 로봇이 다리 사이로 보이게)
    const P = G.plinth;
    this.tableTop = new RoundedBoxGeometry(P.w, 0.045, P.d, 3, 0.012);
    this.tableTop.translate(0, P.h - 0.0225, 0);
    this.tableLeg = new THREE.CylinderGeometry(0.022, 0.026, P.h - 0.045, 16);
    this.tableLeg.translate(0, (P.h - 0.045) / 2, 0);
    this.tableApron = new THREE.BoxGeometry(P.w - 0.1, 0.05, 0.02);
    this.tableApron.translate(0, P.h - 0.07, 0);
    this.tableFoot = new THREE.CylinderGeometry(0.04, 0.04, 0.012, 20);
    this.tableFoot.translate(0, 0.006, 0);
    this.plinthLed = new THREE.BoxGeometry(P.w * 0.96, 0.006, 0.004);
    this.ring = new THREE.PlaneGeometry(1, 1);
    this.ring.rotateX(-Math.PI / 2);
    this.ringTex = radialTexture([[0, 0], [0.45, 0.05], [0.62, 0.55], [0.72, 0.18], [1, 0]]);
  }
  dispose() {
    for (const g of [...this.discs, ...this.bands, this.peg, this.collar, this.board, this.label, this.edge, this.tableTop, this.tableLeg,
      this.tableApron, this.tableFoot, this.plinthLed, this.ring]) g.dispose();
    this.ringTex.dispose();
  }
}

const TABLE_MAT = {
  dark: () => ({ frame: new THREE.MeshPhysicalMaterial({ color: "#3a404c", metalness: 0.85, roughness: 0.32, clearcoat: 0.4 }),
    top: new THREE.MeshPhysicalMaterial({ color: "#1b1f27", metalness: 0.2, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.06 }) }),
  light: () => ({ frame: new THREE.MeshPhysicalMaterial({ color: "#f3f1ec", metalness: 0.1, roughness: 0.38, clearcoat: 0.5 }),
    top: new THREE.MeshPhysicalMaterial({ color: "#dcd8cf", roughness: 0.3, clearcoat: 0.6, clearcoatRoughness: 0.15 }) }),
};

/** 세트 하나 */
export class Station {
  constructor(kit, style, theme) {
    this.kit = kit; this.G = kit.G; this.style = style;
    const G = this.G, M = (this.mats = styleMaterials(style, G.n, kit.tier));
    this.root = new THREE.Group();
    this.top = new THREE.Group();
    this.root.add(this.top);
    // 받침
    const board = new THREE.Mesh(kit.board, M.board);
    board.castShadow = board.receiveShadow = true;
    this.top.add(board);
    this.labelTex = labelTexture(G, M.ink);
    this.labelMat = new THREE.MeshBasicMaterial({ map: this.labelTex, transparent: true, opacity: M.inkOpacity, depthWrite: false,
      color: style === "neon" ? new THREE.Color(1.8, 1.8, 1.8) : new THREE.Color(1, 1, 1) });
    const label = new THREE.Mesh(kit.label, this.labelMat);
    label.position.set(0, BT / 2, G.D / 2 + 0.0009);
    this.top.add(label);
    if (M.edge) {
      const e = new THREE.Mesh(kit.edge, M.edge);
      e.position.set(0, 0.006, G.D / 2 + 0.0012);
      this.top.add(e);
    }
    // 기둥
    this.pegs = G.X.map((x) => {
      const p = new THREE.Mesh(kit.peg, M.peg);
      p.position.x = x; p.castShadow = p.receiveShadow = true;
      const c = new THREE.Mesh(kit.collar, M.collar);
      c.position.x = x; c.receiveShadow = true;
      this.top.add(p, c);
      return p;
    });
    // 원판
    this.discs = [];
    for (let d = 0; d < G.n; d++) {
      const m = new THREE.Mesh(kit.discs[d], M.discs[d]);
      m.castShadow = m.receiveShadow = true;
      if (M.bands) { const b = new THREE.Mesh(kit.bands[d], M.bands[d]); m.add(b); }
      this.top.add(m);
      this.discs.push(m);
    }
    // 다 옮긴 기둥 아래 빛 고리
    this.ringMat = new THREE.MeshBasicMaterial({ map: kit.ringTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
      color: new THREE.Color("#ffc95a").multiplyScalar(2.2), opacity: 0 });
    this.ringMesh = new THREE.Mesh(kit.ring, this.ringMat);
    this.ringMesh.position.y = BT + 0.0012;
    this.ringMesh.scale.setScalar(G.Rmax * 2.9);
    this.ringMesh.renderOrder = 2;
    this.top.add(this.ringMesh);
    // 로봇 모드 테이블
    this.tableMat = (TABLE_MAT[theme] || TABLE_MAT.dark)();
    this.plinth = new THREE.Group();
    const tt = new THREE.Mesh(kit.tableTop, this.tableMat.top);
    tt.castShadow = tt.receiveShadow = true;
    this.plinth.add(tt);
    const lx = G.plinth.w / 2 - 0.07, lz = G.plinth.d / 2 - 0.06;
    for (const [x, z] of [[-lx, -lz], [lx, -lz], [-lx, lz], [lx, lz]]) {
      const leg = new THREE.Mesh(kit.tableLeg, this.tableMat.frame);
      leg.position.set(x, 0, z); leg.castShadow = true;
      const ft = new THREE.Mesh(kit.tableFoot, this.tableMat.frame);
      ft.position.set(x, 0, z);
      this.plinth.add(leg, ft);
    }
    for (const z of [-lz, lz]) { const ap = new THREE.Mesh(kit.tableApron, this.tableMat.frame); ap.position.z = z; this.plinth.add(ap); }
    this.ledMat = glowMaterial("#5fe6ff", 2.6);
    this.plinthLed = new THREE.Mesh(kit.plinthLed, this.ledMat);
    this.plinthLed.position.set(0, PL - 0.05, G.plinth.d / 2 + 0.0025);
    this.plinth.add(this.plinthLed);
    this.root.add(this.plinth);
    this.lift = -1;
    this.setLift(0);
    this.drop = 0;
    this.pose = {};
  }
  /** 0 = 바닥 · 1 = 테이블 위(로봇 모드) — 그 사이는 테이블이 바닥에서 솟아오른다 */
  setLift(k) {
    if (k === this.lift) return;
    this.lift = k;
    this.top.position.y = PL * k;
    this.plinth.visible = k > 0.001;
    this.plinth.scale.y = Math.max(0.001, k);
  }
  /** 막 만들어졌을 때 원판이 위에서 떨어져 쌓인다(0.9초 — 벽시계로, 그리는 빠르기와 상관없이) */
  dropIn() { this.drop = 1; this.dropT0 = performance.now(); }
  update(st, robot, dt, party) {
    const G = this.G, disc = this.discs;
    if (this.drop > 0) this.drop = Math.max(0, 1 - (performance.now() - this.dropT0) / 900);
    const dk = this.drop;
    for (let d = 0; d < G.n; d++) {
      const m = disc[d];
      let x, y, tilt = 0;
      if (st.moving && d === st.disk) {
        const p = discPose(G, st, robot, this.pose);
        x = p.x; y = p.y; tilt = p.tilt;
      } else {
        const peg = st.pos[d], lv = st.lv[d];
        x = G.X[peg]; y = BT + lv * G.t;
      }
      if (dk > 0) {
        const k = clamp(dk * 1.6 - (G.n - 1 - d) / Math.max(1, G.n) * 0.6, 0, 1);
        y += k * k * 0.35;
      }
      m.position.set(x, y, 0);
      m.rotation.z = tilt;
    }
    // 쉬는 동안 도착 기둥 아래 빛
    const hold = st.hold;
    const glow = hold != null ? Math.min(1, hold / 600) * Math.min(1, (HANOI.HOLD_MS - hold) / 700) : 0;
    this.ringMat.opacity = glow;
    this.ringMesh.visible = glow > 0.003;
    if (glow > 0.003) this.ringMesh.position.x = G.X[st.dst];
    // 네온 띠 · 테이블 빛: 파티면 박자에 맞춰 숨쉰다
    if (this.mats.bands) {
      const k = 1 + party.level * 0.9 * party.beat;
      for (let d = 0; d < G.n; d++) this.mats.bands[d].color.copy(this.mats.bandBase[d]).multiplyScalar(k);
    }
  }
  dispose() {
    const M = this.mats;
    for (const m of [...M.discs, ...(M.bands || []), M.peg, M.collar, M.board, M.edge, this.labelMat, this.ringMat, this.tableMat.frame,
      this.tableMat.top, this.ledMat]) m?.dispose();
    this.labelTex.dispose();
  }
}
