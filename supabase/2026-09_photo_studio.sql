-- ashrain.out — 촬영 모듈 (2026-09) 선택 마이그레이션
-- 앱은 이 파일 없이도 동작한다: 표가 없으면 api/photo.js 가 라벨 저장을 조용히 건너뛰고(saved:false) 결과는 학생 기기에만 남는다.
-- SQL Editor 에서 이 파일을 그대로 실행하면
--   · 서술형 채점·풀이과정 검사 결과의 "라벨"이 쌓인다 (photo_answer_labels — 본문 없음, 순서·시각 없음)
--   · 보관 게이트가 central 이라 판정한 답안 원문만 따로 쌓인다 (photo_answers — 기본 정책 labels 에서는 한 건도 생기지 않음)
--   · 정책 스위치 app_settings.photo_retention 이 'labels' 로 놓인다 (labels|gated|all — 근거: LEGAL-판례조사-답안보관-v1)
-- 원칙: 두 표 모두 서비스 롤(서버)만 쓰고, 학생은 자기 행만 읽는다. 문항 본문·사진은 어디에도 저장하지 않는다.
-- 편집저작물 방어를 위해 라벨 표에는 created_at(초 단위 시각)·문항 번호·출처를 두지 않는다 — 날짜(created_day)만 둔다.

-- ── 1. 라벨 표 (텍스트 없음) ────────────────────────────────────────────
create table if not exists public.photo_answer_labels (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references auth.users(id) on delete cascade,
  feature        text not null check (feature in ('essay','check')),      -- essay 서술형 채점 · check 풀이과정 검사
  unit_guess     text,                                                    -- m1-1 … h3-3 (전사기 추정)
  std_grade      text check (std_grade in ('S','M','C')),                 -- 문항 표현 등급 (발문표준성 v2 기준)
  sub_type       text,                                                    -- 단순 소재 대입형 · 상황 설정형 · 자료 해석형 · 해당 없음
  el_grades      jsonb,                                                   -- {발문,조건제시,소재맥락,도형자료,지문}
  overlap_score  integer,                                                 -- 문항–답안 겹침 0~100
  overlap_level  text check (overlap_level in ('low','mid','high')),
  overlap_parts  jsonb,                                                   -- {sentences, run, words, nums}
  score          numeric,                                                 -- 채점 총점 (essay)
  max_score      numeric,
  verdict        text,                                                    -- excellent|good|partial|weak (essay)
  lights         jsonb,                                                   -- {충실성,논리성,명료성,간결성,독창성} → green|yellow|red (check)
  pitfalls       text[],                                                  -- 실수거리 태그
  error_kind     text,                                                    -- calc|concept|reading|transcription|sign|unit|none (check)
  mental_load    text,                                                    -- low|mid|high (check)
  retention      text not null check (retention in ('central','device')), -- 게이트 결정
  policy         text not null default 'labels' check (policy in ('labels','gated','all')),
  created_day    date not null default (now() at time zone 'Asia/Seoul')::date   -- 시각이 아닌 날짜만(KST) — 순서 정보 최소화
);
comment on table public.photo_answer_labels is '촬영 모듈 라벨 — 문항·답안 본문 없음. 학습 통계·개인화용. 표현 등급×겹침 게이트 결과(retention)를 함께 기록.';
create index if not exists photo_answer_labels_user_day on public.photo_answer_labels (user_id, created_day desc);
create index if not exists photo_answer_labels_unit on public.photo_answer_labels (unit_guess, std_grade);

alter table public.photo_answer_labels enable row level security;
drop policy if exists photo_answer_labels_own_select on public.photo_answer_labels;
drop policy if exists photo_answer_labels_admin_select on public.photo_answer_labels;
create policy photo_answer_labels_own_select on public.photo_answer_labels for select to authenticated using (auth.uid() = user_id);
create policy photo_answer_labels_admin_select on public.photo_answer_labels for select to authenticated using (is_admin());
-- insert/update/delete 정책 없음 → 서비스 롤(api/photo.js)만 쓴다.

-- ── 2. 답안 원문 표 (게이트가 central 일 때만) ──────────────────────────
create table if not exists public.photo_answers (
  id           uuid primary key default gen_random_uuid(),
  label_id     uuid not null references public.photo_answer_labels(id) on delete cascade,
  user_id      uuid not null references auth.users(id) on delete cascade,
  answer_text  text not null                                              -- 학생 답안 전사 원문 (문항 본문은 없음)
);
comment on table public.photo_answers is '촬영 모듈 답안 원문 — 보관 게이트(표현 등급 S, 또는 M+겹침 low)가 central 이라 한 답안만. 문항 본문·사진 없음.';
create index if not exists photo_answers_user on public.photo_answers (user_id);
create index if not exists photo_answers_label on public.photo_answers (label_id);

alter table public.photo_answers enable row level security;
drop policy if exists photo_answers_own_select on public.photo_answers;
drop policy if exists photo_answers_admin_select on public.photo_answers;
create policy photo_answers_own_select on public.photo_answers for select to authenticated using (auth.uid() = user_id);
create policy photo_answers_admin_select on public.photo_answers for select to authenticated using (is_admin());
-- insert/update/delete 정책 없음 → 서비스 롤만.

-- ── 3. 정책·모델 스위치 (있으면 건드리지 않음) ───────────────────────────
insert into public.app_settings (key, value) values
  ('photo_retention',   'labels'),            -- labels: 원문 저장 안 함 · gated: S·M(low) 만 central · all: 전부 central(테스트 전용)
  ('photo_model',       'claude-sonnet-4-6'), -- 전사·등급·문장 이해
  ('photo_model_grade', 'claude-opus-4-8')    -- 채점·풀이과정 검사
on conflict (key) do nothing;

-- ── 4. 통계용 뷰 — 단원×등급×보관 위치별 건수 (security_invoker: RLS 그대로 → 학생은 자기 것, 관리자는 전체) ──
create or replace view public.v_photo_label_stats with (security_invoker = true) as
select unit_guess, std_grade, feature, retention, count(*)::int as n,
       round(avg(overlap_score))::int as avg_overlap,
       round(avg(case when max_score > 0 then score / max_score end) * 100)::int as avg_pct
from public.photo_answer_labels
group by unit_guess, std_grade, feature, retention;
grant select on public.v_photo_label_stats to authenticated;

-- 되돌리기 (필요 시 수동):
--   drop view if exists public.v_photo_label_stats; drop table if exists public.photo_answers; drop table if exists public.photo_answer_labels;
--   delete from public.app_settings where key in ('photo_retention','photo_model','photo_model_grade');
