// ashrain.out — 교실 모니터 「액자」: 하노이의 탑 — 그리기 (frames/hanoi.jsx)
// 살짝 내려다본 나무 받침·기둥 세 개·원판(원기둥). 계산은 ../hanoi.js(배치·순서·시간표)가 하고, 여기서는 모습만 그린다.
// 그리는 순서: 받침 → 기둥마다 [기둥 → 쌓인 판(아래부터) → 꿰인 채 움직이는 판 → 맨 위 판의 구멍에서 솟은 기둥 끝] → 공중의 판.
import { along } from "../core";
import { SANS, TITLE } from "../draw";
import { HANOI, PEG_NAMES, levelY, movePath, moveEase, comma, fmtDur } from "../hanoi";

/* ── 색 ── */
const hex = (h) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const rgb = (c) => `rgb(${c.map((v) => Math.round(Math.min(255, Math.max(0, v)))).join(",")})`;
const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
const dark = (c, k) => c.map((v) => v * k);
const WHITE = [255, 255, 255];
// 아래(큰 판) 따뜻한 색 → 위(작은 판) 차가운 색 — 팔레트의 산호·금·잎·청록·하늘·보라
const RAMP = {
  dark: ["#F2877B", "#F4C65A", "#A6D886", "#6BD3C3", "#8FB9F6", "#C6A8F6"].map(hex),
  light: ["#C34E3E", "#B37A0E", "#478A28", "#13877A", "#2D65B2", "#7550BC"].map(hex),
};
const colorCache = new Map();
/** 원판 d(0 = 가장 작은 판)의 몸통·윗면·테두리 색 */
export function diskColors(n, theme) {
  const key = `${n}|${theme}`;
  if (colorCache.has(key)) return colorCache.get(key);
  const R = RAMP[theme] || RAMP.dark;
  const out = [];
  for (let d = 0; d < n; d++) {
    const u = n > 1 ? ((n - 1 - d) / (n - 1)) * (R.length - 1) : 0;
    const i = Math.min(R.length - 2, Math.floor(u));
    const c = mix(R[i], R[i + 1], u - i);
    out.push({ body: rgb(c), top: rgb(mix(c, WHITE, theme === "light" ? 0.22 : 0.2)), edge: rgb(dark(c, theme === "light" ? 0.62 : 0.5)) });
  }
  colorCache.set(key, out);
  return out;
}

/* ── 부품 ── */
function Disk({ cx, yb, w, h, tilt, col, uid }) {
  const rx = w / 2, ry = rx * tilt, yt = yb - h;
  const f = (v) => v.toFixed(1);
  const body = `M${f(cx - rx)} ${f(yt)}L${f(cx - rx)} ${f(yb)}A${f(rx)} ${f(ry)} 0 0 0 ${f(cx + rx)} ${f(yb)}`
    + `L${f(cx + rx)} ${f(yt)}A${f(rx)} ${f(ry)} 0 0 1 ${f(cx - rx)} ${f(yt)}Z`;
  return (
    <g>
      <path d={body} fill={col.body} />
      <path d={body} fill={`url(#${uid}-cyl)`} />
      <path d={body} fill="none" stroke={col.edge} strokeWidth={1.6} strokeLinejoin="round" />
      <ellipse cx={cx} cy={yt} rx={rx} ry={ry} fill={col.top} stroke={col.edge} strokeWidth={1.6} />
      <ellipse cx={cx} cy={yt} rx={rx * 0.78} ry={ry * 0.78} fill="none" stroke="#fff" strokeOpacity={0.13} strokeWidth={1.4} />
    </g>
  );
}
/** 기둥(둥근 끝). y0 = 끝, y1 = 아래 */
function PegStick({ x, y0, y1, r, wood, uid }) {
  if (y1 - y0 < 0.5) return null;
  const top = y0 + r * 0.9;
  return (
    <g>
      <path d={`M${x - r} ${y1}L${x - r} ${top}A${r} ${r * 0.9} 0 0 1 ${x + r} ${top}L${x + r} ${y1}Z`} fill={wood.stick} />
      <path d={`M${x - r} ${y1}L${x - r} ${top}A${r} ${r * 0.9} 0 0 1 ${x + r} ${top}L${x + r} ${y1}Z`} fill={`url(#${uid}-cyl)`} />
      <path d={`M${x - r} ${y1}L${x - r} ${top}A${r} ${r * 0.9} 0 0 1 ${x + r} ${top}L${x + r} ${y1}`} fill="none" stroke={wood.edge} strokeOpacity={0.55} strokeWidth={1.4} />
    </g>
  );
}
/** 원판 윗면 가운데 구멍 + 구멍에서 솟은 기둥 */
function PegAbove({ x, yt, L, wood, uid }) {
  const r = L.PEG_R, hr = r + 6;
  return (
    <g>
      <ellipse cx={x} cy={yt} rx={hr} ry={Math.max(3, hr * L.TILT)} fill="#000" fillOpacity={0.32} />
      <PegStick x={x} y0={L.yTip} y1={yt} r={r} wood={wood} uid={uid} />
    </g>
  );
}

function Board({ L, wood, uid }) {
  const { half, depth, thick } = L.BOARD, y = L.yBase, x0 = 800 - half, x1 = 800 + half;
  return (
    <g>
      <ellipse cx={800} cy={y + depth + thick + 8} rx={half + 36} ry={24} fill={`url(#${uid}-shadow)`} />
      <path d={`M${x0} ${y + depth - 12}L${x0} ${y + depth + thick - 12}Q${x0} ${y + depth + thick} ${x0 + 14} ${y + depth + thick}`
        + `L${x1 - 14} ${y + depth + thick}Q${x1} ${y + depth + thick} ${x1} ${y + depth + thick - 12}L${x1} ${y + depth - 12}Z`}
        fill={wood.front} stroke={wood.edge} strokeOpacity={0.5} strokeWidth={1.6} />
      <rect x={x0} y={y - depth} width={half * 2} height={depth * 2} rx={26} ry={12} fill={wood.top}
        stroke={wood.edge} strokeOpacity={0.5} strokeWidth={1.6} />
      <rect x={x0} y={y - depth} width={half * 2} height={depth * 2} rx={26} ry={12} fill={`url(#${uid}-board)`} />
      {L.X.map((x, i) => (
        <g key={i}>
          <ellipse cx={x} cy={y} rx={L.PEG_R + 7} ry={(L.PEG_R + 7) * L.TILT + 1} fill="#000" fillOpacity={0.18} />
          <text x={x} y={y + depth + thick / 2 + 8} textAnchor="middle" fontFamily={SANS} fontSize={22} fontWeight={800}
            fill={wood.edge} fillOpacity={0.78} letterSpacing="0.06em">{PEG_NAMES[i]}</text>
        </g>
      ))}
    </g>
  );
}

function Defs({ uid, theme }) {
  const lt = theme === "light";
  return (
    <defs>
      <linearGradient id={`${uid}-cyl`} x1="0" x2="1" y1="0" y2="0">
        <stop offset="0" stopColor="#000" stopOpacity={0.3} />
        <stop offset="0.2" stopColor="#fff" stopOpacity={0.08} />
        <stop offset="0.38" stopColor="#fff" stopOpacity={lt ? 0.26 : 0.2} />
        <stop offset="0.6" stopColor="#fff" stopOpacity={0} />
        <stop offset="1" stopColor="#000" stopOpacity={0.36} />
      </linearGradient>
      <linearGradient id={`${uid}-board`} x1="0" x2="0" y1="0" y2="1">
        <stop offset="0" stopColor="#000" stopOpacity={0.1} />
        <stop offset="0.5" stopColor="#fff" stopOpacity={lt ? 0.14 : 0.08} />
        <stop offset="1" stopColor="#fff" stopOpacity={0} />
      </linearGradient>
      <radialGradient id={`${uid}-shadow`}>
        <stop offset="0" stopColor="#000" stopOpacity={lt ? 0.22 : 0.4} />
        <stop offset="1" stopColor="#000" stopOpacity={0} />
      </radialGradient>
      <radialGradient id={`${uid}-glow`}>
        <stop offset="0" stopColor="#F4C65A" stopOpacity={lt ? 0.42 : 0.38} />
        <stop offset="1" stopColor="#F4C65A" stopOpacity={0} />
      </radialGradient>
    </defs>
  );
}

const woodOf = (C) => {
  const w = hex(C.wood), e = hex(C.woodEdge);
  return { top: rgb(mix(w, WHITE, 0.06)), front: rgb(dark(w, 0.74)), stick: rgb(mix(w, WHITE, 0.04)), edge: C.woodEdge, edgeRgb: e };
};

/**
 * 하노이의 탑 한 장면.
 *   L  = hanoiLayout(n) · st = hanoiAt(...) 또는 locate(...) 결과 · C = 팔레트(다크/라이트)
 *   info = 아래 안내 글자 { total, speed } (없으면 그림만 — 목록의 작은 그림)
 */
export function HanoiArt({ L, st, C, uid = "hn", info }) {
  const n = L.n, cols = diskColors(n, C.name), wood = woodOf(C);
  // 움직이는 판의 자리
  let mv = null;
  if (st.moving) {
    const pts = movePath(L, st.from, st.fromLv, st.to, st.toLv);
    const p = along(pts, moveEase(st.k));
    const onPeg = (i) => Math.abs(p[0] - L.X[i]) < 0.01 && p[1] > L.yTip;   // 기둥에 꿰여 있다
    mv = { x: p[0], yb: p[1], d: st.disk, peg: onPeg(st.from) ? st.from : onPeg(st.to) ? st.to : -1 };
  }
  const stacks = [[], [], []];
  for (let d = 0; d < n; d++) if (st.pos[d] >= 0) stacks[st.pos[d]].push(d);
  for (const s of stacks) s.sort((a, b) => st.lv[a] - st.lv[b]);

  const drawDisk = (d, x, yb, key) => <Disk key={key} cx={x} yb={yb} w={L.widths[d]} h={L.h} tilt={L.TILT} col={cols[d]} uid={uid} />;
  const hold = st.hold;
  const glow = hold != null ? Math.min(1, hold / 600) * Math.min(1, (HANOI.HOLD_MS - hold) / 700) : 0;

  return (
    <g>
      <Defs uid={uid} theme={C.name} />
      <Board L={L} wood={wood} uid={uid} />
      {glow > 0.01 && (
        <ellipse cx={L.X[st.dst]} cy={L.yBase} rx={L.widths[n - 1] * 0.7} ry={60} fill={`url(#${uid}-glow)`} opacity={glow} />
      )}
      {L.X.map((x, i) => {
        const S = stacks[i];
        const topD = S.length ? S[S.length - 1] : null;
        const topYt = topD == null ? null : levelY(L, st.lv[topD]) - L.h;
        const thread = mv && mv.peg === i;
        return (
          <g key={i}>
            <PegStick x={x} y0={L.yTip} y1={L.yBase} r={L.PEG_R} wood={wood} uid={uid} />
            {S.map((d) => drawDisk(d, x, levelY(L, st.lv[d]), d))}
            {topD != null && <PegAbove x={x} yt={topYt} L={L} wood={wood} uid={uid} />}
            {thread && drawDisk(mv.d, x, mv.yb, "mv")}
            {thread && <PegAbove x={x} yt={mv.yb - L.h} L={L} wood={wood} uid={uid} />}
          </g>
        );
      })}
      {mv && mv.peg < 0 && drawDisk(mv.d, mv.x, mv.yb, "mv")}
      {info && <Info L={L} st={st} C={C} info={info} glow={glow} />}
    </g>
  );
}

/** 아래 안내: 왼쪽 이름·판 수·방향, 오른쪽 몇 번째·남은 시간. 다 옮기면 가운데 위에 한 줄 */
function Info({ L, st, C, info, glow }) {
  const moves = 2 ** L.n - 1, y = 872;
  const dir = `${PEG_NAMES[st.src]} → ${PEG_NAMES[st.dst]}`;
  const sp = info.speed === "fast" ? "빠르게 · 1초에 1개" : "자연스럽게";
  const done = st.hold != null;
  const right = done
    ? [[`${comma(moves)}번`, C.ink, 700], [` 다 옮김 · ${fmtDur(info.total)}`, C.soft, 600]]
    : [[`${comma(moves)}번 중 `, C.soft, 600], [`${comma(st.m)}번째`, C.ink, 700],
      [`  ·  남은 시간 ${fmtDur(info.total - st.tau)}`, C.soft, 600]];
  return (
    <g>
      <text x={56} y={y} fontFamily={SANS} fontSize={21} fontWeight={600} fill={C.soft}>
        <tspan fontFamily={TITLE} fontSize={30} fontWeight={400} fill={C.ink}>하노이의 탑</tspan>
        <tspan dx={18}>{`원판 ${L.n}개 · ${dir} · ${sp}`}</tspan>
      </text>
      <text x={1544} y={y} textAnchor="end" fontFamily={SANS} fontSize={21}>
        {right.map(([s, f, w], i) => <tspan key={i} fill={f} fontWeight={w} xmlSpace="preserve">{s}</tspan>)}
      </text>
      {glow > 0.01 && (
        <g opacity={glow}>
          <rect x={800 - 340} y={L.yTip - 150} width={680} height={58} rx={29} fill={C.capBg} />
          <text x={800} y={L.yTip - 111} textAnchor="middle" fontFamily={SANS} fontSize={28} fontWeight={650} fill={C.capInk}>
            {`다 옮겼어요 · ${comma(moves)}번 — 이번엔 ${PEG_NAMES[st.dst]} → ${PEG_NAMES[st.src]}`}
          </text>
        </g>
      )}
    </g>
  );
}

/** 액자 목록의 작은 그림(원판 5개, 옮기는 중) */
export function HanoiThumb({ C, TL, uid = "hnt" }) {
  const st = { ...TL.locate(TL.total * 0.37, 0, 2), src: 0, dst: 2, hold: null };
  return <HanoiArt L={TL.L} st={st} C={C} uid={uid} />;
}
