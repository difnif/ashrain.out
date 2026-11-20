// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 단일 모드의 오른쪽 그림 (frames/c100fig.jsx)
// 판서 줄과 맞물려 움직이는 간단한 그림 셋 — 데이터는 ../cnt100-items.js 의 it.fig (만든 곳: 프로젝트 SRC-…-모니터해설 · figs.py)
//   seats  (한 줄로 세우기) — 자리 칸을 늘어놓고, 고정된 사람(금빛) · 묶음(테두리, 묶음 안 순서는 빨간 글씨) · 빈자리 ∨ ·
//          양 끝을 바꾸는 화살표를 판서 줄에 맞춰 보이며, 식을 쓰는 줄에서 칸마다 가짓수(5 · 4 · 3 …)가 차례로 뜬다.
//          rows[]: { cap, at, units[{ w, lab[], hi?, cnt?, ca?, inner?, gap?, mid? }], cntAt, innerAt, swaps[{ a, b, lab, at }], note?, noteAt }
//   grades (학년별 선발) — 학년마다 학생 점(이름 붙은 학생은 이름까지). 판서 줄이 가리키는 학년 · 학생이 빛난다(hl[줄]).
//   bag    (주머니 공) — 주머니(하나 또는 A · B) 속 공(색 또는 번호). 판서 줄이 가리키는 공이 빛나고 나머지는 흐려진다(hl[줄]).
// at · cntAt … 은 판서 줄 번호 — 그 줄이 써지기 시작하는 시각(l10Plan)에 나타난다.
import { seg, E, clamp } from "../core.js";
import { SANS } from "../draw.jsx";
import { l10Plan, lineAt } from "../lin10.js";

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

export function SeatsFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it), G = seatsGeom(f), S = G.S;
  const els = [];
  f.rows.forEach((r, ri) => {
    const g = G.rows[ri];
    const ro = seg(t, lineT(P, r.at), lineT(P, r.at) + 500, E.sine);
    if (ro <= 0) return;
    const y = g.y;
    const parts = [];
    const capY = y - S * 1.25 - (r.swaps.length ? 92 : 0);      // 바꾸는 화살표가 있으면 그 위로
    parts.push(<text key="cap" x={g.x0} y={capY} fontFamily={SANS} fontSize={26} fontWeight={700} fill={C.soft}>{r.cap}</text>);
    let order = 0;
    r.units.forEach((u, ui) => {
      const ux = g.us[ui].x, uw = g.us[ui].w;
      if (u.gap) {
        parts.push(<text key={`g${ui}`} x={ux + uw / 2} y={y + S * 0.12} fontFamily={SANS} fontSize={S * 0.62} fontWeight={800} fill={C.teal} textAnchor="middle">∨</text>);
      } else {
        const seatW = (uw - (u.w - 1) * 4) / u.w;
        for (let k = 0; k < u.w; k++) {
          const sx = ux + k * (seatW + 4);
          const lab = u.lab[k] || "";
          const gold = u.hi || (u.mid && k === 1);
          parts.push(
            <g key={`s${ui}-${k}`}>
              <rect x={sx} y={y - S * 0.5} width={seatW} height={S} rx={8} fill={gold ? C.gold : "none"} fillOpacity={gold ? 0.16 : 0}
                stroke={gold ? C.gold : C.soft} strokeWidth={gold ? 3.5 : 2.2} />
              {lab && <text x={sx + seatW / 2} y={y + S * 0.18} fontFamily={SANS} fontSize={S * 0.46} fontWeight={800} fill={gold ? C.gold : C.ink} textAnchor="middle">{lab}</text>}
            </g>,
          );
        }
        if (u.w > 1) parts.push(<rect key={`b${ui}`} x={ux - 6} y={y - S * 0.5 - 6} width={uw + 12} height={S + 12} rx={14} fill="none" stroke={C.teal} strokeWidth={3} />);
      }
      if (u.cnt != null) {
        const ta = lineT(P, u.ca != null ? u.ca : r.cntAt) + 250 + order * 330;
        order += 1;
        const o = seg(t, ta, ta + 360, E.out);
        if (o > 0) {
          const sc = 0.6 + 0.4 * o;
          parts.push(
            <text key={`c${ui}`} x={ux + uw / 2} y={y - S * 0.68} fontFamily={SANS} fontSize={S * 0.5 * sc} fontWeight={800} fill={C.gold} textAnchor="middle" opacity={o}>{u.cnt}</text>,
          );
        }
      }
      if (u.inner) {
        const ta = lineT(P, r.innerAt) + 600 + order * 330;
        const o = seg(t, ta, ta + 400, E.out);
        if (o > 0) parts.push(<text key={`i${ui}`} x={ux + uw / 2} y={y + S * 0.5 + 34} fontFamily={SANS} fontSize={26} fontWeight={700} fill={C.red} textAnchor="middle" opacity={o}>{u.inner}</text>);
      }
    });
    r.swaps.forEach((sw, si) => {
      const a = g.us[sw.a], b = g.us[sw.b];
      const ta = lineT(P, sw.at) + 200;
      const o = seg(t, ta, ta + 600, E.out);
      if (o <= 0) return;
      const xa = a.x + a.w / 2, xb = b.x + b.w / 2, top = y - S * 0.5 - 16;
      const lift = Math.min(90, 26 + (xb - xa) * 0.18);
      const mx = (xa + xb) / 2;
      parts.push(
        <g key={`w${si}`} opacity={o}>
          <path d={`M${xa} ${top} Q ${mx} ${top - lift * 2} ${xb} ${top}`} fill="none" stroke={C.red} strokeWidth={3} strokeDasharray="8 7" />
          <path d={`M${xa - 9} ${top - 12} L${xa} ${top} L${xa + 11} ${top - 9}`} fill="none" stroke={C.red} strokeWidth={3} />
          <path d={`M${xb - 11} ${top - 9} L${xb} ${top} L${xb + 9} ${top - 12}`} fill="none" stroke={C.red} strokeWidth={3} />
          <text x={mx} y={top - lift - 6} fontFamily={SANS} fontSize={26} fontWeight={800} fill={C.red} textAnchor="middle">× {sw.lab}</text>
        </g>,
      );
    });
    if (r.note) {
      const ta = lineT(P, r.noteAt) + 900;
      const o = seg(t, ta, ta + 500, E.out);
      if (o > 0) parts.push(<text key="note" x={(g.x0 + g.x0 + g.W) / 2} y={y + S * 0.5 + 76} fontFamily={SANS} fontSize={28} fontWeight={800} fill={C.red} textAnchor="middle" opacity={o}>{r.note}</text>);
    }
    els.push(<g key={`r${ri}`} opacity={ro}>{parts}</g>);
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
export function GradesFig({ it, t, C }) {
  const f = it.fig, P = l10Plan(it);
  const base = seg(t, 0, 700, E.sine);
  const { st, k } = hlNow(f, P, t);
  const ng = f.groups.length;
  const colW = (BOX.x1 - BOX.x0) / ng;
  const maxN = Math.max(...f.groups.map((gp) => (gp.n != null ? gp.n : gp.m + gp.f)));
  const per = maxN > 8 ? 3 : 2;
  const r = Math.min(30, (colW - 40) / (per * 2.4));
  const els = [];
  f.groups.forEach((gp, gi) => {
    const cx = BOX.x0 + colW * (gi + 0.5);
    const on = st === "all" || (st && st.g && st.g.includes(gp.key));
    const glow = on ? k : 0;
    els.push(
      <text key={`h${gi}`} x={cx} y={BOX.y0 + 70} fontFamily={SANS} fontSize={38} fontWeight={800} fill={glow > 0.5 ? C.gold : C.ink} textAnchor="middle">{gp.lab}</text>,
      <text key={`n${gi}`} x={cx} y={BOX.y0 + 108} fontFamily={SANS} fontSize={24} fontWeight={600} fill={C.soft} textAnchor="middle">
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
          {nm && <text x={x} y={y + r + 26} fontFamily={SANS} fontSize={22} fontWeight={nOn > 0.3 ? 800 : 600} fill={nOn > 0.3 ? C.gold : C.soft} textAnchor="middle">{nm.name}</text>}
        </g>,
      );
    });
  });
  return <g opacity={base}>{els}</g>;
}

/* ══════════ 주머니 공 ══════════ */
const BALL = { 빨간: "#E5534B", 파란: "#4C8DF6", 노란: "#F2C230", 흰: "#F7F3E8", 검은: "#2B2B2B", 초록: "#3DBB6B" };

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
