# 시드 명세 (seed spec v1) — Claude가 쓰고 로컬이 실체화한다

분업의 경계가 여기다.

| | 하는 일 | 산출 |
|---|---|---|
| **Claude(세션·API)** | 전사 코퍼스의 유형을 읽고 **파라미터화된 시드**를 쓴다 | `itemfactory/seeds/<seed_id>.json` |
| **로컬(파이썬)** | 시드를 수만 번 대입해 실체화하고 5관문으로 검산한다 | `out/gen/<seed_id>_pool.json` |

시드는 **파이썬 코드가 아니라 JSON**이다. 안의 식은 `genkit/expr.py`의 제한된 평가기에서만
돌아가고(허용 함수·이름 밖은 예외), 임의 코드가 실행될 수 없다. 채팅에서 시드를 받아
그대로 커밋해도 안전하다는 뜻이다.

---

## 파일 뼈대

```jsonc
{
  "seed_id": "m1-2-sector-arc",         // 파일명과 같게. 문항 gen_meta에 남는다
  "title":   "부채꼴의 호의 길이와 넓이",
  "unit_id": "m1-2",
  "concept_ids": ["m1-2-11"],
  "schema_id": "<schemas.id>",           // 근거로 삼은 유형 스키마 (있으면)
  "source_item_ids": ["<corpus_items.id>", "..."],   // 유형 참조한 원문항 — 복제가 아님을 남기는 자리
  "note": "무엇을 차용했고 무엇을 새로 썼는지 한 줄",
  "geometry": true,                      // ★ 해설 단수를 가른다: true → 2단, false → 3단
  "templates": [ /* 틀 1..N */ ]
}
```

`geometry`를 생략하면 도형 함수로 자동 판정한다(`figspec.is_geometry`).
틀마다 다르면 틀 안에서 다시 선언할 수 있다.

## 틀 하나

```jsonc
{
  "id": "m1-2-sector-arc-t1",
  "title": "반지름·중심각으로 호의 길이 구하기",

  // ── 라벨 (LABELING.md · 레지스트리 L-01~L-49)
  "skill": "부채꼴 호의 길이 공식",
  "prereq": ["원주 = 2πr", "비례식"],          // L-15
  "process": "절차수행",                       // L-40  개념이해|절차수행|추론|문제해결|표현
  "context": "기하맥락",                       // L-41  무맥락|생활맥락|기하맥락|자료맥락
  "ops": ["비례", "넓이"],                     // L-14  생략하면 문면·해설에서 자동 추정
  "traps": ["구하는대상혼동"],                  // L-21  부호|단위|조건누락|역연산|구하는대상혼동|제곱누락|평균오용
  "variant_axis": {"구하는 것 순환": "l 미지"},  // L-44  schemas.axes 의 어느 칸인지
  "discriminates": "중심각을 360에 대한 비율로 다루는가",   // L-43

  "qtype": "short",                            // short | choice
  "difficulty": 2,                             // L-06 예상 난이도 1~5 (실측 b와 영구 분리)
  "time_limit": 60, "points": 4, "pool_target": 120,
  "tags": ["부채꼴", "호의길이"],

  // ── 파라미터 공간 (전단사 색인 — 같은 idx면 언제나 같은 문항)
  "params": [
    {"name": "th", "values": {"in": [30, 45, 60, 90, 120]}},
    {"name": "k",  "values": {"int": [1, 10]}},
    {"name": "s",  "values": {"step": [0.5, 3, 0.5]}}
  ],

  // ── 파생값 (순서대로 평가, 앞의 값을 쓸 수 있다)
  //    ★ 조건은 여기서 '이미 만족하는 꼴'로 만든다 — LOCALGUIDE.md §3
  "derive": {"r": "k*360/gcd(2*th,360)", "kl": "2*(k*360/gcd(2*th,360))*th/360"},

  // ── 성립 제약 (G1). 하나라도 거짓이면 조용히 버린다
  "constraints": ["r <= 36", "kl >= 2"],

  // ── 난이도 비용 (설계문서 v0.1 §1). 생략하면 모든 파라미터·파생값을 쓴다.
  //    주어진 값(src)도 반드시 포함할 것 — 빠뜨리면 난이도가 낮게 잡힌다(R-04)
  "cost_values": ["r", "th", "kl"],

  // ── 의미 키 (math_key). 생략하면 derive 의 값들 + 정답
  "math_key_values": ["kl", "th"],

  // ── 독립 검증 (G2) — relation 또는 verify 중 최소 하나 필수
  "relation": "X/(2*r) - th/360",              // sympy가 X를 풀어 정답과 대조
  "unknown": "X",
  "answer_var": "kl",                          // 답이 π·단위를 포함할 때 수치는 이 변수로
  "verify": ["2*ks == kl*r", "kl > 0"],        // env + ans 로 평가되는 참/거짓 식들

  // ── 문면·답·도형 — 문자열 안의 {식}이 대입된다
  "question": "중심각이 [[deg({th})]]이고 반지름이 {r} cm인 부채꼴의 호의 길이를 구하시오.",
  "figure":   [{"fn": "sector", "args": {"r": "{r}", "angle": "{th}"}}],
  "answer":   "[[{kl} * pi]]",
  "answer_alt": ["[[{kl} * pi]] cm"],

  // ── 객관식이면
  "distractor_fmt": "[[{v} * pi]]",            // 오답 표기를 정답과 통일 (형식으로 답을 찍지 못하게)
  "distractors": [                              // 6~8개 넣을 것 — 규칙 R-01~03 으로 일부가 탈락한다
    {"expr": "kl",  "misconception": "MC-SECT-02"},
    {"expr": "r*r", "misconception": "MC-SECT-01"}
  ],

  // ── 해설 (기하 2단 / 그 외 3단) + 단계별 도식
  "sol1": "방침 한 문장 이상 — 왜 그 방법인지까지. 기하면 '도형 읽기'",
  "sol1_fig": [{"fn": "bar", "args": {…}}],     // 선택 — 해설 전용 도식도 쓸 수 있다
  "sol2": ["전개 1", "전개 2", "전개 3"],        // 잘게 쪼갤수록 좋다 (최대 8단계)
  "sol2_fig": [{"fn": "steps", "args": {"lines": ["…", "…"]}}],
  "sol3": "확인 한 문장 — 비기하(3단)만. 기하(2단)에는 두지 않는다",
  "sol3_fig": [ … ],
  "sol_check": "기하(2단)에서 '확인' 줄을 직접 쓰고 싶을 때. 생략하면 '답: X'가 들어간다.",

  // ── 서술형 (생략하면 해설에서 자동 조립)
  "model_answer": "학생이 그대로 옮겨 써도 되는 흐름글 한 문단",
  "rubric": [
    {"element": "관계식 세우기", "points": 4,
     "criterion": "…를 식으로 나타냈다.", "partial": "둘 중 하나만 반영하면 2점."}
  ]
}
```

## 해설 애니메이션 (sol1_anim · sol2_anim · sol3_anim)

원칙(2026-09-07): **도형은 처음부터 다 그려 두고(보조선 포함) 색으로 강조**하며 설명을 따라간다.
텍스트와 싱크(진행 중인 단계가 굵어짐), 그림 여백 클릭 = 일시정지/재생. 이동 문제만 실제로 움직인다.

```jsonc
"sol1_anim": [ [큐, …], [큐, …] ],          // 단일 텍스트 단계도 순차 큐 여러 개 가능
"sol2_anim": [ [큐, …], [], [큐, …] ],      // sol2 의 단계 수와 같은 길이 (짧으면 빈 큐로 채움)
```

재생: 기본 1×(단계 2.4초·이동 3.3초 — 예전의 1.5배 느림). 그림 오른쪽 위 `1.5×` 버튼으로 전환, 하단 진행바를 클릭·드래그해 위치 이동,
그림 클릭 = 일시정지/재생. 강조는 선 색 + 은은한 형광펜 번짐(glow), 글자는 노란 형광펜 배경.

큐 `{ "act": …, "k": "키" | ["키", …], "dur": ms, "keep": true }`  — `dur` 은 예전 1.5× 기준 값이라 1× 로 환산(×1.5)되어 쓰인다.

| act | 뜻 |
|---|---|
| `hl` | 강조 (다음 단계에서 해제, `keep:true` 면 유지) |
| `show` / `hide` | 보이기 / 숨기기 (유지) |
| `move` | 이동 — `train`(기차, 궤적 `trail` 동반) · `mover`(journey 위의 점) |
| `reveal` | `steps` 판서의 `line:i` 를 짚음(줄 배경 강조). **판서 줄은 처음부터 전부 보인다** — 숨겨 두는 것은 작은 빨간 메모(`hint:i`·`mark:i-j`의 note)만이고, 그 키를 `hl`/`pulse` 하는 순간 써지듯 나타난다 (2026-09-07 변경) |
| `pulse` | 잠깐 커졌다 작아짐 |

요소 키(`data-k`) — 렌더러가 붙인다.

| 도형 | 키 |
|---|---|
| scene | `pt:A` `lbl:A` `seg:A-B` `seglbl:A-B` `arc:A`(또는 arc의 `k`) `arc:A:lbl` `right:B` `eq:A-B` `shade:i` `circle:i` `label:i`(labels의 `k`) |
| passing | `train` `span` `span-lbl` `arrow` `arrow-lbl` `trail` |
| journey | `stop:i` `stop-lbl:i` `leg:i` `mover` |
| numline | `pt:라벨` `lbl:라벨` `seg:i` |
| coordplane | `pt:이름` `lbl:이름` `line:i` `run` `rise` `run-lbl` `rise-lbl` (`rise_run:["A","B"]` 로 기울기 삼각형) |
| steps | `line:i` `hint:i` `mark:i-j` — 줄은 `{"text", "hint", "marks":[{"on","note"}]}` 로 덧표시 가능 |
| bar | `row:i` `part:i-j` `part-lbl:i-j` `total:i` |
| sector | `sector` `arc` `radius` `r-lbl` `angle-lbl` |
| solid(cylinder) | `top` `height` `h-lbl` `radius` `r-lbl` |
| river | `bank:0/1` `flow` `flow-lbl` `down` `down-lbl` `down-sub` `up` `up-lbl` `up-sub` `span-lbl` `stop:i` `stop-lbl:i` |
| mountain | `slope` `base` `peak` `base-lbl` `peak-lbl` `up` `up-lbl` `up-sub` `down` `down-lbl` `down-sub` `total-lbl` |
| vessel | `vessel:i` `row:i` `total:i` `part:i-j` `part-lbl:i-j` |
| wire | `edge:AB`(역순 `edge:BA` 도 맞음) `pt:A` `lbl:A` `face:ABCD`(회전·역순 전부 맞음) — 위치관계용 입체 골격 |

## 해설 전용 도식 (문항 본문에는 못 쓴다)

문제에 그림이 없어도 해설에서는 그려서 설명한다. **사실적일 필요 없이, 서술형 답안에
샤프로 옮겨 그릴 수 있는 정도**면 된다.

| fn | 무엇 | 인자 |
|---|---|---|
| `journey` | 지점 사이의 이동 (거리·속력·시간) — 수직선이면 충분하다 | `stops[]`, `legs[{label, sub, back}]`, `total` |
| `passing` | 기차·터널/다리 통과 — 둥근 직사각형 + 두꺼운 선 | `obj{label,len}`, `span{label,len}`, `total` |
| `river` | **강물** — 두 줄이 강, 강 안에 강물 방향·속력, 위에 순방향(내려갈 때)·아래에 역방향(올라올 때) 조건 | `stops[]`, `span`, `flow{label,dir}`, `down{label,sub}`, `up{label,sub}` |
| `mountain` | **등산** — 우상향 굵은 초록 직선이 산. 오를 때 조건은 왼쪽에 화살표와 함께, 내려올 때는 반대편에 | `base`, `peak`, `up{label,sub}`, `down{label,sub}`, `total` |
| `bar` | 부분·전체 막대 (비율·개수 배분 — **액체에는 쓰지 않는다**) | `parts[{label,value,fill}]` 또는 `rows[]`, `total`, `name` |
| `vessel` | **용기에 담긴 액체** — 농도(소금물)·물탱크·원기둥에 물 채우기. 컵(`beaker`)·실린더(`cylinder`)·탱크(`tank`) | `rows[{name,total,parts[{label,value,kind:"water"|"salt"|"other"}]}]`, `kind`, `capacity` |
| `steps` | 식 변형을 줄 맞춰 보여주는 판서 | `lines[]` |

**상황은 간단하고 직관적인 그림 하나로 옮기는 훈련**이 목적이다(Park, 09-07) — 그림에서 식이 그대로 읽히면 실수가 준다.
새 상황 유형이 오면 먼저 "샤프로 3초에 그릴 수 있는 그림"을 정하고 그 도식을 렌더러에 추가한다(journey·passing·river·mountain·vessel 이 그 예).

`journey`·`passing`·`river`·`mountain` 은 상황 묘사라 **문항 본문에도** 쓸 수 있다(`bar`·`vessel`·`steps` 만 해설 전용).
문항 도형에도 쓰는 `numline` `scene` `polygon(diagonals:"fan")` `coordplane` `wire` 도 해설에서 그대로 쓸 수 있다.

### vessel — 액체는 용기에, 물은 파랑, 소금은 빨강 (Park, 09-07)

농도·물탱크·원기둥 물 채우기처럼 **액체가 등장하면 막대가 아니라 용기 모양**으로 그린다(컵, 하다못해 기다란 실린더).
물(액체)은 푸른색, 소금(용질)은 붉은색으로 바닥에 가라앉은 얇은 층. 용기는 모두 같은 크기이고 담긴 양이 많을수록 높이 차오른다
(`capacity` 로 가득 찬 양을 정할 수 있다 — 물탱크 600 L 에 450 L 처럼). 키는 `bar` 와 같다: `row:i` `total:i` `part:i-j` `part-lbl:i-j` + `vessel:i`.

### wire — 이름 붙은 입체 골격 (위치관계)

`{"fn": "wire", "args": {"kind": "box" | "triprism", "names": "ABCDEFGH"}}` — 꼭짓점 이름·모서리 전부를 한 번에 그린다
(뒤에 숨은 모서리는 점선). `box` 는 윗면 A B C D(앞왼→앞오→뒤오→뒤왼)·밑면 E F G H(A 아래가 E), `triprism` 은 윗면 A B C·밑면 D E F.
모서리 이름은 `AB BC CD DA EF FG GH HE AE BF CG DH` / `AB BC CA DE EF FD AD BE CF` 를 정규로 쓰되 애니메이션 키는 역순도 받는다.
관계(평행·만남·꼬인 위치·포함·수직)는 식으로 파생할 수 없으므로 **표(table)** 로 굽는다 — `tools/mkseed_position.py` 참고.
`polygon` 의 `"diagonals": "fan"` 은 한 꼭짓점에서 대각선을 모두 그어 삼각형 n−2개를 보여 준다.

## 식 문법

- 허용: `+ - * / % ()`, 비교·논리, 그리고 `abs min max sqrt gcd lcm floor ceil sign
  factorial binomial isprime sin cos tan log pi Rational` 와 파라미터·파생값 이름.
- **조사 함수**: `{n}{eul(n)}` → "3을/를", `eun` 은/는, `ika` 이/가, `ro` 로/으로, `wa` 와/과, `ida` 이다/다.
  숫자 읽기의 끝소리로 판정하므로 수치변주에서 조사가 어긋나지 않는다.
- `{식}`은 문항·해설에서 **표시형**으로(분수는 `[[frac(a,b)]]` 마커), 도형 인자에서는 **수치 그대로** 채워진다.
- **계수 표기**: `{co(k)}x` — k가 1이면 "x", -1이면 "-x", 그 밖이면 "3x". `{sgn(b)}` 는 "+ 3" / "- 3".
- `{dv(a, b)}` — "a ÷ b = q". 나누는 수가 1이면 "÷ 1" 없이 몫만 쓴다.
- 조사 함수는 **영문 이름**에도 맞는다: `{e}{wa(e)}` → "AB와" / "EF와" (엘·엠·엔·알만 받침으로 본다), 목록 "BC, DA"도 끝 이름 기준.
- `{{`, `}}` 는 중괄호 자체.

### 표 파생 (`table`) — 문자열 파라미터

```jsonc
"params": [{"name": "c", "values": {"in": ["AB|CG|0", "AB|CG|1", …]}}],
"table":  {"key": "c", "rows": {"AB|CG|0": {"e": "AB", "t": "CG", "skew": "CG, DH, EH, FG", "d1": "CD", …}, …}}
```
파라미터 값으로 행을 찾아 그 열들을 모두 env 에 붙인다(derive 앞). 이름·목록처럼 식으로 만들 수 없는 값에 쓴다.
`verify` 에는 `in`/`not` 을 쓸 수 있다: `"t in skew"`, `"not (t in par)"`. 표는 손으로 쓰지 말고 **생성 스크립트로 굽고**
`tools/recheck.py` 에 독립 재계산을 함께 넣는다.

### 분수 표기

렌더는 `renderHtml()`(mathir.js)로 — `[[frac(a,b)]]` 마커든 평문 `x/5`·`(30 − x)/6`·`17/2` 든 **상하(분자/분모)** 로 세운다.
`m/분`·`km/h` 같은 단위는 그대로 둔다. 시드에서 분수를 굳이 마커로 감쌀 필요는 없다.

## 규칙 (지키지 않으면 관문에서 떨어진다)

1. **정답은 반드시 다른 경로로 재현되어야 한다** — `relation` 또는 `verify` 없으면 G2 탈락.
2. **오답은 모두 오개념 코드를 달아야 한다** — `labels.MISCONCEPTIONS`에 등록된 코드만(자유 문자열 금지).
3. **오답 표기는 정답과 같은 꼴로** — `distractor_fmt`. 답만 π가 붙어 있으면 학생이 형식으로 찍는다.
4. **도형은 정규 인자만** — `figspec.py`의 v1.6 스키마. 문자열 숫자·한국어 kind 금지
   (단, 구하는 값을 그림에 문자로 둘 때는 `"r"` 같은 한 글자 변수 허용).
5. **그림이 답을 알려주면 안 된다** — 구하는 값은 그림에 숫자로 넣지 말고 문자로.
6. **문면에 수치를 넣는다** — DB의 `content_key`는 문면+보기만 보므로, 수치가 그림에만 있으면
   생성 문항이 전부 중복으로 병합된다(§ 마이그레이션 `2026-09_seed_items.sql`).
7. 기하 = 2단 해설(`sol3` 금지), 그 외 = 3단 해설(`sol3` 필수).
8. **채점기준과 모범답안이 반드시 있어야 한다** — 직접 쓰지 않으면 해설에서 자동 조립되지만,
   서술형으로 쓸 문항이라면 `rubric` 을 직접 쓰는 편이 낫다(배점과 부분점수를 통제할 수 있다).
   **배점은 5~8점**(Park, 09-07 확정 · 09-08 동아출판 통계로 보정): 핵심 채점 요소 2~4개에만 점수 — 2개 5점 · 3개 7점(**활용은 8점 = 식 세우기 3 | 해 구하기 3 | 답 구하기 2**) · 4개 8점, `rubric_total` 로 지정 가능 — 요소마다
   수행 수준(정확/부분/0)이 붙는다. **감점 요인은 일반 감점표가 아니라 그 틀의 실수거리**(`pitfalls`, 09-08): 빠지면 논리가 끊기는 진술,
   선후가 뒤바뀌기 쉬운 성질, 바꿔 쓰기 쉬운 두 값을 2~4개 적고 `on`(요소 이름 일부)·`effect`(부분|불인정)를 단다. 등록부는 `tools/pitfalls.py`.
   **빠지면 풀이 자체가 서지 않는 전제 진술**("구하는 수는 (a, b의 공배수)+1 꼴이다" 류)은 실수거리가 아니라 **요소**다 — pitfall 에 `"as_element": true`
   를 달면 `rubric.py` 가 첫 요소(최대 배점)로 승격한다(동아·교육청 관행). 공통 채점 원칙 5개는 자동으로 붙는다. 참고: `reference/gyeonggi/README.md` · `reference/donga/README.md`. `genkit/rubric.py` 가 옛 형식도 자동으로 v3 로 바꾼다
   (검토·답 제시 요소 제거 → 남은 요소 비례 배분).
9. **오답은 6~8개 준비한다.** 규칙 R-01(겉모양)·R-02(값 붕괴)·R-03(문면의 수)이 일부를 버린다.
10. 조건은 `constraints` 로 거르기 전에 `derive` 에서 **만족하는 꼴로 생성**한다 (LOCALGUIDE.md §3).

## 실행

```bash
python -m genkit.build seeds/m1-2-sector-arc.json --n 120        # 드라이런
python -m genkit.build seeds/*.json --n 120                       # 전부
node tools/review.mjs --per 4                                     # 눈검수 HTML
python -m genkit.build seeds/*.json --n 120 --push --status draft  # 승인 후 DB
```
