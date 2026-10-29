// ashrain.out — 컨셉 문제 「종이처럼 풀기」: 답안 꼴 · 채점 (순수 함수, node 테스트 가능)
//
// 문항별 답(answers[no])
//   { k:"text", raw:"5/12" }               타자
//   { k:"ink", lay, w, h, s, wd }           손글씨(ink.js) — 채점할 때 판독 글자(reads[no])로 판정
//   { k:"pick", sel:["ㄱ","ㄷ"] }           보기 체크 — 중복 허용, 다시 누르면 해제(실수를 막지 않는다)
// 빈칸이 있어도 그냥 제출된다(빈칸 = 틀림으로 센다). 손글씨를 못 읽으면 「확인 필요」로 두고 점수에서 뺀다.
import { judge } from "../../lib/conceptsets.js";
import { hasInk, normalizeRead } from "./ink.js";

export function isAnswered(ans) {
  if (!ans) return false;
  if (ans.k === "text") return String(ans.raw ?? "").trim() !== "";
  if (ans.k === "pick") return Array.isArray(ans.sel) && ans.sel.length > 0;
  if (ans.k === "ink") return hasInk(ans);
  return false;
}

/** 보기 하나 체크/해제 — 보기 차례대로 정렬해 둔다 */
export function togglePick(ans, label, opts = ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]) {
  const cur = new Set(ans?.k === "pick" ? ans.sel : []);
  if (cur.has(label)) cur.delete(label); else cur.add(label);
  const sel = opts.filter((o) => cur.has(o));
  return sel.length ? { k: "pick", sel } : null;
}

/** 채점에 쓸 글자 — 손글씨는 판독 글자(없으면 null = 아직 못 읽음) */
export function rawFor(ans, read) {
  if (!ans) return "";
  if (ans.k === "text") return String(ans.raw ?? "").trim();
  if (ans.k === "pick") return (ans.sel || []).join(", ");
  if (ans.k === "ink") return read == null ? null : normalizeRead(read);
  return "";
}

/**
 * 채점. reads: { [no]: 손글씨 판독 글자 } (판독 실패는 "" 또는 없음)
 * → { rows:[{ no, id, lv, src, raw, status:"ok"|"wrong"|"blank"|"unread", note }], score, n, counts }
 */
export function gradePaper(set, answers = {}, reads = {}) {
  const rows = (set?.items || []).map((it) => {
    const ans = answers[it.no];
    const base = { no: it.no, id: it.id, lv: it.lv, src: ans?.k || null, raw: "", status: "blank", note: "" };
    if (!isAnswered(ans)) return base;
    const raw = rawFor(ans, reads[it.no]);
    if (raw == null || raw === "") return { ...base, status: "unread" };
    const j = judge(it, raw);
    if (j.ok === null) return { ...base, raw, status: raw.includes("?") ? "unread" : "blank", note: j.note };
    return { ...base, raw, status: j.ok ? "ok" : "wrong", note: j.note };
  });
  const counts = { ok: 0, wrong: 0, blank: 0, unread: 0 };
  for (const r of rows) counts[r.status]++;
  return { rows, score: counts.ok, n: rows.length, counts };
}

/** 난이도별 맞힌 수 [[lv, ok, n]] */
export function levelSummary(set, graded, levels = ["하", "중", "상"]) {
  return levels.map((lv) => {
    const xs = graded.rows.filter((r) => r.lv === lv);
    return [lv, xs.filter((r) => r.status === "ok").length, xs.length];
  });
}

/** 답의 짧은 글자(목록 · 해설 시트) */
export function answerLabel(ans, read) {
  if (!isAnswered(ans)) return "";
  if (ans.k === "ink") return read ? normalizeRead(read) : "손글씨";
  return rawFor(ans, read) || "";
}
