// ashrain.out — 해설 액자 오른쪽 그림: 그림 DSL (frames/figdsl.jsx) — 기본기 해설(frames/basics.jsx)이 쓴다
// 생성기(프로젝트 SRC-학년별해설-*.py 의 fig.py)가 좌표를 다 계산해 넘기고, 여기서는 판서 박자(../lin10.js 의 l10Plan)에 맞춰 그리기만 한다.
//   it.fig = { kind: "dsl", els: [요소], must? } — 그림 칸 660 × 680(무대 x 880 ~ 1540 · y 170 ~ 850, 아래로 갈수록 y 가 커짐)
//   must: 1 — 꼭 보여야 하는 그림(「다음 그래프 · 표」를 읽는 문항): 남은 빈자리가 모자라면 그림 칸을 먼저 떼고 판서가 흐른다(../board.js).
//   요소 k: L 선 · P 꺾은선/다각형 · R 직사각형 · C 원 · D 점 · T 글자(무대 수식 문법) · A 각 표시(a0 → a1 도, 동쪽 0 · 시계 반대 +)
//          G 격자(nx × ny 칸 — 10칸 상자 · 분수 막대) · B 십 모형 막대(n 칸) · X × 표시(지우기)
//   적지 않은 값은 기본값: c ink · sw 3 · z 30 · a m(가운데) · b 600 · at q · 글자 바탕 테두리 있음(ho 0 이면 없음)
//   at: "q"(문제와 함께) · "p"(방침) · 정수 i(판서 i번째 줄) · "a"(답) — 그때 나타난다. dl 늦춤(ms) · un 사라지는 때
//   c 선 색 · f 칠 색(팔레트 이름) · fo 칠 진하기 · sw 선 굵기 · d 점선 · ar 화살촉(1 끝 · 2 양쪽) · dr 그리듯이 · hl 그 줄일 때 빛남
//   mv { at, dx, dy, r, cx, cy, dl } — 그때 옮긴다(잘라 붙이기 · 돌리기). o 진하기.
//   fr { dx, dy, dl, ms } — 나타날 때 (dx, dy) 떨어진 곳에서 출발해 제자리로 날아온다(받아올린 1이 일의 자리 합에서 윗자리로 · 빌려 온 10이 옆 자리에서).
//   rv — 각(A)을 a1 쪽에서 a0 쪽으로 쓸기(시계 방향 — 긴바늘이 12에서 돌아가듯).
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

/* ══════════ 나타나는 모양 — 칠판에 그리듯(선은 그어지고, 각은 쓸리고, 칠은 칠해지고, 점은 톡, 글자는 써진다) ══════════ */
const hyp = (x, y) => Math.hypot(x, y);
/** 꺾은선을 앞에서부터 k 만큼(0 ~ 1) */
function partial(pts, k) {
  if (k >= 1 || pts.length < 2) return pts;
  const L = [];
  let tot = 0;
  for (let i = 1; i < pts.length; i++) { const d = hyp(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
  let rem = tot * Math.max(0, k);
  const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (rem >= L[i - 1]) { out.push(pts[i]); rem -= L[i - 1]; continue; }
    const u = L[i - 1] ? rem / L[i - 1] : 0;
    out.push([pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * u, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * u]);
    break;
  }
  return out;
}
const polyLen = (pts) => { let s = 0; for (let i = 1; i < pts.length; i++) s += hyp(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return s; };
const clampMs = (v, a, b) => Math.max(a, Math.min(b, v));
/** 요소마다 나타나는 데 걸리는 시간(ms) — 길이 · 폭에 맞춰 */
function enterMs(el) {
  switch (el.k) {
    case "L": { const d = hyp(el.x2 - el.x, el.y2 - el.y); return el.dr ? clampMs(420 + d * 1.1, 520, 1100) : clampMs(160 + d * 0.65, 220, 560); }
    case "P": { const closed = !(el.z === false || el.z === 0); const d = polyLen(closed ? [...el.pts, el.pts[0]] : el.pts);
      return el.dr ? clampMs(420 + d * 0.9, 560, 1200) : clampMs(200 + d * 0.5, 260, 700); }
    case "C": return clampMs(260 + el.r * 2.2, 320, 760);
    case "A": return clampMs(300 + Math.abs(el.a1 - el.a0) * 1.6, 340, 760);
    case "R": return clampMs(220 + (el.w + el.h) * 0.35, 260, 560);
    case "G": return clampMs(260 + (el.cw * el.nx + el.ch * el.ny) * 0.3, 320, 620);
    case "B": return 420;
    case "D": return 360;
    case "X": return 380;
    case "T": return clampMs(150 + mathWidth(el.s, el.z || 30, el.b || 600) * 0.9, 200, 620);
    default: return 450;
  }
}

/** 한 요소 그리기 (p: 나타난 정도 0 ~ 1 · glow: 지금 줄이면 0 ~ 1 숨 쉬는 빛 · id: 잘라 보이기 이름) */
function drawEl(el, C, p, glow, id) {
  const col = (n, d) => (n ? C[n] || n : d);
  const sc = col(el.c, C.ink), sw = el.sw ?? 3;
  const dash = el.d ? "12 9" : undefined;
  const fill = el.f ? col(el.f, C.ink) : "none";
  const fo = el.f ? el.fo ?? 1 : undefined;
  const halo = glow > 0;
  const ho = 0.18 + 0.22 * glow;
  const wipe = (x0, y0, w, h, node, dir = "x") => (p >= 1 ? node : (
    <g>
      <clipPath id={id}><rect x={x0 - 6} y={y0 - 6} width={dir === "x" ? (w + 12) * p : w + 12} height={dir === "y" ? (h + 12) * p : h + 12} /></clipPath>
      <g clipPath={`url(#${id})`}>{node}</g>
    </g>
  ));
  switch (el.k) {
    case "L": {
      const x2 = el.x + (el.x2 - el.x) * p, y2 = el.y + (el.y2 - el.y) * p;
      const out = [];
      if (halo) out.push(<line key="g" x1={el.x} y1={el.y} x2={x2} y2={y2} stroke={C.gold} strokeWidth={sw + 12} strokeOpacity={ho} strokeLinecap="round" />);
      out.push(<line key="l" x1={el.x} y1={el.y} x2={x2} y2={y2} stroke={sc} strokeWidth={sw} strokeDasharray={dash} strokeLinecap="round" />);
      if (el.ar && p >= 0.98) {
        out.push(arrowHead(el.x, el.y, el.x2, el.y2, 9 + sw * 2.2, sc, "h1"));
        if (el.ar === 2) out.push(arrowHead(el.x2, el.y2, el.x, el.y, 9 + sw * 2.2, sc, "h2"));
      }
      return <g>{out}</g>;
    }
    case "P": {
      const closed = !(el.z === false || el.z === 0);
      const Tag = closed ? "polygon" : "polyline";
      const all = el.pts.map((q) => q.join(",")).join(" ");
      const part = p >= 1 ? null : partial(closed ? [...el.pts, el.pts[0]] : el.pts, p).map((q) => q.map((v) => v.toFixed(1)).join(",")).join(" ");
      const out = [];
      if (halo) out.push(<Tag key="g" points={all} fill="none" stroke={C.gold} strokeWidth={sw + 12} strokeOpacity={ho} strokeLinejoin="round" strokeLinecap="round" />);
      if (el.f) out.push(<Tag key="f" points={all} fill={fill} fillOpacity={fo * seg(p, 0.55, 1)} stroke="none" />);
      if (el.c !== "none") {
        out.push(part != null
          ? <polyline key="l" points={part} fill="none" stroke={sc} strokeWidth={sw} strokeDasharray={dash} strokeLinejoin="round" strokeLinecap="round" />
          : <Tag key="l" points={all} fill="none" stroke={sc} strokeWidth={sw} strokeDasharray={dash} strokeLinejoin="round" strokeLinecap="round" />);
      }
      if (el.ar && p >= 0.98 && el.pts.length > 1) {
        const n = el.pts.length, [x1, y1] = el.pts[n - 2], [x2, y2] = el.pts[n - 1];
        out.push(arrowHead(x1, y1, x2, y2, 9 + sw * 2.2, sc, "h"));
      }
      return <g>{out}</g>;
    }
    case "R": {
      const node = (
        <g>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={el.w + 10} height={el.h + 10} rx={(el.rx || 0) + 5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={ho} /> : null}
          <rect x={el.x} y={el.y} width={el.w} height={el.h} rx={el.rx || 0} fill={fill} fillOpacity={fo} stroke={el.c === "none" ? "none" : sc} strokeWidth={sw} strokeDasharray={dash} />
        </g>
      );
      // 칠만 있는 칸은 칠하듯(왼쪽 → 오른쪽), 테두리가 있는 칸은 한 바퀴 그은 뒤 칠이 든다
      if (el.c === "none" || el.d || p >= 1) return wipe(el.x, el.y, el.w, el.h, node, el.h > el.w * 2.4 ? "y" : "x");
      return (
        <g>
          {el.f ? <rect x={el.x} y={el.y} width={el.w} height={el.h} rx={el.rx || 0} fill={fill} fillOpacity={fo * seg(p, 0.5, 1)} stroke="none" /> : null}
          <rect x={el.x} y={el.y} width={el.w} height={el.h} rx={el.rx || 0} fill="none" stroke={sc} strokeWidth={sw} pathLength={1} strokeDasharray={`${p} 1`} />
        </g>
      );
    }
    case "C": {
      if (p < 1 && !el.d) {
        return (
          <g>
            {el.f ? <circle cx={el.x} cy={el.y} r={el.r} fill={fill} fillOpacity={fo * seg(p, 0.5, 1)} stroke="none" /> : null}
            {el.c !== "none" && <circle cx={el.x} cy={el.y} r={el.r} fill="none" stroke={sc} strokeWidth={sw} pathLength={1} strokeDasharray={`${p} 1`}
              transform={`rotate(-90 ${el.x} ${el.y})`} />}
          </g>
        );
      }
      const r = el.r * (p >= 1 ? 1 : 0.7 + 0.3 * p);
      return (
        <g opacity={p >= 1 ? 1 : p}>
          {halo ? <circle cx={el.x} cy={el.y} r={el.r + 6} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={ho} /> : null}
          <circle cx={el.x} cy={el.y} r={r} fill={fill} fillOpacity={fo} stroke={el.c === "none" ? "none" : sc} strokeWidth={sw} strokeDasharray={dash} />
        </g>
      );
    }
    case "D": {
      const k = p >= 1 ? 1 : Math.max(0, E.back(p));
      const r = (el.r ?? 8) * (0.15 + 0.85 * k);
      return (
        <g>
          {halo ? <circle cx={el.x} cy={el.y} r={r + 7 + 4 * glow} fill={C.gold} fillOpacity={0.2 + 0.2 * glow} /> : null}
          <circle cx={el.x} cy={el.y} r={r} fill={col(el.f, C.ink)} stroke={el.c ? col(el.c, C.ink) : "none"} strokeWidth={el.sw ?? 2} />
        </g>
      );
    }
    case "G": {
      const w = el.cw * el.nx, h = el.ch * el.ny, ls = [];
      for (let i = 1; i < el.nx; i++) ls.push(<line key={"v" + i} x1={el.x + el.cw * i} y1={el.y} x2={el.x + el.cw * i} y2={el.y + h} stroke={sc} strokeWidth={Math.max(1, sw * 0.67)} />);
      for (let j = 1; j < el.ny; j++) ls.push(<line key={"h" + j} x1={el.x} y1={el.y + el.ch * j} x2={el.x + w} y2={el.y + el.ch * j} stroke={sc} strokeWidth={Math.max(1, sw * 0.67)} />);
      return wipe(el.x, el.y, w, h, (
        <g>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={w + 10} height={h + 10} rx={(el.rx || 0) + 5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={ho} /> : null}
          <rect x={el.x} y={el.y} width={w} height={h} rx={el.rx || 0} fill={fill} fillOpacity={fo} stroke={sc} strokeWidth={sw} />
          {ls}
        </g>
      ), h > w * 2.4 ? "y" : "x");
    }
    case "B": {
      const n = el.n || 10, w = el.w ?? 26, h = el.h ?? 230, ls = [];
      for (let i = 1; i < n; i++) ls.push(<line key={i} x1={el.x} y1={el.y + (h * i) / n} x2={el.x + w} y2={el.y + (h * i) / n} stroke={sc} strokeWidth={1.2} />);
      const drop = p >= 1 ? 0 : (1 - E.back(p)) * -34;
      return (
        <g transform={drop ? `translate(0 ${drop.toFixed(1)})` : undefined}>
          {halo ? <rect x={el.x - 5} y={el.y - 5} width={w + 10} height={h + 10} rx={5} fill="none" stroke={C.gold} strokeWidth={10} strokeOpacity={ho} /> : null}
          <rect x={el.x} y={el.y} width={w} height={h} fill={el.f ? col(el.f, C.gold) : "none"} fillOpacity={el.fo ?? 0.35} stroke={sc} strokeWidth={el.sw ?? 2.5} />
          {ls}
        </g>
      );
    }
    case "X": {
      const s = el.s ?? 12, c = col(el.c, C.red), w2 = el.sw ?? 4, a = Math.min(1, p * 2), b = Math.max(0, p * 2 - 1);
      return (
        <g>
          <line x1={el.x - s} y1={el.y - s} x2={el.x - s + 2 * s * a} y2={el.y - s + 2 * s * a} stroke={c} strokeWidth={w2} strokeLinecap="round" />
          {b > 0 && <line x1={el.x - s} y1={el.y + s} x2={el.x - s + 2 * s * b} y2={el.y + s - 2 * s * b} stroke={c} strokeWidth={w2} strokeLinecap="round" />}
        </g>
      );
    }
    case "T": {
      const z = el.z || 30;
      const node = (
        <g>
          {halo ? <circle cx={el.x} cy={el.y - z * 0.34} r={z * 0.95} fill={C.gold} fillOpacity={0.1 + 0.14 * glow} /> : null}
          <MText x={el.x} y={el.y} s={el.s} size={z} weight={el.b || 600} anchor={ANCHOR[el.a] || "middle"} fill={col(el.c, C.ink)}
            halo={el.ho === 0 ? undefined : C.halo} C={C} />
        </g>
      );
      if (p >= 1) return node;
      // 왼쪽부터 써진다
      const w = mathWidth(el.s, z, el.b || 600), a = ANCHOR[el.a] || "middle";
      const lx = a === "start" ? el.x : a === "end" ? el.x - w : el.x - w / 2;
      const fr = String(el.s).includes("{");
      return wipe(lx - z * 0.1, el.y - z * (fr ? 1.2 : 1), w + z * 0.2, z * (fr ? 1.9 : 1.4), node);
    }
    case "A": {
      const span = el.a1 - el.a0 + (el.a1 < el.a0 ? 360 : 0);
      const b0 = el.rv ? el.a1 - span * p : el.a0, b1 = el.rv ? el.a1 : el.a0 + span * p;
      return (
        <g>
          {el.f ? <path d={arcPath(el.x, el.y, el.r, b0, b1, true)} fill={fill} fillOpacity={(el.fo ?? 0.25) * (1 + 0.6 * glow)} stroke="none" /> : null}
          <path d={arcPath(el.x, el.y, el.r, b0, b1, false)} fill="none" stroke={glow > 0 ? C.gold : sc} strokeWidth={glow > 0 ? sw + 1.5 : sw} strokeLinecap="round" />
        </g>
      );
    }
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
    if (el.fr) for (const m of [0.5, 1]) for (const [x, y] of corners) put(x + (el.fr.dx || 0) * m, y + (el.fr.dy || 0) * m);
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

/**
 * 같은 때(at) 나타나는 요소 가운데 늦춤(dl)이 없는 것들은 적힌 차례대로 조금씩 늦춰 — 한꺼번에 뜨지 않고 그려 나가듯.
 * 문제와 함께 나오는 그림(q)은 문제를 읽는 동안(1.9초 안에) 다 그려진다 — 인쇄(문제지)는 그 뒤 모습을 찍는다.
 */
const ORDER = new WeakMap();
function orderOf(f) {
  if (ORDER.has(f)) return ORDER.get(f);
  const groups = new Map();
  f.els.forEach((el, i) => {
    if (el.dl) return;
    const key = String(el.at ?? "q");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(i);
  });
  const extra = new Array(f.els.length).fill(0);
  for (const [key, idx] of groups) {
    if (idx.length < 2) continue;
    const step = Math.min(110, (key === "q" ? 800 : 650) / (idx.length - 1));
    idx.forEach((i, j) => { extra[i] = Math.round(j * step); });
  }
  ORDER.set(f, extra);
  return extra;
}
export const Q_DONE = 1900;

export function FigDsl({ it, t, C, uid = "" }) {
  const f = it.fig, P = l10Plan(it), cur = lineAt(P, t);
  const extra = orderOf(f);
  const out = [];
  f.els.forEach((el, i) => {
    const isQ = el.at == null || el.at === "q";
    const ta = atTime(P, el.at) + (el.dl || 0) + extra[i];
    let dur = enterMs(el);
    if (isQ) dur = Math.max(120, Math.min(dur, Q_DONE - ta));
    if (t < ta) return;
    const p = seg(t, ta, ta + dur, el.k === "D" || el.k === "B" ? E.lin : E.io);
    let o = Math.min(1, (t - ta) / 140);
    if (el.un != null) {
      const tu = atTime(P, el.un);
      o *= 1 - seg(t, tu, tu + 420, E.sine);
      if (o <= 0.001) return;
    }
    const glow = el.hl && Number.isInteger(el.at) && cur === el.at ? 0.5 + 0.5 * Math.sin(((t - ta) / 1200) * Math.PI * 2 - Math.PI / 2) : 0;
    let g = drawEl(el, C, p, glow, `fd${uid}-${it.no}-${i}`);
    if (el.fr) {
      // 날아오기 — 떨어진 곳에서 잠깐 머문 뒤 휘어 날아와 제자리에(끝 모습은 제자리 — 인쇄도 같다)
      const t0 = ta + (el.fr.dl ?? 260), m = seg(t, t0, t0 + (el.fr.ms || 620), E.io);
      if (m < 1) {
        const dx = el.fr.dx || 0, dy = el.fr.dy || 0, lift = Math.min(60, hyp(dx, dy) * 0.3) * 4 * m * (1 - m);
        g = <g transform={`translate(${(dx * (1 - m)).toFixed(1)} ${(dy * (1 - m) - lift).toFixed(1)})`}>{g}</g>;
      }
    }
    if (el.mv) {
      // 들어 올려 옮기듯 — 위로 살짝 휘어 가서 내려놓는다(돌리기는 그 자리에서)
      const tm = atTime(P, el.mv.at) + (el.mv.dl || 0), m = seg(t, tm, tm + 900, E.io);
      if (m > 0) {
        const dx = el.mv.dx || 0, dy = el.mv.dy || 0;
        const lift = el.mv.r ? 0 : Math.min(70, hyp(dx, dy) * 0.28) * 4 * m * (1 - m);
        const tr = `translate(${(dx * m).toFixed(1)} ${(dy * m - lift).toFixed(1)})` + (el.mv.r ? ` rotate(${(el.mv.r * m).toFixed(2)} ${el.mv.cx || 0} ${el.mv.cy || 0})` : "");
        g = <g transform={tr}>{g}</g>;
      }
    }
    out.push(<g key={i} opacity={o * (el.o ?? 1)}>{g}</g>);
  });
  return <g transform={`translate(${FIG_BOX.x0} ${FIG_BOX.y0})`}>{out}</g>;
}
