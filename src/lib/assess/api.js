// ashrain.out — 서술형 평가 서버 호출 (POST /api/photo { task:"assess", op }) + 이 기기의 응시 기록(비밀값) 보관
// 로그인 토큰이 있으면 붙이고, 없으면 그냥 보낸다(QR 비로그인 응시). 비로그인 응시는 sid + secret 으로 이어 간다.
import { supabase } from "../../supabaseClient";

export class AssessError extends Error {
  constructor(msg, status, extra) { super(msg); this.status = status; this.extra = extra || {}; }
}

export async function accessToken() {
  try { const { data } = await supabase.auth.getSession(); return data?.session?.access_token || null; } catch { return null; }
}
/** 지금 로그인한 계정 id (없으면 null) — 이 기기의 응시 기록을 '지금 보는 사람' 것만 쓰려고 */
export async function currentUid() {
  try { const { data } = await supabase.auth.getSession(); return data?.session?.user?.id || null; } catch { return null; }
}

export async function assessCall(op, body = {}, { signal } = {}) {
  const headers = { "content-type": "application/json" };
  const tok = await accessToken();
  if (tok) headers.authorization = `Bearer ${tok}`;
  let r;
  try {
    r = await fetch("/api/photo", { method: "POST", headers, body: JSON.stringify({ task: "assess", op, ...body }), signal });
  } catch (e) {
    if (e?.name === "AbortError") throw new AssessError("취소했어요", 0);
    throw new AssessError("인터넷 연결을 확인해 주세요", 0);
  }
  let j = null;
  try { j = await r.json(); } catch { /* 본문 없음 */ }
  if (!r.ok) throw new AssessError(j?.error || `요청 실패 (${r.status})`, r.status, j || {});
  return j;
}

// ── 이 기기 ─────────────────────────────────────────────────────────────────
const DEV_KEY = "ash.assess.device";
const SESS_KEY = (code) => `ash.assess.s.${code}`;
const CLAIM_KEY = "ash.assess.claims";
const SEEN_KEY = "ash.assess.seen";

const ls = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* 저장 못 해도 흐름은 계속 */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* */ } },
  json(k, def) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch { return def; } },
};

/** 기기 토큰 — 브라우저마다 한 번 만들고 계속 쓴다(서버에는 해시만) */
export function deviceId() {
  let d = ls.get(DEV_KEY);
  if (!d) {
    try { d = crypto.randomUUID(); } catch { d = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`; }
    ls.set(DEV_KEY, d);
  }
  return d;
}

/**
 * 평가별 응시 기록 { sid, secret, at, step, uid } — uid: 만들 때 로그인해 있던 계정(비로그인 null).
 * 같은 기기를 여럿이 쓰면(학원 태블릿) 다른 사람 기록이 섞이지 않게, 읽을 때 지금 보는 사람(uid)과 같은 것만 쓴다.
 */
export const readLocal = (code) => ls.json(SESS_KEY(code), null);
export function readLocalFor(code, uid) {
  const v = readLocal(code);
  return v && (v.uid || null) === (uid || null) ? v : null;
}
export function writeLocal(code, patch) {
  const cur = readLocal(code) || {};
  const next = { ...cur, ...patch, at: Date.now() };
  ls.set(SESS_KEY(code), JSON.stringify(next));
  return next;
}
export const clearLocal = (code) => ls.del(SESS_KEY(code));

/** 이 기기에 남은 비로그인 응시(비로그인 결과 목록용) */
export function localSessions() {
  const out = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k && k.startsWith("ash.assess.s.")) {
        const v = ls.json(k, null);
        if (v?.sid && !v.uid) out.push({ code: k.slice("ash.assess.s.".length), ...v });
      }
    }
  } catch { /* */ }
  return out.sort((a, b) => (b.at || 0) - (a.at || 0));
}

/** 결과 화면에서 '로그인하고 담기'를 누른 응시 — 그 뒤 30분 안에 로그인하면 계정에 담는다(저절로 담지 않는다) */
const CLAIM_TTL = 30 * 60 * 1000;
export function addPendingClaim(sid, secret) {
  const list = ls.json(CLAIM_KEY, []).filter((x) => x.sid !== sid && Date.now() - (x.at || 0) < CLAIM_TTL);
  list.push({ sid, secret, at: Date.now() });
  ls.set(CLAIM_KEY, JSON.stringify(list.slice(-5)));
}
/** 로그인 상태면 담기를 누른 지 30분 안 된 응시를 계정으로 옮긴다 — 오래된 것·성공·영구 실패는 목록에서 뺀다 */
export async function claimPending() {
  const list = ls.json(CLAIM_KEY, []).filter((x) => Date.now() - (x.at || 0) < CLAIM_TTL);
  if (!list.length) { ls.del(CLAIM_KEY); return 0; }
  if (!(await accessToken())) { ls.set(CLAIM_KEY, JSON.stringify(list)); return 0; }
  let n = 0;
  const keep = [];
  for (const c of list) {
    try { await assessCall("claim", { sid: c.sid, secret: c.secret }); n++; }
    catch (e) { if (!(e.status >= 400 && e.status < 500)) keep.push(c); }
  }
  ls.set(CLAIM_KEY, JSON.stringify(keep));
  return n;
}
export const hasPendingClaim = (sid) => ls.json(CLAIM_KEY, []).some((x) => x.sid === sid);

/** 알림(새로 열린 평가) 본 표시 */
export const seenCodes = () => new Set(ls.json(SEEN_KEY, []));
export function markSeen(code) {
  const s = seenCodes();
  if (s.has(code)) return;
  s.add(code);
  ls.set(SEEN_KEY, JSON.stringify([...s].slice(-200)));
}

/** /e 경로로 이동 (학생앱 셸 밖 단독 페이지 — /answers 와 같은 방식) */
export function goAssess(code = "") {
  history.pushState(null, "", code ? `/e/${encodeURIComponent(code)}` : "/e");
  window.dispatchEvent(new Event("pathchange"));
  window.scrollTo(0, 0);
}
