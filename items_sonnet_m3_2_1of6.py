# -*- coding: utf-8 -*-
# esc_sonnet_m3-2_1of6 — 이미지 기준 전사 (80 항목 / 80쪽)
# 특수한 각의 삼각비 · 예각의 삼각비의 값 · 삼각비의 활용(2) 넓이 · 삼각비
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

# ======================= 특수한 각의 삼각비 =======================
# p1 직각이등변삼각형 sinA×cosB
add(id="4177a680", qtype="choice",
    question=("다음 그림과 같이 [[seg(AC) = seg(BC)]]인 직각이등변삼각형 ABC에서 [[sin(A) × cos(B)]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(sqrt(3),3)]]", "[[frac(sqrt(2),2)]]", "[[1]]", "[[sqrt(2)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: A 위, C 좌하(직각 표시), B 우하. AC와 CB에 같은 길이 표시(=)"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각이등변삼각형 도형",
    note="A=B=45° → (√2/2)(√2/2)=1/2 → ① (빠른정답 없음, 풀이 답).")

# p3 sin²60°+cos²60°
add(id="07b9e802", qtype="short",
    question="[[pow(sin(deg(60)),2) + pow(cos(deg(60)),2)]]의 값을 구하시오.",
    choices=None, derived_answer="1", figure=None, difficulty_est=1, confidence=0.9,
    note="3/4+1/4=1 (빠른정답 없음, 풀이 답).")

# p19 cos x = √3/2
add(id="800f6cd6", qtype="short",
    question="[[deg(0) < x < deg(90)]]일 때, [[cos(x) = frac(sqrt(3),2)]]을 만족시키는 [[x]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(30)", figure=None, difficulty_est=1, confidence=0.9,
    note="cos30°=√3/2 → x=30°. 빠른정답 deg(45)와 불일치(이미지는 cos x=√3/2).")

# p20 ∠B=90°, AB=6√3, AC=12 → ∠A
add(id="3d809714", qtype="short",
    question=("다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 6 sqrt(3)]], [[seg(AC) = 12]]일 때, "
              "[[angle(A)]]의 크기를 구하시오."),
    choices=None, derived_answer="deg(30)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC: A 위, B 좌하(직각 표시), C 우하. AB=6√3, AC=12(점선 치수), A에 각 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="cos A=6√3/12=√3/2 → 30° = 빠른정답 ✓.")

# p28 cos(2x−20°)=√3/2
add(id="0fa95f82", qtype="short",
    question=("[[cos(2x - deg(20)) = frac(sqrt(3),2)]]을 만족시키는 [[angle(x)]]의 크기를 구하시오. "
              "(단, [[deg(10) < x < deg(45)]])"),
    choices=None, derived_answer="deg(25)", figure=None, difficulty_est=2, confidence=0.9,
    note="2x−20°=30° → x=25°. 빠른정답 5와 불일치.")

# p33 반원, AB⊥CD, ∠AOC=135°, AO=16
add(id="54e4e83c", qtype="choice",
    question=("다음 그림에서 [[seg(AB)]]는 반원 O의 지름이고 [[perp(seg(AB), seg(CD))]]이다. "
              "[[angle(AOC) = deg(135)]], [[seg(AO) = 16]]일 때, [[seg(CD)]]의 길이는?"),
    choices=["[[frac(16,3) sqrt(2)]]", "[[frac(16,3) sqrt(3)]]", "[[8]]", "[[8 sqrt(2)]]", "[[8 sqrt(3)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "반원(지름 AB, 중심 O): A 좌, O 중앙, D·B 우측. 점 C 호 위(우상), 선분 AC·OC·CD(CD⊥AB, D에 직각 표시). ∠AOC=135° 표시, AO=16(점선 치수)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 반원+삼각형 도형",
    note="∠COD=45°, OC=16 → CD=16 sin45°=8√2 → ④. 빠른정답 45와 불일치.")

# p41 □DEFB 직사각형, ∠CAB=30°, BC=12, AF=BF → CE
add(id="f0ef7f1d", qtype="choice",
    question=("다음 그림에서 [[quad(DEFB)]]는 직사각형이고 [[angle(CAB) = deg(30)]], [[angle(ABC) = deg(90)]]이다. "
              "[[seg(BC) = 12]], [[seg(AF) = seg(BF)]]일 때, [[seg(CE)]]의 길이는?"),
    choices=["[[6 sqrt(2) + 6 sqrt(3)]]", "[[6 sqrt(3) + 12]]", "[[6 sqrt(2) + 6 sqrt(6)]]",
             "[[6 sqrt(3) + 6 sqrt(6)]]", "[[6 sqrt(6) + 12]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 좌하, B 우, C 위, ∠B 직각 표시, ∠A=30° 표시, BC=12 점선 치수). 직사각형 DEFB(D는 CE 위, E·F는 AF 위, F에 직각 표시). AB와 CE의 교점 G(직각 표시). AE=EF 같은 길이 표시, BF 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+직사각형 복합 도형",
    note="AB=12√3, AF=BF=6√6, CE=BF+BC sin45°=6√6+6√2 → ③ = 빠른정답 ✓.")

# p46 사면체 AB:AC=3:2, sin x
add(id="f50c3fff", qtype="choice",
    question=("다음 그림과 같이 [[ratio(seg(AB), seg(AC)) = ratio(3, 2)]]인 사면체가 있다. "
              "[[angle(ADB) = angle(ADC) = deg(90)]]이고 [[angle(ABD) = x]], [[angle(ACD) = deg(60)]]일 때, [[sin(x)]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(sqrt(3),3)]]", "[[frac(2,3)]]", "[[frac(sqrt(3),2)]]", "[[frac(3 sqrt(3),4)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "사면체 A(위)-B(좌하)-C(우)-D(안쪽, 점선). AD⊥BD·CD(D에 직각 표시), ∠ABD=x, ∠ACD=60° 표시, 면 색칠(보라)"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사면체 입체 도형",
    note="AD=AC·√3/2, sin x=AD/AB=(√3/2)(2/3)=√3/3 → ②. 빠른정답 10과 불일치.")

# p47 정사면체(모서리 4) ∠OCH=x, tan x
add(id="f7c6dd90", qtype="choice",
    question=("다음 그림과 같이 모서리의 길이가 4인 정사면체의 한 꼭짓점 O에서 밑면에 내린 수선의 발을 H라 하고, "
              "[[seg(AB)]]의 중점을 M이라 하자. [[angle(OCH) = x]]라 할 때, [[tan(x)]]의 값은?"),
    choices=["[[sqrt(2)]]", "[[2 sqrt(2)]]", "[[3 sqrt(2)]]", "[[sqrt(3)]]", "[[3 sqrt(3)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 O(위)-A(좌)-B(아래)-C(우). OH 수선(H 밑면 위, 직각 표시), CM(M은 AB 중점), OA=OC=4 점선 치수, ∠OCH=x 표시, 면 색칠(하늘)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="CH=4√3/3, OH=4√6/3 → tan x=√2 → ① = 빠른정답 ✓.")

# p48 정사면체(4) ∠AED=x, cos x
add(id="2079c9df", qtype="choice",
    question=("다음 그림과 같이 한 모서리의 길이가 4인 정사면체 A-BCD에서 [[seg(BC)]]의 중점을 E라 하자. "
              "[[angle(AED) = x]]일 때, [[cos(x)]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(2,3)]]", "[[frac(1,8)]]", "[[frac(1,16)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 A(위)-B(좌)-C(아래)-D(우). E는 BC 중점, 선분 AE·DE, AB=4 점선 치수, ∠AED=x 표시, 면 색칠(청회색)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="AE=DE=2√3, AD=4 → cos x=(12+12−16)/24=1/3 → ②. 빠른정답 3과 불일치.")

# p50 정사면체(2) ∠AED=x, cos x
add(id="517954a9", qtype="choice",
    question=("다음 그림과 같이 한 변의 길이가 2인 정사면체 A-BCD에서 [[seg(BC)]]의 중점을 E라 하고, "
              "[[angle(AED) = x]]일 때, [[cos(x)]]의 값은?"),
    choices=["[[frac(1,2)]]", "[[frac(1,3)]]", "[[frac(1,4)]]", "[[frac(1,5)]]", "[[frac(1,6)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 A(위)-B(좌)-C(아래)-D(우). E는 BC 중점(BE=EC 같은 길이 표시), 선분 AE·DE, AB=2 점선 치수, ∠AED=x 표시, 면 색칠(베이지)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="AE=DE=√3, AD=2 → cos x=(3+3−4)/6=1/3 → ②. 빠른정답 1과 불일치.")

# p52 정사면체 ∠ABH=x, tan x
add(id="5cb148e6", qtype="choice",
    question=("다음 그림과 같이 정사면체의 점 A에서 밑면에 내린 수선의 발을 H라 하고 [[angle(ABH) = x]]라 할 때, "
              "[[tan(x)]]의 값은?"),
    choices=["[[sqrt(2)]]", "[[sqrt(3)]]", "[[3]]", "[[2 sqrt(3)]]", "[[2 sqrt(6)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 A(위)-B(좌)-C(아래)-D(우, 점선). AH 수선(H 밑면 위, 직각 표시), BH 선분, ∠ABH=x 표시, 면 색칠(청록)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="모서리 a: BH=a/√3, AH=a√(2/3) → tan x=√2 → ① = 빠른정답 ✓.")

# p53 정사면체 ∠AMD=a, cos a
add(id="4839e255", qtype="short",
    question=("정사면체 A-BCD에서 변 BC의 중점을 M이라 하고, [[perp(seg(AM), seg(BC))]], [[perp(seg(DM), seg(BC))]], "
              "[[angle(AMD) = a]]일 때, [[cos(a)]]를 구하시오."),
    choices=None, derived_answer="frac(1,3)",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 A(위)-B(좌)-C(아래)-D(우). M은 BC 중점, 선분 AM·DM(점선), M에 직각 표시 2개, ∠AMD=a 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="AM=DM=(√3/2)a, AD=a → cos a=1/3 = 빠른정답 ✓.")

# p54 직육면체 EF=8, ∠AFE=60°, ∠CFG=45°, cos(x/2)
add(id="76b02394", qtype="choice",
    question=("다음 그림과 같은 직육면체에서 [[seg(EF) = 8]], [[angle(AFE) = deg(60)]], [[angle(CFG) = deg(45)]]이다. "
              "[[angle(CAF) = x]]라 할 때, [[cos(frac(x,2))]]의 값은?"),
    choices=["[[frac(sqrt(10),16)]]", "[[frac(sqrt(10),8)]]", "[[frac(3 sqrt(10),16)]]", "[[frac(sqrt(10),4)]]", "[[frac(5 sqrt(10),16)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직육면체 ABCD-EFGH(A 좌상 앞, B 앞, C 우, D 뒤; E 좌하, F 앞아래, G 우하, H 뒤 점선). 선분 AF·FC·AC로 삼각형 AFC. EF=8, ∠AFE=60°, ∠CFG=45°, ∠CAF=x 표시, 면 색칠(분홍)"}}],
    difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 직육면체 입체 도형",
    note="AE=CG=FG=8√3, AF=AC=16, FC=8√6 → cos x=1/4 → cos(x/2)=√10/4 → ④ = 빠른정답 ✓.")

# p55 정사면체(4) BM=CM, ∠AMD=x, sin x+tan x
add(id="bfaf4c5f", qtype="choice",
    question=("다음 그림과 같이 한 모서리 길이가 4인 정사면체에서 [[seg(BM) = seg(CM)]]이고 [[angle(AMD) = x]]일 때, "
              "[[sin(x) + tan(x)]]의 값은?"),
    choices=["[[frac(7 sqrt(2),3)]]", "[[frac(8 sqrt(2),3)]]", "[[3 sqrt(2)]]", "[[frac(10 sqrt(2),3)]]", "[[frac(11 sqrt(2),3)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "정사면체 A(위)-B(좌)-C(아래)-D(우). M은 BC 중점(BM=MC 같은 길이 표시), 선분 AM·DM, AB=4 점선 치수, ∠AMD=x 표시, 면 색칠(분홍)"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 정사면체 입체 도형",
    note="cos x=1/3, sin x=2√2/3, tan x=2√2 → 합 8√2/3 → ② = 빠른정답 ✓.")

# p58 AC=8, tan15°
add(id="f0e4cdd5", qtype="choice",
    question="다음 그림에서 [[seg(AC) = 8]]일 때, [[tan(deg(15))]]의 값은?",
    choices=["[[2 - sqrt(2)]]", "[[2 + sqrt(2)]]", "[[2 + sqrt(3)]]", "[[2 - sqrt(3)]]", "[[2 + 2 sqrt(3)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(B 좌, C 우하 직각 표시, A 우상). BC 위의 점 D, 선분 AD. ∠B=15°, ∠ADC=30° 표시, AC=8 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="DC=8√3, AD=BD=16 → tan15°=8/(16+8√3)=2−√3 → ④ = 빠른정답 ✓.")

# p60 직사각형 ABCD, △DEF, DF=2√3, ∠EDF=30°, ∠BFE=45° → cos15°
add(id="4343e077", qtype="choice",
    question=("다음 그림과 같은 직사각형 ABCD의 두 변 AB, BC 위의 점 E, F에 대하여 [[tri(DEF)]]가 [[angle(F) = deg(90)]]인 "
              "직각삼각형이고 [[seg(DF) = 2 sqrt(3)]], [[angle(EDF) = deg(30)]], [[angle(BFE) = deg(45)]]일 때, "
              "[[cos(deg(15))]]의 값은?"),
    choices=["[[frac(sqrt(2) + sqrt(6), 8)]]", "[[frac(3 sqrt(2), 8)]]", "[[frac(sqrt(2) + sqrt(6), 4)]]",
             "[[frac(sqrt(2) + sqrt(7), 4)]]", "[[frac(sqrt(2) + 3, 4)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). E는 AB 위, F는 BC 위. 삼각형 DEF(F에 직각 표시). ∠EDF=30°, ∠BFE=45° 표시, DF=2√3 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+삼각형 복합 도형",
    note="EF=2, DE=4, BF=√2, FC=√6, AD=√2+√6, ∠ADE=15° → cos15°=AD/DE=(√2+√6)/4 → ③ = 빠른정답 ✓.")

# p62 같은 구조, DF=6√3, ∠BEF=45°
add(id="a3daec78", qtype="choice",
    question=("다음 그림과 같은 직사각형 ABCD의 두 변 AB, BC 위의 점 E, F에 대하여 [[tri(DEF)]]가 [[angle(F) = deg(90)]]인 "
              "직각삼각형이고 [[seg(DF) = 6 sqrt(3)]], [[angle(EDF) = deg(30)]], [[angle(BEF) = deg(45)]]일 때, "
              "[[cos(deg(15))]]의 값은?"),
    choices=["[[frac(-sqrt(2) + sqrt(6), 4)]]", "[[frac(-sqrt(2) + sqrt(10), 4)]]", "[[frac(sqrt(2) + 2, 4)]]",
             "[[frac(sqrt(2) + sqrt(6), 4)]]", "[[frac(sqrt(3) + sqrt(6), 4)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). E는 AB 위, F는 BC 위. 삼각형 DEF(F에 직각 표시). ∠EDF=30°, ∠BEF=45° 표시, DF=6√3 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 직사각형+삼각형 복합 도형",
    note="EF=6, DE=12, BF=3√2, FC=3√6, AD=3√2+3√6 → cos15°=(√2+√6)/4 → ④ = 빠른정답 ✓.")

# p72 ∠BAE=30°, BE=8, AD=DE, ∠AEB=90°, □CDEF 직사각형 → cos75°
add(id="772da7e1", qtype="choice",
    question=("다음 그림에서 [[angle(BAE) = deg(30)]], [[seg(BE) = 8]], [[seg(AD) = seg(DE)]], [[angle(AEB) = deg(90)]]이고 "
              "[[quad(CDEF)]]는 직사각형일 때, [[cos(deg(75))]]의 값은?"),
    choices=["[[frac(sqrt(6) - sqrt(2), 16)]]", "[[frac(sqrt(6) - sqrt(2), 8)]]", "[[frac(sqrt(6) - sqrt(2), 4)]]",
             "[[frac(sqrt(6) - sqrt(2), 2)]]", "[[sqrt(6) - sqrt(2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "A 좌하, B 위, E 우(∠AEB 직각 표시), D 우하(직각 표시). 직사각형 CDEF(C는 AD 위, F는 BC 위). 선분 BC(세로)와 AE의 교점 G. ∠BAE=30° 표시, BE=8 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+직사각형 복합 도형",
    note="AB=16, AE=8√3, AD=DE=4√6, ∠BAD=75°, AC=4√6−4√2 → cos75°=AC/AB=(√6−√2)/4 → ③ = 빠른정답 ✓.")

# p82 두 직선 기울기 1, √3/3 → ∠a
add(id="012e720c", qtype="short",
    question="다음 그림과 같은 두 직선 [[l]], [[m]]의 기울기가 각각 [[1]], [[frac(sqrt(3),3)]]일 때, [[angle(a)]]의 크기를 구하시오.",
    choices=None, derived_answer="deg(15)",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면(원점 O): 두 직선 l(가파름, 원점 근처 통과)·m(완만)이 제1사분면에서 만남. 교점에서 두 직선 사이 각 a 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 위 두 직선 도형",
    note="l: 45°, m: 30° → a=15°. 빠른정답 1과 불일치.")

# p86 반원 OC=6, ∠AOC=45°, ∠ACB=90° → tan x
add(id="2bdff36e", qtype="choice",
    question=("다음 그림과 같은 반원 O에서 [[seg(OC) = 6]], [[angle(AOC) = deg(45)]], [[angle(ACB) = deg(90)]]일 때, "
              "[[tan(x)]]의 값은?"),
    choices=["[[frac(sqrt(2) - 1, 6)]]", "[[frac(sqrt(2) - 1, 2)]]", "[[sqrt(2) - 1]]", "[[2 sqrt(2) - 2]]", "[[6 sqrt(2) - 6]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "반원(중심 O, 지름 좌측 끝 B). 호 위의 점 A(우상), C는 지름 위(A의 수선 발, 직각 표시). 선분 BA·OA·AC. ∠ABC=x, ∠AOC=45° 표시, OC=6 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 반원+삼각형 도형",
    note="AC=6, OA=OB=6√2 → tan x=6/(6√2+6)=√2−1 → ③. 빠른정답 4와 불일치.")

# p87 ∠B=90°, ∠A=30°, AC=8cm 넓이
add(id="0162b4e4", qtype="choice",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC의 넓이는?",
    choices=["[[8]] cm²", "[[12]] cm²", "[[8 sqrt(3)]] cm²", "[[12 sqrt(2)]] cm²", "[[12 sqrt(3)]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 좌하 직각 표시, C 우하), 색칠(분홍). ∠A=30° 표시, AC=8cm 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="BC=4, AB=4√3 → 8√3 → ③ = 빠른정답 ✓.")

# p89 ∠B=90°, ∠A=60°, AC=20cm 넓이
add(id="489e4171", qtype="choice",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AC) = 20]] cm일 때, 직각삼각형 ABC의 넓이는?",
    choices=["[[50]] cm²", "[[50 sqrt(2)]] cm²", "[[50 sqrt(3)]] cm²", "[[90]] cm²", "[[100]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 좌상, B 좌하 직각 표시, C 우하), 색칠(분홍). ∠A=60° 표시, AC=20cm 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="AB=10, BC=10√3 → 50√3 → ③ = 빠른정답 ✓.")

# p92 AH=8, ∠B=30°, ∠ACH=60° → △ABC 넓이
add(id="856d7952", qtype="choice",
    question="다음 그림에서 [[seg(AH) = 8]], [[angle(B) = deg(30)]], [[angle(ACH) = deg(60)]]일 때, [[tri(ABC)]]의 넓이는?",
    choices=["[[frac(40 sqrt(2), 3)]]", "[[16 sqrt(2)]]", "[[frac(56 sqrt(3), 3)]]", "[[frac(64 sqrt(3), 3)]]", "[[24 sqrt(3)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 우상) 색칠(분홍). H는 BC 연장선 위(A의 수선 발, 직각 표시). ∠B=30°, ∠ACH=60° 표시, AH=8 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형",
    note="BH=8√3, CH=8√3/3, BC=16√3/3 → 넓이 64√3/3 → ④. 빠른정답 3과 불일치.")

# p93 AH=12, ∠B=30°, ∠ACH=60°
add(id="eeba5db3", qtype="choice",
    question="다음 그림에서 [[seg(AH) = 12]], [[angle(B) = deg(30)]], [[angle(ACH) = deg(60)]]일 때, [[tri(ABC)]]의 넓이는?",
    choices=["[[40 sqrt(3)]]", "[[48 sqrt(3)]]", "[[56 sqrt(3)]]", "[[64 sqrt(3)]]", "[[72 sqrt(3)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 우상) 색칠(하늘). H는 BC 연장선 위(A의 수선 발, 직각 표시). ∠B=30°, ∠ACH=60° 표시, AH=12 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+수선 도형",
    note="BH=12√3, CH=4√3, BC=8√3 → 넓이 48√3 → ②. 빠른정답 4와 불일치.")

# p97 직사각형 회전 30°, 겹치는 부분 넓이
add(id="d20c03aa", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 9]], [[seg(BC) = 12]]인 직사각형 ABCD를 점 A를 중심으로 [[deg(30)]]만큼 회전시켜 "
              "직사각형 AEFG를 만들었다. 두 직사각형이 겹쳐지는 부분인 색칠한 사각형의 넓이는?"),
    choices=["[[34 sqrt(3)]]", "[[frac(69 sqrt(3), 2)]]", "[[35 sqrt(3)]]", "[[frac(71 sqrt(3), 2)]]", "[[36 sqrt(3)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직사각형 ABCD(A 좌하, B 우하, C 우상, D 좌상)와 A를 중심으로 30° 회전한 직사각형 AEFG(E 우, F 위, G 좌). 겹치는 사각형(A·E·DC와 EF의 교점·D) 색칠(하늘). ∠BAE=30° 표시, AB=9, BC=12 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 두 직사각형 회전 겹침 도형",
    note="A(0,0),E(9√3/2,9/2),P(2√3,12),D(0,12) 신발끈 → 69√3/2 → ② = 빠른정답 ✓.")

# ======================= 예각의 삼각비의 값 =======================
# p1 사분원 DA
add(id="311c643e", qtype="choice",
    question="아래 그림과 같이 반지름의 길이가 1인 사분원에서 다음 중 [[seg(DA)]]의 길이와 그 값이 항상 같은 것은?",
    choices=["[[sin(x)]]", "[[cos(x)]]", "[[tan(x)]]", "[[frac(1, sin(x))]]", "[[frac(1, cos(x))]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "사분원(중심 O, 반지름 1, E 위·B 우). 호 위의 점 D, OD=1(점선), D에서 OB에 내린 수선의 발 A(직각 표시). B에서 세운 수선과 OD 연장선의 교점 C(B에 직각 표시). ∠DOA=x 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 사분원 도형",
    note="DA=OD sin x=sin x → ① = 빠른정답 ✓.")

# p6 사분원 cos47°
add(id="98c54a4d", qtype="short",
    question="다음 그림은 반지름의 길이가 1인 사분원을 좌표평면 위에 나타낸 것이다. [[cos(deg(47))]]의 값을 구하시오.",
    choices=None, derived_answer="0.68",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(반지름 1). 원점에서 47° 방향 반직선이 호와 만나는 점 (0.68, 0.73)(점선 표시), x=1에서 세운 수선과 만나는 점 (1, 1.07). 직각 표시 2개"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos47°=0.68(x좌표). 빠른정답 5와 불일치.")

# p9 사분원 cos43°
add(id="58d8e7cb", qtype="short",
    question="다음 그림은 반지름의 길이가 1인 사분원을 좌표평면 위에 나타낸 것이다. [[cos(deg(43))]]의 값을 구하시오.",
    choices=None, derived_answer="0.73",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(반지름 1). 원점에서 47° 방향 반직선이 호와 만나는 점 (0.68, 0.73)(점선 표시), x=1에서 세운 수선과 만나는 점 (1, 1.07). 직각 표시 2개"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos43°=sin47°=0.73. 빠른정답 0.68과 불일치.")

# p10 사분원 cos42°
add(id="89dea5d6", qtype="short",
    question="다음 그림은 반지름의 길이가 1인 사분원을 좌표평면 위에 나타낸 것이다. [[cos(deg(42))]]의 값을 구하시오.",
    choices=None, derived_answer="0.743",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(반지름 1). 원점에서 48° 방향 반직선이 호와 만나는 점 (0.669, 0.743)(점선 표시), x=1에서 세운 수선과 만나는 점 (1, 1.111). 직각 표시 2개"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos42°=sin48°=0.743 = 빠른정답 ✓.")

# p13 접선 AT, BH⊥OA, TA/BH (정답 2개)
add(id="6c8b9f61", qtype="choice",
    question=("다음 그림에서 직선 AT는 반지름의 길이가 1인 원 O 위의 한 점 A에서의 접선이고, [[perp(seg(BH), seg(OA))]]이다. "
              "[[angle(BOA) = x]]라 할 때, [[frac(seg(TA), seg(BH))]]의 값과 같은 것을 모두 고르면? (정답 2개)"),
    choices=["[[1 + tan(x)]]", "[[frac(1, cos(x))]]", "[[frac(sin(x), tan(x))]]", "[[frac(cos(x), sin(x))]]", "[[frac(tan(x), sin(x))]]"],
    derived_answer="②, ⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "O 좌하, A 우하, T 우상(접선 AT 세로, A에 직각 표시). 호 위의 점 B(OB=1 점선), B에서 OA에 내린 수선의 발 H(직각 표시). ∠BOA=x 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원 접선+사분원 도형",
    note="TA=tan x, BH=sin x → tan x/sin x=1/cos x → ②, ⑤. 빠른정답 0.743과 불일치.")

# p14 사분원 sin x 선분
add(id="19545853", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 1인 사분원에서 [[sin(x)]]를 나타내는 선분은?",
    choices=["[[seg(OB)]]", "[[seg(OC)]]", "[[seg(OD)]]", "[[seg(CD)]]", "[[seg(BE)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "사분원(중심 O, A 위, B 우, 반지름 1 점선 치수 2개). 호 위의 점 C, C에서 OB에 내린 수선의 발 D(직각 표시), B에서 세운 수선과 OC 연장선의 교점 E(B에 직각 표시). ∠COD=x 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 사분원 도형",
    note="OC=1 → CD=sin x → ④. 빠른정답 '1, 3'과 불일치.")

# p16 cos0°×sin90°+sin60°×tan30°
add(id="79798a9f", qtype="choice",
    question="[[cos(deg(0)) × sin(deg(90)) + sin(deg(60)) × tan(deg(30))]]의 값은?",
    choices=["[[1]]", "[[frac(3,2)]]", "[[2]]", "[[frac(4 sqrt(3), 3)]]", "[[2 + 3 sqrt(2)]]"],
    derived_answer="②", figure=None, difficulty_est=1, confidence=0.9,
    note="1·1+(√3/2)(√3/3)=3/2 → ②. 빠른정답 '2, 5'와 불일치.")

# p17 옳지 않은 것 2개
add(id="8e322044", qtype="choice",
    question="다음 중에서 옳지 않은 것을 모두 고르면? (정답 2개)",
    choices=["[[sin(deg(0)) = 0]], [[sin(deg(90)) = 1]]", "[[cos(deg(0)) = 0]], [[cos(deg(90)) = 1]]",
             "[[sin(deg(30)) + cos(deg(30)) = frac(1,2)]]", "[[tan(deg(30)) × tan(deg(60)) = 1]]",
             "[[tan(deg(60)) = 2 sin(deg(60))]]"],
    derived_answer="②, ③", figure=None, difficulty_est=1, confidence=0.9,
    note="cos0°=1, cos90°=0 ②✗; sin30°+cos30°=(1+√3)/2 ③✗ → ②, ③ = 빠른정답 ✓.")

# p42 사분원 옳지 않은 것 (θ)
add(id="f359116b", qtype="choice",
    question="다음 그림과 같이 반지름의 길이가 1인 사분원이 있다. 다음 중 옳지 않은 것은? (단, [[theta]]는 예각)",
    choices=["[[sin(theta) = seg(BC)]]", "[[cos(theta) = seg(AB)]]", "[[tan(theta) = seg(DE)]]",
             "[[sin(theta) < tan(theta)]]", "[[sin(theta) = cos(theta)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "사분원(중심 A 좌하, D 우, 반지름 1 점선 치수). 호 위의 점 C, C에서 AD에 내린 수선의 발 B(직각 표시), D에서 세운 수선과 AC 연장선의 교점 E(D에 직각 표시). ∠CAB=θ 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 사분원 도형",
    note="①②③④ 성립, sinθ=cosθ는 θ=45°일 때만 → ⑤. 빠른정답 3과 불일치.")

# p43 사분원 옳지 않은 것 (x, y)
add(id="fdfde9d0", qtype="choice",
    question="아래 그림과 같이 반지름의 길이가 1인 사분원에서 다음 중 옳지 않은 것은? (단, [[deg(0) < x < deg(90)]])",
    choices=["[[seg(AB) = sin(y)]]", "[[sin(x) = cos(y)]]", "[[tan(x) × tan(y) = 1]]",
             "[[x]]의 크기가 커지면 [[sin(y)]]의 값도 커진다.", "[[y]]의 크기가 작아지면 [[cos(x)]]의 값도 작아진다."],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "사분원(중심 A 좌하, D 우, 반지름 1 점선 치수, A에 직각 표시). 호 위의 점 C, C에서 AD에 내린 수선의 발 B(직각 표시), D에서 세운 수선과 AC 연장선의 교점 E(D에 직각 표시). ∠CAB=x, ∠AED=y(E에서) 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사분원 도형",
    note="y=90°−x; x 커지면 y 작아져 sin y 작아짐 → ④. 빠른정답 2와 불일치.")

# p45 식 간단히 (45°<A<90°)
add(id="e74b435d", qtype="choice",
    question=("다음 식을 간단히 하면? (단, [[deg(45) < A < deg(90)]])\n"
              "[[-sqrt(pow(cos(A) - tan(A), 2)) - sqrt(pow(sin(A) + cos(A), 2)) + sqrt(pow(sin(A), 2))]]"),
    choices=["[[tan(A)]]", "[[-tan(A)]]", "[[2 sin(A) + tan(A)]]", "[[-2 sin(A) - tan(A)]]", "[[2 cos(A) - tan(A)]]"],
    derived_answer="②", figure=None, difficulty_est=2, confidence=0.9,
    note="cosA<tanA, → −(tanA−cosA)−(sinA+cosA)+sinA=−tanA → ②. 빠른정답 5와 불일치. 식은 상자 안에 인쇄.")

# p62 삼각비표 tan54°−sin53°+cos52°
add(id="b455b5ad", qtype="choice",
    question="다음 삼각비의 표를 보고 [[tan(deg(54)) - sin(deg(53)) + cos(deg(52))]]의 값을 올바르게 구한 것은?",
    choices=["[[1.1932]]", "[[1.1933]]", "[[1.1934]]", "[[1.1935]]", "[[1.1936]]"],
    derived_answer="④",
    figure=[{"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["52°", "0.7880", "0.6157", "1.2799"], ["53°", "0.7986", "0.6018", "1.3270"],
                                              ["54°", "0.8090", "0.5878", "1.3764"], ["55°", "0.8192", "0.5736", "1.4281"]]}}],
    difficulty_est=1, confidence=0.9,
    note="1.3764−0.7986+0.6157=1.1935 → ④ = 빠른정답 ✓.")

# p63 삼각비표 sin39°+cos42°
add(id="e26cc407", qtype="short",
    question="다음 삼각비의 표를 이용하여 [[sin(deg(39)) + cos(deg(42))]]의 값을 구하시오.",
    choices=None, derived_answer="1.3724",
    figure=[{"fn": "table", "args": {"head": ["각도", "사인(sin)", "코사인(cos)", "탄젠트(tan)"],
                                     "rows": [["39°", "0.6293", "0.7771", "0.8098"], ["40°", "0.6428", "0.7660", "0.8391"],
                                              ["41°", "0.6561", "0.7547", "0.8693"], ["42°", "0.6691", "0.7431", "0.9004"]]}}],
    difficulty_est=1, confidence=0.9,
    note="0.6293+0.7431=1.3724. 빠른정답 57과 불일치.")

# p64 삼각비표 cos35°
add(id="f6be952d", qtype="short",
    question="다음 삼각비의 표를 이용하여 [[cos(deg(35))]]의 값을 구하시오.",
    choices=None, derived_answer="0.8192",
    figure=[{"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["34°", "0.5592", "0.8290", "0.6745"], ["35°", "0.5736", "0.8192", "0.7002"],
                                              ["36°", "0.5878", "0.8090", "0.7265"]]}}],
    difficulty_est=1, confidence=0.9,
    note="표에서 cos35°=0.8192. 빠른정답 1.7321과 불일치.")

# p66 삼각비표 sin61°
add(id="c3a01d49", qtype="short",
    question="다음 삼각비의 표를 이용하여 [[sin(deg(61))]]의 값을 구하시오.",
    choices=None, derived_answer="0.8746",
    figure=[{"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["60°", "0.8660", "0.5000", "1.7321"], ["61°", "0.8746", "0.4848", "1.8040"],
                                              ["62°", "0.8829", "0.4695", "1.8807"], ["63°", "0.8910", "0.4540", "1.9626"],
                                              ["64°", "0.8988", "0.4384", "2.0503"], ["65°", "0.9063", "0.4226", "2.1445"]]}}],
    difficulty_est=1, confidence=0.9,
    note="표에서 sin61°=0.8746 = 빠른정답 ✓.")

# p69 삼각비표 sin23°
add(id="1e22d1bd", qtype="short",
    question="다음 삼각비의 표를 이용하여 [[sin(deg(23))]]의 값을 구하시오.",
    choices=None, derived_answer="0.3907",
    figure=[{"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["22°", "0.3746", "0.9272", "0.4040"], ["23°", "0.3907", "0.9205", "0.4245"],
                                              ["24°", "0.4067", "0.9135", "0.4452"]]}}],
    difficulty_est=1, confidence=0.9,
    note="표에서 sin23°=0.3907. 빠른정답 0.7986과 불일치.")

# p72 삼각비표 sin53°
add(id="1f0d86ab", qtype="short",
    question="다음 삼각비의 표를 이용하여 [[sin(deg(53))]]의 값을 구하시오.",
    choices=None, derived_answer="0.7986",
    figure=[{"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["53°", "0.7986", "0.6018", "1.3270"], ["54°", "0.8090", "0.5878", "1.3764"],
                                              ["55°", "0.8192", "0.5736", "1.4281"]]}}],
    difficulty_est=1, confidence=0.9,
    note="표에서 sin53°=0.7986 = 빠른정답 ✓.")

# p75 원뿔 모선 15cm, 높이 12cm, ∠ABO
add(id="5e848c30", qtype="choice",
    question=("아래 그림과 같이 모선 AB의 길이가 [[15]] cm이고 밑면의 높이의 길이가 [[12]] cm인 원뿔이 있다. "
              "이때 [[angle(ABO)]]의 크기를 다음 삼각비의 표를 이용하여 구하면?"),
    choices=["[[deg(36)]]", "[[deg(37)]]", "[[deg(53)]]", "[[deg(54)]]", "[[deg(55)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "원뿔(꼭짓점 A, 밑면 중심 O, 밑면 둘레 위 점 B). AO=12cm(높이, 점선 치수), AB=15cm(모선, 점선 치수), 선분 OB, 색칠(보라)"}},
            {"fn": "table", "args": {"head": ["각도", "sin", "cos", "tan"],
                                     "rows": [["53°", "0.80", "0.60", "1.33"], ["54°", "0.81", "0.59", "1.38"], ["55°", "0.82", "0.57", "1.43"]]}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 원뿔 입체 도형",
    note="sin∠ABO=12/15=0.80 → 53° → ③. 빠른정답 0.7986과 불일치. 원문 '밑면의 높이의 길이' 그대로.")

# p89 사분원+찢어진 삼각비표, 10000(y−x) 소인수 합 (OC=0.6947)
add(id="7ae87e07", qtype="short",
    question=("아래 그림과 같이 좌표평면 위의 원점 O를 중심으로 하고 반지름의 길이가 1인 사분원이 있다. "
              "[[perp(seg(AC), seg(OB))]], [[perp(seg(DB), seg(OB))]]이고 [[seg(AC) = x]], [[seg(DB) = y]]라 할 때, "
              "일부가 찢어진 다음 삼각비의 표를 이용하여 [[10000 (y - x)]]의 모든 소인수의 합을 구하시오."),
    choices=None, derived_answer="53",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(원점 O, 반지름 1, y축 위 1 표시). 호 위의 점 A, A에서 x축에 내린 수선의 발 C(0.6947, 직각 표시), B(1, 0)에서 세운 수선과 OA 연장선의 교점 D(직각 표시)"}},
            {"fn": "table", "args": {"head": ["각도", "사인(sin)", "코사인(cos)", "탄젠트(tan)"],
                                     "rows": [["43°", "0.6820", "0.7314", "0.9325"], ["44°", "0.6947", "0.7193", "0.9657"],
                                              ["45°", "", "", "1.0000"], ["46°", "", "", "1.0355"], ["47°", "", "", "1.0724"]]}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos∠AOC=0.6947 → 46°, x=sin46°=cos44°=0.7193, y=tan46°=1.0355 → 3162=2·3·17·31 → 53. 빠른정답 5와 불일치. 표의 45°~47° sin·cos 칸은 찢어져 비어 있음.")

# p90 같은 구조 (OC=0.6820)
add(id="e9096da2", qtype="short",
    question=("아래 그림과 같이 좌표평면 위의 원점 O를 중심으로 하고 반지름의 길이가 1인 사분원이 있다. "
              "[[perp(seg(AC), seg(OB))]], [[perp(seg(DB), seg(OB))]]이고 [[seg(AC) = x]], [[seg(DB) = y]]라 할 때, "
              "일부가 찢어진 다음 삼각비의 표를 이용하여 [[10000 (y - x)]]의 모든 소인수의 합을 구하시오."),
    choices=None, derived_answer="49",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(원점 O, 반지름 1, y축 위 1 표시). 호 위의 점 A, A에서 x축에 내린 수선의 발 C(0.6820, 직각 표시), B(1, 0)에서 세운 수선과 OA 연장선의 교점 D(직각 표시)"}},
            {"fn": "table", "args": {"head": ["각도", "사인(sin)", "코사인(cos)", "탄젠트(tan)"],
                                     "rows": [["43°", "0.6820", "0.7314", "0.9325"], ["44°", "0.6947", "0.7193", "0.9657"],
                                              ["45°", "", "", "1.0000"], ["46°", "", "", "1.0355"], ["47°", "", "", "1.0724"]]}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos∠AOC=0.6820 → 47°, x=sin47°=cos43°=0.7314, y=tan47°=1.0724 → 3410=2·5·11·31 → 49. 빠른정답 28과 불일치. 표의 45°~47° sin·cos 칸은 찢어져 비어 있음.")

# p91 같은 구조 (OC=0.6561, a·b)
add(id="98502fc9", qtype="short",
    question=("아래 그림과 같이 좌표평면 위의 원점 O를 중심으로 하고 반지름의 길이가 1인 사분원이 있다. "
              "[[perp(seg(AC), seg(OB))]], [[perp(seg(DB), seg(OB))]]이고 [[seg(AC) = a]], [[seg(DB) = b]]라 할 때, "
              "일부가 찢어진 다음 삼각비의 표를 이용하여 [[10000 (b - a)]]의 모든 소인수의 합을 구하시오."),
    choices=None, derived_answer="1322",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면 위 사분원(원점 O, 반지름 1, y축 위 1 표시). 호 위의 점 A, A에서 x축에 내린 수선의 발 C(0.6561, 직각 표시), B(1, 0)에서 세운 수선과 OA 연장선의 교점 D(직각 표시). AC=a, DB=b 점선 치수"}},
            {"fn": "table", "args": {"head": ["각도", "사인(sin)", "코사인(cos)", "탄젠트(tan)"],
                                     "rows": [["41°", "0.6561", "0.7547", "0.8693"], ["43°", "0.6820", "0.7314", "0.9325"],
                                              ["45°", "", "", "1.0000"], ["47°", "", "", "1.0724"], ["49°", "", "", "1.1504"]]}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 좌표평면 사분원 도형",
    note="cos∠AOC=0.6561 → 49°, a=sin49°=cos41°=0.7547, b=tan49°=1.1504 → 3957=3·1319 → 1322 = 빠른정답 ✓. 표의 45°~49° sin·cos 칸은 찢어져 비어 있음.")

# ======================= 삼각비의 활용(2) 넓이 =======================
# p1 BC=10cm, ∠B=60°, 넓이 20√3 → AB
add(id="6181c2f5", qtype="short",
    question=("다음 그림과 같은 [[seg(BC) = 10]] cm, [[angle(B) = deg(60)]]인 삼각형 ABC의 넓이가 [[20 sqrt(3)]] cm²일 때, "
              "[[seg(AB)]]의 길이를 구하시오."),
    choices=None, derived_answer="8 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하) 색칠(분홍). ∠B=60° 표시, BC=10cm 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형",
    note="(1/2)·AB·10·sin60°=20√3 → AB=8 = 빠른정답 ✓.")

# p3 AB=5, BC=8, 넓이 10√2 → ∠B
add(id="b7270153", qtype="choice",
    question=("다음 그림에서 [[seg(AB) = 5]], [[seg(BC) = 8]]인 삼각형의 넓이가 [[10 sqrt(2)]]일 때, [[angle(B)]]의 크기는? "
              "(단, [[deg(0) < angle(B) <= deg(90)]])"),
    choices=["[[deg(30)]]", "[[deg(35)]]", "[[deg(40)]]", "[[deg(45)]]", "[[deg(60)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(A 위, B 좌하, C 우하). AB=5, BC=8 점선 치수, B에 각 표시"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형 도형",
    note="(1/2)·5·8·sinB=10√2 → sinB=√2/2 → 45° → ④ = 빠른정답 ✓.")

# p6 평행사변형, DG=24, DH=20, ∠EDF=30° → □EFHG 넓이
add(id="6fd398f9", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD에서 [[seg(AB)]], [[seg(BC)]]의 중점을 각각 E, F라 하고 [[seg(DE)]], [[seg(DF)]]가 "
              "대각선 AC와 만나는 점을 각각 G, H라 하자. [[seg(DG) = 24]], [[seg(DH) = 20]], [[angle(EDF) = deg(30)]]일 때, "
              "[[quad(EFHG)]]의 넓이를 구하시오."),
    choices=None, derived_answer="150",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 좌상, B 좌하, C 우하, D 우상). E는 AB 중점, F는 BC 중점(같은 길이 표시). 대각선 AC, 선분 DE·DF, 교점 G·H. 사각형 EFHG 색칠(연두). DG=24, DH=20 점선 치수, ∠EDF=30° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형+대각선 복합 도형",
    note="G·H는 무게중심 → DE=36, DF=30; △DEF=270, △DGH=120 → 150 = 빠른정답 ✓.")

# p9 □ABCD, AE가 넓이 이등분 → CE
add(id="ef60a775", qtype="short",
    question=("다음 그림의 [[quad(ABCD)]]에서 [[seg(AB) = 2]] cm, [[seg(BC) = 6]] cm, [[seg(CD) = 4]] cm, "
              "[[angle(B) = angle(C) = deg(60)]]이다. [[seg(AE)]]가 [[quad(ABCD)]]의 넓이를 이등분할 때, [[seg(CE)]]의 길이를 구하시오. "
              "(단, 점 E는 [[seg(CD)]] 위의 점이다.)"),
    choices=None, derived_answer="frac(1,2) cm",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(B 좌하, C 우하, A 좌상, D 우상). BA·CD의 연장선 교점 F(점선, 위). E는 CD 위(D 아래쪽), 선분 AE. AB=2cm, BC=6cm, CD=4cm 점선 치수, ∠B=60°, ∠C=60° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+보조선 도형",
    note="□ABCD=7√3, △ABC=3√3 → △ACE=√3/2, △ACD=4√3 → CE=CD/8=1/2 (빠른정답 없음, 풀이 답).")

# p10 한 변 40% 줄, 다른 변 40% 늘 → 넓이 변화 (A′, C′)
add(id="809efd24", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 한 변의 길이는 [[pct(40)]] 줄이고, 다른 한 변의 길이는 [[pct(40)]] 늘여서 "
              "새로운 삼각형 A′BC′를 만들 때, △A′BC′의 넓이의 변화는?"),
    choices=["변함없다.", "[[pct(4)]] 줄어든다.", "[[pct(4)]] 늘어난다.", "[[pct(16)]] 줄어든다.", "[[pct(16)]] 늘어난다."],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 좌하, C 우하) 색칠(분홍). A′는 BA 위(A보다 아래), C′는 BC 연장선 위(C 오른쪽), 점선 A′C′·CC′"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 삼각형 도형 / 프라임 점 라벨(A′, C′)",
    note="0.6×1.4=0.84 → 16% 감소 → ④ = 빠른정답 ✓.")

# p11 ∠ABC=∠ACD=30°, △BCD 넓이
add(id="89a0572c", qtype="choice",
    question="다음 그림과 같은 [[tri(ABC)]]에서 [[angle(ABC) = angle(ACD) = deg(30)]]일 때, [[tri(BCD)]]의 넓이는?",
    choices=["[[15]] cm²", "[[frac(140,9)]] cm²", "[[frac(145,9)]] cm²", "[[frac(50,3)]] cm²", "[[frac(155,9)]] cm²"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "삼각형 ABC(B 좌, C 우, A 우상). D는 AB 위, 선분 CD, 삼각형 BCD 색칠(하늘). AB=9cm, AC=5cm, BC=10cm 점선 치수, ∠ABC=30°, ∠ACD=30° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+보조선 도형",
    note="△ACD∽△ABC → AD=25/9, BD=56/9 → (1/2)(56/9)(10)sin30°=140/9 → ② = 빠른정답 ✓.")

# p16 둔각삼각형 넓이 과정, 빈칸 순서대로
add(id="c0b4106c", qtype="choice",
    question=("아래는 둔각삼각형에서 두 변의 길이와 그 끼인 각의 크기가 주어질 때, 그 삼각형의 넓이를 구하는 과정이다. "
              "다음 중 □ 안에 들어갈 값을 순서대로 나열한 것은?\n"
              "[[tri(ABC)]]에서 [[angle(ABH) = deg(180) - angle(B)]]\n"
              "[[sin(deg(180) - angle(B))]] = □/□ 이므로\n"
              "[[h]] = □ × □\n"
              "∴ [[tri(ABC) = frac(1,2) a h = frac(1,2) a c sin(deg(180) - angle(B))]]"),
    choices=["[[frac(h,a)]], [[a]], [[tan(deg(180) - angle(B))]]", "[[frac(c,a)]], [[a]], [[sin(deg(180) - angle(B))]]",
             "[[frac(h,c)]], [[c]], [[cos(deg(180) - angle(B))]]", "[[frac(c,h)]], [[c]], [[sin(deg(180) - angle(B))]]",
             "[[frac(h,c)]], [[c]], [[sin(deg(180) - angle(B))]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "상자 안 둔각삼각형 ABC(B 둔각, A 위, C 우) 색칠(보라). A에서 CB 연장선에 내린 수선의 발 H(직각 표시), AH=h(점선), AB=c, BC=a, ∠B=b 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+수선 도형",
    note="sin(180°−B)=h/c, h=c×sin(180°−B) → ⑤. 빠른정답 12와 불일치. 빈칸은 □로 표기.")

# p17 둔각삼각형 넓이 과정, 공통 빈칸
add(id="913f5411", qtype="choice",
    question=("아래는 둔각삼각형에서 두 변의 길이와 그 끼인 각의 크기가 주어질 때, 그 삼각형의 넓이를 구하는 과정이다. "
              "다음 중 □ 안에 공통적으로 들어갈 값으로 알맞은 것은?\n"
              "[[tri(ABC)]]에서 [[angle(ABH) = deg(180) - angle(B)]]\n"
              "[[sin(deg(180) - angle(B))]] = [[h]]/□ 이므로\n"
              "[[h]] = □ × [[sin(deg(180) - angle(B))]]\n"
              "∴ [[tri(ABC) = frac(1,2) a h]] = [[frac(1,2) a]] □ [[sin(deg(180) - angle(B))]]"),
    choices=["[[seg(AC)]]", "[[seg(HB)]]", "[[a]]", "[[c]]", "[[h]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "상자 안 둔각삼각형 ABC(B 둔각, A 위, C 우) 색칠(분홍). A에서 CB 연장선에 내린 수선의 발 H(직각 표시), AH=h(점선), AB=c, BC=a, ∠B=b 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형+수선 도형",
    note="공통 빈칸은 c → ④ = 빠른정답 ✓. 빈칸은 □로 표기.")

# p18 AB=6, BC=10, 넓이 15√3, 둔각 B
add(id="97155a35", qtype="choice",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(AB) = 6]], [[seg(BC) = 10]]이고, 넓이가 [[15 sqrt(3)]]일 때, [[angle(B)]]의 크기는?\n"
              "(단, [[deg(90) < angle(B) <= deg(180)]])"),
    choices=["[[deg(95)]]", "[[deg(100)]]", "[[deg(120)]]", "[[deg(135)]]", "[[deg(150)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(A 좌상, B 아래, C 우) 색칠(분홍). AB=6, BC=10 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형 도형",
    note="(1/2)·6·10·sinB=15√3 → sinB=√3/2, 둔각 → 120° → ③. 빠른정답 5와 불일치.")

# p19 BC=6, ∠C=120°, 넓이 18√3 → AC
add(id="c6e1e53b", qtype="short",
    question="다음 그림에서 [[seg(BC) = 6]], [[angle(C) = deg(120)]]이고 [[tri(ABC)]]의 넓이가 [[18 sqrt(3)]]일 때, [[seg(AC)]]의 길이를 구하시오.",
    choices=None, derived_answer="12",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(B 좌하, C 우하, A 우상 멀리). ∠C=120° 표시, BC=6 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형 도형",
    note="(1/2)·6·AC·sin120°=18√3 → AC=12. 빠른정답 5와 불일치.")

# p25 정사각형 ABCD, ∠EAD=60°, AB=8cm, 색칠 넓이
add(id="d1c593a8", qtype="short",
    question="다음 그림에서 [[quad(ABCD)]]는 정사각형이다. [[angle(EAD) = deg(60)]], [[seg(AB) = 8]] cm일 때, 색칠된 부분의 넓이를 구하시오.",
    choices=None, derived_answer="24 cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 위쪽에 점 E(∠AED 직각 표시), 삼각형 AED, 선분 EC(AD와 교차). 삼각형 EDC 색칠(분홍). ∠EAD=60° 표시, AB=8cm 점선 치수"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 정사각형+삼각형 복합 도형",
    note="∠AED=90°(그림 직각 표시) → ED=4√3, ∠EDC=120° → △EDC=(1/2)·4√3·8·sin120°=24 (빠른정답 없음, 풀이 답).")

# p29 BC=8cm, ∠BCA=150°, 넓이 32 → AC
add(id="53c14225", qtype="short",
    question=("다음 그림과 같은 [[tri(ABC)]]에서 [[seg(BC) = 8]] cm, [[angle(BCA) = deg(150)]]이고 [[tri(ABC)]]의 넓이가 [[32]] cm²일 때, "
              "[[seg(AC)]]의 길이를 구하시오."),
    choices=None, derived_answer="16 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "둔각삼각형 ABC(B 좌하, C 우하, A 우상 멀리) 색칠(분홍). ∠BCA=150° 표시, BC=8cm 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 둔각삼각형 도형",
    note="(1/2)·8·AC·sin150°=32 → AC=16. 빠른정답 2와 불일치.")

# p31 △ABC(∠A=90°)+정사각형 BDEC, DE=8, ∠ABC=45° → △ABD 넓이
add(id="3a0999e2", qtype="choice",
    question=("다음 그림에서 [[tri(ABC)]]는 [[angle(A) = deg(90)]]인 직각삼각형이고 [[quad(BDEC)]]는 [[seg(BC)]]를 한 변으로 하는 정사각형이다. "
              "[[seg(DE) = 8]] cm, [[angle(ABC) = deg(45)]]일 때, [[tri(ABD)]]의 넓이는?"),
    choices=["[[8]] cm²", "[[8 sqrt(2)]] cm²", "[[8 sqrt(3)]] cm²", "[[16]] cm²", "[[16 sqrt(2)]] cm²"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 BDEC(B 좌상, C 우상, D 좌하, E 우하) 위에 직각삼각형 ABC(A 위, 직각 표시). 선분 AD, 삼각형 ABD 색칠(하늘). ∠ABC=45° 표시, DE=8cm 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형+정사각형 복합 도형",
    note="AB=4√2, BD=8, ∠ABD=135° → (1/2)·4√2·8·sin135°=16 → ④ = 빠른정답 ✓.")

# p32 정사각형, ∠EAD=60°, 색칠 넓이 24 → 한 변
add(id="20e90280", qtype="short",
    question=("다음 그림에서 [[quad(ABCD)]]는 정사각형이고 [[angle(EAD) = deg(60)]]이다. 색칠한 부분의 넓이가 [[24]] cm²일 때, "
              "정사각형의 한 변의 길이를 구하시오."),
    choices=None, derived_answer="8 cm",
    figure=[{"fn": "unsupported", "args": {"raw": "정사각형 ABCD(A 좌상, B 좌하, C 우하, D 우상). 위쪽에 점 E(∠AED 직각 표시), 삼각형 AED, 선분 EC(AD와 교차). 삼각형 EDC 색칠(베이지). ∠EAD=60° 표시"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 정사각형+삼각형 복합 도형",
    note="한 변 a: ED=a√3/2, ∠EDC=120° → △EDC=3a²/8=24 → a=8. 빠른정답 16 cm와 불일치.")

# p36 AB=1, BC=3, BD=2, ∠DBC=30° □ABCD 최대 넓이
add(id="8c16d5cc", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = 1]], [[seg(BC) = 3]], [[seg(BD) = 2]], [[angle(DBC) = deg(30)]]인 [[quad(ABCD)]] 중 "
              "넓이가 최대인 것의 넓이는?"),
    choices=["[[frac(5,2)]]", "[[3]]", "[[frac(7,2)]]", "[[4]]", "[[frac(9,2)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, B 좌하, C 우하, D 위) 색칠(하늘), 대각선 BD. AB=1, BC=3, BD=2 점선 치수, ∠DBC=30° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="△BCD=3/2, △ABD 최대=(1/2)·1·2=1 → 5/2 → ①. 빠른정답 4와 불일치.")

# p37 AB=√2, BC=3, BD=2, ∠DBC=30°
add(id="d7747486", qtype="choice",
    question=("다음 그림과 같이 [[seg(AB) = sqrt(2)]], [[seg(BC) = 3]], [[seg(BD) = 2]], [[angle(DBC) = deg(30)]]인 [[quad(ABCD)]] 중 "
              "넓이가 최대인 것의 넓이는?"),
    choices=["[[frac(1 + sqrt(2), 2)]]", "[[frac(1 + 2 sqrt(2), 2)]]", "[[frac(3 + sqrt(2), 2)]]", "[[frac(3 + 2 sqrt(2), 2)]]", "[[frac(5 + 2 sqrt(2), 2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, B 좌하, C 우하, D 위) 색칠(연두), 대각선 BD. AB=√2, BC=3, BD=2 점선 치수, ∠DBC=30° 표시"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="△BCD=3/2, △ABD 최대=√2 → (3+2√2)/2 → ④ = 빠른정답 ✓.")

# p42 반지름 6 원에 내접, ∠B=30°, AD=DC → □ABCD 넓이
add(id="d5395778", qtype="choice",
    question=("다음 그림과 같이 반지름의 길이가 6인 원 O에 내접하는 사각형 ABCD에서 [[angle(B) = deg(30)]], [[seg(AD) = seg(DC)]]일 때, "
              "[[quad(ABCD)]]의 넓이는?"),
    choices=["[[12 + 6 sqrt(3)]]", "[[12 + 9 sqrt(3)]]", "[[18 + 6 sqrt(3)]]", "[[18 + 9 sqrt(3)]]", "[[20 + 6 sqrt(3)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "원 O(반지름 6, O는 AB 위 → AB 지름). A 좌, B 우, C·D 좌상 호 위. 사각형 ABCD 색칠(보라). AD=DC 같은 길이 표시, ∠B=30° 표시, OB=6 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 원+내접사각형 도형",
    note="AB 지름=12, ∠ADB=90°, ∠ABD=15° → △ABD=18, △BCD=9√3 → 18+9√3 → ④. 빠른정답 5와 불일치.")

# p44 □ABCD 넓이 과정 빈칸
add(id="57f13091", qtype="choice",
    question=("다음은 [[quad(ABCD)]]의 넓이를 구하는 과정이다. □ 안에 알맞은 것을 바르게 나열한 것은?\n"
              "[[sub(S,1) = frac(1,2) × 4 sqrt(3) × 8]] × □\n"
              "= [[frac(1,2) × 4 sqrt(3) × 8 × frac(1,2) = 8 sqrt(3)]]\n"
              "[[sub(S,2) = frac(1,2) × 12 × 16]] × □\n"
              "= [[frac(1,2) × 12 × 16 × frac(sqrt(3),2) = 48 sqrt(3)]]\n"
              "[[quad(ABCD) = sub(S,1) + sub(S,2) = 8 sqrt(3) + 48 sqrt(3)]]\n"
              "= [[56 sqrt(3)]] (cm²)"),
    choices=["[[tan(deg(30))]], [[tan(deg(60))]]", "[[cos(deg(30))]], [[cos(deg(60))]]", "[[sin(deg(30))]], [[sin(deg(60))]]",
             "[[sin(deg(30))]], [[tan(deg(60))]]", "[[tan(deg(30))]], [[sin(deg(60))]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, B 좌, C 좌하, D 우하) 색칠(분홍), 대각선 AC(점선)로 S₁(△ABC)·S₂(△ACD) 구분. AB=4√3cm, BC=8cm, AD=12cm, CD=16cm 점선 치수, ∠B=150°, ∠D=60° 표시. 아래 상자에 풀이 과정"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="1/2=sin30°, √3/2=sin60° → ③ = 빠른정답 ✓. 빈칸은 □로 표기.")

# p48 등변사다리꼴 AD=3, BC=7, cosB=√10/10 → 넓이
add(id="f54231d8", qtype="short",
    question=("다음 그림과 같이 [[par(seg(AD), seg(BC))]]인 등변사다리꼴 ABCD에서 [[seg(AD) = 3]], [[seg(BC) = 7]]이고 "
              "[[cos(B) = frac(sqrt(10),10)]]일 때, 사다리꼴 ABCD의 넓이를 구하시오."),
    choices=None, derived_answer="30",
    figure=[{"fn": "unsupported", "args": {"raw": "등변사다리꼴 ABCD(A 좌상, D 우상, B 좌하, C 우하) 색칠(분홍). AD=3, BC=7 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 사다리꼴 도형",
    note="AB cosB=2 → AB=2√10, 높이=AB sinB=6 → (3+7)/2·6=30. 빠른정답 1과 불일치.")

# p67 평행사변형 넓이 12√3, AB:BC=3:2, ∠B=60° → 둘레
add(id="1c49dd22", qtype="short",
    question=("다음 그림과 같은 평행사변형 ABCD의 넓이가 [[12 sqrt(3)]]이고 [[ratio(seg(AB), seg(BC)) = ratio(3, 2)]]일 때, "
              "[[quad(ABCD)]]의 둘레의 길이를 구하시오."),
    choices=None, derived_answer="20",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 좌상, D 우상, B 좌하, C 우하). ∠B=60° 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 도형",
    note="3k·2k·sin60°=12√3 → k=2, AB=6, BC=4 → 둘레 20 = 빠른정답 ✓. ∠B=60°는 그림에만 표시.")

# p69 세 도형 넓이 같을 때 a:b:c
add(id="42ec7294", qtype="choice",
    question="다음 그림과 같은 세 도형의 넓이가 모두 같을 때, 세 선분의 길이의 비 [[ratio(a, b, c)]]는?",
    choices=["[[ratio(sqrt(6), 1, sqrt(2))]]", "[[ratio(2, 1, sqrt(3))]]", "[[ratio(2 sqrt(2), sqrt(2), sqrt(3))]]",
             "[[ratio(2 sqrt(2), sqrt(3), 2)]]", "[[ratio(2 sqrt(3), 1, sqrt(2))]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "상자 안 도형 3개: (1) 두 변 a·b, 끼인각 45°인 삼각형 (2) 두 변 c·b, 끼인각 60°인 평행사변형(대변 같은 길이 표시) (3) 두 변 c·a, 끼인각 30°인 삼각형. 길이는 점선 치수"}}],
    difficulty_est=3, confidence=0.8,
    needs_review="도형 표현 불가: 삼각형·평행사변형 3개 도형",
    note="(√2/4)ab=(√3/2)bc=ca/4 → c=√2b, a=2√3b → 2√3:1:√2 → ⑤. 빠른정답 25/2와 불일치.")

# p75 평행사변형 넓이 24√2, AB=8, BC=6 → ∠C (둔각)
add(id="63fa2dc3", qtype="short",
    question=("다음 그림의 평행사변형 ABCD의 넓이가 [[24 sqrt(2)]] cm²일 때, [[angle(C)]]의 크기를 구하시오. "
              "(단, [[deg(90) < angle(C) < deg(180)]])"),
    choices=None, derived_answer="deg(135)",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 좌상, D 우상, B 좌하, C 우하). AB=8, BC=6 점선 치수, C에 둔각 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형 도형",
    note="8·6·sinB=24√2 → B=45° → C=135° = 빠른정답(135 deg) ✓. AB=8, BC=6은 그림에만 표시.")

# p85 대각선 AC=10, BD=13, 85°·65° → 사각형 넓이
add(id="fb03f4b9", qtype="short",
    question="다음 그림과 같이 대각선의 길이가 [[seg(AC) = 10]] cm, [[seg(BD) = 13]] cm인 사각형 ABCD의 넓이를 구하시오.",
    choices=None, derived_answer="frac(65,2) cm²",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌, B 아래, C 우, D 위) 색칠(하늘), 대각선 AC·BD. ∠BAC=85°, ∠ABD=65° 표시, AC=10cm, BD=13cm 점선 치수"}}],
    difficulty_est=3, confidence=0.75,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="두 대각선이 이루는 각 180°−85°−65°=30° → (1/2)·10·13·sin30°=65/2 (빠른정답 없음, 풀이 답).")

# p94 평행사변형 대각선 60°, AC=10, BD=14
add(id="ba335435", qtype="choice",
    question=("다음 그림의 평행사변형 ABCD에서 대각선이 이루는 각의 크기가 [[deg(60)]]이고, [[seg(AC) = 10]] cm, [[seg(BD) = 14]] cm일 때, "
              "평행사변형 ABCD의 넓이를 구하면?"),
    choices=["[[35]] cm²", "[[35 sqrt(2)]] cm²", "[[35 sqrt(3)]] cm²", "[[frac(35 sqrt(2), 2)]] cm²", "[[frac(35 sqrt(3), 2)]] cm²"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "평행사변형 ABCD(A 좌상, D 우상, B 좌하, C 우하) 색칠(베이지), 대각선 AC·BD. 교점에서 60° 표시, AC=10cm, BD=14cm 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 평행사변형+대각선 도형",
    note="(1/2)·10·14·sin60°=35√3 → ③. 빠른정답 4와 불일치.")

# p95 □ABCD, P 교점, BD=8, ∠APB=60°, 넓이 10√3 → AC
add(id="a28b0f46", qtype="choice",
    question=("다음 그림의 [[quad(ABCD)]]에서 두 대각선의 교점을 P라 하자. [[seg(BD) = 8]], [[angle(APB) = deg(60)]]이고 사각형의 넓이가 "
              "[[10 sqrt(3)]]일 때, [[seg(AC)]]의 길이는?"),
    choices=["[[3]]", "[[5]]", "[[6]]", "[[5 sqrt(3)]]", "[[6 sqrt(2)]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 위, B 좌하, C 우하, D 우), 대각선 AC·BD의 교점 P. ∠APB=60° 표시, BD=8 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="(1/2)·AC·8·sin60°=10√3 → AC=5 → ② (값 5 = 빠른정답 5 ✓).")

# p97 ∠AOB=45°, AC:BD=3:4, 넓이 48√2 → BD
add(id="d5992e05", qtype="short",
    question=("다음 그림과 같이 [[angle(AOB) = deg(45)]]이고 [[ratio(seg(AC), seg(BD)) = ratio(3, 4)]]인 사각형 ABCD의 넓이가 "
              "[[48 sqrt(2)]]일 때, [[seg(BD)]]의 길이를 구하시오."),
    choices=None, derived_answer="16",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(A 좌상, D 우상, B 좌하, C 우하), 대각선 AC·BD의 교점 O. ∠AOB=45° 표시"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 사각형+대각선 도형",
    note="(1/2)(3k)(4k)sin45°=48√2 → k=4 → BD=16 = 빠른정답 ✓.")

# p99 (가)(나) 사각형 넓이 과정 — 이미지에 별개 문항 2개(아래: 사각형 ABCD 넓이 60°,6,8), id는 1개 → 첫 문항(draft_a·빠른정답 대응) 전사
add(id="e627d40a", qtype="choice",
    question=("다음은 두 대각선의 길이가 [[p]], [[q]]이고 두 대각선이 이루는 예각의 크기가 [[x]]인 사각형의 넓이를 구하는 과정이다. "
              "(가), (나)에 알맞은 것을 차례로 쓴 것은?\n"
              "[[quad(ABCD)]]의 각 꼭짓점을 지나고 두 대각선에 각각 평행한 직선을 그어 [[quad(EFGH)]]를 만들면\n"
              "[[quad(ABCD)]] = (가) [[quad(EFGH)]] = [[frac(1,2) p q]] (나)"),
    choices=["[[frac(1,4)]], [[sin(x)]]", "[[frac(1,4)]], [[cos(x)]]", "[[frac(1,2)]], [[sin(x)]]", "[[frac(1,2)]], [[cos(x)]]", "[[1]], [[sin(x)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "사각형 ABCD(색칠, 보라)의 대각선 AC=q, BD=p(점선 치수), 이루는 각 x. 각 꼭짓점을 지나 대각선에 평행한 직선으로 만든 평행사변형 EFGH(E 위, F 좌, G 아래, H 우), EF=q, FG=p, ∠F=x 표시, 평행 화살표 표시. 아래 상자에 (가)(나) 풀이 과정"}}],
    difficulty_est=2, confidence=0.75,
    needs_review="도형 표현 불가: 사각형+평행사변형 복합 도형 / 이미지에 별개 문항 2개(id 1개): 아래쪽 '사각형 ABCD의 넓이(대각선 6, 8, 60°)' 문항은 id가 없어 전사하지 않음",
    note="□ABCD=(1/2)□EFGH=(1/2)pq sin x → ③ = 빠른정답 ✓. 아래 두 번째 문항 답은 (1/2)·6·8·sin60°=12√3(①).")

# ======================= 삼각비 =======================
# p3 ∠B=90°, AC=18, AB=9 → 3cosA−sinA
add(id="43c4ec0b", qtype="choice",
    question="다음과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[3 cos(A) - sin(A)]]의 값은?",
    choices=["[[frac(1 - sqrt(3), 2)]]", "[[frac(2 - sqrt(3), 2)]]", "[[frac(3 - sqrt(3), 2)]]", "[[frac(4 - sqrt(3), 2)]]", "[[frac(5 - sqrt(3), 2)]]"],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(C 좌하, B 우하 직각 표시, A 우상). AC=18, AB=9 점선 치수"}}],
    difficulty_est=2, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="cosA=1/2, sinA=√3/2 → (3−√3)/2 → ③ = 빠른정답 ✓.")

# p5 직각삼각형 sin x (BC=3, AB=4)
add(id="44548923", qtype="short",
    question="다음 그림의 직각삼각형 ABC에서 [[sin(x)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(4,5)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 좌하, B 우하 직각 표시, C 우상). ∠C=x 표시, BC=3, AB=4 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="AC=5 → sin x=AB/AC=4/5 = 빠른정답 ✓.")

# p7 ∠B=90°, AB=2, BC=2√3 → cosA
add(id="a224f4b2", qtype="choice",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 2]], [[seg(BC) = 2 sqrt(3)]]일 때, [[cos(A)]]의 값은?",
    choices=["[[frac(1,4)]]", "[[frac(1,2)]]", "[[frac(sqrt(2),2)]]", "[[frac(sqrt(3),2)]]", "[[1]]"],
    derived_answer="②",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 위, B 좌하 직각 표시, C 우하). AB=2, BC=2√3 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="AC=4 → cosA=2/4=1/2 → ② = 빠른정답 ✓.")

# p10 ∠B=90°, AB=3, BC=2 → cosA
add(id="751fed90", qtype="choice",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에서 [[seg(AB) = 3]], [[seg(BC) = 2]]일 때, [[cos(A)]]의 값은?",
    choices=["[[frac(3 sqrt(13), 13)]]", "[[frac(2 sqrt(13), 13)]]", "[[frac(sqrt(2), 3)]]", "[[frac(2,3)]]", "[[frac(2,13)]]"],
    derived_answer="①",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 좌하, B 우하 직각 표시, C 우상). AB=3, BC=2 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="AC=√13 → cosA=3/√13=3√13/13 → ① = 빠른정답 ✓.")

# p11 ∠B=90°, AC=15, BC=9, AB=12 → sinA
add(id="c5598534", qtype="short",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에 대하여 [[sin(A)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(3,5)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 좌하, B 우하 직각 표시, C 우상). AC=15, BC=9, AB=12 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="sinA=BC/AC=9/15=3/5 = 빠른정답 ✓.")

# p12 같은 그림 → sinC
add(id="206e6b7e", qtype="short",
    question="다음 그림과 같이 [[angle(B) = deg(90)]]인 직각삼각형 ABC에 대하여 [[sin(C)]]의 값을 구하시오.",
    choices=None, derived_answer="frac(4,5)",
    figure=[{"fn": "unsupported", "args": {"raw": "직각삼각형 ABC(A 좌하, B 우하 직각 표시, C 우상). AC=15, BC=9, AB=12 점선 치수"}}],
    difficulty_est=1, confidence=0.8,
    needs_review="도형 표현 불가: 직각삼각형 도형",
    note="sinC=AB/AC=12/15=4/5 = 빠른정답 ✓.")
