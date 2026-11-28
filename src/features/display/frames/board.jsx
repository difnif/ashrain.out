// ashrain.out — 해설 액자의 글자 판 그리기 (frames/board.jsx) — 배치는 ../board.js(boardLayout)
// ① 문제 → ② 방침(꼬리표 + 한 줄 · 길면 이어서) → ③ 판서 줄(지금 줄에 금빛 막대 · 빨간 메모가 써지듯) → ④ 답 칸.
// 판서 · 방침 · 답은 칠판에 쓰듯 왼쪽부터 써 내려간다(writeOn — 글자 폭만큼 시간, 쓰는 끝에 분필 점). 문제는 주어진 것이라 그대로 떠오른다.
// 일차함수 10단계 · 경우의 수와 확률 100제 · 기본기 해설(frames/lin10.jsx 의 L10Art)과 그래프와 넓이(frames/area.jsx)가 함께 쓴다.
// 판이 넘쳐 흐르면(Lo.scroll) 방침 · 판서 · 답 칸을 잘라 보이며 위로 올린다 — 문제는 위에 그대로.
// 두 단(Lo.two)이면 두 단 사이에 옅은 세로줄.
// 그림 자리(Lo.fig): FigSlot 이 그림을 그 네모에 넣는다 — 제 크기 그림은 배율로 줄이고(box 제 크기 네모), 좌표평면처럼 스스로 맞추는 그림은 네모를 그대로 넘긴다.
import { MText, mathWidth, SANS } from "../draw.jsx";
import { seg, E } from "../core.js";
import { boardScroll, upOf, dnOf } from "../board.js";

/** 글자 폭만큼 쓰는 시간(ms) — 짧은 줄 0.3초 · 긴 줄 1.1초까지 */
export const writeMs = (w) => Math.max(300, Math.min(1100, 240 + w * 0.5));
/**
 * 써 내려가기 — 조각(segs: { x, y, w, up, dn, el }) 을 차례로 왼쪽부터 드러낸다(f 0 ~ 1 · 폭에 비례해 나눔).
 * 쓰는 동안 끝에 작은 분필 점. id 는 잘라 보이기(clipPath) 이름 머리.
 */
export function WriteOn({ segs, f, id, C, tip = true }) {
  const tot = segs.reduce((a, g) => a + Math.max(1, g.w), 0);
  let acc = 0;
  const out = [];
  segs.forEach((g, k) => {
    const w = Math.max(1, g.w), f0 = acc / tot;
    acc += w;
    const fk = f >= 1 ? 1 : Math.max(0, Math.min(1, (f - f0) / (w / tot)));
    if (fk <= 0) return;
    if (fk >= 1) { out.push(<g key={k}>{g.el}</g>); return; }
    const x1 = g.x - 6 + (g.w + 14) * fk;
    out.push(
      <g key={k}>
        <clipPath id={`${id}-${k}`}><rect x={g.x - 8} y={g.y - g.up - 8} width={Math.max(0, x1 - g.x + 8)} height={g.up + g.dn + 16} /></clipPath>
        <g clipPath={`url(#${id}-${k})`}>{g.el}</g>
        {tip && <circle cx={x1} cy={g.y - g.up * 0.3} r={4.5} fill={C.gold} opacity={0.85} />}
      </g>,
    );
  });
  return <g>{out}</g>;
}

/** 「이름표: 식」의 이름표 길이(콜론까지) — 이름표에 한글이 있고 콜론 뒤가 수식(수가 든)일 때만, 아니면 0 */
export function labelLen(s) {
  const m = /^([^:]*[가-힣][^:]*):\s/.exec(String(s || ""));
  if (!m) return 0;
  const rest = String(s).slice(m[0].length);
  return /\d/.test(rest) && !/[가-힣]{2,}/.test(rest.replace(/\([^)]*\)/g, "")) ? m[1].length + 1 : 0;
}
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
  // 방침 — 꼬리표가 톡 붙고, 방침 글이 써진다
  const planSegs = Lo.plan.map((p, i) => ({ x: p.x, y: p.y, w: mathWidth(p.s, T.plan, 620), up: upOf(p.s, T.plan), dn: dnOf(p.s, T.plan),
    el: <MText key={i} x={p.x} y={p.y} s={p.s} size={T.plan} weight={620} fill={C.teal} C={C} /> }));
  const planW = planSegs.reduce((a, g) => a + g.w, 0);
  const pf = seg(t, P.plan[0] + 180, P.plan[0] + 180 + writeMs(planW), E.lin);
  const tagK = seg(t, P.plan[0], P.plan[0] + 320, E.back);
  const tcx = L - 4 + Lo.tagW / 2, tcy = Lo.planY - Lo.tagZ * 0.32;
  const plan = po > 0 && Lo.plan.length > 0 && (
    <g opacity={Math.min(1, po * 2)}>
      <g transform={`translate(${tcx} ${tcy}) scale(${(0.6 + 0.4 * tagK).toFixed(3)}) translate(${-tcx} ${-tcy})`}>
        <rect x={L - 4} y={Lo.planY - Lo.tagZ * 1.05} width={Lo.tagW} height={Lo.tagZ * 1.45} rx={Lo.tagZ * 0.72} fill={C.teal} opacity={0.2} />
        <text x={L - 4 + Lo.tagW / 2} y={Lo.planY - Lo.tagZ * 0.02} fontFamily={SANS} fontSize={Lo.tagZ} fontWeight={800} fill={C.teal} textAnchor="middle">{Lo.tag}</text>
      </g>
      <WriteOn segs={planSegs} f={pf} id={`${id}-p`} C={C} />
    </g>
  );
  const rows = it.lines.map((ln, i) => {
    const TT = P.lines[i], R = Lo.rows[i];
    if (!TT || t < TT.a) return null;
    const a = seg(t, TT.a, TT.a + 160, E.out);
    const isCur = i === cur;
    const dim = i < cur ? 0.78 : 1;
    const dy = 0;
    const mk = ln.memo ? (TT.m ? seg(t, TT.m[0], TT.m[1], E.lin) : seg(t, TT.a + 300, TT.a + 1300, E.lin)) : 0;
    const memoW = R.memo ? R.memo.lines.reduce((s, m) => s + m.w, 0) : 0;
    let acc = 0;
    // 머리말 → 식 조각을 차례로 써 내려간다
    const segs = [];
    if (R.pre) segs.push({ x: R.pre.x, y: R.pre.y, w: mathWidth(R.pre.s, T.s, 600), up: T.s, dn: T.s * 0.35,
      el: <MText x={R.pre.x} y={R.pre.y} s={R.pre.s} size={T.s} weight={600} fill={C.soft} C={C} /> });
    // 「이름표: 식」 줄(경우의 수 해설 — 「빨간 공 4개 중 2개: 4 × 3 ÷ 2 = 6」)은 이름표를 옅게 — 무엇을 센 식인지 한눈에
    const labN = labelLen(ln.s);
    let off = 0;
    R.parts.forEach((p, k) => {
      const lc = Math.max(0, Math.min(labN - off, p.s.length));
      off += p.s.length + 1;
      const el = lc <= 0 ? <MText key={k} x={p.x} y={p.y} s={p.s} size={T.b} weight={560} fill={C.ink} C={C} />
        : lc >= p.s.length ? <MText key={k} x={p.x} y={p.y} s={p.s} size={T.b} weight={520} fill={C.soft} C={C} />
        : (<g key={k}>
            <MText x={p.x} y={p.y} s={p.s.slice(0, lc)} size={T.b} weight={520} fill={C.soft} C={C} />
            <MText x={p.x + mathWidth(p.s.slice(0, lc), T.b, 520) + T.b * 0.3} y={p.y} s={p.s.slice(lc).trimStart()} size={T.b} weight={560} fill={C.ink} C={C} />
          </g>);
      segs.push({ x: p.x, y: p.y, w: p.w, up: upOf(p.s, T.b), dn: dnOf(p.s, T.b), el });
    });
    const wf = seg(t, TT.a, TT.a + writeMs(segs.reduce((s2, g) => s2 + g.w, 0)), E.lin);
    const barK = seg(t, TT.a, TT.a + 300, E.out);
    return (
      <g key={i} opacity={a * dim}>
        {isCur && <rect x={R.L - 24} y={R.top} width={6} height={Math.max(0, (R.bot - R.top) * barK)} rx={3} fill={C.bar} />}
        <WriteOn segs={segs} f={wf} id={`${id}-w${i}`} C={C} tip={isCur} />
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
  // 답 — 금빛 칸을 한 바퀴 그리고, 「답」이 찍히고, 답을 쓴다
  const boxK = seg(t, P.ans, P.ans + 520, E.io);
  const ansW = mathWidth(it.ans ?? "", T.b, 700);
  const af = seg(t, P.ans + 380, P.ans + 380 + writeMs(ansW), E.lin);
  const ans = ao > 0 && (
    <g opacity={Math.min(1, ao * 2.5)}>
      <rect x={A.x - 8} y={A.top} width={A.w} height={A.h} rx={T.b * 0.3} fill="none" stroke={C.gold} strokeWidth={3.5}
        pathLength={1} strokeDasharray={boxK < 1 ? `${boxK} 1` : undefined} />
      <text x={A.x + T.b * 0.3} y={A.y - T.b * 0.02} fontFamily={SANS} fontSize={T.b * 0.7} fontWeight={800} fill={C.gold}
        opacity={seg(t, P.ans + 200, P.ans + 420, E.out)}>답</text>
      <WriteOn segs={[{ x: A.x + T.b * 1.7, y: A.y, w: ansW, up: upOf(it.ans ?? "", T.b), dn: dnOf(it.ans ?? "", T.b),
        el: <MText x={A.x + T.b * 1.7} y={A.y} s={it.ans} size={T.b} weight={700} fill={C.ink} C={C} /> }]} f={af} id={`${id}-a`} C={C} />
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
