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

## 구조
```
supabase/schema.sql        프로필·권한·개념·QnA·아바타 버킷 (RLS 포함)
supabase/seed.sql          개념 01 (소수와 합성수) + 채택 QnA
src/lib/theme.js           라이트/다크 테마 훅
src/lib/concepts.js        개념·QnA 데이터 접근
src/components/            SplashAuth · Home · ConceptViewer · AdminQna · Signup
src/features/portrait/     ribbedGlass(필터) · facePipeline(MediaPipe) · PortraitStudio
public/brand/              손글씨 로고 레이어 (스플래시 애니메이션용)
```

## 배포
GitHub 저장소 push → Vercel/Netlify 연결 → 환경변수(VITE_*) 등록 → 자동 배포.
