-- ashrain.out — 시록고 강사도구 (2026-11) · 「푼 만큼만 매기고 넘어가기」(패스)
-- 문항이 많은 프린트이거나 학습 계획 때문에 일부만 풀고 넘어갈 때 쓴다.
-- ① 문항 결과에 P(넘어감)를 더한다. 지금 결과가 P인 문항은 다시 풀기(2차 …) · 오답 프린트 · 정답률에 넣지 않는다.
--    나중에 풀어 오면 「채점 수정」으로 다시 열어 O · X로 매기면 된다(가장 늦은 기록이 지금 결과).
-- ② tt_pass_grading(채점, 넘길 문항들): 이번 차에 남은 문항을 넘기고 채점을 끝낸다.
--    1차 — 아직 안 매긴 문항과 지난 회차에 '안 풂'으로 남은 문항(화면이 보낸 것 중 지금 결과가 없거나 안 풂인 것)을 P로 매긴다.
--    2차부터 — 이번 차 다시 풀 문항 중 이번 차에 아직 안 매긴 것을 이번 차에서 뺀다(앞 차 결과 그대로). 이번 차에 매긴 것이 없으면
--             넘기지 않고 「채점 취소」를 쓰게 한다.
--    업무 기록 grading_pass 하나(되돌릴 때 씀). 돌려주는 것: {ok, status, n, seqs, event}
-- ③ tt_unpass_grading(업무 기록 id): 그 넘기기를 되돌려 넘기기 전 상태로 — 그 뒤 채점을 다시 열거나 넘긴 문항을 매겼으면 되돌리지 않는다.
-- 함수는 부른 사람 권한(RLS 그대로 — 본인 것만). 여러 번 실행해도 안전.

do $$
declare c text;
begin
  for c in select conname from pg_constraint
            where conrelid = 'public.tt_marks'::regclass and contype = 'c' and pg_get_constraintdef(oid) ilike '%result%' loop
    execute format('alter table public.tt_marks drop constraint %I', c);
  end loop;
end $$;
alter table public.tt_marks add constraint tt_marks_result_check check (result in ('O', 'X', 'U', 'P'));

create or replace function public.tt_pass_grading(p_grading bigint, p_seqs integer[])
returns jsonb language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; s public.tt_sessions; v_seqs integer[]; v_status text; v_id bigint; t integer;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if g.status = 'done' then raise exception '이미 다 끝난 채점이에요' using errcode = 'P0001'; end if;
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if s.id is null then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if s.kind = 'retry' then
    if not exists (select 1 from public.tt_marks m join public.tt_sessions y on y.grading_id = m.grading_id and y.no = m.session_no
                    where m.grading_id = p_grading and y.round = s.round
                      and m.seq = any(coalesce(s.targets, '{}'::integer[]))) then
      raise exception '%차에 매긴 문항이 없어요 — 넘기지 말고 「채점 취소」로 이번 차를 없애 주세요', s.round using errcode = 'P0001';
    end if;
    select array_agg(x order by x) into v_seqs from unnest(coalesce(s.targets, '{}'::integer[])) x
     where x = any(coalesce(p_seqs, '{}'::integer[]))
       and not exists (select 1 from public.tt_marks m join public.tt_sessions y on y.grading_id = m.grading_id and y.no = m.session_no
                        where m.grading_id = p_grading and m.seq = x and y.round = s.round);
  else
    select array_agg(i.seq order by i.seq) into v_seqs from public.tt_print_items i
     where i.print_id = g.print_id and i.seq = any(coalesce(p_seqs, '{}'::integer[]))
       and coalesce((select c.result from public.tt_current(p_grading) c where c.seq = i.seq), '') in ('', 'U');
  end if;
  if v_seqs is null then raise exception '넘길 문항이 없어요' using errcode = 'P0001'; end if;

  if s.kind = 'retry' then
    update public.tt_sessions
       set targets = (select coalesce(array_agg(x order by x), '{}'::integer[]) from unnest(coalesce(targets, '{}'::integer[])) x where not (x = any(v_seqs)))
     where grading_id = p_grading and round = s.round;
    foreach t in array v_seqs loop          -- 채점 취소가 되돌릴 수 있게(다시 풀 문항 바뀐 기록)
      perform public.tt_log('retry_target_remove', g.student_id, g.print_id,
        jsonb_build_object('grading', p_grading, 'round', s.round, 'seq', t, 'by', 'pass'));
    end loop;
  else
    insert into public.tt_marks(grading_id, session_no, seq, result) select p_grading, s.no, x, 'P' from unnest(v_seqs) x;
  end if;

  update public.tt_sessions set ended_at = coalesce(ended_at, now()), end_reason = 'done' where id = s.id;
  v_status := case when public.tt_blank_count(p_grading) > 0 then 'paused_ungraded' else 'done' end;
  update public.tt_gradings set status = v_status, updated_at = now() where id = p_grading;
  insert into public.tt_events(kind, student_id, print_id, detail)
    values ('grading_pass', g.student_id, g.print_id,
            jsonb_build_object('grading', p_grading, 'round', s.round, 'session', s.no, 'kind', s.kind, 'seqs', to_jsonb(v_seqs),
                               'n', cardinality(v_seqs), 'was', g.status, 'was_reason', s.end_reason, 'was_ended', s.ended_at, 'status', v_status))
    returning id into v_id;
  return jsonb_build_object('ok', true, 'status', v_status, 'n', cardinality(v_seqs), 'seqs', to_jsonb(v_seqs), 'event', v_id);
end $$;

create or replace function public.tt_unpass_grading(p_event bigint)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare
  ev public.tt_events; d jsonb; g public.tt_gradings; s public.tt_sessions;
  v_seqs integer[]; v_add integer[]; v_round integer; v_id bigint; v_status text; n integer := 0; t integer;
begin
  select * into ev from public.tt_events where id = p_event and kind = 'grading_pass';
  if not found then raise exception '그런 기록이 없어요' using errcode = 'P0001'; end if;
  d := ev.detail;
  if d ? 'undone_by' then raise exception '이미 되돌린 기록이에요' using errcode = 'P0001'; end if;
  select * into g from public.tt_gradings where id = (d->>'grading')::bigint;
  if not found then raise exception '그 채점 기록이 지워져서 되돌릴 수 없어요' using errcode = 'P0001'; end if;
  select * into s from public.tt_sessions where grading_id = g.id order by no desc limit 1;
  if s.no is distinct from (d->>'session')::integer or s.ended_at is null then
    raise exception '넘긴 뒤에 채점을 다시 열어서 되돌릴 수 없어요 — 채점 화면에서 고쳐 주세요' using errcode = 'P0001';
  end if;
  v_round := (d->>'round')::integer;
  select array_agg(x::integer) into v_seqs from jsonb_array_elements_text(coalesce(d->'seqs', '[]'::jsonb)) x;
  if d->>'kind' = 'retry' then
    -- 앞 차 결과가 아직 틀림 · 안 풂인 문항만 다시 이번 차에 넣는다
    select array_agg(x order by x) into v_add from unnest(coalesce(v_seqs, '{}'::integer[])) x
     where (select e.result from public.tt_marks_eff(g.id) e where e.seq = x and e.round < v_round
             order by e.round desc, e.id desc limit 1) in ('X', 'U');
    if v_add is not null then
      update public.tt_sessions
         set targets = (select array_agg(distinct y order by y) from unnest(coalesce(targets, '{}'::integer[]) || v_add) y)
       where grading_id = g.id and round = v_round;
      foreach t in array v_add loop
        perform public.tt_log('retry_target_add', g.student_id, g.print_id,
          jsonb_build_object('grading', g.id, 'round', v_round, 'seq', t, 'by', 'unpass'));
      end loop;
      n := cardinality(v_add);
    end if;
  else
    if exists (select 1 from public.tt_current(g.id) c where c.seq = any(coalesce(v_seqs, '{}'::integer[])) and c.result <> 'P') then
      raise exception '넘긴 뒤에 매긴 문항이 있어서 되돌릴 수 없어요 — 채점 화면에서 고쳐 주세요' using errcode = 'P0001';
    end if;
    delete from public.tt_marks
     where grading_id = g.id and session_no = (d->>'session')::integer and seq = any(coalesce(v_seqs, '{}'::integer[])) and result = 'P';
    get diagnostics n = row_count;
  end if;
  update public.tt_sessions set ended_at = (d->>'was_ended')::timestamptz, end_reason = d->>'was_reason' where id = s.id;
  v_status := coalesce(d->>'was', 'paused_ungraded');
  update public.tt_gradings set status = v_status, updated_at = now() where id = g.id;
  insert into public.tt_events(kind, student_id, print_id, detail)
    values ('grading_unpass', g.student_id, g.print_id, jsonb_build_object('grading', g.id, 'round', v_round, 'n', n, 'undo_of', p_event))
    returning id into v_id;
  update public.tt_events set detail = detail || jsonb_build_object('undone_by', v_id, 'undone_at', now()) where id = p_event;
  return jsonb_build_object('ok', true, 'status', v_status, 'n', n, 'event', v_id);
end $$;

revoke all on function public.tt_pass_grading(bigint, integer[]) from anon;
revoke all on function public.tt_unpass_grading(bigint) from anon;
