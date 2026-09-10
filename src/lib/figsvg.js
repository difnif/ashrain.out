// ashrain.out — 문항 도형 렌더러 (figsvg.js, v1.0 / SPEC-도형렌더러 §2 구현)
// 위치: src/lib/figsvg.js
//
// 원칙
//   · 순수 함수 — React·DOM 의존 없음. Node에서 그대로 시험 가능(tools/figcheck.mjs).
//   · 관대한 입력 / 엄격한 출력 — 코퍼스의 느슨한 인자를 정규화해서 받고,
//     그릴 수 없으면 예외나 빈 그림이 아니라 "설명 상자"로 떨어진다(원칙 P3 오류보다 침묵).
//   · 색은 currentColor 기반 — 라이트/다크 어느 쪽에서도 살아남는다. 강조색만 accent.
//
// 사용
//   import { figureToHtml } from "./figsvg.js";
//   el.innerHTML = figureToHtml(item.figure, { width: 320 });

import { parse, ev, disp, renderHtml } from "./mathir.js";

// ---------------------------------------------------------------- 상수·유틸
const NS = 'xmlns="http://www.w3.org/2000/svg"';
const DEF = {
  width: 320, pad: 14, accent: "#d1495b", grid: 0.18, faint: 0.35,
  font: 12, debug: false,
};

export function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

const R2 = (n) => (Math.round(n * 100) / 100);

// ---------------------------------------------------------------- 정규화 계층
const UNIT_RE = /\s*(cm|mm|m|km|kg|g|초|분|시간|도|°|개|명|점|원|%)\s*$/;

/** 숫자화: 숫자 → 그대로 / 문자열 → 숫자 → MathIR 평가 → 실패시 null */
export function num(v, env = {}) {
  if (v == null || v === "") return null;
  if (typeof v === "number") return Number.isFinite(v) ? v : null;
  if (typeof v === "boolean") return null;
  if (Array.isArray(v)) return null;
  if (typeof v === "object") {
    for (const k of ["value", "val", "n", "len", "length", "measure"]) {
      if (k in v) return num(v[k], env);
    }
    return null;
  }
  let s = String(v).trim();
  if (!s) return null;
  s = s.replace(/^\[\[([\s\S]*)\]\]$/, "$1").trim();   // [[ ]] 마커 탈피
  s = s.replace(UNIT_RE, "");                          // 꼬리 단위 제거
  s = s.replace(/[−–—]/g, "-");                        // 유니코드 마이너스
  if (/^-?\d+(\.\d+)?$/.test(s)) return parseFloat(s);
  if (/^-?\d+\/\d+$/.test(s)) { const [a, b] = s.split("/").map(Number); return b ? a / b : null; }
  try {
    const [node] = parse(s);
    const r = ev(node, env);
    const x = (r && typeof r.toNumber === "function") ? r.toNumber() : r;
    return (typeof x === "number" && Number.isFinite(x)) ? x : null;
  } catch { return null; }
}

/** 범위: "[-3, 3]" | [-3,3] | "0, 35" | {min,max} | "-3~3" → [lo, hi] */
export function rng(v, env = {}) {
  if (v == null) return null;
  if (Array.isArray(v)) {
    const a = num(v[0], env), b = num(v[1], env);
    return (a == null || b == null) ? null : (a <= b ? [a, b] : [b, a]);
  }
  if (typeof v === "object") {
    const a = num(v.min ?? v.lo ?? v.from ?? v.start, env);
    const b = num(v.max ?? v.hi ?? v.to ?? v.end, env);
    return (a == null || b == null) ? null : [Math.min(a, b), Math.max(a, b)];
  }
  const s = String(v).trim().replace(/^\[|\]$/g, "");
  const parts = s.split(/\s*[,~]\s*/).filter((p) => p !== "");
  if (parts.length === 2) {
    const a = num(parts[0], env), b = num(parts[1], env);
    if (a != null && b != null) return [Math.min(a, b), Math.max(a, b)];
  }
  const one = num(v, env);
  return one == null ? null : [0, one];
}

/** 좌표: [x,y] | "[0,5]" | {x,y} | {coord} | "point(0,2)" → [x, y] */
export function pt(v, env = {}) {
  if (v == null) return null;
  if (Array.isArray(v)) {
    const a = num(v[0], env), b = num(v[1], env);
    return (a == null || b == null) ? null : [a, b];
  }
  if (typeof v === "object") {
    if ("coord" in v) return pt(v.coord, env);
    if ("pos" in v && !("y" in v)) { const a = num(v.pos, env); return a == null ? null : [a, 0]; }
    const a = num(v.x ?? v.X, env), b = num(v.y ?? v.Y, env);
    return (a == null || b == null) ? null : [a, b];
  }
  const s = String(v).trim();
  const m = s.match(/^point3?\s*\(([^)]*)\)$/i);
  if (m) return pt(m[1].split(",").map((t) => t.trim()), env);
  return pt(s.replace(/^\[|\]$/g, "").split(","), env);
}

/** 수직선 위 위치: {x|pos|coord|value|at} 또는 순수 숫자 */
function pos1(o, env = {}) {
  if (o == null) return null;
  if (typeof o !== "object" || Array.isArray(o)) return num(o, env);
  for (const k of ["x", "pos", "coord", "value", "at", "v"]) if (k in o) { const n = num(o[k], env); if (n != null) return n; }
  return null;
}

/** 라벨: MathIR 마커·식이면 표시형으로, 아니면 원문 */
export function lab(v) {
  if (v == null) return "";
  if (typeof v === "object") return lab(v.label ?? v.name ?? v.text ?? "");
  let s = String(v).trim();
  if (!s) return "";
  const m = s.match(/^\[\[([\s\S]*)\]\]$/);
  if (m) { try { const [n] = parse(m[1].trim()); return disp(n); } catch { return m[1].trim(); } }
  if (/^[A-Za-z0-9_^{}().,+\-*/ ]+$/.test(s) && /[(^_]/.test(s)) {
    try { const [n] = parse(s); return disp(n); } catch { /* 그대로 */ }
  }
  return s;
}

const arr = (v) => (Array.isArray(v) ? v : v == null ? [] : [v]);
const isNum = (n) => typeof n === "number" && Number.isFinite(n);

// ---------------------------------------------------------------- SVG 프리미티브
function svgOpen(w, h, o) {
  return `<svg ${NS} viewBox="0 0 ${R2(w)} ${R2(h)}" width="${R2(w)}" height="${R2(h)}" `
       + `role="img" style="max-width:100%;height:auto;color:inherit;overflow:visible" `
       + `font-family="system-ui,-apple-system,'Malgun Gothic',sans-serif" font-size="${o.font}">`;
}
const K = (a) => (a && a.k ? ` data-k="${esc(a.k)}"` : "");
const L = (x1, y1, x2, y2, a = {}) =>
  `<line${K(a)} x1="${R2(x1)}" y1="${R2(y1)}" x2="${R2(x2)}" y2="${R2(y2)}" stroke="${a.stroke || "currentColor"}" `
  + `stroke-width="${a.w || 1.2}" ${a.dash ? `stroke-dasharray="${a.dash}"` : ""} `
  + `${a.op ? `opacity="${a.op}"` : ""} stroke-linecap="round"/>`;
const C = (cx, cy, r, a = {}) =>
  `<circle${K(a)} cx="${R2(cx)}" cy="${R2(cy)}" r="${R2(r)}" fill="${a.fill || "none"}" `
  + `stroke="${a.stroke || "currentColor"}" stroke-width="${a.w ?? 1.2}" ${a.op ? `opacity="${a.op}"` : ""}/>`;
const PATH = (d, a = {}) =>
  `<path${K(a)} d="${d}" fill="${a.fill || "none"}" stroke="${a.stroke || "currentColor"}" `
  + `stroke-width="${a.w ?? 1.2}" ${a.dash ? `stroke-dasharray="${a.dash}"` : ""} `
  + `${a.op ? `opacity="${a.op}"` : ""} stroke-linejoin="round"/>`;
const POLY = (pts, a = {}) =>
  `<polygon${K(a)} points="${pts.map(([x, y]) => `${R2(x)},${R2(y)}`).join(" ")}" fill="${a.fill || "none"}" `
  + `stroke="${a.stroke || "currentColor"}" stroke-width="${a.w ?? 1.2}" `
  + `${a.dash ? `stroke-dasharray="${a.dash}"` : ""} ${a.op ? `opacity="${a.op}"` : ""} stroke-linejoin="round"/>`;
const T = (x, y, s, a = {}) =>
  `<text${K(a)} x="${R2(x)}" y="${R2(y)}" text-anchor="${a.anchor || "middle"}" `
  + `dominant-baseline="${a.base || "auto"}" fill="${a.fill || "currentColor"}" `
  + `font-size="${a.size || "inherit"}" ${a.op ? `opacity="${a.op}"` : ""}>${esc(s)}</text>`;
const DOT = (x, y, a = {}) => C(x, y, a.r || 2.6, { fill: a.fill || "currentColor", stroke: a.stroke || "currentColor", w: 1, k: a.k });

/** 그릴 수 없을 때의 설명 상자 — 빈 그림 대신 항상 이것 */
function note(text, why) {
  const body = String(text || "").trim();
  return `<div class="fig-note" style="border:1px dashed currentColor;border-radius:8px;padding:8px 10px;`
       + `opacity:.75;font-size:13px;line-height:1.5;white-space:pre-wrap">`
       + (body ? esc(body) : `<em>도형 설명 없음</em>`)
       + (why ? `<div style="opacity:.6;font-size:11px;margin-top:4px">${esc(why)}</div>` : "")
       + `</div>`;
}

// ---------------------------------------------------------------- 좌표 프레임
function frame(xr, yr, o, opts = {}) {
  const W = o.width, pad = o.pad + (opts.padExtra || 0);
  let [xlo, xhi] = xr, [ylo, yhi] = yr;
  if (xhi - xlo < 1e-9) { xlo -= 1; xhi += 1; }
  if (yhi - ylo < 1e-9) { ylo -= 1; yhi += 1; }
  const aspect = opts.aspect ?? ((yhi - ylo) / (xhi - xlo));
  let H = (W - 2 * pad) * Math.max(0.35, Math.min(1.6, aspect)) + 2 * pad;
  H = Math.max(90, Math.min(360, H));
  const X = (x) => pad + (x - xlo) / (xhi - xlo) * (W - 2 * pad);
  const Y = (y) => H - pad - (y - ylo) / (yhi - ylo) * (H - 2 * pad);
  return { W, H, X, Y, xlo, xhi, ylo, yhi, pad };
}

function axes(f, o, { grid = true, ticks = true } = {}) {
  let s = "";
  const step = (lo, hi) => {
    const raw = (hi - lo) / 8, p = Math.pow(10, Math.floor(Math.log10(raw || 1)));
    const c = [1, 2, 2.5, 5, 10].map((k) => k * p).find((k) => k >= raw) || p * 10;
    return c;
  };
  const sx = step(f.xlo, f.xhi), sy = step(f.ylo, f.yhi);
  if (grid) {
    for (let x = Math.ceil(f.xlo / sx) * sx; x <= f.xhi + 1e-9; x += sx)
      s += L(f.X(x), f.Y(f.ylo), f.X(x), f.Y(f.yhi), { w: 0.6, op: o.grid });
    for (let y = Math.ceil(f.ylo / sy) * sy; y <= f.yhi + 1e-9; y += sy)
      s += L(f.X(f.xlo), f.Y(y), f.X(f.xhi), f.Y(y), { w: 0.6, op: o.grid });
  }
  const y0 = Math.min(Math.max(0, f.ylo), f.yhi), x0 = Math.min(Math.max(0, f.xlo), f.xhi);
  s += L(f.X(f.xlo), f.Y(y0), f.X(f.xhi), f.Y(y0), { w: 1.1 });
  s += L(f.X(x0), f.Y(f.ylo), f.X(x0), f.Y(f.yhi), { w: 1.1 });
  s += T(f.X(f.xhi) + 6, f.Y(y0) + 4, "x", { anchor: "start", op: 0.7 });
  s += T(f.X(x0) - 4, f.Y(f.yhi) - 4, "y", { anchor: "end", op: 0.7 });
  if (ticks) {
    for (let x = Math.ceil(f.xlo / sx) * sx; x <= f.xhi + 1e-9; x += sx) {
      if (Math.abs(x) < 1e-9) continue;
      s += L(f.X(x), f.Y(y0) - 3, f.X(x), f.Y(y0) + 3, { w: 1 });
      s += T(f.X(x), f.Y(y0) + 14, R2(x), { op: 0.65, size: 10 });
    }
    for (let y = Math.ceil(f.ylo / sy) * sy; y <= f.yhi + 1e-9; y += sy) {
      if (Math.abs(y) < 1e-9) continue;
      s += L(f.X(x0) - 3, f.Y(y), f.X(x0) + 3, f.Y(y), { w: 1 });
      s += T(f.X(x0) - 6, f.Y(y) + 3.5, R2(y), { anchor: "end", op: 0.65, size: 10 });
    }
    s += T(f.X(x0) - 6, f.Y(y0) + 14, "O", { anchor: "end", op: 0.65, size: 10 });
  }
  return s;
}

/** 관계식/함수식을 표본 평가해 폴리라인으로 — y=f(x), f(x), 음함수 x는 격자 스캔 */
function sampleCurve(expr, f, env = {}) {
  let src = String(expr || "").trim();
  if (!src) return null;
  src = src.replace(/^y\s*=\s*/i, "").replace(/^f\s*\(\s*x\s*\)\s*=\s*/i, "");
  if (/[=<>]/.test(src)) return null;                       // 남은 관계식은 미지원
  let node;
  try { [node] = parse(src); } catch { return null; }
  const N = 240, segs = [];
  let cur = [];
  for (let i = 0; i <= N; i++) {
    const x = f.xlo + (f.xhi - f.xlo) * i / N;
    let y = null;
    try {
      const r = ev(node, { ...env, x });
      y = (r && typeof r.toNumber === "function") ? r.toNumber() : r;
    } catch { y = null; }
    if (!isNum(y) || y < f.ylo - (f.yhi - f.ylo) * 2 || y > f.yhi + (f.yhi - f.ylo) * 2) {
      if (cur.length > 1) segs.push(cur);
      cur = [];
      continue;
    }
    cur.push([f.X(x), f.Y(Math.max(f.ylo - 0.02 * (f.yhi - f.ylo), Math.min(f.yhi + 0.02 * (f.yhi - f.ylo), y)))]);
  }
  if (cur.length > 1) segs.push(cur);
  if (!segs.length) return null;
  return segs.map((s) => "M" + s.map(([x, y]) => `${R2(x)} ${R2(y)}`).join(" L")).join(" ");
}

// ---------------------------------------------------------------- numline
function fnNumline(a, o) {
  let r = rng({ min: a.min, max: a.max }, {});
  const pts = arr(a.points).map((p) => ({ v: pos1(p, {}), t: lab(p && p.label != null ? p.label : p) }))
                           .filter((p) => p.v != null);
  if (!r) {
    const vs = pts.map((p) => p.v);
    if (!vs.length) return null;
    r = [Math.min(...vs) - 1, Math.max(...vs) + 1];
  }
  let [lo, hi] = r;
  for (const p of pts) { lo = Math.min(lo, p.v); hi = Math.max(hi, p.v); }
  if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
  const W = o.width, H = 74, pad = o.pad + 12;
  const X = (x) => pad + (x - lo) / (hi - lo) * (W - 2 * pad), y0 = 44;
  let s = svgOpen(W, H, o);
  s += L(pad - 10, y0, W - pad + 10, y0, { w: 1.3 });
  s += PATH(`M${W - pad + 10} ${y0} l-7 -3.5 v7 z`, { fill: "currentColor", w: 0 });
  s += PATH(`M${pad - 10} ${y0} l7 -3.5 v7 z`, { fill: "currentColor", w: 0 });
  const st = Math.max(1, Math.round((hi - lo) / 12));
  for (let v = Math.ceil(lo); v <= hi + 1e-9; v += st) {
    s += L(X(v), y0 - 4, X(v), y0 + 4, { w: 1, op: 0.75 });
    s += T(X(v), y0 + 17, R2(v), { op: 0.6, size: 10 });
  }
  // 구간(음영)
  const segsIn = [];
  for (const k of ["segments", "segment", "interval", "shaded", "highlight"]) {
    for (const g of arr(a[k])) {
      if (g == null) continue;
      const rr = Array.isArray(g) ? rng(g, {}) : rng({ min: g.start ?? g.from ?? g.min ?? g[0], max: g.end ?? g.to ?? g.max ?? g[1] }, {});
      if (rr) segsIn.push({ r: rr, inc: g && g.inclusive !== false });
    }
  }
  segsIn.forEach((g, gi) => {
    s += L(X(g.r[0]), y0, X(g.r[1]), y0, { w: 4, stroke: o.accent, op: 0.85, k: `seg:${gi}` });
    for (const e of g.r) s += C(X(e), y0, 3.4, { fill: g.inc ? o.accent : "var(--fig-bg,#fff)", stroke: o.accent, w: 1.4 });
  });
  for (const p of pts) {
    s += DOT(X(p.v), y0, { r: 3, k: `pt:${p.t || p.v}` });
    if (p.t) s += T(X(p.v), y0 - 10, p.t, { size: 11, k: `lbl:${p.t}` });
  }
  return s + "</svg>";
}

// ---------------------------------------------------------------- coordplane
function fnCoordplane(a, o) {
  const xr = rng(a.x ?? a.x_range ?? a.xrange, {}) || [-5, 5];
  const yr = rng(a.y ?? a.y_range ?? a.yrange, {}) || [-5, 5];
  const named = {};
  const pts = [];
  for (const p of arr(a.points)) {
    if (typeof p === "string") {
      const m = p.match(/^point\s*\(([^)]*)\)$/i);
      const c = pt(m ? m[1].split(",") : p, {});
      if (c) pts.push({ c, t: "" });
      continue;
    }
    const c = pt(p, {});
    const nm = lab(p && (p.name ?? p.label));
    if (c) { pts.push({ c, t: nm }); if (nm) named[nm] = c; }
  }
  const hasCircle = arr(a.circles).length > 0 || arr(a.lines).some((l) => typeof l === "string" && /^circle\s*\(/i.test(l));
  const f = frame(xr, yr, o, { aspect: hasCircle ? (yr[1] - yr[0]) / (xr[1] - xr[0]) : 0.78 });
  let s = svgOpen(f.W, f.H, o) + axes(f, o, { grid: true });
  const drawSeg = (p, q, at = {}) => L(f.X(p[0]), f.Y(p[1]), f.X(q[0]), f.Y(q[1]), { stroke: o.accent, w: 1.5, ...at });
  const lineLike = [...arr(a.lines), ...arr(a.curves), ...arr(a.asymptotes)];
  for (const ln of lineLike) {
    if (ln == null) continue;
    if (typeof ln === "string") {
      const cm = ln.match(/^circle\s*\(([^)]*)\)$/i);
      if (cm) {
        const parts = cm[1].split(",").map((t) => num(t, {}));
        const rr = parts.length >= 3 ? parts[2] : parts[0];
        const cx = parts.length >= 3 ? parts[0] : 0, cy = parts.length >= 3 ? parts[1] : 0;
        if (isNum(rr)) s += C(f.X(cx), f.Y(cy), Math.abs(f.X(cx + rr) - f.X(cx)), { stroke: o.accent, w: 1.5 });
        continue;
      }
      const d = sampleCurve(ln, f); if (d) s += PATH(d, { stroke: o.accent, w: 1.5 });
      continue;
    }
    const ps = arr(ln.points).map((p) => (typeof p === "string" && named[p]) ? named[p] : pt(p, {})).filter(Boolean);
    const lk = `line:${lineLike.indexOf(ln)}`;
    if (ps.length >= 2) {
      for (let i = 0; i < ps.length - 1; i++) s += drawSeg(ps[i], ps[i + 1], ln.style === "dashed" ? { dash: "4 3", k: lk } : { k: lk });
      if (ln.label) s += T(f.X((ps[0][0] + ps[ps.length - 1][0]) / 2), f.Y((ps[0][1] + ps[ps.length - 1][1]) / 2) - 5, lab(ln.label), { size: 11, fill: o.accent });
      continue;
    }
    const d = sampleCurve(ln.expr ?? ln.eq ?? ln.equation, f);
    if (d) { s += PATH(d, { stroke: o.accent, w: 1.5, dash: ln.style === "dashed" ? "4 3" : null, k: lk }); continue; }
  }
  for (const g of [...arr(a.circles)]) {
    const c = pt(g.center ?? g.c ?? [0, 0], {}), rr = num(g.r ?? g.radius, {});
    if (c && isNum(rr)) s += C(f.X(c[0]), f.Y(c[1]), Math.abs(f.X(c[0] + rr) - f.X(c[0])), { stroke: o.accent, w: 1.4 });
  }
  for (const p of pts) {
    s += DOT(f.X(p.c[0]), f.Y(p.c[1]), { r: 3, fill: o.accent, stroke: o.accent, k: p.t ? `pt:${p.t}` : null });
    if (p.t) s += T(f.X(p.c[0]) + 6, f.Y(p.c[1]) - 6, p.t, { anchor: "start", size: 11, k: `lbl:${p.t}` });
  }
  // 기울기 삼각형 — rise_run: ["A","B"] (이름) 또는 [[x1,y1],[x2,y2]]
  if (a.rise_run) {
    const [pa, pb] = arr(a.rise_run);
    const A = typeof pa === "string" ? named[pa] : pt(pa, {}), B = typeof pb === "string" ? named[pb] : pt(pb, {});
    if (A && B) {
      const Cx = [B[0], A[1]];
      s += L(f.X(A[0]), f.Y(A[1]), f.X(Cx[0]), f.Y(Cx[1]), { w: 1.3, dash: "4 3", stroke: o.accent, k: "run" });
      s += L(f.X(Cx[0]), f.Y(Cx[1]), f.X(B[0]), f.Y(B[1]), { w: 1.3, dash: "4 3", stroke: o.accent, k: "rise" });
      const rl = lab(a.run_label ?? `${R2(B[0] - A[0])}`), hl = lab(a.rise_label ?? `${R2(B[1] - A[1])}`);
      s += T((f.X(A[0]) + f.X(Cx[0])) / 2, f.Y(A[1]) + (B[1] >= A[1] ? 14 : -6), rl, { size: 10.5, fill: o.accent, k: "run-lbl" });
      s += T(f.X(Cx[0]) + (B[0] >= A[0] ? 8 : -8), (f.Y(Cx[1]) + f.Y(B[1])) / 2 + 4, hl, { size: 10.5, fill: o.accent, anchor: B[0] >= A[0] ? "start" : "end", k: "rise-lbl" });
    }
  }
  return s + "</svg>";
}

// ---------------------------------------------------------------- funcgraph
function fnFuncgraph(a, o) {
  const expr = a.expr ?? a.equation;
  const xr = rng(a.domain ?? a.x_range ?? a.xrange, {}) || [-5, 5];
  let yr = rng(a.y_range ?? a.yrange, {});
  const f0 = frame(xr, yr || [-5, 5], o, { aspect: 0.78 });
  if (!yr) {                                   // y 범위 자동 — 표본 분위수
    const ys = [];
    try {
      const [node] = parse(String(expr).replace(/^y\s*=\s*/i, ""));
      for (let i = 0; i <= 120; i++) {
        const x = xr[0] + (xr[1] - xr[0]) * i / 120;
        try { const r = ev(node, { x }); const y = r && r.toNumber ? r.toNumber() : r; if (isNum(y)) ys.push(y); } catch { /* skip */ }
      }
    } catch { /* skip */ }
    if (ys.length > 4) {
      ys.sort((p, q) => p - q);
      const lo = ys[Math.floor(ys.length * 0.05)], hi = ys[Math.floor(ys.length * 0.95)];
      const m = Math.max(1e-6, (hi - lo) * 0.15);
      yr = [Math.min(0, lo - m), Math.max(0, hi + m)];
    } else yr = [-5, 5];
  }
  const f = frame(xr, yr, o, { aspect: 0.78 });
  const d = sampleCurve(expr, f);
  if (!d) return null;
  let s = svgOpen(f.W, f.H, o) + axes(f, o, { grid: true }) + PATH(d, { stroke: o.accent, w: 1.7 });
  for (const p of arr(a.points)) {
    const c = pt(p, {}); if (!c) continue;
    s += DOT(f.X(c[0]), f.Y(c[1]), { r: 3, fill: o.accent, stroke: o.accent });
    const t = lab(p && (p.name ?? p.label)); if (t) s += T(f.X(c[0]) + 6, f.Y(c[1]) - 6, t, { anchor: "start", size: 11 });
  }
  return s + "</svg>";
}

// ---------------------------------------------------------------- scene (생성 문항 표준 기하)
// args: { pts:{A:[x,y],…}, segs:[["A","B"]|{a,b,dash,label}], circles:[{c,r,dash}],
//         marks:{ right:[["A","B","C"]], eq:[[["A","B"],["C","D"]]], arc:[{at,from,to,label}] },
//         shade:[["A","B","C"]], labels:[{at,text,dx,dy}], axes:false }
function fnScene(a, o) {
  const P = {};
  for (const [k, v] of Object.entries(a.pts || a.points || {})) { const c = pt(v, {}); if (c) P[k] = c; }
  const keys = Object.keys(P);
  if (!keys.length) return null;
  const seg = arr(a.segs).map((s) => (Array.isArray(s) ? { a: s[0], b: s[1] } : s)).filter((s) => s && P[s.a] && P[s.b]);
  const cir = arr(a.circles).map((c) => ({ c: (typeof c.c === "string" ? P[c.c] : pt(c.c, {})) || [0, 0], r: num(c.r, {}), dash: c.dash })).filter((c) => isNum(c.r));
  let xs = keys.map((k) => P[k][0]), ys = keys.map((k) => P[k][1]);
  for (const c of cir) { xs.push(c.c[0] - c.r, c.c[0] + c.r); ys.push(c.c[1] - c.r, c.c[1] + c.r); }
  const xlo = Math.min(...xs), xhi = Math.max(...xs), ylo = Math.min(...ys), yhi = Math.max(...ys);
  let mx = Math.max(0.12 * (xhi - xlo || 1), 0.4), my = Math.max(0.12 * (yhi - ylo || 1), 0.4);
  // ★ 등축(uniform scale) 보장 — 각이 그림에서 실제와 같아야 한다.
  //   납작하거나 길쭉하면 여백을 늘려 비율을 0.5~1.4 안으로 맞춘다(찌그러뜨리지 않는다).
  let spanX = xhi - xlo + 2 * mx, spanY = yhi - ylo + 2 * my;
  const minA = a.aspect_min ?? 0.5, maxA = 1.4;
  if (spanY / spanX < minA) { const need = minA * spanX; my += (need - spanY) / 2; spanY = need; }
  if (spanY / spanX > maxA) { const need = spanY / maxA; mx += (need - spanX) / 2; spanX = need; }
  const f = frame([xlo - mx, xhi + mx], [ylo - my, yhi + my], o, { aspect: spanY / spanX, padExtra: 6 });
  const p2 = (n) => [f.X(P[n][0]), f.Y(P[n][1])];
  let s = svgOpen(f.W, f.H, o);
  if (a.axes) s += axes(f, o, { grid: true });
  arr(a.shade).forEach((tri, si) => {
    const ps = arr(tri).map((n) => (P[n] ? p2(n) : null)).filter(Boolean);
    if (ps.length >= 3) s += POLY(ps, { fill: o.accent, op: 0.12, w: 0, k: `shade:${si}` });
  });
  cir.forEach((c, ci) => { s += C(f.X(c.c[0]), f.Y(c.c[1]), Math.abs(f.X(c.c[0] + c.r) - f.X(c.c[0])), { dash: c.dash ? "4 3" : null, k: `circle:${ci}` }); });
  for (const g of seg) {
    const A = p2(g.a), B = p2(g.b);
    s += L(A[0], A[1], B[0], B[1], { dash: g.dash ? "4 3" : null, w: 1.4, k: `seg:${g.a}-${g.b}` });
    if (g.label) {
      const nx = -(B[1] - A[1]), ny = B[0] - A[0], nl = Math.hypot(nx, ny) || 1, txt = lab(g.label);
      // 오프셋 11px는 가로 선분 기준 — 세로에 가까운 선분에서는 넓은 라벨("12 cm")이 선에 얹히므로
      // 글자 상자를 법선에 투영한 반폭 + 4px 만큼은 띄운다 (가로 선분·한 글자 라벨은 그대로 11px)
      const off = Math.max(11, (Math.abs(nx / nl) * textW(txt, 11) + Math.abs(ny / nl) * 11) / 2 + 4);
      s += T((A[0] + B[0]) / 2 + nx / nl * off, (A[1] + B[1]) / 2 + ny / nl * off + 3, txt, { size: 11, k: `seglbl:${g.a}-${g.b}` });
    }
  }
  const cxm = keys.reduce((t, n) => t + f.X(P[n][0]), 0) / keys.length;   // 점들의 무게중심(px) — 라벨을 바깥쪽에 둘 때 기준
  const cym = keys.reduce((t, n) => t + f.Y(P[n][1]), 0) / keys.length;
  const M = a.marks || {};
  for (const r of arr(M.right)) {           // ["A","B","C"] — 꼭짓점 B에서의 직각
    const [x, y, z] = arr(r); if (!P[x] || !P[y] || !P[z]) continue;
    const B = p2(y), A = p2(x), Cc = p2(z), sz = 9;
    const u = norm([A[0] - B[0], A[1] - B[1]]), v = norm([Cc[0] - B[0], Cc[1] - B[1]]);
    s += PATH(`M${R2(B[0] + u[0] * sz)} ${R2(B[1] + u[1] * sz)} L${R2(B[0] + (u[0] + v[0]) * sz)} ${R2(B[1] + (u[1] + v[1]) * sz)} L${R2(B[0] + v[0] * sz)} ${R2(B[1] + v[1] * sz)}`, { w: 1.1, k: `right:${y}` });
  }
  arr(M.eq).forEach((grp, gi) => {          // [["A","B"],["C","D"]] — 같은 길이 표시
    for (const e of arr(grp)) {
      const [x, y] = arr(e); if (!P[x] || !P[y]) continue;
      const A = p2(x), B = p2(y), mxp = (A[0] + B[0]) / 2, myp = (A[1] + B[1]) / 2;
      const u = norm([B[0] - A[0], B[1] - A[1]]), n = [-u[1], u[0]];
      for (let k = 0; k <= gi; k++) {
        const off = (k - gi / 2) * 4;
        s += L(mxp + u[0] * off - n[0] * 4, myp + u[1] * off - n[1] * 4,
               mxp + u[0] * off + n[0] * 4, myp + u[1] * off + n[1] * 4, { w: 1.2, k: `eq:${x}-${y}` });
      }
    }
  });
  for (const g of arr(M.arc)) {             // {at,from,to,label} — 각 표시
    const at = g.at ?? g.vertex, from = g.from, to = g.to;
    if (!P[at] || !P[from] || !P[to]) continue;
    const B = p2(at), A = p2(from), Cc = p2(to);
    // 호 반지름은 두 변 길이에 맞춰 줄인다 — 작은 삼각형에서 라벨이 겹치지 않도록
    const R = Math.max(9, Math.min(18, 0.3 * Math.min(Math.hypot(A[0] - B[0], A[1] - B[1]),
                                                      Math.hypot(Cc[0] - B[0], Cc[1] - B[1]))));
    const a1 = Math.atan2(A[1] - B[1], A[0] - B[0]), a2 = Math.atan2(Cc[1] - B[1], Cc[0] - B[0]);
    let d = a2 - a1; while (d <= -Math.PI) d += 2 * Math.PI; while (d > Math.PI) d -= 2 * Math.PI;
    const large = 0, sweep = d > 0 ? 1 : 0;
    const ak = g.k || `arc:${at}`;
    s += PATH(`M${R2(B[0] + R * Math.cos(a1))} ${R2(B[1] + R * Math.sin(a1))} A${R} ${R} 0 ${large} ${sweep} ${R2(B[0] + R * Math.cos(a2))} ${R2(B[1] + R * Math.sin(a2))}`, { w: 1.1, op: 0.85, k: ak });
    if (g.label != null) {
      const am = a1 + d / 2, txt = lab(g.label);
      // 글자가 두 변 사이에 들어가려면 이등분선 위 거리가 (반폭 + 2) / sin(각/2) 이상이어야 한다.
      // 25° 이상의 각은 이등분선 위에서 그만큼 밀어낸다(기존 R + 13이 최소, R + 70이 최대 — 긴 라벨 "(4x + 35)°"도 쐐기 안에).
      // 25° 미만의 좁은 각은 쐐기 안에 못 들어가므로 호 바깥쪽 옆 — 그림 무게중심 반대편 — 에 둔다.
      const half = Math.abs(d) / 2, need = (textW(txt, 11) / 2 + 2) / Math.max(Math.sin(half), 0.01);
      let lx, ly;
      if (Math.abs(d) >= Math.PI * 25 / 180) {
        const D = Math.min(R + 70, Math.max(R + 13, need));
        lx = B[0] + D * Math.cos(am); ly = B[1] + D * Math.sin(am);
      } else {
        const nx = -Math.sin(am), ny = Math.cos(am);
        const side = (B[0] - cxm) * nx + (B[1] - cym) * ny >= 0 ? 1 : -1;
        const D = R + 10, off = textW(txt, 11) / 2 + 8;
        lx = B[0] + D * Math.cos(am) + side * off * nx; ly = B[1] + D * Math.sin(am) + side * off * ny;
      }
      s += T(lx, ly + 3.5, txt, { size: 11, k: ak + ":lbl" });
    }
  }
  const hideDot = new Set(arr(a.nodot));
  const segPx = seg.map((g) => ({ A: p2(g.a), B: p2(g.b) }));
  for (const k of keys) {
    const [x, y] = p2(k);
    if (hideDot.has(k)) continue;
    s += DOT(x, y, { r: 2.8, k: `pt:${k}` });
    // 점 이름은 무게중심 반대쪽이 기본. 그 자리가 선분에 얹히면(예: 외심 O 옆을 지나는 현) 반대쪽·양옆 순으로 비켜 준다.
    const u0 = norm([x - cxm, y - cym]);
    const w = textW(k, 11.5), h = 11.5;
    let u = u0;
    for (const c of [u0, [-u0[0], -u0[1]], [-u0[1], u0[0]], [u0[1], -u0[0]]]) {
      const lx = x + c[0] * 12, ly = y + c[1] * 12 + 4;
      const box = { x0: lx - w / 2 + 1, x1: lx + w / 2 - 1, y0: ly - h * 0.78 + 1, y1: ly + h * 0.22 - 1 };
      if (!segPx.some((sg) => segHitsBox(sg.A, sg.B, box))) { u = c; break; }
    }
    s += T(x + u[0] * 12, y + u[1] * 12 + 4, k, { size: 11.5, k: `lbl:${k}` });
  }
  arr(a.labels).forEach((g, li) => {
    const c = typeof g.at === "string" ? P[g.at] : pt(g.at, {});
    if (!c) return;
    s += T(f.X(c[0]) + (g.dx || 0), f.Y(c[1]) + (g.dy || 0), lab(g.text), { size: 11, fill: g.accent ? o.accent : null, k: g.k || `label:${li}` });
  });
  return s + "</svg>";
}
function norm([x, y]) { const d = Math.hypot(x, y) || 1; return [x / d, y / d]; }
/** 선분 A–B가 상자 {x0,x1,y0,y1}를 지나는가 (Liang–Barsky) — 점 이름 자리 고르기에 쓴다 */
function segHitsBox(A, B, b) {
  if (b.x1 <= b.x0 || b.y1 <= b.y0) return false;
  let t0 = 0, t1 = 1;
  const dx = B[0] - A[0], dy = B[1] - A[1];
  for (const [p, q] of [[-dx, A[0] - b.x0], [dx, b.x1 - A[0]], [-dy, A[1] - b.y0], [dy, b.y1 - A[1]]]) {
    if (p === 0) { if (q < 0) return false; continue; }
    const r = q / p;
    if (p < 0) { if (r > t1) return false; if (r > t0) t0 = r; }
    else { if (r < t0) return false; if (r < t1) t1 = r; }
  }
  return t0 < t1;
}
/** 라벨 글자 폭 어림(px) — 라벨을 선·변에서 얼마나 띄울지 정할 때 쓴다 (ASCII 0.58em · 그 밖 0.95em) */
function textW(s, size) { let w = 0; for (const ch of String(s ?? "")) w += size * (/[\x20-\x7e]/.test(ch) ? 0.58 : 0.95); return w; }

// ---------------------------------------------------------------- tri / quad / polygon / trapezoid
function degOf(v) { const n = num(v, {}); return (isNum(n) && n > 0 && n < 180) ? n : null; }

function fnTri(a, o) {
  const v = (arr(a.v).length ? arr(a.v) : arr(a.vertices));
  const V = (v.length >= 3 ? v : ["A", "B", "C"]).slice(0, 3).map((x) => lab(x) || "?");
  // 각: [A,B,C] 순서 (빈칸·null 허용). marks 안의 {type:'angle',vertex,measure}도 흡수
  const ang = [null, null, null];
  arr(a.angles).forEach((x, i) => { if (i < 3) ang[i] = degOf(x); });
  for (const m of arr(a.marks)) {
    if (m && typeof m === "object" && (m.type === "angle") && m.vertex) {
      const i = V.indexOf(lab(m.vertex)); if (i >= 0) ang[i] = degOf(m.measure ?? m.value ?? m.deg) ?? ang[i];
    }
  }
  let A = [0, 0], B = [0, 0], Cc = [0, 0];
  const known = ang.map((x, i) => [x, i]).filter(([x]) => x != null);
  if (known.length >= 2) {
    const [aA, aB] = [ang[0] ?? (180 - ang[1] - ang[2]), ang[1] ?? (180 - ang[0] - ang[2])];
    const rA = aA * Math.PI / 180, rB = aB * Math.PI / 180, rC = Math.PI - rA - rB;
    if (rC > 0.05) {
      const c = 1;                              // AB = 1
      const b = c * Math.sin(rB) / Math.sin(rC); // AC
      A = [0, 0]; B = [c, 0]; Cc = [b * Math.cos(rA), b * Math.sin(rA)];
    } else { A = [0, 0]; B = [1, 0]; Cc = [0.38, 0.82]; }
  } else if (known.length === 1 && known[0][0] !== 90) {
    const [d, i] = known[0], rd = d * Math.PI / 180;
    // 알려진 각을 i번 꼭짓점에 실제로 배치 (나머지 두 각은 보기 좋게 배분)
    const rest = (Math.PI - rd) / 2, rB = rest * 1.15, rC = Math.PI - rd - rB;
    const c = 1, b = c * Math.sin(rB) / Math.sin(rC);
    const P = [[0, 0], [c, 0], [b * Math.cos(rd), b * Math.sin(rd)]];
    // P[0]이 각 d를 갖는 꼭짓점 → i만큼 회전 배정
    const asg = [P[(0 - i + 3) % 3], P[(1 - i + 3) % 3], P[(2 - i + 3) % 3]];
    A = asg[0]; B = asg[1]; Cc = asg[2];
    if (i === 0) { A = P[0]; B = P[1]; Cc = P[2]; }
    if (i === 1) { B = P[0]; Cc = P[1]; A = P[2]; }
    if (i === 2) { Cc = P[0]; A = P[1]; B = P[2]; }
  } else if (ang.includes(90)) {
    const i = ang.indexOf(90);
    const base = [[0, 0], [1, 0], [0, 0.8]];
    A = base[(0 - i + 3) % 3]; B = base[(1 - i + 3) % 3]; Cc = base[(2 - i + 3) % 3];
    A = [0, 0.8]; B = [0, 0]; Cc = [1, 0];
    if (i === 0) { A = [0, 0]; B = [0, 0.85]; Cc = [1.05, 0]; }
    if (i === 1) { A = [0, 0.85]; B = [0, 0]; Cc = [1.05, 0]; }
    if (i === 2) { A = [0, 0.85]; B = [1.05, 0]; Cc = [0, 0]; }
  } else { A = [0.42, 0.9]; B = [0, 0]; Cc = [1.1, 0]; }
  const pts = { [V[0]]: A, [V[1]]: B, [V[2]]: Cc };
  // 변 라벨: 꼭짓점 이름쌍이면 생략, 그 밖에는 라벨로
  const isName = (t) => { const s = String(t || "").replace(/\s/g, ""); return s.length === 2 && V.includes(s[0]) && V.includes(s[1]); };
  const edges = [[V[0], V[1]], [V[1], V[2]], [V[0], V[2]]];
  const segs = edges.map(([p, q], i) => {
    const raw = arr(a.sides)[i];
    const t = (raw == null || raw === "" || isName(raw)) ? null : lab(raw);
    return { a: p, b: q, label: t };
  });
  const marks = { right: [], eq: [], arc: [] };
  ang.forEach((d, i) => {
    if (d == null) return;
    const at = V[i], from = V[(i + 1) % 3], to = V[(i + 2) % 3];
    if (Math.abs(d - 90) < 0.01) marks.right.push([from, at, to]);
    else marks.arc.push({ at, from, to, label: `${R2(d)}°` });
  });
  for (const m of arr(a.marks)) {
    if (typeof m === "string" && /right|직각/.test(m)) marks.right.push([V[0], V[1], V[2]]);
    if (m && typeof m === "object" && m.type === "segment" && m.label && m.length) {
      const s2 = String(m.label).replace(/\s/g, "");
      const e = segs.find((g) => (g.a + g.b === s2) || (g.b + g.a === s2));
      if (e) e.label = lab(m.length);
    }
  }
  return fnScene({ pts, segs, marks }, o);
}

function fnPolygonLike(a, o, nDefault) {
  const vertsRaw = arr(a.vertices).map((v) => pt(v, {})).filter(Boolean);
  const names = (arr(a.labels).length ? arr(a.labels) : arr(a.v).length ? arr(a.v) : arr(a.vertices))
    .map((x) => (typeof x === "string" ? lab(x) : lab(x && (x.name ?? x.label))))
    .filter((x) => x && /^[A-Za-z][A-Za-z0-9_']*$/.test(x));
  let n = num(a.n, {}) || nDefault || (vertsRaw.length || names.length) || 5;
  n = Math.max(3, Math.min(12, Math.round(n)));
  const pts = {};
  if (vertsRaw.length >= 3) {
    vertsRaw.forEach((c, i) => { pts[names[i] || String.fromCharCode(65 + i)] = c; });
  } else {
    const N = Math.max(n, names.length || 0);
    for (let i = 0; i < N; i++) {
      const th = Math.PI / 2 + (2 * Math.PI * i) / N * (N === 4 ? 1 : 1) + (N % 2 === 0 ? Math.PI / N : 0);
      pts[names[i] || String.fromCharCode(65 + i)] = [Math.cos(th), Math.sin(th)];
    }
  }
  const ks = Object.keys(pts);
  const segs = ks.map((k, i) => ({ a: k, b: ks[(i + 1) % ks.length] }));
  arr(a.sides).forEach((sd, i) => {
    if (sd == null || sd === "" || !segs[i]) return;
    const t = typeof sd === "object" ? lab(sd.label ?? sd.len ?? sd.length) : lab(sd);
    if (t && !/^[A-Z]{2}$/.test(t)) segs[i].label = t;
  });
  const marks = { right: [], eq: [], arc: [] };
  arr(a.angles).forEach((d, i) => {
    const deg = degOf(d && typeof d === "object" ? (d.deg ?? d.measure ?? d.value) : d);
    if (deg == null || !ks[i]) return;
    const at = ks[i], from = ks[(i + 1) % ks.length], to = ks[(i - 1 + ks.length) % ks.length];
    if (Math.abs(deg - 90) < 0.01) marks.right.push([from, at, to]);
    else marks.arc.push({ at, from, to, label: `${R2(deg)}°` });
  });
  if (a.diagonals === "fan" || a.diagonals === "부채") {   // 한 꼭짓점에서 그은 대각선 — 삼각형 n-2개
    for (let i = 2; i < ks.length - 1; i++) segs.push({ a: ks[0], b: ks[i], dash: true });
  } else {
    for (const d of arr(a.diagonals)) {
      const s2 = String(d).replace(/\s/g, "");
      if (s2.length === 2 && pts[s2[0]] && pts[s2[1]]) segs.push({ a: s2[0], b: s2[1], dash: true });
    }
  }
  return fnScene({ pts, segs, marks }, o);
}

function fnRect(a, o) {
  const w = num(a.w ?? a.width, {}), h = num(a.h ?? a.height, {});
  const W = isNum(w) && w > 0 ? w : 1.6, H = isNum(h) && h > 0 ? h : 1;
  const k = Math.max(W, H);
  const pts = { A: [0, H / k], B: [0, 0], C: [W / k, 0], D: [W / k, H / k] };
  const segs = [{ a: "A", b: "D", label: (a.w != null && !isNum(w)) || isNum(w) ? lab(a.w ?? a.width) : null },
                { a: "D", b: "C" }, { a: "C", b: "B" },
                { a: "B", b: "A", label: lab(a.h ?? a.height) }];
  segs[1].label = null;
  const marks = { right: [["D", "A", "B"], ["A", "B", "C"]], eq: [], arc: [] };
  const scene = { pts, segs, marks };
  const out = fnScene(scene, o);
  return out;
}

function fnCircle(a, o) {
  const r = num(a.r ?? a.radius, {});
  const R = isNum(r) && r > 0 ? 1 : 1;
  const cLab = lab(a.center && typeof a.center !== "string" ? "O" : (typeof a.center === "string" && !/^point/i.test(a.center) ? a.center : "O")) || "O";
  const W = o.width, H = Math.min(220, W * 0.82), cx = W / 2, cy = H / 2, rr = Math.min(W, H) / 2 - o.pad - 12;
  let s = svgOpen(W, H, o);
  s += C(cx, cy, rr, { w: 1.5 });
  s += DOT(cx, cy, { r: 2.6 });
  s += T(cx - 6, cy + 13, cLab, { anchor: "end", size: 11 });
  const rt = a.r != null ? lab(a.r) : null;
  if (rt) { s += L(cx, cy, cx + rr, cy, { w: 1.2, dash: "4 3" }); s += T(cx + rr / 2, cy - 6, rt, { size: 11 }); }
  const np = num(a.points, {});
  if (isNum(np) && np >= 2 && np <= 24) {
    for (let i = 0; i < np; i++) {
      const th = -Math.PI / 2 + 2 * Math.PI * i / np;
      s += DOT(cx + rr * Math.cos(th), cy + rr * Math.sin(th), { r: 2.6, fill: o.accent, stroke: o.accent });
    }
  } else {
    for (const p of arr(a.points)) {
      const t = lab(p && (p.name ?? p.label ?? p));
      if (!t) continue;
      const i = arr(a.points).indexOf(p), n = arr(a.points).length;
      const th = -Math.PI / 2 + 2 * Math.PI * i / Math.max(1, n);
      s += DOT(cx + rr * Math.cos(th), cy + rr * Math.sin(th), { r: 2.8, fill: o.accent, stroke: o.accent });
      s += T(cx + (rr + 12) * Math.cos(th), cy + (rr + 12) * Math.sin(th) + 4, t, { size: 11 });
    }
  }
  return s + "</svg>";
}

function fnSector(a, o) {
  const deg = num(a.angle, {}), rt = lab(a.r), at = lab(a.angle);
  const W = o.width, H = Math.min(210, W * 0.8), cx = W / 2 - 20, cy = H / 2 + 20, rr = Math.min(W, H) / 2 - o.pad - 6;
  const d = isNum(deg) ? Math.max(1, Math.min(359, deg)) : 90;
  const a0 = 0, a1 = -d * Math.PI / 180;
  const P0 = [cx + rr, cy], P1 = [cx + rr * Math.cos(a1), cy + rr * Math.sin(a1)];
  let s = svgOpen(W, H, o);
  s += PATH(`M${R2(cx)} ${R2(cy)} L${R2(P0[0])} ${R2(P0[1])} A${rr} ${rr} 0 ${d > 180 ? 1 : 0} 0 ${R2(P1[0])} ${R2(P1[1])} Z`,
            { w: 1.5, fill: o.accent, op: 0.14 });
  s += PATH(`M${R2(cx)} ${R2(cy)} L${R2(P0[0])} ${R2(P0[1])} A${rr} ${rr} 0 ${d > 180 ? 1 : 0} 0 ${R2(P1[0])} ${R2(P1[1])} Z`, { w: 1.5, k: "sector" });
  s += PATH(`M${R2(P0[0])} ${R2(P0[1])} A${rr} ${rr} 0 ${d > 180 ? 1 : 0} 0 ${R2(P1[0])} ${R2(P1[1])}`, { w: 1.5, k: "arc" });
  s += L(cx, cy, P0[0], P0[1], { w: 1.5, k: "radius" });
  s += DOT(cx, cy, { r: 2.6 });
  s += T(cx - 8, cy + 14, "O", { anchor: "end", size: 11 });
  if (rt) s += T(cx + rr / 2, cy + 14, rt, { size: 11, k: "r-lbl" });
  if (at) s += T(cx + 26 * Math.cos(a1 / 2), cy + 26 * Math.sin(a1 / 2) + 4, /°|도/.test(at) ? at : at + "°", { size: 11, k: "angle-lbl" });
  return s + "</svg>";
}

function fnCrossing(a, o) {
  const raw = arr(a.angles).filter((x) => x != null && x !== "");
  const W = o.width, H = 156, cx = W / 2, cy = H / 2, r = Math.min(W, H) / 2 - 26;
  let s = svgOpen(W, H, o);
  const th1 = 0, th2 = 64 * Math.PI / 180;           // 화면각(위가 +)
  const seg = (th) => L(cx - r * Math.cos(th), cy + r * Math.sin(th), cx + r * Math.cos(th), cy - r * Math.sin(th), { w: 1.4 });
  s += seg(th1) + seg(th2);
  s += DOT(cx, cy, { r: 2.6 });
  // 네 영역의 이등분 방향: (th1,th2) / (th2,th1+pi) / (th1+pi,th2+pi) / (th2+pi,th1+2pi)
  const dirs = [(th1 + th2) / 2, (th2 + th1 + Math.PI) / 2, (th1 + Math.PI + th2 + Math.PI) / 2, (th2 + Math.PI + th1 + 2 * Math.PI) / 2];
  raw.slice(0, 4).forEach((v, i) => {
    const t = lab(v), th = dirs[i], R = 42;
    const txt = /^-?\d+(\.\d+)?$/.test(String(t)) ? t + "\u00b0" : t;
    s += T(cx + R * Math.cos(th), cy - R * Math.sin(th) + 4, txt, { size: 11.5, fill: o.accent });
  });
  return s + "</svg>";
}
function fnParallel(a, o) {
  const raw = arr(a.angles).filter((x) => x != null && x !== "" && String(x) !== "0");
  const W = o.width, H = 178, pad = o.pad + 8;
  const y1 = 54, y2 = 128;
  let s = svgOpen(W, H, o);
  s += L(pad, y1, W - pad, y1, { w: 1.4 }) + L(pad, y2, W - pad, y2, { w: 1.4 });
  s += T(W - pad, y1 - 8, "l", { anchor: "end", size: 11, op: .7 });
  s += T(W - pad, y2 + 18, "m", { anchor: "end", size: 11, op: .7 });
  // 횡단선: 기울기 고정, 두 평행선과의 실제 교점을 계산해 각 라벨을 배치
  const k = 1.55;                       // dx/dy — 오른쪽 아래로
  const cx = W / 2, cyMid = (y1 + y2) / 2;
  const xAt = (y) => cx + (y - cyMid) / k;
  const yTop = y1 - 34, yBot = y2 + 34;
  s += L(xAt(yTop), yTop, xAt(yBot), yBot, { w: 1.4 });
  const p1 = [xAt(y1), y1], p2 = [xAt(y2), y2];
  s += DOT(p1[0], p1[1], { r: 2.4 }) + DOT(p2[0], p2[1], { r: 2.4 });
  const off = 17;
  const spots = [
    [p1[0] - off - 6, p1[1] - 9], [p1[0] + off, p1[1] - 9],
    [p1[0] - off, p1[1] + 19], [p1[0] + off + 6, p1[1] + 19],
    [p2[0] - off - 6, p2[1] - 9], [p2[0] + off, p2[1] - 9],
    [p2[0] - off, p2[1] + 19], [p2[0] + off + 6, p2[1] + 19],
  ];
  raw.slice(0, 8).forEach((v, i) => {
    const t = lab(v);
    s += T(spots[i][0], spots[i][1], /^-?\d+(\.\d+)?$/.test(String(t)) ? t + "\u00b0" : t, { size: 11, fill: o.accent });
  });
  return s + "</svg>";
}

// ---------------------------------------------------------------- 표·통계 (HTML/SVG)
function fnTable(a) {
  const head = arr(a.head).map(lab), rows = arr(a.rows);
  if (!rows.length && !head.length) return null;
  const cell = (v) => `<td style="border:1px solid currentColor;padding:3px 8px;text-align:center">${esc(lab(v))}</td>`;
  let h = `<table class="fig-table" style="border-collapse:collapse;font-size:13px;margin:2px 0">`;
  if (a.caption) h += `<caption style="font-size:12px;opacity:.7;margin-bottom:3px">${esc(lab(a.caption))}</caption>`;
  if (head.length) h += `<thead><tr>${head.map((t) => `<th style="border:1px solid currentColor;padding:3px 8px;background:currentColor;color:transparent"><span style="color:initial;mix-blend-mode:difference">${esc(t)}</span></th>`).join("")}</tr></thead>`;
  h += `<tbody>${rows.map((r) => `<tr>${arr(r).map(cell).join("")}</tr>`).join("")}</tbody></table>`;
  // 헤더 배경 트릭은 테마 대비가 불안정 — 단순 굵게로 대체
  return h.replace(/background:currentColor;color:transparent"><span style="color:initial;mix-blend-mode:difference">/g, 'font-weight:600">');
}

function barChart(labels, values, o, { ylab } = {}) {
  const vs = values.map((v) => num(v, {}));
  if (!vs.some(isNum)) return null;
  const mx = Math.max(...vs.filter(isNum), 0) * 1.15 || 1;
  const W = o.width, H = 175, padL = 34, padB = 34, padT = 12, padR = 10;
  const n = labels.length || vs.length;
  const bw = (W - padL - padR) / Math.max(1, n);
  let s = svgOpen(W, H, o);
  s += L(padL, H - padB, W - padR, H - padB, { w: 1.1 }) + L(padL, padT, padL, H - padB, { w: 1.1 });
  vs.forEach((v, i) => {
    if (!isNum(v)) return;
    const hgt = (H - padB - padT) * (v / mx);
    s += `<rect x="${R2(padL + i * bw + bw * 0.14)}" y="${R2(H - padB - hgt)}" width="${R2(bw * 0.72)}" height="${R2(hgt)}" `
       + `fill="${o.accent}" opacity="0.55" stroke="${o.accent}" stroke-width="1"/>`;
    s += T(padL + i * bw + bw / 2, H - padB - hgt - 4, R2(v), { size: 9.5, op: .8 });
  });
  labels.forEach((t, i) => { s += T(padL + i * bw + bw / 2, H - padB + 13, lab(t), { size: 9, op: .75 }); });
  const step = mx / 4;
  for (let k = 0; k <= 4; k++) {
    const y = H - padB - (H - padB - padT) * k / 4;
    s += L(padL - 3, y, padL, y, { w: 1, op: .7 });
    s += T(padL - 6, y + 3.5, R2(step * k), { anchor: "end", size: 9, op: .65 });
  }
  if (ylab) s += T(padL - 4, padT - 2, lab(ylab), { anchor: "end", size: 9.5, op: .7 });
  return s + "</svg>";
}

function fnHist(a, o) {
  return barChart(arr(a.bins).map(lab), arr(a.counts), o, { ylab: a.labels ?? a.y_label ?? a.y_axis });
}

function fnScatter(a, o) {
  const ps = arr(a.points).map((p) => pt(p, {})).filter(Boolean);
  if (ps.length < 2) return null;
  const xs = ps.map((p) => p[0]), ys = ps.map((p) => p[1]);
  const xr = rng(a.x_range ?? a.xrange, {}) || [Math.min(...xs, 0), Math.max(...xs)];
  const yr = rng(a.y_range ?? a.yrange, {}) || [Math.min(...ys, 0), Math.max(...ys)];
  const pad = (r) => { const d = (r[1] - r[0]) * 0.1 || 1; return [r[0] - d, r[1] + d]; };
  const f = frame(pad(xr), pad(yr), o, { aspect: 0.8 });
  let s = svgOpen(f.W, f.H, o) + axes(f, o, { grid: true });
  ps.forEach((c, i) => {
    s += DOT(f.X(c[0]), f.Y(c[1]), { r: 3, fill: o.accent, stroke: o.accent });
    const t = lab(arr(a.points)[i] && arr(a.points)[i].label);
    if (t) s += T(f.X(c[0]) + 6, f.Y(c[1]) - 5, t, { anchor: "start", size: 10 });
  });
  return s + "</svg>";
}

function fnStemleaf(a) {
  const stems = arr(a.stems).map(lab);
  if (!stems.length) return null;
  const left = arr(a.leaves_left ?? a.left ?? a.left_leaves);
  const right = arr(a.leaves_right ?? a.right ?? a.right_leaves);
  const mid = arr(a.leaves ?? a.data);
  const two = left.length || right.length;
  const labs = arr(a.labels).map(lab);
  const cell = (v, align) => `<td style="border:1px solid currentColor;padding:2px 8px;text-align:${align};letter-spacing:.18em">${esc(v)}</td>`;
  let h = `<table class="fig-stemleaf" style="border-collapse:collapse;font-size:13px">`;
  if (two) {
    h += `<thead><tr><th style="border:1px solid currentColor;padding:2px 8px;font-weight:600">${esc(labs[0] || "잎")}</th>`
       + `<th style="border:1px solid currentColor;padding:2px 8px;font-weight:600">${esc(labs[1] || "줄기")}</th>`
       + `<th style="border:1px solid currentColor;padding:2px 8px;font-weight:600">${esc(labs[2] || "잎")}</th></tr></thead>`;
  } else {
    h += `<thead><tr><th style="border:1px solid currentColor;padding:2px 8px;font-weight:600">줄기</th>`
       + `<th style="border:1px solid currentColor;padding:2px 8px;font-weight:600">잎</th></tr></thead>`;
  }
  h += "<tbody>";
  stems.forEach((st, i) => {
    if (two) h += `<tr>${cell(arr(left[i]).map(lab).join(" "), "right")}${cell(st, "center")}${cell(arr(right[i]).map(lab).join(" "), "left")}</tr>`;
    else h += `<tr>${cell(st, "center")}${cell(arr(mid[i]).map(lab).join(" "), "left")}</tr>`;
  });
  h += "</tbody></table>";
  const nt = lab(a.note ?? a.unit);
  if (nt) h += `<div style="font-size:11.5px;opacity:.7;margin-top:3px">(${esc(nt)})</div>`;
  return h;
}

function fnBoxplot(a, o) {
  const vs = arr(a.values).map((v) => num(v, {})).filter(isNum).sort((p, q) => p - q);
  if (vs.length < 5) return null;
  const q = (k) => { const i = (vs.length - 1) * k; const lo = Math.floor(i), hi = Math.ceil(i); return vs[lo] + (vs[hi] - vs[lo]) * (i - lo); };
  const [mn, q1, me, q3, mx] = [vs[0], q(0.25), q(0.5), q(0.75), vs[vs.length - 1]];
  const W = o.width, H = 110, pad = o.pad + 12, y = 46;
  const X = (v) => pad + (v - mn) / ((mx - mn) || 1) * (W - 2 * pad);
  let s = svgOpen(W, H, o);
  s += L(X(mn), y, X(q1), y, { w: 1.2 }) + L(X(q3), y, X(mx), y, { w: 1.2 });
  s += L(X(mn), y - 8, X(mn), y + 8, { w: 1.2 }) + L(X(mx), y - 8, X(mx), y + 8, { w: 1.2 });
  s += `<rect x="${R2(X(q1))}" y="${y - 15}" width="${R2(X(q3) - X(q1))}" height="30" fill="${o.accent}" opacity=".16" stroke="currentColor" stroke-width="1.2"/>`;
  s += L(X(me), y - 15, X(me), y + 15, { w: 1.6, stroke: o.accent });
  for (const [v, t] of [[mn, "최소"], [q1, "Q1"], [me, "중앙"], [q3, "Q3"], [mx, "최대"]])
    s += T(X(v), y + 30, `${R2(v)}`, { size: 9.5, op: .7 });
  return s + "</svg>";
}

// ---------------------------------------------------------------- venn / tree
function fnVenn(a, o) {
  const sets = arr(a.sets).map((s) => lab(typeof s === "object" ? (s.name ?? s.label) : s)).filter(Boolean);
  const n = Math.min(3, Math.max(2, sets.filter((x) => x.toUpperCase() !== "U").length || 2));
  const W = o.width, H = 190, cx = W / 2, cy = 96, r = 44;
  let s = svgOpen(W, H, o);
  const hasU = sets.some((x) => x.toUpperCase() === "U");
  if (hasU) {
    s += `<rect x="${o.pad}" y="18" width="${W - 2 * o.pad}" height="${H - 30}" fill="none" stroke="currentColor" stroke-width="1.1" rx="4"/>`;
    s += T(o.pad + 10, 32, "U", { anchor: "start", size: 11.5 });
  }
  const named = sets.filter((x) => x.toUpperCase() !== "U");
  const cs = n === 2 ? [[cx - 26, cy], [cx + 26, cy]] : [[cx - 28, cy - 14], [cx + 28, cy - 14], [cx, cy + 26]];
  cs.forEach((c, i) => {
    s += C(c[0], c[1], r, { w: 1.3 });
    const ang = n === 2 ? (i ? 0 : Math.PI) : [-2.4, -0.7, 1.57][i];
    s += T(c[0] + (r + 12) * Math.cos(ang), c[1] + (r + 12) * Math.sin(ang) + 4, named[i] || String.fromCharCode(65 + i), { size: 12 });
  });
  const sh = lab(a.shaded);
  if (sh) s += T(cx, H - 6, `음영: ${sh}`, { size: 10.5, op: .7 });
  return s + "</svg>";
}

function fnTree(a, o) {
  let levels = arr(a.labels);
  if (!levels.length && arr(a.nodes).length) {
    const byL = {};
    for (const nd of arr(a.nodes)) { const l = num(nd.level, {}) ?? 0; (byL[l] = byL[l] || []).push(lab(nd.label)); }
    levels = Object.keys(byL).sort((x, y) => x - y).map((k) => byL[k]);
  }
  if (!levels.length) {
    const n = num(a.levels, {});
    if (!isNum(n)) return null;
    levels = Array.from({ length: Math.min(4, Math.max(2, Math.round(n))) }, (_, i) => Array.from({ length: Math.pow(2, i) }, () => ""));
  }
  const W = o.width, H = 40 + levels.length * 46;
  let s = svgOpen(W, H, o);
  const posOf = (li, i, cnt) => [o.pad + (W - 2 * o.pad) * (i + 0.5) / cnt, 26 + li * 46];
  for (let li = 0; li < levels.length - 1; li++) {
    const A = arr(levels[li]), B = arr(levels[li + 1]);
    B.forEach((_, j) => {
      const p = posOf(li, Math.min(A.length - 1, Math.floor(j * A.length / Math.max(1, B.length))), A.length);
      const q = posOf(li + 1, j, B.length);
      s += L(p[0], p[1] + 8, q[0], q[1] - 8, { w: 1, op: .7 });
    });
  }
  levels.forEach((row, li) => arr(row).forEach((t, i) => {
    const [x, y] = posOf(li, i, arr(row).length);
    s += C(x, y, 9, { fill: "none", w: 1.2 });
    if (t) s += T(x, y + 3.6, lab(t), { size: 9.5 });
  }));
  return s + "</svg>";
}

// ---------------------------------------------------------------- solid / net (정형 몇 종)
const SOLID_ALIAS = {
  cube: "cube", 정육면체: "cube", 육면체: "cube",
  rectangular_prism: "box", 직육면체: "box", box: "box", cuboid: "box",
  cylinder: "cylinder", 원기둥: "cylinder",
  cone: "cone", 원뿔: "cone",
  sphere: "sphere", 구: "sphere", hemisphere: "hemisphere", 반구: "hemisphere",
  triangular_prism: "triprism", 삼각기둥: "triprism", 정삼각기둥: "triprism",
  square_pyramid: "pyramid", 사각뿔: "pyramid", pyramid: "pyramid", 각뿔: "pyramid",
};
function solidKind(k) {
  const s = String(k || "").trim().toLowerCase().replace(/\s+/g, "_");
  return SOLID_ALIAS[s] || SOLID_ALIAS[String(k || "").trim()] || null;
}
function fnSolid(a, o) {
  const kind = solidKind(a.kind);
  if (!kind) return null;
  const W = o.width, H = 190, cx = W / 2, cy = H / 2;
  const dx = 26, dy = -16;   // 사투상 깊이
  let s = svgOpen(W, H, o);
  const D = (d, at) => { s += PATH(d, at); };
  if (kind === "cube" || kind === "box") {
    const w = kind === "cube" ? 74 : 92, h = kind === "cube" ? 74 : 58;
    const x0 = cx - (w + dx) / 2, y0 = cy - (h + dy) / 2;
    const A = [x0, y0], B = [x0 + w, y0], Cc = [x0 + w, y0 + h], Dd = [x0, y0 + h];
    const off = ([x, y]) => [x + dx, y + dy];
    D(`M${A} L${B} L${Cc} L${Dd} Z`.replace(/,/g, " ").replace(/L(\S+) (\S+)/g, "L$1 $2"), { w: 1.4 });
    s += POLY([A, B, Cc, Dd], { w: 1.4 });
    s += POLY([off(A), off(B), off(Cc)], { w: 0 });
    s += L(...A, ...off(A), { w: 1.2 }) + L(...B, ...off(B), { w: 1.2 }) + L(...Cc, ...off(Cc), { w: 1.2 });
    s += L(...off(A), ...off(B), { w: 1.2 }) + L(...off(B), ...off(Cc), { w: 1.2 });
    s += L(...Dd, ...off(Dd), { w: 1, dash: "3 3", op: .6 });
    s += L(...off(Dd), ...off(A), { w: 1, dash: "3 3", op: .6 });
    s += L(...off(Dd), ...off(Cc), { w: 1, dash: "3 3", op: .6 });
  } else if (kind === "cylinder" || kind === "cone" || kind === "hemisphere") {
    const rx = 46, ry = 15, h = 86;
    const top = cy - h / 2, bot = cy + h / 2;
    if (kind === "cylinder") {
      s += `<ellipse data-k="top" cx="${cx}" cy="${top}" rx="${rx}" ry="${ry}" fill="none" stroke="currentColor" stroke-width="1.4"/>`;
      s += `<ellipse data-k="base" cx="${cx}" cy="${bot}" rx="${rx}" ry="${ry}" fill="none" stroke="none"/>`;
      s += L(cx - rx, top, cx - rx, bot, { w: 1.4 }) + L(cx + rx, top, cx + rx, bot, { w: 1.4 });
      s += PATH(`M${cx - rx} ${bot} A${rx} ${ry} 0 0 0 ${cx + rx} ${bot}`, { w: 1.4 });
      s += PATH(`M${cx - rx} ${bot} A${rx} ${ry} 0 0 1 ${cx + rx} ${bot}`, { w: 1, dash: "3 3", op: .6 });
    } else if (kind === "cone") {
      s += L(cx, top, cx - rx, bot, { w: 1.4 }) + L(cx, top, cx + rx, bot, { w: 1.4 });
      s += PATH(`M${cx - rx} ${bot} A${rx} ${ry} 0 0 0 ${cx + rx} ${bot}`, { w: 1.4 });
      s += PATH(`M${cx - rx} ${bot} A${rx} ${ry} 0 0 1 ${cx + rx} ${bot}`, { w: 1, dash: "3 3", op: .6 });
    } else {
      s += PATH(`M${cx - rx} ${cy} A${rx} ${rx} 0 0 1 ${cx + rx} ${cy}`, { w: 1.4 });
      s += `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="currentColor" stroke-width="1.4"/>`;
    }
    const ht = lab(a.height ?? a.h);
    if (ht && kind !== "hemisphere") { s += L(cx, top, cx, bot, { w: 1, dash: "3 3", op: .6, k: "height" }); s += T(cx + 8, cy, ht, { anchor: "start", size: 11, k: "h-lbl" }); }
    const rt = lab(a.radius ?? a.r);
    if (rt) { s += L(cx, bot, cx + rx, bot, { w: 1, dash: "3 3", op: .6, k: "radius" }); s += T(cx + rx / 2, bot + 14, rt, { size: 11, k: "r-lbl" }); }
  } else if (kind === "sphere") {
    const r = 52;
    s += C(cx, cy, r, { w: 1.4 });
    s += `<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="16" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" opacity=".6"/>`;
    const rt = lab(a.radius ?? a.r);
    if (rt) { s += L(cx, cy, cx + r, cy, { w: 1, dash: "3 3", op: .7 }); s += T(cx + r / 2, cy - 6, rt, { size: 11 }); }
  } else if (kind === "triprism" || kind === "pyramid") {
    const w = 88, h = 66;
    const b = [[cx - w / 2, cy + h / 2], [cx + w / 2, cy + h / 2]];
    if (kind === "pyramid") {
      const back = [cx - w / 2 + dx, cy + h / 2 + dy], back2 = [cx + w / 2 + dx, cy + h / 2 + dy], apex = [cx + dx / 2, cy - h / 2 - 8];
      s += POLY([b[0], b[1], back2, back], { w: 1.4 });
      s += L(...b[0], ...apex, { w: 1.4 }) + L(...b[1], ...apex, { w: 1.4 }) + L(...back2, ...apex, { w: 1.4 });
      s += L(...back, ...apex, { w: 1, dash: "3 3", op: .6 });
    } else {
      const t = [[cx - w / 2 + dx, cy + h / 2 + dy], [cx + w / 2 + dx, cy + h / 2 + dy], [cx + dx, cy - h / 2 + dy]];
      const f2 = [[cx - w / 2, cy + h / 2], [cx + w / 2, cy + h / 2], [cx, cy - h / 2]];
      s += POLY(f2, { w: 1.4 });
      s += POLY(t, { w: 1, dash: "3 3", op: .6 });
      for (let i = 0; i < 3; i++) s += L(...f2[i], ...t[i], { w: 1.2 });
    }
  } else return null;
  return s + "</svg>";
}

// ---------------------------------------------------------------- wire — 이름 붙은 입체 골격 (위치관계용)
// { kind: "box"|"triprism", names: "ABCDEFGH", w, h, d }
//   box      : 윗면 A B C D (앞왼→앞오→뒤오→뒤왼) · 밑면 E F G H (같은 순서, A 아래가 E)
//   triprism : 윗면 A B C (앞왼→앞오→뒤) · 밑면 D E F
// 모서리 키 edge:AB (정규 이름 = 두 글자, data-ka 에 역순도) · 꼭짓점 pt:A · lbl:A · 면 face:ABCD (data-ka 에 회전·역순 전부)
// 뒤쪽에 숨은 모서리는 점선. 도형은 전부 한 번에 그리고 애니메이션은 색으로만 강조한다.
const WIRE_BOX_FACES = ["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "ADHE"];
const WIRE_TRI_FACES = ["ABC", "DEF", "ABED", "BCFE", "ACFD"];
function faceAliases(f) {
  const n = f.length, out = [];
  for (let i = 0; i < n; i++) {
    const r = f.slice(i) + f.slice(0, i);
    out.push("face:" + r, "face:" + [...r].reverse().join(""));
  }
  return [...new Set(out)].join(" ");
}
function fnWire(a, o) {
  const kind = String(a.kind || "box").toLowerCase() === "triprism" ? "triprism" : "box";
  const names = String(a.names || (kind === "box" ? "ABCDEFGH" : "ABCDEF")).replace(/[^A-Za-z]/g, "");
  const need = kind === "box" ? 8 : 6;
  if (names.length !== need) return null;
  const w = Math.max(1, num(a.w) ?? 3), h = Math.max(1, num(a.h) ?? 2), d = Math.max(1, num(a.d) ?? 2);
  // 3D 좌표 (x 오른쪽, y 위, z 뒤)
  let P3, edges, hiddenV;
  if (kind === "box") {
    P3 = [[0, h, 0], [w, h, 0], [w, h, d], [0, h, d], [0, 0, 0], [w, 0, 0], [w, 0, d], [0, 0, d]];
    edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
    hiddenV = 7;                                   // H — 뒤·아래·왼쪽
  } else {
    P3 = [[0, h, 0], [w, h, 0], [w / 2, h, d], [0, 0, 0], [w, 0, 0], [w / 2, 0, d]];
    edges = [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3], [0, 3], [1, 4], [2, 5]];
    hiddenV = 5;                                   // F — 뒤·아래
  }
  const kx = 0.48, ky = 0.36;                      // 사투상
  const raw = P3.map(([x, y, z]) => [x + kx * z, -(y + ky * z)]);
  const xs = raw.map((p) => p[0]), ys = raw.map((p) => p[1]);
  const W = o.width, pad = o.pad + 12;
  const spanX = Math.max(...xs) - Math.min(...xs), spanY = Math.max(...ys) - Math.min(...ys);
  const sc = Math.min((W - 2 * pad) / spanX, 150 / spanY);
  const H = Math.round(spanY * sc + 2 * pad);
  const ox = (W - spanX * sc) / 2 - Math.min(...xs) * sc, oy = pad - Math.min(...ys) * sc;
  const P = raw.map(([x, y]) => [x * sc + ox, y * sc + oy]);
  const cxm = P.reduce((t, p) => t + p[0], 0) / P.length, cym = P.reduce((t, p) => t + p[1], 0) / P.length;
  let s = svgOpen(W, H, o);
  // 면(투명 다각형 — 강조될 때만 보임)
  const faces = kind === "box" ? WIRE_BOX_FACES : WIRE_TRI_FACES;
  const idx = (ch) => "ABCDEFGH".indexOf(ch);
  for (const f of faces) {
    const pts = [...f].map((ch) => P[idx(ch)]);
    const fname = [...f].map((ch) => names[idx(ch)]).join("");
    const poly = POLY(pts, { w: 0, k: `face:${fname}` }).replace("<polygon", `<polygon data-ka="${faceAliases(fname)}" pointer-events="none"`)
      .replace('stroke="currentColor"', 'stroke="none"');
    s += poly;
  }
  // 모서리
  for (const [i, j] of edges) {
    const hidden = i === hiddenV || j === hiddenV;
    const nm = names[i] + names[j];
    const ln = L(P[i][0], P[i][1], P[j][0], P[j][1], { w: hidden ? 1.1 : 1.5, dash: hidden ? "4 3" : "", op: hidden ? 0.7 : 0, k: `edge:${nm}` })
      .replace("<line", `<line data-ka="edge:${nm} edge:${names[j]}${names[i]}"`);
    s += ln;
  }
  // 꼭짓점 라벨 — 그 점에 모이는 모서리들의 반대쪽(어느 모서리와도 겹치지 않는 방향)으로
  P.forEach((p, i) => {
    let vx = 0, vy = 0;
    for (const [a1, b1] of edges) {
      const j = a1 === i ? b1 : b1 === i ? a1 : -1;
      if (j < 0) continue;
      const ex = P[j][0] - p[0], ey = P[j][1] - p[1], el = Math.hypot(ex, ey) || 1;
      vx -= ex / el; vy -= ey / el;
    }
    if (Math.hypot(vx, vy) < 0.2) { vx = p[0] - cxm; vy = p[1] - cym; }
    const L2 = Math.hypot(vx, vy) || 1;
    const lx = p[0] + (vx / L2) * 13, ly = p[1] + (vy / L2) * 13 + 4;
    s += C(p[0], p[1], 2.2, { fill: "currentColor", w: 0, k: `pt:${names[i]}` }).replace('stroke="currentColor"', 'stroke="none"');
    s += T(lx, ly, names[i], { size: 12, k: `lbl:${names[i]}` });
  });
  return s + "</svg>";
}

function fnNet(a, o) {
  const kind = solidKind(a.kind);
  const W = o.width, H = 180;
  const u = 34, cx = W / 2, cy = H / 2;
  let s = svgOpen(W, H, o);
  const sq = (i, j) => `<rect x="${R2(cx + (i - 0.5) * u)}" y="${R2(cy + (j - 0.5) * u)}" width="${u}" height="${u}" fill="none" stroke="currentColor" stroke-width="1.3"/>`;
  if (kind === "cube" || kind === "box") {
    for (const [i, j] of [[-1, -1], [-1, 0], [0, 0], [1, 0], [2, 0], [-1, 1]]) s += sq(i, j);
  } else if (kind === "pyramid") {
    s += sq(0, 0);
    const P = [[cx - u / 2, cy - u / 2], [cx + u / 2, cy - u / 2], [cx + u / 2, cy + u / 2], [cx - u / 2, cy + u / 2]];
    const O = [[cx, cy - u / 2 - 30], [cx + u / 2 + 30, cy], [cx, cy + u / 2 + 30], [cx - u / 2 - 30, cy]];
    for (let k = 0; k < 4; k++) s += POLY([P[k], P[(k + 1) % 4], O[k]], { w: 1.3 });
  } else if (kind === "cylinder") {
    s += `<rect x="${cx - 60}" y="${cy - 26}" width="120" height="52" fill="none" stroke="currentColor" stroke-width="1.3"/>`;
    s += C(cx - 60 - 22, cy, 20, { w: 1.3 }) + C(cx + 60 + 22, cy, 20, { w: 1.3 });
  } else if (kind === "cone") {
    s += PATH(`M${cx - 10} ${cy - 40} A48 48 0 0 1 ${cx + 52} ${cy + 14} L${cx - 10} ${cy - 40} Z`, { w: 1.3 });
    s += C(cx - 52, cy + 24, 20, { w: 1.3 });
  } else return null;
  return s + "</svg>";
}

// ---------------------------------------------------------------- 해설용 도식 (손그림 수준)
// 문제에 그림이 없어도 해설에서는 그려서 설명한다.
// 사실적일 필요 없음 — 서술형 답안에 샤프로 옮겨 그릴 수 있는 정도.

/** journey — 거리·속력·시간 이동 도식 (지점 사이를 오가는 것은 수직선이면 충분하다)
 *  args: { stops:["집","학교"], legs:[{label:"시속 60 km", sub:"2시간", back?:true}], total?:"120 km" } */
function fnJourney(a, o) {
  const stops = arr(a.stops).map(lab).filter((x) => x !== "");
  const legs = arr(a.legs);
  if (stops.length < 2) return null;
  const n = stops.length - 1;
  const W = o.width, pad = o.pad + 16;
  const hasBack = legs.some((g) => g && g.back);
  const H = hasBack ? 152 : 104;
  const y = hasBack ? 66 : 62;
  const X = (i) => pad + (W - 2 * pad) * i / n;
  let s = svgOpen(W, H, o);
  s += L(pad - 8, y, W - pad + 8, y, { w: 1.6 });
  stops.forEach((t, i) => {
    s += L(X(i), y - 7, X(i), y + 7, { w: 1.6, k: `stop:${i}` });
    s += T(X(i), y + 22, t, { size: 11.5, k: `stop-lbl:${i}` });
  });
  // 이동체 (애니메이션용 점 — 기본은 숨김)
  s += `<circle data-k="mover" data-x0="${R2(X(0))}" data-x1="${R2(X(n))}" cx="${R2(X(0))}" cy="${y}" r="5" fill="${o.accent}" opacity="0"/>`;
  let fwd = 0;
  legs.forEach((g, li) => {
    if (!g) return;
    const i = g.back ? Math.max(0, fwd - 1) : Math.min(n - 1, fwd++);
    const x0 = X(i), x1 = X(i + 1), mid = (x0 + x1) / 2;
    const up = !g.back;
    const ay = up ? y - 16 : y + 34;
    s += `<g data-k="leg:${li}">`;
    s += L(x0 + 4, ay, x1 - 4, ay, { w: 1.2, stroke: o.accent });
    const tip = up ? x1 - 4 : x0 + 4, dir = up ? -1 : 1;
    s += PATH(`M${R2(tip)} ${R2(ay)} l${R2(dir * 7)} -3.5 v7 z`, { fill: o.accent, w: 0 });
    if (g.label) s += T(mid, ay + (up ? -6 : 15), lab(g.label), { size: 11, fill: o.accent });
    if (g.sub) s += T(mid, ay + (up ? -19 : 27), lab(g.sub), { size: 10.5, op: .8 });
    s += `</g>`;
  });
  if (a.total) {
    s += T(W / 2, H - 4, `전체 ${lab(a.total)}`, { size: 11, op: .8 });
  }
  return s + "</svg>";
}

/** 화살표(선 + 삼각 머리) — 상황 도식 공용 */
function ARROW(x0, y0, x1, y1, a = {}) {
  const col = a.stroke || "currentColor", w = a.w || 1.3;
  const ang = Math.atan2(y1 - y0, x1 - x0), hl = 8, hw = 3.6;
  const bx = x1 - hl * Math.cos(ang), by = y1 - hl * Math.sin(ang);
  const nx = -Math.sin(ang) * hw, ny = Math.cos(ang) * hw;
  let g = `<g${K(a)}>`;
  g += L(x0, y0, bx, by, { stroke: col, w, dash: a.dash });
  g += `<polygon points="${R2(x1)},${R2(y1)} ${R2(bx + nx)},${R2(by + ny)} ${R2(bx - nx)},${R2(by - ny)}" fill="${col}" stroke="none"/>`;
  return g + `</g>`;
}

/** river — 강을 두 줄로, 강물의 방향·속력은 강 안에, 위에는 순방향(내려갈 때)·아래에는 역방향(거슬러 올라갈 때) 조건 (Park, 09-07)
 *  args: { stops:["A","B"], span:"12 km", flow:{label:"강물 시속 2 km", dir:"right"}, down:{label, sub}, up:{label, sub} }
 *  키: bank:0/1 flow flow-lbl down down-lbl down-sub up up-lbl up-sub span-lbl stop:i stop-lbl:i  — 전부 한 번에 그리고 강조만 애니메이션 */
function fnRiver(a, o) {
  const W = o.width, pad = o.pad + 18;
  const stops = arr(a.stops).map(lab); if (stops.length < 2) stops.splice(0, stops.length, "A", "B");
  const flow = a.flow || {}, down = a.down || {}, up = a.up || {};
  const toRight = String(flow.dir || "right") !== "left";
  const H = 168, y0 = 62, y1 = 96;                         // 두 줄 = 강둑
  const x0 = pad, x1 = W - pad;
  const WATER = "#3b82c4";
  let s = svgOpen(W, H, o);
  s += `<rect x="${R2(x0 - 10)}" y="${y0}" width="${R2(x1 - x0 + 20)}" height="${y1 - y0}" fill="${WATER}" opacity=".10"/>`;
  s += L(x0 - 10, y0, x1 + 10, y0, { w: 1.6, k: "bank:0" });
  s += L(x0 - 10, y1, x1 + 10, y1, { w: 1.6, k: "bank:1" });
  // 강물 방향 — 강 안에 짧은 화살표 여러 개 + 조건
  const ym = (y0 + y1) / 2;
  s += `<g data-k="flow">`;
  for (let i = 0; i < 2; i++) {
    const cx = x0 + (x1 - x0) * (0.16 + 0.2 * i);
    const ax0 = cx - 9, ax1 = cx + 9;
    s += toRight ? ARROW(ax0, ym, ax1, ym, { stroke: WATER, w: 1.2 }) : ARROW(ax1, ym, ax0, ym, { stroke: WATER, w: 1.2 });
  }
  s += `</g>`;
  if (flow.label) s += T(x0 + (x1 - x0) * 0.68, ym + 4, lab(flow.label), { size: 10.5, fill: WATER, k: "flow-lbl" });   // 강 안, 오른쪽
  // 지점(양 끝 세로 눈금)
  stops.slice(0, 2).forEach((t, i) => {
    const x = i === 0 ? x0 : x1;
    s += L(x, y0 - 4, x, y1 + 4, { w: 1.4, k: `stop:${i}` });
    s += T(x, y1 + 18, t, { size: 11.5, k: `stop-lbl:${i}` });
  });
  if (a.span) s += T((x0 + x1) / 2, y1 + 18, lab(a.span), { size: 10.5, op: .8, k: "span-lbl" });
  // 위: 순방향(강물과 같은 쪽) / 아래: 역방향
  const yd = y0 - 16, yu = y1 + 36;
  s += toRight ? ARROW(x0 + 6, yd, x1 - 6, yd, { stroke: o.accent, k: "down" }) : ARROW(x1 - 6, yd, x0 + 6, yd, { stroke: o.accent, k: "down" });
  if (down.label) s += T((x0 + x1) / 2, yd - 7, lab(down.label), { size: 11, fill: o.accent, k: "down-lbl" });
  if (down.sub) s += T((x0 + x1) / 2, yd - 20, lab(down.sub), { size: 10.5, op: .8, k: "down-sub" });
  s += toRight ? ARROW(x1 - 6, yu, x0 + 6, yu, { stroke: o.accent, k: "up" }) : ARROW(x0 + 6, yu, x1 - 6, yu, { stroke: o.accent, k: "up" });
  if (up.label) s += T((x0 + x1) / 2, yu + 15, lab(up.label), { size: 11, fill: o.accent, k: "up-lbl" });
  if (up.sub) s += T((x0 + x1) / 2, yu + 28, lab(up.sub), { size: 10.5, op: .8, k: "up-sub" });
  return s + "</svg>";
}

/** mountain — 산은 우상향 굵은 초록 직선. 오를 때 조건은 왼쪽(위쪽)에 화살표와 함께, 내려올 때는 반대편에 (Park, 09-07)
 *  args: { base:"출발", peak:"정상", up:{label, sub}, down:{label, sub}, total:"…" }
 *  키: slope base peak base-lbl peak-lbl up up-lbl up-sub down down-lbl down-sub total-lbl */
function fnMountain(a, o) {
  const W = o.width, pad = o.pad + 10;
  const up = a.up || {}, down = a.down || {};
  const H = 176;
  const bx = pad + 56, by = H - 34, px = W - pad - 56, py = 34;   // 출발(왼아래) → 정상(오른위)
  const GREEN = "#2e8b57";
  let s = svgOpen(W, H, o);
  s += L(bx, by, px, py, { stroke: GREEN, w: 5, k: "slope" });
  s += L(bx - 30, by, bx, by, { w: 1.2, op: .5 });                 // 땅
  s += DOT(bx, by, { r: 3, k: "base" }) + DOT(px, py, { r: 3, k: "peak" });
  s += T(bx, by + 18, lab(a.base ?? "출발"), { size: 11, k: "base-lbl" });
  s += T(px, py - 10, lab(a.peak ?? "정상"), { size: 11, k: "peak-lbl" });
  // 경사선과 평행한 화살표 — 오를 때(왼쪽 위 편), 내려올 때(오른쪽 아래 편)
  const dx = px - bx, dy = py - by, L2 = Math.hypot(dx, dy), ux = dx / L2, uy = dy / L2;
  const nx = uy, ny = -ux;                                          // 왼쪽(위) 법선
  const off = 22, ins = 26;
  const ax0 = bx + ux * ins + nx * off, ay0 = by + uy * ins + ny * off, ax1 = px - ux * ins + nx * off, ay1 = py - uy * ins + ny * off;
  s += ARROW(ax0, ay0, ax1, ay1, { stroke: o.accent, k: "up" });
  const mxu = (ax0 + ax1) / 2 + nx * 14, myu = (ay0 + ay1) / 2 + ny * 14;
  if (up.label) s += T(mxu, myu, lab(up.label), { size: 11, fill: o.accent, anchor: "end", k: "up-lbl" });
  if (up.sub) s += T(mxu, myu + 13, lab(up.sub), { size: 10.5, op: .8, anchor: "end", k: "up-sub" });
  const dx0 = px - ux * ins - nx * off, dy0 = py - uy * ins - ny * off, dx1 = bx + ux * ins - nx * off, dy1 = by + uy * ins - ny * off;
  s += ARROW(dx0, dy0, dx1, dy1, { stroke: o.accent, k: "down" });
  const mxd = (dx0 + dx1) / 2 - nx * 14, myd = (dy0 + dy1) / 2 - ny * 14 + 4;
  if (down.label) s += T(mxd, myd, lab(down.label), { size: 11, fill: o.accent, anchor: "start", k: "down-lbl" });
  if (down.sub) s += T(mxd, myd + 13, lab(down.sub), { size: 10.5, op: .8, anchor: "start", k: "down-sub" });
  if (a.total) s += T(W / 2, H - 4, lab(a.total), { size: 11, op: .8, k: "total-lbl" });
  return s + "</svg>";
}

/** passing — 기차·터널/다리 통과 도식
 *  args: { obj:{label:"기차", len:"x"}, span:{label:"다리", len:"300 m"}, total?:"300 + x" } */
function fnPassing(a, o) {
  const ob = a.obj || {}, sp = a.span || {};
  const W = o.width, H = 132, pad = o.pad + 6;
  const yTrack = 84;                       // 다리(두꺼운 선)
  const tw = 62, th = 20;                  // 기차(둥글고 긴 직사각형)
  const bx0 = pad + tw + 4, bx1 = W - pad - tw - 2;   // 오른쪽에 기차가 완전히 빠져나올 자리를 남긴다
  const tx = bx0 - tw, ty = yTrack - th - 4;   // ★ 기차 앞머리 = 다리 왼쪽 끝 (이격 0)
  const dx = (bx1 - bx0) + tw;              // 통과 거리 = 다리 + 기차 (화면 px)
  let s = svgOpen(W, H, o);
  // 다리
  s += L(bx0, yTrack, bx1, yTrack, { w: 5, k: "span" });
  s += L(bx0, yTrack - 9, bx0, yTrack + 9, { w: 1.3, k: "span-l" });
  s += L(bx1, yTrack - 9, bx1, yTrack + 9, { w: 1.3, k: "span-r" });
  s += T((bx0 + bx1) / 2, yTrack + 24, `${lab(sp.label || "다리")} ${lab(sp.len ?? "")}`.trim(), { size: 11, k: "span-lbl" });
  // 기차 (그룹 — 애니메이션에서 통째로 이동)
  s += `<g data-k="train" data-dx="${R2(dx)}">`
     + `<rect x="${R2(tx)}" y="${R2(ty)}" width="${tw}" height="${th}" rx="${th / 2}" fill="var(--fig-bg,#fff)" stroke="currentColor" stroke-width="1.4"/>`
     + L(tx + tw * 0.62, ty, tx + tw * 0.62, ty + th, { w: 1, op: .6 })
     + T(tx + tw / 2, ty - 6, `${lab(ob.label || "기차")} ${lab(ob.len ?? "")}`.trim(), { size: 11 })
     + `</g>`;
  // 통과 거리 화살표 (기차 뒤끝 → 다리 끝)  — 정적 표시
  const ay = 30;
  s += L(tx, ay, bx1, ay, { w: 1.2, stroke: o.accent, dash: "5 3", k: "arrow" });
  s += PATH(`M${R2(tx)} ${ay} l7 -3.5 v7 z`, { fill: o.accent, w: 0, k: "arrow-l" });
  s += PATH(`M${R2(bx1)} ${ay} l-7 -3.5 v7 z`, { fill: o.accent, w: 0, k: "arrow-r" });
  s += L(tx, ay, tx, ty, { w: .9, op: .45, dash: "3 3", k: "guide-l" });
  s += L(bx1, ay, bx1, yTrack - 9, { w: .9, op: .45, dash: "3 3", k: "guide-r" });
  s += T((tx + bx1) / 2, ay - 6, `통과 거리 ${lab(a.total ?? "")}`.trim(), { size: 11, fill: o.accent, k: "arrow-lbl" });
  // 실제 이동 궤적 (애니메이션이 늘린다 — 기차 뒤끝이 지나간 길)
  s += `<line data-k="trail" data-x0="${R2(tx)}" data-dx="${R2(dx)}" x1="${R2(tx)}" y1="${yTrack + 8}" x2="${R2(tx)}" y2="${yTrack + 8}" stroke="${o.accent}" stroke-width="3" stroke-linecap="round" opacity="0"/>`;
  return s + "</svg>";
}

/** bar — 부분·전체 막대 도식 (농도·비율·개수 배분)
 *  args: { parts:[{label:"소금 6 g", value:6, fill:true}], total?:"소금물 100 g", rows?:[…] } */
function fnBar(a, o) {
  const rows = arr(a.rows).length ? arr(a.rows) : [{ parts: a.parts, total: a.total, name: a.name }];
  const W = o.width, pad = o.pad + 4, bh = 26, gap = 50;
  const H = 26 + rows.length * gap + 6;
  let s = svgOpen(W, H, o);
  rows.forEach((row, ri) => {
    const parts = arr(row.parts).map((p) => ({ ...p, v: Math.max(0, num(p.value, {}) ?? 1) }));
    if (!parts.length) return;
    const tot = parts.reduce((t, p) => t + p.v, 0) || 1;
    const y = 28 + ri * gap;
    const x0 = row.name ? pad + 44 : pad;
    if (row.name) s += T(pad, y + bh / 2 + 4, lab(row.name), { anchor: "start", size: 11, k: `row:${ri}` });
    let x = x0;
    parts.forEach((p, pi) => {
      const w = (W - pad - x0) * p.v / tot;
      s += `<rect data-k="part:${ri}-${pi}" x="${R2(x)}" y="${R2(y)}" width="${R2(w)}" height="${bh}" fill="${p.fill ? o.accent : "none"}" `
         + `${p.fill ? 'opacity="0.22"' : ""} stroke="currentColor" stroke-width="1.2"/>`;
      if (p.fill) s += `<rect x="${R2(x)}" y="${R2(y)}" width="${R2(w)}" height="${bh}" fill="none" stroke="${o.accent}" stroke-width="1.2"/>`;
      if (p.label) {
        if (w >= 30) s += T(x + w / 2, y + bh / 2 + 4, lab(p.label), { size: 10.5, k: `part-lbl:${ri}-${pi}` });
        else s += T(x + w / 2, y + bh + 12, lab(p.label), { size: 10 , op: .85, k: `part-lbl:${ri}-${pi}` });
      }
      x += w;
    });
    if (row.total) {
      s += L(x0, y - 8, W - pad, y - 8, { w: .9, op: .55 });
      s += L(x0, y - 11, x0, y - 5, { w: .9, op: .55 });
      s += L(W - pad, y - 11, W - pad, y - 5, { w: .9, op: .55 });
      s += T((x0 + W - pad) / 2, y - 13, lab(row.total), { size: 10.5, op: .8, k: `total:${ri}` });
    }
  });
  return s + "</svg>";
}

/** vessel — 용기에 담긴 액체 (해설 전용). 농도·물탱크·원기둥에 물 채우기.
 *  { kind: "beaker"|"cylinder"|"tank", capacity, rows: [{ name, total, parts: [{label, value, kind: "water"|"salt"|"other"}] }] }
 *  원칙(Park, 09-07): 농도는 막대가 아니라 **컵(또는 실린더)** 로 보여야 하고, 물은 푸른색·소금(용질)은 붉은색.
 *  용기는 모두 같은 크기, 담긴 양이 많을수록 높이 차오른다. 소금은 바닥에 얇게 가라앉은 층(최소 두께 보장). */
const LIQUID = { water: { fill: "#3b82c4", op: 0.28, stroke: "#2f6fa8" }, salt: { fill: "#d1495b", op: 0.6, stroke: "#b23a4a" }, other: { fill: "#8a8a8a", op: 0.3, stroke: "#777" } };
function liquidKind(p) {
  const k = String(p.kind || "").toLowerCase();
  if (k in LIQUID) return k;
  const t = String(p.label || "");
  if (/소금|설탕|용질|salt|sugar/.test(t) || p.fill) return "salt";
  if (/물|water|액|용액/.test(t)) return "water";
  return "other";
}
function fnVessel(a, o) {
  const rows = arr(a.rows).length ? arr(a.rows) : [{ parts: a.parts, total: a.total, name: a.name }];
  const n = rows.length;
  if (!n) return null;
  const kind = String(a.kind || "beaker").toLowerCase();
  const W = o.width, pad = o.pad + 4;
  const top = 34, vh = 108, bottom = 30, H = top + vh + bottom;
  const gap = 18;
  const vw = Math.min(96, (W - 2 * pad - gap * (n - 1)) / n);
  const totalW = n * vw + (n - 1) * gap;
  const x00 = (W - totalW) / 2;
  const parsed = rows.map((row) => {
    const parts = arr(row.parts).map((p) => ({ ...p, v: Math.max(0, num(p.value, {}) ?? 0), kind: liquidKind(p) }));
    return { row, parts, tot: parts.reduce((t, p) => t + p.v, 0) };
  });
  const cap = Math.max(num(a.capacity, {}) ?? 0, ...parsed.map((r) => r.tot)) || 1;
  const ry = kind === "cylinder" ? Math.max(5, vw * 0.14) : 0;      // 실린더 윗면 타원
  let s = svgOpen(W, H, o);
  parsed.forEach(({ row, parts, tot }, ri) => {
    const x = x00 + ri * (vw + gap), yb0 = top + vh;                  // yb0 = 용기 바닥(그림)
    const yb = yb0 - ry;                                                // 액체 기둥의 바닥(실린더는 바닥 타원 중심)
    const inner = vh - 2 * ry - 6;                                      // 담을 수 있는 높이
    // 액체 — 아래(소금 등 침전)부터 쌓는다. 소금 층은 최소 6px.
    const order = [...parts].sort((p, q) => (p.kind === "salt" ? -1 : 0) - (q.kind === "salt" ? -1 : 0));
    const hs = order.map((p) => inner * p.v / cap);
    order.forEach((p, i) => { if (p.kind === "salt" && p.v > 0 && hs[i] < 6) hs[i] = 6; });
    let y = yb;
    order.forEach((p, i) => {
      const h = hs[i], pi = parts.indexOf(p);
      if (h <= 0) return;
      const c = LIQUID[p.kind];
      y -= h;
      if (kind === "cylinder" && i === 0) s += `<ellipse cx="${R2(x + vw / 2)}" cy="${R2(yb)}" rx="${R2(vw / 2)}" ry="${R2(ry)}" fill="${c.fill}" opacity="${c.op}"/>`;   // 바닥 타원까지 채움
      s += `<rect data-k="part:${ri}-${pi}" x="${R2(x)}" y="${R2(y)}" width="${R2(vw)}" height="${R2(h)}" fill="${c.fill}" opacity="${c.op}"/>`;
      if (kind === "cylinder") s += `<ellipse cx="${R2(x + vw / 2)}" cy="${R2(y)}" rx="${R2(vw / 2)}" ry="${R2(ry)}" fill="${c.fill}" opacity="${c.op + 0.15}"/>`;   // 액면
      else s += L(x, y, x + vw, y, { stroke: c.stroke, w: 1.1, op: 0.9 });
      if (p.label) {
        const txt = lab(p.label);
        if (p.kind === "salt") s += T(x + vw / 2, yb0 + 14, txt, { size: 10, fill: LIQUID.salt.stroke, k: `part-lbl:${ri}-${pi}` });
        else if (h >= 16) s += T(x + vw / 2, y + h / 2 + 4 + (kind === "cylinder" ? ry / 2 : 0), txt, { size: 10.5, k: `part-lbl:${ri}-${pi}` });
        else s += T(x + vw + 4, y + h / 2 + 4, txt, { size: 10, anchor: "start", op: .85, k: `part-lbl:${ri}-${pi}` });
      }
    });
    // 용기
    if (kind === "cylinder") {
      s += PATH(`M${R2(x)} ${R2(top + ry)} L${R2(x)} ${R2(yb)} A${R2(vw / 2)} ${R2(ry)} 0 0 0 ${R2(x + vw)} ${R2(yb)} L${R2(x + vw)} ${R2(top + ry)}`, { w: 1.4, k: `vessel:${ri}` });
      s += `<ellipse data-k="vessel-top:${ri}" cx="${R2(x + vw / 2)}" cy="${R2(top + ry)}" rx="${R2(vw / 2)}" ry="${R2(ry)}" fill="none" stroke="currentColor" stroke-width="1.1" opacity=".7"/>`;
    } else if (kind === "tank") {
      s += `<rect data-k="vessel:${ri}" x="${R2(x)}" y="${R2(top)}" width="${R2(vw)}" height="${R2(vh)}" fill="none" stroke="currentColor" stroke-width="1.4"/>`;
    } else {                                                            // beaker — 위가 열린 컵, 살짝 벌어진 입
      s += PATH(`M${R2(x - 3)} ${R2(top)} L${R2(x)} ${R2(top + 8)} L${R2(x)} ${R2(yb0)} L${R2(x + vw)} ${R2(yb0)} L${R2(x + vw)} ${R2(top + 8)} L${R2(x + vw + 3)} ${R2(top)}`, { w: 1.4, k: `vessel:${ri}` });
    }
    if (row.name) s += T(x + vw / 2, top - 18, lab(row.name), { size: 11.5, k: `row:${ri}` });
    if (row.total) s += T(x + vw / 2, top - 5, lab(row.total), { size: 10, op: .75, k: `total:${ri}` });
  });
  return s + "</svg>";
}

/** steps — 식 변형을 줄 맞춰 보여주는 판 (해설 전용, 그림이 아니라 판서) */
function fnSteps(a, o) {
  const lines = arr(a.lines).filter((l) => l != null && l !== "");
  if (!lines.length) return null;
  // 판서 줄은 손으로 쓴 표기 그대로 — 분수는 상하(분자/분모)로 (renderHtml 이 이스케이프까지 한다)
  const showH = (t) => renderHtml(t == null ? "" : String(t));
  const render = (ln, i) => {
    const text = typeof ln === "string" ? ln : (ln.text || "");
    let html = showH(text);
    const marks = typeof ln === "object" ? arr(ln.marks) : [];
    marks.forEach((m, j) => {
      const on = showH(m.on);
      if (!on || !html.includes(on)) return;
      const note = m.note ? `<sup class="fig-note-sup" style="color:${o.accent};font-size:.72em;margin-left:2px">${showH(m.note)}</sup>` : "";
      const cls = m.strike ? "fig-mk fig-strike" : "fig-mk";
      html = html.replace(on, `<span class="${cls}" data-k="mark:${i}-${j}">${on}${note}</span>`);
    });
    const hint = typeof ln === "object" && ln.hint
      ? `<span class="fig-hint" data-k="hint:${i}" style="display:block;font-size:.8em;color:${o.accent};opacity:.85;margin:-2px 0 2px 0">${showH(ln.hint)}</span>` : "";
    return `<div class="fig-line" data-k="line:${i}">${hint}${html}</div>`;
  };
  return `<div class="fig-steps" style="border-left:3px solid currentColor;padding:4px 0 4px 10px;opacity:.95;`
       + `font-size:13px;line-height:1.75;font-variant-numeric:tabular-nums">` + lines.map(render).join("") + `</div>`;
}

// ---------------------------------------------------------------- point / image
function fnPoint(a, o) {
  const c = pt({ x: a.x, y: a.y }, {});
  if (!c) return null;
  const m = Math.max(2, Math.abs(c[0]), Math.abs(c[1])) + 1;
  const f = frame([-m, m], [-m, m], o, { aspect: 0.8 });
  let s = svgOpen(f.W, f.H, o) + axes(f, o, { grid: true });
  s += DOT(f.X(c[0]), f.Y(c[1]), { r: 3.4, fill: o.accent, stroke: o.accent });
  s += T(f.X(c[0]) + 7, f.Y(c[1]) - 6, `(${R2(c[0])}, ${R2(c[1])})`, { anchor: "start", size: 10.5 });
  return s + "</svg>";
}

function fnImage(a, o) {
  const src = a.src ? (o.assetUrl ? o.assetUrl(a.src) : null) : null;
  if (!src) return note(a.raw, "이미지 자산 미연결 — 원본은 코퍼스 전용");
  return `<figure style="margin:0"><img src="${esc(src)}" alt="${esc(lab(a.raw).slice(0, 120))}" `
       + `style="max-width:100%;height:auto;border-radius:6px"/>`
       + `<figcaption style="font-size:11px;opacity:.6;margin-top:2px">코퍼스 원본 이미지 — 서비스 노출 금지</figcaption></figure>`;
}

// ---------------------------------------------------------------- 디스패처
const RENDER = {
  numline: fnNumline, coordplane: fnCoordplane, funcgraph: fnFuncgraph, scene: fnScene,
  tri: fnTri, rect: fnRect, circle: fnCircle, sector: fnSector,
  quad: (a, o) => fnPolygonLike(a, o, 4), polygon: (a, o) => fnPolygonLike(a, o, null),
  trapezoid: (a, o) => fnPolygonLike({ ...a, n: 4 }, o, 4),
  crossing: fnCrossing, parallel: fnParallel,
  table: (a) => fnTable(a), hist: fnHist, scatter: fnScatter,
  stemleaf: (a) => fnStemleaf(a), boxplot: fnBoxplot,
  venn: fnVenn, tree: fnTree, solid: fnSolid, net: fnNet, wire: fnWire, point: fnPoint, image: fnImage,
  journey: fnJourney, passing: fnPassing, river: fnRiver, mountain: fnMountain, bar: fnBar, vessel: fnVessel, steps: fnSteps,
  unitcircle: (a, o) => fnCircle({ r: 1, ...a }, o),
  conic: (a, o) => (a.expr ? fnCoordplane({ x: [-6, 6], y: [-6, 6], lines: [a.expr], points: [] }, o) : null),
};

/** 도형 하나 → { kind, html, warnings } */
export function figureToHtml1(fig, opts = {}) {
  const o = { ...DEF, ...opts };
  const warnings = [];
  if (!fig || typeof fig !== "object") return { kind: "note", html: note("", "도형 자료 없음"), warnings: ["빈 도형"] };
  const fn = String(fig.fn || "").trim();
  const a = (fig.args && typeof fig.args === "object") ? fig.args : {};
  if (fn === "unsupported") return { kind: "note", html: note(a.raw ?? fig.raw, null), warnings: [] };
  const r = RENDER[fn];
  if (!r) {
    warnings.push(`미지 도형 함수 ${fn}`);
    return { kind: "note", html: note(a.raw ?? a.description ?? "", `미지원 도형 ${fn}`), warnings };
  }
  let out = null;
  try { out = r(a, o); }
  catch (e) { warnings.push(`${fn} 렌더 예외: ${e && e.message}`); out = null; }
  if (!out) {
    warnings.push(`${fn} 인자로는 그릴 수 없음`);
    const desc = a.raw ?? a.description ?? a.note ?? "";
    return { kind: "note", html: note(desc || `${fn}(${Object.keys(a).join(", ")})`, `${fn} — 그릴 수 있는 인자 부족`), warnings };
  }
  return { kind: out.startsWith("<svg") ? "svg" : "html", html: out, warnings };
}

/** 도형 배열 → HTML 문자열 (앱·검수 화면 공용 진입점) */
export function figureToHtml(figList, opts = {}) {
  const list = Array.isArray(figList) ? figList : (figList ? [figList] : []);
  if (!list.length) return "";
  return `<div class="fig-wrap" style="display:flex;flex-wrap:wrap;gap:10px;align-items:flex-start">`
       + list.map((f) => `<div class="fig-item">${figureToHtml1(f, opts).html}</div>`).join("")
       + `</div>`;
}

/** 검수용 — 그릴 수 있는지와 경고만 (렌더 결과는 버림) */
export function figureAudit(figList, opts = {}) {
  const list = Array.isArray(figList) ? figList : (figList ? [figList] : []);
  return list.map((f, i) => {
    const r = figureToHtml1(f, opts);
    return { i, fn: f && f.fn, kind: r.kind, ok: r.kind !== "note", warnings: r.warnings };
  });
}

export default { figureToHtml, figureToHtml1, figureAudit, num, rng, pt, lab, esc };
