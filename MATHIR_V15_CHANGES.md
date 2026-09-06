# mathir v1.5 제안 패치 (r2, 2026-09-05) — 변경 명세 및 mathir.js 동형 패치 체크리스트

파일: `mathir_v15.py`(v1.4 원본에 패치를 적용한 완성본, 자가 시험 포함) · `mathir_v15.diff`(원본 대비 diff, 372줄)
검증: v1.4 자가 시험 전부 통과 + v1.5·r2 시험 통과, 기존 산출물 4,436건(1차 3,709 + 재작업 704 + 둘째 문항 23) 전부 r2로 재검산해도 오류 0, IR(to_ir) 변화 0(하위 호환).
**r2는 r1(2026-09-04 커밋본)에 §7의 항목을 더한 것 — `improvements/` 폴더의 세 파일을 이 묶음으로 교체하면 된다.**
적용: `mathir.py`를 `mathir_v15.py` 내용으로 교체(또는 diff 적용) → 관리자 앱의 `mathir.js`에 아래 표대로 동형 패치 → 버전 문구 v1.5 → `GUIDE.md` §3·§4의 "v1.5 적용 시" 항목 반영 → 보류 중 문법 사유 항목 재전사 후 `build_out.py` 재실행.

## 1. 함수표(FUNCS) 추가

| 함수 | 인자 | 뜻 | 표시(disp) | 해결하는 보류 유형 |
|---|---|---|---|---|
| `cases(식1, 조건1, 식2, 조건2, …)` | 2~8, **짝수** (홀수면 V-02) | 경우 나눔 정의 | `{식1 (조건1) ; 식2 (조건2)}` | 조각적 정의(가장 많음) |
| `app(F, x, …)` | 2~6 | 파생 함수 적용 | F가 var/label/prime/inv/sub/iter/xbar/hat이면 `F(x)`, 그 외(comp 등)는 `(F)(x)` | f′(x), (f∘g)(x), f⁻¹(k), S₁(t), α(t) |
| `iter(f, n, x)` | 3 | 거듭 합성 | `fⁿ(x)` (n이 숫자면 위첨자, 아니면 `f^(n)(x)`) | fⁿ(x) |
| `xbar(X)` / `hat(p)` | 1 | 표본평균·추정량 | `X̄` / `p̂` (결합 문자 U+0304 / U+0302) | 확통 기호 |
| `box(k)` | 1 | 빈칸 상자 | `□(가)` (k=1..14 → 가~하) | 빈칸 (가)(나)(다) |

## 2. 상수·식별자
- `CONSTS`에 `cdots`(⋯, 평가 불가) 추가 → `sub(a,1) + cdots + sub(a,n)`.
- `GREEK`에 `sigma` 추가. 표시에서 그리스 이름을 실제 문자로 출력(`alpha`→α …, `GREEK_DISP`). **IR(to_ir)은 이름 그대로**라 데이터는 바뀌지 않음.
- 그리스 문자 함수 적용: `alpha(t)`가 `apply` 노드로 파싱(기존 한 글자 함수 `f(x)`와 같은 규칙, 학년 h1).

## 3. 렉서·파서
- 토큰에 `'` 추가(프라임). `_TOKEN` op 클래스 `[=<>+\-*/(),|']`.
- 기하 라벨 함수(`seg line ray arc angle tri quad vec`)의 인자는 **id·숫자·`'`를 이어 붙인 한 덩어리 라벨**: `seg(O1A)`, `angle(A'PB)`, `tri(P1P2P3)`. 표시에서 숫자는 아래첨자(₁), `'`는 ′.
- `point3` 렉서 버그 수정: 식별자 뒤 숫자를 붙인 이름이 FUNCS에 있으면 하나의 토큰으로(`point`+`3` 분리 방지). 다른 곳(`x2` 등)은 v1.4와 동일하게 병치 곱.

## 4. figure DSL(FIGS)
- `image`: 필수 `src` — 도형을 이미지 자산으로 저장(`{"fn":"image","args":{"src":"figs/<id>.png","raw":"설명"}}`). 렌더는 `<img>`.
- `scene`: 필수 `pts` — 선언형 장면. 권장 인자: `pts{"A":[x,y]}`, `segs[["A","B"]]`, `circles[{"c":"O","r":2}]`, `marks{"right":["B"],"eq":[["AB","AC"]]}`, `shade[["A","B","C"]]`, `axes:true`, `labels{}`. check_figure는 `pts` 존재만 검사(다른 키는 렌더러 재량).

## 5. mathir.js 동형 패치 체크리스트
1. FUNCS 표에 위 6개 함수 추가(인자 범위·학년 동일: cases h1 / app h1 / iter h2 / xbar·hat h3 / box m1).
2. 토크나이저: `'` 토큰, `point3` 병합, (렉서 정규식은 동일하게 유지).
3. `call()`: 라벨 함수 인자 이어 붙이기(id·num·`'`), `cases` 짝수 인자 검사(V-02), `GREEK` 이름의 함수 적용을 apply로.
4. `disp()`: 라벨의 숫자→아래첨자·`'`→′, var/apply의 그리스 문자 표시, `cases/app/iter/xbar/hat/box` 표시 규칙, `cdots`→⋯.
5. FIGS에 `image`, `scene` 추가 + 렌더(`<img src>` / SVG).
6. 버전 문자열 v1.5. 자가 시험 케이스(`mathir_v15.py` 하단)를 JS 테스트로 동일 이식.

## 6. 적용 뒤 재작업 범위
- 보류 488건 중 문법 사유(조각적 정의·f′(x)·합성/역함수 적용·첨자/프라임 라벨·그리스 함수·⋯·빈칸)는 전사 원본(`tools\items\items_*.py`)의 해당 문항만 v1.5 표기로 고쳐 `build_out.py`를 다시 돌리면 됨(전체 재전사 불필요).
- 남은 28개 zip은 v1.4 규칙으로 먼저 끝내고, v1.5 재작업을 한 번에 하는 것을 권장.

## 7. r2 추가분 (2026-09-05) — 잔여 보류 111건 회수용

### 7.1 함수표(FUNCS) 추가
| 함수 | 인자 | 뜻 | 표시(disp) | 해결하는 보류 유형 |
|---|---|---|---|---|
| `op(기호, a, b)` | 3 | 사용자 정의 이항연산 | `a ◎ b` (피연산자가 관계식·다른 op이면 괄호; 곱·거듭제곱·분수 안에서는 `(a ◎ b)`) | 약속 연산 ◎ ★ ◇ ⊗ △ … 32건 |
| `nota(괄호, x[, y])` | 2~3 | 약속 괄호 기호 | `⟨x⟩`, `<a, b>`, `{x}`, `[a, b]` … | ⟨x⟩(약수의 개수), <a, b>(최대공약수) 등 |
| `idx(P, x)` | 2 | 첨자 괄호 | `P[x]`, `(A − B)[2]` | 집합 기호 P[x] |
| `tr(A)` | 1 | 전치행렬 | `Aᵗ` | 전치 |
| `dig(a, b, …)` | 1~8 | 자릿수 나열 | `abcd` (전부 숫자면 값으로 평가: dig(4,3,5,8)=4358) | 자릿수 문자열, 세로셈 20B5 − 1BA6 = A39 |
| `recdec` | 2~**3** | (기존) + 3인자형 `recdec(정수부, 비순환, 순환마디)` | `0.abċḋ`; 인자에 문자 자릿수 허용 `recdec(0, a0bc)` = `0.ȧ0bċ` | 문자 순환소수 10건 |

- 기호 이름표 `OPSYMS`(op의 첫 인자, id 토큰만 허용: star ★ wstar ☆ circ ○ dcirc ◎ bcirc ● fisheye ◉ odot ⊙ oplus ⊕ otimes ⊗ ominus ⊖ oslash ⊘ sq □ bsq ■ dsq ▣ diamond ◇ bdiamond ◆ tri △ btri ▲ dtri ▽ bdtri ▼ ltri ◁ rtri ▷ heart ♡ bheart ♥ spade ♠ club ♣ ast ∗ bullet • ring ∘ dagger † ddagger ‡ sharp ♯ flat ♭ natural ♮ ref ※ hash # at @ amp & sun ☀ cloud ☁ umbrella ☂ snow ☃ smile ☺ note ♪ dnote ♫ check ✓ cross ✗ flower ✿ arrow → larrow ← uarrow ↑ darrow ↓ bowtie ⋈ wr ≀ hexagon ⬡ pentagon ⬠)와 `NOTASYMS`(nota의 첫 인자: angle ⟨⟩ lt <> brace {} sq [] paren () dsq ⟦⟧ dangle ⟪⟫ ceil ⌈⌉ flr ⌊⌋ dbar ‖‖). 이름표에 없으면 V-01. **IR에는 이름이 그대로 남는다**(`op(dcirc, a, b)`).
- `recdec` 인자 파싱: 인자가 id·num 토큰만으로 이루어지면(연산자·괄호 없음) 하나의 라벨(`a0bc`)로, 아니면 종전대로 식. 숫자 인자의 IR·평가는 v1.4와 동일. 문자 라벨은 평가 불가(V-03).

### 7.2 파서·답 표기
- 변수 프라임: `a'` → var `a'`(표시 a′, `a''` → a″). `f'(x)`·`f''(x)`는 파싱 시 `app(prime(f), x)`·`app(prime(f, 2), x)`로 **정규화**(IR에는 `'` 변수가 함수로 적용되는 형태가 남지 않음). 라벨 함수 안의 `'`(seg(A'B'))는 종전과 동일.
- 답 표기(parse_answer): 낱말 답 문자 집합에 원문자 `㉠~㉻` 추가(`㉢`, `㉠, ㉣`). 양의 부호 답 `+23`, `+3000` → 식 `23`에 `sign: "+"` 주석(부호 표기가 요지인 문항).

### 7.3 표시(disp) 수정 — IR 불변, 렌더만 바뀜 (mathir.js도 같이 고칠 것)
1. `recdec(0, 3)` → `0.3̇` (종전 `03̇`: 정수부 뒤 소수점 누락 버그).
2. 곱 표시: 병치 사슬을 그대로 잇는다 — `2 a b` → `2ab`(종전 `(2a) × b`), `-5x` → `−5x`(종전 `(−5) × x`), `2 sqrt(3) x` → `2√3x`, `(x+1)(x+2)` → `(x + 1)(x + 2)`, `-(x+1)(x-2)` → `−(x + 1)(x − 2)`. 단 오른쪽이 숫자로 시작하는 함수 표시이면 ` × `를 유지: `9 × pow(2, n+1)` → `9 × 2^(n + 1)`(종전 `92^(n+1)`로 붙던 버그), `2 frac(1,3)` → `2 × 1/3`.
3. `op` 노드는 원자가 아님: `pow(op(dcirc,a,b), 2)` → `(a ◎ b)²`, `4 op(dcirc,a,b)` → `4(a ◎ b)`.
기존 산출물에서 표시가 달라지는 조각 1,423개는 전부 위 1·2에 해당(개선), IR 변화 0.

### 7.4 mathir.js 동형 패치 체크리스트 (r2 추가)
1. FUNCS에 `op`(3, m1) `nota`(2~3, m1) `idx`(2, h1) `tr`(1, h1) `dig`(1~8, m1) 추가, `recdec` 최대 인자 3.
2. `OPSYMS`·`NOTASYMS` 표 이식. `call()`: `op`·`nota`의 첫 인자는 id 토큰을 표에서 찾아 label 노드(없으면 V-01); `recdec` 인자는 "id·num만"이면 라벨로 이어 붙이기.
3. `primary()`: id 뒤 `'` 처리 — `(` 가 따라오면 `app(prime(f[, n]), args)` 노드 생성, 아니면 var 이름에 `'` 부착.
4. `disp()`: var의 `'` → ′/″/‴; `op`·`nota`·`idx`·`tr`·`dig` 표시; `recdec` 라벨 원문 표시 + 3인자형 + 소수점 수정; 곱 병치 사슬 규칙(`_xprod`); `_atom`에서 op 제외.
5. `ev()`: `recdec` 3인자·문자 라벨(V-03), `dig` 평가.
6. `parse_answer`: 낱말 문자 집합에 `㉠-㉻`, 선행 `+` → sign 주석.
7. 자가 시험(`mathir_v15.py` 하단 "v1.5 r2 자가 시험")을 JS 테스트로 이식.

### 7.5 적용 뒤 반영 범위
- `out\v15\{zip}.rework_final.json` 704건 중 `v14_ok: true` 115건은 패치 전에도 반영 가능, 나머지 589건은 r2 패치 뒤 반영(그중 r2 전용 표기는 batch11~14의 약 70건 — `op/nota/idx/tr/dig/문자 recdec/a'/원문자 답`).
- `out\v15\{zip}.rework_extra.json` 23건(한 이미지 두 문항의 둘째 문항)은 **id 발급 후** 반영. `out\v15\figs\*.png` 18개는 `image` 도형 자산(src는 `figs/…` 상대경로) — 앱의 자산 경로 규칙에 맞춰 배치.
