// api/points.js — 재화 잔액/내역/쿠폰 등록 (로그인 필수)
// 재화 2종: Ⓟ Ash(ash) = 유료 학습 기능(AI 한도 초과분)에 쓰는 재화 · Ⓓ Drop(drop) = 학습 활동 보상(추후 숍). 상호 교환 없음.
// POST { action, ... }
//  balance : {} → { balance(=ash), ash, drop, ready }   ready=false 면 원장에 currency 열이 아직 없음(Ⓓ 0)
//  history : { limit?, currency? } → { rows: [{delta, currency, reason, ref, memo, created_at}] }
//  redeem  : { member_code(유형 7 쿠폰) } → { added, balance }   (Ⓟ 충전)
// Ⓓ 적립은 api/review.js 등 서버에서만 한다. 결제(PG) 없음 — 충전은 쿠폰·관리자 지급뿐.

import {
  admin, getUser, bad, json,
  normCode, quickCheck, verifyCode,
} from './_lib/core.js';

const CURRENCIES = ['ash', 'drop'];
const isMissing = (err) => /does not exist|schema cache|column|function/i.test(err?.message || '');

async function balances(db, uid) {
  const { data: ash, error } = await db.rpc('point_balance', { p_uid: uid });
  if (error) throw error;
  const { data: drop, error: e2 } = await db.rpc('point_balance_of', { p_uid: uid, p_currency: 'drop' });
  if (e2) {
    if (isMissing(e2)) return { ash: ash ?? 0, drop: 0, ready: false };
    throw e2;
  }
  return { ash: ash ?? 0, drop: drop ?? 0, ready: true };
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const { action } = req.body || {};
    const db = admin();

    const user = await getUser(req);
    if (!user) return bad(res, '로그인이 필요합니다', 401);

    // ---------------- 잔액 ----------------
    if (action === 'balance') {
      try {
        const b = await balances(db, user.id);
        return json(res, 200, { balance: b.ash, ...b });
      } catch (e) { return bad(res, e.message, 500); }
    }

    // ---------------- 내역 ----------------
    if (action === 'history') {
      const lim = Math.min(Math.max(+req.body.limit || 30, 1), 100);
      const cur = CURRENCIES.includes(req.body.currency) ? req.body.currency : null;
      let q = db.from('point_ledger')
        .select('delta, currency, reason, ref, memo, created_at')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })
        .limit(lim);
      if (cur) q = q.eq('currency', cur);
      let { data, error } = await q;
      if (error && isMissing(error)) {
        // currency 열이 아직 없는 DB — 전부 Ⓟ 로 본다
        const r = await db.from('point_ledger').select('delta, reason, ref, memo, created_at')
          .eq('user_id', user.id).order('created_at', { ascending: false }).limit(lim);
        data = (r.data || []).map((x) => ({ ...x, currency: 'ash' }));
        error = r.error;
        if (cur === 'drop') data = [];
      }
      if (error) return bad(res, error.message, 500);
      return json(res, 200, { rows: data || [] });
    }

    // ---------------- 쿠폰 등록 (Ⓟ) ----------------
    if (action === 'redeem') {
      const code = normCode(req.body.member_code);
      if (!quickCheck(code)) return bad(res, '쿠폰 번호를 다시 확인해주세요');

      const { data: row } = await db.from('member_codes').select('*').eq('code', code).maybeSingle();
      if (!row) return bad(res, '등록되지 않은 쿠폰입니다');
      if (row.role_type !== 7) return bad(res, '포인트 쿠폰이 아닙니다');
      if (row.status === 'used') return bad(res, '이미 사용된 쿠폰입니다');
      if (row.status === 'revoked') return bad(res, '사용이 중지된 쿠폰입니다');
      if (!row.point_value || row.point_value <= 0) return bad(res, '쿠폰 금액 정보가 없습니다. 학원에 문의해주세요');

      const { data: academy } = await db.from('academies')
        .select('region').eq('code', row.academy_code).maybeSingle();
      if (!academy) return bad(res, '학원 정보를 찾을 수 없습니다');

      const v = verifyCode(code, { region: academy.region, ver: row.key_ver || 'v1' });
      if (!v.ok) return bad(res, '쿠폰 검증에 실패했습니다. 학원에 문의해주세요');

      // 선점 (동시 등록 경쟁 차단)
      const { data: taken } = await db.from('member_codes')
        .update({
          status: 'used', assigned_user: user.id, used_at: new Date().toISOString(),
        })
        .eq('code', code).eq('status', row.status)
        .select('code');
      if (!taken?.length) return bad(res, '이미 사용된 쿠폰입니다', 409);

      // currency 열이 없는 DB 에서도 동작하도록 두 번 시도
      let { error: lErr } = await db.from('point_ledger').insert({
        user_id: user.id, delta: row.point_value, currency: 'ash',
        reason: 'coupon', ref: code,
      });
      if (lErr && isMissing(lErr)) {
        ({ error: lErr } = await db.from('point_ledger').insert({
          user_id: user.id, delta: row.point_value, reason: 'coupon', ref: code,
        }));
      }
      if (lErr) {
        // 적립 실패 시 쿠폰 원복
        await db.from('member_codes')
          .update({ status: 'issued', assigned_user: null, used_at: null }).eq('code', code);
        return bad(res, '적립에 실패했습니다: ' + lErr.message, 500);
      }

      const { data: bal } = await db.rpc('point_balance', { p_uid: user.id });
      return json(res, 200, { added: row.point_value, balance: bal ?? 0, ash: bal ?? 0 });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    return bad(res, '서버 오류: ' + (e?.message || e), 500);
  }
}
