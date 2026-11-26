// ashrain.out — 학습 기능 이용 자격 (2026-11-26)
// 원장님 결정: "회원가입이 모두 다 된 상태라면, 누구든지 승인 절차 없이" — 가입을 끝까지 마친 계정은 바로 모든 학습 기능.
//  · 관리자: 항상
//  · 체험(trial): 개념 열람만
//  · 운영자 학습 허용(learn_grants 행): 항상
//  · 만 14세 미만: 보호자 동의가 활성이면 (문자 인증 + 동의 제출 = 즉시 활성, 관리자 승인 없음)
//  · 만 14세 이상: 휴대폰 인증을 마쳤거나 아이디(이메일) 가입이면 — 소셜 가입은 온보딩(생년월일·휴대폰 인증)까지 마쳐야
// 학원 고유번호는 더 이상 AI 기능의 조건이 아니다.
// 앱 관문(App.jsx VerifyGate) · AI 관문(api/ai.js · api/photo.js) · 관리자 가입 로그가 이 한 곳을 쓴다. DOM 없음.

export function learnAccess({ role, is_minor, phone_verified, provider, guardianActive, granted } = {}) {
  if (role === "admin") return { ok: true, why: "admin" };
  if (role === "trial") return { ok: false, why: "trial" };
  if (granted) return { ok: true, why: "grant" };
  if (is_minor) return guardianActive ? { ok: true, why: "guardian" } : { ok: false, why: "need_guardian" };
  return (phone_verified || (provider || "email") === "email")
    ? { ok: true, why: "verified" } : { ok: false, why: "need_verify" };
}

export const GATE_MSG = {
  trial: "체험 계정은 개념 열람만 가능해요 — 정식 가입 후 이용할 수 있어요",
  need_guardian: "만 14세 미만은 보호자 동의를 마치면 AI 기능이 열려요",
  need_verify: "회원가입(휴대폰 인증)을 마치면 AI 기능이 열려요",
};

// 서버(API) 관문. sb 는 학생 본인 토큰으로 만든 클라이언트 — RLS 로 자기 행만 읽힌다.
// 프로필이 없거나 조회가 실패하면 열지 않는다(허용 표·보호자 표가 없으면 그 근거만 빠진다).
export async function learnGate(sb, user) {
  const uid = user?.id;
  if (!uid) return { ok: false, why: "need_verify" };
  let prof = null;
  try {
    const { data } = await sb.from("profiles").select("role, is_minor, phone_verified").eq("id", uid).maybeSingle();
    prof = data || null;
  } catch { prof = null; }
  if (!prof) return { ok: false, why: "need_verify" };
  if (prof.role === "admin" || prof.role === "trial") return { ...learnAccess(prof), prof };

  const safe = async (q) => { try { const r = await q; return r?.error ? null : r?.data; } catch { return null; } };
  const [grant, consents] = await Promise.all([
    safe(sb.from("learn_grants").select("user_id").eq("user_id", uid).maybeSingle()),
    prof.is_minor
      ? safe(sb.from("guardian_consents").select("id").eq("student_id", uid).eq("status", "active").limit(1))
      : Promise.resolve(null),
  ]);
  const r = learnAccess({
    ...prof,
    provider: user?.app_metadata?.provider,
    granted: !!grant,
    guardianActive: Array.isArray(consents) && consents.length > 0,
  });
  return { ...r, prof };
}
