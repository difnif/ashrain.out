-- ashrain.out — 경시 대비 (2026-11) 마이그레이션
-- 흐름: 채팅방에서 PDF → 문항 패키지 JSON(정답·해설·문항 특성) → 관리자 「경시」 탭 가져오기
--       → 응시자·응답 입력(앱이 정오 판정) → [분석용 내보내기] md → 채팅방에서 학생 분석.
-- 앱은 AI 를 부르지 않는다. 표는 전부 관리자 전용(읽기·쓰기 모두 is_admin()).
-- SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

-- ── 1. 시험 세트 (가져오기 JSON 한 개 = 한 행) ──────────────────────────
create table if not exists public.contest_sets (
  id           uuid primary key default gen_random_uuid(),
  code         text not null unique,                 -- 예: KU-2025-M2
  title        text not null,
  contest      text,                                 -- 대회명
  year         integer,
  round        text,                                 -- 회차·예선/본선 등
  grade_label  text,                                 -- 대상 (중2 등)
  test_date    date,
  n_items      integer not null default 0,
  max_score    numeric not null default 0,
  spec         jsonb,                                -- 가져온 JSON 전체 (원본 보관). PDF만 먼저 올린 세트는 null
  files        jsonb not null default '[]'::jsonb,   -- 프린트 파일 [{name, path, kind:'problem'|'answer'|'solution'|'etc', size}]
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
comment on table public.contest_sets is '경시 대비 — 채팅방에서 만든 문항 패키지 JSON. 문항 원문·해설이 있어 관리자만 읽는다.';

-- 이미 만든 표에도 열 보강 (재실행 안전)
alter table public.contest_sets add column if not exists files jsonb not null default '[]'::jsonb;
alter table public.contest_sets alter column spec drop not null;

-- ── 2. 문항 ──────────────────────────────────────────────────────────────
create table if not exists public.contest_items (
  set_id       uuid not null references public.contest_sets(id) on delete cascade,
  no           integer not null,
  points       numeric not null default 1,
  answer_type  text not null default 'int' check (answer_type in ('choice','int','text')),
  n_choices    integer,                              -- 객관식 보기 수
  accept       text[] not null,                      -- 정답(정규화 전 원형). 여럿이면 모두 정답
  text         text,                                 -- 발문 원문 (관리자 전용, 기계 지표 계산용)
  features     jsonb not null default '{}'::jsonb,   -- 채팅방이 판단한 특성 (단원·영역·유형·난이도 근거…)
  metrics      jsonb not null default '{}'::jsonb,   -- 앱이 원문에서 센 지표 (글자 수·문장 수·수식 수…)
  solution     jsonb,                                -- 해설
  primary key (set_id, no)
);
comment on table public.contest_items is '경시 대비 문항 — features 는 채팅방 판단, metrics 는 앱 계산.';

-- ── 3. 응시자 (앱 계정과 별개, 이름만으로) ───────────────────────────────
create table if not exists public.contest_takers (
  id           uuid primary key default gen_random_uuid(),
  seq          bigint generated always as identity,  -- 익명 코드 S0001 의 번호
  name         text not null,
  grade        text not null default '',          -- 빈 문자열 = 미기재 (unique 를 위해 null 대신)
  user_id      uuid references auth.users(id) on delete set null,  -- 필요하면 나중에 연결
  memo         text,
  created_at   timestamptz not null default now(),
  unique (name, grade)
);
comment on table public.contest_takers is '경시 대비 응시자 — 내보내기에는 익명 코드(S+seq)만 나간다. 실명은 앱 안에서만.';

-- ── 4. 응답 ──────────────────────────────────────────────────────────────
create table if not exists public.contest_responses (
  set_id       uuid not null references public.contest_sets(id) on delete cascade,
  taker_id     uuid not null references public.contest_takers(id) on delete cascade,
  item_no      integer not null,
  response     text,                                 -- 학생이 쓴 답 (빈칸 = 무응답)
  is_correct   boolean,                              -- 무응답이면 null
  updated_at   timestamptz not null default now(),
  primary key (set_id, taker_id, item_no)
);
create index if not exists contest_responses_taker on public.contest_responses (taker_id);

-- ── 5. RLS — 관리자 전용 ─────────────────────────────────────────────────
alter table public.contest_sets      enable row level security;
alter table public.contest_items     enable row level security;
alter table public.contest_takers    enable row level security;
alter table public.contest_responses enable row level security;

drop policy if exists contest_sets_admin on public.contest_sets;
create policy contest_sets_admin on public.contest_sets for all to authenticated
  using (public.is_admin()) with check (public.is_admin());
drop policy if exists contest_items_admin on public.contest_items;
create policy contest_items_admin on public.contest_items for all to authenticated
  using (public.is_admin()) with check (public.is_admin());
drop policy if exists contest_takers_admin on public.contest_takers;
create policy contest_takers_admin on public.contest_takers for all to authenticated
  using (public.is_admin()) with check (public.is_admin());
drop policy if exists contest_responses_admin on public.contest_responses;
create policy contest_responses_admin on public.contest_responses for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

-- ── 6. 프린트 파일 저장소 (비공개, 관리자만) ─────────────────────────────
insert into storage.buckets (id, name, public) values ('contest-files', 'contest-files', false)
on conflict (id) do nothing;

drop policy if exists contest_files_admin_read on storage.objects;
create policy contest_files_admin_read on storage.objects
  for select to authenticated using (bucket_id = 'contest-files' and public.is_admin());
drop policy if exists contest_files_admin_insert on storage.objects;
create policy contest_files_admin_insert on storage.objects
  for insert to authenticated with check (bucket_id = 'contest-files' and public.is_admin());
drop policy if exists contest_files_admin_update on storage.objects;
create policy contest_files_admin_update on storage.objects
  for update to authenticated using (bucket_id = 'contest-files' and public.is_admin());
drop policy if exists contest_files_admin_delete on storage.objects;
create policy contest_files_admin_delete on storage.objects
  for delete to authenticated using (bucket_id = 'contest-files' and public.is_admin());
