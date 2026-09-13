# itemfactory/tools/mkseed_h2_seq.py — 고2 수학I 수열 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h2_seq.py
#     → seeds/h2-1-seq.json   (수열: 등차 항·등차 합·등비 항·등비 합·∑ 계산·합과 일반항·여러 가지 수열의 합·귀납적 정의, 8틀)
#   수열 표기 {aₙ}는 {{ }} 이스케이프, 항 번호는 {sub(n)} (expr v1.3). 수학적 귀납법(17)은 수치 답 틀이 없어 보류.
from __future__ import annotations

import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import sub as _sub, eul as _eul  # noqa: E402

rng = random.Random(20260917)


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


SQ = "h2-1-seq"
SQ_B = {**HS, "prereq": ["일차함수", "지수법칙"], "ops": ["수열"], "traps": ["항 번호와 항의 값 혼동", "n − 1 개수 세기"], "tags": ["등차수열", "등비수열", "수열의 합"]}


# ── t1 등차수열의 항 ──────────────────────────────────────────
def sq_t1():
    return T(SQ, 1, SQ_B, title="등차수열 — 두 항으로 다른 항 구하기",
        skill="aₙ = a + (n − 1)d에 두 항을 넣어 a, d를 정한 뒤 다른 항 구하기", axis={"첫째항": "−10~10", "공차": "±1~±4", "항 번호": "1~20"}, disc="두 항의 차를 항 번호의 차로 나눠 공차를 구하는가", diff=2,
        params=[{"name": "a1", "values": {"int": [-10, 10]}}, {"name": "d", "values": {"in": NZ(-4, 4)}}, {"name": "p", "values": {"int": [1, 6]}}, {"name": "qn", "values": {"int": [2, 10]}}, {"name": "r", "values": {"int": [1, 20]}}],
        derive={"u": "a1 + (p - 1)*d", "v": "a1 + (qn - 1)*d", "ans": "a1 + (r - 1)*d", "dn": "qn - p", "dv": "(qn - p)*d"},
        constraints=["p < qn", "r != p", "r != qn", "ans != 0", "ans not in (u, v, p, qn, r)", "u != v"], cost=["a1", "d", "p", "qn", "r", "u", "v", "ans"], verify=["v - u == dn*d", "ans == u + (r - p)*d"],
        q="등차수열 {{aₙ}}에 대하여 a{sub(p)} = {u}, a{sub(qn)} = {v}일 때, a{sub(r)}의 값을 구하시오.", answer="{ans}",
        sol1="등차수열의 일반항은 aₙ = a + (n − 1)d(a: 첫째항, d: 공차)이다. 두 항의 차 a{sub(qn)} − a{sub(p)} = {v} − {pn(u)} = {dv}{ika(dv)} 항 번호의 차 {dn}에 공차를 곱한 것이므로 d = {d}이다.",
        sol2=[("a{sub(qn)} − a{sub(p)} = ({qn} − {p})d → {dv} = {dn}d → d = {d}", "공차"), ("a = a{sub(p)} − ({p} − 1)d = {u} − {p - 1} × {pn(d)} = {a1}", "첫째항"), ("a{sub(r)} = {a1} + ({r} − 1) × {pn(d)} = {ans}", None, ("{ans}", "a{sub(r)}"))],
        sol3=["a{sub(r)} = a{sub(p)} + ({r} − {p})d = {u} + {pn(r - p)} × {pn(d)} = {ans}{ro(ans)} 다른 항에서 출발해도 같다. 따라서 a{sub(r)} = {ans}이다.", "a{sub(r)} = a{sub(p)} + ({r} − {p})d", "a{sub(r)} = {ans}"],
        model="공차 d = ({v} − {pn(u)})/({qn} − {p}) = {d}, 첫째항 a = {a1}이므로 a{sub(r)} = {a1} + ({r} − 1) × {pn(d)} = {ans}이다.",
        rubric=[("공차·첫째항", 3, "d = {d}, a = {a1}{eul(a1)} 구했다.", "공차만 맞으면 1점."), ("항 구하기", 2, "a{sub(r)} = {ans}{eul(ans)} 구했다.", "n − 1 대신 n을 곱했으면 1점.")],
        pitfalls=[("항 번호의 차 대신 항 번호로 나눔", "공차·첫째항", "불인정"), ("aₙ = a + nd로 둠", "항 구하기", "부분"), ("부호 실수", "항 구하기", "부분")])


# ── t2 등차수열의 합 ──────────────────────────────────────────
def sq_t2():
    return T(SQ, 2, SQ_B, title="등차수열의 합 — Sₙ = n(2a + (n − 1)d)/2",
        skill="첫째항과 공차(또는 끝항)로 첫째항부터 제n항까지의 합 구하기", axis={"첫째항": "−8~10", "공차": "±1~±5", "n": "5~20"}, disc="n(a + l)/2 또는 n(2a + (n − 1)d)/2를 바르게 세우는가", diff=2,
        params=[{"name": "a1", "values": {"int": [-8, 10]}}, {"name": "d", "values": {"in": NZ(-5, 5)}}, {"name": "n", "values": {"int": [5, 20]}}],
        derive={"last": "a1 + (n - 1)*d", "ans": "n*(2*a1 + (n - 1)*d)/2", "twoa": "2*a1"},
        constraints=["ans != 0", "ans not in (a1, d, n, last)", "last != 0"], cost=["a1", "d", "n", "last", "ans"], verify=["2*ans == n*(a1 + last)"],
        q="첫째항이 {a1}, 공차가 {d}인 등차수열 {{aₙ}}의 첫째항부터 제{n}항까지의 합을 구하시오.", answer="{ans}",
        sol1="등차수열의 합은 Sₙ = n(a + l)/2 (l: 제n항) = n(2a + (n − 1)d)/2이다. 첫째항 a = {a1}, 공차 d = {d}이고 제{n}항은 a{sub(n)} = {a1} + ({n} − 1) × {pn(d)} = {last}이다.",
        sol2=[("a = {a1}, d = {d}", "첫째항·공차"), ("a{sub(n)} = {a1} + {n - 1} × {pn(d)} = {last}", "끝항"), ("S{sub(n)} = [[frac({n}({pn(a1)} + {pn(last)}), 2)]] = {ans}", None, ("{ans}", "S{sub(n)}"))],
        sol3=["S{sub(n)} = [[frac({n}(2 × {pn(a1)} + ({n} − 1) × {pn(d)}), 2)]] = [[frac({n} × {pn(twoa + (n - 1)*d)}, 2)]] = {ans}{ro(ans)} 다른 공식으로도 같다. 따라서 합은 {ans}이다.", "n(2a + (n − 1)d)/2 ✓", "S{sub(n)} = {ans}"],
        model="a = {a1}, d = {d}, a{sub(n)} = {last}이므로 S{sub(n)} = [[frac({n}({pn(a1)} + {pn(last)}), 2)]] = {ans}이다.",
        rubric=[("공식 세우기", 3, "S{sub(n)} = n(a + l)/2 또는 n(2a + (n − 1)d)/2에 a = {a1}, d = {d}, n = {n}{eul(n)} 넣었다.", "끝항을 잘못 구했으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("2로 나누는 것을 잊음", "공식 세우기", "불인정"), ("(n − 1)d 대신 nd", "공식 세우기", "부분"), ("두 항에서 공차를 (a₅ − a₂)/5로 둠", "공식 세우기", "불인정")])


# ── t3 등비수열의 항 ──────────────────────────────────────────
def sq_t3():
    return T(SQ, 3, SQ_B, title="등비수열 — 두 항으로 다른 항 구하기",
        skill="aₙ = arⁿ⁻¹에 두 항을 넣어 공비 r를 정한 뒤 다른 항 구하기", axis={"첫째항": "±1~±5", "공비": "±2, ±3", "항 번호": "1~8"}, disc="두 항의 비가 r^(항 번호의 차)임을 써서 공비를 구하는가", diff=2,
        params=[{"name": "a1", "values": {"in": NZ(-5, 5)}}, {"name": "r", "values": {"in": [2, 3, -2, -3]}}, {"name": "p", "values": {"int": [1, 4]}}, {"name": "qn", "values": {"int": [2, 6]}}, {"name": "s", "values": {"int": [1, 8]}}],
        derive={"u": "a1*r**(p - 1)", "v": "a1*r**(qn - 1)", "ans": "a1*r**(s - 1)", "dn": "qn - p", "rp": "r**(qn - p)"},
        constraints=["p < qn", "(qn - p) % 2 == 1", "s != p", "s != qn", "abs(ans) < 3000", "ans not in (u, v, p, qn, s)", "abs(ans) != abs(u)", "abs(ans) != abs(v)", "abs(u) != 1"], cost=["a1", "r", "p", "qn", "s", "u", "v", "ans"], verify=["v == u*rp", "ans == u*r**(s - p)"],
        q="등비수열 {{aₙ}}에 대하여 a{sub(p)} = {u}, a{sub(qn)} = {v}일 때, a{sub(s)}의 값을 구하시오.", answer="{ans}",
        sol1="등비수열의 일반항은 aₙ = arⁿ⁻¹(a: 첫째항, r: 공비)이다. 두 항의 비 a{sub(qn)} ÷ a{sub(p)} = {v} ÷ {pn(u)} = {rp}{ika(rp)} r^({qn} − {p}) = r^{dn}이므로 r = {r}이다(공비의 부호는 항의 부호로 정한다).",
        sol2=[("a{sub(qn)} ÷ a{sub(p)} = r^{dn} → {rp} = r^{dn} → r = {r}", "공비"), ("a = a{sub(p)} ÷ r^({p} − 1) = {a1}", "첫째항"), ("a{sub(s)} = {a1} × {pn(r)}^({s} − 1) = {ans}", None, ("{ans}", "a{sub(s)}"))],
        sol3=["a{sub(s)} = a{sub(p)} × r^({s} − {p}) = {u} × {pn(r)}^{s - p} = {ans}{ro(ans)} 다른 항에서 출발해도 같다. 따라서 a{sub(s)} = {ans}이다.", "a{sub(s)} = a{sub(p)} × r^({s} − {p})", "a{sub(s)} = {ans}"],
        model="공비 r = {r}(r^{dn} = {rp}), 첫째항 a = {a1}이므로 a{sub(s)} = {a1} × {pn(r)}^({s} − 1) = {ans}이다.",
        rubric=[("공비·첫째항", 3, "r = {r}, a = {a1}{eul(a1)} 구했다.", "공비의 부호가 틀리면 1점."), ("항 구하기", 2, "a{sub(s)} = {ans}{eul(ans)} 구했다.", "지수를 n으로 두었으면 1점.")],
        pitfalls=[("두 항의 차를 공비로 봄(등차와 혼동)", "공비·첫째항", "불인정"), ("r^(n−1) 대신 rⁿ", "항 구하기", "부분"), ("음의 공비의 부호 실수", "항 구하기", "부분")])


# ── t4 등비수열의 합 ──────────────────────────────────────────
def sq_t4():
    return T(SQ, 4, SQ_B, title="등비수열의 합 — Sₙ = a(rⁿ − 1)/(r − 1)",
        skill="첫째항 a, 공비 r인 등비수열의 첫째항부터 제n항까지의 합 공식 쓰기", axis={"첫째항": "±1~±6", "공비": "2, 3, −2, ½, −½", "n": "3~8"}, disc="r ≠ 1일 때 a(rⁿ − 1)/(r − 1)을 바르게 세우고 거듭제곱을 계산하는가", diff=2,
        params=[{"name": "a1", "values": {"in": NZ(-6, 6)}}, {"name": "rk", "values": {"in": ["2", "3", "m2", "h", "mh"]}}, {"name": "n", "values": {"int": [3, 8]}}],
        table={"key": "rk", "rows": {"2": {"RS": "2", "RN": 2, "RD": 1}, "3": {"RS": "3", "RN": 3, "RD": 1}, "m2": {"RS": "-2", "RN": -2, "RD": 1}, "h": {"RS": "[[frac(1,2)]]", "RN": 1, "RD": 2}, "mh": {"RS": "[[-frac(1,2)]]", "RN": -1, "RD": 2}}},
        derive={"r": "RN/RD", "rn": "(RN/RD)**n", "ans": "a1*((RN/RD)**n - 1)/(RN/RD - 1)"},
        constraints=["ans != 0", "abs(ans) < 5000", "ans not in (a1, n, RN, RD)"], cost=["a1", "n", "rn", "ans"], verify=["ans*(r - 1) == a1*(rn - 1)"],
        q="첫째항이 {a1}, 공비가 {RS}인 등비수열의 첫째항부터 제{n}항까지의 합을 구하시오.", answer="{ans}",
        sol1="공비 r ≠ 1인 등비수열의 합은 Sₙ = [[frac(a(pow(r, n) − 1), r − 1)]] = [[frac(a(1 − pow(r, n)), 1 − r)]]이다. a = {a1}, r = {RS}, n = {n}을 넣고 r^{n} = {rn}을 계산한다.",
        sol2=[("S{sub(n)} = [[frac(a(pow(r, n) − 1), r − 1)]], a = {a1}, r = {RS}, n = {n}", "공식"), ("r^{n} = {rn}, r − 1 = {r - 1}", "거듭제곱"), ("S{sub(n)} = {a1} × ({rn} − 1) ÷ ({r - 1}) = {ans}", None, ("{ans}", "S{sub(n)}"))],
        sol3=["n이 작을 때 항을 직접 더해 보면(예: 처음 두 항 {a1} + {pn(a1*r)}) 공식의 값과 맞는다. 따라서 합은 {ans}이다.", "S{sub(n)} = a(rⁿ − 1)/(r − 1)", "S{sub(n)} = {ans}"],
        model="S{sub(n)} = {a1} × ({rn} − 1) ÷ ({r - 1}) = {ans}이다.",
        rubric=[("공식", 3, "S{sub(n)} = a(rⁿ − 1)/(r − 1)에 a = {a1}, r = {RS}, n = {n}{eul(n)} 넣었다.", "분모 r − 1을 빠뜨렸으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "거듭제곱 계산 실수면 1점.")],
        pitfalls=[("분모 r − 1을 빠뜨림", "공식", "불인정"), ("rⁿ 대신 rⁿ⁻¹", "공식", "부분"), ("음의 공비의 거듭제곱 부호 실수", "계산", "부분")])


# ── t5 ∑ 계산 ─────────────────────────────────────────────────
def _t5_rows():
    out = {}
    for n in range(4, 13):
        forms = []
        for a in (1, 2, 3, 4):
            for b in (-3, -1, 1, 2, 3, 5):
                forms.append((f"{'' if a == 1 else a}k {'+' if b > 0 else '−'} {abs(b)}", lambda k, a=a, b=b: a * k + b, f"{a} × [[frac({n}({n} + 1), 2)]] {'+' if b > 0 else '−'} {abs(b)} × {n}".replace("1 × ", "")))
        for a in (1, 2, 3):
            forms.append((f"{'' if a == 1 else a}pow(k, 2)", lambda k, a=a: a * k * k, f"{a} × [[frac({n}({n} + 1)(2 × {n} + 1), 6)]]".replace("1 × ", "")))
            forms.append((f"{'' if a == 1 else a}pow(k, 2) − k", lambda k, a=a: a * k * k - k, f"{a} × [[frac({n}({n} + 1)(2 × {n} + 1), 6)]] − [[frac({n}({n} + 1), 2)]]".replace("1 × ", "")))
        forms.append(("k(k + 1)", lambda k: k * (k + 1), f"[[frac({n}({n} + 1)(2 × {n} + 1), 6)]] + [[frac({n}({n} + 1), 2)]]"))
        forms.append(("(k + 1)(k − 1)", lambda k: k * k - 1, f"[[frac({n}({n} + 1)(2 × {n} + 1), 6)]] − {n}"))
        forms.append(("pow(2, k)", lambda k: 2 ** k, f"[[frac(2(pow(2, {n}) − 1), 2 − 1)]] (등비수열의 합)"))
        forms.append(("pow(3, k − 1)", lambda k: 3 ** (k - 1), f"[[frac(pow(3, {n}) − 1, 3 − 1)]] (등비수열의 합)"))
        forms.append(("(2k − 1)", lambda k: 2 * k - 1, f"2 × [[frac({n}({n} + 1), 2)]] − {n} = {n}²"))
        forms.append(("pow(k, 3)", lambda k: k ** 3, f"[[pow(frac({n}({n} + 1), 2), 2)]]"))
        for expr, fn, expl in forms:
            v = sum(fn(k) for k in range(1, n + 1))
            q = f"[[sum(k, 1, {n}, {expr})]]"
            if v == 0 or Fraction(v) in _nums(q):
                continue
            terms = [fn(k) for k in range(1, min(n, 3) + 1)]
            out[f"{n}_{expr}"] = {"EXPR": q, "N": n, "EXPL": expl, "V": v, "HEAD": " + ".join((f"({t})" if (i and t < 0) else str(t)) for i, t in enumerate(terms)) + " + ⋯"}
    return _pick(out, 330)


T5_ROWS = _t5_rows()


def sq_t5():
    return T(SQ, 5, SQ_B, title="합의 기호 ∑ — 자연수의 거듭제곱의 합 공식",
        skill="∑k = n(n + 1)/2, ∑k² = n(n + 1)(2n + 1)/6, ∑k³ = (n(n + 1)/2)²과 ∑의 성질로 합 계산하기", axis={"식": "ak + b, ak², k(k + 1), 2ᵏ, k³ 등", "n": "4~12"}, disc="∑를 항별로 나누고 상수는 n배임을 알며 공식을 정확히 대입하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(T5_ROWS)}}], table={"key": "f", "rows": T5_ROWS},
        derive={"ans": "V"}, cost=["N", "ans"], verify=["ans == V"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="∑는 k = 1부터 {N}까지 식의 값을 모두 더하라는 기호다({HEAD}). ∑(aₖ + bₖ) = ∑aₖ + ∑bₖ, ∑caₖ = c∑aₖ, ∑c = cn으로 나눈 뒤 자연수의 거듭제곱의 합 공식을 쓴다(등비수열은 합 공식).",
        sol2=[("{EXPR} = {HEAD}", "∑의 뜻"), ("공식 대입: {EXPL}", "항별로 나누어 공식"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["처음 몇 항을 직접 더해 보면({HEAD}) 공식의 값과 어긋나지 않는다. 따라서 값은 {ans}이다.", "{EXPL}", "답 {ans}"],
        model="{EXPR} = {EXPL} = {ans}이다.",
        rubric=[("∑ 분리·공식", 3, "{EXPL} 꼴로 세웠다.", "상수항을 n배 하지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("상수 c의 합을 c로 둠(cn이 아님)", "∑ 분리·공식", "불인정"), ("∑k²을 (∑k)²으로 계산", "∑ 분리·공식", "불인정"), ("공식의 분모 6, 2 혼동", "계산", "부분")])


# ── t6 수열의 합과 일반항 ──────────────────────────────────────
def sq_t6():
    return T(SQ, 6, SQ_B, title="수열의 합과 일반항 — aₙ = Sₙ − Sₙ₋₁",
        skill="첫째항부터 제n항까지의 합 Sₙ이 주어질 때 aₙ = Sₙ − Sₙ₋₁ (n ≥ 2), a₁ = S₁로 항 구하기", axis={"Sₙ": "An² + Bn (+ C)", "묻는 항": "a₁ ~ a₁₅"}, disc="Sₙ − Sₙ₋₁을 전개해 일반항을 얻고, a₁은 S₁로 따로 확인하는가", diff=3,
        params=[{"name": "A", "values": {"in": NZ(-3, 4)}}, {"name": "B", "values": {"in": NZ(-6, 6)}}, {"name": "C", "values": {"in": NZ(-3, 3)}}, {"name": "n", "values": {"int": [1, 15]}}],
        derive={"Sn": "A*n*n + B*n + C", "Sn1": "A*(n - 1)*(n - 1) + B*(n - 1) + C", "ans": "(A*n*n + B*n + C) - (A*(n - 1)*(n - 1) + B*(n - 1) + C)*(1 - floor(1/n))", "gen": "2*A*n - A + B"},
        constraints=["ans != 0", "ans not in (A, B, C, n)", "n == 1 or ans == gen"], cost=["A", "B", "C", "n", "Sn", "ans"], verify=["n == 1 or ans == Sn - Sn1", "n != 1 or ans == Sn"],
        q="수열 {{aₙ}}의 첫째항부터 제n항까지의 합 Sₙ이 Sₙ = {co(A)}n² {sgt(B)}n {sgn(C)}일 때, a{sub(n)}의 값을 구하시오.", answer="{ans}",
        sol1="첫째항부터 제n항까지의 합이 Sₙ이면 aₙ = Sₙ − Sₙ₋₁ (n ≥ 2)이고 a₁ = S₁이다. Sₙ − Sₙ₋₁을 전개하면 n ≥ 2에서 aₙ = {co(2*A)}n {sgn(B - A)}이다. n = 1이면 이 식이 아니라 S₁을 써야 하는데, 상수항 C = {C}이므로 a₁ = S₁ = {A + B + C}이다.",
        sol2=[("aₙ = Sₙ − Sₙ₋₁ (n ≥ 2) = {co(2*A)}n {sgn(B - A)}", "차로 일반항"), ("a₁ = S₁ = {A + B + C} (C ≠ 0이면 일반항과 다름)", "첫째항 확인"), ("a{sub(n)} = {ans}", None, ("{ans}", "a{sub(n)}"))],
        sol3=["S{sub(n)} = {Sn}, S{sub(n - 1)} = {Sn1}이므로 차 {Sn} − {pn(Sn1)}{eul(Sn1)} 계산하면 (n ≥ 2에서) {Sn - Sn1}{ro(Sn - Sn1)} 확인된다. 따라서 a{sub(n)} = {ans}이다.", "S{sub(n)} − S{sub(n - 1)}", "a{sub(n)} = {ans}"],
        model="aₙ = Sₙ − Sₙ₋₁ = {co(2*A)}n {sgn(B - A)} (n ≥ 2), a₁ = S₁ = {A + B + C}이므로 a{sub(n)} = {ans}이다.",
        rubric=[("일반항", 3, "aₙ = Sₙ − Sₙ₋₁ (n ≥ 2)를 계산해 {co(2*A)}n {sgn(B - A)}{eul(B - A)} 얻었다.", "n ≥ 2 조건 없이 a₁에도 적용했으면 1점."), ("답", 2, "a{sub(n)} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("a₁도 Sₙ − Sₙ₋₁ 식으로 구함(C ≠ 0)", "답", "불인정"), ("Sₙ₋₁ 전개 실수", "일반항", "부분"), ("aₙ = Sₙ으로 착각", "일반항", "불인정")])


# ── t7 여러 가지 수열의 합 ──────────────────────────────────────
def _t7_rows():
    out = {}
    for n in range(3, 25):
        kinds = [("frac(1, k(k + 1))", lambda k: Fraction(1, k * (k + 1)), "[[frac(1, k(k + 1))]] = [[frac(1, k)]] − [[frac(1, k + 1)]]", f"1 − [[frac(1, {n + 1})]]"),
                 ("frac(1, (2k − 1)(2k + 1))", lambda k: Fraction(1, (2 * k - 1) * (2 * k + 1)), "[[frac(1, (2k − 1)(2k + 1))]] = [[frac(1,2)]]([[frac(1, 2k − 1)]] − [[frac(1, 2k + 1)]])", f"[[frac(1,2)]](1 − [[frac(1, {2 * n + 1})]])"),
                 ("frac(2, k(k + 1))", lambda k: Fraction(2, k * (k + 1)), "[[frac(2, k(k + 1))]] = 2([[frac(1, k)]] − [[frac(1, k + 1)]])", f"2(1 − [[frac(1, {n + 1})]])"),
                 ("frac(1, k(k + 2))", lambda k: Fraction(1, k * (k + 2)), "[[frac(1, k(k + 2))]] = [[frac(1,2)]]([[frac(1, k)]] − [[frac(1, k + 2)]])", f"[[frac(1,2)]](1 + [[frac(1,2)]] − [[frac(1, {n + 1})]] − [[frac(1, {n + 2})]])"),
                 ("frac(1, (k + 1)(k + 2))", lambda k: Fraction(1, (k + 1) * (k + 2)), "[[frac(1, (k + 1)(k + 2))]] = [[frac(1, k + 1)]] − [[frac(1, k + 2)]]", f"[[frac(1,2)]] − [[frac(1, {n + 2})]]")]
        for expr, fn, expl, tel in kinds:
            v = sum(fn(k) for k in range(1, n + 1))
            q = f"[[sum(k, 1, {n}, {expr})]]"
            if v in _nums(q):
                continue
            out[f"{n}_{expr}"] = {"EXPR": q, "N": n, "EXPL": expl, "TEL": tel, "VN": v.numerator, "VD": v.denominator, "KIND": "부분분수"}
        m = n + 1
        r = int(m ** 0.5)
        if r * r == m:
            v = Fraction(r - 1)
            q = f"[[sum(k, 1, {n}, frac(1, sqrt(k + 1) + sqrt(k)))]]"
            if v not in _nums(q) and v != 0:
                out[f"{n}_root"] = {"EXPR": q, "N": n, "EXPL": "분모를 유리화: [[frac(1, sqrt(k + 1) + sqrt(k))]] = [[sqrt(k + 1)]] − [[sqrt(k)]]", "TEL": f"[[sqrt({n + 1})]] − 1 = {r} − 1", "VN": r - 1, "VD": 1, "KIND": "유리화"}
    return _pick(out, 300)


T7_ROWS = _t7_rows()


def sq_t7():
    return T(SQ, 7, SQ_B, title="여러 가지 수열의 합 — 부분분수·유리화",
        skill="1/(k(k + 1)) = 1/k − 1/(k + 1)처럼 항을 두 조각의 차로 나눠 소거하고 남는 항만 더하기", axis={"식": "1/(k(k+1)), 1/((2k−1)(2k+1)), 1/(k(k+2)), 유리화", "n": "3~24"}, disc="부분분수로 나눈 뒤 소거되고 남는 항을 정확히 찾는가", diff=3,
        params=[{"name": "f", "values": {"in": list(T7_ROWS)}}], table={"key": "f", "rows": T7_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="분모가 두 일차식의 곱이면 부분분수 [[frac(1, A B)]] = [[frac(1, B − A)]]([[frac(1, A)]] − [[frac(1, B)]])로 나눈다. 나눈 뒤 이웃한 항끼리 소거되어 처음과 끝의 몇 항만 남는다({KIND}).",
        sol2=[("{EXPL}", "{KIND}"), ("소거 후 남는 항: {TEL}", "망원급수"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["n이 작을 때(예: n = 1, 2) 직접 더한 값이 같은 공식으로 나오는지 확인한다. 따라서 값은 {ans}이다.", "{TEL}", "답 {ans}"],
        model="{EXPL}이므로 합은 {TEL} = {ans}이다.",
        rubric=[("부분분수", 3, "{EXPL} 꼴로 나눴다.", "계수(½ 등)를 빠뜨렸으면 1점."), ("소거·답", 2, "{ans}{eul(ans)} 구했다.", "남는 항을 잘못 골랐으면 1점.")],
        pitfalls=[("부분분수의 계수 ½을 빠뜨림", "부분분수", "부분"), ("소거 후 남는 항을 잘못 셈", "소거·답", "불인정"), ("유리화 부호 실수", "부분분수", "부분")])


# ── t8 귀납적 정의 ─────────────────────────────────────────────
def _t8_rows():
    out = {}
    recs = []
    for a1 in range(-3, 6):
        for d in (2, 3, -2, 5):
            recs.append((f"a₁ = {a1}, aₙ₊₁ = aₙ {'+' if d > 0 else '−'} {abs(d)}", lambda a, n, d=d: a + d, a1, "등차(공차 %d)" % d, "aₙ₊₁ − aₙ = 일정 → 등차수열"))
        for r in (2, 3, -2):
            recs.append((f"a₁ = {a1}, aₙ₊₁ = {r}aₙ", lambda a, n, r=r: r * a, a1, "등비(공비 %d)" % r, "aₙ₊₁ ÷ aₙ = 일정 → 등비수열"))
        for c in (1, 2, -1):
            recs.append((f"a₁ = {a1}, aₙ₊₁ = aₙ + {2 * c}n".replace("+ -2n", "− 2n"), lambda a, n, c=c: a + 2 * c * n, a1, "계차가 2cn", "aₙ₊₁ − aₙ = 2cn → 계차수열"))
        for p, q_ in ((2, -1), (2, 1), (3, -2), (2, -3), (3, 1)):
            recs.append((f"a₁ = {a1}, aₙ₊₁ = {p}aₙ {'+' if q_ > 0 else '−'} {abs(q_)}", lambda a, n, p=p, q_=q_: p * a + q_, a1, "aₙ₊₁ = paₙ + q", "차례로 대입"))
        recs.append((f"a₁ = {a1}, aₙ₊₁ = aₙ + n²", lambda a, n: a + n * n, a1, "계차 n²", "aₙ₊₁ − aₙ = n²"))
        recs.append((f"a₁ = {a1}, aₙ₊₁ = aₙ + 2ⁿ", lambda a, n: a + 2 ** n, a1, "계차 2ⁿ", "aₙ₊₁ − aₙ = 2ⁿ"))
    for desc, fn, a1, kind, law in recs:
        for m in (4, 5, 6, 7, 8):
            seq = [a1]
            for n in range(1, m):
                seq.append(fn(seq[-1], n))
            v = seq[-1]
            q = f"수열 {{aₙ}}이 {desc} (n = 1, 2, 3, ⋯)로 정의될 때, a{_sub(m)}의 값을 구하시오."
            if v == 0 or abs(v) > 3000 or Fraction(v) in _nums(q):
                continue
            out[f"{desc}_{m}"] = {"DESC": desc, "M": m, "V": v, "SEQ": ", ".join(f"a{_sub(i + 1)} = {x}" for i, x in enumerate(seq)), "KIND": kind, "LAW": law}
    for a1 in range(1, 4):
        for a2 in range(1, 5):
            desc = f"a₁ = {a1}, a₂ = {a2}, aₙ₊₂ = aₙ₊₁ + aₙ"
            for m in (5, 6, 7, 8):
                seq = [a1, a2]
                while len(seq) < m:
                    seq.append(seq[-1] + seq[-2])
                v = seq[-1]
                q = f"수열 {{aₙ}}이 {desc} (n = 1, 2, 3, ⋯)로 정의될 때, a{_sub(m)}의 값을 구하시오."
                if Fraction(v) in _nums(q):
                    continue
                out[f"{desc}_{m}"] = {"DESC": desc, "M": m, "V": v, "SEQ": ", ".join(f"a{_sub(i + 1)} = {x}" for i, x in enumerate(seq)), "KIND": "앞의 두 항의 합", "LAW": "aₙ₊₂ = aₙ₊₁ + aₙ 에 차례로 대입"}
    return _pick(out, 330)


T8_ROWS = _t8_rows()


def sq_t8():
    return T(SQ, 8, SQ_B, title="수열의 귀납적 정의 — 항을 차례로 구하기",
        skill="첫째항과 이웃한 항 사이의 관계식으로 정의된 수열의 항을 차례로 구하기", axis={"관계식": "등차·등비·계차(2cn, n², 2ⁿ)·paₙ + q·피보나치형", "묻는 항": "a₄ ~ a₈"}, disc="관계식의 n에 1, 2, 3, ⋯을 차례로 넣어 항을 만들고 등차·등비 구조를 알아보는가", diff=2,
        params=[{"name": "f", "values": {"in": list(T8_ROWS)}}], table={"key": "f", "rows": T8_ROWS},
        derive={"ans": "V"}, cost=["M", "ans"], verify=["ans == V"],
        q="수열 {{aₙ}}이 {DESC} (n = 1, 2, 3, ⋯)로 정의될 때, a{sub(M)}의 값을 구하시오.", answer="{ans}",
        sol1="귀납적 정의는 첫째항과 '앞의 항으로 다음 항을 만드는 규칙'으로 수열을 정하는 것이다. n = 1, 2, 3, ⋯을 차례로 넣어 항을 구한다. 이 수열은 {KIND} 꼴이다({LAW}).",
        sol2=[("{LAW}", "규칙 읽기"), ("{SEQ}", "차례로 대입"), ("a{sub(M)} = {ans}", None, ("{ans}", "a{sub(M)}"))],
        sol3=["구한 항들이 관계식을 만족하는지 한 쌍을 골라 확인한다(예: 두 번째 항과 세 번째 항). 따라서 a{sub(M)} = {ans}이다.", "{SEQ}", "a{sub(M)} = {ans}"],
        model="{LAW}. 차례로 구하면 {SEQ}이므로 a{sub(M)} = {ans}이다.",
        rubric=[("항 구하기", 3, "{SEQ}{ro(ans)} 차례로 구했다.", "한 항의 계산 실수면 1점."), ("답", 2, "a{sub(M)} = {ans}{eul(ans)} 구했다.", "항 번호를 잘못 세었으면 1점.")],
        pitfalls=[("n에 넣는 값을 하나 건너뜀", "항 구하기", "부분"), ("aₙ₊₁의 n을 항의 값으로 착각", "항 구하기", "불인정"), ("항 번호 착오(a₅를 a₆으로)", "답", "부분")])


SQ_SEED = SEED(SQ, category="대수", title="수열 — 등차·등비의 항과 합·∑ 계산·합과 일반항·여러 가지 수열의 합·귀납적 정의", unit_id="h2-1", concept_ids=["h2-1-12", "h2-1-13", "h2-1-14", "h2-1-15", "h2-1-16"],
               schema_name="수열", note="수학적 귀납법(17)은 수치 답 틀이 없어 보류. 항 번호는 sub() 첨자, 수열 표기는 {{aₙ}} 이스케이프.",
               templates=[sq_t1(), sq_t2(), sq_t3(), sq_t4(), sq_t5(), sq_t6(), sq_t7(), sq_t8()])


if __name__ == "__main__":
    run(SQ_SEED)
