# itemfactory/tools/mkseed_h_extra.py — 보류했던 유형 3개: 수학적 귀납법·역/대우/귀류법·산점도 (v1.0 · 2026-09-15 세션 5c)
#
#   python itemfactory/tools/mkseed_h_extra.py
#     → seeds/h2-1-induct.json  (h2-1-17 수학적 귀납법 — 빈칸 (가)(나)를 f(k), g(k)로 두고 값을 묻는다, 3틀)
#     → seeds/h1-2-logic2.json  (h1-2-12 역·이·대우 / h1-2-14 귀류법 — 보기 A~E 글자 답, 3틀)
#     → seeds/m3-2-scatter.json (m3-2-14 산점도·상관관계 — scatter 도형 + 자료 나열, 글자 답·개수 답, 3틀)
#   답이 진술·증명인 유형은 "보기 글자(A~E)" 또는 "빈칸 식의 값"으로 바꿔 파이프라인이 검산할 수 있게 한 것 (HANDOFF §3 ①·④).
from __future__ import annotations

import math
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260923)


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


def _row(q, v, **kw):
    f = Fraction(v)
    shown = _nums(q) | _nums(kw.get("Q", ""))
    if f == 0 or f in shown or abs(f) in shown:
        return None
    d = {"VN": f.numerator, "VD": f.denominator}
    d.update(kw)
    return d


# ═══════════════════════════════════════════════════════════════════ 1. 수학적 귀납법 (h2-1-17)
IN = "h2-1-induct"
IN_B = {**HS, "prereq": ["수열의 합", "지수법칙"], "ops": ["수학적 귀납법"], "traps": ["n = k + 1일 때 더해지는 항", "가정한 식을 그대로 대입"], "tags": ["수학적 귀납법", "증명"]}

# (등식 표기, 좌변 n = 1, 우변 n = 1, n = k 가정식, n = k + 1 좌변, k 우변 마커, (가) f(k) 표기, (나) g(k) 표기, f, g)
EQS = [
    ("1 + 2 + 3 + ⋯ + n = [[frac(n(n + 1), 2)]]", "1", "[[frac(1 × 2, 2)]] = 1", "1 + 2 + ⋯ + k = [[frac(k(k + 1), 2)]]", "1 + 2 + ⋯ + k + (k + 1)", "[[frac(k(k + 1), 2)]]",
     "k + 1", "[[frac((k + 1)(k + 2), 2)]]", lambda k: Fraction(k + 1), lambda k: Fraction((k + 1) * (k + 2), 2)),
    ("1² + 2² + 3² + ⋯ + n² = [[frac(n(n + 1)(2n + 1), 6)]]", "1", "[[frac(1 × 2 × 3, 6)]] = 1", "1² + 2² + ⋯ + k² = [[frac(k(k + 1)(2k + 1), 6)]]", "1² + 2² + ⋯ + k² + (k + 1)²", "[[frac(k(k + 1)(2k + 1), 6)]]",
     "[[pow(k + 1, 2)]]", "[[frac((k + 1)(k + 2)(2k + 3), 6)]]", lambda k: Fraction((k + 1) ** 2), lambda k: Fraction((k + 1) * (k + 2) * (2 * k + 3), 6)),
    ("1 + 3 + 5 + ⋯ + (2n − 1) = n²", "1", "1² = 1", "1 + 3 + ⋯ + (2k − 1) = k²", "1 + 3 + ⋯ + (2k − 1) + (2k + 1)", "k²",
     "2k + 1", "[[pow(k + 1, 2)]]", lambda k: Fraction(2 * k + 1), lambda k: Fraction((k + 1) ** 2)),
    ("1 + 2 + 2² + ⋯ + 2ⁿ⁻¹ = 2ⁿ − 1", "1", "2 − 1 = 1", "1 + 2 + ⋯ + 2ᵏ⁻¹ = 2ᵏ − 1", "1 + 2 + ⋯ + 2ᵏ⁻¹ + 2ᵏ", "2ᵏ − 1",
     "[[pow(2, k)]]", "[[pow(2, k + 1)]] − 1", lambda k: Fraction(2 ** k), lambda k: Fraction(2 ** (k + 1) - 1)),
    ("1·2 + 2·3 + 3·4 + ⋯ + n(n + 1) = [[frac(n(n + 1)(n + 2), 3)]]", "1·2 = 2", "[[frac(1 × 2 × 3, 3)]] = 2", "1·2 + 2·3 + ⋯ + k(k + 1) = [[frac(k(k + 1)(k + 2), 3)]]", "1·2 + ⋯ + k(k + 1) + (k + 1)(k + 2)", "[[frac(k(k + 1)(k + 2), 3)]]",
     "(k + 1)(k + 2)", "[[frac((k + 1)(k + 2)(k + 3), 3)]]", lambda k: Fraction((k + 1) * (k + 2)), lambda k: Fraction((k + 1) * (k + 2) * (k + 3), 3)),
    ("[[frac(1, 1 × 2)]] + [[frac(1, 2 × 3)]] + ⋯ + [[frac(1, n(n + 1))]] = [[frac(n, n + 1)]]", "[[frac(1, 2)]]", "[[frac(1, 2)]]", "[[frac(1, 1 × 2)]] + ⋯ + [[frac(1, k(k + 1))]] = [[frac(k, k + 1)]]", "[[frac(1, 1 × 2)]] + ⋯ + [[frac(1, k(k + 1))]] + [[frac(1, (k + 1)(k + 2))]]", "[[frac(k, k + 1)]]",
     "[[frac(1, (k + 1)(k + 2))]]", "[[frac(k + 1, k + 2)]]", lambda k: Fraction(1, (k + 1) * (k + 2)), lambda k: Fraction(k + 1, k + 2)),
    ("1³ + 2³ + 3³ + ⋯ + n³ = [[pow(frac(n(n + 1), 2), 2)]]", "1", "[[pow(frac(1 × 2, 2), 2)]] = 1", "1³ + 2³ + ⋯ + k³ = [[pow(frac(k(k + 1), 2), 2)]]", "1³ + 2³ + ⋯ + k³ + (k + 1)³", "[[pow(frac(k(k + 1), 2), 2)]]",
     "[[pow(k + 1, 3)]]", "[[pow(frac((k + 1)(k + 2), 2), 2)]]", lambda k: Fraction((k + 1) ** 3), lambda k: Fraction((k + 1) * (k + 2), 2) ** 2),
    ("2 + 4 + 6 + ⋯ + 2n = n(n + 1)", "2", "1 × 2 = 2", "2 + 4 + ⋯ + 2k = k(k + 1)", "2 + 4 + ⋯ + 2k + 2(k + 1)", "k(k + 1)",
     "2k + 2", "(k + 1)(k + 2)", lambda k: Fraction(2 * k + 2), lambda k: Fraction((k + 1) * (k + 2))),
    ("1 + 4 + 7 + ⋯ + (3n − 2) = [[frac(n(3n − 1), 2)]]", "1", "[[frac(1 × 2, 2)]] = 1", "1 + 4 + ⋯ + (3k − 2) = [[frac(k(3k − 1), 2)]]", "1 + 4 + ⋯ + (3k − 2) + (3k + 1)", "[[frac(k(3k − 1), 2)]]",
     "3k + 1", "[[frac((k + 1)(3k + 2), 2)]]", lambda k: Fraction(3 * k + 1), lambda k: Fraction((k + 1) * (3 * k + 2), 2)),
]


def _proof(eq, L1, R1, ASSUME, LHS1, RK):
    return (f"다음은 모든 자연수 n에 대하여 등식 {eq} 이 성립함을 수학적 귀납법으로 증명한 것이다. "
            f"(ⅰ) n = 1일 때, (좌변) = {L1}, (우변) = {R1}이므로 등식이 성립한다. "
            f"(ⅱ) n = k일 때 등식이 성립한다고 가정하면 {ASSUME} 이다. 이 식의 양변에 (가) 를 더하면 {LHS1} = {RK} + (가) = (나) 이므로 n = k + 1일 때도 등식이 성립한다. "
            f"따라서 모든 자연수 n에 대하여 주어진 등식이 성립한다.")


def _in1_rows():
    out = {}
    for i, (eq, L1, R1, ASSUME, LHS1, RK, FK, GK, f, g) in enumerate(EQS):
        pf = _proof(eq, L1, R1, ASSUME, LHS1, RK)
        for a in range(1, 7):
            for b in range(1, 7):
                fa, gb = f(a), g(b)
                for kind, v, ask, step in (("s", fa + gb, f"f({a}) + g({b})", f"f({a}) + g({b}) = {_fm(fa)} + {_fm(gb)}"), ("p", fa * gb, f"f({a}) × g({b})", f"f({a}) × g({b}) = {_fm(fa)} × {_fm(gb)}")):
                    q = f"귀납법 {i} {a} {b} {kind}"
                    r = _row(q, v, Q=f"{pf} 위의 증명에서 (가), (나)에 알맞은 식을 각각 f(k), g(k)라 할 때, {ask}의 값을 구하시오.", FK=FK, GK=GK, FA=_fm(fa), GB=_fm(gb), STEP=step, ASK=ask, EQ=eq, A=a, B=b)
                    if r: out[f"{i}_{a}_{b}_{kind}"] = r
    return _pick(out, 330)


IN1_ROWS = _in1_rows()


def in_t1():
    return T(IN, 1, IN_B, title="수학적 귀납법 — 등식의 증명에서 빈칸 (가), (나)",
        skill="n = k일 때의 가정에 n = k + 1번째 항을 더해 n = k + 1일 때의 식을 만드는 과정에서 빈칸의 식을 읽어 값을 구하기", axis={"등식": "자연수 합·제곱합·홀수 합·등비 합·부분분수 등 9가지", "묻는 것": "f(a) + g(b) / f(a) × g(b)"}, disc="더해지는 항(가)과 정리된 결과(나)를 구분해 읽는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IN1_ROWS)}}], table={"key": "f", "rows": IN1_ROWS},
        derive={"ans": "VN/VD"}, cost=["A", "B", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="수학적 귀납법의 (ⅱ)단계는 n = k일 때의 식에 n = k + 1번째 항을 더해 n = k + 1일 때의 우변 꼴로 정리하는 것이다. 더해지는 항이 (가), 정리한 결과가 (나)이다.",
        sol2=[("(가) = f(k) = {FK}, (나) = g(k) = {GK}", "빈칸 읽기"), ("f({A}) = {FA}, g({B}) = {GB}", "대입"), ("{STEP} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["(나)에 k = 1을 넣으면 n = 2일 때의 우변이 되는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP} = {ans}", "답 {ans}"],
        model="(가)는 더해지는 항 {FK}, (나)는 정리한 결과 {GK}이므로 f({A}) = {FA}, g({B}) = {GB}이고 {STEP} = {ans}이다.",
        rubric=[("빈칸 읽기", 3, "(가) = {FK}, (나) = {GK}로 읽었다.", "(가)만 맞으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("(가)에 k번째 항을 씀", "빈칸 읽기", "불인정"), ("(나)를 n = k의 우변 그대로 둠", "빈칸 읽기", "불인정"), ("f, g에 대입할 때 k 자리에 다른 수를 넣음", "값 구하기", "부분")])


# 배수 증명: (명제, n = 1 확인, 가정, k + 1 전개, (가), f)
MULT = [
    ("n³ + 2n은 3의 배수이다", "1³ + 2 × 1 = 3", "k³ + 2k = 3m (m은 자연수)", "(k + 1)³ + 2(k + 1) = (k³ + 2k) + (가) = 3m + (가)", "3(k² + k + 1)", lambda k: Fraction(3 * (k * k + k + 1))),
    ("n³ − n은 6의 배수이다", "1³ − 1 = 0", "k³ − k = 6m (m은 0 또는 자연수)", "(k + 1)³ − (k + 1) = (k³ − k) + (가) = 6m + (가)", "3k(k + 1)", lambda k: Fraction(3 * k * (k + 1))),
    ("4ⁿ − 1은 3의 배수이다", "4 − 1 = 3", "4ᵏ − 1 = 3m (m은 자연수)", "4ᵏ⁺¹ − 1 = 4(4ᵏ − 1) + (가) = 4 × 3m + (가)", "3", lambda k: Fraction(3)),
    ("5ⁿ − 1은 4의 배수이다", "5 − 1 = 4", "5ᵏ − 1 = 4m (m은 자연수)", "5ᵏ⁺¹ − 1 = 5(5ᵏ − 1) + (가) = 5 × 4m + (가)", "4", lambda k: Fraction(4)),
    ("n(n + 1)(n + 2)는 6의 배수이다", "1 × 2 × 3 = 6", "k(k + 1)(k + 2) = 6m (m은 자연수)", "(k + 1)(k + 2)(k + 3) = k(k + 1)(k + 2) + (가) = 6m + (가)", "3(k + 1)(k + 2)", lambda k: Fraction(3 * (k + 1) * (k + 2))),
    ("7ⁿ − 1은 6의 배수이다", "7 − 1 = 6", "7ᵏ − 1 = 6m (m은 자연수)", "7ᵏ⁺¹ − 1 = 7(7ᵏ − 1) + (가) = 7 × 6m + (가)", "6", lambda k: Fraction(6)),
    ("n² + n은 2의 배수이다", "1² + 1 = 2", "k² + k = 2m (m은 자연수)", "(k + 1)² + (k + 1) = (k² + k) + (가) = 2m + (가)", "2(k + 1)", lambda k: Fraction(2 * (k + 1))),
    ("2ⁿ⁺¹ + 3ⁿ⁻¹ 은 5의 배수이다", "2² + 3⁰ = 5", "2ᵏ⁺¹ + 3ᵏ⁻¹ = 5m (m은 자연수)", "2ᵏ⁺² + 3ᵏ = 2(2ᵏ⁺¹ + 3ᵏ⁻¹) + (가) = 2 × 5m + (가)", "3ᵏ⁻¹", lambda k: Fraction(3 ** (k - 1))),
]


def _in2_rows():
    out = {}
    for i, (prop, base, assume, expand, FK, f) in enumerate(MULT):
        pf = (f"다음은 모든 자연수 n에 대하여 명제 '{prop}'가 성립함을 수학적 귀납법으로 증명한 것이다. "
              f"(ⅰ) n = 1일 때, {base}이므로 성립한다. "
              f"(ⅱ) n = k일 때 성립한다고 가정하면 {assume}이다. 이때 {expand} 이고 (가) 도 같은 수의 배수이므로 n = k + 1일 때도 성립한다. "
              f"따라서 모든 자연수 n에 대하여 주어진 명제가 성립한다.")
        for a in range(1, 8):
            v = f(a)
            q = f"배수 귀납법 {i} {a}"
            r = _row(q, v, Q=f"{pf} 위의 증명에서 (가)에 알맞은 식을 f(k)라 할 때, f({a})의 값을 구하시오.", FK=FK, STEP=f"f({a}) = {_fm(v)}", A=a, PROP=prop)
            if r: out[f"{i}_{a}"] = r
            for b in range(a + 1, 8):
                v2 = f(a) + f(b)
                r2 = _row(f"{q} {b}", v2, Q=f"{pf} 위의 증명에서 (가)에 알맞은 식을 f(k)라 할 때, f({a}) + f({b})의 값을 구하시오.", FK=FK, STEP=f"f({a}) + f({b}) = {_fm(f(a))} + {_fm(f(b))}", A=a, PROP=prop)
                if r2: out[f"{i}_{a}_{b}"] = r2
    return _pick(out, 330)


IN2_ROWS = _in2_rows()


def in_t2():
    return T(IN, 2, IN_B, title="수학적 귀납법 — 배수 명제의 증명에서 빈칸 (가)",
        skill="n = k + 1일 때의 식을 n = k일 때의 식과 나머지 항으로 쪼개어, 더해진 항이 배수임을 보이는 과정에서 빈칸 읽기", axis={"명제": "n³ + 2n·n³ − n·4ⁿ − 1·5ⁿ − 1·n(n+1)(n+2)·7ⁿ − 1·n² + n·2ⁿ⁺¹ + 3ⁿ⁻¹", "묻는 것": "f(a) / f(a) + f(b)"}, disc="k + 1의 식에서 k의 식을 빼 나머지를 정확히 정리하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IN2_ROWS)}}], table={"key": "f", "rows": IN2_ROWS},
        derive={"ans": "VN/VD"}, cost=["A", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="배수 명제의 귀납법 (ⅱ)단계: n = k + 1일 때의 식을 (n = k일 때의 식) + (나머지)로 쪼개고, 나머지도 같은 수의 배수임을 보인다. 그 나머지가 (가)이다.",
        sol2=[("(가) = f(k) = {FK}", "빈칸 읽기"), ("{STEP}", "대입"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["(가)에 k = 1을 넣어 n = 2일 때의 값과 n = 1일 때의 값의 차와 같은지 확인한다. 따라서 값은 {ans}이다.", "{STEP} = {ans}", "답 {ans}"],
        model="(가)는 n = k + 1의 식에서 n = k의 식을 뺀 나머지 {FK}이므로 {STEP} = {ans}이다.",
        rubric=[("빈칸 읽기", 3, "(가) = {FK}로 읽었다.", "부호·계수가 틀렸으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("(가)를 n = k + 1 전체 식으로 둠", "빈칸 읽기", "불인정"), ("전개할 때 항을 빠뜨림", "빈칸 읽기", "부분"), ("거듭제곱 계산 실수", "값 구하기", "부분")])


# 부등식 증명: (부등식, 시작 n0, n = n0 확인, 가정, 전개 문장, (가), f)
INEQ = [
    ("2ⁿ > 2n + 1", 3, "2³ = 8 > 7 = 2 × 3 + 1", "2ᵏ > 2k + 1", "양변에 2를 곱하면 2ᵏ⁺¹ > 4k + 2 = {2(k + 1) + 1} + (가) 이고 k ≥ 3에서 (가) > 0이므로 2ᵏ⁺¹ > 2(k + 1) + 1", "2k − 1", lambda k: Fraction(2 * k - 1)),
    ("3ⁿ > 2n + 1", 2, "3² = 9 > 5 = 2 × 2 + 1", "3ᵏ > 2k + 1", "양변에 3을 곱하면 3ᵏ⁺¹ > 6k + 3 = {2(k + 1) + 1} + (가) 이고 (가) > 0이므로 3ᵏ⁺¹ > 2(k + 1) + 1", "4k", lambda k: Fraction(4 * k)),
    ("2ⁿ > n²", 5, "2⁵ = 32 > 25 = 5²", "2ᵏ > k²", "양변에 2를 곱하면 2ᵏ⁺¹ > 2k² = (k + 1)² + (가) 이고 k ≥ 5에서 (가) > 0이므로 2ᵏ⁺¹ > (k + 1)²", "k² − 2k − 1", lambda k: Fraction(k * k - 2 * k - 1)),
    ("n! > 2ⁿ", 4, "4! = 24 > 16 = 2⁴", "k! > 2ᵏ", "양변에 k + 1을 곱하면 (k + 1)! > (k + 1) × 2ᵏ = 2ᵏ⁺¹ + (가) 이고 (가) > 0이므로 (k + 1)! > 2ᵏ⁺¹", "(k − 1) × 2ᵏ", lambda k: Fraction((k - 1) * 2 ** k)),
    ("4ⁿ > 3n + 1", 1, "4 > 4 = 3 × 1 + 1 은 성립하지 않으므로 n = 2부터: 4² = 16 > 7", "4ᵏ > 3k + 1", "양변에 4를 곱하면 4ᵏ⁺¹ > 12k + 4 = {3(k + 1) + 1} + (가) 이고 (가) > 0이므로 4ᵏ⁺¹ > 3(k + 1) + 1", "9k", lambda k: Fraction(9 * k)),
]


def _in3_rows():
    out = {}
    for i, (ineq, n0, base, assume, expand, FK, f) in enumerate(INEQ):
        if i == 4:
            continue                       # n = 1 에서 성립하지 않는 예는 문면이 복잡 — 제외
        pf = (f"다음은 n ≥ {n0}인 모든 자연수 n에 대하여 부등식 {ineq} 이 성립함을 수학적 귀납법으로 증명한 것이다. "
              f"(ⅰ) n = {n0}일 때, {base}이므로 성립한다. "
              f"(ⅱ) n = k (k ≥ {n0})일 때 성립한다고 가정하면 {assume} 이다. {expand}. 즉 n = k + 1일 때도 성립한다. "
              f"따라서 n ≥ {n0}인 모든 자연수 n에 대하여 주어진 부등식이 성립한다.")
        pf = pf.replace("{", "").replace("}", "")
        for a in range(n0, n0 + 6):
            v = f(a)
            q = f"부등식 귀납법 {i} {a}"
            r = _row(q, v, Q=f"{pf} 위의 증명에서 (가)에 알맞은 식을 f(k)라 할 때, f({a})의 값을 구하시오.", FK=FK, STEP=f"f({a}) = {_fm(v)}", A=a, INEQ=ineq)
            if r: out[f"{i}_{a}"] = r
            for b in range(a + 1, n0 + 6):
                v2 = f(a) + f(b)
                r2 = _row(f"{q} {b}", v2, Q=f"{pf} 위의 증명에서 (가)에 알맞은 식을 f(k)라 할 때, f({a}) + f({b})의 값을 구하시오.", FK=FK, STEP=f"f({a}) + f({b}) = {_fm(f(a))} + {_fm(f(b))}", A=a, INEQ=ineq)
                if r2: out[f"{i}_{a}_{b}"] = r2
    return out


IN3_ROWS = _in3_rows()


def in_t3():
    return T(IN, 3, IN_B, title="수학적 귀납법 — 부등식의 증명에서 빈칸 (가)",
        skill="가정한 부등식의 양변에 같은 수를 곱해 n = k + 1일 때의 우변과의 차 (가)가 양수임을 보이는 과정에서 빈칸 읽기", axis={"부등식": "2ⁿ > 2n + 1 · 3ⁿ > 2n + 1 · 2ⁿ > n² · n! > 2ⁿ", "묻는 것": "f(a) / f(a) + f(b)"}, disc="(k + 1)번째 우변과의 차를 정확히 정리해 부호를 확인하는가", diff=4,
        params=[{"name": "f", "values": {"in": list(IN3_ROWS)}}], table={"key": "f", "rows": IN3_ROWS},
        derive={"ans": "VN/VD"}, cost=["A", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="부등식의 귀납법 (ⅱ)단계: 가정한 부등식의 양변에 같은 수를 곱한 뒤, 얻은 우변을 (n = k + 1일 때의 우변) + (가)로 쪼개어 (가) > 0임을 보인다.",
        sol2=[("(가) = f(k) = {FK}", "빈칸 읽기"), ("{STEP}", "대입"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["(가)에 k의 시작값을 넣어 양수인지 확인한다. 따라서 값은 {ans}이다.", "{STEP} = {ans}", "답 {ans}"],
        model="(가)는 곱한 뒤의 우변에서 n = k + 1일 때의 우변을 뺀 {FK}이므로 {STEP} = {ans}이다.",
        rubric=[("빈칸 읽기", 3, "(가) = {FK}로 읽었다.", "부호가 반대면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("(가)를 n = k + 1의 우변 전체로 둠", "빈칸 읽기", "불인정"), ("양변에 곱한 수를 잘못 잡음", "빈칸 읽기", "부분"), ("거듭제곱·계승 계산 실수", "값 구하기", "부분")])


IN_SEED = SEED(IN, category="대수", title="수학적 귀납법 — 등식·배수·부등식 증명의 빈칸 (가), (나)", unit_id="h2-1", concept_ids=["h2-1-17"],
               schema_name="수학적 귀납법", note="증명 자체는 검산할 수 없으므로 증명 골격을 문면에 주고 빈칸의 식 f(k), g(k)의 값을 묻는다(수능형). 값은 파이썬 람다로 계산해 행에 굽는다.",
               templates=[in_t1(), in_t2(), in_t3()])


# ═══════════════════════════════════════════════════════════════════ 2. 명제의 역·이·대우 / 귀류법 (h1-2-12·14)
LG = "h1-2-logic2"
LG_B = {**HS, "prereq": ["명제와 조건", "부정"], "ops": ["명제"], "traps": ["역과 이 혼동", "'그리고'의 부정은 '또는'"], "tags": ["역", "대우", "귀류법"]}

_NEG_REL = {">": "≤", "<": "≥", "≥": "<", "≤": ">", "=": "≠", "≠": "="}


def neg(s):
    """조건의 부정 — recheck.py 의 _lneg 와 같은 규칙."""
    m = re.fullmatch(r"(.+?) ([<>≤≥=≠]) (.+)", s)
    if m: return f"{m.group(1)} {_NEG_REL[m.group(2)]} {m.group(3)}"
    if s.endswith("짝수"): return s[:-2] + "홀수"
    if s.endswith("홀수"): return s[:-2] + "짝수"
    if s.endswith(" 아니"): return s[:-4]
    if s.endswith("의 배수") or s.endswith("소수") or s.endswith("무리수") or s.endswith("유리수") or s.endswith("정삼각형") or s.endswith("이등변삼각형"): return s + _ika(s) + " 아니"
    raise ValueError(s)


def sent(p, q):
    return p + ("면 " if p.endswith("아니") else "이면 ") + q + ("다" if q.endswith("아니") else "이다")


PROPS = []
for a in (1, 2, 3, 4, 5):
    PROPS.append((f"x > {a}", f"x² > {a * a}", True))
    PROPS.append((f"x = {a}", f"x² = {a * a}", True))
    PROPS.append((f"x² < {a * a}", f"x < {a}", True))
for a in (2, 3, 4, 5):
    PROPS.append((f"x가 {2 * a}의 배수", f"x가 {a}의 배수", True))
    PROPS.append((f"x가 {3 * a}의 배수", f"x가 {a}의 배수", True))
for a in (2, 3, 4, 6):
    PROPS.append((f"x + y > {2 * a}", f"x > {a}", False))
PROPS += [("x가 짝수", "x²이 짝수", True), ("x²이 홀수", "x가 홀수", True), ("x가 소수", "x가 홀수", False), ("x가 4의 배수", "x가 짝수", True), ("x가 짝수", "x가 4의 배수", False), ("x가 무리수", "x²이 유리수", False),
          ("삼각형 ABC가 정삼각형", "삼각형 ABC가 이등변삼각형", True), ("x > 3", "x > 1", True), ("x < 0", "x² > 0", True), ("x가 6의 배수", "x가 짝수", True)]


def _lg_rows(kind):
    out = {}
    for i, (p, q, true) in enumerate(PROPS):
        np_, nq = neg(p), neg(q)
        S = sent(p, q)
        variants = {"역": sent(q, p), "이": sent(np_, nq), "대우": sent(nq, np_), "d1": sent(np_, q), "d2": sent(nq, p)}
        for t in range(3):
            keys = list(variants); rng.shuffle(keys)
            letters = "ABCDE"
            opts = " ".join(f"{letters[j]}. {variants[k]}" for j, k in enumerate(keys))
            if kind == "conv":
                for ask in ("역", "이", "대우"):
                    L = letters[keys.index(ask)]
                    out[f"{i}_{t}_{ask}"] = {"Q": f"명제 '{S}'의 {ask}를 다음 A~E 중에서 고르시오. {opts}", "L": L, "K": ord(L) - 64, "ASK": ask, "S": S, "P": p, "QQ": q, "NP": np_, "NQ": nq, "OPT": opts,
                                            "PICK": variants[ask], "CONV": variants["역"], "INV": variants["이"], "CONTRA": variants["대우"]}
            elif true:
                L = letters[keys.index("대우")]
                out[f"{i}_{t}"] = {"Q": f"명제 '{S}'가 참일 때, 다음 A~E 중 반드시 참인 명제를 고르시오. {opts}", "L": L, "K": ord(L) - 64, "S": S, "P": p, "QQ": q, "NP": np_, "NQ": nq, "OPT": opts,
                                    "PICK": variants["대우"], "CONV": variants["역"], "INV": variants["이"], "CONTRA": variants["대우"]}
    return _pick(out, 330)


LG1_ROWS = _lg_rows("conv")
LG2_ROWS = _lg_rows("true")


def lg_t1():
    return T(LG, 1, LG_B, title="명제의 역·이·대우 고르기",
        skill="명제 p → q의 역 q → p, 이 ~p → ~q, 대우 ~q → ~p를 조건의 부정과 함께 정확히 만들기", axis={"조건": "부등식·등식·배수·홀짝·소수·무리수·삼각형", "묻는 것": "역 / 이 / 대우"}, disc="역(순서 바꿈)·이(둘 다 부정)·대우(바꾸고 부정)를 구분하고 부정을 정확히 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG1_ROWS)}}], table={"key": "f", "rows": LG1_ROWS},
        derive={"ans": "K"}, cost=["K"], verify=["K >= 1", "K <= 5"], ans_var=None,
        q="{Q}", answer="{L}",
        sol1="명제 p → q에 대하여 역은 q → p, 이는 ~p → ~q, 대우는 ~q → ~p이다. 부정은 부등호를 반대로(> ↔ ≤), '=' ↔ '≠', 짝수 ↔ 홀수, '…의 배수' ↔ '…의 배수가 아니다'로 쓴다.",
        sol2=[("p: {P}, q: {QQ}, ~p: {NP}, ~q: {NQ}", "부정 만들기"), ("역: {CONV} / 이: {INV} / 대우: {CONTRA}", "세 명제"), ("{ASK}는 '{PICK}' → {L}", None, ("{L}", "{ASK}"))],
        sol3=["역과 대우는 서로 '이'의 관계이고, 대우는 원래 명제와 참·거짓이 같다는 점으로 확인한다. 따라서 답은 {L}이다.", "{ASK}: {PICK}", "답 {L}"],
        model="~p: {NP}, ~q: {NQ}이므로 {ASK}는 '{PICK}'이다. 따라서 답은 {L}이다.",
        rubric=[("부정 만들기", 2, "~p: {NP}, ~q: {NQ}로 썼다.", "부등호의 등호 처리(>의 부정은 ≤)를 틀렸으면 1점."), ("고르기", 3, "보기 {L}({PICK}){eul(L)} 골랐다.", "역과 이를 바꿔 골랐으면 인정하지 않는다.")],
        pitfalls=[(">의 부정을 <로 씀(등호 누락)", "부정 만들기", "부분"), ("역과 이를 혼동", "고르기", "불인정"), ("대우에서 순서만 바꾸고 부정을 빠뜨림", "고르기", "불인정")])


def lg_t2():
    return T(LG, 2, LG_B, title="참인 명제의 대우 — 반드시 참인 명제 고르기",
        skill="명제가 참이면 그 대우도 참임을 이용해, 여러 명제 중 반드시 참인 것(대우)을 고르기", axis={"조건": "부등식·등식·배수·홀짝·삼각형", "보기": "역·이·대우·기타 5개"}, disc="역·이는 참이 아닐 수 있고 대우만 반드시 참임을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG2_ROWS)}}], table={"key": "f", "rows": LG2_ROWS},
        derive={"ans": "K"}, cost=["K"], verify=["K >= 1", "K <= 5"], ans_var=None,
        q="{Q}", answer="{L}",
        sol1="명제 p → q가 참이면 대우 ~q → ~p도 참이다. 역 q → p와 이 ~p → ~q는 참이 아닐 수 있다.",
        sol2=[("~p: {NP}, ~q: {NQ}", "부정 만들기"), ("대우: {CONTRA}", "대우"), ("반드시 참인 것은 대우 → {L}", None, ("{L}", "대우"))],
        sol3=["역 '{CONV}'의 반례를 하나 찾아 역이 참이 아닐 수 있음을 확인한다. 따라서 답은 {L}이다.", "대우: {CONTRA}", "답 {L}"],
        model="참인 명제의 대우는 참이다. ~q: {NQ}, ~p: {NP}이므로 대우는 '{CONTRA}'이고, 답은 {L}이다.",
        rubric=[("대우 만들기", 3, "대우 명제('{CONTRA}')를 세웠다.", "부정을 틀렸으면 1점."), ("고르기", 2, "보기 {L}{eul(L)} 골랐다.", "역을 골랐으면 인정하지 않는다.")],
        pitfalls=[("역을 참이라고 봄", "고르기", "불인정"), ("부정에서 등호 처리 실수", "대우 만들기", "부분"), ("이를 대우로 착각", "고르기", "불인정")])


# 귀류법: (증명할 명제, 처음 가정(정답), 오답 4개)
CONTRA = [
    ("√2는 무리수이다", "√2는 유리수이다", ["√2는 무리수이다", "√2는 정수이다", "√2는 자연수가 아니다", "√2 > 1이다"]),
    ("√3은 무리수이다", "√3은 유리수이다", ["√3은 무리수이다", "√3은 정수이다", "√3 > √2이다", "√3은 자연수가 아니다"]),
    ("√5는 무리수이다", "√5는 유리수이다", ["√5는 무리수이다", "√5는 정수이다", "√5는 자연수가 아니다", "√5 > 2이다"]),
    ("1 + √2는 무리수이다", "1 + √2는 유리수이다", ["√2는 유리수이다", "1 + √2는 무리수이다", "1 + √2는 정수이다", "√2는 무리수이다"]),
    ("2√3은 무리수이다", "2√3은 유리수이다", ["√3은 유리수이다", "2√3은 무리수이다", "2√3은 정수이다", "√3은 무리수이다"]),
    ("자연수 n에 대하여 n²이 짝수이면 n은 짝수이다", "n은 홀수이다", ["n²은 홀수이다", "n은 짝수이다", "n²은 짝수이다", "n은 소수이다"]),
    ("자연수 n에 대하여 n²이 3의 배수이면 n은 3의 배수이다", "n은 3의 배수가 아니다", ["n²은 3의 배수가 아니다", "n은 3의 배수이다", "n²은 3의 배수이다", "n은 홀수이다"]),
    ("실수 a, b에 대하여 a + b > 0이면 a > 0 또는 b > 0이다", "a ≤ 0이고 b ≤ 0이다", ["a ≤ 0 또는 b ≤ 0이다", "a < 0이고 b < 0이다", "a + b ≤ 0이다", "a > 0이고 b > 0이다"]),
    ("실수 a, b에 대하여 ab = 0이면 a = 0 또는 b = 0이다", "a ≠ 0이고 b ≠ 0이다", ["a ≠ 0 또는 b ≠ 0이다", "ab ≠ 0이다", "a = 0이고 b = 0이다", "a = 0 또는 b = 0이다"]),
    ("소수는 무한히 많다", "소수는 유한개이다", ["소수는 무한히 많다", "가장 작은 소수는 2이다", "소수는 홀수이다", "소수는 하나뿐이다"]),
    ("실수 x에 대하여 x² = 2이면 x는 무리수이다", "x는 유리수이다", ["x² ≠ 2이다", "x는 무리수이다", "x는 정수이다", "x > 0이다"]),
    ("자연수 n에 대하여 n² + n은 홀수가 아니다", "n² + n은 홀수이다", ["n은 홀수이다", "n은 짝수이다", "n² + n은 짝수이다", "n² + n은 소수이다"]),
    ("실수 x에 대하여 x + [[frac(1, x)]] ≥ 2이면 x > 0이다 (단, x ≠ 0)", "x < 0이다", ["x + [[frac(1, x)]] < 2이다", "x > 0이다", "x = 0이다", "x ≥ 0이다"]),
    ("정수 a, b에 대하여 a² + b²이 홀수이면 a, b 중 하나만 홀수이다", "a, b가 모두 홀수이거나 모두 짝수이다", ["a, b 중 하나만 홀수이다", "a² + b²은 짝수이다", "a, b가 모두 홀수이다", "a, b가 모두 짝수이다"]),
]


def _lg3_rows():
    out = {}
    for i, (prop, ans, wrong) in enumerate(CONTRA):
        for t in range(6):
            items = [ans] + wrong; rng.shuffle(items)
            letters = "ABCDE"
            opts = " ".join(f"{letters[j]}. {s}" for j, s in enumerate(items))
            L = letters[items.index(ans)]
            out[f"{i}_{t}"] = {"Q": f"명제 '{prop}'를 귀류법으로 증명하려고 한다. 증명을 시작할 때 세우는 가정으로 알맞은 것을 다음 A~E 중에서 고르시오. {opts}", "L": L, "K": ord(L) - 64, "PROP": prop, "ASSUME": ans, "OPT": opts}
    return _pick(out, 330)


LG3_ROWS = _lg3_rows()


def lg_t3():
    return T(LG, 3, LG_B, title="귀류법 — 처음에 세우는 가정 고르기",
        skill="귀류법은 결론의 부정을 가정하고 모순을 이끌어 내는 방법임을 알고, 결론의 부정을 정확히 쓰기", axis={"명제": "√p 무리수 · n² 홀짝 · a + b > 0 · ab = 0 · 소수 무한 · 절댓값 부등식", "보기": "결론의 부정(정답)·결론·가정의 부정·무관한 진술"}, disc="'또는'의 부정이 '그리고'가 됨을 포함해 결론의 부정을 세우는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG3_ROWS)}}], table={"key": "f", "rows": LG3_ROWS},
        derive={"ans": "K"}, cost=["K"], verify=["K >= 1", "K <= 5"], ans_var=None,
        q="{Q}", answer="{L}",
        sol1="귀류법은 증명하려는 결론이 거짓이라고(결론의 부정을) 가정한 뒤 모순을 이끌어 내어 결론이 참임을 보이는 방법이다. 가정은 '결론의 부정'이어야 한다.",
        sol2=[("결론: 명제의 '…이다' 부분", "결론 찾기"), ("결론의 부정: {ASSUME}", "부정"), ("따라서 {L}", None, ("{L}", "가정"))],
        sol3=["가정과 결론이 서로 모순되는지(둘 다 참일 수 없는지) 확인한다. 따라서 답은 {L}이다.", "가정: {ASSUME}", "답 {L}"],
        model="귀류법의 가정은 결론의 부정 '{ASSUME}'이다. 따라서 답은 {L}이다.",
        rubric=[("부정 세우기", 3, "결론의 부정('{ASSUME}')을 세웠다.", "'또는'을 '또는'으로 그대로 두었으면 1점."), ("고르기", 2, "보기 {L}{eul(L)} 골랐다.", "결론 자체를 골랐으면 인정하지 않는다.")],
        pitfalls=[("결론 자체를 가정으로 세움", "부정 세우기", "불인정"), ("'또는'의 부정을 '또는'으로 둠", "부정 세우기", "부분"), ("가정(전제)의 부정을 고름", "고르기", "불인정")])


LG_SEED = SEED(LG, category="대수", title="명제의 역·이·대우와 귀류법 — 보기에서 고르기", unit_id="h1-2", concept_ids=["h1-2-12", "h1-2-14"],
               schema_name="명제의 역과 대우·귀류법", note="답이 진술이라 보기 A~E 글자 답으로 바꿨다(m2-2-pythagoras-t3 방식). recheck 는 명제를 되읽어 부정·대우를 다시 만든다.",
               templates=[lg_t1(), lg_t2(), lg_t3()])


# ═══════════════════════════════════════════════════════════════════ 3. 산점도와 상관관계 (m3-2-14)
SC = "m3-2-scatter"
SC_B = {**HS, "process": "추론", "context": "자료맥락", "time_limit": 120, "prereq": ["순서쌍", "좌표평면"], "ops": ["통계"], "traps": ["점의 개수 세기", "x와 y의 역할"], "tags": ["산점도", "상관관계"]}
SCORES = list(range(50, 101, 5))


def _corr(pts):
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts); sxx = sum((p[0] - mx) ** 2 for p in pts); syy = sum((p[1] - my) ** 2 for p in pts)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


def _gen_pts(kind, n):
    """kind: pos / neg / none — 점수(50~100, 5 단위) 순서쌍 n개, 서로 다른 점."""
    for _ in range(200):
        pts = set()
        while len(pts) < n:
            x = rng.choice(SCORES)
            if kind == "pos": y = x + rng.choice((-10, -5, -5, 0, 0, 5, 5, 10))
            elif kind == "neg": y = 150 - x + rng.choice((-10, -5, -5, 0, 0, 5, 5, 10))
            else: y = rng.choice(SCORES)
            if 50 <= y <= 100: pts.add((x, y))
        pts = sorted(pts)
        r = _corr(pts)
        if (kind == "pos" and r > 0.7) or (kind == "neg" and r < -0.7) or (kind == "none" and abs(r) < 0.2):
            return pts
    return None


def _ptlist(pts):
    return ", ".join(f"({x}, {y})" for x, y in pts)


def _sc_fig(pts):
    return [{"fn": "scatter", "args": {"points": [{"x": x, "y": y} for x, y in pts], "x_label": "수학", "y_label": "과학", "x_range": [45, 105], "y_range": [45, 105]}}]


CTX = [("수학", "과학"), ("국어", "영어"), ("1차", "2차"), ("중간고사", "기말고사")]


def _sc1_rows():
    out = {}
    for i in range(120):
        kind = ("pos", "neg", "none")[i % 3]
        n = rng.choice((10, 12))
        pts = _gen_pts(kind, n)
        if not pts:
            continue
        cx, cy = CTX[i % 4]
        opts = ["양의 상관관계가 있다", "음의 상관관계가 있다", "상관관계가 없다"]
        order = [0, 1, 2]; rng.shuffle(order)
        letters = "ABC"
        optstr = " ".join(f"{letters[j]}. {opts[o]}" for j, o in enumerate(order))
        correct = {"pos": 0, "neg": 1, "none": 2}[kind]
        L = letters[order.index(correct)]
        WORD = opts[correct]
        out[f"c{i}"] = {"Q": f"다음은 학생 {n}명의 {cx} 점수 x와 {cy} 점수 y를 순서쌍 (x, y)로 나타낸 것이고, 그 산점도는 그림과 같다. {_ptlist(pts)}. 두 변량 x, y 사이의 상관관계로 옳은 것을 다음 A~C 중에서 고르시오. {optstr}",
                        "L": L, "K": ord(L) - 64, "WORD": WORD, "PTS": [{"x": x, "y": y} for x, y in pts], "XL": cx, "YL": cy, "N": n,
                        "TREND": {"pos": "x가 커질수록 y도 대체로 커진다", "neg": "x가 커질수록 y는 대체로 작아진다", "none": "x가 커져도 y가 커지거나 작아지는 경향이 없다"}[kind],
                        "CHK": {"pos": "점들이 오른쪽 위로 향하는 한 직선 주위에 모여 있다", "neg": "점들이 오른쪽 아래로 향하는 한 직선 주위에 모여 있다", "none": "점들이 어느 한 직선 주위에 모여 있지 않고 고르게 흩어져 있다"}[kind]}
    return _pick(out, 330)


SC1_ROWS = _sc1_rows()


def sc_t1():
    return T(SC, 1, SC_B, title="산점도에서 상관관계 판정하기",
        skill="산점도의 점들이 오른쪽 위로·오른쪽 아래로 몰리는지, 흩어져 있는지로 양·음의 상관관계와 상관관계 없음을 판정하기", axis={"상관": "양 / 음 / 없음", "자료": "점수 순서쌍 10~12개"}, disc="점의 분포 경향을 직선 방향으로 읽어 상관의 종류를 가르는가", diff=1,
        params=[{"name": "f", "values": {"in": list(SC1_ROWS)}}], table={"key": "f", "rows": SC1_ROWS},
        derive={"ans": "K"}, cost=["K"], verify=["K >= 1", "K <= 3"], ans_var=None,
        q="{Q}", answer="{L}",
        figure=[{"fn": "scatter", "args": {"points": "{PTS}", "x_label": "{XL}", "y_label": "{YL}", "x_range": [45, 105], "y_range": [45, 105]}}],
        sol1="산점도에서 x가 커질수록 y도 커지는 경향이면 양의 상관관계, y가 작아지는 경향이면 음의 상관관계, 뚜렷한 경향이 없으면 상관관계가 없다고 한다.",
        sol2=[("점의 분포: {TREND}", "경향 읽기"), ("따라서 {WORD}", "판정"), ("답: {L}", None, ("{L}", "판정"))],
        sol3=["점들이 오른쪽 위(또는 아래)로 향하는 한 직선 주위에 모이는지 확인하면, {CHK}. 따라서 답은 {L}이다.", "{WORD}", "답 {L}"],
        model="산점도에서 {TREND}. 따라서 {WORD}고 판단할 수 있으므로 답은 {L}이다.",
        rubric=[("경향 읽기", 3, "{TREND}는 것을 읽었다.", "몇 점만 보고 판정했으면 1점."), ("판정", 2, "{WORD}고 답했다.", "양·음을 바꿨으면 인정하지 않는다.")],
        pitfalls=[("점 몇 개만 보고 판정", "경향 읽기", "부분"), ("양과 음을 반대로 봄", "판정", "불인정"), ("점이 많이 흩어져 있어도 상관관계가 있다고 봄", "판정", "불인정")])


def _sc2_rows():
    out = {}
    for i in range(160):
        kind = ("pos", "neg", "none")[i % 3]
        n = rng.choice((10, 12))
        pts = _gen_pts(kind, n)
        if not pts:
            continue
        cx, cy = CTX[i % 4]
        a = rng.choice((70, 75, 80, 85))
        base = f"다음은 학생 {n}명의 {cx} 점수 x와 {cy} 점수 y를 순서쌍 (x, y)로 나타낸 것이고, 그 산점도는 그림과 같다. {_ptlist(pts)}."
        asks = (("both", f"{cx} 점수와 {cy} 점수가 모두 {a}점 이상인 학생 수", sum(1 for x, y in pts if x >= a and y >= a), f"x ≥ {a}이고 y ≥ {a}인 점"),
                ("higher", f"{cy} 점수가 {cx} 점수보다 높은 학생 수", sum(1 for x, y in pts if y > x), "y > x인 점(직선 y = x 위쪽)"),
                ("lowx", f"{cx} 점수가 {a}점 미만인 학생 수", sum(1 for x, y in pts if x < a), f"x < {a}인 점"),
                ("same", f"{cx} 점수와 {cy} 점수가 같은 학생 수", sum(1 for x, y in pts if x == y), "x = y인 점(직선 y = x 위)"))
        for kk, ask, v, desc in asks:
            if v == 0:
                continue
            r = _row(f"산점도 {i} {kk}", v, Q=f"{base} {ask}{_eul(ask)} 구하시오.", PTS=[{"x": x, "y": y} for x, y in pts], XL=cx, YL=cy, N=n, ASK=ask, DESC=desc, CNT=v)
            if r: out[f"{i}_{kk}"] = r
    return _pick(out, 330)


SC2_ROWS = _sc2_rows()


def sc_t2():
    return T(SC, 2, SC_B, title="산점도에서 조건을 만족하는 점의 개수",
        skill="산점도(또는 순서쌍)에서 x, y의 조건(이상·미만·y > x·x = y)을 만족하는 점의 개수 세기", axis={"조건": "둘 다 a 이상 / y > x / x < a / x = y", "자료": "점수 순서쌍 10~12개"}, disc="경계(이상·미만)와 직선 y = x의 위·아래를 정확히 가르는가", diff=1,
        params=[{"name": "f", "values": {"in": list(SC2_ROWS)}}], table={"key": "f", "rows": SC2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        figure=[{"fn": "scatter", "args": {"points": "{PTS}", "x_label": "{XL}", "y_label": "{YL}", "x_range": [45, 105], "y_range": [45, 105]}}],
        sol1="산점도에서 조건은 영역으로 나타난다: x ≥ a는 세로선 x = a의 오른쪽, y > x는 직선 y = x의 위쪽, x = y는 직선 y = x 위의 점이다. 순서쌍을 하나씩 조건에 대입해 세어도 된다.",
        sol2=[("조건에 맞는 점: {DESC}", "영역 읽기"), ("순서쌍을 대입해 세면 {CNT}개", "세기"), ("답: {ans}", None, ("{ans}", "개수"))],
        sol3=["경계 위의 점(이상은 포함, 미만·초과는 제외)을 다시 확인한다. 따라서 답은 {ans}이다.", "{DESC}: {CNT}개", "답 {ans}"],
        model="{DESC}을 세면 {CNT}개이다. 따라서 답은 {ans}이다.",
        rubric=[("영역 읽기", 2, "{DESC}으로 조건을 옮겼다.", "y > x를 x > y로 읽었으면 인정하지 않는다."), ("세기", 3, "{ans}개로 세었다.", "경계 처리 실수면 2점.")],
        pitfalls=[("이상과 초과를 혼동(경계 점 포함 여부)", "세기", "부분"), ("y > x의 방향을 반대로 봄", "영역 읽기", "불인정"), ("점을 빠뜨리거나 두 번 셈", "세기", "부분")])


def _dc(f):
    """t3 확인·모범답안 문장용 소수 표기(정수면 정수, 아니면 소수 한 자리까지)."""
    return str(f.numerator) if f.denominator == 1 else f"{float(f):g}"


def _sc3_rows():
    out = {}
    for i in range(160):
        kind = ("pos", "neg", "none")[i % 3]
        n = rng.choice((10, 12))
        pts = _gen_pts(kind, n)
        if not pts:
            continue
        cx, cy = CTX[i % 4]
        base = f"다음은 학생 {n}명의 {cx} 점수 x와 {cy} 점수 y를 순서쌍 (x, y)로 나타낸 것이고, 그 산점도는 그림과 같다. {_ptlist(pts)}."
        up = sum(1 for x, y in pts if y > x); dn = sum(1 for x, y in pts if y < x)
        sx = sum(x for x, y in pts); sy = sum(y for x, y in pts)
        eq = n - up - dn; hi = sum(1 for x, y in pts if x + y >= 150)
        chk = {"diff": f"p + q = {up + dn}" + (f"에 두 점수가 같은 학생(직선 y = x 위의 점) {eq}명을 더하면 전체 인원 {n}명과 같다" if eq else f"{_ro(up + dn)} 전체 인원 {n}명과 같다(두 점수가 같은 학생은 없다)"),
               "pct": f"합이 150점 이상인 학생 {hi}명과 150점 미만인 학생 {n - hi}명을 더하면 전체 인원 {n}명과 같고, {hi} ÷ {n} × 100 = {_dc(Fraction(hi * 100, n))}이다",
               "meanx": f"평균 {_dc(Fraction(sx, n))}에 인원 {n}{_eul(n)} 곱하면 {cx} 점수의 합 {sx}{_wa(sx)} 같다"}
        conc = {"diff": f"p − q = {up} − {dn} = {up - dn}이다", "pct": f"{cx} 점수와 {cy} 점수의 합이 150점 이상인 학생은 전체의 {_dc(Fraction(hi * 100, n))} %이다",
                "meanx": f"{cx} 점수의 평균은 {_dc(Fraction(sx, n))}점이다"}
        # 묻는 것별 [방침]·부분점수·실수거리(pitfalls.py 의 {PIT1}~{PIT3} 자리표시자로 들어간다)
        per = {"diff": {"S1": "산점도의 각 점은 한 학생의 두 점수이다. 직선 y = x 위쪽의 점은 y가 더 큰 학생, 아래쪽의 점은 x가 더 큰 학생이고, 직선 y = x 위의 점은 두 점수가 같은 학생이므로 p와 q 어느 쪽에도 세지 않는다.",
                        "PA1": "직선 y = x의 위·아래를 바꿨으면 인정하지 않는다. 두 점수가 같은 학생을 p나 q에 넣어 셌으면 1점.", "PA2": "q − p로 계산했으면 인정하지 않는다. 뺄셈 값 계산 실수면 1점.",
                        "PIT1": "직선 y = x 위의 점(두 점수가 같은 학생)을 p나 q에 넣어 셈", "PIT2": "p − q 대신 q − p를 계산함", "PIT3": "뺄셈 값 계산 실수"},
               "pct": {"S1": "산점도의 각 점은 한 학생의 두 점수이다. 두 점수의 합이 150점 이상인 점(합이 정확히 150점인 점 포함)을 세고, 비율은 (조건을 만족하는 학생 수) ÷ (전체 학생 수) × 100이다.",
                       "PA1": "두 점수의 합이 정확히 150인 학생을 빠뜨렸으면 1점.", "PA2": "100을 곱하지 않았으면 인정하지 않는다. 나눗셈 계산 실수면 1점.",
                       "PIT1": "합이 정확히 150점인 점을 빼고 셈", "PIT2": "백분율에서 100을 곱하지 않음", "PIT3": "나눗셈 계산 실수"},
               "meanx": {"S1": f"산점도의 각 점은 한 학생의 두 점수이고, {cx} 점수는 각 점의 x좌표이다. x좌표를 모두 더한 합을 전체 학생 수로 나누면 {cx} 점수의 평균이다.",
                         "PA1": f"{cy} 점수(y좌표)를 더했으면 인정하지 않는다. x좌표를 빠뜨리거나 두 번 더했으면 1점.", "PA2": "합을 인원으로 나누지 않았으면 인정하지 않는다. 인원 수를 잘못 세었거나 나눗셈 실수면 1점.",
                         "PIT1": "x좌표 하나를 빠뜨리거나 두 번 더함", "PIT2": "합을 인원으로 나누지 않고 합을 답함", "PIT3": "인원 수를 잘못 세어 나누거나 나눗셈 실수"}}
        asks = (("diff", f"{cy} 점수가 {cx} 점수보다 높은 학생 수를 p, 낮은 학생 수를 q라 할 때 p − q의 값", Fraction(up - dn), f"p = {up}, q = {dn}"),
                ("pct", f"{cx} 점수와 {cy} 점수의 합이 150점 이상인 학생은 전체의 몇 %인지", Fraction(sum(1 for x, y in pts if x + y >= 150) * 100, n), f"합이 150 이상인 점 {sum(1 for x, y in pts if x + y >= 150)}개 ÷ {n}명 × 100"),
                ("meanx", f"{cx} 점수의 평균", Fraction(sx, n), f"{cx} 점수의 합 {sx} ÷ {n}"))
        for kk, ask, v, desc in asks:
            if v == 0 or (kk == "pct" and (v * 100).denominator != 1) or (kk == "meanx" and (v * 10).denominator != 1):
                continue
            r = _row(f"산점도3 {i} {kk}", v, Q=f"{base} {ask}{_eul(ask)} 구하시오.", PTS=[{"x": x, "y": y} for x, y in pts], XL=cx, YL=cy, N=n, ASK=ask, DESC=desc, KIND=kk, CHK=chk[kk], CONC=conc[kk], **per[kk])
            if r: out[f"{i}_{kk}"] = r
    return _pick(out, 330)


SC3_ROWS = _sc3_rows()


def sc_t3():
    return T(SC, 3, SC_B, title="산점도 자료의 계산 — 위·아래 점의 개수 차, 비율, 평균",
        skill="산점도의 순서쌍에서 직선 y = x 위·아래의 점의 개수, 조건을 만족하는 비율(%), 한 변량의 평균을 계산하기", axis={"묻는 것": "p − q / 백분율 / 평균", "자료": "점수 순서쌍 10~12개"}, disc="산점도를 자료표로 되읽어 계산하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SC3_ROWS)}}], table={"key": "f", "rows": SC3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{dec(ans)}",
        figure=[{"fn": "scatter", "args": {"points": "{PTS}", "x_label": "{XL}", "y_label": "{YL}", "x_range": [45, 105], "y_range": [45, 105]}}],
        sol1="{S1}",
        sol2=[("{DESC}", "자료 읽기"), ("계산하면 {dec(ans)}", "계산"), ("답: {dec(ans)}", None, ("{dec(ans)}", "값"))],
        sol3=["{CHK}. 따라서 답은 {dec(ans)}이다.", "{DESC}", "답 {dec(ans)}"],
        model="{DESC}이므로 {CONC}. 따라서 답은 {dec(ans)}이다.",
        rubric=[("자료 읽기", 2, "{DESC}으로 읽었다.", "{PA1}"), ("계산", 3, "{dec(ans)}{eul(dec(ans))} 구했다.", "{PA2}")],
        pitfalls=[("{PIT1}", "자료 읽기", "부분"), ("{PIT2}", "계산", "불인정"), ("{PIT3}", "계산", "부분")])


SC_SEED = SEED(SC, category="확률통계", title="산점도와 상관관계 — 판정·개수·계산", unit_id="m3-2", concept_ids=["m3-2-14"],
               schema_name="산점도와 상관관계", note="scatter 도형 + 문면에 순서쌍 나열(DB 키는 문면만이라 수치는 문면에). 상관 판정은 글자 답(A~C), 나머지는 수 답. 점수는 50~100(5 단위)이라 개수 답과 겹치지 않는다.",
               templates=[sc_t1(), sc_t2(), sc_t3()])


if __name__ == "__main__":
    run(IN_SEED, LG_SEED, SC_SEED)
