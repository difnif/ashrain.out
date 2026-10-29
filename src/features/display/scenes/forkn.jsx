// 장면 — 갈림길이 늘어나면(초등 · 규칙 찾기와 가능성) ↔ 갈림길이 늘어나면: 파스칼의 삼각형(중2 · 경우의 수와 확률)
// 갈림길을 한 단계씩 늘린다(설정: 단계 2~6). 단계가 하나 늘 때마다
//   · 길의 수는 2배 · 마디까지 가는 길의 수 = 위의 두 마디의 수의 합(파스칼의 삼각형)
//   · 오른쪽 막대: 구멍마다의 확률. 막대 하나가 반씩 쪼개져 양옆으로 가서 더해진다(= 위의 두 수의 합 ÷ 2)
// 다 늘린 뒤: 끝 구멍은 길이 늘 1가지 → 확률 ({1/2})ⁿ, 가운데는 길이 가장 많다.
// 마지막에 구슬 256개(결정적 난수)를 굴려 구멍에 모인 개수를 기대 개수(256 × 확률)와 견준다.
import { beats, seg, win, E, lerp } from "../core";
import { Board, Caption, MText, Path } from "../draw";
import { FORKN, HOLE_NAMES } from "../branch.js";

const CX = 450, Y0 = 214;
const CH = { x0: 900, x1: 1540, yBase: 520, h: 250 };       // 오른쪽 막대(확률 0 ~ {1/2})
const GROW = 2700, ROLL_GAP = 30, ROLL_LEV = 260;
const SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹";

const TLS = new Map();
const timeline = (n) => {
  if (!TLS.has(n)) TLS.set(n, beats([["intro", 2600], ...Array.from({ length: n }, (_, k) => [`g${k + 1}`, GROW]), ["read", 8600], ["roll", 10600], ["hold", 2200]]));
  return TLS.get(n);
};
const layout = (n) => {
  const dx = Math.min(140, 660 / n), dy = Math.min(120, 430 / n);
  return { n, dx, dy, node: (i, j) => [CX + (j - i / 2) * dx, Y0 + i * dy], hr: Math.min(34, dx * 0.3) };
};

function Scene({ t, C, mode, P }) {
  const isM = mode === "m";
  const n = P.n, B = timeline(n), L = layout(n), F = FORKN.of(n);
  // 지금까지 자란 단계(소수: 자라는 중)
  let lev = 0;
  for (let k = 1; k <= n; k++) lev += seg(t, B.a[`g${k}`] + 100, B.a[`g${k}`] + 1100, E.io);
  const levI = Math.floor(lev + 1e-9), grow = lev - levI;
  const o = seg(t, 150, 1100);
  const readO = seg(t, B.a.read, B.a.read + 600);
  return (
    <g>
      <Lattice L={L} C={C} t={t} B={B} lev={lev} levI={levI} grow={grow} isM={isM} o={o} F={F} readO={readO} />
      <Marbles L={L} C={C} t={t} B={B} F={F} isM={isM} />
      <Bars L={L} C={C} t={t} B={B} lev={lev} levI={levI} grow={grow} isM={isM} o={o} F={F} />
      <Board x={CH.x0 - 10} y={612} t={t} C={C} size={29} lh={50} lines={isM ? [
        { t: B.a.g1 + 300, s: "단계가 하나 늘면 길의 수는 2배", u: B.a.read },
        { t: B.a.g2 + 300, s: "마디의 수 = 위의 두 수의 합", u: B.a.read },
        { t: B.a.read + 300, s: `끝 구멍 A: 길 1가지 → ({1/2})${SUP[n]} = ‹{1/${F.total}}›`, row: 0 },
        { t: B.a.read + 2600, s: `가운데 구멍: 길 ${Math.max(...F.ways)}가지 → ‹${frac(F.P[Math.floor(n / 2)])}›`, row: 1 },
        { t: B.a.roll + 400, s: `구슬 ${FORKN.ROLLN}개 → 기대 개수 = ${FORKN.ROLLN} × 확률`, row: 2 },
      ] : [
        { t: B.a.g1 + 300, s: "갈림길이 하나 늘면 길이 2배", u: B.a.read },
        { t: B.a.g2 + 300, s: "마디의 수 = 위의 두 수의 합", u: B.a.read },
        { t: B.a.read + 300, s: `끝 구멍으로 가는 길은 늘 ‹1›가지`, row: 0 },
        { t: B.a.read + 2600, s: `가운데로 가는 길은 ‹${Math.max(...F.ways)}›가지`, row: 1 },
        { t: B.a.roll + 400, s: `구슬 ${FORKN.ROLLN}개를 굴려 보면`, row: 2 },
      ]} />
      <Caption t={t} C={C} y={862} size={33} caps={isM ? [
        { t: 300, s: "갈림길에서 왼쪽·오른쪽으로 갈 확률은 각각 {1/2}" },
        { t: B.a.g1 + 200, s: "갈림길을 한 단계씩 늘려 봐요" },
        { t: B.a.g2 + 400, s: "마디까지 가는 길의 수는 위의 두 수의 합 — 파스칼의 삼각형" },
        ...(n >= 3 ? [{ t: B.a.g3 + 400, s: "막대 하나가 반씩 나뉘어 양옆으로 — 확률도 위의 두 확률의 합의 반" }] : []),
        { t: B.a.read + 300, s: `구멍으로 갈 확률 = (그 구멍으로 가는 길의 수) ÷ 2${SUP[n]}` },
        { t: B.a.read + 4800, s: "단계가 늘수록 끝 구멍은 반씩 작아지고, 가운데로 몰려요" },
        { t: B.a.roll + 400, s: `실제로 ${FORKN.ROLLN}개를 굴려 기대 개수와 견주어 봐요` },
      ] : [
        { t: 300, s: "갈림길에서 왼쪽·오른쪽으로 갈 가능성은 반반이에요" },
        { t: B.a.g1 + 200, s: "갈림길을 한 단계씩 늘려 봐요" },
        { t: B.a.g2 + 400, s: "마디까지 가는 길의 수는 위의 두 수를 더하면 돼요" },
        ...(n >= 3 ? [{ t: B.a.g3 + 400, s: "갈림길이 늘수록 길의 수가 빠르게 늘어요" }] : []),
        { t: B.a.read + 300, s: "끝 구멍으로 가는 길은 늘 한 가지뿐이에요" },
        { t: B.a.read + 4800, s: "가운데 구멍일수록 길이 많아서 가능성이 커요" },
        { t: B.a.roll + 400, s: `${FORKN.ROLLN}개를 굴려 보면 가운데에 많이 모여요` },
      ]} />
    </g>
  );
}
const frac = (p) => (p[1] === 1 ? String(p[0]) : `{${p[0]}/${p[1]}}`);

/** 갈림길 판: 길(확률만큼 굵은 물줄기) · 마디(길의 수) · 지금 맨 아래 단계의 구멍 */
function Lattice({ L, C, t, B, lev, levI, grow, isM, o, F, readO }) {
  const { n, node } = L;
  const out = [];
  const [x0, y0] = node(0, 0);
  // 입구
  out.push(<Path key="ent" pts={[[x0 - 30, y0 - 78], [x0 - 12, y0 - 40], [x0 + 12, y0 - 40], [x0 + 30, y0 - 78]]} stroke={C.ink} sw={4} o={0.8} />);
  out.push(<Path key="ent2" pts={[[x0, y0 - 40], [x0, y0]]} stroke={C.gold} sw={4 + 30} o={0.22} />);
  // 길: i 단계 → i+1 단계(자라는 만큼)
  for (let i = 0; i < n; i++) {
    const p = i < levI ? 1 : i === levI ? grow : 0;
    if (p <= 0) continue;
    for (let j = 0; j <= i; j++) {
      const a = node(i, j), pr = comb(i, j) / 2 ** (i + 1);                            // 그 길로 흐르는 확률
      for (const d of [0, 1]) {
        const b = node(i + 1, j + d), q = [lerp(a[0], b[0], p), lerp(a[1], b[1], p)];
        out.push(<Path key={`w${i}-${j}-${d}`} pts={[a, q]} stroke={C.gold} sw={3 + 60 * pr} o={0.26} />);
        out.push(<Path key={`l${i}-${j}-${d}`} pts={[a, q]} stroke={C.ink} sw={2.4} o={0.55} />);
      }
    }
  }
  // 마디(갈림목)와 길의 수
  const numSize = Math.min(24, L.dx * 0.26);
  for (let i = 0; i <= Math.min(n, levI); i++) {
    const isHole = i === levI && i > 0;                 // 맨 처음(단계 0)은 구멍이 아니라 출발점
    for (let j = 0; j <= i; j++) {
      const [x, y] = node(i, j);
      const appear = i === 0 ? 1 : seg(t, B.a[`g${i}`] + 700, B.a[`g${i}`] + 1200);
      // 맨 아래 단계는 구멍(다음 단계가 자라면 갈림목으로 줄어든다)
      const shrink = isHole ? grow : 1;
      const r = isHole ? lerp(L.hr, 7, E.io(shrink)) : 7;
      out.push(
        <g key={`n${i}-${j}`} opacity={appear}>
          {isHole && r > 7.5
            ? <g><circle cx={x} cy={y} r={r} fill={C.paper} /><circle cx={x} cy={y} r={r} fill={C.ink} fillOpacity={0.1} stroke={C.ink} strokeWidth={3} /></g>
            : <circle cx={x} cy={y} r={7} fill={C.soft} />}
          <MText x={x} y={isHole && r > 7.5 ? y + 8 : y - 12} s={String(comb(i, j))} size={numSize} weight={800}
            anchor="middle" fill={C.teal} halo={C.halo} opacity={i === 0 ? 0 : isHole ? 1 - seg(t, B.a.roll + 300, B.a.roll + 700) : 1} C={C} />
          {isHole && <MText x={x} y={y + L.hr + 30} s={HOLE_NAMES[j]} size={Math.min(28, L.dx * 0.3)} weight={800} anchor="middle"
            fill={C.soft} opacity={1 - E.io(shrink)} C={C} />}
        </g>,
      );
    }
  }
  // 다 자란 뒤: 끝 구멍과 가운데 구멍 강조
  if (readO > 0) {
    const hi = (k, a) => { const [x, y] = node(n, k); return <circle key={"hi" + k} cx={x} cy={y} r={L.hr + 7} fill="none" stroke={C.gold} strokeWidth={4} opacity={a} />; };
    out.push(hi(0, win(t, B.a.read + 300, B.a.read + 2600, 400, 400)));
    const mids = n % 2 ? [Math.floor(n / 2), Math.ceil(n / 2)] : [n / 2];
    for (const k of mids) out.push(hi(k, seg(t, B.a.read + 2600, B.a.read + 3100)));
  }
  return <g opacity={o}>{out}</g>;
}
function comb(n, k) { let c = 1; for (let i = 1; i <= k; i++) c = (c * (n - k + i)) / i; return Math.round(c); }

/** 구슬 256개(결정적): 다 자란 판을 빠르게 굴러 구멍에 모인다 — 구멍 안 숫자 */
function Marbles({ L, C, t, B, F, isM }) {
  if (t < B.a.roll) return null;
  const { n, node } = L;
  const cols = [C.gold, C.coral, C.teal, C.sky];
  const cnt = new Array(n + 1).fill(0), out = [];
  const a0 = B.a.roll + 800, travel = ROLL_LEV * (n + 1);
  F.rolls.forEach((w, i) => {
    const s = a0 + i * ROLL_GAP, p = (t - s) / travel;
    if (p < 0) return;
    const h = w.reduce((a, b) => a + b, 0);
    if (p >= 1) { cnt[h]++; return; }
    // 입구 → 마디들 → 구멍
    const pts = [[node(0, 0)[0], node(0, 0)[1] - 40]];
    let j = 0;
    for (let i = 0; i <= n; i++) { pts.push(node(i, j)); if (i < n) j += w[i]; }
    const u = p * (pts.length - 1), k = Math.min(pts.length - 2, Math.floor(u)), f = u - k;
    out.push(<circle key={i} cx={lerp(pts[k][0], pts[k + 1][0], f)} cy={lerp(pts[k][1], pts[k + 1][1], f)} r={7} fill={cols[i % 4]} />);
  });
  const fade = 1 - seg(t, B.a.hold - 200, B.a.hold + 600);
  return (
    <g>
      <g opacity={fade}>{out}</g>
      {cnt.map((v, k) => {
        const [x, y] = node(n, k);
        return v > 0 && <MText key={k} x={x} y={y + 8} s={String(v)} size={Math.min(24, L.dx * 0.26)} weight={800} anchor="middle"
          fill={C.gold} halo={C.halo} C={C} />;
      })}
      {/* 중등: 다 굴린 뒤 기대 개수 */}
      {isM && F.expect.map((v, k) => {
        const [x, y] = node(n, k);
        return <MText key={"e" + k} x={x} y={y + L.hr + 56} s={`기대 ${v}`} size={Math.min(18, L.dx * 0.2)} weight={700} anchor="middle"
          fill={C.soft} opacity={seg(t, a0 + F.rolls.length * ROLL_GAP + travel, a0 + F.rolls.length * ROLL_GAP + travel + 500)} C={C} />;
      })}
    </g>
  );
}

/** 오른쪽 막대: 지금 단계의 구멍마다 확률. 단계가 늘 때 막대가 반씩 나뉘어 양옆으로 가서 쌓인다 */
function Bars({ L, C, t, B, lev, levI, grow, isM, o, F }) {
  const { n } = L;
  const sx = (CH.x1 - CH.x0) / ((n + 1) * L.dx), xc = (CH.x0 + CH.x1) / 2;
  const X = (i, j) => xc + (j - i / 2) * L.dx * sx, bw = L.dx * sx * 0.62;
  const H = (p) => (p / 0.5) * CH.h;
  const rects = [];
  const prob = (i, j) => comb(i, j) / 2 ** i;
  const showL = levI;                      // 다 자란 단계
  if (grow > 0 && levI < n) {
    // levI → levI+1 로 쪼개지는 중
    for (let j = 0; j <= levI; j++) {
      const p = prob(levI, j), x = X(levI, j), dxh = (L.dx * sx) / 2;
      const nextLeft = j + 1 <= levI ? prob(levI, j + 1) / 2 : 0;
      rects.push({ x: x - dxh * E.io(grow), b: 0, h: p / 2, c: C.sky });
      rects.push({ x: x + dxh * E.io(grow), b: lerp(p / 2, nextLeft, E.io(grow)), h: p / 2, c: C.teal });
    }
  } else {
    for (let j = 0; j <= showL; j++) rects.push({ x: X(showL, j), b: 0, h: prob(showL, j), c: C.sky });
  }
  const readO = seg(t, B.a.read + 600, B.a.read + 1200);
  const rollO = seg(t, B.a.roll + 400, B.a.roll + 1000);
  const doneLev = grow > 0 ? -1 : showL;
  if (lev <= 0.001) return null;
  return (
    <g opacity={o}>
      <MText x={CH.x0} y={200} s={isM ? `단계 ${Math.max(1, Math.round(lev))} — 구멍마다 확률` : `갈림길 ${Math.max(1, Math.round(lev))}번 — 구멍마다 가능성`} size={28} weight={800}
        opacity={seg(t, B.a.g1, B.a.g1 + 500)} C={C} />
      <Path pts={[[CH.x0 - 6, CH.yBase], [CH.x1 + 6, CH.yBase]]} stroke={C.ink} sw={2.6} />
      <line x1={CH.x0 - 6} x2={CH.x1 + 6} y1={CH.yBase - CH.h} y2={CH.yBase - CH.h} stroke={C.grid} strokeWidth={1.5} />
      <MText x={CH.x1 + 4} y={CH.yBase - CH.h - 8} s={isM ? "{1/2}" : "반반"} size={17} weight={600} anchor="end" fill={C.soft} C={C} />
      {rects.map((r, k) => <rect key={k} x={r.x - bw / 2} y={CH.yBase - H(r.b + r.h)} width={bw} height={Math.max(0, H(r.h))} rx={3}
        fill={r.c} fillOpacity={0.8} stroke={C.halo} strokeWidth={1} opacity={seg(t, B.a.g1, B.a.g1 + 400)} />)}
      {/* 막대 위: 확률(중등) · 길의 수(초등) */}
      {doneLev >= 1 && Array.from({ length: doneLev + 1 }, (_, j) => {
        const x = X(doneLev, j), p = prob(doneLev, j);
        return <MText key={"v" + j} x={x} y={CH.yBase - H(p) - 10} s={isM ? `{${comb(doneLev, j) / gcd(comb(doneLev, j), 2 ** doneLev)}/${2 ** doneLev / gcd(comb(doneLev, j), 2 ** doneLev)}}` : `${comb(doneLev, j)}`}
          size={Math.min(22, L.dx * sx * 0.3)} weight={700} anchor="middle" fill={C.ink} C={C} />;
      })}
      {doneLev >= 1 && Array.from({ length: doneLev + 1 }, (_, j) => (
        <MText key={"k" + j} x={X(doneLev, j)} y={CH.yBase + 28} s={HOLE_NAMES[j]} size={Math.min(22, L.dx * sx * 0.32)} weight={700} anchor="middle" fill={C.soft} C={C} />
      ))}
      {/* 굴린 결과: 기대 개수(점선)와 실제 개수(금빛 점) — 256개 기준 높이 */}
      {rollO > 0 && F.counts.map((v, j) => {
        const x = X(n, j), done = cntDone(t, B, F, n)[j];
        return (
          <g key={"r" + j} opacity={rollO}>
            <circle cx={x} cy={CH.yBase - H(done / FORKN.ROLLN)} r={7} fill={C.gold} stroke={C.halo} strokeWidth={2} />
          </g>
        );
      })}
      {rollO > 0 && <g opacity={rollO}>
        <circle cx={CH.x0 + 4} cy={232} r={7} fill={C.gold} />
        <MText x={CH.x0 + 18} y={239} s={isM ? `굴린 구슬 ${FORKN.ROLLN}개 가운데 들어간 비율` : `굴린 구슬 ${FORKN.ROLLN}개 가운데 들어간 비율`} size={20} weight={700} fill={C.soft} C={C} />
      </g>}
    </g>
  );
}
function gcd(a, b) { return b ? gcd(b, a % b) : a; }
/** t 까지 구멍에 들어간 구슬 수 */
function cntDone(t, B, F, n) {
  const a0 = B.a.roll + 800, travel = ROLL_LEV * (n + 1), c = new Array(n + 1).fill(0);
  F.rolls.forEach((w, i) => { if (t >= a0 + i * ROLL_GAP + travel) c[w.reduce((a, b) => a + b, 0)]++; });
  return c;
}

export default {
  key: "forkn",
  dur: (P) => timeline(P.n).dur,
  controls: [{ key: "n", label: "단계", kind: "step", options: FORKN.NS, def: FORKN.NDEF, unit: "번" }],
  title: { e: "갈림길이 늘어나면", m: "갈림길이 늘어나면 — 파스칼의 삼각형" },
  sub: { e: "초등 · 규칙 찾기와 가능성", m: "중2 · 경우의 수와 확률" },
  render: (mode, t, C, P) => <Scene t={t} C={C} mode={mode} P={P || { n: FORKN.NDEF }} />,
};
