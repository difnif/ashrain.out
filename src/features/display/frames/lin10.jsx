// ashrain.out — 교실 모니터 「액자」: 일차함수 10단계 계산 해설 (frames/lin10.jsx)
// 학원 프린트 「일차함수의 그래프 · 세트 1 · 2」(10단계 × 20문항)를 문항마다 한 장면으로 끝없이 돌린다.
//   ① 문제 → ② 방침(한 줄) → ③ 판서: 계산 과정을 한 줄씩(지금 줄에 금빛 막대, 빨간 메모가 줄 뒤에 써지듯) → ④ 답
//   9단계(색칠한 부분의 넓이)는 그림 — 판서 줄에 맞춰 밑변 · 높이 · 나눈 삼각형이 빛난다.
//   경우의 수와 확률 100제(frames/cnt100.jsx)도 이 그리기를 쓴다 — it.planTag 가 있으면 방침 칸 이름을 바꾸고(사전식 「숫자 분석」),
//   it.fig.kind 가 tree(사전식 — 카드로 순번 찾기, frames/lexcards.jsx · 받은 칸에 맞춰 그린다) · seats · grades · bag(줄 세우기 · 학년별 선발 · 주머니 공 — frames/c100fig.jsx)면 그 그림.
//   기본기 해설(frames/basics.jsx — 초등 · 중등 · 고등 단원)도 이 그리기를 쓴다 — it.fig.kind === "dsl" 이면 그림 DSL(frames/figdsl.jsx).
// 글자 판은 ../board.js(배치) · frames/board.jsx(그리기): 글자 크기 두 벌로 고르게, 문제는 판 너비를 다 쓰고,
//   그림은 글자를 다 놓고 남은 빈자리에 줄여 넣는다(화면의 25%까지 · 배율 0.6 아래면 뺀다). region 을 주면(듀얼 반쪽 판) 그 판 안에 같은 규칙으로.
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「세트 1 | 세트 2」 · 빠르기 0.75× ~ 2× · 번호 · 단계 목록(전체 · 1~10단계) · 단일 | 듀얼.
//   7 · 8단계(수직)는 고1 내용이라 표시를 붙인다.
// 계산 · 박자표: ../lin10.js · 문항: ../lin10-items.js
import { memo } from "react";
import { MText, Arrow, Path, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { L10_SETS, L10_STAGE, L10_HIGH, l10Plan, lineAt } from "../lin10.js";
import { stepMarks } from "./scrub.jsx";
import { LessonFrame } from "./lesson.jsx";
import { LexCards, LEX_FIG } from "./lexcards.jsx";
import { SeatsFig, GradesFig, BagFig } from "./c100fig.jsx";
import { FigDsl } from "./figdsl.jsx";

import { boardLayout, STAGE_REGION, PANE_REGION } from "../board.js";
import { Board, FigSlot } from "./board.jsx";
import { seatsBox, gradesBox, bagBox } from "./c100fig.jsx";
import { dslBox } from "./figdsl.jsx";

/* ══════════ 배치 (1600×900) — 글자 판은 ../board.js 가 놓는다 ══════════ */
// 그림은 제 크기(FIG 칸 660 × 680 안에서 실제로 차지하는 네모)로 그린 뒤, 글자를 다 놓고 남은 빈자리에 맞춰 줄여 넣는다.
const FIG = { x0: 880, y0: 170, x1: 1540, y1: 850 };

/** 오른쪽 그림 — 9단계 넓이(kind 없음 · 아래 Figure)와 경우의 수와 확률 100제 · 기본기 해설의 그림들. box = 실제로 차지하는 네모 */
const FIGS = {
  tree: { draw: (p) => <LexCards {...p} />, flex: LEX_FIG },   // 사전식 — 카드로 순번 찾기(받은 칸에 맞춰 그린다)
  seats: { draw: (p) => <SeatsFig {...p} />, box: (f) => seatsBox(f) },
  grades: { draw: (p) => <GradesFig {...p} />, box: (f) => gradesBox(f) },
  bag: { draw: (p) => <BagFig {...p} />, box: (f) => bagBox(f) },
  dsl: { draw: (p) => <FigDsl {...p} />, box: (f) => dslBox(f) },          // 기본기 해설(frames/basics.jsx)
};
const AREA9 = { draw: (p) => <Figure {...p} />, box: (f) => area9Box(f), ts: true };
const figOf = (it) => (it.fig ? FIGS[it.fig.kind] || AREA9 : null);
const NAT = new WeakMap();
/** 그림의 제 크기 네모(무대 좌표) — 없으면 null */
export function figNatural(it) {
  if (!it.fig || figOf(it).flex) return null;
  if (NAT.has(it)) return NAT.get(it);
  const b = figOf(it).box(it.fig);
  const out = b && b.x1 - b.x0 > 20 && b.y1 - b.y0 > 20 ? b : null;
  NAT.set(it, out);
  return out;
}
export const L10_REGION = { stage: STAGE_REGION, pane: PANE_REGION };
/**
 * 글자 판 배치(../board.js). region — 무대 전체(기본) · 듀얼 반쪽 판(PANE_REGION).
 * Lo.fig 가 있으면 그 네모에 그림을, 없으면(noFig) 그림 없이 — 글자가 먼저다.
 */
export function layoutOf(it, region = STAGE_REGION) {
  const F = figOf(it), nb = figNatural(it);
  const Lo = boardLayout(it, region, F?.flex ? F.flex : nb ? { w: nb.x1 - nb.x0, h: nb.y1 - nb.y0 } : null);
  return Lo.noFig != null ? Lo : Object.assign(Lo, { noFig: !Lo.fig });
}

/* ══════════ 9단계 그림 ══════════ */
function figFrame(f) {
  const xs = [0, f.A[0], f.B[0], f.P[0]], ys = [0, f.A[1], f.B[1], f.P[1]];
  const xr = [Math.min(...xs) - 1.6, Math.max(...xs) + 1.6], yr = [Math.min(...ys) - 1.6, Math.max(...ys) + 1.6];
  const s = Math.min((FIG.x1 - FIG.x0) / (xr[1] - xr[0]), (FIG.y1 - FIG.y0) / (yr[1] - yr[0]));
  const cx = (FIG.x0 + FIG.x1) / 2 - s * (xr[0] + xr[1]) / 2, cy = (FIG.y0 + FIG.y1) / 2 + s * (yr[0] + yr[1]) / 2;
  return { s, xr, yr, X: (v) => cx + s * v, Y: (v) => cy - s * v };
}
/** 9단계 그림이 실제로 차지하는 네모 — 축 끝 · 이름 자리까지 */
function area9Box(f) {
  const F = figFrame(f);
  const x0 = F.X(F.xr[0]) - 46, x1 = F.X(F.xr[1]) + 26, y0 = F.Y(F.yr[1]) - 12, y1 = F.Y(F.yr[0]) + 14;
  return { x0: Math.max(FIG.x0 - 20, x0), y0: Math.max(FIG.y0 - 10, y0), x1: Math.min(FIG.x1 + 20, x1), y1: Math.min(FIG.y1 + 10, y1) };
}
/** 두 점을 지나는 직선을 그림 칸으로 자른 두 끝 */
function clipThrough(p, q, xr, yr) {
  const dx = q[0] - p[0], dy = q[1] - p[1];
  let lo = -Infinity, hi = Infinity;
  for (const [d, a, r] of [[dx, p[0], xr], [dy, p[1], yr]]) {
    if (Math.abs(d) < 1e-12) continue;
    const t1 = (r[0] - a) / d, t2 = (r[1] - a) / d;
    lo = Math.max(lo, Math.min(t1, t2)); hi = Math.min(hi, Math.max(t1, t2));
  }
  return [[p[0] + lo * dx, p[1] + lo * dy], [p[0] + hi * dx, p[1] + hi * dy]];
}
const fnum = (v) => (v < 0 ? "−" + -v : String(v));

/** ts — 글자 크기 배수(그림을 줄여 넣을 때 글자는 덜 줄도록) */
function Figure({ it, t, cur, C, ts = 1 }) {
  const f = it.fig, F = figFrame(f), { X, Y } = F;
  const P = l10Plan(it);
  const o = seg(t, 400, 1200, E.sine);
  const xr = [F.xr[0] + 0.3, F.xr[1] - 0.3], yr = [F.yr[0] + 0.3, F.yr[1] - 0.3];
  const lA = clipThrough(f.A, f.P, xr, yr), lB = clipThrough(f.B, f.P, xr, yr);
  const pts = (arr) => arr.map((v) => [X(v[0]), Y(v[1])]);
  const k = (i) => (cur === i ? seg(t, P.lines[i].a, P.lines[i].a + 600, E.sine) : cur > i ? 1 : 0);
  const done = t >= P.ans;
  const glow = (i) => (cur === i ? 1 : 0) * k(i);
  // P 이름: 색칠한 부분의 반대쪽으로
  const gx = f.poly.reduce((a, v) => a + v[0], 0) / f.poly.length, gy = f.poly.reduce((a, v) => a + v[1], 0) / f.poly.length;
  const rt = f.P[0] >= gx, up = f.P[1] >= gy;
  const pTxt = `P(${fnum(f.P[0])}, ${fnum(f.P[1])})`, pZ = 32 * ts, pW = mathWidth(pTxt, pZ, 700) + 8;
  const pBox = [rt ? X(f.P[0]) + 16 : X(f.P[0]) - 16 - pW, Y(f.P[1]) + (up ? -14 - pZ : 14), 0, 0];
  pBox[2] = pBox[0] + pW; pBox[3] = pBox[1] + pZ * 1.12;
  // 높이 글자(X · Y 꼴): 발이 밑변 안이면 색칠한 쪽으로, 밑변 밖이면 바깥쪽으로(삼각형 변과 겹치지 않게)
  const hTag = (() => {
    if (f.kind === "X") {
      const lo = Math.min(f.A[0], f.B[0]), hi2 = Math.max(f.A[0], f.B[0]), x0 = f.P[0];
      const left = x0 < lo ? true : x0 > hi2 ? false : gx < x0 - 0.2;
      return { x: X(x0) + (left ? -14 : 14), y: (Y(f.P[1]) + Y(0)) / 2 + 10, anchor: left ? "end" : "start" };
    }
    if (f.kind === "Y") {
      const lo = Math.min(f.A[1], f.B[1]), hi2 = Math.max(f.A[1], f.B[1]), y0 = f.P[1];
      const below = y0 < lo ? true : y0 > hi2 ? false : gy < y0 - 0.2;
      return { x: (X(f.P[0]) + X(0)) / 2, y: Y(y0) + (below ? 36 : -14), anchor: "middle" };
    }
    return null;
  })();
  const hBox = hTag && (hTag.anchor === "end" ? [hTag.x - 62, hTag.y - 26, hTag.x, hTag.y + 6]
    : hTag.anchor === "start" ? [hTag.x, hTag.y - 26, hTag.x + 62, hTag.y + 6] : [hTag.x - 31, hTag.y - 26, hTag.x + 31, hTag.y + 6]);
  // 절편 숫자 칸
  const xs = f.kind === "X" ? [f.A[0], f.B[0]] : f.kind === "Q" ? [f.B[0]] : [];
  const ys = f.kind === "Y" ? [f.A[1], f.B[1]] : f.kind === "Q" ? [f.A[1]] : [];
  const boxes = [pBox,
    ...xs.map((v) => [X(v) - 26, Y(0) + 10, X(v) + 26, Y(0) + 44]),
    ...ys.map((v) => [X(0) - 64, Y(v) - 18, X(0) - 8, Y(v) + 16]),
    [X(0) - 34, Y(0) + 8, X(0) - 4, Y(0) + 38], ...(hBox ? [hBox] : [])];
  // 직선 이름(ℓ, m): 선을 따라 몇 군데 · 양옆을 놓아 보고, 글자 · 점 · 축 · 다른 직선에서 가장 넉넉한 자리로
  const names = (() => {
    const px = (s2) => s2.map((v) => [X(v[0]), Y(v[1])]);
    const Ls = [px(lA), px(lB)];
    const dRect = (q, r) => Math.hypot(Math.max(r[0] - q[0], 0, q[0] - r[2]), Math.max(r[1] - q[1], 0, q[1] - r[3]));
    const dSeg = (q, [a, b]) => {
      const dx = b[0] - a[0], dy = b[1] - a[1], u = clamp(((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / (dx * dx + dy * dy || 1), 0, 1);
      return Math.hypot(q[0] - a[0] - u * dx, q[1] - a[1] - u * dy);
    };
    const inPoly = (q) => {
      const v = pts(f.poly); let c = false;
      for (let i = 0, j = v.length - 1; i < v.length; j = i++)
        if ((v[i][1] > q[1]) !== (v[j][1] > q[1]) && q[0] < ((v[j][0] - v[i][0]) * (q[1] - v[i][1])) / (v[j][1] - v[i][1]) + v[i][0]) c = !c;
      return c;
    };
    const dots = [f.A, f.B, f.P, [0, 0]].map((v) => [X(v[0]), Y(v[1])]);
    const out = [];
    for (let j = 0; j < 2; j++) {
      const [a0, b0] = Ls[j];
      // P 에서 먼 끝부터 훑는다(같은 점수면 먼 쪽이 이긴다)
      const far = Math.hypot(a0[0] - X(f.P[0]), a0[1] - Y(f.P[1])) > Math.hypot(b0[0] - X(f.P[0]), b0[1] - Y(f.P[1]));
      const [a, b] = far ? [a0, b0] : [b0, a0];
      const dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
      let best = null;
      for (let fr = 0.04; fr <= 0.9; fr += 0.04) for (const sg of [1, -1]) {
        const q = [a[0] + fr * dx + sg * 30 * nx, a[1] + fr * dy + sg * 30 * ny];
        if (q[0] < FIG.x0 + 16 || q[0] > FIG.x1 - 16 || q[1] < FIG.y0 + 20 || q[1] > FIG.y1 - 20) continue;
        let sc = Math.min(
          ...boxes.map((r) => dRect(q, r) - 16),
          ...dots.map((d) => Math.hypot(q[0] - d[0], q[1] - d[1]) - 14),
          ...out.map((o) => Math.hypot(q[0] - o[0], q[1] - o[1]) - 30),
          dSeg(q, Ls[1 - j]) - 14, Math.abs(q[1] - Y(0)) - 18, Math.abs(q[0] - X(0)) - 14, 80);
        if (inPoly(q)) sc -= 20;
        if (!best || sc > best.sc + 0.5) best = { q, sc };
      }
      out.push(best ? best.q : [a[0], a[1]]);
    }
    return out;
  })();
  const name = (q, s) => <MText x={q[0]} y={q[1] + 12 * ts} s={s} size={36 * ts} weight={600} anchor="middle" fill={C.sky} halo={C.halo} C={C} />;
  const O = [0, 0];
  let hi = null;
  if (f.kind === "X" || f.kind === "Y") {
    const foot = f.kind === "X" ? [f.P[0], 0] : [0, f.P[1]];
    hi = (
      <g>
        <Path pts={pts([f.A, f.B])} stroke={C.gold} sw={12} o={0.75 * Math.max(glow(0), done ? 0.5 : 0)} />
        {(cur >= 1 || done) && <Path pts={pts([f.P, foot])} stroke={C.red} sw={4} dash="10 8" o={Math.max(k(1), done ? 1 : 0)} />}
        {(cur >= 1 || done) && (
          <MText x={hTag.x} y={hTag.y} s="높이" size={28 * ts} weight={700} fill={C.red} halo={C.halo} anchor={hTag.anchor} opacity={Math.max(k(1), done ? 1 : 0)} C={C} />
        )}
      </g>
    );
  } else {
    hi = (
      <g>
        <Path pts={pts([O, f.B, f.P])} closed fill={C.coral} fo={0.32} o={Math.max(glow(1), 0)} />
        <Path pts={pts([O, f.A, f.P])} closed fill={C.teal} fo={0.32} o={Math.max(glow(2), 0)} />
        {(cur >= 0 || done) && <Path pts={pts([O, f.P])} stroke={C.red} sw={4} dash="10 8" o={Math.max(cur >= 0 ? k(0) : 0, done ? 1 : 0)} />}
      </g>
    );
  }
  const lbl = (v, axis) => axis === "x"
    ? <MText key={"x" + v} x={X(v)} y={Y(0) + 8 + 30 * ts} s={fnum(v)} size={30 * ts} weight={600} anchor="middle" fill={C.ink} halo={C.halo} C={C} />
    : <MText key={"y" + v} x={X(0) - 14} y={Y(v) + 10 * ts} s={fnum(v)} size={30 * ts} weight={600} anchor="end" fill={C.ink} halo={C.halo} C={C} />;
  const ax = f.kind === "X" ? [lbl(f.A[0], "x"), lbl(f.B[0], "x")] : f.kind === "Y" ? [lbl(f.A[1], "y"), lbl(f.B[1], "y")] : [lbl(f.A[1], "y"), lbl(f.B[0], "x")];
  return (
    <g opacity={o}>
      <Path pts={pts(f.poly)} closed fill={C.gold} fo={0.3} stroke="none" />
      {hi}
      <Arrow p={[X(F.xr[0]), Y(0)]} q={[X(F.xr[1]), Y(0)]} stroke={C.ink} sw={3} h={18} />
      <Arrow p={[X(0), Y(F.yr[0])]} q={[X(0), Y(F.yr[1])]} stroke={C.ink} sw={3} h={18} />
      <text x={X(F.xr[1]) - 6} y={Y(0) + 40} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>x</text>
      <text x={X(0) + 16} y={Y(F.yr[1]) + 22} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>y</text>
      <text x={X(0) - 12} y={Y(0) + 32} fontFamily={SERIF} fontStyle="italic" fontSize={28} fill={C.soft} textAnchor="end">O</text>
      <Path pts={pts(lA)} stroke={C.sky} sw={4.5} />
      <Path pts={pts(lB)} stroke={C.sky} sw={4.5} />
      {name(names[0], "ℓ")}{name(names[1], "m")}
      {[f.A, f.B, f.P].map((v, i) => <circle key={i} cx={X(v[0])} cy={Y(v[1])} r={7} fill={C.ink} />)}
      {ax}
      <MText x={rt ? pBox[0] : pBox[2] - 8} y={pBox[1] + pZ * 0.88} s={pTxt} size={pZ} weight={700} anchor={rt ? "start" : "end"} fill={C.ink} halo={C.halo} C={C} />
    </g>
  );
}

/* ══════════ 한 문항 한 순간 ══════════ */
/** region — 무대 전체(기본) · 듀얼 반쪽 판(PANE_REGION). 글자 판은 Board(frames/board.jsx), 그림은 남은 빈자리에(FigSlot) */
export function L10Art({ it, t, C, uid = "", region = STAGE_REGION }) {
  const P = l10Plan(it), Lo = layoutOf(it, region);
  const cur = lineAt(P, t);
  const F = Lo.fig ? figOf(it) : null;
  return (
    <g>
      <Board it={it} Lo={Lo} P={P} t={t} cur={cur} C={C} uid={uid} />
      {F && F.flex && <FigSlot spot={Lo.fig} flex draw={(box) => F.draw({ it, t, C, cur, box })} />}
      {F && !F.flex && <FigSlot spot={Lo.fig} box={figNatural(it)} draw={() => F.draw({ it, t, C, cur, ts: F.ts ? Math.min(1.3, Math.max(1, 0.95 / Lo.fig.s)) : 1 })} />}
    </g>
  );
}

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function l10Scenes(setKey, sp = 1, stage = 0) {
  const k = `${setKey}|${sp}|${stage}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const S = L10_SETS[setKey];
  const list = S.items.filter((it) => !stage || it.st === stage).map((it) => {
    const title = `일차함수 10단계 · ${S.name}`;
    const sub = `${it.st}단계 ${L10_STAGE[it.st]}${L10_HIGH.has(it.st) ? " (고1)" : ""} · ${it.no}번`;
    return {
      key: `l10-${setKey}-${it.no}`, no: it.no, st: it.st, sub0: it.sub, dur: Math.round(l10Plan(it).dur / sp),
      grp: `${it.st}단계`, marks: stepMarks(l10Plan(it), it.lines, sp), card: `${it.st}단계 · ${it.sub}`,
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} />,
      pane: (t, C, uid) => <L10Art it={it} t={t * sp} C={C} uid={uid} region={PANE_REGION} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 — 조작은 해설 액자 공통 틀(frames/lesson.jsx) ══════════ */
export const L10_SPEC = {
  lsk: "ash.display.lin10", title: "일차함수 10단계 계산 해설", defSet: 1, cols: 5,
  sets: [1, 2].map((k) => ({ key: k, name: L10_SETS[k].name, short: L10_SETS[k].name })),
  stages: () => Array.from({ length: 10 }, (_, i) => i + 1).map((v) => ({
    v, lab: `${v}단계 ${L10_STAGE[v]}${L10_HIGH.has(v) ? " (고1)" : ""}`, chip: `${v}단계${L10_HIGH.has(v) ? "(고1)" : ""}` })),
  scenes: l10Scenes,
};
export function Lin10Frame(props) {
  return <LessonFrame spec={L10_SPEC} {...props} />;
}

/** 액자 목록의 작은 그림 — 세트 1 · 170번(9단계 넓이) 다 푼 순간 */
export const Lin10Thumb = memo(function Lin10Thumb({ C }) {
  const it = L10_SETS[1].items[169];
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="th" />;
});
