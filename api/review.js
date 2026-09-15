// api/review.js — 개념 복습 모드 (Ⓓ Drop 을 적립하는 유일한 경로, 로그인 필수)
// POST { action, ... } + Bearer
//  status   : { recent:[conceptId…] (가장 최근이 앞, ≤5) }
//             → { ready, concepts:[{ concept_id, rank, cap, done, remaining }], today_done, today_cap }
//  start    : { concept_id, recent }
//             → { review_id, items:[{ id, qtype, question, choices, figure, difficulty, source }], rank, cap, done, remaining,
//                 today_done, today_cap, rewardable, reward, ready }
//               (concept_reviews 테이블이 없으면 review_id:null · ready:false · rewardable:false — 퀴즈는 그대로 낸다)
//  complete : { review_id, answers:[{ item_id, answer?|index? }], read_ms }  (review_id 없으면 concept_id 로 채점만)
//             → 만점 { ok:true, score, max, reward, drop_balance, remaining, today_done, today_cap, cap, rank }
//               오답 { ok:false, reason:'wrong', score, max, wrong:[item_id…] }   (행은 미완료로 남아 다시 start 가능)
//               빠름 { ok:false, reason:'too_fast', wait(초) }
// 정답 판정은 전부 서버(service role 로 test_items 정답 조회 → src/lib/review.js judgeQuiz). 클라 판정은 믿지 않는다.
// 테이블·함수가 아직 없으면(supabase/2026-09_wallet_review.sql 미적용) 500 대신 ready:false 로 조용히 내려간다.

import { admin, getUser, bad, json } from './_lib/core.js';
import {
  capForRank, rankOf, normRecent, pickQuiz, checkBlockItems, stripAnswers, judgeQuiz, kstDayStart,
  REWARD, DAILY_CAP, QUIZ_N, MIN_TOTAL_MS, RETRY_WINDOW_MS,
} from '../src/lib/review.js';

const ITEM_PUBLIC = 'id, qtype, question, choices, figure, difficulty, template_id, math_key';
const ITEM_FULL = 'id, qtype, question, choices, figure, difficulty, answer, answer_alt';
const ID_RE = /^[\w-]{1,40}$/;

/** 테이블·컬럼·함수가 아직 없어서 난 오류인가 (마이그레이션 미적용) */
function missingRel(err) {
  if (!err) return false;
  const code = String(err.code || '');
  if (['42P01', '42703', '42883', 'PGRST202', 'PGRST204', 'PGRST205'].includes(code)) return true;
  return /does not exist|could not find|schema cache/i.test(String(err.message || ''));
}
const cleanErr = (err) => (missingRel(err) ? '복습 기록 저장소가 아직 준비되지 않았어요' : '잠시 후 다시 시도해 주세요');

/** 보상 완주 기록 → { done: {concept_id: n}, todayDone } . 테이블이 없으면 null */
async function loadProgress(db, uid) {
  const { data, error } = await db.from('concept_reviews')
    .select('concept_id, completed_at, reward')
    .eq('user_id', uid).not('completed_at', 'is', null).gt('reward', 0)
    .order('completed_at', { ascending: false }).limit(1000);
  if (error) { if (missingRel(error)) return null; throw error; }
  const dayStart = kstDayStart();
  const done = {};
  let todayDone = 0;
  for (const r of data || []) {
    done[r.concept_id] = (done[r.concept_id] || 0) + 1;
    if (r.completed_at >= dayStart) todayDone++;
  }
  return { done, todayDone };
}

/** 공개 문항 후보 (service role 이라 status 필터를 직접 건다) */
async function liveCandidates(db, conceptId) {
  const axis = ['created_at', 'id', 'difficulty'][Math.floor(Math.random() * 3)];
  const { data, error } = await db.from('test_items').select(ITEM_PUBLIC)
    .eq('status', 'live').contains('concept_ids', [conceptId]).in('qtype', ['choice', 'short'])
    .order(axis, { ascending: Math.random() < 0.5 }).limit(80);
  if (error) throw error;
  return data || [];
}

/** quiz[{item_id}] → 정답 포함 문항 (순서 유지). check:* 는 개념 단락에서 다시 만든다 */
async function loadQuizItems(db, quiz, concept) {
  const ids = (Array.isArray(quiz) ? quiz : []).map((q) => (typeof q === 'string' ? q : q?.item_id)).filter(Boolean);
  const real = ids.filter((id) => !String(id).startsWith('check:'));
  const by = {};
  if (real.length) {
    const { data, error } = await db.from('test_items').select(ITEM_FULL).in('id', real);
    if (error) throw error;
    for (const it of data || []) by[it.id] = it;
  }
  if (ids.some((id) => String(id).startsWith('check:'))) {
    for (const it of checkBlockItems(concept)) by[it.id] = it;
  }
  return ids.map((id) => by[id]).filter(Boolean);
}

async function loadConcept(db, conceptId) {
  const { data, error } = await db.from('concepts').select('id, title, blocks').eq('id', conceptId).maybeSingle();
  if (error) throw error;
  return data;
}

async function dropBalance(db, uid) {
  const { data, error } = await db.rpc('point_balance_of', { p_uid: uid, p_currency: 'drop' });
  if (error) return null;
  return data ?? 0;
}

export default async function handler(req, res) {
  try {
    if (req.method !== 'POST') return bad(res, 'POST only', 405);
    const body = req.body || {};
    const { action } = body;
    const user = await getUser(req);
    if (!user) return bad(res, '로그인이 필요해요', 401);
    const uid = user.id;
    const db = admin();

    // ---------------- 현황 ----------------
    if (action === 'status') {
      const recent = normRecent(body.recent);
      let prog = null;
      try { prog = await loadProgress(db, uid); } catch (e) { return bad(res, cleanErr(e), 500); }
      const ready = !!prog;
      const concepts = recent.map((id, i) => {
        const rank = i + 1, cap = capForRank(rank), done = prog?.done?.[id] || 0;
        return { concept_id: id, rank, cap, done, remaining: ready ? Math.max(0, cap - done) : 0 };
      });
      return json(res, 200, { ready, concepts, today_done: prog?.todayDone || 0, today_cap: DAILY_CAP, reward: REWARD });
    }

    // ---------------- 시작 ----------------
    if (action === 'start') {
      const conceptId = String(body.concept_id || '');
      if (!ID_RE.test(conceptId)) return bad(res, '개념 id 가 필요해요');
      const concept = await loadConcept(db, conceptId);
      if (!concept) return bad(res, '개념을 찾을 수 없어요', 404);

      const recent = normRecent(body.recent);
      const rank = rankOf(recent, conceptId);
      const cap = capForRank(rank);

      let picked = pickQuiz(await liveCandidates(db, conceptId), QUIZ_N);
      if (picked.length < QUIZ_N) picked = picked.concat(pickQuiz(checkBlockItems(concept), QUIZ_N - picked.length));
      const items = picked.map(stripAnswers);

      let prog = null;
      try { prog = await loadProgress(db, uid); } catch (e) { return bad(res, cleanErr(e), 500); }
      const done = prog?.done?.[conceptId] || 0;
      const todayDone = prog?.todayDone || 0;
      const base = { items, rank, cap, done, today_done: todayDone, today_cap: DAILY_CAP, reward: REWARD };
      if (!prog) return json(res, 200, { ...base, review_id: null, remaining: 0, rewardable: false, ready: false });

      const { data: row, error } = await db.from('concept_reviews')
        .insert({ user_id: uid, concept_id: conceptId, rank, quiz: items.map((it) => ({ item_id: it.id })), started_at: new Date().toISOString() })
        .select('id').single();
      if (error) {
        if (missingRel(error)) return json(res, 200, { ...base, review_id: null, remaining: 0, rewardable: false, ready: false });
        return bad(res, cleanErr(error), 500);
      }
      return json(res, 200, {
        ...base, review_id: row.id, remaining: Math.max(0, cap - done),
        rewardable: done < cap && todayDone < DAILY_CAP, ready: true,
      });
    }

    // ---------------- 완료 ----------------
    if (action === 'complete') {
      const answers = Array.isArray(body.answers) ? body.answers.slice(0, 10) : [];
      const readMs = Number.isFinite(+body.read_ms) ? Math.max(0, Math.min(Math.round(+body.read_ms), 86400000)) : null;

      // 기록 없이 채점만 (테이블 미적용 상태의 클라) — 보상 없음
      if (body.review_id == null) {
        const conceptId = String(body.concept_id || '');
        if (!ID_RE.test(conceptId)) return bad(res, '개념 id 가 필요해요');
        const concept = await loadConcept(db, conceptId);
        if (!concept) return bad(res, '개념을 찾을 수 없어요', 404);
        const items = await loadQuizItems(db, answers.map((a) => a?.item_id), concept);
        const j = judgeQuiz(items, answers);
        const ok = j.score === j.max;
        return json(res, 200, { ok, reason: ok ? undefined : 'wrong', score: j.score, max: j.max, wrong: j.wrong, reward: 0, drop_balance: null, remaining: 0, ready: false });
      }

      const reviewId = Number(body.review_id);
      if (!Number.isInteger(reviewId) || reviewId <= 0) return bad(res, '복습 id 가 올바르지 않아요');
      const { data: row, error: rErr } = await db.from('concept_reviews')
        .select('id, user_id, concept_id, rank, quiz, started_at, completed_at')
        .eq('id', reviewId).eq('user_id', uid).maybeSingle();
      if (rErr) return bad(res, cleanErr(rErr), missingRel(rErr) ? 409 : 500);
      if (!row) return bad(res, '복습 기록을 찾을 수 없어요', 404);
      if (row.completed_at) return bad(res, '이미 완료한 복습이에요', 409);

      // 경과 시간 — 같은 개념을 최근 2시간 안에 처음 시작한 시각부터 잰다 (오답 뒤 재도전이 45초 규칙에 막히지 않게)
      const now = Date.now();
      let firstStart = new Date(row.started_at).getTime();
      const { data: earlier } = await db.from('concept_reviews').select('started_at')
        .eq('user_id', uid).eq('concept_id', row.concept_id)
        .gte('started_at', new Date(now - RETRY_WINDOW_MS).toISOString())
        .order('started_at', { ascending: true }).limit(1);
      if (earlier?.[0]?.started_at) firstStart = Math.min(firstStart, new Date(earlier[0].started_at).getTime());
      const elapsed = now - firstStart;
      if (elapsed < MIN_TOTAL_MS) {
        return json(res, 200, { ok: false, reason: 'too_fast', wait: Math.ceil((MIN_TOTAL_MS - elapsed) / 1000) });
      }

      const concept = await loadConcept(db, row.concept_id);
      const items = await loadQuizItems(db, row.quiz, concept || { id: row.concept_id, blocks: [] });
      const j = judgeQuiz(items, answers);
      if (j.max > 0 && j.score < j.max) {
        await db.from('concept_reviews').update({ score: j.score, max: j.max, read_ms: readMs }).eq('id', reviewId);
        return json(res, 200, { ok: false, reason: 'wrong', score: j.score, max: j.max, wrong: j.wrong });
      }

      // 보상 가능? (상한·하루 한도는 서버가 다시 센다)
      const rank = Number.isInteger(row.rank) ? row.rank : rankOf(normRecent(body.recent), row.concept_id);
      const cap = capForRank(rank);
      let prog = null;
      try { prog = await loadProgress(db, uid); } catch (e) { return bad(res, cleanErr(e), 500); }
      const done = prog?.done?.[row.concept_id] || 0;
      const todayDone = prog?.todayDone || 0;
      const rewardable = !!prog && done < cap && todayDone < DAILY_CAP;

      // 완료 선점 — 같은 행을 두 번 제출해도 보상이 두 번 나가지 않는다
      const completedAt = new Date().toISOString();
      const { data: claimed, error: cErr } = await db.from('concept_reviews')
        .update({ completed_at: completedAt, read_ms: readMs, score: j.score, max: j.max, reward: 0 })
        .eq('id', reviewId).eq('user_id', uid).is('completed_at', null).select('id');
      if (cErr) return bad(res, cleanErr(cErr), 500);
      if (!claimed?.length) return bad(res, '이미 완료한 복습이에요', 409);

      let reward = 0, ledgerId = null, rewardError = null;
      if (rewardable) {
        const { data: led, error: lErr } = await db.from('point_ledger')
          .insert({ user_id: uid, delta: REWARD, currency: 'drop', reason: 'review:' + row.concept_id, ref: String(reviewId) })
          .select('id').single();
        if (lErr) rewardError = missingRel(lErr) ? 'not_ready' : 'failed';
        else { reward = REWARD; ledgerId = led?.id ?? null; }
        if (reward) await db.from('concept_reviews').update({ reward, ledger_id: ledgerId }).eq('id', reviewId);
      }

      const doneNow = done + (reward ? 1 : 0);
      return json(res, 200, {
        ok: true, score: j.score, max: j.max, reward,
        drop_balance: await dropBalance(db, uid),
        remaining: Math.max(0, cap - doneNow), cap, rank,
        today_done: todayDone + (reward ? 1 : 0), today_cap: DAILY_CAP,
        ready: !!prog, reward_error: rewardError || undefined,
      });
    }

    return bad(res, 'unknown action');
  } catch (e) {
    console.error('[review]', e?.message || e);
    return bad(res, '서버 오류: ' + cleanErr(e), 500);
  }
}
