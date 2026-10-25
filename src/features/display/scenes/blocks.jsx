// 장면 1 — 쌓기나무의 개수(초등) ↔ 최단 경로의 수(중등)
// 같은 4×3 바닥 위: 초등은 나무를 쌓아 세고, 중등은 그 바닥의 길을 걷는다. 둘 다 위에서 내려다본 뒤
// 칸(초등)·교차점(중등)에 수를 써서 더한다 — 「바둑판에 수 쓰기」가 겹치는 지점.
import { beats, seg, E, camera, lerp, clamp } from "../core";
import { Board, Caption, Path, Lbl, MText, Arrow } from "../draw";
import { shade, lambert, facing } from "../core";
import { BLOCKS } from "../facts";

const { COLS, ROWS, HT, LAYERS, ROW_SUM, TOTAL, PASCAL, PATHS } = BLOCKS;

const B = beats([["intro", 2200], ["build", 11000], ["tally", 3600], ["tilt", 3000], ["nums", 9000], ["total", 3800], ["hold", 3400]]);

// 떨어지는 순서: 층마다, 뒷줄부터 — 뒤에 놓일 나무가 앞 나무에 가려지지 않게
const DROPS = [];
{
  let tt = B.a.build + 250;
  for (let k = 0; k < 3; k++) {
    for (let y = ROWS - 1; y >= 0; y--) for (let x = 0; x < COLS; x++) if (HT[y][x] > k) { DROPS.push({ x, y, k, t: tt }); tt += 520; }
    tt += 620;
  }
}
const LAYER_DONE = [0, 1, 2].map((k) => Math.max(...DROPS.filter((d) => d.k === k).map((d) => d.t)) + 700);

function cam(t) {
  const sway = -33 + 7 * Math.sin((t / 21000) * Math.PI * 2);
  const k = seg(t, B.a.tilt, B.b.tilt, E.io);
  const sway0 = -33 + 7 * Math.sin((B.a.tilt / 21000) * Math.PI * 2);
  const yaw = t < B.a.tilt ? sway : lerp(sway0, 0, k);
  return camera({
    yaw, pitch: lerp(31, 90, k), scale: lerp(122, 148, k),
    cx: lerp(560, 520, k), cy: lerp(520, 468, k), target: [2, 1.5, lerp(0.9, 0, k)],
  });
}

/* ── 바닥 격자 ── */
function Floor({ c, C, o = 1, strong }) {
  const lines = [];
  for (let x = 0; x <= COLS; x++) lines.push([[x, 0, 0], [x, ROWS, 0]]);
  for (let y = 0; y <= ROWS; y++) lines.push([[0, y, 0], [COLS, y, 0]]);
  return (
    <g opacity={o}>
      <Path pts={[[0, 0, 0], [COLS, 0, 0], [COLS, ROWS, 0], [0, ROWS, 0]].map((q) => c.p(q))} closed
        fill={C.ink} fo={0.05} stroke="none" />
      {lines.map((L, i) => <Path key={i} pts={L.map((q) => c.p(q))} stroke={strong ? C.soft : C.faint} sw={strong ? 3 : 2.4} />)}
    </g>
  );
}

/* ── 정육면체 한 개 (보이는 면만) ── */
const CUBE_F = [
  { n: [0, 0, 1], q: [[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]], nb: [0, 0, 1] },
  { n: [0, 0, -1], q: [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]], nb: [0, 0, -1] },
  { n: [0, -1, 0], q: [[0, 0, 0], [1, 0, 0], [1, 0, 1], [0, 0, 1]], nb: [0, -1, 0] },
  { n: [0, 1, 0], q: [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]], nb: [0, 1, 0] },
  { n: [-1, 0, 0], q: [[0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 0]], nb: [-1, 0, 0] },
  { n: [1, 0, 0], q: [[1, 0, 0], [1, 1, 0], [1, 1, 1], [1, 0, 1]], nb: [1, 0, 0] },
];
function Cube({ c, C, at, has, o = 1, color, edge, sw = 2.6 }) {
  const out = [];
  for (const f of CUBE_F) {
    if (!facing(c, f.n)) continue;
    if (has && has(f.nb)) continue;
    const P = f.q.map((q) => c.p([at[0] + q[0], at[1] + q[1], at[2] + q[2]]));
    out.push(<path key={f.n.join()} d={"M" + P.map((p) => p[0].toFixed(1) + " " + p[1].toFixed(1)).join("L") + "Z"}
      fill={shade(color, lambert(c, f.n))} stroke={edge} strokeWidth={sw} strokeLinejoin="round" />);
  }
  return <g opacity={o}>{out}</g>;
}

/* ══════════ 초등: 쌓기나무 ══════════ */
function Elem({ t, C }) {
  const c = cam(t);
  const landed = new Set();
  const live = [];
  for (const d of DROPS) {
    const p = seg(t, d.t, d.t + 650, E.drop);
    if (t < d.t) continue;
    if (p >= 1) landed.add(`${d.x},${d.y},${d.k}`);
    live.push({ ...d, z: d.k + (1 - p) * 3.4, o: seg(t, d.t, d.t + 160, E.lin) });
  }
  const occ = (x, y, z) => landed.has(`${x},${y},${z}`);
  const center = (b) => c.p([b.x + 0.5, b.y + 0.5, b.z + 0.5])[2];
  live.sort((a, b) => center(b) - center(a));
  const top = seg(t, B.a.tilt + 1800, B.b.tilt, E.sine);
  // 위에서 본 모양의 수
  const nums = [];
  let nt = B.a.nums + 300;
  for (let y = ROWS - 1; y >= 0; y--) for (let x = 0; x < COLS; x++) if (HT[y][x] > 0) { nums.push({ x, y, v: HT[y][x], t: nt }); nt += 560; }
  const sumT = [0, 1, 2].map((i) => nt + 300 + i * 600);
  return (
    <g>
      <Floor c={c} C={C} o={seg(t, 200, 1600, E.sine)} />
      {live.map((b) => {
        const done = b.z === b.k;
        return <Cube key={`${b.x}${b.y}${b.k}`} c={c} C={C} at={[b.x, b.y, b.z]} o={b.o} color={C.wood} edge={C.woodEdge}
          has={done ? (n) => occ(b.x + n[0], b.y + n[1], b.k + n[2]) : null} />;
      })}
      {top > 0 && nums.map((n) => {
        const a = seg(t, n.t, n.t + 380, E.back);
        if (a <= 0) return null;
        const q = c.p([n.x + 0.5, n.y + 0.5, HT[n.y][n.x]]);
        return <g key={`${n.x}${n.y}`} transform={`translate(${q[0]} ${q[1]}) scale(${a})`}>
          <MText x={0} y={20} s={String(n.v)} size={58} weight={800} anchor="middle" fill="#3a230c" />
        </g>;
      })}
      {[2, 1, 0].map((y, i) => {
        const a = seg(t, sumT[i], sumT[i] + 450, E.out);
        if (a <= 0) return null;
        const q = c.p([COLS + 0.62, y + 0.5, 0]);
        return <g key={y} opacity={a}>
          <Arrow p={[q[0] - 40, q[1]]} q={[q[0] + 2, q[1]]} stroke={C.soft} sw={3} h={13} />
          <MText x={q[0] + 14} y={q[1] + 15} s={String(ROW_SUM[y])} size={44} weight={800} fill={C.gold} C={C} />
        </g>;
      })}
      <Board x={1120} y={240} t={t} C={C} lines={[
        { t: B.a.build + 200, s: "층별로 세기", k: "h" },
        { t: LAYER_DONE[0], s: `1층 :  ${LAYERS[0]}개` },
        { t: LAYER_DONE[1], s: `2층 :  ${LAYERS[1]}개` },
        { t: LAYER_DONE[2], s: `3층 :  ${LAYERS[2]}개` },
        { t: B.a.tally + 300, s: `${LAYERS.join(" + ")} = ‹${TOTAL}›(개)` },
        { t: B.a.nums, s: "위에서 본 모양에 수 쓰기", k: "h" },
        { t: sumT[2] + 700, s: `${ROW_SUM.slice().reverse().join(" + ")} = ‹${TOTAL}›(개)` },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 400, s: "쌓기나무를 한 층씩 쌓아요" },
        { t: B.a.build + 6800, s: "뒤에 가려서 안 보이는 나무도 있어요" },
        { t: B.a.tally, s: `층별로 세면  ${LAYERS.join(" + ")} = ${TOTAL}개` },
        { t: B.a.tilt, s: "위에서 내려다보면?" },
        { t: B.a.nums, s: "위에서 본 모양의 칸마다 쌓은 개수를 써요" },
        { t: B.a.total, s: `칸의 수를 모두 더해도 ${TOTAL}개` },
      ]} />
    </g>
  );
}

/* ══════════ 중등: 최단 경로 ══════════ */
const PATH_COL = ["coral", "sky", "leaf", "lilac"];
function pathAt(moves, p) {
  // moves: "RRUU…" — 진행도 p 까지의 3D 점들
  const pts = [[0, 0, 0.02]];
  let x = 0, y = 0;
  const n = moves.length, steps = p * n;
  for (let i = 0; i < n; i++) {
    const f = clamp(steps - i, 0, 1);
    if (f <= 0) break;
    const dx = moves[i] === "R" ? 1 : 0, dy = moves[i] === "U" ? 1 : 0;
    pts.push([x + dx * f, y + dy * f, 0.02]);
    if (f < 1) break;
    x += dx; y += dy;
  }
  return pts;
}
function Mid({ t, C }) {
  const c = cam(t);
  const top = seg(t, B.a.tilt + 1800, B.b.tilt, E.sine);
  // 길 걷기
  const walkT = PATHS.map((_, i) => B.a.build + 400 + i * 2600);
  // 교차점 수: 가장자리 1 → 대각선 차례로
  const edgeT = (x, y) => B.a.nums + 200 + (y === 0 ? x : COLS + y) * 190;
  const diagT = (d) => B.a.nums + 2100 + (d - 2) * 1080;
  const ptT = (x, y) => (x === 0 || y === 0 ? edgeT(x, y) : diagT(x + y) + 520);
  // 바닥의 블록(길 사이 구역) — 초등의 나무가 놓였던 자리
  const tiles = [];
  for (let y = ROWS - 1; y >= 0; y--) for (let x = 0; x < COLS; x++) tiles.push({ x, y });
  const tileO = 1 - 0.55 * top;
  return (
    <g>
      <Floor c={c} C={C} o={seg(t, 200, 1600, E.sine)} strong />
      {tiles.map(({ x, y }) => {
        const P = [[x + 0.16, y + 0.16, 0], [x + 0.84, y + 0.16, 0], [x + 0.84, y + 0.84, 0], [x + 0.16, y + 0.84, 0]].map((q) => c.p(q));
        return <Path key={`${x}${y}`} pts={P} closed fill={C.sky} fo={0.13 * tileO} stroke={C.sky} sw={1.6} o={0.55 * seg(t, 300, 1800)} />;
      })}
      {PATHS.map((m, i) => {
        const p = seg(t, walkT[i], walkT[i] + 2300, E.io);
        if (p <= 0) return null;
        const pts = pathAt(m, p).map((q) => c.p(q));
        const fade = t > walkT[i] + 2300 ? 0.38 + 0.62 * (1 - seg(t, walkT[i] + 2300, walkT[i] + 3200)) : 1;
        const col = C[PATH_COL[i]];
        const head = pts.at(-1);
        return <g key={i} opacity={fade * (1 - 0.75 * seg(t, B.a.nums - 600, B.a.nums + 600))}>
          <Path pts={pts} stroke={col} sw={9} />
          {p < 1 && <circle cx={head[0]} cy={head[1]} r={12} fill={col} />}
        </g>;
      })}
      {/* A, B */}
      {[[0, 0, "A"], [COLS, ROWS, "B"]].map(([x, y, s]) => {
        const q = c.p([x, y, 0]);
        const o = seg(t, 600, 1500);
        return <g key={s} opacity={o}>
          <circle cx={q[0]} cy={q[1]} r={11} fill={C.gold} />
          <Lbl x={q[0] + (s === "A" ? -36 : 50)} y={q[1] + (s === "A" ? 30 : -44)} s={s} size={42} fill={C.gold} C={C} />
        </g>;
      })}
      {/* 교차점의 수 */}
      {top > 0 && PASCAL.flatMap((row, y) => row.map((v, x) => {
        const t0 = ptT(x, y);
        const a = seg(t, t0, t0 + 380, E.back);
        const q = c.p([x, y, 0]);
        const arrows = x > 0 && y > 0 ? seg(t, diagT(x + y), diagT(x + y) + 300) * (1 - seg(t, diagT(x + y) + 900, diagT(x + y) + 1250)) : 0;
        const fromL = c.p([x - 1, y, 0]), fromD = c.p([x, y - 1, 0]);
        const isB = x === COLS && y === ROWS;
        return (
          <g key={`${x}-${y}`}>
            {arrows > 0 && <g opacity={arrows}>
              <Arrow p={[lerp(fromL[0], q[0], 0.3), fromL[1]]} q={[lerp(fromL[0], q[0], 0.72), q[1]]} stroke={C.teal} sw={6} h={18} />
              <Arrow p={[fromD[0], lerp(fromD[1], q[1], 0.3)]} q={[q[0], lerp(fromD[1], q[1], 0.72)]} stroke={C.teal} sw={6} h={18} />
            </g>}
            {a > 0 && <g transform={`translate(${q[0]} ${q[1]}) scale(${a})`}>
              <circle r={isB ? 33 : 26} fill={C.paper} stroke={isB ? C.gold : C.soft} strokeWidth={isB ? 4 : 2} />
              <MText x={0} y={isB ? 12 : 10.5} s={String(v)} size={isB ? 34 : 29} weight={800} anchor="middle" fill={isB ? C.gold : C.ink} C={C} />
            </g>}
          </g>
        );
      }))}
      <Board x={1120} y={240} t={t} C={C} lines={[
        { t: B.a.build + 200, s: "A에서 B까지 가장 짧은 길", k: "h" },
        { t: LAYER_DONE[0], s: "→ 4번,  ↑ 3번" },
        { t: LAYER_DONE[1], s: "모두 7칸을 가요" },
        { t: B.a.tally + 300, s: "‹몇 가지›일까?" },
        { t: B.a.nums, s: "점마다 길의 수 쓰기", k: "h" },
        { t: B.a.nums + 2100, s: "(왼쪽 점) + (아래쪽 점)" },
        { t: B.a.total + 300, s: `B까지 ‹${PASCAL[ROWS][COLS]}›가지` },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 400, s: "A에서 B까지, 가장 짧은 길로 가요" },
        { t: B.a.build + 6800, s: "가장 짧은 길은 → 4번과 ↑ 3번의 순서만 달라요" },
        { t: B.a.tally, s: "가장 짧은 길은 모두 몇 가지일까?" },
        { t: B.a.tilt, s: "위에서 내려다보면 바둑판 길" },
        { t: B.a.nums, s: "한 점까지의 길의 수 = 왼쪽 점의 수 + 아래쪽 점의 수" },
        { t: B.a.total, s: `B까지 가는 가장 짧은 길은 ${PASCAL[ROWS][COLS]}가지` },
      ]} />
    </g>
  );
}

export default {
  key: "blocks",
  dur: B.dur,
  title: { e: "쌓기나무의 개수", m: "최단 경로의 수" },
  sub: { e: "초등 · 쌓기나무", m: "중등 · 경우의 수" },
  render: (mode, t, C) => (mode === "m" ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />),
};
