-- ashrain.out — 시록고 강사도구 (2026-11) · 하위 문제 (1)·(2)·(3) 따로 채점 — 이미 등록한 프린트의 문항 줄 다시 짜기
-- 채점 단위 = 문항 줄(tt_print_items). 하위 문제가 있는 문제는 하위 문제마다 한 줄(같은 그림 · label 「3 (1)」).
-- 새로 변환 · 등록하는 프린트는 앱이 처음부터 나눠 넣고, 이 함수는 이미 있는 프린트를 나누거나 다시 묶을 때 쓴다.
--
-- p_layout: [{"seq":1,"from":1,"label":"1","answer":"3","choice":false,"hash":"…"},
--            {"seq":2,"from":2,"label":"2 (1)","answer":"12","choice":false,"hash":"…#1","points":4}, …]
--   seq  = 새 채점 단위 번호(1부터 차례), from = 그림 · 정답 그림 · 해설 · 매긴 기록을 물려받을 지금 줄의 seq.
--   points 를 안 주면 from 줄 것 그대로.
-- 한 번에(중간에 실패하면 모두 되돌림):
--   ① 문항 줄을 새 배치로(그림 · 정답 그림 · 해설 · 유형 · 정답률 · 자리 정보는 from 줄 것)
--   ② 이 프린트의 채점 기록(tt_marks)을 from 을 따라 옮김 — 한 줄을 여러 하위 문제로 나누면 그 기록을 하위 문제마다 같은 결과로 복사
--   ③ 다시 풀기 대상(tt_sessions.targets)도 같이 옮김 ④ n_items · n_choice
-- 함수는 부른 사람 권한(RLS 그대로 — 본인 것만). SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

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
    insert into public.tt_marks (owner, grading_id, session_no, seq, result, answer, at)
    select m.owner, m.grading_id, m.session_no, (e->>'seq')::int, m.result, m.answer, m.at
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

revoke all on function public.tt_relayout_items(bigint, jsonb) from anon;
