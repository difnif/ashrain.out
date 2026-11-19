// ashrain.out — 교실 모니터 「액자」: 하노이의 탑 — 계산부 (hanoi.js)
// 위치: src/features/display/hanoi.js — JSX · three.js 없음. 2D 그리기(frames/hanoi.jsx) · 3D 무대(hanoi3d/) · 검산(tests/hanoi.test.mjs)이 함께 쓴다.
//
// 규칙  원판 n개(3 ~ 30)를 첫 기둥에서 마지막 기둥으로. 한 번에 맨 위 원판 하나만, 큰 원판은 작은 원판 위에 못 놓는다.
//       기둥 3개: 최소 2ⁿ − 1번(30개면 1,073,741,823번).
//       기둥 4 · 5개: 프레임–스튜어트(Frame–Stewart) 방법 — 위의 작은 판 q개를 빈 기둥 하나에 비켜 두고, 남은 큰 판을
//       기둥 하나 적은 판에서 옮긴 뒤, 비켜 둔 q개를 다시 얹는다. q 는 횟수가 가장 적게 고른다(4개 기둥에서 최소임이 증명됨).
//       30개면 기둥 4개 1,025번 · 기둥 5개 271번.
// 시간  1 ~ 4배속: 한 번 옮기는 데 1초 ÷ 배수(1배속 = 1초에 1개 → 기둥 3개 원판 n개는 (2ⁿ − 1)초).
//       자연스럽게: 한 번 옮기는 시간이 원판이 실제로 지나가는 길(들어 올림 + 건너감 + 내려놓음)의 길이에 비례한다.
//                   같은 원판이라도 깔린 판 수에 따라 길이가 달라서, 다 옮기는 시간은 재귀로 센다
//                   (「옮길 판 수 · 출발 · 도착 · 쓸 수 있는 기둥 · 기둥마다 깔린 큰 판 수」를 열쇠로 기억 — 2³⁰번이어도 금방).
//       어느 순간이든 재귀를 한 번 내려가며(원판 수만큼) 몇 번째 이동인지 · 모든 판의 자리를 바로 낸다 — 미리 다 펼치지 않는다.
// 반복  다 옮기면 HOLD 동안 쉬고 반대로(마지막 기둥 → 첫 기둥) 옮긴다 — 끝없이 돈다.
// 세트  세트가 여럿이면 같은 탑을 조금씩 늦게(세트마다 STAGGER) 따라 옮겨 물결처럼 보인다.
// 무대  1600×900, 화면 y 는 아래로 +. 원판 위치는 「아랫면 가운데」 좌표로 센다(3D 는 1px = 1cm 로 옮겨 쓴다).

export const HANOI = {
  MIN: 3, MAX: 30, DEF: 14,   // 처음 값: 원판 14개(1배속이면 4시간 33분 3초 — 3시간 넘게 걸리는 가장 작은 수)
  PEGS: [3, 4, 5], SETS: [1, 2, 3, 4, 5],
  SPEEDS: ["natural", "x1", "x2", "x3", "x4"],
  FAST_MS: 1000,   // 1배속: 1초에 1개
  NAT_V: 780,      // 자연스럽게: 1초에 780px(무대 좌표) 빠르기 — 한 번 옮기는 시간 = 지나가는 길이 ÷ 이 빠르기(기둥 3개 평균 1.8초쯤)
  MOTION: 0.86,    // 한 번 옮기는 시간 가운데 움직이는 몫(나머지는 내려놓고 숨 고르기)
  EASE_A: 0.24,    // 움직이는 시간 앞뒤로 이만큼씩 천천히 출발·멈춤(그 사이는 같은 빠르기)
  HOLD_MS: 4000,   // 다 옮긴 뒤 쉬는 시간
  STAGGER: 0.25,   // 세트마다 늦게 따라가는 몫 — 배속이면 한 번 옮기는 시간의 1/4
  STAGGER_NAT: 420, // 자연스럽게면 세트마다 0.42초
};
export const MUL = { x1: 1, x2: 2, x3: 3, x4: 4 };
export const SPEED_LABEL = { natural: "자연스럽게", x1: "1배속", x2: "2배속", x3: "3배속", x4: "4배속" };
export const PEG_NAMES = ["A", "B", "C", "D", "E"];
/** 예전 이름 "fast" = 1배속 */
export const normSpeed = (s) => (s === "fast" ? "x1" : HANOI.SPEEDS.includes(s) ? s : "x1");
export const fastMs = (speed) => HANOI.FAST_MS / MUL[normSpeed(speed)];
/** 세트 i 가 첫 세트보다 늦게 따라가는 시간(ms) */
export const staggerMs = (speed) => (normSpeed(speed) === "natural" ? HANOI.STAGGER_NAT : fastMs(speed) * HANOI.STAGGER);

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const popc = (m) => { let c = 0; for (let x = m; x; x >>= 1) c += x & 1; return c; };

/* ══════════ 최소 횟수 ══════════ */
// FS[k][c] = 기둥 k개로 원판 c개를 옮기는 횟수 · SPLIT[k][c] = 먼저 비켜 둘 작은 판 수 q(같으면 큰 q)
const FS = { 3: [], 4: [], 5: [] }, SPLIT = { 4: [], 5: [] };
for (let c = 0; c <= HANOI.MAX; c++) FS[3][c] = 2 ** c - 1;
for (const k of [4, 5]) {
  FS[k][0] = 0; FS[k][1] = 1; SPLIT[k][1] = 0;
  for (let c = 2; c <= HANOI.MAX; c++) {
    let best = Infinity, bq = 1;
    for (let q = 1; q < c; q++) { const v = 2 * FS[k][q] + FS[k - 1][c - q]; if (v <= best) { best = v; bq = q; } }
    FS[k][c] = best; SPLIT[k][c] = bq;
  }
}
/** 원판 n개 · 기둥 k개의 최소(프레임–스튜어트) 횟수 */
export const movesOf = (n, pegs = 3) => FS[pegs][n];
export const splitOf = (n, pegs) => (pegs > 3 ? SPLIT[pegs][n] : n - 1);

/* ══════════ 배치 ══════════ */
const SAFE_TOP = 122, SAFE_BOT = 836;    // 위는 조작 막대, 아래는 안내 글자 자리
// 기둥 수마다: 기둥 사이 · 가장 큰·작은 원판 지름(무대 px) — 큰 판도 기둥 사이보다 좁다
const KIT = { 3: { SP: 470, WMAX: 440, WMIN: 78 }, 4: { SP: 352, WMAX: 328, WMIN: 64 }, 5: { SP: 282, WMAX: 256, WMIN: 54 } };

/** 원판 n개 · 기둥 pegs 개일 때의 무대 배치 — 그림 전체(올라가는 길 꼭대기 ~ 받침 그림자)가 화면 가운데 오도록 받침 높이를 정한다 */
export function hanoiLayout(n, pegs = 3) {
  const K = KIT[pegs] || KIT[3];
  const X = Array.from({ length: pegs }, (_, i) => 800 + (i - (pegs - 1) / 2) * K.SP);
  const h = Math.min(56, 380 / n);                          // 원판 두께
  const pegH = clamp(n * h + 60, 240, 440);                 // 받침 위 기둥 높이(다 쌓아도 위가 남게)
  const step = n > 1 ? Math.min(125, (K.WMAX - K.WMIN) / (n - 1)) : 0;
  const widths = Array.from({ length: n }, (_, d) => K.WMAX - step * (n - 1 - d));   // d = 0 이 가장 작은 판
  const TILT = 0.17;                                        // 윗면 타원의 납작함(세로/가로) — 살짝 내려다본 모습
  const R = 62, LIFT = 26, PEG_R = 11;                      // 길 모서리 반지름 · 기둥 끝 위 여유 · 기둥 반지름
  const BOARD = { half: ((pegs - 1) / 2) * K.SP + K.WMAX / 2 + 40, depth: 42, thick: 34, shadow: 24 };
  const ryMax = (K.WMAX / 2) * TILT;
  const topOff = -(pegH + LIFT + R + h + ryMax);
  const botOff = BOARD.depth + BOARD.thick + BOARD.shadow;
  const yBase = (SAFE_TOP + SAFE_BOT) / 2 - (topOff + botOff) / 2;
  const yTip = yBase - pegH;
  return { n, pegs, X, SP: K.SP, WMAX: K.WMAX, h, pegH, widths, TILT, R, LIFT, PEG_R, BOARD, yBase, yTip, yClear: yTip - LIFT };
}

/** 깔린 판이 lv 개인 자리에 놓인 원판의 아랫면 y */
export const levelY = (L, lv) => L.yBase - lv * L.h;

/**
 * 한 번 옮기는 길: 곧게 들어 올려 기둥 끝을 벗어나고(LIFT 만큼 여유), 사분원으로 돌아 건너가서, 사분원으로 내려와 곧게 내려놓는다.
 * 원판이 기둥에 꿰여 있는 동안(아랫면이 기둥 끝보다 아래)에는 옆으로 움직이지 않는다.
 */
export function moveLen(L, from, fromLv, to, toLv) {
  const up = levelY(L, fromLv) - L.yClear, down = levelY(L, toLv) - L.yClear;
  const across = Math.abs(L.X[to] - L.X[from]);
  return up + Math.PI * L.R + (across - 2 * L.R) + down;    // 사분원 둘 = πR
}
export function movePath(L, from, fromLv, to, toLv, segs = 12) {
  const x0 = L.X[from], x1 = L.X[to], dir = Math.sign(x1 - x0), yc = L.yClear, r = L.R;
  const pts = [[x0, levelY(L, fromLv)], [x0, yc]];
  for (let i = 1; i <= segs; i++) {
    const a = (i / segs) * (Math.PI / 2);
    pts.push([x0 + dir * r * (1 - Math.cos(a)), yc - r * Math.sin(a)]);
  }
  for (let i = 0; i <= segs; i++) {
    const a = (Math.PI / 2) * (1 - i / segs);
    pts.push([x1 - dir * r * (1 - Math.cos(a)), yc - r * Math.sin(a)]);
  }
  pts.push([x1, levelY(L, toLv)]);
  return pts;
}
/**
 * 길 위의 비율 u(0~1) → [x, y] (무대 px). movePath 를 촘촘히 펼친 것과 같지만 꺾은선 없이 정확히 센다(3D 가 매 순간 쓴다).
 */
export function pathPoint(L, from, fromLv, to, toLv, u) {
  const x0 = L.X[from], x1 = L.X[to], dir = Math.sign(x1 - x0) || 1, yc = L.yClear, r = L.R;
  const y0 = levelY(L, fromLv), y1 = levelY(L, toLv);
  const up = y0 - yc, arc = (Math.PI / 2) * r, mid = Math.abs(x1 - x0) - 2 * r, down = y1 - yc;
  let s = clamp(u, 0, 1) * (up + 2 * arc + mid + down);
  if (s <= up) return [x0, y0 - s];
  s -= up;
  if (s <= arc) { const a = s / r; return [x0 + dir * r * (1 - Math.cos(a)), yc - r * Math.sin(a)]; }
  s -= arc;
  if (s <= mid) return [x0 + dir * (r + s), yc - r];
  s -= mid;
  if (s <= arc) { const a = Math.PI / 2 - s / r; return [x1 - dir * r * (1 - Math.cos(a)), yc - r * Math.sin(a)]; }
  s -= arc;
  return [x1, yc + Math.min(s, down)];
}
/** 한 번 옮기는 시간(ms) */
export function moveMs(L, speed, from, fromLv, to, toLv) {
  const sp = normSpeed(speed);
  return sp === "natural" ? (moveLen(L, from, fromLv, to, toLv) / HANOI.NAT_V) * 1000 : fastMs(sp);
}

/**
 * 움직임의 진행: 옮기는 시간 중 k(0~1) 지점 → 길 위의 비율(0~1).
 * 앞 MOTION 몫 동안 움직이고(처음·끝 EASE_A 는 고르게 빨라졌다 느려짐), 나머지는 내려놓은 채 쉰다.
 * a ~ b 구간만 움직이게 하려면 moveEase((k − a) / (b − a) · MOTION) 처럼 쓴다(로봇이 나를 때).
 */
export function moveEase(k) {
  const u = clamp(k / HANOI.MOTION, 0, 1), a = HANOI.EASE_A, z = 2 * a * (1 - a);
  if (u < a) return (u * u) / z;
  if (u > 1 - a) return 1 - ((1 - u) * (1 - u)) / z;
  return (u - a / 2) / (1 - a);
}

/* ══════════ 시간표 ══════════ */
/** 기둥 묶음 P(비트)에서 s · t 를 뺀 기둥 가운데 비켜 둘 곳: 출발 기둥에 가장 가까운 것(같으면 도착에 가까운 쪽) */
function viaOf(P, s, t, pegs) {
  let best = -1, bd = Infinity;
  for (let i = 0; i < pegs; i++) {
    if (!((P >> i) & 1) || i === s || i === t) continue;
    const d = Math.abs(i - s) * 100 + Math.abs(i - t);
    if (d < bd) { bd = d; best = i; }
  }
  return best;
}

/**
 * 원판 n개 · 빠르기 speed("natural" | "x1" ~ "x4", 예전 "fast" = "x1") · 기둥 pegs 개의 시간표.
 *   total                — 한 번 다 옮기는 시간(ms) · moves — 횟수
 *   locate(τ, s, t)      — s → t 로 옮기기 시작해 τ ms 지난 순간: 몇 번째 이동인지(m, 1부터), 움직이는 판, 나머지 판의 자리
 *   startOf(m, s, t)     — m 번째 이동이 시작하는 시각과 걸리는 시간
 *   moveAt(m, s, t)      — m 번째 이동의 { disk, from, to, fromLv, toLv }
 */
export function hanoiTimeline(n, speed, pegs = 3) {
  const sp = normSpeed(speed);
  const L = hanoiLayout(n, pegs);
  const FULL = (1 << pegs) - 1, last = pegs - 1;
  const fast = sp !== "natural", D = fast ? fastMs(sp) : 0;
  const memo = new Map();
  const md = (s, bs, t, bt) => (fast ? D : (moveLen(L, s, bs, t, bt) / HANOI.NAT_V) * 1000);
  const keyOf = (c, s, t, P, b) => {
    let h = 0;
    for (let i = 0; i < pegs; i++) h = h * 32 + ((P >> i) & 1 ? b[i] : 0);
    return ((((c * 8 + s) * 8 + t) * 32 + P) * 33554432) + h;      // 2²⁵
  };
  const spare3 = (P, s, t) => { for (let i = 0; i < pegs; i++) if ((P >> i) & 1 && i !== s && i !== t) return i; return -1; };
  // W(c, s, t, P, b) = 기둥마다 큰 판이 b 개씩 깔린 위에서, 묶음 c 개를 기둥 묶음 P 만 써서 s → t 로 옮기는 시간
  function W(c, s, t, P, b) {
    if (c === 0) return 0;
    const kp = popc(P);
    if (fast) return FS[kp][c] * D;
    const key = keyOf(c, s, t, P, b);
    const hit = memo.get(key);
    if (hit !== undefined) return hit;
    let v;
    if (c === 1) v = md(s, b[s], t, b[t]);
    else if (kp === 3) {
      const a = spare3(P, s, t);
      const b1 = b.slice(); b1[s]++;            // 묶음의 맨 큰 판이 s 에 남은 채 나머지를 s → a
      const b2 = b.slice(); b2[t]++;            // 맨 큰 판을 t 로 옮긴 뒤 나머지를 a → t
      v = W(c - 1, s, a, P, b1) + md(s, b[s], t, b[t]) + W(c - 1, a, t, P, b2);
    } else {
      const q = SPLIT[kp][c], via = viaOf(P, s, t, pegs);
      const bA = b.slice(); bA[s] += c - q;      // 큰 판 c − q 개가 s 에 남은 채 작은 q 개를 via 로
      const bB = b.slice(); bB[t] += c - q;      // 큰 판을 t 로 옮긴 뒤 작은 q 개를 via → t
      v = W(q, s, via, P, bA) + W(c - q, s, t, P & ~(1 << via), b) + W(q, via, t, P, bB);
    }
    memo.set(key, v);
    return v;
  }
  const zero = () => new Array(pegs).fill(0);
  const total = W(n, 0, last, FULL, zero());
  const moves = FS[pegs][n];

  function done(t0) {
    const pos = [], lv = [];
    for (let d = 0; d < n; d++) { pos[d] = t0; lv[d] = n - 1 - d; }
    return { m: moves, moving: false, pos, lv };
  }
  function locate(tau, s0 = 0, t0 = last) {
    if (!(tau < total)) return done(t0);
    const pos = new Array(n), lv = new Array(n);
    let lo = 0, hi = n - 1, c = n, s = s0, t = t0, P = FULL, b = zero(), acc = 0, m = 0;
    const out = (mm, d, from, to, start, dur) => {
      pos[d] = -1; lv[d] = -1;
      return { m: mm, moving: true, disk: d, from, to, fromLv: b[from], toLv: b[to], start, dur, k: clamp((tau - start) / dur, 0, 1), pos, lv };
    };
    for (let guard = 0; guard < 4 * n + 8; guard++) {
      const kp = popc(P);
      if (c === 1) return out(m + 1, lo, s, t, acc, md(s, b[s], t, b[t]));
      if (kp === 3) {
        const a = spare3(P, s, t);
        const b1 = b.slice(); b1[s]++;
        const left = W(c - 1, s, a, P, b1);
        if (tau < acc + left) { pos[hi] = s; lv[hi] = b[s]; b = b1; t = a; hi--; c--; continue; }
        const dd = md(s, b[s], t, b[t]);
        if (tau < acc + left + dd) {
          for (let d = lo; d < hi; d++) { pos[d] = a; lv[d] = b[a] + (hi - 1 - d); }
          return out(m + FS[3][c - 1] + 1, hi, s, t, acc + left, dd);
        }
        acc += left + dd; m += FS[3][c - 1] + 1;
        pos[hi] = t; lv[hi] = b[t];
        const b2 = b.slice(); b2[t]++;
        b = b2; s = a; hi--; c--;
        continue;
      }
      const q = SPLIT[kp][c], via = viaOf(P, s, t, pegs);
      const bA = b.slice(); bA[s] += c - q;
      const wA = W(q, s, via, P, bA);
      if (tau < acc + wA) {
        for (let d = lo + q; d <= hi; d++) { pos[d] = s; lv[d] = b[s] + (hi - d); }
        b = bA; t = via; hi = lo + q - 1; c = q;
        continue;
      }
      acc += wA; m += FS[kp][q];
      const P2 = P & ~(1 << via), wM = W(c - q, s, t, P2, b);
      if (tau < acc + wM) {
        for (let d = lo; d < lo + q; d++) { pos[d] = via; lv[d] = b[via] + (lo + q - 1 - d); }
        P = P2; lo += q; c -= q;
        continue;
      }
      acc += wM; m += FS[kp - 1][c - q];
      for (let d = lo + q; d <= hi; d++) { pos[d] = t; lv[d] = b[t] + (hi - d); }
      const bB = b.slice(); bB[t] += c - q;
      b = bB; s = via; hi = lo + q - 1; c = q;
    }
    return done(t0);   // (부동소수 끝자락)
  }
  function startOf(mv, s0 = 0, t0 = last) {
    if (!(mv >= 1)) return { start: 0, dur: 0 };
    if (mv > moves) return { start: total, dur: 0 };
    let c = n, s = s0, t = t0, P = FULL, b = zero(), acc = 0, base = 0;
    for (let guard = 0; guard < 4 * n + 8; guard++) {
      const kp = popc(P);
      if (c === 1) return { start: acc, dur: md(s, b[s], t, b[t]) };
      if (kp === 3) {
        const a = spare3(P, s, t), lm = FS[3][c - 1];
        const b1 = b.slice(); b1[s]++;
        if (mv - base <= lm) { b = b1; t = a; c--; continue; }
        const left = W(c - 1, s, a, P, b1), dd = md(s, b[s], t, b[t]);
        if (mv - base === lm + 1) return { start: acc + left, dur: dd };
        acc += left + dd; base += lm + 1;
        const b2 = b.slice(); b2[t]++;
        b = b2; s = a; c--;
        continue;
      }
      const q = SPLIT[kp][c], via = viaOf(P, s, t, pegs);
      const bA = b.slice(); bA[s] += c - q;
      if (mv - base <= FS[kp][q]) { b = bA; t = via; c = q; continue; }
      acc += W(q, s, via, P, bA); base += FS[kp][q];
      const P2 = P & ~(1 << via);
      if (mv - base <= FS[kp - 1][c - q]) { P = P2; c -= q; continue; }
      acc += W(c - q, s, t, P2, b); base += FS[kp - 1][c - q];
      const bB = b.slice(); bB[t] += c - q;
      b = bB; s = via; c = q;
    }
    return { start: total, dur: 0 };
  }
  function moveAt(mv, s0 = 0, t0 = last) {
    const so = startOf(mv, s0, t0);
    const st = locate(so.start + so.dur * 0.5, s0, t0);
    return st.moving ? { disk: st.disk, from: st.from, to: st.to, fromLv: st.fromLv, toLv: st.toLv } : null;
  }
  return { n, pegs, speed: sp, L, total, moves, locate, startOf, moveAt, memoSize: () => memo.size };
}

/**
 * 시계(ms) → 지금 모습. 짝수 바퀴는 첫 기둥 → 마지막 기둥, 홀수 바퀴는 거꾸로. 다 옮기면 HOLD 동안 쉰다.
 *   { cycle, src, dst(이번 바퀴의 출발·도착 기둥), tau(이번 바퀴에서 지난 시간), hold(쉬는 중이면 지난 ms), ...locate }
 */
export function hanoiAt(TL, elapsed) {
  const Tc = TL.total + HANOI.HOLD_MS;
  const e = Math.max(0, elapsed);
  const cycle = Math.floor(e / Tc);
  const tau = e - cycle * Tc;
  const last = (TL.pegs || 3) - 1;
  const [s, t] = cycle % 2 === 0 ? [0, last] : [last, 0];
  const st = TL.locate(Math.min(tau, TL.total), s, t);
  return { ...st, cycle, src: s, dst: t, tau, hold: tau >= TL.total ? tau - TL.total : null };
}

/** 빠르기를 바꿀 때: 같은 바퀴의 같은 이동, 같은 진행 비율에서 이어지도록 새 시계 값을 준다 */
export function remapElapsed(oldTL, newTL, elapsed) {
  const st = hanoiAt(oldTL, elapsed);
  const Tc = newTL.total + HANOI.HOLD_MS;
  if (st.hold != null) return st.cycle * Tc + newTL.total + Math.min(st.hold, HANOI.HOLD_MS - 1);
  if (!st.moving) return st.cycle * Tc;
  const nw = newTL.startOf(st.m, st.src, st.dst);
  return st.cycle * Tc + nw.start + st.k * nw.dur;
}

/**
 * 세트 i 의 모습: 첫 세트보다 staggerMs 만큼씩 늦게 따라간다(아직 시작 전이면 처음 모습).
 * 로봇이 미리 움직이도록 바로 앞 · 뒤 이동도 붙인다(시각은 이번 바퀴 안의 ms):
 *   prev = { to, toLv, disk, start, dur } — 바로 전에 놓은 자리. 바퀴의 첫 이동이면 출발 기둥 맨 위(가장 작은 판), start = null
 *   next = { from, fromLv, disk, start, dur } — 다음에 잡을 자리. 바퀴의 마지막 이동이면 null
 */
export function setAt(TL, elapsed, i, speed = TL.speed) {
  const st = hanoiAt(TL, elapsed - i * staggerMs(speed));
  let prev = null, next = null;
  if (st.moving) {
    if (st.m > 1) {
      const p = TL.moveAt(st.m - 1, st.src, st.dst), so = TL.startOf(st.m - 1, st.src, st.dst);
      prev = { to: p.to, toLv: p.toLv, disk: p.disk, start: so.start, dur: so.dur };
    } else prev = { to: st.src, toLv: TL.n - 1, disk: 0, start: null, dur: 0 };
    if (st.m < TL.moves) {
      const q = TL.moveAt(st.m + 1, st.src, st.dst), so = TL.startOf(st.m + 1, st.src, st.dst);
      next = { from: q.from, fromLv: q.fromLv, disk: q.disk, start: so.start, dur: so.dur };
    }
  }
  return { ...st, prev, next, set: i };
}

/* ══════════ 글자 ══════════ */
export const comma = (v) => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
/** 4시간 33분 3초 · 12일 3시간 16분 15초 · 34년 9일 … — 0 인 단위는 앞뒤만 빼고(가운데 0분은 남긴다) */
export function fmtDur(ms) {
  let s = Math.max(0, Math.round(ms / 1000));
  const y = Math.floor(s / 31536000); s -= y * 31536000;
  const d = Math.floor(s / 86400); s -= d * 86400;
  const h = Math.floor(s / 3600); s -= h * 3600;
  const m = Math.floor(s / 60); s -= m * 60;
  const parts = [[y, "년"], [d, "일"], [h, "시간"], [m, "분"], [s, "초"]];
  const i0 = parts.findIndex(([v]) => v > 0);
  if (i0 < 0) return "0초";
  let i1 = parts.length - 1;
  while (i1 > i0 && parts[i1][0] === 0) i1--;
  return parts.slice(i0, i1 + 1).map(([v, u]) => `${comma(v)}${u}`).join(" ");
}
/** 2의 거듭제곱 위 첨자(2¹⁴) */
export const supNum = (k) => String(k).split("").map((c) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[Number(c)]).join("");
