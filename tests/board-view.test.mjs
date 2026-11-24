// 「문제지 그대로」 강사 모드 화면 다루기(src/pages/sets/boardview.js) — node tests/board-view.test.mjs
import assert from "node:assert/strict";
import { Gestures, stepZoom, clampZoom, zoomLabel, anchorScroll, pageAt, undoLast, ZOOM_STEPS } from "../src/pages/sets/boardview.js";

let pass = 0;
const ok = (name, fn) => { fn(); pass++; console.log("✓", name); };
const T = (id, x, y, t) => ({ id, x, y, t });

ok("한 손가락은 필기로 넘긴다(쓰기)", () => {
  const g = new Gestures();
  assert.deepEqual(g.down(T(1, 300, 300, 0), { fingers: "draw" }), { route: "guard", cancel: [] });
  assert.equal(g.move(T(1, 340, 310, 30)), null);
  assert.equal(g.up(T(1, 340, 310, 60)).route, "guard");
});

ok("두 손가락(막 닿은 첫 터치 + 떨어진 둘째) → 첫 터치를 돌려받고 확대 · 이동", () => {
  const g = new Gestures();
  g.down(T(1, 300, 300, 0), { fingers: "draw" });
  const d = g.down(T(2, 460, 300, 60), { fingers: "draw" });
  assert.deepEqual(d, { route: "gest", cancel: [1] });
  assert.ok(g.owns(1) && g.owns(2) && g.busy());
  assert.equal(g.move(T(2, 465, 300, 80)), null);                      // 활성 전(떨림)
  const v = g.move(T(2, 540, 300, 120));                                // 거리 160 → 240
  assert.equal(v.k, "view");
  assert.ok(Math.abs(v.s - 1.5) < 1e-9 && v.ox === 380 && v.oy === 300 && v.tx === 40 && v.ty === 0);
  const u = g.up(T(1, 300, 300, 200));
  assert.equal(u.route, "gest"); assert.equal(u.end.s, v.s);
  // 남은 손가락은 필기로 새지 않는다
  assert.equal(g.move(T(2, 560, 320, 220)), null);
  assert.equal(g.up(T(2, 560, 320, 240)).route, "ignore");
  assert.ok(!g.busy());
});

ok("이미 쓰던 첫 터치(움직였거나 늦게) 옆의 둘째는 필기 쪽으로(손바닥 거르기가 맡음)", () => {
  const g = new Gestures();
  g.down(T(1, 300, 300, 0), { fingers: "draw" });
  g.move(T(1, 330, 300, 40));                                           // 30px 움직임 = 쓰는 중
  assert.equal(g.down(T(2, 500, 320, 60), { fingers: "draw" }).route, "guard");
  const h = new Gestures();
  h.down(T(1, 300, 300, 0), { fingers: "draw" });
  assert.equal(h.down(T(2, 500, 320, 400), { fingers: "draw" }).route, "guard");   // 220ms 넘어 닿음
});

ok("손바닥 한 덩이(가까운 두 점)는 두 손가락이 아니다", () => {
  const g = new Gestures();
  g.down(T(1, 300, 300, 0), { fingers: "draw" });
  assert.equal(g.down(T(2, 318, 305, 20), { fingers: "draw" }).route, "guard");
});

ok("펜을 본 직후엔 화면 다루기를 시작하지 않는다(선생님 손바닥)", () => {
  const g = new Gestures();
  g.pen(1000);
  g.down(T(1, 300, 300, 1200), { fingers: "draw" });
  assert.equal(g.down(T(2, 480, 300, 1250), { fingers: "draw" }).route, "guard");
  const h = new Gestures();
  h.pen(0);
  h.down(T(1, 300, 300, 900), { fingers: "draw" });
  assert.equal(h.down(T(2, 480, 300, 950), { fingers: "draw" }).route, "gest");
});

ok("움직이지 않은 두 점 + 셋째 = 손바닥 + 쓰는 손가락 → 셋째는 필기, 두 점은 끝까지 무시", () => {
  const g = new Gestures();
  g.down(T(1, 600, 500, 0), { fingers: "draw" });
  g.down(T(2, 660, 540, 40), { fingers: "draw" });
  assert.equal(g.move(T(2, 662, 541, 60)), null);                       // 활성 전
  assert.deepEqual(g.down(T(3, 300, 300, 120), { fingers: "draw" }), { route: "guard", cancel: [] });
  assert.ok(!g.busy());
  assert.equal(g.move(T(1, 640, 560, 150)), null);
  assert.equal(g.up(T(1, 640, 560, 200)).route, "ignore");
  assert.equal(g.up(T(3, 340, 300, 220)).route, "guard");
});

ok("넘기기: 한 손가락은 이동(떨림 막기), 둘째가 오면 두 손가락 확대", () => {
  const g = new Gestures();
  assert.equal(g.down(T(1, 300, 300, 0), { fingers: "pan" }).route, "gest");
  assert.equal(g.move(T(1, 302, 301, 10)), null);
  assert.deepEqual(g.move(T(1, 300, 280, 20)), { k: "pan", dx: 0, dy: -20 });
  assert.deepEqual(g.move(T(1, 290, 260, 30)), { k: "pan", dx: -10, dy: -20 });
  assert.equal(g.down(T(2, 450, 260, 40), { fingers: "pan" }).route, "gest");
  const v = g.move(T(2, 610, 260, 60));
  assert.equal(v.k, "view"); assert.ok(v.s > 1.9);
  const u = g.up(T(2, 610, 260, 90));
  assert.ok(u.end && u.end.k === "view");
});

ok("확대 단계 · 범위 · 이름", () => {
  assert.deepEqual(ZOOM_STEPS, [1, 1.25, 1.5, 2, 2.5, 3]);
  assert.equal(stepZoom(1, 1), 1.25); assert.equal(stepZoom(1.3, 1), 1.5); assert.equal(stepZoom(1.3, -1), 1.25);
  assert.equal(stepZoom(3, 1), 3); assert.equal(stepZoom(1, -1), 1); assert.equal(stepZoom(2.2, -1), 2);
  assert.equal(clampZoom(0.4), 1); assert.equal(clampZoom(9), 3); assert.equal(clampZoom(NaN), 1);
  assert.equal(zoomLabel(1), "맞춤"); assert.equal(zoomLabel(1.5), "150%");
});

ok("확대 뒤 스크롤 보정 — 손가락 가운데 아래 내용이 제자리(+ 이동)에", () => {
  // 문서 상자가 화면 (0, 60)에 있고 배율 1.5 → 2.25(1.5배), 가운데 (400, 360)
  const r0 = { left: 0, top: 60 }, z0 = 1.5, z1 = 2.25;
  const ux = 400 / z0, uy = 300 / z0;                                   // 배율 1 기준 (266.7, 200)
  const r1 = { left: 0, top: 60 };                                      // 바꾼 직후(스크롤 그대로)
  const { dx, dy } = anchorScroll(r0, z0, r1, z1, 400, 360);
  assert.ok(Math.abs(dx - (ux * z1 - 400)) < 1e-9 && Math.abs(dy - (60 + uy * z1 - 360)) < 1e-9);
  // 보정 뒤: 그 내용이 다시 (400, 360)
  assert.ok(Math.abs((r1.left - dx) + ux * z1 - 400) < 1e-9 && Math.abs((r1.top - dy) + uy * z1 - 360) < 1e-9);
  const m = anchorScroll(r0, z0, r1, z0, 400, 360, 30, -20);            // 배율 그대로 · 30, −20 이동
  assert.ok(Math.abs(m.dx + 30) < 1e-9 && Math.abs(m.dy - 20) < 1e-9);
});

ok("쪽 찾기 · 되돌리기(사람마다)", () => {
  const rs = [{ t: 0, b: 1100 }, { t: 1120, b: 2220 }, { t: 2240, b: 3340 }];
  assert.equal(pageAt(rs, 500), 0); assert.equal(pageAt(rs, 1110), 0); assert.equal(pageAt(rs, 1115), 1);
  assert.equal(pageAt(rs, 5000), 2); assert.equal(pageAt(rs, -50), 0); assert.equal(pageAt([], 10), -1);
  const h = [{ src: "pen", pi: 0 }, { src: "touch", pi: 1 }, { src: "pen", pi: 2 }];
  assert.deepEqual(undoLast(h, "touch"), { src: "touch", pi: 1 });
  assert.deepEqual(undoLast(h, "pen"), { src: "pen", pi: 2 });
  assert.equal(h.length, 1); assert.equal(undoLast(h, "touch"), null);
});

console.log(`\n${pass}/${pass} 통과`);
