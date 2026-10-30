// ashrain.out — 교실 모니터 「3D 축구」: WebGL 그리기 (sim3d/engine.js)
// three.js 로 경기장(잔디 줄무늬 · 선 · 골대와 그물 · 광고판 · 관중석 · 지붕 조명 · 하늘)과 사람 모형 · 공을 그린다.
// 이 파일만 three.js 를 쓴다 — 3D 를 켤 때만 불러온다(Stage3D.jsx 가 늦게 들여온다).
// 무엇을 어디에 그릴지는 장면 대본(sim3d/scenes/*)이 정한 세계 한 장면(world)이 모두 가지고 있고, 여기서는 그대로 옮기기만 한다.
//   world = { cam: { pos, at, fov }, dim(0~1 화면 어둡기), actors: [{ id, kit, x, z, yaw, pose, lift, hi }], ball: { p, spin, dir, hi }, net }
// 설명 구간(dim > 0)에는 화면 전체를 어둡게 한 뒤 hi 인 선수 · 공만 다시 그려 밝게 남긴다(다큐 시뮬레이터의 「조명」).
import * as THREE from "three";
import { BODY } from "./rig.js";
import { canvasFov } from "./persp.js";
import { rng } from "../core.js";
import { KITS } from "./kits.js";

/* ══════════ 색 ══════════ */
const SKIN = "#C9BBA8", BOOT = "#22252B";

const ENV = {
  dark: {
    sky: ["#060b1a", "#0f1a3c", "#26365f"], fog: "#1b2850", fogNear: 200, fogFar: 620,
    grass: ["#3a8a39", "#45973f"], surround: "#2f6f31", line: "#F2F6EE",
    wall: "#1d2438", rake: "#1a2034", roof: "#0b0f1d", roofEdge: "#FFF3D4", board: "#0f1834", boardHi: ["#F4C65A", "#6BD3C3", "#8FB9F6"],
    crowd: ["#323c5c", "#3b4668", "#465274", "#55628a", "#6c86b4", "#5d5f72", "#6e5a5e", "#77745f"], seat: "#161c2e", aisle: "#0d1220", head: "rgba(150,140,128,0.55)",
    hemi: ["#a9bcf2", "#22351f", 1.45], key: ["#fff5e3", 2.6, [-40, 70, -55]], fill: ["#c9d8ff", 1.15, [55, 50, 45]],
    dimColor: "#03060f",
  },
  light: {
    sky: ["#7fa7de", "#b7cfee", "#e8eef3"], fog: "#dde6ee", fogNear: 220, fogFar: 680,
    grass: ["#4c9a3e", "#57a848"], surround: "#3f8235", line: "#FBFCF8",
    wall: "#8c96a6", rake: "#7d889a", roof: "#c7ced8", roofEdge: "#fdfbf2", board: "#1c2a52", boardHi: ["#F4C65A", "#6BD3C3", "#ffffff"],
    crowd: ["#6a7695", "#7a86a3", "#8b95b0", "#9aa5c0", "#8fb0de", "#a39c95", "#a8817c", "#b4ac8c"], seat: "#717b92", aisle: "#5d667c", head: "rgba(220,205,185,0.6)",
    hemi: ["#e6efff", "#4d6234", 1.9], key: ["#fff4df", 3.1, [-45, 85, -35]], fill: ["#dbe6ff", 0.9, [50, 40, 50]],
    dimColor: "#03060f",
  },
};

const HALF_L = 52.5, HALF_W = 34;

/* ══════════ 그림 재료 ══════════ */
function canvasTex(w, h, draw, srgb = true) {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  draw(c.getContext("2d"), w, h);
  const t = new THREE.CanvasTexture(c);
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

/** 관중석 — 줄마다 작은 사람 점(색 여럿 · 대비는 낮게) · 빈자리 · 층 사이 통로 띠 */
function crowdTex(E, seed) {
  const R = rng(seed);
  return canvasTex(1024, 512, (g, w, h) => {
    g.fillStyle = E.seat; g.fillRect(0, 0, w, h);
    const rows = 32, rh = h / rows;
    for (let r = 0; r < rows; r++) {
      if (r % 16 === 15) { g.fillStyle = E.aisle; g.fillRect(0, r * rh, w, rh); continue; }     // 통로
      g.fillStyle = "rgba(0,0,0,0.22)"; g.fillRect(0, r * rh + rh * 0.8, w, rh * 0.2);
      for (let x = 1; x < w; x += 3 + (R() < 0.3 ? 1 : 0)) {
        if (R() < 0.1) continue;                                   // 빈자리
        g.fillStyle = E.crowd[Math.floor(R() * E.crowd.length)];
        const hh = rh * (0.5 + R() * 0.16);
        g.fillRect(x, r * rh + rh * 0.8 - hh, 2, hh);
        g.fillStyle = E.head; g.fillRect(x, r * rh + rh * 0.8 - hh - 1.6, 2, 1.6);
      }
    }
  });
}
/** 공 — 흰 바탕에 짙은 오각형 무늬 몇 개 */
function ballTex() {
  return canvasTex(256, 128, (g, w, h) => {
    g.fillStyle = "#f7f7f4"; g.fillRect(0, 0, w, h);
    g.fillStyle = "#1d2230";
    const spots = [[0.1, 0.5], [0.35, 0.22], [0.35, 0.78], [0.6, 0.5], [0.85, 0.22], [0.85, 0.78], [0.5, 0.02], [0.5, 0.98]];
    for (const [u, v] of spots) {
      g.beginPath();
      for (let i = 0; i < 5; i++) { const a = (i / 5) * Math.PI * 2 - Math.PI / 2; g.lineTo(u * w + Math.cos(a) * 14, v * h + Math.sin(a) * 11); }
      g.closePath(); g.fill();
    }
  });
}
/** 그물 — 투명 바탕에 흰 격자 */
function netTex() {
  const t = canvasTex(64, 64, (g, w, h) => {
    g.clearRect(0, 0, w, h);
    g.strokeStyle = "rgba(255,255,255,0.9)"; g.lineWidth = 2;
    g.beginPath(); g.moveTo(0, 1); g.lineTo(w, 1); g.moveTo(1, 0); g.lineTo(1, h); g.stroke();
  });
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}
/** 둥근 그림자 */
function blobTex() {
  return canvasTex(128, 128, (g, w) => {
    const r = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2);
    r.addColorStop(0, "rgba(0,0,0,0.62)"); r.addColorStop(0.55, "rgba(0,0,0,0.32)"); r.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = r; g.fillRect(0, 0, w, w);
  }, false);
}
/** 광고판 — 짙은 바탕에 수학 기호 띠(상표 없음) */
function boardTex(E) {
  const t = canvasTex(1024, 64, (g, w, h) => {
    g.fillStyle = E.board; g.fillRect(0, 0, w, h);
    const words = ["숫자로 읽는 축구", "a² + b² = c²", "거리 ÷ 속력 = 시간", "1 − P(빗나감)", "y = ax + b"];
    g.font = "700 30px 'Pretendard Variable', Pretendard, sans-serif";
    g.textBaseline = "middle";
    let x = 24, i = 0;
    while (x < w) {
      const s = words[i % words.length];
      g.fillStyle = E.boardHi[i % E.boardHi.length];
      g.globalAlpha = 0.82;
      g.fillText(s, x, h / 2 + 1);
      x += g.measureText(s).width + 70; i++;
    }
    g.globalAlpha = 1;
  });
  t.wrapS = THREE.RepeatWrapping;
  return t;
}

/* ══════════ 경기장 ══════════ */
/** 둥근 직사각형(가운데 원점) 둘레를 따라가는 점들: [x, z, 바깥 방향 nx, nz, 둘레 거리] */
function roundRect(hx, hz, r, step = 6) {
  const pts = [];
  const corner = (cx, cz, a0) => { for (let i = 0; i <= 10; i++) { const a = a0 + (i / 10) * (Math.PI / 2); pts.push([cx + r * Math.cos(a), cz + r * Math.sin(a), Math.cos(a), Math.sin(a)]); } };
  const line = (x0, z0, x1, z1, nx, nz) => { const L = Math.hypot(x1 - x0, z1 - z0), n = Math.max(1, Math.round(L / step)); for (let i = 1; i < n; i++) pts.push([x0 + ((x1 - x0) * i) / n, z0 + ((z1 - z0) * i) / n, nx, nz]); };
  corner(hx - r, hz - r, 0); line(hx - r, hz, -hx + r, hz, 0, 1);
  corner(-hx + r, hz - r, Math.PI / 2); line(-hx, hz - r, -hx, -hz + r, -1, 0);
  corner(-hx + r, -hz + r, Math.PI); line(-hx + r, -hz, hx - r, -hz, 0, -1);
  corner(hx - r, -hz + r, (3 * Math.PI) / 2); line(hx, -hz + r, hx, hz - r, 1, 0);
  pts.push(pts[0]);
  let acc = 0;
  for (let i = 0; i < pts.length; i++) { if (i) acc += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); pts[i][4] = acc; }
  return pts;
}
/** 둘레를 따라 단면(바깥 거리 d, 높이 y)을 쓸어 만든 띠 — 관중석 · 지붕 · 광고판 */
function sweep(path, profile, uScale = 6) {
  const pos = [], uv = [], idx = [];
  const P = profile.length;
  for (let i = 0; i < path.length; i++) {
    const [x, z, nx, nz, s] = path[i];
    for (let j = 0; j < P; j++) {
      const [d, y, v] = profile[j];
      pos.push(x + nx * d, y, z + nz * d);
      uv.push(s / uScale, v ?? j / (P - 1));
    }
  }
  for (let i = 0; i < path.length - 1; i++) for (let j = 0; j < P - 1; j++) {
    const a = i * P + j, b = (i + 1) * P + j;
    idx.push(a, b, a + 1, b, b + 1, a + 1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

/** 경기장 선(흰 띠) — 사각 띠 · 호를 한 덩어리로 */
function pitchLines(w = 0.14) {
  const pos = [], idx = [];
  const quad = (a, b, c, d) => { const n = pos.length / 3; pos.push(...a, ...b, ...c, ...d); idx.push(n, n + 2, n + 1, n, n + 3, n + 2); };
  const Y = 0.012;
  const seg = (x0, z0, x1, z1) => {
    const L = Math.hypot(x1 - x0, z1 - z0) || 1, nx = (-(z1 - z0) / L) * (w / 2), nz = ((x1 - x0) / L) * (w / 2);
    quad([x0 + nx, Y, z0 + nz], [x1 + nx, Y, z1 + nz], [x1 - nx, Y, z1 - nz], [x0 - nx, Y, z0 - nz]);
  };
  const arc = (cx, cz, r, a0, a1, n = 48) => {
    for (let i = 0; i < n; i++) {
      const p = a0 + ((a1 - a0) * i) / n, q = a0 + ((a1 - a0) * (i + 1)) / n;
      const ri = r - w / 2, ro = r + w / 2;
      quad([cx + ri * Math.cos(p), Y, cz + ri * Math.sin(p)], [cx + ri * Math.cos(q), Y, cz + ri * Math.sin(q)],
        [cx + ro * Math.cos(q), Y, cz + ro * Math.sin(q)], [cx + ro * Math.cos(p), Y, cz + ro * Math.sin(p)]);
    }
  };
  const L = HALF_L, H = HALF_W;
  seg(-L, -H, L, -H); seg(-L, H, L, H); seg(-L, -H, -L, H); seg(L, -H, L, H); seg(0, -H, 0, H);
  arc(0, 0, 9.15, 0, Math.PI * 2, 72);
  arc(0, 0, 0.18, 0, Math.PI * 2, 12);
  for (const s of [-1, 1]) {
    const gx = s * L;
    // 페널티 박스 16.5 × 40.32 · 골 에어리어 5.5 × 18.32 · 페널티 점 11 m · 페널티 아크
    seg(gx, -20.16, gx - s * 16.5, -20.16); seg(gx, 20.16, gx - s * 16.5, 20.16); seg(gx - s * 16.5, -20.16, gx - s * 16.5, 20.16);
    seg(gx, -9.16, gx - s * 5.5, -9.16); seg(gx, 9.16, gx - s * 5.5, 9.16); seg(gx - s * 5.5, -9.16, gx - s * 5.5, 9.16);
    arc(gx - s * 11, 0, 0.16, 0, Math.PI * 2, 12);
    const a = Math.acos(5.5 / 9.15);
    if (s > 0) arc(gx - 11, 0, 9.15, Math.PI - a, Math.PI + a, 28); else arc(gx + 11, 0, 9.15, -a, a, 28);
    // 코너 아크
    arc(gx, -H, 1, s > 0 ? Math.PI / 2 : 0, s > 0 ? Math.PI : Math.PI / 2, 10);
    arc(gx, H, 1, s > 0 ? Math.PI : (3 * Math.PI) / 2, s > 0 ? (3 * Math.PI) / 2 : 2 * Math.PI, 10);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

function buildStadium(E, R) {
  const root = new THREE.Group();
  const track = (o) => { R.push(o); return o; };
  const lam = (color, extra = {}) => track(new THREE.MeshLambertMaterial({ color, ...extra }));

  // 하늘 — 위에서 아래로 짙은 → 옅은
  {
    const g = new THREE.SphereGeometry(900, 32, 16);
    const col = [], c0 = new THREE.Color(E.sky[0]), c1 = new THREE.Color(E.sky[1]), c2 = new THREE.Color(E.sky[2]);
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const y = p.getY(i) / 900;
      const c = y > 0.25 ? c1.clone().lerp(c0, Math.min(1, (y - 0.25) / 0.6)) : c2.clone().lerp(c1, Math.max(0, (y + 0.05) / 0.3));
      col.push(c.r, c.g, c.b);
    }
    g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
    const m = track(new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false, depthWrite: false }));
    const sky = new THREE.Mesh(track(g), m);
    sky.renderOrder = -10;
    root.add(sky);
  }
  // 바깥 잔디 · 줄무늬 잔디
  {
    const g = track(new THREE.PlaneGeometry(150, 104));
    const m = new THREE.Mesh(g, lam(E.surround));
    m.rotation.x = -Math.PI / 2; m.position.y = -0.01;
    root.add(m);
    const bands = 18, bw = (2 * HALF_L + 6) / bands;
    const mats = [lam(E.grass[0]), lam(E.grass[1])];
    const bg = track(new THREE.PlaneGeometry(bw, 2 * HALF_W + 6));
    for (let i = 0; i < bands; i++) {
      const s = new THREE.Mesh(bg, mats[i % 2]);
      s.rotation.x = -Math.PI / 2; s.position.set(-HALF_L - 3 + bw * (i + 0.5), 0, 0);
      root.add(s);
    }
  }
  // 선
  {
    const m = track(new THREE.MeshBasicMaterial({ color: E.line, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }));
    root.add(new THREE.Mesh(track(pitchLines()), m));
  }
  // 코너 깃발
  {
    const pole = track(new THREE.CylinderGeometry(0.03, 0.03, 1.5, 6)), flag = track(new THREE.PlaneGeometry(0.34, 0.24));
    const pm = lam("#f2f2ee"), fm = track(new THREE.MeshLambertMaterial({ color: "#F4C65A", side: THREE.DoubleSide }));
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
      const g = new THREE.Group();
      const p = new THREE.Mesh(pole, pm); p.position.y = 0.75; g.add(p);
      const f = new THREE.Mesh(flag, fm); f.position.set(0.17, 1.36, 0); g.add(f);
      g.position.set(sx * HALF_L, 0, sz * HALF_W); g.rotation.y = sx * sz > 0 ? 0.6 : -0.6;
      root.add(g);
    }
  }
  // 광고판(터치라인에서 5 m) — 둘레를 따라 낮은 띠
  {
    const path = roundRect(HALF_L + 5, HALF_W + 5, 3, 4);
    const g = track(sweep(path, [[0, 0, 0], [0, 0.95, 1]], 26));
    const tex = track(boardTex(E));
    // 앞면(경기장 쪽)에만 글자, 뒷면은 민무늬
    root.add(new THREE.Mesh(g, track(new THREE.MeshBasicMaterial({ map: tex, side: THREE.FrontSide }))));
    root.add(new THREE.Mesh(g, track(new THREE.MeshLambertMaterial({ color: E.wall, side: THREE.BackSide }))));
  }
  // 관중석 — 앞벽 · 통로 · 비탈(관중) · 뒷벽
  {
    const path = roundRect(HALF_L + 10, HALF_W + 10, 16, 8);
    const wall = sweep(path, [[0, 0], [0, 2.4]]);
    root.add(new THREE.Mesh(track(wall), lam(E.wall, { side: THREE.DoubleSide })));
    const walk = sweep(path, [[0, 2.4], [2.8, 2.4]]);
    root.add(new THREE.Mesh(track(walk), lam(E.wall)));
    const tex = track(crowdTex(E, 7));
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 1.4);
    const rake = sweep(path, [[2.8, 2.4, 0], [32, 23.5, 1]], 155);
    root.add(new THREE.Mesh(track(rake), lam("#ffffff", { map: tex })));
    const back = sweep(path, [[32, 23.5], [32.4, 31]]);
    root.add(new THREE.Mesh(track(back), lam(E.wall, { side: THREE.DoubleSide })));
    // 지붕과 지붕 끝 조명 — 설명 컷처럼 카메라가 지붕보다 높으면 감춘다(내려다보는 그림을 가리지 않게)
    const roofG = new THREE.Group(); roofG.name = "roof";
    const roof = sweep(path, [[6, 29.5], [34, 31.5]]);
    roofG.add(new THREE.Mesh(track(roof), lam(E.roof, { side: THREE.DoubleSide })));
    const glow = sweep(path, [[5.6, 29.1], [6.4, 29.4]]);
    roofG.add(new THREE.Mesh(track(glow), track(new THREE.MeshBasicMaterial({ color: E.roofEdge, side: THREE.DoubleSide, fog: false }))));
    root.add(roofG);
  }
  return root;
}

/* ── 골대 · 그물(뒤 그물은 출렁인다) ── */
function buildGoal(side, R, E) {
  const track = (o) => { R.push(o); return o; };
  const g = new THREE.Group();
  const post = track(new THREE.MeshLambertMaterial({ color: "#f6f7f4", emissive: "#3a3a36" }));
  const W = 7.32, Hh = 2.44, D = 2.0, r = 0.06;
  const cyl = track(new THREE.CylinderGeometry(r, r, Hh, 10));
  for (const z of [-W / 2 - r, W / 2 + r]) { const m = new THREE.Mesh(cyl, post); m.position.set(0, Hh / 2, z); g.add(m); }
  const bar = new THREE.Mesh(track(new THREE.CylinderGeometry(r, r, W + 4 * r, 10)), post);
  bar.rotation.x = Math.PI / 2; bar.position.set(0, Hh, 0); g.add(bar);
  const thin = track(new THREE.MeshLambertMaterial({ color: "#d9dde2" }));
  const bk = track(new THREE.CylinderGeometry(0.03, 0.03, W, 6));
  const back = new THREE.Mesh(bk, thin); back.rotation.x = Math.PI / 2; back.position.set(side * D, 0.04, 0); g.add(back);
  const tex = track(netTex());
  const mk = (rx, ry) => { const t = tex.clone(); t.needsUpdate = true; t.repeat.set(rx, ry); R.push(t); return track(new THREE.MeshBasicMaterial({ map: t, transparent: true, opacity: E === ENV.light ? 0.6 : 0.5, side: THREE.DoubleSide, depthWrite: false, color: "#eef3f8" })); };
  // 뒤 그물(출렁임) — 위가 조금 앞으로 기운다
  const bg = track(new THREE.PlaneGeometry(W, Hh, 28, 10));
  const backNet = new THREE.Mesh(bg, mk(52, 18));
  backNet.rotation.y = side > 0 ? -Math.PI / 2 : Math.PI / 2;
  backNet.position.set(side * D, Hh / 2, 0);
  g.add(backNet);
  const base = Float32Array.from(bg.attributes.position.array);
  // 윗그물 · 옆그물
  const top = new THREE.Mesh(track(new THREE.PlaneGeometry(D, W)), mk(14, 52));
  top.rotation.x = -Math.PI / 2; top.position.set((side * D) / 2, Hh, 0); g.add(top);
  for (const z of [-W / 2, W / 2]) {
    const s = new THREE.Mesh(track(new THREE.PlaneGeometry(D, Hh)), mk(14, 18));
    s.position.set((side * D) / 2, Hh / 2, z); g.add(s);
  }
  g.position.set(side * HALF_L, 0, 0);
  return { group: g, backNet, base, W, Hh, D };
}

/* ══════════ 사람 모형 ══════════ */
/** 회전체: pts = [[반지름, 높이], …] (아래 → 위) */
function lathe(pts, n = 16) {
  const g = new THREE.LatheGeometry(pts.map(([r, y]) => new THREE.Vector2(r, y)), n);
  g.computeVertexNormals();
  return g;
}
const GEO = {};
function geos(R) {
  if (GEO.ready) return GEO;
  const track = (o) => { R.push(o); return o; };
  Object.assign(GEO, {
    // 몸통: 허리 → 가슴 → 어깨가 넓어지는 회전체(앞뒤로 납작하게 눌러 쓴다)
    torso: track(lathe([[0, -0.04], [0.148, -0.03], [0.152, 0.1], [0.172, 0.28], [0.182, 0.4], [0.17, 0.49], [0.13, 0.555], [0.065, 0.6], [0, 0.61]], 18)),
    shorts: track(lathe([[0, -0.1], [0.172, -0.1], [0.178, 0.0], [0.165, 0.1], [0.152, 0.13], [0, 0.13]], 18)),
    neck: track(new THREE.CylinderGeometry(0.05, 0.055, 0.1, 8)),
    head: track(new THREE.SphereGeometry(0.118, 18, 14)),
    hair: track(new THREE.SphereGeometry(0.124, 18, 10, 0, Math.PI * 2, 0, Math.PI * 0.52)),   // 정수리 · 뒤통수 — 얼굴 쪽이 어디인지 보인다
    upper: track(new THREE.CapsuleGeometry(0.056, 0.19, 4, 10)),
    fore: track(new THREE.CapsuleGeometry(0.047, 0.19, 4, 10)),
    hand: track(new THREE.SphereGeometry(0.052, 10, 8)),
    thigh: track(new THREE.CapsuleGeometry(0.08, 0.3, 4, 10)),
    leg: track(new THREE.CylinderGeometry(0.098, 0.112, 0.2, 14)),
    shin: track(new THREE.CapsuleGeometry(0.064, 0.3, 4, 10)),
    boot: track(new THREE.BoxGeometry(0.1, 0.075, 0.25)),
    blob: track(new THREE.PlaneGeometry(1, 1)),
    ready: true,
  });
  return GEO;
}
function kitMats(kit, R) {
  const K = KITS[kit] || KITS.rival;
  const m = (c, rough = 0.62) => { const x = new THREE.MeshStandardMaterial({ color: c, roughness: rough, metalness: 0 }); R.push(x); return x; };
  return { shirt: m(K.shirt, 0.55), shorts: m(K.shorts), socks: m(K.socks), skin: m(K.skin || SKIN, 0.5), boot: m(BOOT, 0.4),
    glove: m(K.gloves ? "#f3f3ef" : (K.skin || SKIN), 0.5), hair: m(K.hair || "#3a3330", 0.7) };
}
function makeFigure(mats, blobMat) {
  const G = GEO;
  const root = new THREE.Group();
  const pivot = new THREE.Group(); pivot.position.y = BODY.hip; root.add(pivot);
  const hips = new THREE.Group(); pivot.add(hips);
  const add = (parent, geo, mat, x, y, z, sx = 1, sy = 1, sz = 1) => { const o = new THREE.Mesh(geo, mat); o.position.set(x, y, z); o.scale.set(sx, sy, sz); parent.add(o); return o; };
  add(hips, G.shorts, mats.shorts, 0, 0.0, 0, 1.12, 1, 0.8);
  const torso = new THREE.Group(); hips.add(torso);
  add(torso, G.torso, mats.shirt, 0, 0.0, 0, 1.16, 1, 0.72);
  add(torso, G.neck, mats.skin, 0, 0.6, 0);
  const head = new THREE.Group(); head.position.y = 0.66; torso.add(head);
  add(head, G.head, mats.skin, 0, 0.075, 0.005);
  const hair = add(head, G.hair, mats.hair, 0, 0.082, -0.012);
  hair.rotation.x = -0.42;
  const limbs = {};
  for (const [side, sx] of [["L", 1], ["R", -1]]) {
    const sh = new THREE.Group(); sh.position.set(sx * BODY.shW, 0.5, 0); torso.add(sh);
    add(sh, G.upper, mats.shirt, 0, -0.14, 0);
    const el = new THREE.Group(); el.position.y = -BODY.upper; sh.add(el);
    add(el, G.fore, mats.skin, 0, -0.13, 0);
    add(el, G.hand, mats.glove, 0, -BODY.fore, 0);
    const hp = new THREE.Group(); hp.position.set(sx * BODY.hipW, 0, 0); hips.add(hp);
    add(hp, G.thigh, mats.skin, 0, -0.22, 0);
    add(hp, G.leg, mats.shorts, 0, -0.08, 0);
    const kn = new THREE.Group(); kn.position.y = -BODY.thigh; hp.add(kn);
    add(kn, G.shin, mats.socks, 0, -0.21, 0);
    add(kn, G.boot, mats.boot, 0, -BODY.shin - 0.02, 0.05);
    limbs[side] = { sh, el, hp, kn };
  }
  const blob = new THREE.Mesh(G.blob, blobMat);
  blob.rotation.x = -Math.PI / 2;
  blob.position.y = 0.02;
  blob.renderOrder = 1;
  return { root, pivot, hips, torso, head, limbs, blob };
}
function poseFigure(F, a) {
  const p = a.pose;
  F.root.position.set(a.x, 0, a.z);
  F.root.rotation.y = a.yaw;
  F.pivot.rotation.set(p.pitch || 0, 0, p.roll || 0);
  F.pivot.position.y = BODY.hip + (p.y || 0);
  F.torso.rotation.x = p.lean || 0;
  F.head.rotation.x = p.neck || 0;
  const L = F.limbs.L, Rr = F.limbs.R;
  L.hp.rotation.x = -(p.hipL || 0); Rr.hp.rotation.x = -(p.hipR || 0);
  L.kn.rotation.x = p.kneeL || 0; Rr.kn.rotation.x = p.kneeR || 0;
  L.sh.rotation.set(-(p.shL || 0), 0, p.abL || 0); Rr.sh.rotation.set(-(p.shR || 0), 0, -(p.abR || 0));
  L.el.rotation.x = -(p.elL || 0); Rr.el.rotation.x = -(p.elR || 0);
  const lift = Math.max(0, (p.y || 0));
  const s = 1.05 - 0.35 * Math.min(1, lift / 1.2);
  F.blob.position.set(a.x, 0.02, a.z);
  F.blob.scale.set(s, s, 1);
  F.blob.material.opacity = 1;
}

/* ══════════ 엔진 ══════════ */
/**
 * createEngine(canvas, theme) → { setTheme, render(world), dispose, info }
 * canvas 는 화면 전체를 덮고, 그 부모(16:9 무대)의 크기에 맞춰 시야각을 정한다(persp.canvasFov).
 */
export function createEngine(canvas, theme = "dark") {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.autoClear = false;
  const maxPR = Math.min(window.devicePixelRatio || 1, 2);
  let pr = Math.min(maxPR, 1.5);
  renderer.setPixelRatio(pr);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 16 / 9, 0.2, 2000);
  const res = [];            // 경기장 재료(테마를 바꾸면 버린다)
  const keep = [];           // 사람 모형 · 공 재료
  let env = null, E = ENV[theme] || ENV.dark, goals = [], roofRef = null;
  geos(keep);

  // 빛
  const hemi = new THREE.HemisphereLight("#fff", "#000", 1);
  const key = new THREE.DirectionalLight("#fff", 2);
  const fill = new THREE.DirectionalLight("#fff", 1);
  for (const l of [hemi, key, fill]) { l.layers.enable(1); scene.add(l); }
  scene.add(key.target); scene.add(fill.target);

  function setTheme(name) {
    E = ENV[name] || ENV.dark;
    if (env) { scene.remove(env); for (const o of res.splice(0)) o.dispose?.(); }
    env = new THREE.Group();
    env.add(buildStadium(E, res));
    roofRef = env.getObjectByName("roof");
    goals = [buildGoal(1, res, E), buildGoal(-1, res, E)];
    for (const g of goals) env.add(g.group);
    scene.add(env);
    scene.fog = new THREE.Fog(E.fog, E.fogNear, E.fogFar);
    hemi.color.set(E.hemi[0]); hemi.groundColor.set(E.hemi[1]); hemi.intensity = E.hemi[2];
    key.color.set(E.key[0]); key.intensity = E.key[1]; key.position.set(...E.key[2]);
    fill.color.set(E.fill[0]); fill.intensity = E.fill[1]; fill.position.set(...E.fill[2]);
    dimMat.color.set(E.dimColor);
  }

  // 화면 어둡기(설명 구간) — 화면 전체를 덮는 판
  const dimScene = new THREE.Scene(), dimCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const dimMat = new THREE.MeshBasicMaterial({ color: "#000", transparent: true, opacity: 0, depthTest: false, depthWrite: false });
  keep.push(dimMat);
  dimScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), dimMat));

  // 사람 모형 · 그림자 · 공
  const blobTexture = blobTex(); keep.push(blobTexture);
  const figs = new Map();
  const kitCache = {};
  const people = new THREE.Group(); scene.add(people);
  function figureFor(a) {
    let F = figs.get(a.id);
    if (F && F.kit !== a.kit) { people.remove(F.root); people.remove(F.blob); figs.delete(a.id); F = null; }
    if (!F) {
      const mats = kitCache[a.kit] || (kitCache[a.kit] = kitMats(a.kit, keep));
      const blobMat = new THREE.MeshBasicMaterial({ map: blobTexture, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
      keep.push(blobMat);
      F = makeFigure(mats, blobMat);
      F.kit = a.kit;
      F.meshes = [];
      F.root.traverse((o) => { if (o.isMesh) F.meshes.push(o); });
      people.add(F.root); people.add(F.blob);
      figs.set(a.id, F);
    }
    return F;
  }
  const ballTexture = ballTex(); keep.push(ballTexture);
  const ballGeo = new THREE.SphereGeometry(0.2, 24, 16); keep.push(ballGeo);
  const ballMat = new THREE.MeshStandardMaterial({ map: ballTexture, roughness: 0.38, metalness: 0, emissive: "#202020" }); keep.push(ballMat);
  const ball = new THREE.Mesh(ballGeo, ballMat);
  scene.add(ball);
  const ballBlobMat = new THREE.MeshBasicMaterial({ map: blobTexture, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 });
  keep.push(ballBlobMat);
  const ballBlob = new THREE.Mesh(GEO.blob, ballBlobMat); ballBlob.rotation.x = -Math.PI / 2; scene.add(ballBlob);
  const axis = new THREE.Vector3();

  setTheme(theme);

  // 크기: 캔버스(화면 전체) · 무대(16:9)
  let size = { cw: 0, ch: 0, fh: 0 };
  function measure() {
    const cw = canvas.clientWidth || 1, ch = canvas.clientHeight || 1;
    const fr = canvas.parentElement?.getBoundingClientRect();
    const fh = fr && fr.height > 0 ? fr.height : ch;
    if (cw !== size.cw || ch !== size.ch || fh !== size.fh) { size = { cw, ch, fh }; renderer.setSize(cw, ch, false); }
  }
  // 크기가 바뀌면(멈춘 동안에도) 마지막 장면을 다시 그린다
  let rq = 0;
  const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => {
    size.cw = -1;
    cancelAnimationFrame(rq);
    rq = requestAnimationFrame(() => { if (lastW) render(lastW); });
  }) : null;
  ro?.observe(canvas); if (canvas.parentElement) ro?.observe(canvas.parentElement);

  // 느린 기기: 그리는 간격이 길면 해상도를 조금 낮춘다
  let lastT = 0, slow = 0, fast = 0;
  function adapt(now) {
    if (lastT) {
      const dt = now - lastT;
      if (dt > 0 && dt < 250) {
        if (dt > 26) { slow++; fast = 0; } else if (dt < 18) { fast++; slow = Math.max(0, slow - 1); }
        if (slow > 90 && pr > 0.6) { pr = Math.max(0.6, pr * 0.82); renderer.setPixelRatio(pr); size.cw = -1; slow = 0; }
        else if (fast > 600 && pr < Math.min(maxPR, 1.5)) { pr = Math.min(maxPR, 1.5, pr * 1.12); renderer.setPixelRatio(pr); size.cw = -1; fast = 0; }
      }
    }
    lastT = now;
  }

  let lost = false;
  const onLost = (e) => { e.preventDefault(); lost = true; };
  const onRestored = () => { lost = false; size.cw = -1; };
  canvas.addEventListener("webglcontextlost", onLost);
  canvas.addEventListener("webglcontextrestored", onRestored);

  let lastW = null;
  function render(W) {
    if (lost || !W) return;
    lastW = W;
    adapt(performance.now());
    measure();
    // 카메라
    const c = W.cam;
    camera.position.set(...c.pos);
    camera.up.set(0, 1, 0);
    camera.lookAt(c.at[0], c.at[1], c.at[2]);
    camera.aspect = size.cw / size.ch;
    camera.fov = canvasFov(c.fov, size.fh, size.ch);
    camera.updateProjectionMatrix();
    if (roofRef) roofRef.visible = c.pos[1] < 27;
    // 선수
    const seen = new Set();
    for (const a of W.actors) {
      const F = figureFor(a);
      seen.add(a.id);
      F.root.visible = F.blob.visible = a.o !== 0;
      poseFigure(F, a);
      const hi = !!a.hi;
      if (F.hi !== hi) { for (const m of F.meshes) { if (hi) m.layers.enable(1); else m.layers.disable(1); } F.hi = hi; }
    }
    // 이 세계에 없는 선수(앞 장면)는 치운다 — 다시 나오면 새로 만든다(모양 · 재료는 함께 쓰니 싸다)
    for (const [id, F] of figs) if (!seen.has(id)) { people.remove(F.root); people.remove(F.blob); F.blob.material.dispose(); figs.delete(id); }
    // 공
    const b = W.ball;
    ball.visible = ballBlob.visible = b && b.o !== 0;
    if (b) {
      ball.position.set(b.p[0], b.p[1], b.p[2]);
      const d = b.dir || [1, 0];
      axis.set(d[1], 0, -d[0]).normalize();
      if (axis.lengthSq() > 0.5) ball.quaternion.setFromAxisAngle(axis, b.spin || 0);
      if (b.hi) ball.layers.enable(1); else ball.layers.disable(1);
      const h = Math.max(0, b.p[1] - 0.2), s = 0.55 / (1 + h * 0.18);
      ballBlob.position.set(b.p[0], 0.021, b.p[2]); ballBlob.scale.set(s, s, 1);
      ballBlobMat.opacity = 1 / (1 + h * 0.25);
    }
    // 그물 출렁임
    for (const [i, g] of goals.entries()) {
      const side = i === 0 ? 1 : -1;
      const n = W.net && W.net.side === side && W.net.k != null && W.net.k >= 0 && W.net.k < 1600 ? W.net : null;
      const pos = g.backNet.geometry.attributes.position;
      if (!n && !g.moved) continue;
      for (let v = 0; v < pos.count; v++) {
        const bx = g.base[v * 3], by = g.base[v * 3 + 1];
        let off = 0;
        if (n) {
          // backNet 의 지역 좌표: x = 골대 폭 방향(회전 때문에 −side·z), y = 높이 − Hh/2
          const zz = side * bx, yy = by + g.Hh / 2;
          const r2 = ((zz - n.z) ** 2) / 4.5 + ((yy - n.y) ** 2) / 1.6;
          const amp = 0.75 * Math.exp(-n.k / 420) * Math.cos(n.k / 95) * Math.max(0, 1 - Math.min(n.k, 150) / 600);
          off = amp * Math.exp(-r2);
        }
        pos.setZ(v, -off);
      }
      pos.needsUpdate = true;
      g.moved = !!n;
    }
    // 그리기: 장면 → (설명이면) 어둡게 → 밝게 남길 것만 다시
    renderer.clear();
    camera.layers.set(0);
    renderer.render(scene, camera);
    const dim = Math.min(1, Math.max(0, W.dim || 0));
    if (dim > 0.002) {
      dimMat.opacity = dim;
      renderer.render(dimScene, dimCam);
      const anyHi = (b && b.hi) || W.actors.some((a) => a.hi);
      if (anyHi && dim < 0.98) {
        camera.layers.set(1);
        renderer.render(scene, camera);
        camera.layers.set(0);
      }
    }
  }

  function dispose() {
    ro?.disconnect();
    cancelAnimationFrame(rq);
    canvas.removeEventListener("webglcontextlost", onLost);
    canvas.removeEventListener("webglcontextrestored", onRestored);
    for (const o of [...res, ...keep]) o.dispose?.();
    res.length = 0;
    GEO.ready = false;
    renderer.dispose();
  }
  return { setTheme, render, dispose, get pixelRatio() { return pr; }, renderer };
}
