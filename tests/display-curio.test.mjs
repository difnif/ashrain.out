// node tests/display-curio.test.mjs — 수학 호기심 액자 일곱(축구 · 농구 · 야구 직선, 주머니 공 꺼내기, 알파벳 카드, 일렬로 세우기,
// 학년별 뽑기) 검산. 실패 시 exit 1.
//   직선: 모든 장면(축구 403 · 농구 893 · 야구 211)의 두 점이 화면에 쓴 식 위에 있는지 유리수로 다시 맞춘다.
//   주머니: 한 번 꺼내기의 확률을 공 하나하나를 구별해 모든 조합을 늘어놓아 센 값과 맞추고, 판 전체의 공 개수 · 누적 확률을 확인.
//   알파벳 카드: 사전식 목록 = 모든 순열을 직접 만들어 정렬한 것, 경우의 수 식 = 목록 길이, 낱말 표시는 사전에 있는 것만.
//   일렬로 세우기: 조건 조합 전부를 직접 늘어놓아 센 수 = 공식 = 화면의 식.
//   학년별 뽑기: 뽑힌 수 · 서로 다름 · 확률 = Π 1/C(인원, 뽑는 수).
//   그리기: 일곱 액자를 여러 순간 · 두 판(초등 · 중등) · 두 테마로 그려 오류 · NaN 이 없는지 훑는다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { lineOf, eqText, lineSteps, fs as fsx, frac, namesOf, comb, cycleAt } from "../src/features/display/curio/kit.js";
import { POUCH, fixPouch, setupOf, drawOnce, roundOf, pouchAt, PT, combExpr } from "../src/features/display/curio/pouch.js";
import { fixLexi, arrangements, countArr, setOf, lexiAt, countText } from "../src/features/display/curio/lexi.js";
import { LINE, fixLine, feasible, casesOf, countLine, strategyLines, okLine } from "../src/features/display/curio/lineup.js";
import { fixCrowd, crowdOf, pickOf, crowdLines, posOf } from "../src/features/display/curio/crowd.js";
import SOCCER from "../src/features/display/curio/data-soccer.js";
import NBA from "../src/features/display/curio/data-nba.js";
import MLB from "../src/features/display/curio/data-mlb.js";
import { DICT, SEEDS } from "../src/features/display/curio/data-dict.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
let n = 0, failed = 0;
async function test(name, fn) {
  n++;
  try { await fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

/* ── 유리수 ── */
const R = (a, b = 1) => { const [p, q] = frac(a, b); return [p, q]; };
const add = (x, y) => R(x[0] * y[1] + y[0] * x[1], x[1] * y[1]);
const mul = (x, y) => R(x[0] * y[0], x[1] * y[1]);
const eq = (x, y) => x[0] === y[0] && x[1] === y[1];
/** 식 글자를 다시 읽어 [기울기, 절편] — y = ax + b 꼴만 */
function parseEq(s) {
  const t = s.replace(/−/g, "-").replace(/\s+/g, "");
  const m = /^y=(-)?(?:\{(\d+)\/(\d+)\}|(\d+))?x(?:([+-])(?:\{(\d+)\/(\d+)\}|(\d+)))?$/.exec(t);
  if (!m) return null;
  let a = m[2] ? R(+m[2], +m[3]) : m[4] ? R(+m[4]) : R(1);
  if (m[1]) a = R(-a[0], a[1]);
  let b = R(0);
  if (m[5]) { b = m[6] ? R(+m[6], +m[7]) : R(+m[8]); if (m[5] === "-") b = R(-b[0], b[1]); }
  return { a, b };
}
function checkLine(p, q, label) {
  const L = lineOf(p, q);
  if (L.kind === "pt") return "pt";
  if (L.kind === "v") { assert.equal(eqText(L), `x = ${p[0] < 0 ? "−" + -p[0] : p[0]}`, label); return "v"; }
  const s = eqText(L);
  if (L.kind === "h") { assert.ok(/^y = /.test(s), label); assert.ok(eq(R(L.b[0], L.b[1]), R(p[1])), label); return "h"; }
  const E = parseEq(s);
  assert.ok(E, `${label}: 식을 못 읽음 ${s}`);
  for (const r of [p, q]) assert.ok(eq(add(mul(E.a, R(r[0])), E.b), R(r[1])), `${label}: ${s} 위에 ${r} 가 없다`);
  const st = lineSteps(p, q).lines;
  assert.equal(st[st.length - 1].s, s, `${label}: 판서 마지막 줄 = 식`);
  return "f";
}

await test("직선 · 식 글자: 무작위 정수 두 점 5,000쌍 — 두 점이 식 위, 판서 끝 줄 = 식, 세로선 · 가로선 · 같은 점 구분", () => {
  let seed = 7; const rnd = () => ((seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648);
  const kinds = {};
  for (let i = 0; i < 5000; i++) {
    const p = [Math.floor(rnd() * 41) - 20, Math.floor(rnd() * 41) - 20], q = [Math.floor(rnd() * 41) - 20, Math.floor(rnd() * 41) - 20];
    const k = checkLine(p, q, `${p}→${q}`); kinds[k] = (kinds[k] || 0) + 1;
  }
  assert.ok(kinds.f > 4000 && kinds.v > 0 && kinds.h > 0, JSON.stringify(kinds));
  assert.equal(eqText(lineOf([0, 0], [3, 3])), "y = x");
  assert.equal(eqText(lineOf([0, 0], [3, -3])), "y = −x");
  assert.equal(eqText(lineOf([-12, 5], [18, -10])), "y = −{1/2}x − 1");
  assert.equal(fsx(6, -4), "−{3/2}");
});

await test("축구: 6경기 장면 403개 — 모든 두 점이 식 위, 점수 흐름(골 장면) = 최종 점수, 시계 · 선수 이름 · 360 자리 있음", () => {
  let total = 0, f = 0, withFF = 0;
  for (const m of SOCCER.matches) {
    const goals = [0, 0], pens = [0, 0];
    for (const s of m.scenes) {
      total++;
      if (checkLine(s.a, s.b, `${m.title} ${s.m}' ${s.pl}`) === "f") f++;
      assert.ok(s.pl && !/[A-Za-z]{3}/.test(s.pl), `한글 이름: ${s.pl}`);
      assert.ok(Array.isArray(s.ff), "선수 자리"); if (s.ff.length >= 2) withFF++;
      if (s.k === "s" && s.g && s.p < 5) { goals[s.t]++; assert.equal(s.sa[s.t], s.sc[s.t] + 1); assert.equal(s.sa[1 - s.t], s.sc[1 - s.t]); }
      if (s.p === 5 && s.pe) { if (s.g) pens[s.t]++; assert.deepEqual(s.pe, pens); }
    }
    const last = m.scenes.filter((s) => s.p < 5).at(-1);
    const fin = last.sa || last.sc;
    // 자책골은 장면이 없어 점수표(sc)로만 반영된다 → 마지막 점수 ≤ 최종 점수
    assert.ok(fin[0] <= m.final[0] && fin[1] <= m.final[1], `${m.title}: ${fin} vs ${m.final}`);
    if (m.pens) assert.deepEqual(pens, m.pens, `${m.title} 승부차기`);
  }
  assert.equal(total, 403);
  assert.ok(f >= 370, `일차함수 장면 ${f}`);
  assert.ok(withFF / total > 0.85, `선수 자리 있는 장면 ${withFF}/${total}`);
});

await test("농구: 5경기 야투 893개 — 원점을 지나는 직선 식, 주인공 야투 기록(코비 28/46 · 클레이 16/25 · 커리 14/24 · 부커 21/40 · 돈치치 25/33)", () => {
  let total = 0;
  const want = [[28, 46], [16, 25], [14, 24], [21, 40], [25, 33]];
  NBA.games.forEach((g, gi) => {
    let mk = 0, at = 0;
    for (const s of g.shots) {
      total++;
      checkLine([0, 0], [s.X, s.Y], `${g.title} ${s.pl}`);
      const L = lineOf([0, 0], [s.X, s.Y]);
      if (L.kind === "f") assert.ok(eq(L.b, [0, 1]), "정비례: 절편 0");
      if (s.pl === g.star) { at++; mk += s.mk; }
    }
    assert.deepEqual([mk, at], want[gi], g.title);
  });
  assert.equal(total, 893);
});

await test("야구: 4경기 타구 211개 — 원점을 지나는 직선, 땅볼 송구 직선(1루 (90, 0)), 최종 점수(9:7 · 8:4 · 5:1 · 6:2)", () => {
  let total = 0, thr = 0;
  const fin = [[7, 9], [4, 8], [1, 5], [6, 2]];
  MLB.games.forEach((g, gi) => {
    for (const b of g.balls) {
      total++;
      checkLine([0, 0], [b.U, b.V], `${g.date} ${b.bat}`);
      if (b.th) { thr++; assert.deepEqual(b.th, [90, 0]); checkLine([b.U, b.V], b.th, `송구 ${b.bat}`); }
      assert.ok(b.U % 5 === 0 && b.V % 5 === 0);
    }
    assert.deepEqual(g.final, fin[gi]);
    assert.ok(MLB.parks[g.park].fence.length > 20);
  });
  assert.equal(total, 211);
  assert.ok(thr >= 40, `송구 ${thr}`);
});

await test("주머니: 한 번 꺼내기 확률 = 공을 하나하나 구별해 모든 조합을 늘어놓아 센 값(300판 × 여러 설정)", () => {
  const subsets = (arr, k) => { const out = []; const rec = (s, cur) => { if (cur.length === k) { out.push(cur.slice()); return; } for (let i = s; i < arr.length; i++) { cur.push(arr[i]); rec(i + 1, cur); cur.pop(); } }; rec(0, []); return out; };
  let checked = 0;
  for (const P0 of [{ n: 12, k: 2, b: 2, c: 3 }, { n: 15, k: 3, b: 3, c: 4 }, { n: 20, k: 1, b: 4, c: 5 }, { n: 18, k: 4, b: 2, c: 2 }, { n: 10, k: 2, b: 1, c: 6 }]) {
    for (let seed = 1; seed <= 60; seed++) {
      const P = fixPouch({ ...P0, seed });
      const bags = setupOf(P, 0);
      assert.equal(bags.flat().reduce((a, v) => a + v, 0), P.n, "공 수");
      bags.forEach((b) => assert.ok(b.reduce((a, v) => a + v, 0) >= P.k, "주머니마다 k개 이상"));
      let s = seed * 7919 >>> 0;
      const Rr = () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
      const d = drawOnce(bags.map((b) => b.slice()), P, Rr);
      const balls = d.before.flatMap((v, c) => Array(v).fill(c));
      const subs = subsets(balls.map((_, i) => i), P.k);
      const same = subs.filter((S) => { const kc = new Array(P.c).fill(0); S.forEach((i) => kc[balls[i]]++); return kc.every((v, c) => v === d.kc[c]); }).length;
      assert.equal(Number(d.fav), same, "경우의 수");
      assert.equal(Number(d.tot), subs.length, "전체");
      assert.equal(Number(d.num) * subs.length * d.elig.length, Number(d.den) * same, "확률 = 1/E × 같은 것/전체");
      checked++;
    }
  }
  assert.equal(checked, 300);
  assert.equal(combExpr(9, 3), "9 × 8 × 7 ÷ (3 × 2 × 1)");
  assert.equal(combExpr(7, 2), "7 × 6 ÷ 2");
});

await test("주머니: 판 전체 — 빼 두기는 꺼낸 공 + 남은 공 = 처음, 누적 확률 = 차례 확률의 곱 · 다시 넣기는 24차례 · 기대 개수 합 = 24k", () => {
  for (const rep of [false, true]) for (const [nn, k, b, c] of [[24, 2, 3, 4], [30, 3, 4, 5], [12, 1, 2, 2], [60, 4, 6, 6]]) for (let r = 0; r < 4; r++) {
    const P = fixPouch({ n: nn, k, b, c, rep, seed: 3 });
    const RD = roundOf(P, r);
    const drawn = RD.turns.reduce((a, T) => a + T.draw.length, 0);
    let pn = 1n, pd = 1n;
    for (const T of RD.turns) { pn *= T.num; pd *= T.den; }
    const last = RD.turns.at(-1);
    assert.equal(last.cum[0] * pd, last.cum[1] * pn, "누적 확률");
    if (!rep) {
      const left = last.after.flat().reduce((a, v) => a + v, 0);
      assert.equal(drawn + left, P.n);
      assert.ok(last.after.every((bg) => bg.reduce((a, v) => a + v, 0) < P.k), "더 꺼낼 주머니가 없을 때 끝");
    } else {
      assert.equal(RD.turns.length, POUCH.REP_TURNS);
      assert.ok(Math.abs(RD.expect.reduce((a, v) => a + v, 0) - POUCH.REP_TURNS * P.k) < 1e-9);
    }
  }
  // 시간 → 판 · 차례
  const P = fixPouch({ n: 24, k: 2, b: 3, c: 4, seed: 5 });
  const RD0 = roundOf(P, 0);
  const A = pouchAt(P, PT.SETUP + 2 * PT.TURN + 100);
  assert.equal(A.round, 0); assert.equal(A.stage, "turn"); assert.equal(A.ti, 2);
  const B = pouchAt(P, PT.SETUP + RD0.turns.length * PT.TURN + PT.SUM + 10);
  assert.equal(B.round, 1); assert.equal(B.stage, "setup");
});

await test("알파벳 카드: 사전식 목록 = 모든 순열을 만들어 정렬한 것(같은 글자 · 일부만 늘어놓기 포함), 경우의 수 식 = 목록 길이", () => {
  const permsAll = (arr, r) => { const out = new Set(); const rec = (cur, used) => { if (cur.length === r) { out.add(cur.join("")); return; } arr.forEach((c, i) => { if (!used[i]) { used[i] = 1; cur.push(c); rec(cur, used); cur.pop(); used[i] = 0; } }); }; rec([], []); return [...out].sort(); };
  for (const word of ["ABC", "LISTEN", "LETTER", "BANANA", "STARE", "PEPPER", "ABCDEFG"]) for (const r of [2, 3, word.length]) {
    if (r > word.length) continue;
    const cards = word.split("").sort();
    const A = arrangements(cards, r);
    const B = permsAll(cards, r);
    assert.deepEqual(A, B, `${word} r=${r}`);
    assert.deepEqual(arrangements(cards, r, true), B.slice().reverse());
    assert.equal(countArr(cards, r), B.length);
    const ct = countText(cards, r, "m");
    assert.ok(ct.includes(B.length.toLocaleString("en-US")), `${word} ${r}: ${ct}`);
  }
  // 식 글자: 5! · 같은 글자 나누기
  assert.equal(countText("ABCDE".split(""), 5, "m"), "5 × 4 × 3 × 2 × 1 = 120가지 (5!)");
  assert.equal(countText("EELRTT".split(""), 6, "e"), "6 × 5 × 4 × 3 × 2 × 1 ÷ (2 × 1) ÷ (2 × 1) = 180가지");
});

await test("알파벳 카드: 사전(낱말 3,600여 개) — 발음기호 · 뜻, 변화형은 원형이 사전에 있음 · 섞기용 낱말은 철자를 바꾼 다른 낱말이 있음 · 낱말 표시는 사전에 있는 것만", () => {
  const words = Object.keys(DICT);
  assert.ok(words.length > 3500, `${words.length}`);
  for (const w of words) {
    const e = DICT[w];
    assert.ok(/^\/.+\/$/.test(e[0]), `${w} 발음`);
    assert.ok(e[1] && e[1].length >= 2, `${w} 뜻`);
    if (e.length > 2) assert.ok(DICT[e[2]], `${w} → ${e[2]}`);
  }
  const key = (w) => w.split("").sort().join("");
  const groups = {};
  words.forEach((w) => { (groups[key(w)] ||= []).push(w); });
  for (const s of SEEDS) assert.ok(groups[key(s)].length >= 2, s);
  const P = fixLexi({ src: "mine", text: "LISTEN", rate: 4 });
  const S = setOf(P, 0, { DICT, SEEDS });
  assert.equal(S.list.length, 720);
  assert.deepEqual(S.words.map((w) => w.toLowerCase()).sort(), ["enlist", "inlets", "listen", "silent", "tinsel"].filter((w) => DICT[w]).sort());
  S.words.forEach((w) => assert.ok(DICT[w.toLowerCase()]));
  // 시각 → 배열: 낱말에서는 HOLD 만큼 더 머문다
  const i = S.list.indexOf("SILENT");
  const A = lexiAt(P, S.start[i] + 10, { DICT, SEEDS });
  assert.equal(A.set.list[A.i], "SILENT");
});

await test("일렬로 세우기: 모든 조건 조합(인원 3~8 · 이웃 · 양 끝 · 이웃하지 않음) — 직접 늘어놓아 센 수 = 공식 = 화면의 식, 사전식 순서", () => {
  let checked = 0;
  for (const nn of LINE.NS) for (const k of LINE.KS) for (const e of LINE.ES) for (const m of LINE.MS) {
    if (!feasible(nn, k, e, m)) continue;
    const P = fixLine({ n: nn, k, e, m, seed: 9 });
    assert.deepEqual([P.n, P.k, P.e, P.m], [nn, k, e, m]);
    const C = casesOf(P, 0);
    const f = countLine(nn, k, e, m);
    assert.equal(C.cases.length, f, `${nn},${k},${e},${m}`);
    assert.equal(strategyLines(P, C.who, "m").total, f);
    for (let i = 1; i < C.cases.length; i++) { const a = C.cases[i - 1], b = C.cases[i]; const j = a.findIndex((v, q) => v !== b[q]); assert.ok(j >= 0 && a[j] < b[j], "사전식"); }
    C.cases.forEach((c) => assert.ok(okLine(c, C.who, nn)));
    // 이름은 가나다순
    const ns = C.who.names.slice().sort((a, b) => a.localeCompare(b, "ko"));
    assert.deepEqual(C.who.names, ns);
    checked++;
  }
  assert.ok(checked >= 120, `${checked}`);
});

await test("학년별 뽑기: 뽑는 수 · 서로 다름 · 확률 = Π 1/C(인원, 뽑는 수) — 설정 여럿 × 차례 200", () => {
  for (const cfg of [{ a1: 12, a2: 10, a3: 8, r1: 1, r2: 2, r3: 1 }, { a1: 4, a2: 30, a3: 6, r1: 3, r2: 0, r3: 2 }, { a1: 20, a2: 18, a3: 16, r1: 1, r2: 1, r3: 1 }]) {
    const P = fixCrowd({ ...cfg, seed: 4 });
    const cr = crowdOf(P);
    assert.equal(cr.students.length, P.a1 + P.a2 + P.a3);
    assert.equal(new Set(cr.students.map((s) => s.name)).size, cr.students.length, "이름이 겹치지 않음");
    for (let k = 0; k < 200; k++) {
      const picks = pickOf(P, k, cr);
      for (const { g, list } of picks) {
        assert.equal(list.length, P[`r${g}`]);
        assert.equal(new Set(list).size, list.length);
        list.forEach((i) => assert.ok(i >= 0 && i < P[`a${g}`]));
      }
      const { total } = crowdLines(P, picks, cr, "m");
      assert.equal(total, [1, 2, 3].reduce((a, g) => a * comb(P[`a${g}`], P[`r${g}`]), 1));
    }
    for (const p of cr.people) { const q = posOf(p, 123456); assert.ok(q.x > 200 && q.x < 1340 && q.y > 150 && q.y < 760, `${q.x},${q.y}`); }
  }
  const names = namesOf(77, 60);
  assert.equal(new Set(names).size, 60);
  names.forEach((nm) => assert.notEqual(nm[0], nm[1], nm));
});

await test("시간: 같은 길이 장면 순환 · 빠르기", () => {
  const A = cycleAt(25500, 10000, 7);
  assert.deepEqual([A.k, A.i, A.t], [2, 2, 5500]);
  assert.deepEqual(cycleAt(75000, 10000, 7).i, 0);
});

/* ══════════ 그리기 ══════════ */
await test("그리기 훑기: 일곱 액자 × 여러 순간 × 초등 · 중등 × 두 테마 — 오류 · NaN 없음, 목록 그림 일곱", async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "curio-"));
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { SoccerArt, SC } from ${F("frames/soccerfn.jsx")};
import { HoopArt, HC, shotsOf } from ${F("frames/hoopfn.jsx")};
import { BatArt, BC } from ${F("frames/batfn.jsx")};
import { PouchArt } from ${F("frames/pouch.jsx")};
import { LexiArt } from ${F("frames/lexi.jsx")};
import { LineupArt } from ${F("frames/lineup.jsx")};
import { CrowdArt, crowdAt } from ${F("frames/crowd.jsx")};
import { CURIO_LABS, CurioThumb } from ${F("frames/curio.jsx")};
import { fixPouch, pouchAt } from ${F("curio/pouch.js")};
import { fixLexi, lexiAt } from ${F("curio/lexi.js")};
import { fixLine, lineAt } from ${F("curio/lineup.js")};
import { fixCrowd } from ${F("curio/crowd.js")};
import SOCCER from ${F("curio/data-soccer.js")};
import NBA from ${F("curio/data-nba.js")};
import MLB from ${F("curio/data-mlb.js")};
import { DICT, SEEDS } from ${F("curio/data-dict.js")};
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const keys = Object.keys(CURIO_LABS);
export const hoopList = (P) => shotsOf(NBA, P).map(({ s }) => [s.X, s.Y]);
export const thumb = (k, mode, th) => svg(<CurioThumb fkey={k} C={PALETTE[th]} mode={mode} />);
export function sweep(mode, th) {
  const C = PALETTE[th], out = [];
  const D = { DICT, SEEDS };
  for (const [i, t] of [[0, 0], [37, 1500], [120, 3500], [250, 5200], [402, 9600]]) out.push(svg(<SoccerArt C={C} mode={mode} P={{ match: -1, kind: "all", sp: 1 }} data={SOCCER} at={{ i, k: i, t }} />));
  const NH = shotsOf(NBA, { game: -1, who: "all" }).length;
  for (const [i, t] of [[0, 300], [45, 1800], [46, 5200], [98, 5200], [300, 2500], [600, 4200], [NH - 1, 7000]]) out.push(svg(<HoopArt C={C} mode={mode} P={{ game: -1, who: "all", sp: 1 }} data={NBA} at={{ i, k: i, t }} />));
  for (const [i, t] of [[0, 300], [12, 2000], [60, 4300], [150, 5100], [210, 8800]]) out.push(svg(<BatArt C={C} mode={mode} P={{ game: -1, sp: 1 }} data={MLB} at={{ i, k: i, t }} />));
  for (const cfg of [{ n: 24, k: 2, b: 3, c: 4 }, { n: 60, k: 4, b: 6, c: 6, rep: true }, { n: 6, k: 1, b: 1, c: 2 }]) {
    const P = fixPouch({ ...cfg, seed: 2 });
    for (const e of [0, 1500, 4000, 9000, 15000, 40000, 200000]) out.push(svg(<PouchArt C={C} mode={mode} P={P} at={pouchAt(P, e)} />));
  }
  for (const cfg of [{ src: "word", n: 5 }, { src: "abc", n: 8, r: 3 }, { src: "mine", text: "LISTEN", rate: 16 }]) {
    const P = fixLexi(cfg);
    for (const e of [0, 700, 5000, 60000, 400000]) out.push(svg(<LexiArt C={C} mode={mode} P={P} at={lexiAt(P, e, D)} D={D} />));
  }
  for (const cfg of [{ n: 5, k: 2 }, { n: 8, k: 3, e: 2 }, { n: 6, k: 2, e: 1, m: 2 }, { n: 3 }]) {
    const P = fixLine(cfg);
    for (const e of [0, 900, 12000, 47000, 400000]) out.push(svg(<LineupArt C={C} mode={mode} P={P} at={lineAt(P, e)} />));
  }
  for (const cfg of [{}, { a1: 30, a2: 30, a3: 30, r1: 3, r2: 2, r3: 3 }, { a1: 4, a2: 4, a3: 4, r1: 0, r2: 0, r3: 1 }]) {
    const P = fixCrowd({ ...cfg, seed: 5 });
    for (const e of [0, 1200, 3000, 5000, 7900, 100000]) out.push(svg(<CrowdArt C={C} mode={mode} P={P} at={crowdAt(P, e)} />));
  }
  return out;
}
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{60}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  assert.deepEqual(m.keys, ["soccerfn", "hoopfn", "batfn", "badminton", "tennis", "tabletennis", "volleyball", "jokgu", "sepak",
    "golf", "cue", "bowl", "pouch", "lexi", "lineup", "crowd"]);
  // 농구: 하프라인 너머에서 던진 슛은 반코트 그림 밖이라 목록에서만 빠진다(야투 기록에는 남는다)
  const hl = m.hoopList({ game: -1, who: "all" });
  assert.ok(hl.every(([X, Y]) => X >= -5.25 && X <= 41.25 && Math.abs(Y) <= 25), "반코트 밖 슛이 목록에 있음");
  assert.ok(hl.length >= 890 && hl.length < 893, `농구 목록 ${hl.length}`);
  let cnt = 0;
  for (const mode of ["e", "m"]) for (const th of ["dark", "light"]) {
    for (const k of m.keys) { const s = m.thumb(k, mode, th); assert.ok(s.length > 2000 && !BAD.test(s), `${k} ${mode}/${th}: ${bad(s)}`); cnt++; }
    for (const s of m.sweep(mode, th)) { assert.ok(s.length > 1500 && !BAD.test(s), `${mode}/${th}: ${bad(s)}`); cnt++; }
  }
  assert.ok(cnt > 300, `${cnt}`);
});

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
