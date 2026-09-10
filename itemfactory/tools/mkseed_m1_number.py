# itemfactory/tools/mkseed_m1_number.py — 수와 연산 활용 시드 생성기 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m1_number.py
#     → seeds/m1-1-gcd-lcm-apply.json (최대공약수·최소공배수의 활용 4틀) · seeds/m1-1-abs-pair.json (절댓값 3틀)
#
# 소인수분해 문자열·수직선 점 목록처럼 식으로 못 만드는 값은 표(table)로 굽는다 (SEEDSPEC "표 파생").
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, dump, hl, numline, reveal, steps, with_pitfalls  # noqa: E402

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def factor_str(n: int) -> str:
    """12 → '2² × 3'  (소인수분해 표기)"""
    out, m, p = [], n, 2
    while p * p <= m:
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        if e:
            out.append(f"{p}{str(e).translate(SUP) if e > 1 else ''}")
        p += 1
    if m > 1:
        out.append(str(m))
    return " × ".join(out) if out else str(n)


def lcm_factor_str(a: int, b: int) -> str:
    """최소공배수를 소인수의 곱으로 — 각 소인수의 큰 지수를 택한다."""
    def fac(n):
        d, m, p = {}, n, 2
        while p * p <= m:
            while m % p == 0:
                m //= p
                d[p] = d.get(p, 0) + 1
            p += 1
        if m > 1:
            d[m] = d.get(m, 0) + 1
        return d
    fa, fb = fac(a), fac(b)
    ps = sorted(set(fa) | set(fb))
    return " × ".join(f"{p}{str(max(fa.get(p, 0), fb.get(p, 0))).translate(SUP) if max(fa.get(p, 0), fb.get(p, 0)) > 1 else ''}" for p in ps)


def gcd_factor_str(a: int, b: int) -> str:
    def fac(n):
        d, m, p = {}, n, 2
        while p * p <= m:
            while m % p == 0:
                m //= p
                d[p] = d.get(p, 0) + 1
            p += 1
        if m > 1:
            d[m] = d.get(m, 0) + 1
        return d
    fa, fb = fac(a), fac(b)
    ps = sorted(set(fa) & set(fb))
    return " × ".join(f"{p}{str(min(fa[p], fb[p])).translate(SUP) if min(fa[p], fb[p]) > 1 else ''}" for p in ps) or "1"


SCHEMA_GL_REL = "0970a9a3-cb33-43a0-a969-eb86e1ffee9e"    # 두 수의 곱과 최대공약수·최소공배수 관계
SCHEMA_ABS = "3dc107d0-2647-4ab0-a3d4-966de449bc19"       # 절댓값이 같고 부호가 반대인 두 수

BASE = {**COMMON_APPLY, "prereq": ["소인수분해", "최대공약수·최소공배수"], "ops": ["인수분해", "사칙"], "traps": ["구하는대상혼동", "조건누락"]}


def tpl(seed_id, no, **kw):
    t = dict(BASE)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. 최대공약수·최소공배수의 활용
LCM_PAIRS = [(4, 6), (6, 8), (6, 9), (6, 10), (8, 10), (8, 12), (9, 12), (10, 12), (10, 15), (12, 15), (12, 16), (12, 18), (12, 20),
             (14, 21), (15, 18), (15, 20), (15, 25), (16, 24), (18, 24), (18, 27), (20, 24), (20, 30), (21, 28), (24, 36), (30, 45),
             (4, 10), (6, 14), (6, 15), (8, 14), (8, 18), (9, 15), (10, 14), (10, 18), (10, 25), (12, 30), (14, 35), (16, 20), (18, 30), (20, 50), (12, 21), (15, 24)]
GCD_PAIRS = [(36, 24), (48, 36), (60, 45), (72, 48), (90, 60), (84, 60), (96, 72), (120, 90), (100, 75), (80, 64), (54, 36), (70, 42),
             (63, 45), (56, 40), (108, 72), (150, 120), (140, 100), (66, 44), (78, 52), (132, 88)]


def lcm_row(a, b):
    L = a * b // math.gcd(a, b)
    return {"a": a, "b": b, "L": L, "fa": factor_str(a), "fb": factor_str(b), "fl": lcm_factor_str(a, b), "na": L // a, "nb": L // b,
            "tl": [{"x": k * a, "label": "A"} for k in range(1, L // a)] + [{"x": k * b, "label": "B"} for k in range(1, L // b)] + [{"x": L, "label": "동시"}]}


LCM_TABLE = {"key": "ab", "rows": {str(a * 100 + b): lcm_row(a, b) for a, b in LCM_PAIRS}}
LCM_PARAM = {"name": "ab", "values": {"in": [str(a * 100 + b) for a, b in LCM_PAIRS]}}

DEPART_CTX = {
    "1": {"S": "어느 지하철역에서 두 노선의 열차가", "A": "1호선 열차", "B": "2호선 열차", "V": "출발한다", "VM": "출발하는", "VG": "출발한다고", "PAIR": "두 열차가"},
    "2": {"S": "어느 버스 정류장에서 두 노선의 버스가", "A": "101번 버스", "B": "202번 버스", "V": "출발한다", "VM": "출발하는", "VG": "출발한다고", "PAIR": "두 버스가"},
    "3": {"S": "공항에서 셔틀버스와 공항 리무진이", "A": "셔틀버스", "B": "공항 리무진", "V": "출발한다", "VM": "출발하는", "VG": "출발한다고", "PAIR": "두 대가"},
    "4": {"S": "놀이공원에서 두 놀이 기구가", "A": "회전목마", "B": "대관람차", "V": "운행을 시작한다", "VM": "운행을 시작하는", "VG": "운행을 시작한다고", "PAIR": "두 놀이 기구가"},
}


def gl_t1():
    return tpl("m1-1-gcd-lcm-apply", 1,
        title="동시 출발 — 다음에 처음으로 다시 동시에 출발하는 때 (최소공배수)",
        skill="'처음으로 다시 동시에'는 두 간격의 최소공배수임을 알고 소인수분해로 구하기",
        variant_axis={"구하는 것": "몇 분 후", "상황": "동시 출발", "맥락": "지하철·버스·셔틀·놀이기구"},
        discriminates="두 간격의 공배수 중 가장 작은 것이 답임을 근거와 함께 쓰는가 (최대공약수와 혼동하지 않는가)",
        qtype="short", difficulty=2, pool_target=300, tags=["최소공배수", "동시 출발", "최대공약수와 최소공배수의 활용"],
        params=[{"name": "c", "values": {"in": list(DEPART_CTX)}}, LCM_PARAM],
        table=[{"key": "c", "rows": DEPART_CTX}, LCM_TABLE],
        derive={"g": "gcd(a, b)", "pr": "a*b"},
        constraints=["L != a", "L != b"],
        cost_values=["a", "b", "L", "g"],
        verify=["lcm(a, b) == L", "ans == L", "L % a == 0", "L % b == 0"],
        question="{S} {A}{eun(A)} {a}분 간격으로, {B}{eun(B)} {b}분 간격으로 {V}. 오전 9시에 {PAIR} 동시에 {VG} 할 때, 다음에 처음으로 다시 동시에 {VM} 것은 몇 분 후인지 구하시오.",
        answer="{L}", answer_alt=["{L}분 후", "{L}분"],
        sol1="{A}{eun(A)} {a}분, {2*a}분, {3*a}분, … 마다, {B}{eun(B)} {b}분, {2*b}분, {3*b}분, … 마다 {V}. 둘이 다시 동시에 {VM} 때는 {a}의 배수이면서 {b}의 배수인 때, 곧 {a}{wa(a)} {b}의 공배수이고, '처음으로'이므로 그중 가장 작은 최소공배수다. 수직선에 두 출발 시각을 찍어 보면 처음 겹치는 점이 답이다.",
        sol1_fig=numline(0, "{L}", "{tl}"),
        sol1_anim=[[hl("pt:A", "lbl:A")], [hl("pt:B", "lbl:B")], [hl("pt:동시", "lbl:동시", keep=True)]],
        sol2=[
            "다시 동시에 {VM} 때는 {a}{wa(a)} {b}의 공배수이고, 처음으로 그렇게 되는 때는 최소공배수이다.",
            "소인수분해하면 {a} = {fa}, {b} = {fb}",
            "최소공배수는 각 소인수의 지수가 큰 쪽을 택해 곱한 것이므로 {fl} = {L}",
            "따라서 {L}분 후에 처음으로 다시 동시에 {V}.",
        ],
        sol2_fig=steps([
            {"text": "{a} = {fa}", "hint": "소인수분해"},
            {"text": "{b} = {fb}"},
            {"text": "최소공배수 = {fl} = {L}", "hint": "소인수마다 지수가 큰 쪽", "marks": [{"on": "{L}", "note": "{a}×{na}={L}, {b}×{nb}={L}"}]},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0"), reveal(1)], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol3="{L}분은 {a} × {na} = {L}, {b} × {nb} = {L}{ro(L)} {a}의 배수이면서 {b}의 배수다. {L}보다 작은 공배수는 없으므로({a}{wa(a)} {b}의 공배수는 {L}, {2*L}, …) 처음으로 다시 동시에 {VM} 것은 {L}분 후가 맞다. 답은 {L}분 후다.",
        sol3_fig=steps(["{a} × {na} = {L}", "{b} × {nb} = {L}", "공배수: {L}, {2*L}, {3*L}, … → 처음은 {L}"]),
        sol3_anim=[[reveal(0), reveal(1)], [reveal(2)]],
        model_answer="{PAIR} 다시 동시에 {VM} 때는 {a}{wa(a)} {b}의 공배수이고, 처음으로 그렇게 되는 때는 최소공배수이다. {a} = {fa}, {b} = {fb}이므로 최소공배수는 {fl} = {L}이다. 따라서 처음으로 다시 동시에 {VM} 것은 {L}분 후다.",
        rubric=[
            {"element": "최소공배수 판단", "points": 3, "criterion": "다시 동시에 {VM} 때가 {a}{wa(a)} {b}의 공배수이며, '처음'은 최소공배수임을 밝혔다.", "partial": "공배수라는 말만 쓰고 '가장 작은'을 밝히지 않았으면 1점."},
            {"element": "최소공배수 구하기", "points": 3, "criterion": "소인수분해(또는 나눗셈)로 최소공배수 {L}{eul(L)} 바르게 구했다.", "partial": "소인수분해까지 옳고 지수 선택이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {L}분 후로 썼다.", "partial": "단위·시점 없이 수만 썼으면 1점."},
        ],
        rubric_total=8,
    )


GEAR_ROWS = {str(a * 100 + b): {**lcm_row(a, b), "ra": round(0.8 * a / max(a, b) + 0.2, 2), "rb": round(0.8 * b / max(a, b) + 0.2, 2)} for a, b in LCM_PAIRS}
GEAR_TABLE = {"key": "ab", "rows": GEAR_ROWS}
GEAR_W = {"key": "w", "rows": {"A": {"W": "A", "isB": 0}, "B": {"W": "B", "isB": 1}}}


def gl_t2():
    return tpl("m1-1-gcd-lcm-apply", 2,
        title="맞물린 두 톱니바퀴 — 처음 위치로 돌아올 때까지의 회전 수 (최소공배수)",
        skill="맞물려 지나간 톱니 수가 두 톱니 수의 최소공배수일 때 처음 위치로 돌아옴을 알고, 회전 수 = (최소공배수) ÷ (톱니 수)로 구하기",
        variant_axis={"구하는 것": "A의 회전 수 / B의 회전 수", "상황": "톱니바퀴", "맥락": "기계"},
        discriminates="지나간 톱니 수(최소공배수)와 회전 수를 구분해 톱니 수로 나누는가",
        qtype="short", difficulty=3, pool_target=300, tags=["최소공배수", "톱니바퀴", "최대공약수와 최소공배수의 활용"],
        params=[{"name": "w", "values": {"in": ["A", "B"]}}, LCM_PARAM],
        table=[GEAR_W, GEAR_TABLE],
        derive={"g": "gcd(a, b)", "ans_v": "L/a*(1 - isB) + L/b*isB"},
        constraints=["ans_v != a", "ans_v != b", "ans_v >= 2"],
        cost_values=["a", "b", "L", "ans_v"],
        verify=["lcm(a, b) == L", "(isB == 0 and ans*a == L) or (isB == 1 and ans*b == L)"],
        question="톱니의 수가 각각 {a}개, {b}개인 두 톱니바퀴 A, B가 서로 맞물려 돌고 있다. 두 톱니바퀴가 회전을 시작한 후 처음으로 다시 같은 톱니끼리 맞물릴 때까지 톱니바퀴 {W}{eun(W)} 몇 바퀴 회전하는지 구하시오.",
        answer="{ans_v}", answer_alt=["{ans_v}바퀴"],
        sol1="맞물려 도는 두 톱니바퀴는 언제나 같은 개수의 톱니가 지나간다. A가 한 바퀴 돌면 톱니 {a}개, B가 한 바퀴 돌면 톱니 {b}개가 지나가므로, 처음 위치로 돌아오려면 지나간 톱니 수가 {a}의 배수이면서 {b}의 배수 — 곧 공배수 — 여야 하고 '처음'이므로 최소공배수 {L}개다. 회전 수는 지나간 톱니 수를 그 톱니바퀴의 톱니 수로 나눈 것이다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": ["{ra + rb}", 0]}, "circles": [{"c": "A", "r": "{ra}"}, {"c": "B", "r": "{rb}"}],
                                            "labels": [{"at": "A", "text": "{a}개", "dy": -14}, {"at": "B", "text": "{b}개", "dy": -14}]}}],
        sol1_anim=[[hl("circle:0", "label:0")], [hl("circle:1", "label:1")], [hl("circle:0", "circle:1", keep=True)]],
        sol2=[
            "처음으로 다시 같은 톱니끼리 맞물릴 때까지 지나간 톱니의 수는 {a}{wa(a)} {b}의 최소공배수이다.",
            "소인수분해하면 {a} = {fa}, {b} = {fb}이므로 최소공배수는 {fl} = {L}",
            "톱니 {L}개가 지나가는 동안 톱니바퀴 A는 {L} ÷ {a} = {na}(바퀴), B는 {L} ÷ {b} = {nb}(바퀴) 회전한다.",
            "따라서 톱니바퀴 {W}{eun(W)} {ans_v}바퀴 회전한다.",
        ],
        sol2_fig=steps([
            {"text": "{a} = {fa},  {b} = {fb}", "hint": "소인수분해"},
            {"text": "최소공배수 = {fl} = {L}", "hint": "지나간 톱니 수"},
            {"text": "A: {L} ÷ {a} = {na}바퀴,  B: {L} ÷ {b} = {nb}바퀴", "hint": "회전 수 = 지나간 톱니 수 ÷ 톱니 수"},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0"), reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol3="A가 {na}바퀴 돌면 톱니 {a} × {na} = {L}개, B가 {nb}바퀴 돌면 톱니 {b} × {nb} = {L}개가 지나가 서로 같다. {L}은 {a}{wa(a)} {b}의 최소공배수이므로 이보다 먼저 같은 톱니끼리 맞물리는 일은 없다. 답은 {ans_v}바퀴다.",
        sol3_fig=steps(["A: {a} × {na} = {L}", "B: {b} × {nb} = {L}", "지나간 톱니 수가 같다 → 처음 위치"]),
        sol3_anim=[[reveal(0), reveal(1)], [reveal(2)]],
        model_answer="두 톱니바퀴가 처음으로 다시 같은 톱니끼리 맞물릴 때까지 지나간 톱니의 수는 {a}{wa(a)} {b}의 최소공배수이다. {a} = {fa}, {b} = {fb}이므로 최소공배수는 {fl} = {L}이다. 따라서 톱니바퀴 A는 {L} ÷ {a} = {na}바퀴, B는 {L} ÷ {b} = {nb}바퀴 회전하므로 톱니바퀴 {W}{eun(W)} {ans_v}바퀴 회전한다.",
        rubric=[
            {"element": "최소공배수 판단", "points": 3, "criterion": "처음 위치로 돌아올 때까지 지나간 톱니의 수가 {a}{wa(a)} {b}의 최소공배수임을 밝혔다.", "partial": "공배수라는 말만 쓰고 '가장 작은'을 밝히지 않았으면 1점."},
            {"element": "최소공배수 구하기", "points": 3, "criterion": "소인수분해(또는 나눗셈)로 최소공배수 {L}{eul(L)} 바르게 구했다.", "partial": "소인수분해까지 옳고 지수 선택이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{L}{eul(L)} 톱니바퀴 {W}의 톱니 수로 나누어 {ans_v}바퀴를 답으로 썼다.", "partial": "최소공배수 {L}{eul(L)} 그대로 회전 수로 답했으면 인정하지 않고, 다른 톱니바퀴의 회전 수를 답했으면 1점."},
        ],
        rubric_total=8,
    )


TILE_CTX = {
    "1": {"S": "직사각형 모양의 벽에", "I": "타일", "V": "붙이려고 한다"},
    "2": {"S": "직사각형 모양의 게시판에", "I": "메모지", "V": "붙이려고 한다"},
    "3": {"S": "직사각형 모양의 전시 벽에", "I": "사진 패널", "V": "걸려고 한다"},
    "4": {"S": "직사각형 모양의 책상 매트에", "I": "스티커", "V": "붙이려고 한다"},
}
GCD_PAIRS += [(75, 45), (64, 48), (90, 54), (112, 84), (98, 70), (91, 65), (85, 51), (120, 72), (105, 60), (128, 96)]


def gcd_row(a, b):
    g = math.gcd(a, b)
    return {"a": a, "b": b, "G": g, "fa": factor_str(a), "fb": factor_str(b), "fg": gcd_factor_str(a, b), "ma": a // g, "mb": b // g, "cnt": (a // g) * (b // g)}


GCD_TABLE = {"key": "ab", "rows": {str(a * 1000 + b): gcd_row(a, b) for a, b in GCD_PAIRS}}
GCD_PARAM = {"name": "ab", "values": {"in": [str(a * 1000 + b) for a, b in GCD_PAIRS]}}


def gl_tile(no, which):
    cnt = which == "cnt"
    return tpl("m1-1-gcd-lcm-apply", no,
        title="직사각형을 가능한 한 큰 정사각형으로 빈틈없이 채우기 — " + ("개수 구하기" if cnt else "한 변의 길이 구하기"),
        skill="'가능한 한 큰 정사각형으로 빈틈없이'는 가로·세로의 최대공약수임을 알고" + (", 개수는 (가로 ÷ G) × (세로 ÷ G)로 구하기" if cnt else " 소인수분해로 구하기"),
        variant_axis={"구하는 것": "개수" if cnt else "한 변의 길이", "상황": "정사각형으로 채우기", "맥락": "타일·메모지·사진 패널·스티커"},
        discriminates="최대공약수와 최소공배수를 구분하는가" + (" · 개수를 가로·세로 각각의 개수의 곱으로 구하는가" if cnt else ""),
        qtype="short", difficulty=3 if cnt else 2, pool_target=300, tags=["최대공약수", "타일", "최대공약수와 최소공배수의 활용"],
        params=[{"name": "c", "values": {"in": list(TILE_CTX)}}, GCD_PARAM],
        table=[{"key": "c", "rows": TILE_CTX}, GCD_TABLE],
        derive={"L": "lcm(a, b)"},
        constraints=["cnt != a", "cnt != b", "cnt != G"] if cnt else ["G != a", "G != b"],
        cost_values=["a", "b", "G", "ma", "mb", "cnt"],
        verify=["gcd(a, b) == G", "ans == (a/G)*(b/G)" if cnt else "ans == G"],
        question="가로 {a} cm, 세로 {b} cm인 {S} 크기가 같은 정사각형 모양의 {I}{eul(I)} 빈틈없이 {V}. 가능한 한 큰 {I}{eul(I)} 쓸 때, " + ("필요한 {I}{eun(I)} 모두 몇 장인지 구하시오." if cnt else "{I} 한 변의 길이는 몇 cm인지 구하시오."),
        answer="{cnt}" if cnt else "{G}", answer_alt=["{cnt}장"] if cnt else ["{G} cm"],
        sol1="빈틈없이 채우려면 정사각형 {I}의 한 변의 길이가 가로 {a} cm와 세로 {b} cm를 모두 나누어떨어지게 해야 한다 — 곧 {a}{wa(a)} {b}의 공약수. '가능한 한 큰'이므로 최대공약수다." + (" 한 변의 길이를 구하면 가로에 {ma}장, 세로에 {mb}장이 들어가므로 개수는 그 곱이다." if cnt else " 그림에서 가로와 세로를 같은 길이로 똑같이 나눌 수 있는 가장 긴 길이를 찾는 셈이다."),
        sol1_fig=[{"fn": "rect", "args": {"w": "{a}", "h": "{b}"}}],
        sol1_anim=[[hl("seg:A-D", "seglbl:A-D")], [hl("seg:B-A", "seglbl:B-A")], [hl("seg:A-D", "seg:B-A", keep=True)]],
        sol2=[
            "{I} 한 변의 길이는 {a}{wa(a)} {b}의 공약수이고, 가능한 한 크게 하려면 최대공약수여야 한다.",
            "소인수분해하면 {a} = {fa}, {b} = {fb}이므로 최대공약수는 {fg} = {G}",
            "따라서 {I} 한 변의 길이는 {G} cm이다.",
        ] + (["가로에는 {a} ÷ {G} = {ma}(장), 세로에는 {b} ÷ {G} = {mb}(장)이 들어가므로 필요한 {I}{eun(I)} {ma} × {mb} = {cnt}(장)이다."] if cnt else []),
        sol2_fig=steps([
            {"text": "{a} = {fa},  {b} = {fb}", "hint": "소인수분해"},
            {"text": "최대공약수 = {fg} = {G}", "hint": "공통인 소인수의 작은 지수 — 한 변의 길이"},
        ] + ([{"text": "{a} ÷ {G} = {ma},  {b} ÷ {G} = {mb}", "hint": "가로·세로에 들어가는 장수"}, {"text": "{ma} × {mb} = {cnt}", "hint": "개수"}] if cnt else [])),
        sol2_anim=[[], [reveal(0), hl("hint:0"), reveal(1), hl("hint:1")], []] + ([[reveal(2), hl("hint:2"), reveal(3), hl("hint:3")]] if cnt else []),
        sol3="한 변이 {G} cm인 {I}{eul(I)} 가로로 {ma}장 붙이면 {G} × {ma} = {a}(cm), 세로로 {mb}장 붙이면 {G} × {mb} = {b}(cm)로 딱 맞는다. {G}보다 큰 공약수는 없으므로 이보다 큰 {I}로는 빈틈없이 채울 수 없다. 답은 " + ("{cnt}장이다." if cnt else "{G} cm이다."),
        sol3_fig=steps(["{G} × {ma} = {a} (가로)", "{G} × {mb} = {b} (세로)"] + (["{ma} × {mb} = {cnt}장"] if cnt else [])),
        sol3_anim=[[reveal(0), reveal(1)]] + ([[reveal(2)]] if cnt else []),
        model_answer="{I} 한 변의 길이는 {a}{wa(a)} {b}의 공약수이고 가능한 한 크게 하려면 최대공약수여야 한다. {a} = {fa}, {b} = {fb}이므로 최대공약수는 {fg} = {G}이고, {I} 한 변의 길이는 {G} cm이다." + (" 가로에 {a} ÷ {G} = {ma}장, 세로에 {b} ÷ {G} = {mb}장이 들어가므로 필요한 {I}{eun(I)} {ma} × {mb} = {cnt}장이다." if cnt else " 실제로 {G} × {ma} = {a}, {G} × {mb} = {b}로 가로·세로가 딱 맞으므로 답은 {G} cm다."),
        rubric=[
            {"element": "최대공약수 판단", "points": 3, "criterion": "빈틈없이 채우려면 한 변의 길이가 {a}{wa(a)} {b}의 공약수이고, 가능한 한 크게 하려면 최대공약수임을 밝혔다.", "partial": "공약수라는 말만 쓰고 '가장 큰'을 밝히지 않았으면 1점."},
            {"element": "최대공약수 구하기", "points": 3, "criterion": "소인수분해(또는 나눗셈)로 최대공약수 {G}{eul(G)} 바르게 구했다.", "partial": "소인수분해까지 옳고 지수 선택이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": ("가로 {ma}장 × 세로 {mb}장 = {cnt}장을 답으로 썼다." if cnt else "답을 {G} cm로 썼다."), "partial": ("가로·세로 장수 중 하나만 구했거나 더했으면 1점." if cnt else "최대공약수를 구하고 단위 없이 수만 썼어도 2점, 최소공배수를 답했으면 인정하지 않는다.")},
        ],
        rubric_total=8,
    )


COPRIME = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5), (2, 7), (3, 7), (5, 6)]
REL = {
    "prod": {"QT": "두 자연수 A, B의 최대공약수가 {G}, 최소공배수가 {L}일 때, A × B의 값을 구하시오.", "QN": "A × B", "GIVE": "최대공약수 {G}, 최소공배수 {L}", "ANS": "{P}", "EQ": "A × B = {G} × {L} = {P}"},
    "lcm": {"QT": "두 자연수 A, B의 곱이 {P}이고 최대공약수가 {G}일 때, 두 수의 최소공배수를 구하시오.", "QN": "최소공배수", "GIVE": "곱 {P}, 최대공약수 {G}", "ANS": "{L}", "EQ": "{P} = {G} × L,  L = {P} ÷ {G} = {L}"},
    "gcd": {"QT": "두 자연수 A, B의 곱이 {P}이고 최소공배수가 {L}일 때, 두 수의 최대공약수를 구하시오.", "QN": "최대공약수", "GIVE": "곱 {P}, 최소공배수 {L}", "ANS": "{G}", "EQ": "{P} = G × {L},  G = {P} ÷ {L} = {G}"},
}


def gl_rel(no, which):
    r = REL[which]
    return tpl("m1-1-gcd-lcm-apply", no,
        title="두 수의 곱 = (최대공약수) × (최소공배수) — " + r["QN"] + " 구하기",
        skill="A = G·p, B = G·q (p, q는 서로소)로 놓아 A × B = G × L 임을 유도하고 활용하기",
        variant_axis={"구하는 것": r["QN"], "주어진 정보": r["GIVE"].replace("{G}", "G").replace("{L}", "L").replace("{P}", "P")},
        discriminates="A × B = G × L 관계를 근거(A = Gp, B = Gq, L = Gpq)와 함께 쓰는가",
        qtype="short", difficulty=3, pool_target=300, tags=["최대공약수", "최소공배수", "최대공약수와 최소공배수의 관계"],
        params=[{"name": "G", "values": {"in": [2, 3, 4, 5, 6, 8, 9, 10, 12]}}, {"name": "pq", "values": {"in": [p * 10 + q for p, q in COPRIME]}}],
        derive={"p": "floor(pq/10)", "q": "pq % 10", "A": "G*floor(pq/10)", "B": "G*(pq % 10)", "L": "G*floor(pq/10)*(pq % 10)", "P": "G*G*floor(pq/10)*(pq % 10)"},
        constraints=["G != L", "G != P", "L != P", "P >= 30"],
        cost_values=["G", "L", "P"],
        verify=["gcd(A, B) == G", "lcm(A, B) == L", "A*B == P", "ans == " + {"prod": "P", "lcm": "L", "gcd": "G"}[which]],
        question=r["QT"],
        answer=r["ANS"], answer_alt=[],
        sol1="최대공약수가 G인 두 수는 A = G × p, B = G × q (p, q는 서로소)로 쓸 수 있고, 그때 최소공배수는 L = G × p × q이다. 그러면 A × B = G × p × G × q = G × (G × p × q) = G × L — 두 수의 곱은 언제나 (최대공약수) × (최소공배수)이다. 주어진 것은 " + r["GIVE"] + "이므로 이 관계식에서 나머지 하나를 구한다.",
        sol1_fig=steps(["A = G × p,  B = G × q  (p, q는 서로소)", "L = G × p × q", "A × B = G × p × G × q = G × L"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "두 자연수의 최대공약수를 G, 최소공배수를 L이라 하면 A = G × p, B = G × q (p, q는 서로소), L = G × p × q이므로 A × B = G × L이다.",
            "주어진 값(" + r["GIVE"] + ")을 A × B = G × L에 넣으면 " + r["EQ"],
            "따라서 " + r["QN"] + "{eun_qn} " + r["ANS"] + "이다.",
        ],
        sol2_fig=steps([
            {"text": "A × B = G × L", "hint": "(두 수의 곱) = (최대공약수) × (최소공배수)"},
            {"text": r["EQ"], "hint": r["GIVE"], "marks": [{"on": r["ANS"], "note": "구하는 값"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], []],
        sol3="예를 들어 두 수가 A = {A}, B = {B}이면 최대공약수는 {G}, 최소공배수는 {L}이고 곱은 {A} × {B} = {P}이다. 실제로 {G} × {L} = {P}로 A × B = G × L이 성립한다. 답은 " + r["ANS"] + "이다.",
        sol3_fig=steps(["A = {A} = {G} × {p},  B = {B} = {G} × {q}", "G = {G},  L = {G} × {p} × {q} = {L}", "A × B = {P} = {G} × {L}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="두 자연수의 최대공약수를 G, 최소공배수를 L이라 하면 A = G × p, B = G × q (p, q는 서로소)이고 L = G × p × q이므로 A × B = G × L이다. 주어진 값을 넣으면 " + r["EQ"] + "이므로 " + r["QN"] + "{eun_qn} " + r["ANS"] + "이다.",
        rubric=[
            {"element": "관계식 세우기", "points": 3, "criterion": "A = Gp, B = Gq, L = Gpq에서 A × B = G × L임을 유도하거나 관계식을 밝혀 썼다.", "partial": "관계식만 쓰고 근거를 쓰지 않았으면 2점."},
            {"element": "값 구하기", "points": 3, "criterion": "관계식에 주어진 값을 넣어 " + r["QN"] + " " + r["ANS"] + "{eul_ans} 바르게 구했다.", "partial": "대입은 옳으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 " + r["ANS"] + "{ro_ans} 썼다.", "partial": "구하는 값이 아닌 다른 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def _rel_fix(t, which):
    """{eun_qn}·{eul_ans}·{ro_ans} 자리표시자를 조사 함수로 — QN 은 고정 문자열이라 미리 계산한다."""
    qn = REL[which]["QN"]
    eun = "은" if (ord(qn[-1]) - 0xAC00) % 28 != 0 and "\uac00" <= qn[-1] <= "\ud7a3" else "는"
    var = {"prod": "P", "lcm": "L", "gcd": "G"}[which]
    from seedlib import sub_all
    return sub_all(t, {"{eun_qn}": eun, "{eul_ans}": "{eul(%s)}" % var, "{ro_ans}": "{ro(%s)}" % var})


GL_SEED = {
    "seed_id": "m1-1-gcd-lcm-apply", "category": "활용",
    "title": "최대공약수·최소공배수의 활용 — 동시 출발·톱니바퀴·정사각형 채우기·곱의 관계",
    "unit_id": "m1-1", "concept_ids": ["m1-1-07", "m1-1-08"],
    "schema_id": SCHEMA_GL_REL, "schema_name": "최대공약수·최소공배수의 응용 / 두 수의 곱과 최대공약수·최소공배수 관계",
    "source_item_ids": [],
    "note": "구조만 차용. 수 쌍은 최소공배수·최대공약수가 적당한 것만 표로 굽고 소인수분해 문자열도 표에 둔다. 맥락은 요즘 상황(지하철·셔틀·놀이기구·게시판·전시 벽) 표 변주.",
    "geometry": False,
    "templates": [gl_t1(), gl_t2(), gl_tile(3, "len"), gl_tile(4, "cnt"), _rel_fix(gl_rel(5, "prod"), "prod"), _rel_fix(gl_rel(6, "lcm"), "lcm"), _rel_fix(gl_rel(7, "gcd"), "gcd")],
}


# ═══════════════════════════════════════════════════════════════════ 2. 절댓값이 같고 부호가 반대인 두 수
ABS_BASE = dict(context="무맥락", prereq=["절댓값", "수직선"], ops=["사칙"], tags=["절댓값", "수직선"], traps=["부호", "구하는대상혼동"], time_limit=90, points=4)


def abs_t1():
    return tpl("m1-1-abs-pair", 1, **ABS_BASE,
        title="절댓값이 같고 부호가 반대인 두 수 — 거리(차)로 두 수 구하기",
        skill="절댓값이 같고 부호가 반대인 두 수는 원점에서 같은 거리에 있으므로 두 점 사이의 거리를 반으로 나누기",
        variant_axis={"구하는 것": "큰 수 / 작은 수", "주어진 조건": "두 점 사이의 거리 / 차"},
        discriminates="'절댓값이 같고 부호가 반대'를 원점 대칭으로 읽고 거리를 2로 나누는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "q", "values": {"in": ["big-dist", "small-dist", "big-diff", "small-diff"]}}, {"name": "h", "values": {"int": [2, 30]}}],
        table={"key": "q", "rows": {
            "big-dist": {"Q": "큰 수", "o": 1, "COND": "수직선 위에서 두 수를 나타내는 두 점 사이의 거리가", "CN": "거리"},
            "small-dist": {"Q": "작은 수", "o": -1, "COND": "수직선 위에서 두 수를 나타내는 두 점 사이의 거리가", "CN": "거리"},
            "big-diff": {"Q": "큰 수", "o": 1, "COND": "큰 수에서 작은 수를 뺀 차가", "CN": "차"},
            "small-diff": {"Q": "작은 수", "o": -1, "COND": "큰 수에서 작은 수를 뺀 차가", "CN": "차"},
        }},
        derive={"d": "2*h", "ans_v": "o*h", "nh": "-h"},
        constraints=["d != h"],
        cost_values=["d", "h", "ans_v"],
        relation="2*o*X - d", unknown="X", answer_var="ans_v",
        verify=["abs(ans) == d/2", "ans*o > 0"],
        question="절댓값이 같고 부호가 반대인 두 수가 있다. {COND} {d}일 때, 두 수 중 {Q}{eul(Q)} 구하시오.",
        answer="{ans_v}", answer_alt=[],
        sol1="절댓값이 같다는 것은 원점 0에서 같은 거리에 있다는 뜻이고, 부호가 반대이므로 한 수는 0의 오른쪽, 다른 수는 왼쪽에 있다. 그러면 두 점은 0을 가운데에 두고 마주 보므로, 두 점 사이의 {CN} {d}{eul(d)} 반으로 나눈 {h}{ika(h)} 각 점과 0 사이의 거리다. 수직선에 그려 보면 바로 보인다.",
        sol1_fig=numline("{nh - 2}", "{h + 2}", [{"x": "{nh}", "label": "b"}, {"x": 0, "label": "0"}, {"x": "{h}", "label": "a"}], [["{nh}", 0], [0, "{h}"]]),
        sol1_anim=[[hl("pt:0", "lbl:0", keep=True)], [hl("seg:0", "seg:1")], [hl("pt:a", "lbl:a", "pt:b", "lbl:b", keep=True)]],
        sol2=[
            "두 수를 a, b (a > b)라 하면 절댓값이 같고 부호가 반대이므로 a > 0, b < 0이고 |a| = |b|이다.",
            "두 수는 원점에서 같은 거리에 있으므로, 두 점 사이의 {CN} {d}{eun(d)} 원점까지의 거리의 2배이다: 2 × |a| = {d}",
            "따라서 |a| = |b| = {d} ÷ 2 = {h}",
            "a > 0, b < 0이므로 a = {h}, b = {nh}",
            "구하는 것은 {Q}이므로 {ans_v}",
        ],
        sol2_fig=steps([
            {"text": "|a| = |b|,  a > 0 > b", "hint": "절댓값 같고 부호 반대"},
            {"text": "2 × |a| = {d}", "hint": "두 점 사이의 {CN} = 원점까지의 거리 × 2"},
            {"text": "|a| = {h}", "marks": [{"on": "{h}", "note": "{d}÷2"}]},
            {"text": "a = {h},  b = {nh}", "hint": "부호를 붙인다"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3), hl("hint:3")], []],
        sol3="{h}{wa(h)} {nh}{eun(nh)} 절댓값이 모두 {h}{ro(h)} 같고 부호가 반대이며, 두 수의 차는 {h} − ({nh}) = {d}로 조건과 같다. 따라서 {Q}{eun(Q)} {ans_v}이다.",
        sol3_fig=numline("{nh - 2}", "{h + 2}", [{"x": "{nh}", "label": "{nh}"}, {"x": 0, "label": "0"}, {"x": "{h}", "label": "{h}"}], [["{nh}", "{h}"]]),
        sol3_anim=[[hl("seg:0")], [hl("pt:{ans_v}", "lbl:{ans_v}", keep=True)]],
        model_answer="두 수를 a, b (a > b)라 하면 절댓값이 같고 부호가 반대이므로 a > 0, b < 0이고 두 수는 원점에서 같은 거리에 있다. 두 점 사이의 {CN}{ika(CN)} {d}이므로 원점까지의 거리는 각각 {d} ÷ 2 = {h}이고, a = {h}, b = {nh}이다. 따라서 {Q}{eun(Q)} {ans_v}이다.",
        rubric=[
            {"element": "원점 대칭 파악", "points": 3, "criterion": "절댓값이 같고 부호가 반대인 두 수는 원점에서 같은 거리에 있음을 밝히고 수직선(또는 식)으로 나타냈다.", "partial": "'부호가 반대'만 쓰고 원점에서의 거리가 같다는 근거를 쓰지 않았으면 1점."},
            {"element": "원점까지의 거리 구하기", "points": 3, "criterion": "두 점 사이의 {CN} {d}{eul(d)} 반으로 나누어 원점까지의 거리 {h}{eul(h)} 구했다.", "partial": "2로 나누지 않고 {d}{eul(d)} 그대로 절댓값으로 썼으면 인정하지 않고, 나눗셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "부호를 붙여 두 수 {h}, {nh}{eul(nh)} 구하고 {Q} {ans_v}{eul(ans_v)} 답으로 썼다.", "partial": "두 수를 모두 구하고 {Q}{eul(Q)} 표시하지 않았으면 1점."},
        ],
        rubric_total=8,
    )


def abs_t2():
    return tpl("m1-1-abs-pair", 2, **ABS_BASE,
        title="절댓값이 a 이하(미만)인 정수의 개수",
        skill="|x| ≤ a 를 −a ≤ x ≤ a 로 읽고 수직선에서 정수를 세기 (0을 빠뜨리지 않기)",
        variant_axis={"부등호": "이하 / 미만", "구하는 것": "정수의 개수"},
        discriminates="절댓값 조건을 −a ~ a 구간으로 옮기고 0과 양 끝의 포함 여부를 바르게 세는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "q", "values": {"in": ["le", "lt"]}}, {"name": "a", "values": {"int": [4, 60]}}],
        table={"key": "q", "rows": {
            "le": {"Q": "이하", "e": 1, "SYM": "≤", "EDGE": "양 끝도 포함되므로", "K": "포함"},
            "lt": {"Q": "미만", "e": 0, "SYM": "<", "EDGE": "양 끝은 포함되지 않으므로", "K": "제외"},
        }},
        derive={"m": "a - 1 + e", "cnt": "2*(a - 1 + e) + 1", "na": "-a", "nm": "-(a - 1 + e)"},
        constraints=["cnt != a"],
        cost_values=["a", "cnt", "m"],
        verify=["ans == 2*m + 1", "m == a - 1 + e"],
        question="절댓값이 {a} {Q}인 정수는 모두 몇 개인지 구하시오.",
        answer="{cnt}", answer_alt=["{cnt}개"],
        sol1="절댓값이 {a} {Q}라는 것은 원점 0에서의 거리가 {a} {Q}라는 뜻이다. 그런 수는 수직선에서 {na}{wa(na)} {a} 사이(|x| {SYM} {a})에 있고, {EDGE} 정수는 {nm}부터 {m}까지다. 음의 정수, 0, 양의 정수로 나누어 세면 빠뜨리지 않는다 — 특히 0을 잊기 쉽다.",
        sol1_fig=numline("{na - 1}", "{a + 1}", [{"x": "{na}", "label": "{na}"}, {"x": 0, "label": "0"}, {"x": "{a}", "label": "{a}"}], [{"start": "{nm}", "end": "{m}"}]),
        sol1_anim=[[hl("pt:{na}", "lbl:{na}", "pt:{a}", "lbl:{a}")], [hl("seg:0", keep=True)], [hl("pt:0", "lbl:0")]],
        sol2=[
            "절댓값이 {a} {Q}인 수 x는 |x| {SYM} {a}, 곧 원점에서의 거리가 {a} {Q}인 수이다.",
            "{EDGE} 이 조건을 만족하는 정수는 {nm}, …, 0, …, {m}이다.",
            "양의 정수는 1부터 {m}까지 {m}개, 음의 정수도 {m}개, 그리고 0이 1개다.",
            "따라서 정수의 개수는 {m} + {m} + 1 = {cnt}(개)이다.",
        ],
        sol2_fig=steps([
            {"text": "|x| {SYM} {a}", "hint": "원점에서의 거리가 {a} {Q}"},
            {"text": "{nm}, …, 0, …, {m}", "hint": "양 끝 ±{a}{eun(a)} {K}"},
            {"text": "{m} + {m} + 1 = {cnt}", "hint": "음의 정수 + 양의 정수 + 0", "marks": [{"on": "+ 1", "note": "0을 잊지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="{m}의 절댓값 {m}{eun(m)} 조건 '{a} {Q}'에 맞고 {m+1}의 절댓값 {m+1}{eun(m+1)} 맞지 않으므로 경계가 맞다. 세어 보면 {nm}부터 {m}까지 정수는 {cnt}개다. 답은 {cnt}개다.",
        sol3_fig=numline("{na - 1}", "{a + 1}", [{"x": "{nm}", "label": "{nm}"}, {"x": 0, "label": "0"}, {"x": "{m}", "label": "{m}"}], [{"start": "{nm}", "end": "{m}"}]),
        sol3_anim=[[hl("seg:0", keep=True)], [hl("pt:{nm}", "lbl:{nm}", "pt:{m}", "lbl:{m}")]],
        model_answer="절댓값이 {a} {Q}인 수 x는 |x| {SYM} {a}, 곧 원점에서의 거리가 {a} {Q}인 수이므로 이 조건을 만족하는 정수는 {nm}, …, 0, …, {m}이다. 양의 정수 {m}개, 음의 정수 {m}개, 0이 1개이므로 모두 {m} + {m} + 1 = {cnt}개다.",
        rubric=[
            {"element": "조건을 구간으로 옮기기", "points": 3, "criterion": "절댓값이 {a} {Q}인 수를 원점에서의 거리로 해석해 {nm}부터 {m}까지의 정수(양 끝 {K})로 나타냈다.", "partial": "구간은 맞으나 양 끝 포함 여부가 틀렸으면 1점."},
            {"element": "개수 세기", "points": 3, "criterion": "음의 정수 {m}개, 0, 양의 정수 {m}개로 나누어 세거나 나열하여 {cnt}개를 구했다.", "partial": "0을 빠뜨려 {cnt - 1}개로 셌으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {cnt}개로 썼다.", "partial": "절댓값이 {a}인 수의 개수(2개)처럼 다른 것을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def abs_t3():
    return tpl("m1-1-abs-pair", 3, **ABS_BASE,
        title="절댓값이 분수 이하인 정수의 개수",
        skill="|x| ≤ p/q 를 수직선에 옮겨 분수 경계 안쪽의 정수를 세기",
        variant_axis={"경계": "분수", "구하는 것": "정수의 개수"},
        discriminates="분수 경계를 정수 경계로 바꾸어(가장 큰 정수) 세는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "m", "values": {"int": [2, 24]}}, {"name": "fr", "values": {"in": ["12", "13", "23", "14", "34", "15", "25", "35", "45"]}}],
        table={"key": "fr", "rows": {
            "12": {"nu": 1, "de": 2}, "13": {"nu": 1, "de": 3}, "23": {"nu": 2, "de": 3}, "14": {"nu": 1, "de": 4}, "34": {"nu": 3, "de": 4},
            "15": {"nu": 1, "de": 5}, "25": {"nu": 2, "de": 5}, "35": {"nu": 3, "de": 5}, "45": {"nu": 4, "de": 5},
        }},
        derive={"N": "m*de + nu", "cnt": "2*m + 1", "nm": "-m"},
        constraints=["cnt != N", "cnt != de"],
        cost_values=["N", "de", "m", "cnt"],
        verify=["ans == 2*floor(N/de) + 1", "N/de > m", "N/de < m + 1"],
        question="절댓값이 [[frac({N},{de})]] 이하인 정수는 모두 몇 개인지 구하시오.",
        answer="{cnt}", answer_alt=["{cnt}개"],
        sol1="절댓값이 {N}/{de} 이하라는 것은 원점에서의 거리가 {N}/{de} 이하라는 뜻이므로 −{N}/{de}부터 {N}/{de}까지의 수다. {N}/{de} = {m} + {nu}/{de}이므로 {m}{wa(m)} {m+1} 사이에 있고, 이 범위 안의 정수는 {nm}부터 {m}까지다. 경계가 분수일 때는 그 안쪽의 가장 큰 정수를 먼저 찾는다.",
        sol1_fig=numline("{nm - 1}", "{m + 1}", [{"x": "{nm}", "label": "{nm}"}, {"x": 0, "label": "0"}, {"x": "{m}", "label": "{m}"}], [{"start": "{-N/de}", "end": "{N/de}"}]),
        sol1_anim=[[hl("seg:0", keep=True)], [hl("pt:{nm}", "lbl:{nm}", "pt:{m}", "lbl:{m}")], [hl("pt:0", "lbl:0")]],
        sol2=[
            "절댓값이 {N}/{de} 이하인 수 x는 |x| ≤ {N}/{de}, 곧 −{N}/{de} ≤ x ≤ {N}/{de}이다.",
            "{N}/{de} = {m} + {nu}/{de}이므로 {m} < {N}/{de} < {m+1}이고, 이 범위 안의 정수는 {nm}, …, 0, …, {m}이다.",
            "양의 정수 {m}개, 음의 정수 {m}개, 0이 1개이므로 정수의 개수는 {m} + {m} + 1 = {cnt}(개)이다.",
        ],
        sol2_fig=steps([
            {"text": "|x| ≤ {N}/{de}", "hint": "원점에서의 거리가 {N}/{de} 이하"},
            {"text": "{N}/{de} = {m} + {nu}/{de}  →  {m} < {N}/{de} < {m+1}", "hint": "경계 안쪽의 가장 큰 정수는 {m}"},
            {"text": "{nm}, …, 0, …, {m}  →  {m} + {m} + 1 = {cnt}", "marks": [{"on": "+ 1", "note": "0을 잊지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{m}의 절댓값 {m}{eun(m)} {N}/{de}보다 작고 {m+1}의 절댓값 {m+1}{eun(m+1)} {N}/{de}보다 크므로 경계가 맞다. {nm}부터 {m}까지 정수는 {cnt}개다. 답은 {cnt}개다.",
        sol3_fig=numline("{nm - 1}", "{m + 1}", [{"x": "{nm}", "label": "{nm}"}, {"x": 0, "label": "0"}, {"x": "{m}", "label": "{m}"}], [{"start": "{nm}", "end": "{m}"}]),
        sol3_anim=[[hl("seg:0", keep=True)], [hl("pt:{nm}", "lbl:{nm}", "pt:{m}", "lbl:{m}")]],
        model_answer="절댓값이 {N}/{de} 이하인 수 x는 |x| ≤ {N}/{de}, 곧 −{N}/{de} ≤ x ≤ {N}/{de}이다. {N}/{de} = {m} + {nu}/{de}이므로 이 범위 안의 정수는 {nm}부터 {m}까지이고, 양의 정수 {m}개, 음의 정수 {m}개, 0이 1개이므로 모두 {cnt}개다.",
        rubric=[
            {"element": "조건을 구간으로 옮기기", "points": 3, "criterion": "절댓값이 {N}/{de} 이하인 수를 원점에서의 거리로 해석해 −{N}/{de} ≤ x ≤ {N}/{de}로 나타내고, 경계 안쪽의 정수가 {nm}부터 {m}까지임을 밝혔다.", "partial": "구간은 맞으나 정수 경계 {m}{eul(m)} 잘못 잡았으면 1점."},
            {"element": "개수 세기", "points": 3, "criterion": "음의 정수 {m}개, 0, 양의 정수 {m}개로 나누어 세거나 나열하여 {cnt}개를 구했다.", "partial": "0을 빠뜨려 {cnt - 1}개로 셌으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {cnt}개로 썼다.", "partial": "가장 큰 정수 {m}{eul(m)} 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


ABS_SEED = {
    "seed_id": "m1-1-abs-pair", "category": "활용",
    "title": "절댓값 — 부호가 반대인 두 수·절댓값 조건을 만족하는 정수의 개수",
    "unit_id": "m1-1", "concept_ids": ["m1-1-12"],
    "schema_id": SCHEMA_ABS, "schema_name": "절댓값이 같고 부호가 반대인 두 수 / 절댓값 부등식을 만족하는 정수 개수",
    "source_item_ids": [],
    "note": "구조만 차용. 거리 d는 짝수(2h)로 생성해 정수해 보장. 정수 개수는 2m+1 꼴로 생성. 그림은 수직선(원점 대칭·구간).",
    "geometry": False,
    "templates": [abs_t1(), abs_t2(), abs_t3()],
}


if __name__ == "__main__":
    for seed in (GL_SEED, ABS_SEED):
        with_pitfalls(seed)
        dump(seed)
