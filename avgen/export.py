# 기본기 해설(초등 · 중등 · 고등 단원 100가지) → 앱 자료 src/features/display/basics/<단원>.js · index.js · thumbs.js
#   python3 export.py            모든 단원(생성기가 아직 없는 단원은 「아직」으로 건너뛴다)
#   python3 export.py e-add m-root   몇 단원만 다시(index.js 는 늘 전부 — 이미 만든 단원 파일은 그대로 둔다)
# 단원 = 100문항(1 ~ 5단계 20문항씩). 학년에 묶지 않고 학년을 넘나들며(span) 원리 → 확장으로 이어 간다.
import json, os, sys, secrets, importlib, re
sys.path.insert(0, os.path.dirname(__file__))
REPO = os.environ.get("ASHRAIN_REPO") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))      # 레포 뿌리(avgen/ 의 한 단계 위)
OUT_JS = f"{REPO}/src/features/display/basics"
CODES = os.path.join(os.path.dirname(__file__), "codes.json")
ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

LEVELS = [
    {"key": "e", "level": "초등", "frame": "basic-e", "icon": "🎒", "title": "초등 기본기 해설",
     "desc": "세로셈 · 분수 · 소수 · 도형 · 시각 · 단위 · 규칙 — 초1부터 초6까지 넘나드는 단원 중 하나를 골라 100문항씩 돌려요.",
     "thumb": ("e-circle", 70)},
    {"key": "m", "level": "중등", "frame": "basic-m", "icon": "📘", "title": "중등 기본기 해설",
     "desc": "수와 식 · 방정식 · 함수 · 도형 · 확률과 통계 — 중1부터 중3까지 단원을 골라 100문항씩 돌려요.",
     "thumb": ("m-pyth", 50)},
    {"key": "h", "level": "고등", "frame": "basic-h", "icon": "🎓", "title": "고등 기본기 해설",
     "desc": "다항식 · 방정식 · 도형의 방정식 · 지수로그 · 삼각 · 수열 · 미적분 · 확률 · 기하 — 단원을 골라 100문항씩 돌려요.",
     "thumb": ("h-diff", 70)},
]

# 단원 등록표 — (id, 학년 범위, 아이콘, "모듈:함수", 한 줄 설명). 차례가 곧 목록 차례(학교급 안에서).
# old: 학년별 해설(PR #62) 때의 세트 — 프린트 코드를 그대로 이어 쓴다.
REG = [
    # ───── 초등 ─────
    ("e-ten", "초1", "🔟", "g_e1:set_a", "10을 가르고 모아 10을 넘는 덧셈 · 뺄셈을 10 상자로", "e1/a", "e1-2:덧셈과 뺄셈"),
    ("e-hund", "초1", "💯", "g_e1:set_b", "십 모형과 낱개로 100까지 — 뛰어 세기 · 크기 비교 · 두 자리 덧셈 뺄셈", "e1/b", "e1-2:100까지의 수"),
    ("e-col", "초2", "🧮", "g_e2:set_a", "자리를 맞춰 쓰고 10이 되면 올리고, 모자라면 빌려 오는 세로셈", "e2/a", "e2-1:덧셈과 뺄셈"),
    ("e-add", "초3~초4", "➕", "g_ea:add", "세 자리 · 네 자리 덧셈 — 받아올림이 여러 번, 어림으로 확인", None, "e3-1:덧셈과 뺄셈"),
    ("e-sub", "초3~초4", "➖", "g_ea:sub", "세 자리 · 네 자리 뺄셈 — 0이 있는 자리에서 받아내림", None, "e3-1:덧셈과 뺄셈"),
    ("e-rel", "초1~초4", "🔁", "g_ea:rel", "덧셈 ↔ 뺄셈, 곱셈 ↔ 나눗셈 — 거꾸로 셈으로 □ 구하기", None, "e2-1:덧셈과 뺄셈"),
    ("e-word", "초1~초4", "📝", "g_ea:word", "합 · 차 · 몇 배 · 나누어 주기 — 문장을 식으로 옮기기", None, "e3-1:나눗셈"),
    ("e-big", "초2~초4", "🔢", "g_ea:big", "세 자리에서 조까지 — 자릿값 · 뛰어 세기 · 크기 비교", None, "e4-1:큰 수"),
    ("e-time", "초1~초3", "🕐", "g_ea:time", "시계 읽기에서 시간 계산까지 — 몇 시 몇 분, 걸린 시간", None, "e2-2:시각과 시간"),
    ("e-unit", "초2~초3", "📏", "g_ea:unit", "cm · m · km, mL · L, g · kg — 단위를 바꾸고 더하고 빼기", None, "e3-2:들이와 무게"),
    ("e-times", "초2", "✖️", "g_e2:set_b", "묶어 세기에서 곱셈구구로 — 점 배열로 보는 2단부터 9단까지", "e2/b", "e2-2:곱셈구구"),
    ("e-area3", "초3", "🟦", "g_e3:set_a", "자리마다 나누어 곱하는 넓이 모델 — (두 자리)×(두 자리)까지", "e3/a", "e3-2:곱셈"),
    ("e-mul", "초3~초4", "🧾", "g_eb:mul", "곱셈 세로셈 — 올림을 적으며 (세 자리)×(두 자리)까지", None, "e4-1:곱셈과 나눗셈"),
    ("e-div3", "초3", "➗", "g_e3:set_b", "곱셈을 거꾸로 — 몫과 나머지, 나머지를 생각하는 문장제", "e3/b", "e3-1:나눗셈"),
    ("e-div", "초3~초4", "📐", "g_eb:div", "나눗셈 세로셈 — 몫을 한 자리씩, 검산으로 확인", None, "e4-1:곱셈과 나눗셈"),
    ("e-mix", "초5", "🧩", "g_eb:mix", "덧셈 · 뺄셈 · 곱셈 · 나눗셈이 섞인 식 — 계산 순서와 괄호", None, "e5-1:자연수의 혼합 계산"),
    ("e-gcd", "초5", "🔗", "g_eb:gcd_set", "약수와 배수 — 최대공약수 · 최소공배수와 그 활용", None, "e5-1:약수와 배수"),
    ("e-fsize", "초3~초5", "🍕", "g_eb:fsize", "분수로 나타내기에서 크기 비교까지 — 단위분수 · 크기가 같은 분수", None, "e3-2:분수"),
    ("e-frac4", "초4", "🍰", "g_e4:set_a", "분모가 같은 분수의 덧셈 · 뺄셈 — 분수 막대로", "e4/a", "e4-2:분수의 덧셈과 뺄셈"),
    ("e-red", "초5", "✂️", "g_e5:set_a", "약분과 통분 — 분모가 다른 분수의 덧셈 · 뺄셈", "e5/a", "e5-1:약분과 통분"),
    ("e-fmul", "초5", "🍫", "g_eb:fmul", "분수의 곱셈 — 분자끼리 분모끼리, 약분은 먼저", None, "e5-2:분수의 곱셈"),
    ("e-fdiv", "초6", "🍩", "g_e6:set_a", "분수의 나눗셈 — 몇 번 들어가나에서 역수의 곱셈까지", "e6/a", "e6-1:분수의 나눗셈"),
    ("e-dec", "초3~초4", "🔸", "g_ec:dec", "소수의 자릿값 — 0.1, 0.01, 0.001과 크기 비교", None, "e3-1:분수와 소수"),
    ("e-dadd", "초4", "🔹", "g_ec:dadd", "소수의 덧셈 · 뺄셈 — 소수점을 맞추어 세로로", None, "e4-2:소수의 덧셈과 뺄셈"),
    ("e-dmul", "초5", "🔷", "g_ec:dmul", "소수의 곱셈 — 자연수처럼 곱하고 소수점 자리 세기", None, "e5-2:소수의 곱셈"),
    ("e-ddiv", "초6", "💠", "g_ec:ddiv", "소수의 나눗셈 — 소수점을 옮겨 자연수로 나누기", None, "e6-1:소수의 나눗셈"),
    ("e-fdec", "초4~초6", "🔄", "g_ec:fdec", "분수와 소수 — 서로 바꾸고 크기 비교하기", None, "e6-1:비와 비율"),
    ("e-angle", "초4", "📐", "g_e4:set_b", "직선 180°, 삼각형 180°, 사각형 360° — 각도의 합과 차", "e4/b", "e4-1:각도"),
    ("e-shape", "초3~초4", "🔺", "g_ec:shape", "삼각형과 사각형 — 이등변 · 정삼각형, 평행사변형 · 마름모의 성질", None, "e4-2:사각형"),
    ("e-poly5", "초5", "⬛", "g_e5:set_b", "다각형의 넓이 — 잘라 붙이고 두 배 하기", "e5/b", "e5-1:다각형의 둘레와 넓이"),
    ("e-circle", "초3~초6", "⚪", "g_ec:circle", "원 — 반지름 · 지름에서 원주와 원의 넓이까지", None, "e6-2:원의 넓이"),
    ("e-box", "초5~초6", "📦", "g_ed:box", "직육면체 — 면 · 모서리에서 겉넓이와 부피까지", None, "e6-1:직육면체의 부피와 겉넓이"),
    ("e-prism", "초6", "🔻", "g_ed:prism", "각기둥과 각뿔 — 면 · 모서리 · 꼭짓점의 수 규칙", None, "e6-1:각기둥과 각뿔"),
    ("e-rule", "초1~초5", "🧷", "g_ed:rule", "수의 배열 규칙에서 대응 관계식까지 — □와 △", None, "e5-1:규칙과 대응"),
    ("e-avg", "초4~초5", "📊", "g_ed:avg", "올림 · 버림 · 반올림과 평균 — 어림하고 고르게 하기", None, "e5-2:평균과 가능성"),
    ("e-ratio", "초6", "⚖️", "g_e6:set_b", "비와 비율 · 백분율 · 비례식과 비례배분", "e6/b", "e6-2:비례식과 비례배분"),
    # ───── 중등 ─────
    ("m-prime", "중1", "🔗", "g_ma:prime", "소인수분해 — 거듭제곱으로 최대공약수 · 최소공배수 · 약수의 개수", None, "m1-1:소인수분해"),
    ("m-int", "중1", "🧭", "g_m1:set_a", "정수와 유리수의 계산 — 수직선 위에서", "m1/a", "m1-1:정수와 유리수"),
    ("m-expr", "중1", "🔤", "g_ma:expr", "문자와 식 — 식의 값과 일차식의 계산", None, "m1-1:문자와 식"),
    ("m-eq1", "중1", "⚖️", "g_m1:set_b", "일차방정식 — 저울과 이항", "m1/b", "m1-1:문자와 식"),
    ("m-coord", "중1", "📍", "g_ma:coord", "좌표평면 — 사분면과 대칭인 점, 세 점으로 만든 넓이", None, "m1-1:좌표평면과 그래프"),
    ("m-prop", "중1", "📈", "g_ma:prop", "정비례와 반비례 — 표 · 식 · 그래프", None, "m1-1:좌표평면과 그래프"),
    ("m-angle", "중1", "📏", "g_ma:angle", "맞꼭지각과 평행선의 동위각 · 엇각", None, "m1-2:기본 도형과 작도"),
    ("m-pgon", "중1", "🔷", "g_ma:pgon", "다각형의 대각선 · 내각의 합 · 외각의 합", None, "m1-2:평면도형"),
    ("m-sector", "중1", "🍕", "g_mb:sector", "원과 부채꼴 — π로 쓰는 호의 길이와 넓이", None, "m1-2:평면도형"),
    ("m-solid", "중1", "🧊", "g_mb:solid", "기둥 · 뿔 · 구의 겉넓이와 부피", None, "m1-2:입체도형"),
    ("m-stat", "중1~중3", "📊", "g_mb:stat", "대푯값에서 산포도까지 — 평균 · 중앙값 · 최빈값 · 분산", None, "m1-2:자료의 정리와 해석"),
    ("m-rec", "중2", "🔁", "g_mb:rec", "유리수와 순환소수 — 순환마디와 분수로 바꾸기", None, "m2-1:수와 식의 계산"),
    ("m-exp", "중2", "🔺", "g_m2:set_a", "지수법칙과 단항식의 계산", "m2/a", "m2-1:수와 식의 계산"),
    ("m-calc", "중2", "🧮", "g_mb:calc", "다항식의 덧셈 · 뺄셈과 분배법칙", None, "m2-1:수와 식의 계산"),
    ("m-ineq", "중2", "↔️", "g_mb:ineq", "일차부등식 — 부등호 방향과 해의 범위", None, "m2-1:부등식과 연립방정식"),
    ("m-sys", "중2", "✖️", "g_m2:set_b", "연립일차방정식 — 가감법과 대입법", "m2/b", "m2-1:부등식과 연립방정식"),
    ("m-lin", "중2", "📉", "g_mc:lin", "일차함수 — 기울기 · 절편 · 두 점으로 식 세우기", None, "m2-1:일차함수"),
    ("m-iso", "중2", "🔺", "g_mc:iso", "이등변삼각형 · 외심 · 내심 — 각의 크기 구하기", None, "m2-2:도형의 성질"),
    ("m-quad", "중2", "▱", "g_mc:quad", "평행사변형과 여러 사각형의 성질", None, "m2-2:도형의 성질"),
    ("m-sim", "중2", "🔍", "g_mc:sim", "닮음 — 닮음비 · 평행선과 선분의 비 · 넓이의 비", None, "m2-2:도형의 닮음과 피타고라스 정리"),
    ("m-pyth", "중2~중3", "📐", "g_mc:pyth", "피타고라스 정리 — 세 변의 관계에서 거리까지", None, "m2-2:도형의 닮음과 피타고라스 정리"),
    ("m-count", "중2", "🎲", "g_mc:count", "경우의 수의 기초 — 합의 법칙 · 곱의 법칙 · 줄 세우기 · 뽑기", None, "m2-2:확률"),
    ("m-prob", "중2", "🎯", "g_mc:prob", "확률의 기초 — 여사건 · 두 사건이 함께 일어날 확률", None, "m2-2:확률"),
    ("m-root", "중3", "√", "g_md:root", "제곱근과 실수 — 근호의 계산과 분모의 유리화", None, "m3-1:제곱근과 실수"),
    ("m-expand", "중2~중3", "✳️", "g_md:expand", "곱셈 공식 — 전개하고 변형하기", None, "m3-1:다항식의 곱셈과 인수분해"),
    ("m-fact", "중3", "🧱", "g_m3:set_a", "인수분해 — 넓이 타일로 거꾸로 곱하기", "m3/a", "m3-1:다항식의 곱셈과 인수분해"),
    ("m-qeq", "중3", "🎯", "g_md:qeq", "이차방정식 — 인수분해 · 완전제곱식 · 근의 공식", None, "m3-1:이차방정식"),
    ("m-parab", "중3", "⌒", "g_m3:set_b", "이차함수 — 꼭짓점과 평행이동", "m3/b", "m3-1:이차함수"),
    ("m-trig", "중3", "📐", "g_md:trig", "삼각비 — 직각삼각형의 변의 비와 특수각", None, "m3-2:삼각비"),
    ("m-circ", "중3", "⭕", "g_md:circ", "원의 성질 — 원주각 · 중심각 · 접선", None, "m3-2:원의 성질"),
    # ───── 고등 ─────
    ("h-poly", "고1", "🧮", "g_ha:poly_", "다항식의 연산 — 곱셈 공식의 변형과 식의 값", None, "h1-1:다항식"),
    ("h-ident", "고1", "🟰", "g_ha:ident", "항등식과 미정계수 — 계수 비교 · 수치 대입", None, "h1-1:다항식"),
    ("h-rem", "고1", "➗", "g_h1:set_a", "나머지정리와 조립제법", "h1/a", "h1-1:다항식"),
    ("h-cplx", "고1", "🌀", "g_ha:cplx", "복소수 — i의 계산 · 켤레 · 거듭제곱", None, "h1-1:방정식과 부등식"),
    ("h-disc", "고1", "🔎", "g_h1:set_b", "이차방정식과 이차함수 — 판별식으로 읽기", "h1/b", "h1-1:방정식과 부등식"),
    ("h-qmax", "고1", "⛰️", "g_ha:qmax", "이차함수의 최대 · 최소 — 꼭짓점과 구간의 끝", None, "h1-1:방정식과 부등식"),
    ("h-eqs", "고1", "🧩", "g_ha:eqs", "삼차 · 사차방정식과 연립이차방정식", None, "h1-1:방정식과 부등식"),
    ("h-ineqs", "고1", "↔️", "g_ha:ineqs", "연립일차부등식 · 절댓값 부등식 · 연립이차부등식", None, "h1-1:방정식과 부등식"),
    ("h-perm", "고1", "🎲", "g_hb:perm", "순열과 조합 — _{n}P_{r}와 _{n}C_{r}", None, "h1-1:경우의 수"),
    ("h-matrix", "고1", "🔲", "g_hb:mat", "행렬 — 덧셈 · 실수배 · 곱셈", None, "h1-1:행렬"),
    ("h-line", "고1", "📏", "g_hb:line", "점과 직선 — 거리 · 내분점 · 직선의 방정식 · 점과 직선 사이의 거리", None, "h1-2:도형의 방정식"),
    ("h-circle", "고1", "⭕", "g_hb:circle", "원의 방정식 — 중심과 반지름, 원과 직선", None, "h1-2:도형의 방정식"),
    ("h-move", "고1", "↪️", "g_hb:move", "도형의 이동 — 평행이동과 대칭이동", None, "h1-2:도형의 방정식"),
    ("h-set", "고1", "🔵", "g_hb:set_", "집합과 명제 — 원소의 개수 · 연산 · 진리집합", None, "h1-2:집합과 명제"),
    ("h-func", "고1", "🔀", "g_hc:func", "합성함수의 값과 식 · 역함수 — 안쪽부터 계산하고, 거꾸로 되돌리기", None, "h1-2:함수"),
    ("h-ratf", "고1", "〰️", "g_hc:ratf", "유리함수의 점근선 · 무리함수의 정의역과 치역 — 기본형을 평행이동한 그래프", None, "h1-2:함수"),
    ("h-explog", "고2", "📈", "g_h2:set_a", "지수와 로그 — 정의에서 성질까지", "h2/a", "h2-1:지수함수와 로그함수"),
    ("h-expg", "고2", "📉", "g_hc:expg", "지수함수 · 로그함수의 그래프와 점근선 · 크기 비교 · 방정식과 부등식 · 최대최소", None, "h2-1:지수함수와 로그함수"),
    ("h-trig", "고2", "🌊", "g_hc:trig", "호도법 · 일반각의 삼각함수 값 · 삼각함수 사이의 관계 · 주기와 최대최소 · 삼각방정식", None, "h2-1:삼각함수"),
    ("h-law", "고2", "🔺", "g_hc:law", "사인법칙 · 외접원 · 코사인법칙으로 변과 각 · 두 변과 끼인각으로 넓이", None, "h2-1:삼각함수"),
    ("h-seq", "고2", "🪜", "g_hd:seq", "등차수열 · 등비수열의 일반항과 합 · 합으로 일반항 구하기 · 등차중항과 등비중항", None, "h2-1:수열"),
    ("h-sigma", "고2", "Σ", "g_hd:sigma", "Σ를 풀어 쓰기 · Σ의 성질 · 자연수 거듭제곱의 합 공식 · 부분분수로 합", None, "h2-1:수열"),
    ("h-lim", "고2", "🎯", "g_hd:lim", "그래프로 좌극한 · 우극한 · 0/0 꼴 · ∞/∞ 꼴 · 극한값으로 미정계수 · 함수의 연속", None, "h2-2:함수의 극한과 연속"),
    ("h-diff", "고2", "📉", "g_h2:set_b", "미분 — 접선의 기울기에서 극값까지", "h2/b", "h2-2:미분"),
    ("h-int", "고2", "∫", "g_hd:int_", "다항함수의 부정적분 · 정적분 계산과 성질 · 정적분으로 정의된 함수", None, "h2-2:적분"),
    ("h-iarea", "고2", "🟩", "g_hd:iarea", "곡선과 x축 · 두 곡선 사이의 넓이 · 속도로 위치와 움직인 거리", None, "h2-2:적분"),
    ("h-count", "고3", "🔢", "g_h3:set_a", "경우의 수 — 중복순열 · 원순열 · 중복조합 · 이항정리", "h3/a", "h3-2:경우의 수"),
    ("h-prob", "고3", "🎯", "g_he:prob", "덧셈정리 · 여사건(적어도) · 조건부확률 · 곱셈정리 · 독립시행의 확률", None, "h3-2:확률"),
    ("h-dist", "고3", "🔔", "g_he:dist", "확률분포와 기댓값 · 분산 · aX + b의 평균과 분산 · 이항분포 · 정규분포와 표준화", None, "h3-2:통계"),
    ("h-slim", "고3", "♾️", "g_he:slim", "∞/∞ · ∞ − ∞ 꼴의 극한 · 등비수열의 극한 · 부분분수 급수 · 등비급수", None, "h3-1:수열의 극한"),
    ("h-diff2", "고3", "🌀", "g_h3:set_b", "여러 가지 미분법 — 몫 · 합성 · 초월함수", "h3/b", "h3-1:미분법"),
    ("h-int2", "고3", "∬", "g_he:int2", "지수 · 로그 · 삼각함수의 정적분 · 치환적분 · 부분적분 · 구분구적법", None, "h3-1:적분법"),
    ("h-conic", "고3", "🥚", "g_he:conic", "포물선의 초점과 준선 · 타원과 쌍곡선의 초점 · 점근선 · 정의로 거리 구하기", None, "h3-3:이차곡선"),
    ("h-vec", "고3", "➡️", "g_he:vec", "벡터의 성분 계산 · 크기 · 성분과 각으로 내적 · 수직과 평행 조건", None, "h3-3:벡터"),
]
LV = {"e": "초등", "m": "중등", "h": "고등"}

def codes():
    return json.load(open(CODES)) if os.path.exists(CODES) else {}

def load(entry):
    sid, span, icon, src, desc, old, unit = entry
    mod, fn = src.split(":")
    try:
        m = importlib.import_module(mod)
    except ModuleNotFoundError:
        return None
    f = getattr(m, fn, None)
    return f() if f else None

def build(only=None):
    cj = codes()
    out = []
    ids = set()
    for e in REG:
        sid, span, icon, src, desc, old, unit = e
        assert sid not in ids, sid
        ids.add(sid)
        if only and sid not in only:
            continue
        S = load(e)
        if S is None:
            print(f"  아직 {sid} ({src})")
            continue
        assert len(S.items) == 100, (sid, len(S.items))
        for st in range(1, 6):
            assert sum(1 for it in S.items if it["st"] == st) == 20, (sid, st)
        if sid not in cj:
            cj[sid] = cj.get(old) if old and old in cj else "".join(secrets.choice(ALPHA) for _ in range(6))
        S.id, S.level, S.span, S.icon, S.desc, S.code, S.unit = sid, LV[sid[0]], span, icon, desc, cj[sid], unit
        out.append(S)
    json.dump(cj, open(CODES, "w"), indent=1)
    return out

def js_items(items):
    return "[\n" + ",\n".join("  " + json.dumps(it, ensure_ascii=False, separators=(",", ":")) for it in items) + ",\n]"

def write_set(S):
    os.makedirs(OUT_JS, exist_ok=True)
    body = f"""// ashrain.out — 기본기 해설 「{S.title}」({S.span}) 문항 ({S.id}.js) — 생성기가 만든 파일(손으로 고치지 말 것)
// 생성기: 프로젝트 문서 SRC-기본기해설-*.txt (avgen) · 검산: 판서의 「=」 계산을 문항마다 sympy 로 다시 계산 · tests/display-basics.test.mjs
// pp 문제지 한 쪽 문항 수 · note 지도 도움말(해설지 첫머리) · tips 단계마다 한 줄 요령(문제지 · 해설지 단계 머리)
// 한 문항: no · st 단계 · q 발문 · ans 답 · plan 방침 · lines 판서 [{{ pre?, s, memo? }}] · fig? 그림 DSL(frames/figdsl.jsx) · ap 빠른 정답 글자 · omr 칸 종류 · qf 1 이면 문제지에도 그림(문제 때 모습)
export const SET = {{ id: {json.dumps(S.id)}, pp: {S.pp}, note: {json.dumps(S.note, ensure_ascii=False)},
  tips: {json.dumps({str(k): v for k, v in S.tips.items()}, ensure_ascii=False)},
  items: {js_items(S.items)} }};
"""
    open(f"{OUT_JS}/{S.id}.js", "w").write(body)

def meta_of(S):
    return {"id": S.id, "level": S.level, "span": S.span, "unit": S.unit, "icon": S.icon, "title": S.title, "short": S.short, "desc": S.desc,
            "n": len(S.items), "code": S.code, "stages": {str(k): v for k, v in S.stages.items()}}

def write_index(built):
    """index.js 는 늘 등록표 전부 — 이번에 만들지 않은 단원은 이미 있는 파일의 머리 정보를 다시 읽어 쓴다(META 캐시)"""
    cache_p = os.path.join(os.path.dirname(__file__), "meta.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    for S in built:
        cache[S.id] = meta_of(S)
        th = cache.setdefault("_thumbs", {})
        for L in LEVELS:
            if L["thumb"][0] == S.id:
                th[L["frame"]] = S.items[L["thumb"][1] - 1]
    json.dump(cache, open(cache_p, "w"), ensure_ascii=False)
    metas = [cache[e[0]] for e in REG if e[0] in cache and os.path.exists(f"{OUT_JS}/{e[0]}.js")]
    ml = ",\n".join("  " + json.dumps(m, ensure_ascii=False, separators=(",", ":")) for m in metas)
    lv = ",\n".join("  " + json.dumps({k: v for k, v in L.items() if k != "thumb"}, ensure_ascii=False, separators=(",", ":")) for L in LEVELS)
    loads = ",\n".join(f'  {json.dumps(m["id"])}: () => import("./{m["id"]}.js")' for m in metas)
    src = f"""// ashrain.out — 기본기 해설 머리 정보 (basics/index.js) — 생성기가 만든 파일(손으로 고치지 말 것)
// 초등 · 중등 · 고등 학교급마다 액자 하나(frames/basics.jsx) · 단원 {len(metas)}가지(100문항, 1 ~ 5단계). 학년에 묶지 않고 학년을 넘나든다(span).
// id 는 학생앱 시청각 학습의 항목 key(#/av/<id>) · code 는 프린트 코드(문제지 · 해설지 · 빠른 정답 · OMR 오른쪽 위).
// 가벼운 머리 정보만 — 학생앱 목록(lib/av.js)이 바로 읽는다. 문항은 단원마다 늦게 들여온다(loadBasic). 목록 그림용 문항은 thumbs.js.
export const LEVELS = [
{lv}
];
export const BASICS = [
{ml}
];
export const basicOf = (id) => BASICS.find((b) => b.id === id) || null;
export const levelOf = (k) => LEVELS.find((l) => l.key === k || l.level === k || l.frame === k) || null;
export const basicsOf = (k) => {{ const L = levelOf(k); return L ? BASICS.filter((b) => b.level === L.level) : []; }};
const LOAD = {{
{loads},
}};
const done = new Map(), wait = new Map();
/** 단원 문항 들여오기 → {{ id, pp, note, tips, items }} */
export function loadBasic(id) {{
  if (!LOAD[id]) return Promise.reject(new Error(`없는 단원: ${{id}}`));
  if (!wait.has(id)) wait.set(id, LOAD[id]().then((m) => {{ done.set(id, m.SET); return m.SET; }}));
  return wait.get(id);
}}
export const basicCached = (id) => done.get(id) || null;
"""
    open(f"{OUT_JS}/index.js", "w").write(src)
    th = cache.get("_thumbs", {})
    tsrc = ("// ashrain.out — 기본기 해설 목록 그림용 한 문항씩 (basics/thumbs.js) — 생성기가 만든 파일(손으로 고치지 말 것)\n"
            "// 액자 목록(AdminDisplay 의 FrameGallery)에서만 읽는다 — 학생앱 첫 화면 꾸러미를 가볍게 두려고 index.js 와 나눴다.\n"
            "export const THUMBS = {\n" + "".join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False, separators=(',', ':'))},\n" for k, v in th.items()) + "};\n")
    open(f"{OUT_JS}/thumbs.js", "w").write(tsrc)
    return metas

if __name__ == "__main__":
    only = set(sys.argv[1:]) or None
    built = build(only)
    for S in built:
        write_set(S)
    metas = write_index(built)
    for S in built:
        print(f"  {S.id:10} {S.span:8} {len(S.items)} 검산 {S.checks:4} {S.code} {S.short}")
    by = {}
    for m in metas:
        by[m["level"]] = by.get(m["level"], 0) + 1
    print(f"단원 {len(metas)}가지 / 등록표 {len(REG)} — " + " · ".join(f"{k} {v}" for k, v in by.items()))
