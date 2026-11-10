// ashrain.out — 교실 모니터 「액자」: 일차함수 10단계 계산 해설 (frames/lin10.jsx)
// 학원 프린트 「일차함수의 그래프 · 세트 1 · 2」(10단계 × 20문항)를 문항마다 한 장면으로 끝없이 돌린다.
//   ① 문제 → ② 방침(한 줄) → ③ 판서: 계산 과정을 한 줄씩(지금 줄에 금빛 막대, 빨간 메모가 줄 뒤에 써지듯) → ④ 답
//   9단계(색칠한 부분의 넓이)는 오른쪽에 그림 — 판서 줄에 맞춰 밑변 · 높이 · 나눈 삼각형이 빛난다.
// 재생기는 장면 묶음과 같은 StoryPlayer. 이 액자만의 것: 「세트 1 | 세트 2」 · 「1× | 1.5×」 · 번호 목록(L) — 목록 위
//   단계 칩(전체 · 1~10)으로 고르면 그 단계 20문항만 돈다. 7 · 8단계(수직)는 고1 내용이라 표시를 붙인다.
// 계산 · 박자표: ../lin10.js · 문항: ../lin10-items.js
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { MText, Arrow, Path, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { L10_SETS, L10_SPEEDS, L10_STAGE, L10_HIGH, l10Plan, lineAt } from "../lin10.js";
import { StoryPlayer } from "./player.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";

/* ══════════ 배치 (1600×900) ══════════ */
const LEFT = 60, TOP = 168, BOTTOM = 866;
const FIG = { x0: 880, y0: 170, x1: 1540, y1: 850 };

function wrap(s, size, maxW, weight = 560) {
  const words = String(s).split(/(?<= )/), lines = [""];
  for (const w of words) {
    const cur = lines[lines.length - 1];
    if (cur && mathWidth(cur + w, size, weight) > maxW) lines.push(w); else lines[lines.length - 1] = cur + w;
  }
  return lines.map((l) => l.trimEnd());
}

const LAYOUT = new WeakMap();
export const L10_BOX = { LEFT, TOP, BOTTOM, FIG };
export function layoutOf(it) {
  if (LAYOUT.has(it)) return LAYOUT.get(it);
  const right = it.fig ? FIG.x0 - 50 : 1540;
  const W0 = right - LEFT;
  let best = null;
  for (const [qs, bs] of [[38, 44], [36, 40], [34, 37], [32, 34], [30, 31], [28, 28]]) {
    const qLines = wrap(`${it.no}. ${it.q}`, qs, W0);
    let y = TOP + qs;
    const qY = qLines.map((_, i) => y + i * qs * 1.48);
    y = qY[qY.length - 1] + qs * 1.55;
    const planY = y;
    y += bs * 1.55;
    const ps = Math.round(bs * 0.66), ms = Math.round(bs * 0.62), lh = bs * 1.5;
    const rows = [];
    let ok = true;
    it.lines.forEach((ln, i) => {
      const preW = ln.pre ? mathWidth(ln.pre, ps, 600) + ps * 0.9 : 0;
      const sW = mathWidth(ln.s, bs, 560);
      const memoW = ln.memo ? mathWidth(ln.memo, ms, 600) + ms * 1.2 : 0;
      const r = { i, preRow: false, memoRow: false };
      if (preW + sW > W0) { r.preRow = true; r.preY = y + ps * 0.2; y += ps * 1.35; }
      r.y = y + bs * 0.35;
      r.sx = LEFT + (r.preRow ? 0 : preW);
      r.sW = sW;
      if (sW + (r.preRow ? 0 : preW) > W0) ok = false;
      if (ln.memo) {
        if (r.sx + sW + memoW <= right) { r.mx = r.sx + sW + ms * 1.2; r.my = r.y; }
        else { r.memoRow = true; r.mx = r.sx + bs * 0.4; r.my = r.y + ms * 1.5; y += ms * 1.4; }
      }
      y += lh;
      r.bottom = y;
      rows.push(r);
    });
    const ansY = y + bs * 0.55;
    const cand = { qs, bs, ps, ms, qLines, qY, planY, rows, ansY, right };
    best = cand;
    if (ok && ansY + bs * 0.75 <= BOTTOM) break;
  }
  LAYOUT.set(it, best);
  return best;
}

/* ══════════ 9단계 그림 ══════════ */
function figFrame(f) {
  const xs = [0, f.A[0], f.B[0], f.P[0]], ys = [0, f.A[1], f.B[1], f.P[1]];
  const xr = [Math.min(...xs) - 1.6, Math.max(...xs) + 1.6], yr = [Math.min(...ys) - 1.6, Math.max(...ys) + 1.6];
  const s = Math.min((FIG.x1 - FIG.x0) / (xr[1] - xr[0]), (FIG.y1 - FIG.y0) / (yr[1] - yr[0]));
  const cx = (FIG.x0 + FIG.x1) / 2 - s * (xr[0] + xr[1]) / 2, cy = (FIG.y0 + FIG.y1) / 2 + s * (yr[0] + yr[1]) / 2;
  return { s, xr, yr, X: (v) => cx + s * v, Y: (v) => cy - s * v };
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

function Figure({ it, t, cur, C }) {
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
  const pTxt = `P(${fnum(f.P[0])}, ${fnum(f.P[1])})`, pW = mathWidth(pTxt, 32, 700) + 8;
  const pBox = [rt ? X(f.P[0]) + 16 : X(f.P[0]) - 16 - pW, Y(f.P[1]) + (up ? -46 : 14), 0, 0];
  pBox[2] = pBox[0] + pW; pBox[3] = pBox[1] + 36;
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
  const name = (q, s) => <MText x={q[0]} y={q[1] + 12} s={s} size={36} weight={600} anchor="middle" fill={C.sky} halo={C.halo} C={C} />;
  const O = [0, 0];
  let hi = null;
  if (f.kind === "X" || f.kind === "Y") {
    const foot = f.kind === "X" ? [f.P[0], 0] : [0, f.P[1]];
    hi = (
      <g>
        <Path pts={pts([f.A, f.B])} stroke={C.gold} sw={12} o={0.75 * Math.max(glow(0), done ? 0.5 : 0)} />
        {(cur >= 1 || done) && <Path pts={pts([f.P, foot])} stroke={C.red} sw={4} dash="10 8" o={Math.max(k(1), done ? 1 : 0)} />}
        {(cur >= 1 || done) && (
          <MText x={hTag.x} y={hTag.y} s="높이" size={28} weight={700} fill={C.red} halo={C.halo} anchor={hTag.anchor} opacity={Math.max(k(1), done ? 1 : 0)} C={C} />
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
    ? <MText key={"x" + v} x={X(v)} y={Y(0) + 38} s={fnum(v)} size={30} weight={600} anchor="middle" fill={C.ink} halo={C.halo} C={C} />
    : <MText key={"y" + v} x={X(0) - 14} y={Y(v) + 10} s={fnum(v)} size={30} weight={600} anchor="end" fill={C.ink} halo={C.halo} C={C} />;
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
      <MText x={rt ? pBox[0] : pBox[2] - 8} y={pBox[1] + 28} s={pTxt} size={32} weight={700} anchor={rt ? "start" : "end"} fill={C.ink} halo={C.halo} C={C} />
    </g>
  );
}

/* ══════════ 한 문항 한 순간 ══════════ */
export function L10Art({ it, t, C, uid = "" }) {
  const P = l10Plan(it), Lo = layoutOf(it);
  const cur = lineAt(P, t);
  const qo = seg(t, 0, 600, E.sine);
  const po = seg(t, P.plan[0], P.plan[0] + 600, E.sine);
  const ans = seg(t, P.ans, P.ans + 700, E.sine);
  const id = `l10${uid}-${it.no}`;
  return (
    <g>
      <g opacity={qo}>
        {Lo.qLines.map((s, i) => <MText key={i} x={LEFT} y={Lo.qY[i]} s={s} size={Lo.qs} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />)}
      </g>
      {po > 0 && (
        <g opacity={po}>
          <rect x={LEFT - 4} y={Lo.planY - Lo.ps * 1.05} width={Lo.ps * 2.9} height={Lo.ps * 1.45} rx={Lo.ps * 0.72} fill={C.teal} opacity={0.2} />
          <text x={LEFT + Lo.ps * 1.41} y={Lo.planY - Lo.ps * 0.02} fontFamily={SANS} fontSize={Lo.ps} fontWeight={800} fill={C.teal} textAnchor="middle">방침</text>
          <MText x={LEFT + Lo.ps * 3.4} y={Lo.planY} s={it.plan} size={Math.round(Lo.ps * 1.12)} weight={600} fill={C.teal} C={C} />
        </g>
      )}
      {it.lines.map((ln, i) => {
        const T = P.lines[i], R = Lo.rows[i];
        if (t < T.a) return null;
        const a = seg(t, T.a, T.a + 420, E.out);
        const isCur = i === cur;
        const dim = i < cur ? 0.78 : 1;
        const dy = (1 - a) * 12;
        const mk = T.m ? seg(t, T.m[0], T.m[1], E.lin) : 0;
        const top = (R.preRow ? R.preY - Lo.ps * 1.05 : R.y - Lo.bs * 0.95) + dy;
        const bot = (R.memoRow ? R.my + Lo.ms * 0.35 : R.y + Lo.bs * 0.3) + dy;
        return (
          <g key={i} opacity={a * dim}>
            {isCur && <rect x={LEFT - 24} y={top} width={6} height={bot - top} rx={3} fill={C.bar} />}
            {ln.pre && <MText x={LEFT} y={(R.preRow ? R.preY : R.y) + dy} s={ln.pre + (R.preRow ? "" : ":")} size={Lo.ps} weight={600} fill={C.soft} C={C} />}
            <MText x={R.sx} y={R.y + dy} s={ln.s} size={Lo.bs} weight={560} fill={C.ink} C={C} />
            {ln.memo && mk > 0 && (
              <g>
                <clipPath id={`${id}-m${i}`}><rect x={R.mx - 4} y={R.my - Lo.ms * 1.3 + dy} width={(mathWidth(ln.memo, Lo.ms, 600) + 12) * mk} height={Lo.ms * 1.8} /></clipPath>
                <g clipPath={`url(#${id}-m${i})`}>
                  <MText x={R.mx} y={R.my + dy} s={ln.memo} size={Lo.ms} weight={600} fill={C.red} C={C} />
                </g>
              </g>
            )}
          </g>
        );
      })}
      {ans > 0 && (() => {
        const w = mathWidth(it.ans, Lo.bs, 700) + Lo.bs * 2.6;
        return (
          <g opacity={ans}>
            <rect x={LEFT - 8} y={Lo.ansY - Lo.bs * 1.05} width={w} height={Lo.bs * 1.5} rx={Lo.bs * 0.3} fill="none" stroke={C.gold} strokeWidth={3.5} />
            <text x={LEFT + Lo.bs * 0.3} y={Lo.ansY - Lo.bs * 0.02} fontFamily={SANS} fontSize={Lo.bs * 0.7} fontWeight={800} fill={C.gold}>답</text>
            <MText x={LEFT + Lo.bs * 1.7} y={Lo.ansY} s={it.ans} size={Lo.bs} weight={700} fill={C.ink} C={C} />
          </g>
        );
      })()}
      {it.fig && <Figure it={it} t={t} cur={cur} C={C} />}
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
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <L10Art it={it} t={t * sp} C={C} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
const LSK = "ash.display.lin10";
const fixSet = (v) => (L10_SETS[v] ? +v : 1);
const fixSp = (v) => (L10_SPEEDS.includes(v) ? v : 1);
const fixSt = (v) => (Number.isInteger(v) && v >= 0 && v <= 10 ? v : 0);

export function Lin10Frame(props) {
  const { ui, poke, inert } = props;
  const { Btn, Ic } = ui;
  const [cfg, setCfg] = useState(() => { const o = lsRead(LSK) || {}; return { set: fixSet(o.set), sp: fixSp(o.sp), st: fixSt(o.st) }; });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg]);
  const [list, setList] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const scenes = useMemo(() => l10Scenes(cfg.set, cfg.sp, cfg.st), [cfg]);
  const pickSet = useCallback((v) => setCfg((c) => ({ ...c, set: fixSet(v) })), []);
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);
  const pickSt = useCallback((v) => setCfg((c) => ({ ...c, st: fixSt(v) })), []);
  useKeys({
    l: () => { setList((v) => !v); poke(); },
    b: () => { pickSet(cfg.set === 1 ? 2 : 1); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => setList(false),
  }, inert);
  const extra = (
    <>
      <span className="dsp-sep" />
      <Seg label="세트" value={cfg.set} options={[[1, "세트 1"], [2, "세트 2"]]} onChange={pickSet} poke={poke} />
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 · 단계 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };
  const label = `일차함수 10단계 계산 해설 · ${L10_SETS[cfg.set].name}${cfg.st ? ` · ${cfg.st}단계` : ""}`;
  return (
    <>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}|${cfg.st}`} list={scenes} lsKey={`${LSK}.${cfg.set}.${cfg.st}`} label={label}
        {...props} inert={inert || list} noMode extra={extra} apiRef={api} onIdx={setCur} />
      {list && <NumList scenes={scenes} cfg={cfg} cur={cur} onPick={pick} onStage={(v) => { pickSt(v); poke(); }} onClose={() => setList(false)} />}
    </>
  );
}

/** 번호 · 단계 목록 — 단계 칩을 고르면 그 단계만 돌고, 번호를 고르면 그 문항부터 */
function NumList({ scenes, cfg, cur, onPick, onStage, onClose }) {
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 · 단계 목록">
        <style>{".l10-grid { grid-template-columns: repeat(5, 1fr); }"}</style>
        <div className="dsp-list-h">
          <b>일차함수 10단계 · {L10_SETS[cfg.set].name}</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <div className="dsp-chips">
          {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((v) => (
            <button key={v} type="button" className={"dsp-chip" + (cfg.st === v ? " on" : "")} aria-pressed={cfg.st === v} onClick={() => onStage(v)}>
              {v ? `${v}단계${L10_HIGH.has(v) ? "(고1)" : ""}` : "전체 200"}
            </button>
          ))}
        </div>
        <p className="dsp-gal-sub">
          {cfg.st ? `${cfg.st}단계 ${L10_STAGE[cfg.st]} 20문항만 돌아요` : "1단계부터 10단계까지 차례로 돌아요"} · 한 바퀴 약 {Math.round(lap / 60000)}분 · 지금 {scenes[cur]?.no}번 · 번호를 고르면 그 문항부터
        </p>
        <div className="dsp-grid l10-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{s.st}단계 · {s.sub0}</span>
              <span className="m">{Math.round(s.dur / 1000)}초</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/** 액자 목록의 작은 그림 — 세트 1 · 170번(9단계 넓이) 다 푼 순간 */
export const Lin10Thumb = memo(function Lin10Thumb({ C }) {
  const it = L10_SETS[1].items[169];
  return <L10Art it={it} t={l10Plan(it).ans + 900} C={C} uid="th" />;
});
