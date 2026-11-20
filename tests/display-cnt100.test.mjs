// node tests/display-cnt100.test.mjs — 교실 모니터 「경우의 수와 확률 100제 해설」 액자 검산(선발 · 공 꺼내기 · 사전식 · 줄 세우기). 실패 시 exit 1.
// 판서: 줄마다 「=」로 이은 쪽 가운데 계산식(수 · {a/b} · 괄호 · + − × ÷)인 것을 분수로 직접 계산해 모두 같은지 본다.
//       확률(분수) 답은 판서 마지막 줄의 마지막 값과 같은지.
// 박자표: 문제 → 전략 → 줄 차례 → 답. 목록: 세트마다 1~100번 · 단계 1~5(15 · 20 · 25 · 22 · 18).
// 그리기: 400문항을 여러 순간 × 두 테마로 그려 오류 · NaN 이 없는지, 글자 판이 무대 안인지 훑는다.
// 단일 모드 그림(줄 세우기 자리 칸 · 학년 · 주머니 공 · 사전식 나무): 줄 번호 · 빛남이 판서와 맞고 그림 자리 안인지.
// 듀얼 모드: 반쪽 판(PANE_BOX)에 400문항이 다 들어가는지, 판 기억(벽시계로 이어 돌기)과 기본값.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { C100_SETS, C100_KEYS } from "../src/features/display/cnt100.js";
import { l10Plan, lineAt } from "../src/features/display/lin10.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const ALL = C100_KEYS.flatMap((k) => C100_SETS[k].items.map((it) => [k, it]));

/* ══════════ 분수 ══════════ */
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const Q = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return { n: n / g, d: d / g }; };
const add = (a, b) => Q(a.n * b.d + b.n * a.d, a.d * b.d);
const sub = (a, b) => Q(a.n * b.d - b.n * a.d, a.d * b.d);
const mul = (a, b) => Q(a.n * b.n, a.d * b.d);
const div = (a, b) => Q(a.n * b.d, a.d * b.n);
const same = (a, b) => a.n === b.n && a.d === b.d;

/** 계산식이면 값, 아니면 null */
function calc(s) {
  const t = s.trim();
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
const ansQ = (s) => calc(s.replace(/(개|번째)$/, ""));
const isWord = (s) => /^[A-Z]+( \(.+\))?$/.test(s);

test("판서 계산: 「=」로 이은 계산식이 모두 같은 값 · 답이 판서와 맞음", () => {
  let lines = 0, eqs = 0;
  for (const [k, it] of ALL) {
    let last = null;
    for (const ln of it.lines) {
      const vals = ln.s.split(" = ").map((p) => calc(tail(p))).filter(Boolean);
      for (let i = 1; i < vals.length; i++) { assert.ok(same(vals[0], vals[i]), `${k} ${it.no}: ${ln.s}`); eqs++; }
      if (vals.length) { last = vals[vals.length - 1]; lines++; }
    }
    if (isWord(it.ans)) continue;          // 사전식 「○번째 문자열」 — 아래 사전식 검산에서 본다
    const a = ansQ(it.ans);
    assert.ok(a, `${k} ${it.no} 답 ${it.ans}`);
    // 확률 답(분수)은 판서 마지막 줄의 마지막 값이 곧 답
    if (a.d !== 1) assert.ok(last && same(last, a), `${k} ${it.no}: 마지막 값 ≠ 답 ${it.ans}`);
  }
  assert.ok(eqs > 250, `등식 ${eqs}개`);
  console.log(`   계산 줄 ${lines}개 · 등식 ${eqs}개`);
});

/* ══════════ 사전식: 문자열을 모두 늘어놓아 다시 센다 ══════════ */
function strings(cards, k) {
  const out = [];
  const go = (pre, rest) => { if (pre.length === k) { out.push(pre); return; } rest.forEach((c, i) => go(pre + c, rest.filter((_, j) => j !== i))); };
  go("", [...cards].sort());
  return out.sort();
}
test("사전식: 숫자 분석 합 = 번호 · 나무로 찾은 글자 = 답 · 늘어놓아 센 순번과 같음 · 나무 줄 번호가 판서 안", () => {
  let n = 0;
  for (const it of C100_SETS.lex.items) {
    const f = it.fig;
    const kth = it.planTag === "숫자 분석";
    if (!f) {                                   // 두 단어 사이
      const [w1, w2] = it.lines.slice(2, 4).map((l) => l.pre);
      const S = strings(w1.split(""), w1.length);
      const d = Math.abs(S.indexOf(w1) - S.indexOf(w2)) - 1;
      assert.equal(`${d}개`, it.ans, `lex ${it.no}`);
      continue;
    }
    const word = f.cols.map((c) => c.items.find((x) => x[2])[0]).join("") + f.tail;
    const S = strings(f.cards, word.length);
    if (kth) {
      const [lhs, rhs] = it.plan.split(" = ");
      const kk = +lhs, sum = rhs.split(" + ").reduce((a, b) => a + +b, 0);
      assert.equal(sum, kk, `lex ${it.no} 숫자 분석`);
      assert.ok(it.q.includes(`${kk}번째`), `lex ${it.no} 발문의 번호`);
      assert.equal(S[kk - 1], word, `lex ${it.no} ${kk}번째`);
      assert.equal(it.ans.split(" ")[0], word, `lex ${it.no} 답`);
    } else {
      assert.ok(it.q.includes(word), `lex ${it.no} 발문의 단어 ${word}`);
      const r = S.indexOf(word) + 1;
      const fromEnd = it.q.includes("뒤에서");
      assert.equal(it.ans, `${fromEnd ? S.length - r + 1 : r}번째`, `lex ${it.no} 순번`);
    }
    for (const [a, b] of f.at) assert.ok(a >= 0 && b >= a && b < it.lines.length, `lex ${it.no} 나무 줄`);
    assert.ok(f.tailAt < it.lines.length);
    n++;
  }
  console.log(`   나무 ${n}개`);
});

const STAGES = { sel: [15, 20, 25, 22, 18], ball: [15, 20, 25, 22, 18], lex: [10, 16, 24, 25, 25], line: [15, 20, 25, 22, 18] };
test("문항 목록: 세트마다 1~100번 · 단계 1~5 문항 수, 차례대로", () => {
  for (const k of C100_KEYS) {
    const its = C100_SETS[k].items;
    assert.equal(its.length, 100);
    its.forEach((it, i) => assert.equal(it.no, i + 1));
    assert.deepEqual([1, 2, 3, 4, 5].map((s) => its.filter((it) => it.st === s).length), STAGES[k]);
    for (let i = 1; i < 100; i++) assert.ok(its[i].st >= its[i - 1].st);
    assert.ok(its.every((it) => it.q && it.plan && it.ans && it.lines.length >= 3 && it.lines[0].pre === "포지티브" && it.lines[1].pre === "네거티브"));
  }
});

test("박자표: 문제 → 전략 → 줄 차례 → 답", () => {
  for (const [k, it] of ALL) {
    const P = l10Plan(it);
    assert.ok(P.q[1] <= P.plan[0] && P.plan[1] <= P.lines[0].a);
    P.lines.forEach((L, i) => { assert.ok(L.a < L.b); if (i) assert.ok(P.lines[i - 1].b <= L.a); });
    assert.ok(P.lines.at(-1).b <= P.ans && P.ans < P.dur);
    assert.equal(lineAt(P, P.plan[1] + 1), 0);
  }
});

/* ══════════ 그리기 훑기(번들) ══════════ */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-cnt100-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { L10Art, layoutOf, L10_BOX } from ${F("frames/lin10.jsx")};
import { Cnt100Thumb, c100Scenes, PANE, PANE_BOX, DUAL_SPEEDS, paneLoad } from ${F("frames/cnt100.jsx")};
import { seatsGeom } from ${F("frames/c100fig.jsx")};
import { Scrub } from ${F("frames/scrub.jsx")};
import { l10Scenes } from ${F("frames/lin10.jsx")};
import { areaScenes } from ${F("frames/area.jsx")};
import { graphScenes } from ${F("frames/graphdraw.jsx")};
import { L10_SETS } from ${F("lin10.js")};
import { AREA_SETS } from ${F("area.js")};
import { GD_SETS } from ${F("graphdraw.js")};
export { FRAMES, c100Scenes, layoutOf, L10_BOX, PANE, PANE_BOX, DUAL_SPEEDS, paneLoad, seatsGeom };
export const lessonLists = () => [
  ...Object.keys(L10_SETS).map((k) => ["lin10 " + k, l10Scenes(+k, 1, 0)]),
  ...Object.keys(AREA_SETS).map((k) => ["area " + k, areaScenes(k, 1.5, 0)]),
  ...Object.keys(GD_SETS).map((k) => ["graph " + k, graphScenes(k, 1)]),
];
export const scrub = (scenes, idx, t, v, show) => renderToStaticMarkup(<Scrub variant={v} show={show} scenes={scenes} idx={idx} onPick={() => {}}
  t={t} dur={scenes[idx].dur} marks={scenes[idx].marks} onSeek={() => {}} />);
export const paneArt = (it, t, th) => renderToStaticMarkup(<svg><L10Art it={it} t={t} C={PALETTE[th]} box={PANE_BOX} /></svg>);
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<L10Art it={it} t={t} C={PALETTE[th]} />);
export const scene = (sc, t, th) => svg(sc.render("m", t, PALETTE[th]));
export const thumb = (th) => svg(<Cnt100Thumb C={PALETTE[th]} />);
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

  test("액자 목록: 「경우의 수와 확률 100제 해설」이 해설 액자로 · 그림 두 테마 오류 없음", () => {
    const f = m.FRAMES.find((x) => x.key === "cnt100");
    assert.ok(f && f.lesson && f.title && f.desc);
    for (const th of ["dark", "light"]) { const s = m.thumb(th); assert.ok(s.length > 3000 && !BAD.test(s), `${th}: ${bad(s)}`); }
  });

  test("그리기 훑기: 400문항 × (문제 · 전략 · 줄마다 · 답 · 끝) × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const [k, it] of ALL) {
      const P = l10Plan(it);
      const ts = [0, 300, P.plan[0] + 300, P.ans + 300, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 100, (L.a + L.b) / 2);
      for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light");
        assert.ok(!BAD.test(s), `${k} ${it.no} t=${Math.round(t)}: ${bad(s)}`);
      }
    }
    console.log(`   그림 ${cnt}장`);
  });

  test("글자 판: 발문 · 판서 · 답이 무대 안", () => {
    const B = m.L10_BOX;
    for (const [k, it] of ALL) {
      const L = m.layoutOf(it), tag = `${k} ${it.no}`;
      assert.ok(L.ansY + L.bs * 0.75 <= B.BOTTOM, `${tag} 아래로 넘침 (${Math.round(L.ansY)})`);
      for (const r of L.rows) assert.ok(r.sx + r.sW <= L.right + 2, `${tag} 줄이 오른쪽으로 넘침: ${it.lines[r.i].s}`);
      assert.ok(L.planS >= 18, `${tag} 방침 칸 글자가 너무 작음(${L.planS}): ${it.plan}`);
    }
  });

  test("단일 모드 그림: 데이터가 판서 줄과 맞고(줄 번호 · 빛남 줄 수) 그림이 그림 자리 안 · 그림이 붙는 문항 수", () => {
    const n = { sel: 0, ball: 0, lex: 0, line: 0 };
    for (const [k, it] of ALL) {
      const f = it.fig, tag = `${k} ${it.no}`;
      if (!f) continue;
      const nl = it.lines.length;
      if (f.kind === "seats") {
        const G = m.seatsGeom(f);
        for (const [ri, r] of f.rows.entries()) {
          for (const a of [r.at, r.cntAt, r.innerAt, r.noteAt, ...r.swaps.map((x) => x.at), ...r.units.filter((u) => u.ca != null).map((u) => u.ca)])
            assert.ok(Number.isInteger(a) && a >= 0 && a < nl, `${tag} 줄 번호 ${a}`);
          for (const sw of r.swaps) assert.ok(sw.a >= 0 && sw.b < r.units.length);
          const g = G.rows[ri];
          assert.ok(g.x0 >= m.L10_BOX.FIG.x0 - 1 && g.x0 + g.W <= m.L10_BOX.FIG.x1 + 1, `${tag} 자리 칸이 그림 자리 밖`);
        }
        // 가짓수(칸 위 숫자)를 곱하면 식의 한 덩어리 — 적어도 한 줄에 그 곱이 나온다(빈자리 · 묶음 안 순서는 따로)
        const cs = f.rows[0].mixed ? [] : f.rows[0].units.filter((u) => u.cnt != null && !u.ca).map((u) => +u.cnt);
        const prod = cs.reduce((a, v) => a * v, 1), seq = cs.join(" × ");
        assert.ok(prod === 1 || it.lines.some((l) => l.s.includes(String(prod)) || l.s.includes(seq)), `${tag} 칸 위 수(${seq} = ${prod})가 판서에 없음`);
      } else if (f.kind === "grades" || f.kind === "bag") {
        assert.equal(f.hl.length, nl, `${tag} 빛남 줄 수`);
      } else if (f.kind === "tree") { /* 사전식 — 위에서 따로 */ }
      else assert.fail(`${tag} 모르는 그림 ${f.kind}`);
      if (!m.layoutOf(it).noFig) n[k]++;
    }
    console.log(`   그림이 붙는 문항: ${Object.entries(n).map(([k, v]) => `${C100_SETS[k].short} ${v}`).join(" · ")}`);
    for (const k of C100_KEYS) assert.ok(n[k] >= 60, `${k} 그림 문항이 너무 적음(${n[k]})`);
  });

  test("듀얼 모드: 반쪽 판에 400문항 모두 들어감 · 그리기 오류 없음 · 판 기억(벽시계로 이어 돌기 · 기본 왼쪽 앞 빠르게 · 오른쪽 뒤 느리게)", () => {
    const B = m.PANE_BOX;
    let cnt = 0;
    for (const [k, it] of ALL) {
      const L = m.layoutOf(it, B), tag = `${k} ${it.no}`;
      assert.ok(L.noFig, `${tag} 반쪽 판에 그림`);
      assert.ok(L.ansY + L.bs * 0.75 <= B.bottom, `${tag} 반쪽 판 아래로 넘침 (${Math.round(L.ansY)})`);
      for (const r of L.rows) assert.ok(r.sx + r.sW <= B.right + 2, `${tag} 반쪽 판 오른쪽으로 넘침: ${it.lines[r.i].s}`);
      assert.ok(L.qs >= 28 && L.bs >= 28);
      const P = l10Plan(it);
      for (const t of [P.plan[1] + 100, P.ans + 400]) {
        const s = m.paneArt(it, t, cnt++ % 2 ? "dark" : "light");
        assert.ok(!BAD.test(s), `${tag} 반쪽 t=${Math.round(t)}: ${bad(s)}`);
      }
    }
    const now = 1_700_000_000_000;
    const dl = m.paneLoad(null, "L", "lex", now), dr = m.paneLoad(null, "R", "lex", now);
    assert.deepEqual([dl.set, dl.sp, dl.i, dl.held], ["lex", 1.5, 0, null]);
    assert.deepEqual([dr.set, dr.sp, dr.i], ["lex", 0.75, 50]);
    const L = m.c100Scenes("line", 2, 3);
    const o = { set: "line", st: 3, sp: 2, i: 2, t0: now - (L[2].dur + L[3].dur + 500), held: null, rep: false };
    const p = m.paneLoad(o, "R", "sel", now);
    assert.deepEqual([p.set, p.st, p.sp, p.i, now - p.t0], ["line", 3, 2, 4, 500]);
    const ph = m.paneLoad({ ...o, held: 1200 }, "R", "sel", now);
    assert.deepEqual([ph.i, ph.held], [2, 1200]);
    const pr = m.paneLoad({ ...o, rep: true }, "L", "sel", now);
    assert.equal(pr.i, 2);
    assert.deepEqual(m.DUAL_SPEEDS, [0.75, 1, 1.5, 2]);
    console.log(`   반쪽 판 그림 ${cnt}장`);
  });

  test("두 막대: 해설 액자 넷의 장면마다 풀이 눈금(문제 → … → 답, 장면 안) · 단계 이름 · 막대 그리기(단일 · 듀얼 판)", () => {
    const lists = [...C100_KEYS.flatMap((k) => [["c100 " + k, m.c100Scenes(k, 1, 0)], ["c100 " + k + " 2×", m.c100Scenes(k, 2, 3)]]), ...m.lessonLists()];
    let nm = 0;
    for (const [tag, L] of lists) {
      assert.ok(L.length > 0, tag);
      for (const sc of L) {
        const ms = sc.marks;
        assert.ok(Array.isArray(ms) && ms.length >= 3, `${tag} ${sc.no} 눈금`);
        assert.equal(ms[0].t, 0);
        assert.equal(ms[0].lab, "문제");
        assert.equal(ms.at(-1).lab, "답");
        for (let i = 1; i < ms.length; i++) assert.ok(ms[i].t >= ms[i - 1].t, `${tag} ${sc.no} 눈금 차례`);
        assert.ok(ms.at(-1).t < sc.dur, `${tag} ${sc.no} 답이 장면 안`);
        assert.ok(ms.every((x) => typeof x.lab === "string" && x.lab.length > 0 && x.lab.length <= 30), `${tag} ${sc.no} 눈금 이름`);
        nm += ms.length;
      }
      const grpChanges = L.filter((s, i) => i && s.grp !== L[i - 1].grp).length;
      assert.ok(grpChanges <= 40, `${tag} 단계 눈금이 너무 많음(${grpChanges})`);
      for (const v of ["full", "L", "R"]) {
        const h = m.scrub(L, Math.min(5, L.length - 1), 1200, v, true);
        assert.ok(h.includes("scb-long") && h.includes("scb-short") && !BAD.test(h), `${tag} ${v} 막대`);
      }
    }
    console.log(`   장면 묶음 ${lists.length}개 · 풀이 눈금 ${nm}개`);
  });

  test("장면 목록: 세트 × 빠르기 × 단계 — 1.5× 는 길이 2/3 · 같은 순간", () => {
    for (const k of C100_KEYS) {
      const all = m.c100Scenes(k, 1, 0), fast = m.c100Scenes(k, 1.5, 0);
      assert.equal(all.length, 100);
      assert.equal(new Set(all.map((s) => s.key)).size, 100);
      for (let st = 1; st <= 5; st++) {
        const one = m.c100Scenes(k, 1, st);
        assert.ok(one.length >= 10 && one.every((s) => s.st === st));
        assert.ok(one[0].sub.m.startsWith(`${st}단계`));
      }
      all.forEach((s, i) => assert.ok(Math.abs(fast[i].dur - s.dur / 1.5) <= 1));
      assert.equal(m.scene(all[30], 9000, "dark"), m.scene(fast[30], 6000, "dark"));
    }
    const lap = (k) => Math.round(m.c100Scenes(k, 1, 0).reduce((s, x) => s + x.dur, 0) / 60000);
    console.log(`   한 바퀴: ${C100_KEYS.map((k) => `${C100_SETS[k].short} 약 ${lap(k)}분`).join(" · ")}`);
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
