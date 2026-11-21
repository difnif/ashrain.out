// ashrain.out — 우물 맞춤 추천에 쓸 학생 기록 읽기 (Supabase · localStorage) — lib/recommend.js 의 profile 을 만든다
// 로그인했으면 최근 180일 풀이(attempts, 1000개까지) → 문항(test_items)의 개념 → 단원(chapters.js)으로 숙달도를 모으고,
// 기기 안의 시청각 본 기록(lib/avHistory.js)을 붙인다. 하나라도 실패하면 있는 것만으로(없으면 기본 추천).
// 한 번 읽은 것은 10분 동안 다시 쓴다.
import { supabase } from "../supabaseClient";
import { recentAttempts, fetchItemsByIds } from "./items";
import { listConcepts } from "./concepts";
import { masteryFrom } from "./recommend";
import { readHist } from "./avHistory";

let memo = null;
const TTL = 10 * 60 * 1000;

export async function loadProfile({ force = false } = {}) {
  if (!force && memo && Date.now() - memo.at < TTL) return { ...memo.p, watched: readHist() };
  let mastery = {};
  try {
    const { data } = await supabase.auth.getSession();
    const uid = data?.session?.user?.id;
    if (uid) {
      const att = await recentAttempts(uid, { days: 180, limit: 1000 });
      if (att.length) {
        const ids = [...new Set(att.map((a) => a.item_id).filter(Boolean))];
        const [items, concepts] = await Promise.all([fetchItemsByIds(ids), listConcepts()]);
        mastery = masteryFrom(att, new Map(items.map((i) => [i.id, i])), new Map(concepts.map((c) => [c.id, c])));
      }
    }
  } catch { /* 기록을 못 읽으면 본 기록만 */ }
  memo = { at: Date.now(), p: { mastery } };
  return { mastery, watched: readHist() };
}
