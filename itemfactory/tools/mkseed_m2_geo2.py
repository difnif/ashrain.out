# itemfactory/tools/mkseed_m2_geo2.py — 중2-2 사각형·피타고라스 시드 생성기: 평행사변형 · 여러 가지 사각형 · 피타고라스 정리 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_geo2.py
#     → seeds/m2-2-parallelogram.json (5틀) · seeds/m2-2-special-quad.json (5틀) · seeds/m2-2-pythagoras.json (5틀)
#
# 유형은 출판사 평가자료 카탈로그(reference/pubs/TYPES.md 6.1~6.3 · 7.5)에서 골랐다 — 문항 복제 아님.
# 도형은 전부 scene. '구하는 변'이 바뀌는 틀은 변 라벨을 파생 수치로 두고(모르는 변 = 0 → 렌더러가 숨김) 행 문자열 "x"로 표시한다.
from __future__ import annotations

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mkseed_m2_geo1 import arc, scene  # noqa: E402
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_PAR = "3d6e730c-f860-4fbc-96eb-8c941a22d54c"      # 평행사변형 대각 크기 비율 응용 (A)
SCHEMA_SQ = "99bffd76-117f-45d8-998c-667d7fd339e7"       # 마름모 성질 활용 넓이·거리 계산 (B)
SCHEMA_PY = "48e88411-b4c1-4a72-8aba-1ff25f83c60b"       # 직각삼각형 피타고라스 정리 응용 (A)

GEO = {"process": "추론", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["구하는대상혼동"]}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def lseg(a, b, label, **kw):
    d = {"a": a, "b": b, "label": label}
    d.update(kw)
    return d


# ═══════════════════════════════════════════════════════════════════ 1. 평행사변형
PAR = dict(prereq=["평행사변형의 성질: 두 쌍의 대변·대각이 각각 같고 두 대각선은 서로 다른 것을 이등분한다", "평행선의 엇각·동측내각"], ops=["각도", "사칙"], tags=["평행사변형", "대변", "대각", "대각선"])

RATIO_P = {}
for _p, _q in [(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4), (4, 1), (4, 5), (5, 4), (1, 5), (5, 1), (2, 7), (7, 2), (7, 3), (3, 7), (1, 8), (8, 1),
               (5, 7), (7, 5), (1, 9), (9, 1), (7, 11), (11, 7), (4, 11), (11, 4), (13, 17), (17, 13), (7, 23), (23, 7), (1, 11), (11, 1), (5, 13), (13, 5)]:
    if (180 * _p) % (_p + _q) == 0:
        RATIO_P[f"{_p}-{_q}"] = {"p": _p, "q": _q, "av": 180 * _p // (_p + _q), "bv": 180 * _q // (_p + _q)}


def par_t1():
    rows = {"C": {"XQ": "C", "isC": 1, "XA": "C", "XF": "B", "XT": "D", "SAME": "A", "LAW": "대각 ∠C = ∠A"},
            "D": {"XQ": "D", "isC": 0, "XA": "D", "XF": "A", "XT": "C", "SAME": "B", "LAW": "대각 ∠D = ∠B"}}
    pts = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": [5, 0], "D": ["{ax + 5}", "{ay}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]]
    marks = {"arc": [arc("A", "B", "D", None, "arc:a"), arc("B", "C", "A", None, "arc:b"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-parallelogram", 1, PAR,
        title="평행사변형의 각 — 이웃한 두 내각의 비로 대각 구하기",
        skill="이웃한 두 내각의 합이 180°임을 쓰고 비로 나눈 뒤 대각으로 옮기기",
        variant_axis={"구하는 것": "∠C / ∠D", "비": "정수 답이 되는 34쌍"},
        discriminates="∠A + ∠B = 180°(동측내각)를 세우고 대각이 같음을 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "pr", "values": {"in": list(RATIO_P)}}],
        table=[{"key": "w", "rows": rows}, {"key": "pr", "rows": RATIO_P}],
        derive={"ans_v": "av*isC + bv*(1 - isC)", "ax": "3*cos(pi*bv/180)", "ay": "3*sin(pi*bv/180)"},
        constraints=["av != bv"],
        cost_values=["p", "q", "av", "bv", "ans_v"],
        answer_var="ans_v",
        verify=["av + bv == 180", "av*q == bv*p", "(isC == 1 and ans == av) or (isC == 0 and ans == bv)"],
        question="다음 그림의 평행사변형 ABCD에서 [[angle(A)]] : [[angle(B)]] = {p} : {q}일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="평행사변형에서 AD ∥ BC이므로 ∠A와 ∠B는 동측내각 — 합이 180°다. 이 180°를 {p} : {q}로 나누면 ∠A, ∠B가 나오고, 평행사변형은 두 쌍의 대각의 크기가 같으므로 ∠C = ∠A, ∠D = ∠B다.",
        sol1_fig=scene(pts, segs, marks=marks, labels=[{"at": "A", "text": "{av}°", "dx": 22, "dy": 18, "accent": True, "k": "lbl:a"}, {"at": "B", "text": "{bv}°", "dx": 26, "dy": -12, "accent": True, "k": "lbl:b"},
                                                     {"at": "{XA}", "text": "{ans_v}°", "dx": "{-24*isC + 26*(1 - isC)}", "dy": "{-12*isC + 18*(1 - isC)}", "accent": True, "k": "lbl:ans"}]),
        sol1_anim=[[hl("arc:a", "arc:b", "lbl:a", "lbl:b", keep=True)], [hl("arc:ask", "lbl:ans")]],
        sol2=[
            "AD ∥ BC이므로 ∠A + ∠B = 180° (동측내각)",
            "∠A : ∠B = {p} : {q}이므로 ∠A = 180° × [[frac({p}, {p + q})]] = {av}°, ∠B = 180° − {av}° = {bv}°",
            "평행사변형의 대각의 크기는 같으므로 ∠{XQ} = ∠{SAME} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠A + ∠B = 180°", "hint": "동측내각"}, {"text": "∠A = {av}°, ∠B = {bv}°", "hint": "{p} : {q}로 나누기"}, {"text": "∠{XQ} = ∠{SAME} = {ans_v}°", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol_check="네 내각 {av}° + {bv}° + {av}° + {bv}° = 360°로 사각형의 내각의 합과 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="AD ∥ BC이므로 ∠A + ∠B = 180°이고 ∠A : ∠B = {p} : {q}이므로 ∠A = {av}°, ∠B = {bv}°이다. 평행사변형의 대각의 크기는 같으므로 ∠{XQ} = ∠{SAME} = {ans_v}°다.",
        rubric=[
            {"element": "동측내각", "points": 3, "criterion": "AD ∥ BC에서 ∠A + ∠B = 180°임을 밝히고 비로 나누었다.", "partial": "180°의 근거 없이 나누기만 했으면 1점."},
            {"element": "대각", "points": 2, "criterion": "대각의 크기가 같음을 써서 ∠{XQ} = ∠{SAME}로 옮겼다.", "partial": "이웃한 각으로 잘못 옮겼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


def par_t2():
    rows = {"perim": {"Q": "□ABCD의 둘레의 길이", "isP": 1, "uAB": 0, "uBC": 0, "XAB": "", "XBC": "", "G1T": "[[seg(AB)]] = ", "G2T": "[[seg(BC)]] = ", "G2U": " cm",
                      "F1": "둘레 = 2 × (", "F2": " + ", "F3": ")", "LAW": "2 × (AB + BC)"},
            "bc": {"Q": "[[seg(BC)]]의 길이", "isP": 0, "uAB": 0, "uBC": 1, "XAB": "", "XBC": "x", "G1T": "[[seg(AB)]] = ", "G2T": "둘레의 길이가 ", "G2U": " cm",
                   "F1": "BC = ", "F2": " ÷ 2 − ", "F3": "", "LAW": "둘레 ÷ 2 − AB"},
            "ab": {"Q": "[[seg(AB)]]의 길이", "isP": 0, "uAB": 1, "uBC": 0, "XAB": "x", "XBC": "", "G1T": "[[seg(BC)]] = ", "G2T": "둘레의 길이가 ", "G2U": " cm",
                   "F1": "AB = ", "F2": " ÷ 2 − ", "F3": "", "LAW": "둘레 ÷ 2 − BC"}}
    pts = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": ["{b}", 0], "D": ["{ax + b}", "{ay}"]}
    segs = [lseg("A", "B", "{la}"), lseg("B", "C", "{lb}"), ["C", "D"], ["D", "A"], lseg("A", "B", "{XAB}"), lseg("B", "C", "{XBC}")]
    return tpl("m2-2-parallelogram", 2, PAR,
        title="평행사변형의 둘레와 변 — 대변의 길이가 같다",
        skill="AB = DC, BC = AD를 써서 둘레 = 2(AB + BC)로 두고 묻는 것 구하기",
        variant_axis={"구하는 것": "둘레 / BC / AB", "AB": "3~12", "BC": "4~15"},
        discriminates="두 쌍의 대변이 같음을 근거로 둘레를 2(AB + BC)로 세우는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=60, process="절차수행",
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"int": [3, 12]}}, {"name": "b", "values": {"int": [4, 15]}}],
        table={"key": "w", "rows": rows},
        derive={"P": "2*(a + b)", "la": "a*(1 - uAB)", "lb": "b*(1 - uBC)", "g1": "a*(1 - uAB) + b*uAB", "g2": "b*isP + 2*(a + b)*(1 - isP)",
                "v1": "a*isP + 2*(a + b)*(1 - isP)", "v2": "b*isP + a*uBC + b*uAB", "ans_v": "2*(a + b)*isP + b*uBC + a*uAB",
                "ax": "a*cos(pi*65/180)", "ay": "a*sin(pi*65/180)"},
        constraints=["a != b", "2*a != b", "a != 2*b"],
        cost_values=["a", "b", "P", "ans_v"],
        answer_var="ans_v",
        verify=["P == 2*(a + b)", "(isP == 1 and ans == P) or (uBC == 1 and ans == b) or (uAB == 1 and ans == a)"],
        question="다음 그림의 평행사변형 ABCD에서 {G1T}{g1} cm이고 {G2T}{g2}{G2U}일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="평행사변형은 두 쌍의 대변의 길이가 각각 같다: DC = AB, AD = BC. 그래서 둘레는 AB + BC + CD + DA = 2 × (AB + BC)다. 둘레와 한 변을 알면 둘레 ÷ 2에서 그 변을 빼서 다른 변을 얻는다.",
        sol1_fig=scene(pts, [lseg("A", "B", "{a} cm"), lseg("B", "C", "{b} cm"), lseg("C", "D", "{a} cm"), lseg("D", "A", "{b} cm")],
                       marks={"eq": [[["A", "B"], ["C", "D"]], [["B", "C"], ["D", "A"]]]}),
        sol1_anim=[[hl("eq:A-B", "eq:C-D", "seglbl:A-B", "seglbl:C-D", keep=True)], [hl("eq:B-C", "eq:D-A", "seglbl:B-C", "seglbl:D-A", keep=True)]],
        sol2=[
            "평행사변형의 대변의 길이는 같으므로 DC = AB, AD = BC",
            "둘레 = AB + BC + CD + DA = 2 × (AB + BC)",
            "{F1}{v1}{F2}{v2}{F3} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "DC = AB, AD = BC", "hint": "대변"}, {"text": "둘레 = 2 × (AB + BC)", "hint": "네 변의 합"}, {"text": "{F1}{v1}{F2}{v2}{F3} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AB = {a} cm, BC = {b} cm이면 둘레는 2 × ({a} + {b}) = {P}(cm)로 세 값이 서로 맞는다. 답은 {ans_v} cm다.",
        model_answer="평행사변형의 대변의 길이는 같으므로 DC = AB, AD = BC이고 둘레는 2 × (AB + BC)이다. {F1}{v1}{F2}{v2}{F3} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "대변 상등", "points": 3, "criterion": "DC = AB, AD = BC임을 밝혔다.", "partial": "한 쌍만 썼으면 1점."},
            {"element": "둘레 식", "points": 2, "criterion": "둘레 = 2 × (AB + BC)로 두고 {F1}{v1}{F2}{v2}{F3} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "둘레를 AB + BC로 두었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def par_t3():
    rows = {"ocd": {"Q": "△OCD의 둘레의 길이", "isO": 1, "isAC": 0, "isBD": 0, "isS": 0, "F1": "OC + OD + CD = ", "F2": " + ", "F3": " + ", "LAW": "OC = OA, OD = OB, CD = AB"},
            "ac": {"Q": "[[seg(AC)]]의 길이", "isO": 0, "isAC": 1, "isBD": 0, "isS": 0, "F1": "AC = 2 × OA = 2 × ", "F2": "", "F3": "", "LAW": "OA = OC"},
            "bd": {"Q": "[[seg(BD)]]의 길이", "isO": 0, "isAC": 0, "isBD": 1, "isS": 0, "F1": "BD = 2 × OB = 2 × ", "F2": "", "F3": "", "LAW": "OB = OD"},
            "sum": {"Q": "두 대각선의 길이의 합", "isO": 0, "isAC": 0, "isBD": 0, "isS": 1, "F1": "AC + BD = 2 × ", "F2": " + 2 × ", "F3": "", "LAW": "각 대각선 = 2 × 절반"}}
    pts = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": ["{w}", 0], "D": ["{ax + w}", "{ay}"], "O": ["{(ax + w)/2}", "{ay/2}"]}
    segs = [lseg("A", "B", "{c} cm"), ["B", "C"], ["C", "D"], ["D", "A"], lseg("O", "A", "{p} cm"), lseg("O", "B", "{q} cm"), ["O", "C"], ["O", "D"]]
    olab = [{"at": "O", "text": "O", "dx": 12, "dy": -8, "k": "lbl:O"}]
    return tpl("m2-2-parallelogram", 3, PAR,
        title="평행사변형의 대각선 — 교점에서 나뉜 길이",
        skill="두 대각선이 서로 다른 것을 이등분함을 써서 OC = OA, OD = OB로 옮기기",
        variant_axis={"구하는 것": "△OCD 둘레 / AC / BD / 대각선의 합", "OA·OB·AB": "3~12"},
        discriminates="대각선의 교점 O가 각 대각선의 중점임을 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "p", "values": {"int": [3, 9]}}, {"name": "q", "values": {"int": [3, 9]}}, {"name": "c", "values": {"int": [4, 12]}}],
        table={"key": "w", "rows": rows},
        derive={"ans_v": "(p + q + c)*isO + 2*p*isAC + 2*q*isBD + (2*p + 2*q)*isS", "v1": "p*(isO + isAC + isS) + q*isBD", "v2": "q*(isO + isS)", "v3": "c*isO",
                "w": "sqrt(abs(2*p*p + 2*q*q - c*c))", "ax": "(w*w + c*c - 4*p*p)/(2*w)", "ay": "sqrt(abs(c*c - ax*ax))"},
        constraints=["p != q", "p + q > c + 1", "p + c > q + 1", "q + c > p + 1", "2*p*p + 2*q*q > c*c + 4", "ans_v != p", "ans_v != q", "ans_v != c"],
        cost_values=["p", "q", "c", "ans_v"],
        answer_var="ans_v",
        verify=["(isO == 1 and ans == p + q + c) or (isAC == 1 and ans == 2*p) or (isBD == 1 and ans == 2*q) or (isS == 1 and ans == 2*p + 2*q)"],
        question="다음 그림의 평행사변형 ABCD에서 두 대각선의 교점을 O라고 하자. [[seg(OA)]] = {p} cm, [[seg(OB)]] = {q} cm, [[seg(AB)]] = {c} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, labels=olab),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="평행사변형의 두 대각선은 서로 다른 것을 이등분한다. 그러므로 교점 O는 AC와 BD 각각의 중점이고 OC = OA = {p} cm, OD = OB = {q} cm다. 또 대변의 길이가 같으므로 CD = AB = {c} cm — △OCD의 세 변은 △OAB의 세 변과 같다.",
        sol1_fig=scene(pts, [["A", "B"], ["B", "C"], lseg("D", "C", "{c} cm"), ["D", "A"], ["O", "A"], ["O", "B"], lseg("C", "O", "{p} cm"), lseg("D", "O", "{q} cm")],
                       marks={"eq": [[["O", "A"], ["O", "C"]], [["O", "B"], ["O", "D"]]]}, labels=olab),
        sol1_anim=[[hl("eq:O-A", "eq:O-C", "seglbl:C-O", keep=True)], [hl("eq:O-B", "eq:O-D", "seglbl:D-O", keep=True)], [hl("seglbl:D-C", "seg:C-D")]],
        sol2=[
            "두 대각선은 서로 다른 것을 이등분하므로 OC = OA = {p} cm, OD = OB = {q} cm",
            "대변의 길이는 같으므로 CD = AB = {c} cm",
            "{F1}{v1}{F2}{v2}{F3}{v3} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "OC = {p}, OD = {q}", "hint": "대각선이 서로를 이등분"}, {"text": "CD = AB = {c}", "hint": "대변"}, {"text": "{Q}: {ans_v} cm", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AC = 2 × {p} = {2*p}(cm), BD = 2 × {q} = {2*q}(cm)이고 △OCD의 둘레는 {p} + {q} + {c} = {p + q + c}(cm)로 △OAB의 둘레와 같다. 답은 {ans_v} cm다.",
        model_answer="평행사변형의 두 대각선은 서로 다른 것을 이등분하므로 OC = OA = {p} cm, OD = OB = {q} cm이고, 대변의 길이가 같으므로 CD = AB = {c} cm이다. 따라서 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "대각선의 이등분", "points": 3, "criterion": "O가 두 대각선의 중점이므로 OC = OA, OD = OB임을 밝혔다.", "partial": "한 대각선만 썼으면 1점."},
            {"element": "길이 계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2}{F3}{v3} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "대변 CD = AB를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def par_t4():
    rows = {"ec": {"Q": "[[seg(EC)]]의 길이", "PT": "점 E는 [[angle(A)]]의 이등분선과 변 BC의 교점이다", "isEF": 0, "HID": "F", "S1A": "A", "S1B": "E", "S2A": "A", "S2B": "E", "Q1A": "A", "Q1B": "B", "Q2A": "B", "Q2B": "E", "LP": "E", "LDX": -20,
                   "A1": "A", "A1F": "B", "A1T": "E", "A2": "A", "A2F": "E", "A2T": "D", "A3": "A", "A3F": "B", "A3T": "E", "A4": "A", "A4F": "E", "A4T": "D",
                   "PAR": "AD ∥ BC이므로 ∠DAE = ∠AEB (엇각)", "BIS": "AE가 ∠A를 이등분하므로 ∠BAE = ∠DAE = ∠AEB, 즉 △ABE는 BE = AB인 이등변삼각형: BE = AB =",
                   "F1": "EC = BC − BE = ", "F2": " − ", "LAW": "BE = AB"},
            "bf": {"Q": "[[seg(BF)]]의 길이", "PT": "점 F는 [[angle(D)]]의 이등분선과 변 BC의 교점이다", "isEF": 0, "HID": "E", "S1A": "D", "S1B": "F", "S2A": "D", "S2B": "F", "Q1A": "C", "Q1B": "D", "Q2A": "C", "Q2B": "F", "LP": "F", "LDX": 20,
                   "A1": "D", "A1F": "A", "A1T": "F", "A2": "D", "A2F": "F", "A2T": "C", "A3": "D", "A3F": "A", "A3T": "F", "A4": "D", "A4F": "F", "A4T": "C",
                   "PAR": "AD ∥ BC이므로 ∠ADF = ∠DFC (엇각)", "BIS": "DF가 ∠D를 이등분하므로 ∠CDF = ∠ADF = ∠DFC, 즉 △DFC는 CF = CD인 이등변삼각형: CF = CD = AB =",
                   "F1": "BF = BC − CF = ", "F2": " − ", "LAW": "CF = CD = AB"},
            "ef": {"Q": "[[seg(EF)]]의 길이", "PT": "두 점 E, F는 각각 [[angle(A)]], [[angle(D)]]의 이등분선과 변 BC의 교점이다", "isEF": 1, "HID": "Z", "S1A": "A", "S1B": "E", "S2A": "D", "S2B": "F", "Q1A": "A", "Q1B": "B", "Q2A": "B", "Q2B": "E", "LP": "E", "LDX": -20,
                   "A1": "A", "A1F": "B", "A1T": "E", "A2": "A", "A2F": "E", "A2T": "D", "A3": "D", "A3F": "A", "A3T": "F", "A4": "D", "A4F": "F", "A4T": "C",
                   "PAR": "AD ∥ BC이므로 ∠DAE = ∠AEB, ∠ADF = ∠DFC (엇각)", "BIS": "두 이등분선에서 △ABE, △DFC가 각각 이등변삼각형이므로 BE = AB, CF = CD = AB =",
                   "F1": "EF = BE + CF − BC = 2 × ", "F2": " − ", "LAW": "두 선분이 겹친 길이"}}
    pts = {"A": ["{a/2}", "{ay}"], "B": [0, 0], "C": ["{b}", 0], "D": ["{a/2 + b}", "{ay}"], "E": ["{a}", 0], "F": ["{b - a}", 0]}
    segs = [lseg("A", "B", "{a} cm"), ["B", "C"], ["C", "D"], lseg("D", "A", "{b} cm"), ["{S1A}", "{S1B}"], ["{S2A}", "{S2B}"]]
    marks = {"arc": [arc("{A1}", "{A1F}", "{A1T}", "•", "arc:1"), arc("{A2}", "{A2F}", "{A2T}", "•", "arc:2"), arc("{A3}", "{A3F}", "{A3T}", "•", "arc:3"), arc("{A4}", "{A4F}", "{A4T}", "•", "arc:4")]}
    return tpl("m2-2-parallelogram", 4, PAR,
        title="평행사변형의 각의 이등분선 — 엇각으로 생기는 이등변삼각형",
        skill="이등분선과 평행선의 엇각으로 이등변삼각형(BE = AB)을 찾아 길이 구하기",
        variant_axis={"구하는 것": "EC / BF / EF(겹친 부분)", "AB": "3~8", "AD": "5~14"},
        discriminates="엇각과 이등분된 각이 같아 △ABE가 이등변삼각형(BE = AB)이 됨을 읽는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=100,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"int": [3, 8]}}, {"name": "b", "values": {"int": [5, 14]}}],
        table={"key": "w", "rows": rows},
        derive={"ans_v": "(b - a)*(1 - isEF) + (2*a - b)*isEF", "v1": "b*(1 - isEF) + a*isEF", "v2": "a*(1 - isEF) + b*isEF", "ay": "a*sin(pi*60/180)"},
        constraints=["b > a", "isEF == 0 or b < 2*a", "ans_v != a", "ans_v != b", "ans_v >= 1"],
        cost_values=["a", "b", "ans_v"],
        answer_var="ans_v",
        verify=["(isEF == 0 and ans == b - a) or (isEF == 1 and ans == 2*a - b)"],
        question="다음 그림의 평행사변형 ABCD에서 {PT}. [[seg(AB)]] = {a} cm, [[seg(AD)]] = {b} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, nodot=["{HID}"]),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="각의 이등분선이 평행사변형의 변과 만나면 이등변삼각형이 생긴다. AD ∥ BC이므로 이등분선이 만드는 각은 엇각으로 옮겨져 이등변삼각형의 두 밑각이 되고, 그 삼각형의 두 변이 같아진다: BE = AB(또는 CF = CD = AB). 그 다음 BC = {b} cm에서 빼거나 겹친 길이를 센다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["{Q1A}", "{Q1B}"], ["{Q2A}", "{Q2B}"]]]}, nodot=["{HID}"],
                       labels=[{"at": "{LP}", "text": "{a} cm", "dx": "{LDX}", "dy": 16, "accent": True, "k": "lbl:be"}]),
        sol1_anim=[[hl("arc:1", "arc:2", "arc:3", "arc:4", keep=True)], [hl("eq:A-B", "eq:B-E", "eq:C-D", "eq:C-F", "lbl:be", keep=True)]],
        sol2=[
            "{PAR}",
            "{BIS} {a} cm",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "엇각 = 이등분된 각", "hint": "AD ∥ BC"}, {"text": "BE = AB = {a} (또는 CF = CD = {a})", "hint": "이등변삼각형"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="BE = {a} cm, BC = {b} cm이므로 EC = {b - a} cm, 마찬가지로 CF = {a} cm, BF = {b - a} cm이며, 두 이등분선을 모두 그리면 BE + CF = {2*a} cm가 BC = {b} cm와 비교된다. 답은 {ans_v} cm다.",
        model_answer="{PAR}. {BIS} {a} cm이다. {F1}{v1}{F2}{v2} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "엇각·이등변삼각형", "points": 3, "criterion": "엇각과 이등분된 각이 같아 이등변삼각형이 생김(BE = AB 또는 CF = CD)을 밝혔다.", "partial": "이등변삼각형이라고만 쓰고 근거(엇각)가 없으면 1점."},
            {"element": "길이 계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "BE = AB까지만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "다른 토막의 길이를 답했으면 인정하지 않는다."},
        ],
    )


P_POS = {"1": {"px": 2.8, "py": 1.2}, "2": {"px": 4.2, "py": 1.9}, "3": {"px": 3.4, "py": 2.4}}


def par_t5():
    rows = {"quad": {"Q": "□ABCD의 넓이", "isQ": 1, "L2P": "", "G1T": "△PAB의 넓이가 ", "G2T": "△PCD의 넓이가 ", "F1": "□ABCD = 2 × (", "F2": " + ", "F3": ")", "LAW": "2 × (△PAB + △PCD)"},
            "pcd": {"Q": "△PCD의 넓이", "isQ": 0, "L2P": "□ABCD = ", "G1T": "△PAB의 넓이가 ", "G2T": "□ABCD의 넓이가 ", "F1": "△PCD = [[frac(1, 2)]] × ", "F2": " − ", "F3": "", "LAW": "□ABCD ÷ 2 − △PAB"}}
    pts = {"A": [1.5, 3.2], "B": [0, 0], "C": [6, 0], "D": [7.5, 3.2], "P": ["{px}", "{py}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["P", "A"], ["P", "B"], ["P", "C"], ["P", "D"]]
    labels = [{"at": ["{(px + 1.5)/3}", "{(py + 3.2)/3}"], "text": "{g1} cm²", "dx": 0, "dy": 4, "k": "lbl:g1"},
              {"at": ["{isQ*(px + 13.5)/3 + (1 - isQ)*4.5}", "{isQ*(py + 3.2)/3 + (1 - isQ)*3.9}"], "text": "{L2P}{g2} cm²", "dx": 0, "dy": 4, "k": "lbl:g2"}]
    return tpl("m2-2-parallelogram", 5, PAR,
        title="평행사변형 내부의 점 — △PAB + △PCD = ½□ABCD",
        skill="P에서 두 평행한 변까지의 거리의 합이 높이임을 써서 두 삼각형의 넓이의 합이 절반임을 쓰기",
        variant_axis={"구하는 것": "□ABCD / △PCD", "넓이": "4~20", "P의 위치": "3가지"},
        discriminates="마주 보는 두 삼각형의 넓이의 합이 평행사변형의 절반임을 근거(높이의 합)와 함께 쓰는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90, process="문제해결",
        prereq=["삼각형의 넓이", "평행사변형의 넓이", "평행선 사이의 거리"], ops=["넓이", "방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "s1", "values": {"int": [4, 20]}}, {"name": "s2", "values": {"int": [4, 20]}}, {"name": "s", "values": {"in": list(P_POS)}}],
        table=[{"key": "w", "rows": rows}, {"key": "s", "rows": P_POS}],
        derive={"S": "2*(s1 + s2)", "g1": "s1", "g2": "s2*isQ + 2*(s1 + s2)*(1 - isQ)", "ans_v": "2*(s1 + s2)*isQ + s2*(1 - isQ)",
                "ux": "1.5/sqrt(1.5*1.5 + 3.2*3.2)", "uy": "3.2/sqrt(1.5*1.5 + 3.2*3.2)", "t1": "px*ux + py*uy", "h1x": "t1*ux", "h1y": "t1*uy",
                "t2": "(px - 6)*ux + py*uy", "h2x": "6 + t2*ux", "h2y": "t2*uy"},
        constraints=["s1 != s2", "ans_v != s1", "ans_v != s2"],
        cost_values=["s1", "s2", "S", "ans_v"],
        answer_var="ans_v",
        verify=["S == 2*(s1 + s2)", "(isQ == 1 and ans == S) or (isQ == 0 and ans == s2)"],
        question="다음 그림과 같이 평행사변형 ABCD의 내부에 한 점 P를 잡았다. {G1T}{g1} cm², {G2T}{g2} cm²일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, labels=labels, shade=[["P", "A", "B"], ["P", "C", "D"]]),
        answer="{ans_v}", answer_alt=["{ans_v} cm²"],
        sol1="AB ∥ DC이므로 점 P에서 AB까지의 거리 h₁과 DC까지의 거리 h₂의 합은 두 평행선 사이의 거리, 곧 AB를 밑변으로 한 평행사변형의 높이 h와 같다. △PAB = [[frac(1, 2)]] × AB × h₁, △PCD = [[frac(1, 2)]] × DC × h₂이고 DC = AB이므로 두 넓이의 합은 [[frac(1, 2)]] × AB × h = [[frac(1, 2)]]□ABCD다.",
        sol1_fig=scene({**pts, "H": ["{h1x}", "{h1y}"], "K": ["{h2x}", "{h2y}"]}, segs + [{"a": "P", "b": "H", "dash": True, "label": "h₁"}, {"a": "P", "b": "K", "dash": True, "label": "h₂"}],
                       marks={"right": [["P", "H", "B"], ["P", "K", "D"]]}, nodot=["H", "K"], labels=labels, shade=[["P", "A", "B"], ["P", "C", "D"]]),
        sol1_anim=[[hl("shade:0", "shade:1", keep=True)], [hl("seg:P-H", "seg:P-K", "seglbl:P-H", "seglbl:P-K", keep=True)]],
        sol2=[
            "P에서 AB, DC에 내린 수선의 길이를 h₁, h₂라 하면 h₁ + h₂ = (평행사변형의 높이 h)",
            "△PAB + △PCD = [[frac(1, 2)]] × AB × h₁ + [[frac(1, 2)]] × AB × h₂ = [[frac(1, 2)]] × AB × h = [[frac(1, 2)]]□ABCD",
            "{F1}{g1}{F2}{g2}{F3} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm²",
        ],
        sol2_fig=steps([{"text": "h₁ + h₂ = h", "hint": "평행선 사이의 거리"}, {"text": "△PAB + △PCD = [[frac(1, 2)]]□ABCD", "hint": "밑변 AB = DC"}, {"text": "{F1}{g1}{F2}{g2}{F3} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="△PAB + △PCD = {s1} + {s2} = {s1 + s2}(cm²)는 □ABCD = {S} cm²의 절반이고, 나머지 △PBC + △PDA도 {s1 + s2} cm²다. 답은 {ans_v} cm²다.",
        model_answer="AB ∥ DC이므로 P에서 AB, DC까지의 거리의 합은 평행사변형의 높이와 같다. 따라서 △PAB + △PCD = [[frac(1, 2)]]□ABCD이고, {F1}{g1}{F2}{g2}{F3} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm²다.",
        rubric=[
            {"element": "절반 관계", "points": 3, "criterion": "높이의 합을 근거로 △PAB + △PCD = [[frac(1, 2)]]□ABCD임을 밝혔다.", "partial": "관계만 쓰고 근거가 없으면 1점."},
            {"element": "넓이 계산", "points": 2, "criterion": "{F1}{g1}{F2}{g2}{F3} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "절반을 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm²를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


PAR_SEED = {
    "seed_id": "m2-2-parallelogram", "category": "도형",
    "title": "평행사변형의 성질 — 각의 비, 둘레·변, 대각선의 교점, 각의 이등분선, 내부의 점과 넓이",
    "unit_id": "m2-2", "concept_ids": ["m2-2-03"],
    "schema_id": SCHEMA_PAR, "schema_name": "평행사변형 대각 크기 비율 응용 / 대변·대각선 길이 / 이등분선 / 내부 점 분할 넓이",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 6.1~6.2)을 참고해 새로 씀. 둘레·변(t2)은 모르는 변의 라벨 수치를 0으로 두어 숨기고 행 문자열 'x'를 겹쳐 그린다. 대각선(t3)의 꼭짓점은 평행사변형 법칙(AC² + BD² = 2(AB² + BC²))으로 BC를 계산해 정확히 배치. 이등분선(t4)은 (변형 × 도형 요소) 행 선택.",
    "geometry": True,
    "templates": [par_t1(), par_t2(), par_t3(), par_t4(), par_t5()],
}



# ═══════════════════════════════════════════════════════════════════ 2. 여러 가지 사각형
SQ = dict(prereq=["직사각형·마름모·정사각형·등변사다리꼴의 뜻과 대각선의 성질", "이등변삼각형의 두 밑각은 같다"], ops=["각도"], tags=["직사각형", "마름모", "정사각형", "등변사다리꼴", "대각선"])


def sq_t1():
    rows = {"AOB": {"XQ": "AOB", "XA": "O", "XF": "A", "XT": "B", "isAOB": 1, "isOAB": 0, "isBOC": 0, "LAW": "∠AOB = 180° − ∠BOC (평각)", "F1": "∠AOB = 180° − ", "F2": "°"},
            "OAB": {"XQ": "OAB", "XA": "A", "XF": "O", "XT": "B", "isAOB": 0, "isOAB": 1, "isBOC": 0, "LAW": "∠OAB = ∠OBA = 90° − ∠OBC", "F1": "∠OAB = 90° − ", "F2": "°"},
            "BOC": {"XQ": "BOC", "XA": "O", "XF": "B", "XT": "C", "isAOB": 0, "isOAB": 0, "isBOC": 1, "LAW": "△OBC의 내각의 합", "F1": "∠BOC = 180° − 2 × ", "F2": "°"}}
    pts = {"A": [0, "{h}"], "B": [0, 0], "C": [6, 0], "D": [6, "{h}"], "O": [3, "{h/2}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["A", "C"], ["B", "D"]]
    marks = {"arc": [arc("B", "O", "C", "{t}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    olab = [{"at": "O", "text": "O", "dx": 0, "dy": -10, "k": "lbl:O"}]
    return tpl("m2-2-special-quad", 1, SQ,
        title="직사각형의 대각선 — 교점에서 생기는 이등변삼각형의 각",
        skill="두 대각선의 길이가 같고 서로를 이등분하므로 OB = OC인 이등변삼각형에서 각 구하기",
        variant_axis={"구하는 것": "∠AOB / ∠OAB / ∠BOC", "∠OBC": "20°~40°"},
        discriminates="OA = OB = OC = OD(대각선의 성질)에서 이등변삼각형을 읽는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"int": [18, 42]}}],
        table={"key": "w", "rows": rows},
        derive={"aob": "2*t", "oab": "90 - t", "boc": "180 - 2*t", "ans_v": "2*t*isAOB + (90 - t)*isOAB + (180 - 2*t)*isBOC", "gv2": "t*isOAB + (180 - 2*t)*isAOB + t*isBOC",
                "h": "6*tan(pi*t/180)"},
        constraints=["ans_v != t"],
        cost_values=["t", "aob", "oab", "boc", "ans_v"],
        answer_var="ans_v",
        verify=["aob + boc == 180", "oab + t == 90", "(isAOB == 1 and ans == aob) or (isOAB == 1 and ans == oab) or (isBOC == 1 and ans == boc)"],
        question="다음 그림의 직사각형 ABCD에서 두 대각선의 교점을 O라고 하자. [[angle(OBC)]] = [[deg({t})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=olab),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="직사각형의 두 대각선은 길이가 같고 서로 다른 것을 이등분하므로 OA = OB = OC = OD다. 그래서 △OBC는 OB = OC인 이등변삼각형이라 ∠OCB = ∠OBC = {t}°이고, ∠BOC = 180° − 2 × {t}° = {boc}°, 평각에서 ∠AOB = {aob}°, △OAB도 이등변삼각형이라 ∠OAB = ∠OBA = 90° − {t}° = {oab}°다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["O", "A"], ["O", "B"], ["O", "C"], ["O", "D"]]]},
                       labels=olab + [{"at": "C", "text": "{t}°", "dx": -28, "dy": -10, "accent": True, "k": "lbl:c"}, {"at": "O", "text": "{boc}°", "dx": 0, "dy": 22, "accent": True, "k": "lbl:boc"}]),
        sol1_anim=[[hl("eq:O-A", "eq:O-B", "eq:O-C", "eq:O-D", keep=True)], [hl("arc:given", "lbl:c", keep=True)], [hl("lbl:boc", "arc:ask")]],
        sol2=[
            "직사각형의 대각선은 길이가 같고 서로를 이등분하므로 OA = OB = OC = OD",
            "△OBC는 이등변삼각형이므로 ∠OCB = ∠OBC = {t}°, ∠BOC = 180° − 2 × {t}° = {boc}°",
            "평각에서 ∠AOB = 180° − {boc}° = {aob}°, △OAB에서 ∠OAB = ∠OBA = 90° − {t}° = {oab}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "OA = OB = OC = OD", "hint": "직사각형의 대각선"}, {"text": "∠OCB = {t}°, ∠BOC = {boc}°", "hint": "이등변삼각형 OBC"}, {"text": "∠AOB = {aob}°, ∠OAB = {oab}°", "hint": "평각·이등변삼각형 OAB"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="∠OBA + ∠OBC = {oab}° + {t}° = 90° = ∠ABC로 직사각형의 한 내각과 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="직사각형의 두 대각선은 길이가 같고 서로 다른 것을 이등분하므로 OA = OB = OC = OD이다. △OBC에서 ∠OCB = ∠OBC = {t}°, ∠BOC = {boc}°이고, ∠AOB = 180° − {boc}° = {aob}°, ∠OAB = 90° − {t}° = {oab}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "대각선의 성질", "points": 3, "criterion": "OA = OB = OC = OD에서 △OBC(△OAB)가 이등변삼각형임을 밝혔다.", "partial": "OB = OC만 쓰고 근거가 없으면 1점."},
            {"element": "각의 계산", "points": 2, "criterion": "{F1}{gv2}{F2} = {ans_v}°를 계산했다.", "partial": "밑각을 잘못 잡았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
    )


def sq_t2():
    rows = {"OCB": {"XQ": "OCB", "XA": "C", "XF": "O", "XT": "B", "i1": 1, "i2": 0, "i3": 0, "F1": "∠OCB = 90° − ", "F2": "°", "LAW": "AC ⊥ BD"},
            "ABC": {"XQ": "ABC", "XA": "B", "XF": "A", "XT": "C", "i1": 0, "i2": 1, "i3": 0, "F1": "∠ABC = 2 × ", "F2": "°", "LAW": "BD가 ∠B를 이등분"},
            "BAD": {"XQ": "BAD", "XA": "A", "XF": "B", "XT": "D", "i1": 0, "i2": 0, "i3": 1, "F1": "∠BAD = 180° − 2 × ", "F2": "°", "LAW": "이웃한 두 내각의 합 180°"}}
    pts = {"A": [0, "{h}"], "B": [-4, 0], "C": [0, "{-h}"], "D": [4, 0], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["A", "C"], ["B", "D"]]
    marks = {"arc": [arc("B", "O", "C", "{t}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")], "right": [["B", "O", "C"]]}
    olab = [{"at": "O", "text": "O", "dx": 12, "dy": -8, "k": "lbl:O"}]
    return tpl("m2-2-special-quad", 2, SQ,
        title="마름모의 대각선 — 수직이등분과 각의 이등분",
        skill="마름모의 두 대각선은 서로 다른 것을 수직이등분하고 내각을 이등분함을 써서 각 구하기",
        variant_axis={"구하는 것": "∠OCB / ∠ABC / ∠BAD", "∠OBC": "20°~60°"},
        discriminates="AC ⊥ BD(∠BOC = 90°)와 대각선이 내각을 이등분함을 함께 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"int": [20, 60]}}],
        table={"key": "w", "rows": rows},
        derive={"ocb": "90 - t", "abc": "2*t", "bad": "180 - 2*t", "ans_v": "(90 - t)*i1 + 2*t*i2 + (180 - 2*t)*i3", "h": "4*tan(pi*t/180)"},
        constraints=["ans_v != t", "t != 45"],
        cost_values=["t", "ocb", "abc", "bad", "ans_v"],
        answer_var="ans_v",
        verify=["ocb + t == 90", "abc + bad == 180", "(i1 == 1 and ans == ocb) or (i2 == 1 and ans == abc) or (i3 == 1 and ans == bad)"],
        question="다음 그림의 마름모 ABCD에서 두 대각선의 교점을 O라고 하자. [[angle(OBC)]] = [[deg({t})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=olab),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="마름모는 네 변의 길이가 같은 평행사변형이다. 두 대각선은 서로 다른 것을 수직이등분하므로 ∠BOC = 90°이고, 각 대각선은 내각을 이등분한다(△ABC가 AB = BC인 이등변삼각형이고 BO가 그 꼭지각의 이등분선). 그래서 △OBC에서 ∠OCB = 90° − {t}°, ∠ABC = 2 × ∠OBC, ∠BAD = 180° − ∠ABC다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]]], "arc": marks["arc"] + [arc("B", "A", "O", "{t}°", "arc:b2")]},
                       labels=olab + [{"at": "C", "text": "{ocb}°", "dx": -26, "dy": -6, "accent": True, "k": "lbl:c"}]),
        sol1_anim=[[hl("right:O", keep=True)], [hl("arc:given", "arc:b2", keep=True)], [hl("lbl:c", "arc:ask")]],
        sol2=[
            "마름모의 두 대각선은 서로 다른 것을 수직이등분하므로 ∠BOC = 90°, 따라서 ∠OCB = 90° − {t}° = {ocb}°",
            "AB = BC이므로 BD는 ∠B를 이등분한다: ∠ABC = 2 × {t}° = {abc}°",
            "이웃한 두 내각의 합은 180°이므로 ∠BAD = 180° − {abc}° = {bad}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠BOC = 90° → ∠OCB = {ocb}°", "hint": "대각선이 수직"}, {"text": "∠ABC = 2 × {t}° = {abc}°", "hint": "대각선이 내각을 이등분"}, {"text": "∠BAD = 180° − {abc}° = {bad}°", "hint": "이웃한 내각의 합"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="△OBC의 세 각 {t}° + {ocb}° + 90° = 180°이고, ∠ABC + ∠BAD = {abc}° + {bad}° = 180°로 평행사변형의 이웃한 두 내각의 합과 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="마름모의 두 대각선은 서로 다른 것을 수직이등분하므로 ∠BOC = 90°이고 ∠OCB = 90° − {t}° = {ocb}°이다. 또 BD는 ∠B를 이등분하므로 ∠ABC = {abc}°이고, ∠BAD = 180° − {abc}° = {bad}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "대각선의 성질", "points": 3, "criterion": "AC ⊥ BD와 대각선이 내각을 이등분함(또는 AB = BC인 이등변삼각형)을 밝혔다.", "partial": "둘 중 하나만 썼으면 1점."},
            {"element": "각의 계산", "points": 2, "criterion": "{F1}{t}{F2} = {ans_v}°를 계산했다.", "partial": "∠BOC를 90°로 두지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
    )


def sq_t3():
    rows = {"BEC": {"XQ": "BEC", "XA": "E", "XF": "B", "XT": "C", "isE": 1, "F1": "∠BEC = 180° − 45° − (90° − ", "F2": "°)", "LAW": "△BCE의 내각의 합"},
            "BCE": {"XQ": "BCE", "XA": "C", "XF": "B", "XT": "E", "isE": 0, "F1": "∠BCE = ∠BAE = 90° − ", "F2": "°", "LAW": "합동인 두 삼각형의 대응각"}}
    pts = {"A": [0, 4], "B": [0, 0], "C": [4, 0], "D": [4, 4], "E": ["{ex}", "{ex}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["B", "D"], ["A", "E"], ["C", "E"]]
    marks = {"arc": [arc("A", "E", "D", "{a}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-special-quad", 3, SQ,
        title="정사각형의 대각선 위의 점 — 합동인 두 삼각형의 각",
        skill="△ABE ≡ △CBE(SAS)임을 써서 대응각을 옮기고 삼각형의 내각의 합으로 각 구하기",
        variant_axis={"구하는 것": "∠BEC / ∠BCE", "∠DAE": "10°~40°"},
        discriminates="대각선 BD가 ∠B를 이등분(45°)하고 AB = CB이므로 △ABE ≡ △CBE임을 밝히는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        prereq=["정사각형의 대각선은 내각을 이등분한다(45°)", "삼각형의 합동 조건 SAS", "삼각형의 내각의 합 180°"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"int": [10, 40]}}],
        table={"key": "w", "rows": rows},
        derive={"bae": "90 - a", "bec": "45 + a", "ans_v": "(45 + a)*isE + (90 - a)*(1 - isE)", "be": "4*cos(pi*a/180)/sin(pi*(45 + a)/180)", "ex": "be*sin(pi/4)"},
        constraints=["ans_v != a", "bae != bec"],
        cost_values=["a", "bae", "bec", "ans_v"],
        answer_var="ans_v",
        verify=["bae + a == 90", "bec == 45 + a", "(isE == 1 and ans == bec) or (isE == 0 and ans == bae)"],
        question="다음 그림과 같이 정사각형 ABCD의 대각선 BD 위에 한 점 E를 잡았다. [[angle(DAE)]] = [[deg({a})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="정사각형의 대각선 BD는 ∠B를 이등분하므로 ∠ABE = ∠CBE = 45°다. △ABE와 △CBE에서 AB = CB, ∠ABE = ∠CBE, BE는 공통이므로 두 삼각형은 SAS 합동 — 대응각이 같아 ∠BCE = ∠BAE, ∠BEC = ∠BEA다. ∠BAE = 90° − {a}°이고, △ABE의 내각의 합에서 ∠BEA가 나온다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["A", "B"], ["C", "B"]]], "arc": marks["arc"] + [arc("B", "E", "A", "45°", "arc:b1"), arc("B", "C", "E", "45°", "arc:b2")]},
                       labels=[{"at": "A", "text": "{bae}°", "dx": 14, "dy": 26, "accent": True, "k": "lbl:bae"}]),
        sol1_anim=[[hl("arc:b1", "arc:b2", "eq:A-B", "eq:C-B", keep=True)], [hl("arc:given", "lbl:bae", keep=True)], [hl("arc:ask")]],
        sol2=[
            "대각선 BD는 ∠B를 이등분하므로 ∠ABE = ∠CBE = 45°",
            "△ABE와 △CBE에서 AB = CB, ∠ABE = ∠CBE, BE는 공통 → △ABE ≡ △CBE (SAS 합동)",
            "∠BAE = 90° − {a}° = {bae}°이고, 대응각이므로 ∠BCE = ∠BAE = {bae}°",
            "△BCE에서 ∠BEC = 180° − 45° − {bae}° = {bec}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠ABE = ∠CBE = 45°", "hint": "정사각형의 대각선"}, {"text": "△ABE ≡ △CBE", "hint": "SAS 합동"}, {"text": "∠BCE = ∠BAE = {bae}°", "hint": "대응각"}, {"text": "∠BEC = 180° − 45° − {bae}° = {bec}°", "hint": "내각의 합"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], []],
        sol_check="∠BEC = {bec}°는 △ABE의 외각으로도 확인된다: ∠BEC = ∠BEA는 △ADE 쪽 ∠AED의 보각이고, ∠AED = 180° − {a}° − 45° = {135 - a}°이므로 ∠BEA = {45 + a}°다. 답은 [[deg({ans_v})]]다.",
        model_answer="정사각형의 대각선 BD는 ∠B를 이등분하므로 ∠ABE = ∠CBE = 45°이다. △ABE와 △CBE는 AB = CB, ∠ABE = ∠CBE, BE 공통이므로 SAS 합동이고 ∠BCE = ∠BAE = 90° − {a}° = {bae}°이다. △BCE에서 ∠BEC = 180° − 45° − {bae}° = {bec}°이므로 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "합동 밝히기", "points": 3, "criterion": "∠ABE = ∠CBE = 45°와 AB = CB, BE 공통에서 △ABE ≡ △CBE(SAS)임을 밝혔다.", "partial": "합동이라고만 쓰고 조건을 밝히지 않았으면 1점."},
            {"element": "각의 계산", "points": 2, "criterion": "∠BAE = {bae}°를 구하고 {F1}{a}{F2} = {ans_v}°를 계산했다.", "partial": "대응각을 잘못 짝지었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


def sq_t4():
    rows = {"bc": {"Q": "[[seg(BC)]]의 길이", "isBC": 1, "isAD": 0, "isP": 0, "uAD": 0, "XAD": "", "XBC": "x", "G2T": "[[seg(AD)]] = ", "F1": "BC = BE + EC = AB + AD = ", "F2": " + ", "F3": "", "LAW": "BE = AB, EC = AD"},
            "ad": {"Q": "[[seg(AD)]]의 길이", "isBC": 0, "isAD": 1, "isP": 0, "uAD": 1, "XAD": "x", "XBC": "", "G2T": "[[seg(BC)]] = ", "F1": "AD = EC = BC − BE = ", "F2": " − ", "F3": "", "LAW": "BE = AB"},
            "perim": {"Q": "□ABCD의 둘레의 길이", "isBC": 0, "isAD": 0, "isP": 1, "uAD": 0, "XAD": "", "XBC": "", "G2T": "[[seg(AD)]] = ", "F1": "둘레 = 3 × ", "F2": " + 2 × ", "F3": "", "LAW": "AB + BC + CD + DA = 3AB + 2AD"}}
    pts = {"A": ["{a/2}", "{ay}"], "B": [0, 0], "C": ["{a + d}", 0], "D": ["{a/2 + d}", "{ay}"]}
    segs = [lseg("A", "B", "{a} cm"), lseg("B", "C", "{lc}"), ["C", "D"], lseg("D", "A", "{ld}"), lseg("B", "C", "{XBC}"), lseg("D", "A", "{XAD}")]
    marks = {"arc": [arc("B", "C", "A", "60°", "arc:b")], "eq": [[["A", "B"], ["D", "C"]]]}
    return tpl("m2-2-special-quad", 4, SQ,
        title="등변사다리꼴 — 한 각이 60°일 때 변의 길이·둘레",
        skill="한 꼭짓점에서 다른 변에 평행한 선을 그어 평행사변형과 정삼각형으로 나누기",
        variant_axis={"구하는 것": "BC / AD / 둘레", "AB": "3~8", "AD": "2~10"},
        discriminates="AE ∥ DC를 그어 EC = AD, AE = AB이고 △ABE가 정삼각형임을 읽는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=100, process="문제해결",
        prereq=["등변사다리꼴: 평행하지 않은 두 변의 길이가 같고 밑각이 같다", "평행사변형의 대변", "정삼각형"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"int": [3, 8]}}, {"name": "d", "values": {"int": [2, 10]}}],
        table={"key": "w", "rows": rows},
        derive={"bc": "a + d", "P": "3*a + 2*d", "ans_v": "(a + d)*isBC + d*isAD + (3*a + 2*d)*isP", "g2": "d*(1 - uAD) + (a + d)*uAD",
                "lc": "(a + d)*isAD", "ld": "d*(1 - uAD)", "v1": "a*(isBC + isP) + (a + d)*isAD", "v2": "d*(isBC + isP) + a*isAD", "ay": "a*sin(pi*60/180)"},
        constraints=["a != d", "ans_v != a", "2*a != d"],
        cost_values=["a", "d", "bc", "ans_v"],
        answer_var="ans_v",
        verify=["bc == a + d", "(isBC == 1 and ans == bc) or (isAD == 1 and ans == d) or (isP == 1 and ans == P)"],
        question="다음 그림과 같이 [[seg(AD)]] ∥ [[seg(BC)]]인 등변사다리꼴 ABCD에서 [[angle(B)]] = [[deg(60)]], [[seg(AB)]] = {a} cm, {G2T}{g2} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="점 A를 지나고 DC에 평행한 직선이 BC와 만나는 점을 E라 하자. AD ∥ EC, AE ∥ DC이므로 □AECD는 평행사변형 — EC = AD, AE = DC = AB(등변사다리꼴)다. △ABE는 AB = AE이고 ∠B = 60°이므로 정삼각형이라 BE = AB = {a} cm. 그러므로 BC = BE + EC = AB + AD다.",
        sol1_fig=scene({**pts, "E": ["{a}", 0]}, [lseg("A", "B", "{a} cm"), ["B", "C"], ["C", "D"], ["D", "A"], {"a": "A", "b": "E", "dash": True}],
                       marks={"arc": [arc("B", "C", "A", "60°", "arc:b"), arc("E", "A", "B", "60°", "arc:e"), arc("A", "B", "E", "60°", "arc:a")], "eq": [[["A", "B"], ["D", "C"], ["A", "E"], ["B", "E"]], [["A", "D"], ["E", "C"]]]},
                       labels=[{"at": "E", "text": "{a} cm", "dx": -24, "dy": 16, "accent": True, "k": "lbl:be"}, {"at": ["{a + d/2}", 0], "text": "{d} cm", "dx": 0, "dy": 16, "accent": True, "k": "lbl:ec"}]),
        sol1_anim=[[hl("seg:A-E", keep=True)], [hl("eq:A-D", "eq:E-C", "lbl:ec", keep=True)], [hl("arc:a", "arc:e", "arc:b", "eq:A-E", "eq:B-E", "lbl:be", keep=True)]],
        sol2=[
            "A를 지나고 DC에 평행한 직선이 BC와 만나는 점을 E라 하면 □AECD는 평행사변형: EC = AD, AE = DC = AB = {a} cm",
            "△ABE는 AB = AE, ∠B = 60°이므로 정삼각형: BE = {a} cm",
            "{F1}{v1}{F2}{v2}{F3} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "EC = AD, AE = AB = {a}", "hint": "□AECD 평행사변형"}, {"text": "BE = {a}", "hint": "△ABE 정삼각형 (60°)"}, {"text": "{F1}{v1}{F2}{v2}{F3} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AB = {a} cm, AD = {d} cm이면 BC = {a} + {d} = {a + d}(cm), 둘레 = {a} + {a + d} + {a} + {d} = {P}(cm)로 서로 맞는다. 답은 {ans_v} cm다.",
        model_answer="A를 지나고 DC에 평행한 직선이 BC와 만나는 점을 E라 하면 □AECD는 평행사변형이므로 EC = AD, AE = DC = AB = {a} cm이다. △ABE는 AB = AE이고 ∠B = 60°이므로 정삼각형이고 BE = {a} cm이다. {F1}{v1}{F2}{v2}{F3} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "보조선·평행사변형", "points": 3, "criterion": "AE ∥ DC를 그어 EC = AD, AE = AB임을 밝혔다.", "partial": "보조선만 긋고 길이를 옮기지 못했으면 1점."},
            {"element": "정삼각형", "points": 2, "criterion": "△ABE가 정삼각형이므로 BE = AB = {a} cm임을 썼다.", "partial": "BE = {a} cm만 쓰고 근거가 없으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def sq_t5():
    rows = {"area": {"Q": "마름모 ABCD의 넓이", "isA": 1, "U": " cm²", "UA": "cm²", "XBD": "", "G2T": "[[seg(BD)]] = ", "G2U": " cm", "F1": "넓이 = [[frac(1, 2)]] × ", "F2": " × ", "LAW": "[[frac(1, 2)]] × (두 대각선의 곱)"},
            "bd": {"Q": "[[seg(BD)]]의 길이", "isA": 0, "U": " cm", "UA": "cm", "XBD": "x", "G2T": "넓이가 ", "G2U": " cm²", "F1": "BD = 2 × (넓이) ÷ AC = 2 × ", "F2": " ÷ ", "LAW": "넓이 = [[frac(1, 2)]] × AC × BD"}}
    pts = {"A": [0, "{p}"], "B": ["{-q}", 0], "C": [0, "{-p}"], "D": ["{q}", 0], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], lseg("A", "O", "{2*p}"), ["O", "C"], ["B", "O"], lseg("O", "D", "{lbd}"), lseg("O", "D", "{XBD}")]
    marks = {"right": [["A", "O", "D"]]}
    return tpl("m2-2-special-quad", 5, SQ,
        title="마름모의 넓이 — 두 대각선의 곱의 절반",
        skill="대각선이 서로 수직이므로 마름모가 네 직각삼각형으로 나뉨을 써서 넓이 = ½ × AC × BD",
        variant_axis={"구하는 것": "넓이 / BD", "대각선": "4~16"},
        discriminates="대각선이 수직임을 근거로 넓이를 ½ × (대각선의 곱)으로 세우는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        prereq=["마름모의 대각선은 서로 다른 것을 수직이등분한다", "삼각형의 넓이"], ops=["넓이", "방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "p", "values": {"int": [2, 8]}}, {"name": "q", "values": {"int": [2, 8]}}],
        table={"key": "w", "rows": rows},
        derive={"S": "2*p*q", "ans_v": "2*p*q*isA + 2*q*(1 - isA)", "g2": "2*q*isA + 2*p*q*(1 - isA)", "lbd": "2*q*isA", "v1": "2*p*isA + 2*p*q*(1 - isA)", "v2": "2*q*isA + 2*p*(1 - isA)"},
        constraints=["p != q", "ans_v != 2*p", "ans_v != g2"],
        cost_values=["p", "q", "S", "ans_v"],
        answer_var="ans_v",
        verify=["S == 2*p*q", "(isA == 1 and ans == S) or (isA == 0 and ans == 2*q)"],
        question="다음 그림의 마름모 ABCD에서 [[seg(AC)]] = {2*p} cm이고 {G2T}{g2}{G2U}일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="마름모의 두 대각선은 서로 다른 것을 수직이등분한다. 그래서 마름모는 대각선에 의해 합동인 네 직각삼각형으로 나뉘고, 넓이는 [[frac(1, 2)]] × AC × BD — 대각선이 수직인 사각형의 넓이 공식이다.",
        sol1_fig=scene(pts, [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], lseg("A", "O", "{2*p}"), ["O", "C"], ["B", "O"], lseg("O", "D", "{2*q}")], marks={"right": [["A", "O", "D"], ["A", "O", "B"], ["C", "O", "B"], ["C", "O", "D"]]},
                       shade=[["A", "O", "D"], ["C", "O", "B"]]),
        sol1_anim=[[hl("right:O", keep=True)], [hl("shade:0", "shade:1", "seglbl:A-O", "seglbl:O-D")]],
        sol2=[
            "마름모의 두 대각선은 서로 다른 것을 수직이등분한다: AC ⊥ BD",
            "대각선이 수직이므로 넓이 = [[frac(1, 2)]] × AC × BD",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "AC ⊥ BD", "hint": "마름모의 대각선"}, {"text": "넓이 = [[frac(1, 2)]] × AC × BD", "hint": "네 직각삼각형"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AC = {2*p} cm, BD = {2*q} cm이면 넓이는 [[frac(1, 2)]] × {2*p} × {2*q} = {S}(cm²)로 서로 맞는다. 답은 {ans_v}{U}다.",
        model_answer="마름모의 두 대각선은 서로 수직이므로 넓이 = [[frac(1, 2)]] × AC × BD이다. {F1}{v1}{F2}{v2} = {ans_v}이므로 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "대각선 수직", "points": 3, "criterion": "AC ⊥ BD를 근거로 넓이 = [[frac(1, 2)]] × AC × BD를 세웠다.", "partial": "공식만 쓰고 근거가 없으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "[[frac(1, 2)]]을 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


SQ_SEED = {
    "seed_id": "m2-2-special-quad", "category": "도형",
    "title": "여러 가지 사각형 — 직사각형·마름모의 대각선, 정사각형 대각선 위의 점, 등변사다리꼴, 마름모의 넓이",
    "unit_id": "m2-2", "concept_ids": ["m2-2-04"],
    "schema_id": SCHEMA_SQ, "schema_name": "직사각형·마름모·정사각형·등변사다리꼴의 성질 활용",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 6.3)을 참고해 새로 씀. 직사각형·마름모는 ∠OBC에서 높이를 tan으로 계산해 실제 각으로 그린다. 정사각형 위의 점 E는 사인법칙으로 BE를 구해 대각선 위에 정확히 놓는다. 등변사다리꼴·마름모 넓이는 모르는 변 라벨 0(숨김) + 'x'.",
    "geometry": True,
    "templates": [sq_t1(), sq_t2(), sq_t3(), sq_t4(), sq_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 피타고라스 정리
PY = dict(prereq=["피타고라스 정리: 직각삼각형에서 (빗변)² = (다른 두 변의 제곱의 합)"], ops=["제곱", "방정식"], tags=["피타고라스", "직각삼각형"])
PY_TRIPLES = {"345": {"a0": 3, "b0": 4, "c0": 5}, "435": {"a0": 4, "b0": 3, "c0": 5}, "51213": {"a0": 5, "b0": 12, "c0": 13}, "12513": {"a0": 12, "b0": 5, "c0": 13},
              "81517": {"a0": 8, "b0": 15, "c0": 17}, "15817": {"a0": 15, "b0": 8, "c0": 17}, "72425": {"a0": 7, "b0": 24, "c0": 25}, "202129": {"a0": 20, "b0": 21, "c0": 29}}


def py_t1():
    rows = {"AB": {"XS": "AB", "u1": 1, "u2": 0, "u3": 0, "X1": "x", "X2": "", "X3": "", "G1T": "[[seg(BC)]] = ", "G2T": "[[seg(CA)]] = ", "F1": "x² = ", "F2": "² + ", "LAW": "빗변² = 두 변의 제곱의 합"},
            "BC": {"XS": "BC", "u1": 0, "u2": 1, "u3": 0, "X1": "", "X2": "x", "X3": "", "G1T": "[[seg(CA)]] = ", "G2T": "[[seg(AB)]] = ", "F1": "x² = ", "F2": "² − ", "LAW": "변² = 빗변² − 다른 변²"},
            "CA": {"XS": "CA", "u1": 0, "u2": 0, "u3": 1, "X1": "", "X2": "", "X3": "x", "G1T": "[[seg(BC)]] = ", "G2T": "[[seg(AB)]] = ", "F1": "x² = ", "F2": "² − ", "LAW": "변² = 빗변² − 다른 변²"}}
    pts = {"A": [0, "{b}"], "B": ["{a}", 0], "C": [0, 0]}
    segs = [lseg("B", "A", "{lc}"), lseg("C", "B", "{la}"), lseg("A", "C", "{lb}"), lseg("B", "A", "{X1}"), lseg("C", "B", "{X2}"), lseg("A", "C", "{X3}")]
    marks = {"right": [["A", "C", "B"]]}
    return tpl("m2-2-pythagoras", 1, PY,
        title="피타고라스 정리 — 두 변에서 나머지 한 변 구하기",
        skill="빗변을 구별해 (빗변)² = (두 변)²의 합을 세우고 제곱수에서 길이 읽기",
        variant_axis={"구하는 것": "AB(빗변) / BC / CA", "세 변": "피타고라스 수 8종 × 1~3배"},
        discriminates="빗변(직각의 대변)을 바르게 놓고 더할지 뺄지 판단하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"in": list(PY_TRIPLES)}}, {"name": "k", "values": {"int": [1, 3]}}],
        table=[{"key": "w", "rows": rows}, {"key": "t", "rows": PY_TRIPLES}],
        derive={"a": "k*a0", "b": "k*b0", "c": "k*c0", "ans_v": "c*u1 + a*u2 + b*u3", "sq": "ans_v*ans_v",
                "la": "a*(1 - u2)", "lb": "b*(1 - u3)", "lc": "c*(1 - u1)", "g1": "a*(u1 + u3) + b*u2", "g2": "b*u1 + c*(u2 + u3)",
                "v1": "a*u1 + c*(u2 + u3)", "v2": "b*(u1 + u2) + a*u3"},
        constraints=["a != b"],
        cost_values=["a", "b", "c", "ans_v"],
        answer_var="ans_v",
        verify=["a*a + b*b == c*c", "(u1 == 1 and ans == c) or (u2 == 1 and ans == a) or (u3 == 1 and ans == b)"],
        question="다음 그림과 같이 [[angle(C)]] = [[deg(90)]]인 직각삼각형 ABC에서 {G1T}{g1} cm, {G2T}{g2} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="∠C = 90°이므로 빗변은 직각의 대변인 AB다. 피타고라스 정리 AB² = BC² + CA²에서 두 변을 알면 나머지 한 변의 제곱이 나온다 — 빗변을 구할 때는 더하고, 다른 변을 구할 때는 빗변의 제곱에서 뺀다. 길이는 양수이므로 제곱이 {sq}인 양수 {ans_v}를 읽는다.",
        sol1_fig=scene(pts, [lseg("B", "A", "{c}"), lseg("C", "B", "{a}"), lseg("A", "C", "{b}")], marks=marks,
                       labels=[{"at": ["{a/2}", "{b/2}"], "text": "빗변", "dx": 10, "dy": -8, "accent": True, "k": "lbl:hyp"}]),
        sol1_anim=[[hl("right:C", keep=True)], [hl("seg:B-A", "lbl:hyp", keep=True)], [hl("seglbl:B-A", "seglbl:C-B", "seglbl:A-C")]],
        sol2=[
            "∠C = 90°이므로 빗변은 AB: AB² = BC² + CA² (피타고라스 정리)",
            "{XS} = x cm라 하면 {F1}{v1}{F2}{v2}² = {sq}",
            "x > 0이므로 x = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AB² = BC² + CA²", "hint": "빗변은 AB"}, {"text": "{F1}{v1}{F2}{v2}² = {sq}", "hint": "{LAW}"}, {"text": "x = {ans_v}", "hint": "{ans_v}² = {sq}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="세 변 {a}, {b}, {c}에 대해 {a}² + {b}² = {a*a} + {b*b} = {c*c} = {c}²이 성립한다. 답은 {ans_v} cm다.",
        model_answer="∠C = 90°이므로 AB² = BC² + CA²이다. {XS} = x cm라 하면 {F1}{v1}{F2}{v2}² = {sq}이고 x > 0이므로 x = {ans_v}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "정리 적용", "points": 3, "criterion": "빗변 AB를 바르게 놓고 AB² = BC² + CA²를 세웠다.", "partial": "빗변을 잘못 놓았으면 인정하지 않는다."},
            {"element": "제곱 계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2}² = {sq}{eul(sq)} 계산했다.", "partial": "계산 실수가 있으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "x > 0에서 {XS} = {ans_v} cm를 답했다.", "partial": "제곱한 값 {sq}{eul(sq)} 답했으면 인정하지 않는다."},
        ],
    )


def py_t2():
    rows = {"c": {"XS": "AB", "uA": 0, "uB": 0, "uC": 1, "G1P": "Qa", "G2P": "Qb", "S1": "A", "S2": "B", "S3": "P2", "S4": "P1", "F1": "(AB 위의 정사각형) = ", "F2": " + ", "LAW": "빗변 위 정사각형 = 두 변 위 정사각형의 합"},
            "a": {"XS": "BC", "uA": 1, "uB": 0, "uC": 0, "G1P": "Qb", "G2P": "Qc", "S1": "B", "S2": "C", "S3": "Q1", "S4": "Q2", "F1": "(BC 위의 정사각형) = ", "F2": " − ", "LAW": "빗변 위 정사각형 − 다른 변 위 정사각형"},
            "b": {"XS": "CA", "uA": 0, "uB": 1, "uC": 0, "G1P": "Qa", "G2P": "Qc", "S1": "C", "S2": "A", "S3": "R2", "S4": "R1", "F1": "(CA 위의 정사각형) = ", "F2": " − ", "LAW": "빗변 위 정사각형 − 다른 변 위 정사각형"}}
    pts = {"A": [0, "{b}"], "B": ["{a}", 0], "C": [0, 0], "P1": ["{b}", "{a + b}"], "P2": ["{a + b}", "{a}"], "Q1": [0, "{-a}"], "Q2": ["{a}", "{-a}"], "R1": ["{-b}", 0], "R2": ["{-b}", "{b}"],
           "Qa": ["{a/2}", "{-a/2}"], "Qb": ["{-b/2}", "{b/2}"], "Qc": ["{(a + b)/2}", "{(a + b)/2}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["A", "P1"], ["P1", "P2"], ["P2", "B"], ["C", "Q1"], ["Q1", "Q2"], ["Q2", "B"], ["C", "R1"], ["R1", "R2"], ["R2", "A"]]
    marks = {"right": [["A", "C", "B"]]}
    labels = [{"at": "{G1P}", "text": "{g1} cm²", "dx": 0, "dy": 4, "k": "lbl:g1"}, {"at": "{G2P}", "text": "{g2} cm²", "dx": 0, "dy": 4, "k": "lbl:g2"}]
    aux = ["P1", "P2", "Q1", "Q2", "R1", "R2", "Qa", "Qb", "Qc"]
    return tpl("m2-2-pythagoras", 2, PY,
        title="세 변 위의 정사각형 — 넓이의 합",
        skill="정사각형의 넓이가 변의 제곱이므로 피타고라스 정리가 넓이의 관계(빗변 위 = 두 변 위의 합)로 읽힘을 쓰기",
        variant_axis={"구하는 것": "AB 위 / BC 위 / CA 위 정사각형", "세 변": "피타고라스 수 8종 × 1~2배"},
        discriminates="정사각형의 넓이를 변의 제곱으로 읽어 더하거나 빼는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"in": list(PY_TRIPLES)}}, {"name": "k", "values": {"int": [1, 2]}}],
        table=[{"key": "w", "rows": rows}, {"key": "t", "rows": PY_TRIPLES}],
        derive={"a": "k*a0", "b": "k*b0", "c": "k*c0", "Sa": "a*a", "Sb": "b*b", "Sc": "c*c", "ans_v": "a*a*uA + b*b*uB + c*c*uC",
                "g1": "a*a*(uC + uB) + b*b*uA", "g2": "b*b*uC + c*c*(uA + uB)", "v1": "a*a*uC + c*c*(uA + uB)", "v2": "b*b*(uC + uA) + a*a*uB"},
        constraints=["a != b", "a + b <= 40"],
        cost_values=["Sa", "Sb", "Sc", "ans_v"],
        answer_var="ans_v",
        verify=["Sa + Sb == Sc", "(uC == 1 and ans == Sc) or (uA == 1 and ans == Sa) or (uB == 1 and ans == Sb)"],
        question="다음 그림은 [[angle(C)]] = [[deg(90)]]인 직각삼각형 ABC의 세 변을 각각 한 변으로 하는 정사각형을 그린 것이다. 두 정사각형의 넓이가 각각 {g1} cm², {g2} cm²일 때, [[seg({XS})]]를 한 변으로 하는 색칠한 정사각형의 넓이를 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=labels, nodot=aux, shade=[["{S1}", "{S2}", "{S3}", "{S4}"]]),
        answer="{ans_v}", answer_alt=["{ans_v} cm²"],
        sol1="한 변의 길이가 ℓ인 정사각형의 넓이는 ℓ²이므로 세 정사각형의 넓이는 BC², CA², AB²다. ∠C = 90°이므로 피타고라스 정리 AB² = BC² + CA²는 곧 (빗변 AB 위의 정사각형) = (BC 위의 정사각형) + (CA 위의 정사각형)이라는 넓이의 관계다.",
        sol1_fig=scene(pts, segs, marks=marks, labels=[{"at": "Qa", "text": "BC² = {Sa}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:a"}, {"at": "Qb", "text": "CA² = {Sb}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:b"}, {"at": "Qc", "text": "AB² = {Sc}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:c"}],
                       nodot=aux, shade=[["{S1}", "{S2}", "{S3}", "{S4}"]]),
        sol1_anim=[[hl("right:C", keep=True)], [hl("lbl:a", "lbl:b", keep=True)], [hl("lbl:c", "shade:0")]],
        sol2=[
            "세 정사각형의 넓이는 각각 BC², CA², AB² (변의 제곱)",
            "∠C = 90°이므로 AB² = BC² + CA² — 빗변 위의 정사각형의 넓이는 두 변 위의 정사각형의 넓이의 합",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 색칠한 정사각형의 넓이는 {ans_v} cm²",
        ],
        sol2_fig=steps([{"text": "넓이 = (변)²", "hint": "정사각형"}, {"text": "AB² = BC² + CA²", "hint": "피타고라스 정리"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="세 정사각형의 넓이 {Sa}, {Sb}, {Sc}는 변 {a}, {b}, {c}의 제곱이고 {Sa} + {Sb} = {Sc}가 성립한다. 답은 {ans_v} cm²다.",
        model_answer="정사각형의 넓이는 변의 제곱이므로 세 정사각형의 넓이는 BC², CA², AB²이다. ∠C = 90°이므로 AB² = BC² + CA²이고, {F1}{v1}{F2}{v2} = {ans_v}이다. 따라서 색칠한 정사각형의 넓이는 {ans_v} cm²다.",
        rubric=[
            {"element": "넓이 = 제곱", "points": 3, "criterion": "정사각형의 넓이가 변의 제곱이므로 AB² = BC² + CA²가 넓이의 관계임을 밝혔다.", "partial": "피타고라스 정리만 쓰고 넓이와 연결하지 못했으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "더하기·빼기를 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v} cm²를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


_VALID = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (7, 24, 25), (9, 12, 15), (20, 21, 29), (12, 16, 20)]
_INVALID = [(2, 3, 4), (3, 4, 6), (6, 9, 14), (4, 5, 6), (5, 6, 8), (7, 8, 9), (10, 12, 15), (8, 9, 12), (4, 6, 7), (5, 7, 9)]
_KOR = "ABCDE"     # 보기 기호 — mathir 가 한글 자음(ㄱㄴㄷ)을 답으로 받지 못해 A~E 로 쓴다


def judge_rows():
    rows = {}
    seq = []
    for k in (1, 2, 3):
        vs = list(itertools.combinations(range(len(_VALID)), k))
        step = max(1, len(vs) // 12)
        for i, vc in enumerate(vs[::step][:12]):
            iv = [(i + j) % len(_INVALID) for j in range(5 - k)]
            seq.append((k, vc, iv))
    for n, (k, vc, iv) in enumerate(seq):
        tri = [_VALID[i] for i in vc] + [_INVALID[i] for i in iv]
        order = [(j * 3 + n) % 5 for j in range(5)]
        if len(set(order)) < 5:
            order = list(range(5))
        tri = [tri[j] for j in order]
        lst = " ".join(f"{_KOR[i]}. {t[0]}, {t[1]}, {t[2]}" for i, t in enumerate(tri))
        chk = []
        for i, t in enumerate(tri):
            x, y, z = sorted(t)
            ok = x * x + y * y == z * z
            chk.append(f"{_KOR[i]}. {z}² = {z * z}, {x}² + {y}² = {x * x + y * y} → {'○' if ok else '×'}")
        okl = ", ".join(_KOR[i] for i, t in enumerate(tri) if (lambda x, y, z: x * x + y * y == z * z)(*sorted(t)))
        rows[f"r{n}"] = {"LIST": lst, "CHK": "  ".join(chk), "OKL": okl, "OKC": okl.replace(", ", ","), "K": k}
    return rows


JUDGE_ROWS = judge_rows()


def py_t3():
    return tpl("m2-2-pythagoras", 3, PY,
        title="직각삼각형이 되는 세 변의 길이 — 모두 고르기",
        skill="가장 긴 변의 제곱이 나머지 두 변의 제곱의 합과 같은지 하나씩 확인하기",
        variant_axis={"직각삼각형의 개수": "1~3", "보기 조합": "36가지"},
        discriminates="가장 긴 변을 빗변 후보로 두고 제곱을 비교하는가(세 수의 크기 순서에 주의)",
        qtype="short", difficulty=2, pool_target=300, time_limit=100, process="개념이해", figure=[],
        params=[{"name": "r", "values": {"in": list(JUDGE_ROWS)}}],
        table={"key": "r", "rows": JUDGE_ROWS},
        derive={"cnt": "K"},
        constraints=[],
        cost_values=["K"],
        verify=["K >= 1", "K <= 3"],
        question="다음 보기 A~E 중 세 변의 길이가 주어진 값인 삼각형이 직각삼각형이 되는 것을 모두 고르시오. (단위: cm) 보기: {LIST}",
        answer="{OKL}", answer_alt=["{OKC}"],
        sol1="세 변의 길이가 a, b, c(c가 가장 긴 변)인 삼각형은 c² = a² + b²일 때, 그리고 그때만 직각삼각형이다(피타고라스 정리의 역). 보기마다 가장 긴 변의 제곱과 나머지 두 변의 제곱의 합을 비교한다.",
        sol1_fig=steps(["가장 긴 변² = 나머지 두 변의 제곱의 합 → 직각삼각형", "{CHK}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "가장 긴 변을 c로 두고 c² = a² + b²인지 확인한다",
            "{CHK}",
            "직각삼각형이 되는 것은 {OKL}로 {K}개",
        ],
        sol2_fig=steps([{"text": "c² = a² + b² ?", "hint": "c는 가장 긴 변"}, {"text": "○: {OKL}", "hint": "{K}개"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [], [reveal(1), hl("hint:1")]],
        sol_check="○로 표시한 세 수는 모두 가장 긴 변의 제곱이 나머지 제곱의 합과 같고, ×인 것은 같지 않다. 답은 {K}개다.",
        model_answer="가장 긴 변의 제곱이 나머지 두 변의 제곱의 합과 같으면 직각삼각형이다. {CHK} 따라서 직각삼각형이 되는 것은 {OKL}의 {K}개다.",
        rubric=[
            {"element": "판정 기준", "points": 3, "criterion": "가장 긴 변의 제곱과 나머지 두 변의 제곱의 합을 비교하는 기준(피타고라스 정리의 역)을 썼다.", "partial": "기준 없이 결과만 나열했으면 1점."},
            {"element": "보기별 판정", "points": 2, "criterion": "다섯 보기를 모두 판정해 ○·×를 바르게 가렸다.", "partial": "한 개를 잘못 판정했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{K}개를 답했다.", "partial": ""},
        ],
    )


ISO_TRIPLES = {"345": {"a0": 3, "h0": 4, "c0": 5}, "435": {"a0": 4, "h0": 3, "c0": 5}, "51213": {"a0": 5, "h0": 12, "c0": 13}, "12513": {"a0": 12, "h0": 5, "c0": 13},
               "81517": {"a0": 8, "h0": 15, "c0": 17}, "15817": {"a0": 15, "h0": 8, "c0": 17}}


def py_t4():
    rows = {"h": {"Q": "[[seg(AD)]]의 길이", "isH": 1, "U": " cm", "UA": "cm", "F1": "AD² = ", "F2": "² − ", "F3": "² = ", "LAW": "AD² = AB² − BD²"},
            "area": {"Q": "△ABC의 넓이", "isH": 0, "U": " cm²", "UA": "cm²", "F1": "△ABC = [[frac(1, 2)]] × ", "F2": " × ", "F3": " = ", "LAW": "[[frac(1, 2)]] × BC × AD"}}
    pts = {"A": [0, "{h}"], "B": ["{-a}", 0], "C": ["{a}", 0], "D": [0, 0]}
    segs = [lseg("A", "B", "{c} cm"), ["B", "C"], ["C", "A"], {"a": "A", "b": "D", "dash": True}]
    marks = {"eq": [[["A", "B"], ["A", "C"]]], "right": [["A", "D", "C"]]}
    bclab = [{"at": ["{-a/2}", 0], "text": "{2*a} cm", "dx": 0, "dy": 15, "k": "lbl:bc"}]
    return tpl("m2-2-pythagoras", 4, PY,
        title="이등변삼각형의 높이와 넓이",
        skill="꼭짓점에서 밑변에 내린 수선이 밑변을 이등분함을 쓰고 직각삼각형에서 높이를 구하기",
        variant_axis={"구하는 것": "높이 / 넓이", "세 변": "피타고라스 수 6종 × 1~3배"},
        discriminates="BD = BC ÷ 2를 쓰고 △ABD에 피타고라스 정리를 적용하는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90, process="문제해결",
        prereq=["피타고라스 정리", "이등변삼각형의 꼭지각의 이등분선은 밑변을 수직이등분한다", "삼각형의 넓이"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"in": list(ISO_TRIPLES)}}, {"name": "k", "values": {"int": [1, 3]}}],
        table=[{"key": "w", "rows": rows}, {"key": "t", "rows": ISO_TRIPLES}],
        derive={"a": "k*a0", "h": "k*h0", "c": "k*c0", "S": "a*h", "ans_v": "h*isH + a*h*(1 - isH)", "v1": "c*isH + 2*a*(1 - isH)", "v2": "a*isH + h*(1 - isH)", "v3": "h*h*isH + a*h*(1 - isH)"},
        constraints=["ans_v != c", "ans_v != 2*a"],
        cost_values=["a", "h", "c", "ans_v"],
        answer_var="ans_v",
        verify=["a*a + h*h == c*c", "(isH == 1 and ans == h) or (isH == 0 and ans == a*h)"],
        question="다음 그림과 같이 [[seg(AB)]] = [[seg(AC)]] = {c} cm, [[seg(BC)]] = {2*a} cm인 이등변삼각형 ABC에서 꼭짓점 A에서 밑변 BC에 내린 수선의 발을 D라고 할 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=bclab),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="이등변삼각형의 꼭짓점 A에서 밑변에 내린 수선 AD는 밑변을 수직이등분하므로 BD = [[frac(1, 2)]]BC = {a} cm다. △ABD는 ∠ADB = 90°인 직각삼각형이므로 피타고라스 정리로 높이 AD를 구하고, 넓이는 [[frac(1, 2)]] × BC × AD다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["A", "B"], ["A", "C"]], [["B", "D"], ["D", "C"]]]}, labels=bclab + [{"at": "D", "text": "{a} cm", "dx": -24, "dy": 16, "accent": True, "k": "lbl:bd"}],
                       shade=[["A", "B", "D"]]),
        sol1_anim=[[hl("right:D", "eq:B-D", "eq:D-C", "lbl:bd", keep=True)], [hl("shade:0", "seg:A-D")]],
        sol2=[
            "AD ⊥ BC이므로 AD는 BC를 수직이등분한다: BD = [[frac(1, 2)]] × {2*a} = {a}(cm)",
            "△ABD에서 AD² = AB² − BD² = {c}² − {a}² = {c*c} − {a*a} = {h*h}, AD > 0이므로 AD = {h}(cm)",
            "{F1}{v1}{F2}{v2}{F3}{v3}",
            "따라서 {Q}{eun(Q)} {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "BD = {a}", "hint": "밑변의 수직이등분"}, {"text": "AD² = {c}² − {a}² = {h*h} → AD = {h}", "hint": "피타고라스 정리"}, {"text": "{Q}: {ans_v}{U}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="{a}² + {h}² = {a*a} + {h*h} = {c*c} = {c}²으로 △ABD가 직각삼각형임이 확인되고, 넓이는 [[frac(1, 2)]] × {2*a} × {h} = {S}(cm²)다. 답은 {ans_v}{U}다.",
        model_answer="AD는 밑변 BC를 수직이등분하므로 BD = {a} cm이다. △ABD에서 AD² = {c}² − {a}² = {h*h}이고 AD > 0이므로 AD = {h} cm이다. {F1}{v1}{F2}{v2}{F3}{v3}이므로 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "수직이등분", "points": 2, "criterion": "AD가 BC를 수직이등분하므로 BD = {a} cm임을 밝혔다.", "partial": "BD = {a} cm만 쓰고 근거가 없으면 1점."},
            {"element": "피타고라스 정리", "points": 3, "criterion": "△ABD에서 AD² = {c}² − {a}² = {h*h}, AD = {h} cm를 구했다.", "partial": "빗변을 잘못 놓았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


RECT_TRIPLES = {"345": {"w0": 4, "h0": 3, "d0": 5}, "435": {"w0": 3, "h0": 4, "d0": 5}, "51213": {"w0": 12, "h0": 5, "d0": 13}, "12513": {"w0": 5, "h0": 12, "d0": 13},
                "81517": {"w0": 15, "h0": 8, "d0": 17}, "15817": {"w0": 8, "h0": 15, "d0": 17}, "72425": {"w0": 24, "h0": 7, "d0": 25}}


def py_t5():
    rows = {"diag": {"XS": "BD", "isD": 1, "XAB": "", "XBD": "x", "G1T": "[[seg(AB)]] = ", "G2T": "[[seg(BC)]] = ", "F1": "x² = ", "F2": "² + ", "LAW": "대각선² = 가로² + 세로²"},
            "side": {"XS": "AB", "isD": 0, "XAB": "x", "XBD": "", "G1T": "[[seg(BC)]] = ", "G2T": "[[seg(BD)]] = ", "F1": "x² = ", "F2": "² − ", "LAW": "세로² = 대각선² − 가로²"}}
    pts = {"A": [0, "{h}"], "B": [0, 0], "C": ["{w}", 0], "D": ["{w}", "{h}"]}
    segs = [lseg("A", "B", "{lw}"), lseg("B", "C", "{w}"), ["C", "D"], ["D", "A"], lseg("D", "B", "{ld}"), lseg("A", "B", "{XAB}"), lseg("D", "B", "{XBD}")]
    marks = {"right": [["A", "B", "C"]]}
    return tpl("m2-2-pythagoras", 5, PY,
        title="직사각형의 대각선의 길이",
        skill="직사각형의 한 내각이 직각이므로 대각선을 빗변으로 하는 직각삼각형에 피타고라스 정리 적용하기",
        variant_axis={"구하는 것": "대각선 / 한 변", "세 변": "피타고라스 수 7종 × 1~3배"},
        discriminates="대각선이 직각삼각형의 빗변임을 읽는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"in": list(RECT_TRIPLES)}}, {"name": "k", "values": {"int": [1, 3]}}],
        table=[{"key": "w", "rows": rows}, {"key": "t", "rows": RECT_TRIPLES}],
        derive={"w": "k*w0", "h": "k*h0", "d": "k*d0", "ans_v": "d*isD + h*(1 - isD)", "sq": "ans_v*ans_v", "lw": "h*isD", "ld": "d*(1 - isD)",
                "g1": "h*isD + w*(1 - isD)", "g2": "w*isD + d*(1 - isD)", "v1": "h*isD + d*(1 - isD)", "v2": "w"},
        constraints=["w != h"],
        cost_values=["w", "h", "d", "ans_v"],
        answer_var="ans_v",
        verify=["w*w + h*h == d*d", "(isD == 1 and ans == d) or (isD == 0 and ans == h)"],
        question="다음 그림의 직사각형 ABCD에서 {G1T}{g1} cm, {G2T}{g2} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="직사각형의 네 내각은 모두 90°이므로 대각선 BD는 △ABD(∠A = 90°)의 빗변이다. 따라서 BD² = AB² + AD²이고, AD = BC(대변)다. 두 변을 알면 나머지 한 변의 제곱이 나오고, 길이는 양수인 쪽을 읽는다.",
        sol1_fig=scene(pts, [lseg("A", "B", "{h}"), lseg("B", "C", "{w}"), ["C", "D"], lseg("D", "A", "{w}"), lseg("D", "B", "{d}")], marks={"right": [["A", "B", "C"], ["B", "A", "D"]]}, shade=[["A", "B", "D"]]),
        sol1_anim=[[hl("right:A", "shade:0", keep=True)], [hl("seglbl:D-A", "seglbl:B-C", keep=True)], [hl("seg:D-B", "seglbl:D-B")]],
        sol2=[
            "직사각형의 대변은 같으므로 AD = BC = {w} cm이고 ∠A = 90°",
            "△ABD에서 BD² = AB² + AD² (피타고라스 정리)",
            "{XS} = x cm라 하면 {F1}{v1}{F2}{v2}² = {sq}, x > 0이므로 x = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AD = BC = {w}, ∠A = 90°", "hint": "직사각형"}, {"text": "BD² = AB² + AD²", "hint": "빗변은 대각선"}, {"text": "{F1}{v1}{F2}{v2}² = {sq} → x = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="세 변 {h}, {w}, {d}에 대해 {h}² + {w}² = {h*h} + {w*w} = {d*d} = {d}²이 성립한다. 답은 {ans_v} cm다.",
        model_answer="직사각형에서 AD = BC = {w} cm이고 ∠A = 90°이므로 △ABD에서 BD² = AB² + AD²이다. {XS} = x cm라 하면 {F1}{v1}{F2}{v2}² = {sq}이고 x > 0이므로 x = {ans_v}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "직각삼각형 읽기", "points": 3, "criterion": "대각선 BD가 △ABD의 빗변이고 AD = BC임을 밝혔다.", "partial": "AD = BC를 쓰지 않았으면 1점."},
            {"element": "정리 적용", "points": 2, "criterion": "{F1}{v1}{F2}{v2}² = {sq}{eul(sq)} 세워 x = {ans_v}{eul(ans_v)} 구했다.", "partial": "빗변을 잘못 놓았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "제곱한 값을 답했으면 인정하지 않는다."},
        ],
    )


PY_SEED = {
    "seed_id": "m2-2-pythagoras", "category": "도형",
    "title": "피타고라스 정리 — 변 구하기, 정사각형의 넓이, 직각삼각형 판정, 이등변삼각형의 높이, 직사각형의 대각선",
    "unit_id": "m2-2", "concept_ids": ["m2-2-10", "m2-2-11"],
    "schema_id": SCHEMA_PY, "schema_name": "직각삼각형 피타고라스 정리 응용 / 직각삼각형 판정 / 직사각형 대각선",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 7.5)을 참고해 새로 씀. 세 변은 피타고라스 수(정수 답)만 쓴다 — 중2에서는 제곱근을 쓰지 않으므로 '제곱이 25인 양수 5'로 읽는다. 모르는 변은 라벨 0(숨김) + 'x'. 판정(t3)은 보기 5개를 합성 키 행으로 고정(그림 없음).",
    "geometry": True,
    "templates": [py_t1(), py_t2(), py_t3(), py_t4(), py_t5()],
}


if __name__ == "__main__":
    for seed in (PAR_SEED, SQ_SEED, PY_SEED):
        with_pitfalls(seed, strict=False)
        dump(seed)
