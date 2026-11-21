// ashrain.out — 해설 액자 오른쪽 그림: 그림 DSL (frames/figdsl.jsx) — 기본기 해설(frames/basics.jsx)이 쓴다
// 생성기(프로젝트 SRC-학년별해설-*.py 의 fig.py)가 좌표를 다 계산해 넘기고, 여기서는 판서 박자(../lin10.js 의 l10Plan)에 맞춰 그리기만 한다.
//   it.fig = { kind: "dsl", els: [요소] } — 그림 칸 660 × 680(무대 x 880 ~ 1540 · y 170 ~ 850, 아래로 갈수록 y 가 커짐)
//   요소 k: L 선 · P 꺾은선/다각형 · R 직사각형 · C 원 · D 점 · T 글자(무대 수식 문법) · A 각 표시(a0 → a1 도, 동쪽 0 · 시계 반대 +)
//          G 격자(nx × ny 칸 — 10칸 상자 · 분수 막대) · B 십 모형 막대(n 칸) · X × 표시(지우기)
//   적지 않은 값은 기본값: c ink · sw 3 · z 30 · a m(가운데) · b 600 · at q · 글자 바탕 테두리 있음(ho 0 이면 없음)
//   at: "q"(문제와 함께) · "p"(방침) · 정수 i(판서 i번째 줄) · "a"(답) — 그때 나타난다. dl 늦춤(ms) · un 사라지는 때
//   c 선 색 · f 칠 색(팔레트 이름) · fo 칠 진하기 · sw 선 굵기 · d 점선 · ar 화살촉(1 끝 · 2 양쪽) · dr 그리듯이 · hl 그 줄일 때 빛남
//   mv { at, dx, dy, r, cx, cy } — 그때 옮긴다(잘라 붙이기 · 돌리기). o 진하기.
// 같은 그림을 인쇄 문서(흑백)로도 찍는다 — frames/avfig.jsx(흑백 팔레트) → frames/avprint.js.
import { MText, mathWidth } from "../draw.jsx";
import { seg, E } from "../core.js";
import { l10Plan, lineAt } from "../lin10.js";

export const FIG_BOX = { x0: 880, y0: 170, x1: 1540, y1: 850 };
const ANCHOR = { s: "start", m: "middle", e: "end" };

/** 요소가 나타나는 시각(ms) */
export function atTime(P, at) {
  if (at === "q" || at == null) return 0;
  if (at === "p") return P.plan[0];
  if (at === "a") return P.ans;
  if (Number.isInteger(at)) return P.lines[at] ? P.lines[at].a : P.ans;
  return 0;
}

function arrowHead(x1, y1, x2, y2, size, fill, key) {
  const a = Math.atan2(y2 - y1, x2 - x1), s = size;
  const p = [[x2, y2], [x2 - s * Math.cos(a - 0.42), y2 - s * Math.sin(a - 0.42)], [x2 - s * Math.cos(a + 0.42), y2 - s * Math.sin(a + 0.42)]];
  return <polygon key={key} points={p.map((q) => q.join(",")).join(" ")} fill={fill} />;
}

function arcPath(x, y, r, a0, a1, sector) {
  const p = (a) => [x + r * Math.cos((a * Math.PI) / 180), y - r * Math.sin((a * Math.PI) / 180)];
  let d1 = a1;
  while (d1 < a0) d1 += 360;
  const [sx, sy] = p(a0), [ex, ey] = p(d1);
  const large = d1 - a0 > 180 ? 1 : 0;
  const arc = `M${sx.toFixed(1)},${sy.toFixed(1)} A${r},${r} 0 ${large} 0 ${ex.toFixed(1)},${ey.toFixed(1)}`;
  return sector ? `M${x},${y} L${sx.toFixed(1)},${sy.toFixed(1)} A${r},${r} 0 ${large} 0 ${ex.toFixed(1)},${ey.toFixed(1)} Z` : arc;
}

/** 한 요소 그리기 (k: 나타남 0~1 · draw: 그려진 정도 0~1 · glow: 지금 줄) */
function drawEl(el, C, k, draw, glow, key) {
  const col = (n, d) => (n ? C[n] || n : d);
  const sc = col(el.c, C.ink), sw = el.sw ?? 3;
  const dash = el.d ? "12 9" : undefined;
  const dr = el.dr && !el.d && draw < 1 ? { pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - draw } : null;
  const fill = el.f ? col(el.f, C.ink) : "none";
  const fo = el.f ? el.fo ?? 1 : undefined;
  const halo = glow ? 1 : 0;
  switch (el.k) {
    case "L": {
      const out = [];
      if (halo) out.push(<line key="g" x1={el.x} y1={el.y} x2={el.x2} y2={el.y2} stroke={C.gold} strokeWidth={sw + 12} strokeOpacity={0.32} strokeLinecap="round" />);
      out.push(<line key="l" x1={el.x} y1={el.y} x2={el.x2} y2={el.y2} stroke={sc} strokeWidth={sw} strokeDasharray={dash} strokeLinecap="round" {...dr} />);
      if (el.ar && draw >= 0.98) {
        out.push(arrowHead(el.x, el.y, el.x2, el.y2, 9 + sw * 2.2, sc, "h1"));
        if (el.ar === 2) out.push(arrowHead(el.x2, el.y2, el.x, el.y, 9 + sw * 2.2, sc, "h2"));
      }
      return <g key={key}>{out}</g>;
    }
    case "P": {
      const pts = el.pts.map((q) => q.join(",")).join(" ");
      const Tag = el.z === false || el.z === 0 ? "polyline" : "polygon";
      const out = [];
      if (halo) out.push(<Tag key="g" points={pts} fill="none" stroke={C.gold} strokeWidth={sw + 12} strokeOpacity={0.32} strokeLinejoin="round" strokeLinecap="round" />);
      if (el.f) out.push(<Tag key="f" points={pts} fill={fill} fillOpacity={fo * Math.min(1, draw * 1.4)} stroke="none" />);
      if (el.c !== "none") out.push(<Tag key="l" points={pts} fill="none" stroke={sc} strokeWidth={sw} strokeDasharray={dash} strokeLinejoin="round" strokeLinecap="round" {...dr} />);
      if (el.ar && draw >= 0.98 && el.pts.length > 1) {
        const n = el.pts.length, [x1, y1] = el.pts[n - 2], [x2, y2] = el.pts[n - 1];
        out.push(arrowHead(x1, y1, x2, y2, 9 + sw * 2.2, sc, "h"));
      }
      return <g key={key}>{out}</g>;
    }
    case "R":
      return (
        <g key={key}>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={el.w + 10} height={el.h + 10} rx={(el.rx || 0) + 5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={0.32} /> : null}
          <rect x={el.x} y={el.y} width={el.w} height={el.h} rx={el.rx || 0} fill={fill} fillOpacity={fo} stroke={el.c === "none" ? "none" : sc} strokeWidth={sw} strokeDasharray={dash} />
        </g>
      );
    case "C":
      return (
        <g key={key}>
          {halo ? <circle cx={el.x} cy={el.y} r={el.r + 6} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={0.32} /> : null}
          <circle cx={el.x} cy={el.y} r={el.r} fill={fill} fillOpacity={fo} stroke={el.c === "none" ? "none" : sc} strokeWidth={sw} strokeDasharray={dash} {...dr} />
        </g>
      );
    case "D": {
      const r = (el.r ?? 8) * (0.55 + 0.45 * k);
      return (
        <g key={key}>
          {halo ? <circle cx={el.x} cy={el.y} r={r + 9} fill={C.gold} fillOpacity={0.3} /> : null}
          <circle cx={el.x} cy={el.y} r={r} fill={col(el.f, C.ink)} stroke={el.c ? col(el.c, C.ink) : "none"} strokeWidth={el.sw ?? 2} />
        </g>
      );
    }
    case "G": {
      const w = el.cw * el.nx, h = el.ch * el.ny, ls = [];
      for (let i = 1; i < el.nx; i++) ls.push(<line key={"v" + i} x1={el.x + el.cw * i} y1={el.y} x2={el.x + el.cw * i} y2={el.y + h} stroke={sc} strokeWidth={Math.max(1, sw * 0.67)} />);
      for (let j = 1; j < el.ny; j++) ls.push(<line key={"h" + j} x1={el.x} y1={el.y + el.ch * j} x2={el.x + w} y2={el.y + el.ch * j} stroke={sc} strokeWidth={Math.max(1, sw * 0.67)} />);
      return (
        <g key={key}>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={w + 10} height={h + 10} rx={(el.rx || 0) + 5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={0.32} /> : null}
          <rect x={el.x} y={el.y} width={w} height={h} rx={el.rx || 0} fill={fill} fillOpacity={fo} stroke={sc} strokeWidth={sw} />
          {ls}
        </g>
      );
    }
    case "B": {
      const n = el.n || 10, w = el.w ?? 26, h = el.h ?? 230, ls = [];
      for (let i = 1; i < n; i++) ls.push(<line key={i} x1={el.x} y1={el.y + (h * i) / n} x2={el.x + w} y2={el.y + (h * i) / n} stroke={sc} strokeWidth={1.2} />);
      return (
        <g key={key}>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={w + 10} height={h + 10} rx={5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={0.32} /> : null}
          <rect x={el.x} y={el.y} width={w} height={h} fill={el.f ? col(el.f, C.gold) : "none"} fillOpacity={el.fo ?? 0.35} stroke={sc} strokeWidth={el.sw ?? 2.5} />
          {ls}
        </g>
      );
    }
    case "X": {
      const s = el.s ?? 12, c = col(el.c, C.red), w2 = el.sw ?? 4, p = Math.min(1, draw * 2), q = Math.max(0, draw * 2 - 1);
      return (
        <g key={key}>
          <line x1={el.x - s} y1={el.y - s} x2={el.x - s + 2 * s * p} y2={el.y - s + 2 * s * p} stroke={c} strokeWidth={w2} strokeLinecap="round" />
          {q > 0 && <line x1={el.x - s} y1={el.y + s} x2={el.x - s + 2 * s * q} y2={el.y + s - 2 * s * q} stroke={c} strokeWidth={w2} strokeLinecap="round" />}
        </g>
      );
    }
    case "T":
      return (
        <g key={key}>
          {halo ? <circle cx={el.x} cy={el.y - (el.z || 30) * 0.34} r={(el.z || 30) * 0.95} fill={C.gold} fillOpacity={0.18} /> : null}
          <MText x={el.x} y={el.y} s={el.s} size={el.z || 30} weight={el.b || 600} anchor={ANCHOR[el.a] || "middle"} fill={col(el.c, C.ink)}
            halo={el.ho === 0 ? undefined : C.halo} C={C} />
        </g>
      );
    case "A":
      return (
        <g key={key}>
          {el.f ? <path d={arcPath(el.x, el.y, el.r, el.a0, el.a1, true)} fill={fill} fillOpacity={(el.fo ?? 0.25) * (glow ? 1.6 : 1)} stroke="none" /> : null}
          <path d={arcPath(el.x, el.y, el.r, el.a0, el.a1, false)} fill="none" stroke={glow ? C.gold : sc} strokeWidth={glow ? sw + 1.5 : sw} strokeLinecap="round" {...dr} />
        </g>
      );
    default:
      return null;
  }
}

/**
 * 그림이 실제로 차지하는 네모(무대 좌표) — 해설 판이 글자 옆 빈자리에 맞춰 줄여 넣을 때 쓴다(../board.js).
 * 요소마다 끝 · 굵기 · 글자 폭을 재고, 옮기는(mv) 것은 옮기기 전 · 중간 · 뒤 자리를 모두 넣는다.
 */
const BOXES = new WeakMap();
export function dslBox(f) {
  if (BOXES.has(f)) return BOXES.get(f);
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  const put = (x, y) => { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); };
  for (const el of f.els) {
    const p = (el.sw ?? 3) / 2 + 2;
    let r = null;
    switch (el.k) {
      case "L": { const h = el.ar ? 9 + (el.sw ?? 3) * 2.2 : 0; r = [Math.min(el.x, el.x2) - p - h, Math.min(el.y, el.y2) - p - h, Math.max(el.x, el.x2) + p + h, Math.max(el.y, el.y2) + p + h]; break; }
      case "P": { const xs = el.pts.map((q) => q[0]), ys = el.pts.map((q) => q[1]), h = el.ar ? 9 + (el.sw ?? 3) * 2.2 : 0;
        r = [Math.min(...xs) - p - h, Math.min(...ys) - p - h, Math.max(...xs) + p + h, Math.max(...ys) + p + h]; break; }
      case "R": r = [el.x - p, el.y - p, el.x + el.w + p, el.y + el.h + p]; break;
      case "C": case "A": r = [el.x - el.r - p, el.y - el.r - p, el.x + el.r + p, el.y + el.r + p]; break;
      case "D": { const q = (el.r ?? 8) + 4; r = [el.x - q, el.y - q, el.x + q, el.y + q]; break; }
      case "G": r = [el.x - p, el.y - p, el.x + el.cw * el.nx + p, el.y + el.ch * el.ny + p]; break;
      case "B": r = [el.x - 2, el.y - 2, el.x + (el.w ?? 26) + 2, el.y + (el.h ?? 230) + 2]; break;
      case "X": { const q = (el.s ?? 12) + 3; r = [el.x - q, el.y - q, el.x + q, el.y + q]; break; }
      case "T": {
        const z = el.z || 30, w = mathWidth(el.s, z, el.b || 600), a = ANCHOR[el.a] || "middle";
        const lx = a === "start" ? el.x : a === "end" ? el.x - w : el.x - w / 2;
        const fr = String(el.s).includes("{"), up = z * (fr ? 1.04 : 0.84), dn = z * (fr ? 0.52 : 0.26);
        r = [lx - z * 0.12, el.y - up, lx + w + z * 0.12, el.y + dn]; break;
      }
      default: r = null;
    }
    if (!r) continue;
    const corners = [[r[0], r[1]], [r[2], r[1]], [r[0], r[3]], [r[2], r[3]]];
    for (const [x, y] of corners) put(x, y);
    if (el.mv) {
      for (const m of [0.5, 1]) {
        const th = ((el.mv.r || 0) * m * Math.PI) / 180, cx = el.mv.cx || 0, cy = el.mv.cy || 0;
        for (const [x, y] of corners) {
          const rx = cx + (x - cx) * Math.cos(th) - (y - cy) * Math.sin(th), ry = cy + (x - cx) * Math.sin(th) + (y - cy) * Math.cos(th);
          put(rx + (el.mv.dx || 0) * m, ry + (el.mv.dy || 0) * m);
        }
      }
    }
  }
  const out = Number.isFinite(x0) ? { x0: x0 + FIG_BOX.x0 - 6, y0: y0 + FIG_BOX.y0 - 6, x1: x1 + FIG_BOX.x0 + 6, y1: y1 + FIG_BOX.y0 + 6 } : null;
  BOXES.set(f, out);
  return out;
}

export function FigDsl({ it, t, C }) {
  const f = it.fig, P = l10Plan(it), cur = lineAt(P, t);
  const out = [];
  f.els.forEach((el, i) => {
    const ta = atTime(P, el.at) + (el.dl || 0);
    let k = seg(t, ta, ta + 450, E.out);
    if (k <= 0) return;
    if (el.un != null) {
      const tu = atTime(P, el.un);
      k *= 1 - seg(t, tu, tu + 420, E.sine);
      if (k <= 0.001) return;
    }
    const draw = el.dr ? seg(t, ta, ta + 750, E.sine) : el.k === "X" ? seg(t, ta, ta + 380, E.sine) : 1;
    const glow = el.hl && Number.isInteger(el.at) && cur === el.at;
    let g = drawEl(el, C, k, draw, glow, "e");
    if (el.mv) {
      const tm = atTime(P, el.mv.at), m = seg(t, tm, tm + 900, E.sine);
      if (m > 0) {
        const tr = `translate(${(el.mv.dx || 0) * m} ${(el.mv.dy || 0) * m})` + (el.mv.r ? ` rotate(${el.mv.r * m} ${el.mv.cx || 0} ${el.mv.cy || 0})` : "");
        g = <g transform={tr}>{g}</g>;
      }
    }
    out.push(<g key={i} opacity={k * (el.o ?? 1)}>{g}</g>);
  });
  return <g transform={`translate(${FIG_BOX.x0} ${FIG_BOX.y0})`}>{out}</g>;
}
