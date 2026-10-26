// 장면 13 — 분류하기(초등 2-1) ↔ 사건과 경우의 수 · 합의 법칙(중2)
// 같은 카드 12장(모양 3가지 × 색 3가지)을 모양으로, 다시 색깔로 나눈다. 두 판의 카드 움직임은 똑같다.
//   초등: 하나씩 표시하며 세기 → 기준이 바뀌면 나누어진 모습도 바뀜 → 분명한 기준
//   중등: 한 장 뽑기 = 12가지 → 동시에 일어나지 않는 두 사건은 더한다 → 동시에 일어날 수 있으면 겹친 것을 한 번 뺀다
import { beats, seg, win, E, lerp, rng } from "../core";
import { Board, Caption, MText, ShapeIcon, Check } from "../draw";
import { SORT } from "../facts";

const { CARDS, SHAPES, COLORS, CN } = SORT;
const B = beats([["intro", 2600], ["ask", 2400], ["sort1", 4200], ["count1", 4200], ["sort2", 4200], ["count2", 3800], ["last", 6400], ["hold", 2600]]);
const CW = 96, CH = 86, COLX = [250, 470, 690], TOP0 = 673, STEP = 94;
const COLOR_KEY = { r: "red", b: "blue", y: "yellow" };

/* 흩어진 자리 — 4×3 칸에 섞어 놓고 조금씩 기울인다(결정적) */
const SLOT_OF = [5, 0, 9, 2, 7, 11, 3, 8, 1, 10, 6, 4];
const PILE = CARDS.map((c) => {
  const s = SLOT_OF[c.id], col = s % 4, row = Math.floor(s / 4), r = rng(31 + s * 17);
  return { x: 200 + col * 160 + (r() - 0.5) * 44, y: 290 + row * 150 + (r() - 0.5) * 36, rot: (r() - 0.5) * 28, drop: s };
});
/** 기준(key)·순서(order)로 나눈 자리 — 열마다 아래에서 위로 쌓는다(그래프처럼) */
function layout(key, order, sub, subOrder) {
  const pos = {}, seq = [];
  order.forEach((g, col) => {
    CARDS.filter((c) => c[key] === g).sort((a, b) => subOrder.indexOf(a[sub]) - subOrder.indexOf(b[sub]) || a.id - b.id)
      .forEach((c, k) => { pos[c.id] = { x: COLX[col], y: TOP0 - STEP * k, col, k }; seq.push(c.id); });
  });
  const ord = {}; seq.forEach((id, j) => (ord[id] = j));
  return { pos, ord, n: order.map((g) => CARDS.filter((c) => c[key] === g).length) };
}
const L1 = layout("shape", SHAPES, "color", COLORS);
const L2 = layout("color", COLORS, "shape", SHAPES);
const colTop = (n) => TOP0 - STEP * (n - 1) - CH / 2;

function cardAt(c, t, mode) {
  const P = PILE[c.id];
  const dt = 300 + P.drop * 110, pd = seg(t, dt, dt + 650, E.drop);
  let x = P.x, y = P.y - (1 - pd) * 520, rot = P.rot;
  // 초등은 "어떻게 나눌까" 동안 살짝 흔들린다
  if (mode === "e") rot += 5 * Math.sin(t / 140 + c.id) * win(t, B.a.ask, B.b.ask, 300, 300);
  const s1 = B.a.sort1 + 250 + L1.ord[c.id] * 170, p1 = seg(t, s1, s1 + 950, E.io);
  const T1 = L1.pos[c.id];
  x = lerp(x, T1.x, p1); y = lerp(y, T1.y, p1) - 70 * Math.sin(Math.PI * p1); rot = lerp(rot, 0, p1);
  const s2 = B.a.sort2 + 250 + L2.ord[c.id] * 170, p2 = seg(t, s2, s2 + 950, E.io);
  const T2 = L2.pos[c.id];
  x = lerp(x, T2.x, p2); y = lerp(y, T2.y, p2) - 70 * Math.sin(Math.PI * p2);
  return { x, y, rot, o: seg(t, dt, dt + 160, E.lin), flying: (p1 > 0 && p1 < 1) || (p2 > 0 && p2 < 1) };
}

function Card({ c, st, C, dim = 0, rings = [], check = 0, flash = 0 }) {
  const k = COLOR_KEY[c.color];
  return (
    <g transform={`translate(${st.x.toFixed(1)} ${st.y.toFixed(1)}) rotate(${st.rot.toFixed(2)})`} opacity={st.o * (1 - 0.6 * dim)}>
      {flash > 0 && <rect x={-CW / 2 - 6} y={-CH / 2 - 6} width={CW + 12} height={CH + 12} rx={16} fill={C.gold} opacity={0.35 * flash} />}
      <rect x={-CW / 2} y={-CH / 2} width={CW} height={CH} rx={12} fill={C.card} stroke={C.cardEdge} strokeWidth={2.4} />
      <ShapeIcon kind={c.shape} cx={0} cy={2} r={25} fill={C[k]} C={C} />
      {rings.map((r, i) => r.o > 0 && (
        <rect key={i} x={-CW / 2 - r.pad} y={-CH / 2 - r.pad} width={CW + 2 * r.pad} height={CH + 2 * r.pad} rx={14 + r.pad}
          fill="none" stroke={C[r.col]} strokeWidth={5} opacity={r.o} />
      ))}
      {check > 0 && <g>
        <circle cx={CW / 2 - 6} cy={-CH / 2 + 6} r={15} fill={C.paper} stroke={C.gold} strokeWidth={2.4} opacity={Math.min(1, check * 2)} />
        <Check cx={CW / 2 - 6} cy={-CH / 2 + 6} r={10} color={C.gold} sw={3.6} p={check} />
      </g>}
    </g>
  );
}

function Scene({ t, C, mode }) {
  const isM = mode === "m";
  const T = isM ? SORT.M : SORT.E;
  // 열 머리글: 모양 → 색깔
  const h1 = seg(t, B.a.sort1, B.a.sort1 + 600) * (1 - seg(t, B.a.sort2, B.a.sort2 + 500));
  const h2 = seg(t, B.a.sort2 + 400, B.a.sort2 + 1000);
  // 셈: 초등은 하나씩 ✓, 중등은 한꺼번에
  const chk = (id) => {
    if (isM) return 0;
    const a = B.a.count1 + 300 + L1.ord[id] * 240, b = B.a.count2 + 300 + L2.ord[id] * 200;
    const c1 = seg(t, a, a + 280) * (1 - seg(t, B.a.sort2, B.a.sort2 + 300));
    const c2 = seg(t, b, b + 280) * (1 - seg(t, B.a.last + 200, B.a.last + 600));
    return Math.max(c1, c2);
  };
  const shown = (L, col, t0, step) => {
    if (isM) return t >= t0 ? L.n[col] : 0;
    return CARDS.filter((c) => L.pos[c.id].col === col && t >= t0 + L.ord[c.id] * step + 200).length;
  };
  const cnt1 = SHAPES.map((_, col) => shown(L1, col, B.a.count1 + 300, 240));
  const cnt2 = COLORS.map((_, col) => shown(L2, col, B.a.count2 + 300, 200));
  const n1O = seg(t, B.a.count1 + 300, B.a.count1 + 700) * (1 - seg(t, B.a.sort2, B.a.sort2 + 400));
  const n2O = seg(t, B.a.count2 + 300, B.a.count2 + 700);
  // 강조
  const w1 = win(t, B.a.count1 + 300, B.a.sort2 + 100, 400, 400);     // 중등: ○·△ 열
  const w2 = win(t, B.a.count2 + 300, B.a.last + 200, 400, 400);      // 중등: 파랑·노랑 열
  const wL = seg(t, B.a.last + 400, B.a.last + 900);
  const cards = CARDS.map((c) => ({ c, st: cardAt(c, t, mode) }));
  cards.sort((a, b) => (a.st.flying === b.st.flying ? 0 : a.st.flying ? 1 : -1));
  return (
    <g>
      {/* 열 머리글 */}
      {h1 > 0 && SHAPES.map((k, i) => <ShapeIcon key={k} kind={k} cx={COLX[i]} cy={760} r={17} stroke={C.ink} C={C} o={h1} />)}
      {h2 > 0 && COLORS.map((k, i) => (
        <g key={k} opacity={h2}>
          <circle cx={COLX[i] - 34} cy={758} r={11} fill={C[COLOR_KEY[k]]} />
          <MText x={COLX[i] - 16} y={770} s={CN[k]} size={30} weight={600} C={C} />
        </g>
      ))}
      {cards.map(({ c, st }) => {
        let dim = 0;
        const rings = [];
        const p1 = L1.pos[c.id], p2 = L2.pos[c.id];
        if (isM) {
          if (p1.col <= 1) rings.push({ col: "gold", pad: 4, o: w1 }); else dim = Math.max(dim, w1);
          if (p2.col >= 1) rings.push({ col: "gold", pad: 4, o: w2 }); else dim = Math.max(dim, w2);
          if (c.shape === "circle") rings.push({ col: "teal", pad: 3, o: wL });
          if (c.color === "r") rings.push({ col: "coral", pad: 9, o: seg(t, B.a.last + 1400, B.a.last + 1900) });
          if (c.shape !== "circle" && c.color !== "r") dim = Math.max(dim, seg(t, B.a.last + 1400, B.a.last + 1900));
        } else if (p2.col === COLORS.indexOf(SORT.mostColor)) {
          rings.push({ col: "gold", pad: 5, o: seg(t, B.a.last + 2400, B.a.last + 2900) });
        }
        const both = isM && c.shape === "circle" && c.color === "r";
        const pulse = both ? win(t, B.a.last + 2400, Infinity, 300, 300) * (0.5 + 0.5 * Math.sin(t / 160)) : 0;
        const flash = isM ? win(t, B.a.ask + 300 + c.id * 110, B.a.ask + 900 + c.id * 110, 150, 300) : 0;
        return <Card key={c.id} c={c} st={st} C={C} dim={dim} rings={rings} check={chk(c.id)} flash={Math.max(flash, pulse)} />;
      })}
      {/* 열 위의 수 */}
      {n1O > 0 && SHAPES.map((_, i) => cnt1[i] > 0 && (
        <MText key={"a" + i} x={COLX[i]} y={colTop(L1.n[i]) - 18} s={`${cnt1[i]}`} size={40} weight={800} anchor="middle"
          fill={isM && i === 2 ? C.soft : C.gold} opacity={n1O} C={C} />
      ))}
      {n2O > 0 && COLORS.map((_, i) => cnt2[i] > 0 && (
        <MText key={"b" + i} x={COLX[i]} y={colTop(L2.n[i]) - 18} s={`${cnt2[i]}`} size={40} weight={800} anchor="middle"
          fill={isM && i === 0 && t < B.a.last + 200 ? C.soft : C.gold} opacity={n2O} C={C} />
      ))}
      {!isM && <MText x={COLX[COLORS.indexOf(SORT.mostColor)]} y={colTop(L2.n[1]) - 70} s="가장 많아요" size={30} weight={700}
        anchor="middle" fill={C.gold} opacity={seg(t, B.a.last + 2400, B.a.last + 2900)} C={C} />}
      {isM && <MText x={COLX[0]} y={colTop(L2.n[0]) - 70} s="겹치는 2장" size={30} weight={700} anchor="middle"
        fill={C.gold} opacity={seg(t, B.a.last + 2400, B.a.last + 2900)} C={C} />}
      <Board x={980} y={232} t={t} C={C} size={36} lh={58} lines={isM ? [
        { t: B.a.ask + 200, s: "카드 한 장을 뽑는 사건", k: "h" },
        { t: B.a.ask + 900, s: T.all },
        { t: B.a.count1 + 200, s: "합의 법칙 — 동시에 일어나지 않을 때", k: "h" },
        { t: B.a.count1 + 1800, s: T.ct },
        { t: B.a.count2 + 1600, s: T.by },
        { t: B.a.last + 200, s: "동시에 일어날 수 있을 때", k: "h" },
        { t: B.a.last + 3400, s: T.cr },
      ] : [
        { t: B.a.sort1 + 200, s: "모양에 따라 분류", k: "h" },
        { t: B.a.count1 + 3300, s: T.shapeLine },
        { t: B.a.sort2 + 200, s: "색깔에 따라 분류", k: "h" },
        { t: B.a.count2 + 2900, s: T.colorLine },
        { t: B.a.last + 200, s: "분류한 결과", k: "h" },
        { t: B.a.last + 800, s: `어느 기준으로 나누어도 모두 ‹${CARDS.length}›장` },
        { t: B.a.last + 2600, s: T.most },
      ]} />
      <Caption t={t} C={C} caps={isM ? [
        { t: 300, s: "카드 12장 중 한 장을 뽑아요" },
        { t: B.a.ask, s: "경우의 수 — 사건이 일어나는 가짓수" },
        { t: B.a.sort1, s: "모양에 따라 나누면" },
        { t: B.a.count1, s: "⟪○⟫과 ⟪△⟫은 동시에 나올 수 없어요 → 더해요" },
        { t: B.a.sort2, s: "색깔에 따라 나누면" },
        { t: B.a.count2, s: "파랑과 노랑도 동시에 나올 수 없어요" },
        { t: B.a.last, s: "⟪○⟫이면서 빨강인 카드는 두 번 세면 안 돼요" },
        { t: B.a.last + 3200, s: "겹치는 2장을 한 번 빼요" },
      ] : [
        { t: 300, s: "모양과 색깔이 다른 카드 12장" },
        { t: B.a.ask, s: "어떻게 나누어 볼까요?" },
        { t: B.a.sort1, s: "모양에 따라 분류해요" },
        { t: B.a.count1, s: "하나씩 표시하며 세면 빠뜨리지 않아요" },
        { t: B.a.sort2, s: "이번에는 색깔에 따라" },
        { t: B.a.count2, s: "기준이 바뀌면 나누어진 모습도 달라져요" },
        { t: B.a.last, s: "‘예쁜 것’처럼 사람마다 다른 것은 기준이 될 수 없어요" },
        { t: B.a.last + 3400, s: "누가 분류해도 결과가 같은 분명한 기준으로" },
      ]} />
    </g>
  );
}

export default {
  key: "sort",
  dur: B.dur,
  title: { e: "분류하기", m: "경우의 수와 합의 법칙" },
  sub: { e: "초등 · 분류하기", m: "중2 · 경우의 수" },
  render: (mode, t, C) => <Scene t={t} C={C} mode={mode} />,
};
