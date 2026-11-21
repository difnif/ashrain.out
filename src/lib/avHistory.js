// ashrain.out — 시청각 학습 본 기록 (기기 안 · localStorage) — 순수 도우미
// 기본기 해설(단원 100제 · 주차별 회차)을 열고 몇 번째 문항까지 봤는지 남긴다. 우물 맞춤 추천(lib/recommend.js)과
// 문제 풀이 해설 목록의 ✓ · 「이어 보기」가 읽는다. 서버로 보내지 않는다(학생 기기에만).
//   { [key]: { t: 마지막으로 본 때(ms), v: 연 횟수, max: 가장 멀리 본 문항 번호(1부터), n: 문항 수 } }  · 최근 400개까지만

const KEY = "ash.av.hist";
const CAP = 400;

export function readHist(storage = globalThis.localStorage) {
  try { const v = JSON.parse(storage?.getItem(KEY) || "null"); return v && typeof v === "object" ? v : {}; } catch { return {}; }
}
function write(h, storage) {
  const keys = Object.keys(h);
  if (keys.length > CAP) for (const k of keys.sort((a, b) => (h[a].t || 0) - (h[b].t || 0)).slice(0, keys.length - CAP)) delete h[k];
  try { storage?.setItem(KEY, JSON.stringify(h)); } catch { /* 가득 참 · 막힘 — 무시 */ }
}
/** 열었다 — 연 횟수 +1 */
export function noteOpen(key, n, { now = Date.now(), storage = globalThis.localStorage } = {}) {
  if (!key) return;
  const h = readHist(storage);
  const r = h[key] || { t: 0, v: 0, max: 0, n: n || 0 };
  r.t = now; r.v += 1; if (n) r.n = n;
  h[key] = r;
  write(h, storage);
}
/** 몇 번째 문항(1부터)까지 봤다 */
export function noteSeen(key, no, n, { now = Date.now(), storage = globalThis.localStorage } = {}) {
  if (!key || !no) return;
  const h = readHist(storage);
  const r = h[key] || { t: 0, v: 1, max: 0, n: n || 0 };
  r.t = now; r.max = Math.max(r.max || 0, no); if (n) r.n = n;
  h[key] = r;
  write(h, storage);
}
/** 다 봤나(문항의 80% 이상) */
export const histDone = (r) => !!r && r.n > 0 && r.max >= Math.ceil(r.n * 0.8);
/** 가장 최근에 본 것(키 앞글자로 거를 수 있다 — "w-e3-" 처럼) */
export function lastSeen(h, prefix = "") {
  let best = null;
  for (const [k, r] of Object.entries(h)) if (k.startsWith(prefix) && (!best || r.t > best.r.t)) best = { key: k, r };
  return best;
}
