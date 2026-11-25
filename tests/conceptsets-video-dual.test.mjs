// 컨셉 문제 「해설 영상」 — 시청각 해설과 같은 틀(frames/lesson.jsx) 위에서: 단일 | 듀얼 · 빠르기 · 단계 목록 · 두 막대 · 반쪽 판 그리기
//   node tests/conceptsets-video-dual.test.mjs
// ① spec(src/pages/sets/videoSpec.js) — 세트 전부(경우의 수와 확률 · 일차함수와 그래프, 범주 · 묶음 차례) · key · 단계(하 · 중 · 상) · 자리 기억 이름
// ② 장면(src/pages/sets/videoScenes.jsx) — 빠르기마다 박자 ÷ sp · 단계 거르기 · 풀이 눈금 · 목록 칸 · 같은 인자면 같은 목록
// ③ 반쪽 판(800×900) 배치 — 모든 세트 × 50문항: 위 띠 · 판서 · 도식 · 문제(크게) · 자막이 판 안에, 판서가 도식 자리를 침범하지 않음
// ④ 반쪽 판 그리기 — 세트마다 세 문항 × 박자 지점(두 테마) 오류 · NaN 없음 · 판마다 그림 id 가 따로
// ⑤ 틀 그리기(서버 렌더) — 단일: 보기 · 세트 목록 단추 · 빠르기 넷 · 목록 · 두 막대 · pickNo 그 번호부터 /
//    듀얼: 판마다 조작 · 머리(세트 · 번호 · 수준) · ⇄ — 「전부」 spec(allspec.jsx)이 들어와 있어도 컨셉 문제 세트에서만(ownDual)
// 글자 폭은 노드에서 어림치(draw.jsx estimate)로 잰다.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log("  ok  " + name); }
  catch (e) { failed++; console.log("FAIL  " + name + "\n      " + (e && e.stack || e).toString().split("\n").slice(0, 6).join("\n      ")); }
}

const CATS = [], SETS = new Map();
for (const cat of ["prob", "lin"]) {
  const dir = path.join(ROOT, "public/concept-sets", cat);
  if (!fs.existsSync(path.join(dir, "index.json"))) continue;
  const c = JSON.parse(fs.readFileSync(path.join(dir, "index.json"), "utf8")).categories.find((x) => x.id === cat);
  CATS.push(c);
  for (const s of c.sets) SETS.set(`${cat}:${String(s.no).padStart(2, "0")}`, JSON.parse(fs.readFileSync(path.join(dir, `${String(s.no).padStart(2, "0")}.json`), "utf8")));
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "csv-dual-"));
try {
  const { build } = await import(pathToFileURL(path.join(ROOT, "node_modules/esbuild/lib/main.js")).href);
  const entry = path.join(tmp, "entry.jsx");
  const P = (p) => JSON.stringify(path.join(ROOT, p));
  fs.writeFileSync(entry, `
import { renderToStaticMarkup } from "react-dom/server";
import { videoScenes, solutionScenes, VIDEO_STAGES, PANE } from ${P("src/pages/sets/videoScenes.jsx")};
import { videoSpec, videoSets, videoKey, parseVideoKey, VIDEO_LSK } from ${P("src/pages/sets/videoSpec.js")};
import { PALETTE, mathWidth } from ${P("src/features/display/draw.jsx")};
import { Btn, Ic, FrameIc } from ${P("src/features/display/stage-ui.jsx")};
import { LessonFrame, LESSON_SPEEDS, paneLoad } from ${P("src/features/display/frames/lesson.jsx")};
import ${P("src/features/display/frames/allspec.jsx")};          // 「전부」 spec 이 들어와 있어도(교실 모니터를 먼저 연 기기) 컨셉 문제 세트에서만
export { videoScenes, solutionScenes, VIDEO_STAGES, PANE, videoSpec, videoSets, videoKey, parseVideoKey, VIDEO_LSK, mathWidth, LESSON_SPEEDS, paneLoad };
export const pane = (sc, t, th, uid = "dL") => renderToStaticMarkup(<svg viewBox="0 0 800 900">{sc.pane(t, PALETTE[th], uid)}</svg>);
const props = (th) => ({ C: PALETTE[th], ui: { Btn, Ic, FrameIc }, ctl: true, poke: () => {}, inert: false, isFs: false, toggleFs: () => {},
  onTheme: () => {}, onGallery: null, noGallery: true, onExit: () => {}, exitTitle: "나가기 — 세트로", mode: "m", onMode: () => {} });
export const frame = (spec, th, pick = null, pickNo = null) => renderToStaticMarkup(<LessonFrame spec={spec} pick={pick} pickNo={pickNo} {...props(th)} />);
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
  const BAD = /NaN|undefined|(?<!Do As |Another )Infinity|\[object Object\]/;
  const bad = (s) => (s.match(/.{60}(NaN|undefined|Infinity|\[object Object\]).{40}/) || [""])[0];
  const src = { get: (k) => SETS.get(k), load: (k) => (SETS.has(k) ? Promise.resolve(SETS.get(k)) : Promise.reject(new Error(k))) };
  const spec = m.videoSpec(CATS, src);
  const nSets = CATS.reduce((a, c) => a + c.sets.length, 0);

  console.log("spec");
  test(`세트 전부(${nSets}) — 범주 · 묶음 차례 · key 「범주:NN」 · 이름표 · 묶음 이름 · 세트 목록 단추(U) · 듀얼도 이 세트에서만`, () => {
    assert.equal(spec.sets.length, nSets);
    assert.equal(new Set(spec.sets.map((s) => s.key)).size, nSets, "key 중복");
    assert.equal(spec.lsk, "ash.cs.video");
    assert.ok(spec.ownDual && spec.setMenu?.word === "세트" && spec.cols === 3);
    // 범주 차례(경우의 수와 확률 → 일차함수와 그래프) · 범주 안은 index 묶음 차례
    const cats = spec.sets.map((s) => s.cat);
    assert.deepEqual([...new Set(cats)], CATS.map((c) => c.id));
    for (const c of CATS) {
      const want = [];
      const seen = new Set();
      for (const g of c.groups || []) for (const no of g.sets) if (!seen.has(no) && c.sets.some((s) => s.no === no)) { seen.add(no); want.push(no); }
      for (const s of c.sets) if (!seen.has(s.no)) want.push(s.no);
      assert.deepEqual(spec.sets.filter((s) => s.cat === c.id).map((s) => s.no), want, `${c.id} 차례`);
    }
    for (const s of spec.sets) {
      assert.match(s.key, /^(prob|lin):\d{2,}$/);
      assert.deepEqual(m.parseVideoKey(s.key), { cat: s.cat, no: s.no });
      assert.equal(m.videoKey(s.cat, s.no), s.key);
      assert.ok(s.name && s.short.startsWith(String(s.no).padStart(2, "0") + " ") && s.icon && s.grp, s.key);
    }
    assert.ok(spec.sets.find((s) => s.key === "prob:121")?.grp.includes("애니메이션"), "121 은 애니메이션 묶음");
    assert.ok(spec.setMenu.hint.includes(`${CATS[0].title} ${CATS[0].sets.length}세트`));
    assert.equal(m.parseVideoKey("x"), null);
  });
  test("단계 = 하 · 중 · 상(1 · 2 · 3) — 칩 글자(단일 「하 · 기본 15」 · 듀얼 「하 15」) · 자리 기억 이름(전체는 예전 해설 영상 이름 그대로)", () => {
    assert.deepEqual(m.VIDEO_STAGES.map((x) => [x.v, x.lv]), [[1, "하"], [2, "중"], [3, "상"]]);
    for (const s of spec.sets) {
      const st = spec.stages(s.key);
      assert.deepEqual(st.map((x) => x.v), [1, 2, 3], s.key);
      for (const x of st) {
        const n = s.lv?.[m.VIDEO_STAGES[x.v - 1].lv];
        assert.ok(n > 0, `${s.key} ${x.lab}`);
        assert.equal(x.chip, `${x.lab} ${n}`);
        assert.equal(x.short, `${m.VIDEO_STAGES[x.v - 1].lv} ${n}`);
      }
    }
    assert.equal(spec.stages("prob:05")[0].lab, "하 · 기본");
    assert.equal(spec.posKey(spec.lsk, "prob:05", 0), "ash.cs.video.prob.05");
    assert.equal(spec.posKey(spec.lsk, "lin:03", 2), "ash.cs.video.lin.03.2");
    assert.ok(spec.ready("prob:01") && !spec.ready("prob:999"));
  });

  console.log("장면 — 빠르기 · 단계 · 눈금");
  test("빠르기 넷: 박자 ÷ sp · 그림은 같은 순간(t × sp) · 같은 (세트, sp, st)는 같은 목록 · 예전 이름(solutionScenes)은 1배속 전체", () => {
    const set = SETS.get("prob:01");
    const base = m.videoScenes(set, 1, 0);
    assert.equal(base, m.solutionScenes(set));
    assert.equal(base, m.videoScenes(set, 1, 0));
    for (const sp of m.LESSON_SPEEDS) {
      const L = m.videoScenes(set, sp, 0);
      assert.equal(L.length, 50);
      L.forEach((sc, i) => {
        assert.equal(sc.key, base[i].key);
        assert.equal(sc.dur, Math.round(base[i].timing.dur / sp), `${sc.key} ${sp}×`);
        assert.ok(sc.marks.at(-1).t < sc.dur, `${sc.key} 답 눈금이 장면 안`);
      });
      // 같은 순간: 0.75× 의 t 와 1× 의 t × 0.75 는 같은 그림
      if (sp !== 1) {
        const sc = L[7], b = base[7], t = Math.round(b.timing.steps[0].t / sp) + 200;
        assert.equal(m.pane(sc, t, "dark"), m.pane(b, t * sp, "dark"), `${sp}× 같은 순간`);
      }
    }
  });
  test("단계 거르기: 하 15 · 중 25 · 상 10 — 그 수준만 · 번호 차례 그대로 · 긴 막대 눈금(grp) · 목록 칸(유형 · 딱지 · 소주제)", () => {
    for (const [k, set] of SETS) {
      const all = m.videoScenes(set, 1, 0);
      const cnt = { 1: 0, 2: 0, 3: 0 };
      for (const sc of all) {
        cnt[sc.st]++;
        assert.equal(m.VIDEO_STAGES[sc.st - 1].lv, sc.lv, sc.key);
        assert.equal(sc.grp, m.VIDEO_STAGES[sc.st - 1].lab, sc.key);
        assert.ok(sc.card && sc.cardMeta && sc.cardTag?.s === sc.lv && /^#[0-9a-f]{6}$/i.test(sc.cardTag.bg), sc.key);
        assert.equal(typeof sc.pane, "function");
      }
      for (const st of [1, 2, 3]) {
        const L = m.videoScenes(set, 1.5, st);
        assert.equal(L.length, cnt[st], `${k} ${st}단계`);
        assert.ok(L.every((sc) => sc.st === st), `${k} ${st}단계만`);
        assert.deepEqual(L.map((sc) => sc.no), all.filter((sc) => sc.st === st).map((sc) => sc.no));
      }
      assert.deepEqual(cnt, { 1: set.items.filter((it) => it.lv === "하").length, 2: set.items.filter((it) => it.lv === "중").length, 3: set.items.filter((it) => it.lv === "상").length });
    }
  });
  test("풀이 눈금(짧은 막대): 문제 → 방침(일차함수는 주어진 것 · 구할 것) → 전개 줄마다 → 확인 → 답 · 시각이 늘어나고 장면 안", () => {
    for (const [k, set] of SETS) for (const sc of m.videoScenes(set, 2, 0)) {
      const M = sc.marks, T = sc.timing;
      assert.equal(M.length, T.board.length + 4, sc.key);
      assert.equal(M[0].lab, "문제");
      assert.equal(M[1].lab, set.cat === "lin" ? "주어진 것 · 구할 것" : "방침", sc.key);
      // 눈금 이름: 강조 표시 · 분수 괄호 · 꼬리표가 남지 않고 짧게(부등호 · 집합 괄호는 글자 그대로)
      assert.ok(M.slice(2, -2).every((x, i) => x.lab.startsWith(`${i + 1}줄 · `) && !/[‹›]|\{[^{}]*\/[^{}]*\}|<\/?[a-z]/i.test(x.lab) && x.lab.length <= 23), sc.key);
      assert.deepEqual(M.slice(-2).map((x) => x.lab), ["확인", "답"]);
      for (let i = 1; i < M.length; i++) assert.ok(M[i].t > M[i - 1].t, `${sc.key} 눈금 ${i}`);
      assert.ok(M.at(-1).t < sc.dur && M[2].t === T.steps[0].t / 2, sc.key);
    }
  });

  console.log("반쪽 판 배치 — 모든 문항");
  const stat = { size: {}, squash: 0, bigK: 0, dgMin: Infinity, cut: 0, n: 0 };
  test("모든 세트 × 50문항: 위 띠 두 줄 · 판서 폭 · 아래 끝 · 도식은 판서 아래 판 안 · 문제(크게)는 판 안 · 자막 폭", () => {
    const P = m.PANE;
    for (const [k, set] of SETS) for (const sc of m.videoScenes(set, 1, 0)) {
      const L = sc.paneLayout(), T = sc.timing, id = sc.key;
      stat.n++;
      assert.ok(L.band.length >= 1 && L.band.length <= 2, id);
      for (const s of L.band) assert.ok(m.mathWidth(s, P.band.size, 540) <= P.w + 2, `${id} 띠 폭: ${s}`);
      const n = Math.max(0, ...L.lines.map((x) => x.row));
      const bot = L.by + n * L.lh + L.size * 0.45;
      assert.ok(bot <= P.bottom + 0.5, `${id} 판서 아래 ${bot}`);
      assert.ok(L.lh >= L.size * 1.2, `${id} 줄 간격 ${L.lh}/${L.size}`);
      assert.ok(L.by - L.size >= L.topY - 0.5, `${id} 판서가 띠 아래`);
      for (const x of L.lines) {
        const w = m.mathWidth(x.s, x.k === "h" ? Math.round(L.size * 0.72) : x.size || L.size, x.k === "h" ? 600 : 560) + (x.ind || 0);
        assert.ok(w <= L.bw + 2, `${id} 판서 폭 ${Math.round(w)} > ${L.bw}: ${x.s}`);
      }
      assert.ok(L.bx - 22 >= 46 && L.bx + L.bw <= 762, `${id} 판서 좌우`);
      stat.size[L.size] = (stat.size[L.size] || 0) + 1;
      if (L.lh < Math.round(L.size * P.board.lhK)) stat.squash++;
      if (T.dg) {
        const D = L.dgL, b = D.box;
        assert.ok(b.y >= bot + P.board.gap - 0.5, `${id} 도식이 판서 아래`);
        assert.ok(b.y + b.h <= P.bottom + 0.5 && b.h >= 120, `${id} 도식 자리 ${b.y}+${b.h}`);
        stat.dgMin = Math.min(stat.dgMin, b.h);
        if (D.tbl) assert.ok(D.tbl.w <= b.w + 0.5 && D.tbl.y0 + D.tbl.h <= b.y + b.h + 6.5 && D.tbl.x0 - (D.tbl.w - D.tbl.wsum * D.tbl.k) >= b.x - 0.5, `${id} 표`);
        else {
          assert.ok(D.fit, `${id} 그림 viewBox`);
          const f = D.fit;
          assert.ok(f.x >= b.x && f.x + f.w <= b.x + b.w + 0.5 && f.y >= b.y && f.y + f.h <= b.y + b.h - 17.5, `${id} 그림 자리`);
        }
      } else assert.equal(L.dgL, null);
      const B = L.big;
      assert.ok(B.top + (B.bottom - B.top) * B.k <= 846.5, `${id} 문제 아래 ${B.bottom} × ${B.k}`);
      for (const s of B.lines) assert.ok(m.mathWidth(s, B.size, 560) <= B.maxW + 2 && B.maxW <= P.w, `${id} 문제 폭: ${s}`);
      if (B.fig) assert.ok(B.fig.x >= P.x - 0.5 && B.fig.x + B.fig.w <= P.x + P.w + 0.5, `${id} 문제 그림`);
      if (B.k < 1) stat.bigK++;
      for (const c of L.caps) assert.ok(m.mathWidth(c.s, P.cap.size, 560) + 52 <= P.cap.w + 1, `${id} 자막 폭: ${c.s}`);
      if (L.caps.some((c, i) => c.s !== T.caps[i].s)) stat.cut++;
    }
  });
  console.log(`      ${stat.n}문항 · 판서 글자 ${JSON.stringify(stat.size)} · 줄 간격 줄임 ${stat.squash} · 문제 통째 줄임 ${stat.bigK} · 도식 높이 최소 ${Math.round(stat.dgMin)} · 자막 줄임 ${stat.cut}`);

  console.log("반쪽 판 그리기");
  test("세트마다 세 문항(첫 · 가운데 · 끝) × 박자 지점 — 오류 · NaN 없음 · 판마다 그림 id 가 따로(같은 문항이 두 판에 떠도 강조가 섞이지 않게)", () => {
    let cnt = 0;
    for (const [k, set] of SETS) {
      const L = m.videoScenes(set, 1, 0);
      for (const sc of [L[0], L[24], L[49]]) {
        const T = sc.timing;
        const times = [0, T.tA - 1, T.tA + 400, T.tPos + 300, T.tB + 200, ...T.steps.map((s) => s.t + 400), T.tC + 300, T.tAns + 300, T.dur];
        for (const t of times) {
          const h = m.pane(sc, t, cnt % 2 ? "light" : "dark");
          cnt++;
          assert.ok(!BAD.test(h), `${sc.key} t=${t}: ${bad(h)}`);
        }
        if (T.dg && !T.isTbl) {
          const t = T.steps[0].t + 400;
          const a = m.pane(sc, t, "dark", "dL"), b = m.pane(sc, t, "dark", "dR");
          const ids = (h) => [...h.matchAll(/<svg id="([^"]+)"/g)].map((x) => x[1]);
          assert.ok(ids(a).length && ids(a).every((x) => x.endsWith("dL")) && ids(b).every((x) => x.endsWith("dR")), `${sc.key} 판 id`);
        }
      }
    }
    console.log(`      반쪽 판 그림 ${cnt}장`);
  });

  console.log("틀 그리기(단일 · 듀얼)");
  test("단일: 보기 단일 | 듀얼 · 세트 목록 단추(U) · 빠르기 넷 · 번호 · 단계 목록 · 두 막대(하 · 중 · 상 눈금) · 나가기 — 두 테마", () => {
    for (const th of ["dark", "light"]) {
      const h = m.frame(spec, th, "prob:121");
      assert.ok(!BAD.test(h), bad(h));
      for (const w of ["단일", "듀얼", "0.75×", "1×", "1.5×", "2×", "번호 · 단계 목록 (L)", "세트 목록 (U)", "scb-long", "scb-short", "이 장면 반복", "나가기 — 세트로",
        "121 방어력에 올인", "하 · 기본", "중 · 발전", "상 · 심화"]) assert.ok(h.includes(w), `단일 ${th} — ${w} 없음`);
      assert.ok(!h.includes("액자 목록") && !h.includes('class="lsn-pane-ctl'), "액자 단추 · 듀얼 판 없음");
      assert.match(h, /aria-label="컨셉 문제 해설 영상 · 방어력 올인[^"]* — 1\. /);
    }
  });
  test("pickNo — 그 번호부터(단계는 전체로) · 다른 세트로 들어오면 단일 · 같은 세트로 다시 들어오면(pick 없이) 마지막 보기 그대로", () => {
    store[m.VIDEO_LSK] = JSON.stringify({ set: "prob:05", sp: 1.5, st: 3 });
    const h = m.frame(spec, "dark", "prob:05", 7);
    assert.match(h, /— 7\. /, "7번부터");
    assert.ok(h.includes('aria-checked="true">1.5×<'), "빠르기는 기억한 것");
    const h2 = m.frame(spec, "dark", "prob:05", null);
    assert.match(h2, /— 41\. /, "번호 없이 같은 세트 — 기억한 단계(상)의 첫 문항");
    store[m.VIDEO_LSK + ".mode"] = JSON.stringify("dual");
    assert.ok(m.frame(spec, "dark", null).includes('class="lsn-pane-ctl'), "pick 없이 — 듀얼 그대로");
    assert.ok(!m.frame(spec, "dark", "prob:05").includes('class="lsn-pane-ctl'), "pick — 단일로");
    delete store[m.VIDEO_LSK]; delete store[m.VIDEO_LSK + ".mode"];
  });
  test("듀얼: 판마다 세트 목록 단추 · 번호 · 단계 목록 · 이전 · 멈춤 · 다음 · 반복 · 빠르기 넷 · 두 막대 · ⇄ · 머리(세트 · 번호 · 수준 · 빠르기) — 컨셉 문제 세트에서만", () => {
    store[m.VIDEO_LSK + ".mode"] = JSON.stringify("dual");
    store[m.VIDEO_LSK + ".dual"] = JSON.stringify({ L: { set: "prob:121", sp: 1.5, st: 0, i: 3, t0: Date.now() - 1000, held: null, rep: false },
      R: { set: "lin:03", sp: 0.75, st: 2, i: 2, t0: Date.now() - 500, held: 800, rep: true } });
    for (const th of ["dark", "light"]) {
      const h = m.frame(spec, th, null);
      assert.ok(!BAD.test(h), bad(h));
      assert.equal((h.match(/class="lsn-pane-ctl /g) || []).length, 2, "판 조작 둘");
      assert.equal((h.match(/class="scb-long /g) || []).length, 2, "판마다 긴 막대");
      assert.ok(h.includes("lsn-swap") && h.includes("왼쪽 빠르기") && h.includes("오른쪽 빠르기"), "⇄ · 판마다 빠르기");
      assert.ok(h.includes("121 방어력에 올인 · 4번 · 하") && h.includes("1.5×"), "왼쪽 머리");
      const r = spec.sets.find((s) => s.key === "lin:03");
      const rs = m.videoScenes(SETS.get("lin:03"), 0.75, 2)[2];
      assert.ok(h.includes(`${r.short} · ${rs.no}번 · 중`) && h.includes("0.75× · 반복 · 멈춤"), "오른쪽 머리(중 단계 · 반복 · 멈춤)");
      assert.ok(!h.includes("📚") && !h.includes("콘텐츠 목록"), "「전부」 spec 이 아니라 컨셉 문제 세트");
      assert.match(h, /aria-label="컨셉 문제 해설 영상 — 듀얼: 왼쪽 방어력 올인[^"]*4번, 오른쪽 [^"]*번"/);
    }
    // 판 기억이 없으면 두 판 다 단일 모드에서 보던 세트(왼쪽 앞에서 1.5× · 오른쪽 가운데부터 0.75×)
    delete store[m.VIDEO_LSK + ".dual"];
    store[m.VIDEO_LSK] = JSON.stringify({ set: "prob:30", sp: 1, st: 0 });
    const now = 1_700_000_000_000;
    const L = m.paneLoad(spec, null, "L", "prob:30", now), R = m.paneLoad(spec, null, "R", "prob:30", now);
    assert.deepEqual([L.set, L.sp, L.i, R.set, R.sp, R.i], ["prob:30", 1.5, 0, "prob:30", 0.75, 25]);
    const h = m.frame(spec, "dark", null);
    assert.ok(h.includes("30 ") && (h.match(/class="lsn-pane-ctl /g) || []).length === 2, "기본 두 판");
    delete store[m.VIDEO_LSK]; delete store[m.VIDEO_LSK + ".mode"];
  });
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}

console.log(`\n${passed}/${passed + failed} 통과`);
if (failed) process.exit(1);
