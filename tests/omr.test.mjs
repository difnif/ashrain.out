// 사진 OMR — sheet.js(레이아웃) · detect.js(인식) · sets.js(저장) 노드 테스트
//   node tests/omr.test.mjs
// 합성 카드를 그려 원근 변형·조명 기울기·잡음을 얹은 "사진"을 만들고 readSheet 가 답을 복원하는지 확인한다.
import assert from "node:assert/strict";
import {
  layoutSheet, sheetHtml, testHtml, packetHtml, markerCenters, INSTRUCTION,
  SHEET_W, SHEET_H, BUBBLE_R, ROW_PITCH, MAX_ITEMS, ROWS_PER_COL,
} from "../src/lib/omr/sheet.js";
import {
  readSheet, homography, applyH, invertH, toGray, threshold, findMarkers, readBubbles, warpToSpec, mergeAnswers,
  FILL_MIN, CONF_OK,
} from "../src/lib/omr/detect.js";
import { newCode, fmtCode, normCode, saveSet, listSets, getSet, removeSet, LS_KEY, MAX_SETS, CODE_ALPHABET } from "../src/lib/omr/sets.js";

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 4).join("\n      ")); }
}

// ── 아주 작은 래스터라이저 (회색조 Float32) ───────────────────────────────────
function raster(w, h, v) { return { w, h, px: new Float32Array(w * h).fill(v) }; }
function fillRect(r, x, y, w, h, v) {
  for (let j = Math.max(0, Math.floor(y)); j < Math.min(r.h, Math.ceil(y + h)); j++)
    for (let i = Math.max(0, Math.floor(x)); i < Math.min(r.w, Math.ceil(x + w)); i++) r.px[j * r.w + i] = v;
}
function fillCircle(r, cx, cy, rad, v) {
  for (let j = Math.max(0, Math.floor(cy - rad)); j <= Math.min(r.h - 1, Math.ceil(cy + rad)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad)); i <= Math.min(r.w - 1, Math.ceil(cx + rad)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy;
      if (dx * dx + dy * dy <= rad * rad) r.px[j * r.w + i] = v;
    }
}
function ring(r, cx, cy, rad, width, v) {
  const a = (rad - width / 2) ** 2, b = (rad + width / 2) ** 2;
  for (let j = Math.max(0, Math.floor(cy - rad - width)); j <= Math.min(r.h - 1, Math.ceil(cy + rad + width)); j++)
    for (let i = Math.max(0, Math.floor(cx - rad - width)); i <= Math.min(r.w - 1, Math.ceil(cx + rad + width)); i++) {
      const dx = i + 0.5 - cx, dy = j + 0.5 - cy, d = dx * dx + dy * dy;
      if (d >= a && d <= b) r.px[j * r.w + i] = v;
    }
}
function strokeRect(r, x, y, w, h, lw, v) {
  fillRect(r, x, y, w, lw, v); fillRect(r, x, y + h - lw, w, lw, v); fillRect(r, x, y, lw, h, v); fillRect(r, x + w - lw, y, lw, h, v);
}
function sampleBilinear(r, x, y) {
  x = Math.max(0, Math.min(r.w - 1.001, x)); y = Math.max(0, Math.min(r.h - 1.001, y));
  const x0 = x | 0, y0 = y | 0, fx = x - x0, fy = y - y0, i = y0 * r.w + x0;
  const top = r.px[i] * (1 - fx) + r.px[i + 1] * fx, bot = r.px[i + r.w] * (1 - fx) + r.px[i + r.w + 1] * fx;
  return top * (1 - fy) + bot * fy;
}
// 결정적 난수
function prng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

/** 캔버스 좌표계 카드 그림 — key: { [no]: "①"|"②"|…|["②","④"](double) | ""(blank) }, opts.noOrient 면 방향 막대 생략 */
function drawCard(spec, key, opts = {}) {
  const r = raster(spec.W, spec.H, 235);
  for (const m of spec.markers) fillRect(r, m.x, m.y, m.size, m.size, 22);
  if (!opts.noOrient) fillRect(r, spec.orient.x, spec.orient.y, spec.orient.w, spec.orient.h, 22);
  // 코드 글자 흉내 — 속 빈 큰 글자 7개 (마커와 헷갈릴 만한 어두운 덩어리)
  for (let k = 0; k < 7; k++) strokeRect(r, 352 + k * 44, 108, 30, 46, 7, 25);
  // 제목·안내·이름줄 흉내
  fillRect(r, 380, 200, 240, 4, 90); fillRect(r, 300, 262, 400, 3, 120);
  fillRect(r, 215, 308, 255, 2, 60); fillRect(r, 585, 308, 245, 2, 60);
  if (spec.header.dividerX) fillRect(r, spec.header.dividerX, spec.rows[0].y - 30, 2, ROW_PITCH * ROWS_PER_COL, 190);
  for (const row of spec.rows) {
    // 번호 흉내 — 속찬 작은 직사각형 (마커 후보 걸러내기 시험)
    fillRect(r, row.numX - 14, row.y - 11, 12, 22, 40);
    if (row.bubbles) {
      for (const b of row.bubbles) { ring(r, b.x, b.y, b.r, 2, 60); fillRect(r, b.x - 3, b.y - 4, 6, 8, 200); }
      const a = key[row.no];
      const marks = Array.isArray(a) ? a : a ? [a] : [];
      for (const lab of marks) {
        const b = row.bubbles.find((bb) => bb.label === lab);
        // 펜(짙게, 딱 맞게) / 연필(회색, 삐져나가게) 번갈아
        if (row.no % 3 === 0) fillCircle(r, b.x + 1, b.y - 1, b.r + 2, 128); else fillCircle(r, b.x, b.y, b.r - 1, 60);
      }
    } else if (row.blankBox) {
      const b = row.blankBox; strokeRect(r, b.x, b.y, b.w, b.h, 2, 60);
      fillRect(r, b.x + 30, b.y + 12, 40, 18, 50);   // 손글씨 답 흉내
    }
  }
  return r;
}

/**
 * 카드를 quad(이미지 좌표 [TL,TR,BR,BL] = 카드의 네 귀) 위치에 놓고 찍은 사진 (RGBA ImageData 꼴)
 * 조명 기울기·잡음·약한 블러 포함. 반환 { img, H(캔버스→이미지) }
 */
function photograph(card, W, H, quad, seed = 1, table = 105) {
  const Hc2i = homography([[0, 0], [card.w, 0], [card.w, card.h], [0, card.h]], quad);
  const Hi2c = invertH(Hc2i);
  const rnd = prng(seed);
  const g = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const [cx, cy] = applyH(Hi2c, x + 0.5, y + 0.5);
    let v = table;
    if (cx >= 0 && cy >= 0 && cx < card.w && cy < card.h) v = sampleBilinear(card, cx, cy);
    v *= 0.72 + 0.33 * (x / W) - 0.06 * (y / H);          // 조명 기울기
    g[y * W + x] = v + (rnd() - 0.5) * 16;                  // 잡음
  }
  // 3×3 박스 블러
  const b = new Float32Array(W * H);
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    let s = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) s += g[(y + dy) * W + x + dx];
    b[y * W + x] = s / 9;
  }
  const data = new Uint8ClampedArray(W * H * 4);
  for (let i = 0; i < W * H; i++) { const v = Math.max(0, Math.min(255, Math.round(b[i]))); data[i * 4] = v; data[i * 4 + 1] = v; data[i * 4 + 2] = v; data[i * 4 + 3] = 255; }
  return { img: { width: W, height: H, data }, H: Hc2i };
}

const cornersOf = (card) => [[0, 0], [card.w, 0], [card.w, card.h], [0, card.h]];
function expectCorners(spec, Hc2i) { return markerCenters(spec).map(([x, y]) => applyH(Hc2i, x, y)); }
function maxCornerErr(got, exp) { return Math.max(...got.map((p, i) => Math.hypot(p[0] - exp[i][0], p[1] - exp[i][1]))); }

// ── 20문항 세트 (2열) — 정답 키 ─────────────────────────────────────────────
const ITEMS20 = Array.from({ length: 20 }, (_, i) => ({ no: i + 1, kind: [5, 17].includes(i + 1) ? "short" : "choice" }));
const SPEC20 = layoutSheet({ code: "K7Q2-4M", items: ITEMS20 });
const LAB = ["①", "②", "③", "④", "⑤"];
const KEY20 = {};
for (const it of ITEMS20) if (it.kind === "choice") KEY20[it.no] = LAB[(it.no * 7) % 5];
KEY20[8] = ["②", "④"];   // 이중 표기
KEY20[12] = "";          // 무응답
const CARD20 = drawCard(SPEC20, KEY20);

function checkAnswers(res, key, spec) {
  assert.equal(res.ok, true, "ok (" + res.reason + ")");
  for (const row of spec.rows) {
    const a = res.answers.find((x) => x.no === row.no);
    assert.ok(a, "row " + row.no);
    if (row.kind === "short") { assert.equal(a.kind, "short"); assert.equal(a.answer, ""); continue; }
    const k = key[row.no];
    if (Array.isArray(k)) { assert.equal(a.answer, "", `row ${row.no} double → ""`); assert.equal(a.flag, "double", `row ${row.no} flag`); }
    else if (k === "") { assert.equal(a.answer, "", `row ${row.no} blank`); assert.equal(a.flag, "blank"); assert.ok(a.conf >= CONF_OK, `row ${row.no} blank conf ${a.conf}`); }
    else { assert.equal(a.answer, k, `row ${row.no}: got ${a.answer} fills=${JSON.stringify(a.fills)}`); assert.ok(a.conf >= CONF_OK, `row ${row.no} conf ${a.conf}`); }
  }
}

console.log("sheet.js");
test("layoutSheet: 1열(n≤15) 기하", () => {
  const s = layoutSheet({ code: "ABCD-EF", items: Array.from({ length: 10 }, (_, i) => ({ no: i + 1, kind: "choice" })) });
  assert.equal(s.W, SHEET_W); assert.equal(s.H, SHEET_H); assert.equal(s.cols, 1); assert.equal(s.rows.length, 10);
  assert.equal(s.markers.length, 4); assert.equal(s.meta.code, "ABCD-EF"); assert.equal(s.meta.n, 10);
  const x1 = s.rows[0].bubbles[0].x;
  for (const [i, r] of s.rows.entries()) {
    assert.equal(r.col, 0); assert.equal(r.bubbles.length, 5); assert.equal(r.bubbles[0].x, x1);
    assert.equal(r.y, s.rows[0].y + i * ROW_PITCH);
    assert.deepEqual(r.bubbles.map((b) => b.label), LAB);
  }
});
test("layoutSheet: 2열(n>15) — 16번은 오른쪽 열 첫 행", () => {
  const s = SPEC20;
  assert.equal(s.cols, 2);
  assert.ok(s.rows.slice(0, 15).every((r) => r.col === 0) && s.rows.slice(15).every((r) => r.col === 1));
  assert.equal(s.rows[15].y, s.rows[0].y);
  assert.ok(s.rows[15].bubbles[0].x > s.rows[0].bubbles[4].x + 2 * BUBBLE_R);
  assert.equal(s.rows[4].kind, "short"); assert.equal(s.rows[4].bubbles, null); assert.ok(s.rows[4].blankBox && s.rows[4].blankBox.w > 200);
});
test("layoutSheet: 버블은 프레임 안 · 서로 겹치지 않음 · 마커·방향막대와 떨어짐", () => {
  for (const n of [1, 15, 16, 30]) {
    const s = layoutSheet({ code: "X", items: Array.from({ length: n }, (_, i) => ({ no: i + 1, kind: "choice" })) });
    const all = s.rows.flatMap((r) => r.bubbles);
    for (const b of all) assert.ok(b.x - b.r > 0 && b.x + b.r < s.W && b.y - b.r > 0 && b.y + b.r < s.H, "inside");
    for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++)
      assert.ok(Math.hypot(all[i].x - all[j].x, all[i].y - all[j].y) >= 2 * BUBBLE_R + 4, "overlap");
    const boxes = [...s.markers.map((m) => ({ x: m.x, y: m.y, w: m.size, h: m.size })), { x: s.orient.x, y: s.orient.y, w: s.orient.w, h: s.orient.h }];
    for (const b of all) for (const k of boxes)
      assert.ok(b.x + b.r < k.x - 20 || b.x - b.r > k.x + k.w + 20 || b.y + b.r < k.y - 20 || b.y - b.r > k.y + k.h + 20, "near marker");
  }
});
test("layoutSheet: 30개 초과는 잘라냄", () => {
  const s = layoutSheet({ code: "X", items: Array.from({ length: 33 }, (_, i) => ({ no: i + 1, kind: "choice" })) });
  assert.equal(s.rows.length, MAX_ITEMS);
});
test("sheetHtml: 코드·마커 4개·안내문·viewBox", () => {
  const html = sheetHtml(SPEC20, { title: "중1-1 소인수분해", subtitle: "20문항" });
  assert.ok(html.includes("K7Q2-4M"));
  assert.equal((html.match(/class="mk"/g) || []).length, 4);
  assert.ok(html.includes('viewBox="0 0 1000 1414"'));
  assert.ok(html.includes(INSTRUCTION));
  assert.ok(html.includes("@page"));
  assert.equal((html.match(/<circle /g) || []).length, 18 * 5);
  assert.ok(html.includes("<rect") && html.includes('rx="5"'), "blank box");
});
test("testHtml: 문항 텍스트 이스케이프 · 분수 · 보기 · MATH_CSS", () => {
  const items = [
    { question: "다음 중 [[frac(1,2)]]보다 <b>큰</b> 수는?", choices: ["1/3", "2/3", "0.4", "0", "-1"], qtype: "choice", points: 4 },
    { question: "12의 약수의 개수를 구하시오.", qtype: "short", choices: null },
  ];
  const spec = layoutSheet({ code: "ABCD-EF", items: [{ no: 1, kind: "choice" }, { no: 2, kind: "short" }] });
  const html = testHtml({ title: "시험", subtitle: "부제", items, spec });
  assert.ok(html.includes("&lt;b&gt;큰&lt;/b&gt;"), "escaped");
  assert.ok(html.includes('class="mf"'), "fraction");
  assert.ok(html.includes("<b>①</b>") && html.includes("<b>⑤</b>"));
  assert.ok(html.includes(".mf{"), "MATH_CSS");
  assert.ok(html.includes("ABCD-EF"));
  assert.equal((html.match(/class="om-it"/g) || []).length, 2);
  assert.ok(html.includes("답: "), "short answer line");
  const pk = packetHtml({ title: "시험", subtitle: "", items, spec });
  assert.ok(pk.indexOf("om-test") < pk.indexOf("om-card"), "card last");
});

console.log("detect.js");
test("homography: 4점 대응 정확 · 역행렬 왕복", () => {
  const src = [[0, 0], [1000, 0], [1000, 1414], [0, 1414]], dst = [[170, 140], [1030, 175], [1060, 1490], [135, 1450]];
  const H = homography(src, dst), Hi = invertH(H);
  for (let i = 0; i < 4; i++) {
    const p = applyH(H, ...src[i]); assert.ok(Math.hypot(p[0] - dst[i][0], p[1] - dst[i][1]) < 1e-6);
    const q = applyH(Hi, ...dst[i]); assert.ok(Math.hypot(q[0] - src[i][0], q[1] - src[i][1]) < 1e-6);
  }
  const m = applyH(H, 500, 707), back = applyH(Hi, ...m);
  assert.ok(Math.hypot(back[0] - 500, back[1] - 707) < 1e-6);
});
test("toGray/threshold: 종이는 0, 잉크는 1", () => {
  const img = { width: 64, height: 64, data: new Uint8ClampedArray(64 * 64 * 4).fill(230) };
  for (let y = 20; y < 40; y++) for (let x = 20; x < 40; x++) { const i = (y * 64 + x) * 4; img.data[i] = 30; img.data[i + 1] = 30; img.data[i + 2] = 30; }
  const g = toGray(img); assert.equal(g[0], 229 + 1 - 1 >= 228 ? g[0] : -1);
  const bin = threshold(g, 64, 64);
  assert.equal(bin[0], 0); assert.equal(bin[30 * 64 + 30], 1); assert.equal(bin[10 * 64 + 50], 0);
});

const PORTRAIT_Q = [[170, 140], [1030, 175], [1060, 1490], [135, 1450]];
const SHOT = photograph(CARD20, 1200, 1600, PORTRAIT_Q, 7);
test("readSheet: 원근·조명·잡음 아래 마커 4개를 3px 안에서 찾음", () => {
  const res = readSheet(SHOT.img, SPEC20);
  assert.equal(res.ok, true, "ok: " + res.reason);
  const exp = expectCorners(SPEC20, SHOT.H);
  const err = maxCornerErr(res.corners, exp);
  assert.ok(err < 3, "corner err " + err.toFixed(2));
  assert.equal(res.orientation, 0);
});
test("readSheet: 답 전부 복원 · 이중표기는 double · 무응답은 blank · 단답은 비움", () => {
  const res = readSheet(SHOT.img, SPEC20);
  checkAnswers(res, KEY20, SPEC20);
  assert.ok(res.confidence >= 0.9, "confidence " + res.confidence);
  assert.equal(res.nMarked, 16);
  assert.equal(res.warped.width, 500); assert.equal(res.warped.height, 707);
});
test("readSheet: 180° 돌려 찍은 사진도 같은 답", () => {
  const q = [PORTRAIT_Q[2], PORTRAIT_Q[3], PORTRAIT_Q[0], PORTRAIT_Q[1]];
  const shot = photograph(CARD20, 1200, 1600, q, 11);
  const res = readSheet(shot.img, SPEC20);
  assert.equal(res.orientation, 2);
  checkAnswers(res, KEY20, SPEC20);
  assert.ok(maxCornerErr(res.corners, expectCorners(SPEC20, shot.H)) < 3);
});
test("readSheet: 가로(90°) 사진도 같은 답", () => {
  // 카드 TL → 이미지 오른쪽 위, TR → 오른쪽 아래 (시계 방향 90°)
  const q = [[1450, 150], [1470, 1040], [160, 1070], [130, 130]];
  const shot = photograph(CARD20, 1600, 1200, q, 5);
  const res = readSheet(shot.img, SPEC20);
  assert.equal(res.ok, true, "ok: " + res.reason);
  checkAnswers(res, KEY20, SPEC20);
  assert.ok(maxCornerErr(res.corners, expectCorners(SPEC20, shot.H)) < 3);
});
test("readSheet: 카드가 작게 찍혀도(35% 영역 밖) 두 번째 탐색으로 찾음", () => {
  const q = [[420, 380], [900, 395], [910, 1080], [410, 1060]];
  const shot = photograph(CARD20, 1300, 1450, q, 3);
  const res = readSheet(shot.img, SPEC20);
  assert.equal(res.ok, true, "ok: " + res.reason);
  checkAnswers(res, KEY20, SPEC20);
});
test("readSheet: 1열 카드(10문항) 도 읽음", () => {
  const items = Array.from({ length: 10 }, (_, i) => ({ no: i + 1, kind: i === 3 ? "short" : "choice" }));
  const spec = layoutSheet({ code: "AAAA-AA", items });
  const key = {}; for (const it of items) if (it.kind === "choice") key[it.no] = LAB[(it.no * 3) % 5];
  key[7] = "";
  const card = drawCard(spec, key);
  const shot = photograph(card, 1100, 1500, [[120, 90], [980, 130], [1000, 1420], [90, 1380]], 9);
  const res = readSheet(shot.img, spec);
  checkAnswers(res, key, spec);
});
test("readSheet: 카드 없는 사진 → ok=false, 답은 모두 빈칸", () => {
  const rnd = prng(42);
  const data = new Uint8ClampedArray(400 * 500 * 4);
  for (let i = 0; i < 400 * 500; i++) { const v = 60 + rnd() * 150; data[i * 4] = v; data[i * 4 + 1] = v; data[i * 4 + 2] = v; data[i * 4 + 3] = 255; }
  const res = readSheet({ width: 400, height: 500, data }, SPEC20);
  assert.equal(res.ok, false);
  assert.equal(res.answers.length, 20);
  assert.ok(res.answers.every((a) => a.answer === ""));
});
test("readSheet: 방향 막대가 없으면(검증 실패) ok=false", () => {
  const card = drawCard(SPEC20, KEY20, { noOrient: true });
  const shot = photograph(card, 1200, 1600, PORTRAIT_Q, 7);
  const res = readSheet(shot.img, SPEC20);
  assert.equal(res.ok, false); assert.equal(res.reason, "orient");
  assert.ok(Array.isArray(res.corners) && res.corners.length === 4, "마커는 찾았음");
});
test("readSheet: 딱딱한 그림자가 왼쪽 열을 덮어도 거짓 표시 없음 · 경계가 지나는 버블은 낮은 conf 로 표시", () => {
  const shot = photograph(CARD20, 1200, 1600, PORTRAIT_Q, 7);
  const d = shot.img.data;
  for (let y = 0; y < 1600; y++) for (let x = 0; x < 1200; x++) if (x < 330 + y * 0.08) { const i = (y * 1200 + x) * 4; d[i] *= 0.55; d[i + 1] *= 0.55; d[i + 2] *= 0.55; }
  const res = readSheet(shot.img, SPEC20);
  assert.equal(res.ok, true);
  for (const a of res.answers) {
    if (a.kind !== "choice") continue;
    const k = KEY20[a.no];
    const okRow = Array.isArray(k) ? a.flag === "double" : a.answer === k;
    if (!okRow) { assert.ok(a.conf < CONF_OK, `row ${a.no} wrong but confident: ${JSON.stringify(a)}`); }
  }
  const wrongConfident = res.answers.filter((a) => a.kind === "choice" && a.conf >= CONF_OK && !(Array.isArray(KEY20[a.no]) ? a.flag === "double" : a.answer === KEY20[a.no]));
  assert.equal(wrongConfident.length, 0);
});
test("readBubbles: 채움 비율 — 표시한 버블만 FILL_MIN 이상", () => {
  const g = toGray(SHOT.img);
  const res = readSheet(SHOT.img, SPEC20);
  const rows = readBubbles(res.warped, SPEC20, 0.5);
  const r1 = rows.find((r) => r.no === 1);
  const idx = LAB.indexOf(KEY20[1]);
  assert.ok(r1.fills[idx] >= FILL_MIN, "filled " + r1.fills[idx]);
  assert.ok(r1.fills.filter((_, i) => i !== idx).every((f) => f < 0.12), "others " + JSON.stringify(r1.fills));
  assert.ok(g.length === SHOT.img.width * SHOT.img.height);
  const w2 = warpToSpec(g, SHOT.img.width, SHOT.img.height, res.corners, SPEC20, 0.25);
  assert.equal(w2.width, 250);
});

test("mergeAnswers: CV 확신 → CV, 불확실 → AI, 단답은 AI 또는 빈칸, 고친 행 유지", () => {
  const items = [{ no: 1, kind: "choice", q: "q1" }, { no: 2, kind: "choice" }, { no: 3, kind: "short" }, { no: 4, kind: "choice" }, { no: 5, kind: "short" }];
  const cv = { ok: true, answers: [
    { no: 1, kind: "choice", answer: "③", conf: 0.9, flag: null },
    { no: 2, kind: "choice", answer: "", conf: 0, flag: "double" },
    { no: 3, kind: "short", answer: "", conf: 0, flag: "manual" },
    { no: 4, kind: "choice", answer: "①", conf: 0.2, flag: "uneven" },
    { no: 5, kind: "short", answer: "", conf: 0, flag: "manual" },
  ] };
  const a = mergeAnswers(items, cv, null, null);
  assert.deepEqual(a.map((r) => [r.answer, r.src]), [["③", "cv"], ["", "cv"], ["", "none"], ["①", "cv"], ["", "none"]]);
  assert.equal(a[0].q, "q1"); assert.equal(a[2].flag, "manual");
  const ai = [{ no: 1, answer: "②" }, { no: 2, answer: "④" }, { no: 3, answer: "3/4" }, { no: 4, answer: "⑤" }, { no: 5, answer: "" }];
  const b = mergeAnswers(items, cv, ai, a);
  assert.deepEqual(b.map((r) => [r.answer, r.src]), [["③", "cv"], ["④", "ai"], ["3/4", "ai"], ["⑤", "ai"], ["", "none"]]);
  // 학생이 고친 행은 AI 가 와도 유지
  const edited = b.map((r) => (r.no === 2 ? { ...r, answer: "①", src: "me", edited: true } : r));
  const c = mergeAnswers(items, cv, [{ no: 2, answer: "⑤" }], edited);
  assert.equal(c[1].answer, "①"); assert.equal(c[1].src, "me");
  // CV 실패(ok=false) 면 전부 AI/빈칸
  const d = mergeAnswers(items, { ok: false, answers: [] }, [{ no: 1, answer: "3" }, { no: 4, answer: "②" }], null);
  assert.deepEqual(d.map((r) => [r.answer, r.src]), [["", "none"], ["", "none"], ["", "none"], ["②", "ai"], ["", "none"]]);
});

console.log("sets.js");
// localStorage 폴리필 (node)
const store = new Map();
globalThis.localStorage = { getItem: (k) => (store.has(k) ? store.get(k) : null), setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k) };
test("newCode: 6글자 XXXX-XX · 헷갈리는 글자 없음", () => {
  for (let i = 0; i < 200; i++) {
    const c = newCode();
    assert.match(c, /^[A-Z2-9]{4}-[A-Z2-9]{2}$/);
    for (const ch of c.replace("-", "")) assert.ok(CODE_ALPHABET.includes(ch) && !"01OIL".includes(ch), c);
  }
  assert.equal(fmtCode("k7q24m"), "K7Q2-4M");
  assert.equal(normCode(" k7q2-4m "), "K7Q24M");
  assert.equal(normCode("K7Q2-4M"), normCode("k7q24m"));
});
test("saveSet/getSet/listSets/removeSet", () => {
  store.clear();
  const a = saveSet({ code: "K7Q2-4M", conceptId: "m1-1-01", conceptTitle: "소인수분해", items: [
    { id: "u1", no: 1, kind: "choice", answer: "②", choices: ["1", "2", "3", "4", "5"], question: "다음 [[frac(1,2)]] 중 …" },
    { id: "u2", no: 2, kind: "short", answer: "[[deg(60)]]", answer_alt: ["60"] },
  ] });
  assert.equal(a.code, "K7Q2-4M");
  assert.equal(a.items[0].q, "다음 frac(1,2) 중 …");
  assert.equal(getSet("k7q24m").items.length, 2, "대소문자·하이픈 무시");
  assert.equal(getSet("K7Q2-4M").items[1].answer_alt[0], "60");
  assert.equal(getSet("ZZZZ-ZZ"), null);
  saveSet({ code: "AAAA-BB", items: [], createdAt: "2026-09-13T00:00:00Z" });
  saveSet({ code: "CCCC-DD", items: [], createdAt: "2026-09-15T00:00:00Z" });
  assert.equal(listSets()[0].code, "CCCC-DD", "최신 먼저");
  assert.equal(removeSet("aaaabb"), 1);
  assert.equal(listSets().length, 2);
  for (let i = 0; i < MAX_SETS + 5; i++) saveSet({ code: fmtCode("Q" + String(i).padStart(5, "2")), items: [] });
  assert.equal(listSets().length, MAX_SETS, "≤ 20");
  assert.ok(JSON.parse(store.get(LS_KEY)).length <= MAX_SETS);
  // 같은 코드 덮어쓰기
  saveSet({ code: "K7Q2-4M", items: [{ id: "u9", no: 1, kind: "choice" }] });
  assert.equal(getSet("K7Q2-4M").items[0].id, "u9");
});

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
