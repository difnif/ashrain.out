-- 강사도구 원비표 — 언제부터(그달 1일) · 대상(학년 묶음) · 주당 횟수마다 월 원비. 재원 기록에 주당 횟수를 고르면 그달 원비표로 원비를 채운다.
-- 원비표는 학원 영업 정보라 공개 저장소에 적지 않고 이 표에만 둔다. 여러 번 실행해도 안전.
create table if not exists public.tt_fee_plans (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  start_month date not null check (extract(day from start_month) = 1),            -- 이 달부터(다음 원비표가 시작되기 전까지)
  level       text not null check (char_length(level) between 1 and 40),         -- 대상: 초1 ~ 초6 · 중1 ~ 중3 · 고1 ~ 고3 중 묶음(예: 「초1-4」 「초5-6」 「중」 「고」)
  grades      text[] not null default '{}',                                       -- 대상 학년(예: {초1,초2,초3,초4})
  per_week    integer not null check (per_week between 1 and 7),                  -- 주당 횟수
  minutes     integer check (minutes is null or minutes between 10 and 600),      -- 한 번 수업 길이(분)
  fee         integer not null check (fee between 0 and 100000000),               -- 월 원비(원)
  note        text not null default '' check (char_length(note) <= 200),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (owner, start_month, level, per_week)
);
comment on table public.tt_fee_plans is '강사도구 원비표 — start_month(이 달부터) · level · grades(대상 학년) · per_week · minutes · fee(월 원비). 본인 것만.';
alter table public.tt_student_months add column if not exists per_week integer check (per_week is null or per_week between 1 and 7);   -- 그달 주당 횟수

alter table public.tt_fee_plans enable row level security;
drop policy if exists tt_fee_plans_own on public.tt_fee_plans;
create policy tt_fee_plans_own on public.tt_fee_plans for all to authenticated
  using (owner = (select auth.uid()) and public.tt_allowed())
  with check (owner = (select auth.uid()) and public.tt_allowed());
revoke all on table public.tt_fee_plans from anon;
