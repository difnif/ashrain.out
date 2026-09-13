# itemfactory/tools/mkseed_h1_algebra.py — 고1 공통수학1 대수 시드 생성기 ① (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h1_algebra.py
#     → seeds/h1-1-poly.json     (다항식: 전개 계수·나머지정리·항등식·두 나머지→계수·인수정리·삼차식 인수분해, 6틀)
#     → seeds/h1-1-complex.json  (복소수: 곱셈·나눗셈·i의 거듭제곱·실수 조건·켤레복소수, 5틀)
#     → seeds/h1-1-quad.json     (이차방정식: 판별식 범위·근과 계수 대칭식·두 근으로 방정식·무리근/허근 계수·근의 차, 5틀)
#     → seeds/h1-1-quadfn.json   (이차함수와 직선·최대최소: 교점 개수 범위·접선 상수·제한범위 최대최소·꼭짓점 이동 최소, 4틀)
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402

# ═══════════════════════════════════════════════════════════════════ 1. 다항식
PO = "h1-1-poly"
PO_B = {**HS, "prereq": ["다항식의 곱셈", "인수분해"], "ops": ["다항식"], "traps": ["부호", "동류항"], "tags": ["다항식", "나머지정리"]}


def po_t1():
    return T(PO, 1, PO_B, title="(x + a)(x² + bx + c)의 전개 — x² 또는 x의 계수",
        skill="분배법칙으로 전개해 같은 차수의 항끼리 모으기", axis={"a, b, c": "±1~±6", "구하는 계수": "x² / x"}, disc="차수별로 곱이 두 개씩 생김(x²: a + b, x: ab + c)을 빠짐없이 모으는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-6, 6)}}, {"name": "k", "values": {"in": ["x2", "x1"]}}],
        table={"key": "k", "rows": {"x2": {"ASK": "x²", "w": 1}, "x1": {"ASK": "x", "w": 0}}},
        derive={"c2": "a + b", "c1": "a*b + c", "c0": "a*c", "ans": "w*(a + b) + (1 - w)*(a*b + c)"},
        constraints=["c2 != 0", "c1 != 0", "ans not in (a, b, c)", "ans != 0"], cost=["a", "b", "c", "c2", "c1", "ans"],
        verify=["c2 == a + b", "c1 == a*b + c", "c0 == a*c"],
        q="(x {sgn(a)})(x² {sgt(b)}x {sgn(c)})을 전개했을 때, {ASK}의 계수를 구하시오.", answer="{ans}",
        sol1="앞 괄호의 x와 {a}{eul(a)} 각각 뒤 괄호의 세 항에 곱한 뒤 차수별로 모은다. x² 항은 x × (x의 항)과 {pn(a)} × x²의 둘, x 항은 x × (상수항)과 {pn(a)} × (x의 항)의 둘에서 나온다.",
        sol2=[("x × (x² {sgt(b)}x {sgn(c)}) = x³ {sgt(b)}x² {sgt(c)}x", "x를 곱한 항"), ("{pn(a)} × (x² {sgt(b)}x {sgn(c)}) = {co(a)}x² {sgt(a*b)}x {sgn(a*c)}", "{a}를 곱한 항"),
              ("합: x³ {sgt(c2)}x² {sgt(c1)}x {sgn(c0)} → {ASK}의 계수 {ans}", None, ("{ans}", "{ASK}의 계수"))],
        sol3=["x = 1을 넣어 확인하면 좌변 (1 {sgn(a)})(1 {sgn(b)} {sgn(c)}) = {(1 + a)*(1 + b + c)}, 전개식 1 {sgn(c2)} {sgn(c1)} {sgn(c0)} = {1 + c2 + c1 + c0}{ro(1 + c2 + c1 + c0)} 같다. 따라서 {ASK}의 계수는 {ans}이다.", "x = 1 대입: 양변 모두 {(1 + a)*(1 + b + c)}", "{ASK}의 계수 = {ans}"],
        model="(x {sgn(a)})(x² {sgt(b)}x {sgn(c)}) = x³ {sgt(c2)}x² {sgt(c1)}x {sgn(c0)}이므로 {ASK}의 계수는 {ans}이다.",
        rubric=[("전개", 3, "x³ {sgt(c2)}x² {sgt(c1)}x {sgn(c0)}{ro(c0)} 전개했다.", "한 항의 곱을 빠뜨렸으면 1점."), ("계수 읽기", 2, "{ASK}의 계수 {ans}{eul(ans)} 답했다.", "다른 차수의 계수를 답했으면 인정하지 않는다.")],
        pitfalls=[("차수별로 두 곱 중 하나를 빠뜨림", "전개", "부분"), ("부호 실수", "전개", "부분"), ("x²과 x의 계수를 바꿔 답함", "계수 읽기", "불인정")])


def po_t2():
    return T(PO, 2, PO_B, title="나머지정리 — 삼차식을 x − p로 나눈 나머지",
        skill="f(x)를 x − p로 나눈 나머지는 f(p)임을 써서 직접 대입하기", axis={"계수": "±1~±5", "p": "±1~±3"}, disc="나눗셈을 하지 않고 f(p)를 계산하며, (−p)³의 부호를 바르게 하는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "p", "values": {"in": [-3, -2, 2, 3]}}],
        derive={"np": "-p", "p3": "p**3", "p2": "p*p", "ans": "p**3 + a*p*p + b*p + c"},
        constraints=["ans != 0", "ans not in (a, b, c, p)"], cost=["a", "b", "c", "p", "ans"], verify=["ans == p3 + a*p2 + b*p + c"],
        q="다항식 x³ {sgt(a)}x² {sgt(b)}x {sgn(c)}{eul(c)} x {sgn(np)}{ro(np)} 나누었을 때의 나머지를 구하시오.", answer="{ans}",
        sol1="나머지정리: 다항식 f(x)를 일차식 x − p로 나눈 나머지는 f(p)이다. x {sgn(np)} = 0이 되는 x = {p}{eul(p)} f(x)에 대입하면 나눗셈 없이 나머지가 나온다.",
        sol2=[("f(x) = x³ {sgt(a)}x² {sgt(b)}x {sgn(c)}, 나머지 = f({p})", "나머지정리"), ("f({p}) = {pn(p)}³ {sgn(a)} × {pn(p)}² {sgn(b)} × {pn(p)} {sgn(c)}", "x = {p} 대입"),
              ("= {p3} {sgn(a*p2)} {sgn(b*p)} {sgn(c)} = {ans}", None, ("{ans}", "나머지"))],
        sol3=["f(x) = (x {sgn(np)})Q(x) + R에 x = {p}{eul(p)} 넣으면 첫 항이 0이 되어 f({p}) = R이다. 계산을 다시 확인하면 R = {ans}이다.", "f({p}) = R", "R = {ans}"],
        model="나머지정리에 의해 나머지는 f({p}) = {pn(p)}³ {sgn(a)} × {pn(p)}² {sgn(b)} × {pn(p)} {sgn(c)} = {ans}이다.",
        rubric=[("나머지정리", 2, "나머지가 f({p})임을 밝혔다.", "직접 나눗셈으로 구했어도 인정한다."), ("계산", 3, "f({p}) = {ans}{eul(ans)} 구했다.", "거듭제곱 부호 실수면 1점.")],
        pitfalls=[("x = −p를 대입함(부호 반대)", "나머지정리", "불인정"), ("(−p)³·(−p)²의 부호 실수", "계산", "부분"), ("계수 곱셈 실수", "계산", "부분")])


def po_t3():
    return T(PO, 3, PO_B, title="항등식의 계수 — a(x − 1)² + b(x − 1) + c = 이차식",
        skill="수치대입법(x = 1) 또는 계수비교법으로 항등식의 미정계수 구하기", axis={"이차식": "계수 ±1~±6"}, disc="항등식은 모든 x에서 성립하므로 x = 1 등 편한 값을 넣거나 전개해 계수를 비교하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "q", "values": {"in": NZ(-6, 6)}}, {"name": "r", "values": {"in": NZ(-6, 6)}}],
        derive={"a": "p", "b": "2*p + q", "c": "p + q + r", "ans": "p + (2*p + q) + (p + q + r)"},
        constraints=["b != 0", "c != 0", "ans != 0", "ans not in (p, q, r)"], cost=["p", "q", "r", "a", "b", "c", "ans"], verify=["a == p", "b == 2*p + q", "c == p + q + r", "ans == a + b + c"],
        q="등식 a(x − 1)² + b(x − 1) + c = {co(p)}x² {sgt(q)}x {sgn(r)}{ika(r)} x에 대한 항등식일 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.", answer="{ans}",
        sol1="항등식은 x에 어떤 값을 넣어도 성립한다. x = 1을 넣으면 c가 바로 나오고, 좌변을 전개해 x²의 계수를 비교하면 a = {p}, x의 계수를 비교하면 b를 얻는다. 또는 a + b + c는 x = 2를 넣은 값이기도 하다.",
        sol2=[("x = 1 대입: c = {p} {sgn(q)} {sgn(r)} = {c}", "수치대입법"), ("좌변 전개: ax² + (b − 2a)x + (a − b + c) → x²의 계수 a = {p}, x의 계수 b − 2a = {q}이므로 b = {b}", "계수비교법"),
              ("a + b + c = {a} {sgn(b)} {sgn(c)} = {ans}", None, ("{ans}", "a + b + c"))],
        sol3=["x = 2를 넣으면 좌변은 a + b + c, 우변은 {4*p} {sgn(2*q)} {sgn(r)} = {4*p + 2*q + r}{ro(4*p + 2*q + r)} 같은 값이다. 따라서 a + b + c = {ans}이다.", "x = 2 대입: a + b + c = {4*p + 2*q + r}", "a + b + c = {ans}"],
        model="x = 1을 대입하면 c = {c}이고, 좌변을 전개하면 ax² + (b − 2a)x + (a − b + c)이므로 a = {p}, b − 2a = {q}에서 b = {b}이다. 따라서 a + b + c = {ans}이다.",
        rubric=[("계수 구하기", 3, "a = {a}, b = {b}, c = {c}{eul(c)} 구했다.", "하나만 틀렸으면 1점."), ("합", 2, "a + b + c = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("x = 1 대입에서 부호 실수", "계수 구하기", "부분"), ("전개 없이 b = q로 둠", "계수 구하기", "불인정"), ("합 계산 실수", "합", "부분")])


def po_t4():
    return T(PO, 4, PO_B, title="두 나머지로 계수 구하기 — f(1), f(−1)",
        skill="나머지정리로 두 조건식을 세우고 연립해 두 계수 구하기", axis={"a, b": "±1~±6", "나머지": "−9~9"}, disc="f(1) = a + b + 1, f(−1) = −1 + a − b 두 식을 연립하는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "ask", "values": {"in": ["sum", "prod"]}}],
        table={"key": "ask", "rows": {"sum": {"ASK": "a + b", "w": 1}, "prod": {"ASK": "ab", "w": 0}}},
        derive={"r1": "1 + a + b", "r2": "-1 + a - b", "ans": "w*(a + b) + (1 - w)*a*b"},
        constraints=["r1 != 0", "r2 != 0", "ans != 0", "ans not in (a, b, r1, r2)"], cost=["a", "b", "r1", "r2", "ans"], verify=["r1 == 1 + a + b", "r2 == -1 + a - b"],
        q="다항식 f(x) = x³ + ax + b를 x − 1로 나눈 나머지가 {r1}, x + 1로 나눈 나머지가 {r2}일 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="나머지정리에서 f(1) = {r1}, f(−1) = {r2}이다. f(1) = 1 + a + b, f(−1) = −1 + a − b이므로 a, b에 대한 연립일차방정식이 된다. 두 식을 더하면 2a, 빼면 2b가 나온다.",
        sol2=[("f(1) = 1 + a + b = {r1} → a + b = {r1 - 1}", "x − 1로 나눈 나머지"), ("f(−1) = −1 + a − b = {r2} → a − b = {r2 + 1}", "x + 1로 나눈 나머지"),
              ("두 식을 연립하면 a = {a}, b = {b} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["a = {a}, b = {b}이면 f(1) = 1 {sgn(a)} {sgn(b)} = {r1}, f(−1) = −1 {sgn(a)} {sgn(-b)} = {r2}{ro(r2)} 두 조건과 맞는다. 따라서 {ASK} = {ans}이다.", "f(1) = {r1} ✓, f(−1) = {r2} ✓", "{ASK} = {ans}"],
        model="나머지정리에서 f(1) = 1 + a + b = {r1}, f(−1) = −1 + a − b = {r2}이므로 연립하면 a = {a}, b = {b}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("조건식", 3, "f(1) = {r1}, f(−1) = {r2}에서 a + b = {r1 - 1}, a − b = {r2 + 1}{eul(r2 + 1)} 세웠다.", "한 식만 세웠으면 1점."), ("연립·답", 2, "a = {a}, b = {b}{ro(b)} 풀어 {ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("f(−1)에서 (−1)³ = −1의 부호 실수", "조건식", "부분"), ("x + 1로 나눈 나머지를 f(1)로 둠", "조건식", "불인정"), ("연립 계산 실수", "연립·답", "부분")])


def po_t5():
    return T(PO, 5, PO_B, title="인수정리 — (x − p)(x − q)로 나누어떨어지는 삼차식의 계수",
        skill="f(p) = 0, f(q) = 0 두 조건으로 연립방정식을 세워 계수 구하기", axis={"두 근": "±1~±4", "상수항": "따라 정함"}, disc="나누어떨어짐 ⇔ 인수정리(f(p) = 0)를 쓰고 두 조건을 연립하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "q", "values": {"in": NZ(-4, 4)}}, {"name": "r", "values": {"in": NZ(-4, 4)}}],
        derive={"a": "-(p + q + r)", "b": "p*q + q*r + r*p", "c": "-p*q*r", "np": "-p", "nq": "-q", "ans": "-(p + q + r) + p*q + q*r + r*p"},
        constraints=["p < q", "r not in (p, q)", "a != 0", "b != 0", "ans != 0", "ans not in (p, q, c)"], cost=["p", "q", "r", "a", "b", "c", "ans"], verify=["p**3 + a*p*p + b*p + c == 0", "q**3 + a*q*q + b*q + c == 0", "ans == a + b"],
        q="다항식 x³ + ax² + bx {sgn(c)}{ika(c)} (x {sgn(np)})(x {sgn(nq)})로 나누어떨어질 때, 상수 a, b에 대하여 a + b의 값을 구하시오.", answer="{ans}",
        sol1="(x {sgn(np)})(x {sgn(nq)})로 나누어떨어지면 x {sgn(np)}, x {sgn(nq)} 각각으로도 나누어떨어지므로 인수정리에서 f({p}) = 0, f({q}) = 0이다. 두 식을 연립해 a, b를 구한다.",
        sol2=[("f({p}) = 0: {p**3} {sgt(p*p)}a {sgt(p)}b {sgn(c)} = 0", "인수정리"), ("f({q}) = 0: {q**3} {sgt(q*q)}a {sgt(q)}b {sgn(c)} = 0", "인수정리"),
              ("연립하면 a = {a}, b = {b} → a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=["f(x) = (x {sgn(np)})(x {sgn(nq)})(x {sgn(-r)})로 인수분해되어 전개하면 x³ {sgt(a)}x² {sgt(b)}x {sgn(c)}{ika(c)} 된다. 따라서 a + b = {ans}이다.", "f(x) = (x {sgn(np)})(x {sgn(nq)})(x {sgn(-r)})", "a + b = {ans}"],
        model="인수정리에서 f({p}) = 0, f({q}) = 0이므로 {p**3} {sgt(p*p)}a {sgt(p)}b {sgn(c)} = 0, {q**3} {sgt(q*q)}a {sgt(q)}b {sgn(c)} = 0이다. 연립하면 a = {a}, b = {b}이고 a + b = {ans}이다.",
        rubric=[("인수정리", 3, "f({p}) = 0, f({q}) = 0의 두 식을 세웠다.", "한 식만 세웠으면 1점."), ("연립·답", 2, "a = {a}, b = {b}{ro(b)} 풀어 a + b = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("f(−p) = 0으로 부호를 반대로 둠", "인수정리", "불인정"), ("한 조건만 씀", "인수정리", "부분"), ("연립 계산 실수", "연립·답", "부분")])


def po_t6():
    return T(PO, 6, PO_B, title="인수정리를 이용한 삼차식의 인수분해 — (x − p)(x − q)(x − r)의 근의 합·곱",
        skill="f(p) = 0인 p를 찾아 조립제법으로 나눈 뒤 남은 이차식을 인수분해하기", axis={"세 근": "−4~4 (서로 다름)"}, disc="상수항의 약수에서 f(p) = 0인 p를 찾고 조립제법으로 몫을 구하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-5, 5)}}, {"name": "q", "values": {"in": NZ(-5, 5)}}, {"name": "r", "values": {"in": NZ(-5, 5)}}, {"name": "ask", "values": {"in": ["max", "sq"]}}],
        table={"key": "ask", "rows": {"max": {"ASK": "가장 큰 근", "w": 1}, "sq": {"ASK": "세 근의 제곱의 합", "w": 0}}},
        derive={"a": "-(p + q + r)", "b": "p*q + q*r + r*p", "c": "-p*q*r", "ans": "w*r + (1 - w)*(p*p + q*q + r*r)", "np": "-p", "nq": "-q", "nr": "-r", "qb": "-(q + r)", "qc": "q*r"},
        constraints=["p < q", "q < r", "a != 0", "b != 0", "ans not in (a, b, c)", "ans != 0"], cost=["p", "q", "r", "a", "b", "c", "ans"], verify=["a == -(p + q + r)", "b == p*q + q*r + r*p", "c == -p*q*r"],
        q="삼차방정식 x³ {sgt(a)}x² {sgt(b)}x {sgn(c)} = 0의 {ASK}을 구하시오.", answer="{ans}",
        sol1="f(x) = x³ {sgt(a)}x² {sgt(b)}x {sgn(c)}에서 상수항 {c}의 약수 중 f(k) = 0이 되는 k를 찾는다: f({p}) = 0이므로 x {sgn(np)}{ika(np)} 인수이다. 조립제법으로 나누면 몫이 x² {sgt(qb)}x {sgn(qc)}이고 이를 인수분해해 나머지 두 근을 얻는다.",
        sol2=[("f({p}) = 0 → x {sgn(np)}{ika(np)} 인수", "인수정리 (상수항의 약수 시도)"), ("조립제법: f(x) = (x {sgn(np)})(x² {sgt(qb)}x {sgn(qc)}) = (x {sgn(np)})(x {sgn(nq)})(x {sgn(nr)})", "몫의 인수분해"),
              ("세 근 {p}, {q}, {r} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["세 근의 합 {p} {sgn(q)} {sgn(r)} = {p + q + r}{eun(p + q + r)} x²의 계수의 부호를 바꾼 {-a}{wa(-a)} 같고, 세 근의 곱 {p*q*r}{eun(p*q*r)} 상수항의 부호를 바꾼 {-c}{wa(-c)} 같다. 따라서 {ASK} = {ans}이다.", "합 {p + q + r} = −(x²의 계수) ✓", "{ASK} = {ans}"],
        model="f({p}) = 0이므로 조립제법으로 나누면 f(x) = (x {sgn(np)})(x² {sgt(qb)}x {sgn(qc)}) = (x {sgn(np)})(x {sgn(nq)})(x {sgn(nr)})이다. 세 근은 {p}, {q}, {r}이므로 {ASK}은 {ans}이다.",
        rubric=[("인수 찾기·조립제법", 3, "f({p}) = 0을 찾아 (x {sgn(np)})(x² {sgt(qb)}x {sgn(qc)}){ro(qc)} 나누었다.", "인수는 찾았으나 몫이 틀렸으면 1점."), ("근·답", 2, "세 근 {p}, {q}, {r}에서 {ASK} {ans}{eul(ans)} 구했다.", "한 근을 빠뜨렸으면 1점.")],
        pitfalls=[("상수항의 약수를 시도하지 않고 멈춤", "인수 찾기·조립제법", "불인정"), ("조립제법 계산 실수", "인수 찾기·조립제법", "부분"), ("몫의 이차식을 인수분해하지 않음", "근·답", "부분")])


PO_SEED = SEED(PO, category="연산", title="다항식 — 전개 계수·나머지정리·항등식·두 나머지→계수·인수정리·삼차식 인수분해", unit_id="h1-1", concept_ids=["h1-1-01", "h1-1-02", "h1-1-03"],
               schema_name="다항식의 연산과 나머지정리·인수분해", note="근·계수는 파라미터로 잡고 다항식의 계수를 파생(정수 보장). 삼차식은 세 근 p < q < r 로 만든다.",
               templates=[po_t1(), po_t2(), po_t3(), po_t4(), po_t5(), po_t6()])


# ═══════════════════════════════════════════════════════════════════ 2. 복소수
CX = "h1-1-complex"
CX_B = {**HS, "prereq": ["i² = −1", "다항식의 곱셈"], "ops": ["복소수"], "traps": ["i² = −1", "켤레의 부호"], "tags": ["복소수"]}


def cx_t1():
    return T(CX, 1, CX_B, title="복소수의 곱셈 — (a + bi)(c + di) = p + qi에서 p + q",
        skill="분배법칙으로 전개하고 i² = −1을 써서 실수부와 허수부로 정리하기", axis={"a, b, c, d": "±1~±5"}, disc="i²을 −1로 바꾸어 실수부에 −bd를 더하는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "d", "values": {"in": NZ(-5, 5)}}],
        derive={"p": "a*c - b*d", "qq": "a*d + b*c", "ans": "a*c - b*d + a*d + b*c", "bd": "b*d", "ac": "a*c"},
        constraints=["p != 0", "qq != 0", "ans != 0", "ans not in (a, b, c, d)"], cost=["a", "b", "c", "d", "p", "qq", "ans"], verify=["p == ac - bd", "qq == a*d + b*c", "ans == p + qq"],
        q="({a} {sgt(b)}i)({c} {sgt(d)}i) = p + qi일 때, 실수 p, q에 대하여 p + q의 값을 구하시오.", answer="{ans}",
        sol1="복소수의 곱셈은 다항식처럼 전개한 뒤 i² = −1을 쓴다. ({a} {sgt(b)}i)({c} {sgt(d)}i) = {ac} {sgt(a*d)}i {sgt(b*c)}i {sgt(bd)}i²에서 i² = −1이므로 마지막 항 {sgt(bd)}i²은 실수 {sgn(-bd)}{ika(-bd)} 된다.",
        sol2=[("전개: {ac} {sgt(a*d)}i {sgt(b*c)}i {sgt(bd)}i²", "분배법칙"), ("i² = −1: 실수부 {ac} {sgn(-bd)} = {p}, 허수부 {a*d} {sgn(b*c)} = {qq}", "i² = −1"),
              ("p + qi = {p} {sgt(qq)}i → p + q = {ans}", None, ("{ans}", "p + q"))],
        sol3=["실수부는 ac − bd = {ac} − {pn(bd)} = {p}, 허수부는 ad + bc = {a*d} + {pn(b*c)} = {qq}이다(i²의 부호 확인). 따라서 p + q = {ans}이다.", "p = ac − bd = {p}, q = ad + bc = {qq}", "p + q = {ans}"],
        model="({a} {sgt(b)}i)({c} {sgt(d)}i) = {ac} {sgt(a*d + b*c)}i {sgt(bd)}i² = {p} {sgt(qq)}i이므로 p = {p}, q = {qq}이고 p + q = {ans}이다.",
        rubric=[("전개·i² = −1", 3, "i² = −1을 써서 {p} {sgt(qq)}i{ro(qq)} 정리했다.", "i²을 1로 두었으면 인정하지 않는다."), ("p + q", 2, "p + q = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("i²을 1로 둠", "전개·i² = −1", "불인정"), ("허수부의 두 항 중 하나를 빠뜨림", "전개·i² = −1", "부분"), ("p, q를 바꿔 계산", "p + q", "부분")])


def _cx2_rows():
    out = {}
    for c in range(-4, 5):
        for d in range(-4, 5):
            if c == 0 or d == 0:
                continue
            n = c * c + d * d
            for a in range(-6, 7):
                for b in range(-6, 7):
                    if a == 0 or b == 0:
                        continue
                    re_, im_ = a * c + b * d, b * c - a * d              # (a+bi)(c−di)/(c²+d²)
                    if re_ % n or im_ % n or re_ == 0 or im_ == 0:
                        continue
                    out[f"{a}_{b}_{c}_{d}"] = {"a": a, "b": b, "c": c, "d": d, "n": n, "nd": -d, "re": re_ // n, "im": im_ // n, "RE0": re_, "IM0": im_}
    return out


CX2_ROWS = _cx2_rows()


def cx_t2():
    return T(CX, 2, CX_B, title="복소수의 나눗셈 — (a + bi)/(c + di)를 p + qi로",
        skill="분모의 켤레복소수를 분자·분모에 곱해 분모를 실수로 만들기", axis={"분모": "c² + d² | 분자 성분"}, disc="켤레 c − di를 곱해 분모가 c² + d²이 됨을 알고 분자도 전개하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CX2_ROWS)}}, {"name": "ask", "values": {"in": ["p", "q", "pq"]}}],
        table=[{"key": "f", "rows": CX2_ROWS}, {"key": "ask", "rows": {"p": {"ASK": "p", "w1": 1, "w2": 0}, "q": {"ASK": "q", "w1": 0, "w2": 1}, "pq": {"ASK": "p + q", "w1": 1, "w2": 1}}}],
        derive={"ans": "w1*re + w2*im"},
        constraints=["ans != 0", "ans not in (a, b, c, d)", "n <= 25"], cost=["a", "b", "c", "d", "n", "re", "im", "ans"], verify=["re*n == RE0", "im*n == IM0"],
        q="[[frac({a} {sgt(b)}i, {c} {sgt(d)}i)]] = p + qi일 때, 실수 p, q에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="분모 {c} {sgt(d)}i의 켤레복소수 {c} {sgt(nd)}i를 분자와 분모에 곱한다. 분모는 ({c} {sgt(d)}i)({c} {sgt(nd)}i) = {pn(c)}² + {pn(d)}² = {n}{ika(n)} 되어 실수가 되고, 분자 ({a} {sgt(b)}i)({c} {sgt(nd)}i)를 전개해 실수부·허수부로 나눈다.",
        sol2=[("분모: ({c} {sgt(d)}i)({c} {sgt(nd)}i) = {c*c} + {d*d} = {n}", "켤레복소수의 곱 = c² + d²"), ("분자: ({a} {sgt(b)}i)({c} {sgt(nd)}i) = {RE0} {sgt(IM0)}i", "전개, i² = −1"),
              ("[[frac({RE0} {sgt(IM0)}i, {n})]] = {re} {sgt(im)}i → p = {re}, q = {im}, {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["({re} {sgt(im)}i)({c} {sgt(d)}i)를 전개하면 {a} {sgt(b)}i{ika(b)} 되어 원래 분자와 같다. 따라서 {ASK} = {ans}이다.", "(p + qi)(분모) = 분자 ✓", "{ASK} = {ans}"],
        model="분자·분모에 {c} {sgt(nd)}i를 곱하면 [[frac({RE0} {sgt(IM0)}i, {n})]] = {re} {sgt(im)}i이므로 p = {re}, q = {im}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("켤레 곱하기", 3, "분모를 {n}{ro(n)}, 분자를 {RE0} {sgt(IM0)}i{ro(IM0)} 만들었다.", "분모에만 곱했으면 인정하지 않는다."), ("p, q 읽기", 2, "p = {re}, q = {im}에서 {ASK} = {ans}{eul(ans)} 구했다.", "약분 실수면 1점.")],
        pitfalls=[("분모에만 켤레를 곱함", "켤레 곱하기", "불인정"), ("켤레의 부호를 바꾸지 않음", "켤레 곱하기", "불인정"), ("i² = −1 처리 실수", "p, q 읽기", "부분")])


CX3_ROWS = {}
for _k in range(1, 6):
    _n = 4 * _k
    CX3_ROWS[f"pw{_n}"] = {"EXPR": f"(1 + i)^{_n}", "n": _n, "ans": (-4) ** _k, "KEY": "(1 + i)² = 2i", "STEP1": f"(1 + i)^{_n} = ((1 + i)²)^{2 * _k} = (2i)^{2 * _k}", "STEP2": f"(2i)^{2 * _k} = 2^{2 * _k} × i^{2 * _k} = {4 ** _k} × {(-1) ** _k} = {(-4) ** _k}"}
for _n in range(6, 41, 2):
    _v = 2 if _n % 4 == 0 else -2
    CX3_ROWS[f"rt{_n}"] = {"EXPR": f"[[pow(frac(1 + i, 1 − i), {_n})]] + [[pow(frac(1 − i, 1 + i), {_n})]]", "n": _n, "ans": _v, "KEY": "(1 + i)/(1 − i) = i, (1 − i)/(1 + i) = −i",
                           "STEP1": f"i^{_n} + (−i)^{_n} = 2 × i^{_n}", "STEP2": f"{_n} = 4 × {_n // 4} + {_n % 4}이므로 i^{_n} = i^{_n % 4} = {'1' if _n % 4 == 0 else '-1'}, 값은 {_v}"}


def cx_t3():
    return T(CX, 3, CX_B, title="i의 거듭제곱 — (1 + i)^n, ((1 + i)/(1 − i))^n의 값",
        skill="(1 + i)² = 2i, (1 + i)/(1 − i) = i로 바꾼 뒤 i⁴ = 1의 주기성으로 값 구하기", axis={"형태": "(1 + i)^{4k} / 몫의 거듭제곱 합", "n": "4~40"}, disc="먼저 간단한 꼴(2i, i)로 바꾸고 지수를 4로 나눈 나머지로 i^n을 정하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CX3_ROWS)}}], table={"key": "f", "rows": CX3_ROWS},
        derive={"v": "ans"}, constraints=["ans != n"], cost=["n", "ans"], verify=["v == ans"],
        q="{EXPR}의 값을 구하시오. (단, i = [[sqrt(-1)]])", answer="{ans}",
        sol1="{KEY}임을 먼저 쓴다. 그러면 식은 i의 거듭제곱(또는 (2i)의 거듭제곱)이 되고, i⁴ = 1이므로 지수를 4로 나눈 나머지로 값이 정해진다.",
        sol2=[("{KEY}", "간단한 꼴로"), ("{STEP1}", "거듭제곱으로 정리"), ("{STEP2}", None, ("{ans}", "값"))],
        sol3=["i, i², i³, i⁴ = i, −1, −i, 1이 반복되므로 지수 {n}을 4로 나눈 나머지 {n % 4}(0이면 4)에 해당하는 값을 쓴다. 따라서 값은 {ans}이다.", "주기 4: {n} = 4 × {floor(n/4)} + {n % 4}", "값 = {ans}"],
        model="{KEY}이므로 {STEP1}이다. {STEP2}이다.",
        rubric=[("간단한 꼴", 2, "{KEY}{eul(KEY)} 써서 i의 거듭제곱으로 바꿨다.", "직접 전개하다 멈췄으면 1점."), ("주기성·값", 3, "i⁴ = 1의 주기로 {ans}{eul(ans)} 구했다.", "나머지 계산 실수면 1점.")],
        pitfalls=[("(1 + i)² = 2로 계산", "간단한 꼴", "불인정"), ("i³ = i로 착각", "주기성·값", "불인정"), ("2의 거듭제곱 계산 실수", "주기성·값", "부분")])


def cx_t4():
    return T(CX, 4, CX_B, title="복소수가 실수(또는 순허수)가 될 조건",
        skill="(a + bi)(c + xi)를 전개해 허수부(실수부)가 0이 되는 x 구하기", axis={"a, b, c": "±1~±5", "조건": "실수 / 순허수"}, disc="실수 조건은 허수부 = 0, 순허수 조건은 실수부 = 0(허수부 ≠ 0)임을 구별하는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": ["real", "imag"]}}],
        table={"key": "k", "rows": {"real": {"COND": "실수", "PART": "허수부", "w": 1}, "imag": {"COND": "순허수", "PART": "실수부", "w": 0}}},
        derive={"xr": "-b*c/a", "xi": "a*c/b", "ans": "w*(-b*c/a) + (1 - w)*(a*c/b)", "ac": "a*c", "bc": "b*c"},
        constraints=["(w == 1 and (b*c) % a == 0) or (w == 0 and (a*c) % b == 0)", "ans != 0", "ans not in (a, b, c)"], cost=["a", "b", "c", "ans"], verify=["w == 0 or a*ans + b*c == 0", "w == 1 or a*c - b*ans == 0"],
        q="복소수 ({a} {sgt(b)}i)({c} + xi)가 {COND}가 되도록 하는 실수 x의 값을 구하시오.", answer="{ans}",
        sol1="전개하면 ({a} {sgt(b)}i)({c} + xi) = ({ac} {sgt(-b)}x) + ({co(a)}x {sgn(bc)})i이다. {COND}가 되려면 {PART}가 0이어야 한다({COND}이면 {PART} = 0). 그 식을 x에 대해 푼다.",
        sol2=[("({a} {sgt(b)}i)({c} + xi) = ({ac} {sgt(-b)}x) + ({co(a)}x {sgn(bc)})i", "전개, i² = −1"), ("{COND} ⇔ {PART} = 0", "조건"), ("x = {ans}", None, ("{ans}", "x"))],
        sol3=["x = {ans}{eul(ans)} 넣으면 {PART}가 0이 되고 다른 부분은 0이 아니므로 {COND}가 맞다. 따라서 x = {ans}이다.", "x = {ans} → {PART} = 0 ✓", "x = {ans}"],
        model="({a} {sgt(b)}i)({c} + xi) = ({ac} {sgt(-b)}x) + ({co(a)}x {sgn(bc)})i이고 {COND}가 되려면 {PART}가 0이어야 하므로 x = {ans}이다.",
        rubric=[("전개·조건", 3, "실수부 {ac} {sgt(-b)}x, 허수부 {co(a)}x {sgn(bc)}{ro(bc)} 나누고 {PART} = 0을 세웠다.", "실수부와 허수부를 바꿔 조건을 세웠으면 인정하지 않는다."), ("x 구하기", 2, "x = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("실수 조건을 실수부 = 0으로 둠", "전개·조건", "불인정"), ("i² 처리 실수", "전개·조건", "부분"), ("이항 부호 실수", "x 구하기", "부분")])


def cx_t5():
    return T(CX, 5, CX_B, title="켤레복소수 — z + z̄, z z̄, z² 의 값",
        skill="z = a + bi의 켤레 z̄ = a − bi를 써서 합·곱을 계산하기", axis={"a, b": "±1~±6", "구하는 것": "z + z̄ / z z̄ / (z + z̄)(z z̄)"}, disc="z + z̄ = 2a, z z̄ = a² + b²(실수)임을 아는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "k", "values": {"in": ["sum", "prod", "both"]}}],
        table={"key": "k", "rows": {"sum": {"ASK": "z + [[conj(z)]]", "w1": 1, "w2": 0}, "prod": {"ASK": "z[[conj(z)]]", "w1": 0, "w2": 1}, "both": {"ASK": "z + [[conj(z)]] + z[[conj(z)]]", "w1": 1, "w2": 1}}},
        derive={"s": "2*a", "pp": "a*a + b*b", "nb": "-b", "ans": "w1*2*a + w2*(a*a + b*b)"},
        constraints=["ans != 0", "ans not in (a, b)"], cost=["a", "b", "s", "pp", "ans"], verify=["s == 2*a", "pp == a*a + b*b"],
        q="복소수 z = {a} {sgt(b)}i에 대하여 {ASK}의 값을 구하시오. (단, [[conj(z)]]는 z의 켤레복소수)", answer="{ans}",
        sol1="z = {a} {sgt(b)}i의 켤레복소수는 허수부의 부호만 바꾼 [[conj(z)]] = {a} {sgt(nb)}i이다. z + [[conj(z)]] = 2 × (실수부) = {s}, z[[conj(z)]] = (실수부)² + (허수부)² = {a}² + {pn(b)}² = {pp}{ro(pp)} 항상 실수가 된다.",
        sol2=[("[[conj(z)]] = {a} {sgt(nb)}i", "허수부의 부호만 반대"), ("z + [[conj(z)]] = {s}, z[[conj(z)]] = {a}² + {pn(b)}² = {pp}", "합은 2a, 곱은 a² + b²"), ("{ASK} = {ans}", None, ("{ans}", "답"))],
        sol3=["직접 곱해 보면 ({a} {sgt(b)}i)({a} {sgt(nb)}i) = {a*a} − {pn(b*b)}i² = {a*a} + {b*b} = {pp}{ro(pp)} 실수이다. 따라서 {ASK} = {ans}이다.", "z z̄ = {a*a} + {b*b} = {pp} ✓", "{ASK} = {ans}"],
        model="[[conj(z)]] = {a} {sgt(nb)}i이므로 z + [[conj(z)]] = {s}, z[[conj(z)]] = {a}² + {pn(b)}² = {pp}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("켤레·계산", 3, "[[conj(z)]] = {a} {sgt(nb)}i로 놓고 합 {s}, 곱 {pp}{eul(pp)} 구했다.", "곱에서 i² = −1을 놓쳐 a² − b²으로 했으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("z z̄ = a² − b²으로 계산", "켤레·계산", "불인정"), ("켤레의 실수부 부호도 바꿈", "켤레·계산", "불인정"), ("합·곱을 바꿔 답함", "답", "부분")])


CX_SEED = SEED(CX, category="연산", title="복소수 — 곱셈·나눗셈·i의 거듭제곱·실수 조건·켤레복소수", unit_id="h1-1", concept_ids=["h1-1-04"],
               schema_name="복소수의 뜻과 사칙연산", note="나눗셈은 분모 c² + d² 이 분자 성분을 나누는 (a, b, c, d) 만 표로 추림. 켤레 마커 [[conj(z)]].",
               templates=[cx_t1(), cx_t2(), cx_t3(), cx_t4(), cx_t5()])


# ═══════════════════════════════════════════════════════════════════ 3. 이차방정식 (판별식·근과 계수)
QD = "h1-1-quad"
QD_B = {**HS, "prereq": ["근의 공식", "이차방정식의 풀이"], "ops": ["이차방정식"], "traps": ["판별식 부호", "대칭식 변형"], "tags": ["판별식", "근과 계수의 관계"]}


def qd_t1():
    return T(QD, 1, QD_B, title="판별식 — 허근을 가질 때 상수 k의 범위",
        skill="x² + kx + c = 0이 허근을 가지려면 D = k² − 4c < 0임을 써서 k의 범위 구하기", axis={"c": "완전제곱수 1~36"}, disc="D < 0을 세우고 k² < 4c를 −2√c < k < 2√c로 푸는가", diff=3,
        params=[{"name": "s", "values": {"int": [2, 7]}}, {"name": "b", "values": {"in": NZ(-6, 6)}}],
        derive={"c": "s*s", "hi": "2*s", "lo": "-2*s", "lo2": "-2*s + b", "hi2": "2*s + b"},
        constraints=["lo2 != 0"], cost=["s", "c", "b", "lo2", "hi2"], verify=["hi == 2*s", "c == s*s"], ans_var=None,
        q="x에 대한 이차방정식 x² + (k {sgn(-b)})x + {c} = 0이 서로 다른 두 허근을 가질 때, 실수 k의 값의 범위를 구하시오.", answer="{lo2} < k < {hi2}", answer_alt=[],
        sol1="계수가 실수인 이차방정식이 허근을 가질 조건은 판별식 D < 0이다. D = (k {sgn(-b)})² − {4*c} < 0, 즉 (k {sgn(-b)})² < {4*c}이므로 {lo} < k {sgn(-b)} < {hi}이고 여기에 {b}{eul(b)} 더해 k의 범위를 얻는다.",
        sol2=[("D = (k {sgn(-b)})² − 4 × {c} = (k {sgn(-b)})² − {4*c} < 0", "허근 ⇔ D < 0"), ("(k {sgn(-b)})² < {4*c} → {lo} < k {sgn(-b)} < {hi}", "제곱근 풀이: −2√c < ○ < 2√c"), ("{lo2} < k < {hi2}", None, ("{lo2} < k < {hi2}", "k의 범위"))],
        sol3=["경계 k = {lo2}, {hi2}에서는 D = 0(중근)이 되고, 그 사이에서 D < 0이다. 따라서 {lo2} < k < {hi2}이다.", "k = {lo2}, {hi2} → D = 0 (경계)", "{lo2} < k < {hi2}"],
        model="허근을 가지려면 D = (k {sgn(-b)})² − {4*c} < 0이어야 하므로 {lo} < k {sgn(-b)} < {hi}, 즉 {lo2} < k < {hi2}이다.",
        rubric=[("판별식 조건", 3, "D = (k {sgn(-b)})² − {4*c} < 0을 세웠다.", "D > 0으로 세웠으면 인정하지 않는다."), ("범위", 2, "{lo2} < k < {hi2}{eul(hi2)} 구했다.", "한쪽 경계만 썼으면 1점.")],
        pitfalls=[("D > 0으로 조건을 세움", "판별식 조건", "불인정"), ("k² < 4c에서 k < 2√c만 씀", "범위", "부분"), ("이항 부호 실수", "범위", "부분")])


def qd_t2():
    return T(QD, 2, QD_B, title="근과 계수의 관계 — 두 근의 대칭식 α² + β², (α − β)², 1/α + 1/β",
        skill="α + β = −b/a, αβ = c/a를 구한 뒤 대칭식을 합·곱으로 변형하기", axis={"이차방정식": "x² + bx + c", "대칭식": "3가지"}, disc="근을 직접 구하지 않고 합·곱으로 변형하며, α² + β² = (α + β)² − 2αβ 등의 부호를 지키는가", diff=3,
        params=[{"name": "s", "values": {"in": NZ(-7, 7)}}, {"name": "p", "values": {"in": NZ(-8, 8)}}, {"name": "k", "values": {"in": ["sq", "dsq", "inv"]}}],
        table={"key": "k", "rows": {"sq": {"ASK": "α² + β²", "FORM": "(α + β)² − 2αβ", "w1": 1, "w2": 0, "w3": 0}, "dsq": {"ASK": "(α − β)²", "FORM": "(α + β)² − 4αβ", "w1": 0, "w2": 1, "w3": 0}, "inv": {"ASK": "1/α + 1/β", "FORM": "(α + β)/(αβ)", "w1": 0, "w2": 0, "w3": 1}}},
        derive={"b": "-s", "c": "p", "v1": "s*s - 2*p", "v2": "s*s - 4*p", "v3": "s/p", "ans": "w1*(s*s - 2*p) + w2*(s*s - 4*p) + w3*s/p"},
        constraints=["ans != 0", "ans not in (s, p, b)", "w3 == 0 or s % p == 0"], cost=["s", "p", "ans"], verify=["v1 == s*s - 2*p", "v2 == s*s - 4*p"],
        q="이차방정식 x² {sgt(b)}x {sgn(c)} = 0의 두 근을 α, β라 할 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="근과 계수의 관계에서 α + β = {s}, αβ = {p}이다. 근을 직접 구하지 않고 {ASK} = {FORM}으로 변형해 합과 곱을 대입한다.",
        sol2=[("α + β = {s}, αβ = {p}", "근과 계수의 관계"), ("{ASK} = {FORM}", "대칭식의 변형"), ("= {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["α² + β² = {v1}, (α − β)² = {v2}, 1/α + 1/β = (α + β)/(αβ)로 세 대칭식이 모두 합 {s}, 곱 {p}만으로 정해진다. 따라서 {ASK} = {ans}이다.", "합 {s}, 곱 {p}", "{ASK} = {ans}"],
        model="α + β = {s}, αβ = {p}이므로 {ASK} = {FORM} = {ans}이다.",
        rubric=[("근과 계수", 2, "α + β = {s}, αβ = {p}{eul(p)} 구했다.", "부호가 틀렸으면 인정하지 않는다."), ("변형·계산", 3, "{ASK} = {FORM}{ro(ans)} 변형해 {ans}{eul(ans)} 구했다.", "변형 공식의 부호가 틀렸으면 1점.")],
        pitfalls=[("α + β = b(부호 반대)로 둠", "근과 계수", "불인정"), ("α² + β² = (α + β)²으로 둠", "변형·계산", "불인정"), ("(α − β)²에서 4αβ 대신 2αβ", "변형·계산", "부분")])


def qd_t3():
    return T(QD, 3, QD_B, title="두 근이 α + 1, β + 1인 이차방정식 만들기",
        skill="새 두 근의 합과 곱을 구해 x² − (합)x + (곱) = 0 세우기", axis={"원래 방정식": "x² + bx + c", "이동": "+1 / −1 / 2배"}, disc="새 근의 합·곱을 원래 합·곱으로 나타내고 x² − (합)x + (곱)의 부호를 지키는가", diff=3,
        params=[{"name": "s", "values": {"in": NZ(-6, 6)}}, {"name": "p", "values": {"in": NZ(-8, 8)}}, {"name": "k", "values": {"in": ["p1", "m1", "d2"]}}],
        table={"key": "k", "rows": {"p1": {"NEW": "α + 1, β + 1", "SUMF": "(α + β) + 2", "PRODF": "αβ + (α + β) + 1", "ws": 1, "wp": 1, "kk": 1, "cc": 1},
                                    "m1": {"NEW": "α − 1, β − 1", "SUMF": "(α + β) − 2", "PRODF": "αβ − (α + β) + 1", "ws": 1, "wp": -1, "kk": 1, "cc": -1},
                                    "d2": {"NEW": "2α, 2β", "SUMF": "2(α + β)", "PRODF": "4αβ", "ws": 2, "wp": 0, "kk": 4, "cc": 0}}},
        derive={"b": "-s", "c": "p", "ns": "ws*s + 2*cc", "npd": "kk*p + wp*s + cc*cc", "ans": "-(ws*s + 2*cc) + (kk*p + wp*s + cc*cc)"},
        constraints=["ns != 0", "npd != 0", "ans != 0", "ans not in (s, p, b)"], cost=["s", "p", "ns", "npd", "ans"], verify=["ans == -ns + npd"],
        q="이차방정식 x² {sgt(b)}x {sgn(c)} = 0의 두 근을 α, β라 할 때, 두 근이 {NEW}인 이차방정식이 x² + mx + n = 0이다. 상수 m, n에 대하여 m + n의 값을 구하시오.", answer="{ans}",
        sol1="α + β = {s}, αβ = {p}이다. 새 두 근의 합은 {SUMF} = {ns}, 곱은 {PRODF} = {npd}이므로 구하는 방정식은 x² − (합)x + (곱) = 0, 즉 x² {sgt(-ns)}x {sgn(npd)} = 0이다. 따라서 m = {-ns}, n = {npd}.",
        sol2=[("α + β = {s}, αβ = {p}", "근과 계수의 관계"), ("새 근의 합 {SUMF} = {ns}, 곱 {PRODF} = {npd}", "새 근의 합·곱"), ("x² {sgt(-ns)}x {sgn(npd)} = 0 → m = {-ns}, n = {npd}, m + n = {ans}", None, ("{ans}", "m + n"))],
        sol3=["m은 새 근의 합의 부호를 바꾼 값 {-ns}, n은 새 근의 곱 {npd}이다. 합의 부호를 그대로 쓰면 틀린다. 따라서 m + n = {ans}이다.", "m = −(합) = {-ns}, n = 곱 = {npd}", "m + n = {ans}"],
        model="α + β = {s}, αβ = {p}이므로 새 두 근의 합은 {ns}, 곱은 {npd}이다. 구하는 방정식은 x² {sgt(-ns)}x {sgn(npd)} = 0이므로 m + n = {ans}이다.",
        rubric=[("새 근의 합·곱", 3, "합 {ns}, 곱 {npd}{eul(npd)} 구했다.", "곱의 전개에서 (α + β) 항을 빠뜨렸으면 1점."), ("방정식·답", 2, "x² {sgt(-ns)}x {sgn(npd)} = 0을 세워 m + n = {ans}{eul(ans)} 구했다.", "합의 부호를 그대로 썼으면 인정하지 않는다.")],
        pitfalls=[("x² + (합)x + (곱)으로 부호를 틀림", "방정식·답", "불인정"), ("곱의 전개에서 (α + β) 항 누락", "새 근의 합·곱", "부분"), ("원래 합의 부호 실수", "새 근의 합·곱", "불인정")])


def _qd_conj(no, title, kind, root_q, root_sol, prod_f, prod_expr, qvals, extra_constraints):
    return T(QD, no, QD_B, title=title,
        skill="켤레근도 근임을 써서 합·곱으로 a, b 구하기", axis={"p": "±1~±4", "q": qvals}, disc=f"계수가 {kind}이면 켤레근도 근임을 알고 합 2p, 곱 {prod_f}로 계수를 정하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-4, 4)}}, {"name": "qv", "values": {"in": [2, 3, 5, 6, 7] if kind == "유리수" else [1, 2, 3, 4, 5]}}],
        derive={"s": "2*p", "prod": prod_expr, "a": "-2*p", "b": prod_expr, "ans": f"-2*p + {prod_expr}"},
        constraints=["b != 0", "ans != 0", "ans not in (p, qv)"] + extra_constraints, cost=["p", "qv", "s", "prod", "ans"], verify=["a == -s", "b == prod"],
        q=f"x에 대한 이차방정식 x² + ax + b = 0의 한 근이 {{p}} + {root_q}일 때, {kind} a, b에 대하여 a + b의 값을 구하시오.", answer="{ans}",
        sol1=f"계수가 {kind}인 이차방정식의 한 근이 {{p}} + {root_q}이면 다른 한 근은 켤레인 {{p}} − {root_q}이다. 두 근의 합은 {{s}}, 곱은 {prod_f} = {{prod}}이므로 근과 계수의 관계에서 a = −(합) = {{a}}, b = (곱) = {{b}}이다.",
        sol2=[(f"다른 한 근: {{p}} − {root_q} (켤레근)", f"계수가 {kind}"), (f"합 = {{s}}, 곱 = ({{p}} + {root_q})({{p}} − {root_q}) = {{prod}}", "합차 공식"), ("a = −({s}) = {a}, b = {prod} → a + b = {ans}", None, ("{ans}", "a + b"))],
        sol3=[f"x = {{p}} + {root_sol}{{eul(qv)}} x² {{sgt(a)}}x {{sgn(b)}}에 넣으면 0이 된다(직접 전개해 확인). 따라서 a + b = {{ans}}이다.", "x² {sgt(a)}x {sgn(b)} = 0에 근 대입 → 0 ✓", "a + b = {ans}"],
        model=f"켤레근 {{p}} − {root_q}도 근이므로 두 근의 합은 {{s}}, 곱은 {{prod}}이다. 따라서 a = {{a}}, b = {{b}}이고 a + b = {{ans}}이다.",
        rubric=[("켤레근", 2, f"다른 한 근이 {{p}} − {root_q}임을 밝혔다.", "근거 없이 썼으면 1점."), ("계수 구하기", 3, "합 {s}, 곱 {prod}에서 a = {a}, b = {b}{ro(b)} 구해 a + b = {ans}{eul(ans)} 답했다.", "a의 부호가 틀렸으면 1점.")],
        pitfalls=[("켤레근을 쓰지 않고 한 근만 대입해 못 풂", "켤레근", "불인정"), ("a = 합(부호 반대)으로 둠", "계수 구하기", "부분"), ("곱의 계산에서 (√q)² 또는 i² 실수", "계수 구하기", "부분")])


def qd_t4():
    return _qd_conj(4, "한 근이 p + √q인 유리계수 이차방정식의 계수", "유리수", "[[sqrt({qv})]]", "[[sqrt({qv})]]", "p² − q", "p*p - qv", "2·3·5·6·7", [])


def qd_t6():
    return _qd_conj(6, "한 근이 p + qi인 실계수 이차방정식의 계수", "실수", "{qv}i", "{qv}i", "p² + q²", "p*p + qv*qv", "1~5", [])


def qd_t5():
    return T(QD, 5, QD_B, title="두 근의 차가 주어진 이차방정식의 상수",
        skill="α − β = d에서 (α − β)² = (α + β)² − 4αβ를 써서 상수 구하기", axis={"합": "±2~±9", "차": "1~6"}, disc="두 근의 차를 대칭식 (α + β)² − 4αβ로 바꾸어 상수를 구하는가", diff=3,
        params=[{"name": "s", "values": {"in": NZ(-12, 12)}}, {"name": "d", "values": {"int": [1, 8]}}],
        derive={"b": "-s", "p": "(s*s - d*d)/4", "s2": "s*s", "d2": "d*d", "ans": "(s*s - d*d)/4"},
        constraints=["(s*s - d*d) % 4 == 0", "ans != 0", "ans not in (s, d, b)"], cost=["s", "d", "s2", "d2", "ans"], verify=["4*ans == s2 - d2"],
        q="이차방정식 x² {sgt(b)}x + k = 0의 두 근의 차가 {d}일 때, 상수 k의 값을 구하시오.", answer="{ans}",
        sol1="두 근을 α, β라 하면 α + β = {s}, αβ = k이다. 두 근의 차가 {d}이므로 (α − β)² = {d2}이고, (α − β)² = (α + β)² − 4αβ = {s2} − 4k이다. 이 식에서 k를 구한다.",
        sol2=[("α + β = {s}, αβ = k", "근과 계수의 관계"), ("(α − β)² = (α + β)² − 4αβ → {d2} = {s2} − 4k", "차의 제곱을 합·곱으로"), ("4k = {s2 - d2} → k = {ans}", None, ("{ans}", "k"))],
        sol3=["k = {ans}이면 두 근은 [[frac(pm({s}, {d}), 2)]] = {(s + d)/2}, {(s - d)/2}{ro((s - d)/2)} 차가 {d}, 합이 {s}이다. 따라서 k = {ans}이다.", "두 근 {(s + d)/2}, {(s - d)/2}: 차 {d} ✓", "k = {ans}"],
        model="α + β = {s}, αβ = k이고 (α − β)² = (α + β)² − 4αβ이므로 {d2} = {s2} − 4k에서 k = {ans}이다.",
        rubric=[("대칭식 변형", 3, "(α − β)² = (α + β)² − 4αβ를 써서 {d2} = {s2} − 4k를 세웠다.", "2αβ로 썼으면 1점."), ("k 구하기", 2, "k = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("(α − β)² = (α + β)² − 2αβ로 둠", "대칭식 변형", "부분"), ("α − β = d를 α + β와 혼동", "대칭식 변형", "불인정"), ("이항 부호 실수", "k 구하기", "부분")])


QD_SEED = SEED(QD, category="연산", title="이차방정식 — 판별식 범위·근과 계수 대칭식·두 근으로 방정식·무리근 계수·근의 차·허근 계수", unit_id="h1-1", concept_ids=["h1-1-05", "h1-1-06"],
               schema_name="이차방정식의 판별식과 근과 계수의 관계", note="합 s·곱 p 를 파라미터로 두어 계수를 파생. 범위 답은 'lo < k < hi' 문자열(answer_var 없음).",
               templates=[qd_t1(), qd_t2(), qd_t3(), qd_t4(), qd_t5(), qd_t6()])


# ═══════════════════════════════════════════════════════════════════ 4. 이차함수와 직선·최대최소
QF = "h1-1-quadfn"
QF_B = {**HS, "prereq": ["판별식", "이차함수의 꼭짓점"], "ops": ["이차함수"], "traps": ["판별식 부호", "범위의 끝값"], "tags": ["이차함수와 직선", "최대·최소"]}


def qf_t1():
    return T(QF, 1, QF_B, title="이차함수의 그래프와 직선이 만나지 않을(두 점에서 만날) 조건 — k의 범위",
        skill="y = x² + ax + b와 y = mx + k를 연립한 이차방정식의 판별식 부호로 교점 개수 정하기", axis={"이차함수": "x² + ax + b", "직선": "y = mx + k", "조건": "만나지 않음 / 서로 다른 두 점"}, disc="연립해 x² + (a − m)x + (b − k) = 0의 판별식을 세우고 부등호 방향을 조건에 맞추는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "m", "values": {"in": NZ(-4, 4)}}, {"name": "k", "values": {"in": ["none", "two"]}}],
        table={"key": "k", "rows": {"none": {"COND": "만나지 않을", "OP": "<", "DC": "< 0"}, "two": {"COND": "서로 다른 두 점에서 만날", "OP": ">", "DC": "> 0"}}},
        derive={"am": "a - m", "am2": "(a - m)**2", "T": "b - (a - m)**2/4"},
        constraints=["am != 0", "am % 2 == 0", "T != 0"], cost=["a", "b", "m", "am", "T"], verify=["4*T == 4*b - am2"], ans_var=None,
        q="이차함수 y = x² {sgt(a)}x {sgn(b)}의 그래프와 직선 y = {co(m)}x + k가 {COND} 때, 실수 k의 값의 범위를 구하시오.", answer="k {OP} {T}",
        sol1="두 그래프의 교점의 x좌표는 x² {sgt(a)}x {sgn(b)} = {co(m)}x + k, 즉 x² {sgt(am)}x + ({b} − k) = 0의 실근이다. 교점의 개수는 이 이차방정식의 판별식 D의 부호로 정해진다: {COND} 조건은 D {DC}.",
        sol2=[("연립: x² {sgt(am)}x + ({b} − k) = 0", "교점 ⇔ 실근"), ("D = {am2} − 4({b} − k) {DC}", "{COND} ⇔ D {DC}"), ("4k {OP} {4*b - am2} → k {OP} {T}", None, ("k {OP} {T}", "k의 범위"))],
        sol3=["k = {T}이면 D = 0으로 접한다(경계). 그보다 k가 크면 직선이 위로 올라가 두 점에서 만나고, 작으면 만나지 않는다. 따라서 k {OP} {T}이다.", "k = {T}: 접함 (경계)", "k {OP} {T}"],
        model="연립하면 x² {sgt(am)}x + ({b} − k) = 0이고 {COND} 조건은 D = {am2} − 4({b} − k) {DC}이므로 k {OP} {T}이다.",
        rubric=[("연립·판별식", 3, "x² {sgt(am)}x + ({b} − k) = 0의 판별식 조건 D {DC}{eul(DC)} 세웠다.", "부등호 방향이 반대면 1점."), ("범위", 2, "k {OP} {T}{eul(T)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("판별식의 부등호 방향을 반대로 둠", "연립·판별식", "불인정"), ("연립 없이 이차함수의 판별식만 봄", "연립·판별식", "불인정"), ("4로 나누는 계산 실수", "범위", "부분")])


def qf_t2():
    return T(QF, 2, QF_B, title="이차함수의 그래프에 접하는 직선 — 상수 k",
        skill="연립한 이차방정식의 판별식 D = 0으로 접할 조건 세우기", axis={"이차함수": "x² + ax + b", "직선의 기울기": "±1~±5"}, disc="접한다 ⇔ 연립 방정식이 중근(D = 0)임을 쓰는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-8, 8)}}, {"name": "m", "values": {"in": NZ(-5, 5)}}],
        derive={"am": "a - m", "am2": "(a - m)**2", "ans": "b - (a - m)**2/4"},
        constraints=["am != 0", "am % 2 == 0", "ans != 0", "ans not in (a, b, m)"], cost=["a", "b", "m", "am", "ans"], verify=["4*ans == 4*b - am2"],
        q="직선 y = {co(m)}x + k가 이차함수 y = x² {sgt(a)}x {sgn(b)}의 그래프에 접할 때, 상수 k의 값을 구하시오.", answer="{ans}",
        sol1="접한다는 것은 교점이 하나(중근)라는 뜻이다. 연립하면 x² {sgt(am)}x + ({b} − k) = 0이고, 이 방정식의 판별식이 0이어야 한다: D = {am2} − 4({b} − k) = 0.",
        sol2=[("연립: x² {sgt(am)}x + ({b} − k) = 0", "접점 ⇔ 중근"), ("D = {am2} − 4({b} − k) = 0", "접함 ⇔ D = 0"), ("4k = {4*b - am2} → k = {ans}", None, ("{ans}", "k"))],
        sol3=["k = {ans}이면 연립 방정식은 (x {sgn(am/2)})² = 0이 되어 x = {-am/2}에서 접한다. 따라서 k = {ans}이다.", "접점의 x좌표 {-am/2}", "k = {ans}"],
        model="연립하면 x² {sgt(am)}x + ({b} − k) = 0이고 접하려면 D = {am2} − 4({b} − k) = 0이어야 하므로 k = {ans}이다.",
        rubric=[("접할 조건", 3, "연립한 이차방정식의 D = 0을 세웠다.", "D > 0 또는 < 0으로 세웠으면 인정하지 않는다."), ("k 구하기", 2, "k = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("접할 조건을 D > 0으로 둠", "접할 조건", "불인정"), ("연립 없이 이차함수의 판별식을 씀", "접할 조건", "불인정"), ("계산 실수", "k 구하기", "부분")])


def qf_t3():
    return T(QF, 3, QF_B, title="제한된 범위에서 이차함수의 최댓값·최솟값",
        skill="꼭짓점의 x좌표가 범위 안에 있는지 확인하고 꼭짓점·양 끝값 중에서 최대·최소 고르기", axis={"이차함수": "±(x − p)² + q", "범위": "p − 3 ≤ x ≤ p + 1 등"}, disc="꼭짓점이 범위 안이면 꼭짓점의 값이 최대(최소), 반대쪽 극값은 끝값에서 나옴을 아는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-3, 3)}}, {"name": "qv", "values": {"in": NZ(-5, 5)}}, {"name": "l", "values": {"int": [1, 3]}}, {"name": "r", "values": {"int": [1, 3]}}, {"name": "k", "values": {"in": ["min", "max"]}}, {"name": "sgk", "values": {"in": [1, -1]}}],
        table={"key": "k", "rows": {"min": {"ASK": "최솟값", "wmin": 1}, "max": {"ASK": "최댓값", "wmin": 0}}},
        derive={"lo": "p - l", "hi": "p + r", "b": "-2*sgk*p", "c": "sgk*p*p + qv", "fl": "sgk*l*l + qv", "fr": "sgk*r*r + qv", "far": "max(l, r)", "fend": "sgk*max(l, r)**2 + qv", "np": "-p", "xfar": "(p + r)*(1 + sign(r - l))/2 + (p - l)*(1 - sign(r - l))/2",
                "ans": "wmin*(qv*(sgk == 1) + fend*(sgk == -1)) + (1 - wmin)*(fend*(sgk == 1) + qv*(sgk == -1))"},
        constraints=["l != r", "c != 0", "ans not in (lo, hi, b, c)", "ans != 0", "ans != qv or (wmin == 1 and sgk == 1) or (wmin == 0 and sgk == -1)"], cost=["p", "qv", "lo", "hi", "fl", "fr", "ans"], verify=["fend == fl or fend == fr"],
        q="{lo} ≤ x ≤ {hi}에서 이차함수 y = {co(sgk)}x² {sgt(b)}x {sgn(c)}의 {ASK}을 구하시오.", answer="{ans}",
        sol1="완전제곱식으로 고치면 y = {co(sgk)}(x {sgn(np)})² {sgn(qv)}이고 꼭짓점은 ({p}, {qv})이다. 꼭짓점의 x좌표 {p}{ika(p)} 범위 {lo} ≤ x ≤ {hi} 안에 있으므로 한쪽 극값은 꼭짓점의 값 {qv}, 다른 쪽 극값은 꼭짓점에서 더 먼 끝 x = {xfar}에서의 값 {fend}이다.",
        sol2=[("y = {co(sgk)}(x {sgn(np)})² {sgn(qv)} → 꼭짓점 ({p}, {qv}), 범위 안", "완전제곱식"), ("양 끝값: f({lo}) = {fl}, f({hi}) = {fr}", "끝값 비교"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["x² 의 계수가 {sgk}이므로 꼭짓점에서 {ASK}{ika(ASK)} 되는지(아래로 볼록이면 최솟값) 확인하고, 반대쪽은 꼭짓점에서 먼 끝에서 나온다. 따라서 {ASK} = {ans}이다.", "꼭짓점 값 {qv}, 끝값 {fl}·{fr}", "{ASK} = {ans}"],
        model="y = {co(sgk)}(x {sgn(np)})² {sgn(qv)}이고 꼭짓점 ({p}, {qv})이 범위 안에 있다. f({lo}) = {fl}, f({hi}) = {fr}이므로 {ASK}은 {ans}이다.",
        rubric=[("꼭짓점·범위", 3, "꼭짓점 ({p}, {qv})이 범위 안에 있음을 확인하고 끝값 {fl}, {fr}{eul(fr)} 구했다.", "끝값을 하나만 구했으면 1점."), ("답", 2, "{ASK} {ans}{eul(ans)} 답했다.", "최대·최소를 바꿨으면 인정하지 않는다.")],
        pitfalls=[("범위를 무시하고 꼭짓점 값만 답함", "답", "불인정"), ("끝값 중 가까운 쪽을 택함", "꼭짓점·범위", "부분"), ("완전제곱식 변형 실수", "꼭짓점·범위", "부분")])


def qf_t4():
    return T(QF, 4, QF_B, title="꼭짓점이 범위 밖에 있을 때의 최댓값·최솟값",
        skill="꼭짓점의 x좌표가 범위 밖이면 함수가 범위에서 단조이므로 양 끝값이 최대·최소임을 쓰기", axis={"이차함수": "(x − p)² + q", "범위": "꼭짓점 오른쪽/왼쪽"}, disc="꼭짓점이 범위 밖일 때 꼭짓점 값을 답하지 않고 양 끝값만 비교하는가", diff=3,
        params=[{"name": "p", "values": {"in": NZ(-3, 3)}}, {"name": "qv", "values": {"in": NZ(-5, 5)}}, {"name": "g", "values": {"int": [1, 3]}}, {"name": "w", "values": {"int": [1, 3]}}, {"name": "side", "values": {"in": [1, -1]}}, {"name": "k", "values": {"in": ["min", "max"]}}],
        table={"key": "k", "rows": {"min": {"ASK": "최솟값", "wmin": 1}, "max": {"ASK": "최댓값", "wmin": 0}}},
        derive={"lo": "p + side*g - (side == -1)*w", "hi": "p + side*g + (side == 1)*w", "b": "-2*p", "c": "p*p + qv", "np": "-p", "fnear": "g*g + qv", "ffar": "(g + w)**2 + qv", "ans": "wmin*(g*g + qv) + (1 - wmin)*((g + w)**2 + qv)"},
        constraints=["c != 0", "ans not in (lo, hi, qv, b, c)", "ans != 0"], cost=["p", "qv", "lo", "hi", "fnear", "ffar", "ans"], verify=["ffar > fnear"],
        q="{lo} ≤ x ≤ {hi}에서 이차함수 y = x² {sgt(b)}x {sgn(c)}의 {ASK}을 구하시오.", answer="{ans}",
        sol1="완전제곱식으로 고치면 y = (x {sgn(np)})² {sgn(qv)}, 꼭짓점 ({p}, {qv})이다. 꼭짓점의 x좌표 {p}{eun(p)} 범위 {lo} ≤ x ≤ {hi} 밖에 있으므로 이 범위에서 그래프는 한쪽으로만 증가하거나 감소한다. 따라서 최댓값·최솟값은 모두 양 끝 x = {lo}, x = {hi}에서 나온다.",
        sol2=[("y = (x {sgn(np)})² {sgn(qv)}, 꼭짓점 ({p}, {qv})은 범위 밖", "완전제곱식"), ("f({lo}) = {(lo - p)**2 + qv}, f({hi}) = {(hi - p)**2 + qv}", "양 끝값"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["꼭짓점에서 먼 끝일수록 (x {sgn(np)})²이 크므로 값이 크다. 꼭짓점 값 {qv}{eun(qv)} 범위 밖이라 답이 아니다. 따라서 {ASK} = {ans}이다.", "꼭짓점 밖 → 끝값만 비교", "{ASK} = {ans}"],
        model="y = (x {sgn(np)})² {sgn(qv)}이고 꼭짓점 ({p}, {qv})이 범위 밖에 있으므로 f({lo}) = {(lo - p)**2 + qv}, f({hi}) = {(hi - p)**2 + qv} 중에서 {ASK}은 {ans}이다.",
        rubric=[("꼭짓점 위치", 3, "꼭짓점이 범위 밖임을 확인하고 양 끝값을 구했다.", "꼭짓점 값을 최솟값으로 썼으면 인정하지 않는다."), ("답", 2, "{ASK} {ans}{eul(ans)} 답했다.", "계산 실수면 1점.")],
        pitfalls=[("꼭짓점 값 q를 최솟값으로 답함", "꼭짓점 위치", "불인정"), ("끝값 계산 실수", "답", "부분"), ("최대·최소를 바꿈", "답", "부분")])


QF_SEED = SEED(QF, category="함수", title="이차함수와 직선·최대최소 — 교점 개수 범위·접선 상수·범위 안 꼭짓점·범위 밖 꼭짓점", unit_id="h1-1", concept_ids=["h1-1-07", "h1-1-08"],
               schema_name="이차함수의 그래프와 직선의 위치 관계·최대최소", note="직선과의 위치 관계는 a − m 짝수로 잡아 경계 T 를 정수로. 제한범위 최대최소는 꼭짓점 (p, q) 기준으로 범위를 만든다.",
               templates=[qf_t1(), qf_t2(), qf_t3(), qf_t4()])


if __name__ == "__main__":
    run(PO_SEED, CX_SEED, QD_SEED, QF_SEED)
