# cnt100gen — 경우의 수와 확률 100제 넷 생성기 (중2-2)

학원 프린트 넷(문제지 · 해설지 PDF)과 해설 액자 「경우의 수와 확률 100제」(`src/features/display/cnt100-items.js`)를 같은 문항 · 같은 번호 · 같은 답으로 만든다. 만든 파일은 손으로 고치지 않는다.

| 프린트 | 코드 | 생성기 |
|---|---|---|
| 학년별 선발로 익히는 경우의 수와 확률 100제 | SQ9-HWR | `set_a.py` |
| 주머니 속 공으로 익히는 경우의 수와 확률 100제 | QS7-3DF | `set_b.py` |
| 영어 단어로 익히는 사전식 나열 100제 | QHD-WUB | `set_c.py` |
| 한 줄로 세우기 100제 — 이웃 · 양 끝 | Z2W-3KQ | `set_d.py` |

- 해설 액자 문항: `cd cnt100gen && python3 gen_disp.py ../src/features/display/cnt100-items.js` → `node tests/display-cnt100.test.mjs`
- 프린트 PDF: `cd cnt100gen && python3 render.py [선발 공꺼내기 사전식 한줄세우기]` → `cnt100gen/out/`(git 밖). 필요: pymupdf · google-chrome · Noto Sans CJK KR. 코드는 `render.py`의 `FIXED`(바꾸지 않는다).
- 문항마다 `ans`(공식으로 낸 답)와 `chk`(학생 · 공 · 문자열 · 줄을 하나하나 늘어놓고 직접 센 수)가 같아야 만들어진다.
- 해설 식 규칙(2026-11-28): 공식은 간단한 수여도 다 펼치고 줄마다 무엇을 센 식인지 이름표 — 「이름표: 펼친 식 = 값」(`common.py`의 `L` · `chain` · `row` · `c2s` · `c3s` · `pfeq` · `pnot`). 앞 줄에서 구하지 않은 수는 쓰지 않는다. 사전식은 덩어리 크기 줄(`blocks_lines`) → 숫자 분석.
- `figs.py` — 해설 액자 오른쪽 그림(자리 · 학년 · 주머니)이 판서 몇째 줄에 맞물리는지(줄 안의 글자로 찾는다).
- 이전판(공식을 덜 펼친 v1)은 프로젝트 문서 `SRC-…100제-v1.py`.
