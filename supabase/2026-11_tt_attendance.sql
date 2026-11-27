-- 강사도구 결석부 — 학생 · 날마다 결석 확정 · 결석 예정 · 지각 · 지각 예정 · 조퇴 예정 · 연락 없음 + 사유, 당일 확인(왔음 · 안 옴 · 늦음).
-- 나중에 학부모 모드(종성)에서 학부모가 결석 · 사유를 넣으면 강사에게 저절로 전달된다 — 누가 넣었는지 source 로 구분. 여러 번 실행해도 안전.
create table if not exists public.tt_attendance (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  day         date not null,
  kind        text not null check (kind in ('absent', 'absent_maybe', 'late', 'late_maybe', 'early_maybe', 'no_contact')),
  reason      text not null default '' check (char_length(reason) <= 300),
  checked     text check (checked is null or checked in ('came', 'absent', 'late')),      -- 당일 확인: 왔음 · 안 옴 · 늦음
  checked_at  timestamptz,
  source      text not null default 'teacher' check (source in ('teacher', 'parent')),     -- 강사가 넣음 · 학부모가 넣음(종성)
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (student_id, day)
);
comment on table public.tt_attendance is '강사도구 결석부 — 학생 · 날마다 kind(absent 결석 확정 · absent_maybe 결석 예정 · late 지각 · late_maybe 지각 예정 · early_maybe 조퇴 예정 · no_contact 연락 없음) · reason · checked(당일 확인 came · absent · late) · source(teacher · parent). 본인 것만.';
create index if not exists tt_attendance_day on public.tt_attendance (day desc);

alter table public.tt_attendance enable row level security;
drop policy if exists tt_attendance_own on public.tt_attendance;
create policy tt_attendance_own on public.tt_attendance for all to authenticated
  using (owner = (select auth.uid()) and public.tt_allowed())
  with check (owner = (select auth.uid()) and public.tt_allowed());
revoke all on table public.tt_attendance from anon;
