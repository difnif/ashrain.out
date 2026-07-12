import { supabase } from "../supabaseClient";

export async function listConcepts() {
  const { data, error } = await supabase
    .from("concepts")
    .select("id, unit_id, title, subtitle, sort_order")
    .order("unit_id").order("sort_order");
  if (error) throw error;
  return data;
}

export async function getConcept(id) {
  const { data, error } = await supabase.from("concepts").select("*").eq("id", id).single();
  if (error) throw error;
  return data;
}

export async function getAdoptedQna(conceptId) {
  const { data, error } = await supabase
    .from("concept_qna")
    .select("id, block_id, question, answer")
    .eq("concept_id", conceptId).eq("status", "adopted")
    .order("created_at");
  if (error) throw error;
  return data;
}

// 학생 질문 접수 (pending으로 저장 → 관리자 채택 시 화면에 노출)
export async function askQuestion(conceptId, blockId, question) {
  const { data: { user } } = await supabase.auth.getUser();
  const { error } = await supabase.from("concept_qna").insert({
    concept_id: conceptId, block_id: blockId, question, asked_by: user?.id,
  });
  if (error) throw error;
}

// (관리자) 채택/폐기/답변 — 관리자 화면에서 사용
export async function reviewQna(id, patch) {
  const { error } = await supabase.from("concept_qna").update(patch).eq("id", id);
  if (error) throw error;
}

// (관리자) 블록 수정 — "대화형 패치"의 저장 지점
export async function updateBlocks(conceptId, blocks) {
  const { error } = await supabase.from("concepts")
    .update({ blocks, updated_at: new Date().toISOString() }).eq("id", conceptId);
  if (error) throw error;
}
