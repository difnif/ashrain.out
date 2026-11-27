-- 강사도구 재원 · 원비 — 학생마다 달마다 다님 · 휴원 · 그만둠과 그달 원비. 매출 = 그달 「다님」 학생 원비의 합.
-- 선생님이 매월 직접 적는다(안 적은 달은 학생 화면에 노랑 · 빨강). 여러 번 실행해도 안전.
create table if not exists public.tt_student_months (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  month       date not null check (extract(day from month) = 1),                  -- 그달 1일
  status      text not null check (status in ('attend', 'pause', 'quit')),       -- 다님 · 휴원 · 그만둠
  fee         integer check (fee is null or fee between 0 and 100000000),        -- 그달 원비(원), 모르면 비움
  note        text not null default '' check (char_length(note) <= 300),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (student_id, month)
);
comment on table public.tt_student_months is '강사도구 재원 · 원비 — 학생 · 달(1일)마다 status(attend 다님 · pause 휴원 · quit 그만둠)와 fee(원비, 원). 매출 = 그달 다님 학생 fee 합. 본인 것만.';
create index if not exists tt_student_months_month on public.tt_student_months (month desc);

alter table public.tt_student_months enable row level security;
drop policy if exists tt_student_months_own on public.tt_student_months;
create policy tt_student_months_own on public.tt_student_months for all to authenticated
  using (owner = (select auth.uid()) and public.tt_allowed())
  with check (owner = (select auth.uid()) and public.tt_allowed());
revoke all on table public.tt_student_months from anon;
