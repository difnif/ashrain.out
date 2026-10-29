// ashrain.out — 컨셉 문제 「종이처럼 풀기」: 손글씨 답 읽기
// 손글씨 답들을 번호 붙은 칸에 모은 이미지(ink.inkSheets)로 만들어 기존 AI 판독(/api/ai, task "omr")에 보낸다.
//   서버는 그대로 — 손글씨 답안지 사진을 번호별 답으로 읽는 같은 태스크(학생 하루 무료 한도 · 고유번호 자격도 같다).
//   한 장에 최대 24칸(4열), 많으면 여러 장. 읽지 못한 칸은 빈 글자로 오고, 채점 화면에서 「확인 필요」로 남는다.
import { supabase } from "../../supabaseClient";
import { inkSheets } from "./ink";

/** entries: [{ no, ink }] → { reads: { [no]: 글자 }, error } */
export async function readInkAnswers(entries) {
  if (!entries.length) return { reads: {}, error: null };
  let token = null;
  try { const { data } = await supabase.auth.getSession(); token = data?.session?.access_token || null; } catch { token = null; }
  if (!token) return { reads: {}, error: "로그인이 필요해요 — 손글씨 답은 타자로 확인해 주세요" };
  const reads = {};
  let error = null;
  for (const sh of inkSheets(entries)) {
    let image;
    try { image = sh.canvas.toDataURL("image/jpeg", 0.9).split(",")[1]; } catch { error = "손글씨 이미지를 만들지 못했어요"; break; }
    try {
      const r = await fetch("/api/ai", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
        body: JSON.stringify({ task: "omr", image, items: sh.nos.map((no) => ({ no, type: "short" })) }),
      });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) { error = j.error || `손글씨를 읽지 못했어요 (${r.status})`; break; }
      for (const a of j.answers || []) if (sh.nos.includes(Number(a.no))) reads[Number(a.no)] = String(a.answer ?? "");
    } catch {
      error = "손글씨를 읽으러 가지 못했어요 — 연결을 확인해 주세요"; break;
    }
  }
  return { reads, error };
}
