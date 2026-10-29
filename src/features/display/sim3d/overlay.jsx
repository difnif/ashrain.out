// ashrain.out — 교실 모니터 「3D 축구」: 3D 그림 위에 얹는 SVG (sim3d/overlay.jsx)
// 글자는 WebGL 이 아니라 SVG 로 — 어느 해상도에서도 또렷하고, 수식 글자(UText: 분수 · 강조 · 기울인 변수)를 그대로 쓴다.
// 위치는 3D 와 같은 카메라로 계산한다(persp.project). three.js 를 쓰지 않으니 검산 테스트가 Node 에서 그대로 그린다.
//   Labels    선수 머리 위 이름표(등번호 · 이름) — 주인공은 크게, 흐린 선수는 작고 연하게. 겹치면 뒤엣것이 흐려진다.
//   Trail     공이 지나온 자취(빛나는 꼬리)
//   GLine · GDot · GLabel · GRight · GTape   멈춘 경기장 바닥에 그리는 빛나는 선 · 점 · 글자 · 직각 표시 · 줄자
//   Explain   설명 카드 — 화면 전체가 어두워진 위에 큰 글씨(엔진이 어둡게 한다)
//   Lower     다큐 자막(왼쪽 아래) · Tag 재구성 표시 · Title3D 제목
import { Fragment } from "react";
import { project, projectPath, FW, FH, onStage } from "./persp.js";
import { UText, uWidth } from "../kit-story.jsx";
import { PALETTE, SANS, TITLE } from "../draw.jsx";
import { clamp, seg, win, E, polyLen, lerp } from "../core.js";
import { KIT_INK } from "./kits.js";

/** 설명 카드 · 이름표는 테마와 상관없이 어두운 판 색(3D 위에서 읽히게) */
export const DK = PALETTE.dark;
const r1 = (v) => Math.round(v * 10) / 10;
const pathD = (pts) => (pts.length ? "M" + pts.map((p) => `${r1(p[0])} ${r1(p[1])}`).join("L") : "");

/* ══════════ 이름표 ══════════ */
/**
 * world.actors → 머리 위 이름표. main = 주인공(크게, 팀 색 번호 동그라미), 그 밖은 작고 연하게.
 * 겹침: 중요한 것(주인공 → 가까운 것) 먼저 놓고, 앞에 놓인 이름표와 겹친 만큼 흐려진다(시각에 따라 매끄럽게).
 */
export function Labels({ W, o = 1, only, hide }) {
  if (o <= 0.01) return null;
  const cam = W.cam;
  const items = [];
  for (const a of W.actors) {
    if (!a.label || a.o === 0) continue;
    if (only && !only.includes(a.id)) continue;
    if (hide && hide.includes(a.id)) continue;
    const top = 1.9 + (a.pose?.y > 0 ? a.pose.y : 0);
    const s = project(cam, [a.x, top, a.z]);
    if (!s || !onStage(s, 60)) continue;
    const main = a.role === "main";
    const far = main ? 1 : 1 - clamp((s[2] - 24) / 10);          // 흐린 선수 이름표는 멀면(24 m~) 사라진다
    if (far <= 0.02) continue;
    const k = clamp(22 / s[2], 0.72, 1.3);
    const size = (main ? 23 : 15.5) * k;
    const num = a.n != null ? String(a.n) : "";
    const w = main ? (a.name ? size * 1.5 + 8 + uWidth(a.name, size, 750) + size * 0.7 : size * 1.55) : uWidth(`${num} ${a.name || ""}`, size, 650);
    const h = main ? size * 1.55 : size * 1.2;
    items.push({ a, s, size, w, h, main, num, z: s[2], far });
  }
  items.sort((p, q) => (p.main !== q.main ? (p.main ? -1 : 1) : p.z - q.z));
  // 공을 가리지 않게: 공이 이름표 밑에 오면 그만큼 위로 민다(가로로 멀어질수록 덜 — 매끄럽게)
  const bs = W.ball && W.ball.o !== 0 ? project(cam, W.ball.p) : null;
  const br = bs ? Math.max(8, (0.25 * cam.F) / bs[2]) : 0;
  const placed = [];
  const out = [];
  for (const it of items) {
    let lift = 0;
    if (bs) {
      const hx = Math.abs(bs[0] - it.s[0]) - it.w / 2;                      // 이름표 가장자리에서 공까지(가로)
      const wgt = 1 - clamp(hx / 40);
      const need = it.s[1] - 6 - (bs[1] - br - 8);                          // 이름표 아래끝이 공 위로 가야 하는 만큼
      if (wgt > 0 && need > 0 && bs[1] + br > it.s[1] - 6 - it.h - 30) lift = wgt * need;
    }
    const x0 = it.s[0] - it.w / 2, y1 = it.s[1] - 6 - lift, y0 = y1 - it.h;
    let cover = 0;
    for (const p of placed) {
      const ox = Math.max(0, Math.min(x0 + it.w, p.x0 + p.w) - Math.max(x0, p.x0));
      const oy = Math.max(0, Math.min(y1, p.y1) - Math.max(y0, p.y0));
      cover = Math.max(cover, (ox * oy) / (it.w * it.h));
    }
    const fade = it.main ? 1 - clamp((cover - 0.35) * 1.6) * 0.7 : 1 - clamp(cover * 2.2);
    if (fade > 0.03) placed.push({ x0, y0, y1, w: it.w });
    if (fade <= 0.02) continue;
    out.push({ ...it, x0, y0, y1, lift, fade: fade * it.far });
  }
  return (
    <g opacity={o}>
      {out.map(({ a, s, size, w, h, main, num, x0, y0, fade, lift }) => main ? (
        <g key={a.id} opacity={fade}>
          <rect x={x0} y={y0} width={w} height={h} rx={h / 2} fill="rgba(6,10,24,0.66)" stroke="rgba(255,255,255,0.18)" strokeWidth={1} />
          <circle cx={x0 + h / 2} cy={y0 + h / 2} r={h / 2 - 3} fill={KIT_INK[a.kit] || DK.soft} />
          <text x={x0 + h / 2} y={y0 + h / 2 + size * 0.36} fontSize={size * (num.length > 2 ? 0.7 : 0.95)} fontWeight={800} fontFamily={SANS} textAnchor="middle"
            fill={a.kit === "city" ? "#10203c" : "#fff"}>{num}</text>
          <UText x={x0 + h + 4} y={y0 + h / 2 + size * 0.36} s={a.name} size={size} weight={750} fill="#F7F1E1" C={DK} />
          {lift < 4 && <path d={`M${s[0] - 5} ${y0 + h}L${s[0]} ${y0 + h + 6}L${s[0] + 5} ${y0 + h}Z`} fill="rgba(6,10,24,0.66)" />}
        </g>
      ) : (
        <g key={a.id} opacity={fade * 0.92}>
          <UText x={s[0]} y={s[1] - 8 - lift} s={`${num} ${a.name || ""}`.trim()} size={size} weight={650} anchor="middle" fill="#D5DAE2" halo="rgba(8,12,26,0.85)" C={DK} />
        </g>
      ))}
    </g>
  );
}

/* ══════════ 공의 자취 ══════════ */
export function Trail({ W, pts, col = "#FFF6DA", o = 1, sw = 5 }) {
  if (o <= 0.01 || !pts || pts.length < 2) return null;
  const S = projectPath(W.cam, pts);
  if (S.length < 2) return null;
  const n = S.length;
  return (
    <g opacity={o}>
      {S.slice(1).map((p, i) => {
        const k = (i + 1) / (n - 1);
        return <line key={i} x1={r1(S[i][0])} y1={r1(S[i][1])} x2={r1(p[0])} y2={r1(p[1])} stroke={col} strokeWidth={sw * (0.35 + 0.65 * k)}
          strokeOpacity={0.08 + 0.62 * k * k} strokeLinecap="round" />;
      })}
    </g>
  );
}

/* ══════════ 바닥 그림 (멈춘 장면 위) ══════════ */
const G3 = (p, y = 0.03) => (p.length === 3 ? p : [p[0], y, p[1]]);
/** 바닥(또는 공중) 꺾은선 — p 만큼 그려지고, 빛 번짐이 있다. pts 는 [x, z] 또는 [x, y, z] */
export function GLine({ W, pts, col = DK.gold, p = 1, o = 1, sw = 5, dash, glow = true, n = 24 }) {
  if (o <= 0.01 || p <= 0) return null;
  // 원근 때문에 직선도 잘게 나눠 투영한다(가까운 면 자르기가 매끄럽도록)
  const dense = [];
  const P3 = pts.map((q) => G3(q));
  for (let i = 0; i < P3.length - 1; i++) for (let j = 0; j < n; j++) dense.push(P3[i].map((v, c) => lerp(v, P3[i + 1][c], j / n)));
  dense.push(P3.at(-1));
  const part = p >= 1 ? dense : partial3(dense, p);
  const S = projectPath(W.cam, part);
  if (S.length < 2) return null;
  const d = pathD(S);
  return (
    <g opacity={o}>
      {glow && <path d={d} fill="none" stroke={col} strokeWidth={sw * 3.2} strokeOpacity={0.22} strokeLinecap="round" strokeLinejoin="round" />}
      <path d={d} fill="none" stroke={col} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={dash} />
    </g>
  );
}
function partial3(pts, p) {
  let L = 0;
  const seg3 = [];
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1], pts[i][2] - pts[i - 1][2]); seg3.push(d); L += d; }
  let need = L * clamp(p);
  const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (need <= seg3[i - 1]) { const k = seg3[i - 1] ? need / seg3[i - 1] : 0; out.push(pts[i - 1].map((v, c) => lerp(v, pts[i][c], k))); return out; }
    out.push(pts[i]); need -= seg3[i - 1];
  }
  return out;
}
/** 바닥의 점(동그라미) */
export function GDot({ W, p, col = DK.gold, r = 0.45, o = 1, fill = true, sw = 3 }) {
  if (o <= 0.01) return null;
  const ring = [];
  for (let i = 0; i <= 24; i++) { const a = (i / 24) * Math.PI * 2; ring.push([p[0] + r * Math.cos(a), 0.03, p[1] + r * Math.sin(a)]); }
  const S = projectPath(W.cam, ring);
  if (S.length < 3) return null;
  return <path d={pathD(S) + "Z"} fill={fill ? col : "none"} fillOpacity={fill ? 0.85 : 0} stroke={col} strokeWidth={sw} opacity={o} />;
}
/** 세계 점에 붙는 글자(둥근 이름표) */
export function GLabel({ W, p, s, size = 30, col = DK.gold, ink = "#10162a", o = 1, dx = 0, dy = 0, chip = true, weight = 800, y = 0.03 }) {
  if (o <= 0.01) return null;
  const q = project(W.cam, G3(p, y));
  if (!q) return null;
  const x = q[0] + dx, yy = q[1] + dy;
  if (!chip) return <UText x={x} y={yy + size * 0.35} s={s} size={size} weight={weight} anchor="middle" fill={col} halo="rgba(3,6,15,0.9)" opacity={o} C={DK} />;
  const w = uWidth(s, size, weight) + size * 1.0;
  return (
    <g opacity={o}>
      <rect x={x - w / 2} y={yy - size * 0.78} width={w} height={size * 1.56} rx={size * 0.78} fill={col} />
      <UText x={x} y={yy + size * 0.35} s={s} size={size} weight={weight} anchor="middle" fill={ink} C={DK} />
    </g>
  );
}
/** 꺾은선 가운데 옆에 길이 글자 — side 는 화면에서 왼(−1)/오른(+1) 바깥 */
export function GSegLbl({ W, a, b, s, size = 30, col = DK.gold, o = 1, off = 30, side = 1, at = 0.5, chip = false, ink }) {
  const A = project(W.cam, G3(a)), B = project(W.cam, G3(b));
  if (!A || !B || o <= 0.01) return null;
  const mx = lerp(A[0], B[0], at), my = lerp(A[1], B[1], at);
  const dx = B[0] - A[0], dy = B[1] - A[1], L = Math.hypot(dx, dy) || 1;
  const nx = (-dy / L) * side, ny = (dx / L) * side;
  const x = mx + nx * off, y = my + ny * off;
  if (chip) {
    const w = uWidth(s, size, 800) + size;
    return (
      <g opacity={o}>
        <rect x={x - w / 2} y={y - size * 0.78} width={w} height={size * 1.56} rx={size * 0.78} fill={col} />
        <UText x={x} y={y + size * 0.35} s={s} size={size} weight={800} anchor="middle" fill={ink || "#10162a"} C={DK} />
      </g>
    );
  }
  return <UText x={x} y={y + size * 0.35} s={s} size={size} weight={800} anchor="middle" fill={col} halo="rgba(3,6,15,0.92)" opacity={o} C={DK} />;
}
/** 바닥의 직각 표시: V 에서 A·B 쪽으로 s m */
export function GRight({ W, V, A, B, s = 1.2, col = DK.gold, o = 1, sw = 3 }) {
  if (o <= 0.01) return null;
  const u = (P) => { const dx = P[0] - V[0], dz = P[1] - V[1], L = Math.hypot(dx, dz) || 1; return [dx / L, dz / L]; };
  const a = u(A), b = u(B);
  const p1 = [V[0] + a[0] * s, V[1] + a[1] * s], p2 = [V[0] + (a[0] + b[0]) * s, V[1] + (a[1] + b[1]) * s], p3 = [V[0] + b[0] * s, V[1] + b[1] * s];
  const S = projectPath(W.cam, [p1, p2, p3].map((q) => G3(q)));
  if (S.length < 3) return null;
  return <path d={pathD(S)} fill="none" stroke={col} strokeWidth={sw} opacity={o} strokeLinejoin="round" />;
}
/** 줄자 — a 에서 b 로 늘어나며 눈금 수가 커진다(초등) */
export function GTape({ W, a, b, p, s, col = DK.gold, o = 1, size = 30, side = 1, off = 34, unit = " m", total }) {
  if (p <= 0 || o <= 0.01) return null;
  const L = total ?? Math.hypot(b[0] - a[0], b[1] - a[1]);
  const e = [lerp(a[0], b[0], p), lerp(a[1], b[1], p)];
  const read = s && p >= 1 ? s : `${Math.round(L * p * 10) / 10}${unit}`;
  return (
    <g>
      <GLine W={W} pts={[a, e]} col={col} sw={7} o={o} />
      <GLine W={W} pts={[a, e]} col="#10162a" sw={2} dash="2 14" o={o * 0.7} glow={false} />
      <GDot W={W} p={e} col={col} r={0.35} o={o} />
      <GSegLbl W={W} a={a} b={e} s={read} size={size} col={col} o={o} side={side} off={off} at={0.55} chip ink="#10162a" />
    </g>
  );
}

/* ══════════ 설명 카드 ══════════ */
/**
 * 화면이 어두워진 위에 큰 글씨. local = hold 구간 안의 시각(ms), dur = 구간 길이.
 * kicker(작은 머리말) · head(제목) · lines: [{ t(ms, 구간 안), s, size?, c?(색 이름) }] · side: "left" | "right" | "center"
 * 가장 최근 줄이 또렷하고(금빛 막대), 앞 줄은 조금 흐려진다.
 */
export function Explain({ local, dur, kicker, head, lines = [], side = "left", x, y = 200, w = 760, lh = 88, size = 58, hsize = 46, foot }) {
  const o = Math.min(seg(local, 250, 800), 1 - seg(local, dur - 1650, dur - 1250));
  if (o <= 0.005) return null;
  const X = x ?? (side === "right" ? FW - 96 - w : side === "center" ? (FW - w) / 2 : 96);
  const vis = lines.filter((L) => local >= L.t);
  const cur = vis.at(-1);
  const scrim = side === "right"
    ? <rect x={FW * 0.42} y={0} width={FW * 0.58} height={FH} fill="url(#ex-scr-r)" />
    : side === "center" ? <rect x={0} y={0} width={FW} height={FH} fill="rgba(3,6,15,0.28)" />
    : <rect x={0} y={0} width={FW * 0.62} height={FH} fill="url(#ex-scr-l)" />;
  let yy = y + (head ? hsize * 1.75 : 0);
  return (
    <g opacity={o}>
      <defs>
        <linearGradient id="ex-scr-l" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stopColor="#03060f" stopOpacity="0.62" /><stop offset="0.75" stopColor="#03060f" stopOpacity="0.3" /><stop offset="1" stopColor="#03060f" stopOpacity="0" /></linearGradient>
        <linearGradient id="ex-scr-r" x1="1" x2="0" y1="0" y2="0"><stop offset="0" stopColor="#03060f" stopOpacity="0.62" /><stop offset="0.75" stopColor="#03060f" stopOpacity="0.3" /><stop offset="1" stopColor="#03060f" stopOpacity="0" /></linearGradient>
      </defs>
      {scrim}
      {kicker && <g opacity={seg(local, 250, 700)}>
        <rect x={X} y={y - 46} width={46} height={6} rx={3} fill={DK.gold} />
        <text x={X + 60} y={y - 36} fontFamily={SANS} fontSize={26} fontWeight={800} fill={DK.gold} letterSpacing="0.08em">{kicker}</text>
      </g>}
      {head && <g opacity={seg(local, 350, 900)} transform={`translate(0 ${r1((1 - seg(local, 350, 900, E.out)) * 14)})`}>
        <UText x={X} y={y + hsize * 0.82} s={head} size={hsize} weight={800} fill="#F7F1E1" C={DK} />
      </g>}
      {lines.map((L, i) => {
        if (local < L.t) { yy += (L.gap ?? lh); return null; }
        const a = seg(local, L.t, L.t + 420, E.out);
        const isCur = L === cur;
        const sz = L.size || size;
        const yPos = yy + sz * 0.8;
        yy += L.gap ?? lh;
        const col = L.c ? DK[L.c] || L.c : "#F7F1E1";
        const dimK = isCur ? 1 : 1 - 0.38 * seg(local, cur.t, cur.t + 500);
        const anchor = side === "center" ? "middle" : "start";
        const xx = side === "center" ? FW / 2 : X;
        return (
          <g key={i} opacity={a * dimK} transform={`translate(0 ${r1((1 - a) * 18)})`}>
            {isCur && side !== "center" && <rect x={X - 30} y={yPos - sz * 0.86} width={8} height={sz * 1.08} rx={4} fill={DK.gold} />}
            <UText x={xx} y={yPos} s={L.s} size={sz} weight={L.w || 680} anchor={anchor} fill={col} accent={DK.gold} C={DK} />
          </g>
        );
      })}
      {foot && <UText x={side === "center" ? FW / 2 : X} y={FH - 118} s={foot} size={26} weight={600} anchor={side === "center" ? "middle" : "start"} fill="#C9C2B1" opacity={seg(local, 900, 1400)} C={DK} />}
    </g>
  );
}

/* ══════════ 다큐 자막 · 표시 · 제목 ══════════ */
/** 왼쪽 아래 자막: [{ t0, t1, a(작은 줄), b(큰 줄) }] — 화면 시각 t */
export function Lower({ t, items }) {
  const it = items.find((x) => t >= x.t0 && t < x.t1);
  if (!it) return null;
  const o = win(t, it.t0, it.t1, 420, 380);
  const k = seg(t, it.t0, it.t0 + 520, E.out);
  const wb = uWidth(it.b, 34, 700), wa = it.a ? uWidth(it.a, 22, 700) : 0;
  const w = Math.max(wa, wb) + 64;
  return (
    <g opacity={o} transform={`translate(${r1((1 - k) * -24)} 0)`}>
      <rect x={58} y={FH - 178} width={w} height={it.a ? 104 : 74} rx={10} fill="rgba(4,8,20,0.72)" />
      <rect x={58} y={FH - 178} width={7} height={it.a ? 104 : 74} rx={3} fill={DK.gold} />
      {it.a && <UText x={86} y={FH - 144} s={it.a} size={22} weight={700} fill={DK.gold} C={DK} />}
      <UText x={86} y={FH - (it.a ? 98 : 128)} s={it.b} size={34} weight={700} fill="#F7F1E1" C={DK} />
    </g>
  );
}
/** 오른쪽 아래 작은 표시 — 실제 장면을 다듬어 다시 만든 그림임을 밝힌다 */
export function Tag({ o = 1, s = "재구성 화면 · 위치는 실제 장면을 바탕으로 다듬은 값 · 흐린 선수는 그날 선발, 자리는 짐작" }) {
  if (o <= 0.01) return null;
  return (
    <g opacity={o * 0.85}>
      <circle cx={FW - 60 - uWidth(s, 17, 600) - 18} cy={FH - 48} r={5} fill={DK.coral} />
      <UText x={FW - 60} y={FH - 42} s={s} size={17} weight={600} anchor="end" fill="#E6DFCF" halo="rgba(3,6,15,0.85)" C={DK} />
    </g>
  );
}
/** 제목(왼쪽 위) — 3D 위에서도 읽히게 테두리 */
export function Title3D({ title, sub, mode, o = 1 }) {
  if (o <= 0.01) return null;
  return (
    <g opacity={o}>
      <rect x={0} y={0} width={FW} height={170} fill="url(#t3d-scr)" />
      <defs><linearGradient id="t3d-scr" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#03060f" stopOpacity="0.55" /><stop offset="1" stopColor="#03060f" stopOpacity="0" /></linearGradient></defs>
      <text x={56} y={68} fontFamily={TITLE} fontSize={40} fill="#F7F1E1" style={{ paintOrder: "stroke", stroke: "rgba(3,6,15,0.7)", strokeWidth: 6, strokeLinejoin: "round" }}>{title}</text>
      {sub && <text x={58} y={108} fontFamily={SANS} fontSize={24} fontWeight={600} fill={mode === "m" ? DK.teal : DK.coral}
        style={{ paintOrder: "stroke", stroke: "rgba(3,6,15,0.7)", strokeWidth: 5, strokeLinejoin: "round" }} letterSpacing="0.02em">{sub}</text>}
    </g>
  );
}
/** 큰 「골!」 */
export function GoalBurst({ k, x = FW / 2, y = FH * 0.42 }) {
  if (k <= 0.01) return null;
  const s = 1 + 0.25 * (1 - E.out(Math.min(1, k * 2)));
  return (
    <g opacity={Math.min(1, k * 3)} transform={`translate(${x} ${y}) scale(${r1(s * 100) / 100})`}>
      <text x={0} y={0} fontFamily={SANS} fontSize={150} fontWeight={900} textAnchor="middle" fill={DK.gold}
        style={{ paintOrder: "stroke", stroke: "rgba(3,6,15,0.75)", strokeWidth: 14, strokeLinejoin: "round" }} letterSpacing="0.04em">골!</text>
    </g>
  );
}

export { Fragment, project, FW, FH, polyLen };

/** 설명 카드 안의 어두운 판(표 · 점 그림 받침) */
export function Panel({ x, y, w, h, o = 1, r = 22 }) {
  if (o <= 0.01) return null;
  return <rect x={x} y={y} width={w} height={h} rx={r} fill="rgba(6,10,24,0.72)" stroke="rgba(242,232,208,0.18)" strokeWidth={1.5} opacity={o} />;
}
