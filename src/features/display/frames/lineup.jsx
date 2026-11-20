// ashrain.out — 수학 호기심 액자: 일렬로 세우기 — 모든 경우 늘어놓기 (frames/lineup.jsx)
// 인원 · 이웃하는 사람 수 · 양 끝에 서는 사람 수 · 이웃하지 않는 사람 수를 고르면, 조건을 지키는 줄을
// 이름 가나다순 사전식으로 한 줄씩 차곡차곡 늘어놓는다. 한 쪽이 차면 다음 쪽으로. 다 늘어놓으면 새 이름으로 다시.
//   오른쪽 판: 줄 설 사람 · 조건 · 셀 전략(묶기 → 늘어놓기 → 사이사이 → 묶음 안) · 식, 지금 몇 번째인지.
//   묶음(이웃)은 노란 띠, 양 끝은 깃발, 이웃하지 않음은 하늘색 동그라미.
// 계산: ../curio/lineup.js — 모든 줄을 직접 늘어놓아 센 수와 공식이 같은지 tests/display-curio.test.mjs 가 맞춘다.
import { memo } from "react";
import { W, H, MText, SceneTitle, SANS } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { UText, Chip } from "../kit-story.jsx";
import { hashSeed, comma, keepPlace, EXS, fixEx } from "../curio/kit.js";
import { LINE, LINE_DEF, fixLine, lineAt, casesOf, strategyLines } from "../curio/lineup.js";
import { LabChrome, Stepper, Seg, Setting, useLabClock, useTicker, useKeys, useModeLayers, baseKeys } from "./xkit.jsx";
import { Lines, Panel, Small, FitText } from "./curio-kit.jsx";

const LSK = "ash.display.curio.lineup";
const GRID_FULL = { x: 56, y: 136, w: 1100, h: 728 };
const GRID_MINI = { x: 56, y: 136, w: 1496, h: 684 };   // 최소화: 판 없이 너비 전체, 아래 한 줄은 상태 칩
const PANEL = { x: 1176, y: 150, w: 386, h: 720 };

/* ── 사람 모습: 이름에서 정해진다 ── */
const SKIN = ["#f6d7bd", "#eac4a2", "#d9a77f", "#c58c62"];
const HAIR = ["#2b211c", "#3d2b1f", "#5a3b24", "#1d1d24", "#7a4a2a", "#8a5a33"];
const SHIRT = ["#e8664f", "#3f8fd8", "#f2b53b", "#55b26b", "#9a6ad6", "#ef8bb0", "#36b5ad", "#f08a3c"];
export function lookOf(name) {
  const h = hashSeed("look", name);
  return { skin: SKIN[h % 4], hair: HAIR[(h >>> 3) % 6], style: (h >>> 7) % 5, shirt: SHIRT[(h >>> 11) % 8] };
}
export function Kid({ x, y, s, look, C, o = 1 }) {
  if (o <= 0.001) return null;
  const cx = x + s / 2, hy = y + s * 0.34, hr = s * 0.2;
  const { skin, hair, style, shirt } = look;
  return (
    <g opacity={o}>
      <ellipse cx={cx} cy={y + s * 0.98} rx={s * 0.26} ry={s * 0.05} fill="#000" opacity={0.16} />
      <path d={`M${cx - s * 0.27} ${y + s * 0.98}C${cx - s * 0.28} ${y + s * 0.66} ${cx - s * 0.22} ${y + s * 0.58} ${cx} ${y + s * 0.58}C${cx + s * 0.22} ${y + s * 0.58} ${cx + s * 0.28} ${y + s * 0.66} ${cx + s * 0.27} ${y + s * 0.98}Z`}
        fill={shirt} stroke="#2a2018" strokeOpacity={0.55} strokeWidth={1.2} />
      {style === 1 && <path d={`M${cx - hr * 1.05} ${hy}Q${cx - hr * 1.25} ${hy + hr * 1.6} ${cx - hr * 0.5} ${hy + hr * 1.55}L${cx + hr * 0.5} ${hy + hr * 1.55}Q${cx + hr * 1.25} ${hy + hr * 1.6} ${cx + hr * 1.05} ${hy}Z`} fill={hair} />}
      <circle cx={cx} cy={hy} r={hr} fill={skin} stroke="#2a2018" strokeOpacity={0.45} strokeWidth={1.1} />
      {style !== 4 && <path d={`M${cx - hr * 1.02} ${hy + hr * 0.05}A${hr * 1.02} ${hr * 1.05} 0 0 1 ${cx + hr * 1.02} ${hy + hr * 0.05}Q${cx + hr * 0.4} ${hy - hr * 0.42} ${cx - hr * 0.2} ${hy - hr * 0.3}Q${cx - hr * 0.7} ${hy - hr * 0.2} ${cx - hr * 1.02} ${hy + hr * 0.05}Z`} fill={hair} />}
      {style === 4 && <path d={`M${cx - hr * 0.95} ${hy - hr * 0.1}A${hr} ${hr} 0 0 1 ${cx + hr * 0.95} ${hy - hr * 0.1}`} fill="none" stroke={hair} strokeWidth={hr * 0.32} />}
      {style === 2 && <circle cx={cx + hr * 1.08} cy={hy - hr * 0.2} r={hr * 0.38} fill={hair} />}
      {style === 3 && <><rect x={cx - hr * 1.08} y={hy - hr * 0.1} width={hr * 0.36} height={hr * 0.95} rx={hr * 0.15} fill={hair} /><rect x={cx + hr * 0.72} y={hy - hr * 0.1} width={hr * 0.36} height={hr * 0.95} rx={hr * 0.15} fill={hair} /></>}
      <circle cx={cx - hr * 0.36} cy={hy + hr * 0.12} r={hr * 0.11} fill="#2a2018" />
      <circle cx={cx + hr * 0.36} cy={hy + hr * 0.12} r={hr * 0.11} fill="#2a2018" />
      <path d={`M${cx - hr * 0.3} ${hy + hr * 0.45}Q${cx} ${hy + hr * 0.68} ${cx + hr * 0.3} ${hy + hr * 0.45}`} fill="none" stroke="#2a2018" strokeWidth={Math.max(1, hr * 0.1)} strokeLinecap="round" />
    </g>
  );
}

/** 한 쪽의 칸 나누기 */
export function gridOf(n, GRID = GRID_FULL) {
  const minW = GRID === GRID_MINI ? 84 : 58;   // 최소화는 사람을 더 크게
  for (const cols of [4, 3, 2, 1]) {
    const colW = GRID.w / cols;
    const cw = Math.min(100, (colW - 62) / n);
    if (cw >= minW || cols === 1) {
      const rh = cw * 1.06 + 30;
      const rows = Math.max(1, Math.floor(GRID.h / rh));
      return { cols, colW, cw, rh, rows, cap: rows * cols };
    }
  }
  return null;
}

const ROLE_COL = (C) => ({ block: C.gold, end: C.coral, apart: C.sky });

function CaseRow({ x, y, G, perm, who, num, C, k = 1, looks }) {
  const role = who.role;
  // 묶음 띠
  let band = null;
  if (who.block.length >= 2) {
    const ps = perm.map((p, i) => [p, i]).filter(([p]) => role[p] === "block").map(([, i]) => i);
    const a = Math.min(...ps), b = Math.max(...ps);
    band = <rect x={x + 54 + a * G.cw - 4} y={y + 2} width={(b - a + 1) * G.cw + 8} height={G.cw * 1.06 + 22} rx={14} fill={C.gold} opacity={0.2 * k} />;
  }
  return (
    <g>
      {band}
      <text x={x + 40} y={y + G.cw * 0.62} textAnchor="end" fontFamily={SANS} fontWeight={800} fontSize={Math.min(22, G.cw * 0.3)} fill={C.soft} opacity={k}>{num}</text>
      {perm.map((p, i) => {
        const kk = clamp(k * (perm.length + 2) - i);
        const yy = y + (1 - E.out(kk)) * -26;
        const xx = x + 54 + i * G.cw;
        const r = role[p];
        return (
          <g key={i} opacity={kk}>
            <Kid x={xx + G.cw * 0.06} y={yy} s={G.cw * 0.88} look={looks[p]} C={C} />
            {r === "end" && <path d={`M${xx + G.cw * 0.74} ${yy + G.cw * 0.06}v${G.cw * 0.3}M${xx + G.cw * 0.74} ${yy + G.cw * 0.06}l${G.cw * 0.18} ${G.cw * 0.07}l${-G.cw * 0.18} ${G.cw * 0.07}`} stroke={C.coral} strokeWidth={2.4} fill={C.coral} />}
            {r === "apart" && <circle cx={xx + G.cw * 0.5} cy={yy + G.cw * 0.47} r={G.cw * 0.4} fill="none" stroke={C.sky} strokeWidth={2.4} strokeDasharray="5 4" />}
            <text x={xx + G.cw / 2} y={yy + G.cw * 1.04 + 12} textAnchor="middle" fontFamily={SANS} fontWeight={700} fontSize={Math.min(18, G.cw * 0.25)}
              fill={r ? ROLE_COL(C)[r] : C.ink}>{who.names[p].slice(1)}</text>
          </g>
        );
      })}
    </g>
  );
}

/* ══════════ 그리기 ══════════ */
export function LineupArt({ C, mode, P, at, ex = "full" }) {
  const { who, cases, j, t, sum, d } = at;
  const mini = ex === "mini", GRID = mini ? GRID_MINI : GRID_FULL, CX = mini ? 800 : 600;
  const G = gridOf(P.n, GRID);
  const looks = who.names.map(lookOf);
  const page = Math.floor(j / G.cap), first = page * G.cap;
  const pages = Math.ceil(cases.length / G.cap);
  const rows = [];
  const pos = (q) => { const c = Math.floor(q / G.rows), r = q % G.rows; return [GRID.x + c * G.colW, GRID.y + r * G.rh]; };
  for (let q = first; q <= j; q++) {
    const [x, y] = pos(q - first);
    const k = q < j || sum >= 0 ? 1 : seg(t, 0, Math.min(700, d * 0.8));
    rows.push(<CaseRow key={q} x={x} y={y} G={G} perm={cases[q]} who={who} num={q + 1} C={C} k={k} looks={looks} />);
  }
  // 쪽 넘김: 새 쪽 첫 줄일 때 지난 쪽이 옅어지며 사라진다
  let prevPage = null;
  if (j === first && page > 0 && sum < 0) {
    const k = seg(t, 0, Math.min(600, d * 0.7));
    if (k < 1) {
      const pf = (page - 1) * G.cap;
      prevPage = (
        <g opacity={1 - k} transform={`translate(${-60 * k}, 0)`}>
          {Array.from({ length: G.cap }, (_, q) => { const [x, y] = pos(q); return <CaseRow key={q} x={x} y={y} G={G} perm={cases[pf + q]} who={who} num={pf + q + 1} C={C} looks={looks} />; })}
        </g>
      );
    }
  }
  const { lines, total } = strategyLines(P, who, mode);
  return (
    <g>
      {prevPage}
      <g opacity={prevPage ? seg(t, 200, Math.min(700, d * 0.8)) : 1}>{rows}</g>
      {sum >= 0 && (
        <g opacity={seg(sum, 0, 500) * (1 - seg(sum, LINE.SUM - 500, LINE.SUM))}>
          <rect x={CX - 320} y={380} width={640} height={150} rx={24} fill={C.card} stroke={C.gold} strokeWidth={2.4} />
          <UText x={CX} y={446} s={`모두 ${comma(cases.length)}가지를 늘어놓았어요!`} size={34} weight={800} anchor="middle" C={C} />
          <UText x={CX} y={494} s={`식으로 센 ${comma(total)}가지와 같아요 — 다음은 새 이름으로`} size={22} weight={650} anchor="middle" fill={C.soft} C={C} />
        </g>
      )}
      {!mini && <LinePanel C={C} mode={mode} P={P} who={who} lines={lines} n={cases.length} j={j} page={page} pages={pages} />}
      {mini && <LineMini C={C} mode={mode} P={P} who={who} lines={lines} n={cases.length} j={j} page={page} pages={pages} />}
    </g>
  );
}
/** 최소화 — 아래 한 줄: 조건 · 식(금빛) · 지금 몇 번째 */
function LineMini({ C, mode, P, who, lines, n, j, page, pages }) {
  const RC = ROLE_COL(C);
  const cond = [];
  if (who.block.length) cond.push(`${who.block.map((i) => who.names[i].slice(1)).join("·")} 이웃`);
  if (who.ends.length) cond.push(`${who.ends.map((i) => who.names[i].slice(1)).join("·")} ${who.ends.length === 2 ? "양 끝" : "한쪽 끝"}`);
  if (who.apart.length) cond.push(`${who.apart.map((i) => who.names[i].slice(1)).join("·")} 떨어져`);
  const hi = [...lines].reverse().find((L) => L.hi);
  return (
    <g>
      <Chip x={56} y={846} s={`${P.n}명 한 줄로${cond.length ? ` · ${cond.join(" · ")}` : " · 조건 없음"}`} size={20} C={C} anchor="start" color={mode === "m" ? C.teal : C.coral} />
      {hi && <Chip x={800} y={846} s={hi.s} size={24} C={C} color={C.gold} />}
      <Chip x={1552} y={846} s={`${comma(j + 1)} / ${comma(n)}가지 · ${page + 1}/${pages}쪽`} size={20} C={C} anchor="end" />
    </g>
  );
}

function LinePanel({ C, mode, P, who, lines, n, j, page, pages }) {
  const { x, y, w, h } = PANEL, x0 = x + 22, mw = w - 44;
  const RC = ROLE_COL(C);
  const cond = [];
  if (who.block.length) cond.push({ c: RC.block, s: `${who.block.map((i) => who.names[i].slice(1)).join(" · ")} — 이웃(붙어 서기)` });
  if (who.ends.length) cond.push({ c: RC.end, s: `${who.ends.map((i) => who.names[i].slice(1)).join(" · ")} — ${who.ends.length === 2 ? "양 끝" : "어느 한쪽 끝"}` });
  if (who.apart.length) cond.push({ c: RC.apart, s: `${who.apart.map((i) => who.names[i].slice(1)).join(" · ")} — 서로 이웃하지 않기` });
  if (!cond.length) cond.push({ c: C.soft, s: "조건 없음 — 아무렇게나 한 줄로" });
  return (
    <g>
      <Panel x={x} y={y} w={w} h={h} C={C} />
      <UText x={x0} y={y + 38} s={`${P.n}명을 한 줄로 · 가나다 사전식`} size={19} weight={800} fill={mode === "m" ? C.teal : C.coral} C={C} />
      <FitText x={x0} y={y + 74} s={who.names.join(" · ")} size={18} maxW={mw} minSize={12} weight={700} fill={C.ink} C={C} />
      {cond.map((q, i) => (
        <g key={i}>
          <circle cx={x0 + 7} cy={y + 106 + i * 30} r={6} fill={q.c} />
          <UText x={x0 + 22} y={y + 112 + i * 30} s={q.s} size={17} weight={700} fill={C.ink} C={C} />
        </g>
      ))}
      <line x1={x0} x2={x + w - 22} y1={y + 214} y2={y + 214} stroke={C.cardEdge} strokeWidth={1.2} />
      <Lines x={x0} y={y + 252} lines={lines.map((L) => ({ ...L, at: 0 }))} t={1e9} C={C} size={17} lh={40} maxW={mw} hiSize={24} />
      <line x1={x0} x2={x + w - 22} y1={y + h - 128} y2={y + h - 128} stroke={C.cardEdge} strokeWidth={1.2} />
      <UText x={x0} y={y + h - 72} s={`${comma(j + 1)}`} size={46} weight={900} fill={C.gold} C={C} />
      <UText x={x0 + 12 + String(comma(j + 1)).length * 27} y={y + h - 74} s={`/ ${comma(n)}가지`} size={24} weight={700} fill={C.soft} C={C} />
      <Small x={x0} y={y + h - 30} s={`${page + 1}쪽 / ${pages}쪽`} size={17} C={C} />
    </g>
  );
}

/* ══════════ 액자 ══════════ */
const LINE_DEF_EX = { ...LINE_DEF, ex: "full" };
const fixLineEx = (p = {}) => ({ ...fixLine(p), ex: fixEx(p.ex) });
export function LineupFrame({ C, ctl, poke, isFs, toggleFs, onTheme, onGallery, onExit, inert, mode, onMode, ui }) {
  const lab = useLabClock(LSK, LINE_DEF_EX, fixLineEx);
  const P = lab.prm;
  const layers = useModeLayers(mode);
  useTicker(() => !(lab.clk.current.held != null && layers.length < 2));
  const at = lineAt(P, lab.elapsed());
  const newNames = () => lab.setPrm({ seed: (P.seed % 999983) + 1 });
  const keepRate = (o, n, el) => {          // 빠르기를 바꿔도 같은 줄에서 이어지게
    const A = lineAt(o, el), dn = 1000 / n.rate;
    let base = 0;
    for (let c = 0; c < A.cycle; c++) base += casesOf(n, c).cases.length * dn + LINE.SUM;
    return base + (A.sum >= 0 ? A.cases.length * dn + A.sum : A.j * dn + A.t * (o.rate / n.rate));
  };
  const stepIn = (key, list, dd) => { const i = list.indexOf(P[key]); const j = clamp(i + dd, 0, list.length - 1); if (j !== i) lab.setPrm({ [key]: list[j] }); poke(); };
  useKeys({
    ...baseKeys({ togglePause: lab.togglePause, restart: newNames, toggleFs, onMode, poke }),
    ArrowUp: () => stepIn("n", LINE.NS, 1), ArrowDown: () => stepIn("n", LINE.NS, -1),
    d: () => { lab.setPrm({ ex: P.ex === "mini" ? "full" : "mini" }, keepPlace); poke(); },
  }, inert);
  const settings = (
    <>
      <Setting label="인원"><Stepper ui={ui} label="인원" value={P.n} options={LINE.NS} unit="명" onChange={(v) => lab.setPrm({ n: v })} poke={poke} keyHint={["↓", "↑"]} /></Setting>
      <Setting label="이웃" sep><Stepper ui={ui} label="이웃" value={P.k} options={LINE.KS} fmt={(v) => (v ? v : "없음")} unit={P.k ? "명" : ""} onChange={(v) => lab.setPrm({ k: v })} poke={poke} /></Setting>
      <Setting label="양 끝" sep><Stepper ui={ui} label="양 끝" value={P.e} options={LINE.ES} fmt={(v) => (v ? v : "없음")} unit={P.e ? "명" : ""} onChange={(v) => lab.setPrm({ e: v })} poke={poke} /></Setting>
      <Setting label="이웃 안 함" sep><Stepper ui={ui} label="이웃하지 않는 사람" value={P.m} options={LINE.MS} fmt={(v) => (v ? v : "없음")} unit={P.m ? "명" : ""} onChange={(v) => lab.setPrm({ m: v })} poke={poke} /></Setting>
      <Setting label="풀이" sep><Seg label="풀이" value={P.ex} options={EXS} onChange={(v) => lab.setPrm({ ex: v }, keepPlace)} poke={poke} /></Setting>
      <Setting label="빠르기" sep><Stepper ui={ui} label="빠르기" value={P.rate} options={LINE.RATES} fmt={(v) => `${v}`} unit="줄/초" onChange={(v) => lab.setPrm({ rate: v }, keepRate)} poke={poke} /></Setting>
    </>
  );
  const title = { e: "한 줄로 서는 방법 모두 세기", m: "일렬로 세우기 — 모든 경우 늘어놓기" };
  const sub = "조건을 지키는 줄을 이름 가나다순으로 하나도 빠짐없이";
  return (
    <>
      <svg className="dsp-svg" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="xMidYMid meet" role="img" aria-label="조건에 맞게 일렬로 세우는 경우를 모두 늘어놓는 액자">
        {layers.map((Ly) => (
          <g key={Ly.mode} opacity={Ly.o} pointerEvents={Ly.top ? undefined : "none"}>
            <SceneTitle title={title[Ly.mode]} sub={sub} C={C} mode={Ly.mode} />
            <LineupArt C={C} mode={Ly.mode} P={P} at={at} ex={P.ex} />
          </g>
        ))}
      </svg>
      <LabChrome ui={ui} ctl={ctl} poke={poke} mode={mode} onMode={onMode} paused={lab.paused} onPause={lab.togglePause} onRestart={newNames} restartTitle="새 이름"
        isFs={isFs} toggleFs={toggleFs} onTheme={onTheme} onGallery={onGallery} onExit={onExit} settings={settings}
        prog={(at.sum >= 0 ? at.cases.length : at.j + at.t / at.d) / Math.max(1, at.cases.length)} />
    </>
  );
}

export const LineupThumb = memo(function LineupThumb({ C, mode = "m" }) {
  const P = fixLine({ n: 5, k: 2, e: 0, m: 0, rate: 1, seed: 2 });
  return <LineupArt C={C} mode={mode} P={P} at={lineAt(P, 9400)} />;
});
