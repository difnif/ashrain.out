// 서술형 4 — 「게임의 규칙」 간식 심부름: 셋이 하는 가위바위보
// 서아 · 도윤 · 지민이 저마다 가위 · 바위 · 보 가운데 하나를 같은 가능성으로 낸다. 셋이 모두 같거나 모두 다르면 비기고,
// 그 밖에는 승부가 난다. 한 번 할 때 승부가 날 확률.
//   초등: 27가지를 모두 늘어놓기 → 모두 같은 손 3 · 모두 다른 손 6 → 비김 9 → 승부 18 → 27번 중 18번 = 3번 중 2번 → {2/3}
//   중등: 3 × 3 × 3 = 27, 비김 3 + 3 × 2 × 1 = 9 → 1 − {9/27} = {2/3} · 1 − {3/27} = {8/9} ✗(모두 다른 경우를 빠뜨림)
import { beats, seg, win } from "../core";
import { UText, UBoard, UCaption, Chip, Person } from "../kit-story";
import { Hand, HAND_COL } from "../kit-essay";
import { RPS, CLUB } from "../facts-essay";

const B = beats([["intro", 2600], ["rule", 6600], ["all", 6200], ["same", 3800], ["diff", 4800], ["ans", 6400], ["trap", 5600], ["hold", 2400]]);
const NAMES = CLUB.FRIENDS;                              // 서아 · 도윤 · 지민(「게임의 규칙」의 세 친구)
const FX = 110, FY = [258, 388, 518], FR_COL = ["gold", "teal", "blue"];
const HX = 214;
const EX = RPS.SHOW.map((h, k) => ({ h, t0: B.a.rule + 100 + k * 2100 }));
/** 받침이 있으면 "이", 없으면 "가" */
const iga = (w) => { const c = w.charCodeAt(w.length - 1) - 0xac00; return c >= 0 && c < 11172 && c % 28 ? "이" : "가"; };
const kindOf = (h) => (new Set(h).size === 1 ? "same" : new Set(h).size === 3 ? "diff" : "dec");
// 27칸: 서아의 손(묶음) × 도윤(가로줄) × 지민(세로줄)
const GX = 620, EW = 92, EH = 54, EG = 8, GW = 3 * EW + 2 * EG, GG = 24, GY = 236;
const ex = (a, c) => GX + a * (GW + GG) + c * (EW + EG);
const ey = (b) => GY + b * (EH + EG);

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const cur = [...EX].reverse().find((e) => t >= e.t0);
  const exO = (cur ? 1 : 0) * (1 - seg(t, B.b.rule - 300, B.b.rule + 200));
  const gridO = seg(t, B.a.all, B.a.all + 500);
  return (
    <g>
      {/* 세 친구 */}
      {NAMES.map((nm, i) => (
        <g key={nm} opacity={seg(t, 200 + i * 200, 700 + i * 200)}>
          <Person x={FX} y={FY[i]} h={56} col={C[FR_COL[i]]} C={C} />
          <UText x={FX} y={FY[i] + 26} s={nm} size={22} weight={750} anchor="middle" fill={C[FR_COL[i]]} C={C} />
        </g>
      ))}
      {/* 예: 손을 흔들다가 낸다 */}
      {exO > 0 && cur && <Shown e={cur} t={t} C={C} o={exO} />}
      {t < B.a.rule && <g opacity={seg(t, 900, 1300)}>
        {NAMES.map((_, i) => <Hand key={i} kind={1} x={HX} y={FY[i] - 20 - 8 * Math.abs(Math.sin((t - 900) / 150))} s={60} C={C} />)}
      </g>}
      {/* 27가지 */}
      {gridO > 0 && <g opacity={gridO}>
        <UText x={GX} y={176} s={`한 칸 = ${NAMES.join(" · ")}${iga(NAMES.at(-1))} 낸 손`} size={20} weight={650} fill={C.soft} C={C} />
        {[0, 1, 2].map((a) => (
          <g key={a} opacity={seg(t, B.a.all + 200 + a * 700, B.a.all + 600 + a * 700)}>
            <UText x={ex(a, 0) + GW / 2} y={GY - 22} s={`${NAMES[0]} : ${RPS.HANDS[a]}`} size={21} weight={750} anchor="middle" fill={C.ink} C={C} />
            <rect x={ex(a, 0) + 6} y={GY - 12} width={GW - 12} height={5} rx={2.5} fill={C[HAND_COL[a]]} />
          </g>
        ))}
        {RPS.ALL.map((x, i) => <Entry key={i} x={x} i={i} t={t} C={C} />)}
        <Counts t={t} C={C} isM={isM} />
      </g>}
      {/* 손 모양 보기 */}
      {gridO > 0 && <g opacity={gridO}>
        {RPS.HANDS.map((nm, k) => (
          <g key={nm}>
            <Hand kind={k} x={96 + k * 120} y={664} s={50} C={C} />
            <UText x={96 + k * 120} y={712} s={nm} size={24} weight={750} anchor="middle" fill={C[HAND_COL[k]]} C={C} />
          </g>
        ))}
      </g>}
      <UBoard x={GX} y={500} t={t} C={C} size={30} lh={54} lines={isM ? [
        { t: B.a.all + 2600, s: RPS.M.all },
        { t: B.a.diff + 2400, s: RPS.M.draw },
        { t: B.a.ans + 1800, s: RPS.M.ans },
        { t: B.a.trap + 1200, s: RPS.M.trap, size: 27 },
      ] : [
        { t: B.a.all + 2600, s: RPS.E.all },
        { t: B.a.same + 700, s: RPS.E.same },
        { t: B.a.diff + 700, s: RPS.E.diff },
        { t: B.a.ans + 400, s: RPS.E.draw },
        { t: B.a.ans + 2400, s: RPS.E.ans },
        { t: B.a.trap + 1200, s: `${RPS.E.trap}  ${RPS.E.why}`, size: 27 },
      ]} />
      <UCaption t={t} C={C} caps={[
        { t: 300, s: `간식 심부름은 가위바위보로 — ${NAMES.join(" · ")} 셋이 해요` },
        { t: EX[0].t0, s: "셋이 모두 같은 손을 내면 비겨요" },
        { t: EX[1].t0, s: "셋이 모두 다른 손을 내도 비겨요" },
        { t: EX[2].t0, s: "그 밖에는 이긴 사람과 진 사람이 갈려요 — 승부!" },
        ...(isM ? [
          { t: B.a.all, s: `셋이 저마다 ${RPS.HANDS.length}가지 — 곱의 법칙` },
          { t: B.a.all + 2600, s: `모든 경우 ${RPS.total}가지 — 하나하나 가능성이 같아요` },
          { t: B.a.same, s: `모두 같은 손 — ${RPS.same}가지` },
          { t: B.a.diff, s: `모두 다른 손 — ${RPS.HANDS.length} × ${RPS.HANDS.length - 1} × ${RPS.HANDS.length - 2} = ${RPS.diff}가지` },
          { t: B.a.ans, s: `비기지 않을 확률 = 1 − (비길 확률)` },
          { t: B.a.ans + 1800, s: `승부가 날 확률 ${strip(RPS.M.ans)}` },
          { t: B.a.trap, s: `모두 같은 경우만 빼서 1 − {${RPS.same}/${RPS.total}}로 하면 틀려요` },
          { t: B.a.trap + 2600, s: "모두 다른 손을 낸 경우도 비김이에요" },
        ] : [
          { t: B.a.all, s: `${NAMES[0]}의 손 ${RPS.HANDS.length}가지마다 도윤 · 지민의 손 ${RPS.HANDS.length ** 2}가지` },
          { t: B.a.all + 2600, s: `모두 ${RPS.total}가지 — 하나하나 가능성이 같아요` },
          { t: B.a.same, s: `모두 같은 손 — ${RPS.same}가지` },
          { t: B.a.diff, s: `모두 다른 손 — ${RPS.diff}가지` },
          { t: B.a.ans, s: `비기는 ${RPS.draw}가지를 빼면 승부 ${RPS.dec}가지` },
          { t: B.a.ans + 2400, s: strip(RPS.E.ans) },
          { t: B.a.trap, s: `모두 같은 손만 빼서 ${RPS.total - RPS.same}번이라고 하면 틀려요` },
          { t: B.a.trap + 2600, s: "모두 다른 손을 낸 경우도 비김이에요" },
        ]),
      ]} />
    </g>
  );
}
const strip = (s) => s.replace(/[‹›]/g, "");

/** 예 한 판: 셋의 손 + 결과 */
function Shown({ e, t, C, o }) {
  const shake = t < e.t0 + 700;
  const k = kindOf(e.h);
  const res = seg(t, e.t0 + 900, e.t0 + 1300);
  const label = k === "same" ? "비김 — 모두 같아요" : k === "diff" ? "비김 — 모두 달라요" : "승부!";
  return (
    <g opacity={o * seg(t, e.t0, e.t0 + 200)}>
      {e.h.map((h, i) => (
        <Hand key={i} kind={shake ? 1 : h} x={HX} y={FY[i] - 20 - (shake ? 8 * Math.abs(Math.sin((t - e.t0) / 150)) : 0)} s={60} C={C} />
      ))}
      {!shake && e.h.map((h, i) => (
        <UText key={"n" + i} x={HX + 46} y={FY[i] - 14} s={RPS.HANDS[h]} size={26} weight={750} fill={C[HAND_COL[h]]} opacity={res} C={C} />
      ))}
      {res > 0 && <Chip x={HX + 140} y={FY[1] - 30} s={label} size={28} C={C} anchor="start" o={res}
        fill={k === "dec" ? C.teal : C.lilac} color={C.paper} />}
      {res > 0 && k === "dec" && <Winners h={e.h} C={C} o={res} />}
    </g>
  );
}
/** 승부가 난 판: 이긴 손에 ✓ */
function Winners({ h, C, o }) {
  const kinds = [...new Set(h)];
  const beats2 = (a, b) => (a + 2) % 3 === b;            // 가위(0) > 보(2), 바위(1) > 가위(0), 보(2) > 바위(1)
  const win1 = beats2(kinds[0], kinds[1]) ? kinds[0] : kinds[1];
  return (
    <g opacity={o}>
      {h.map((x, i) => x === win1 && <UText key={i} x={HX - 46} y={FY[i] - 12} s="⟪✓t⟫" size={30} anchor="middle" C={C} />)}
    </g>
  );
}

/** 27칸 가운데 하나 */
function Entry({ x, i, t, C }) {
  const [a, b, c] = x.h;
  const a0 = B.a.all + 300 + a * 700 + (b * 3 + c) * 45;
  const o = seg(t, a0, a0 + 260);
  if (o <= 0) return null;
  const px = ex(a, c), py = ey(b);
  const kS = x.same ? seg(t, B.a.same + 300, B.a.same + 800) : 0;
  const kD = x.diff ? seg(t, B.a.diff + 300 + i * 12, B.a.diff + 800 + i * 12) : 0;
  const kA = seg(t, B.a.ans + 300, B.a.ans + 900);
  const trap = x.diff ? win(t, B.a.trap + 300, B.b.trap - 200, 400, 400) : 0;
  const col = x.same ? C.gold : x.diff ? C.lilac : C.teal;
  const hi = x.draw ? Math.max(kS, kD) : kA;
  const dim = x.draw ? 1 - 0.45 * kA * (1 - trap) : 1;
  return (
    <g opacity={o * dim}>
      <rect x={px} y={py} width={EW} height={EH} rx={10} fill={hi > 0 ? col : C.faint} fillOpacity={hi > 0 ? 0.12 + 0.2 * hi : 1}
        stroke={trap > 0 ? C.red : hi > 0 ? col : C.cardEdge} strokeWidth={trap > 0 ? 3.4 : hi > 0 ? 2.6 : 1.2} strokeDasharray={trap > 0 ? "7 5" : undefined} />
      {x.h.map((h, k) => <Hand key={k} kind={h} x={px + 18 + k * 28} y={py + EH / 2 + 6} s={25} C={C} />)}
    </g>
  );
}

/** 묶음마다 센 수 */
function Counts({ t, C, isM }) {
  const rows = [
    { k: "same", s: (n) => `같음 ${n}`, col: "gold", t0: B.a.same + 900 },
    { k: "diff", s: (n) => `다름 ${n}`, col: "lilac", t0: B.a.diff + 900 },
  ];
  const decO = seg(t, B.a.ans + 900, B.a.ans + 1300);
  return (
    <g>
      {[0, 1, 2].map((a) => {
        const xs = RPS.ALL.filter((x) => x.h[0] === a);
        const cx = ex(a, 0) + GW / 2, y = ey(2) + EH + 34;
        const nS = xs.filter((x) => x.same).length, nD = xs.filter((x) => x.diff).length, nE = xs.length - nS - nD;
        const items = [];
        rows.forEach((r, j) => {
          const o = seg(t, r.t0, r.t0 + 400) * (1 - decO);
          if (o > 0) items.push(<Chip key={r.k} x={cx + (j ? 58 : -58)} y={y} s={r.s(r.k === "same" ? nS : nD)} size={20} C={C} o={o} fill={C[r.col]} color={C.paper} />);
        });
        if (decO > 0) items.push(<Chip key="d" x={cx} y={y} s={isM ? `승부 ${nE}` : `승부 ${nE}가지`} size={22} C={C} o={decO} fill={C.teal} color={C.paper} />);
        return <g key={a}>{items}</g>;
      })}
    </g>
  );
}

export default {
  key: "ess-rps",
  dur: B.dur,
  title: { e: "셋이 하는 가위바위보 — 27가지", m: "셋이 하는 가위바위보 — 승부가 날 확률" },
  sub: { e: "초등 · 일이 일어날 가능성 · 「게임의 규칙」", m: "중2 · 경우의 수와 확률 · 「게임의 규칙」" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
