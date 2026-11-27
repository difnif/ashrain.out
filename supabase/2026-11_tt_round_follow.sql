-- ashrain.out — 시록고 강사도구 (2026-11) · 다음 차는 앞 차를 따른다 · 채점 취소
-- ① 앞 차(1차 …)를 고치면 다음 차 다시 풀 문항이 따라 바뀐다.
--    틀림 · 안 풂이 된 문항은 다음 차에 들어가 '아직 안 매김'(그 차 미완성)이 되고, 맞음이 된 문항은 다음 차에서 빠진다.
--    빠진 문항의 그 차 기록은 지우지 않고 셈에서만 뺀다(다시 들어오면 다시 보임). 넣기는 한 차씩(그 차에서 매기면 그다음 차로),
--    빼기는 뒤 차까지 잇달아.
-- ② 닫힌 채점도 앞 차를 고쳐 안 매긴 문항이 생기면 '채점 덜 함'(미완성), 다 채워지면 '채점 완료'. 닫을 때도 모든 차를 본다.
-- ③ 다 끝난 채점을 다시 열면 같은 차의 새 회차를 만든다 — 열어 보기만 하고 닫으면 그 회차는 없어지고 그대로 '채점 완료'.
-- ④ 채점 취소(tt_cancel_grading): 지금 열린 회차와 그 뒤 매긴 것(앞 차를 고친 것 포함)을 되돌려 연 전 상태로.
--    처음 연 채점이면 기록째 없앤다(채점을 열면서 생긴 출제 대상도). 처음 연 채점을 아무것도 매기지 않고 닫아도
--    기록째 없앤다 — '이어서 채점할 것'에 남지 않게(스캔본이 있으면 둠).
-- 함수는 부른 사람 권한(RLS 그대로 — 본인 것만). SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

-- 셈에 드는 기록: 다시 풀기 차의 기록은 그 차 다시 풀 문항 것만
create or replace function public.tt_marks_eff(p_grading bigint)
returns table (id bigint, seq integer, round integer, result text, answer text, session_no integer, at timestamptz)
language sql stable security invoker set search_path = public as $$
  select m.id, m.seq, coalesce(x.round, 1), m.result, m.answer, m.session_no, m.at
  from public.tt_marks m
  left join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
  where m.grading_id = p_grading
    and (x.kind is distinct from 'retry' or m.seq = any(coalesce(x.targets, array[m.seq])));
$$;

-- 문항마다 지금 결과 = 기록이 있는 가장 늦은 차의 마지막 기록 (다음 차 다시 풀 문항을 고를 때 씀)
create or replace function public.tt_current(p_grading bigint)
returns table (seq integer, result text, answer text, session_no integer)
language sql stable security invoker set search_path = public as $$
  select distinct on (e.seq) e.seq, e.result, e.answer, e.session_no
  from public.tt_marks_eff(p_grading) e
  order by e.seq, e.round desc, e.id desc;
$$;

-- 안 매긴 문항 수(모든 차): 1차는 기록이 하나도 없는 문항, 다시 풀기 차는 그 차 다시 풀 문항 중 그 차에 아직 안 매긴 것
create or replace function public.tt_blank_count(p_grading bigint)
returns integer language sql stable security invoker set search_path = public as $$
  select ((select count(*) from public.tt_gradings g join public.tt_print_items i on i.print_id = g.print_id
            where g.id = p_grading
              and not exists (select 1 from public.tt_marks m where m.grading_id = p_grading and m.seq = i.seq))
        + (select count(*) from (select distinct on (x.round) x.round, x.targets from public.tt_sessions x
                                   where x.grading_id = p_grading and x.kind = 'retry' order by x.round, x.no desc) r
             cross join lateral unnest(coalesce(r.targets, '{}'::integer[])) t(seq)
            where not exists (select 1 from public.tt_marks m join public.tt_sessions y on y.grading_id = m.grading_id and y.no = m.session_no
                               where m.grading_id = p_grading and m.seq = t.seq and y.round = r.round)))::integer;
$$;

create or replace function public.tt_open_grading(p_print bigint, p_student bigint, p_purpose text default null)
returns bigint language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; s public.tt_sessions; v_targets integer[]; v_round integer;
begin
  select * into g from public.tt_gradings where print_id = p_print and student_id = p_student;
  if not found then
    insert into public.tt_gradings(print_id, student_id) values (p_print, p_student) returning * into g;
    insert into public.tt_targets(print_id, student_id) values (p_print, p_student) on conflict do nothing;
    insert into public.tt_sessions(grading_id, no, round, kind) values (g.id, 1, 1, 'solve');
    perform public.tt_log('grading_start', p_student, p_print, jsonb_build_object('grading', g.id));
    return g.id;
  end if;
  select * into s from public.tt_sessions where grading_id = g.id order by no desc limit 1;
  if p_purpose = 'retry' then
    select array_agg(c.seq order by c.seq) into v_targets
      from public.tt_current(g.id) c where c.result in ('X', 'U')
       and c.seq in (select i.seq from public.tt_print_items i where i.print_id = p_print);
    if v_targets is null then
      raise exception '다시 매길 문항(틀리거나 안 푼 문항)이 없어요' using errcode = 'P0001';
    end if;
    if s.id is not null and s.ended_at is null then
      update public.tt_sessions set ended_at = now(), end_reason = coalesce(end_reason, 'done') where id = s.id;
    end if;
    select coalesce(max(round), 1) + 1 into v_round from public.tt_sessions where grading_id = g.id;
    insert into public.tt_sessions(grading_id, no, round, kind, targets)
      values (g.id, coalesce(s.no, 0) + 1, v_round, 'retry', v_targets);
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('retry_start', p_student, p_print, jsonb_build_object('grading', g.id, 'round', v_round, 'targets', cardinality(v_targets)));
  elsif s.id is not null and s.ended_at is null then
    null;                                               -- 열려 있던 회차를 그대로 이어 감
  elsif g.status = 'done' and s.id is not null then     -- 다 끝난 채점을 다시 열면 = 고치기: 같은 차의 새 회차
    insert into public.tt_sessions(grading_id, no, round, kind, targets)
      values (g.id, s.no + 1, coalesce(s.round, 1), coalesce(s.kind, 'solve'), s.targets);
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('grading_reopen', p_student, p_print, jsonb_build_object('grading', g.id, 'round', s.round, 'session', s.no + 1));
  else                                                  -- 덜 풀었거나 덜 매겨 멈춘 채점 → 같은 차의 다음 회차
    insert into public.tt_sessions(grading_id, no, round, kind, targets)
      values (g.id, coalesce(s.no, 0) + 1, coalesce(s.round, 1), coalesce(s.kind, 'solve'), s.targets);
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('grading_resume', p_student, p_print, jsonb_build_object('grading', g.id, 'was', g.status));
  end if;
  return g.id;
end $$;

-- 닫기. p_reason: done | unsolved(아이가 덜 풂) | ungraded(채점을 덜 함). p_untouched: 열어 보기만 했으면 빈 회차를 없애고 전 상태로.
-- '다 채점함'이어도 어느 차든 안 매긴 문항이 남았으면 '채점 덜 함'. 처음 연 채점을 열어 보기만 했으면 기록째 없애고 'deleted'.
create or replace function public.tt_close_grading(p_grading bigint, p_reason text, p_untouched boolean default false)
returns text language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; s public.tt_sessions; prev public.tt_sessions; v_blank integer[]; v_status text; n_here integer;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if p_untouched then
    select count(*) into n_here from public.tt_marks where grading_id = p_grading and session_no = s.no;
    select * into prev from public.tt_sessions where grading_id = p_grading and no < s.no order by no desc limit 1;
    if n_here = 0 and prev.id is not null then
      delete from public.tt_sessions where id = s.id;
      update public.tt_sessions set ended_at = coalesce(ended_at, now()) where id = prev.id;
      v_status := case prev.end_reason when 'done' then 'done' when 'unsolved' then 'paused_unsolved' else 'paused_ungraded' end;
      if v_status = 'done' and public.tt_blank_count(p_grading) > 0 then v_status := 'paused_ungraded'; end if;
      update public.tt_gradings set status = v_status where id = p_grading;
      return v_status;
    end if;
    if n_here = 0 and prev.id is null and not exists (select 1 from public.tt_marks where grading_id = p_grading)
       and not exists (select 1 from public.tt_scans where grading_id = p_grading) then
      perform public.tt_log('grading_cancel', g.student_id, g.print_id, jsonb_build_object('grading', p_grading, 'deleted', true, 'marks', 0, 'auto', true));
      delete from public.tt_targets where print_id = g.print_id and student_id = g.student_id and issued_at = g.created_at;
      delete from public.tt_gradings where id = p_grading;
      return 'deleted';
    end if;
  end if;
  if s.kind = 'retry' then          -- 다시 풀기: 이번 차에 아직 안 매긴 다시 풀 문항만 '남음'(U를 쓰지 않음 — 앞 차 결과가 최종)
    select array_agg(t) into v_blank from unnest(coalesce(s.targets, '{}'::integer[])) t
     where not exists (select 1 from public.tt_marks m join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
                       where m.grading_id = p_grading and m.seq = t and x.round = s.round);
  else
    select array_agg(i.seq) into v_blank from public.tt_print_items i
     where i.print_id = g.print_id and not exists (select 1 from public.tt_marks m where m.grading_id = p_grading and m.seq = i.seq);
    if p_reason = 'unsolved' and v_blank is not null then
      insert into public.tt_marks(grading_id, session_no, seq, result) select p_grading, s.no, t, 'U' from unnest(v_blank) t;
    end if;
  end if;
  v_status := case p_reason when 'done' then 'done' when 'unsolved' then 'paused_unsolved' else 'paused_ungraded' end;
  if v_status = 'done' and (v_blank is not null or public.tt_blank_count(p_grading) > 0) then v_status := 'paused_ungraded'; end if;
  update public.tt_sessions set ended_at = now(), end_reason = p_reason where id = s.id;
  update public.tt_gradings set status = v_status, updated_at = now() where id = p_grading;
  perform public.tt_log('grading_close', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'reason', p_reason, 'session', s.no, 'round', s.round, 'blank', coalesce(cardinality(v_blank), 0)));
  return v_status;
end $$;

-- 지우기. p_scope: all(그 학생의 그 프린트 채점 전부) | last_round(마지막 차만). 돌려주는 것: 지울 스캔본 경로들
create or replace function public.tt_delete_grading(p_grading bigint, p_scope text default 'all')
returns jsonb language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; mx integer; last public.tt_sessions; v_paths text[]; n integer; v_status text;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '그런 채점 기록이 없어요' using errcode = 'P0001'; end if;
  if p_scope = 'last_round' then
    select coalesce(max(round), 1) into mx from public.tt_sessions where grading_id = p_grading;
    if mx <= 1 then raise exception '1차만 있는 채점이에요. 지우려면 채점 기록 전체를 지우세요' using errcode = 'P0001'; end if;
    delete from public.tt_marks m using public.tt_sessions x
     where m.grading_id = p_grading and x.grading_id = p_grading and x.no = m.session_no and x.round = mx;
    get diagnostics n = row_count;
    delete from public.tt_sessions where grading_id = p_grading and round = mx;
    update public.tt_sessions set ended_at = coalesce(ended_at, now()) where grading_id = p_grading;
    select * into last from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
    v_status := case coalesce(last.end_reason, 'done') when 'unsolved' then 'paused_unsolved' when 'ungraded' then 'paused_ungraded' else 'done' end;
    if v_status = 'done' and public.tt_blank_count(p_grading) > 0 then v_status := 'paused_ungraded'; end if;
    update public.tt_gradings set updated_at = now(), status = v_status where id = p_grading;
    perform public.tt_log('round_delete', g.student_id, g.print_id, jsonb_build_object('grading', p_grading, 'round', mx, 'marks', n));
    return jsonb_build_object('ok', true, 'deleted_round', mx, 'paths', '[]'::jsonb);
  end if;
  select array_agg(path) into v_paths from public.tt_scans where grading_id = p_grading;
  select count(*) into n from public.tt_marks where grading_id = p_grading;
  perform public.tt_log('grading_delete', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'marks', n, 'scans', coalesce(cardinality(v_paths), 0),
                       'rounds', (select coalesce(max(round), 1) from public.tt_sessions where grading_id = p_grading)));
  delete from public.tt_gradings where id = p_grading;   -- 회차·기록·스캔본 행은 on delete cascade
  return jsonb_build_object('ok', true, 'paths', to_jsonb(coalesce(v_paths, '{}'::text[])));
end $$;

-- 앞 차 고치기: p_round 차(이번 차보다 앞)의 그 문항 결과를 p_result 로 — 그 차의 마지막 회차에 기록을 덧붙인다.
--   p_answer 가 null 이면 그 차에 적어 둔 답을 그대로 둔다. 그 뒤 다음 차들을 앞 차에 맞춘다(맨 위 ①).
--   닫힌 채점이면 상태도 다시(안 매긴 문항이 생기면 '채점 덜 함', 다 채워지면 '채점 완료').
-- 돌려주는 것: {ok, changed, added_round(넣은 차), removed_rounds(뺀 차들), status, blanks(모든 차의 안 매긴 문항 수)}
create or replace function public.tt_mark_round(p_grading bigint, p_round integer, p_seq integer, p_result text, p_answer text default null)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  g public.tt_gradings; last public.tt_sessions; rs public.tt_sessions; rk public.tt_sessions; v_prev public.tt_marks;
  v_before text; v_changed boolean := false; k integer; v_added integer; v_removed integer[] := '{}'::integer[]; v_status text;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if coalesce(p_result, '') not in ('O', 'X', 'U') then
    raise exception '앞 차 결과는 O · X · 안 풂 중 하나로 고쳐요' using errcode = 'P0001';
  end if;
  if not exists (select 1 from public.tt_print_items i where i.print_id = g.print_id and i.seq = p_seq) then
    raise exception '그런 문항이 없어요' using errcode = 'P0001';
  end if;
  select * into last from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if last.id is null or p_round is null or p_round < 1 or p_round >= last.round then
    raise exception '앞 차만 여기서 고쳐요 (이번 차는 그대로 매기면 돼요)' using errcode = 'P0001';
  end if;
  select * into rs from public.tt_sessions where grading_id = p_grading and round = p_round order by no desc limit 1;
  if rs.id is null then raise exception '%차 기록이 없어요', p_round using errcode = 'P0001'; end if;
  if rs.kind = 'retry' and not (p_seq = any(coalesce(rs.targets, array[p_seq]))) then
    raise exception '%차에 다시 푼 문항이 아니에요', p_round using errcode = 'P0001';
  end if;

  select m.* into v_prev from public.tt_marks m
    join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
   where m.grading_id = p_grading and m.seq = p_seq and x.round = p_round
   order by m.id desc limit 1;
  if v_prev.id is null or v_prev.result is distinct from p_result
     or (p_answer is not null and v_prev.answer is distinct from p_answer) then
    insert into public.tt_marks(grading_id, session_no, seq, result, answer)
      values (p_grading, rs.no, p_seq, p_result, coalesce(p_answer, v_prev.answer, ''));
    v_changed := true;
    perform public.tt_log('mark_fix', g.student_id, g.print_id,
      jsonb_build_object('grading', p_grading, 'round', p_round, 'seq', p_seq, 'from', v_prev.result, 'to', p_result));
  end if;

  -- 다음 차는 앞 차를 따른다
  k := p_round + 1;
  while k <= last.round loop
    select * into rk from public.tt_sessions where grading_id = p_grading and round = k order by no desc limit 1;
    exit when rk.id is null or rk.kind <> 'retry';
    select e.result into v_before from public.tt_marks_eff(p_grading) e
     where e.seq = p_seq and e.round < k order by e.round desc, e.id desc limit 1;
    if v_before in ('X', 'U') then
      exit when p_seq = any(coalesce(rk.targets, '{}'::integer[]));     -- 이미 그 차 다시 풀 문항 — 그대로
      update public.tt_sessions
         set targets = (select array_agg(distinct t order by t) from unnest(coalesce(targets, '{}'::integer[]) || p_seq) t)
       where grading_id = p_grading and round = k;
      v_added := k;
      perform public.tt_log('retry_target_add', g.student_id, g.print_id,
        jsonb_build_object('grading', p_grading, 'round', k, 'seq', p_seq, 'by', 'fix'));
      exit;                                                              -- 넣기는 한 차만
    end if;
    if p_seq = any(coalesce(rk.targets, '{}'::integer[])) then
      update public.tt_sessions set targets = array_remove(targets, p_seq) where grading_id = p_grading and round = k;
      v_removed := v_removed || k;
      perform public.tt_log('retry_target_remove', g.student_id, g.print_id,
        jsonb_build_object('grading', p_grading, 'round', k, 'seq', p_seq, 'by', 'fix'));
    end if;
    k := k + 1;                                                          -- 그 차에 없으니 그다음 차도 다시 봄
  end loop;

  if last.ended_at is not null then         -- 닫힌 채점: 안 매긴 문항이 생겼으면 미완성, 다 채워졌으면 완료
    v_status := case when g.status = 'paused_unsolved' then 'paused_unsolved' else 'done' end;
    if v_status = 'done' and public.tt_blank_count(p_grading) > 0 then v_status := 'paused_ungraded'; end if;
    update public.tt_gradings set status = v_status where id = p_grading;
  else
    v_status := g.status;
  end if;
  if v_changed or v_added is not null or cardinality(v_removed) > 0 then
    update public.tt_gradings set updated_at = now() where id = p_grading;
  end if;
  return jsonb_build_object('ok', true, 'changed', v_changed, 'added_round', v_added, 'removed_rounds', to_jsonb(v_removed),
                            'status', v_status, 'blanks', public.tt_blank_count(p_grading));
end $$;

-- 채점 취소: 마지막 회차(지금 열려 있거나, 덜 끝나 멈춘 것)를 없던 일로 — 그 회차를 연 뒤 매긴 기록(이번 차 · 앞 차를 고친 것)과
--   다시 풀 문항 바뀐 것을 되돌리고 연 전 상태로. 회차가 하나뿐인 채점이거나 매긴 기록 · 스캔본이 하나도 없으면 채점 기록째 없앤다
--   (함께 생긴 출제 대상도). 다 끝난 채점은 취소하지 않는다(고치기 · 지우기는 따로).
--   p_dry = true 면 아무것도 바꾸지 않고 무엇을 할지만 돌려준다(확인 창에 쓰려고).
-- 돌려주는 것: {ok, result: 'deleted' | 'reverted', status | back(연 전 상태), marks(지우거나 되돌릴 기록 수), scans, paths(지울 스캔본 경로)}
drop function if exists public.tt_cancel_grading(bigint);
create or replace function public.tt_cancel_grading(p_grading bigint, p_dry boolean default false)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  g public.tt_gradings; s public.tt_sessions; prev public.tt_sessions; e record;
  v_since timestamptz; v_reopen timestamptz; v_reason text; v_status text; v_paths text[]; n integer := 0; n_all integer; n_scans integer;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if s.id is not null and s.ended_at is not null and g.status = 'done' then
    raise exception '다 끝난 채점은 취소하지 않아요 — 고치려면 「채점 수정」, 지우려면 결과 화면의 「채점 기록 지우기」를 쓰세요' using errcode = 'P0001';
  end if;
  select count(*) into n_all from public.tt_marks where grading_id = p_grading;
  select count(*) into n_scans from public.tt_scans where grading_id = p_grading;
  if s.id is null or (n_all = 0 and n_scans = 0)
     or not exists (select 1 from public.tt_sessions x where x.grading_id = p_grading and x.no <> s.no) then
    if p_dry then return jsonb_build_object('ok', true, 'result', 'deleted', 'marks', n_all, 'scans', n_scans); end if;
    select array_agg(path) into v_paths from public.tt_scans where grading_id = p_grading;
    perform public.tt_log('grading_cancel', g.student_id, g.print_id,
      jsonb_build_object('grading', p_grading, 'deleted', true, 'marks', n_all, 'scans', n_scans));
    delete from public.tt_targets where print_id = g.print_id and student_id = g.student_id and issued_at = g.created_at;
    delete from public.tt_gradings where id = p_grading;
    return jsonb_build_object('ok', true, 'result', 'deleted', 'marks', n_all, 'paths', to_jsonb(coalesce(v_paths, '{}'::text[])));
  end if;
  -- 이 회차를 연 때: 예전 방식으로 같은 회차를 다시 연 것이면 다시 연 때부터
  select max(ev.at) into v_reopen from public.tt_events ev
   where ev.kind = 'grading_reopen' and (ev.detail->>'grading')::bigint = p_grading and ev.at > s.started_at;
  v_since := coalesce(v_reopen, s.started_at);
  if p_dry then
    select * into prev from public.tt_sessions where grading_id = p_grading and no < s.no order by no desc limit 1;
    return jsonb_build_object('ok', true, 'result', 'reverted', 'round', s.round,
      'marks', (select count(*) from public.tt_marks where grading_id = p_grading and at >= v_since), 'scans', n_scans,
      'back', case when v_reopen is not null then 'done' else coalesce(prev.end_reason, 'ungraded') end);
  end if;
  delete from public.tt_marks where grading_id = p_grading and at >= v_since;
  get diagnostics n = row_count;
  for e in select ev.kind, ev.detail from public.tt_events ev
            where ev.kind in ('retry_target_add', 'retry_target_remove') and (ev.detail->>'grading')::bigint = p_grading
              and ev.at >= v_since
            order by ev.id desc loop
    if e.kind = 'retry_target_add' then
      update public.tt_sessions set targets = array_remove(targets, (e.detail->>'seq')::integer)
       where grading_id = p_grading and round = (e.detail->>'round')::integer;
    else
      update public.tt_sessions
         set targets = (select array_agg(distinct t order by t) from unnest(coalesce(targets, '{}'::integer[]) || (e.detail->>'seq')::integer) t)
       where grading_id = p_grading and round = (e.detail->>'round')::integer;
    end if;
  end loop;
  if v_reopen is not null then              -- 예전 방식으로 다시 연 회차: 회차는 두고 다시 닫음
    update public.tt_sessions set ended_at = now(), end_reason = 'done' where id = s.id;
    v_reason := 'done';
  else                                      -- 이번에 새로 연 회차(다시 풀기 시작 · 이어서 · 고치기): 회차를 없앰
    delete from public.tt_sessions where id = s.id;
    select * into prev from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
    update public.tt_sessions set ended_at = coalesce(ended_at, now()) where id = prev.id;
    v_reason := coalesce(prev.end_reason, 'ungraded');
  end if;
  v_status := case v_reason when 'done' then 'done' when 'unsolved' then 'paused_unsolved' else 'paused_ungraded' end;
  if v_status = 'done' and public.tt_blank_count(p_grading) > 0 then v_status := 'paused_ungraded'; end if;
  update public.tt_gradings set status = v_status, updated_at = now() where id = p_grading;
  perform public.tt_log('grading_cancel', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'marks', n, 'round', s.round, 'session', s.no, 'kept_session', v_reopen is not null));
  return jsonb_build_object('ok', true, 'result', 'reverted', 'status', v_status, 'marks', n, 'paths', '[]'::jsonb);
end $$;

revoke all on function public.tt_marks_eff(bigint) from anon;
revoke all on function public.tt_blank_count(bigint) from anon;
revoke all on function public.tt_cancel_grading(bigint, boolean) from anon;
