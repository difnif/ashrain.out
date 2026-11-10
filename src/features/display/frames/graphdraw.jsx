// ashrain.out — 교실 모니터 「액자」: 일차함수 그래프 그리기 해설 (frames/graphdraw.jsx)
// 학원 프린트 「조건을 보고 일차함수의 그래프 그리기」 기본 96제 · 심화 64제를 문항마다 한 장면으로 끝없이 돌린다.
//   왼쪽: 발문과 풀이 순서 ①②③④ — 프린트와 같은 네모 칸. 지금 줄에 노란 형광펜, 칸에 답이 써진다.
//   오른쪽: −5~5 모눈 좌표평면 — 점이 찍히고(축에서 점선 · 좌표), 빨간 화살표가 가로로 한 칸씩 세며(1, 2, 3 …) 가고
//          세로로 세며 올라가거나 내려가 다음 점을 찍고, 두 점 사이에서 직선이 양쪽으로 뻗는다. 끝나면 정답 직선의 식.
// 재생기는 장면 묶음과 같은 StoryPlayer(player.jsx — 이전 · 멈춤 · 다음 · 이 문항 반복 · 밝기 · 전체 화면, ←/→ · 스페이스 · R · F).
// 이 액자만의 것: 「기본 96 | 심화 64」 · 「1× | 1.5×」(기본은 느리게 — 해설 규격) · 번호 목록(L). 고른 것은 기기에 기억한다.
// 계산·박자표: ../graphdraw.js · 문항: ../graphdraw-items.js
import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { W, H, MText, Arrow, Path, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { GD_SETS, GD_SPEEDS, GD_KIND, gdPlan, stepAt, stepAtoms, toM, linStr, qv, qstr, clipLine } from "../graphdraw.js";
import { StoryPlayer } from "./player.jsx";
import { Seg, useKeys, lsRead, lsWrite } from "./xkit.jsx";

/* ══════════ 무대 배치 (1600×900) ══════════ */
const G = { cx: 1192, cy: 498, u: 61, L: 5 };          // 좌표평면: 가운데 · 한 칸 · −5~5
const X = (v) => G.cx + G.u * v, Y = (v) => G.cy - G.u * v;
const LEFT = 60, RIGHT = 830, TOP = 168, BOTTOM = 862;  // 글자 판
const NUMS = "①②③④";

/* ══════════ 글자 판 배치(문항마다 한 번 — 글자 크기를 맞춰 넣는다) ══════════ */
function boxW(a, size) {
  const min = a.k === "dir" ? size * 2.7 : a.k === "eq" ? size * 4.4 : size * 1.45;
  return Math.max(min, mathWidth(toM(a.v), size, 700) + size * 0.7);
}
function flow(atoms, size, x0, maxW) {
  // 붙어 있어야 하는 조각끼리 한 덩이로 → 덩이 단위로 줄을 바꾼다
  const lumps = [];
  for (const a of atoms) {
    const w = a.t === "box" ? boxW(a, size) + size * 0.12 : mathWidth(toM(a.s), size, 560);
    const piece = { ...a, w };
    if (a.glue && lumps.length) lumps[lumps.length - 1].push(piece); else lumps.push([piece]);
  }
  const lines = [[]];
  let x = 0;
  for (const L of lumps) {
    const lw = L.reduce((s, p) => s + p.w, 0);
    if (x > 0 && x + lw > maxW) {
      // 줄 끝의 띄어쓰기는 버린다
      lines.push([]); x = 0;
    }
    for (const p of L) { lines[lines.length - 1].push({ ...p, x: x0 + x }); x += p.w; }
  }
  return lines;
}
function wrapText(s, size, maxW) {
  const words = s.split(/(?<= )/), lines = [""];
  for (const w of words) {
    const cur = lines[lines.length - 1];
    if (cur && mathWidth(toM(cur + w), size, 560) > maxW) lines.push(w); else lines[lines.length - 1] = cur + w;
  }
  return lines.map((l) => l.trimEnd());
}
const LAYOUT = new WeakMap();
export const GD_BOX = { LEFT, RIGHT, TOP, BOTTOM };
export function layoutOf(it) {
  if (LAYOUT.has(it)) return LAYOUT.get(it);
  let out = null;
  for (const [qs, ss] of [[38, 34], [35, 31], [32, 29], [30, 27]]) {
    const qLines = wrapText(`${it.no}. ${it.q}`, qs, RIGHT - LEFT);
    let y = TOP + qs;
    const qY = qLines.map((_, i) => y + i * qs * 1.5);
    y = qY[qY.length - 1] + qs * 0.6 + ss * 1.6;
    const ind = ss * 1.7, lh = ss * 1.95;
    const steps = it.steps.map((text) => {
      const lines = flow(stepAtoms(text), ss, LEFT + ind, RIGHT - LEFT - ind);
      const y0 = y;
      y += lines.length * lh + ss * 0.5;
      return { lines, y0, lh };
    });
    const ansY = y + ss * 0.9;
    out = { qs, ss, qLines, qY, steps, ansY };
    if (ansY + ss * 0.6 <= BOTTOM) break;
  }
  LAYOUT.set(it, out);
  return out;
}

/* ══════════ 좌표평면 ══════════ */
function Plane({ C }) {
  const ks = [];
  for (let k = -G.L; k <= G.L; k++) ks.push(k);
  const ext = G.L + 0.62;
  return (
    <g>
      {ks.map((k) => (
        <g key={k}>
          <line x1={X(k)} y1={Y(-G.L)} x2={X(k)} y2={Y(G.L)} stroke={C.soft} strokeOpacity={0.3} strokeWidth={1.4} />
          <line x1={X(-G.L)} y1={Y(k)} x2={X(G.L)} y2={Y(k)} stroke={C.soft} strokeOpacity={0.3} strokeWidth={1.4} />
        </g>
      ))}
      <Arrow p={[X(-ext), G.cy]} q={[X(ext), G.cy]} stroke={C.ink} sw={3} h={18} />
      <Arrow p={[G.cx, Y(-ext)]} q={[G.cx, Y(ext)]} stroke={C.ink} sw={3} h={18} />
      <text x={X(ext) - 4} y={G.cy + 38} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>x</text>
      <text x={G.cx + 16} y={Y(ext) + 18} fontFamily={SERIF} fontStyle="italic" fontSize={34} fill={C.ink}>y</text>
      <text x={G.cx - 12} y={G.cy + 28} fontFamily={SERIF} fontStyle="italic" fontSize={24} fill={C.soft} textAnchor="end">O</text>
      {ks.filter((k) => k).map((k) => (
        <g key={"n" + k} fontFamily={SANS} fontSize={22} fontWeight={500} fill={C.soft}>
          <text x={X(k)} y={G.cy + 29} textAnchor="middle">{k < 0 ? "−" + -k : k}</text>
          <text x={G.cx - 10} y={Y(k) + 8} textAnchor="end">{k < 0 ? "−" + -k : k}</text>
        </g>
      ))}
    </g>
  );
}

function labelAt(P, m) {
  const px = X(qv(P[0])), py = Y(qv(P[1]));
  // 직선과 겹치지 않게: 기울기가 양수면 점의 왼쪽 위, 음수면 오른쪽 위(직선 위쪽 빈자리). 판 끝이면 반대쪽으로.
  let left = qv(m) > 0;
  if (left && px - 18 < 960) left = false;
  if (!left && px + 18 > 1430) left = true;
  const y = clamp(py - 18, 150, 850);
  const dx = qv(P[0]) === 0 ? 46 : 18;        // y축 위의 점: 축 눈금 수를 비켜서
  return { x: px + (left ? -dx : dx), y, anchor: left ? "end" : "start" };
}

function Dot({ P, m, C, k }) {
  if (k <= 0) return null;
  const px = X(qv(P[0])), py = Y(qv(P[1]));
  const grow = seg(k, 0, 0.38, E.back), lab = seg(k, 0.38, 0.72, E.sine), ring = seg(k, 0, 0.5, E.out);
  const onAxis = qv(P[0]) === 0 || qv(P[1]) === 0;
  const L = labelAt(P, m);
  return (
    <g>
      {!onAxis && <path d={`M${px},${G.cy} V${py} M${G.cx},${py} H${px}`} fill="none" stroke={C.blue} strokeWidth={2}
        strokeDasharray="8 7" opacity={0.6 * lab} />}
      {ring < 1 && <circle cx={px} cy={py} r={10 + 30 * ring} fill="none" stroke={C.blue} strokeWidth={3} opacity={1 - ring} />}
      <circle cx={px} cy={py} r={10 * grow} fill={C.blue} />
      <MText x={L.x} y={L.y} s={`(${qstr(P[0])}, ${qstr(P[1])})`} size={32} weight={700} anchor={L.anchor} fill={C.blue} halo={C.halo} opacity={lab} C={C} />
    </g>
  );
}

function Move({ a, t, C }) {
  const ph = seg(t, a.h[0], a.h[1], E.lin), pv = seg(t, a.v[0], a.v[1], E.lin);
  if (ph <= 0) return null;
  const x0 = X(qv(a.P[0])), y0 = Y(qv(a.P[1])), x1 = X(qv(a.Q[0])), y1 = Y(qv(a.Q[1]));
  const nH = Math.round(Math.abs(a.run)), nV = Math.round(Math.abs(a.rise));
  const sx = Math.sign(a.run), sy = Math.sign(a.rise);
  const hx = x0 + (x1 - x0) * ph, vy = y0 + (y1 - y0) * pv;
  const cntY = y0 + (a.rise > 0 ? 44 : -18), cntX = x1 + (a.run > 0 ? 30 : -30);
  const cnt = [];
  for (let k = 1; k <= nH; k++) if (ph * nH >= k - 0.55) cnt.push(<text key={"h" + k} x={X(qv(a.P[0]) + sx * (k - 0.5))} y={cntY}>{k}</text>);
  for (let k = 1; k <= nV; k++) if (pv * nV >= k - 0.55) cnt.push(<text key={"v" + k} x={cntX} y={Y(qv(a.P[1]) + sy * (k - 0.5)) + 11}>{k}</text>);
  return (
    <g>
      {pv <= 0
        ? <Arrow p={[x0, y0]} q={[hx, y0]} stroke={C.red} sw={5} h={ph < 1 ? 16 : 0.01} />
        : <Path pts={[[x0, y0], [x1, y0]]} stroke={C.red} sw={5} />}
      {pv > 0 && <Arrow p={[x1, y0]} q={[x1, vy]} stroke={C.red} sw={5} h={18} />}
      <g fontFamily={SANS} fontSize={34} fontWeight={800} fill={C.red} textAnchor="middle"
        style={{ paintOrder: "stroke", stroke: C.halo, strokeWidth: 7, strokeLinejoin: "round" }}>{cnt}</g>
    </g>
  );
}

function Line({ plan, k, C }) {
  if (k <= 0) return null;
  const mv = qv(plan.m), bv = qv(plan.b);
  const [A, B] = clipLine(mv, bv, G.L + 0.45);
  const M0 = [(qv(plan.P1[0]) + qv(plan.P2[0])) / 2, (qv(plan.P1[1]) + qv(plan.P2[1])) / 2];
  const p = E.io(k);
  const a = [M0[0] + (A[0] - M0[0]) * p, M0[1] + (A[1] - M0[1]) * p], b = [M0[0] + (B[0] - M0[0]) * p, M0[1] + (B[1] - M0[1]) * p];
  return <line x1={X(a[0])} y1={Y(a[1])} x2={X(b[0])} y2={Y(b[1])} stroke={C.blue} strokeWidth={6} strokeLinecap="round" />;
}

/* ══════════ 글자 판 ══════════ */
function StepLine({ st, Ls, i, t, cur, C, ss }) {
  const hl = i === cur ? seg(t, st.a, st.a + 420, E.sine) : 0;
  const fill = seg(t, st.f[0], st.f[1], E.sine);
  const shown = t >= st.a ? 1 : 0.42;
  const bh = ss * 1.32;
  const top = Ls.y0 - ss * 1.12, h = Ls.lines.length * Ls.lh - ss * 0.42;
  return (
    <g>
      {hl > 0 && (
        <g opacity={hl}>
          <rect x={LEFT - 14} y={top} width={RIGHT - LEFT + 28} height={h} rx={12} fill={C.yellow} opacity={C.name === "dark" ? 0.13 : 0.24} />
          <rect x={LEFT - 30} y={top + 6} width={6} height={h - 12} rx={3} fill={C.bar} />
        </g>
      )}
      <g opacity={shown}>
        <text x={LEFT} y={Ls.y0} fontFamily={SANS} fontSize={ss * 1.05} fontWeight={800} fill={C.ink}>{NUMS[i]}</text>
        {Ls.lines.map((line, j) => {
          const y = Ls.y0 + j * Ls.lh;
          return (
            <g key={j}>
              {line.map((p, k) => p.t === "txt"
                ? <MText key={k} x={p.x} y={y} s={toM(p.s)} size={ss} weight={560} fill={C.ink} C={C} />
                : (
                  <g key={k}>
                    <rect x={p.x + ss * 0.06} y={y - ss * 0.98} width={p.w - ss * 0.12} height={bh} rx={5} fill="none" stroke={C.ink} strokeOpacity={0.75} strokeWidth={2.4} />
                    <MText x={p.x + p.w / 2} y={y} s={toM(p.v)} size={ss} weight={700} anchor="middle" fill={C.blue} opacity={fill} C={C} />
                  </g>
                ))}
            </g>
          );
        })}
      </g>
    </g>
  );
}

/** 한 문항 한 순간(t — 1배속 ms) */
export function GraphArt({ it, t, C }) {
  const plan = gdPlan(it), Lo = layoutOf(it);
  const cur = stepAt(plan, t);
  const qo = seg(t, 0, 600, E.sine);
  const acts = plan.steps.flatMap((s) => s.acts);
  const lineAct = acts.find((a) => a.type === "line");
  const ans = seg(t, plan.ans, plan.ans + 700, E.sine);
  return (
    <g>
      <Plane C={C} />
      {lineAct && <Line plan={plan} k={seg(t, lineAct.a, lineAct.b, E.lin)} C={C} />}
      {acts.filter((a) => a.type === "move").map((a, i) => <Move key={i} a={a} t={t} C={C} />)}
      {acts.filter((a) => a.type === "dot").map((a, i) => (
        <Dot key={i} P={a.P} m={plan.m} C={C} k={seg(t, a.a, a.b, E.lin)} />
      ))}
      <g opacity={qo}>
        {Lo.qLines.map((s, i) => (
          <MText key={i} x={LEFT} y={Lo.qY[i]} s={toM(s)} size={Lo.qs} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />
        ))}
      </g>
      {plan.steps.map((st, i) => <StepLine key={i} st={st} Ls={Lo.steps[i]} i={i} t={t} cur={cur} C={C} ss={Lo.ss} />)}
      {ans > 0 && (
        <g opacity={ans}>
          <text x={LEFT} y={Lo.ansY} fontFamily={SANS} fontSize={Lo.ss * 0.82} fontWeight={700} fill={C.soft}>정답 직선</text>
          <MText x={LEFT + Lo.ss * 4.4} y={Lo.ansY} s={toM(linStr(plan.m, plan.b))} size={Lo.ss * 1.12} weight={700} fill={C.blue} C={C} />
        </g>
      )}
    </g>
  );
}

/* ══════════ 장면 목록 (StoryPlayer 형식) ══════════ */
const SCENES = new Map();
export function graphScenes(setKey, sp = 1) {
  const k = `${setKey}|${sp}`;
  if (SCENES.has(k)) return SCENES.get(k);
  const S = GD_SETS[setKey];
  const list = S.items.map((it) => {
    const plan = gdPlan(it);
    const title = "일차함수 그래프 그리기";
    const sub = `${S.name} ${it.no}번 · ${GD_KIND[it.kind]}`;
    return {
      key: `gd-${setKey}-${it.no}`, no: it.no, kind: it.kind, dur: Math.round(plan.dur / sp),
      title: { e: title, m: title }, sub: { e: sub, m: sub },
      render: (mode, t, C) => <GraphArt it={it} t={t * sp} C={C} />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 ══════════ */
const LSK = "ash.display.graph";
const fixSet = (v) => (GD_SETS[v] ? v : "basic");
const fixSp = (v) => (GD_SPEEDS.includes(v) ? v : 1);

export function GraphFrame(props) {
  const { ui, poke, inert } = props;
  const { Btn, Ic } = ui;
  const [cfg, setCfg] = useState(() => { const o = lsRead(LSK) || {}; return { set: fixSet(o.set), sp: fixSp(o.sp) }; });
  useEffect(() => { lsWrite(LSK, cfg); }, [cfg]);
  const [list, setList] = useState(false);
  const [cur, setCur] = useState(0);
  const api = useRef(null);
  const scenes = useMemo(() => graphScenes(cfg.set, cfg.sp), [cfg]);
  const pickSet = useCallback((v) => setCfg((c) => ({ ...c, set: fixSet(v) })), []);
  const pickSp = useCallback((v) => setCfg((c) => ({ ...c, sp: fixSp(v) })), []);
  useKeys({
    l: () => { setList((v) => !v); poke(); },
    b: () => { pickSet(cfg.set === "basic" ? "hard" : "basic"); poke(); },
    s: () => { pickSp(cfg.sp === 1 ? 1.5 : 1); poke(); },
    Escape: () => setList(false),
  }, inert);
  const extra = (
    <>
      <span className="dsp-sep" />
      <Seg label="문항" value={cfg.set} options={[["basic", "기본 96"], ["hard", "심화 64"]]} onChange={pickSet} poke={poke} />
      <Seg label="빠르기" value={cfg.sp} options={[[1, "1×"], [1.5, "1.5×"]]} onChange={pickSp} poke={poke} />
      <Btn title="번호 목록 (L)" on={list} onClick={() => { setList((v) => !v); poke(); }}>
        <Ic d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01" />
      </Btn>
      <span className="dsp-sep" />
    </>
  );
  const pick = (i) => { api.current?.goTo(i); setList(false); poke(); };
  return (
    <>
      <StoryPlayer key={`${cfg.set}|${cfg.sp}`} list={scenes} lsKey={`${LSK}.${cfg.set}`} label={`일차함수 그래프 그리기 해설 · ${GD_SETS[cfg.set].name}`}
        {...props} inert={inert || list} noMode extra={extra} apiRef={api} onIdx={setCur} />
      {list && <NumList scenes={scenes} setName={GD_SETS[cfg.set].name} cur={cur} onPick={pick} onClose={() => setList(false)} />}
    </>
  );
}

const fmtMin = (ms) => `${Math.round(ms / 60000)}분`;
/** 번호 목록 — 고르면 그 문항부터 이어서 돈다 */
function NumList({ scenes, setName, cur, onPick, onClose }) {
  const lap = scenes.reduce((s, x) => s + x.dur, 0);
  return (
    <div className="dsp-list" onPointerDown={(e) => e.stopPropagation()} onClick={onClose}>
      <div className="dsp-list-in" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="번호 목록">
        <style>{".gd-grid { grid-template-columns: repeat(6, 1fr); } .gd-grid .dsp-card .e { font-size: 1.05cqw; }"}</style>
        <div className="dsp-list-h">
          <b>일차함수 그래프 그리기 · {setName} {scenes.length}제</b>
          <button type="button" onClick={onClose} aria-label="닫기">✕</button>
        </div>
        <p className="dsp-gal-sub">고르면 그 문항부터 이어서 돌아요 · 한 바퀴 약 {fmtMin(lap)} · 지금 {scenes[cur]?.no}번</p>
        <div className="dsp-grid gd-grid">
          {scenes.map((s, i) => (
            <button key={s.key} type="button" className={"dsp-card" + (i === cur ? " on" : "")} onClick={() => onPick(i)}>
              <span className="n">{s.no}</span>
              <span className="e">{GD_KIND[s.kind]}</span>
              <span className="m">{Math.round(s.dur / 1000)}초</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

/** 액자 목록의 작은 그림 — 심화 41번(일차방정식과 평행) 다 그린 순간 */
export const GraphThumb = memo(function GraphThumb({ C }) {
  const it = GD_SETS.hard.items[40];
  return <GraphArt it={it} t={gdPlan(it).ans + 800} C={C} />;
});
