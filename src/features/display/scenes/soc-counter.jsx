// 축구 5 — 박지성 · 루니 · 호날두 역습 (2009-05-05 챔피언스리그 준결승 2차전 아스널 1−3 맨유, 61분)
// 박지성이 공을 받은 곳 O, 루니가 패스한 곳 R(48, 36), 호날두가 슈팅한 곳 C(63, 16). 공 O → R → C, 호날두 O → C.
//   초등: 줄자 60 · 25 · 65 m → 공 85 m, 호날두 65 m → 20 m 더 / 오각형 = 직사각형 63 × 36 − 삼각형 15 × 20 ÷ 2 = 2118 m²
//   중등: R, C 는 직선의 교점 → OR² = 48² + 36², RC² = 15² + 20², OC² = 63² + 16² → 20 m / 오각형 2118 m²
import { beats, seg, win, E, mix2, fmt } from "../core";
import { Path, RightMark } from "../draw";
import { UText, UBoard, UCaption, Tape, Chip, SegLbl } from "../kit-story";
import { mapper, Grass, Player, Ball, GoalFlash, DirNote } from "../kit-soccer";
import { COUNTER as CT } from "../facts-soccer";

const B = beats([["intro", 2400], ["play", 6600], ["len", 7200], ["diff", 6000], ["area", 7800], ["hold", 2400]]);
const MP = mapper({ ox: 116, oy: 712, s: 11, flipY: true });
const GR = [-4, -5, 74, 42];
const O = MP.p(CT.O), R = MP.p(CT.R), Cc = MP.p(CT.C), Hh = MP.p(CT.H), K = MP.p(CT.K), T = MP.p(CT.T);
const RON0 = MP.p([1.4, -2.4]);                          // 호날두 출발(박지성 바로 옆)
const GOALPT = MP.p([74, 12]);

// 경기 흐름(그림 시각)
const P = B.a.play;
const T_RUN = [P + 300, P + 3900], T_P1 = [P + 600, P + 2400], T_P2 = [P + 2700, P + 3900], T_SHOT = [P + 4200, P + 4700];
function playAt(t) {
  const ron = t < T_RUN[0] ? RON0 : t < T_RUN[1] ? mix2(RON0, Cc, (t - T_RUN[0]) / (T_RUN[1] - T_RUN[0])) : Cc;
  let ball;
  if (t < T_P1[0]) ball = O;
  else if (t < T_P1[1]) ball = mix2(O, R, seg(t, T_P1[0], T_P1[1], E.lin));
  else if (t < T_P2[0]) ball = R;
  else if (t < T_P2[1]) ball = mix2(R, Cc, seg(t, T_P2[0], T_P2[1], E.lin));
  else if (t < T_SHOT[0]) ball = Cc;
  else ball = mix2(Cc, GOALPT, seg(t, T_SHOT[0], T_SHOT[1], E.out));
  return { ron, ball };
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700), playersO = seg(t, 400, 1200);
  const pl = playAt(t);
  const flash = win(t, T_SHOT[1] - 100, B.b.play + 200, 120, 500);
  const trailOR = seg(t, T_P1[0], T_P1[1]), trailRC = seg(t, T_P2[0], T_P2[1]), trailRun = seg(t, T_RUN[0], T_RUN[1]);
  const areaO = seg(t, B.a.area + 200, B.a.area + 900);
  const triO = seg(t, B.a.area + 2200, B.a.area + 2900);
  const pentO = seg(t, B.a.area + 4200, B.a.area + 5000);
  // 경기가 끝나면 공은 슈팅한 곳에 둔다
  const ball = t > B.b.play ? Cc : pl.ball;
  const ballO = t > B.b.play ? 0 : playersO;
  return (
    <g>
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={6} along="x" />
        <DirNote x={MP.p([73, 39.6])[0]} y={MP.p([73, 39.6])[1]} s="상대 골대 쪽 →" anchor="end" C={C} />
        <DirNote x={MP.p([-3, 39.6])[0]} y={MP.p([-3, 39.6])[1]} s="위치는 실제 장면을 바탕으로 다듬은 값" anchor="start" size={18} C={C} />
      </g>
      {/* 오각형 · 직사각형 · 삼각형 */}
      {pentO > 0 && <Path pts={[O, Hh, Cc, R, K]} closed fill={C.teal} fo={0.3 * pentO} stroke={C.teal} sw={3.4} o={pentO} />}
      {areaO > 0 && <g opacity={areaO * (1 - 0.55 * pentO)}>
        <Path pts={[O, Hh, T, K]} closed stroke={C.gold} sw={3} dash="12 8" fill={C.gold} fo={0.08} />
        <UDimLike a={K} b={T} s={CT.E.lab.w} off={-26} C={C} />
        <UDimLike a={O} b={K} s={CT.E.lab.h} off={-34} C={C} vertical />
      </g>}
      {triO > 0 && <g opacity={triO}>
        <Path pts={[Cc, T, R]} closed fill={C.coral} fo={0.32} stroke={C.coral} sw={2.6} />
        <SegLbl P={R} Q={T} s={CT.E.lab.tw} side={-1} off={18} C={C} size={24} fill={C.coral} />
        <SegLbl P={T} Q={Cc} s={CT.E.lab.th} side={-1} off={18} C={C} size={24} fill={C.coral} />
      </g>}
      {/* 길 */}
      <Path pts={[O, mix2(O, R, trailOR)]} stroke={C.red} sw={3.6} o={trailOR > 0 ? 0.85 : 0} />
      <Path pts={[R, mix2(R, Cc, trailRC)]} stroke={C.red} sw={3.6} o={trailRC > 0 ? 0.85 : 0} />
      <Path pts={[O, mix2(O, Cc, trailRun)]} stroke={C.ink} sw={2.6} dash="9 9" o={trailRun > 0 ? 0.7 : 0} />
      {isM ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />}
      {/* 점 이름 */}
      {areaO > 0 && <g opacity={areaO}>
        <Chip x={Hh[0] + 4} y={Hh[1] + 30} s="H" size={20} C={C} fill={C.paper} color={C.ink} stroke={C.ink} />
        <Chip x={K[0] - 30} y={K[1]} s="K" size={20} C={C} fill={C.paper} color={C.ink} stroke={C.ink} />
        <Chip x={T[0] + 28} y={T[1] - 6} s="T" size={20} C={C} fill={C.paper} color={C.ink} stroke={C.ink} />
      </g>}
      {/* 선수 */}
      <Player x={O[0]} y={O[1]} n={13} team="united" C={C} o={playersO} r={19} label="박지성" lp="b" lsize={20} />
      <Player x={R[0]} y={R[1]} n={10} team="united" C={C} o={playersO} r={19} label="루니" lp="l" lsize={20} ring={win(t, T_P1[1] - 150, T_P1[1] + 350, 120, 300)} />
      <Player x={pl.ron[0]} y={pl.ron[1]} n={7} team="united" C={C} o={playersO} r={19} label="호날두" lp="r" lsize={20} ring={win(t, T_P2[1] - 150, T_P2[1] + 350, 120, 300)} />
      <Ball x={ball[0] + 10} y={ball[1] + 10} r={8} C={C} o={ballO} />
      <GoalFlash x={GOALPT[0] - 40} y={GOALPT[1] - 30} k={flash} C={C} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "2009년 5월 5일 챔피언스리그 준결승 2차전 — 아스널 1−3 맨유" },
        { t: B.a.play, s: "61분, 호날두 → 박지성 → 루니 → 호날두로 이어진 역습" },
        { t: B.a.play + 3600, s: "공은 박지성과 루니를 거쳐 가고, 호날두는 곧장 달려요" },
        ...(isM ? [
          { t: B.a.len, s: "R과 C는 두 직선의 교점 — 연립방정식으로 찾아요" },
          { t: B.a.diff, s: "세 거리 모두 피타고라스 정리로 — 3 : 4 : 5가 두 번" },
          { t: B.a.area, s: "오각형 OHCRK = 직사각형 OHTK − 직각삼각형 CTR" },
        ] : [
          { t: B.a.len, s: "공이 간 길과 호날두가 달린 길을 줄자로 재요" },
          { t: B.a.diff, s: `공은 ${fmt(CT.ball)} m, 호날두는 ${fmt(CT.OC)} m — 공이 ${fmt(CT.more)} m 더 움직였어요` },
          { t: B.a.area, s: "역습이 만든 오각형 — 직사각형에서 삼각형을 빼요" },
        ]),
        { t: B.a.area + 5200, s: "공이 더 먼 길을 돌아도 패스가 달리기보다 빨라 골이 되었어요" },
      ]} />
    </g>
  );
}

/** 간단한 치수 글자(직사각형 바깥) */
function UDimLike({ a, b, s, off, C, vertical }) {
  const m = mix2(a, b, 0.5);
  return vertical
    ? <Chip x={m[0] + off} y={m[1]} s={s} size={20} C={C} fill={C.gold} color={C.paper} />
    : <Chip x={m[0]} y={m[1] + off} s={s} size={20} C={C} fill={C.gold} color={C.paper} />;
}

/* ── 초등 ── */
function Elem({ t, C }) {
  const p1 = seg(t, B.a.len + 300, B.a.len + 1500, E.io), p2 = seg(t, B.a.len + 2000, B.a.len + 2900, E.io), p3 = seg(t, B.a.len + 3600, B.a.len + 4900, E.io);
  const bars = seg(t, B.a.diff + 300, B.a.diff + 1100);
  return (
    <g>
      <Tape a={O} b={R} p={p1} pxPerM={MP.s} C={C} read={CT.E.tape.or} side={1} rs={22} w={11} />
      <Tape a={R} b={Cc} p={p2} pxPerM={MP.s} C={C} read={CT.E.tape.rc} side={1} rs={22} w={11} />
      <Tape a={O} b={Cc} p={p3} pxPerM={MP.s} C={C} read={CT.E.tape.oc} side={-1} rs={22} w={11} />
      {bars > 0 && <Bars t={t} C={C} o={bars} />}
      <UBoard x={990} y={232} t={t} C={C} size={28} lh={52} lines={[
        { t: B.a.len + 1500, s: CT.E.or },
        { t: B.a.len + 2900, s: CT.E.rc },
        { t: B.a.len + 4900, s: CT.E.oc },
        { t: B.a.diff + 1200, s: CT.E.ball },
        { t: B.a.diff + 2800, s: CT.E.more },
        { t: B.a.area + 1000, s: CT.E.rect },
        { t: B.a.area + 2900, s: CT.E.tri },
        { t: B.a.area + 5000, s: CT.E.penta },
      ]} />
    </g>
  );
}
/** 공 85 m · 호날두 65 m 막대 */
function Bars({ t, C, o }) {
  const x = 1000, y = 700, s = 5.2;
  const g1 = seg(t, B.a.diff + 300, B.a.diff + 1400), g2 = seg(t, B.a.diff + 900, B.a.diff + 2000);
  const extra = seg(t, B.a.diff + 2400, B.a.diff + 3000);
  return (
    <g opacity={o * (1 - seg(t, B.a.area, B.a.area + 500))}>
      <UText x={x} y={y - 12} s="공" size={22} weight={700} anchor="end" fill={C.soft} C={C} />
      <rect x={x + 10} y={y - 30} width={CT.OR * s * g1} height={22} rx={5} fill={C.red} fillOpacity={0.7} />
      <rect x={x + 10 + CT.OR * s * g1} y={y - 30} width={CT.RC * s * g1} height={22} rx={5} fill={C.coral} fillOpacity={0.7} />
      <UText x={x} y={y + 30} s="호날두" size={22} weight={700} anchor="end" fill={C.soft} C={C} />
      <rect x={x + 10} y={y + 12} width={CT.OC * s * g2} height={22} rx={5} fill={C.ink} fillOpacity={0.45} />
      {extra > 0 && <g opacity={extra}>
        <Path pts={[[x + 10 + CT.OC * s, y + 42], [x + 10 + CT.OC * s, y - 38]]} stroke={C.gold} sw={2.4} dash="5 5" />
        <Chip x={x + 10 + (CT.OC + CT.more / 2) * s} y={y + 22} s={`${fmt(CT.more)} m`} size={20} C={C} fill={C.gold} color={C.paper} />
      </g>}
    </g>
  );
}

/* ── 중등 ── */
function Mid({ t, C }) {
  const l1 = seg(t, B.a.len + 300, B.a.len + 1100), l2 = seg(t, B.a.len + 900, B.a.len + 1700), l3 = seg(t, B.a.len + 1500, B.a.len + 2300);
  const chipO = 1 - seg(t, B.a.diff, B.a.diff + 500);         // 직선의 식은 교점을 찾는 동안만
  const lg = (k) => seg(t, B.a.diff + 300 + k * 1300, B.a.diff + 900 + k * 1300);
  const F48 = MP.p([CT.R[0], 0]);
  const ln = (x0, x1, f) => [MP.p([x0, f(x0)]), MP.p([x1, f(x1)])];
  return (
    <g>
      {l1 > 0 && <g opacity={l1}><Path pts={ln(0, 54, (x) => (3 / 4) * x)} stroke={C.ink} sw={1.8} o={0.5} />
        <Chip x={MP.p([22, 22.6])[0]} y={MP.p([22, 22.6])[1]} s={CT.M.lines.or} size={20} C={C} o={chipO} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      {l2 > 0 && <g opacity={l2}><Path pts={ln(44.5, 70, (x) => -(4 / 3) * x + 100)} stroke={C.ink} sw={1.8} o={0.5} />
        <Chip x={MP.p([62.5, 30.4])[0]} y={MP.p([62.5, 30.4])[1]} s={CT.M.lines.rc} size={20} C={C} o={chipO} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      {l3 > 0 && <g opacity={l3}><Path pts={ln(0, 72, (x) => (16 / 63) * x)} stroke={C.ink} sw={1.8} o={0.5} />
        <Chip x={MP.p([38, 6.2])[0]} y={MP.p([38, 6.2])[1]} s={CT.M.lines.oc} size={20} C={C} o={chipO} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      <Chip x={R[0]} y={R[1] - 40} s={CT.M.labR} size={20} C={C} o={seg(t, B.a.len + 2600, B.a.len + 3100)} fill={C.paper} color={C.ink} stroke={C.ink} />
      <Chip x={Cc[0] + 70} y={Cc[1] - 40} s={CT.M.labC} size={20} C={C} o={seg(t, B.a.len + 4400, B.a.len + 4900)} fill={C.paper} color={C.ink} stroke={C.ink} />
      {/* 다리: OR (48, 36) · RC (15, 20) · OC (63, 16) */}
      {lg(0) > 0 && <g opacity={lg(0) * (1 - seg(t, B.a.area, B.a.area + 500))}>
        <Path pts={[O, F48, R]} stroke={C.gold} sw={2.4} dash="8 7" />
        <RightMark V={F48} A={O} B={R} s={12} C={C} color={C.gold} />
        <SegLbl P={O} Q={F48} s="48" side={-1} off={16} C={C} size={22} fill={C.gold} />
        <SegLbl P={F48} Q={R} s="36" side={-1} off={18} C={C} size={22} fill={C.gold} />
      </g>}
      {lg(1) > 0 && <g opacity={lg(1) * (1 - seg(t, B.a.area, B.a.area + 500))}>
        <Path pts={[R, T, Cc]} stroke={C.coral} sw={2.4} dash="8 7" />
        <RightMark V={T} A={R} B={Cc} s={12} C={C} color={C.coral} />
        <SegLbl P={R} Q={T} s="15" side={-1} off={16} C={C} size={22} fill={C.coral} />
        <SegLbl P={T} Q={Cc} s="20" side={-1} off={18} C={C} size={22} fill={C.coral} />
      </g>}
      {lg(2) > 0 && <g opacity={lg(2) * (1 - seg(t, B.a.area, B.a.area + 500))}>
        <Path pts={[O, Hh, Cc]} stroke={C.teal} sw={2.4} dash="8 7" />
        <RightMark V={Hh} A={O} B={Cc} s={12} C={C} color={C.teal} />
        <SegLbl P={Hh} Q={Cc} s="16" side={1} off={18} C={C} size={22} fill={C.teal} />
        <SegLbl P={O} Q={Hh} s="63" side={1} off={18} C={C} size={22} fill={C.teal} at={0.78} />
      </g>}
      <UBoard x={990} y={232} t={t} C={C} size={27} lh={52} lines={[
        { t: B.a.len + 3100, s: CT.M.r },
        { t: B.a.len + 4900, s: CT.M.c },
        { t: B.a.diff + 900, s: CT.M.or },
        { t: B.a.diff + 2200, s: CT.M.rc, size: 24 },
        { t: B.a.diff + 3900, s: CT.M.more },
        { t: B.a.area + 5000, s: CT.M.penta, size: 24 },
      ]} />
    </g>
  );
}

export default {
  key: "soc-counter",
  dur: B.dur,
  title: { e: "역습이 만든 오각형", m: "역습이 만든 오각형 — 교점과 피타고라스" },
  sub: { e: "초등 · 길이의 합과 차 · 넓이 · 2009 아스널 1−3 맨유", m: "중2 · 교점 · 피타고라스 정리 · 넓이 · 2009 아스널 1−3 맨유" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
