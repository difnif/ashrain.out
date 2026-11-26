// node tests/signupLog.test.mjs — 학습 이용 자격(learnAccess)과 관리자 가입 로그 표시(signupLog)
import { learnAccess, learnGate } from "../src/lib/learnAccess.js";
import { kstStamp, ageLabel, signupState, buildSignupLog } from "../src/lib/signupLog.js";

let pass = 0, fail = 0;
const ok = (c, name, extra) => {
  if (c) { pass++; console.log("ok   -", name); }
  else { fail++; console.log("FAIL -", name, extra === undefined ? "" : JSON.stringify(extra)); }
};

// ── 1) 이용 자격 — 가입을 끝까지 마쳤으면 승인 없이 ──
const A = (o) => learnAccess(o);
ok(A({ role: "admin" }).ok, "관리자 → 항상");
ok(!A({ role: "trial", phone_verified: true }).ok && A({ role: "trial" }).why === "trial", "체험 → 막힘");
ok(!A({ role: "trial", granted: true }).ok, "체험은 운영자 허용이 있어도 막힘");
ok(A({ role: "student", phone_verified: true, provider: "kakao" }).ok, "소셜 + 휴대폰 인증 → 이용");
ok(A({ role: "student", phone_verified: false, provider: "email" }).ok, "아이디(이메일) 가입 → 이용");
ok(A({ role: "student", phone_verified: false }).ok, "가입 방식을 모르면 아이디 가입으로 본다(앱과 같음)");
ok(A({ role: "student", phone_verified: false, provider: "google" }).why === "need_verify", "소셜 + 휴대폰 인증 전 → 가입 마무리 전");
ok(A({ role: "student", is_minor: true, provider: "google" }).why === "need_guardian", "14세 미만 + 보호자 동의 전 → 막힘");
ok(A({ role: "student", is_minor: true, phone_verified: true }).why === "need_guardian", "14세 미만은 휴대폰 인증이 있어도 보호자 동의가 있어야");
ok(A({ role: "student", is_minor: true, guardianActive: true }).ok, "14세 미만 + 보호자 동의 활성 → 이용");
ok(A({ role: "student", provider: "kakao", granted: true }).ok, "운영자 학습 허용 → 이용");
ok(A({ role: "teacher", phone_verified: true, provider: "kakao" }).ok, "학생 외 역할도 가입을 마쳤으면 이용");

// ── 2) 서버 관문 learnGate — 가짜 supabase 클라이언트 ──
function fakeSb({ prof, grant = false, guardian = false, missing = {} }) {
  const q = (table) => {
    const st = { table };
    const b = {
      select() { return b; }, eq() { return b; }, limit() { return b; },
      maybeSingle() { return b; },
      then(res, rej) {
        let out;
        if (missing[table]) out = { data: null, error: { code: "PGRST205", message: "no table" } };
        else if (table === "profiles") out = { data: prof, error: null };
        else if (table === "learn_grants") out = { data: grant ? { user_id: "u1" } : null, error: null };
        else if (table === "guardian_consents") out = { data: guardian ? [{ id: "g1" }] : [], error: null };
        else out = { data: null, error: { message: "unknown " + st.table } };
        return Promise.resolve(out).then(res, rej);
      },
    };
    return b;
  };
  return { from: q };
}
const U = (provider) => ({ id: "u1", app_metadata: { provider } });
let g = await learnGate(fakeSb({ prof: { role: "student", is_minor: false, phone_verified: true } }), U("kakao"));
ok(g.ok, "gate: 휴대폰 인증 마친 소셜 → 통과", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: false, phone_verified: false } }), U("kakao"));
ok(!g.ok && g.why === "need_verify", "gate: 휴대폰 인증 전 → need_verify", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: true }, guardian: true }), U("google"));
ok(g.ok && g.why === "guardian", "gate: 14세 미만 + 보호자 동의 활성 → 통과", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: true }, guardian: false }), U("google"));
ok(!g.ok && g.why === "need_guardian", "gate: 14세 미만 + 동의 없음 → need_guardian", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: true }, guardian: true, missing: { guardian_consents: true } }), U("google"));
ok(!g.ok, "gate: 보호자 표 조회 실패 → 열지 않음", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: false, phone_verified: false }, grant: true }), U("kakao"));
ok(g.ok && g.why === "grant", "gate: 운영자 허용 → 통과", g);
g = await learnGate(fakeSb({ prof: { role: "student", is_minor: false, phone_verified: false }, grant: true, missing: { learn_grants: true } }), U("kakao"));
ok(!g.ok, "gate: 허용 표가 없으면 허용 근거만 빠짐", g);
g = await learnGate(fakeSb({ prof: null }), U("email"));
ok(!g.ok, "gate: 프로필이 없으면 열지 않음", g);
g = await learnGate(fakeSb({ prof: { role: "trial" }, grant: true }), U("email"));
ok(!g.ok && g.why === "trial", "gate: 체험 → trial", g);
g = await learnGate(fakeSb({ prof: { role: "student" } }), null);
ok(!g.ok, "gate: 사용자 없음 → 열지 않음", g);

// ── 3) 한국 시간 · 분까지 ──
const s = kstStamp("2026-11-26T09:41:00Z");
ok(s.day === "2026-11-26" && s.time === "18:41" && s.weekday === "목", "UTC 09:41 → KST 18:41 (목)", s);
const mid = kstStamp("2026-11-26T15:05:00Z");
ok(mid.day === "2026-11-27" && mid.time === "00:05", "UTC 15:05 → KST 다음 날 00:05", mid);
ok(kstStamp(null).full === "" && kstStamp("이상한 값").full === "", "시각이 없거나 깨지면 빈칸");

// ── 4) 나이 · 상태 ──
ok(ageLabel({ age: 13, birth_year: 2012 }) === "만 13세 (2012년생)", "만 나이 + 출생연도");
ok(ageLabel({ age: null, birth_year: 2010 }) === "2010년생", "생년월일 없이 출생연도만");
ok(ageLabel({}) === "나이 미입력", "나이 정보 없음");
ok(ageLabel({ age: 0, birth_year: 2026 }) === "만 0세 (2026년생)", "만 0세도 숫자로");
const base = { role: "student", provider: "google", phone_verified: true, onboarded: true };
ok(signupState(base).label === "이용 중", "가입 완료 → 이용 중");
ok(signupState({ ...base, phone_verified: false, onboarded: false }).label === "가입 마무리 전", "소셜 온보딩 전 → 가입 마무리 전");
ok(signupState({ ...base, phone_verified: false }).label === "휴대폰 인증 전", "온보딩은 했는데 인증 전");
ok(signupState({ ...base, is_minor: true }).label === "보호자 동의 전", "14세 미만 동의 전");
ok(signupState({ ...base, is_minor: true, guardian_status: "pending" }).label === "보호자 동의 확인 대기", "반려됐던 번호 재제출 → 확인 대기");
ok(signupState({ ...base, is_minor: true, guardian_status: "rejected" }).label === "보호자 동의 반려", "반려됨");
ok(signupState({ ...base, is_minor: true, guardian_status: "active" }).ok, "보호자 동의 활성 → 이용 중");
ok(signupState({ ...base, role: "trial" }).key === "trial", "체험");
ok(signupState({ ...base, merged: true }).key === "merged", "통합된 계정");
ok(signupState({ ...base, phone_verified: false, onboarded: false, granted: true }).ok, "운영자 허용 → 이용 중");

// ── 5) 묶음 · 요약 ──
const now = new Date("2026-11-26T12:00:00Z"); // KST 21:00
const rows = [
  { user_id: "a", signed_up_at: "2026-11-03T08:15:00Z", name: "가나다", nickname: "가나", age: 14, birth_year: 2012, provider: "google", phone_verified: true, onboarded: true, role: "student" },
  { user_id: "b", signed_up_at: "2026-11-26T09:41:00Z", name: "라마바", nickname: "마바", age: 13, birth_year: 2013, is_minor: true, provider: "google", onboarded: true, role: "student", guardian_status: "active", guardian_at: "2026-11-26T10:02:00Z" },
  { user_id: "c", signed_up_at: "2026-11-25T14:59:00Z", name: "어제가입", nickname: null, age: null, birth_year: null, provider: "kakao", onboarded: false, role: "student" },
  { user_id: "d", signed_up_at: "2026-11-26T01:00:00Z", name: null, provider: "email", username: "kid01", role: "student", is_minor: true, guardian_status: "active", guardian_at: "2026-11-27T02:00:00Z" },
];
const L = buildSignupLog(rows, now);
ok(L.groups.length === 3, "날짜별 3묶음", L.groups.map((x) => x.label));
ok(L.groups[0].label.startsWith("오늘 · 2026-11-26"), "첫 묶음 = 오늘", L.groups[0].label);
ok(L.groups[0].items.map((i) => i.id).join() === "b,d", "오늘 묶음은 최근 순(18:41 → 10:00)", L.groups[0].items.map((i) => i.time));
ok(L.groups[1].label.startsWith("어제 · 2026-11-25"), "어제 묶음(KST 23:59 가입)", L.groups[1].label);
ok(L.groups[1].items[0].time === "23:59", "어제 23:59");
const b = L.items.find((i) => i.id === "b");
ok(b.full === "2026-11-26 (목) 18:41" && b.age === "만 13세 (2013년생)" && b.nickname === "마바" && b.provider === "구글", "한 줄: 시각·나이·닉네임·가입 방식", b);
ok(b.guardianAt === "19:02", "같은 날 보호자 동의는 시각만", b.guardianAt);
const d = L.items.find((i) => i.id === "d");
ok(d.name === "(이름 없음)" && d.username === "kid01" && d.provider === "아이디", "이름 없음 · 아이디 가입", d);
ok(d.guardianAt === "2026-11-27 (금) 11:00", "다른 날 보호자 동의는 날짜까지", d.guardianAt);
const c = L.items.find((i) => i.id === "c");
ok(c.state.label === "가입 마무리 전" && c.age === "나이 미입력", "소셜 온보딩 전", c);
ok(L.counts.total === 4 && L.counts.today === 2 && L.counts.week === 3 && L.counts.notReady === 1, "요약: 전체 4 · 오늘 2 · 7일 3(11-03 가입은 밖) · 마무리 전 1", L.counts);
ok(buildSignupLog(null, now).counts.total === 0, "빈 목록");

console.log(`\n${pass}/${pass + fail} passed`);
if (fail) process.exit(1);
