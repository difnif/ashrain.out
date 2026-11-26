-- ashrain.out — 시록고 강사도구 (2026-11) · 스캔본 차수
-- 학생 풀이 스캔본이 언제 스캔한 것인지: 1 = 1차 채점 때, 2 = 2차 채점 때(3차 …도 같은 식), null = 확실하지 않음.
-- 이 칸이 생기기 전에 올린 스캔본과 PC에서 옮겨 온 스캔본은 null(확실하지 않음)로 남는다.
-- 앱은 이 칸이 없어도 동작한다(차수 고르기만 꺼짐). SQL Editor 에서 그대로 실행 — 여러 번 실행해도 안전.

alter table public.tt_scans add column if not exists round smallint check (round between 1 and 9);
comment on column public.tt_scans.round is '언제 스캔한 것인지: 1 = 1차 채점 때, 2 = 2차 채점 때 …, null = 확실하지 않음';
