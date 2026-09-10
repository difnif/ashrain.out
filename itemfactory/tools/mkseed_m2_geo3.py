# itemfactory/tools/mkseed_m2_geo3.py — 중2-2 닮음 시드 생성기: 닮음비 · 삼각형의 닮음 조건 · 평행선과 선분의 비 · 무게중심 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_geo3.py
#     → seeds/m2-2-similar-ratio.json · seeds/m2-2-tri-similar.json · seeds/m2-2-parallel-ratio.json · seeds/m2-2-centroid.json
#
# 유형은 출판사 평가자료 카탈로그(reference/pubs/TYPES.md 7.1~7.4)에서 골랐다 — 문항 복제 아님.
# 길이는 닮음비 u : w 와 단위 길이(m, n, t)로 만들어 모든 대응변이 정수가 되게 하고, 좌표는 그 길이 그대로(등축) 그린다.
# 모르는 변의 라벨은 파생 수치 0(렌더러가 숨김) + 행 문자열 "x"(겹쳐 그림).
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mkseed_m2_geo1 import arc, scene  # noqa: E402
from mkseed_m2_geo2 import lseg  # noqa: E402
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_SR = "16e84f37-4911-475f-b6e5-6870ab0ab2c6"       # 평면도형 닮음비 응용 (B)
SCHEMA_TS = "ef59d268-eaa0-454b-a77d-569e509ede99"       # 삼각형 SAS 닮음 조건 응용 (A)
SCHEMA_PR = "19f0ba5b-344d-4e7d-9d66-ab4142e18e84"       # 평행선과 선분의 길이비(공통각 삼각형) (A)
SCHEMA_CG = "d4f5573d-5dd7-4b79-93e8-b1b71d11cdcd"       # 삼각형 무게중심 중선 분할비 (A)

GEO = {"process": "추론", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["구하는대상혼동"]}
RATIOS = {"1-2": {"u": 1, "w": 2}, "2-3": {"u": 2, "w": 3}, "3-4": {"u": 3, "w": 4}, "2-5": {"u": 2, "w": 5}, "3-5": {"u": 3, "w": 5}, "4-5": {"u": 4, "w": 5},
          "1-3": {"u": 1, "w": 3}, "3-7": {"u": 3, "w": 7}, "4-7": {"u": 4, "w": 7}, "5-7": {"u": 5, "w": 7}, "5-6": {"u": 5, "w": 6}, "5-8": {"u": 5, "w": 8}}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. 닮음비
SR = dict(prereq=["닮은 도형에서 대응변의 길이의 비는 모두 같다(닮음비)", "비례식"], ops=["비례"], tags=["닮음", "닮음비", "대응변"])
# 두 닮은 삼각형: △ABC(작은 것, 닮음비 u) · △DEF(큰 것, w). ∠B = ∠E = 70° 로 그린다.
SR_PTS = {"A": ["{ab*cos(pi*70/180)}", "{ab*sin(pi*70/180)}"], "B": [0, 0], "C": ["{bc}", 0],
          "D": ["{bc + 2 + de*cos(pi*70/180)}", "{de*sin(pi*70/180)}"], "E": ["{bc + 2}", 0], "F": ["{bc + 2 + ef}", 0]}


def sr_t1():
    rows = {"EF": {"XS": "EF", "uE": 1, "uC": 0, "XEF": "x", "XBC": "", "G3T": "[[seg(BC)]] = ", "F1": "EF = ", "LAW": "BC : EF = u : w"},
            "BC": {"XS": "BC", "uE": 0, "uC": 1, "XEF": "", "XBC": "x", "G3T": "[[seg(EF)]] = ", "F1": "BC = ", "LAW": "BC : EF = u : w"}}
    segs = [lseg("A", "B", "{ab}"), lseg("B", "C", "{lbc}"), ["C", "A"], lseg("D", "E", "{de}"), lseg("E", "F", "{lef}"), ["F", "D"], lseg("B", "C", "{XBC}"), lseg("E", "F", "{XEF}")]
    return tpl("m2-2-similar-ratio", 1, SR,
        title="닮은 두 삼각형 — 닮음비로 대응변의 길이 구하기",
        skill="대응하는 한 쌍의 변에서 닮음비를 읽고 다른 대응변에 같은 비를 적용하기",
        variant_axis={"구하는 것": "EF / BC", "닮음비": "12쌍", "단위 길이": "2~6 · 3~8"},
        discriminates="대응변을 바르게 짝짓고(AB ↔ DE, BC ↔ EF) 닮음비를 같은 방향으로 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [2, 6]}}, {"name": "n", "values": {"int": [3, 8]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ab": "u*m", "de": "w*m", "bc": "u*n", "ef": "w*n", "ans_v": "w*n*uE + u*n*uC", "g3": "u*n*uE + w*n*uC", "lbc": "u*n*uE", "lef": "w*n*uC", "v1": "u*n*uE + w*n*uC"},
        constraints=["m != n", "ab != bc", "ans_v != ab", "ans_v != de", "ans_v != g3", "de <= 30", "ef <= 40"],
        cost_values=["ab", "de", "g3", "ans_v"],
        answer_var="ans_v",
        verify=["ab*ef == de*bc", "(uE == 1 and ans == ef) or (uC == 1 and ans == bc)"],
        question="다음 그림에서 △ABC ∽ △DEF이다. [[seg(AB)]] = {ab} cm, [[seg(DE)]] = {de} cm, {G3T}{g3} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(SR_PTS, segs),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="△ABC ∽ △DEF에서 대응변은 AB ↔ DE, BC ↔ EF, CA ↔ FD다. 닮음비는 대응변의 길이의 비이므로 AB : DE = {ab} : {de} = {u} : {w}이고, 같은 비가 BC : EF에도 성립한다.",
        sol1_fig=scene(SR_PTS, [lseg("A", "B", "{ab}"), lseg("B", "C", "{bc}"), ["C", "A"], lseg("D", "E", "{de}"), lseg("E", "F", "{ef}"), ["F", "D"]],
                       marks={"eq": [[["A", "B"]], [["D", "E"]]], "arc": [arc("B", "C", "A", "•", "arc:b"), arc("E", "F", "D", "•", "arc:e")]}),
        sol1_anim=[[hl("seglbl:A-B", "seglbl:D-E", "seg:A-B", "seg:D-E", keep=True)], [hl("seg:B-C", "seg:E-F", "seglbl:B-C", "seglbl:E-F")]],
        sol2=[
            "닮음비: AB : DE = {ab} : {de} = {u} : {w}",
            "대응변 BC : EF도 {u} : {w}이므로 {u} : {w} = BC : EF",
            "{F1}{v1} × [[frac({w*uE + u*uC}, {u*uE + w*uC})]] = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AB : DE = {ab} : {de} = {u} : {w}", "hint": "닮음비"}, {"text": "BC : EF = {u} : {w}", "hint": "대응변"}, {"text": "{XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="BC : EF = {bc} : {ef} = {u} : {w}로 AB : DE와 같은 비다. 답은 {ans_v} cm다.",
        model_answer="△ABC ∽ △DEF이므로 닮음비는 AB : DE = {ab} : {de} = {u} : {w}이다. 대응변 BC : EF = {u} : {w}에서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "닮음비", "points": 3, "criterion": "대응변 AB : DE에서 닮음비 {u} : {w}를 구했다.", "partial": "대응변을 잘못 짝지었으면 인정하지 않는다."},
            {"element": "비례식", "points": 2, "criterion": "BC : EF = {u} : {w}를 세워 풀었다.", "partial": "비의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def sr_t2():
    rows = {"pb": {"Q": "△DEF의 둘레의 길이", "GT": "△ABC의 둘레의 길이가 ", "U": " cm", "UA": "cm", "iP": 1, "big": 1, "F1": "(△DEF의 둘레) = ", "LAW": "둘레의 비 = 닮음비"},
            "ps": {"Q": "△ABC의 둘레의 길이", "GT": "△DEF의 둘레의 길이가 ", "U": " cm", "UA": "cm", "iP": 1, "big": 0, "F1": "(△ABC의 둘레) = ", "LAW": "둘레의 비 = 닮음비"},
            "ab": {"Q": "△DEF의 넓이", "GT": "△ABC의 넓이가 ", "U": " cm²", "UA": "cm²", "iP": 0, "big": 1, "F1": "(△DEF의 넓이) = ", "LAW": "넓이의 비 = 닮음비의 제곱"},
            "as": {"Q": "△ABC의 넓이", "GT": "△DEF의 넓이가 ", "U": " cm²", "UA": "cm²", "iP": 0, "big": 0, "F1": "(△ABC의 넓이) = ", "LAW": "넓이의 비 = 닮음비의 제곱"}}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["D", "E"], ["E", "F"], ["F", "D"]]
    return tpl("m2-2-similar-ratio", 2, SR,
        title="닮음비와 둘레·넓이의 비",
        skill="닮음비가 u : w이면 둘레의 비는 u : w, 넓이의 비는 u² : w²임을 쓰기",
        variant_axis={"구하는 것": "큰/작은 도형의 둘레 / 넓이", "닮음비": "12쌍"},
        discriminates="넓이의 비를 닮음비의 제곱으로 쓰는가(둘레는 1제곱)",
        qtype="short", difficulty=2, pool_target=300, time_limit=80, process="절차수행",
        prereq=["닮음비가 m : n이면 둘레의 비는 m : n, 넓이의 비는 m² : n²"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "k", "values": {"int": [4, 12]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ab": "u*3", "de": "w*3", "bc": "u*4", "ef": "w*4", "ps": "u*k", "pb": "w*k", "ss": "u*u*k", "sb": "w*w*k",
                "gv": "iP*(u*k*big + w*k*(1 - big)) + (1 - iP)*(u*u*k*big + w*w*k*(1 - big))",
                "ans_v": "iP*(w*k*big + u*k*(1 - big)) + (1 - iP)*(w*w*k*big + u*u*k*(1 - big))",
                "fn": "iP*(w*big + u*(1 - big)) + (1 - iP)*(w*w*big + u*u*(1 - big))", "fd": "iP*(u*big + w*(1 - big)) + (1 - iP)*(u*u*big + w*w*(1 - big))"},
        constraints=["ans_v != gv", "de <= 24", "ef <= 32"],
        cost_values=["u", "w", "gv", "ans_v"],
        answer_var="ans_v",
        verify=["ps*w == pb*u", "ss*w*w == sb*u*u", "ans > 0"],
        question="다음 그림에서 △ABC ∽ △DEF이고 닮음비가 {u} : {w}이다. {GT}{gv}{U}일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(SR_PTS, segs),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="닮음비가 {u} : {w}이면 대응하는 모든 길이가 {u} : {w}이므로 둘레(길이의 합)의 비도 {u} : {w}다. 넓이는 가로·세로 두 방향으로 {w}/{u}배가 되므로 넓이의 비는 {u}² : {w}² = {u*u} : {w*w}다.",
        sol1_fig=scene(SR_PTS, segs, labels=[{"at": ["{bc/2}", -0.9], "text": "{u}", "dx": 0, "dy": 6, "accent": True, "k": "lbl:u"}, {"at": ["{bc + 2 + ef/2}", -0.9], "text": "{w}", "dx": 0, "dy": 6, "accent": True, "k": "lbl:w"}]),
        sol1_anim=[[hl("lbl:u", "lbl:w", keep=True)], [hl("seg:A-B", "seg:B-C", "seg:C-A", "seg:D-E", "seg:E-F", "seg:F-D")]],
        sol2=[
            "닮음비가 {u} : {w}이므로 둘레의 비는 {u} : {w}, 넓이의 비는 {u}² : {w}² = {u*u} : {w*w}",
            "{Q}{eul(Q)} x라 하면 비례식에서 {F1}{gv} × [[frac({fn}, {fd})]] = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "둘레의 비 {u} : {w}, 넓이의 비 {u*u} : {w*w}", "hint": "닮음비 {u} : {w}"}, {"text": "{F1}{gv} × [[frac({fn}, {fd})]] = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="둘레 {ps} : {pb} = {u} : {w}, 넓이 {ss} : {sb} = {u*u} : {w*w}{ro(w*w)} 닮음비와 그 제곱의 비가 맞는다. 답은 {ans_v}{U}다.",
        model_answer="닮음비가 {u} : {w}이므로 둘레의 비는 {u} : {w}, 넓이의 비는 {u*u} : {w*w}이다. {F1}{gv} × [[frac({fn}, {fd})]] = {ans_v}이므로 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "비의 관계", "points": 3, "criterion": "둘레의 비는 닮음비, 넓이의 비는 닮음비의 제곱임을 썼다.", "partial": "넓이의 비를 닮음비 그대로 두었으면 인정하지 않는다."},
            {"element": "비례식", "points": 2, "criterion": "{F1}{gv} × [[frac({fn}, {fd})]] = {ans_v}{eul(ans_v)} 계산했다.", "partial": "비의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


SCALES = {"1000": {"N": 1000, "NT": "1000"}, "2000": {"N": 2000, "NT": "2000"}, "5000": {"N": 5000, "NT": "5000"}, "10000": {"N": 10000, "NT": "10000"}, "25000": {"N": 25000, "NT": "25000"}, "50000": {"N": 50000, "NT": "50000"}}


def sr_t3():
    rows = {"real": {"Q": "두 지점 사이의 실제 거리는 몇 m인지", "isR": 1, "GT": "지도에서 두 지점 사이의 거리가 ", "GU": " cm", "U": " m", "UA": "m", "F1": "(실제 거리) = ", "F2": " × ", "F3": " cm = ", "LAW": "지도 거리 × 축척의 분모"},
            "map": {"Q": "지도에서 두 지점 사이의 거리는 몇 cm인지", "isR": 0, "GT": "두 지점 사이의 실제 거리가 ", "GU": " m", "U": " cm", "UA": "cm", "F1": "(지도 거리) = ", "F2": " m ÷ ", "F3": " = ", "LAW": "실제 거리 ÷ 축척의 분모"}}
    return tpl("m2-2-similar-ratio", 3, SR,
        title="축도와 축척 — 지도의 거리와 실제 거리",
        skill="축척 1/N은 닮음비 1 : N이므로 실제 거리 = 지도 거리 × N, 단위(cm → m)를 바꾸기",
        variant_axis={"구하는 것": "실제 거리 / 지도 거리", "축척": "6종", "거리": "2~9 cm"},
        discriminates="축척을 닮음비로 읽고 cm와 m의 단위 환산(100 cm = 1 m)을 바르게 하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80, process="문제해결", context="생활맥락", figure=[],
        prereq=["축척 = (축도에서의 길이) : (실제 길이)", "단위 환산 1 m = 100 cm"], ops=["비례", "단위"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "sc", "values": {"in": list(SCALES)}}, {"name": "d", "values": {"int": [2, 9]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "sc", "rows": SCALES}],
        derive={"realcm": "d*N", "realm": "d*N/100", "ans_v": "d*N/100*isR + d*(1 - isR)", "gv": "d*isR + d*N/100*(1 - isR)"},
        constraints=["realm == floor(realm)"],
        cost_values=["N", "d", "realcm", "ans_v"],
        answer_var="ans_v",
        verify=["realcm == 100*realm", "(isR == 1 and ans == realm) or (isR == 0 and ans == d)"],
        question="축척이 [[frac(1, {NT})]]인 지도가 있다. {GT}{gv}{GU}일 때, {Q} 구하시오.",
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="축척 [[frac(1, {NT})]]은 (지도 위의 길이) : (실제 길이) = 1 : {NT}라는 닮음비다. 지도 위 1 cm가 실제 {NT} cm이므로 실제 거리는 지도 거리의 {NT}배이고, cm로 나온 값은 100으로 나누어 m로 바꾼다.",
        sol1_fig=steps(["축척 1 : {NT} — 지도 1 cm = 실제 {NT} cm", "{d} cm ↔ {realcm} cm = {realm} m"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "축척이 [[frac(1, {NT})]]이므로 (지도 거리) : (실제 거리) = 1 : {NT}",
            "지도 거리 {d} cm에 대한 실제 거리는 {d} × {NT} = {realcm}(cm)",
            "{realcm} cm = {realm} m (100 cm = 1 m)",
            "따라서 {Q} 물으면 {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "1 : {NT}", "hint": "축척 = 닮음비"}, {"text": "{d} × {NT} = {realcm} cm", "hint": "{LAW}"}, {"text": "{realcm} cm = {realm} m", "hint": "÷ 100"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="{realm} m = {realcm} cm를 {NT}로 나누면 {d} cm로 지도 거리와 맞는다. 답은 {ans_v}{U}다.",
        model_answer="축척이 [[frac(1, {NT})]]이므로 실제 거리는 지도 거리의 {NT}배이다. {d} cm × {NT} = {realcm} cm = {realm} m이므로 {Q} 물으면 {ans_v}{U}다.",
        rubric=[
            {"element": "축척 = 닮음비", "points": 3, "criterion": "축척 1/{NT}에서 실제 거리가 지도 거리의 {NT}배(또는 그 역)임을 밝혔다.", "partial": "비의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "길이의 환산", "points": 2, "criterion": "cm를 m로(또는 m를 cm로) 바르게 바꾸었다.", "partial": "환산을 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


SR_SEED = {
    "seed_id": "m2-2-similar-ratio", "category": "도형",
    "title": "닮음비 — 대응변의 길이, 둘레·넓이의 비, 축척",
    "unit_id": "m2-2", "concept_ids": ["m2-2-05", "m2-2-09"],
    "schema_id": SCHEMA_SR, "schema_name": "평면도형 닮음비 응용 / 닮음비와 둘레·넓이의 비 / 축도",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 7.1)을 참고해 새로 씀. 두 삼각형은 닮음비 u : w 그대로 등축으로 그린다(∠B = ∠E = 70°). 축척(t3)은 그림 없음.",
    "geometry": True,
    "templates": [sr_t1(), sr_t2(), sr_t3()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 삼각형의 닮음 조건
TS = dict(prereq=["삼각형의 닮음 조건 SSS·SAS·AA", "닮은 도형의 대응변의 비"], ops=["비례"], tags=["닮음조건", "SAS닮음", "AA닮음", "직각삼각형의 닮음"])


def ts_t1():
    # 공통각 A, AD·AB = AE·AC → △ADE ∽ △ACB (SAS). AD = u·m, AE = u·n, AC = w·m, AB = w·n
    rows = {"BC": {"XS": "BC", "uB": 1, "XBC": "x", "XDE": "", "G5T": "[[seg(DE)]] = ", "F1": "BC = ", "LAW": "DE : BC = u : w"},
            "DE": {"XS": "DE", "uB": 0, "XBC": "", "XDE": "x", "G5T": "[[seg(BC)]] = ", "F1": "DE = ", "LAW": "DE : BC = u : w"}}
    pts = {"A": [0, 0], "B": ["{-ab*s2}", "{-ab*c2}"], "C": ["{ac*s2}", "{-ac*c2}"], "D": ["{-ad*s2}", "{-ad*c2}"], "E": ["{ae*s2}", "{-ae*c2}"]}
    segs = [lseg("D", "A", "{ad}"), lseg("B", "D", "{db}"), lseg("A", "E", "{ae}"), lseg("E", "C", "{ec}"), lseg("B", "C", "{lbc}"), lseg("D", "E", "{lde}"), lseg("B", "C", "{XBC}"), lseg("D", "E", "{XDE}")]
    return tpl("m2-2-tri-similar", 1, TS,
        title="SAS 닮음 — 공통인 각을 낀 두 변의 비가 같은 두 삼각형",
        skill="∠A가 공통이고 AD : AC = AE : AB이면 △ADE ∽ △ACB임을 밝히고 대응변 DE ↔ CB에 닮음비 적용하기",
        variant_axis={"구하는 것": "BC / DE", "닮음비": "12쌍", "변의 배율": "m, n = 1~3 · t = 2~5"},
        discriminates="대응 순서(A↔A, D↔C, E↔B)를 바르게 잡아 DE와 BC(엇갈린 대응)를 짝짓는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110,
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [2, 5]}}, {"name": "n", "values": {"int": [2, 5]}}, {"name": "t", "values": {"int": [2, 6]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ad": "u*m", "ae": "u*n", "ac": "w*m", "ab": "w*n", "db": "w*n - u*m", "ec": "w*m - u*n", "de": "u*t", "bc": "w*t",
                "ans_v": "w*t*uB + u*t*(1 - uB)", "g5": "u*t*uB + w*t*(1 - uB)", "lbc": "w*t*(1 - uB)", "lde": "u*t*uB", "v1": "u*t*uB + w*t*(1 - uB)",
                "cth": "(m*m + n*n - t*t)/(2*m*n)", "s2": "sqrt(abs((1 - cth)/2))", "c2": "sqrt(abs((1 + cth)/2))",
                "L": "max(ab, ac, bc)", "mn": "min(ad, db, ae, ec, de)",
                "cB": "(n*n + t*t - m*m)/(2*n*t)", "cC": "(m*m + t*t - n*n)/(2*m*t)"},
        # 꼭지각 40°~120°(단일 삼각형의 모양 한계)는 유지. 변의 비율 상한(1.5배)·D, E 위치 비율은 두 규칙으로 대체 —
        # ① 세 각이 모두 28° 이상(cos ≤ 0.88: 밑각이 더 작으면 라벨이 이웃 변에 얹힌다) ② 라벨이 붙는 선분이 가장 긴 변의 10% 이상.
        constraints=["m != n", "t > abs(m - n)", "t < m + n", "2*cth > -1", "100*cth < 76", "100*cB <= 88", "100*cC <= 88", "10*mn >= L", "ab <= 28", "ac <= 28", "ans_v != ad", "ans_v != ae", "ans_v != db", "ans_v != ec", "ans_v != g5"],
        cost_values=["ad", "db", "ae", "ec", "g5", "ans_v"],
        answer_var="ans_v",
        verify=["ad*ab == ae*ac", "de*w == bc*u", "(uB == 1 and ans == bc) or (uB == 0 and ans == de)"],
        question="다음 그림의 △ABC에서 두 점 D, E는 각각 변 AB, AC 위의 점이고 [[seg(AD)]] = {ad} cm, [[seg(DB)]] = {db} cm, [[seg(AE)]] = {ae} cm, [[seg(EC)]] = {ec} cm, {G5T}{g5} cm이다. [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="△ADE와 △ACB를 비교한다(순서에 주의 — D는 C에, E는 B에 대응). ∠A는 공통이고 AD : AC = {ad} : {ac} = {u} : {w}, AE : AB = {ae} : {ab} = {u} : {w}로 끼인각을 낀 두 변의 비가 같으므로 SAS 닮음이다. 닮음비 {u} : {w}가 DE : CB에도 적용된다.",
        sol1_fig=scene(pts, [lseg("D", "A", "{ad}"), lseg("B", "D", "{db}"), lseg("A", "E", "{ae}"), lseg("E", "C", "{ec}"), lseg("B", "C", "{bc}"), lseg("D", "E", "{de}")],
                       marks={"arc": [arc("A", "B", "C", "•", "arc:a")]}, shade=[["A", "D", "E"]],
                       labels=[{"at": ["{-ab*s2/2}", "{-ab*c2/2}"], "text": "AB = {ab}", "dx": -30, "dy": 4, "accent": True, "k": "lbl:ab"},
                               {"at": ["{ac*s2/2}", "{-ac*c2/2}"], "text": "AC = {ac}", "dx": 30, "dy": 4, "accent": True, "k": "lbl:ac"}]),
        sol1_anim=[[hl("arc:a", keep=True)], [hl("shade:0", "lbl:ab", "lbl:ac", keep=True)], [hl("seg:D-E", "seg:B-C", "seglbl:D-E", "seglbl:B-C")]],
        sol2=[
            "AB = {ad} + {db} = {ab}, AC = {ae} + {ec} = {ac}",
            "△ADE와 △ACB에서 ∠A는 공통, AD : AC = {ad} : {ac} = {u} : {w}, AE : AB = {ae} : {ab} = {u} : {w}",
            "따라서 △ADE ∽ △ACB (SAS 닮음), 닮음비 {u} : {w}",
            "DE : CB = {u} : {w}이므로 {F1}{v1} × [[frac({w*uB + u*(1 - uB)}, {u*uB + w*(1 - uB)})]] = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AD : AC = {u} : {w}, AE : AB = {u} : {w}", "hint": "끼인각 ∠A 공통"}, {"text": "△ADE ∽ △ACB", "hint": "SAS 닮음 (D ↔ C, E ↔ B)"}, {"text": "DE : CB = {u} : {w} → {XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [], []],
        sol_check="AD × AB = {ad} × {ab} = {ad*ab}, AE × AC = {ae} × {ac} = {ae*ac}{ro(ae*ac)} 같고, DE : BC = {de} : {bc} = {u} : {w}다. 답은 {ans_v} cm다.",
        model_answer="△ADE와 △ACB에서 ∠A는 공통이고 AD : AC = {ad} : {ac} = {u} : {w}, AE : AB = {ae} : {ab} = {u} : {w}이므로 △ADE ∽ △ACB(SAS 닮음)이다. 닮음비가 {u} : {w}이므로 DE : CB = {u} : {w}에서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "닮음 밝히기", "points": 3, "criterion": "∠A 공통과 두 변의 비 {u} : {w}에서 △ADE ∽ △ACB(SAS)임을 대응 순서와 함께 밝혔다.", "partial": "닮음이라고만 쓰고 조건을 밝히지 않았으면 1점."},
            {"element": "대응변의 비", "points": 2, "criterion": "DE : CB = {u} : {w}를 세워 {XS}{eul(XS)} 구했다.", "partial": "DE를 BC와 평행한 것처럼 AD : AB로 잘못 짝지었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def ts_t2():
    # AA 닮음: ∠ABC = ∠ADE (D는 AC 위, E는 AB 위) → △ADE ∽ △ABC. AD = u·m, AB = w·m, AE = u·n, AC = w·n
    rows = {"CD": {"XS": "CD", "uD": 1, "XDC": "x", "XEB": "", "G3T": "[[seg(AB)]] = ", "g3n": 1, "F1": "CD = AC − AD = ", "F2": " − ", "LAW": "AB : AD = AC : AE"},
            "EB": {"XS": "EB", "uD": 0, "XDC": "", "XEB": "x", "G3T": "[[seg(AC)]] = ", "g3n": 0, "F1": "EB = AB − AE = ", "F2": " − ", "LAW": "AB : AD = AC : AE"}}
    pts = {"A": [0, 0], "B": ["{-ab*sin(pi*36/180)}", "{-ab*cos(pi*36/180)}"], "C": ["{ac*sin(pi*34/180)}", "{-ac*cos(pi*34/180)}"],
           "E": ["{-ae*sin(pi*36/180)}", "{-ae*cos(pi*36/180)}"], "D": ["{ad*sin(pi*34/180)}", "{-ad*cos(pi*34/180)}"]}
    # 선분 라벨은 a→b 방향의 왼쪽 법선(화면 기준)에 놓이므로, 바깥쪽에 두려면 왼쪽 변은 위→아래, 오른쪽 변은 아래→위로 적는다
    # (안쪽에 두면 B·D의 각 표시 '•'와 x 라벨이 겹친다)
    segs = [lseg("A", "E", "{ae}"), lseg("E", "B", "{leb}"), lseg("D", "A", "{ad}"), lseg("C", "D", "{ldc}"), ["B", "C"], ["D", "E"], lseg("E", "B", "{XEB}"), lseg("C", "D", "{XDC}")]
    marks = {"arc": [arc("B", "C", "A", "•", "arc:b"), arc("D", "E", "A", "•", "arc:d")]}
    return tpl("m2-2-tri-similar", 2, TS,
        title="AA 닮음 — 같은 각이 표시된 두 삼각형",
        skill="∠A 공통, ∠ABC = ∠ADE에서 △ABC ∽ △ADE를 밝히고 대응변의 비로 길이 구하기",
        variant_axis={"구하는 것": "CD / EB", "닮음비": "12쌍", "배율": "m, n = 1~3"},
        discriminates="같은 각끼리 대응시켜(B ↔ D, C ↔ E) AB : AD = AC : AE로 세우는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110,
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [1, 4]}}, {"name": "n", "values": {"int": [1, 4]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ad": "u*m", "ab": "w*m", "ae": "u*n", "ac": "w*n", "dc": "w*n - u*m", "eb": "w*m - u*n",
                "ans_v": "(w*n - u*m)*uD + (w*m - u*n)*(1 - uD)", "g3": "w*m*g3n + w*n*(1 - g3n)", "ldc": "(w*n - u*m)*(1 - uD)", "leb": "(w*m - u*n)*uD",
                "v1": "w*n*uD + w*m*(1 - uD)", "v2": "u*m*uD + u*n*(1 - uD)",
                "L": "max(ab, ac)", "mn": "min(ad, ae, dc, eb)"},
        # 꼭지각 70° 고정 그림 — 두 변의 비가 2배를 넘으면 밑각이 25° 아래로 내려가 라벨이 겹친다. 부분 선분은 가독성 규칙(큰 변의 10% 이상).
        constraints=["dc >= 1", "eb >= 1", "2*m >= n", "2*n >= m", "10*mn >= L", "ab <= 24", "ac <= 24", "ans_v != ad", "ans_v != ae", "ans_v != g3"],
        cost_values=["ad", "ae", "g3", "ans_v"],
        answer_var="ans_v",
        verify=["ad*ac == ae*ab", "(uD == 1 and ans == dc) or (uD == 0 and ans == eb)"],
        question="다음 그림의 △ABC에서 두 점 D, E는 각각 변 AC, AB 위의 점이고 [[angle(ABC)]] = [[angle(ADE)]]이다. [[seg(AD)]] = {ad} cm, [[seg(AE)]] = {ae} cm, {G3T}{g3} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="△ABC와 △ADE에서 ∠A는 공통이고 ∠ABC = ∠ADE이므로 두 쌍의 각이 같다 — AA 닮음이다. 같은 각끼리 대응하므로 B ↔ D, C ↔ E이고, 대응변의 비 AB : AD = AC : AE = BC : DE가 같다. 여기서 모르는 변을 구한 뒤 부분 길이(CD 또는 EB)로 옮긴다.",
        sol1_fig=scene(pts, [lseg("A", "E", "{ae}"), lseg("E", "B", "{eb}"), lseg("D", "A", "{ad}"), lseg("C", "D", "{dc}"), ["B", "C"], ["D", "E"]], marks={**marks, "arc": marks["arc"] + [arc("A", "B", "C", "∘", "arc:a")]},
                       shade=[["A", "D", "E"]]),
        sol1_anim=[[hl("arc:a", "arc:b", "arc:d", keep=True)], [hl("shade:0", keep=True)], [hl("seglbl:E-B", "seglbl:C-D")]],
        sol2=[
            "△ABC와 △ADE에서 ∠A는 공통, ∠ABC = ∠ADE → △ABC ∽ △ADE (AA 닮음), 대응은 B ↔ D, C ↔ E",
            "AB : AD = AC : AE이므로 {ab} : {ad} = {ac} : {ae} (닮음비 {w} : {u})",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "△ABC ∽ △ADE", "hint": "AA 닮음 (B ↔ D, C ↔ E)"}, {"text": "AB : AD = AC : AE = {w} : {u}", "hint": "대응변의 비"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}", "hint": "부분 길이"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AB × AE = {ab} × {ae} = {ab*ae}, AD × AC = {ad} × {ac} = {ad*ac}{ro(ad*ac)} 같아 비례식이 성립한다. CD = {dc}, EB = {eb}다. 답은 {ans_v} cm다.",
        model_answer="△ABC와 △ADE에서 ∠A는 공통이고 ∠ABC = ∠ADE이므로 △ABC ∽ △ADE(AA 닮음)이다. AB : AD = AC : AE에서 {ab} : {ad} = {ac} : {ae}이고 {F1}{v1}{F2}{v2} = {ans_v}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "닮음 밝히기", "points": 3, "criterion": "∠A 공통, ∠ABC = ∠ADE에서 △ABC ∽ △ADE(AA)임을 대응 순서와 함께 밝혔다.", "partial": "닮음이라고만 쓰고 조건을 밝히지 않았으면 1점."},
            {"element": "비례식", "points": 2, "criterion": "AB : AD = AC : AE를 세워 모르는 변을 구했다.", "partial": "대응변을 잘못 짝지었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "전체 변의 길이를 답했으면 인정하지 않는다."},
        ],
    )


SQPAIRS = {"1-2": {"mm": 1, "nn": 2}, "2-3": {"mm": 2, "nn": 3}, "1-3": {"mm": 1, "nn": 3}, "3-4": {"mm": 3, "nn": 4}, "2-5": {"mm": 2, "nn": 5}, "3-5": {"mm": 3, "nn": 5},
           "2-1": {"mm": 2, "nn": 1}, "3-2": {"mm": 3, "nn": 2}, "4-3": {"mm": 4, "nn": 3}, "3-1": {"mm": 3, "nn": 1}, "5-2": {"mm": 5, "nn": 2}, "5-3": {"mm": 5, "nn": 3}}


def ts_t3():
    # ∠A = 90°, AH ⊥ BC: AH² = BH·CH. BH = k·mm², CH = k·nn², AH = k·mm·nn
    rows = {"AH": {"XS": "AH", "uA": 1, "uB": 0, "XAH": "x", "XBH": "", "G1T": "[[seg(BH)]] = ", "G2T": "[[seg(CH)]] = ", "F1": "AH² = BH × CH = ", "F2": " × ", "F3": " = ", "LAW": "AH² = BH × CH"},
            "BH": {"XS": "BH", "uA": 0, "uB": 1, "XAH": "", "XBH": "x", "G1T": "[[seg(AH)]] = ", "G2T": "[[seg(CH)]] = ", "F1": "BH = AH² ÷ CH = ", "F2": "² ÷ ", "F3": " = ", "LAW": "BH = AH² ÷ CH"}}
    pts = {"A": [0, "{ah}"], "B": ["{-bh}", 0], "C": ["{ch}", 0], "H": [0, 0]}
    segs = [["A", "B"], lseg("B", "H", "{lbh}"), lseg("H", "C", "{ch}"), ["C", "A"], lseg("H", "A", "{lah}"), lseg("B", "H", "{XBH}"), lseg("H", "A", "{XAH}")]
    marks = {"right": [["B", "A", "C"], ["A", "H", "C"]]}
    return tpl("m2-2-tri-similar", 3, TS,
        title="직각삼각형의 닮음 — 빗변에 내린 수선 AH² = BH × CH",
        skill="∠A = 90°, AH ⊥ BC에서 △ABH ∽ △CAH임을 밝히고 AH : CH = BH : AH를 세우기",
        variant_axis={"구하는 것": "AH / BH", "비": "12쌍 × k = 1~4"},
        discriminates="두 작은 직각삼각형이 닮음(AA)임을 밝히고 AH가 두 삼각형에서 서로 다른 변에 대응함을 읽는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110,
        prereq=["삼각형의 닮음 조건 AA", "직각삼각형에서 직각을 낀 두 각의 합은 90°"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "pr", "values": {"in": list(SQPAIRS)}}, {"name": "k", "values": {"int": [1, 4]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "pr", "rows": SQPAIRS}],
        derive={"bh": "k*mm*mm", "ch": "k*nn*nn", "ah": "k*mm*nn", "ans_v": "ah*uA + bh*uB", "g1": "bh*uA + ah*uB", "lbh": "bh*uA", "lah": "ah*uB",
                "v1": "bh*uA + ah*uB", "v2": "ch", "v3": "ah*ah*uA + bh*uB"},
        # BH : CH는 1 : 9까지(보조선 AH가 있는 결합 그림) — 짧은 쪽이 빗변의 8% 이상이면 라벨이 겹치지 않는다
        # 짧은 쪽이 빗변의 12% 미만이면 그 선분의 라벨이 H 이름과 겹친다(1 : 9는 탈락, 4 : 25·9 : 25는 통과). bh, ch = 1은 '÷ 1' 항등 연산이 풀이에 남으므로 제외.
        constraints=["bh <= 36", "ch <= 36", "bh >= 2", "ch >= 2", "25*bh >= 3*(bh + ch)", "25*ch >= 3*(bh + ch)", "ans_v != ch", "ans_v != g1"],
        cost_values=["bh", "ch", "ah", "ans_v"],
        answer_var="ans_v",
        verify=["ah*ah == bh*ch", "(uA == 1 and ans == ah) or (uB == 1 and ans == bh)"],
        question="다음 그림과 같이 [[angle(A)]] = [[deg(90)]]인 직각삼각형 ABC에서 점 H는 꼭짓점 A에서 빗변 BC에 내린 수선의 발이다. {G1T}{g1} cm, {G2T}{ch} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="△ABH와 △CAH는 모두 H에서 직각이고, ∠BAH = 90° − ∠B = ∠C이므로 AA 닮음이다(A ↔ C, B ↔ A, H ↔ H). 대응변의 비 BH : AH = AH : CH에서 AH² = BH × CH가 나온다 — 수선 AH가 한 삼각형에서는 긴 변, 다른 삼각형에서는 짧은 변으로 대응하는 것이 핵심이다.",
        sol1_fig=scene(pts, [["A", "B"], lseg("B", "H", "{bh}"), lseg("H", "C", "{ch}"), ["C", "A"], lseg("H", "A", "{ah}")], marks={**marks, "arc": [arc("B", "H", "A", "•", "arc:b"), arc("A", "C", "H", "•", "arc:a1"), arc("C", "A", "H", "×", "arc:c"), arc("A", "H", "B", "×", "arc:a2")]},
                       shade=[["A", "B", "H"]]),
        sol1_anim=[[hl("right:A", "right:H", keep=True)], [hl("arc:b", "arc:a1", "arc:c", "arc:a2", keep=True)], [hl("shade:0", "seglbl:H-A")]],
        sol2=[
            "△ABH와 △CAH에서 ∠AHB = ∠CHA = 90°, ∠BAH = ∠ACH (= 90° − ∠B) → △ABH ∽ △CAH (AA 닮음)",
            "대응변의 비: BH : AH = AH : CH, 즉 AH² = BH × CH",
            "{F1}{v1}{F2}{v2}{F3}{v3}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "△ABH ∽ △CAH", "hint": "AA 닮음 (직각 + ∠BAH = ∠C)"}, {"text": "BH : AH = AH : CH → AH² = BH × CH", "hint": "대응변"}, {"text": "{F1}{v1}{F2}{v2}{F3}{v3} → {XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AH² = {ah}² = {ah*ah}이고 BH × CH = {bh} × {ch} = {bh*ch}{ro(bh*ch)} 같다. 답은 {ans_v} cm다.",
        model_answer="△ABH와 △CAH에서 ∠AHB = ∠CHA = 90°이고 ∠BAH = ∠ACH이므로 △ABH ∽ △CAH(AA 닮음)이다. BH : AH = AH : CH에서 AH² = BH × CH이고 {F1}{v1}{F2}{v2}{F3}{v3}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "닮음 밝히기", "points": 3, "criterion": "△ABH ∽ △CAH(AA)임을 두 각의 상등과 함께 밝혔다.", "partial": "닮음이라고만 썼으면 1점."},
            {"element": "비례식", "points": 2, "criterion": "BH : AH = AH : CH(AH² = BH × CH)를 세워 계산했다.", "partial": "AH를 같은 위치의 변으로 잘못 대응시켰으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "제곱한 값을 답했으면 인정하지 않는다."},
        ],
    )


def ts_t4():
    # AB ∥ CD, AD·BC 가 O 에서 만남 → △OAB ∽ △ODC (맞꼭지각 + 엇각). OA = u·m, OD = w·m, OB = u·n, OC = w·n, AB = u·t, DC = w·t
    rows = {"DC": {"XS": "DC", "i1": 1, "i2": 0, "i3": 0, "XDC": "x", "XOB": "", "XOD": "", "G2T": "[[seg(OD)]] = ", "G3T": "[[seg(AB)]] = ", "F1": "DC = ", "LAW": "AB : DC = u : w"},
            "OB": {"XS": "OB", "i1": 0, "i2": 1, "i3": 0, "XDC": "", "XOB": "x", "XOD": "", "G2T": "[[seg(OD)]] = ", "G3T": "[[seg(OC)]] = ", "F1": "OB = ", "LAW": "OB : OC = u : w"},
            "OD": {"XS": "OD", "i1": 0, "i2": 0, "i3": 1, "XDC": "", "XOB": "", "XOD": "x", "G2T": "[[seg(AB)]] = ", "G3T": "[[seg(DC)]] = ", "F1": "OD = ", "LAW": "OA : OD = u : w"}}
    pts = {"O": [0, 0], "A": ["{-oa*s2}", "{oa*c2}"], "B": ["{ob*s2}", "{ob*c2}"], "D": ["{od*s2}", "{-od*c2}"], "C": ["{-oc*s2}", "{-oc*c2}"]}
    segs = [lseg("O", "A", "{oa}"), lseg("D", "O", "{lod}"), lseg("O", "C", "{loc}"), lseg("A", "B", "{lab}"), lseg("C", "D", "{ldc}"),
            lseg("B", "O", "{XOB}"), lseg("D", "O", "{XOD}"), lseg("C", "D", "{XDC}")]
    marks = {"arc": [arc("O", "A", "B", None, "arc:o1"), arc("O", "C", "D", None, "arc:o2")]}
    return tpl("m2-2-tri-similar", 4, TS,
        title="맞꼭지각과 엇각 — 평행한 두 선분이 만드는 닮은 삼각형",
        skill="AB ∥ CD에서 △OAB ∽ △ODC(AA)임을 밝히고 OA : OD = OB : OC = AB : DC로 길이 구하기",
        variant_axis={"구하는 것": "DC / OB / OD", "닮음비": "12쌍"},
        discriminates="맞꼭지각과 엇각으로 AA 닮음을 밝히고 대응(A ↔ D, B ↔ C)을 바르게 잡는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=100,
        prereq=["삼각형의 닮음 조건 AA", "평행선의 엇각", "맞꼭지각"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 3]}}, {"name": "t", "values": {"int": [1, 3]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"oa": "u*m", "od": "w*m", "ob": "u*n", "oc": "w*n", "ab": "u*t", "dc": "w*t", "ans_v": "w*t*i1 + u*n*i2 + w*m*i3",
                "g2": "w*m*(i1 + i2) + u*t*i3", "g3": "u*t*i1 + w*n*i2 + w*t*i3",
                "lod": "w*m*(i1 + i2)", "loc": "w*n*i2", "lab": "u*t*(i1 + i3)", "ldc": "w*t*i3", "v1": "u*t*i1 + w*n*i2 + u*m*i3",
                "cth": "(m*m + n*n - t*t)/(2*m*n)", "s2": "sqrt(abs((1 - cth)/2))", "c2": "sqrt(abs((1 + cth)/2))"},
        constraints=["m != n or t != m", "t > abs(m - n)", "t < m + n", "10*cth <= 7", "10*cth >= -7", "od <= 21", "oc <= 21", "dc <= 21", "ans_v != oa", "ans_v != g2", "ans_v != g3"],
        cost_values=["oa", "g2", "g3", "ans_v"],
        answer_var="ans_v",
        verify=["oa*dc == od*ab", "ob*od == oa*oc", "(i1 == 1 and ans == dc) or (i2 == 1 and ans == ob) or (i3 == 1 and ans == od)"],
        question="다음 그림에서 [[seg(AB)]] ∥ [[seg(CD)]]이고 두 선분 AD, BC의 교점을 O라고 하자. [[seg(OA)]] = {oa} cm, {G2T}{g2} cm, {G3T}{g3} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="AB ∥ CD이므로 엇각 ∠OAB = ∠ODC, ∠OBA = ∠OCD이고(맞꼭지각 ∠AOB = ∠DOC도 같다), △OAB와 △ODC는 AA 닮음이다. 대응은 A ↔ D, B ↔ C이므로 OA : OD = OB : OC = AB : DC — 알려진 한 쌍의 대응변에서 닮음비를 읽고 묻는 변에 적용한다.",
        sol1_fig=scene(pts, [lseg("O", "A", "{oa}"), lseg("B", "O", "{ob}"), lseg("D", "O", "{od}"), lseg("O", "C", "{oc}"), lseg("A", "B", "{ab}"), lseg("C", "D", "{dc}")],
                       marks={"arc": marks["arc"] + [arc("A", "O", "B", "•", "arc:a"), arc("D", "C", "O", "•", "arc:d")]}, shade=[["O", "A", "B"]]),
        sol1_anim=[[hl("arc:o1", "arc:o2", keep=True)], [hl("arc:a", "arc:d", keep=True)], [hl("shade:0", "seg:C-D")]],
        sol2=[
            "AB ∥ CD이므로 ∠OAB = ∠ODC (엇각), ∠AOB = ∠DOC (맞꼭지각) → △OAB ∽ △ODC (AA 닮음)",
            "대응은 A ↔ D, B ↔ C: OA : OD = OB : OC = AB : DC, 닮음비 {u} : {w}",
            "{F1}{v1} × [[frac({w*(i1 + i3) + u*i2}, {u*(i1 + i3) + w*i2})]] = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "△OAB ∽ △ODC", "hint": "엇각 + 맞꼭지각 (AA)"}, {"text": "OA : OD = OB : OC = AB : DC = {u} : {w}", "hint": "대응 A ↔ D, B ↔ C"}, {"text": "{XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="OA : OD = {oa} : {od}, OB : OC = {ob} : {oc}, AB : DC = {ab} : {dc}가 모두 {u} : {w}로 같다. 답은 {ans_v} cm다.",
        model_answer="AB ∥ CD이므로 엇각과 맞꼭지각에 의해 △OAB ∽ △ODC(AA 닮음)이고, 대응변의 비 OA : OD = OB : OC = AB : DC = {u} : {w}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "닮음 밝히기", "points": 3, "criterion": "엇각(또는 맞꼭지각)으로 △OAB ∽ △ODC(AA)임을 대응 순서와 함께 밝혔다.", "partial": "닮음이라고만 썼으면 1점."},
            {"element": "비례식", "points": 2, "criterion": "닮음비 {u} : {w}를 읽어 {XS}의 비례식을 세웠다.", "partial": "대응을 A ↔ C처럼 잘못 잡았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


TS_SEED = {
    "seed_id": "m2-2-tri-similar", "category": "도형",
    "title": "삼각형의 닮음 조건 — SAS 닮음, AA 닮음, 직각삼각형의 수선, 평행한 두 선분(맞꼭지각)",
    "unit_id": "m2-2", "concept_ids": ["m2-2-06"],
    "schema_id": SCHEMA_TS, "schema_name": "삼각형 SAS 닮음 조건 응용 / AA 닮음 / 직각삼각형의 닮음 / 평행선과 닮음",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 7.2)을 참고해 새로 씀. 모든 길이는 닮음비 u : w 와 배율 m, n, t 의 곱 — 대응변이 항상 정수. 좌표는 길이 그대로(등축)이므로 그림의 각 조건(∠ABC = ∠ADE, AH ⊥ BC 등)이 실제로 성립한다.",
    "geometry": True,
    "templates": [ts_t1(), ts_t2(), ts_t3(), ts_t4()],
}



# ═══════════════════════════════════════════════════════════════════ 3. 평행선과 선분의 길이의 비
PR = dict(prereq=["삼각형에서 평행선과 선분의 길이의 비 AD : AB = AE : AC = DE : BC", "삼각형의 두 변의 중점을 연결한 선분의 성질"], ops=["비례"], tags=["평행선", "선분의비", "중점연결정리"])


def pr_t1():
    # BC ∥ DE (D∈AB, E∈AC): AD = u·m, DB = (w−u)·m, AE = u·n, EC = (w−u)·n, DE = u·t, BC = w·t
    rows = {"EC": {"XS": "EC", "i1": 1, "i2": 0, "i3": 0, "XEC": "x", "XDE": "", "XBC": "", "G3T": "[[seg(AE)]] = ", "F1": "AD : DB = AE : EC → EC = ", "LAW": "AD : DB = AE : EC"},
            "DE": {"XS": "DE", "i1": 0, "i2": 1, "i3": 0, "XEC": "", "XDE": "x", "XBC": "", "G3T": "[[seg(BC)]] = ", "F1": "AD : AB = DE : BC → DE = ", "LAW": "AD : AB = DE : BC"},
            "BC": {"XS": "BC", "i1": 0, "i2": 0, "i3": 1, "XEC": "", "XDE": "", "XBC": "x", "G3T": "[[seg(DE)]] = ", "F1": "AD : AB = DE : BC → BC = ", "LAW": "AD : AB = DE : BC"}}
    pts = {"A": [0, 0], "B": ["{-ab*s2}", "{-ab*c2}"], "C": ["{ac*s2}", "{-ac*c2}"], "D": ["{-ad*s2}", "{-ad*c2}"], "E": ["{ae*s2}", "{-ae*c2}"]}
    # DE 라벨은 D→E 방향(아래쪽, 사다리꼴 DBCE 안)에 둔다 — E→D로 적으면 △ADE 안쪽에 놓여 AD 라벨과 겹친다
    segs = [lseg("D", "A", "{ad}"), lseg("B", "D", "{db}"), lseg("A", "E", "{lae}"), lseg("E", "C", "{lec}"), lseg("B", "C", "{lbc}"), lseg("D", "E", "{lde}"),
            lseg("E", "C", "{XEC}"), lseg("D", "E", "{XDE}"), lseg("B", "C", "{XBC}")]
    return tpl("m2-2-parallel-ratio", 1, PR,
        title="삼각형과 평행선 — BC ∥ DE일 때 선분의 길이",
        skill="AD : AB = AE : AC = DE : BC와 AD : DB = AE : EC를 구별해 쓰기",
        variant_axis={"구하는 것": "EC / DE / BC", "닮음비": "12쌍", "배율": "m, n, t"},
        discriminates="DE : BC는 AD : AB(전체)와 같고 AD : DB(부분)와는 다름을 구별하는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 3]}}, {"name": "t", "values": {"int": [1, 3]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ad": "u*m", "db": "(w - u)*m", "ab": "w*m", "ae": "u*n", "ec": "(w - u)*n", "ac": "w*n", "de": "u*t", "bc": "w*t",
                "ans_v": "(w - u)*n*i1 + u*t*i2 + w*t*i3", "g3": "u*n*i1 + w*t*i2 + u*t*i3",
                "lae": "u*n*i1", "lec": "0*i1", "lbc": "w*t*i2", "lde": "u*t*i3", "v1": "u*n*i1 + w*t*i2 + u*t*i3",
                "cth": "(m*m + n*n - t*t)/(2*m*n)", "s2": "sqrt(abs((1 - cth)/2))", "c2": "sqrt(abs((1 + cth)/2))",
                "L": "max(ab, ac, bc)", "mn": "min(ad, db, ae, ec, de)",
                "cB": "(m*m + t*t - n*n)/(2*m*t)", "cC": "(n*n + t*t - m*m)/(2*n*t)"},
        # 꼭지각 40°~120°는 유지, 변의 비율 상한(1.5배)은 ① 세 각 28° 이상 ② 라벨 선분 ≥ 큰 변의 10% 로 대체
        constraints=["m != n or n != t", "t > abs(m - n)", "t < m + n", "2*cth > -1", "100*cth < 76", "100*cB <= 88", "100*cC <= 88", "10*mn >= L", "ab <= 21", "ac <= 21", "bc <= 21", "ans_v != ad", "ans_v != db", "ans_v != g3"],
        cost_values=["ad", "db", "g3", "ans_v"],
        answer_var="ans_v",
        verify=["ad*ec == db*ae", "ad*bc == ab*de", "(i1 == 1 and ans == ec) or (i2 == 1 and ans == de) or (i3 == 1 and ans == bc)"],
        question="다음 그림의 △ABC에서 [[seg(BC)]] ∥ [[seg(DE)]]이고 [[seg(AD)]] = {ad} cm, [[seg(DB)]] = {db} cm, {G3T}{g3} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="BC ∥ DE이면 △ADE ∽ △ABC(동위각, AA)이므로 AD : AB = AE : AC = DE : BC다. 또 두 변이 같은 비로 나뉘어 AD : DB = AE : EC도 성립한다. 부분끼리의 비(AD : DB)와 전체에 대한 비(AD : AB)를 섞어 쓰지 않는 것이 핵심 — DE : BC는 AD : AB와 같다.",
        sol1_fig=scene(pts, [lseg("D", "A", "{ad}"), lseg("B", "D", "{db}"), lseg("A", "E", "{ae}"), lseg("E", "C", "{ec}"), lseg("B", "C", "{bc}"), lseg("D", "E", "{de}")],
                       marks={"arc": [arc("D", "E", "B", "•", "arc:d"), arc("B", "C", "A", "•", "arc:b")]}, shade=[["A", "D", "E"]]),
        sol1_anim=[[hl("arc:d", "arc:b", keep=True)], [hl("shade:0", keep=True)], [hl("seg:D-E", "seg:B-C", "seglbl:D-E", "seglbl:B-C")]],
        sol2=[
            "BC ∥ DE이므로 AD : DB = AE : EC, AD : AB = AE : AC = DE : BC",
            "AD : DB = {ad} : {db} = {u} : {w - u}, AD : AB = {ad} : {ab} = {u} : {w}",
            "{F1}{v1} × [[frac({(w - u)*i1 + u*i2 + w*i3}, {u*i1 + w*i2 + u*i3})]] = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AD : DB = AE : EC", "hint": "부분 : 부분"}, {"text": "AD : AB = DE : BC", "hint": "전체에 대한 비"}, {"text": "{XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AD : DB = {ad} : {db}, AE : EC = {ae} : {ec}가 같은 비 {u} : {w - u}이고, DE : BC = {de} : {bc} = {u} : {w} = AD : AB다. 답은 {ans_v} cm다.",
        model_answer="BC ∥ DE이므로 AD : DB = AE : EC이고 AD : AB = DE : BC이다. {F1}{v1} × [[frac({(w - u)*i1 + u*i2 + w*i3}, {u*i1 + w*i2 + u*i3})]] = {ans_v}이므로 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "비례 관계", "points": 3, "criterion": "BC ∥ DE에서 {LAW}를 바르게 세웠다.", "partial": "부분의 비와 전체의 비를 섞어 썼으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "비례식을 풀어 {XS} = {ans_v}{eul(ans_v)} 구했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def pr_t2():
    # l ∥ m ∥ n: AB = u·m, BC = w·m (왼쪽 횡단선), DE = u·n, EF = w·n
    rows = {"EF": {"XS": "EF", "i1": 1, "XEF": "x", "XDE": "", "G3T": "[[seg(DE)]] = ", "F1": "EF = ", "LAW": "AB : BC = DE : EF"},
            "DE": {"XS": "DE", "i1": 0, "XEF": "", "XDE": "x", "G3T": "[[seg(EF)]] = ", "F1": "DE = ", "LAW": "AB : BC = DE : EF"}}
    pts = {"A": [0, 0], "B": [0, "{-ab}"], "C": [0, "{-ab - bc}"], "D": ["{dx0}", 0], "E": ["{dx0 + ab*0.45}", "{-ab}"], "F": ["{dx0 + (ab + bc)*0.45}", "{-ab - bc}"],
           "L1": [-1.5, 0], "L2": ["{dx0 + (ab + bc)*0.45 + 1.5}", 0], "M1": [-1.5, "{-ab}"], "M2": ["{dx0 + (ab + bc)*0.45 + 1.5}", "{-ab}"], "N1": [-1.5, "{-ab - bc}"], "N2": ["{dx0 + (ab + bc)*0.45 + 1.5}", "{-ab - bc}"]}
    segs = [["L1", "L2"], ["M1", "M2"], ["N1", "N2"], lseg("A", "B", "{ab}"), lseg("B", "C", "{bc}"), lseg("E", "D", "{lde}"), lseg("F", "E", "{lef}"), ["A", "C"], ["D", "F"],
            lseg("E", "D", "{XDE}"), lseg("F", "E", "{XEF}")]
    labels = [{"at": "L1", "text": "l", "dx": -10, "dy": 4, "k": "lbl:l"}, {"at": "M1", "text": "m", "dx": -10, "dy": 4, "k": "lbl:m"}, {"at": "N1", "text": "n", "dx": -10, "dy": 4, "k": "lbl:n"}]
    return tpl("m2-2-parallel-ratio", 2, PR,
        title="평행선 사이의 선분의 길이의 비 — l ∥ m ∥ n",
        skill="세 평행선이 두 직선을 같은 비로 자름(AB : BC = DE : EF)을 쓰기",
        variant_axis={"구하는 것": "EF / DE", "비": "12쌍 × 배율 1~3"},
        discriminates="평행선 사이의 선분의 비가 같음을 쓰되 대응 위치(위 : 아래)를 맞추는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80, process="절차수행",
        prereq=["평행한 세 직선이 두 직선과 만나서 생기는 선분의 길이의 비는 같다"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "r", "values": {"in": list(RATIOS)}}, {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 3]}}],
        table=[{"key": "wv", "rows": rows}, {"key": "r", "rows": RATIOS}],
        derive={"ab": "u*m", "bc": "w*m", "de": "u*n", "ef": "w*n", "ans_v": "w*n*i1 + u*n*(1 - i1)", "g3": "u*n*i1 + w*n*(1 - i1)", "lde": "u*n*i1", "lef": "w*n*(1 - i1)", "dx0": "3", "v1": "u*n*i1 + w*n*(1 - i1)"},
        constraints=["m != n", "ab + bc <= 21", "ans_v != ab", "ans_v != bc", "ans_v != g3"],
        cost_values=["ab", "bc", "g3", "ans_v"],
        answer_var="ans_v",
        verify=["ab*ef == bc*de", "(i1 == 1 and ans == ef) or (i1 == 0 and ans == de)"],
        question="다음 그림에서 세 직선 l, m, n이 평행하고(l ∥ m ∥ n) [[seg(AB)]] = {ab} cm, [[seg(BC)]] = {bc} cm, {G3T}{g3} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, labels=labels, nodot=["L1", "L2", "M1", "M2", "N1", "N2"]),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="평행한 세 직선이 두 직선과 만나면 잘린 선분의 길이의 비가 같다: AB : BC = DE : EF. 왼쪽 직선에서 위·아래 토막의 비 {ab} : {bc} = {u} : {w}가 오른쪽 직선에서도 그대로다. (점 A를 지나고 DF에 평행한 직선을 그으면 삼각형과 평행선의 성질로 돌아간다.)",
        sol1_fig=scene(pts, [["L1", "L2"], ["M1", "M2"], ["N1", "N2"], lseg("A", "B", "{ab}"), lseg("B", "C", "{bc}"), lseg("E", "D", "{de}"), lseg("F", "E", "{ef}"), ["A", "C"], ["D", "F"]],
                       labels=labels, nodot=["L1", "L2", "M1", "M2", "N1", "N2"]),
        sol1_anim=[[hl("seg:A-B", "seg:B-C", "seglbl:A-B", "seglbl:B-C", keep=True)], [hl("seg:E-D", "seg:F-E", "seglbl:E-D", "seglbl:F-E")]],
        sol2=[
            "l ∥ m ∥ n이므로 AB : BC = DE : EF",
            "{ab} : {bc} = {u} : {w}",
            "{F1}{v1} × [[frac({w*i1 + u*(1 - i1)}, {u*i1 + w*(1 - i1)})]] = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AB : BC = DE : EF", "hint": "l ∥ m ∥ n"}, {"text": "{ab} : {bc} = {u} : {w}", "hint": "왼쪽 비"}, {"text": "{XS} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="DE : EF = {de} : {ef} = {u} : {w} = AB : BC로 비가 맞는다. 답은 {ans_v} cm다.",
        model_answer="l ∥ m ∥ n이므로 AB : BC = DE : EF이다. {ab} : {bc} = {u} : {w}이므로 {F1}{v1} × [[frac({w*i1 + u*(1 - i1)}, {u*i1 + w*(1 - i1)})]] = {ans_v}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "비례 관계", "points": 3, "criterion": "l ∥ m ∥ n에서 AB : BC = DE : EF를 세웠다.", "partial": "대응 위치를 바꿔 AB : BC = EF : DE로 두었으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "비례식을 풀어 {XS} = {ans_v}{eul(ans_v)} 구했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def pr_t3():
    rows = {"DE": {"XS": "DE", "isD": 1, "XDE": "x", "XBC": "", "G1T": "[[seg(BC)]] = ", "F1": "DE = [[frac(1, 2)]]BC = [[frac(1, 2)]] × ", "LAW": "DE = ½BC"},
            "BC": {"XS": "BC", "isD": 0, "XDE": "", "XBC": "x", "G1T": "[[seg(DE)]] = ", "F1": "BC = 2DE = 2 × ", "LAW": "BC = 2DE"}}
    pts = {"A": [0, 0], "B": ["{-ab*sin(pi*33/180)}", "{-ab*cos(pi*33/180)}"], "C": ["{ac*sin(pi*37/180)}", "{-ac*cos(pi*37/180)}"],
           "D": ["{-ab*sin(pi*33/180)/2}", "{-ab*cos(pi*33/180)/2}"], "E": ["{ac*sin(pi*37/180)/2}", "{-ac*cos(pi*37/180)/2}"]}
    segs = [["A", "B"], ["A", "C"], lseg("B", "C", "{lbc}"), lseg("E", "D", "{lde}"), lseg("B", "C", "{XBC}"), lseg("E", "D", "{XDE}")]
    marks = {"eq": [[["A", "D"], ["D", "B"]], [["A", "E"], ["E", "C"]]]}
    return tpl("m2-2-parallel-ratio", 3, PR,
        title="삼각형의 두 변의 중점을 연결한 선분 — DE = ½BC",
        skill="두 변의 중점을 이은 선분은 나머지 변과 평행하고 길이는 그 절반임을 쓰기",
        variant_axis={"구하는 것": "DE / BC", "BC": "4~40"},
        discriminates="중점연결정리를 2배·절반 방향에 맞게 쓰는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=60, process="절차수행",
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "h", "values": {"int": [2, 20]}}],
        table={"key": "wv", "rows": rows},
        derive={"bc": "2*h", "de": "h", "ans_v": "h*isD + 2*h*(1 - isD)", "g1": "2*h*isD + h*(1 - isD)", "lbc": "2*h*isD", "lde": "h*(1 - isD)",
                "ab": "2*h*8/9", "ac": "2*h*8/9"},
        constraints=[],
        cost_values=["g1", "ans_v"],
        answer_var="ans_v",
        verify=["bc == 2*de", "(isD == 1 and ans == de) or (isD == 0 and ans == bc)"],
        question="다음 그림의 △ABC에서 두 점 D, E는 각각 변 AB, AC의 중점이다. {G1T}{g1} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="D, E가 각각 AB, AC의 중점이므로 AD : AB = AE : AC = 1 : 2다. 그러면 △ADE ∽ △ABC(SAS)이고 닮음비가 1 : 2이므로 DE ∥ BC, DE = [[frac(1, 2)]]BC — 삼각형의 두 변의 중점을 연결한 선분의 성질이다.",
        sol1_fig=scene(pts, [["A", "B"], ["A", "C"], lseg("B", "C", "{bc}"), lseg("E", "D", "{de}")], marks={**marks, "arc": [arc("D", "E", "B", "•", "arc:d"), arc("B", "C", "A", "•", "arc:b")]}, shade=[["A", "D", "E"]]),
        sol1_anim=[[hl("eq:A-D", "eq:D-B", "eq:A-E", "eq:E-C", keep=True)], [hl("shade:0", "arc:d", "arc:b", keep=True)], [hl("seglbl:E-D", "seglbl:B-C")]],
        sol2=[
            "D, E가 AB, AC의 중점이므로 AD : AB = AE : AC = 1 : 2",
            "△ADE ∽ △ABC (닮음비 1 : 2)이므로 DE ∥ BC, DE : BC = 1 : 2",
            "{F1}{g1} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AD : AB = AE : AC = 1 : 2", "hint": "중점"}, {"text": "DE = [[frac(1, 2)]]BC", "hint": "중점연결정리"}, {"text": "{F1}{g1} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="DE = {de} cm, BC = {bc} cm로 BC가 DE의 2배다. 답은 {ans_v} cm다.",
        model_answer="D, E가 각각 AB, AC의 중점이므로 DE ∥ BC이고 DE = [[frac(1, 2)]]BC이다. {F1}{g1} = {ans_v}이므로 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "중점연결정리", "points": 3, "criterion": "두 변의 중점을 이은 선분이 나머지 변의 절반(DE = ½BC)임을 근거와 함께 썼다.", "partial": "관계만 쓰고 근거(닮음비 1 : 2)가 없으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{F1}{g1} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "2배·절반을 거꾸로 했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def pr_t4():
    rows = {"perim": {"Q": "△DEF의 둘레의 길이", "isP": 1, "i1": 0, "i2": 0, "i3": 0, "F1": "(△DEF의 둘레) = [[frac(1, 2)]] × (", "F2": " + ", "F3": " + ", "F4": ")", "LAW": "세 변의 절반의 합"},
            "EF": {"Q": "[[seg(EF)]]의 길이", "isP": 0, "i1": 1, "i2": 0, "i3": 0, "F1": "EF = [[frac(1, 2)]]AB = [[frac(1, 2)]] × ", "F2": "", "F3": "", "F4": "", "LAW": "EF ∥ AB, EF = ½AB"},
            "DF": {"Q": "[[seg(DF)]]의 길이", "isP": 0, "i1": 0, "i2": 1, "i3": 0, "F1": "DF = [[frac(1, 2)]]BC = [[frac(1, 2)]] × ", "F2": "", "F3": "", "F4": "", "LAW": "DF ∥ BC, DF = ½BC"},
            "DE": {"Q": "[[seg(DE)]]의 길이", "isP": 0, "i1": 0, "i2": 0, "i3": 1, "F1": "DE = [[frac(1, 2)]]CA = [[frac(1, 2)]] × ", "F2": "", "F3": "", "F4": "", "LAW": "DE ∥ CA, DE = ½CA"}}
    # D∈AB, E∈BC, F∈CA 중점. 세 변 a = BC, b = CA, c = AB (짝수)
    pts = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": ["{a}", 0], "D": ["{ax/2}", "{ay/2}"], "E": ["{a/2}", 0], "F": ["{(ax + a)/2}", "{ay/2}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["D", "E"], ["E", "F"], ["F", "D"]]
    marks = {"eq": [[["A", "D"], ["D", "B"]], [["B", "E"], ["E", "C"]], [["C", "F"], ["F", "A"]]]}
    sidelab = [{"at": ["{ax/4}", "{ay/4}"], "text": "{c} cm", "dx": -22, "dy": 4, "k": "lbl:c"}, {"at": ["{a/4}", 0], "text": "{a} cm", "dx": 0, "dy": 15, "k": "lbl:a"},
               {"at": ["{a + (ax - a)/4}", "{ay/4}"], "text": "{b} cm", "dx": 24, "dy": 4, "k": "lbl:b"}]
    return tpl("m2-2-parallel-ratio", 4, PR,
        title="세 변의 중점을 연결한 삼각형 — 둘레와 변",
        skill="각 변의 중점을 이은 선분이 마주 보는 변의 절반이므로 △DEF의 둘레가 △ABC의 절반임을 쓰기",
        variant_axis={"구하는 것": "둘레 / EF / DF / DE", "세 변": "짝수 6~20"},
        discriminates="중점연결선분을 마주 보는(평행한) 변과 짝짓는가(EF ↔ AB 등)",
        qtype="short", difficulty=2, pool_target=300, time_limit=80, process="절차수행",
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "a2", "values": {"int": [3, 10]}}, {"name": "b2", "values": {"int": [3, 10]}}, {"name": "c2", "values": {"int": [3, 10]}}],
        table={"key": "wv", "rows": rows},
        derive={"a": "2*a2", "b": "2*b2", "c": "2*c2", "P": "a + b + c", "ans_v": "(a2 + b2 + c2)*isP + c2*i1 + a2*i2 + b2*i3",
                "v1": "c*(isP + i1) + a*i2 + b*i3", "v2": "a*isP", "v3": "b*isP", "ax": "(a*a + c*c - b*b)/(2*a)", "ay": "sqrt(abs(c*c - ax*ax))"},
        constraints=["a2 != b2", "b2 != c2", "a2 != c2", "a2 + b2 > c2", "b2 + c2 > a2", "a2 + c2 > b2", "ans_v != a", "ans_v != b", "ans_v != c"],
        cost_values=["a", "b", "c", "ans_v"],
        answer_var="ans_v",
        verify=["2*ans_v == P or isP == 0", "(isP == 1 and ans == P/2) or (i1 == 1 and 2*ans == c) or (i2 == 1 and 2*ans == a) or (i3 == 1 and 2*ans == b)"],
        question="다음 그림의 △ABC에서 세 점 D, E, F는 각각 변 AB, BC, CA의 중점이다. [[seg(AB)]] = {c} cm, [[seg(BC)]] = {a} cm, [[seg(CA)]] = {b} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=sidelab),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="두 변의 중점을 이은 선분은 나머지 변과 평행하고 길이는 그 절반이다. D, E가 AB, BC의 중점이므로 DE = [[frac(1, 2)]]CA, 마찬가지로 EF = [[frac(1, 2)]]AB, FD = [[frac(1, 2)]]BC — 각 선분은 자신과 마주 보는 변의 절반이다. 그래서 △DEF의 둘레는 △ABC의 둘레의 절반이다.",
        sol1_fig=scene(pts, segs, marks=marks, labels=sidelab + [{"at": ["{(ax/2 + a/2)/2}", "{ay/4}"], "text": "{b2}", "dx": -8, "dy": 4, "accent": True, "k": "lbl:de"},
                                                          {"at": ["{(a/2 + (ax + a)/2)/2}", "{ay/4}"], "text": "{c2}", "dx": 8, "dy": 4, "accent": True, "k": "lbl:ef"},
                                                          {"at": ["{(ax/2 + (ax + a)/2)/2}", "{ay/2}"], "text": "{a2}", "dx": 0, "dy": 14, "accent": True, "k": "lbl:fd"}]),
        sol1_anim=[[hl("seg:D-E", "lbl:de", "seg:C-A", keep=True)], [hl("seg:E-F", "lbl:ef", "seg:A-B", keep=True)], [hl("seg:F-D", "lbl:fd", "seg:B-C", keep=True)]],
        sol2=[
            "중점연결정리: DE = [[frac(1, 2)]]CA = {b2}, EF = [[frac(1, 2)]]AB = {c2}, FD = [[frac(1, 2)]]BC = {a2}",
            "{F1}{v1}{F2}{v2}{F3}{v3}{F4} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "DE = {b2}, EF = {c2}, FD = {a2}", "hint": "마주 보는 변의 절반"}, {"text": "{Q}: {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="△DEF의 둘레 {a2} + {b2} + {c2} = {a2 + b2 + c2}(cm)는 △ABC의 둘레 {P} cm의 절반이다. 답은 {ans_v} cm다.",
        model_answer="두 변의 중점을 이은 선분은 나머지 변의 절반이므로 DE = {b2} cm, EF = {c2} cm, FD = {a2} cm이다. {F1}{v1}{F2}{v2}{F3}{v3}{F4} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "중점연결정리", "points": 3, "criterion": "각 중점연결선분이 마주 보는 변의 절반임을 바르게 짝지어 썼다.", "partial": "한 쌍을 잘못 짝지었으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{F1}{v1}{F2}{v2}{F3}{v3}{F4} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "절반을 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def pr_t5():
    rows = {"perim": {"Q": "□EFGH의 둘레의 길이", "isP": 1, "XBD": "", "G2T": "[[seg(BD)]] = ", "G2U": " cm", "F1": "(둘레) = AC + BD = ", "F2": " + ", "LAW": "둘레 = AC + BD"},
            "bd": {"Q": "[[seg(BD)]]의 길이", "isP": 0, "XBD": "x", "G2T": "□EFGH의 둘레의 길이가 ", "G2U": " cm", "F1": "BD = (둘레) − AC = ", "F2": " − ", "LAW": "둘레 = AC + BD"}}
    pts = {"A": [1.5, 5], "B": [0, 0], "C": [7, 0], "D": [6.5, 4.2], "E": [0.75, 2.5], "F": [3.5, 0], "G": [6.75, 2.1], "H": [4, 4.6], "K": [4.875, 3.15]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["E", "F"], ["F", "G"], ["G", "H"], ["H", "E"], {"a": "A", "b": "C", "dash": True}, {"a": "B", "b": "K", "dash": True}, {"a": "K", "b": "D", "dash": True, "label": "{lbd}"}, lseg("K", "D", "{XBD}")]
    aclab = [{"at": [2.875, 3.75], "text": "{p} cm", "dx": 22, "dy": 2, "k": "lbl:ac"}]
    marks = {"eq": [[["A", "E"], ["E", "B"]], [["B", "F"], ["F", "C"]], [["C", "G"], ["G", "D"]], [["D", "H"], ["H", "A"]]]}
    return tpl("m2-2-parallel-ratio", 5, PR,
        title="사각형의 네 변의 중점을 연결한 사각형 — 둘레 = 두 대각선의 합",
        skill="각 삼각형에서 중점연결정리를 써서 □EFGH의 각 변이 대각선의 절반임을 밝히기",
        variant_axis={"구하는 것": "둘레 / BD", "대각선": "4~14"},
        discriminates="EF = HG = ½AC, EH = FG = ½BD(평행사변형)로 둘레가 두 대각선의 합임을 쓰는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "p", "values": {"int": [4, 14]}}, {"name": "q", "values": {"int": [4, 14]}}],
        table={"key": "wv", "rows": rows},
        derive={"P": "p + q", "ans_v": "(p + q)*isP + q*(1 - isP)", "g2": "q*isP + (p + q)*(1 - isP)", "lbd": "q*isP", "v1": "p*isP + (p + q)*(1 - isP)", "v2": "q*isP + p*(1 - isP)"},
        constraints=["p != q", "ans_v != p", "ans_v != g2"],
        cost_values=["p", "g2", "ans_v"],
        answer_var="ans_v",
        verify=["P == p + q", "(isP == 1 and ans == P) or (isP == 0 and ans == q)"],
        question="다음 그림의 □ABCD에서 네 점 E, F, G, H는 각각 변 AB, BC, CD, DA의 중점이다. [[seg(AC)]] = {p} cm이고 {G2T}{g2}{G2U}일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=aclab, nodot=["K"]),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="대각선 AC를 그으면 △ABC에서 E, F가 두 변의 중점이므로 EF ∥ AC, EF = [[frac(1, 2)]]AC이고, △ACD에서도 HG ∥ AC, HG = [[frac(1, 2)]]AC다. 대각선 BD에 대해서도 EH = FG = [[frac(1, 2)]]BD. 그래서 □EFGH는 평행사변형이고 둘레는 2 × ([[frac(1, 2)]]AC + [[frac(1, 2)]]BD) = AC + BD다.",
        sol1_fig=scene(pts, [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["E", "F"], ["F", "G"], ["G", "H"], ["H", "E"], {"a": "A", "b": "C", "dash": True}, {"a": "B", "b": "K", "dash": True}, {"a": "K", "b": "D", "dash": True, "label": "{q} cm"}],
                       marks={**marks, "eq": marks["eq"] + [[["E", "F"], ["H", "G"]], [["E", "H"], ["F", "G"]]]}, shade=[["A", "B", "C"]], labels=aclab, nodot=["K"]),
        sol1_anim=[[hl("shade:0", "seg:A-C", keep=True)], [hl("seg:E-F", "seg:H-G", "eq:E-F", "eq:H-G", keep=True)], [hl("seg:E-H", "seg:F-G", "eq:E-H", "eq:F-G", "seg:D-B")]],
        sol2=[
            "△ABC, △ACD에서 중점연결정리: EF = HG = [[frac(1, 2)]]AC",
            "△ABD, △BCD에서 중점연결정리: EH = FG = [[frac(1, 2)]]BD",
            "□EFGH의 둘레 = 2 × ([[frac(1, 2)]]AC + [[frac(1, 2)]]BD) = AC + BD",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "EF = HG = [[frac(1, 2)]]AC", "hint": "△ABC, △ACD"}, {"text": "EH = FG = [[frac(1, 2)]]BD", "hint": "△ABD, △BCD"}, {"text": "둘레 = AC + BD", "hint": "{LAW}"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3)], []],
        sol_check="AC = {p} cm, BD = {q} cm이면 □EFGH의 네 변은 {p/2}, {q/2}, {p/2}, {q/2}(cm)로 둘레가 {P} cm다. 답은 {ans_v} cm다.",
        model_answer="중점연결정리에 의해 EF = HG = [[frac(1, 2)]]AC, EH = FG = [[frac(1, 2)]]BD이므로 □EFGH의 둘레는 AC + BD이다. {F1}{v1}{F2}{v2} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "중점연결정리", "points": 3, "criterion": "대각선을 그어 EF = HG = ½AC, EH = FG = ½BD임을 밝혔다.", "partial": "한 대각선에 대해서만 밝혔으면 1점."},
            {"element": "둘레 식", "points": 2, "criterion": "둘레 = AC + BD를 세워 {F1}{v1}{F2}{v2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "절반을 빠뜨려 2(AC + BD)로 두었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


PR_SEED = {
    "seed_id": "m2-2-parallel-ratio", "category": "도형",
    "title": "평행선과 선분의 길이의 비 — BC ∥ DE, 세 평행선, 중점연결정리(삼각형·둘레·사각형)",
    "unit_id": "m2-2", "concept_ids": ["m2-2-07"],
    "schema_id": SCHEMA_PR, "schema_name": "평행선과 선분의 길이비 / 삼각형 중점연결정리 / 사각형 중점연결",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 7.3)을 참고해 새로 씀. 비는 u : w 와 배율의 곱으로 정수화, 좌표는 길이 그대로. 세 평행선(t2)의 오른쪽 횡단선은 기울기를 고정해 그려 비만 맞다(길이는 축척 아님).",
    "geometry": True,
    "templates": [pr_t1(), pr_t2(), pr_t3(), pr_t4(), pr_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 4. 삼각형의 무게중심
CG = dict(prereq=["무게중심: 세 중선의 교점, 각 중선을 꼭짓점으로부터 2 : 1로 나눈다", "중선은 삼각형의 넓이를 이등분한다"], ops=["비례", "넓이"], tags=["무게중심", "중선"])
CG_PTS = {"A": [1.2, 5], "B": [0, 0], "C": [6, 0], "D": [3, 0], "E": [3.6, 2.5], "F": [0.6, 2.5], "G": [2.4, "{5/3}"]}


def cg_t1():
    rows = {"AD-AG": {"XS": "AG", "GT": "[[seg(AD)]] = ", "i": 1, "j": 1, "XAG": "x", "XGD": "", "F1": "AG = [[frac(2, 3)]]AD = [[frac(2, 3)]] × ", "LAW": "AG : AD = 2 : 3"},
            "AD-GD": {"XS": "GD", "GT": "[[seg(AD)]] = ", "i": 1, "j": 0, "XAG": "", "XGD": "x", "F1": "GD = [[frac(1, 3)]]AD = [[frac(1, 3)]] × ", "LAW": "GD : AD = 1 : 3"},
            "AG-GD": {"XS": "GD", "GT": "[[seg(AG)]] = ", "i": 2, "j": 0, "XAG": "", "XGD": "x", "F1": "GD = [[frac(1, 2)]]AG = [[frac(1, 2)]] × ", "LAW": "AG : GD = 2 : 1"},
            "AG-AD": {"XS": "AD", "GT": "[[seg(AG)]] = ", "i": 2, "j": 2, "XAG": "", "XGD": "", "F1": "AD = [[frac(3, 2)]]AG = [[frac(3, 2)]] × ", "LAW": "AG : AD = 2 : 3"},
            "GD-AG": {"XS": "AG", "GT": "[[seg(GD)]] = ", "i": 3, "j": 1, "XAG": "x", "XGD": "", "F1": "AG = 2GD = 2 × ", "LAW": "AG : GD = 2 : 1"},
            "GD-AD": {"XS": "AD", "GT": "[[seg(GD)]] = ", "i": 3, "j": 2, "XAG": "", "XGD": "", "F1": "AD = 3GD = 3 × ", "LAW": "GD : AD = 1 : 3"}}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], lseg("A", "G", "{lag}"), lseg("G", "D", "{lgd}"), lseg("A", "G", "{XAG}"), lseg("G", "D", "{XGD}"), ["B", "E"], ["C", "F"]]
    marks = {"eq": [[["B", "D"], ["D", "C"]]]}
    return tpl("m2-2-centroid", 1, CG,
        title="무게중심 — 중선을 2 : 1로 나눈다",
        skill="AG : GD = 2 : 1을 써서 AD, AG, GD 사이를 오가기",
        variant_axis={"주어진 것 → 구하는 것": "AD → AG / AD → GD / AG → GD / AG → AD / GD → AG / GD → AD", "GD": "2~9"},
        discriminates="2 : 1의 방향(꼭짓점 쪽이 2)을 지키고 전체 AD가 3등분임을 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=60, process="절차수행",
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "k", "values": {"int": [2, 9]}}],
        table={"key": "wv", "rows": rows},
        derive={"ag": "2*k", "gd": "k", "ad": "3*k", "gv": "3*k*(i == 1) + 2*k*(i == 2) + k*(i == 3)", "ans_v": "2*k*(j == 1) + k*(j == 0) + 3*k*(j == 2)",
                "lag": "2*k*(i == 2)", "lgd": "k*(i == 3)"},
        constraints=[],
        cost_values=["gv", "ans_v"],
        answer_var="ans_v",
        verify=["ag == 2*gd", "ad == ag + gd", "ans == ans_v"],
        question="다음 그림에서 점 G는 △ABC의 무게중심이고 점 D는 변 BC의 중점이다. {GT}{gv} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(CG_PTS, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="무게중심 G는 세 중선의 교점이고, 각 중선을 꼭짓점 쪽부터 2 : 1로 나눈다: AG : GD = 2 : 1. 즉 중선 AD를 3등분했을 때 AG는 2칸, GD는 1칸이다. 주어진 길이가 몇 칸인지 보고 한 칸의 길이 {k} cm를 구하면 나머지가 나온다.",
        sol1_fig=scene(CG_PTS, [["A", "B"], ["B", "C"], ["C", "A"], lseg("A", "G", "{ag}"), lseg("G", "D", "{gd}"), ["B", "E"], ["C", "F"]], marks=marks,
                       labels=[{"at": "G", "text": "2 : 1", "dx": 26, "dy": 4, "accent": True, "k": "lbl:ratio"}]),
        sol1_anim=[[hl("seg:B-E", "seg:C-F", keep=True)], [hl("seg:A-G", "seg:G-D", "lbl:ratio", keep=True)], [hl("seglbl:A-G", "seglbl:G-D")]],
        sol2=[
            "점 G가 무게중심이므로 AG : GD = 2 : 1, 곧 AG = [[frac(2, 3)]]AD, GD = [[frac(1, 3)]]AD",
            "{F1}{gv} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AG : GD = 2 : 1", "hint": "무게중심"}, {"text": "{F1}{gv} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="AG = {ag} cm, GD = {gd} cm, AD = {ad} cm로 AG : GD = 2 : 1이고 AG + GD = AD다. 답은 {ans_v} cm다.",
        model_answer="점 G는 무게중심이므로 AG : GD = 2 : 1이다. {F1}{gv} = {ans_v}이므로 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "무게중심의 성질", "points": 3, "criterion": "AG : GD = 2 : 1(꼭짓점 쪽이 2)임을 밝혔다.", "partial": "비의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "{F1}{gv} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "AD를 2등분으로 보았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def cg_t2():
    rows = {"gbc": {"Q": "△GBC의 넓이", "GT": "△ABC의 넓이가 ", "i": 0, "j": 1, "S1": "G", "S2": "B", "S3": "C", "F1": "△GBC = [[frac(1, 3)]]△ABC = [[frac(1, 3)]] × ", "LAW": "세 중선이 넓이를 3등분"},
            "gbd": {"Q": "△GBD의 넓이", "GT": "△ABC의 넓이가 ", "i": 0, "j": 2, "S1": "G", "S2": "B", "S3": "D", "F1": "△GBD = [[frac(1, 6)]]△ABC = [[frac(1, 6)]] × ", "LAW": "6등분 중 하나"},
            "abc6": {"Q": "△ABC의 넓이", "GT": "△GBD의 넓이가 ", "i": 2, "j": 0, "S1": "G", "S2": "B", "S3": "D", "F1": "△ABC = 6△GBD = 6 × ", "LAW": "△GBD = ⅙△ABC"},
            "abc3": {"Q": "△ABC의 넓이", "GT": "△GBC의 넓이가 ", "i": 1, "j": 0, "S1": "G", "S2": "B", "S3": "C", "F1": "△ABC = 3△GBC = 3 × ", "LAW": "△GBC = ⅓△ABC"}}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["A", "D"], ["B", "E"], ["C", "F"]]
    marks = {"eq": [[["B", "D"], ["D", "C"]], [["C", "E"], ["E", "A"]], [["A", "F"], ["F", "B"]]]}
    return tpl("m2-2-centroid", 2, CG,
        title="무게중심과 넓이 — △GBC = ⅓△ABC, △GBD = ⅙△ABC",
        skill="중선이 넓이를 이등분하고 AG : GD = 2 : 1이므로 세 중선이 삼각형을 넓이가 같은 6개로 나눔을 쓰기",
        variant_axis={"구하는 것": "△GBC / △GBD / △ABC(⅙에서) / △ABC(⅓에서)", "넓이": "6의 배수 12~60"},
        discriminates="G와 세 꼭짓점을 이은 세 삼각형의 넓이가 같고(⅓), 중선이 다시 이등분(⅙)함을 근거와 함께 쓰는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90, process="문제해결",
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "k", "values": {"int": [2, 10]}}],
        table={"key": "wv", "rows": rows},
        derive={"S": "6*k", "gbc": "2*k", "gbd": "k", "gv": "6*k*(i == 0) + 2*k*(i == 1) + k*(i == 2)", "ans_v": "6*k*(j == 0) + 2*k*(j == 1) + k*(j == 2)"},
        constraints=[],
        cost_values=["gv", "ans_v"],
        answer_var="ans_v",
        verify=["S == 3*gbc", "S == 6*gbd", "ans == ans_v"],
        question="다음 그림에서 점 G는 △ABC의 무게중심이고 세 점 D, E, F는 각각 변 BC, CA, AB의 중점이다. {GT}{gv} cm²일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(CG_PTS, segs, marks=marks, shade=[["{S1}", "{S2}", "{S3}"]]),
        answer="{ans_v}", answer_alt=["{ans_v} cm²"],
        sol1="중선 AD는 밑변을 이등분하므로 △ABD = △ADC = [[frac(1, 2)]]△ABC다. 또 AG : GD = 2 : 1이므로 △GBD = [[frac(1, 3)]]△ABD = [[frac(1, 6)]]△ABC, △GBC = 2△GBD = [[frac(1, 3)]]△ABC — 세 중선은 삼각형을 넓이가 같은 6조각으로 나눈다.",
        sol1_fig=scene(CG_PTS, segs, marks=marks, shade=[["G", "B", "D"], ["G", "D", "C"], ["G", "C", "E"], ["G", "E", "A"], ["G", "A", "F"], ["G", "F", "B"]],
                       labels=[{"at": ["{(2.4 + 0 + 3)/3}", "{(5/3)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:1"}, {"at": ["{(2.4 + 3 + 6)/3}", "{(5/3)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:2"},
                               {"at": ["{(2.4 + 6 + 3.6)/3}", "{(5/3 + 2.5)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:3"}, {"at": ["{(2.4 + 3.6 + 1.2)/3}", "{(5/3 + 2.5 + 5)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:4"},
                               {"at": ["{(2.4 + 1.2 + 0.6)/3}", "{(5/3 + 5 + 2.5)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:5"}, {"at": ["{(2.4 + 0.6 + 0)/3}", "{(5/3 + 2.5)/3}"], "text": "{k}", "dx": 0, "dy": 4, "accent": True, "k": "lbl:6"}]),
        sol1_anim=[[hl("seg:A-D", keep=True)], [hl("shade:0", "shade:1", "lbl:1", "lbl:2", keep=True)], [hl("shade:2", "shade:3", "shade:4", "shade:5", "lbl:3", "lbl:4", "lbl:5", "lbl:6")]],
        sol2=[
            "중선 AD가 넓이를 이등분: △ABD = [[frac(1, 2)]]△ABC",
            "AG : GD = 2 : 1이므로 △GBD = [[frac(1, 3)]]△ABD = [[frac(1, 6)]]△ABC, 같은 이유로 △GBC = △GBD + △GDC = [[frac(1, 3)]]△ABC",
            "{F1}{gv} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm²",
        ],
        sol2_fig=steps([{"text": "△ABD = [[frac(1, 2)]]△ABC", "hint": "중선"}, {"text": "△GBD = [[frac(1, 6)]]△ABC, △GBC = [[frac(1, 3)]]△ABC", "hint": "AG : GD = 2 : 1"}, {"text": "{F1}{gv} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="△ABC = {S} cm²이면 6조각이 각각 {k} cm², △GBC = {gbc} cm², △GBD = {gbd} cm²로 서로 맞는다. 답은 {ans_v} cm²다.",
        model_answer="중선은 넓이를 이등분하고 AG : GD = 2 : 1이므로 △GBD = [[frac(1, 6)]]△ABC, △GBC = [[frac(1, 3)]]△ABC이다. {F1}{gv} = {ans_v}이므로 {Q}{eun(Q)} {ans_v} cm²다.",
        rubric=[
            {"element": "넓이 관계", "points": 3, "criterion": "중선의 이등분과 2 : 1을 근거로 △GBD = ⅙△ABC(△GBC = ⅓△ABC)임을 밝혔다.", "partial": "관계만 쓰고 근거가 없으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{F1}{gv} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "⅓과 ⅙을 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm²를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def cg_t3():
    rows = {"bg": {"XS": "BG", "isB": 1, "XBG": "x", "XAC": "", "GT": "[[seg(AC)]] = ", "F1": "BG = [[frac(2, 3)]]BD = [[frac(2, 3)]] × [[frac(1, 2)]] × ", "LAW": "BG = ⅔BD, BD = ½AC"},
            "ac": {"XS": "AC", "isB": 0, "XBG": "", "XAC": "x", "GT": "[[seg(BG)]] = ", "F1": "AC = 2BD = 2 × [[frac(3, 2)]] × ", "LAW": "BD = 3/2 BG, AC = 2BD"}}
    pts = {"A": [0, "{1.8*k}"], "B": [0, 0], "C": ["{2.4*k}", 0], "D": ["{1.2*k}", "{0.9*k}"], "G": ["{0.8*k}", "{0.6*k}"]}
    segs = [["A", "B"], ["B", "C"], ["A", "D"], lseg("D", "C", "{lac}"), ["B", "D"], lseg("B", "G", "{lbg}"), lseg("D", "C", "{XAC}"), lseg("B", "G", "{XBG}")]
    marks = {"right": [["A", "B", "C"]], "eq": [[["A", "D"], ["D", "C"]]]}
    return tpl("m2-2-centroid", 3, CG,
        title="직각삼각형의 무게중심 — 빗변의 중점과 BG",
        skill="빗변의 중점 D는 외심이므로 BD = ½AC이고, 무게중심에서 BG = ⅔BD임을 이어 쓰기",
        variant_axis={"구하는 것": "BG / AC", "AC": "3의 배수 6~27"},
        discriminates="직각삼각형의 외심(빗변의 중점)과 무게중심의 성질 두 가지를 이어 쓰는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90, process="문제해결",
        prereq=["직각삼각형의 외심은 빗변의 중점(BD = AD = CD)", "무게중심은 중선을 2 : 1로 나눈다"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "k", "values": {"int": [2, 9]}}],
        table={"key": "wv", "rows": rows},
        derive={"ac": "3*k", "bd": "3*k/2", "bg": "k", "ans_v": "k*isB + 3*k*(1 - isB)", "gv": "3*k*isB + k*(1 - isB)", "lac": "3*k*isB", "lbg": "k*(1 - isB)"},
        constraints=[],
        cost_values=["gv", "bd", "ans_v"],
        answer_var="ans_v",
        verify=["2*bd == ac", "3*bg == 2*bd", "(isB == 1 and ans == bg) or (isB == 0 and ans == ac)"],
        question="다음 그림과 같이 [[angle(B)]] = [[deg(90)]]인 직각삼각형 ABC에서 점 D는 빗변 AC의 중점이고 점 G는 △ABC의 무게중심이다. {GT}{gv} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="직각삼각형의 외심은 빗변의 중점이므로 D에서 세 꼭짓점까지의 거리가 같다: BD = AD = CD = [[frac(1, 2)]]AC. 한편 BD는 중선이고 G는 무게중심이므로 BG : GD = 2 : 1, BG = [[frac(2, 3)]]BD. 두 성질을 이으면 BG = [[frac(2, 3)]] × [[frac(1, 2)]]AC = [[frac(1, 3)]]AC다.",
        sol1_fig=scene(pts, [["A", "B"], ["B", "C"], ["A", "D"], lseg("D", "C", "{ac}"), ["B", "D"], lseg("B", "G", "{bg}"), {"a": "G", "b": "D", "label": "{bd - bg}"}], marks={**marks, "eq": [[["A", "D"], ["D", "C"], ["D", "B"]]]},
                       labels=[{"at": "D", "text": "BD = {bd}", "dx": 34, "dy": 14, "accent": True, "k": "lbl:bd"}]),
        sol1_anim=[[hl("right:B", "eq:A-D", "eq:D-C", "eq:D-B", "lbl:bd", keep=True)], [hl("seg:B-G", "seglbl:B-G", "seglbl:G-D")]],
        sol2=[
            "∠B = 90°이므로 빗변의 중점 D는 외심: BD = AD = CD = [[frac(1, 2)]]AC",
            "G는 무게중심이므로 BG : GD = 2 : 1, BG = [[frac(2, 3)]]BD",
            "{F1}{gv} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "BD = [[frac(1, 2)]]AC", "hint": "빗변의 중점 = 외심"}, {"text": "BG = [[frac(2, 3)]]BD", "hint": "무게중심 2 : 1"}, {"text": "{F1}{gv} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="AC = {ac} cm이면 BD = {bd} cm, BG = [[frac(2, 3)]] × {bd} = {bg}(cm)로 BG = [[frac(1, 3)]]AC다. 답은 {ans_v} cm다.",
        model_answer="직각삼각형의 빗변의 중점 D는 외심이므로 BD = [[frac(1, 2)]]AC이고, G는 무게중심이므로 BG = [[frac(2, 3)]]BD이다. {F1}{gv} = {ans_v}이므로 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "외심의 성질", "points": 3, "criterion": "빗변의 중점 D가 외심이므로 BD = ½AC임을 밝혔다.", "partial": "BD = ½AC만 쓰고 근거가 없으면 1점."},
            {"element": "무게중심", "points": 2, "criterion": "BG = ⅔BD를 써서 {F1}{gv} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "2 : 1의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def cg_t4():
    rows = {"oe": {"XS": "OE", "isO": 1, "XOE": "x", "XBD": "", "GT": "[[seg(BD)]] = ", "F1": "OE = [[frac(1, 3)]]OD = [[frac(1, 3)]] × [[frac(1, 2)]] × ", "LAW": "OE = ⅓OD, OD = ½BD"},
            "bd": {"XS": "BD", "isO": 0, "XOE": "", "XBD": "x", "GT": "[[seg(OE)]] = ", "F1": "BD = 2OD = 2 × 3 × ", "LAW": "OD = 3OE, BD = 2OD"}}
    pts = {"A": [1.5, 3.5], "B": [0, 0], "C": [6, 0], "D": [7.5, 3.5], "O": [3.75, 1.75], "M": [6.75, 1.75], "E": [5, "{7/3}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["A", "C"], lseg("B", "O", "{lbd}"), ["O", "D"], ["A", "M"], lseg("O", "E", "{loe}"), lseg("B", "O", "{XBD}"), lseg("O", "E", "{XOE}")]
    marks = {"eq": [[["C", "M"], ["M", "D"]]]}
    return tpl("m2-2-centroid", 4, CG,
        title="평행사변형 속의 무게중심 — 대각선의 교점과 변의 중점",
        skill="△ACD에서 O(AC의 중점)와 M(CD의 중점)이 만드는 두 중선의 교점 E가 무게중심임을 읽기",
        variant_axis={"구하는 것": "OE / BD", "BD": "6의 배수 12~54"},
        discriminates="E가 △ACD의 무게중심이므로 DE : EO = 2 : 1, OE = ⅓OD = ⅙BD임을 세우는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110, process="문제해결",
        prereq=["평행사변형의 대각선은 서로 다른 것을 이등분", "무게중심은 중선을 2 : 1로 나눈다"],
        params=[{"name": "wv", "values": {"in": list(rows)}}, {"name": "k", "values": {"int": [2, 9]}}],
        table={"key": "wv", "rows": rows},
        derive={"bd": "6*k", "od": "3*k", "oe": "k", "ans_v": "k*isO + 6*k*(1 - isO)", "gv": "6*k*isO + k*(1 - isO)", "lbd": "6*k*isO", "loe": "k*(1 - isO)"},
        constraints=[],
        cost_values=["gv", "od", "ans_v"],
        answer_var="ans_v",
        verify=["2*od == bd", "3*oe == od", "(isO == 1 and ans == oe) or (isO == 0 and ans == bd)"],
        question="다음 그림의 평행사변형 ABCD에서 점 O는 두 대각선의 교점, 점 M은 변 CD의 중점이고 점 E는 [[seg(AM)]]과 [[seg(BD)]]의 교점이다. {GT}{gv} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="△ACD를 보자. 평행사변형의 대각선은 서로를 이등분하므로 O는 AC의 중점 — DO는 △ACD의 중선이다. M은 CD의 중점이므로 AM도 중선이고, 두 중선의 교점 E는 △ACD의 무게중심이다. 따라서 DE : EO = 2 : 1, 즉 OE = [[frac(1, 3)]]OD이고 OD = [[frac(1, 2)]]BD다.",
        sol1_fig=scene(pts, [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["A", "C"], lseg("B", "O", "{bd}"), ["A", "M"], lseg("O", "E", "{oe}"), lseg("E", "D", "{2*k}")], marks={"eq": [[["C", "M"], ["M", "D"]], [["A", "O"], ["O", "C"]]]},
                       shade=[["A", "C", "D"]]),
        sol1_anim=[[hl("shade:0", keep=True)], [hl("seg:A-M", "eq:C-M", "eq:M-D", "eq:A-O", "eq:O-C", keep=True)], [hl("seglbl:O-E", "seglbl:E-D")]],
        sol2=[
            "O는 AC의 중점(대각선의 이등분), M은 CD의 중점 → DO, AM은 △ACD의 두 중선",
            "두 중선의 교점 E는 △ACD의 무게중심: DE : EO = 2 : 1, OE = [[frac(1, 3)]]OD",
            "OD = [[frac(1, 2)]]BD이므로 {F1}{gv} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "DO, AM은 △ACD의 중선", "hint": "O, M은 중점"}, {"text": "E = 무게중심, OE = [[frac(1, 3)]]OD", "hint": "DE : EO = 2 : 1"}, {"text": "{F1}{gv} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="BD = {bd} cm이면 OD = {od} cm, OE = {oe} cm, DE = {2*k} cm로 DE : EO = 2 : 1이 맞는다. 답은 {ans_v} cm다.",
        model_answer="O는 AC의 중점이고 M은 CD의 중점이므로 DO와 AM은 △ACD의 중선이고 그 교점 E는 △ACD의 무게중심이다. 따라서 OE = [[frac(1, 3)]]OD = [[frac(1, 6)]]BD이고 {F1}{gv} = {ans_v}이므로 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "무게중심 읽기", "points": 3, "criterion": "DO, AM이 △ACD의 중선이고 E가 무게중심임을 밝혔다.", "partial": "중선 하나만 밝혔으면 1점."},
            {"element": "길이 계산", "points": 2, "criterion": "OE = ⅓OD, OD = ½BD를 이어 {F1}{gv} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "2 : 1의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


CG_SEED = {
    "seed_id": "m2-2-centroid", "category": "도형",
    "title": "삼각형의 무게중심 — 중선의 2 : 1, 넓이의 ⅓·⅙, 직각삼각형, 평행사변형 속의 무게중심",
    "unit_id": "m2-2", "concept_ids": ["m2-2-08"],
    "schema_id": SCHEMA_CG, "schema_name": "삼각형 무게중심 중선 분할비 / 무게중심과 넓이 / 평행사변형 무게중심 응용",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 7.4)을 참고해 새로 씀. 무게중심 좌표는 세 꼭짓점의 평균으로 정확히 놓고, 길이는 '한 칸' k 의 배수로 만든다. 직각삼각형(t3)은 3-4-5 모양을 k·3/5 배로 그려 AC = 3k 가 정확히 맞는다.",
    "geometry": True,
    "templates": [cg_t1(), cg_t2(), cg_t3(), cg_t4()],
}


if __name__ == "__main__":
    for seed in (SR_SEED, TS_SEED, PR_SEED, CG_SEED):
        with_pitfalls(seed, strict=False)
        dump(seed)
