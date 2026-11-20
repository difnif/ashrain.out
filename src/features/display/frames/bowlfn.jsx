// ashrain.out — 수학 호기심 액자: 볼링으로 보는 일차함수와 점수 계산 (frames/bowlfn.jsx)
// 레인을 위에서 본 그림(왼쪽 파울 선 → 오른쪽 핀). 가로 = 파울 선에서 간 거리(ft), 세로 = 보드 번호(오른쪽 끝 1 ~ 왼쪽 끝 39).
// 곧게 굴린 공은 직선 — 파울 선의 보드 b 와 15 ft 화살표의 보드 c 로 정해지고, 핀(60 ft)에서는 4c − 3b 번 보드.
//   중등: 두 점 (0, b) · (15, c) 를 지나는 직선의 식 → x = 60 대입.  초등: 15 ft 에 몇 칸 → 60 ft 는 4배(비례).
// 아래 점수표: 스트라이크(10 + 다음 두 번) · 스페어(10 + 다음 한 번) 보너스를 덧셈으로 보여 준다.
// 그림은 길이를 줄이고 폭을 늘린 것(가로 · 세로 눈금이 다르다) — 핀 자리는 가로로 더 벌려 그린다.
// 풀이 상세: 오른쪽 설명 판 · 최소화: 레인과 점수표를 크게, 칩 하나. 계산: ../curio/bowl.js
import { memo } from "react";
import { W, H, MText, SceneTitle, Path, SANS, textW } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW } from "../kit-story.jsx";
import { SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, fs, num, lineOf, eqText } from "../curio/kit.js";
import { LANE, ARROWS, PINS, ALL, BT, bowlAt, bowlGame, bowlSteps, frameCalc, entryName } from "../curio/bowl.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel, Small, BigChip, bigW, besideLine, pickSpot } from "./curio-kit.jsx";

const LSK = "ash.display.curio.bowl";
const PANEL = { x: 1162, y: 150, w: 400, h: 720 };
/** 레인 그림 자리: 파울 선 x · 60 ft x · 보드 20 의 y · 보드 한 칸 높이 · 핀 줄 사이 */
const LAY = {
  full: { x0: 96, x60: 920, deck: 40, cy: 392, sy: 6.8, box: [40, 150, 1140, 600], sheet: [40, 616, 1140, 760], calc: 800 },
  mini: { x0: 110, x60: 1290, deck: 52, cy: 400, sy: 8.2, box: [36, 150, 1564, 632], sheet: [36, 650, 1564, 820], calc: 856 },
};
const ftX = (L, ft) => (ft <= 60 ? L.x0 + (ft / 60) * (L.x60 - L.x0) : L.x60 + ((ft - 60) / 0.866) * L.deck);
const bY = (L, b) => L.cy - (b - 20) * L.sy;
const COL = {
  dark: { wood: "#c9925a", wood2: "#b98450", gut: "#2b2f3a", line: "#7a4d24", appr: "#d9a86e", pin: "#fbfbf7", neck: "#d23c3c" },
  light: { wood: "#e2b47c", wood2: "#d6a66e", gut: "#5b6170", line: "#8a5a2c", appr: "#ecc58e", pin: "#ffffff", neck: "#d23c3c" },
};

/* ══════════ 레인 ══════════ */
const Lane = memo(function Lane({ ex, C, mode }) {
  const L = LAY[ex], K = COL[C.name === "light" ? "light" : "dark"];
  const top = bY(L, 39.5), bot = bY(L, 0.5), gw = L.sy * 2.6;
  const xEnd = ftX(L, 60 + 3 * 0.866) + L.deck * 0.9;
  const isM = mode === "m";
  const ink = C.name === "light" ? "#2a1d10" : "#fff4e6";
  const boards = [];
  for (let b = 1; b < 39; b++) boards.push(<line key={b} x1={L.x0} x2={xEnd} y1={bY(L, b + 0.5)} y2={bY(L, b + 0.5)} stroke={K.line} strokeOpacity={b % 5 === 0 ? 0.22 : 0.09} strokeWidth={1} />);
  const arrows = ARROWS.map((b) => { const x = ftX(L, 15), y = bY(L, b); return <path key={b} d={`M${x - 9} ${y - 5}L${x + 9} ${y}L${x - 9} ${y + 5}Z`} fill="#3b2a1a" opacity={0.75} />; });
  const dots = [3, 5, 8, 11, 14, 26, 29, 32, 35, 37].map((b) => { const p = [ftX(L, 7), bY(L, b)]; return <circle key={b} cx={p[0]} cy={p[1]} r={2.6} fill="#3b2a1a" opacity={0.7} />; });
  const TN = { 0: "0 파울 선", 15: "15 화살표", 60: isM ? "60 핀" : "60 ft 핀" };
  const ticks = [0, 15, 30, 45, 60].map((ft) => <g key={ft}><line x1={ftX(L, ft)} x2={ftX(L, ft)} y1={bot + gw} y2={bot + gw + 7} stroke={ink} opacity={0.5} /><text x={ftX(L, ft)} y={bot + gw + 24} textAnchor="middle" fontFamily={SANS} fontSize={14} fontWeight={700} fill={C.soft}>{TN[ft] || ft}</text></g>);
  const bl = [1, 5, 10, 15, 20, 25, 30, 35, 39].map((b) => <text key={b} x={L.x0 - 34} y={bY(L, b) + 5} textAnchor="end" fontFamily={SANS} fontSize={13} fontWeight={700} fill={C.soft}>{b}</text>);
  return (
    <g>
      {/* 도랑 · 바닥 */}
      <rect x={L.x0 - 30} y={top - gw} width={xEnd - L.x0 + 30} height={bot - top + 2 * gw} rx={10} fill={K.gut} />
      <rect x={L.x0 - 30} y={top} width={30} height={bot - top} fill={K.appr} />
      <rect x={L.x0} y={top} width={xEnd - L.x0} height={bot - top} fill={K.wood} />
      <rect x={ftX(L, 59)} y={top} width={xEnd - ftX(L, 59)} height={bot - top} fill={K.wood2} />
      {boards}
      {/* 파울 선 */}
      <line x1={L.x0} x2={L.x0} y1={top} y2={bot} stroke="#c62828" strokeWidth={3} />
      {dots}{arrows}
      {/* 핀 자리 표시 */}
      {ALL.map((n) => { const [x, y] = pinXY(L, n); return <circle key={n} cx={x} cy={y} r={L.sy * 1.1} fill="none" stroke="#3b2a1a" strokeOpacity={0.35} />; })}
      {ticks}
      {bl}
      <text x={L.x0 - 34} y={bot + gw + 24} textAnchor="end" fontFamily={SANS} fontSize={13} fontWeight={750} fill={C.soft}>{isM ? "y(보드)" : "보드"}</text>
      <text x={xEnd} y={bot + gw + 24} textAnchor="end" fontFamily={SANS} fontSize={13} fontWeight={750} fill={C.soft}>{isM ? "x(ft)" : ""}</text>
    </g>
  );
});
const pinXY = (L, n) => [ftX(L, PINS[n][0]), bY(L, PINS[n][1])];

function Pin({ x, y, r, K, o = 1, lying, ang = 0 }) {
  if (o <= 0.01) return null;
  if (lying) return <g opacity={o} transform={`rotate(${ang} ${x} ${y})`}><rect x={x - r * 1.9} y={y - r * 0.55} width={r * 3.8} height={r * 1.1} rx={r * 0.55} fill={K.pin} stroke="#555" strokeOpacity={0.4} /><rect x={x - r * 0.9} y={y - r * 0.55} width={r * 0.5} height={r * 1.1} fill={K.neck} /></g>;
  return (
    <g opacity={o}>
      <ellipse cx={x + r * 0.2} cy={y + r * 0.3} rx={r} ry={r * 0.8} fill="#000" opacity={0.25} />
      <circle cx={x} cy={y} r={r} fill={K.pin} stroke="#555" strokeOpacity={0.45} strokeWidth={1.2} />
      <circle cx={x} cy={y} r={r * 0.62} fill="none" stroke={K.neck} strokeWidth={r * 0.22} />
    </g>
  );
}

/* ══════════ 장면 ══════════ */
/** 핀 상태(그림): 지금 투구 i 의 시각 t */
function pinsNow(g, i, t) {
  const o = g.rolls[i];
  if (!o) return { stand: [], fall: [] };
  const fresh = o.before.length === 10;
  const kd = new Map(o.down.map((d) => [d.n, d]));
  const stand = [], fall = [];
  for (const n of ALL) {
    if (!o.before.includes(n)) continue;
    const d = kd.get(n);
    const t0 = BT.fall[0] + 60 + (d ? d.k : 0) * 75;
    if (d && t >= t0) fall.push({ n, d, k: seg(t, t0, t0 + 320, E.out), clear: seg(t, BT.clear[0], BT.clear[1]) });
    else stand.push({ n, o: fresh ? seg(t, 0, 500) : 1 });
  }
  return { stand, fall };
}
export function BowlArt({ C, mode, ex, at }) {
  const { g, i, t } = at;
  const L = LAY[ex], K = COL[C.name === "light" ? "light" : "dark"], isM = mode === "m", mini = ex === "mini";
  const over = i >= g.rolls.length;
  const o = over ? g.rolls[g.rolls.length - 1] : g.rolls[i];
  const tt = over ? BT.roll : t;
  const ka = seg(tt, BT.aim[0], BT.aim[1]);
  const kt = seg(tt, BT.travel[0], BT.travel[1], (u) => u);
  const ball = kt > 0 && kt < 1 ? [lerp(L.x0, L.x60, kt), bY(L, o.b + (o.c - o.b) / 15 * 60 * kt)] : null;
  const deckK = seg(tt, BT.travel[1], BT.fall[1], E.out);
  const ballDeck = deckK > 0 && deckK < 1 && o.entry >= 0.5 && o.entry <= 39.5 ? [lerp(L.x60, ftX(L, 64), deckK), bY(L, o.entry + (o.c - o.b) / 15 * 4 * deckK)] : null;
  const P = pinsNow(g, over ? g.rolls.length - 1 : i, tt);
  const pr = L.sy * 1.25;
  const A = [L.x0, bY(L, o.b)], B = [ftX(L, 15), bY(L, o.c)], Z = [L.x60, bY(L, clamp(o.entry, -1, 41))];
  const tc = C.name === "light" ? "#0f766e" : "#7fe3d3";
  const km = seg(tt, BT.math, BT.math + 500);
  const res = seg(tt, BT.fall[1] - 300, BT.fall[1] + 200) * (1 - seg(tt, BT.clear[1] - 200, BT.clear[1]));
  const word = o.mark === "X" ? "스트라이크!" : o.mark === "/" ? "스페어!" : o.entry < 0.5 || o.entry > 39.5 ? "도랑(거터)" : o.split ? `스플릿! ${o.n}개` : `${o.n}개`;
  const eq = eqText(lineOf([0, o.b], [15, o.c]));
  const LS = mini ? 25 : 22;   // 좌표 칩 — 그림에서 눈에 띄게
  const lbl = (p, s2, dy, col, op) => <Chip x={p[0]} y={p[1] + dy} s={s2} size={LS} C={C} color={col} o={op} />;
  // 기울기 칩(금테 · 크게): 중등 「기울기 2/15」, 초등 「15 ft에 2칸」 — 직선 가운데 위 · 아래 중 빈 쪽
  const d0 = o.c - o.b, bs = mini ? 36 : 30;
  const slopeTxt = isM ? `기울기 ${fs(o.a[0], o.a[1])}` : d0 === 0 ? "15 ft에 0칸 — 똑바로" : `15 ft에 ${Math.abs(d0)}칸 ${d0 > 0 ? "왼쪽" : "오른쪽"}으로`;
  const sbw = bigW(slopeTxt, bs);
  const aLbl = isM ? `y절편 (0, ${o.b})` : `${o.b}번`;
  const slopeAt = pickSpot([0.45, 0.6, 0.32, 0.75].flatMap((f) => [besideLine(A, Z, sbw, bs * 1.5, f, -1), besideLine(A, Z, sbw, bs * 1.5, f, 1)]), sbw, bs * 1.5,
    [{ x: A[0] + 4, y: A[1] + (o.c >= o.b ? LS + 10 : -(LS + 10)), w: chipW(aLbl, LS), h: LS * 1.5 }, { x: B[0], y: B[1] + (o.c >= o.b ? -(LS + 10) : LS + 10), w: chipW(`(15, ${o.c})`, LS), h: LS * 1.5 },
      { x: Z[0] - 60, y: Z[1] + (o.entry >= 20 ? -(LS + 14) : LS + 14), w: 160, h: LS * 1.5 }, { x: ftX(L, 61.3), y: bY(L, 20), w: 4 * L.deck + 40, h: 300 }],
    [L.x0 + 20, bY(L, 39), ftX(L, 59), bY(L, 1)]);
  return (
    <g>
      <rect x={L.box[0]} y={L.box[1]} width={L.box[2] - L.box[0]} height={L.box[3] - L.box[1]} rx={16} fill={C.card} fillOpacity={C.name === "light" ? 0.55 : 0.4} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lane ex={ex} C={C} mode={mode} />
      {/* 겨냥 직선(점선) — 파울 선 · 화살표 · 핀 */}
      {ka > 0 && (
        <g opacity={ka * (over ? 0.5 : 1)}>
          <Path pts={[A, Z]} stroke={tc} sw={2.6} dash="10 8" o={0.9} />
          <circle cx={A[0]} cy={A[1]} r={6} fill={tc} stroke="#fff" strokeWidth={1.6} />
          <circle cx={B[0]} cy={B[1]} r={6} fill={tc} stroke="#fff" strokeWidth={1.6} />
          {lbl([A[0] + 4 + chipW(aLbl, LS) / 2 - 10, A[1]], aLbl, o.c >= o.b ? LS + 10 : -(LS + 10), isM ? (C.name === "light" ? "#0f766e" : "#7fe3d3") : undefined, 1)}
          {lbl(B, isM ? `(15, ${o.c})` : `${o.c}번`, o.c >= o.b ? -(LS + 10) : LS + 10, undefined, 1)}
          <BigChip x={slopeAt[0]} y={slopeAt[1]} s={slopeTxt} size={bs} C={C} />
        </g>
      )}
      {/* 공이 지난 길 */}
      {kt > 0 && <Path pts={[A, ball || Z]} stroke={C.gold} sw={4} o={0.85 * (1 - seg(tt, BT.clear[0], BT.clear[1]) * 0.8)} />}
      {/* 핀 */}
      {P.fall.map(({ n, d, k, clear }) => {
        const [x, y] = pinXY(L, n);
        const from = d.by ? pinXY(L, d.by) : [x - 30, bY(L, o.entry)];
        const dx = x - from[0], dy = y - from[1], nn = Math.hypot(dx, dy) || 1;
        const q = [x + (dx / nn) * 16 * k, y + (dy / nn) * 16 * k];
        return <Pin key={n} x={q[0]} y={q[1]} r={pr} K={K} lying ang={(Math.atan2(dy, dx) * 180) / Math.PI} o={(1 - clear) * (0.5 + 0.5 * (1 - k))} />;
      })}
      {P.stand.map(({ n, o: op }) => { const [x, y] = pinXY(L, n); return <Pin key={n} x={x} y={y} r={pr} K={K} o={op} />; })}
      {/* 공 */}
      {(ball || ballDeck) && (() => { const q = ball || ballDeck; return <g><ellipse cx={q[0] + 3} cy={q[1] + 4} rx={L.sy * 1.7} ry={L.sy * 1.3} fill="#000" opacity={0.25} /><circle cx={q[0]} cy={q[1]} r={L.sy * 1.6} fill="#2d4fd8" stroke="#0d1b6b" strokeWidth={1.5} /><circle cx={q[0] - 4} cy={q[1] - 4} r={2.4} fill="#0d1b6b" /><circle cx={q[0] + 2} cy={q[1] - 6} r={2.2} fill="#0d1b6b" /><circle cx={q[0] + 1} cy={q[1] + 2} r={2.4} fill="#0d1b6b" /></g>; })()}
      {/* 핀에서 지나는 보드 */}
      {kt >= 1 && km > 0 && lbl([Z[0] - 60, Z[1]], isM ? `(60, ${num(o.entry)})` : `${num(o.entry)}번 보드`, o.entry >= 20 ? -(LS + 14) : LS + 14, C.gold, km * (1 - seg(tt, BT.clear[0], BT.clear[1])))}
      {/* 결과 */}
      {res > 0 && !over && <UText x={mini ? ftX(L, 50) : (L.box[0] + L.box[2]) / 2} y={L.box[1] + (mini ? 54 : 60)} s={word} size={mini ? 44 : 40} weight={900} anchor="middle" fill={o.mark === "X" || o.mark === "/" ? C.gold : C.ink} halo={C.halo} opacity={res} C={C} />}
      {mini && !over && <Chip x={L.box[0] + 16} y={L.box[1] + 36} s={isM ? `${eq} → 핀에서 ${num(o.entry)}번 보드` : `15 ft에 ${Math.abs(o.c - o.b)}칸 → 60 ft에 ${Math.abs(4 * (o.c - o.b))}칸 → ${num(o.entry)}번 보드`} size={21} C={C} anchor="start" o={ka} />}
      <Sheet C={C} ex={ex} g={g} i={i} t={t} over={over} />
      {over && <GameEnd C={C} ex={ex} g={g} t={t} />}
      {!mini && <BowlPanel C={C} mode={mode} g={g} i={i} t={t} k={at.k} over={over} />}
      {mini && <BowlMiniCalc C={C} ex={ex} g={g} i={i} t={t} over={over} />}
    </g>
  );
}
function GameEnd({ C, ex, g, t }) {
  const L = LAY[ex], k = seg(t, 0, 600) * (1 - seg(t, BT.gameEnd - 500, BT.gameEnd));
  return (
    <g opacity={k}>
      <rect x={L.box[0]} y={L.box[1]} width={L.box[2] - L.box[0]} height={L.box[3] - L.box[1]} rx={16} fill={C.name === "light" ? "#fffaf0" : "#0b1020"} opacity={0.55} />
      <UText x={(L.box[0] + L.box[2]) / 2} y={(L.box[1] + L.box[3]) / 2 - 6} s={`게임 끝 — ${g.name} ${g.total}점`} size={52} weight={900} anchor="middle" fill={C.gold} halo={C.halo} C={C} />
      <UText x={(L.box[0] + L.box[2]) / 2} y={(L.box[1] + L.box[3]) / 2 + 46} s={`스트라이크 ${g.frames.filter((F) => F.kind === "strike").length}번 · 스페어 ${g.frames.filter((F) => F.kind === "spare").length}번`} size={26} weight={750} anchor="middle" fill={C.ink} halo={C.halo} C={C} />
    </g>
  );
}

/* ══════════ 점수표 ══════════ */
/** 투구 j 의 표시가 나타났나(그 투구의 핀이 다 쓰러진 뒤) */
const shown = (j, i, t, over) => over || j < i || (j === i && t >= BT.fall[1] - 200);
function Sheet({ C, ex, g, i, t, over }) {
  const [x0, y0, x1, y1] = LAY[ex].sheet;
  const mini = ex === "mini";
  const fw = (x1 - x0) / 10.6, w10 = fw * 1.6, hh = y1 - y0;
  const cur = over ? -1 : g.rolls[i].f;
  const out = [];
  for (let f = 0; f < 10; f++) {
    const F = g.frames[f], fx = x0 + f * fw, w = f === 9 ? w10 : fw;
    const nb = f === 9 ? 3 : 2, bw = Math.min(fw / 2.4, 40);
    const totalShown = shown(F.done, i, t, over);
    const fresh = totalShown && !over && F.done === i ? seg(t, BT.fall[1], BT.fall[1] + 500) : 0;
    out.push(
      <g key={f}>
        <rect x={fx} y={y0} width={w} height={hh} fill={f === cur ? C.gold : C.ink} fillOpacity={f === cur ? 0.12 : 0.04} stroke={C.cardEdge} strokeWidth={1.2} />
        <text x={fx + 8} y={y0 + 20} fontFamily={SANS} fontSize={mini ? 16 : 14} fontWeight={750} fill={C.soft}>{f + 1}</text>
        {Array.from({ length: nb }, (_, j) => {
          const bx = fx + w - bw * (nb - j), ri = F.rolls[j];
          const mk = ri != null && shown(ri, i, t, over) ? g.rolls[ri].mark : "";
          return (
            <g key={j}>
              <rect x={bx} y={y0} width={bw} height={bw} fill="none" stroke={C.cardEdge} strokeWidth={1} />
              {mk && <text x={bx + bw / 2} y={y0 + bw * 0.72} textAnchor="middle" fontFamily={SANS} fontSize={mini ? 23 : 19} fontWeight={850} fill={mk === "X" || mk === "/" ? C.gold : C.ink}>{mk}</text>}
            </g>
          );
        })}
        {totalShown && <text x={fx + w / 2} y={y1 - 14} textAnchor="middle" fontFamily={SANS} fontSize={(mini ? 32 : 27) * (1 + 0.25 * (1 - fresh) * (fresh > 0 ? 1 : 0))} fontWeight={850} fill={fresh > 0 && fresh < 1 ? C.gold : C.ink}>{F.total}</text>}
      </g>,
    );
  }
  return <g>{out}</g>;
}

/* ══════════ 설명 판 ══════════ */
/** 투구 i 에서 점수가 정해진 프레임들 */
const settledAt = (g, i) => g.frames.map((F, f) => (F.done === i ? f : -1)).filter((f) => f >= 0);
function BowlPanel({ C, mode, g, i, t, k, over }) {
  const { x, y, w, h } = PANEL, x0 = x + 22, mw = w - 44;
  const o = over ? null : g.rolls[i];
  const lines = o ? bowlSteps(o, mode).map((L, j) => ({ ...L, col: L.col ? C[L.col] : undefined, at: BT.math + j * 520 })) : [];
  const calcs = o ? settledAt(g, i).map((f, j) => ({ s: `${frameCalc(g, f)} → 누계 ${g.frames[f].total}`, at: BT.fall[1] + 200 + j * 400, col: C.teal })) : [];
  const soFar = (() => { let s = 0; g.frames.forEach((F) => { if (shown(F.done, i, t, over)) s = F.total; }); return s; })();
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <FitText x={x0} y={y + 34} s={`볼링 · 가상 게임 ${k + 1} · ${g.name} · 공 놓는 보드 ${g.base}`} size={15} maxW={mw} minSize={10} weight={650} fill={C.soft} C={C} />
      <UText x={x0} y={y + 74} s={o ? `${o.f + 1}프레임 · ${o.r + 1}구` : "게임 끝"} size={26} weight={800} fill={C.ink} C={C} />
      <UText x={x + w - 22} y={y + 74} s={`${soFar}점`} size={24} weight={850} anchor="end" fill={C.gold} C={C} />
      <line x1={x0} x2={x + w - 22} y1={y + 98} y2={y + 98} stroke={C.cardEdge} strokeWidth={1.2} />
      {o && <Lines x={x0} y={y + 140} lines={lines} t={t} C={C} size={21} lh={46} maxW={mw} hiSize={23} />}
      {o && <Lines x={x0} y={y + 470} lines={calcs} t={t} C={C} size={17} lh={36} maxW={mw} />}
      <Small x={x0} y={y + h - 44} s="보드 1칸 ≈ 2.7 cm · 1 ft ≈ 30.5 cm" size={14} C={C} />
      <Small x={x0} y={y + h - 20} s="곧게 굴린 공 · 가상 게임(핀이 쓰러지는 건 흉내)" size={14} C={C} />
    </g>
  );
}
function BowlMiniCalc({ C, ex, g, i, t, over }) {
  if (over) return null;
  const fs2 = settledAt(g, i);
  if (!fs2.length) return null;
  const k = seg(t, BT.fall[1] + 200, BT.fall[1] + 700) * (1 - seg(t, BT.clear[1] - 200, BT.clear[1]));
  const s = fs2.map((f) => `${frameCalc(g, f)} → 누계 ${g.frames[f].total}`).join("   ·   ");
  return <Chip x={(LAY[ex].sheet[0] + LAY[ex].sheet[2]) / 2} y={LAY[ex].calc} s={s} size={22} C={C} color={C.teal} o={k} />;
}

/* ══════════ 액자 ══════════ */
const DEF = { ex: "full", sp: 1, seed: 1 };
const fixPrm = (p = {}) => ({ ex: fixEx(p.ex), sp: SPEEDS.includes(p.sp) ? p.sp : 1, seed: Number.isInteger(p.seed) && p.seed > 0 && p.seed < 1e6 ? p.seed : 1 });
export function BowlFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const e = lab.elapsed() * P.sp;
  const at = bowlAt(P.seed, e);
  const jump = (d) => {
    // 투구 단위로: 다음 투구 · (1.5초 넘게 봤으면) 이 투구 처음 · 아니면 앞 투구
    const base = e - at.t;
    const target = d > 0 ? base + (at.i >= at.g.rolls.length ? BT.gameEnd : BT.roll) : at.t > 1500 || base <= 0 ? base : base - BT.roll;
    lab.jump(Math.max(0, target) / P.sp); poke();
  };
  const fresh = () => { lab.setPrm({ seed: P.seed + 50 }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: fresh, toggleFs, onMode, poke }),
    ArrowRight: () => jump(1), ArrowLeft: () => jump(-1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="풀이"><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 투구 (←)" onClick={() => jump(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 투구 (→)" onClick={() => jump(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "볼링으로 보는 비례와 점수 계산", m: "볼링으로 보는 일차함수" };
  const sub = `가상 게임 · ${at.g.name} · 곧게 굴린 공 = 직선, 보너스 = 다음 투구 핀 수`;
  const prog = Math.min(1, (at.i + at.t / BT.roll) / at.g.rolls.length);
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="볼링으로 보는 일차함수와 점수 계산">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <BowlArt C={C} mode={Ly.mode} ex={P.ex} at={at} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={fresh}
        restartTitle="새 게임" isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings} prog={prog} />
    </>
  );
}
export const BowlThumb = memo(function BowlThumb({ C, mode = "m" }) {
  const g = bowlGame(2);
  const i = Math.min(5, g.rolls.length - 1);
  return <BowlArt C={C} mode={mode} ex="full" at={{ g, k: 0, i, t: BT.math + 1600 }} />;
});
