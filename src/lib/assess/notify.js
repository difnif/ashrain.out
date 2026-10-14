// ashrain.out — 서술형 평가 알림(앱 안): 열린 평가 목록을 잠깐 캐시하고, 새로 열린 평가는 한 번 토스트로 알린다.
// 진짜 푸시 알림은 아직 없다(마이페이지 '알림 받기'는 준비 중) — 앱을 열면 대시보드 카드·우물·토스트로 보인다.
import { assessCall, deviceId, seenCodes, claimPending } from "./api.js";

const TTL = 2 * 60 * 1000;
const TOAST_KEY = "ash.assess.toasted";
let cache = null, at = 0, inflight = null, claimed = false;

/** { open:[{code,title,date,…}], mine:[{sid,code,status,total,max}] } — 실패하면 빈 목록 */
export async function assessList({ force = false } = {}) {
  if (!force && cache && Date.now() - at < TTL) return cache;
  if (inflight) return inflight;
  inflight = (async () => {
    try {
      if (!claimed) { claimed = true; await claimPending().catch(() => 0); }
      const r = await assessCall("list", { device: deviceId() });
      cache = { open: r.open || [], mine: r.mine || [], ready: r.ready !== false };
    } catch {
      cache = cache || { open: [], mine: [], ready: false };
    }
    at = Date.now();
    inflight = null;
    return cache;
  })();
  return inflight;
}
export const invalidateAssessList = () => { cache = null; at = 0; };

/** 아직 제출하지 않은 열린 평가 */
export function pendingSets(list) {
  if (!list) return [];
  const done = new Set((list.mine || []).filter((m) => m.status === "submitted").map((m) => m.code));
  return (list.open || []).filter((s) => !done.has(s.code));
}
export const isNew = (code) => !seenCodes().has(code);

/** 새로 열린 평가를 한 번만 토스트로 (셸의 ash:job-toast — 누르면 그 평가로) */
export function toastNewSets(list) {
  let done;
  try { done = new Set(JSON.parse(localStorage.getItem(TOAST_KEY) || "[]")); } catch { done = new Set(); }
  const fresh = pendingSets(list).filter((s) => !done.has(s.code) && isNew(s.code));
  if (!fresh.length) return;
  const s = fresh[0];
  try {
    window.dispatchEvent(new CustomEvent("ash:job-toast", { detail: {
      title: "📝 새 서술형 평가가 열렸어요",
      body: `${s.title}${fresh.length > 1 ? ` 외 ${fresh.length - 1}개` : ""} — 눌러서 열기`,
      to: `/e/${s.code}`,
    } }));
  } catch { /* */ }
  for (const x of fresh) done.add(x.code);
  try { localStorage.setItem(TOAST_KEY, JSON.stringify([...done].slice(-200))); } catch { /* */ }
}
