// api/otp.js — SMS 인증번호 발송/검증
// POST { action: 'send'|'verify', ... }
//   send   : { phone, purpose }            → { sent: true }
//   verify : { phone, purpose, code }      → { phone_token }   (15분 유효)
// purpose: signup(가입) / find(아이디찾기) / reset(비번재설정) / merge(통합) / social(소셜 온보딩)

import {
  admin, bad, json, clientIp, normPhone,
  sha, randCode6, sendSMS, signToken,
} from './_lib/core.js';

const PURPOSES = new Set(['signup', 'find', 'reset', 'merge', 'social']);

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const { action } = req.body || {};
    const db = admin();
    const ip = clientIp(req);

    // ---------------- 발송 ----------------
    if (action === 'send') {
      const phone = normPhone(req.body.phone);
      const purpose = PURPOSES.has(req.body.purpose) ? req.body.purpose : null;
      if (!phone) return bad(res, '휴대폰 번호 형식이 올바르지 않습니다');
      if (!purpose) return bad(res, '요청 목적이 올바르지 않습니다');

      const t1m = new Date(Date.now() - 60e3).toISOString();
      const t24 = new Date(Date.now() - 864e5).toISOString();

      const { count: c1 } = await db.from('otp_codes')
        .select('*', { count: 'exact', head: true })
        .eq('phone', phone).gte('created_at', t1m);
      if ((c1 ?? 0) >= 1) return bad(res, '잠시 후 다시 시도해주세요 (1분에 1회)', 429);

      const { count: c24 } = await db.from('otp_codes')
        .select('*', { count: 'exact', head: true })
        .eq('phone', phone).gte('created_at', t24);
      if ((c24 ?? 0) >= 8) return bad(res, '오늘 이 번호의 발송 한도를 초과했습니다', 429);

      if (ip) {
        const { count: cIp } = await db.from('otp_codes')
          .select('*', { count: 'exact', head: true })
          .eq('ip', ip).gte('created_at', t24);
        if ((cIp ?? 0) >= 30) return bad(res, '발송 한도를 초과했습니다', 429);
      }

      const code = randCode6();
      const { error: insErr } = await db.from('otp_codes').insert({
        phone, purpose, ip,
        code_hash: sha(code),
        expires_at: new Date(Date.now() + 5 * 60e3).toISOString(),
      });
      if (insErr) return bad(res, 'DB 오류: ' + insErr.message, 500);

      const r = await sendSMS(phone, `[ashrain] 인증번호 ${code} (5분 내 입력)`);
      if (!r.ok) {
        return bad(res, '문자 발송에 실패했습니다: ' + (r.raw?.message || '알 수 없는 오류'), 502);
      }

      // 하루 지난 레코드 청소 (응답 지연 없이 발사 후 무시)
      db.from('otp_codes').delete()
        .lt('expires_at', new Date(Date.now() - 864e5).toISOString())
        .then(() => {}, () => {});

      return json(res, 200, { sent: true });
    }

    // ---------------- 검증 ----------------
    if (action === 'verify') {
      const phone = normPhone(req.body.phone);
      const purpose = PURPOSES.has(req.body.purpose) ? req.body.purpose : null;
      const code = String(req.body.code || '').trim();
      if (!phone || !purpose || !/^\d{6}$/.test(code)) return bad(res, '입력값이 올바르지 않습니다');

      const { data: rows, error } = await db.from('otp_codes')
        .select('*')
        .eq('phone', phone).eq('purpose', purpose).eq('verified', false)
        .order('created_at', { ascending: false }).limit(1);
      if (error) return bad(res, 'DB 오류: ' + error.message, 500);

      const row = rows?.[0];
      if (!row) return bad(res, '인증번호를 먼저 요청해주세요');
      if (new Date(row.expires_at) < new Date()) return bad(res, '인증번호가 만료되었습니다. 재발송해주세요');
      if (row.attempts >= 5) return bad(res, '시도 횟수를 초과했습니다. 재발송해주세요');

      if (row.code_hash !== sha(code)) {
        await db.from('otp_codes').update({ attempts: row.attempts + 1 }).eq('id', row.id);
        return bad(res, '인증번호가 일치하지 않습니다');
      }

      await db.from('otp_codes').update({ verified: true }).eq('id', row.id);
      return json(res, 200, {
        phone_token: signToken({ t: 'phone', phone, purpose }, 15 * 60),
      });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
