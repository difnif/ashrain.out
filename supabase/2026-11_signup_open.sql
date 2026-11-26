-- 2026-11 가입 완료 = 바로 이용 · 관리자 가입 로그
-- 원장님 결정(2026-11-26): "회원가입이 모두 다 된 상태라면, 누구든지 승인 절차 없이 이용할 수 있게.
--   대신 이름·닉네임·나이와 함께 누가 언제 몇 시 몇 분에 가입했는지 관리자 모드에서 확인할 수 있게."
-- 이 SQL 은 두 번 실행해도 같다. (DB 에는 2026-11-26 에 이미 적용됨)

-- 1) 보호자 동의: 문자 인증 + 동의 제출 = 즉시 활성 (관리자 승인 단계 없음)
--    · 같은 (학생, 보호자 번호)가 반려된 적이 있으면 그때만 'pending' 으로 남겨 관리자가 본다.
--    · api/guardian.js v1.1 도 같은 규칙으로 저장한다. 이 트리거는 그 배포 전에 들어오는 건까지 덮는다.
--    · 되돌리기(관리자 승인으로 돌아가기): drop trigger guardian_consent_auto_active on public.guardian_consents;
create or replace function public.guardian_consent_auto_active()
returns trigger
language plpgsql
security definer
set search_path = public, pg_temp
as $$
begin
  if new.status = 'pending'
     and new.consented_at is not null
     and new.guardian_phone is not null
     and not exists (
       select 1 from public.guardian_consents c
       where c.student_id = new.student_id
         and c.guardian_phone = new.guardian_phone
         and c.status = 'rejected')
  then
    new.status := 'active';
    new.approved_at := coalesce(new.approved_at, now());
  end if;
  return new;
end $$;

drop trigger if exists guardian_consent_auto_active on public.guardian_consents;
create trigger guardian_consent_auto_active
  before insert on public.guardian_consents
  for each row execute function public.guardian_consent_auto_active();
-- upsert(insert … on conflict do update)도 excluded 값이 이 BEFORE INSERT 트리거를 거친 값이라 같은 규칙이 된다.

-- 2) 관리자 가입 로그 — #/admin/signups (src/components/AdminSignups.jsx)
--    관리자에게만 행이 나온다(그 밖의 계정은 빈 결과). 가입 방식(아이디·구글·카카오)은 auth.users 에서.
--    나이는 오늘(한국 시간) 기준 만 나이.
create or replace function public.admin_signup_log(p_limit int default 300)
returns table (
  user_id         uuid,
  signed_up_at    timestamptz,
  name            text,
  nickname        text,
  username        text,
  role            text,
  birth_date      date,
  birth_year      int,
  age             int,
  is_minor        boolean,
  provider        text,
  phone_verified  boolean,
  onboarded       boolean,
  guardian_status text,
  guardian_at     timestamptz,
  guardian_warn   boolean,
  granted         boolean,
  merged          boolean
)
language sql
stable
security definer
set search_path = public, pg_temp
as $$
  select p.id, p.created_at, p.name, p.nickname, p.username, p.role,
         p.birth_date, p.birth_year,
         case when p.birth_date is not null
              then extract(year from age((now() at time zone 'Asia/Seoul')::date, p.birth_date))::int end,
         coalesce(p.is_minor, false),
         coalesce(u.raw_app_meta_data->>'provider', 'email'),
         coalesce(p.phone_verified, false),
         (p.birth_date is not null),
         g.status, g.consented_at, coalesce(g.age_gap_warn, false),
         exists (select 1 from public.learn_grants lg where lg.user_id = p.id),
         (p.merged_into is not null)
  from public.profiles p
  left join auth.users u on u.id = p.id
  left join lateral (
    select c.status, c.consented_at, c.age_gap_warn
    from public.guardian_consents c
    where c.student_id = p.id
    order by (c.status = 'active') desc, c.created_at desc
    limit 1
  ) g on true
  where public.is_admin() and p.role <> 'admin'
  order by p.created_at desc
  limit greatest(1, least(coalesce(p_limit, 300), 2000));
$$;

revoke all on function public.admin_signup_log(int) from public, anon;
grant execute on function public.admin_signup_log(int) to authenticated;
