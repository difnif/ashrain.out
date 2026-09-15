// 문항에 대해 질문하기 — 문항 요약을 세션에 두고 #/solve/ask/<id> 로 이동한다 (App.jsx 가 QuestionChat 을 연다)
// 정답·해설은 절대 넘기지 않는다 (AI 가 답을 흘리지 않게).
export const ASK_KEY = "ash.askItem";

export function askAboutItem(item) {
  if (!item?.id) return;
  const payload = {
    id: item.id,
    concept_id: item.concept_ids?.[0] || null,
    unit_id: item.unit_id || null,
    question: item.question,
    choices: Array.isArray(item.choices) ? item.choices : null,
    qtype: item.qtype,
  };
  try { sessionStorage.setItem(ASK_KEY, JSON.stringify(payload)); } catch {}
  location.hash = `#/solve/ask/${item.id}`;
}

export function readAskItem(id) {
  try {
    const raw = sessionStorage.getItem(ASK_KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    return !id || p.id === id ? p : null;
  } catch { return null; }
}
