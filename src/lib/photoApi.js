// ashrain.out — 촬영 모듈 서버 호출 (/api/photo). 로그인 토큰을 붙여 POST, 오류는 메시지로 던진다.
//   scan     { image, mode:'problem'|'answer'|'page', hint? }      → 전사 결과 (+ 문항이면 표준성 등급)
//   approach { question, figure_note, choices }                     → 식 세우기까지의 방침 (정답 없음)
//   essay    { question, figure_note, answer, std }                 → 채점·첨삭 + 보관 결정
//   process  { question, figure_note, answer, lines, legibility, std } → 풀이과정 검사 + 보관 결정
import { supabase } from "../supabaseClient";

export async function photoCall(task, body = {}) {
  const { data: sess } = await supabase.auth.getSession();
  const token = sess?.session?.access_token;
  if (!token) throw new Error("세션이 만료됐어요 — 다시 로그인해 주세요");
  const r = await fetch("/api/photo", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
    body: JSON.stringify({ task, ...body }),
  });
  let j = null;
  try { j = await r.json(); } catch { /* 본문 없음 */ }
  if (!r.ok) throw new Error(j?.error || `요청 실패 (${r.status})`);
  return j;
}

/** 여러 화면이 같은 촬영 결과를 이어 쓰도록 세션 저장소에 둔다 (탭 닫으면 사라짐) */
const KEY = "ash.photo.current";
export function stashCurrent(obj) {
  try { sessionStorage.setItem(KEY, JSON.stringify(obj)); }
  catch { try { sessionStorage.removeItem(KEY); } catch { /* */ } }   // 용량 초과면 이전 문제가 남지 않게 비운다 → 화면은 촬영 단계로
}
export function readCurrent() { try { const r = sessionStorage.getItem(KEY); return r ? JSON.parse(r) : null; } catch { return null; } }
export function clearCurrent() { try { sessionStorage.removeItem(KEY); } catch { /* */ } }
