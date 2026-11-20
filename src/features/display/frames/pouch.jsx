// ashrain.out — 수학 호기심 액자: 주머니 공 꺼내기 — 확률 쌓기 (frames/pouch.jsx)
// 하노이의 탑 · 갈톤 보드처럼 계속 돈다. 전체 공 수 · 한 번에 꺼내는 수 · 주머니 수 · 색 가짓수를 고르고
// 「새로 섞기(R)」를 누르면 주머니마다 공이 무작위로 새로 담긴다. 차례마다:
//   ① 주머니 고르기(불빛이 주머니를 건너다니다 멈춘다) ② 한꺼번에 꺼내기 ③ 그 결과의 확률을 판서 ④ 꺼낸 공은 색깔 통에 차곡차곡.
//   오른쪽 판에는 지난 차례의 확률이 쌓이고, 「이 순서 그대로 나올 확률」을 곱해 간다.
//   중등: 경우의 수 ÷ 전체 경우의 수를 7 × 6 ÷ 2 꼴로(학원 해설과 같은 꼴) · 초등: 몇 가지 중 몇 가지.
// 계산: ../curio/pouch.js(씨앗으로 늘 같은 판 — 벽시계로 흘러 새로고침해도 이어진다)
import { memo, useMemo } from "react";
import { W, H, MText, SceneTitle } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { UText, Chip } from "../kit-story.jsx";
import { fs, hashSeed, rng, rint, shuffle, bigFracText, pctText, SPEEDS, spFmt, keepSpeed, keepPlace, EXS, fixEx, comb } from "../curio/kit.js";
import { POUCH, POUCH_DEF, fixPouch, roundOf, pouchAt, PT, combExpr } from "../curio/pouch.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { Lines, Panel, Small } from "./curio-kit.jsx";

const LSK = "ash.display.curio.pouch";
const ICON = ["r", "b", "y", "g", "p", "o"];
const colOf = (C, c) => C[POUCH.COLORS[c][1]];
const nameOf = (c) => POUCH.COLORS[c][0];
/* 한 차례 박자(1× ms) */
export const TT = { hop: [0, 1300], lift: [1300, 2500], calc: [2500, 5200], fall: [5200, 6300] };
const AREA_FULL = { x0: 60, x1: 1060, top: 170, bagH: 270 };
const AREA_MINI = { x0: 70, x1: 1530, top: 170, bagH: 270 };   // 최소화: 설명 판 없이 화면 너비 전체
const PANEL = { x: 1090, y: 150, w: 472, h: 720 };

/* ── 주머니 안 공 자리: 처음 담긴 공을 섞어 아래부터 쌓고, 꺼낼 때마다 그 색의 맨 위 공을 뺀다 ── */
function slotsOf(RD, P, round) {
  const R = rng(hashSeed("slots", P.seed, round, P.n, P.b, P.c));
  const slots = RD.start.map((cnt) => shuffle(cnt.flatMap((v, c) => Array(v).fill(c)), R));
  // 차례마다 뺀 자리 번호
  const alive = slots.map((s) => s.map(() => true));
  const removed = [];
  for (const T of RD.turns) {
    const gone = [];
    if (!P.rep) {
      for (const c of T.draw) {
        const s = slots[T.bag];
        for (let i = s.length - 1; i >= 0; i--) if (alive[T.bag][i] && s[i] === c) { alive[T.bag][i] = false; gone.push(i); break; }
      }
    }
    removed.push(gone);
  }
  return { slots, removed };
}
/** 주머니 그림 자리 */
function bagGeom(P, AREA) {
  const B = P.b, span = AREA.x1 - AREA.x0;
  const w = Math.min(AREA === AREA_MINI ? 260 : 230, (span - (B - 1) * 26) / B);
  const gap = B > 1 ? (span - B * w) / (B - 1) : 0;
  const maxIn = Math.max(...Array.from({ length: B }, () => P.n));
  return Array.from({ length: B }, (_, i) => {
    const x = B === 1 ? (AREA.x0 + AREA.x1) / 2 - w / 2 : AREA.x0 + i * (w + gap);
    return { x, w, cx: x + w / 2, top: AREA.top, bot: AREA.top + AREA.bagH, maxIn };
  });
}
/** 주머니 안 공 하나의 자리(아래부터 줄 맞춰) */
function slotPos(g, i, per, r) {
  const row = Math.floor(i / per), col = i % per;
  const off = row % 2 ? r : 0;
  const x = g.cx - ((per - 1) * 2 * r) / 2 + col * 2 * r + off - (row % 2 ? r * 0.5 : 0);
  const y = g.bot - 24 - r - row * r * 1.72;
  return [x, y];
}

function Bag({ g, C, hi, o = 1 }) {
  const { x, w, top, bot } = g;
  const neck = top + 34, cx = x + w / 2;
  const light = C.name === "light";
  const cloth = light ? "#d9bb8f" : "#7a5f45", edge = light ? "#8d6c43" : "#3e2c1d", band = light ? "#b2453b" : "#c4584b";
  const d = `M${cx - w * 0.2} ${neck}C${x - 8} ${neck + 40} ${x - 14} ${bot - 30} ${x + 18} ${bot - 6}Q${cx} ${bot + 14} ${x + w - 18} ${bot - 6}C${x + w + 14} ${bot - 30} ${x + w + 8} ${neck + 40} ${cx + w * 0.2} ${neck}Z`;
  return (
    <g opacity={o}>
      {hi > 0.001 && <path d={d} fill="none" stroke={C.gold} strokeWidth={10} opacity={0.35 * hi} />}
      <path d={d} fill={cloth} stroke={edge} strokeWidth={2.4} />
      <path d={`M${cx - w * 0.22} ${neck}L${cx - w * 0.16} ${top + 8}L${cx + w * 0.16} ${top + 8}L${cx + w * 0.22} ${neck}Z`} fill={cloth} stroke={edge} strokeWidth={2.2} />
      <rect x={cx - w * 0.24} y={neck - 7} width={w * 0.48} height={9} rx={4} fill={band} />
      {hi > 0.001 && <path d={d} fill="none" stroke={C.gold} strokeWidth={3.4} opacity={hi} />}
    </g>
  );
}
function Ball({ x, y, r, col, o = 1 }) {
  if (o <= 0.001) return null;
  return (
    <g opacity={o}>
      <circle cx={x} cy={y} r={r} fill={col} stroke="#000" strokeOpacity={0.35} strokeWidth={1.2} />
      <circle cx={x - r * 0.32} cy={y - r * 0.34} r={r * 0.32} fill="#fff" opacity={0.42} />
    </g>
  );
}

/* ══════════ 그리기 ══════════ */
export function PouchArt({ C, mode, P, at, ex = "full" }) {
  const isM = mode === "m", mini = ex === "mini", AREA = mini ? AREA_MINI : AREA_FULL;
  const { RD, round, stage, ti, t } = at;
  const G = useMemo(() => bagGeom(P, AREA), [P, AREA]);
  const TX = (AREA.x0 + AREA.x1) / 2;   // 쟁반 가운데
  const S = useMemo(() => slotsOf(RD, P, round), [RD, P, round]);
  const r = clamp(Math.min(19, Math.sqrt((G[0].w * 0.62 * (AREA.bagH - 70)) / Math.max(4, Math.max(...RD.start.map((b) => b.reduce((a, v) => a + v, 0))))) * 0.5), 7, 19);
  const per = Math.max(2, Math.floor((G[0].w * 0.66) / (2 * r)));
  const T = stage === "turn" ? RD.turns[ti] : null;
  // 지금 주머니 속: ti 차례까지 뺀 공(이번 차례 공은 꺼내는 순간 빠진다)
  const goneTo = stage === "setup" ? 0 : stage === "turn" ? ti + (t >= TT.lift[0] ? 1 : 0) : RD.turns.length;
  const gone = new Set();
  for (let j = 0; j < goneTo; j++) for (const i of S.removed[j]) gone.add(`${RD.turns[j].bag}:${i}`);
  // 주머니 고르기 불빛
  let hiBag = -1, hiK = 0;
  if (T) {
    const kh = seg(t, TT.hop[0], TT.hop[1], E.lin);
    if (P.b > 1 && kh < 1) {
      const R = rng(hashSeed("hop", P.seed, round, ti));
      const hops = 6 + rint(R, 3);
      const seq = Array.from({ length: hops }, () => T.elig[rint(R, T.elig.length)]);
      seq.push(T.bag);
      const idx = Math.min(seq.length - 1, Math.floor(E.out(kh) * seq.length));
      hiBag = seq[idx]; hiK = 0.75;
    } else { hiBag = T.bag; hiK = 1 - seg(t, TT.fall[1], PT.TURN); }
  }
  const setupK = stage === "setup" ? seg(t, 200, PT.SETUP - 400) : 1;
  // 꺼낸 공: 주머니 입구 → 쟁반 → 통
  const tubes = (stage === "turn" && T) ? (ti > 0 ? RD.turns[ti - 1].tubes : new Array(P.c).fill(0)) : stage === "sum" ? (RD.turns.at(-1)?.tubes || new Array(P.c).fill(0)) : new Array(P.c).fill(0);
  const tray = T ? T.draw.map((c, j) => [TX + (j - (T.draw.length - 1) / 2) * 64, 548]) : [];
  const tubeG = Array.from({ length: P.c }, (_, c) => ({ cx: AREA.x0 + 60 + ((AREA.x1 - AREA.x0 - 120) * (P.c === 1 ? 0.5 : c / (P.c - 1))), bot: 862, top: 640 }));
  const tr = 12, cap = Math.floor((862 - 640 - 16) / (tr * 1.9));
  const tubeBall = (c, j, total) => { const k = total > cap * 2 ? (cap * 2) / total : 1; const row = Math.floor(j / 2), col = j % 2; return [tubeG[c].cx - tr + col * tr * 2, tubeG[c].bot - 10 - tr - row * tr * 1.9 * k]; };
  const lifting = T ? seg(t, TT.lift[0], TT.lift[1], E.io) : 0;
  const falling = T ? seg(t, TT.fall[0], TT.fall[1], E.drop) : 0;
  return (
    <g>
      {/* 주머니 */}
      {G.map((g, bi) => {
        const s = S.slots[bi];
        const balls = [];
        s.forEach((c, i) => {
          if (gone.has(`${bi}:${i}`)) return;
          const [x, y] = slotPos(g, i, per, r);
          const appear = stage === "setup" ? seg(setupK, i / s.length * 0.8, i / s.length * 0.8 + 0.2) : 1;
          balls.push(<Ball key={i} x={x} y={y - (1 - appear) * 120} r={r} col={colOf(C, c)} o={appear} />);
        });
        const left = s.length - [...gone].filter((k) => k.startsWith(`${bi}:`)).length;
        const cnt = new Array(P.c).fill(0); s.forEach((c, i) => { if (!gone.has(`${bi}:${i}`)) cnt[c]++; });
        return (
          <g key={bi}>
            <Bag g={g} C={C} hi={bi === hiBag ? hiK : 0} />
            {balls}
            <UText x={g.cx} y={g.top - 6} s={`주머니 ${bi + 1} · ${left}개`} size={20} weight={800} anchor="middle" fill={bi === hiBag ? C.gold : C.ink} C={C} />
            <MText x={g.cx} y={g.bot + 34} s={cnt.map((v, c) => (v ? `⟪●${ICON[c]}⟫${v}` : "")).filter(Boolean).join(" ")} size={18} weight={700} anchor="middle" fill={C.soft} C={C} />
          </g>
        );
      })}
      {/* 쟁반 → 통 */}
      {T && T.draw.map((c, j) => {
        const g = G[T.bag];
        const from = [g.cx + (j - (T.draw.length - 1) / 2) * 18, g.top + 20];
        const to = tray[j];
        const seen = tubes[c] + T.draw.slice(0, j).filter((x) => x === c).length;
        const end = tubeBall(c, seen, tubes[c] + T.kc[c]);
        let p;
        if (falling > 0) p = [lerp(to[0], end[0], falling), lerp(to[1], end[1], falling) - Math.sin(Math.PI * falling) * 60];
        else p = [lerp(from[0], to[0], lifting), lerp(from[1], to[1], lifting) - Math.sin(Math.PI * lifting) * 90];
        return lifting > 0 ? <Ball key={j} x={p[0]} y={p[1]} r={falling > 0 ? lerp(22, tr, falling) : lerp(r, 22, lifting)} col={colOf(C, c)} /> : null;
      })}
      {T && lifting >= 1 && falling < 0.05 && !(mini && t >= TT.calc[0] + 1600) && <UText x={TX} y={604} s={T.draw.map((c) => nameOf(c)).join(" · ")} size={20} weight={700} anchor="middle" fill={C.soft} C={C} />}
      {mini && T && t >= TT.calc[0] + 1600 && (() => { const L = turnLines(T, P, mode); const hi = L[L.length - 1]; return <Chip x={TX} y={600} s={hi.s} size={28} C={C} color={C.gold} o={seg(t, TT.calc[0] + 1600, TT.calc[0] + 2100) * (1 - seg(t, TT.fall[1] - 300, TT.fall[1]))} />; })()}
      {/* 색깔 통 */}
      {tubeG.map((g, c) => {
        const n = tubes[c];
        return (
          <g key={c}>
            <rect x={g.cx - tr * 2 - 8} y={g.top} width={tr * 4 + 16} height={g.bot - g.top} rx={18} fill={C.ink} fillOpacity={0.05} stroke={C.ink} strokeOpacity={0.35} strokeWidth={2} />
            {Array.from({ length: n }, (_, j) => { const q = tubeBall(c, j, n); return <Ball key={j} x={q[0]} y={q[1]} r={tr} col={colOf(C, c)} />; })}
            <UText x={g.cx} y={g.bot + 26} s={`${nameOf(c)} ${n}`} size={17} weight={800} anchor="middle" fill={C.ink} C={C} />
          </g>
        );
      })}
      {!mini && <PouchPanel C={C} mode={mode} P={P} at={at} isM={isM} />}
      {mini && <PouchMini C={C} P={P} at={at} isM={isM} />}
    </g>
  );
}
/** 최소화 — 위 오른쪽에 판 · 꺼내기 차례와 「이 순서 그대로」 확률만 */
function PouchMini({ C, P, at, isM }) {
  const { RD, round, stage, ti, t } = at;
  const done = stage === "turn" ? ti + (t >= TT.fall[1] ? 1 : 0) : stage === "sum" ? RD.turns.length : 0;
  const cum = done ? RD.turns[done - 1].cum : null;
  const a = `${round + 1}번째 판 · ${stage === "turn" ? `${ti + 1}번째 꺼내기` : stage === "sum" ? "판 끝" : "공 담기"} · ${P.rep ? "다시 넣기" : "빼 두기"}`;
  return (
    <g>
      <Chip x={1552} y={522} s={a} size={19} C={C} anchor="end" color={isM ? C.teal : C.coral} />
      {cum && <Chip x={1552} y={562} s={`이 순서 그대로: ${bigFracText(cum[0], cum[1], 8)}${pctText(cum[0], cum[1]) ? ` (${pctText(cum[0], cum[1])})` : ""}`} size={19} C={C} anchor="end" color={C.gold} />}
    </g>
  );
}

/** 이번 차례 확률 줄 */
export function turnLines(T, P, mode) {
  const out = [];
  const k = P.k, E1 = T.elig.length;
  const icons = T.draw.map((c) => `⟪●${ICON[c]}⟫`).join("");
  const pairs = T.kc.map((v, c) => [c, v]).filter(([, v]) => v);
  const favV = pairs.reduce((a, [c, v]) => a * comb(T.before[c], v), 1), totV = comb(T.Nb, k);
  if (mode === "m") {
    out.push({ s: E1 > 1 ? `주머니 고르기: ${E1}개 중 하나 → {1/${E1}}` : "주머니 고르기: 하나뿐 → 1" });
    out.push({ s: `${icons} 나오는 경우: ${pairs.map(([c, v]) => (pairs.length > 1 && v > 1 ? `(${combExpr(T.before[c], v)})` : combExpr(T.before[c], v))).join(" × ")} = ${favV}`, small: k > 2 });
    out.push({ s: `전체 경우: ${combExpr(T.Nb, k)} = ${totV}` });
    out.push({ s: `${icons}일 확률 = {${favV}/${totV}}${fs(favV, totV) !== `{${favV}/${totV}}` ? ` = ${fs(favV, totV)}` : ""}` });
    out.push({ s: `확률 = ${E1 > 1 ? `{1/${E1}} × ` : ""}${fs(favV, totV)} = ${bigFracText(T.num, T.den)}`, hi: true });
  } else {
    out.push({ s: E1 > 1 ? `주머니 ${E1}개 중 하나를 골라요 → {1/${E1}}` : "주머니가 하나뿐이에요" });
    out.push({ s: `${T.Nb}개 중 ${k}개를 꺼내는 방법 ${totV}가지` });
    const ga = POUCH.COLORS[T.draw[T.draw.length - 1]][0] === "보라" ? "가" : "이";   // 마지막 공의 색 이름(받침)으로 이/가
    out.push({ s: `그중 ${icons}${ga} 나오는 방법 ${favV}가지 → {${favV}/${totV}}` });
    out.push({ s: `확률 = ${bigFracText(T.num, T.den)}`, hi: true });
  }
  return out;
}

function PouchPanel({ C, mode, P, at, isM }) {
  const { x, y, w, h } = PANEL, x0 = x + 24, mw = w - 48;
  const { RD, round, stage, ti, t } = at;
  const T = stage === "turn" ? RD.turns[ti] : null;
  const lines = T ? turnLines(T, P, mode).map((L, j) => ({ ...L, at: TT.calc[0] + j * 520 })) : [];
  // 지난 차례 기록(최근 4)
  const done = stage === "turn" ? ti + (t >= TT.fall[1] ? 1 : 0) : stage === "sum" ? RD.turns.length : 0;
  const logs = RD.turns.slice(Math.max(0, done - 4), done).map((q, j, arr) => ({ q, n: done - arr.length + j + 1 }));
  const cum = done ? RD.turns[done - 1].cum : null;
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <UText x={x0} y={y + 40} s={`${round + 1}번째 판 · ${P.rep ? "다시 넣기" : "빼 두기"}`} size={20} weight={800} fill={isM ? C.teal : C.coral} C={C} />
      <Small x={x + w - 24} y={y + 38} s={`공 ${P.n}개 · 주머니 ${P.b}개 · ${P.c}색 · 한 번에 ${P.k}개`} size={15} C={C} anchor="end" />
      {stage === "setup" && (
        <g opacity={seg(t, 200, 700)}>
          <UText x={x0} y={y + 100} s="새 판! 주머니에 공을 담아요" size={28} weight={800} C={C} />
          {RD.start.map((cnt, bi) => (
            <MText key={bi} x={x0} y={y + 150 + bi * 40} s={`주머니 ${bi + 1}: ${cnt.map((v, c) => (v ? `⟪●${ICON[c]}⟫${v}` : "")).filter(Boolean).join("  ")}`} size={22} weight={700} C={C} />
          ))}
        </g>
      )}
      {T && (
        <g>
          <UText x={x0} y={y + 88} s={`${ti + 1}번째 꺼내기`} size={26} weight={800} C={C} />
          <Lines x={x0} y={y + 136} lines={lines} t={t} C={C} size={22} lh={46} maxW={mw} hiSize={28} />
        </g>
      )}
      {stage === "sum" && (
        <g opacity={seg(t, 0, 500)}>
          <UText x={x0} y={y + 96} s={`이번 판 끝 — ${RD.turns.length}번 꺼냈어요`} size={26} weight={800} C={C} />
          {P.rep && RD.expect ? (
            <>
              <Small x={x0} y={y + 134} s="색마다 나올 것으로 기대한 개수 vs 실제로 나온 개수" size={16} C={C} />
              {RD.expect.map((ev, c) => (
                <MText key={c} x={x0} y={y + 174 + c * 38} s={`⟪●${ICON[c]}⟫ 기대 ${ev.toFixed(1)}개 · 실제 ${RD.turns.at(-1).tubes[c]}개`} size={21} weight={700} C={C} />
              ))}
            </>
          ) : (
            <MText x={x0} y={y + 140} s="꺼낸 공은 처음 주머니에 담긴 공과 같아요" size={19} weight={650} fill={C.soft} C={C} />
          )}
        </g>
      )}
      {/* 기록 */}
      <line x1={x0} x2={x + w - 24} y1={y + 400} y2={y + 400} stroke={C.cardEdge} strokeWidth={1.2} />
      <Small x={x0} y={y + 428} s="지난 꺼내기" size={15} C={C} />
      {logs.map(({ q, n }, j) => (
        <MText key={n} x={x0} y={y + 466 + j * 40} s={`${n}. 주머니 ${q.bag + 1}  ${q.draw.map((c) => `⟪●${ICON[c]}⟫`).join("")}  → ${bigFracText(q.num, q.den)}`} size={20} weight={650}
          fill={j === logs.length - 1 ? C.ink : C.soft} C={C} />
      ))}
      {cum && (
        <g>
          <Small x={x0} y={y + h - 64} s="이번 판 지금까지, 이 순서 그대로 나올 확률" size={15} C={C} />
          <MText x={x0} y={y + h - 26} s={`${bigFracText(cum[0], cum[1], 8)}${pctText(cum[0], cum[1]) ? `  (${pctText(cum[0], cum[1])})` : ""}`} size={24} weight={800} fill={C.gold} C={C} />
        </g>
      )}
    </g>
  );
}

/* ══════════ 액자 ══════════ */
const DEF_EX = { ...POUCH_DEF, ex: "full" };
const fixEx2 = (p = {}) => ({ ...fixPouch(p), ex: fixEx(p.ex) });
export function PouchFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, DEF_EX, fixEx2);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const at = pouchAt(P, lab.elapsed() * P.sp);
  const reshuffle = () => lab.setPrm({ seed: (P.seed % 999983) + 1 });
  const stepIn = (key, list, d) => { const i = list.indexOf(P[key]); const j = clamp(i + d, 0, list.length - 1); if (j !== i) lab.setPrm({ [key]: list[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: reshuffle, toggleFs, onMode, poke }),
    ArrowUp: () => stepIn("n", POUCH.NS, 1), ArrowDown: () => stepIn("n", POUCH.NS, -1),
    ArrowRight: () => stepIn("k", POUCH.KS, 1), ArrowLeft: () => stepIn("k", POUCH.KS, -1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="공"><Stepper ui={ui} label="공" value={P.n} options={POUCH.NS} unit="개" onChange={(v) => lab.setPrm({ n: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="한 번에" sep><Stepper ui={ui} label="한 번에" value={P.k} options={POUCH.KS} unit="개" onChange={(v) => lab.setPrm({ k: v })} poke={poke} keyHint={["←", "→"]} /></Setting>
      <Setting label="주머니" sep><Stepper ui={ui} label="주머니" value={P.b} options={POUCH.BS} unit="개" onChange={(v) => lab.setPrm({ b: v })} poke={poke} /></Setting>
      <Setting label="색" sep><Stepper ui={ui} label="색" value={P.c} options={POUCH.CS} unit="가지" onChange={(v) => lab.setPrm({ c: v })} poke={poke} /></Setting>
      <Setting label="꺼낸 공" sep><Seg label="꺼낸 공" value={P.rep} options={[[false, "빼 두기"], [true, "다시 넣기"]]} onChange={(v) => lab.setPrm({ rep: v })} poke={poke} /></Setting>
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.sp} options={SPEEDS} fmt={spFmt} onChange={(v) => lab.setPrm({ sp: v }, keepSpeed)} poke={poke} /></Setting>
    </>
  );
  const title = { e: "주머니에서 공 꺼내기", m: "주머니 공 꺼내기 — 확률 쌓기" };
  const sub = `주머니를 고르고, 공 ${P.k}개를 한꺼번에 — 나온 결과의 확률을 차곡차곡`;
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="주머니에서 공을 꺼내며 확률을 계산하는 액자">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <PouchArt C={C} mode={Ly.mode} P={P} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={reshuffle} restartTitle="새로 섞기"
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={at.D ? (at.stage === "setup" ? at.t : PT.SETUP + (at.stage === "turn" ? at.ti * PT.TURN + at.t : at.RD.turns.length * PT.TURN + at.t)) / at.D : 0} />
    </>
  );
}

export const PouchThumb = memo(function PouchThumb({ C, mode = "m" }) {
  const P = fixPouch({ ...POUCH_DEF, seed: 3 });
  const at = pouchAt(P, PT.SETUP + 2 * PT.TURN + 3600);
  return <PouchArt C={C} mode={mode} P={P} at={at} />;
});
