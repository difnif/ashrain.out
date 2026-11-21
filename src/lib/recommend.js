// ashrain.out — 우물 추천: 꾹 누른 해설 둘레에 띄울 콘텐츠 6가지 (순수 함수 + 학생 기록 읽기)
// 두 가지 길:
//   · 기본(default) — 학습 기록이 없거나 모자랄 때. 교육과정 단원 지도(lib/units.js)로 고른다:
//       이어서(같은 단원 다음 회차) 2 · 앞 단원 다지기 2 · 다음 단원 미리 보기 2 → 모자라면 같은 단원 · 같은 주로 채운다.
//   · 맞춤(personal) — 기록이 넉넉할 때. 단원마다 숙달도(문항 풀이 정답률의 베타 평균)와 본 기록(lib/avHistory.js)으로 점수를 매긴다:
//       약한 앞 단원 다지기(숙달도 < 0.6) · 지금 수준에 맞는 회차(숙달도에 따라 개념 → 연습 → 응용 → 마무리) ·
//       이어서 볼 회차(안 본 다음 회차) · 다시 볼 때(14일 넘게 지난 것, 숙달도가 낮으면 더) · 다음 단원 도전(숙달도 ≥ 0.75) —
//       한 단원에서 셋까지, 이유(rel)를 카드에 붙인다. 방금(3일 안) 본 것은 뒤로.
//   넉넉함의 기준: 단원을 아는 풀이 15개 이상 또는 절반 넘게 본 해설 5개 이상.
// pool 항목 모양: { key, unit, gidx(학년 차례 0 ~ 11), week?, kind?, seq?, title, short?, icon, grade } — 회차와 단원 100제가 섞여도 된다.
import { prevUnits, nextUnits, termRank } from "./units.js";
import { CHAPTERS } from "./chapters.js";

export const MAX = 6;
const KIND_STEP = { 개념: 0, 예습: 0, 연습: 1, 복습: 1, 응용: 2, 마무리: 3 };
const DAY = 86400000;

/** 단원 숙달도 — 정답률의 베타(1, 1) 평균, 3문항 미만이면 모름(null) */
export function masteryOf(profile, unit) {
  const r = profile?.mastery?.[unit];
  if (!r || r.n < 3) return null;
  return (r.ok + 1) / (r.n + 2);
}
/** 맞춤 추천을 쓸 만큼 기록이 있나 */
export function profileEnough(profile) {
  if (!profile) return false;
  const n = Object.values(profile.mastery || {}).reduce((s, r) => s + (r.n || 0), 0);
  const seen = Object.values(profile.watched || {}).filter((r) => r.n > 0 && r.max >= r.n / 2).length;
  return n >= 15 || seen >= 5;
}

/** 한 방향으로 단원 지도를 몇 단계까지 — 가까운 것부터 [단원] */
function walk(u, step, depth = 3) {
  const out = [], seen = new Set([u]);
  let front = [u];
  for (let d = 1; d <= depth; d++) {
    const nx = [];
    for (const x of front) for (const y of step(x)) if (!seen.has(y)) { seen.add(y); nx.push(y); out.push({ u: y, d }); }
    front = nx;
  }
  return out;
}
const order = (a, b) => (a.gidx ?? 99) - (b.gidx ?? 99) || (a.week ?? 0) - (b.week ?? 0) || String(a.key).localeCompare(String(b.key));
const card = (c, rel) => ({ ...c, rel });

/** 기본 — 교육과정 지도 */
export function defaultPicks(item, pool, max = MAX) {
  if (!item) return [];
  const others = pool.filter((c) => c.key !== item.key);
  const out = [], used = new Set([item.key]);
  const push = (c, rel) => { if (c && !used.has(c.key) && out.length < max) { used.add(c.key); out.push(card(c, rel)); } };
  const sameUnit = others.filter((c) => c.unit === item.unit).sort(order);
  // ① 이어서 — 같은 단원에서 이 뒤(같은 학년이면 다음 주, 단원 100제는 회차 뒤에)
  const after = sameUnit.filter((c) => (c.gidx ?? 99) > (item.gidx ?? 99) || ((c.gidx ?? 99) === (item.gidx ?? 99) && (c.week ?? 99) > (item.week ?? -1)));
  after.slice(0, 2).forEach((c) => push(c, "이어서"));
  // ② 앞 단원 — 가까운 앞 단원의 마무리 · 개념(없으면 아무 회차 · 단원 100제)
  const pick1 = (units, prefer) => {
    const got = [];
    for (const { u } of units) {
      const cs = others.filter((c) => c.unit === u).sort(order);
      if (!cs.length) continue;
      const best = cs.find((c) => prefer.includes(c.kind)) || cs[0];
      got.push(best);
      if (got.length >= 3) break;
    }
    return got;
  };
  pick1(walk(item.unit, prevUnits).sort((a, b) => a.d - b.d || termRank(b.u) - termRank(a.u)), ["마무리", "개념"]).slice(0, 2).forEach((c) => push(c, "앞 단원"));
  // ③ 다음 단원 — 개념 회차부터
  pick1(walk(item.unit, nextUnits).sort((a, b) => a.d - b.d || termRank(a.u) - termRank(b.u)), ["개념", "예습"]).slice(0, 2).forEach((c) => push(c, "다음 단원"));
  // ④ 채우기 — 같은 단원 다른 회차 · 같은 주 · 같은 학년
  sameUnit.forEach((c) => push(c, "같은 단원"));
  others.filter((c) => c.gidx === item.gidx && c.week === item.week).forEach((c) => push(c, "같은 주"));
  others.filter((c) => c.gidx === item.gidx).sort((a, b) => Math.abs((a.week ?? 0) - (item.week ?? 0)) - Math.abs((b.week ?? 0) - (item.week ?? 0))).forEach((c) => push(c, "같은 학년"));
  return out;
}

/** 맞춤 — 숙달도 · 본 기록으로 점수 */
export function personalPicks(item, pool, profile, { now = Date.now(), max = MAX } = {}) {
  const W = profile.watched || {};
  const mt = masteryOf(profile, item.unit);
  const prev = new Map(walk(item.unit, prevUnits, 2).map((x) => [x.u, x.d]));
  const next = new Map(walk(item.unit, nextUnits, 2).map((x) => [x.u, x.d]));
  const level = mt == null ? 1 : mt < 0.5 ? 0 : mt < 0.8 ? 1.5 : 3;      // 지금 단원에서 알맞은 회차 종류(0 개념 … 3 마무리)
  const scored = [];
  for (const c of pool) {
    if (c.key === item.key) continue;
    const w = W[c.key], age = w ? (now - w.t) / DAY : Infinity;
    const m = masteryOf(profile, c.unit);
    let s = 0, rel = null;
    if (prev.has(c.unit)) {
      if (m != null && m < 0.6) { s = 2.2 + (0.6 - m) * 3 - prev.get(c.unit) * 0.2; rel = "약한 앞 단원"; }
      else { s = 0.6 - prev.get(c.unit) * 0.2; rel = "앞 단원"; }
      if (KIND_STEP[c.kind] === 3 || KIND_STEP[c.kind] === 0) s += 0.2;
    } else if (c.unit === item.unit) {
      const k = KIND_STEP[c.kind] ?? 1.5;
      s = 1.8 - Math.abs(k - level) * 0.5;
      rel = "지금 수준";
      if (!w && (c.gidx ?? 0) === (item.gidx ?? 0) && (c.week ?? 0) > (item.week ?? 0)) { s += 0.5; rel = "이어서"; }
    } else if (next.has(c.unit)) {
      s = (mt != null && mt >= 0.75 ? 1.9 : 0.5) - next.get(c.unit) * 0.3;
      rel = mt != null && mt >= 0.75 ? "다음 단원 도전" : "다음 단원";
      if (KIND_STEP[c.kind] === 0) s += 0.2;
    } else continue;
    if (w) {
      if (age < 3) s -= 1.6;
      else if (age > 14) { s += 0.4 + (m != null && m < 0.6 ? 0.5 : 0); rel = rel === "약한 앞 단원" ? rel : "다시 볼 때"; }
      else s -= 0.4;
    } else s += 0.2;
    scored.push({ c, s, rel });
  }
  scored.sort((a, b) => b.s - a.s || order(a.c, b.c));
  const out = [], per = {};
  const take = (x) => {
    if (out.length >= max || out.some((o) => o.key === x.c.key)) return;
    if ((per[x.c.unit] || 0) >= 3) return;
    per[x.c.unit] = (per[x.c.unit] || 0) + 1;
    out.push(card(x.c, x.rel));
  };
  // 꼭 넣을 것: 약한 앞 단원 하나 · (숙달도가 높으면) 다음 단원 도전 하나
  const weak = scored.find((x) => x.rel === "약한 앞 단원");
  if (weak) take(weak);
  const up = scored.find((x) => x.rel === "다음 단원 도전");
  if (up) take(up);
  for (const x of scored) take(x);
  if (out.length < max) for (const c of defaultPicks(item, pool, max)) if (out.length < max && !out.some((o) => o.key === c.key)) out.push(c);
  return out;
}

/** 우물 추천 — { mode: "personal" | "default", cards } */
export function recommend(item, pool, profile, opts = {}) {
  const max = opts.max || MAX;
  if (profileEnough(profile)) return { mode: "personal", cards: personalPicks(item, pool, profile, { ...opts, max }) };
  return { mode: "default", cards: defaultPicks(item, pool, max) };
}

/* ══════════ 학생 기록 → 단원 숙달도 ══════════ */
/** 개념(unit_id · sort_order)으로 단원 이름 "m2-1:일차함수" */
export function unitOfConcept(concept) {
  if (!concept) return null;
  const chs = CHAPTERS[concept.unit_id];
  if (!chs) return null;
  const ch = chs.find((x) => Number(concept.sort_order) >= x[1] && Number(concept.sort_order) <= x[2]);
  return ch ? `${concept.unit_id}:${ch[0]}` : null;
}
/** 풀이 기록 · 문항 · 개념 → { 단원: { ok, n } } */
export function masteryFrom(attempts, itemsById, conceptsById) {
  const out = {};
  for (const a of attempts || []) {
    const it = itemsById.get(a.item_id);
    const cid = it?.concept_ids?.[0];
    const u = cid != null ? unitOfConcept(conceptsById.get(cid)) : null;
    if (!u) continue;
    const r = (out[u] ||= { ok: 0, n: 0 });
    r.n += 1;
    if (a.correct) r.ok += 1;
  }
  return out;
}
