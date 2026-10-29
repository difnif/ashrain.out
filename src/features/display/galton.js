// ashrain.out — 교실 모니터: 갈톤 보드(구슬 낙하) 배치와 세계 만들기 (galton.js) — JSX 없음
// 못을 R줄 엇갈리게 박고(가운데 삼각형 = 이론의 길, 위에서 i번째 줄에 i + 1개) 아래에 칸을 R + 1개 둔다.
// 구슬 수 N 과 줄 수 R 에 따라 구슬 크기를 정해 가장 많이 쌓이는 칸도 무대 안에 들어가게 한다.
// 물리 값(반발·저항·흔들림)은 줄 수 6~12, 구슬 100~2000개에서 칸별 개수가 이항분포 B(R, 1/2)에 가깝게 나오도록
// 맞춘 값이다(검산: tests/display.test.mjs — 분포 거리와 표준편차 비).
import { makeWorld, addPeg, addWall, addMarble, seal } from "./physics.js";
import { rng } from "./core.js";

/** 크기에 상관없이 같은 모양(비율) — 줄 간격 · 구슬+못 닿는 거리 · 중력 · 흔들림은 못 간격 sx 에 비례 */
export const SHAPE = { sy: 0.64, reach: 0.2, g: 23, vy: 4.4, jitter: 0.5, pack: 4.3, fv: 0.4, ft: 0.12, kick: 1.5 };
export const GALTON = {
  NS: [100, 200, 500, 1000, 2000], NDEF: 500,
  ROWS: [6, 8, 10, 12], RDEF: 10,
};

/** 이항계수 */
export function comb(n, k) {
  if (k < 0 || k > n) return 0;
  let c = 1;
  for (let i = 1; i <= k; i++) c = (c * (n - k + i)) / i;
  return Math.round(c);
}
/** B(n, 1/2) 의 k 번째 확률 */
export const binom = (n, k) => comb(n, k) / 2 ** n;

/** 구슬이 다 나오는 데 걸리는 시간(초) — 1초에 FLOW개. 더 빠르면 구슬끼리 너무 자주 부딪혀 가운데로 몰린다 */
export const FLOW = 45;
export const spawnSpan = (N) => Math.max(3, N / FLOW);

/**
 * 배치. cx 가운데 x · yTop 첫 못 줄 · yFloor 칸 바닥 · wMax 보드 최대 폭
 * 반환: { R, N, sx, sy, rp, r, cx, ys(못 줄 y), yDiv(칸막이 시작), yFloor, bins: [{x0, x1, xc}], wallL, wallR }
 */
export function galtonLayout({ R = GALTON.RDEF, N = GALTON.NDEF, cx = 520, yTop = 172, yFloor = 798, wMax = 620 } = {}) {
  const sx = Math.min(56, wMax / (R + 1));
  const sy = sx * SHAPE.sy;
  const ys = Array.from({ length: R }, (_, i) => yTop + i * sy);
  // 칸 높이: 마지막 못 줄 아래부터 바닥까지
  const yDiv0 = ys[R - 1] + sx * 0.36;
  const Hb = yFloor - yDiv0 - 8;
  // 가장 많이 쌓일 칸(가운데)이 칸 안에 들어가게 구슬 반지름을 정한다
  const M = N * binom(R, Math.floor(R / 2)) * 1.25 + 4;
  let r = Math.sqrt((Hb * (sx - 3)) / (SHAPE.pack * M));
  r = Math.max(2.3, Math.min(9.5, sx * 0.15, r));
  // 못 반지름: 구슬 + 못 = 늘 같은 비율(SHAPE.reach × sx) — 구슬이 작아지면 못이 굵어져 한 줄마다 튀는 모습이 같다
  const rp = Math.max(3, Math.min(sx * 0.3, SHAPE.reach * sx - r));
  const yDiv = ys[R - 1] + rp + Math.max(2 * r + 4, sx * 0.2);
  const bins = Array.from({ length: R + 1 }, (_, k) => {
    const xc = cx + (k - R / 2) * sx;
    return { xc, x0: xc - sx / 2, x1: xc + sx / 2 };
  });
  return { R, N, sx, sy, rp, r, cx, yTop, ys, yDiv, yFloor, Hb: yFloor - yDiv, bins };
}

/** 못의 자리: [{x, y}] — 직사각형으로 빽빽하게(줄마다 반 칸씩 엇갈림). 가운데 삼각형이 이론의 길이고,
 *  바깥 못은 멀리 튄 구슬도 벽을 타고 미끄러지지 않고 다시 못에 부딪히게 한다 */
export function pegsOf(L) {
  const out = [], half = (L.R / 2) * L.sx + 0.01;
  for (let i = 0; i < L.R; i++) {
    const off = i % 2 ? 0.5 : 0;
    for (let m = -L.R; m <= L.R; m++) {
      const x = L.cx + (m + off) * L.sx;
      if (Math.abs(x - L.cx) <= half) out.push({ x, y: L.ys[i], tri: Math.abs(x - L.cx) <= (i / 2) * L.sx + 0.01 });
    }
  }
  return out;
}
/** 바깥 벽(왼쪽·오른쪽) — 위는 깔때기, 아래는 곧은 벽 */
export function wallsOf(L) {
  const { cx, sx, sy, yTop, R, yFloor } = L;
  const xw = (R / 2 + 0.5) * sx, yA = yTop - sy * 1.6, yB = yTop - sy * 0.25;
  const left = [[cx - 0.55 * sx, yA - sx * 0.9], [cx - 0.55 * sx, yA], [cx - xw, yB], [cx - xw, yFloor]];
  const right = [[cx + 0.55 * sx, yA - sx * 0.9], [cx + 0.55 * sx, yA], [cx + xw, yB], [cx + xw, yFloor]];
  return { left, right };
}
/** 칸막이: 마지막 못 줄의 못 바로 아래부터 바닥까지 */
export function dividersOf(L) {
  return L.bins.slice(0, -1).map((b) => [[b.x1, L.yDiv], [b.x1, L.yFloor]]);
}

/** 세계 만들기 — 구슬은 0.5초 뒤부터 spawnSpan(N)초 동안 위 입구에서 나온다 */
export const PHYS = { eWall: 0.32, eBall: 0.22, fric: 0.04 };
/** 공기 저항 — 구슬이 많아 서로 자주 부딪히면 퍼짐이 줄어드는 만큼 조금 덜 막는다(이론 분포에 가깝게 맞춘 값) */
export const dragOf = (N) => 2.8 - 0.35 * Math.min(1, Math.log(Math.max(500, N) / 500) / Math.log(2));
export function galtonWorld(L, seed = 11, phys = PHYS) {
  const W = makeWorld({ g: SHAPE.g * L.sx, drag: dragOf(L.N), ...phys, cell: 14, freezeY: L.yDiv + 6, freezeV: SHAPE.fv * L.sx, freezeT: SHAPE.ft, nudge: 1.4 * L.sx, kick: SHAPE.kick * L.sx, seed });
  for (const p of pegsOf(L)) addPeg(W, p.x, p.y, L.rp);
  const { left, right } = wallsOf(L);
  for (const side of [left, right]) for (let k = 0; k + 1 < side.length; k++) addWall(W, ...side[k], ...side[k + 1], 2.5);
  for (const d of dividersOf(L)) addWall(W, ...d[0], ...d[1], 1.6);
  addWall(W, L.bins[0].x0 - 4, L.yFloor + 3, L.bins[L.R].x1 + 4, L.yFloor + 3, 3);
  const rnd = rng(seed * 7919 + L.N);
  const span = spawnSpan(L.N);
  for (let i = 0; i < L.N; i++) {
    const at = 0.5 + (span * i) / L.N + rnd() * 0.004;
    addMarble(W, {
      x: L.cx + (rnd() - 0.5) * L.sx * SHAPE.jitter, y: L.yTop - L.sy * 0.95 + (rnd() - 0.5) * 6, r: L.r * (0.94 + rnd() * 0.12),
      vx: (rnd() - 0.5) * 0.45 * L.sx, vy: L.sx * (SHAPE.vy + rnd() * 0.9), at, tag: i % 3,
    });
  }
  return seal(W);
}

/** 칸 번호(0..R) — 칸막이 사이 어디에 있는지. 칸 밖이면 -1 */
export function binOf(L, x, y) {
  if (y < L.yDiv) return -1;
  const k = Math.floor((x - L.bins[0].x0) / L.sx);
  return k >= 0 && k <= L.R ? k : -1;
}
