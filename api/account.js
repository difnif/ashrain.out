// api/account.js — raindrop 계정 흐름
// POST { action, ... }
//  check-username  : { username } → { available }
//  reserve  (v2)   : { username, email, minor, phone_token?(signup·성인 필수), member_code?(선택) }
//                    → { reserve_token, role_type?, academy_name? }  (이후 클라이언트가 supabase.auth.signUp 호출)
//                    → 409 { merge_required, existing } = 전화번호 겹침 → 통합 플로우로
//                    · 만 14세 미만(minor)은 전화 인증 없이 가입 → 보호자 동의(#/guardian)로 해금
//                    · 고유번호는 선택 — 없으면 student로 가입, AI 기능만 잠김
//  finalize (v2)   : (JWT) { signup_token } → { done }  이메일 인증 후 첫 로그인 시 1회 호출:
//                    예약된 전화·고유번호를 프로필에 반영하고 member_codes를 used 처리
//  login           : { username(또는 이메일), password } → { session }
//  find-id         : { phone_token(find) } → { accounts: [...] }
//  reset-pw        : { phone_token(reset), username, new_password } → { done }
//  social-complete : (JWT 필요) { phone_token(social), member_code, nickname? } → { done, role }
//  trial-start     : { member_code(유형9) } → { email, password, expires_at }  (클라이언트가 즉시 로그인)
//  contact-otp-send: (JWT) { kind:'phone'|'email', target } → { sent }   연락처 변경용 인증번호
//  contact-change  : (JWT) { kind, target, code } → { done, kind, target }  인증 확인 + 즉시 반영

import {
  admin, anon, getUser, bad, json, clientIp,
  verifyToken, randToken, randPassword,
  normCode, quickCheck, verifyCode, ROLE_MAP,
  normPhone, sha, randCode6, sendSMS, sendEmail,
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

    // ---------------- 가입 예약 (v2: 전화·고유번호 선택화) ----------------
    if (action === 'reserve') {
      const minor = req.body.minor === true;
      const vt = phoneTok(req.body, 'signup');
      if (!minor && !vt) return bad(res, '전화번호 인증이 만료되었습니다. 다시 인증해주세요', 401);

      const username = String(req.body.username || '').toLowerCase();
      const email = String(req.body.email || '').trim().toLowerCase();
      if (!USERNAME_RE.test(username)) return bad(res, '아이디는 영문 소문자/숫자/_ 4~20자입니다');
      if (!EMAIL_RE.test(email)) return bad(res, '이메일 형식이 올바르지 않습니다');

      const { data: dupU } = await db.from('profiles').select('id').eq('username', username).limit(1);
      if (dupU?.length) return bad(res, '이미 사용 중인 아이디입니다');

      // 전화번호 겹침 → 통합 필수 (관리자 계정은 면제) — 전화 인증을 한 경우에만
      if (vt) {
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
      }

      // 고유번호 — 선택. 있으면 검증·선점, 없으면 건너뜀(AI 기능만 잠김)
      const reserve_token = randToken();
      let chk = null;
      if (String(req.body.member_code || '').trim()) {
        chk = await loadValidCode(db, req.body.member_code);
        if (chk.err) return bad(res, chk.err);
        const { data: upd, error } = await db.from('member_codes')
          .update({
            status: 'reserved',
            reserve_token,
            reserved_phone: vt?.phone || null,
            reserved_at: new Date().toISOString(),
          })
          .eq('code', chk.row.code)
          .in('status', ['issued', 'reserved'])
          .select('code');
        if (error || !upd?.length) return bad(res, '예약에 실패했습니다. 다시 시도해주세요', 409);
      }

      // 예약 기록 — 이메일 인증 후 첫 로그인(finalize)에서 프로필에 반영
      const { error: rsvErr } = await db.from('signup_reservations').insert({
        token: reserve_token,
        phone: vt?.phone || null,
        phone_verified: !!vt,
        minor,
        member_code: chk?.row.code || null,
      });
      if (rsvErr) return bad(res, 'DB 오류: ' + rsvErr.message + ' — 2026-08_signup_v2.sql 실행 여부를 확인해주세요', 500);

      return json(res, 200, {
        reserve_token,
        role_type: chk ? chk.row.role_type : null,
        academy_name: chk ? chk.academy.name : null,
      });
    }

    // ---------------- 가입 확정 (v2: 이메일 인증 후 첫 로그인 시 1회) ----------------
    if (action === 'finalize') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const tok = String(req.body.signup_token || '').trim();
      if (!tok) return bad(res, 'signup_token이 필요합니다');

      const { data: rsv } = await db.from('signup_reservations')
        .select('*').eq('token', tok).maybeSingle();
      if (!rsv || rsv.consumed_at) return json(res, 200, { done: true });

      const upd = { is_minor: rsv.minor, real_email: user.email || null };

      // 전화 반영 — 가입~인증 사이에 같은 번호가 다른 계정에 등록됐으면 건너뜀
      if (rsv.phone && rsv.phone_verified) {
        const { data: dup } = await db.from('profiles')
          .select('id, role').eq('phone', rsv.phone).is('merged_into', null);
        if (!(dup || []).some((x) => x.id !== user.id && x.role !== 'admin')) {
          upd.phone = rsv.phone;
          upd.phone_verified = true;
        }
      }

      // 고유번호 확정 — 예약 토큰 일치 시에만 사용 처리
      if (rsv.member_code) {
        const { data: mc } = await db.from('member_codes')
          .select('*').eq('code', rsv.member_code).maybeSingle();
        if (mc && mc.reserve_token === tok && mc.status === 'reserved') {
          upd.member_code = mc.code;
          upd.academy_code = mc.academy_code;
          upd.role = ROLE_MAP[mc.role_type] || 'student';
          await db.from('member_codes').update({
            status: 'used', assigned_user: user.id, used_at: new Date().toISOString(),
          }).eq('code', mc.code);
        }
      }

      const { error: pErr } = await db.from('profiles').update(upd).eq('id', user.id);
      if (pErr) return bad(res, '프로필 반영 실패: ' + pErr.message, 500);

      await db.from('signup_reservations')
        .update({ consumed_at: new Date().toISOString() }).eq('token', tok);

      // 3일 지난 미소비 예약 청소 — 발사 후 무시
      db.from('signup_reservations').delete()
        .is('consumed_at', null)
        .lt('created_at', new Date(Date.now() - 3 * 864e5).toISOString())
        .then(() => {}, () => {});

      return json(res, 200, { done: true });
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
    // ---------------- 연락처 변경: 인증번호 발송 (JWT) ----------------
    if (action === 'contact-otp-send') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const kind = req.body.kind === 'email' ? 'email' : req.body.kind === 'phone' ? 'phone' : null;
      if (!kind) return bad(res, '변경 대상이 올바르지 않습니다');

      let target;
      if (kind === 'phone') {
        target = normPhone(req.body.target);
        if (!target) return bad(res, '휴대폰 번호 형식이 올바르지 않습니다');
      } else {
        target = String(req.body.target || '').trim().toLowerCase();
        if (!EMAIL_RE.test(target)) return bad(res, '이메일 형식이 올바르지 않습니다');
      }

      const { data: me } = await db.from('profiles').select('phone, real_email').eq('id', user.id).maybeSingle();
      if (kind === 'phone' && me?.phone === target) return bad(res, '현재 등록된 번호와 같습니다');
      if (kind === 'email' && (me?.real_email || '').toLowerCase() === target) return bad(res, '현재 등록된 이메일과 같습니다');

      if (kind === 'phone') {
        const { data: dup } = await db.from('profiles')
          .select('id, role').eq('phone', target).is('merged_into', null);
        if ((dup || []).some((x) => x.id !== user.id && x.role !== 'admin'))
          return bad(res, '이미 다른 계정에서 사용 중인 번호입니다', 409);
      }

      const t1m = new Date(Date.now() - 60e3).toISOString();
      const t24 = new Date(Date.now() - 864e5).toISOString();
      const { count: c1 } = await db.from('contact_otp_codes')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', user.id).gte('created_at', t1m);
      if ((c1 ?? 0) >= 1) return bad(res, '잠시 후 다시 시도해주세요 (1분에 1회)', 429);
      const { count: c24 } = await db.from('contact_otp_codes')
        .select('*', { count: 'exact', head: true })
        .eq('user_id', user.id).gte('created_at', t24);
      if ((c24 ?? 0) >= 8) return bad(res, '오늘 발송 한도를 초과했습니다', 429);

      const code = randCode6();
      const { error: insErr } = await db.from('contact_otp_codes').insert({
        user_id: user.id, kind, target, ip: clientIp(req),
        code_hash: sha(code),
        expires_at: new Date(Date.now() + 5 * 60e3).toISOString(),
      });
      if (insErr) return bad(res, 'DB 오류: ' + insErr.message, 500);

      const r = kind === 'phone'
        ? await sendSMS(target, `[ashrain] 인증번호 ${code} (5분 내 입력)`)
        : await sendEmail(target, '[ashrain] 이메일 인증번호', `ashrain.out 이메일 인증번호는 ${code} 입니다. (5분 내 입력)`);
      if (!r.ok) return bad(res, (kind === 'phone' ? '문자' : '이메일') + ' 발송에 실패했습니다: ' + (r.raw?.message || '알 수 없는 오류'), 502);
      return json(res, 200, { sent: true });
    }

    // ---------------- 연락처 변경: 인증 확인 + 반영 (JWT) ----------------
    if (action === 'contact-change') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const kind = req.body.kind === 'email' ? 'email' : req.body.kind === 'phone' ? 'phone' : null;
      const code = String(req.body.code || '').trim();
      if (!kind || !/^\d{6}$/.test(code)) return bad(res, '인증번호를 다시 확인해주세요');
      const target = kind === 'phone'
        ? normPhone(req.body.target)
        : String(req.body.target || '').trim().toLowerCase();
      if (!target) return bad(res, '대상 정보가 올바르지 않습니다');

      const { data: row } = await db.from('contact_otp_codes').select('*')
        .eq('user_id', user.id).eq('kind', kind).eq('target', target).eq('used', false)
        .gte('expires_at', new Date().toISOString())
        .order('created_at', { ascending: false }).limit(1).maybeSingle();
      if (!row || row.code_hash !== sha(code)) return bad(res, '인증번호가 올바르지 않거나 만료됐습니다');

      await db.from('contact_otp_codes').update({ used: true }).eq('id', row.id);

      if (kind === 'phone') {
        const { data: dup } = await db.from('profiles')
          .select('id, role').eq('phone', target).is('merged_into', null);
        if ((dup || []).some((x) => x.id !== user.id && x.role !== 'admin'))
          return bad(res, '이미 다른 계정에서 사용 중인 번호입니다', 409);
        const { error } = await db.from('profiles').update({ phone: target, phone_verified: true }).eq('id', user.id);
        if (error) return bad(res, '변경 실패: ' + error.message, 500);
      } else {
        const { error } = await db.from('profiles').update({ real_email: target }).eq('id', user.id);
        if (error) return bad(res, '변경 실패: ' + error.message, 500);
      }
      return json(res, 200, { done: true, kind, target });
    }

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

    // ---------------- 스태프 가입 (초대코드, /#/staff-join) ----------------
    if (action === 'staff-join') {
      const vt = phoneTok(req.body, 'signup');
      if (!vt) return bad(res, '전화번호 인증이 필요합니다', 401);

      const inviteCode = String(req.body.invite_code || '').trim();
      const username = String(req.body.username || '').toLowerCase();
      const password = String(req.body.password || '');
      const email = String(req.body.email || '').trim().toLowerCase();
      const nickname = String(req.body.nickname || '').trim() || null;
      if (!inviteCode) return bad(res, '초대코드를 입력해주세요');
      if (!USERNAME_RE.test(username)) return bad(res, '아이디는 영문 소문자/숫자/_ 4~20자입니다');
      if (password.length < 8) return bad(res, '비밀번호는 8자 이상이어야 합니다');
      if (!EMAIL_RE.test(email)) return bad(res, '이메일 형식이 올바르지 않습니다');

      const { data: inv } = await db.from('staff_invites')
        .select('*').eq('code', inviteCode).maybeSingle();
      if (!inv) return bad(res, '유효하지 않은 초대코드입니다', 404);
      if (inv.used_by) return bad(res, '이미 사용된 초대코드입니다', 409);
      if (inv.expires_at && new Date(inv.expires_at) < new Date()) {
        return bad(res, '만료된 초대코드입니다', 410);
      }

      const { data: dupU } = await db.from('profiles').select('id').eq('username', username).limit(1);
      if (dupU?.length) return bad(res, '이미 사용 중인 아이디입니다');

      const { data: created, error: cErr } = await db.auth.admin.createUser({
        email, password, email_confirm: true,
        user_metadata: { username, staff: true },
      });
      if (cErr || !created?.user) {
        return bad(res, '계정 생성 실패: ' + (cErr?.message || ''), 500);
      }

      const { error: pErr } = await db.from('profiles').upsert({
        id: created.user.id,
        username, nickname,
        phone: vt.phone, phone_verified: true,
        real_email: email,
        role: inv.role || 'admin',
        academy_code: inv.academy_code || null,
      }, { onConflict: 'id' });
      if (pErr) return bad(res, '프로필 저장 실패: ' + pErr.message, 500);

      await db.from('staff_invites').update({
        used_by: created.user.id, used_at: new Date().toISOString(),
      }).eq('code', inviteCode);

      const { data: signed, error: sErr } = await anon().auth.signInWithPassword({ email, password });
      if (sErr || !signed?.session) {
        return json(res, 200, { done: true, session: null }); // 생성은 성공 — 로그인 화면에서 진행
      }
      return json(res, 200, { done: true, session: signed.session });
    }

    // ---------------- 계정 통합 신청 (로그인 상태, 관리자 처리 대기) ----------------
    if (action === 'merge-request') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const vt = verifyToken(req.body.phone_token);
      if (!vt || vt.t !== 'phone' || !['social', 'merge', 'signup'].includes(vt.purpose)) {
        return bad(res, '전화번호 인증이 필요합니다', 401);
      }

      const { data: others } = await db.from('profiles')
        .select('id, username, role').eq('phone', vt.phone).is('merged_into', null);
      const target = (others || []).find((p) => p.id !== user.id && p.role !== 'admin');
      if (!target) return bad(res, '통합 대상 계정을 찾지 못했습니다', 404);

      const { data: dup } = await db.from('merge_requests')
        .select('id').eq('merged_user', user.id).eq('primary_user', target.id)
        .eq('status', 'pending').limit(1);
      if (dup?.length) return json(res, 200, { requested: true, already: true });

      const { error } = await db.from('merge_requests').insert({
        primary_user: target.id, merged_user: user.id,
        reason: 'phone', requested_by: user.id, status: 'pending',
      });
      if (error) return bad(res, error.message, 500);
      return json(res, 200, { requested: true, target: maskName(target.username) });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
