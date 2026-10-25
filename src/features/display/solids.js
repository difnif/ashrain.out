// ashrain.out — 교실 모니터: 전개도·입체 자료 (solids.js, 순수 계산)
// 전개도는 바닥 평면(z=0) 위의 다각형들 + 접는 경첩. foldNet(core.js)이 접어 입체를 만든다.
// 꼭짓점 이름은 교과서 관례: 직육면체·정육면체 ABCD-EFGH (윗면 ABCD, A 아래가 E), 삼각기둥 ABC-DEF.
import { foldNet, sub3, cross3, dot3, norm3 } from "./core.js";

const H3 = (3 * Math.sqrt(3)) / 2;   // 한 변 3 인 정삼각형의 높이

export const SOLIDS = {
  cuboid: {
    name: "직육면체", center: [2, 1.5, 1], netCenter: [2, 3, 0],
    faces: [
      { id: "bottom", poly: [[0, 0], [4, 0], [4, 3], [0, 3]], color: "coral" },
      { id: "front", poly: [[0, -2], [4, -2], [4, 0], [0, 0]], parent: "bottom", hinge: [[0, 0], [4, 0]], angle: 90, color: "sky" },
      { id: "back", poly: [[0, 3], [4, 3], [4, 5], [0, 5]], parent: "bottom", hinge: [[0, 3], [4, 3]], angle: 90, color: "leaf" },
      { id: "left", poly: [[-2, 0], [0, 0], [0, 3], [-2, 3]], parent: "bottom", hinge: [[0, 0], [0, 3]], angle: 90, color: "gold" },
      { id: "right", poly: [[4, 0], [6, 0], [6, 3], [4, 3]], parent: "bottom", hinge: [[4, 0], [4, 3]], angle: 90, color: "lilac" },
      { id: "top", poly: [[0, 5], [4, 5], [4, 8], [0, 8]], parent: "back", hinge: [[0, 5], [4, 5]], angle: 90, color: "teal" },
    ],
    V: { A: [0, 0, 2], B: [4, 0, 2], C: [4, 3, 2], D: [0, 3, 2], E: [0, 0, 0], F: [4, 0, 0], G: [4, 3, 0], H: [0, 3, 0] },
    edges: ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"],
  },
  cube: {
    name: "정육면체", center: [1.5, 1.5, 1.5], netCenter: [1.5, 3, 0],
    faces: [
      { id: "bottom", poly: [[0, 0], [3, 0], [3, 3], [0, 3]], color: "coral" },
      { id: "front", poly: [[0, -3], [3, -3], [3, 0], [0, 0]], parent: "bottom", hinge: [[0, 0], [3, 0]], angle: 90, color: "sky" },
      { id: "back", poly: [[0, 3], [3, 3], [3, 6], [0, 6]], parent: "bottom", hinge: [[0, 3], [3, 3]], angle: 90, color: "leaf" },
      { id: "top", poly: [[0, 6], [3, 6], [3, 9], [0, 9]], parent: "back", hinge: [[0, 6], [3, 6]], angle: 90, color: "teal" },
      { id: "right", poly: [[3, 0], [6, 0], [6, 3], [3, 3]], parent: "bottom", hinge: [[3, 0], [3, 3]], angle: 90, color: "lilac" },
      { id: "left", poly: [[-3, 3], [0, 3], [0, 6], [-3, 6]], parent: "back", hinge: [[0, 3], [0, 6]], angle: 90, color: "gold" },
    ],
    V: { A: [0, 0, 3], B: [3, 0, 3], C: [3, 3, 3], D: [0, 3, 3], E: [0, 0, 0], F: [3, 0, 0], G: [3, 3, 0], H: [0, 3, 0] },
    edges: ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"],
    planes: { ABCD: "ABCD", EFGH: "EFGH", ABFE: "ABFE", DCGH: "DCGH", AEHD: "AEHD", BFGC: "BFGC" },
  },
  prism: {
    name: "삼각기둥", center: [2, 1.5, H3 / 2], netCenter: [2, 1.5, 0],
    faces: [
      { id: "bottom", poly: [[0, 0], [4, 0], [4, 3], [0, 3]], color: "coral" },
      { id: "front", poly: [[0, -3], [4, -3], [4, 0], [0, 0]], parent: "bottom", hinge: [[0, 0], [4, 0]], angle: 120, color: "sky" },
      { id: "back", poly: [[0, 3], [4, 3], [4, 6], [0, 6]], parent: "bottom", hinge: [[0, 3], [4, 3]], angle: 120, color: "leaf" },
      { id: "left", poly: [[0, 0], [0, 3], [-H3, 1.5]], parent: "bottom", hinge: [[0, 0], [0, 3]], angle: 90, color: "gold" },
      { id: "right", poly: [[4, 0], [4 + H3, 1.5], [4, 3]], parent: "bottom", hinge: [[4, 0], [4, 3]], angle: 90, color: "lilac" },
    ],
    V: { A: [0, 1.5, H3], B: [0, 0, 0], C: [0, 3, 0], D: [4, 1.5, H3], E: [4, 0, 0], F: [4, 3, 0] },
    edges: ["AB", "BC", "CA", "DE", "EF", "FD", "AD", "BE", "CF"],
  },
};

/** 면마다 경첩 깊이(뿌리 0) */
export function depthOf(solid) {
  const by = Object.fromEntries(solid.faces.map((f) => [f.id, f]));
  const d = (id) => (by[id].parent ? 1 + d(by[id].parent) : 0);
  return Object.fromEntries(solid.faces.map((f) => [f.id, d(f.id)]));
}

/**
 * 펼침 정도 U(0 접힘 ~ 1 펼침) → 면별 3D 꼭짓점.
 * 펼 때는 뚜껑(깊이 2)이 먼저 열리고 옆면이 눕는다. 접을 때는 거꾸로(옆면이 서고 뚜껑이 닫힘).
 */
export function foldAt(solid, U) {
  const dep = depthOf(solid);
  const seg01 = (x, a, b) => (x <= a ? 0 : x >= b ? 1 : (x - a) / (b - a));
  const ease = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
  return foldNet(solid.faces, (f) => {
    const un = dep[f.id] >= 2 ? seg01(U, 0, 0.55) : seg01(U, 0.3, 1);
    return 1 - ease(un);
  });
}

const key3 = (p) => p.map((v) => Math.round(v * 1000) / 1000).join(",");
const ekey = (p, q) => [key3(p), key3(q)].sort().join("|");

/** 입체의 모서리 PQ 가 전개도의 어느 면·어느 변인지 — [{ face, i }] (자른 모서리면 2개, 접은 선이면 2개가 같은 선) */
export function netEdgesOf(solid, P, Q) {
  const pos = foldAt(solid, 0);
  const want = ekey(P, Q), out = [];
  for (const f of solid.faces) {
    const pts = pos[f.id];
    for (let i = 0; i < pts.length; i++) {
      if (ekey(pts[i], pts[(i + 1) % pts.length]) === want) out.push({ face: f.id, i });
    }
  }
  return out;
}
/** 전개도의 경첩(접는 선)인지 */
export function isHinge(solid, P, Q) {
  const hits = netEdgesOf(solid, P, Q);
  if (hits.length < 2) return false;
  const pos = foldAt(solid, 1);           // 펼친 상태에서 두 변이 같은 자리면 경첩
  const a = hits.map((h) => { const pts = pos[h.face]; return ekey(pts[h.i], pts[(h.i + 1) % pts.length]); });
  return a[0] === a[1];
}

/* ── 두 직선의 위치 관계 (모서리를 직선으로 늘려 판단) ── */
export function lineRelation(P1, Q1, P2, Q2) {
  const d1 = sub3(Q1, P1), d2 = sub3(Q2, P2), w = sub3(P2, P1);
  const c = cross3(d1, d2);
  const cl = Math.hypot(...c);
  if (cl < 1e-9) {
    const cw = cross3(d1, w);
    return Math.hypot(...cw) < 1e-9 ? "same" : "parallel";
  }
  return Math.abs(dot3(w, c)) < 1e-9 ? "meet" : "skew";
}
/** 직선과 평면(세 점)의 위치 관계: contain | parallel | meet(+수직 여부) */
export function linePlane(P, Q, A, B, Cp) {
  const n = norm3(cross3(sub3(B, A), sub3(Cp, A)));
  const d = norm3(sub3(Q, P));
  const dn = dot3(d, n);
  if (Math.abs(dn) < 1e-9) return Math.abs(dot3(sub3(P, A), n)) < 1e-9 ? "contain" : "parallel";
  return Math.abs(Math.abs(dn) - 1) < 1e-9 ? "perp" : "meet";
}
