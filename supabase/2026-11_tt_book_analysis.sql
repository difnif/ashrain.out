-- 강사도구 교재 분석(2단계) — 교재 문항 · 교재 채점 결과 · 물어볼 것 · 스캔본 「분석함」
-- 스캔본을 채팅에서 Claude가 분석하고(분석 맡기기 묶음), 결과 파일을 강사도구에 넣는다. 여러 번 실행해도 안전.

-- 1) 교재 문항 — 교재 자체(tt_prints, options.textbook.role = 'master')에 매단다. 학생마다 같은 문항을 함께 쓴다.
create table if not exists public.tt_book_items (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  page        integer not null check (page between 0 and 9999),                          -- 교재 쪽
  label       text not null check (char_length(label) between 1 and 40),                 -- 교재에 적힌 번호(예: 12 · 유제 3 · 12(2))
  answer      text not null default '' check (char_length(answer) <= 300),               -- 정답(알면)
  answer_src  text not null default '' check (answer_src in ('', 'claude', 'teacher', 'book')),   -- 누가 정한 정답인지
  topic       text not null default '' check (char_length(topic) <= 100),
  crop        jsonb,                                                                     -- 문항 그림 자리 {scan_id, page_index, box:[x, y, w, h] (0~1)}
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (print_id, page, label)
);
comment on table public.tt_book_items is '강사도구 교재 문항 — 교재 자체(print_id) · 쪽 · 번호마다 하나, 정답 · 누가 정했나 · 단원 · 그림 자리. 본인 것만.';

-- 2) 교재 채점 결과 — 학생 교재(options.textbook.role = 'student') · 문항 · 차마다 하나
create table if not exists public.tt_book_marks (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  item_id     bigint not null references public.tt_book_items(id) on delete cascade,
  round       integer not null check (round between 1 and 9),
  result      text not null check (result in ('O', 'X', 'U')),                           -- 맞음 · 틀림 · 안 풂(넘어감)
  unsolved    boolean not null default false,                                            -- 안 풀었지만 오답으로 봄(별표 · 빗금)
  mark        text not null default '' check (char_length(mark) <= 20),                  -- 종이에서 읽은 선생님 표시(o · slash · tri · x · ribbon · check · star · none)
  answer      text not null default '' check (char_length(answer) <= 300),               -- 학생이 쓴 답
  graded_by   text not null default 'teacher' check (graded_by in ('teacher', 'claude')),
  day         date not null,                                                             -- 채점한 날
  report_day  date,                                                                      -- 기록에 넣을 날(물어볼 것에서 정함, 비면 day)
  scan_id     bigint references public.tt_scans(id) on delete set null,
  note        text not null default '' check (char_length(note) <= 300),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (print_id, item_id, round)
);
comment on table public.tt_book_marks is '강사도구 교재 채점 결과 — 학생 교재 · 문항 · 차마다 result(O · X · U) · unsolved(안 풀었지만 오답) · 선생님 표시 · 학생 답 · 누가 채점 · 채점한 날 · 기록에 넣을 날. 본인 것만.';
create index if not exists tt_book_marks_item on public.tt_book_marks (item_id);
create index if not exists tt_book_marks_student on public.tt_book_marks (student_id, day desc);

-- 3) 물어볼 것 — 확인할 것(선생님 ○인데 틀림 · 빨간 표시 + ○ · 안 푼 문제 표시 · 애매한 표시) · 늦은 채점 질문, 답과 이유(교육관)
create table if not exists public.tt_questions (
  id           bigint generated always as identity primary key,
  owner        uuid not null default auth.uid() references auth.users(id) on delete cascade,
  kind         text not null check (kind in ('o_but_wrong', 'red_note_o', 'unsolved_mark', 'unsure_mark', 'late_grade')),
  student_id   bigint references public.tt_students(id) on delete cascade,
  print_id     bigint references public.tt_prints(id) on delete cascade,
  item_id      bigint references public.tt_book_items(id) on delete cascade,
  mark_id      bigint references public.tt_book_marks(id) on delete set null,
  grading_id   bigint references public.tt_gradings(id) on delete cascade,              -- 프린트 채점(늦은 채점 · 프린트 스캔본 분석)
  seq          integer,                                                                  -- 프린트 문항 번호
  detail       jsonb not null default '{}'::jsonb,                                       -- 무엇을 왜 묻는지(Claude가 본 것 · 학생 답 · 정답 …)
  status       text not null default 'open' check (status in ('open', 'fixed', 'accepted', 'answered', 'dismissed')),
  answer       jsonb,                                                                    -- 고른 답(결과 · 기록에 넣을 날 …)
  reason       text not null default '' check (char_length(reason) <= 1000),            -- 맞다고 인정한 이유 · 늦은 까닭
  reason_later boolean not null default false,                                           -- 「이유는 나중에」
  created_at   timestamptz not null default now(),
  answered_at  timestamptz,
  updated_at   timestamptz not null default now()
);
comment on table public.tt_questions is '강사도구 물어볼 것 — kind(o_but_wrong · red_note_o · unsolved_mark · unsure_mark · late_grade) · 무엇을 묻는지 · status(open · fixed · accepted · answered · dismissed) · 답 · 이유(교육관). 본인 것만.';
create index if not exists tt_questions_open on public.tt_questions (status, created_at desc);

-- 4) 스캔본 「분석함」 — 분석 결과를 넣은 때(비면 아직 분석 안 함)
alter table public.tt_scans add column if not exists analyzed_at timestamptz;

do $$
declare t text;
begin
  foreach t in array array['tt_book_items', 'tt_book_marks', 'tt_questions'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists %I on public.%I', t || '_own', t);
    execute format('create policy %I on public.%I for all to authenticated using (owner = (select auth.uid()) and public.tt_allowed()) '
                   'with check (owner = (select auth.uid()) and public.tt_allowed())', t || '_own', t);
    execute format('revoke all on table public.%I from anon', t);
  end loop;
end $$;
