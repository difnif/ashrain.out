# itemfactory/tools/mkseed_m1_algebra.py — m1-1 문자와 식·방정식 기본 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m1_algebra.py
#     → seeds/m1-1-expr-value.json      (식의 값: 정수 대입·분수 대입·공식·두 문자, 4틀)
#     → seeds/m1-1-linear-expr.json     (일차식: 괄호 전개 계수·분수 계수·잘못 계산한 식·둘레 식·동류항, 5틀)
#     → seeds/m1-1-eq-solution.json     (방정식과 해: 항등식 a,b·해→상수항·해→계수·해가 같은 두 방정식, 4틀)
#     → seeds/m1-1-linear-eq-const.json (해 조건→상수: 해의 배수 관계·자연수 해·해 없음·해 무수히 많음, 4틀)
#     → seeds/m1-1-eq-apply-2.json      (활용 2: 정가·원가, 일, 직사각형 둘레, 사다리꼴 넓이, 4틀)
#
# 식(일차식) 답은 문자열 — verify 는 ans 를 쓰지 않고, recheck.py 가 mathir 로 x = 0, 1 에서 대조한다.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


NZ = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
NZ2 = [-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]          # 계수 ±1 제외 (표기 '1x' 회피)
BASE = {"process": "절차수행", "context": "무맥락", "ops": ["사칙", "대입"], "traps": ["부호", "계산순서"], "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}

# ═══════════════════════════════════════════════════════════════════ 1. 식의 값
EV = "m1-1-expr-value"
EV_BASE = {**BASE, "prereq": ["문자를 사용한 식", "유리수의 계산"], "tags": ["식의 값", "대입"]}
LIN_ROWS = {str(q): {"QX": ("+ " if q > 0 else "− ") + (str(abs(q)) if abs(q) != 1 else "") + "x", "q": q} for q in NZ}


def ev_t1():
    return tpl(EV, 1, EV_BASE,
        title="x에 정수를 대입한 식의 값 — px² + qx + r",
        skill="음수를 대입할 때 괄호를 써서 부호와 거듭제곱을 바르게 처리하고 계산 순서를 지키기",
        variant_axis={"대입값": "−5~5 (0 제외)", "이차항 계수": "±1~±4"},
        discriminates="x = −a를 대입할 때 (−a)²과 −a²을 구별하고, 곱셈을 덧셈보다 먼저 하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": [-5, -4, -3, -2, -1, 2, 3, 4, 5]}}, {"name": "p", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}},
                {"name": "qq", "values": {"in": list(LIN_ROWS)}}, {"name": "r", "values": {"in": NZ}}],
        table={"key": "qq", "rows": LIN_ROWS},
        derive={"sq": "a*a", "t2": "p*a*a", "t1": "q*a", "ans": "p*a*a + q*a + r"},
        constraints=["ans != a", "ans != p", "ans != q", "ans != r", "ans != 0", "abs(ans) <= 150"],
        cost_values=["a", "p", "q", "r", "ans"],
        answer_var="ans",
        verify=["ans == p*a*a + q*a + r"],
        question="x = {a}일 때, {co(p)}x² {QX} {sgn(r)}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="식의 값은 문자 자리에 수를 대입해 계산한 값이다. 음수를 대입할 때는 반드시 괄호를 쓰고, 거듭제곱 → 곱셈 → 덧셈·뺄셈의 순서로 계산한다. 특히 x = {a}이면 x² = {pn(a)}² = {sq}이다.",
        sol2=[
            "x = {a}{eul(a)} 대입하면 {co(p)}x² {QX} {sgn(r)} = {p} × {pn(a)}² {QX_SUB} {sgn(r)}",
            "거듭제곱과 곱셈을 먼저 계산하면 {t2} {sgn(t1)} {sgn(r)}",
            "따라서 식의 값은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "{p} × {pn(a)}² {QX_SUB} {sgn(r)}", "hint": "음수는 괄호로 대입"},
            {"text": "= {t2} {sgn(t1)} {sgn(r)}", "hint": "거듭제곱 → 곱셈", "marks": [{"on": "{t2}", "note": "{pn(a)}² = {sq}"}]},
            {"text": "= {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="x² = {sq}, 이차항 {p} × {sq} = {t2}, 일차항 {q} × {pn(a)} = {t1}이고 {t2} {sgn(t1)} {sgn(r)} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["x² = {pn(a)}² = {sq}", "{t2} {sgn(t1)} {sgn(r)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = {a}{eul(a)} 대입하면 {p} × {pn(a)}² {QX_SUB} {sgn(r)} = {t2} {sgn(t1)} {sgn(r)} = {ans}이다.",
        rubric=[
            {"element": "대입", "points": 2, "criterion": "x 자리에 {a}{eul(a)} 괄호를 써서 대입한 식을 썼다.", "partial": "괄호 없이 대입해 부호가 어긋났으면 인정하지 않는다."},
            {"element": "거듭제곱·곱셈 계산", "points": 3, "criterion": "{pn(a)}² = {sq}, {p} × {sq} = {t2}, {q} × {pn(a)} = {t1}{eul(t1)} 바르게 계산했다.", "partial": "거듭제곱의 부호가 틀렸으면 인정하지 않고, 곱셈 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "식의 값 {ans}{eul(ans)} 구했다.", "partial": "마지막 덧셈·뺄셈 실수면 1점."},
        ],
        rubric_total=7,
    )


# 표 문자열에는 {pn(a)} 를 둘 수 없다 → 계수 부분과 대입값을 나눈다: QS0 = '+ 3 ×' / '+' , 그 뒤 템플릿에서 {pn(a)}
LIN_ROWS_SUB = {k: {**v, "QS0": ("+ " if v["q"] > 0 else "− ") + (f"{abs(v['q'])} ×" if abs(v["q"]) != 1 else "")} for k, v in LIN_ROWS.items()}


def ev_t1_final():
    t = ev_t1()
    t["table"] = {"key": "qq", "rows": LIN_ROWS_SUB}
    from seedlib import sub_all
    return sub_all(t, {"{QX_SUB}": "{QS0} {pn(a)}"})


def ev_t2():
    return tpl(EV, 2, EV_BASE,
        title="x에 분수를 대입한 식의 값 — cx² ± 1/x",
        skill="분수를 대입할 때 거듭제곱은 분자·분모를 각각 제곱하고, 1/x는 x의 역수임을 이용하기",
        variant_axis={"대입값": "±m/n (n 2~5)", "부호": "+ / −"},
        discriminates="1/x에 분수를 대입하면 역수가 됨을 알고, 음수의 제곱을 양수로 처리하는가",
        difficulty=3,
        params=[{"name": "sg", "values": {"in": ["p", "n"]}}, {"name": "op", "values": {"in": ["plus", "minus"]}}, {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [2, 5]}}, {"name": "k", "values": {"int": [1, 5]}}],
        table=[{"key": "sg", "rows": {"p": {"s": 1}, "n": {"s": -1}}}, {"key": "op", "rows": {"plus": {"OP": "+", "o": 1}, "minus": {"OP": "−", "o": -1}}}],
        derive={"X": "s*m/n", "c": "k*n*n", "sq": "m*m/(n*n)", "t1": "k*m*m", "rec": "s*n/m", "ans": "k*m*m + o*s*n/m"},
        constraints=["gcd(m, n) == 1", "ans != 0", "ans != c", "ans != n", "ans != m", "abs(ans) != 1", "k*m*m <= 60"],
        cost_values=["X", "c", "ans"],
        answer_var="ans",
        verify=["ans == c*X*X + o/X", "X*n == s*m"],
        question="x = {X}일 때, {c}x² {OP} [[frac(1,x)]]의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x = {X}{eul(m)} 대입한다. x²은 분자와 분모를 각각 제곱한 {sq}이고, [[frac(1,x)]]는 x의 역수이므로 {X}의 역수 {rec}이다(부호는 그대로, 분자·분모만 바꾼다). 그다음 곱셈을 먼저 하고 {OP} 기호로 잇는다.",
        sol2=[
            "x² = ({X})² = {sq}이므로 {c}x² = {c} × {sq} = {t1}",
            "[[frac(1,x)]] = 1 ÷ ({X}) = {rec}",
            "따라서 {c}x² {OP} [[frac(1,x)]] = {t1} {OP} {pn(rec)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{c} × ({X})² = {c} × {sq} = {t1}", "hint": "분수의 제곱 = 분자²/분모²"},
            {"text": "[[frac(1,x)]] = {rec}", "hint": "x의 역수 — 부호 그대로"},
            {"text": "{t1} {OP} {pn(rec)} = {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{X} × {rec} = 1이므로 역수가 맞고, ({X})² = {sq} > 0이다. {t1} {OP} {pn(rec)} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{X} × {pn(rec)} = 1", "{t1} {OP} {pn(rec)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = {X}이면 x² = {sq}, [[frac(1,x)]] = {rec}이므로 {c}x² {OP} [[frac(1,x)]] = {t1} {OP} {pn(rec)} = {ans}이다.",
        rubric=[
            {"element": "x² 계산", "points": 2, "criterion": "({X})² = {sq}{eul(m*m)} 구하고 {c}x² = {t1}{eul(t1)} 구했다.", "partial": "분자만 제곱했거나 부호를 음수로 했으면 인정하지 않는다."},
            {"element": "1/x 계산", "points": 3, "criterion": "[[frac(1,x)]]을 x의 역수 {rec}{ro(n)} 구했다.", "partial": "역수의 부호를 바꿨으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{t1} {OP} {pn(rec)} = {ans}{eul(ans)} 구했다.", "partial": "마지막 계산의 부호 실수면 1점."},
        ],
        rubric_total=7,
    )


FORM_ROWS = {
    "sound": {"INTRO": "기온이 x °C일 때 소리의 속력은 초속 (331 + 0.6x) m이다.", "VAR": "기온이", "XU": " °C일 때", "ASK": "소리의 속력은 초속 몇 m인지", "sc": 5, "off": -30, "iA": 1, "iB": 0, "iC": 0, "iD": 0, "iE": 0, "iF": 0, "iG": 0, "F1": "331 + 0.6 ×", "F2": "", "UNIT": " m", "xmax": 14},
    "fahr": {"INTRO": "섭씨온도 x °C를 화씨온도로 나타내면 (1.8x + 32) °F이다.", "VAR": "섭씨온도가", "XU": " °C일 때", "ASK": "화씨온도는 몇 °F인지", "sc": 5, "off": -20, "iA": 0, "iB": 1, "iC": 0, "iD": 0, "iE": 0, "iF": 0, "iG": 0, "F1": "1.8 ×", "F2": " + 32", "UNIT": " °F", "xmax": 12},
    "sale": {"INTRO": "정가가 x원인 물건을 20 % 할인하여 팔 때의 판매 가격은 0.8x원이다.", "VAR": "정가가", "XU": "원일 때", "ASK": "판매 가격은 몇 원인지", "sc": 2500, "off": 0, "iA": 0, "iB": 0, "iC": 1, "iD": 0, "iE": 0, "iF": 0, "iG": 0, "F1": "0.8 ×", "F2": "", "UNIT": "원", "xmax": 12},
    "fuel": {"INTRO": "휘발유 1 L로 15 km를 갈 수 있는 자동차가 휘발유 x L로 갈 수 있는 거리는 15x km이다.", "VAR": "휘발유가", "XU": " L일 때", "ASK": "갈 수 있는 거리는 몇 km인지", "sc": 4, "off": 0, "iA": 0, "iB": 0, "iC": 0, "iD": 1, "iE": 0, "iF": 0, "iG": 0, "F1": "15 ×", "F2": "", "UNIT": " km", "xmax": 12},
    "alt": {"INTRO": "지면의 기온이 25 °C일 때, 높이가 x km인 곳의 기온은 (25 − 6x) °C이다.", "VAR": "높이가", "XU": " km일 때", "ASK": "그곳의 기온은 몇 °C인지", "sc": 1, "off": 0, "iA": 0, "iB": 0, "iC": 0, "iD": 0, "iE": 1, "iF": 0, "iG": 0, "F1": "25 − 6 ×", "F2": "", "UNIT": " °C", "xmax": 4},
    "taxi": {"INTRO": "어느 택시의 요금은 기본요금 4800원에 1 km를 갈 때마다 1000원씩 더해져 x km를 가면 (4800 + 1000x)원이다.", "VAR": "택시로", "XU": " km를 갈 때", "ASK": "요금은 몇 원인지", "sc": 1, "off": 1, "iA": 0, "iB": 0, "iC": 0, "iD": 0, "iE": 0, "iF": 1, "iG": 0, "F1": "4800 + 1000 ×", "F2": "", "UNIT": "원", "xmax": 14},
    "speed": {"INTRO": "시속 80 km로 달리는 고속버스가 x시간 동안 달린 거리는 80x km이다.", "VAR": "이 버스가", "XU": "시간 동안 달렸을 때", "ASK": "달린 거리는 몇 km인지", "sc": 1, "off": 0, "iA": 0, "iB": 0, "iC": 0, "iD": 0, "iE": 0, "iF": 0, "iG": 1, "F1": "80 ×", "F2": "", "UNIT": " km", "xmax": 9},
}


def ev_t3():
    return tpl(EV, 3, EV_BASE,
        title="공식에 값을 대입하기 — 소리의 속력·화씨온도·할인 가격·연비·기온·택시 요금·거리",
        skill="실생활 공식(문자를 사용한 식)에 주어진 값을 대입해 식의 값을 구하기",
        variant_axis={"공식": "소리 속력 / 화씨 / 할인 가격 / 연비 / 기온", "대입값": "공식별 범위"},
        discriminates="식의 문자 자리에 값을 바르게 대입하고 소수·괄호 계산을 정확히 하는가",
        difficulty=2, context="생활맥락", process="문제해결",
        params=[{"name": "f", "values": {"in": list(FORM_ROWS)}}, {"name": "x", "values": {"int": [1, 14]}}],
        table={"key": "f", "rows": FORM_ROWS},
        derive={"X": "sc*x + off", "ans": "iA*(331 + 3*(sc*x + off)/5) + iB*(9*(sc*x + off)/5 + 32) + iC*(4*(sc*x + off)/5) + iD*(15*(sc*x + off)) + iE*(25 - 6*(sc*x + off)) + iF*(4800 + 1000*(sc*x + off)) + iG*(80*(sc*x + off))"},
        constraints=["x <= xmax", "X != 0", "ans != X", "not (ans in (331, 32, 20, 25, 6, 15, 80, 1000, 4800))", "ans > 0"],
        cost_values=["X", "ans"],
        answer_var="ans",
        verify=["ans == iA*(331 + 3*X/5) + iB*(9*X/5 + 32) + iC*(4*X/5) + iD*(15*X) + iE*(25 - 6*X) + iF*(4800 + 1000*X) + iG*(80*X)"],
        question="{INTRO} {VAR} {X}{XU} {ASK} 구하시오.",
        answer="{ans}", answer_alt=["{ans}{UNIT}"],
        sol1="공식은 문자를 사용한 식이므로, 문자 자리에 주어진 값 {X}{eul(X)} 대입하면 식의 값이 곧 답이다. 소수 계수는 그대로 곱하고, 곱셈을 덧셈·뺄셈보다 먼저 계산한다.",
        sol2=[
            "식의 문자 자리에 {X}{eul(X)} 대입한다.",
            "{F1} {X}{F2} = {ans}",
            "따라서 구하는 값은 {ans}{UNIT}이다.",
        ],
        sol2_fig=steps([
            {"text": "문자 자리에 {X} 대입", "hint": "단위는 식과 같게"},
            {"text": "{F1} {X}{F2} = {ans}", "hint": "곱셈 먼저", "marks": [{"on": "{ans}", "note": "단위 {UNIT}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], []],
        sol3="대입한 값 {X}{ika(X)} 문자의 뜻(단위)에 맞는지 확인하고 다시 계산해도 {F1} {X}{F2} = {ans}이다. 따라서 답은 {ans}{UNIT}이다.",
        sol3_fig=steps(["{F1} {X}{F2} = {ans}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="식에 {X}{eul(X)} 대입하면 {F1} {X}{F2} = {ans}이므로 구하는 값은 {ans}{UNIT}이다.",
        rubric=[
            {"element": "대입", "points": 2, "criterion": "공식의 문자 자리에 {X}{eul(X)} 바르게 대입했다.", "partial": "다른 문자 자리에 대입했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 3, "criterion": "계산하여 {ans}{UNIT}{eul(UNIT)} 구했다.", "partial": "대입은 옳고 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


TWO_ROWS = {
    "2a-3b": {"FORM": "2a − 3b", "c4": 2, "c5": -3, "c1": 0, "c2": 0, "c3": 0, "c6": 0, "n1": 2, "n2": 3},
    "ab-a": {"FORM": "ab − a", "c4": -1, "c5": 0, "c1": 0, "c2": 1, "c3": 0, "c6": 0, "n1": 0, "n2": 0},
    "a2-b": {"FORM": "a² − b", "c4": 0, "c5": -1, "c1": 1, "c2": 0, "c3": 0, "c6": 0, "n1": 0, "n2": 0},
    "3a+b2": {"FORM": "3a + b²", "c4": 3, "c5": 0, "c1": 0, "c2": 0, "c3": 1, "c6": 0, "n1": 3, "n2": 0},
    "a2-2ab": {"FORM": "a² − 2ab", "c4": 0, "c5": 0, "c1": 1, "c2": -2, "c3": 0, "c6": 0, "n1": 2, "n2": 0},
    "4a-ab+1": {"FORM": "4a − ab + 1", "c4": 4, "c5": 0, "c1": 0, "c2": -1, "c3": 0, "c6": 1, "n1": 4, "n2": 1},
    "a-b2": {"FORM": "a − b²", "c4": 1, "c5": 0, "c1": 0, "c2": 0, "c3": -1, "c6": 0, "n1": 0, "n2": 0},
    "2ab-3": {"FORM": "2ab − 3", "c4": 0, "c5": 0, "c1": 0, "c2": 2, "c3": 0, "c6": -3, "n1": 2, "n2": 3},
}


def ev_t4():
    return tpl(EV, 4, EV_BASE,
        title="두 문자 a, b에 값을 대입한 식의 값",
        skill="두 문자에 각각의 값을 괄호를 써서 대입하고 곱·제곱을 먼저 계산하기",
        variant_axis={"식": "8가지 (일차·곱·제곱 혼합)", "대입값": "−4~4"},
        discriminates="ab는 곱셈임을 알고 각 문자에 제 값을 대입하는가, 음수의 제곱과 곱의 부호를 바르게 하는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(TWO_ROWS)}}, {"name": "a", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "b", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}],
        table={"key": "f", "rows": TWO_ROWS},
        derive={"ans": "c1*a*a + c2*a*b + c3*b*b + c4*a + c5*b + c6"},
        constraints=["a != b", "ans != a", "ans != b", "ans != n1", "ans != n2", "ans != 0"],
        cost_values=["a", "b", "ans"],
        answer_var="ans",
        verify=["ans == c1*a*a + c2*a*b + c3*b*b + c4*a + c5*b + c6"],
        question="a = {a}, b = {b}일 때, {FORM}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="문자가 두 개이면 각 문자 자리에 제 값을 대입한다. 곱셈 기호가 생략된 ab는 a × b이고, 음수는 괄호를 써서 대입한 뒤 거듭제곱 → 곱셈 → 덧셈·뺄셈 순서로 계산한다.",
        sol2=[
            "a = {a}, b = {b}{eul(b)} 대입한다(음수는 괄호).",
            "제곱과 곱셈을 먼저 계산한 뒤 덧셈·뺄셈을 하면 {FORM} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "a → {pn(a)},  b → {pn(b)}", "hint": "각 문자에 제 값, 음수는 괄호"},
            {"text": "{FORM} = {ans}", "hint": "제곱·곱셈 먼저", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="a와 b의 값을 서로 바꿔 대입하지 않았는지, 곱과 제곱의 부호가 맞는지 확인하면 {FORM} = {ans}이다. 답은 {ans}이다.",
        sol3_fig=steps(["a = {a}, b = {b} 확인", "{FORM} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="a = {a}, b = {b}{eul(b)} 대입하면 {FORM} = {ans}이다.",
        rubric=[
            {"element": "대입", "points": 2, "criterion": "a 자리에 {a}, b 자리에 {b}{eul(b)} 괄호를 써서 대입했다.", "partial": "두 값을 바꿔 대입했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 3, "criterion": "제곱·곱셈을 먼저 계산해 {ans}{eul(ans)} 구했다.", "partial": "부호 실수 하나면 1점."},
        ],
        rubric_total=5,
    )


EV_SEED = {
    "seed_id": EV, "category": "연산",
    "title": "식의 값 — 정수 대입·분수 대입·공식 대입·두 문자 대입",
    "unit_id": "m1-1", "concept_ids": ["m1-1-20", "m1-1-21"],
    "schema_id": None, "schema_name": "식의 값 구하기",
    "source_item_ids": [],
    "note": "구조만 차용. 공식 대입은 5가지 실생활 공식(문장은 표, 수치는 파생값)으로, 두 문자 식은 계수 표로 값을 계산한다.",
    "geometry": False,
    "templates": [ev_t1_final(), ev_t2(), ev_t3(), ev_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 일차식의 계산
LE = "m1-1-linear-expr"
LE_BASE = {**BASE, "prereq": ["일차식", "동류항", "분배법칙"], "ops": ["사칙", "동류항"], "tags": ["일차식의 계산", "동류항"]}
QT_ROWS = {"coef": {"QT": "x의 계수", "c1": 1, "c0": 0}, "const": {"QT": "상수항", "c1": 0, "c0": 1}, "sum": {"QT": "x의 계수와 상수항의 합", "c1": 1, "c0": 1}}
SIGN_ROWS = {"plus": {"S2": "+", "s2": 1}, "minus": {"S2": "−", "s2": -1}}
P9 = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def le_t1():
    return tpl(LE, 1, LE_BASE,
        title="괄호가 있는 일차식의 계산 — x의 계수·상수항·그 합",
        skill="분배법칙으로 괄호를 풀고(뺄셈은 괄호 안 모든 항의 부호를 바꿈) 동류항끼리 모으기",
        variant_axis={"구하는 것": "x의 계수 / 상수항 / 합", "계수": "±2~±4"},
        discriminates="괄호 앞의 음수·뺄셈을 괄호 안 모든 항에 적용하는가, 동류항만 모으는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(QT_ROWS)}}, {"name": "p", "values": {"in": [-4, -3, -2, 2, 3, 4]}}, {"name": "q", "values": {"in": NZ}},
                {"name": "r", "values": {"int": [2, 4]}}, {"name": "s", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "t", "values": {"in": NZ}}],
        table={"key": "q1", "rows": QT_ROWS},
        derive={"A": "p - r*s", "B": "p*q - r*t", "e1": "p*q", "e2": "-r*s", "e3": "-r*t", "ans": "c1*(p - r*s) + c0*(p*q - r*t)"},
        constraints=["A != 0", "B != 0", "ans != 0", "ans != p", "ans != q", "ans != r", "ans != s", "ans != t", "abs(A) != 1 or c1 == 0"],
        cost_values=["p", "q", "r", "s", "t", "A", "B", "ans"],
        answer_var="ans",
        verify=["ans == c1*(p - r*s) + c0*(p*q - r*t)"],
        question="{p}(x {sgn(q)}) − {r}({co(s)}x {sgn(t)}){eul(t)} 간단히 하였을 때, {QT}{eul(QT)} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="괄호 앞의 수를 괄호 안의 모든 항에 곱해 괄호를 푼다(분배법칙). 특히 '− {r}(…)'는 괄호 안의 각 항에 −{r}{eul(r)} 곱하는 것이므로 두 항의 부호가 모두 바뀐다. 그다음 x가 있는 항끼리, 상수항끼리(동류항) 모아 간단히 한 뒤 {QT}{eul(QT)} 읽는다.",
        sol2=[
            "{p}(x {sgn(q)}) = {co(p)}x {sgn(e1)}",
            "− {r}({co(s)}x {sgn(t)}) = {sgn(e2)}x {sgn(e3)}",
            "동류항끼리 모으면 ({p} {sgn(e2)})x + ({e1} {sgn(e3)}) = {co(A)}x {sgn(B)}",
            "따라서 {QT}{eun(QT)} {ans}이다.",
        ],
        sol2_fig=steps([
            {"text": "{p}(x {sgn(q)}) = {co(p)}x {sgn(e1)}", "hint": "분배법칙"},
            {"text": "− {r}({co(s)}x {sgn(t)}) = {sgn(e2)}x {sgn(e3)}", "hint": "−{r}{eul(r)} 두 항 모두에", "marks": [{"on": "{sgn(e3)}", "note": "부호 바뀜"}]},
            {"text": "= {co(A)}x {sgn(B)}", "hint": "동류항 정리"},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="x = 1을 넣어 확인하면 원래 식은 {p} × (1 {sgn(q)}) − {r} × ({s} {sgn(t)}) = {p*(1 + q) - r*(s + t)}, 간단히 한 식은 {A} {sgn(B)} = {A + B}{ro(A + B)} 같다. 따라서 {QT}{eun(QT)} {ans}이다.",
        sol3_fig=steps(["x = 1: {p} × (1 {sgn(q)}) − {r} × ({s} {sgn(t)}) = {p*(1 + q) - r*(s + t)}", "{co(A)}x {sgn(B)} → {A} {sgn(B)} = {A + B}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{p}(x {sgn(q)}) − {r}({co(s)}x {sgn(t)}) = {co(p)}x {sgn(e1)} {sgn(e2)}x {sgn(e3)} = {co(A)}x {sgn(B)}이므로 {QT}{eun(QT)} {ans}이다.",
        rubric=[
            {"element": "괄호 풀기", "points": 3, "criterion": "분배법칙으로 두 괄호를 풀어 {co(p)}x {sgn(e1)} {sgn(e2)}x {sgn(e3)}{eul(e3)} 얻었다.", "partial": "− {r}{eul(r)} 뒤 항에 곱하지 않거나 부호를 바꾸지 않았으면 1점."},
            {"element": "동류항 정리", "points": 2, "criterion": "동류항끼리 모아 {co(A)}x {sgn(B)}{ro(B)} 간단히 했다.", "partial": "x항과 상수항을 섞어 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} {ans}{eul(ans)} 답했다.", "partial": "다른 것(계수·상수항)을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def le_t2():
    return tpl(LE, 2, LE_BASE,
        title="분수 계수가 있는 일차식의 계산 — x의 계수·상수항·그 합",
        skill="분수를 괄호 안의 각 항에 곱해(약분) 정수 계수로 만든 뒤 동류항끼리 모으기",
        variant_axis={"구하는 것": "x의 계수 / 상수항 / 합", "가운데 부호": "+ / −"},
        discriminates="분수를 괄호 안 모든 항에 곱하고 약분하는가, 뺄셈일 때 뒤 괄호의 부호를 모두 바꾸는가",
        difficulty=3,
        params=[{"name": "q1", "values": {"in": list(QT_ROWS)}}, {"name": "sg", "values": {"in": list(SIGN_ROWS)}},
                {"name": "a", "values": {"int": [1, 3]}}, {"name": "b", "values": {"in": [2, 3, 4]}}, {"name": "cc", "values": {"int": [1, 3]}}, {"name": "dd", "values": {"in": [-3, -2, -1, 1, 2, 3]}},
                {"name": "e", "values": {"int": [1, 3]}}, {"name": "f", "values": {"in": [2, 3, 5]}}, {"name": "gg", "values": {"int": [1, 3]}}, {"name": "hh", "values": {"in": [-3, -2, -1, 1, 2, 3]}}],
        table=[{"key": "q1", "rows": QT_ROWS}, {"key": "sg", "rows": SIGN_ROWS}],
        derive={"c": "b*cc", "d": "b*dd", "g": "f*gg", "h": "f*hh", "u1": "a*cc", "u0": "a*dd", "v1": "s2*e*gg", "v0": "s2*e*hh", "A": "a*cc + s2*e*gg", "B": "a*dd + s2*e*hh", "ans": "c1*(a*cc + s2*e*gg) + c0*(a*dd + s2*e*hh)"},
        constraints=["gcd(a, b) == 1", "a < b", "gcd(e, f) == 1", "e < f", "A != 0", "B != 0", "abs(v1) != 1", "ans != 0", "ans != c", "ans != d", "ans != g", "ans != h", "ans != a", "ans != b", "ans != e", "ans != f", "abs(A) != 1 or c1 == 0"],
        cost_values=["a", "b", "c", "d", "e", "f", "g", "h", "A", "B", "ans"],
        answer_var="ans",
        verify=["ans == c1*A + c0*B", "A == a*c/b + s2*e*g/f", "B == a*d/b + s2*e*h/f"],
        question="[[frac({a},{b})]]({c}x {sgn(d)}) {S2} [[frac({e},{f})]]({g}x {sgn(h)}){eul(h)} 간단히 하였을 때, {QT}{eul(QT)} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분수 계수도 분배법칙은 같다 — 괄호 안의 각 항에 분수를 곱하고 약분해 정수로 만든다. 뒤 괄호 앞이 '{S2}'이므로 그 괄호의 각 항에는 {S2}[[frac({e},{f})]]{eul(f)} 곱한다. 그런 다음 동류항끼리 모아 {QT}{eul(QT)} 읽는다.",
        sol2=[
            "[[frac({a},{b})]]({c}x {sgn(d)}) = {co(u1)}x {sgn(u0)}",
            "{S2} [[frac({e},{f})]]({g}x {sgn(h)}) = {sgn(v1)}x {sgn(v0)}",
            "동류항끼리 모으면 {co(A)}x {sgn(B)}",
            "따라서 {QT}{eun(QT)} {ans}이다.",
        ],
        sol2_fig=steps([
            {"text": "[[frac({a},{b})]] × {c}x = {co(u1)}x,  [[frac({a},{b})]] × {pn(d)} = {u0}", "hint": "약분"},
            {"text": "{S2} [[frac({e},{f})]] × {g}x = {sgn(v1)}x,  {S2} [[frac({e},{f})]] × {pn(h)} = {sgn(v0)}", "hint": "뒤 괄호는 부호까지"},
            {"text": "= {co(A)}x {sgn(B)}", "hint": "동류항 정리"},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="x = 0을 넣으면 원래 식은 [[frac({a},{b})]] × {pn(d)} {S2} [[frac({e},{f})]] × {pn(h)} = {B}{ro(B)} 상수항 {B}{wa(B)} 같고, x의 계수도 {u1} {sgn(v1)} = {A}{ro(A)} 맞는다. 따라서 {QT}{eun(QT)} {ans}이다.",
        sol3_fig=steps(["x = 0: [[frac({a},{b})]] × {pn(d)} {S2} [[frac({e},{f})]] × {pn(h)} = {B}", "x의 계수: {u1} {sgn(v1)} = {A}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({a},{b})]]({c}x {sgn(d)}) {S2} [[frac({e},{f})]]({g}x {sgn(h)}) = {co(u1)}x {sgn(u0)} {sgn(v1)}x {sgn(v0)} = {co(A)}x {sgn(B)}이므로 {QT}{eun(QT)} {ans}이다.",
        rubric=[
            {"element": "괄호 풀기", "points": 3, "criterion": "분수를 각 항에 곱해 {co(u1)}x {sgn(u0)} {sgn(v1)}x {sgn(v0)}{eul(v0)} 얻었다.", "partial": "약분 실수 하나면 2점, 뒤 괄호의 부호를 바꾸지 않았으면 1점."},
            {"element": "동류항 정리", "points": 2, "criterion": "동류항끼리 모아 {co(A)}x {sgn(B)}{ro(B)} 간단히 했다.", "partial": "x항과 상수항을 섞었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} {ans}{eul(ans)} 답했다.", "partial": "다른 것을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


WR_ROWS = {"as": {"PRE": "에", "OPC": "더해야", "OPW": "뺐더니", "S1": "−", "S2": "+", "S3": "+", "i": 1, "WR": "뺀", "CR": "더한"},
           "sa": {"PRE": "에서", "OPC": "빼야", "OPW": "더했더니", "S1": "+", "S2": "−", "S3": "−", "i": -1, "WR": "더한", "CR": "뺀"}}


def le_t3():
    return tpl(LE, 3, LE_BASE,
        title="어떤 식에 일차식을 잘못 더하거나 뺀 결과로 바르게 계산한 식 구하기",
        skill="어떤 식을 A로 놓아 잘못된 계산을 식으로 세우고, 역연산으로 A를 구한 뒤 바르게 계산하기",
        variant_axis={"잘못한 연산": "더함→뺌 / 뺌→더함", "계수": "±1~±6"},
        discriminates="어떤 식을 미지의 식으로 두고 역연산하는가, 괄호를 붙여 빼면서 두 항의 부호를 모두 바꾸는가",
        difficulty=3, process="문제해결",
        params=[{"name": "w", "values": {"in": list(WR_ROWS)}}, {"name": "a1", "values": {"in": NZ}}, {"name": "a0", "values": {"in": P9}}, {"name": "b1", "values": {"in": NZ}}, {"name": "b0", "values": {"in": P9}}],
        table={"key": "w", "rows": WR_ROWS},
        derive={"x1": "b1 + i*a1", "x0": "b0 + i*a0", "r1": "b1 + 2*i*a1", "r0": "b0 + 2*i*a0"},
        constraints=["x1 != 0", "x0 != 0", "r1 != 0", "r0 != 0", "a1 != b1", "abs(r1) <= 12", "abs(r0) <= 20"],
        cost_values=["a1", "a0", "b1", "b0", "x1", "x0", "r1", "r0"],
        verify=["r1 == b1 + 2*i*a1", "r0 == b0 + 2*i*a0", "x1 + i*a1 == r1"],
        question="어떤 식{PRE} {co(a1)}x {sgn(a0)}{eul(a0)} {OPC} 할 것을 잘못하여 {co(a1)}x {sgn(a0)}{eul(a0)} {OPW} {co(b1)}x {sgn(b0)}{ika(b0)} 되었다. 바르게 계산한 식을 구하시오.",
        answer="{co(r1)}x {sgn(r0)}", answer_alt=[],
        sol1="어떤 식을 A라 하고 잘못 계산한 과정을 그대로 식으로 쓰면 A {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}이다. 이 식에서 A를 구한 다음(역연산 — 괄호를 붙여 {S2} 한다), 원래 하려던 바른 계산 A {S3} ({co(a1)}x {sgn(a0)}){eul(a0)} 한다. 잘못 계산한 결과를 답으로 쓰지 않도록 한다.",
        sol2=[
            "어떤 식을 A라 하면 잘못 계산한 식은 A {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}",
            "따라서 A = {co(b1)}x {sgn(b0)} {S2} ({co(a1)}x {sgn(a0)}) = {co(x1)}x {sgn(x0)}",
            "바르게 계산하면 ({co(x1)}x {sgn(x0)}) {S3} ({co(a1)}x {sgn(a0)}) = {co(r1)}x {sgn(r0)}",
        ],
        sol2_fig=steps([
            {"text": "A {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}", "hint": "잘못 {WR} 계산"},
            {"text": "A = {co(b1)}x {sgn(b0)} {S2} ({co(a1)}x {sgn(a0)}) = {co(x1)}x {sgn(x0)}", "hint": "역연산 — 괄호 붙여서", "marks": [{"on": "({co(a1)}x {sgn(a0)})", "note": "부호 주의"}]},
            {"text": "({co(x1)}x {sgn(x0)}) {S3} ({co(a1)}x {sgn(a0)}) = {co(r1)}x {sgn(r0)}", "hint": "바르게 {CR} 계산"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="구한 어떤 식 {co(x1)}x {sgn(x0)}{ro(x0)} 잘못 계산한 대로 하면 ({co(x1)}x {sgn(x0)}) {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}{ika(b0)} 되어 조건과 같다. 따라서 바르게 계산한 식은 {co(r1)}x {sgn(r0)}이다.",
        sol3_fig=steps(["({co(x1)}x {sgn(x0)}) {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}  (조건 확인)", "바른 계산: {co(r1)}x {sgn(r0)}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="어떤 식을 A라 하면 A {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}이므로 A = {co(x1)}x {sgn(x0)}이다. 따라서 바르게 계산한 식은 ({co(x1)}x {sgn(x0)}) {S3} ({co(a1)}x {sgn(a0)}) = {co(r1)}x {sgn(r0)}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "어떤 식을 A로 놓고 잘못 계산한 식 A {S1} ({co(a1)}x {sgn(a0)}) = {co(b1)}x {sgn(b0)}{eul(b0)} 세웠다.", "partial": "바른 연산으로 식을 세웠으면 인정하지 않는다."},
            {"element": "어떤 식 구하기", "points": 2, "criterion": "역연산으로 A = {co(x1)}x {sgn(x0)}{eul(x0)} 구했다.", "partial": "괄호 없이 계산해 상수항의 부호가 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "바르게 계산한 식 {co(r1)}x {sgn(r0)}{eul(r0)} 답했다.", "partial": "어떤 식 A를 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def le_t4():
    return tpl(LE, 4, LE_BASE,
        title="직사각형의 둘레의 길이를 x의 식으로 나타내기",
        skill="둘레 = 2 × (가로 + 세로)임을 식으로 세우고 괄호를 풀어 동류항을 정리하기",
        variant_axis={"가로·세로 계수": "1~4", "상수항": "±1~±6"},
        discriminates="둘레를 가로·세로의 합의 2배로 세우는가(넓이·한 번만 더하기와 혼동하지 않는가), 분배법칙을 두 항에 모두 적용하는가",
        difficulty=2, context="기하맥락", process="문제해결",
        params=[{"name": "p", "values": {"int": [1, 4]}}, {"name": "q", "values": {"in": NZ}}, {"name": "r", "values": {"int": [1, 4]}}, {"name": "s", "values": {"in": NZ}}],
        derive={"m1": "p + r", "m0": "q + s", "r1": "2*(p + r)", "r0": "2*(q + s)"},
        constraints=["m0 != 0", "not (p == r and q == s)", "p + q >= 1", "r + s >= 1"],
        cost_values=["p", "q", "r", "s", "r1", "r0"],
        verify=["r1 == 2*(p + r)", "r0 == 2*(q + s)"],
        question="가로의 길이가 ({co(p)}x {sgn(q)}) cm, 세로의 길이가 ({co(r)}x {sgn(s)}) cm인 직사각형의 둘레의 길이를 x를 사용한 식으로 나타내시오.",
        answer="{co(r1)}x {sgn(r0)}", answer_alt=["({co(r1)}x {sgn(r0)}) cm"],
        sol1="직사각형은 가로와 세로가 각각 두 개씩 있으므로 둘레의 길이는 2 × (가로 + 세로)이다. 가로와 세로의 식을 괄호로 묶어 더한 뒤 2를 곱하고, 동류항끼리 정리한다.",
        sol2=[
            "(둘레) = 2 × {{(가로) + (세로)}} = 2 × {{({co(p)}x {sgn(q)}) + ({co(r)}x {sgn(s)})}}",
            "괄호 안을 정리하면 2 × ({co(m1)}x {sgn(m0)})",
            "따라서 둘레의 길이는 ({co(r1)}x {sgn(r0)}) cm이다.",
        ],
        sol2_fig=steps([
            {"text": "2 × {{({co(p)}x {sgn(q)}) + ({co(r)}x {sgn(s)})}}", "hint": "둘레 = 2(가로 + 세로)"},
            {"text": "= 2 × ({co(m1)}x {sgn(m0)})", "hint": "동류항 정리"},
            {"text": "= {co(r1)}x {sgn(r0)}", "hint": "분배법칙", "marks": [{"on": "{sgn(r0)}", "note": "상수항에도 2를 곱한다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="x = 1을 넣으면 가로 {p + q} cm, 세로 {r + s} cm이고 둘레는 2 × ({p + q} + {r + s}) = {2*(p + q + r + s)}, 구한 식에서도 {r1} {sgn(r0)} = {r1 + r0}{ro(r1 + r0)} 같다. 따라서 둘레의 길이는 ({co(r1)}x {sgn(r0)}) cm이다.",
        sol3_fig=steps(["x = 1: 2 × ({p + q} + {r + s}) = {2*(p + q + r + s)}", "{r1} {sgn(r0)} = {r1 + r0}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="(둘레) = 2 × {{({co(p)}x {sgn(q)}) + ({co(r)}x {sgn(s)})}} = 2 × ({co(m1)}x {sgn(m0)}) = {co(r1)}x {sgn(r0)}이므로 둘레의 길이는 ({co(r1)}x {sgn(r0)}) cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "둘레를 2 × {{(가로) + (세로)}}로 세웠다.", "partial": "가로와 세로를 한 번만 더했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "동류항을 정리하고 2를 곱해 {co(r1)}x {sgn(r0)}{eul(r0)} 구했다.", "partial": "상수항에 2를 곱하지 않았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def le_t5():
    return tpl(LE, 5, LE_BASE,
        title="동류항이 흩어진 일차식을 간단히 하기",
        skill="x가 있는 항끼리, 상수항끼리 부호까지 붙여 모아 계수를 더하기",
        variant_axis={"계수": "±1~±9", "항의 수": "4"},
        discriminates="항의 부호를 항에 붙여 옮기고 동류항끼리만 더하는가",
        difficulty=1,
        params=[{"name": "a", "values": {"in": NZ}}, {"name": "b", "values": {"in": P9}}, {"name": "c", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9]}}, {"name": "d", "values": {"in": P9}}],
        derive={"r1": "a + c", "r0": "b + d"},
        constraints=["r1 != 0", "r0 != 0", "abs(r1) <= 12", "abs(r0) <= 15"],
        cost_values=["a", "b", "c", "d", "r1", "r0"],
        verify=["r1 == a + c", "r0 == b + d"],
        question="{co(a)}x {sgn(b)} {sgn(c)}x {sgn(d)}{eul(d)} 간단히 하시오.",
        answer="{co(r1)}x {sgn(r0)}", answer_alt=[],
        sol1="문자와 차수가 같은 항이 동류항이다. x가 있는 항 {co(a)}x와 {sgn(c)}x, 상수항 {sgn(b)}{wa(b)} {sgn(d)}{eul(d)} 각각 부호까지 붙여 모으고 계수끼리 더한다.",
        sol2=[
            "동류항끼리 모으면 ({co(a)}x {sgn(c)}x) + ({b} {sgn(d)})",
            "x의 계수: {a} {sgn(c)} = {r1}, 상수항: {b} {sgn(d)} = {r0}",
            "따라서 {co(r1)}x {sgn(r0)}",
        ],
        sol2_fig=steps([
            {"text": "({co(a)}x {sgn(c)}x) + ({b} {sgn(d)})", "hint": "부호를 항에 붙여서 모은다"},
            {"text": "= ({a} {sgn(c)})x + ({b} {sgn(d)})", "hint": "계수끼리"},
            {"text": "= {co(r1)}x {sgn(r0)}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="x = 1을 넣으면 원래 식은 {a} {sgn(b)} {sgn(c)} {sgn(d)} = {a + b + c + d}, 간단히 한 식은 {r1} {sgn(r0)} = {r1 + r0}{ro(r1 + r0)} 같다. 답은 {co(r1)}x {sgn(r0)}이다.",
        sol3_fig=steps(["x = 1: {a} {sgn(b)} {sgn(c)} {sgn(d)} = {a + b + c + d}", "{r1} {sgn(r0)} = {r1 + r0}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(a)}x {sgn(b)} {sgn(c)}x {sgn(d)} = ({a} {sgn(c)})x + ({b} {sgn(d)}) = {co(r1)}x {sgn(r0)}이다.",
        rubric=[
            {"element": "동류항 모으기", "points": 3, "criterion": "x항끼리, 상수항끼리 부호를 붙여 모았다.", "partial": "부호를 떼고 모았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{co(r1)}x {sgn(r0)}{eul(r0)} 구했다.", "partial": "계수 덧셈 실수 하나면 1점."},
        ],
        rubric_total=5,
    )


LE_SEED = {
    "seed_id": LE, "category": "연산",
    "title": "일차식의 계산 — 괄호 전개·분수 계수·잘못 계산한 식·둘레 식·동류항",
    "unit_id": "m1-1", "concept_ids": ["m1-1-22", "m1-1-23"],
    "schema_id": None, "schema_name": "일차식의 덧셈과 뺄셈",
    "source_item_ids": [],
    "note": "구조만 차용. 식이 답인 틀(t3·t4·t5)은 answer 가 문자열이라 verify 는 파생값끼리 대조하고 recheck.py 가 mathir 로 x = 0, 1 에서 답을 되읽어 검산한다.",
    "geometry": False,
    "templates": [le_t1(), le_t2(), le_t3(), le_t4(), le_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 방정식과 그 해 (항등식·해가 주어질 때 상수)
ES = "m1-1-eq-solution"
ES_BASE = {**BASE, "prereq": ["방정식과 항등식", "등식의 성질", "일차방정식의 풀이"], "ops": ["방정식", "대입"], "traps": ["조건누락", "역연산"], "tags": ["항등식", "방정식의 해"]}
KB_ROWS = {"p1": {"KB": "+ b", "k": 1}, "m1": {"KB": "− b", "k": -1}, "p2": {"KB": "+ 2b", "k": 2}, "m2": {"KB": "− 2b", "k": -2}, "p3": {"KB": "+ 3b", "k": 3}, "m3": {"KB": "− 3b", "k": -3}, "p4": {"KB": "+ 4b", "k": 4}, "m4": {"KB": "− 4b", "k": -4}}
AB_ROWS = {"sum": {"QT": "a + b", "c1": 1, "c2": 1, "cp": 0}, "diff": {"QT": "a − b", "c1": 1, "c2": -1, "cp": 0}, "prod": {"QT": "ab", "c1": 0, "c2": 0, "cp": 1}}


def es_t1():
    return tpl(ES, 1, ES_BASE,
        title="항등식이 되기 위한 상수 a, b — 양변의 계수 비교",
        skill="x에 대한 항등식은 모든 x에서 성립하므로 양변의 x의 계수와 상수항이 각각 같음을 이용하기",
        variant_axis={"구하는 것": "a + b / a − b / ab", "b의 계수": "±1~±4"},
        discriminates="항등식의 뜻(모든 x에서 성립)에서 계수 비교로 넘어가는가, 상수항의 계수(±kb)로 나누어 b를 구하는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(AB_ROWS)}}, {"name": "kb", "values": {"in": list(KB_ROWS)}}, {"name": "c", "values": {"in": NZ}}, {"name": "bv", "values": {"in": NZ}}],
        table=[{"key": "q1", "rows": AB_ROWS}, {"key": "kb", "rows": KB_ROWS}],
        derive={"m": "k*bv", "a": "c", "b": "bv", "ans": "c1*c + c2*bv + cp*c*bv"},
        constraints=["ans != m", "ans != c", "ans != k", "ans != -k", "ans != 0"],
        cost_values=["m", "c", "k", "a", "b", "ans"],
        answer_var="ans",
        verify=["a == c", "k*b == m", "ans == c1*a + c2*b + cp*a*b"],
        question="등식 ax {sgn(m)} = {co(c)}x {KB}가 x에 대한 항등식일 때, 상수 a, b에 대하여 {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x에 대한 항등식은 x에 어떤 값을 넣어도 성립하는 등식이다. 그러려면 양변을 정리했을 때 x의 계수끼리, 상수항끼리 각각 같아야 한다. 좌변 ax {sgn(m)}{wa(m)} 우변 {co(c)}x {KB}에서 x의 계수를 비교해 a를, 상수항을 비교해 b를 구한다.",
        sol2=[
            "x의 계수를 비교하면 a = {c}",
            "상수항을 비교하면 {m} = {co(k)}b, b = {bv}",
            "따라서 {QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "ax {sgn(m)} = {co(c)}x {KB}", "hint": "양변의 계수·상수항이 각각 같다"},
            {"text": "a = {c}", "hint": "x의 계수"},
            {"text": "{co(k)}b = {m}  →  b = {bv}", "hint": "상수항", "marks": [{"on": "{bv}", "note": "{k}{ro(k)} 나눈다"}]},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="a = {c}, b = {bv}{eul(bv)} 넣으면 우변은 {co(c)}x {sgn(m)}{ika(m)} 되어 좌변과 똑같으므로 x에 어떤 값을 넣어도 성립한다. 따라서 {QT} = {ans}이다.",
        sol3_fig=steps(["우변: {co(c)}x + {k} × {pn(bv)} = {co(c)}x {sgn(m)}", "좌변과 같다 → 항등식"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x에 대한 항등식이므로 양변의 x의 계수와 상수항이 각각 같다. a = {c}이고 {co(k)}b = {m}에서 b = {bv}이므로 {QT} = {ans}이다.",
        rubric=[
            {"element": "항등식의 조건", "points": 3, "criterion": "항등식이려면 양변의 x의 계수와 상수항이 각각 같아야 함을 밝혔다.", "partial": "특정 x값만 대입해 풀었으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "a = {c}, b = {bv}{eul(bv)} 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 답했다.", "partial": "a, b만 쓰고 {QT}{eul(QT)} 쓰지 않았으면 1점."},
        ],
        rubric_total=7,
    )


SA_ROWS = {"minus": {"SA": "− a", "sa": -1, "S2": "+"}, "plus": {"SA": "+ a", "sa": 1, "S2": "−"}}


def es_t2():
    return tpl(ES, 2, ES_BASE,
        title="해가 주어진 일차방정식에서 상수항의 상수 a 구하기",
        skill="방정식의 해는 대입하면 등식이 성립하는 값이므로 x에 해를 대입해 a에 대한 방정식으로 풀기",
        variant_axis={"a의 부호": "− a / + a", "해": "−6~6"},
        discriminates="해를 x에 대입하는가(a에 대입하지 않는가), 대입 후 a를 바르게 이항하는가",
        difficulty=2,
        params=[{"name": "sa1", "values": {"in": list(SA_ROWS)}}, {"name": "p", "values": {"in": NZ}}, {"name": "k", "values": {"in": [-6, -5, -4, -3, -2, -1, 2, 3, 4, 5, 6]}}, {"name": "r", "values": {"in": P9}}],
        table={"key": "sa1", "rows": SA_ROWS},
        derive={"pk": "p*k", "a": "(p*k - r)*(-sa)", "ans": "(p*k - r)*(-sa)"},
        constraints=["ans != 0", "ans != r", "ans != k", "ans != p", "ans != pk"],
        cost_values=["p", "k", "r", "ans"],
        answer_var="ans",
        verify=["p*k + sa*ans == r"],
        question="x에 대한 일차방정식 {co(p)}x {SA} = {r}의 해가 x = {k}일 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="방정식의 해란 대입했을 때 등식이 참이 되는 x의 값이다. 그러므로 x = {k}{eul(k)} x 자리에 대입하면 a만 남은 등식이 되고, 그것을 a에 대하여 풀면 된다. a 자리에 {k}{eul(k)} 넣지 않도록 주의한다.",
        sol2=[
            "x = {k}{eul(k)} 대입하면 {p} × {pn(k)} {SA} = {r}, 곧 {pk} {SA} = {r}",
            "a에 대하여 풀면 {sa}a = {r} − {pn(pk)}, 따라서 a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{p} × {pn(k)} {SA} = {r}", "hint": "x 자리에 해 {k} 대입"},
            {"text": "{pk} {SA} = {r}", "hint": "정리"},
            {"text": "a = {ans}", "hint": "{pk}{eul(pk)} 이항", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="a = {ans}{eul(ans)} 넣은 방정식 {co(p)}x {sgn(sa*ans)} = {r}에 x = {k}{eul(k)} 대입하면 {pk} {sgn(sa*ans)} = {r}{ro(r)} 성립한다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["{co(p)}x {sgn(sa*ans)} = {r}에 x = {k} 대입", "{pk} {sgn(sa*ans)} = {r}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="해 x = {k}{eul(k)} 대입하면 {p} × {pn(k)} {SA} = {r}이므로 {pk} {SA} = {r}, a = {ans}이다.",
        rubric=[
            {"element": "해 대입", "points": 3, "criterion": "x = {k}{eul(k)} x 자리에 대입해 {pk} {SA} = {r}{eul(r)} 얻었다.", "partial": "a 자리에 대입했으면 인정하지 않고, 곱셈 실수면 1점."},
            {"element": "a 구하기", "points": 2, "criterion": "a = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def es_t3():
    return tpl(ES, 3, ES_BASE,
        title="해가 주어진 일차방정식에서 x의 계수 a 구하기",
        skill="해를 대입해 a에 대한 일차방정식으로 만들고 양변을 해로 나누어 a 구하기",
        variant_axis={"해": "−6~6", "상수항": "±1~±9"},
        discriminates="ax에 해를 대입해 a × (해)로 쓰는가, 마지막에 해로 나누는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ}}, {"name": "k", "values": {"in": [-6, -5, -4, -3, -2, -1, 2, 3, 4, 5, 6]}}, {"name": "q", "values": {"in": P9}}],
        derive={"r": "a*k + q", "ak": "a*k", "ans": "a"},
        constraints=["ans != q", "ans != r", "ans != k", "r != 0", "r != k", "ak != k"],
        cost_values=["k", "q", "r", "ans"],
        answer_var="ans",
        verify=["ans*k + q == r"],
        question="x에 대한 일차방정식 ax {sgn(q)} = {r}의 해가 x = {k}일 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="해 x = {k}{eul(k)} 방정식의 x 자리에 대입하면 성립해야 한다. ax는 a × x이므로 대입하면 a × {pn(k)}, 곧 {co(k)}a가 되고, 남은 것은 a에 대한 일차방정식이다. 상수항을 이항한 뒤 a의 계수 {k}{ro(k)} 나눈다.",
        sol2=[
            "x = {k}{eul(k)} 대입하면 a × {pn(k)} {sgn(q)} = {r}, 곧 {co(k)}a {sgn(q)} = {r}",
            "상수항을 이항하면 {co(k)}a = {r} − {pn(q)} = {ak}",
            "양변을 {k}{ro(k)} 나누면 a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "a × {pn(k)} {sgn(q)} = {r}", "hint": "x 자리에 해 {k} 대입"},
            {"text": "{co(k)}a = {r} − {pn(q)} = {ak}", "hint": "이항"},
            {"text": "a = {ak} ÷ {pn(k)} = {ans}", "hint": "계수로 나누기", "marks": [{"on": "{ans}", "note": "{k}{ro(k)} 나눈다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="a = {ans}{eul(ans)} 넣은 방정식 {co(ans)}x {sgn(q)} = {r}에 x = {k}{eul(k)} 대입하면 {ak} {sgn(q)} = {r}{ro(r)} 성립한다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["{co(ans)}x {sgn(q)} = {r}에 x = {k} 대입", "{ak} {sgn(q)} = {r}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = {k}{eul(k)} 대입하면 {co(k)}a {sgn(q)} = {r}이므로 {co(k)}a = {ak}, a = {ans}이다.",
        rubric=[
            {"element": "해 대입", "points": 3, "criterion": "x = {k}{eul(k)} 대입해 {co(k)}a {sgn(q)} = {r}{eul(r)} 얻었다.", "partial": "ax를 a + {pn(k)}처럼 잘못 대입했으면 인정하지 않는다."},
            {"element": "a 구하기", "points": 2, "criterion": "이항하고 {k}{ro(k)} 나누어 a = {ans}{eul(ans)} 구했다.", "partial": "이항까지 옳고 나눗셈 실수면 1점."},
        ],
        rubric_total=5,
    )


def es_t4():
    return tpl(ES, 4, ES_BASE,
        title="해가 서로 같은 두 일차방정식 — 상수 a 구하기",
        skill="상수가 없는 방정식을 먼저 풀어 해를 구한 뒤, 그 해를 다른 방정식에 대입해 a 구하기",
        variant_axis={"해": "−6~6", "계수": "±2~±6"},
        discriminates="어느 방정식을 먼저 풀어야 하는지 판단하고, 구한 해를 다른 방정식의 x에 대입하는가",
        difficulty=3,
        params=[{"name": "x0", "values": {"in": NZ}}, {"name": "p", "values": {"in": NZ2}}, {"name": "q", "values": {"in": P9}}, {"name": "s", "values": {"in": NZ2}}, {"name": "t", "values": {"in": P9}}],
        derive={"r": "p*x0 + q", "sx": "s*x0", "ans": "s*x0 - t"},
        constraints=["ans != 0", "ans != q", "ans != r", "ans != t", "ans != x0", "ans != p", "ans != s", "r != 0", "abs(r) <= 40"],
        cost_values=["p", "q", "r", "s", "t", "x0", "ans"],
        answer_var="ans",
        verify=["p*x0 + q == r", "s*x0 - ans == t"],
        question="두 일차방정식 {co(p)}x {sgn(q)} = {r}, {co(s)}x − a = {t}의 해가 서로 같을 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 방정식의 해가 같으므로, 상수 a가 없는 첫 번째 방정식을 풀어 해를 구하면 그 값이 두 번째 방정식의 해이기도 하다. 구한 해를 두 번째 방정식의 x에 대입해 a를 구한다.",
        sol2=[
            "{co(p)}x {sgn(q)} = {r}에서 {co(p)}x = {r} − {pn(q)} = {p*x0}, x = {x0}",
            "이 해를 {co(s)}x − a = {t}에 대입하면 {s} × {pn(x0)} − a = {t}, {sx} − a = {t}",
            "따라서 a = {sx} − {pn(t)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}x = {p*x0}  →  x = {x0}", "hint": "a가 없는 방정식부터"},
            {"text": "{s} × {pn(x0)} − a = {t}", "hint": "해를 대입"},
            {"text": "a = {sx} − {pn(t)} = {ans}", "marks": [{"on": "{ans}", "note": "이항 부호"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="a = {ans}이면 두 번째 방정식은 {co(s)}x {sgn(-ans)} = {t}이고 x = {x0}{eul(x0)} 넣으면 {sx} {sgn(-ans)} = {t}{ro(t)} 성립한다. 첫 번째 방정식도 x = {x0}에서 {p*x0} {sgn(q)} = {r}{ro(r)} 성립하므로 두 해가 같다. 답은 {ans}이다.",
        sol3_fig=steps(["x = {x0}: {p*x0} {sgn(q)} = {r}  ✓", "x = {x0}: {sx} {sgn(-ans)} = {t}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(p)}x {sgn(q)} = {r}을 풀면 x = {x0}이고, 이것이 {co(s)}x − a = {t}의 해이므로 {sx} − a = {t}, a = {ans}이다.",
        rubric=[
            {"element": "첫 방정식의 해", "points": 3, "criterion": "{co(p)}x {sgn(q)} = {r}{eul(r)} 풀어 x = {x0}{eul(x0)} 구했다.", "partial": "이항 부호 실수면 1점."},
            {"element": "해 대입", "points": 2, "criterion": "x = {x0}{eul(x0)} 두 번째 방정식에 대입해 {sx} − a = {t}{eul(t)} 얻었다.", "partial": "a 자리에 대입했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=7,
    )


ES_SEED = {
    "seed_id": ES, "category": "연산",
    "title": "방정식과 그 해 — 항등식의 계수·해가 주어진 방정식의 상수·해가 같은 두 방정식",
    "unit_id": "m1-1", "concept_ids": ["m1-1-24", "m1-1-26"],
    "schema_id": None, "schema_name": "항등식과 방정식의 해",
    "source_item_ids": [],
    "note": "구조만 차용. 해·상수를 먼저 뽑고 문면의 상수항을 파생해 정수해를 보장한다.",
    "geometry": False,
    "templates": [es_t1(), es_t2(), es_t3(), es_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 4. 해의 조건 → 상수
LC = "m1-1-linear-eq-const"
LC_BASE = {**ES_BASE, "tags": ["일차방정식의 해", "상수 구하기"]}


def lc_t1():
    return tpl(LC, 1, LC_BASE,
        title="한 방정식의 해가 다른 방정식의 해의 m배일 때 상수 a",
        skill="상수가 없는 방정식의 해를 구하고 배수 관계로 다른 방정식의 해를 정한 뒤 대입해 a 구하기",
        variant_axis={"배수": "2 / 3", "해": "−6~6"},
        discriminates="'A의 해가 B의 해의 m배'에서 어느 해를 m으로 나누는지(방향)를 바르게 잡는가",
        difficulty=3,
        params=[{"name": "m", "values": {"in": [2, 3]}}, {"name": "x2", "values": {"in": NZ}}, {"name": "p", "values": {"in": NZ2}}, {"name": "q", "values": {"in": P9}}, {"name": "s", "values": {"in": NZ2}}, {"name": "t", "values": {"in": P9}}],
        derive={"x1": "m*x2", "r": "p*m*x2 + q", "sx": "s*x2", "ans": "t - s*x2"},
        constraints=["ans != 0", "ans != q", "ans != r", "ans != t", "ans != m", "ans != p", "ans != s", "abs(r) <= 60", "r != 0"],
        cost_values=["m", "p", "q", "r", "s", "t", "x1", "x2", "ans"],
        answer_var="ans",
        verify=["p*x1 + q == r", "x1 == m*x2", "s*x2 + ans == t"],
        question="x에 대한 일차방정식 {co(p)}x {sgn(q)} = {r}의 해가 일차방정식 {co(s)}x + a = {t}의 해의 {m}배일 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="a가 없는 첫 번째 방정식은 바로 풀 수 있다. 그 해가 두 번째 방정식의 해의 {m}배이므로, 두 번째 방정식의 해는 첫 번째 해를 {m}{ro(m)} 나눈 값이다. 이 값을 두 번째 방정식에 대입해 a를 구한다 — {m}{eul(m)} 곱하는지 나누는지 방향을 잘 잡아야 한다.",
        sol2=[
            "{co(p)}x {sgn(q)} = {r}에서 {co(p)}x = {p*x1}, x = {x1}",
            "두 번째 방정식의 해는 {x1} ÷ {m} = {x2}",
            "x = {x2}{eul(x2)} {co(s)}x + a = {t}에 대입하면 {s} × {pn(x2)} + a = {t}, {sx} + a = {t}",
            "따라서 a = {t} − {pn(sx)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}x = {p*x1}  →  x = {x1}", "hint": "첫 방정식의 해"},
            {"text": "두 번째 해 = {x1} ÷ {m} = {x2}", "hint": "'{m}배'이므로 나눈다", "marks": [{"on": "{x2}", "note": "곱하지 말 것"}]},
            {"text": "{sx} + a = {t}  →  a = {ans}", "hint": "대입"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], []],
        sol3="a = {ans}이면 두 번째 방정식은 {co(s)}x {sgn(ans)} = {t}, 해는 x = {x2}이고 첫 번째 방정식의 해 {x1}{eun(x1)} 그 {m}배({x2} × {m} = {x1})가 맞다. 답은 {ans}이다.",
        sol3_fig=steps(["{co(s)}x {sgn(ans)} = {t}  →  x = {x2}", "{x2} × {m} = {x1}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(p)}x {sgn(q)} = {r}의 해는 x = {x1}이고, 두 번째 방정식의 해는 그 [[frac(1,{m})]]인 x = {x2}이다. 이를 {co(s)}x + a = {t}에 대입하면 {sx} + a = {t}이므로 a = {ans}이다.",
        rubric=[
            {"element": "첫 방정식의 해", "points": 3, "criterion": "{co(p)}x {sgn(q)} = {r}{eul(r)} 풀어 x = {x1}{eul(x1)} 구했다.", "partial": "이항 부호 실수면 1점."},
            {"element": "배수 관계", "points": 2, "criterion": "두 번째 방정식의 해가 {x1} ÷ {m} = {x2}임을 밝혔다.", "partial": "{m}{eul(m)} 곱해 {m*x1}{ro(m*x1)} 놓았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "x = {x2}{eul(x2)} 대입해 a = {ans}{eul(ans)} 구했다.", "partial": "대입은 옳고 이항 실수면 1점."},
        ],
        rubric_total=7,
    )


def lc_t2():
    return tpl(LC, 2, LC_BASE,
        title="해가 자연수가 되게 하는 두 자리 자연수 a의 개수",
        skill="해를 a의 식으로 나타내어 자연수가 될 조건(분자가 계수의 배수)을 찾고 범위 안에서 개수 세기",
        variant_axis={"계수": "2~9", "상수": "1~9"},
        discriminates="해 x = (a + q)/p 가 자연수이려면 a + q 가 p 의 배수임을 알고, 두 자리 범위에서 빠짐없이 세는가",
        difficulty=4,
        params=[{"name": "p", "values": {"int": [2, 9]}}, {"name": "q", "values": {"int": [1, 9]}}],
        derive={"lo": "10 + q", "hi": "99 + q", "ans": "floor((99 + q)/p) - floor((9 + q)/p)", "f1": "p*(floor((9 + q)/p) + 1)", "fL": "p*floor((99 + q)/p)"},
        constraints=["ans != p", "ans != q", "ans != 10", "ans != 99"],
        cost_values=["p", "q", "ans"],
        answer_var="ans",
        verify=["ans == floor((99 + q)/p) - floor((9 + q)/p)", "f1 >= lo", "fL <= hi"],
        question="x에 대한 일차방정식 {p}x − {q} = a의 해가 자연수가 되도록 하는 두 자리 자연수 a는 모두 몇 개인지 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="먼저 해를 a로 나타낸다: {p}x = a + {q}, x = (a + {q})/{p}. 이것이 자연수이려면 a + {q}{ika(q)} {p}의 배수여야 한다. a가 두 자리 자연수이므로 a + {q}{eun(q)} {lo}부터 {hi}까지이고, 그 범위 안의 {p}의 배수의 개수를 세면 된다.",
        sol2=[
            "{p}x − {q} = a에서 {p}x = a + {q}, x = (a + {q}) ÷ {p}",
            "x가 자연수이려면 a + {q}{ika(q)} {p}의 배수여야 한다.",
            "10 ≤ a ≤ 99이므로 {lo} ≤ a + {q} ≤ {hi}이고, 이 범위의 {p}의 배수는 {f1}, {f1 + p}, …, {fL}",
            "그 개수는 {ans}이므로 구하는 a는 모두 {ans}개이다.",
        ],
        sol2_fig=steps([
            {"text": "x = (a + {q}) ÷ {p}", "hint": "해를 a로 나타낸다"},
            {"text": "a + {q} = {p}의 배수", "hint": "자연수 조건"},
            {"text": "{lo} ≤ a + {q} ≤ {hi}  →  {f1}, …, {fL}", "hint": "두 자리 범위로 옮긴다", "marks": [{"on": "{fL}", "note": "끝값 확인"}]},
            {"text": "개수 = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="가장 작은 경우 a = {f1 - q}이면 x = {f1/p}, 가장 큰 경우 a = {fL - q}이면 x = {fL/p}{ro(fL/p)} 모두 자연수이고, a는 {p}씩 커지므로 개수는 ({fL} − {f1}) ÷ {p} + 1 = {ans}이다. 답은 {ans}개다.",
        sol3_fig=steps(["a = {f1 - q}: x = {f1/p},   a = {fL - q}: x = {fL/p}", "({fL} − {f1}) ÷ {p} + 1 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = (a + {q}) ÷ {p}이므로 x가 자연수이려면 a + {q}{ika(q)} {p}의 배수여야 한다. 10 ≤ a ≤ 99에서 a + {q}{eun(q)} {lo} 이상 {hi} 이하이고 이 범위의 {p}의 배수는 {f1}부터 {fL}까지 {ans}개이다. 따라서 a는 모두 {ans}개다.",
        rubric=[
            {"element": "해를 a로 나타내기", "points": 2, "criterion": "x = (a + {q}) ÷ {p}{ro(p)} 나타냈다.", "partial": "부호 실수(a − {q})면 1점."},
            {"element": "자연수 조건", "points": 3, "criterion": "a + {q}{ika(q)} {p}의 배수여야 함을 밝히고 두 자리 범위 {lo} ≤ a + {q} ≤ {hi}{ro(hi)} 옮겼다.", "partial": "배수 조건만 쓰고 범위를 옮기지 않았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "범위 안의 {p}의 배수를 세어 {ans}개를 답했다.", "partial": "끝값 하나를 빠뜨리거나 더 셌으면 1점."},
        ],
        rubric_total=7,
    )


def lc_t3():
    return tpl(LC, 3, LC_BASE,
        title="해가 없는 x에 대한 방정식 — 상수 a 구하기",
        skill="ax = b 꼴로 정리했을 때 해가 없으려면 x의 계수가 0이고 상수항이 0이 아니어야 함을 이용하기",
        variant_axis={"계수": "±2~±6", "a의 이동": "a ± k"},
        discriminates="해가 없을 조건을 '양변의 x의 계수가 같고 상수항이 다르다'로 옮기고, (a ± k) = p 에서 a를 구하는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": NZ2}}, {"name": "q", "values": {"in": P9}}, {"name": "k", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "r", "values": {"in": P9}}],
        derive={"ans": "p - k"},
        constraints=["q != r", "ans != 0", "ans != p", "ans != q", "ans != k", "ans != r", "ans != -k"],
        cost_values=["p", "q", "k", "r", "ans"],
        answer_var="ans",
        verify=["ans + k == p", "q != r"],
        question="x에 대한 방정식 {co(p)}x {sgn(q)} = (a {sgn(k)})x {sgn(r)}의 해가 없을 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="방정식을 (x의 계수)x = (상수) 꼴로 정리했을 때, x의 계수가 0이고 우변의 상수가 0이 아니면 어떤 x를 넣어도 0 = (0이 아닌 수)가 되어 해가 없다. 즉 양변의 x의 계수는 같고 상수항은 달라야 한다. 상수항 {q}{wa(q)} {r}{eun(r)} 이미 다르므로 x의 계수만 같게 놓는다.",
        sol2=[
            "우변의 항을 좌변으로 이항하면 {{{p} − (a {sgn(k)})}}x = {r} − {pn(q)}",
            "해가 없으려면 x의 계수가 0이고 상수 {r - q}{eun(r - q)} 0이 아니어야 하므로 {p} − (a {sgn(k)}) = 0",
            "따라서 a {sgn(k)} = {p}, a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{{{p} − (a {sgn(k)})}}x = {r - q}", "hint": "(계수)x = (상수) 꼴"},
            {"text": "{p} − (a {sgn(k)}) = 0,  {r - q} ≠ 0", "hint": "해 없음: 계수 0, 상수 ≠ 0", "marks": [{"on": "{r - q} ≠ 0", "note": "이 조건도 확인"}]},
            {"text": "a {sgn(k)} = {p}  →  a = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="a = {ans}이면 우변은 ({ans} {sgn(k)})x {sgn(r)} = {co(p)}x {sgn(r)}{ika(r)} 되어 방정식은 {co(p)}x {sgn(q)} = {co(p)}x {sgn(r)}, 곧 {q} = {r}{ika(r)} 되는데 이는 거짓이므로 해가 없다. 답은 {ans}이다.",
        sol3_fig=steps(["a = {ans}: {co(p)}x {sgn(q)} = {co(p)}x {sgn(r)}", "{q} = {r}  (거짓) → 해 없음"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="이항하여 정리하면 {{{p} − (a {sgn(k)})}}x = {r - q}이고, 해가 없으려면 x의 계수가 0이어야 하므로 {p} − (a {sgn(k)}) = 0, a = {ans}이다(상수 {r - q}{eun(r - q)} 0이 아니다).",
        rubric=[
            {"element": "해가 없을 조건", "points": 3, "criterion": "(계수)x = (상수) 꼴에서 계수가 0이고 상수가 0이 아니어야 함을 밝혔다.", "partial": "계수 조건만 쓰고 상수 조건을 확인하지 않았으면 2점."},
            {"element": "답 구하기", "points": 2, "criterion": "a {sgn(k)} = {p}에서 a = {ans}{eul(ans)} 구했다.", "partial": "a = {p}{ro(p)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


KB2_ROWS = {"p1": {"KB": "+ b", "kb": 1}, "m1": {"KB": "− b", "kb": -1}, "p2": {"KB": "+ 2b", "kb": 2}, "m2": {"KB": "− 2b", "kb": -2}, "p3": {"KB": "+ 3b", "kb": 3}, "m3": {"KB": "− 3b", "kb": -3}}


def lc_t4():
    return tpl(LC, 4, LC_BASE,
        title="해가 무수히 많은 x에 대한 방정식 — a, b로 만든 식의 값",
        skill="해가 무수히 많으려면 양변이 똑같은 식(항등식)이어야 함을 알고 계수와 상수항을 각각 비교하기",
        variant_axis={"구하는 것": "a + b / a − b / ab", "b의 계수": "±1~±3"},
        discriminates="해가 무수히 많음 = 항등식으로 옮기는가, 상수항 비교에서 b의 계수로 나누는가",
        difficulty=3,
        params=[{"name": "q1", "values": {"in": list(AB_ROWS)}}, {"name": "kb1", "values": {"in": list(KB2_ROWS)}}, {"name": "p", "values": {"in": NZ2}}, {"name": "bv", "values": {"in": NZ}}, {"name": "k", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}],
        table=[{"key": "q1", "rows": AB_ROWS}, {"key": "kb1", "rows": KB2_ROWS}],
        derive={"q": "kb*bv", "a": "p - k", "b": "bv", "ans": "c1*(p - k) + c2*bv + cp*(p - k)*bv"},
        constraints=["a != 0", "ans != 0", "ans != p", "ans != q", "ans != k", "ans != -k", "ans != kb", "ans != -kb"],
        cost_values=["p", "q", "k", "kb", "a", "b", "ans"],
        answer_var="ans",
        verify=["a + k == p", "kb*b == q", "ans == c1*a + c2*b + cp*a*b"],
        question="x에 대한 방정식 {co(p)}x {sgn(q)} = (a {sgn(k)})x {KB}의 해가 무수히 많을 때, 상수 a, b에 대하여 {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="해가 무수히 많다는 것은 x에 어떤 값을 넣어도 성립한다는 뜻, 곧 이 등식이 x에 대한 항등식이라는 뜻이다. 그러므로 양변의 x의 계수끼리, 상수항끼리 각각 같아야 한다. x의 계수에서 a를, 상수항에서 b를 구한다.",
        sol2=[
            "해가 무수히 많으므로 양변의 x의 계수가 같다: a {sgn(k)} = {p}, a = {a}",
            "상수항도 같다: {co(kb)}b = {q}, b = {bv}",
            "따라서 {QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "a {sgn(k)} = {p}  →  a = {a}", "hint": "x의 계수 비교"},
            {"text": "{co(kb)}b = {q}  →  b = {bv}", "hint": "상수항 비교", "marks": [{"on": "{bv}", "note": "{kb}{ro(kb)} 나눈다"}]},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="a = {a}, b = {bv}{eul(bv)} 넣으면 우변은 {co(p)}x {sgn(q)}{ika(q)} 되어 좌변과 똑같으므로 x에 어떤 값을 넣어도 성립한다(해가 무수히 많다). 따라서 {QT} = {ans}이다.",
        sol3_fig=steps(["우변: ({a} {sgn(k)})x + {kb} × {pn(bv)} = {co(p)}x {sgn(q)}", "좌변과 같다 → 해가 무수히 많다"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="해가 무수히 많으므로 항등식이고 양변의 x의 계수와 상수항이 각각 같다. a {sgn(k)} = {p}에서 a = {a}, {co(kb)}b = {q}에서 b = {bv}이므로 {QT} = {ans}이다.",
        rubric=[
            {"element": "무수히 많은 해의 조건", "points": 3, "criterion": "해가 무수히 많으려면 양변의 x의 계수와 상수항이 각각 같아야 함(항등식)을 밝혔다.", "partial": "계수만 비교하고 근거를 쓰지 않았으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "a = {a}, b = {bv}{eul(bv)} 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 답했다.", "partial": "a, b만 쓰고 {QT}{eul(QT)} 쓰지 않았으면 1점."},
        ],
        rubric_total=7,
    )


LC_SEED = {
    "seed_id": LC, "category": "연산",
    "title": "해의 조건으로 상수 구하기 — 해의 배수 관계·자연수 해의 개수·해 없음·해 무수히 많음",
    "unit_id": "m1-1", "concept_ids": ["m1-1-24", "m1-1-26"],
    "schema_id": None, "schema_name": "일차방정식의 해의 조건과 상수",
    "source_item_ids": [],
    "note": "구조만 차용. 해 없음 틀은 a = p 가 문면에 노출되지 않도록 (a ± k)x 꼴로 둔다.",
    "geometry": False,
    "templates": [lc_t1(), lc_t2(), lc_t3(), lc_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 5. 일차방정식의 활용 2 — 정가·원가, 일, 도형
EA = "m1-1-eq-apply-2"
EA_BASE = {**COMMON_APPLY, "prereq": ["일차방정식의 풀이", "백분율"], "traps": ["미지수설정", "식세우기", "구하는대상혼동"], "tags": ["일차방정식의 활용"], "qtype": "short", "pool_target": 300, "rubric_total": 8}


def ea_t1():
    return tpl(EA, 1, EA_BASE,
        title="정가와 원가 — 이익을 붙여 정가를 정하고 할인하여 판 이익으로 원가 구하기",
        skill="원가를 x로 놓고 정가 = x(1 + 이익률), 판매가 = 정가(1 − 할인율), 이익 = 판매가 − 원가로 식 세우기",
        variant_axis={"이익률": "10~50 %", "할인율": "10~30 %", "원가": "2,000~30,000원"},
        discriminates="할인율을 원가가 아니라 정가에 적용하는가, 이익 = 판매가 − 원가로 세우는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": [10, 15, 20, 25, 30, 40, 50]}}, {"name": "q", "values": {"in": [5, 10, 15, 20, 25, 30]}}, {"name": "k", "values": {"int": [2, 30]}}],
        derive={"x": "1000*k", "m1": "(100 + p)/100", "m2": "(100 + p)*(100 - q)/10000", "pr": "((100 + p)*(100 - q) - 10000)/10000", "r": "1000*k*((100 + p)*(100 - q) - 10000)/10000",
                "jg": "1000*k*(100 + p)/100", "pm": "1000*k*(100 + p)*(100 - q)/10000"},
        constraints=["(100 + p)*(100 - q) > 10000", "r == floor(r)", "r >= 100", "r != x", "r != p", "r != q"],
        cost_values=["p", "q", "r", "x"],
        answer_var="x",
        verify=["x*m2 - x == r", "ans == x", "ans*(100 + p)*(100 - q) - 10000*ans == 10000*r"],
        question="원가가 x원인 상품에 원가의 {p} %의 이익을 붙여 정가를 정하고, 정가에서 {q} %를 할인하여 팔았더니 {r}원의 이익이 생겼다. 이 상품의 원가를 구하시오.",
        answer="{x}", answer_alt=["{x}원"],
        sol1="원가 x원에 {p} %의 이익을 붙이면 정가는 x × (1 + [[frac({p},100)]]) = {dec(m1)}x원이다. 할인은 정가에 대한 것이므로 판매 가격은 {dec(m1)}x × (1 − [[frac({q},100)]]) = {dec(m2)}x원이고, 이익은 (판매 가격) − (원가) = {dec(m2)}x − x = {dec(pr)}x원이다. 이것이 {r}원이라는 방정식을 세운다.",
        sol2=[
            "정가는 x × (1 + [[frac({p},100)]]) = {dec(m1)}x (원)",
            "판매 가격은 정가의 (100 − {q}) %이므로 {dec(m1)}x × (1 − [[frac({q},100)]]) = {dec(m2)}x (원)",
            "이익은 (판매 가격) − (원가)이므로 {dec(m2)}x − x = {r}, 곧 {dec(pr)}x = {r}",
            "따라서 x = {r} ÷ {dec(pr)} = {x}, 원가는 {x}원이다.",
        ],
        sol2_fig=steps([
            {"text": "정가 = {dec(m1)}x", "hint": "원가 × (1 + {p}/100)"},
            {"text": "판매 가격 = {dec(m1)}x × {dec((100 - q)/100)} = {dec(m2)}x", "hint": "할인은 정가에", "marks": [{"on": "{dec(m1)}x ×", "note": "원가가 아니라 정가"}]},
            {"text": "{dec(m2)}x − x = {r}", "hint": "이익 = 판매가 − 원가"},
            {"text": "x = {x}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="원가 {x}원이면 정가는 {jg}원, 판매 가격은 {pm}원이고 이익은 {pm} − {x} = {r}(원)으로 조건과 같다. 따라서 원가는 {x}원이다.",
        sol3_fig=steps(["정가 {jg}원 → 판매가 {pm}원", "{pm} − {x} = {r}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="원가를 x원이라 하면 정가는 {dec(m1)}x원, 판매 가격은 {dec(m1)}x × (1 − [[frac({q},100)]]) = {dec(m2)}x원이다. 이익이 {r}원이므로 {dec(m2)}x − x = {r}, {dec(pr)}x = {r}, x = {x}이다. 따라서 원가는 {x}원이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "정가 {dec(m1)}x, 판매 가격 {dec(m2)}x를 구해 {dec(m2)}x − x = {r}{eul(r)} 세웠다.", "partial": "할인을 원가에 적용해 세웠으면 인정하지 않고, 정가까지만 옳으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{dec(pr)}x = {r}{eul(r)} 풀어 x = {x}{eul(x)} 구했다.", "partial": "소수 계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "원가 {x}원을 답으로 썼다.", "partial": "정가나 판매 가격을 답했으면 인정하지 않는다."},
        ],
    )


def ea_t2():
    return tpl(EA, 2, EA_BASE,
        title="일 — A가 먼저 며칠 일한 뒤 B가 나머지를 마칠 때 B가 일한 날수",
        skill="전체 일의 양을 1로 놓고 하루에 하는 일의 양(1/a, 1/b)으로 식을 세우기",
        variant_axis={"A·B의 기간": "2~20일", "A가 먼저 일한 날": "1~8일"},
        discriminates="전체를 1로 놓고 하루 일의 양을 역수로 쓰는가, A가 한 일을 뺀 나머지를 B의 몫으로 세우는가",
        difficulty=3,
        params=[{"name": "c", "values": {"int": [1, 9]}}, {"name": "d", "values": {"int": [1, 9]}}, {"name": "m", "values": {"int": [1, 6]}}],
        derive={"a": "c + d", "g": "gcd(c, d)", "y": "m*d/gcd(c, d)", "b": "m*(c + d)/gcd(c, d)", "wa": "c/(c + d)", "wb": "d/(c + d)"},
        constraints=["b != a", "b >= 2", "y >= 1", "y != c", "y != a", "y != b", "a <= 20", "b <= 30"],
        cost_values=["a", "b", "c", "y"],
        answer_var="y",
        verify=["c/a + ans/b == 1", "ans == y"],
        question="어떤 일을 A가 혼자 하면 {a}일, B가 혼자 하면 {b}일이 걸린다. 이 일을 A가 혼자 {c}일 동안 한 다음 나머지를 B가 혼자 하여 마쳤다. B가 혼자 일한 기간은 며칠인지 구하시오.",
        answer="{y}", answer_alt=["{y}일"],
        sol1="전체 일의 양을 1로 놓으면 A는 하루에 [[frac(1,{a})]], B는 하루에 [[frac(1,{b})]]만큼 한다. B가 일한 날수를 x일이라 하면 A가 {c}일 동안 한 일 {c} × [[frac(1,{a})]]와 B가 x일 동안 한 일 x × [[frac(1,{b})]]를 합해 1이 된다는 방정식을 세운다.",
        sol1_fig=[{"fn": "bar", "args": {"rows": [{"name": "전체 일 1", "total": "{a*b}", "parts": [{"label": "A {c}일", "value": "{c*b}"}, {"label": "B x일", "value": "{y*a}"}]}]}}],
        sol1_anim=[[hl("part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1")], [hl("total:0")]],
        sol2=[
            "전체 일의 양을 1이라 하면 A와 B가 하루에 하는 일의 양은 각각 [[frac(1,{a})]], [[frac(1,{b})]]",
            "B가 x일 동안 일했다고 하면 [[frac({c},{a})]] + [[frac(x,{b})]] = 1",
            "양변에 {a*b}{eul(a*b)} 곱하면 {c*b} + {a}x = {a*b}, {a}x = {a*b - c*b}",
            "따라서 x = {y}, B는 {y}일 동안 일했다.",
        ],
        sol2_fig=steps([
            {"text": "A: 하루 [[frac(1,{a})]],  B: 하루 [[frac(1,{b})]]", "hint": "전체 = 1"},
            {"text": "[[frac({c},{a})]] + [[frac(x,{b})]] = 1", "hint": "A의 몫 + B의 몫 = 전체"},
            {"text": "{c*b} + {a}x = {a*b}  →  x = {y}", "hint": "분모의 최소공배수 곱하기"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol3="A가 {c}일 동안 한 일은 [[frac({c},{a})]] = {wa}, B가 {y}일 동안 한 일은 [[frac({y},{b})]] = {wb}이고 둘을 더하면 1이므로 일을 모두 마친 것이 맞다. 답은 {y}일이다.",
        sol3_fig=steps(["A: [[frac({c},{a})]] = {wa}", "B: [[frac({y},{b})]] = {wb}", "{wa} + {wb} = 1  ✓"]),
        sol3_anim=[[reveal(0), reveal(1)], [reveal(2)]],
        model_answer="전체 일의 양을 1이라 하면 A, B가 하루에 하는 일의 양은 각각 [[frac(1,{a})]], [[frac(1,{b})]]이다. B가 x일 동안 일했다고 하면 [[frac({c},{a})]] + [[frac(x,{b})]] = 1이므로 {c*b} + {a}x = {a*b}, x = {y}이다. 따라서 B는 {y}일 동안 일했다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "전체를 1로 놓고 [[frac({c},{a})]] + [[frac(x,{b})]] = 1을 세웠다.", "partial": "하루 일의 양을 역수로 쓰지 않고 날수를 그대로 더했으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "분모를 없애 {c*b} + {a}x = {a*b}{eul(a*b)} 풀어 x = {y}{eul(y)} 구했다.", "partial": "최소공배수를 한 항에만 곱했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "B가 일한 기간 {y}일을 답했다.", "partial": "A와 B가 함께 일한 총 날수를 답했으면 인정하지 않는다."},
        ],
    )


RQ_ROWS = {"h": {"Q": "세로의 길이", "isW": 0}, "w": {"Q": "가로의 길이", "isW": 1}}


def ea_t3():
    return tpl(EA, 3, EA_BASE,
        title="둘레가 주어진 직사각형 — 가로가 세로보다 d cm 길 때 변의 길이 구하기",
        skill="세로를 x로 놓고 가로를 x + d로 나타내어 둘레 = 2(가로 + 세로) 방정식 세우기",
        variant_axis={"구하는 것": "세로 / 가로", "차": "1~10 cm"},
        discriminates="둘레를 두 변의 합의 2배로 세우는가, 구하는 것이 세로인지 가로인지 확인하는가",
        difficulty=2, context="기하맥락",
        params=[{"name": "q", "values": {"in": list(RQ_ROWS)}}, {"name": "x", "values": {"int": [2, 20]}}, {"name": "d", "values": {"int": [1, 10]}}],
        table={"key": "q", "rows": RQ_ROWS},
        derive={"P": "4*x + 2*d", "w": "x + d", "ans": "x + isW*d"},
        constraints=["ans != d", "ans != P", "x != d", "w != d", "w != P"],
        cost_values=["P", "d", "x", "w", "ans"],
        answer_var="ans",
        verify=["2*(x + d + x) == P", "ans == x + isW*d"],
        question="가로의 길이가 세로의 길이보다 {d} cm 더 긴 직사각형의 둘레의 길이가 {P} cm일 때, 이 직사각형의 {Q}{eul(Q)} 구하시오.",
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="세로의 길이를 x cm라 하면 가로는 그보다 {d} cm 긴 (x + {d}) cm다. 직사각형의 둘레는 (가로 + 세로)의 2배이므로 2 × {{(x + {d}) + x}} = {P}라는 방정식을 세워 x를 구하고, 묻는 것이 {Q}임을 확인해 답한다.",
        sol1_fig=[{"fn": "rect", "args": {"w": "{w}", "h": "{x}"}}],
        sol2=[
            "세로의 길이를 x cm라 하면 가로의 길이는 (x + {d}) cm",
            "둘레가 {P} cm이므로 2 × {{(x + {d}) + x}} = {P}, 4x + {2*d} = {P}",
            "4x = {4*x}, x = {x}",
            "따라서 세로는 {x} cm, 가로는 {x} + {d} = {w} (cm)이고 구하는 {Q}{eun(Q)} {ans} cm이다.",
        ],
        sol2_fig=steps([
            {"text": "세로 x,  가로 x + {d}", "hint": "차를 이용해 한 문자로"},
            {"text": "2 × {{(x + {d}) + x}} = {P}", "hint": "둘레 = 2(가로 + 세로)"},
            {"text": "4x + {2*d} = {P}  →  x = {x}", "marks": [{"on": "{2*d}", "note": "{d}에도 2를 곱한다"}]},
            {"text": "{Q} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3)]],
        sol3="세로 {x} cm, 가로 {w} cm이면 가로가 {d} cm 더 길고 둘레는 2 × ({w} + {x}) = {P}(cm)로 조건과 같다. 따라서 {Q}{eun(Q)} {ans} cm이다.",
        sol3_fig=steps(["가로 {w} − 세로 {x} = {d}  ✓", "2 × ({w} + {x}) = {P}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="세로의 길이를 x cm라 하면 가로는 (x + {d}) cm이고, 둘레가 {P} cm이므로 2 × {{(x + {d}) + x}} = {P}, 4x + {2*d} = {P}, x = {x}이다. 따라서 {Q}{eun(Q)} {ans} cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "세로 x, 가로 x + {d}로 놓고 2 × {{(x + {d}) + x}} = {P}{eul(P)} 세웠다.", "partial": "둘레를 가로 + 세로로 세웠으면 인정하지 않고, 가로·세로만 바르게 놓았으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "4x + {2*d} = {P}{eul(P)} 풀어 x = {x}{eul(x)} 구했다.", "partial": "괄호 전개에서 {d}에 2를 곱하지 않았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans} cm를 답했다.", "partial": "가로와 세로를 바꿔 답했으면 인정하지 않는다."},
        ],
    )


def ea_t4():
    return tpl(EA, 4, EA_BASE,
        title="넓이가 주어진 사다리꼴 — 아랫변의 길이 구하기",
        skill="아랫변을 x로 놓고 사다리꼴의 넓이 = (윗변 + 아랫변) × 높이 ÷ 2 방정식 세우기",
        variant_axis={"윗변": "2~15 cm", "높이": "2~12 cm"},
        discriminates="넓이 공식의 ÷ 2를 빠뜨리지 않는가, 양변에 2를 곱해 괄호를 푸는가",
        difficulty=2, context="기하맥락",
        params=[{"name": "x", "values": {"int": [3, 20]}}, {"name": "a", "values": {"int": [2, 15]}}, {"name": "h", "values": {"int": [2, 12]}}],
        derive={"S": "(a + x)*h/2", "S2": "(a + x)*h", "ax": "a + x"},
        constraints=["((a + x)*h) % 2 == 0", "x != a", "x != h", "x != S", "S != a", "S != h", "a != h", "ax != S"],
        cost_values=["a", "h", "S", "x"],
        answer_var="x",
        verify=["(a + ans)*h == 2*S", "ans == x"],
        question="윗변의 길이가 {a} cm, 높이가 {h} cm인 사다리꼴의 넓이가 {S} cm²일 때, 이 사다리꼴의 아랫변의 길이를 구하시오.",
        answer="{x}", answer_alt=["{x} cm"],
        sol1="사다리꼴의 넓이는 (윗변 + 아랫변) × (높이) ÷ 2이다. 아랫변의 길이를 x cm라 하면 ({a} + x) × {h} ÷ 2 = {S}라는 방정식이 되고, 양변에 2를 곱한 뒤 {h}{ro(h)} 나누면 {a} + x가 나온다.",
        sol2=[
            "아랫변의 길이를 x cm라 하면 (사다리꼴의 넓이) = ({a} + x) × {h} ÷ 2",
            "넓이가 {S} cm²이므로 ({a} + x) × {h} ÷ 2 = {S}, 양변에 2를 곱하면 ({a} + x) × {h} = {S2}",
            "양변을 {h}{ro(h)} 나누면 {a} + x = {ax}, x = {x}",
            "따라서 아랫변의 길이는 {x} cm이다.",
        ],
        sol2_fig=steps([
            {"text": "({a} + x) × {h} ÷ 2 = {S}", "hint": "(윗변 + 아랫변) × 높이 ÷ 2", "marks": [{"on": "÷ 2", "note": "빠뜨리지 말 것"}]},
            {"text": "({a} + x) × {h} = {S2}", "hint": "양변 × 2"},
            {"text": "{a} + x = {ax}  →  x = {x}", "hint": "양변 ÷ {h}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol3="아랫변이 {x} cm이면 넓이는 ({a} + {x}) × {h} ÷ 2 = {ax} × {h} ÷ 2 = {S}(cm²)로 조건과 같다. 따라서 아랫변의 길이는 {x} cm이다.",
        sol3_fig=steps(["({a} + {x}) × {h} ÷ 2 = {S}  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="아랫변의 길이를 x cm라 하면 ({a} + x) × {h} ÷ 2 = {S}이므로 ({a} + x) × {h} = {S2}, {a} + x = {ax}, x = {x}이다. 따라서 아랫변의 길이는 {x} cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "아랫변을 x로 놓고 ({a} + x) × {h} ÷ 2 = {S}{eul(S)} 세웠다.", "partial": "÷ 2를 빠뜨리고 세웠으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "방정식을 풀어 x = {x}{eul(x)} 구했다.", "partial": "2를 곱하거나 {h}{ro(h)} 나누는 과정에서 한쪽 변만 처리했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "아랫변의 길이 {x} cm를 답했다.", "partial": "{a} + x의 값 {ax}{eul(ax)} 답했으면 인정하지 않는다."},
        ],
    )


EA_SEED = {
    "seed_id": EA, "category": "활용",
    "title": "일차방정식의 활용 2 — 정가·원가, 일, 직사각형 둘레, 사다리꼴 넓이",
    "unit_id": "m1-1", "concept_ids": ["m1-1-27"],
    "schema_id": None, "schema_name": "일차방정식의 활용(정가·일·도형)",
    "source_item_ids": [],
    "note": "구조만 차용. 원가·해를 먼저 뽑아 이익·둘레·넓이를 파생(정수 보장). 일 문제는 c·d·m 인수로 날수를 정수화.",
    "geometry": False,
    "templates": [ea_t1(), ea_t2(), ea_t3(), ea_t4()],
}


if __name__ == "__main__":
    for seed in (EV_SEED, LE_SEED, ES_SEED, LC_SEED, EA_SEED):
        with_pitfalls(seed)
        dump(seed)
