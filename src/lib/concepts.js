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

// (관리자) 개념 일괄 등록/수정 — JSON 붙여넣기 임포트용
export async function upsertConcepts(list) {
  const rows = list.map((c) => ({
    id: c.id, unit_id: c.unitId ?? c.unit_id, title: c.title, subtitle: c.subtitle ?? null,
    sort_order: c.order ?? c.sort_order ?? 0, blocks: c.blocks ?? [], cover: c.cover ?? null,
    updated_at: new Date().toISOString(),
  }));
  const { error } = await supabase.from("concepts").upsert(rows);
  if (error) throw error;
  // qna 필드가 있으면 채택 QnA도 함께 등록 (id 없는 신규만)
  const qna = list.flatMap((c) => (c.qna || []).map((q) => ({
    concept_id: c.id, block_id: q.anchor ?? q.block_id, question: q.q ?? q.question,
    answer: q.a ?? q.answer, status: q.status ?? "adopted",
  })));
  if (qna.length) {
    const { error: e2 } = await supabase.from("concept_qna").insert(qna);
    if (e2) throw e2;
  }
  return rows.length;
}

// (관리자) 전체 내보내기 — 백업/재편집용
export async function exportConcepts() {
  const { data, error } = await supabase.from("concepts").select("*").order("unit_id").order("sort_order");
  if (error) throw error;
  return data;
}
