-- 회원가입 확장: 아이디·성별·출생년도·학년·학교
alter table public.profiles
  add column if not exists username text unique,
  add column if not exists gender text check (gender in ('male','female') or gender is null),
  add column if not exists birth_year int,
  add column if not exists grade text,
  add column if not exists school text;

-- 가입 시 메타데이터 → 프로필 자동 반영 (트리거 갱신)
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, name, username, gender, birth_year, grade, school)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
    nullif(new.raw_user_meta_data->>'username', ''),
    nullif(new.raw_user_meta_data->>'gender', ''),
    nullif(new.raw_user_meta_data->>'birth_year', '')::int,
    nullif(new.raw_user_meta_data->>'grade', ''),
    nullif(new.raw_user_meta_data->>'school', '')
  );
  return new;
end $$;
