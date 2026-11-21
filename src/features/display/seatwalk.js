// ashrain.out — 「한 줄로 세우기」 해설 그림의 움직임 차례 (seatwalk.js) — 그리기는 frames/c100fig.jsx 의 SeatsFig
// 칠판에서 하듯 자리를 하나씩 채운다:
//   자리마다 후보가 돌아가며 지나가고(룰렛) 위의 수가 1, 2, 3 … 으로 세어진 뒤, 한 사람이 앉고 그 자리의 가짓수가 찍힌다.
//   다음 자리에서는 앉은 사람이 빠져 후보가 하나 적다 — 「5 × 4 × 3」이 왜 줄어드는지가 눈에 보이게.
//   고정된 사람(금빛)은 줄이 나올 때 먼저 내려앉고, 묶음은 한데 모여 띠로 묶인 뒤 하나처럼 움직이며, 묶음 안 순서는 따로 섞어 보인다(× 2).
//   빈자리 ∨ 에 넣을 때(이웃하지 않기)는 남은 빈자리를 하나씩 짚어 세고 그 가운데 하나에 내려앉는다.
//   양 끝 바꾸기(× 2)는 두 자리가 실제로 자리를 바꿨다 돌아온다.
// 사람 이름은 문제에서 읽는다(A, B, C … 또는 남학생 · 여학생 — 남₁ 남₂ …). 움직임이 판서 줄 안에 다 돌도록 줄마다 hold 를 더한다(seatsPrep).
import { lineLen } from "./lin10.js";

/** 문제에 나오는 사람 — 글자(A, B, C …) 또는 남 · 여 수 */
export function peopleOf(it) {
  const q = it.q || "";
  const m1 = q.match(/([A-H](?:, [A-H])+)\s*(\d+)명/);
  if (m1) return { kind: "letter", list: m1[1].split(/,\s*/) };
  const m2 = q.match(/남학생\s*(\d+)명과\s*여학생\s*(\d+)명/);
  if (m2) return { kind: "gender", b: +m2[1], g: +m2[2] };
  return null;
}

/** 사람 하나 — { lab: "A" } · { lab: "남", i: 1 } · 묶음 { bundle: [사람 …] } */
const tokLab = (k) => (k.bundle ? k.bundle.map(tokLab).join("") : `${k.lab}${k.i || ""}`);
export const SEAT_T = { INTRO: 650, START: 260, SETTLE: 220, GAP_DROP: 320, INNER: 1150, SWAP: 1500, NOTE: 520, TAIL: 320 };
/** 후보 하나를 지나가는 시간 — 후보가 많으면 빨리(휘리릭) */
export const reelTick = (n) => Math.max(70, Math.min(150, 520 / Math.max(1, n)));
export const gapTick = (n) => Math.max(90, Math.min(170, 560 / Math.max(1, n)));

const PLANS = new WeakMap();
/**
 * 줄마다 자리 채우는 차례. rows[ri] = { units[ui] = { tok(앉을 사람 · 끝 모습), members(묶음) }, acts[] }
 *   act: reel { ri, ui, cands[], pick, line } · gap { ri, ui, avail[ui …], tok, line } · inner { ri, ui, line } · swap { ri, sw, line } · note { ri, line }
 *   cands 수가 가짓수(cnt)와 다르면 이름 없이 1 ~ cnt 로 센다(ok = false).
 */
export function seatsPlan(it) {
  if (PLANS.has(it)) return PLANS.get(it);
  const f = it.fig, who = peopleOf(it);
  const rows = f.rows.map((r, ri) => {
    // 이 줄의 사람들(줄마다 처음부터)
    let pool = [];
    if (who?.kind === "letter") pool = who.list.map((lab) => ({ lab }));
    else if (who?.kind === "gender") {
      for (let i = 1; i <= who.b; i++) pool.push({ lab: "남", i });
      for (let i = 1; i <= who.g; i++) pool.push({ lab: "여", i });
    }
    const take = (pred) => { const j = pool.findIndex(pred); return j < 0 ? null : pool.splice(j, 1)[0]; };
    const takeLab = (lab) => take((k) => !k.bundle && k.lab === lab);
    const hasGap = r.units.some((u) => u.gap);
    const genderCat = (u) => (u.lab[0] === "남" || u.lab[0] === "여") && (u.hi || r.mixed || hasGap);
    const units = r.units.map((u) => ({ tok: null, members: null }));
    // 묶음 — 사람들을 먼저 꺼내 한 덩이로(남 · 여 묶음은 그 성별에서 차례로)
    r.units.forEach((u, ui) => {
      if (u.gap || u.w <= 1) return;
      const mem = u.lab.map((lab) => (lab === "남" || lab === "여" ? takeLab(lab) : takeLab(lab)) || { lab });
      const b = { bundle: mem };
      units[ui].members = mem;
      units[ui].tok = b;
      pool.push(b);               // 묶음은 「한 사람」처럼 자리를 고르는 후보가 된다
    });
    // 고정된 사람(금빛 · 가짓수 없음) — 줄이 나올 때 먼저 앉는다
    r.units.forEach((u, ui) => {
      if (u.gap || u.w > 1 || !u.hi || u.cnt != null) return;
      units[ui].tok = takeLab(u.lab[0]) || { lab: u.lab[0] };
      units[ui].fixed = true;
    });
    // 묶음 중 가짓수가 없는 것(자리가 정해진 묶음)은 처음부터 그 자리에
    r.units.forEach((u, ui) => {
      if (u.w > 1 && u.cnt == null) { const j = pool.indexOf(units[ui].tok); if (j >= 0) pool.splice(j, 1); units[ui].fixed = true; }
    });
    // 가짓수를 세는 차례 — 그 줄(ca · cntAt) 먼저, 같은 줄이면 성별이 정해진 자리(양 끝 남 · 여 …)를 먼저, 그다음 왼쪽부터
    const order = r.units.map((u, ui) => ({ u, ui, line: u.ca != null ? u.ca : r.cntAt, pri: !u.gap && u.w <= 1 && genderCat(u) && !r.mixed ? 0 : 1 }))
      .filter((x) => x.u.cnt != null)
      .sort((a, b) => a.line - b.line || a.pri - b.pri || a.ui - b.ui);
    const acts = [];
    const gapsLeft = r.units.map((u, ui) => (u.gap ? ui : -1)).filter((ui) => ui >= 0);
    const insertLab = (() => {         // 빈자리에 넣는 쪽 — 빈자리가 아닌 칸에 없는 성별
      const used = new Set(r.units.filter((u) => !u.gap).flatMap((u) => u.lab));
      return used.has("남") && !used.has("여") ? "여" : used.has("여") && !used.has("남") ? "남" : "여";
    })();
    for (const { u, ui, line } of order) {
      const cnt = +u.cnt;
      if (u.gap) {
        const avail = gapsLeft.slice();
        const tok = takeLab(insertLab) || { lab: insertLab };
        gapsLeft.splice(gapsLeft.indexOf(ui), 1);
        units[ui].tok = tok;
        acts.push({ type: "gap", ri, ui, avail, tok, cnt, line, ok: avail.length === cnt });
        continue;
      }
      let cands;
      if (genderCat(u)) cands = pool.filter((k) => !k.bundle && k.lab === u.lab[0]);
      else cands = pool.slice();
      let pick;
      if (u.w > 1) pick = units[ui].tok;
      else if (genderCat(u)) pick = cands[0];
      else if (u.lab[0]) pick = cands.find((k) => !k.bundle && k.lab === u.lab[0]) || cands.find((k) => !k.bundle);
      else pick = cands.find((k) => !k.bundle);
      const ok = cands.length === cnt && !!pick;
      if (pick) pool.splice(pool.indexOf(pick), 1);
      units[ui].tok = pick || units[ui].tok;
      acts.push({ type: "reel", ri, ui, cands: ok ? cands.slice() : Array.from({ length: cnt }, (_, j) => ({ lab: String(j + 1) })), pick, cnt, line, ok });
    }
    r.units.forEach((u, ui) => { if (u.inner && u.w > 1) acts.push({ type: "inner", ri, ui, line: r.innerAt, n: u.w }); });
    r.swaps.forEach((sw, si) => acts.push({ type: "swap", ri, si, line: sw.at }));
    if (r.note) acts.push({ type: "note", ri, line: r.noteAt });
    return { units, acts };
  });
  const out = { rows, who };
  PLANS.set(it, out);
  return out;
}

/** 움직임 하나의 길이(ms) */
export function actMs(a) {
  if (a.type === "reel") return a.cnt * reelTick(a.cnt) + SEAT_T.SETTLE;
  if (a.type === "gap") return a.cnt * gapTick(a.cnt) + SEAT_T.GAP_DROP;
  if (a.type === "inner") return SEAT_T.INNER + (a.n > 2 ? 250 : 0);
  if (a.type === "swap") return SEAT_T.SWAP;
  return SEAT_T.NOTE;
}
const RANK = { reel: 0, gap: 0, inner: 1, swap: 2, note: 3 };
/** 줄마다 움직임 차례(그 줄에 든 것을 줄 순서 · 종류 순서대로) */
function byLine(it) {
  const { rows } = seatsPlan(it), m = new Map();
  rows.forEach((R) => R.acts.forEach((a) => { if (!m.has(a.line)) m.set(a.line, []); m.get(a.line).push(a); }));
  for (const v of m.values()) v.sort((a, b) => RANK[a.type] - RANK[b.type] || a.ri - b.ri);
  return m;
}
/** 줄이 나오는 순간에 먼저 도는 것(고정된 사람 내려앉기 · 묶음 묶기)이 있는 줄 */
const introLines = (it) => new Set(it.fig.rows.filter((r, ri) => seatsPlan(it).rows[ri].units.some((u) => u.fixed || u.members)).map((r) => r.at));

/** 판서 줄마다 그림 움직임에 필요한 시간 — 모자라면 hold 로 늘린다 */
export function seatsPrep(it) {
  if (!it.fig || it.fig.kind !== "seats") return;
  const m = byLine(it), intro = introLines(it);
  const lines = new Set([...m.keys(), ...intro]);
  for (const i of lines) {
    const ln = it.lines[i];
    if (!ln) continue;
    const acts = m.get(i) || [];
    const need = SEAT_T.START + (intro.has(i) ? SEAT_T.INTRO : 0) + acts.reduce((s, a) => s + actMs(a), 0) + SEAT_T.TAIL;
    const len0 = lineLen({ ...ln, hold: 0 }), body = lineLen({ ...ln, hold: 0, memo: null });
    ln.hold = len0 >= need ? 0 : Math.max(0, Math.round(need - body));
  }
}

const TIMES = new WeakMap();
/** 시각표 — 움직임마다 t0 · t1 (P = l10Plan(it)), 줄이 나오는 시각 rowAt[ri] · 고정 · 묶음 내려앉는 introAt[ri] */
export function seatsTimes(it, P) {
  if (TIMES.has(it)) return TIMES.get(it);
  const m = byLine(it), intro = introLines(it);
  const L = (i) => P.lines[Math.min(Math.max(0, i), P.lines.length - 1)];
  const timed = [];
  for (const [i, acts] of m) {
    let c = L(i).a + SEAT_T.START + (intro.has(i) ? SEAT_T.INTRO : 0);
    for (const a of acts) { const d = actMs(a); timed.push({ ...a, t0: c, t1: c + d }); c += d; }
  }
  const rowAt = it.fig.rows.map((r) => L(r.at).a);
  const out = { acts: timed, rowAt, introAt: rowAt.map((a) => a + 120) };
  TIMES.set(it, out);
  return out;
}
export const tokLabel = tokLab;
