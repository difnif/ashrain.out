# itemfactory/tools/mkseed_m3_number.py — m3-1 실수와 그 계산·곱셈 공식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_number.py
#     → seeds/m3-1-sqrt-basic.json   (제곱근의 뜻·성질: √(kx) 자연수·√(a−x) 개수·√a<n<√b 정수 개수·성질 계산·정수 부분, 5틀)
#     → seeds/m3-1-sqrt-ops.json     (근호 계산: 근호 간단히·곱셈·유리화·덧셈뺄셈·분배법칙, 5틀)
#     → seeds/m3-1-mult-formula.json (곱셈 공식: 전개 계수·수의 계산·무리수 계산·유리화·변형·무리수 대입, 6틀)
#
# 무리수는 [[sqrt(n)]]·[[k*sqrt(n)]] 마커. 답은 a√b 꼴의 a + b 처럼 수치로 묻는다(채점 안정). 근호 안 수는 표에 미리 계산(제곱인수 분리).
from __future__ import annotations

import os
import sys
from math import gcd, isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def sqfree(n: int):
    """n = a²·b (b 는 제곱인수 없음) → (a, b)"""
    a, b = 1, n
    p = 2
    while p * p <= b:
        while b % (p * p) == 0:
            b //= p * p
            a *= p
        p += 1
    return a, b


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
SQF = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]          # 제곱인수 없는 수

# ═══════════════════════════════════════════════════════════════════ 1. 제곱근의 뜻과 성질
SB = "m3-1-sqrt-basic"
SB_BASE = {**BASE, "prereq": ["제곱근의 뜻", "소인수분해"], "ops": ["제곱근"], "traps": ["제곱근과 √ 혼동", "제곱인수"], "tags": ["제곱근"]}

# t1 — √(kx) 가 자연수가 되는 가장 작은 자연수 x (k = a²·b → x = b)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def fstr(n: int) -> str:
    """60 → '2² × 3 × 5'"""
    fs, m, p = [], n, 2
    while p * p <= m:
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        if e:
            fs.append((p, e))
        p += 1
    if m > 1:
        fs.append((m, 1))
    return " × ".join(f"{q}{'' if e == 1 else str(e).translate(SUP)}" for q, e in fs)


KX_ROWS = {}
for _k in range(2, 600):
    _a, _b = sqfree(_k)
    if _b >= 2 and _a * _a != _k:
        KX_ROWS[str(_k)] = {"k": _k, "F": fstr(_k), "A": _a, "B": _b, "KB": _k * _b, "SQ": isqrt(_k * _b)}


def sb_t1():
    return tpl(SB, 1, SB_BASE,
        title="√(kx)가 자연수가 되도록 하는 가장 작은 자연수 x",
        skill="k를 소인수분해해 지수가 홀수인 소인수를 곱해 완전제곱수가 되게 하기",
        variant_axis={"k": "2~599 (제곱인수가 있는 수)"},
        discriminates="근호 안이 완전제곱수여야 함을 알고, 지수가 홀수인 소인수만 곱하는가(k 전체를 곱하지 않는가)",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(KX_ROWS)}}],
        table={"key": "f", "rows": KX_ROWS},
        derive={"ans": "B"},
        constraints=["ans != k"],
        cost_values=["k", "B", "SQ", "ans"],
        answer_var="ans",
        verify=["ans == B", "SQ*SQ == k*ans", "A*A*B == k"],
        question="[[sqrt({k}x)]]가 자연수가 되도록 하는 가장 작은 자연수 x의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="√(어떤 수)가 자연수이려면 근호 안의 수가 자연수의 제곱(완전제곱수)이어야 한다. {k}{eul(k)} 소인수분해하면 {F}이므로, 지수가 홀수인 소인수에 하나씩 더 곱해 모든 지수를 짝수로 만드는 가장 작은 x를 찾는다.",
        sol2=[
            "{k} = {F}",
            "지수가 홀수인 소인수를 한 번씩 더 곱해야 하므로 x = {B}",
            "확인: [[sqrt({k} × {B})]] = [[sqrt({KB})]] = {SQ}",
        ],
        sol2_fig=steps([
            {"text": "{k} = {F}", "hint": "소인수분해"},
            {"text": "x = {B}", "hint": "지수가 홀수인 소인수의 곱", "marks": [{"on": "{B}", "note": "가장 작은 x"}]},
            {"text": "[[sqrt({KB})]] = {SQ}", "hint": "완전제곱수 확인"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="{k} × {B} = {KB} = {SQ}²이므로 [[sqrt({KB})]] = {SQ}{ro(SQ)} 자연수가 된다. {B}보다 작은 자연수를 곱하면 지수가 홀수인 소인수가 남아 완전제곱수가 되지 않는다. 따라서 답은 {B}이다.",
        sol3_fig=steps(["{k} × {B} = {KB} = {SQ}²", "x = {B}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{k} = {F}이므로 {k}x가 완전제곱수가 되려면 x = {B}이어야 한다(이때 [[sqrt({KB})]] = {SQ}). 따라서 가장 작은 자연수 x는 {B}이다.",
        rubric=[
            {"element": "소인수분해", "points": 2, "criterion": "{k} = {F}{ro(F)} 소인수분해했다.", "partial": "소인수 하나를 빠뜨렸으면 1점."},
            {"element": "x 구하기", "points": 3, "criterion": "지수가 홀수인 소인수를 곱해 x = {B}{eul(B)} 구했다.", "partial": "{k} 전체를 곱해 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t2 — √(a − x) 가 자연수가 되는 자연수 x 의 개수 (a − x ∈ {1, 4, 9, …})
def _cnt_rows():
    out = {}
    for a in range(10, 100):
        sqs = [s * s for s in range(1, isqrt(a) + 1) if a - s * s >= 1]
        if 2 <= len(sqs) <= 8 and isqrt(a) ** 2 != a:
            xs = sorted(a - s for s in sqs)
            out[str(a)] = {"a": a, "CNT": len(sqs), "SQS": ", ".join(str(s) for s in sqs), "XS": ", ".join(str(x) for x in xs), "MAXS": isqrt(a) ** 2, "XMIN": min(xs)}
    return out


CNT_ROWS = _cnt_rows()
ASKC_ROWS = {"key": "ask", "rows": {"cnt": {"ASK": "자연수 x의 개수를", "w": 1}, "min": {"ASK": "가장 작은 자연수 x의 값을", "w": 0}}}


def sb_t2():
    return tpl(SB, 2, SB_BASE,
        title="√(a − x)가 자연수가 되도록 하는 자연수 x — 개수 또는 가장 작은 값",
        skill="a − x가 a보다 작은 완전제곱수(1, 4, 9, …)여야 함을 이용해 x를 모두 찾기",
        variant_axis={"a": "10~99 (완전제곱수 제외)", "구하는 것": "개수 / 가장 작은 x"},
        discriminates="a − x를 완전제곱수 목록과 맞추어 빠짐없이 세는가(0을 포함하지 않는가)",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(CNT_ROWS)}}, {"name": "ask", "values": {"in": ["cnt", "min"]}}],
        table=[{"key": "f", "rows": CNT_ROWS}, ASKC_ROWS],
        derive={"ans": "w*CNT + (1 - w)*XMIN"},
        constraints=["ans != a"],
        cost_values=["a", "CNT", "XMIN", "ans"],
        answer_var="ans",
        verify=["ans == w*CNT + (1 - w)*XMIN", "a - XMIN == MAXS"],
        question="[[sqrt({a} − x)]]가 자연수가 되도록 하는 {ASK} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="[[sqrt({a} − x)]]가 자연수이려면 근호 안 {a} − x가 완전제곱수여야 한다. x가 자연수이므로 {a} − x는 {a}보다 작은 자연수이고, 그런 완전제곱수는 {SQS}이다. 각각에서 x를 구하면 된다(0은 자연수의 제곱이 아니므로 제외).",
        sol2=[
            "{a} − x가 완전제곱수: {a} − x = {SQS}",
            "x = {XS}",
            "따라서 x의 개수는 {CNT}, 가장 작은 x는 {XMIN}",
        ],
        sol2_fig=steps([
            {"text": "{a} − x ∈ {{{SQS}}}", "hint": "{a}보다 작은 완전제곱수"},
            {"text": "x = {XS}", "hint": "각각에서 x", "marks": [{"on": "{XS}", "note": "{CNT}개"}]},
            {"text": "개수 {CNT}, 최솟값 {XMIN}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="가장 작은 x = {XMIN}일 때 {a} − {XMIN} = {MAXS}{ro(MAXS)} {a}보다 작은 가장 큰 완전제곱수가 되고, 그보다 큰 완전제곱수는 {a} 이상이라 x가 자연수가 아니다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{a} − {XMIN} = {MAXS} (가장 큰 완전제곱수)", "답 {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{a} − x가 완전제곱수여야 하므로 {a} − x = {SQS}, 즉 x = {XS}이다. 따라서 자연수 x의 개수는 {CNT}이고 가장 작은 x는 {XMIN}이다.",
        rubric=[
            {"element": "완전제곱수 조건", "points": 3, "criterion": "{a} − x가 완전제곱수 {SQS}이어야 함을 밝혔다.", "partial": "일부 완전제곱수를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "x = {XS}에서 {ASK} {ans}{ro(ans)} 답했다.", "partial": "0을 포함해 셌으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def sb_t3():
    return tpl(SB, 3, SB_BASE,
        title="√a < n < √b를 만족하는 자연수 n의 개수",
        skill="양변을 제곱해 a < n² < b로 바꾸고 제곱이 그 사이에 있는 자연수를 세기",
        variant_axis={"a": "2~40", "b": "20~120"},
        discriminates="제곱근의 대소를 제곱의 대소로 옮기고 경계(등호 없음)를 지켜 세는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [2, 40]}}, {"name": "b", "values": {"int": [20, 120]}}],
        derive={"lo": "floor(sqrt(a)) + 1", "hi": "ceiling(sqrt(b)) - 1", "ans": "ceiling(sqrt(b)) - 1 - floor(sqrt(a))", "lo2": "(floor(sqrt(a)) + 1)**2", "hi2": "(ceiling(sqrt(b)) - 1)**2"},
        constraints=["ans >= 2", "ans <= 8", "b > a + 10", "ans != a", "ans != b"],
        cost_values=["a", "b", "lo", "hi", "ans"],
        answer_var="ans",
        verify=["ans == hi - lo + 1", "lo2 > a", "hi2 < b", "(lo - 1)**2 <= a", "(hi + 1)**2 >= b"],
        question="[[sqrt({a})]] < n < [[sqrt({b})]]{eul(b)} 만족하는 자연수 n의 개수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="양수끼리는 제곱해도 대소가 그대로이므로 [[sqrt({a})]] < n < [[sqrt({b})]]는 {a} < n² < {b}와 같다. n²이 {a}보다 크고 {b}보다 작은 자연수 n을 찾는다 — 경계에 등호가 없으므로 n² = {a}, n² = {b}인 n은 제외한다.",
        sol2=[
            "각 변을 제곱하면 {a} < n² < {b}",
            "n²이 {a}보다 큰 가장 작은 n은 {lo}(n² = {lo2}), {b}보다 작은 가장 큰 n은 {hi}(n² = {hi2})",
            "따라서 n = {lo}, …, {hi}의 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "{a} < n² < {b}", "hint": "제곱해도 대소는 그대로"},
            {"text": "{lo}² = {lo2} > {a},  {hi}² = {hi2} < {b}", "hint": "경계의 n"},
            {"text": "n = {lo}, …, {hi} → {ans}개", "marks": [{"on": "{ans}개", "note": "{hi} − {lo} + 1"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="n = {lo}이면 n² = {lo2}{ro(lo2)} {a}보다 크고, n = {hi}이면 n² = {hi2}{ro(hi2)} {b}보다 작다. 그 밖의 n은 범위를 벗어난다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{a} < {lo2}, …, {hi2} < {b}", "n의 개수 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="각 변을 제곱하면 {a} < n² < {b}이므로 n = {lo}, …, {hi}이다. 따라서 자연수 n의 개수는 {ans}이다.",
        rubric=[
            {"element": "제곱하여 비교", "points": 2, "criterion": "{a} < n² < {b}{ro(b)} 바꾸었다.", "partial": "한쪽만 제곱했으면 인정하지 않는다."},
            {"element": "개수 세기", "points": 3, "criterion": "n = {lo}, …, {hi}의 {ans}개를 구했다.", "partial": "경계값 하나를 잘못 넣어 1개 차이면 1점."},
        ],
        rubric_total=5,
    )


def sb_t4():
    return tpl(SB, 4, SB_BASE,
        title="제곱근의 성질을 이용한 계산 — √(−a)², (−√b)², √c² 의 덧셈·뺄셈",
        skill="√(a²) = |a|, (√a)² = a, (−√a)² = a 를 구별해 근호를 벗기기",
        variant_axis={"수": "2~13"},
        discriminates="√((−a)²) = a(양수)이고 (−√b)² = b, −√(c²) = −c 임을 구별하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [2, 12]}}, {"name": "b", "values": {"in": [2, 3, 5, 6, 7, 10, 11, 13]}}, {"name": "c", "values": {"int": [2, 12]}}, {"name": "d", "values": {"in": [2, 3, 5, 6, 7, 10, 11, 13]}}],
        derive={"ans": "a + b - c - d", "ab": "a + b"},
        constraints=["ans != 0", "a != c", "b != d", "ans not in (a, b, c, d)"],
        cost_values=["a", "b", "c", "d", "ab", "ans"],
        answer_var="ans",
        verify=["ans == a + b - c - d"],
        question="[[sqrt(pow(-{a}, 2))]] + [[pow(-sqrt({b}), 2)]] − [[sqrt(pow({c}, 2))]] − [[pow(sqrt({d}), 2)]]{eul(d)} 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="제곱근의 성질: a > 0일 때 (√a)² = a, (−√a)² = a이고, √(a²) = a, √((−a)²) = a이다(근호를 벗기면 항상 0 이상). 그러므로 [[sqrt(pow(-{a}, 2))]] = {a}, [[pow(-sqrt({b}), 2)]] = {b}, [[sqrt(pow({c}, 2))]] = {c}, [[pow(sqrt({d}), 2)]] = {d}로 바꾼 뒤 계산한다.",
        sol2=[
            "[[sqrt(pow(-{a}, 2))]] = [[sqrt({a*a})]] = {a}, [[pow(-sqrt({b}), 2)]] = {b}",
            "[[sqrt(pow({c}, 2))]] = {c}, [[pow(sqrt({d}), 2)]] = {d}",
            "따라서 {a} + {b} − {c} − {d} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[sqrt(pow(-{a}, 2))]] = {a},  [[pow(-sqrt({b}), 2)]] = {b}", "hint": "√((−a)²) = a, (−√b)² = b"},
            {"text": "[[sqrt(pow({c}, 2))]] = {c},  [[pow(sqrt({d}), 2)]] = {d}", "hint": "√(c²) = c, (√d)² = d"},
            {"text": "{a} + {b} − {c} − {d} = {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="네 항이 모두 양수 {a}, {b}, {c}, {d}로 벗겨지는 것이 핵심이다(√((−{a})²)를 −{a}로 쓰면 틀린다). {a} + {b} = {ab}, {ab} − {c} − {d} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{a} + {b} = {ab}", "{ab} − {c} − {d} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[sqrt(pow(-{a}, 2))]] = {a}, [[pow(-sqrt({b}), 2)]] = {b}, [[sqrt(pow({c}, 2))]] = {c}, [[pow(sqrt({d}), 2)]] = {d}이므로 {a} + {b} − {c} − {d} = {ans}이다.",
        rubric=[
            {"element": "근호 벗기기", "points": 3, "criterion": "네 항을 각각 {a}, {b}, {c}, {d}{ro(d)} 바르게 벗겼다.", "partial": "√((−{a})²)를 −{a}로 썼으면 인정하지 않고, 하나만 틀렸으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{a} + {b} − {c} − {d} = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def sb_t5():
    return tpl(SB, 5, SB_BASE,
        title="c + √n의 정수 부분",
        skill="√n이 어느 두 연속 정수 사이에 있는지 제곱수로 잡아 정수 부분을 구하기",
        variant_axis={"n": "2~120 (완전제곱수 제외)", "c": "−5~9"},
        discriminates="√n의 정수 부분을 k² ≤ n < (k+1)²로 잡고 c를 더한 뒤 정수 부분을 읽는가",
        difficulty=2,
        params=[{"name": "n", "values": {"int": [2, 120]}}, {"name": "c", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}],
        derive={"k": "floor(sqrt(n))", "k1": "floor(sqrt(n)) + 1", "k2": "floor(sqrt(n))**2", "k12": "(floor(sqrt(n)) + 1)**2", "ans": "floor(sqrt(n)) + c"},
        constraints=["k2 != n", "ans != 0", "ans not in (n, c)"],
        cost_values=["n", "c", "k", "ans"],
        answer_var="ans",
        verify=["ans == k + c", "k2 < n", "n < k12"],
        question="{c} + [[sqrt({n})]]의 정수 부분을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="[[sqrt({n})]]의 값은 {n}을 사이에 두는 두 완전제곱수 {k2} = {k}²과 {k12} = {k1}²으로 잡는다: {k} < [[sqrt({n})]] < {k1}이므로 [[sqrt({n})]]의 정수 부분은 {k}이다. 여기에 {c}{eul(c)} 더한 수의 정수 부분은 {k} + {pn(c)} = {ans}이다.",
        sol2=[
            "{k2} < {n} < {k12}이므로 {k} < [[sqrt({n})]] < {k1}",
            "각 변에 {c}{eul(c)} 더하면 {ans} < {c} + [[sqrt({n})]] < {ans + 1}",
            "따라서 정수 부분은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "{k}² = {k2} < {n} < {k12} = {k1}²", "hint": "이웃한 완전제곱수"},
            {"text": "{k} < [[sqrt({n})]] < {k1}", "hint": "√{n}의 정수 부분 {k}"},
            {"text": "{ans} < {c} + [[sqrt({n})]] < {ans + 1}", "marks": [{"on": "{ans}", "note": "정수 부분"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="[[sqrt({n})]]{eun(n)} {k}보다 크고 {k1}보다 작으므로 {c} + [[sqrt({n})]]{eun(n)} {ans}보다 크고 {ans + 1}보다 작다. 따라서 정수 부분은 {ans}이다.",
        sol3_fig=steps(["{ans} < {c} + [[sqrt({n})]] < {ans + 1}", "정수 부분 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{k2} < {n} < {k12}에서 {k} < [[sqrt({n})]] < {k1}이므로 {ans} < {c} + [[sqrt({n})]] < {ans + 1}이다. 따라서 정수 부분은 {ans}이다.",
        rubric=[
            {"element": "√n의 범위", "points": 3, "criterion": "{k} < [[sqrt({n})]] < {k1}{eul(k1)} 밝혔다.", "partial": "완전제곱수를 잘못 잡았으면 인정하지 않는다."},
            {"element": "정수 부분", "points": 2, "criterion": "{c}{eul(c)} 더해 정수 부분 {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


SB_SEED = {
    "seed_id": SB, "category": "연산",
    "title": "제곱근의 뜻과 성질 — √(kx) 자연수·√(a − x) 개수·√a < n < √b·성질 계산·정수 부분",
    "unit_id": "m3-1", "concept_ids": ["m3-1-01", "m3-1-02", "m3-1-03"],
    "schema_id": None, "schema_name": "제곱근의 뜻·성질과 무리수의 대소",
    "source_item_ids": [],
    "note": "√(kx)·√(a−x) 틀은 소인수분해·완전제곱수 목록을 표에 미리 계산. 정수 부분은 floor(sqrt(n)) 파생.",
    "geometry": False,
    "templates": [sb_t1(), sb_t2(), sb_t3(), sb_t4(), sb_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 근호를 포함한 식의 계산
SO = "m3-1-sqrt-ops"
SO_BASE = {**BASE, "prereq": ["제곱근의 뜻", "소인수분해"], "ops": ["제곱근의 계산"], "traps": ["근호 안 곱셈", "동류항(같은 근호)"], "tags": ["제곱근의 계산"]}


def _rt(k: int, m: int) -> str:
    """k√m 의 마커 본문: 1 → 'sqrt(m)', 3 → '3*sqrt(m)'"""
    return f"sqrt({m})" if k == 1 else f"{k}*sqrt({m})"


# t1 — √n = a√b
SIMP_ROWS = {}
for _n in range(8, 400):
    _a, _b = sqfree(_n)
    if _a >= 2 and _b >= 2:
        SIMP_ROWS[str(_n)] = {"n": _n, "A": _a, "B": _b, "A2": _a * _a}


def so_t1():
    return tpl(SO, 1, SO_BASE,
        title="√n을 a√b 꼴로 간단히 — a + b",
        skill="근호 안의 수를 (제곱수) × (제곱인수 없는 수)로 나누어 제곱수를 근호 밖으로 꺼내기",
        variant_axis={"n": "8~399 (a ≥ 2, b ≥ 2)"},
        discriminates="가장 큰 제곱인수를 꺼내 b에 제곱인수가 남지 않게 하는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(SIMP_ROWS)}}],
        table={"key": "f", "rows": SIMP_ROWS},
        derive={"ans": "A + B"},
        constraints=["ans != n"],
        cost_values=["n", "A", "B", "ans"],
        answer_var="ans",
        verify=["ans == A + B", "A2*B == n"],
        question="[[sqrt({n})]] = a[[sqrt({b_})]] 꼴에서 b가 가장 작은 자연수가 되도록 나타낼 때, 자연수 a, b에 대하여 a + b의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="근호 안의 수를 제곱수와 제곱인수가 없는 수의 곱으로 나누면 제곱수는 근호 밖으로 나온다: √(a² × b) = a√b. {n} = {A2} × {B} = {A}² × {B}이므로 [[sqrt({n})]] = {A}[[sqrt({B})]]이고, {B}에는 더 이상 제곱인수가 없으므로 b가 가장 작다.",
        sol2=[
            "{n} = {A2} × {B} = {A}² × {B}",
            "[[sqrt({n})]] = [[sqrt({A}*{A}*{B})]] = {A}[[sqrt({B})]]",
            "따라서 a = {A}, b = {B}이고 a + b = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{n} = {A}² × {B}", "hint": "가장 큰 제곱인수 {A2}"},
            {"text": "[[sqrt({n})]] = {A}[[sqrt({B})]]", "hint": "제곱수는 근호 밖으로", "marks": [{"on": "{A}[[sqrt({B})]]", "note": "a = {A}, b = {B}"}]},
            {"text": "a + b = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="({A}[[sqrt({B})]])² = {A2} × {B} = {n}이므로 맞고, {B}{eun(B)} 제곱인수가 없어 더 간단히 할 수 없다. 따라서 a + b = {ans}이다.",
        sol3_fig=steps(["({A}[[sqrt({B})]])² = {A2} × {B} = {n} ✓", "a + b = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{n} = {A}² × {B}이므로 [[sqrt({n})]] = {A}[[sqrt({B})]]이다. 따라서 a = {A}, b = {B}이고 a + b = {ans}이다.",
        rubric=[
            {"element": "제곱인수 분리", "points": 3, "criterion": "{n} = {A}² × {B}{ro(B)} 나누어 [[sqrt({n})]] = {A}[[sqrt({B})]]{eul(B)} 얻었다.", "partial": "제곱인수를 일부만 꺼냈으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "a + b = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=5,
    )


def so_t1_final():
    t = so_t1()
    t["question"] = "[[sqrt({n})]]{eul(n)} a[[sqrt(b)]] (a, b는 자연수, b는 가장 작은 자연수) 꼴로 나타낼 때, a + b의 값을 구하시오."
    return t


# t2 — p√a × q√b = k√m
MUL_ROWS = {}
for _a in (2, 3, 5, 6, 7, 10):
    for _b in (2, 3, 5, 6, 7, 10, 14, 15):
        _c, _m = sqfree(_a * _b)
        if _m >= 2:
            for _p in (2, 3, 4, 5):
                for _q in (2, 3, 5):
                    if _p == _q and _a == _b:
                        continue
                    k = _p * _q * _c
                    MUL_ROWS[f"{_p}-{_a}-{_q}-{_b}"] = {"p": _p, "a": _a, "q": _q, "b": _b, "PA": _rt(_p, _a), "QB": _rt(_q, _b), "pq": _p * _q, "ab": _a * _b, "c": _c, "m": _m, "k": k, "KM": _rt(k, _m), "CM": _rt(_c, _m), "FAC": (f"{_c}² × {_m}" if _c > 1 else f"{_m} (제곱인수 없음)")}


def so_t2():
    return tpl(SO, 2, SO_BASE,
        title="p√a × q√b = k√m — k + m",
        skill="계수는 계수끼리, 근호 안은 근호 안끼리 곱한 뒤 제곱인수를 꺼내 간단히 하기",
        variant_axis={"계수": "2~5", "근호 안": "2~15"},
        discriminates="근호 안의 곱에서 생긴 제곱인수를 밖으로 꺼내 m을 가장 작게 하는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(MUL_ROWS)}}],
        table={"key": "f", "rows": MUL_ROWS},
        derive={"ans": "k + m"},
        constraints=["ans not in (p, a, q, b)", "k <= 90"],
        cost_values=["p", "a", "q", "b", "pq", "ab", "k", "m", "ans"],
        answer_var="ans",
        verify=["ans == k + m", "k == pq*c", "c*c*m == ab"],
        question="[[{PA}]] × [[{QB}]] = k[[sqrt(m)]] (m은 가장 작은 자연수)일 때, 자연수 k, m에 대하여 k + m의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="근호가 있는 수의 곱셈은 계수는 계수끼리({p} × {q}), 근호 안은 근호 안끼리({a} × {b}) 곱한다. 곱한 근호 안의 수 {ab} = {FAC}에서 제곱인수가 있으면 밖으로 꺼내 k√m 꼴로 정리한다.",
        sol2=[
            "[[{PA}]] × [[{QB}]] = ({p} × {q})[[sqrt({a} × {b})]] = {pq}[[sqrt({ab})]]",
            "{ab} = {FAC}이므로 [[sqrt({ab})]] = [[{CM}]]",
            "따라서 {pq} × [[{CM}]] = [[{KM}]]이고 k = {k}, m = {m}, k + m = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{pq}[[sqrt({ab})]]", "hint": "계수끼리 × 근호 안끼리"},
            {"text": "[[sqrt({ab})]] = [[{CM}]]", "hint": "{ab} = {FAC}"},
            {"text": "[[{KM}]] → k + m = {ans}", "marks": [{"on": "[[{KM}]]", "note": "k = {k}, m = {m}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="([[{KM}]])² = {k*k*m}이고 ([[{PA}]])² × ([[{QB}]])² = {p*p*a} × {q*q*b} = {k*k*m}{ro(k*k*m)} 같다. {m}에는 제곱인수가 없다. 따라서 k + m = {ans}이다.",
        sol3_fig=steps(["제곱 확인: {p*p*a} × {q*q*b} = {k*k*m} = {k}² × {m}", "k + m = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[{PA}]] × [[{QB}]] = {pq}[[sqrt({ab})]] = {pq} × [[{CM}]] = [[{KM}]]이므로 k = {k}, m = {m}이고 k + m = {ans}이다.",
        rubric=[
            {"element": "곱셈", "points": 2, "criterion": "{pq}[[sqrt({ab})]]{eul(ab)} 얻었다.", "partial": "계수와 근호 안을 뒤섞어 곱했으면 인정하지 않는다."},
            {"element": "간단히 하기", "points": 3, "criterion": "제곱인수를 꺼내 [[{KM}]]{ro(m)} 정리하고 k + m = {ans}{eul(ans)} 구했다.", "partial": "제곱인수를 꺼내지 않았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t3 — p/√n 유리화 → a√b/c
RAT_ROWS = {}
for _n in (2, 3, 5, 6, 7, 8, 10, 12, 18, 20, 27, 32, 45, 50):
    _s, _m = sqfree(_n)
    for _p in range(1, 13):
        g = gcd(_p, _s * _m)
        a, c = _p // g, _s * _m // g
        RAT_ROWS[f"{_p}-{_n}"] = {"p": _p, "n": _n, "s": _s, "m": _m, "sm": _s * _m, "a": a, "b": _m, "c": c, "g": g, "SN": _rt(_s, _m), "PM": _rt(_p, _m), "RES": (f"frac({_rt(a, _m)}, {c})" if c != 1 else _rt(a, _m)), "PROD": (f"frac({a * _s * _m}, {c})" if c != 1 else str(a * _s * _m))}


def so_t3():
    return tpl(SO, 3, SO_BASE,
        title="분모의 유리화 p/√n = a√b/c — a + b + c",
        skill="분모의 근호를 간단히 한 뒤 분자·분모에 같은 근호를 곱해 분모를 유리수로 만들고 약분하기",
        variant_axis={"분자": "1~12", "분모": "√2~√50"},
        discriminates="분모의 √n을 먼저 간단히 하고, 곱한 뒤 약분까지 하는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(RAT_ROWS)}}],
        table={"key": "f", "rows": RAT_ROWS},
        derive={"ans": "a + b + c"},
        constraints=["ans not in (p, n)", "c >= 2 or a >= 2"],
        cost_values=["p", "n", "s", "m", "a", "b", "c", "ans"],
        answer_var="ans",
        verify=["ans == a + b + c", "a*sm == c*p", "s*s*m == n", "gcd(a, c) == 1"],
        question="[[frac({p}, sqrt({n}))]]의 분모를 유리화하여 [[frac(a*sqrt(b), c)]] 꼴로 나타낼 때, 자연수 a, b, c에 대하여 a + b + c의 값을 구하시오. (단, b는 가장 작은 자연수, a와 c는 서로소)",
        answer="{ans}", answer_alt=[],
        sol1="분모에 근호가 있으면 분자와 분모에 같은 근호를 곱해 분모를 유리수로 만든다. 먼저 분모 [[sqrt({n})]] = [[{SN}]]{ro(m)} 간단히 한 뒤 [[sqrt({m})]]{eul(m)} 곱하면 분모는 {sm}{ika(sm)} 되고, 마지막에 분자의 계수와 분모를 약분한다.",
        sol2=[
            "[[sqrt({n})]] = [[{SN}]]이므로 [[frac({p}, sqrt({n}))]] = [[frac({p}, {SN})]]",
            "분자·분모에 [[sqrt({m})]]{eul(m)} 곱하면 [[frac({PM}, {sm})]]",
            "약분하면 [[{RES}]]이므로 a = {a}, b = {b}, c = {c}, a + b + c = {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[frac({p}, {SN})]]", "hint": "분모 먼저 간단히"},
            {"text": "[[frac({PM}, {sm})]]", "hint": "분자·분모 × [[sqrt({m})]]"},
            {"text": "[[{RES}]] → a + b + c = {ans}", "marks": [{"on": "[[{RES}]]", "note": "{g}{ro(g)} 약분"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="[[{RES}]] × [[sqrt({n})]] = {p}{ika(p)} 되는지 보면 [[{RES}]] × [[{SN}]] = [[{PROD}]] = {p}{ro(p)} 맞다. 따라서 a + b + c = {ans}이다.",
        sol3_fig=steps(["[[{RES}]] × [[sqrt({n})]] = {p} ✓", "a + b + c = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({p}, sqrt({n}))]] = [[frac({p}, {SN})]] = [[frac({PM}, {sm})]] = [[{RES}]]이므로 a = {a}, b = {b}, c = {c}이고 a + b + c = {ans}이다.",
        rubric=[
            {"element": "유리화", "points": 3, "criterion": "분모를 간단히 하고 [[sqrt({m})]]{eul(m)} 곱해 [[frac({PM}, {sm})]]{eul(sm)} 얻었다.", "partial": "분모를 간단히 하지 않고 [[sqrt({n})]]{eul(n)} 곱했어도 결과가 같으면 인정한다."},
            {"element": "약분·답", "points": 2, "criterion": "약분해 [[{RES}]]{ro(c)} 쓰고 a + b + c = {ans}{eul(ans)} 구했다.", "partial": "약분하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t4 — √n1 + √n2 − √n3 = k√m (같은 m)
ADD_ROWS = {}
for _m in (2, 3, 5, 6, 7):
    for _a1 in (1, 2, 3, 4, 5):
        for _a2 in (1, 2, 3, 4, 5):
            for _a3 in (1, 2, 3, 4, 5, 6):
                if len({_a1, _a2, _a3}) < 3:
                    continue
                k = _a1 + _a2 - _a3
                if k == 0:
                    continue
                ADD_ROWS[f"{_m}-{_a1}-{_a2}-{_a3}"] = {"m": _m, "a1": _a1, "a2": _a2, "a3": _a3, "n1": _a1 * _a1 * _m, "n2": _a2 * _a2 * _m, "n3": _a3 * _a3 * _m, "k": k,
                                                     "R1": _rt(_a1, _m), "R2": _rt(_a2, _m), "R3": _rt(_a3, _m)}


def so_t4():
    return tpl(SO, 4, SO_BASE,
        title="√n₁ + √n₂ − √n₃ = k√m — 근호 안을 같게 만들어 덧셈·뺄셈",
        skill="각 근호를 a√m 꼴로 간단히 한 뒤 같은 근호끼리 계수를 더하고 빼기",
        variant_axis={"m": "2·3·5·6·7", "계수": "1~6"},
        discriminates="근호 안이 다르면 바로 더할 수 없음을 알고 먼저 간단히 하는가, 뺄셈의 부호를 지키는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(ADD_ROWS)}}],
        table={"key": "f", "rows": ADD_ROWS},
        derive={"ans": "k"},
        constraints=["ans not in (n1, n2, n3, m)", "n1 != n2", "n2 != n3", "n1 != n3"],
        cost_values=["n1", "n2", "n3", "a1", "a2", "a3", "ans"],
        answer_var="ans",
        verify=["ans == a1 + a2 - a3", "a1*a1*m == n1", "a2*a2*m == n2", "a3*a3*m == n3"],
        question="[[sqrt({n1})]] + [[sqrt({n2})]] − [[sqrt({n3})]] = k[[sqrt({m})]]일 때, 상수 k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="근호 안이 다른 수는 그대로 더하거나 뺄 수 없다. 각각을 a√m 꼴로 간단히 하면 세 항 모두 [[sqrt({m})]]{ika(m)} 되므로, 그때 계수끼리 더하고 뺀다(동류항 정리와 같다).",
        sol2=[
            "[[sqrt({n1})]] = [[{R1}]], [[sqrt({n2})]] = [[{R2}]], [[sqrt({n3})]] = [[{R3}]]",
            "[[{R1}]] + [[{R2}]] − [[{R3}]] = ({a1} + {a2} − {a3})[[sqrt({m})]]",
            "따라서 k = {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[{R1}]] + [[{R2}]] − [[{R3}]]", "hint": "각각 a√{m} 꼴로"},
            {"text": "({a1} + {a2} − {a3})[[sqrt({m})]]", "hint": "계수끼리 계산"},
            {"text": "k = {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{n1} = {a1}² × {m}, {n2} = {a2}² × {m}, {n3} = {a3}² × {m}{ro(m)} 근호 안이 모두 {m}{ro(m)} 맞추어지고 {a1} + {a2} − {a3} = {ans}이다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["{a1} + {a2} − {a3} = {ans}", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[sqrt({n1})]] = [[{R1}]], [[sqrt({n2})]] = [[{R2}]], [[sqrt({n3})]] = [[{R3}]]이므로 [[sqrt({n1})]] + [[sqrt({n2})]] − [[sqrt({n3})]] = ({a1} + {a2} − {a3})[[sqrt({m})]] = {ans}[[sqrt({m})]]이다. 따라서 k = {ans}이다.",
        rubric=[
            {"element": "간단히 하기", "points": 3, "criterion": "세 근호를 [[{R1}]], [[{R2}]], [[{R3}]]{ro(m)} 간단히 했다.", "partial": "하나만 틀렸으면 1점."},
            {"element": "계수 계산", "points": 2, "criterion": "{a1} + {a2} − {a3} = {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t5 — √a(√b − √c) = p + q√m
DIST_ROWS = {}
for _a in (2, 3, 5, 6, 7):
    for _t in (1, 2, 3, 4):
        _b = _a * _t * _t
        for _m in (2, 3, 5, 6, 7, 10):
            if _m == _a:
                continue
            for _t2 in (1, 2, 3):
                _c = _a * _m * _t2 * _t2
                if _c == _b or _c > 150 or _t == _t2:
                    continue
                p, q = _a * _t, _a * _t2
                DIST_ROWS[f"{_a}-{_b}-{_c}"] = {"a": _a, "b": _b, "c": _c, "t": _t, "t2": _t2, "m": _m, "p": p, "q": q, "ab": _a * _b, "ac": _a * _c, "QM": _rt(q, _m), "nq": -q}


def so_t5():
    return tpl(SO, 5, SO_BASE,
        title="√a(√b − √c) = p + q√m — 분배법칙으로 전개 후 p + q",
        skill="근호 앞의 수를 괄호 안의 각 항에 곱하고, 곱한 근호 안을 간단히 해 유리수 부분과 무리수 부분으로 정리하기",
        variant_axis={"√a": "√2~√7", "괄호 안": "제곱수 곱이 되는 항 + 안 되는 항"},
        discriminates="√a × √b가 유리수가 되는 경우를 알아보고, √a × √c는 제곱인수를 꺼내 정리하는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(DIST_ROWS)}}],
        table={"key": "f", "rows": DIST_ROWS},
        derive={"ans": "p - q"},
        constraints=["ans != 0", "ans not in (a, b, c)"],
        cost_values=["a", "b", "c", "ab", "ac", "p", "q", "ans"],
        answer_var="ans",
        verify=["ans == p + nq", "p*p == ab", "q*q*m == ac"],
        question="[[sqrt({a})]]([[sqrt({b})]] − [[sqrt({c})]]) = p + q[[sqrt({m})]]일 때, 유리수 p, q에 대하여 p + q의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분배법칙으로 [[sqrt({a})]]{eul(a)} 괄호 안의 두 항에 각각 곱한다: [[sqrt({a})]] × [[sqrt({b})]] = [[sqrt({ab})]]{eun(ab)} {ab}{ika(ab)} 제곱수라 유리수 {p}{ika(p)} 되고, [[sqrt({a})]] × [[sqrt({c})]] = [[sqrt({ac})]]{eun(ac)} 제곱인수를 꺼내 [[{QM}]]{ika(m)} 된다. 그래서 유리수 부분 p와 [[sqrt({m})]]의 계수 q를 읽는다.",
        sol2=[
            "[[sqrt({a})]] × [[sqrt({b})]] = [[sqrt({ab})]] = {p}",
            "[[sqrt({a})]] × [[sqrt({c})]] = [[sqrt({ac})]] = [[{QM}]]",
            "따라서 [[sqrt({a})]]([[sqrt({b})]] − [[sqrt({c})]]) = {p} − [[{QM}]]이므로 p = {p}, q = {nq}, p + q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[sqrt({ab})]] = {p}", "hint": "{ab} = {p}² — 유리수"},
            {"text": "[[sqrt({ac})]] = [[{QM}]]", "hint": "{ac} = {q}² × {m}"},
            {"text": "{p} − [[{QM}]] → p + q = {ans}", "marks": [{"on": "{ans}", "note": "q = {nq} (부호!)"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="q는 [[sqrt({m})]]의 계수이므로 빼는 항의 부호를 붙여 {nq}이다(q = {q}{ro(q)} 쓰면 틀린다). p + q = {p} + {pn(nq)} = {ans}이다.",
        sol3_fig=steps(["p = {p}, q = {nq}", "p + q = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[sqrt({a})]]([[sqrt({b})]] − [[sqrt({c})]]) = [[sqrt({ab})]] − [[sqrt({ac})]] = {p} − [[{QM}]]이므로 p = {p}, q = {nq}이고 p + q = {ans}이다.",
        rubric=[
            {"element": "전개", "points": 3, "criterion": "분배법칙으로 [[sqrt({ab})]] − [[sqrt({ac})]]{eul(ac)} 얻고 각각 {p}, [[{QM}]]{ro(m)} 간단히 했다.", "partial": "한 항만 간단히 했으면 1점."},
            {"element": "p, q 읽기", "points": 2, "criterion": "p = {p}, q = {nq}{ro(nq)} 읽어 p + q = {ans}{eul(ans)} 구했다.", "partial": "q의 부호를 틀렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


SO_SEED = {
    "seed_id": SO, "category": "연산",
    "title": "근호를 포함한 식의 계산 — 간단히 하기·곱셈·유리화·덧셈뺄셈·분배법칙",
    "unit_id": "m3-1", "concept_ids": ["m3-1-04", "m3-1-05", "m3-1-06"],
    "schema_id": None, "schema_name": "제곱근의 곱셈·나눗셈·덧셈·뺄셈과 분모의 유리화",
    "source_item_ids": [],
    "note": "근호 안·계수는 표에서 제곱인수를 미리 분리(sqfree). 답은 k + m 같은 수치. 마커 본문 조각 _rt(k, m) = 'k*sqrt(m)'(k = 1 이면 'sqrt(m)').",
    "geometry": False,
    "templates": [so_t1_final(), so_t2(), so_t3(), so_t4(), so_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 곱셈 공식
MF = "m3-1-mult-formula"
MF_BASE = {**BASE, "prereq": ["다항식의 곱셈", "동류항 정리"], "ops": ["곱셈 공식"], "traps": ["가운데 항 2ab", "부호"], "tags": ["곱셈 공식"]}


def _sg(v: int) -> str:
    return "+" if v > 0 else "−"


# t1 — (ax + b)(cx + d) 전개 → x 의 계수 (또는 두 문자 xy 의 계수)
VAR_ROWS = {"one": {"Y": "", "Y2": "", "T": "x", "w": 0}, "two": {"Y": "y", "Y2": "y²", "T": "xy", "w": 1}}


def mf_t1():
    return tpl(MF, 1, MF_BASE,
        title="(ax + b)(cx + d) 전개식에서 x(또는 xy)의 계수",
        skill="분배법칙으로 전개해 바깥 항의 곱과 안쪽 항의 곱을 더해 가운데 항의 계수 읽기",
        variant_axis={"계수": "1~4, ±1~±6", "문자": "x 하나 / x, y 둘"},
        discriminates="가운데 항이 ad + bc(두 곱의 합)임을 알고 부호를 지켜 더하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [1, 4]}}, {"name": "b", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}},
                {"name": "c", "values": {"int": [1, 4]}}, {"name": "d", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}},
                {"name": "v", "values": {"in": ["one", "two"]}}],
        table={"key": "v", "rows": VAR_ROWS},
        derive={"ac": "a*c", "ad": "a*d", "bc": "b*c", "bd": "b*d", "ans": "a*d + b*c"},
        constraints=["ans*ans != 1", "ans != ac", "ans != bd", "ans not in (a, b, c, d)", "w == 0 or (b*b != 1 and d*d != 1)", "not (a == 1 and c == 1 and w == 1)", "not (a == c and b == d)"],
        cost_values=["a", "b", "c", "d", "ac", "ad", "bc", "bd", "ans"],
        answer_var="ans",
        verify=["ans == ad + bc", "ac == a*c", "bd == b*d"],
        question="({co(a)}x {sgn(b)}{Y})({co(c)}x {sgn(d)}{Y})의 전개식에서 {T}의 계수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="앞 괄호의 각 항을 뒤 괄호의 각 항에 모두 곱한다(분배법칙). (ax + b)(cx + d) = acx² + (ad + bc)x + bd에서 가운데 항의 계수는 바깥 항끼리의 곱 ad와 안쪽 항끼리의 곱 bc를 더한 것이다 — 두 곱의 부호를 각각 정한 뒤 더한다.",
        sol2=[
            "{co(a)}x × {co(c)}x = {co(ac)}x²",
            "바깥 항의 곱 {co(a)}x × ({d}{Y}) = {co(ad)}x{Y}, 안쪽 항의 곱 ({b}{Y}) × {co(c)}x = {co(bc)}x{Y}",
            "전개식은 {co(ac)}x² {sgn(ans)}x{Y} {sgn(bd)}{Y2}이므로 {T}의 계수는 {ad} + {pn(bc)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(ac)}x²", "hint": "앞 항끼리"},
            {"text": "ad = {ad},  bc = {bc}", "hint": "바깥 항끼리, 안쪽 항끼리", "marks": [{"on": "{ad}", "note": "ad"}]},
            {"text": "{co(ac)}x² {sgn(ans)}x{Y} {sgn(bd)}{Y2}", "marks": [{"on": "{sgn(ans)}x{Y}", "note": "계수 {ans}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("mark:2-0")]],
        sol3="가운데 항은 두 곱의 합이다: {a} × {pn(d)} = {ad}, {b} × {c} = {bc}이고 {ad} + {pn(bc)} = {ans}. 상수항 {bd}{ika(bd)} 아니라 x{Y}의 계수를 묻고 있음에 주의하면 답은 {ans}이다.",
        sol3_fig=steps(["{a} × {pn(d)} = {ad},  {b} × {c} = {bc}", "{ad} + {pn(bc)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="({co(a)}x {sgn(b)}{Y})({co(c)}x {sgn(d)}{Y}) = {co(ac)}x² {sgn(ans)}x{Y} {sgn(bd)}{Y2}이므로 {T}의 계수는 {ans}이다.",
        rubric=[
            {"element": "전개", "points": 3, "criterion": "분배법칙으로 전개해 {co(ac)}x² {sgn(ans)}x{Y} {sgn(bd)}{Y2} 꼴을 얻었다.", "partial": "가운데 항의 두 곱 중 하나만 썼으면 1점."},
            {"element": "계수 읽기", "points": 2, "criterion": "{T}의 계수 {ans}{eul(ans)} 답했다.", "partial": "상수항이나 x²의 계수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t2 — (N ± k)² 수의 계산
SQN_ROWS = {"p": {"S": "+", "s": 1, "FORM": "(a + b)² = a² + 2ab + b²"}, "m": {"S": "−", "s": -1, "FORM": "(a − b)² = a² − 2ab + b²"}}


def mf_t2():
    return tpl(MF, 2, MF_BASE,
        title="곱셈 공식을 이용한 수의 계산 — (N ± k)²",
        skill="수를 (기준수 ± 작은 수)로 나누어 완전제곱 공식으로 계산하기",
        variant_axis={"기준수": "30~100·200~500·1000", "k": "1~9", "부호": "+ / −"},
        difficulty=2,
        discriminates="가운데 항 2 × N × k를 빠뜨리지 않고 부호를 맞추는가",
        params=[{"name": "N", "values": {"in": [30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000]}}, {"name": "k", "values": {"int": [1, 9]}}, {"name": "sg", "values": {"in": ["p", "m"]}}],
        table={"key": "sg", "rows": SQN_ROWS},
        derive={"A": "N + s*k", "N2": "N*N", "M": "2*N*k", "k2": "k*k", "NM": "N*N + s*2*N*k", "ans": "(N + s*k)**2"},
        constraints=["ans != A"],
        cost_values=["N", "k", "A", "N2", "M", "k2", "ans"],
        answer_var="ans",
        verify=["ans == A*A", "ans == NM + k2"],
        question="곱셈 공식을 이용하여 {A}²을 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{A} = {N} {S} {k}{ro(k)} 나누어 보면 {FORM}{eul(FORM)} 쓸 수 있다. {N}²과 {k}²은 바로 나오고, 가운데 항 2 × {N} × {k} = {M}{eul(M)} 부호 {S}와 함께 잊지 않는 것이 핵심이다.",
        sol2=[
            "{A}² = ({N} {S} {k})²",
            "= {N}² {S} 2 × {N} × {k} + {k}² = {N2} {S} {M} + {k2}",
            "= {NM} + {k2} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "({N} {S} {k})²", "hint": "기준수 {N}"},
            {"text": "{N2} {S} {M} + {k2}", "hint": "{FORM}", "marks": [{"on": "{S} {M}", "note": "2 × {N} × {k}"}]},
            {"text": "= {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="직접 곱해 확인하면 {A} × {A} = {ans}{ro(ans)} 같다. 가운데 항의 부호는 ({N} {S} {k})²의 {S}{eul(S)} 따르고 마지막 항 {k}² = {k2}{eun(k2)} 항상 더한다.",
        sol3_fig=steps(["{A} × {A} = {ans} ✓", "마지막 항 +{k2}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{A}² = ({N} {S} {k})² = {N}² {S} 2 × {N} × {k} + {k}² = {N2} {S} {M} + {k2} = {ans}이다.",
        rubric=[
            {"element": "공식 적용", "points": 3, "criterion": "{A} = {N} {S} {k}{ro(k)} 놓고 {N2} {S} {M} + {k2}{ro(k2)} 전개했다.", "partial": "가운데 항을 빠뜨렸으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t3 — (N + p)(N − p) 합차 공식
def mf_t3():
    return tpl(MF, 3, MF_BASE,
        title="곱셈 공식을 이용한 수의 계산 — (N + p)(N − p)",
        skill="두 수를 (N + p)(N − p) 꼴로 보고 합차 공식 a² − b²으로 계산하기",
        variant_axis={"기준수": "30~100·200~500·1000", "p": "1~9"},
        difficulty=2,
        discriminates="두 수의 평균을 기준수로 잡아 합차 공식을 쓰는가(N² − p², 가운데 항 없음)",
        params=[{"name": "N", "values": {"in": [30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000]}}, {"name": "p", "values": {"int": [1, 9]}}],
        derive={"A": "N + p", "B": "N - p", "N2": "N*N", "p2": "p*p", "ans": "N*N - p*p"},
        constraints=["ans != A"],
        cost_values=["N", "p", "A", "B", "N2", "p2", "ans"],
        answer_var="ans",
        verify=["ans == A*B", "A - B == 2*p"],
        question="곱셈 공식을 이용하여 {A} × {B}{eul(B)} 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{A}{wa(A)} {B}{eun(B)} {N}{eul(N)}가운데 두고 {p}만큼 크고 작은 수이므로 ({N} + {p})({N} − {p})로 쓸 수 있다. 합차 공식 (a + b)(a − b) = a² − b²을 쓰면 가운데 항 없이 {N}² − {p}²으로 바로 계산된다.",
        sol2=[
            "{A} × {B} = ({N} + {p})({N} − {p})",
            "= {N}² − {p}² = {N2} − {p2}",
            "= {ans}",
        ],
        sol2_fig=steps([
            {"text": "({N} + {p})({N} − {p})", "hint": "기준수 {N}, 차 {p}"},
            {"text": "{N2} − {p2}", "hint": "(a + b)(a − b) = a² − b²", "marks": [{"on": "− {p2}", "note": "p² 을 뺀다"}]},
            {"text": "= {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="직접 곱해 확인하면 {A} × {B} = {ans}{ro(ans)} 같다. {N}² = {N2}보다 {p}² = {p2}만큼 작아지는 것이 합차 공식의 뜻이다.",
        sol3_fig=steps(["{A} × {B} = {ans} ✓", "{N2} − {p2} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{A} × {B} = ({N} + {p})({N} − {p}) = {N}² − {p}² = {N2} − {p2} = {ans}이다.",
        rubric=[
            {"element": "공식 적용", "points": 3, "criterion": "({N} + {p})({N} − {p}) = {N2} − {p2}{ro(p2)} 썼다.", "partial": "가운데 항을 넣어 (N + p)² 꼴로 계산했으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — (N + p)(N + q) (x + a)(x + b) 공식
def mf_t4():
    return tpl(MF, 4, MF_BASE,
        title="곱셈 공식을 이용한 수의 계산 — (N + p)(N + q)",
        skill="두 수를 기준수 N에 대한 (N + p)(N + q)로 보고 N² + (p + q)N + pq로 계산하기",
        variant_axis={"기준수": "30~100·200·300", "p": "1~9", "q": "±1~±9"},
        difficulty=3,
        discriminates="(x + a)(x + b) = x² + (a + b)x + ab에서 a + b와 ab의 부호를 각각 바르게 정하는가",
        params=[{"name": "N", "values": {"in": [30, 40, 50, 60, 70, 80, 90, 100, 200, 300]}}, {"name": "p", "values": {"int": [1, 9]}}, {"name": "q", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}],
        derive={"A": "N + p", "B": "N + q", "N2": "N*N", "s": "p + q", "sN": "(p + q)*N", "pq": "p*q", "ans": "(N + p)*(N + q)"},
        constraints=["q != p", "q != -p", "ans != A"],
        cost_values=["N", "p", "q", "A", "B", "N2", "s", "sN", "pq", "ans"],
        answer_var="ans",
        verify=["ans == A*B", "ans == N2 + sN + pq"],
        question="곱셈 공식을 이용하여 {A} × {B}{eul(B)} 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{A} = {N} + {p}, {B} = {N} {sgn(q)}{ro(q)} 나누면 (x + a)(x + b) = x² + (a + b)x + ab에서 x = {N}, a = {p}, b = {q}인 꼴이다. a + b = {s}, ab = {pq}{eul(pq)} 부호까지 정확히 구해 대입한다.",
        sol2=[
            "{A} × {B} = ({N} + {p})({N} {sgn(q)})",
            "= {N}² + ({p} {sgn(q)}) × {N} + {p} × {pn(q)} = {N2} {sgn(sN)} {sgn(pq)}",
            "= {ans}",
        ],
        sol2_fig=steps([
            {"text": "({N} + {p})({N} {sgn(q)})", "hint": "기준수 {N}"},
            {"text": "{N2} {sgn(sN)} {sgn(pq)}", "hint": "x² + (a + b)x + ab", "marks": [{"on": "{sgn(sN)}", "note": "(a + b)x = {s} × {N}"}, {"on": "{sgn(pq)}", "note": "ab = {pq}"}]},
            {"text": "= {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="직접 곱해 확인하면 {A} × {B} = {ans}{ro(ans)} 같다. (a + b)x의 부호는 a + b = {s}의 부호를, ab의 부호는 {p} × {pn(q)} = {pq}의 부호를 따른다.",
        sol3_fig=steps(["{A} × {B} = {ans} ✓", "a + b = {s}, ab = {pq}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{A} × {B} = ({N} + {p})({N} {sgn(q)}) = {N}² + ({p} {sgn(q)}) × {N} + {p} × {pn(q)} = {N2} {sgn(sN)} {sgn(pq)} = {ans}이다.",
        rubric=[
            {"element": "공식 적용", "points": 3, "criterion": "({N} + {p})({N} {sgn(q)}) = {N2} {sgn(sN)} {sgn(pq)}{ro(pq)} 전개했다.", "partial": "a + b 또는 ab의 부호가 틀렸으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t5 — (p√a + q)² = m + n√a
PS_ROWS = {}
for _p in (1, 2, 3):
    for _a in (2, 3, 5, 6, 7, 10):
        PS_ROWS[f"{_p}-{_a}"] = {"p": _p, "a": _a, "PS": _rt(_p, _a), "PA": _p * _p * _a}


def mf_t5():
    return tpl(MF, 5, MF_BASE,
        title="(p√a + q)² = m + n√a — m + n",
        skill="완전제곱 공식을 무리수에 적용해 유리수 부분과 √a의 계수를 나누어 정리하기",
        variant_axis={"p": "1~3", "a": "2·3·5·6·7·10", "q": "±1~±4"},
        difficulty=3,
        discriminates="(√a)² = a로 바꾸고 가운데 항 2pq√a의 부호를 지키며, 유리수 부분과 무리수 부분을 나누어 읽는가",
        params=[{"name": "f", "values": {"in": list(PS_ROWS)}}, {"name": "q", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}],
        table={"key": "f", "rows": PS_ROWS},
        derive={"q2": "q*q", "m": "PA + q*q", "n": "2*p*q", "ans": "PA + q*q + 2*p*q"},
        constraints=["ans != 0", "ans not in (a, m, n, PA, q)"],
        cost_values=["p", "a", "q", "PA", "q2", "m", "n", "ans"],
        answer_var="ans",
        verify=["ans == m + n", "m == PA + q2", "n == 2*p*q"],
        question="[[pow({PS} {sgn(q)}, 2)]] = m + n[[sqrt({a})]]일 때, 유리수 m, n에 대하여 m + n의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="(a + b)² = a² + 2ab + b²에 a = [[{PS}]], b = {q}{eul(q)} 넣는다. ([[{PS}]])² = {PA}, {pn(q)}² = {q2}{eun(q2)} 유리수이고, 가운데 항 2 × [[{PS}]] × {pn(q)} = {n}[[sqrt({a})]]{eun(a)} 무리수 부분이다. 유리수끼리 모아 m, [[sqrt({a})]]의 계수를 n으로 읽는다.",
        sol2=[
            "([[{PS}]])² = {PA},  2 × [[{PS}]] × {pn(q)} = {n}[[sqrt({a})]],  {pn(q)}² = {q2}",
            "[[pow({PS} {sgn(q)}, 2)]] = {PA} + {q2} {sgn(n)}[[sqrt({a})]] = {m} {sgn(n)}[[sqrt({a})]]",
            "따라서 m = {m}, n = {n}이고 m + n = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{PA} {sgn(n)}[[sqrt({a})]] + {q2}", "hint": "a² + 2ab + b²"},
            {"text": "{m} {sgn(n)}[[sqrt({a})]]", "hint": "유리수끼리 모으기", "marks": [{"on": "{m}", "note": "m"}, {"on": "{sgn(n)}[[sqrt({a})]]", "note": "n = {n}"}]},
            {"text": "m + n = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="m은 유리수 부분 {PA} + {q2} = {m}, n은 [[sqrt({a})]]의 계수이다: 2 × [[{PS}]] × {pn(q)} = {n}[[sqrt({a})]]에서 n = {n}. 가운데 항의 부호는 {pn(q)}의 부호를 따른다. 따라서 m + n = {ans}이다.",
        sol3_fig=steps(["m = {PA} + {q2} = {m}", "n = {n},  m + n = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[pow({PS} {sgn(q)}, 2)]] = ([[{PS}]])² + 2 × [[{PS}]] × {pn(q)} + {pn(q)}² = {PA} {sgn(n)}[[sqrt({a})]] + {q2} = {m} {sgn(n)}[[sqrt({a})]]이므로 m = {m}, n = {n}이고 m + n = {ans}이다.",
        rubric=[
            {"element": "전개", "points": 3, "criterion": "완전제곱 공식으로 {m} {sgn(n)}[[sqrt({a})]]{eul(a)} 얻었다.", "partial": "가운데 항을 빠뜨리거나 (√{a})²을 √{a}로 두었으면 1점."},
            {"element": "m, n 읽기", "points": 2, "criterion": "m = {m}, n = {n}{ro(n)} 읽어 m + n = {ans}{eul(ans)} 구했다.", "partial": "n의 부호가 틀렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t6 — 켤레를 이용한 분모의 유리화 c/(√a ± b), c/(b ± √a) → p + q√a
def _rc_rows():
    out = {}
    for _a in (2, 3, 5, 6, 7, 10, 11, 13):
        for _b in (1, 2, 3, 4):
            D0 = _a - _b * _b
            if D0 == 0:
                continue
            order, D = ("r", D0) if D0 > 0 else ("n", -D0)
            for _s in (1, -1):
                for _k in (1, 2, 3):
                    c = _k * D
                    if c > 30:
                        continue
                    if order == "r":     # (√a + s·b)(√a − s·b) = a − b²
                        den, conj = f"sqrt({_a}) {_sg(_s)} {_b}", f"sqrt({_a}) {_sg(-_s)} {_b}"
                        num = f"{_rt(c, _a)} {_sg(-_s)} {c * _b}"                    # c√a − s·c·b
                        p, q = -_s * c * _b // D, c // D
                        sq = f"{_a} − {_b * _b}"
                        chk1, chk2 = f"{pn_(p)} × {pn_(_s * _b)} + {pn_(q)} × {_a}", f"{pn_(p)} + {pn_(q)} × {pn_(_s * _b)}"      # (p + q√a)(√a + s·b)
                        v1, v2 = p * _s * _b + q * _a, p + q * _s * _b
                    else:                # (b + s·√a)(b − s·√a) = b² − a
                        den, conj = f"{_b} {_sg(_s)} sqrt({_a})", f"{_b} {_sg(-_s)} sqrt({_a})"
                        num = f"{c * _b} {_sg(-_s)} {_rt(c, _a)}"                    # c·b − s·c√a
                        p, q = c * _b // D, -_s * c // D
                        sq = f"{_b * _b} − {_a}"
                        chk1, chk2 = f"{pn_(p)} × {_b} + {pn_(q)} × {pn_(_s * _a)}", f"{pn_(p)} × {pn_(_s)} + {pn_(q)} × {_b}"    # (p + q√a)(b + s√a)
                        v1, v2 = p * _b + q * _s * _a, p * _s + q * _b
                    res = f"{p} {_sg(q)} {_rt(abs(q), _a)}"
                    out[f"{_a}-{_b}-{_s}-{_k}"] = {"a": _a, "b": _b, "c": c, "D": D, "DEN": den, "CONJ": conj, "NUM": num, "SQ": sq, "RES": res, "p": p, "q": q, "CHK1": chk1, "CHK2": chk2, "V1": v1, "V2": v2}
    return out


def pn_(v: int) -> str:
    return f"({v})" if v < 0 else str(v)


RC_ROWS = _rc_rows()


def mf_t6():
    return tpl(MF, 6, MF_BASE,
        title="켤레를 곱하는 분모의 유리화 — c/(√a ± b)를 p + q√a로",
        skill="분모의 켤레(부호만 바꾼 식)를 분자·분모에 곱해 합차 공식으로 분모를 유리수로 만들기",
        variant_axis={"a": "2~13 (제곱인수 없음)", "b": "1~4", "순서·부호": "√a ± b / b ± √a"},
        difficulty=3,
        discriminates="켤레를 곱하면 분모가 a − b²(또는 b² − a)이 됨을 알고, 분자도 같은 식을 곱해 전개하는가",
        params=[{"name": "f", "values": {"in": list(RC_ROWS)}}],
        table={"key": "f", "rows": RC_ROWS},
        derive={"ans": "p + q"},
        constraints=["ans != 0", "ans not in (a, b, c)"],
        cost_values=["a", "b", "c", "D", "p", "q", "ans"],
        answer_var="ans",
        verify=["ans == p + q", "V1 == c", "V2 == 0"],
        question="[[frac({c}, {DEN})]]의 분모를 유리화하여 p + q[[sqrt({a})]] 꼴로 나타낼 때, 유리수 p, q에 대하여 p + q의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분모가 [[{DEN}]]처럼 두 항이면 부호만 바꾼 켤레 [[{CONJ}]]{eul(CONJ)} 분자와 분모에 함께 곱한다. 합차 공식 (a + b)(a − b) = a² − b²에 따라 분모는 {SQ} = {D}{ika(D)} 되어 근호가 사라지고, 분자 {c}([[{CONJ}]]){eun(CONJ)} 전개해 유리수 부분과 [[sqrt({a})]]의 계수로 나눈다.",
        sol2=[
            "분모: ([[{DEN}]])([[{CONJ}]]) = {SQ} = {D}",
            "분자: {c}([[{CONJ}]]) = [[{NUM}]]",
            "분자를 {D}{ro(D)} 나누면 [[{RES}]]이므로 p = {p}, q = {q}, p + q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "분모 {SQ} = {D}", "hint": "켤레 [[{CONJ}]]{eul(CONJ)} 곱함"},
            {"text": "분자 [[{NUM}]]", "hint": "{c} × 켤레"},
            {"text": "[[{RES}]] → p + q = {ans}", "marks": [{"on": "[[{RES}]]", "note": "p = {p}, q = {q}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="검산: ([[{RES}]]) × ([[{DEN}]])의 전개에서 유리수 부분은 {CHK1} = {c}, [[sqrt({a})]]의 계수는 {CHK2} = 0이 되어 원래 분자 {c}{ika(c)} 나온다. 따라서 p + q = {ans}이다.",
        sol3_fig=steps(["([[{RES}]])([[{DEN}]]) = {c} ✓", "p + q = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({c}, {DEN})]]의 분자·분모에 [[{CONJ}]]{eul(CONJ)} 곱하면 분모는 {SQ} = {D}, 분자는 [[{NUM}]]이므로 [[{RES}]]이다. 따라서 p = {p}, q = {q}이고 p + q = {ans}이다.",
        rubric=[
            {"element": "켤레 곱하기", "points": 3, "criterion": "[[{CONJ}]]{eul(CONJ)} 분자·분모에 곱해 분모 {D}, 분자 [[{NUM}]]{eul(NUM)} 얻었다.", "partial": "분모에만 곱했거나 켤레의 부호가 틀렸으면 인정하지 않는다."},
            {"element": "p, q 읽기", "points": 2, "criterion": "[[{RES}]]에서 p = {p}, q = {q}{ro(q)} 읽어 p + q = {ans}{eul(ans)} 구했다.", "partial": "약분(나눗셈)을 하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t7 — 곱셈 공식의 변형: x ± y, xy → x² + y², (x ∓ y)²
VF_ROWS = {
    "ss": {"G": "x + y", "ASK": "x² + y²", "FORM": "x² + y² = (x + y)² − 2xy", "k": -2, "KT": "− 2", "D": 1},
    "ds": {"G": "x − y", "ASK": "x² + y²", "FORM": "x² + y² = (x − y)² + 2xy", "k": 2, "KT": "+ 2", "D": -1},
    "sd": {"G": "x + y", "ASK": "(x − y)²", "FORM": "(x − y)² = (x + y)² − 4xy", "k": -4, "KT": "− 4", "D": 1},
    "dd": {"G": "x − y", "ASK": "(x + y)²", "FORM": "(x + y)² = (x − y)² + 4xy", "k": 4, "KT": "+ 4", "D": -1},
}


def mf_t7():
    return tpl(MF, 7, MF_BASE,
        title="곱셈 공식의 변형 — x ± y와 xy의 값으로 x² + y², (x ∓ y)² 구하기",
        skill="(x + y)² = x² + 2xy + y², (x − y)² = x² − 2xy + y²을 변형해 주어진 두 값으로 식의 값 구하기",
        variant_axis={"주어진 합·차": "±1~±9", "xy": "±1~±12", "형태": "4가지"},
        difficulty=3,
        discriminates="x² + y² = (x ± y)² ∓ 2xy, (x ∓ y)² = (x ± y)² ∓ 4xy의 부호와 계수(2, 4)를 바르게 쓰는가",
        params=[{"name": "s", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}, {"name": "p", "values": {"in": [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}}, {"name": "v", "values": {"in": ["ss", "ds", "sd", "dd"]}}],
        table={"key": "v", "rows": VF_ROWS},
        derive={"s2": "s*s", "kp": "k*p", "ans": "s*s + k*p"},
        constraints=["ans != 0", "s*s - D*4*p >= 0", "ans not in (s, p)"],
        cost_values=["s", "p", "s2", "kp", "ans"],
        answer_var="ans",
        verify=["ans == s2 + kp", "kp == k*p"],
        question="{G} = {s}, xy = {p}일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="곱셈 공식 (x + y)² = x² + 2xy + y², (x − y)² = x² − 2xy + y²을 변형하면 {FORM}{ika(FORM)} 된다. 여기에 {G} = {s}, xy = {p}{eul(p)} 대입한다 — 부호와 계수({KT}xy)를 공식 그대로 옮기는 것이 핵심이다.",
        sol2=[
            "{FORM}",
            "{ASK} = {pn(s)}² {KT} × {pn(p)} = {s2} {sgn(kp)}",
            "= {ans}",
        ],
        sol2_fig=steps([
            {"text": "{FORM}", "hint": "곱셈 공식의 변형"},
            {"text": "{pn(s)}² {KT} × {pn(p)}", "hint": "{G} = {s}, xy = {p} 대입", "marks": [{"on": "{KT} × {pn(p)}", "note": "부호·계수 확인"}]},
            {"text": "{s2} {sgn(kp)} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{ASK}{eun(ASK)} {G}의 제곱 {s2}에서 xy의 {KT}배, 즉 {sgn(kp)}{eul(kp)} 더한 값이다. {s2} {sgn(kp)} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{s2} {sgn(kp)} = {ans}", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{FORM}이므로 {ASK} = {pn(s)}² {KT} × {pn(p)} = {s2} {sgn(kp)} = {ans}이다.",
        rubric=[
            {"element": "공식 변형", "points": 3, "criterion": "공식의 변형으로 {FORM} 꼴을 세웠다.", "partial": "부호나 계수(2, 4)가 틀렸으면 1점."},
            {"element": "대입·계산", "points": 2, "criterion": "{s2} {sgn(kp)} = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t8 — x ± 1/x = s → x² + 1/x², (x ∓ 1/x)²
XR_ROWS = {
    "ss": {"G": "x + [[frac(1, x)]]", "ASK": "x² + [[frac(1, pow(x,2))]]", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x + frac(1, x), 2)]] − 2", "k": -2, "KT": "− 2"},
    "ds": {"G": "x − [[frac(1, x)]]", "ASK": "x² + [[frac(1, pow(x,2))]]", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x − frac(1, x), 2)]] + 2", "k": 2, "KT": "+ 2"},
    "sd": {"G": "x + [[frac(1, x)]]", "ASK": "[[pow(x − frac(1, x), 2)]]", "FORM": "[[pow(x − frac(1, x), 2)]] = [[pow(x + frac(1, x), 2)]] − 4", "k": -4, "KT": "− 4"},
    "dd": {"G": "x − [[frac(1, x)]]", "ASK": "[[pow(x + frac(1, x), 2)]]", "FORM": "[[pow(x + frac(1, x), 2)]] = [[pow(x − frac(1, x), 2)]] + 4", "k": 4, "KT": "+ 4"},
}


def mf_t8():
    return tpl(MF, 8, MF_BASE,
        title="x ± 1/x = s일 때 x² + 1/x², (x ∓ 1/x)²의 값",
        skill="x와 1/x의 곱이 1임을 이용해 곱셈 공식의 변형 (x ± 1/x)² ∓ 2로 식의 값 구하기",
        variant_axis={"s": "±2~±9", "형태": "4가지"},
        difficulty=3,
        discriminates="x × (1/x) = 1이므로 2xy 자리에 2가 옴을 알고 부호를 바르게 쓰는가",
        params=[{"name": "s", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9]}}, {"name": "v", "values": {"in": ["ss", "ds", "sd", "dd"]}}],
        table={"key": "v", "rows": XR_ROWS},
        derive={"s2": "s*s", "ans": "s*s + k"},
        constraints=["ans != s", "ans > 0"],
        cost_values=["s", "s2", "ans"],
        answer_var="ans",
        verify=["ans == s2 + k"],
        question="{G} = {s}일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x와 [[frac(1, x)]]의 곱은 항상 1이므로 곱셈 공식의 변형에서 2xy 자리에 2 × 1 = 2가 온다: {FORM}. 주어진 값 {s}{eul(s)} 대입하면 된다.",
        sol2=[
            "{FORM}",
            "{ASK} = {pn(s)}² {KT} = {s2} {KT}",
            "= {ans}",
        ],
        sol2_fig=steps([
            {"text": "{FORM}", "hint": "x × 1/x = 1"},
            {"text": "{pn(s)}² {KT}", "hint": "{G} = {s} 대입", "marks": [{"on": "{KT}", "note": "2xy = 2 (또는 4xy = 4)"}]},
            {"text": "{s2} {KT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{ASK}{eun(ASK)} ({G})² = {s2}에서 {KT}{eul(KT)} 한 값이다. {s2} {KT} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{s2} {KT} = {ans}", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{FORM}이므로 {ASK} = {pn(s)}² {KT} = {s2} {KT} = {ans}이다.",
        rubric=[
            {"element": "공식 변형", "points": 3, "criterion": "공식의 변형으로 {FORM} 꼴을 세웠다.", "partial": "2xy 자리에 2가 아닌 값을 썼으면 1점."},
            {"element": "대입·계산", "points": 2, "criterion": "{s2} {KT} = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t9 — x² ± sx ± 1 = 0 → x ± 1/x → x² + 1/x²
XE_ROWS = {
    "mp": {"SG1": "−", "C": "+ 1", "GT": "x + [[frac(1, x)]]", "gs": 1, "k": -2, "KT": "− 2", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x + frac(1, x), 2)]] − 2"},
    "pp": {"SG1": "+", "C": "+ 1", "GT": "x + [[frac(1, x)]]", "gs": -1, "k": -2, "KT": "− 2", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x + frac(1, x), 2)]] − 2"},
    "mm": {"SG1": "−", "C": "− 1", "GT": "x − [[frac(1, x)]]", "gs": 1, "k": 2, "KT": "+ 2", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x − frac(1, x), 2)]] + 2"},
    "pm": {"SG1": "+", "C": "− 1", "GT": "x − [[frac(1, x)]]", "gs": -1, "k": 2, "KT": "+ 2", "FORM": "x² + [[frac(1, pow(x,2))]] = [[pow(x − frac(1, x), 2)]] + 2"},
}


def mf_t9():
    return tpl(MF, 9, MF_BASE,
        title="x² ± sx ± 1 = 0일 때 x² + 1/x²의 값",
        skill="x ≠ 0이므로 양변을 x로 나누어 x ± 1/x의 값을 만든 뒤 곱셈 공식의 변형으로 x² + 1/x² 구하기",
        variant_axis={"s": "2~12", "부호": "4가지"},
        difficulty=3,
        discriminates="이차방정식을 x로 나누면 x ± 1/x가 나옴을 알아채고, 상수항의 부호에 따라 +2인지 −2인지 가리는가",
        params=[{"name": "s", "values": {"int": [2, 12]}}, {"name": "v", "values": {"in": ["mp", "pp", "mm", "pm"]}}],
        table={"key": "v", "rows": XE_ROWS},
        derive={"GV": "gs*s", "s2": "s*s", "ans": "s*s + k"},
        constraints=["ans != s", "ans > 0"],
        cost_values=["s", "GV", "s2", "ans"],
        answer_var="ans",
        verify=["ans == s2 + k", "GV*GV == s2"],
        question="x² {SG1} {s}x {C} = 0일 때, x² + [[frac(1, pow(x,2))]]의 값을 구하시오. (단, x ≠ 0)",
        answer="{ans}", answer_alt=[],
        sol1="x ≠ 0이므로 양변을 x로 나눌 수 있다: x {SG1} {s} {C}[[frac(1, x)]] = 0 꼴이 되어 {GT} = {GV}{eul(GV)} 얻는다. 이제 {FORM}에 대입하면 된다 — 상수항이 {C}일 때 x × 1/x = 1이므로 변형 공식의 상수는 {KT}이다.",
        sol2=[
            "양변을 x로 나누면 x {SG1} {s} {C} × [[frac(1, x)]] = 0, 즉 {GT} = {GV}",
            "{FORM}",
            "x² + [[frac(1, pow(x,2))]] = {pn(GV)}² {KT} = {s2} {KT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{GT} = {GV}", "hint": "양변 ÷ x"},
            {"text": "{FORM}", "hint": "곱셈 공식의 변형"},
            {"text": "{pn(GV)}² {KT} = {ans}", "marks": [{"on": "{KT}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{GT}의 값이 {GV}{ika(GV)} 아니라 그 제곱 {s2}{ika(s2)} 쓰이므로 부호는 답에 영향을 주지 않는다. {s2} {KT} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["({GT})² = {s2}", "{s2} {KT} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x ≠ 0이므로 양변을 x로 나누면 {GT} = {GV}이다. {FORM}이므로 x² + [[frac(1, pow(x,2))]] = {pn(GV)}² {KT} = {ans}이다.",
        rubric=[
            {"element": "x로 나누기", "points": 3, "criterion": "양변을 x로 나누어 {GT} = {GV}{eul(GV)} 얻었다.", "partial": "부호가 틀렸어도 제곱하므로 이후가 맞으면 2점."},
            {"element": "변형 공식", "points": 2, "criterion": "{FORM}에 대입해 {ans}{eul(ans)} 구했다.", "partial": "상수 {KT}의 부호가 틀렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t10 — x = c ± √a 대입: x² − 2cx + e 의 값
XS_ROWS = {"p": {"S": "+", "SR": ""}, "m": {"S": "−", "SR": "−"}}


def mf_t10():
    return tpl(MF, 10, MF_BASE,
        title="x = c ± √a일 때 x² − 2cx + e의 값",
        skill="x − c = ±√a로 옮겨 제곱해 x² − 2cx의 값을 먼저 구한 뒤 대입하기",
        variant_axis={"c": "1~5", "a": "2~13 (제곱인수 없음)", "e": "±1~±9"},
        difficulty=3,
        discriminates="무리수를 직접 대입하지 않고 (x − c)² = a로 정리해 x² − 2cx = a − c²을 만드는가",
        params=[{"name": "c", "values": {"int": [1, 5]}}, {"name": "a", "values": {"in": [2, 3, 5, 6, 7, 10, 11, 13]}}, {"name": "e", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}, {"name": "v", "values": {"in": ["p", "m"]}}],
        table={"key": "v", "rows": XS_ROWS},
        derive={"c2": "2*c", "cc": "c*c", "c2c": "2*c*c", "base": "a - c*c", "ans": "a - c*c + e"},
        constraints=["ans != 0", "base != 0", "ans not in (a, c, e, c2)"],
        cost_values=["c", "a", "e", "c2", "cc", "base", "ans"],
        answer_var="ans",
        verify=["ans == base + e", "base == a - cc"],
        question="x = {c} {S} [[sqrt({a})]]일 때, x² − {c2}x {sgn(e)}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="무리수를 그대로 제곱해 대입해도 되지만, x − {c} = {SR}[[sqrt({a})]]{ro(a)} 옮긴 뒤 양변을 제곱하면 근호가 사라진다: (x − {c})² = {a}, 즉 x² − {c2}x + {cc} = {a}. 여기서 x² − {c2}x = {base}{eul(base)} 얻어 대입한다.",
        sol2=[
            "x − {c} = {SR}[[sqrt({a})]]이므로 (x − {c})² = {a}",
            "x² − {c2}x + {cc} = {a}에서 x² − {c2}x = {base}",
            "따라서 x² − {c2}x {sgn(e)} = {base} {sgn(e)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "(x − {c})² = {a}", "hint": "상수를 옮기고 제곱"},
            {"text": "x² − {c2}x = {a} − {cc} = {base}", "hint": "전개 후 정리", "marks": [{"on": "{base}", "note": "x² − {c2}x의 값"}]},
            {"text": "{base} {sgn(e)} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="직접 대입해도 x² = {cc} + {a} {S} {c2}[[sqrt({a})]], {c2}x = {c2c} {S} {c2}[[sqrt({a})]]{ro(a)} 근호 부분이 서로 지워져 x² − {c2}x = {base}{ika(base)} 된다. 따라서 답은 {base} {sgn(e)} = {ans}이다.",
        sol3_fig=steps(["x² − {c2}x = {base} (근호 소거)", "{base} {sgn(e)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x − {c} = {SR}[[sqrt({a})]]의 양변을 제곱하면 x² − {c2}x + {cc} = {a}이므로 x² − {c2}x = {base}이다. 따라서 x² − {c2}x {sgn(e)} = {base} {sgn(e)} = {ans}이다.",
        rubric=[
            {"element": "제곱하여 정리", "points": 3, "criterion": "(x − {c})² = {a}에서 x² − {c2}x = {base}{eul(base)} 얻었다.", "partial": "직접 대입해 근호 항을 바르게 소거했어도 인정한다."},
            {"element": "대입·계산", "points": 2, "criterion": "{base} {sgn(e)} = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


MF_SEED = {
    "seed_id": MF, "category": "연산",
    "title": "곱셈 공식 — 전개 계수·수의 계산(제곱·합차·혼합)·무리수 제곱·켤레 유리화·변형·x ± 1/x·무리수 대입",
    "unit_id": "m3-1", "concept_ids": ["m3-1-07", "m3-1-08", "m3-1-09", "m3-1-10"],
    "schema_id": None, "schema_name": "곱셈 공식과 그 변형",
    "source_item_ids": [],
    "note": "수의 계산은 기준수 N(50~500)·작은 수 k. 켤레 유리화는 표에서 분모·켤레·분자·결과 문자열을 미리 만든다(D | c). 변형은 형태 4행 표.",
    "geometry": False,
    "templates": [mf_t1(), mf_t2(), mf_t3(), mf_t4(), mf_t5(), mf_t6(), mf_t7(), mf_t8(), mf_t9(), mf_t10()],
}


if __name__ == "__main__":
    for seed in (SB_SEED, SO_SEED, MF_SEED):
        with_pitfalls(seed)
        dump(seed)
