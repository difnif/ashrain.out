# mathir v1.6 — 도형 함수표 확장 (scene · quad · 해설 도식 · wire)

생성 문항이 쓰는 도형(scene·quad·journey·passing·river·mountain·bar·vessel·steps·wire)이 `mathir.FIGS`에 없다. `check_figure`가 "미지 도형 함수"로
떨어뜨리므로, 생성 문항을 앱에 넣기 전에 **파이썬·JS 양쪽에 같은 두 줄**을 넣어야 한다.
(파이썬과 JS는 항상 동형으로 유지 — mathir.js 머리말의 규약)

## 1) `itemfactory/mathir.py` — FIGS (55행 부근)

```diff
 FIGS = {  # figure DSL: 필수 인자 키 (존재 검사)
     "numline": ["min", "max"], "coordplane": ["x", "y"], "table": ["rows"],
     "hist": ["bins", "counts"], "stemleaf": ["stems"], "crossing": ["angles"],
     "parallel": ["angles"], "tri": ["v"], "rect": ["w", "h"], "polygon": ["n"],
+    "quad": ["v"], "scene": ["pts"],
+    "journey": ["stops"], "passing": ["obj", "span"], "bar": [], "vessel": [], "river": [], "mountain": [], "steps": ["lines"], "wire": ["kind"],
     "circle": ["r"], "sector": ["r", "angle"], "solid": ["kind"], "net": ["kind"],
```

## 2) `src/lib/mathir.js` — FIGS (33행 부근)

```diff
 export const FIGS = {
   numline:["min","max"], coordplane:["x","y"], table:["rows"], hist:["bins","counts"],
   stemleaf:["stems"], crossing:["angles"], parallel:["angles"], tri:["v"], rect:["w","h"],
-  polygon:["n"], circle:["r"], sector:["r","angle"], solid:["kind"], net:["kind"],
+  polygon:["n"], quad:["v"], scene:["pts"], circle:["r"], sector:["r","angle"],
+  solid:["kind"], net:["kind"],
+  journey:["stops"], passing:["obj","span"], bar:[], vessel:[], river:[], mountain:[], steps:["lines"], wire:["kind"],
```

## `scene`이 뭔가 — 생성 문항용 표준 기하 도형

기존 `tri`/`quad`/`polygon`은 "이름과 값"만 주고 배치는 렌더러가 짐작한다.
그래서 같은 인자로도 그림이 달라질 수 있고, 수치변주를 하면 그림이 조건과 어긋날 수 있다.
`scene`은 **점의 좌표를 직접 준다.** 수치변주에서 좌표만 다시 계산하면 그림이 항상 조건과 일치한다.

```jsonc
{"fn": "scene", "args": {
  "pts":  {"A": [0, 0], "B": [1, 0], "C": [0.55, 0.26]},
  "segs": [["A","B"], ["B","C"], ["A","C"], {"a":"C","b":"D","dash":true,"label":"8"}],
  "circles": [{"c": "A", "r": 1.2}],
  "marks": {
    "right": [["A","B","C"]],                                  // 꼭짓점 B에서의 직각
    "eq":    [[["A","D"],["B","C"]]],                          // 같은 길이 표시(묶음마다 빗금 수 증가)
    "arc":   [{"at":"A","from":"B","to":"C","label":"25°"}]     // 각 표시
  },
  "shade":  [["A","B","C"]],
  "labels": [{"at": "A", "text": "[[frac(1,2)]]", "dx": 6, "dy": -4}],
  "axes":   false
}}
```

- 좌표계는 수학 좌표(위가 +y). 화면 배치는 렌더러가 자동으로 맞춘다.
- `pts`의 키가 그대로 꼭짓점 이름이 되고, 라벨은 도형 바깥쪽으로 자동 배치된다.
- 필수 키는 `pts` 하나. 나머지는 모두 선택.

## 러너(전사) 쪽은 건드리지 않는다

`api/transcribeJob.js` 프롬프트는 v1.1 함수 목록 그대로 둔다.
`scene`은 **생성 전용**이고, 전사에서 나오면 안 된다(원본 이미지에 좌표가 없으므로).


## 해설 전용 도식 4종 (journey · passing · bar · steps)

문항 본문에는 쓰지 않고 **해설에서만** 쓰는 손그림 수준의 도식이다.
`genkit/figspec.py` 의 `SOLUTION_ONLY` 가 본문 사용을 막고, `mathir.FIGS` 에는 위처럼 등록만 해 둔다.

| fn | 무엇을 그리나 | 예 |
|---|---|---|
| `journey` | 지점 사이의 이동을 수직선으로 — 거리·속력·시간 | `{stops:["집","학교"], legs:[{label:"시속 4 km", sub:"2시간"}, {label:"올 때 시속 5 km", back:true}]}` |
| `passing` | 기차·터널 통과 — 둥근 직사각형(기차) + 두꺼운 선(다리) + 통과 거리 화살표 | `{obj:{label:"기차",len:"x m"}, span:{label:"다리",len:"300 m"}, total:"300 + x"}` |
| `bar` | 부분·전체 막대 — 농도·비율·개수 배분 | `{rows:[{name:"6 %", parts:[{label:"소금 6 g", value:6, fill:true},{label:"물 94 g", value:94}], total:"100 g"}]}` |
| `steps` | 식 변형 판서 (그림이 아니라 줄 맞춘 식) | `{lines:["2(300+x) = 700+x", "x = 100"]}` |

그리고 `polygon` 에 `"diagonals": "fan"` 을 주면 한 꼭짓점에서 대각선을 모두 그어
**삼각형 n−2개**를 보여 준다 — 다각형 내각의 합을 설명할 때 쓴다.


## `wire` — 이름 붙은 입체 골격 (2026-09-07 추가)

`{"fn":"wire","args":{"kind":"box"|"triprism","names":"ABCDEFGH"}}` — 위치관계(m1-2) 문항의 직육면체·삼각기둥.
꼭짓점 이름과 모서리를 전부 한 번에 그리고(숨은 모서리 점선), 애니메이션은 `edge:AB`·`face:ABCD` 키를 색으로 강조한다.
렌더러(figsvg.js fnWire)·스키마(figspec.py)·gates.FIGS_V16 에는 이미 들어 있으니 위 FIGS 두 줄만 맞추면 된다.
