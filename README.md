# ASH RAIN. Out

수학은 매일. 개념 뷰어 · 질문-채택 루프 · 리브드 글라스 초상화를 담은 학습 앱.
(라이트 = 비 오는 거리 / 다크 = 재의 밤)

## 시작하기

```bash
npm install
cp .env.example .env      # Supabase 값 입력
npm run dev
```

### 1) Supabase
1. supabase.com 프로젝트 생성
2. SQL Editor에서 아래 4개 파일을 순서대로 전체 실행:
   `supabase/schema.sql` → `supabase/seed.sql` → `supabase/2026-07_profiles_extend.sql` → `supabase/2026-07_settings.sql`
   (이미 앞의 둘을 실행한 프로젝트라면 뒤의 둘만 실행)
3. Settings → API 에서 URL / anon key 복사 → `.env`

### 2) 첫 관리자
앱에서 회원가입 후, SQL Editor에서:
```sql
update public.profiles set role='admin' where id='<본인 uuid>';
-- uuid 확인: select id, name from public.profiles;
```

### 3) 초상화 기능 모델 (선택, 최초 1회)
```bash
npm install   # @mediapipe/tasks-vision 포함됨
cp -r node_modules/@mediapipe/tasks-vision/wasm public/models/wasm
```
`public/models/` 에 모델 2종 다운로드:
- https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite
- https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite

### 4) 라이트 테마 배경 사진 (선택)
`public/brand/rainy_street.jpg` 를 넣고 `src/components/SplashAuth.jsx`의
`.th-light` 블록 주석에 표시된 한 줄을 교체.

## 라우트
| 해시 | 화면 |
|---|---|
| (없음) | 비로그인: 스플래시+로그인(아이디·카카오·구글) / 로그인: 개념 목록 |
| `#/signup` | 회원가입 |
| `#/c/:id` | 개념 뷰어 (물음표 = 질문 보기/보내기) |
| `#/admin/qna` | (관리자) 질문 검토·채택 |
| `#/portrait` | 리브드 글라스 초상화 → 프로필 아바타 저장 |
| `#/me` | 마이페이지 (프로필·내 정보·환경설정·계정) |

### 학생앱 베타 — 문제풀이 (`#/solve/*`, 2026-09)
상단 기능바는 **개념 / 문제풀이 / 오답노트 / 질문** 네 개. 연산·사진 힌트는 문제풀이 허브 안으로 들어갔다.
공개(`status='live'`) 문항만 학생에게 보인다 — 생성 문항은 `#/admin/items` 에서 live 로 올려야 나온다.

| 해시 | 화면 | 기록 |
|---|---|---|
| `#/solve` | 문제풀이 허브 (이번 주 기록·자주 나온 실수) | — |
| `#/solve/set[/:conceptId]` | 개념별 문항 세트 풀기 → 해설·도형 애니메이션 → 결과·오답노트 저장 | `attempts` |
| `#/solve/item/:itemId` | 문항 하나 다시 풀기 (오답노트에서) | `attempts` |
| `#/solve/practice` | 예제·유제 개념 고르기 → `#/p/:conceptId` | `practice_progress` |
| `#/solve/omr` | 사진 채점 — 시험지·답안 카드 인쇄(4모서리 마커) → 촬영 → CV 인식(+AI 폴백) → 확인 → 채점 | `attempts` (`set_id=omr:<code>`) |
| `#/solve/read[/:itemId]` | 문장 해설 — 숫자·척도·단서 경계 표시, 구하는 것·주어진 조건 | — |
| `#/solve/mark[/:itemId]` | 표시 연습 — 동그라미·밑줄·빗금 → 정답 표시와 비교 | localStorage |
| `#/solve/essay[/:itemId]` | 서술형 자가채점 — 답안 작성/촬영 → 루브릭 자가채점 → 모범답안 | `essay_grades`(없으면 로컬) + `attempts` |
| `#/solve/ask/:itemId` | 문항 질문하기 (QuestionChat) | `concept_qna` (`block_id=item:<id>`) |
| `#/solve/test[/:type[/:scopeId]]` | 시험 보기 — 개념 묶음·단원·연산·산과·모의고사·Ash·Rain·Out 8유형. 범위 고르기 → 확인 카드 → 응시(타이머·답안 현황) → 결과 | `test_runs`(없으면 로컬) + `attempts` (`set_id=test:<type>:<ts>`) |
| `#/c/:id?review=1` | 개념 **복습 모드** — 단락을 순서대로 펼쳐 읽기(단락당 4초+끝까지 스크롤) → 퀴즈 3문제(live 문항) 만점이면 Ⓓ 10 | `concept_reviews` + `point_ledger`(currency=drop) — 서버(`api/review.js`)만 적립 |
| `#/me` 「지갑」 | Ⓟ Ash(유료 기능용, 쿠폰·지급 충전) · Ⓓ Drop(복습 보상) 잔액·내역·쿠폰 등록. 홈 히어로 아래에도 잔액 한 줄 | `point_ledger.currency` |

문항형 오답노트는 `wrong_notes.image_path = 'item:<test_items.id>'` 센티널로 저장한다(DDL 불필요).
선택 마이그레이션: `supabase/2026-09_student_beta.sql` (essay_grades · attempts 관리자 열람 · v_live_item_counts) · `supabase/2026-09_wallet_review.sql` (point_ledger.currency · point_balance_of · concept_reviews · test_runs). 둘 다 적용 전에도 앱은 동작한다(해당 기능만 "준비 중"·로컬 저장).
공용 모듈: `src/lib/items.js`(문항 로딩·attempts) · `src/lib/answers.js`(정답 판정) · `src/lib/marking.js`(표시 규칙) · `src/lib/omr/`(카드 레이아웃·인식) · `src/lib/exam.js`(시험 프리셋·선발·채점) · `src/lib/review.js`(복습 순위·상한·퀴즈 채점) · `src/lib/wallet.js`(재화 2종) · `src/components/ItemQuestion.jsx`/`ItemView.jsx`(문항 렌더·풀이). 테스트: `node tests/<name>.test.mjs`.

재화 규칙(확정): Ⓟ와 Ⓓ는 서로 바꿀 수 없다 · 결제(PG)·숍 없음 · Ⓓ 적립은 복습 완주뿐(출석·시험 보상 없음) · 상한 = 최근 읽은 순위별 5·3·3·2·2회, 하루 5회, 1회 10Ⓓ · 판정·적립은 전부 서버.

패치 반입(웹만으로): `main` 에서 `difnif-patch-<n>` 브랜치를 만들고 `*.patch` 를 루트에 올리면 `.github/workflows/apply-patch.yml` 이 `beta/student-app` 에 적용하고 PR 을 연다.

## 구조
```
supabase/schema.sql        프로필·권한·개념·QnA·아바타 버킷 (RLS 포함)
supabase/seed.sql          개념 01 (소수와 합성수) + 채택 QnA
src/lib/theme.js           라이트/다크 테마 훅
src/lib/concepts.js        개념·QnA 데이터 접근
src/components/            SplashAuth · Home · ConceptViewer(+ReviewMode) · ReviewCard · PointsCard · AdminQna · Signup
src/pages/solve/           학생앱 문제풀이 화면들 (Solve 허브 · ItemPlay · Exam · Omr · Read · Mark · Essay · AskItem)
src/features/portrait/     ribbedGlass(필터) · facePipeline(MediaPipe) · PortraitStudio
api/                       Vercel 서버리스 — ai(힌트·OMR·질문) · points(지갑) · review(복습 보상) · transcribeJob …
supabase/2026-09_*.sql     학생앱 베타 선택 마이그레이션 (student_beta · wallet_review)
public/brand/              손글씨 로고 레이어 (스플래시 애니메이션용)
.github/workflows/         apply-patch.yml — difnif-patch-* 브랜치의 *.patch 를 beta/student-app 에 적용
```

## 배포
GitHub 저장소 push → Vercel/Netlify 연결 → 환경변수(VITE_*) 등록 → 자동 배포.
