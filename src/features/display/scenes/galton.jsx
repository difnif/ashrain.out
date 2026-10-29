// 장면 — 구슬 낙하 실험(초등 · 막대그래프와 꺾은선그래프) ↔ 갈톤 보드와 정규분포(중등 · 경우의 수와 확률)
// 물리 엔진(physics.js)으로 구슬을 실제로 떨어뜨린다. 같은 설정(구슬 수·줄 수)이면 언제나 같은 결과(결정적).
//   들어가며: 못이 줄줄이 박히고, 못마다 "그 못에 닿는 길의 수"(파스칼의 삼각형)가 위의 두 수를 더하며 채워진다.
//   떨어뜨리기: 구슬이 못에 부딪히며 칸에 쌓이고, 오른쪽 그래프가 함께 자란다.
//   정리: 초등 — 가운데가 가장 많고 양 끝으로 갈수록 적다(꺾은선그래프 = 종 모양)
//         중등 — 칸으로 가는 길의 수 C(R, k), 확률 C(R, k)/2^R, 기대 개수와 실제 개수 → 정규분포 곡선
import { seg, win, E, clamp, fmt } from "../core";
import { Board, Caption, MText, Path, mathWidth } from "../draw";
import { GALTON, galtonLayout, galtonWorld, pegsOf, wallsOf, dividersOf, binOf, comb, binom, spawnSpan } from "../galton.js";
import { simAt, circlesD } from "../physics.js";

const T0 = 4600;                 // 세계 시계 0초 = 장면 4.6초 (구슬은 세계 0.5초부터)
const SETTLE = 4500, OUTRO = 9500;
const CX = 560;
const PANEL = { x0: 940, x1: 1540, yTop: 342, yBase: 566 };
const AREA = 4.15;               // 쌓인 구슬 하나가 차지하는 넓이 ≈ AREA × r² (측정값)

export function timeline(N) {
  const drop0 = T0 + 500, drop1 = T0 + (0.5 + spawnSpan(N)) * 1000, done = drop1 + SETTLE;
  return { drop0, drop1, done, dur: done + OUTRO };
}
const LCACHE = new Map();
function layoutOf(R, N) {
  const k = `${R}|${N}`;
  if (!LCACHE.has(k)) {
    const L = galtonLayout({ R, N, cx: CX });
    L.pegs = pegsOf(L); L.walls = wallsOf(L); L.divs = dividersOf(L);
    LCACHE.set(k, L);
  }
  return LCACHE.get(k);
}
const pegsD = (pegs, r, pick) => circlesD(pegs.map((p) => p.x), pegs.map((p) => p.y), pegs.map(() => r), pegs.map((_, i) => i).filter((i) => pick(pegs[i])));

/** 세계를 t 까지 돌리고, 쌓인 구슬의 그림 줄·칸별 개수를 이어 붙여 둔다 */
function worldAt(L, t) {
  const W = simAt(`galton|${L.R}|${L.N}`, () => galtonWorld(L, 11), Math.max(0, t - T0));
  if (!W._fz) W._fz = { n: 0, d: ["", "", ""], cnt: new Array(L.R + 1).fill(0), landed: 0 };
  const F = W._fz;
  for (; F.n < W.frozenList.length; F.n++) {
    const i = W.frozenList[F.n];
    F.d[W.tag[i]] += circlesD(W.x, W.y, W.r, [i]);
    const k = binOf(L, W.x[i], W.y[i]);
    if (k >= 0) { F.cnt[k]++; F.landed++; }
  }
  return W;
}

function Scene({ t, C, mode, P }) {
  const isM = mode === "m";
  const R = P.rows, N = P.n;
  const L = layoutOf(R, N);
  const TL = timeline(N);
  const W = worldAt(L, t);
  const F = W._fz;
  const cols = [C.gold, C.coral, C.teal];
  const half = (R / 2 + 0.5) * L.sx;
  const mid = Math.floor(R / 2), pMid = binom(R, mid), total = 2 ** R;
  // 들어가며
  const boardO = seg(t, 100, 900);
  const rowT = (i) => 900 + (i * 2600) / R;
  const pasO = seg(t, 1000, 1500) * (1 - seg(t, T0 - 300, T0 + 500));
  const doneO = seg(t, TL.done, TL.done + 900);
  const fallen = F.landed + 0;
  const left = Math.max(0, N - (W.nextSpawn || 0));
  // 이론 높이(쌓인 구슬): 칸 k 에 N·p_k 개 → 높이 N·p_k·AREA·r² / (sx − 3)
  const hOf = (k) => (N * binom(R, k) * AREA * L.r * L.r) / (L.sx - 3);
  return (
    <g>
      {/* 깔때기 통 — 남은 구슬만큼 차 있다 */}
      <Hopper L={L} C={C} o={boardO} fill={left / N} cols={cols} />
      {/* 벽·칸막이·바닥 */}
      <g opacity={boardO}>
        {[L.walls.left, L.walls.right].map((w, i) => <Path key={i} pts={w} stroke={C.ink} sw={4.5} o={0.85} />)}
        {L.divs.map((d, i) => <Path key={i} pts={d} stroke={C.soft} sw={2.6} o={0.9} />)}
        <Path pts={[[L.cx - half - 2, L.yFloor + 3], [L.cx + half + 2, L.yFloor + 3]]} stroke={C.ink} sw={5} />
      </g>
      {/* 못 — 이론의 길(삼각형)은 또렷하게 */}
      <path d={pegsD(L.pegs, L.rp, (p) => !p.tri)} fill={C.soft} opacity={0.38 * boardO} />
      {L.ys.map((y, i) => (
        <path key={i} d={pegsD(L.pegs, L.rp, (p) => p.tri && Math.abs(p.y - y) < 0.5)} fill={C.ink}
          opacity={0.85 * seg(t, rowT(i), rowT(i) + 350)} />
      ))}
      {/* 못마다 그 못에 닿는 길의 수(파스칼의 삼각형) */}
      {pasO > 0.01 && L.ys.map((y, i) => {
        const a = seg(t, rowT(i) + 250, rowT(i) + 650) * pasO;
        return a > 0.01 && Array.from({ length: i + 1 }, (_, j) => (
          <MText key={`${i}-${j}`} x={L.cx + (j - i / 2) * L.sx} y={y - L.rp - 5} s={String(comb(i, j))}
            size={Math.min(18, L.sx * 0.36)} weight={700} anchor="middle" fill={C.teal} halo={C.halo} opacity={a} C={C} />
        ));
      })}
      {/* 구슬: 쌓인 것 + 움직이는 것 */}
      {cols.map((c, k) => <path key={"f" + k} d={F.d[k]} fill={c} />)}
      {cols.map((c, k) => <path key={"m" + k} d={circlesD(W.x, W.y, W.r, W.live.filter((i) => W.tag[i] === k))} fill={c} />)}
      {/* 중등: 다 쌓이면 이론의 곡선 */}
      {isM && doneO > 0.01 && <Curve L={L} C={C} o={seg(t, TL.done + 1400, TL.done + 2600)} hOf={hOf} />}
      {/* 오른쪽 — 떨어진 구슬 수 · 그래프 · 판서 */}
      <Counter C={C} fallen={fallen} N={N} o={boardO} />
      <Chart L={L} C={C} t={t} TL={TL} isM={isM} cnt={F.cnt} o={boardO} />
      <Board x={PANEL.x0 + 18} y={652} t={t} C={C} size={30} lh={48} lines={isM ? [
        { t: 1600, s: "그 못에 닿는 길의 수", k: "h", u: TL.done },
        { t: 2100, s: "= 위의 두 수의 합 (파스칼의 삼각형)", u: TL.done },
        { t: TL.drop0 + 400, s: `한 구슬이 가는 길: 2를 ${R}번 곱해 ${total}가지`, row: 2, u: TL.done },
        { t: TL.done, s: `가운데 칸: 오른쪽으로 ${mid}번`, k: "h", row: 0 },
        { t: TL.done + 400, s: `확률 = {${comb(R, mid)}/${total}} ≈ ${fmt(pMid, 2)}`, row: 1 },
        { t: TL.done + 2200, s: `기대 ${Math.round(N * pMid)}개 · 실제 ‹${F.cnt[mid]}›개`, row: 2 },
      ] : [
        { t: 1600, s: "그 못까지 가는 길의 수", k: "h", u: TL.done },
        { t: 2100, s: "가운데로 갈수록 길이 많아요", u: TL.done },
        { t: TL.drop0 + 400, s: "못마다 왼쪽 또는 오른쪽", row: 2, u: TL.done },
        { t: TL.done, s: "가장 많이 모인 칸", k: "h", row: 0 },
        { t: TL.done + 400, s: `가운데 칸 ‹${F.cnt[mid]}›개`, row: 1 },
        { t: TL.done + 2200, s: "양 끝으로 갈수록 적어요", row: 2 },
      ]} />
      <Caption t={t} C={C} y={862} size={33} caps={isM ? [
        { t: 300, s: `갈톤 보드 — 못 ${R}줄, 구슬 ${N}개` },
        { t: 1500, s: "못에 닿는 길의 수는 위의 두 수를 더한 것" },
        { t: TL.drop0, s: "못마다 왼쪽·오른쪽으로 갈 가능성이 같다고 보면" },
        { t: TL.drop0 + Math.min(6000, (TL.drop1 - TL.drop0) * 0.45), s: `칸 k로 가는 길의 수 = 오른쪽으로 k번 가는 경우의 수` },
        { t: TL.done, s: `가운데 칸으로 갈 확률은 {${comb(R, mid)}/${total}} — 실제로도 가장 많이 모였어요` },
        { t: TL.done + 4800, s: "구슬과 줄이 많을수록 종 모양 곡선(정규분포)에 가까워져요" },
      ] : [
        { t: 300, s: `구슬 ${N}개를 위에서 떨어뜨려요` },
        { t: 1500, s: "가운데 못일수록 그 못까지 가는 길이 많아요" },
        { t: TL.drop0, s: "못에 부딪힐 때마다 왼쪽이나 오른쪽으로 튀어요" },
        { t: TL.drop0 + Math.min(6000, (TL.drop1 - TL.drop0) * 0.45), s: "어느 칸에 가장 많이 모일까요?" },
        { t: TL.done, s: "가운데에 가장 많이, 양 끝으로 갈수록 적게 모였어요" },
        { t: TL.done + 4800, s: "꺾은선그래프로 이으면 종 모양이 돼요" },
      ]} />
    </g>
  );
}

/** 깔때기 통: 위가 넓은 사다리꼴, 남은 구슬만큼 무늬로 채운다 */
function Hopper({ L, C, o, fill, cols }) {
  const top = L.walls.left[0][1], w1 = 120, w0 = L.sx * 0.55, y0 = top - 46;
  const shape = [[L.cx - w1, y0], [L.cx + w1, y0], [L.cx + w0, top], [L.cx - w0, top]];
  const lvl = top - 46 * clamp(fill);
  const pid = `hop-${C.name}`;
  return (
    <g opacity={o}>
      <defs>
        <pattern id={pid} width={14} height={12} patternUnits="userSpaceOnUse">
          <circle cx={4} cy={4} r={3.6} fill={cols[0]} /><circle cx={11} cy={10} r={3.6} fill={cols[1]} />
          <circle cx={11} cy={2} r={2.2} fill={cols[2]} />
        </pattern>
        <clipPath id={pid + "-c"}><path d={`M${shape.map((p) => p.join(" ")).join("L")}Z`} /></clipPath>
      </defs>
      {fill > 0.001 && <rect x={L.cx - w1} y={lvl} width={2 * w1} height={top - lvl} fill={`url(#${pid})`} clipPath={`url(#${pid}-c)`} opacity={0.9} />}
      <Path pts={shape} closed stroke={C.ink} sw={3.5} fill={C.ink} fo={0.06} o={0.85} />
    </g>
  );
}

function Counter({ C, fallen, N, o }) {
  return (
    <g opacity={o}>
      <MText x={PANEL.x0 + 18} y={196} s="떨어진 구슬" size={26} weight={700} fill={C.soft} C={C} />
      <MText x={PANEL.x0 + 18} y={268} s={`‹${fallen}›`} size={64} weight={800} C={C} />
      <MText x={PANEL.x0 + 18 + mathWidth(String(fallen), 64, 800) + 14} y={268} s={`/ ${N}개`} size={32} weight={600} fill={C.soft} C={C} />
    </g>
  );
}

/** 오른쪽 그래프 — 칸별 개수 막대(+ 중등: 기대 개수 테두리·정규분포 곡선, 초등: 꺾은선) */
function Chart({ L, C, t, TL, isM, cnt, o }) {
  const { R, N } = L, { x0, x1, yTop, yBase } = PANEL;
  const slot = (x1 - x0) / (R + 1), bw = slot * 0.62;
  const xc = (k) => x0 + slot * (k + 0.5);
  const expMax = N * binom(R, Math.floor(R / 2));
  const yMax = Math.max(expMax, ...cnt) * 1.12 || 1;
  const hh = (v) => (v / yMax) * (yBase - yTop);
  const thO = isM ? seg(t, 2600, 3400) : 0;
  const pasO = seg(t, 2900, 3700);
  const doneO = seg(t, TL.done + 1200, TL.done + 2400);
  const sig = Math.sqrt(R) / 2, mu = R / 2;
  const curve = [];
  for (let i = 0; i <= 120; i++) {
    const k = -0.5 + ((R + 1) * i) / 120;
    const f = (N / (sig * Math.sqrt(2 * Math.PI))) * Math.exp(-((k - mu) ** 2) / (2 * sig * sig));
    curve.push([x0 + slot * (k + 0.5), yBase - hh(f)]);
  }
  const fs = Math.min(18, slot * 0.42);
  return (
    <g opacity={o}>
      <Path pts={[[x0 - 6, yBase], [x1 + 6, yBase]]} stroke={C.ink} sw={2.6} />
      {cnt.map((v, k) => {
        const h = hh(v);
        return h > 0.3 && <rect key={k} x={xc(k) - bw / 2} y={yBase - h} width={bw} height={h} rx={3}
          fill={k === Math.floor(R / 2) && doneO > 0 ? C.gold : C.sky} fillOpacity={0.78} />;
      })}
      {/* 중등: 이론의 기대 개수(점선 테두리) */}
      {thO > 0.01 && cnt.map((_, k) => {
        const h = hh(N * binom(R, k));
        return <rect key={"e" + k} x={xc(k) - bw / 2 - 2} y={yBase - h} width={bw + 4} height={h} fill="none"
          stroke={C.gold} strokeWidth={2} strokeDasharray="6 5" opacity={0.9 * thO} />;
      })}
      {/* 칸으로 가는 길의 수 */}
      {cnt.map((_, k) => (
        <MText key={"p" + k} x={xc(k)} y={yTop - 14} s={String(comb(R, k))} size={fs} weight={700} anchor="middle"
          fill={C.teal} opacity={pasO} C={C} />
      ))}
      <MText x={x0 - 4} y={yTop - 40} s={isM ? "칸으로 가는 길의 수(경우의 수)" : "칸까지 가는 길의 수"} size={20} weight={700}
        fill={C.teal} opacity={pasO} C={C} />
      {/* 칸 번호 */}
      {cnt.map((_, k) => (
        <MText key={"k" + k} x={xc(k)} y={yBase + 26} s={String(isM ? k : k + 1)} size={Math.min(19, slot * 0.44)} weight={600}
          anchor="middle" fill={C.soft} C={C} />
      ))}
      <MText x={x1 + 4} y={yBase + 52} s={isM ? "오른쪽으로 간 횟수" : "칸"} size={18} weight={600} anchor="end" fill={C.soft} C={C} />
      {/* 정리: 초등 꺾은선 · 중등 종 모양 곡선 */}
      {!isM && doneO > 0.01 && <g opacity={doneO}>
        <Path pts={cnt.map((v, k) => [xc(k), yBase - hh(v)])} stroke={C.coral} sw={3.5} />
        {cnt.map((v, k) => <circle key={k} cx={xc(k)} cy={yBase - hh(v)} r={5} fill={C.coral} />)}
      </g>}
      {isM && doneO > 0.01 && <Path pts={curve} stroke={C.coral} sw={3.5} o={doneO} />}
    </g>
  );
}

/** 쌓인 구슬 위의 이론 곡선(중등) */
function Curve({ L, C, o, hOf }) {
  const { R, sx } = L, sig = Math.sqrt(R) / 2, mu = R / 2;
  const pts = [];
  for (let i = 0; i <= 160; i++) {
    const k = -0.5 + ((R + 1) * i) / 160;
    const f = Math.exp(-((k - mu) ** 2) / (2 * sig * sig)) / (sig * Math.sqrt(2 * Math.PI));
    const h = (hOf(mu) / binom(R, mu)) * f;
    pts.push([L.bins[0].x0 + sx * (k + 0.5), L.yFloor - h]);
  }
  return <Path pts={pts} stroke={C.coral} sw={4} o={o * 0.95} dash="12 8" />;
}

export default {
  key: "galton",
  dur: (P) => timeline(P.n).dur,
  controls: [
    { key: "n", label: "구슬", kind: "step", options: GALTON.NS, def: GALTON.NDEF, unit: "개" },
    { key: "rows", label: "못", kind: "step", options: GALTON.ROWS, def: GALTON.RDEF, unit: "줄" },
  ],
  title: { e: "구슬 낙하 실험", m: "갈톤 보드와 정규분포" },
  sub: { e: "초등 · 막대그래프와 꺾은선그래프", m: "중2 · 경우의 수와 확률" },
  render: (mode, t, C, P) => <Scene t={t} C={C} mode={mode} P={P || { n: GALTON.NDEF, rows: GALTON.RDEF }} />,
};
