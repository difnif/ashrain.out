// node tests/render0930.test.mjs — 09-30 렌더러 수정 검사 (틀 전수 검토 R1~R6)
//   R4 문자+숫자 아래첨자 변수 x1 → x₁ · R5 거듭제곱 밑 괄호 · R6 조합 문자 첨자 (mathir.js)
//   R1 히스토그램 · R2 축('O'·'y'·잘림) · R3 원기둥·원뿔 비율 (figsvg.js)
import assert from "node:assert/strict";
import { parse, toIR, disp, renderText, renderHtml, parseText } from "../src/lib/mathir.js";
import { figureToHtml1 } from "../src/lib/figsvg.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log("ok   -", name); }
  catch (e) { failed++; console.log("FAIL -", name); console.log("      " + String(e?.message || e).split("\n").join("\n      ")); }
}
const D = (src) => disp(parse(src)[0]);
const rt = (src) => { const ir = toIR(parse(src)[0]); assert.equal(toIR(parse(ir)[0]), ir, "왕복 " + src); return ir; };
const svg = (fg) => figureToHtml1(fg, { width: 320 }).html;
const texts = (h) => [...h.matchAll(/<text[^>]*>([^<]*)<\/text>/g)].map((m) => m[1]);

test("R4 문자 하나+숫자는 아래첨자 변수 (종전 x × 1)", () => {
  assert.equal(D("frac(m*x2 + n*x1, m + n)"), "(mx₂ + nx₁)/(m + n)");
  assert.equal(D("frac(S1, 1 − r)"), "S₁/(1 − r)");
  assert.equal(D("abs(a*x1 + b*y1 + c)"), "|ax₁ + by₁ + c|");
  assert.equal(D("a100 + a1"), "a₁₀₀ + a₁");
  assert.equal(D("x1' + f1(x)"), "x₁′ + f₁(x)");
  assert.equal(rt("frac(x1 + x2, 2)"), "frac(x1 + x2, 2)");
  assert.equal(D("x2.5"), "x × 2.5");                         // 소수는 그대로 곱
  assert.equal(D("tri(P1P2P3)"), "△P₁P₂P₃");                  // 라벨은 종전 그대로
  assert.equal(D("point3(1, 2, 3)"), "(1, 2, 3)");
  assert.equal(renderText("[[frac(S1, 1 − r)]]"), "S₁/(1 − r)");
  assert.equal(parseText("[[x1 + y1 = 3]]").errs.length, 0);
});

test("R5 거듭제곱 밑이 분수·근호·로그면 괄호, 삼각함수는 sin²x", () => {
  assert.equal(D("pow(frac(2,3), 4)"), "(2/3)⁴");
  assert.equal(D("pow(sqrt(6), 2)"), "(√6)²");
  assert.equal(D("sqrt(pow(6, 2))"), "√6²");                  // √(6²) 는 종전 그대로 — 이제 (√6)² 와 구별된다
  assert.equal(D("pow(root(3, 5), 6)"), "(³√5)⁶");
  assert.equal(D("pow(log(3, x), 2)"), "(log₃ x)²");
  assert.equal(D("pow(ln(x), 6)"), "(ln x)⁶");
  assert.equal(D("pow(sin(x), 2) + pow(cos(x), 2) = 1"), "sin² x + cos² x = 1");
  assert.equal(D("pow(sin(x), -1)"), "(sin x)⁻¹");           // sin⁻¹ 은 역함수 표기라 괄호
  assert.equal(D("pow(abs(vec(a) − vec(b)), 2)"), "|a⃗ − b⃗|²");   // 닫힌 모양은 괄호 없음
  assert.equal(D("pow(x, 2) − 4"), "x² − 4");
  assert.equal(D("3pow(frac(1,2), n)"), "3(1/2)^(n)");
  assert.ok(renderHtml("[[pow(frac(2,3), 4)]]").startsWith('(<span class="mf">'));
  rt("pow(frac(1 + i, 1 − i), 22)");
});

test("R6 조합·순열의 문자 인자는 아래첨자 (종전 nCr 평문)", () => {
  assert.equal(D("comb(n, r)"), "ₙCᵣ");
  assert.equal(D("comb(n + r − 1, r)"), "ₙ₊ᵣ₋₁Cᵣ");
  assert.equal(D("hcomb(n, r)"), "ₙHᵣ");
  assert.equal(D("comb(n, k)"), "ₙCₖ");
  assert.equal(D("comb(5, 2)"), "₅C₂");
  assert.equal(D("comb(b, 2)"), "bC2");                       // 유니코드 첨자가 없는 글자는 종전 그대로
  assert.equal(renderHtml("[[comb(n + r − 1, r)]]"), '<sub class="msb">n+r−1</sub>C<sub class="msb">r</sub>');
});

test("R1 히스토그램: 빈틈없는 직사각형·계급 경계 눈금·정수 세로 눈금·'도수(명)' 안 잘림", () => {
  const h = svg({ fn: "hist", args: { bins: ["40~50", "50~60", "60~70", "70~80", "80~90"], counts: [4, 12, 3, 9, 5], labels: "도수(명)" } });
  const rects = [...h.matchAll(/<rect data-k="bin:\d+" x="([\d.]+)" y="[\d.]+" width="([\d.]+)"/g)].map((m) => [Number(m[1]), Number(m[2])]);
  assert.equal(rects.length, 5);
  for (let i = 1; i < rects.length; i++) assert.ok(Math.abs(rects[i - 1][0] + rects[i - 1][1] - rects[i][0]) < 0.02, "막대 사이 빈틈");
  const ts = texts(h);
  for (const e of ["40", "50", "60", "70", "80", "90"]) assert.ok(ts.includes(e), "경계 눈금 " + e);
  for (const t of ["0", "2", "4", "6", "8", "10", "12", "14"]) assert.ok(ts.includes(t), "세로 눈금 " + t);
  assert.ok(!ts.some((t) => /^\d+\.\d+$/.test(t)), "소수 눈금 없음");
  const yl = /<text data-k="ylab" x="([\d.]+)" y="([\d.]+)"/.exec(h);
  assert.ok(yl && Number(yl[1]) >= 0 && Number(yl[2]) >= 10, "'도수(명)' 가 그림 안");
  // 계급을 못 읽으면 막대그래프로 — 그래도 정수 눈금
  const b = svg({ fn: "hist", args: { bins: ["A", "B", "C"], counts: [3, 7, 5] } });
  assert.ok(!texts(b).some((t) => /^\d+\.\d+$/.test(t)));
});

test("R2 축: 원점이 없으면 'O' 대신 생략 표시, 'y' 는 축 위 끝 위, 긴 세로 눈금값은 그림을 넓혀 안에", () => {
  const sc = svg({ fn: "scatter", args: { points: [[150, 40], [160, 52], [170, 61], [180, 70]], x_range: [140, 190], y_range: [30, 80] } });
  assert.ok(!texts(sc).includes("O"), "원점이 그림 밖이면 'O' 없음");
  assert.ok(sc.includes('data-k="axis-break"'), "생략 표시");
  const cp = svg({ fn: "coordplane", args: { x: [0, 30], y: [0, 1600], points: [{ name: "A", coord: [20, 1500] }] } });
  assert.ok(texts(cp).includes("O"));
  const vb = /viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"/.exec(cp);
  assert.ok(Number(vb[1]) < 0, "세 자리 이상 세로 눈금값 → 왼쪽으로 넓힘");
  assert.ok(!cp.includes("fig-pad"), "자리표 주석은 지운다");
  const y = /<text x="([\d.]+)" y="([\d.]+)" text-anchor="middle"[^>]*>y<\/text>/.exec(cp);
  assert.ok(y, "'y' 는 축 위 가운데");
  const small = svg({ fn: "coordplane", args: { x: [-5, 5], y: [-5, 5], points: [] } });
  assert.ok(/viewBox="0 /.test(small), "세로 눈금값이 짧으면 왼쪽은 넓히지 않는다");
});

test("R3 원기둥·원뿔은 반지름:높이 비율, 반구 반지름 선은 밑면 위", () => {
  const dims = (fg) => {
    const h = svg(fg);
    const e = /<ellipse data-k="top" cx="([\d.]+)" cy="([\d.]+)" rx="([\d.]+)"/.exec(h);
    const base = /<ellipse data-k="base" cx="[\d.]+" cy="([\d.]+)"/.exec(h);
    return { rx: Number(e[3]), h: Number(base[1]) - Number(e[2]) };
  };
  const a = dims({ fn: "solid", args: { kind: "cylinder", radius: 8, height: 17 } });
  const b = dims({ fn: "solid", args: { kind: "cylinder", radius: 2, height: 3 } });
  assert.ok(Math.abs(a.h / (2 * a.rx) - 17 / 16) < 0.02, "높이:지름 = 17:16");
  assert.ok(Math.abs(b.h / (2 * b.rx) - 3 / 4) < 0.02, "높이:지름 = 3:4");
  const c = dims({ fn: "solid", args: { kind: "cylinder", radius: "r = 3", height: "2r = 6" } });
  assert.ok(Math.abs(c.h / (2 * c.rx) - 1) < 0.02, "'r = 3'·'2r = 6' 라벨도 수로 읽음");
  const d = dims({ fn: "solid", args: { kind: "cylinder", radius: "r", height: 12 } });
  assert.equal(d.rx, 46);                                        // 한쪽이 문자면 종전 모양
  const hemi = svg({ fn: "solid", args: { kind: "hemisphere", radius: 6 } });
  const rl = /<line data-k="radius" x1="[\d.]+" y1="([\d.]+)"/.exec(hemi);
  assert.equal(Number(rl[1]), 95, "반구 반지름 선은 밑면 타원(가운데) 위");
});

console.log(`\n${n - failed}/${n} passed`);
if (failed) process.exit(1);
