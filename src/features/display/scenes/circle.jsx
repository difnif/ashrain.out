// 장면 2 — 원주와 원의 넓이(초등) ↔ 부채꼴의 호의 길이와 넓이(중등)
// 같은 원(반지름 5 cm)을 같은 박자로 굴리고, 같은 박자로 잘게 잘라 번갈아 붙인다.
//   초등: 한 바퀴 → 원주 = 지름 × 3.14 · 16조각 → 직사각형(가로 = 원주의 1/2, 세로 = 반지름)
//   중등: 호(72°)가 먼저 펴진다 → l = 2π · 부채꼴 8조각 → 직사각형(가로 = l/2, 세로 = r) → S = ½rl
import { beats, seg, E, lerp, rad, polar, arcPts } from "../core";
import { Board, Caption, Path, Lbl, Dot, Dim } from "../draw";
import { CIRCLE } from "../facts";

const { R_CM, ANG, E_TXT, M_TXT } = CIRCLE;
const B = beats([["intro", 2600], ["roll", 8400], ["ruler", 3800], ["back", 2800], ["cut", 2400],
  ["arrange", 6400], ["fix", 1700], ["area", 5200], ["hold", 3000]]);

const GY = 600, X0 = 200, R1 = 112;           // 굴리기: 바닥선·출발점·반지름(px)
const C2 = [330, 372], R2 = 128;              // 자르기: 원 자리
const PX = R1 / R_CM;                         // 1 cm 당 px (굴리기)

/* ── 굴리기: 진행 u(0~1) → 중심·회전 ── */
function rollState(t) {
  const u = Math.max(seg(t, B.a.roll + 400, B.b.roll - 300, E.io) - seg(t, B.a.back, B.a.back + 1700, E.io), 0);
  const ph = u * Math.PI * 2;                 // 굴러간 각(라디안)
  const gone = seg(t, B.a.back + 1500, B.b.back, E.io);
  const c = [lerp(X0 + R1 * ph, C2[0], gone), lerp(GY - R1, C2[1], gone)];
  return { u, ph, c, r: lerp(R1, R2, gone), gone };
}

/** 원 둘레(몸 기준 각 a0→a1, 도)를 세계 좌표 호로 — 몸은 시계 방향으로 ph 만큼 돌았다 */
const bodyArc = (s, a0, a1) => arcPts(s.c, s.r, a0 - (s.ph * 180) / Math.PI, a1 - (s.ph * 180) / Math.PI);

/* ── 쐐기(부채꼴 조각) 재배치 ──
   pieces: 원래 자리 [a0,a1](수학 각, 도) 를 슬롯 순서대로. 짝수 슬롯 = 호가 위, 홀수 = 호가 아래.
   슬롯 0 의 왼쪽 절반은 fix 단계에서 오른쪽 끝으로 옮겨 직사각형을 만든다. */
function placeWedges({ ranges, O, R, Rf, x0, yb, k, fixK, delay = 0, t, tA, span }) {
  const out = [];
  const dA = ranges[0][1] - ranges[0][0];
  const c = 2 * Rf * Math.sin(rad(dA / 2));
  const nUp = Math.ceil(ranges.length / 2);
  ranges.forEach(([a0, a1], s) => {
    const kk = t == null ? k : seg(t, tA + s * delay, tA + s * delay + span, E.io);
    const up = s % 2 === 0, j = Math.floor(s / 2);
    const target = up ? [x0 + j * c, yb] : [x0 + (j + 0.5) * c, yb - Rf * Math.cos(rad(dA / 2))];
    const beta = (a0 + a1) / 2, tb = up ? 90 : -90;
    let rot = tb - beta;
    while (rot > 180) rot -= 360;
    while (rot <= -180) rot += 360;
    const apex = [lerp(O[0], target[0], kk), lerp(O[1], target[1], kk)];
    const rr = lerp(R, Rf, kk), ro = rot * kk;
    if (s === 0) {
      // 왼쪽 절반(각이 큰 쪽)은 fix 때 오른쪽 끝으로
      const mid = (a0 + a1) / 2;
      const shift = fixK * nUp * c;
      out.push({ s, half: "R", pts: [apex, ...arcPts(apex, rr, a0 + ro, mid + ro, 10)] });
      const ap2 = [apex[0] + shift, apex[1]];
      out.push({ s, half: "L", pts: [ap2, ...arcPts(ap2, rr, mid + ro, a1 + ro, 10)] });
    } else out.push({ s, pts: [apex, ...arcPts(apex, rr, a0 + ro, a1 + ro, 10)] });
  });
  return { out, width: nUp * c };
}

/* ══════════ 공통: 굴러가는 원 ══════════ */
function Rolling({ t, C, mode }) {
  const s = rollState(t);
  const o = 1 - seg(t, B.a.back + 1500, B.a.back + 2100);     // 굴리기 원은 자르기 원으로 바뀐다
  const draw = seg(t, 200, 1700, E.out);
  const phD = (s.ph * 180) / Math.PI;
  const laid = R1 * s.ph;                                    // 바닥에 펴진 길이(px)
  const secLen = R1 * rad(ANG);                              // 부채꼴 호(px)
  const lineO = 1 - seg(t, B.a.back + 900, B.a.back + 1500);
  const showSec = mode === "m";
  // 남은 둘레: 세계 각 −90° 에서 반시계로 (270 − phD)° 까지
  const rimEnd = 270 - phD;
  const restSec = Math.max(0, ANG - phD);                    // 아직 원에 붙어 있는 호(중등)
  return (
    <g opacity={o}>
      {/* 바닥선 */}
      <Path pts={[[X0 - 70, GY], [X0 + 2 * Math.PI * R1 + 90, GY]]} stroke={C.faint} sw={3} o={seg(t, 300, 1400)} />
      {/* 원판 */}
      <circle cx={s.c[0]} cy={s.c[1]} r={s.r} fill={C.ink} fillOpacity={0.06} />
      {showSec && <Path pts={[s.c, ...bodyArc(s, -90, -90 + ANG)]} closed fill={C.coral} fo={0.32 * draw} stroke="none" />}
      <Path pts={arcPts(s.c, s.r, 0, 360)} stroke={C.ink} sw={2.2} o={0.35 * draw} />
      {/* 아직 펴지지 않은 둘레 */}
      {!showSec && <Path pts={partial2(arcPts(s.c, s.r, -90, rimEnd), draw)} stroke={C.gold} sw={7} o={lineO} />}
      {showSec && <g opacity={lineO}>
        <Path pts={partial2(arcPts(s.c, s.r, -90 + restSec, rimEnd), draw)} stroke={C.sky} sw={6} o={0.85} />
        {restSec > 0 && <Path pts={arcPts(s.c, s.r, -90, -90 + restSec)} stroke={C.coral} sw={8} o={draw} />}
        <Path pts={[bodyArc(s, -90, -90)[0], s.c, bodyArc(s, -90 + ANG, -90 + ANG)[0]]} stroke={C.coral} sw={3.5} o={draw} />
      </g>}
      {/* 펴진 둘레(바닥) */}
      {laid > 0.5 && (showSec
        ? <g opacity={lineO}>
            <Path pts={[[X0, GY], [X0 + Math.min(laid, secLen), GY]]} stroke={C.coral} sw={8} />
            {laid > secLen && <Path pts={[[X0 + secLen, GY], [X0 + laid, GY]]} stroke={C.sky} sw={6} o={0.85} />}
          </g>
        : <Path pts={[[X0, GY], [X0 + laid, GY]]} stroke={C.gold} sw={7} o={lineO} />)}
      {/* 처음 닿았던 점 · 지름 */}
      <Path pts={[...bodyArc(s, 0, 0), s.c, ...bodyArc(s, 180, 180)]} stroke={C.soft} sw={2.6} dash="10 9" o={draw * (1 - s.gone)} />
      <Dot p={bodyArc(s, -90, -90)[0]} r={8} fill={C.ink} o={draw * lineO} />
      <Dot p={s.c} r={6} fill={C.ink} o={draw} />
      {/* 처음 치수 */}
      <g opacity={seg(t, 1200, 2000) * (1 - seg(t, B.a.roll + 200, B.a.roll + 700))}>
        <Lbl x={s.c[0] + R1 / 2} y={s.c[1] - 24} s={`${2 * R_CM} cm`} size={30} C={C} />
        <Lbl x={s.c[0] - 26} y={s.c[1] + 22} s="O" size={30} C={C} />
      </g>
    </g>
  );
}
const partial2 = (pts, p) => (p >= 1 ? pts : pts.slice(0, Math.max(2, Math.ceil(pts.length * p))));

/* ── 자르기 단계의 원 ── */
function CutCircle({ t, C, cuts, hiRange }) {
  const o = seg(t, B.a.back + 1500, B.a.back + 2100);
  const cutP = seg(t, B.a.cut, B.a.cut + 1500, E.out);
  if (o <= 0) return null;
  return (
    <g opacity={o}>
      <circle cx={C2[0]} cy={C2[1]} r={R2} fill={C.ink} fillOpacity={0.06} stroke={C.ink} strokeOpacity={0.55} strokeWidth={2.6} />
      {hiRange && <Path pts={[C2, ...arcPts(C2, R2, hiRange[0], hiRange[1])]} closed fill={C.coral} fo={0.34} stroke={C.coral} sw={3} />}
      {cuts.map((a, i) => <Path key={i} pts={[C2, polar(C2, R2 * cutP, a)]} stroke={C.ink} sw={1.8} o={0.7} />)}
      <Dot p={C2} r={5} fill={C.ink} />
    </g>
  );
}

/* ══════════ 초등 ══════════ */
const N_E = 16;
function Elem({ t, C }) {
  const s = rollState(t);
  const circ = 2 * Math.PI * R1;
  // 지름 세 번 + 조금
  const rulerK = (i) => seg(t, B.a.ruler + 200 + i * 750, B.a.ruler + 900 + i * 750, E.io);
  const rulerO = 1 - seg(t, B.a.back + 600, B.a.back + 1200);
  // 조각
  const tA = B.a.arrange;
  const d = 360 / N_E;
  const up = Array.from({ length: N_E / 2 }, (_, i) => [i * d, (i + 1) * d]).reverse();   // 위 반원: 왼쪽(180°)부터
  const dn = Array.from({ length: N_E / 2 }, (_, i) => [180 + i * d, 180 + (i + 1) * d]);  // 아래 반원: 180°부터
  const ranges = [];
  for (let j = 0; j < N_E / 2; j++) ranges.push(up[j], dn[j]);
  const fixK = seg(t, B.a.fix + 100, B.b.fix - 100, E.io);
  const RX = 500, RY = 604;
  const W = placeWedges({ ranges, O: C2, R: R2, Rf: R2, x0: RX, yb: RY, t, tA: tA + 200, delay: 260, span: 2300, fixK });
  const colO = seg(t, B.a.cut + 600, B.a.cut + 1800);
  const showW = t >= B.a.cut + 600;
  const labO = seg(t, B.a.area, B.a.area + 700);
  return (
    <g>
      <Rolling t={t} C={C} mode="e" />
      {/* 지름 자 */}
      <g opacity={rulerO}>
        {[0, 1, 2].map((i) => {
          const k = rulerK(i);
          if (k <= 0) return null;
          const from = [s.c[0] - R1, s.c[1]], to = [X0 + i * 2 * R1, GY + 40];
          const a = [lerp(from[0], to[0], k), lerp(from[1], to[1], k)];
          return <g key={i}>
            <Path pts={[a, [a[0] + 2 * R1, a[1]]]} stroke={i % 2 ? C.sky : C.coral} sw={9} />
            {k >= 1 && <Lbl x={a[0] + R1} y={a[1] + 34} s={`${2 * R_CM} cm`} size={28} C={C} />}
          </g>;
        })}
        {rulerK(2) >= 1 && <g opacity={seg(t, B.a.ruler + 2600, B.a.ruler + 3200)}>
          <Path pts={[[X0 + 6 * R1, GY + 40], [X0 + circ, GY + 40]]} stroke={C.leaf} sw={9} />
          <Lbl x={X0 + circ + 16} y={GY + 74} s="조금 더" size={26} fill={C.leaf} C={C} />
        </g>}
        <Lbl x={X0 + circ / 2} y={GY - 32} s={`원주 ${E_TXT.circ} cm`} size={34} fill={C.gold} C={C}
          o={seg(t, B.a.ruler, B.a.ruler + 500)} />
      </g>
      <CutCircle t={t} C={C} cuts={Array.from({ length: N_E }, (_, i) => i * d)} />
      {showW && <g opacity={colO}>
        {W.out.map((w, i) => <Path key={i} pts={w.pts} closed fill={w.s % 2 === 0 ? C.gold : C.sky} fo={0.62}
          stroke={C.ink} sw={1.6} />)}
      </g>}
      {/* 직사각형 표시 */}
      <g opacity={labO}>
        <Path pts={[[RX, RY - R2], [RX + W.width, RY - R2], [RX + W.width, RY], [RX, RY]]} closed stroke={C.ink} sw={2.4} dash="9 8" />
        <Dim A={[RX, RY]} B={[RX + W.width, RY]} off={-30} lofs={-28} s="원주 × {1/2}" C={C} color={C.gold} size={30} />
        <Dim A={[RX + W.width, RY]} B={[RX + W.width, RY - R2]} off={-30} lofs={-58} s="반지름" C={C} color={C.gold} size={30} />
      </g>
      <Board x={1080} y={232} t={t} C={C} lines={[
        { t: B.a.ruler + 300, s: "(원주)", k: "h" },
        { t: B.a.ruler + 600, s: "= (지름) × 3.14" },
        { t: B.a.ruler + 2600, s: E_TXT.circLine },
        { t: B.a.area + 300, s: "(원의 넓이)", k: "h" },
        { t: B.a.area + 600, s: "= (원주) × {1/2} × (반지름)" },
        { t: B.a.area + 1800, s: "= (반지름) × (반지름) × 3.14" },
        { t: B.a.area + 3000, s: E_TXT.areaLine },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 400, s: `반지름이 ${R_CM} cm인 원` },
        { t: B.a.roll + 300, s: "원을 한 바퀴 굴리면 둘레가 쭉 펴져요" },
        { t: B.a.ruler, s: "원주는 지름의 약 3.14배" },
        { t: B.a.back + 800, s: "이번에는 원을 똑같이 잘게 잘라요" },
        { t: B.a.arrange, s: "조각을 번갈아 붙이면 직사각형에 가까워져요" },
        { t: B.a.area, s: "가로는 원주의 {1/2}, 세로는 반지름" },
      ]} />
    </g>
  );
}

/* ══════════ 중등 ══════════ */
const N_M = 8;
function Mid({ t, C }) {
  const circ = 2 * Math.PI * R1, secLen = R1 * rad(ANG);
  const fiveK = seg(t, B.a.ruler + 900, B.a.ruler + 2200, E.out);
  const rulerO = 1 - seg(t, B.a.back + 600, B.a.back + 1200);
  // 부채꼴(몸 기준 −90° ~ −18°)을 8조각으로 — 크게 키워 오른쪽에서 붙인다
  const a0 = -90, d = ANG / N_M;
  const sl = Array.from({ length: N_M }, (_, i) => [a0 + i * d, a0 + (i + 1) * d]);
  const fixK = seg(t, B.a.fix + 100, B.b.fix - 100, E.io);
  const RX = 640, RY = 650, RF = R2 * 1.55;
  const W = placeWedges({ ranges: sl, O: C2, R: R2, Rf: RF, x0: RX, yb: RY, t, tA: B.a.arrange + 200, delay: 330, span: 2600, fixK });
  const showW = t >= B.a.cut + 1200;
  const colO = seg(t, B.a.cut + 1200, B.a.cut + 2000);
  const labO = seg(t, B.a.area, B.a.area + 700);
  const perO = seg(t, B.a.back + 1900, B.a.back + 2500) * (1 - seg(t, B.a.cut + 900, B.a.cut + 1500));
  return (
    <g>
      <Rolling t={t} C={C} mode="m" />
      {/* 원주를 다섯 등분 */}
      <g opacity={rulerO}>
        {[1, 2, 3, 4].map((i) => {
          const x = X0 + (circ * i) / 5;
          return <Path key={i} pts={[[x, GY - 16 * fiveK], [x, GY + 16 * fiveK]]} stroke={C.ink} sw={3} o={fiveK} />;
        })}
        <Lbl x={X0 + secLen / 2} y={GY + 38} s="*l*" size={40} fill={C.coral} C={C} o={seg(t, B.a.ruler, B.a.ruler + 500)} />
        <Lbl x={X0 + circ / 2} y={GY - 32} s={`원주 ${M_TXT.circ} cm`} size={34} fill={C.sky} C={C}
          o={seg(t, B.a.ruler, B.a.ruler + 500)} />
        <Lbl x={X0 + circ * 0.6} y={GY + 40} s="원주의 {1/5}씩" size={28} fill={C.soft} C={C} o={fiveK} />
      </g>
      <CutCircle t={t} C={C} cuts={[0, 1, 2, 3, 4].map((i) => -90 + i * ANG)} hiRange={showW ? null : [-90, -90 + ANG]} />
      {/* 부채꼴의 둘레 = 호 + 반지름 2개 */}
      {perO > 0 && <g opacity={perO}>
        <Path pts={[polar(C2, R2, -90 + ANG), C2, ...arcPts(C2, R2, -90, -90 + ANG)]} closed stroke={C.gold} sw={6} />
        <Lbl x={polar(C2, R2 + 64, -90 + ANG / 2)[0]} y={polar(C2, R2 + 64, -90 + ANG / 2)[1]} s={`${M_TXT.per} (cm)`} size={30} anchor="start" fill={C.gold} C={C} />
      </g>}
      {showW && <g opacity={colO}>
        {W.out.map((w, i) => <Path key={i} pts={w.pts} closed fill={w.s % 2 === 0 ? C.coral : C.lilac} fo={0.6}
          stroke={C.ink} sw={1.5} />)}
      </g>}
      <g opacity={labO}>
        <Path pts={[[RX, RY - RF], [RX + W.width, RY - RF], [RX + W.width, RY], [RX, RY]]} closed stroke={C.ink} sw={2.4} dash="9 8" />
        <Dim A={[RX, RY]} B={[RX + W.width, RY]} off={-30} lofs={-28} s="{1/2}*l*" C={C} color={C.coral} size={30} />
        <Dim A={[RX + W.width, RY]} B={[RX + W.width, RY - RF]} off={-30} lofs={-30} s="*r*" C={C} color={C.coral} size={32} />
      </g>
      <Board x={1080} y={232} t={t} C={C} lines={[
        { t: B.a.ruler + 300, s: "호의 길이", k: "h" },
        { t: B.a.ruler + 600, s: M_TXT.arcLine1 },
        { t: B.a.ruler + 2600, s: M_TXT.arcLine2 },
        { t: B.a.back + 2100, s: M_TXT.perLine },
        { t: B.a.area + 300, s: "부채꼴의 넓이", k: "h" },
        { t: B.a.area + 600, s: M_TXT.areaLine1 },
        { t: B.a.area + 1800, s: "*S* = {1/2}*rl*" },
        { t: B.a.area + 3000, s: M_TXT.areaLine2 },
      ]} />
      <Caption t={t} C={C} caps={[
        { t: 400, s: `반지름이 ${R_CM} cm, 중심각이 ${ANG}°인 부채꼴` },
        { t: B.a.roll + 300, s: "원을 굴리면 부채꼴의 호가 먼저 펴져요" },
        { t: B.a.ruler, s: `호의 길이는 원주의 {${ANG}/360} = {1/5}` },
        { t: B.a.back + 1900, s: "부채꼴의 둘레는 호와 반지름 2개" },
        { t: B.a.cut + 1500, s: "부채꼴의 넓이는?" },
        { t: B.a.arrange, s: "부채꼴을 잘게 잘라 번갈아 붙이면" },
        { t: B.a.area, s: "가로는 호의 길이의 {1/2}, 세로는 반지름" },
      ]} />
    </g>
  );
}

export default {
  key: "circle",
  dur: B.dur,
  title: { e: "원주와 원의 넓이", m: "부채꼴의 둘레와 넓이" },
  sub: { e: "초등 · 원주율 3.14", m: "중등 · 원주율 π" },
  render: (mode, t, C) => (mode === "m" ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />),
};
