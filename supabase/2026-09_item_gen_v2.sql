-- ashrain.out — 생성 문항 수납 + 라벨 그릇 마이그레이션 (2026-09, v2)
--
-- 근거 문서
--   · 「문항 생성 시스템 설계 문서 v0.1」 §8 스키마 초안 (attempts·user_ability·item_difficulty·
--     template_calib·math_calib·item_stats·segment_stats, θ/b 분리, content_key 개편)
--   · 「문항 · 유저 라벨 / 분석 알고리즘 리스트업 v2」 (L-01~38 / U-01~39 / A-01~28)
--
-- 이 파일은 **한 번에 실행**하면 되도록 짜 두었다. 트랜잭션 안이라 중간에 실패하면 전부 되돌아간다.
-- 실행 위치: Supabase SQL Editor.
--
-- ─────────────────────────────────────────────────────────────────────────────
-- 왜 필요한가 — 지금 test_items 로는 생성 문항을 담을 수 없다
--   ① figure 열이 없다        → 도형이 있는 문항을 아예 넣을 수 없음
--   ② labels 열이 없다        → 라벨을 tags(text[])에 납작하게만 넣게 됨
--   ③ content_key = md5(question + choices) 인 **생성 열** 이라, 문면이 같고 그림의 수치만
--      다른 문항이 전부 같은 문항으로 병합·삭제된다.
--      실측: 삼각형 각도 문항을 그림만 바꿔 생성했더니 300건 중 1건만 살아남았다.
--   ④ 실측 난이도(b)·능력(θ)을 담을 자리가 없다 → 출제 알고리즘 select.py 가 선행 조건 미충족
--
-- 설계 결정 (설계문서 §8과 다른 점 하나)
--   문서는 `content_key = template_id:param_index` 로 바꾸자고 했지만, 그러면 수제 문항
--   (template_id 없음)과 AdminItemGen 의 upsert(on_conflict=test_type,content_key)가 깨진다.
--   그래서 **둘로 나눈다**:
--     · content_key : 지금처럼 표면 해시. 단 **figure 를 포함**하도록 정의만 고친다 (③ 해결)
--     · item_key    : 'template_id:param_index' 엄격 키. 생성 문항만 채우고 unique.
--   두 키가 각각 "표면 중복"과 "생성 중복"을 맡는다. 기존 코드는 그대로 돌아간다.
-- ─────────────────────────────────────────────────────────────────────────────

begin;

-- ══════════════════════════════════════════════════════ 1. test_items 확장
alter table public.test_items
  add column if not exists figure       jsonb,
  add column if not exists labels       jsonb,
  add column if not exists item_key     text,
  add column if not exists math_key     text,
  add column if not exists cost         int,
  add column if not exists template_id  text,
  add column if not exists param_index  bigint,
  add column if not exists prereq       text[]  not null default '{}',
  add column if not exists flag         text;          -- 'broken' 이면 자동 출제 제외

comment on column public.test_items.figure  is 'figure DSL 배열. 생성 문항은 figsvg 정규 인자(v1.6)만 — genkit/figspec.py 가 관문.';
comment on column public.test_items.labels  is '라벨 L-01~L-49 (registry: labels-v2). genkit/labels.py 참조. C군(L-25~38)은 item_stats 쪽.';
comment on column public.test_items.item_key is '엄격 키 template_id:param_index — 생성 문항의 유일성. 수제 문항은 null.';
comment on column public.test_items.math_key is '의미 키. 표면이 달라도 수학이 같으면 같은 값. 거부 기준이 아니라 시험지 다양성 예산(세트당 ≤2).';
comment on column public.test_items.cost     is '중간 계산값 비용(설계문서 v0.1 §1). difficulty(L-06 예상)의 산출 근거이며 실측 b와 별개.';
comment on column public.test_items.flag     is 'broken = 예측 정답률과 실측이 크게 어긋남(정답 키 오류·중의성 의심). 출제에서 제외하고 리뷰 큐로.';

-- ── content_key 재정의: figure 포함 (생성 열이라 drop 후 재생성해야 한다)
-- 기존 행은 figure 가 null 이므로 새 정의가 만드는 문자열은 "…choices" 뒤에 공백 하나가 더 붙을 뿐이고,
-- btrim + regexp_replace 를 거치면 **옛 값과 완전히 같은 해시**가 나온다. 즉 기존 400건의 content_key 는
-- 값이 바뀌지 않고, 유니크 충돌도 생기지 않는다. (그래도 트랜잭션 안이라 실패하면 전부 되돌아간다.)
alter table public.test_items drop column if exists content_key;   -- 의존 인덱스도 함께 사라진다
alter table public.test_items
  add column content_key text
  generated always as (
    md5(btrim(regexp_replace(
      question || ' ' || coalesce(choices::text, '') || ' ' || coalesce(figure::text, ''),
      '\s+', ' ', 'g')))
  ) stored;
create unique index if not exists test_items_type_content_uq
  on public.test_items (test_type, content_key);      -- 원래 이름 그대로 복구

create unique index if not exists test_items_item_key_uq on public.test_items (item_key) where item_key is not null;
create index if not exists ti_math_key on public.test_items (math_key);
create index if not exists ti_template on public.test_items (template_id);
create index if not exists ti_flag     on public.test_items (flag) where flag is not null;
create index if not exists ti_labels   on public.test_items using gin (labels jsonb_path_ops);

-- source 에 'seed' 추가 (체크 제약이 있다면 넓힌다 — 없으면 이 블록은 그냥 지나간다)
do $$
declare cname text;
begin
  select con.conname into cname
  from pg_constraint con join pg_class c on c.oid = con.conrelid
  where c.relname = 'test_items' and con.contype = 'c'
    and pg_get_constraintdef(con.oid) ilike '%source%';
  if cname is not null then
    execute format('alter table public.test_items drop constraint %I', cname);
  end if;
end $$;
alter table public.test_items
  add constraint test_items_source_check
  check (source in ('manual', 'template', 'seed'));

-- ══════════════════════════════════════════════════════ 2. 틀·시드 보관
alter table public.item_templates
  add column if not exists dims       int[],
  add column if not exists type_axis  jsonb,
  add column if not exists verified_at timestamptz;

create table if not exists public.item_seeds (
  seed_id         text primary key,
  title           text,
  unit_id         text,
  concept_ids     text[] not null default '{}',
  schema_id       uuid,
  source_item_ids uuid[] not null default '{}',
  geometry        boolean,
  spec            jsonb not null,        -- 시드 JSON 원본 (itemfactory/seeds/*.json 과 같은 내용)
  builder_version text,
  status          text not null default 'draft',   -- draft | active | retired
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
comment on table public.item_seeds is
  'Claude가 쓴 시드 명세. 로컬 genkit이 이걸 받아 수치변주로 실체화한다. 파일과 DB 중 하나만 있어도 되지만 둘을 맞춰 둔다.';

-- ══════════════════════════════════════════════════════ 3. 응답 원장 (U-28 · 모든 분석의 원자)
create table if not exists public.attempts (
  id             bigserial primary key,
  user_id        uuid not null references auth.users(id) on delete cascade,
  item_id        uuid not null references public.test_items(id) on delete cascade,
  set_id         text,                    -- 연습 세트·시험 식별
  seq            int,                     -- 세트 안의 순서 (피로도 보정)
  ts             timestamptz not null default now(),

  -- 무엇을 냈나
  raw_answer     text,                    -- 학생이 실제로 쓴 것 그대로 (판정 규칙이 바뀌어도 재채점 가능)
  correct        boolean not null,
  chosen_index   int,                     -- 객관식에서 고른 번호(1~5)
  chosen_choice  text,                    -- 고른 보기 원문
  distractor_tag text,                    -- ★ 응답 시점에 박는다. labels.L42_distractor_map 으로 사상.
                                          --   나중에 템플릿이 바뀌면 역추적이 불가능하므로 여기 기록.

  -- 어떻게 냈나
  elapsed_sec    int,                     -- 기록만 한다. θ 추정에는 쓰지 않는다(설계문서 §6).
  first_input_ms int,                     -- 표시~첫 입력 (읽고 막힌 시간과 쓰는 시간 분리)
  edits_n        int not null default 0,
  hint_level     int not null default 0,  -- 본 힌트 단계 (0 = 안 봄)
  solution_seen  boolean not null default false,
  retry_n        int not null default 0,
  confidence     int,                     -- 자기보고 확신도 1~3 (선택). '확신했는데 틀림'이 가장 강한 신호.

  -- 어디서 냈나
  device         text,                    -- mobile | tablet | desktop  (U-16)
  session_id     text,

  -- 재추정을 위한 스냅샷 (설계문서 §6 — 모델 교체·재추정 시 원본)
  theta_at       double precision,
  b_at           double precision,
  labels_snapshot jsonb
);
create index if not exists attempts_user_ts on public.attempts (user_id, ts desc);
create index if not exists attempts_item    on public.attempts (item_id);
create index if not exists attempts_tag     on public.attempts (distractor_tag) where distractor_tag is not null;
create index if not exists attempts_set     on public.attempts (set_id) where set_id is not null;

alter table public.attempts enable row level security;
drop policy if exists attempts_own_select on public.attempts;
drop policy if exists attempts_own_insert on public.attempts;
create policy attempts_own_select on public.attempts for select using (auth.uid() = user_id);
create policy attempts_own_insert on public.attempts for insert with check (auth.uid() = user_id);
-- 관리자 정책은 기존 admin 판별 방식에 맞춰 별도로 추가할 것.

-- ══════════════════════════════════════════════════════ 4. 능력·난이도 (θ/b 분리 · Elo 온라인)
create table if not exists public.user_ability (
  user_id    uuid not null references auth.users(id) on delete cascade,
  concept_id text not null,               -- ★ θ는 개념 단위 (전역 하나로는 방정식○/도형× 를 설명 못 함)
  theta      double precision not null default 0,
  n          int not null default 0,
  updated_at timestamptz not null default now(),
  primary key (user_id, concept_id)
);
alter table public.user_ability enable row level security;
drop policy if exists ua_own on public.user_ability;
create policy ua_own on public.user_ability for select using (auth.uid() = user_id);

create table if not exists public.item_difficulty (
  item_id  uuid primary key references public.test_items(id) on delete cascade,
  b        double precision not null default 0,
  b_prior  double precision not null default 0,   -- 3층 사전값에서 상속받은 출발점
  n        int not null default 0,
  se       double precision,
  updated_at timestamptz not null default now()
);
create table if not exists public.template_calib (
  template_id text primary key,
  b0 double precision not null default 0,
  n  int not null default 0,
  updated_at timestamptz not null default now()
);
create table if not exists public.math_calib (
  math_key text primary key,
  b1 double precision not null default 0,
  n  int not null default 0,
  updated_at timestamptz not null default now()
);
comment on table public.item_difficulty is
  '실측 난이도 b (L-25). test_items.difficulty(L-06 예상)와 **영구 분리** — 덮어쓰지 말 것. 둘의 차이 L-35가 생성기 성적표.';
comment on table public.template_calib is '3층 사전값 2층 — cost → b0. 데이터 없는 새 문항이 상속받는다.';
comment on table public.math_calib     is '3층 사전값 3층 — math_key 단위 b1.';

-- ══════════════════════════════════════════════════════ 5. 통계 그릇 (문항 QA · 세그먼트)
create table if not exists public.item_stats (
  item_id     uuid primary key references public.test_items(id) on delete cascade,
  n           int not null default 0,
  n_correct   int not null default 0,
  p_correct   numeric(5,3),
  median_sec  int,
  choice_dist jsonb,                       -- {"①":12,"②":40,…} 선택률 0%인 보기 = 죽은 선택지
  hint_used   int not null default 0,
  give_up     int not null default 0,
  updated_at  timestamptz not null default now()
);
comment on table public.item_stats is
  '문항 단위 통계는 측정용이 아니라 **그물**이다. 예측 70% vs 실측 20% = 난이도가 아니라 고장(정답 키 오류·중의성). 세그먼트 분해 금지(표본 부족).';

create table if not exists public.segment_stats (
  id           bigserial primary key,
  scope        text not null,              -- 'template' | 'type_axis' | 'math_key'
  scope_key    text not null,
  grade        text,
  region       text,
  gender       text,
  n            int not null default 0,
  p_correct    numeric(5,3),
  dif_residual double precision,           -- θ 통제 후 잔차 — 튀면 문항 결함(DIF) 신호
  updated_at   timestamptz not null default now()
);
-- 세그먼트 조합은 null 을 허용하므로 표현식 유니크 인덱스로 잡는다 (PK 에는 coalesce 를 쓸 수 없다)
create unique index if not exists segment_stats_uq on public.segment_stats
  (scope, scope_key, coalesce(grade, ''), coalesce(region, ''), coalesce(gender, ''));
comment on table public.segment_stats is
  '세그먼트는 **편향 문항 탐지(DIF) 전용**. 출제 알고리즘 입력 금지. 집계 셀 n < 20 은 노출하지 않는다(A-18 억제 게이트).';

-- ══════════════════════════════════════════════════════ 6. 파생 뷰 (P2 — 원장은 attempts 하나)
create or replace view public.v_item_quality as
select i.id                as item_id,
       i.template_id,
       i.difficulty        as difficulty_prior,
       s.n, s.p_correct,
       d.b                 as difficulty_measured,
       (i.difficulty - 1) * 0.25 - coalesce(d.b, 0) as prior_gap,   -- L-35 난이도 이동폭
       i.flag
from public.test_items i
left join public.item_stats s      on s.item_id = i.id
left join public.item_difficulty d on d.item_id = i.id;

create or replace view public.v_misconception_hits as
select a.user_id, a.distractor_tag as misconception, count(*) as n, max(a.ts) as last_at
from public.attempts a
where a.distractor_tag is not null
group by 1, 2;

create or replace view public.v_dead_choices as
-- 선택률 0%인 보기 = 템플릿의 오개념 설계 결함 → 그 틀 전체를 고치면 일괄 개선된다
select i.template_id, i.id as item_id, s.n, s.choice_dist
from public.test_items i join public.item_stats s on s.item_id = i.id
where s.n >= 30 and s.choice_dist is not null
  and exists (select 1 from jsonb_each_text(s.choice_dist) kv where kv.value = '0');

commit;

-- ─────────────────────────────────────────────────────────────────────────────
-- 실행 후 확인 (읽기 전용)
--   select column_name, is_generated from information_schema.columns
--    where table_name='test_items' and column_name in ('figure','labels','item_key','math_key','cost','content_key');
--   select count(*) from public.test_items;                       -- 400 그대로여야 한다
--   select indexname from pg_indexes where tablename='test_items';
--
-- 되돌리기 (필요할 때만)
--   content_key 정의를 원래대로 되돌리려면 위 §1의 drop/add 두 문장에서
--   " || ' ' || coalesce(figure::text,'')" 부분만 빼고 다시 실행하면 된다.
-- ─────────────────────────────────────────────────────────────────────────────
