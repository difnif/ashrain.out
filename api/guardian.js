// api/guardian.js — 법정대리인(보호자) 동의 제출 (v1.0)
// POST { action: 'submit', phone_token, guardian_name, relation, guardian_birth_year }
//   · 로그인(학생) JWT 필요. phone_token은 /api/otp (purpose: 'guardian') 인증으로 발급.
//   · 보호자 정보는 인증+동의가 완료된 이 시점에만 저장 → 미동의 개인정보를 보관하지 않음.
//   · 저장 상태는 'pending'(강사 확인 대기). 승인·반려는 관리자 화면에서 RLS로 직접.
//   · 반려(rejected) 후 5일 경과 건은 호출 시마다 자동 파기(동의 미확인 정보 파기 의무).
// 조회·철회는 클라이언트가 guardian_consents에 RLS로 직접 수행하므로 API가 필요 없음.

import { admin, bad, json, getUser, verifyToken, normPhone } from './_lib/core.js';

const CONSENT_VERSION = 'v1.0';
const RELATIONS = new Set(['모', '부', '조부모', '기타']);

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const user = await getUser(req);
    if (!user) return bad(res, '로그인이 필요합니다', 401);
    const b = req.body || {};
    if (b.action !== 'submit') return bad(res, 'unknown action');

    // 1) 보호자 휴대폰 인증 토큰 검증
    const tk = verifyToken(b.phone_token);
    if (!tk || tk.t !== 'phone' || tk.purpose !== 'guardian')
      return bad(res, '보호자 휴대폰 인증을 먼저 완료해주세요', 401);
    const phone = normPhone(tk.phone);
    if (!phone) return bad(res, '인증된 번호가 올바르지 않습니다');

    // 2) 입력 검증
    const name = String(b.guardian_name || '').trim();
    const relation = RELATIONS.has(b.relation) ? b.relation : '기타';
    const gby = parseInt(b.guardian_birth_year, 10) || null;
    const nowY = new Date().getFullYear();
    if (name.length < 2 || name.length > 20)
      return bad(res, '보호자 성명을 정확히 입력해주세요');
    if (!gby || gby < nowY - 100 || gby > nowY - 19)
      return bad(res, '보호자 출생연도가 올바르지 않습니다 — 성인만 법정대리인이 될 수 있어요');

    const db = admin();

    // 3) 나이 간극 점검 (학생과 16년 미만 차이면 강사 확인용 경고 플래그)
    const { data: prof } = await db.from('profiles')
      .select('birth_year').eq('id', user.id).maybeSingle();
    const sby = prof?.birth_year || null;
    const age_gap_warn = !!(sby && sby - gby < 16);

    // 4) 이미 활성인 동일 (학생, 보호자번호)면 덮어쓰지 않음
    const { data: ex } = await db.from('guardian_consents')
      .select('id, status').eq('student_id', user.id).eq('guardian_phone', phone).maybeSingle();
    if (ex?.status === 'active')
      return json(res, 200, { consent: ex, already: true });

    // 5) 저장 (재제출이면 pending으로 갱신)
    const now = new Date().toISOString();
    const row = {
      student_id: user.id,
      guardian_name: name,
      guardian_phone: phone,
      guardian_birth_year: gby,
      relation,
      consent_version: CONSENT_VERSION,
      consented_at: now,
      status: 'pending',
      age_gap_warn,
      approved_by: null,
      approved_at: null,
      reject_reason: null,
      updated_at: now,
    };
    const { data, error } = await db.from('guardian_consents')
      .upsert(row, { onConflict: 'student_id,guardian_phone' })
      .select().single();
    if (error) return bad(res, 'DB 오류: ' + error.message, 500);

    // 6) 반려 후 5일 경과 건 파기 — 발사 후 무시
    db.from('guardian_consents').delete()
      .eq('status', 'rejected')
      .lt('updated_at', new Date(Date.now() - 5 * 864e5).toISOString())
      .then(() => {}, () => {});

    return json(res, 200, { consent: data, age_gap_warn });
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
