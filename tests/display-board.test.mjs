// node tests/display-board.test.mjs — 해설 액자의 공통 틀(frames/lesson.jsx)과 글자 판 배치(board.js) 검산. 실패 시 exit 1.
// ① 조작이 모두 같다: 해설 액자(lesson — 일차함수 셋 · 경우의 수 100제 · 기본기 해설 초등 · 중등 · 고등)가 같은 틀로 단일 · 듀얼을 그리고,
//    같은 단추(보기 · 세트(기본기는 단원 목록) · 빠르기 0.75× ~ 2× · 목록 · 두 막대 · ⇄)를 가진다.
// ② 글자 크기: 두 벌(기본 · 촘촘)뿐 — 판서 37 이상 · 문제 36 이상(약 1 m 에서 읽히게), 방침 칸 글자도 같은 벌.
// ③ 그림: 글자를 다 놓고 남은 빈자리에 — 글자 칸과 겹치지 않고, 화면(단일 무대 · 듀얼 반쪽)의 25% 이하, 배율 0.6 이상, 판 안.
// ④ 넘치는 판: 무대는 두 단, 그래도 넘치면(또 반쪽 판) 판서가 흐른다 — 흐르는 동안 지금 줄이 늘 보이는 칸 안에 있다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "display-board-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src/features/display", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("draw.jsx")};
import { Btn, Ic, FrameIc } from ${F("stage-ui.jsx")};
import { FRAMES } from ${F("frames/index.js")};
import { boardLayout, boardScroll, STAGE_REGION, PANE_REGION, BOARD_TYPE, FIG_AREA, FIG_MIN, wrapMath } from ${F("board.js")};
import { LessonFrame, LESSON_SPEEDS, paneLoad } from ${F("frames/lesson.jsx")};
import { layoutOf as l10Layout } from ${F("frames/lin10.jsx")};
import { layoutOf as areaLayout } from ${F("frames/area.jsx")};
import { L10_SPEC } from ${F("frames/lin10.jsx")};
import { C100_SPEC } from ${F("frames/cnt100.jsx")};
import { AREA_SPEC } from ${F("frames/area.jsx")};
import { GD_SPEC } from ${F("frames/graphdraw.jsx")};
import { basicsSpec } from ${F("frames/basics.jsx")};
import { LEVELS, BASICS, loadBasic, basicCached } from ${F("basics/index.js")};
import { l10Plan } from ${F("lin10.js")};
import { arPlan, AREA_SETS } from ${F("area.js")};
import { L10_SETS } from ${F("lin10.js")};
import { C100_SETS } from ${F("cnt100.js")};
export { FRAMES, boardLayout, boardScroll, STAGE_REGION, PANE_REGION, BOARD_TYPE, FIG_AREA, FIG_MIN, wrapMath, LESSON_SPEEDS, paneLoad, l10Plan, arPlan };
export const SPECS = { lin10: L10_SPEC, cnt100: C100_SPEC, area: AREA_SPEC, graph: GD_SPEC,
  ...Object.fromEntries(LEVELS.map((L) => [L.frame, basicsSpec(L.key)])) };
export const loadAll = () => Promise.all(BASICS.map((b) => loadBasic(b.id)));
export const loadOne = (id) => loadBasic(id);
export const basicReady = (id) => !!basicCached(id);
/** 글자 판 가족 — [이름, 문항들, 배치(문항, 판), 박자표] (기본기 단원은 들여온 뒤에) */
export const fams = () => [
  ["lin10", Object.values(L10_SETS).flatMap((s) => s.items), l10Layout, l10Plan],
  ["cnt100", Object.values(C100_SETS).flatMap((s) => s.items), l10Layout, l10Plan],
  ["area", Object.values(AREA_SETS).flatMap((s) => s.items), areaLayout, arPlan],
  ["basics", BASICS.flatMap((b) => basicCached(b.id).items), l10Layout, l10Plan],
];
const props = (th) => ({ C: PALETTE[th], ui: { Btn, Ic, FrameIc }, ctl: true, poke: () => {}, inert: false, isFs: false, toggleFs: () => {},
  onTheme: () => {}, onGallery: () => {}, onExit: () => {}, mode: "m", onMode: () => {} });
export const frame = (spec, th) => renderToStaticMarkup(<LessonFrame spec={spec} {...props(th)} />);
export const framePick = (spec, pick, th) => renderToStaticMarkup(<LessonFrame spec={spec} pick={pick} {...props(th)} />);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    loader: { ".js": "jsx" },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const store = {};
  globalThis.localStorage = { getItem: (k) => store[k] ?? null, setItem: (k, v) => { store[k] = String(v); }, removeItem: (k) => { delete store[k]; } };
  const m = await import(pathToFileURL(out).href);
  const BAD = /NaN|undefined|Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{50}(NaN|undefined|Infinity|\[object Object\]).{30}/) || [""])[0];
  const LESSONS = m.FRAMES.filter((f) => f.lesson).map((f) => f.key);
  const FAMS0 = { v: null };

  // 기본기 단원: 단일 · 듀얼 첫 그림이 「불러오는 중」인지 먼저 보고, 그다음 다 들여온다
  for (const L of ["basic-e", "basic-m", "basic-h"]) {
    const S = m.SPECS[L];
    test(`${S.title}: 단원 문항을 들여오기 전에는 「불러오는 중」(단일 · 듀얼)`, () => {
      for (const mode of ["single", "dual"]) {
        store[S.lsk + ".mode"] = JSON.stringify(mode);
        const h = m.frame(S, "dark");
        assert.ok(h.includes("불러오는 중") && !BAD.test(h), `${L} ${mode}`);
      }
      delete store[S.lsk + ".mode"];
    });
  }
  await m.loadAll();
  const FAMS = m.fams();

  test("해설 액자 일곱이 모두 공통 틀 — 세트 · 단계 · 장면(반쪽 판 그리기 · 풀이 눈금 · 목록 글자 · 큰 제목)", () => {
    assert.equal(LESSONS.length, 7);
    assert.deepEqual(m.LESSON_SPEEDS, [0.75, 1, 1.5, 2]);
    const lsks = new Set();
    for (const k of LESSONS) {
      const S = m.SPECS[k];
      assert.ok(S, `${k} 틀 설정`);
      assert.ok(S.lsk && !lsks.has(S.lsk), `${k} 기억 이름`); lsks.add(S.lsk);
      assert.ok(S.title && S.sets.length >= 1, k);
      for (const set of S.sets) {
        assert.ok(set.name && set.short, `${k} 세트 이름`);
        const st = S.stages(set.key);
        for (const sp of m.LESSON_SPEEDS) {
          const L = S.scenes(set.key, sp, 0);
          assert.ok(L.length >= 60, `${k}/${set.key} 장면 수 ${L.length}`);
          if (sp !== 1 || (S.setMenu && set.key !== S.sets[0].key && set.key !== S.sets.at(-1).key)) continue;
          assert.equal(new Set(L.map((x) => x.key)).size, L.length, `${k} 장면 key`);
          for (const sc of L) {
            assert.equal(typeof sc.pane, "function", `${k} ${sc.no} 반쪽 판 그리기`);
            assert.equal(sc.tsz, "lesson", `${k} ${sc.no} 큰 제목`);
            assert.ok(sc.marks?.length >= 3 && sc.card, `${k} ${sc.no} 눈금 · 목록 글자`);
          }
          if (sp === 1) for (const x of st) assert.ok(S.scenes(set.key, 1, x.v).every((sc) => sc.st === x.v), `${k} ${x.lab} 만`);
        }
      }
    }
  });

  test("단일 · 듀얼 그리기: 일곱 액자 모두 같은 단추(보기 · 세트/단원 · 빠르기 넷 · 목록 · 두 막대 · 듀얼은 판마다 · ⇄) — 두 테마 오류 없음", () => {
    let cnt = 0;
    for (const k of LESSONS) {
      const S = m.SPECS[k];
      for (const mode of ["single", "dual"]) {
        store[S.lsk + ".mode"] = JSON.stringify(mode);
        for (const th of ["dark", "light"]) {
          const h = m.frame(S, th);
          cnt++;
          assert.ok(!BAD.test(h), `${k} ${mode} ${th}: ${bad(h)}`);
          for (const w of ["단일", "듀얼", "0.75×", "1×", "1.5×", "2×", "번호 · 단계 목록", "scb-long", "scb-short"]) assert.ok(h.includes(w), `${k} ${mode} — ${w} 없음`);
          if (S.setMenu) assert.ok(h.includes("lsn-unit") && h.includes(`${S.setMenu.word} 목록 (U)`), `${k} ${mode} 단원 단추`);
          else if (S.sets.length > 1) for (const set of S.sets) assert.ok(h.includes(`>${set.short}<`), `${k} ${mode} 세트 ${set.short}`);
          if (mode === "dual") {
            assert.equal((h.match(/class="lsn-pane-ctl /g) || []).length, 2, `${k} 판 조작 둘`);
            assert.ok(h.includes("lsn-swap") && h.includes("자리 바꾸기"), `${k} ⇄`);
            assert.equal((h.match(/class="scb-long /g) || []).length, 2, `${k} 판마다 긴 막대`);
            assert.ok(h.includes("왼쪽 빠르기") && h.includes("오른쪽 빠르기"), `${k} 판마다 빠르기`);
          } else assert.ok(h.includes("이 장면 반복") && h.includes("dsp-ctl"), `${k} 단일 조작`);
          if (S.topExtra) assert.ok(h.includes('aria-label="문서"'), `${k} ${mode} 📄 문서`);
        }
      }
      delete store[S.lsk + ".mode"];
    }
    console.log(`   액자 그림 ${cnt}장`);
  });

  test("학생앱에서 고른 단원(pick)으로 단일 모드부터 · 단원 목록 단추 · 판 기억은 그대로", () => {
    const S = m.SPECS["basic-m"], id = S.sets[5].key;
    store[S.lsk + ".mode"] = JSON.stringify("dual");
    const h = m.framePick(S, id, "light");
    assert.ok(h.includes("이 장면 반복") && !h.includes('class="lsn-pane-ctl'), "고른 단원은 단일 모드로");
    assert.ok(h.includes(S.sets[5].short), "고른 단원 이름");
    delete store[S.lsk + ".mode"];
  });

  test("판 기억: 듀얼 판은 기본 왼쪽 앞에서 1.5× · 오른쪽 가운데부터 0.75× · 저장한 자리에서 벽시계로 이어 돈다(모든 액자)", () => {
    const now = 1_700_000_000_000;
    for (const k of LESSONS) {
      const S = m.SPECS[k], set = S.sets.at(-1).key;
      const l = m.paneLoad(S, null, "L", set, now), r = m.paneLoad(S, null, "R", set, now);
      assert.deepEqual([l.set, l.sp, l.i, l.held], [set, 1.5, 0, null], k);
      assert.equal(r.sp, 0.75);
      assert.equal(r.i, Math.floor(S.scenes(set, 0.75, 0).length / 2));
      const L = S.scenes(set, 2, 0);
      const o = { set, st: 0, sp: 2, i: 1, t0: now - (L[1].dur + L[2].dur + 400), held: null, rep: false };
      const p = m.paneLoad(S, o, "R", S.sets[0].key, now);
      assert.deepEqual([p.set, p.sp, p.i, now - p.t0], [set, 2, 3, 400], k);
      assert.equal(m.paneLoad(S, { ...o, sp: 3 }, "L", set, now).sp, 1, `${k} 모르는 빠르기는 1×`);
    }
  });

  test("글자 크기: 두 벌(기본 · 촘촘)뿐 · 판서 37 이상 · 문제 36 이상 · 머리말 · 메모 28 이상", () => {
    assert.equal(m.BOARD_TYPE.length, 2);
    for (const T of m.BOARD_TYPE) assert.ok(T.b >= 37 && T.q >= 36 && T.s >= 28 && T.plan >= 29, T.key);
    const cnt = {};
    for (const [fam, items, lay] of FAMS) for (const R of [m.STAGE_REGION, m.PANE_REGION]) for (const it of items) {
      const L = lay(it, R);
      assert.ok(m.BOARD_TYPE.includes(L.T), `${fam} ${it.no} 정해진 글자 크기가 아님`);
      const key = `${R.key} ${L.type}`;
      cnt[key] = (cnt[key] || 0) + 1;
    }
    console.log(`   ${Object.entries(cnt).map(([a, b]) => `${a} ${b}`).join(" · ")}`);
  });

  test("그림 자리: 글자 칸과 겹치지 않음 · 판 안 · 화면의 25% 이하 · 배율 0.6 이상(단일 무대 · 듀얼 반쪽)", () => {
    const rep = [];
    for (const [fam, items, lay] of FAMS) for (const R of [m.STAGE_REGION, m.PANE_REGION]) {
      let has = 0, want = 0, areaSum = 0;
      const screen = R.key === "pane" ? 800 * 900 : 1600 * 900;
      for (const it of items) {
        if (!it.fig) continue;
        want++;
        const L = lay(it, R), f = L.fig, tag = `${fam} ${R.key} ${it.no}`;
        if (!f) continue;
        has++;
        const fb = [f.x, f.y, f.x + f.w, f.y + f.h];
        assert.ok(fb[0] >= R.left - 50 && fb[2] <= R.right + 1 && fb[1] >= L.qBottom && fb[3] <= R.bottom + 1, `${tag} 그림이 판 밖 ${fb.map(Math.round)}`);
        // 흐르는 판(꼭 보여야 하는 그림 — 사전식 카드)은 글자가 흐르는 칸(잘라 보이는 곳)과 그림이 겹치지 않으면 된다
        const S = L.scroll;
        const boxes = S ? L.boxes.filter((b) => b[1] < S.bottom && b[3] > S.top).map((b) => [b[0], Math.max(b[1], S.top), b[2], Math.min(b[3], S.bottom)]) : L.boxes;
        const textR = Math.max(...L.boxes.filter((b) => b[1] >= L.qBottom - 2).map((b) => b[2]));     // 문제 아래 글자(방침 · 판서 · 답)의 오른쪽 끝
        if (S) assert.ok(fb[1] >= S.bottom - 1 || fb[0] >= textR - 1, `${tag} 흐르는 글자 칸과 그림이 겹침`);
        else for (const b of boxes) assert.ok(fb[0] >= b[2] - 1 || fb[2] <= b[0] + 1 || fb[1] >= b[3] - 1 || fb[3] <= b[1] + 1, `${tag} 그림이 글자와 겹침`);
        assert.ok(f.w * f.h <= m.FIG_AREA * screen + 1, `${tag} 그림이 화면의 25%를 넘음 (${Math.round((100 * f.w * f.h) / screen)}%)`);
        assert.ok(f.s >= m.FIG_MIN - 1e-9 && f.s <= 1 + 1e-9, `${tag} 배율 ${f.s}`);
        assert.ok(!L.two, `${tag} 두 단인 판에 그림`);
        if (L.scroll) assert.ok(fam === "cnt100" && it.fig.kind === "tree", `${tag} 흐르는 판에 그림(꼭 보여야 하는 사전식 카드만)`);
        areaSum += (f.w * f.h) / screen;
      }
      if (want) rep.push(`${fam} ${R.key} ${has}/${want}(평균 ${Math.round((100 * areaSum) / Math.max(1, has))}%)`);
      if (R.key === "stage" && want) assert.ok(has >= want * 0.9, `${fam} 단일 모드에서 그림이 빠진 문항이 많다 ${want - has}`);
      if (fam === "cnt100") {                        // 사전식 카드는 꼭 — 단일 · 반쪽 모두
        const lex = items.filter((it) => it.fig?.kind === "tree");
        assert.ok(lex.every((it) => lay(it, R).fig), `사전식 카드 그림이 빠진 문항 (${R.key})`);
      }
    }
    console.log(`   ${rep.join(" · ")}`);
  });

  test("넘치는 판: 무대는 두 단 먼저(흐름은 드물게) · 흐르는 판은 줄이 나타날 때마다 그 줄이 보이는 칸 안에", () => {
    let two = 0, flow = 0, checks = 0;
    for (const [fam, items, lay, plan] of FAMS) for (const R of [m.STAGE_REGION, m.PANE_REGION]) for (const it of items) {
      const L = lay(it, R), tag = `${fam} ${R.key} ${it.no}`;
      if (L.two) { two++; assert.equal(R.key, "stage", `${tag} 두 단은 무대에서만`); assert.ok(L.bottom <= R.bottom + 1, `${tag} 두 단도 넘침`); }
      if (!L.scroll) continue;
      flow++;
      const P = plan(it), S = L.scroll;
      let prev = 0;
      L.rows.forEach((r, i) => {
        const t = (P.lines[i + 1] ? P.lines[i + 1].a : P.ans) - 10;
        const off = m.boardScroll(L, P, t);
        assert.ok(off >= prev - 0.01, `${tag} 거꾸로 흐름`);
        prev = off;
        assert.ok(r.bot - off <= S.bottom + 1 && r.top - off >= S.top - 4, `${tag} ${i}번째 줄이 보이는 칸 밖 (${Math.round(r.top - off)} ~ ${Math.round(r.bot - off)})`);
        checks++;
      });
      const offEnd = m.boardScroll(L, P, P.dur);
      assert.ok(L.bottom - offEnd <= S.bottom + 1, `${tag} 답 칸이 보이지 않음`);
    }
    console.log(`   두 단 ${two} · 흐르는 판 ${flow} · 줄 확인 ${checks}`);
    const stageFlow = FAMS.reduce((a, [, items, lay]) => a + items.filter((it) => { const L = lay(it, m.STAGE_REGION); return L.scroll && !L.fig; }).length, 0);
    assert.ok(stageFlow <= 8, `무대에서 흐르는 판이 많다(${stageFlow})`);
  });

  test("줄 바꾸기: 판 폭을 넘지 않고(끊을 수 없는 한 덩이 말고) · 식은 「=」 앞에서 · 괄호 · 좌표 가운데는 끊지 않음", () => {
    const rows = m.wrapMath("x^{3} × x^{4} = x^{3 + 4} = x^{7} = x × x × x × x × x × x × x", 42, 520, 560, true);
    assert.ok(rows.length >= 2 && rows.slice(1).every((r) => r.startsWith("=")), rows.join(" | "));
    const q = m.wrapMath("두 점 (0, −8), (1, 0)을 지나는 직선: y = 8x − 8", 40, 420, 560, true);
    assert.ok(q.every((r) => (r.match(/\(/g) || []).length === (r.match(/\)/g) || []).length), q.join(" | "));
    assert.deepEqual(m.wrapMath("짧은 줄", 40, 900), ["짧은 줄"]);
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
