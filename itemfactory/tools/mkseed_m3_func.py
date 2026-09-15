# itemfactory/tools/mkseed_m3_func.py — m3-1 이차함수 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_func.py
#     → seeds/m3-1-quad-func.json        (이차함수의 그래프: y = ax² 점 통과·두 점·평행이동·꼭짓점·x절편 거리·y절편·식 구하기, 7틀)
#     → seeds/m3-1-quad-func-apply.json  (최댓값·최솟값과 활용: 일반형 최대/최소·최댓값→상수·둘레 고정 넓이·물체 최고 높이, 4틀)
#
# 이차함수 표기: y = {co(a)}x² {sgt(b)}x {sgn(c)} (b, c ≠ 0 제약). 꼭짓점형은 y = {co(a)}(x {sgn(np)})² {sgn(q)}.
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


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
NZ = lambda lo, hi: [v for v in range(lo, hi + 1) if v != 0]  # noqa: E731

# ═══════════════════════════════════════════════════════════════════ 1. 이차함수의 그래프
QF = "m3-1-quad-func"
QF_BASE = {**BASE, "prereq": ["함수의 뜻", "제곱"], "ops": ["이차함수"], "traps": ["평행이동 부호", "꼭짓점 좌표"], "tags": ["이차함수"]}


# t1 — y = ax² 가 점 (p, q) 를 지날 때 a (분수 가능)
def qf_t1():
    return tpl(QF, 1, QF_BASE,
        title="y = ax²의 그래프가 지나는 점으로 a 구하기",
        skill="점의 좌표를 x, y에 대입해 a에 대한 일차방정식으로 풀기",
        variant_axis={"점": "x ±2~±4, y ±1~±12"},
        difficulty=2,
        discriminates="x좌표를 제곱해 대입하고, 필요하면 분수로 a를 구하는가(정수라고 단정하지 않는가)",
        params=[{"name": "p", "values": {"in": [-4, -3, -2, 2, 3, 4]}}, {"name": "q", "values": {"in": NZ(-12, 12)}}],
        derive={"p2": "p*p", "ans": "q/(p*p)"},
        constraints=["ans != 1", "ans != -1", "ans not in (p, q)"],
        cost_values=["p", "q", "p2", "ans"],
        answer_var="ans",
        verify=["ans*p2 == q"],
        question="이차함수 y = ax²의 그래프가 점 ({p}, {q})를 지날 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="그래프가 점을 지난다는 것은 그 점의 좌표를 대입하면 등식이 성립한다는 뜻이다. y = ax²에 x = {p}, y = {q}{eul(q)} 넣으면 {q} = a × {pn(p)}² = {p2}a이므로 a = {q} ÷ {p2}로 구한다.",
        sol2=[
            "x = {p}, y = {q} 대입: {q} = a × {pn(p)}²",
            "{q} = {p2}a",
            "a = [[frac({q}, {p2})]] = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{q} = a × {pn(p)}²", "hint": "점의 좌표 대입"},
            {"text": "{q} = {p2}a", "hint": "제곱 먼저", "marks": [{"on": "{p2}a", "note": "{pn(p)}² = {p2}"}]},
            {"text": "a = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="a = {ans}{eul(ans)} 넣은 y = {ans}x²에 x = {p}{eul(p)} 대입하면 y = {ans} × {p2} = {q}{ro(q)} 점 ({p}, {q})를 지난다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["{ans} × {p2} = {q} ✓", "a = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = ax²에 x = {p}, y = {q}{eul(q)} 대입하면 {q} = {p2}a이므로 a = {ans}이다.",
        rubric=[
            {"element": "대입", "points": 2, "criterion": "{q} = a × {pn(p)}²{eul(p2)} 세웠다.", "partial": "x와 y를 바꿔 대입했으면 인정하지 않는다."},
            {"element": "a 구하기", "points": 3, "criterion": "a = {ans}{eul(ans)} 구했다.", "partial": "제곱을 빠뜨려 {p2}a가 아닌 {p}a로 풀었으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t2 — y = ax² 가 (p, q) 를 지나고 (m, k) 도 지날 때 k
def qf_t2():
    return tpl(QF, 2, QF_BASE,
        title="y = ax²의 그래프가 두 점을 지날 때 — 다른 점의 y좌표",
        skill="한 점으로 a를 구한 뒤 다른 점의 x좌표를 대입해 y좌표 구하기",
        variant_axis={"첫 점": "x ±2~±3", "둘째 점": "x ±2~±5"},
        difficulty=2,
        discriminates="a를 먼저 정하고, 둘째 점의 x좌표를 제곱해 대입하는가",
        params=[{"name": "p", "values": {"in": [-3, -2, 2, 3]}}, {"name": "a", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "m", "values": {"in": [-5, -4, -3, -2, 2, 3, 4, 5]}}],
        derive={"q": "a*p*p", "p2": "p*p", "m2": "m*m", "ans": "a*m*m"},
        constraints=["m*m != p*p", "ans not in (p, q, m)", "ans != 0"],
        cost_values=["p", "q", "a", "m", "ans"],
        answer_var="ans",
        verify=["q == a*p2", "ans == a*m2"],
        question="이차함수 y = ax²의 그래프가 두 점 ({p}, {q}), ({m}, k)를 지날 때, k의 값을 구하시오. (단, a는 상수)",
        answer="{ans}", answer_alt=[],
        sol1="먼저 좌표를 모두 아는 점 ({p}, {q})를 대입해 a를 정한다: {q} = a × {pn(p)}² = {p2}a에서 a = {a}. 그다음 y = {co(a)}x²에 x = {m}{eul(m)} 넣으면 k가 나온다.",
        sol2=[
            "({p}, {q}) 대입: {q} = {p2}a → a = {a}",
            "y = {co(a)}x²에 x = {m} 대입: k = {a} × {pn(m)}² = {a} × {m2}",
            "따라서 k = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{q} = {p2}a → a = {a}", "hint": "아는 점으로 a"},
            {"text": "k = {a} × {pn(m)}²", "hint": "x = {m} 대입", "marks": [{"on": "{pn(m)}²", "note": "= {m2}"}]},
            {"text": "k = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="y = {co(a)}x²은 x = {p}에서 {a} × {p2} = {q}, x = {m}에서 {a} × {m2} = {ans}{ro(ans)} 두 점을 모두 지난다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["y = {co(a)}x²: ({p}, {q}) ✓", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="({p}, {q}){eul(q)} 대입하면 {q} = {p2}a이므로 a = {a}이다. y = {co(a)}x²에 x = {m}{eul(m)} 대입하면 k = {a} × {m2} = {ans}이다.",
        rubric=[
            {"element": "a 구하기", "points": 2, "criterion": "({p}, {q}){eul(q)} 대입해 a = {a}{eul(a)} 구했다.", "partial": "제곱을 빠뜨렸으면 인정하지 않는다."},
            {"element": "k 구하기", "points": 3, "criterion": "x = {m}{eul(m)} 대입해 k = {ans}{eul(ans)} 구했다.", "partial": "x좌표의 부호를 살려 제곱하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t3 — 평행이동한 그래프가 지나는 점: y = a(x − p)² + q 에 x = m
def qf_t3():
    return tpl(QF, 3, QF_BASE,
        title="y = ax²의 그래프를 평행이동한 그래프가 지나는 점 — k의 값",
        skill="x축 방향 p, y축 방향 q만큼 평행이동한 식 y = a(x − p)² + q를 세우고 대입하기",
        variant_axis={"a": "±1~±3", "p, q": "±1~±5", "x좌표": "−4~4"},
        difficulty=3,
        discriminates="x축 방향 이동은 (x − p)로 부호가 바뀌고 y축 방향 이동은 + q로 그대로임을 구별하는가",
        params=[{"name": "a", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "p", "values": {"in": NZ(-5, 5)}}, {"name": "q", "values": {"in": NZ(-5, 5)}}, {"name": "m", "values": {"int": [-4, 4]}}],
        derive={"np": "-p", "d": "m - p", "d2": "(m - p)**2", "ad2": "a*(m - p)**2", "ans": "a*(m - p)**2 + q"},
        constraints=["m != p", "d2 != 1", "ans not in (a, p, q, m)", "ans != 0", "d2 <= 49"],
        cost_values=["a", "p", "q", "m", "d", "d2", "ans"],
        answer_var="ans",
        verify=["ans == ad2 + q", "d2 == d*d"],
        question="이차함수 y = {co(a)}x²의 그래프를 x축의 방향으로 {p}만큼, y축의 방향으로 {q}만큼 평행이동한 그래프가 점 ({m}, k)를 지날 때, k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y = ax²의 그래프를 x축의 방향으로 p만큼, y축의 방향으로 q만큼 평행이동하면 y = a(x − p)² + q이다. x 대신 x − p를 넣는 것이므로 x축 방향은 부호가 반대로 들어가고, y축 방향은 그대로 더한다. 평행이동한 식 y = {co(a)}(x {sgn(np)})² {sgn(q)}에 x = {m}{eul(m)} 대입한다.",
        sol2=[
            "평행이동한 식: y = {co(a)}(x {sgn(np)})² {sgn(q)}",
            "x = {m} 대입: k = {a} × ({m} {sgn(np)})² {sgn(q)} = {a} × {pn(d)}² {sgn(q)}",
            "= {a} × {d2} {sgn(q)} = {ad2} {sgn(q)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "y = {co(a)}(x {sgn(np)})² {sgn(q)}", "hint": "x → x − ({p}), y → y − ({q})", "marks": [{"on": "(x {sgn(np)})²", "note": "x축 방향 {p}"}]},
            {"text": "k = {a} × {pn(d)}² {sgn(q)}", "hint": "x = {m} 대입"},
            {"text": "k = {ad2} {sgn(q)} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="평행이동한 그래프의 꼭짓점은 ({p}, {q})이다. x = {m}{eun(m)} 꼭짓점에서 {pn(d)}만큼 떨어져 있으므로 y는 꼭짓점의 y좌표 {q}보다 {a} × {d2} = {ad2}만큼 변한 {ans}이다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["꼭짓점 ({p}, {q}), x = {m}은 {pn(d)}만큼 떨어짐", "k = {q} + {pn(ad2)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="평행이동한 그래프의 식은 y = {co(a)}(x {sgn(np)})² {sgn(q)}이다. x = {m}{eul(m)} 대입하면 k = {a} × {pn(d)}² {sgn(q)} = {ans}이다.",
        rubric=[
            {"element": "평행이동한 식", "points": 3, "criterion": "y = {co(a)}(x {sgn(np)})² {sgn(q)}{eul(q)} 세웠다.", "partial": "x축 방향의 부호를 반대로 썼으면 인정하지 않는다."},
            {"element": "대입·계산", "points": 2, "criterion": "x = {m}{eul(m)} 대입해 k = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — y = ax² + bx + c 의 꼭짓점 (p, q) → p + q 또는 pq
VX_ROWS = {"sum": {"ASK": "p + q", "w": 1}, "prod": {"ASK": "pq", "w": 0}}


def qf_t4():
    return tpl(QF, 4, QF_BASE,
        title="y = ax² + bx + c의 꼭짓점 — y = a(x − p)² + q로 고쳐 p + q 또는 pq",
        skill="이차항·일차항을 a로 묶고 완전제곱식을 만들어 꼭짓점의 좌표 읽기",
        variant_axis={"a": "±1, ±2", "꼭짓점": "p ±1~±4, q ±1~±9", "구하는 것": "p + q / pq"},
        difficulty=3,
        discriminates="a로 묶은 뒤 (x의 계수의 반)²을 더하고 빼며, 빼는 값에 a를 곱하는 것을 잊지 않는가",
        params=[{"name": "a", "values": {"in": [-2, -1, 1, 2]}}, {"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "q", "values": {"in": NZ(-9, 9)}}, {"name": "ask", "values": {"in": ["sum", "prod"]}}],
        table={"key": "ask", "rows": VX_ROWS},
        derive={"b": "-2*a*p", "c": "a*p*p + q", "np": "-p", "p2": "p*p", "ap2": "a*p*p", "boa": "-2*p", "ans": "w*(p + q) + (1 - w)*p*q"},
        constraints=["c != 0", "ans not in (a, b, c)", "ans != 0"],
        cost_values=["a", "p", "q", "b", "c", "p2", "ap2", "ans"],
        answer_var="ans",
        verify=["b == -2*a*p", "c == ap2 + q", "ans == w*(p + q) + (1 - w)*p*q"],
        question="이차함수 y = {co(a)}x² {sgt(b)}x {sgn(c)}의 그래프의 꼭짓점의 좌표가 (p, q)일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y = ax² + bx + c를 y = a(x − p)² + q 꼴로 고치면 꼭짓점은 (p, q)이다. 이차항과 일차항을 a = {a}{ro(a)} 묶어 y = {co(a)}(x² {sgt(boa)}x) {sgn(c)}{ro(c)} 만들고, 괄호 안에 (x의 계수의 반)² = {p2}{eul(p2)} 더하고 빼어 완전제곱식을 만든다 — 괄호 밖으로 나올 때 {a}배가 되는 것에 주의한다.",
        sol2=[
            "y = {co(a)}(x² {sgt(boa)}x) {sgn(c)} = {co(a)}(x² {sgt(boa)}x + {p2} − {p2}) {sgn(c)}",
            "= {co(a)}(x {sgn(np)})² {sgn(-ap2)} {sgn(c)} = {co(a)}(x {sgn(np)})² {sgn(q)}",
            "꼭짓점 ({p}, {q})이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}(x² {sgt(boa)}x + {p2} − {p2}) {sgn(c)}", "hint": "a로 묶고 ({boa} ÷ 2)² 더하고 빼기"},
            {"text": "{co(a)}(x {sgn(np)})² {sgn(q)}", "hint": "−{p2}에 {a}를 곱해 밖으로", "marks": [{"on": "(x {sgn(np)})²", "note": "p = {p}"}, {"on": "{sgn(q)}", "note": "q = {q}"}]},
            {"text": "꼭짓점 ({p}, {q}) → {ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="{co(a)}(x {sgn(np)})² {sgn(q)}{eul(q)} 전개하면 {co(a)}x² {sgt(b)}x + {pn(ap2)} {sgn(q)} = {co(a)}x² {sgt(b)}x {sgn(c)}{ro(c)} 원래 식과 같다. 따라서 꼭짓점은 ({p}, {q})이고 {ASK} = {ans}이다.",
        sol3_fig=steps(["전개 확인: {co(a)}x² {sgt(b)}x {sgn(c)} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = {co(a)}x² {sgt(b)}x {sgn(c)} = {co(a)}(x² {sgt(boa)}x + {p2} − {p2}) {sgn(c)} = {co(a)}(x {sgn(np)})² {sgn(q)}이므로 꼭짓점은 ({p}, {q})이다. 따라서 {ASK} = {ans}이다.",
        rubric=[
            {"element": "완전제곱식 변형", "points": 3, "criterion": "y = {co(a)}(x {sgn(np)})² {sgn(q)}{ro(q)} 고쳤다.", "partial": "빼는 값에 a를 곱하지 않아 q가 틀렸으면 1점."},
            {"element": "꼭짓점·답", "points": 2, "criterion": "꼭짓점 ({p}, {q})에서 {ASK} = {ans}{eul(ans)} 구했다.", "partial": "p의 부호를 반대로 읽었으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t5 — y = a(x − p)² + q 그래프와 x축의 두 교점: 거리 2s 또는 x좌표의 곱
XI_ROWS = {"dist": {"ASK": "두 점 사이의 거리", "w": 1}, "prod": {"ASK": "두 점의 x좌표의 곱", "w": 0}}


def qf_t5():
    return tpl(QF, 5, QF_BASE,
        title="y = a(x − p)² + q의 그래프와 x축의 두 교점 — 거리 또는 x좌표의 곱",
        skill="y = 0을 대입해 (x − p)² = −q/a를 제곱근으로 풀어 두 x절편 구하기",
        variant_axis={"a": "±1~±3", "p": "±1~±4", "s": "1~4", "구하는 것": "거리 / 곱"},
        difficulty=3,
        discriminates="y = 0을 넣어 (x − p)² = s²에서 x = p ± s를 얻고, 거리 2s 또는 곱 (p − s)(p + s)를 구하는가",
        params=[{"name": "a", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "s", "values": {"int": [1, 4]}}, {"name": "ask", "values": {"in": ["dist", "prod"]}}],
        table={"key": "ask", "rows": XI_ROWS},
        derive={"q": "-a*s*s", "np": "-p", "s2": "s*s", "x1": "p - s", "x2": "p + s", "ans": "w*2*s + (1 - w)*(p - s)*(p + s)"},
        constraints=["ans not in (a, p, q)", "ans != 0", "x1 != 0", "x2 != 0"],
        cost_values=["a", "p", "q", "s", "x1", "x2", "ans"],
        answer_var="ans",
        verify=["q == -a*s2", "x2 - x1 == 2*s", "ans == w*2*s + (1 - w)*x1*x2"],
        question="이차함수 y = {co(a)}(x {sgn(np)})² {sgn(q)}의 그래프가 x축과 만나는 두 점에 대하여 {ASK}를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x축과 만나는 점은 y = 0인 점이다. {co(a)}(x {sgn(np)})² {sgn(q)} = 0에서 (x {sgn(np)})² = {s2}{ika(s2)} 되고, 제곱근을 취하면 x {sgn(np)} = ±{s}, 즉 x = {x1} 또는 x = {x2}이다. 두 점의 x좌표로 거리(차)와 곱을 구한다.",
        sol2=[
            "y = 0: {co(a)}(x {sgn(np)})² {sgn(q)} = 0 → (x {sgn(np)})² = {s2}",
            "x {sgn(np)} = ±{s} → x = {x1} 또는 x = {x2}",
            "두 점 ({x1}, 0), ({x2}, 0): 거리 {x2} − {pn(x1)} = {2*s}, 곱 {pn(x1)} × {pn(x2)} = {x1*x2} → {ASK} {ans}",
        ],
        sol2_fig=steps([
            {"text": "(x {sgn(np)})² = {s2}", "hint": "y = 0 대입, {a}로 나눔"},
            {"text": "x = {x1} 또는 x = {x2}", "hint": "x {sgn(np)} = ±{s}", "marks": [{"on": "x = {x1}", "note": "p − s"}, {"on": "x = {x2}", "note": "p + s"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="꼭짓점 ({p}, {q})를 중심으로 두 x절편이 좌우로 {s}씩 떨어져 있으므로 x절편은 {x1}, {x2}이다. 거리는 2 × {s} = {2*s}, 곱은 {pn(x1)} × {pn(x2)} = {x1*x2}이므로 {ASK}는 {ans}이다.",
        sol3_fig=steps(["축 x = {p}에서 좌우 {s}: {x1}, {x2}", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = 0을 대입하면 (x {sgn(np)})² = {s2}이므로 x = {x1} 또는 x = {x2}이다. 따라서 {ASK}는 {ans}이다.",
        rubric=[
            {"element": "x절편 구하기", "points": 3, "criterion": "y = 0을 대입해 x = {x1}, {x2}{eul(x2)} 구했다.", "partial": "±를 빠뜨려 한 점만 구했으면 1점."},
            {"element": "거리·곱 구하기", "points": 2, "criterion": "{ASK} {ans}{eul(ans)} 구했다.", "partial": "거리와 곱을 바꿔 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t6 — y = a(x − p)² + q 의 y절편
def qf_t6():
    return tpl(QF, 6, QF_BASE,
        title="y = a(x − p)² + q의 그래프가 y축과 만나는 점의 y좌표",
        skill="y축 위의 점은 x = 0이므로 x = 0을 대입해 y좌표 구하기",
        variant_axis={"a": "±1~±3", "p": "±2~±5", "q": "±1~±9"},
        difficulty=2,
        discriminates="y절편은 x = 0을 대입한 값 ap² + q이지 q(꼭짓점의 y좌표)가 아님을 아는가",
        params=[{"name": "a", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "p", "values": {"in": [-5, -4, -3, -2, 2, 3, 4, 5]}}, {"name": "q", "values": {"in": NZ(-9, 9)}}],
        derive={"np": "-p", "p2": "p*p", "ap2": "a*p*p", "ans": "a*p*p + q"},
        constraints=["ans not in (a, p, q)", "ans != 0"],
        cost_values=["a", "p", "q", "p2", "ap2", "ans"],
        answer_var="ans",
        verify=["ans == ap2 + q", "ap2 == a*p2"],
        question="이차함수 y = {co(a)}(x {sgn(np)})² {sgn(q)}의 그래프가 y축과 만나는 점의 y좌표를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y축 위의 점은 x좌표가 0이다. 따라서 x = 0을 대입한 y = {a} × (0 {sgn(np)})² {sgn(q)}{ika(q)} y절편이다. 꼭짓점의 y좌표 {q}{eul(q)} 그대로 답하지 않도록 한다.",
        sol2=[
            "x = 0 대입: y = {a} × (0 {sgn(np)})² {sgn(q)}",
            "= {a} × {pn(np)}² {sgn(q)} = {a} × {p2} {sgn(q)}",
            "= {ap2} {sgn(q)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "y = {a} × (0 {sgn(np)})² {sgn(q)}", "hint": "y축 위 → x = 0"},
            {"text": "= {a} × {p2} {sgn(q)}", "hint": "{pn(np)}² = {p2}", "marks": [{"on": "{a} × {p2}", "note": "= {ap2}"}]},
            {"text": "= {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="전개하면 y = {co(a)}x² {sgt(-2*a*p)}x {sgn(ans)}이고 상수항이 y절편이므로 {ans}{ika(ans)} 맞다. 꼭짓점의 y좌표 {q}{wa(q)} 다르다.",
        sol3_fig=steps(["전개: 상수항 = {ans}", "y절편 {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = 0을 대입하면 y = {a} × {pn(np)}² {sgn(q)} = {ap2} {sgn(q)} = {ans}이므로 y축과 만나는 점의 y좌표는 {ans}이다.",
        rubric=[
            {"element": "x = 0 대입", "points": 2, "criterion": "x = 0을 대입해 {a} × {pn(np)}² {sgn(q)}{eul(q)} 세웠다.", "partial": "꼭짓점의 y좌표 {q}{eul(q)} 답했으면 인정하지 않는다."},
            {"element": "계산", "points": 3, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t7 — 꼭짓점과 한 점으로 식 구하기: y = ax² + bx + c 의 a + b + c
def qf_t7():
    return tpl(QF, 7, QF_BASE,
        title="꼭짓점과 다른 한 점이 주어진 이차함수의 식 — a + b + c",
        skill="꼭짓점형 y = a(x − p)² + q에 다른 점을 대입해 a를 정하고 일반형으로 전개하기",
        variant_axis={"a": "±1, ±2", "꼭짓점": "p ±1~±4, q ±1~±6", "다른 점": "x −4~4"},
        difficulty=3,
        discriminates="꼭짓점을 y = a(x − p)² + q로 옮기고 나머지 한 점으로 a를 구한 뒤 전개까지 하는가",
        params=[{"name": "a", "values": {"in": [-2, -1, 1, 2]}}, {"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "q", "values": {"in": NZ(-6, 6)}}, {"name": "m", "values": {"int": [-4, 4]}}],
        derive={"np": "-p", "d": "m - p", "d2": "(m - p)**2", "n": "a*(m - p)**2 + q", "b": "-2*a*p", "c": "a*p*p + q", "ans": "a - 2*a*p + a*p*p + q"},
        constraints=["m != p", "d2 != 1", "d2 <= 25", "c != 0", "n != 0", "n != q", "ans not in (p, q, m, n)", "ans != 0"],
        cost_values=["a", "p", "q", "m", "n", "b", "c", "ans"],
        answer_var="ans",
        verify=["n == a*d2 + q", "ans == a + b + c", "b == -2*a*p", "c == a*p*p + q"],
        question="꼭짓점의 좌표가 ({p}, {q})이고 점 ({m}, {n})을 지나는 이차함수의 식이 y = ax² + bx + c일 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="꼭짓점이 ({p}, {q})이므로 식을 y = a(x {sgn(np)})² {sgn(q)}{ro(q)} 놓을 수 있다. 여기에 지나는 점 ({m}, {n})을 대입하면 {n} = a × {pn(d)}² {sgn(q)}에서 a = {a}가 나온다. 마지막으로 전개해 y = ax² + bx + c 꼴로 만들고 계수를 읽는다.",
        sol2=[
            "y = a(x {sgn(np)})² {sgn(q)}에 ({m}, {n}) 대입: {n} = {d2}a {sgn(q)} → a = {a}",
            "y = {co(a)}(x {sgn(np)})² {sgn(q)} = {co(a)}(x² {sgt(-2*p)}x + {p*p}) {sgn(q)}",
            "= {co(a)}x² {sgt(b)}x {sgn(c)}이므로 a + b + c = {ans}",
        ],
        sol2_fig=steps([
            {"text": "y = a(x {sgn(np)})² {sgn(q)}", "hint": "꼭짓점 ({p}, {q})"},
            {"text": "{n} = {d2}a {sgn(q)} → a = {a}", "hint": "({m}, {n}) 대입", "marks": [{"on": "a = {a}", "note": "a"}]},
            {"text": "y = {co(a)}x² {sgt(b)}x {sgn(c)} → a + b + c = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="y = {co(a)}x² {sgt(b)}x {sgn(c)}에 x = {m}{eul(m)} 넣으면 {n}{ika(n)} 되고, 꼭짓점의 x좌표 −b/(2a) = {p}{ro(p)} 맞다. a + b + c는 x = 1일 때의 y의 값이기도 하다: {ans}.",
        sol3_fig=steps(["x = {m} → y = {n} ✓", "a + b + c = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="꼭짓점이 ({p}, {q})이므로 y = a(x {sgn(np)})² {sgn(q)}{ro(q)} 놓고 ({m}, {n})을 대입하면 a = {a}이다. 전개하면 y = {co(a)}x² {sgt(b)}x {sgn(c)}이므로 a + b + c = {ans}이다.",
        rubric=[
            {"element": "꼭짓점형·a", "points": 3, "criterion": "y = a(x {sgn(np)})² {sgn(q)}{ro(q)} 놓고 a = {a}{eul(a)} 구했다.", "partial": "p의 부호를 반대로 놓았으면 인정하지 않는다."},
            {"element": "전개·답", "points": 2, "criterion": "y = {co(a)}x² {sgt(b)}x {sgn(c)}{ro(c)} 전개해 a + b + c = {ans}{eul(ans)} 구했다.", "partial": "전개 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


QF_SEED = {
    "seed_id": QF, "category": "함수",
    "title": "이차함수의 그래프 — y = ax² 점 통과·두 점·평행이동·꼭짓점·x절편·y절편·식 구하기",
    "unit_id": "m3-1", "concept_ids": ["m3-1-22", "m3-1-23", "m3-1-24", "m3-1-25", "m3-1-26", "m3-1-27", "m3-1-28"],
    "schema_id": None, "schema_name": "이차함수의 그래프와 식",
    "source_item_ids": [],
    "note": "그래프 그림 없이 식·좌표로만 묻는 틀. 일반형 y = ax² + bx + c 는 꼭짓점 (p, q) 에서 b = −2ap, c = ap² + q 로 파생해 정수 보장.",
    "geometry": False,
    "templates": [qf_t1(), qf_t2(), qf_t3(), qf_t4(), qf_t5(), qf_t6(), qf_t7()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 최댓값·최솟값과 활용
QM = "m3-1-quad-func-apply"
QM_BASE = {**BASE, "prereq": ["이차함수의 꼭짓점", "완전제곱식"], "ops": ["이차함수"], "traps": ["최대/최소 구분", "꼭짓점 y좌표"], "tags": ["이차함수의 최댓값과 최솟값"]}
MM_ROWS = {"max": {"MM": "최댓값", "sg": -1, "DIR": "위로 볼록"}, "min": {"MM": "최솟값", "sg": 1, "DIR": "아래로 볼록"}}


# t1 — y = ax² + bx + c 의 최댓값/최솟값
def qm_t1():
    return tpl(QM, 1, QM_BASE,
        title="y = ax² + bx + c의 최댓값 또는 최솟값",
        skill="완전제곱식으로 고쳐 꼭짓점의 y좌표를 읽고, a의 부호로 최댓값인지 최솟값인지 판단하기",
        variant_axis={"a": "±1~±3", "꼭짓점": "p ±1~±4, q ±1~±9"},
        difficulty=3,
        discriminates="a < 0이면 최댓값, a > 0이면 최솟값이며 그 값은 꼭짓점의 y좌표임을 아는가",
        params=[{"name": "aa", "values": {"int": [1, 3]}}, {"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "q", "values": {"in": NZ(-9, 9)}}, {"name": "v", "values": {"in": ["max", "min"]}}],
        table={"key": "v", "rows": MM_ROWS},
        derive={"a": "sg*aa", "b": "-2*sg*aa*p", "c": "sg*aa*p*p + q", "np": "-p", "p2": "p*p", "boa": "-2*p", "ap2": "sg*aa*p*p", "ans": "q"},
        constraints=["c != 0", "ans not in (b, c)", "ans != 0"],
        cost_values=["a", "p", "q", "b", "c", "ans"],
        answer_var="ans",
        verify=["b == -2*a*p", "c == ap2 + q", "ans == q"],
        question="이차함수 y = {co(a)}x² {sgt(b)}x {sgn(c)}의 {MM}을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y = a(x − p)² + q 꼴로 고치면 그래프의 꼭짓점이 (p, q)이고, a = {a}{eun(a)} {DIR}이므로 꼭짓점에서 {MM} q를 갖는다. 이차항·일차항을 {a}{ro(a)} 묶고 (x의 계수의 반)² = {p2}{eul(p2)} 더하고 빼어 완전제곱식을 만든다.",
        sol2=[
            "y = {co(a)}(x² {sgt(boa)}x) {sgn(c)} = {co(a)}(x² {sgt(boa)}x + {p2} − {p2}) {sgn(c)}",
            "= {co(a)}(x {sgn(np)})² {sgn(-ap2)} {sgn(c)} = {co(a)}(x {sgn(np)})² {sgn(q)}",
            "a = {a}{eun(a)} {DIR}: x = {p}일 때 {MM} {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}(x² {sgt(boa)}x + {p2} − {p2}) {sgn(c)}", "hint": "a로 묶고 완전제곱식"},
            {"text": "{co(a)}(x {sgn(np)})² {sgn(q)}", "hint": "꼭짓점 ({p}, {q})", "marks": [{"on": "{sgn(q)}", "note": "{MM} {q}"}]},
            {"text": "a = {a} → {DIR} → {MM} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{co(a)}(x {sgn(np)})²{eun(p)} x = {p}일 때 0이고 그 밖에서는 {DIR}의 방향으로 커지거나 작아지므로 y는 x = {p}에서 {MM} {q}{eul(q)} 갖는다. 따라서 {MM}은 {ans}이다.",
        sol3_fig=steps(["(x {sgn(np)})² ≥ 0, a = {a}", "{MM} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = {co(a)}x² {sgt(b)}x {sgn(c)} = {co(a)}(x {sgn(np)})² {sgn(q)}이고 a = {a}{eun(a)} {DIR}이므로 x = {p}일 때 {MM} {ans}{eul(ans)} 갖는다.",
        rubric=[
            {"element": "완전제곱식 변형", "points": 3, "criterion": "y = {co(a)}(x {sgn(np)})² {sgn(q)}{ro(q)} 고쳤다.", "partial": "빼는 값에 a를 곱하지 않았으면 1점."},
            {"element": "최대·최소 판단", "points": 2, "criterion": "a의 부호로 {MM}임을 밝히고 {ans}{eul(ans)} 답했다.", "partial": "최댓값·최솟값을 반대로 말했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t2 — 최댓값(최솟값)이 M 일 때 상수 c
def qm_t2():
    return tpl(QM, 2, QM_BASE,
        title="최댓값(최솟값)이 주어진 이차함수 y = ax² + bx + c의 상수 c",
        skill="완전제곱식으로 고쳐 꼭짓점의 y좌표를 c로 나타내고 주어진 최댓값(최솟값)과 같다고 놓기",
        variant_axis={"a": "±1, ±2", "p": "±1~±4", "M": "−9~9"},
        difficulty=3,
        discriminates="꼭짓점의 y좌표 c − ap²이 최댓값(최솟값)임을 식으로 세워 c를 역으로 구하는가",
        params=[{"name": "aa", "values": {"int": [1, 2]}}, {"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "M", "values": {"int": [-9, 9]}}, {"name": "v", "values": {"in": ["max", "min"]}}],
        table={"key": "v", "rows": MM_ROWS},
        derive={"a": "sg*aa", "b": "-2*sg*aa*p", "np": "-p", "p2": "p*p", "boa": "-2*p", "ap2": "sg*aa*p*p", "ans": "M + sg*aa*p*p"},
        constraints=["ans != 0", "ans not in (b, M)", "M != 0"],
        cost_values=["a", "p", "M", "b", "ap2", "ans"],
        answer_var="ans",
        verify=["b == -2*a*p", "ans == M + ap2"],
        question="이차함수 y = {co(a)}x² {sgt(b)}x + c의 {MM}이 {M}일 때, 상수 c의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="a = {a}{eun(a)} {DIR}이므로 {MM}은 꼭짓점의 y좌표이다. y = {co(a)}(x² {sgt(boa)}x) + c = {co(a)}(x {sgn(np)})² {sgn(-ap2)} + c로 고치면 꼭짓점의 y좌표는 c {sgn(-ap2)}이고, 이것이 {M}{wa(M)} 같다고 놓아 c를 구한다.",
        sol2=[
            "y = {co(a)}(x² {sgt(boa)}x + {p2} − {p2}) + c = {co(a)}(x {sgn(np)})² {sgn(-ap2)} + c",
            "{MM}(꼭짓점의 y좌표) c {sgn(-ap2)} = {M}",
            "c = {M} {sgn(ap2)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}(x {sgn(np)})² {sgn(-ap2)} + c", "hint": "완전제곱식"},
            {"text": "c {sgn(-ap2)} = {M}", "hint": "{MM} = 꼭짓점의 y좌표", "marks": [{"on": "= {M}", "note": "{MM}"}]},
            {"text": "c = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="c = {ans}{eul(ans)} 넣으면 y = {co(a)}(x {sgn(np)})² {sgn(M)}{ika(M)} 되어 x = {p}에서 {MM} {M}{eul(M)} 갖는다. 따라서 c = {ans}이다.",
        sol3_fig=steps(["y = {co(a)}(x {sgn(np)})² {sgn(M)}", "c = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = {co(a)}x² {sgt(b)}x + c = {co(a)}(x {sgn(np)})² {sgn(-ap2)} + c이므로 {MM}은 c {sgn(-ap2)}이다. c {sgn(-ap2)} = {M}에서 c = {ans}이다.",
        rubric=[
            {"element": "꼭짓점의 y좌표", "points": 3, "criterion": "완전제곱식으로 고쳐 {MM}이 c {sgn(-ap2)}임을 밝혔다.", "partial": "빼는 값에 a를 곱하지 않았으면 1점."},
            {"element": "c 구하기", "points": 2, "criterion": "c {sgn(-ap2)} = {M}에서 c = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t3 — 둘레가 일정한 직사각형의 넓이의 최댓값
def qm_t3():
    return tpl(QM, 3, {**QM_BASE, **COMMON_APPLY, "context": "기하맥락", "ops": ["이차함수"], "points": 4, "pool_target": 300},
        title="둘레의 길이가 일정한 직사각형의 넓이의 최댓값",
        skill="가로를 x로 놓아 넓이를 x의 이차함수로 나타내고 완전제곱식으로 최댓값 구하기",
        variant_axis={"둘레": "12~160 (4의 배수)", "문장": "둘레가 주어진 직사각형 / 철사로 만든 직사각형 / 직사각형 모양의 액자"},
        difficulty=3,
        discriminates="세로를 (둘레/2 − x)로 나타내 넓이 식을 세우고, 정사각형일 때 최대임을 확인하는가",
        params=[{"name": "k", "values": {"int": [3, 40]}}, {"name": "c", "values": {"in": ["rect", "wire", "frame"]}}],
        table={"key": "c", "rows": {"rect": {"PRE": "둘레의 길이가 ", "POST": " cm인 직사각형의 넓이의 최댓값"}, "wire": {"PRE": "길이가 ", "POST": " cm인 철사를 남김없이 모두 사용하여 직사각형을 만들 때, 이 직사각형의 넓이의 최댓값"}, "frame": {"PRE": "둘레의 길이가 ", "POST": " cm인 직사각형 모양의 액자를 만들 때, 액자 안쪽 직사각형의 넓이의 최댓값"}}},
        derive={"L": "4*k", "H": "2*k", "ans": "k*k"},
        constraints=["ans != L"],
        cost_values=["k", "L", "H", "ans"],
        answer_var="ans",
        verify=["L == 4*k", "H == 2*k", "ans == k*k"],
        question="{PRE}{L}{POST}을 구하시오.",
        answer="{ans}", answer_alt=["{ans} cm²"],
        sol1="가로를 x cm라 하면 가로 + 세로 = {L} ÷ 2 = {H}이므로 세로는 ({H} − x) cm이다. 넓이 S = x({H} − x) = −x² + {H}x는 x의 이차함수이고 x²의 계수가 음수이므로 최댓값을 갖는다. 완전제곱식으로 고쳐 꼭짓점의 y좌표를 읽는다.",
        sol2=[
            "가로 x, 세로 {H} − x: S = x({H} − x) = −x² + {H}x",
            "S = −(x² − {H}x + {k*k} − {k*k}) = −(x − {k})² + {ans}",
            "x = {k}일 때 최댓값 {ans} (가로 = 세로 = {k} cm인 정사각형)",
        ],
        sol2_fig=steps([
            {"text": "S = x({H} − x)", "hint": "가로 + 세로 = {H}"},
            {"text": "S = −(x − {k})² + {ans}", "hint": "완전제곱식", "marks": [{"on": "+ {ans}", "note": "최댓값"}]},
            {"text": "x = {k}: 정사각형일 때 최대"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="가로와 세로가 같은 {k} cm일 때 넓이는 {k} × {k} = {ans}이고, 예컨대 가로를 {k+1} cm로 하면 세로는 {k-1} cm가 되어 넓이 {(k+1)*(k-1)}{ro((k+1)*(k-1))} 더 작다. 따라서 최댓값은 {ans} cm²이다.",
        sol3_fig=steps(["{k} × {k} = {ans}  vs  {k+1} × {k-1} = {(k+1)*(k-1)}", "최댓값 {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="가로를 x cm라 하면 세로는 ({H} − x) cm이므로 넓이 S = x({H} − x) = −(x − {k})² + {ans}이다. 따라서 x = {k}일 때 넓이의 최댓값은 {ans} cm²이다.",
        rubric=[
            {"element": "넓이 식", "points": 2, "criterion": "S = x({H} − x){eul(H)} 세웠다.", "partial": "세로를 {L} − x로 놓았으면 인정하지 않는다."},
            {"element": "최댓값", "points": 3, "criterion": "완전제곱식으로 고쳐 최댓값 {ans}{eul(ans)} 구했다.", "partial": "정사각형일 때 최대라는 사실만 써서 답했으면 2점."},
        ],
        rubric_total=5,
    )


# t4 — 던져 올린 물체의 최고 높이·시각
HT_ROWS = {"h": {"ASK": "최고 높이", "UNIT": " m", "w": 1, "w3": 0}, "t": {"ASK": "최고 높이에 도달하는 시각", "UNIT": "초", "w": 0, "w3": 0}, "back": {"ASK": "다시 지면에 떨어지는 시각", "UNIT": "초", "w": 0, "w3": 1}}
H0_ROWS = {"0": {"PLACE": "지면", "TAIL": "", "h0": 0}, "10": {"PLACE": "높이 10 m인 곳", "TAIL": " + 10", "h0": 10}, "20": {"PLACE": "높이 20 m인 곳", "TAIL": " + 20", "h0": 20}, "30": {"PLACE": "높이 30 m인 곳", "TAIL": " + 30", "h0": 30}}


def qm_t4():
    return tpl(QM, 4, {**QM_BASE, **COMMON_APPLY, "ops": ["이차함수"], "points": 4, "pool_target": 300},
        title="던져 올린 물체의 최고 높이와 그때의 시각",
        skill="h = −5t² + vt를 완전제곱식으로 고쳐 꼭짓점 (t, h)를 읽기",
        variant_axis={"초속": "20~300 (10의 배수)", "출발 높이": "0·10·20·30 m", "구하는 것": "최고 높이 / 시각 / 지면에 떨어지는 시각"},
        difficulty=3,
        discriminates="꼭짓점의 t좌표가 시각, h좌표가 최고 높이임을 구별해 답하는가",
        params=[{"name": "k", "values": {"int": [2, 30]}}, {"name": "ask", "values": {"in": ["h", "t", "back"]}}, {"name": "s0", "values": {"in": ["0", "10", "20", "30"]}}],
        table=[{"key": "ask", "rows": HT_ROWS}, {"key": "s0", "rows": H0_ROWS}],
        derive={"v": "10*k", "hmax": "5*k*k + h0", "k2": "k*k", "ans": "w*(5*k*k + h0) + w3*2*k + (1 - w - w3)*k"},
        constraints=["ans != v", "w3 == 0 or h0 == 0", "ans != h0"],
        cost_values=["k", "v", "hmax", "ans"],
        answer_var="ans",
        verify=["v == 10*k", "hmax == 5*k2 + h0", "ans == w*hmax + w3*2*k + (1 - w - w3)*k"],
        question="{PLACE}에서 초속 {v} m로 똑바로 위로 던져 올린 물체의 t초 후의 높이를 h m라 하면 h = {v}t − 5t²{TAIL}인 관계가 성립한다. 이 물체의 {ASK}를 구하시오.",
        answer="{ans}", answer_alt=["{ans}{UNIT}"],
        sol1="h = −5t² + {v}t{TAIL}는 t의 이차함수이고 t²의 계수가 음수이므로 꼭짓점에서 최댓값(최고 높이)을 갖는다. −5로 묶어 h = −5(t² − {2*k}t){TAIL} = −5(t − {k})² + {hmax}{ro(hmax)} 고치면 꼭짓점은 ({k}, {hmax}): t = {k}초일 때 최고 높이 {hmax} m이다. 지면(h = 0)에 떨어지는 시각은 h = 0을 풀어 구한다.",
        sol2=[
            "h = −5(t² − {2*k}t){TAIL} = −5(t² − {2*k}t + {k2} − {k2}){TAIL}",
            "= −5(t − {k})² + {hmax}",
            "t = {k}초일 때 최고 높이 {hmax} m, 지면에 떨어질 때(h = 0) t = {2*k} → {ASK}는 {ans}{UNIT}",
        ],
        sol2_fig=steps([
            {"text": "h = −5(t² − {2*k}t)", "hint": "−5로 묶기"},
            {"text": "h = −5(t − {k})² + {hmax}", "hint": "꼭짓점 ({k}, {hmax})", "marks": [{"on": "(t − {k})²", "note": "시각 {k}초"}, {"on": "+ {hmax}", "note": "최고 높이"}]},
            {"text": "{ASK} = {ans}{UNIT}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="t = {k}{eul(k)} 대입하면 h = {v} × {k} − 5 × {k2}{TAIL} = {hmax}{ro(hmax)} 맞고, 대칭성으로 t = 0과 t = {2*k}(높이가 처음과 같아지는 시각)의 한가운데 t = {k}에서 최고이다. 따라서 {ASK}는 {ans}{UNIT}이다.",
        sol3_fig=steps(["t = {k}: h = {hmax} (t = 0, {2*k}의 중점)", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="h = −5t² + {v}t{TAIL} = −5(t − {k})² + {hmax}이므로 t = {k}초일 때 최고 높이 {hmax} m에 도달하고, 출발 높이로 되돌아오는 시각은 t = {2*k}이다. 따라서 {ASK}는 {ans}{UNIT}이다.",
        rubric=[
            {"element": "완전제곱식 변형", "points": 3, "criterion": "h = −5(t − {k})² + {hmax}{ro(hmax)} 고쳤다.", "partial": "−5로 묶지 않아 계수가 틀렸으면 1점."},
            {"element": "시각·높이 읽기", "points": 2, "criterion": "{ASK} {ans}{UNIT}{eul(UNIT)} 답했다.", "partial": "시각과 높이를 바꿔 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


QM_SEED = {
    "seed_id": QM, "category": "함수",
    "title": "이차함수의 최댓값·최솟값과 활용 — 일반형 최대/최소·최댓값→상수·둘레 고정 넓이·물체 최고 높이",
    "unit_id": "m3-1", "concept_ids": ["m3-1-29", "m3-1-30"],
    "schema_id": None, "schema_name": "이차함수의 최댓값과 최솟값·활용",
    "source_item_ids": [],
    "note": "최대/최소는 a 의 부호 행(MM_ROWS)으로 나눈다. 활용 두 틀은 둘레 4k·초속 10k 로 정수 꼭짓점 보장.",
    "geometry": False,
    "templates": [qm_t1(), qm_t2(), qm_t3(), qm_t4()],
}


if __name__ == "__main__":
    for seed in (QF_SEED, QM_SEED):
        with_pitfalls(seed)
        dump(seed)
