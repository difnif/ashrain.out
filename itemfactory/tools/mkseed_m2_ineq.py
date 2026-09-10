# itemfactory/tools/mkseed_m2_ineq.py — 일차부등식 시드 생성기: 풀이(연산) · 유리한 선택(활용) (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_ineq.py
#     → seeds/m2-1-ineq-solve.json (4틀) · seeds/m2-1-ineq-choice.json (4틀)
#
# 풀이 틀의 답은 'x > 3' 같은 부등식 문자열(answer_type 식). 독립 검산은 recheck.check_ineq 가 발문의 양변을 mathir.ev 로 대입해 확인한다.
# 부호·방향 조합(os)은 표로: OP(원래 부등호) · ps(a−c의 부호; sgn 은 조사 도우미 이름이라 피함) → FOP(최종 부등호) · fd(해의 방향 ±1) · flip(방향 바뀜 여부).
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, numline, reveal, steps, table, with_pitfalls  # noqa: E402

SCHEMA_SOLVE = "e0dabf6c-362c-4f6e-bdce-527bc0f317e4"     # 일차부등식의 풀이
SCHEMA_CHOICE = "88fcccc5-68a4-4d24-bde7-15fb7990f2ab"    # 두 선택지 비용 비교 → 유리한 조건 찾기

OPS = {"gt": (">", 1, 1), "ge": ("≥", 1, 0), "lt": ("<", -1, 1), "le": ("≤", -1, 0)}   # 기호, sg(좌변이 큰 쪽이면 +1), strict
REV = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}


def os_rows():
    rows = {}
    for code, (sym, sg, strict) in OPS.items():
        for ps in (1, -1):
            fop = sym if ps == 1 else REV[sym]
            fd = 1 if fop in (">", "≥") else -1
            rows[f"{code}{'p' if ps == 1 else 'n'}"] = {
                "OP": sym, "FOP": fop, "sg": sg, "ps": ps, "fd": fd, "strict": strict, "flip": 0 if ps == 1 else 1,
                "FLIP": "" if ps == 1 else " — 음수로 나누므로 부등호의 방향이 바뀐다",
                "INC": "포함하지 않는다" if strict else "포함한다",
                "DIR": "오른쪽" if fd == 1 else "왼쪽",
            }
    return rows


OS_ROWS = os_rows()
OS_PARAM = {"name": "os", "values": {"in": list(OS_ROWS)}}
OS_TABLE = {"key": "os", "rows": OS_ROWS}

SOLVE = {"process": "절차수행", "context": "무맥락", "prereq": ["일차방정식의 풀이", "부등식의 성질"], "ops": ["부등식", "사칙"], "traps": ["부호", "역연산"],
         "time_limit": 70, "points": 4, "tags": ["일차부등식", "부등식의 풀이"]}


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def numfig(strict_key="strict"):
    """해를 수직선에: 경계점 x0 + 해의 방향으로 뻗는 반직선 — 구간의 먼 끝을 축 범위(±4) 밖(±5.4)에 두어 렌더러가 끝점 원을 그리지 못하게(잘리게) 한다."""
    return [{"fn": "numline", "args": {"min": "{x0 - 4}", "max": "{x0 + 4}", "points": [{"x": "{x0}", "label": "{x0}"}],
                                        "segments": [{"start": "{min(x0, x0 + 5.4*fd)}", "end": "{max(x0, x0 + 5.4*fd)}", "inclusive": "{strict == 0}"}]}}]


# ═══════════════════════════════════════════════════════════════════ 1. 일차부등식의 풀이
def solve_t1():
    return tpl("m2-1-ineq-solve", 1, SOLVE,
        title="ax + b ▷ cx + d 꼴의 일차부등식 풀기",
        skill="이항해 x항과 상수항을 모으고, x의 계수로 나눌 때 음수이면 부등호의 방향을 바꾸기",
        variant_axis={"부등호": "> ≥ < ≤", "계수 부호": "x의 계수가 양수/음수가 됨", "해의 형태": "정수 경계"},
        discriminates="음수로 나눌 때 부등호의 방향을 바꾸는가, 이항할 때 부호를 바꾸는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[OS_PARAM, {"name": "a", "values": {"int": [2, 6]}}, {"name": "k", "values": {"in": [1, 2, 3]}}, {"name": "b", "values": {"in": [-8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8]}}, {"name": "x0", "values": {"int": [-5, 5]}}],
        table=OS_TABLE,
        derive={"c": "a - ps*k", "d": "b + ps*k*x0", "m": "ps*k", "r": "ps*k*x0"},
        constraints=["c >= 1", "d != 0", "x0 != 0", "c != a", "abs(d) <= 30", "ps < 0 or k >= 2"],
        cost_values=["a", "b", "c", "d", "m", "r", "x0"],
        verify=["a*x0 + b == c*x0 + d", "sg*(a - c)*fd > 0", "m == a - c", "r == d - b"],
        question="일차부등식 {a}x {sgn(b)} {OP} {co(c)}x {sgn(d)}{eul(d)} 푸시오.",
        answer="x {FOP} {x0}", answer_alt=[],
        sol1="일차방정식을 풀 때처럼 x가 있는 항은 좌변으로, 상수항은 우변으로 이항한다(넘기면 부호가 바뀐다). 마지막에 x의 계수로 양변을 나누는데, 그 계수가 음수이면 부등호의 방향이 바뀐다 — 부등식에서 방정식과 다른 점은 이것 하나뿐이다. 해는 수직선에 경계점과 방향으로 나타낸다.",
        sol1_fig=steps(["{a}x {sgn(b)} {OP} {co(c)}x {sgn(d)}", "{a}x − {co(c)}x {OP} {d} − {pn(b)}", "{co(m)}x {OP} {r}", "x {FOP} {x0}{FLIP}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)], [reveal(3)]],
        sol2=[
            "x가 있는 항은 좌변으로, 상수항은 우변으로 이항한다: {a}x − {co(c)}x {OP} {d} − {pn(b)}",
            "동류항을 정리하면 {co(m)}x {OP} {r}",
            "양변을 x의 계수 {m}{ro(m)} 나누면 x {FOP} {x0}{FLIP}",
        ],
        sol2_fig=steps([
            {"text": "{a}x − {co(c)}x {OP} {d} − {pn(b)}", "hint": "이항 — 부호가 바뀐다"},
            {"text": "{co(m)}x {OP} {r}", "hint": "동류항 정리"},
            {"text": "x {FOP} {x0}", "hint": "양변 ÷ {pn(m)}{FLIP}", "marks": [{"on": "{x0}", "note": "{r} ÷ {pn(m)} = {x0}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="경계 x = {x0}{eul(x0)} 원래 부등식에 넣으면 양변이 {a*x0 + b}{ro(a*x0 + b)} 같아진다(경계는 {INC}). 경계보다 {DIR}의 수 x = {x0 + fd}{eul(x0 + fd)} 넣으면 좌변 {a*(x0 + fd) + b}, 우변 {c*(x0 + fd) + d}{ro(c*(x0 + fd) + d)} 부등식이 성립하므로 해의 방향이 맞다. 답은 x {FOP} {x0}이다.",
        sol3_fig=numfig(),
        sol3_anim=[[hl("pt:{x0}", "lbl:{x0}")], [hl("seg:0", keep=True)]],
        model_answer="{a}x {sgn(b)} {OP} {co(c)}x {sgn(d)}에서 x항과 상수항을 이항하면 {a}x − {co(c)}x {OP} {d} − {pn(b)}, 곧 {co(m)}x {OP} {r}이다. 양변을 {m}{ro(m)} 나누면{FLIP} x {FOP} {x0}이다.",
        rubric=[
            {"element": "이항·정리", "points": 2, "criterion": "x항과 상수항을 이항해 {co(m)}x {OP} {r}{ro(r)} 정리했다.", "partial": "이항의 부호 실수가 있으면 1점."},
            {"element": "계수로 나누기", "points": 3, "criterion": "양변을 {m}{ro(m)} 나누어 x {FOP} {x0}{eul(x0)} 얻었다(음수이면 방향을 바꾸었다).", "partial": "음수로 나누며 방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "해 나타내기", "points": 2, "criterion": "해를 x {FOP} {x0}{ro(x0)} 쓰고(또는 수직선에 나타내고) 경계값이 {INC}는 것을 바르게 표시했다.", "partial": "경계 포함 여부(등호)가 틀렸으면 1점."},
        ],
    )


def solve_t2():
    return tpl("m2-1-ineq-solve", 2, SOLVE,
        title="괄호가 있는 일차부등식 풀기",
        skill="분배법칙으로 괄호를 먼저 풀고, 이항·정리·계수로 나누기",
        variant_axis={"부등호": "> ≥ < ≤", "구조": "a(x − p) 꼴 괄호", "해의 형태": "정수 경계"},
        discriminates="괄호를 풀 때 뒤 항에도 곱하는가, 음수로 나눌 때 방향을 바꾸는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[OS_PARAM, {"name": "a", "values": {"int": [2, 6]}}, {"name": "k", "values": {"in": [1, 2, 3]}}, {"name": "p", "values": {"int": [1, 6]}}, {"name": "x0", "values": {"int": [-5, 5]}}],
        table=OS_TABLE,
        derive={"c": "a - ps*k", "b": "-a*p", "d": "-a*p + ps*k*x0", "m": "ps*k", "r": "d + a*p"},
        constraints=["c >= 1", "d != 0", "x0 != 0", "c != a", "abs(d) <= 40", "x0 != p", "ps < 0 or k >= 2"],
        cost_values=["a", "p", "c", "d", "m", "r", "x0"],
        verify=["a*(x0 - p) == c*x0 + d", "sg*(a - c)*fd > 0", "m == a - c"],
        question="일차부등식 {a}(x − {p}) {OP} {co(c)}x {sgn(d)}{eul(d)} 푸시오.",
        answer="x {FOP} {x0}", answer_alt=[],
        sol1="괄호가 있으면 먼저 분배법칙으로 푼다 — {a}(x − {p})는 {a}x − {a*p}이고, 뒤의 {p}에도 {a}{eul(a)} 곱해야 한다. 그다음은 보통의 일차부등식과 같다: 이항해 정리하고 x의 계수로 나눈다(음수면 방향이 바뀐다).",
        sol1_fig=steps(["{a}(x − {p}) {OP} {co(c)}x {sgn(d)}", "{a}x − {a*p} {OP} {co(c)}x {sgn(d)}", "{co(m)}x {OP} {r}", "x {FOP} {x0}{FLIP}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)], [reveal(3)]],
        sol2=[
            "괄호를 풀면 {a}x − {a*p} {OP} {co(c)}x {sgn(d)}",
            "이항하여 정리하면 {a}x − {co(c)}x {OP} {d} + {a*p}, 곧 {co(m)}x {OP} {r}",
            "양변을 {m}{ro(m)} 나누면 x {FOP} {x0}{FLIP}",
        ],
        sol2_fig=steps([
            {"text": "{a}x − {a*p} {OP} {co(c)}x {sgn(d)}", "hint": "분배법칙 — {p}에도 {a}{eul(a)} 곱한다", "marks": [{"on": "{a*p}", "note": "{a}×{p}"}]},
            {"text": "{co(m)}x {OP} {r}", "hint": "이항 후 정리"},
            {"text": "x {FOP} {x0}", "hint": "양변 ÷ {pn(m)}{FLIP}", "marks": [{"on": "{x0}", "note": "{r} ÷ {pn(m)} = {x0}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="경계 x = {x0}{eul(x0)} 넣으면 좌변 {a}({x0} − {p}) = {a*(x0 - p)}, 우변 {c*x0 + d}{ro(c*x0 + d)} 같다(경계는 {INC}). 경계보다 {DIR}의 x = {x0 + fd}{eul(x0 + fd)} 넣으면 좌변 {a*(x0 + fd - p)}, 우변 {c*(x0 + fd) + d}{ro(c*(x0 + fd) + d)} 부등식이 성립한다. 답은 x {FOP} {x0}이다.",
        sol3_fig=numfig(),
        sol3_anim=[[hl("pt:{x0}", "lbl:{x0}")], [hl("seg:0", keep=True)]],
        model_answer="괄호를 풀면 {a}x − {a*p} {OP} {co(c)}x {sgn(d)}이고, 이항하여 정리하면 {co(m)}x {OP} {r}이다. 양변을 {m}{ro(m)} 나누면{FLIP} x {FOP} {x0}이다.",
        rubric=[
            {"element": "괄호 풀기", "points": 2, "criterion": "분배법칙으로 {a}(x − {p}) = {a}x − {a*p}{ro(a*p)} 바르게 풀었다.", "partial": "뒤 항에 곱하지 않았으면 인정하지 않는다."},
            {"element": "이항·계수로 나누기", "points": 3, "criterion": "이항해 {co(m)}x {OP} {r}{ro(r)} 정리하고 양변을 {m}{ro(m)} 나누어 x {FOP} {x0}{eul(x0)} 얻었다(음수이면 방향을 바꾸었다).", "partial": "정리까지 옳고 나눌 때 방향이 틀렸으면 1점."},
            {"element": "해 나타내기", "points": 2, "criterion": "해를 x {FOP} {x0}{ro(x0)} 쓰고 경계값 포함 여부를 바르게 표시했다.", "partial": "등호 포함 여부가 틀렸으면 1점."},
        ],
    )


def solve_t3():
    return tpl("m2-1-ineq-solve", 3, SOLVE,
        title="일차부등식을 만족하는 자연수 x의 개수",
        skill="부등식을 풀어 x의 범위를 구한 뒤 그 안의 자연수를 세기",
        variant_axis={"부등호": "≤ / <", "구하는 것": "자연수 해의 개수"},
        discriminates="해의 경계(분수)를 구하고 등호 포함 여부에 따라 자연수를 바르게 세는가",
        qtype="short", difficulty=3, pool_target=300, process="추론",
        params=[{"name": "q", "values": {"in": ["le", "lt"]}}, {"name": "a", "values": {"int": [2, 5]}}, {"name": "b", "values": {"int": [1, 9]}}, {"name": "N", "values": {"int": [2, 9]}}, {"name": "r", "values": {"int": [0, 4]}}],
        table={"key": "q", "rows": {"le": {"OP": "≤", "strict": 0, "K": "포함하므로", "TAIL": "이하"}, "lt": {"OP": "<", "strict": 1, "K": "포함하지 않으므로", "TAIL": "미만"}}},
        derive={"c": "a*N + r - b", "s": "a*N + r", "bd": "(a*N + r)/a"},
        constraints=["r < a", "c >= 1", "strict == 0 or r >= 1", "a != 3 or r == 0", "N != a", "N != b", "N != c"],
        cost_values=["a", "b", "c", "s", "N", "bd"],
        verify=["a*N - b <= c", "a*(N + 1) - b > c", "(strict == 0) or (a*N - b < c)"],
        question="일차부등식 {a}x − {b} {OP} {c}{eul(c)} 만족하는 자연수 x의 개수를 구하시오.",
        answer="{N}", answer_alt=["{N}개"],
        sol1="먼저 부등식을 풀어 x의 범위를 구한다: {b}{eul(b)} 이항하면 {a}x {OP} {s}, 양변을 {a}{ro(a)} 나누면 x {OP} {dec(bd)}. 이 범위 안의 자연수를 세는데, 경계가 자연수이면 등호 포함 여부가 개수를 바꾼다. 수직선에 경계를 찍고 그 왼쪽의 자연수를 세어 본다.",
        sol1_fig=[{"fn": "numline", "args": {"min": 0, "max": "{N + 2}", "points": [{"x": "{bd}", "label": "{dec(bd)}"}], "segments": [{"start": 0, "end": "{bd}", "inclusive": "{strict == 0}"}]}}],
        sol1_anim=[[hl("pt:{dec(bd)}", "lbl:{dec(bd)}")], [hl("seg:0", keep=True)]],
        sol2=[
            "{b}{eul(b)} 우변으로 이항하면 {a}x {OP} {c} + {b}, 곧 {a}x {OP} {s}",
            "양변을 {a}{ro(a)} 나누면 x {OP} {dec(bd)}",
            "경계 {dec(bd)}{eul(dec(bd))} {K} 이 범위의 자연수는 1, 2, …, {N}이다.",
            "따라서 자연수 x의 개수는 {N}개이다.",
        ],
        sol2_fig=steps([
            {"text": "{a}x {OP} {s}", "hint": "{b}{eul(b)} 이항"},
            {"text": "x {OP} {dec(bd)}", "hint": "양변 ÷ {a}", "marks": [{"on": "{dec(bd)}", "note": "{s} ÷ {a} = {dec(bd)}"}]},
            {"text": "x = 1, 2, …, {N}  → {N}개", "hint": "경계 {dec(bd)}{eun(dec(bd))} {TAIL}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], []],
        sol3="x = {N}{eul(N)} 넣으면 {a} × {N} − {b} = {a*N - b}{ro(a*N - b)} {c} {TAIL}이고, x = {N + 1}{eul(N + 1)} 넣으면 {a*(N + 1) - b}{ro(a*(N + 1) - b)} {c}{eul(c)} 넘으므로 자연수 해는 1부터 {N}까지, 모두 {N}개다.",
        sol3_fig=steps(["x = {N}: {a} × {N} − {b} = {a*N - b}  ✓", "x = {N + 1}: {a} × {N + 1} − {b} = {a*(N + 1) - b}  ✗"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{a}x − {b} {OP} {c}에서 {a}x {OP} {s}, x {OP} {dec(bd)}이다. 이 범위의 자연수는 1, 2, …, {N}이므로 자연수 x의 개수는 {N}개다.",
        rubric=[
            {"element": "부등식 풀기", "points": 3, "criterion": "이항·나눗셈으로 x {OP} {dec(bd)}{eul(dec(bd))} 구했다.", "partial": "이항까지 옳고 나눗셈이 틀렸으면 1점."},
            {"element": "자연수 세기", "points": 2, "criterion": "경계 {dec(bd)}의 포함 여부를 판단해 1부터 {N}까지임을 밝혔다.", "partial": "경계 처리(등호)가 틀려 하나 많거나 적으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "개수 {N}개를 답했다.", "partial": "가장 큰 자연수 {N}{eul(N)} 개수로 혼동했어도 값이 같으므로 근거를 확인해 1점."},
        ],
    )


def solve_t4():
    return tpl("m2-1-ineq-solve", 4, SOLVE,
        title="해가 주어진 일차부등식에서 x의 계수 구하기",
        skill="해의 부등호 방향이 원래와 반대이면 x의 계수가 음수임을 알아내고, 경계값으로 계수를 구하기",
        variant_axis={"구하는 것": "x의 계수 a", "조건": "해 x < k (방향이 바뀜)"},
        discriminates="'방향이 바뀌었으므로 a < 0'을 근거로 밝히고 (c − b)/a = k 를 푸는가",
        qtype="short", difficulty=4, pool_target=300, process="추론",
        params=[{"name": "a", "values": {"int": [-6, -2]}}, {"name": "b", "values": {"in": [-6, -4, -3, -2, 2, 3, 4, 5, 6]}}, {"name": "k", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}],
        derive={"c": "b + a*k", "cb": "a*k"},
        constraints=["c != 0", "c != b", "abs(c) <= 40", "a != k", "a != b", "a != c", "k != 1"],
        cost_values=["a", "b", "c", "k", "cb"],
        relation="(c - b)/X - k", unknown="X", answer_var="a",
        verify=["(c - b)/ans == k", "ans < 0"],
        question="x에 대한 일차부등식 ax {sgn(b)} > {c}의 해가 x < {k}일 때, 상수 a의 값을 구하시오.",
        answer="{a}", answer_alt=[],
        sol1="{b}{eul(b)} 이항하면 ax > {cb}. 그런데 해가 x < {k}로 부등호의 방향이 원래(>)와 반대다 — 양변을 a로 나눌 때 방향이 바뀌었다는 뜻이므로 a < 0이다. a < 0이면 x < {cb}/a이고, 이것이 x < {k}와 같으므로 {cb}/a = {k}에서 a를 구한다.",
        sol1_fig=steps(["ax {sgn(b)} > {c}", "ax > {cb}", "해가 x < {k}  ⇒  방향이 바뀜  ⇒  a < 0", "x < {cb}/a  이므로  {cb}/a = {k}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)], [reveal(3)]],
        sol2=[
            "{b}{eul(b)} 우변으로 이항하면 ax > {c} − {pn(b)}, 곧 ax > {cb}",
            "해 x < {k}의 부등호 방향이 원래와 반대이므로 양변을 나눈 수 a는 음수이다: a < 0",
            "a < 0이므로 ax > {cb}의 양변을 a로 나누면 x < {cb}/a",
            "이것이 x < {k}와 같아야 하므로 {cb}/a = {k}, 따라서 a = {cb} ÷ {pn(k)} = {a}",
        ],
        sol2_fig=steps([
            {"text": "ax > {cb}", "hint": "{b}{eul(b)} 이항"},
            {"text": "a < 0", "hint": "해의 방향이 반대 → 음수로 나눴다"},
            {"text": "x < {cb}/a  ⇒  {cb}/a = {k}", "hint": "양변 ÷ a (방향 바뀜)"},
            {"text": "a = {a}", "marks": [{"on": "{a}", "note": "{cb} ÷ {pn(k)} = {a}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="a = {a}{eul(a)} 넣으면 {a}x {sgn(b)} > {c}, {a}x > {cb}, 양변을 음수 {a}{ro(a)} 나누면 방향이 바뀌어 x < {k}로 주어진 해와 같다. a를 양수로 두면 해가 x > {k}가 되어 조건에 맞지 않는다. 답은 {a}이다.",
        sol3_fig=steps(["{a}x > {cb}", "x < {k}  (÷ {a}, 방향 바뀜)"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="ax {sgn(b)} > {c}에서 ax > {cb}이다. 해가 x < {k}로 부등호의 방향이 바뀌었으므로 a < 0이고, 양변을 a로 나누면 x < {cb}/a이다. 따라서 {cb}/a = {k}에서 a = {a}이다.",
        rubric=[
            {"element": "계수의 부호 판단", "points": 3, "criterion": "해의 부등호 방향이 반대이므로 a < 0임을 근거와 함께 밝혔다.", "partial": "a < 0이라고만 쓰고 근거(방향이 바뀜)가 없으면 1점."},
            {"element": "해 구하기", "points": 2, "criterion": "x < {cb}/a 로 정리하고 {cb}/a = {k}{eul(k)} 세웠다.", "partial": "ax > {cb}까지만 옳으면 1점."},
            {"element": "a 구하기", "points": 2, "criterion": "a = {a}{eul(a)} 구하고 해가 x < {k}{ika(k)} 됨을 확인했다.", "partial": "부호를 놓쳐 {-a}{ro(-a)} 답했으면 인정하지 않는다."},
        ],
    )


SOLVE_SEED = {
    "seed_id": "m2-1-ineq-solve", "category": "연산",
    "title": "일차부등식의 풀이 — 기본·괄호·자연수 해의 개수·계수 역산",
    "unit_id": "m2-1", "concept_ids": ["m2-1-08"],
    "schema_id": SCHEMA_SOLVE, "schema_name": "일차부등식의 풀이 / 괄호가 있는 일차부등식의 풀이 / 자연수 해 개수",
    "source_item_ids": [],
    "note": "경계 x0 를 먼저 뽑고 d = b + (a − c)x0 로 생성해 정수 경계 보장. 부등호·계수 부호 조합은 표(os). 해는 'x > 3' 문자열 답 — recheck.check_ineq 가 양변을 대입해 검산.",
    "geometry": False,
    "templates": [solve_t1(), solve_t2(), solve_t3(), solve_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 유리한 선택 (활용)
CHOICE = {"process": "문제해결", "context": "생활맥락", "prereq": ["일차부등식의 풀이"], "ops": ["부등식", "사칙"], "traps": ["조건누락", "구하는대상혼동"],
          "time_limit": 120, "points": 5, "tags": ["일차부등식의 활용", "유리한 선택"]}

SUB_CTX = {
    "1": {"S": "어느 영화 스트리밍 서비스는 영화 한 편을 볼 때마다", "A": "원을 내거나, 한 달에", "B": "원을 내고 무제한으로 볼 수 있다", "U": "편", "Q": "한 달에 영화를 몇 편 이상 볼 때 월 구독이 유리한지", "X": "한 달에 보는 영화의 수", "P1": "편당 결제", "P2": "월 구독"},
    "2": {"S": "어느 헬스장은 1회 이용할 때마다", "A": "원을 내거나, 한 달에", "B": "원을 내고 무제한으로 이용할 수 있다", "U": "회", "Q": "한 달에 몇 회 이상 이용할 때 월 정기권이 유리한지", "X": "한 달 이용 횟수", "P1": "1회 이용권", "P2": "월 정기권"},
    "3": {"S": "어느 실내 클라이밍장은 1회 입장할 때마다", "A": "원을 내거나, 한 달에", "B": "원을 내고 무제한으로 입장할 수 있다", "U": "회", "Q": "한 달에 몇 회 이상 입장할 때 월 정기권이 유리한지", "X": "한 달 입장 횟수", "P1": "1회 입장권", "P2": "월 정기권"},
    "4": {"S": "어느 음악 앱은 노래 한 곡을 내려받을 때마다", "A": "원을 내거나, 한 달에", "B": "원을 내고 무제한으로 내려받을 수 있다", "U": "곡", "Q": "한 달에 몇 곡 이상 내려받을 때 월 구독이 유리한지", "X": "한 달에 내려받는 곡의 수", "P1": "곡당 결제", "P2": "월 구독"},
}


def choice_t1():
    return tpl("m2-1-ineq-choice", 1, CHOICE,
        title="건당 결제 vs 월 구독 — 몇 번 이상이면 구독이 유리한가",
        skill="횟수를 x로 놓고 (건당 요금) × x > (구독료) 를 세워 가장 작은 자연수 해 찾기",
        variant_axis={"비교": "건당 vs 정액", "구하는 것": "몇 회 이상", "맥락": "스트리밍·헬스장·클라이밍·음악 앱"},
        discriminates="'유리하다'를 비용의 대소로 옮겨 부등식을 세우고, 해 x > k 에서 자연수(이상) 조건으로 답하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(SUB_CTX)}}, {"name": "a", "values": {"in": [1000, 1200, 1500, 2000, 2500, 3000, 3500, 4000]}}, {"name": "b", "values": {"in": [9900, 10000, 11000, 12000, 12900, 13000, 14900, 15000, 15900, 18000, 19900, 20000, 22000, 24900, 25000]}}],
        table={"key": "c", "rows": SUB_CTX},
        derive={"bd": "b/a", "N": "floor(b/a) + 1"},
        constraints=["N >= 3", "N <= 16", "N != a", "N != b", "100*bd == floor(100*bd)"],
        cost_values=["a", "b", "bd", "N"],
        relation="X - floor(b/a) - 1", unknown="X", answer_var="N",
        verify=["a*ans > b", "a*(ans - 1) <= b"],
        question="{S} {a}{A} {b}{B}. {Q} 구하시오.",
        answer="{N}", answer_alt=["{N}{U}", "{N}{U} 이상"],
        sol1="{X}{eul(X)} x{U}이라 하면 {P1} 비용은 {a}x원, {P2} 비용은 {b}원으로 고정이다. 구독이 유리하다는 것은 구독 비용이 더 적다는 뜻이므로 {a}x > {b}라는 부등식을 세운다. 해는 x > {dec(bd)}이지만 횟수는 자연수이므로 이를 만족하는 가장 작은 자연수를 답한다 — 경계값 그대로가 아니다.",
        sol1_fig=table(["", "{P1}", "{P2}"], [["비용", "{a}x원", "{b}원"], ["구독이 유리", "{a}x > {b}", ""]]),
        sol2=[
            "{X}{eul(X)} x{U}이라 하면 {P1}은 {a}x(원), {P2}은 {b}(원)이다.",
            "{P2}이 유리하려면 {P2} 비용이 더 적어야 하므로 {a}x > {b}",
            "양변을 {a}{ro(a)} 나누면 x > {dec(bd)}",
            "x는 자연수이므로 이를 만족하는 가장 작은 값은 {N}이다. 따라서 {N}{U} 이상 볼(이용할) 때 {P2}이 유리하다.",
        ],
        sol2_fig=steps([
            {"text": "{a}x > {b}", "hint": "건당 비용 > 구독료 이면 구독이 유리"},
            {"text": "x > {dec(bd)}", "hint": "양변 ÷ {a}", "marks": [{"on": "{dec(bd)}", "note": "{b} ÷ {a} = {dec(bd)}"}]},
            {"text": "x = {N}, {N + 1}, …  → {N}{U} 이상", "hint": "자연수 조건"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], []],
        sol3="{N - 1}{U}이면 {P1} {a} × {N - 1} = {a*(N - 1)}원으로 {P2} {b}원보다 싸거나 같아 {P2}이 유리하지 않다. {N}{U}이면 {a} × {N} = {a*N}원 > {b}원이므로 {P2}이 유리하다. 답은 {N}{U}이다.",
        sol3_fig=table(["{X}", "{P1}", "{P2}", "유리한 쪽"], [["{N - 1}{U}", "{a*(N - 1)}원", "{b}원", "{P1}"], ["{N}{U}", "{a*N}원", "{b}원", "{P2}"]]),
        model_answer="{X}{eul(X)} x{U}이라 하면 {P1} 비용은 {a}x원, {P2} 비용은 {b}원이다. {P2}이 유리하려면 {a}x > {b}이어야 하므로 x > {dec(bd)}이고, x는 자연수이므로 {N}{U} 이상일 때 {P2}이 유리하다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "횟수를 x로 놓고 두 비용 {a}x, {b}{eul(b)} 비교하는 부등식 {a}x > {b}{eul(b)} 세웠다.", "partial": "부등호 방향이 반대이면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "x > {dec(bd)}{eul(dec(bd))} 바르게 구했다.", "partial": "나눗셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 {N}{U} 이상이라고 답했다.", "partial": "경계값 {dec(bd)}{eul(dec(bd))} 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


SHIP_CTX = {
    "1": {"I": "볼펜", "U": "자루", "SH": "동네 문구점", "ON": "온라인 문구 쇼핑몰", "AMAX": 3000},
    "2": {"I": "과자", "U": "봉지", "SH": "동네 마트", "ON": "온라인 식품몰", "AMAX": 3000},
    "3": {"I": "마스크 팩", "U": "장", "SH": "동네 드러그스토어", "ON": "온라인 뷰티몰", "AMAX": 5000},
    "4": {"I": "손 세정제", "U": "개", "SH": "동네 생활용품점", "ON": "온라인 생활용품몰", "AMAX": 5000},
}


def choice_t2():
    return tpl("m2-1-ineq-choice", 2, CHOICE,
        title="온라인 할인 + 배송비 vs 동네 가게 — 몇 개 이상 살 때 온라인이 유리한가",
        skill="할인율을 적용한 단가와 배송비를 합쳐 (동네 가게 비용) > (온라인 비용) 부등식 세우기",
        variant_axis={"비교": "할인+고정비 vs 정가", "구하는 것": "몇 개 이상", "맥락": "문구·식품·뷰티·생활용품"},
        discriminates="할인된 단가 (1 − p/100)a 를 바르게 쓰고 배송비를 한 번만 더하는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(SHIP_CTX)}}, {"name": "a", "values": {"in": [1500, 2000, 2500, 3000, 4000, 5000]}}, {"name": "p", "values": {"in": [10, 20, 25, 30]}}, {"name": "f", "values": {"in": [2500, 3000, 3500, 4000, 4500, 5000]}}],
        table={"key": "c", "rows": SHIP_CTX},
        derive={"da": "a*p/100", "oa": "a - a*p/100", "bd": "f/(a*p/100)", "N": "floor(f/(a*p/100)) + 1"},
        constraints=["a <= AMAX", "N >= 3", "N <= 15", "da == floor(da)", "N != p", "100*bd == floor(100*bd)"],
        cost_values=["a", "p", "f", "da", "oa", "bd", "N"],
        relation="X - floor(f/(a*p/100)) - 1", unknown="X", answer_var="N",
        verify=["da*ans > f", "da*(ans - 1) <= f", "oa == a - da"],
        question="{SH}에서 한 {U}에 {a}원인 {I}{eul(I)} {ON}에서는 {p}% 할인된 가격에 팔지만 배송비 {f}원을 따로 내야 한다. {I}{eul(I)} 몇 {U} 이상 살 때 {ON}에서 사는 것이 유리한지 구하시오.",
        answer="{N}", answer_alt=["{N}{U}", "{N}{U} 이상"],
        sol1="x{U}{eul(U)} 산다고 하면 {SH} 비용은 {a}x원, {ON} 비용은 할인된 단가 {a} × (1 − {p}/100) = {oa}원에 x를 곱하고 배송비 {f}원을 한 번 더한 {oa}x + {f}원이다. 온라인이 유리하려면 {a}x > {oa}x + {f}. 한 {U}당 {da}원씩 아끼는 셈이므로 배송비 {f}원을 넘어서는 개수를 찾는 문제다.",
        sol1_fig=table(["", "{SH}", "{ON}"], [["단가", "{a}원", "{oa}원 ({p}% 할인)"], ["배송비", "0", "{f}원"], ["비용", "{a}x", "{oa}x + {f}"]]),
        sol2=[
            "{I}{eul(I)} x{U} 산다고 하면 {SH} 비용은 {a}x(원)",
            "{ON}의 단가는 {a} × (1 − {p}/100) = {oa}(원)이므로 비용은 {oa}x + {f}(원)",
            "{ON}이 유리하려면 {a}x > {oa}x + {f}, 곧 {da}x > {f}",
            "양변을 {da}{ro(da)} 나누면 x > {dec(bd)}이고, x는 자연수이므로 {N}{U} 이상이다.",
        ],
        sol2_fig=steps([
            {"text": "{a}x > {oa}x + {f}", "hint": "동네 비용 > 온라인 비용", "marks": [{"on": "{oa}x", "note": "{a}×{100 - p}%"}]},
            {"text": "{da}x > {f}", "hint": "한 {U}당 {da}원 절약"},
            {"text": "x > {dec(bd)}  → {N}{U} 이상", "hint": "자연수 조건", "marks": [{"on": "{dec(bd)}", "note": "{f} ÷ {da} = {dec(bd)}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol3="{N - 1}{U}: {SH} {a*(N - 1)}원, {ON} {oa*(N - 1) + f}원 → 온라인이 유리하지 않다. {N}{U}: {SH} {a*N}원, {ON} {oa*N + f}원 → 온라인이 더 싸다. 답은 {N}{U}이다.",
        sol3_fig=table(["개수", "{SH}", "{ON}"], [["{N - 1}{U}", "{a*(N - 1)}원", "{oa*(N - 1) + f}원"], ["{N}{U}", "{a*N}원", "{oa*N + f}원"]]),
        model_answer="{I}{eul(I)} x{U} 산다고 하면 {SH} 비용은 {a}x원, {ON} 비용은 {oa}x + {f}원이다. {ON}이 유리하려면 {a}x > {oa}x + {f}, 곧 {da}x > {f}에서 x > {dec(bd)}이므로 x는 자연수 조건에서 {N}{U} 이상이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "할인 단가 {oa}원과 배송비 {f}원으로 두 비용을 나타내고 {a}x > {oa}x + {f}{eul(f)} 세웠다.", "partial": "할인율 적용이 틀렸거나 배송비를 x배 했으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{da}x > {f}{ro(f)} 정리하고 x > {dec(bd)}{eul(dec(bd))} 구했다.", "partial": "정리까지 옳고 나눗셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 {N}{U} 이상이라고 답했다.", "partial": "경계값을 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


BUDGET_CTX = {
    "1": {"I": "티셔츠", "U": "장", "W": "동아리 단체 티셔츠"},
    "2": {"I": "간식 세트", "U": "개", "W": "봉사 활동 간식"},
    "3": {"I": "책", "U": "권", "W": "학급 문고 도서"},
    "4": {"I": "키링", "U": "개", "W": "축제 기념 키링"},
}


def choice_t3():
    return tpl("m2-1-ineq-choice", 3, CHOICE,
        title="예산 안에서 배송비를 내고 살 수 있는 최대 개수",
        skill="(단가) × x + (배송비) ≤ (예산) 을 세우고 가장 큰 자연수 해 찾기",
        variant_axis={"비교": "예산 상한", "구하는 것": "최대 개수", "맥락": "단체 티셔츠·간식·도서·키링"},
        discriminates="배송비를 한 번만 더해 ≤ 부등식을 세우고 해에서 가장 큰 자연수를 택하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(BUDGET_CTX)}}, {"name": "B", "values": {"in": [50000, 80000, 100000, 150000, 200000]}}, {"name": "a", "values": {"in": [4500, 6000, 7500, 8000, 9000, 12000, 15000]}}, {"name": "f", "values": {"in": [3000, 3500, 4000, 5000]}}],
        table={"key": "c", "rows": BUDGET_CTX},
        derive={"bd": "(B - f)/a", "N": "floor((B - f)/a)"},
        constraints=["N >= 3", "N <= 30", "N != a", "100*bd == floor(100*bd)"],
        cost_values=["B", "a", "f", "bd", "N"],
        relation="X - floor((B - f)/a)", unknown="X", answer_var="N",
        verify=["a*ans + f <= B", "a*(ans + 1) + f > B"],
        question="{W}{eul(W)} 온라인으로 주문하려고 한다. 예산은 {B}원이고, {I}{eun(I)} 한 {U}에 {a}원이며 배송비 {f}원을 따로 내야 한다. {I}{eul(I)} 최대 몇 {U}까지 살 수 있는지 구하시오.",
        answer="{N}", answer_alt=["{N}{U}"],
        sol1="x{U}{eul(U)} 산다고 하면 비용은 {a}x + {f}원이고, 예산을 넘지 않아야 하므로 {a}x + {f} ≤ {B}이다. 배송비는 개수와 상관없이 한 번만 든다. 해 x ≤ {dec(bd)}에서 자연수 중 가장 큰 값이 답이다 — 올림하면 예산을 넘긴다.",
        sol1_fig=table(["", "금액"], [["{I} x{U}", "{a}x원"], ["배송비", "{f}원"], ["합계", "{a}x + {f} ≤ {B}"]]),
        sol2=[
            "{I}{eul(I)} x{U} 산다고 하면 비용은 {a}x + {f}(원)",
            "예산을 넘지 않아야 하므로 {a}x + {f} ≤ {B}",
            "{f}{eul(f)} 이항하면 {a}x ≤ {B - f}, 양변을 {a}{ro(a)} 나누면 x ≤ {dec(bd)}",
            "x는 자연수이므로 가장 큰 값은 {N}이다. 따라서 최대 {N}{U}까지 살 수 있다.",
        ],
        sol2_fig=steps([
            {"text": "{a}x + {f} ≤ {B}", "hint": "비용 ≤ 예산 (배송비는 한 번)"},
            {"text": "{a}x ≤ {B - f}", "hint": "{f}{eul(f)} 이항"},
            {"text": "x ≤ {dec(bd)}  → 최대 {N}{U}", "hint": "자연수 조건 — 내림", "marks": [{"on": "{dec(bd)}", "note": "{B - f} ÷ {a} = {dec(bd)}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol3="{N}{U}이면 {a} × {N} + {f} = {a*N + f}원으로 예산 {B}원 안이고, {N + 1}{U}이면 {a*(N + 1) + f}원으로 예산을 넘는다. 답은 {N}{U}이다.",
        sol3_fig=table(["개수", "비용", "예산 {B}원"], [["{N}{U}", "{a*N + f}원", "가능"], ["{N + 1}{U}", "{a*(N + 1) + f}원", "초과"]]),
        model_answer="{I}{eul(I)} x{U} 산다고 하면 {a}x + {f} ≤ {B}이어야 하므로 {a}x ≤ {B - f}, x ≤ {dec(bd)}이다. x는 자연수이므로 최대 {N}{U}까지 살 수 있다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "개수를 x로 놓고 배송비를 한 번 더한 {a}x + {f} ≤ {B}{eul(B)} 세웠다.", "partial": "배송비를 빠뜨리거나 x배 했으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "x ≤ {dec(bd)}{eul(dec(bd))} 바르게 구했다.", "partial": "이항까지 옳고 나눗셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 최대 {N}{U}라고 답했다.", "partial": "예산을 넘는 {N + 1}{U}{ro(U)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


PLAN_CTX = {
    "1": {"S": "전기차 충전 요금제 A는 기본료 없이 1 kWh당", "T": "원이고, 요금제 B는 월 기본료", "V": "원에 1 kWh당", "E": "원이다", "U": " kWh", "Q": "한 달에 몇 kWh 이상 충전할 때 요금제 B가 유리한지", "X": "한 달 충전량", "N1": "요금제 A", "N2": "요금제 B", "NMAX": 80, "FMIN": 1900, "FMAX": 9900},
    "2": {"S": "배달 앱에서 구독 없이 주문하면 한 건당 배달비가", "T": "원이고, 월 구독을 하면 월", "V": "원을 내고 한 건당 배달비가", "E": "원이다", "U": "건", "Q": "한 달에 몇 건 이상 주문할 때 월 구독이 유리한지", "X": "한 달 주문 건수", "N1": "구독 없이", "N2": "월 구독", "NMAX": 30, "FMIN": 2900, "FMAX": 12900},
    "3": {"S": "어느 공유 자전거는 이용권 없이 타면 1회당", "T": "원이고, 월 이용권을 사면 월", "V": "원에 1회당", "E": "원이다", "U": "회", "Q": "한 달에 몇 회 이상 탈 때 월 이용권이 유리한지", "X": "한 달 이용 횟수", "N1": "이용권 없이", "N2": "월 이용권", "NMAX": 40, "FMIN": 4900, "FMAX": 14900},
}
PLAN_PAIRS = {   # 맥락별 (단가만, 기본료 있는 쪽 단가) — 전기차 kWh 단가 / 배달비 / 자전거 1회 요금 규모에 맞춘다
    "1": [(350, 250), (320, 220), (400, 250), (300, 200), (360, 240), (420, 300), (380, 260), (450, 300), (500, 300), (480, 320)],
    "2": [(3000, 2000), (3500, 2500), (3000, 1500), (2500, 1500), (4000, 2500), (3500, 2000), (2500, 2000), (4000, 3000), (3000, 2500), (4500, 3000)],
    "3": [(1500, 1000), (1200, 800), (2000, 1000), (1000, 500), (1800, 1200), (1500, 800), (2000, 1500), (1300, 800), (1000, 700), (1600, 1000)],
}
PLAN_ROWS = {f"{c}-{i}": {**PLAN_CTX[c], "a1": a1, "a2": a2, "dd": a1 - a2} for c, prs in PLAN_PAIRS.items() for i, (a1, a2) in enumerate(prs)}
PLAN_F = [1900, 2900, 3900, 4900, 5900, 6900, 7900, 9900, 12900, 14900]


def choice_t4():
    return tpl("m2-1-ineq-choice", 4, CHOICE,
        title="기본료 + 단가 요금제 비교 — 몇 단위 이상이면 기본료가 있는 쪽이 유리한가",
        skill="(단가만) × x > (기본료) + (낮은 단가) × x 를 세워 단가 차이로 기본료를 나누기",
        variant_axis={"비교": "단가 vs 기본료+낮은 단가", "구하는 것": "몇 단위 이상", "맥락": "전기차 충전·배달 앱 구독·공유 자전거"},
        discriminates="두 요금제의 비용을 x의 식으로 나타내고 부등호 방향(유리 = 더 적은 비용)을 바르게 잡는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "cp", "values": {"in": list(PLAN_ROWS)}}, {"name": "F", "values": {"in": PLAN_F}}],
        table={"key": "cp", "rows": PLAN_ROWS},
        derive={"bd": "F/dd", "N": "floor(F/dd) + 1"},
        constraints=["F >= FMIN", "F <= FMAX", "N >= 3", "N <= NMAX", "N != a1", "N != a2", "100*bd == floor(100*bd)"],
        cost_values=["a1", "a2", "F", "dd", "bd", "N"],
        relation="X - floor(F/dd) - 1", unknown="X", answer_var="N",
        verify=["a1*ans > F + a2*ans", "a1*(ans - 1) <= F + a2*(ans - 1)", "dd == a1 - a2"],
        question="{S} {a1}{T} {F}{V} {a2}{E}. {Q} 구하시오.",
        answer="{N}", answer_alt=["{N}{U}", "{N}{U} 이상"],
        sol1="{X}{eul(X)} x{U}라 하면 {N1} 비용은 {a1}x원, {N2} 비용은 기본료를 더한 {F} + {a2}x원이다. {N2}가 유리하려면 {a1}x > {F} + {a2}x. {U}당 {dd}원씩 덜 내는 대신 기본료 {F}원을 내는 셈이므로, 절약액이 기본료를 넘는 x를 찾는다.",
        sol1_fig=table(["", "{N1}", "{N2}"], [["기본료", "0", "{F}원"], ["{U}당", "{a1}원", "{a2}원"], ["비용", "{a1}x", "{F} + {a2}x"]]),
        sol2=[
            "{X}{eul(X)} x{U}라 하면 {N1}은 {a1}x(원), {N2}는 {F} + {a2}x(원)",
            "{N2}가 유리하려면 {a1}x > {F} + {a2}x",
            "이항하여 정리하면 {dd}x > {F}, 양변을 {dd}{ro(dd)} 나누면 x > {dec(bd)}",
            "x는 자연수이므로 {N}{U} 이상일 때 {N2}가 유리하다.",
        ],
        sol2_fig=steps([
            {"text": "{a1}x > {F} + {a2}x", "hint": "{N1} 비용 > {N2} 비용"},
            {"text": "{dd}x > {F}", "hint": "{U}당 {dd}원 절약", "marks": [{"on": "{dd}x", "note": "{a1} − {a2}"}]},
            {"text": "x > {dec(bd)}  → {N}{U} 이상", "hint": "자연수 조건", "marks": [{"on": "{dec(bd)}", "note": "{F} ÷ {dd} = {dec(bd)}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol3="{N - 1}{U}: {N1} {a1*(N - 1)}원, {N2} {F + a2*(N - 1)}원 → {N2}가 유리하지 않다. {N}{U}: {N1} {a1*N}원, {N2} {F + a2*N}원 → {N2}가 더 싸다. 답은 {N}{U}이다.",
        sol3_fig=table(["{X}", "{N1}", "{N2}"], [["{N - 1}{U}", "{a1*(N - 1)}원", "{F + a2*(N - 1)}원"], ["{N}{U}", "{a1*N}원", "{F + a2*N}원"]]),
        model_answer="{X}{eul(X)} x{U}라 하면 {N1} 비용은 {a1}x원, {N2} 비용은 {F} + {a2}x원이다. {N2}가 유리하려면 {a1}x > {F} + {a2}x, 곧 {dd}x > {F}에서 x > {dec(bd)}이므로 자연수 조건에서 {N}{U} 이상이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "두 비용을 {a1}x, {F} + {a2}x로 나타내고 {a1}x > {F} + {a2}x{eul(F)} 세웠다.", "partial": "기본료를 x배 하거나 부등호 방향이 반대이면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{dd}x > {F}{ro(F)} 정리하고 x > {dec(bd)}{eul(dec(bd))} 구했다.", "partial": "정리까지 옳고 나눗셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 {N}{U} 이상이라고 답했다.", "partial": "경계값을 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


CHOICE_SEED = {
    "seed_id": "m2-1-ineq-choice", "category": "활용",
    "title": "일차부등식의 활용 — 유리한 선택(구독·할인+배송비·예산·요금제)",
    "unit_id": "m2-1", "concept_ids": ["m2-1-09", "m2-1-10"],
    "schema_id": SCHEMA_CHOICE, "schema_name": "두 선택지 비용 비교 → 유리한 조건 찾기 / 고정비용+단위비용 최대개수",
    "source_item_ids": [],
    "note": "관계식 (비용 비교 부등식)만 차용. 맥락은 요즘 상황(스트리밍·헬스장·클라이밍·음악 앱·온라인몰 배송비·단체 굿즈 예산·전기차 충전·배달 구독·공유 자전거). 답은 경계의 가장 작은(큰) 자연수.",
    "geometry": False,
    "templates": [choice_t1(), choice_t2(), choice_t3(), choice_t4()],
}


if __name__ == "__main__":
    for seed in (SOLVE_SEED, CHOICE_SEED):
        with_pitfalls(seed)
        dump(seed)
