// ashrain.out — 교실 모니터 장면 엔진: 그리기 부품 (draw.jsx)
// 팔레트 · 글자 재기 · 수식 글자(이탤릭 변수·세로 분수·강조) · 판서 · 자막 · 각 표시 · 입체 면 그리기.
// 무대 좌표는 1600×900 (16:9). 장면 함수가 이 부품들로 <g> 를 만든다.
import { Fragment } from "react";
import {
  clamp, lerp, seg, win, E, polar, arcPts, pathOf, partial, sub2, add2, mul2, len2, rad,
  lambert, shade, centroid3, normal3, facing,
} from "./core";

export const W = 1600, H = 900;

/* ══════════ 팔레트 ══════════ */
// 다크 = 남색 종이(개념 무대와 같은 계열), 라이트 = 한지. 그림 색은 두 판(초등·중등)이 같이 쓴다.
export const PALETTE = {
  dark: {
    name: "dark",
    bg: ["#2a3762", "#1c2647", "#121a33"],
    ink: "#F2E8D0", soft: "#B8B0A0", faint: "rgba(242,232,208,0.16)", grid: "rgba(242,232,208,0.10)",
    halo: "#18213e", paper: "#1c2647",
    gold: "#F4C65A", coral: "#F2877B", teal: "#6BD3C3", sky: "#8FB9F6", lilac: "#C6A8F6", leaf: "#A6D886",
    wood: "#E3B57A", woodEdge: "#5B3A1A",
    card: "#2c3a68", cardEdge: "rgba(242,232,208,0.38)",
    red: "#F2685C", blue: "#6EA6F5", yellow: "#F5CF4E",
    capBg: "rgba(8,12,27,0.58)", capInk: "#F5ECD5",
    bar: "#F4C65A", fillA: 0.42,
  },
  light: {
    name: "light",
    bg: ["#fcf8ee", "#f3ead6", "#e6d9bb"],
    ink: "#3B3021", soft: "#7B6C55", faint: "rgba(59,48,33,0.16)", grid: "rgba(59,48,33,0.10)",
    halo: "#f4ecd9", paper: "#f3ead6",
    gold: "#B37A0E", coral: "#C34E3E", teal: "#13877A", sky: "#2D65B2", lilac: "#7550BC", leaf: "#478A28",
    wood: "#D9A867", woodEdge: "#6B4720",
    card: "#fffaf0", cardEdge: "rgba(59,48,33,0.32)",
    red: "#D2463A", blue: "#2F6FC4", yellow: "#E0AC12",
    capBg: "rgba(255,251,241,0.80)", capInk: "#3B3021",
    bar: "#B37A0E", fillA: 0.36,
  },
};

/* ══════════ 글꼴·글자 재기 ══════════ */
export const SANS = "'Pretendard Variable', Pretendard, 'Noto Sans KR', 'Malgun Gothic', system-ui, sans-serif";
export const SERIF = "'Times New Roman', 'Liberation Serif', 'Noto Serif', serif";
export const TITLE = "'EBS Hunminjeongeum Saeron', 'Gowun Batang', serif";

const fontStr = (size, weight, italic, serif) =>
  `${italic ? "italic " : ""}${weight} ${size}px ${serif ? SERIF : SANS}`;

// 브라우저 = 캔버스로 정확히, 그 밖(검산 렌더) = setMeasurer 로 주입하거나 추정치
let measurer = null;
const wcache = new Map();
export function setMeasurer(fn) { measurer = fn; wcache.clear(); }
export function clearMeasureCache() { wcache.clear(); layoutCache.clear(); }
function estimate(s, size, italic, serif) {
  let w = 0;
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (c >= 0xac00 && c <= 0xd7a3) w += 0.93;
    else if (ch === " ") w += 0.25;
    else if (/[0-9]/.test(ch)) w += 0.58;
    else if (/[a-z]/.test(ch)) w += serif ? 0.46 : 0.52;
    else if (/[A-Z]/.test(ch)) w += serif ? 0.64 : 0.66;
    else if ("²³°".includes(ch)) w += 0.38;
    else if ("()[],.:".includes(ch)) w += 0.32;
    else if ("×÷+−=<>".includes(ch)) w += 0.66;
    else if (ch === "π") w += 0.56;
    else w += 0.7;
  }
  return w * size;
}
export function textW(s, size, weight = 500, italic = false, serif = false) {
  const key = `${s}\u0001${size}\u0001${weight}\u0001${italic}\u0001${serif}`;
  const hit = wcache.get(key);
  if (hit != null) return hit;
  if (!measurer && typeof document !== "undefined") {
    try {
      const g = document.createElement("canvas").getContext("2d");
      // 캔버스를 못 쓰는 환경(드물게 null)이면 추정치로 — 화면이 죽지 않게
      measurer = g ? (str, sz, wt, it, sf) => { g.font = fontStr(sz, wt, it, sf); return g.measureText(str).width; }
        : (str, sz, wt, it, sf) => estimate(str, sz, it, sf);
    } catch { measurer = (str, sz, wt, it, sf) => estimate(str, sz, it, sf); }
  }
  const w = measurer ? measurer(s, size, weight, italic, serif) : estimate(s, size, italic, serif);
  wcache.set(key, w);
  return w;
}

/* ══════════ 수식 글자 ══════════ */
// 표기: ‹강조› · {분자/분모} · *S*(대문자 이탤릭) · 홀로 선 소문자 라틴 글자와 π 는 자동 이탤릭(세리프).
//       cm, cm² 처럼 붙은 글자는 바로 선다. ² ³ 은 유니코드 위 첨자를 그대로 쓴다.
//       ⟪아이콘⟫ — 글꼴에 없을 수 있는 기호는 그림으로: ⟪○⟫ ⟪△⟫ ⟪□⟫ ⟪●⟫ ⟪✓⟫ ⟪×⟫, 주사위 눈 ⟪d1⟫~⟪d6⟫.
//       뒤에 색 글자를 붙이면 칠한다(r 빨강 · b 파랑 · y 노랑 · g 초록 · p 보라 · t 청록 · k 글자색): ⟪○r⟫ ⟪●b⟫
const ICON_KIND = { "○": "circle", "△": "tri", "□": "square", "●": "dot", "✓": "check", "×": "cross" };
export const ICON_COLOR = { r: "red", b: "blue", y: "yellow", g: "leaf", p: "lilac", t: "teal", k: "ink", o: "coral", s: "sky" };
function parseIcon(s) {
  if (/^d[1-6]/.test(s)) return { kind: "die", n: Number(s[1]), color: s[2] || null };
  return { kind: ICON_KIND[s[0]] || "circle", color: s[1] || null };
}
function runs(s, accent) {
  const out = [];
  let buf = "";
  const flush = () => { if (buf) { out.push({ s: buf, it: false, ac: accent }); buf = ""; } };
  const isLat = (ch) => !!ch && /[A-Za-z]/.test(ch);
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === "*") {
      const j = s.indexOf("*", i + 1);
      if (j > i) { flush(); out.push({ s: s.slice(i + 1, j), it: true, ac: accent }); i = j; continue; }
    }
    if (ch === "π" || (/[a-z]/.test(ch) && !isLat(s[i - 1]) && !isLat(s[i + 1]))) {
      flush(); out.push({ s: ch, it: true, ac: accent }); continue;
    }
    buf += ch;
  }
  flush();
  return out;
}
export function parseMath(str) {
  const toks = [];
  let accent = false, buf = "";
  const flush = () => { if (buf) { toks.push(...runs(buf, accent)); buf = ""; } };
  for (let i = 0; i < str.length; i++) {
    const ch = str[i];
    if (ch === "‹") { flush(); accent = true; continue; }
    if (ch === "›") { flush(); accent = false; continue; }
    if (ch === "⟪") {
      const j = str.indexOf("⟫", i + 1);
      if (j > i) { flush(); toks.push({ icon: parseIcon(str.slice(i + 1, j)), ac: accent }); i = j; continue; }
    }
    if (ch === "{") {
      const j = str.indexOf("}", i + 1), inner = str.slice(i + 1, j), k = inner.indexOf("/");
      if (j > i && k >= 0) {
        flush();
        toks.push({ frac: true, ac: accent, num: runs(inner.slice(0, k), accent), den: runs(inner.slice(k + 1), accent) });
        i = j; continue;
      }
    }
    buf += ch;
  }
  flush();
  return toks;
}
const layoutCache = new Map();
const runW = (r, size, weight) => textW(r.s, size, r.it ? 500 : weight, r.it, r.it);
/** 수식 한 줄의 배치 — [{s, x, dy, size, it, ac} | {bar:[x1,x2], dy}] 와 전체 폭 */
export function layoutMath(str, size, weight = 500) {
  const key = `${str}\u0001${size}\u0001${weight}`;
  const hit = layoutCache.get(key);
  if (hit) return hit;
  const toks = parseMath(String(str ?? ""));
  const items = [];
  let x = 0;
  const fs = size * 0.72, axis = -size * 0.31;
  for (const t of toks) {
    if (t.icon) {
      items.push({ icon: t.icon, x: x + size * 0.06, w: size * 0.82, size, ac: t.ac });
      x += size * 0.94;
      continue;
    }
    if (!t.frac) {
      const w = runW(t, size, weight);
      items.push({ s: t.s, x, dy: 0, size, it: t.it, ac: t.ac, w });
      x += w + (t.it ? size * 0.04 : 0);
      continue;
    }
    const nw = t.num.reduce((a, r) => a + runW(r, fs, weight), 0);
    const dw = t.den.reduce((a, r) => a + runW(r, fs, weight), 0);
    const fw = Math.max(nw, dw) + size * 0.16, x0 = x + size * 0.08;
    let nx = x0 + (fw - nw) / 2;
    for (const r of t.num) { const w = runW(r, fs, weight); items.push({ s: r.s, x: nx, dy: axis - size * 0.13, size: fs, it: r.it, ac: t.ac || r.ac, w }); nx += w; }
    let dx = x0 + (fw - dw) / 2;
    for (const r of t.den) { const w = runW(r, fs, weight); items.push({ s: r.s, x: dx, dy: axis + size * 0.13 + fs * 0.72, size: fs, it: r.it, ac: t.ac || r.ac, w }); dx += w; }
    items.push({ bar: [x0, x0 + fw], dy: axis, ac: t.ac });
    x = x0 + fw + size * 0.08;
  }
  const out = { items, w: x };
  layoutCache.set(key, out);
  return out;
}

/**
 * 수식 글자. anchor: start | middle | end. halo: 글자 뒤 바탕색 테두리(그림 위에서 읽히게).
 */
export function MText({ x, y, s, size = 40, weight = 500, anchor = "start", fill, accent, halo, opacity = 1, C }) {
  if (s == null || s === "" || opacity <= 0.001) return null;
  const L = layoutMath(s, size, weight);
  const x0 = anchor === "middle" ? x - L.w / 2 : anchor === "end" ? x - L.w : x;
  const col = fill || C?.ink || "#fff", acc = accent || C?.gold || col;
  const hs = halo ? { paintOrder: "stroke", stroke: halo, strokeWidth: size * 0.2, strokeLinejoin: "round" } : null;
  return (
    <g opacity={opacity}>
      {L.items.map((it, i) => it.icon
        ? <ShapeIcon key={i} kind={it.icon.kind} n={it.icon.n} cx={x0 + it.x + it.w / 2} cy={y - it.size * 0.34} r={it.size * 0.34}
            fill={it.icon.color && C ? C[ICON_COLOR[it.icon.color]] : null} stroke={it.ac ? acc : col} C={C} />
        : it.bar
        ? <line key={i} x1={x0 + it.bar[0]} x2={x0 + it.bar[1]} y1={y + it.dy} y2={y + it.dy}
            stroke={it.ac ? acc : col} strokeWidth={Math.max(2, size * 0.055)} strokeLinecap="round" />
        : <text key={i} x={x0 + it.x} y={y + it.dy} fontSize={it.size}
            fontFamily={it.it ? SERIF : SANS} fontStyle={it.it ? "italic" : undefined}
            fontWeight={it.it ? 500 : weight} fill={it.ac ? acc : col} xmlSpace="preserve"
            style={hs ? { ...hs, whiteSpace: "pre" } : PRE}>{it.s}</text>)}
    </g>
  );
}
export const mathWidth = (s, size = 40, weight = 500) => layoutMath(s, size, weight).w;
const PRE = { whiteSpace: "pre" };

/** 그림 위의 이름표 — 바탕 테두리로 선 위에서도 읽힌다 */
export function Lbl({ x, y, s, size = 34, anchor = "middle", fill, weight = 600, o = 1, C }) {
  return <MText x={x} y={y + size * 0.34} s={s} size={size} anchor={anchor} weight={weight}
    fill={fill || C.ink} halo={C.halo} opacity={o} C={C} />;
}

/* ══════════ 판서 ══════════ */
/**
 * 오른쪽(또는 지정 위치) 판서. lines: [{ t, s, u?, row?, k? }]
 *   t 나타나는 시각 · u 사라지는 시각 · row 줄 번호(같은 줄은 덮어쓴다) · k:"h" 작은 머리글
 *   가장 최근에 나타난 줄이 금빛 막대와 함께 또렷하고, 이전 줄은 조금 흐려진다.
 */
export function Board({ x, y, t, lines, C, size = 40, lh = 64, hsize, dim = 0.62 }) {
  const vis = lines.map((L, i) => ({ ...L, row: L.row ?? i })).filter((L) => t >= L.t && (L.u == null || t < L.u));
  let cur = null;
  for (const L of vis) if (!cur || L.t >= cur.t) cur = L;
  const hs = hsize || Math.round(size * 0.72);
  return (
    <g>
      {vis.map((L, i) => {
        const a = win(t, L.t, L.u ?? Infinity, 420, 320);
        const isCur = L === cur;
        const yy = y + L.row * lh + (1 - seg(t, L.t, L.t + 420, E.out)) * 12;
        const head = L.k === "h";
        return (
          <g key={i} opacity={a * (isCur || head ? 1 : 1 - (1 - dim) * seg(t, cur.t, cur.t + 500))}>
            {isCur && !head && <rect x={x - 22} y={yy - size * 0.95} width={6} height={size * 1.15} rx={3} fill={C.bar} />}
            {L.dot && <circle cx={x + size * 0.32} cy={yy - size * 0.36} r={size * 0.24} fill={C[L.dot] || L.dot} />}
            <MText x={x + (L.dot ? size * 0.8 : 0)} y={yy} s={L.s} size={head ? hs : (L.size || size)} weight={head ? 600 : 560}
              fill={head ? C.soft : C.ink} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/* ══════════ 자막 ══════════ */
/** caps: [{ t, s, u? }] — 마지막으로 나타난 한 줄을 화면 아래 가운데에 */
export function Caption({ t, caps, C, y = 846, size = 38 }) {
  const live = caps.filter((c) => t >= c.t && (c.u == null || t < c.u));
  if (!live.length) return null;
  const out = [];
  const last = live[live.length - 1];
  const prev = live.length > 1 ? live[live.length - 2] : null;
  const k = seg(t, last.t, last.t + 560, E.lin);         // 앞 자막이 먼저 사라지고 새 자막이 뜬다(겹쳐 읽히지 않게)
  const one = (c, o, key) => {
    const w = mathWidth(c.s, size, 560);
    const a = o * (c.u != null ? 1 - seg(t, c.u - 320, c.u, E.sine) : 1);
    return (
      <g key={key} opacity={a}>
        <rect x={800 - w / 2 - 26} y={y - size * 1.02} width={w + 52} height={size * 1.48} rx={size * 0.5} fill={C.capBg} />
        <MText x={800} y={y} s={c.s} size={size} weight={560} anchor="middle" fill={C.capInk} C={C} />
      </g>
    );
  };
  if (prev && k < 0.5) out.push(one(prev, E.sine(1 - 2 * k), "p"));
  out.push(one(last, prev ? E.sine(Math.max(0, 2 * k - 1)) : E.sine(k), "c"));
  return <g>{out}</g>;
}

/* ══════════ 2D 도형 부품 ══════════ */
export function Path({ pts, closed, stroke, sw = 4, fill = "none", fo = 1, dash, o = 1, cap = "round" }) {
  if (!pts || pts.length < 2 || o <= 0.001) return null;
  return <path d={pathOf(pts, closed)} fill={fill} fillOpacity={fo} stroke={stroke || "none"} strokeWidth={sw}
    strokeDasharray={dash} strokeLinecap={cap} strokeLinejoin="round" opacity={o} />;
}
/** 선이 그려지며 나타남: p = 0~1 */
export function Draw({ pts, p = 1, closed, ...rest }) {
  if (p <= 0) return null;
  return <Path pts={partial(pts, p, closed)} closed={closed && p >= 1} {...rest} />;
}
/** 화살표 p → q (머리 크기 h) */
export function Arrow({ p, q, stroke, sw = 4, h = 16, o = 1, dash }) {
  if (o <= 0.001) return null;
  const a = Math.atan2(q[1] - p[1], q[0] - p[0]);
  const hd = [[q[0] - h * Math.cos(a - 0.45), q[1] - h * Math.sin(a - 0.45)], q, [q[0] - h * Math.cos(a + 0.45), q[1] - h * Math.sin(a + 0.45)]];
  const tail = [q[0] - h * 0.6 * Math.cos(a), q[1] - h * 0.6 * Math.sin(a)];
  return (
    <g opacity={o}>
      <Path pts={[p, tail]} stroke={stroke} sw={sw} dash={dash} />
      <Path pts={hd} closed fill={stroke} stroke={stroke} sw={2} />
    </g>
  );
}
/** 은은한 형광펜 번짐 */
export function Glow({ pts, closed, C, o = 1, sw = 16 }) {
  if (o <= 0.01) return null;
  return <Path pts={pts} closed={closed} stroke={C.gold} sw={sw} o={0.28 * o} />;
}
export function Dot({ p, r = 7, fill, o = 1, ring }) {
  if (o <= 0.001) return null;
  return <circle cx={p[0]} cy={p[1]} r={r} fill={fill} opacity={o} stroke={ring} strokeWidth={ring ? 3 : 0} />;
}
/** 꼭짓점 V 에서 A·B 방향 사이의 각 표시(작은 쪽). label 이 있으면 이등분선 위에 */
export function Angle({ V, A, B, r = 46, C, color, p = 1, label, lsize = 32, lr, fillO = 0.18, sw = 3.5 }) {
  if (p <= 0) return null;
  const aA = Math.atan2(-(A[1] - V[1]), A[0] - V[0]) * 180 / Math.PI;
  const aB = Math.atan2(-(B[1] - V[1]), B[0] - V[0]) * 180 / Math.PI;
  let d = aB - aA;
  while (d > 180) d -= 360;
  while (d < -180) d += 360;
  const col = color || C.gold;
  const arc = arcPts(V, r, aA, aA + d * p);
  const mid = aA + d / 2;
  const lp = polar(V, lr || r + lsize * 0.95, mid);
  return (
    <g>
      <Path pts={[V, ...arc]} closed fill={col} fo={fillO} stroke="none" />
      <Path pts={arc} stroke={col} sw={sw} />
      {label && p >= 1 && <Lbl x={lp[0]} y={lp[1]} s={label} size={lsize} fill={col} C={C} />}
    </g>
  );
}
/** 직각 표시 */
export function RightMark({ V, A, B, s = 22, C, color, o = 1 }) {
  const u = mul2(sub2(A, V), 1 / len2(sub2(A, V))), w = mul2(sub2(B, V), 1 / len2(sub2(B, V)));
  const p1 = add2(V, mul2(u, s)), p2 = add2(p1, mul2(w, s)), p3 = add2(V, mul2(w, s));
  return <Path pts={[p1, p2, p3]} stroke={color || C.ink} sw={2.5} o={o} />;
}
/** 같은 길이 표시(눈금 n 개) */
export function Ticks({ A, B, n = 1, C, color, o = 1, s = 13 }) {
  const m = mul2(add2(A, B), 0.5), d = sub2(B, A), L = len2(d), u = [d[0] / L, d[1] / L], nrm = [-u[1], u[0]];
  const out = [];
  for (let i = 0; i < n; i++) {
    const c = add2(m, mul2(u, (i - (n - 1) / 2) * 9));
    out.push(<Path key={i} pts={[add2(c, mul2(nrm, s)), add2(c, mul2(nrm, -s))]} stroke={color || C.ink} sw={3} o={o} />);
  }
  return <g>{out}</g>;
}
/** 치수선: A→B 를 법선 방향으로 off 만큼 띄워 양 끝 눈금 + 가운데 이름표 */
export function Dim({ A, B, off = 34, s, C, color, o = 1, size = 32, lofs = 30, at = 0.5 }) {
  if (o <= 0.001) return null;
  const d = sub2(B, A), L = len2(d), u = [d[0] / L, d[1] / L], nrm = [u[1], -u[0]];
  const a = add2(A, mul2(nrm, off)), b = add2(B, mul2(nrm, off));
  const col = color || C.soft;
  const m = add2(add2(a, mul2(sub2(b, a), at)), mul2(nrm, lofs));
  return (
    <g opacity={o}>
      <Path pts={[a, b]} stroke={col} sw={2.5} />
      <Path pts={[add2(a, mul2(nrm, 10)), add2(a, mul2(nrm, -10))]} stroke={col} sw={2.5} />
      <Path pts={[add2(b, mul2(nrm, 10)), add2(b, mul2(nrm, -10))]} stroke={col} sw={2.5} />
      {s && <Lbl x={m[0]} y={m[1]} s={s} size={size} fill={col === C.soft ? C.ink : col} C={C} />}
    </g>
  );
}

/* ══════════ 입체 면 그리기 ══════════ */
/**
 * faces: [{ pts: [[x,y,z],…], color, o?(불투명도 0~1), edge?, sw?, n?(바깥 법선), hidden?:"dash"|"skip", key }]
 *   깊이(먼 것부터) 순으로 그린다. 바깥 법선이 뒤를 보는 면은 점선 모서리(교과서 규약)로.
 */
export function Faces({ cam, faces, C, fillO = 0.86, sw = 3, edge, backDash = true, backO = 0.5, light = true }) {
  const items = faces.map((f, i) => {
    const P = f.pts.map((q) => cam.p(q));
    const n = f.n || normal3(f.pts);
    const front = facing(cam, n);
    const depth = P.reduce((a, q) => a + q[2], 0) / P.length;
    return { f, P, n, front, depth, i };
  });
  items.sort((a, b) => b.depth - a.depth || a.i - b.i);
  return (
    <g>
      {items.map(({ f, P, n, front, i }) => {
        if (!front && f.hidden === "skip") return null;
        const k = light ? lambert(cam, n) : 1;
        const back = !front && backDash;
        const o = f.o ?? 1;
        return (
          <path key={f.key ?? i} d={pathOf(P, true)}
            fill={f.color ? shade(f.color, k) : "none"} fillOpacity={(back ? fillO * 0.35 : fillO) * o}
            stroke={f.edge || edge || C.ink} strokeWidth={f.sw || sw} strokeLinejoin="round"
            strokeDasharray={back ? "9 8" : undefined} strokeOpacity={(back ? backO : 1) * (f.eo ?? 1) * o} />
        );
      })}
    </g>
  );
}

/** 3D 꺾은선(모서리·호) */
export function Path3({ cam, pts, ...rest }) {
  return <Path pts={pts.map((q) => cam.p(q))} {...rest} />;
}
export function Lbl3({ cam, p, ...rest }) {
  const q = cam.p(p);
  return <Lbl x={q[0]} y={q[1]} {...rest} />;
}

/* ══════════ 모양 아이콘 · 주사위 · 표 ══════════ */
const DIE_PIPS = {
  1: [[0, 0]], 2: [[-1, -1], [1, 1]], 3: [[-1, -1], [0, 0], [1, 1]], 4: [[-1, -1], [1, -1], [-1, 1], [1, 1]],
  5: [[-1, -1], [1, -1], [0, 0], [-1, 1], [1, 1]], 6: [[-1, -1], [-1, 0], [-1, 1], [1, -1], [1, 0], [1, 1]],
};
/** 주사위 한 면 — 가운데 (cx, cy), 한 변 s */
export function DieFace({ cx, cy, s, n, C, fill, pip, edge, o = 1, rot = 0, sw }) {
  if (o <= 0.001) return null;
  const k = s * 0.27, pr = s * 0.095;
  return (
    <g opacity={o} transform={rot ? `rotate(${rot} ${cx} ${cy})` : undefined}>
      <rect x={cx - s / 2} y={cy - s / 2} width={s} height={s} rx={s * 0.2} fill={fill || C.card}
        stroke={edge || C.ink} strokeWidth={sw ?? Math.max(1.6, s * 0.045)} />
      {(DIE_PIPS[n] || []).map(([a, b], i) => <circle key={i} cx={cx + a * k} cy={cy + b * k} r={pr} fill={pip || (n === 1 ? C.red : C.ink)} />)}
    </g>
  );
}
/** 체크 표시(✓) */
export function Check({ cx, cy, r = 14, color, sw = 4, p = 1, o = 1 }) {
  if (p <= 0 || o <= 0.001) return null;
  const pts = [[cx - r * 0.55, cy + r * 0.02], [cx - r * 0.12, cy + r * 0.45], [cx + r * 0.62, cy - r * 0.5]];
  return <Path pts={partial(pts, p)} stroke={color} sw={sw} o={o} />;
}
/** 모양 아이콘: circle · tri · square · dot · check · cross · die */
export function ShapeIcon({ kind, cx, cy, r, fill, stroke, sw, C, n = 1, halo, o = 1 }) {
  if (o <= 0.001) return null;
  const w = sw ?? Math.max(2, r * 0.16);
  const f = fill || "none";
  const st = stroke || C?.ink;
  const hal = halo ? <circle cx={cx} cy={cy} r={r * 1.15} fill={halo} opacity={0.6} /> : null;
  if (kind === "die") return <g opacity={o}>{hal}<DieFace cx={cx} cy={cy} s={r * 1.9} n={n} C={C} fill={fill || C?.card} edge={st} sw={w * 0.8} /></g>;
  if (kind === "check") return <g opacity={o}><Check cx={cx} cy={cy} r={r} color={fill || st} sw={w * 1.3} /></g>;
  if (kind === "cross") return <g opacity={o}><Path pts={[[cx - r * 0.6, cy - r * 0.6], [cx + r * 0.6, cy + r * 0.6]]} stroke={fill || st} sw={w * 1.2} />
    <Path pts={[[cx + r * 0.6, cy - r * 0.6], [cx - r * 0.6, cy + r * 0.6]]} stroke={fill || st} sw={w * 1.2} /></g>;
  if (kind === "dot") return <circle cx={cx} cy={cy} r={r * 0.78} fill={fill || st} opacity={o} />;
  if (kind === "tri") {
    const R = r * 1.12, pts = [0, 1, 2].map((i) => polar([cx, cy + r * 0.14], R, 90 + i * 120));
    return <g opacity={o}>{hal}<Path pts={pts} closed fill={f} fo={fill ? 1 : 0} stroke={fill ? shadeEdge(fill) : st} sw={w} /></g>;
  }
  if (kind === "square") {
    const h = r * 0.86;
    return <g opacity={o}>{hal}<rect x={cx - h} y={cy - h} width={2 * h} height={2 * h} rx={r * 0.12} fill={f}
      stroke={fill ? shadeEdge(fill) : st} strokeWidth={w} /></g>;
  }
  return <g opacity={o}>{hal}<circle cx={cx} cy={cy} r={r * 0.92} fill={f} stroke={fill ? shadeEdge(fill) : st} strokeWidth={w} /></g>;
}
const shadeEdge = (hex) => (typeof hex === "string" && hex.startsWith("#") ? shade(hex, 0.72) : hex);

/**
 * 표. cols: 열 너비들, rh: 행 높이(수 또는 배열), rows: 행마다 칸 배열.
 * 칸: 문자열 | { s, t(나타나는 시각), fill, fo, color, cross(지움 표시 시각), hi(강조), size, weight }
 */
export function Table({ x, y, cols, rh, rows, C, t = 1e12, size = 30, o = 1, line }) {
  if (o <= 0.001) return null;
  const xs = [x]; for (const w of cols) xs.push(xs.at(-1) + w);
  const hs = rows.map((_, i) => (Array.isArray(rh) ? rh[i] : rh));
  const ys = [y]; for (const h of hs) ys.push(ys.at(-1) + h);
  const lc = line || C.soft;
  const cells = [];
  rows.forEach((row, r) => row.forEach((cell, c) => {
    if (cell == null) return;
    const cs = typeof cell === "string" || typeof cell === "number" ? { s: String(cell) } : cell;
    const x0 = xs[c], x1 = xs[c + 1], y0 = ys[r], y1 = ys[r + 1], cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const a = cs.t == null ? 1 : seg(t, cs.t, cs.t + 320, E.sine);
    const k = `${r}-${c}`;
    if (cs.fill) cells.push(<rect key={"f" + k} x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill={C[cs.fill] || cs.fill} fillOpacity={(cs.fo ?? 0.16) * (cs.fillT == null ? 1 : seg(t, cs.fillT, cs.fillT + 300))} />);
    if (cs.s != null && cs.s !== "" && a > 0) {
      const sz = cs.size || size;
      cells.push(<MText key={"s" + k} x={cx} y={cy + sz * 0.36} s={cs.s} size={sz} weight={cs.weight || 600} anchor="middle"
        fill={cs.color ? C[cs.color] || cs.color : C.ink} opacity={a} C={C} />);
    }
    if (cs.cross != null) {
      const p = seg(t, cs.cross, cs.cross + 380, E.out);
      if (p > 0) {
        const m = Math.min(x1 - x0, y1 - y0) * 0.26;
        cells.push(<g key={"x" + k} opacity={0.85}>
          <Path pts={partial([[cx - m, cy - m], [cx + m, cy + m]], Math.min(1, p * 2))} stroke={C.coral} sw={4} />
          {p > 0.5 && <Path pts={partial([[cx + m, cy - m], [cx - m, cy + m]], p * 2 - 1)} stroke={C.coral} sw={4} />}
        </g>);
      }
    }
    if (cs.hi != null) {
      const h = seg(t, cs.hi, cs.hi + 400, E.out) * (cs.hiU == null ? 1 : 1 - seg(t, cs.hiU, cs.hiU + 400));
      if (h > 0) cells.push(<rect key={"h" + k} x={x0 + 3} y={y0 + 3} width={x1 - x0 - 6} height={y1 - y0 - 6} rx={6}
        fill="none" stroke={C[cs.hiCol] || C.gold} strokeWidth={4} opacity={h} />);
    }
  }));
  return (
    <g opacity={o}>
      {cells.filter((c) => c.key.startsWith("f"))}
      {xs.map((xx, i) => <line key={"v" + i} x1={xx} x2={xx} y1={ys[0]} y2={ys.at(-1)} stroke={lc} strokeWidth={i === 0 || i === xs.length - 1 ? 2.6 : 1.6} />)}
      {ys.map((yy, i) => <line key={"h" + i} x1={xs[0]} x2={xs.at(-1)} y1={yy} y2={yy} stroke={lc} strokeWidth={i === 0 || i === ys.length - 1 ? 2.6 : 1.6} />)}
      {cells.filter((c) => !c.key.startsWith("f"))}
    </g>
  );
}

/* ══════════ 무대 머리글 ══════════ */
export function SceneTitle({ title, sub, C, mode }) {
  return (
    <g>
      <text x={56} y={68} fontFamily={TITLE} fontSize={40} fill={C.ink}>{title}</text>
      {sub && <text x={58} y={108} fontFamily={SANS} fontSize={24} fontWeight={600} fill={mode === "m" ? C.teal : C.coral}
        opacity={0.95} letterSpacing="0.02em">{sub}</text>}
    </g>
  );
}

export { Fragment, clamp, lerp, seg, win, E, rad, centroid3 };
