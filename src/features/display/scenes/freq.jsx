// 장면 16 — 막대그래프(초등 4-1) ↔ 상대도수와 확률(중2)
// 같은 주사위 기록(결정적 난수)으로 같은 막대가 자란다. 30번까지는 두 판의 막대 높이가 똑같다.
//   초등: 눈금 한 칸 = 1번 → 60번까지 던지며 눈금 한 칸 = 2번 → 가장 많이/적게 나온 눈
//   중등: 눈금을 상대도수로 읽기 → 6000번까지 늘리면 모든 막대가 {1/6} 에 가까워진다 → 확률
import { beats, seg, E, lerp, clamp } from "../core";
import { Board, Caption, MText, DieFace, Path } from "../draw";
import { FREQ } from "../facts";

const B = beats([["intro", 2400], ["roll30", 7200], ["read30", 4400], ["more", 6800], ["final", 5200], ["hold", 2400]]);
const OX = 330, BASE = 700, PH = 400, BW = 60;
const barX = (f) => 400 + (f - 1) * 92;
const T30 = (i) => B.a.roll30 + 200 + i * 230;          // 1~30번째
const T60 = (j) => B.a.more + 1000 + j * 170;           // 31~60번째(초등)

/** 지금까지 던진 횟수(소수: 마지막 한 번이 자라는 중) */
function throwsAt(t, mode) {
  let n = 0;
  for (let i = 0; i < 30; i++) if (t >= T30(i)) n = i + seg(t, T30(i), T30(i) + 180);
  if (mode === "e") { for (let j = 0; j < 30; j++) if (t >= T60(j)) n = 30 + j + seg(t, T60(j), T60(j) + 150); return n; }
  const k = seg(t, B.a.more + 600, B.b.more - 400, E.in);
  return k > 0 ? 30 * Math.pow(FREQ.N / 30, k) : n;
}
/** 눈별 횟수 — 마지막 한 번은 부분 */
function countsAt(n) {
  const whole = Math.floor(n), frac = n - whole;
  const c = FREQ.countAt(whole);
  if (frac > 0 && whole < FREQ.N) c[FREQ.ROLLS[whole] - 1] += frac;
  return c;
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const n = throwsAt(t, mode);
  const cnt = countsAt(n);
  // 초등: 눈금 한 칸의 크기 1번 → 2번
  const rescale = isM ? 0 : seg(t, B.a.more, B.a.more + 900, E.io);
  const pxPer = lerp(40, 20, rescale);
  // 중등도 30번까지는 초등과 같은 높이(1번 = 40px ↔ 상대도수 {1/30} = 40px), 그 뒤로는 상대도수 × 1200px
  const H = (f) => clamp(isM ? (n <= 30 ? cnt[f - 1] * 40 : (cnt[f - 1] / n) * 1200) : cnt[f - 1] * pxPer, 0, PH + 20);
  const last = Math.floor(Math.max(0, n - 1e-9));
  const face = n > 0 ? FREQ.ROLLS[Math.min(FREQ.N - 1, last)] : 1;
  const fast = isM && n > 30.5;                              // 중등: 수천 번을 빠르게
  const wob = fast ? (t < B.b.more ? 8 * Math.sin(t / 40) : 0) : n > 0 ? 14 * Math.sin((n % 1) * Math.PI) : 0;
  const axisO = seg(t, 200, 1200);
  const rfO = isM ? seg(t, B.a.read30 + 400, B.a.read30 + 1100) : 0;
  const sixO = isM ? seg(t, B.a.read30 + 2000, B.a.read30 + 2600) : 0;
  const hiMax = !isM ? seg(t, B.a.final + 200, B.a.final + 700) : 0;
  const maxF = n > 31 ? FREQ.max60 : FREQ.max30;
  // 눈금 글자
  const ticksE = [0, 2, 4, 6, 8, 10];
  return (
    <g>
      {/* 주사위와 던진 횟수 */}
      <DieFace cx={180} cy={300} s={120} n={face} C={C} rot={wob} o={axisO} />
      <MText x={180} y={420} s="던진 횟수" size={26} weight={700} anchor="middle" fill={C.soft} opacity={axisO} C={C} />
      <MText x={180} y={478} s={`${Math.floor(n)}번`} size={48} weight={800} anchor="middle" fill={C.gold} opacity={axisO} C={C} />
      {/* 축·눈금선 */}
      <g opacity={axisO}>
        {Array.from({ length: 11 }, (_, i) => <line key={i} x1={OX} x2={OX + 580} y1={BASE - i * 40} y2={BASE - i * 40}
          stroke={C.faint} strokeWidth={i === 0 ? 0 : 1.2} />)}
        <Path pts={[[OX, BASE - PH - 20], [OX, BASE], [OX + 590, BASE]]} stroke={C.ink} sw={3} />
        {!isM && ticksE.map((v, i) => (
          <g key={v}>
            <MText x={OX - 14} y={BASE - i * 80 + 10} s={String(v)} size={24} weight={600} anchor="end" fill={C.soft} opacity={1 - rescale} C={C} />
            <MText x={OX - 14} y={BASE - i * 80 + 10} s={String(v * 2)} size={24} weight={600} anchor="end" fill={C.soft} opacity={rescale} C={C} />
          </g>
        ))}
        {isM && <g>
          {ticksE.map((v, i) => <MText key={v} x={OX - 14} y={BASE - i * 80 + 10} s={String(v)} size={24} weight={600} anchor="end"
            fill={C.soft} opacity={1 - rfO} C={C} />)}
          {[0, 0.1, 0.2, 0.3].map((v) => <MText key={v} x={OX - 14} y={BASE - v * 1200 + 10} s={v === 0 ? "0" : v.toFixed(1)} size={24}
            weight={600} anchor="end" fill={C.teal} opacity={rfO} C={C} />)}
        </g>}
        <MText x={OX - 6} y={BASE - PH - 34} s={isM && rfO > 0.5 ? "(상대도수)" : "(번)"} size={22} weight={700} anchor="middle"
          fill={isM && rfO > 0.5 ? C.teal : C.soft} C={C} />
        {[1, 2, 3, 4, 5, 6].map((f) => <DieFace key={f} cx={barX(f)} cy={BASE + 34} s={38} n={f} C={C} />)}
      </g>
      {/* 막대 */}
      {[1, 2, 3, 4, 5, 6].map((f) => {
        const h = H(f);
        const isMax = !isM && f === maxF && hiMax > 0;
        const isMin = !isM && f === FREQ.min60 && hiMax > 0;
        const col = isMax ? C.gold : isMin ? C.teal : isM ? C.lilac : C.sky;
        return h > 0.5 && <g key={f}>
          <rect x={barX(f) - BW / 2} y={BASE - h} width={BW} height={h} rx={5} fill={col} fillOpacity={0.75} stroke={col} strokeWidth={2} />
          {!isM && n <= 30.5 && t > B.a.read30 && <MText x={barX(f)} y={BASE - h - 12} s={String(Math.round(cnt[f - 1]))} size={24} weight={700}
            anchor="middle" fill={C.ink} opacity={seg(t, B.a.read30, B.a.read30 + 400) * (1 - seg(t, B.a.more, B.a.more + 300))} C={C} />}
        </g>;
      })}
      {/* 중등: {1/6} 선 */}
      {sixO > 0 && <g opacity={sixO}>
        <line x1={OX} x2={OX + 590} y1={BASE - 200} y2={BASE - 200} stroke={C.gold} strokeWidth={3} strokeDasharray="12 9" />
        <MText x={OX + 600} y={BASE - 190} s="{1/6}" size={30} weight={700} fill={C.gold} C={C} />
      </g>}
      <Board x={980} y={232} t={t} C={C} size={34} lh={58} lines={isM ? [
        { t: B.a.read30 + 200, s: "상대도수", k: "h" },
        { t: B.a.read30 + 600, s: "= {(그 눈이 나온 횟수)/(던진 횟수)}" },
        { t: B.a.read30 + 2400, s: FREQ.M.ex30 },
        { t: B.a.more + 200, s: "던진 횟수를 늘리면", k: "h" },
        { t: B.b.more - 300, s: FREQ.M.range },
        { t: B.a.final + 300, s: "상대도수가 {1/6}에 가까워져요" },
        { t: B.a.final + 1800, s: "‹(한 눈이 나올 확률) = {1/6}›" },
      ] : [
        { t: B.a.read30 + 200, s: "막대그래프", k: "h" },
        { t: B.a.read30 + 600, s: "눈금 한 칸 = ‹1›번" },
        { t: B.a.read30 + 2200, s: FREQ.E.max30 },
        { t: B.a.more + 200, s: "60번까지 던지면", k: "h" },
        { t: B.a.more + 900, s: "눈금 한 칸 = ‹2›번" },
        { t: B.a.final + 300, s: FREQ.E.max60 },
        { t: B.a.final + 1300, s: FREQ.E.min60 },
      ]} />
      <Caption t={t} C={C} caps={isM ? [
        { t: 300, s: "주사위를 던져 나온 눈을 기록해요" },
        { t: B.a.roll30, s: "한 번 던질 때마다 막대가 한 칸씩 올라가요" },
        { t: B.a.read30, s: "같은 막대를 상대도수로 읽어요" },
        { t: B.a.more, s: "던진 횟수를 6000번까지 늘리면" },
        { t: B.a.final, s: "상대도수가 일정한 값 {1/6}에 가까워져요 — 이 값이 확률" },
      ] : [
        { t: 300, s: "주사위를 던져 나온 눈을 기록해요" },
        { t: B.a.roll30, s: "한 번 던질 때마다 막대가 한 칸씩 올라가요" },
        { t: B.a.read30, s: "막대의 길이로 많고 적음을 한눈에 비교해요" },
        { t: B.a.more, s: "60번까지 던지면 — 눈금 한 칸을 2번으로 바꿔요" },
        { t: B.a.final, s: FREQ.E.cap },
      ]} />
    </g>
  );
}

export default {
  key: "freq",
  dur: B.dur,
  title: { e: "막대그래프", m: "상대도수와 확률" },
  sub: { e: "초등 · 막대그래프", m: "중2 · 확률의 뜻" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
