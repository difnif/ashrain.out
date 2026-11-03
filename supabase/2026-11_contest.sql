-- ashrain.out — 경시 대비 (2026-11) 마이그레이션 · v2 흐름
-- 1 분석 대상 등록(이름·학년·전화 뒷자리) → 2 프린트 선택(연도·상/하반기) → 답안 입력 → 채점
-- → 3 채점한 프린트 체크 → 오답 프린트 생성 → 4 오답 프린트도 2와 같이 채점
-- → 5 분석할 프린트 골라 분석 파일 추출(md) → 6 채팅방 분석 → 다듬어 브리핑 입력.
-- 앱은 AI 를 부르지 않는다. 표는 전부 관리자 전용(읽기·쓰기 모두 is_admin()).
-- SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

-- ── 1. 프린트 (기출 원본 = 'original', 오답 프린트 = 'wrong') ────────────
create table if not exists public.contest_sets (
  id           uuid primary key default gen_random_uuid(),
  code         text not null unique,                 -- 원본: KUT-2025-H1-M2 · 오답: W-S0003-20261103-1
  kind         text not null default 'original' check (kind in ('original','wrong')),
  title        text not null,
  contest      text,                                 -- 대회명 (KUT)
  year         integer,
  half         text check (half in ('상반기','하반기')),
  grade_label  text,                                 -- 대상 학년 (중2 등)
  test_date    date,
  taker_id     uuid,                                 -- 오답 프린트의 주인 (원본은 null)
  parent_ids   uuid[] not null default '{}',         -- 오답 프린트를 만든 출처 프린트들
  n_items      integer not null default 0,
  max_score    numeric not null default 0,
  spec         jsonb,                                -- 가져온 JSON 전체 (원본 보관)
  files        jsonb not null default '[]'::jsonb,   -- 프린트 파일 [{name, path, kind:'problem'|'answer'|'solution'|'etc', size}]
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
comment on table public.contest_sets is '경시 대비 프린트 — 원본(채팅방 JSON)과 학생별 오답 프린트. 관리자만 읽는다.';
create index if not exists contest_sets_find on public.contest_sets (kind, year desc, half);

-- ── 2. 문항 ──────────────────────────────────────────────────────────────
create table if not exists public.contest_items (
  set_id       uuid not null references public.contest_sets(id) on delete cascade,
  no           integer not null,
  points       numeric not null default 1,
  answer_type  text not null default 'int' check (answer_type in ('choice','int','text')),
  n_choices    integer,
  choices      text[],                               -- 객관식 보기 문구 (오답 프린트 인쇄용)
  accept       text[] not null,                      -- 정답. 여럿이면 모두 정답
  text         text,                                 -- 발문 (관리자 전용 · 지표 계산 · 오답 프린트 인쇄)
  figure       text,                                 -- 그림 (data URI 또는 URL) — 오답 프린트 인쇄용
  crop         text,                                 -- 원본 문항 이미지 (contest-files 경로) — 있으면 오답 프린트에 그대로 인쇄
  features     jsonb not null default '{}'::jsonb,   -- 채팅방 판단 특성
  metrics      jsonb not null default '{}'::jsonb,   -- 앱이 원문에서 센 지표
  solution     jsonb,
  src_set_id   uuid,                                 -- 오답 프린트 문항의 원본 프린트 (원본 문항은 null)
  src_no       integer,                              -- 원본 문항 번호
  primary key (set_id, no)
);

alter table public.contest_items add column if not exists crop text;

-- ── 3. 분석 대상 (학생) ──────────────────────────────────────────────────
create table if not exists public.contest_takers (
  id           uuid primary key default gen_random_uuid(),
  seq          bigint generated always as identity,  -- 익명 코드 S0001 의 번호
  name         text not null,
  grade        text not null default '',
  phone4       text not null default '' check (phone4 ~ '^[0-9]{0,4}$'),   -- 전화번호 뒷자리
  user_id      uuid references auth.users(id) on delete set null,
  memo         text,
  created_at   timestamptz not null default now(),
  unique (name, phone4)
);
comment on table public.contest_takers is '경시 대비 분석 대상 — 내보내기에는 익명 코드(S+seq)와 학년만 나간다.';

-- ── 4. 응답 · 채점 ───────────────────────────────────────────────────────
create table if not exists public.contest_responses (
  set_id       uuid not null references public.contest_sets(id) on delete cascade,
  taker_id     uuid not null references public.contest_takers(id) on delete cascade,
  item_no      integer not null,
  response     text,                                 -- 빈칸 = 무응답
  is_correct   boolean,                              -- 무응답이면 null
  updated_at   timestamptz not null default now(),
  primary key (set_id, taker_id, item_no)
);
create index if not exists contest_responses_taker on public.contest_responses (taker_id);

create table if not exists public.contest_attempts (
  set_id       uuid not null references public.contest_sets(id) on delete cascade,
  taker_id     uuid not null references public.contest_takers(id) on delete cascade,
  taken_on     date,                                 -- 응시일
  score        numeric not null default 0,
  max_score    numeric not null default 0,
  n_right      integer not null default 0,
  n_wrong      integer not null default 0,
  n_blank      integer not null default 0,
  graded_at    timestamptz not null default now(),
  primary key (set_id, taker_id)
);
comment on table public.contest_attempts is '채점 완료 기록 — 오답 프린트 생성·분석 대상 고르기의 기준.';

-- ── 5. 브리핑 (채팅방 분석을 다듬어 넣는 곳) ─────────────────────────────
create table if not exists public.contest_briefings (
  id           uuid primary key default gen_random_uuid(),
  taker_id     uuid not null references public.contest_takers(id) on delete cascade,
  title        text not null,
  set_ids      uuid[] not null default '{}',         -- 분석에 쓴 프린트
  body         text not null default '',             -- 마크다운
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create index if not exists contest_briefings_taker on public.contest_briefings (taker_id, created_at desc);

alter table public.contest_sets drop constraint if exists contest_sets_taker_fk;
alter table public.contest_sets add constraint contest_sets_taker_fk
  foreign key (taker_id) references public.contest_takers(id) on delete cascade;

-- ── 6. RLS — 관리자 전용 ─────────────────────────────────────────────────
do $$
declare t text;
begin
  foreach t in array array['contest_sets','contest_items','contest_takers','contest_responses','contest_attempts','contest_briefings'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('drop policy if exists %I on public.%I', t || '_admin', t);
    execute format('create policy %I on public.%I for all to authenticated using (public.is_admin()) with check (public.is_admin())', t || '_admin', t);
  end loop;
end $$;

-- ── 7. 프린트 파일 저장소 (비공개, 관리자만) ─────────────────────────────
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
