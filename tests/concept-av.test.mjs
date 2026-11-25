// node tests/concept-av.test.mjs — 개념 카드 「▶ 움직이는 예시」의 학기 파일 예시(public/concept-av/*.json · cvgen/) 검산. 실패 시 exit 1.
// 카드(components/ConceptAv.jsx)는 경우의 수와 확률 예시(features/display/concept-av.js)와 같은 것 — 이 파일은 그 밖의 개념(초1 ~ 고3) 예시를 본다.
// 자료: 학기 25개(중1 ~ 고3 13개 — cvgen/ · 초1 ~ 초6 12개 — elemgen/) · 예시 id = <개념 id>-<번호> · 경우의 수와 확률(m2-2-12 ~ 14)은 코드 안 예시라 없다 ·
//       중 · 고 자리(cvgen/places.json — DB 개념 blocks 에 「[[av:<id>]]」 글줄을 넣을 단락)가 예시와 하나씩 맞는다.
//       초등은 개념 카드(public/concepts/elem/*.json)에 표식이 들어 있다 — 그 짝은 tests/elem-concepts.test.mjs 가 본다. 초등 예시는 그림 없이 글만인 것도 있다.
// 글자: 빈 값 · ASCII 빼기 · 중1 · 중2 개념의 √ 가 없다 · 카드 머리(title) · 칩(tab) · 번호 없음(no ""). 판서 「=」 검산은 생성기(cvgen/cv.py → avgen/core.py chain_check)가 한다.
// 그림: 요소 좌표가 수이고 그림 칸(660 × 680) 안(여유 40) · 나타나는/사라지는/옮기는 때가 판서 줄 안.
// 판: 넓은 판(AV_WIDE) · 좁은 판(AV_NARROW) 모두 그림이 들어가고(배율 0.8 이상) 글자 칸과 겹치지 않으며 흐르지 않는다 · 잘라 쓴 판 안에 다 든다.
// 그리기: 예시마다 (시작 · 방침 · 줄마다 셋 · 답 · 끝) × 두 판 × 두 테마 — 오류 · NaN 없음, 재생 카드도 그려진다(받아 둔 학기 파일 · 받는 중 자리).
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { avMarker, avUnitOf } from "../src/lib/conceptAv.js";

let n = 0, failed = 0;
function test(name, fn) {
  n++;
  try { fn(); console.log(`✓ ${name}`); }
  catch (e) { failed++; console.log(`✗ ${name}\n   ${e.message}`); }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const MH_UNITS = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"];
const E_UNITS = ["e1-1", "e1-2", "e2-1", "e2-2", "e3-1", "e3-2", "e4-1", "e4-2", "e5-1", "e5-2", "e6-1", "e6-2"];
const UNITS = [...E_UNITS, ...MH_UNITS];
const isE = (u) => u[0] === "e";
const SKIP = new Set(["m2-2-12", "m2-2-13", "m2-2-14"]);
const DATA = {};
for (const u of UNITS) DATA[u] = JSON.parse(fs.readFileSync(path.join(ROOT, "public/concept-av", `${u}.json`), "utf8"));
const PLACES = JSON.parse(fs.readFileSync(path.join(ROOT, "cvgen/places.json"), "utf8"));
const ALL = UNITS.flatMap((u) => Object.entries(DATA[u].items).map(([k, it]) => ({ u, k, it })));
const ALL_MH = ALL.filter((x) => !isE(x.u)), ALL_E = ALL.filter((x) => isE(x.u));

/* ══════════ 자료 ══════════ */
test("학기 25개(초 12 · 중고 13) · 파일마다 unit · v · items · id = <개념 id>-<번호>(키와 같다) · 개념이 그 단원 · 예시 350개 넘게", () => {
  assert.deepEqual(fs.readdirSync(path.join(ROOT, "public/concept-av")).filter((f) => f.endsWith(".json")).sort(), UNITS.map((u) => `${u}.json`).sort());
  for (const u of UNITS) {
    const d = DATA[u];
    assert.equal(d.unit, u);
    assert.equal(d.v, 1, u);
    assert.ok(Object.keys(d.items).length >= (isE(u) ? 8 : 10), `${u} 예시 ${Object.keys(d.items).length}`);
  }
  for (const { u, k, it } of ALL) {
    assert.equal(it.id, k);
    assert.match(k, isE(u) ? /^e[1-6]-[1-2]-\d{2}-\d+$/ : /^[mh][1-3]-[1-3]-\d{2}-\d+$/, k);
    assert.ok(k.startsWith(it.cid + "-"), `${k} 개념 ${it.cid}`);
    assert.ok(it.cid.startsWith(u + "-"), `${k} 단원 ${u}`);
  }
  assert.ok(ALL_MH.length > 200 && ALL_E.length > 120, `예시 중고 ${ALL_MH.length} · 초 ${ALL_E.length}`);
});

test("카드 머리 · 칩: no 비움(번호 없이) · title(방침을 평문으로) · tab(예제 n) — 수식 꼴({a/b} · ^{} · _{} · √{}) 이 남지 않음", () => {
  for (const { k, it } of ALL) {
    assert.equal(it.no, "", k);
    assert.ok(typeof it.title === "string" && it.title.length >= 4 && it.title.length <= 90, `${k} title ${it.title}`);
    assert.ok(!/[{}^_]/.test(it.title), `${k} title 에 수식 꼴: ${it.title}`);
    assert.match(it.tab, /^예제 \d+$/, k);
    assert.equal(it.tab, `예제 ${k.split("-").pop()}`, k);
  }
});

test("경우의 수와 확률(m2-2-12 ~ 14)은 코드 안 예시 몫 — 학기 파일에는 예시도 자리도 없다", () => {
  for (const { k, it } of ALL) assert.ok(!SKIP.has(it.cid), k);
  for (const [k, p] of Object.entries(PLACES)) assert.ok(!SKIP.has(p.cid), `자리 ${k}`);
});

test("자리(places.json): 중 · 고 예시마다 꼭 하나 · 개념이 같다 · 단락 id b<n> · after ≥ −1(−1 = 정의 · 주의 단락 끝에 덧붙이기)", () => {
  const ids = new Set(ALL_MH.map((x) => x.k));
  assert.deepEqual(Object.keys(PLACES).sort(), [...ids].sort(), "자리와 예시가 하나씩 맞지 않는다");
  for (const { k, it } of ALL_MH) {
    const p = PLACES[k];
    assert.equal(p.cid, it.cid, k);
    assert.match(p.bid, /^b\d+$/, k);
    assert.ok(Number.isInteger(p.after) && p.after >= -1, `${k} after ${p.after}`);
  }
});

test("글자: 문제 · 방침 · 판서 1 ~ 6줄 · 답이 있다 · 빈 값 · ASCII 빼기 없음 · 초등 · 중1 · 중2 개념에 √ 없음", () => {
  for (const { k, it } of ALL) {
    assert.ok(it.q && it.plan && it.ans, k);
    assert.ok(Array.isArray(it.lines) && it.lines.length >= 1 && it.lines.length <= 6, `${k} 판서 ${it.lines?.length}줄`);
    const txt = [it.q, it.plan, it.ans, it.title, ...it.lines.flatMap((l) => [l.s, l.memo || "", l.pre || ""])].join(" ");
    for (const l of it.lines) assert.ok(typeof l.s === "string" && l.s.length > 0, k);
    assert.ok(!/undefined|NaN|null|\[object/.test(txt), `${k} 빈 값`);
    assert.ok(!/(^|[^\w])-\d/.test(txt), `${k} ASCII 빼기`);
    if (/^(m[12]|e\d)-/.test(it.cid)) assert.ok(!txt.includes("√") && !JSON.stringify(it.fig || {}).includes("√"), `${k} 초등 · 중1 · 중2 에 √`);
  }
});

test("그림: 그림 DSL · 요소 좌표가 수 · 그림 칸(660 × 680) 안(여유 40) · 때(at · un · mv.at)가 판서 줄 안 · 중고는 모두 그림 · 초등은 85 % 넘게", () => {
  const NUM = ["x", "y", "x2", "y2", "w", "h", "r"];
  let figs = 0;
  for (const { k, it } of ALL) {
    if (!it.fig) continue;
    figs++;
    assert.equal(it.fig.kind, "dsl", k);
    assert.ok(it.fig.els.length > 0, k);
    for (const el of it.fig.els) {
      for (const key of NUM) if (el[key] != null) assert.ok(Number.isFinite(el[key]), `${k} ${el.k}.${key}`);
      if (el.k !== "A" && el.x != null) assert.ok(el.x >= -40 && el.x <= 700, `${k} ${el.k} x ${el.x}`);
      if (el.k !== "A" && el.y != null) assert.ok(el.y >= -40 && el.y <= 720, `${k} ${el.k} y ${el.y}`);
      if (el.pts) for (const [px, py] of el.pts) assert.ok(px >= -40 && px <= 700 && py >= -40 && py <= 720, `${k} P (${px}, ${py})`);
      for (const at of [el.at, el.un, el.mv?.at]) if (Number.isInteger(at)) assert.ok(at >= 0 && at < it.lines.length, `${k} at ${at} ≥ 줄 수`);
      for (const at of [el.at, el.un, el.mv?.at]) if (typeof at === "string") assert.ok(["q", "p", "a"].includes(at), `${k} at ${at}`);
      if (el.mv) for (const key of ["dx", "dy", "r", "cx", "cy", "dl"]) if (el.mv[key] != null) assert.ok(Number.isFinite(el.mv[key]), `${k} mv.${key}`);
      if (el.fr) for (const key of ["dx", "dy", "dl", "ms"]) if (el.fr[key] != null) assert.ok(Number.isFinite(el.fr[key]), `${k} fr.${key}`);
    }
  }
  assert.ok(ALL_MH.every((x) => x.it.fig), `중 · 고 예시에 그림이 빠짐: ${ALL_MH.filter((x) => !x.it.fig).map((x) => x.k)}`);
  const ef = ALL_E.filter((x) => x.it.fig).length;
  assert.ok(ef >= ALL_E.length * 0.85, `초등 그림 있는 예시 ${ef}/${ALL_E.length}`);
  assert.equal(figs, ALL_MH.length + ef);
});

/* ══════════ 붙이는 자리 · 학기 ══════════ */
test("avUnitOf: 예시 id → 학기 · 모양이 다르면 null — 「[[av:<id>]]」 글줄이 학기 파일 예시를 받는다", () => {
  for (const { u, k } of ALL) assert.equal(avUnitOf(k), u, k);
  assert.equal(avUnitOf("e3-2-05-1"), "e3-2", "초등 학기도 같은 꼴");
  for (const x of ["", null, undefined, "m1-1-26", "t", "c12-sum", "m1-1-26-1x", "x1-1-01-1"]) assert.equal(avUnitOf(x), null, String(x));
  const [a, b] = [ALL[0].k, ALL[ALL.length - 1].k];
  assert.deepEqual(avMarker(`[[av:${a}]]`), [a]);
  assert.deepEqual(avMarker(` [[av:${a}, ${b}]] `), [a, b]);
  assert.deepEqual(avMarker(`[[av:${a},c12-sum]]`), [a, "c12-sum"], "코드 안 예시와 섞어도");
  assert.equal(avMarker(`[[fig:av-${a}]]`), null, "옛 표식은 카드가 아님");
  assert.deepEqual(avMarker("[[av:m1-1-26]]"), [], "모양이 다른 id 는 버린다");
});

/* ══════════ 판 · 그리기(번들) ══════════ */
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "concept-av-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const F = (p) => JSON.stringify(path.join(ROOT, "src", p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { PALETTE } from ${F("features/display/draw.jsx")};
import { L10Art, layoutOf } from ${F("features/display/frames/lin10.jsx")};
import ConceptAv, { avView, avSpan, avItem, primeAvUnit, AV_WIDE, AV_NARROW } from ${F("components/ConceptAv.jsx")};
export { layoutOf, avView, avSpan, avItem, primeAvUnit, AV_WIDE, AV_NARROW };
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

  test("판: 넓은 판 · 좁은 판 모두 그림이 들어가고(배율 0.8 이상) 글자 칸과 겹치지 않음 · 흐르지 않음 · 잘라 쓴 판 안 · 좁은 판은 그림이 글자 아래 · 글만인 초등 예시도 판 안", () => {
    const hit = (a, b) => a[0] < b[2] - 1 && b[0] < a[2] - 1 && a[1] < b[3] - 1 && b[1] < a[3] - 1;
    let lo = 9;
    for (const { k, it } of ALL) {
      for (const [nm, R] of REGIONS) {
        const Lo = m.layoutOf(it, R), v = m.avView(it, R);
        if (!it.fig) {                                  // 글만인 초등 예시
          assert.ok(!Lo.fig && !Lo.scroll, `${k} ${nm}: 글만인 예시 판`);
          const [, y0, , h] = v.vb.split(" ").map(Number);
          assert.ok(y0 <= R.top - 30 && y0 + h >= Lo.bottom + 30, `${k} ${nm}: 잘라 쓴 판(${v.vb})이 글자를 다 담지 못함`);
          continue;
        }
        assert.ok(Lo.fig, `${k} ${nm}: 그림이 빠짐`);
        assert.ok(!Lo.scroll, `${k} ${nm}: 판서가 흐름`);
        assert.ok(Lo.fig.s == null || Lo.fig.s >= 0.8, `${k} ${nm}: 그림 배율 ${Lo.fig.s}`);
        lo = Math.min(lo, Lo.fig.s ?? 1);
        const fr = [Lo.fig.x, Lo.fig.y, Lo.fig.x + Lo.fig.w, Lo.fig.y + Lo.fig.h];
        assert.ok(fr[0] >= R.left - 1 && fr[2] <= R.right + 1, `${k} ${nm}: 그림이 판 밖(가로)`);
        for (const b of Lo.boxes) assert.ok(!hit(fr, b), `${k} ${nm}: 그림이 글자 칸과 겹침 ${b.map(Math.round)}`);
        const [, y0, w, h] = v.vb.split(" ").map(Number);
        assert.ok(y0 <= R.top - 30 && y0 + h >= Math.max(Lo.bottom, fr[3]) + 30, `${k} ${nm}: 잘라 쓴 판(${v.vb})이 글자 · 그림을 다 담지 못함`);
        assert.equal(w, R.right > 1000 ? 1600 : 800);
        if (nm === "좁은 판") assert.ok(fr[1] >= Lo.bottom - 1, `${k}: 좁은 판의 그림은 글자 아래`);
      }
    }
    console.log(`   가장 작은 그림 배율 ${lo.toFixed(2)}`);
  });

  test("재생 구간: 문제는 처음부터 보이고 방침부터 써짐 · 답 칸이 그려진 뒤 멈춤 · 예시 하나 30초 안", () => {
    for (const { k, it } of ALL) {
      const { P, t0, t1 } = m.avSpan(it);
      assert.ok(t0 >= 600 && t0 < P.plan[0], `${k}: 시작 ${t0}`);
      assert.ok(t1 > P.ans + 1400 && t1 < P.dur, `${k}: 끝 ${t1}`);
      assert.ok((t1 - t0) / 1000 < 30, `${k}: ${(t1 - t0) / 1000}초`);
    }
  });

  test("그리기 훑기: 예시마다 (시작 · 방침 · 줄마다 셋 · 답 · 끝) × 두 판 × 두 테마 — 오류 · NaN 없음", () => {
    let cnt = 0;
    for (const { k, it } of ALL) {
      const { P, t0, t1 } = m.avSpan(it);
      const ts = [0, t0, P.plan[0] + 400, P.ans + 300, t1, P.dur - 1];
      for (const L of P.lines) ts.push(L.a + 120, (L.a + L.b) / 2, L.b - 60);
      for (const [nm, R] of REGIONS) for (const t of ts) {
        const s = m.art(it, t, cnt++ % 2 ? "dark" : "light", R);
        assert.ok((t < 600 || /<text/.test(s)) && !BAD.test(s), `${k} ${nm} t=${Math.round(t)}: ${bad(s) || "글자 없음"}`);
      }
    }
    assert.ok(cnt > 5000, `그린 순간 ${cnt}`);
    console.log(`   그림 ${cnt}장`);
  });

  test("재생 카드: 받기 전엔 자리만(학기 파일을 받는 중) · 받아 두면 머리 · 판 · 막대 · 빠르기 · 둘이면 칩 · 없는 예시는 비움", () => {
    const one = ALL[0].k;
    for (const th of ["light", "dark"]) {
      const wait = m.card([one], th);
      assert.ok(wait.includes("cav-wait") && !wait.includes("<svg"), `받는 중 자리 ${th}`);
    }
    for (const u of UNITS) m.primeAvUnit(u, DATA[u]);
    assert.equal(m.avItem(one)?.id, one);
    assert.equal(m.avItem("m1-1-99-9"), null);
    for (const th of ["light", "dark"]) {
      const s = m.card([one], th);
      assert.ok(s.includes("움직이는 예시") && s.includes("<svg") && s.includes('class="cav-bar"') && /1\.5(<!-- -->)?×/.test(s) && !/class="cav-tab( on)?"/.test(s), `${one} ${th}`);
      assert.ok(s.includes(ALL[0].it.title.replace(/&/g, "&amp;").replace(/</g, "&lt;").slice(0, 8)), "카드 머리 = 방침");
      assert.ok(!BAD.test(s), bad(s));
      const two = m.card([ALL[1].k, ALL[2].k], th);
      assert.equal((two.match(/class="cav-tab( on)?"/g) || []).length, 2, `칩 둘 ${th}`);
      assert.equal(m.card(["m1-1-99-9"], th), "", "받아 둔 학기에 없는 예시는 조용히 비운다");
    }
    for (const { k } of ALL.filter((_, i) => i % 7 === 0)) assert.ok(m.card([k], "light").includes("<svg"), k);
    for (const { k } of ALL_E.filter((x) => !x.it.fig)) {
      const s = m.card([k], "dark");
      assert.ok(s.includes("<svg") && !BAD.test(s), `글만인 초등 예시 카드 ${k}: ${bad(s)}`);
    }
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${n - failed}/${n} 통과`);
if (failed) process.exit(1);
