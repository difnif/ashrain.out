// 판서 모드 손바닥 거르기(src/pages/sets/palm.js) — node tests/board-palm.test.mjs
import assert from "node:assert/strict";
import { PalmGuard, toPage, toStage, hitStrokes } from "../src/pages/sets/palm.js";

let pass = 0;
const ok = (name, fn) => { fn(); pass++; console.log("✓", name); };
const PG = { l: 200, t: 20, r: 760, b: 812 };          // 쪽 상자(무대 px) — 가운데 480
const G = (cfg) => { const g = new PalmGuard(cfg); g.setPage(PG); return g; };
const T = (id, x, y, t, w = 8, h = 8) => ({ id, type: "touch", x, y, t, w, h });
const PEN = (id, x, y, t) => ({ id, type: "pen", x, y, t, w: 1, h: 1 });
const kinds = (acts) => acts.map((a) => a.k + (a.why ? ":" + a.why : ""));
const has = (acts, k, id) => acts.some((a) => a.k === k && (id == null || a.id === id));

ok("펜과 터치가 동시에 따로 그린다", () => {
  const g = G(); g.skipHint();
  assert.ok(has(g.down(PEN(1, 300, 200, 0)), "start", 1));
  assert.deepEqual(g.down(T(2, 650, 600, 5)), []);                  // 터치는 지연 확정 — 아직 안 그림
  assert.ok(has(g.move(PEN(1, 310, 205, 10)), "add", 1));
  const m = g.move(T(2, 655, 604, 80));                             // 70ms 지나 확정
  assert.ok(has(m, "start", 2) && m.find((a) => a.k === "start").src === "touch");
  assert.ok(has(g.move(T(2, 660, 608, 90)), "add", 2));
  assert.ok(has(g.up(PEN(1, 310, 205, 100)), "end", 1));
  assert.ok(has(g.up(T(2, 660, 608, 110)), "end", 2));
});

ok("손 받침 안내 → 오른쪽 단에 0.3초 대면 잠금, 잠긴 단에서 시작한 터치는 버림", () => {
  const g = G();
  assert.equal(g.phase, "hint");
  g.down(T(1, 640, 600, 0));
  assert.deepEqual(g.tick(200), []);
  const a = g.tick(320);
  assert.ok(a.some((x) => x.k === "phase" && x.phase === "locked" && x.col === "R"));
  g.up(T(1, 640, 600, 400));                                          // 손바닥이 들려도 잠금은 그대로
  assert.equal(g.phase, "locked");
  assert.ok(kinds(g.down(T(2, 600, 300, 500))).includes("reject:locked"));
  g.up(T(2, 600, 300, 520));
  g.down(T(3, 300, 300, 600));
  assert.ok(has(g.tick(680), "start", 3));                            // 왼쪽 단은 그대로 쓴다
});

ok("왼쪽 단에서 시작한 획은 잠긴 단으로 넘어가도 이어진다", () => {
  const g = G(); g.down(T(9, 650, 600, 0)); g.tick(400);             // 잠금 R
  g.down(T(1, 400, 300, 1000)); g.tick(1080);
  assert.ok(has(g.move(T(1, 560, 302, 1100)), "add", 1));
  assert.ok(has(g.move(T(1, 700, 305, 1120)), "add", 1));
});

ok("쪽 오른쪽 바깥에 0.3초 닿으면(손바닥이 쪽 밖으로 걸침) 잠금 해제", () => {
  const g = G(); g.down(T(9, 650, 600, 0)); g.tick(400); g.up(T(9, 650, 600, 450));
  g.down(T(5, 800, 500, 1000));                                       // 쪽 밖 오른쪽
  assert.equal(g.phase, "locked");
  const a = g.tick(1320);
  assert.ok(a.some((x) => x.k === "phase" && x.phase === "free"));
  // 쪽 밖에 놓인 손 근처의 새 터치는 버림
  assert.ok(kinds(g.down(T(6, 740, 520, 1400))).some((k) => k === "reject:rest-near" || k === "reject:edge"));
  g.up(T(6, 740, 520, 1410));
  g.down(T(7, 600, 200, 1500)); assert.ok(has(g.tick(1580), "start", 7)); // 오른쪽 단 위쪽에 쓴다
});

ok("왼쪽 바깥 접촉은 오른손 잠금을 풀지 않는다(다른 손으로 모니터를 잡은 경우)", () => {
  const g = G(); g.down(T(9, 650, 600, 0)); g.tick(400);
  g.down(T(5, 150, 500, 1000)); g.tick(1500);
  assert.equal(g.phase, "locked");
});

ok("왼손잡이 — 왼쪽 단에 손바닥을 대면 왼쪽 단을 잠근다", () => {
  const g = G({ hand: "L" });
  g.down(T(1, 300, 600, 0)); const a = g.tick(350);
  assert.ok(a.some((x) => x.k === "phase" && x.col === "L"));
  assert.ok(kinds(g.down(T(2, 300, 200, 500))).includes("reject:locked"));
});

ok("안내 단에서 움직이면 손바닥이 아니라 필기 — 바로 그린다", () => {
  const g = G();
  g.down(T(1, 600, 300, 0));
  const a = g.move(T(1, 640, 310, 40));
  assert.ok(has(a, "start", 1));
  assert.equal(g.phase, "hint");
});

ok("넓은 접촉(손바닥)은 버리고, 안내 중이면 그 단을 잠근다", () => {
  const g = G({ palmSize: 40 });
  const a = g.down(T(1, 650, 600, 0, 70, 55));
  assert.ok(kinds(a).includes("reject:size"));
  assert.ok(a.some((x) => x.k === "phase" && x.phase === "locked"));
  const g2 = G({ palmSize: 0 }); g2.skipHint();                     // 크기 규칙 끔
  g2.down(T(1, 300, 300, 0, 90, 90));
  assert.ok(has(g2.tick(80), "start", 1));
});

ok("펜 근처에서 새로 닿는 터치는 선생님 손바닥", () => {
  const g = G(); g.skipHint();
  g.down(PEN(1, 300, 300, 0));
  assert.ok(kinds(g.down(T(2, 400, 380, 20))).includes("reject:pen-near"));
  g.down(T(3, 650, 700, 30)); assert.ok(has(g.tick(110), "start", 3)); // 멀리는 학생
});

ok("펜이 떠 있기만 해도(호버) 근처 터치를 버린다", () => {
  const g = G(); g.skipHint();
  g.move({ id: 1, type: "pen", x: 300, y: 300, t: 0 });
  assert.ok(kinds(g.down(T(2, 330, 360, 200))).includes("reject:pen-near"));
  g.up(T(2, 330, 360, 210));
  g.down(T(3, 330, 360, 1000)); assert.ok(has(g.tick(1080), "start", 3)); // 펜을 안 본 지 오래 → 학생
});

ok("터치가 먼저 닿고 바로 옆에 펜이 닿으면, 먼저 닿은 터치(손바닥)를 거둔다", () => {
  const g = G(); g.skipHint();
  g.down(T(2, 330, 360, 0)); g.tick(80);                              // 확정돼 그리던 중
  const a = g.down(PEN(1, 300, 300, 120));
  assert.ok(has(a, "drop", 2) && has(a, "start", 1));
});

ok("지연 확정 중 가까이 또 닿으면 둘 다 손바닥", () => {
  const g = G(); g.skipHint();
  g.down(T(1, 300, 300, 0));
  const a = g.down(T(2, 360, 340, 30));
  assert.ok(kinds(a).includes("reject:two-touch") && kinds(a).includes("reject:one-writer"));
  assert.deepEqual(g.tick(200).filter((x) => x.k === "start"), []);
});

ok("터치 필기는 한 번에 하나", () => {
  const g = G(); g.skipHint();
  g.down(T(1, 300, 300, 0)); g.tick(80);
  assert.ok(kinds(g.down(T(2, 300, 700, 100))).includes("reject:one-writer"));
});

ok("가장자리 여백 — 손 쪽 · 아래 가장자리 바로 안쪽", () => {
  const g = G(); g.skipHint();
  assert.ok(kinds(g.down(T(1, 750, 300, 0))).includes("reject:edge"));
  assert.ok(kinds(g.down(T(2, 300, 805, 0))).includes("reject:edge"));
});

ok("해제 뒤 — 마지막 필기 지점의 아래 · 손 쪽 새 터치는 버림, 다음 줄 왼쪽은 산다", () => {
  const g = G(); g.skipHint();
  g.down(T(1, 300, 300, 0)); g.tick(80); g.move(T(1, 340, 300, 90)); g.up(T(1, 340, 300, 100));
  assert.ok(kinds(g.down(T(2, 400, 400, 300))).includes("reject:below"));
  g.up(T(2, 400, 400, 310));
  g.down(T(3, 260, 350, 400)); assert.ok(has(g.tick(480), "start", 3));
});

ok("새 쪽 · 손 받침 다시 → 안내부터", () => {
  const g = G(); g.down(T(9, 650, 600, 0)); g.tick(400);
  const a = g.rehint();
  assert.equal(g.phase, "hint");
  assert.ok(a.some((x) => x.k === "phase" && x.phase === "hint"));
});

ok("쪽 단위 ↔ 무대 좌표, 지우개 맞춤", () => {
  const [u, v] = toPage(PG, 793.7, 480, 416);
  const [x, y] = toStage(PG, 793.7, u, v);
  assert.ok(Math.abs(x - 480) < 0.2 && Math.abs(y - 416) < 0.2);
  const strokes = [{ w: 2, p: [10, 10, 50, 10] }, { w: 2, p: [10, 100, 50, 120] }];
  assert.deepEqual(hitStrokes(strokes, 30, 14, 5), [0]);
  assert.deepEqual(hitStrokes(strokes, 30, 60, 5), []);
});

console.log(`\n${pass}개 통과`);
