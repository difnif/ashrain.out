// ashrain.out — 수학 호기심 액자: 골프로 보는 포물선 (frames/golffn.jsx)
// 가상 코스(수학 컨트리클럽 9홀)를 가상 선수가 돈다. 위: 홀을 내려다본 지도(공이 있던 곳 → 떨어진 곳 → 굴러간 곳),
// 아래: 옆에서 본 공의 길 — 포물선. 샷이 끝나면 꼭짓점 · 식(중등) 또는 대칭 · 남은 거리 비율(초등).
//   중등(중3 이차함수): y = a(x − p)² + q, 꼭짓점 (날아간 거리 ÷ 2, 가장 높은 높이), (0, 0)을 지나서 a = −q ÷ p².
//   초등: 가장 높은 곳은 한가운데(대칭) · 남은 거리 중 몇 %를 줄였나.
// 풀이 상세: 오른쪽 설명 판(홀 · 타수 · 판서 · 점수 카드) · 최소화: 지도와 옆모습을 크게, 칩만. 계산: ../curio/golf.js
import { memo } from "react";
import { W, H, MText, SceneTitle, Path, SANS, textW } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip, chipW } from "../kit-story.jsx";
import { SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, rng, hashSeed, fs } from "../curio/kit.js";
import { HOLES, holeInfo, along, holeLen, roundOf, golfAt, GT, golfSteps, parabola, scoreName, totalText, LIE } from "../curio/golf.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { FitText, Lines, Panel } from "./curio-kit.jsx";

const LSK = "ash.display.curio.golf";
const PANEL = { x: 1162, y: 150, w: 400, h: 720 };
const TOP = { full: [40, 150, 1140, 640], mini: [36, 150, 1564, 628] };
const SIDE = { full: [40, 654, 1140, 870], mini: [36, 640, 1564, 872] };

/* ══════════ 홀 지도 ══════════ */
const CAM = new Map();
/** 홀 i 의 카메라(m → px) */
function holeCam(i, ex) {
  const key = i + ex;
  if (CAM.has(key)) return CAM.get(key);
  const h = HOLES[i], { green } = holeInfo(h);
  const pts = [...h.line, [green[0] + h.gr + 14, green[1]], ...h.bunk.map(([x, y, rx, ry]) => [x + rx, y + ry]), ...h.bunk.map(([x, y, rx, ry]) => [x - rx, y - ry]),
    ...h.water.map(([x, y, rx, ry]) => [x + rx, y + ry]), ...h.water.map(([x, y, rx, ry]) => [x - rx, y - ry])];
  let x0 = Math.min(...pts.map((q) => q[0])) - 24, x1 = Math.max(...pts.map((q) => q[0])) + 24;
  let y0 = Math.min(...pts.map((q) => q[1])) - 40, y1 = Math.max(...pts.map((q) => q[1])) + 40;
  const A = TOP[ex], aw = A[2] - A[0], ah = A[3] - A[1];
  const s = Math.min(aw / (x1 - x0), ah / (y1 - y0));
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, mx = (A[0] + A[2]) / 2, my = (A[1] + A[3]) / 2;
  const cam = { s, p: (q) => [mx + (q[0] - cx) * s, my - (q[1] - cy) * s], box: A };
  CAM.set(key, cam);
  return cam;
}
const COL = {
  dark: { rough: "#244a2c", deep: "#1c3b23", fw: "#3f7a42", fwStripe: "#46844a", green: "#5aa35a", fringe: "#4b9150", sand: "#d9c38e", water: "#2f6fae", tree: "#163420", tee: "#4f8f52" },
  light: { rough: "#8dbb6c", deep: "#78a95a", fw: "#a9d68a", fwStripe: "#b3dd94", green: "#c4e9a3", fringe: "#b2df90", sand: "#f0e0b0", water: "#5aa0e0", tree: "#4e7f3d", tee: "#b6de98" },
};
/** 중심선을 따라 폭 w 의 띠(다각형) */
function band(line, w, s0, s1, step = 6) {
  const L = [], Rr = [];
  for (let s = s0; s <= s1 + 0.01; s += step) {
    const p = along(line, s), q = along(line, Math.min(s1, s + 2) === s ? s - 2 : Math.min(s1, s + 2));
    let dx = q[0] - p[0], dy = q[1] - p[1];
    if (Math.min(s1, s + 2) === s) { dx = -dx; dy = -dy; }
    const n = Math.hypot(dx, dy) || 1;
    const nx = -dy / n, ny = dx / n;
    L.push([p[0] + nx * w / 2, p[1] + ny * w / 2]); Rr.push([p[0] - nx * w / 2, p[1] - ny * w / 2]);
  }
  return [...L, ...Rr.reverse()];
}
const HoleMap = memo(function HoleMap({ i, ex, C }) {
  const h = HOLES[i], cam = holeCam(i, ex), K = COL[C.name === "light" ? "light" : "dark"];
  const { green, pin } = holeInfo(h), len = holeLen(h);
  const [bx0, by0, bx1, by1] = cam.box;
  const poly = (pts) => "M" + pts.map((q) => cam.p(q).map((v) => v.toFixed(1)).join(" ")).join("L") + "Z";
  const fw = h.fw ? band(h.line, h.fw, 90, Math.max(100, len - h.gr - 6)) : null;
  const tee = cam.p(h.line[0]);
  // 나무: 페어웨이 양옆(씨앗 = 홀 번호)
  const R = rng(hashSeed("trees", i));
  const trees = [];
  for (let s = 20; s < len + 10; s += 16) {
    for (const side of [-1, 1]) {
      if (R() < 0.35) continue;
      const p = along(h.line, s), q = along(h.line, s + 2);
      const dx = q[0] - p[0], dy = q[1] - p[1], n = Math.hypot(dx, dy) || 1;
      const off = (Math.max(h.fw, 30) / 2 + 22 + R() * 30) * side;
      const t = [p[0] - (dy / n) * off, p[1] + (dx / n) * off];
      if (Math.hypot(t[0] - green[0], t[1] - green[1]) < h.gr + 16) continue;
      if (h.water.some(([x, y, rx, ry]) => ((t[0] - x) / (rx + 6)) ** 2 + ((t[1] - y) / (ry + 6)) ** 2 <= 1)) continue;
      trees.push([t, 4 + R() * 4]);
    }
  }
  const g = cam.p(green), pp = cam.p(pin);
  const id = `golf-clip-${i}-${ex}`;
  return (
    <g>
      <defs><clipPath id={id}><rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} /></clipPath></defs>
      <g clipPath={`url(#${id})`}>
        <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} fill={K.deep} />
        <path d={poly(band(h.line, Math.max(h.fw, 30) + 50, 0, len))} fill={K.rough} />
        {fw && <path d={poly(fw)} fill={K.fw} stroke={K.fwStripe} strokeWidth={2} />}
        {h.water.map(([x, y, rx, ry], j) => { const q = cam.p([x, y]); return <ellipse key={"w" + j} cx={q[0]} cy={q[1]} rx={rx * cam.s} ry={ry * cam.s} fill={K.water} stroke="#9fd0ff" strokeOpacity={0.6} strokeWidth={2} />; })}
        <circle cx={g[0]} cy={g[1]} r={(h.gr + 4) * cam.s} fill={K.fringe} />
        <circle cx={g[0]} cy={g[1]} r={h.gr * cam.s} fill={K.green} />
        {h.bunk.map(([x, y, rx, ry], j) => { const q = cam.p([x, y]); return <ellipse key={"b" + j} cx={q[0]} cy={q[1]} rx={rx * cam.s} ry={ry * cam.s} fill={K.sand} stroke="#b89d5c" strokeOpacity={0.6} strokeWidth={1.5} />; })}
        {trees.map(([t, r], j) => { const q = cam.p(t); return <circle key={"t" + j} cx={q[0]} cy={q[1]} r={r * cam.s} fill={K.tree} opacity={0.9} />; })}
        <rect x={tee[0] - 5 * cam.s} y={tee[1] - 4 * cam.s} width={10 * cam.s} height={8 * cam.s} rx={2} fill={K.tee} stroke="#fff" strokeOpacity={0.5} />
        {/* 깃대 */}
        <circle cx={pp[0]} cy={pp[1]} r={3.5} fill="#111" />
        <line x1={pp[0]} x2={pp[0]} y1={pp[1]} y2={pp[1] - 34} stroke="#f4f4f4" strokeWidth={2.4} />
        <path d={`M${pp[0]} ${pp[1] - 34}l20 6l-20 6z`} fill="#e53935" />
      </g>
      <rect x={bx0} y={by0} width={bx1 - bx0} height={by1 - by0} rx={16} fill="none" stroke={C.cardEdge} strokeWidth={1.4} />
    </g>
  );
});

/* ══════════ 옆에서 본 길 ══════════ */
function SideView({ C, mode, ex, s, kf, km }) {
  const [x0, y0, x1, y1] = SIDE[ex];
  const isM = mode === "m", mini = ex === "mini";
  const pad = 46, gy = y1 - 30;
  const panelEl = <rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} rx={14} fill={C.card} fillOpacity={C.name === "light" ? 0.7 : 0.5} stroke={C.cardEdge} strokeWidth={1.2} />;
  if (!s) return panelEl;
  const ink = C.ink, soft = C.soft;
  if (s.kind === "putt") {
    // 퍼트: 0 m 에서 출발해 컵까지 굴러가는 자 — 눈금은 0.5 m 또는 1 m
    const L = Math.max(2, Math.ceil(s.d0 * 1.2)), sc = (x1 - x0 - 2 * pad - 40) / L;
    const P = (d) => x0 + pad + d * sc;
    const stop = s.made ? s.d0 : Math.max(0, s.d0 - s.d1);
    const bx = P(stop * kf), cup = P(s.d0);
    const step = L <= 4 ? 0.5 : L <= 12 ? 1 : 2, ticks = [];
    for (let v = 0; v <= L + 1e-9; v += step) ticks.push(Math.round(v * 10) / 10);
    return (
      <g>
        {panelEl}
        <line x1={P(0) - 10} x2={P(L) + 10} y1={gy} y2={gy} stroke={ink} strokeWidth={2} opacity={0.5} />
        {ticks.map((v) => <g key={v}><line x1={P(v)} x2={P(v)} y1={gy} y2={gy + 6} stroke={ink} opacity={0.5} /><text x={P(v)} y={gy + 21} textAnchor="middle" fontFamily={SANS} fontSize={13} fontWeight={700} fill={soft}>{v}</text></g>)}
        <rect x={cup - 7} y={gy - 1} width={14} height={9} rx={2} fill="#111" />
        <line x1={cup} x2={cup} y1={gy} y2={gy - 62} stroke={ink} strokeWidth={2.2} opacity={0.85} />
        <path d={`M${cup} ${gy - 62}l22 6.5l-22 6.5z`} fill="#e53935" />
        {kf > 0 && <line x1={P(0)} x2={bx} y1={gy - 7} y2={gy - 7} stroke={C.gold} strokeWidth={3} strokeLinecap="round" opacity={0.85} />}
        <circle cx={bx} cy={gy - 7} r={7} fill="#fff" stroke="#333" strokeWidth={1.2} />
        <text x={x0 + 14} y={y0 + 26} fontFamily={SANS} fontSize={mini ? 16 : 15} fontWeight={700} fill={soft}>{`옆에서 본 퍼트(m) — 높이는 늘 0, 굴러가는 거리 ${s.d0}m`}</text>
      </g>
    );
  }
  const { p, q, a } = parabola(s.carry, s.apex);
  // 세로는 판 높이에 맞추고, 가로는 판 너비에 맞추되 세로 눈금의 3.2배까지만 늘인다(짧은 어프로치가 납작해지지 않게).
  // 두 축 모두 눈금을 적으므로 그래프로 읽힌다.
  const sy = (gy - y0 - 58) / s.apex, sx = Math.min((x1 - x0 - 2 * pad - 20) / s.carry, sy * 3.2);
  const X = (x) => x0 + pad + x * sx, Y = (y) => gy - y * sy;
  const N = 60, pts = [];
  for (let j = 0; j <= N; j++) {
    const x = (s.carry * j) / N;
    if (j / N > kf + 1e-9) break;
    pts.push([X(x), Y((a[0] / a[1]) * (x - p) * (x - p) + q)]);
  }
  const tip = pts.length ? pts[pts.length - 1] : [X(0), gy];
  const ticks = [], hticks = [];
  const tstep = s.carry > 120 ? 50 : s.carry > 40 ? 20 : s.carry > 15 ? 5 : 2;
  for (let v = 0; v <= s.carry + 0.01; v += tstep) ticks.push(v);
  const hstep = s.apex > 24 ? 10 : s.apex > 8 ? 5 : s.apex > 3 ? 2 : 1;
  for (let v = hstep; v <= s.apex + 0.01; v += hstep) if (gy - Y(v) > 18) hticks.push(v);
  const kv = seg(km, 0, 500);
  const eq = isM ? `y = ${fs(a[0], a[1])}(x − ${p})² + ${q}` : `가장 높은 곳: 한가운데 ${p}m · 높이 ${q}m`;
  const head = isM ? "옆에서 본 길(m) — 이차함수" : "옆에서 본 길(m)", hsz = mini ? 16 : 15;
  // 꼭짓점 이름표: 꼭짓점 위, 왼쪽 제목과 오른쪽 식 칩 사이에서
  const esz = mini ? 22 : 19, ew = chipW(eq, esz), vs = isM ? `꼭짓점 (${p}, ${q})` : `높이 ${q}m`, vw = chipW(vs, 18);
  const vx = clamp(X(p), x0 + 14 + textW(head, hsz, 700) + 14 + vw / 2, x1 - 16 - ew - 14 - vw / 2);
  return (
    <g>
      {panelEl}
      <line x1={x0 + pad - 10} x2={X(s.carry) + 30} y1={gy} y2={gy} stroke={ink} strokeWidth={2} opacity={0.55} />
      {ticks.map((v) => <g key={v}><line x1={X(v)} x2={X(v)} y1={gy} y2={gy + 6} stroke={ink} opacity={0.5} /><text x={X(v)} y={gy + 21} textAnchor="middle" fontFamily={SANS} fontSize={13} fontWeight={700} fill={soft}>{v}</text></g>)}
      {hticks.map((v) => <g key={"h" + v}><line x1={X(0) - 6} x2={X(s.carry)} y1={Y(v)} y2={Y(v)} stroke={ink} opacity={0.08} /><text x={X(0) - 10} y={Y(v) + 4.5} textAnchor="end" fontFamily={SANS} fontSize={12} fontWeight={700} fill={soft} opacity={0.85}>{v}</text></g>)}
      <text x={x0 + 14} y={y0 + 26} fontFamily={SANS} fontSize={hsz} fontWeight={700} fill={soft}>{head}</text>
      {pts.length > 1 && <Path pts={pts} stroke={C.gold} sw={3.4} />}
      {kf > 0 && kf < 1 && <circle cx={tip[0]} cy={tip[1]} r={6} fill="#fff" stroke="#333" strokeWidth={1.2} />}
      {kv > 0 && (
        <g opacity={kv}>
          <line x1={X(p)} x2={X(p)} y1={Y(q)} y2={gy} stroke={C.teal} strokeWidth={2} strokeDasharray="6 5" />
          <circle cx={X(p)} cy={Y(q)} r={6.5} fill={C.teal} stroke="#fff" strokeWidth={2} />
          {!isM && <rect x={X(0)} y={Y(q) - 4} width={X(p) - X(0)} height={gy - Y(q) + 4} fill={C.teal} opacity={0.08} />}
          <Chip x={vx} y={Y(q) - 22} s={vs} size={18} C={C} color={C.teal} />
          <Chip x={x1 - ew / 2 - 16} y={y0 + 30} s={eq} size={esz} C={C} o={seg(km, 400, 900)} />
        </g>
      )}
    </g>
  );
}

/* ══════════ 장면 ══════════ */
const PH = { full: { addr: 500, fly: [500, 2700], roll: [2700, 3500], math: 3400 }, chip: { addr: 400, fly: [400, 1600], roll: [1600, 2400], math: 2200 }, putt: { addr: 400, fly: [400, 2200], roll: [2200, 2200], math: 1800 } };
export function GolfArt({ C, mode, ex, at }) {
  const { round, hi, T, t } = at;
  const hole = round.holes[hi], h = HOLES[hi], cam = holeCam(hi, ex), mini = ex === "mini", isM = mode === "m";
  const { pin } = holeInfo(h);
  let k = -1;
  for (let j = 0; j < hole.shots.length; j++) if (t >= T.shotsAt[j]) k = j;
  const s = k >= 0 ? hole.shots[k] : null, st = k >= 0 ? t - T.shotsAt[k] : 0;
  const ph = s ? PH[s.kind] : null;
  const kf = s ? seg(st, ph.fly[0], ph.fly[1], s.kind === "putt" ? E.out : (u) => u) : 0;
  const kr = s ? seg(st, ph.roll[0], ph.roll[1], E.out) : 0;
  const done = t >= T.endAt;
  // 지난 샷 길
  const trails = [];
  hole.shots.forEach((q, j) => {
    if (j >= k && !(done && j === hole.shots.length - 1)) return;
    if (j === k && !done) return;
    const A = cam.p(q.from), L = cam.p(q.land), Rr = cam.p(q.drop || q.rest);
    trails.push(<Path key={"a" + j} pts={[A, L]} stroke="#fff" sw={2} o={0.55} />);
    if (!q.drop) trails.push(<Path key={"b" + j} pts={[L, cam.p(q.rest)]} stroke="#fff" sw={1.6} dash="3 4" o={0.45} />);
    trails.push(<circle key={"c" + j} cx={Rr[0]} cy={Rr[1]} r={3.4} fill="#fff" opacity={0.7} />);
  });
  // 이번 샷: 공 자리
  let ball = cam.p(round.holes[hi].shots[0].from), aimEl = null, curEl = null, splash = 0;
  if (s) {
    const A = cam.p(s.from), L = cam.p(s.land), Rr = cam.p(s.rest);
    if (s.kind === "putt") {
      ball = [lerp(A[0], Rr[0], kf), lerp(A[1], Rr[1], kf)];
      curEl = <Path pts={[A, ball]} stroke={C.gold} sw={3} />;
    } else {
      const fl = [lerp(A[0], L[0], kf), lerp(A[1], L[1], kf)];
      ball = kr > 0 && !s.pen ? [lerp(L[0], Rr[0], kr), lerp(L[1], Rr[1], kr)] : fl;
      curEl = (
        <g>
          <Path pts={[A, fl]} stroke={C.gold} sw={3.4} />
          {kr > 0 && !s.pen && <Path pts={[L, ball]} stroke={C.gold} sw={2.4} dash="4 4" />}
        </g>
      );
      if (s.pen && kf >= 1) { splash = seg(st, ph.fly[1], ph.fly[1] + 300) * (1 - seg(st, ph.roll[1] + 600, ph.roll[1] + 1200)); if (st > ph.roll[1] + 900) ball = cam.p(s.drop); }
    }
    if (st < ph.fly[0] + 200) aimEl = <Path pts={[A, cam.p(s.kind === "putt" ? pin : s.land)]} stroke="#fff" sw={1.4} dash="5 7" o={0.5 * (1 - seg(st, ph.fly[0], ph.fly[0] + 200))} />;
  }
  if (done && hole.shots.length) { const ls = hole.shots[hole.shots.length - 1]; ball = cam.p(ls.made ? pin : ls.rest); }
  const lift = s && s.kind !== "putt" && kf > 0 && kf < 1 ? 4 * kf * (1 - kf) * Math.min(1, s.apex / 30) : 0;
  const intro = 1 - seg(t, GT.intro - 600, GT.intro);
  const endK = seg(t, T.endAt, T.endAt + 400);
  const sp = s && s.kind !== "putt" ? cam.p(s.land) : null;
  const m = st - (ph ? ph.math : 0);
  return (
    <g>
      <HoleMap i={hi} ex={ex} C={C} />
      {trails}
      {aimEl}
      {curEl}
      {s && s.pen && st > ph.roll[1] + 900 && (() => { const L = cam.p(s.land), D = cam.p(s.drop), o = seg(st, ph.roll[1] + 900, ph.roll[1] + 1300);
        return <g opacity={o}><Path pts={[L, D]} stroke="#bfe3ff" sw={2} dash="4 5" /><UText x={D[0] - 12} y={D[1] + 6} s="드롭" size={18} weight={800} anchor="end" fill={C.ink} halo={C.halo} C={C} /></g>; })()}
      {splash > 0 && sp && <g opacity={splash}><circle cx={sp[0]} cy={sp[1]} r={10 + 16 * splash} fill="none" stroke="#bfe3ff" strokeWidth={3} /><UText x={sp[0]} y={sp[1] - 24} s="풍덩! 벌타 1" size={22} weight={900} anchor="middle" fill="#bfe3ff" halo={C.halo} C={C} /></g>}
      {!(done && hole.shots[hole.shots.length - 1].made) && (
        <g>
          <ellipse cx={ball[0]} cy={ball[1] + 3} rx={6} ry={2.4} fill="#000" opacity={0.3} />
          <circle cx={ball[0]} cy={ball[1] - lift * 26} r={5.5 + lift * 3} fill="#fff" stroke="#333" strokeWidth={1.2} />
        </g>
      )}
      {intro > 0.01 && <HoleIntro C={C} ex={ex} hole={hole} o={intro} />}
      {endK > 0 && <EndLabel C={C} ex={ex} hole={hole} o={endK * (1 - seg(t, T.dur - 400, T.dur))} />}
      <SideView C={C} mode={mode} ex={ex} s={s} kf={s ? (s.kind === "putt" ? seg(st, ph.fly[0], ph.fly[1], E.out) : kf) : 0} km={m} />
      {!mini && <GolfPanel C={C} mode={mode} round={round} hi={hi} k={k} s={s} st={st} done={done} />}
      {mini && <GolfMini C={C} mode={mode} round={round} hi={hi} k={k} s={s} done={done} />}
    </g>
  );
}
function HoleIntro({ C, ex, hole, o }) {
  const [x0, y0, x1, y1] = TOP[ex];
  const s = `${hole.i + 1}번 홀 · 파 ${hole.par} · ${hole.len}m`;
  return <UText x={(x0 + x1) / 2} y={(y0 + y1) / 2 + 14} s={s} size={46} weight={900} anchor="middle" fill={C.ink} halo={C.halo} opacity={o} C={C} />;
}
function EndLabel({ C, ex, hole, o }) {
  const [x0, y0, x1] = TOP[ex];
  const name = hole.strokes === 1 ? "홀인원!" : scoreName(hole.score);
  return (
    <g opacity={o}>
      <UText x={(x0 + x1) / 2} y={y0 + 84} s={`${name}`} size={52} weight={900} anchor="middle" fill={hole.score < 0 ? C.gold : hole.score === 0 ? C.teal : C.coral} halo={C.halo} C={C} />
      <UText x={(x0 + x1) / 2} y={y0 + 124} s={`${hole.strokes}타 (파 ${hole.par})`} size={26} weight={800} anchor="middle" fill={C.ink} halo={C.halo} C={C} />
    </g>
  );
}

/** 설명 판(상세) */
function GolfPanel({ C, mode, round, hi, k, s, st, done }) {
  const { x, y, w, h } = PANEL;
  const hole = round.holes[hi], x0 = x + 22, mw = w - 44;
  const before = hi > 0 ? round.holes[hi - 1].total : 0;
  const strokesNow = k >= 0 ? hole.shots.slice(0, k + 1).reduce((n, q) => n + 1 + (q.pen ? 1 : 0), 0) : 0;
  const lines = s ? golfSteps(s, mode).map((L, j) => ({ ...L, col: L.col ? C[L.col] : undefined, at: (s.kind === "putt" ? 600 : 500) + j * (s.kind === "full" ? 620 : 520) })) : [];
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <FitText x={x0} y={y + 34} s={`수학 컨트리클럽 · 가상 라운드 · ${round.name}`} size={15} maxW={mw} minSize={10} weight={650} fill={C.soft} C={C} />
      <UText x={x0} y={y + 74} s={`${hole.i + 1}번 홀 · 파 ${hole.par} · ${hole.len}m`} size={26} weight={800} fill={C.ink} C={C} />
      <UText x={x0} y={y + 108} s={`${strokesNow}타째${s ? ` · ${s.club}` : ""}`} size={21} weight={750} fill={C.teal} C={C} />
      <UText x={x + w - 22} y={y + 108} s={totalText(before + (done ? hole.score : 0))} size={20} weight={800} anchor="end" fill={C.gold} C={C} />
      <line x1={x0} x2={x + w - 22} y1={y + 128} y2={y + 128} stroke={C.cardEdge} strokeWidth={1.2} />
      {s && <Lines x={x0} y={y + 170} lines={lines} t={st} C={C} size={21} lh={46} maxW={mw} hiSize={25} unit />}
      {/* 점수 카드 */}
      <ScoreCard x={x0} y={y + h - 128} w={mw} C={C} round={round} hi={hi} done={done} />
    </g>
  );
}
function ScoreCard({ x, y, w, C, round, hi, done }) {
  // 골프 점수 카드 표기: ○ 버디 · ◎ 이글 이하 · □ 보기 · ▣(겹사각) 더블 보기 이상
  const lw = 46, cw = (w - lw) / 9, rh = 30;
  const rows = [["홀", y + 22], ["파", y + 22 + rh], ["타수", y + 22 + rh * 2 + 4]];
  return (
    <g>
      <text x={x} y={y - 12} fontFamily={SANS} fontSize={16} fontWeight={750} fill={C.soft}>점수 카드 · 파 36</text>
      <rect x={x} y={y} width={w} height={rh * 3 + 10} rx={10} fill={C.ink} fillOpacity={0.04} stroke={C.cardEdge} strokeWidth={1} />
      <line x1={x + 6} x2={x + w - 6} y1={y + rh * 2 + 2} y2={y + rh * 2 + 2} stroke={C.cardEdge} strokeWidth={1} />
      {rows.map(([lab, yy]) => <text key={lab} x={x + 10} y={yy} fontFamily={SANS} fontSize={14} fontWeight={750} fill={C.soft}>{lab}</text>)}
      {round.holes.map((hl, j) => {
        const cx = x + lw + cw * j + cw / 2, show = j < hi || (j === hi && done);
        const col = hl.score < 0 ? C.gold : hl.score === 0 ? C.teal : C.coral;
        const sy = rows[2][1] - 6;
        return (
          <g key={j}>
            <text x={cx} y={rows[0][1]} textAnchor="middle" fontFamily={SANS} fontSize={16} fontWeight={750} fill={j === hi ? C.ink : C.soft}>{j + 1}</text>
            <text x={cx} y={rows[1][1]} textAnchor="middle" fontFamily={SANS} fontSize={16} fontWeight={650} fill={C.soft}>{hl.par}</text>
            {show && hl.score < 0 && <circle cx={cx} cy={sy} r={14} fill="none" stroke={col} strokeWidth={2} />}
            {show && hl.score < -1 && <circle cx={cx} cy={sy} r={10.5} fill="none" stroke={col} strokeWidth={1.6} />}
            {show && hl.score > 0 && <rect x={cx - 13} y={sy - 13} width={26} height={26} rx={2} fill="none" stroke={col} strokeWidth={2} />}
            {show && hl.score > 1 && <rect x={cx - 9.5} y={sy - 9.5} width={19} height={19} rx={1.5} fill="none" stroke={col} strokeWidth={1.4} />}
            {show && <text x={cx} y={sy + 6.5} textAnchor="middle" fontFamily={SANS} fontSize={hl.score < -1 || hl.score > 1 ? 15 : 19} fontWeight={850} fill={col}>{hl.strokes}</text>}
            {j === hi && !done && <circle cx={cx} cy={sy} r={4.5} fill={C.ink} opacity={0.5} />}
          </g>
        );
      })}
    </g>
  );
}
/** 최소화: 위 왼쪽 홀 · 타수, 위 오른쪽 합계 */
function GolfMini({ C, mode, round, hi, k, s, done }) {
  const hole = round.holes[hi], [x0, y0, x1] = TOP.mini;
  const before = hi > 0 ? round.holes[hi - 1].total : 0;
  const strokesNow = k >= 0 ? hole.shots.slice(0, k + 1).reduce((n, q) => n + 1 + (q.pen ? 1 : 0), 0) : 0;
  const a = `${hole.i + 1}번 홀 · 파 ${hole.par} · ${hole.len}m  —  ${strokesNow}타째${s ? ` · ${s.club}` : ""}${s && s.kind !== "putt" ? ` · 남은 거리 ${s.d0}m → ${s.d1}m` : s ? ` · ${s.d0}m 퍼트` : ""}`;
  const b = `${round.name} · ${totalText(before + (done ? hole.score : 0))}`;
  const wa = textW(a, 20, 750) + 34, wb = textW(b, 20, 800) + 34;
  return (
    <g>
      <rect x={x0 + 14} y={y0 + 14} width={wa} height={38} rx={19} fill={C.capBg} />
      <text x={x0 + 31} y={y0 + 40} fontFamily={SANS} fontSize={20} fontWeight={750} fill={C.capInk}>{a}</text>
      <rect x={x1 - wb - 14} y={y0 + 14} width={wb} height={38} rx={19} fill={C.capBg} />
      <text x={x1 - wb + 3} y={y0 + 40} fontFamily={SANS} fontSize={20} fontWeight={800} fill={C.gold}>{b}</text>
    </g>
  );
}

/* ══════════ 액자 ══════════ */
const DEF = { ex: "full", sp: 1, seed: 1 };
const fixPrm = (p = {}) => ({ ex: fixEx(p.ex), sp: SPEEDS.includes(p.sp) ? p.sp : 1, seed: Number.isInteger(p.seed) && p.seed > 0 && p.seed < 1e6 ? p.seed : 1 });
export function GolfFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const e = lab.elapsed() * P.sp;
  const at = golfAt(P.seed, e);
  const newRound = () => { lab.setPrm({ seed: P.seed + 100 }); poke(); };
  const jumpHole = (d) => {
    // 홀 단위로: 다음 홀 처음 · (지금 홀을 1.5초 넘게 봤으면) 이 홀 처음 · 아니면 앞 홀 처음
    const base = e - at.t;
    let target;
    if (d > 0) target = base + at.T.dur;
    else if (at.t > 1500 || base <= 0) target = base;
    else { const pv = golfAt(P.seed, base - 1); target = base - 1 - pv.t; }
    lab.jump(Math.max(0, target) / P.sp); poke();
  };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: newRound, toggleFs, onMode, poke }),
    ArrowRight: () => jumpHole(1), ArrowLeft: () => jumpHole(-1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="풀이"><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
      <span className="dsp-sep" />
      <ui.Btn title="이전 홀 (←)" onClick={() => jumpHole(-1)}><ui.Ic d="M15 5 8 12l7 7" /></ui.Btn>
      <ui.Btn title="다음 홀 (→)" onClick={() => jumpHole(1)}><ui.Ic d="m9 5 7 7-7 7" /></ui.Btn>
    </>
  );
  const title = { e: "골프로 보는 대칭과 비율", m: "골프로 보는 이차함수" };
  const sub = `수학 컨트리클럽(가상) · ${at.round.name} · 옆에서 본 공의 길 = 포물선`;
  const prog = (at.hi + at.t / at.T.dur) / 9;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="골프 샷으로 보는 포물선">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <GolfArt C={C} mode={Ly.mode} ex={P.ex} at={at} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={newRound}
        restartTitle="새 라운드" isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings} prog={prog} />
    </>
  );
}
export const GolfThumb = memo(function GolfThumb({ C, mode = "m" }) {
  const at = golfAt(3, 0);
  const T = at.T;
  return <GolfArt C={C} mode={mode} ex="full" at={{ ...at, t: T.shotsAt[0] + 4600 }} />;
});
