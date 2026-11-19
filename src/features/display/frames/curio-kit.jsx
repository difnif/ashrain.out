// ashrain.out — 수학 호기심 액자 공용 그리기 부품 (frames/curio-kit.jsx)
// 축구 · 농구 · 야구 직선 액자와 공 꺼내기 · 알파벳 카드 · 일렬로 세우기 · 학년별 뽑기 액자가 함께 쓴다.
//   · FitText — 칸 너비에 맞춰 글자 크기를 줄여 쓰는 MText
//   · Lines — 판서 줄을 시각에 맞춰 하나씩(마지막 식 줄은 금빛 · 크게)
//   · Panel — 둥근 판(설명 칸) · clipLine — 무한 직선을 사각형 안 선분으로 · seq — 장면 박자
import { MText, mathWidth, SANS } from "../draw.jsx";
import { seg } from "../core.js";

/** 너비 maxW 안에 들도록 size 를 줄인 MText(최소 minSize) */
export function FitText({ s, size = 28, maxW, minSize = 16, ...rest }) {
  if (!s) return null;
  let k = size;
  if (maxW) { const w = mathWidth(s, size, rest.weight || 500); if (w > maxW) k = Math.max(minSize, (size * maxW) / w); }
  return <MText s={s} size={k} {...rest} />;
}

/**
 * 판서 줄: lines = [{ s, at(나타나는 시각), hi?, small?, col? }] — t 가 at 을 지나면 0.4초에 걸쳐 나타난다.
 * hi 줄은 금빛으로 크게, small 줄은 옅게 작게. 반환 높이만큼 아래로 쌓는다.
 */
export function Lines({ x, y, lines, t, C, size = 26, lh = 52, maxW, o = 1, hiSize }) {
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
          <FitText x={x} y={yy} s={L.s} size={sz} maxW={maxW} weight={L.hi ? 800 : L.small ? 600 : 650}
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
