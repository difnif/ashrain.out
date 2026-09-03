# 전사 작업 가이드 (subagent용) — ashrain.out escalated 재전사

당신의 임무: zip 하나(`/root/esc/work/{ZIP}/`)의 모든 문항 이미지를 보고 mathir v1.4 문법으로 전사한 뒤,
`/root/esc/items_{SLUG}.py`를 작성하고 `python3 /root/esc/build_out.py {ZIP} items_{SLUG}`로 산출을 만든다.
**이미지가 유일한 근거다.** manifest의 `draft_a`(이전 실패 초안)는 보지 않아도 된다(참고만, 절대 복사 금지).

## 0. 절대 규칙
1. 이미지에 없는 것을 만들어 넣지 않는다(선지·수치·조건 창작 금지). 원문 표현을 그대로 옮기고 윤문하지 않는다. 오타로 보여도 그대로.
2. 검산 불통과를 final에 넣지 않는다 — build_out.py가 자동 처리하지만, 오류가 나면 문법을 고쳐서 통과시킨다(문법을 못 맞추면 `needs_review`).
3. `/root/esc/mathir.py`는 절대 수정하지 않는다.
4. **모든 문항(manifest items 전부, 같은 이미지에 id가 여러 개면 id마다)** 을 다룬다. build 출력의 `missing 0`을 확인한다.
5. 이미지가 흐리거나 잘렸으면 지어내지 말고 `needs_review="이미지 하단 잘림"` 등으로 표시(초안은 보이는 데까지).

## 1. 작업 순서
1. `python3 /root/esc/extract.py {ZIP}` 의 출력(또는 manifest.json)으로 항목 목록을 본다: id(앞 8자리면 됨), image, seq, unit_id, src_tag, quick_answer.
2. 이미지를 Read 도구로 본다(한 번에 3~4장씩 배치). 590px 폭이라 대체로 읽히지만, 작은 글씨·행렬 성분·첨자가 헷갈리면 PIL로 2배 확대해서 다시 본다:
   `python3 -c "from PIL import Image; im=Image.open('경로'); im.resize((im.width*2, im.height*2), Image.LANCZOS).save('/tmp/x.png')"`
3. 문항마다 dict를 만들어 ITEMS에 넣는다(아래 스키마). 같은 쪽에 id가 여러 개면 같은 내용으로 id마다 넣는다(`dup([...], **kw)` 헬퍼 사용).
4. `python3 /root/esc/build_out.py {ZIP} items_{SLUG}` 실행 → `검산 불통과`가 있으면 해당 문항 문법을 고쳐 재실행. `missing 0` 확인.
5. `python3 /root/esc/reverify.py {ZIP}` 가 OK를 출력해야 끝. 마지막 줄의 `| zip | 문항 n | 통과 n | 보류 n | 시각 |` 행과 함께 짧게 보고.

## 2. items 파일 스키마 (`/root/esc/items_{SLUG}.py`)
```python
# -*- coding: utf-8 -*-
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

add(id="1b87172e",            # manifest id 앞 8자리(전체도 가능)
    qtype="choice",           # 보기 ①~⑤ 있으면 choice / 답만 쓰면 short / 서술 요구면 essay
    question="…[[수식]]…",    # 문항 본문. 보기(<보기> ㄱㄴㄷ), 조건 상자 (가)(나)도 여기에 줄바꿈(\n)으로 포함
    choices=["…","…","…","…","…"],   # choice면 정확히 5개(①~⑤ 기호 제외), 아니면 None
    derived_answer="③",       # 이미지에 답이 있거나 짧은 풀이로 확실할 때만. 불확실하면 None (절대 추측 금지)
    figure=None,              # 도형/표가 있으면 [{"fn":…, "args":{…}}] 리스트, 없으면 None
    difficulty_est=3,         # 1~5 (모르면 None)
    confidence=0.9,           # 기본 0.9. 흔들리면 낮춤. needs_review면 0.7~0.8
    needs_review=None,        # 보류 사유 문자열(문법 범위 밖 / 도형 표현 불가 / 이미지 잘림 …). 없으면 생략
    note="…")                 # 풀이 요지·출처 머리말·특이사항 한 줄(review 사유 뒤에 붙음)
```
- `quick_answer`는 쓰지 않는다(build_out이 manifest에서 읽어 derived_answer와 비교, 어긋나면 자동 review).
- `unit_id`는 보통 생략(manifest 값 사용). 내용이 명백히 다른 단원이면 `unit_id="h3-2"`처럼 지정.
- 이미지 맨 위의 출처 머리말(예: `[2023년 9월 고1 30번/4점]`)은 question에 넣지 않고 note에 적는다.

## 3. mathir v1.4 문법 핵심 (수식은 `[[ ]]` 안에만; 한글·특수문자는 밖에)
- 토큰: 숫자(`3`, `0.25`), 영문 식별자, 연산자 `+ - * / = < > <= >= != ( ) ,`. `^`, `_`, `{}`, `[]`, `|`, `·`, `√`, `π`, `°`, 한글은 **마커 안에서 금지**.
- 식별자: **한 글자 변수**(a, x, A, E …) / 그리스 `alpha beta gamma delta theta lam mu omega phi` / 상수 `pi e inf empty i` / 함수 이름. 두 글자 이상은 오류 → `kB`는 `k B`, `AB`(행렬 곱)는 `A B`, `2AB`는 `2 A B`, `abx`는 `a b x`. (`4B`처럼 숫자+글자는 붙여도 됨.)
- 곱은 병치 `2x`, `a b`, `(a - b) x`. 숫자끼리 병치 불가(`2 3` 오류). `*`/`×`도 허용.
- 함수 적용: 한 글자 이름 `f(x)`, `S(n)`, `C(0, n - 1)`, `P(sub(x,1), sub(y,1))` — `f(x)`형은 모두 "함수 적용"으로 파싱되며 표시는 원문과 같다(`p(k + 1)`도 그대로 써도 됨).
- 관계식 연쇄 가능: `1 < x <= 3`, `a = b = c`.
- 주요 함수(인자 수): `frac(a,b)` 분수 · `pow(x,2)` 거듭제곱 · `sqrt(x)` · `root(n,x)` n제곱근 · `abs(x)` · `mixed(2,1,3)` 대분수 · `recdec(0.2,45)` 순환소수 · `fact(n)` · `perm(n,r) comb(n,r) pperm hcomb` · `pct(x)` % · `deg(30)` 각도 · `dms(35,30)` · `pm(a,b)` ± · `floor(x)` [x]
  기하: `seg(AB)` 선분(윗줄) · `line(AB)` · `ray(AB)` · `arc(AB)` · `angle(ABC)` ∠ · `tri(ABC)` △ · `quad(ABCD)` □ · `par(l, m)` ∥ · `perp(seg(AB), seg(CD))` ⊥ · `cong(a,b)` ≡ · `sim(a,b)` ∽ · `point(x,y)` 좌표 (x, y) · `point3(x,y,z)` · `vec(AB)` · `dot(a,b)`
  (세그/각/삼각형 인자는 **점 라벨 한 덩어리**: `seg(AB)`, `angle(OPA)`. 첨자 점(O₁, A′)은 넣을 수 없음 → 텍스트 혼합 + needs_review)
  집합·논리: `set(1,2,3)` {…} · `setb(x, cond)` {x | cond} (cond가 식 하나일 때만) · `in(x, A)` ∈ · `notin` · `subset(A,B)` ⊂ · `nsubset` · `union(A,B)` ∪ · `inter(A,B)` ∩ · `comp(A)` 여집합 Aᶜ · `comp(f,g)` 합성 f∘g · `card(A)` n(A) · `imp(p,q)` p→q · `iff(p,q)` · `neg(p)` ~p · `itv(a,b,cc|co|oc|oo)` 구간 · `conj(z)` 켤레
  지수로그·삼각: `log(x)` 상용로그 · `log(a, x)` 밑 a · `ln(x)` · `sin(x) cos(x) tan(x) csc sec cot`
  수열·미적: `sub(a, n)` 첨자 aₙ (`sub(a, n+1)`도 됨) · `sub(a, i, j)` 행렬 성분 · `set(sub(a,n))` 수열 {aₙ} · `sum(k, 1, n, 식)` Σ · `lim(x, a, 식)` / `lim(x, a, 식, +)` · `prime(f)` f′ · `dydx(y,x)` · `integ(식, x)` · `dinteg(a, b, 식, x)` · `inv(f)` f⁻¹
  행렬: `mat(행, 열, 성분들…)` 예 `mat(2,2, 1,0, -2,-1)` · 확통: `prob(A)` P(A) · `cprob(A,B)` P(A|B) · `ev(X)` · `var(X)` · `sd(X)` · `binomd(n,p)` · `normald(m,v)`
- **답(answer) 문법**: 선지 답은 `"③"`, 합답형은 `"ㄱ, ㄴ"`, 수는 `"36"`, `"-3"`, `"frac(3,2)"`, 각도 `"deg(36)"`, 단위 꼬리 허용 `"12 cm"`, 복수 해 `"[[x = 1]] 또는 [[x = 2]]"`, 병립 `"a = 5, b = -1"`.
- 렌더 확인: `python3 -c "import sys;sys.path.insert(0,'/root/esc');import mathir;print(mathir.render_text('…'))"`

## 4. 문법으로 못 쓰는 것 → 이렇게 (텍스트 혼합, 필요하면 needs_review)
- 나열/열거 `i = 1, 2, 3, 4` → `[[i]] = 1, 2, 3, 4` (콤마는 마커 밖). 순서쌍 6개짜리 `(a₁, …, a₆)` → `([[sub(a,1)]], [[sub(a,2)]], …)`.
- 집합 조건이 여러 개/한글 포함: `[[A]] = { [[x]] | [[x < 100]], [[x]]는 자연수 }` (중괄호·세로줄은 텍스트).
- 연립부등식/연립방정식의 중괄호: 두 식을 콤마로 나열 `[[식1]], [[식2]]`.
- 줄임표 `⋯`: 마커 밖 텍스트. `[[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,n)]]`.
- 빈칸 상자 (가)(나)(다): 텍스트. 식이 잘리면 `[[S(n)]] = (나)`, `= [[frac(1,2) × n]] × ((나))`처럼 조각으로.
- 화살표 `f: X→Y`: `[[f]]: [[X]]→[[Y]]`. 함수 정의 한글 설명: `[[f(x)]] = ([[x]]의 양의 약수의 개수)`.
- (f∘f)(x) 적용: `([[comp(f, f)]])([[x]])`(부등호는 텍스트) → needs_review 표시.
- **needs_review가 필요한 문법 한계**: 조각적(경우 나눔) 정의 `f(x) = { … (x<a) ; … (x≥a) }` / 프라임·첨자 점 라벨(A′, O₁A, ∠O₁O₂O₃) / 그리스 문자 함수 `α(t)` / 합성함수 적용 표기 / 그 밖에 뜻이 달라지는 우회. 사유를 짧게 적는다.
- 행렬 `A = (a_ij)` → `[[A = (sub(a,i,j))]]`; 성분 조건 `[[sub(a,i,j) = 0]]`. 선지의 행렬은 `[[mat(4,4, 1,0,1,0, …)]]`.
- 다항식 `pA³`처럼 문자·거듭제곱 병치: `p pow(A,3)`. 계수 곱 `a₁·100`: `sub(a,1) × 100`.

## 5. 도형(figure) 정책
- 표는 `{"fn":"table","args":{"head":[…],"rows":[[…],…]}}` (head는 있을 때만, rows 필수) — has_figure는 build가 자동 계산.
- 장식 그림(카드·상자 등 정보 없는 삽화)은 `{"fn":"unsupported","args":{"raw":"짧은 설명"}}`로 final 가능(confidence 0.85).
- 좌표평면·원·삼각형 복합 도형, 함수 그래프 등 **정보를 담은 기하 도형은 표현 불가** → `unsupported`로 raw 설명을 남기고 `needs_review="도형 표현 불가: …"`. (FIGS의 numline/coordplane/funcgraph 등은 인자 스키마가 불명확하므로 쓰지 않는다.)
- 도형이 없으면 `figure=None`.

## 6. 답(derived_answer) 정책
- 이미지에 정답이 인쇄돼 있으면 그것. 없으면 **짧은 계산으로 확실할 때만** 풀어서 넣는다(선지형은 대체로 확인 가능). 길고 어려운 문항은 `None`으로 두고 note에 "답 미도출".
- 절대 quick_answer를 베껴 넣지 않는다(정렬이 어긋난 문서가 많다). build_out이 quick_answer와 비교해 다르면 자동으로 review로 보낸다 — 그건 정상이다.
- 계수 세기 문제는 파이썬으로 전수 확인해도 좋다(짧게).

## 7. 효율
- 한 문항에 오래 매달리지 말 것. 전사가 목적이고, 풀이는 부수적이다. note는 한 줄.
- 이미지 4장 → 4개 dict 작성 → 다음 4장. 파일은 한 번에 쓰되(Write), 길면 두세 번에 나눠 Edit로 이어 붙여도 된다.

## 8. v1.5 적용 시 (mathir_v15 패치가 mathir.py·mathir.js에 반영된 뒤에만 사용)
- 경우 나눔: `[[f(x) = cases(pow(3,x) + 1, x <= 1, 9 - 3 log(3,x), x > 1)]]` (텍스트 혼합·needs_review 불필요)
- 파생 함수 적용: `[[app(prime(f), x)]]`=f′(x), `[[app(comp(f, g), x)]]`=(f∘g)(x), `[[app(inv(f), 2)]]`, `[[app(sub(S,1), t)]]`, 그리스 함수는 `[[alpha(t)]]` 직접 가능, 거듭 합성 `[[iter(f, n, x)]]`
- 첨자·프라임 점 라벨: `[[seg(O1A)]]`, `[[angle(A'PB)]]`, `[[tri(P1P2P3)]]`, `[[vec(OP1)]]`
- 통계: `[[xbar(X)]]`, `[[hat(p)]]`, `[[sigma]]` · 빈칸 상자 `[[box(1)]]`=□(가) · 줄임표 `[[sub(a,1) + cdots + sub(a,n)]]` · 3차원 좌표 `[[point3(1,2,3)]]`
- 도형: 정보를 담은 도형은 `{"fn":"image","args":{"src":"figs/<id>.png","raw":"…"}}` 또는 `{"fn":"scene","args":{"pts":{…},"segs":[…],…}}` 로 final 처리
