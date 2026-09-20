// node tests/photo.test.mjs — 촬영 모듈 순수 도우미 (src/lib/photoText.js)
import { tokenize, explain } from "../src/lib/marking.js";
import { findSpan, cutText, aggregateLights, titleOf, stripMarker } from "../src/lib/photoText.js";

let pass = 0, fail = 0;
const ok = (cond, name) => { if (cond) { pass++; console.log("ok   -", name); } else { fail++; console.log("FAIL -", name); } };
const eq = (a, b, name) => { const s = JSON.stringify(a) === JSON.stringify(b); if (!s) console.log("   got", JSON.stringify(a), "want", JSON.stringify(b)); ok(s, name); };
const rangeText = (tokens, sp) => tokens.slice(sp.t0, sp.t1 + 1).map((t) => t.text).join("");

const Q = "둘레가 54cm인 직사각형의 가로의 길이가 세로의 길이보다 3cm 길 때, 이 직사각형의 넓이를 구하시오.";
const tokens = tokenize(Q);

// findSpan — 그대로 · 띄어쓰기 다름 · 끝 조사 다름 · 못 찾음
{
  const a = findSpan(tokens, "둘레가 54cm");
  ok(a && rangeText(tokens, a) === "둘레가 54cm", "findSpan: 문구 그대로");
  const b = findSpan(tokens, "둘레가54cm인");
  ok(b && rangeText(tokens, b).replace(/\s/g, "") === "둘레가54cm인", "findSpan: 띄어쓰기 무시");
  const c = findSpan(tokens, "가로의 길이가 세로의 길이보다 3cm 길다");
  ok(c === null || rangeText(tokens, c).includes("3cm"), "findSpan: 어미가 다르면 못 찾거나(=null) 앞부분만");
  const d = findSpan(tokens, "직사각형의 넓이를");
  ok(d && rangeText(tokens, d).startsWith("직사각형의 넓이"), "findSpan: 끝 조사 떼고 찾기");
  eq(findSpan(tokens, "원의 반지름"), null, "findSpan: 없는 문구는 null");
  eq(findSpan(tokens, "가"), null, "findSpan: 한 글자는 null");
  eq(findSpan([], "둘레"), null, "findSpan: 토큰 없음");
}

// findSpan — 마커 안 수식도 찾는다
{
  const q2 = "일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.";
  const t2 = tokenize(q2);
  const s = findSpan(t2, "frac(x,2) - 3 = frac(x,4) - 1");
  ok(s && rangeText(t2, s).includes("frac(x,2)"), "findSpan: 마커 속 수식(마커 없이 물어도)");
}

// cutText — 빗금 자리에 ／
{
  const ex = explain(Q);
  const cut = cutText(ex.tokens, ex.marks);
  ok(cut.includes("／"), "cutText: 빗금이 들어간다");
  eq(cut.replace(/ ／ ?/g, (m, off) => (cut[off + m.length] === " " ? "" : " ")).replace(/  /g, " "), Q, "cutText: 빗금을 빼면 원문과 같다");
  ok(!/／\s*$/.test(cut), "cutText: 끝에 빗금이 남지 않는다");
  eq(cutText(tokens, []), Q, "cutText: 표시가 없으면 원문");
}

// aggregateLights — 평균 규칙
{
  const mk = (l) => ({ criteria: { 충실성: { light: l }, 논리성: { light: l }, 명료성: { light: l }, 간결성: { light: l }, 독창성: { light: l } } });
  eq(aggregateLights([mk("green")]).충실성.light, "green", "aggregate: 하나면 그대로(초록)");
  eq(aggregateLights([mk("red")]).논리성.light, "red", "aggregate: 하나면 그대로(빨강)");
  eq(aggregateLights([mk("green"), mk("green"), mk("yellow")]).명료성.light, "green", "aggregate: 초·초·노 → 초록");
  eq(aggregateLights([mk("green"), mk("yellow"), mk("yellow")]).간결성.light, "yellow", "aggregate: 초·노·노 → 노랑");
  eq(aggregateLights([mk("red"), mk("red"), mk("green")]).독창성.light, "red", "aggregate: 빨·빨·초 → 빨강");
  eq(aggregateLights([mk("green"), mk("green"), mk("red")]).독창성.light, "yellow", "aggregate: 초·초·빨 → 노랑");
  eq(aggregateLights([]).충실성, { light: null, why: "" }, "aggregate: 비면 null");
  eq(aggregateLights([{ criteria: { 충실성: { light: "purple" } } }]).충실성.light, null, "aggregate: 이상한 값은 무시");
}

// titleOf · stripMarker
{
  eq(titleOf("  [[frac(1,2)]] 을   더하시오 "), "frac(1,2) 을 더하시오", "titleOf: 마커·공백 정리");
  ok(titleOf("가".repeat(60)).length === 41, "titleOf: 40자 + …");
  eq(stripMarker("[[x]]"), "x", "stripMarker");
}

console.log(`\n${pass}/${pass + fail} passed`);
if (fail) process.exit(1);
