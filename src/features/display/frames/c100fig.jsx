// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 단일 모드의 오른쪽 그림 (frames/c100fig.jsx)
// 판서 줄과 맞물려 움직이는 간단한 그림 셋 — 데이터는 ../cnt100-items.js 의 it.fig (만든 곳: 프로젝트 SRC-…-모니터해설 · figs.py)
//   seats  (한 줄로 세우기) — 자리 칸을 늘어놓고, 고정된 사람(금빛) · 묶음(테두리, 묶음 안 순서는 빨간 글씨) · 빈자리 ∨ ·
//          양 끝을 바꾸는 화살표를 판서 줄에 맞춰 보이며, 식을 쓰는 줄에서 칸마다 가짓수(5 · 4 · 3 …)가 차례로 뜬다.
//          rows[]: { cap, at, units[{ w, lab[], hi?, cnt?, ca?, inner?, gap?, mid? }], cntAt, innerAt, swaps[{ a, b, lab, at }], note?, noteAt }
//   grades (학년별 선발) — 학년마다 학생 점(이름 붙은 학생은 이름까지). 판서 줄이 가리키는 학년 · 학생이 빛난다(hl[줄]).
//   bag    (주머니 공) — 주머니(하나 또는 A · B) 속 공(색 또는 번호). 판서 줄이 가리키는 공이 빛나고 나머지는 흐려진다(hl[줄]).
// at · cntAt … 은 판서 줄 번호 — 그 줄이 써지기 시작하는 시각(l10Plan)에 나타난다.
import { seg, E, clamp } from "../core.js";
import { SANS, mathWidth } from "../draw.jsx";
import { l10Plan, lineAt } from "../lin10.js";
import { seatsPlan, seatsTimes, reelTick, gapTick, SEAT_T } from "../seatwalk.js";

const BOX = { x0: 880, y0: 170, x1: 1540, y1: 850 };
const lineT = (P, i) => (P.lines[clamp(i, 0, P.lines.length - 1)] || { a: 0 }).a;

/* ══════════ 한 줄로 세우기 ══════════ */
export function seatsGeom(f) {
  const rows = f.rows.map((r) => {
    const ws = r.units.map((u) => (u.gap ? 0.5 : u.w));
    const total = ws.reduce((a, b) => a + b, 0) + (r.units.length - 1) * 0.16;
    return { ws, total };
  });
  const S = Math.min(84, Math.floor((BOX.x1 - BOX.x0 - 60) / Math.max(...rows.map((r) => r.total))));
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
        const tick = reelTick(reel.cnt), run = reel.cnt * tick;
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
        const tick = reelTick(reel.cnt), run = reel.cnt * tick, e = t - reel.t0;
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
      const tick = gapTick(a.cnt), run = a.cnt * tick, e = t - a.t0;
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

/* ══════════ 빛남(학년 · 공) — 지금 판서 줄의 상태 ══════════ */
function hlNow(f, P, t) {
  const cur = lineAt(P, t);
  if (cur < 0) return { st: null, k: 0 };
  const i = Math.min(cur, f.hl.length - 1);
  return { st: f.hl[i], k: seg(t, lineT(P, i), lineT(P, i) + 380, E.sine) };
}

/* ══════════ 학년별 선발 ══════════ */
function gradesGeom(f) {
  const ng = f.groups.length;
  const colW = (BOX.x1 - BOX.x0) / ng;
  const maxN = Math.max(...f.groups.map((gp) => (gp.n != null ? gp.n : gp.m + gp.f)));
  const per = maxN > 8 ? 3 : 2;
  const r = Math.min(30, (colW - 40) / (per * 2.4));
  return { ng, colW, maxN, per, r };
}
export function gradesBox(f) {
  const { ng, colW, maxN, per, r } = gradesGeom(f);
  const rowsN = Math.ceil(maxN / per);
  const half = Math.max((per - 1) * r * 1.25 + r + 4, ...f.groups.map((gp) => mathWidth(gp.lab, 38, 800) / 2 + 4));
  const x0 = BOX.x0 + colW / 2 - half, x1 = BOX.x0 + colW * (ng - 0.5) + half;
  const y1 = BOX.y0 + 170 + (rowsN - 1) * r * 2.9 + r + (f.named.length ? 34 : 8);
  return { x0, y0: BOX.y0 + 38, x1, y1 };
}
export function GradesFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it);
  const base = seg(t, 0, 700, E.sine);
  const { st, k } = hlNow(f, P, t);
  const { colW, per, r } = gradesGeom(f);
  const els = [];
  f.groups.forEach((gp, gi) => {
    const cx = BOX.x0 + colW * (gi + 0.5);
    const on = st === "all" || (st && st.g && st.g.includes(gp.key));
    const glow = on ? k : 0;
    els.push(
      <text key={`h${gi}`} x={cx} y={BOX.y0 + 70} fontFamily={SANS} fontSize={38} fontWeight={800} fill={glow > 0.5 ? C.gold : C.ink} textAnchor="middle">{gp.lab}</text>,
      <text key={`n${gi}`} x={cx} y={BOX.y0 + 108} fontFamily={SANS} fontSize={27} fontWeight={600} fill={C.soft} textAnchor="middle">
        {gp.n != null ? `${gp.n}명` : `남 ${gp.m} · 여 ${gp.f}`}
      </text>,
    );
    const kids = gp.n != null ? Array.from({ length: gp.n }, () => (gp.key === "남" ? "남" : gp.key === "여" ? "여" : "")) : [...Array(gp.m).fill("남"), ...Array(gp.f).fill("여")];
    kids.forEach((sx, j) => {
      const row = Math.floor(j / per), col = j % per;
      const x = cx + (col - (per - 1) / 2) * r * 2.5, y = BOX.y0 + 170 + row * r * 2.9;
      const nm = f.named.find((q) => q.g === gp.key && q.i === j);
      const nOn = nm && st && st !== "all" && st.w && st.w.includes(nm.name) ? k : 0;
      const g2 = Math.max(glow * (st === "all" ? 0.55 : 1), nOn);
      els.push(
        <g key={`k${gi}-${j}`}>
          <circle cx={x} cy={y} r={r} fill={C.gold} fillOpacity={0.12 + 0.6 * g2} stroke={g2 > 0.3 ? C.gold : C.soft} strokeWidth={nOn > 0.3 ? 5 : 2.2} />
          {sx && <text x={x} y={y + r * 0.36} fontFamily={SANS} fontSize={r * 0.95} fontWeight={800} fill={C.ink} textAnchor="middle">{sx}</text>}
          {nm && <text x={x} y={y + r + 28} fontFamily={SANS} fontSize={26} fontWeight={nOn > 0.3 ? 800 : 600} fill={nOn > 0.3 ? C.gold : C.soft} textAnchor="middle">{nm.name}</text>}
        </g>,
      );
    });
  });
  return <g opacity={base}>{els}</g>;
}

/* ══════════ 주머니 공 ══════════ */
const BALL = { 빨간: "#E5534B", 파란: "#4C8DF6", 노란: "#F2C230", 흰: "#F7F3E8", 검은: "#2B2B2B", 초록: "#3DBB6B" };

export function bagBox(f) {
  return { x0: BOX.x0 - 4, y0: BOX.y0 + (f.bags.some((b) => b.lab) ? 44 : 90), x1: BOX.x1 + 4, y1: BOX.y1 - 34 };
}

export function BagFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it);
  const base = seg(t, 0, 700, E.sine);
  const { st, k } = hlNow(f, P, t);
  const nb = f.bags.length;
  const bw = (BOX.x1 - BOX.x0 - (nb - 1) * 40) / nb;
  const els = [];
  f.bags.forEach((bg, bi) => {
    const x0 = BOX.x0 + bi * (bw + 40), x1 = x0 + bw;
    const y0 = BOX.y0 + 120, y1 = BOX.y1 - 40;
    const n = bg.balls.length;
    const cols = Math.max(2, Math.ceil(Math.sqrt(n * (bw / (y1 - y0 - 60)))));
    const rowsN = Math.ceil(n / cols);
    const r = Math.min(40, (bw - 120) / cols / 2.25, (y1 - y0 - 150) / rowsN / 2.25);   // 주머니 둥근 옆 · 밑에 걸리지 않게
    const lit = st === "all" ? null : st ? new Set(st[bi] || []) : null;
    els.push(
      <path key={`bag${bi}`} d={`M${x0 + 40} ${y0} Q ${x0 + 6} ${y0 + 40} ${x0 + 8} ${(y0 + y1) / 2} Q ${x0 + 4} ${y1} ${(x0 + x1) / 2} ${y1}
        Q ${x1 - 4} ${y1} ${x1 - 8} ${(y0 + y1) / 2} Q ${x1 - 6} ${y0 + 40} ${x1 - 40} ${y0} Z`} fill={C.soft} fillOpacity={0.08} stroke={C.soft} strokeWidth={3} />,
      <path key={`tie${bi}`} d={`M${x0 + 40} ${y0} Q ${(x0 + x1) / 2} ${y0 - 26} ${x1 - 40} ${y0}`} fill="none" stroke={C.soft} strokeWidth={3} />,
    );
    if (bg.lab) els.push(<text key={`bl${bi}`} x={(x0 + x1) / 2} y={y0 - 44} fontFamily={SANS} fontSize={32} fontWeight={800} fill={C.ink} textAnchor="middle">주머니 {bg.lab}</text>);
    const gw = cols * r * 2.25, gh = rowsN * r * 2.25;
    const gx = (x0 + x1) / 2 - gw / 2 + r * 1.125, gy = Math.max(y0 + 50 + r, (y0 + y1) / 2 - gh / 2 + r * 1.125);   // 주머니 가운데쯤
    bg.balls.forEach((b, j) => {
      const x = gx + (j % cols) * r * 2.25, y = gy + Math.floor(j / cols) * r * 2.25;
      const on = lit && lit.has(j);
      const dim = lit && lit.size && !on ? 1 - 0.6 * k : 1;
      const big = on ? 1 + 0.14 * k : 1;
      const fill = b.c ? BALL[b.c] : "#F4EEDC";          // 번호 공은 밝기와 상관없이 상아색(숫자가 잘 보이게)
      els.push(
        <g key={`b${bi}-${j}`} opacity={dim}>
          <circle cx={x} cy={y} r={r * big} fill={fill} stroke={on ? C.gold : st === "all" ? C.gold : "rgba(0,0,0,.35)"} strokeWidth={on ? 5 : st === "all" ? 2.5 * k : 1.5} />
          {b.n != null && <text x={x} y={y + r * 0.34} fontFamily={SANS} fontSize={r * (b.n >= 10 ? 0.8 : 0.95)} fontWeight={800} fill="#2b2418" textAnchor="middle">{b.n}</text>}
        </g>,
      );
    });
  });
  return <g opacity={base}>{els}</g>;
}
