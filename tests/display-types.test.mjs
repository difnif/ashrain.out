// node tests/display-types.test.mjs — 유형별 문제 세트의 유형 · 꾹 눌러 프린트 받기 · 듀얼 「문제 풀이 해설 전부」 검산. 실패 시 exit 1.
// ① 유형 = 단원의 한 단계 20문항(lib/avtypes.js): 단원 100가지 × 5 = 500 · 유형마다 교과서 단원 · 학년 · 프린트 코드(6글자 — 단원 · 회차 · 유형끼리 겹치지 않음)
//    · 번호 1 ~ 20(원래 번호는 src) · 학생앱 주소 #/av/<단원>.<단계> · 문제지 · 해설지 · 빠른 정답 · OMR 에 유형 코드 · 「20문항 · n단계」.
// ② 프린트 받기: 프린트가 있는 것(단원 · 유형 · 회차)만 「📄 프린트」 · 단원은 PDF 받기, 유형 · 회차는 바로 인쇄 창 · 받기 판 첫 그림.
// ③ 우물 추천: 유형도 카드로 섞이고, 유형별 문제 세트 ↔ 그 단원의 유형(서로 품은 사이)은 서로 추천하지 않는다 · 자리(키 낮은 화면에서 위 · 아래 띠 비우기).
// ④ 기본기 해설 「🧩 유형」 보기(typesSpec) · 학생앱에서 고른 유형으로 열기 · 본 기록(단원을 보면 그 문항의 유형에도).
// ⑤ 듀얼 모드 「문제 풀이 해설 전부」(frames/allspec.jsx): 어느 해설 액자에서 나눠도 판마다 유형별 문제 세트 · 유형 · 주차별 회차 · 해설 액자 세트 —
//    key 풀이 · 이름표 · 단계 · 장면 · 들여오기 · 📄(단원 · 유형 · 회차만) · 목록(탭 넷 · 학교급 · 학년) · 예전 듀얼 기억 옮기기 · 그리기 오류 없음.
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
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-types-"));

// 브라우저 대신 — localStorage 는 메모리, fetch 는 public/ 파일
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
export { BASICS, LEVELS, basicOf, loadBasic, basicCached } from ${J("src/features/display/basics/index.js")};
export { TYPE_TAGS } from ${J("src/features/display/basics/typetags.js")};
export { parseTypeKey, typeKey, typeMeta, typeSet, loadType, typesOf } from ${J("src/lib/avtypes.js")};
export { avSource, hasPrint } from ${J("src/lib/avsrc.js")};
export { avItem, typeItem, typeCard, unitCard, weekCard, typesOfLevel, avOfLevel } from ${J("src/lib/av.js")};
export { recommend } from ${J("src/lib/recommend.js")};
export { TERM_LABEL } from ${J("src/lib/units.js")};
export { readHist } from ${J("src/lib/avHistory.js")};
export { avDocHtml, avManifest, avCard, fmtCode } from ${J("src/features/display/frames/avprint.js")};
export { prerendered, avFileBase, avDownloadName } from ${J("src/features/display/frames/docsmenu.jsx")};
export { WGRADES, loadWeekIndex, loadWeek, weekMetaCached, weekCached } from ${J("src/features/display/weeks/index.js")};
export { wellLayout } from ${J("src/components/WellPick.jsx")};
import { DocsMenu } from ${J("src/features/display/frames/docsmenu.jsx")};
import { typesSpec, basicsSpec, weeksSpec, BasicsFrame, TYPE_NO, noteBasicSeen } from ${J("src/features/display/frames/basics.jsx")};
import { LessonFrame, paneLoad, setOfSpec } from ${J("src/features/display/frames/lesson.jsx")};
import { allSpecFor, allSource, LESSON_FRAMES } from ${J("src/features/display/frames/allspec.jsx")};
import { GD_SPEC } from ${J("src/features/display/frames/graphdraw.jsx")};
import { L10_SPEC } from ${J("src/features/display/frames/lin10.jsx")};
import AvPrintSheet from ${J("src/components/AvPrintSheet.jsx")};
export { typesSpec, basicsSpec, weeksSpec, TYPE_NO, noteBasicSeen, paneLoad, setOfSpec, allSpecFor, allSource, LESSON_FRAMES, GD_SPEC, L10_SPEC };
const props = (th) => ({ C: PALETTE[th], ui: { Btn, Ic, FrameIc }, ctl: true, poke: () => {}, inert: false, isFs: false, toggleFs: () => {},
  onTheme: () => {}, onGallery: () => {}, onExit: () => {}, mode: "m", onMode: () => {} });
export const frame = (spec, th, pick = null) => renderToStaticMarkup(<LessonFrame spec={spec} pick={pick} {...props(th)} />);
export const basics = (lv, th, pick = null) => renderToStaticMarkup(<BasicsFrame lv={lv} pick={pick} {...props(th)} />);
export const menu = (spec, cur, side = "왼쪽") => { const M = spec.Menu; return renderToStaticMarkup(<M spec={spec} cur={cur} side={side} onPick={() => {}} onClose={() => {}} />); };
export const docs = (meta, set) => renderToStaticMarkup(<DocsMenu meta={meta} set={set} open onOpen={() => {}} />);
export const sheet = (key) => renderToStaticMarkup(<AvPrintSheet itemKey={key} onClose={() => {}} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent",
    // 우물(WellPick → Well.jsx)이 supabase 를 들인다 — 가짜 주소(테스트는 부르지 않는다)
    define: { "process.env.NODE_ENV": '"production"', "import.meta.env": JSON.stringify({ VITE_SUPABASE_URL: "http://localhost:1", VITE_SUPABASE_ANON_KEY: "test" }) },
    loader: { ".js": "jsx" },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{60}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  const ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
  await Promise.all(m.BASICS.map((b) => m.loadBasic(b.id)));
  const TYPES = m.BASICS.flatMap((b) => m.typesOf(b.id));

  /* ══════════ ① 유형 ══════════ */
  await test("유형 500가지 — 단원 100가지 × 1 ~ 5단계 · 교과서 단원 · 학년 · 코드 6글자(단원 · 회차 · 유형끼리 겹치지 않음 · 코드 기록과 같음)", () => {
    assert.equal(m.BASICS.length, 100);
    assert.equal(TYPES.length, 500);
    const tcodes = JSON.parse(fs.readFileSync(path.join(ROOT, "avgen/tcodes.json"), "utf8"));
    const wcodes = JSON.parse(fs.readFileSync(path.join(ROOT, "avgen/wcodes.json"), "utf8"));
    const ucodes = JSON.parse(fs.readFileSync(path.join(ROOT, "avgen/codes.json"), "utf8"));
    const others = new Set([...m.BASICS.map((b) => b.code), ...Object.values(wcodes), ...Object.values(ucodes)]);
    const seen = new Set();
    for (const b of m.BASICS) {
      assert.ok(m.TYPE_TAGS[b.id], `${b.id} 유형 꼬리표`);
      for (const st of [1, 2, 3, 4, 5]) {
        const k = m.typeKey(b.id, st), t = m.typeMeta(k), [unit, code] = m.TYPE_TAGS[b.id][st];
        assert.deepEqual(m.parseTypeKey(k), { id: b.id, st }, k);
        assert.ok(t && t.id === k && t.base === b.id && t.st === st && t.n === 20, `${k} 머리 정보`);
        assert.equal(t.level, b.level, `${k} 학교급`);
        assert.equal(t.unit, unit, `${k} 교과서 단원`);
        const [term, name] = unit.split(":");
        assert.ok(m.TERM_LABEL[term] && name, `${k} 교과서 단원 ${unit}`);
        assert.equal(t.span, `${{ e: "초", m: "중", h: "고" }[term[0]]}${term[1]}`, `${k} 학년 = 교과서 단원의 학년(고등도 과목 이름이 아니라 학년)`);
        assert.ok(m.WGRADES.some((g) => g.grade === t.span), `${k} 학년 ${t.span}`);
        assert.ok(/^[A-Z0-9]{6}$/.test(code) && [...code].every((c) => ALPHA.includes(c)), `${k} 코드 ${code}`);
        assert.equal(tcodes[k], code, `${k} 코드 기록`);
        assert.ok(!others.has(code), `${k} 코드가 단원 · 회차 코드와 겹침 ${code}`);
        assert.ok(!seen.has(code), `${k} 코드 겹침 ${code}`); seen.add(code);
        assert.equal(t.name, b.stages[st]);
        assert.equal(t.title, `${b.title} — ${st}단계 ${b.stages[st]}`);
        assert.equal(t.short, `${b.short} ${st}단계`);
      }
    }
    for (const bad0 of ["e-ten", "e-ten.0", "e-ten.6", "x-none.1", "e-ten.3x", "", null, "w-e3-07a"]) assert.equal(m.parseTypeKey(bad0), null, String(bad0));
  });

  await test("유형 문항 — 그 단계 20문항을 1 ~ 20번으로(원래 번호 src · 단계 · 정답 그대로) · 지도 도움말 · 단계 팁", () => {
    for (const t of TYPES) {
      const S = m.typeSet(t.id), U = m.basicCached(t.base);
      const src = U.items.filter((x) => x.st === t.st);
      assert.equal(S.items.length, 20, t.id);
      assert.equal(src.length, 20, `${t.id} 단원의 그 단계`);
      S.items.forEach((it, i) => {
        assert.equal(it.no, i + 1, `${t.id} 번호`);
        assert.equal(it.src, src[i].no, `${t.id} 원래 번호`);
        assert.equal(it.st, t.st);
        assert.equal(it.ap, src[i].ap);
      });
      assert.equal(S.pp, U.pp);
      assert.equal(S.note, U.note);
      assert.deepEqual(Object.keys(S.tips), [String(t.st)]);
      assert.equal(m.typeSet(t.id), S, "한 번 만들면 그대로");
    }
  });

  await test("학생앱 주소 #/av/<단원>.<단계> — 그 학교급 기본기 액자를 그 유형으로 · 카드(우물) · 학교급 목록", () => {
    for (const t of TYPES) {
      const it = m.avItem(t.id);
      assert.ok(it, t.id);
      assert.equal(it.frame, m.LEVELS.find((L) => L.level === t.level).frame, `${t.id} 액자`);
      assert.equal(it.set, t.id);
      assert.equal(it.kind, "유형");
      assert.equal(it.cat, "sol");
      assert.equal(it.unit, t.unit);
      const c = m.typeCard(t);
      assert.equal(c.key, t.id);
      assert.equal(c.base, t.base);
      assert.equal(c.kind, "유형");
      assert.ok(c.gidx != null && c.week === 60 + t.st, `${t.id} 카드 학년 · 차례`);
    }
    assert.equal(["초등", "중등", "고등"].reduce((s, lv) => s + m.typesOfLevel(lv).length, 0), 500);
    for (const lv of ["초등", "중등", "고등"]) {
      const units = m.avOfLevel(lv).filter((x) => m.basicOf(x.key));
      assert.equal(m.typesOfLevel(lv).length, units.length * 5, lv);
      for (const x of m.avOfLevel(lv).filter((y) => !m.basicOf(y.key))) assert.equal(m.typesOf(x.key).length, 0, `${x.key} 해설 액자는 유형 없음`);
    }
  });

  await test("유형 프린트 — 문제지 · 해설지 · 빠른 정답 · OMR · 등록 정보에 유형 코드 · 「20문항 · n단계」 · 번호 1 ~ 20 · 파일 이름", () => {
    for (const k of ["e-ten.3", "m-lin.5", "h-count.1", TYPES[137].id, TYPES[388].id]) {
      const t = m.typeMeta(k), S = m.typeSet(k), code = m.fmtCode(t.code);
      for (const doc of ["problems", "solutions", "answers"]) {
        const h = m.avDocHtml(t, S, doc, () => "<svg></svg>");
        assert.ok(h.includes(code), `${k} ${doc} 코드`);
        assert.ok(h.includes(`20문항 · ${t.st}단계`), `${k} ${doc} 머리말`);
        assert.ok(!BAD.test(h), `${k} ${doc}: ${bad(h)}`);
        assert.ok(!h.includes(m.fmtCode(m.basicOf(t.base).code)), `${k} ${doc} 단원 코드가 섞임`);
      }
      const man = m.avManifest(t, S);
      assert.equal(man.code, t.code);
      assert.equal(man.items.length, 20);
      assert.deepEqual(man.items.map((x) => x.no), Array.from({ length: 20 }, (_, i) => String(i + 1)));
      assert.ok(man.items.every((x, i) => x.key === `av/${k}/${i + 1}`), `${k} 등록 key`);
      assert.ok(man.sub.includes("20문항") && man.sub.includes(`${t.st}단계`), man.sub);
      const card = JSON.stringify(m.avCard(t, S.items));
      assert.ok(card.includes(code) && card.includes("20제"), `${k} OMR`);
      assert.ok(m.avDownloadName(t, "problems").includes(`${t.st}단계`), m.avDownloadName(t, "problems"));
      assert.notEqual(m.avFileBase(t), m.avFileBase(m.basicOf(t.base)), "유형 · 단원 파일 이름이 다르다");
    }
  });

  /* ══════════ ② 프린트 받기 ══════════ */
  await m.loadWeekIndex("e3"); await m.loadWeek("w-e3-07a");
  await test("프린트가 있는 것: 단원 · 유형 · 회차(해설 액자는 없음) · PDF 를 미리 찍는 것은 유형별 문제 세트뿐", () => {
    const u = m.avSource("e-ten"), t = m.avSource("e-ten.3"), w = m.avSource("w-e3-07a");
    assert.deepEqual([u.kind, t.kind, w.kind], ["unit", "type", "week"]);
    assert.ok(u.ready() && t.ready() && w.ready(), "들여온 뒤 ready");
    assert.equal(t.set().items.length, 20);
    assert.equal(w.meta().id, "w-e3-07a");
    for (const k of ["graph", "lin10", "area", "cnt100", "basic-e", "hanoi", "", "nope"]) assert.equal(m.hasPrint(k), false, k);
    for (const k of ["e-ten", "m-lin.2", "w-m2-30b"]) assert.equal(m.hasPrint(k), true, k);
    assert.equal(m.prerendered(m.basicOf("e-ten")), true);
    assert.equal(m.prerendered(m.typeMeta("e-ten.3")), false);
    assert.equal(m.prerendered(m.weekMetaCached("w-e3-07a")), false);
  });

  await test("받기 판(학생앱)과 액자 📄 — 첫 그림: 문서 넷 · 유형 코드 · 문항 수 · 오류 없음", () => {
    for (const k of ["e-ten", "e-ten.3", "w-e3-07a"]) {
      const h = m.sheet(k), S = m.avSource(k), meta = S.meta();
      assert.ok(!BAD.test(h), `${k}: ${bad(h)}`);
      for (const w of ["문제지", "해설지", "빠른 정답", "OMR", "확인", m.fmtCode(meta.code), `${S.set().items.length}문항`]) assert.ok(h.includes(w), `${k} 받기 판 — ${w}`);
      const d = m.docs(meta, S.set());
      assert.ok(d.includes(m.fmtCode(meta.code)) && d.includes(`${S.set().items.length}제`) && !BAD.test(d), `${k} 📄`);
    }
    assert.ok(m.sheet("e-ten.3").includes("유형 · 프린트 받기"));
    assert.ok(m.sheet("w-e3-07a").includes("주차별 회차 · 프린트 받기"));
  });

  /* ══════════ ③ 우물 ══════════ */
  await test("우물 추천: 유형이 섞인 더미에서 6가지 · 유형별 문제 세트 ↔ 그 단원의 유형은 서로 추천하지 않음(같은 단원 다른 유형은 됨)", () => {
    const pool = [...m.BASICS.map((b) => m.unitCard(m.avItem(b.id))), ...TYPES.map(m.typeCard)];
    const none = { mastery: {}, watched: {} };
    for (const b of m.BASICS.slice(0, 40)) {
      const r = m.recommend(m.unitCard(m.avItem(b.id)), pool, none);
      assert.equal(r.cards.length, 6, b.id);
      assert.ok(r.cards.every((c) => c.base !== b.id && c.key !== b.id), `${b.id} 자기 유형을 추천`);
    }
    let sib = 0;
    for (const t of TYPES.filter((_, i) => i % 7 === 0)) {
      const r = m.recommend(m.typeCard(t), pool, none);
      assert.equal(r.cards.length, 6, t.id);
      assert.ok(r.cards.every((c) => c.key !== t.base && c.key !== t.id), `${t.id} 자기 단원을 추천`);
      if (r.cards.some((c) => c.base === t.base)) sib++;
    }
    assert.ok(sib > 0, "같은 단원의 다른 유형도 추천된다");
  });

  await test("우물 자리: 키 낮은 화면(가로 휴대폰)에서도 위 띠(누른 것 · 📄 프린트) · 아래 띠(안내)를 비움 · 큰 화면은 그대로", () => {
    for (const [vw, vh] of [[390, 844], [360, 640], [844, 390], [740, 360], [1280, 800], [1920, 1080], [820, 1180]]) {
      const L = m.wellLayout(6, vw, vh);
      const ys = L.pos.map((p) => p.y);
      assert.ok(Math.min(...ys) - L.ch / 2 >= 76 - 1e-9 || vh < 330, `${vw}×${vh} 위 카드가 위 띠에 ${Math.min(...ys) - L.ch / 2}`);
      assert.ok(Math.max(...ys) + L.ch / 2 <= vh - 46 + 1e-9, `${vw}×${vh} 아래 카드가 안내 띠에`);
      assert.ok(L.cy - L.D / 2 >= Math.min(...ys) + L.ch / 2, `${vw}×${vh} 위 카드와 우물이 겹침`);
    }
    const tall = m.wellLayout(6, 390, 844);
    assert.equal(Math.round(tall.pos[0].y), Math.round(844 / 2 - Math.min(Math.max(844 * 0.3, 150), 270)), "큰 화면은 예전 자리");
  });

  /* ══════════ ④ 유형 보기 ══════════ */
  await test("기본기 해설 「🧩 유형」 보기 — 학교급마다 단원 × 5 · 단원마다 묶은 목록 · 장면 20(1 ~ 20번) · 단계 칩 없음 · 📄 은 유형 프린트", () => {
    for (const L of m.LEVELS) {
      const S = m.typesSpec(L.key), units = m.BASICS.filter((b) => b.level === L.level);
      assert.equal(S.sets.length, units.length * 5, L.key);
      assert.equal(new Set(S.sets.map((x) => x.grp)).size, units.length, `${L.key} 단원마다 묶음`);
      assert.equal(S.dualLsk, m.basicsSpec(L.key).dualLsk, "듀얼 기억은 단원 보기와 같이");
      for (const x of S.sets.filter((_, i) => i % 9 === 0)) {
        const sc = S.scenes(x.key, 1, 0);
        assert.equal(sc.length, 20, x.key);
        assert.deepEqual(sc.map((y) => y.no), Array.from({ length: 20 }, (_, i) => i + 1));
        assert.equal(new Set(sc.map((y) => y.key)).size, 20);
        assert.deepEqual(S.stages(x.key), []);
        assert.ok(x.icon === m.TYPE_NO[m.typeMeta(x.key).st]);
      }
    }
  });

  await test("학생앱에서 고른 유형으로 열기(단일 · 그 유형 이름) · 단원 · 회차 pick 은 예전 그대로 · 두 테마 오류 없음", () => {
    store["ash.display.type.e.mode"] = JSON.stringify("dual");      // 고르면 단일로
    for (const th of ["dark", "light"]) {
      const h = m.basics("basic-e", th, "e-ten.3");
      assert.ok(!BAD.test(h), bad(h));
      assert.ok(h.includes("10 만들기 3단계") && h.includes("유형 목록 (U)") && h.includes("이 장면 반복"), "유형 단일");
      assert.ok(h.includes(m.fmtCode(m.typeMeta("e-ten.3").code)) || h.includes('aria-label="문서"'), "📄");
      const u = m.basics("basic-e", th, "e-ten");
      assert.ok(u.includes("단원 목록 (U)") && u.includes("10 만들기"), "단원 단일");
      const w = m.basics("basic-e", th, "w-e3-07a");
      assert.ok(w.includes("회차 목록 (U)") && !BAD.test(w), "회차 단일");
    }
    delete store["ash.display.type.e.mode"];
  });

  /* ══════════ ⑤ 듀얼 — 문제 풀이 해설 전부 ══════════ */
  const ORIGINS = [m.GD_SPEC, m.L10_SPEC, m.basicsSpec("e"), m.basicsSpec("m"), m.typesSpec("h"), m.weeksSpec("e3")];
  await test("「전부」 key 풀이 — 단원 · 유형 · 회차 · 해설 액자 세트(graph:basic · lin10:1 …) · 모르는 것은 없음", () => {
    assert.equal(m.allSource("e-ten").kind, "unit");
    assert.equal(m.allSource("m-lin.4").kind, "type");
    assert.equal(m.allSource("w-h2-40b").kind, "week");
    for (const F of m.LESSON_FRAMES) for (const S of F.spec.sets) {
      const r = m.allSource(`${F.fk}:${S.key}`);
      assert.ok(r && r.kind === "frame" && r.set === S.key && r.fs === F.spec, `${F.fk}:${S.key}`);
    }
    assert.equal(m.allSource("lin10:1").set, 1, "10단계 세트 key 는 수");
    for (const k of ["graph:none", "nope:1", "graph", "e-ten.9", "w-e3-60a", ""]) assert.equal(m.allSource(k), null, k);
  });

  await test("듀얼 처음 — 예전 듀얼 기억(이 액자 세트끼리)은 「전부」 key 로 옮겨 온다(한 번) · 기억이 없으면 두 판 다 단일에서 보던 것", () => {
    const now = Date.now(), C = m.LESSON_FRAMES.find((f) => f.fk === "cnt100").spec, [k1, k2] = [C.sets[1].key, C.sets[0].key];
    store["ash.display.cnt100.dual"] = JSON.stringify({ L: { set: k1, st: 3, sp: 1.5, i: 4, t0: now, held: null, rep: false }, R: { set: k2, st: 0, sp: 1, i: 0, t0: now, held: null, rep: true } });
    const A = m.allSpecFor(C);
    const moved = JSON.parse(store["ash.display.cnt100.all.dual"]);
    assert.deepEqual([moved.L.set, moved.L.st, moved.L.i, moved.R.set, moved.R.rep], [`cnt100:${k1}`, 3, 4, `cnt100:${k2}`, true]);
    const p = m.paneLoad(A, moved.L, "L", A.defSet, now);
    assert.deepEqual([p.set, p.st, p.i], [`cnt100:${k1}`, 3, 4]);
    store[C.lsk + ".mode"] = JSON.stringify("dual");
    const h = m.frame(C, "dark");
    assert.ok(!BAD.test(h) && (h.match(/class="lsn-pane-ctl /g) || []).length === 2, bad(h));
    assert.ok(h.includes(m.setOfSpec(A, `cnt100:${k1}`).short), "옮겨 온 왼쪽 판");
    delete store[C.lsk + ".mode"]; delete store["ash.display.cnt100.dual"]; delete store["ash.display.cnt100.all.dual"];
    // 기억 없음 — 단일에서 보던 세트
    store["ash.display.area"] = JSON.stringify({ set: "B", sp: 1, st: 0 });
    const B = m.allSpecFor(m.LESSON_FRAMES.find((f) => f.fk === "area").spec);
    assert.equal(m.paneLoad(B, null, "R", B.single0(), now).set, "area:B");
    delete store["ash.display.area"];
  });

  await test("「전부」 spec — 액자마다 하나 · 기억 이름(기본기 해설은 보기 셋이 한 기억) · 처음엔 단일 모드에서 보던 것", () => {
    const g = m.allSpecFor(m.GD_SPEC);
    assert.equal(g, m.allSpecFor(m.GD_SPEC), "한 번만 만든다");
    assert.equal(g.lsk, "ash.display.graph.all");
    assert.equal(g.defSet, "graph:basic");
    store["ash.display.graph"] = JSON.stringify({ set: "hard", sp: 1, st: 0 });
    assert.equal(g.single0(), "graph:hard");
    assert.equal(m.allSpecFor(m.L10_SPEC).defSet, "lin10:1");
    const e = m.allSpecFor(m.basicsSpec("e")), t = m.allSpecFor(m.typesSpec("e")), w = m.allSpecFor(m.weeksSpec("e3"));
    assert.ok(e.lsk === t.lsk && t.lsk === w.lsk && e.lsk === "ash.display.basic.e.all", "기본기 보기 셋 = 한 듀얼 기억");
    store["ash.display.type.e"] = JSON.stringify({ set: "e-col.2", sp: 1, st: 0 });
    assert.equal(t.single0(), "e-col.2");
    delete store["ash.display.graph"]; delete store["ash.display.type.e"];
  });

  await test("「전부」 spec — 이름표 · 단계 · 장면(반쪽 판 그리기) · 들여오기 · 목록 칸 · 액자 이름", async () => {
    const A = m.allSpecFor(m.basicsSpec("m"));
    const keys = ["e-ten", "m-lin.3", "w-e3-07a", "graph:basic", "graph:hard", "lin10:2", "area:B", "cnt100:sel"];
    for (const k of keys) {
      assert.ok(A.hasSet(k), k);
      if (!A.ready(k)) await A.load(k);
      assert.ok(A.ready(k), `${k} 들여옴`);
      const S = m.setOfSpec(A, k);
      assert.ok(S && S.key === k && S.name && S.short && !BAD.test(JSON.stringify(S)), `${k} 이름표 ${JSON.stringify(S)}`);
      const L = A.scenes(k, 1, 0);
      assert.ok(L.length >= 20 && L.every((s) => typeof s.pane === "function" && s.dur > 0), `${k} 장면`);
      for (const x of A.stages(k)) assert.ok(A.scenes(k, 1, x.v).every((s) => s.st === x.v), `${k} ${x.lab}`);
      assert.ok(A.titleOf(k) && A.colsOf(k) >= 5, `${k} 액자 이름 · 칸`);
    }
    assert.equal(A.scenes("m-lin.3", 1, 0).length, 20);
    assert.deepEqual(A.stages("m-lin.3"), []);
    assert.equal(A.stages("e-ten").length, 5);
    assert.equal(A.titleOf("e-ten"), "초등 기본기 해설");
    assert.equal(A.titleOf("w-e3-07a"), "초3 주차별 기초 다지기");
    assert.equal(A.titleOf("graph:basic"), m.GD_SPEC.title);
    assert.equal(A.colsOf("graph:basic"), m.GD_SPEC.cols);
    assert.ok(A.paneHead(m.setOfSpec(A, "graph:basic"), A.scenes("graph:basic", 1, 0)[0]), "그래프 액자 판 머리");
    assert.equal(A.paneHead(m.setOfSpec(A, "e-ten"), A.scenes("e-ten", 1, 0)[0]), null);
    assert.equal(A.topExtra({ set: "graph:basic", open: false, onOpen() {}, poke() {} }), null, "해설 액자 세트는 📄 없음");
    assert.ok(A.topExtra({ set: "m-lin.3", open: false, onOpen() {}, poke() {} }), "유형 📄");
  });

  await test("듀얼 그리기 — 어느 해설 액자에서 나눠도 판마다 「콘텐츠」 단추 · 왼쪽 그래프 액자 + 오른쪽 초등 유형처럼 섞어도 오류 없음 · 📄 은 프린트 있는 판만", () => {
    for (const O of ORIGINS) {
      const A = m.allSpecFor(O);
      store[O.lsk + ".mode"] = JSON.stringify("dual");
      store[A.lsk + ".dual"] = JSON.stringify({ L: { set: "graph:hard", st: 0, sp: 1, i: 3, t0: Date.now() - 500, held: null, rep: false },
        R: { set: "e-ten.3", st: 0, sp: 0.75, i: 5, t0: Date.now() - 900, held: null, rep: false } });
      for (const th of ["dark", "light"]) {
        const h = m.frame(O, th);
        assert.ok(!BAD.test(h), `${O.lsk} ${th}: ${bad(h)}`);
        assert.equal((h.match(/class="lsn-pane-ctl /g) || []).length, 2, `${O.lsk} 판 둘`);
        assert.equal((h.match(/콘텐츠 목록 \(U\)/g) || []).length, 2, `${O.lsk} 판마다 콘텐츠 단추`);
        assert.ok(h.includes("그래프 그리기 심화 64") && h.includes("10 만들기 3단계"), `${O.lsk} 두 판 이름`);
        assert.equal((h.match(/aria-label="문서"/g) || []).length, 1, `${O.lsk} 📄 은 유형 판만`);
        assert.ok(h.includes("6번") || h.includes("4번"), `${O.lsk} 판 머리 번호`);
      }
      delete store[O.lsk + ".mode"]; delete store[A.lsk + ".dual"];
    }
  });

  await test("듀얼 판 목록 — 탭 둘(유형별 문제 세트 프린트 전부 · 주차별) · 유형별 문제 세트는 「전체」부터(시그니처 프린트도 같은 서열) · 지금 것 표시", () => {
    const A = m.allSpecFor(m.basicsSpec("e"));
    const ROW = /class="lsn-set( on)?( hot)?( sig)?"/g;
    const u = m.menu(A, "m-lin");
    for (const w of ["문제 풀이 해설 전부", "📚 유형별 문제 세트", "🗓 주차별", "전체", "초등", "중등", "고등", "왼쪽 판"]) assert.ok(u.includes(w), `목록 — ${w}`);
    for (const w of ["🧩 유형", "🎬 해설 액자"]) assert.ok(!u.includes(w), `탭 없음 — ${w}`);
    assert.equal((u.match(ROW) || []).length, m.BASICS.length + 21, "전체 = 기본기 단원 100 + 시그니처 프린트 21");
    assert.ok(u.includes('class="lsn-set on"') && u.includes("일차함수"), "지금 단원 표시");
    for (const w of ["학년별 선발 100", "그래프 그리기 심화 64", "10단계 계산 세트 2", "그래프와 넓이 240", "초등 · 유형별 문제 세트 36", "중등 · 유형별 문제 세트 51"]) assert.ok(u.includes(w), `전체 목록 — ${w}`);
    const f = m.menu(A, "cnt100:ball");
    assert.ok(f.includes('class="lsn-set on sig"') && f.includes("주머니 공 100"), "지금 시그니처 프린트 표시");
    assert.equal((f.match(ROW) || []).length, m.BASICS.length + 21, "시그니처 프린트에서 열어도 전체");
    const t = m.menu(A, "e-ten.3");
    assert.ok(t.includes('class="lsn-set on"'), "예전 유형 기억 → 그 단원 줄");
    const w = m.menu(A, "w-e3-07a");
    assert.equal((w.match(ROW) || []).length, 104, "초3 104회차");
    assert.ok(w.includes("1학기") && w.includes("겨울방학"), "학기 · 방학 묶음");
    for (const h of [u, f, t, w]) assert.ok(!BAD.test(h), bad(h));
  });

  await test("본 기록 — 유형을 열면 그 유형 key(1 ~ 20) · 단원을 보면 그 문항이 든 유형에도(유형 안 번호) · 회차는 예전 그대로", () => {
    delete store["ash.av.hist"];
    const U = m.basicCached("e-col"), it = U.items.find((x) => x.st === 4 && x.no % 20 === 7);
    const T = m.typeSet("e-col.4"), r = T.items.findIndex((x) => x.src === it.no) + 1;
    m.noteBasicSeen("e-col", it.no, true);
    let h = m.readHist();
    assert.deepEqual([h["e-col"].v, h["e-col"].max, h["e-col"].n], [1, it.no, 100], "단원");
    assert.deepEqual([h["e-col.4"].max, h["e-col.4"].n], [r, 20], "그 문항의 유형");
    assert.ok(!h["e-col.3"] && !h["e-col.5"], "다른 유형은 그대로");
    m.noteBasicSeen("e-col.2", 12, true);
    m.noteBasicSeen("e-col.2", 5, false);
    h = m.readHist();
    assert.deepEqual([h["e-col.2"].v, h["e-col.2"].max, h["e-col.2"].n], [1, 12, 20], "유형 — 가장 멀리 본 번호");
    m.noteBasicSeen("w-e3-07a", 20, true);
    assert.deepEqual([m.readHist()["w-e3-07a"].max, m.readHist()["w-e3-07a"].n], [20, 20], "회차");
    m.noteBasicSeen("graph", 3, true);
    assert.ok(!m.readHist().graph, "모르는 세트는 남기지 않음");
    delete store["ash.av.hist"];
  });

  console.log(`\n${n - failed}/${n} 통과`);
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
if (failed) process.exit(1);
