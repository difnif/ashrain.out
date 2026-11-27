-- 강사도구 교재 기록 — 학생 교재마다 푼 데까지(수업 끝 진도) · 채점한 날 · 해설지 준 날
-- 교재는 tt_prints.options.textbook 으로 둔다(role 'student' = 학생마다 붙인 교재, 스캔본은 그 채점 기록에).
-- 이 표는 그 학생 교재(print_id)에 날짜별 기록을 단다. 여러 번 실행해도 안전.
create table if not exists public.tt_book_logs (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  print_id    bigint not null references public.tt_prints(id) on delete cascade,      -- 학생 몫 교재
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  day         date not null,                                                           -- solved: 푼 날 · graded: 채점한 날 · solution: 해설지 준 날
  kind        text not null check (kind in ('solved', 'graded', 'solution')),
  page_to     integer check (page_to is null or page_to between 0 and 9999),           -- solved: 몇 쪽까지 풀었는지
  pages       text not null default '' check (char_length(pages) <= 200),              -- graded: 채점한 쪽(예: 12-20, 25) — 비어도 됨
  round       integer check (round is null or round between 1 and 9),                  -- graded: 몇 차 채점
  note        text not null default '' check (char_length(note) <= 300),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
comment on table public.tt_book_logs is '강사도구 교재 기록 — solved(그날 몇 쪽까지, 수업 끝 진도) · graded(채점한 날 · 몇 차 · 채점한 쪽) · solution(해설지 준 날). 본인 것만.';

create index if not exists tt_book_logs_print on public.tt_book_logs (print_id, day desc);
create index if not exists tt_book_logs_student on public.tt_book_logs (student_id, day desc);
-- 같은 교재 · 같은 날 진도는 하나(다시 적으면 고침), 해설지는 한 번, 채점은 같은 날 · 같은 차에 하나(쪽을 합침)
create unique index if not exists tt_book_logs_solved_day on public.tt_book_logs (print_id, day) where kind = 'solved';
create unique index if not exists tt_book_logs_solution_once on public.tt_book_logs (print_id) where kind = 'solution';
create unique index if not exists tt_book_logs_graded_day on public.tt_book_logs (print_id, day, (coalesce(round, 0))) where kind = 'graded';

alter table public.tt_book_logs enable row level security;
drop policy if exists tt_book_logs_own on public.tt_book_logs;
create policy tt_book_logs_own on public.tt_book_logs for all to authenticated
  using (owner = (select auth.uid()) and public.tt_allowed())
  with check (owner = (select auth.uid()) and public.tt_allowed());
revoke all on table public.tt_book_logs from anon;
