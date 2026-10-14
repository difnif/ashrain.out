-- ashrain.out — 서술형 평가 (2026-10) 마이그레이션
-- 채팅방 생성기 JSON → 관리자 등록 → 학생앱 알림·QR(/e/<코드>) → 쪽마다 촬영 → 판독·채점 → 결과.
-- 앱은 이 파일 없이도 죽지 않는다(목록이 비고, 열면 "아직 준비되지 않았어요"). SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.
-- 원칙: 표는 전부 서비스 롤(api/_lib/assess.js)만 쓴다. 학생은 표를 직접 읽지 않고 API 로만 본다(해시·판독 원문이 새지 않게). 관리자는 전부 읽는다.
--       평가 JSON(정답·채점 기준 포함)은 관리자만 읽는다 — 학생에게는 API 가 공개용만 준다.
--       사진은 assess_store_images='on' 일 때만 비공개 버킷 assess-pages 에 쌓인다(기본 off).
--       호출 한도·쪽 맡기는 DB 함수(assess_charge · assess_reserve_page)로 원자적으로 — 동시에 여러 번 눌러도 한 번만 센다.

-- ── 1. 평가 (채팅방 JSON 한 개 = 한 행) ─────────────────────────────────
create table if not exists public.assess_sets (
  id           uuid primary key default gen_random_uuid(),
  code         text not null unique check (code ~ '^[A-Z0-9]{4,12}$'),   -- QR 주소 /e/<code>
  title        text not null,
  level        text,                                                     -- elem|mid|high
  grade_label  text,                                                     -- 중2 등 (표시용)
  test_date    date,
  status       text not null default 'live' check (status in ('draft','live','closed')),
  opens_at     timestamptz,
  closes_at    timestamptz,
  reveal       text not null default 'after_close' check (reveal in ('after_submit','after_close','never')),   -- 정답·모범 풀이 공개 시점
  n_items      integer not null,
  n_pages      integer not null,
  spec         jsonb not null,                                           -- 생성기 JSON 전체 (정답·채점 기준 포함)
  created_by   uuid references auth.users(id) on delete set null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
comment on table public.assess_sets is '서술형 평가 — 채팅방 생성기 JSON 한 개. spec 에 정답·채점 기준이 있어 관리자만 읽는다(학생에게는 API 가 공개용만).';
create index if not exists assess_sets_live on public.assess_sets (status, created_at desc);

-- ── 2. 응시자 명부 (로그인 계정 또는 2쪽 이름·학년) ─────────────────────
create table if not exists public.assess_people (
  id          uuid primary key default gen_random_uuid(),
  person_key  text not null unique,                                      -- 'u:<계정 uuid>' | 'n:<이름>|<학년 e4·m2…>'
  user_id     uuid references auth.users(id) on delete set null,          -- 로그인 응시였거나 나중에 로그인해 담았으면
  name        text,
  grade       text,
  nickname    text,
  n_sessions  integer not null default 0,                                -- 제출한 응시 수
  first_seen  timestamptz not null default now(),
  last_seen   timestamptz not null default now()
);
comment on table public.assess_people is '서술형 평가 응시자 명부 — 비로그인은 2쪽 이름·학년(학생이 확인한 값)으로 묶는다. 같은 이름·학년이 둘이면 관리자가 나눈다.';
create index if not exists assess_people_user on public.assess_people (user_id);

-- ── 3. 응시 기록 ─────────────────────────────────────────────────────────
create table if not exists public.assess_sessions (
  id           uuid primary key default gen_random_uuid(),
  set_id       uuid not null references public.assess_sets(id) on delete cascade,
  person_id    uuid references public.assess_people(id) on delete set null,
  user_id      uuid references auth.users(id) on delete set null,
  device_hash  text,                                                     -- 기기 토큰 해시 (원문 없음)
  secret_hash  text,                                                     -- 응시 비밀값 해시 — 비로그인 이어 하기·결과 보기
  ip_hash      text,                                                     -- 호출 한도용 해시
  ua           text,
  status       text not null default 'open' check (status in ('open','submitted')),
  info         jsonb,                                                    -- 확인된 2쪽 정보 {name, grade, nickname, by:'ocr'|'user'|'profile'}
  ocr_info     jsonb,                                                    -- 2쪽 판독 원본 {grade, name, nickname, phrase[], confidence}
  total        numeric,
  max          numeric,
  started_at   timestamptz not null default now(),
  submitted_at timestamptz
);
comment on table public.assess_sessions is '서술형 평가 응시 — 로그인/비로그인 공통. 비로그인은 기기 토큰·비밀값(해시)으로 잇는다.';
create index if not exists assess_sessions_set on public.assess_sessions (set_id, started_at desc);
create index if not exists assess_sessions_user on public.assess_sessions (user_id, started_at desc);
create index if not exists assess_sessions_device on public.assess_sessions (device_hash, set_id);
create index if not exists assess_sessions_person on public.assess_sessions (person_id);

-- ── 4. 쪽 기록 (한 쪽 = 한 행, 다시 찍으면 덮어씀) ──────────────────────
-- status: reading(판독 중) → read(판독됨) → grading(채점 중) → graded / ok(안내 쪽) / error(판독 실패 — 같은 사진으로 다시 보내거나 다시 찍기)
-- shot: 사진 한 장마다 브라우저가 만든 id. 다시 찍으면 바뀌고, 늦게 끝난 옛 사진의 결과는 shot 이 달라 저장되지 않는다.
create table if not exists public.assess_pages (
  session_id   uuid not null references public.assess_sessions(id) on delete cascade,
  page_no      integer not null,
  kind         text not null check (kind in ('guide','info','item')),
  item_no      integer,
  attempts     integer not null default 1,                               -- 이 쪽에 보낸 서로 다른 사진 수
  status       text not null default 'read',
  shot         text,
  grade_tries  integer not null default 0,                               -- 지금 사진으로 채점을 맡은 횟수
  quality      jsonb,                                                    -- 브라우저 품질값 {sharp, paper, contrast, margin}
  read         jsonb,                                                    -- 판독(학생이 쓴 그대로·그은 줄·⍰)
  grade        jsonb,                                                    -- 채점 {marks[], total, max, final_answer, feedback, tags}
  flagged      boolean not null default false,                           -- 학생이 '잘못 읽었어요'
  flag_note    text,
  image_path   text,                                                     -- assess-pages 버킷 경로 (저장 켰을 때만)
  model_read   text,
  model_grade  text,
  updated_at   timestamptz not null default now(),
  primary key (session_id, page_no)
);
alter table public.assess_pages add column if not exists shot text;
alter table public.assess_pages add column if not exists grade_tries integer not null default 0;
alter table public.assess_pages drop constraint if exists assess_pages_status_check;
alter table public.assess_pages add constraint assess_pages_status_check check (status in ('ok','reading','read','grading','graded','error'));
comment on table public.assess_pages is '서술형 평가 쪽별 판독·채점 — 손글씨 데이터(판독 원문)와 채점 결과. 사진은 저장을 켰을 때만 경로가 남는다.';
create index if not exists assess_pages_flagged on public.assess_pages (flagged) where flagged;

-- ── 5. 호출 한도 (키·시각만) ─────────────────────────────────────────────
create table if not exists public.assess_calls (
  key         text not null,                                             -- 'u:<uuid>' | 'ip:<해시>' | 'set:<uuid>' | 'anon'
  created_at  timestamptz not null default now()
);
create index if not exists assess_calls_key on public.assess_calls (key, created_at desc);
create index if not exists assess_calls_at on public.assess_calls (created_at);
comment on table public.assess_calls is '서술형 평가 호출 한도 — 하루(KST) 단위로 센다. 3일 지난 행은 assess_charge 가 가끔 지운다.';

-- ── 5-1. 호출 한도 세기 (원자적) ─────────────────────────────────────────
-- 키마다 p_since 이후 센 수가 한도 미만이면 키마다 한 행씩 넣고 null, 하나라도 찼으면 넣지 않고 그 키를 돌려준다.
-- 키 순서대로 잠가서(트랜잭션 잠금) 동시에 들어와도 한도를 넘지 않는다.
create or replace function public.assess_charge(p_keys text[], p_caps integer[], p_since timestamptz)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  k text;
  i integer;
  n integer;
begin
  if p_keys is null or array_length(p_keys, 1) is null or array_length(p_keys, 1) <> array_length(p_caps, 1) then
    raise exception 'assess_charge: keys/caps';
  end if;
  for k in select unnest(p_keys) as x order by 1 loop
    perform pg_advisory_xact_lock(hashtext('assess_calls:' || k));
  end loop;
  for i in 1 .. array_length(p_keys, 1) loop
    select count(*) into n from public.assess_calls where key = p_keys[i] and created_at >= p_since;
    if n >= p_caps[i] then
      return p_keys[i];
    end if;
  end loop;
  insert into public.assess_calls (key) select unnest(p_keys);
  if random() < 0.02 then
    delete from public.assess_calls where created_at < now() - interval '3 days';
  end if;
  return null;
end
$$;

-- ── 5-2. 쪽 맡기 (원자적) ────────────────────────────────────────────────
-- 사진(shot) 한 장을 이 요청이 맡아도 되는지 정한다. 결과 o_state:
--   fresh  새 사진 — 시도 횟수 +1, 판독·채점 비우고 reading 으로
--   retry  같은 사진인데 앞 요청이 실패했거나(error) 멈춤(reading 70초 넘음) — 횟수는 그대로
--   busy   같은 사진을 다른 요청이 지금 읽는 중
--   done   같은 사진이 이미 판독됨(read·grading·graded) — AI 를 다시 부르지 않는다
--   over   새 사진인데 이 쪽 시도 횟수(p_max)를 다 씀
create or replace function public.assess_reserve_page(p_session uuid, p_page integer, p_kind text, p_item integer, p_shot text, p_max integer)
returns table (o_state text, o_attempts integer)
language plpgsql
security definer
set search_path = public
as $$
declare
  r public.assess_pages%rowtype;
begin
  insert into public.assess_pages as ap (session_id, page_no, kind, item_no, attempts, status, shot, updated_at)
    values (p_session, p_page, p_kind, p_item, 0, 'reading', null, now())
    on conflict (session_id, page_no) do nothing;
  select * into r from public.assess_pages ap where ap.session_id = p_session and ap.page_no = p_page for update;
  if p_shot is not null and r.shot is not distinct from p_shot then
    if r.status in ('read', 'grading', 'graded', 'ok') then
      return query select 'done'::text, r.attempts;
      return;
    end if;
    if r.status = 'reading' and r.updated_at > now() - interval '70 seconds' then
      return query select 'busy'::text, r.attempts;
      return;
    end if;
    update public.assess_pages ap set status = 'reading', updated_at = now()
      where ap.session_id = p_session and ap.page_no = p_page;
    return query select 'retry'::text, r.attempts;
    return;
  end if;
  if r.attempts >= p_max then
    return query select 'over'::text, r.attempts;
    return;
  end if;
  update public.assess_pages ap
    set attempts = r.attempts + 1, shot = p_shot, status = 'reading', kind = p_kind, item_no = p_item,
        read = null, grade = null, grade_tries = 0, flagged = false, flag_note = null,
        model_read = null, model_grade = null, image_path = null, updated_at = now()
    where ap.session_id = p_session and ap.page_no = p_page;
  return query select 'fresh'::text, r.attempts + 1;
end
$$;

-- 서비스 롤(API)만 부른다
revoke all on function public.assess_charge(text[], integer[], timestamptz) from public, anon, authenticated;
revoke all on function public.assess_reserve_page(uuid, integer, text, integer, text, integer) from public, anon, authenticated;
grant execute on function public.assess_charge(text[], integer[], timestamptz) to service_role;
grant execute on function public.assess_reserve_page(uuid, integer, text, integer, text, integer) to service_role;

-- ── 6. RLS — 쓰기 정책 없음(서비스 롤만). 읽기: 관리자만 ─────────────────
alter table public.assess_sets enable row level security;
alter table public.assess_people enable row level security;
alter table public.assess_sessions enable row level security;
alter table public.assess_pages enable row level security;
alter table public.assess_calls enable row level security;

drop policy if exists assess_sets_admin on public.assess_sets;
create policy assess_sets_admin on public.assess_sets for select to authenticated using (is_admin());
drop policy if exists assess_people_admin on public.assess_people;
create policy assess_people_admin on public.assess_people for select to authenticated using (is_admin());
drop policy if exists assess_sessions_admin on public.assess_sessions;
create policy assess_sessions_admin on public.assess_sessions for select to authenticated using (is_admin());
drop policy if exists assess_sessions_own on public.assess_sessions;     -- (예전 초안의 '자기 것 읽기' — 해시·판독 원문이 보여서 뺐다. 학생은 API 로만)
drop policy if exists assess_pages_admin on public.assess_pages;
create policy assess_pages_admin on public.assess_pages for select to authenticated using (is_admin());
drop policy if exists assess_pages_own on public.assess_pages;
drop policy if exists assess_calls_admin on public.assess_calls;
create policy assess_calls_admin on public.assess_calls for select to authenticated using (is_admin());

-- ── 7. 사진 버킷 (비공개 — 서비스 롤만 올리고, 관리자 화면은 서명 URL 로 본다) ─
insert into storage.buckets (id, name, public) values ('assess-pages', 'assess-pages', false)
on conflict (id) do nothing;

-- ── 8. 설정 기본값 (이미 있으면 그대로) ─────────────────────────────────
insert into public.app_settings (key, value) values
  ('assess_store_images', 'off'),      -- on 이면 펴진 쪽 사진을 assess-pages 에 저장 (손글씨 데이터) — 동의서 정리 뒤 켤 것
  ('assess_anon', 'on')                -- off 면 QR 비로그인 응시를 막고 로그인 응시만
on conflict (key) do nothing;
-- 선택: assess_model_read · assess_model_strong · assess_model_grade (없으면 photo_model · photo_model_fallback · photo_model_grade)
--       assess_limits = '{"anon_ip_day":400,"user_day":300}' 처럼 JSON 으로 한도 덮어쓰기
