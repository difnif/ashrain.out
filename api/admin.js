// api/admin.js — 관리자 전용 API (모든 action에 admin JWT 필수)
// POST { action, ... }
//  issue-codes   : { role_type, birth_year?, count, note?, academy_code? } → { codes: [...] }
//                  * 체험(9)은 출생년 자리에 발급 월이 자동 인코딩됨
//  list-codes    : { academy_code?, status?, role_type?, limit?, offset? } → { rows }
//  decode-code   : { code } → { academy, roleType, regYear, birthYear, row }
//  revoke-code   : { code } → { done }
//  find-users    : { q } → { users }
//  reset-user-pw : { user_id } → { temp_password }
//  merge-users   : { primary_user, merged_user, reason? } → { report }
//  create-invite : { role?, expires_days? } → { invite_code }
//  cleanup-trials: {} → { blocked }

import {
  admin, getUser, bad, json,
  makeCode, fmtCode, normCode, decodeCode, ROLE_MAP,
  randToken, randPassword,
} from './_lib/core.js';

async function requireAdmin(req, db) {
  const user = await getUser(req);
  if (!user) return { err: [401, '로그인이 필요합니다'] };
  const { data: prof } = await db.from('profiles')
    .select('id, role, academy_code').eq('id', user.id).maybeSingle();
  if (prof?.role !== 'admin') return { err: [403, '관리자 권한이 필요합니다'] };
  return { user, prof };
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const { action } = req.body || {};
    const db = admin();

    const g = await requireAdmin(req, db);
    if (g.err) return bad(res, g.err[1], g.err[0]);

    async function pickAcademy(bodyCode) {
      const code = bodyCode || g.prof.academy_code;
      if (code) {
        const { data } = await db.from('academies').select('*').eq('code', code).maybeSingle();
        if (data) return data;
      }
      const { data: all } = await db.from('academies').select('*').limit(2);
      if (all?.length === 1) return all[0];
      return null;
    }

    // ---------------- 코드 발급 ----------------
    if (action === 'issue-codes') {
      const roleType = +req.body.role_type;
      if (![1, 2, 3, 5, 9].includes(roleType)) return bad(res, 'role_type은 1/2/3/5/9 중 하나입니다');

      const count = Math.min(Math.max(+req.body.count || 1, 1), 200);
      const academy = await pickAcademy(req.body.academy_code);
      if (!academy) return bad(res, '학원을 지정해주세요 (academies 등록 필요)');

      const now = new Date();
      const regYear = now.getFullYear();
      const birthYear = roleType === 9
        ? 2000 + (now.getMonth() + 1)          // 체험: 발급 월 인코딩
        : (+req.body.birth_year || null);
      if (roleType === 1 && !birthYear) return bad(res, '학생 코드는 출생년도(예: 2012)가 필요합니다');

      const note = String(req.body.note || '').slice(0, 200) || null;

      const out = [];
      let guard = 0;
      while (out.length < count && guard < count * 30) {
        guard++;
        const code = makeCode({
          academy: academy.code, region: academy.region,
          roleType, regYear, birthYear,
        });
        const { error } = await db.from('member_codes').insert({
          code, academy_code: academy.code, role_type: roleType,
          reg_year: regYear, birth_year: roleType === 9 ? null : birthYear,
          key_ver: 'v1', status: 'issued', note, issued_by: g.user.id,
        });
        if (!error) out.push(fmtCode(code));
        else if (!String(error.message || '').toLowerCase().includes('duplicate')) {
          return bad(res, '발급 실패: ' + error.message, 500);
        }
        // duplicate → 재추첨 (코호트당 961조합 특성)
      }
      if (out.length < count) {
        return json(res, 200, {
          codes: out,
          warning: `요청 ${count}건 중 ${out.length}건만 발급 (해당 조합 용량 소진 임박)`,
        });
      }
      return json(res, 200, { codes: out });
    }

    // ---------------- 코드 목록 ----------------
    if (action === 'list-codes') {
      const off = +req.body.offset || 0;
      const lim = Math.min(+req.body.limit || 50, 200);
      let q = db.from('member_codes')
        .select('*').order('issued_at', { ascending: false })
        .range(off, off + lim - 1);
      if (req.body.academy_code) q = q.eq('academy_code', req.body.academy_code);
      if (req.body.status) q = q.eq('status', req.body.status);
      if (req.body.role_type) q = q.eq('role_type', +req.body.role_type);
      const { data, error } = await q;
      if (error) return bad(res, error.message, 500);
      return json(res, 200, {
        rows: (data || []).map((r) => ({ ...r, code_fmt: fmtCode(r.code) })),
      });
    }

    // ---------------- 코드 해독 ----------------
    if (action === 'decode-code') {
      const code = normCode(req.body.code);
      const { data: row } = await db.from('member_codes').select('*').eq('code', code).maybeSingle();
      const d = decodeCode(code, { ver: row?.key_ver || 'v1' });
      if (!d) return bad(res, '형식이 올바르지 않습니다');
      return json(res, 200, {
        ...d,
        role_name: ROLE_MAP[d.roleType] || '?',
        registered: !!row,
        row: row || null,
      });
    }

    // ---------------- 코드 취소 ----------------
    if (action === 'revoke-code') {
      const code = normCode(req.body.code);
      const { data, error } = await db.from('member_codes')
        .update({ status: 'revoked' })
        .eq('code', code).in('status', ['issued', 'reserved'])
        .select('code');
      if (error) return bad(res, error.message, 500);
      if (!data?.length) return bad(res, '취소할 수 없는 상태입니다 (이미 사용됨 또는 없음)');
      return json(res, 200, { done: true });
    }

    // ---------------- 유저 검색 ----------------
    if (action === 'find-users') {
      const q = String(req.body.q || '').trim();
      if (q.length < 2) return bad(res, '검색어는 2자 이상');
      const like = `%${q}%`;
      const { data, error } = await db.from('profiles')
        .select('id, username, nickname, role, phone, real_email, member_code, academy_code, trial_expires_at, merged_into')
        .or(`username.ilike.${like},nickname.ilike.${like},phone.ilike.${like}`)
        .limit(30);
      if (error) return bad(res, error.message, 500);
      return json(res, 200, { users: data || [] });
    }

    // ---------------- 임시 비밀번호 ----------------
    if (action === 'reset-user-pw') {
      const uid = String(req.body.user_id || '');
      if (!uid) return bad(res, 'user_id 필요');
      const temp = randPassword(10);
      const { error } = await db.auth.admin.updateUserById(uid, { password: temp });
      if (error) return bad(res, '변경 실패: ' + error.message, 500);
      return json(res, 200, { temp_password: temp });
    }

    // ---------------- 계정 통합 실행 ----------------
    if (action === 'merge-users') {
      const pFrom = String(req.body.merged_user || '');
      const pTo = String(req.body.primary_user || '');
      if (!pFrom || !pTo || pFrom === pTo) return bad(res, '대상 계정 2개를 확인해주세요');

      const { data: fromProf } = await db.from('profiles').select('id, role').eq('id', pFrom).maybeSingle();
      const { data: toProf } = await db.from('profiles').select('id, role').eq('id', pTo).maybeSingle();
      if (!fromProf || !toProf) return bad(res, '계정을 찾을 수 없습니다', 404);
      if (fromProf.role === 'admin') return bad(res, '관리자 계정은 흡수 대상이 될 수 없습니다');

      const { data: report, error: mErr } = await db.rpc('migrate_user_data', {
        p_from: pFrom, p_to: pTo,
      });
      if (mErr) return bad(res, '이관 실패: ' + mErr.message, 500);

      const { error: bErr } = await db.auth.admin.updateUserById(pFrom, {
        ban_duration: '87600h', // 10년
      });
      if (bErr) return bad(res, '이관 완료·차단 실패: ' + bErr.message, 500);

      await db.from('merge_requests').insert({
        primary_user: pTo, merged_user: pFrom,
        reason: String(req.body.reason || 'manual'),
        status: 'done', requested_by: g.user.id,
        completed_at: new Date().toISOString(),
        detail: JSON.stringify(report || []),
      });

      return json(res, 200, { report });
    }

    // ---------------- 스태프 초대코드 ----------------
    if (action === 'create-invite') {
      const role = ['admin', 'assistant'].includes(req.body.role) ? req.body.role : 'admin';
      const days = Math.min(Math.max(+req.body.expires_days || 7, 1), 30);
      const invite = randToken(9);
      const { error } = await db.from('staff_invites').insert({
        code: invite, role,
        academy_code: g.prof.academy_code || null,
        created_by: g.user.id,
        expires_at: new Date(Date.now() + days * 864e5).toISOString(),
      });
      if (error) return bad(res, error.message, 500);
      return json(res, 200, { invite_code: invite, role, expires_days: days });
    }

    // ---------------- 만료 체험계정 정리 ----------------
    if (action === 'cleanup-trials') {
      const { data: expired } = await db.from('profiles')
        .select('id').eq('role', 'trial')
        .lt('trial_expires_at', new Date().toISOString());
      let blocked = 0;
      for (const p of expired || []) {
        const { error } = await db.auth.admin.updateUserById(p.id, { ban_duration: '87600h' });
        if (!error) blocked++;
      }
      return json(res, 200, { blocked });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
