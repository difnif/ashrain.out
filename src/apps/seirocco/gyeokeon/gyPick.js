// 시록고 · 격언 도우미 — 달마다 격언 고르기 (GY-2)
// 같은 규칙의 기준 구현은 pick_gy.py(격언 그림 원문 대조 도구). 같은 달 기록이면 같은 항목을 고른다(tests/gyeokeon.test.mjs).
// 규칙 문서: 프로젝트 ME-수학 교육의 claude/SPEC-격언그림-항목규칙-v2.md 3절 · claude/HANDOFF-격언그림-시록고-v1.md
//
//   const data = await (await fetch("/gyeokeon/gyeokeon.v2.json")).json()
//   const picks = pickMonths(seed, months, data.entries)   // picks[i] = { label, id, score, entry, ctx }
//   fillReport(picks[i].entry, "소현", months[i].cum)       // → 보고서 문장
//
// 달(month) 하나에 쓰는 값: label, who('P' 박재우 선생님 · 'O' 다른 선생님 · 'AI' AI 문장 · 'E' 코멘트 없음),
//   S{아홉 유형 몫}(주 유형은 여기서 정한다), dacc(정답률 변화 — 고르는 데만 쓰고 어디에도 보이지 않는다),
//   cum(누적 문항), n · med_n(이달 문항 · 본인 중앙값) 또는 R(이달 비율 밴드), band.vol 또는 vb(기복 밴드 0~5).
//   PRZ-1 정식 코드에서 만든 달(codeline.js)은 nth(그 학생 기록의 몇 번째 달)와 prevCum(앞달 누적)을 따로 준다.

export const TYPES = ["rush", "shadow", "cross", "steady", "stubborn", "cue", "evap", "shrink", "auto"];

const enc = new TextEncoder();

/** FNV-1a 32비트(UTF-8 바이트). 같은 이름 + 같은 항목 번호면 같은 값 */
export function fnv1a(str) {
  let h = 2166136261;
  for (const b of enc.encode(str)) h = Math.imul(h ^ b, 16777619) >>> 0;
  return h;
}

/** 이달 비율 밴드 R: 이달 문항 ÷ 본인 중앙값, 컷 0.6 · 0.9 · 1.1 · 1.4 → 1~5 */
export function rband(n, med) {
  if (!med) return 3;
  const r = n / med;
  return r < 0.6 ? 1 : r < 0.9 ? 2 : r < 1.1 ? 3 : r < 1.4 ? 4 : 5;
}

/** 주 유형 = S에서 가장 큰 몫. 동점이거나 모두 0이면 null(주 유형 없음). 그리는 코드의 domIdx와 같다.
 *  달 기록의 'dom' 칸은 주 렌즈(수치·원인·정서…)라서 쓰지 않는다. */
export function dominantType(S) {
  const w = TYPES.map((k) => S[k] || 0), top = Math.max(...w);
  if (!(top > 0) || w.filter((v) => top - v < 1e-9).length > 1) return null;
  return TYPES[w.indexOf(top)];
}

/** 그달의 고르기 맥락. prevCum = 앞달 누적 문항(첫 달 0) */
export function monthContext(m, i, prevCum) {
  const S = m.S;
  const mx = Math.max(...Object.values(S)) || 1;
  const s = {};
  for (const k of TYPES) s[k] = S[k] / mx;
  if (!dominantType(S)) {  // 주 유형 없음(동점·미분화)
    for (const k of TYPES) s[k] = s[k] * 0.5;
    s.none = 1.0;
  } else s.none = 0.0;
  const d = m.dacc || 0;
  const nth = m.nth ?? i + 1;
  return {
    s, cum: m.cum, prev_cum: (m.prevCum ?? prevCum) || 0, vb: m.band ? m.band.vol : m.vb,
    R: m.R ?? rband(m.n, m.med_n), sig: m.cum / 100,
    nth, who: m.who, dir: nth === 1 ? "○" : d > 0 ? "↑" : d < 0 ? "↓" : "→",
  };
}

/** 점수 = Σ 유형 무게 × s(유형) ÷ 3 + 조건 + 사건 */
export function scoreEntry(e, c) {
  let ts = 0;
  for (const [k, w] of Object.entries(e.types)) ts += w * (c.s[k] ?? 0);
  ts = ts / 3;
  let b = 0;
  for (const [k, v] of Object.entries(e.when || {})) {
    if (k === "dir") b += v.includes(c.dir) ? 0.2 : 0;               // 오른 달에만 덤, 내린 달은 아무것도 안 함
    else if (k === "who") b += v.includes(c.who) ? (v.includes("E") ? 0.45 : 0.1) : -2;
    else { const [lo, hi] = v; b += (lo <= c[k] && c[k] <= hi) ? 0.1 : -2; }   // vb · R · nth
  }
  for (const [k, v] of Object.entries(e.event || {})) {
    let ok = false;
    if (k === "nth") ok = c.nth === v;
    else if (k === "nthIn") ok = v.includes(c.nth);
    else if (k === "sigCross") ok = c.nth > 1 && c.prev_cum < v * 100 && v * 100 <= c.cum;
    b += ok ? 1.0 : -5;
  }
  return ts + b;
}

/** 한 아이의 달들(오래된 달부터)에 격언을 하나씩 고른다. seed = 이름 씨앗 */
export function pickMonths(seed, months, entries) {
  const used = new Map(), out = [];
  let prev = 0;
  months.forEach((m, i) => {
    const c = monthContext(m, i, prev);
    prev = m.cum;
    let best = null;
    for (const e of entries) {
      let sc = scoreEntry(e, c) + (fnv1a(seed + e.id) % 1000) / 20000;
      const last = used.get(e.id);
      const isEvent = !!e.event && Object.keys(e.event).length > 0;
      if (last !== undefined && !isEvent) sc -= (c.nth - last < 24) ? 1.5 : 0.3;   // 같은 아이에게 2년 안에 다시 주지 않음
      if (best === null || sc > best.sc || (sc === best.sc && e.id > best.id)) best = { sc, id: e.id, e };
    }
    used.set(best.id, c.nth);
    out.push({ label: m.label, id: best.id, score: Math.round(best.sc * 100) / 100, entry: best.e, ctx: c });
  });
  return out;
}

/** 짧은 이름 + 이는/는 (받침 있으면 '이는') */
export function nameWithTopic(short) {
  const ch = short.charCodeAt(short.length - 1);
  const batchim = ch >= 0xac00 && ch <= 0xd7a3 && (ch - 0xac00) % 28 !== 0;
  return short + (batchim ? "이는" : "는");
}

/** 보고서 문장: {N} → '소현이는', {C} → '1,234' */
export function fillReport(entry, short, cum) {
  return entry.report.replace("{N}", nameWithTopic(short)).replace("{C}", Math.round(cum).toLocaleString("en-US"));
}

/** 선생님 카드(정확하게): 출전 · 원문 · 음 · 뜻 · 표제 출처 · 판본 표기 · 대조 출처 */
export function teacherCard(entry) {
  const ed = Object.entries(entry.check.edition_chars || {}).map(([a, b]) => `${a}→${b}`).join(", ");
  return {
    title: `${entry.label} ${entry.label_eum}`,
    source: entry.src,
    text: entry.text, eum: entry.eum, meaning: entry.meaning,
    labelNote: entry.label_kind === "후대 줄임" ? "표제는 후대의 줄임말이라 원문 구절과 함께 적는다" : "",
    edition: ed ? `대조 판본 표기: ${ed}` : "",
    checked: entry.check.how === "웹 인용 대조" ? `웹 인용 대조: ${entry.check.against}` : `원문 대조: ${entry.check.against}`,
  };
}
