// ashrain.out — 해설 액자의 글자 판 그리기 (frames/board.jsx) — 배치는 ../board.js(boardLayout)
// ① 문제 → ② 방침(꼬리표 + 한 줄 · 길면 이어서) → ③ 판서 줄(지금 줄에 금빛 막대 · 빨간 메모가 써지듯) → ④ 답 칸.
// 일차함수 10단계 · 경우의 수와 확률 100제 · 기본기 해설(frames/lin10.jsx 의 L10Art)과 그래프와 넓이(frames/area.jsx)가 함께 쓴다.
// 판이 넘쳐 흐르면(Lo.scroll) 방침 · 판서 · 답 칸을 잘라 보이며 위로 올린다 — 문제는 위에 그대로.
// 두 단(Lo.two)이면 두 단 사이에 옅은 세로줄.
// 그림 자리(Lo.fig): FigSlot 이 그림을 그 네모에 넣는다 — 제 크기 그림은 배율로 줄이고(box 제 크기 네모), 좌표평면처럼 스스로 맞추는 그림은 네모를 그대로 넘긴다.
import { MText, mathWidth, SANS } from "../draw.jsx";
import { seg, E } from "../core.js";
import { boardScroll } from "../board.js";

/**
 * 글자 판. it 문항 · Lo 배치(boardLayout) · P 박자표(lines[i].a · m? · plan · ans) · t 1배속 ms · cur 지금 줄 · uid 그림 id 꼬리.
 * planTag — 방침 꼬리표 이름(사전식 「숫자 분석」 · 기본 「방침」).
 */
export function Board({ it, Lo, P, t, cur, C, uid = "" }) {
  const T = Lo.T, L = Lo.R.left;
  const qo = seg(t, 0, 600, E.sine);
  const po = seg(t, P.plan[0], P.plan[0] + 600, E.sine);
  const ao = seg(t, P.ans, P.ans + 700, E.sine);
  const id = `bd${uid}-${it.no}-${Lo.R.key}`;
  const q = (
    <g opacity={qo}>
      {Lo.q.map((r, i) => <MText key={i} x={r.x} y={r.y} s={r.s} size={T.q} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />)}
    </g>
  );
  const plan = po > 0 && Lo.plan.length > 0 && (
    <g opacity={po}>
      <rect x={L - 4} y={Lo.planY - Lo.tagZ * 1.05} width={Lo.tagW} height={Lo.tagZ * 1.45} rx={Lo.tagZ * 0.72} fill={C.teal} opacity={0.2} />
      <text x={L - 4 + Lo.tagW / 2} y={Lo.planY - Lo.tagZ * 0.02} fontFamily={SANS} fontSize={Lo.tagZ} fontWeight={800} fill={C.teal} textAnchor="middle">{Lo.tag}</text>
      {Lo.plan.map((p, i) => <MText key={i} x={p.x} y={p.y} s={p.s} size={T.plan} weight={620} fill={C.teal} C={C} />)}
    </g>
  );
  const rows = it.lines.map((ln, i) => {
    const TT = P.lines[i], R = Lo.rows[i];
    if (!TT || t < TT.a) return null;
    const a = seg(t, TT.a, TT.a + 420, E.out);
    const isCur = i === cur;
    const dim = i < cur ? 0.78 : 1;
    const dy = (1 - a) * 12;
    const mk = ln.memo ? (TT.m ? seg(t, TT.m[0], TT.m[1], E.lin) : seg(t, TT.a + 300, TT.a + 1300, E.lin)) : 0;
    const memoW = R.memo ? R.memo.lines.reduce((s, m) => s + m.w, 0) : 0;
    let acc = 0;
    return (
      <g key={i} opacity={a * dim}>
        {isCur && <rect x={R.L - 24} y={R.top + dy} width={6} height={R.bot - R.top} rx={3} fill={C.bar} />}
        {R.pre && <MText x={R.pre.x} y={R.pre.y + dy} s={R.pre.s} size={T.s} weight={600} fill={C.soft} C={C} />}
        {R.parts.map((p, k) => <MText key={k} x={p.x} y={p.y + dy} s={p.s} size={T.b} weight={560} fill={C.ink} C={C} />)}
        {R.memo && mk > 0 && R.memo.lines.map((m, k) => {
          const f0 = acc / memoW; acc += m.w;
          const f = Math.max(0, Math.min(1, (mk - f0) / (m.w / memoW)));
          if (f <= 0) return null;
          return (
            <g key={"m" + k}>
              <clipPath id={`${id}-m${i}-${k}`}><rect x={m.x - 4} y={m.y - T.s * 1.3 + dy} width={(m.w + 12) * f} height={T.s * 1.9} /></clipPath>
              <g clipPath={`url(#${id}-m${i}-${k})`}>
                <MText x={m.x} y={m.y + dy} s={m.s} size={T.s} weight={600} fill={C.red} C={C} />
              </g>
            </g>
          );
        })}
      </g>
    );
  });
  const A = Lo.ans;
  const ans = ao > 0 && (
    <g opacity={ao}>
      <rect x={A.x - 8} y={A.top} width={A.w} height={A.h} rx={T.b * 0.3} fill="none" stroke={C.gold} strokeWidth={3.5} />
      <text x={A.x + T.b * 0.3} y={A.y - T.b * 0.02} fontFamily={SANS} fontSize={T.b * 0.7} fontWeight={800} fill={C.gold}>답</text>
      <MText x={A.x + T.b * 1.7} y={A.y} s={it.ans} size={T.b} weight={700} fill={C.ink} C={C} />
    </g>
  );
  const divider = Lo.two && po > 0 && (
    <line x1={Lo.two.x} y1={Lo.two.top} x2={Lo.two.x} y2={Lo.R.bottom - 6} stroke={C.soft} strokeWidth={2} opacity={0.25 * po} strokeDasharray="6 10" />
  );
  if (!Lo.scroll) return <g>{q}{plan}{divider}{rows}{ans}</g>;
  const S = Lo.scroll, off = boardScroll(Lo, P, t);
  return (
    <g>
      {S.pinQ && q}
      <clipPath id={`${id}-clip`}><rect x={L - 40} y={S.top} width={Lo.R.right - L + 80} height={S.bottom - S.top} /></clipPath>
      <g clipPath={`url(#${id}-clip)`}>
        <g transform={`translate(0 ${-off.toFixed(1)})`}>{!S.pinQ && q}{plan}{rows}{ans}</g>
      </g>
      {off > 2 && (
        <g opacity={Math.min(1, off / 40)}>
          <line x1={L} y1={S.top + 1} x2={Lo.R.right} y2={S.top + 1} stroke={C.soft} strokeWidth={2} opacity={0.35} strokeDasharray="4 8" />
          <path d={`M${L - 31} ${S.top + 24} l9 -14 l9 14 z`} fill={C.soft} opacity={0.7} />
        </g>
      )}
    </g>
  );
}

/**
 * 그림 자리에 그림 넣기. spot = Lo.fig · box = 그림의 제 크기 네모(무대 좌표 — 배율로 줄일 때) · draw(box?) = 그림 그리기.
 * flex 그림(좌표평면)은 배율 없이 네모를 그대로 넘겨 스스로 맞춘다.
 */
export function FigSlot({ spot, box, flex = false, draw }) {
  if (!spot) return null;
  if (flex) return <g>{draw({ x0: spot.x, y0: spot.y, x1: spot.x + spot.w, y1: spot.y + spot.h })}</g>;
  return (
    <g transform={`translate(${spot.x.toFixed(1)} ${spot.y.toFixed(1)}) scale(${spot.s.toFixed(4)}) translate(${(-box.x0).toFixed(1)} ${(-box.y0).toFixed(1)})`}>
      {draw(null)}
    </g>
  );
}

/** 글자 폭 — 판 밖에서 쓸 때(목록 · 판 머리) */
export const textW = (s, z, w = 600) => mathWidth(s, z, w);
