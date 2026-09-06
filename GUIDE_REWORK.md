# 보류 재작업 가이드 (v1.5 문법) — subagent용

목적: 1차 전사에서 **문법 한계 때문에 보류(review)** 된 문항을 mathir **v1.5**(`/root/esc/mathir_v15.py`) 문법으로 다시 써서 통과시킨다.
입력: `/root/esc/rework/batchNN.json` — 항목마다 `id, zip, image(절대경로), reason(보류 사유), seq, qtype, question(텍스트 혼합 초안), choices, answer, figure, difficulty_est, unit_id, confidence`.
출력: `/root/esc/rework_batchNN.py` — `ITEMS` 리스트(스키마 아래). 빌드: `python3 /root/esc/build_rework.py rework_batchNN` → `검산 불통과` 0건이 될 때까지 고친다.

기본 규칙은 `/root/esc/GUIDE.md`(§0~§7)와 같다. **이미지가 근거**이며, 초안의 텍스트 혼합 부분을 v1.5 표기로 바꾸는 것이 핵심이다. 초안 내용이 의심스럽거나 그림·수식이 애매하면 이미지를 Read로 다시 본다(항목의 `image` 경로). 이미지에 없는 내용은 만들지 않는다.

## v1.5에서 새로 쓸 수 있는 표기 (렌더 확인: `python3 -c "import importlib.util as u;s=u.spec_from_file_location('m','/root/esc/mathir_v15.py');m=u.module_from_spec(s);s.loader.exec_module(m);print(m.render_text('…'))"`)
- 경우 나눔 정의: `[[f(x) = cases(pow(3,x) + 1, x <= 1, 9 - 3 log(3,x), x > 1)]]` (식, 조건 쌍 — 짝수 인자, 최대 8). "x<0 또는 x>4" 같은 조건은 `cases(x, x < 0, x, x > 4, …)`처럼 구간을 나눠 쓰거나, 조건 하나로 못 쓰면 텍스트로 남기고 needs_review.
- 파생 함수 적용: `[[app(prime(f), x)]]` = f′(x), `[[app(prime(f, 2), x)]]` = f″(x), `[[app(comp(f, g), x)]]` = (f∘g)(x), `[[app(inv(f), 2)]]` = f⁻¹(2), `[[app(sub(S, 1), t)]]` = S₁(t), `[[app(sub(v,1), t)]]`, `[[iter(f, n, x)]]` = fⁿ(x). 방정식 안에서도 그대로: `[[app(prime(f), 1) = -55]]`, `[[app(comp(f, f), x) + frac(1,2) f(x) = n]]`.
- 그리스 문자 함수: `[[alpha(t) + beta(t) = 5]]`, `[[alpha(sub(t,1)) = alpha(sub(t,2))]]`. 상수·변수로는 `[[sigma]]`, `[[alpha]]`.
- 첨자·프라임 점 라벨: `[[seg(O1A) = 21]]`, `[[angle(A'PB)]]`, `[[tri(P1P2P3)]]`, `[[seg(A'B')]]`, `[[vec(OP1)]]`, `[[angle(F'PF)]]`, `[[quad(A'B'C'D')]]`, `[[par(seg(XX'), seg(YY'))]]`. (라벨 함수 seg/line/ray/arc/angle/tri/quad/vec 안에서만 숫자·`'`가 라벨로 붙는다.) 단독 점 이름은 텍스트(A′)로 두어도 된다.
- 통계: `[[xbar(X)]]` = X̄, `[[hat(p)]]` = p̂, `[[sigma]]`. 빈칸 상자: `[[box(1)]]` = □(가), `box(2)` = □(나) … 줄임표: `[[sub(a,1) + sub(a,2) + cdots + sub(a,n)]]`, `[[sub(a,k) sub(a,k+1) cdots sub(a,k+m)]]`. 3차원 좌표 `[[point3(1, 2, 3)]]`.
- 그 밖에 v1.4의 모든 표기는 그대로(예: `sum`, `lim`, `dinteg`, `mat`, `set`, `setb`, `comp(A)` 여집합, `ratio`, `deg` …).

## 어떻게 고치나
1. `reason`을 읽고 무엇이 문제였는지 파악한다(프라임 라벨 / 조각적 정의 / 적용 표기 / 그리스 함수 / 줄임표 / 빈칸 …).
2. `question`·`choices`의 텍스트 혼합 부분을 위 표기로 바꾼다. 예:
   - `f′(x)` 를 `prime(f)(x)`나 텍스트로 쓴 것 → `[[app(prime(f), x)]]`
   - `[[f(x)]] = { [[식]] ([[조건]]) ; [[식]] ([[조건]]) }` → `[[f(x) = cases(식, 조건, 식, 조건)]]`
   - `선분 AA′`, `[[sub(O,1)]]A`, `∠A′PB` 텍스트 → `[[seg(AA')]]`, `[[seg(O1A)]]`, `[[angle(A'PB)]]`
   - `[[alpha]]([[t]])` → `[[alpha(t)]]`; `([[comp(f, f)]])([[x]]) < 3` → `[[app(comp(f, f), x) < 3]]`
   - `[[sub(a,1) + sub(a,2)]] + ⋯ + [[sub(a,n)]]` → `[[sub(a,1) + sub(a,2) + cdots + sub(a,n)]]`
   - 빈칸 `(가)` 상자 → `[[box(1)]]` (식 안에 들어갈 때만; 문장 속 "(가)에 알맞은 수"는 텍스트 그대로)
3. 고칠 수 없는 사유(이미지 잘림, 한 이미지에 문항 2개인데 id 1개, 답 기호 ㉡처럼 답 문법 범위 밖, 정보가 그림에만 있음 등)는 그대로 `needs_review`에 사유를 남긴다. 도형 `unsupported`는 그대로 두어도 된다(도형만으로는 보류되지 않음).
4. `answer`는 초안 값을 유지(`derived_answer`로 넣거나 생략하면 초안 값 사용). 답을 새로 검토했으면 note에 적는다.
5. **모든 항목**을 ITEMS에 넣는다(고칠 게 없어 그대로 통과시킬 것도, 여전히 보류인 것도). build 결과의 `재작업 n` = batch 항목 수여야 한다.

## rework 파일 스키마
```python
# -*- coding: utf-8 -*-
ITEMS = []
def add(**kw): ITEMS.append(kw)
add(id="1cce8564",                 # batch의 id (앞 8자리 가능)
    qtype="short", question="…v1.5 표기…", choices=None,   # choice면 5개
    derived_answer="③",            # 생략하면 초안 answer 사용
    figure=None,                   # 초안 figure를 그대로 복사하거나 None
    confidence=0.85, needs_review=None, note="프라임 라벨을 seg(AA')로 교체")
```

---
# r2 추가 (2026-09-05) — 잔여 보류 회수 라운드 (batch11~14)

이번 라운드의 입력 항목은 `question` 등이 **직전 재작업 결과(초안)** 이고, `reason`에 왜 남았는지, `quick_answer`에 manifest의 빠른정답(보조 수단, 없으면 null)이 있다. 목표는 **문항 결함 의심을 뺀 모든 항목을 최대한 통과**시키는 것. `mathir_v15.py`가 r2로 확장되었다(아래 표기). 렌더 확인 명령은 위와 같다.

## r2에서 새로 쓸 수 있는 표기
- 사용자 정의 이항연산: `[[op(dcirc, a, b) = a b - a + b]]` → a ◎ b = ab − a + b, `[[op(star, op(dcirc, 2, 3), 4)]]` → (2 ◎ 3) ★ 4. 기호 이름표(OPSYMS): star ★, wstar ☆, circ ○, dcirc ◎, bcirc ●, fisheye ◉, odot ⊙, oplus ⊕, otimes ⊗, ominus ⊖, sq □, bsq ■, diamond ◇, bdiamond ◆, tri △, btri ▲, dtri ▽, bdtri ▼, heart ♡, spade ♠, club ♣, ast ∗, bullet •, ring ∘, dagger †, sharp ♯, flat ♭, ref ※, hash #, at @, amp &, arrow → 등(`mathir_v15.py`의 OPSYMS 참조). 이미지의 기호와 **같은 글자**를 골라야 한다. 피연산자가 합·차이면 이미지대로 소괄호를 써 `op(star, (x + 2y), (3y - x))`.
- 약속 괄호 기호: `[[nota(angle, x)]]` → ⟨x⟩, `[[nota(lt, x)]]` → <x>, `[[nota(brace, a)]]` → {a}, `[[nota(sq, a, b)]]` → [a, b], `[[nota(angle, a, b)]]` → ⟨a, b⟩ (2~3인자). 예: `[[nota(angle, x) = 8]]`, `[[nota(lt, 20) + nota(lt, 13)]]`.
- 첨자 괄호 `[[idx(P, 2)]]` → P[2], `[[idx((A - B), 2)]]` → (A − B)[2]. 전치행렬 `[[tr(B)]]` → Bᵗ.
- 자릿수 나열 `[[dig(a, b, c, d)]]` → abcd(= 1000a+100b+10c+d 뜻), `[[dig(2, 0, B, 5) - dig(1, B, A, 6) = dig(A, 3, 9)]]` → 20B5 − 1BA6 = A39.
- 문자 순환소수: `[[recdec(0, ab)]]` → 0.ȧḃ, `[[recdec(0, a0bc)]]` → 0.ȧ0bċ, 비순환부가 있으면 3인자 `[[recdec(0, ab, cd)]]` → 0.abċḋ (정수부, 비순환, 순환마디). 숫자만이면 종전과 같이 `recdec(0.2, 45)`. (첨자·줄임표가 든 순환마디 0.ȧ₁a₂⋯ȧₙ, 순환점 위치가 비표준인 인쇄 오류 예시 등은 여전히 불가 → 아래 "텍스트 혼합 통과".)
- 프라임 상수·변수: `[[y = a' x + b']]` → y = a′x + b′ (`f'(x)`도 허용되며 `app(prime(f), x)`로 자동 정규화).
- 답 표기: 원문자 답 `㉡`, `㉠, ㉣` 허용. 양의 부호 답 `+23`, `+3000` 허용(부호를 그대로 둔다).

## 이번 라운드 처리 규칙 (항목의 reason 유형별)
1. **사용자 정의 연산·기호** → 위 op/nota/idx/dig 로 정의식·계산식 전부 `[[ ]]` 안에 넣는다. 정의가 한글 문장이면(예: "a★b는 a와 b 중 큰 수") 정의 문장은 텍스트로 두고 계산식만 `[[op(star, 3, 5)]]`처럼.
2. **텍스트 혼합 통과(tags=["텍스트혼합"])**: r2로도 표기가 없는 부분(조건이 한글 문장인 경우 나눔, 밑줄 '(n−1)개'가 붙은 순환마디, 비표준 순환점 인쇄 등)은 텍스트 혼합을 그대로 두되, **모든 `[[ ]]` 조각이 파싱되고 렌더가 이미지와 같으면** `needs_review=None`, `tags=["텍스트혼합"]`, note에 어느 부분이 텍스트인지 적고 통과시킨다. 경우 나눔은 `[[f(x)]] = { [[x + 1]] (x가 홀수일 때), [[frac(x,2)]] (x가 짝수일 때) }` 꼴로.
3. **한 이미지 두 문항, id 1개(tags=["두문항_id1개"])**: id는 `quick_answer`와 답이 맞는 쪽 문항에 귀속(맞는 쪽이 없거나 둘 다면 위쪽 문항), 그 문항을 ITEMS에 통과시키고 note에 귀속 근거를 쓴다. **다른 쪽 문항은 EXTRAS에 완전 전사**(아래 `add_extra`) — 질문·선지·답·도형 전부 v1.5 문법으로, id는 나중에 발급되므로 parent_id만. 둘 다 검산 통과해야 한다.
4. **선지가 그림 / 정보가 그림에만(tags=["그림선지_이미지"] 또는 ["그림정보_이미지"])**: 이미지에서 해당 영역(선지 5개 묶음, 또는 수직선·흐름도 등)을 PIL로 **원본 해상도 그대로, 꼭 필요한 영역만** 잘라 `/root/esc/out/v15/figs/{id 앞 8자리}.png`(선지면 `{id8}_choices.png`)로 저장하고, figure 목록에 `{"fn": "image", "args": {"src": "figs/{id8}_choices.png", "raw": "선지 ①~⑤: …각 그림의 중립적 설명…"}}`을 **추가**한다(기존 unsupported 항목은 그대로 둠). 선지 문자열은 `"① (그림: 마름모)"`처럼 번호 + 짧은 중립 설명(설명이 애매하면 `"① (그림)"`). 빌더가 파일 존재를 검사한다(같은 이미지를 쓰는 id가 여럿이면 각 id 이름으로 저장하거나 같은 src를 공유해도 됨).
5. **이미지 잘림**: 같은 zip의 `manifest.json`에서 같은 `doc_id`의 `seq±1`(또는 `page±1`) 이미지를 열어 잘린 부분(선지 ④⑤, 첫 줄)이 이어지는지 확인한다. 이어지면 그 내용으로 완성하고 `tags=["잘림_인접이미지보완"]`, note에 보완 출처 이미지 파일명. 없으면 그대로 `needs_review`.
6. **답 기호 ㉠㉡㉢ / 양의 부호 답**: 이제 문법 안이므로 `derived_answer="㉢"`, `"+23"`처럼 그대로 넣는다(초안에 ㄷ으로 바꿔 둔 것은 이미지대로 ㉢으로 되돌린다).
7. **프라임 상수** `a' x + b'` 로. **전치** `tr(B)`. **세로셈** `dig(...)`.
8. 답은 초안 값 유지가 원칙. 초안에 답이 없고(`answer: null`) 이제 쓸 수 있게 된 경우(㉡ 등)만 이미지·풀이로 채우고 note에 근거. `quick_answer`는 보조 수단일 뿐 답을 그것에 맞추지 않는다.

## r2 rework 파일 스키마 (추가분)
```python
add(id="1c88b31d", qtype="short", question="…", choices=None, derived_answer="3", figure=None,
    tags=["두문항_id1개"],            # 선택: 위 규칙의 태그(여러 개 가능)
    confidence=0.85, needs_review=None, note="id 귀속 근거: 빠른정답 3과 위 문항 답 일치")
EXTRAS = []
def add_extra(**kw): EXTRAS.append(kw)
add_extra(parent_id="1c88b31d", position="하단",   # 같은 이미지의 둘째 문항 (id 미발급)
    qtype="short", question="…v1.5 문법…", choices=None, answer="5", figure=None,
    difficulty_est=2, confidence=0.85, note="…")
```
빌드 결과: `rework_batchNN: 재작업 n | 통과 n | 잔여 보류 n | 둘째 문항(extra) k (검산 불통과 0)` — `재작업 n`은 batch 항목 수와 같아야 하고, 검산 불통과는 0이어야 한다.
