// ashrain.out — 교실 모니터 「축구」·「서술형」 묶음의 공용 그리기 부품 (kit-story.jsx)
// draw.jsx 는 고치지 않고 그 위에 얹는다.
//   · UText — draw.jsx 의 수식 배치(layoutMath)를 그대로 쓰되, 홀로 선 소문자 m 은 변수가 아니라 단위(미터)이므로 바로 세운다.
//     (이 묶음의 글자에는 변수 m 이 없다.) UBoard · UCaption · UTable · ULbl 은 draw.jsx 의 Board · Caption · Table · Lbl 과
//     같은 모양이고 글자만 UText 로 그린다.
//   · Chip(둥근 이름표) · CircNum(원 숫자) · Person(사람 표시) · IconGrid(점 그림) · Tape(줄자) · Chain(수의 사슬) · Stopwatch
import { layoutMath, textW, SANS, SERIF, ShapeIcon, ICON_COLOR, Path } from "./draw.jsx";
import { seg, win, E, clamp, partial, sub2, len2, add2, mul2 } from "./core.js";

/* ══════════ 글자 ══════════ */
const patched = new WeakMap();
/** layoutMath 결과에서 단위 m(분수 밖, 기울인 소문자 m)을 바로 세우고 뒤 글자를 그만큼 민다. 글꼴이 다시 재어지면 새로 고친다. */
export function layoutU(str, size, weight = 500) {
  const L = layoutMath(str, size, weight);
  let P = patched.get(L);
  if (P) return P;
  let shift = 0;
  const items = L.items.map((it) => {
    if (it.bar) return shift ? { ...it, bar: [it.bar[0] + shift, it.bar[1] + shift] } : it;
    const x = it.x + shift;
    if (it.it && it.s === "m" && it.dy === 0) {
      const w = textW("m", it.size, weight, false, false);
      shift += w - (it.w + it.size * 0.04);
      return { ...it, x, it: false, w };
    }
    return shift ? { ...it, x } : it;
  });
  P = { items, w: L.w + shift };
  patched.set(L, P);
  return P;
}
export const uWidth = (s, size = 40, weight = 500) => layoutU(String(s ?? ""), size, weight).w;
const PRE = { whiteSpace: "pre" };

/** draw.jsx MText 와 같은 쓰임 — 단위 m 만 바로 선다 */
export function UText({ x, y, s, size = 40, weight = 500, anchor = "start", fill, accent, halo, opacity = 1, C }) {
  if (s == null || s === "" || opacity <= 0.001) return null;
  const L = layoutU(String(s), size, weight);
  const x0 = anchor === "middle" ? x - L.w / 2 : anchor === "end" ? x - L.w : x;
  const col = fill || C?.ink || "#fff", acc = accent || C?.gold || col;
  const st = halo ? { paintOrder: "stroke", stroke: halo, strokeWidth: size * 0.2, strokeLinejoin: "round", whiteSpace: "pre" } : PRE;
  return (
    <g opacity={opacity}>
      {L.items.map((it, i) => it.icon
        ? <ShapeIcon key={i} kind={it.icon.kind} n={it.icon.n} cx={x0 + it.x + it.w / 2} cy={y - it.size * 0.34} r={it.size * 0.34}
            fill={it.icon.color && C ? C[ICON_COLOR[it.icon.color]] : null} stroke={it.ac ? acc : col} C={C} />
        : it.bar
        ? <line key={i} x1={x0 + it.bar[0]} x2={x0 + it.bar[1]} y1={y + it.dy} y2={y + it.dy}
            stroke={it.ac ? acc : col} strokeWidth={Math.max(2, size * 0.055)} strokeLinecap="round" />
        : <text key={i} x={x0 + it.x} y={y + it.dy} fontSize={it.size} fontFamily={it.it ? SERIF : SANS}
            fontStyle={it.it ? "italic" : undefined} fontWeight={it.it ? 500 : weight} fill={it.ac ? acc : col}
            xmlSpace="preserve" style={st}>{it.s}</text>)}
    </g>
  );
}

/** 그림 위 이름표 — 바탕 테두리로 선 위에서도 읽힌다 */
export function ULbl({ x, y, s, size = 30, anchor = "middle", fill, weight = 600, o = 1, C }) {
  return <UText x={x} y={y + size * 0.34} s={s} size={size} anchor={anchor} weight={weight} fill={fill || C.ink} halo={C.halo} opacity={o} C={C} />;
}

/**
 * 판서 — draw.jsx Board 와 같다. lines: [{ t, s, u?, row?, k?:"h", c?(색 이름), size? }]
 * 가장 최근 줄이 금빛 막대와 함께 또렷하고, 이전 줄은 조금 흐려진다.
 */
export function UBoard({ x, y, t, lines, C, size = 34, lh = 56, hsize, dim = 0.62 }) {
  const vis = lines.map((L, i) => ({ ...L, row: L.row ?? i })).filter((L) => t >= L.t && (L.u == null || t < L.u));
  let cur = null;
  for (const L of vis) if (!cur || L.t >= cur.t) cur = L;
  const hs = hsize || Math.round(size * 0.74);
  return (
    <g>
      {vis.map((L, i) => {
        const a = win(t, L.t, L.u ?? Infinity, 420, 320);
        const isCur = L === cur, head = L.k === "h";
        const yy = y + L.row * lh + (1 - seg(t, L.t, L.t + 420, E.out)) * 12;
        const sz = head ? hs : (L.size || size);
        return (
          <g key={i} opacity={a * (isCur || head ? 1 : 1 - (1 - dim) * seg(t, cur.t, cur.t + 500))}>
            {isCur && !head && <rect x={x - 22} y={yy - sz * 0.95} width={6} height={sz * 1.15} rx={3} fill={C.bar} />}
            <UText x={x} y={yy} s={L.s} size={sz} weight={head ? 650 : 560} fill={head ? C.soft : L.c ? C[L.c] : C.ink} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 자막 — draw.jsx Caption 과 같다. caps: [{ t, s, u? }] */
export function UCaption({ t, caps, C, y = 846, size = 36 }) {
  const live = caps.filter((c) => t >= c.t && (c.u == null || t < c.u));
  if (!live.length) return null;
  const last = live[live.length - 1];
  const prev = live.length > 1 ? live[live.length - 2] : null;
  const k = seg(t, last.t, last.t + 560, E.lin);
  const one = (c, o, key) => {
    const w = uWidth(c.s, size, 560);
    const a = o * (c.u != null ? 1 - seg(t, c.u - 320, c.u, E.sine) : 1);
    return (
      <g key={key} opacity={a}>
        <rect x={800 - w / 2 - 26} y={y - size * 1.02} width={w + 52} height={size * 1.48} rx={size * 0.5} fill={C.capBg} />
        <UText x={800} y={y} s={c.s} size={size} weight={560} anchor="middle" fill={C.capInk} C={C} />
      </g>
    );
  };
  const out = [];
  if (prev && k < 0.5) out.push(one(prev, E.sine(1 - 2 * k), "p"));
  out.push(one(last, prev ? E.sine(Math.max(0, 2 * k - 1)) : E.sine(k), "c"));
  return <g>{out}</g>;
}

/**
 * 표 — draw.jsx Table 과 같다. 칸: 문자열 | { s, t, fill, fo, fillT, color, cross, hi, hiU, hiCol, size, weight }
 */
export function UTable({ x, y, cols, rh, rows, C, t = 1e12, size = 28, o = 1, line }) {
  if (o <= 0.001) return null;
  const xs = [x]; for (const w of cols) xs.push(xs.at(-1) + w);
  const hs = rows.map((_, i) => (Array.isArray(rh) ? rh[i] : rh));
  const ys = [y]; for (const h of hs) ys.push(ys.at(-1) + h);
  const lc = line || C.soft;
  const fills = [], marks = [];
  rows.forEach((row, r) => row.forEach((cell, c) => {
    if (cell == null) return;
    const cs = typeof cell === "string" || typeof cell === "number" ? { s: String(cell) } : cell;
    const x0 = xs[c], x1 = xs[c + 1], y0 = ys[r], y1 = ys[r + 1], cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const a = cs.t == null ? 1 : seg(t, cs.t, cs.t + 320, E.sine);
    const k = `${r}-${c}`;
    if (cs.fill) fills.push(<rect key={"f" + k} x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill={C[cs.fill] || cs.fill}
      fillOpacity={(cs.fo ?? 0.16) * (cs.fillT == null ? 1 : seg(t, cs.fillT, cs.fillT + 300))} />);
    if (cs.s != null && cs.s !== "" && a > 0) {
      const sz = cs.size || size;
      marks.push(<UText key={"s" + k} x={cx} y={cy + sz * 0.36} s={cs.s} size={sz} weight={cs.weight || 600} anchor="middle"
        fill={cs.color ? C[cs.color] || cs.color : C.ink} opacity={a} C={C} />);
    }
    if (cs.hi != null) {
      const h = seg(t, cs.hi, cs.hi + 400, E.out) * (cs.hiU == null ? 1 : 1 - seg(t, cs.hiU, cs.hiU + 400));
      if (h > 0) marks.push(<rect key={"h" + k} x={x0 + 3} y={y0 + 3} width={x1 - x0 - 6} height={y1 - y0 - 6} rx={6}
        fill="none" stroke={C[cs.hiCol] || C.gold} strokeWidth={4} opacity={h} />);
    }
  }));
  return (
    <g opacity={o}>
      {fills}
      {xs.map((xx, i) => <line key={"v" + i} x1={xx} x2={xx} y1={ys[0]} y2={ys.at(-1)} stroke={lc} strokeWidth={i === 0 || i === xs.length - 1 ? 2.4 : 1.4} />)}
      {ys.map((yy, i) => <line key={"h" + i} x1={xs[0]} x2={xs.at(-1)} y1={yy} y2={yy} stroke={lc} strokeWidth={i === 0 || i === ys.length - 1 ? 2.4 : 1.4} />)}
      {marks}
    </g>
  );
}
/** 표의 한 행(가로줄)을 둘러 강조 — 행 번호 r, 열 범위 전체 */
export function RowHi({ x, y, cols, rh, r, C, o = 1, col }) {
  if (o <= 0.001) return null;
  const w = cols.reduce((a, b) => a + b, 0);
  const hs = Array.isArray(rh) ? rh : null;
  const top = hs ? y + hs.slice(0, r).reduce((a, b) => a + b, 0) : y + r * rh;
  const h = hs ? hs[r] : rh;
  return <rect x={x - 4} y={top - 3} width={w + 8} height={h + 6} rx={8} fill={C[col] || C.gold} fillOpacity={0.14 * o}
    stroke={C[col] || C.gold} strokeWidth={3.5} opacity={o} />;
}

/** 치수선 — draw.jsx Dim 과 같다(이름표만 ULbl): A→B 를 법선 방향으로 off 만큼 띄워 양 끝 눈금 + 가운데 글자 */
export function UDim({ A, B, off = 30, s, C, color, o = 1, size = 26, lofs = 22, at = 0.5, lcol }) {
  if (o <= 0.001) return null;
  const d = sub2(B, A), L = len2(d) || 1, u = [d[0] / L, d[1] / L], nrm = [u[1], -u[0]];
  const a = add2(A, mul2(nrm, off)), b = add2(B, mul2(nrm, off));
  const col = color || C.soft;
  const m = add2(add2(a, mul2(sub2(b, a), at)), mul2(nrm, lofs));
  return (
    <g opacity={o}>
      <Path pts={[a, b]} stroke={col} sw={2.2} />
      <Path pts={[add2(a, mul2(nrm, 9)), add2(a, mul2(nrm, -9))]} stroke={col} sw={2.2} />
      <Path pts={[add2(b, mul2(nrm, 9)), add2(b, mul2(nrm, -9))]} stroke={col} sw={2.2} />
      {s && <ULbl x={m[0]} y={m[1]} s={s} size={size} fill={lcol || C.ink} C={C} />}
    </g>
  );
}

/** 선분 옆 글자: P→Q 의 가운데에서 법선 방향(side)으로 off 만큼 */
export function SegLbl({ P, Q, s, off = 22, side = 1, C, size = 28, fill, o = 1, at = 0.5 }) {
  if (o <= 0.001 || !s) return null;
  const d = sub2(Q, P), L = len2(d) || 1, nrm = [(-d[1] / L) * side, (d[0] / L) * side];
  const m = add2(add2(P, mul2(d, at)), mul2(nrm, off));
  return <ULbl x={m[0]} y={m[1]} s={s} size={size} fill={fill} o={o} C={C} />;
}

/* ══════════ 작은 부품 ══════════ */
/** 둥근 이름표: 글자 폭에 맞춘 알약 모양 */
export function Chip({ x, y, s, size = 26, C, fill, stroke, color, anchor = "middle", o = 1, weight = 700, pad = 0.55 }) {
  if (o <= 0.001 || !s) return null;
  const w = uWidth(s, size, weight) + size * pad * 2, h = size * 1.5;
  const x0 = anchor === "middle" ? x - w / 2 : anchor === "end" ? x - w : x;
  return (
    <g opacity={o}>
      <rect x={x0} y={y - h / 2} width={w} height={h} rx={h / 2} fill={fill || C.capBg} stroke={stroke || "none"} strokeWidth={stroke ? 2 : 0} />
      <UText x={x0 + w / 2} y={y + size * 0.36} s={s} size={size} weight={weight} anchor="middle" fill={color || C.capInk} C={C} />
    </g>
  );
}
export const chipW = (s, size = 26, weight = 700, pad = 0.55) => uWidth(s, size, weight) + size * pad * 2;

/** 원 숫자(①②…) — 글꼴에 기대지 않고 그린다 */
export function CircNum({ x, y, n, r = 17, C, fill, color, stroke, o = 1 }) {
  if (o <= 0.001) return null;
  return (
    <g opacity={o}>
      <circle cx={x} cy={y} r={r} fill={fill || C.paper} stroke={stroke || C.ink} strokeWidth={2.4} />
      <text x={x} y={y + r * 0.42} textAnchor="middle" fontFamily={SANS} fontSize={r * 1.22} fontWeight={800} fill={color || C.ink}>{n}</text>
    </g>
  );
}

/** 사람 표시(머리 + 몸) — 얼굴은 그리지 않는다. (x, y) = 발 아래 가운데 */
export function Person({ x, y, h = 40, col, C, o = 1 }) {
  if (o <= 0.001) return null;
  const r = h * 0.17, c = col || C.soft;
  const bw = h * 0.42, by = y - h * 0.62;
  return (
    <g opacity={o}>
      <circle cx={x} cy={y - h + r} r={r} fill={c} />
      <path d={`M${x - bw / 2} ${y}L${x - bw / 2} ${by + bw * 0.4}Q${x - bw / 2} ${by} ${x} ${by}Q${x + bw / 2} ${by} ${x + bw / 2} ${by + bw * 0.4}L${x + bw / 2} ${y}Z`} fill={c} />
    </g>
  );
}

/** 점 그림(자연 빈도): cols × rows 개의 동그라미. paint(i) → { fill, o, ring } */
export function IconGrid({ x, y, cols, rows, step = 26, r = 9, paint, C, o = 1 }) {
  if (o <= 0.001) return null;
  const out = [];
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const k = j * cols + i, P = paint(k) || {};
    const cx = x + i * step + step / 2, cy = y + j * step + step / 2;
    out.push(<circle key={k} cx={cx} cy={cy} r={r * (P.scale ?? 1)} fill={P.fill || "none"} fillOpacity={P.fo ?? 1}
      stroke={P.stroke || C.soft} strokeWidth={P.sw ?? 1.6} opacity={P.o ?? 1} />);
  }
  return <g opacity={o}>{out}</g>;
}

/**
 * 줄자: a → b 로 노란 띠가 풀려 나간다(p = 0~1). pxPerM 마다 눈금(5 m마다 길게).
 * 끝에 걸쇠, 시작에 줄자 통. read 가 있으면 다 풀린 뒤 끝 근처에 읽은 값을 띄운다.
 */
export function Tape({ a, b, p = 1, pxPerM, C, read, rs = 26, ro, side = 1, o = 1, w = 13 }) {
  if (p <= 0 || o <= 0.001) return null;
  const d = sub2(b, a), L = len2(d) || 1, u = [d[0] / L, d[1] / L], n = [-u[1] * side, u[0] * side];
  const e = add2(a, mul2(u, L * clamp(p)));
  const band = (k) => add2(e, mul2(n, k));
  const ang = (Math.atan2(u[1], u[0]) * 180) / Math.PI;
  const ticks = [];
  const every = pxPerM >= 7 ? 1 : pxPerM >= 2.5 ? 5 : 10;
  const nT = Math.floor((L * clamp(p)) / (pxPerM * every));
  for (let i = 1; i <= nT; i++) {
    const m = i * every, q = add2(a, mul2(u, m * pxPerM)), big = m % 5 === 0;
    ticks.push(<line key={i} x1={q[0] + n[0] * w * 0.5} y1={q[1] + n[1] * w * 0.5} x2={q[0] + n[0] * (w * 0.5 - (big ? w * 0.75 : w * 0.42))}
      y2={q[1] + n[1] * (w * 0.5 - (big ? w * 0.75 : w * 0.42))} stroke="#5a4300" strokeWidth={big ? 1.8 : 1.1} />);
  }
  const rp = ro ?? seg(p, 0.92, 1, E.lin);
  const mid = add2(add2(a, mul2(d, 0.5)), mul2(n, -(w * 0.5 + rs * 0.95)));
  return (
    <g opacity={o}>
      <path d={`M${a[0] + n[0] * w / 2} ${a[1] + n[1] * w / 2}L${band(w / 2)[0]} ${band(w / 2)[1]}L${band(-w / 2)[0]} ${band(-w / 2)[1]}L${a[0] - n[0] * w / 2} ${a[1] - n[1] * w / 2}Z`}
        fill={C.yellow} stroke="#8a6a00" strokeWidth={1.2} strokeLinejoin="round" />
      {ticks}
      {/* 걸쇠 */}
      <line x1={band(w * 0.75)[0]} y1={band(w * 0.75)[1]} x2={band(-w * 0.75)[0]} y2={band(-w * 0.75)[1]} stroke="#3b3b3b" strokeWidth={4} strokeLinecap="round" />
      {/* 줄자 통 */}
      <g transform={`translate(${a[0]} ${a[1]}) rotate(${ang})`}>
        <rect x={-30} y={-17} width={32} height={34} rx={9} fill={C.coral} stroke="#3b1a12" strokeWidth={1.6} />
        <circle cx={-14} cy={0} r={8} fill="#f6efe2" stroke="#3b1a12" strokeWidth={1.4} />
      </g>
      {read && rp > 0 && <Chip x={mid[0]} y={mid[1]} s={read} size={rs} C={C} o={rp} fill={C.yellow} color="#2a2000" />}
    </g>
  );
}

/**
 * 수의 사슬: 상자 [v0] → [v1] → … 화살표 위에 곱하는 수(또는 말). 상자 i 는 at[i] 시각에 나타난다.
 *   vals: 글자 배열 · ops: 화살표 위 글자 배열(길이 vals − 1) · last: 마지막 상자 강조 색
 */
export function Chain({ x, y, vals, ops, at, t, C, size = 30, gap = 56, bh = 50, col, last = "gold", o = 1, opSize }) {
  if (o <= 0.001) return null;
  const ws = vals.map((v) => Math.max(bh * 1.4, uWidth(v, size, 750) + size * 0.9));
  const xs = []; let cx = x;
  ws.forEach((w) => { xs.push(cx); cx += w + gap; });
  const out = [];
  vals.forEach((v, i) => {
    const a = seg(t, at[i], at[i] + 380, E.out);
    if (a <= 0) return;
    const isLast = i === vals.length - 1;
    const c = isLast ? C[last] : C[col] || C.ink;
    if (i > 0) {
      const x0 = xs[i - 1] + ws[i - 1] + 6, x1 = xs[i] - 6;
      out.push(<g key={"a" + i} opacity={a}>
        <Path pts={[[x0, y], [x1 - 9, y]]} stroke={C.soft} sw={3} />
        <path d={`M${x1 - 12} ${y - 7}L${x1} ${y}L${x1 - 12} ${y + 7}Z`} fill={C.soft} />
        {ops?.[i - 1] && <UText x={(x0 + x1) / 2} y={y - bh * 0.62} s={ops[i - 1]} size={opSize || size * 0.66} weight={650} anchor="middle" fill={C.soft} C={C} />}
      </g>);
    }
    out.push(<g key={"b" + i} opacity={a} transform={`translate(${xs[i] + ws[i] / 2} ${y}) scale(${0.85 + 0.15 * a}) translate(${-(xs[i] + ws[i] / 2)} ${-y})`}>
      <rect x={xs[i]} y={y - bh / 2} width={ws[i]} height={bh} rx={bh * 0.28} fill={c} fillOpacity={isLast ? 0.2 : 0.08} stroke={c} strokeWidth={isLast ? 3.2 : 2} />
      <UText x={xs[i] + ws[i] / 2} y={y + size * 0.36} s={v} size={size} weight={750} anchor="middle" fill={isLast ? C[last] : C.ink} C={C} />
    </g>);
  });
  return <g opacity={o}>{out}</g>;
}
export const chainW = (vals, size = 30, gap = 56, bh = 50) =>
  vals.reduce((a, v) => a + Math.max(bh * 1.4, uWidth(v, size, 750) + size * 0.9), 0) + gap * (vals.length - 1);

/** 초시계: 바늘이 sec 만큼 돈다(한 바퀴 = full 초). label 은 아래 글자 */
export function Stopwatch({ x, y, r = 30, sec, full = 4, C, col, label, o = 1 }) {
  if (o <= 0.001) return null;
  const a = (sec / full) * 360 - 90;
  const c = col || C.ink;
  const tip = [x + r * 0.78 * Math.cos((a * Math.PI) / 180), y + r * 0.78 * Math.sin((a * Math.PI) / 180)];
  return (
    <g opacity={o}>
      <rect x={x - 6} y={y - r - 11} width={12} height={9} rx={2} fill={c} />
      <circle cx={x} cy={y} r={r} fill={C.paper} stroke={c} strokeWidth={3.4} />
      {Array.from({ length: 8 }, (_, i) => {
        const q = (i / 8) * Math.PI * 2;
        return <line key={i} x1={x + r * 0.78 * Math.cos(q)} y1={y + r * 0.78 * Math.sin(q)} x2={x + r * 0.92 * Math.cos(q)} y2={y + r * 0.92 * Math.sin(q)} stroke={C.soft} strokeWidth={1.6} />;
      })}
      <line x1={x} y1={y} x2={tip[0]} y2={tip[1]} stroke={C.coral} strokeWidth={3.4} strokeLinecap="round" />
      <circle cx={x} cy={y} r={3.6} fill={c} />
      {label && <UText x={x} y={y + r + 34} s={label} size={26} weight={750} anchor="middle" fill={c} C={C} />}
    </g>
  );
}

/** 선분을 따라가는 점 — pts 위 비율 p */
export { partial };
