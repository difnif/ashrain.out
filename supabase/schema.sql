-- ═══════════════════════════════════════════════
-- ASH RAIN. Out — 초기 스키마 (신규 프로젝트용)
-- Supabase SQL Editor에서 전체 실행
-- ═══════════════════════════════════════════════

-- 1) 프로필 (auth.users 연동)
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  name text,
  role text not null default 'student' check (role in ('student','teacher','admin')),
  avatar_url text,
  created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
create policy profiles_read on public.profiles for select to authenticated using (true);
create policy profiles_update_own on public.profiles for update to authenticated
  using (id = auth.uid()) with check (id = auth.uid() and role = (select role from public.profiles where id = auth.uid()));

-- 가입 시 프로필 자동 생성
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, name)
  values (new.id, coalesce(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)));
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- 관리자 판별 헬퍼
create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as
$$ select exists (select 1 from public.profiles where id = auth.uid() and role = 'admin') $$;

-- 2) 개념 페이지
create table if not exists public.concepts (
  id text primary key,
  unit_id text not null,
  title text not null,
  subtitle text,
  sort_order int not null default 0,
  blocks jsonb not null default '[]',
  cover jsonb,
  updated_at timestamptz not null default now()
);
alter table public.concepts enable row level security;
create policy concepts_read on public.concepts for select to authenticated using (true);
create policy concepts_admin_write on public.concepts for all to authenticated
  using (public.is_admin()) with check (public.is_admin());

-- 3) 개념 QnA (학생 질문 → 관리자 채택)
create table if not exists public.concept_qna (
  id uuid primary key default gen_random_uuid(),
  concept_id text not null references public.concepts(id) on delete cascade,
  block_id text not null,
  question text not null,
  answer text,
  status text not null default 'pending' check (status in ('pending','adopted','discarded')),
  asked_by uuid references public.profiles(id),
  created_at timestamptz not null default now()
);
create index if not exists concept_qna_idx on public.concept_qna(concept_id, status);
alter table public.concept_qna enable row level security;
create policy qna_read on public.concept_qna for select to authenticated
  using (status = 'adopted' or asked_by = auth.uid() or public.is_admin());
create policy qna_insert on public.concept_qna for insert to authenticated
  with check (asked_by = auth.uid() and status = 'pending' and answer is null);
create policy qna_admin_update on public.concept_qna for update to authenticated using (public.is_admin());
create policy qna_admin_delete on public.concept_qna for delete to authenticated using (public.is_admin());

-- 실시간 (질문 접수 알림용)
alter publication supabase_realtime add table public.concept_qna;

-- 4) 아바타 저장 버킷 (Storage → 정책)
insert into storage.buckets (id, name, public) values ('avatars', 'avatars', true)
  on conflict (id) do nothing;
create policy avatars_upload on storage.objects for insert to authenticated
  with check (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy avatars_update on storage.objects for update to authenticated
  using (bucket_id = 'avatars' and (storage.foldername(name))[1] = auth.uid()::text);
create policy avatars_read on storage.objects for select to public using (bucket_id = 'avatars');
