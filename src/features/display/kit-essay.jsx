// ashrain.out — 교실 모니터 「서술형」 묶음의 그리기 부품 (kit-essay.jsx)
// 선로(침목 + 두 줄 레일) · 전차 · 위에서 본 자동차 · 왕복 2차로 · 옆에서 본 자동차 · 굽은 화살표 · 가위바위보 손 · 동아리 그림.
import { shade } from "./core.js";
import { SANS, Path } from "./draw.jsx";

/** 3차 베지에 곡선을 n 토막으로 */
export function bez(p0, p1, p2, p3, n = 28) {
  const out = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, u = 1 - t;
    out.push([u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
      u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]]);
  }
  return out;
}
/** 가로로 나아가는 S자 곡선(양 끝이 수평) */
export const sCurve = (p, q, n = 28) => bez(p, [p[0] + (q[0] - p[0]) * 0.5, p[1]], [q[0] - (q[0] - p[0]) * 0.5, q[1]], q, n);

/** 꺾은선의 길이와 비율 위치 · 방향 */
export function polyInfo(pts) {
  const acc = [0];
  for (let i = 1; i < pts.length; i++) acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const L = acc.at(-1);
  const at = (k) => {
    const d = Math.max(0, Math.min(1, k)) * L;
    let i = 1;
    while (i < pts.length - 1 && acc[i] < d) i++;
    const s = (d - acc[i - 1]) / ((acc[i] - acc[i - 1]) || 1);
    const p = [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * s, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * s];
    const ang = (Math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0]) * 180) / Math.PI;
    return { p, ang };
  };
  return { L, at };
}

/** 선로: 침목 + 레일 두 줄 */
export function Track({ pts, C, o = 1, w = 7, hi }) {
  if (o <= 0.001 || pts.length < 2) return null;
  const { L, at } = polyInfo(pts);
  const sleepers = [];
  for (let d = 8; d < L - 4; d += 17) {
    const { p, ang } = at(d / L), r = (ang * Math.PI) / 180, nx = -Math.sin(r), ny = Math.cos(r);
    sleepers.push(<line key={d} x1={p[0] + nx * (w + 6)} y1={p[1] + ny * (w + 6)} x2={p[0] - nx * (w + 6)} y2={p[1] - ny * (w + 6)}
      stroke={C.name === "light" ? "#a08560" : "#6d5a43"} strokeWidth={4} strokeLinecap="round" />);
  }
  const rail = (s) => {
    const out = pts.map((p, i) => {
      const q = pts[Math.min(pts.length - 1, i + 1)], b = pts[Math.max(0, i - 1)];
      const dx = q[0] - b[0], dy = q[1] - b[1], l = Math.hypot(dx, dy) || 1;
      return [p[0] - (dy / l) * w * s, p[1] + (dx / l) * w * s];
    });
    return "M" + out.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L");
  };
  const col = C.name === "light" ? "#6b6f77" : "#c9ccd4";
  return (
    <g opacity={o}>
      {hi && <path d={"M" + pts.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L")} fill="none" stroke={hi} strokeWidth={w * 2 + 22} strokeOpacity={0.22} strokeLinecap="round" strokeLinejoin="round" />}
      {sleepers}
      <path d={rail(1)} fill="none" stroke={col} strokeWidth={2.6} />
      <path d={rail(-1)} fill="none" stroke={col} strokeWidth={2.6} />
    </g>
  );
}

/** 전차(위에서 본 모습) */
export function Tram({ x, y, ang = 0, C, o = 1, col, len = 46, wid = 22 }) {
  if (o <= 0.001) return null;
  const c = col || C.gold;
  return (
    <g opacity={o} transform={`translate(${x} ${y}) rotate(${ang})`}>
      <rect x={-len / 2} y={-wid / 2} width={len} height={wid} rx={7} fill={c} stroke={shade(c, 0.5)} strokeWidth={2} />
      <rect x={-len / 2 + 6} y={-wid / 2 + 4} width={len - 12} height={wid - 8} rx={4} fill="#fff" fillOpacity={0.35} />
      <rect x={len / 2 - 9} y={-wid / 2 + 3} width={5} height={wid - 6} rx={2} fill={shade(c, 0.45)} />
    </g>
  );
}

/** 위에서 본 자동차: ang = 0 이면 오른쪽(→)으로 향한다 */
export function Car({ x, y, ang = 0, C, col, o = 1, len = 70, wid = 34, label }) {
  if (o <= 0.001) return null;
  const c = col || C.soft;
  const dk = shade(c, 0.5);
  return (
    <g opacity={o} transform={`translate(${x} ${y}) rotate(${ang})`}>
      {[[-len * 0.3, -wid / 2], [len * 0.28, -wid / 2], [-len * 0.3, wid / 2], [len * 0.28, wid / 2]].map(([wx, wy], i) =>
        <rect key={i} x={wx - 8} y={wy - 4} width={16} height={8} rx={3} fill="#1b1b1b" />)}
      <rect x={-len / 2} y={-wid / 2} width={len} height={wid} rx={wid * 0.36} fill={c} stroke={dk} strokeWidth={2.2} />
      <path d={`M${len * 0.12} ${-wid * 0.36}L${len * 0.3} ${-wid * 0.3}L${len * 0.3} ${wid * 0.3}L${len * 0.12} ${wid * 0.36}Z`} fill={dk} opacity={0.75} />
      <path d={`M${-len * 0.36} ${-wid * 0.3}L${-len * 0.26} ${-wid * 0.33}L${-len * 0.26} ${wid * 0.33}L${-len * 0.36} ${wid * 0.3}Z`} fill={dk} opacity={0.6} />
      {label && <text x={-len * 0.06} y={6} textAnchor="middle" fontFamily={SANS} fontSize={15} fontWeight={800} fill={C.paper} transform={ang > 90 || ang < -90 ? "rotate(180)" : undefined}>{label}</text>}
    </g>
  );
}

/** 굽은 화살표: pts 를 따라 그리고 끝에 머리 */
export function PathArrow({ pts, stroke, sw = 4, h = 16, o = 1, dash }) {
  if (o <= 0.001 || !pts || pts.length < 2) return null;
  const q = pts.at(-1), p = pts[Math.max(0, pts.length - 4)];
  const a = Math.atan2(q[1] - p[1], q[0] - p[0]);
  const hd = [[q[0] - h * Math.cos(a - 0.45), q[1] - h * Math.sin(a - 0.45)], q, [q[0] - h * Math.cos(a + 0.45), q[1] - h * Math.sin(a + 0.45)]];
  const tail = [q[0] - h * 0.6 * Math.cos(a), q[1] - h * 0.6 * Math.sin(a)];
  const body = pts.slice(0, -1).filter((r) => (r[0] - q[0]) * Math.cos(a) + (r[1] - q[1]) * Math.sin(a) < -h * 0.6);
  return (
    <g opacity={o}>
      <Path pts={[...body, tail]} stroke={stroke} sw={sw} dash={dash} />
      <Path pts={hd} closed fill={stroke} stroke={stroke} sw={2} />
    </g>
  );
}

/** 왕복 2차로와 인도(위에서 본 모습): top~mid 위 차로(←), mid~bot 아래 차로(→), bot~walk 인도 */
export function Road({ x0, x1, top, mid, bot, walk, C, o = 1 }) {
  if (o <= 0.001) return null;
  const dk = C.name !== "light";
  const asphalt = dk ? "#2f3549" : "#bcb5a5", line = dk ? "#dfe3ec" : "#fffdf6", yel = dk ? "#e9b949" : "#d69b10";
  const side = dk ? "#3c4256" : "#d9d0bc", curb = dk ? "#8c91a5" : "#978d79";
  const paving = [];
  for (let x = x0 + 30; x < x1; x += 46) paving.push(<line key={x} x1={x} y1={bot + 4} x2={x} y2={walk} stroke={curb} strokeOpacity={0.35} strokeWidth={1.4} />);
  const arrow = (x, y, s, key) => (
    <path key={key} d={`M${x - 26 * s} ${y}L${x + 10 * s} ${y}M${x + 2 * s} ${y - 9}L${x + 14 * s} ${y}L${x + 2 * s} ${y + 9}`}
      fill="none" stroke={line} strokeOpacity={0.3} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />
  );
  const uy = (top + mid) / 2, ly = (mid + bot) / 2;
  return (
    <g opacity={o}>
      <rect x={x0} y={top} width={x1 - x0} height={bot - top} rx={4} fill={asphalt} />
      <rect x={x0} y={bot} width={x1 - x0} height={walk - bot} fill={side} />
      {paving}
      <line x1={x0} x2={x1} y1={top + 6} y2={top + 6} stroke={line} strokeOpacity={0.7} strokeWidth={3} />
      <line x1={x0} x2={x1} y1={bot - 6} y2={bot - 6} stroke={line} strokeOpacity={0.7} strokeWidth={3} />
      <line x1={x0} x2={x1} y1={mid - 4} y2={mid - 4} stroke={yel} strokeWidth={3} />
      <line x1={x0} x2={x1} y1={mid + 4} y2={mid + 4} stroke={yel} strokeWidth={3} />
      <line x1={x0} x2={x1} y1={bot} y2={bot} stroke={curb} strokeWidth={5} />
      {[140, 1440].map((x, i) => arrow(x, uy, -1, "u" + i))}
      {[140, 1440].map((x, i) => arrow(x, ly, 1, "l" + i))}
    </g>
  );
}

/** 옆에서 본 자동차: (x, y) = 바닥 가운데, dir = 1 이면 오른쪽(→)으로 향한다 */
export function SideCar({ x, y, C, col, len = 44, h = 15, dir = 1, o = 1 }) {
  if (o <= 0.001) return null;
  const c = col || C.soft, dk = shade(c, 0.5), wr = h * 0.36, b = -wr, m = b - h * 0.6, r = b - h;
  return (
    <g opacity={o} transform={`translate(${x} ${y}) scale(${dir} 1)`}>
      <path d={`M${-len / 2} ${b}L${-len / 2} ${m + 3}Q${-len / 2} ${m} ${-len * 0.42} ${m}L${-len * 0.24} ${m}L${-len * 0.12} ${r}L${len * 0.16} ${r}L${len * 0.3} ${m}L${len * 0.44} ${m + 1}Q${len / 2} ${m + 2} ${len / 2} ${m + 6}L${len / 2} ${b}Z`}
        fill={c} stroke={dk} strokeWidth={1.6} strokeLinejoin="round" />
      <circle cx={-len * 0.28} cy={b} r={wr} fill="#1b1b1b" />
      <circle cx={len * 0.28} cy={b} r={wr} fill="#1b1b1b" />
    </g>
  );
}

/* ── 가위바위보 손(손등 쪽, 손가락이 위) — 0 가위 · 1 바위 · 2 보 ── */
export const HAND_COL = ["sky", "coral", "leaf"];
export function Hand({ kind, x, y, s = 40, C, o = 1, col }) {
  if (o <= 0.001) return null;
  const c = col || C[HAND_COL[kind]];
  const dk = shade(c, 0.55);
  const u = s / 40;
  const finger = (dx, len, rot = 0, key) => (
    <rect key={key} x={-4.2} y={-len} width={8.4} height={len + 4} rx={4.2} fill={c} stroke={dk} strokeWidth={1.6}
      transform={`translate(${dx} -6) rotate(${rot})`} />
  );
  const fist = (
    <g>
      <rect x={-15} y={-8} width={30} height={22} rx={8} fill={c} stroke={dk} strokeWidth={1.8} />
      {[-10.5, -3.5, 3.5, 10.5].map((dx, i) => <circle key={i} cx={dx} cy={-8} r={4.4} fill={c} stroke={dk} strokeWidth={1.5} />)}
      <path d="M-15 4 Q-20 -1 -13 -4" fill="none" stroke={dk} strokeWidth={1.6} />
    </g>
  );
  let g;
  if (kind === 1) g = fist;
  else if (kind === 0) g = <g>{finger(-4, 22, -14, "a")}{finger(5, 22, 14, "b")}{fist}</g>;
  else g = (
    <g>
      {[-10.5, -3.5, 3.5, 10.5].map((dx, i) => finger(dx, [17, 21, 22, 18][i], (dx / 10.5) * 6, i))}
      <rect x={-4} y={-14} width={8} height={18} rx={4} fill={c} stroke={dk} strokeWidth={1.5} transform="translate(-16 6) rotate(-48)" />
      <rect x={-15} y={-8} width={30} height={22} rx={8} fill={c} stroke={dk} strokeWidth={1.8} />
    </g>
  );
  return <g opacity={o} transform={`translate(${x} ${y}) scale(${u})`}>{g}</g>;
}

/** 반티(무늬 없는 티셔츠) — (x, y) 가운데, s = 폭 */
export function Shirt({ x, y, s = 44, col, C, o = 1 }) {
  if (o <= 0.001) return null;
  const c = col || C.sky, dk = shade(c, 0.55), u = s / 44;
  return (
    <g opacity={o} transform={`translate(${x} ${y}) scale(${u})`}>
      <path d="M-9 -18 Q0 -12 9 -18 L22 -12 L28 -2 L19 3 L16 0 L16 20 L-16 20 L-16 0 L-19 3 L-28 -2 L-22 -12 Z"
        fill={c} stroke={dk} strokeWidth={1.8} strokeLinejoin="round" />
      <path d="M-9 -18 Q0 -10 9 -18" fill="none" stroke={dk} strokeWidth={1.6} />
    </g>
  );
}

/* ── 동아리 그림 ── */
export function ClubIcon({ kind, x, y, C, s = 1 }) {
  const ink = C.ink;
  const g = {
    0: <g>{/* 음표 두 개 */}
      <circle cx={-8} cy={10} r={6} fill={ink} /><circle cx={10} cy={6} r={6} fill={ink} />
      <path d="M-2.5 10 V-12 L15.5 -16 V6" fill="none" stroke={ink} strokeWidth={3} />
      <path d="M-2.5 -12 L15.5 -16 V-10 L-2.5 -6 Z" fill={ink} /></g>,
    1: <g>{/* 주사위 */}
      <rect x={-14} y={-14} width={28} height={28} rx={6} fill={C.card} stroke={ink} strokeWidth={2.4} />
      {[[-6, -6], [6, 6], [0, 0], [6, -6], [-6, 6]].map(([a, b], i) => <circle key={i} cx={a} cy={b} r={2.6} fill={ink} />)}</g>,
    2: <g>{/* 사진기 */}
      <rect x={-17} y={-9} width={34} height={22} rx={4} fill="none" stroke={ink} strokeWidth={2.6} />
      <rect x={-7} y={-14} width={12} height={6} rx={2} fill={ink} />
      <circle cx={0} cy={2} r={7} fill="none" stroke={ink} strokeWidth={2.6} /></g>,
    3: <g>{/* 냄비 */}
      <path d="M-15 -2 H15 V8 Q15 15 8 15 H-8 Q-15 15 -15 8 Z" fill="none" stroke={ink} strokeWidth={2.6} />
      <path d="M-18 -2 H18" stroke={ink} strokeWidth={2.6} strokeLinecap="round" />
      <path d="M-4 -8 H4" stroke={ink} strokeWidth={3} strokeLinecap="round" />
      <path d="M-15 2 H-21 M15 2 H21" stroke={ink} strokeWidth={2.6} strokeLinecap="round" /></g>,
  }[kind];
  return <g transform={`translate(${x} ${y}) scale(${s})`}>{g}</g>;
}
