// ashrain.out — 교실 모니터 「3D 축구」: 장면 대본 도구 (sim3d/script.js)
// 순수 계산 — 3D 장면도 2D 장면처럼 「시각 t(ms) → 그림」 이다. 같은 t 면 같은 세계라서 초등·중등 글자를 겹쳐 그릴 수 있고,
// 어느 순간이든 다시 그릴 수 있다(검산 테스트가 모든 순간을 훑는다).
//   · 박자표(timeline): 화면 시각 t 를 「세계 시각 tw」로 바꾼다. play 구간은 세계가 흐르고(느리게 · 빠르게 · 다시 보기),
//     hold 구간은 세계가 멈춘 채 화면이 어두워지며 큰 글씨 설명이 나온다(다큐 속 시뮬레이터처럼).
//   · 선수(actor): 세계 시각에 따른 자리(열쇠 자리를 매끈하게 잇는다) · 몸 방향 · 자세(달리기 · 차기 · 헤더 …).
//   · 공(ballPath): 머무름 · 날기(포물선) · 굴러가기 · 그물 · 함수.
//   · 카메라(shots): 화면 시각에 따른 눈 · 보는 곳 · 시야각. 앞 컷에서 부드럽게 넘어올 수 있다.
import { clamp, lerp, E } from "../core.js";
import { lookCam, camMix } from "./persp.js";
import { REST, idlePose, readyPose, runPose, kickPose, headerPose, cheerPose, divePose, lungePose, mixPose, STRIDE } from "./rig.js";

export const smooth = (a, b, v) => { const k = clamp((v - a) / (b - a)); return k * k * (3 - 2 * k); };
const wrapPI = (a) => { while (a > Math.PI) a -= 2 * Math.PI; while (a < -Math.PI) a += 2 * Math.PI; return a; };
export const angMix = (a, b, w) => a + wrapPI(b - a) * w;

/* ══════════ 박자표 ══════════ */
// 구간: { name, kind: "play" | "hold", dur(ms), tw: [세계 시작, 세계 끝](play) , speed?: "lin" | "into" | "outof" | "both",
//         dim?(hold 의 어둡기, 기본 0.62), spot?: [밝게 남길 선수 id …, "ball"], hide?: [이 구간에 감출 선수 id …] }
// hold 는 바로 앞 구간이 끝난 세계 시각에 멈춘다(tw 를 주면 그 시각).
const PROFILE = {
  lin: () => 1,
  into: (k) => (k < 0.72 ? 1 : 0.08 + 0.92 * (0.5 + 0.5 * Math.cos((Math.PI * (k - 0.72)) / 0.28))),
  outof: (k) => (k > 0.25 ? 1 : 0.08 + 0.92 * (0.5 - 0.5 * Math.cos((Math.PI * k) / 0.25))),
  both: (k) => Math.min(PROFILE.into(k), PROFILE.outof(k)),
};
function progressTable(speed) {
  const f = typeof speed === "function" ? speed : PROFILE[speed || "lin"];
  const N = 240, acc = [0];
  for (let i = 1; i <= N; i++) acc.push(acc[i - 1] + (f((i - 0.5) / N) || 0));
  const tot = acc[N] || 1;
  return (k) => { const x = clamp(k) * N, i = Math.min(N - 1, Math.floor(x)); return lerp(acc[i], acc[i + 1], x - i) / tot; };
}
export const HOLD_IN = 650, HOLD_OUT = 480, FADE_IN = 900, FADE_OUT = 800;

export function timeline(list) {
  let t = 0, tw = 0;
  const segs = list.map((s, i) => {
    const o = { ...s, i, t0: t, t1: t + s.dur };
    if (s.kind === "play") { o.tw = s.tw; o.prog = progressTable(s.speed); tw = s.tw[1]; }
    else { o.tw = [s.tw ?? tw, s.tw ?? tw]; tw = o.tw[0]; o.dim = s.dim ?? 0.62; }
    t += s.dur;
    return o;
  });
  const a = {}, b = {};
  for (const s of segs) if (s.name) { a[s.name] = s.t0; b[s.name] = s.t1; }
  const dur = t;
  function at(tt) {
    const T = clamp(tt, 0, dur);
    let s = segs[segs.length - 1];
    for (const x of segs) if (T < x.t1) { s = x; break; }
    const local = T - s.t0, k = s.dur ? clamp(local / s.dur) : 1;
    const w = s.kind === "play" ? lerp(s.tw[0], s.tw[1], s.prog(k)) : s.tw[0];
    return { seg: s, k, local, tw: w };
  }
  /** 처음 · 끝에 검게 열고 닫는 정도(0 → 1 = 깜깜) — 글자도 같이 사라지게 */
  const edgeAt = (tt) => Math.max(1 - smooth(0, FADE_IN, tt), smooth(dur - FADE_OUT, dur, tt));
  /** 화면 어둡기: 처음 · 끝은 검게 열고 닫고, hold 구간은 어두워졌다 돌아온다 */
  function dimAt(tt) {
    const { seg, local } = at(tt);
    let d = 0;
    if (seg.kind === "hold") {
      // 설명이 이어지면(hold 다음 hold) 사이에서 밝아지지 않는다
      const prevHold = segs[seg.i - 1]?.kind === "hold", nextHold = segs[seg.i + 1]?.kind === "hold";
      d = seg.dim * Math.min(prevHold ? 1 : smooth(0, HOLD_IN, local), nextHold ? 1 : 1 - smooth(seg.dur - HOLD_OUT, seg.dur, local));
    }
    const edge = Math.max(1 - smooth(0, FADE_IN, tt), smooth(dur - FADE_OUT, dur, tt));
    return Math.max(d, edge);
  }
  /** play 구간 name 안에서 세계 시각 tw 에 닿는 화면 시각(카메라를 세계 사건에 맞춰 바꿀 때) */
  function tAt(name, tw) {
    const s = segs.find((x) => x.name === name);
    if (!s || s.kind !== "play") return s ? s.t0 : 0;
    let lo = 0, hi = 1;
    for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (lerp(s.tw[0], s.tw[1], s.prog(m)) < tw) lo = m; else hi = m; }
    return s.t0 + s.dur * hi;
  }
  return { segs, a, b, dur, at, dimAt, edgeAt, tAt, seg: (name) => segs.find((s) => s.name === name) };
}

/* ══════════ 자리 잇기(단조 3차 — 열쇠 자리를 지나며 넘치지 않는다) ══════════ */
function monotone(ts, vs) {
  const n = ts.length;
  if (n === 1) return { f: () => vs[0], d: () => 0 };
  const h = [], dl = [];
  for (let i = 0; i < n - 1; i++) { h.push(ts[i + 1] - ts[i]); dl.push((vs[i + 1] - vs[i]) / h[i]); }
  const m = new Array(n);
  m[0] = dl[0]; m[n - 1] = dl[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = dl[i - 1] * dl[i] <= 0 ? 0 : (dl[i - 1] + dl[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (dl[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
    const a = m[i] / dl[i], b = m[i + 1] / dl[i], s = a * a + b * b;
    if (s > 9) { const k = 3 / Math.sqrt(s); m[i] = k * a * dl[i]; m[i + 1] = k * b * dl[i]; }
  }
  const find = (t) => { let i = 0; while (i < n - 2 && t > ts[i + 1]) i++; return i; };
  const f = (t) => {
    if (t <= ts[0]) return vs[0];
    if (t >= ts[n - 1]) return vs[n - 1];
    const i = find(t), u = (t - ts[i]) / h[i], u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * vs[i] + (u3 - 2 * u2 + u) * h[i] * m[i] + (-2 * u3 + 3 * u2) * vs[i + 1] + (u3 - u2) * h[i] * m[i + 1];
  };
  const d = (t) => {   // 단위: 값/ms
    if (t <= ts[0] || t >= ts[n - 1]) return 0;
    const i = find(t), u = (t - ts[i]) / h[i], u2 = u * u;
    return ((6 * u2 - 6 * u) * vs[i] + (3 * u2 - 4 * u + 1) * h[i] * m[i] + (-6 * u2 + 6 * u) * vs[i + 1] + (3 * u2 - 2 * u) * h[i] * m[i + 1]) / h[i];
  };
  return { f, d };
}

/**
 * 자리 궤적: keys = [[tw, x, z], …] (세계 시각 ms 차례). 반환 at(tw) → [x, z] · vel(tw) → [m/s, m/s] · dist(tw) → 간 거리(m)
 * 같은 자리를 두 번 이어 쓰면 그동안 서 있다.
 */
export function track(keys) {
  const ts = keys.map((k) => k[0]);
  const X = monotone(ts, keys.map((k) => k[1])), Z = monotone(ts, keys.map((k) => k[2]));
  const at = (tw) => [X.f(tw), Z.f(tw)];
  const vel = (tw) => [X.d(tw) * 1000, Z.d(tw) * 1000];
  // 간 거리 표(20 ms 마다) — 달리기 걸음의 위상에 쓴다. 처음 · 끝에 오래 서 있는 구간(±9만 ms 같은)은 표에 넣지 않는다.
  const moves = (i) => keys[i][1] !== keys[i + 1][1] || keys[i][2] !== keys[i + 1][2];
  let i0 = 0, i1 = keys.length - 2;
  while (i0 < keys.length - 1 && !moves(i0)) i0++;
  while (i1 > i0 && !moves(i1)) i1--;
  const t0 = ts[Math.min(i0, ts.length - 1)], t1 = keys.length > 1 ? ts[Math.min(i1 + 1, ts.length - 1)] : t0, STEP = 20;
  let acc = null;                                       // 처음 쓸 때 만든다(2D 만 보는 화면은 이 계산을 하지 않는다)
  const table = () => {
    acc = [0];
    let prev = at(t0);
    for (let t = t0 + STEP; t <= t1 + STEP; t += STEP) { const p = at(t); acc.push(acc[acc.length - 1] + Math.hypot(p[0] - prev[0], p[1] - prev[1])); prev = p; }
    return acc;
  };
  const dist = (tw) => {
    if (tw <= t0) return 0;
    const A = acc || table();
    if (A.length < 2) return 0;
    const x = (tw - t0) / STEP, i = Math.min(A.length - 2, Math.floor(x));
    return lerp(A[i], A[i + 1], clamp(x - i));
  };
  return { at, vel, dist, t0, t1 };
}

/* ══════════ 선수 ══════════ */
// spec: { id, kit, n, name, role: "main" | "mate" | "rival" | "keeper", keys, look?: (tw, ctx) => [x, z] | [x, z],
//         acts?: [{ kind: "kick" | "pass" | "head" | "dive" | "cheer" | "lunge", at | from/to, foot?, power?, dir?, h? }],
//         stance?: "idle" | "ready", seed?, label?: false }
const ACT = {
  kick: { pre: 380, post: 420 }, pass: { pre: 300, post: 340 }, head: { pre: 420, post: 460 },
  dive: { pre: 180, post: 900 }, lunge: { pre: 200, post: 700 },
};
export function actor(spec) {
  const tr = track(spec.keys);
  const seed = spec.seed ?? (spec.n || 0) * 0.37 + (spec.id.length % 7);
  const acts = (spec.acts || []).map((a) => ({ ...a, ...(ACT[a.kind] || {}) }));
  function state(tw, ctx = {}) {
    const [x, z] = tr.at(tw);
    const [vx, vz] = tr.vel(tw);
    const v = Math.hypot(vx, vz);
    // 몸 방향: 움직이면 가는 쪽, 서 있으면 볼 곳(기본은 공)
    const lookAt = typeof spec.look === "function" ? spec.look(tw, ctx) : spec.look || (ctx.ball ? [ctx.ball[0], ctx.ball[2]] : null);
    const faceLook = lookAt ? Math.atan2(lookAt[0] - x, lookAt[1] - z) : spec.yaw ?? 0;
    const faceMove = v > 0.05 ? Math.atan2(vx, vz) : faceLook;
    let yaw = angMix(faceLook, faceMove, smooth(0.6, 2.2, v));
    // 자세: 서 있기 ↔ 달리기
    const still = spec.stance === "ready" ? readyPose(tw, seed, spec.deep ?? 0.6) : idlePose(tw, seed);
    let pose = v < 0.35 ? still : mixPose(still, runPose((2 * Math.PI * tr.dist(tw)) / STRIDE + seed, clamp((v - 0.8) / 6.4, 0, 1)), smooth(0.35, 1.4, v));
    let y = 0;
    for (const a of acts) {
      if (a.kind === "cheer") {
        const w = Math.min(smooth(a.from, a.from + 260, tw), 1 - smooth(a.to - 260, a.to, tw));
        if (w > 0) pose = mixPose(pose, { ...cheerPose(tw, 1), hipL: pose.hipL, hipR: pose.hipR, kneeL: pose.kneeL, kneeR: pose.kneeR, y: pose.y }, w);
        continue;
      }
      if (a.kind === "face") { const w = Math.min(smooth(a.from, a.from + 300, tw), 1 - smooth(a.to - 300, a.to, tw)); if (w > 0) yaw = angMix(yaw, Math.atan2(a.p[0] - x, a.p[1] - z), w); continue; }
      const lo = a.at - a.pre, hi = a.at + a.post;
      if (tw < lo - 120 || tw > hi + 160) continue;
      const w = Math.min(smooth(lo - 120, lo, tw), 1 - smooth(hi, hi + 160, tw));
      let p;
      if (a.kind === "kick" || a.kind === "pass") {
        const k = tw < a.at ? (tw - a.at) / a.pre : (tw - a.at) / a.post;
        p = kickPose(clamp(k, -1, 1), a.power ?? (a.kind === "pass" ? 0.55 : 1), a.foot || "R");
      } else if (a.kind === "head") {
        p = headerPose(clamp(0.5 + (tw - a.at) / (2 * (tw < a.at ? a.pre : a.post))), a.h ?? 0.65);
      } else if (a.kind === "dive") {
        p = divePose(clamp((tw - lo) / (a.pre + a.post)), a.dir ?? 1, a.h ?? 0.5);
      } else if (a.kind === "lunge") {
        p = lungePose(clamp((tw - lo) / (a.pre + 300)), a.dir ?? 1);
      }
      if (p) pose = mixPose(pose, p, w);
      if (a.kind === "head") y = Math.max(y, w * (p.y || 0));
    }
    return { id: spec.id, kit: spec.kit, x, z, yaw, pose, v, lift: y, n: spec.n, name: spec.name, role: spec.role || "main", label: spec.label !== false };
  }
  return { ...spec, tr, state };
}

/* ══════════ 공 ══════════ */
// parts: [{ t0, t1, kind: "air" | "ground" | "fn", a, b, h?, ease?, f? }] — 구간 밖에서는 가까운 구간의 끝자리에 머문다.
//   air: a·b = [x, y, z], h = 직선보다 더 솟는 높이(m) · 시간에 따라 고르게(살짝 느려지게 ease: "drag")
//   ground: a·b = [x, z] 굴러감(ease: "lin" | "slow")  ·  fn: f(tw) → [x, y, z]
export const BALL_R = 0.2;
export function ballPath(parts) {
  const P = [...parts].sort((p, q) => p.t0 - q.t0);
  const endOf = (p) => (p.kind === "fn" ? p.f(p.t1) : p.kind === "ground" ? [p.b[0], BALL_R, p.b[1]] : p.b);
  const startOf = (p) => (p.kind === "fn" ? p.f(p.t0) : p.kind === "ground" ? [p.a[0], BALL_R, p.a[1]] : p.a);
  function at(tw) {
    if (tw <= P[0].t0) return startOf(P[0]);
    for (let i = 0; i < P.length; i++) {
      const p = P[i];
      if (tw < p.t0) return endOf(P[i - 1]);
      if (tw <= p.t1) {
        const k = (tw - p.t0) / (p.t1 - p.t0 || 1);
        if (p.kind === "fn") return p.f(tw);
        if (p.kind === "ground") {
          const u = p.ease === "slow" ? 1 - (1 - k) * (1 - k) : k;
          return [lerp(p.a[0], p.b[0], u), BALL_R, lerp(p.a[1], p.b[1], u)];
        }
        const u = p.ease === "drag" ? k * (1.18 - 0.18 * k) : p.ease === "net" ? E.out(k) : p.ease === "fall" ? k * k : k;
        // bend: 공이 휘어 가는 정도(m) — 날아가는 방향의 왼쪽(+) · 오른쪽(−)으로 가운데가 불룩
        let bx = 0, bz = 0;
        if (p.bend) { const dx = p.b[0] - p.a[0], dz = p.b[2] - p.a[2], L = Math.hypot(dx, dz) || 1, c = p.bend * 4 * u * (1 - u); bx = (dz / L) * c; bz = (-dx / L) * c; }
        return [lerp(p.a[0], p.b[0], u) + bx, lerp(p.a[1], p.b[1], u) + (p.h || 0) * 4 * u * (1 - u), lerp(p.a[2], p.b[2], u) + bz];
      }
    }
    return endOf(P[P.length - 1]);
  }
  // 구른 거리(회전) 표 — 끝없이 머무는 마지막 구간은 30초까지만
  const t0 = P[0].t0, t1 = Math.min(P[P.length - 1].t1, t0 + 30000), STEP = 20;
  let acc = null;
  const table = () => {
    acc = [0];
    let prev = at(t0);
    for (let t = t0 + STEP; t <= t1 + STEP; t += STEP) { const p = at(t); acc.push(acc[acc.length - 1] + Math.hypot(p[0] - prev[0], p[1] - prev[1], p[2] - prev[2])); prev = p; }
    return acc;
  };
  const spin = (tw) => {
    if (tw <= t0) return 0;
    const A = acc || table();
    const x = (tw - t0) / STEP, i = Math.min(A.length - 2, Math.floor(x));
    return lerp(A[i], A[i + 1], clamp(x - i)) / BALL_R;
  };
  /** 지난 ms 동안의 자취(세계 점들) */
  const trail = (tw, ms = 600, n = 18) => {
    const out = [];
    for (let i = n; i >= 0; i--) out.push(at(tw - (ms * i) / n));
    return out;
  };
  return { at, spin, trail, parts: P };
}

/* ══════════ 카메라 컷 ══════════ */
// list: [{ t0, t1, cam: (k, t) => ({ pos, at, fov }), blend?(ms — 앞 컷에서 부드럽게 옮겨 옴), ease? }]
export function shots(list) {
  const L = [...list].sort((a, b) => a.t0 - b.t0);
  const one = (s, t) => s.cam(clamp((t - s.t0) / (s.t1 - s.t0 || 1)), t);
  return (t) => {
    let i = 0;
    while (i < L.length - 1 && t >= L[i + 1].t0) i++;
    const s = L[i];
    const c = one(s, t);
    if (i > 0 && s.blend && t < s.t0 + s.blend) {
      const k = (s.ease || E.io)(clamp((t - s.t0) / s.blend));
      return camMix(one(L[i - 1], t), c, k);
    }
    return c;
  };
}

/* ══════════ 세계 한 장면 ══════════ */
/**
 * sim = makeWorld({ tl, actors, ball, cam, spot?, net?, extra? })
 * world(t) → { t, tw, seg, k, local, cam(lookCam), dim, actors: [state + hi], ball: { p, spin, hi, o }, net }
 *   spot: hold 구간에서 밝게 남길 것 — 구간의 spot 을 기본으로 쓴다.
 *   net: (tw) → { side: ±1, y, z, k(골망이 출렁인 뒤 지난 ms) } | null
 */
export function makeWorld({ tl, actors, ball, cam, net, extra }) {
  return function world(t) {
    const { seg, k, local, tw } = tl.at(t);
    const bp = ball.at(tw), bq = ball.at(tw - 40);
    const ctx = { ball: bp, tw };
    const dx = bp[0] - bq[0], dz = bp[2] - bq[2], dl = Math.hypot(dx, dz);
    const spot = new Set(seg.kind === "hold" ? seg.spot || [] : []);
    const hide = seg.hide || [];
    const list = actors.map((a) => { const s = a.state(tw, ctx); s.hi = spot.has(a.id); if (hide.includes(a.id)) s.o = 0; return s; });
    return {
      t, tw, seg, k, local,
      cam: lookCam(cam(t, tw)),
      dim: tl.dimAt(t),
      edge: tl.edgeAt(t),
      actors: list,
      ball: { p: bp, spin: ball.spin(tw), dir: dl > 1e-4 ? [dx / dl, dz / dl] : [1, 0], hi: spot.has("ball"), o: 1 },
      net: net ? net(tw) : null,
      ...(extra ? extra(t, tw) : {}),
    };
  };
}

export { REST, lookCam };
