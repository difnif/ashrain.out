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
  return [...out.keys()].sort((a, b) => a - b).map((r) => {
    const o = out.get(r);
    const tg = o.targets !== null ? o.targets : seqs;
    const ms = rm.get(r) || new Map();
    o.summary = summarize(tg.map((s) => ({ mark: ms.get(s) })));
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
  return { summary: fin, summary1: s1, n_rounds: nr, n_retry: fin.X + fin.U };
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
