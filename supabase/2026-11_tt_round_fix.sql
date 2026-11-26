-- ashrain.out — 시록고 강사도구 (2026-11) · 2차(다음 차)를 시작한 뒤에도 1차(앞 차) 결과 고치기
-- 매긴 기록(tt_marks)은 덧붙여 쌓인다. 문항의 한 차 결과 = 그 차의 마지막 기록,
-- 지금(최종) 결과 = 기록이 있는 가장 늦은 차의 결과. 앞 차를 고친 기록은 id 가 더 커도 늦은 차 결과를 덮지 않는다.
-- (이제까지 쌓인 기록은 차가 늦을수록 id 도 커서, 지금 결과를 차 순서로 골라도 전과 같다.)
-- 함수는 부른 사람 권한(RLS 그대로 — 본인 것만). SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

-- 문항마다 지금 결과 = 기록이 있는 가장 늦은 차의 마지막 기록 (다음 차 다시 풀 문항을 고를 때 씀)
create or replace function public.tt_current(p_grading bigint)
returns table (seq integer, result text, answer text, session_no integer)
language sql stable security invoker set search_path = public as $$
  select distinct on (m.seq) m.seq, m.result, m.answer, m.session_no
  from public.tt_marks m
  left join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
  where m.grading_id = p_grading
  order by m.seq, coalesce(x.round, 1) desc, m.id desc;
$$;

-- 앞 차 고치기: p_round 차(이번 차보다 앞)의 그 문항 결과를 p_result 로 — 그 차의 마지막 회차에 기록을 덧붙인다.
--   p_answer 가 null 이면 그 차에 적어 둔 답을 그대로 둔다.
--   이번 차가 다시 풀기이고 그 문항을 이번 차에 아직 안 매겼으면: 고친 결과로 더는 틀리거나 안 푼 문항이 아니면
--   이번 차 다시 풀 문항에서 뺀다(이번 차에 이미 매긴 문항은 그대로 — 그 결과가 최종).
-- 돌려주는 것: {ok, changed(기록을 더했는지), removed(이번 차에서 뺐는지),
--              can_add(틀리거나 안 푼 문항이 됐는데 이번 차 대상이 아님 → tt_retry_add 로 넣을 수 있음)}
create or replace function public.tt_mark_round(p_grading bigint, p_round integer, p_seq integer, p_result text, p_answer text default null)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  g public.tt_gradings; last public.tt_sessions; rs public.tt_sessions; v_prev public.tt_marks;
  v_before text; v_changed boolean := false; v_removed boolean := false; v_can_add boolean := false;
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

  -- 이번 차(다시 풀기)의 다시 풀 문항 맞추기 — 이번 차에 이미 매긴 문항은 그대로
  if last.kind = 'retry' and not exists (
       select 1 from public.tt_marks m join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
        where m.grading_id = p_grading and m.seq = p_seq and x.round = last.round) then
    select m.result into v_before from public.tt_marks m
      join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
     where m.grading_id = p_grading and m.seq = p_seq and x.round < last.round
     order by x.round desc, m.id desc limit 1;
    if p_seq = any(coalesce(last.targets, '{}'::integer[])) then
      if coalesce(v_before, '') not in ('X', 'U') then
        update public.tt_sessions set targets = array_remove(targets, p_seq) where grading_id = p_grading and round = last.round;
        v_removed := true;
        perform public.tt_log('retry_target_remove', g.student_id, g.print_id,
          jsonb_build_object('grading', p_grading, 'round', last.round, 'seq', p_seq));
      end if;
    elsif v_before in ('X', 'U') and last.ended_at is null then
      v_can_add := true;
    end if;
  end if;
  if v_changed or v_removed then update public.tt_gradings set updated_at = now() where id = p_grading; end if;
  return jsonb_build_object('ok', true, 'changed', v_changed, 'removed', v_removed, 'can_add', v_can_add);
end $$;

-- 이번 차(다시 풀기)에 문항 넣기 — 앞 차를 고쳐 틀리거나 안 푼 문항이 된 것을 이번 차에서도 다시 풀게 할 때.
-- 이번 차가 열려 있어야(채점 중) 한다. 돌려주는 것: {ok, added}
create or replace function public.tt_retry_add(p_grading bigint, p_seq integer)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; last public.tt_sessions; v_before text;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  select * into last from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if last.id is null or last.kind <> 'retry' then raise exception '다시 풀기 차가 아니에요' using errcode = 'P0001'; end if;
  if last.ended_at is not null then
    raise exception '%차 채점이 닫혀 있어요 — 채점을 다시 연 뒤 넣어 주세요', last.round using errcode = 'P0001';
  end if;
  if p_seq = any(coalesce(last.targets, '{}'::integer[])) then return jsonb_build_object('ok', true, 'added', false); end if;
  select m.result into v_before from public.tt_marks m
    join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
   where m.grading_id = p_grading and m.seq = p_seq and x.round < last.round
   order by x.round desc, m.id desc limit 1;
  if coalesce(v_before, '') not in ('X', 'U') then
    raise exception '앞 차까지 틀리거나 안 푼 문항만 다시 풀기에 넣어요' using errcode = 'P0001';
  end if;
  update public.tt_sessions
     set targets = (select array_agg(distinct t order by t) from unnest(coalesce(targets, '{}'::integer[]) || p_seq) t)
   where grading_id = p_grading and round = last.round;
  update public.tt_gradings set status = 'open', updated_at = now() where id = p_grading;
  perform public.tt_log('retry_target_add', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'round', last.round, 'seq', p_seq));
  return jsonb_build_object('ok', true, 'added', true);
end $$;

revoke all on function public.tt_mark_round(bigint, integer, integer, text, text) from anon;
revoke all on function public.tt_retry_add(bigint, integer) from anon;
