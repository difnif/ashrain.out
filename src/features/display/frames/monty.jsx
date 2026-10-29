// ashrain.out — 교실 모니터 「액자」: 몬티홀 — 바꿀까, 그대로 둘까? (frames/monty.jsx)
// 해 보기(먼저): 문 n개 · 사회자가 여는 문 k개 · 사회자가 답을 아는지 · 직접/저절로 · 빠르기를 고른다.
//   직접 — 반 아이들이 문을 눌러 고르고(키보드 1~9 · 0), 사회자가 문을 연 뒤 그대로/바꾸기도 눌러 정한다. 반 기록이 쌓인다.
//   저절로 — 컴퓨터가 한 바퀴(자연스럽게 30판 · 빠르게 300판)를 쉬지 않고 해, 그대로·바꾸기 두 기록이 이론값으로 다가간다.
//   판 사이사이에 풀이가 끼어든다: 문 아래 막대(그 문 뒤에 자동차가 있을 확률)가 사회자가 연 문에서 닫힌 다른 문으로 옮겨 가고,
//   그 아래 한 줄이 「내 문 {1/n} · 고르지 않은 문 모두 {(n−1)/n}」을 말해 준다.
// 풀이 보기: 몬티홀 · 5지선다 찍기 · 맞물린 답 장면을 그대로 돌린다(../stories.js EXPLAIN.monty).
// 계산: ../montylab.js
import { memo, useCallback, useRef } from "react";
import { W, H, MText, Caption, SceneTitle, mathWidth } from "../draw.jsx";
import { seg, E, clamp, lerp } from "../core.js";
import { Car, Goat } from "../scenes/monty.jsx";
import { EXPLAIN } from "../stories.js";
import {
  MLAB, KS, fixPrm, theory, val, ftx, pct, red, luck, hostOpens, shares, PACE, openGap, phases, autoAt, remapAuto,
  emptyTally, tallyKey, handDur,
} from "../montylab.js";
import { LabShell, LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys, lsRead, lsWrite } from "./xkit.jsx";

const LS = { lab: "ash.display.lab.monty", hand: "ash.display.lab.monty.hand" };
const DEF = { n: MLAB.NDEF, k: MLAB.KDEF, know: true, play: "hand", speed: "natural" };
const DOOR = { y0: 226, h: 220, x0: 110, x1: 1490 };
const BAR = { base: 612, h: 130 };
const LINE_Y = 662;
const TAL = { x0: 360, x1: 980, y: [738, 782], th: 22, name: 336 };

/** 문의 자리: 왼쪽 x · 너비 · 사이 */
const GEO = new Map();
function geom(n) {
  if (!GEO.has(n)) {
    const gap = n <= 4 ? 60 : n <= 6 ? 38 : 22;
    const w = Math.min(176, (DOOR.x1 - DOOR.x0 - (n - 1) * gap) / n);
    const tot = n * w + (n - 1) * gap;
    GEO.set(n, { w, gap, xs: Array.from({ length: n }, (_, i) => 800 - tot / 2 + i * (w + gap)) });
  }
  return GEO.get(n);
}

/* ══════════ 직접 하기: 반 기록 ══════════ */
function loadHand(P) {
  const all = lsRead(LS.hand);
  const o = all && typeof all === "object" ? all[tallyKey(P)] : null;
  if (o && Number.isInteger(o.seed) && Number.isInteger(o.r) && o.r >= 0 && o.tally && typeof o.tally === "object") {
    const t = emptyTally();
    for (const k of Object.keys(t)) if (Number.isInteger(o.tally[k]) && o.tally[k] >= 0) t[k] = o.tally[k];
    return { seed: o.seed >>> 0 || 1, r: o.r, tally: t };
  }
  return { seed: (Math.floor(Math.random() * 4294967295) >>> 0) || 1, r: 0, tally: emptyTally() };
}
function saveHand(P, h) {
  const all = lsRead(LS.hand);
  const o = all && typeof all === "object" ? all : {};
  o[tallyKey(P)] = { seed: h.seed, r: h.r, tally: h.tally };
  lsWrite(LS.hand, o);
}

/* ══════════ 그리기 ══════════ */
/** 지금 보여 줄 한 판(vm)과 설정으로 문 · 막대 · 한 줄 풀이 · 기록 · 자막 */
export function MontyArt({ C, mode, P, vm, onDoor, live = false, caps = null }) {
  const isM = mode === "m";
  const { n, k, know } = P;
  const T = theory(n, k, know);
  const G = geom(n);
  const pace = PACE[vm.auto ? P.speed : "natural"];
  const { phase, ms, p } = vm;
  const picked = vm.pick != null && !(vm.auto && phase === "pick" && p < 0.3);
  const openK = (d) => {
    if (vm.pick == null) return 0;
    const hostI = vm.opened.indexOf(d);
    if (phase === "open") { if (hostI < 0) return 0; const a = hostI * openGap(k, pace); return seg(ms, a, a + pace.door, E.out); }
    if (hostI >= 0) return 1;
    if (phase === "reveal") {
      const order = revealOrder(vm), j = order.indexOf(d);
      return seg(ms, j * 120, j * 120 + pace.door, E.out);
    }
    return phase === "done" || phase === "sum" ? 1 : 0;
  };
  // 막대: 고른 뒤 1/n → 사회자가 연 뒤의 몫
  const after = vm.pick != null && !vm.void ? shares(n, k, know, vm.pick, vm.opened, "after") : null;
  const flowK = phase === "flow" ? E.io(clamp(p / 0.8)) : ["decide", "reveal", "done"].includes(phase) ? 1 : 0;
  const barsO = phase === "sum" ? 1 - E.sine(clamp(vm.sumP * 4)) : phase === "void" ? 1 - 0.65 * seg(ms, 0, 500) : 1;
  const sw = vm.auto ? vm.sw : vm.choice != null && vm.choice !== vm.pick ? vm.choice : null;
  const deciding = !vm.auto && phase === "decide";
  const pulse = 0.5 + 0.5 * Math.sin((ms || 0) / 330);
  const capsL = caps ? caps[mode] : null;
  return (
    <g>
      {/* 문 */}
      {G.xs.map((x, d) => {
        const op = openK(d);
        const isPick = picked && d === vm.pick, isSw = sw === d && ["decide", "reveal", "done", "sum"].includes(phase);
        const ringO = phase === "sum" ? 0 : isPick ? (vm.auto && phase === "pick" ? seg(p, 0.3, 0.6) : 1) : isSw ? (vm.auto && phase === "decide" ? seg(p, 0.15, 0.5) : 1) : 0;
        const can = live && onDoor && ((phase === "pick" && !vm.auto) || (deciding && !vm.opened.includes(d)) || (!vm.auto && phase === "done"));
        const glowCar = d === vm.car && op > 0.4 && (phase === "reveal" || phase === "done" || phase === "sum");
        const voidCar = vm.void && d === vm.car && vm.opened.includes(d) && (phase === "void" || (phase === "open" && op > 0.5));
        return (
          <g key={d}>
            <Door C={C} x={x} w={G.w} num={d + 1} open={op} car={d === vm.car} glow={glowCar ? seg(op, 0.4, 1) : 0} voidCar={voidCar}
              ring={ringO} ringCol={isPick ? C.sky : C.gold}
              dim={phase === "sum" ? 0.3 : vm.opened.includes(d) && phase !== "open" && !voidCar ? 0.72 : 1}
              hint={(phase === "pick" && !vm.auto) || (deciding && !vm.opened.includes(d)) ? 0.35 + 0.45 * pulse : 0} />
            <DoorChips C={C} x={x + G.w / 2} d={d} vm={vm} isM={isM} isPick={isPick} isSw={isSw} ringO={ringO} deciding={deciding} pulse={pulse} />
            {can && (
              <rect x={x - G.gap / 2} y={DOOR.y0 - 50} width={G.w + G.gap} height={BAR.base - DOOR.y0 + 64} fill="transparent"
                style={{ cursor: "pointer" }} onPointerDown={(e) => e.stopPropagation()} onClick={() => onDoor(d)} />
            )}
          </g>
        );
      })}
      {/* 문 아래 막대 = 그 문 뒤에 자동차가 있을 확률 */}
      {barsO > 0.01 && (
        <g opacity={barsO} pointerEvents="none">
          {G.xs.map((x, d) => {
            const cx = x + G.w / 2, bw = Math.min(58, G.w * 0.42);
            const v = after ? lerp(1 / n, after[d], flowK) : 1 / n;
            const h = v * BAR.h;
            const lab = !after || flowK >= 0.98 || flowK <= 0.02
              ? (after && flowK >= 0.98 ? (vm.opened.includes(d) ? "0" : d === vm.pick ? ftx(T.pick) : ftx(T.each)) : ftx(red(1, n)))
              : null;
            const col = picked && d === vm.pick ? C.sky : picked ? C.gold : C.soft;
            return (
              <g key={d}>
                <line x1={x} x2={x + G.w} y1={BAR.base} y2={BAR.base} stroke={C.ink} strokeWidth={2.4} opacity={0.75} />
                {h > 0.5 && <rect x={cx - bw / 2} y={BAR.base - h} width={bw} height={h} rx={4} fill={col} fillOpacity={0.85} />}
                {lab && <MText x={cx} y={BAR.base - h - 12} s={lab} size={n > 7 ? 24 : 28} weight={800} anchor="middle" fill={col === C.soft ? C.ink : col}
                  halo={C.halo} C={C} />}
              </g>
            );
          })}
        </g>
      )}
      {/* 한 줄 풀이: 내 문 · 고르지 않은 문 */}
      {picked && phase !== "sum" && <ShareLine C={C} vm={vm} P={P} T={T} isM={isM} o={barsO} />}
      {/* 기록 */}
      <Tally C={C} vm={vm} P={P} T={T} isM={isM} />
      {/* 한 바퀴 정리(저절로) */}
      {phase === "sum" && <Summary C={C} vm={vm} P={P} T={T} isM={isM} />}
      {capsL && <Caption t={capsL.t} caps={capsL.caps} C={C} y={862} size={31} />}
    </g>
  );
}

/** 결과를 열 때 여는 차례: 고른 문 · 바꾼 문 먼저, 나머지는 왼쪽부터 */
function revealOrder(vm) {
  const first = [vm.pick, vm.auto ? vm.sw : vm.choice].filter((d, i, a) => d != null && a.indexOf(d) === i);
  const rest = [];
  for (let d = 0; d < vm.n; d++) if (!first.includes(d) && !vm.opened.includes(d)) rest.push(d);
  return [...first, ...rest];
}

/** 문 하나: 문틀 · 문짝(열리면 왼쪽 경첩으로 접힌다) · 문 뒤(염소 또는 자동차) · 번호 · 고른 표시 */
function Door({ C, x, w, num, open, car, glow, voidCar, ring, ringCol, dim, hint }) {
  const y0 = DOOR.y0, h = DOOR.h;
  const pw = w * (1 - 0.86 * open), skew = 14 * open;
  return (
    <g opacity={dim}>
      <rect x={x} y={y0} width={w} height={h} rx={4} fill={C.ink} fillOpacity={0.08} />
      {glow > 0.01 && <ellipse cx={x + w / 2} cy={y0 + h * 0.62} rx={w * 0.62} ry={h * 0.34} fill={C.gold} opacity={0.32 * glow} />}
      {voidCar && <rect x={x + 3} y={y0 + 3} width={w - 6} height={h - 6} rx={4} fill={C.coral} opacity={0.22} />}
      {open > 0.02 && (car ? <Car C={C} cx={x + w / 2} cy={y0 + h * 0.62} s={w * 0.8} /> : <Goat C={C} cx={x + w / 2} cy={y0 + h * 0.56} s={w * 0.6} />)}
      <path d={`M${x} ${y0} L${x + pw} ${y0 + skew} L${x + pw} ${y0 + h - skew} L${x} ${y0 + h} Z`} fill={C.wood} fillOpacity={0.92}
        stroke={C.woodEdge} strokeWidth={3} strokeLinejoin="round" />
      {open < 0.6 && (
        <g opacity={1 - open / 0.6}>
          <circle cx={x + pw / 2} cy={y0 + h * 0.36} r={Math.min(30, w * 0.22)} fill={C.paper} stroke={C.woodEdge} strokeWidth={3} />
          <text x={x + pw / 2} y={y0 + h * 0.36 + Math.min(32, w * 0.24) * 0.35} fontSize={Math.min(32, w * 0.24)} fontWeight={800} textAnchor="middle"
            fill={C.ink}>{num}</text>
          <circle cx={x + pw - 16} cy={y0 + h * 0.58} r={5} fill={C.woodEdge} />
        </g>
      )}
      <rect x={x} y={y0} width={w} height={h} rx={4} fill="none" stroke={C.ink} strokeWidth={3.5} opacity={0.8} />
      {hint > 0.01 && <rect x={x - 5} y={y0 - 5} width={w + 10} height={h + 10} rx={7} fill="none" stroke={C.gold} strokeWidth={3} opacity={hint} strokeDasharray="10 7" />}
      {ring > 0.01 && <rect x={x - 7} y={y0 - 7} width={w + 14} height={h + 14} rx={8} fill="none" stroke={ringCol} strokeWidth={5.5} opacity={ring} />}
      {voidCar && <rect x={x - 7} y={y0 - 7} width={w + 14} height={h + 14} rx={8} fill="none" stroke={C.coral} strokeWidth={5.5} />}
    </g>
  );
}

/** 문 위 이름표: 고른 문 · 그대로/바꾸기(고르는 중) · 결과(✓ 자동차 / × 염소) */
function DoorChips({ C, x, d, vm, isM, isPick, isSw, ringO, deciding, pulse }) {
  const y = DOOR.y0 - 26;
  const { phase } = vm;
  const res = (phase === "reveal" && vm.ms > 380) || phase === "done" || phase === "sum";
  const chips = [];
  if (deciding && !vm.opened.includes(d)) {
    chips.push({ s: d === vm.pick ? "그대로" : "바꾸기", col: d === vm.pick ? C.sky : C.gold, o: 0.75 + 0.25 * pulse });
  } else if (isPick && ringO > 0.01) {
    const after = ["decide", "reveal", "done"].includes(phase);
    const mark = d === vm.car ? "⟪✓⟫" : "⟪×⟫";
    const who = vm.auto ? "컴퓨터가 고른 문" : isM ? "처음 고른 문" : "내가 고른 문";
    let s = who;
    if (after && (vm.auto || vm.choice === vm.pick)) s = res ? `그대로 ${mark}` : "그대로";
    else if (after && res && !vm.auto && vm.choice != null) s = `그대로였다면 ${mark}`;
    chips.push({ s, col: C.sky, o: ringO });
  } else if (isSw && ringO > 0.01) {
    chips.push({ s: res ? `바꾸기 ${d === vm.car ? "⟪✓⟫" : "⟪×⟫"}` : "바꾸기", col: C.gold, o: ringO });
  } else if (vm.void && d === vm.car && vm.opened.includes(d) && (phase === "void" || phase === "open")) {
    chips.push({ s: "자동차가 나왔어요!", col: C.coral, o: phase === "open" ? seg(vm.ms, 400, 800) : 1 });
  }
  return chips.map((c, i) => {
    const w = mathWidth(c.s, 24, 800) + 30;
    return (
      <g key={i} opacity={c.o} pointerEvents="none">
        <rect x={x - w / 2} y={y - 22} width={w} height={36} rx={18} fill={C.halo} stroke={c.col} strokeWidth={2.5} />
        <MText x={x} y={y + 4} s={c.s} size={24} weight={800} anchor="middle" fill={c.col} C={C} />
      </g>
    );
  });
}

/** 색 글자 조각을 이어 한 줄로(가운데 맞춤) */
function Pieces({ C, y, parts, size = 28, o = 1 }) {
  const ws = parts.map(([s]) => mathWidth(s, size, 760));
  const tot = ws.reduce((a, b) => a + b, 0);
  let x = 800 - tot / 2;
  return (
    <g opacity={o} pointerEvents="none">
      {parts.map(([s, col], i) => { const x0 = x; x += ws[i]; return <MText key={i} x={x0} y={y} s={s} size={size} weight={760} fill={col} C={C} />; })}
    </g>
  );
}

/** 막대 아래 한 줄: 고른 문의 몫과 고르지 않은 문 모두의 몫 — 사회자가 연 뒤 어떻게 바뀌는지.
 *  옮겨 가는 동안(flow) 앞 줄이 사라지고 새 줄이 뜬다 */
function ShareLine({ C, vm, P, T, isM, o }) {
  const { n, k, know } = P;
  if (vm.void) return <Pieces C={C} y={LINE_Y} o={o} parts={[["사회자가 자동차 문을 열었어요 — ", C.coral], ["이 판은 세지 않아요", C.ink]]} />;
  const sep = ["   ·   ", C.soft];
  const restN = n - 1 - k;
  const before = [["내 문 ", C.sky], [ftx(red(1, n)), C.ink], sep, ["고르지 않은 문 모두 ", C.gold], [ftx(red(n - 1, n)), C.ink]];
  const after = know
    ? [["내 문 ", C.sky], [`그대로 ${ftx(T.pick)}`, C.ink], sep, [restN > 1 ? `닫힌 다른 문 ${restN}개 ` : "닫힌 다른 문 ", C.gold],
      [restN > 1 ? `모두 ${ftx(T.rest)} → 하나에 ${ftx(T.each)}` : `${ftx(T.rest)} — 열린 문의 몫까지`, C.ink]]
    : [["내 문 ", C.sky], [`${ftx(T.pick)}로`, C.ink], sep, [restN > 1 ? `닫힌 다른 문 ${restN}개 ` : "닫힌 다른 문 ", C.gold],
      [restN > 1 ? `하나에 ${ftx(T.each)} — 모두 똑같아요` : `${ftx(T.each)} — 똑같아요`, C.ink]];
  const sz = isM ? 28 : 27;
  if (k === 0 || vm.phase === "pick" || vm.phase === "open") return <Pieces C={C} y={LINE_Y} parts={before} o={o} size={sz} />;
  if (vm.phase === "flow") {
    return (
      <g>
        <Pieces C={C} y={LINE_Y} parts={before} o={o * (1 - seg(vm.p, 0.05, 0.35))} size={sz} />
        <Pieces C={C} y={LINE_Y} parts={after} o={o * seg(vm.p, 0.6, 0.9)} size={sz} />
      </g>
    );
  }
  return <Pieces C={C} y={LINE_Y} parts={after} o={o} size={sz} />;
}

/** 기록: 그대로 · 바꾸기 이긴 비율(막대) + 이론값(점선) */
function Tally({ C, vm, P, T, isM }) {
  const t1 = vm.tally, t0 = vm.prev || t1, k = vm.tw ?? 1;
  const rows = [
    { name: "그대로", col: C.sky, N: t1.stayN, W: t1.stayW, r0: t0.stayN ? t0.stayW / t0.stayN : 0, th: T.stay },
    { name: "바꾸기", col: C.gold, N: t1.swN, W: t1.swW, r0: t0.swN ? t0.swW / t0.swN : 0, th: T.sw },
  ];
  const span = TAL.x1 - TAL.x0;
  const who = vm.auto ? "컴퓨터 기록" : "우리 반 기록";
  const cnt = vm.auto ? (isM ? `${vm.rounds}/${vm.G}판` : `${vm.rounds}번째 (${vm.G}번 중)`) : `${t1.stayN + t1.swN}${isM ? "판" : "번"}`;
  const voids = (vm.auto ? vm.voidsShow : !P.know) ? ` · 세지 않은 판 ${t1.voids}` : "";
  return (
    <g pointerEvents="none">
      <MText x={TAL.x1 + 22} y={TAL.y[0] - 36} s={`${who} · ${cnt}${voids}`} size={21} weight={700} fill={C.soft} C={C} />
      {rows.map((R, i) => {
        const y = TAL.y[i], r1 = R.N ? R.W / R.N : 0, rate = lerp(R.r0, r1, k);
        const thx = TAL.x0 + val(R.th) * span;
        const txt = R.N ? (isM ? `‹${R.W}›/${R.N} · ${pct(r1)}` : `${R.N}번 중 ‹${R.W}›번`) : isM ? "아직 0판" : "아직 없어요";
        return (
          <g key={R.name}>
            <MText x={TAL.name} y={y + 9} s={R.name} size={26} weight={800} anchor="end" fill={R.col} C={C} />
            <rect x={TAL.x0} y={y - TAL.th / 2} width={span} height={TAL.th} rx={TAL.th / 2} fill={C.ink} fillOpacity={0.1} />
            {rate > 0.002 && <rect x={TAL.x0} y={y - TAL.th / 2} width={Math.max(TAL.th, rate * span)} height={TAL.th} rx={TAL.th / 2} fill={R.col} fillOpacity={0.88} />}
            <line x1={thx} x2={thx} y1={y - 20} y2={y + 20} stroke={C.ink} strokeWidth={3} strokeDasharray="5 4" opacity={0.85} />
            {i === 0 && <MText x={thx} y={y - 24} s={isM ? `이론 ${ftx(R.th)}` : `가능성 ${ftx(R.th)}`} size={19} weight={700} anchor="middle" fill={C.soft} C={C} />}
            {i === 1 && <MText x={thx} y={y + 44} s={isM ? `이론 ${ftx(R.th)}` : `가능성 ${ftx(R.th)}`} size={19} weight={700} anchor="middle" fill={C.soft} C={C} />}
            <MText x={TAL.x1 + 22} y={y + 9} s={txt} size={25} weight={700} fill={C.ink} C={C} />
          </g>
        );
      })}
    </g>
  );
}

/** 저절로 한 바퀴를 마치면: 몇 번씩 이겼는지 + 이론 */
function Summary({ C, vm, P, T, isM }) {
  const { know, k, n } = P;
  const t = vm.tally, o = E.sine(clamp(vm.sumP * 5)) * (1 - E.sine(clamp((vm.sumP - 0.9) * 10)));
  const dW = t.swW - t.stayW;
  const unit = isM ? "판" : "번";
  const lines = [
    [`${vm.G}${unit} 해 보니`, 30, C.soft, 700],
    [`그대로 ‹${t.stayW}›번 · 바꾸기 ‹${t.swW}›번 이겼어요`, 40, C.ink, 800],
    [dW > 0 ? `바꾼 쪽이 ${dW}번 더 이겼어요` : dW < 0 ? `이번엔 그대로 둔 쪽이 ${-dW}번 더 이겼어요` : "두 쪽이 똑같이 이겼어요", 30, C.ink, 650],
    [know && k > 0
      ? (isM ? `이론: 그대로 ${ftx(T.stay)} · 바꾸기 ${ftx(T.sw)}` : `가능성: 그대로 ${ftx(T.stay)} · 바꾸기 ${ftx(T.sw)}`)
      : (isM ? `이론: 둘 다 ${ftx(T.stay)} — 바꿔도 같아요` : `가능성: 둘 다 ${ftx(T.stay)} — 바꿔도 같아요`), 28, C.gold, 760],
  ];
  if (!know) lines.splice(3, 0, [`세지 않은 판 ${t.voids}${unit} — 모르는 사회자가 자동차 문을 열었어요`, 22, C.soft, 600]);
  const wMax = Math.max(...lines.map(([s, sz, , wt]) => mathWidth(s, sz, wt))) + 90;
  const h = lines.reduce((a, [, sz]) => a + sz * 1.55, 0) + 40;
  const y0 = DOOR.y0 + DOOR.h / 2 - h / 2;
  let y = y0 + 26;
  return (
    <g opacity={o} pointerEvents="none">
      <rect x={800 - wMax / 2} y={y0} width={wMax} height={h} rx={26} fill={C.halo} fillOpacity={0.94} stroke={C.gold} strokeWidth={3} />
      {lines.map(([s, sz, col, wt], i) => { y += sz * 1.55; return <MText key={i} x={800} y={y - sz * 0.42} s={s} size={sz} weight={wt} anchor="middle" fill={col} C={C} />; })}
    </g>
  );
}

/* ══════════ 자막(판의 구간마다 한 줄) ══════════ */
function capOf(vm, P, isM) {
  const { n, k, know } = P;
  const T = theory(n, k, know);
  const d1 = (d) => `${d + 1}번 문`;
  if (vm.auto && P.speed === "fast" && vm.phase !== "sum") {
    return isM ? `빠르게 ${vm.G}판 — 이긴 비율(상대도수)이 이론값(점선)으로 다가가요` : `빠르게 ${vm.G}번 — 막대 끝이 점선(가능성)으로 다가가요`;
  }
  switch (vm.phase) {
    case "pick":
      if (vm.auto) return `${vm.r + 1}번째 판 — 컴퓨터가 문을 하나 골라요`;
      return isM ? `문을 하나 눌러 고르세요 — 어느 문이든 자동차일 확률은 ${ftx(red(1, n))}` : `문을 하나 골라 눌러 보세요 — 문 ${n}개 중 하나에 자동차가 있어요`;
    case "open":
      if (know) return isM ? `답을 아는 사회자는 염소 문만 ${k}개 열어요 — 내 문은 열지 않아요` : `자동차가 어디 있는지 아는 사회자가 염소 문을 ${k}개 열어요`;
      return isM ? `답을 모르는 사회자가 아무 문이나 ${k}개 열어요` : `사회자도 몰라요 — 아무 문이나 ${k}개 열어요`;
    case "flow":
      if (know) return isM ? `내 문은 그대로 ${ftx(T.pick)} — 열린 문의 몫은 닫힌 다른 문으로 옮겨 가요` : "열린 문의 몫은 내가 고르지 않은 닫힌 문으로 옮겨 가요";
      return isM ? `모르고 열었는데 염소가 나왔으니 닫힌 문 ${n - k}개가 똑같이 ${ftx(T.each)}` : "사회자도 몰랐으니 닫힌 문은 모두 똑같아져요";
    case "decide":
      if (vm.auto) return isM ? "그대로 둘 때와 바꿀 때 — 두 가지를 함께 따져 봐요" : "그대로 둘 때와 바꿀 때를 함께 봐요";
      if (k === 0) return "사회자가 문을 하나도 열지 않았어요 — 그대로? 바꾸기? 문을 눌러요";
      return "그대로 둘까요, 바꿀까요? — 고른 문이나 닫힌 다른 문을 눌러요";
    case "reveal": case "done": {
      if (vm.auto) {
        const a = vm.pick === vm.car, b = vm.sw === vm.car;
        return `그대로였다면 ${a ? "자동차" : "염소"} · 바꿨다면 ${b ? "자동차" : "염소"}`;
      }
      const stay = vm.choice === vm.pick, win = vm.choice === vm.car;
      if (win) return stay ? "자동차! 그대로 둬서 이겼어요" : "자동차! 바꿔서 이겼어요";
      return stay ? `염소예요 — 자동차는 ${d1(vm.car)}에 있었어요 (바꿨다면…)` : `염소예요 — 자동차는 ${d1(vm.car)}에 있었어요`;
    }
    case "void":
      return isM ? "자동차가 열려 버렸어요 — 모르는 사회자라서 생긴 일, 이 판은 세지 않아요" : "자동차가 나와 버렸어요! 사회자도 몰랐으니까요 — 이 판은 세지 않아요";
    case "sum":
      return isM ? `한 바퀴 ${vm.G}판 끝 — 다음 바퀴를 새로 시작해요` : `${vm.G}번 해 봤어요 — 다음 바퀴를 새로 시작해요`;
    default: return "";
  }
}
/** 자막이 바뀌는 순간을 기억해 앞 자막이 사라지고 새 자막이 뜨게 */
function useCaps(vm, P, e) {
  const R = useRef({ e: null, m: null });
  const out = {};
  for (const md of ["e", "m"]) {
    const s = capOf(vm, P, md === "m");
    let c = R.current[md];
    if (!c || c.s !== s || e < c.at) { c = { s, prev: c && e >= c.at ? c.s : null, at: e }; R.current[md] = c; }
    const t = e - c.at + 10000;
    out[md] = { t, caps: c.prev ? [{ t: 0, s: c.prev }, { t: 10000, s: c.s }] : [{ t: 9440, s: c.s }] };
  }
  return out;
}

/* ══════════ 해 보기 ══════════ */
function MontyTry({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui, viewSeg }) {
  const lab = useLabClock(LS.lab, DEF, fixPrm);
  const P = lab.prm;
  const hand = P.play === "hand";
  const HS = useRef(null);
  const key = `${tallyKey(P)}#${lab.epoch}`;
  if (!HS.current || HS.current.key !== key) {
    HS.current = { key, ...loadHand(P), prev: null, phase: "pick", at: lab.elapsed(), pick: null, opened: [], car: null, void: false, choice: null };
  }
  const nextRound = useCallback((h, at) => {
    Object.assign(h, { r: h.r + 1, phase: "pick", at, pick: null, opened: [], car: null, void: false, choice: null, prev: null });
    saveHand(P, h);
  }, [P]);

  /* 직접: 시간이 다 된 구간은 다음 구간으로 */
  const advance = useCallback((e) => {
    const h = HS.current;
    for (let guard = 0; guard < 6; guard++) {
      const d = handDur(h.phase, P.k);
      if (!Number.isFinite(d) || e - h.at < d) return;
      const at = h.at + d;
      if (h.phase === "open") {
        if (h.void) { h.prev = h.tally; h.tally = { ...h.tally, voids: h.tally.voids + 1 }; saveHand(P, h); }
        Object.assign(h, { phase: h.void ? "void" : "flow", at });
      } else if (h.phase === "flow") Object.assign(h, { phase: "decide", at });
      else if (h.phase === "reveal") Object.assign(h, { phase: "done", at });
      else if (h.phase === "done" || h.phase === "void") nextRound(h, at);
      else return;
    }
  }, [P, nextRound]);

  const onDoor = useCallback((d) => {
    if (!hand || lab.clk.current.held != null || d < 0 || d >= P.n) return;
    const e = lab.elapsed(), h = HS.current;
    if (h.phase === "pick") {
      const L = luck(h.seed, h.r, P.n);
      const opened = hostOpens(L, P.n, P.k, P.know, d);
      Object.assign(h, { pick: d, opened, car: L.car, void: !P.know && opened.includes(L.car), phase: P.k ? "open" : "decide", at: e });
    } else if (h.phase === "decide") {
      if (h.opened.includes(d)) return;
      const stay = d === h.pick, win = d === h.car, t = h.tally;
      h.prev = t;
      h.tally = stay ? { ...t, stayN: t.stayN + 1, stayW: t.stayW + (win ? 1 : 0) } : { ...t, swN: t.swN + 1, swW: t.swW + (win ? 1 : 0) };
      Object.assign(h, { choice: d, phase: "reveal", at: e });
      saveHand(P, h);
    } else if (h.phase === "done") nextRound(h, e);
  }, [hand, lab, P, nextRound]);

  const restart = useCallback(() => {
    if (hand) saveHand(P, { ...HS.current, tally: emptyTally() });
    lab.restart();
  }, [hand, P, lab]);

  const layers = useModeLayers(mode);
  useTicker(() => {
    const e = lab.elapsed();
    if (hand) advance(e);
    return !(lab.clk.current.held != null && layers.length < 2);
  });

  const setN = (n) => lab.setPrm({ n });
  const setK = (k) => lab.setPrm({ k });
  const setSpeed = (s) => lab.setPrm({ speed: s }, P.play === "auto" ? (o, nx, e) => remapAuto(o, nx, e) : null);
  const keys = {
    ...baseKeys({ togglePause: lab.togglePause, restart, toggleFs, onMode, poke }),
    ArrowUp: () => { const i = MLAB.NS.indexOf(P.n); if (i < MLAB.NS.length - 1) setN(MLAB.NS[i + 1]); poke(); },
    ArrowDown: () => { const i = MLAB.NS.indexOf(P.n); if (i > 0) setN(MLAB.NS[i - 1]); poke(); },
    ArrowRight: () => { if (P.k < P.n - 2) setK(P.k + 1); poke(); },
    ArrowLeft: () => { if (P.k > 0) setK(P.k - 1); poke(); },
    s: () => { if (!hand) setSpeed(P.speed === "fast" ? "natural" : "fast"); poke(); },
    Enter: () => { if (hand && HS.current.phase === "done") nextRound(HS.current, lab.elapsed()); },
  };
  for (let d = 0; d < 10; d++) keys[String((d + 1) % 10)] = () => onDoor(d);
  useKeys(keys, inert);

  /* 지금 보여 줄 판 */
  const e = lab.elapsed();
  let vm;
  if (hand) {
    const h = HS.current, dur = handDur(h.phase, P.k), ms = Math.max(0, e - h.at);
    vm = { auto: false, n: P.n, phase: h.phase, ms, p: Number.isFinite(dur) ? clamp(ms / dur) : 0, pick: h.pick, opened: h.opened, car: h.car,
      void: h.void, choice: h.choice, sw: null, r: h.r, tally: h.tally, prev: h.prev,
      tw: h.phase === "reveal" || h.phase === "void" ? E.out(clamp(ms / 700)) : 1 };
  } else vm = autoVm(P, autoAt(P, e));
  const caps = useCaps(vm, P, e);
  const sub = `${hand ? "직접 해 보기" : `저절로 · ${P.speed === "fast" ? "빠르게" : "자연스럽게"}`} · 문 ${P.n}개 · ${P.k}개를 열어요`;
  const prog = hand ? null : vm.prog;

  const settings = (
    <>
      <Setting label="문"><Stepper ui={ui} label="문" value={P.n} options={MLAB.NS} unit="개" onChange={setN} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="여는 문" sep><Stepper ui={ui} label="여는 문" value={P.k} options={KS(P.n)} unit="개" onChange={setK} poke={poke} keyHint={["←", "→"]} /></Setting>
      <Setting label="사회자" sep><Seg label="사회자" value={P.know} options={[[true, "답을 알아요"], [false, "몰라요"]]} onChange={(v) => lab.setPrm({ know: v })} poke={poke} /></Setting>
      <Setting sep><Seg label="진행" value={P.play} options={[["hand", "직접"], ["auto", "저절로"]]} onChange={(v) => lab.setPrm({ play: v })} poke={poke} /></Setting>
      {!hand && <Setting sep><Seg label="빠르기" value={P.speed} options={[["natural", "자연스럽게"], ["fast", "빠르게"]]} onChange={setSpeed} poke={poke} /></Setting>}
    </>
  );
  const title = { e: "바꿀까, 그대로 둘까?", m: "몬티홀 문제" };
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img"
        aria-label={`몬티홀 — 문 ${P.n}개, 사회자가 ${P.k}개를 열어요`}>
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <MontyArt C={C} mode={Ly.mode} P={P} vm={vm} onDoor={onDoor} live={Ly.top && hand} caps={caps} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={restart}
        restartTitle={hand ? "우리 반 기록 지우고 처음부터" : "처음부터"} isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery}
        onExit={onExit} view={viewSeg} settings={settings} prog={prog} />
    </>
  );
}

/** 몬티홀 액자 — 해 보기(먼저) · 풀이 보기 */
export function MontyFrame(props) {
  return <LabShell fkey="monty" label="몬티홀" explain={EXPLAIN.monty} renderTry={({ viewSeg }) => <MontyTry {...props} viewSeg={viewSeg} />} {...props} />;
}

/** 저절로: autoAt 결과 → 그릴 판(vm) */
export function autoVm(P, A) {
  const R = A.R;
  return {
    auto: true, n: P.n, phase: A.phase, ms: A.te - A.ps, p: A.p, pick: R.pick, opened: R.opened, car: R.car, void: R.void, choice: null, sw: R.sw,
    r: A.r, G: A.G, rounds: A.tally.rounds, voidsShow: !P.know, sumP: A.sum ?? 0, tally: A.tally, prev: A.prev,
    tw: A.phase === "reveal" ? E.out(A.p) : A.phase === "void" ? E.out(clamp(A.p * 3)) : 1,
    prog: A.phase === "sum" ? 1 : (A.r + A.te / A.D) / A.G,
  };
}

/** 액자 목록의 작은 그림 — 저절로 넷째 판, 사회자가 문을 연 뒤 막대가 옮겨 간 순간 */
export const MontyThumb = memo(function MontyThumb({ C, mode = "e" }) {
  const P = fixPrm({ n: 3, k: 1, know: true, play: "auto", speed: "natural" });
  const PHS = phases(P.k, P.speed), dec = PHS.list.find(([nm]) => nm === "decide");
  const vm = autoVm(P, autoAt(P, 3 * PHS.dur + dec[1] + 900));
  return <MontyArt C={C} mode={mode} P={P} vm={vm} />;
});
