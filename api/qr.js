// api/qr.js — QR 로그인 (PC에 QR 표시 → 로그인된 폰으로 스캔·승인 → PC 세션 발급)
// POST { action, ... }
//  create  : {} → { qr_id, poll_key, expires_at }
//            PC가 qr_id로 QR 생성: (앱주소)/#/qr-approve?sid=(qr_id)
//  approve : (JWT 필수) { qr_id } → { done }        폰에서 승인
//  claim   : { qr_id, poll_key } → { pending:true } 반복 → 승인되면 { token_hash }
//            PC는 supabase.auth.verifyOtp({ type:'magiclink', token_hash })로 세션 생성

import { admin, getUser, bad, json, randToken } from './_lib/core.js';

const TTL_MS = 2 * 60e3; // QR 유효 2분

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const { action } = req.body || {};
    const db = admin();

    // 만료 세션 청소 (발사 후 무시)
    db.from('qr_sessions').delete()
      .lt('expires_at', new Date(Date.now() - 10 * 60e3).toISOString())
      .then(() => {}, () => {});

    // ---------------- 생성 (PC) ----------------
    if (action === 'create') {
      const poll_key = randToken();
      const expires_at = new Date(Date.now() + TTL_MS).toISOString();
      const { data, error } = await db.from('qr_sessions')
        .insert({ poll_key, expires_at })
        .select('id').single();
      if (error) return bad(res, error.message, 500);
      return json(res, 200, { qr_id: data.id, poll_key, expires_at });
    }

    // ---------------- 승인 (폰, 로그인 필요) ----------------
    if (action === 'approve') {
      const user = await getUser(req);
      if (!user) return bad(res, '로그인이 필요합니다', 401);
      const qr_id = String(req.body.qr_id || '');
      if (!qr_id) return bad(res, 'qr_id 필요');

      const { data: row } = await db.from('qr_sessions')
        .select('*').eq('id', qr_id).maybeSingle();
      if (!row) return bad(res, '만료되었거나 없는 요청입니다', 404);
      if (row.status !== 'pending') return bad(res, '이미 처리된 요청입니다', 409);
      if (new Date(row.expires_at) < new Date()) return bad(res, 'QR이 만료되었습니다. PC에서 새로고침해주세요', 410);
      if (!user.email) return bad(res, '이 계정으로는 QR 로그인을 사용할 수 없습니다', 400);

      const { data: link, error: lErr } = await db.auth.admin.generateLink({
        type: 'magiclink', email: user.email,
      });
      const token_hash = link?.properties?.hashed_token;
      if (lErr || !token_hash) return bad(res, '승인 처리 실패: ' + (lErr?.message || ''), 500);

      const { error: uErr } = await db.from('qr_sessions').update({
        status: 'approved', approved_by: user.id,
        otp_email: user.email, token_hash,
      }).eq('id', qr_id).eq('status', 'pending');
      if (uErr) return bad(res, uErr.message, 500);

      return json(res, 200, { done: true });
    }

    // ---------------- 수령 (PC 폴링) ----------------
    if (action === 'claim') {
      const qr_id = String(req.body.qr_id || '');
      const poll_key = String(req.body.poll_key || '');
      if (!qr_id || !poll_key) return bad(res, 'qr_id/poll_key 필요');

      const { data: row } = await db.from('qr_sessions')
        .select('*').eq('id', qr_id).maybeSingle();
      if (!row || row.poll_key !== poll_key) return bad(res, '유효하지 않은 요청입니다', 404);
      if (new Date(row.expires_at) < new Date() && row.status === 'pending') {
        return bad(res, 'QR이 만료되었습니다', 410);
      }
      if (row.status === 'pending') return json(res, 200, { pending: true });
      if (row.status !== 'approved' || !row.token_hash) return bad(res, '이미 사용된 요청입니다', 409);

      // 1회 수령 후 토큰 즉시 파기
      const { data: took } = await db.from('qr_sessions')
        .update({ status: 'claimed', token_hash: null })
        .eq('id', qr_id).eq('status', 'approved')
        .select('id');
      if (!took?.length) return bad(res, '이미 사용된 요청입니다', 409);

      return json(res, 200, { token_hash: row.token_hash });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
