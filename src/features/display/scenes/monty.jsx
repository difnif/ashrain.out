// 장면 — 바꿀까, 그대로 둘까?(초등 · 가능성) ↔ 몬티홀 문제 — 문이 늘어나면(중2 · 확률)
// 문 n개(설정: 3~5) 가운데 하나 뒤에 자동차. 처음엔 늘 1번 문을 고르고, 답을 아는 사회자가 염소 문을 연다.
//   문 아래 막대 = 그 문 뒤에 자동차가 있을 확률. 사회자가 연 문의 몫은 "내가 고르지 않은 닫힌 문"으로만 옮겨 간다.
//   그대로 {1/n} · 하나 열고 바꾸기 (n−1)/(n(n−2)) · (n ≥ 4) 하나만 남기고 다 연 뒤 바꾸기 (n−1)/n
//   300판(결정적 난수)을 그대로/바꾸기로 해 본 기록이 점으로 찬다. 마지막엔 문 3·4·5개를 한 표로.
import { beats, seg, win, E, lerp, clamp } from "../core";
import { Board, Caption, MText, Path, Table } from "../draw";
import { MONTY, fracS, pctS } from "../guess.js";

const DOOR = { y0: 262, h: 226, gap: 24, cx: 488 };
const BAR = { base: 762, h: 220 };
const GRID = { cols: 20, rows: 15, sp: 12, x: [992, 1290], y: 330 };

const TLS = new Map();
function timeline(n) {
  if (!TLS.has(n)) TLS.set(n, beats([
    ["intro", 3200], ["pick", 3600], ["open", 4200], ["flow", 7600], ["sim", 10500],
    ["part2", n >= 4 ? 9200 : 0], ["sum", 8200], ["hold", 1800],
  ]));
  return TLS.get(n);
}
const doorW = (n) => Math.min(150, (830 - (n - 1) * DOOR.gap) / n);
const doorX = (n, i) => DOOR.cx + (i - (n - 1) / 2) * (doorW(n) + DOOR.gap);

/** 지금 문 i 가 열린 정도(0~1) */
function openOf(n, i, t, B) {
  if (i === n - 1) return seg(t, B.a.open + 900, B.a.open + 2100, E.out);
  if (n >= 4 && i >= 2 && i <= n - 2) { const a = B.a.part2 + 1400 + (i - 2) * 900; return seg(t, a, a + 900, E.out); }
  return 0;
}
/** 문 i 뒤에 자동차가 있을 확률(지금 보여 줄 값) */
function probOf(n, i, t, B) {
  const P = MONTY.probs(n), v = (p) => p[0] / p[1];
  const k1 = seg(t, B.a.flow + 600, B.a.flow + 2600, E.io);              // 하나 연 뒤 몫이 옮겨 감
  const k2 = n >= 4 ? seg(t, B.a.part2 + 1400 + (n - 3) * 900, B.a.part2 + 1400 + (n - 3) * 900 + 2000, E.io) : 0;
  const base = 1 / n;
  const after1 = i === 0 ? base : i === n - 1 ? 0 : v(P.sw1);
  const after2 = i === 0 ? base : i === 1 ? v(P.swAll) : 0;
  return lerp(lerp(base, after1, k1), after2, k2);
}

function Scene({ t, C, mode, P }) {
  const isM = mode === "m";
  const n = P.n, B = timeline(n), PR = MONTY.probs(n), G = MONTY.GAMES;
  const dw = doorW(n);
  const doorsO = seg(t, 200, 1200);
  const pickO = seg(t, B.a.pick + 300, B.a.pick + 900);
  const barsO = seg(t, B.a.pick + 1400, B.a.pick + 2200) * (1 - 0.0 * seg(t, B.a.sum, B.a.sum + 500));
  const k = Math.round(G * seg(t, B.a.sim + 800, B.b.sim - 900, E.sine));
  const simO = win(t, B.a.sim + 200, B.a.sum + 200, 500, 500);
  const sumO = seg(t, B.a.sum + 300, B.a.sum + 900);
  const wStay = MONTY.wins(n, k, "stay"), wSw = MONTY.wins(n, k, "sw1"), wAll = MONTY.wins(n, G, "swAll");
  const nf = (a, b) => `{${a}/${b}}`;
  return (
    <g>
      {/* 문 */}
      {Array.from({ length: n }, (_, i) => (
        <Door key={i} C={C} x={doorX(n, i)} w={dw} i={i} open={openOf(n, i, t, B)} o={doorsO} car={i === 1}
          picked={i === 0 ? pickO : 0} isM={isM} />
      ))}
      {/* 문 아래: 자동차가 있을 확률 막대 */}
      {barsO > 0.01 && Array.from({ length: n }, (_, i) => {
        const v = probOf(n, i, t, B), x = doorX(n, i), h = v * BAR.h, bw = Math.min(64, dw * 0.46);
        const lab = labelOf(n, i, t, B);
        return (
          <g key={"b" + i} opacity={barsO}>
            <line x1={x - dw / 2} x2={x + dw / 2} y1={BAR.base} y2={BAR.base} stroke={C.ink} strokeWidth={2.4} opacity={0.8} />
            {h > 0.5 && <rect x={x - bw / 2} y={BAR.base - h} width={bw} height={h} rx={4} fill={i === 0 ? C.sky : C.gold} fillOpacity={0.85} />}
            {lab && <MText x={x} y={BAR.base - h - 12} s={lab} size={28} weight={800} anchor="middle" fill={i === 0 ? C.sky : C.gold} halo={C.halo} C={C} />}
          </g>
        );
      })}
      <MText x={70} y={BAR.base - BAR.h - 14} s={isM ? "자동차가 있을 확률" : "자동차가 있을 가능성"} size={22} weight={700} fill={C.soft}
        opacity={barsO} C={C} />
      {/* 오른쪽: 300판 해 보기 */}
      {simO > 0.01 && <Sim C={C} t={t} B={B} n={n} k={k} wStay={wStay} wSw={wSw} o={simO} isM={isM} PR={PR} />}
      {/* 정리 표: 문 3 · 4 · 5개 */}
      {sumO > 0.01 && <SumTable C={C} t={t} B={B} n={n} o={sumO} isM={isM} />}
      {/* 판서: 해 보기 전(오른쪽 위) · 해 본 뒤(점 그림 아래) */}
      <Board x={1000} y={300} t={t} C={C} size={30} lh={54} lines={isM ? [
        { t: B.a.pick + 600, s: `처음 고른 1번 문: ‹${fracS(PR.stay)}›`, u: B.a.sim + 200 },
        { t: B.a.open + 400, s: "사회자는 자동차를 피해 염소 문만 연다", u: B.a.sim + 200 },
        { t: B.a.flow + 300, s: `→ 내 문은 그대로 ${fracS(PR.stay)}`, u: B.a.sim + 200 },
        { t: B.a.flow + 1600, s: `나머지 ${nf(n - 1, n)}은 닫힌 다른 문으로`, u: B.a.sim + 200 },
        ...(n >= 4 ? [{ t: B.a.flow + 3200, s: `${n - 2}개가 나눠 각 ‹${fracS(PR.sw1)}›`, u: B.a.sim + 200 }] : []),
      ] : [
        { t: B.a.pick + 600, s: `1번 문에 자동차: ‹${n}번 중 1번›꼴`, u: B.a.sim + 200 },
        { t: B.a.open + 400, s: "사회자는 염소 문만 열어요", u: B.a.sim + 200 },
        { t: B.a.flow + 300, s: "→ 내 문의 가능성은 그대로", u: B.a.sim + 200 },
        { t: B.a.flow + 1600, s: "열린 문의 몫은 닫힌 다른 문으로", u: B.a.sim + 200 },
      ]} />
      <Board x={1000} y={672} t={t} C={C} size={29} lh={50} lines={isM ? [
        { t: B.a.sim + 5600, s: `바꾸기 = ${nf(n - 1, n)} × ${nf(1, n - 2)} = ‹${fracS(PR.sw1)}›`, row: 0, u: n >= 4 ? B.a.part2 + 200 : B.a.sum + 200 },
        ...(n >= 4 ? [
          { t: B.a.part2 + 300, s: "사회자가 하나만 남기고 다 열면", k: "h", row: 0, u: B.a.sum + 200 },
          { t: B.a.part2 + 4200, s: `바꾸기 = ‹${fracS(PR.swAll)}›`, row: 1, u: B.a.sum + 200 },
          { t: B.a.part2 + 5600, s: `${G}판 중 바꿔서 이긴 판 ‹${wAll}›`, row: 2, size: 27, u: B.a.sum + 200 },
        ] : []),
      ] : [
        { t: B.a.sim + 5600, s: `바꾼 쪽이 ‹${wSw - wStay}›판 더 이겼어요`, row: 0, u: n >= 4 ? B.a.part2 + 200 : B.a.sum + 200 },
        ...(n >= 4 ? [
          { t: B.a.part2 + 300, s: "하나만 남기고 다 열면", k: "h", row: 0, u: B.a.sum + 200 },
          { t: B.a.part2 + 4200, s: `남은 문: ‹${n}번 중 ${n - 1}번›꼴`, row: 1, u: B.a.sum + 200 },
          { t: B.a.part2 + 5600, s: `${G}번 중 바꿔서 이긴 판 ‹${wAll}›`, row: 2, size: 27, u: B.a.sum + 200 },
        ] : []),
      ]} />
      <Caption t={t} C={C} y={862} size={32} caps={isM ? [
        { t: 300, s: `문 ${n}개 가운데 하나 뒤에 자동차, 나머지 뒤에는 염소` },
        { t: B.a.pick + 300, s: "1번 문을 골랐어요 — 자동차일 확률은?" },
        { t: B.a.open + 300, s: "답을 아는 사회자가 염소가 있는 문을 하나 열어요" },
        { t: B.a.flow + 300, s: "바꿀까요, 그대로 둘까요? — 열린 문의 확률은 어디로 갈까요?" },
        { t: B.a.flow + 3600, s: "사회자는 내 문을 열 수 없으니, 내 문의 확률은 처음 그대로" },
        { t: B.a.sim + 300, s: `같은 게임을 ${G}판 — 그대로 둘 때와 바꿀 때` },
        { t: B.a.sim + 5600, s: `바꾸면 ${fracS(PR.sw1)}, 그대로면 ${fracS(PR.stay)} — 바꾸는 쪽이 ${ratioWord(PR.sw1, PR.stay)}` },
        ...(n >= 4 ? [
          { t: B.a.part2 + 300, s: "이번엔 사회자가 문을 하나만 남기고 모두 연다면?" },
          { t: B.a.part2 + 4200, s: `남은 한 문에 ${nf(n - 1, n)}이 모여요 — 바꾸면 ${fracS(PR.swAll)}` },
        ] : []),
        { t: B.a.sum + 300, s: "문이 늘어도 바꾸는 쪽이 늘 유리해요" },
      ] : [
        { t: 300, s: `문 ${n}개 가운데 하나 뒤에만 자동차가 있어요` },
        { t: B.a.pick + 300, s: "1번 문을 골랐어요" },
        { t: B.a.open + 300, s: "자동차가 어디 있는지 아는 사회자가 염소 문을 열어요" },
        { t: B.a.flow + 300, s: "바꿀까요, 그대로 둘까요?" },
        { t: B.a.flow + 3600, s: "내 문의 가능성은 처음과 같아요" },
        { t: B.a.sim + 300, s: `${G}번 해 보면 — 그대로 둘 때와 바꿀 때` },
        { t: B.a.sim + 5600, s: "바꾼 쪽이 더 많이 이겼어요" },
        ...(n >= 4 ? [
          { t: B.a.part2 + 300, s: "사회자가 문을 하나만 남기고 모두 연다면?" },
          { t: B.a.part2 + 4200, s: "남은 한 문으로 바꾸면 거의 이겨요" },
        ] : []),
        { t: B.a.sum + 300, s: "문이 늘어도 바꾸는 쪽이 더 유리해요" },
      ]} />
    </g>
  );
}
/** 몇 배인지 말로: 2/3 ÷ 1/3 = 2배 */
function ratioWord(a, b) {
  const r = (a[0] * b[1]) / (a[1] * b[0]);
  const s = Number.isInteger(r) ? `${r}배` : `${Math.round(r * 100) / 100}배`;
  return `${s} 유리해요`;
}
/** 막대 위 글자 — 몫이 다 옮겨 간 뒤에만 분수로 */
function labelOf(n, i, t, B) {
  const P = MONTY.probs(n);
  const k1 = seg(t, B.a.flow + 600, B.a.flow + 2600), k2 = n >= 4 ? seg(t, B.a.part2 + 1400 + (n - 3) * 900, B.a.part2 + 1400 + (n - 3) * 900 + 2000) : 0;
  if (k2 >= 1) return i === 0 ? fracS(P.stay) : i === 1 ? fracS(P.swAll) : "0";
  if (k2 > 0) return i === 0 ? fracS(P.stay) : null;
  if (k1 >= 1) return i === 0 ? fracS(P.stay) : i === n - 1 ? "0" : fracS(P.sw1);
  if (k1 > 0) return i === 0 ? fracS(P.stay) : null;
  return fracS(P.stay);
}

/** 문 하나: 문틀 · 문짝(열리면 왼쪽 경첩으로 접힌다) · 문 뒤(염소 또는 자동차) · 번호 · 내 선택 표시 */
function Door({ C, x, w, i, open, o, car, picked, isM }) {
  const y0 = DOOR.y0, h = DOOR.h, x0 = x - w / 2;
  const pw = w * (1 - 0.86 * open);                          // 문짝 너비(열릴수록 좁게)
  const skew = 14 * open;
  return (
    <g opacity={o}>
      <rect x={x0} y={y0} width={w} height={h} rx={4} fill={C.ink} fillOpacity={0.08} />
      {open > 0.02 && (car ? <Car C={C} cx={x} cy={y0 + h * 0.62} s={w * 0.78} /> : <Goat C={C} cx={x} cy={y0 + h * 0.58} s={w * 0.62} />)}
      <path d={`M${x0} ${y0} L${x0 + pw} ${y0 + skew} L${x0 + pw} ${y0 + h - skew} L${x0} ${y0 + h} Z`} fill={C.wood} fillOpacity={0.9}
        stroke={C.woodEdge} strokeWidth={3} strokeLinejoin="round" />
      {open < 0.6 && <g opacity={1 - open / 0.6}>
        <circle cx={x0 + pw / 2} cy={y0 + h * 0.36} r={Math.min(30, w * 0.22)} fill={C.paper} stroke={C.woodEdge} strokeWidth={3} />
        <text x={x0 + pw / 2} y={y0 + h * 0.36 + 11} fontSize={Math.min(32, w * 0.24)} fontWeight={800} textAnchor="middle" fill={C.ink}>{i + 1}</text>
        <circle cx={x0 + pw - 16} cy={y0 + h * 0.58} r={5} fill={C.woodEdge} />
      </g>}
      <rect x={x0} y={y0} width={w} height={h} rx={4} fill="none" stroke={C.ink} strokeWidth={3.5} opacity={0.8} />
      {picked > 0.01 && <g opacity={picked}>
        <rect x={x0 - 7} y={y0 - 7} width={w + 14} height={h + 14} rx={8} fill="none" stroke={C.sky} strokeWidth={5} />
        <MText x={x} y={y0 - 20} s={isM ? "내 선택" : "내가 고른 문"} size={24} weight={800} anchor="middle" fill={C.sky} C={C} />
      </g>}
    </g>
  );
}
export function Car({ C, cx, cy, s }) {
  const b = s / 2;
  return (
    <g>
      <path d={`M${cx - b} ${cy + 0.18 * s} L${cx - b} ${cy - 0.02 * s} Q${cx - b} ${cy - 0.1 * s} ${cx - b + 0.08 * s} ${cy - 0.1 * s}
        L${cx - 0.26 * s} ${cy - 0.1 * s} L${cx - 0.15 * s} ${cy - 0.3 * s} L${cx + 0.17 * s} ${cy - 0.3 * s} L${cx + 0.3 * s} ${cy - 0.1 * s}
        L${cx + b - 0.06 * s} ${cy - 0.08 * s} Q${cx + b} ${cy - 0.06 * s} ${cx + b} ${cy + 0.02 * s} L${cx + b} ${cy + 0.18 * s} Z`}
        fill={C.coral} stroke={C.ink} strokeWidth={2.5} strokeLinejoin="round" />
      <path d={`M${cx - 0.22 * s} ${cy - 0.11 * s} L${cx - 0.13 * s} ${cy - 0.26 * s} L${cx - 0.01 * s} ${cy - 0.26 * s} L${cx - 0.01 * s} ${cy - 0.11 * s} Z`} fill={C.paper} opacity={0.85} />
      <path d={`M${cx + 0.03 * s} ${cy - 0.11 * s} L${cx + 0.03 * s} ${cy - 0.26 * s} L${cx + 0.15 * s} ${cy - 0.26 * s} L${cx + 0.25 * s} ${cy - 0.11 * s} Z`} fill={C.paper} opacity={0.85} />
      {[-0.28, 0.28].map((d) => <circle key={d} cx={cx + d * s} cy={cy + 0.19 * s} r={0.1 * s} fill={C.ink} stroke={C.paper} strokeWidth={3} />)}
    </g>
  );
}
export function Goat({ C, cx, cy, s }) {
  return (
    <g>
      {/* 뿔 */}
      <path d={`M${cx - 0.1 * s} ${cy - 0.3 * s} Q${cx - 0.34 * s} ${cy - 0.62 * s} ${cx - 0.42 * s} ${cy - 0.36 * s}`} fill="none" stroke={C.soft} strokeWidth={0.06 * s} strokeLinecap="round" />
      <path d={`M${cx + 0.1 * s} ${cy - 0.3 * s} Q${cx + 0.34 * s} ${cy - 0.62 * s} ${cx + 0.42 * s} ${cy - 0.36 * s}`} fill="none" stroke={C.soft} strokeWidth={0.06 * s} strokeLinecap="round" />
      {/* 귀 */}
      <ellipse cx={cx - 0.32 * s} cy={cy - 0.14 * s} rx={0.18 * s} ry={0.07 * s} transform={`rotate(20 ${cx - 0.32 * s} ${cy - 0.14 * s})`} fill={C.ink} opacity={0.75} />
      <ellipse cx={cx + 0.32 * s} cy={cy - 0.14 * s} rx={0.18 * s} ry={0.07 * s} transform={`rotate(-20 ${cx + 0.32 * s} ${cy - 0.14 * s})`} fill={C.ink} opacity={0.75} />
      {/* 얼굴 · 수염 */}
      <path d={`M${cx - 0.2 * s} ${cy - 0.28 * s} Q${cx} ${cy - 0.4 * s} ${cx + 0.2 * s} ${cy - 0.28 * s} L${cx + 0.13 * s} ${cy + 0.2 * s} Q${cx} ${cy + 0.3 * s} ${cx - 0.13 * s} ${cy + 0.2 * s} Z`}
        fill={C.ink} opacity={0.9} />
      <path d={`M${cx - 0.06 * s} ${cy + 0.25 * s} L${cx} ${cy + 0.42 * s} L${cx + 0.06 * s} ${cy + 0.25 * s} Z`} fill={C.ink} opacity={0.9} />
      <circle cx={cx - 0.09 * s} cy={cy - 0.12 * s} r={0.035 * s} fill={C.paper} />
      <circle cx={cx + 0.09 * s} cy={cy - 0.12 * s} r={0.035 * s} fill={C.paper} />
    </g>
  );
}

/** 오른쪽: 같은 300판을 그대로 / 바꾸기로 — 이긴 판은 금빛 점 */
function Sim({ C, t, B, n, k, wStay, wSw, o, isM, PR }) {
  const Gm = MONTY.games(n);
  // (문 4개 이상) 둘째 장면: 오른쪽 점 그림을 "하나만 남기고 바꾸기"로 다시 채운다
  const p2 = n >= 4 && t >= B.a.part2 + 4200;
  const k2 = p2 ? Math.round(MONTY.GAMES * seg(t, B.a.part2 + 4400, B.a.part2 + 7600, E.sine)) : 0;
  const grids = [
    { key: "stay", name: "그대로", w: wStay, p: PR.stay, col: C.sky, k },
    p2 ? { key: "swAll", name: "하나만 남기고 바꾸기", w: MONTY.wins(n, k2, "swAll"), p: PR.swAll, col: C.coral, k: k2 }
      : { key: "sw1", name: "바꾸기", w: wSw, p: PR.sw1, col: C.gold, k },
  ];
  return (
    <g opacity={o}>
      <MText x={GRID.x[0]} y={244} s={`${isM ? "" : ""}‹${k}›판 해 보면`} size={30} weight={800} C={C} />
      {grids.map((g, gi) => {
        const X = GRID.x[gi];
        const dots = [];
        for (let i = 0; i < g.k; i++) {
          const win1 = Gm[i][g.key];
          const cx = X + (i % GRID.cols) * GRID.sp + 5, cy = GRID.y + Math.floor(i / GRID.cols) * GRID.sp + 5;
          dots.push(<circle key={i} cx={cx} cy={cy} r={4.4} fill={win1 ? g.col : C.soft} opacity={win1 ? 1 : 0.28} />);
        }
        return (
          <g key={g.key}>
            <MText x={X} y={308} s={g.name} size={g.name.length > 6 ? 21 : 26} weight={800} fill={g.col} C={C} />
            {dots}
            <MText x={X} y={GRID.y + GRID.rows * GRID.sp + 40} s={`이긴 판 ‹${g.w}›`} size={26} weight={700} C={C} />
            <MText x={X} y={GRID.y + GRID.rows * GRID.sp + 76} s={isM ? `이론 ${fracS(g.p)} ≈ ${pctS(g.p[0] / g.p[1])}` : `${pctS(g.k ? g.w / g.k : 0)}`} size={22} weight={600}
              fill={C.soft} opacity={seg(t, B.a.sim + 4000, B.a.sim + 4600)} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 정리: 문 3 · 4 · 5개 — 그대로 · 하나 열고 바꾸기 · 하나만 남기고 바꾸기 */
function SumTable({ C, t, B, n, o, isM }) {
  const a = B.a.sum;
  const rows = [
    [{ s: "문", color: "soft" }, { s: "그대로", color: "soft" }, { s: "하나 열고 바꾸기", color: "soft", size: 20 }, { s: "하나만 남기고 바꾸기", color: "soft", size: 20 }],
    ...MONTY.NS.map((m, r) => {
      const P = MONTY.probs(m), tt = a + 700 + r * 500, hi = m === n ? a + 2400 : null;
      return [
        { s: `${m}개`, t: tt, weight: 800, hi, hiCol: "sky" },
        { s: fracS(P.stay), t: tt },
        { s: `‹${fracS(P.sw1)}›`, t: tt },
        { s: `‹${fracS(P.swAll)}›`, t: tt },
      ];
    }),
  ];
  return <Table x={985} y={250} cols={[70, 100, 185, 212]} rh={[50, 70, 70, 70]} rows={rows} C={C} t={t} size={28} o={o} />;
}

export default {
  key: "monty",
  dur: (P) => timeline(P.n).dur,
  controls: [{ key: "n", label: "문", kind: "step", options: MONTY.NS, def: MONTY.NDEF, unit: "개" }],
  title: { e: "바꿀까, 그대로 둘까?", m: "몬티홀 문제 — 문이 늘어나면" },
  sub: { e: "초등 · 일이 일어날 가능성", m: "중2 · 확률의 뜻과 계산" },
  render: (mode, t, C, P) => <Scene t={t} C={C} mode={mode} P={P || { n: MONTY.NDEF }} />,
};
