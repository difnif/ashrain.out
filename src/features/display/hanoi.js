// ashrain.out — 교실 모니터 「액자」: 하노이의 탑 — 계산부 (hanoi.js)
// 위치: src/features/display/hanoi.js — JSX 없음. 그리기(frames/hanoi.jsx)와 검산(tests/hanoi.test.mjs)이 함께 쓴다.
//
// 규칙  원판 n개를 한 기둥에서 다른 기둥으로. 한 번에 맨 위 원판 하나만, 큰 원판은 작은 원판 위에 못 놓는다 → 최소 2ⁿ − 1번.
// 시간  빠르게    : 한 번 옮기는 데 1초(1초에 1개) → 다 옮기는 시간 = (2ⁿ − 1)초.
//       자연스럽게: 한 번 옮기는 시간이 원판이 실제로 지나가는 길(들어 올림 + 건너감 + 내려놓음)의 길이에 비례한다.
//                   같은 원판이라도 깔린 판 수에 따라 길이가 달라서, 다 옮기는 시간은 재귀로 센다
//                   (「옮길 판 수 · 출발 · 도착 · 기둥마다 깔린 큰 판 수」를 열쇠로 기억 — 2²⁰번이어도 금방).
// 반복  다 옮기면 HOLD 동안 쉬고 반대로(C → A) 옮긴다 — 끝없이 돈다.
// 무대  1600×900, 화면 y 는 아래로 +. 원판 위치는 「아랫면 가운데」 좌표로 센다.

export const HANOI = {
  MIN: 3, MAX: 20, DEF: 14,   // 처음 값: 원판 14개(빠르게면 4시간 33분 3초 — 3시간 넘게 걸리는 가장 작은 수)
  FAST_MS: 1000,   // 빠르게: 1초에 1개
  NAT_V: 780,      // 자연스럽게: 1초에 780px(무대 좌표) 빠르기 — 한 번 옮기는 시간 = 지나가는 길이 ÷ 이 빠르기(평균 1.8초쯤)
  MOTION: 0.86,    // 한 번 옮기는 시간 가운데 움직이는 몫(나머지는 내려놓고 숨 고르기)
  EASE_A: 0.24,    // 움직이는 시간 앞뒤로 이만큼씩 천천히 출발·멈춤(그 사이는 같은 빠르기)
  HOLD_MS: 4000,   // 다 옮긴 뒤 쉬는 시간
};
export const PEG_NAMES = ["A", "B", "C"];

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

/* ══════════ 배치 ══════════ */
const SP = 470;                          // 기둥 사이
const PEG_X = [800 - SP, 800, 800 + SP];
const WMAX = 440, WMIN = 78;             // 가장 큰·작은 원판 지름(무대 px) — 큰 판도 기둥 사이보다 좁다
const SAFE_TOP = 122, SAFE_BOT = 836;    // 위는 조작 막대, 아래는 안내 글자 자리

/** 원판 n개일 때의 무대 배치 — 그림 전체(올라가는 길 꼭대기 ~ 받침 그림자)가 화면 가운데 오도록 받침 높이를 정한다 */
export function hanoiLayout(n) {
  const h = Math.min(56, 380 / n);                         // 원판 두께
  const pegH = clamp(n * h + 60, 240, 440);                 // 받침 위 기둥 높이(다 쌓아도 위가 남게)
  const step = n > 1 ? Math.min(125, (WMAX - WMIN) / (n - 1)) : 0;
  const widths = Array.from({ length: n }, (_, d) => WMAX - step * (n - 1 - d));   // d = 0 이 가장 작은 판
  const TILT = 0.17;                                        // 윗면 타원의 납작함(세로/가로) — 살짝 내려다본 모습
  const R = 62, LIFT = 26, PEG_R = 11;                      // 길 모서리 반지름 · 기둥 끝 위 여유 · 기둥 반지름
  const BOARD = { half: 730, depth: 42, thick: 34, shadow: 24 };
  const ryMax = (WMAX / 2) * TILT;
  const topOff = -(pegH + LIFT + R + h + ryMax);
  const botOff = BOARD.depth + BOARD.thick + BOARD.shadow;
  const yBase = (SAFE_TOP + SAFE_BOT) / 2 - (topOff + botOff) / 2;
  const yTip = yBase - pegH;
  return { n, X: PEG_X, SP, h, pegH, widths, TILT, R, LIFT, PEG_R, BOARD, yBase, yTip, yClear: yTip - LIFT };
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
/** 한 번 옮기는 시간(ms) */
export function moveMs(L, speed, from, fromLv, to, toLv) {
  return speed === "fast" ? HANOI.FAST_MS : (moveLen(L, from, fromLv, to, toLv) / HANOI.NAT_V) * 1000;
}

/**
 * 움직임의 진행: 옮기는 시간 중 k(0~1) 지점 → 길 위의 비율(0~1).
 * 앞 MOTION 몫 동안 움직이고(처음·끝 EASE_A 는 고르게 빨라졌다 느려짐), 나머지는 내려놓은 채 쉰다.
 */
export function moveEase(k) {
  const u = clamp(k / HANOI.MOTION, 0, 1), a = HANOI.EASE_A, z = 2 * a * (1 - a);
  if (u < a) return (u * u) / z;
  if (u > 1 - a) return 1 - ((1 - u) * (1 - u)) / z;
  return (u - a / 2) / (1 - a);
}

/* ══════════ 시간표 ══════════ */
/**
 * 원판 n개 · 빠르기 speed("fast" | "natural") 의 시간표.
 *   total                — 한 번 다 옮기는 시간(ms)
 *   locate(τ, s, t)      — s → t 로 옮기기 시작해 τ ms 지난 순간: 몇 번째 이동인지, 움직이는 판, 나머지 판의 자리
 *   startOf(m, s, t)     — m 번째 이동이 시작하는 시각과 걸리는 시간
 */
export function hanoiTimeline(n, speed) {
  const L = hanoiLayout(n);
  const memo = new Map();
  const dur = (s, bs, t, bt) => moveMs(L, speed, s, bs, t, bt);
  // T(k, s, t, b) = 큰 판들이 기둥마다 b 개씩 깔린 위에서, 작은 판 k 개를 s → t 로 옮기는 시간
  function T(k, s, t, b0, b1, b2) {
    if (k === 0) return 0;
    const key = ((((k * 3 + s) * 3 + t) * 32 + b0) * 32 + b1) * 32 + b2;
    const hit = memo.get(key);
    if (hit !== undefined) return hit;
    const a = 3 - s - t, b = [b0, b1, b2];
    const bl = b.slice(); bl[s]++;            // 맨 큰 판(이 묶음의)이 s 에 남은 채 나머지를 s → a
    const br = b.slice(); br[t]++;            // 맨 큰 판을 t 로 옮긴 뒤 나머지를 a → t
    const v = T(k - 1, s, a, bl[0], bl[1], bl[2]) + dur(s, b[s], t, b[t]) + T(k - 1, a, t, br[0], br[1], br[2]);
    memo.set(key, v);
    return v;
  }
  const total = T(n, 0, 2, 0, 0, 0);

  function done(t) {
    const pos = [], lv = [];
    for (let d = 0; d < n; d++) { pos[d] = t; lv[d] = n - 1 - d; }
    return { m: 2 ** n - 1, moving: false, pos, lv };
  }
  function locate(tau, s0 = 0, t0 = 2) {
    if (tau >= total) return done(t0);
    const pos = new Array(n), lv = new Array(n);
    let s = s0, t = t0, b = [0, 0, 0], acc = 0, m = 0;
    for (let k = n; k >= 1; k--) {
      const a = 3 - s - t, d = k - 1, half = 2 ** (k - 1);
      const bl = b.slice(); bl[s]++;
      const left = T(k - 1, s, a, bl[0], bl[1], bl[2]);
      if (tau < acc + left) { pos[d] = s; lv[d] = b[s]; b = bl; t = a; continue; }
      const md = dur(s, b[s], t, b[t]);
      if (tau < acc + left + md) {
        for (let e = 0; e < d; e++) { pos[e] = a; lv[e] = b[a] + (d - 1 - e); }
        pos[d] = -1; lv[d] = -1;
        const start = acc + left;
        return { m: m + half, moving: true, disk: d, from: s, to: t, fromLv: b[s], toLv: b[t],
          start, dur: md, k: (tau - start) / md, pos, lv };
      }
      acc += left + md; m += half;
      const br = b.slice(); br[t]++;
      pos[d] = t; lv[d] = b[t]; b = br; s = a;
    }
    return done(t0);   // (부동소수 끝자락)
  }
  function startOf(mv, s0 = 0, t0 = 2) {
    let s = s0, t = t0, b = [0, 0, 0], acc = 0, base = 0;
    for (let k = n; k >= 1; k--) {
      const a = 3 - s - t, half = 2 ** (k - 1);
      const bl = b.slice(); bl[s]++;
      const left = T(k - 1, s, a, bl[0], bl[1], bl[2]);
      if (mv - base < half) { b = bl; t = a; continue; }
      const md = dur(s, b[s], t, b[t]);
      if (mv - base === half) return { start: acc + left, dur: md };
      acc += left + md; base += half;
      const br = b.slice(); br[t]++; b = br; s = a;
    }
    return { start: total, dur: 0 };
  }
  return { n, speed, L, total, moves: 2 ** n - 1, locate, startOf, memoSize: () => memo.size };
}

/**
 * 시계(ms) → 지금 모습. 짝수 바퀴는 A → C, 홀수 바퀴는 C → A. 다 옮기면 HOLD 동안 쉰다.
 *   { cycle, from, to(이번 바퀴의 출발·도착 기둥), tau(이번 바퀴에서 지난 시간), hold(쉬는 중이면 지난 ms), ...locate }
 */
export function hanoiAt(TL, elapsed) {
  const Tc = TL.total + HANOI.HOLD_MS;
  const e = Math.max(0, elapsed);
  const cycle = Math.floor(e / Tc);
  const tau = e - cycle * Tc;
  const [s, t] = cycle % 2 === 0 ? [0, 2] : [2, 0];
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

/* ══════════ 글자 ══════════ */
export const comma = (v) => String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
/** 4시간 33분 3초 · 12일 3시간 16분 15초 · 31초 — 0 인 단위는 앞뒤만 빼고(가운데 0분은 남긴다) */
export function fmtDur(ms) {
  let s = Math.max(0, Math.round(ms / 1000));
  const d = Math.floor(s / 86400); s -= d * 86400;
  const h = Math.floor(s / 3600); s -= h * 3600;
  const m = Math.floor(s / 60); s -= m * 60;
  const parts = [[d, "일"], [h, "시간"], [m, "분"], [s, "초"]];
  let i0 = parts.findIndex(([v]) => v > 0);
  if (i0 < 0) return "0초";
  let i1 = parts.length - 1;
  while (i1 > i0 && parts[i1][0] === 0) i1--;
  return parts.slice(i0, i1 + 1).map(([v, u]) => `${v}${u}`).join(" ");
}
/** 2의 거듭제곱 위 첨자(2¹⁴) */
export const supNum = (k) => String(k).split("").map((c) => "⁰¹²³⁴⁵⁶⁷⁸⁹"[Number(c)]).join("");
