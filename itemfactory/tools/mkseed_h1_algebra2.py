# itemfactory/tools/mkseed_h1_algebra2.py — 고1 공통수학1 시드 생성기 ② (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h1_algebra2.py
#     → seeds/h1-1-poly-eq.json  (여러 가지 방정식: 삼차 근과 계수 대칭식·복이차방정식·연립이차(일차+이차)·(α+1)(β+1)(γ+1)·연립(합·제곱합), 5틀)
#     → seeds/h1-1-ineq.json     (부등식: 연립일차 정수 개수·절댓값 정수 개수·이차부등식 해·해→계수·연립이차 정수 개수·항상 성립 범위, 6틀)
#     → seeds/h1-1-count.json    (경우의 수: 합·곱의 법칙·순열·조건 순열·조합·조합 응용, 5틀)
#     → seeds/h1-1-matrix.json   (행렬: 상등·덧셈과 실수배·곱셈·정사각행렬의 거듭제곱 성분, 4틀)
from __future__ import annotations

import os
import sys
from math import comb, factorial, perm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from genkit.expr import ika as _ika  # noqa: E402

# ═══════════════════════════════════════════════════════════════════ 1. 여러 가지 방정식
PE = "h1-1-poly-eq"
PE_B = {**HS, "prereq": ["인수분해", "근과 계수의 관계"], "ops": ["방정식"], "traps": ["근 누락", "부호"], "tags": ["삼차방정식", "연립이차방정식"]}


def pe_t1():
    return T(PE, 1, PE_B, title="삼차방정식의 근과 계수의 관계 — α² + β² + γ²",
        skill="세 근의 합·두 근끼리의 곱의 합·세 근의 곱을 계수로 읽고 대칭식으로 변형하기", axis={"세 근": "−4~4 (서로 다름)", "구하는 것": "제곱의 합 / 역수의 합"}, disc="x³ + ax² + bx + c = 0에서 α + β + γ = −a, αβ + βγ + γα = b, αβγ = −c의 부호를 지키는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-5, 5)}}, {"name": "q", "values": {"in": NZ(-5, 5)}}, {"name": "r", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": ["sq", "inv"]}}],
        table={"key": "k", "rows": {"sq": {"ASK": "α² + β² + γ²", "FORM": "(α + β + γ)² − 2(αβ + βγ + γα)", "w": 1}, "inv": {"ASK": "1/α + 1/β + 1/γ", "FORM": "(αβ + βγ + γα)/(αβγ)", "w": 0}}},
        derive={"a": "-(p + q + r)", "b": "p*q + q*r + r*p", "c": "-p*q*r", "s1": "p + q + r", "s2": "p*q + q*r + r*p", "s3": "p*q*r", "ans": "w*(p*p + q*q + r*r) + (1 - w)*(p*q + q*r + r*p)/(p*q*r)"},
        constraints=["p < q", "q < r", "a != 0", "b != 0", "ans != 0", "ans not in (a, b, c)", "w == 1 or s2 % s3 == 0"], cost=["p", "q", "r", "a", "b", "c", "ans"], verify=["s1 == -a", "s2 == b", "s3 == -c"],
        q="삼차방정식 x³ {sgt(a)}x² {sgt(b)}x {sgn(c)} = 0의 세 근을 α, β, γ라 할 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="삼차방정식 x³ + ax² + bx + c = 0의 세 근에 대하여 α + β + γ = −a, αβ + βγ + γα = b, αβγ = −c이다. 여기서는 α + β + γ = {s1}, αβ + βγ + γα = {s2}, αβγ = {s3}이고, {ASK} = {FORM}으로 변형해 대입한다.",
        sol2=[("α + β + γ = {s1}, αβ + βγ + γα = {s2}, αβγ = {s3}", "삼차의 근과 계수"), ("{ASK} = {FORM}", "대칭식 변형"), ("= {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["세 근은 {p}, {q}, {r}이다(인수분해 (x {sgn(-p)})(x {sgn(-q)})(x {sgn(-r)})). 직접 계산해도 {ASK} = {ans}이다.", "세 근 {p}, {q}, {r}", "{ASK} = {ans}"],
        model="α + β + γ = {s1}, αβ + βγ + γα = {s2}, αβγ = {s3}이므로 {ASK} = {FORM} = {ans}이다.",
        rubric=[("근과 계수", 2, "세 관계식의 값 {s1}, {s2}, {s3}{eul(s3)} 바르게 읽었다.", "부호가 하나라도 틀렸으면 1점."), ("변형·계산", 3, "{ASK} = {FORM}{ro(ans)} 변형해 {ans}{eul(ans)} 구했다.", "변형 공식이 틀렸으면 인정하지 않는다.")],
        pitfalls=[("α + β + γ = a로 부호를 틀림", "근과 계수", "불인정"), ("αβγ = c로 부호를 틀림", "근과 계수", "부분"), ("α² + β² + γ² = (α + β + γ)²으로 둠", "변형·계산", "불인정")])


def pe_t2():
    return T(PE, 2, PE_B, title="복이차방정식 x⁴ + ax² + b = 0 — 실근의 합·제곱의 합",
        skill="x² = t로 치환해 t의 이차방정식을 풀고 x로 되돌리기", axis={"t의 두 근": "p², q² (p, q = 1~10)", "구하는 것": "양의 근의 합 / 모든 근의 제곱의 합 / 절댓값의 합 / 양의 근의 곱"}, disc="x² = t 치환 후 t = p², q²에서 x = ±p, ±q의 네 근을 모두 찾는가", diff=3,
        params=[{"name": "p", "values": {"int": [1, 10]}}, {"name": "q", "values": {"int": [1, 10]}}, {"name": "k", "values": {"in": ["pos", "sq", "abs", "prod"]}}],
        table={"key": "k", "rows": {"pos": {"ASK": "모든 양의 근의 합", "w1": 1, "w2": 0, "w3": 0}, "sq": {"ASK": "모든 근의 제곱의 합", "w1": 0, "w2": 0, "w3": 0}, "abs": {"ASK": "모든 근의 절댓값의 합", "w1": 0, "w2": 1, "w3": 0}, "prod": {"ASK": "모든 양의 근의 곱", "w1": 0, "w2": 0, "w3": 1}}},
        derive={"a": "-(p*p + q*q)", "b": "p*p*q*q", "p2": "p*p", "q2": "q*q", "ans": "w1*(p + q) + w2*2*(p + q) + w3*p*q + (1 - w1 - w2 - w3)*2*(p*p + q*q)"},
        constraints=["p < q", "ans not in (a, b, p2, q2)", "ans != 0"], cost=["p", "q", "a", "b", "ans"], verify=["a == -(p2 + q2)", "b == p2*q2"],
        q="사차방정식 x⁴ {sgt(a)}x² {sgn(b)} = 0의 {ASK}을 구하시오.", answer="{ans}",
        sol1="x² = t로 놓으면 t² {sgt(a)}t {sgn(b)} = 0이고 인수분해하면 (t − {p2})(t − {q2}) = 0이다. t = x² ≥ 0이므로 x² = {p2} 또는 x² = {q2}, 즉 x = ±{p} 또는 x = ±{q}의 네 근을 얻는다.",
        sol2=[("x² = t: t² {sgt(a)}t {sgn(b)} = (t − {p2})(t − {q2}) = 0", "치환"), ("x² = {p2}, {q2} → x = ±{p}, ±{q}", "되돌리기(± 모두)"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["네 근 {p}, −{p}, {q}, −{q}의 합은 0, 양의 근의 합은 {p + q}, 양의 근의 곱은 {p*q}, 절댓값의 합은 {2*(p + q)}, 제곱의 합은 2({p2} + {q2}) = {2*(p2 + q2)}이다. 따라서 {ASK} = {ans}이다.", "근: ±{p}, ±{q}", "{ASK} = {ans}"],
        model="x² = t로 놓으면 (t − {p2})(t − {q2}) = 0이므로 x² = {p2} 또는 x² = {q2}, 즉 x = ±{p}, ±{q}이다. 따라서 {ASK}은 {ans}이다.",
        rubric=[("치환·인수분해", 2, "x² = t로 놓아 (t − {p2})(t − {q2}) = 0을 얻었다.", "인수분해 실수면 1점."), ("근·답", 3, "네 근 ±{p}, ±{q}를 모두 구해 {ASK} {ans}{eul(ans)} 답했다.", "음의 근을 빠뜨렸으면 1점.")],
        pitfalls=[("x = ±√t에서 음의 근을 빠뜨림", "근·답", "부분"), ("t의 근을 x의 근으로 답함", "근·답", "불인정"), ("인수분해 실수", "치환·인수분해", "부분")])


def pe_t3():
    return T(PE, 3, PE_B, title="연립이차방정식(일차 + 이차) — 해에서 x + y의 최댓값",
        skill="일차식을 한 문자에 대해 정리해 이차식에 대입하고 두 해를 모두 구하기", axis={"일차식": "y = x + a", "이차식": "x² + y² = b"}, disc="대입해 얻은 이차방정식의 두 근을 모두 구해 두 해 (x, y)를 완성하는가", diff=3,
        params=[{"name": "x1", "values": {"in": NZ(-6, 6)}}, {"name": "a", "values": {"in": NZ(-6, 6)}}],
        derive={"y1": "x1 + a", "x2": "-a - x1", "y2": "-x1", "b": "x1*x1 + (x1 + a)**2", "s1": "2*x1 + a", "s2": "-a - 2*x1", "ans": "max(2*x1 + a, -a - 2*x1)", "a2b": "a*a - b"},
        constraints=["x1 != x2", "ans != 0", "ans not in (a, b)", "b <= 100"], cost=["x1", "a", "b", "s1", "s2", "ans"], verify=["x2*x2 + y2*y2 == b", "y2 == x2 + a"],
        q="연립방정식 y = x {sgn(a)}, x² + y² = {b}의 해를 (x, y)라 할 때, x + y의 값 중 가장 큰 것을 구하시오.", answer="{ans}",
        sol1="일차식 y = x {sgn(a)}{eul(a)} 이차식에 대입하면 x² + (x {sgn(a)})² = {b}, 정리하면 2x² {sgt(2*a)}x {sgn(a2b)} = 0이다. 이 이차방정식의 두 근 x = {x1}, {x2}에 대해 y를 구하면 두 해가 나온다.",
        sol2=[("대입: x² + (x {sgn(a)})² = {b} → 2x² {sgt(2*a)}x {sgn(a2b)} = 0", "일차식을 대입"), ("x = {x1} 또는 x = {x2} → 해 ({x1}, {y1}), ({x2}, {y2})", "y = x {sgn(a)}"), ("x + y = {s1} 또는 {s2} → 가장 큰 값 {ans}", None, ("{ans}", "x + y의 최댓값"))],
        sol3=["({x1}, {y1}): {x1}² + {pn(y1)}² = {b} ✓, ({x2}, {y2}): {pn(x2)}² + {pn(y2)}² = {b} ✓. 두 해 모두 원래 식을 만족한다. 따라서 답은 {ans}이다.", "두 해 검산 ✓", "x + y 최댓값 {ans}"],
        model="y = x {sgn(a)}{eul(a)} 대입하면 2x² {sgt(2*a)}x {sgn(a2b)} = 0에서 x = {x1} 또는 {x2}이고, 해는 ({x1}, {y1}), ({x2}, {y2})이다. 따라서 x + y의 최댓값은 {ans}이다.",
        rubric=[("대입·풀이", 3, "대입해 x = {x1}, {x2}{eul(x2)} 구했다.", "한 근만 구했으면 1점."), ("해·답", 2, "두 해를 완성해 x + y의 최댓값 {ans}{eul(ans)} 답했다.", "y를 구하지 않았으면 1점.")],
        pitfalls=[("한 해만 구하고 멈춤", "대입·풀이", "부분"), ("대입 후 전개 실수", "대입·풀이", "부분"), ("x의 최댓값을 답함", "해·답", "불인정")])


def pe_t4():
    return T(PE, 4, PE_B, title="삼차방정식의 세 근으로 (α + 1)(β + 1)(γ + 1) 구하기",
        skill="f(x) = (x − α)(x − β)(x − γ)에서 x = −1을 대입해 곱을 한 번에 구하기", axis={"계수": "±1~±6"}, disc="세 근을 구하지 않고 f(−1) = (−1 − α)(−1 − β)(−1 − γ) = −(α + 1)(β + 1)(γ + 1)임을 쓰는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-6, 6)}}],
        derive={"fm1": "-1 + a - b + c", "ans": "1 - a + b - c"},
        constraints=["ans != 0", "ans not in (a, b, c)"], cost=["a", "b", "c", "fm1", "ans"], verify=["ans == -fm1"],
        q="삼차방정식 x³ {sgt(a)}x² {sgt(b)}x {sgn(c)} = 0의 세 근을 α, β, γ라 할 때, (α + 1)(β + 1)(γ + 1)의 값을 구하시오.", answer="{ans}",
        sol1="f(x) = x³ {sgt(a)}x² {sgt(b)}x {sgn(c)}{eun(c)} 세 근으로 f(x) = (x − α)(x − β)(x − γ)로 인수분해된다. x = −1을 넣으면 f(−1) = (−1 − α)(−1 − β)(−1 − γ) = −(α + 1)(β + 1)(γ + 1)이므로 구하는 값은 −f(−1)이다.",
        sol2=[("f(x) = (x − α)(x − β)(x − γ)", "인수분해 꼴"), ("f(−1) = (−1 − α)(−1 − β)(−1 − γ) = −(α + 1)(β + 1)(γ + 1)", "x = −1 대입"), ("f(−1) = −1 {sgn(a)} {sgn(-b)} {sgn(c)} = {fm1} → (α + 1)(β + 1)(γ + 1) = {ans}", None, ("{ans}", "답"))],
        sol3=["전개해서 확인하면 (α + 1)(β + 1)(γ + 1) = αβγ + (αβ + βγ + γα) + (α + β + γ) + 1 = {pn(-c)} + {pn(b)} + {pn(-a)} + 1 = {ans}{ro(ans)} 같다. 따라서 답은 {ans}이다.", "αβγ + Σαβ + Σα + 1 = {ans}", "답 {ans}"],
        model="f(x) = (x − α)(x − β)(x − γ)에 x = −1을 대입하면 f(−1) = −(α + 1)(β + 1)(γ + 1)이고 f(−1) = {fm1}이므로 (α + 1)(β + 1)(γ + 1) = {ans}이다.",
        rubric=[("x = −1 대입", 3, "f(−1) = −(α + 1)(β + 1)(γ + 1)임을 밝혔다.", "근과 계수의 관계로 전개해 구했어도 인정한다."), ("계산", 2, "f(−1) = {fm1}에서 {ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("f(−1)의 부호를 그대로 답함", "계산", "불인정"), ("f(1)을 대입함", "x = −1 대입", "불인정"), ("(−1)³·(−1)² 부호 실수", "계산", "부분")])


def pe_t5():
    return T(PE, 5, PE_B, title="연립방정식 x + y = s, x² + y² = t — xy와 (x − y)²",
        skill="x² + y² = (x + y)² − 2xy로 xy를 구하고 (x − y)² = (x + y)² − 4xy로 이어가기", axis={"합": "±2~±9", "곱": "±1~±12"}, disc="근을 직접 구하지 않고 대칭식으로 xy를 끌어내는가", diff=2,
        params=[{"name": "s", "values": {"in": NZ(-9, 9)}}, {"name": "p", "values": {"in": NZ(-12, 12)}}, {"name": "k", "values": {"in": ["xy", "dsq"]}}],
        table={"key": "k", "rows": {"xy": {"ASK": "xy", "w": 1}, "dsq": {"ASK": "(x − y)²", "w": 0}}},
        derive={"t": "s*s - 2*p", "d2": "s*s - 4*p", "ans": "w*p + (1 - w)*(s*s - 4*p)"},
        constraints=["d2 >= 0", "ans != 0", "ans not in (s, t)"], cost=["s", "p", "t", "ans"], verify=["t == s*s - 2*p", "d2 == s*s - 4*p"],
        q="연립방정식 x + y = {s}, x² + y² = {t}의 해 (x, y)에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="x² + y² = (x + y)² − 2xy이므로 {t} = {s}² − 2xy에서 xy = {p}이다. (x − y)² = (x + y)² − 4xy = {s*s} − 4 × {pn(p)} = {d2}로 이어진다.",
        sol2=[("x² + y² = (x + y)² − 2xy → {t} = {s*s} − 2xy", "대칭식"), ("xy = {p}", "곱"), ("(x − y)² = {s*s} − 4 × {pn(p)} = {d2} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["x, y는 t² − ({s})t + {pn(p)} = 0의 두 근이고 판별식 {d2} ≥ 0이므로 실수해가 있다. 따라서 {ASK} = {ans}이다.", "판별식 {d2} ≥ 0 ✓", "{ASK} = {ans}"],
        model="x² + y² = (x + y)² − 2xy이므로 {t} = {s*s} − 2xy에서 xy = {p}이고, (x − y)² = (x + y)² − 4xy = {d2}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("대칭식", 3, "x² + y² = (x + y)² − 2xy로 xy = {p}{eul(p)} 구했다.", "부호 실수면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "(x − y)²에서 2xy로 썼으면 인정하지 않는다.")],
        pitfalls=[("x² + y² = (x + y)²으로 둠", "대칭식", "불인정"), ("(x − y)² = (x + y)² − 2xy로 둠", "답", "부분"), ("이항 부호 실수", "대칭식", "부분")])


PE_SEED = SEED(PE, category="연산", title="여러 가지 방정식 — 삼차 근과 계수·복이차·연립이차(일차+이차)·(α+1)(β+1)(γ+1)·합과 제곱합", unit_id="h1-1", concept_ids=["h1-1-09", "h1-1-10"],
               schema_name="삼차·사차방정식과 연립이차방정식", note="삼차식은 세 정수 근에서 계수를 파생. 연립이차는 x1, a 로 두 해를 만든다(x2 = −a − x1).",
               templates=[pe_t1(), pe_t2(), pe_t3(), pe_t4(), pe_t5()])


# ═══════════════════════════════════════════════════════════════════ 2. 부등식
IQ = "h1-1-ineq"
IQ_B = {**HS, "prereq": ["일차부등식", "이차식의 인수분해"], "ops": ["부등식"], "traps": ["부등호 방향", "경계 포함"], "tags": ["연립부등식", "절댓값", "이차부등식"]}


def iq_t1():
    return T(IQ, 1, IQ_B, title="연립일차부등식의 정수인 해의 개수",
        skill="두 부등식을 각각 풀어 공통 범위를 구하고 그 안의 정수를 세기", axis={"범위": "p < x ≤ q (p, q 정수)"}, disc="각각 푼 뒤 공통 부분을 잡고, 경계 포함 여부(<, ≤)에 따라 정수를 세는가", diff=2,
        params=[{"name": "p", "values": {"int": [-6, 6]}}, {"name": "n", "values": {"int": [2, 7]}}, {"name": "k1", "values": {"int": [2, 4]}}, {"name": "k2", "values": {"int": [2, 4]}}, {"name": "c1", "values": {"in": NZ(-5, 5)}}, {"name": "c2", "values": {"in": NZ(-5, 5)}}],
        derive={"qv": "p + n", "r1": "k1*p + c1", "r2": "k2*(p + n) + c2", "ans": "n"},
        constraints=["ans not in (p, qv, r1, r2)"], cost=["p", "qv", "k1", "k2", "r1", "r2", "ans"], verify=["r1 == k1*p + c1", "r2 == k2*qv + c2"],
        q="연립부등식 {k1}x {sgn(c1)} > {r1}, {k2}x {sgn(c2)} ≤ {r2}를 만족시키는 정수 x의 개수를 구하시오.", answer="{ans}",
        sol1="첫 번째 부등식 {k1}x {sgn(c1)} > {r1}에서 {k1}x > {r1 - c1}, x > {p}. 두 번째 부등식 {k2}x {sgn(c2)} ≤ {r2}에서 {k2}x ≤ {r2 - c2}, x ≤ {qv}. 두 범위의 공통 부분은 {p} < x ≤ {qv}이고, 그 안의 정수는 {p + 1}부터 {qv}까지이다.",
        sol2=[("{k1}x > {r1 - c1} → x > {p}", "첫 번째"), ("{k2}x ≤ {r2 - c2} → x ≤ {qv}", "두 번째"), ("{p} < x ≤ {qv} → 정수 {p + 1}, …, {qv}의 {ans}개", None, ("{ans}개", "{qv} − {p}"))],
        sol3=["x = {p}{eun(p)} 첫 번째 부등식의 등호가 없어 제외되고, x = {qv}{eun(qv)} 두 번째의 등호가 있어 포함된다. 따라서 정수 해는 {ans}개이다.", "{p} 제외 · {qv} 포함", "개수 {ans}"],
        model="첫 번째 부등식에서 x > {p}, 두 번째에서 x ≤ {qv}이므로 {p} < x ≤ {qv}이다. 따라서 정수 x는 {p + 1}, …, {qv}의 {ans}개이다.",
        rubric=[("각각 풀기", 3, "x > {p}, x ≤ {qv}{eul(qv)} 얻었다.", "부등호 방향이 틀렸으면 인정하지 않는다."), ("공통 범위·개수", 2, "{p} < x ≤ {qv}에서 정수 {ans}개를 셌다.", "경계 포함을 틀려 1개 차이면 1점.")],
        pitfalls=[("경계 x = p를 포함해 셈", "공통 범위·개수", "부분"), ("이항 시 부호 실수", "각각 풀기", "부분"), ("두 범위의 합집합을 취함", "공통 범위·개수", "불인정")])


def iq_t2():
    return T(IQ, 2, IQ_B, title="절댓값 기호를 포함한 일차부등식 — 정수 해의 개수",
        skill="|ax − b| < c ⇔ −c < ax − b < c로 벗겨 범위를 구하고 정수를 세기", axis={"a": "2, 3", "b, c": "정수"}, disc="절댓값을 두 부등식으로 벗기고 나눗셈 후 경계가 정수가 아닐 때 정수를 정확히 세는가", diff=3,
        params=[{"name": "a", "values": {"in": [2, 3]}}, {"name": "b", "values": {"in": NZ(-7, 7)}}, {"name": "c", "values": {"int": [3, 12]}}],
        derive={"lo": "(b - c)/a", "hi": "(b + c)/a", "ans": "ceiling((b + c)/a) - floor((b - c)/a) - 1", "L": "b - c", "U": "b + c"},
        constraints=["ans >= 2", "ans not in (a, b, c)"], cost=["a", "b", "c", "L", "U", "ans"], verify=["ans >= 1"],
        q="부등식 [[abs({a}x {sgn(-b)})]] < {c}를 만족시키는 정수 x의 개수를 구하시오.", answer="{ans}",
        sol1="|X| < c ⇔ −c < X < c이다. 따라서 −{c} < {a}x {sgn(-b)} < {c}, 각 변에 {b}{eul(b)} 더하면 {L} < {a}x < {U}, {a}로 나누면 {dec(lo)} < x < {dec(hi)}이다. 이 범위의 정수를 센다.",
        sol2=[("−{c} < {a}x {sgn(-b)} < {c}", "절댓값 벗기기"), ("{L} < {a}x < {U} → {dec(lo)} < x < {dec(hi)}", "이항 후 {a}로 나눔"), ("정수 x의 개수 {ans}", None, ("{ans}", "개수"))],
        sol3=["경계 {dec(lo)}, {dec(hi)}{eun(dec(hi))} 포함되지 않으므로 그 사이의 정수만 센다(경계가 정수이면 제외). 따라서 {ans}개이다.", "{dec(lo)} < x < {dec(hi)}", "정수 {ans}개"],
        model="−{c} < {a}x {sgn(-b)} < {c}에서 {L} < {a}x < {U}, 즉 {dec(lo)} < x < {dec(hi)}이므로 정수 x는 {ans}개이다.",
        rubric=[("절댓값 벗기기", 3, "−{c} < {a}x {sgn(-b)} < {c}{ro(c)} 바꾸어 {dec(lo)} < x < {dec(hi)}{eul(dec(hi))} 얻었다.", "한쪽 부등식만 썼으면 1점."), ("개수", 2, "정수 {ans}개를 셌다.", "경계를 포함해 셌으면 1점.")],
        pitfalls=[("|X| < c를 X < c로만 둠", "절댓값 벗기기", "불인정"), ("경계가 정수가 아닐 때 개수 실수", "개수", "부분"), ("나눗셈 실수", "절댓값 벗기기", "부분")])


def iq_t3():
    return T(IQ, 3, IQ_B, title="이차부등식의 해 — x² + bx + c < 0, ≥ 0",
        skill="좌변을 인수분해해 두 근 사이(또는 바깥)로 해를 쓰기", axis={"두 근": "−7~7", "부등호": "< / ≥"}, disc="x²의 계수가 양수일 때 < 0은 두 근 사이, ≥ 0은 두 근의 바깥(등호 포함)임을 구별하는가", diff=2,
        params=[{"name": "p", "values": {"in": NZ(-7, 7)}}, {"name": "q", "values": {"in": NZ(-7, 7)}}, {"name": "k", "values": {"in": ["lt", "ge"]}}],
        table={"key": "k", "rows": {"lt": {"OP": "<", "KIND": "두 근 사이", "PRE": "", "MID": " < x < ", "POST": ""}, "ge": {"OP": "≥", "KIND": "두 근의 바깥(등호 포함)", "PRE": "x ≤ ", "MID": " 또는 x ≥ ", "POST": ""}}},
        derive={"b": "-(p + q)", "c": "p*q", "np": "-p", "nq": "-q"},
        constraints=["p < q", "b != 0"], cost=["p", "q", "b", "c"], verify=["b == -(p + q)", "c == p*q"], ans_var=None,
        q="이차부등식 x² {sgt(b)}x {sgn(c)} {OP} 0의 해를 구하시오.", answer="{PRE}{p}{MID}{q}{POST}",
        sol1="좌변을 인수분해하면 (x {sgn(np)})(x {sgn(nq)})이고 두 근은 {p}, {q}이다. x²의 계수가 양수이므로 그래프는 아래로 볼록: 부등식 {OP} 0의 해는 {KIND}이다.",
        sol2=[("(x {sgn(np)})(x {sgn(nq)}) {OP} 0", "인수분해"), ("두 근 {p}, {q}, 아래로 볼록", "그래프의 모양"), ("해: {PRE}{p}{MID}{q}{POST}", None, ("{PRE}{p}{MID}{q}{POST}", "{KIND}"))],
        sol3=["두 근 사이의 값을 넣으면 좌변이 음수, 바깥 값을 넣으면 양수가 됨을 확인한다. 따라서 해는 {PRE}{p}{MID}{q}{POST}이다.", "두 근 사이 음수 · 바깥 양수", "해 {PRE}{p}{MID}{q}{POST}"],
        model="x² {sgt(b)}x {sgn(c)} = (x {sgn(np)})(x {sgn(nq)})이므로 부등식 {OP} 0의 해는 {PRE}{p}{MID}{q}{POST}이다.",
        rubric=[("인수분해", 2, "(x {sgn(np)})(x {sgn(nq)}){ro(nq)} 인수분해했다.", "부호 실수면 1점."), ("해", 3, "{PRE}{p}{MID}{q}{POST}{eul(q)} 답했다.", "안팎을 바꾸었거나 등호 포함을 틀렸으면 인정하지 않는다.")],
        pitfalls=[("< 0의 해를 바깥으로 씀", "해", "불인정"), ("≥ 0에서 등호를 빠뜨림", "해", "부분"), ("근의 부호 실수", "인수분해", "부분")])


def iq_t4():
    return T(IQ, 4, IQ_B, title="이차부등식의 해가 주어질 때 계수 구하기",
        skill="해가 p ≤ x ≤ q이면 (x − p)(x − q) ≤ 0을 전개해 계수 비교하기", axis={"해의 범위": "−6~6"}, disc="해에서 두 근을 읽어 (x − p)(x − q) ≤ 0을 만들고 전개해 a, b를 읽는가", diff=2,
        params=[{"name": "p", "values": {"in": NZ(-6, 6)}}, {"name": "q", "values": {"in": NZ(-6, 6)}}],
        derive={"a": "-(p + q)", "b": "p*q", "ans": "-(p + q) + p*q", "np": "-p", "nq": "-q"},
        constraints=["p < q", "a != 0", "ans != 0", "ans not in (p, q)"], cost=["p", "q", "a", "b", "ans"], verify=["a == -(p + q)", "b == p*q"],
        q="이차부등식 x² + ax + b ≤ 0의 해가 {p} ≤ x ≤ {q}일 때, 상수 a, b에 대하여 a + b의 값을 구하시오.", answer="{ans}",
        sol1="해가 {p} ≤ x ≤ {q}인 이차부등식은 두 근이 {p}, {q}이고 x²의 계수가 양수인 (x {sgn(np)})(x {sgn(nq)}) ≤ 0이다. 전개하면 x² {sgt(a)}x {sgn(b)} ≤ 0이므로 계수를 비교한다.",
        sol2=[("(x {sgn(np)})(x {sgn(nq)}) ≤ 0", "해 → 부등식"), ("x² {sgt(a)}x {sgn(b)} ≤ 0", "전개"), ("a = {a}, b = {b} → a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=["a = −(두 근의 합) = −({p} {sgn(q)}) = {a}, b = (두 근의 곱) = {p} × {pn(q)} = {b}로 근과 계수의 관계와 맞는다. 따라서 a + b = {ans}이다.", "a = −(합), b = 곱", "a + b = {ans}"],
        model="해가 {p} ≤ x ≤ {q}이므로 (x {sgn(np)})(x {sgn(nq)}) ≤ 0, 즉 x² {sgt(a)}x {sgn(b)} ≤ 0이다. 따라서 a = {a}, b = {b}이고 a + b = {ans}이다.",
        rubric=[("부등식 세우기", 3, "(x {sgn(np)})(x {sgn(nq)}) ≤ 0을 세워 전개했다.", "근의 부호를 틀렸으면 인정하지 않는다."), ("계수·합", 2, "a = {a}, b = {b}에서 a + b = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("a = 두 근의 합(부호 반대)", "계수·합", "부분"), ("(x + p)(x + q)로 근의 부호를 틀림", "부등식 세우기", "불인정"), ("전개 실수", "부등식 세우기", "부분")])


def iq_t5():
    return T(IQ, 5, IQ_B, title="연립이차부등식 — 정수 x의 개수",
        skill="이차부등식과 일차부등식을 각각 풀어 공통 범위의 정수를 세기", axis={"이차부등식의 두 근": "−6~6", "일차 조건": "x ≥ c"}, disc="이차부등식의 해(두 근 사이)와 일차 조건의 공통 부분을 잡아 정수를 세는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-6, 6)}}, {"name": "q", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"int": [-5, 5]}}],
        derive={"b": "-(p + q)", "cc": "p*q", "lo": "max(p + 1, c)", "ans": "q - max(p + 1, c)", "np": "-p", "nq": "-q"},
        constraints=["p < q", "b != 0", "c > p", "c < q", "ans >= 1", "ans not in (p, q, c)"], cost=["p", "q", "c", "lo", "ans"], verify=["ans == q - lo"],
        q="연립부등식 x² {sgt(b)}x {sgn(cc)} < 0, x ≥ {c}를 만족시키는 정수 x의 개수를 구하시오.", answer="{ans}",
        sol1="이차부등식 x² {sgt(b)}x {sgn(cc)} < 0은 (x {sgn(np)})(x {sgn(nq)}) < 0이므로 해가 {p} < x < {q}이다. 여기에 x ≥ {c}를 함께 만족시키는 범위는 {lo} ≤ x < {q}이고, 그 안의 정수를 센다.",
        sol2=[("(x {sgn(np)})(x {sgn(nq)}) < 0 → {p} < x < {q}", "이차부등식"), ("공통 범위: {lo} ≤ x < {q}", "x ≥ {c}와 겹치는 부분"), ("정수 {lo}, …, {q - 1}의 {ans}개", None, ("{ans}개", "개수"))],
        sol3=["x = {q}{eun(q)} 이차부등식의 등호가 없어 제외된다. 따라서 정수 해는 {ans}개이다.", "{q} 제외", "개수 {ans}"],
        model="x² {sgt(b)}x {sgn(cc)} < 0의 해는 {p} < x < {q}이고 x ≥ {c}와의 공통 범위는 {lo} ≤ x < {q}이다. 따라서 정수 x는 {ans}개이다.",
        rubric=[("이차부등식", 3, "{p} < x < {q}{eul(q)} 구했다.", "안팎을 바꾸었으면 인정하지 않는다."), ("공통 범위·개수", 2, "{lo} ≤ x < {q}에서 {ans}개를 셌다.", "경계 처리 실수로 1개 차이면 1점.")],
        pitfalls=[("x = q를 포함해 셈", "공통 범위·개수", "부분"), ("이차부등식의 해를 바깥으로 씀", "이차부등식", "불인정"), ("일차 조건을 무시함", "공통 범위·개수", "불인정")])


def iq_t6():
    return T(IQ, 6, IQ_B, title="모든 실수 x에 대하여 이차부등식이 성립할 조건 — k의 범위",
        skill="x² + kx + c > 0이 항상 성립하려면 D = k² − 4c < 0임을 쓰기", axis={"c": "완전제곱수 4~49"}, disc="항상 성립 ⇔ 그래프가 x축 위 ⇔ D < 0임을 알고 k의 범위를 푸는가", diff=3,
        params=[{"name": "s", "values": {"int": [2, 7]}}, {"name": "b", "values": {"in": NZ(-5, 5)}}],
        derive={"c": "s*s", "lo": "-2*s", "hi": "2*s", "lo2": "-2*s + b", "hi2": "2*s + b"},
        constraints=["lo2 != 0"], cost=["s", "c", "b", "lo2", "hi2"], verify=["c == s*s"], ans_var=None,
        q="모든 실수 x에 대하여 부등식 x² + (k {sgn(-b)})x + {c} > 0이 성립할 때, 실수 k의 값의 범위를 구하시오.", answer="{lo2} < k < {hi2}",
        sol1="x²의 계수가 양수이므로 부등식이 모든 실수에서 성립하려면 그래프가 x축과 만나지 않아야 한다: 판별식 D = (k {sgn(-b)})² − {4*s*s} < 0. 즉 (k {sgn(-b)})² < {4*s*s}이므로 {lo} < k {sgn(-b)} < {hi}이다.",
        sol2=[("항상 성립 ⇔ D < 0", "그래프가 x축 위"), ("(k {sgn(-b)})² − {4*s*s} < 0 → {lo} < k {sgn(-b)} < {hi}", "판별식"), ("{lo2} < k < {hi2}", None, ("{lo2} < k < {hi2}", "k의 범위"))],
        sol3=["k = {lo2} 또는 {hi2}이면 D = 0이 되어 x축에 접하므로 어떤 x에서 = 0이 되어 > 0이 깨진다. 따라서 {lo2} < k < {hi2}이다.", "경계에서 D = 0 (접함)", "{lo2} < k < {hi2}"],
        model="모든 실수 x에 대하여 성립하려면 D = (k {sgn(-b)})² − {4*s*s} < 0이어야 하므로 {lo} < k {sgn(-b)} < {hi}, 즉 {lo2} < k < {hi2}이다.",
        rubric=[("조건 세우기", 3, "D = (k {sgn(-b)})² − {4*s*s} < 0을 세웠다.", "D > 0으로 세웠으면 인정하지 않는다."), ("범위", 2, "{lo2} < k < {hi2}{eul(hi2)} 구했다.", "경계 포함(≤)으로 썼으면 1점.")],
        pitfalls=[("D ≤ 0으로 등호를 포함함", "범위", "부분"), ("D > 0으로 둠", "조건 세우기", "불인정"), ("k² < 4c에서 한쪽 범위만 씀", "범위", "부분")])


IQ_SEED = SEED(IQ, category="연산", title="부등식 — 연립일차 정수 개수·절댓값 정수 개수·이차부등식의 해·해→계수·연립이차 정수 개수·항상 성립 범위", unit_id="h1-1", concept_ids=["h1-1-11", "h1-1-12", "h1-1-13"],
               schema_name="연립일차부등식·절댓값 부등식·이차부등식", note="범위 답은 문자열(answer_var 없음). 이차부등식의 해는 행(< / ≥)별 문자열을 파생 없이 조립한다.",
               templates=[iq_t1(), iq_t2(), iq_t3(), iq_t4(), iq_t5(), iq_t6()])


# ═══════════════════════════════════════════════════════════════════ 3. 경우의 수
CN = "h1-1-count"
CN_B = {**HS, "prereq": ["합의 법칙·곱의 법칙"], "ops": ["경우의 수"], "traps": ["순열·조합 혼동", "이웃 조건"], "tags": ["순열", "조합"]}
def _cn1_rows():
    out = {}
    for a in range(2, 7):
        for b in range(2, 7):
            for c in range(2, 5):
                out[f"p{a}{b}{c}"] = {"Q": f"티셔츠 {a}종류, 바지 {b}종류, 신발 {c}종류 중에서 각각 하나씩 골라 입는 경우의 수", "LAW": "곱의 법칙(동시에 일어남)", "CALC": f"{a} × {b} × {c} = {a * b * c}", "ans": a * b * c, "NOTE": "종류별로 독립 선택"}
    for a in range(2, 13):
        for b in range(a + 1, 13):
            ca, cb = 6 - abs(a - 7), 6 - abs(b - 7)
            out[f"s{a}_{b}"] = {"Q": f"서로 다른 두 개의 주사위를 동시에 던져 나온 눈의 수의 합이 {a} 또는 {b}{_ika(b)} 되는 경우의 수", "LAW": "합의 법칙(동시에 일어나지 않음)", "CALC": f"{ca} + {cb} = {ca + cb}", "ans": ca + cb,
                               "NOTE": f"합이 {a}인 경우 {ca}가지, 합이 {b}인 경우 {cb}가지"}
    return out


CN1_ROWS = _cn1_rows()


def cn_t1():
    return T(CN, 1, CN_B, title="합의 법칙과 곱의 법칙",
        skill="동시에 일어나는 선택은 곱하고, 동시에 일어날 수 없는 경우는 더하기", axis={"형태": "옷 고르기(곱) / 주사위 눈의 합(합)"}, disc="곱의 법칙과 합의 법칙을 상황에 맞게 고르는가", diff=1,
        params=[{"name": "f", "values": {"in": list(CN1_ROWS)}}], table={"key": "f", "rows": CN1_ROWS},
        derive={"v": "ans"}, cost=["ans"], verify=["v == ans"],
        q="{Q}를 구하시오.", answer="{ans}",
        sol1="{LAW}을 쓴다. 곱의 법칙: 두 사건이 잇달아(동시에) 일어나면 각각의 경우의 수를 곱한다. 합의 법칙: 두 사건이 동시에 일어나지 않으면 더한다. {NOTE}.",
        sol2=[("{LAW}", "법칙 고르기"), ("{NOTE}", "경우의 수 세기"), ("{CALC}", None, ("{ans}", "경우의 수"))],
        sol3=["주사위 두 개의 눈의 합이 n이 되는 경우는 n ≤ 7이면 n − 1가지, n > 7이면 13 − n가지이다(옷은 종류별 독립 선택). 따라서 답은 {ans}이다.", "{CALC}", "답 {ans}"],
        model="{LAW}에 의해 {CALC}이다.",
        rubric=[("법칙 선택", 2, "{LAW}을 바르게 골랐다.", "합·곱을 바꿨으면 인정하지 않는다."), ("계산", 3, "{CALC}{ro(ans)} 구했다.", "경우의 수 세기 실수면 1점.")],
        pitfalls=[("곱해야 할 것을 더함", "법칙 선택", "불인정"), ("주사위 합의 경우의 수 세기 실수", "계산", "부분"), ("순서 쌍을 중복으로 셈", "계산", "부분")])


def cn_t2():
    return T(CN, 2, CN_B, title="순열 — n명 중 r명을 뽑아 일렬로 세우는 경우의 수",
        skill="ₙPᵣ = n(n − 1)…(n − r + 1)로 계산하기", axis={"n": "4~12", "r": "2~6", "형태": "일렬로 세우기 / 서로 다른 상 / 자리 자연수 / 의자"}, disc="순서를 고려하므로 순열이며, r개의 연속 정수를 곱함을 아는가", diff=1,
        params=[{"name": "n", "values": {"int": [4, 12]}}, {"name": "r", "values": {"int": [2, 6]}}, {"name": "k", "values": {"in": ["line", "prize", "digits", "seats"]}}],
        table={"key": "k", "rows": {"line": {"PRE": "", "MID": "명의 학생 중에서 ", "POST": "명을 뽑아 일렬로 세우는 경우의 수", "d": 0}, "prize": {"PRE": "", "MID": "명의 학생 중에서 ", "POST": "명을 뽑아 각각 서로 다른 상을 한 개씩 주는 경우의 수", "d": 0},
                                    "digits": {"PRE": "1부터 ", "MID": "까지의 숫자가 각각 하나씩 적힌 카드 중에서 ", "POST": "장을 뽑아 일렬로 나열하여 만들 수 있는 자연수의 개수", "d": 1}, "seats": {"PRE": "서로 다른 ", "MID": "개의 의자에 ", "POST": "명의 학생이 한 명씩 앉는 경우의 수", "d": 0}}},
        derive={"ans": "factorial(n)/factorial(n - r)", "n1": "n - 1", "nr": "n - r + 1"},
        constraints=["r <= n - 2", "ans not in (n, r)", "d == 0 or n <= 9"], cost=["n", "r", "ans"], verify=["ans*factorial(n - r) == factorial(n)"],
        q="{PRE}{n}{MID}{r}{POST}를 구하시오.", answer="{ans}",
        sol1="뽑는 순서(자리)가 다르면 다른 경우이므로 순열이다. 첫 자리에 {n}명, 다음 자리에 {n1}명, … 차례로 줄어들어 {r}개의 수를 곱한다: [[perm({n}, {r})]] = {n} × {n1} × … × {nr}.",
        sol2=[("순서가 있으므로 순열 [[perm({n}, {r})]]", "자리마다 사람이 줄어듦"), ("[[perm({n}, {r})]] = {n} × {n1} × … × {nr} = {ans}", None, ("{ans}", "경우의 수"))],
        sol3=["[[perm({n}, {r})]] = {n}! ÷ ({n} − {r})! = {factorial(n)} ÷ {factorial(n - r)} = {ans}{ro(ans)} 같다. 따라서 답은 {ans}이다.", "n!/(n − r)! = {ans}", "답 {ans}"],
        model="순서를 고려하므로 [[perm({n}, {r})]] = {ans}이다.",
        rubric=[("순열 판단", 2, "순서를 고려해 [[perm({n}, {r})]]{ro(r)} 세웠다.", "조합으로 세웠으면 인정하지 않는다."), ("계산", 3, "{ans}{eul(ans)} 구했다.", "곱하는 수의 개수를 틀렸으면 1점.")],
        pitfalls=[("조합 ₙCᵣ로 계산", "순열 판단", "불인정"), ("곱하는 수를 r개보다 많거나 적게 함", "계산", "부분"), ("계산 실수", "계산", "부분")])


def _cn3_rows():
    out = {}
    for n in range(4, 12):
        f0, f1, f2, f3 = factorial(n), factorial(n - 1), factorial(n - 2), factorial(n - 3)
        out[f"adj{n}"] = {"n": n, "COND": "특정 2명이 서로 이웃하도록", "LAW": "이웃한 2명을 한 묶음으로 보아 (n − 1)!을 세고, 묶음 안의 순서 2!을 곱한다", "CALC": f"({n} − 1)! × 2 = {f1} × 2 = {2 * f1}", "ans": 2 * f1, "f0": f0, "f1": f1}
        out[f"ends{n}"] = {"n": n, "COND": "특정 2명이 양 끝에 서도록", "LAW": "양 끝의 2명을 먼저 배치(2!)하고 나머지 (n − 2)명을 가운데에 세운다", "CALC": f"2 × ({n} − 2)! = 2 × {f2} = {2 * f2}", "ans": 2 * f2, "f0": f0, "f1": f1}
        out[f"nadj{n}"] = {"n": n, "COND": "특정 2명이 서로 이웃하지 않도록", "LAW": "전체 n!에서 이웃하는 경우 (n − 1)! × 2를 뺀다", "CALC": f"{n}! − ({n} − 1)! × 2 = {f0} − {2 * f1} = {f0 - 2 * f1}", "ans": f0 - 2 * f1, "f0": f0, "f1": f1}
        out[f"first{n}"] = {"n": n, "COND": "특정 1명이 맨 앞에 서도록", "LAW": "맨 앞을 그 한 명으로 고정하고 나머지 (n − 1)명을 일렬로 세운다", "CALC": f"({n} − 1)! = {f1}", "ans": f1, "f0": f0, "f1": f1}
        out[f"last{n}"] = {"n": n, "COND": "특정 1명이 맨 뒤에 서도록", "LAW": "맨 뒤를 그 한 명으로 고정하고 나머지 (n − 1)명을 일렬로 세운다", "CALC": f"({n} − 1)! = {f1}", "ans": f1, "f0": f0, "f1": f1}
        out[f"nfirst{n}"] = {"n": n, "COND": "특정 1명이 맨 앞에 서지 않도록", "LAW": "전체 n!에서 그 한 명이 맨 앞에 서는 경우 (n − 1)!을 뺀다", "CALC": f"{n}! − ({n} − 1)! = {f0} − {f1} = {f0 - f1}", "ans": f0 - f1, "f0": f0, "f1": f1}
        out[f"nends{n}"] = {"n": n, "COND": "특정 2명이 양 끝에 서지 않도록", "LAW": "전체 n!에서 두 사람이 양 끝에 서는 경우 2 × (n − 2)!을 뺀다", "CALC": f"{n}! − 2 × ({n} − 2)! = {f0} − {2 * f2} = {f0 - 2 * f2}", "ans": f0 - 2 * f2, "f0": f0, "f1": f1}
        out[f"adj3_{n}"] = {"n": n, "COND": "특정 3명이 모두 서로 이웃하도록", "LAW": "이웃한 3명을 한 묶음으로 보아 (n − 2)!을 세고, 묶음 안의 순서 3!을 곱한다", "CALC": f"({n} − 2)! × 6 = {f2} × 6 = {6 * f2}", "ans": 6 * f2, "f0": f0, "f1": f1}
        if n >= 5:
            out[f"between{n}"] = {"n": n, "COND": "특정 2명 사이에 정확히 1명이 서도록", "LAW": "두 사람 사이에 설 1명을 고르고(n − 2가지) 세 사람을 한 묶음(양 끝 순서 2!)으로 보아 (n − 2)!을 곱한다", "CALC": f"({n} − 2) × 2 × ({n} − 2)! = {n - 2} × 2 × {f2} = {2 * (n - 2) * f2}", "ans": 2 * (n - 2) * f2, "f0": f0, "f1": f1}
    return out


CN3_ROWS = _cn3_rows()


def cn_t3():
    return T(CN, 3, CN_B, title="조건이 있는 순열 — 이웃·양 끝·이웃하지 않음",
        skill="이웃하는 것은 한 묶음으로, 양 끝은 먼저 배치, 이웃하지 않음은 전체에서 빼기", axis={"n": "4~11", "조건": "이웃 / 양 끝 / 이웃하지 않음 / 맨 앞·맨 뒤 고정 / 맨 앞 아님 / 양 끝 아님 / 3명 이웃 / 사이에 1명"}, disc="묶음 안의 순서 2!을 곱하는가, 여사건(전체 − 이웃)으로 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CN3_ROWS)}}], table={"key": "f", "rows": CN3_ROWS},
        derive={"v": "ans"}, constraints=["ans != n"], cost=["n", "f0", "f1", "ans"], verify=["f0 == n*f1"],
        q="{n}명의 학생을 일렬로 세울 때, {COND} 세우는 경우의 수를 구하시오.", answer="{ans}",
        sol1="{LAW}.", sol2=[("{LAW}", "조건 처리"), ("{CALC}", None, ("{ans}", "경우의 수"))],
        sol3=["전체 {n}! = {f0}가지 중 이웃하는 경우 {f1} × 2 = {2*f1}가지, 이웃하지 않는 경우 {f0 - 2*f1}가지로 합이 전체와 같다. 따라서 답은 {ans}이다.", "이웃 {2*f1} + 이웃 안 함 {f0 - 2*f1} = {f0}", "답 {ans}"],
        model="{LAW}. 따라서 {CALC}이다.",
        rubric=[("조건 처리", 3, "{LAW}는 방법을 썼다.", "묶음 안의 순서 2!을 빠뜨렸으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계승 계산 실수면 1점.")],
        pitfalls=[("묶음 안의 순서 2!을 빠뜨림", "조건 처리", "부분"), ("이웃하지 않는 경우를 직접 세다 누락", "조건 처리", "부분"), ("계승 계산 실수", "계산", "부분")])


def _cn4_rows():
    out = {}
    for n in range(5, 13):
        for r in range(2, 6):
            if r > n - 2:
                continue
            out[f"p{n}_{r}"] = {"Q": f"{n}명의 학생 중에서 대표 {r}명을 뽑는 경우의 수", "CALC": f"[[comb({n}, {r})]] = {comb(n, r)}", "LAW": "순서가 없으므로 조합", "ans": comb(n, r), "n": n, "r": r}
    for m in range(3, 9):
        for w in range(2, 8):
            out[f"mw{m}_{w}"] = {"Q": f"남학생 {m}명, 여학생 {w}명 중에서 남학생 2명과 여학생 1명을 뽑는 경우의 수", "CALC": f"[[comb({m}, 2)]] × [[comb({w}, 1)]] = {comb(m, 2)} × {w} = {comb(m, 2) * w}", "LAW": "남·여를 각각 조합으로 뽑고 곱의 법칙", "ans": comb(m, 2) * w, "n": m, "r": w}
            if m >= 3 and w >= 3:
                out[f"mw2{m}_{w}"] = {"Q": f"남학생 {m}명, 여학생 {w}명 중에서 남학생 2명과 여학생 2명을 뽑는 경우의 수", "CALC": f"[[comb({m}, 2)]] × [[comb({w}, 2)]] = {comb(m, 2)} × {comb(w, 2)} = {comb(m, 2) * comb(w, 2)}", "LAW": "남·여를 각각 조합으로 뽑고 곱의 법칙", "ans": comb(m, 2) * comb(w, 2), "n": m, "r": w}
                out[f"mw12{m}_{w}"] = {"Q": f"남학생 {m}명, 여학생 {w}명 중에서 남학생 1명과 여학생 2명을 뽑는 경우의 수", "CALC": f"[[comb({m}, 1)]] × [[comb({w}, 2)]] = {m} × {comb(w, 2)} = {m * comb(w, 2)}", "LAW": "남·여를 각각 조합으로 뽑고 곱의 법칙", "ans": m * comb(w, 2), "n": m, "r": w}
    return out


CN4_ROWS = _cn4_rows()


def cn_t4():
    return T(CN, 4, CN_B, title="조합 — 대표 뽑기, 남녀 조건 조합",
        skill="순서 없이 뽑는 것은 조합 ₙCᵣ이며, 조건이 나뉘면 각각의 조합을 곱하기", axis={"형태": "n명 중 r명 / 남 m·여 w 중 남 2 여 1"}, disc="순서 없음 → 조합, 두 집단에서 각각 뽑을 때는 곱의 법칙으로 곱하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CN4_ROWS)}}], table={"key": "f", "rows": CN4_ROWS},
        derive={"v": "ans"}, constraints=["ans not in (n, r)"], cost=["n", "r", "ans"], verify=["ans > 0"],
        q="{Q}를 구하시오.", answer="{ans}",
        sol1="{LAW}. 조합 ₙCᵣ = n! ÷ (r!(n − r)!)은 순서를 고려하지 않고 r개를 고르는 방법의 수이다.",
        sol2=[("{LAW}", "조합 판단"), ("{CALC}", None, ("{ans}", "경우의 수"))],
        sol3=["순열로 세면 순서가 다른 같은 묶음이 여러 번 세어지므로 r!로 나눠야 조합이 된다. 따라서 답은 {ans}이다.", "{CALC}", "답 {ans}"],
        model="{LAW}이므로 {CALC}이다.",
        rubric=[("조합 판단", 2, "{LAW}임을 밝혔다.", "순열로 세웠으면 인정하지 않는다."), ("계산", 3, "{CALC}{ro(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("순열로 세어 r!배 큰 값을 답함", "조합 판단", "불인정"), ("남·여 조합을 더함", "계산", "불인정"), ("조합 계산 실수", "계산", "부분")])


def _cn5_rows():
    out = {}
    for n in range(5, 16):
        out[f"diag{n}"] = {"Q": f"{n}각형의 대각선의 개수", "LAW": "꼭짓점 2개를 고르는 조합에서 변의 개수를 뺀다", "CALC": f"[[comb({n}, 2)]] − {n} = {comb(n, 2)} − {n} = {comb(n, 2) - n}", "ans": comb(n, 2) - n, "n": n}
        out[f"shake{n}"] = {"Q": f"{n}명이 서로 빠짐없이 한 번씩 악수할 때, 악수한 총 횟수", "LAW": "두 사람을 고르는 조합(순서 없음)", "CALC": f"[[comb({n}, 2)]] = {comb(n, 2)}", "ans": comb(n, 2), "n": n}
    for m in range(3, 8):
        for w in range(3, 8):
            if m > w:
                continue
            out[f"para{m}_{w}"] = {"Q": f"서로 평행한 {m}개의 직선과, 이들과 평행하지 않으면서 서로 평행한 {w}개의 직선이 만나서 생기는 평행사변형의 개수", "LAW": "두 방향에서 각각 직선 2개씩 고르는 조합의 곱", "CALC": f"[[comb({m}, 2)]] × [[comb({w}, 2)]] = {comb(m, 2)} × {comb(w, 2)} = {comb(m, 2) * comb(w, 2)}", "ans": comb(m, 2) * comb(w, 2), "n": m}
    for n in range(5, 13):
        out[f"tri{n}"] = {"Q": f"원 위의 서로 다른 {n}개의 점 중 3개를 꼭짓점으로 하는 삼각형의 개수", "LAW": "어느 세 점도 한 직선 위에 있지 않으므로 3개를 고르는 조합", "CALC": f"[[comb({n}, 3)]] = {comb(n, 3)}", "ans": comb(n, 3), "n": n}
        out[f"line{n}"] = {"Q": f"원 위의 서로 다른 {n}개의 점 중 2개를 이어 만들 수 있는 직선의 개수", "LAW": "어느 세 점도 한 직선 위에 있지 않으므로 2개를 고르는 조합", "CALC": f"[[comb({n}, 2)]] = {comb(n, 2)}", "ans": comb(n, 2), "n": n}
        if n >= 6:
            out[f"quad{n}"] = {"Q": f"원 위의 서로 다른 {n}개의 점 중 4개를 꼭짓점으로 하는 사각형의 개수", "LAW": "어느 세 점도 한 직선 위에 있지 않으므로 4개를 고르는 조합", "CALC": f"[[comb({n}, 4)]] = {comb(n, 4)}", "ans": comb(n, 4), "n": n}
        for r in (3, 4, 5):
            if r > n - 2:
                continue
            out[f"incl{n}_{r}"] = {"Q": f"{n}명 중에서 특정한 한 명을 반드시 포함하여 {r}명을 뽑는 경우의 수", "LAW": f"그 한 명은 이미 뽑혔으므로 나머지 {n - 1}명 중 {r - 1}명을 고른다", "CALC": f"[[comb({n - 1}, {r - 1})]] = {comb(n - 1, r - 1)}", "ans": comb(n - 1, r - 1), "n": n}
            out[f"excl{n}_{r}"] = {"Q": f"{n}명 중에서 특정한 한 명을 제외하고 {r}명을 뽑는 경우의 수", "LAW": f"그 한 명을 뺀 나머지 {n - 1}명 중 {r}명을 고른다", "CALC": f"[[comb({n - 1}, {r})]] = {comb(n - 1, r)}", "ans": comb(n - 1, r), "n": n}
    return out


CN5_ROWS = _cn5_rows()


def cn_t5():
    return T(CN, 5, CN_B, title="조합의 활용 — 대각선의 개수·삼각형의 개수·특정인 포함",
        skill="상황을 '몇 개 중 몇 개 고르기'로 바꾸고 조건(변 제외·특정인 포함)을 반영하기", axis={"형태": "대각선·악수 / 삼각형·사각형·직선 / 평행사변형 / 특정인 포함·제외", "n": "5~15"}, disc="대각선은 ₙC₂에서 변 n개를 빼고, 특정인 포함은 나머지에서 r − 1명을 고름을 아는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CN5_ROWS)}}], table={"key": "f", "rows": CN5_ROWS},
        derive={"v": "ans"}, constraints=["ans != n"], cost=["n", "ans"], verify=["ans > 0"],
        q="{Q}를 구하시오.", answer="{ans}",
        sol1="{LAW}. 조합으로 고른 뒤 조건에 맞지 않는 것을 빼거나, 고정된 것을 제외한 나머지에서 고른다.",
        sol2=[("{LAW}", "상황 → 조합"), ("{CALC}", None, ("{ans}", "개수"))],
        sol3=["작은 경우로 확인: 사각형의 대각선은 ₄C₂ − 4 = 2, 4명 중 특정인 포함 2명은 ₃C₁ = 3. 같은 방식으로 답은 {ans}이다.", "{CALC}", "답 {ans}"],
        model="{LAW}이므로 {CALC}이다.",
        rubric=[("조합 세우기", 3, "{LAW}는 식을 세웠다.", "변을 빼지 않거나 특정인을 포함하지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("대각선에서 변의 개수를 빼지 않음", "조합 세우기", "부분"), ("특정인 포함을 ₙCᵣ 그대로 계산", "조합 세우기", "불인정"), ("조합 계산 실수", "계산", "부분")])


CN_SEED = SEED(CN, category="확률통계", title="경우의 수 — 합·곱의 법칙·순열·조건 순열·조합·조합의 활용", unit_id="h1-1", concept_ids=["h1-1-14", "h1-1-15", "h1-1-16"],
               schema_name="경우의 수·순열·조합", note="계승은 factorial 파생. 조건 순열·조합 활용은 행 표의 문장·계산 문자열로 변형.",
               templates=[cn_t1(), cn_t2(), cn_t3(), cn_t4(), cn_t5()])


# ═══════════════════════════════════════════════════════════════════ 4. 행렬
MX = "h1-1-matrix"
MX_B = {**HS, "prereq": ["행렬의 뜻", "연립일차방정식"], "ops": ["행렬"], "traps": ["곱셈 순서", "성분 위치"], "tags": ["행렬의 연산"]}


def mx_t1():
    return T(MX, 1, MX_B, title="두 행렬이 서로 같을 조건 — 성분 비교",
        skill="같은 위치의 성분끼리 같다고 놓아 연립방정식 풀기", axis={"x, y": "±1~±6"}, disc="같은 위치의 성분끼리 비교해 연립하는가", diff=2,
        params=[{"name": "x", "values": {"in": NZ(-6, 6)}}, {"name": "y", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": ["xy", "sum"]}}],
        table={"key": "k", "rows": {"xy": {"ASK": "xy", "w": 1}, "sum": {"ASK": "x + y", "w": 0}}},
        derive={"s": "x + y", "d": "x - y", "ans": "w*x*y + (1 - w)*(x + y)"},
        constraints=["x != y", "ans != 0", "ans not in (x, y, c, s, d)"], cost=["x", "y", "s", "d", "ans"], verify=["s == x + y", "d == x - y"],
        q="두 행렬 A = [[mat(2, 2, x + y, {c}, 3, x − y)]], B = [[mat(2, 2, {s}, {c}, 3, {d})]]에 대하여 A = B일 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="두 행렬이 같으려면 같은 위치의 성분이 모두 같아야 한다. (1, 1) 성분에서 x + y = {s}, (2, 2) 성분에서 x − y = {d}이고, 나머지 성분은 이미 같다. 두 식을 연립해 x, y를 구한다.",
        sol2=[("x + y = {s}, x − y = {d}", "같은 위치의 성분"), ("더하면 2x = {2*x} → x = {x}, y = {y}", "연립"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["x = {x}, y = {y}{eul(y)} A에 넣으면 (1, 1) 성분 {s}, (2, 2) 성분 {d}{ro(d)} B와 모든 성분이 같다. 따라서 {ASK} = {ans}이다.", "A의 성분 = B의 성분 ✓", "{ASK} = {ans}"],
        model="A = B이므로 x + y = {s}, x − y = {d}이고 연립하면 x = {x}, y = {y}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("성분 비교", 3, "x + y = {s}, x − y = {d}{eul(d)} 세웠다.", "다른 위치의 성분을 비교했으면 인정하지 않는다."), ("연립·답", 2, "x = {x}, y = {y}에서 {ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("다른 위치의 성분을 비교", "성분 비교", "불인정"), ("연립 계산 실수", "연립·답", "부분"), ("xy와 x + y를 바꿔 답함", "연립·답", "부분")])


def mx_t2():
    return T(MX, 2, MX_B, title="행렬의 덧셈·뺄셈·실수배 — kA + lB의 성분",
        skill="같은 위치의 성분끼리 실수배하고 더하기", axis={"k, l": "±1~±3", "성분": "−5~5"}, disc="실수배를 모든 성분에 곱하고 같은 위치끼리 더하는가", diff=2,
        params=[{"name": "k", "values": {"in": NZ(-3, 3)}}, {"name": "l", "values": {"in": NZ(-3, 3)}}, {"name": "a1", "values": {"int": [-5, 5]}}, {"name": "a2", "values": {"int": [-5, 5]}}, {"name": "a3", "values": {"int": [-5, 5]}}, {"name": "a4", "values": {"int": [-5, 5]}},
                {"name": "b1", "values": {"int": [-5, 5]}}, {"name": "b2", "values": {"int": [-5, 5]}}, {"name": "b3", "values": {"int": [-5, 5]}}, {"name": "b4", "values": {"int": [-5, 5]}}, {"name": "ask", "values": {"in": ["all", "12"]}}],
        table={"key": "ask", "rows": {"all": {"ASK": "모든 성분의 합", "w": 1}, "12": {"ASK": "(1, 2) 성분", "w": 0}}},
        derive={"c1": "k*a1 + l*b1", "c2": "k*a2 + l*b2", "c3": "k*a3 + l*b3", "c4": "k*a4 + l*b4", "ans": "w*(k*(a1 + a2 + a3 + a4) + l*(b1 + b2 + b3 + b4)) + (1 - w)*(k*a2 + l*b2)"},
        constraints=["ans != 0", "ans not in (k, l, a1, a2, a3, a4, b1, b2, b3, b4)"], cost=["k", "l", "c1", "c2", "c3", "c4", "ans"], verify=["c2 == k*a2 + l*b2"],
        q="두 행렬 A = [[mat(2, 2, {a1}, {a2}, {a3}, {a4})]], B = [[mat(2, 2, {b1}, {b2}, {b3}, {b4})]]에 대하여 행렬 {co(k)}A {sgt(l)}B의 {ASK}을 구하시오.", answer="{ans}",
        sol1="실수배는 모든 성분에 그 수를 곱하고, 덧셈·뺄셈은 같은 위치의 성분끼리 한다. 각 성분은 {k} × (A의 성분) {sgn(l)} × (B의 성분)이다.",
        sol2=[("{co(k)}A = [[mat(2, 2, {k*a1}, {k*a2}, {k*a3}, {k*a4})]], {co(l)}B = [[mat(2, 2, {l*b1}, {l*b2}, {l*b3}, {l*b4})]]", "실수배"), ("{co(k)}A {sgt(l)}B = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]", "같은 위치끼리 더함"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["(1, 2) 성분은 첫째 행·둘째 열의 성분으로 {k} × {pn(a2)} {sgn(l)} × {pn(b2)} = {c2}이다. 네 성분의 합은 {c1} {sgn(c2)} {sgn(c3)} {sgn(c4)} = {c1 + c2 + c3 + c4}이다. 따라서 {ASK} = {ans}이다.", "[[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]", "{ASK} = {ans}"],
        model="{co(k)}A {sgt(l)}B = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]이므로 {ASK}은 {ans}이다.",
        rubric=[("연산", 3, "{co(k)}A {sgt(l)}B = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]{eul(c4)} 구했다.", "한 성분만 틀렸으면 2점."), ("답", 2, "{ASK} {ans}{eul(ans)} 답했다.", "(1, 2)와 (2, 1) 성분을 혼동했으면 인정하지 않는다.")],
        pitfalls=[("실수배를 한 성분에만 적용", "연산", "불인정"), ("(1, 2)와 (2, 1) 성분 혼동", "답", "불인정"), ("부호 실수", "연산", "부분")])


def mx_t3():
    return T(MX, 3, MX_B, title="행렬의 곱셈 — AB의 성분",
        skill="(i, j) 성분은 A의 i행과 B의 j열의 성분을 차례로 곱해 더한 것임을 쓰기", axis={"성분": "−4~4", "구하는 것": "(1, 1) / (2, 1) 성분 / 모든 성분의 합"}, disc="행과 열을 바르게 짝지어 곱하고 AB ≠ BA임을 아는가", diff=3,
        params=[{"name": "a1", "values": {"int": [-4, 4]}}, {"name": "a2", "values": {"int": [-4, 4]}}, {"name": "a3", "values": {"int": [-4, 4]}}, {"name": "a4", "values": {"int": [-4, 4]}},
                {"name": "b1", "values": {"int": [-4, 4]}}, {"name": "b2", "values": {"int": [-4, 4]}}, {"name": "b3", "values": {"int": [-4, 4]}}, {"name": "b4", "values": {"int": [-4, 4]}}, {"name": "ask", "values": {"in": ["11", "21", "all"]}}],
        table={"key": "ask", "rows": {"11": {"ASK": "(1, 1) 성분", "w1": 1, "w2": 0, "w3": 0}, "21": {"ASK": "(2, 1) 성분", "w1": 0, "w2": 1, "w3": 0}, "all": {"ASK": "모든 성분의 합", "w1": 0, "w2": 0, "w3": 1}}},
        derive={"c1": "a1*b1 + a2*b3", "c2": "a1*b2 + a2*b4", "c3": "a3*b1 + a4*b3", "c4": "a3*b2 + a4*b4", "ans": "w1*(a1*b1 + a2*b3) + w2*(a3*b1 + a4*b3) + w3*(a1*b1 + a2*b3 + a1*b2 + a2*b4 + a3*b1 + a4*b3 + a3*b2 + a4*b4)"},
        constraints=["ans != 0", "ans not in (a1, a2, a3, a4, b1, b2, b3, b4)", "a1*a2*a3*a4*b1*b2*b3*b4 != 0"], cost=["c1", "c2", "c3", "c4", "ans"], verify=["c1 == a1*b1 + a2*b3"],
        q="두 행렬 A = [[mat(2, 2, {a1}, {a2}, {a3}, {a4})]], B = [[mat(2, 2, {b1}, {b2}, {b3}, {b4})]]에 대하여 행렬 AB의 {ASK}을 구하시오.", answer="{ans}",
        sol1="AB의 (i, j) 성분은 A의 i행 성분과 B의 j열 성분을 차례로 곱해 더한 값이다. 예를 들어 (1, 1) 성분은 {a1} × {pn(b1)} + {pn(a2)} × {pn(b3)} = {c1}, (2, 1) 성분은 {a3} × {pn(b1)} + {pn(a4)} × {pn(b3)} = {c3}이다.",
        sol2=[("(1, 1): {a1} × {pn(b1)} + {pn(a2)} × {pn(b3)} = {c1}, (1, 2): {a1} × {pn(b2)} + {pn(a2)} × {pn(b4)} = {c2}", "1행 × 각 열"), ("(2, 1): {a3} × {pn(b1)} + {pn(a4)} × {pn(b3)} = {c3}, (2, 2): {a3} × {pn(b2)} + {pn(a4)} × {pn(b4)} = {c4}", "2행 × 각 열"),
              ("AB = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]] → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["행렬의 곱은 순서를 바꾸면(BA) 일반적으로 다른 값이 나오므로 A의 행·B의 열 순서를 지켜야 한다. 따라서 {ASK} = {ans}이다.", "AB = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]", "{ASK} = {ans}"],
        model="AB = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]이므로 {ASK}은 {ans}이다.",
        rubric=[("곱셈", 3, "AB = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]{eul(c4)} 구했다.", "행과 열을 바꿔 곱했으면 인정하지 않는다."), ("답", 2, "{ASK} {ans}{eul(ans)} 답했다.", "성분 위치를 혼동했으면 인정하지 않는다.")],
        pitfalls=[("같은 위치 성분끼리 곱함", "곱셈", "불인정"), ("BA를 계산함", "곱셈", "불인정"), ("성분 위치 혼동", "답", "부분")])


def mx_t4():
    return T(MX, 4, MX_B, title="행렬의 거듭제곱 — A²의 성분과 A² = kA + lE",
        skill="A² = AA를 직접 계산해 성분을 구하기", axis={"성분": "−3~3"}, disc="A²을 성분의 제곱이 아닌 행렬의 곱으로 계산하는가", diff=3,
        params=[{"name": "a1", "values": {"int": [-3, 3]}}, {"name": "a2", "values": {"int": [-3, 3]}}, {"name": "a3", "values": {"int": [-3, 3]}}, {"name": "a4", "values": {"int": [-3, 3]}}, {"name": "ask", "values": {"in": ["11", "all"]}}],
        table={"key": "ask", "rows": {"11": {"ASK": "(1, 1) 성분", "w": 1}, "all": {"ASK": "모든 성분의 합", "w": 0}}},
        derive={"c1": "a1*a1 + a2*a3", "c2": "a1*a2 + a2*a4", "c3": "a3*a1 + a4*a3", "c4": "a3*a2 + a4*a4", "ans": "w*(a1*a1 + a2*a3) + (1 - w)*(a1*a1 + a2*a3 + a1*a2 + a2*a4 + a3*a1 + a4*a3 + a3*a2 + a4*a4)"},
        constraints=["ans != 0", "ans not in (a1, a2, a3, a4)", "a2*a3 != 0", "ans != a1*a1"], cost=["c1", "c2", "c3", "c4", "ans"], verify=["c1 == a1*a1 + a2*a3"],
        q="행렬 A = [[mat(2, 2, {a1}, {a2}, {a3}, {a4})]]에 대하여 행렬 A²의 {ASK}을 구하시오.", answer="{ans}",
        sol1="A² = A × A이다. 성분을 각각 제곱하는 것이 아니라 행렬의 곱셈 규칙(행 × 열)을 따른다: (1, 1) 성분은 {a1} × {pn(a1)} + {pn(a2)} × {pn(a3)} = {c1}.",
        sol2=[("A² = AA: (1, 1) {c1}, (1, 2) {c2}", "1행 × 각 열"), ("(2, 1) {c3}, (2, 2) {c4}", "2행 × 각 열"), ("A² = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]] → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["성분을 제곱한 [[mat(2, 2, {a1*a1}, {a2*a2}, {a3*a3}, {a4*a4})]]{eun(a4*a4)} A²이 아니다((1, 1) 성분에는 (1, 2) 성분과 (2, 1) 성분의 곱 {a2*a3}{ika(a2*a3)} 더해진다). 따라서 {ASK} = {ans}이다.", "A² = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]", "{ASK} = {ans}"],
        model="A² = AA = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]이므로 {ASK}은 {ans}이다.",
        rubric=[("곱셈", 3, "A² = [[mat(2, 2, {c1}, {c2}, {c3}, {c4})]]{eul(c4)} 구했다.", "성분을 각각 제곱했으면 인정하지 않는다."), ("답", 2, "{ASK} {ans}{eul(ans)} 답했다.", "계산 실수면 1점.")],
        pitfalls=[("성분을 각각 제곱함", "곱셈", "불인정"), ("행·열 짝짓기 실수", "곱셈", "부분"), ("합 계산 실수", "답", "부분")])


MX_SEED = SEED(MX, category="연산", title="행렬 — 상등·덧셈과 실수배·곱셈·거듭제곱", unit_id="h1-1", concept_ids=["h1-1-17", "h1-1-18"],
               schema_name="행렬의 뜻과 연산", note="행렬 마커 [[mat(2, 2, a, b, c, d)]]. 성분은 파라미터, 결과는 파생.",
               templates=[mx_t1(), mx_t2(), mx_t3(), mx_t4()])


if __name__ == "__main__":
    run(PE_SEED, IQ_SEED, CN_SEED, MX_SEED)
