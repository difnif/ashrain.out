-- ashrain.out — 문항 검토 화면 「틀별 보기」 집계 (2026-09-22)
-- 왜: 관리자 검토는 문항 하나씩이 아니라 틀(template) 단위로 한다 — 같은 틀은 숫자만 다르다. 그런데 item_templates 표에는
--     시드 틀이 없고(옛 4행뿐) test_items 에 template_id 만 있어서, 틀 목록·건수를 한 번에 세는 함수가 필요하다.
--     PostgREST 는 group by 를 못 하고, 138k 행을 클라로 내려받을 수도 없다.
-- 이 파일을 SQL Editor 에서 그대로 실행하면 된다. 표·정책은 바꾸지 않는다.
--   · 인덱스 (template_id, status) include (id) — 집계가 인덱스만 읽고 끝난다 (heap 스캔 3초 → 수백 ms).
--   · security invoker — 호출자의 RLS 그대로: 관리자는 draft 까지, 학생이 부르면 live 만 세어진다(해가 없음).

create index if not exists ti_tpl_status on public.test_items (template_id, status) include (id);

create or replace function public.admin_template_stats()
returns table (
  template_id  text,
  seed         text,
  n_draft      bigint,
  n_live       bigint,
  sample_id    uuid,
  unit_id      text,
  concept_id   text,
  qtype        text,
  difficulty   integer,
  made_at      timestamptz,
  sample_q     text,
  discriminates text,
  geometry     boolean,
  has_figure   boolean
)
language sql
stable
security invoker
set search_path = public
as $$
  with g as (
    select template_id,
           count(*) filter (where status = 'draft') as n_draft,
           count(*) filter (where status = 'live')  as n_live,
           min(id::text)::uuid                      as sample_id      -- 틀의 표본 문항 (아무거나 하나)
    from public.test_items
    where template_id is not null
    group by template_id
  )
  select g.template_id,
         regexp_replace(g.template_id, '-t\d+$', '') as seed,
         g.n_draft, g.n_live, g.sample_id,
         s.unit_id, s.concept_ids[1] as concept_id, s.qtype, s.difficulty, s.created_at as made_at,
         s.question as sample_q,
         s.labels ->> 'L43_discriminates' as discriminates,
         coalesce((s.labels ->> 'geometry')::boolean, false) as geometry,
         (s.figure is not null) as has_figure
  from g
  join public.test_items s on s.id = g.sample_id;
$$;

comment on function public.admin_template_stats()
  is '틀(template_id)별 draft·live 건수와 표본 문항 — 관리자 문항 검토 화면의 「틀별 보기」 (AdminItemReview.jsx)';

revoke execute on function public.admin_template_stats() from public, anon;
grant execute on function public.admin_template_stats() to authenticated;
