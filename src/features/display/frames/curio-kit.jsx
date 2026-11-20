// ashrain.out — 수학 호기심 액자 공용 그리기 부품 (frames/curio-kit.jsx)
// 축구 · 농구 · 야구 직선 액자와 공 꺼내기 · 알파벳 카드 · 일렬로 세우기 · 학년별 뽑기 액자가 함께 쓴다.
//   · FitText — 칸 너비에 맞춰 글자 크기를 줄여 쓰는 MText
//   · Lines — 판서 줄을 시각에 맞춰 하나씩(마지막 식 줄은 금빛 · 크게)
//   · Panel — 둥근 판(설명 칸) · clipLine — 무한 직선을 사각형 안 선분으로 · seq — 장면 박자
import { MText, mathWidth, SANS } from "../draw.jsx";
import { UText, uWidth, Chip, chipW } from "../kit-story.jsx";
import { seg } from "../core.js";

/** 너비 maxW 안에 들도록 size 를 줄인 MText(최소 minSize). unit 이면 홀로 선 m 을 단위(미터)로 바로 세운다(UText) */
export function FitText({ s, size = 28, maxW, minSize = 16, unit, ...rest }) {
  if (!s) return null;
  let k = size;
  if (maxW) { const w = (unit ? uWidth : mathWidth)(s, size, rest.weight || 500); if (w > maxW) k = Math.max(minSize, (size * maxW) / w); }
  return unit ? <UText s={s} size={k} {...rest} /> : <MText s={s} size={k} {...rest} />;
}

/**
 * 판서 줄: lines = [{ s, at(나타나는 시각), hi?, small?, col? }] — t 가 at 을 지나면 0.4초에 걸쳐 나타난다.
 * hi 줄은 금빛으로 크게, small 줄은 옅게 작게. 반환 높이만큼 아래로 쌓는다.
 */
export function Lines({ x, y, lines, t, C, size = 26, lh = 52, maxW, o = 1, hiSize, unit }) {
  let yy = y;
  const out = [];
  lines.forEach((L, i) => {
    const k = seg(t, L.at, L.at + 400);
    const sz = L.hi ? hiSize || size * 1.3 : L.small ? size * 0.78 : size;
    const step = L.hi ? lh * 1.25 : L.small ? lh * 0.78 : lh;
    yy += L.gap || 0;
    if (k > 0.001) {
      out.push(
        <g key={i} opacity={k * o} transform={`translate(${(1 - k) * 14},0)`}>
          <FitText x={x} y={yy} s={L.s} size={sz} maxW={maxW} unit={unit} weight={L.hi ? 800 : L.small ? 600 : 650}
            fill={L.col || (L.hi ? C.gold : L.small ? C.soft : C.ink)} C={C} />
        </g>,
      );
    }
    yy += step;
  });
  return <g>{out}</g>;
}

/** 둥근 판 */
export function Panel({ x, y, w, h, C, o = 1, r = 22 }) {
  if (o <= 0.001) return null;
  return <rect x={x} y={y} width={w} height={h} rx={r} fill={C.card} fillOpacity={C.name === "light" ? 0.78 : 0.62}
    stroke={C.cardEdge} strokeWidth={1.6} opacity={o} />;
}

/** 작은 글자(그냥 글자 — 영어 이름 · 출처) */
export function Small({ x, y, s, size = 16, C, fill, anchor = "start", o = 1, weight = 600 }) {
  if (!s || o <= 0.001) return null;
  return <text x={x} y={y} fontFamily={SANS} fontSize={size} fontWeight={weight} fill={fill || C.soft} textAnchor={anchor} opacity={o}>{s}</text>;
}

/**
 * 무한 직선(점 p 를 지나고 방향 d)을 사각형 [x0, y0, x1, y1] 안 선분으로 — 없으면 null
 */
export function clipLine(p, d, rect) {
  const [x0, y0, x1, y1] = rect;
  let lo = -Infinity, hi = Infinity;
  for (const [pp, dd, mn, mx] of [[p[0], d[0], x0, x1], [p[1], d[1], y0, y1]]) {
    if (Math.abs(dd) < 1e-12) { if (pp < mn || pp > mx) return null; continue; }
    let a = (mn - pp) / dd, b = (mx - pp) / dd;
    if (a > b) [a, b] = [b, a];
    lo = Math.max(lo, a); hi = Math.min(hi, b);
  }
  if (!(lo <= hi)) return null;
  return [[p[0] + d[0] * lo, p[1] + d[1] * lo], [p[0] + d[0] * hi, p[1] + d[1] * hi]];
}

/** 박자: [[이름, 길이], …] → { 이름: [시작, 끝] , dur } */
export function seq(list) {
  const out = {}; let t = 0;
  for (const [k, d] of list) { out[k] = [t, t + d]; t += d; }
  out.dur = t;
  return out;
}

/** 직선의 방향(그리기용) — 무한 직선을 그릴 때 */
export const dirOf = (a, b) => [b[0] - a[0], b[1] - a[1]];

/** 화살표 머리(끝 q, 방향 p→q) */
export function Head({ p, q, size = 14, fill, o = 1 }) {
  const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
  const a = [q[0] - ux * size - uy * size * 0.55, q[1] - uy * size + ux * size * 0.55];
  const b = [q[0] - ux * size + uy * size * 0.55, q[1] - uy * size - ux * size * 0.55];
  return <path d={`M${q[0]} ${q[1]}L${a[0]} ${a[1]}L${b[0]} ${b[1]}Z`} fill={fill} opacity={o} />;
}

/* ══════════ 기울기 · 절편 강조 ══════════ */
/** 금테 두른 큰 칩 — 그래프 위에서 기울기 · 절편이 눈에 확 들어오게 */
export function BigChip({ x, y, s, size = 34, C, o = 1, color, edge, anchor = "middle" }) {
  if (!s || o <= 0.001) return null;
  return <Chip x={x} y={y} s={s} size={size} C={C} color={color || C.gold} stroke={edge || C.gold} o={o} anchor={anchor} weight={800} />;
}
export const bigW = (s, size = 34) => chipW(s, size, 800);
/**
 * 직선 P→Q(화면 좌표) 위 f 지점에서, 기울기 삼각형 모서리 (Q.x, P.y) 반대쪽으로 직선에 수직하게 비켜 선 자리 — w × h 칩의 가운데.
 * 가로선이면 위, 세로선이면 오른쪽. side = -1 이면 삼각형 쪽으로.
 */
export function besideLine(P, Q, w, h, f = 0.5, side = 1, gap = 14) {
  const mx = P[0] + (Q[0] - P[0]) * f, my = P[1] + (Q[1] - P[1]) * f;
  const len = Math.hypot(Q[0] - P[0], Q[1] - P[1]) || 1;
  let nx = -(Q[1] - P[1]) / len, ny = (Q[0] - P[0]) / len;
  if (Math.abs(Q[1] - P[1]) < 1) { nx = 0; ny = -1; }
  else if (Math.abs(Q[0] - P[0]) < 1) { nx = 1; ny = 0; }
  else if (nx * (mx - Q[0]) + ny * (my - P[1]) < 0) { nx = -nx; ny = -ny; }
  nx *= side; ny *= side;
  const off = Math.abs(nx) * (w / 2) + Math.abs(ny) * (h / 2) + gap;
  return [mx + nx * off, my + ny * off];
}
/**
 * 칩 자리 고르기: 후보 가운데 피할 것(사각형 {x, y, w, h} — 점은 w = h = 0)과 가장 먼 곳. box 안으로 맞춘다.
 */
export function pickSpot(cands, w, h, avoid, box) {
  let best = null, bs = -Infinity;
  for (const c of cands) {
    let [x, y] = c;
    if (box) { x = Math.min(Math.max(x, box[0] + w / 2 + 6), box[2] - w / 2 - 6); y = Math.min(Math.max(y, box[1] + h / 2 + 6), box[3] - h / 2 - 6); }
    let m = Infinity;
    for (const r of avoid) {
      const dx = Math.max(0, Math.abs(r.x - x) - (r.w + w) / 2), dy = Math.max(0, Math.abs(r.y - y) - (r.h + h) / 2);
      m = Math.min(m, Math.hypot(dx, dy));
    }
    if (m > bs + 0.5) { bs = m; best = [x, y]; }
    if (m >= 40) break;   // 넉넉하면 앞 후보(더 좋은 자리)로
  }
  return best;
}
/** 칩 사각형(가운데 x, y · 앵커) */
export const chipRect = (x, y, s, size, anchor = "middle") => { const w = chipW(s, size); return { x: anchor === "middle" ? x : anchor === "end" ? x - w / 2 : x + w / 2, y, w, h: size * 1.5 }; };
