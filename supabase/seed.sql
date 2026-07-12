-- 개념 01: 소수와 합성수 (뷰어 확정 시안 그대로)
insert into public.concepts (id, unit_id, title, subtitle, sort_order, blocks) values (
'm1-1-01', 'm1-1', '소수와 합성수', '약수의 개수로 자연수를 분류하기', 1,
$$[
 {"id":"b1","type":"text","label":"먼저 떠올리기 · 약수","icon":{"kind":"emoji","value":"🔍"},
  "style":{"tone":"slate","size":"md","width":"full"},
  "lines":["약수는 어떤 수를 **나머지 없이** 나누어떨어지게 하는 수예요.",
   "빠짐없이 찾는 요령은 ==곱셈 짝꿍 찾기== — 곱해서 그 수가 되는 두 수는 둘 다 약수! 6이라면 짝꿍 두 쌍에서 [[teal:1, 2, 3, 6]] 네 개가 전부 나와요."],
  "figure":null},
 {"id":"b2","type":"definition","label":"핵심 정의","icon":{"kind":"emoji","value":"📐"},
  "style":{"tone":"teal","size":"md","width":"half"},
  "term":"소수","hanja":"素數",
  "text":"1과 자기 자신만을 약수로 가지는 수, 즉 ==약수가 정확히 2개==인 수",
  "chips":[2,3,5,7,11,13,17,19],"chipLabel":"20까지의 소수","figure":null},
 {"id":"b3","type":"definition","label":"핵심 정의","icon":{"kind":"emoji","value":"🧩"},
  "style":{"tone":"amber","size":"md","width":"half"},
  "term":"합성수","hanja":"合成數",
  "text":"1과 자기 자신 외에 **다른 약수가 더 있는** 수, 즉 ==약수가 3개 이상==인 수",
  "chips":[4,6,8,9,10,12,14,15,16,18,20],"chipLabel":"20까지의 합성수","figure":null},
 {"id":"b4","type":"warning","label":"꼭 조심할 것","icon":{"kind":"emoji","value":"⚠️"},
  "style":{"tone":"coral","size":"md","width":"full"},
  "items":["[[coral:1은 소수도 합성수도 아니다]] — 약수가 1개뿐이라 어느 쪽에도 속하지 않아요. 시험 단골!",
   "짝수 중 소수는 **2 하나뿐** — 4, 6, 8, …은 전부 2로 나누어떨어져서 무조건 합성수.",
   "홀수라고 다 소수가 아니다 — ==9 = 3×3==, 15 = 3×5, 21 = 3×7처럼 홀수인 합성수도 많아요."],"figure":null},
 {"id":"b5","type":"check","label":"바로 확인","icon":{"kind":"emoji","value":"✅"},
  "style":{"tone":"teal","size":"md","width":"full"},
  "question":"다음 수를 분류해 보세요:  1, 2, 9, 11, 15, 21",
  "answer":[{"group":"소수","nums":"2, 11","tone":"teal"},
   {"group":"합성수","nums":"9, 15, 21","tone":"amber"},
   {"group":"둘 다 아님","nums":"1","tone":"coral"}]}
]$$::jsonb)
on conflict (id) do update set blocks = excluded.blocks, title = excluded.title,
  subtitle = excluded.subtitle, sort_order = excluded.sort_order, updated_at = now();

insert into public.concept_qna (concept_id, block_id, question, answer, status) values
('m1-1-01','b2','0은 소수예요, 합성수예요?','둘 다 아니에요. 소수·합성수는 자연수(1, 2, 3, …)에서만 따지는 개념인데, 0은 자연수가 아니라서 아예 분류 대상이 아닙니다.','adopted'),
('m1-1-01','b4','왜 1은 소수에서 뺐어요?','1은 ''1과 자기 자신''이 같은 수라서 약수가 1개뿐이에요. 그리고 1을 소수로 인정하면 소인수분해 결과가 6 = 2×3 = 1×2×3처럼 여러 개가 되어 버려서, 답이 하나로 정해지도록 일부러 제외했습니다.','adopted'),
('m1-1-01','b1','짝꿍으로 약수를 찾을 때 언제까지 찾아요?','곱하는 두 수가 서로 가까워지다가 만나거나 순서가 뒤집히면 끝. 36이라면 1×36, 2×18, 3×12, 4×9, 6×6 — 여기서 멈추면 됩니다.','adopted');
