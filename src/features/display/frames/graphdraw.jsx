// ashrain.out — 교실 모니터 「액자」: 일차함수 그래프 그리기 해설 (frames/graphdraw.jsx)
// 학원 프린트 「조건을 보고 일차함수의 그래프 그리기」 기본 96제 · 심화 64제를 문항마다 한 장면으로 끝없이 돌린다.
//   왼쪽: 발문과 풀이 순서 ①②③④ — 프린트와 같은 네모 칸. 지금 줄에 노란 형광펜, 칸에 답이 써진다.
//   오른쪽: −5~5 모눈 좌표평면 — 점이 찍히고(축에서 점선 · 좌표), 빨간 화살표가 가로로 한 칸씩 세며(1, 2, 3 …) 가고
//          세로로 세며 올라가거나 내려가 다음 점을 찍고, 두 점 사이에서 직선이 양쪽으로 뻗는다. 끝나면 정답 직선의 식.
// 조작은 해설 액자 공통 틀(frames/lesson.jsx) — 「기본 96 | 심화 64」 · 빠르기 0.75× ~ 2× · 번호 목록 · 두 막대 · 단일 | 듀얼.
//   듀얼 반쪽 판은 위에 문제와 지금 순서 한 줄, 아래에 좌표평면(paneLayoutOf — 판이 좁아 순서를 다 늘어놓지 않는다).
// 계산·박자표: ../graphdraw.js · 문항: ../graphdraw-items.js
import { memo } from "react";
import { W, H, MText, Arrow, Path, mathWidth, SANS, SERIF } from "../draw.jsx";
import { seg, E, clamp } from "../core.js";
import { GD_SETS, GD_KIND, gdPlan, stepAt, stepAtoms, toM, linStr, qv, qstr, clipLine } from "../graphdraw.js";
import { stepMarks } from "./scrub.jsx";
import { LessonFrame } from "./lesson.jsx";
import { sigTop } from "./sigdocs.jsx";

/* ══════════ 무대 배치 (1600×900) ══════════ */
// 좌표평면(가운데 · 한 칸 · −5~5)과 글자 판 — 단일 모드는 오른쪽에 큰 좌표평면, 듀얼 모드의 반쪽 판(800 × 900)은
//   위에 문제와 지금 순서 한 줄(①②③④ 가운데 지금 것), 아래에 좌표평면(planeIn — 남은 칸에 맞춰 한 칸 크기를 정한다).
const geoOf = (cx, cy, u) => ({ cx, cy, u, L: 5, X: (v) => cx + u * v, Y: (v) => cy - u * v,
  x0: cx - u * 5.62, x1: cx + u * 5.62, y0: cy - u * 5.62, y1: cy + u * 5.62 });
const G1 = geoOf(1192, 498, 61);
export const GD_TEXT = { left: 60, right: 830, top: 168, bottom: 862 };   // 단일 모드 글자 판
const NUMS = "①②③④";
/** 글자 크기 두 벌(../board.js 와 같은 생각 — 기본으로 넘치면 촘촘) · 문제 qs · 순서 ss */
const GD_TYPE = [[40, 36], [36, 33], [34, 31]];

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
export const GD_BOX = { LEFT: GD_TEXT.left, RIGHT: GD_TEXT.right, TOP: GD_TEXT.top, BOTTOM: GD_TEXT.bottom };
/** 단일 모드 글자 판 — 문제 → 순서 ①②③④(네모 칸) → 정답 직선 */
export function layoutOf(it) {
  if (LAYOUT.has(it)) return LAYOUT.get(it);
  const { left: LEFT, right: RIGHT, top: TOP, bottom: BOTTOM } = GD_TEXT;
  let out = null;
  for (const [qs, ss] of GD_TYPE) {
    const qLines = wrapText(`${it.no}. ${it.q}`, qs, RIGHT - LEFT);
    let y = TOP + qs;
    const qY = qLines.map((_, i) => y + i * qs * 1.45);
    y = qY[qY.length - 1] + qs * 0.6 + ss * 1.6;
    const ind = ss * 1.7, lh = ss * 1.9;
    const steps = it.steps.map((text) => {
      const lines = flow(stepAtoms(text), ss, LEFT + ind, RIGHT - LEFT - ind);
      const y0 = y;
      y += lines.length * lh + ss * 0.5;
      return { lines, y0, lh };
    });
    const ansY = y + ss * 0.9;
    out = { qs, ss, qLines, qY, steps, ansY, box: GD_TEXT };
    if (ansY + ss * 0.6 <= BOTTOM) break;
  }
  LAYOUT.set(it, out);
  return out;
}
const PLAY = new WeakMap();
export const GD_PANE = { left: 46, right: 760, top: 152, bottom: 868 };
/**
 * 듀얼 반쪽 판 배치 — 문제(판 너비) · 순서 한 줄 칸(가장 긴 순서에 맞춘 높이) · 좌표평면(남은 칸 · 한 칸 ≥ 30).
 * 순서는 지금 것 하나만 보인다(바뀔 때 겹쳐 넘어감) — 판이 좁아 넷을 다 늘어놓으면 좌표평면이 너무 작아진다.
 */
export function paneLayoutOf(it) {
  if (PLAY.has(it)) return PLAY.get(it);
  const B = GD_PANE, W0 = B.right - B.left;
  let out = null;
  for (const [qs, ss] of GD_TYPE) {
    const qLines = wrapText(`${it.no}. ${it.q}`, qs, W0);
    const qY = qLines.map((_, i) => B.top + qs + i * qs * 1.45);
    const capTop = qY[qY.length - 1] + qs * 0.75;
    const ind = ss * 1.7, lh = ss * 1.9;
    const steps = it.steps.map((text) => ({ lines: flow(stepAtoms(text), ss, B.left + ind, W0 - ind), y0: capTop + ss * 1.05, lh }));
    const capH = Math.max(1, ...steps.map((st) => st.lines.length)) * lh + ss * 0.35;
    const pTop = capTop + capH + 10, avail = Math.min(B.bottom - pTop, W0);
    const u = Math.min(52, avail / 11.6);
    out = { qs, ss, qLines, qY, steps, capTop, capH, ansY: capTop + ss * 1.05, box: B,
      geo: geoOf((B.left + B.right) / 2 + 8, pTop + (B.bottom - pTop) / 2, u) };
    if (u >= 32) break;
  }
  PLAY.set(it, out);
  return out;
}

/* ══════════ 좌표평면 ══════════ */
function Plane({ C, g }) {
  const G = g, { X, Y } = g;
  const ks = [];
  for (let k = -G.L; k <= G.L; k++) ks.push(k);
  const ext = G.L + 0.62;
  const nz = Math.round(Math.max(21, Math.min(26, G.u * 0.43)));
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
      <text x={G.cx - 12} y={G.cy + nz + 6} fontFamily={SERIF} fontStyle="italic" fontSize={nz + 2} fill={C.soft} textAnchor="end">O</text>
      {ks.filter((k) => k).map((k) => (
        <g key={"n" + k} fontFamily={SANS} fontSize={nz} fontWeight={600} fill={C.soft}>
          <text x={X(k)} y={G.cy + nz + 7} textAnchor="middle">{k < 0 ? "−" + -k : k}</text>
          <text x={G.cx - 10} y={Y(k) + nz * 0.36} textAnchor="end">{k < 0 ? "−" + -k : k}</text>
        </g>
      ))}
    </g>
  );
}

function labelAt(P, m, g) {
  const px = g.X(qv(P[0])), py = g.Y(qv(P[1]));
  // 직선과 겹치지 않게: 기울기가 양수면 점의 왼쪽 위, 음수면 오른쪽 위(직선 위쪽 빈자리). 판 끝이면 반대쪽으로.
  let left = qv(m) > 0;
  if (left && px - 18 < g.x0 + g.u * 1.8) left = false;
  if (!left && px + 18 > g.x1 - g.u * 1.7) left = true;
  const y = clamp(py - 18, g.y0 + 10, g.y1 - 8);
  const dx = qv(P[0]) === 0 ? 46 : 18;        // y축 위의 점: 축 눈금 수를 비켜서
  return { x: px + (left ? -dx : dx), y, anchor: left ? "end" : "start" };
}

function Dot({ P, m, C, k, g }) {
  if (k <= 0) return null;
  const G = g, X = g.X, Y = g.Y;
  const px = X(qv(P[0])), py = Y(qv(P[1]));
  const grow = seg(k, 0, 0.38, E.back), lab = seg(k, 0.38, 0.72, E.sine), ring = seg(k, 0, 0.5, E.out);
  const onAxis = qv(P[0]) === 0 || qv(P[1]) === 0;
  const L = labelAt(P, m, g);
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

function Move({ a, t, C, g }) {
  const X = g.X, Y = g.Y;
  const ph = seg(t, a.h[0], a.h[1], E.lin), pv = seg(t, a.v[0], a.v[1], E.lin);
  if (ph <= 0) return null;
  const x0 = X(qv(a.P[0])), y0 = Y(qv(a.P[1])), x1 = X(qv(a.Q[0])), y1 = Y(qv(a.Q[1]));
  const nH = Math.round(Math.abs(a.run)), nV = Math.round(Math.abs(a.rise));
  const sx = Math.sign(a.run), sy = Math.sign(a.rise);
  const hx = x0 + (x1 - x0) * ph, vy = y0 + (y1 - y0) * pv;
  const fz = Math.max(26, Math.min(34, g.u * 0.62));
  const cntY = y0 + (a.rise > 0 ? fz * 1.3 : -fz * 0.53), cntX = x1 + (a.run > 0 ? fz * 0.9 : -fz * 0.9);
  const cnt = [];
  for (let k = 1; k <= nH; k++) if (ph * nH >= k - 0.55) cnt.push(<text key={"h" + k} x={X(qv(a.P[0]) + sx * (k - 0.5))} y={cntY}>{k}</text>);
  for (let k = 1; k <= nV; k++) if (pv * nV >= k - 0.55) cnt.push(<text key={"v" + k} x={cntX} y={Y(qv(a.P[1]) + sy * (k - 0.5)) + fz * 0.33}>{k}</text>);
  return (
    <g>
      {pv <= 0
        ? <Arrow p={[x0, y0]} q={[hx, y0]} stroke={C.red} sw={5} h={ph < 1 ? 16 : 0.01} />
        : <Path pts={[[x0, y0], [x1, y0]]} stroke={C.red} sw={5} />}
      {pv > 0 && <Arrow p={[x1, y0]} q={[x1, vy]} stroke={C.red} sw={5} h={18} />}
      <g fontFamily={SANS} fontSize={fz} fontWeight={800} fill={C.red} textAnchor="middle"
        style={{ paintOrder: "stroke", stroke: C.halo, strokeWidth: 7, strokeLinejoin: "round" }}>{cnt}</g>
    </g>
  );
}

function Line({ plan, k, C, g }) {
  if (k <= 0) return null;
  const G = g, X = g.X, Y = g.Y;
  const mv = qv(plan.m), bv = qv(plan.b);
  const [A, B] = clipLine(mv, bv, G.L + 0.45);
  const M0 = [(qv(plan.P1[0]) + qv(plan.P2[0])) / 2, (qv(plan.P1[1]) + qv(plan.P2[1])) / 2];
  const p = E.io(k);
  const a = [M0[0] + (A[0] - M0[0]) * p, M0[1] + (A[1] - M0[1]) * p], b = [M0[0] + (B[0] - M0[0]) * p, M0[1] + (B[1] - M0[1]) * p];
  return <line x1={X(a[0])} y1={Y(a[1])} x2={X(b[0])} y2={Y(b[1])} stroke={C.blue} strokeWidth={6} strokeLinecap="round" />;
}

/* ══════════ 글자 판 ══════════ */
function StepLine({ st, Ls, i, t, cur, C, ss, box, o = 1 }) {
  const LEFT = box.left, RIGHT = box.right;
  const hl = i === cur ? seg(t, st.a, st.a + 420, E.sine) : 0;
  const fill = seg(t, st.f[0], st.f[1], E.sine);
  const shown = (t >= st.a ? 1 : 0.42) * o;
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

/** 좌표평면 위의 것들 — 직선 · 칸 세기 화살표 · 점 */
function PlaneArt({ plan, t, C, g }) {
  const acts = plan.steps.flatMap((s) => s.acts);
  const lineAct = acts.find((a) => a.type === "line");
  return (
    <g>
      <Plane C={C} g={g} />
      {lineAct && <Line plan={plan} k={seg(t, lineAct.a, lineAct.b, E.lin)} C={C} g={g} />}
      {acts.filter((a) => a.type === "move").map((a, i) => <Move key={i} a={a} t={t} C={C} g={g} />)}
      {acts.filter((a) => a.type === "dot").map((a, i) => (
        <Dot key={i} P={a.P} m={plan.m} C={C} k={seg(t, a.a, a.b, E.lin)} g={g} />
      ))}
    </g>
  );
}

/** 한 문항 한 순간(t — 1배속 ms). pane — 듀얼 모드의 반쪽 판(위에 문제 · 지금 순서 한 줄, 아래에 좌표평면) */
export function GraphArt({ it, t, C, pane = false }) {
  if (pane) return <GraphPaneArt it={it} t={t} C={C} />;
  const plan = gdPlan(it), Lo = layoutOf(it);
  const cur = stepAt(plan, t);
  const qo = seg(t, 0, 600, E.sine);
  const ans = seg(t, plan.ans, plan.ans + 700, E.sine);
  const L = Lo.box.left;
  return (
    <g>
      <PlaneArt plan={plan} t={t} C={C} g={G1} />
      <g opacity={qo}>
        {Lo.qLines.map((s, i) => (
          <MText key={i} x={L} y={Lo.qY[i]} s={toM(s)} size={Lo.qs} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />
        ))}
      </g>
      {plan.steps.map((st, i) => <StepLine key={i} st={st} Ls={Lo.steps[i]} i={i} t={t} cur={cur} C={C} ss={Lo.ss} box={Lo.box} />)}
      {ans > 0 && (
        <g opacity={ans}>
          <text x={L} y={Lo.ansY} fontFamily={SANS} fontSize={Lo.ss * 0.82} fontWeight={700} fill={C.soft}>정답 직선</text>
          <MText x={L + Lo.ss * 4.4} y={Lo.ansY} s={toM(linStr(plan.m, plan.b))} size={Lo.ss * 1.12} weight={700} fill={C.blue} C={C} />
        </g>
      )}
    </g>
  );
}

/** 듀얼 반쪽 판 — 순서는 지금 것만(바뀔 때 겹쳐 넘어감), 다 그리면 그 자리에 정답 직선 */
function GraphPaneArt({ it, t, C }) {
  const plan = gdPlan(it), Lo = paneLayoutOf(it);
  const cur = stepAt(plan, t);
  const qo = seg(t, 0, 600, E.sine);
  const ans = seg(t, plan.ans, plan.ans + 700, E.sine);
  const L = Lo.box.left;
  const n = plan.steps.length;
  return (
    <g>
      <PlaneArt plan={plan} t={t} C={C} g={Lo.geo} />
      <g opacity={qo}>
        {Lo.qLines.map((s, i) => <MText key={i} x={L} y={Lo.qY[i]} s={toM(s)} size={Lo.qs} weight={i === 0 ? 620 : 560} fill={C.ink} C={C} />)}
      </g>
      {plan.steps.map((st, i) => {
        // 이 순서가 보이는 정도 — 다음 순서가 오기 직전에 사라지고, 그다음에 새 순서가 나타난다(겹치지 않게)
        const nextA = i + 1 < n ? plan.steps[i + 1].a : plan.ans;
        const o = seg(t, st.a, st.a + 320, E.sine) * (1 - seg(t, nextA - 300, nextA, E.sine));
        if (o <= 0.01) return null;
        return <StepLine key={i} st={st} Ls={Lo.steps[i]} i={i} t={t} cur={cur} C={C} ss={Lo.ss} box={Lo.box} o={o} />;
      })}
      {ans > 0 && (
        <g opacity={ans}>
          <text x={L} y={Lo.ansY} fontFamily={SANS} fontSize={Lo.ss * 0.82} fontWeight={700} fill={C.soft}>정답 직선</text>
          <MText x={L + Lo.ss * 4.4} y={Lo.ansY} s={toM(linStr(plan.m, plan.b))} size={Lo.ss * 1.12} weight={700} fill={C.blue} C={C} />
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
      grp: GD_KIND[it.kind], marks: stepMarks({ lines: plan.steps, ans: plan.ans }, plan.steps.map((x) => ({ s: x.text })), sp), card: GD_KIND[it.kind],
      title: { e: title, m: title }, sub: { e: sub, m: sub }, tsz: "lesson",
      render: (mode, t, C) => <GraphArt it={it} t={t * sp} C={C} />,
      pane: (t, C) => <GraphArt it={it} t={t * sp} C={C} pane />,
    };
  });
  SCENES.set(k, list);
  return list;
}

/* ══════════ 액자 — 조작은 해설 액자 공통 틀(frames/lesson.jsx) ══════════ */
export const GD_SPEC = {
  lsk: "ash.display.graph", title: "일차함수 그래프 그리기 해설", defSet: "basic", cols: 6,
  topExtra: sigTop("graph"),                                 // 오른쪽 위 📄 — 원본 프린트(문제지 · 정답) 받기
  sets: [{ key: "basic", name: "기본 96제", short: "기본 96" }, { key: "hard", name: "심화 64제", short: "심화 64" }],
  stages: () => [],
  scenes: (set, sp) => graphScenes(set, sp),
  posKey: (lsk, set) => `${lsk}.${set}`,
  paneHead: (S, s) => `${S.short} · ${s.no}번 · ${s.grp}`,
};
export function GraphFrame(props) {
  return <LessonFrame spec={GD_SPEC} {...props} />;
}

/** 액자 목록의 작은 그림 — 심화 41번(일차방정식과 평행) 다 그린 순간 */
export const GraphThumb = memo(function GraphThumb({ C }) {
  const it = GD_SETS.hard.items[40];
  return <GraphArt it={it} t={gdPlan(it).ans + 800} C={C} />;
});
