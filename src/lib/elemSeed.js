// 기본 제공 초등 개념(public/concepts/elem — elemgen/ 생성기) 을 DB(concepts) 에 넣어 둔다.
// · 학생 질문(concept_qna) · 복습(concept_reviews) 이 concepts(id) 를 외래키로 물고 있어 화면만 정적 파일로 보여 줄 수는 없다 — DB 에 있어야 한다.
// · 관리자가 앱을 열면(셸 상단이 역할을 읽은 뒤) 한 번 돈다: DB 에 없는 id 만 새로 넣고, 이미 있는 개념은 건드리지 않는다
//   (관리자가 고친 내용을 지키려고 — 관리 화면 「기본 제공 초등 개념 등록」 단추와 같은 규칙).
// · 이 기기에서 같은 판(index.json 의 v · count)을 이미 맞췄으면 건너뛴다 — 관리자가 일부러 지운 개념이 매번 되살아나지 않게.
//   새 판(개념 추가)이 올라오면 그때 다시 없는 것만 채운다.
import { supabase } from "../supabaseClient";
import { bustStudyCache } from "./studyCache";

const KEY = "ash.elemSeed";
let running = null;

const lsGet = (k) => { try { return localStorage.getItem(k); } catch { return null; } };
const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch { /* 저장 못 해도 다음에 다시 확인할 뿐 */ } };

/** 개념 JSON(elemgen 형식) → concepts 행 */
export function toConceptRow(c, now = new Date().toISOString()) {
  return {
    id: c.id, unit_id: c.unitId ?? c.unit_id, title: c.title, subtitle: c.subtitle ?? null,
    sort_order: c.order ?? c.sort_order ?? 0, blocks: c.blocks ?? [], cover: c.cover ?? null, updated_at: now,
  };
}

/**
 * DB 에 없는 기본 제공 초등 개념을 넣는다.
 * @param {{ force?: boolean }} o  force — 이 기기에서 맞춘 판이어도 다시 확인(관리 화면 단추)
 * @returns {Promise<{ added: number, total: number, skipped?: boolean }>}
 */
export function seedBundledElem({ force = false } = {}) {
  if (running) return running;
  running = (async () => {
    const idx = await fetch("/concepts/elem/index.json", { cache: "no-cache" }).then((r) => (r.ok ? r.json() : null));
    if (!idx?.units?.length) return { added: 0, total: 0 };
    const ver = `${idx.v}:${idx.count}`;
    if (!force && lsGet(KEY) === ver) return { added: 0, total: idx.count, skipped: true };
    const { data, error } = await supabase.from("concepts").select("id").like("id", "e%");
    if (error) throw error;
    const have = new Set((data || []).map((r) => r.id));
    let fresh = [];
    if (have.size < idx.count || force) {
      const packs = await Promise.all(idx.units.map((u) =>
        fetch(`/concepts/elem/${u}.json`, { cache: "no-cache" }).then((r) => (r.ok ? r.json() : []))));
      fresh = packs.flat().filter((c) => c && c.id && !have.has(c.id));
    }
    if (fresh.length) {
      const now = new Date().toISOString();
      const { error: e2 } = await supabase.from("concepts")
        .upsert(fresh.map((c) => toConceptRow(c, now)), { onConflict: "id", ignoreDuplicates: true });
      if (e2) throw e2;
      bustStudyCache();
      try { window.dispatchEvent(new CustomEvent("ash:concepts-changed", { detail: { added: fresh.length } })); } catch { /* */ }
    }
    lsSet(KEY, ver);
    return { added: fresh.length, total: idx.count };
  })().finally(() => { running = null; });
  return running;
}
