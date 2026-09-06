# 1-B: mathir.js v1.5 r2 동형 패치 (2026-09-07)

## 들어 있는 것
- `src/lib/mathir.js` — 새 파일(교체). v1.0(스펙 v1.1)에서 **v1.4 답 표기층 + v1.5 + r2**까지 한 번에 올린 파이썬 동형 이식.
- `itemfactory/mathir.py`, `improvements/mathir_v15.py`, `improvements/mathir_v15.diff` — 파이썬 쪽 소수정 2건 반영본(아래 "함께 바뀐 것"). 이미 커밋한 r2와 내용상 동작 차이는 없지만 JS와 글자까지 같게 맞춘 것이라 같이 덮어쓴다.
- `improvements/tools/test_mathir.mjs` — JS 자가 시험(파이썬 자가 시험과 같은 케이스 + v1.4 답 표기 + r2).

## 검증한 것
- JS 자가 시험 전부 통과. 파이썬 자가 시험 전부 통과.
- **동형 검사**: 코퍼스 산출물 4,444건(반영 4,413 + 둘째 문항 23 + 보류 8)의 모든 `[[ ]]` 조각에 대해 파이썬·JS의 IR·표시 문자열, 답 파싱 결과(kind·IR·unit·sign), 도형 검사 결과가 **전부 일치**(불일치 0).
- **하위 호환**: v1.4 반영분 3,824건에 대해 옛 mathir.js(v1.0)와 새 mathir.js의 IR이 전부 동일(불일치 0). 표시만 recdec 소수점(`03̇`→`0.3̇`)·곱 병치(`(2a) × b`→`2ab`, `(−5) × x`→`−5x`, `92^(n+1)`→`9 × 2^(n + 1)`)가 고쳐진다.

## 적용 (Codespace 터미널, 레포 루트)
```
unzip -o step1b_mathir_js.zip
node improvements/tools/test_mathir.mjs        # "mathir.js 자가 시험 전부 통과 (v1.5 r2)"
python3 itemfactory/mathir.py                   # "mathir.py 자가 시험 전부 통과 (v1.5 r2)"
git add src/lib/mathir.js itemfactory/mathir.py improvements/mathir_v15.py improvements/mathir_v15.diff improvements/tools/test_mathir.mjs improvements/README_1B.md
git commit -m "mathir.js v1.5 r2 (py 동형)" && git push
```
`node` 시험이 "Unexpected token 'export'"로 실패하면(package.json에 "type":"module"이 없는 경우) `node --experimental-default-type=module improvements/tools/test_mathir.mjs`.
push 후 Vercel 배포가 끝나면 관리자 코퍼스 화면에서 반영된 문항 몇 개가 전과 같이 보이는지(수식 깨짐 없음) 확인 → 그다음 2단계(figs 자산) → 3단계(ALL_v15.json 반영).

## 함께 바뀐 것(파이썬 소수정 2건, r2 커밋본 대비)
1. `recdec(0, 3` 처럼 괄호가 안 닫힌 입력이 TypeError로 새던 것을 문법 오류(V-01)로 보고하도록 `_plain_run` 보강 — JS `plainRun` 동일.
2. 곱 표시에서 "함수 표시가 숫자로 시작하는지" 판정을 명시적 집합(0-9·위첨자·아래첨자)으로 — 파이썬 `str.isdigit()`과 JS `/\d/`가 달랐던 것을 양쪽 같은 집합으로 통일(표시 결과는 종전 파이썬과 동일).

## 선택 사항(이번엔 손대지 않음)
- `api/transcribeJob.js`의 전사 프롬프트(SYS_T)는 v1.1 함수 목록 그대로다. 새 전사에서도 v1.5 표기를 쓰게 하려면 함수 줄에 `cases app iter xbar hat box op nota idx tr dig`, 도형에 `image{src} scene{pts}`, 상수에 `cdots`를 추가하면 되지만, 러너 품질에 영향이 있으니 별도로 시험한 뒤 적용할 것.
- `image` 도형의 실제 렌더(`<img src>`)는 도형을 그리는 컴포넌트(StageFigure.jsx?) 쪽 일 — 2단계에서 그 파일을 보고 맞춘다.
