// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 로봇 다섯 대의 몸놀림 (hanoi3d/kin.js)
// three.js 를 쓰지 않는 순수 계산 — 관절 자리(세트 좌표 m, 바닥 y = 0)만 낸다. 모양은 robots.js 가 이 자리에 맞춰 그린다.
// 검산(tests/hanoi3d.test.mjs)이 「나르는 동안 손끝이 판 테두리에서 1.5cm 안」을 모든 로봇 · 기둥 수에서 확인한다.
//   arm      산업용 팔 — 테이블 뒤 레일을 따라 미끄러지며 여섯 축 팔로 집는다
//   dog      네 발 로봇 개 — 등에 단 팔로 집고, 빠르기에 맞춰 종종걸음(대각선 두 발씩)
//   humanoid 사람 모양 로봇 — 두 손으로 판 양쪽을 들고 옆걸음, 아주 빠르면 발바닥 추진기로 떠서 미끄러진다
//   rover    두 바퀴 균형 로봇 — 늘어나는 기둥과 집게 팔, 달릴 때 몸을 기울인다
//   drone    드론 — 세 가닥 줄을 판 윗면 테두리에 걸어 들어 올린다
// 모두 robotPlan(plan.js)의 같은 계획을 따른다 — 다가가 잡기 → 나르기 → 내려놓고 물러나기. 다 옮기고 쉬는 동안은 기뻐한다.
import { HANOI } from "../hanoi.js";
import { gripAt, smooth } from "./plan.js";

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const lerp = (a, b, k) => a + (b - a) * k;
const v3 = (x = 0, y = 0, z = 0) => [x, y, z];
const set3 = (o, x, y, z) => { o[0] = x; o[1] = y; o[2] = z; return o; };
const mixTo = (o, a, b, k) => set3(o, lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k));
export const dist3 = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
/** 쉬는 동안의 기쁨 크기 — 쉬기 시작과 끝에 0 (다음 바퀴의 첫 이동과 이어진다) */
export const cheerEnv = (hold) => { const s = Math.sin(Math.PI * clamp(hold / HANOI.HOLD_MS, 0, 1)); return s * s; };

/**
 * 두 마디 팔·다리: 뿌리 A 에서 목표 T 로. pole 쪽으로 가운데 관절을 굽힌다.
 * out.mid · out.end(닿은 끝) · out.miss(닿지 못한 거리)
 */
export function ik2(A, T, l1, l2, pole, out = { mid: v3(), end: v3(), miss: 0 }) {
  const dx = T[0] - A[0], dy = T[1] - A[1], dz = T[2] - A[2];
  const d = Math.hypot(dx, dy, dz) || 1e-6;
  const ux = dx / d, uy = dy / d, uz = dz / d;
  const dd = clamp(d, Math.abs(l1 - l2) + 1e-4, l1 + l2 - 1e-4);
  const a = (l1 * l1 - l2 * l2 + dd * dd) / (2 * dd);
  const h = Math.sqrt(Math.max(0, l1 * l1 - a * a));
  let px = pole[0], py = pole[1], pz = pole[2];
  const pd = px * ux + py * uy + pz * uz;
  px -= pd * ux; py -= pd * uy; pz -= pd * uz;
  let pl = Math.hypot(px, py, pz);
  if (pl < 1e-6) { px = -uy; py = ux; pz = 0; pl = Math.hypot(px, py) || 1; if (pl < 1e-6) { px = 1; pl = 1; } }
  px /= pl; py /= pl; pz /= pl;
  set3(out.mid, A[0] + ux * a + px * h, A[1] + uy * a + py * h, A[2] + uz * a + pz * h);
  set3(out.end, A[0] + ux * dd, A[1] + uy * dd, A[2] + uz * dd);
  out.miss = d - dd;
  return out;
}

/**
 * 걸음 위상 p(0~1)에서 발 하나: [앞뒤 오프셋, 들림]. 딛는 동안(duty)은 몸이 나아간 만큼 발이 뒤로 — 땅에 붙어 있다.
 * 위상은 「간 거리 ÷ 보폭」으로 돈다(몸이 멈추면 발도 멈추고, 뒤로 가면 거꾸로 돈다).
 */
export function footStep(p, stride, lift, duty = 0.56) {
  if (p < duty) return [stride * duty * (0.5 - p / duty), 0];
  const s = (p - duty) / (1 - duty);
  return [stride * duty * (s - 0.5), lift * Math.sin(Math.PI * s)];
}
const fract = (x) => x - Math.floor(x);

/** 몸의 움직임 기록(빠르기 · 가속 · 걸음 위상) — 시계가 건너뛰면(빠르기 바꿈 · 처음부터) 새로 시작 */
function motion(S, x, dt, stride) {
  if (S.x == null || Math.abs(x - S.x) > 0.6 || !(dt > 0)) { S.x = x; S.v = 0; S.a = 0; S.phi = S.phi || 0; S.walk = 0; return S; }
  const v = (x - S.x) / dt;
  const k = 1 - Math.exp(-dt * 14);
  const vs = lerp(S.v, v, k);
  S.a = lerp(S.a, (vs - S.v) / dt, 1 - Math.exp(-dt * 8));
  S.v = vs;
  S.phi += (x - S.x) / stride;
  S.x = x;
  S.walk = lerp(S.walk, Math.abs(S.v) > 0.03 ? 1 : 0, 1 - Math.exp(-dt * 9));
  return S;
}

/* ══════════ 사람 모양 로봇 ══════════ */
export const HU = { hipW: 0.1, thigh: 0.43, shin: 0.42, ankle: 0.075, pelvisH: 0.93, torso: 0.47, shW: 0.19,
  upper: 0.3, fore: 0.29, hand: 0.065, stride: 0.34, lift: 0.06, zBack: 0.28 };
export function humanoidKin() {
  const S = {};
  const P = { pelvis: v3(), chest: v3(), neck: v3(), head: v3(), lean: 0, headPitch: 0, hover: 0,
    sh: [v3(), v3()], el: [v3(), v3()], wr: [v3(), v3()], hd: [v3(), v3()], miss: [0, 0],
    hip: [v3(), v3()], kn: [v3(), v3()], an: [v3(), v3()], toe: [v3(), v3()], yaw: 0, base: v3() };
  const gA = {}, gB = {}, ik = { mid: v3(), end: v3(), miss: 0 };
  const T = [v3(), v3()], Wt = [v3(), v3()];
  function update(G, plan, yOff, dt, time) {
    gripAt(G, plan, -1, gA); gripAt(G, plan, 1, gB);
    set3(T[0], gA.x, gA.y + yOff, gA.z); set3(T[1], gB.x, gB.y + yOff, gB.z);
    const bx = (gA.x + gB.x) / 2, bz = G.back - HU.zBack;
    motion(S, bx, dt, HU.stride);
    const hoverT = clamp((Math.abs(S.v) - 1.0) / 0.5, 0, 1);
    P.hover = S.hover = lerp(S.hover ?? 0, hoverT, 1 - Math.exp(-dt * 6));
    const env = plan.mode === "hold" ? cheerEnv(plan.hold) : 0;
    // 손목 목표(손바닥은 테두리 바로 뒤)
    for (let i = 0; i < 2; i++) set3(Wt[i], T[i][0], T[i][1] + 0.012, T[i][2] - HU.hand);
    const ty = Math.min(Wt[0][1], Wt[1][1]);
    // 쭈그리기 · 숙이기: 어깨가 손목 목표에서 팔 길이보다 조금 안쪽에 오도록
    const crouch = clamp((0.98 - ty) * 0.62, 0, 0.3);
    const ph = HU.pelvisH - crouch + 0.035 * env * Math.max(0, Math.sin(plan.hold * 0.011)) + P.hover * 0.05;
    // 덜 숙이는 쪽부터: 두 손목 목표 모두 어깨에서 0.5m 안에 들어오는 가장 작은 각(0 ~ 1.05) — 칸으로 찾고 반씩 좁혀 매끄럽게
    const reachOk = (th) => {
      const cz = bz - 0.04 * Math.sin(th) + HU.torso * Math.sin(th), cy = ph + HU.torso * Math.cos(th) - 0.04;
      for (let j = 0; j < 2; j++) {
        const sx = bx + (j === 0 ? -1 : 1) * HU.shW;
        if (Math.hypot(Wt[j][0] - sx, Wt[j][1] - cy, Wt[j][2] - cz) > 0.5) return false;
      }
      return true;
    };
    let best = 1.05;
    if (reachOk(0)) best = 0;
    else {
      for (let i = 1; i <= 42; i++) {
        if (!reachOk(i * 0.025)) continue;
        let lo = (i - 1) * 0.025, hi = i * 0.025;
        for (let j = 0; j < 10; j++) { const m = (lo + hi) / 2; if (reachOk(m)) hi = m; else lo = m; }
        best = hi;
        break;
      }
    }
    S.lean = best;
    const th = S.lean * (1 - env * 0.8);
    P.lean = th;
    set3(P.base, bx, 0, bz);
    set3(P.pelvis, bx, ph, bz - 0.04 * Math.sin(th));
    set3(P.chest, bx, ph + HU.torso * Math.cos(th), P.pelvis[2] + HU.torso * Math.sin(th));
    set3(P.neck, P.chest[0], P.chest[1] + 0.06 * Math.cos(th * 0.7), P.chest[2] + 0.06 * Math.sin(th * 0.7));
    const hp = clamp(th * 0.5 + 0.25, 0, 0.8) * (1 - env);
    P.headPitch = hp;
    set3(P.head, P.neck[0], P.neck[1] + 0.13 * Math.cos(hp), P.neck[2] + 0.13 * Math.sin(hp) * 0.4);
    // 팔
    for (let i = 0; i < 2; i++) {
      const sx = i === 0 ? -1 : 1;
      set3(P.sh[i], bx + sx * HU.shW, P.chest[1] - 0.04, P.chest[2]);
      // 기쁠 때: 두 팔을 V 로
      const cheer = [P.sh[i][0] + sx * 0.3, P.sh[i][1] + 0.44 + 0.04 * Math.sin(time * 9 + i), P.sh[i][2] + 0.1];
      const goal = env > 0 ? mixTo(v3(), Wt[i], cheer, env) : Wt[i];
      ik2(P.sh[i], goal, HU.upper, HU.fore, [sx * 0.7, -0.55, -0.35], ik);
      set3(P.el[i], ...ik.mid); set3(P.wr[i], ...ik.end); P.miss[i] = ik.miss;
      const hd = env > 0 ? [P.wr[i][0], P.wr[i][1] + HU.hand, P.wr[i][2]] : T[i];
      mixTo(P.hd[i], T[i], hd, env);
    }
    // 다리: 옆걸음(거리로 도는 위상). 떠서 미끄러질 때는 두 발을 모으고 조금 든다
    for (let i = 0; i < 2; i++) {
      const sx = i === 0 ? -1 : 1;
      set3(P.hip[i], bx + sx * HU.hipW, ph - 0.06, P.pelvis[2]);
      const [off, lift] = footStep(fract(S.phi + i * 0.5), HU.stride, HU.lift);
      const w = (S.walk || 0) * (1 - P.hover);
      const ax = bx + sx * (HU.hipW + 0.01) + off * w, ay = HU.ankle + lift * w + P.hover * 0.06, az = bz + 0.03;
      ik2(P.hip[i], [ax, ay, az], HU.thigh, HU.shin, [0, 0.15, 1], ik);
      set3(P.kn[i], ...ik.mid); set3(P.an[i], ...ik.end);
      set3(P.toe[i], P.an[i][0], P.an[i][1] - HU.ankle + 0.03, P.an[i][2] + 0.12);
    }
    P.yaw = 0;
    return P;
  }
  return { update, pose: P, kind: "humanoid" };
}

/* ══════════ 네 발 로봇 개 ══════════ */
export const DG = { hipX: 0.31, hipZ: 0.13, thigh: 0.31, shin: 0.33, armX: 0.2, armY: 0.17, up: 0.62, fore: 0.56, tool: 0.13,
  stride: 0.46, lift: 0.08, zBack: 0.36 };
export function dogKin() {
  const S = {};
  const P = { body: v3(), head: v3(), roll: 0, pitch: 0, yaw: 0, sh: v3(), el: v3(), wr: v3(), tip: v3(), open: 1, miss: 0,
    hip: [v3(), v3(), v3(), v3()], kn: [v3(), v3(), v3(), v3()], ft: [v3(), v3(), v3(), v3()] };
  const g = {}, ik = { mid: v3(), end: v3(), miss: 0 }, T = v3(), Wt = v3();
  // 다리 차례: 앞왼 · 앞오 · 뒤왼 · 뒤오 — 대각선(앞왼+뒤오 / 앞오+뒤왼)이 함께
  const LEG = [[1, 1, 0], [1, -1, 0.5], [-1, 1, 0.5], [-1, -1, 0]];
  function update(G, plan, yOff, dt, time) {
    gripAt(G, plan, 0, g);
    set3(T, g.x, g.y + yOff, g.z);
    P.open = g.open; P.gap = G.t / 2;
    const env = plan.mode === "hold" ? cheerEnv(plan.hold) : 0;
    const bx = T[0] - DG.armX, bz = G.back - DG.zBack;
    motion(S, bx, dt, DG.stride);
    const by = clamp(0.46 + (T[1] - 0.7) * 0.18, 0.42, 0.6) + env * 0.03 * Math.sin(time * 12);
    const sway = env * 0.05 * Math.sin(time * 6.5);
    set3(P.body, bx, by, bz + sway);
    P.pitch = clamp(-S.a * 0.004, -0.08, 0.08);
    P.roll = env * 0.1 * Math.sin(time * 6.5);
    set3(P.head, bx + 0.44, by + 0.03, bz + sway);
    set3(P.sh, bx + DG.armX, by + DG.armY, bz + 0.03 + sway);
    set3(Wt, T[0], T[1], T[2] - DG.tool);
    if (env > 0) {
      const wave = [P.sh[0] + 0.18 * Math.sin(time * 7), P.sh[1] + 0.62, P.sh[2] + 0.3];
      mixTo(Wt, Wt, wave, env);
    }
    ik2(P.sh, Wt, DG.up, DG.fore, [0, 1, -0.5], ik);
    set3(P.el, ...ik.mid); set3(P.wr, ...ik.end); P.miss = ik.miss;
    set3(P.tip, P.wr[0], P.wr[1], P.wr[2] + DG.tool);
    for (let i = 0; i < 4; i++) {
      const [fx, fz, ps] = LEG[i];
      set3(P.hip[i], bx + fx * DG.hipX, by - 0.05, bz + fz * DG.hipZ + sway);
      const [off, lift] = footStep(fract(S.phi + ps), DG.stride, DG.lift);
      const w = S.walk || 0;
      const fy = 0.03 + lift * w + (env > 0 && i < 2 ? env * 0.04 * Math.max(0, Math.sin(time * 12 + i * Math.PI)) : 0);
      ik2(P.hip[i], [bx + fx * DG.hipX + off * w, fy, bz + fz * (DG.hipZ + 0.02)], DG.thigh, DG.shin, [-1, 0.25, 0], ik);
      set3(P.kn[i], ...ik.mid); set3(P.ft[i], ...ik.end);
    }
    return P;
  }
  return { update, pose: P, kind: "dog" };
}

/* ══════════ 산업용 팔(레일 위) ══════════ */
export const AR = { railZ: 0.32, shY: 0.6, up: 0.6, fore: 0.55, wrist: 0.09, tool: 0.12 };
export function armKin() {
  const S = {};
  const P = { cx: 0, rz: 0, yaw: 0, sh: v3(), el: v3(), wr: v3(), fl: v3(), tip: v3(), open: 1, miss: 0, spin: 0 };
  const g = {}, ik = { mid: v3(), end: v3(), miss: 0 }, T = v3(), Wc = v3();
  function update(G, plan, yOff, dt, time) {
    gripAt(G, plan, 0, g);
    set3(T, g.x, g.y + yOff, g.z);
    P.open = g.open; P.gap = G.t / 2;
    const env = plan.mode === "hold" ? cheerEnv(plan.hold) : 0;
    const zr = G.back - AR.railZ;
    motion(S, T[0], dt, 1);
    P.cx = T[0]; P.rz = zr;
    set3(P.sh, P.cx, AR.shY, zr);
    if (env > 0) {
      const dance = [P.cx + 0.22 * Math.sin(time * 5.5), yOff + G.top + 0.25 + 0.08 * Math.sin(time * 11), -0.2];
      mixTo(T, T, dance, env);
    }
    set3(Wc, T[0], T[1], T[2] - AR.tool - AR.wrist);
    P.yaw = Math.atan2(Wc[0] - P.sh[0], Wc[2] - P.sh[2]);
    ik2(P.sh, Wc, AR.up, AR.fore, [0, 0.8, -1], ik);
    set3(P.el, ...ik.mid); set3(P.wr, ...ik.end); P.miss = ik.miss;
    set3(P.fl, P.wr[0], P.wr[1], P.wr[2] + AR.wrist);
    set3(P.tip, P.fl[0], P.fl[1], P.fl[2] + AR.tool);
    P.spin = env * Math.sin(time * 8) * 0.8;
    return P;
  }
  return { update, pose: P, kind: "arm" };
}

/* ══════════ 두 바퀴 균형 로봇 ══════════ */
export const RV = { wheelR: 0.16, zBack: 0.36, body: 0.3, mastMin: 0.22, mastMax: 1.5, tip: 0.035 };
export function roverKin() {
  const S = {};
  const P = { axle: v3(), lean: 0, wheel: 0, mb: v3(), mt: v3(), mast: 0, boomEnd: v3(), tip: v3(), open: 1, yaw: 0, miss: 0 };
  const g = {}, T = v3();
  function update(G, plan, yOff, dt, time) {
    gripAt(G, plan, 0, g);
    set3(T, g.x, g.y + yOff, g.z);
    P.open = g.open; P.gap = G.t / 2;
    const env = plan.mode === "hold" ? cheerEnv(plan.hold) : 0;
    const zr = G.back - RV.zBack;
    motion(S, T[0], dt, 1);
    const lean = clamp(-S.a * 0.035, -0.28, 0.28);
    P.lean = S.lean = lerp(S.lean ?? 0, lean, 1 - Math.exp(-dt * 10));
    const sl = Math.sin(P.lean), cl = Math.cos(P.lean);
    const ty = T[1] + env * 0.1 * Math.sin(time * 9);
    const mby = RV.wheelR + RV.body * cl;
    const Lm = clamp((ty - mby) / cl, RV.mastMin, RV.mastMax);
    const bx = T[0] + sl * (RV.body + Lm);
    set3(P.axle, bx, RV.wheelR, zr);
    set3(P.mb, bx - sl * RV.body, mby, zr);
    set3(P.mt, P.mb[0] - sl * Lm, P.mb[1] + cl * Lm, zr);
    P.mast = Lm;
    P.wheel = -bx / RV.wheelR;
    set3(P.tip, T[0], P.mt[1], T[2]);
    set3(P.boomEnd, T[0], P.mt[1], T[2] - RV.tip);
    P.miss = Math.abs(P.mt[1] - T[1]) + Math.abs(P.mt[0] - T[0]);
    P.yaw = env > 0 ? 2 * Math.PI * smooth(plan.hold / HANOI.HOLD_MS) : 0;
    return P;
  }
  return { update, pose: P, kind: "rover" };
}

/* ══════════ 드론 ══════════ */
export const DR = { cable: 0.17, clear: 0.09, body: 0.06 };
export function droneKin() {
  const S = {};
  const P = { body: v3(), pitch: 0, roll: 0, yaw: 0, rotor: 0, ext: 0, hub: [v3(), v3(), v3()], hook: [v3(), v3(), v3()], rim: [v3(), v3(), v3()], flip: 0 };
  const A = [Math.PI / 2, Math.PI / 2 + (2 * Math.PI) / 3, Math.PI / 2 + (4 * Math.PI) / 3];
  const hover = (G, d, yOff) => Math.max(d.y + G.t + DR.cable, G.pegTop + DR.clear) + yOff + DR.body;
  function update(G, plan, yOff, dt, time) {
    const env = plan.mode === "hold" ? cheerEnv(plan.hold) : 0;
    let x, y, ext, ref;
    if (plan.go) {
      const { a: q, A, B } = plan.go, s = smooth(Math.min(1, q / 0.7));
      ref = B;
      x = lerp(A.x, B.x, s);
      y = lerp(hover(G, A, yOff) + 0.05, hover(G, B, yOff), s) + 0.1 * Math.sin(Math.PI * s) * Math.min(1, Math.abs(A.x - B.x) / 0.12);
      ext = smooth((q - 0.66) / 0.34);
      if (q < 0.5) ref = A;
    } else if (plan.mode === "hold") {
      ref = plan.to; x = ref.x; y = hover(G, ref, yOff) + 0.05 + 0.12 * env; ext = 0;
    } else if (plan.phase === 1) {
      ref = plan.disc; x = ref.x; y = hover(G, ref, yOff); ext = 1;
    } else {
      ref = plan.to; const s = smooth(plan.rq);
      x = ref.x; y = hover(G, ref, yOff) + 0.05 * s; ext = 1 - smooth(plan.rq / 0.85);
    }
    motion(S, x, dt, 1);
    set3(P.body, x, y, 0);
    P.ext = ext;
    P.pitch = 0;
    P.roll = clamp(-S.a * 0.012, -0.35, 0.35) + (env > 0 ? 2 * Math.PI * smooth((plan.hold / HANOI.HOLD_MS - 0.3) / 0.4) : 0);
    P.yaw = env * 0.6 * Math.sin(time * 3);
    P.rotor += dt * 95;
    const r = (ref.r ?? G.radii[0]) - 0.006, ry = ref.y + G.t + yOff;
    for (let i = 0; i < 3; i++) {
      set3(P.hub[i], x + 0.05 * Math.cos(A[i]), y - DR.body * 0.6, 0.05 * Math.sin(A[i]));
      set3(P.rim[i], ref.x + r * Math.cos(A[i]), ry, r * Math.sin(A[i]));
      mixTo(P.hook[i], [P.hub[i][0], P.hub[i][1] - 0.03, P.hub[i][2]], P.rim[i], ext);
    }
    return P;
  }
  return { update, pose: P, kind: "drone" };
}

export const KINS = { humanoid: humanoidKin, dog: dogKin, arm: armKin, rover: roverKin, drone: droneKin };
