// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 단일 모드의 오른쪽 그림 (frames/c100fig.jsx)
// 판서 줄과 맞물려 「세는 방법」이 움직임으로 보이는 그림 셋 — 데이터는 ../cnt100-items.js 의 it.fig (만든 곳: 프로젝트 SRC-…-모니터해설 · figs.py)
//   seats  (한 줄로 세우기 · ../seatwalk.js) — 자리마다 후보가 돌며 1, 2, 3 … 세고 한 사람이 앉아 가짓수가 찍힌다(앉은 사람은 다음 자리에서 빠짐).
//          고정된 사람은 내려앉고, 묶음은 모여 띠로 묶인 뒤 안 순서를 섞어 보이고, 빈자리 ∨ 는 짚어 세고 내려앉고, 양 끝은 자리를 바꿨다 돌아온다.
//          rows[]: { cap, at, units[{ w, lab[], hi?, cnt?, ca?, inner?, gap?, mid? }], cntAt, innerAt, swaps[{ a, b, lab, at }], note?, noteAt }
//   grades (학년별 선발) · bag (주머니 공) — ../pickwalk.js 가 판서 식의 수를 그림의 무리(학년 · 성별 · 색 · 홀짝 · 배수 …)에 맞춰,
//          무리를 짚어 세고(합) · 아래 「뽑은 자리」로 하나씩 뽑아 보내고(곱 — n, n − 1 …) · 순서가 없으면 자리끼리 바꿔 「÷ 2」,
//          적힌 수의 공을 꺼내 늘어놓고(나열) · A · B 공을 잇는다(순서쌍). 맞추지 못한 줄은 그대로 둔다.
// at · cntAt … 은 판서 줄 번호 — 그 줄이 써지기 시작하는 시각(l10Plan)부터 움직인다(줄마다 hold 로 시간을 늘려 둠).
// 개념 설명의 움직이는 예시(../concept-av.js)는 그림 자료에 smax(줄 세우기 칸 크기 상한 — 기본 84) · slow(돌리기 · 짚기 박자 배율 — 기본 1)를 더해 크게 · 천천히 보인다.
import { seg, E, clamp } from "../core.js";
import { SANS, mathWidth } from "../draw.jsx";
import { l10Plan, lineAt } from "../lin10.js";
import { seatsPlan, seatsTimes, reelTickOf, gapTickOf, SEAT_T } from "../seatwalk.js";
import { objectsOf, slotsOf, pickPlan, pickTimes, touchTick, PICK_T } from "../pickwalk.js";

const BOX = { x0: 880, y0: 170, x1: 1540, y1: 850 };
const lineT = (P, i) => (P.lines[clamp(i, 0, P.lines.length - 1)] || { a: 0 }).a;

/* ══════════ 한 줄로 세우기 ══════════ */
export function seatsGeom(f) {
  const rows = f.rows.map((r) => {
    const ws = r.units.map((u) => (u.gap ? 0.5 : u.w));
    const total = ws.reduce((a, b) => a + b, 0) + (r.units.length - 1) * 0.16;
    return { ws, total };
  });
  const S = Math.min(f.smax || 84, Math.floor((BOX.x1 - BOX.x0 - 60) / Math.max(...rows.map((r) => r.total))));   // smax — 칸 크기 상한(개념 설명의 움직이는 예시는 크게)
  const ys = f.rows.length === 1 ? [BOX.y0 + 360] : [BOX.y0 + 240, BOX.y0 + 520];
  const out = rows.map((r, ri) => {
    const W = r.total * S, x0 = (BOX.x0 + BOX.x1) / 2 - W / 2;
    let x = x0;
    const us = r.ws.map((w) => { const u = { x, w: w * S }; x += w * S + 0.16 * S; return u; });
    return { x0, W, y: ys[ri], us };
  });
  return { S, rows: out };
}

/** 그림이 실제로 차지하는 네모(무대 좌표) — 해설 판이 빈자리에 맞춰 줄여 넣을 때(../board.js) */
export function seatsBox(f) {
  const G = seatsGeom(f), S = G.S;
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  f.rows.forEach((r, ri) => {
    const g = G.rows[ri], y = g.y;
    const capY = y - S * 1.25 - (r.swaps.length ? 92 : 0);
    const capW = mathWidth(r.cap || "", 30, 700);
    x0 = Math.min(x0, g.x0 - 10); x1 = Math.max(x1, g.x0 + g.W + 10, g.x0 + capW + 6);
    y0 = Math.min(y0, capY - 30);
    const below = r.note ? 76 + 8 : r.units.some((u) => u.inner) ? 34 + 8 : 8;
    y1 = Math.max(y1, y + S * 0.5 + below);
    if (r.note) { const nw = mathWidth(r.note, 32, 800); x0 = Math.min(x0, g.x0 + g.W / 2 - nw / 2 - 6); x1 = Math.max(x1, g.x0 + g.W / 2 + nw / 2 + 6); }
  });
  return { x0, y0, x1, y1 };
}

/** 사람 글자 — 「남」 + 작은 번호 */
function Who({ x, y, k, size, fill, weight = 800, o = 1 }) {
  if (!k) return null;
  if (k.bundle) return null;
  return (
    <text x={x} y={y} fontFamily={SANS} fontSize={size} fontWeight={weight} fill={fill} textAnchor="middle" opacity={o}>
      {k.lab}{k.i ? <tspan fontSize={size * 0.58} dy={size * 0.18}>{k.i}</tspan> : null}
    </text>
  );
}
const perm = (n, j) => {   // 묶음 안 순서 섞기 — j 번째 모습(돌려 가며)
  const a = Array.from({ length: n }, (_, i) => i);
  for (let r = 0; r < j % n; r++) a.push(a.shift());
  return j % 2 && n > 2 ? [a[1], a[0], ...a.slice(2)] : a;
};

export function SeatsFig({ it, t, C, uid = "" }) {
  const f = it.fig, P = l10Plan(it), G = seatsGeom(f), S = G.S;
  const plan = seatsPlan(it), T = seatsTimes(it, P);
  const els = [];
  f.rows.forEach((r, ri) => {
    const g = G.rows[ri], y = g.y, R = plan.rows[ri];
    const t0r = T.rowAt[ri];
    if (t < t0r) return;
    const ro = seg(t, t0r, t0r + 360, E.out);
    const acts = T.acts.filter((a) => a.ri === ri);
    const actOf = (type, ui) => acts.find((a) => a.type === type && a.ui === ui);
    const parts = [];
    const capY = y - S * 1.25 - (r.swaps.length ? 92 : 0);
    parts.push(<text key="cap" x={g.x0} y={capY} fontFamily={SANS} fontSize={30} fontWeight={700} fill={C.soft} opacity={ro}>{r.cap}</text>);
    // 자리를 바꾸는 움직임(양 끝 × 2) — 그동안 두 칸의 사람이 서로의 자리로 갔다 온다
    const shift = new Map();
    for (const a of acts.filter((x) => x.type === "swap")) {
      const sw = r.swaps[a.si], A = g.us[sw.a], B = g.us[sw.b];
      const k = t < a.t0 ? 0 : t > a.t1 ? 0 : (() => { const u = (t - a.t0) / (a.t1 - a.t0); return u < 0.45 ? E.io(u / 0.45) : u < 0.55 ? 1 : 1 - E.io((u - 0.55) / 0.45); })();
      if (k > 0) {
        // 바꾼 뒤 자리: b 가 맨 앞(A.x)으로, 가운데 칸들은 폭 차이만큼, a 는 뒤쪽 끝으로(묶음 폭이 달라도 칸에 맞게)
        const da = B.x + B.w - A.w - A.x, db = A.x - B.x, lift = Math.min(70, 24 + Math.abs(da) * 0.16);
        shift.set(sw.a, [da * k, -lift * Math.sin(Math.PI * k)]);
        shift.set(sw.b, [db * k, lift * Math.sin(Math.PI * k)]);
        for (let ui = sw.a + 1; ui < sw.b; ui++) shift.set(ui, [(B.w - A.w) * k, 0]);
      }
    }
    const intro = seg(t, T.introAt[ri], T.introAt[ri] + 480, E.lin);
    r.units.forEach((u, ui) => {
      const ux = g.us[ui].x, uw = g.us[ui].w, U = R.units[ui];
      const so = seg(t, t0r + ui * 70, t0r + ui * 70 + 380, E.io);
      if (u.gap) {
        const ga = actOf("gap", ui);
        const filled = ga && t >= ga.t1 - SEAT_T.GAP_DROP;
        parts.push(<text key={`g${ui}`} x={ux + uw / 2} y={y + S * 0.12} fontFamily={SANS} fontSize={S * 0.62} fontWeight={800} fill={C.teal} textAnchor="middle"
          opacity={so * (filled ? 0.25 : 1)}>∨</text>);
        if (filled) {
          const k = seg(t, ga.t1 - SEAT_T.GAP_DROP, ga.t1, E.lin), dy = (1 - Math.max(0, E.back(k))) * -S * 0.9;
          parts.push(
            <g key={`gt${ui}`} transform={`translate(0 ${dy.toFixed(1)})`} opacity={Math.min(1, k * 3)}>
              <rect x={ux + uw / 2 - S * 0.4} y={y - S * 0.42} width={S * 0.8} height={S * 0.84} rx={10} fill={C.sky} fillOpacity={0.14} stroke={C.sky} strokeWidth={2.5} />
              <Who x={ux + uw / 2} y={y + S * 0.17} k={ga.tok} size={S * 0.44} fill={C.ink} />
            </g>,
          );
        }
        return;
      }
      const seatW = (uw - (u.w - 1) * 4) / u.w;
      const gold = u.hi;
      const reel = actOf("reel", ui);
      const settled = U.fixed || U.members ? true : reel ? t >= reel.t1 - SEAT_T.SETTLE : false;
      for (let k = 0; k < u.w; k++) {
        const sx = ux + k * (seatW + 4);
        parts.push(
          <rect key={`s${ui}-${k}`} x={sx} y={y - S * 0.5} width={seatW} height={S} rx={8} fill={gold ? C.gold : settled ? C.sky : "none"}
            fillOpacity={gold ? 0.16 : settled ? 0.08 : 0} stroke={gold ? C.gold : settled ? C.ink : C.soft} strokeWidth={gold ? 3.5 : settled ? 2.6 : 2.2}
            pathLength={so < 1 ? 1 : undefined} strokeDasharray={so < 1 ? `${so} 1` : undefined} />,
        );
      }
      // 묶음 — 따로 서 있던 사람들이 한데 모여 띠로 묶인다 · 묶음 안 순서는 섞어 보인다
      if (U.members) {
        const inner = actOf("inner", ui);
        let order = U.members.map((_, i) => i);
        let mv = null;
        if (inner && t > inner.t0 && t < inner.t1 && !/고정/.test(u.inner)) {
          const n = U.members.length, steps = n === 2 ? 2 : 4, j = Math.min(steps - 1, Math.floor(((t - inner.t0) / (inner.t1 - inner.t0)) * steps));
          const fr = ((t - inner.t0) / (inner.t1 - inner.t0)) * steps - j;
          const from = u.mid ? (j % 2 ? [2, 1, 0] : [0, 1, 2]) : perm(n, j), to = u.mid ? (j % 2 ? [0, 1, 2] : [2, 1, 0]) : perm(n, j + 1);
          order = from; mv = { to, k: E.io(Math.min(1, fr * 1.4)) };
        }
        const spread = (1 - E.out(intro)) * S * 0.55;
        U.members.forEach((m, i) => {
          const slot = order.indexOf(i), slot2 = mv ? mv.to.indexOf(i) : slot;
          const cx0 = ux + slot * (seatW + 4) + seatW / 2, cx1 = ux + slot2 * (seatW + 4) + seatW / 2;
          const cx = cx0 + (cx1 - cx0) * (mv ? mv.k : 0) + (i - (U.members.length - 1) / 2) * spread;
          const hop = mv ? -Math.sin(Math.PI * mv.k) * S * 0.28 * (slot2 > slot ? 1 : -1) : 0;
          const [sx2, sy2] = shift.get(ui) || [0, 0];
          parts.push(<g key={`m${ui}-${i}`} transform={`translate(${sx2.toFixed(1)} ${sy2.toFixed(1)})`}>
            <Who x={cx} y={y + S * 0.17 + hop} k={m} size={S * 0.44} fill={gold || u.mid && i === 1 ? C.gold : C.ink} o={Math.min(1, intro * 2.5)} />
          </g>);
        });
        const band = seg(t, T.introAt[ri] + 260, T.introAt[ri] + 620, E.io);
        const [bx2, by2] = shift.get(ui) || [0, 0];
        if (band > 0) parts.push(<rect key={`b${ui}`} x={ux - 6 + bx2} y={y - S * 0.5 - 6 + by2} width={uw + 12} height={S + 12} rx={14} fill="none" stroke={C.teal} strokeWidth={3}
          pathLength={1} strokeDasharray={band < 1 ? `${band} 1` : undefined} />);
        if (u.inner) {
          const ta = inner ? inner.t1 - 380 : T.introAt[ri] + 800;
          const o = seg(t, ta, ta + 360, E.out);
          if (o > 0) parts.push(<text key={`i${ui}`} x={ux + uw / 2} y={y + S * 0.5 + 34} fontFamily={SANS} fontSize={30 * (0.7 + 0.3 * E.back(o))} fontWeight={800} fill={C.red} textAnchor="middle" opacity={Math.min(1, o * 2)}>{u.inner}</text>);
        }
      } else if (U.fixed) {
        // 고정된 사람 — 위에서 내려앉는다
        const dy = (1 - Math.max(0, E.back(intro))) * -S * 1.1;
        const [sx2, sy2] = shift.get(ui) || [0, 0];
        parts.push(<g key={`f${ui}`} transform={`translate(${sx2.toFixed(1)} ${(dy + sy2).toFixed(1)})`} opacity={Math.min(1, intro * 3)}>
          <Who x={ux + uw / 2} y={y + S * 0.17} k={U.tok} size={S * 0.46} fill={C.gold} />
        </g>);
      } else if (reel && t >= reel.t0) {
        // 후보가 돌며 지나간다(위 수가 1, 2, 3 … 으로 세어진다) → 한 사람이 앉고 가짓수가 찍힌다
        const tick = reelTickOf(reel), run = reel.cnt * tick;
        const seq = reel.ok ? [...reel.cands.filter((k) => k !== reel.pick), reel.pick] : reel.cands;
        const e = t - reel.t0;
        const j = Math.min(reel.cnt - 1, Math.floor(e / tick));
        const fr = e >= run ? 1 : (e - j * tick) / tick;
        const id = `st${uid}-${it.no}-${ri}-${ui}`;
        const roll = e >= run ? 0 : (1 - E.out(Math.min(1, fr * 2.2))) * S * 0.7;
        const [sx2, sy2] = shift.get(ui) || [0, 0];
        const lab = e >= run ? (reel.pick || seq[seq.length - 1]) : seq[j];
        const st = e >= run ? seg(t, reel.t0 + run, reel.t1, E.lin) : 0;
        const sc = e >= run ? 1 + 0.18 * Math.sin(Math.PI * st) : 1;
        parts.push(
          <g key={`r${ui}`} transform={`translate(${sx2.toFixed(1)} ${sy2.toFixed(1)})`}>
            <clipPath id={id}><rect x={ux} y={y - S * 0.5} width={uw} height={S} rx={8} /></clipPath>
            <g clipPath={e < run ? `url(#${id})` : undefined}>
              {e < run && j > 0 && <Who x={ux + uw / 2} y={y + S * 0.17 + roll - S * 0.7} k={seq[j - 1]} size={S * 0.44} fill={C.soft} o={roll / (S * 0.7)} />}
              <g transform={`translate(${ux + uw / 2} ${y}) scale(${sc.toFixed(3)}) translate(${-(ux + uw / 2)} ${-y})`}>
                {lab?.bundle
                  ? <text x={ux + uw / 2} y={y + S * 0.17 + roll} fontFamily={SANS} fontSize={S * 0.4} fontWeight={800} fill={C.teal} textAnchor="middle">{lab.bundle.map((m) => m.lab).join("")}</text>
                  : <Who x={ux + uw / 2} y={y + S * 0.17 + roll} k={lab} size={S * 0.44} fill={e >= run ? C.ink : C.sky} />}
              </g>
            </g>
          </g>,
        );
      }
      // 가짓수 — 세는 동안은 옅게 1, 2, 3 … · 다 세면 금빛으로 찍힌다
      if (reel && t >= reel.t0) {
        const tick = reelTickOf(reel), run = reel.cnt * tick, e = t - reel.t0;
        const n = Math.min(reel.cnt, Math.floor(e / tick) + 1);
        const done = e >= run;
        const pop = done ? seg(t, reel.t0 + run, reel.t0 + run + 260, E.lin) : (e % tick) / tick;
        const sc = done ? 1 + 0.35 * Math.sin(Math.PI * pop) : 1 + 0.12 * (1 - pop);
        parts.push(<text key={`c${ui}`} x={ux + uw / 2} y={y - S * 0.68} fontFamily={SANS} fontSize={S * 0.5 * sc} fontWeight={800}
          fill={done ? C.gold : C.soft} textAnchor="middle">{done ? u.cnt : n}</text>);
      }
    });
    // 빈자리 고르기 — 남은 빈자리를 하나씩 짚어 세고, 그 가운데 하나에 내려앉는다
    for (const a of acts.filter((x) => x.type === "gap")) {
      if (t < a.t0) continue;
      const tick = gapTickOf(a), run = a.cnt * tick, e = t - a.t0;
      const tu = g.us[a.ui];
      if (e < run) {
        const j = Math.min(a.avail.length - 1, Math.floor(e / tick)), q = g.us[a.avail[j]];
        const fr = (e - j * tick) / tick;
        parts.push(<circle key={`gs${a.ui}`} cx={q.x + q.w / 2} cy={y} r={S * (0.42 + 0.08 * Math.sin(Math.PI * fr))} fill={C.gold} fillOpacity={0.14} stroke={C.gold} strokeWidth={3.5} />);
        parts.push(<text key={`gn${a.ui}`} x={q.x + q.w / 2} y={y - S * 0.68} fontFamily={SANS} fontSize={S * 0.46} fontWeight={800} fill={C.soft} textAnchor="middle">{j + 1}</text>);
      } else {
        const pop = seg(t, a.t0 + run, a.t0 + run + 260, E.lin);
        parts.push(<text key={`gc${a.ui}`} x={tu.x + tu.w / 2} y={y - S * 0.68} fontFamily={SANS} fontSize={S * 0.5 * (1 + 0.35 * Math.sin(Math.PI * pop))} fontWeight={800}
          fill={C.gold} textAnchor="middle">{r.units[a.ui].cnt}</text>);
      }
    }
    // 양 끝을 바꾸는 화살표(× 2) — 바꾸는 움직임과 함께 그어진다
    for (const a of acts.filter((x) => x.type === "swap")) {
      const sw = r.swaps[a.si];
      const o = seg(t, a.t0, a.t0 + 500, E.io);
      if (o <= 0) continue;
      const A = g.us[sw.a], B = g.us[sw.b];
      const xa = A.x + A.w / 2, xb = B.x + B.w / 2, top = y - S * 0.5 - 16;
      const lift = Math.min(90, 26 + (xb - xa) * 0.18);
      const mx = (xa + xb) / 2;
      parts.push(
        <g key={`w${a.si}`}>
          <path d={`M${xa} ${top} Q ${mx} ${top - lift * 2} ${xb} ${top}`} fill="none" stroke={C.red} strokeWidth={3} strokeDasharray="8 7" opacity={o} />
          {o >= 1 && <path d={`M${xa - 9} ${top - 12} L${xa} ${top} L${xa + 11} ${top - 9}`} fill="none" stroke={C.red} strokeWidth={3} />}
          {o >= 1 && <path d={`M${xb - 11} ${top - 9} L${xb} ${top} L${xb + 9} ${top - 12}`} fill="none" stroke={C.red} strokeWidth={3} />}
          <text x={mx} y={top - lift - 6} fontFamily={SANS} fontSize={30} fontWeight={800} fill={C.red} textAnchor="middle" opacity={seg(t, a.t1 - 600, a.t1 - 200, E.out)}>× {sw.lab}</text>
        </g>,
      );
    }
    if (r.note) {
      const a = acts.find((x) => x.type === "note");
      const ta = a ? a.t0 : lineT(P, r.noteAt) + 900;
      const o = seg(t, ta, ta + 420, E.lin);
      if (o > 0) parts.push(<text key="note" x={(g.x0 + g.x0 + g.W) / 2} y={y + S * 0.5 + 76} fontFamily={SANS} fontSize={32 * (0.75 + 0.25 * Math.max(0, E.back(o)))} fontWeight={800} fill={C.red} textAnchor="middle" opacity={Math.min(1, o * 2)}>{r.note}</text>);
    }
    els.push(<g key={`r${ri}`}>{parts}</g>);
  });
  return <g>{els}</g>;
}

/* ══════════ 학년별 선발 · 주머니 공 — 짚어 세고 · 자리로 뽑고 · 꺼내 늘어놓기(../pickwalk.js) ══════════ */
const BALL = { 빨간: "#E5534B", 파란: "#4C8DF6", 노란: "#F2C230", 흰: "#F7F3E8", 검은: "#2B2B2B", 초록: "#3DBB6B" };
const TRAY_H = 132;

function gradesGeom(f) {
  const ng = f.groups.length;
  const colW = (BOX.x1 - BOX.x0) / ng;
  const maxN = Math.max(...f.groups.map((gp) => (gp.n != null ? gp.n : gp.m + gp.f)));
  const per = maxN > 8 ? 3 : 2;
  const r = Math.min(30, (colW - 40) / (per * 2.4));
  return { ng, colW, maxN, per, r };
}
/** 그림 자리 — 학생 · 공 하나하나의 자리(objs[j]), 무리 머리, 뽑은 자리 칸(tray) */
const GEO = new WeakMap();
function pickGeom(it) {
  if (GEO.has(it)) return GEO.get(it);
  const f = it.fig, objs = objectsOf(it), nSlot = slotsOf(it);
  const pos = [];
  let heads = [], bags = [], bottom = 0, r0 = 30;
  if (f.kind === "grades") {
    const { colW, per, r } = gradesGeom(f);
    r0 = r;
    let j = 0;
    f.groups.forEach((gp, gi) => {
      const cx = BOX.x0 + colW * (gi + 0.5);
      heads.push({ x: cx, lab: gp.lab, sub: gp.n != null ? `${gp.n}명` : `남 ${gp.m} · 여 ${gp.f}`, key: gp.key });
      const n = gp.n != null ? gp.n : gp.m + gp.f;
      for (let q = 0; q < n; q++, j++) {
        const row = Math.floor(q / per), col = q % per;
        pos[j] = { x: cx + (col - (per - 1) / 2) * r * 2.5, y: BOX.y0 + 170 + row * r * 2.9, r };
        bottom = Math.max(bottom, pos[j].y + r + (objs[j].name ? 34 : 8));
      }
    });
    bottom += 56;                      // 센 수 도장 줄
  } else {
    const nb = f.bags.length, bw = (BOX.x1 - BOX.x0 - (nb - 1) * 40) / nb;
    const yb1 = BOX.y1 - 40 - (nSlot ? TRAY_H : 0);
    let j = 0;
    f.bags.forEach((bg, bi) => {
      const x0 = BOX.x0 + bi * (bw + 40), x1 = x0 + bw, y0 = BOX.y0 + 120, y1 = yb1;
      const n = bg.balls.length;
      const cols = Math.max(2, Math.ceil(Math.sqrt(n * (bw / (y1 - y0 - 60)))));
      const rowsN = Math.ceil(n / cols);
      const r = Math.min(40, (bw - 120) / cols / 2.25, (y1 - y0 - 150) / rowsN / 2.25);
      r0 = Math.min(r0 === 30 ? r : r0, r);
      const gw = cols * r * 2.25, gh = rowsN * r * 2.25;
      const gx = (x0 + x1) / 2 - gw / 2 + r * 1.125, gy = Math.max(y0 + 50 + r, (y0 + y1) / 2 - gh / 2 + r * 1.125);
      for (let q = 0; q < n; q++, j++) pos[j] = { x: gx + (q % cols) * r * 2.25, y: gy + Math.floor(q / cols) * r * 2.25, r };
      bags.push({ x0, x1, y0, y1, lab: bg.lab });
    });
    bottom = yb1;
  }
  let tray = null;
  if (nSlot) {
    const s = Math.min(f.kind === "grades" ? r0 * 2.3 : 76, (BOX.x1 - BOX.x0 - 80) / nSlot - 14);
    const y = (f.kind === "grades" ? bottom + 40 : bottom + 22) + s / 2 + 26;
    const gap = s * 0.28, W = nSlot * s + (nSlot - 1) * gap, x0 = (BOX.x0 + BOX.x1) / 2 - W / 2;
    tray = { y, s, xs: Array.from({ length: nSlot }, (_, i) => x0 + i * (s + gap) + s / 2), x0, W };
    const marks = pickPlan(it).lines.some((L) => L.acts.some((a) => a.div || a.type === "arrange"));
    bottom = y + s / 2 + (marks ? 72 : 14);           // ÷ 2 · × 6 괄호와 글자 자리까지
  }
  const badgeY = f.kind === "grades" ? (tray ? tray.y - tray.s / 2 - 70 : bottom - 30) : bags[0].y0 + 30;
  const out = { objs, pos, heads, bags, tray, bottom, r0, badgeY };
  GEO.set(it, out);
  return out;
}
export function gradesBox(f, it) {
  const { ng, colW, per, r } = gradesGeom(f);
  const half = Math.max((per - 1) * r * 1.25 + r + 4, ...f.groups.map((gp) => mathWidth(gp.lab, 38, 800) / 2 + 4));
  const x0 = BOX.x0 + colW / 2 - half, x1 = BOX.x0 + colW * (ng - 0.5) + half;
  const G = it ? pickGeom(it) : null;
  let y1 = G ? G.bottom : BOX.y0 + 300;
  let X0 = x0, X1 = x1;
  if (G?.tray) { X0 = Math.min(X0, G.tray.x0 - 10); X1 = Math.max(X1, G.tray.x0 + G.tray.W + 10); }
  return { x0: X0, y0: BOX.y0 + 38, x1: X1, y1 };
}
export function bagBox(f, it) {
  const G = it ? pickGeom(it) : null;
  return { x0: BOX.x0 - 4, y0: BOX.y0 + (f.bags.some((b) => b.lab) ? 44 : 90), x1: BOX.x1 + 4, y1: G ? Math.max(G.bottom, BOX.y1 - 34 - (G.tray ? TRAY_H : 0)) : BOX.y1 - 34 };
}

/** 지금 순간의 모습 — 움직임을 처음부터 차례로 되짚어 만든다(시각만으로 정해짐) */
function pickState(it, P, t) {
  const T = pickTimes(it, P), G = pickGeom(it);
  const S = { lit: new Map(), dim: null, spot: null, slots: [], fly: [], ghost: new Set(), badges: [], marks: [], lift: new Map(), pairs: [], back: new Set() };
  let line = -1;
  const reset = () => { S.lit.clear(); S.slots = []; S.ghost.clear(); S.badges = []; S.marks = []; S.lift.clear(); S.pairs = []; S.back.clear(); };
  for (const a of T.acts) {
    if (t < a.t0) break;
    if (a.line !== line) { reset(); line = a.line; }
    const tt = Math.min(t, a.t1), on = t < a.t1;
    if (a.type === "count") {
      const tick = touchTick(a.ids.length) * (a.slow || 1), u0 = a.t0 + PICK_T.POOL;
      const n = tt < u0 ? 0 : Math.min(a.ids.length, Math.floor((tt - u0) / tick) + 1);
      for (let q = 0; q < n; q++) S.lit.set(a.ids[q], 1);
      if (on && n > 0 && tt < u0 + a.ids.length * tick) S.spot = { j: a.ids[n - 1], n, k: ((tt - u0) % tick) / tick };
      if (on) S.dim = new Set(a.ids);
      const done = u0 + a.ids.length * tick;
      if (tt >= done) {
        const ps = a.ids.map((j) => G.pos[j]);
        const top = Math.min(...ps.map((p) => p.y - p.r)), cx = ps.reduce((s2, p) => s2 + p.x, 0) / ps.length;
        S.badges.push({ x: cx, y: it.fig.kind === "grades" ? G.badgeY : top - 24, val: a.val, k: seg(t, done, done + PICK_T.STAMP, E.lin) });
      }
    } else if (a.type === "all") {
      const N = G.objs.length, u = (tt - a.t0) / PICK_T.ALL;
      if (on) G.objs.forEach((o) => { const d = u * 1.4 - (o.j / N) * 0.9; if (d > 0 && d < 0.5) S.lit.set(o.j, Math.sin((d / 0.5) * Math.PI)); });
      S.badges.push({ x: (BOX.x0 + BOX.x1) / 2, y: G.badgeY, val: a.val, k: seg(t, a.t0 + 300, a.t0 + 560, E.lin), all: true });
    } else if (a.type === "pick") {
      if (on) S.dim = new Set(a.pool.ids);
      for (const st of a.steps) {
        if (tt < st.c0) break;
        const avail = a.back ? a.pool.ids : a.pool.ids.filter((j) => !a.got.slice(0, st.q).includes(j));
        const n = Math.min(avail.length, Math.floor((tt - st.c0) / st.tick) + 1);
        const j = a.got[st.q], slot = a.slot0 + st.q;
        if (tt < st.fly) {
          // 남은 후보를 짚어 센다
          const order = [...avail.filter((x) => x !== j), j];
          S.spot = { j: order[n - 1], n, k: ((tt - st.c0) % st.tick) / st.tick };
          for (let q = 0; q < n; q++) S.lit.set(order[q], 0.55);
        } else if (tt < st.fly + PICK_T.FLY) {
          S.fly.push({ j, slot, k: seg(tt, st.fly, st.fly + PICK_T.FLY, E.io), n: st.n });
          if (!a.back) S.ghost.add(j);
        } else {
          S.slots[slot] = { j, n: st.n, k: seg(t, st.fly + PICK_T.FLY, st.end, E.lin) };
          if (!a.back) S.ghost.add(j); else S.back.add(j);
        }
      }
      if (a.un && t >= a.un[0]) {
        const u = seg(t, a.un[0], a.un[1], E.lin);
        S.marks.push({ type: "div", from: a.slot0, to: a.slot0 + a.k - 1, d: a.div, u, k: seg(t, a.un[1] - 380, a.un[1], E.out) });
      }
    } else if (a.type === "arrange") {
      const u = seg(t, a.t0, a.t1, E.lin);
      const k = S.slots.filter(Boolean).length;
      S.marks.push({ type: "arr", from: 0, to: k - 1, d: [1, 1, 2, 6, 24, 120][k] || k, u, k: seg(t, a.t1 - 380, a.t1, E.out) });
    } else if (a.type === "clear") {
      const u = seg(t, a.t0, a.t1, E.io);
      if (u >= 1) { S.slots = []; S.ghost.clear(); S.marks = []; S.lit.clear(); S.back.clear(); }
      else S.fade = 1 - u;
      S.sign = { s: a.sign > 0 ? "+" : "−", k: on ? Math.sin(Math.PI * u) : 0 };
    } else if (a.type === "list") {
      a.ids.forEach((j, q) => { const t0 = a.t0 + q * PICK_T.LIST; if (tt >= t0) { S.lift.set(j, seg(t, t0, t0 + 260, E.back)); S.lit.set(j, 1); } });
      const n = Math.min(a.ids.length, Math.floor((tt - a.t0) / PICK_T.LIST) + 1);
      const last = G.pos[a.ids[n - 1]];
      if (on && n > 0) S.spot = { j: a.ids[n - 1], n, k: ((tt - a.t0) % PICK_T.LIST) / PICK_T.LIST, lift: true };
      const done = a.t0 + a.ids.length * PICK_T.LIST;
      if (tt >= done && last) S.badges.push({ x: (G.bags[0].x0 + G.bags[G.bags.length - 1].x1) / 2, y: G.badgeY, val: `${a.ids.length}개`, k: seg(t, done, done + PICK_T.STAMP, E.lin), all: true });
    } else if (a.type === "pairs") {
      a.pairs.forEach((pr, q) => { const t0 = a.t0 + q * PICK_T.PAIR; if (tt >= t0) { S.pairs.push({ pr, k: seg(t, t0, t0 + 300, E.io) }); S.lit.set(pr[0], 1); S.lit.set(pr[1], 1); } });
      const done = a.t0 + a.pairs.length * PICK_T.PAIR;
      if (tt >= done) S.badges.push({ x: (BOX.x0 + BOX.x1) / 2, y: G.badgeY, val: `${a.pairs.length}가지`, k: seg(t, done, done + PICK_T.STAMP, E.lin), all: true });
    }
  }
  return S;
}

/** 학생 · 공 하나 */
function Obj({ it, o, x, y, r, C, lit = 0, dim = 1, ghost = false, sc = 1 }) {
  if (ghost) return <circle cx={x} cy={y} r={r} fill="none" stroke={C.soft} strokeWidth={2} strokeDasharray="5 6" opacity={0.55} />;
  if (it.fig.kind === "grades") {
    return (
      <g opacity={dim}>
        <circle cx={x} cy={y} r={r * sc} fill={C.gold} fillOpacity={0.12 + 0.6 * lit} stroke={lit > 0.3 ? C.gold : C.soft} strokeWidth={lit > 0.3 ? 4 : 2.2} />
        {o.sx && <text x={x} y={y + r * 0.36 * sc} fontFamily={SANS} fontSize={r * 0.95 * sc} fontWeight={800} fill={C.ink} textAnchor="middle">{o.sx}</text>}
        {o.name && <text x={x} y={y + r + 28} fontFamily={SANS} fontSize={26} fontWeight={lit > 0.3 ? 800 : 600} fill={lit > 0.3 ? C.gold : C.soft} textAnchor="middle">{o.name}</text>}
      </g>
    );
  }
  const fill = o.c ? BALL[o.c] : "#F4EEDC";
  const darkOnDark = o.c === "검은" && C.name === "dark";      // 남색 종이 위 검은 공 — 테두리를 밝게 해 보이게
  return (
    <g opacity={dim}>
      <circle cx={x} cy={y} r={r * sc} fill={fill} stroke={lit > 0.3 ? C.gold : darkOnDark ? C.soft : "rgba(0,0,0,.35)"} strokeWidth={lit > 0.3 ? 5 : darkOnDark ? 2.4 : 1.5} />
      {o.n != null && <text x={x} y={y + r * 0.34 * sc} fontFamily={SANS} fontSize={r * (o.n >= 10 ? 0.8 : 0.95) * sc} fontWeight={800} fill="#2b2418" textAnchor="middle">{o.n}</text>}
    </g>
  );
}

/** 순서 없음 · 자리 정하기 도장 글 — 공식을 펼쳐서: 2명이면 「÷ 2」, 3명 이상이면 「÷ (3 × 2 × 1)」 · 「× (3 × 2 × 1)」 */
const FACTS = { 2: 2, 3: 6, 4: 24, 5: 120 };
function markText(m) {
  const k = m.to - m.from + 1;
  const sym = m.type === "div" ? "÷" : "×";
  if (k >= 3 && FACTS[k] === m.d) return `${sym} (${Array.from({ length: k }, (_, q) => k - q).join(" × ")})`;
  if (k === 2 && m.d === 2 && m.type !== "div") return `${sym} (2 × 1)`;
  return `${sym} ${m.d}`;
}
function PickFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it), G = pickGeom(it);
  const base = seg(t, 0, 700, E.sine);
  const S = pickState(it, P, t);
  const els = [];
  // 무리 머리 · 주머니
  if (f.kind === "grades") {
    G.heads.forEach((h, gi) => {
      const on = [...S.lit.keys()].some((j) => G.objs[j].g === h.key && S.lit.get(j) > 0.3);
      els.push(<text key={`h${gi}`} x={h.x} y={BOX.y0 + 70} fontFamily={SANS} fontSize={38} fontWeight={800} fill={on ? C.gold : C.ink} textAnchor="middle">{h.lab}</text>,
        <text key={`n${gi}`} x={h.x} y={BOX.y0 + 108} fontFamily={SANS} fontSize={27} fontWeight={600} fill={C.soft} textAnchor="middle">{h.sub}</text>);
    });
  } else {
    G.bags.forEach((b, bi) => {
      const { x0, x1, y0, y1 } = b;
      els.push(
        <path key={`bag${bi}`} d={`M${x0 + 40} ${y0} Q ${x0 + 6} ${y0 + 40} ${x0 + 8} ${(y0 + y1) / 2} Q ${x0 + 4} ${y1} ${(x0 + x1) / 2} ${y1}
          Q ${x1 - 4} ${y1} ${x1 - 8} ${(y0 + y1) / 2} Q ${x1 - 6} ${y0 + 40} ${x1 - 40} ${y0} Z`} fill={C.soft} fillOpacity={0.08} stroke={C.soft} strokeWidth={3} />,
        <path key={`tie${bi}`} d={`M${x0 + 40} ${y0} Q ${(x0 + x1) / 2} ${y0 - 26} ${x1 - 40} ${y0}`} fill="none" stroke={C.soft} strokeWidth={3} />,
      );
      if (b.lab) els.push(<text key={`bl${bi}`} x={(x0 + x1) / 2} y={y0 - 44} fontFamily={SANS} fontSize={32} fontWeight={800} fill={C.ink} textAnchor="middle">주머니 {b.lab}</text>);
    });
  }
  // 뽑은 자리 칸
  const T2 = G.tray;
  if (T2) {
    const used = S.slots.some(Boolean) || S.fly.length;
    T2.xs.forEach((x, i) => els.push(<rect key={`sl${i}`} x={x - T2.s / 2} y={T2.y - T2.s / 2} width={T2.s} height={T2.s} rx={12} fill="none"
      stroke={C.soft} strokeWidth={2.2} strokeDasharray="7 7" opacity={used ? 0.9 : 0.4} />));
  }
  // 순서쌍 선
  S.pairs.forEach(({ pr, k }, q) => {
    const a = G.pos[pr[0]], b = G.pos[pr[1]];
    const ay = a.y - (S.lift.get(pr[0]) || 0) * a.r * 0.6, by = b.y - (S.lift.get(pr[1]) || 0) * b.r * 0.6;
    els.push(<line key={`pr${q}`} x1={a.x} y1={ay} x2={a.x + (b.x - a.x) * k} y2={ay + (by - ay) * k} stroke={C.gold} strokeWidth={3.5} opacity={0.85} />);
  });
  // 학생 · 공
  G.objs.forEach((o) => {
    const p = G.pos[o.j];
    const lit = S.lit.get(o.j) || 0;
    const dim = S.dim && !S.dim.has(o.j) ? 0.3 : 1;
    const lift = (S.lift.get(o.j) || 0) * p.r * 0.6;
    if (S.ghost.has(o.j)) { els.push(<g key={`o${o.j}`}><Obj it={it} o={o} x={p.x} y={p.y} r={p.r} C={C} ghost /></g>); return; }
    els.push(<g key={`o${o.j}`}><Obj it={it} o={o} x={p.x} y={p.y - lift} r={p.r} C={C} lit={lit} dim={dim * (S.fade != null && S.back.has(o.j) ? 1 : 1)} /></g>);
  });
  // 짚는 손(금빛 고리) — 세는 수가 옆에
  if (S.spot) {
    const p = G.pos[S.spot.j], lift = S.spot.lift ? (S.lift.get(S.spot.j) || 0) * p.r * 0.6 : 0;
    const rr = p.r * (1.32 + 0.12 * Math.sin(Math.PI * S.spot.k));
    els.push(<circle key="spot" cx={p.x} cy={p.y - lift} r={rr} fill="none" stroke={C.gold} strokeWidth={4} />,
      <text key="spotn" x={p.x + p.r * 0.95} y={p.y - lift - p.r * 0.95} fontFamily={SANS} fontSize={Math.max(36, p.r * 1.15)} fontWeight={800} fill={C.gold} textAnchor="middle" stroke={C.halo} strokeWidth={5} paintOrder="stroke">{S.spot.n}</text>);
  }
  // 자리로 날아가는 것 · 자리에 앉은 것
  const slotObj = (j, x, y, sc, key, o2 = 1) => {
    const o = G.objs[j], r = Math.min(G.pos[j].r, T2.s * 0.4);
    return <g key={key} opacity={o2}><Obj it={it} o={o} x={x} y={y} r={r} C={C} lit={0.35} sc={sc} /></g>;
  };
  const slotX = (i) => {
    // 순서 없음(÷) · 자리 정하기(×): 자리끼리 바꿔 보이기
    for (const m of S.marks) {
      if (i < m.from || i > m.to || m.u <= 0 || m.u >= 1) continue;
      const n = m.to - m.from + 1, ph = m.u * (n === 2 ? 2 : 3);
      const step = Math.floor(ph), fr = E.io(ph - step);
      const cyc = (q) => m.from + ((i - m.from + q) % n);
      const a = T2.xs[cyc(step)], b = T2.xs[cyc(step + 1)];
      return { x: a + (b - a) * fr, dy: -Math.sin(Math.PI * fr) * T2.s * 0.35 * (((i - m.from) % 2) ? 1 : -1) };
    }
    return { x: T2.xs[i], dy: 0 };
  };
  if (T2) {
    S.slots.forEach((s2, i) => {
      if (!s2) return;
      const { x, dy } = slotX(i);
      els.push(slotObj(s2.j, x, T2.y + dy, 1 + 0.12 * Math.sin(Math.PI * s2.k), `ss${i}`, S.fade != null ? S.fade : 1));
      els.push(<text key={`sn${i}`} x={T2.xs[i]} y={T2.y - T2.s / 2 - 10} fontFamily={SANS} fontSize={34 * (1 + 0.3 * Math.sin(Math.PI * s2.k))} fontWeight={800}
        fill={C.gold} textAnchor="middle" opacity={S.fade != null ? S.fade : 1}>{s2.n}</text>);
    });
    S.fly.forEach((fl, q) => {
      const p = G.pos[fl.j], x1 = T2.xs[fl.slot], y1 = T2.y;
      const x = p.x + (x1 - p.x) * fl.k, y = p.y + (y1 - p.y) * fl.k - Math.sin(Math.PI * fl.k) * 70;
      els.push(slotObj(fl.j, x, y, 1.08, `fl${q}`));
    });
    for (const m of S.marks) {
      if (m.k <= 0) continue;
      const xa = T2.xs[m.from] - T2.s / 2, xb = T2.xs[m.to] + T2.s / 2, yb = T2.y + T2.s / 2 + 10;
      const col = m.type === "div" ? C.red : C.gold;
      els.push(<g key={`mk${m.from}${m.type}`} opacity={(S.fade != null ? S.fade : 1) * Math.min(1, m.k * 2)}>
        <path d={`M${xa} ${yb} q 0 14 14 14 L ${xb - 14} ${yb + 14} q 14 0 14 -14`} fill="none" stroke={col} strokeWidth={3} />
        <text x={(xa + xb) / 2} y={yb + 52} fontFamily={SANS} fontSize={34 * (0.75 + 0.25 * Math.max(0, E.back(m.k)))} fontWeight={800} fill={col} textAnchor="middle">{markText(m)}</text>
      </g>);
    }
    if (S.sign && S.sign.k > 0) els.push(<text key="sign" x={T2.x0 - 34} y={T2.y + 14} fontFamily={SANS} fontSize={54} fontWeight={800} fill={S.sign.s === "−" ? C.red : C.gold} textAnchor="middle" opacity={S.sign.k}>{S.sign.s}</text>);
  }
  // 센 수 도장
  S.badges.forEach((b, q) => {
    if (b.k <= 0) return;
    const sc = 0.7 + 0.3 * Math.max(0, E.back(b.k));
    els.push(<g key={`bd${q}`} transform={`translate(${b.x} ${b.y}) scale(${sc.toFixed(3)})`} opacity={Math.min(1, b.k * 2)}>
      <rect x={-34 - String(b.val).length * 8} y={-30} width={68 + String(b.val).length * 16} height={46} rx={23} fill={C.gold} fillOpacity={0.18} stroke={C.gold} strokeWidth={2.5} />
      <text x={0} y={4} fontFamily={SANS} fontSize={32} fontWeight={800} fill={C.gold} textAnchor="middle">{b.all ? b.val : b.val}</text>
    </g>);
  });
  return <g opacity={base}>{els}</g>;
}
export const GradesFig = PickFig;
export const BagFig = PickFig;
