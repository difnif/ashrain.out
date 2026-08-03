-- 시험 일정·디데이 (2026-08)
create table if not exists public.events (
  id uuid primary key default gen_random_uuid(),
  date date not null,
  title text not null,
  dday boolean not null default false,
  created_at timestamptz not null default now()
);
alter table public.events enable row level security;
drop policy if exists ev_read on public.events;
create policy ev_read on public.events for select to authenticated using (true);
drop policy if exists ev_admin on public.events;
create policy ev_admin on public.events for all to authenticated
  using (public.is_admin()) with check (public.is_admin());
create index if not exists ev_date on public.events (date);
