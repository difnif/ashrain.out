// api/account.js — raindrop 계정 흐름
// POST { action, ... }
//  check-username  : { username } → { available }
//  reserve         : { phone_token(signup), member_code, username, email }
//                    → { reserve_token, role_type }  (이후 클라이언트가 supabase.auth.signUp 호출)
//                    → 409 { merge_required, existing } = 전화번호 겹침 → 통합 플로우로
//  login           : { username(또는 이메일), password } → { session }
//  find-id         : { phone_token(find) } → { accounts: [...] }
//  reset-pw        : { phone_token(reset), username, new_password } → { done }
//  social-complete : (JWT 필요) { phone_token(social), member_code, nickname? } → { done, role }
//  trial-start     : { member_code(유형9) } → { email, password, expires_at }  (클라이언트가 즉시 로그인)

import {
  admin, anon, getUser, bad, json, clientIp,
  verifyToken, randToken, randPassword,
  normCode, quickCheck, verifyCode, ROLE_MAP,
} from './_lib/core.js';

const USERNAME_RE = /^[a-z0-9_]{4,20}$/;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const maskName = (s) => {
  const v = String(s || '');
  return v.length <= 2 ? v[0] + '*' : v.slice(0, 2) + '*'.repeat(Math.max(1, v.length - 2));
};
const maskEmail = (e) => {
  const [a, b] = String(e || '').split('@');
  if (!b) return '';
  return (a.length <= 2 ? a[0] + '*' : a.slice(0, 3) + '***') + '@' + b;
};

function phoneTok(body, purpose) {
  const v = verifyToken(body.phone_token);
  return v && v.t === 'phone' && v.purpose === purpose ? v : null;
}

// member_code 검증 공통: 형식 → DB(issued) → 서명. 성공 시 { row, academy } 반환
async function loadValidCode(db, rawCode, { allowTrial = false } = {}) {
  const code = normCode(rawCode);
  if (!quickCheck(code)) return { err: '고유번호를 다시 확인해주세요 (형식/오타)' };

  const { data: row } = await db.from('member_codes').select('*').eq('code', code).maybeSingle();
  if (!row) return { err: '등록되지 않은 고유번호입니다' };
  if (row.status === 'used') return { err: '이미 사용된 고유번호입니다' };
  if (row.status === 'revoked') return { err: '사용이 중지된 고유번호입니다' };
  if (row.status === 'reserved') {
    const stale = !row.reserved_at || new Date(row.reserved_at) < new Date(Date.now() - 30 * 60e3);
    if (!stale) return { err: '다른 기기에서 가입 진행 중인 번호입니다. 30분 후 다시 시도해주세요' };
  }

  const { data: academy } = await db.from('academies').select('*').eq('code', row.academy_code).maybeSingle();
  if (!academy) return { err: '학원 정보를 찾을 수 없습니다. 학원에 문의해주세요' };

  const v = verifyCode(code, { region: academy.region, ver: row.key_ver || 'v1' });
  if (!v.ok) return { err: '고유번호 검증에 실패했습니다. 학원에 문의해주세요' };

  if (!allowTrial && row.role_type === 9) {
    return { err: '체험 코드입니다. 로그인 화면의 [체험으로 시작]을 이용해주세요' };
  }
  if (allowTrial && row.role_type !== 9) {
    return { err: '체험 코드가 아닙니다. 일반 가입을 이용해주세요' };
  }
  return { row, academy };
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const { action } = req.body || {};
    const db = admin();
    const ip = clientIp(req);

    // ---------------- 아이디 중복 확인 ----------------
    if (action === 'check-username') {
      const u = String(req.body.username || '').toLowerCase();
      if (!USERNAME_RE.test(u)) return json(res, 200, { available: false, why: 'format' });
      const { data } = await db.from('profiles').select('id').eq('username', u).limit(1);
      return json(res, 200, { available: !data?.length });
    }

    // ---------------- 가입 예약 ----------------
    if (action === 'reserve') {
      const vt = phoneTok(req.body, 'signup');
      if (!vt) return bad(res, '전화번호 인증이 만료되었습니다. 다시 인증해주세요', 401);

      const username = String(req.body.username || '').toLowerCase();
      const email = String(req.body.email || '').trim().toLowerCase();
      if (!USERNAME_RE.test(username)) return bad(res, '아이디는 영문 소문자/숫자/_ 4~20자입니다');
      if (!EMAIL_RE.test(email)) return bad(res, '이메일 형식이 올바르지 않습니다');

      const { data: dupU } = await db.from('profiles').select('id').eq('username', username).limit(1);
      if (dupU?.length) return bad(res, '이미 사용 중인 아이디입니다');

      // 전화번호 겹침 → 통합 필수 (관리자 계정은 면제)
      const { data: dupP } = await db.from('profiles')
        .select('id, username, role, merged_into')
        .eq('phone', vt.phone).is('merged_into', null);
      const clash = (dupP || []).find((p) => p.role !== 'admin');
      if (clash) {
        return json(res, 409, {
          merge_required: true,
          reason: 'phone',
          existing: { username: maskName(clash.username) },
          message: '이 전화번호로 가입된 계정이 있습니다. 계정 통합 후 이용해주세요.',
        });
      }

      const chk = await loadValidCode(db, req.body.member_code);
      if (chk.err) return bad(res, chk.err);

      const reserve_token = randToken();
      const { data: upd, error } = await db.from('member_codes')
        .update({
          status: 'reserved',
          reserve_token,
          reserved_phone: vt.phone,
          reserved_at: new Date().toISOString(),
        })
        .eq('code', chk.row.code)
        .in('status', ['issued', 'reserved'])
        .select('code');
      if (error || !upd?.length) return bad(res, '예약에 실패했습니다. 다시 시도해주세요', 409);

      return json(res, 200, {
        reserve_token,
        role_type: chk.row.role_type,
        academy_name: chk.academy.name,
      });
    }

    // ---------------- 로그인 (아이디 or 이메일) ----------------
    if (action === 'login') {
      const idRaw = String(req.body.username || '').trim();
      const password = String(req.body.password || '');
      if (!idRaw || !password) return bad(res, '아이디와 비밀번호를 입력해주세요');

      // 레이트리밋: 같은 IP 15분 내 실패 10회
      if (ip) {
        const t15 = new Date(Date.now() - 15 * 60e3).toISOString();
        const { count } = await db.from('login_attempts')
          .select('*', { count: 'exact', head: true })
          .eq('ip', ip).eq('ok', false).gte('at', t15);
        if ((count ?? 0) >= 10) return bad(res, '시도가 너무 많습니다. 15분 후 다시 시도해주세요', 429);
      }

      let email = null;
      if (idRaw.includes('@')) {
        email = idRaw.toLowerCase();
      } else {
        const { data: prof } = await db.from('profiles')
          .select('id, merged_into').eq('username', idRaw.toLowerCase()).maybeSingle();
        if (prof?.merged_into) {
          return bad(res, '통합되어 사용이 종료된 계정입니다. 통합된 계정으로 로그인해주세요', 403);
        }
        if (prof) {
          const { data: u } = await db.auth.admin.getUserById(prof.id);
          email = u?.user?.email || null;
        }
      }

      const fail = async () => {
        await db.from('login_attempts').insert({ ip, username: idRaw.toLowerCase(), ok: false });
        return bad(res, '아이디 또는 비밀번호가 일치하지 않습니다', 401);
      };
      if (!email) return fail();

      const { data: signed, error } = await anon().auth.signInWithPassword({ email, password });
      if (error || !signed?.session) return fail();

      await db.from('login_attempts').insert({ ip, username: idRaw.toLowerCase(), ok: true });
      return json(res, 200, { session: signed.session });
    }

    // ---------------- 아이디 찾기 ----------------
    if (action === 'find-id') {
      const vt = phoneTok(req.body, 'find');
      if (!vt) return bad(res, '전화번호 인증이 필요합니다', 401);

      const { data: profs } = await db.from('profiles')
        .select('id, username, nickname, real_email, role, merged_into')
        .eq('phone', vt.phone).is('merged_into', null);

      const accounts = [];
      for (const p of profs || []) {
        let providers = [];
        try {
          const { data: u } = await db.auth.admin.getUserById(p.id);
          providers = (u?.user?.identities || []).map((i) => i.provider);
        } catch { /* 무시 */ }
        accounts.push({
          username: p.username,
          nickname: p.nickname,
          email_masked: maskEmail(p.real_email),
          role: p.role,
          providers,
        });
      }
      return json(res, 200, { accounts });
    }

    // ---------------- 비밀번호 재설정 (전화 인증 기반) ----------------
    if (action === 'reset-pw') {
      const vt = phoneTok(req.body, 'reset');
      if (!vt) return bad(res, '전화번호 인증이 필요합니다', 401);

      const username = String(req.body.username || '').toLowerCase();
      const newPw = String(req.body.new_password || '');
      if (!USERNAME_RE.test(username)) return bad(res, '아이디를 확인해주세요');
      if (newPw.length < 8) return bad(res, '비밀번호는 8자 이상이어야 합니다');

      const { data: prof } = await db.from('profiles')
        .select('id, phone, phone_verified, merged_into')
        .eq('username', username).maybeSingle();
      if (!prof || prof.merged_into) return bad(res, '해당 아이디를 찾을 수 없습니다', 404);
      if (!prof.phone_verified || prof.phone !== vt.phone) {
        return bad(res, '이 계정에 등록된 전화번호가 아닙니다', 403);
      }

      const { error } = await db.auth.admin.updateUserById(prof.id, { password: newPw });
      if (error) return bad(res, '변경 실패: ' + error.message, 500);
      return json(res, 200, { done: true });
    }

    // ---------------- 소셜 가입 온보딩 완성 ----------------
    if (action === 'social-complete') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const vt = phoneTok(req.body, 'social');
      if (!vt) return bad(res, '전화번호 인증이 필요합니다', 401);

      const { data: me } = await db.from('profiles').select('*').eq('id', user.id).maybeSingle();
      if (me?.role === 'admin') return bad(res, '관리자 계정은 온보딩이 필요 없습니다');

      // 전화번호 겹침 → 통합 필수 (본인/관리자 제외)
      const { data: dupP } = await db.from('profiles')
        .select('id, username, role').eq('phone', vt.phone).is('merged_into', null);
      const clash = (dupP || []).find((p) => p.id !== user.id && p.role !== 'admin');
      if (clash) {
        return json(res, 409, {
          merge_required: true,
          reason: 'phone',
          existing: { username: maskName(clash.username) },
        });
      }

      const chk = await loadValidCode(db, req.body.member_code);
      if (chk.err) return bad(res, chk.err);

      const role = ROLE_MAP[chk.row.role_type] || 'student';
      const nickname = String(req.body.nickname || '').trim() || null;

      const { error: e1 } = await db.from('profiles').upsert({
        id: user.id,
        phone: vt.phone,
        phone_verified: true,
        real_email: user.email || null,
        member_code: chk.row.code,
        academy_code: chk.row.academy_code,
        ...(nickname ? { nickname } : {}),
        role,
      }, { onConflict: 'id' });
      if (e1) return bad(res, '프로필 저장 실패: ' + e1.message, 500);

      const { error: e2 } = await db.from('member_codes').update({
        status: 'used', assigned_user: user.id, used_at: new Date().toISOString(),
      }).eq('code', chk.row.code);
      if (e2) return bad(res, '코드 처리 실패: ' + e2.message, 500);

      return json(res, 200, { done: true, role });
    }

    // ---------------- 체험 시작 (유형 9, 24시간) ----------------
    if (action === 'trial-start') {
      const chk = await loadValidCode(db, req.body.member_code, { allowTrial: true });
      if (chk.err) return bad(res, chk.err);

      // 선점 (동시 사용 경쟁 차단)
      const { data: taken } = await db.from('member_codes')
        .update({ status: 'used', used_at: new Date().toISOString() })
        .eq('code', chk.row.code).eq('status', chk.row.status)
        .select('code');
      if (!taken?.length) return bad(res, '이미 사용된 체험 코드입니다', 409);

      const suffix = chk.row.code.slice(-6).toLowerCase();
      const email = `trial-${suffix}-${Date.now().toString(36)}@trial.ashrain.local`;
      const password = randPassword(12);
      const expires = new Date(Date.now() + 24 * 3600e3).toISOString();

      const { data: created, error } = await db.auth.admin.createUser({
        email, password, email_confirm: true,
        user_metadata: { trial: true, member_code: chk.row.code },
      });
      if (error || !created?.user) {
        // 실패 시 코드 원복
        await db.from('member_codes').update({ status: 'issued', used_at: null }).eq('code', chk.row.code);
        return bad(res, '체험 계정 생성 실패: ' + (error?.message || ''), 500);
      }

      await db.from('profiles').upsert({
        id: created.user.id,
        username: `trial_${suffix}`,
        nickname: '체험회원',
        role: 'trial',
        trial_expires_at: expires,
        member_code: chk.row.code,
        academy_code: chk.row.academy_code,
      }, { onConflict: 'id' });

      await db.from('member_codes').update({
        assigned_user: created.user.id, expires_at: expires,
      }).eq('code', chk.row.code);

      return json(res, 200, { email, password, expires_at: expires });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
