# avgen — 기본기 해설 생성기 (단원 100제 · 주차별 기초 다지기)

시청각 학습 › 문제 풀이 해설과 교실 모니터 기본기 액자(초등 · 중등 · 고등)에 쓰는 문항을 만든다. 만든 파일은 손으로 고치지 않는다.

| 만드는 것 | 명령 | 쓰는 곳 |
|---|---|---|
| 단원 100제 — 단원 100가지(초등 36 · 중등 30 · 고등 34) × 100문항(1 ~ 5단계 20문항씩) | `python3 export.py [단원 id …]` | `src/features/display/basics/<id>.js` · `index.js` · `thumbs.js` |
| 주차별 기초 다지기 — 학년마다 주 2회 × 52주 = 104회차 × 20문항(5단계 × 4) | `python3 weeks.py [학년 …]` (전체 약 3분) | `public/av-weeks/<학년>/index.json` · `<회차 id>.json` |
| 유형 — 단원 100제의 한 단계(20문항) = 500가지 · 유형마다 교과서 단원 · 프린트 코드 | `python3 typetags.py` (단원을 더하거나 `weeks.py`의 `TAG`를 고친 뒤) | `src/features/display/basics/typetags.js` |

- 필요: python3 · sympy. 레포 뿌리는 이 폴더의 한 단계 위(다르면 `ASHRAIN_REPO`).
- 단원 생성기: `g_*.py`의 함수 하나가 단원 하나(`Set` 100문항). 등록표는 `export.py`의 `REG`(id · 학년 범위 · 아이콘 · `모듈:함수` · 설명 · 예전 키 · 주요 단원).
- 회차에만 쓰는 생성기: `weeks_extra.py`의 `EXTRA`(`g_x1` ~ `g_x6` — 교과서 단원 가운데 단원 100제에 없던 27가지). 단계 → 교과서 단원은 `weeks.py`의 `TAG` + `EXTRA`.
- 회차 문항은 같은 생성기를 `core.SEED_SHIFT`를 1, 2, 3 … 으로 바꿔 다시 돌려 뽑는다 — 단원 100제(SEED_SHIFT 0)와 따로, 학년 안에서는 겹치지 않게(그림이 자료인 문항은 발문 + 그림으로 판정).
- 유형(단원 100제의 한 단계 20문항, 학생앱 `#/av/e-ten.3`): 문항은 단원 자료에서 그 단계만 1 ~ 20번으로 다시 붙인다(앱 `src/lib/avtypes.js`) — 생성기는 교과서 단원(`weeks.py`의 `TAG`)과 코드만 만든다.
- 프린트 코드: `codes.json`(단원) · `wcodes.json`(회차) · `tcodes.json`(유형) — 지우면 코드가 바뀐다. 새 코드는 셋 모두와 겹치지 않게 뽑는다. `meta.json`은 `export.py` 부분 실행 때 `index.js`를 온전히 다시 쓰는 캐시.
- 검산: `Set.add`가 판서의 「=」 줄을 sympy로 다시 계산해 틀리면 멈춘다. 레포에서 `node tests/display-basics.test.mjs` · `node tests/display-weeks.test.mjs`(분수 계산기로 한 번 더 · 그림 칸 · 판 짜기 · 문서 · 추천).

## 생성기를 고칠 때

1. `python3 try.py <모듈> <함수 …>` — 100문항 · 단계별 20 · 검산 수 · 물음 길이.
2. 그려 보기: `python3 dump.py <모듈> <함수>` → `node shot2.mjs /tmp/cv/<함수>.json <번호,…> light end` → `python3 montage.py out.png <png …>`.
3. 단원 100제는 `python3 export.py <id>`, 회차는 `python3 weeks.py` — 무작위 수를 더 뽑게 바꾸면(조건 추가 등) 이미 낸 문항이 바뀐다. 그림 좌표만 고치는 수정은 문항이 그대로다.
4. 지켜 온 것: 중1 · 중2 문항에 √ 없음 · 빼기 기호는 `−`(Set.add 가 바로잡음) · 흑백 인쇄에서도 구분되게(색만으로 구분하지 않기) · 조사는 `eun · iga · eul · wa · ro`로.
