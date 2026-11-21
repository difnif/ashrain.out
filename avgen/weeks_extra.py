# 주차별 기초 다지기에 더하는 생성기 — 단원 100제(export.REG)에는 없고 회차에만 쓰인다
#   {id: ("모듈:함수", {단계: "학기:단원"})}
def same(unit):
    return {i: unit for i in range(1, 6)}

def split(a, b, cut=2):
    """1 ~ cut 단계는 a, 나머지는 b"""
    return {i: (a if i <= cut else b) for i in range(1, 6)}

EXTRA = {
    # 초1
    "x-num9": ("g_x1:num9", same("e1-1:9까지의 수")),
    "x-shape1": ("g_x1:shape1", split("e1-1:여러 가지 모양", "e1-2:모양과 시각")),
    "x-add9": ("g_x1:add9", same("e1-1:덧셈과 뺄셈")),
    "x-comp": ("g_x1:comp", same("e1-1:비교하기")),
    "x-num50": ("g_x1:num50", same("e1-1:50까지의 수")),
    "x-rule1": ("g_x1:rule1", same("e1-2:규칙 찾기")),
    # 초2
    "x-num1000": ("g_x2:num1000", same("e2-1:세 자리 수")),
    "x-fig2": ("g_x2:fig2", same("e2-1:여러 가지 도형")),
    "x-len2": ("g_x2:len2", split("e2-1:길이 재기", "e2-2:길이 재기")),
    "x-sort2": ("g_x2:sort2", split("e2-1:분류하기", "e2-2:표와 그래프")),
    "x-mul2": ("g_x2:mul2", same("e2-1:곱셈")),
    "x-num10000": ("g_x2:num10000", same("e2-2:네 자리 수")),
    "x-rule2": ("g_x2:rule2", same("e2-2:규칙 찾기")),
    # 초3
    "x-plane3": ("g_x3:plane3", same("e3-1:평면도형")),
    "x-frac3": ("g_x3:frac3", split("e3-1:분수와 소수", "e3-2:분수", cut=1)),
    "x-circ3": ("g_x3:circ3", same("e3-2:원")),
    "x-pict": ("g_x3:pict", same("e3-2:자료의 정리")),
    # 초4
    "x-move4": ("g_x4:move4", same("e4-1:평면도형의 이동")),
    "x-bar4": ("g_x4:bar4", same("e4-1:막대그래프")),
    "x-line4": ("g_x4:line4", same("e4-2:꺾은선그래프")),
    "x-pgon4": ("g_x4:pgon4", same("e4-2:다각형")),
    # 초5 · 초6
    "x-cong5": ("g_x5:cong5", same("e5-2:합동과 대칭")),
    "x-graph6": ("g_x5:graph6", same("e6-1:여러 가지 그래프")),
    "x-cube6": ("g_x5:cube6", same("e6-2:공간과 입체")),
    "x-cyl6": ("g_x5:cyl6", same("e6-2:원기둥, 원뿔, 구")),
    # 중3 · 고3
    "x-stat3": ("g_x6:stat3", same("m3-2:통계")),
    "x-space3": ("g_x6:space3", same("h3-3:공간도형과 공간좌표")),
}
