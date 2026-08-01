-- 질문대화 마무리 상태 (2026-08)
-- draft = 작성 중(마무리 전, 이어쓰기 대상) / done = 마무리됨(제목 확정)
alter table public.concept_chats add column if not exists status text not null default 'done';
alter table public.concept_chats drop constraint if exists concept_chats_status_ck;
alter table public.concept_chats add constraint concept_chats_status_ck check (status in ('draft','done'));
