// ashrain.out — 교실 모니터 「축구」 묶음의 그리기 부품 (kit-soccer.jsx)
// 경기장(잔디·선·골대), 선수(등번호를 쓴 원 — 얼굴·구단 로고는 그리지 않는다, 팀 색만), 공.
// 좌표: 장면마다 세계 좌표(m)를 무대(1600×900) 위로 옮기는 mapper 를 만든다.
import { shade } from "./core.js";
import { SANS } from "./draw.jsx";
import { UText } from "./kit-story.jsx";

/** 세계 좌표(m) → 무대 좌표. flipY: 세계 y 가 위로 늘면 true */
export function mapper({ ox, oy, s, flipY = false }) {
  const p = (q) => [ox + q[0] * s, flipY ? oy - q[1] * s : oy + q[1] * s];
  return { p, s, ox, oy, flipY };
}

/** 테마별 잔디·선 색 */
export function pitchColors(C) {
  return C.name === "light"
    ? { g1: "#d3e5bd", g2: "#c8deb0", line: "#ffffff", lineO: 0.95, edge: "#7d9a5f", net: "#7d9a5f", ink: C.ink }
    : { g1: "#1d3b30", g2: "#214335", line: "#e9f1e3", lineO: 0.62, edge: "#2f5a46", net: "#9fb8a8", ink: C.ink };
}

/** 잔디: 세계 사각형 [x0, y0, x1, y1] 에 띠 무늬(along: "x" 면 세로 띠, "y" 면 가로 띠, band m 간격) */
export function Grass({ M, rect, C, band = 5, along = "x", o = 1, rx = 14 }) {
  const K = pitchColors(C);
  const [a, b] = [M.p([rect[0], rect[1]]), M.p([rect[2], rect[3]])];
  const x0 = Math.min(a[0], b[0]), x1 = Math.max(a[0], b[0]), y0 = Math.min(a[1], b[1]), y1 = Math.max(a[1], b[1]);
  const bands = [];
  const step = band * M.s;
  if (along === "x") for (let x = x0, i = 0; x < x1; x += step, i++) { if (i % 2) bands.push(<rect key={i} x={x} y={y0} width={Math.min(step, x1 - x)} height={y1 - y0} fill={K.g2} />); }
  else for (let y = y0, i = 0; y < y1; y += step, i++) { if (i % 2) bands.push(<rect key={i} x={x0} y={y} width={x1 - x0} height={Math.min(step, y1 - y)} fill={K.g2} />); }
  const id = `gr${Math.round(x0)}_${Math.round(y0)}`;
  return (
    <g opacity={o}>
      <defs><clipPath id={id}><rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} rx={rx} /></clipPath></defs>
      <g clipPath={`url(#${id})`}>
        <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill={K.g1} />
        {bands}
      </g>
      <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} rx={rx} fill="none" stroke={K.edge} strokeWidth={2} />
    </g>
  );
}

/** 경기장 선(세계 좌표 꺾은선들). clip: 세계 사각형 [x0, y0, x1, y1] 밖은 그리지 않는다(잔디 밖으로 삐져나오지 않게) */
export function PLines({ M, C, lines, w = 2.6, o = 1, clip }) {
  const K = pitchColors(C);
  let cp = null, id = null;
  if (clip) {
    const a = M.p([clip[0], clip[1]]), b = M.p([clip[2], clip[3]]);
    const x0 = Math.min(a[0], b[0]), y0 = Math.min(a[1], b[1]);
    id = `pl${Math.round(x0)}_${Math.round(y0)}_${Math.round(Math.abs(b[0] - a[0]))}`;
    cp = <defs><clipPath id={id}><rect x={x0} y={y0} width={Math.abs(b[0] - a[0])} height={Math.abs(b[1] - a[1])} /></clipPath></defs>;
  }
  return (
    <g opacity={o * K.lineO}>
      {cp}
      <g clipPath={id ? `url(#${id})` : undefined}>
        {lines.map((pts, i) => <path key={i} d={"M" + pts.map((q) => M.p(q).map((v) => v.toFixed(1)).join(" ")).join("L")}
          fill="none" stroke={K.line} strokeWidth={w} strokeLinejoin="round" strokeLinecap="round" />)}
      </g>
    </g>
  );
}

/** 호(세계 좌표, 수학 각도 기준이 아니라 세계 x→y 방향 각도 a0→a1, 도) */
export function arcW(c, r, a0, a1, n = 24) {
  const out = [];
  for (let i = 0; i <= n; i++) { const a = ((a0 + ((a1 - a0) * i) / n) * Math.PI) / 180; out.push([c[0] + r * Math.cos(a), c[1] + r * Math.sin(a)]); }
  return out;
}

/**
 * 골대가 위쪽(세계 y = 0 이 골라인, 경기장은 y > 0 쪽)일 때의 페널티 박스·골 에어리어·페널티 마크·아크 선.
 *   cx: 골대 가운데의 세계 x
 */
export function boxLines(cx) {
  const L = [];
  L.push([[cx - 20.16, 0], [cx - 20.16, 16.5], [cx + 20.16, 16.5], [cx + 20.16, 0]]);
  L.push([[cx - 9.16, 0], [cx - 9.16, 5.5], [cx + 9.16, 5.5], [cx + 9.16, 0]]);
  // 페널티 아크: 페널티 마크(11 m)에서 9.15 m, 박스 밖 부분
  const yA = 16.5, dy = yA - 11, half = (Math.acos(dy / 9.15) * 180) / Math.PI;
  L.push(arcW([cx, 11], 9.15, 90 - half, 90 + half));
  return L;
}

/** 골대(위에서 본 모습): 골라인 위 cx 를 가운데로 너비 7.32 m, 깊이 2 m 그물. dir = -1 이면 세계 y 가 줄어드는 쪽으로 */
export function Goal({ M, C, cx, w = 7.32, depth = 2, dir = -1, o = 1 }) {
  const K = pitchColors(C);
  const a = M.p([cx - w / 2, 0]), b = M.p([cx + w / 2, dir * depth]);
  const x0 = Math.min(a[0], b[0]), x1 = Math.max(a[0], b[0]), y0 = Math.min(a[1], b[1]), y1 = Math.max(a[1], b[1]);
  const net = [];
  const st = Math.max(7, M.s * 0.5);
  for (let x = x0 + st; x < x1 - 1; x += st) net.push(<line key={"x" + x} x1={x} x2={x} y1={y0} y2={y1} stroke={K.net} strokeWidth={1} opacity={0.6} />);
  for (let y = y0 + st; y < y1 - 1; y += st) net.push(<line key={"y" + y} x1={x0} x2={x1} y1={y} y2={y} stroke={K.net} strokeWidth={1} opacity={0.6} />);
  return (
    <g opacity={o}>
      <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill={C.name === "light" ? "#eef3e6" : "#16302a"} />
      {net}
      <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill="none" stroke={C.ink} strokeWidth={3} opacity={0.85} />
      <circle cx={x0} cy={dir < 0 ? y1 : y0} r={4.5} fill={C.ink} />
      <circle cx={x1} cy={dir < 0 ? y1 : y0} r={4.5} fill={C.ink} />
    </g>
  );
}

/** 팀 색(팔레트 이름) — 실제 구단 로고·얼굴은 그리지 않고 색만 쓴다 */
export const TEAM = { city: "sky", united: "red", chelsea: "blue", rival: "soft" };

/**
 * 선수: 팀 색 원 + 등번호. label 이 있으면 원 옆에 이름표(lp: "b" 아래, "t" 위, "l" 왼쪽, "r" 오른쪽).
 *   ring: 0~1 — 공을 받을 때 금빛 고리
 */
export function Player({ x, y, n, team = "city", C, r = 22, o = 1, label, lp = "b", ring = 0, lsize = 24, dim = false }) {
  if (o <= 0.001) return null;
  const col = C[TEAM[team] || team] || team;
  const L = label && {
    b: [x, y + r + lsize * 1.05, "middle"], t: [x, y - r - lsize * 0.55, "middle"],
    l: [x - r - 10, y + lsize * 0.34, "end"], r: [x + r + 10, y + lsize * 0.34, "start"],
  }[lp];
  return (
    <g opacity={o}>
      <ellipse cx={x + 3} cy={y + r * 0.82} rx={r * 0.95} ry={r * 0.32} fill="#000" opacity={0.18} />
      {ring > 0 && <circle cx={x} cy={y} r={r + 7 + 5 * (1 - ring)} fill="none" stroke={C.gold} strokeWidth={4} opacity={ring} />}
      <circle cx={x} cy={y} r={r} fill={col} stroke={shade(hexOf(col), 0.55)} strokeWidth={2.6} opacity={dim ? 0.55 : 1} />
      {n != null && <text x={x} y={y + r * 0.36} textAnchor="middle" fontFamily={SANS} fontSize={r * (String(n).length > 1 ? 0.92 : 1.02)}
        fontWeight={800} fill={C.paper}>{n}</text>}
      {L && <UText x={L[0]} y={L[1]} s={label} size={lsize} weight={700} anchor={L[2]} fill={C.ink} halo={C.halo} C={C} />}
    </g>
  );
}
const hexOf = (c) => (typeof c === "string" && c.startsWith("#") ? c : "#888888");

/** 상대 선수(번호 없음, 옅게) */
export function Rival({ x, y, C, r = 17, o = 1 }) {
  if (o <= 0.001) return null;
  return (
    <g opacity={o * 0.75}>
      <circle cx={x} cy={y} r={r} fill={C.soft} fillOpacity={0.45} stroke={C.soft} strokeWidth={2.2} />
    </g>
  );
}

/** 공: h(0~1) 만큼 떠 있으면 그림자와 떨어져 위로 그리고 조금 크게 */
export function Ball({ x, y, r = 10, h = 0, C, o = 1 }) {
  if (o <= 0.001) return null;
  const lift = h * 34, k = 1 + 0.45 * h;
  const R = r * k;
  const pent = [0, 1, 2, 3, 4].map((i) => { const a = ((-90 + 72 * i) * Math.PI) / 180; return [x + 0.42 * R * Math.cos(a), y - lift + 0.42 * R * Math.sin(a)]; });
  return (
    <g opacity={o}>
      <ellipse cx={x} cy={y + r * 0.7} rx={r * (1 - 0.35 * h)} ry={r * 0.36 * (1 - 0.35 * h)} fill="#000" opacity={0.28 - 0.12 * h} />
      <circle cx={x} cy={y - lift} r={R} fill="#fbfbf7" stroke="#202020" strokeWidth={1.6} />
      <path d={"M" + pent.map((q) => q.map((v) => v.toFixed(1)).join(" ")).join("L") + "Z"} fill="#202020" />
    </g>
  );
}

/** 골! 글자 반짝 */
export function GoalFlash({ x, y, k, C, s = "골!" }) {
  if (k <= 0.001) return null;
  return <UText x={x} y={y} s={s} size={44 + 10 * k} weight={900} anchor="middle" fill={C.gold} halo={C.halo} opacity={Math.min(1, k * 1.6)} C={C} />;
}

/** 방향 안내 글자(→) */
export function DirNote({ x, y, s, C, o = 1, anchor = "start", size = 22 }) {
  return <UText x={x} y={y} s={s} size={size} weight={650} anchor={anchor} fill={C.soft} opacity={o} C={C} />;
}
