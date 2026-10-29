// ashrain.out — 컨셉 문제 「해설 영상」: 문항 하나 = 장면 하나 (교실 모니터 장면 형식 · 무대 1600×900)
//
// 장면 = { key, dur, title:{e,m}, sub:{e,m}, render(mode, t, C) } — 교실 모니터의 장면 묶음 재생기(frames/player.jsx 의 StoryPlayer)가
// 그대로 돌린다(자동으로 다음 장면 · 끝나면 처음부터 · 이 장면 반복 · 조작 막대 · 벽시계로 이어 보기).
// 한 장면의 흐름(박자표 — 글자 수로 읽는 시간을 어림한다)
//   ① 문제   — 발문(+자료 줄 · 보기 · 그림)을 크게
//   ② 방침   — 포지티브 · 네거티브 → 전략 (판서). 도식이 오른쪽에 함께 뜬다
//   ③ 전개   — 판서 줄이 하나씩, 줄마다 도식(표 · 그림)의 그 부분이 함께 빛난다(생성기가 붙인 애니메이션 큐 그대로)
//   ④ 확인 · 답
// 글자는 생성기 HTML(분수 · 강조)을 무대 수식 글자({분자/분모} · ‹강조›)로 바꿔 쓴다. 도식의 표는 무대 표(Table)로 다시 그리고,
// 그림(SVG)은 종이 카드 위에 그대로 얹어 짚는 부분만 빨갛게 칠한다(그 그림 안에서만 듣는 <style>).
// 배치(줄바꿈 · 글자 크기)는 글자 폭을 재서 정하므로 글꼴이 늦게 오면 다시 잰다(bumpFontEpoch). 박자는 글꼴과 상관없다.
import { MText, Caption, Table, mathWidth } from "../../features/display/draw.jsx";
import { seg, win, E, clamp } from "../../features/display/core.js";
import { LEVEL_NAME } from "./labels";

const EMPTY = new Set();

/* ══════════ 글자 ══════════ */
const ENT = { "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#x27;": "'", "&#39;": "'", "&nbsp;": " " };
const strip = (h) => String(h ?? "").replace(/<[^>]+>/g, "");
const keep = (s) => s.replace(/[ \t\r\n]+/g, " ");          // 줄을 바꾸지 않을 덩어리(분수 · nw) — 안의 빈칸을 붙은 빈칸으로

/** 생성기 HTML → 무대 수식 글자 */
export function toStage(html) {
  let s = String(html ?? "");
  s = s.replace(/<span class="fr"><span class="n">([\s\S]*?)<\/span><span class="d">([\s\S]*?)<\/span><\/span>/g,
    (m, n, d) => `{${keep(strip(n).trim())}/${keep(strip(d).trim())}}`)
    .replace(/<span class="nw">([\s\S]*?)<\/span>/g, (m, x) => keep(x.trim()))
    .replace(/<i class="v">([\s\S]*?)<\/i>/g, "$1")
    .replace(/<span class="cd">([\s\S]*?)<\/span>/g, "$1")
    .replace(/<b>([\s\S]*?)<\/b>/g, "‹$1›")
    .replace(/<br\s*\/?>/g, " ")
    .replace(/<[^>]+>/g, "")
    .replace(/&(amp|lt|gt|quot|#x27|#39|nbsp);/g, (m) => ENT[m] || m);
  return s.replace(/\*/g, "∗").replace(/[ \t\r\n]+/g, " ").trim();
}
/** 강조 표시를 뺀 글자 */
export const plain = (s) => String(s ?? "").replace(/[‹›]/g, "");
/** 머리글(제목 줄)용 — 분수 괄호도 푼다 */
const flat = (s) => plain(s).replace(/\{([^}/]*)\/([^}]*)\}/g, "$1/$2");
/** 생성기 HTML → 한 줄 글자(목록 · 제목) */
export const stageTitle = (html) => flat(toStage(html));
/** 글자 수(읽는 시간 어림) — 분수는 두 글자쯤 */
const plainLen = (s) => String(s ?? "").replace(/\{[^}]*\}/g, "00").replace(/[‹›]/g, "").length;
/** 글자를 쪼개는 단위 — 분수 덩어리는 하나로 */
const toks = (s) => String(s).match(/\{[^}]*\}|./gu) || [];

/** 무대 글자 줄바꿈 — 빈칸에서 바꾸고, 강조(‹ ›)가 줄을 넘으면 다음 줄에서 다시 연다 */
export function wrapStage(s, size, maxW, weight = 560) {
  const words = String(s || "").split(" ").filter(Boolean);
  const lines = [];
  let line = "";
  const fits = (x) => mathWidth(x, size, weight) <= maxW;
  const push = (x) => { if (x) lines.push(x); };
  for (const w of words) {
    const test = line ? `${line} ${w}` : w;
    if (fits(test)) { line = test; continue; }
    push(line);
    if (fits(w)) { line = w; continue; }
    // 한 낱말이 너무 길면 글자로 자른다(분수 덩어리는 쪼개지 않는다)
    let cur = "";
    for (const ch of toks(w)) {
      if (cur && !fits(cur + ch)) { push(cur); cur = ch; } else cur += ch;
    }
    line = cur;
  }
  push(line);
  // 강조 짝 맞추기
  let open = false;
  return lines.map((L) => {
    let x = (open ? "‹" : "") + L;
    const o = (x.match(/‹/g) || []).length, c = (x.match(/›/g) || []).length;
    open = o > c;
    if (open) x += "›";
    return x;
  });
}

/** 줄 끝을 「…」로 — 넘치면 글자를 덜어 낸다 */
function withEllipsis(s, size, maxW, weight) {
  const tk = toks(s.replace(/›$/, ""));
  const mk = () => {
    const x = tk.join("");
    const open = (x.match(/‹/g) || []).length > (x.match(/›/g) || []).length;
    return `${x}${open ? "›" : ""} …`;
  };
  while (tk.length > 1 && mathWidth(mk(), size, weight) > maxW) tk.pop();
  return mk();
}

/* ══════════ 도식 ══════════ */
/** 생성기 표 HTML(.tbl) → { head:[…], rows:[[…]], foot } */
export function parseTbl(html) {
  const head = [...((html.match(/<thead>([\s\S]*?)<\/thead>/) || [])[1] || "").matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map((m) => toStage(m[1]));
  const body = (html.match(/<tbody>([\s\S]*?)<\/tbody>/) || [])[1] || "";
  const rows = [...body.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/g)].map((m) => [...m[1].matchAll(/<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/g)].map((x) => toStage(x[1])));
  const foot = toStage((html.match(/<tfoot>[\s\S]*?<td[^>]*>([\s\S]*?)<\/td>/) || [])[1] || "");
  return { head, rows, foot };
}

const HL = "#d1495b", GLOW = "rgba(255,196,0,.9)";
const SHAPES = ["line", "path", "polygon", "circle", "rect", "ellipse", "polyline"];
/**
 * 그림 안에서만 듣는 강조 규칙 — 그림 id 로 범위를 묶는다(장면이 겹쳐 넘어갈 때 다른 그림을 칠하지 않게).
 * keys: 짚는 키(data-k · data-ka). sw: 강조 선 굵기(그림 단위)
 */
export function hiCss(id, keys, sw = 0.6) {
  const A = [...keys].flatMap((k) => [`[data-k="${k}"]`, `[data-ka~="${k}"]`]);
  if (!A.length) return "";
  const p = (s) => `#${id} ${s}`;
  const shape = A.flatMap((a) => SHAPES.flatMap((tg) => [p(`${tg}${a}`), p(`g${a} ${tg}`)]));
  const text = A.flatMap((a) => [p(`text${a}`), p(`g${a} text`)]);
  const glow = A.flatMap((a) => [p(`g${a}`), ...SHAPES.map((tg) => p(`${tg}${a}`))]);
  return `<style>${shape.join(",")}{stroke:${HL}!important;stroke-width:${sw}px;stroke-opacity:1;opacity:1!important}`
    + `${A.map((a) => p(`polygon${a}`)).join(",")}{fill:${HL}!important;fill-opacity:.2}`
    + `${text.join(",")}{fill:${HL}!important;font-weight:700}`
    + `${glow.join(",")}{filter:drop-shadow(0 0 ${(sw * 0.8).toFixed(2)}px ${GLOW})}</style>`;
}

/** 그림 SVG 를 무대 상자에 맞춘 자리 */
function fitSvg(svg, box, maxScale = 13) {
  const open = String(svg || "").match(/<svg\b[^>]*>/);
  const m = open && open[0].match(/viewBox="([^"]+)"/);
  if (!m) return null;
  const vb = m[1].trim().split(/[\s,]+/).map(Number);
  if (vb.length !== 4 || vb.some((v) => !Number.isFinite(v)) || vb[2] <= 0 || vb[3] <= 0) return null;
  const s = Math.min(box.w / vb[2], box.h / vb[3], maxScale);
  const w = vb[2] * s, h = vb[3] * s;
  const ff = (open[0].match(/font-family="([^"]*)"/) || [])[1] || "'Noto Serif KR', serif";
  return { vb, s, w, h, x: box.x + (box.w - w) / 2, y: box.y + (box.h - h) / 2, open: open[0], ff };
}
/** 무대에 얹을 SVG 글자 — 여는 꼬리표를 무대 자리 · 크기로 바꾸고 강조 규칙을 넣는다 */
function svgMarkup(svg, f, id, keys) {
  const head = `<svg id="${id}" x="${f.x.toFixed(1)}" y="${f.y.toFixed(1)}" width="${f.w.toFixed(1)}" height="${f.h.toFixed(1)}" `
    + `viewBox="${f.vb.join(" ")}" font-family="${f.ff}" overflow="visible" xmlns="http://www.w3.org/2000/svg">`
    + hiCss(id, keys, Math.max(0.3, f.vb[2] * 0.018));
  return svg.replace(f.open, () => head);
}

/* ══════════ 박자 ══════════ */
const readMs = (s, base, per, lo, hi) => clamp(base + plainLen(s) * per, lo, hi);
const keysOf = (st) => {
  const out = new Set();
  for (const c of st || []) for (const k of [].concat(c.k)) if (k && !/^(line|hint):/.test(k)) out.add(String(k));
  return out;
};

/** 문항 하나의 글자 · 박자(글꼴과 상관없다) */
export function timing(it) {
  const s = it.s || {};
  const q = toStage(it.q);
  const rows = (it.rows || []).map((r) => (Array.isArray(r) ? r : [r]).map(toStage));
  const box = (it.box || []).map(toStage);
  const board = (s.board && s.board.length ? s.board : (s.steps || []).map((t) => ({ h: "", t })))
    .map((b) => ({ h: toStage(b.h), t: toStage(b.t) }));
  const pos = toStage(s.pos), neg = toStage(s.neg), pl = toStage(s.plan), check = toStage(s.check);
  const ans = toStage(it.a?.t || "");
  // ① 문제 — 발문 + 자료 줄 · 보기 · 그림을 읽는 시간
  const extra = rows.reduce((a, r) => a + plainLen(r.join(" ")), 0) * 45 + box.reduce((a, b) => a + plainLen(b), 0) * 50 + (it.fig ? 1500 : 0);
  const tA = clamp(3200 + plainLen(q) * 70, 6500, 17000) + clamp(extra, 0, 14000);
  // ② 방침
  const tPos = tA + 600, tNeg = tPos + readMs(pos, 1400, 60, 2400, 4800), tPlan = tNeg + readMs(neg, 1400, 60, 2400, 4800);
  const tB = tPlan + readMs(pl, 1400, 60, 2400, 4800) + 700;
  // ③ 전개 — 줄마다 읽는 시간
  const steps = [];
  let at = tB + 900;
  for (const b of board) { const d = readMs(`${b.h} ${b.t}`, 1600, 75, 3000, 6400); steps.push({ t: at, d }); at += d; }
  const tC = at + 600;
  // ④ 확인 · 답
  const tChk = tC + 500, tAns = tChk + readMs(check, 1800, 60, 2800, 5600);
  const dur = tAns + 4600;
  // 도식 · 줄마다 짚는 키(생성기 큐: 그 줄을 여는 reveal line:i 가 든 단계, 없으면 i 번째 단계)
  const dg = s.dg || "";
  const isTbl = /^\s*<table/i.test(dg);
  const anim = Array.isArray(s.anim) ? s.anim : [];
  const cueOf = (i) => anim.find((st) => (st || []).some((c) => c.act === "reveal" && c.k === `line:${i}`)) || anim[i] || [];
  const stepKeys = board.map((_, i) => keysOf(cueOf(i)));
  const resKeys = anim.some((st) => (st || []).some((c) => [].concat(c.k).includes("res"))) ? new Set(["res"]) : EMPTY;
  const T = { q, rows, box, board, pos, neg, pl, check, ans, tA, tPos, tNeg, tPlan, tB, steps, tC, tChk, tAns, dur,
    dg, isTbl, tbl: isTbl ? parseTbl(dg) : null, stepKeys, resKeys };
  T.caps = captions(T, it);
  return T;
}

/** 지금 짚는 도식 키 — 전개 i 번째 줄 동안 큐 i 의 키들, 확인 · 답 동안 결과(res) */
export function activeKeys(T, t) {
  if (!T.steps.length || t < T.steps[0].t) return EMPTY;
  if (t >= T.tC) return T.resKeys;
  let i = 0;
  while (i + 1 < T.steps.length && t >= T.steps[i + 1].t) i++;
  return T.stepKeys[i] || EMPTY;
}

/** 자막 — 흐름을 짧게 */
function captions(T, it) {
  const caps = [{ t: 300, s: `${it.no}번 — 문제를 천천히 읽어요`, u: T.tA }];
  caps.push({ t: T.tA + 200, s: "되는 것 · 안 되는 것으로 나눠 읽어요", u: T.tB });
  T.board.forEach((b, i) => caps.push({
    t: T.steps[i].t, u: T.steps[i].t + T.steps[i].d,
    s: b.h ? flat(b.h) : i === T.board.length - 1 ? "식을 마무리해요" : "식을 세워 계산해요",
  }));
  caps.push({ t: T.tC + 200, s: "다른 길로 확인해요", u: T.tAns });
  caps.push({ t: T.tAns, s: `답  ${plain(T.ans)}` });
  return caps;
}

/* ══════════ 배치(글자 폭을 잰다) ══════════ */
const BAND = { size: 26, lh: 38, y: 152, w: 1490 };
const BOARD = { x: 96, wDg: 760, wAll: 1400, bottom: 790, sizes: [34, 32, 30, 28, 26, 24] };
export const DG_BOX = { x: 900, w: 640, bottom: 790 };

/** 판서 줄 — 방침 · 전개 · 확인과 답 (긴 줄은 접어서 여러 줄, 접힌 줄은 같은 시각에 함께 뜬다) */
function boardLines(T, bw, size) {
  const lines = [];
  let row = 0;
  const ind = Math.round(size * 0.8);
  const add = (s, t, u, opt = {}) => {
    const w = bw - (opt.dot ? ind : 0);
    wrapStage(s, opt.size || size, w, 560).forEach((p, i) =>
      lines.push({ t, u, s: p, row: row++, size: opt.size, ind: opt.dot ? ind : 0, dot: i === 0 ? opt.dot : undefined }));
  };
  // ② 방침
  lines.push({ t: T.tA + 100, u: T.tB, s: "방침 — 규칙을 나눠 읽고 셀 길을 정해요", k: "h", row: row++ });
  add(`포지티브 · ${T.pos}`, T.tPos, T.tB, { dot: "teal" });
  add(`네거티브 · ${T.neg}`, T.tNeg, T.tB, { dot: "coral" });
  add(`→ ${T.pl}`, T.tPlan, T.tB);
  // ③ 전개
  row = 0;
  lines.push({ t: T.tB + 100, u: T.tC, s: "전개 — 식을 세워 계산해요", k: "h", row: row++ });
  T.board.forEach((b, i) => add(b.h ? `‹${plain(b.h)}›  ${b.t}` : b.t, T.steps[i].t, T.tC));
  // ④ 확인 · 답
  row = 0;
  lines.push({ t: T.tC + 100, s: "확인 — 다른 길로 다시 봐요", k: "h", row: row++ });
  add(T.check, T.tChk, undefined);
  row += 0.35;
  add(`답   ‹${plain(T.ans)}›`, T.tAns, undefined, { size: Math.round(size * 1.3) });
  return lines;
}
const lastRow = (lines) => Math.max(0, ...lines.map((L) => L.row));

/** ① 문제를 크게 — 발문 · 자료 줄 · 보기 · 그림의 자리 */
function bigLayout(T, it, id) {
  const fig = it.fig ? fitSvg(it.fig, { x: 1110, y: 200, w: 420, h: 520 }, 12) : null;
  const maxW = fig ? 1000 : 1460;
  let size = 40;
  let lines = wrapStage(T.q, size, maxW);
  const cap = T.rows.length || T.box.length ? 5 : 8;
  while (lines.length > cap && size > 30) { size -= 2; lines = wrapStage(T.q, size, maxW); }
  const lh = Math.round(size * 1.55);
  let y = 196 + (lines.length - 1) * lh + size * 0.4;          // 아래로 쓸 자리(위 끝)
  // 자료 줄: 이름 · 내용(길면 접는다)
  let rows = null;
  if (T.rows.length) {
    const rs = 26, rl = Math.round(rs * 1.5);
    const labW = Math.max(0, ...T.rows.map((r) => (r.length > 1 ? mathWidth(r[0], rs, 700) : 0))) + 34;
    const tw = maxW - labW - 24;
    y += 22;
    rows = { size: rs, lh: rl, labW, top: y, items: [] };
    for (const r of T.rows) {
      const lab = r.length > 1 ? r[0] : "";
      const txt = r.length > 1 ? r.slice(1).join(" ") : r[0] || "";
      const tl = wrapStage(txt, rs, tw, 540);
      const h = 14 + tl.length * rl;
      rows.items.push({ lab, lines: tl, top: y, h });
      y += h;
    }
    rows.bottom = y;
    y += 12;
  }
  // 보기
  let box = null;
  if (T.box.length) {
    const bs = 30, bl = Math.round(bs * 1.6);
    const wrapped = T.box.flatMap((b) => wrapStage(b, bs, maxW - 70, 540));
    y += 26;
    box = { size: bs, lh: bl, top: y, h: wrapped.length * bl + 24, lines: wrapped };
    y += box.h + 10;
  }
  // 넘치면 통째로 줄인다(왼쪽 위 기준)
  const k = y > 800 ? (800 - 160) / (y - 160) : 1;
  return { size, lh, lines, rows, box, maxW, k, bottom: y, fig, figHtml: fig ? svgMarkup(it.fig, fig, id + "q", EMPTY) : "" };
}

/** 도식 표의 자리 — 상자에 들어가게 글자를 줄이고, 그래도 넘치면 통째로 줄인다 */
function tableLayout(T, box) {
  const ncol = Math.max(1, T.head.length, ...T.rows.map((r) => r.length));
  const colW = (sz) => Array.from({ length: ncol }, (_, c) =>
    Math.max(mathWidth(T.head[c] || "", sz, 800), ...T.rows.map((r) => mathWidth(r[c] || "", sz, 800))) + sz * 1.3);
  const rh0 = (sz) => Math.round(sz * 1.75);
  const hTot = (sz) => rh0(sz) * (T.rows.length + (T.head.length ? 1 : 0)) + (T.foot ? sz * 1.9 : 0);
  const wTot = (sz, cols) => Math.max(cols.reduce((a, b) => a + b, 0), T.foot ? mathWidth(T.foot, sz, 800) : 0);
  let size = 28, cols = colW(size);
  while ((wTot(size, cols) > box.w || hTot(size) > box.h) && size > 16) { size -= 2; cols = colW(size); }
  const wsum = cols.reduce((a, b) => a + b, 0);
  const k = Math.min(1, box.w / wTot(size, cols), box.h / hTot(size));
  return { size, cols, ncol, wsum, rh: rh0(size), k, x0: box.x + Math.max(0, (box.w - wTot(size, cols) * k) / 2) + (wTot(size, cols) - wsum) * k, y0: box.y + 6,
    w: wTot(size, cols) * k, h: hTot(size) * k };
}

/** 문항 하나의 배치 */
export function layout(T, it, id) {
  // 위 띠(②~④ 동안 문제를 작게, 세 줄까지)
  const ql = wrapStage(T.q, BAND.size, BAND.w, 540);
  const band = ql.slice(0, 3);
  if (ql.length > 3) band[2] = withEllipsis(band[2], BAND.size, BAND.w, 540);
  const topY = BAND.y + band.length * BAND.lh + 20;
  // 판서 — 들어가는 가장 큰 글자로
  const bw = T.dg ? BOARD.wDg : BOARD.wAll;
  let pick = null;
  for (const sz of BOARD.sizes) {
    const lines = boardLines(T, bw, sz);
    const lh = Math.round(sz * 1.58), y0 = topY + sz + 6, n = lastRow(lines);
    pick = { size: sz, lines, lh, y0, n };
    if (y0 + n * lh <= BOARD.bottom) break;
  }
  if (pick.y0 + pick.n * pick.lh > BOARD.bottom) pick.lh = Math.max(Math.round(pick.size * 1.22), Math.floor((BOARD.bottom - pick.y0) / Math.max(1, pick.n)));
  // 도식
  let dgL = null;
  if (T.dg) {
    const box = { x: DG_BOX.x, y: topY, w: DG_BOX.w, h: DG_BOX.bottom - topY };
    dgL = T.isTbl ? { tbl: tableLayout(T.tbl, box) }
      : { fit: fitSvg(T.dg, { x: box.x + 18, y: box.y + 18, w: box.w - 36, h: box.h - 36 }, 13), cache: new Map() };
  }
  return { band, topY, bx: BOARD.x, bw, by: pick.y0, size: pick.size, lh: pick.lh, lines: pick.lines, dgL, big: bigLayout(T, it, id), jsx: {} };
}

/* ══════════ 장면 ══════════ */
/** 글꼴이 늦게 오면 다시 재도록 — 해설 영상 화면이 글꼴을 다 받은 뒤 부른다 */
let fontEpoch = 0;
export function bumpFontEpoch() { fontEpoch++; }

export function solutionScene(set, it, idx, total) {
  const T = timing(it);
  const id = `cvd-${String(set.no ?? "s").replace(/[^0-9A-Za-z_-]/g, "")}-${idx}`;
  let L = null, epoch = -1;
  const lay = () => {
    if (!L || epoch !== fontEpoch) { L = layout(T, it, id); epoch = fontEpoch; }
    return L;
  };
  const title = `${it.no}. ${flat(toStage(it.ty))}`;
  const sub = `${set.short} · ${it.lv}(${LEVEL_NAME[it.lv] || ""}) · ${flat(toStage(it.sp))}`;
  return {
    key: `${set.key}-${it.id}`,
    dur: T.dur,
    title: { e: title, m: title },
    sub: { e: sub, m: sub },
    render: (mode, t, C) => renderScene(T, lay(), it, t, C, idx, total, id),
    timing: T, layout: lay,                     // 검산 · 목록용
  };
}

export function solutionScenes(set) {
  return set.items.map((it, i) => solutionScene(set, it, i, set.items.length));
}

function renderScene(T, L, it, t, C, idx, total, id) {
  const out = [];
  // 오른쪽 위: 몇 번째 문항인지
  out.push(<MText key="cnt" x={1544} y={70} s={`${idx + 1} / ${total}`} size={26} weight={700} anchor="end" fill={C.soft} C={C} />);

  /* ① 문제(크게) — 방침이 시작되면 위쪽 띠로 작아진다 */
  const big = 1 - seg(t, T.tA - 500, T.tA + 300, E.sine);
  const small = seg(t, T.tA, T.tA + 700, E.sine);
  if (big > 0.001) out.push(<g key="qa" opacity={big}>{bigEl(L, C)}</g>);
  if (small > 0.001) {
    out.push(<g key="qs" opacity={small * 0.9}>
      {L.band.map((s, i) => <MText key={i} x={56} y={BAND.y + i * BAND.lh} s={s} size={BAND.size} weight={540} fill={C.soft} C={C} />)}
    </g>);
  }

  /* ②③④ 판서 + 도식 */
  if (t >= T.tA) {
    out.push(<SolBoard key="bd" x={L.bx} y={L.by} t={t} lines={L.lines} C={C} size={L.size} lh={L.lh} />);
    if (L.dgL) out.push(<g key="dg" opacity={seg(t, T.tA + 200, T.tA + 1000, E.sine)}>{diagramEl(T, L, t, C, id)}</g>);
  }

  /* 자막 */
  out.push(<Caption key="cap" t={t} caps={T.caps} C={C} size={32} />);
  return <g>{out}</g>;
}

/** ① 문제 크게 — 테마마다 한 번 만들어 둔다(매 장면 다시 만들지 않게) */
function bigEl(L, C) {
  if (L.jsx[C.name]) return L.jsx[C.name];
  const B = L.big;
  const els = [];
  B.lines.forEach((s, i) => els.push(<MText key={"q" + i} x={70} y={196 + i * B.lh} s={s} size={B.size} weight={560} C={C} />));
  if (B.rows) {
    const R = B.rows;
    els.push(<rect key="rbg" x={70} y={R.top} width={R.labW} height={R.bottom - R.top} fill={C.faint} opacity={0.55} />);
    R.items.forEach((r, i) => {
      const base = r.top + 8 + R.size * 0.98;
      els.push(<g key={"r" + i}>
        <line x1={70} x2={70 + B.maxW} y1={r.top} y2={r.top} stroke={C.soft} strokeWidth={i ? 1.2 : 2.2} opacity={0.7} />
        {r.lab && <MText x={70 + R.labW / 2} y={base} s={r.lab} size={R.size} weight={700} anchor="middle" fill={C.soft} C={C} />}
        {r.lines.map((s, j) => <MText key={j} x={70 + R.labW + 22} y={base + j * R.lh} s={s} size={R.size} weight={540} C={C} />)}
      </g>);
    });
    els.push(<line key="rend" x1={70} x2={70 + B.maxW} y1={R.bottom} y2={R.bottom} stroke={C.soft} strokeWidth={2.2} opacity={0.7} />);
  }
  if (B.box) {
    const X = B.box;
    els.push(<g key="box">
      <rect x={70} y={X.top} width={B.maxW} height={X.h} rx={14} fill="none" stroke={C.soft} strokeWidth={2} />
      <rect x={70 + B.maxW / 2 - 50} y={X.top - 16} width={100} height={30} rx={8} fill={C.paper} />
      <MText x={70 + B.maxW / 2} y={X.top + 8} s="보기" size={24} weight={700} anchor="middle" fill={C.soft} C={C} />
      {X.lines.map((s, i) => <MText key={i} x={100} y={X.top + 44 + i * X.lh} s={s} size={X.size} weight={540} C={C} />)}
    </g>);
  }
  if (B.fig) {
    const f = B.fig;
    els.push(<g key="fig">
      <rect x={f.x - 18} y={f.y - 18} width={f.w + 36} height={f.h + 36} rx={16} fill="#fbf8ef" stroke="rgba(0,0,0,.08)" />
      <g dangerouslySetInnerHTML={{ __html: B.figHtml }} />
    </g>);
  }
  const el = B.k < 1
    ? <g transform={`translate(${(70 * (1 - B.k)).toFixed(1)} ${(160 * (1 - B.k)).toFixed(1)}) scale(${B.k.toFixed(4)})`}>{els}</g>
    : <g>{els}</g>;
  L.jsx[C.name] = el;
  return el;
}

/**
 * 판서 — 교실 모니터 Board 와 같은 모양(나타날 때 살짝 올라오고, 지금 줄에 금빛 막대, 앞 줄은 조금 흐려진다).
 * 한 줄이 길어 접힌 줄들은 같은 시각에 뜨므로 한 덩어리로 또렷하고, 금빛 막대도 덩어리 전체에 걸친다.
 */
function SolBoard({ x, y, t, lines, C, size, lh, dim = 0.62 }) {
  const vis = lines.filter((L) => t >= L.t && (L.u == null || t < L.u));
  if (!vis.length) return null;
  let curT = -Infinity;
  for (const L of vis) if (L.t > curT) curT = L.t;
  const fade = seg(t, curT, curT + 500);
  const hs = Math.round(size * 0.72);
  const out = [];
  const cur = vis.filter((L) => L.t === curT && L.k !== "h");
  if (cur.length) {
    const slide = (1 - seg(t, curT, curT + 420, E.out)) * 12;
    const r0 = Math.min(...cur.map((L) => L.row)), r1 = Math.max(...cur.map((L) => L.row));
    const top = y + r0 * lh - (cur[0].size || size) * 0.95 + slide, bot = y + r1 * lh + size * 0.2 + slide;
    out.push(<rect key="bar" x={x - 22} y={top} width={6} height={bot - top} rx={3} fill={C.bar} opacity={win(t, curT, cur[0].u ?? Infinity, 420, 320)} />);
  }
  vis.forEach((L, i) => {
    const a = win(t, L.t, L.u ?? Infinity, 420, 320);
    const head = L.k === "h";
    const yy = y + L.row * lh + (1 - seg(t, L.t, L.t + 420, E.out)) * 12;
    const sz = head ? hs : (L.size || size);
    out.push(
      <g key={i} opacity={a * (L.t === curT || head ? 1 : 1 - (1 - dim) * fade)}>
        {L.dot && <circle cx={x + size * 0.32} cy={yy - size * 0.36} r={size * 0.24} fill={C[L.dot] || L.dot} />}
        <MText x={x + (L.ind || 0)} y={yy} s={L.s} size={sz} weight={head ? 600 : 560} fill={head ? C.soft : C.ink} C={C} />
      </g>,
    );
  });
  return <g>{out}</g>;
}

/** 도식: 표는 무대 표로, 그림은 종이 카드 위에 */
function diagramEl(T, L, t, C, id) {
  const act = activeKeys(T, t);
  const D = L.dgL;
  if (D.tbl) return tableEl(T.tbl, D.tbl, act, t, C);
  const f = D.fit;
  if (!f) return null;
  const sig = [...act].sort().join("|");
  let html = D.cache.get(sig);
  if (html == null) { html = svgMarkup(T.dg, f, id, act); D.cache.set(sig, html); }
  return (<g>
    <rect x={f.x - 20} y={f.y - 20} width={f.w + 40} height={f.h + 40} rx={18} fill="#fbf8ef" stroke="rgba(0,0,0,.08)" />
    <g dangerouslySetInnerHTML={{ __html: html }} />
  </g>);
}

function tableEl(T, D, act, t, C) {
  const rows = [];
  if (T.head.length) rows.push(Array.from({ length: D.ncol }, (_, c) => ({ s: T.head[c] || "", weight: 800, fill: "faint", fo: 0.55 })));
  T.rows.forEach((r, i) => {
    const on = act.has(`row:${i}`) || (i === T.rows.length - 1 && act.has("res") && !T.foot);
    rows.push(Array.from({ length: D.ncol }, (_, c) => ({ s: r[c] || "", weight: on ? 800 : 600, fill: on ? "gold" : undefined, fo: on ? 0.3 : 0, color: on ? "red" : undefined })));
  });
  const hY = D.y0 + D.rh * rows.length;
  const footOn = act.has("res");
  const fw = T.foot ? mathWidth(T.foot, D.size, 800) : 0;
  const body = (<g>
    <Table x={D.x0} y={D.y0} cols={D.cols} rh={D.rh} rows={rows} C={C} size={D.size} />
    {T.foot && <g>
      <MText x={D.x0 + D.wsum} y={hY + D.size * 1.35} s={T.foot} size={D.size} weight={800} anchor="end" fill={footOn ? C.red : C.coral} C={C} />
      {footOn && <rect x={D.x0 + D.wsum - fw} y={hY + D.size * 1.55} width={fw} height={4} rx={2} fill={C.gold} opacity={0.6 + 0.4 * Math.sin(t / 220)} />}
    </g>}
  </g>);
  if (D.k >= 1) return body;
  // 통째로 줄일 때는 표의 왼쪽 위를 기준으로
  return <g transform={`translate(${(D.x0 * (1 - D.k)).toFixed(1)} ${(D.y0 * (1 - D.k)).toFixed(1)}) scale(${D.k.toFixed(4)})`}>{body}</g>;
}
