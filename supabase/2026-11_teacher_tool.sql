-- ashrain.out — 시록고 강사도구 (2026-11) · PC 「애쉬레인 강사도구」의 웹판
-- 프린트(코드) 등록 → 학생별 채점(1차·2차·3차) → 스캔본·수업 기록·활동 로그 → 오답 출제·내보내기.
-- 표는 전부 「본인 것만」: owner = auth.uid() 이고, 강사(활성 instructor 멤버십) 또는 관리자만.
-- 파일은 비공개 저장 공간 teacher-tool/<uid>/tt/<코드>/… (PC 강사도구의 <uid>/blobs·state.json 과 같은 버킷, 폴더가 다름).
-- 앱은 AI 를 부르지 않는다. SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

-- ── 0. 누가 쓰나 ─────────────────────────────────────────────────────────
create or replace function public.tt_allowed() returns boolean
language sql stable security definer set search_path = public as $$
  select public.is_admin() or exists (
    select 1 from public.memberships m where m.user_id = auth.uid() and m.role = 'instructor' and m.status = 'active')
$$;

-- ── 1. 학생 ──────────────────────────────────────────────────────────────
create table if not exists public.tt_students (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name        text not null,
  grade       text not null default '',
  memo        text not null default '',
  active      boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (owner, name)
);
comment on table public.tt_students is '강사도구 학생 — 강사가 직접 적는 명단(앱 계정과 무관). 본인 것만.';

-- ── 2. 프린트 ────────────────────────────────────────────────────────────
create table if not exists public.tt_prints (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  code        text not null check (code ~ '^[2-9A-HJKMNP-Z]{6}$'),
  title       text not null default '',
  sub         text not null default '',
  kind        text not null default 'registered' check (kind in ('mathflat', 'registered', 'wrong')),
  template    text not null default '',
  label       text not null default '서답형',
  level       text not null default '',
  n_items     integer not null default 0,
  n_choice    integer not null default 0,
  pages       integer not null default 0,
  sources     jsonb not null default '[]'::jsonb,
  files       jsonb not null default '{}'::jsonb,     -- {sheet, answer, src:[], extras:[{name, role, path}]} (저장 공간 경로)
  name_boxes  jsonb not null default '[]'::jsonb,     -- 출력 때 이름 찍을 자리 [{page, rect, size, align}]
  options     jsonb not null default '{}'::jsonb,
  shelf       text not null default 'active' check (shelf in ('library', 'active', 'deleted')),  -- 보관함 · 프린트함 · 지운 프린트
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (owner, code)
);
comment on table public.tt_prints is '강사도구 프린트 — 코드 6글자. shelf: library(보관함, 아직 안 꺼냄)·active(프린트함)·deleted(지운 프린트). 저장본은 이름 없는 판.';
create index if not exists tt_prints_list on public.tt_prints (owner, shelf, created_at desc);

create table if not exists public.tt_print_items (
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  seq         integer not null,
  label       text not null default '',
  src         text not null default '',
  src_no      text not null default '',
  choice      boolean not null default false,
  hash        text,                                   -- 문항 그림 지문(같은 문항 = 반복 오답)
  answer      text not null default '',
  points      numeric,
  topic       text not null default '',
  tag         text not null default '',               -- 매쓰플랫 유형
  rate        text not null default '',               -- 매쓰플랫 정답률
  png         text,                                   -- 문항 그림 (코드 폴더 안 상대 경로)
  answer_png  text,
  sol_png     text,
  scale       real,                                   -- 그림 1px의 pt (오답 프린트 짤 때)
  origin      text,                                   -- 오답 프린트 문항의 원래 「코드:번호:표시」
  page        integer,
  bbox        jsonb,
  primary key (print_id, seq)
);
create index if not exists tt_print_items_hash on public.tt_print_items (owner, hash);

create table if not exists public.tt_targets (
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  issued_at   timestamptz not null default now(),
  primary key (print_id, student_id)
);

-- ── 3. 채점 ──────────────────────────────────────────────────────────────
create table if not exists public.tt_gradings (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  status      text not null default 'open' check (status in ('open', 'done', 'paused_unsolved', 'paused_ungraded')),
  mode        text not null default 'ox',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (print_id, student_id)
);
create index if not exists tt_gradings_student on public.tt_gradings (student_id, created_at);

-- 회차(session) = 한 번 앉아 매긴 단위. 차(round) 1 = 처음 풀기(이어 푼 회차 포함), 2·3 = 틀리거나 안 푼 문항만 다시 풀기(targets).
create table if not exists public.tt_sessions (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  grading_id  bigint not null references public.tt_gradings(id) on delete cascade,
  no          integer not null,
  round       integer not null default 1,
  kind        text not null default 'solve' check (kind in ('solve', 'retry')),
  targets     integer[],
  started_at  timestamptz not null default now(),
  ended_at    timestamptz,
  end_reason  text,
  unique (grading_id, no)
);

create table if not exists public.tt_marks (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  grading_id  bigint not null references public.tt_gradings(id) on delete cascade,
  session_no  integer not null,
  seq         integer not null,
  result      text not null check (result in ('O', 'X', 'U')),
  answer      text not null default '',
  at          timestamptz not null default now()
);
create index if not exists tt_marks_g on public.tt_marks (grading_id, seq, id);

create table if not exists public.tt_scans (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  grading_id  bigint not null references public.tt_gradings(id) on delete cascade,
  path        text not null,
  name        text not null default '',
  size        bigint not null default 0,
  mime        text not null default '',
  pages       integer,
  created_at  timestamptz not null default now(),
  deleted     boolean not null default false
);
create index if not exists tt_scans_g on public.tt_scans (grading_id);

-- ── 4. 수업 기록 · 활동 로그 · 전사본 ────────────────────────────────────
create table if not exists public.tt_class_records (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  day         date not null,
  student_id  bigint not null references public.tt_students(id) on delete cascade,
  kind        text not null check (kind in ('used', 'graded', 'reviewed', 'homework')),
  print_id    bigint not null references public.tt_prints(id) on delete cascade,
  created_at  timestamptz not null default now(),
  unique (day, student_id, kind, print_id)
);

create table if not exists public.tt_events (
  id          bigint generated always as identity primary key,
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  at          timestamptz not null default now(),
  kind        text not null,
  student_id  bigint,                                 -- 지운 뒤에도 기록이 남도록 외래 키 없음
  print_id    bigint,
  detail      jsonb not null default '{}'::jsonb
);
create index if not exists tt_events_at on public.tt_events (owner, at desc);

create table if not exists public.tt_transcripts (
  owner       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  item_key    text not null,
  print_id    bigint,
  seq         integer,
  level       text not null default '',
  question    text,
  solution    text,
  corpus_id   text,
  source      text not null default '',
  batch       text not null default '',
  updated_at  timestamptz not null default now(),
  primary key (owner, item_key)
);

-- ── 5. RLS — 본인 것만, 강사·관리자만 ────────────────────────────────────
do $$
declare t text;
begin
  foreach t in array array['tt_students', 'tt_prints', 'tt_print_items', 'tt_targets', 'tt_gradings', 'tt_sessions', 'tt_marks',
                           'tt_scans', 'tt_class_records', 'tt_events', 'tt_transcripts'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists %I on public.%I', t || '_own', t);
    execute format('create policy %I on public.%I for all to authenticated using (owner = (select auth.uid()) and public.tt_allowed()) '
                   'with check (owner = (select auth.uid()) and public.tt_allowed())', t || '_own', t);
  end loop;
end $$;

-- ── 6. 저장 공간 teacher-tool — 관리자만 → 강사도 자기 폴더만 ─────────────
drop policy if exists teacher_tool_select on storage.objects;
create policy teacher_tool_select on storage.objects for select to authenticated
  using (bucket_id = 'teacher-tool' and public.tt_allowed() and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists teacher_tool_insert on storage.objects;
create policy teacher_tool_insert on storage.objects for insert to authenticated
  with check (bucket_id = 'teacher-tool' and public.tt_allowed() and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists teacher_tool_update on storage.objects;
create policy teacher_tool_update on storage.objects for update to authenticated
  using (bucket_id = 'teacher-tool' and public.tt_allowed() and (storage.foldername(name))[1] = (select auth.uid())::text)
  with check (bucket_id = 'teacher-tool' and public.tt_allowed() and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists teacher_tool_delete on storage.objects;
create policy teacher_tool_delete on storage.objects for delete to authenticated
  using (bucket_id = 'teacher-tool' and public.tt_allowed() and (storage.foldername(name))[1] = (select auth.uid())::text);

-- ── 7. 채점 함수 (부른 사람 권한 = RLS 그대로) ────────────────────────────
create or replace function public.tt_log(p_kind text, p_student bigint, p_print bigint, p_detail jsonb default '{}'::jsonb)
returns void language sql security invoker set search_path = public as $$
  insert into public.tt_events(kind, student_id, print_id, detail) values (p_kind, p_student, p_print, coalesce(p_detail, '{}'::jsonb));
$$;

-- 문항마다 지금 결과(마지막 기록)
create or replace function public.tt_current(p_grading bigint)
returns table (seq integer, result text, answer text, session_no integer)
language sql stable security invoker set search_path = public as $$
  select distinct on (m.seq) m.seq, m.result, m.answer, m.session_no
  from public.tt_marks m where m.grading_id = p_grading order by m.seq, m.id desc;
$$;

-- 채점 열기. p_purpose = 'retry' 이면 지금 틀리거나 안 푼 문항으로 다음 차를 시작.
create or replace function public.tt_open_grading(p_print bigint, p_student bigint, p_purpose text default null)
returns bigint language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; s public.tt_sessions; v_targets integer[]; v_round integer;
begin
  select * into g from public.tt_gradings where print_id = p_print and student_id = p_student;
  if not found then
    insert into public.tt_gradings(print_id, student_id) values (p_print, p_student) returning * into g;
    insert into public.tt_targets(print_id, student_id) values (p_print, p_student) on conflict do nothing;
    insert into public.tt_sessions(grading_id, no, round, kind) values (g.id, 1, 1, 'solve');
    perform public.tt_log('grading_start', p_student, p_print, jsonb_build_object('grading', g.id));
    return g.id;
  end if;
  select * into s from public.tt_sessions where grading_id = g.id order by no desc limit 1;
  if p_purpose = 'retry' then
    select array_agg(c.seq order by c.seq) into v_targets
      from public.tt_current(g.id) c where c.result in ('X', 'U')
       and c.seq in (select i.seq from public.tt_print_items i where i.print_id = p_print);
    if v_targets is null then
      raise exception '다시 매길 문항(틀리거나 안 푼 문항)이 없어요' using errcode = 'P0001';
    end if;
    if s.id is not null and s.ended_at is null then
      update public.tt_sessions set ended_at = now(), end_reason = coalesce(end_reason, 'done') where id = s.id;
    end if;
    select coalesce(max(round), 1) + 1 into v_round from public.tt_sessions where grading_id = g.id;
    insert into public.tt_sessions(grading_id, no, round, kind, targets)
      values (g.id, coalesce(s.no, 0) + 1, v_round, 'retry', v_targets);
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('retry_start', p_student, p_print, jsonb_build_object('grading', g.id, 'round', v_round, 'targets', cardinality(v_targets)));
  elsif s.id is not null and s.ended_at is null then
    null;                                               -- 열려 있던 회차를 그대로 이어 감
  elsif g.status = 'done' and s.id is not null then     -- 다 끝난 채점을 다시 열면 = 고치기 (마지막 회차를 다시 엶)
    update public.tt_sessions set ended_at = null, end_reason = null where id = s.id;
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('grading_reopen', p_student, p_print, jsonb_build_object('grading', g.id, 'round', s.round));
  else                                                  -- 덜 풀었거나 덜 매겨 멈춘 채점 → 같은 차의 다음 회차
    insert into public.tt_sessions(grading_id, no, round, kind, targets)
      values (g.id, coalesce(s.no, 0) + 1, coalesce(s.round, 1), coalesce(s.kind, 'solve'), s.targets);
    update public.tt_gradings set status = 'open', updated_at = now() where id = g.id;
    perform public.tt_log('grading_resume', p_student, p_print, jsonb_build_object('grading', g.id, 'was', g.status));
  end if;
  return g.id;
end $$;

-- 매기기. p_result '' = 이번 회차에 그 문항을 매긴 기록 지우기(앞 기록이 다시 보임)
create or replace function public.tt_mark(p_grading bigint, p_seq integer, p_result text, p_answer text default '')
returns void language plpgsql security invoker set search_path = public as $$
declare s public.tt_sessions;
begin
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  if s.kind = 'retry' and not (p_seq = any(coalesce(s.targets, array[p_seq]))) then
    raise exception '이번 차에 다시 풀 문항이 아니에요' using errcode = 'P0001';
  end if;
  if coalesce(p_result, '') = '' then
    delete from public.tt_marks where grading_id = p_grading and session_no = s.no and seq = p_seq;
  else
    insert into public.tt_marks(grading_id, session_no, seq, result, answer) values (p_grading, s.no, p_seq, p_result, coalesce(p_answer, ''));
  end if;
  update public.tt_gradings set status = 'open', updated_at = now() where id = p_grading;
end $$;

-- 닫기. p_reason: done | unsolved(아이가 덜 풂) | ungraded(채점을 덜 함). p_untouched: 열어 보기만 했으면 빈 회차를 없애고 전 상태로.
create or replace function public.tt_close_grading(p_grading bigint, p_reason text, p_untouched boolean default false)
returns text language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; s public.tt_sessions; prev public.tt_sessions; v_blank integer[]; v_status text; n_here integer;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '채점 기록이 없어요' using errcode = 'P0001'; end if;
  select * into s from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
  if p_untouched then
    select count(*) into n_here from public.tt_marks where grading_id = p_grading and session_no = s.no;
    select * into prev from public.tt_sessions where grading_id = p_grading and no < s.no order by no desc limit 1;
    if n_here = 0 and prev.id is not null then
      delete from public.tt_sessions where id = s.id;
      update public.tt_sessions set ended_at = coalesce(ended_at, now()) where id = prev.id;
      v_status := case prev.end_reason when 'done' then 'done' when 'unsolved' then 'paused_unsolved' else 'paused_ungraded' end;
      update public.tt_gradings set status = v_status where id = p_grading;
      return v_status;
    end if;
  end if;
  if s.kind = 'retry' then          -- 다시 풀기: 이번 차에 아직 안 매긴 다시 풀 문항만 '남음'(U를 쓰지 않음 — 앞 차 결과가 최종)
    select array_agg(t) into v_blank from unnest(coalesce(s.targets, '{}'::integer[])) t
     where not exists (select 1 from public.tt_marks m join public.tt_sessions x on x.grading_id = m.grading_id and x.no = m.session_no
                       where m.grading_id = p_grading and m.seq = t and x.round = s.round);
  else
    select array_agg(i.seq) into v_blank from public.tt_print_items i
     where i.print_id = g.print_id and not exists (select 1 from public.tt_marks m where m.grading_id = p_grading and m.seq = i.seq);
    if p_reason = 'unsolved' and v_blank is not null then
      insert into public.tt_marks(grading_id, session_no, seq, result) select p_grading, s.no, t, 'U' from unnest(v_blank) t;
    end if;
  end if;
  v_status := case p_reason when 'done' then 'done' when 'unsolved' then 'paused_unsolved' else 'paused_ungraded' end;
  if p_reason = 'done' and v_blank is not null then v_status := 'paused_ungraded'; end if;
  update public.tt_sessions set ended_at = now(), end_reason = p_reason where id = s.id;
  update public.tt_gradings set status = v_status, updated_at = now() where id = p_grading;
  perform public.tt_log('grading_close', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'reason', p_reason, 'session', s.no, 'round', s.round, 'blank', coalesce(cardinality(v_blank), 0)));
  return v_status;
end $$;

-- 지우기. p_scope: all(그 학생의 그 프린트 채점 전부) | last_round(마지막 차만). 돌려주는 것: 지울 스캔본 경로들
create or replace function public.tt_delete_grading(p_grading bigint, p_scope text default 'all')
returns jsonb language plpgsql security invoker set search_path = public as $$
declare g public.tt_gradings; mx integer; last public.tt_sessions; v_paths text[]; n integer;
begin
  select * into g from public.tt_gradings where id = p_grading;
  if not found then raise exception '그런 채점 기록이 없어요' using errcode = 'P0001'; end if;
  if p_scope = 'last_round' then
    select coalesce(max(round), 1) into mx from public.tt_sessions where grading_id = p_grading;
    if mx <= 1 then raise exception '1차만 있는 채점이에요. 지우려면 채점 기록 전체를 지우세요' using errcode = 'P0001'; end if;
    delete from public.tt_marks m using public.tt_sessions x
     where m.grading_id = p_grading and x.grading_id = p_grading and x.no = m.session_no and x.round = mx;
    get diagnostics n = row_count;
    delete from public.tt_sessions where grading_id = p_grading and round = mx;
    update public.tt_sessions set ended_at = coalesce(ended_at, now()) where grading_id = p_grading;
    select * into last from public.tt_sessions where grading_id = p_grading order by no desc limit 1;
    update public.tt_gradings set updated_at = now(),
      status = case coalesce(last.end_reason, 'done') when 'unsolved' then 'paused_unsolved' when 'ungraded' then 'paused_ungraded' else 'done' end
     where id = p_grading;
    perform public.tt_log('round_delete', g.student_id, g.print_id, jsonb_build_object('grading', p_grading, 'round', mx, 'marks', n));
    return jsonb_build_object('ok', true, 'deleted_round', mx, 'paths', '[]'::jsonb);
  end if;
  select array_agg(path) into v_paths from public.tt_scans where grading_id = p_grading;
  select count(*) into n from public.tt_marks where grading_id = p_grading;
  perform public.tt_log('grading_delete', g.student_id, g.print_id,
    jsonb_build_object('grading', p_grading, 'marks', n, 'scans', coalesce(cardinality(v_paths), 0),
                       'rounds', (select coalesce(max(round), 1) from public.tt_sessions where grading_id = p_grading)));
  delete from public.tt_gradings where id = p_grading;   -- 회차·기록·스캔본 행은 on delete cascade
  return jsonb_build_object('ok', true, 'paths', to_jsonb(coalesce(v_paths, '{}'::text[])));
end $$;

-- 프린트 완전히 지우기(채점·수업 기록·출제 대상·문항 모두, 코드 비워짐). 돌려주는 것: 지울 저장 공간 경로 머리·스캔본 경로들
create or replace function public.tt_purge_print(p_print bigint)
returns jsonb language plpgsql security invoker set search_path = public as $$
declare p public.tt_prints; v_paths text[]; n_g integer;
begin
  select * into p from public.tt_prints where id = p_print;
  if not found then raise exception '그런 프린트가 없어요' using errcode = 'P0001'; end if;
  select array_agg(s.path) into v_paths from public.tt_scans s join public.tt_gradings g on g.id = s.grading_id where g.print_id = p_print;
  select count(*) into n_g from public.tt_gradings where print_id = p_print;
  perform public.tt_log('print_purge', null, null, jsonb_build_object('code', p.code, 'title', p.title, 'gradings', n_g));
  delete from public.tt_prints where id = p_print;      -- 문항·대상·채점·수업 기록은 on delete cascade
  return jsonb_build_object('ok', true, 'code', p.code, 'gradings', n_g, 'paths', to_jsonb(coalesce(v_paths, '{}'::text[])));
end $$;

revoke all on function public.tt_open_grading(bigint, bigint, text) from anon;
revoke all on function public.tt_mark(bigint, integer, text, text) from anon;
revoke all on function public.tt_close_grading(bigint, text, boolean) from anon;
revoke all on function public.tt_delete_grading(bigint, text) from anon;
revoke all on function public.tt_purge_print(bigint) from anon;
