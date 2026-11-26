-- 2026-11 운영자 학습 허용 (learn_grants)
-- 원장님 지시(2026-11-26): 지금 가입된 학생 전원에게 관리자 기능을 뺀 학습 기능을 모두 연다.
--  · 보호자 동의 · 휴대폰 인증 · 학원 고유번호를 '받은 것처럼' 꾸미지 않고, 운영자가 열어 준 사실을 따로 남긴다.
--  · 행이 있으면 앱의 인증 관문(App.jsx VerifyGate)과 AI 관문(api/ai.js · api/photo.js 의 고유번호 확인)을 통과한다.
--    관리자 화면·관리자 태스크는 그대로 관리자만.
--  · 학생은 자기 행을 읽기만 한다. 쓰기는 관리자만(profiles 는 학생이 자기 행 대부분의 열을 고칠 수 있어 여기 두지 않음).
--  · 이 SQL 은 두 번 실행해도 같다.
-- 되돌리기: delete from public.learn_grants where note = '2026-11-26 원장님 지시: 가입 학생 전원 학습 기능 허용';
--          (표째 지우려면 drop table public.learn_grants; — 앱은 표가 없으면 예전처럼 동작)

create table if not exists public.learn_grants (
  user_id    uuid primary key references public.profiles(id) on delete cascade,
  granted_by uuid references public.profiles(id) on delete set null,
  granted_at timestamptz not null default now(),
  note       text
);
comment on table public.learn_grants is
  '운영자 학습 허용 — 행이 있으면 보호자 동의·본인 인증·학원 고유번호 없이도 학습 기능(관리자 기능 제외)을 연다. 동의·인증 기록과 섞지 않는다.';

alter table public.learn_grants enable row level security;

drop policy if exists learn_grants_read on public.learn_grants;
create policy learn_grants_read on public.learn_grants for select to authenticated
  using (user_id = (select auth.uid()) or public.is_admin());

drop policy if exists learn_grants_admin on public.learn_grants;
create policy learn_grants_admin on public.learn_grants for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

revoke all on public.learn_grants from anon;

-- 2026-11-26 시점 가입 학생 전원 (통합되어 끝난 계정 제외)
insert into public.learn_grants (user_id, granted_by, note)
select p.id,
       (select a.id from public.profiles a where a.role = 'admin' order by a.created_at limit 1),
       '2026-11-26 원장님 지시: 가입 학생 전원 학습 기능 허용'
from public.profiles p
where p.role = 'student' and p.merged_into is null
on conflict (user_id) do nothing;
