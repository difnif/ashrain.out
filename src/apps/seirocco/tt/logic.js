// 시록고 강사도구 — 채점 계산(순수 함수). PC server.py 의 summarize · current_marks · round_marks · rounds_info ·
// grading_stats · wrong_history · auto_judge 를 그대로 옮김.

export const CODE_ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ";
export const normCode = (s) => String(s || "").toUpperCase().split("").filter((c) => CODE_ALPHA.includes(c)).join("");
export const fmtCode = (c) => (c && c.length === 6 ? c.slice(0, 3) + "-" + c.slice(3) : c || "");
export function newCode() {
  const a = new Uint32Array(6);
  crypto.getRandomValues(a);
  return [...a].map((x) => CODE_ALPHA[x % CODE_ALPHA.length]).join("");
}
export const nowIso = () => new Date().toISOString();
export const todayStr = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
export const normName = (s) => String(s || "").replace(/\s+/g, " ").trim();

export function summarize(marksOrItems) {
  const s = { O: 0, X: 0, U: 0, none: 0 };
  for (const it of marksOrItems) {
    const r = (it && it.mark ? it.mark.result : it && it.result) || "";
    s[["O", "X", "U"].includes(r) ? r : "none"]++;
  }
  s.total = marksOrItems.length;
  return s;
}

// marks: [{id, seq, result, answer, session_no, at}] (id 오름차순), sessions: [{no, round, kind, targets, …}]
export function roundOfSession(sessions) {
  const m = new Map();
  for (const s of sessions) m.set(s.no, s.round || 1);
  return m;
}
// 셈에 드는 기록: 다시 풀기 차의 기록은 그 차 다시 풀 문항 것만 — 앞 차를 고쳐 그 차에서 빠진 문항의 기록은 지우지 않고
// 셈에서만 뺀다(다시 들어오면 다시 보임). SQL tt_marks_eff 와 같음.
export function effectiveMarks(marks, sessions) {
  const tg = new Map();
  for (const s of sessions) if (s.kind === "retry" && Array.isArray(s.targets)) tg.set(s.no, new Set(s.targets));
  return marks.filter((m) => { const t = tg.get(m.session_no); return !t || t.has(m.seq); });
}
// 문항의 한 차 결과 = 그 차의 마지막 기록, 지금(최종) 결과 = 기록이 있는 가장 늦은 차의 결과.
// 앞 차를 고친 기록(2차를 시작한 뒤 1차를 고침)은 id 가 더 커도 늦은 차 결과를 덮지 않는다 — SQL tt_current 와 같은 차례.
export function currentMarks(marks, sessions) {
  const rs = roundOfSession(sessions);
  const rd = (m) => rs.get(m.session_no) || 1;
  const out = new Map();
  for (const m of [...effectiveMarks(marks, sessions)].sort((a, b) => rd(a) - rd(b) || a.id - b.id)) out.set(m.seq, { ...m, round: rd(m) });
  return out;
}
export function roundMarks(marks, sessions) {
  const rs = roundOfSession(sessions);
  const out = new Map(); // round → Map(seq → mark)
  for (const m of [...effectiveMarks(marks, sessions)].sort((a, b) => a.id - b.id)) {
    const r = rs.get(m.session_no) || 1;
    if (!out.has(r)) out.set(r, new Map());
    out.get(r).set(m.seq, { ...m, round: r });
  }
  return out;
}
export function roundsInfo(sessions, marks, seqs) {
  const rm = roundMarks(marks, sessions);
  const out = new Map();
  for (const se of [...sessions].sort((a, b) => a.no - b.no)) {
    const r = se.round || 1;
    if (!out.has(r)) out.set(r, { round: r, kind: se.kind || "solve", targets: null, sessions: 0, started_at: se.started_at, ended_at: null, end_reason: null });
    const o = out.get(r);
    o.sessions += 1;
    o.ended_at = se.ended_at;
    o.end_reason = se.end_reason;
    if (se.targets && o.targets === null) o.targets = se.targets;
  }
  const gd = new Map(gradedDays(marks, sessions).map((x) => [x.round, x]));
  return [...out.keys()].sort((a, b) => a - b).map((r) => {
    const o = out.get(r);
    const tg = o.targets !== null ? o.targets : seqs;
    const ms = rm.get(r) || new Map();
    o.summary = summarize(tg.map((s) => ({ mark: ms.get(s) })));
    o.graded_first = gd.get(r)?.first || null;       // 그 차를 매긴 날(처음 · 마지막)
    o.graded_last = gd.get(r)?.last || null;
    return o;
  });
}
export function gradingStats(marks, sessions, nItems) {
  const cur = currentMarks(marks, sessions);
  const pad = (m) => [...m.values()].map((x) => ({ mark: x })).concat(Array(Math.max(0, (nItems || 0) - m.size)).fill({ mark: null }));
  const fin = summarize(pad(cur));
  const r1 = roundMarks(marks, sessions).get(1) || new Map();
  const s1 = summarize(pad(r1));
  const nr = Math.max(1, ...sessions.map((s) => s.round || 1));
  return { summary: fin, summary1: s1, n_rounds: nr, n_retry: fin.X + fin.U, graded_days: gradedDays(marks, sessions) };
}
// 어느 차에서든 그 차 결과가 X였던 문항(2차에서 고쳤어도 그 채점에서 한 번 틀린 것).
// 차 결과 = 그 차의 마지막 기록 — X를 잘못 눌렀다가 고친 것 · 앞 차 결과를 고친 것은 고친 결과로 본다.
export function everWrong(marks, sessions = []) {
  const out = new Set();
  for (const byRound of roundMarks(marks, sessions).values()) for (const [seq, m] of byRound) if (m.result === "X") out.add(seq);
  return out;
}
// 이번 차(round)보다 앞 차까지의 결과 — 기록이 있는 가장 늦은 앞 차의 결과(없으면 "")
export function resultBefore(rounds, round) {
  const prev = (rounds || []).filter((x) => x.round < round && x.result).sort((a, b) => a.round - b.round);
  return prev.length ? prev[prev.length - 1].result : "";
}

const CIRCLED = { "①": "1", "②": "2", "③": "3", "④": "4", "⑤": "5", "⑥": "6", "⑦": "7", "⑧": "8", "⑨": "9", "⑩": "10" };
export function normAns(s) {
  s = String(s || "").trim();
  for (const [k, v] of Object.entries(CIRCLED)) s = s.split(k).join(v);
  s = s.replace(/−/g, "-").replace(/–/g, "-").replace(/，/g, ",").replace(/÷/g, "/");
  s = s.replace(/\[\[\s*-?frac\((\d+)\s*,\s*(\d+)\)\s*\]\]/g, (_, a, b) => `${a}/${b}`);
  s = s.replace(/\s+/g, "");
  s = s.replace(/(가지|개|명|번|장|cm|m|kg|g|L|원|초|분|시간|일|쪽|점|배|도|°|%)$/, "");
  return s.toLowerCase();
}
function frac(s) {
  const m = /^(-?\d+)(?:\/(-?\d+))?$/.exec(s) || /^(-?\d*\.\d+)$/.exec(s);
  if (!m) return null;
  if (m[2] !== undefined && m[2] !== null && s.includes("/")) return Number(m[1]) / Number(m[2]);
  return Number(s);
}
export function autoJudge(key, given) {
  if (!String(key || "").trim() || !String(given || "").trim()) return "";
  const k = normAns(key), g = normAns(given);
  if (k === g) return "O";
  if (k.includes(",")) {
    const a = k.split(/[,/]|또는/).filter(Boolean).sort(), b = g.split(",").filter(Boolean).sort();
    if (a.length === b.length && a.every((x, i) => x === b[i])) return "O";
  }
  const fk = frac(k), fg = frac(g);
  if (fk !== null && fg !== null && Number.isFinite(fk) && Math.abs(fk - fg) < 1e-12) return "O";
  return "X";
}

// ── 자동 채점(OMR 카드) — 단위만 다른 답은 맞다 · 틀리다 정하지 않고 「?」로 돌려 선생님께 묻는다
// judge(정답, 적은 답) → { result: "O" | "X" | "?" | "", why } ("" = 정답이나 답이 비어 못 매김)
const U_ALIAS = [
  [/㎝/g, "cm"], [/㎜/g, "mm"], [/㎞/g, "km"], [/㎏/g, "kg"], [/㎎/g, "mg"], [/㎖/g, "mL"], [/㎗/g, "dL"], [/㎘/g, "kL"], [/ℓ/g, "L"],
  [/㎠/g, "cm²"], [/㎡/g, "m²"], [/㎢/g, "km²"], [/㎟/g, "mm²"], [/㎤/g, "cm³"], [/㎥/g, "m³"], [/℃/g, "°C"],
  [/(cm|mm|km|m)\^?2(?![\d.])/g, "$1²"], [/(cm|mm|km|m)\^?3(?![\d.])/g, "$1³"],
];
const UNIT_LIST = ["cm²", "mm²", "km²", "m²", "cm³", "m³", "°C", "km", "cm", "mm", "kg", "mg", "kL", "mL", "dL", "ml", "dl", "kl", "m", "g", "t", "L", "l", "°", "%",
  "시간", "분", "초", "일", "주", "개월", "달", "년", "원", "개", "명", "번째", "번", "장", "권", "마리", "자루", "송이", "대", "살", "가지", "쪽", "점", "배", "도", "세트",
  "상자", "컵", "병", "봉지", "줄", "칸", "층", "회", "개씩", "씩", "km/h", "m/s", "m/분", "km/시"].sort((a, b) => b.length - a.length);
const U_CANON = { ml: "mL", dl: "dL", kl: "kL", l: "L", 도: "°" };
const U_FAMILY = {
  mm: ["길이", 0.1], cm: ["길이", 1], m: ["길이", 100], km: ["길이", 100000],
  mg: ["무게", 0.001], g: ["무게", 1], kg: ["무게", 1000], t: ["무게", 1000000],
  mL: ["들이", 1], dL: ["들이", 100], L: ["들이", 1000], kL: ["들이", 1000000], "cm³": ["들이", 1], "m³": ["들이", 1000000],
  "mm²": ["넓이", 0.01], "cm²": ["넓이", 1], "m²": ["넓이", 10000], "km²": ["넓이", 1e10],
  초: ["시간", 1], 분: ["시간", 60], 시간: ["시간", 3600], 일: ["시간", 86400],
};
function normJ(s) {
  s = String(s || "").trim();
  for (const [k, v] of Object.entries(CIRCLED)) s = s.split(k).join(v);
  for (const [re, to] of U_ALIAS) s = s.replace(re, to);
  s = s.replace(/−/g, "-").replace(/–/g, "-").replace(/，/g, ",").replace(/÷/g, "/");
  s = s.replace(/\[\[\s*-?frac\((\d+)\s*,\s*(\d+)\)\s*\]\]/g, (_, a, b) => `${a}/${b}`);
  return s.replace(/\s+/g, "");
}
// 끝의 단위 떼기: "12cm" → {v:"12", u:"cm"} (값이 숫자 · 분수 · 소수로 끝날 때만)
export function splitUnit(s) {
  for (const u of UNIT_LIST) {
    if (s.length > u.length && s.endsWith(u)) {
      const v = s.slice(0, -u.length);
      if (/[\d)]$/.test(v)) return { v, u: U_CANON[u] || u };
    }
  }
  return { v: s, u: "" };
}
const numOf = (v) => { const f = frac(v.toLowerCase()); return f !== null && Number.isFinite(f) ? f : null; };
const sameVal = (a, b) => a.toLowerCase() === b.toLowerCase() || (numOf(a) !== null && numOf(b) !== null && Math.abs(numOf(a) - numOf(b)) < 1e-9);
function judgeOne(k, g) {
  if (k.toLowerCase() === g.toLowerCase()) return { result: "O" };
  const a = splitUnit(k), b = splitUnit(g);
  if (sameVal(a.v, b.v)) {
    if (a.u === b.u) return { result: "O" };
    if (!b.u) return { result: "?", why: `단위가 빠졌어요 (정답 ${a.u})` };
    if (!a.u) return { result: "?", why: `정답에 없는 단위를 붙였어요 (${b.u})` };
    return { result: "?", why: `단위가 달라요 (정답 ${a.u} · 적은 답 ${b.u})` };
  }
  const fa = U_FAMILY[a.u], fb = U_FAMILY[b.u];
  if (fa && fb && fa[0] === fb[0] && a.u !== b.u && numOf(a.v) !== null && numOf(b.v) !== null && Math.abs(numOf(a.v) * fa[1] - numOf(b.v) * fb[1]) < 1e-6 * Math.max(1, Math.abs(numOf(a.v) * fa[1])))
    return { result: "?", why: `단위를 바꿔 적었어요 — 값은 같아요 (정답 ${a.u} · 적은 답 ${b.u})` };
  return { result: "X" };
}
export function judge(key, given) {
  if (!String(key || "").trim() || !String(given || "").trim()) return { result: "" };
  const k = normJ(key), g = normJ(given);
  const one = judgeOne(k, g);
  if (one.result !== "X" || !/[,/]|또는/.test(k)) return one;
  // 여러 개 답(「3, 5」): 차례 상관없이 하나하나 맞대기
  const ka = k.split(/,|또는/).filter(Boolean), ga = g.split(",").filter(Boolean);
  if (ka.length < 2 || ka.length !== ga.length) return one;
  const left = [...ga];
  let unit = null;
  for (const x of ka) {
    let hit = left.findIndex((y) => judgeOne(x, y).result === "O");
    if (hit < 0) { hit = left.findIndex((y) => judgeOne(x, y).result === "?"); if (hit >= 0) unit = unit || judgeOne(x, left[hit]).why; }
    if (hit < 0) return one;
    left.splice(hit, 1);
  }
  return unit ? { result: "?", why: unit } : { result: "O" };
}

export const LEVELS = ["초등", "중등", "고등"];
// 프린트 양식 [값, 보이는 이름] — 「초등 크리스마스」는 초등 양식 + 장식(전구 줄·도장 화환·아래 눈밭 띠)
export const TEMPLATES = [["문정중", "문정중 (중등)"], ["초등", "초등 (귀여운)"], ["초등 크리스마스", "초등 크리스마스"]];
export function guessLevel(title, sub, template) {
  const t = `${title} ${sub}`;
  if (String(template || "").startsWith("초등") || /초\s*[1-6]|초등/.test(t)) return "초등";
  if (/고\s*[1-3]|고등|수학\s*[ⅠⅡ]|미적분|기하|확률과\s*통계/.test(t)) return "고등";
  return "중등";
}

export function safeName(s, n = 60) {
  return String(s || "").replace(/[\\/:*?"<>|\r\n\t]+/g, " ").replace(/\s+/g, " ").trim().slice(0, n) || "이름없음";
}

// 퍼센트로 깨진 이름(매쓰플랫 %EC%9C…) 풀기 — PC clean_name 과 같음
export function cleanName(name) {
  let s = String(name || "");
  for (let i = 0; i < 3 && /%[0-9A-Fa-f]{2}/.test(s); i++) {
    try { s = decodeURIComponent(s); } catch { break; }
  }
  if (!/\s/.test(s) && (String(name).match(/%[0-9A-Fa-f]{2}/g) || []).length >= 2) s = s.replace(/\+/g, " ");
  return s.normalize("NFC").replace(/\s+/g, " ").trim();
}

// 학생 이름 빼기 (제목·파일 이름에서) — PC anon.strip_names
export function stripNames(text, names) {
  let t = String(text || "");
  for (const n of [...new Set([...(names || [])].filter((x) => x && String(x).length >= 2))].sort((a, b) => b.length - a.length)) t = t.split(n).join(" ");
  t = t.replace(/\s*[_\-]\s*(?=[_\-])/g, "").replace(/^[\s_\-·,]+|[\s_\-·,]+$/g, "").replace(/\(\s*\)|\[\s*\]/g, "");
  return t.replace(/\s{2,}/g, " ").trim();
}

// ── 날짜 — 이 기기 시간대의 날(YYYY-MM-DD) · 두 날 사이 일수
export function localDay(iso) {
  if (!iso) return null;
  const d = new Date(iso);
  if (isNaN(d)) return null;
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}
export const daysBetween = (a, b) => Math.round((Date.parse(b + "T00:00:00Z") - Date.parse(a + "T00:00:00Z")) / 86400000);

// 채점한 날 — 차마다 그 차 기록(매긴 것)을 넣은 날. 문제를 푼 날이 아니라 매긴 날(처음 · 마지막).
export function gradedDays(marks, sessions) {
  const rs = roundOfSession(sessions);
  const by = new Map();
  for (const m of effectiveMarks(marks, sessions)) {
    const d = localDay(m.at);
    if (!d) continue;
    const r = rs.get(m.session_no) || 1;
    if (!by.has(r)) by.set(r, new Set());
    by.get(r).add(d);
  }
  return [...by.keys()].sort((a, b) => a - b).map((r) => {
    const ds = [...by.get(r)].sort();
    return { round: r, first: ds[0], last: ds[ds.length - 1], n_days: ds.length };
  });
}

// ── 교재 쪽 — "12-20, 25" ↔ [[12, 20], [25, 25]] (쪽 · p · ~ · 띄어쓰기도 받음). 알아볼 수 없으면 null
export function mergeRanges(rs) {
  const s = (rs || []).filter(Boolean).map(([a, b]) => [Math.min(a, b), Math.max(a, b)]).sort((x, y) => x[0] - y[0] || x[1] - y[1]);
  const out = [];
  for (const r of s) {
    const l = out[out.length - 1];
    if (l && r[0] <= l[1] + 1) l[1] = Math.max(l[1], r[1]);
    else out.push([...r]);
  }
  return out;
}
const pageText = (s) => String(s ?? "").replace(/까지|부터|쪽|[pP]\.?/g, " ").replace(/[～〜~–—]/g, "-").replace(/\s*-\s*/g, "-").trim();
export function parsePages(s) {
  const t = pageText(s);
  if (!t) return [];
  const out = [];
  for (const part of t.split(/[,，\s]+/)) {
    if (!part) continue;
    const m = /^(\d{1,4})(?:-(\d{1,4}))?$/.exec(part);
    if (!m) return null;
    out.push([+m[1], m[2] ? +m[2] : +m[1]]);
  }
  return mergeRanges(out);
}
export const fmtPages = (rs) => (rs || []).map(([a, b]) => (a === b ? String(a) : `${a}-${b}`)).join(", ");
export function subtractRanges(a, b) {
  const cut = mergeRanges(b), out = [];
  for (const [s, e] of mergeRanges(a)) {
    let cur = s;
    for (const [bs, be] of cut) {
      if (be < cur || bs > e) continue;
      if (bs > cur) out.push([cur, bs - 1]);
      cur = Math.max(cur, be + 1);
      if (cur > e) break;
    }
    if (cur <= e) out.push([cur, e]);
  }
  return out;
}
// 진도 칸: "45" = 45쪽까지, "30-45" = 30쪽부터 45쪽까지 → { to, pages } · 비면 { empty } · 알아볼 수 없으면 null
export function parseProgress(s) {
  const t = pageText(s);
  if (!t) return { empty: true };
  let m = /^(\d{1,4})$/.exec(t);
  if (m) return { to: +m[1], pages: "" };
  m = /^(\d{1,4})-(\d{1,4})$/.exec(t);
  if (m) { const a = Math.min(+m[1], +m[2]), b = Math.max(+m[1], +m[2]); return { to: b, pages: `${a}-${b}` }; }
  return null;
}
// 푼 쪽 중 채점 기록이 없는 쪽(적은 기록으로 어림) — solved: 날짜 차례 [{page_to, pages}], graded: [{pages}]
// 푼 범위 = 적은 범위(30-45), 없으면 앞 진도 다음 쪽 ~ 이번 쪽. 첫 진도의 시작 쪽을 모르면 채점 기록의 첫 쪽부터 본다.
// 채점 쪽 기록이 하나도 없으면 { known: false } (어림하지 않음)
export function uncheckedPages(solved, graded) {
  const g = mergeRanges((graded || []).flatMap((l) => parsePages(l.pages) || []));
  if (!g.length) return { known: false, ranges: [], text: "" };
  const done = [];
  let prev = null;
  for (const l of solved || []) {
    if (l.page_to == null) continue;
    const r = parsePages(l.pages);
    if (r && r.length) done.push(...r);
    else if (prev != null) { if (l.page_to > prev) done.push([prev + 1, l.page_to]); }
    else if (g[0][0] <= l.page_to) done.push([g[0][0], l.page_to]);
    prev = Math.max(prev ?? 0, l.page_to);
  }
  const left = subtractRanges(done, g);
  return { known: true, ranges: left, text: fmtPages(left) };
}

// ── 재원 · 원비 — 달은 그달 1일(YYYY-MM-01)로 적는다
export const monthStart = (d) => String(d || todayStr()).slice(0, 7) + "-01";
export function addMonths(m, k) {
  const [y, mo] = String(m).split("-").map(Number);
  const t = new Date(Date.UTC(y, mo - 1 + k, 1));
  return `${t.getUTCFullYear()}-${String(t.getUTCMonth() + 1).padStart(2, "0")}-01`;
}
export const monthLabel = (m) => `${+String(m).slice(5, 7)}월`;
// 원비 칸: 「300000」 · 「300,000」 · 「30만」 · 「35.5만」 · 「30만 5천」 → 원. 비면 null, 못 읽으면 NaN
export function parseFee(s) {
  const t = String(s ?? "").replace(/[\s,원₩]/g, "");
  if (!t) return null;
  let m = /^(\d+)$/.exec(t);
  if (m) return +m[1];
  m = /^(\d+(?:\.\d+)?)만(?:(\d+(?:\.\d+)?)천)?$/.exec(t);
  if (m) return Math.round(+m[1] * 10000 + (m[2] ? +m[2] * 1000 : 0));
  m = /^(\d+(?:\.\d+)?)천$/.exec(t);
  if (m) return Math.round(+m[1] * 1000);
  return NaN;
}
export const fmtWon = (n) => (n == null ? "" : `${Number(n).toLocaleString("ko-KR")}원`);
export function fmtMan(n) {          // 300000 → 「30만」, 355000 → 「35만 5천」, 12345 → 「12,345원」
  if (n == null) return "";
  if (n % 1000 !== 0) return fmtWon(n);
  const man = Math.floor(n / 10000), cheon = (n % 10000) / 1000;
  return man ? `${man}만${cheon ? ` ${cheon}천` : ""}` : `${cheon}천`;
}
// 재원 표시 — 이번 달을 적었으면 그 상태.
// 안 적었으면 노랑(y: 지난달은 적었거나 처음) · 빨강(r: 지난달도 비었음). 그만둠으로 끝났거나, 기록 없이 쉬는 중인 옛 학생은 묻지 않는다.
export function monthFlag(st, rows, cur) {
  const mine = rows.filter((r) => r.student_id === st.id && r.month <= cur).sort((a, b) => a.month.localeCompare(b.month));
  const now = mine.find((r) => r.month === cur) || null;
  const last = mine.length ? mine[mine.length - 1] : null;
  if (now) return { status: now.status, fee: now.fee ?? null, note: now.note || "", flag: "", last: now };
  if (last && last.status === "quit") return { status: null, flag: "", quit: true, last };
  if (!last && st.active === false) return { status: null, flag: "", last: null };
  const prev = mine.find((r) => r.month === addMonths(cur, -1));
  return { status: null, flag: !last || prev ? "y" : "r", last };
}
// 달마다 모아 보기 — 다님 · 휴원 · 그만둠 수, 매출(다님 원비 합), 원비 안 적은 다님 수
export function monthTotals(rows, m) {
  const r = rows.filter((x) => x.month === m);
  const at = r.filter((x) => x.status === "attend");
  return { month: m, attend: at.length, pause: r.filter((x) => x.status === "pause").length, quit: r.filter((x) => x.status === "quit").length,
    revenue: at.reduce((a, x) => a + (x.fee || 0), 0), no_fee: at.filter((x) => x.fee == null).length, entered: r.length };
}

// ── 원비표 — 학생 학년 글자(「초4」 · 「중2」 · 「고등학교 1학년」 …)를 「초4」 꼴로. 알아볼 수 없으면 null
export function gradeKey(g) {
  const t = String(g || "").replace(/\s+/g, "");
  const m = /^(초등학교|초등|초)([1-6])(학년)?$/.exec(t) || /^(중학교|중등|중)([1-3])(학년)?$/.exec(t) || /^(고등학교|고등|고)([1-3])(학년)?$/.exec(t);
  if (!m) return null;
  return `${m[1][0]}${m[2]}`;
}
// 그달에 쓰는 원비표 = 그달까지 시작한 원비표 중 가장 늦은 것(그 원비표 안에서만 찾음 — 없는 학년은 그때 받지 않은 것)
export function planStart(plans, month) {
  const starts = [...new Set((plans || []).map((p) => p.start_month))].filter((s) => s <= month).sort();
  return starts.length ? starts[starts.length - 1] : null;
}
export function feeFor(plans, month, gk, perWeek) {
  const st = planStart(plans, month);
  if (!st || !gk || !perWeek) return null;
  const p = (plans || []).find((x) => x.start_month === st && Number(x.per_week) === Number(perWeek) && (x.grades || []).includes(gk));
  return p ? { fee: p.fee, level: p.level, minutes: p.minutes ?? null, start_month: p.start_month } : null;
}

// 원비표의 학년 칸 — 「초1-4」 · 「초5,6」 · 「중등」(= 중1-3) · 「고1 고2」 → ["초1", …]. 못 읽으면 null
const G_MAX = { 초: 6, 중: 3, 고: 3 }, G_ORDER = ["초", "중", "고"];
export function parseGrades(s) {
  const t = String(s || "").replace(/학년|과정|부/g, "").replace(/초등학교|초등/g, "초").replace(/중학교|중등/g, "중").replace(/고등학교|고등/g, "고");
  const out = new Set();
  let pre = null, used = true, m;
  const flush = () => { if (pre && !used) for (let i = 1; i <= G_MAX[pre]; i++) out.add(pre + i); };
  const re = /([초중고])|(\d)\s*[-~∼〜]\s*(\d)|(\d)|([\s,·/、]+)|(.)/g;
  while ((m = re.exec(t))) {
    if (m[1]) { flush(); pre = m[1]; used = false; }
    else if (m[2]) { const a = +m[2], b = +m[3]; if (!pre || a < 1 || b > G_MAX[pre] || a > b) return null; for (let i = a; i <= b; i++) out.add(pre + i); used = true; }
    else if (m[4]) { const a = +m[4]; if (!pre || a < 1 || a > G_MAX[pre]) return null; out.add(pre + a); used = true; }
    else if (m[5]) continue;
    else return null;
  }
  flush();
  if (!out.size) return null;
  return [...out].sort((a, b) => G_ORDER.indexOf(a[0]) - G_ORDER.indexOf(b[0]) || a.slice(1) - b.slice(1));
}
export function fmtGrades(gs) {           // ["초1", "초2", "초3", "초4"] → 「초1-4」
  const by = {};
  for (const g of gs || []) (by[g[0]] = by[g[0]] || []).push(+g.slice(1));
  return G_ORDER.filter((p) => by[p]).map((p) => {
    const ns = [...new Set(by[p])].sort((a, b) => a - b), parts = [];
    for (let i = 0; i < ns.length; ) { let j = i; while (j + 1 < ns.length && ns[j + 1] === ns[j] + 1) j++; parts.push(i === j ? `${ns[i]}` : `${ns[i]}-${ns[j]}`); i = j + 1; }
    return p + parts.join(",");
  }).join(" ");
}
// 그달 고를 수 있는 주당 횟수 — 그달 원비표에 있는 것(없으면 주2 · 주3), 이미 적힌 값은 늘 보임
export function perWeekOpts(plans, month, extra) {
  const st = planStart(plans, month);
  const s = new Set((plans || []).filter((p) => p.start_month === st).map((p) => Number(p.per_week)));
  if (!s.size) { s.add(2); s.add(3); }
  for (const e of [].concat(extra ?? [])) if (e) s.add(Number(e));
  return [...s].sort((a, b) => a - b);
}
// 그달 원비 채우기 — 원비표(학년 · 주당 횟수) 값. 다만 지난달에 원비표와 다른 원비(할인 등)를 같은 주당 횟수로 냈으면
// 지난달 원비를 그대로 두고 special. 원비표에서 못 찾으면 지난달 원비. 원비표가 바뀐 달(1월 등)에는 원비표대로 낸 학생만 새 원비로.
export function suggestFee(plans, month, gk, perWeek, prev) {
  const plan = perWeek ? feeFor(plans, month, gk, perWeek) : null;
  const pf = prev && prev.status === "attend" && prev.fee != null ? prev.fee : null;
  const samePw = pf != null && (prev.per_week == null || !perWeek || Number(prev.per_week) === Number(perWeek));
  if (samePw) {
    const was = feeFor(plans, addMonths(month, -1), gk, prev.per_week || perWeek);
    if (!plan) return { fee: pf, src: "prev", plan: null };
    if (was && pf !== was.fee) return { fee: pf, src: "prev", plan, special: true };
  }
  return plan ? { fee: plan.fee, src: "plan", plan } : null;
}
