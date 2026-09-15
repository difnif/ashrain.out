// ashrain.out — 오답노트 생성 (문항형)
// 기존 wrong_notes 는 사진 기반(image_path NOT NULL)이다. 문항형 노트는 DDL 없이 쓰기 위해
// image_path 에 "item:<test_items.id>" 센티널을 넣고, 본문은 memo 에 요약해 둔다.
// WrongNote 화면은 isItemNote() 로 구분해 문항을 다시 불러 렌더한다.

import { supabase } from "../supabaseClient";
import { reasonForMc } from "./misconceptions";
import { displayAnswer } from "./answers";

export const ITEM_PREFIX = "item:";
export const isItemNote = (n) => typeof n?.image_path === "string" && n.image_path.startsWith(ITEM_PREFIX);
export const itemIdOf = (n) => (isItemNote(n) ? n.image_path.slice(ITEM_PREFIX.length) : null);

/** 이미 있는(정리되지 않은) 문항형 노트의 item id 집합 */
export async function existingItemNoteIds(uid) {
  const { data, error } = await supabase.from("wrong_notes").select("image_path, status")
    .eq("user_id", uid).like("image_path", `${ITEM_PREFIX}%`).neq("status", "cleared");
  if (error) return new Set();
  return new Set((data || []).map(itemIdOf));
}

/**
 * 틀린 문항들을 오답노트로 저장. entries: [{ item, myAnswer, tag }]
 * 같은 문항의 미정리 노트가 이미 있으면 건너뛴다. 반환 { added, skipped, error }
 */
export async function saveItemWrongNotes({ uid, entries, source = "문제풀이" }) {
  const list = (entries || []).filter((e) => e?.item?.id);
  if (!uid || !list.length) return { added: 0, skipped: 0, error: null };
  const have = await existingItemNoteIds(uid);
  const rows = [];
  const seen = new Set();
  for (const e of list) {
    const id = e.item.id;
    if (have.has(id) || seen.has(id)) continue;
    seen.add(id);
    const tag = e.tag || null;
    rows.push({
      user_id: uid,
      image_path: ITEM_PREFIX + id,
      unit_id: e.item.unit_id || null,
      concept_id: e.item.concept_ids?.[0] || null,
      reason: reasonForMc(tag),
      source,
      tags: ["문항", ...(tag ? [tag] : [])],
      status: "new",
      memo: `내 답: ${e.myAnswer ? displayAnswer(e.myAnswer) : "(무응답)"} · 정답: ${displayAnswer(e.item.answer)}`,
    });
  }
  if (!rows.length) return { added: 0, skipped: list.length, error: null };
  const { error } = await supabase.from("wrong_notes").insert(rows);
  return { added: error ? 0 : rows.length, skipped: list.length - rows.length, error: error || null };
}

/** 내 오답노트 개수 (미정리) */
export async function countOpenWrongNotes(uid) {
  const { count, error } = await supabase.from("wrong_notes").select("id", { count: "exact", head: true })
    .eq("user_id", uid).neq("status", "cleared");
  return error ? 0 : (count || 0);
}
