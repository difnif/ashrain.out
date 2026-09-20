// ashrain.out — 기기 보관소 (IndexedDB). 촬영 모듈의 답안 원문·첨삭 결과는 기본적으로 여기(학생 기기)에만 둔다.
// 서버에는 라벨만 간다 (src/lib/retention.js). IndexedDB 가 없으면 localStorage 로 조용히 대체한다.
//   레코드: { id, feature('read'|'mark'|'essay'|'check'), at(ISO), title, unit, grade, question, figure_note, answer, result, retention }
const DB = "ash.photo", STORE = "sessions", VER = 1, LS_KEY = "ash.photo.sessions", MAX_LS = 60;

function openDb() {
  return new Promise((resolve, reject) => {
    if (typeof indexedDB === "undefined") { resolve(null); return; }
    const req = indexedDB.open(DB, VER);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) {
        const st = db.createObjectStore(STORE, { keyPath: "id" });
        st.createIndex("at", "at"); st.createIndex("feature", "feature");
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => resolve(null);    // 사생활 모드 등 — localStorage 로 대체
    req.onblocked = () => resolve(null);
  });
}
function tx(db, mode, fn) {
  return new Promise((resolve, reject) => {
    try {
      const t = db.transaction(STORE, mode); const st = t.objectStore(STORE);
      const out = fn(st);
      t.oncomplete = () => resolve(out?.result ?? out);
      t.onerror = () => reject(t.error);
      t.onabort = () => reject(t.error || new Error("aborted"));
    } catch (e) { reject(e); }
  });
}
/** IndexedDB 가 열리긴 했는데 트랜잭션이 실패하면(저장 공간 부족·손상) null → 호출자는 localStorage 로 간다 */
async function withDb(mode, fn) {
  const db = await openDb();
  if (!db) return { ok: false };
  try { const r = await tx(db, mode, fn); return { ok: true, r }; }
  catch { return { ok: false }; }
  finally { try { db.close(); } catch { /* */ } }
}
const lsRead = () => { try { const a = JSON.parse(localStorage.getItem(LS_KEY) || "[]"); return Array.isArray(a) ? a : []; } catch { return []; } };
const lsWrite = (a) => { try { localStorage.setItem(LS_KEY, JSON.stringify(a.slice(0, MAX_LS))); } catch { /* 용량 초과면 포기 */ } };

export const newId = () => (typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2));

/** 저장(같은 id 면 덮어씀) → id */
export async function putSession(rec) {
  const row = { ...rec, id: rec.id || newId(), at: rec.at || new Date().toISOString() };
  const { ok } = await withDb("readwrite", (st) => st.put(row));
  if (!ok) lsWrite([row, ...lsRead().filter((r) => r.id !== row.id)]);
  return row.id;
}
/** 최근순 목록 (feature 로 거름, 본문은 그대로 — 기기 안이므로) */
export async function listSessions({ feature, limit = 50 } = {}) {
  const { ok, r } = await withDb("readonly", (st) => st.getAll());
  let rows = ok ? r : lsRead();
  rows = (rows || []).filter((r) => !feature || r.feature === feature);
  rows.sort((a, b) => String(b.at).localeCompare(String(a.at)));
  return rows.slice(0, limit);
}
export async function getSession(id) {
  const { ok, r } = await withDb("readonly", (st) => st.get(id));
  if (ok) return r || null;
  return lsRead().find((x) => x.id === id) || null;
}
export async function deleteSession(id) {
  const { ok } = await withDb("readwrite", (st) => st.delete(id));
  if (!ok) lsWrite(lsRead().filter((r) => r.id !== id));
}
export async function clearSessions() {
  const { ok } = await withDb("readwrite", (st) => st.clear());
  if (!ok) lsWrite([]);
}
