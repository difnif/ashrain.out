// 축구 4 — 맨유 삼각패스: 패스 삼각형의 넓이
// 터치라인이 x축, 하프라인이 y축(단위 m). A(3, 2) → B(12, 14) → C(28, 2) → A 로 공을 돌린다.
//   초등: 모눈에서 가로 25 m · 세로 12 m 읽기 → 직사각형 300에서 두 삼각형 54 · 96 빼기 → 150 m² (밑변 × 높이 ÷ 2 로 확인)
//   중등: C(28, 2) 대입 b = 23 → A(3, 2) · B(12, 14)(교점) → 밑변 25 · 높이 14 − 2 = 12 → 150 m² (높이 14 ✗)
import { beats, seg, win, E, mix2 } from "../core";
import { Path, RightMark } from "../draw";
import { UText, UBoard, UCaption, Chip, SegLbl } from "../kit-story";
import { mapper, Grass, Player, Ball, DirNote } from "../kit-soccer";
import { TRIANGLE as TR } from "../facts-soccer";

const B = beats([["intro", 2400], ["pass", 5200], ["read", 7600], ["area1", 7000], ["area2", 5800], ["hold", 2400]]);
const MP = mapper({ ox: 128, oy: 690, s: 24, flipY: true });
const GR = [-2, -2.5, 33, 19.5];
const A = MP.p(TR.A), Bp = MP.p(TR.B), Cp = MP.p(TR.C);
const R1 = MP.p([TR.A[0], TR.B[1]]), R2 = MP.p([TR.C[0], TR.B[1]]), FOOT = MP.p([TR.B[0], TR.C[1]]);

const P0 = B.a.pass + 300, LEG = 1400;
function ballAt(t) {
  const k = (t - P0) / LEG;
  if (k <= 0) return A;
  if (k < 1) return mix2(A, Bp, E.io(k));
  if (k < 2) return mix2(Bp, Cp, E.io(k - 1));
  if (k < 3) return mix2(Cp, A, E.io(k - 2));
  return A;
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const pitchO = seg(t, 0, 700), playersO = seg(t, 400, 1200);
  const ball = ballAt(t);
  const tr = (i) => seg(t, P0 + i * LEG + LEG * 0.2, P0 + (i + 1) * LEG);
  const gridO = seg(t, B.a.read, B.a.read + 700);
  const triFill = seg(t, B.a.area2 + 200, B.a.area2 + 900);
  const hold = (k) => (k === 0 ? A : k === 1 ? Bp : Cp);
  const ring = (k) => {
    const at = [P0 + 3 * LEG, P0 + LEG, P0 + 2 * LEG][k];
    return win(t, at - 200, at + 300, 150, 250);
  };
  return (
    <g>
      <g opacity={pitchO}>
        <Grass M={MP} rect={GR} C={C} band={5} along="x" />
        <Path pts={[MP.p([-2, 0]), MP.p([33, 0])]} stroke={C.name === "light" ? "#fff" : "#e9f1e3"} sw={3} o={0.8} />
        <Path pts={[MP.p([0, -2.5]), MP.p([0, 19.5])]} stroke={C.name === "light" ? "#fff" : "#e9f1e3"} sw={3} o={0.8} />
        <DirNote x={MP.p([16, -1.6])[0]} y={MP.p([16, -1.6])[1] + 8} s="터치라인" anchor="middle" C={C} o={1 - seg(t, B.a.read - 600, B.a.read)} />
        <DirNote x={MP.p([-1.2, 17.6])[0]} y={MP.p([-1.2, 17.6])[1]} s="하프라인" anchor="end" C={C} o={1 - seg(t, B.a.read - 600, B.a.read)} />
      </g>
      {/* 모눈 · 눈금 */}
      {gridO > 0 && <Grid C={C} o={gridO} isM={isM} />}
      {/* 패스 길 */}
      {[0, 1, 2].map((i) => {
        const [p, q] = [[A, Bp], [Bp, Cp], [Cp, A]][i];
        const k = tr(i);
        return k > 0 && <Path key={i} pts={[p, mix2(p, q, k)]} stroke={C.red} sw={4} o={0.85} />;
      })}
      {triFill > 0 && <Path pts={[A, Bp, Cp]} closed fill={C.teal} fo={0.28 * triFill} stroke={C.teal} sw={4} o={triFill} />}
      {isM ? <Mid t={t} C={C} /> : <Elem t={t} C={C} />}
      {/* 선수 */}
      {["A", "B", "C"].map((n, k) => {
        const q = hold(k);
        return <Player key={n} x={q[0]} y={q[1]} n={n} team="united" C={C} o={playersO} r={22} ring={ring(k)} />;
      })}
      <Ball x={ball[0] + 16} y={ball[1] + 14} r={9} C={C} o={playersO} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: "맨유 세 선수가 삼각형을 만들어 공을 돌려요" },
        { t: B.a.pass, s: "A → B → C → A, 삼각패스 한 바퀴" },
        { t: B.a.pass + 2800, s: isM ? "터치라인이 x축, 하프라인이 y축 (단위 m)" : "터치라인과 하프라인에서 잰 거리로 자리를 나타내요" },
        ...(isM ? [
          { t: B.a.read, s: "세 패스가 지나간 직선 — 식을 세워 꼭짓점을 찾아요" },
          { t: B.a.area1, s: `밑변 AC는 직선 y = ${TR.C[1]} 위 — 높이는 ${TR.B[1]} − ${TR.C[1]}` },
          { t: B.a.area2, s: `패스 삼각형의 넓이는 ${TR.area} m²` },
        ] : [
          { t: B.a.read, s: "모눈의 눈금으로 가로와 세로 길이를 읽어요" },
          { t: B.a.area1, s: "삼각형을 둘러싼 직사각형에서 남는 두 삼각형을 빼요" },
          { t: B.a.area2, s: `패스 삼각형의 넓이는 ${TR.area} m²` },
        ]),
        { t: B.a.area2 + 2800, s: "삼각형이 넓을수록 상대가 공을 빼앗기 어려워요" },
      ]} />
    </g>
  );
}

/** 모눈(1 m) · 5 m 굵은 선 · 눈금 수 */
function Grid({ C, o, isM }) {
  const out = [];
  for (let x = 1; x <= 32; x++) out.push(<Path key={"x" + x} pts={[MP.p([x, -0.0]), MP.p([x, 19])]} stroke={C.ink} sw={x % 5 ? 0.8 : 1.6} o={x % 5 ? 0.1 : 0.22} />);
  for (let y = 1; y <= 19; y++) out.push(<Path key={"y" + y} pts={[MP.p([0, y]), MP.p([32.5, y])]} stroke={C.ink} sw={y % 5 ? 0.8 : 1.6} o={y % 5 ? 0.1 : 0.22} />);
  const nums = [];
  for (let x = 0; x <= 30; x += 5) { const q = MP.p([x, 0]); nums.push(<UText key={"nx" + x} x={q[0]} y={q[1] + 30} s={String(x)} size={20} weight={650} anchor="middle" fill={C.soft} C={C} />); }
  for (let y = 5; y <= 15; y += 5) { const q = MP.p([0, y]); nums.push(<UText key={"ny" + y} x={q[0] - 10} y={q[1] + 7} s={String(y)} size={20} weight={650} anchor="end" fill={C.soft} C={C} />); }
  return (
    <g opacity={o}>
      {out}
      {nums}
      {isM && <g>
        <UText x={MP.p([32.8, 0])[0] + 6} y={MP.p([32.8, 0])[1] + 9} s="x" size={28} C={C} />
        <UText x={MP.p([0, 19.2])[0] + 10} y={MP.p([0, 19.2])[1] + 6} s="y" size={28} C={C} />
      </g>}
    </g>
  );
}

/* ── 초등: 직사각형에서 빼기 ── */
function Elem({ t, C }) {
  const dropA = seg(t, B.a.read + 600, B.a.read + 1300), dropC = seg(t, B.a.read + 1600, B.a.read + 2300), dropB = seg(t, B.a.read + 3600, B.a.read + 4300);
  const rect = seg(t, B.a.area1 + 200, B.a.area1 + 900);
  const lt = seg(t, B.a.area1 + 2000, B.a.area1 + 2700), rt = seg(t, B.a.area1 + 3600, B.a.area1 + 4300);
  const cut = seg(t, B.a.area2 + 200, B.a.area2 + 900);
  const ax = MP.p([TR.A[0], -0.9]), cx = MP.p([TR.C[0], -0.9]);
  return (
    <g>
      {/* 가로: A와 C의 눈금 */}
      {dropA > 0 && <Path pts={[A, MP.p([TR.A[0], 0])]} stroke={C.gold} sw={2.6} dash="6 6" o={dropA} />}
      {dropC > 0 && <Path pts={[Cp, MP.p([TR.C[0], 0])]} stroke={C.gold} sw={2.6} dash="6 6" o={dropC} />}
      {dropC > 0 && <g opacity={dropC}>
        <Path pts={[ax, cx]} stroke={C.gold} sw={3} />
        <Chip x={(ax[0] + cx[0]) / 2} y={ax[1] + 4} s={TR.E.lab.w} size={22} C={C} fill={C.gold} color={C.paper} />
      </g>}
      {/* 세로: B의 높이와 직선 y = 2 */}
      {dropB > 0 && <g opacity={dropB}>
        <Path pts={[MP.p([TR.C[0] + 1.6, TR.C[1]]), MP.p([TR.C[0] + 1.6, TR.B[1]])]} stroke={C.gold} sw={3} />
        <Path pts={[Bp, MP.p([TR.C[0] + 1.6, TR.B[1]])]} stroke={C.gold} sw={2.2} dash="6 6" />
        <Chip x={MP.p([TR.C[0] + 1.6, 8])[0] + 30} y={MP.p([TR.C[0] + 1.6, 8])[1]} s={TR.E.lab.h} size={22} C={C} fill={C.gold} color={C.paper} />
      </g>}
      {/* 둘러싼 직사각형과 두 삼각형 */}
      {rect > 0 && <Path pts={[A, R1, R2, Cp]} closed stroke={C.gold} sw={3.2} dash="12 8" fill={C.gold} fo={0.08} o={rect * (1 - 0.6 * cut)} />}
      {lt > 0 && <g opacity={lt * (1 - 0.75 * cut)}>
        <Path pts={[A, R1, Bp]} closed fill={C.coral} fo={0.3} stroke={C.coral} sw={2.4} />
        <UText x={(A[0] + R1[0] + Bp[0]) / 3 - 6} y={(A[1] + R1[1] + Bp[1]) / 3 + 10} s={TR.E.lab.left} size={28} weight={800} anchor="middle" fill={C.coral} halo={C.halo} C={C} />
      </g>}
      {rt > 0 && <g opacity={rt * (1 - 0.75 * cut)}>
        <Path pts={[Bp, R2, Cp]} closed fill={C.coral} fo={0.3} stroke={C.coral} sw={2.4} />
        <UText x={(Bp[0] + R2[0] + Cp[0]) / 3 + 6} y={(Bp[1] + R2[1] + Cp[1]) / 3 + 10} s={TR.E.lab.right} size={28} weight={800} anchor="middle" fill={C.coral} halo={C.halo} C={C} />
      </g>}
      <UBoard x={990} y={232} t={t} C={C} size={30} lh={56} lines={[
        { t: B.a.read + 2300, s: TR.E.w },
        { t: B.a.read + 4300, s: TR.E.h },
        { t: B.a.area1 + 900, s: TR.E.rect },
        { t: B.a.area1 + 2700, s: TR.E.left },
        { t: B.a.area1 + 4300, s: TR.E.right },
        { t: B.a.area2 + 600, s: TR.E.area },
        { t: B.a.area2 + 2200, s: TR.E.check, size: 26 },
      ]} />
    </g>
  );
}

/* ── 중등: 직선의 식과 교점 ── */
function Mid({ t, C }) {
  const l1 = seg(t, B.a.read + 300, B.a.read + 1100), l2 = seg(t, B.a.read + 900, B.a.read + 1700), l3 = seg(t, B.a.read + 1500, B.a.read + 2300);
  const base = seg(t, B.a.area1 + 200, B.a.area1 + 900), hgt = seg(t, B.a.area1 + 1600, B.a.area1 + 2400);
  const trap = seg(t, B.a.area2 + 2000, B.a.area2 + 2600);
  const ln = (x0, x1, f) => [MP.p([x0, f(x0)]), MP.p([x1, f(x1)])];
  return (
    <g>
      {l1 > 0 && <g opacity={l1}><Path pts={ln(1.5, 15.0, (x) => (4 / 3) * x - 2)} stroke={C.ink} sw={2} o={0.55} />
        <Chip x={MP.p([5.6, 9.6])[0]} y={MP.p([5.6, 9.6])[1]} s={TR.M.lineAB} size={22} C={C} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      {l2 > 0 && <g opacity={l2}><Path pts={ln(8.2, 30.6, (x) => -(3 / 4) * x + TR.bcB)} stroke={C.ink} sw={2} o={0.55} />
        <Chip x={MP.p([23.4, 11.6])[0]} y={MP.p([23.4, 11.6])[1]} s={TR.M.lineBC} size={22} C={C} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      {l3 > 0 && <g opacity={l3}><Path pts={[MP.p([0, TR.C[1]]), MP.p([32.5, TR.C[1]])]} stroke={C.ink} sw={2} o={0.55} />
        <Chip x={MP.p([31.2, 3.6])[0]} y={MP.p([31.2, 3.6])[1]} s={TR.M.lineCA} size={22} C={C} fill={C.paper} color={C.ink} stroke={C.soft} /></g>}
      {base > 0 && <g opacity={base}>
        <Path pts={[A, Cp]} stroke={C.gold} sw={7} o={0.6} />
        <SegLbl P={A} Q={Cp} s={`밑변 ${TR.base}`} side={-1} off={30} C={C} size={26} fill={C.gold} at={0.62} />
      </g>}
      {hgt > 0 && <g opacity={hgt}>
        <Path pts={[Bp, FOOT]} stroke={C.gold} sw={3} dash="8 7" />
        <RightMark V={FOOT} A={Cp} B={Bp} s={14} C={C} color={C.gold} />
        <SegLbl P={Bp} Q={FOOT} s={`높이 ${TR.height}`} side={1} off={44} C={C} size={26} fill={C.gold} />
      </g>}
      {trap > 0 && <g opacity={trap}>
        <Path pts={[Bp, MP.p([TR.B[0], 0])]} stroke={C.red} sw={2.4} dash="3 7" o={0.8} />
        <UText x={MP.p([TR.B[0], 0])[0] + 8} y={MP.p([TR.B[0], 0])[1] - 10} s={`${TR.B[1]} ⟪×r⟫`} size={22} weight={700} fill={C.red} C={C} />
      </g>}
      {/* 꼭짓점 좌표 */}
      <Chip x={A[0] - 20} y={A[1] + 46} s={TR.M.labA} size={22} C={C} o={seg(t, B.a.read + 3300, B.a.read + 3800)} fill={C.paper} color={C.ink} stroke={C.ink} anchor="middle" />
      <Chip x={Bp[0]} y={Bp[1] - 46} s={TR.M.labB} size={22} C={C} o={seg(t, B.a.read + 5600, B.a.read + 6100)} fill={C.paper} color={C.ink} stroke={C.ink} />
      <Chip x={Cp[0] + 6} y={Cp[1] + 46} s={TR.M.labC} size={22} C={C} o={seg(t, B.a.read + 400, B.a.read + 900)} fill={C.paper} color={C.ink} stroke={C.ink} />
      <UBoard x={990} y={232} t={t} C={C} size={28} lh={54} lines={[
        { t: B.a.read + 2400, s: TR.M.b },
        { t: B.a.read + 3800, s: TR.M.a },
        { t: B.a.read + 6100, s: TR.M.bb },
        { t: B.a.area1 + 2400, s: TR.M.bh },
        { t: B.a.area2 + 600, s: TR.M.area },
        { t: B.a.area2 + 2600, s: TR.M.trap, c: "soft" },
      ]} />
    </g>
  );
}

export default {
  key: "soc-triangle",
  dur: B.dur,
  title: { e: "패스 삼각형의 넓이", m: "패스 삼각형의 넓이 — 직선과 교점" },
  sub: { e: "초등 · 직사각형에서 빼는 넓이 · 맨유 삼각패스", m: "중2 · 일차함수의 그래프와 교점 · 맨유 삼각패스" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
