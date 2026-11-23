// node tests/display-concept-av.test.mjs — 개념 설명의 「움직이는 예시」(경우의 수와 확률 · 개념 12 · 13 · 14) 검산. 실패 시 exit 1.
// ① 붙이는 자리(src/lib/conceptAv.js)와 예시(src/features/display/concept-av.js)가 짝이 맞고, 「[[av:…]]」 글줄 · 기본 자리 규칙이 맞는지.
// ② 판서: 줄마다 「=」로 이은 계산식이 모두 같은 값이고(빨간 메모의 「= …」도), 답이 마지막 값과 같은지.
// ③ 그림이 판서와 같은 것을 세는지:
//    경우 카드(outwalk.js · frames/outfig.jsx) — 짚어 세는 카드 수 = 도장의 「n가지」, 고른 카드가 말한 것(짝수 · 소수 · 6 이하 · (앞, 앞) · (뒤, 뒤) · A = 6 …)과 같고,
//      묶음을 합친 수 · 분수 도장의 계산이 답과 같으며, 움직임이 그 판서 줄 시간 안에 차례로 돈다.
//    주머니 공(pickwalk.js) — 식의 수를 그림에 맞춰 뽑은 값 = 식의 값, 다시 넣기 · 안 넣기가 그대로.
//    한 줄 세우기(seatwalk.js) — 자리마다 후보 수 = 3, 2, 1.
// ④ 판: 넓은 판 · 좁은 판 모두 그림이 들어가고(배율 0.85 이상) 글자 칸과 겹치지 않으며 흐르지 않는다 · 잘라 쓴 판 안에 다 든다.
// ⑤ 그리기: 예시마다 여러 순간 × 두 판 × 두 테마 — 오류 · NaN 없음, 재생 카드(components/ConceptAv.jsx)도 그려진다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { CONCEPT_AV, AV_IDS, avMarker, avForBlock } from "../src/lib/conceptAv.js";
import { AV_EXAMPLES, AV_BY_ID } from "../src/features/display/concept-av.js";
import { l10Plan } from "../src/features/display/lin10.js";
import { outsTimes, selIds, outsCount } from "../src/features/display/outwalk.js";
import { pickPlan, evalTree } from "../src/features/display/pickwalk.js";
import { seatsPlan } from "../src/features/display/seatwalk.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

/* ══════════ 분수 ══════════ */
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const Q = (p, q = 1) => { if (q < 0) { p = -p; q = -q; } const g = gcd(p, q); return { n: p / g, d: q / g }; };
const add = (a, b) => Q(a.n * b.d + b.n * a.d, a.d * b.d);
const sub = (a, b) => Q(a.n * b.d - b.n * a.d, a.d * b.d);
const mul = (a, b) => Q(a.n * b.n, a.d * b.d);
const div = (a, b) => Q(a.n * b.d, a.d * b.n);
const same = (a, b) => a && b && a.n === b.n && a.d === b.d;
const show = (a) => (a ? (a.d === 1 ? `${a.n}` : `${a.n}/${a.d}`) : "∅");
/** 계산식이면 값, 아니면 null */
function calc(s) {
  const t = String(s).trim();
  if (!t || !/\d/.test(t) || !/^[\d{}/()+−×÷ ]+$/.test(t)) return null;
  const tk = [];
  for (let i = 0; i < t.length;) {
    const c = t[i];
    if (c === " ") { i++; continue; }
    if (c === "{") { const j = t.indexOf("}", i), [a, b] = t.slice(i + 1, j).split("/"); tk.push(Q(+a, +b)); i = j + 1; continue; }
    if (/\d/.test(c)) { let j = i; while (/\d/.test(t[j] || "")) j++; tk.push(Q(+t.slice(i, j))); i = j; continue; }
    tk.push(c); i++;
  }
  let p = 0;
  const atom = () => { const x = tk[p++]; if (x === "(") { const v = expr(); if (tk[p++] !== ")") throw 0; return v; } if (typeof x !== "object") throw 0; return x; };
  const term = () => { let v = atom(); while (tk[p] === "×" || tk[p] === "÷") { const o = tk[p++], r = atom(); v = o === "×" ? mul(v, r) : div(v, r); } return v; };
  const expr = () => { let v = term(); while (tk[p] === "+" || tk[p] === "−") { const o = tk[p++], r = term(); v = o === "+" ? add(v, r) : sub(v, r); } return v; };
  try { const v = expr(); return p === tk.length ? v : null; } catch { return null; }
}
/** 「=」 한 쪽에서 계산식 꼬리(앞의 말머리는 뗀다) */
const tail = (piece) => (piece.match(/[\d{}/()+−×÷ ]*$/) || [""])[0].replace(/^[\s)]*/, "");
/** 한 줄의 「=」 사슬 값들(계산식인 쪽만) */
const chain = (s) => String(s).split(" = ").map((x, i) => calc(i === 0 ? tail(x) : x)).filter(Boolean);
const nGa = (val) => { const m = String(val).match(/^(\d+)가지/); return m ? +m[1] : null; };

/* ══════════ ① 붙이는 자리 ══════════ */
test("붙이는 자리: 개념 12 · 13 · 14의 단락마다 예시 id — 모두 있는 예시 · 예시는 한 곳에만", () => {
  assert.deepEqual(Object.keys(CONCEPT_AV).sort(), ["m2-2-12", "m2-2-13", "m2-2-14"]);
  const seen = new Map();
  for (const [cid, m] of Object.entries(CONCEPT_AV)) {
    for (const [bid, ids] of Object.entries(m)) {
      assert.match(bid, /^b\d+$/, `${cid} ${bid}`);
      assert.ok(ids.length >= 1 && ids.length <= 3, `${cid} ${bid}: 예시 ${ids.length}개`);
      for (const id of ids) {
        assert.ok(AV_BY_ID.has(id), `${cid} ${bid}: 없는 예시 ${id}`);
        assert.ok(!seen.has(id), `${id}: ${seen.get(id)} 와 ${cid} ${bid} 두 곳`);
        seen.set(id, `${cid} ${bid}`);
      }
    }
  }
  for (const it of AV_EXAMPLES) assert.ok(seen.has(it.id), `붙지 않은 예시 ${it.id}`);
  assert.equal(AV_IDS.size, AV_EXAMPLES.length);
  assert.equal(new Set(AV_EXAMPLES.map((it) => it.id)).size, AV_EXAMPLES.length, "예시 id 겹침");
});

test("글줄 「[[av:…]]」: 아는 id 만 · 그 자리에 놓은 예시는 단락 끝(기본 자리)에 다시 놓지 않음", () => {
  assert.deepEqual(avMarker("[[av:c12-sum]]"), ["c12-sum"]);
  assert.deepEqual(avMarker(" [[av:c14-back, c14-noback]] "), ["c14-back", "c14-noback"]);
  assert.deepEqual(avMarker("[[av:c99-none]]"), []);
  assert.equal(avMarker("[[av:없는것]]"), null);
  assert.equal(avMarker("[[fig:c]]"), null);
  assert.equal(avMarker("글 [[av:c12-sum]]"), null);
  assert.equal(avMarker({ x: 1 }), null);
  assert.deepEqual(avForBlock("m2-2-13", { id: "b2", lines: ["글"] }), ["c13-prime", "c13-hh"]);
  assert.deepEqual(avForBlock("m2-2-13", { id: "b2", lines: ["[[av:c13-hh]]"] }), ["c13-prime"]);
  assert.deepEqual(avForBlock("m2-2-13", { id: "b2", panels: [{ lines: ["[[av:c13-prime]]"] }] }), ["c13-hh"]);
  assert.deepEqual(avForBlock("m2-2-13", { id: "b9", lines: [] }), []);
  assert.deepEqual(avForBlock("m1-1-01", { id: "b2" }), []);
  assert.deepEqual(avForBlock(undefined, { id: "b2" }), []);
});

test("예시 꼴: 해설 액자 문항과 같은 꼴(no 비움 · 문제 · 방침 · 포지티브 · 네거티브 · 식 · 답 · 그림) + 칩 · 머리 · 중2 낱말", () => {
  for (const it of AV_EXAMPLES) {
    assert.equal(it.no, "", it.id);
    assert.ok(it.q && it.plan && it.ans && it.tab && it.title, it.id);
    assert.equal(it.lines[0].pre, "포지티브", it.id);
    assert.equal(it.lines[1].pre, "네거티브", it.id);
    assert.ok(it.lines.length >= 4 && it.lines.length <= 7, `${it.id}: 판서 ${it.lines.length}줄`);
    assert.ok(["outs", "bag", "seats"].includes(it.fig?.kind), it.id);
    const all = [it.q, it.plan, it.title, it.tab, ...it.lines.flatMap((l) => [l.s, l.memo || ""])].join(" ");
    assert.ok(!/순열|조합|여사건|배반|\d!|√/.test(all), `${it.id}: 고등 낱말 · 기호 — ${all.match(/순열|조합|여사건|배반|\d!|√/)}`);
  }
});

/* ══════════ ② 판서 ══════════ */
test("판서: 줄마다 「=」 계산이 모두 같고 · 빨간 메모 「= …」도 · 답은 마지막 값", () => {
  let eqs = 0;
  for (const it of AV_EXAMPLES) {
    let last = null;
    for (const ln of it.lines) {
      const vs = chain(ln.s);
      for (let i = 1; i < vs.length; i++) { assert.ok(same(vs[i], vs[0]), `${it.id} 「${ln.s}」: ${show(vs[0])} ≠ ${show(vs[i])}`); eqs++; }
      if (ln.memo && ln.memo.startsWith("= ")) {
        const m = calc(ln.memo.slice(2));
        assert.ok(same(m, vs[vs.length - 1]), `${it.id} 메모 「${ln.memo}」 = ${show(m)} · 줄 값 ${show(vs[vs.length - 1])}`);
        eqs++;
      }
      if (vs.length) last = vs[vs.length - 1];
    }
    if (it.ans.includes(",")) continue;          // 「1, 0」(두 물음)은 줄마다 본다
    const a = calc(it.ans);
    assert.ok(same(a, last), `${it.id}: 답 ${it.ans} · 판서 마지막 ${show(last)}`);
  }
  console.log(`   「=」 ${eqs}개`);
});

/* ══════════ ③ 그림 ══════════ */
const OUTS = AV_EXAMPLES.filter((it) => it.fig.kind === "outs");
const dieOf = (it, ids) => ids.map((j) => it.fig.items[j].die);
const leafOf = (it, m) => { const n1 = it.fig.lv[1].opts.length; return [it.fig.lv[0].opts[Math.floor(m / n1)], it.fig.lv[1].opts[m % n1]]; };
const cellOf = (it, i) => [Math.floor(i / it.fig.cols.n) + 1, (i % it.fig.cols.n) + 1];

test("경우 카드: 짚어 센 카드 수 = 도장 「n가지」 · 분수 도장 계산이 맞고 답과 같음 · 묶음 합 = 답", () => {
  for (const it of OUTS) {
    const f = it.fig, N = outsCount(f);
    assert.ok(N > 0, it.id);
    let fracs = 0;
    for (const a of f.acts) {
      if (a.sel != null) {
        const ids = selIds(f, a.sel);
        assert.ok(ids.length > 0 || a.type === "scan", `${it.id} ${a.type}: 고른 카드 없음`);
        assert.equal(new Set(ids).size, ids.length, `${it.id}: 고른 카드 겹침`);
        const k = nGa(a.val);
        if (k != null) assert.equal(ids.length, k, `${it.id} ${a.type} 「${a.val}」: 카드 ${ids.length}장`);
        // 「{a/b}」 도장이면 a = 고른 카드 수, b = 모든 경우 수(같은 줄을 고른 칸이면 그 줄 안에서)
        const fr = String(a.val).match(/^\{(\d+)\/(\d+)\}/);
        if (fr && a.type === "count" && !a.keep && f.lay !== "grid") assert.deepEqual([+fr[1], +fr[2]], [ids.length, N], `${it.id} 「${a.val}」`);
      }
      if (a.type === "frac") {
        fracs++;
        const vs = chain(a.s);
        for (let i = 1; i < vs.length; i++) assert.ok(same(vs[i], vs[0]), `${it.id} 분수 도장 「${a.s}」`);
        assert.ok(same(vs[vs.length - 1], calc(it.ans)), `${it.id}: 분수 도장 ${a.s} · 답 ${it.ans}`);
        for (const k of a.from || []) assert.ok(f.acts[k] && f.acts[k].val, `${it.id}: 분수 도장이 모을 도장 ${k} 없음`);
      }
      if (a.type === "join") {
        const gs = f.acts.filter((b) => b.type === "count" && b.fly != null);
        assert.ok(gs.length >= 2, `${it.id}: 합칠 묶음`);
        const union = new Set(gs.flatMap((b) => selIds(f, b.sel)));
        assert.equal(union.size, gs.reduce((s, b) => s + selIds(f, b.sel).length, 0), `${it.id}: 묶음끼리 겹침(합의 법칙은 겹치지 않을 때)`);
        const v = String(a.val).split(" = ").pop();
        const want = calc(v) ?? Q(nGa(v));
        const got = /\{/.test(a.val) ? Q(union.size, N) : Q(union.size);
        assert.ok(same(want, got), `${it.id} 합친 도장 「${a.val}」: 카드 ${union.size}/${N}`);
        assert.ok(same(want, calc(it.ans)), `${it.id}: 합친 도장 · 답 ${it.ans}`);
      }
    }
    if (it.ans.includes("/") || it.ans.includes("{")) assert.ok(fracs || f.acts.some((a) => a.type === "join"), `${it.id}: 확률인데 분수 도장 · 합친 도장 없음`);
  }
});

test("경우 카드: 고른 카드가 판서가 말한 것과 같음(짝수 · 5 · 소수 · 6 이하 · 2 이하 · 6 · (앞, 앞) · (뒤, 뒤) · A = 6 · (6, 6) · 길 6갈래)", () => {
  const A = (id) => AV_BY_ID.get(id);
  const acts = (id, type) => A(id).fig.acts.filter((a) => a.type === type);
  const ids = (id, a) => selIds(A(id).fig, a.sel);
  // 12 합의 법칙 — 짝수 묶음 + 5 묶음
  const [ev, five] = acts("c12-sum", "count");
  assert.deepEqual(dieOf(A("c12-sum"), ids("c12-sum", ev)), [2, 4, 6]);
  assert.deepEqual(dieOf(A("c12-sum"), ids("c12-sum", five)), [5]);
  // 12 곱의 법칙 — 3갈래 × 2갈래 = 잎 6, 잎 이름이 모두 다르다
  const road = A("c12-road").fig;
  assert.equal(road.lv[0].opts.length * road.lv[1].opts.length, 6);
  assert.deepEqual(acts("c12-road", "grow").map((a) => a.lv), [0, 1]);
  assert.equal(acts("c12-road", "trace").length, 1);
  // 13 확률 — 모든 경우 6, 소수 2 · 3 · 5
  const [all6, pr] = acts("c13-prime", "count");
  assert.deepEqual(dieOf(A("c13-prime"), ids("c13-prime", all6)), [1, 2, 3, 4, 5, 6]);
  assert.deepEqual(dieOf(A("c13-prime"), ids("c13-prime", pr)), [2, 3, 5]);
  // 13 동전 2개 — 잎 4개, 모두 앞면은 (앞, 앞) 하나
  const hh = acts("c13-hh", "count")[0];
  assert.deepEqual(ids("c13-hh", hh).map((m) => leafOf(A("c13-hh"), m)), [["앞", "앞"]]);
  // 13 성질 — 6 이하는 6장 모두, 7은 없음(scan)
  assert.deepEqual(dieOf(A("c13-sure"), ids("c13-sure", acts("c13-sure", "count")[0])), [1, 2, 3, 4, 5, 6]);
  assert.equal(acts("c13-sure", "scan").length, 1);
  // 13 적어도 — (뒤, 뒤)를 지우고 남은 셋을 센다
  const cr = acts("c13-least", "cross")[0], rest = acts("c13-least", "count")[0];
  assert.deepEqual(ids("c13-least", cr).map((m) => leafOf(A("c13-least"), m)), [["뒤", "뒤"]]);
  const restLeaves = ids("c13-least", rest).map((m) => leafOf(A("c13-least"), m));
  assert.equal(restLeaves.length, 3);
  assert.ok(restLeaves.every((l) => l.includes("앞")), "남은 셋은 모두 앞면이 하나 이상");
  // 14 덧셈 — 2 이하 묶음 + 6 묶음
  const [le2, six] = acts("c14-add", "count");
  assert.deepEqual(dieOf(A("c14-add"), ids("c14-add", le2)), [1, 2]);
  assert.deepEqual(dieOf(A("c14-add"), ids("c14-add", six)), [6]);
  // 14 곱셈 — A = 6 인 가로줄 6칸, 그 가운데 (6, 6)
  const [rowA, cell] = acts("c14-66", "count");
  assert.deepEqual(ids("c14-66", rowA).map((i) => cellOf(A("c14-66"), i)[0]), [6, 6, 6, 6, 6, 6]);
  assert.deepEqual(ids("c14-66", cell).map((i) => cellOf(A("c14-66"), i)), [[6, 6]]);
  assert.equal(acts("c14-66", "all").length, 1);
});

test("경우 카드: 움직임이 그 판서 줄 시간 안에 · 같은 줄은 차례로(겹치지 않게)", () => {
  for (const it of OUTS) {
    const P = l10Plan(it), T = outsTimes(it, P);
    assert.equal(T.acts.length, it.fig.acts.length, it.id);
    const byLine = new Map();
    for (const a of T.acts) {
      const L = P.lines[a.at];
      assert.ok(L, `${it.id}: 판서 ${a.at}번 줄 없음`);
      assert.ok(a.t0 >= L.a && a.t1 <= L.b + 1, `${it.id} ${a.type}@${a.at}: ${Math.round(a.t0)} ~ ${Math.round(a.t1)} · 줄 ${Math.round(L.a)} ~ ${Math.round(L.b)}`);
      const prev = byLine.get(a.at);
      if (prev) assert.ok(a.t0 >= prev.t1 - 1, `${it.id}: 같은 줄 움직임이 겹침`);
      byLine.set(a.at, a);
    }
  }
});

test("주머니 공: 식의 수를 그림에 맞춘 값 = 식의 값 · 다시 넣기는 같은 무리에서 두 번 · 안 넣기는 하나씩 줄어", () => {
  const back = AV_BY_ID.get("c14-back"), nob = AV_BY_ID.get("c14-noback");
  for (const it of [back, nob]) {
    const { lines } = pickPlan(it);
    const moving = lines.map((L, i) => [L, i]).filter(([L]) => L.acts.length);
    assert.equal(moving.length, 2, `${it.id}: 그림에 맞춘 식 줄 ${moving.length}`);
    for (const [L, i] of moving) {
      const v = chain(it.lines[i].s);
      assert.equal(L.expect, v[v.length - 1].n, `${it.id} 「${it.lines[i].s}」: 그림 ${L.expect}`);
      const picks = L.acts.filter((a) => a.type === "pick");
      const got = picks.reduce((s, a) => { let m = s; for (let q = 0; q < a.k; q++) m *= a.back ? a.pool.ids.length : a.pool.ids.length - q; return m; }, 1);
      assert.equal(got, L.expect, `${it.id}: 뽑기 차례로 센 값`);
      assert.ok(picks.every((a) => a.slow === it.fig.slow), `${it.id}: 천천히(slow)`);
    }
    assert.ok(Number.isFinite(evalTree({ k: "num", v: 1 })));
  }
  assert.ok(pickPlan(back).lines.flatMap((L) => L.acts).filter((a) => a.type === "pick").every((a) => a.back), "다시 넣기: 모두 되돌려 넣음");
  assert.ok(pickPlan(nob).lines.flatMap((L) => L.acts).filter((a) => a.type === "pick").every((a) => !a.back), "안 넣기: 되돌려 넣지 않음");
});

test("한 줄 세우기: 자리마다 후보가 3, 2, 1 로 줄고 A · B · C 가 앉음 · 천천히", () => {
  const it = AV_BY_ID.get("c12-line"), sp = seatsPlan(it);
  const reels = sp.rows[0].acts.filter((a) => a.type === "reel");
  assert.deepEqual(reels.map((a) => a.cnt), [3, 2, 1]);
  assert.ok(reels.every((a) => a.ok && a.cands.length === a.cnt && a.slow === it.fig.slow), "후보 수 = 가짓수");
  assert.deepEqual(reels.map((a) => a.pick.lab).sort(), ["A", "B", "C"]);
  const v = chain(it.lines[3].s);
  assert.equal(reels.reduce((s, a) => s * a.cnt, 1), v[v.length - 1].n);
});

/* ══════════ ④ · ⑤ 판 · 그리기 ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-concept-av-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("features/display/draw.jsx")};
import { L10Art, layoutOf } from ${F("features/display/frames/lin10.jsx")};
import { AV_EXAMPLES } from ${F("features/display/concept-av.js")};
import ConceptAv, { avView, avSpan, AV_WIDE, AV_NARROW } from ${F("components/ConceptAv.jsx")};
export { AV_EXAMPLES, layoutOf, avView, avSpan, AV_WIDE, AV_NARROW };
export const art = (it, t, th, R) => renderToStaticMarkup(<svg>{<L10Art it={it} t={t} C={PALETTE[th]} uid={"t" + it.id} region={R} />}</svg>);
export const card = (ids, th) => renderToStaticMarkup(<ConceptAv ids={ids} theme={th} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  const REGIONS = [["넓은 판", m.AV_WIDE], ["좁은 판", m.AV_NARROW]];

  test("판: 넓은 판 · 좁은 판 모두 그림이 들어가고(배율 0.85 이상) 글자 칸과 겹치지 않음 · 흐르지 않음 · 잘라 쓴 판 안", () => {
    const hit = (a, b) => a[0] < b[2] - 1 && b[0] < a[2] - 1 && a[1] < b[3] - 1 && b[1] < a[3] - 1;
    for (const it of m.AV_EXAMPLES) {
      for (const [nm, R] of REGIONS) {
        const Lo = m.layoutOf(it, R), v = m.avView(it, R);
        assert.ok(Lo.fig, `${it.id} ${nm}: 그림이 빠짐`);
        assert.ok(!Lo.scroll, `${it.id} ${nm}: 판서가 흐름`);
        assert.ok(Lo.fig.s == null || Lo.fig.s >= 0.85, `${it.id} ${nm}: 그림 배율 ${Lo.fig.s}`);
        const fr = [Lo.fig.x, Lo.fig.y, Lo.fig.x + Lo.fig.w, Lo.fig.y + Lo.fig.h];
        assert.ok(fr[0] >= R.left - 1 && fr[2] <= R.right + 1, `${it.id} ${nm}: 그림이 판 밖(가로)`);
        for (const b of Lo.boxes) assert.ok(!hit(fr, b), `${it.id} ${nm}: 그림이 글자 칸과 겹침 ${b.map(Math.round)}`);
        const [, y0, w, h] = v.vb.split(" ").map(Number);
        assert.ok(y0 <= R.top - 30 && y0 + h >= Math.max(Lo.bottom, fr[3]) + 30, `${it.id} ${nm}: 잘라 쓴 판(${v.vb})이 글자 · 그림을 다 담지 못함`);
        assert.equal(w, R.right > 1000 ? 1600 : 800);
        if (nm === "좁은 판") assert.ok(fr[1] >= Lo.bottom - 1, `${it.id}: 좁은 판의 그림은 글자 아래`);
      }
    }
  });

  test("재생 구간: 문제는 처음부터 보이고 방침부터 써짐 · 답 칸이 그려진 뒤 멈춤 · 예시 하나 30초 안팎", () => {
    for (const it of m.AV_EXAMPLES) {
      const { P, t0, t1 } = m.avSpan(it);
      assert.ok(t0 >= 600 && t0 < P.plan[0], `${it.id}: 시작 ${t0}`);
      assert.ok(t1 > P.ans + 1400 && t1 < P.dur, `${it.id}: 끝 ${t1}`);
      assert.ok((t1 - t0) / 1000 < 30, `${it.id}: ${(t1 - t0) / 1000}초`);
    }
  });

  test("그리기 훑기: 예시마다 (시작 · 방침 · 줄마다 셋 · 답 · 끝) × 두 판 × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const it of m.AV_EXAMPLES) {
      const { P, t0, t1 } = m.avSpan(it);
      const ts = [0, t0, P.plan[0] + 400, P.ans + 300, t1, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 120, (L.a + L.b) / 2, L.b - 60);
      for (const [nm, R] of REGIONS) for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light", R);
        assert.ok((t < 600 || /<text/.test(s)) && !BAD.test(s), `${it.id} ${nm} t=${Math.round(t)}: ${bad(s) || "글자 없음"}`);
      }
    }
    console.log(`   그림 ${cnt}장`);
  });

  test("재생 카드: 예시 하나 · 둘(칩) × 두 테마 — 머리 · 판 · 막대 · 빠르기가 그려짐", () => {
    for (const th of ["light", "dark"]) {
      const one = m.card(["c12-sum"], th);
      assert.ok(one.includes("움직이는 예시") && one.includes("<svg") && one.includes('class="cav-bar"') && /1\.5(<!-- -->)?×/.test(one) && !/class="cav-tab( on)?"/.test(one), th);
      assert.ok(!BAD.test(one), bad(one));
      const two = m.card(["c14-back", "c14-noback"], th);
      assert.ok((two.match(/class="cav-tab( on)?"/g) || []).length === 2 && two.includes("다시 넣지 않기"), th);
      assert.equal(m.card(["없는것"], th), "");
    }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
