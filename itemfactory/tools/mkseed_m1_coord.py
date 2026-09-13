# itemfactory/tools/mkseed_m1_coord.py — m1-1 좌표평면·정비례/반비례 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m1_coord.py
#     → seeds/m1-1-coordinate.json  (순서쌍 같음·대칭점·사분면 판정·좌표 삼각형 넓이·축 위의 점, 5틀)
#     → seeds/m1-1-proportion.json  (정비례 점·반비례 점·그래프 지나는 점→a·두 점→k·정비례 삼각형 넓이·반비례 직사각형 넓이, 6틀)
#
# 정비례 그래프는 틀 안에서 자른 선분으로 그린다(expr 표본화의 수평 꼬리 회피, HANDOFF §1-1). 반비례 곡선은 그리지 않는다(점·수선만).
from __future__ import annotations

import os
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def cplane(xs, ys, points, lines=None, **extra):
    a = {"x": xs, "y": ys, "points": points}
    if lines:
        a["lines"] = lines
    a.update(extra)
    return [{"fn": "coordplane", "args": a}]


NZ = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
NZ2 = [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]
BASE = {"process": "절차수행", "context": "무맥락", "ops": ["좌표", "사칙"], "traps": ["부호", "구하는대상혼동"], "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}

# ═══════════════════════════════════════════════════════════════════ 1. 좌표평면
CO = "m1-1-coordinate"
CO_BASE = {**BASE, "prereq": ["순서쌍과 좌표", "사분면"], "tags": ["좌표평면", "순서쌍"]}
AB_ROWS = {"sum": {"QT": "a + b", "c1": 1, "c2": 1, "cp": 0}, "diff": {"QT": "a − b", "c1": 1, "c2": -1, "cp": 0}, "prod": {"QT": "ab", "c1": 0, "c2": 0, "cp": 1}}


def co_t1():
    return tpl(CO, 1, CO_BASE,
        title="서로 같은 두 순서쌍 — a, b 구하기",
        skill="두 순서쌍이 같으면 x좌표끼리, y좌표끼리 각각 같음을 이용해 a, b를 구하기",
        variant_axis={"구하는 것": "a + b / a − b / ab", "계수": "±1~±4"},
        discriminates="x좌표끼리·y좌표끼리 대응시키는가(자리를 바꾸지 않는가), 일차방정식을 바르게 푸는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(AB_ROWS)}}, {"name": "a", "values": {"in": NZ}}, {"name": "b", "values": {"in": NZ}},
                {"name": "p", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "q", "values": {"in": NZ}}, {"name": "t", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "u", "values": {"in": NZ}}],
        table={"key": "q1", "rows": AB_ROWS},
        derive={"s": "p*a + q", "r": "t*b + u", "ans": "c1*a + c2*b + cp*a*b"},
        constraints=["a != b", "ans != 0", "ans != s", "ans != r", "ans != q", "ans != u", "ans != p", "ans != t", "s != r", "s != 0", "r != 0"],
        cost_values=["p", "q", "r", "s", "t", "u", "a", "b", "ans"],
        answer_var="ans",
        verify=["p*a + q == s", "t*b + u == r", "ans == c1*a + c2*b + cp*a*b"],
        question="두 순서쌍 ({co(p)}a {sgn(q)}, {r}), ({s}, {co(t)}b {sgn(u)}){ika(u)} 서로 같을 때, {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 순서쌍이 서로 같다는 것은 x좌표끼리 같고 y좌표끼리 같다는 뜻이다. 첫째 순서쌍의 x좌표 {co(p)}a {sgn(q)}{wa(q)} 둘째의 x좌표 {s}{eul(s)} 같게 놓아 a를, y좌표 {r}{wa(r)} {co(t)}b {sgn(u)}{eul(u)} 같게 놓아 b를 구한다.",
        sol2=[
            "x좌표가 같으므로 {co(p)}a {sgn(q)} = {s}, a = {a}",
            "y좌표가 같으므로 {co(t)}b {sgn(u)} = {r}, b = {b}",
            "따라서 {QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}a {sgn(q)} = {s}  →  a = {a}", "hint": "x좌표끼리"},
            {"text": "{co(t)}b {sgn(u)} = {r}  →  b = {b}", "hint": "y좌표끼리"},
            {"text": "{QT} = {ans}", "marks": [{"on": "{ans}", "note": "자리를 바꾸지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="a = {a}, b = {b}{eul(b)} 넣으면 두 순서쌍은 모두 ({s}, {r})로 같다. 따라서 {QT} = {ans}이다.",
        sol3_fig=steps(["({p} × {pn(a)} {sgn(q)}, {r}) = ({s}, {r})", "({s}, {t} × {pn(b)} {sgn(u)}) = ({s}, {r})"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 순서쌍이 같으므로 {co(p)}a {sgn(q)} = {s}에서 a = {a}, {co(t)}b {sgn(u)} = {r}에서 b = {b}이다. 따라서 {QT} = {ans}이다.",
        rubric=[
            {"element": "좌표 대응", "points": 3, "criterion": "x좌표끼리, y좌표끼리 같게 놓아 두 방정식 {co(p)}a {sgn(q)} = {s}, {co(t)}b {sgn(u)} = {r}{eul(r)} 세웠다.", "partial": "x좌표와 y좌표를 바꿔 대응시켰으면 인정하지 않는다."},
            {"element": "a, b 구하기", "points": 2, "criterion": "a = {a}, b = {b}{eul(b)} 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 답했다.", "partial": "a, b만 쓰고 {QT}{eul(QT)} 쓰지 않았으면 1점."},
        ],
        rubric_total=7,
    )


SYM_ROWS = {"x": {"AX": "x축", "sx": 1, "sy": -1, "RULE": "y좌표의 부호만 바뀐다", "KEEP": "x좌표"},
            "y": {"AX": "y축", "sx": -1, "sy": 1, "RULE": "x좌표의 부호만 바뀐다", "KEEP": "y좌표"},
            "o": {"AX": "원점", "sx": -1, "sy": -1, "RULE": "x좌표와 y좌표의 부호가 모두 바뀐다", "KEEP": "절댓값"}}


def co_t2():
    return tpl(CO, 2, CO_BASE,
        title="x축·y축·원점에 대하여 대칭인 점의 좌표",
        skill="x축 대칭은 y좌표의 부호, y축 대칭은 x좌표의 부호, 원점 대칭은 두 좌표의 부호를 바꾸는 것임을 알고 좌표 구하기",
        variant_axis={"대칭의 기준": "x축 / y축 / 원점", "구하는 것": "a + b / a − b / ab"},
        discriminates="어느 좌표의 부호가 바뀌는지 기준별로 구별하는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(AB_ROWS)}}, {"name": "sym", "values": {"in": list(SYM_ROWS)}}, {"name": "x", "values": {"in": NZ}}, {"name": "y", "values": {"in": NZ}}],
        table=[{"key": "q1", "rows": AB_ROWS}, {"key": "sym", "rows": SYM_ROWS}],
        derive={"a": "sx*x", "b": "sy*y", "ans": "c1*sx*x + c2*sy*y + cp*sx*sy*x*y"},
        constraints=["abs(x) != abs(y)", "ans != 0", "ans != x", "ans != y"],
        cost_values=["x", "y", "a", "b", "ans"],
        answer_var="ans",
        verify=["a == sx*x", "b == sy*y", "ans == c1*a + c2*b + cp*a*b"],
        question="점 ({x}, {y}){wa(y)} {AX}에 대하여 대칭인 점의 좌표가 (a, b)일 때, {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{AX}에 대하여 대칭인 점은 {AX}{eul(AX)} 접는 선(중심)으로 접었을 때 겹치는 점이다. 그러면 {RULE}. 점 ({x}, {y})에 이 규칙을 적용해 (a, b)를 구하고 {QT}{eul(QT)} 계산한다.",
        sol1_fig=cplane(["{-abs(x) - 2}", "{abs(x) + 2}"], ["{-abs(y) - 2}", "{abs(y) + 2}"], [{"name": "P", "coord": ["{x}", "{y}"]}, {"name": "Q", "coord": ["{a}", "{b}"]}], [{"points": [["{x}", "{y}"], ["{a}", "{b}"]], "style": "dashed"}]),
        sol1_anim=[[hl("pt:P", "lbl:P")], [hl("line:0")], [hl("pt:Q", "lbl:Q", keep=True)]],
        sol2=[
            "{AX}에 대하여 대칭이면 {RULE}.",
            "따라서 점 ({x}, {y})와 {AX}에 대하여 대칭인 점은 ({a}, {b}), 곧 a = {a}, b = {b}",
            "{QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "({x}, {y})  →  ({a}, {b})", "hint": "{AX} 대칭: {RULE}", "marks": [{"on": "({a}, {b})", "note": "바뀌는 부호 확인"}]},
            {"text": "a = {a},  b = {b}"},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1)], [reveal(2)]],
        sol3="점 ({x}, {y})와 ({a}, {b})는 {AX}{eul(AX)} 기준으로 서로 반대쪽에 같은 거리만큼 떨어져 있으므로 {AX}에 대하여 대칭이 맞다. 따라서 {QT} = {ans}이다.",
        sol3_fig=cplane(["{-abs(x) - 2}", "{abs(x) + 2}"], ["{-abs(y) - 2}", "{abs(y) + 2}"], [{"name": "P", "coord": ["{x}", "{y}"]}, {"name": "Q", "coord": ["{a}", "{b}"]}]),
        model_answer="{AX}에 대하여 대칭이면 {RULE}. 따라서 점 ({x}, {y})와 {AX}에 대하여 대칭인 점은 ({a}, {b})이므로 a = {a}, b = {b}이고 {QT} = {ans}이다.",
        rubric=[
            {"element": "대칭의 규칙", "points": 3, "criterion": "{AX} 대칭에서 {RULE}는 것을 밝혔다.", "partial": "다른 기준의 규칙을 적용했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "(a, b) = ({a}, {b})에서 {QT} = {ans}{eul(ans)} 구했다.", "partial": "좌표는 맞고 {QT}의 계산이 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


def _quad_rows():
    """점 (a, b)가 제k사분면 → (F1, F2)의 사분면. 부호가 정해지는 식만 쓴다."""
    sgn = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}
    exprs = {"a": lambda sa, sb: sa, "b": lambda sa, sb: sb, "-a": lambda sa, sb: -sa, "-b": lambda sa, sb: -sb,
             "ab": lambda sa, sb: sa * sb, "-ab": lambda sa, sb: -sa * sb, "a²b": lambda sa, sb: sb, "ab²": lambda sa, sb: sa}
    show = {"a": "a", "b": "b", "-a": "−a", "-b": "−b", "ab": "ab", "-ab": "−ab", "a²b": "a²b", "ab²": "ab²"}
    rows = {}
    for k, (sa, sb) in sgn.items():
        for e1, e2 in product(list(show), repeat=2):
            if e1 == e2:
                continue
            s1, s2 = exprs[e1](sa, sb), exprs[e2](sa, sb)
            n = {(1, 1): 1, (-1, 1): 2, (-1, -1): 3, (1, -1): 4}[(s1, s2)]
            if n == k:
                continue                                                    # 답이 문면의 사분면 번호와 같으면 R-05
            rows[f"{k}-{e1}-{e2}"] = {"k": k, "F1": show[e1], "F2": show[e2], "n": n, "s1": s1, "s2": s2, "sa": sa, "sb": sb,
                                       "SA": "a > 0" if sa > 0 else "a < 0", "SB": "b > 0" if sb > 0 else "b < 0",
                                       "T1": ("양수" if s1 > 0 else "음수"), "T2": ("양수" if s2 > 0 else "음수")}
    return rows


QUAD_ROWS = _quad_rows()


def co_t3():
    return tpl(CO, 3, CO_BASE,
        title="점 (a, b)의 사분면으로 다른 점의 사분면 판정하기",
        skill="사분면에서 a, b의 부호를 읽고, 곱·부호 반전의 부호를 정해 새 점이 속한 사분면의 번호를 구하기",
        variant_axis={"주어진 사분면": "1~4", "좌표 식": "a, b, −a, −b, ab, −ab, a²b, ab²"},
        discriminates="사분면 번호를 부호 조합으로 옮기고 되돌리는가, 곱의 부호와 제곱의 부호를 바르게 정하는가",
        difficulty=3, process="추론",
        params=[{"name": "r", "values": {"in": list(QUAD_ROWS)}}],
        table={"key": "r", "rows": QUAD_ROWS},
        derive={"ans": "n"},
        constraints=["n != k"],
        cost_values=["k", "n"],
        answer_var="ans",
        verify=["ans == n", "n != k", "(s1 > 0 and s2 > 0 and n == 1) or (s1 < 0 and s2 > 0 and n == 2) or (s1 < 0 and s2 < 0 and n == 3) or (s1 > 0 and s2 < 0 and n == 4)"],
        question="점 (a, b)가 제{k}사분면 위의 점일 때, 점 ({F1}, {F2})는 제n사분면 위의 점이다. n의 값을 구하시오.",
        answer="{n}", answer_alt=[],
        sol1="사분면은 x좌표와 y좌표의 부호로 정해진다: 제1사분면 (+, +), 제2사분면 (−, +), 제3사분면 (−, −), 제4사분면 (+, −). 점 (a, b)가 제{k}사분면에 있으므로 {SA}, {SB}이다. 이것으로 {F1}과 {F2}의 부호를 정하면 점 ({F1}, {F2})가 어느 사분면에 있는지 알 수 있다.",
        sol2=[
            "점 (a, b)가 제{k}사분면 위의 점이므로 {SA}, {SB}",
            "따라서 {F1}{eun(F1)} {T1}, {F2}{eun(F2)} {T2}",
            "x좌표가 {T1}, y좌표가 {T2}인 점은 제{n}사분면 위의 점이므로 n = {n}",
        ],
        sol2_fig=steps([
            {"text": "제{k}사분면: {SA}, {SB}", "hint": "사분면 → 부호"},
            {"text": "{F1}: {T1},  {F2}: {T2}", "hint": "곱의 부호·부호 반전", "marks": [{"on": "{T2}", "note": "제곱은 항상 양수"}]},
            {"text": "({T1}, {T2}) → 제{n}사분면"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="예를 들어 제{k}사분면의 점 ({sa}, {2*sb})를 넣어 보면 ({F1}, {F2})의 부호는 ({T1}, {T2})가 되어 제{n}사분면에 있다. 따라서 n = {n}이다.",
        sol3_fig=steps(["예: (a, b) = ({sa}, {2*sb})", "({F1}, {F2}) → ({T1}, {T2}) → 제{n}사분면"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="점 (a, b)가 제{k}사분면 위의 점이므로 {SA}, {SB}이다. 따라서 {F1}{eun(F1)} {T1}, {F2}{eun(F2)} {T2}이므로 점 ({F1}, {F2})는 제{n}사분면 위의 점이고 n = {n}이다.",
        rubric=[
            {"element": "부호 읽기", "points": 2, "criterion": "제{k}사분면에서 {SA}, {SB}임을 밝혔다.", "partial": "부호 하나가 틀렸으면 인정하지 않는다."},
            {"element": "좌표의 부호 정하기", "points": 3, "criterion": "{F1}{eun(F1)} {T1}, {F2}{eun(F2)} {T2}임을 근거와 함께 밝혔다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "부호 조합으로 제{n}사분면, n = {n}{eul(n)} 답했다.", "partial": "부호는 맞고 사분면 번호를 잘못 읽었으면 1점."},
        ],
        rubric_total=7,
    )


ORI_ROWS = {"H": {"isV": 0, "BASE": "변 BC가 x축에 평행", "AXIS": "x축", "LEN": "x좌표의 차", "HGT": "y좌표의 차"},
            "V": {"isV": 1, "BASE": "변 BC가 y축에 평행", "AXIS": "y축", "LEN": "y좌표의 차", "HGT": "x좌표의 차"}}


def co_t4():
    return tpl(CO, 4, CO_BASE,
        title="세 점을 꼭짓점으로 하는 삼각형의 넓이 — 한 변이 좌표축에 평행",
        skill="좌표축에 평행한 변을 밑변으로 잡아 길이(좌표의 차)와 높이(다른 좌표의 차)를 읽어 넓이 구하기",
        variant_axis={"밑변의 방향": "x축 평행 / y축 평행", "좌표": "−6~6"},
        discriminates="밑변의 길이와 높이를 좌표의 차(절댓값)로 읽는가, 넓이에 1/2을 곱하는가",
        difficulty=3, context="기하맥락", geometry=True,
        params=[{"name": "o", "values": {"in": list(ORI_ROWS)}}, {"name": "u", "values": {"in": [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3]}}, {"name": "d", "values": {"int": [2, 8]}},
                {"name": "h", "values": {"in": [-4, -3, -2, -1, 0, 1, 2, 3, 4]}}, {"name": "w", "values": {"in": [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]}}, {"name": "e", "values": {"in": [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]}}],
        table={"key": "o", "rows": ORI_ROWS},
        derive={"v": "u + d", "k": "h + e", "x1": "(1 - isV)*w + isV*k", "y1": "(1 - isV)*k + isV*w", "x2": "(1 - isV)*u + isV*h", "y2": "(1 - isV)*h + isV*u",
                "x3": "(1 - isV)*v + isV*h", "y3": "(1 - isV)*h + isV*v", "S": "d*abs(e)/2",
                "xlo": "min(x1, x2, x3) - 2", "xhi": "max(x1, x2, x3) + 2", "ylo": "min(y1, y2, y3) - 2", "yhi": "max(y1, y2, y3) + 2"},
        constraints=["v <= 6", "abs(k) <= 6", "(d*abs(e)) % 2 == 0", "S != d", "S != abs(e)", "not (S in (x1, y1, x2, y2, x3, y3))", "S >= 3"],
        cost_values=["x1", "y1", "x2", "y2", "x3", "y3", "d", "e", "S"],
        answer_var="S",
        verify=["2*ans == d*abs(e)", "isV == 1 or y2 == y3", "isV == 0 or x2 == x3"],
        question="세 점 A({x1}, {y1}), B({x2}, {y2}), C({x3}, {y3})을 꼭짓점으로 하는 삼각형 ABC의 넓이를 구하시오.",
        figure=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{x1}", "{y1}"]}, {"name": "B", "coord": ["{x2}", "{y2}"]}, {"name": "C", "coord": ["{x3}", "{y3}"]}],
                      [{"points": [["{x1}", "{y1}"], ["{x2}", "{y2}"], ["{x3}", "{y3}"], ["{x1}", "{y1}"]]}]),
        answer="{S}", answer_alt=[],
        sol1="두 점 B, C의 {AXIS}에 평행한 좌표가 같으므로 {BASE}하다. 이 변을 밑변으로 잡으면 밑변의 길이는 B, C의 {LEN}이고, 높이는 점 A에서 그 변까지의 거리, 곧 {HGT}이다. 좌표의 차는 큰 수에서 작은 수를 빼(절댓값) 양수로 잡는다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{x1}", "{y1}"]}, {"name": "B", "coord": ["{x2}", "{y2}"]}, {"name": "C", "coord": ["{x3}", "{y3}"]}, {"name": "H", "coord": ["{(1 - isV)*x1 + isV*x2}", "{(1 - isV)*y2 + isV*y1}"]}],
                        [{"points": [["{x1}", "{y1}"], ["{x2}", "{y2}"], ["{x3}", "{y3}"], ["{x1}", "{y1}"]]}, {"points": [["{x1}", "{y1}"], ["{(1 - isV)*x1 + isV*x2}", "{(1 - isV)*y2 + isV*y1}"]], "style": "dashed"}]),
        sol1_anim=[[hl("pt:B", "lbl:B", "pt:C", "lbl:C")], [hl("line:1", keep=True)], [hl("pt:A", "lbl:A")]],
        sol2=[
            "{BASE}하므로 밑변 BC의 길이는 {LEN} = {d}",
            "높이는 점 A와 변 BC 사이의 {HGT} = {abs(e)}",
            "따라서 (넓이) = [[frac(1,2)]] × {d} × {abs(e)} = {S}",
        ],
        sol2_fig=steps([
            {"text": "BC = {d}", "hint": "{LEN}"},
            {"text": "높이 = {abs(e)}", "hint": "{HGT}(절댓값)"},
            {"text": "[[frac(1,2)]] × {d} × {abs(e)} = {S}", "marks": [{"on": "[[frac(1,2)]]", "note": "삼각형은 절반"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="밑변 {d}, 높이 {abs(e)}인 삼각형의 넓이는 {d} × {abs(e)} ÷ 2 = {S}이다. 답: {S}",
        model_answer="{BASE}하므로 이를 밑변으로 하면 밑변의 길이는 {d}, 높이는 {abs(e)}이다. 따라서 삼각형 ABC의 넓이는 [[frac(1,2)]] × {d} × {abs(e)} = {S}이다.",
        rubric=[
            {"element": "밑변과 높이 읽기", "points": 3, "criterion": "{BASE}함을 이용해 밑변 {d}, 높이 {abs(e)}{eul(abs(e))} 좌표의 차로 구했다.", "partial": "밑변·높이 중 하나만 맞으면 1점, 좌표를 그대로 길이로 썼으면 인정하지 않는다."},
            {"element": "넓이 구하기", "points": 2, "criterion": "[[frac(1,2)]] × {d} × {abs(e)} = {S}{eul(S)} 구했다.", "partial": "[[frac(1,2)]]{eul(2)} 곱하지 않았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


AX_ROWS = {"x": {"AX": "x축", "isX": 1, "ZERO": "y좌표가 0", "ASK": "x좌표", "AXV": "y좌표"}, "y": {"AX": "y축", "isX": 0, "ZERO": "x좌표가 0", "ASK": "y좌표", "AXV": "x좌표"}}


def co_t5():
    return tpl(CO, 5, CO_BASE,
        title="좌표축 위의 점 — 다른 좌표 구하기",
        skill="x축 위의 점은 y좌표가 0, y축 위의 점은 x좌표가 0임을 이용해 a를 구하고 나머지 좌표 계산하기",
        variant_axis={"축": "x축 / y축", "계수": "±1~±4"},
        discriminates="축 위의 점의 조건(어느 좌표가 0인가)을 바르게 쓰는가, 구한 a로 묻는 좌표를 계산하는가",
        difficulty=2,
        params=[{"name": "ax", "values": {"in": list(AX_ROWS)}}, {"name": "a", "values": {"in": NZ}}, {"name": "p", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "q0", "values": {"in": NZ}},
                {"name": "r", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "s0", "values": {"in": NZ}}],
        table={"key": "ax", "rows": AX_ROWS},
        derive={"q": "isX*q0 + (1 - isX)*(-p*a)", "s": "isX*(-r*a) + (1 - isX)*s0", "xv": "p*a + q", "yv": "r*a + s", "ans": "isX*(p*a + q) + (1 - isX)*(r*a + s)",
                "zc": "isX*r + (1 - isX)*p", "zk": "isX*s + (1 - isX)*q", "ac": "isX*p + (1 - isX)*r", "ak": "isX*q + (1 - isX)*s"},
        constraints=["ans != 0", "ans != a", "ans != q", "ans != s", "ans != p", "ans != r", "q != 0", "s != 0"],
        cost_values=["p", "q", "r", "s", "a", "ans"],
        answer_var="ans",
        verify=["isX == 0 or r*a + s == 0", "isX == 1 or p*a + q == 0", "ans == isX*(p*a + q) + (1 - isX)*(r*a + s)"],
        question="점 ({co(p)}a {sgn(q)}, {co(r)}a {sgn(s)}){ika(s)} {AX} 위의 점일 때, 이 점의 {ASK}{eul(ASK)} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{AX} 위의 점은 {ZERO}이다. 그러므로 {AXV}인 식을 0으로 놓아 a를 구한 다음, 그 a를 다른 좌표의 식에 대입하면 묻는 {ASK}{ika(ASK)} 나온다.",
        sol2=[
            "{AX} 위의 점은 {ZERO}이므로 {co(zc)}a {sgn(zk)} = 0",
            "이를 풀면 a = {a}",
            "따라서 {ASK}{eun(ASK)} {ac} × {pn(a)} {sgn(ak)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(zc)}a {sgn(zk)} = 0", "hint": "{AX} 위 → {ZERO}"},
            {"text": "a = {a}"},
            {"text": "{ASK} = {ac} × {pn(a)} {sgn(ak)} = {ans}", "marks": [{"on": "{ans}", "note": "a가 아니라 좌표를 답한다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol3="a = {a}{eul(a)} 넣으면 점의 좌표는 ({xv}, {yv})이고 {ZERO}이므로 {AX} 위의 점이 맞다. 따라서 {ASK}{eun(ASK)} {ans}이다.",
        sol3_fig=steps(["a = {a}: ({xv}, {yv})", "{ZERO} → {AX} 위의 점  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{AX} 위의 점은 {ZERO}이므로 {co(zc)}a {sgn(zk)} = 0에서 a = {a}이다. 따라서 이 점의 {ASK}{eun(ASK)} {ac} × {pn(a)} {sgn(ak)} = {ans}이다.",
        rubric=[
            {"element": "축 위의 점의 조건", "points": 3, "criterion": "{AX} 위의 점은 {ZERO}임을 써서 {co(zc)}a {sgn(zk)} = 0{eul(0)} 세웠다.", "partial": "다른 좌표를 0으로 놓았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a = {a}{eul(a)} 구해 {ASK} {ans}{eul(ans)} 답했다.", "partial": "a의 값을 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


CO_SEED = {
    "seed_id": CO, "category": "연산",
    "title": "좌표평면 — 순서쌍 같음·대칭점·사분면 판정·좌표 삼각형 넓이·축 위의 점",
    "unit_id": "m1-1", "concept_ids": ["m1-1-29", "m1-1-30"],
    "schema_id": None, "schema_name": "순서쌍과 좌표평면·사분면",
    "source_item_ids": [],
    "note": "구조만 차용. 사분면 판정은 부호가 정해지는 식만 표로 굽고, 답이 문면의 사분면 번호와 같은 행은 뺀다(R-05). 삼각형 넓이는 한 변을 축에 평행하게 둔다.",
    "geometry": False,
    "templates": [co_t1(), co_t2(), co_t3(), co_t4(), co_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 정비례·반비례
PR = "m1-1-proportion"
PR_BASE = {**BASE, "prereq": ["정비례", "반비례", "좌표평면"], "ops": ["비례", "대입"], "tags": ["정비례", "반비례"]}


def line_through_origin(xl, yl):
    """y = a x 를 틀 안에서 자른 선분의 두 끝점 (xs, ys)-(xe, ye). a 는 env 의 'a'."""
    return {"xlo": f"min({xl}) - 2", "xhi": f"max({xl}) + 2", "ylo": f"min({yl}) - 2", "yhi": f"max({yl}) + 2",
            "xs": "max(xlo, min(ylo/a, yhi/a))", "xe": "min(xhi, max(ylo/a, yhi/a))", "ys": "a*xs", "ye": "a*xe"}


def pr_t1():
    return tpl(PR, 1, PR_BASE,
        title="정비례 관계 — 한 쌍의 값으로 다른 x에서의 y 구하기",
        skill="y = ax로 놓고 주어진 x, y를 대입해 a를 구한 뒤 다른 x에서의 y를 구하기",
        variant_axis={"비례상수": "±1/3~±6", "x": "−18~18"},
        discriminates="정비례를 y = ax로 나타내고 a를 먼저 구하는가 (x, y를 직접 비례식으로 다룰 때 방향을 지키는가)",
        difficulty=2,
        params=[{"name": "pa", "values": {"in": NZ}}, {"name": "qd", "values": {"in": [1, 2, 3]}}, {"name": "m1", "values": {"in": NZ}}, {"name": "m2", "values": {"in": NZ}}],
        derive={"a": "pa/qd", "x1": "qd*m1", "x2": "qd*m2", "y1": "pa*m1", "y2": "pa*m2", **line_through_origin("x1, x2, 0", "y1, y2, 0")},
        constraints=["gcd(pa, qd) == 1", "m1 != m2", "y2 != x1", "y2 != y1", "y2 != x2", "y1 != x1", "abs(y2) <= 30", "abs(x1) <= 18", "abs(x2) <= 18"],
        cost_values=["x1", "y1", "x2", "a", "y2"],
        answer_var="y2",
        verify=["y1*x2 == ans*x1", "ans == a*x2"],
        question="y가 x에 정비례하고, x = {x1}일 때 y = {y1}이다. x = {x2}일 때 y의 값을 구하시오.",
        answer="{y2}", answer_alt=[],
        sol1="y가 x에 정비례하면 y = ax (a ≠ 0) 꼴이다. x = {x1}, y = {y1}{eul(y1)} 대입하면 a가 정해지고, 그 식에 x = {x2}를 넣으면 y의 값이 나온다. 그래프는 원점을 지나는 직선이다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{x1}", "{y1}"]}, {"name": "Q", "coord": ["{x2}", "{y2}"]}], [{"points": [["{xs}", "{ys}"], ["{xe}", "{ye}"]]}]),
        sol1_anim=[[hl("pt:P", "lbl:P")], [hl("line:0", keep=True)], [hl("pt:Q", "lbl:Q")]],
        sol2=[
            "y가 x에 정비례하므로 y = ax로 놓는다.",
            "x = {x1}, y = {y1}{eul(y1)} 대입하면 {y1} = {pn(x1)}a, a = {a}",
            "따라서 y = {co(a)}x이고, x = {x2}를 대입하면 y = {a} × {pn(x2)} = {y2}",
        ],
        sol2_fig=steps([
            {"text": "y = ax", "hint": "정비례"},
            {"text": "{y1} = a × {pn(x1)}  →  a = {a}", "hint": "(x, y) = ({x1}, {y1}) 대입"},
            {"text": "y = {co(a)}x  →  x = {x2}: y = {y2}", "marks": [{"on": "{y2}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="정비례에서는 x가 몇 배가 되면 y도 그만큼 몇 배가 된다. x가 {x1}에서 {x2}로 [[frac({x2},{x1})]]배가 되었으므로 y도 {y1} × [[frac({x2},{x1})]] = {y2}{ika(y2)} 되어 같은 값이다. 답은 {y2}이다.",
        sol3_fig=steps(["x: {x1} → {x2}  ([[frac({x2},{x1})]]배)", "y: {y1} × [[frac({x2},{x1})]] = {y2}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = ax에 x = {x1}, y = {y1}{eul(y1)} 대입하면 a = {a}이므로 y = {co(a)}x이다. 따라서 x = {x2}일 때 y = {y2}이다.",
        rubric=[
            {"element": "관계식 세우기", "points": 3, "criterion": "y = ax로 놓고 (x, y) = ({x1}, {y1}){eul(y1)} 대입해 a = {a}{eul(a)} 구했다.", "partial": "y = a/x로 놓았으면 인정하지 않고, 대입 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "y = {co(a)}x에 x = {x2}를 대입해 y = {y2}{eul(y2)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def pr_t2():
    return tpl(PR, 2, PR_BASE,
        title="반비례 관계 — 한 쌍의 값으로 다른 x에서의 y 구하기",
        skill="y = a/x로 놓고 a = xy가 일정함을 이용해 다른 x에서의 y를 구하기",
        variant_axis={"xy의 값": "±2~±36", "x": "−6~6"},
        discriminates="반비례를 y = a/x(xy = a)로 나타내는가 (정비례처럼 y = ax로 놓지 않는가)",
        difficulty=2,
        params=[{"name": "x1", "values": {"in": NZ}}, {"name": "y1", "values": {"in": NZ}}, {"name": "x2", "values": {"in": NZ}}],
        derive={"k": "x1*y1", "y2": "x1*y1/x2"},
        constraints=["k % x2 == 0", "x2 != x1", "y2 != y1", "y2 != x1", "y2 != x2", "abs(k) >= 2", "x1 != y1"],
        cost_values=["x1", "y1", "x2", "k", "y2"],
        answer_var="y2",
        verify=["x2*ans == x1*y1", "ans == k/x2"],
        question="y가 x에 반비례하고, x = {x1}일 때 y = {y1}이다. x = {x2}일 때 y의 값을 구하시오.",
        answer="{y2}", answer_alt=[],
        sol1="y가 x에 반비례하면 y = [[frac(a,x)]] (a ≠ 0) 꼴이고, 이는 xy = a로 두 값의 곱이 항상 일정하다는 뜻이다. x = {x1}, y = {y1}{eul(y1)} 대입해 a를 구한 뒤 x = {x2}를 넣는다.",
        sol2=[
            "y가 x에 반비례하므로 y = [[frac(a,x)]]로 놓는다.",
            "x = {x1}, y = {y1}{eul(y1)} 대입하면 {y1} = [[frac(a,{x1})]], a = {x1} × {pn(y1)} = {k}",
            "따라서 y = [[frac({k},x)]]이고, x = {x2}를 대입하면 y = [[frac({k},{x2})]] = {y2}",
        ],
        sol2_fig=steps([
            {"text": "y = [[frac(a,x)]],  즉 xy = a", "hint": "반비례: 곱이 일정"},
            {"text": "a = {x1} × {pn(y1)} = {k}", "hint": "(x, y) = ({x1}, {y1}) 대입"},
            {"text": "y = {k} ÷ {pn(x2)} = {y2}", "marks": [{"on": "{y2}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="반비례에서는 xy가 일정하다. {x1} × {pn(y1)} = {k}, {x2} × {pn(y2)} = {k}{ro(k)} 곱이 같으므로 y = {y2}{ika(y2)} 맞다. 답은 {y2}이다.",
        sol3_fig=steps(["{x1} × {pn(y1)} = {k}", "{x2} × {pn(y2)} = {k}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = [[frac(a,x)]]에 x = {x1}, y = {y1}{eul(y1)} 대입하면 a = {k}이므로 y = [[frac({k},x)]]이다. 따라서 x = {x2}일 때 y = {y2}이다.",
        rubric=[
            {"element": "관계식 세우기", "points": 3, "criterion": "y = [[frac(a,x)]]로 놓고 (x, y) = ({x1}, {y1}){eul(y1)} 대입해 a = {k}{eul(k)} 구했다.", "partial": "y = ax로 놓았으면 인정하지 않고, 대입 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "y = [[frac({k},x)]]에 x = {x2}를 대입해 y = {y2}{eul(y2)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


REL_ROWS = {"p": {"REL": "정비례", "FORM": "ax", "isP": 1, "EQ": "y = ax", "AEQ": "a = y ÷ x", "SL": "a ×", "SLV": "×", "F1": "", "F2": "x", "S1": "", "S2": "k"},
            "i": {"REL": "반비례", "FORM": "[[frac(a,x)]]", "isP": 0, "EQ": "y = [[frac(a,x)]]", "AEQ": "a = xy", "SL": "a ÷", "SLV": "÷", "F1": "[[frac(", "F2": ",x)]]", "S1": "[[frac(", "S2": ",k)]]"}}


def pr_t3():
    return tpl(PR, 3, PR_BASE,
        title="그래프가 한 점을 지날 때 상수 a — 정비례 y = ax·반비례 y = a/x",
        skill="그래프 위의 점의 좌표는 관계식을 만족하므로 대입하여 a 구하기",
        variant_axis={"관계": "정비례 / 반비례", "점": "−6~6"},
        discriminates="그래프 위의 점을 관계식에 대입하는가, 정비례(a = y/x)와 반비례(a = xy)의 계산을 구별하는가",
        difficulty=2,
        params=[{"name": "rel", "values": {"in": list(REL_ROWS)}}, {"name": "p", "values": {"in": NZ2}}, {"name": "w", "values": {"in": NZ}}],
        table={"key": "rel", "rows": REL_ROWS},
        derive={"q": "isP*(w*p) + (1 - isP)*w", "ans": "isP*w + (1 - isP)*(p*w)"},
        constraints=["ans != p", "ans != q", "ans != 0", "p != q", "abs(ans) != 1"],
        cost_values=["p", "q", "ans"],
        answer_var="ans",
        verify=["isP == 0 or ans*p == q", "isP == 1 or ans == p*q"],
        question="{REL} 관계 y = {FORM}의 그래프가 점 ({p}, {q}){eul(q)} 지날 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="그래프가 점 ({p}, {q}){eul(q)} 지난다는 것은 x = {p}, y = {q}{eul(q)} 관계식에 대입하면 등식이 성립한다는 뜻이다. {EQ}에 대입해 a에 대한 식을 풀면 된다({AEQ}).",
        sol2=[
            "그래프가 점 ({p}, {q}){eul(q)} 지나므로 {EQ}에 x = {p}, y = {q}{eul(q)} 대입할 수 있다.",
            "대입하면 {q} = {SL} {pn(p)}",
            "따라서 a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{EQ}에 ({p}, {q}) 대입", "hint": "그래프 위의 점 = 식을 만족"},
            {"text": "{q} = {SL} {pn(p)}", "hint": "{AEQ}"},
            {"text": "a = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="a = {ans}이면 x = {p}일 때 y = {ans} {SLV} {pn(p)} = {q}{ika(q)} 되어 그래프가 점 ({p}, {q}){eul(q)} 지난다. 답은 {ans}이다.",
        sol3_fig=steps(["x = {p}: {ans} {SLV} {pn(p)} = {q}  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{EQ}에 x = {p}, y = {q}{eul(q)} 대입하면 {q} = {SL} {pn(p)}이므로 a = {ans}이다.",
        rubric=[
            {"element": "점의 좌표 대입", "points": 3, "criterion": "{EQ}에 x = {p}, y = {q}{eul(q)} 대입해 {q} = {SL} {pn(p)}{eul(p)} 얻었다.", "partial": "x와 y를 바꿔 대입했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a = {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def pr_t4():
    return tpl(PR, 4, PR_BASE,
        title="그래프가 두 점을 지날 때 — 한 점으로 a를 구하고 다른 점의 미지수 k 구하기",
        skill="좌표가 모두 주어진 점으로 a를 구한 뒤, 다른 점의 좌표를 대입해 k 구하기",
        variant_axis={"관계": "정비례 / 반비례", "점": "−6~6"},
        discriminates="어느 점으로 먼저 a를 구할지 판단하고, 구한 식에 남은 점을 대입하는가",
        difficulty=3,
        params=[{"name": "rel", "values": {"in": list(REL_ROWS)}}, {"name": "a0", "values": {"in": NZ}}, {"name": "p", "values": {"in": NZ2}}, {"name": "q0", "values": {"in": NZ}}, {"name": "m", "values": {"in": NZ}}],
        table={"key": "rel", "rows": REL_ROWS},
        derive={"q": "isP*(a0*p) + (1 - isP)*q0", "a": "isP*a0 + (1 - isP)*(p*q0)", "r": "isP*(a0*m) + (1 - isP)*(p*q0/m)", "k": "m"},
        constraints=["isP == 1 or (p*q0) % m == 0", "m != p", "k != q", "k != r", "r != q", "r != p", "abs(a) != 1", "abs(r) <= 36", "p != q"],
        cost_values=["p", "q", "r", "a", "k"],
        answer_var="k",
        verify=["isP == 0 or (a*p == q and a*ans == r)", "isP == 1 or (a == p*q and ans*r == a)"],
        question="{REL} 관계 y = {FORM}의 그래프가 두 점 ({p}, {q}), (k, {r})를 지날 때, k의 값을 구하시오.",
        answer="{k}", answer_alt=[],
        sol1="두 점 모두 그래프 위의 점이므로 관계식을 만족한다. 좌표가 모두 알려진 점 ({p}, {q})를 먼저 대입해 a를 구하고, 완성된 식에 점 (k, {r})를 대입해 k를 구한다.",
        sol2=[
            "점 ({p}, {q}){eul(q)} {EQ}에 대입하면 {q} = {SL} {pn(p)}, a = {a}",
            "따라서 관계식은 y = {F1}{a}{F2}",
            "점 (k, {r})를 대입하면 {r} = {S1}{a}{S2}, k = {k}",
        ],
        sol2_fig=steps([
            {"text": "{q} = {SL} {pn(p)}  →  a = {a}", "hint": "좌표를 모두 아는 점부터"},
            {"text": "y = {F1}{a}{F2}", "hint": "관계식 완성"},
            {"text": "{r} = {S1}{a}{S2}  →  k = {k}", "hint": "(k, {r}) 대입", "marks": [{"on": "{k}", "note": "k는 x좌표"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="y = {F1}{a}{F2}에 x = {k}를 대입하면 y = {r}{ika(r)} 되어 점 ({k}, {r})를 지난다. 답은 {k}이다.",
        sol3_fig=steps(["y = {F1}{a}{F2},  x = {k} → y = {r}  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="점 ({p}, {q}){eul(q)} {EQ}에 대입하면 a = {a}이므로 y = {F1}{a}{F2}이다. 점 (k, {r})를 대입하면 {r} = {S1}{a}{S2}이므로 k = {k}이다.",
        rubric=[
            {"element": "a 구하기", "points": 3, "criterion": "점 ({p}, {q}){eul(q)} 대입해 a = {a}{eul(a)} 구하고 관계식 y = {F1}{a}{F2}{eul(2)} 완성했다.", "partial": "대입 실수면 1점."},
            {"element": "k 구하기", "points": 2, "criterion": "점 (k, {r})를 대입해 k = {k}{eul(k)} 구했다.", "partial": "x, y를 바꿔 대입했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def pr_t5():
    return tpl(PR, 5, PR_BASE,
        title="정비례 그래프 위의 점과 x축이 만드는 삼각형의 넓이",
        skill="그래프 위의 점 A(p, ap)에서 x축에 내린 수선의 발 B로 직각삼각형 OAB를 만들고 넓이 = OB × AB ÷ 2 구하기",
        variant_axis={"비례상수": "±1~±5", "A의 x좌표": "±2~±8"},
        discriminates="A의 y좌표를 관계식으로 구하는가, 밑변·높이를 좌표의 절댓값으로 잡는가",
        difficulty=3, context="기하맥락", geometry=True,
        params=[{"name": "a", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "p", "values": {"in": [-10, -9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9, 10]}}],
        derive={"ay": "a*p", "S": "abs(a)*p*p/2", **line_through_origin("p, 0", "a*p, 0")},
        constraints=["(abs(a)*p*p) % 2 == 0", "S != abs(p)", "S != abs(a*p)", "S != a", "S != p", "abs(a*p) <= 30"],
        cost_values=["a", "p", "ay", "S"],
        answer_var="S",
        verify=["2*ans == abs(p)*abs(a*p)"],
        question="정비례 관계 y = {co(a)}x의 그래프 위의 점 A의 x좌표가 {p}이다. 점 A에서 x축에 내린 수선의 발을 B라 할 때, 삼각형 OAB의 넓이를 구하시오. (단, O는 원점)",
        figure=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{p}", "{ay}"]}, {"name": "B", "coord": ["{p}", 0]}],
                      [{"points": [["{xs}", "{ys}"], ["{xe}", "{ye}"]]}, {"points": [["{p}", "{ay}"], ["{p}", 0]], "style": "dashed"}]),
        answer="{S}", answer_alt=[],
        sol1="점 A는 y = {co(a)}x 위의 점이므로 x = {p}를 대입하면 y = {ay}, 곧 A({p}, {ay})이다. B는 A에서 x축에 내린 수선의 발이므로 B({p}, 0)이고, 삼각형 OAB는 ∠B = 90°인 직각삼각형이다. 밑변 OB = |{p}| = {abs(p)}, 높이 AB = |{ay}| = {abs(ay)}{ro(abs(ay))} 넓이를 구한다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{p}", "{ay}"]}, {"name": "B", "coord": ["{p}", 0]}],
                        [{"points": [["{xs}", "{ys}"], ["{xe}", "{ye}"]]}, {"points": [[0, 0], ["{p}", "{ay}"], ["{p}", 0], [0, 0]]}]),
        sol1_anim=[[hl("pt:A", "lbl:A")], [hl("pt:B", "lbl:B")], [hl("line:1", keep=True)]],
        sol2=[
            "A의 y좌표: y = {a} × {pn(p)} = {ay}이므로 A({p}, {ay}), B({p}, 0)",
            "OB = {abs(p)}, AB = {abs(ay)}",
            "(삼각형 OAB의 넓이) = [[frac(1,2)]] × {abs(p)} × {abs(ay)} = {S}",
        ],
        sol2_fig=steps([
            {"text": "A({p}, {ay}),  B({p}, 0)", "hint": "x = {p} 대입"},
            {"text": "OB = {abs(p)},  AB = {abs(ay)}", "hint": "길이는 절댓값"},
            {"text": "[[frac(1,2)]] × {abs(p)} × {abs(ay)} = {S}", "marks": [{"on": "[[frac(1,2)]]", "note": "직각삼각형"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="밑변 {abs(p)}, 높이 {abs(ay)}인 직각삼각형의 넓이는 {abs(p)} × {abs(ay)} ÷ 2 = {S}이다. 답: {S}",
        model_answer="점 A의 y좌표는 {a} × {pn(p)} = {ay}이므로 A({p}, {ay}), B({p}, 0)이다. OB = {abs(p)}, AB = {abs(ay)}이므로 삼각형 OAB의 넓이는 [[frac(1,2)]] × {abs(p)} × {abs(ay)} = {S}이다.",
        rubric=[
            {"element": "점 A의 좌표", "points": 3, "criterion": "y = {co(a)}x에 x = {p}를 대입해 A({p}, {ay})와 B({p}, 0)을 구했다.", "partial": "A의 y좌표 계산 실수면 1점."},
            {"element": "넓이 구하기", "points": 2, "criterion": "OB = {abs(p)}, AB = {abs(ay)}{ro(abs(ay))} 넓이 {S}{eul(S)} 구했다.", "partial": "길이를 음수로 두어 넓이가 음수이면 1점, [[frac(1,2)]]{eul(2)} 곱하지 않았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


QD_ROWS = {"q2": {"sx": -1, "sy": 1, "QN": "2"}, "q4": {"sx": 1, "sy": -1, "QN": "4"}}


def _k_rows():
    rows = {}
    for n in range(4, 73):
        divs = [d for d in range(2, n) if n % d == 0 and d <= n // d and d != n // d]
        if not divs:
            continue
        u = divs[len(divs) // 2]
        rows[str(n)] = {"n": n, "u": u, "v": n // u}
    return rows


K_ROWS = _k_rows()


def pr_t6(no, kind):
    tri = kind == "tri"
    t = tpl(PR, no, PR_BASE,
        title="반비례 그래프 위의 점과 두 좌표축이 만드는 " + ("삼각형" if tri else "직사각형") + "의 넓이",
        skill="y = k/x 위의 점 P(x, y)에서 두 축에 내린 수선으로 만든 직사각형의 넓이가 |xy| = |k|임을 이용하기",
        variant_axis={"k": "−4~−72", "사분면": "2 / 4"},
        discriminates="직사각형의 가로·세로가 P의 좌표의 절댓값임을 알고 xy = k로 넓이를 구하는가",
        difficulty=3, context="기하맥락", geometry=True,
        params=[{"name": "qd", "values": {"in": list(QD_ROWS)}}, {"name": "kk", "values": {"in": list(K_ROWS)}}],
        table=[{"key": "qd", "rows": QD_ROWS}, {"key": "kk", "rows": K_ROWS}],
        derive={"half": "1" if tri else "0", "k": "-n", "px": "sx*u", "py": "sy*v", "S": "n/(1 + half)", "xlo": "min(px, 0) - 2", "xhi": "max(px, 0) + 2", "ylo": "min(py, 0) - 2", "yhi": "max(py, 0) + 2"},
        constraints=["half == 0 or n % 2 == 0", "S != u", "S != v", "S != 2", "S != 4"],
        cost_values=["k", "S", "half"],
        answer_var="S",
        verify=["ans*(1 + half) == abs(k)", "px*py == k"],
        question="반비례 관계 y = [[frac({k},x)]]의 그래프 위의 제{QN}사분면의 한 점 P에서 x축, y축에 각각 내린 수선의 발을 A, B라 할 때, {ASKW} 구하시오. (단, O는 원점)",
        figure=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{px}", "{py}"]}, {"name": "A", "coord": ["{px}", 0]}, {"name": "B", "coord": [0, "{py}"]}],
                      [{"points": [["{px}", "{py}"], ["{px}", 0]], "style": "dashed"}, {"points": [["{px}", "{py}"], [0, "{py}"]], "style": "dashed"}]),
        answer="{S}", answer_alt=[],
        sol1="점 P의 좌표를 (p, q)라 하면 A(p, 0), B(0, q)이므로 직사각형 OAPB의 가로는 |p|, 세로는 |q|이다. 따라서 직사각형의 넓이는 |p| × |q| = |pq|인데, P가 y = [[frac({k},x)]] 위의 점이므로 pq = {k}이다. 곧 P를 어디에 잡아도 직사각형의 넓이는 |{k}| = {n}{ro(n)} 일정하다." + (" 삼각형 OAP는 이 직사각형을 대각선 OP로 나눈 절반이므로 넓이는 {n} ÷ 2 = {S}이다." if tri else ""),
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{px}", "{py}"]}, {"name": "A", "coord": ["{px}", 0]}, {"name": "B", "coord": [0, "{py}"]}],
                        [{"points": [[0, 0], ["{px}", 0], ["{px}", "{py}"], [0, "{py}"], [0, 0]]}]),
        sol1_anim=[[hl("pt:P", "lbl:P")], [hl("line:0", keep=True)], [hl("pt:A", "lbl:A", "pt:B", "lbl:B")]],
        sol2=[
            "P(p, q)라 하면 y = [[frac({k},x)]] 위의 점이므로 q = [[frac({k},p)]], 곧 pq = {k}",
            "직사각형 OAPB의 가로 OA = |p|, 세로 OB = |q|",
            "(직사각형 OAPB의 넓이) = |p| × |q| = |pq| = |{k}| = {n}",
        ] + (["삼각형 OAP는 직사각형 OAPB의 절반이므로 넓이는 {n} ÷ 2 = {S}"] if tri else []),
        sol2_fig=steps([
            {"text": "pq = {k}", "hint": "그래프 위의 점: xy = k"},
            {"text": "OA = |p|,  OB = |q|", "hint": "길이는 절댓값"},
            {"text": "|p| × |q| = |{k}| = {n}", "marks": [{"on": "{n}", "note": "넓이는 양수"}]},
        ] + ([{"text": "삼각형 OAP = {n} ÷ 2 = {S}", "hint": "대각선이 직사각형을 반으로"}] if tri else [])),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]] + ([[reveal(3), hl("hint:3")]] if tri else []),
        sol_check="예를 들어 P({px}, {py})를 잡으면 가로 {u}, 세로 {v}이고 직사각형의 넓이는 {u} × {v} = {n}" + (", 삼각형 OAP의 넓이는 {n} ÷ 2 = {S}" if tri else "") + "이다. 답: {S}",
        model_answer="P(p, q)라 하면 pq = {k}이고 직사각형 OAPB의 가로와 세로는 |p|, |q|이다. 따라서 직사각형의 넓이는 |p| × |q| = |pq| = |{k}| = {n}이다." + (" 삼각형 OAP는 그 절반이므로 넓이는 {n} ÷ 2 = {S}이다." if tri else ""),
        rubric=[
            {"element": "좌표와 넓이의 관계", "points": 3, "criterion": "P(p, q)로 놓아 가로 |p|, 세로 |q|이고 pq = {k}임을 밝혔다.", "partial": "pq = {k}{eul(k)} 쓰지 않고 특정 점만 잡아 계산했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": ("직사각형의 넓이 {n}의 절반 {S}{eul(S)} 삼각형의 넓이로 답했다." if tri else "넓이 |{k}| = {S}{eul(S)} 구했다."), "partial": "넓이를 음수로 답했으면 인정하지 않고, 직사각형과 삼각형을 혼동했으면 1점."},
        ],
        rubric_total=5,
    )
    from seedlib import sub_all
    return sub_all(t, {"{ASKW}": "삼각형 OAP의 넓이를" if tri else "직사각형 OAPB의 넓이를"})


PR_SEED = {
    "seed_id": PR, "category": "연산",
    "title": "정비례·반비례 — 한 쌍의 값·그래프 위의 점·두 점·삼각형 넓이·직사각형 넓이",
    "unit_id": "m1-1", "concept_ids": ["m1-1-32", "m1-1-33", "m1-1-34"],
    "schema_id": None, "schema_name": "정비례와 반비례의 관계식과 그래프",
    "source_item_ids": [],
    "note": "구조만 차용. 정비례 그래프는 원점을 지나는 선분(틀 안에서 자름)으로 그리고 반비례 곡선은 그리지 않는다. 직사각형 넓이 틀은 k < 0 으로 두어 답 |k| 이 문면에 노출되지 않게 한다.",
    "geometry": False,
    "templates": [pr_t1(), pr_t2(), pr_t3(), pr_t4(), pr_t5(), pr_t6(6, "rect"), pr_t6(7, "tri")],
}


if __name__ == "__main__":
    for seed in (CO_SEED, PR_SEED):
        with_pitfalls(seed)
        dump(seed)
