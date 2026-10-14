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
// 응시 기록 칸: 비로그인은 평가마다 한 칸, 로그인은 계정마다 따로 — 같은 기기를 여럿이 써도(학원 태블릿) 계정 기록과 비로그인 기록이 섞이지 않는다
const SESS_KEY = (code, uid) => (uid ? `ash.assess.s.${code}.u.${uid}` : `ash.assess.s.${code}`);
const ANON_KEY_RE = /^ash\.assess\.s\.([A-Z0-9]{4,12})$/;
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

/** 평가별 응시 기록 { sid, secret, at, step, uid } — 지금 보는 사람(uid: 계정 id, 비로그인 null)의 칸만 읽고 쓴다 */
export function readLocalFor(code, uid) {
  const v = ls.json(SESS_KEY(code, uid), null);
  return v && (v.uid || null) === (uid || null) ? v : null;
}
export function writeLocal(code, patch, uid) {
  const cur = readLocalFor(code, uid) || {};
  const next = { ...cur, ...patch, uid: uid || null, at: Date.now() };
  ls.set(SESS_KEY(code, uid), JSON.stringify(next));
  return next;
}
export const clearLocal = (code, uid) => ls.del(SESS_KEY(code, uid));

/** 이 기기에 남은 비로그인 응시(비로그인 결과 목록용) */
export function localSessions() {
  const out = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      const m = k && k.match(ANON_KEY_RE);
      if (m) {
        const v = ls.json(k, null);
        if (v?.sid && !v.uid) out.push({ code: m[1], ...v });
      }
    }
  } catch { /* */ }
  return out.sort((a, b) => (b.at || 0) - (a.at || 0));
}

/**
 * 계정에 담기 — 결과 화면에서 '로그인하고 담기'를 누른 응시만 30분 동안 기억한다.
 * 로그인한 뒤 저절로 담지 않고 "이 기록을 담을까요?"로 한 번 묻는다(공용 기기에서 남의 결과가 내 계정에 들어오지 않게).
 * label: { code, title, name } — 물을 때 보여 줄 것
 */
const CLAIM_TTL = 30 * 60 * 1000;
const freshClaims = () => ls.json(CLAIM_KEY, []).filter((x) => x?.sid && Date.now() - (x.at || 0) < CLAIM_TTL);
export function addPendingClaim(sid, secret, label = {}) {
  const list = freshClaims().filter((x) => x.sid !== sid);
  list.push({ sid, secret, at: Date.now(), code: label.code || null, title: label.title || "", name: label.name || "" });
  ls.set(CLAIM_KEY, JSON.stringify(list.slice(-5)));
}
export function pendingClaims() {
  const list = freshClaims();
  if (!list.length) ls.del(CLAIM_KEY);
  return list;
}
export function dropClaim(sid) {
  const list = freshClaims().filter((x) => x.sid !== sid);
  if (list.length) ls.set(CLAIM_KEY, JSON.stringify(list)); else ls.del(CLAIM_KEY);
}
/** 학생이 '내 기록이 맞아요'를 눌렀을 때만 */
export async function claimOne(sid) {
  const c = freshClaims().find((x) => x.sid === sid);
  if (!c) return false;
  try { await assessCall("claim", { sid: c.sid, secret: c.secret }); dropClaim(sid); return true; }
  catch (e) { if (e.status >= 400 && e.status < 500) dropClaim(sid); throw e; }
}

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
