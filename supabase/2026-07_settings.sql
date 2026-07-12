-- 개인 환경설정 저장 (알림·사운드 등)
alter table public.profiles
  add column if not exists settings jsonb not null default '{}';
