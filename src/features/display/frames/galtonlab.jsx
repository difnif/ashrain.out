// ashrain.out — 교실 모니터 「액자」: 구슬 낙하 실험 — 갈톤 보드 (frames/galtonlab.jsx)
// 해 보기(먼저): 못 줄 수와 구슬 수를 고르면 한 바퀴를 돈다. 판은 가운데 하나 — 설명은 판 곁에 붙는다.
//   ① 준비 — 못이 한 줄씩 박히며 못마다 「그 못까지 가는 길의 수」(파스칼의 삼각형)가 적히고, 통에 구슬이 찬다.
//   ② 낙하 — 물리 엔진으로 구슬을 실제로 떨어뜨린다. 첫 구슬은 금빛 자취로 따라가 「오른쪽으로 몇 번 → 몇 번째 칸」을 보여 준다.
//   ③ 정리 — 칸 아래 실제 개수, 초등은 쌓인 높이를 잇는 꺾은선(종 모양), 중등은 기대 개수(점선 칸) · 정규분포 곡선과
//            가운데 칸의 확률 C(R, R/2)/2^R 을 판 곁 말풍선으로.
//   통을 누르면(키보드 Enter) 기다리지 않고 바로 떨어뜨린다. 바퀴마다 씨앗이 바뀌어 결과가 조금씩 다르다.
//   다시 켜거나 오래 비웠다 돌아왔는데 따라 돌릴 양이 많으면 그 바퀴를 처음부터 튼다(구슬 수천 개를 한꺼번에 돌리느라 멈칫하지 않게).
// 풀이 보기: 구슬 낙하 실험 장면(../stories.js EXPLAIN.galton). 계산: ../galton.js · 물리: ../physics.js
import { memo, useCallback, useRef } from "react";
import { W, H, MText, Caption, SceneTitle, Path, mathWidth } from "../draw.jsx";
import { seg, E, clamp, fmt } from "../core.js";
import { EXPLAIN } from "../stories.js";
import { GALTON, galtonLayout, galtonWorld, pegsOf, wallsOf, dividersOf, binOf, comb, binom, spawnSpan } from "../galton.js";
import { simAt, circlesD, MARBLE } from "../physics.js";
import { LabShell, LabChrome, Stepper, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";

const LSK = "ash.display.lab.galton";
const DEF = { n: GALTON.NDEF, rows: GALTON.RDEF };
const fixPrm = (p = {}) => ({ n: GALTON.NS.includes(p.n) ? p.n : GALTON.NDEF, rows: GALTON.ROWS.includes(p.rows) ? p.rows : GALTON.RDEF });
const CX = 800;
const PREP = 5200, SETTLE = 4500, SUM = 11500;
const AREA = 4.15;                 // 쌓인 구슬 하나가 차지하는 넓이 ≈ AREA × r² (갈톤 장면과 같은 측정값)
const CATCHUP = 4000;              // 다시 켰을 때 따라 돌릴 양(구슬 수 × 초)이 이보다 크면 그 바퀴를 처음부터

/** 한 바퀴: 준비 → 낙하(세계 0초 = 바퀴 PREP) → 정리 */
export function glTimeline(N) {
  const drop0 = PREP + 500, drop1 = PREP + (0.5 + spawnSpan(N)) * 1000, done = drop1 + SETTLE;
  return { drop0, drop1, done, dur: done + SUM };
}
export function glAt(N, e) {
  const TL = glTimeline(N), x = Math.max(0, e);
  const c = Math.floor(x / TL.dur), t = x - c * TL.dur;
  return { c, t, TL, stage: t < PREP ? "prep" : t < TL.done ? "drop" : "sum" };
}
const LCACHE = new Map();
export function glLayout(R, N) {
  const k = `${R}|${N}`;
  if (!LCACHE.has(k)) {
    const L = galtonLayout({ R, N, cx: CX });
    L.pegs = pegsOf(L); L.walls = wallsOf(L); L.divs = dividersOf(L);
    L.half = (R / 2 + 0.5) * L.sx;
    LCACHE.set(k, L);
  }
  return LCACHE.get(k);
}
const seedOf = (c) => 11 + 7 * c;
const pegsD = (pegs, r, pick) => circlesD(pegs.map((p) => p.x), pegs.map((p) => p.y), pegs.map(() => r), pegs.map((_, i) => i).filter((i) => pick(pegs[i])));

/** 세계를 바퀴 시각 t 까지 — 쌓인 구슬의 그림 줄 · 칸별 개수 · 첫 구슬의 자취를 이어 붙여 둔다 */
function worldAt(L, c, t) {
  const Wd = simAt(`glab|${L.R}|${L.N}|${c}`, () => galtonWorld(L, seedOf(c)), Math.max(0, t - PREP));
  if (!Wd._fz) Wd._fz = { n: 0, d: ["", "", ""], cnt: new Array(L.R + 1).fill(0), landed: 0, trail: [], first: -1 };
  const F = Wd._fz;
  for (; F.n < Wd.frozenList.length; F.n++) {
    const i = Wd.frozenList[F.n];
    F.d[Wd.tag[i]] += circlesD(Wd.x, Wd.y, Wd.r, [i]);
    const k = binOf(L, Wd.x[i], Wd.y[i]);
    if (k >= 0) { F.cnt[k]++; F.landed++; }
    if (i === 0) F.first = k;
  }
  if (Wd.n && Wd.st[0] === MARBLE.LIVE) {
    const last = F.trail[F.trail.length - 1];
    if (!last || Math.hypot(Wd.x[0] - last[0], Wd.y[0] - last[1]) > 3) F.trail.push([Wd.x[0], Wd.y[0]]);
  }
  return Wd;
}

/* ══════════ 그리기 ══════════ */
export function GaltonArt({ C, mode, P, at, onHopper }) {
  const isM = mode === "m";
  const R = P.rows, N = P.n;
  const L = glLayout(R, N), TL = at.TL, t = at.t;
  const Wd = at.stage === "prep" ? null : worldAt(L, at.c, t);
  const F = Wd ? Wd._fz : null;
  const cols = [C.gold, C.coral, C.teal];
  const half = L.half, mid = R / 2;
  const boardO = seg(t, 0, 700);
  const rowT = (i) => 700 + (i * 3000) / R;
  const pasO = at.stage === "prep" ? seg(t, 900, 1400) : 1 - seg(t, TL.drop0 + 1500, TL.drop0 + 3000);
  const doneK = at.stage === "sum" ? seg(t, TL.done, TL.done + 900) : 0;
  const fill = at.stage === "prep" ? seg(t, 1200, PREP - 600, E.sine) : Wd ? Math.max(0, N - Wd.nextSpawn) / N : 0;
  const fallen = F ? F.landed : 0;
  const hOf = (k) => (N * binom(R, k) * AREA * L.r * L.r) / (L.sx - 3);
  const hAct = (v) => (v * AREA * L.r * L.r) / (L.sx - 3);
  const binsY = L.yFloor + 26;
  const canTap = !!onHopper && at.stage === "prep";
  return (
    <g>
      {/* 통 — 남은 구슬만큼 차 있다 */}
      <Hopper L={L} C={C} o={boardO} fill={fill} cols={cols} />
      {canTap && <HopperHit L={L} onHopper={onHopper} />}
      {/* 벽 · 칸막이 · 바닥 */}
      <g opacity={boardO}>
        {[L.walls.left, L.walls.right].map((w, i) => <Path key={i} pts={w} stroke={C.ink} sw={4.5} o={0.85} />)}
        {L.divs.map((d, i) => <Path key={i} pts={d} stroke={C.soft} sw={2.6} o={0.9} />)}
        <Path pts={[[L.cx - half - 2, L.yFloor + 3], [L.cx + half + 2, L.yFloor + 3]]} stroke={C.ink} sw={5} />
      </g>
      {/* 못 — 이론의 길(삼각형)은 또렷하게, 한 줄씩 박힌다 */}
      <path d={pegsD(L.pegs, L.rp, (p) => !p.tri)} fill={C.soft} opacity={0.38 * boardO} />
      {L.ys.map((y, i) => (
        <path key={i} d={pegsD(L.pegs, L.rp, (p) => p.tri && Math.abs(p.y - y) < 0.5)} fill={C.ink}
          opacity={0.85 * seg(t + (at.stage === "prep" ? 0 : 1e9), rowT(i), rowT(i) + 350)} />
      ))}
      {/* 못마다 그 못까지 가는 길의 수(파스칼의 삼각형) */}
      {pasO > 0.01 && L.ys.map((y, i) => {
        const a = (at.stage === "prep" ? seg(t, rowT(i) + 250, rowT(i) + 650) : 1) * pasO;
        return a > 0.01 && Array.from({ length: i + 1 }, (_, j) => (
          <MText key={`${i}-${j}`} x={L.cx + (j - i / 2) * L.sx} y={y - L.rp - 5} s={String(comb(i, j))}
            size={Math.min(18, L.sx * 0.36)} weight={700} anchor="middle" fill={C.teal} halo={C.halo} opacity={a} C={C} />
        ));
      })}
      {/* 구슬: 쌓인 것 + 움직이는 것 */}
      {F && cols.map((c, k) => <path key={"f" + k} d={F.d[k]} fill={c} />)}
      {Wd && cols.map((c, k) => <path key={"m" + k} d={circlesD(Wd.x, Wd.y, Wd.r, Wd.live.filter((i) => Wd.tag[i] === k))} fill={c} />)}
      {/* 첫 구슬의 자취 */}
      {F && F.trail.length > 3 && <Trail F={F} Wd={Wd} C={C} o={1 - doneK} />}
      {/* 정리: 중등 — 기대 개수(점선 칸) + 정규분포 곡선 · 초등 — 쌓인 높이를 잇는 꺾은선 */}
      {doneK > 0.01 && F && (isM
        ? <g opacity={doneK}>
          {L.bins.map((b, k) => { const h = hOf(k); return <rect key={k} x={b.x0 + 2} y={L.yFloor - h} width={L.sx - 4} height={h} fill="none" stroke={C.gold} strokeWidth={2} strokeDasharray="6 5" />; })}
          <Curve L={L} C={C} hOf={hOf} o={seg(t, TL.done + 1400, TL.done + 2600)} />
        </g>
        : <g opacity={doneK}>
          <Path pts={F.cnt.map((v, k) => [L.bins[k].xc, L.yFloor - hAct(v) - 6])} stroke={C.coral} sw={3.5} />
          {F.cnt.map((v, k) => <circle key={k} cx={L.bins[k].xc} cy={L.yFloor - hAct(v) - 6} r={5} fill={C.coral} />)}
        </g>)}
      {/* 칸 아래: 준비 중엔 칸으로 가는 길의 수, 떨어뜨린 뒤엔 실제 개수 */}
      <g pointerEvents="none">
        {L.bins.map((b, k) => {
          const pre = at.stage === "prep";
          const s = pre ? String(comb(R, k)) : String(F ? F.cnt[k] : 0);
          const hi = !pre && doneK > 0 && k === mid;
          return <MText key={k} x={b.xc} y={binsY} s={hi ? `‹${s}›` : s} size={Math.min(19, L.sx * 0.38)} weight={hi ? 800 : 700} anchor="middle"
            fill={pre ? C.teal : C.ink} opacity={pre ? seg(t, rowT(R - 1) + 400, rowT(R - 1) + 900) : 1} C={C} />;
        })}
        <MText x={L.cx - half - 14} y={binsY} s={at.stage === "prep" ? (isM ? "칸으로 가는 길" : "칸까지 가는 길") : (isM ? "개수" : "개수")} size={17} weight={700}
          anchor="end" fill={at.stage === "prep" ? C.teal : C.soft} C={C} />
      </g>
      {/* 왼쪽: 떨어진 구슬 · 첫 구슬 따라가기 */}
      <LeftNote C={C} L={L} at={at} F={F} N={N} fallen={fallen} fill={fill} isM={isM} />
      {/* 오른쪽: 준비 — 못의 수 읽는 법 · 정리 — 가운데 칸 */}
      <RightNote C={C} L={L} at={at} F={F} N={N} isM={isM} />
      <Caption t={t} C={C} y={862} size={31} caps={capsOf(isM, R, N, TL, F)} />
    </g>
  );
}

function capsOf(isM, R, N, TL, F) {
  const mid = R / 2;
  return isM ? [
    { t: 300, s: `갈톤 보드 — 못 ${R}줄, 구슬 ${N}개를 통에 담아요` },
    { t: 1500, s: "못에 적힌 수 = 그 못까지 가는 길의 수 = 위의 두 수의 합(파스칼의 삼각형)" },
    { t: PREP, s: "못마다 왼쪽·오른쪽으로 갈 가능성이 같다고 보면 — 떨어뜨려 볼까요?" },
    { t: TL.drop0 + Math.min(6000, (TL.drop1 - TL.drop0) * 0.4), s: `칸 k로 가는 길의 수 = 오른쪽으로 k번 가는 경우의 수 C(${R}, k)` },
    { t: TL.done, s: `가운데 칸으로 갈 확률 {${comb(R, mid)}/${2 ** R}} — 실제로 ${F ? F.cnt[mid] : 0}개, 가장 많이 모였어요` },
    { t: TL.done + 5200, s: "구슬과 줄이 많을수록 종 모양 곡선(정규분포)에 가까워져요" },
  ] : [
    { t: 300, s: `구슬 ${N}개를 통에 담아요 — 못은 ${R}줄` },
    { t: 1500, s: "못에 적힌 수는 그 못까지 가는 길의 수 — 가운데일수록 길이 많아요" },
    { t: PREP, s: "못에 부딪힐 때마다 왼쪽이나 오른쪽으로 튀어요" },
    { t: TL.drop0 + Math.min(6000, (TL.drop1 - TL.drop0) * 0.4), s: "어느 칸에 가장 많이 모일까요?" },
    { t: TL.done, s: "가운데에 가장 많이, 양 끝으로 갈수록 적게 모였어요" },
    { t: TL.done + 5200, s: "쌓인 높이를 꺾은선으로 이으면 종 모양이 돼요" },
  ];
}

/** 통: 위가 넓은 사다리꼴, 남은 구슬만큼 무늬로 채운다 */
function Hopper({ L, C, o, fill, cols }) {
  const top = L.walls.left[0][1], w1 = 120, w0 = L.sx * 0.55, y0 = top - 52;
  const shape = [[L.cx - w1, y0], [L.cx + w1, y0], [L.cx + w0, top], [L.cx - w0, top]];
  const lvl = top - 52 * clamp(fill);
  const pid = `glhop-${C.name}`;
  return (
    <g opacity={o}>
      <defs>
        <pattern id={pid} width={14} height={12} patternUnits="userSpaceOnUse">
          <circle cx={4} cy={4} r={3.6} fill={cols[0]} /><circle cx={11} cy={10} r={3.6} fill={cols[1]} />
          <circle cx={11} cy={2} r={2.2} fill={cols[2]} />
        </pattern>
        <clipPath id={pid + "-c"}><path d={`M${shape.map((p) => p.join(" ")).join("L")}Z`} /></clipPath>
      </defs>
      {fill > 0.001 && <rect x={L.cx - w1} y={lvl} width={2 * w1} height={top - lvl} fill={`url(#${pid})`} clipPath={`url(#${pid}-c)`} opacity={0.9} />}
      <Path pts={shape} closed stroke={C.ink} sw={3.5} fill={C.ink} fo={0.06} o={0.85} />
    </g>
  );
}
/** 준비 중: 통이나 판을 누르면 바로 떨어뜨린다 */
function HopperHit({ L, onHopper }) {
  const top = L.walls.left[0][1] - 60;
  return <rect x={L.cx - L.half - 20} y={top} width={2 * L.half + 40} height={L.yFloor - top} fill="transparent" style={{ cursor: "pointer" }}
    onPointerDown={(e) => e.stopPropagation()} onClick={onHopper} />;
}

/** 첫 구슬의 금빛 자취와 고리 */
function Trail({ F, Wd, C, o }) {
  if (o <= 0.01) return null;
  const live = Wd.st[0] === MARBLE.LIVE || Wd.st[0] === MARBLE.FROZEN;
  return (
    <g opacity={o} pointerEvents="none">
      <Path pts={F.trail} stroke={C.gold} sw={3} o={0.8} />
      {live && <circle cx={Wd.x[0]} cy={Wd.y[0]} r={Wd.r[0] + 5} fill="none" stroke={C.gold} strokeWidth={2.5} />}
    </g>
  );
}

/** 왼쪽 글: 구슬 수(준비 중엔 담기는 중) · 첫 구슬 따라가기 */
function LeftNote({ C, L, at, F, N, fallen, fill, isM }) {
  const x = 90;
  const pre = at.stage === "prep";
  const shown = pre ? Math.round(N * fill) : fallen;
  const head = pre ? "통에 담은 구슬" : "떨어진 구슬";
  const k0 = F ? F.first : -1;
  const R = L.R;
  return (
    <g pointerEvents="none">
      <MText x={x} y={250} s={head} size={25} weight={700} fill={C.soft} C={C} />
      <MText x={x} y={318} s={`‹${shown}›`} size={60} weight={800} C={C} />
      <MText x={x + mathWidth(String(shown), 60, 800) + 14} y={318} s={`/ ${N}개`} size={30} weight={600} fill={C.soft} C={C} />
      {pre && <MText x={x} y={372} s="판을 누르면 바로 떨어뜨려요" size={20} weight={650} fill={C.soft}
        opacity={seg(at.t, 1800, 2400) * (0.7 + 0.3 * Math.sin(at.t / 300))} C={C} />}
      {!pre && F && (
        <g opacity={seg(at.t, at.TL.drop0, at.TL.drop0 + 600) * (1 - seg(at.t, at.TL.done, at.TL.done + 900))}>
          <circle cx={x + 12} cy={398} r={9} fill="none" stroke={C.gold} strokeWidth={3} />
          <MText x={x + 32} y={406} s="첫 구슬 따라가기" size={23} weight={800} fill={C.gold} C={C} />
          {k0 >= 0 && <>
            <MText x={x} y={450} s={isM ? `오른쪽으로 ‹${k0}›번, 왼쪽으로 ${R - k0}번` : `오른쪽 ‹${k0}›번 · 왼쪽 ${R - k0}번`} size={25} weight={700} C={C} />
            <MText x={x} y={490} s={isM ? `→ 칸 ${k0} (오른쪽으로 간 횟수)` : `→ 왼쪽에서 ${k0 + 1}번째 칸`} size={24} weight={650} fill={C.soft} C={C} />
          </>}
        </g>
      )}
    </g>
  );
}

/** 오른쪽 글: 준비 — 못의 수 읽는 법 · 정리 — 가운데 칸의 확률(중등) / 가장 많이 모인 칸(초등), 칸까지 이은 선 */
function RightNote({ C, L, at, F, N, isM }) {
  const x = L.cx + L.half + 46, R = L.R, mid = R / 2, total = 2 ** R;
  const pre = at.stage === "prep";
  if (pre) {
    const o = seg(at.t, 1500, 2100);
    return (
      <g opacity={o} pointerEvents="none">
        <MText x={x} y={L.ys[0] + 6} s="못에 적힌 수" size={24} weight={800} fill={C.teal} C={C} />
        <MText x={x} y={L.ys[0] + 44} s={isM ? "= 그 못까지 가는 길의 수" : "= 그 못까지 가는 길"} size={23} weight={650} C={C} />
        <MText x={x} y={L.ys[0] + 80} s={isM ? "= 위의 두 수의 합" : "가운데일수록 많아요"} size={23} weight={650} C={C} />
        <MText x={x} y={L.ys[0] + 132} s={isM ? "구슬 하나가 가는 길" : "못마다 왼쪽 · 오른쪽"} size={21} weight={650} fill={C.soft} C={C} />
        <MText x={x} y={L.ys[0] + 164} s={isM ? `2를 ${R}번 곱해 ${total}가지` : "가능성이 반반"} size={21} weight={650} fill={C.soft} C={C} />
      </g>
    );
  }
  if (at.stage !== "sum" || !F) return null;
  const o = seg(at.t, at.TL.done + 600, at.TL.done + 1300);
  const p = comb(R, mid) / total, exp = N * p;
  const hTop = L.yFloor - (F.cnt[mid] * AREA * L.r * L.r) / (L.sx - 3) - 8;
  const by = Math.min(L.yFloor - 220, hTop - 40);
  const lines = isM ? [
    ["가운데 칸: 오른쪽으로 " + mid + "번", 23, C.soft, 700],
    [`확률 = {${comb(R, mid)}/${total}} ≈ ${fmt(p, 3)}`, 27, C.ink, 760],
    [`기대 ${fmt(exp, 1)}개 · 실제 ‹${F.cnt[mid]}›개`, 26, C.ink, 760],
  ] : [
    ["가장 많이 모인 칸", 23, C.soft, 700],
    [`가운데 칸 ‹${F.cnt[mid]}›개`, 28, C.ink, 800],
    [`양 끝 칸 ${F.cnt[0]}개 · ${F.cnt[R]}개`, 24, C.ink, 700],
  ];
  return (
    <g opacity={o} pointerEvents="none">
      <Path pts={[[x - 10, by + 30], [L.bins[mid].xc + L.sx * 0.3, hTop]]} stroke={C.gold} sw={2.5} dash="6 5" />
      <circle cx={L.bins[mid].xc + L.sx * 0.3} cy={hTop} r={5} fill={C.gold} />
      {lines.map(([s, sz, col, wt], i) => <MText key={i} x={x} y={by + i * 42} s={s} size={sz} weight={wt} fill={col} C={C} />)}
    </g>
  );
}

/** 중등: 쌓인 구슬 위의 정규분포 곡선 */
function Curve({ L, C, o, hOf }) {
  const { R, sx } = L, sig = Math.sqrt(R) / 2, mu = R / 2;
  const pts = [];
  for (let i = 0; i <= 160; i++) {
    const k = -0.5 + ((R + 1) * i) / 160;
    const f = Math.exp(-((k - mu) ** 2) / (2 * sig * sig)) / (sig * Math.sqrt(2 * Math.PI));
    const h = (hOf(mu) / binom(R, mu)) * f;
    pts.push([L.bins[0].x0 + sx * (k + 0.5), L.yFloor - h]);
  }
  return <Path pts={pts} stroke={C.coral} sw={4} o={o * 0.95} dash="12 8" />;
}

/* ══════════ 해 보기 ══════════ */
function GaltonTry({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui, viewSeg }) {
  const lab = useLabClock(LSK, DEF, fixPrm);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  // 다시 켰을 때 · 오래 비웠다 돌아왔을 때: 그 바퀴를 처음부터(구슬 수천 개를 따라 돌리느라 멈칫하지 않게)
  const last = useRef(null);
  const align = useCallback(() => {
    const A = glAt(P.n, lab.elapsed());
    if (A.stage !== "prep" && (P.n * (A.t - PREP)) / 1000 > CATCHUP) lab.jump(A.c * A.TL.dur);
  }, [P, lab]);
  if (last.current == null) { align(); last.current = lab.elapsed(); }
  useTicker(() => {
    const e = lab.elapsed();
    if (e - last.current > 3000) align();
    last.current = lab.elapsed();
    return !(lab.clk.current.held != null && layers.length < 2);
  });
  const e = lab.elapsed();
  const at = glAt(P.n, e);
  const skip = useCallback(() => {
    const A = glAt(P.n, lab.elapsed()), base = A.c * A.TL.dur;
    if (A.stage === "prep") lab.jump(base + PREP);
    else if (A.stage === "sum") lab.jump(base + A.TL.dur);
  }, [P, lab]);
  const step = (key, list, d) => { const i = list.indexOf(P[key]); const j = clamp(i + d, 0, list.length - 1); if (j !== i) lab.setPrm({ [key]: list[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: lab.restart, toggleFs, onMode, poke }),
    ArrowUp: () => step("n", GALTON.NS, 1), ArrowDown: () => step("n", GALTON.NS, -1),
    ArrowRight: () => step("rows", GALTON.ROWS, 1), ArrowLeft: () => step("rows", GALTON.ROWS, -1),
    Enter: () => { skip(); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="구슬"><Stepper ui={ui} label="구슬" value={P.n} options={GALTON.NS} unit="개" onChange={(v) => lab.setPrm({ n: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="못" sep><Stepper ui={ui} label="못" value={P.rows} options={GALTON.ROWS} unit="줄" onChange={(v) => lab.setPrm({ rows: v })} poke={poke} keyHint={["←", "→"]} /></Setting>
    </>
  );
  const title = { e: "구슬 낙하 실험", m: "갈톤 보드" };
  const sub = `해 보기 · 못 ${P.rows}줄 · 구슬 ${P.n}개 · ${at.c + 1}번째 실험`;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img"
        aria-label={`갈톤 보드 — 못 ${P.rows}줄, 구슬 ${P.n}개`}>
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <GaltonArt C={C} mode={Ly.mode} P={P} at={at} onHopper={Ly.top ? skip : null} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={lab.restart}
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} view={viewSeg} settings={settings}
        prog={at.t / at.TL.dur} />
    </>
  );
}

/** 구슬 낙하 실험 액자 — 해 보기(먼저) · 풀이 보기 */
export function GaltonFrame(props) {
  return <LabShell fkey="galton" label="구슬 낙하 실험" explain={EXPLAIN.galton} renderTry={({ viewSeg }) => <GaltonTry {...props} viewSeg={viewSeg} />} {...props} />;
}

/** 액자 목록의 작은 그림 — 못 8줄 · 구슬 200개, 떨어지는 중 */
export const GaltonThumb = memo(function GaltonThumb({ C, mode = "e" }) {
  const P = { n: 200, rows: 8 };
  const at = glAt(P.n, PREP + 4200);
  return <GaltonArt C={C} mode={mode} P={P} at={at} />;
});
