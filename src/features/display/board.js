// ashrain.out — 해설 액자의 글자 판 배치 (board.js) — 그리기는 frames/board.jsx
// 일차함수 10단계 · 그래프와 넓이 · 경우의 수와 확률 100제 · 기본기 해설(초등 · 중등 · 고등 단원)이 같은 규칙으로 글자 판을 놓는다.
//   ① 글자 크기는 정해진 두 벌(BOARD_TYPE) — 기본으로 다 들어가면 기본, 아니면 촘촘. 문항마다 들쭉날쭉하지 않게.
//      기본은 교실 모니터(15.6형)를 약 1 m 떨어져 봐도 읽히는 크기 — 판서 42 · 문제 40 · 머리말 · 메모 30.
//   ② 문제(발문)는 판 너비를 다 쓴다 — 줄바꿈을 줄인다. 그 아래 방침 · 판서 줄 · 답.
//   ③ 그림은 글자를 다 놓고 남은 빈자리에 — 판서 줄 오른쪽에서 가장 넉넉한 빈 칸을 찾아 넣는다(무대 넓이의 25%까지).
//      판서 칸 너비를 넓은 것부터 몇 가지로 놓아 보고, 그림이 넉넉히 들어가는 가장 넓은 칸을 고른다.
//      그림을 배율 0.6 아래로 줄여야만 들어가면 그림을 뺀다(글자가 먼저).
//   ④ 촘촘으로도 넘치면 판서가 위로 흐른다 — 문제는 위에 그대로, 방침 · 판서 · 답 칸만 흘러 지금 줄이 늘 보인다(boardScroll).
// 판(region): 단일 모드는 무대 전체(STAGE_REGION), 듀얼 모드는 반쪽 판(PANE_REGION — 800 × 900, 무대와 같은 배율).
//   개념 설명의 움직이는 예시(components/ConceptAv.jsx)는 제 판을 쓴다 — 넓은 판 · 좁은 판(세로로 긴 판 — 그림은 글자 아래), figTop 이면 그림을 남은 칸 위에 붙인다.
import { mathWidth } from "./draw.jsx";
import { seg, E } from "./core.js";

export const STAGE_W = 1600, STAGE_H = 900;
export const STAGE_REGION = { key: "stage", left: 60, right: 1540, top: 168, bottom: 866 };
export const PANE_W = 800, PANE_H = 900;
export const PANE_REGION = { key: "pane", left: 46, right: 760, top: 152, bottom: 868 };

/** 글자 크기 두 벌 — q 문제 · b 판서 · s 머리말 · 메모 · plan 방침 */
export const BOARD_TYPE = [
  { key: "base", q: 40, b: 42, s: 30, plan: 32 },
  { key: "tight", q: 36, b: 37, s: 28, plan: 30 },
];
export const FIG_AREA = 0.25;      // 그림이 차지할 수 있는 무대 넓이의 몫
export const FIG_MIN = 0.6;        // 그림 배율이 이보다 작아야 들어가면 그림을 뺀다
const COLS = [1, 0.8, 0.7, 0.62, 0.55, 0.5];   // 판서 칸 너비(판 너비에 대한 몫) — 넓은 것부터 놓아 본다
const GAP_FIG = 44;                // 글자와 그림 사이

/* ══════════ 글자 높이 ══════════ */
const hasFrac = (s) => /\{[^{}]*\/[^{}]*\}/.test(String(s)) || /\{[^}]*\{/.test(String(s));
const hasSup = (s) => String(s).includes("^{") || String(s).includes("\u20D7");     // 위 첨자 · 벡터 화살
/** 행렬 ⟦1, 2; 3, 4⟧ 의 가장 많은 줄 수 — 없으면 0 (행렬은 가운데 축 위아래로 줄 수만큼 높다, draw.jsx) */
const matRows = (s) => Math.max(0, ...[...String(s).matchAll(/⟦([^⟧]*)⟧/g)].map((m) => m[1].split(";").length));
export const upOf = (s, z) => { const r = matRows(s); return z * Math.max(r ? 0.46 + r * 0.5 : 0, hasFrac(s) ? 1.04 : hasSup(s) ? 0.92 : 0.8); };
export const dnOf = (s, z) => { const r = matRows(s); return z * Math.max(r ? r * 0.5 - 0.16 : 0, hasFrac(s) ? 0.52 : String(s).includes("_{") ? 0.36 : 0.24); };

/* ══════════ 줄 바꾸기 ══════════ */
const HANGUL = /[가-힣]/;
const openParen = (a) => (a.match(/\(/g) || []).length > (a.match(/\)/g) || []).length;
/** 줄을 크게 나눌 자리 — 「→」 앞 · 괄호 밖 쉼표 뒤 */
const strongBreak = (a, b) => b.startsWith("→") || (a.endsWith(",") && !openParen(a));
/** 띄어쓰기 자리 중 줄을 바꿔도 되는 곳 — 식 가운데(= + − × 옆) · 좌표 가운데는 안 되고, 큰 자리 · 한글 낱말 사이만 */
function canBreak(a, b) {
  if (strongBreak(a, b)) return true;
  if (a.endsWith(":") && HANGUL.test(a)) return true;
  return HANGUL.test(a) && HANGUL.test(b) && !/[=+−×]$/.test(a) && !/^[=+−×]/.test(b) && !openParen(a);
}
/** 그래도 길면 — 「=」 앞에서(이어지는 줄이 「= …」로 시작) */
const eqBreak = (a, b) => canBreak(a, b) || ((b === "=" || b.startsWith("=")) && !openParen(a));
const anyBreak = (a) => !openParen(a);
function chunksOf(words, test) {
  const out = [];
  let cur = [];
  words.forEach((w, i) => { cur.push(w); if (i === words.length - 1 || test(cur.join(" "), words[i + 1])) { out.push(cur.join(" ")); cur = []; } });
  return out;
}
/**
 * 수식 글자 줄 바꾸기 — 넓이 maxW 안에. strong: 풀이 줄(「→」 앞 · 쉼표 뒤에서 먼저 나눠 본다).
 * 나눌 자리는 큰 자리 → 한글 낱말 사이 → 「=」 앞 → 괄호 밖 띄어쓰기 차례로 — 앞 것으로 안 되는 덩이만 다음 것으로.
 */
export function wrapMath(s, size, maxW, weight = 560, strong = false) {
  const fits = (x) => mathWidth(x, size, weight) <= maxW;
  const levels = strong ? [strongBreak, canBreak, eqBreak, anyBreak] : [canBreak, eqBreak, anyBreak];
  const lines = [];
  const pack = (text, lv) => {
    const n = lines.length;
    if (n && fits(lines[n - 1] + " " + text)) { lines[n - 1] += " " + text; return; }
    if (fits(text) || lv >= levels.length) { lines.push(text); return; }
    const parts = chunksOf(text.split(" "), levels[lv]);
    if (parts.length === 1) { pack(text, lv + 1); return; }
    for (const p of parts) pack(p, lv + 1);
  };
  const str = String(s ?? "");
  if (!str) return [""];
  if (fits(str)) return [str];
  for (const p of chunksOf(str.split(" "), levels[0])) pack(p, 1);
  return lines.length ? lines : [""];
}

/* ══════════ 한 번 놓기 ══════════ */
/**
 * 글자 판을 한 번 놓는다. T 글자 크기 · R 판 · colR 판서 칸 오른쪽 끝.
 * 돌려주는 것: q(문제 줄) · plan(방침) · rows(판서 줄) · ans(답 칸) · boxes(차지한 네모 — 그림 자리 찾기) · bottom · over(넘친 너비)
 */
function layOnce(it, T, R, colR, split = 0) {
  const two = split > 0;
  const W0 = R.right - R.left;
  let L = R.left, CW = colR - L;
  let over = 0;
  const boxes = [];
  const wOf = (s, z, wt) => mathWidth(s, z, wt);
  // ① 문제 — 판 너비를 다 쓴다
  const qTxt = it.no === "" || it.no == null ? it.q : `${it.no}. ${it.q}`;   // 번호가 없으면(개념 설명의 움직이는 예시) 문제만
  const qParts = wrapMath(qTxt, T.q, W0, 560);
  let y = R.top;
  const q = qParts.map((s, i) => {
    y += i === 0 ? upOf(s, T.q) : Math.max(T.q * 1.4, dnOf(qParts[i - 1], T.q) + upOf(s, T.q) + T.q * 0.3);
    const w = wOf(s, T.q, 560);
    over = Math.max(over, w - W0);
    boxes.push([L, y - upOf(s, T.q), L + w, y + dnOf(s, T.q)]);
    return { s, x: L, y };
  });
  const qBottom = y + dnOf(qParts[qParts.length - 1], T.q);
  // ② 방침 — 꼬리표 + 글자(넘치면 꼬리표 오른쪽에서 이어 쓴다)
  const tag = it.planTag || "방침";
  const tagZ = Math.round(T.s * 0.95);
  const tagW = wOf(tag, tagZ, 800) + tagZ * 1.3;
  const planX = L + tagW + T.plan * 0.45;
  const planParts = it.plan ? wrapMath(it.plan, T.plan, Math.max(200, colR - planX), 620, true) : [];
  y = qBottom + T.q * 0.62;
  const planTop = y;
  const plan = planParts.map((s, i) => {
    y += i === 0 ? Math.max(upOf(s, T.plan), tagZ * 1.02) : Math.max(T.plan * 1.36, dnOf(planParts[i - 1], T.plan) + upOf(s, T.plan) + T.plan * 0.28);
    const w = wOf(s, T.plan, 620);
    over = Math.max(over, planX + w - colR);
    return { s, x: planX, y, w };
  });
  const planY = plan.length ? plan[0].y : y;
  const planBottom = plan.length ? y + dnOf(planParts[planParts.length - 1], T.plan) : y;
  if (plan.length) boxes.push([L, planTop, Math.max(L + tagW, ...plan.map((p) => p.x + p.w)), planBottom]);
  // ③ 판서 줄 — split 이 있으면 두 단(split 번째 줄부터 오른쪽 단 위에서 이어 쓴다 · 답은 마지막 줄 뒤)
  y = planBottom + T.b * 0.52;
  const solTop = y;
  const ind = T.b * 0.6;
  const half = (W0 - 56) / 2;
  let col = 0;
  const startCol = (k) => { col = k; L = R.left + k * (half + 56); colR = L + half; CW = half; };
  if (two) startCol(0);
  const layRow = (ln, i, y0) => {
    let y = y0;
    const r = { i, col, top: 0, bot: 0, parts: [], pre: null, memo: null, L, colR };
    let ov = 0;
    const preTxt = ln.pre ? ln.pre : null;
    const preW = preTxt ? wOf(preTxt + ":", T.s, 600) + T.s * 0.55 : 0;
    const s = ln.s ?? "";
    let x0 = L, first = true;
    if (preTxt) {
      const inline = preW + Math.min(wOf(s, T.b, 560), CW * 0.5) <= CW && preW <= CW * 0.42;
      if (!inline) {
        y += T.s * 0.82;
        r.pre = { s: preTxt, x: L, y, row: true };
        r.top = y - T.s * 0.82;
        y += T.s * 0.42;
        first = false;
      } else {
        r.pre = { s: preTxt + ":", x: L, y: null, row: false };
        x0 = L + preW;
      }
    }
    const parts = wrapMath(s, T.b, colR - x0, 560, true);
    let prevS = null;
    parts.forEach((p, k) => {
      const px = k === 0 ? x0 : (r.pre && !r.pre.row ? x0 : L + ind);
      if (k === 0 && first) y += upOf(p, T.b);
      else if (k === 0) y += upOf(p, T.b) + T.b * 0.12;
      else y += Math.max(T.b * 1.32, dnOf(prevS, T.b) + upOf(p, T.b) + T.b * 0.26);
      const w = wOf(p, T.b, 560);
      ov = Math.max(ov, px + w - colR);
      r.parts.push({ s: p, x: px, y, w });
      prevS = p;
    });
    if (!r.parts.length) { y += upOf("", T.b); r.parts.push({ s: "", x: x0, y, w: 0 }); prevS = ""; }
    if (r.pre && !r.pre.row) r.pre.y = r.parts[0].y;
    if (!r.top) r.top = r.parts[0].y - upOf(r.parts[0].s, T.b);
    let bot = y + dnOf(prevS, T.b);
    // 빨간 메모 — 마지막 조각 뒤에 들어가면 그 자리, 아니면 다음 줄(들여서)
    if (ln.memo) {
      const last = r.parts[r.parts.length - 1];
      const mw = wOf(ln.memo, T.s, 600);
      const mx = last.x + last.w + T.s * 0.9;
      if (mx + mw <= colR) r.memo = { lines: [{ s: ln.memo, x: mx, y: last.y, w: mw }], row: false };
      else {
        const mParts = wrapMath(ln.memo, T.s, colR - L - ind, 600);
        const ls = [];
        mParts.forEach((m, k) => {
          y = (k === 0 ? bot : y) + (k === 0 ? T.s * 1.02 : T.s * 1.3);
          const w = wOf(m, T.s, 600);
          ov = Math.max(ov, L + ind + w - colR);
          ls.push({ s: m, x: L + ind, y, w });
        });
        r.memo = { lines: ls, row: true };
        bot = y + T.s * 0.3;
      }
    }
    r.bot = bot;
    r.right = Math.max(...r.parts.map((p) => p.x + p.w), r.pre ? L + (r.pre.row ? wOf(r.pre.s, T.s, 600) : preW) : 0,
      ...(r.memo ? r.memo.lines.map((m) => m.x + m.w) : []));
    return { r, y: bot + T.b * 0.5, ov };
  };
  const rows = it.lines.map((ln, i) => {
    if (two && i === split) { startCol(1); y = solTop; }
    const got = layRow(ln, i, y);
    over = Math.max(over, got.ov);
    boxes.push([got.r.L, got.r.top, got.r.right, got.r.bot]);
    y = got.y;
    return got.r;
  });
  // ④ 답
  const ansFrac = hasFrac(it.ans) || matRows(it.ans) > 0;
  const ansUp = Math.max(T.b * 1.05, upOf(it.ans ?? "", T.b) + T.b * 0.22), ansDn = Math.max(T.b * 0.45, dnOf(it.ans ?? "", T.b) + T.b * 0.22);
  const ansH = ansFrac ? ansUp + ansDn : T.b * 1.5;
  const ansTop = y + T.b * 0.12;
  const ansY = ansTop + (ansFrac ? ansUp : T.b * 1.05);
  const ansW = wOf(it.ans ?? "", T.b, 700) + T.b * 2.6;
  boxes.push([L - 8, ansTop, L - 8 + ansW, ansTop + ansH]);
  over = Math.max(over, L - 8 + ansW - (two ? colR : R.right));
  const ans = { x: L, y: ansY, top: ansTop, h: ansH, w: ansW };
  const bottom = Math.max(ansTop + ansH, ...rows.map((r) => r.bot));
  return { T, R, colR: two ? R.right : colR, q, qBottom, tag, tagZ, tagW, planTop, planY, planBottom, plan, rows, ans, boxes, bottom, over,
    two: two ? { x: R.left + half + 28, top: solTop - T.b * 0.3 } : null };
}

/* ══════════ 그림 자리 ══════════ */
/** 그림 배율 상한 — 화면(단일: 무대 1600 × 900 · 듀얼: 반쪽 800 × 900) 넓이의 FIG_AREA 를 넘지 않게, 제 크기보다 크게는 안 */
const screenOf = (R) => (R.key === "pane" ? PANE_W * PANE_H : STAGE_W * STAGE_H);
const figCap = (fig, R) => Math.min(1, Math.sqrt((FIG_AREA * screenOf(R)) / (fig.w * fig.h)));
/**
 * 글자 판 옆 빈 칸 중 그림이 가장 크게 들어가는 곳.
 *   fig = { w, h }             — 제 크기가 정해진 그림: 배율 s 로 줄여 넣는다(s ≤ 1, FIG_MIN 아래면 뺀다)
 *   fig = { flex, minW, minH, maxW, maxH } — 받은 칸에 맞춰 스스로 그리는 그림(좌표평면 — 글자 크기는 그대로)
 * 돌려주는 것: { x, y, w, h, s, room } — 그림을 놓을 네모 · 없으면 null
 */
function figSpot(lay, fig, R) {
  if (!fig) return null;
  const top0 = lay.qBottom + 18, bot0 = R.bottom;
  const els = lay.boxes.filter((b) => b[3] > top0);
  const ys0 = [top0, ...els.map((b) => b[3] + 16)].filter((v) => v < bot0 - 120);
  const ys1 = [bot0, ...els.map((b) => b[1] - 16)].filter((v) => v > top0 + 120);
  const capA = FIG_AREA * screenOf(R);
  const cap = fig.flex ? 1 : figCap(fig, R);
  let best = null;
  for (const y0 of ys0) for (const y1 of ys1) {
    if (y1 - y0 < 120) continue;
    const xr = Math.max(R.left - GAP_FIG, ...els.filter((b) => b[3] > y0 && b[1] < y1).map((b) => b[2]));
    const x0 = xr + GAP_FIG, w = R.right - x0, h = y1 - y0;
    if (w < 120) continue;
    let c;
    if (fig.flex) {
      let bw = Math.min(w, fig.maxW), bh = Math.min(h, fig.maxH);
      if (bw < fig.minW || bh < fig.minH) continue;
      if (bw * bh > capA) {                      // 넓이 상한 — 긴 쪽부터 줄인다
        const f = Math.sqrt(capA / (bw * bh));
        bw = Math.max(fig.minW, bw * f); bh = Math.max(fig.minH, Math.min(bh, capA / bw));
      }
      c = { s: 1, a: bw * bh, bw, bh };
    } else {
      const s = Math.min(cap, w / fig.w, h / fig.h);
      c = { s, a: s * s * fig.w * fig.h, bw: fig.w * s, bh: fig.h * s };
    }
    if (!best || c.a > best.a + 1 || (Math.abs(c.a - best.a) <= 1 && w * h > best.w0 * best.h0)) best = { ...c, x0, y0, w0: w, h0: h };
  }
  if (!best || (!fig.flex && best.s < FIG_MIN)) return null;
  // R.figTop — 남은 칸의 위에 붙인다(개념 설명의 움직이는 예시: 판을 그림 아래에서 잘라 쓰므로 가운데에 띄우지 않는다)
  return { x: best.x0 + (best.w0 - best.bw) / 2, y: R.figTop ? best.y0 + 6 : best.y0 + (best.h0 - best.bh) / 2, w: best.bw, h: best.bh, s: best.s,
    room: [best.x0, best.y0, best.x0 + best.w0, best.y0 + best.h0] };
}

/**
 * 꼭 보여야 하는 그림(fig.must — 사전식 카드로 순번 찾기처럼 그림이 풀이의 몸통인 것) — 남은 빈자리가 모자라면 자리를 먼저 떼어 둔다.
 *   넓은 판(무대): 글자 칸 오른쪽에 그림 칸(글자 칸은 넘치면 흐른다).
 *   좁은 판(듀얼 반쪽): 아래에 그림 칸, 위 글자 칸이 흐른다.
 */
function mustLayout(it, R, fig) {
  const W0 = R.right - R.left;
  const capA = FIG_AREA * screenOf(R);
  const last = BOARD_TYPE[BOARD_TYPE.length - 1];
  const fit = (w, h) => {                      // 칸 넓이 상한(화면의 25%) — 높이부터 줄인다
    let bw = Math.min(w, fig.maxW), bh = Math.min(h, fig.maxH);
    if (bw * bh > capA) bh = Math.max(fig.minH, capA / bw);
    if (bw * bh > capA) bw = Math.max(fig.minW, capA / bh);
    return [bw, bh];
  };
  const sideW = Math.min(fig.maxW, Math.max(fig.minW, W0 * 0.42));
  const colR = R.right - sideW - GAP_FIG;
  if (colR - R.left >= 520) {
    const pick = (lay, T, scroll) => {
      const x0 = colR + GAP_FIG, y0 = lay.qBottom + 18;
      const [w, h] = fit(R.right - x0, R.bottom - y0);
      const spot = { x: x0 + (R.right - x0 - w) / 2, y: y0 + (R.bottom - y0 - h) / 2, w, h, s: 1, room: [x0, y0, R.right, R.bottom] };
      return { ...lay, type: T.key, fig: spot, scroll };
    };
    for (const T of BOARD_TYPE) {
      const lay = layOnce(it, T, R, colR);
      if (lay.over <= 2 && lay.bottom <= R.bottom) return pick(lay, T, null);
    }
    const lay = layOnce(it, last, R, colR);
    if (lay.over <= 2) return pick(lay, last, { top: lay.qBottom + last.q * 0.3, bottom: R.bottom + 2, pinQ: true });
    return null;
  }
  // 좁은 판 — 그림은 아래, 글자는 위에서 흐른다
  for (const T of [...BOARD_TYPE].reverse()) {
    const lay = layOnce(it, T, R, R.right);
    if (lay.over > 2) continue;
    const [w, h] = fit(W0, fig.minH);
    const figTop = R.bottom - h;
    if (figTop - lay.qBottom < 110) return null;               // 글자 칸이 두 줄도 못 되면 그림을 접는다
    const spot = { x: R.left + (W0 - w) / 2, y: figTop, w, h, s: 1, room: [R.left, figTop, R.right, R.bottom] };
    const scroll = lay.bottom > figTop - 16 ? { top: lay.qBottom + T.q * 0.3, bottom: figTop - 16, pinQ: true } : null;
    return { ...lay, type: T.key, fig: spot, scroll };
  }
  return null;
}

/* ══════════ 배치 ══════════ */
const CACHE = new WeakMap();
/**
 * 문항 하나의 글자 판 배치. region — 판(STAGE_REGION · PANE_REGION). fig — 그림 제 크기 { w, h } 또는 null.
 *   글자가 다 들어가는 크기(기본 → 촘촘)를 먼저 정하고, 그 크기에서 그림이 가장 크게 들어가는 판서 칸 너비를 고른다.
 *   돌려주는 것: layOnce 의 것 + type(base | tight) · fig(그림 자리 — 없으면 null) · scroll(넘쳐서 흐르면 { top, bottom })
 */
export function boardLayout(it, region = STAGE_REGION, fig = null) {
  let m = CACHE.get(it);
  if (!m) { m = new Map(); CACHE.set(it, m); }
  const key = `${region.key}|${fig ? (fig.flex ? `flex${fig.minW}x${fig.minH}${fig.must ? "!" : ""}` : `${Math.round(fig.w)}x${Math.round(fig.h)}`) : "-"}`;
  if (m.has(key)) return m.get(key);
  const R = region, W0 = R.right - R.left;
  const fitsH = (lay) => lay.bottom <= R.bottom && lay.over <= 2;
  let out = null;
  for (const T of BOARD_TYPE) {
    const full = layOnce(it, T, R, R.right);
    if (!fitsH(full)) continue;
    // 이 크기로 글자가 다 들어간다 — 그림 자리를 찾는다(넓은 판서 칸부터)
    let pick = { lay: full, spot: null };
    if (fig) {
      const enough = 0.97 * (fig.flex ? Math.min(FIG_AREA * screenOf(R), fig.maxW * fig.maxH) : figCap(fig, R) ** 2 * fig.w * fig.h);
      let bestA = -1;
      for (const c of COLS) {
        const colR = R.left + W0 * c;
        const lay = c === 1 ? full : layOnce(it, T, R, colR);
        if (!fitsH(lay)) continue;
        const spot = figSpot(lay, fig, R);
        if (!spot) continue;
        const a = spot.w * spot.h;
        if (a > bestA * 1.04) { bestA = a; pick = { lay, spot }; }
        if (a >= enough) break;                    // 넉넉히 들어갔다 — 더 좁힐 까닭이 없다
      }
    }
    out = { ...pick.lay, type: T.key, fig: pick.spot, scroll: null };
    break;
  }
  // 꼭 보여야 하는 그림인데 자리를 못 찾았으면 — 그림 칸을 먼저 떼어 둔다
  if (fig?.must && !(out && out.fig)) {
    const m2 = mustLayout(it, R, fig);
    if (m2) out = m2;
  }
  // 한 단으로 넘치면 — 무대(넓은 판)는 두 단으로(칠판처럼 왼쪽 단을 채울 만큼 채우고 나머지 줄 · 답은 오른쪽 단 위에서)
  if (!out && R.key === "stage" && it.lines.length >= 2) {
    for (const T of BOARD_TYPE) {
      for (let k = it.lines.length - 1; k >= 1 && !out; k--) {
        const lay = layOnce(it, T, R, R.right, k);
        if (fitsH(lay)) out = { ...lay, type: T.key, fig: null, scroll: null };
      }
      if (out) break;
    }
  }
  if (!out) {
    // 그래도 넘친다 — 판서가 위로 흐른다(문제는 붙여 두고)
    const T = BOARD_TYPE[BOARD_TYPE.length - 1];
    const lay = layOnce(it, T, R, R.right);
    const pinQ = lay.qBottom - R.top <= (R.bottom - R.top) * 0.42;
    out = { ...lay, type: T.key, fig: null, scroll: { top: pinQ ? lay.qBottom + T.q * 0.3 : R.top - T.q * 0.2, bottom: R.bottom + 2, pinQ } };
  }
  m.set(key, out);
  return out;
}

/**
 * 흐르는 판의 위치(t — 1배속 ms): 판서 줄 · 답이 나타날 때마다 그 줄 아래가 판 안에 들도록 부드럽게 올린다.
 *   P = 박자표(lines[i].a · ans). 넘치지 않는 판이면 0.
 */
export function boardScroll(Lo, P, t) {
  if (!Lo.scroll) return 0;
  const lim = Lo.scroll.bottom - 10;
  const need = (bot) => Math.max(0, bot - lim);
  const evs = [...Lo.rows.map((r, i) => [P.lines[i].a, need(r.bot)]), [P.ans, need(Lo.bottom)]];
  let off = 0;
  for (const [ta, v] of evs) {
    if (v <= off) continue;
    const k = seg(t, ta - 150, ta + 550, E.sine);
    if (k <= 0) break;
    off += (v - off) * k;
    if (k < 1) break;
  }
  return off;
}
