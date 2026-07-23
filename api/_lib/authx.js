// src/lib/authx.js — raindrop 클라이언트 공통 모듈
import * as SC from '../supabaseClient';
export const supabase = SC.supabase || SC.default;

// ---------- 서버 API ----------
export async function api(path, body, { auth = false } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const { data } = await supabase.auth.getSession();
    const t = data?.session?.access_token;
    if (t) headers.Authorization = `Bearer ${t}`;
  }
  const r = await fetch(`/api/${path}`, {
    method: 'POST', headers, body: JSON.stringify(body || {}),
  });
  let j = null;
  try { j = await r.json(); } catch { /* 빈 응답 */ }
  if (!r.ok) {
    const e = new Error(j?.error || `요청 실패 (${r.status})`);
    e.status = r.status; e.data = j;
    throw e;
  }
  return j;
}

// ---------- OTP ----------
export const otpSend = (phone, purpose) => api('otp', { action: 'send', phone, purpose });
export const otpVerify = (phone, purpose, code) => api('otp', { action: 'verify', phone, purpose, code });

// ---------- 전화번호 ----------
export function normPhone(p) {
  const d = String(p || '').replace(/\D/g, '');
  return /^01[016789]\d{7,8}$/.test(d) ? d : null;
}

// ---------- 고유번호 (오프라인 1차 검사 — 서버 검증과 동일 공개 알고리즘) ----------
export function normCode(s) {
  return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
}
export function fmtCode(c) {
  const n = normCode(c);
  return n.length === 15 ? `${n.slice(0, 5)}-${n.slice(5, 12)}-${n.slice(12)}` : n;
}
const charVal = (ch) => (/\d/.test(ch) ? +ch : ch.charCodeAt(0) - 55);
function checksum(s) {
  let sum = 0;
  for (let i = 0; i < s.length; i++) {
    const v = charVal(s[s.length - 1 - i]) * (i % 2 === 0 ? 2 : 1);
    sum += Math.floor(v / 10) + (v % 10);
  }
  return String((10 - (sum % 10)) % 10);
}
export function quickCheckCode(code) {
  const c = normCode(code);
  return c.length === 15 && checksum(c.slice(0, 12)) === c[12];
}
export const codeRoleType = (code) => +normCode(code)[5] || 0;

// ---------- 최근 로그인 방법 (기기 로컬) ----------
const LAST_KEY = 'ash.lastLogin';
export function recordLoginMethod(m) {
  try { localStorage.setItem(LAST_KEY, JSON.stringify({ m, at: Date.now() })); } catch { /* 무시 */ }
}
export function getLastLoginMethod() {
  try { return JSON.parse(localStorage.getItem(LAST_KEY) || 'null')?.m || null; } catch { return null; }
}
// m 값: 'id' | 'google' | 'kakao' | 'qr' | 'trial'

export const PW_MIN = 8;
