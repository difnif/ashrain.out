// 축구 1 — 맨시티 코너킥 → 콤파니 헤더 (2012-04-30 맨체스터 더비 1−0, 전반 추가 시간)
// 위에서 내려다본 코너 쪽 경기장. K 코너킥, H 헤더한 곳, F 는 H 에서 골라인에 내린 수선의 발, T 골문에 들어간 곳.
//   초등: 줄자로 재기 — 26 m · 10 m · 31.5 m → K→F 24 m, F→T = 31.5 − 24 = 7.5 m → 헤더 12.5 m → 26 + 12.5 = 38.5 m
//   중등: 직각삼각형 KFH → KF² + 10² = 26² → KF = 24 → FT = 7.5 → 직각삼각형 HFT → HT = 12.5 m
import { beats, seg, win, E, mix2, fmt } from "../core";
import { Path, RightMark } from "../draw";
import { UBoard, UCaption, Tape, Chip, UDim, SegLbl } from "../kit-story";
import { mapper, Grass, PLines, boxLines, Goal, Player, Rival, Ball, GoalFlash, DirNote } from "../kit-soccer";
import { CORNER, who } from "../facts-soccer";

const { P, GOAL, KH, HF, KT, KF, FT, HT, flight, E: TE, M: TM } = CORNER;
const B = beats([["intro", 2600], ["kick", 3800], ["given", 6200], ["step1", 6400], ["step2", 6000], ["wrap", 4600], ["hold", 2400]]);
const MP = mapper({ ox: 118, oy: 300, s: 18 });
const GR = [-3.2, -4.6, 45.6, 24];                      // 잔디(세계 좌표)
const K = MP.p(P.K), F = MP.p(P.F), H = MP.p(P.H), T = MP.p(P.T), NET = MP.p([P.T[0], -1.4]);
const SILVA = MP.p([-2.1, -2.3]);
// 회색 = 맨유(그날 선발). 콤파니를 놓친 스몰링, 골키퍼 데 헤아 — 나머지 자리는 명단으로 짐작
const RIVALS = [[[35.4, 6.4], "퍼디낸드", "r"], [[39.6, 9.4], "에브라", "r"], [[31.2, 14.2], "존스", "r"], [[26.2, 17.4], "스몰링", "r"]]
  .map(([q, nm, lp]) => ({ p: MP.p(q), id: who("derby2012United", nm), lp }));
const KEEPER = { p: MP.p([34.6, 0.9]), id: who("derby2012United", "데 헤아"), lp: "r" };

// 공: 코너킥(포물선) → 헤더 → 그물
const KA = B.a.kick + 200, KB = KA + 1600, KC = KB + 900, KD = KC + 320;
function ballAt(t) {
  if (t < KA) return { p: K, h: 0 };
  if (t < KB) { const k = seg(t, KA, KB, E.lin); return { p: mix2(K, H, k), h: 1.05 * 4 * k * (1 - k) + 0.35 * k }; }
  if (t < KC) { const k = seg(t, KB, KC, E.lin); return { p: mix2(H, T, k), h: 0.35 * (1 - k) }; }
  const k = seg(t, KC, KD, E.out);
  return { p: mix2(T, NET, k), h: 0 };
}

const lines = [
  [[-3.2, 0], [45.6, 0]],                   // 골라인
  [[0, -4.6], [0, 24]],                     // 터치라인
  ...boxLines(GOAL.c),
];
const cornerArc = (() => { const out = []; for (let i = 0; i <= 12; i++) { const a = (i / 12) * Math.PI / 2; out.push([Math.cos(a), Math.sin(a)]); } return out; })();

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700);
  const playersO = seg(t, 500, 1300);
  const ball = ballAt(t);
  const flash = win(t, KC, B.b.kick + 400, 120, 700);
  const jump = win(t, KB - 260, KB + 260, 200, 260);
  const trail = seg(t, KB, KB + 500) * (isM ? 1 : 0.85);
  // 주어진 것
  const g1 = seg(t, B.a.given + 200, B.a.given + 1200), g2 = seg(t, B.a.given + 1800, B.a.given + 2600), g3 = seg(t, B.a.given + 3000, B.a.given + 4400);
  // 중등 강조 삼각형
  const triA = isM ? seg(t, B.a.step1 + 200, B.a.step1 + 900) : 0;
  const triB = isM ? seg(t, B.a.step2 + 200, B.a.step2 + 900) : 0;
  const fMark = seg(t, B.a.step1 + 200, B.a.step1 + 900);
  const ftHi = seg(t, B.a.step1 + 2400, B.a.step1 + 3000);
  const htTape = seg(t, B.a.step2 + 200, B.a.step2 + 1400);
  const wrapHi = seg(t, B.a.wrap + 200, B.a.wrap + 1000);
  const C2 = C;
  return (
    <g>
      {/* 경기장 */}
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={4} along="x" />
        <Goal M={MP} C={C} cx={GOAL.c} w={GOAL.w} depth={2} dir={-1} />
        <DirNote x={MP.p([GR[0], 0])[0] + 2} y={MP.p([0, GR[3]])[1] + 30} s="위치는 실제 장면을 바탕으로 다듬은 값 · 흐린 선수는 그날 선발, 자리는 짐작" anchor="start" size={18} C={C} />
        <PLines M={MP} C={C} lines={lines} clip={GR} />
        <PLines M={MP} C={C} lines={[cornerArc]} w={2.2} />
        <circle cx={MP.p([GOAL.c, 11])[0]} cy={MP.p([GOAL.c, 11])[1]} r={3} fill={C.name === "light" ? "#fff" : "#e9f1e3"} opacity={0.8} />
        {/* 코너 깃발 */}
        <Path pts={[K, [K[0], K[1] - 30]]} stroke={C.ink} sw={2.4} />
        <path d={`M${K[0]} ${K[1] - 30}L${K[0] + 16} ${K[1] - 24}L${K[0]} ${K[1] - 18}Z`} fill={C.sky} />
      </g>

      {/* 공이 지나간 길 */}
      {trail > 0 && <g opacity={trail}>
        <Path pts={[K, H]} stroke={wrapHi > 0 && !isM ? C.gold : C.ink} sw={isM ? 3.6 : 3} dash={isM ? undefined : "10 9"} o={isM ? 0.9 : 0.7} />
      </g>}
      {t > KC && <Path pts={[H, T]} stroke={wrapHi > 0 && !isM ? C.gold : C.ink} sw={isM ? 3.6 : 3} dash={isM ? undefined : "10 9"} o={(isM ? 0.9 : 0.7) * seg(t, KC, KC + 400)} />}

      {/* 중등: 직각삼각형 */}
      {triA > 0 && <Path pts={[K, F, H]} closed fill={C.gold} fo={0.16 * triA} stroke="none" />}
      {triB > 0 && <Path pts={[H, F, T]} closed fill={C.teal} fo={0.18 * triB} stroke="none" />}
      {/* 수선 HF 와 직각 */}
      {g2 > 0 && <g opacity={g2}>
        <Path pts={[H, F]} stroke={C.ink} sw={2.4} dash="8 7" o={0.85} />
        <RightMark V={F} A={K} B={H} s={16} C={C} color={C.ink} />
      </g>}

      {/* 선수 */}
      {RIVALS.map((q, i) => <Rival key={i} x={q.p[0]} y={q.p[1]} C={C} o={playersO} n={q.id[0]} name={q.id[1]} lp={q.lp} />)}
      <Rival x={KEEPER.p[0]} y={KEEPER.p[1]} C={C} o={playersO} r={15} n={KEEPER.id[0]} name={KEEPER.id[1]} lp={KEEPER.lp} />
      <Player x={SILVA[0]} y={SILVA[1]} n={21} team="city" C={C} o={playersO} label="실바" lp="l" r={20} lsize={22} />
      <Player x={H[0]} y={H[1] + (isM ? 0 : 0)} n={4} team="city" C={C} o={playersO} label="콤파니" lp="b" ring={jump} r={22 + 4 * jump} lsize={22} />
      <Ball x={ball.p[0]} y={ball.p[1]} h={ball.h} C={C} o={playersO} />
      <GoalFlash x={MP.p([GOAL.c, -4])[0] + 90} y={MP.p([GOAL.c, -4])[1] + 30} k={flash} C={C} />

      {/* 점 이름 */}
      {g1 > 0 && <g opacity={g1}>
        <Chip x={K[0] + 26} y={K[1] + 26} s="K" size={22} C={C} fill={C.paper} color={C.ink} stroke={C.ink} />
      </g>}
      {g2 > 0 && <Chip x={F[0] - 22} y={F[1] - 24} s="F" size={22} C={C} o={g2} fill={C.paper} color={C.ink} stroke={C.ink} />}
      {g3 > 0 && <Chip x={T[0] + 22} y={T[1] + 26} s="T" size={22} C={C} o={g3} fill={C.paper} color={C.ink} stroke={C.ink} />}
      {g1 > 0 && <Chip x={H[0] + 40} y={H[1] - 26} s="H" size={22} C={C} o={g1} fill={C.paper} color={C.ink} stroke={C.ink} />}

      {isM ? <Mid t={t} C={C2} g={[g1, g2, g3]} fMark={fMark} triB={triB} /> : <Elem t={t} C={C2} g={[g1, g2, g3]} fMark={fMark} ftHi={ftHi} htTape={htTape} />}
    </g>
  );
}

/* ── 초등: 줄자 ── */
function Elem({ t, C, g, fMark, ftHi, htTape }) {
  const pT = (a, b) => seg(t, a, b, E.io);
  return (
    <g>
      <Tape a={K} b={H} p={pT(B.a.given + 200, B.a.given + 1200)} pxPerM={MP.s} C={C} read={TE.tapeKH} side={1} />
      <Tape a={H} b={F} p={pT(B.a.given + 1800, B.a.given + 2600)} pxPerM={MP.s} C={C} read={TE.tapeHF} side={-1} rs={24} />
      <Tape a={K} b={T} p={pT(B.a.given + 3000, B.a.given + 4400)} pxPerM={MP.s} C={C} read={TE.tapeKT} side={1} />
      {fMark > 0 && <g opacity={fMark}>
        <Path pts={[[F[0], F[1] - 12], [F[0], F[1] + 12]]} stroke={C.coral} sw={4} />
        <Chip x={F[0] - 8} y={F[1] - 58} s={`F까지 ${TE.tapeKF}`} size={22} C={C} anchor="end" fill={C.coral} color={C.paper} />
      </g>}
      {ftHi > 0 && <g opacity={ftHi}>
        <Path pts={[F, T]} stroke={C.gold} sw={9} o={0.75} />
        <Chip x={(F[0] + T[0]) / 2 + 26} y={F[1] - 58} s={`${fmt(FT)} m`} size={22} C={C} fill={C.gold} color={C.paper} />
      </g>}
      <Tape a={H} b={T} p={htTape} pxPerM={MP.s} C={C} read={TE.tapeHT} side={-1} />
      <UBoard x={990} y={232} t={t} C={C} size={32} lh={56} lines={[
        { t: B.a.given + 1200, s: TE.kh },
        { t: B.a.given + 2600, s: TE.hf },
        { t: B.a.given + 4400, s: TE.kt },
        { t: B.a.step1 + 900, s: TE.kf },
        { t: B.a.step1 + 2600, s: TE.ft },
        { t: B.a.step2 + 1400, s: TE.ht },
        { t: B.a.wrap + 300, s: TE.sum },
      ]} />
      <UCaption t={t} C={C} caps={caps("e")} />
    </g>
  );
}

/* ── 중등: 피타고라스 정리 ── */
function Mid({ t, C, g, fMark, triB }) {
  const [g1, g2, g3] = g;
  const kfO = seg(t, B.a.step1 + 3800, B.a.step1 + 4400);
  const ftO = seg(t, B.a.step1 + 4600, B.a.step1 + 5200);
  const htO = seg(t, B.a.step2 + 2800, B.a.step2 + 3400);
  return (
    <g>
      <SegLbl P={K} Q={H} s={`${TM.lab.KH} m`} side={1} off={26} C={C} o={g1} size={28} />
      <SegLbl P={H} Q={F} s={`${TM.lab.HF} m`} side={-1} off={34} C={C} o={g2} size={28} />
      <UDim A={K} B={T} off={64} s={TM.lab.KT} C={C} o={g3} size={26} lofs={22} />
      <SegLbl P={K} Q={F} s={TM.lab.KF} side={-1} off={18} C={C} o={kfO} size={28} fill={C.gold} />
      <SegLbl P={F} Q={T} s={TM.lab.FT} side={-1} off={18} C={C} o={ftO} size={28} fill={C.teal} />
      <SegLbl P={H} Q={T} s={`${TM.lab.HT} m`} side={1} off={44} C={C} o={htO} size={30} fill={C.teal} />
      <UBoard x={990} y={232} t={t} C={C} size={32} lh={56} lines={[
        { t: B.a.given + 1200, s: `KH = ${fmt(KH)} m,  HF = ${fmt(HF)} m` },
        { t: B.a.given + 4400, s: `골라인을 따라 KT = ${fmt(KT)} m` },
        { t: B.a.step1 + 900, s: "직각삼각형 KFH", k: "h" },
        { t: B.a.step1 + 1300, s: TM.eq1 },
        { t: B.a.step1 + 2800, s: TM.kf2 },
        { t: B.a.step1 + 4400, s: TM.kf },
        { t: B.a.step2 + 900, s: TM.eq2 },
        { t: B.a.step2 + 2800, s: TM.ht },
        { t: B.a.wrap + 300, s: TM.ratio, size: 28 },
      ]} />
      <UCaption t={t} C={C} caps={caps("m")} />
    </g>
  );
}

function caps(mode) {
  const head = [
    { t: 300, s: "2012년 4월 30일 맨체스터 더비 — 맨시티 1−0 맨유" },
    { t: B.a.kick, s: "전반 추가 시간, 실바의 코너킥을 콤파니가 헤더로 넣었어요" },
  ];
  return mode === "m" ? [...head,
    { t: B.a.given, s: `코너킥은 ${fmt(KH)} m, 헤더한 곳 H는 골라인에서 ${fmt(HF)} m` },
    { t: B.a.given + 3000, s: `골문에 들어간 T는 K에서 골라인을 따라 ${fmt(KT)} m` },
    { t: B.a.step1, s: "H에서 골라인에 수선을 내리면 직각삼각형 KFH" },
    { t: B.a.step2, s: "직각삼각형 HFT에서 한 번 더 피타고라스 정리" },
    { t: B.a.wrap, s: `헤더로 공이 날아간 거리는 ${fmt(HT)} m` },
  ] : [...head,
    { t: B.a.given, s: "공이 날아간 길을 줄자로 재 보아요" },
    { t: B.a.given + 3000, s: "골라인을 따라서도 재요 — 코너에서 골문까지" },
    { t: B.a.step1, s: `K에서 F까지 ${fmt(KF)} m — 그럼 F에서 T까지는?` },
    { t: B.a.step2, s: `헤더로 날아간 H → T를 재면 ${fmt(HT)} m` },
    { t: B.a.wrap, s: `공은 모두 ${fmt(flight)} m를 날아 골문에 들어갔어요` },
  ];
}

export default {
  key: "soc-corner",
  dur: B.dur,
  title: { e: "코너킥과 헤더 — 줄자로 재기", m: "코너킥과 헤더 — 피타고라스 정리" },
  sub: { e: "초등 · 길이 재기와 뺄셈 · 2012 맨체스터 더비", m: "중2 · 피타고라스 정리 · 2012 맨체스터 더비" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
