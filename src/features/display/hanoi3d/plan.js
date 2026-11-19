// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 순수 계산 (hanoi3d/plan.js)
// three.js 를 쓰지 않는다 — 엔진(engine.js) · 로봇(kin.js · robots.js) · 검산(tests/hanoi3d.test.mjs)이 함께 쓴다.
//   단위 m. 2D 배치(hanoi.js 의 hanoiLayout, 1600×900 무대 px)를 U 배로 줄여 그대로 쓴다 — 원판 길도 같은 길(pathPoint)이다.
//   세트(받침 하나)의 좌표: x = 기둥이 늘어선 방향(받침 가운데 0) · y = 위(받침 아랫면 0) · z = 앞(카메라 쪽 +).
//   세트 5개는 로봇 모드: 받침이 테이블(높이 PL) 위로 올라가고, 로봇이 테이블 뒤(z −)에서 원판을 나른다.
// 카메라: 세트 1개는 정면에서 살짝 위, 2개 이상은 대각선 위에서 내려다본다. 모든 세트(로봇 포함)가
//   무대(1600×900)의 안전한 칸(조작 막대 · 아래 안내 글자를 피한 곳)에 들어오도록 거리와 보는 곳을 맞춘다.
import { HANOI, pathPoint, moveEase } from "../hanoi.js";
import { lookCam, project } from "../sim3d/persp.js";

export const U = 1 / 800;          // 무대 1px = 1.25mm
export const BT = 0.05;            // 받침 두께
export const PL = 0.78;            // 로봇 모드 테이블 높이
export const KA = 0.3, KC = 0.84;  // 로봇이 옮길 때: 다가가 잡기 [0, KA) · 나르기 [KA, KC) · 내려놓고 물러나기 [KC, 1)
export const KR = KC + 0.3 * (1 - KC);   // 물러나기를 마치면 곧장 다음에 잡을 자리로 미리 간다(다음 이동의 KA 까지 한 길로)
export const ROBOT_SETS = 5;
export const STYLES = ["candy", "metal", "glass", "neon", "wood"];   // 세트마다 원판 재질
export const ROBOTS = ["arm", "dog", "humanoid", "rover", "drone"];  // 로봇 모드: 세트마다 로봇(왼쪽 뒤부터)

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const lerp = (a, b, k) => a + (b - a) * k;
export const smooth = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

/** 세트 하나의 치수 — L = hanoiLayout(n, pegs) */
export function dims(L) {
  const X = L.X.map((x) => (x - 800) * U);
  const radii = L.widths.map((w) => (w / 2) * U);
  const t = L.h * U;
  const W = 2 * L.BOARD.half * U;
  const D = (L.WMAX + 76) * U;
  const pegR = L.PEG_R * U;
  const pegTop = BT + L.pegH * U;                                  // 기둥 끝(둥근 머리 꼭대기)
  const arcTop = BT + (L.yBase - (L.yClear - L.R)) * U;            // 건너는 판 아랫면의 높이
  return {
    L, n: L.n, pegs: L.pegs, X, radii, t, W, D, pegR, holeR: pegR + 0.0035, pegTop, arcTop, top: arcTop + t,
    Rmax: radii[L.n - 1], Rmin: radii[0],
    plinth: { w: W + 0.12, d: D + 0.12, h: PL },
    back: -(D / 2 + 0.06),                                          // 테이블 뒷면(z) — 로봇은 이보다 뒤
  };
}

/** 쉬는 자리의 원판: 기둥 peg, 아래 깔린 판 lv 개 — { x, y(아랫면), r, peg } */
export const restOf = (G, peg, lv, d) => ({ x: G.X[peg], y: BT + lv * G.t, r: G.radii[d], peg });

const TILT = 0.085;
/**
 * 움직이는 판의 자리: { x, y(아랫면), tilt(z축 둘레 기울기), u(길 위의 비율) }.
 * robot 이면 나르는 구간 [KA, KC) 에서만 움직인다(그 앞은 로봇이 다가가 잡고, 뒤는 내려놓고 물러난다).
 * 건너는 동안 살짝 기울인다 — 출발하며 앞으로 숙이고, 멈추며 뒤로(로봇이 들면 덜).
 */
export function discPose(G, st, robot, out = {}) {
  const L = G.L;
  const k = st.k;
  const u = !robot ? moveEase(k) : k < KA ? 0 : k >= KC ? 1 : moveEase(((k - KA) / (KC - KA)) * HANOI.MOTION);
  const p = pathPoint(L, st.from, st.fromLv, st.to, st.toLv, u);
  const x0 = L.X[st.from], x1 = L.X[st.to];
  const w = Math.abs(x1 - x0) > 1e-6 ? clamp((p[0] - x0) / (x1 - x0), 0, 1) : 0;
  out.x = (p[0] - 800) * U;
  out.y = BT + (L.yBase - p[1]) * U;
  out.tilt = -Math.sign(x1 - x0) * TILT * (robot ? 0.35 : 1) * Math.sin(2 * Math.PI * w);
  out.u = u;
  return out;
}

/**
 * 로봇이 쓸 지금의 계획(세트 좌표, 받침 아랫면 기준 높이). st = setAt(...) 결과.
 *   mode "move": phase 0 다가가 잡기 · 1 나르기 · 2 내려놓고 물러나기, q = 그 구간의 진행(0~1)
 *                from(잡을 자리) · to(놓을 자리) · disc(지금 판의 자리)
 *                go = 「앞에 놓은 자리 → 다음에 잡을 자리」로 가는 길 { a(0~1), A(출발 자리), B(잡을 자리) } —
 *                     앞 이동의 물러나기 끝(KR)에서 이번 이동의 KA 까지 한 길이다(빠르기가 바뀌어도 시각으로 이어진다). 없으면 null
 *                rq = 물러나기의 진행(0~1, KC → KR)
 *   mode "hold": 다 옮기고 쉬는 중 — 마지막으로 놓은 자리(가장 작은 판, 도착 기둥 맨 위) 앞에서 기뻐한다. hold = 쉰 ms
 */
export function robotPlan(G, st, out = {}) {
  const n = G.n;
  out.go = null;
  if (st.moving) {
    const k = st.k, tau = st.start + k * st.dur;
    out.mode = "move";
    out.phase = k < KA ? 0 : k < KC ? 1 : 2;
    out.q = out.phase === 0 ? k / KA : out.phase === 1 ? (k - KA) / (KC - KA) : (k - KC) / (1 - KC);
    out.rq = clamp((k - KC) / (KR - KC), 0, 1);
    out.from = restOf(G, st.from, st.fromLv, st.disk);
    out.to = restOf(G, st.to, st.toLv, st.disk);
    const pv = st.prev || { to: st.src, toLv: n - 1, disk: 0, start: null, dur: 0 };
    out.prev = restOf(G, pv.to, pv.toLv, pv.disk);
    if (out.phase === 0) {
      const t0 = pv.start != null ? pv.start + pv.dur * KR : st.start, t1 = st.start + st.dur * KA;
      out.go = { a: t1 > t0 ? clamp((tau - t0) / (t1 - t0), 0, 1) : 1, A: out.prev, B: out.from };
    } else if (out.phase === 2 && k >= KR && st.next) {
      const nx = st.next, t0 = st.start + st.dur * KR, t1 = nx.start + nx.dur * KA;
      out.go = { a: t1 > t0 ? clamp((tau - t0) / (t1 - t0), 0, 1) : 1, A: out.to, B: restOf(G, nx.from, nx.fromLv, nx.disk) };
    }
    out.disc = discPose(G, st, true, out.disc || {});
    out.disc.r = G.radii[st.disk];
    out.disk = st.disk;
    out.hold = 0;
  } else {
    const last = restOf(G, st.dst ?? G.pegs - 1, n - 1, 0);
    out.mode = "hold";
    out.phase = 2; out.q = 1; out.rq = 1;
    out.from = out.to = out.prev = last;
    out.disc = null;
    out.disk = 0;
    out.hold = st.hold ?? 0;
  }
  out.cycle = st.cycle;
  out.dur = st.dur || 0;
  return out;
}

/* ══════════ 손끝 길 ══════════ */
export const RET_Y = 0.025, RET_Z = 0.05;   // 놓은 뒤 물러나는 거리(위 · 뒤)
/** 두 손으로 잡는 각(뒤쪽 가운데에서) — 큰 판은 어깨너비쯤, 작은 판은 거의 한 점 */
export const twoHandAng = (r) => clamp(Math.asin(clamp(0.13 / Math.max(r, 0.01), 0, 1)), 0.3, 1.0);
/**
 * 판의 뒤쪽 테두리를 잡는 손끝 — { x, y, z, open(0 쥠 ~ 1 폄) } (세트 좌표).
 * side: 0 = 뒤쪽 가운데(집게 하나) · −1 / +1 = 두 손의 왼쪽 · 오른쪽(각은 angFn(판 반지름)).
 * 옮겨 갈 때(plan.go)는 모든 판보다 뒤로 빠졌다가 앞으로 와서 잡는다 — 다른 기둥의 큰 판을 뚫고 지나가지 않는다.
 */
export function gripAt(G, plan, side = 0, out = {}, angFn = twoHandAng) {
  const t = G.t;
  const rim = (x, y, r) => {
    const a = side ? side * angFn(r) : 0, rr = Math.max(0.004, r - 0.003);
    return [x + rr * Math.sin(a), y + t / 2, -rr * Math.cos(a)];
  };
  if (plan.go) {
    const { a: q, A, B } = plan.go;
    const a = rim(A.x, A.y, A.r);
    a[1] += RET_Y; a[2] -= RET_Z;
    const b = rim(B.x, B.y, B.r);
    const s = smooth(q), bump = Math.sin(Math.PI * s);
    const back = -(G.Rmax + 0.07) - (side ? 0.02 : 0);
    const z = lerp(a[2], b[2], s);
    const far = Math.min(1, Math.abs(a[0] - b[0]) / 0.12);          // 같은 기둥으로 다시 오면 뒤로 크게 빠질 까닭이 없다
    out.x = lerp(a[0], b[0], s);
    out.y = lerp(a[1], b[1], s) + 0.05 * bump * far;
    out.z = lerp(z, Math.min(z, back), Math.min(1, bump * 1.6) * far);
    out.open = 1 - smooth((q - 0.78) / 0.22);
    return out;
  }
  if (plan.mode === "hold" || plan.phase === 2) {
    const p = rim(plan.to.x, plan.to.y, plan.to.r), s = plan.mode === "hold" ? 1 : smooth(plan.rq);
    out.x = p[0]; out.y = p[1] + RET_Y * s; out.z = p[2] - RET_Z * s;
    out.open = plan.mode === "hold" ? 1 : smooth(plan.rq / 0.5);
    return out;
  }
  const p = rim(plan.disc.x, plan.disc.y, plan.disc.r);       // 나르기
  out.x = p[0]; out.y = p[1]; out.z = p[2]; out.open = 0;
  return out;
}

/* ══════════ 세트 배치 ══════════ */
export const AZ = 0.4;     // 세트 2개부터: 카메라가 오른쪽으로 돈 각(대각선)
/**
 * 세트 S 개의 자리(받침 가운데의 바닥 x · z). 물결(늦게 따라가기) 차례 = 화면 왼쪽부터.
 *   1: 가운데 · 2: 한 줄 · 3: 뒤 2 + 앞 1 · 4: 2줄 × 2 · 5(로봇): 뒤 3 + 앞 2 엇갈리게
 * 세트 2개부터는 줄을 카메라와 수직으로 돌려 놓는다 — 받침은 그대로 앞(+z)을 보니 대각선으로 보이면서도 화면 너비를 꽉 채운다.
 */
export function layoutSets(G, S) {
  const robot = S >= ROBOT_SETS;
  const ca = Math.cos(AZ), sa = Math.sin(AZ);
  const foot = G.W * ca + G.D * sa;                       // 대각선으로 본 받침의 너비(줄 방향)
  const GX = foot + (robot ? 0.95 : 0.42), GZ = robot ? 3.3 : 2.1;
  const P = S === 1 ? [[0, 0]]
    : S === 2 ? [[-GX / 2, 0], [GX / 2, 0]]
    : S === 3 ? [[-GX * 0.56, -GZ * 0.42], [0, GZ * 0.42], [GX * 0.56, -GZ * 0.42]]
    : S === 4 ? [[-GX / 2, GZ / 2], [-GX / 2, -GZ / 2], [GX / 2, -GZ / 2], [GX / 2, GZ / 2]]
    : [[-GX, -GZ / 2], [-GX / 2, GZ / 2], [0, -GZ / 2], [GX / 2, GZ / 2], [GX, -GZ / 2]];
  if (S === 1) return P.map(([x, z]) => ({ x, z }));
  return P.map(([u, v]) => ({ x: u * ca + v * sa, z: -u * sa + v * ca }));
}

/** 장면이 차지하는 바닥 반지름(가운데에서) — 바닥 무늬 · 그림자 · 콘페티 범위 */
export function sceneRadius(G, S) {
  const P = layoutSets(G, S);
  let r = 0;
  for (const p of P) r = Math.max(r, Math.hypot(Math.abs(p.x) + G.W / 2, Math.abs(p.z) + G.D / 2 + (S >= ROBOT_SETS ? 1.1 : 0)));
  return r;
}

/* ══════════ 카메라 ══════════ */
export const SAFE = { x0: 96, x1: 1504, y0: 150, y1: 806 };   // 무대 px — 위 조작 막대 · 아래 안내 글자를 피한 칸

/**
 * 점들(세계 m)이 무대의 안전한 칸에 꼭 맞게 들어오는 카메라.
 *   az: 오른쪽으로 돈 각(0 = 정면) · el: 내려다보는 각 · fov: 무대 세로 시야각(도)
 *   → { pos, at, fov, d(거리), az, el }
 */
export function fitCam(pts, az, el, fov, safe = SAFE) {
  const dir = [Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)];
  let at = [0, 0, 0];
  for (const p of pts) { at[0] += p[0] / pts.length; at[1] += p[1] / pts.length; at[2] += p[2] / pts.length; }
  const camAt = (dd) => lookCam({ pos: [at[0] + dir[0] * dd, at[1] + dir[1] * dd, at[2] + dir[2] * dd], at, fov });
  const box = (cm) => {
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (const p of pts) {
      const s = project(cm, p);
      if (!s) return null;
      if (s[0] < x0) x0 = s[0]; if (s[0] > x1) x1 = s[0];
      if (s[1] < y0) y0 = s[1]; if (s[1] > y1) y1 = s[1];
    }
    return { x0, x1, y0, y1 };
  };
  const fits = (dd) => { const b = box(camAt(dd)); return !!b && b.x0 >= safe.x0 && b.x1 <= safe.x1 && b.y0 >= safe.y0 && b.y1 <= safe.y1; };
  let d = 10, cam = camAt(d);
  for (let it = 0; it < 6; it++) {
    let lo = 0.2, hi = 600;
    for (let j = 0; j < 46; j++) { const m = Math.sqrt(lo * hi); if (fits(m)) hi = m; else lo = m; }
    d = hi; cam = camAt(d);
    const b = box(cam);
    if (!b) break;
    const ex = (b.x0 + b.x1) / 2 - (safe.x0 + safe.x1) / 2, ey = (b.y0 + b.y1) / 2 - (safe.y0 + safe.y1) / 2;
    if (Math.abs(ex) < 0.4 && Math.abs(ey) < 0.4) break;
    const k = d / cam.F;
    at = [0, 1, 2].map((i) => at[i] + cam.r[i] * ex * k - cam.u[i] * ey * k);
  }
  return { pos: cam.pos, at: cam.at, fov, d, az, el };
}

/** 이 세트 수에서 다 보이게 하는 점들(세계 m) */
export function framePoints(G, S) {
  const robot = S >= ROBOT_SETS;
  const P = layoutSets(G, S);
  const pts = [];
  for (const p of P) {
    const x0 = p.x - G.W / 2 - (robot ? 0.25 : 0.03), x1 = p.x + G.W / 2 + (robot ? 0.25 : 0.03);
    const z0 = p.z - G.D / 2 - (robot ? 1.15 : 0.02), z1 = p.z + G.D / 2 + (robot ? 0.08 : 0.04);
    const y1 = robot ? Math.max(PL + G.top + 0.32, 1.86) : G.top + 0.03;
    for (const x of [x0, x1]) for (const z of [z0, z1]) for (const y of [0, y1]) pts.push([x, y, z]);
  }
  return pts;
}

/** 세트 수에 맞는 카메라(흔들림 없는 기준 자리) */
export function cameraFor(G, S) {
  const robot = S >= ROBOT_SETS;
  const az = S === 1 ? 0 : AZ, el = S === 1 ? 0.15 : robot ? 0.66 : 0.52, fov = S === 1 ? 24 : 26;
  return fitCam(framePoints(G, S), az, el, fov);
}
