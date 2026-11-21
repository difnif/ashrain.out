// node tests/display-weeks.test.mjs — 주차별 기초 다지기(학년마다 52주 × 주 2회 = 104회차, public/av-weeks) · 우물 추천(lib/recommend.js) 검산. 실패 시 exit 1.
// 자료: 학년 12 · 초등 624 · 중등 312 · 고등 312회차 · 회차마다 20문항(1 ~ 5단계 4문항씩) · 회차 id · 주 · 회차(A · B) · 학기 · 종류 ·
//       교과서 단원(빈 단원 없음) · 프린트 코드(6글자, 회차끼리도 단원 100제와도 겹치지 않음) · 학년 안에서 같은 문항 없음 · 중2 이하 √ 없음.
// 판서: 수만 있는 「=」 줄을 이 파일의 분수 계산기로 다시 계산한다(생성기의 sympy 검산과 다른 두 번째 계산).
// 그리기: 그림이 빠지지 않는지(글자 판) · 그림 좌표 · 넷 중 하나는 다 푼 순간으로 그려 오류 · NaN 이 없는지.
// 문서: 학년마다 몇 회차씩 문제지 · 해설지 · 빠른 정답 HTML · 등록 정보 · OMR.
// 학사 달력 · 회차 id 도우미(features/display/weeks) · 본 기록(lib/avHistory.js) · 우물 추천 6가지(기본 · 맞춤).
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { WGRADES, WEEKS, PER_GRADE, PERIODS, KIND_ICON, parseWeekId, weekId, gradeOf, gradesOfLevel, frameOfGrade, periodOf,
  yearStart, weekOfDate, mondayOf, weekLabel } from "../src/features/display/weeks/index.js";
import { BASICS } from "../src/features/display/basics/index.js";
import { TERM_LABEL, nextUnits, prevUnits } from "../src/lib/units.js";
import { readHist, noteOpen, noteSeen, histDone, lastSeen } from "../src/lib/avHistory.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const DIR = path.join(ROOT, "public/av-weeks");
const IDX = {}, SETS = {};
for (const g of WGRADES) {
  IDX[g.gk] = JSON.parse(fs.readFileSync(path.join(DIR, g.gk, "index.json"), "utf8"));
  for (const m of IDX[g.gk].sessions) SETS[m.id] = JSON.parse(fs.readFileSync(path.join(DIR, g.gk, `${m.id}.json`), "utf8"));
}
const ALL = WGRADES.flatMap((g) => IDX[g.gk].sessions.map((meta) => ({ g, meta, set: SETS[meta.id] })));
const KINDS = Object.keys(KIND_ICON);

/* ══════════ 회차 머리 정보 ══════════ */
test("학년 12 · 학년마다 104회차(52주 × A · B) — 초등 624 · 중등 312 · 고등 312 · 머리 정보 칸", () => {
  assert.equal(WGRADES.length, 12);
  assert.equal(PER_GRADE, 104);
  assert.deepEqual(["초등", "중등", "고등"].map((lv) => gradesOfLevel(lv).reduce((s, g) => s + IDX[g.gk].sessions.length, 0)), [624, 312, 312]);
  for (const g of WGRADES) {
    const h = IDX[g.gk];
    assert.equal(h.gk, g.gk);
    assert.equal(h.grade, g.grade);
    assert.equal(h.level, g.level);
    assert.equal(h.n, 104);
    h.sessions.forEach((m, i) => {
      const week = 1 + Math.floor(i / 2), slot = "AB"[i % 2], tag = m.id;
      assert.equal(m.id, weekId(g.gk, week, slot));
      assert.deepEqual(parseWeekId(m.id), { gk: g.gk, week, slot });
      assert.equal(m.week, week, tag);
      assert.equal(m.slot, slot, tag);
      assert.equal(m.gk, g.gk, tag);
      assert.equal(m.grade, g.grade, tag);
      assert.equal(m.level, g.level, tag);
      assert.equal(m.period, periodOf(week), `${tag} 학기`);
      assert.ok(KINDS.includes(m.kind), `${tag} 종류 ${m.kind}`);
      assert.equal(m.n, 20, tag);
      assert.equal(m.short, `${g.grade}-${week}주${slot}`, tag);
      assert.ok(m.title && m.title.length >= 2 && m.desc.length > 8, `${tag} 제목 · 설명`);
      for (const st of [1, 2, 3, 4, 5]) assert.ok(m.stages[st], `${tag} ${st}단계 이름`);
      for (const u of [m.unit, ...m.units]) {
        const [t, name] = String(u).split(":");
        assert.ok(TERM_LABEL[t] && name, `${tag} 단원 ${u}`);
      }
      assert.ok(m.units.includes(m.unit), `${tag} 주요 단원이 단원 목록에`);
    });
  }
});
test("학기 · 방학 차례: 1 ~ 20주 1학기 · 21 ~ 25 여름방학(복습 · 예습) · 26 ~ 45 2학기 · 46 ~ 52 겨울방학(복습 · 예습)", () => {
  assert.deepEqual(PERIODS.map((p) => [p.key, p.from, p.to]), [["1학기", 1, 20], ["여름방학", 21, 25], ["2학기", 26, 45], ["겨울방학", 46, 52]]);
  for (const g of WGRADES) {
    const S = IDX[g.gk].sessions;
    for (const m of S) {
      if (m.period === "여름방학" || m.period === "겨울방학") assert.ok(["복습", "예습"].includes(m.kind), `${m.id} 방학인데 ${m.kind}`);
      else assert.ok(!["예습"].includes(m.kind) || m.period === "1학기", `${m.id} 학기 중 예습`);
    }
    if (g.gk !== "h3") assert.ok(S.some((m) => m.kind === "예습"), `${g.gk} 예습 회차`);
    assert.ok(S.some((m) => m.kind === "복습"), `${g.gk} 복습 회차`);
    assert.ok(S.filter((m) => m.kind === "개념").length >= 4, `${g.gk} 개념 회차`);
  }
});
test("교과서 단원: 빈 단원 없음 · 학년의 학기 단원이 모두 회차의 주요 단원으로 나온다 · 단원 지도에 이어져 있다", () => {
  for (const g of WGRADES) {
    const h = IDX[g.gk];
    assert.deepEqual(h.gaps, [], `${g.gk} 빈 단원 ${h.gaps}`);
    const terms = new Set(h.sessions.filter((m) => m.period === "1학기" || m.period === "2학기").map((m) => m.unit.split(":")[0]));
    for (const t of terms) assert.ok(TERM_LABEL[t], t);
    for (const m of h.sessions) assert.ok(nextUnits(m.unit).length + prevUnits(m.unit).length > 0, `${m.id} ${m.unit} — 단원 지도에 없음`);
  }
  const mains = new Set(ALL.filter((x) => x.meta.period.endsWith("학기")).map((x) => x.meta.unit));
  assert.ok(mains.size >= 110, `학기 중 주요 단원 ${mains.size}가지`);
});
test("프린트 코드: 6글자(헷갈리는 글자 없음) · 1248회차가 서로 겹치지 않고 단원 100제 코드와도 겹치지 않는다", () => {
  const unit = new Set(BASICS.map((b) => b.code));
  const seen = new Set();
  for (const { meta } of ALL) {
    assert.match(meta.code, /^[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/, meta.id);
    assert.ok(!seen.has(meta.code), `${meta.id} 코드 겹침`);
    assert.ok(!unit.has(meta.code), `${meta.id} 단원 100제 코드와 겹침`);
    seen.add(meta.code);
  }
  assert.equal(seen.size, 1248);
});

/* ══════════ 회차 문항 ══════════ */
test("회차마다 20문항 · 번호 1 ~ 20 · 단계 1 ~ 5 가 4문항씩 차례로 · 문항 칸 · 요령 · 도움말 · 한 쪽 문항 수", () => {
  for (const { meta, set } of ALL) {
    const tag = meta.id;
    assert.equal(set.id, meta.id);
    assert.equal(set.items.length, 20, tag);
    assert.ok(set.pp >= 6 && set.pp <= 10, `${tag} pp ${set.pp}`);
    assert.ok(set.note && set.note.length > 20, `${tag} 도움말`);
    for (const st of [1, 2, 3, 4, 5]) assert.ok(set.tips[st], `${tag} ${st}단계 요령`);
    set.items.forEach((it, i) => {
      assert.equal(it.no, i + 1, tag);
      assert.equal(it.st, Math.floor(i / 4) + 1, `${tag} ${it.no} 단계`);
      assert.ok(it.q && it.ans && it.plan && it.lines.length >= 1 && it.ap != null && it.ap !== "", `${tag} ${it.no} 빈 칸`);
      assert.ok(["num", "ex", "pt"].includes(it.omr), `${tag} ${it.no} omr ${it.omr}`);
      for (const ln of it.lines) assert.ok(typeof ln.s === "string" && ln.s.length, `${tag} ${it.no} 판서 줄`);
      assert.ok(!/undefined|NaN|None|\[object/.test(JSON.stringify(it)), `${tag} ${it.no} 글자에 undefined · NaN · None`);
      const txt = [it.q, it.ans, it.plan, ...it.lines.flatMap((l) => [l.s, l.pre || "", l.memo || ""])].join("\n");
      assert.ok(!/(^|[^\w])-\d/m.test(txt), `${tag} ${it.no} 빼기 기호가 아닌 '-'`);
      assert.ok(!/[가-힣]\((을|를|이|가|은|는|과|와)\)|\(으\)로|을\(를\)|이\(가\)|은\(는\)|과\(와\)/.test(it.q), `${tag} ${it.no} 고르지 않은 조사: ${it.q}`);
    });
  }
});
test("학년 안에서 같은 문항이 두 번 나오지 않는다(그림이 자료인 문항은 발문 + 그림으로)", () => {
  for (const g of WGRADES) {
    const seen = new Map();
    for (const m of IDX[g.gk].sessions) for (const it of SETS[m.id].items) {
      const k = it.q + (it.qf ? "|" + JSON.stringify(it.fig) : "");
      assert.ok(!seen.has(k), `${g.gk} ${m.id} ${it.no} = ${seen.get(k)} — ${it.q.slice(0, 40)}`);
      seen.set(k, `${m.id} ${it.no}`);
    }
  }
});
test("중1 · 중2 회차에는 √ 를 쓰지 않는다", () => {
  for (const { g, meta, set } of ALL) {
    if (g.gk !== "m1" && g.gk !== "m2") continue;
    for (const it of set.items) assert.ok(!JSON.stringify(it).includes("√"), `${meta.id} ${it.no} √`);
  }
});

/* ══════════ 판서 다시 계산 (수만 있는 줄) ══════════ */
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const Q = (p, q = 1) => { if (q < 0) { p = -p; q = -q; } const d = gcd(p, q); return { p: p / d, q: q / d }; };
const add = (a, b) => Q(a.p * b.q + b.p * a.q, a.q * b.q);
const mul = (a, b) => Q(a.p * b.p, a.q * b.q);
const div = (a, b) => { if (b.p === 0) throw new Error("0으로 나눔"); return Q(a.p * b.q, a.q * b.p); };
function pow(a, k) {
  if (k.q !== 1) throw new Error("분수 지수");
  let r = Q(1), e = Math.abs(k.p);
  if (e > 40) throw new Error("큰 지수");
  for (let i = 0; i < e; i++) r = mul(r, a);
  return k.p < 0 ? div(Q(1), r) : r;
}
function numVal(src) {
  const s = String(src).replace(/(?<=\d),(?=\d{3}(?!\d))/g, "").replace(/−/g, "-").replace(/\s+/g, "");
  if (!s || !/^[\d+\-×÷().{}/^]+$/.test(s) || !/\d/.test(s)) return null;
  let i = 0;
  const peek = () => s[i];
  const sub = (str) => { const v = numVal(str); if (!v) throw new Error("식"); return v; };
  function grab(open, close) {
    let d = 0, j = i;
    for (; j < s.length; j++) { if (s[j] === open) d++; else if (s[j] === close && --d === 0) break; }
    if (j >= s.length) throw new Error("괄호");
    const inner = s.slice(i + 1, j);
    i = j + 1;
    return inner;
  }
  function atom() {
    const c = peek();
    let v;
    if (c === "(") v = sub(grab("(", ")"));
    else if (c === "{") {
      const inner = grab("{", "}");
      let d = 0, k = -1;
      for (let j = 0; j < inner.length; j++) { if (inner[j] === "{") d++; else if (inner[j] === "}") d--; else if (inner[j] === "/" && d === 0) { k = j; break; } }
      if (k < 0) throw new Error("분수");
      v = div(sub(inner.slice(0, k)), sub(inner.slice(k + 1)));
    } else if (c && /\d/.test(c)) {
      let j = i;
      while (j < s.length && /[\d.]/.test(s[j])) j++;
      const t = s.slice(i, j);
      i = j;
      if (t.includes(".")) { const [x, y] = t.split("."); v = Q(Number(x + y), 10 ** y.length); } else v = Q(Number(t));
      if (peek() === "{" && !t.includes(".")) v = add(v, atom());
    } else throw new Error(`읽을 수 없음 ${c}`);
    while (peek() === "^") { i++; if (peek() !== "{") throw new Error("지수"); v = pow(v, sub(grab("{", "}"))); }
    return v;
  }
  function unary() { if (peek() === "-") { i++; return mul(Q(-1), unary()); } if (peek() === "+") { i++; return unary(); } return atom(); }
  function term() {
    let v = unary();
    for (;;) {
      const c = peek();
      if (c === "×") { i++; v = mul(v, unary()); } else if (c === "÷") { i++; v = div(v, unary()); }
      else if (c === "(" || c === "{") v = mul(v, atom());
      else return v;
    }
  }
  function expr() {
    let v = term();
    for (;;) { const c = peek(); if (c === "+") { i++; v = add(v, term()); } else if (c === "-") { i++; v = add(v, mul(Q(-1), term())); } else return v; }
  }
  try { const v = expr(); return i === s.length ? v : null; } catch { return null; }
}
const eq = (a, b) => a.p === b.p && a.q === b.q;
let checks = 0;
test("판서의 수 계산(분수 · 거듭제곱 · 괄호 · 나머지) — 「=」로 이은 쪽이 모두 같다", () => {
  const bad = [];
  for (const { meta, set } of ALL) for (const it of set.items) {
    for (const ln of [...it.lines.map((l) => l.s), it.plan]) {
      for (const m of ln.matchAll(/(\d+) ÷ (\d+) = (\d+) … (\d+)/g)) {
        const [a, b, q, r] = m.slice(1).map(Number);
        checks++;
        if (!(a === b * q + r && r >= 0 && r < b)) bad.push(`${meta.id} ${it.no}: ${m[0]}`);
      }
      for (const part of ln.split(/→|⇒|, (?=[^)]*(?:\(|$))/)) {
        if (part.includes("…") || part.includes("≠")) continue;
        const sides = part.split("=").map((x) => x.split(/<|>|≤|≥/)[0]);
        if (sides.length < 2) continue;
        const vals = sides.map((x) => { const t = x.match(/[가-힣][^가-힣]*$/) ? x.slice(x.search(/[^가-힣]*$/)) : x; return numVal(t.trim()); });
        for (let k = 0; k + 1 < vals.length; k++) {
          if (!vals[k] || !vals[k + 1]) continue;
          checks++;
          if (!eq(vals[k], vals[k + 1])) bad.push(`${meta.id} ${it.no}: ${part.trim()}`);
        }
      }
    }
  }
  assert.equal(bad.length, 0, bad.slice(0, 8).join("\n   "));
  assert.ok(checks > 15000, `다시 계산한 등식이 너무 적다 (${checks})`);
});

/* ══════════ 학사 달력 · 회차 id ══════════ */
test("학사 달력: 1주 = 3월 2일이 든 주(월요일) · 날짜 → 학년도 · 주 · 주 이름 · 회차 id", () => {
  const ymd = (d) => [d.getFullYear(), d.getMonth() + 1, d.getDate()];
  assert.deepEqual(ymd(yearStart(2026)), [2026, 3, 2]);
  assert.deepEqual(ymd(yearStart(2027)), [2027, 3, 1]);
  assert.deepEqual(ymd(yearStart(2025)), [2025, 2, 24]);
  assert.deepEqual(weekOfDate(new Date(2026, 10, 21)), { year: 2026, week: 38 });
  assert.deepEqual(weekOfDate(new Date(2026, 2, 2)), { year: 2026, week: 1 });
  assert.deepEqual(weekOfDate(new Date(2027, 1, 10)), { year: 2026, week: 50 });
  assert.deepEqual(weekOfDate(new Date(2027, 1, 28)), { year: 2026, week: 52 });
  assert.deepEqual(weekOfDate(new Date(2027, 2, 1)), { year: 2027, week: 1 });
  assert.deepEqual(ymd(mondayOf(2026, 38)), [2026, 11, 16]);
  assert.equal(weekLabel(2026, 1), "3월 1주");
  assert.equal(weekLabel(2026, 38), "11월 3주");
  assert.equal(periodOf(20), "1학기");
  assert.equal(periodOf(21), "여름방학");
  assert.equal(periodOf(45), "2학기");
  assert.equal(periodOf(46), "겨울방학");
  assert.equal(parseWeekId("w-e3-07a").week, 7);
  for (const bad of ["w-e7-01a", "w-e3-53a", "w-e3-00b", "w-e3-7a", "e-ten", null]) assert.equal(parseWeekId(bad), null, String(bad));
  assert.equal(weekId("h2", 3, "B"), "w-h2-03b");
  assert.equal(gradeOf("중2").gk, "m2");
  assert.equal(frameOfGrade("m2"), "basic-m");
  assert.equal(WEEKS, 52);
});

/* ══════════ 본 기록 ══════════ */
test("본 기록(기기 안): 연 횟수 · 가장 멀리 본 문항 · 다 봄(80%) · 가장 최근 · 400개까지만", () => {
  const mem = new Map();
  const storage = { getItem: (k) => mem.get(k) ?? null, setItem: (k, v) => mem.set(k, String(v)) };
  noteOpen("w-e3-07a", 20, { now: 1000, storage });
  noteSeen("w-e3-07a", 9, 20, { now: 2000, storage });
  noteSeen("w-e3-07a", 4, 20, { now: 3000, storage });
  noteOpen("e-ten", 100, { now: 4000, storage });
  let h = readHist(storage);
  assert.deepEqual(h["w-e3-07a"], { t: 3000, v: 1, max: 9, n: 20 });
  assert.equal(histDone(h["w-e3-07a"]), false);
  noteSeen("w-e3-07a", 16, 20, { now: 5000, storage });
  h = readHist(storage);
  assert.equal(histDone(h["w-e3-07a"]), true);
  assert.equal(lastSeen(h).key, "w-e3-07a");
  assert.equal(lastSeen(h, "e-").key, "e-ten");
  for (let i = 0; i < 450; i++) noteOpen(`k${i}`, 20, { now: 10000 + i, storage });
  h = readHist(storage);
  assert.equal(Object.keys(h).length, 400);
  assert.ok(!h["w-e3-07a"] && h.k449, "오래된 것부터 지운다");
  assert.deepEqual(readHist({ getItem: () => "{깨진" }), {});
});

/* ══════════ 그리기 · 문서 · 추천(번들) ══════════ */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-weeks-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { l10Plan } from ${F("lin10.js")};
import { L10Art, layoutOf } from ${F("frames/lin10.jsx")};
import { STAGE_REGION as L10_BOX } from ${F("board.js")};
import { FigDsl } from ${F("frames/figdsl.jsx")};
import { avDocHtml, avManifest, avCard, problemPages } from ${F("frames/avprint.js")};
import { avDownloadName, avFileBase } from ${F("frames/docsmenu.jsx")};
import { PRINT_C } from ${F("frames/avfig.jsx")};
import { weekItem, weekCard, unitCard, avOfCat, avItem } from ${JSON.stringify(path.join(ROOT, "src/lib/av.js"))};
import { recommend, defaultPicks, personalPicks, profileEnough, masteryOf, unitOfConcept, masteryFrom, MAX } from ${JSON.stringify(path.join(ROOT, "src/lib/recommend.js"))};
export { l10Plan, layoutOf, L10_BOX, avDocHtml, avManifest, avCard, problemPages, avDownloadName, avFileBase, weekItem, weekCard, unitCard, avOfCat, avItem,
  recommend, defaultPicks, personalPicks, profileEnough, masteryOf, unitOfConcept, masteryFrom, MAX };
const svg = (el) => renderToStaticMarkup(<svg>{el}</svg>);
export const art = (it, t, th) => svg(<L10Art it={it} t={t} C={PALETTE[th]} />);
export const figPrint = (it, when) => { const P = l10Plan(it); const t = when === "q" ? P.plan[0] - 1 : P.ans + 5000;
  return renderToStaticMarkup(<svg viewBox="880 170 660 680"><FigDsl it={it} t={t} C={PRINT_C} /></svg>); };
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

  test("판 짜기(공통 글자 판 board.js): 24960문항 모두 글자가 무대 안 · 그림이 있는 문항은 남은 자리에 그림이 들어간다 · 그림 좌표가 그림 칸 안", () => {
    const B = m.L10_BOX, NUM = ["x", "y", "x2", "y2", "w", "h", "r"];
    for (const { meta, set } of ALL) for (const it of set.items) {
      const L = m.layoutOf(it), tag = `${meta.id} ${it.no}`;
      if (it.fig) assert.equal(L.noFig, false, `${tag} 글자를 다 놓고 남은 자리에 그림이 들어가지 않는다`);
      assert.ok(!L.scroll && L.bottom <= B.bottom + 1, `${tag} 아래로 넘침 (${Math.round(L.bottom)})`);
      for (const r of L.rows) for (const q of r.parts) assert.ok(q.x + q.w <= B.right + 2, `${tag} 줄이 오른쪽으로 넘침`);
      if (!it.fig) continue;
      for (const el of it.fig.els) {
        for (const k of NUM) if (el[k] != null) assert.ok(Number.isFinite(el[k]), `${tag} ${el.k}.${k}`);
        if (el.k !== "A" && el.x != null) assert.ok(el.x >= -40 && el.x <= 700, `${tag} ${el.k} x ${el.x}`);
        if (el.k !== "A" && el.y != null) assert.ok(el.y >= -40 && el.y <= 720, `${tag} ${el.k} y ${el.y}`);
        if (el.pts) for (const [px, py] of el.pts) assert.ok(px >= -40 && px <= 700 && py >= -40 && py <= 720, `${tag} P (${px}, ${py})`);
        for (const at of [el.at, el.un, el.mv?.at]) if (Number.isInteger(at)) assert.ok(at < it.lines.length, `${tag} at ${at} ≥ 줄 수`);
      }
    }
  });

  test("그리기 훑기: 넷 중 하나(6240문항) 다 푼 순간(어둠) · 그중 넷 중 하나는 문제 순간(밝음) — 오류 · NaN 없음", () => {
    let k = 0;
    for (const { meta, set } of ALL) for (const it of set.items) {
      if (k++ % 4) continue;
      const P = m.l10Plan(it), tag = `${meta.id} ${it.no}`;
      const s = m.art(it, P.ans + 900, "dark");
      assert.ok(s.length > 800 && !BAD.test(s), `${tag}: ${bad(s)}`);
      if (k % 16 === 1) {
        const s2 = m.art(it, 1500, "light");
        assert.ok(s2.length > 300 && !BAD.test(s2), `${tag} 문제: ${bad(s2)}`);
      }
    }
  });

  test("문서: 학년마다 세 회차 — 문제지 · 해설지 · 빠른 정답(20문항 · 코드 · @ashrain.out) · 등록 정보 · OMR 1쪽 · 받는 파일 이름", () => {
    const bases = new Set();
    for (const g of WGRADES) for (const i of [0, 47, 103]) {
      const meta = IDX[g.gk].sessions[i], set = SETS[meta.id], tag = meta.id, code = `${meta.code.slice(0, 3)}-${meta.code.slice(3)}`;
      const P = m.avDocHtml(meta, set, "problems", m.figPrint), S = m.avDocHtml(meta, set, "solutions", m.figPrint), A = m.avDocHtml(meta, set, "answers");
      for (const [nm, h] of [["문제지", P], ["해설지", S], ["빠른 정답", A]]) {
        const body = h.replace(/<style[\s\S]*?<\/style>/g, "");
        assert.ok(!BAD.test(body), `${tag} ${nm}: ${bad(body)}`);
        assert.ok(h.includes(`코드 ${code}`) && h.includes("@ashrain.out"), `${tag} ${nm} 코드 · 문구`);
      }
      assert.equal((P.match(/<div class="q">/g) || []).length, 20, `${tag} 문제 칸`);
      assert.equal((S.match(/<div class="s[ "]/g) || []).length, 20, `${tag} 해설 칸`);
      assert.equal((A.match(/<span class="no">/g) || []).length, 20, `${tag} 정답 칸`);
      assert.equal((S.match(/<svg/g) || []).length, set.items.filter((it) => it.fig).length, `${tag} 해설 그림 수`);
      assert.equal((P.match(/<svg/g) || []).length, set.items.filter((it) => it.qf).length, `${tag} 문제 그림 수`);
      const man = m.avManifest(meta, set);
      assert.equal(man.code, meta.code);
      assert.equal(man.items.length, 20);
      man.items.forEach((x, j) => assert.ok(x.answer && !x.answer.includes("−") && x.key === `av/${meta.id}/${j + 1}`, `${tag} ${x.no}`));
      const card = m.avCard(meta, set.items);
      assert.equal(card.pages.length, 1, `${tag} OMR ${card.pages.length}쪽`);
      assert.equal(m.avDownloadName(meta, "problems"), `${m.avFileBase(meta)}-문제지.pdf`);
      assert.ok(!/[\s·/\\:*?"<>|]/.test(m.avFileBase(meta)), m.avFileBase(meta));
      bases.add(m.avFileBase(meta));
    }
    assert.equal(bases.size, 36, "받는 파일 이름 겹침");
  });

  test("학생앱 항목: 회차 id 로 열면 학교급 기본기 액자 · 회차 카드(단원 · 학년 차례 · 주 · 종류 · 아이콘)", () => {
    const it = m.avItem("w-m2-11b");
    assert.equal(it.frame, "basic-m");
    assert.equal(it.set, "w-m2-11b");
    assert.equal(m.avItem("w-m2-99b"), null);
    const meta = IDX.m2.sessions[21];
    const c = m.weekCard(meta);
    assert.equal(c.key, meta.id);
    assert.equal(c.unit, meta.unit);
    assert.equal(c.gidx, 7);
    assert.equal(c.week, 11);
    assert.equal(c.icon, KIND_ICON[meta.kind]);
  });

  // 우물 추천 — 모든 회차 + 단원 100제를 한 바구니에
  const POOL = [...ALL.map((x) => m.weekCard(x.meta)), ...m.avOfCat("sol").filter((x) => x.unit).map(m.unitCard)];
  const RELS = new Set(["이어서", "앞 단원", "다음 단원", "같은 단원", "같은 주", "같은 학년", "약한 앞 단원", "지금 수준", "다음 단원 도전", "다시 볼 때"]);
  const sane = (item, cards, tag) => {
    assert.ok(cards.length <= m.MAX, `${tag} ${cards.length}개`);
    assert.ok(cards.every((c) => c.key !== item.key && RELS.has(c.rel)), `${tag} 자기 · 이유`);
    assert.equal(new Set(cards.map((c) => c.key)).size, cards.length, `${tag} 겹침`);
  };

  test("우물 추천(기본 — 기록 없음): 모든 회차 · 단원 100제에 6가지 · 자기 빼고 · 겹침 없음 · 앞 · 다음 단원이 섞인다", () => {
    assert.equal(m.MAX, 6);
    let six = 0, prev = 0, next = 0;
    for (const item of POOL) {
      const r = m.recommend(item, POOL, null);
      assert.equal(r.mode, "default");
      sane(item, r.cards, item.key);
      if (r.cards.length === 6) six++;
      if (r.cards.some((c) => c.rel === "앞 단원")) prev++;
      if (r.cards.some((c) => c.rel === "다음 단원")) next++;
    }
    assert.ok(six === POOL.length, `6가지가 다 차지 않은 항목 ${POOL.length - six}`);
    assert.ok(prev >= POOL.length * 0.85 && next >= POOL.length * 0.8, `앞 단원 ${prev} · 다음 단원 ${next} / ${POOL.length}`);
    // 이어서: 같은 단원의 다음 회차가 맨 앞
    const s = ALL.find((x) => x.meta.kind === "개념" && x.g.gk === "e4");
    const r = m.recommend(m.weekCard(s.meta), POOL, null);
    assert.equal(r.cards[0].rel, "이어서");
    assert.equal(r.cards[0].unit, s.meta.unit);
  });

  test("우물 추천(맞춤 — 기록이 넉넉함): 약한 앞 단원 먼저 · 숙달도가 높으면 다음 단원 도전 · 방금 본 것은 뒤로", () => {
    const item = m.weekCard(IDX.m2.sessions.find((x) => x.unit === "m2-1:일차함수" && x.kind === "연습"));
    const pu = prevUnits(item.unit), nu = nextUnits(item.unit);
    assert.ok(pu.length && nu.length);
    // 약한 앞 단원
    const weak = { mastery: { [item.unit]: { ok: 6, n: 10 }, [pu[0]]: { ok: 2, n: 12 } }, watched: {} };
    assert.equal(m.profileEnough(weak), true);
    assert.ok(Math.abs(m.masteryOf(weak, pu[0]) - 3 / 14) < 1e-9);
    const r1 = m.recommend(item, POOL, weak, { now: Date.UTC(2026, 10, 21) });
    assert.equal(r1.mode, "personal");
    sane(item, r1.cards, "약함");
    assert.equal(r1.cards.length, 6);
    assert.equal(r1.cards[0].rel, "약한 앞 단원");
    assert.ok(pu.includes(r1.cards[0].unit));
    // 높은 숙달도 → 다음 단원 도전
    const strong = { mastery: { [item.unit]: { ok: 19, n: 20 } }, watched: {} };
    const r2 = m.recommend(item, POOL, strong, { now: Date.UTC(2026, 10, 21) });
    sane(item, r2.cards, "강함");
    assert.ok(r2.cards.some((c) => c.rel === "다음 단원 도전" && nu.includes(c.unit)), r2.cards.map((c) => c.rel).join(","));
    assert.ok(r2.cards.filter((c) => c.unit === item.unit).length <= 3, "한 단원 셋까지");
    // 방금 본 것은 뒤로 — 맞춤 첫 추천을 어제 봤다면 그 카드는 빠진다(다른 후보가 넉넉하므로)
    const now = Date.UTC(2026, 10, 21);
    const first = r1.cards[0].key;
    const seen = { ...weak, watched: { [first]: { t: now - 86400000, v: 1, max: 20, n: 20 } } };
    const r3 = m.recommend(item, POOL, seen, { now });
    assert.ok(!r3.cards.slice(0, 3).some((c) => c.key === first), "어제 본 회차가 앞에 다시 나옴");
    // 기록이 모자라면 기본
    const thin = { mastery: { [item.unit]: { ok: 3, n: 5 } }, watched: { a: { t: now, v: 1, max: 20, n: 20 } } };
    assert.equal(m.profileEnough(thin), false);
    assert.equal(m.recommend(item, POOL, thin).mode, "default");
  });

  test("학생 기록 → 단원 숙달도: 개념의 단원 · 차례로 교과서 단원을 찾아 맞힌 수 · 푼 수를 모은다", () => {
    const u = m.unitOfConcept({ unit_id: "m2-1", sort_order: 1 });
    assert.ok(u && u.startsWith("m2-1:"), String(u));
    assert.equal(m.unitOfConcept({ unit_id: "zz", sort_order: 1 }), null);
    const items = new Map([[1, { concept_ids: [10] }], [2, { concept_ids: [10] }], [3, { concept_ids: [] }]]);
    const concepts = new Map([[10, { unit_id: "m2-1", sort_order: 1 }]]);
    const got = m.masteryFrom([{ item_id: 1, correct: true }, { item_id: 2, correct: false }, { item_id: 1, correct: true }, { item_id: 3, correct: true }, { item_id: 9, correct: true }], items, concepts);
    assert.deepEqual(got, { [u]: { ok: 2, n: 3 } });
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과 · 다시 계산한 등식 ${checks}개`);
if (failed) process.exit(1);
