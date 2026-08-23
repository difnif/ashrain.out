# 문항 공장 업무 프로세스 (itemfactory/PROCESS.md, v1.0)

로컬 = 생성 + 검증 + 출생 라벨만 / DB = 수납 / 분석 = 별도 층 — 이 격벽을 전제로 한 운영 절차.

## 0. 준비 (기기당 1회)

1. Supabase SQL Editor에서 `supabase/2026-08_item_factory.sql` 실행 (전체 1회)
2. `git clone https://github.com/difnif/ashrain.out` · Python 3.10+
3. 푸시용 패키지: `pip install supabase --break-system-packages`
4. `itemfactory/.env` 작성 — **절대 커밋 금지**
   ```
   SUPABASE_URL=https://<ref>.supabase.co
   SUPABASE_SERVICE_KEY=<service_role 키>
   ```
5. 루트 `.gitignore`에 두 줄 추가: `itemfactory/.env` · `itemfactory/out/`

## 1. 한 사이클 (개념 1개)

| 단계 | 하는 일 |
|---|---|
| ① 틀 수령 | 채팅에 "**m1-1-02 틀 줘**" (또는 "계속") → 틀 파일 수령 → `itemfactory/templates/`에 커밋 |
| ② 실행 | 작업 기기에서 `git pull` → `python factory.py m1-1-02 --push` |
| ③ 확인 | 콘솔 요약(적재/검토/폐기) + `out/<cid>_review.json` 훑기 |
| ④ 검수 | AdminConcepts 난이도 뱃지·브라우즈 모달로 샘플 열람 |
| ⑤ 공개 | 아래 SQL 1줄 (draft → live) |
| ⑥ 다음 | 채팅에 "계속" |

```sql
update test_items set status='live'
where status='draft' and test_type='concept_set'
  and concept_ids @> array['m1-1-02'];
```

드라이런(DB 안 건드림): `python factory.py <cid>` → `out/<cid>_pool.json` 생성만.
신뢰 쌓이면 검수 생략 직행: `--status live`.

## 2. 멀티 사이트 (학원·집·PC방)

- **분업 원칙**: 기기마다 다른 개념 담당 (예: 학원 m1-1 앞쪽 / 집 뒤쪽). 겹쳐 돌려도 안전 — DB 유니크 인덱스 + ignore_duplicates라 중복은 조용히 무시됨.
- `--site 학원` 태그로 어디서 만든 배치인지 gen_meta에 기록.
- PC방 등 임시 기기는 드라이런만 하고 pool.json을 챙겨와도 됨 (푸시는 .env 있는 기기에서).

## 3. 검토·폐기 규칙 (E-10)

- **완전 동일**(문제+보기 일치) → 자동 폐기, `item_rejects`에 사유·대상 기록.
- **구조 동일**(수치만 다름)이 *다른 출처*(수동/앱 생성/다른 틀)와 겹침 → `out/<cid>_review.json`에 보류, 푸시 안 함. 네가 보고: 버리거나, 살릴 것만 AdminItemGen ③탭으로 수동 등록.
- 같은 틀 안의 수치 변형은 정상이므로 검토 대상 아님.
- 폐기 현황: `select reason, count(*) from item_rejects group by 1;`

## 4. 구조 메모

- **content_key v2** = 문제문+보기 정규화 md5 (DB 자동 생성). 지문 같고 보기 다른 객관식이 공존 가능해짐. AdminItemGen 영향 없음.
- **struct_key** = 수치 마스킹 해시 — 유사 탐지용.
- **난이도** = 예상값(prior) 1~5. 실측 난이도는 분석 층이 별도 산출(L-25) — 이 값을 덮어쓰지 않는다.
- **틀 보관**: `item_templates`에 명세 등록 — 서빙 풀 400개 밖 전체 공간은 틀+인덱스로 언제든 리필.
- 앱 노출은 `status='live'`만 (ti_read 정책 확인됨).
