// itemfactory/tools/review.mjs — 생성 문항 눈검수 대조표 (v2.0 · 애니메이션)
//
//   node itemfactory/tools/review.mjs                          # 전체 → out/gen/review.html
//   node itemfactory/tools/review.mjs --cat 활용 --per 4        # 범주별 → out/gen/review-활용.html
//   node itemfactory/tools/review.mjs --cat 연산 / --cat 도형
//   node itemfactory/tools/review.mjs --skip m1-1-mixture       # 특정 시드 제외
//
// 문면·보기·정답·해설(단계별 도식·애니메이션)·모범답안·채점기준을 앱과 같은 렌더러로 그려 한 장에 모은다.
// 애니메이션: 그림 여백 클릭 = 일시정지/재생, 끝난 뒤 클릭 = 처음부터. 화면에 들어오면 자동 재생.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { renderHtml, MATH_CSS } from "../../src/lib/mathir.js";
import { figureToHtml1 } from "../../src/lib/figsvg.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf(k); return i < 0 ? d : argv[i + 1]; };
const PER = Number(arg("--per", 4));
const DIR = arg("--dir", path.join(ROOT, "out", "gen"));
const CAT = arg("--cat", null);
const SKIP = (arg("--skip", "") || "").split(",").filter(Boolean);
const OUT = arg("--out", path.join(DIR, CAT ? `review-${CAT}.html` : "review.html"));
const ANIM_SRC = fs.readFileSync(path.resolve(HERE, "../../src/lib/figanim.js"), "utf8");

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const rt = (s) => renderHtml(String(s ?? ""));   // 이스케이프 포함 · 분수는 상하로
const CAT_TITLE = { "활용": "실생활 활용 유형", "연산": "연산 · 계산 요령 유형", "도형": "도형 다단계 유형" };

let cards = 0, warns = 0, anims = 0;
let h = `<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>생성 문항 검수${CAT ? " — " + CAT : ""}</title><style>
:root{color-scheme:light}
${MATH_CSS}
body{font-family:system-ui,-apple-system,'Malgun Gothic',sans-serif;margin:16px;background:#fafafa;color:#111}
h1{font-size:18px;margin:0 0 4px}
.sub{font-size:12.5px;color:#666;margin-bottom:14px;line-height:1.5}
h2{font-size:15px;margin:26px 0 8px;border-bottom:2px solid #333;padding-bottom:4px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}
.c{background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:12px}
.m{font:11px ui-monospace,monospace;color:#888;margin-bottom:6px}
.q{font-size:14.5px;line-height:1.55;margin-bottom:7px;white-space:pre-wrap}
.ch{font-size:13px;margin:5px 0;padding-left:2px}
.ch span{display:inline-block;margin-right:9px}
.ok{color:#c0392b;font-weight:600}
.a{font-size:13px;margin-top:6px;color:#1a6}
.s{font-size:12.5px;line-height:1.55;margin-top:8px;border-top:1px dashed #ddd;padding-top:6px;color:#333}
.s b{color:#111}
.lv{margin-bottom:8px}
.lv ol{margin:3px 0 3px 17px;padding:0}
.lv li{margin:2px 0;padding:1px 3px;border-radius:3px}
.lv p{margin:2px 0;padding:1px 3px;border-radius:3px}
.fig-stage{margin:6px 0;padding:6px;border-radius:8px;background:#fcfcfb;border:1px solid #eee}
.w{font-size:11px;color:#c0392b;margin-top:5px}
.t{font-size:11px;color:#777;margin-top:6px;word-break:break-all}
.ma{margin-top:7px;padding:6px 8px;background:#f6f6f4;border-radius:6px}
.ma b{font-size:11px;color:#666}
table.rb{margin-top:7px;border-collapse:collapse;font-size:11.5px;width:100%}
table.rb th,table.rb td{border:1px solid #ddd;padding:2px 4px;vertical-align:top}
table.rb th{background:#f0f0ee}
.anim-tag{display:inline-block;font-size:10px;color:#fff;background:#d1495b;border-radius:3px;padding:0 5px;margin-left:6px;vertical-align:middle}
</style>
<h1>생성 문항 검수 대조표${CAT ? " — " + (CAT_TITLE[CAT] || CAT) : ""}</h1>
<div class="sub">해설 도식은 <b>화면에 들어오면 자동 재생</b>됩니다. <b>그림 여백을 클릭</b>하면 일시정지/재생, 끝난 뒤 클릭하면 처음부터. 진행 중인 단계의 설명이 굵게 표시됩니다.</div>`;

function levelHtml(lv, it) {
  const hasAnim = Array.isArray(lv.anim) && lv.anim.length && (lv.figure || []).length;
  let s = `<div class="lv${hasAnim ? " anim-level" : ""}"${hasAnim ? ` data-anim='${esc(JSON.stringify(lv.anim))}'` : ""}>`;
  s += `<b>${lv.level}. ${esc(lv.title)}</b>${hasAnim ? '<span class="anim-tag">애니메이션</span>' : ""}`;
  if (lv.figure && lv.figure.length) {
    s += `<div class="fig-stage">`;
    for (const fg of lv.figure) {
      const r = figureToHtml1(fg, { width: 300 });
      s += r.html;
      if (r.warnings.length) { warns++; s += `<div class="w">⚠ ${esc(r.warnings.join(" / "))}</div>`; }
    }
    s += `</div>`;
  }
  if (lv.steps) s += "<ol>" + lv.steps.map((st, i) => `<li data-step="${i}">${rt(st)}</li>`).join("") + "</ol>";
  else if (lv.text) {
    // 단일 텍스트 단계 — 순차 큐가 여러 개여도 텍스트는 하나
    s += `<p data-step="0">${rt(lv.text)}</p>`;
    if (hasAnim && lv.anim.length > 1) for (let i = 1; i < lv.anim.length; i++) s += `<span data-step="${i}" hidden></span>`;
  }
  if (hasAnim) anims++;
  return s + `</div>`;
}

for (const f of fs.readdirSync(DIR).filter((x) => x.endsWith("_pool.json")).sort()) {
  const seedId = f.replace("_pool.json", "");
  if (SKIP.includes(seedId)) continue;
  const rows = JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8"));
  if (!rows.length) continue;
  if (CAT && rows[0].category !== CAT) continue;
  const byTpl = {};
  for (const r of rows) (byTpl[r.template_id] = byTpl[r.template_id] || []).push(r);
  h += `<h2>${esc(seedId)} — ${rows.length}건</h2><div class="g">`;
  for (const [tpl, list] of Object.entries(byTpl)) {
    // 표본: 처음·끝(경계) 포함 균등
    const idxs = new Set([0, list.length - 1]);
    for (let k = 1; k < PER - 1; k++) idxs.add(Math.floor((list.length - 1) * k / (PER - 1)));
    for (const i of [...idxs].sort((a, b) => a - b)) {
      const it = list[i];
      cards++;
      h += `<div class="c"><div class="m">${esc(tpl)} · idx ${it.param_index} · 난이도 ${it.difficulty} · ${it.qtype} · cost ${it.cost}</div>`;
      h += `<div class="q">${rt(it.question)}</div>`;
      if (it.figure) {
        h += `<div class="fig-stage">`;
        for (const fg of it.figure) {
          const r = figureToHtml1(fg, { width: 300 });
          h += r.html;
          if (r.warnings.length) { warns++; h += `<div class="w">⚠ ${esc(r.warnings.join(" / "))}</div>`; }
        }
        h += `</div>`;
      }
      if (it.choices) {
        h += `<div class="ch">` + it.choices.map((c, k) =>
          `<span class="${c === it.answer ? "ok" : ""}">${"①②③④⑤"[k]} ${rt(c)}</span>`).join("") + `</div>`;
      }
      h += `<div class="a">정답: ${rt(it.answer)}</div>`;
      const sol = it.solution;
      h += `<div class="s">` + sol.levels.map((lv) => levelHtml(lv, it)).join("");
      if (sol.levels.length === 2) h += `<div style="margin-top:4px;opacity:.75">확인: ${rt(sol.check)}</div>`;
      if (sol.model_answer) h += `<div class="ma"><b>서술형 답안 예시</b><div style="margin-top:3px">${rt(sol.model_answer)}</div></div>`;
      if (sol.rubric) {
        h += `<table class="rb"><tr><th>평가 요소</th><th style="width:34px">배점</th><th>채점 기준</th></tr>`;
        for (const r of sol.rubric.items) {
          h += `<tr><td>${esc(r.element)}</td><td style="text-align:center">${r.points}</td><td>${rt(r.criterion)}`
            + (r.partial ? `<div style="opacity:.65;font-size:10.5px">부분: ${rt(r.partial)}</div>` : "")
            + (r.zero ? `<div style="opacity:.5;font-size:10.5px">0점: ${esc(r.zero)}</div>` : "") + `</td></tr>`;
        }
        h += `<tr><td style="font-weight:600">합계</td><td style="text-align:center;font-weight:600">${sol.rubric.total}</td><td></td></tr>`;
        for (const c of sol.rubric.checks || []) {
          h += `<tr style="color:#8a4b00"><td style="opacity:.8">실수거리</td><td style="text-align:center;font-size:10.5px">${c.element_no ? "요소 " + c.element_no : ""}<br>${esc(c.effect)}</td><td>${rt(c.text)}</td></tr>`;
        }
        h += `</table>`;
        if (sol.rubric.principles) h += `<div style="font-size:10.5px;color:#777;margin-top:4px;line-height:1.45">채점 원칙: ${sol.rubric.principles.map(esc).join(" · ")}</div>`;
      }
      h += `</div>`;
      const L = it.labels;
      h += `<div class="t">${esc((L.L39_representation || []).join("/"))} · ${esc(L.L40_process)} · ${esc(L.L41_context)} · ${esc(L.L08_answer_type)}`
         + ` · 풀이 ${esc(L.L13_steps_n)}스텝 · 해설 ${it.solution.levels.length}단 · ${esc(L.L23_param_bucket)}구간`
         + (L.L20_distractor_rule?.length ? ` · 오개념 ${esc(L.L20_distractor_rule.join(","))}` : "") + `</div></div>`;
    }
  }
  h += `</div>`;
}
h += `<p style="font-size:12px;color:#666;margin-top:20px">카드 ${cards}개 · 애니메이션 ${anims}개 · 도형 경고 ${warns}건</p>`;
h += `<script type="module">\n${ANIM_SRC}\nmountAll(document, {});\n</script>`;
fs.writeFileSync(OUT, h, "utf8");
console.log(`· ${OUT} (카드 ${cards} · 애니메이션 ${anims} · 도형 경고 ${warns})`);
