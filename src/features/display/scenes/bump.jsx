// 장면 — 구슬이 부딪히면(초등 · 가능성) ↔ 동시에 굴리면: 독립이 깨질 때(중2 · 확률의 곱)
// 같은 갈림길 판 두 개를 물리 엔진으로 굴린다. 왼쪽은 하나씩, 오른쪽은 두 개씩 나란히 한꺼번에.
//   한 판은 천천히, 한 판은 보통 빠르기로 보여 준 뒤, 300판씩 모아 "구멍마다 들어간 개수의 모양"별 비율을
//   이론값(서로 영향이 없을 때 = 곱의 법칙)과 견준다.
//   하나씩: 구슬끼리 만나지 않는다 → 이론값과 비슷.
//   동시에: 첫 갈림목에 나란히 닿은 구슬이 서로 밀어낸다 → 독립이 아니다 → 결과가 달라진다.
// 판정 글(크게·조금·거의 같다)과 강조할 모양은 실제로 모은 결과에서 고른다(설정마다 다르다).
import { beats, seg, win, E, clamp, fmt } from "../core";
import { Board, Caption, MText, Path, mathWidth } from "../draw";
import {
  BUMP, HOLE_NAMES, POST, bumpLayout, bumpWorld, bumpRuns, chuteWalls, shapeProbs, shapeFreq, shapeLabel, MARBLE,
} from "../branch.js";
import { simAt } from "../physics.js";

const SLOW = 0.55;                                   // 첫 판은 천천히
const LEAD = 450;                                    // 판이 시작되고 구슬을 놓기까지(ms)
const YA = 300;                                      // 판의 천장(출발 통 아래 끝)이 오는 화면 높이
/** 판 두 개의 자리와 크기: 단계가 많을수록 판이 넓어 조금 작게 그린다 */
function placeOf(L) {
  const s = { 1: 1.45, 2: 1.35, 3: 1.05 }[L.n] || 1;
  const hw = ((L.n + 1) * L.dx) / 2 + 2.5, gap = 60, span = 4 * hw * s + gap;
  const x0 = 40 + (935 - span) / 2;
  const Yc = L.y0 - L.neckH;
  const at = (X) => ({ X, s, tf: (x, y) => [X + s * x, YA + s * (y - Yc)], tr: `translate(${X} ${YA}) scale(${s}) translate(0 ${-Yc})` });
  return { seq: at(x0 + hw * s), sim: at(x0 + 3 * hw * s + gap) };
}
const PANEL = { x0: 1012, x1: 1526, yTop: 318, yBase: 566 };
const pct = (p) => `${fmt(p * 100, 1)}%`;

const TLS = new Map();
function timeline(n, m) {
  const k = `${n}|${m}`;
  if (!TLS.has(k)) {
    // 시범 두 판(씨앗 1·2)이 다 멈추는 시각(세계 초) — 두 판 중 늦은 쪽
    const d = [0, 1].map((r) => Math.max(...["seq", "sim"].map((md) => bumpRuns(n, m, md, 2, 1)[r].t)));
    TLS.set(k, beats([
      ["intro", 2800], ["r1", LEAD + Math.ceil((d[0] * 1000) / SLOW) + 2700], ["r2", LEAD + Math.ceil(d[1] * 1000) + 2400],
      ["tally", 8000], ["sum", 10500], ["hold", 1500],
    ]));
  }
  return TLS.get(k);
}

/** 모은 결과: 모양마다 이론·하나씩·동시에 비율, 가장 크게 달라진 모양과 판정 */
const VERD = new Map();
function verdictOf(n, m) {
  const k = `${n}|${m}`;
  if (!VERD.has(k)) {
    const T = BUMP.TRIALS;
    const fs = shapeFreq(bumpRuns(n, m, "seq", T), T), fm = shapeFreq(bumpRuns(n, m, "sim", T), T);
    const cats = shapeProbs(n, m).map((o) => ({ key: o.key, th: o.p, seq: fs(o.key), sim: fm(o.key) }));
    // 가장 크게 달라진 모양(구슬 2개는 늘 "같은 구멍"으로 — 두 모양의 차이는 크기가 같다)
    let best = cats[0];
    for (const c of cats) if (Math.abs(c.sim - c.th) > Math.abs(best.sim - best.th)) best = c;
    if (m === 2) best = cats.find((c) => c.key.startsWith("2"));
    const d = Math.abs(best.sim - best.th);
    VERD.set(k, { cats, best, up: best.sim > best.th, tier: d >= 0.08 ? 2 : d >= 0.04 ? 1 : 0 });
  }
  return VERD.get(k);
}
/** 모양 이름 — 구슬 2개면 "같은 구멍 / 다른 구멍" */
const catName = (key, m) => (m === 2 ? (key.startsWith("2") ? "같은 구멍" : "다른 구멍") : shapeLabel(key));

function Scene({ t, C, mode, P }) {
  const isM = mode === "m";
  const n = P.n, m = P.m;
  const B = timeline(n, m);
  const L = bumpLayout(n, m);
  const cols = [C.gold, C.coral, C.teal, C.sky];
  const boardO = seg(t, 150, 1100);
  // 지금 보여 줄 판: 1판(천천히) → 2판 → 모아 보기(판마다 결과만 빠르게)
  const round = t < B.a.r2 ? 1 : 2;
  const r0 = round === 1 ? B.a.r1 : B.a.r2, speed = round === 1 ? SLOW : 1;
  const wms = Math.max(0, t - r0 - LEAD) * speed;
  const fadeOut = 1 - seg(t, (round === 1 ? B.b.r1 : B.b.r2) - 550, round === 1 ? B.b.r1 : B.b.r2);
  const fadeIn = round === 1 ? seg(t, B.a.r1 - 900, B.a.r1 - 200) : seg(t, B.a.r2, B.a.r2 + 380);
  const live = t < B.a.tally;
  const T = BUMP.TRIALS;
  const cnt = Math.round(T * seg(t, B.a.tally + 500, B.b.tally - 500, E.sine));
  // 판정은 다 모은 뒤에만(모아 보는 동안 한꺼번에 300판을 돌리지 않게 — 그때쯤엔 이미 다 돌려 두었다)
  const V = t >= B.a.sum - 100 ? verdictOf(n, m) : null;
  const sumO = seg(t, B.a.sum, B.a.sum + 700);
  const nm = { seq: "하나씩", sim: isM ? "동시에" : "한꺼번에" };
  const PL = placeOf(L);
  return (
    <g>
      {["seq", "sim"].map((md) => {
        const W = live ? simAt(`bump|${n}|${m}|${md}|${round}`, () => bumpWorld(n, m, md, round), wms) : null;
        const runs = !live && cnt > 0 ? bumpRuns(n, m, md, cnt) : null;
        // 모아 보는 동안: 판마다 결과(구멍별 개수)만 빠르게 바꿔 보여 준다(1초에 아홉 판쯤)
        const show = runs ? runs[Math.max(0, Math.min(cnt - 1, Math.floor(cnt / 4) * 4 - 1))] : null;
        const pl = PL[md];
        return (
          <g key={md}>
            <g transform={pl.tr}>
              <ChuteBoard L={L} C={C} o={boardO} />
              {W && <Marbles W={W} L={L} C={C} cols={cols} md={md} o={fadeIn * fadeOut} />}
              {W && <Sparks W={W} C={C} o={fadeOut} />}
              {W && <Gate W={W} L={L} C={C} md={md} o={boardO} />}
              {show && <Settled L={L} counts={show.counts} C={C} cols={cols} o={0.9 * (1 - 0.45 * sumO)} />}
            </g>
            <BoardText L={L} pl={pl} C={C} o={boardO} name={nm[md]} col={md === "seq" ? C.sky : C.coral} />
            {W && <Result W={W} L={L} pl={pl} C={C} m={m} o={fadeOut} />}
            {!live && <MText x={pl.X} y={pl.tf(0, L.yFloor)[1] + 78} s={`${Math.min(cnt, T)}판`} size={24} weight={700} anchor="middle"
              fill={C.soft} opacity={seg(t, B.a.tally, B.a.tally + 400)} C={C} />}
          </g>
        );
      })}
      <Chart t={t} B={B} C={C} n={n} m={m} isM={isM} cnt={cnt} V={V} o={boardO} />
      <Board x={PANEL.x0 + 16} y={652} t={t} C={C} size={27} lh={44} lines={isM ? [
        { t: 700, s: "하나씩: 구슬끼리 만나지 않는다", u: B.a.tally },
        { t: 1500, s: "동시에: 두 개씩 나란히 떨어진다", u: B.a.tally },
        { t: B.a.r1 + LEAD + 900, s: "→ 첫 갈림목에서 서로 밀어낸다", u: B.a.tally },
        { t: B.a.tally + 300, s: "이론값 = 서로 영향이 없을 때(독립)", row: 0, u: B.a.sum },
        { t: B.a.tally + 1200, s: "곱의 법칙으로 계산한 확률", row: 1, u: B.a.sum },
        ...(V ? [
          { t: B.a.sum + 200, s: `‹${catName(V.best.key, m)}›인 판`, k: "h", row: 0 },
          { t: B.a.sum + 700, s: `이론 ${pct(V.best.th)} · 하나씩 ${pct(V.best.seq)}`, row: 1 },
          { t: B.a.sum + 1300, s: `동시에 ‹${pct(V.best.sim)}›`, row: 2 },
        ] : []),
      ] : [
        { t: 700, s: "하나씩: 한 개가 다 내려간 뒤에", u: B.a.tally },
        { t: 1500, s: "한꺼번에: 두 개씩 나란히", u: B.a.tally },
        { t: B.a.r1 + LEAD + 900, s: "→ 첫 갈림길에서 서로 밀어내요", u: B.a.tally },
        { t: B.a.tally + 300, s: "계산값 = 서로 부딪히지 않을 때", row: 0, u: B.a.sum },
        { t: B.a.tally + 1200, s: "(길의 수로 따진 가능성)", row: 1, u: B.a.sum },
        ...(V ? [
          { t: B.a.sum + 200, s: `‹${catName(V.best.key, m)}›인 판`, k: "h", row: 0 },
          { t: B.a.sum + 700, s: `계산 ${pct(V.best.th)} · 하나씩 ${pct(V.best.seq)}`, row: 1 },
          { t: B.a.sum + 1300, s: `한꺼번에 ‹${pct(V.best.sim)}›`, row: 2 },
        ] : []),
      ]} />
      <Caption t={t} C={C} y={862} size={32} caps={isM ? [
        { t: 300, s: `같은 판에 구슬 ${m}개 — 하나씩 굴릴 때와 동시에 굴릴 때` },
        { t: B.a.r1 + 200, s: "천천히 볼까요? 동시에 굴린 구슬은 첫 갈림목에 함께 닿아요" },
        { t: B.a.r1 + LEAD + 1700, s: "나란히 닿은 두 구슬은 서로 밀어내 반대쪽으로 가요" },
        { t: B.a.r2 + 200, s: "한 번 더 — 이번엔 보통 빠르기로" },
        { t: B.a.tally + 200, s: `${T}판씩 해 보면?` },
        ...(V ? [{ t: B.a.sum + 200, s: verdictText(V, m, true) }] : []),
        { t: B.a.sum + 5200, s: "곱의 법칙은 서로 영향을 주지 않을 때(독립)에만 쓸 수 있어요" },
      ] : [
        { t: 300, s: `구슬 ${m}개를 하나씩 굴릴 때와 한꺼번에 굴릴 때` },
        { t: B.a.r1 + 200, s: "천천히 볼까요? 한꺼번에 굴리면 함께 내려가요" },
        { t: B.a.r1 + LEAD + 1700, s: "나란히 닿은 구슬은 서로 밀어내요" },
        { t: B.a.r2 + 200, s: "한 번 더 볼까요?" },
        { t: B.a.tally + 200, s: `${T}번씩 해 보면?` },
        ...(V ? [{ t: B.a.sum + 200, s: verdictText(V, m, false) }] : []),
        { t: B.a.sum + 5200, s: "구슬끼리 부딪히면 가능성이 달라질 수 있어요" },
      ]} />
    </g>
  );
}

function verdictText(V, m, isM) {
  const lab = catName(V.best.key, m), dir = V.up ? "늘어요" : "줄어요";
  const who = isM ? "동시에" : "한꺼번에";
  if (V.tier === 2) return isM ? `${who} 굴리면 ‹${lab}›인 판이 크게 ${dir} — 부딪힘 때문이에요` : `${who} 굴리면 ‹${lab}›인 판이 많이 ${dir}`;
  if (V.tier === 1) return `${who} 굴리면 ‹${lab}›인 판이 조금 ${dir}`;
  return isM ? "이번엔 거의 같아요 — 갈림길을 여러 번 지나며 부딪힌 영향이 흐려졌어요" : "이번엔 거의 비슷해요 — 여러 번 갈라지며 영향이 흐려졌어요";
}

/** 판: 벽(굵은 선) · 갈림목 지붕은 살짝 채우고 · 칸막이는 뾰족한 기둥으로 */
function ChuteBoard({ L, C, o }) {
  const walls = chuteWalls(L);
  return (
    <g opacity={o}>
      {walls.map((w, i) => {
        if (w.kind === "tip") return null;
        if (w.kind === "post") {
          const [[x, y], [, y1]] = w.pts, h = w.hw, tip = POST.tip;
          return <Path key={i} pts={[[x - h, y1], [x - h, y], [x, y - tip - 2], [x + h, y], [x + h, y1]]} closed stroke={C.ink} sw={1.5}
            fill={C.ink} fo={0.85} o={0.9} />;
        }
        return <Path key={i} pts={w.pts} closed={w.kind === "roof"} stroke={C.ink} sw={2 * w.hw} fill={w.kind === "roof" ? C.ink : "none"} fo={0.22} o={0.85} />;
      })}
    </g>
  );
}
/** 판 밖 글자(크기를 키운 판과 따로): 구멍 이름 · 판 이름 */
function BoardText({ L, pl, C, o, name, col }) {
  const yH = pl.tf(0, L.yFloor)[1] + 34;
  const [nx, ny] = pl.tf(-L.tw - 12, L.y0 - L.neckH - 12);
  return (
    <g opacity={o}>
      {L.bins.map((b, k) => <MText key={k} x={pl.tf(b.xc, 0)[0]} y={yH} s={HOLE_NAMES[k]} size={28} weight={700} anchor="middle" fill={C.soft} C={C} />)}
      <MText x={nx} y={ny} s={name} size={32} weight={800} anchor="end" fill={col} C={C} />
    </g>
  );
}

/** 구슬: 나온 것은 세계의 자리, 기다리는 것은 출발 통 안(하나씩은 한 줄, 동시에는 두 줄) */
function Marbles({ W, L, C, cols, md, o }) {
  if (o <= 0.01) return null;
  const out = [];
  // 하나씩: 방금 하나가 나가면 위의 구슬이 한 칸씩 내려온다
  const last = W.nextSpawn > 0 ? W.spawnAt[W.order[W.nextSpawn - 1]] : -1;
  const shift = last >= 0 ? E.io(clamp((W.time - last) / 0.35)) : 1;
  for (let i = 0; i < W.n; i++) {
    let x, y;
    if (W.st[i] === MARBLE.WAIT) {
      if (md === "seq") { const k = i - W.nextSpawn + (1 - shift); [x, y] = L.slotSeq(0); y -= k * L.pitch; }
      else [x, y] = L.slotSim(i);
    } else { x = W.x[i]; y = W.y[i]; }
    out.push(
      <g key={i}>
        <circle cx={x} cy={y} r={L.r} fill={cols[i % 4]} />
        <text x={x} y={y + L.r * 0.42} fontSize={L.r * 1.15} fontWeight={800} textAnchor="middle" fill={C.halo}>{i + 1}</text>
      </g>,
    );
  }
  return <g opacity={o}>{out}</g>;
}

/** 부딪혀 길이 정해진 자리에 잠깐 번쩍(세계 시각 0.7초) */
function Sparks({ W, C, o }) {
  if (!W.crowds || o <= 0.01) return null;
  return (
    <g opacity={o}>
      {W.crowds.map((c, k) => {
        const a = W.time - c.t;
        if (a < 0 || a > 0.7) return null;
        const p = a / 0.7, rr = 16 + 22 * E.out(p), al = 1 - p;
        return (
          <g key={k} opacity={al}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map((j) => {
              const an = (j / 8) * Math.PI * 2 + 0.3;
              return <line key={j} x1={c.x + Math.cos(an) * rr * 0.55} y1={c.y - 18 + Math.sin(an) * rr * 0.55}
                x2={c.x + Math.cos(an) * rr} y2={c.y - 18 + Math.sin(an) * rr} stroke={C.gold} strokeWidth={3.5} strokeLinecap="round" />;
            })}
          </g>
        );
      })}
    </g>
  );
}

/** 출발 통의 문: 하나씩은 구슬을 내보낼 때만, 동시에는 한 번 열리면 계속 열린다 */
function Gate({ W, L, C, md, o }) {
  let open = 0;
  for (let i = 0; i < W.n; i++) {
    const a = W.time - W.spawnAt[i];
    open = Math.max(open, md === "seq" ? win(a * 1000, -40, 260, 40, 80) : (a >= -0.04 ? 1 : 0));
  }
  const y = L.gateY + L.r + 3.5, w = L.tw;
  return <Path pts={[[-w, y], [w, y]]} stroke={C.gold} sw={5} o={o * (1 - open)} />;
}

/** 판이 끝나면 결과(구슬 2개: 같은/다른 구멍, 그 밖: 모양) */
function Result({ W, L, pl, C, m, o }) {
  if (W.live.length || W.nextSpawn < W.n) return null;
  const counts = new Array(L.n + 1).fill(0);
  for (let i = 0; i < W.n; i++) {
    const k = Math.floor((W.x[i] - L.bins[0].x0) / L.dx);
    if (k >= 0 && k <= L.n) counts[k]++;
  }
  const key = [...counts].sort((a, b) => b - a).join("-");
  const lab = catName(key, m);
  const a = seg(W.time, (W.lastFreeze || 0) + 0.25, (W.lastFreeze || 0) + 0.65) * o;
  const w = Math.max(120, mathWidth(lab, 25, 800) + 44), y = pl.tf(0, L.yFloor)[1] + 52;
  return (
    <g opacity={a}>
      <rect x={pl.X - w / 2} y={y} width={w} height={42} rx={21} fill={m === 2 && key.startsWith("2") ? C.coral : C.ink} fillOpacity={0.18} />
      <MText x={pl.X} y={y + 30} s={lab} size={25} weight={800} anchor="middle" fill={C.ink} C={C} />
    </g>
  );
}

/** 모아 보는 동안: 그 판의 결과만 구멍 바닥에 늘어놓는다 */
function Settled({ L, counts, C, cols, o }) {
  const out = [];
  let idx = 0;
  counts.forEach((c, k) => {
    for (let q = 0; q < c; q++) {
      const row = Math.floor(q / 3), col = q % 3, inRow = Math.min(3, c - row * 3);
      const x = L.bins[k].xc + (col - (inRow - 1) / 2) * (2 * L.r + 3), y = L.yFloor - 2.5 - L.r - row * (2 * L.r + 1);
      out.push(<circle key={`${k}-${q}`} cx={x} cy={y} r={L.r} fill={cols[idx++ % 4]} />);
    }
  });
  return <g opacity={o}>{out}</g>;
}

/** 오른쪽: 모양별 비율 — 이론(점선) · 하나씩 · 동시에 */
function Chart({ t, B, C, n, m, isM, cnt, V, o }) {
  const { x0, x1, yTop, yBase } = PANEL;
  const cats = shapeProbs(n, m);
  const slot = (x1 - x0) / cats.length, bw = Math.min(46, slot * 0.3);
  const hh = (v) => v * (yBase - yTop);
  const T = BUMP.TRIALS;
  const fs = cnt > 0 ? shapeFreq(bumpRuns(n, m, "seq", cnt), cnt) : null;
  const fm = cnt > 0 ? shapeFreq(bumpRuns(n, m, "sim", cnt), cnt) : null;
  const thO = seg(t, B.a.intro + 1800, B.a.intro + 2600);
  const valO = seg(t, B.b.tally - 400, B.b.tally + 300);
  const hiO = seg(t, B.a.sum + 200, B.a.sum + 800);
  return (
    <g opacity={o}>
      <MText x={x0} y={222} s={cnt > 0 ? `‹${Math.min(cnt, T)}›판씩 모아 보면` : m === 2 ? "두 구슬이 같은 구멍에 들어갈까?" : "구멍마다 몇 개씩 들어갈까?"} size={30} weight={800} C={C} />
      {/* 범례 */}
      <g>
        <rect x={x0} y={252} width={18} height={18} rx={3} fill={C.sky} opacity={0.85} />
        <MText x={x0 + 26} y={268} s="하나씩" size={20} weight={700} fill={C.soft} C={C} />
        <rect x={x0 + 112} y={252} width={18} height={18} rx={3} fill={C.coral} opacity={0.85} />
        <MText x={x0 + 138} y={268} s={isM ? "동시에" : "한꺼번에"} size={20} weight={700} fill={C.soft} C={C} />
        <line x1={x0 + 248} x2={x0 + 276} y1={261} y2={261} stroke={C.gold} strokeWidth={3} strokeDasharray="6 4" opacity={thO} />
        <MText x={x0 + 284} y={268} s={isM ? "이론값(독립)" : "계산값"} size={20} weight={700} fill={C.soft} opacity={thO} C={C} />
      </g>
      {/* 눈금 */}
      {[0.25, 0.5, 0.75, 1].map((v) => (
        <g key={v}>
          <line x1={x0} x2={x1} y1={yBase - hh(v)} y2={yBase - hh(v)} stroke={C.grid} strokeWidth={1.5} />
          <MText x={x1 + 4} y={yBase - hh(v) + 6} s={`${v * 100}%`} size={15} weight={600} fill={C.soft} opacity={0.8} C={C} />
        </g>
      ))}
      <Path pts={[[x0 - 4, yBase], [x1 + 4, yBase]]} stroke={C.ink} sw={2.6} />
      {cats.map((c, k) => {
        const xc = x0 + slot * (k + 0.5);
        const vs = fs ? fs(c.key) : 0, vm = fm ? fm(c.key) : 0;
        const hiK = V && V.best.key === c.key ? hiO : 0;
        return (
          <g key={c.key}>
            {hiK > 0.01 && <rect x={xc - bw - 14} y={yTop - 30} width={2 * bw + 28} height={yBase - yTop + 30 + 64} rx={12}
              fill="none" stroke={C.gold} strokeWidth={3} opacity={hiK} />}
            {vs > 0 && <rect x={xc - bw - 3} y={yBase - hh(vs)} width={bw} height={hh(vs)} rx={3} fill={C.sky} fillOpacity={0.8} />}
            {vm > 0 && <rect x={xc + 3} y={yBase - hh(vm)} width={bw} height={hh(vm)} rx={3} fill={C.coral} fillOpacity={0.8} />}
            <line x1={xc - bw - 10} x2={xc + bw + 10} y1={yBase - hh(c.p)} y2={yBase - hh(c.p)} stroke={C.gold} strokeWidth={3.2}
              strokeDasharray="7 5" opacity={thO} />
            <MText x={xc - bw / 2 - 3} y={yBase - hh(vs) - 8} s={`${Math.round(vs * 100)}`} size={17} weight={700} anchor="middle" fill={C.sky} opacity={valO} C={C} />
            <MText x={xc + bw / 2 + 3} y={yBase - hh(vm) - 8} s={`${Math.round(vm * 100)}`} size={17} weight={700} anchor="middle" fill={C.coral} opacity={valO} C={C} />
            <MText x={xc} y={yBase + 28} s={catName(c.key, m)} size={cats.length > 4 ? 18 : 21} weight={700} anchor="middle" C={C} />
            <MText x={xc} y={yBase + 52} s={pct(c.p)} size={16} weight={600} anchor="middle" fill={C.gold} opacity={thO} C={C} />
          </g>
        );
      })}
    </g>
  );
}

export default {
  key: "bump",
  dur: (P) => timeline(P.n, P.m).dur,
  controls: [
    { key: "n", label: "단계", kind: "step", options: BUMP.NS, def: BUMP.NDEF, unit: "번" },
    { key: "m", label: "구슬", kind: "step", options: BUMP.MS, def: BUMP.MDEF, unit: "개" },
  ],
  title: { e: "구슬이 부딪히면?", m: "동시에 굴리면 — 독립이 깨질 때" },
  sub: { e: "초등 · 일이 일어날 가능성", m: "중2 · 확률의 계산(곱의 법칙)" },
  render: (mode, t, C, P) => <Scene t={t} C={C} mode={mode} P={P || { n: BUMP.NDEF, m: BUMP.MDEF }} />,
};
