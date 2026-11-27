// 시청각 해설 — 유형별 문제 세트 = 프린트마다 한 줄(기본기 단원 · 시그니처 프린트가 같은 서열) 시험.  node tests/display-prints.test.mjs
// ① 시그니처 프린트(frames/index.js 의 prints — 22장) — 해설 액자 여섯의 세트와 하나씩(같은 key · 차례) · 문항 수 n = 장면 수 · 번호 1 ~ n.
// ② 학생앱 항목(lib/av.js) — 프린트마다 #/av/<액자>:<세트> · cat sol · 해설 · 교과서 단원 · 학년 · n · 그 단원 바로 뒤 · 예전 액자 주소 · 우물 카드.
// ③ 재생 — 고른 프린트로 단일 모드(숫자 세트 lin10:2 도) · 본 기록은 프린트 key 로(printSeen: 처음 연 횟수 · 가장 멀리 · 다 봤음).
// ④ 듀얼 「전부」 — 프린트 key 풀이 · 이름표는 학생앱과 같은 이름 · 단계(1 ~ 5 · 10 · 없음) · 반쪽 판 장면 수 · 📄 원본 프린트(문제지 · 정답).
// ⑤ 기본기 해설 보기 칩 — 「🧩 유형」은 그 보기로 열렸을 때만(예전 주소) · 예전에 기억한 유형 보기는 유형별 문제 세트로.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

let n = 0, failed = 0;
async function test(name, fn) {
  n++;
  try { await fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.stack?.split("\n").slice(0, 3).join("\n   ") || e.message}`); }
}
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const J = (p) => JSON.stringify(path.join(ROOT, p));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-prints-"));

const store = {};
globalThis.localStorage = { getItem: (k) => store[k] ?? null, setItem: (k, v) => { store[k] = String(v); }, removeItem: (k) => { delete store[k]; } };
globalThis.fetch = async (url) => {
  const f = path.join(ROOT, "public", String(url).split("?")[0]);
  if (!fs.existsSync(f)) return { ok: false, status: 404, json: async () => null, arrayBuffer: async () => new ArrayBuffer(0) };
  const b = fs.readFileSync(f);
  return { ok: true, status: 200, json: async () => JSON.parse(b.toString("utf8")), arrayBuffer: async () => b.buffer.slice(b.byteOffset, b.byteOffset + b.length) };
};

try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${J("src/features/display/draw.jsx")};
import { Btn, Ic, FrameIc } from ${J("src/features/display/stage-ui.jsx")};
import { LessonFrame } from ${J("src/features/display/frames/lesson.jsx")};
import { BasicsFrame } from ${J("src/features/display/frames/basics.jsx")};
export { FRAMES, frameOf, printOf } from ${J("src/features/display/frames/index.js")};
export { BASICS, loadBasic } from ${J("src/features/display/basics/index.js")};
export { loadType } from ${J("src/lib/avtypes.js")};
export { WGRADES } from ${J("src/features/display/weeks/index.js")};
export { AV_ITEMS, avOfCat, avOfLevel, avItem, printItemOf, printSeen, unitCard, avRelated } from ${J("src/lib/av.js")};
export { hasPrint } from ${J("src/lib/avsrc.js")};
export { readHist, histDone } from ${J("src/lib/avHistory.js")};
export { recommend } from ${J("src/lib/recommend.js")};
export { unitLabel } from ${J("src/lib/units.js")};
export { allSpecFor, allSource, LESSON_FRAMES } from ${J("src/features/display/frames/allspec.jsx")};
export { basicsSpec } from ${J("src/features/display/frames/basics.jsx")};
const props = (th) => ({ C: PALETTE[th], ui: { Btn, Ic, FrameIc }, ctl: true, poke: () => {}, inert: false, isFs: false, toggleFs: () => {},
  onTheme: () => {}, onGallery: () => {}, onExit: () => {}, mode: "m", onMode: () => {} });
export const frame = (spec, th, pick = null) => renderToStaticMarkup(<LessonFrame spec={spec} pick={pick} {...props(th)} />);
export const basics = (lv, th, pick = null) => renderToStaticMarkup(<BasicsFrame lv={lv} pick={pick} {...props(th)} />);
export const menu = (spec, cur, side = "왼쪽") => { const M = spec.Menu; return renderToStaticMarkup(<M spec={spec} cur={cur} side={side} onPick={() => {}} onClose={() => {}} />); };
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent",
    define: { "process.env.NODE_ENV": '"production"', "import.meta.env": JSON.stringify({ VITE_SUPABASE_URL: "http://localhost:1", VITE_SUPABASE_ANON_KEY: "test" }) },
    loader: { ".js": "jsx" },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{60}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  const LESSONS = m.FRAMES.filter((f) => f.lesson && !f.basics);
  const PR = LESSONS.flatMap((f) => f.prints.map((p) => ({ f, p, key: `${f.key}:${p.set}` })));
  const specOf = (fk) => m.LESSON_FRAMES.find((F) => F.fk === fk).spec;

  await test("시그니처 프린트 — 해설 액자 여섯의 세트와 하나씩(같은 key · 차례) · 모두 22장 · 문항 수 n = 장면 수 · 번호 1 ~ n · 이름 겹침 없음", async () => {
    assert.deepEqual(LESSONS.map((f) => f.key), m.LESSON_FRAMES.map((F) => F.fk), "해설 액자 여섯 = 듀얼 「전부」의 액자 여섯");
    for (const f of LESSONS) {
      assert.deepEqual(f.prints.map((p) => p.set), specOf(f.key).sets.map((S) => S.key), `${f.key} 세트 key(숫자는 숫자로)`);
      for (const p of f.prints) {
        assert.ok(p.title && p.short && p.icon && p.desc && p.n > 0, `${f.key}:${p.set} 이름 · 그림 · 설명 · 문항 수`);
        const S = specOf(f.key);
        if (S.ready && !S.ready(p.set)) await S.load(p.set);               // 세트 문항을 고를 때 들여오는 액자(두 점 → 식 · 교점 · 만날 조건)
        const sc = S.scenes(p.set, 1, 0);
        assert.equal(sc.length, p.n, `${f.key}:${p.set} 장면 수`);
        assert.deepEqual(sc.map((x) => x.no).sort((a, b) => a - b), Array.from({ length: p.n }, (_, i) => i + 1), `${f.key}:${p.set} 번호 1 ~ n`);
        assert.equal(m.printOf(f.key, String(p.set)), p, `${f.key}:${p.set} printOf`);
        assert.ok(!/순열|조합|여사건|배반|√|\d!/.test(p.title + p.desc), `${f.key}:${p.set} 중2 용어`);
      }
    }
    assert.equal(PR.length, 22);
    const sol = m.avOfCat("sol");
    assert.equal(new Set(sol.map((x) => x.title)).size, sol.length, "유형별 문제 세트 이름 겹침");
    for (const { key } of PR) { const it = m.avItem(key); assert.equal(sol.filter((x) => x.short === it.short).length, 1, `${key} 짧은 이름 겹침`); }
  });

  await test("학생앱 항목 — 프린트마다 한 줄(#/av/<액자>:<세트>) · 기본기 단원과 같은 서열(cat sol · 해설 · 단원 · 학년 · n) · 그 단원 바로 뒤 · 예전 액자 주소", () => {
    const sol = m.avOfCat("sol"), keys = sol.map((x) => x.key);
    for (const { f, p, key } of PR) {
      const it = m.avItem(key);
      assert.ok(it && it.sig, key);
      assert.equal(it, sol.find((x) => x.key === key), `${key} 목록의 그 항목`);
      assert.equal(it.frame, f.key);
      assert.equal(it.set, p.set, `${key} 세트 key 그대로(${typeof p.set})`);
      assert.equal(it.cat, "sol"); assert.equal(it.kind, "해설");
      assert.equal(it.level, "중등"); assert.equal(it.grade, "중2"); assert.equal(it.unit, f.unit); assert.equal(it.n, p.n);
      assert.equal(it.title, p.title); assert.equal(it.icon, p.icon);
      assert.equal(m.printItemOf(f.key, String(p.set)), it, `${key} printItemOf`);
      assert.equal(m.hasPrint(key), false, `${key} 앱 프린트 문서 없음`);
      // 그 단원(after) 뒤에 이어서 — 사이에 기본기 단원이 끼지 않는다
      const i = keys.indexOf(f.after), j = keys.indexOf(key);
      assert.ok(i >= 0 && j > i && keys.slice(i + 1, j).every((k) => sol.find((x) => x.key === k).sig), `${key} 은 ${f.after} 바로 뒤 묶음`);
    }
    for (const b of m.BASICS) assert.equal(m.avItem(b.id).n, b.n || 100, `${b.id} 문항 수`);
    for (const f of LESSONS) {
      const it = m.avItem(f.key);
      assert.ok(it && it.frame === f.key && it.set == null && !it.sig, `#/av/${f.key} 예전 주소 → 그 액자(기억한 세트)`);
      assert.ok(!keys.includes(f.key), `${f.key} 액자 자체는 목록에 없음`);
    }
  });

  await test("우물 카드 · 추천 — 프린트도 유형별 문제 세트 카드(중2 · kind 단원) · 프린트를 누르면 같은 · 앞 · 다음 단원 6가지(자기 빼고)", () => {
    const pool = m.avOfCat("sol").map(m.unitCard);
    const g = m.WGRADES.findIndex((x) => x.grade === "중2");
    const none = { mastery: {}, watched: {} };
    for (const { key } of PR) {
      const c = m.unitCard(m.avItem(key));
      assert.equal(c.gidx, g, `${key} 학년 차례`);
      assert.equal(c.kind, "단원");
      const r = m.recommend(c, pool, none).cards;
      assert.ok(r.length >= 3 && r.length <= 6 && r.every((x) => x.key !== key), `${key} 추천 ${r.length}`);
      assert.equal(new Set(r.map((x) => x.key)).size, r.length, `${key} 추천 겹침`);
      const rel = m.avRelated(m.avItem(key), 6);
      assert.ok(rel.length >= 1 && rel.every((x) => x.key !== key), `${key} 단원 지도 추천`);
    }
    // 같은 단원의 기본기 단원을 누르면 시그니처 프린트도 추천에 든다
    const r = m.recommend(m.unitCard(m.avItem("m-prob")), pool, none).cards.map((x) => x.key);
    assert.ok(r.some((k) => k.startsWith("cnt100:")), `확률 단원 → 경우의 수와 확률 100제: ${r.join(" ")}`);
  });

  await test("재생 — 고른 프린트로 단일 모드부터(숫자 세트 lin10:2 · 문자 세트 cnt100:lex) · 듀얼을 기억해도 단일 · 두 테마 오류 없음", () => {
    store["ash.display.lin10.mode"] = JSON.stringify("dual");
    for (const th of ["dark", "light"]) {
      const h2 = m.frame(specOf("lin10"), th, 2);
      assert.ok(/aria-checked="true">세트 2</.test(h2), "세트 2 로");
      assert.ok(!h2.includes('class="lsn-pane-ctl'), "고르면 단일");
      const hx = m.frame(specOf("cnt100"), th, "lex");
      assert.ok(/aria-checked="true">사전식</.test(hx), "사전식으로");
      const hb = m.frame(specOf("area"), th, "B");
      assert.ok(/aria-checked="true">240제</.test(hb), "240제로");
      for (const h of [h2, hx, hb]) assert.ok(!BAD.test(h), bad(h));
    }
    delete store["ash.display.lin10.mode"];
  });

  await test("본 기록 — 프린트 key 로(처음 본 세트는 연 횟수 +1 · 가장 멀리 본 번호 · n) · 액자 안에서 세트를 옮기면 그 프린트로 · 80% 면 다 봤음", () => {
    delete store["ash.av.hist"];
    const seen = m.printSeen("cnt100");
    seen("sel", 1); seen("sel", 2); seen("sel", 7); seen("sel", 3);
    let h = m.readHist();
    assert.equal(h["cnt100:sel"].v, 1, "연 횟수 한 번");
    assert.equal(h["cnt100:sel"].max, 7);
    assert.equal(h["cnt100:sel"].n, 100);
    assert.ok(!m.histDone(h["cnt100:sel"]));
    seen("ball", 4);
    h = m.readHist();
    assert.ok(h["cnt100:ball"] && h["cnt100:ball"].v === 1 && h["cnt100:ball"].max === 4, "옮긴 세트의 프린트");
    seen("nope", 3); seen("sel", 0);
    assert.equal(Object.keys(m.readHist()).length, 2, "없는 세트 · 0번은 남기지 않음");
    const s10 = m.printSeen("lin10");
    s10(2, 160);
    h = m.readHist();
    assert.equal(h["lin10:2"].n, 200); assert.ok(m.histDone(h["lin10:2"]), "200 중 160 = 80% → 다 봤음");
    delete store["ash.av.hist"];
  });

  await test("듀얼 「전부」 — 프린트 key 풀이 · 이름표는 학생앱과 같은 이름 · 단계(1 ~ 5 · 10 · 없음) · 반쪽 판 장면 수 = n · 📄 원본 프린트", () => {
    const A = m.allSpecFor(m.basicsSpec("m"));
    for (const { f, p, key } of PR) {
      const r = m.allSource(key);
      assert.ok(r && r.kind === "frame" && r.set === p.set, key);
      const L = A.setOf(key), it = m.avItem(key);
      assert.equal(L.name, it.title); assert.equal(L.short, it.short); assert.equal(L.icon, it.icon); assert.equal(L.sub, m.unitLabel(it.unit));
      assert.deepEqual(A.stages(key).map((x) => x.v), specOf(f.key).stages(p.set).map((x) => x.v), `${key} 단계`);
      assert.equal(A.scenes(key, 1, 0).length, p.n, `${key} 장면`);
      const tx = A.topExtra({ set: key, open: false, onOpen() {}, poke() {} });
      assert.ok(tx && tx.props.sig?.key === key && tx.props.sig.code === p.code, `${key} 📄 원본 프린트(코드 ${p.code})`);
      const fx = specOf(f.key).topExtra({ set: p.set, open: false, onOpen() {}, poke() {} });
      assert.ok(fx && fx.props.sig?.key === key, `${key} 해설 액자 오른쪽 위 📄`);
    }
    assert.deepEqual(A.stages("cnt100:sel").map((x) => x.v), [1, 2, 3, 4, 5]);
    assert.equal(A.stages("lin10:1").length, 10);
    assert.deepEqual(A.stages("graph:hard"), []);
    // 목록: 어느 액자에서 나눠도 같은 「전체」 목록 — 기본기 단원 · 시그니처 프린트 한 차례
    const ROW = /class="lsn-set( on)?( hot)?( sig)?"/g;
    const want = m.avOfCat("sol").length;
    for (const F of m.LESSON_FRAMES) {
      const S = m.allSpecFor(F.spec), cur = `${F.fk}:${F.spec.sets[0].key}`;
      const h = m.menu(S, cur);
      assert.equal((h.match(ROW) || []).length, want, `${F.fk} 에서 나눈 목록`);
      assert.equal((h.match(/class="lsn-set on( sig)?"/g) || []).length, 1, `${F.fk} 지금 것 하나`);
      assert.ok(!BAD.test(h), bad(h));
    }
    const sig = (m.menu(A, "m-lin").match(/class="lsn-set( on)?( hot)? sig"/g) || []).length;
    assert.equal(sig, 22, "시그니처 프린트 줄 22");
  });

  await test("기본기 해설 보기 칩 — 「🧩 유형」은 유형 보기로 열렸을 때만 · 예전에 기억한 유형 보기는 유형별 문제 세트로 · 주차별 학년은 그대로", async () => {
    await m.loadBasic("e-ten"); await m.loadType("e-ten.3");
    store["ash.display.basic.e.view"] = JSON.stringify("types");
    const h = m.basics("basic-e", "dark");
    assert.ok(h.includes('title="단원 목록 (U)"') && !h.includes('title="유형 목록 (U)"'), "기억한 유형 보기 → 유형별 문제 세트 " + (h.match(/title="[^"]*목록 \(U\)"/g) || []).join(","));
    const t = m.basics("basic-e", "dark", "e-ten.3");
    assert.ok(t.includes('title="유형 목록 (U)"'), "예전 주소(#/av/e-ten.3) → 유형 보기");
    store["ash.display.basic.e.view"] = JSON.stringify("e3");
    const w = m.basics("basic-e", "dark");
    assert.ok(w.includes("초3 주차별 기초 다지기") && !w.includes('title="단원 목록 (U)"'), "기억한 주차별 학년은 그대로");
    delete store["ash.display.basic.e.view"];
    for (const x of [h, t, w]) assert.ok(!BAD.test(x), bad(x));
  });
} catch (e) {
  failed++;
  console.log("✗ 준비 실패\n  ", e.stack?.split("\n").slice(0, 4).join("\n   "));
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
