// ashrain.out — 기본기 해설(단원 100가지)의 인쇄 문서: 문제지 · 해설지 · 빠른 정답 · OMR (frames/avprint.js)
// 문항 자료(../basics/<단원>.js)에서 바로 HTML 을 만든다 — 저장소에 인쇄 HTML 을 따로 두지 않는다.
//   · 앱: 📄 문서 → PDF 가 아직 없으면 이 HTML 을 인쇄 창으로(frames/docsmenu.jsx)
//   · 워크플로: scripts/av-files.mjs 가 Chromium 안에서 같은 함수로 HTML 을 만들어 PDF 로 찍는다(Storage concept-sets/av/…)
// 그림은 화면과 같은 그림 DSL(frames/figdsl.jsx)을 흑백 팔레트로 찍은 SVG — figOf(it, "q" | "end") 로 받는다(frames/avfig.jsx).
// 흑백 인쇄: 색으로만 가르는 표시가 없게 — 메모는 왼쪽 세로줄 + 작은 회색 글자, 답은 굵게, 강조(‹›)는 굵게.
// 프린트 코드(RULE-프린트코드-v1): 모든 문서 첫 쪽 머리 오른쪽에 「코드 XXX-XXX」, 둘째 쪽부터는 쪽 머리(@page 오른쪽 위).
//   문제지 PDF 에는 등록 정보 ashrain-print.json 을 붙인다(avManifest — 붙이는 일은 scripts/av-files.mjs).
// 문구는 @ashrain.out 만 쓴다(쪽 아래 가운데).
import { parseMath } from "../draw.jsx";
import { layoutCard } from "../../../lib/omr/grid.js";
import { unitLabel } from "../../../lib/units.js";

export const AV_PRINT_FONTS = [
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/400.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/500.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/700.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-serif@5.3.0/400-italic.css",
];
export const fmtCode = (c) => (c ? `${c.slice(0, 3)}-${c.slice(3)}` : "");
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

/* ══════════ 수식 글자 → HTML (무대의 MText 와 같은 문법 · 같은 해석기) ══════════ */
const ICON_CH = { circle: "○", tri: "△", square: "□", dot: "●", check: "✓", cross: "×" };
const DIE = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
function toksHtml(toks) {
  let out = "";
  for (const t of toks) {
    let h;
    if (t.frac) h = `<span class="fr"><span class="n">${toksHtml(t.num)}</span><span class="d">${toksHtml(t.den)}</span></span>`;
    else if (t.sup) h = `<sup>${toksHtml(t.sup)}</sup>`;
    else if (t.sub) h = `<sub>${toksHtml(t.sub)}</sub>`;
    else if (t.root) h = `<span class="rt">√<span class="rb">${toksHtml(t.root)}</span></span>`;
    else if (t.icon) h = t.icon.kind === "die" ? DIE[t.icon.n - 1] || "□" : ICON_CH[t.icon.kind] || "○";
    else h = t.it ? `<i class="mi">${esc(t.s)}</i>` : esc(t.s);
    out += t.ac && !t.frac && !t.sup && !t.sub && !t.root ? `<b>${h}</b>` : h;
  }
  return out;
}
/** 무대 수식 글자({a/b} · ^{} · _{} · √{} · ‹강조› · ⟪아이콘⟫ · 홀로 선 소문자 이탤릭) → HTML */
export const mathHtml = (s) => toksHtml(parseMath(String(s ?? "")));

/* ══════════ 쪽 나누기 — 문제지는 단계마다 새 쪽, 한 쪽에 pp 문항(두 줄) ══════════ */
/** [{ st, items:[…], first }] — 단계의 첫 쪽이면 first */
export function problemPages(set) {
  const pp = Math.max(2, set.pp || 10);
  const pages = [];
  for (let st = 1; st <= 5; st++) {
    const list = set.items.filter((it) => it.st === st);
    for (let i = 0; i < list.length; i += pp) pages.push({ st, items: list.slice(i, i + pp), first: i === 0 });
  }
  return pages;
}

/* ══════════ 등록 정보(ashrain-print.json) ══════════ */
export function avManifest(meta, set) {
  const pageOf = new Map();
  problemPages(set).forEach((p, i) => p.items.forEach((it) => pageOf.set(it.no, i + 1)));
  return {
    kind: "ashrain.print", version: 1, code: meta.code,
    title: meta.title, sub: `기본기 해설 · ${meta.span} · ${set.items.length}문항 · 1 ~ 5단계`, label: "서답형",
    items: set.items.map((it) => ({
      no: String(it.no), answer: String(it.ap).replace(/−/g, "-"), choice: false, points: 1, topic: `${it.st}단계 ${meta.stages[it.st] || ""}`.trim(),
      key: `av/${meta.id}/${it.no}`, page: pageOf.get(it.no),
    })),
  };
}

/** OMR 카드(grid.js 손글씨 한 줄 칸) */
export function avCard(meta, items) {
  return layoutCard({ cat: "av", no: 1, title: meta.title, short: meta.short, sub: `${meta.span} · ${items.length}제 · 코드 ${fmtCode(meta.code)}`,
    items: items.map((it) => ({ no: it.no, a: { k: it.omr === "ex" ? "ex" : it.omr === "pt" ? "pt" : "num" } })) });
}

/* ══════════ 문서 틀 ══════════ */
const PAGE_H = 268;   // mm — A4 297 − 위 12 − 아래 13 = 272 에서 넘치지 않게 조금 덜
function css(code) {
  const c = fmtCode(code);
  return `@page{size:A4;margin:12mm 13mm 13mm 13mm;
@top-right{content:"코드 ${c}";font-family:'Noto Sans KR',sans-serif;font-size:8pt;color:#666;vertical-align:bottom;padding-bottom:2mm}
@bottom-center{content:"@ashrain.out  ·  " counter(page);font-family:'Noto Sans KR',sans-serif;font-size:7.5pt;color:#666;letter-spacing:.4px}}
@page:first{@top-right{content:none}}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:'Noto Sans KR',sans-serif;color:#111;font-size:10pt;line-height:1.6;word-break:keep-all;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.mi{font-family:'Noto Serif','Times New Roman',serif;font-style:italic;font-weight:400;padding:0 .04em}
b .mi{font-weight:400}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.08;font-size:.84em;margin:0 .35mm}
.fr>.n{border-bottom:.22mm solid currentColor;padding:0 .6mm .15mm}
.fr>.d{padding:.15mm .6mm 0}
sup,sub{font-size:.68em;line-height:0}
.rt{white-space:nowrap}.rt>.rb{border-top:.22mm solid currentColor;padding:0 .3mm;margin-left:.2mm}
svg{display:block}
.hd{display:flex;align-items:flex-end;justify-content:space-between;gap:6mm;border-bottom:.5mm solid #222;padding:0 0 2.2mm;margin:0 0 3mm}
.hd .t1{font-size:15pt;font-weight:700;letter-spacing:-.01em;line-height:1.3}
.hd .t2{font-size:8.6pt;color:#555;margin-top:.8mm}
.hd .hr{text-align:right;flex:none}
.hd .code{font-size:8pt;color:#555}
.hd .who{font-size:9pt;color:#333;margin-top:1.6mm;white-space:nowrap}
.hd .who u{display:inline-block;width:24mm;border-bottom:.25mm solid #777;margin:0 3mm 0 1.2mm;text-decoration:none}
.stg{display:flex;align-items:baseline;gap:2.4mm;padding:1.4mm 2.4mm;border:.3mm solid #444;border-radius:1.6mm;margin:0 0 2.4mm;font-size:9pt}
.stg .sn{font-weight:700;font-size:10pt;white-space:nowrap}
.stg .tip{color:#333}
.stg.cont{border-style:dashed;color:#555}
`;
}
function head(title, extra) {
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${esc(title)}</title>`
    + AV_PRINT_FONTS.map((u) => `<link rel="stylesheet" href="${u}">`).join("") + `<style>${extra}</style></head>`;
}
function header(meta, kind, n, who) {
  return `<header class="hd"><div class="hl"><div class="t1">${esc(meta.title)}</div>`
    + `<div class="t2">기본기 해설 · ${esc(meta.span)} · ${esc(unitLabel(meta.unit))} · ${kind} · ${n}문항 · 1 ~ 5단계</div></div>`
    + `<div class="hr"><div class="code">코드 ${fmtCode(meta.code)}</div>${who ? '<div class="who">이름<u></u>날짜<u></u></div>' : ""}</div></header>`;
}
const stageHead = (meta, set, st, cont) => `<div class="stg${cont ? " cont" : ""}"><span class="sn">${st}단계 · ${esc(meta.stages[st] || "")}${cont ? " (이어서)" : ""}</span>`
  + (cont ? "" : `<span class="tip">${mathHtml(set.tips?.[st] || "")}</span>`) + "</div>";

/* ══════════ 문제지 ══════════ */
const P_CSS = `.pg{height:${PAGE_H}mm;display:flex;flex-direction:column;break-after:page;overflow:hidden}
.pg:last-child{break-after:auto}
.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;column-gap:7mm;min-height:0}
.q{border-top:.25mm solid #999;padding:1.8mm .6mm 1.4mm;display:flex;flex-direction:column;min-height:0;overflow:hidden}
.qt{font-size:10pt;line-height:1.7}
.qt .no{display:inline-block;min-width:7mm;font-weight:700}
.qf{margin:1mm auto 0;width:34mm}
.qf svg{width:100%;height:auto}
.ab{margin-top:auto;align-self:flex-end;font-size:8.4pt;color:#444;border:.25mm solid #777;border-radius:1.4mm;padding:.5mm 2mm;min-width:32mm}
`;
export function problemsHtml(meta, set, figOf) {
  const pages = problemPages(set);
  const rows = Math.ceil(Math.max(2, set.pp || 10) / 2);
  const body = pages.map((p, i) => {
    const cells = p.items.map((it) => {
      const fig = it.qf && figOf ? figOf(it, "q") : "";
      return `<div class="q"><div class="qt"><span class="no">${it.no}.</span>${mathHtml(it.q)}</div>`
        + (fig ? `<div class="qf">${fig}</div>` : "") + `<div class="ab">답</div></div>`;
    }).join("");
    return `<section class="pg">${i === 0 ? header(meta, "문제지", set.items.length, true) : ""}${stageHead(meta, set, p.st, !p.first)}`
      + `<div class="grid" style="grid-template-rows:repeat(${rows},minmax(0,1fr))">${cells}</div></section>`;
  }).join("");
  return head(`${meta.short} 문제지`, css(meta.code) + P_CSS) + `<body><div class="av av-p">${body}</div></body></html>`;
}

/* ══════════ 해설지 ══════════ */
const S_CSS = `.note{border:.3mm solid #444;border-radius:1.6mm;padding:2mm 3mm;margin:0 0 3.4mm;font-size:9pt;line-height:1.7}
.note .nh{font-weight:700;margin-right:2mm}
.sh{margin:3.4mm 0 1.6mm;break-after:avoid}
.s{display:grid;grid-template-columns:minmax(0,1fr);column-gap:4mm;break-inside:avoid;border-top:.2mm solid #bbb;padding:2mm 0 2.2mm}
.s.wf{grid-template-columns:minmax(0,1fr) 34mm}
.sq{font-size:8.8pt;color:#333;line-height:1.6}
.sq .no{font-weight:700;color:#111;margin-right:1.2mm}
.sp{font-size:8.8pt;margin:.8mm 0 .6mm;color:#222}
.lb{display:inline-block;font-size:7.6pt;font-weight:700;border:.25mm solid #555;border-radius:1mm;padding:0 1.2mm;margin-right:1.6mm;line-height:1.5;vertical-align:.1em}
.sl{margin:0;padding:0;list-style:none}
.sl li{font-size:9.6pt;line-height:1.75;padding-left:2.6mm}
.sl .pre{color:#555;font-size:8.6pt;margin-right:1mm}
.memo{display:inline-block;font-size:7.8pt;color:#555;margin-left:2.6mm;padding-left:1.6mm;border-left:.35mm solid #888;line-height:1.35}
.sa{margin-top:.8mm;font-size:9.8pt;font-weight:700}
.sf svg{width:34mm;height:auto}
`;
export function solutionsHtml(meta, set, figOf) {
  let body = header(meta, "해설지", set.items.length, false);
  if (set.note) body += `<div class="note"><span class="nh">지도 도움말</span>${mathHtml(set.note)}</div>`;
  for (let st = 1; st <= 5; st++) {
    const list = set.items.filter((it) => it.st === st);
    if (!list.length) continue;
    body += `<div class="sh">${stageHead(meta, set, st, false)}</div>`;
    for (const it of list) {
      const fig = it.fig && figOf ? figOf(it, "end") : "";
      const lines = it.lines.map((ln) => `<li>${ln.pre ? `<span class="pre">${mathHtml(ln.pre)}:</span>` : ""}${mathHtml(ln.s)}`
        + (ln.memo ? `<span class="memo">${mathHtml(ln.memo)}</span>` : "") + "</li>").join("");
      body += `<div class="s${fig ? " wf" : ""}"><div class="st"><div class="sq"><span class="no">${it.no}.</span>${mathHtml(it.q)}</div>`
        + `<div class="sp"><span class="lb">${esc(it.planTag || "방침")}</span>${mathHtml(it.plan)}</div><ol class="sl">${lines}</ol>`
        + `<div class="sa"><span class="lb">답</span>${mathHtml(it.ans)}</div></div>${fig ? `<div class="sf">${fig}</div>` : ""}</div>`;
    }
  }
  return head(`${meta.short} 해설지`, css(meta.code) + S_CSS) + `<body><div class="av av-s">${body}</div></body></html>`;
}

/* ══════════ 빠른 정답 ══════════ */
const A_CSS = `.ak{display:grid;grid-template-columns:repeat(4,1fr);border-top:.3mm solid #444;border-left:.3mm solid #444;margin:0 0 3.2mm;break-inside:avoid}
.ak>div{border-right:.3mm solid #444;border-bottom:.3mm solid #444;padding:1.2mm 2mm;font-size:9.4pt;line-height:1.55;min-height:9mm;display:flex;align-items:center;gap:2mm}
.ak .no{flex:none;min-width:7mm;font-weight:700;color:#444}
.ak .an{min-width:0}
.ks{break-inside:avoid}
`;
export function answersHtml(meta, set) {
  let body = header(meta, "빠른 정답", set.items.length, false);
  for (let st = 1; st <= 5; st++) {
    const list = set.items.filter((it) => it.st === st);
    if (!list.length) continue;
    body += `<div class="ks"><div class="stg"><span class="sn">${st}단계 · ${esc(meta.stages[st] || "")}</span></div><div class="ak">`
      + list.map((it) => `<div><span class="no">${it.no}</span><span class="an">${mathHtml(it.ans)}</span></div>`).join("") + "</div></div>";
  }
  return head(`${meta.short} 빠른 정답`, css(meta.code) + A_CSS) + `<body><div class="av av-a">${body}</div></body></html>`;
}

/** 문서 하나 — doc: problems · solutions · answers */
export function avDocHtml(meta, set, doc, figOf) {
  if (doc === "problems") return problemsHtml(meta, set, figOf);
  if (doc === "solutions") return solutionsHtml(meta, set, figOf);
  if (doc === "answers") return answersHtml(meta, set);
  throw new Error(`알 수 없는 문서: ${doc}`);
}
