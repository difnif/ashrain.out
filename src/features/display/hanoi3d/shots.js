// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 로봇 모드 카메라 샷 (hanoi3d/shots.js) — 순수 계산(three.js 없음)
// 세트 5개(로봇 다섯 대)일 때 카메라를 「샷」으로 고른다 — 사실적인 카메라 길이 아니라 방송처럼 원샷 · 투샷을 바꾼다.
//   전체 null        — 세트 수에 맞춘 기본 카메라(plan.js cameraFor): 대각선 위에서 다섯 대 모두
//   투샷 { n: 2, i } — 이웃한 로봇 i · i + 1(물결 차례 = 화면 왼쪽부터)을 완만한 사선 항공뷰로. 짝마다 둘이 나란히 벌어져 보이는 쪽에서
//   원샷 { n: 1, i } — 로봇 i 가 옮기는 탑을 정면에서(살짝 위 · 망원 쪽 화각). p = 들어오기 전의 투샷(물러날 때 그 투샷으로)
// 샷마다 화각도 다르다(원샷 좁게 · 투샷 넓게). 투샷은 짝마다 둘이 겹치지 않고 나란히 보이는 사선을 찾아서 — 짝마다 왼쪽 · 오른쪽 사선이 갈린다.
// 주인공과 화면에서 겹치는 다른 세트(앞을 가리든 뒤에서 어지럽히든)는 그 샷 동안 무대에서 뺀다(hide) — 샷은 늘 「컷」으로 바뀌므로
//   빠지는 순간이 보이지 않는다. 투샷은 열쇠 빛이 반들한 테이블에 비쳐 눈부신 방위를 피한다.
// 바꾸는 손: 카메라 단추 · C(원샷 1 → 5 → 전체 차례로) · 두 손가락(벌리면 가까이 — 전체 → 투샷 → 원샷, 모으면 멀리, 옆으로 밀면 옆 로봇) · 휠.
import { ROBOT_SETS, ROBOTS, PL, SAFE, layoutSets, fitCam } from "./plan.js";
import { lookCam, project } from "../sim3d/persp.js";

export const ROBOT_NAMES = ["산업용 팔", "로봇 개", "휴머노이드", "두 바퀴", "드론"];
export const NO = ["①", "②", "③", "④", "⑤"];
const LAST = ROBOT_SETS - 1;
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
/** 원샷: 정면에서 살짝 위(테이블 뒤 로봇이 탑 너머로 보이게) · 좁은 화각 / 투샷: 완만한 사선 항공뷰(전체 0.66 보다 낮게) · 넓은 화각 · 사선은 az0 부터 찾는다 */
export const ONE = { fov: 20, el: { arm: 0.32, dog: 0.36, humanoid: 0.2, rover: 0.3, drone: 0.22 } };   // 낮은 로봇일수록 조금 더 위에서(테이블 너머로)
export const TWO = { el: 0.46, fov: 27, az0: 0.45, az1: 1.05 };

/** 샷 다듬기 — 모르는 값은 전체(null) */
export function normShot(s) {
  if (!s || typeof s !== "object" || (s.n !== 1 && s.n !== 2)) return null;
  const max = s.n === 1 ? LAST : LAST - 1;
  const i = Number.isInteger(s.i) ? clamp(s.i, 0, max) : 0;
  return s.n === 1 && Number.isInteger(s.p) && (s.p === i || s.p + 1 === i) ? { n: 1, i, p: s.p } : { n: s.n, i };
}
export const sameShot = (a, b) => { a = normShot(a); b = normShot(b); return !a || !b ? a === b : a.n === b.n && a.i === b.i; };

/** 이름표 — { tag: 왼쪽 위 꼬리표, long: 단추 옆 이름 · 읽어 주기 } */
export function shotLabel(s) {
  s = normShot(s);
  if (!s) return { tag: "전체", long: "전체 — 로봇 다섯 대" };
  if (s.n === 1) return { tag: `원샷 ${NO[s.i]} ${ROBOT_NAMES[s.i]}`, long: `원샷 — ${NO[s.i]} ${ROBOT_NAMES[s.i]} 정면` };
  return { tag: `투샷 ${NO[s.i]}${NO[s.i + 1]}`, long: `투샷 — ${NO[s.i]} ${ROBOT_NAMES[s.i]} · ${NO[s.i + 1]} ${ROBOT_NAMES[s.i + 1]}` };
}

/** 카메라 단추(C): 전체 → 원샷 ① … ⑤ → 전체 (dir −1 이면 거꾸로). 투샷이면 그 짝의 왼쪽(거꾸로면 오른쪽) 원샷 */
export function cycleShot(s, dir = 1) {
  s = normShot(s);
  if (s && s.n === 2) return { n: 1, i: dir > 0 ? s.i : s.i + 1, p: s.i };
  const k = s ? s.i + 1 : 0;                                       // 0 = 전체 · 1 ~ 5 = 원샷
  const m = (k + (dir > 0 ? 1 : -1) + ROBOT_SETS + 1) % (ROBOT_SETS + 1);
  return m === 0 ? null : { n: 1, i: m - 1 };
}

/**
 * 가까이(두 손가락을 벌림 · 휠 위): 전체 → 투샷 → 원샷. dist[i] = 두 손가락 가운데에서 로봇 i 까지 화면 거리(모르면 가운데 로봇).
 *   전체 → 가장 가까운 로봇과 그 옆에서 더 가까운 이웃의 투샷 · 투샷 → 둘 가운데 가까운 쪽 원샷 · 원샷 → 그대로(가장 가깝다)
 */
export function zoomInShot(s, dist = null) {
  s = normShot(s);
  const d = (i) => (dist && Number.isFinite(dist[i]) ? dist[i] : Math.abs(i - 2) * 1e4 + i);
  if (!s) {
    let k = 0;
    for (let i = 1; i < ROBOT_SETS; i++) if (d(i) < d(k)) k = i;
    return { n: 2, i: k === 0 ? 0 : k === LAST ? LAST - 1 : d(k - 1) <= d(k + 1) ? k - 1 : k };
  }
  if (s.n === 2) return { n: 1, i: d(s.i + 1) < d(s.i) ? s.i + 1 : s.i, p: s.i };
  return s;
}
/** 멀리(두 손가락을 모음 · 휠 아래): 원샷 → 투샷(들어온 짝, 없으면 오른쪽 이웃과) → 전체 */
export function zoomOutShot(s) {
  s = normShot(s);
  if (!s || s.n === 2) return null;
  return { n: 2, i: s.p != null ? s.p : Math.min(s.i, LAST - 1) };
}
/** 옆으로(두 손가락을 옆으로 밂 · 가로 휠): 원샷 · 투샷이 한 로봇씩 옆으로(끝에서는 그대로). 전체는 그대로 */
export function swipeShot(s, dir) {
  s = normShot(s);
  if (!s) return null;
  const i = clamp(s.i + (dir > 0 ? 1 : -1), 0, s.n === 1 ? LAST : LAST - 1);
  return i === s.i ? s : { n: s.n, i };
}

/* ══════════ 샷 카메라 ══════════ */
/**
 * 로봇마다 차지하는 곳(세트 좌표, m) — 관절이 닿는 가장 바깥(kin.js 를 한 바퀴 돌려 잰 값) + 모양 여유.
 *   개는 집으러 갈 때 테이블 왼쪽 밖까지 걸어 나가고, 사람 모양은 머리가 가장 높고, 드론은 탑 위를 난다.
 */
export const REACH = {
  arm: { x0: -0.75, x1: 0.75, top: (G) => PL + G.top + 0.08 },
  dog: { x0: -1.55, x1: 1.0, top: (G) => PL + G.top + 0.08 },
  humanoid: { x0: -1.1, x1: 1.1, top: () => 1.92 },
  rover: { x0: -1.1, x1: 1.1, top: (G) => PL + G.top + 0.08 },
  drone: { x0: -0.95, x1: 0.95, top: (G) => PL + G.top + 0.34 },
};
/** 로봇 i 와 그 탑이 차지하는 곳(세계 m) — 테이블 윗부분부터 로봇 꼭대기까지, 테이블 앞 끝부터 로봇 뒤까지 */
export function shotPoints(G, P, i) {
  const p = P[i], R = REACH[ROBOTS[i % ROBOTS.length]];
  const x0 = p.x + Math.min(-G.W / 2 - 0.1, R.x0 - 0.1), x1 = p.x + Math.max(G.W / 2 + 0.1, R.x1 + 0.1);
  const z0 = p.z - G.D / 2 - 0.7, z1 = p.z + G.plinth.d / 2, y0 = PL - 0.22, y1 = R.top(G);
  const pts = [];
  for (const x of [x0, x1]) for (const z of [z0, z1]) for (const y of [y0, y1]) pts.push([x, y, z]);
  return pts;
}
/** 화면 상자 { x0, x1, y0, y1, z(가장 가까운 깊이) } */
function screenBox(L, pts) {
  const b = { x0: Infinity, x1: -Infinity, y0: Infinity, y1: -Infinity, z: Infinity };
  for (const p of pts) {
    const s = project(L, p);
    if (!s) continue;
    b.x0 = Math.min(b.x0, s[0]); b.x1 = Math.max(b.x1, s[0]); b.y0 = Math.min(b.y0, s[1]); b.y1 = Math.max(b.y1, s[1]); b.z = Math.min(b.z, s[2]);
  }
  return b;
}
const unionBox = (a, b) => ({ x0: Math.min(a.x0, b.x0), x1: Math.max(a.x1, b.x1), y0: Math.min(a.y0, b.y0), y1: Math.max(a.y1, b.y1), z: Math.min(a.z, b.z) });
/** 두 화면 상자가 겹친 넓이 / 작은 상자 넓이 */
export function overlap(A, B) {
  const w = Math.min(A.x1, B.x1) - Math.max(A.x0, B.x0), h = Math.min(A.y1, B.y1) - Math.max(A.y0, B.y0);
  if (!(w > 0 && h > 0)) return 0;
  return (w * h) / Math.min((A.x1 - A.x0) * (A.y1 - A.y0), (B.x1 - B.x0) * (B.y1 - B.y0));
}
/** 무대(1600 × 900)에 조금이라도 들어오나 */
const inFrame = (B) => B.x1 > 0 && B.x0 < 1600 && B.y1 > 0 && B.y0 < 900;
/**
 * 이 카메라에서 뺄 세트 — 원샷 · 투샷은 주인공만 또렷하게:
 *   주인공 자리(투샷은 둘을 합친 자리)와 화면에서 겹치는 세트(앞이든 뒤든) · 주인공보다 앞(카메라 쪽)에서 화면에 걸리는 세트
 */
export function crowd(G, P, L, ids) {
  const U = ids.map((i) => screenBox(L, shotPoints(G, P, i))).reduce(unionBox);
  const out = [];
  for (let k = 0; k < P.length; k++) {
    if (ids.includes(k)) continue;
    const K = screenBox(L, shotPoints(G, P, k));
    if (overlap(K, U) > 0.02 || (K.z < U.z && inFrame(K))) out.push(k);
  }
  return out;
}
const camOf = (c) => lookCam({ pos: c.pos, at: c.at, fov: c.fov });
/** 열쇠 빛(engine.js 의 key — 오른쪽 앞 위)이 반들한 테이블에 비쳐 눈부신 방위 — 투샷은 이 둘레를 피한다 */
export const GLARE = { az: Math.atan2(0.42, 0.55), half: 0.27 };
/**
 * 투샷 짝(i, i + 1)의 카메라 — 사선 az0 부터 조금씩 더 돌려 보며(왼쪽 · 오른쪽) 두 로봇이 화면에서 겹치지 않는 가장 완만한 각.
 *   열쇠 빛이 비치는 방위는 되도록 피하고, 비기면 짝마다 왼쪽 · 오른쪽을 번갈아. 끝내 겹치면 가장 덜 겹치는 각
 */
function pairCam(G, P, i) {
  const pts = [...shotPoints(G, P, i), ...shotPoints(G, P, i + 1)];
  let best = null;
  for (let a = TWO.az0; a <= TWO.az1 + 1e-9; a += 0.05) {
    for (const sg of [-1, 1]) {
      const az = sg * a, cam = fitCam(pts, az, TWO.el, TWO.fov, SAFE), L = camOf(cam);
      const ov = overlap(screenBox(L, shotPoints(G, P, i)), screenBox(L, shotPoints(G, P, i + 1)));
      const score = (ov > 0.02 ? 10 + ov * 10 : 0) + (Math.abs(az - GLARE.az) < GLARE.half ? 5 : 0) + a
        + (sg === (i % 2 ? 1 : -1) ? 0 : 0.01);
      if (!best || score < best.score) best = { cam, score };
    }
    if (best && best.score < 5) break;                    // 겹치지 않고 눈부시지 않은 가장 완만한 각
  }
  return best.cam;
}
/** 이 샷의 카메라 — fitCam 결과 + ids(주인공 세트) · hide(그 샷 동안 뺄 세트). 전체면 null. 같은 치수 · 샷이면 기억해 둔 것 */
const CACHE = new Map();
export function shotCam(G, shot) {
  const s = normShot(shot);
  if (!s) return null;
  const key = `${G.n}|${G.pegs}|${G.W.toFixed(4)}|${G.D.toFixed(4)}|${G.top.toFixed(4)}|${s.n}|${s.i}`;
  if (CACHE.has(key)) return CACHE.get(key);
  const P = layoutSets(G, ROBOT_SETS), ids = s.n === 1 ? [s.i] : [s.i, s.i + 1];
  const cam = s.n === 1 ? fitCam(shotPoints(G, P, s.i), 0, ONE.el[ROBOTS[s.i % ROBOTS.length]], ONE.fov, SAFE) : pairCam(G, P, s.i);
  const out = { ...cam, ids, hide: crowd(G, P, camOf(cam), ids) };
  if (CACHE.size > 200) CACHE.clear();
  CACHE.set(key, out);
  return out;
}
