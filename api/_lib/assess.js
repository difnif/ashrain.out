// api/_lib/assess.js — 서술형 평가 (POST /api/photo { task:"assess", op, ... })
// api/photo.js 가 task:"assess" 를 이 함수로 넘긴다 — Vercel 함수 개수(12)를 늘리지 않으려고 새 api 파일을 만들지 않았다.
//
// 흐름: 채팅방 생성기 JSON → 관리자 등록(admin_register) → 학생앱 알림·QR(/e/<코드>) → 열람(get) → 시작(start)
//       → 쪽마다 촬영(page: 브라우저가 마커로 편 사진의 판독 영역만) → 판독(읽기 모델) → 채점(채점 모델) → 제출(finish) → 결과(result)
// 로그인 없이도 된다: 기기 토큰(device) + 응시 비밀값(secret, 해시만 저장)으로 응시 기록을 잇고, 2쪽 이름·학년으로 응시자 명부를 만든다.
// 원칙
//   · 정답·모범 풀이·채점 기준은 학생에게 가지 않는다 — 공개 시점(reveal)이 지나야 결과 화면에 붙는다.
//   · 판독은 "학생이 쓴 그대로"(맞는 값으로 고쳐 읽지 않음, 그은 줄은 따로, 못 읽는 글자는 ⍰). 채점은 판독문 + 기준표로 따로.
//   · 사진(펴진 쪽 이미지)은 app_settings.assess_store_images='on' 일 때만 비공개 버킷 assess-pages 에 남긴다(기본 off — 동의서 정리 뒤 켠다).
//   · IP·기기 토큰은 소금 친 해시로만 저장(호출 한도용).
// app_settings: assess_model_read(기본 photo_model) · assess_model_strong(판독 재시도, 기본 photo_model_fallback) · assess_model_grade(기본 photo_model_grade)
//               · assess_store_images(off|on) · assess_anon(on|off — off 면 로그인 응시만) · assess_limits(JSON, 아래 LIMITS 덮어쓰기)
import crypto from "node:crypto";
import { createClient } from "@supabase/supabase-js";
import { renderText } from "../../src/lib/mathir.js";
import { relBoxes } from "../../src/lib/assess/sheet.js";
import {
  validateSpec, publicView, answerKey, canReveal, aggregate, policyOf,
  normGrade, normName, personKey,
} from "../../src/lib/assess/spec.js";

const DEFAULT_READ = "claude-sonnet-4-6";
const DEFAULT_GRADE = "claude-opus-4-8";
export const LIMITS = {
  page_attempts: 4,          // 한 쪽을 다시 찍을 수 있는 횟수(판독 호출 기준)
  sessions_per_taker: 3,     // 한 사람(로그인 계정·기기)이 한 평가를 새로 시작할 수 있는 횟수
  anon_ip_day: 400,          // 비로그인: IP 하나의 하루 판독 쪽 수 (학원 와이파이 한 반 기준 여유)
  anon_set_day: 3000,        // 비로그인: 평가 하나의 하루 판독 쪽 수
  anon_global_day: 6000,     // 비로그인: 전체 하루 판독 쪽 수
  user_day: 300,             // 로그인: 계정 하나의 하루 판독 쪽 수
};
const MAX_CROP_B64 = 2_800_000;
const MAX_IMAGE_B64 = 1_200_000;
const MAX_SPEC_CHARS = 2_000_000;
const TIME_BUDGET_MS = 50_000;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const TAGS = ["식세우기", "계산실수", "부호", "단위", "조건누락", "개념", "구하는대상혼동", "판독불가", "없음"];

// ─────────────────────────────────────────────────────────────── 공용
class HttpError extends Error { constructor(status, msg, extra) { super(msg); this.status = status; this.extra = extra; } }
const fail = (status, msg, extra) => { throw new HttpError(status, msg, extra); };

function svc() {
  const url = process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_KEY;
  if (!url || !key) return null;
  return createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
}
const pepper = () => process.env.OTP_PEPPER || process.env.TOKEN_SECRET || process.env.SUPABASE_SERVICE_ROLE_KEY || "ash-assess";
const hash = (s) => crypto.createHash("sha256").update(String(s) + "|assess|" + pepper()).digest("hex");
function safeEq(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(String(b || ""));
  return x.length === y.length && x.length > 0 && crypto.timingSafeEqual(x, y);
}
const clientIp = (req) => String(req.headers?.["x-forwarded-for"] || "").split(",")[0].trim() || String(req.socket?.remoteAddress || "") || "unknown";
const str = (v, n = 300) => (typeof v === "string" ? v.trim().slice(0, n) : "");
const arr = (v) => (Array.isArray(v) ? v : []);
/** 마이그레이션 전(표 없음) 오류인가 */
const missingRel = (e) => e && ["42P01", "42703", "PGRST202", "PGRST204", "PGRST205"].includes(String(e.code || ""));
function kstDayStartISO() {
  const kst = Date.now() + 9 * 3600 * 1000;
  return new Date(Math.floor(kst / 86400000) * 86400000 - 9 * 3600 * 1000).toISOString();
}
async function settings(db) {
  const keys = ["assess_model_read", "assess_model_strong", "assess_model_grade", "assess_store_images", "assess_anon", "assess_limits",
    "photo_model", "photo_model_grade", "photo_model_fallback"];
  const { data } = await db.from("app_settings").select("key, value").in("key", keys);
  const out = {};
  for (const r of data || []) out[r.key] = r.value;
  let lim = {};
  try { lim = out.assess_limits ? JSON.parse(out.assess_limits) : {}; } catch { lim = {}; }
  out.limits = { ...LIMITS };
  for (const k of Object.keys(LIMITS)) if (Number.isFinite(+lim[k]) && +lim[k] > 0) out.limits[k] = Math.round(+lim[k]);
  return out;
}
async function userOf(db, req) {
  const h = req.headers?.authorization || "";
  const jwt = h.startsWith("Bearer ") ? h.slice(7) : null;
  if (!jwt) return null;
  try {
    const { data, error } = await db.auth.getUser(jwt);
    return error ? null : data?.user || null;
  } catch { return null; }
}

// ── 호출 한도 (assess_calls: 키·시각만) ───────────────────────────────────────
async function countKey(db, key) {
  const { count, error } = await db.from("assess_calls").select("*", { count: "exact", head: true }).eq("key", key).gte("created_at", kstDayStartISO());
  if (error) throw error;
  return count ?? 0;
}
async function chargeCalls(db, keys, caps) {
  for (const [key, cap] of keys.map((k, i) => [k, caps[i]])) {
    const n = await countKey(db, key);
    if (n >= cap) return key;
  }
  await db.from("assess_calls").insert(keys.map((key) => ({ key })));
  return null;
}

// ── Claude ───────────────────────────────────────────────────────────────────
async function callClaude({ model, system, content, maxTokens = 2000, timeoutMs = 40_000 }) {
  let r;
  try {
    r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": process.env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model, max_tokens: maxTokens, system, messages: [{ role: "user", content }] }),
      signal: typeof AbortSignal !== "undefined" && AbortSignal.timeout ? AbortSignal.timeout(timeoutMs) : undefined,
    });
  } catch (e) {
    throw new Error(e?.name === "TimeoutError" || e?.name === "AbortError" ? "AI 응답이 늦어요 — 잠시 뒤 다시 시도해 주세요" : "AI 호출 실패");
  }
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error("AI 호출 실패: " + (j?.error?.message || r.status));
  return (j.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
}
const img = (data) => ({ type: "image", source: { type: "base64", media_type: "image/jpeg", data } });
const txt = (text) => ({ type: "text", text });
function parseObj(text) {
  const m = String(text || "").replace(/```json|```/g, "").match(/\{[\s\S]*\}/);
  if (!m) throw new Error("AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요");
  try { return JSON.parse(m[0]); } catch { throw new Error("AI 응답을 JSON으로 해석하지 못했어요 — 다시 시도해 주세요"); }
}
const plain = (t) => { try { return renderText(String(t || "")); } catch { return String(t || ""); } };

// ─────────────────────────────────────────────────────────────── 프롬프트
const SYS_READ_ITEM = `너는 학생 손글씨 수학 풀이 판독기다. 이미지는 시험지 한 쪽에서 답안 칸만 잘라 낸 것이다.
칸은 위에서부터 ① 식 세우기(s1) · ② 식 풀기(s2) · ③ 구하는 것(s3)이고, 각 칸 맨 위의 인쇄된 머리줄(칸 이름·배점·안내)은 답안이 아니다.
판독 원칙 — 반드시 지킨다:
1) 학생이 쓴 그대로 옮긴다. 틀린 값·틀린 식·맞춤법도 고치지 않는다. 맞는 값으로 고쳐 읽으면 실패다.
2) 문제 내용은 애매한 글자를 고를 때만 참고한다. 같은 학생이 앞뒤 줄에 쓴 글자 모양과 이어지는 식을 먼저 근거로 삼는다.
3) 줄을 그어 지운 부분은 그 줄을 struck:true 로 적는다(내용도 읽히면 적는다). 새까맣게 덮어 칠해 못 읽으면 "[덮어씀]".
4) 끝내 읽을 수 없는 글자는 ⍰ 로 남긴다. 억지로 추측하지 않는다.
5) → 로 자리를 옮겨 이어 쓴 곳은 읽는 순서대로 이어 적고, 옮겨 간 첫 줄에 arrow:true.
6) 칸 밖(여백)에 쓴 것은 outside 에 적는다. 칸이 비어 있으면 empty:true.
수식 표기: 평문으로 — × ÷ − ² ³ √ ≤ ≥ ≠, 분수는 a/b, 괄호는 쓴 그대로. LaTeX·마크다운 금지.
출력 — 아래 JSON 하나만, 설명 금지:
{"s1":{"lines":[{"t":"줄 내용","struck":false,"arrow":false}],"empty":false},"s2":{"lines":[],"empty":false},"s3":{"lines":[],"empty":false},
 "outside":["…"],"legibility":{"score":1,"issues":["짧은 관찰(예: 7을 1처럼 씀)"]}}
legibility.score 는 1(거의 못 읽음)~5(또렷함).`;

const SYS_READ_INFO = `너는 시험지 2쪽(응시 정보) 판독기다. 이미지에는 학년 칸, 이름 칸, 필적 확인 줄(인쇄된 모범 문장 아래 학생이 따라 쓴 줄), 닉네임 칸이 있다.
인쇄된 글자(칸 이름·"중학교 ○ 학년"·모범 문장)는 답이 아니다 — 학생 손글씨만 읽는다. 쓴 그대로 옮기고, 읽을 수 없는 글자는 ⍰.
- grade: 학년 칸 손글씨 숫자만(예 "2"). 없으면 null.
- name: 이름 칸 손글씨. 없으면 null.
- nickname: 닉네임 칸 손글씨. 비었으면 null.
- phrase: 필적 확인 줄마다 따라 쓴 것을 쓴 그대로(모범 문장과 달라도 쓴 그대로). 비어 있는 줄은 "".
출력 — 아래 JSON 하나만: {"grade":"2","name":"홍길동","nickname":null,"phrase":["…","…"],"confidence":{"grade":0.9,"name":0.8,"nickname":0},"legibility":{"score":4}}`;

function sysGrade(policy) {
  const carry = { full: "① 이 틀렸어도 ② 가 학생 자신이 세운 식을 바르게 풀었으면 ② 는 만점까지 인정한다(연쇄 과정 인정).",
    half: "① 이 틀렸어도 ② 가 학생 자신이 세운 식을 바르게 풀었으면 ② 는 배점의 절반(내림)까지 인정한다(연쇄 과정 인정).",
    none: "① 이 틀리면 ② 는 인정하지 않는다." }[policy.carry];
  return `너는 한국 수학 학원의 서술형 채점자다. 학생 풀이 판독문(손글씨를 그대로 옮긴 것)과 문항·정답·모범 풀이·채점 기준으로 채점한다.
규칙:
- 요소별 배점은 [채점 기준] 그대로. 각 요소 got 은 0 이상 배점 이하의 정수.
- 줄을 그어 지운 줄(~~ ~~ 표시)은 채점하지 않는다. 감점도 없다.
- ⍰ 는 판독기가 못 읽은 글자다. 그 글자 때문에 맞고 틀림이 갈리면 단정하지 말고 needs_review:true 로 하고, 읽힌 부분만으로 채점한다.
- 과정 없이 답만 쓰면 마지막 요소(구하는 것)만 줄 수 있다 — 최대 ${policy.answer_only_max}점.
- ${carry}
- ${policy.alt_method === "accept" ? "모범 풀이와 다른 방법이라도 수학적으로 맞으면 같은 점수를 준다." : "모범 풀이와 다른 방법이면 해당 요소에서 1점을 뺀다."}
- 기준의 '부분' 설명이 있으면 그대로 따른다.
- reason 은 판독문의 어느 줄을 근거로 했는지 한 줄. 학생이 쓰지 않은 내용을 지어내지 않는다.
- feedback 은 학생에게 하는 말: 다정한 해요체 두 문장 이내, 학생 풀이를 기준으로(정답 풀이를 통째로 쓰지 않는다).
출력 — 아래 JSON 하나만:
{"marks":[{"no":1,"got":4,"reason":"…"}],"final_answer":"학생이 ③에 쓴 최종 답(없으면 null)","final_ok":true,"needs_review":false,
 "feedback":["…"],"tags":["${TAGS.join("|")} 중 해당"]}`;
}

// ── 판독·채점 결과 정리 (모델 출력은 모양·길이를 죈다) ─────────────────────────
function cleanBoxRead(b) {
  const lines = arr(b?.lines).slice(0, 40).map((l) => ({ t: str(typeof l === "string" ? l : l?.t, 200), struck: !!l?.struck, arrow: !!l?.arrow })).filter((l) => l.t);
  return { lines, empty: !!b?.empty && !lines.length };
}
const countUnreadable = (read) => ["s1", "s2", "s3"].reduce((n, k) => n + (read[k]?.lines || []).reduce((a, l) => a + (l.t.match(/⍰/g) || []).length, 0), 0);
function cleanReadItem(p) {
  const out = { s1: cleanBoxRead(p?.s1), s2: cleanBoxRead(p?.s2), s3: cleanBoxRead(p?.s3),
    outside: arr(p?.outside).map((x) => str(x, 200)).filter(Boolean).slice(0, 5),
    legibility: { score: Math.min(5, Math.max(1, Math.round(+p?.legibility?.score || 3))), issues: arr(p?.legibility?.issues).map((x) => str(x, 120)).filter(Boolean).slice(0, 5) } };
  out.unreadable = countUnreadable(out);
  out.blank = ["s1", "s2", "s3"].every((k) => !out[k].lines.length);
  return out;
}
function cleanReadInfo(p, nPhrase) {
  const conf = (v) => Math.min(1, Math.max(0, +v || 0));
  const phrase = arr(p?.phrase).slice(0, nPhrase || 6).map((x) => str(x, 140));
  return {
    grade: str(p?.grade == null ? "" : String(p.grade), 10) || null, name: str(p?.name, 20) || null, nickname: str(p?.nickname, 20) || null,
    phrase, confidence: { grade: conf(p?.confidence?.grade), name: conf(p?.confidence?.name), nickname: conf(p?.confidence?.nickname) },
    legibility: { score: Math.min(5, Math.max(1, Math.round(+p?.legibility?.score || 3))) },
  };
}
function cleanGrade(p, rubric) {
  const marks = rubric.map((r, k) => {
    const no = +r.no || k + 1;
    const m = arr(p?.marks).find((x) => +x?.no === no) || arr(p?.marks)[k] || {};
    return { no, got: Math.min(+r.points || 0, Math.max(0, Math.round(+m?.got || 0))), reason: str(m?.reason, 220) };
  });
  return {
    marks, total: marks.reduce((a, m) => a + m.got, 0), max: rubric.reduce((a, r) => a + (+r.points || 0), 0),
    final_answer: str(p?.final_answer == null ? "" : String(p.final_answer), 100) || null, final_ok: !!p?.final_ok, needs_review: !!p?.needs_review,
    feedback: arr(p?.feedback).map((x) => str(x, 220)).filter(Boolean).slice(0, 2),
    tags: arr(p?.tags).map(String).filter((t) => TAGS.includes(t)).slice(0, 4),
  };
}
/** 판독문 → 채점 프롬프트용 글 */
function readToText(read) {
  const lab = { s1: "① 식 세우기 칸", s2: "② 식 풀기 칸", s3: "③ 구하는 것 칸" };
  const parts = [];
  for (const k of ["s1", "s2", "s3"]) {
    const ls = read?.[k]?.lines || [];
    parts.push(`[${lab[k]}]` + (ls.length ? "\n" + ls.map((l, i) => `${i + 1}) ${l.struck ? `~~${l.t}~~ (그어 지움)` : l.t}${l.arrow ? " (→ 옮겨 이어 씀)" : ""}`).join("\n") : "\n(비어 있음)"));
  }
  if (read?.outside?.length) parts.push(`[칸 밖]\n${read.outside.join("\n")}`);
  return parts.join("\n\n");
}

async function readItem(model, crop, spec, page, item) {
  const rb = relBoxes(page);
  const ctx = `[칸 위치 — 이 이미지 기준 비율 x,y,w,h]\n① ${JSON.stringify(rb.s1 || {})}\n② ${JSON.stringify(rb.s2 || {})}\n③ ${JSON.stringify(rb.s3 || {})}\n\n`
    + `[문제 — 애매한 글자를 고를 때만 참고]\n${plain(item.story)}\n${arr(item.conditions).map(plain).join("\n")}\n${plain(item.ask)}`;
  const text = await callClaude({ model, system: SYS_READ_ITEM, content: [img(crop), txt(ctx)], maxTokens: 2200 });
  return cleanReadItem(parseObj(text));
}
async function readInfo(model, crop, spec, page) {
  const rb = relBoxes(page);
  const n = arr(spec.phrase).length;
  const ctx = `[칸 위치 — 이 이미지 기준 비율 x,y,w,h]\n${Object.entries(rb).map(([k, v]) => `${k}: ${JSON.stringify(v)}`).join("\n")}\n\n필적 확인 줄 수: ${n}`;
  const text = await callClaude({ model, system: SYS_READ_INFO, content: [img(crop), txt(ctx)], maxTokens: 900 });
  return cleanReadInfo(parseObj(text), n);
}
async function gradeItem(model, item, read, policy) {
  const rb = (item.rubric || []).map((r, k) => `${+r.no || k + 1}. ${r.element} (${r.points}점): ${r.criterion || ""}${r.partial ? ` / 부분: ${r.partial}` : ""}`).join("\n");
  const ctx = `[문항]\n${plain(item.story)}\n${arr(item.conditions).map(plain).join("\n")}\n${plain(item.ask)}\n\n[정답]\n${plain(item.answer)}\n\n`
    + `[모범 풀이]\n${arr(item.solution).map(plain).join("\n")}\n` + (arr(item.accept).length ? `\n[인정하는 다른 풀이]\n${item.accept.map(plain).join("\n")}\n` : "")
    + `\n[채점 기준]\n${rb}\n\n[학생 풀이 판독문]\n${readToText(read)}`;
  const text = await callClaude({ model, system: sysGrade(policy), content: [txt(ctx)], maxTokens: 1200 });
  return cleanGrade(parseObj(text), item.rubric || []);
}

// ─────────────────────────────────────────────────────────────── DB 도우미
async function setByCode(db, code) {
  const c = String(code || "").toUpperCase();
  if (!/^[A-Z0-9]{4,12}$/.test(c)) fail(400, "평가 코드가 이상해요");
  const { data, error } = await db.from("assess_sets").select("*").eq("code", c).maybeSingle();
  if (error) { if (missingRel(error)) fail(503, "서술형 평가가 아직 준비되지 않았어요(DB 설정 전)"); throw error; }
  if (!data || data.status === "draft") fail(404, "평가를 찾을 수 없어요 — QR이나 코드를 다시 확인해 주세요");
  return data;
}
function openState(set, now = Date.now()) {
  if (set.status !== "live") return "closed";
  if (set.opens_at && Date.parse(set.opens_at) > now) return "soon";
  if (set.closes_at && Date.parse(set.closes_at) <= now) return "closed";
  return "open";
}
function ensureOpen(set) {
  const st = openState(set);
  if (st === "soon") fail(403, "아직 열리지 않은 평가예요");
  if (st === "closed") fail(403, "마감된 평가예요");
}
async function loadSession(db, body, user) {
  const sid = String(body.sid || "");
  if (!UUID_RE.test(sid)) fail(400, "응시 기록을 찾을 수 없어요");
  const { data: s, error } = await db.from("assess_sessions").select("*").eq("id", sid).maybeSingle();
  if (error) { if (missingRel(error)) fail(503, "서술형 평가가 아직 준비되지 않았어요(DB 설정 전)"); throw error; }
  if (!s) fail(404, "응시 기록을 찾을 수 없어요");
  const bySecret = body.secret && s.secret_hash && safeEq(hash(body.secret), s.secret_hash);
  const byUser = user && s.user_id && user.id === s.user_id;
  if (!bySecret && !byUser) fail(403, "이 응시 기록에 접근할 수 없어요");
  return s;
}
async function setById(db, id) {
  const { data, error } = await db.from("assess_sets").select("*").eq("id", id).maybeSingle();
  if (error) throw error;
  if (!data) fail(404, "평가를 찾을 수 없어요");
  return data;
}
async function pagesOf(db, sid) {
  const { data, error } = await db.from("assess_pages").select("*").eq("session_id", sid).order("page_no");
  if (error) throw error;
  return data || [];
}
async function upsertPerson(db, { key, user_id = null, name = null, grade = null, nickname = null }) {
  const now = new Date().toISOString();
  const { data: ex } = await db.from("assess_people").select("id, user_id, nickname").eq("person_key", key).maybeSingle();
  if (ex) {
    const patch = { last_seen: now };
    if (name) patch.name = name;
    if (grade) patch.grade = grade;
    if (nickname) patch.nickname = nickname;
    if (user_id && !ex.user_id) patch.user_id = user_id;
    await db.from("assess_people").update(patch).eq("id", ex.id);
    return ex.id;
  }
  const { data, error } = await db.from("assess_people").insert({ person_key: key, user_id, name, grade, nickname, first_seen: now, last_seen: now }).select("id").single();
  if (!error) return data.id;
  const { data: again } = await db.from("assess_people").select("id").eq("person_key", key).maybeSingle();   // 동시 생성 경합
  return again?.id || null;
}
const pageSummary = (pages) => pages.map((p) => ({ no: p.page_no, kind: p.kind, item: p.item_no, status: p.status, attempts: p.attempts, flagged: !!p.flagged }));

function compactRead(read) {
  if (!read) return null;
  const pick = (b) => ({ lines: (b?.lines || []).map((l) => ({ t: l.t, struck: !!l.struck, arrow: !!l.arrow })), empty: !!b?.empty });
  return { s1: pick(read.s1), s2: pick(read.s2), s3: pick(read.s3), outside: read.outside || [], legibility: read.legibility || null, unreadable: read.unreadable || 0 };
}
function resultOf(set, s, pages) {
  const spec = set.spec || {};
  const byItem = {};
  for (const p of pages) if (p.kind === "item" && p.grade && p.item_no) byItem[p.item_no] = p.grade;
  const agg = aggregate(spec, byItem);
  const reveal = canReveal({ reveal: set.reveal, submitted: s.status === "submitted", status: set.status, closes_at: set.closes_at });
  const key = reveal ? answerKey(spec) : null;
  const items = (spec.items || []).map((it, i) => {
    const p = pages.find((x) => x.kind === "item" && x.item_no === it.no);
    const g = p?.grade || null;
    return {
      no: it.no, page: it.page, topic: it.topic || "", got: agg.items[i]?.got ?? 0, max: agg.items[i]?.max ?? 0, graded: !!g,
      elements: (it.rubric || []).map((r, k) => {
        const m = g?.marks?.find((x) => x.no === (+r.no || k + 1));
        return { no: +r.no || k + 1, element: r.element, points: +r.points, got: m ? m.got : null, reason: m?.reason || "" };
      }),
      read: compactRead(p?.read), feedback: g?.feedback || [], final_answer: g?.final_answer || null, final_ok: g ? !!g.final_ok : null,
      needs_review: !!g?.needs_review, flagged: !!p?.flagged, captured: !!p, answer: key ? key[i] : null,
    };
  });
  return {
    sid: s.id, code: set.code, title: set.title, status: s.status, total: agg.total, max: agg.max, graded: agg.graded, n_items: items.length,
    info: s.info || null, submitted_at: s.submitted_at, reveal, reveal_policy: set.reveal, items,
  };
}

// ─────────────────────────────────────────────────────────────── 학생 op
async function opGet(db, body, user, st) {
  const set = await setByCode(db, body.code);
  const pub = publicView(set.spec || {});
  let me = null;
  if (user) {
    const { data: p } = await db.from("profiles").select("username, name, grade, role").eq("id", user.id).maybeSingle();
    me = { name: p?.name || p?.username || null, nick: p?.username || null, grade: p?.grade || null };
  }
  return {
    set: { ...pub, status: set.status, opens_at: set.opens_at, closes_at: set.closes_at, reveal: set.reveal, state: openState(set) },
    store_images: st.assess_store_images === "on", anon: st.assess_anon !== "off", me,
  };
}

async function opStart(req, db, body, user, st) {
  const set = await setByCode(db, body.code);
  ensureOpen(set);
  const device = str(body.device, 80);
  const devHash = device ? hash("dev:" + device) : null;
  const ipHash = hash("ip:" + clientIp(req));
  const ua = str(req.headers?.["user-agent"], 160);
  const lim = st.limits;
  // 이어 하기: 비밀값이 맞고 아직 제출 전이면 그 기록을 쓴다
  if (body.sid && body.secret && UUID_RE.test(String(body.sid))) {
    const { data: s } = await db.from("assess_sessions").select("*").eq("id", body.sid).maybeSingle();
    if (s && s.set_id === set.id && s.status === "open" && s.secret_hash && safeEq(hash(body.secret), s.secret_hash)) {
      return { sid: s.id, resumed: true, status: s.status, info: s.info || null, ocr: s.ocr_info || null, pages: pageSummary(await pagesOf(db, s.id)) };
    }
  }
  if (user) {
    const { data: open } = await db.from("assess_sessions").select("*").eq("set_id", set.id).eq("user_id", user.id).eq("status", "open")
      .order("started_at", { ascending: false }).limit(1);
    if (open?.[0] && !body.fresh) {
      const s = open[0];
      const secret = crypto.randomBytes(24).toString("base64url");     // 이 기기에서도 비밀값으로 이어 갈 수 있게 새로 준다
      await db.from("assess_sessions").update({ secret_hash: hash(secret) }).eq("id", s.id);
      return { sid: s.id, secret, resumed: true, status: s.status, info: s.info || null, ocr: s.ocr_info || null, pages: pageSummary(await pagesOf(db, s.id)) };
    }
    const { count } = await db.from("assess_sessions").select("*", { count: "exact", head: true }).eq("set_id", set.id).eq("user_id", user.id);
    if ((count ?? 0) >= lim.sessions_per_taker) fail(429, `이 평가는 ${lim.sessions_per_taker}번까지 응시할 수 있어요`);
  } else {
    if (st.assess_anon === "off") fail(403, "이 평가는 로그인한 뒤 응시할 수 있어요");
    if (!devHash) fail(400, "기기 정보가 없어요 — 페이지를 새로 고쳐 주세요");
    const { count } = await db.from("assess_sessions").select("*", { count: "exact", head: true }).eq("set_id", set.id).eq("device_hash", devHash);
    if ((count ?? 0) >= lim.sessions_per_taker) fail(429, `이 기기에서는 이 평가를 ${lim.sessions_per_taker}번까지 응시할 수 있어요`);
  }
  const secret = crypto.randomBytes(24).toString("base64url");
  const { data: s, error } = await db.from("assess_sessions").insert({
    set_id: set.id, user_id: user?.id || null, device_hash: devHash, secret_hash: hash(secret), ip_hash: ipHash, ua, status: "open",
  }).select("id, status").single();
  if (error) throw error;
  return { sid: s.id, secret, resumed: false, status: s.status, info: null, ocr: null, pages: [] };
}

async function opPage(req, db, body, user, st, t0) {
  const s = await loadSession(db, body, user);
  if (s.status !== "open") fail(409, "이미 제출한 응시예요");
  const set = await setById(db, s.set_id);
  ensureOpen(set);
  const spec = set.spec || {};
  const pageNo = Math.round(+body.page_no || 0);
  const pg = (spec.pages || []).find((p) => +p.no === pageNo);
  if (!pg) fail(400, "이 평가에 없는 쪽이에요");
  const crop = typeof body.crop === "string" ? body.crop : "";
  const image = typeof body.image === "string" ? body.image : "";
  if (pg.kind !== "guide" && !crop) fail(400, "사진이 없어요 — 다시 찍어 주세요");
  if (crop.length > MAX_CROP_B64 || image.length > MAX_IMAGE_B64) fail(413, "사진이 너무 커요 — 다시 찍어 주세요");
  const qIn = body.quality || {};
  const quality = { sharp: Math.round(+qIn.sharp || 0), paper: Math.round(+qIn.paper || 0), contrast: Math.round(+qIn.contrast || 0), margin: Math.round((+qIn.margin || 0) * 100) / 100 };

  const { data: prev } = await db.from("assess_pages").select("attempts, status").eq("session_id", s.id).eq("page_no", pageNo).maybeSingle();
  const attempts = (prev?.attempts || 0) + 1;
  const lim = st.limits;
  if (pg.kind !== "guide") {
    if (prev && prev.attempts >= lim.page_attempts) fail(429, `${pageNo}쪽은 더 찍을 수 없어요(${lim.page_attempts}번) — 선생님께 알려 주세요`);
    const keys = s.user_id ? [`u:${s.user_id}`] : [`ip:${s.ip_hash || hash("ip:" + clientIp(req))}`, `set:${set.id}`, "anon"];
    const caps = s.user_id ? [lim.user_day] : [lim.anon_ip_day, lim.anon_set_day, lim.anon_global_day];
    const over = await chargeCalls(db, keys, caps);
    if (over) fail(429, "오늘 채점할 수 있는 양을 다 썼어요 — 내일 다시 이어서 찍어 주세요");
  }
  const base = { session_id: s.id, page_no: pageNo, kind: pg.kind, item_no: pg.kind === "item" ? +pg.item : null, attempts, quality, updated_at: new Date().toISOString() };

  if (pg.kind === "guide") {
    await db.from("assess_pages").upsert({ ...base, status: "ok", read: null, grade: null }, { onConflict: "session_id,page_no" });
    return { kind: "guide", page_no: pageNo, status: "ok" };
  }
  if (!process.env.ANTHROPIC_API_KEY) fail(500, "AI 키가 설정되지 않았어요");
  const readModel = st.assess_model_read || st.photo_model || DEFAULT_READ;
  const strongModel = st.assess_model_strong || st.photo_model_fallback || st.photo_model_grade || DEFAULT_GRADE;
  const gradeModel = st.assess_model_grade || st.photo_model_grade || DEFAULT_GRADE;

  let image_path = null;
  if (st.assess_store_images === "on" && image) {
    const path = `${set.code}/${s.id}/p${pageNo}.jpg`;
    const { error: upErr } = await db.storage.from("assess-pages").upload(path, Buffer.from(image, "base64"), { contentType: "image/jpeg", upsert: true });
    if (!upErr) image_path = path;
  }

  if (pg.kind === "info") {
    let read = await readInfo(readModel, crop, spec, pg);
    let model_read = readModel;
    if ((read.confidence.name < 0.5 || !read.name) && strongModel !== readModel && Date.now() - t0 < TIME_BUDGET_MS * 0.45) {
      try { const r2 = await readInfo(strongModel, crop, spec, pg); if (r2.name && r2.confidence.name >= read.confidence.name) { read = r2; model_read = strongModel; } } catch { /* 첫 결과 */ }
    }
    await db.from("assess_pages").upsert({ ...base, status: "read", read, grade: null, model_read, ...(image_path ? { image_path } : {}) }, { onConflict: "session_id,page_no" });
    await db.from("assess_sessions").update({ ocr_info: read }).eq("id", s.id);
    const suggestion = { name: normName(read.name), grade: normGrade(read.grade, set.spec?.level || set.level), nickname: read.nickname ? str(read.nickname, 20) : null };
    return { kind: "info", page_no: pageNo, status: "read", read, suggestion };
  }

  // 문제 쪽: 판독 → (시간이 되면) 채점
  const item = (spec.items || []).find((it) => +it.no === +pg.item);
  if (!item) fail(400, "문항 정보가 없어요");
  let read = await readItem(readModel, crop, spec, pg, item);
  let model_read = readModel;
  if ((read.unreadable > 3 || read.legibility.score <= 2) && !read.blank && strongModel !== readModel && Date.now() - t0 < TIME_BUDGET_MS * 0.4) {
    try { const r2 = await readItem(strongModel, crop, spec, pg, item); if (r2.unreadable <= read.unreadable) { read = r2; model_read = strongModel; } } catch { /* 첫 결과 */ }
  }
  let grade = null, model_grade = null;
  if (read.blank) {
    grade = cleanGrade({ marks: [], feedback: ["답안 칸이 비어 있어요. 아는 데까지라도 써 보면 점수를 받을 수 있어요."], final_ok: false, tags: ["없음"] }, item.rubric || []);
    model_grade = "rule:blank";
  } else if (Date.now() - t0 < TIME_BUDGET_MS * 0.58) {
    try { grade = await gradeItem(gradeModel, item, read, policyOf(spec)); model_grade = gradeModel; } catch { grade = null; }
  }
  await db.from("assess_pages").upsert({ ...base, status: grade ? "graded" : "read", read, grade, model_read, model_grade, flagged: false, ...(image_path ? { image_path } : {}) }, { onConflict: "session_id,page_no" });
  return { kind: "item", page_no: pageNo, item: item.no, status: grade ? "graded" : "read", read: compactRead(read), grade };
}

async function opGrade(db, body, user, st) {
  const s = await loadSession(db, body, user);
  if (s.status !== "open") fail(409, "이미 제출한 응시예요");
  const set = await setById(db, s.set_id);
  const pageNo = Math.round(+body.page_no || 0);
  const { data: p } = await db.from("assess_pages").select("*").eq("session_id", s.id).eq("page_no", pageNo).maybeSingle();
  if (!p || p.kind !== "item" || !p.read) fail(400, "먼저 이 쪽을 찍어 주세요");
  if (p.grade) return { page_no: pageNo, status: "graded", grade: p.grade };
  const item = (set.spec?.items || []).find((it) => +it.no === +p.item_no);
  if (!item) fail(400, "문항 정보가 없어요");
  if (!process.env.ANTHROPIC_API_KEY) fail(500, "AI 키가 설정되지 않았어요");
  const gradeModel = st.assess_model_grade || st.photo_model_grade || DEFAULT_GRADE;
  const grade = await gradeItem(gradeModel, item, p.read, policyOf(set.spec));
  await db.from("assess_pages").update({ grade, status: "graded", model_grade: gradeModel, updated_at: new Date().toISOString() }).eq("session_id", s.id).eq("page_no", pageNo);
  return { page_no: pageNo, status: "graded", grade };
}

async function opInfo(db, body, user) {
  const s = await loadSession(db, body, user);
  const set = await setById(db, s.set_id);
  const level = set.spec?.level || set.level || "mid";
  const name = normName(body.name);
  const grade = normGrade(body.grade, level) || (/^[emh]\d$/.test(String(body.grade || "")) ? String(body.grade) : null);
  const nickname = str(body.nickname, 20) || null;
  if (!name) fail(400, "이름을 확인해 주세요");
  if (!grade) fail(400, "학년을 확인해 주세요");
  const ocr = s.ocr_info || {};
  const by = normName(ocr.name) === name && normGrade(ocr.grade, level) === grade ? "ocr" : "user";
  const info = { name, grade, nickname, by, at: new Date().toISOString() };
  const key = s.user_id ? `u:${s.user_id}` : personKey({ name, grade });
  const person_id = key ? await upsertPerson(db, { key, user_id: s.user_id || null, name, grade, nickname }) : null;
  await db.from("assess_sessions").update({ info, person_id }).eq("id", s.id);
  return { info, person_id };
}

async function opFinish(db, body, user) {
  const s = await loadSession(db, body, user);
  const set = await setById(db, s.set_id);
  let pages = await pagesOf(db, s.id);
  if (s.status === "submitted") return { result: resultOf(set, s, pages) };
  if (!s.info?.name) {
    if (s.user_id) {
      const { data: p } = await db.from("profiles").select("username, name, grade").eq("id", s.user_id).maybeSingle();
      const name = normName(p?.name || p?.username);
      const info = { name: name || null, grade: null, nickname: null, by: "profile", at: new Date().toISOString() };
      const person_id = await upsertPerson(db, { key: `u:${s.user_id}`, user_id: s.user_id, name });
      await db.from("assess_sessions").update({ info, person_id }).eq("id", s.id);
      s.info = info; s.person_id = person_id;
    } else fail(400, "2쪽의 이름·학년을 먼저 확인해 주세요");
  }
  const res0 = resultOf(set, { ...s, status: "submitted" }, pages);
  const now = new Date().toISOString();
  const { data: upd, error } = await db.from("assess_sessions").update({ status: "submitted", submitted_at: now, total: res0.total, max: res0.max })
    .eq("id", s.id).eq("status", "open").select("*").maybeSingle();
  if (error) throw error;
  if (upd && s.person_id) {
    const { data: per } = await db.from("assess_people").select("n_sessions").eq("id", s.person_id).maybeSingle();
    await db.from("assess_people").update({ n_sessions: (per?.n_sessions || 0) + 1, last_seen: now }).eq("id", s.person_id);
  }
  pages = await pagesOf(db, s.id);
  return { result: resultOf(set, upd || { ...s, status: "submitted", submitted_at: now }, pages) };
}

async function opResult(db, body, user) {
  const s = await loadSession(db, body, user);
  const set = await setById(db, s.set_id);
  return { result: resultOf(set, s, await pagesOf(db, s.id)) };
}

async function opFlag(db, body, user) {
  const s = await loadSession(db, body, user);
  const pageNo = Math.round(+body.page_no || 0);
  const note = str(body.note, 300) || null;
  const { error } = await db.from("assess_pages").update({ flagged: body.off ? false : true, flag_note: body.off ? null : note }).eq("session_id", s.id).eq("page_no", pageNo);
  if (error) throw error;
  return { page_no: pageNo, flagged: !body.off };
}

async function opClaim(db, body, user) {
  if (!user) fail(401, "로그인이 필요해요");
  const s = await loadSession(db, body, null);    // 비밀값으로만
  if (s.user_id && s.user_id !== user.id) fail(409, "다른 계정에 담긴 응시예요");
  if (!s.user_id) await db.from("assess_sessions").update({ user_id: user.id }).eq("id", s.id);
  if (s.person_id) {
    const { data: per } = await db.from("assess_people").select("id, user_id").eq("id", s.person_id).maybeSingle();
    if (per && !per.user_id) await db.from("assess_people").update({ user_id: user.id }).eq("id", per.id);
  }
  return { sid: s.id, claimed: true };
}

async function opList(db, body, user) {
  const nowIso = new Date().toISOString();
  const { data: sets, error } = await db.from("assess_sets").select("id, code, title, level, grade_label, test_date, n_items, opens_at, closes_at, status, created_at")
    .eq("status", "live").order("created_at", { ascending: false }).limit(30);
  if (error) { if (missingRel(error)) return { open: [], mine: [], ready: false }; throw error; }
  const open = (sets || []).filter((x) => openState(x) === "open")
    .map((x) => ({ code: x.code, title: x.title, level: x.level, grade_label: x.grade_label, date: x.test_date, n_items: x.n_items, closes_at: x.closes_at, created_at: x.created_at }));
  let mine = [];
  let q = null;
  if (user) q = db.from("assess_sessions").select("id, set_id, status, total, max, started_at, submitted_at").eq("user_id", user.id);
  else if (str(body.device, 80)) q = db.from("assess_sessions").select("id, set_id, status, total, max, started_at, submitted_at").eq("device_hash", hash("dev:" + str(body.device, 80)));
  if (q) {
    const { data: ss } = await q.order("started_at", { ascending: false }).limit(30);
    const ids = [...new Set((ss || []).map((x) => x.set_id))];
    const codes = {};
    if (ids.length) {
      const { data: rows } = await db.from("assess_sets").select("id, code, title").in("id", ids);
      for (const r of rows || []) codes[r.id] = r;
    }
    mine = (ss || []).map((x) => ({ sid: x.id, code: codes[x.set_id]?.code || null, title: codes[x.set_id]?.title || "", status: x.status, total: x.total, max: x.max, started_at: x.started_at, submitted_at: x.submitted_at }));
  }
  return { open, mine, ready: true, now: nowIso };
}

// ─────────────────────────────────────────────────────────────── 관리자 op
async function requireAdmin(db, user) {
  if (!user) fail(401, "로그인이 필요해요");
  const { data: p } = await db.from("profiles").select("role").eq("id", user.id).maybeSingle();
  if (p?.role !== "admin") fail(403, "관리자만 할 수 있어요");
}

async function opAdminRegister(db, body, user) {
  let spec = body.spec;
  let raw = null;
  if (typeof spec === "string") { raw = spec; try { spec = JSON.parse(spec); } catch { fail(400, "JSON 을 읽지 못했어요"); } }
  raw = raw || JSON.stringify(spec || null);
  if (raw.length > MAX_SPEC_CHARS) fail(413, "JSON 이 너무 커요");
  const v = validateSpec(spec, { bytes: Buffer.byteLength(raw) });
  if (!v.ok) fail(400, "JSON 검사에서 걸렸어요", { errors: v.errors, warnings: v.warnings });
  const { data: ex, error: e0 } = await db.from("assess_sets").select("id, status").eq("code", spec.code).maybeSingle();
  if (e0) { if (missingRel(e0)) fail(503, "DB 설정(마이그레이션 2026-10_assess.sql)을 먼저 해 주세요"); throw e0; }
  if (ex) {
    const { count } = await db.from("assess_sessions").select("*", { count: "exact", head: true }).eq("set_id", ex.id);
    if ((count ?? 0) > 0 && !body.overwrite) fail(409, `이미 응시 기록 ${count}건이 있는 평가예요 — 덮어쓰면 채점 기준이 바뀌어요`, { sessions: count });
  }
  const row = {
    code: spec.code, title: spec.title, level: spec.level || null, grade_label: spec.grade_label || null, test_date: spec.date || null,
    status: ex?.status || (body.status === "draft" ? "draft" : "live"), opens_at: spec.opens_at || null, closes_at: spec.closes_at || null,
    reveal: spec.reveal || "after_close", n_items: spec.items.length, n_pages: spec.pages.length, spec, updated_at: new Date().toISOString(),
    ...(ex ? {} : { created_by: user.id }),
  };
  const { data, error } = await db.from("assess_sets").upsert(row, { onConflict: "code" }).select("id, code, status").single();
  if (error) throw error;
  return { set: data, summary: v.summary, warnings: v.warnings, updated: !!ex };
}

async function opAdminSets(db) {
  const { data: sets, error } = await db.from("assess_sets").select("id, code, title, level, grade_label, test_date, status, reveal, opens_at, closes_at, n_items, n_pages, created_at, updated_at")
    .order("created_at", { ascending: false }).limit(200);
  if (error) { if (missingRel(error)) return { sets: [], ready: false }; throw error; }
  const ids = (sets || []).map((x) => x.id);
  const stats = {};
  if (ids.length) {
    const { data: ss } = await db.from("assess_sessions").select("set_id, status, total, max").in("set_id", ids).limit(10000);
    for (const x of ss || []) {
      const o = stats[x.set_id] || (stats[x.set_id] = { n: 0, done: 0, sum: 0, max: 0 });
      o.n++;
      if (x.status === "submitted") { o.done++; o.sum += +x.total || 0; o.max = +x.max || o.max; }
    }
  }
  return { ready: true, sets: (sets || []).map((x) => ({ ...x, state: openState(x), sessions: stats[x.id]?.n || 0, submitted: stats[x.id]?.done || 0,
    avg: stats[x.id]?.done ? Math.round((stats[x.id].sum / stats[x.id].done) * 10) / 10 : null, max: stats[x.id]?.max || null })) };
}

async function opAdminUpdate(db, body) {
  const set = await setByCodeAny(db, body.code);
  const patch = { updated_at: new Date().toISOString() };
  if (body.status != null) { if (!["draft", "live", "closed"].includes(body.status)) fail(400, "status 가 이상해요"); patch.status = body.status; }
  if (body.reveal != null) { if (!["after_submit", "after_close", "never"].includes(body.reveal)) fail(400, "reveal 이 이상해요"); patch.reveal = body.reveal; }
  for (const k of ["opens_at", "closes_at"]) if (k in body) { if (body[k] && Number.isNaN(Date.parse(body[k]))) fail(400, `${k} 형식`); patch[k] = body[k] || null; }
  const { error } = await db.from("assess_sets").update(patch).eq("id", set.id);
  if (error) throw error;
  return { code: set.code, ...patch };
}
async function setByCodeAny(db, code) {
  const c = String(code || "").toUpperCase();
  const { data, error } = await db.from("assess_sets").select("*").eq("code", c).maybeSingle();
  if (error) throw error;
  if (!data) fail(404, "평가를 찾을 수 없어요");
  return data;
}

async function opAdminSessions(db, body) {
  const set = await setByCodeAny(db, body.code);
  const { data: ss, error } = await db.from("assess_sessions").select("id, person_id, user_id, status, info, ocr_info, total, max, started_at, submitted_at")
    .eq("set_id", set.id).order("started_at", { ascending: false }).limit(1000);
  if (error) throw error;
  const sids = (ss || []).map((x) => x.id);
  const pidx = {};
  if (sids.length) {
    const { data: pg } = await db.from("assess_pages").select("session_id, page_no, kind, item_no, status, flagged, attempts").in("session_id", sids).limit(20000);
    for (const p of pg || []) (pidx[p.session_id] = pidx[p.session_id] || []).push(p);
  }
  const persons = {};
  const pids = [...new Set((ss || []).map((x) => x.person_id).filter(Boolean))];
  if (pids.length) {
    const { data: pp } = await db.from("assess_people").select("id, person_key, name, grade, nickname, n_sessions, user_id").in("id", pids);
    for (const p of pp || []) persons[p.id] = p;
  }
  return {
    set: { code: set.code, title: set.title, n_pages: set.n_pages, n_items: set.n_items },
    sessions: (ss || []).map((x) => ({
      sid: x.id, status: x.status, total: x.total, max: x.max, started_at: x.started_at, submitted_at: x.submitted_at, login: !!x.user_id,
      info: x.info || null, ocr_name: x.ocr_info?.name || null, person: persons[x.person_id] || null,
      pages: (pidx[x.id] || []).sort((a, b) => a.page_no - b.page_no).map((p) => ({ no: p.page_no, kind: p.kind, status: p.status, flagged: !!p.flagged, attempts: p.attempts })),
    })),
  };
}

async function opAdminSession(db, body) {
  if (!UUID_RE.test(String(body.sid || ""))) fail(400, "sid");
  const { data: s, error } = await db.from("assess_sessions").select("*").eq("id", body.sid).maybeSingle();
  if (error) throw error;
  if (!s) fail(404, "응시 기록이 없어요");
  const set = await setById(db, s.set_id);
  const pages = await pagesOf(db, s.id);
  const out = [];
  for (const p of pages) {
    let image_url = null;
    if (p.image_path) {
      const { data } = await db.storage.from("assess-pages").createSignedUrl(p.image_path, 600);
      image_url = data?.signedUrl || null;
    }
    out.push({ no: p.page_no, kind: p.kind, item: p.item_no, status: p.status, attempts: p.attempts, quality: p.quality, read: p.read, grade: p.grade,
      flagged: !!p.flagged, flag_note: p.flag_note, model_read: p.model_read, model_grade: p.model_grade, image_url, updated_at: p.updated_at });
  }
  return { session: { sid: s.id, status: s.status, info: s.info, ocr_info: s.ocr_info, total: s.total, max: s.max, started_at: s.started_at, submitted_at: s.submitted_at, login: !!s.user_id },
    set: { code: set.code, title: set.title }, pages: out, result: resultOf(set, s, pages) };
}

async function opAdminExport(db, body) {
  const set = await setByCodeAny(db, body.code);
  const { data: ss } = await db.from("assess_sessions").select("id, person_id, user_id, status, info, ocr_info, total, max, started_at, submitted_at").eq("set_id", set.id).limit(2000);
  const sids = (ss || []).map((x) => x.id);
  const pages = {};
  if (sids.length) {
    const { data: pg } = await db.from("assess_pages").select("session_id, page_no, kind, item_no, status, attempts, quality, read, grade, flagged, flag_note, model_read, model_grade, image_path").in("session_id", sids).limit(30000);
    for (const p of pg || []) (pages[p.session_id] = pages[p.session_id] || []).push(p);
  }
  return { exported_at: new Date().toISOString(), set: { code: set.code, title: set.title, test_date: set.test_date, level: set.level, grade_label: set.grade_label },
    sessions: (ss || []).map((x) => ({ ...x, login: !!x.user_id, user_id: undefined, pages: (pages[x.id] || []).sort((a, b) => a.page_no - b.page_no) })) };
}

// ─────────────────────────────────────────────────────────────── 핸들러
export async function assessHandler(req, res) {
  const t0 = Date.now();
  try {
    const body = req.body || {};
    const op = String(body.op || "");
    const db = svc();
    if (!db) return res.status(500).json({ error: "Supabase 환경변수가 없어요" });
    const user = await userOf(db, req);
    const needSt = ["get", "start", "page", "grade"].includes(op);
    const st = needSt ? await settings(db) : null;
    let out;
    switch (op) {
      case "list": out = await opList(db, body, user); break;
      case "get": out = await opGet(db, body, user, st); break;
      case "start": out = await opStart(req, db, body, user, st); break;
      case "page": out = await opPage(req, db, body, user, st, t0); break;
      case "grade": out = await opGrade(db, body, user, st); break;
      case "info": out = await opInfo(db, body, user); break;
      case "finish": out = await opFinish(db, body, user); break;
      case "result": out = await opResult(db, body, user); break;
      case "flag": out = await opFlag(db, body, user); break;
      case "claim": out = await opClaim(db, body, user); break;
      case "admin_register": await requireAdmin(db, user); out = await opAdminRegister(db, body, user); break;
      case "admin_sets": await requireAdmin(db, user); out = await opAdminSets(db); break;
      case "admin_update": await requireAdmin(db, user); out = await opAdminUpdate(db, body); break;
      case "admin_sessions": await requireAdmin(db, user); out = await opAdminSessions(db, body); break;
      case "admin_session": await requireAdmin(db, user); out = await opAdminSession(db, body); break;
      case "admin_export": await requireAdmin(db, user); out = await opAdminExport(db, body); break;
      default: return res.status(400).json({ error: "알 수 없는 op: " + op });
    }
    return res.status(200).json(out);
  } catch (err) {
    if (err instanceof HttpError) return res.status(err.status).json({ error: err.message, ...(err.extra || {}) });
    const m = String(err?.message || "");
    if (missingRel(err)) return res.status(503).json({ error: "서술형 평가가 아직 준비되지 않았어요(DB 설정 전)" });
    return res.status(500).json({ error: /^AI /.test(m) ? m : "서버 오류가 났어요 — 잠시 뒤 다시 시도해 주세요" });
  }
}
