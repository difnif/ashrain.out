// node tests/hanoi.test.mjs — 교실 모니터 액자 「하노이의 탑」 검산. 실패 시 exit 1.
//   1) 옮기는 순서: 모든 이동을 기둥들로 따로 흉내 내며 규칙(맨 위 판만 · 큰 판은 작은 판 위에 못 놓음)을 본다.
//      기둥 3개 = 최소 2ⁿ − 1 · 닫힌 식(움직이는 판 = m 의 끝자리 0 개수, 판 d 의 자리 = 방향 × ⌊(m + 2ᵈ)/2ᵈ⁺¹⌋)과 같다.
//      기둥 4 · 5개 = 프레임–스튜어트 횟수(알려진 수열) · 작은 n 은 모든 상태를 넓이 우선으로 뒤져 찾은 진짜 최소와 같다.
//   2) 시간: 1 ~ 4배속 = 정확히 (횟수 ÷ 배수)초, 자연스럽게 = 이동마다 「지나간 길이 ÷ 빠르기」, 재귀로 센 합 = 하나씩 더한 합.
//      원판 30개(10억 번)도 어느 순간이든 바로 찾는다.
//   3) 길: 기둥에 꿰인 동안 옆으로 안 움직이고, 건널 때는 모든 기둥 끝보다 위. 그림이 무대(조작 막대·안내 글자 자리) 안.
//   4) 세트: 세트마다 같은 시간만큼 늦게 따라가고, 바로 전 이동(로봇이 다가갈 출발점)을 바르게 준다.
//   5) 그리기 훑기: 원판 · 기둥 · 빠르기 · 테마 · 세트 수를 섞어 처음부터 끝·쉼·거꾸로까지 그려 오류·NaN 이 없는지.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  HANOI, hanoiLayout, hanoiTimeline, hanoiAt, remapElapsed, moveLen, movePath, pathPoint, moveMs, moveEase, levelY, fmtDur, comma, supNum,
  movesOf, normSpeed, fastMs, staggerMs, setAt, MUL,
} from "../src/features/display/hanoi.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const near = (a, b, eps = 1e-6) => assert.ok(Math.abs(a - b) <= eps, `${a} ≠ ${b}`);
const polyLen = (P) => P.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - P[i][0], p[1] - P[i][1]), 0);
const ctz = (m) => { let k = 0; while (m % 2 === 0) { m /= 2; k++; } return k; };

/** 이동을 하나씩 따라가며 규칙을 확인하고, 이동마다 { m, d, s, t, fromLv, toLv } 를 낸다 */
function* walk(n, s0, t0, pegs = 3, speed = "x1", TL = hanoiTimeline(n, speed, pegs)) {
  const peg = Array.from({ length: pegs }, () => []);
  for (let d = n - 1; d >= 0; d--) peg[s0].push(d);
  for (let m = 1; m <= TL.moves; m++) {
    const { start, dur } = TL.startOf(m, s0, t0);
    const st = TL.locate(start + dur / 2, s0, t0);
    assert.ok(st.moving && st.m === m, `m=${m}: ${st.m}`);
    const { disk: d, from: s, to: t } = st;
    // 나머지 판의 자리가 흉내 낸 기둥과 같다
    for (let p = 0; p < pegs; p++) peg[p].forEach((e, lv) => {
      if (e === d) return;
      assert.equal(st.pos[e], p, `m=${m} 판 ${e} 기둥`); assert.equal(st.lv[e], lv, `m=${m} 판 ${e} 높이`);
    });
    assert.equal(peg[s].at(-1), d, `m=${m}: 판 ${d} 이 ${s} 의 맨 위가 아님`);
    assert.equal(st.fromLv, peg[s].length - 1);
    assert.ok(!peg[t].length || peg[t].at(-1) > d, `m=${m}: 판 ${d} 를 더 작은 판 위에`);
    assert.equal(st.toLv, peg[t].length);
    peg[s].pop(); peg[t].push(d);
    yield { m, d, s, t, fromLv: st.fromLv, toLv: st.toLv };
  }
  assert.deepEqual(peg[t0], [...Array(n).keys()].reverse(), "끝에 모두 도착 기둥에 차례대로");
}

/* ── 1. 옮기는 순서 ── */
for (let k = 1; k <= 11; k++) {
  test(`원판 ${k}개: A→C · C→A 모두 규칙대로 ${2 ** k - 1}번 · 닫힌 식과 같다`, () => {
    for (const [s0, t0] of [[0, 2], [2, 0]]) {
      let cnt = 0;
      for (const mv of walk(k, s0, t0)) {
        cnt++;
        assert.equal(mv.d, ctz(mv.m), `m=${mv.m} 움직이는 판`);
        // 닫힌 식: 판 d 는 한 방향으로만 돈다(A→C 기준 n−d 가 짝수면 +1). C→A 는 거울(기둥 번호 2−p).
        const dir = (k - mv.d) % 2 === 0 ? 1 : 2;
        const at = (mm) => (dir * Math.floor((mm + 2 ** mv.d) / 2 ** (mv.d + 1))) % 3;
        const mirror = (p) => (s0 === 0 ? p : 2 - p);
        assert.equal(mv.s, mirror(at(mv.m - 1)), `m=${mv.m} 출발`); assert.equal(mv.t, mirror(at(mv.m)), `m=${mv.m} 도착`);
      }
      assert.equal(cnt, 2 ** k - 1);
    }
  });
}

// 기둥 4 · 5개: 프레임–스튜어트 횟수 — 알려진 수열(OEIS A007664 · A007665)
const FS4 = [1, 3, 5, 9, 13, 17, 25, 33, 41, 49, 65, 81, 97, 113, 129, 161, 193, 225, 257, 289, 321, 385, 449, 513, 577, 641, 705, 769, 897, 1025];
const FS5 = [1, 3, 5, 7, 11, 15, 19, 23, 27, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 127, 143, 159, 175, 191, 207, 223, 239, 255, 271];
test("기둥 4 · 5개: 원판 1 ~ 30 의 횟수가 프레임–스튜어트 수열과 같다(30개 → 1,025번 · 271번)", () => {
  for (let k = 1; k <= 30; k++) { assert.equal(movesOf(k, 4), FS4[k - 1], `4기둥 n=${k}`); assert.equal(movesOf(k, 5), FS5[k - 1], `5기둥 n=${k}`); }
  for (let k = 1; k <= 30; k++) assert.equal(movesOf(k, 3), 2 ** k - 1);
});
for (const pegs of [4, 5]) {
  test(`기둥 ${pegs}개: 원판 1 ~ 12 를 첫 → 끝 · 끝 → 첫 모두 규칙대로, 끝에 모두 도착`, () => {
    for (let k = 1; k <= 12; k++) for (const [s0, t0] of [[0, pegs - 1], [pegs - 1, 0]]) {
      let cnt = 0;
      for (const mv of walk(k, s0, t0, pegs)) { cnt++; assert.ok(mv.s !== mv.t); }
      assert.equal(cnt, movesOf(k, pegs), `n=${k}`);
    }
  });
}
/** 모든 배치를 넓이 우선으로 뒤져 찾은 진짜 최소 횟수(원판 n개, 기둥 k개, 첫 기둥 → 끝 기둥) */
function bfsMin(n, k) {
  const goal = (k - 1) * ((k ** n - 1) / (k - 1));        // 모든 판이 끝 기둥: 자리수 모두 k−1
  const start = 0, seen = new Map([[start, 0]]);
  let q = [start];
  const pegsOf = (code) => { const a = []; for (let d = 0; d < n; d++) { a.push(code % k); code = Math.floor(code / k); } return a; };
  while (q.length) {
    const nq = [];
    for (const c of q) {
      if (c === goal) return seen.get(c);
      const a = pegsOf(c), top = new Array(k).fill(n);
      for (let d = n - 1; d >= 0; d--) top[a[d]] = d;      // 기둥마다 가장 작은 판
      for (let s = 0; s < k; s++) {
        const d = top[s];
        if (d === n) continue;
        for (let t = 0; t < k; t++) {
          if (t === s || top[t] < d) continue;
          const nc = c + (t - s) * k ** d;
          if (!seen.has(nc)) { seen.set(nc, seen.get(c) + 1); nq.push(nc); }
        }
      }
    }
    q = nq;
  }
  return -1;
}
test("프레임–스튜어트 횟수 = 모든 배치를 뒤진 진짜 최소(기둥 4개 원판 ≤ 7 · 기둥 5개 원판 ≤ 6)", () => {
  for (let n2 = 1; n2 <= 7; n2++) assert.equal(movesOf(n2, 4), bfsMin(n2, 4), `4기둥 n=${n2}`);
  for (let n2 = 1; n2 <= 6; n2++) assert.equal(movesOf(n2, 5), bfsMin(n2, 5), `5기둥 n=${n2}`);
});

/* ── 2. 시간 ── */
test("1 ~ 4배속: 다 옮기는 시간 = 정확히 (횟수 ÷ 배수)초 (원판 3 ~ 30 · 기둥 3 ~ 5) · 예전 이름 fast = 1배속", () => {
  for (const pegs of HANOI.PEGS) for (let k = HANOI.MIN; k <= HANOI.MAX; k++) {
    for (const sp of ["x1", "x2", "x3", "x4"]) {
      const TL = hanoiTimeline(k, sp, pegs);
      assert.equal(TL.moves, movesOf(k, pegs));
      near(TL.total, (movesOf(k, pegs) * 1000) / MUL[sp], 1e-9 * TL.total);
    }
  }
  assert.equal(normSpeed("fast"), "x1"); assert.equal(normSpeed("natural"), "natural"); assert.equal(normSpeed("??"), "x1");
  assert.equal(hanoiTimeline(9, "fast").total, hanoiTimeline(9, "x1").total);
  assert.equal(fastMs("x4"), 250);
  assert.equal(HANOI.MAX, 30); assert.deepEqual(HANOI.SPEEDS, ["natural", "x1", "x2", "x3", "x4"]);
});
test("1배속: 13개 2시간 16분 31초 · 14개 4시간 33분 3초 — 3시간 넘는 가장 작은 수는 14 · 30개는 34년 넘게", () => {
  assert.equal(fmtDur(hanoiTimeline(13, "x1").total), "2시간 16분 31초");
  assert.equal(fmtDur(hanoiTimeline(14, "x1").total), "4시간 33분 3초");
  assert.ok(hanoiTimeline(13, "x1").total < 3 * 3600e3 && hanoiTimeline(14, "x1").total >= 3 * 3600e3);
  assert.equal(HANOI.DEF, 14);
  assert.equal(fmtDur(hanoiTimeline(30, "x1").total), "34년 17일 13시간 37분 3초");
  assert.equal(fmtDur(hanoiTimeline(30, "x1", 4).total), "17분 5초");
  assert.equal(fmtDur(hanoiTimeline(30, "x4", 5).total), "1분 8초");
});
test("배속: 이동마다 1초 ÷ 배수, m 번째 이동은 (m − 1) × 그 시간에 시작", () => {
  for (const sp of ["x1", "x3"]) {
    const TL = hanoiTimeline(10, sp), D = 1000 / MUL[sp];
    for (const m of [1, 2, 3, 100, 511, 512, 1023]) { const s = TL.startOf(m); near(s.start, (m - 1) * D, 1e-6); near(s.dur, D, 1e-9); }
  }
});
for (const [k, pegs] of [[3, 3], [8, 3], [12, 3], [6, 4], [11, 4], [5, 5], [13, 5]]) {
  test(`자연스럽게(원판 ${k}개 · 기둥 ${pegs}개): 이동 시간 ∝ 지나간 길이, 재귀 합 = 하나씩 더한 합, 거울 방향도 같은 합`, () => {
    for (const [s0, t0] of [[0, pegs - 1], [pegs - 1, 0]]) {
      const TL = hanoiTimeline(k, "natural", pegs);
      let sum = 0;
      const ratios = new Set();
      for (const mv of walk(k, s0, t0, pegs, "natural", TL)) {
        const len = moveLen(TL.L, mv.s, mv.fromLv, mv.t, mv.toLv);
        const { start, dur } = TL.startOf(mv.m, s0, t0);
        near(start, sum, 1e-6);
        near(dur, moveMs(TL.L, "natural", mv.s, mv.fromLv, mv.t, mv.toLv), 1e-9);
        ratios.add((dur / len).toFixed(9));
        sum += dur;
      }
      assert.equal(ratios.size, 1, "시간 ÷ 길이가 하나로 같지 않음");
      near([...ratios][0] * 1, 1000 / HANOI.NAT_V, 1e-9);
      near(sum, TL.total, 1e-6);
    }
  });
}
test("자연스럽게: 한 번 평균 1.6~2.0초(원판 7~30 · 기둥 3 ~ 5), 같은 판이라도 높이·거리에 따라 다르다", () => {
  for (const pegs of HANOI.PEGS) for (const k of [7, 10, 14, 20, 30]) {
    const TL = hanoiTimeline(k, "natural", pegs);
    const avg = TL.total / TL.moves / 1000;
    assert.ok(avg > 1.6 && avg < 2.0, `n=${k} 기둥 ${pegs} 평균 ${avg}`);
  }
  const L = hanoiLayout(8);
  assert.ok(moveLen(L, 0, 0, 2, 0) > moveLen(L, 0, 0, 1, 0), "먼 기둥이 더 길다");
  assert.ok(moveLen(L, 0, 0, 1, 0) > moveLen(L, 0, 5, 1, 5), "깔린 판이 많으면 덜 들어 올린다");
});
test("locate ↔ startOf: 임의의 순간이 그 이동의 [시작, 끝) 안 (원판 16 · 30개, 기둥 3 ~ 5, 두 빠르기)", () => {
  let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
  for (const [nn, pegs, sp] of [[16, 3, "x1"], [16, 3, "natural"], [30, 3, "x2"], [30, 3, "natural"], [30, 4, "natural"], [30, 5, "x4"], [30, 5, "natural"]]) {
    const TL = hanoiTimeline(nn, sp, pegs), last = pegs - 1;
    for (let i = 0; i < 2000; i++) {
      const tau = rnd() * TL.total, [s0, t0] = rnd() < 0.5 ? [0, last] : [last, 0];
      const st = TL.locate(tau, s0, t0);
      assert.ok(st.moving && st.start <= tau && tau < st.start + st.dur + 1e-6 * Math.max(1, tau), `${sp} τ=${tau}`);
      assert.ok(st.pos.every((p, d) => (d === st.disk ? p === -1 : p >= 0 && p < pegs)), "모든 판의 자리");
      const so = TL.startOf(st.m, s0, t0);
      near(so.start, st.start, 1e-6 * Math.max(1, st.start)); near(so.dur, st.dur, 1e-9);
      assert.ok(st.k >= 0 && st.k < 1 + 1e-9);
    }
  }
});

/* ── 3. 끝없이 돌기 · 빠르기 바꾸기 ── */
test("다 옮기면 쉬고(HOLD), 거꾸로 C → A, 또 쉬고 다시 A → C", () => {
  const TL = hanoiTimeline(5, "natural"), T = TL.total, Hd = HANOI.HOLD_MS;
  let st = hanoiAt(TL, 10);
  assert.equal(st.cycle, 0); assert.equal(st.src, 0); assert.equal(st.dst, 2); assert.equal(st.m, 1); assert.equal(st.hold, null);
  st = hanoiAt(TL, T + 100);
  assert.equal(st.hold, 100); assert.ok(!st.moving); assert.ok(st.pos.every((p) => p === 2));
  st = hanoiAt(TL, T + Hd + 10);
  assert.equal(st.cycle, 1); assert.equal(st.src, 2); assert.equal(st.dst, 0); assert.equal(st.m, 1); assert.equal(st.from, 2);
  st = hanoiAt(TL, 2 * T + Hd + 50);
  assert.ok(st.hold != null && st.pos.every((p) => p === 0), "두 바퀴째 끝은 A");
  st = hanoiAt(TL, 2 * (T + Hd) + 10);
  assert.equal(st.cycle, 2); assert.equal(st.src, 0);
  // 아주 오래 켜 둬도(30일) 바로 계산된다
  const big = hanoiTimeline(20, "x1");
  const far = hanoiAt(big, 30 * 86400e3);
  assert.ok(far.cycle >= 2 && (far.moving || far.hold != null));
  // 기둥 5개: 첫 기둥 A → 끝 기둥 E, 거꾸로 E → A
  const F = hanoiTimeline(7, "x2", 5);
  assert.equal(hanoiAt(F, 1).dst, 4);
  const h5 = hanoiAt(F, F.total + 10);
  assert.ok(h5.hold != null && h5.pos.every((p) => p === 4));
  const r5 = hanoiAt(F, F.total + HANOI.HOLD_MS + 10);
  assert.equal(r5.src, 4); assert.equal(r5.dst, 0); assert.equal(r5.from, 4);
});
test("빠르기를 바꾸면 같은 바퀴·같은 이동·같은 진행 비율에서 이어진다(기둥 3 · 4)", () => {
  const F = hanoiTimeline(9, "x1"), N = hanoiTimeline(9, "natural"), X4 = hanoiTimeline(9, "x4");
  const F4 = hanoiTimeline(12, "x2", 4), N4 = hanoiTimeline(12, "natural", 4);
  for (const [A, B] of [[F, N], [N, F], [N, X4], [X4, F], [F4, N4], [N4, F4]]) {
    for (const e of [0, 777, A.total * 0.31, A.total * 0.99, A.total + A.total * 0.5 + HANOI.HOLD_MS]) {
      const a = hanoiAt(A, e), b = hanoiAt(B, remapElapsed(A, B, e));
      assert.equal(b.cycle, a.cycle); assert.equal(b.m, a.m); assert.equal(b.src, a.src);
      if (a.moving) near(b.k, a.k, 1e-6);
    }
    // 쉬는 중에 바꾸면 새 시간표에서도 쉬는 중
    const h = hanoiAt(B, remapElapsed(A, B, A.total + 1500));
    assert.equal(h.hold, 1500);
  }
});

/* ── 4. 길과 배치 ── */
test("배치(원판 3~30 · 기둥 3~5): 판은 아래로 갈수록 넓고, 이웃 기둥의 판끼리 안 닿고, 다 쌓아도 기둥 끝이 남는다", () => {
  for (const pegs of HANOI.PEGS) for (let k = HANOI.MIN; k <= HANOI.MAX; k++) {
    const L = hanoiLayout(k, pegs), last = pegs - 1;
    assert.equal(L.X.length, pegs);
    near((L.X[0] + L.X[last]) / 2, 800, 1e-9);
    for (let d = 1; d < k; d++) assert.ok(L.widths[d] > L.widths[d - 1] + 6, `n=${k} 너비 차`);
    assert.ok(L.widths[k - 1] < L.SP - 20, `n=${k} 기둥 ${pegs} 큰 판이 기둥 사이보다 넓음`);
    assert.ok(k * L.h <= L.pegH - 40, `n=${k} 다 쌓으면 기둥 끝이 묻힘`);
    assert.ok(L.X[0] - L.widths[k - 1] / 2 > 800 - L.BOARD.half && L.X[last] + L.widths[k - 1] / 2 < 800 + L.BOARD.half, "판이 받침 밖");
    // 위: 가장 큰 판이 가장 높이 올라가도 조작 막대(무대 위 ~110px) 아래 · 아래: 받침 그림자가 안내 글자(872) 위
    const top = L.yClear - L.R - L.h - (L.widths[k - 1] / 2) * L.TILT;
    assert.ok(top >= 115, `n=${k} 위 ${top}`);
    assert.ok(L.yBase + L.BOARD.depth + L.BOARD.thick + L.BOARD.shadow <= 840, `n=${k} 아래`);
  }
});
test("길: 꿰인 동안은 곧게 위아래로만, 옆으로 갈 때는 모든 기둥 끝보다 위, 길이는 moveLen 과 같다(기둥 3 ~ 5)", () => {
  for (const [k, pegs] of [[3, 3], [9, 3], [20, 3], [30, 4], [12, 5], [30, 5]]) {
    const L = hanoiLayout(k, pegs);
    const pairs = [];
    for (let s = 0; s < pegs; s++) for (let t = 0; t < pegs; t++) if (s !== t) pairs.push([s, t]);
    for (const [s, t] of pairs) for (const [a, b] of [[0, 0], [k - 1, 0], [0, k - 1], [3 % k, 1]]) {
      const P = movePath(L, s, a, t, b, 24);
      assert.deepEqual(P[0], [L.X[s], levelY(L, a)]); assert.deepEqual(P.at(-1), [L.X[t], levelY(L, b)]);
      for (let i = 1; i < P.length; i++) {
        const [x0, y0] = P[i - 1], [x1, y1] = P[i];
        if (Math.abs(x1 - x0) > 1e-9) assert.ok(Math.max(y0, y1) <= L.yTip - L.LIFT + 1e-9, `옆으로 움직일 때 아랫면 y=${Math.max(y0, y1)} (기둥 끝 ${L.yTip})`);
      }
      near(polyLen(P), moveLen(L, s, a, t, b), moveLen(L, s, a, t, b) * 0.002);
      // pathPoint(정확한 길)도 같은 길 위: 끝점이 같고, 촘촘히 나눈 꺾은선 길이 = moveLen
      const Q = Array.from({ length: 801 }, (_, i) => pathPoint(L, s, a, t, b, i / 800));
      assert.deepEqual(Q[0], P[0]); near(Q[800][0], P.at(-1)[0], 1e-9); near(Q[800][1], P.at(-1)[1], 1e-9);
      near(polyLen(Q), moveLen(L, s, a, t, b), 2e-5 * moveLen(L, s, a, t, b));
      for (const [x, y] of Q) {   // 기둥에서 비켜난 점은 모두 기둥 끝보다 LIFT 위
        if (Math.abs(x - L.X[s]) > 1e-9 && Math.abs(x - L.X[t]) > 1e-9) assert.ok(y <= L.yTip - L.LIFT + 1e-9, `pathPoint 가 기둥 끝 아래로 옆걸음 y=${y}`);
      }
    }
  }
});
test("움직임의 진행: 0에서 시작해 MOTION 에서 1, 그 뒤는 쉼 · 줄곧 앞으로만 · 매끄럽게", () => {
  assert.equal(moveEase(0), 0); near(moveEase(HANOI.MOTION), 1, 1e-12); assert.equal(moveEase(0.99), 1);
  let prev = 0;
  for (let i = 1; i <= 2000; i++) {
    const k = i / 2000, v = moveEase(k);
    assert.ok(v >= prev - 1e-12, `k=${k}`);
    assert.ok(v - prev < 0.0025, `k=${k} 에서 튐 ${v - prev}`);
    prev = v;
  }
});
test("글자: 시간·쉼표·위 첨자", () => {
  assert.equal(fmtDur(16383e3), "4시간 33분 3초"); assert.equal(fmtDur(8191e3), "2시간 16분 31초");
  assert.equal(fmtDur(1048575e3), "12일 3시간 16분 15초"); assert.equal(fmtDur(7e3), "7초"); assert.equal(fmtDur(3600e3), "1시간");
  assert.equal(fmtDur(3605e3), "1시간 0분 5초"); assert.equal(fmtDur(0), "0초");
  assert.equal(fmtDur(31536000e3), "1년"); assert.equal(fmtDur((31536000 + 5) * 1e3), "1년 0일 0시간 0분 5초");
  assert.equal(fmtDur((2 ** 30 - 1) * 1e3), "34년 17일 13시간 37분 3초");
  assert.equal(comma(16383), "16,383"); assert.equal(comma(1048575), "1,048,575"); assert.equal(comma(7), "7");
  assert.equal(supNum(14), "¹⁴");
});

/* ── 4. 세트 ── */
test("세트: 세트 i 는 첫 세트보다 i × 늦음(배속은 한 번의 1/4, 자연스럽게는 0.42초) · 바로 전 이동을 준다", () => {
  for (const [sp, pegs] of [["x1", 3], ["x4", 4], ["natural", 5]]) {
    const TL = hanoiTimeline(9, sp, pegs), lag = staggerMs(sp);
    assert.equal(lag, sp === "natural" ? HANOI.STAGGER_NAT : fastMs(sp) * HANOI.STAGGER);
    for (const e of [0, 1234, 9876, TL.total * 0.4, TL.total + 500]) for (let i = 0; i < 5; i++) {
      const a = setAt(TL, e, i, sp), b = hanoiAt(TL, e - i * lag);
      assert.equal(a.m, b.m); assert.equal(a.cycle, b.cycle); assert.equal(a.set, i);
      if (a.moving) {
        assert.ok(a.prev, "앞 이동");
        if (a.m === 1) assert.deepEqual(a.prev, { to: a.src, toLv: TL.n - 1, disk: 0, start: null, dur: 0 });
        else {
          const p = TL.moveAt(a.m - 1, a.src, a.dst), so = TL.startOf(a.m - 1, a.src, a.dst);
          assert.deepEqual(a.prev, { to: p.to, toLv: p.toLv, disk: p.disk, start: so.start, dur: so.dur });
          near(so.start + so.dur, a.start, 1e-6 * Math.max(1, a.start));   // 앞 이동이 끝나면 바로 이번 이동
          // 앞 이동이 놓은 판은 지금도 그 자리(움직이는 판이 아니면)
          if (p.disk !== a.disk) { assert.equal(a.pos[p.disk], p.to); assert.equal(a.lv[p.disk], p.toLv); }
        }
        if (a.m === TL.moves) assert.equal(a.next, null);
        else {
          const q = TL.moveAt(a.m + 1, a.src, a.dst);
          assert.deepEqual([a.next.from, a.next.fromLv, a.next.disk], [q.from, q.fromLv, q.disk]);
          near(a.next.start, a.start + a.dur, 1e-6 * Math.max(1, a.start));
        }
      } else { assert.equal(a.prev, null); assert.equal(a.next, null); }
    }
  }
  // 첫 이동 · 마지막 이동은 늘 가장 작은 판(기둥 수와 상관없이) — 로봇이 쉬던 자리에서 바로 이어진다
  for (const pegs of HANOI.PEGS) for (const nn of [3, 7, 12]) {
    const TL = hanoiTimeline(nn, "x1", pegs);
    assert.equal(TL.moveAt(1).disk, 0); assert.equal(TL.moveAt(TL.moves).disk, 0);
    assert.equal(TL.moveAt(1, pegs - 1, 0).disk, 0); assert.equal(TL.moveAt(TL.moves, pegs - 1, 0).to, 0);
  }
});

/* ── 5. 그리기 훑기 ── */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "hanoi-test-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { HanoiArt, HanoiThumb, HanoiInfo, HanoiSets2D } from ${JSON.stringify(path.join(ROOT, "src/features/display/frames/hanoi.jsx"))};
import { PALETTE } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
import { hanoiTimeline, hanoiAt } from ${JSON.stringify(path.join(ROOT, "src/features/display/hanoi.js"))};
export const frame = (TL, e, th) => renderToStaticMarkup(<svg><HanoiArt L={TL.L} st={hanoiAt(TL, e)} C={PALETTE[th]} info={{ total: TL.total, speed: TL.speed, moves: TL.moves }} /></svg>);
export const sets = (TL, e, th, S) => renderToStaticMarkup(<svg><HanoiSets2D TL={TL} elapsed={e} sets={S} C={PALETTE[th]} speed={TL.speed} />
  <HanoiInfo L={TL.L} st={hanoiAt(TL, e)} C={PALETTE[th]} info={{ total: TL.total, speed: TL.speed, moves: TL.moves, pegs: TL.pegs, sets: S }} bannerY={128} /></svg>);
export const thumb = (th) => renderToStaticMarkup(<svg><HanoiThumb C={PALETTE[th]} TL={hanoiTimeline(5, "x1")} /></svg>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const bad = (s) => /NaN|undefined|Infinity/.test(s);
  for (const [k, pegs] of [[3, 3], [7, 3], [14, 3], [20, 3], [30, 3], [9, 4], [30, 4], [6, 5], [30, 5]]) {
    test(`그리기 훑기: 원판 ${k}개 · 기둥 ${pegs}개 — 두 빠르기·두 테마, 첫 바퀴·쉼·거꾸로, 오류·NaN 없음`, () => {
      for (const sp of ["x1", "natural"]) for (const th of ["dark", "light"]) {
        const TL = hanoiTimeline(k, sp, pegs), T = TL.total, Hd = HANOI.HOLD_MS;
        const times = [];
        for (let i = 0; i <= 160; i++) times.push((i / 160) * Math.min(T, 160 * 1000) * 0.999);   // 앞부분 촘촘히
        for (let i = 0; i <= 80; i++) times.push((i / 80) * T);                                    // 전체 고르게
        times.push(T + 1, T + Hd / 2, T + Hd - 1, T + Hd + 1, T + Hd + T / 2, 2 * T + Hd + 10, 7 * (T + Hd) + 123);
        for (const e of times) {
          const s = m.frame(TL, e, th);
          assert.ok(!bad(s), `${sp}/${th} e=${e}: ${(s.match(/.{40}(NaN|undefined|Infinity).{20}/) || [""])[0]}`);
        }
        // 쉬는 동안 안내, 옮기는 동안 남은 시간
        assert.ok(m.frame(TL, T + Hd / 2, th).includes("다 옮겼어요"));
        assert.ok(m.frame(TL, T / 3, th).includes("남은 시간"));
        assert.ok(m.frame(TL, T / 3, th).includes(`기둥 ${pegs}개`));
      }
    });
  }
  test("그리기 훑기: 세트 1 ~ 5개를 줄여 나란히 — 세트마다 하나씩, 안내에 세트 수 · 배속", () => {
    for (const S of HANOI.SETS) for (const [sp, pegs] of [["x2", 3], ["natural", 4], ["x4", 5]]) for (const th of ["dark", "light"]) {
      const TL = hanoiTimeline(8, sp, pegs);
      for (const e of [0, 777, TL.total * 0.5, TL.total + 1000, TL.total + HANOI.HOLD_MS + 50]) {
        const s = m.sets(TL, e, th, S);
        assert.ok(!bad(s), `S=${S} ${sp} e=${e}`);
        assert.equal((s.match(/<g transform="translate/g) || []).length, S > 1 ? S : 0);
        if (S > 1) assert.ok(s.includes(`세트 ${S}개`));
        if (sp !== "natural") assert.ok(s.includes(`1초에 ${sp.slice(1)}개`));
      }
    }
  });
  test("액자 목록의 작은 그림: 두 테마", () => {
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(!bad(s) && s.includes("<ellipse")); }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
