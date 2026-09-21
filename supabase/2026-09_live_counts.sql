-- ashrain.out — 공개 문항 수 집계 함수 (2026-09-21)
-- 왜: 공부하기 화면(개념 고르기·시험 범위 고르기)이 문항 수를 "행 20,000개를 내려받아 클라에서 세는" 방식(studyCache.fetchCounts)으로 바뀌었는데,
--     live 문항이 103,000건이라 20,000행 밖의 학기·개념은 0으로 세어져 「준비 중」으로 잘못 뜬다(예: 고1-1·고1-2·고2-2·고3-3 전부 0).
-- 이 함수는 서버에서 한 번에 센다. 앱은 supabase.rpc('live_counts', …) 를 먼저 쓰고, 함수가 없으면 예전 방식으로 물러난다.
-- SQL Editor 에서 이 파일을 그대로 실행하면 된다. 표·정책은 바꾸지 않는다.
--   · security invoker — 호출한 학생의 RLS(ti_read: status='live')가 그대로 적용된다.
--   · 인자는 studyCache 의 필터와 같다: 문항형 목록, 채점기준표 있는 것만, 그림 있는 것만, 난이도.

create or replace function public.live_counts(
  p_qtypes      text[]  default null,
  p_with_rubric boolean default false,
  p_with_figure boolean default false,
  p_difficulty  integer default null
) returns jsonb
language sql
stable
security invoker
set search_path = public
as $$
  with rows as (
    select unit_id, concept_ids
    from public.test_items
    where status = 'live'
      and (p_qtypes is null or qtype = any (p_qtypes))
      and (not p_with_rubric or (solution -> 'rubric') is not null)
      and (not p_with_figure or figure is not null)
      and (p_difficulty is null or difficulty = p_difficulty)
  ),
  u as (select unit_id, count(*) as n from rows where unit_id is not null group by unit_id),
  c as (select cid, count(*) as n from rows, unnest(coalesce(concept_ids, '{}'::text[])) as cid group by cid)
  select jsonb_build_object(
    'unit',    coalesce((select jsonb_object_agg(unit_id, n) from u), '{}'::jsonb),
    'concept', coalesce((select jsonb_object_agg(cid, n) from c), '{}'::jsonb)
  );
$$;

comment on function public.live_counts(text[], boolean, boolean, integer)
  is '공개(live) 문항 수를 학기별·개념별로 한 번에 센다 — 공부하기 화면용 (studyCache.js)';

grant execute on function public.live_counts(text[], boolean, boolean, integer) to authenticated, anon;
