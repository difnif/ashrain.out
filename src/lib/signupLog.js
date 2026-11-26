// ashrain.out — 관리자 가입 로그 표시 (#/admin/signups). DOM 없음 — tests/signupLog.test.mjs
// 입력은 DB 함수 admin_signup_log() 의 행. 시각은 모두 한국 시간(KST)으로, 분까지.
import { learnAccess } from "./learnAccess.js";

const KST = "Asia/Seoul";
export const PROVIDER = { email: "아이디", google: "구글", kakao: "카카오" };

const FMT = new Intl.DateTimeFormat("ko-KR", {
  timeZone: KST, year: "numeric", month: "2-digit", day: "2-digit", weekday: "short",
  hour: "2-digit", minute: "2-digit", hourCycle: "h23",
});

// → { day: "2026-11-26", weekday: "목", time: "18:53", full: "2026-11-26 (목) 18:53" }
export function kstStamp(iso) {
  const d = new Date(iso);
  if (!iso || isNaN(d)) return { day: "", weekday: "", time: "", full: "" };
  const p = Object.fromEntries(FMT.formatToParts(d).map((x) => [x.type, x.value]));
  const day = `${p.year}-${p.month}-${p.day}`;
  const time = `${p.hour}:${p.minute}`;
  return { day, weekday: p.weekday, time, full: `${day} (${p.weekday}) ${time}` };
}

export function ageLabel(r) {
  if (Number.isInteger(r?.age)) return `만 ${r.age}세` + (r.birth_year ? ` (${r.birth_year}년생)` : "");
  if (r?.birth_year) return `${r.birth_year}년생`;
  return "나이 미입력";
}

// 이용 상태 — 앱 관문과 같은 규칙(learnAccess)
export function signupState(r) {
  if (r?.merged) return { key: "merged", label: "통합된 계정", ok: false };
  if (r?.role === "trial") return { key: "trial", label: "체험", ok: false };
  const a = learnAccess({
    role: r?.role, is_minor: r?.is_minor, phone_verified: r?.phone_verified, provider: r?.provider,
    guardianActive: r?.guardian_status === "active", granted: r?.granted,
  });
  if (a.ok) return { key: "ok", label: "이용 중", ok: true };
  if (a.why === "need_guardian") {
    const label = r?.guardian_status === "pending" ? "보호자 동의 확인 대기"
      : r?.guardian_status === "rejected" ? "보호자 동의 반려" : "보호자 동의 전";
    return { key: "guardian", label, ok: false };
  }
  return { key: "verify", label: r?.onboarded ? "휴대폰 인증 전" : "가입 마무리 전", ok: false };
}

export function buildSignupLog(rows, now = new Date()) {
  const today = kstStamp(now.toISOString()).day;
  const yday = kstStamp(new Date(now.getTime() - 864e5).toISOString()).day;
  const weekAgo = now.getTime() - 7 * 864e5;
  const items = (rows || []).map((r) => {
    const t = kstStamp(r.signed_up_at);
    const g = r.guardian_at ? kstStamp(r.guardian_at) : null;
    return {
      id: r.user_id,
      ts: new Date(r.signed_up_at).getTime() || 0,
      day: t.day, weekday: t.weekday, time: t.time, full: t.full,
      name: r.name || "(이름 없음)",
      nickname: r.nickname || "",
      username: r.username || "",
      provider: PROVIDER[r.provider] || r.provider || "",
      age: ageLabel(r),
      minor: !!r.is_minor,
      guardianAt: g ? (g.day === t.day ? g.time : g.full) : "",
      guardianWarn: !!r.guardian_warn,
      state: signupState(r),
    };
  }).sort((a, b) => b.ts - a.ts);

  const groups = [];
  for (const it of items) {
    let g = groups[groups.length - 1];
    if (!g || g.day !== it.day) {
      const label = it.day === today ? `오늘 · ${it.day} (${it.weekday})`
        : it.day === yday ? `어제 · ${it.day} (${it.weekday})` : `${it.day} (${it.weekday})`;
      g = { day: it.day, label, items: [] };
      groups.push(g);
    }
    g.items.push(it);
  }
  const counts = {
    total: items.length,
    today: items.filter((i) => i.day === today).length,
    week: items.filter((i) => i.ts >= weekAgo).length,
    notReady: items.filter((i) => !i.state.ok).length,
  };
  return { groups, counts, items };
}
