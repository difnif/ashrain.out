-- 질문게시판 — 상태 확장 + 댓글 (2026-07)
-- 채택(adopted) = "답변 예정"(게시판 공개), answered = 답변 완료(단락 말풍선 노출)
alter table public.concept_qna drop constraint if exists concept_qna_status_check;
alter table public.concept_qna add constraint concept_qna_status_check
  check (status in ('pending','adopted','answered','discarded'));

-- 기존 '채택 + 답변 있음' 글은 답변 완료로 이관
update public.concept_qna set status = 'answered'
 where status = 'adopted' and answer is not null and length(trim(answer)) > 0;

-- 공개 범위: 답변 예정(adopted) + 답변 완료(answered) 모두 게시판에서 열람
drop policy if exists qna_read on public.concept_qna;
create policy qna_read on public.concept_qna for select to authenticated
  using (status in ('adopted','answered') or asked_by = auth.uid() or public.is_admin());

-- 댓글: 모든 로그인 유저 열람·작성, 본인/관리자 삭제. 표시 이름은 작성 시점 스냅샷.
create table if not exists public.concept_qna_comments (
  id uuid primary key default gen_random_uuid(),
  qna_id uuid not null references public.concept_qna(id) on delete cascade,
  user_id uuid not null references public.profiles(id) on delete cascade,
  display_name text not null,
  content text not null,
  created_at timestamptz not null default now()
);
alter table public.concept_qna_comments enable row level security;
create policy qnac_read on public.concept_qna_comments for select to authenticated using (true);
create policy qnac_insert on public.concept_qna_comments for insert to authenticated
  with check (user_id = auth.uid());
create policy qnac_delete on public.concept_qna_comments for delete to authenticated
  using (user_id = auth.uid() or public.is_admin());
create index if not exists qnac_idx on public.concept_qna_comments(qna_id, created_at);
