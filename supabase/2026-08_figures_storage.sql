-- 개념 그림 저장소 (2026-08) — 공개 읽기, 관리자만 쓰기
insert into storage.buckets (id, name, public) values ('figures', 'figures', true)
on conflict (id) do nothing;

drop policy if exists figures_public_read on storage.objects;
create policy figures_public_read on storage.objects
  for select to public using (bucket_id = 'figures');

drop policy if exists figures_admin_insert on storage.objects;
create policy figures_admin_insert on storage.objects
  for insert to authenticated with check (bucket_id = 'figures' and public.is_admin());

drop policy if exists figures_admin_update on storage.objects;
create policy figures_admin_update on storage.objects
  for update to authenticated using (bucket_id = 'figures' and public.is_admin());

drop policy if exists figures_admin_delete on storage.objects;
create policy figures_admin_delete on storage.objects
  for delete to authenticated using (bucket_id = 'figures' and public.is_admin());
