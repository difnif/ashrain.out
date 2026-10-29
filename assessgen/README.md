# assessgen — 서술형 평가 시험지 생성기

채팅방에서 회차(문항·채점 기준)를 정하면 이 생성기로 **PDF(확인·인쇄용) + JSON(앱 등록용)** 두 파일을 만든다.
JSON 은 관리자 화면 `#/admin/assess` 에 올리면 학생앱에 서술형 평가로 열린다(QR `https://ashrainout.com/e/<코드>`).

## 준비 (한 번)
```bash
cd assessgen && npm install          # 시험지 글꼴(@fontsource) — 앱 package.json 과 따로
pip install segno pymupdf playwright # Chromium 은 playwright 가 쓰는 것
```
저장소의 `src/lib/mathir.js`(수식) · `src/lib/assess/spec.js`(JSON 검사) · `src/lib/assess/sheet.js`(쪽 번호 띠) · `src/lib/omr/detect.js`(마커) 를 그대로 불러 쓴다 — 앱과 생성기가 늘 같은 규칙.

## 회차 만들기
1. `specs/<코드>.py` 에 `SPEC` 을 쓴다 (`specs/sample.py` 가 본보기)
   - `code` 영문 대문자·숫자 4~12자 — QR 주소. **열린 평가끼리 확인값(32가지)이 겹치지 않게**(겹치면 등록 때 경고)
   - `title` · `level`(elem·mid·high) · `grade_label`(중2 등) · `date`(YYYY-MM-DD)
   - `reveal` 정답 공개: `after_close`(권장 — 마감 뒤) · `after_submit`(다 채점된 제출 직후) · `never`
   - `opens_at` · `closes_at` (선택, ISO 시각)
   - `policy` 채점 정책: `carry`(full·half·none — ①이 틀려도 ②를 얼마나 인정) · `alt_method`(accept·deduct) · `answer_only_max`
   - `items` (1~13): `topic` · `story` · `figure_svg`(선택 — 스크립트·외부 링크 없는 SVG) · `conditions[]` · `ask` · `answer` · `solution[]` ·
     `rubric[]`(요소 1~5개: `element` · `points` 1~20 · `criterion` · `partial`) · `accept[]`(인정하는 다른 풀이)
   - 수식은 MathIR `[[x + y = 12]]`, 분수 `[[frac(3,10)]]`
   - `verify()` 를 두면 빌드 때 실행 — 정답·수치를 assert 로 검산
2. 빌드
   ```bash
   python3 assessgen/build_assess.py assessgen/specs/<코드>.py --png
   ```
   → `assessgen/out/<코드>/<코드>.pdf · <코드>.json` (+ `--png` 면 쪽 미리보기)
3. PDF 확인·인쇄 → JSON 을 관리자 화면에 등록

## 쪽 구성 (모든 쪽 같은 좌표계: 1000×1414 단위, 1단위 = 0.19mm, A4 여백 10mm)
- 1쪽 학생 확인 사항(풀이 작성 예시·주의) · 2쪽 강사 확인 사항(QR·학년·이름·필적 확인 문장·닉네임) · 3쪽부터 한 쪽에 한 문제(① 식 세우기 ② 식 풀기 ③ 구하는 것)
- 네 귀퉁이 마커 + 방향 막대 + 아래 가운데 **쪽 번호 띠 14칸**(쪽 4비트 + 평가 확인값 5비트, 해밍(13,9)+전체 패리티 — 칸 3개까지 잘못 읽어도 통과하지 않음)
- 띠·마커 값은 `src/lib/assess/sheet.js` 와 같아야 한다 — 빌드할 때마다 480가지 띠를 앱 코드와 대조한다

## 빌드 때 검산
회차 `verify()` · 필적 문장(자모·숫자·연산 기호) · MathIR 문법 · 넘침(카드 밖·마커 띠) · 답안 칸 최소 높이 · 앱 `validateSpec` ·
PDF 를 래스터로 떠서 앱 검출기로 펴고 쪽 번호 띠를 읽어 쪽·확인값 대조 · 띠 부호(1~3칸 오독 전부 거부)·앱과 같은 비트

## 사진 흉내 검사 (선택)
```bash
python3 assessgen/build_assess.py assessgen/specs/sample.py && python3 assessgen/build_assess.py assessgen/specs/sample_elem.py
python3 assessgen/verify/make_photos.py /tmp/ph            # 원근·회전·그림자·흐림·잡음·손글씨 흉내 11장
node assessgen/verify/run_pipeline.mjs . /tmp/ph assessgen/out/SAMPLE01/SAMPLE01.json   # 앱 촬영 처리 그대로 → 11 pass
```
