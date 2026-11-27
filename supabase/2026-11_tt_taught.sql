-- ashrain.out — 시록고 강사도구 (2026-11) · 「풀어 줌」 — 선생님이 풀어 준 문제(종이에는 번호에 직사각형 박스)
-- 결과는 맞음(O)으로 그대로 세고, 풀어 준 문제인지만 따로 적는다(tt_marks.taught). 풀어 준 수는 화면 · 보고서에 따로 보여 준다.
-- 매기는 함수는 결과 'T'를 「O + 풀어 줌」으로 받는다(함수 모양은 그대로).
-- ① tt_marks.taught ② tt_mark · tt_mark_round 가 'T'를 받음 ③ tt_relayout_items(하위 문제 나누기)가 풀어 줌도 옮김
-- 함수는 부른 사람 권한(RLS 그대로 — 본인 것만). 여러 번 실행해도 안전.

alter table public.tt_marks add column if not exists taught boolean not null default false;

-- 매기기. p_result '' = 이번 회차에 그 문항을 매긴 기록 지우기(앞 기록이 다시 보임), 'T' = 풀어 줌(맞음으로 셈)
create or replace function public.tt_mark(p_grading bigint, p_seq integer, p_result text, p_answer text default '')
returns void language plpgsql security invoker set search_path = public as $$
declare s public.tt_sessions;
begin
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if s.kind = 'retry' and not (p_seq = any(coalesce(s.targets, array[p_seq]))) then
    raise exception '이번 차에 다시 풀 문항이 아니에요' using errcode = 'P0001';
  end if;
  if coalesce(p_result, '') = '' then
    delete from public.tt_marks where grading_id = p_grading and session_no = s.no and seq = p_seq;
  else
    insert into public.tt_marks(grading_id, session_no, seq, result, answer, taught)
      values (p_grading, s.no, p_seq, case when p_result = 'T' then 'O' else p_result end, coalesce(p_answer, ''), p_result = 'T');
  end if;
  update public.tt_gradings set status = 'open', updated_at = now() where id = p_grading;
end $$;

-- 앞 차 고치기(supabase/2026-11_tt_round_follow.sql 과 같고, 'T' = 풀어 줌을 받음)
create or replace function public.tt_mark_round(p_grading bigint, p_round integer, p_seq integer, p_result text, p_answer text default null)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  g public.tt_gradings; last public.tt_sessions; rs public.tt_sessions; rk public.tt_sessions; v_prev public.tt_marks;
  v_before text; v_changed boolean := false; k integer; v_added integer; v_removed integer[] := '{}'::integer[]; v_status text;
  v_res text; v_taught boolean;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if coalesce(p_result, '') not in ('O', 'X', 'U', 'T') then
    raise exception '앞 차 결과는 O · X · 안 풂 · 풀어 줌 중 하나로 고쳐요' using errcode = 'P0001';
  end if;
  v_res := case when p_result = 'T' then 'O' else p_result end;        -- 풀어 줌 = 맞음 + taught
  v_taught := p_result = 'T';
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
  if v_prev.id is null or v_prev.result is distinct from v_res or coalesce(v_prev.taught, false) is distinct from v_taught
     or (p_answer is not null and v_prev.answer is distinct from p_answer) then
    insert into public.tt_marks(grading_id, session_no, seq, result, answer, taught)
      values (p_grading, rs.no, p_seq, v_res, coalesce(p_answer, v_prev.answer, ''), v_taught);
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

-- 하위 문제 나누기(supabase/2026-11_tt_item_parts.sql 과 같고, 풀어 줌도 옮김)
create or replace function public.tt_relayout_items(p_print bigint, p_layout jsonb)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  n int; n_marks int := 0; gids bigint[]; v_items jsonb; v_marks jsonb;
begin
  if not exists (select 1 from public.tt_prints where id = p_print) then
    raise exception '그런 프린트가 없어요' using errcode = 'P0001';
  end if;
  if jsonb_typeof(p_layout) is distinct from 'array' then
    raise exception '새 배치가 없어요' using errcode = 'P0001';
  end if;
  n := jsonb_array_length(p_layout);
  if n = 0 then raise exception '문항이 하나도 없어요' using errcode = 'P0001'; end if;
  if (select count(distinct (e->>'seq')::int) from jsonb_array_elements(p_layout) e) <> n
     or (select min((e->>'seq')::int) from jsonb_array_elements(p_layout) e) <> 1
     or (select max((e->>'seq')::int) from jsonb_array_elements(p_layout) e) <> n then
    raise exception '새 번호가 1부터 차례가 아니에요' using errcode = 'P0001';
  end if;
  select coalesce(jsonb_agg(to_jsonb(i)), '[]'::jsonb) into v_items from public.tt_print_items i where i.print_id = p_print;
  if exists (select 1 from jsonb_array_elements(p_layout) e
             where not exists (select 1 from jsonb_array_elements(v_items) x where (x->>'seq')::int = (e->>'from')::int)) then
    raise exception '없는 문항에서 물려받으려 해요' using errcode = 'P0001';
  end if;

  -- ① 문항 줄
  delete from public.tt_print_items where print_id = p_print;
  insert into public.tt_print_items (print_id, owner, seq, label, src, src_no, choice, hash, answer, points, topic, tag, rate, png, answer_png, sol_png, scale, origin, page, bbox)
  select p_print, i.owner, (e->>'seq')::int, coalesce(e->>'label', i.label), i.src, i.src_no, coalesce((e->>'choice')::boolean, i.choice),
         case when e ? 'hash' then e->>'hash' else i.hash end, coalesce(e->>'answer', i.answer),
         case when e ? 'points' then nullif(e->>'points', '')::numeric else i.points end,
         i.topic, i.tag, i.rate, i.png, i.answer_png, i.sol_png, i.scale, i.origin, i.page, i.bbox
    from jsonb_array_elements(p_layout) e
    join jsonb_populate_recordset(null::public.tt_print_items, v_items) i on i.seq = (e->>'from')::int
   order by (e->>'seq')::int;

  -- ② 채점 기록 · ③ 다시 풀기 대상
  select array_agg(id) into gids from public.tt_gradings where print_id = p_print;
  if gids is not null then
    select coalesce(jsonb_agg(to_jsonb(m) order by m.id), '[]'::jsonb) into v_marks from public.tt_marks m where m.grading_id = any(gids);
    delete from public.tt_marks where grading_id = any(gids);
    insert into public.tt_marks (owner, grading_id, session_no, seq, result, answer, at, taught)
    select m.owner, m.grading_id, m.session_no, (e->>'seq')::int, m.result, m.answer, m.at, coalesce(m.taught, false)
      from jsonb_populate_recordset(null::public.tt_marks, v_marks) m
      join jsonb_array_elements(p_layout) e on (e->>'from')::int = m.seq
     order by m.id, (e->>'seq')::int;
    get diagnostics n_marks = row_count;
    update public.tt_sessions s
       set targets = (select coalesce(array_agg(distinct (e->>'seq')::int order by (e->>'seq')::int), '{}'::integer[])
                        from unnest(s.targets) t join jsonb_array_elements(p_layout) e on (e->>'from')::int = t)
     where s.grading_id = any(gids) and s.targets is not null;
  end if;

  -- ④ 프린트 문항 수
  update public.tt_prints
     set n_items = n, n_choice = (select count(*) from jsonb_array_elements(p_layout) e
                                   join jsonb_populate_recordset(null::public.tt_print_items, v_items) i on i.seq = (e->>'from')::int
                                  where coalesce((e->>'choice')::boolean, i.choice)),
         updated_at = now()
   where id = p_print;
  perform public.tt_log('items_relayout', null, p_print, jsonb_build_object('items', n, 'marks', n_marks));
  return jsonb_build_object('ok', true, 'items', n, 'marks', n_marks);
end $$;

revoke all on function public.tt_mark(bigint, integer, text, text) from anon;
revoke all on function public.tt_mark_round(bigint, integer, integer, text, text) from anon;
revoke all on function public.tt_relayout_items(bigint, jsonb) from anon;
