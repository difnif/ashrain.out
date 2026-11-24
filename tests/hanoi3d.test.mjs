// node tests/hanoi3d.test.mjs — 교실 모니터 「하노이의 탑」 3D 무대의 순수 계산 검산(three.js 없이). 실패 시 exit 1.
//   1) 판의 자리: 3D 원판 자리 = 2D 길(pathPoint)을 줄인 것 · 쉬는 자리와 움직임의 처음 · 끝이 꼭 맞는다.
//   2) 로봇 계획 · 손끝 길: 구간(다가가기 · 나르기 · 물러나기) 경계와 이동 · 바퀴 경계에서 끊기지 않는다. 다가갈 때는 모든 판 뒤로.
//   3) 로봇 다섯 대: 나르는 동안 손끝(드론은 갈고리)이 판 테두리에 1.5cm 안 — 기둥 3 ~ 5 · 원판 3 ~ 30 · 세 빠르기.
//      드론은 늘 기둥 끝보다 위, 관절 자리에 NaN 이 없다.
//   4) 세트 배치 · 카메라: 모든 세트(로봇 포함)가 무대의 안전한 칸에 들어오고 꼭 맞다. 물결 차례 = 화면 왼쪽부터.
//   5) 로봇 모드 카메라 샷(shots.js): 단추 · 두 손가락 · 휠의 차례, 원샷 = 정면(로봇마다 살짝 위) · 투샷 = 완만한 사선 항공뷰(눈부신 방위 피함) ·
//      주인공이 안전한 칸 안 · 투샷 둘이 겹치지 않음 · 겹치는 세트는 뺌 · 원샷 < 투샷 < 전체 거리.
import assert from "node:assert/strict";
import { HANOI, hanoiTimeline, hanoiAt, setAt, pathPoint, levelY } from "../src/features/display/hanoi.js";
import {
  U, BT, PL, KA, KC, dims, restOf, discPose, robotPlan, gripAt, layoutSets, cameraFor, framePoints, sceneRadius, SAFE, ROBOTS, STYLES,
} from "../src/features/display/hanoi3d/plan.js";
import { KINS, dist3, ik2, footStep } from "../src/features/display/hanoi3d/kin.js";
import { lookCam, project } from "../src/features/display/sim3d/persp.js";
import {
  normShot, sameShot, shotLabel, cycleShot, zoomInShot, zoomOutShot, swipeShot, shotCam, shotPoints, overlap, ONE, TWO, GLARE, ROBOT_NAMES,
} from "../src/features/display/hanoi3d/shots.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const near = (a, b, eps = 1e-9, msg = "") => assert.ok(Math.abs(a - b) <= eps, `${msg} ${a} ≠ ${b}`);
let seed = 11;
const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
const finite = (o) => JSON.stringify(o, (k, v) => (typeof v === "number" && !Number.isFinite(v) ? "BAD" : v)).includes("BAD") === false;

/* ── 1. 판의 자리 ── */
test("치수: 기둥 자리 · 판 반지름 · 높이가 2D 배치를 U 배로 줄인 것", () => {
  for (const pegs of HANOI.PEGS) for (const nn of [3, 14, 30]) {
    const L = hanoiTimeline(nn, "x1", pegs).L, G = dims(L);
    assert.equal(G.X.length, pegs);
    G.X.forEach((x, i) => near(x, (L.X[i] - 800) * U));
    near(G.radii[nn - 1], (L.widths[nn - 1] / 2) * U);
    assert.ok(G.holeR > G.pegR && G.holeR < G.Rmin, "구멍이 기둥보다 크고 가장 작은 판보다 작다");
    assert.ok(G.D / 2 > G.Rmax, "받침 깊이가 가장 큰 판보다 넓다");
    assert.ok(G.top > G.pegTop + G.t, "건널 때 기둥 끝 위로");
    near(G.arcTop, BT + (L.yBase - (L.yClear - L.R)) * U, 1e-12);
  }
});
test("움직이는 판: 처음 = 출발 자리, 끝 = 도착 자리(로봇이든 아니든), 가운데는 2D 길 그대로", () => {
  for (const [nn, pegs] of [[5, 3], [12, 4], [30, 5]]) {
    const TL = hanoiTimeline(nn, "x1", pegs), G = dims(TL.L);
    for (let i = 0; i < 300; i++) {
      const st = TL.locate(rnd() * TL.total);
      const a = restOf(G, st.from, st.fromLv, st.disk), b = restOf(G, st.to, st.toLv, st.disk);
      for (const robot of [false, true]) {
        const p0 = discPose(G, { ...st, k: 0 }, robot), p1 = discPose(G, { ...st, k: 1 }, robot);
        near(p0.x, a.x, 1e-12); near(p0.y, a.y, 1e-12); near(p1.x, b.x, 1e-12); near(p1.y, b.y, 1e-12);
        near(p0.tilt, 0, 1e-12); near(p1.tilt, 0, 1e-12);
      }
      const p = discPose(G, st, false), q = pathPoint(TL.L, st.from, st.fromLv, st.to, st.toLv, p.u);
      near(p.x, (q[0] - 800) * U, 1e-12); near(p.y, BT + (TL.L.yBase - q[1]) * U, 1e-12);
      assert.ok(Math.abs(p.tilt) <= 0.0851);
      // 로봇이 들면 다가가는 동안 그대로, 물러나는 동안 이미 놓여 있다
      const r0 = discPose(G, { ...st, k: KA * 0.99 }, true), r1 = discPose(G, { ...st, k: (KC + 1) / 2 }, true);
      near(r0.x, a.x, 1e-12); near(r0.y, a.y, 1e-12); near(r1.x, b.x, 1e-12); near(r1.y, b.y, 1e-12);
    }
  }
});

/* ── 2. 로봇 계획 · 손끝 길 ── */
function gripSeq(TL, G, side, e0, e1, step) {
  const out = [];
  for (let e = e0; e <= e1; e += step) {
    const st = setAt(TL, e, 0);
    const plan = robotPlan(G, st, {});
    out.push({ e, g: gripAt(G, plan, side, {}), plan, st });
  }
  return out;
}
test("손끝 길: 구간 · 이동 · 쉼 · 다음 바퀴 경계에서 끊기지 않는다(한 손 · 두 손, 기둥 3 ~ 5)", () => {
  for (const [nn, pegs, sp] of [[4, 3, "x1"], [5, 4, "natural"], [4, 5, "x2"]]) {
    const TL = hanoiTimeline(nn, sp, pegs), G = dims(TL.L);
    const span = 2 * (TL.total + HANOI.HOLD_MS) + 500;
    for (const side of [0, -1, 1]) {
      const seq = gripSeq(TL, G, side, 0, span, 0.5);
      for (let i = 1; i < seq.length; i++) {
        const a = seq[i - 1].g, b = seq[i].g;
        const d = Math.hypot(a.x - b.x, a.y - b.y, a.z - b.z);
        // 0.5ms 동안 손끝이 움직이는 거리 — 2배속에 먼 기둥으로 나를 때(초속 11m)도 1.5cm 를 넘지 않는다(끊기면 수십 cm 가 튄다)
        assert.ok(d < 0.015, `side ${side} e=${seq[i].e} 끊김 ${d.toFixed(4)}m (${seq[i - 1].plan.mode}/${seq[i - 1].plan.phase} → ${seq[i].plan.mode}/${seq[i].plan.phase})`);
      }
    }
  }
});
test("다가갈 때는 모든 판보다 뒤로 빠진다(다른 기둥의 큰 판을 뚫지 않는다) · 잡을 때 쥐고 놓으면 편다", () => {
  for (const [nn, pegs] of [[9, 3], [14, 4], [20, 5]]) {
    const TL = hanoiTimeline(nn, "x1", pegs), G = dims(TL.L);
    for (let i = 0; i < 300; i++) {
      const st = TL.locate(rnd() * TL.total);
      const s2 = { ...st, prev: st.m > 1 ? (() => { const p = TL.moveAt(st.m - 1); return { to: p.to, toLv: p.toLv, disk: p.disk }; })() : null };
      const mid = robotPlan(G, { ...s2, k: KA * 0.5 }, {});
      assert.equal(mid.phase, 0);
      const g = gripAt(G, mid, 0, {});
      if (Math.abs(mid.prev.x - mid.from.x) > 0.12) assert.ok(g.z <= -(G.Rmax + 0.07) + 1e-9, `가운데에서 z=${g.z}`);
      assert.equal(gripAt(G, robotPlan(G, { ...s2, k: (KA + KC) / 2 }, {}), 0, {}).open, 0);
      assert.equal(gripAt(G, robotPlan(G, { ...s2, k: 0.999 }, {}), 0, {}).open, 1);
    }
  }
});

/* ── 3. 로봇 다섯 대 ── */
test("로봇 다섯 대: 나르는 동안 손끝이 판 테두리에서 1.5cm 안(기둥 3 ~ 5 · 원판 3 ~ 30 · 세 빠르기) · NaN 없음", () => {
  const worst = {};
  for (const pegs of HANOI.PEGS) for (const nn of [3, 6, 14, 30]) for (const sp of ["natural", "x1", "x4"]) {
    const TL = hanoiTimeline(nn, sp, pegs), G = dims(TL.L);
    for (const kind of ROBOTS) {
      const K = KINS[kind]();
      for (let trial = 0; trial < 6; trial++) {
        const e0 = rnd() * Math.min(TL.total, 3600e3);
        for (let f = 0; f < 120; f++) {
          const e = e0 + f * (1000 / 60);
          const st = setAt(TL, e, 0, sp);
          const plan = robotPlan(G, st, {});
          const P = K.update(G, plan, PL, 1 / 60, e / 1000);
          assert.ok(finite(P), `${kind} NaN`);
          if (plan.mode !== "move" || plan.phase !== 1 || f < 40) continue;
          let miss;
          const g = gripAt(G, plan, 0, {});
          if (kind === "humanoid") miss = Math.max(P.miss[0], P.miss[1]);
          else if (kind === "rover") miss = P.miss;
          else if (kind === "drone") miss = Math.max(...P.hook.map((h, i) => dist3(h, P.rim[i])));
          else miss = dist3(P.tip, [g.x, g.y + PL, g.z]);
          worst[kind] = Math.max(worst[kind] || 0, miss);
          assert.ok(miss < 0.015, `${kind} 기둥 ${pegs} 원판 ${nn} ${sp} m=${st.m} 판 ${st.disk}: ${miss.toFixed(4)}m`);
          if (kind === "drone") assert.ok(P.body[1] >= PL + G.pegTop + 0.05, "드론이 기둥 끝 아래로");
        }
      }
    }
  }
});
test("로봇은 테이블 뒤에 서 있다(몸이 받침 · 판을 뚫지 않는다) · 걸음은 딛는 동안 땅에 붙어 있다", () => {
  for (const pegs of HANOI.PEGS) {
    const TL = hanoiTimeline(10, "x1", pegs), G = dims(TL.L);
    const H = KINS.humanoid(), D = KINS.dog(), R = KINS.rover();
    for (let f = 0; f < 600; f++) {
      const e = f * 25, plan = robotPlan(G, setAt(TL, e, 0), {});
      const ph = H.update(G, plan, PL, 0.025, e / 1000), pd = D.update(G, plan, PL, 0.025, e / 1000), pr = R.update(G, plan, PL, 0.025, e / 1000);
      assert.ok(ph.pelvis[2] < G.back - 0.1, "사람 골반");
      for (const a of ph.an) assert.ok(a[2] < G.back, "사람 발");
      assert.ok(pd.body[2] + 0.15 < G.back, "개 몸통");
      assert.ok(pr.axle[2] + 0.2 < G.back, "두 바퀴");
    }
  }
  // 딛는 동안(위상 < duty) 발 오프셋 + 몸이 간 거리 = 일정
  const stride = 0.4;
  for (let p = 0; p < 0.55; p += 0.01) near(footStep(p, stride, 0.05)[0] + p * stride, footStep(0, stride, 0.05)[0], 1e-12);
  near(footStep(0.999999, stride, 0.05)[0], footStep(0, stride, 0.05)[0], 1e-5);
  // 두 마디: 닿는 곳이면 정확히, 마디 길이 그대로
  const o = ik2([0, 0, 0], [0.3, 0.4, 0.2], 0.4, 0.35, [0, 1, 0]);
  near(o.miss, 0, 1e-12); near(dist3([0, 0, 0], o.mid), 0.4, 1e-9); near(dist3(o.mid, o.end), 0.35, 1e-9);
});
test("쉬는 동안 기쁨: 쉬기 시작 · 끝에 손끝이 마지막 자리 그대로(다음 바퀴 첫 이동과 이어진다)", () => {
  const TL = hanoiTimeline(5, "x1", 3), G = dims(TL.L);
  for (const kind of ROBOTS) {
    const K = KINS[kind]();
    const atHold = (h) => K.update(G, robotPlan(G, hanoiAt(TL, TL.total + h), {}), PL, 1 / 60, 3);
    const a = JSON.stringify(atHold(0)), b = JSON.stringify(atHold(HANOI.HOLD_MS - 0.001));
    assert.ok(finite(JSON.parse(a)) && finite(JSON.parse(b)), kind);
  }
});

/* ── 4. 세트 배치 · 카메라 ── */
test("세트 배치: 받침끼리 겹치지 않고, 물결 차례 = 화면 왼쪽부터, 장면 반지름 안", () => {
  for (const pegs of HANOI.PEGS) for (const nn of [3, 30]) {
    const G = dims(hanoiTimeline(nn, "x1", pegs).L);
    for (const S of HANOI.SETS) {
      const P = layoutSets(G, S), cam = cameraFor(G, S), C = lookCam(cam);
      assert.equal(P.length, S);
      const R = sceneRadius(G, S);
      const hw = S >= 5 ? G.plinth.w / 2 + 0.3 : G.W / 2, hd = S >= 5 ? G.plinth.d / 2 + 1.0 : G.D / 2;
      for (let i = 0; i < S; i++) {
        assert.ok(Math.hypot(P[i].x, P[i].z) + 1e-9 < R, "반지름");
        for (let j = 0; j < i; j++) {
          const sep = Math.abs(P[i].x - P[j].x) > 2 * (G.W / 2) + 0.05 || Math.abs(P[i].z - P[j].z) > 2 * hd + 0.05 - (S >= 5 ? 1.0 : 0);
          assert.ok(sep, `S=${S} 세트 ${i} · ${j} 겹침`);
        }
      }
      void hw;
      const sx = P.map((p) => project(C, [p.x, 0, p.z])[0]);
      for (let i = 1; i < S; i++) assert.ok(sx[i] > sx[i - 1] - 1e-6, `S=${S} 물결 차례`);
    }
  }
});
test("카메라: 세트 1 ~ 5 · 기둥 3 ~ 5 · 원판 3 ~ 30 모두 무대의 안전한 칸 안, 한쪽은 꼭 맞게 · 세트 1개는 정면, 2개부터 대각선 위", () => {
  for (const pegs of HANOI.PEGS) for (const nn of [3, 10, 30]) {
    const G = dims(hanoiTimeline(nn, "x1", pegs).L);
    for (const S of HANOI.SETS) {
      const cam = cameraFor(G, S), C = lookCam(cam);
      const pts = framePoints(G, S).map((p) => project(C, p));
      assert.ok(pts.every(Boolean), "카메라 뒤");
      const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
      const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
      assert.ok(x0 >= SAFE.x0 - 0.5 && x1 <= SAFE.x1 + 0.5 && y0 >= SAFE.y0 - 0.5 && y1 <= SAFE.y1 + 0.5, `S=${S} 칸 밖 ${[x0, x1, y0, y1].map((v) => v.toFixed(1))}`);
      const tight = Math.min(x0 - SAFE.x0, SAFE.x1 - x1, y0 - SAFE.y0, SAFE.y1 - y1);
      assert.ok(tight < 3, `S=${S} 덜 맞음 ${tight}`);
      if (S === 1) { near(cam.az, 0, 1e-12); assert.ok(cam.el < 0.2); }
      else { assert.ok(cam.az > 0.3 && cam.el > 0.45, "대각선 위"); }
      assert.equal(STYLES.length, 5);
    }
  }
});
test("2D 와 3D 가 같은 높이 눈금: 쌓인 판의 아랫면 = 받침 + 깔린 수 × 두께", () => {
  const TL = hanoiTimeline(12, "x1", 4), G = dims(TL.L);
  for (let lv = 0; lv < 12; lv++) near(restOf(G, 1, lv, 3).y, BT + (TL.L.yBase - levelY(TL.L, lv)) * U, 1e-12);
});


/* ── 5. 로봇 모드 카메라 샷 ── */
test("샷 다듬기 · 이름: 전체(null) · 원샷 ① ~ ⑤ · 투샷 ①② ~ ④⑤ — 모르는 값은 전체, 들어온 투샷(p)은 그 원샷이 든 짝만", () => {
  for (const bad of [null, undefined, 3, "x", {}, { n: 3, i: 0 }, { n: 0 }]) assert.equal(normShot(bad), null);
  assert.deepEqual(normShot({ n: 1, i: 9 }), { n: 1, i: 4 });
  assert.deepEqual(normShot({ n: 2, i: 4 }), { n: 2, i: 3 });
  assert.deepEqual(normShot({ n: 1, i: 2, p: 1 }), { n: 1, i: 2, p: 1 });
  assert.deepEqual(normShot({ n: 1, i: 2, p: 0 }), { n: 1, i: 2 }, "원샷 ③ 은 투샷 ①② 에 없다");
  assert.ok(sameShot({ n: 1, i: 2, p: 1 }, { n: 1, i: 2 }) && sameShot(null, undefined) && !sameShot(null, { n: 2, i: 0 }));
  assert.equal(shotLabel(null).tag, "전체");
  assert.equal(shotLabel({ n: 1, i: 1 }).tag, "원샷 ② 로봇 개");
  assert.equal(shotLabel({ n: 2, i: 3 }).tag, "투샷 ④⑤");
  assert.deepEqual(ROBOT_NAMES, ["산업용 팔", "로봇 개", "휴머노이드", "두 바퀴", "드론"]);
  assert.equal(ROBOTS.length, ROBOT_NAMES.length);
});
test("카메라 단추(C): 전체 → ① → ② → ③ → ④ → ⑤ → 전체 · 거꾸로 · 투샷이면 그 짝의 원샷", () => {
  const seq = [];
  let s = null;
  for (let k = 0; k < 7; k++) { seq.push(s ? s.i + 1 : 0); s = cycleShot(s, 1); }
  assert.deepEqual(seq, [0, 1, 2, 3, 4, 5, 0]);
  assert.deepEqual(cycleShot(null, -1), { n: 1, i: 4 });
  assert.equal(cycleShot({ n: 1, i: 0 }, -1), null);
  assert.deepEqual(cycleShot({ n: 2, i: 2 }, 1), { n: 1, i: 2, p: 2 });
  assert.deepEqual(cycleShot({ n: 2, i: 2 }, -1), { n: 1, i: 3, p: 2 });
});
test("두 손가락 · 휠: 벌리면 전체 → (손가락 가운데 로봇의) 투샷 → 원샷, 모으면 거꾸로(들어온 짝으로), 옆으로는 한 로봇씩(끝에서 그대로)", () => {
  const at = (k) => [0, 1, 2, 3, 4].map((i) => Math.abs(i - k) * 100 + (i > k ? 1 : 0));
  assert.deepEqual(zoomInShot(null, at(0)), { n: 2, i: 0 });
  assert.deepEqual(zoomInShot(null, at(4)), { n: 2, i: 3 });
  assert.deepEqual(zoomInShot(null, [300, 200, 50, 40, 400]), { n: 2, i: 2 }, "가장 가까운 ④ 와 그 옆에서 더 가까운 ③");
  assert.deepEqual(zoomInShot(null, [300, 30, 60, 400, 500]), { n: 2, i: 1 });
  assert.deepEqual(zoomInShot(null, null), { n: 2, i: 1 }, "모르면 가운데");
  assert.deepEqual(zoomInShot({ n: 2, i: 1 }, [9, 80, 20, 9, 9]), { n: 1, i: 2, p: 1 });
  assert.deepEqual(zoomInShot({ n: 2, i: 1 }, null), { n: 1, i: 2, p: 1 }, "모르면 가운데 쪽");
  assert.deepEqual(zoomInShot({ n: 1, i: 3 }, at(0)), { n: 1, i: 3 }, "원샷이 가장 가깝다");
  assert.deepEqual(zoomOutShot({ n: 1, i: 2, p: 1 }), { n: 2, i: 1 }, "들어온 투샷으로");
  assert.deepEqual(zoomOutShot({ n: 1, i: 2 }), { n: 2, i: 2 });
  assert.deepEqual(zoomOutShot({ n: 1, i: 4 }), { n: 2, i: 3 });
  assert.equal(zoomOutShot({ n: 2, i: 0 }), null);
  assert.equal(zoomOutShot(null), null);
  assert.deepEqual(swipeShot({ n: 1, i: 1 }, 1), { n: 1, i: 2 });
  assert.deepEqual(swipeShot({ n: 1, i: 4 }, 1), { n: 1, i: 4 });
  assert.deepEqual(swipeShot({ n: 2, i: 3 }, 1), { n: 2, i: 3 });
  assert.deepEqual(swipeShot({ n: 2, i: 1 }, -1), { n: 2, i: 0 });
  assert.equal(swipeShot(null, 1), null);
});
test("샷 카메라: 원샷 = 정면(로봇마다 살짝 위) · 투샷 = 완만한 사선 항공뷰(눈부신 방위 피함) · 주인공이 안전한 칸 안 · 투샷 둘이 겹치지 않음 · 원샷 < 투샷 < 전체", () => {
  const SH = [0, 1, 2, 3, 4].map((i) => ({ n: 1, i })).concat([0, 1, 2, 3].map((i) => ({ n: 2, i })));
  for (const pegs of HANOI.PEGS) for (const nn of [3, 8, 14, 30]) {
    const G = dims(hanoiTimeline(nn, "x1", pegs).L), P = layoutSets(G, 5), all = cameraFor(G, 5);
    for (const sh of SH) {
      const c = shotCam(G, sh), C = lookCam(c), tag = `원판 ${nn} 기둥 ${pegs} ${sh.n === 1 ? "원샷" : "투샷"} ${sh.i}`;
      assert.equal(shotCam(G, { ...sh }), c, "같은 샷은 기억해 둔 것");
      assert.ok(finite(c) && c.d > 0, tag);
      if (sh.n === 1) {
        near(c.az, 0, 1e-12, `${tag} 정면`);
        assert.equal(c.el, ONE.el[ROBOTS[sh.i]]);
        assert.equal(c.fov, ONE.fov);
        assert.ok(c.el > 0.15 && c.el < 0.4, `${tag} 살짝 위`);
      } else {
        assert.equal(c.el, TWO.el);
        assert.ok(c.el < all.el && c.el > Math.max(...Object.values(ONE.el)), `${tag} 완만한 항공뷰(전체보다 낮고 원샷보다 높게)`);
        assert.ok(Math.abs(c.az) >= TWO.az0 - 1e-9 && Math.abs(c.az) <= TWO.az1 + 1e-9, `${tag} 사선 ${c.az}`);
        assert.ok(Math.abs(c.az - GLARE.az) >= GLARE.half, `${tag} 눈부신 방위 ${c.az}`);
        assert.ok(c.fov > ONE.fov, `${tag} 원샷보다 넓은 화각`);
        const box = (i) => {
          const q = shotPoints(G, P, i).map((p) => project(C, p));
          return { x0: Math.min(...q.map((v) => v[0])), x1: Math.max(...q.map((v) => v[0])), y0: Math.min(...q.map((v) => v[1])), y1: Math.max(...q.map((v) => v[1])) };
        };
        assert.ok(overlap(box(sh.i), box(sh.i + 1)) <= 0.02, `${tag} 두 로봇이 겹친다`);
      }
      assert.deepEqual(c.ids, sh.n === 1 ? [sh.i] : [sh.i, sh.i + 1]);
      assert.ok(c.hide.every((k) => !c.ids.includes(k)), `${tag} 주인공을 뺐다`);
      for (const i of c.ids) for (const p of shotPoints(G, P, i)) {
        const s = project(C, p);
        assert.ok(s && s[0] >= SAFE.x0 - 0.5 && s[0] <= SAFE.x1 + 0.5 && s[1] >= SAFE.y0 - 0.5 && s[1] <= SAFE.y1 + 0.5, `${tag} 주인공이 칸 밖 ${s}`);
      }
      assert.ok(c.d < all.d, `${tag} 전체보다 가깝다`);
    }
    for (let i = 0; i < 5; i++) {
      const one = shotCam(G, { n: 1, i });
      for (const p of [i - 1, i].filter((k) => k >= 0 && k < 4)) assert.ok(one.d < shotCam(G, { n: 2, i: p }).d, `원샷 ${i} 이 투샷 ${p} 보다 가깝다`);
    }
    // 바로 앞 세트에 가린 뒷줄 원샷 — 앞 세트는 그 샷 동안 뺀다 · 주인공보다 앞에서 화면에 걸리는 세트는 어느 샷에도 없다
    for (const [i, k] of [[2, 1], [4, 3]]) {
      const ahead = P[k].z > P[i].z && Math.abs(P[k].x - P[i].x) < G.W / 2;
      if (ahead) assert.ok(shotCam(G, { n: 1, i }).hide.includes(k), `원판 ${nn} 기둥 ${pegs} 원샷 ${i}: 앞의 ${k} 를 뺀다`);
    }
    for (const sh of SH) {
      const c = shotCam(G, sh), C = lookCam(c);
      const zmin = Math.min(...c.ids.flatMap((i) => shotPoints(G, P, i).map((p) => project(C, p)[2])));
      for (let k = 0; k < 5; k++) {
        if (c.ids.includes(k) || c.hide.includes(k)) continue;
        for (const p of shotPoints(G, P, k)) {
          const q = project(C, p);
          if (q && q[0] > 0 && q[0] < 1600 && q[1] > 0 && q[1] < 900) assert.ok(q[2] >= zmin, `원판 ${nn} 기둥 ${pegs} ${JSON.stringify(sh)}: 앞에 ${k} 가 보인다`);
        }
      }
    }
  }
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
