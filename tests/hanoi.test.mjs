// node tests/hanoi.test.mjs — 교실 모니터 액자 「하노이의 탑」 검산. 실패 시 exit 1.
//   1) 옮기는 순서: 모든 이동을 기둥 셋으로 따로 흉내 내며 규칙(맨 위 판만 · 큰 판은 작은 판 위에 못 놓음)과 최소 횟수 2ⁿ − 1 을 본다.
//      닫힌 식(움직이는 판 = m 의 끝자리 0 개수, 판 d 의 자리 = 방향 × ⌊(m + 2ᵈ)/2ᵈ⁺¹⌋)과도 맞춰 본다.
//   2) 시간: 빠르게 = 정확히 (2ⁿ − 1)초, 자연스럽게 = 이동마다 「지나간 길이 ÷ 빠르기」, 재귀로 센 합 = 하나씩 더한 합.
//   3) 길: 기둥에 꿰인 동안 옆으로 안 움직이고, 건널 때는 모든 기둥 끝보다 위. 그림이 무대(조작 막대·안내 글자 자리) 안.
//   4) 그리기 훑기: 원판 3·7·14·20 × 빠르기 2 × 테마 2 를 처음부터 끝·쉼·거꾸로까지 그려 오류·NaN 이 없는지.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import {
  HANOI, hanoiLayout, hanoiTimeline, hanoiAt, remapElapsed, moveLen, movePath, moveMs, moveEase, levelY, fmtDur, comma, supNum,
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
function* walk(n, s0, t0) {
  const TL = hanoiTimeline(n, "fast");
  const peg = [[], [], []];
  for (let d = n - 1; d >= 0; d--) peg[s0].push(d);
  for (let m = 1; m <= 2 ** n - 1; m++) {
    const { start, dur } = TL.startOf(m, s0, t0);
    const st = TL.locate(start + dur / 2, s0, t0);
    assert.ok(st.moving && st.m === m, `m=${m}: ${st.m}`);
    const { disk: d, from: s, to: t } = st;
    // 나머지 판의 자리가 흉내 낸 기둥과 같다
    for (let p = 0; p < 3; p++) peg[p].forEach((e, lv) => {
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

/* ── 2. 시간 ── */
test("빠르게: 다 옮기는 시간 = 정확히 (2ⁿ − 1)초 (n = 3 ~ 20)", () => {
  for (let k = HANOI.MIN; k <= HANOI.MAX; k++) {
    const TL = hanoiTimeline(k, "fast");
    assert.equal(TL.total, (2 ** k - 1) * 1000, `n=${k}`);
    assert.equal(TL.moves, 2 ** k - 1);
  }
});
test("빠르게: 13개 2시간 16분 31초 · 14개 4시간 33분 3초 — 3시간 넘는 가장 작은 수는 14", () => {
  assert.equal(fmtDur(hanoiTimeline(13, "fast").total), "2시간 16분 31초");
  assert.equal(fmtDur(hanoiTimeline(14, "fast").total), "4시간 33분 3초");
  assert.ok(hanoiTimeline(13, "fast").total < 3 * 3600e3 && hanoiTimeline(14, "fast").total >= 3 * 3600e3);
  assert.equal(HANOI.DEF, 14);
});
test("빠르게: 이동마다 1초, m 번째 이동은 (m − 1)초에 시작", () => {
  const TL = hanoiTimeline(10, "fast");
  for (const m of [1, 2, 3, 100, 511, 512, 1023]) { const s = TL.startOf(m); assert.equal(s.start, (m - 1) * 1000); assert.equal(s.dur, 1000); }
});
for (const k of [3, 8, 12]) {
  test(`자연스럽게(원판 ${k}개): 이동 시간 ∝ 지나간 길이, 재귀 합 = 하나씩 더한 합, 거울 방향도 같은 합`, () => {
    for (const [s0, t0] of [[0, 2], [2, 0]]) {
      const TL = hanoiTimeline(k, "natural");
      let sum = 0;
      const ratios = new Set();
      for (const mv of walk(k, s0, t0)) {
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
test("자연스럽게: 한 번 평균 1.6~2.0초(원판 7~20), 같은 판이라도 높이·거리에 따라 다르다", () => {
  for (const k of [7, 10, 14, 20]) {
    const TL = hanoiTimeline(k, "natural");
    const avg = TL.total / TL.moves / 1000;
    assert.ok(avg > 1.6 && avg < 2.0, `n=${k} 평균 ${avg}`);
  }
  const L = hanoiLayout(8);
  assert.ok(moveLen(L, 0, 0, 2, 0) > moveLen(L, 0, 0, 1, 0), "먼 기둥이 더 길다");
  assert.ok(moveLen(L, 0, 0, 1, 0) > moveLen(L, 0, 5, 1, 5), "깔린 판이 많으면 덜 들어 올린다");
});
test("locate ↔ startOf: 임의의 순간이 그 이동의 [시작, 끝) 안 (원판 16개, 두 빠르기)", () => {
  let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
  for (const sp of ["fast", "natural"]) {
    const TL = hanoiTimeline(16, sp);
    for (let i = 0; i < 3000; i++) {
      const tau = rnd() * TL.total, [s0, t0] = rnd() < 0.5 ? [0, 2] : [2, 0];
      const st = TL.locate(tau, s0, t0);
      assert.ok(st.moving && st.start <= tau && tau < st.start + st.dur + 1e-6, `${sp} τ=${tau}`);
      const so = TL.startOf(st.m, s0, t0);
      near(so.start, st.start, 1e-6); near(so.dur, st.dur, 1e-9);
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
  const big = hanoiTimeline(20, "fast");
  const far = hanoiAt(big, 30 * 86400e3);
  assert.ok(far.cycle >= 2 && (far.moving || far.hold != null));
});
test("빠르기를 바꾸면 같은 바퀴·같은 이동·같은 진행 비율에서 이어진다", () => {
  const F = hanoiTimeline(9, "fast"), N = hanoiTimeline(9, "natural");
  for (const [A, B] of [[F, N], [N, F]]) {
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
test("배치(원판 3~20): 판은 아래로 갈수록 넓고, 이웃 기둥의 판끼리 안 닿고, 다 쌓아도 기둥 끝이 남는다", () => {
  for (let k = HANOI.MIN; k <= HANOI.MAX; k++) {
    const L = hanoiLayout(k);
    for (let d = 1; d < k; d++) assert.ok(L.widths[d] > L.widths[d - 1] + 15, `n=${k} 너비 차`);
    assert.ok(L.widths[k - 1] < L.SP - 20, `n=${k} 큰 판이 기둥 사이보다 넓음`);
    assert.ok(k * L.h <= L.pegH - 40, `n=${k} 다 쌓으면 기둥 끝이 묻힘`);
    assert.ok(L.X[0] - L.widths[k - 1] / 2 > 800 - L.BOARD.half && L.X[2] + L.widths[k - 1] / 2 < 800 + L.BOARD.half, "판이 받침 밖");
    // 위: 가장 큰 판이 가장 높이 올라가도 조작 막대(무대 위 ~110px) 아래 · 아래: 받침 그림자가 안내 글자(872) 위
    const top = L.yClear - L.R - L.h - (L.widths[k - 1] / 2) * L.TILT;
    assert.ok(top >= 115, `n=${k} 위 ${top}`);
    assert.ok(L.yBase + L.BOARD.depth + L.BOARD.thick + L.BOARD.shadow <= 840, `n=${k} 아래`);
  }
});
test("길: 꿰인 동안은 곧게 위아래로만, 옆으로 갈 때는 모든 기둥 끝보다 위, 길이는 moveLen 과 같다", () => {
  for (const k of [3, 9, 20]) {
    const L = hanoiLayout(k);
    for (const [s, t] of [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]]) for (const [a, b] of [[0, 0], [k - 1, 0], [0, k - 1], [3 % k, 1]]) {
      const P = movePath(L, s, a, t, b, 24);
      assert.deepEqual(P[0], [L.X[s], levelY(L, a)]); assert.deepEqual(P.at(-1), [L.X[t], levelY(L, b)]);
      for (let i = 1; i < P.length; i++) {
        const [x0, y0] = P[i - 1], [x1, y1] = P[i];
        if (Math.abs(x1 - x0) > 1e-9) assert.ok(Math.max(y0, y1) <= L.yTip - L.LIFT + 1e-9, `옆으로 움직일 때 아랫면 y=${Math.max(y0, y1)} (기둥 끝 ${L.yTip})`);
      }
      near(polyLen(P), moveLen(L, s, a, t, b), moveLen(L, s, a, t, b) * 0.002);
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
  assert.equal(comma(16383), "16,383"); assert.equal(comma(1048575), "1,048,575"); assert.equal(comma(7), "7");
  assert.equal(supNum(14), "¹⁴");
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
import { HanoiArt, HanoiThumb } from ${JSON.stringify(path.join(ROOT, "src/features/display/frames/hanoi.jsx"))};
import { PALETTE } from ${JSON.stringify(path.join(ROOT, "src/features/display/draw.jsx"))};
import { hanoiTimeline, hanoiAt } from ${JSON.stringify(path.join(ROOT, "src/features/display/hanoi.js"))};
export const frame = (TL, e, th) => renderToStaticMarkup(<svg><HanoiArt L={TL.L} st={hanoiAt(TL, e)} C={PALETTE[th]} info={{ total: TL.total, speed: TL.speed }} /></svg>);
export const thumb = (th) => renderToStaticMarkup(<svg><HanoiThumb C={PALETTE[th]} TL={hanoiTimeline(5, "fast")} /></svg>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const bad = (s) => /NaN|undefined|Infinity/.test(s);
  for (const k of [3, 7, 14, 20]) {
    test(`그리기 훑기: 원판 ${k}개 — 두 빠르기·두 테마, 첫 바퀴·쉼·거꾸로, 오류·NaN 없음`, () => {
      for (const sp of ["fast", "natural"]) for (const th of ["dark", "light"]) {
        const TL = hanoiTimeline(k, sp), T = TL.total, Hd = HANOI.HOLD_MS;
        const times = [];
        for (let i = 0; i <= 400; i++) times.push((i / 400) * Math.min(T, 400 * 1000) * 0.999);   // 앞부분 촘촘히
        for (let i = 0; i <= 200; i++) times.push((i / 200) * T);                                 // 전체 고르게
        times.push(T + 1, T + Hd / 2, T + Hd - 1, T + Hd + 1, T + Hd + T / 2, 2 * T + Hd + 10, 7 * (T + Hd) + 123);
        for (const e of times) {
          const s = m.frame(TL, e, th);
          assert.ok(!bad(s), `${sp}/${th} e=${e}: ${(s.match(/.{40}(NaN|undefined|Infinity).{20}/) || [""])[0]}`);
        }
        // 쉬는 동안 안내, 옮기는 동안 남은 시간
        assert.ok(m.frame(TL, T + Hd / 2, th).includes("다 옮겼어요"));
        assert.ok(m.frame(TL, T / 3, th).includes("남은 시간"));
      }
    });
  }
  test("액자 목록의 작은 그림: 두 테마", () => {
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(!bad(s) && s.includes("<ellipse")); }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
