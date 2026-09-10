# itemfactory/tools/mkseed_m1_plane.py — 평면도형 시드 생성기: 다각형의 대각선 · 각의 크기(평각·비·맞꼭지각) (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m1_plane.py
#     → seeds/m1-2-polygon-diagonal.json (4틀) · seeds/m1-2-angle-basic.json (3틀)
#
# 각은 scene 으로 좌표를 직접 계산해 실제 크기대로 그린다(등축). 다각형 이름(십이각형)은 표로 굽고 recheck 가 이름을 수로 되읽는다.
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_DIAG = "699a4402-27bc-4405-b111-f02566e9ec97"     # 다각형 대각선·삼각형 개수
SCHEMA_ANGLE = "0b0d7580-0937-4872-97af-14bce2c3d4e8"    # 각의 크기 비 문제

GEO = {"process": "절차수행", "context": "기하맥락", "points": 4, "time_limit": 70, "traps": ["구하는대상혼동"]}
KNUM = {5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구", 10: "십", 11: "십일", 12: "십이", 13: "십삼", 14: "십사", 15: "십오", 16: "십육", 17: "십칠", 18: "십팔", 19: "십구", 20: "이십"}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. 다각형의 대각선
DIAG = dict(prereq=["다각형의 뜻", "곱셈·나눗셈"], ops=["사칙"], tags=["도형", "다각형", "대각선"])
NAME_ROWS = {str(n): {"NAME": KNUM[n] + "각형"} for n in range(5, 21)}


def diag_t1():
    return tpl("m1-2-polygon-diagonal", 1, DIAG,
        title="n각형의 대각선의 개수 (총 개수 / 한 꼭짓점에서 그을 수 있는 개수 / 삼각형의 개수)",
        skill="한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개, 총 개수는 n(n − 3)/2, 삼각형은 (n − 2)개",
        variant_axis={"구하는 것": "총 개수 / 한 꼭짓점 / 삼각형 개수", "n": "5~12"},
        discriminates="자기 자신과 이웃한 두 꼭짓점을 빼서 (n − 3)을 세우고, 총 개수에서는 2로 나누는 근거(두 번 셈)를 쓰는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "w", "values": {"in": ["all", "one", "tri"]}}, {"name": "n", "values": {"int": [5, 12]}}],
        table=[{"key": "w", "rows": {
            "all": {"Q": "대각선의 총 개수", "isA": 1, "isO": 0, "isT": 0, "DIAG": "fan"},
            "one": {"Q": "한 꼭짓점에서 그을 수 있는 대각선의 개수", "isA": 0, "isO": 1, "isT": 0, "DIAG": "fan"},
            "tri": {"Q": "한 꼭짓점에서 대각선을 모두 그었을 때 생기는 삼각형의 개수", "isA": 0, "isO": 0, "isT": 1, "DIAG": "fan"},
        }}, {"key": "n", "rows": NAME_ROWS}],
        derive={"k": "n - 3", "D": "n*(n - 3)/2", "T": "n - 2", "ans_v": "n*(n - 3)/2*isA + (n - 3)*isO + (n - 2)*isT"},
        constraints=["ans_v != n"],
        cost_values=["n", "k", "D", "ans_v"],
        verify=["2*D == n*k", "(isA == 1 and ans == D) or (isO == 1 and ans == k) or (isT == 1 and ans == T)"],
        question="{NAME}의 {Q}{eul(Q)} 구하시오.",
        figure=[{"fn": "polygon", "args": {"n": "{n}", "diagonals": "fan"}}],
        answer="{ans_v}", answer_alt=["{ans_v}개"],
        sol1="{NAME}은 꼭짓점이 {n}개다. 한 꼭짓점에서 대각선을 그으면 자기 자신과 양옆의 이웃한 두 꼭짓점에는 그을 수 없으므로 {n} − 3 = {k}(개)가 그어지고, 이때 다각형은 삼각형 {n} − 2 = {T}(개)로 나뉜다. 꼭짓점 {n}개에서 각각 {k}개씩 그으면 대각선 하나가 양 끝에서 두 번씩 세어지므로 총 개수는 {n} × {k} ÷ 2다.",
        sol1_fig=[{"fn": "polygon", "args": {"n": "{n}", "diagonals": "fan"}}],
        sol1_anim=[[hl("pt:A", "lbl:A", keep=True)], [hl("seg:A-C", "seg:A-D", "seg:A-E", "seg:A-F", "seg:A-G", "seg:A-H", "seg:A-I", "seg:A-J", "seg:A-K", keep=True)]],
        sol2=[
            "한 꼭짓점에서 그을 수 있는 대각선의 개수: {n} − 3 = {k}(개)",
            "이때 생기는 삼각형의 개수: {n} − 2 = {T}(개)",
            "대각선의 총 개수: {n} × {k} ÷ 2 = {n*k} ÷ 2 = {D}(개)",
            "따라서 {Q}{eun(Q)} {ans_v}개이다.",
        ],
        sol2_fig=steps([
            {"text": "한 꼭짓점: {n} − 3 = {k}", "hint": "자기 자신·이웃 2개 제외"},
            {"text": "삼각형: {n} − 2 = {T}", "hint": "대각선 {k}개가 {k}+1개로 나눈다"},
            {"text": "총 개수: {n} × {k} ÷ 2 = {D}", "hint": "두 번 세었으므로 ÷ 2", "marks": [{"on": "{D}", "note": "{n*k}÷2"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol_check="총 개수를 2로 나누지 않으면 {n*k}개, 한 꼭짓점에서 {n} − 2 = {T}개를 긋는다고 잘못 세면 값이 어긋난다. 답은 {ans_v}개다.",
        model_answer="{NAME}의 한 꼭짓점에서 그을 수 있는 대각선은 자기 자신과 이웃한 두 꼭짓점을 제외한 {n} − 3 = {k}(개)이고, 이때 삼각형 {n} − 2 = {T}(개)가 생긴다. 대각선의 총 개수는 각 꼭짓점에서 {k}개씩 그은 것을 두 번 센 것이므로 {n} × {k} ÷ 2 = {D}(개)이다. 따라서 {Q}{eun(Q)} {ans_v}개다.",
        rubric=[
            {"element": "한 꼭짓점의 대각선", "points": 3, "criterion": "자기 자신과 이웃한 두 꼭짓점을 뺀 {n} − 3 = {k}(개)임을 근거와 함께 썼다.", "partial": "{k}개라고만 쓰고 근거가 없으면 1점."},
            {"element": "총 개수·삼각형", "points": 2, "criterion": "총 개수 {n} × {k} ÷ 2 = {D}(두 번 셈이므로 ÷ 2) 또는 삼각형 {n} − 2 = {T}개를 근거와 함께 구했다.", "partial": "÷ 2의 근거 없이 결과만 썼으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v}개를 답했다.", "partial": "다른 개수를 답했으면 인정하지 않는다."},
        ],
    )


def diag_t2():
    return tpl("m1-2-polygon-diagonal", 2, DIAG,
        title="대각선의 총 개수로 다각형 구하기",
        skill="n(n − 3)/2 = D 를 만족하는 n을 찾기 — 곱이 2D인 차가 3인 두 자연수",
        variant_axis={"구하는 것": "변의 개수", "주어진 조건": "대각선의 총 개수"},
        discriminates="n(n − 3) = 2D로 정리하고 차가 3인 두 수의 곱으로 n을 찾는가",
        qtype="short", difficulty=3, pool_target=300, process="추론",
        params=[{"name": "n", "values": {"int": [5, 20]}}],
        table={"key": "n", "rows": NAME_ROWS},
        derive={"k": "n - 3", "D": "n*(n - 3)/2", "D2": "n*(n - 3)"},
        constraints=["D != n"],
        cost_values=["n", "k", "D", "D2"],
        relation="X*(X - 3)/2 - D", unknown="X", answer_var="n", multi_ok=True,
        verify=["ans*(ans - 3) == 2*D", "ans >= 3"],
        question="대각선의 총 개수가 {D}개인 다각형의 변의 개수를 구하시오.",
        answer="{n}", answer_alt=["{n}개", "{NAME}"],
        sol1="n각형의 대각선의 총 개수는 n(n − 3)/2이다. 이것이 {D}이므로 n(n − 3) = {D2} — 차가 3인 두 자연수의 곱이 {D2}인 것을 찾는다. {D2} = {n} × {k}이므로 n = {n}.",
        sol1_fig=steps(["n(n − 3)/2 = {D}", "n(n − 3) = {D2}", "{D2} = {n} × {k}  (차가 3인 두 수)"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "구하는 다각형을 n각형이라 하면 대각선의 총 개수는 n(n − 3)/2 (개)이다.",
            "n(n − 3)/2 = {D}에서 n(n − 3) = {D2}",
            "n과 n − 3은 차가 3인 두 자연수이고 곱이 {D2}이므로 {n} × {k} = {D2}에서 n = {n}",
            "따라서 이 다각형은 {NAME}이고 변의 개수는 {n}개이다.",
        ],
        sol2_fig=steps([
            {"text": "n(n − 3) = {D2}", "hint": "양변 × 2"},
            {"text": "{n} × {k} = {D2}", "hint": "차가 3인 두 수의 곱", "marks": [{"on": "{n}", "note": "n"}]},
            {"text": "n = {n} → {NAME}"},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="{NAME}의 대각선의 총 개수는 {n} × ({n} − 3) ÷ 2 = {D}(개)로 조건과 같다. 답은 {n}개다.",
        model_answer="구하는 다각형을 n각형이라 하면 대각선의 총 개수는 n(n − 3)/2 (개)이므로 n(n − 3)/2 = {D}, 곧 n(n − 3) = {D2}이다. 차가 3인 두 자연수의 곱이 {D2}인 것은 {n} × {k}이므로 n = {n}이다. 따라서 변의 개수는 {n}개({NAME})다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "n각형으로 놓고 n(n − 3)/2 = {D}{eul(D)} 세웠다.", "partial": "공식은 썼으나 등식으로 놓지 못했으면 1점."},
            {"element": "n 구하기", "points": 2, "criterion": "n(n − 3) = {D2}에서 차가 3인 두 수의 곱 {n} × {k}{eul(k)} 찾아 n = {n}{eul(n)} 구했다.", "partial": "n(n − 3) = {D2}까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "변의 개수 {n}개(또는 {NAME})를 답하고 확인했다.", "partial": "확인 없이 답만 옳으면 1점."},
        ],
    )


def diag_t3():
    return tpl("m1-2-polygon-diagonal", 3, DIAG,
        title="한 꼭짓점에서 그을 수 있는 대각선의 개수로 다각형·총 개수 구하기",
        skill="(n − 3) = k 에서 n을 구하고, 총 개수 n(n − 3)/2 로 잇기",
        variant_axis={"구하는 것": "변의 개수 / 대각선의 총 개수", "주어진 조건": "한 꼭짓점에서 그을 수 있는 대각선의 개수"},
        discriminates="n − 3 = k 로 n을 구한 뒤 묻는 것(변의 개수 / 총 개수)으로 옮기는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "w", "values": {"in": ["n", "all"]}}, {"name": "n", "values": {"int": [5, 20]}}],
        table=[{"key": "w", "rows": {"n": {"Q": "변의 개수", "isA": 0}, "all": {"Q": "대각선의 총 개수", "isA": 1}}}, {"key": "n", "rows": NAME_ROWS}],
        derive={"k": "n - 3", "D": "n*(n - 3)/2", "ans_v": "n*(1 - isA) + n*(n - 3)/2*isA"},
        constraints=["ans_v != k"],
        cost_values=["n", "k", "D", "ans_v"],
        verify=["k == n - 3", "(isA == 0 and ans == n) or (isA == 1 and ans == D)"],
        question="한 꼭짓점에서 그을 수 있는 대각선의 개수가 {k}개인 다각형의 {Q}{eul(Q)} 구하시오.",
        answer="{ans_v}", answer_alt=["{ans_v}개"],
        sol1="n각형의 한 꼭짓점에서 그을 수 있는 대각선은 자기 자신과 이웃한 두 꼭짓점을 뺀 (n − 3)개다. 이것이 {k}개이므로 n = {k} + 3 = {n}, 곧 {NAME}이다. 총 개수가 필요하면 n(n − 3)/2에 넣는다.",
        sol1_fig=steps(["n − 3 = {k}", "n = {n}  ({NAME})", "총 개수 = {n} × {k} ÷ 2 = {D}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "구하는 다각형을 n각형이라 하면 한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개이므로 n − 3 = {k}",
            "따라서 n = {n}이고 이 다각형은 {NAME}이다.",
            "대각선의 총 개수는 {n} × ({n} − 3) ÷ 2 = {n*k} ÷ 2 = {D}(개)",
            "따라서 {Q}{eun(Q)} {ans_v}개이다.",
        ],
        sol2_fig=steps([
            {"text": "n − 3 = {k}", "hint": "한 꼭짓점: 자기 자신·이웃 2개 제외"},
            {"text": "n = {n}", "marks": [{"on": "{n}", "note": "{k}+3"}]},
            {"text": "총 개수 = {n} × {k} ÷ 2 = {D}", "hint": "두 번 세었으므로 ÷ 2"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("hint:2")], []],
        sol_check="{NAME}의 한 꼭짓점에서 그을 수 있는 대각선은 {n} − 3 = {k}(개)로 조건과 같다. 답은 {ans_v}개다.",
        model_answer="구하는 다각형을 n각형이라 하면 한 꼭짓점에서 그을 수 있는 대각선은 (n − 3)개이므로 n − 3 = {k}에서 n = {n}, 곧 {NAME}이다. 대각선의 총 개수는 {n} × ({n} − 3) ÷ 2 = {D}(개)이다. 따라서 {Q}{eun(Q)} {ans_v}개다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "n각형으로 놓고 n − 3 = {k}{eul(k)} 근거와 함께 세웠다.", "partial": "n − 3이라는 식의 근거(자기 자신·이웃 제외)를 쓰지 않았으면 1점."},
            {"element": "n 구하기", "points": 2, "criterion": "n = {n}({NAME})을 구했다.", "partial": "n − 2 = {k} 처럼 잘못 세웠으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v}개를 답했다.", "partial": "총 개수에서 2로 나누지 않았으면 인정하지 않는다."},
        ],
    )


def diag_t4():
    return tpl("m1-2-polygon-diagonal", 4, DIAG,
        title="내각의 크기의 합으로 다각형을 정하고 대각선의 총 개수 구하기",
        skill="180°(n − 2) = S 에서 n을 구하고 대각선의 총 개수 n(n − 3)/2 로 잇기",
        variant_axis={"구하는 것": "대각선의 총 개수", "주어진 조건": "내각의 크기의 합"},
        discriminates="내각의 합 공식과 대각선 공식을 이어서 쓰는가",
        qtype="short", difficulty=3, pool_target=300, prereq=["다각형의 내각의 합", "대각선의 개수"],
        params=[{"name": "n", "values": {"int": [5, 20]}}],
        table={"key": "n", "rows": NAME_ROWS},
        derive={"S": "180*(n - 2)", "k": "n - 3", "D": "n*(n - 3)/2"},
        constraints=["D != n", "D != S"],
        cost_values=["S", "n", "k", "D"],
        relation="X - (S/180 + 2)*(S/180 + 2 - 3)/2", unknown="X", answer_var="D",
        verify=["180*(n - 2) == S", "2*ans == n*(n - 3)"],
        question="내각의 크기의 합이 [[deg({S})]]인 다각형의 대각선의 총 개수를 구하시오.",
        answer="{D}", answer_alt=["{D}개"],
        sol1="먼저 어떤 다각형인지 정한다. n각형의 내각의 크기의 합은 180° × (n − 2)이므로 180 × (n − 2) = {S}에서 n을 구하고, 그다음 대각선의 총 개수 n(n − 3)/2를 계산한다.",
        sol1_fig=steps(["180 × (n − 2) = {S}", "n − 2 = {n - 2},  n = {n}", "대각선: {n} × {k} ÷ 2 = {D}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "구하는 다각형을 n각형이라 하면 내각의 크기의 합은 180° × (n − 2)이므로 180 × (n − 2) = {S}",
            "n − 2 = {S} ÷ 180 = {n - 2}이므로 n = {n}, 곧 {NAME}이다.",
            "{NAME}의 대각선의 총 개수는 {n} × ({n} − 3) ÷ 2 = {n*k} ÷ 2 = {D}(개)",
        ],
        sol2_fig=steps([
            {"text": "180(n − 2) = {S}", "hint": "내각의 합"},
            {"text": "n − 2 = {n - 2},  n = {n}", "marks": [{"on": "{n - 2}", "note": "{S}÷180"}]},
            {"text": "{n} × {k} ÷ 2 = {D}", "hint": "대각선의 총 개수"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("hint:2")]],
        sol_check="{NAME}의 내각의 합은 180° × {n - 2} = {S}°로 조건과 같고, 대각선은 {D}개다. n을 구한 뒤 2를 더하는 것을 잊으면 다른 다각형이 된다. 답은 {D}개다.",
        model_answer="구하는 다각형을 n각형이라 하면 내각의 크기의 합이 180° × (n − 2)이므로 180 × (n − 2) = {S}에서 n − 2 = {n - 2}, n = {n}이다. 따라서 {NAME}이고, 대각선의 총 개수는 {n} × ({n} − 3) ÷ 2 = {D}(개)다.",
        rubric=[
            {"element": "다각형 정하기", "points": 3, "criterion": "180 × (n − 2) = {S}{eul(S)} 세워 n = {n}({NAME})을 구했다.", "partial": "식은 세웠으나 n − 2 = {n - 2}에서 2를 더하지 않았으면 1점."},
            {"element": "대각선 공식", "points": 2, "criterion": "대각선의 총 개수가 n(n − 3)/2임을 밝혔다.", "partial": "n(n − 3)에서 2로 나누지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{n} × {k} ÷ 2 = {D}개를 답했다.", "partial": "계산 실수면 1점."},
        ],
    )


DIAG_SEED = {
    "seed_id": "m1-2-polygon-diagonal", "category": "도형",
    "title": "다각형의 대각선 — 개수·역산·내각의 합과 연결",
    "unit_id": "m1-2", "concept_ids": ["m1-2-07"],
    "schema_id": SCHEMA_DIAG, "schema_name": "다각형 대각선·삼각형 개수 / 대각선 개수로 다각형 구하기",
    "source_item_ids": [],
    "note": "관계식 n − 3, n(n − 3)/2, 180(n − 2) 만 차용. n은 5~20(그림이 있는 틀은 5~12 — polygon.n 상한). 다각형 이름은 표로.",
    "geometry": True,
    "templates": [diag_t1(), diag_t2(), diag_t3(), diag_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 각의 크기 — 평각·비·맞꼭지각 (scene 좌표 직접 계산)
ANG = dict(prereq=["평각 180°", "맞꼭지각", "일차방정식"], ops=["각도", "방정식"], tags=["각", "평각", "맞꼭지각"])
RATIO_PAIRS = [(a, b) for a, b in [(1, 2), (2, 1), (1, 3), (3, 1), (1, 4), (4, 1), (2, 3), (3, 2), (1, 5), (5, 1), (2, 7), (7, 2), (4, 5), (5, 4), (1, 8), (8, 1),
                                   (3, 7), (7, 3), (5, 7), (7, 5), (1, 9), (9, 1), (4, 11), (11, 4), (7, 11), (11, 7), (1, 11), (11, 1), (13, 17), (17, 13), (7, 13), (13, 7), (2, 13), (13, 2), (7, 23), (23, 7)]]


def angle_t1():
    # 평각 위 ∠AOB : ∠BOC = a : b
    return tpl("m1-2-angle-basic", 1, ANG,
        title="평각을 주어진 비로 나눈 각의 크기",
        skill="∠AOB + ∠BOC = 180°(평각)임을 쓰고 비례배분하기",
        variant_axis={"구하는 것": "∠AOB / ∠BOC", "조건": "비"},
        discriminates="직선 위의 두 각의 합이 180°임을 밝히고 비로 나누는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "w", "values": {"in": ["AOB", "BOC"]}}, {"name": "ab", "values": {"in": [a * 100 + b for a, b in RATIO_PAIRS]}}],
        table={"key": "w", "rows": {"AOB": {"Q": "AOB", "isB": 0}, "BOC": {"Q": "BOC", "isB": 1}}},
        derive={"a": "floor(ab/100)", "b": "ab % 100", "s": "floor(ab/100) + ab % 100", "u": "180/(floor(ab/100) + ab % 100)", "x": "180*floor(ab/100)/(floor(ab/100) + ab % 100)", "y": "180*(ab % 100)/(floor(ab/100) + ab % 100)",
                "ans_v": "180*floor(ab/100)/(floor(ab/100) + ab % 100)*(1 - isB) + 180*(ab % 100)/(floor(ab/100) + ab % 100)*isB",
                "bx": "-cos(pi*floor(ab/100)/(floor(ab/100) + ab % 100))", "by": "sin(pi*floor(ab/100)/(floor(ab/100) + ab % 100))",
                "lax": "-0.5*cos(pi*floor(ab/100)/(floor(ab/100) + ab % 100)/2)", "lay": "0.5*sin(pi*floor(ab/100)/(floor(ab/100) + ab % 100)/2)",
                "lbx": "0.5*cos(pi*(ab % 100)/(floor(ab/100) + ab % 100)/2)", "lby": "0.5*sin(pi*(ab % 100)/(floor(ab/100) + ab % 100)/2)"},
        constraints=["a != b", "ans_v != a", "ans_v != b", "u >= 6", "u == floor(u)"],
        cost_values=["a", "b", "s", "u", "ans_v"],
        answer_var="ans_v",
        verify=["x + y == 180", "x*b == y*a", "(isB == 0 and ans == x) or (isB == 1 and ans == y)"],
        question="다음 그림에서 점 O는 직선 AC 위의 점이고 [[angle(AOB)]] : [[angle(BOC)]] = {a} : {b}일 때, [[angle({Q})]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "O": [0, 0], "C": [1, 0], "B": ["{bx}", "{by}"]},
                                          "segs": [["A", "C"], ["O", "B"]],
                                          "marks": {"arc": [{"at": "O", "from": "B", "to": "A", "k": "arc:AOB"}, {"at": "O", "from": "C", "to": "B", "k": "arc:BOC"}]}}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="점 O가 직선 AC 위에 있으므로 ∠AOC는 평각, 곧 ∠AOB + ∠BOC = 180°다. 두 각의 비가 {a} : {b}이므로 180°를 {a} + {b} = {s}등분한 한 칸이 180° ÷ {s} = {u}°이고, ∠AOB는 그 {a}칸, ∠BOC는 {b}칸이다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "O": [0, 0], "C": [1, 0], "B": ["{bx}", "{by}"]},
                                           "segs": [["A", "C"], ["O", "B"]],
                                           "marks": {"arc": [{"at": "O", "from": "B", "to": "A", "k": "arc:AOB"}, {"at": "O", "from": "C", "to": "B", "k": "arc:BOC"}]},
                                           "labels": [{"at": ["{lax}", "{lay}"], "text": "{x}°", "k": "lbl:AOB", "accent": True}, {"at": ["{lbx}", "{lby}"], "text": "{y}°", "k": "lbl:BOC", "accent": True}]}}],
        sol1_anim=[[hl("seg:A-C", "lbl:A", "lbl:C")], [hl("arc:AOB", "lbl:AOB", keep=True)], [hl("arc:BOC", "lbl:BOC", keep=True)]],
        sol2=[
            "점 O가 직선 AC 위에 있으므로 ∠AOB + ∠BOC = 180° (평각)",
            "∠AOB : ∠BOC = {a} : {b}이므로 ∠AOB = 180° × {a}/{s}, ∠BOC = 180° × {b}/{s}",
            "180° ÷ {s} = {u}°이므로 ∠AOB = {u}° × {a} = {x}°, ∠BOC = {u}° × {b} = {y}°",
            "따라서 ∠{Q} = {ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "∠AOB + ∠BOC = 180°", "hint": "평각"},
            {"text": "한 칸 = 180° ÷ {s} = {u}°", "hint": "{a} + {b} = {s}등분", "marks": [{"on": "{u}°", "note": "180÷{s}"}]},
            {"text": "∠AOB = {u}° × {a} = {x}°,  ∠BOC = {u}° × {b} = {y}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)], []],
        sol_check="{x}° + {y}° = 180°로 평각이 되고 {x} : {y} = {a} : {b}로 비도 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 O가 직선 AC 위에 있으므로 ∠AOB + ∠BOC = 180°이다. ∠AOB : ∠BOC = {a} : {b}이므로 ∠AOB = 180° × {a}/{s} = {x}°, ∠BOC = 180° × {b}/{s} = {y}°이다. 따라서 ∠{Q} = {ans_v}°다.",
        rubric=[
            {"element": "평각 조건", "points": 3, "criterion": "점 O가 직선 위에 있으므로 ∠AOB + ∠BOC = 180°임을 밝혔다.", "partial": "180°를 썼으나 평각(직선)이라는 근거가 없으면 1점."},
            {"element": "비례배분", "points": 2, "criterion": "180°를 {a} + {b} = {s}등분하여 ∠{Q} = 180° × {a}/{s}(또는 {b}/{s})로 나타냈다.", "partial": "등분 수를 잘못 잡았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{Q} = {ans_v}°를 구하고 두 각의 합이 180°가 됨을 확인했다.", "partial": "다른 쪽 각을 답했으면 인정하지 않는다."},
        ],
    )


def angle_t2():
    # 평각 위 ∠AOB = x + p, ∠BOC = 2x + q  → x, 구하는 것 ∠AOB
    return tpl("m1-2-angle-basic", 2, ANG,
        title="평각 위의 각을 문자 식으로 나타내고 각의 크기 구하기",
        skill="(x + p) + (2x + q) = 180 을 세워 x를 구한 뒤 묻는 각으로 옮기기",
        variant_axis={"구하는 것": "∠AOB", "조건": "문자 식 각"},
        discriminates="평각 조건으로 방정식을 세우고, x가 아니라 묻는 각의 크기를 답하는가",
        qtype="short", difficulty=3, pool_target=300, process="추론",
        params=[{"name": "x5", "values": {"int": [2, 10]}}, {"name": "p", "values": {"in": [5, 10, 15, 20, 25, 30, 35, 40]}}, {"name": "m", "values": {"in": [2, 3]}}],
        derive={"x": "5*x5", "A": "5*x5 + p", "q": "180 - (5*x5 + p) - m*5*x5", "Bv": "180 - (5*x5 + p)",
                "bx": "-cos(pi*(5*x5 + p)/180)", "by": "sin(pi*(5*x5 + p)/180)",
                "lax": "-0.55*cos(pi*(5*x5 + p)/360)", "lay": "0.55*sin(pi*(5*x5 + p)/360)",
                "lbx": "0.55*cos(pi*(180 - (5*x5 + p))/360)", "lby": "0.55*sin(pi*(180 - (5*x5 + p))/360)"},
        constraints=["q >= 5", "q <= 100", "A != x", "A != p", "A != q", "A != m", "x != p", "x != q", "p != q"],
        cost_values=["x", "p", "q", "m", "A"],
        relation="(X + p) + (m*X + q) - 180", unknown="X", answer_var="x",
        verify=["A + m*x + q == 180", "ans == x"],
        question="다음 그림에서 점 O는 직선 AC 위의 점이고 [[angle(AOB)]] = (x + {p})°, [[angle(BOC)]] = ({m}x + {q})°일 때, [[angle(AOB)]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "O": [0, 0], "C": [1, 0], "B": ["{bx}", "{by}"]},
                                          "segs": [["A", "C"], ["O", "B"]],
                                          "marks": {"arc": [{"at": "O", "from": "B", "to": "A", "k": "arc:AOB"}, {"at": "O", "from": "C", "to": "B", "k": "arc:BOC"}]},
                                          "labels": [{"at": ["{lax}", "{lay}"], "text": "(x + {p})°", "k": "lbl:AOB"}, {"at": ["{lbx}", "{lby}"], "text": "({m}x + {q})°", "k": "lbl:BOC"}]}}],
        answer="[[deg({A})]]", answer_alt=["{A}°", "{A}"],
        sol1="점 O가 직선 AC 위에 있으므로 ∠AOB + ∠BOC = 180°(평각)다. 두 각이 x의 식으로 주어졌으니 (x + {p}) + ({m}x + {q}) = 180이라는 방정식이 나온다. x를 구한 뒤 ∠AOB = x + {p}에 넣어야 한다 — x 자체가 답이 아니다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "O": [0, 0], "C": [1, 0], "B": ["{bx}", "{by}"]},
                                          "segs": [["A", "C"], ["O", "B"]],
                                          "marks": {"arc": [{"at": "O", "from": "B", "to": "A", "k": "arc:AOB"}, {"at": "O", "from": "C", "to": "B", "k": "arc:BOC"}]},
                                          "labels": [{"at": ["{lax}", "{lay}"], "text": "(x + {p})°", "k": "lbl:AOB", "accent": True}, {"at": ["{lbx}", "{lby}"], "text": "({m}x + {q})°", "k": "lbl:BOC", "accent": True}]}}],
        sol1_anim=[[hl("seg:A-C", "lbl:A", "lbl:C")], [hl("arc:AOB", "lbl:AOB", "arc:BOC", "lbl:BOC", keep=True)]],
        sol2=[
            "점 O가 직선 AC 위에 있으므로 ∠AOB + ∠BOC = 180°",
            "(x + {p}) + ({m}x + {q}) = 180, 동류항을 정리하면 {m+1}x + {p + q} = 180",
            "{p + q}{eul(p + q)} 이항하면 {m+1}x = {180 - p - q}, 따라서 x = {x}",
            "∠AOB = x + {p} = {x} + {p} = {A}°",
        ],
        sol2_fig=steps([
            {"text": "(x + {p}) + ({m}x + {q}) = 180", "hint": "평각"},
            {"text": "{m+1}x + {p + q} = 180", "hint": "동류항 정리"},
            {"text": "{m+1}x = {180 - p - q},  x = {x}", "marks": [{"on": "{x}", "note": "{180 - p - q}÷{m+1}"}]},
            {"text": "∠AOB = {x} + {p} = {A}°", "hint": "묻는 것은 ∠AOB (x가 아님)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3), hl("hint:3")]],
        sol_check="x = {x}이면 ∠AOB = {A}°, ∠BOC = {m} × {x} + {q} = {Bv}°이고 {A}° + {Bv}° = 180°로 평각이 맞다. x = {x}{eul(x)} 그대로 답하면 안 된다. 답은 [[deg({A})]]다.",
        model_answer="점 O가 직선 AC 위에 있으므로 ∠AOB + ∠BOC = 180°이다. (x + {p}) + ({m}x + {q}) = 180에서 {m+1}x = {180 - p - q}, x = {x}이다. 따라서 ∠AOB = {x} + {p} = {A}°다.",
        rubric=[
            {"element": "평각 조건", "points": 3, "criterion": "∠AOB + ∠BOC = 180°임을 밝히고 (x + {p}) + ({m}x + {q}) = 180을 세웠다.", "partial": "180°의 근거(평각) 없이 식만 썼으면 2점."},
            {"element": "방정식 풀이", "points": 2, "criterion": "동류항을 정리하고 이항하여 x = {x}{eul(x)} 구했다.", "partial": "동류항 정리까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠AOB = {x} + {p} = {A}°를 답했다.", "partial": "x = {x}{eul(x)} 그대로 답했으면 인정하지 않는다."},
        ],
    )


def angle_t3():
    # 맞꼭지각: ∠AOC = ax + b, ∠BOD = cx + d (맞꼭지각) → x → ∠AOC
    return tpl("m1-2-angle-basic", 3, ANG,
        title="맞꼭지각의 크기가 같음을 이용하여 각의 크기 구하기",
        skill="두 직선이 만날 때 맞꼭지각의 크기는 같다 — 식을 같다고 놓고 x를 구하기",
        variant_axis={"구하는 것": "∠AOC", "조건": "맞꼭지각 두 식"},
        discriminates="맞꼭지각(마주 보는 각)을 바르게 짝짓고 등식을 세우는가",
        qtype="short", difficulty=3, pool_target=300, process="추론", tags=["각", "맞꼭지각"],
        params=[{"name": "x5", "values": {"int": [1, 8]}}, {"name": "a", "values": {"in": [2, 3, 4]}}, {"name": "k", "values": {"in": [1, 2]}}, {"name": "b", "values": {"in": [5, 10, 15, 20, 25, 30, 35, 40]}}],
        derive={"x": "5*x5", "c": "a - k", "d": "b + k*5*x5", "T": "a*5*x5 + b", "ax": "cos(pi*(a*5*x5 + b)/180)", "ay": "sin(pi*(a*5*x5 + b)/180)",
                # O 이름은 각 표시가 없는 ∠BOC 쐐기(오른쪽 위)의 이등분선 위 0.2에 — 고정 좌표(0.1, −0.16)는 CD가 가파르면 선에 얹혔다
                "ox": "0.2*sin(pi*(a*5*x5 + b)/360)", "oy": "0.2*cos(pi*(a*5*x5 + b)/360)"},
        constraints=["T >= 30", "T <= 150", "T != x", "T != a", "T != b", "T != c", "T != d", "x != b", "x != d", "b != d"],
        cost_values=["x", "a", "b", "c", "d", "T"],
        answer_var="T",
        verify=["a*x + b == c*x + d", "ans == a*x + b", "c >= 1"],
        question="다음 그림에서 두 직선 AB, CD가 점 O에서 만나고 [[angle(AOC)]] = ({a}x + {b})°, [[angle(BOD)]] = ({co(c)}x + {d})°일 때, [[angle(AOC)]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "B": [1, 0], "O": [0, 0], "C": ["{-ax}", "{ay}"], "D": ["{ax}", "{-ay}"]},
                                          "segs": [["A", "B"], ["C", "D"]],
                                          "marks": {"arc": [{"at": "O", "from": "C", "to": "A", "label": "({a}x + {b})°", "k": "arc:AOC"}, {"at": "O", "from": "D", "to": "B", "label": "({co(c)}x + {d})°", "k": "arc:BOD"}]},
                                          "nodot": ["O"],
                                          "labels": [{"at": ["{ox}", "{oy}"], "text": "O"}]}}],
        answer="[[deg({T})]]", answer_alt=["{T}°", "{T}"],
        sol1="두 직선이 한 점에서 만날 때 마주 보는 두 각(맞꼭지각)의 크기는 서로 같다 — 각각이 같은 각과 합쳐서 평각 180°를 이루기 때문이다. ∠AOC와 ∠BOD는 맞꼭지각이므로 {a}x + {b} = {co(c)}x + {d}라는 등식이 나온다. 이웃한 각과 짝짓지 않도록 그림에서 마주 보는지 확인한다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [-1, 0], "B": [1, 0], "O": [0, 0], "C": ["{-ax}", "{ay}"], "D": ["{ax}", "{-ay}"]},
                                          "segs": [["A", "B"], ["C", "D"]],
                                          "marks": {"arc": [{"at": "O", "from": "C", "to": "A", "label": "({a}x + {b})°", "k": "arc:AOC"}, {"at": "O", "from": "D", "to": "B", "label": "({co(c)}x + {d})°", "k": "arc:BOD"}]},
                                          "nodot": ["O"],
                                          "labels": [{"at": ["{ox}", "{oy}"], "text": "O"}]}}],
        sol1_anim=[[hl("seg:A-B", "seg:C-D")], [hl("arc:AOC", "arc:AOC:lbl", keep=True)], [hl("arc:BOD", "arc:BOD:lbl", keep=True)]],
        sol2=[
            "∠AOC와 ∠BOD는 맞꼭지각이므로 크기가 같다: {a}x + {b} = {co(c)}x + {d}",
            "x를 한쪽으로 모으면 {a}x − {co(c)}x = {d} − {b}이므로 x = {x}",
            "∠AOC = {a} × {x} + {b} = {T}°",
        ],
        sol2_fig=steps([
            {"text": "{a}x + {b} = {co(c)}x + {d}", "hint": "맞꼭지각은 크기가 같다"},
            {"text": "{a}x − {co(c)}x = {d} − {b}", "hint": "이항 — 부호가 바뀐다"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{dv(d - b, k)}"}]},
            {"text": "∠AOC = {a} × {x} + {b} = {T}°", "hint": "묻는 것은 각의 크기"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1"), reveal(2), hl("mark:2-0")], [reveal(3), hl("hint:3")]],
        sol_check="x = {x}이면 ∠BOD = {c*x} + {d} = {T}°로 ∠AOC와 같다. 이웃한 각 ∠AOD는 180° − {T}° = {180 - T}°다. 답은 [[deg({T})]]다.",
        model_answer="두 직선이 한 점에서 만나므로 ∠AOC와 ∠BOD는 맞꼭지각이고 크기가 같다. {a}x + {b} = {co(c)}x + {d}에서 x = {x}이므로 ∠AOC = {a} × {x} + {b} = {T}°다.",
        rubric=[
            {"element": "맞꼭지각", "points": 3, "criterion": "∠AOC와 ∠BOD가 맞꼭지각이므로 크기가 같음을 밝히고 {a}x + {b} = {co(c)}x + {d}{eul(d)} 세웠다.", "partial": "등식은 세웠으나 맞꼭지각이라는 근거가 없으면 2점."},
            {"element": "방정식 풀이", "points": 2, "criterion": "이항하여 x = {x}{eul(x)} 구했다.", "partial": "이항의 부호 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠AOC = {T}°를 답했다.", "partial": "x = {x}{eul(x)} 그대로 답했으면 인정하지 않는다."},
        ],
    )


ANGLE_SEED = {
    "seed_id": "m1-2-angle-basic", "category": "도형",
    "title": "각의 크기 — 평각의 비례배분·문자 식·맞꼭지각",
    "unit_id": "m1-2", "concept_ids": ["m1-2-02"],
    "schema_id": SCHEMA_ANGLE, "schema_name": "각의 크기 비 문제 / 평각을 이용하여 각의 크기 구하기",
    "source_item_ids": [],
    "note": "관계식(평각 180°, 맞꼭지각 상등)만 차용. 각은 scene 좌표를 직접 계산해 실제 크기대로 그린다. 맞꼭지각 틀은 x, a, k, b 에서 c = a − k, d = b + kx 로 생성해 등식이 항상 성립(정수해).",
    "geometry": True,
    "templates": [angle_t1(), angle_t2(), angle_t3()],
}


if __name__ == "__main__":
    for seed in (DIAG_SEED, ANGLE_SEED):
        with_pitfalls(seed)
        dump(seed)
