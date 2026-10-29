// 컨셉 문제 「해설 영상」 — 장면(videoScenes.jsx) 노드 테스트
//   node tests/conceptsets-video.test.mjs
// 세트 38개 × 50문항 = 1900장면을 만들어, 박자 지점마다 두 테마로 그려 보고(오류 · NaN 없음) 배치가 무대 안에 드는지,
// 글자 변환이 꼬리표를 남기지 않는지, 도식 큐가 짚는 키가 도식에 있는지 본다. 글자 폭은 노드에서 어림치(draw.jsx estimate)로 잰다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = path.join(ROOT, "public/concept-sets/prob");
let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 6).join("\n      ")); }
}

const INDEX = JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf8"));
const SETS = INDEX.categories[0].sets.map((s) => JSON.parse(fs.readFileSync(path.join(DIR, `${String(s.no).padStart(2, "0")}.json`), "utf8")));

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "csv-test-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const P = (p) => JSON.stringify(path.join(ROOT, p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { solutionScenes, activeKeys, toStage, wrapStage, parseTbl, hiCss, DG_BOX } from ${P("src/pages/sets/videoScenes.jsx")};
import { PALETTE, SceneTitle, mathWidth } from ${P("src/features/display/draw.jsx")};
export { solutionScenes, activeKeys, toStage, wrapStage, parseTbl, hiCss, mathWidth, DG_BOX };
export const frame = (sc, t, th) => renderToStaticMarkup(<g><SceneTitle title={sc.title.m} sub={sc.sub.m} C={PALETTE[th]} mode="m" />{sc.render("m", t, PALETTE[th])}</g>);
`);
  const out = path.join(tmp, "bundle.mjs");
  await build({
    entryPoints: [entry], bundle: true, platform: "node", format: "esm", jsx: "automatic", outfile: out,
    nodePaths: [path.join(ROOT, "node_modules")], logLevel: "silent", define: { "process.env.NODE_ENV": '"production"' },
    banner: { js: "import { createRequire as __cr } from 'module'; const require = __cr(import.meta.url);" },
  });
  const m = await import(pathToFileURL(out).href);

  console.log("글자");
  test("toStage: 분수 · 강조 · nw(붙은 빈칸) · 엔티티 · 꼬리표", () => {
    assert.equal(m.toStage('확률은 <span class="fr"><span class="n">5</span><span class="d">36</span></span>이다.'), "확률은 {5/36}이다.");
    assert.equal(m.toStage('<span class="nw">3 : 1</span> 승패 &#x27;처음&#x27; <b>답</b> 2*3'), "3 : 1 승패 '처음' ‹답› 2∗3");
    assert.equal(m.toStage('<span class="fr"><span class="n">2 × 3</span><span class="d">36</span></span>'), "{2 × 3/36}");
  });
  test("wrapStage: 폭 안 · 강조가 줄을 넘으면 다시 연다 · 분수 덩어리는 쪼개지 않는다", () => {
    const s = "가나다 라마바 ‹사아자 차카타 파하› 끝 {12/35}{12/35}{12/35}";
    const L = m.wrapStage(s, 30, 200);
    assert.ok(L.length >= 3);
    for (const x of L) {
      assert.ok(m.mathWidth(x, 30, 560) <= 200 + 1 || !x.includes(" "), x);
      assert.equal((x.match(/‹/g) || []).length, (x.match(/›/g) || []).length, x);
      assert.ok(!/\{[^}]*$/.test(x) && !/^[^{]*\}/.test(x), "분수가 쪼개졌다: " + x);
    }
  });
  test("hiCss: 그림 id 안에서만 · data-k / data-ka · 잘못된 선택자 없음", () => {
    const css = m.hiCss("cvd-07-3", new Set(["row:0", "hi"]), 0.6);
    assert.ok(css.startsWith("<style>") && css.endsWith("</style>"));
    const rules = css.slice(7, -8).split("}").filter(Boolean);
    for (const r of rules) for (const sel of r.split("{")[0].split(",")) {
      assert.ok(sel.startsWith("#cvd-07-3 "), sel);
      assert.ok(!/\]\w/.test(sel), "꼬리표가 속성 뒤에 붙은 선택자: " + sel);
    }
    assert.ok(css.includes('[data-ka~="hi"]') && css.includes('[data-k="row:0"]'));
    assert.equal(m.hiCss("x", new Set()), "");
  });

  const ALL = SETS.map((set) => ({ set, scenes: m.solutionScenes(set) }));
  const stat = { size: {}, lhSquash: 0, bigK: 0, tblK: 0, laps: [] };

  console.log("장면");
  test("세트마다 50장면 · 키 중복 없음 · 길이 25~100초 · 제목 줄에 분수 괄호 · 꼬리표 없음", () => {
    const keys = new Set();
    for (const { set, scenes } of ALL) {
      assert.equal(scenes.length, 50, set.short);
      for (const sc of scenes) {
        assert.ok(!keys.has(sc.key), sc.key); keys.add(sc.key);
        assert.ok(Number.isFinite(sc.dur) && sc.dur >= 25000 && sc.dur <= 100000, `${sc.key} ${sc.dur}`);
        for (const s of [sc.title.m, sc.sub.m]) assert.ok(!/[{}<>]|&\w+;/.test(s), `${sc.key}: ${s}`);
      }
      stat.laps.push(scenes.reduce((a, s) => a + s.dur, 0) / 60000);
    }
  });

  const BAD = /NaN|undefined|Infinity/;   // (「null²」은 실제 전시관 이름이라 null 은 보지 않는다)
  const TAGS = /<[a-z/][^>]*>|&(amp|lt|gt|quot|#x27|#39|nbsp);/i;
  for (const { set, scenes } of ALL) {
    const tag = `${String(set.no).padStart(2, "0")} ${set.short}`;
    test(`${tag}: 그리기 훑기(박자 지점 × 두 테마 · 오류 · NaN 없음) · 배치가 무대 안 · 글자 변환 · 도식 큐`, () => {
      for (const sc of scenes) {
        const T = sc.timing, L = sc.layout(), it = set.items.find((x) => `${set.key}-${x.id}` === sc.key);
        const id = sc.key;
        // 박자 순서
        const marks = [0, T.tA, T.tPos, T.tNeg, T.tPlan, T.tB, ...T.steps.map((s) => s.t), T.tC, T.tChk, T.tAns, T.dur];
        for (let i = 1; i < marks.length; i++) assert.ok(marks[i] > marks[i - 1], `${id} 박자 ${i}: ${marks.join(",")}`);
        for (let i = 1; i < T.caps.length; i++) assert.ok(T.caps[i].t >= T.caps[i - 1].t, `${id} 자막 순서`);
        // 그리기
        const times = [0, 1500, T.tA - 1, T.tA + 400, T.tA + 1200, T.tPos + 300, T.tNeg + 300, T.tPlan + 300, T.tB - 1,
          ...T.steps.map((s) => s.t + 400), T.tC - 1, T.tC + 300, T.tChk + 300, T.tAns + 300, T.dur - 1, T.dur];
        for (const th of ["dark", "light"]) for (const t of th === "dark" ? times : [0, T.tA + 1200, T.steps[0]?.t + 400 || T.tB, T.dur]) {
          const s = m.frame(sc, t, th);
          assert.ok(!BAD.test(s), `${id} ${th} t=${t}: ${(s.match(/.{60}(NaN|undefined|Infinity).{40}/) || [""])[0]}`);
        }
        // 글자 변환: 꼬리표 · 엔티티 · 짝 없는 분수 괄호가 남지 않는다
        const texts = [T.q, ...T.rows.flat(), ...T.box, ...T.board.flatMap((b) => [b.h, b.t]), T.pos, T.neg, T.pl, T.check, T.ans,
          ...(T.tbl ? [...T.tbl.head, ...T.tbl.rows.flat(), T.tbl.foot] : [])];
        for (const x of texts) {
          assert.ok(!TAGS.test(x), `${id} 꼬리표: ${x}`);
          // 분수 {a/b} 를 빼고 남은 괄호는 글자 그대로(집합 {건, 곤} 같은) — 그 안에 / 가 있으면 분수로 잘못 읽힌다
          const y = x.replace(/\{[^{}/]*\/[^{}]*\}/g, "");
          assert.ok(!/\{[^}]*\//.test(y), `${id} 괄호: ${x}`);
        }
        // 배치 — 위 띠 · 판서 · 도식 · 문제(크게)
        for (const s of L.band) assert.ok(m.mathWidth(s, 26, 540) <= 1490 + 2, `${id} 띠 폭: ${s}`);
        const nRow = Math.max(0, ...L.lines.map((x) => x.row));
        assert.ok(L.by + nRow * L.lh <= 790.5, `${id} 판서 아래: ${L.by}+${nRow}×${L.lh}`);
        assert.ok(L.lh >= L.size * 1.2, `${id} 판서 줄 간격 ${L.lh} / ${L.size}`);
        for (const x of L.lines) {
          const w = m.mathWidth(x.s, x.k === "h" ? Math.round(L.size * 0.72) : x.size || L.size, x.k === "h" ? 600 : 560) + (x.ind || 0);
          assert.ok(w <= L.bw + 2, `${id} 판서 폭 ${Math.round(w)} > ${L.bw}: ${x.s}`);
        }
        stat.size[L.size] = (stat.size[L.size] || 0) + 1;
        if (L.lh < Math.round(L.size * 1.58)) stat.lhSquash++;
        const B = L.big;
        assert.ok(160 + (B.bottom - 160) * B.k <= 800.5, `${id} 문제 아래 ${B.bottom} × ${B.k}`);
        for (const s of B.lines) assert.ok(m.mathWidth(s, B.size, 560) <= B.maxW + 2, `${id} 문제 폭: ${s}`);
        if (B.k < 1) stat.bigK++;
        if (T.dg) {
          assert.ok(L.dgL, `${id} 도식 배치 없음`);
          if (T.isTbl) {
            const D = L.dgL.tbl;
            assert.ok(D.w <= m.DG_BOX.w + 0.5 && D.h <= 790 - L.topY + 0.5, `${id} 표 ${D.w}×${D.h}`);
            assert.ok(D.x0 - (D.w - D.wsum * D.k) >= m.DG_BOX.x - 0.5, `${id} 표 왼쪽 ${D.x0}`);
            if (D.k < 1) stat.tblK++;
            // 표: 본문 줄 수 = <tbody> 의 <tr> 수
            const body = (T.dg.match(/<tbody>([\s\S]*?)<\/tbody>/) || [])[1] || "";
            assert.equal(T.tbl.rows.length, (body.match(/<tr\b/g) || []).length, `${id} 표 줄`);
          } else {
            assert.ok(L.dgL.fit, `${id} 그림 viewBox 를 못 읽음`);
            const f = L.dgL.fit;
            assert.ok(f.x >= m.DG_BOX.x && f.x + f.w <= m.DG_BOX.x + m.DG_BOX.w + 0.5 && f.y >= L.topY && f.y + f.h <= 790.5, `${id} 그림 자리`);
          }
        }
        // 도식 큐: 짚는 키가 도식에 있다
        const keys = new Set([...T.stepKeys.flatMap((s) => [...s]), ...T.resKeys]);
        for (const k of keys) {
          if (T.isTbl) {
            const r = k.match(/^row:(\d+)$/);
            assert.ok((r && +r[1] < T.tbl.rows.length) || k === "res" || k === "head", `${id} 표 키 ${k}`);
            if (k === "res") assert.ok(T.tbl.foot || T.tbl.rows.length, `${id} 표 결과`);
          } else {
            const esc = k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
            assert.ok(T.dg.includes(`data-k="${k}"`) || new RegExp(`data-ka="([^"]*\\s)?${esc}(\\s[^"]*)?"`).test(T.dg), `${id} 그림 키 ${k}`);
          }
        }
        // 짚는 키는 전개 줄 동안만 바뀐다
        assert.equal(m.activeKeys(T, T.tA + 100).size, 0);
        if (T.steps.length) assert.deepEqual([...m.activeKeys(T, T.steps[0].t + 1)], [...T.stepKeys[0]]);
        assert.ok(it, id);
      }
    });
  }
  test("한 바퀴(50문항) 길이 — 세트마다 20~60분", () => {
    for (const x of stat.laps) assert.ok(x >= 20 && x <= 60, String(x));
  });
  console.log(`      판서 글자 크기 ${JSON.stringify(stat.size)} · 줄 간격 줄임 ${stat.lhSquash} · 문제 통째 줄임 ${stat.bigK} · 표 통째 줄임 ${stat.tblK}`
    + ` · 한 바퀴 ${Math.min(...stat.laps).toFixed(1)}~${Math.max(...stat.laps).toFixed(1)}분`);
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${passed}/${passed + failed} 통과`);
if (failed) process.exit(1);
