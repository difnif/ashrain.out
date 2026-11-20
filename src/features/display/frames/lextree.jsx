// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 · 사전식 세트의 오른쪽 그림: 세로 나무 (frames/lextree.jsx)
// 강사 칠판 판서 그대로 — 위에 카드를 늘어놓고 쓴 카드는 빗금으로 지우고, 오른쪽에 덩어리 크기(2 · 6 · 24 …)를 세로로 적어 둔 채
//   글자 후보를 단마다 세로로 내려 적는다. 다 쓴 묶음의 글자 옆에는 덩어리 크기를 작게, 고른 글자는 금빛 굵게 밑줄,
//   다음 단은 고른 글자의 줄에서 오른쪽으로 이어진다. 끝으로 최종 묶음 안에서 남은 글자(큰 것부터 · 작은 것부터)를 쓴다.
// 판서 줄과 맞물림: it.fig.at[단] = [그 단이 나타나는 판서 줄, 글자를 고르는 판서 줄] · tailAt = 남은 글자 줄 (l10Plan 의 줄 시각).
// 데이터: ../cnt100-items.js 의 CNT100_LEX[i].fig — { kind: "tree", cards, cols: [{ start, items: [[글자, 덩어리, 고름]] }], tail, tailAt, at, sizes }
import { seg, E } from "../core.js";
import { SANS } from "../draw.jsx";
import { l10Plan } from "../lin10.js";

const BOX = { x0: 880, y0: 170, x1: 1540, y1: 850 };

export function treeGeom(f) {
  const n = f.cards.length;
  const cw = Math.min(64, (BOX.x1 - BOX.x0 - 150) / n - 10);
  const rows = Math.max(...f.cols.map((c) => c.start + c.items.length));
  const top = BOX.y0 + 150, bot = BOX.y1 - 20;
  const rh = Math.min(62, (bot - top) / rows);
  const ncol = f.cols.length + (f.tail ? 1 : 0);
  const colW = Math.min(118, (BOX.x1 - 130 - (BOX.x0 + 30)) / ncol);
  const ls = Math.min(40, rh * 0.68);
  return { n, cw, rows, top, rh, colW, ls, deckY: BOX.y0 + 40, x0: BOX.x0 + 30, szX: BOX.x1 - 24 };
}

export function LexTree({ it, t, C }) {
  const f = it.fig, P = l10Plan(it), G = treeGeom(f);
  const lt = (i) => (P.lines[Math.min(i, P.lines.length - 1)] || P.lines[P.lines.length - 1]).a;
  const base = seg(t, P.plan[0], P.plan[0] + 600, E.sine);
  if (base <= 0) return null;
  // 고른 시각(카드에 빗금) — 단마다
  const pickT = f.cols.map((c, li) => lt(f.at[li][1]) + 350);
  const picked = new Map();
  f.cols.forEach((c, li) => { const ch = c.items.find((x) => x[2]); if (ch) picked.set(ch[0], pickT[li]); });
  const els = [];
  // 카드
  f.cards.forEach((L, i) => {
    const x = G.x0 + i * (G.cw + 10);
    const sl = picked.has(L) ? seg(t, picked.get(L), picked.get(L) + 450, E.out) : 0;
    els.push(
      <g key={`c${i}`}>
        <rect x={x} y={G.deckY} width={G.cw} height={G.cw * 1.15} rx={8} fill="none" stroke={C.soft} strokeWidth={2.5} />
        <text x={x + G.cw / 2} y={G.deckY + G.cw * 0.8} fontFamily={SANS} fontSize={G.cw * 0.62} fontWeight={700} fill={C.ink} textAnchor="middle" opacity={sl > 0.5 ? 0.45 : 1}>{L}</text>
        {sl > 0 && <line x1={x + G.cw * 0.15} y1={G.deckY + G.cw * 1.05} x2={x + G.cw * 0.15 + G.cw * 0.7 * sl} y2={G.deckY + G.cw * 1.05 - G.cw * 0.95 * sl} stroke={C.red} strokeWidth={4} strokeLinecap="round" />}
      </g>,
    );
  });
  // 덩어리 크기(오른쪽 세로)
  els.push(<text key="szh" x={G.szX} y={G.top - 12} fontFamily={SANS} fontSize={20} fontWeight={700} fill={C.soft} textAnchor="end">덩어리</text>);
  (f.sizes.length ? f.sizes : [1]).forEach((s, i) => {
    els.push(<text key={`sz${i}`} x={G.szX} y={G.top + 30 + i * 40} fontFamily={SANS} fontSize={30} fontWeight={600} fill={C.soft} textAnchor="end">{s}</text>);
  });
  els.push(<line key="szl" x1={G.szX - 78} y1={G.top - 34} x2={G.szX - 78} y2={G.top + 20 + Math.max(1, f.sizes.length) * 40} stroke={C.soft} strokeWidth={2} opacity={0.6} />);
  // 세로 나무
  f.cols.forEach((c, li) => {
    const [sa, pa] = f.at[li];
    const t0 = lt(sa), tp = lt(pa);
    const x = G.x0 + li * G.colW;
    c.items.forEach(([L, blk, ch], j) => {
      const y = G.top + (c.start + j) * G.rh + G.ls;
      const ta = ch ? Math.max(tp, t0 + j * 260) + (pa === sa ? 300 : 0) : t0 + j * 260;
      const o = seg(t, ta, ta + 380, E.out);
      if (o <= 0) return;
      els.push(
        <g key={`t${li}-${j}`} opacity={o}>
          <text x={x} y={y} fontFamily={SANS} fontSize={G.ls} fontWeight={ch ? 800 : 600} fill={ch ? C.gold : C.ink}>{L}</text>
          {ch && <line x1={x - 2} y1={y + G.ls * 0.18} x2={x + G.ls * 0.78} y2={y + G.ls * 0.18} stroke={C.gold} strokeWidth={3.5} strokeLinecap="round" />}
          {!ch && blk > 1 && <text x={x + G.ls * 0.82} y={y - G.ls * 0.05} fontFamily={SANS} fontSize={G.ls * 0.5} fontWeight={600} fill={C.soft}>{blk}</text>}
        </g>,
      );
    });
  });
  if (f.tail) {
    const last = f.cols[f.cols.length - 1];
    const y = G.top + (last.start + last.items.length - 1) * G.rh + G.ls;
    const ta = lt(f.tailAt) + 300;
    const o = seg(t, ta, ta + 500, E.out);
    if (o > 0) els.push(
      <text key="tail" x={G.x0 + f.cols.length * G.colW} y={y} fontFamily={SANS} fontSize={G.ls} fontWeight={800} fill={C.gold} letterSpacing={G.ls * 0.12} opacity={o}>{f.tail}</text>,
    );
  }
  return <g opacity={base}>{els}</g>;
}
