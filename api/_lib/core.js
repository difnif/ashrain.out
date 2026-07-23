// api/_lib/core.js — 서버 전용 공통 모듈 (클라이언트 번들에 절대 포함 금지)
// 필요 환경변수(Vercel):
//   SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
//   TOKEN_SECRET            임의 64자 hex (전화인증 토큰 서명)
//   OTP_PEPPER              임의 문자열 (OTP 해시 소금)
//   CODE_SECRET_V1          임의 64자 hex (고유번호 서명·년도 암호화 키 v1)
//   ALIGO_API_KEY, ALIGO_USER_ID, ALIGO_SENDER (등록된 발신번호)

import crypto from 'node:crypto';
import { createClient } from '@supabase/supabase-js';

const need = (k) => {
  const v = process.env[k];
  if (!v) throw new Error(`missing env: ${k}`);
  return v;
};

// ---------- Supabase ----------
export const admin = () =>
  createClient(need('SUPABASE_URL'), need('SUPABASE_SERVICE_ROLE_KEY'), {
    auth: { persistSession: false, autoRefreshToken: false },
  });

export const anon = () =>
  createClient(need('SUPABASE_URL'), need('SUPABASE_ANON_KEY'), {
    auth: { persistSession: false, autoRefreshToken: false },
  });

// 요청의 Supabase JWT → 유저 (없으면 null)
export async function getUser(req) {
  const h = req.headers.authorization || '';
  const jwt = h.startsWith('Bearer ') ? h.slice(7) : null;
  if (!jwt) return null;
  const { data, error } = await admin().auth.getUser(jwt);
  return error ? null : data.user;
}

// ---------- 응답 헬퍼 ----------
export const json = (res, status, obj) => res.status(status).json(obj);
export const bad = (res, msg, status = 400) => res.status(status).json({ error: msg });
export const clientIp = (req) =>
  ((req.headers['x-forwarded-for'] || '').split(',')[0].trim() || null);

// ---------- 전화번호 ----------
export function normPhone(p) {
  const d = String(p || '').replace(/\D/g, '');
  return /^01[016789]\d{7,8}$/.test(d) ? d : null;
}

// ---------- 해시/난수 ----------
export const sha = (s) =>
  crypto.createHash('sha256').update(String(s) + need('OTP_PEPPER')).digest('hex');
export const randCode6 = () => String(crypto.randomInt(0, 1000000)).padStart(6, '0');
export const randToken = (n = 24) => crypto.randomBytes(n).toString('base64url');
export const randPassword = (n = 12) => {
  const cs = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789';
  let out = '';
  for (let i = 0; i < n; i++) out += cs[crypto.randomInt(cs.length)];
  return out;
};

// ---------- 서명 토큰 (JWT-lite, 무의존) ----------
export function signToken(payload, ttlSec) {
  const body = { ...payload, exp: Math.floor(Date.now() / 1000) + ttlSec };
  const p = Buffer.from(JSON.stringify(body)).toString('base64url');
  const sig = crypto.createHmac('sha256', need('TOKEN_SECRET')).update(p).digest('base64url');
  return `${p}.${sig}`;
}
export function verifyToken(tok) {
  try {
    const [p, sig] = String(tok || '').split('.');
    if (!p || !sig) return null;
    const good = crypto.createHmac('sha256', need('TOKEN_SECRET')).update(p).digest('base64url');
    const a = Buffer.from(sig), b = Buffer.from(good);
    if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
    const body = JSON.parse(Buffer.from(p, 'base64url').toString());
    if (!body.exp || body.exp < Date.now() / 1000) return null;
    return body;
  } catch {
    return null;
  }
}

// ============================================================
// 고유번호 (member code)
//   전체 15자 = 학원5 + 개인7 + 검증3
//   학원5   : 이니셜3(공개) + 비공개번호2
//   개인7   : 유형1 + 등록년도(암호화 문자+숫자 2) + 출생년도(〃 2) + 무작위2
//   검증3   : 검증숫자1(공개 가중합, 오타용) + 서명 알파벳1 + 서명 숫자1(비밀키)
//   표기    : AAAAA-PPPPPPP-CSS  (입력 시 하이픈 없어도 인식)
//   ※ 개인부 무작위가 1→2자인 이유: 동일 학원·등록년·출생년 집단 수용량 31→961 확보
// ============================================================
const L24 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'; // I,O 제외 24자
const RAND = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'; // 육안 혼동 문자 제외

const codeKey = (ver = 'v1') => need(`CODE_SECRET_${String(ver).toUpperCase()}`);

// 학원별 년도 암호화 오프셋 4개 (키+학원코드에서 유도 — DB 유출만으로는 복원 불가)
function encOffsets(academy5, ver) {
  return crypto.createHmac('sha256', codeKey(ver)).update(`enc|${academy5}`).digest();
}

const charVal = (ch) => (/\d/.test(ch) ? +ch : ch.charCodeAt(0) - 55); // A=10..Z=35

// 공개 검증숫자: Luhn 변형 (가중 2,1 교대·자릿수 합)
export function checksum(s) {
  let sum = 0;
  for (let i = 0; i < s.length; i++) {
    const v = charVal(s[s.length - 1 - i]) * (i % 2 === 0 ? 2 : 1);
    sum += Math.floor(v / 10) + (v % 10);
  }
  return String((10 - (sum % 10)) % 10);
}

function signPart(base12, attrs, ver = 'v1') {
  const h = crypto.createHmac('sha256', codeKey(ver))
    .update(`sig|${ver}|${base12}|${attrs}`).digest();
  return L24[h[0] % 24] + String(h[1] % 10);
}

export function normCode(s) {
  return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
}
export function fmtCode(c) {
  const n = normCode(c);
  return n.length === 15 ? `${n.slice(0, 5)}-${n.slice(5, 12)}-${n.slice(12)}` : n;
}

// 생성. academy5는 academies.code, region은 academies.region
export function makeCode({ academy, region, roleType, regYear, birthYear, ver = 'v1' }) {
  const o = encOffsets(academy, ver);
  const yy = ((regYear ?? new Date().getFullYear()) % 100 + 100) % 100;
  const by = (((birthYear ?? 0) % 100) + 100) % 100;
  const person =
    String(roleType) +
    L24[(yy + o[0]) % 24] + String((yy + o[1]) % 10) +
    L24[(by + o[2]) % 24] + String((by + o[3]) % 10) +
    RAND[crypto.randomInt(RAND.length)] + RAND[crypto.randomInt(RAND.length)];
  const base = academy + person; // 12자
  return base + checksum(base) + signPart(base, `${region}|${roleType}`, ver);
}

// 1차(오프라인) 검사: 길이+검증숫자
export function quickCheck(code) {
  const c = normCode(code);
  return c.length === 15 && checksum(c.slice(0, 12)) === c[12];
}

// 최종 검증: 비밀키 서명 대조
export function verifyCode(code, { region, ver = 'v1' }) {
  const c = normCode(code);
  if (!quickCheck(c)) return { ok: false, why: 'checksum' };
  const base = c.slice(0, 12);
  const roleType = +c[5];
  if (![1, 2, 3, 5, 7, 9].includes(roleType)) return { ok: false, why: 'role' };
  if (signPart(base, `${region}|${roleType}`, ver) !== c.slice(13)) {
    return { ok: false, why: 'signature' };
  }
  return { ok: true, roleType, academy: c.slice(0, 5) };
}

// 해독 (관리자 표시용): 등록년도·출생년도 복원
export function decodeCode(code, { ver = 'v1' } = {}) {
  const c = normCode(code);
  if (c.length !== 15) return null;
  const academy = c.slice(0, 5);
  const o = encOffsets(academy, ver);
  const solve = (li, di, oL, oD) => {
    if (li < 0 || !(di >= 0)) return null;
    for (let y = 0; y < 100; y++) {
      if ((y + oL) % 24 === li && (y + oD) % 10 === di) return y;
    }
    return null;
  };
  const yy = solve(L24.indexOf(c[6]), +c[7], o[0], o[1]);
  const by = solve(L24.indexOf(c[8]), +c[9], o[2], o[3]);
  return {
    academy,
    roleType: +c[5],
    regYear: yy == null ? null : 2000 + yy,
    birthYear: by == null ? null : 2000 + by,
  };
}

export const ROLE_MAP = { 1: 'student', 2: 'parent', 3: 'assistant', 5: 'teacher', 7: 'point', 9: 'trial' };

// ============================================================
// SMS 어댑터  (SMS_PROVIDER = 'solapi'(기본) | 'aligo')
//   solapi : API키+시크릿 HMAC 서명 인증 → IP 등록 불필요 (Vercel 서버리스 호환)
//   aligo  : 발송 서버 IP 사전 등록 필수 → 고정 IP 환경에서만 사용 가능
// ============================================================
async function sendViaSolapi(phone, msg) {
  const apiKey = need('SOLAPI_API_KEY');
  const apiSecret = need('SOLAPI_API_SECRET');
  const date = new Date().toISOString();
  const salt = crypto.randomBytes(16).toString('hex');
  const signature = crypto.createHmac('sha256', apiSecret).update(date + salt).digest('hex');

  const r = await fetch('https://api.solapi.com/messages/v4/send', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `HMAC-SHA256 apiKey=${apiKey}, date=${date}, salt=${salt}, signature=${signature}`,
    },
    body: JSON.stringify({
      message: { to: phone, from: need('SOLAPI_SENDER'), text: msg, type: 'SMS' },
    }),
  });
  const j = await r.json().catch(() => ({}));
  return { ok: r.ok && !j.errorCode, raw: j };
}

async function sendViaAligo(phone, msg) {
  const body = new URLSearchParams({
    key: need('ALIGO_API_KEY'),
    user_id: need('ALIGO_USER_ID'),
    sender: need('ALIGO_SENDER'),
    receiver: phone,
    msg,
    msg_type: 'SMS',
  });
  const r = await fetch('https://apis.aligo.in/send/', { method: 'POST', body });
  const j = await r.json().catch(() => ({}));
  return { ok: String(j.result_code) === '1', raw: j }; // '1' = 성공
}

export async function sendSMS(phone, msg) {
  const provider = (process.env.SMS_PROVIDER || 'solapi').toLowerCase();
  return provider === 'aligo' ? sendViaAligo(phone, msg) : sendViaSolapi(phone, msg);
}
