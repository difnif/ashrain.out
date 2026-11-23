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
export function currentMarks(marks, sessions) {
  const rs = roundOfSession(sessions);
  const out = new Map();
  for (const m of [...marks].sort((a, b) => a.id - b.id)) out.set(m.seq, { ...m, round: rs.get(m.session_no) || 1 });
  return out;
}
export function roundMarks(marks, sessions) {
  const rs = roundOfSession(sessions);
  const out = new Map(); // round → Map(seq → mark)
  for (const m of [...marks].sort((a, b) => a.id - b.id)) {
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
// 어느 차에서든 X였던 문항(2차에서 고쳤어도 그 채점에서 한 번 틀린 것)
export function everWrong(marks) {
  return new Set(marks.filter((m) => m.result === "X").map((m) => m.seq));
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

export const LEVELS = ["초등", "중등", "고등"];
export function guessLevel(title, sub, template) {
  const t = `${title} ${sub}`;
  if (template === "초등" || /초\s*[1-6]|초등/.test(t)) return "초등";
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
