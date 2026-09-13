# itemfactory/tools/mkseed_h3_calc.py — 고3 미적분 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h3_calc.py
#     → seeds/h3-1-seqlim.json  (수열의 극한·급수: 수열의 극한값·등비수열 수렴 조건·부분분수 급수·등비급수·등비급수 활용, 5틀)
#     → seeds/h3-1-diff2.json   (여러 가지 미분: 지수로그 극한·삼각 극한·미분법(곱·몫·합성·매개변수·음함수·역함수)·접선·극값, 5틀)
#     → seeds/h3-1-integ2.json  (여러 가지 적분: 기본 적분·치환·부분·정적분과 급수·넓이·속도와 거리, 6틀)
#   값은 파이썬(sympy)에서 미리 계산해 행(VN/VD)에 넣는다. π·e 는 마커 안 pi·e 상수.
from __future__ import annotations

import math
import os
import random
import re
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260920)
X, N, K, TT = sp.symbols("x n k t")


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _fmp(v):
    return f"({_fm(v)})" if Fraction(v) < 0 else _fm(v)


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


def _rat(v):
    v = sp.nsimplify(v)
    if v.is_Rational:
        return Fraction(int(v.p), int(v.q))
    return None


def _row(q, v, **kw):
    """분수 답 행 — 노출 검사 후 VN/VD 와 부가 필드"""
    f = Fraction(v)
    if f == 0 or f in _nums(q) or abs(f) in _nums(q):
        return None
    d = {"VN": f.numerator, "VD": f.denominator}
    d.update(kw)
    return d


def _sc(c):
    """계수 문자열 — 1 → '', -1 → '-', 그 외 수"""
    return "" if c == 1 else ("-" if c == -1 else str(c))


def _sg(c):
    return f"{'+' if c > 0 else '−'} {abs(c)}"


def _sgc(c):
    """문자 앞 부호 붙은 계수 — '+ ', '− ', '+ 3', '− 3'"""
    return f"{'+' if c > 0 else '−'} {'' if abs(c) == 1 else abs(c)}"


# ═══════════════════════════════════════════════════════════════════ 1. 수열의 극한·급수
SL = "h3-1-seqlim"
SL_B = {**HS, "prereq": ["등비수열", "함수의 극한"], "ops": ["수열의 극한"], "traps": ["∞/∞ 최고차항", "수렴 조건의 등호"], "tags": ["수열의 극한", "급수", "등비급수"]}


def _sl1_rows():
    out = {}
    for a in range(1, 7):
        for b in range(1, 7):
            for c in (-3, -1, 2, 5):
                for d in (-2, 1, 3):
                    q = f"[[lim(n, inf, frac({_sc(a)}pow(n,2) {_sgc(c)}n, {_sc(b)}pow(n,2) {_sg(d)}))]]"
                    r = _row(q, Fraction(a, b), EXPR=q, KIND="∞/∞ — 분모의 최고차항 n²으로 나눔", STEP=f"분모·분자를 n²으로 나누면 [[frac({a} + frac({c}, n), {b} + frac({d}, pow(n,2)))]]", RES=f"n → ∞이면 1/n, 1/n² → 0이므로 [[frac({a}, {b})]] = {_fm(Fraction(a, b))}")
                    if r: out[f"r{a}_{b}_{c}_{d}"] = r
    for a in range(1, 13):
        q = f"[[lim(n, inf, sqrt(pow(n,2) + {_sc(a)}n) − n)]]".replace("+ n)", "+ n)")
        r = _row(q, Fraction(a, 2), EXPR=q, KIND="∞ − ∞ — 유리화", STEP=f"[[frac({_sc(a)}n, sqrt(pow(n,2) + {_sc(a)}n) + n)]], 분모·분자를 n으로 나누면 [[frac({a}, sqrt(1 + frac({a}, n)) + 1)]]", RES=f"n → ∞이면 {a}/n → 0이므로 [[frac({a}, 2)]] = {_fm(Fraction(a, 2))}")
        if r: out[f"s{a}"] = r
    for big in (2, 3, 5):
        for small in (2, 3):
            if small >= big:
                continue
            for p in (1, 2, 3):
                for qv in (1, 2, -1):
                    # (p·big^n + small^n)/(q·big^n − small^n) → p/q
                    num = f"{_sc(p)}pow({big},n) + pow({small},n)"
                    den = f"{_sc(qv)}pow({big},n) − pow({small},n)"
                    q = f"[[lim(n, inf, frac({num}, {den}))]]"
                    r = _row(q, Fraction(p, qv), EXPR=q, KIND=f"지수 — 밑이 가장 큰 {big}ⁿ으로 나눔", STEP=f"분모·분자를 [[pow({big},n)]]으로 나누면 [[frac({p} + pow(frac({small},{big}),n), {qv} − pow(frac({small},{big}),n))]]", RES=f"n → ∞이면 ({small}/{big})ⁿ → 0이므로 {_fm(Fraction(p, qv))}")
                    if r: out[f"e{big}_{small}_{p}_{qv}"] = r
    return _pick(out, 330)


SL1_ROWS = _sl1_rows()


def sl_t1():
    return T(SL, 1, SL_B, title="수열의 극한값 — ∞/∞, ∞ − ∞, 지수",
        skill="분모의 최고차항으로 나누기, 유리화, 밑이 가장 큰 거듭제곱으로 나누기로 극한값 구하기", axis={"꼴": "유리식 / 근호 차 / 지수", "값": "분수"}, disc="발산하는 항을 나눠 0으로 가는 항을 만들어 극한값을 읽는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SL1_ROWS)}}], table={"key": "f", "rows": SL1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="수열의 극한에서 ∞/∞ 꼴은 분모의 최고차항(또는 밑이 가장 큰 거듭제곱)으로 분모·분자를 나누고, ∞ − ∞ 꼴은 유리화해 ∞/∞ 꼴로 바꾼다. 1/n, rⁿ(|r| < 1) → 0을 쓴다. 이 문제는 {KIND}이다.",
        sol2=[("{KIND}", "꼴 판단"), ("{STEP}", "변형"), ("{RES}", None, ("{ans}", "극한값"))],
        sol3=["나눈 뒤 남는 항이 n → ∞에서 0으로 가는지(1/n, (r)ⁿ) 확인한다. 따라서 극한값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{KIND}. {STEP}. {RES}. 따라서 극한값은 {ans}이다.",
        rubric=[("변형", 3, "{STEP} 꼴로 변형했다.", "최고차항이 아닌 것으로 나눴으면 1점."), ("극한값", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("∞/∞를 ∞로 답함", "변형", "불인정"), ("유리화 없이 √(n² + an) − n → 0으로 봄", "변형", "불인정"), ("밑이 작은 거듭제곱으로 나눔", "변형", "부분")])


def sl_t2():
    return T(SL, 2, SL_B, title="등비수열의 수렴 조건 — 정수 r의 개수",
        skill="등비수열 {(r − c)/k}ⁿ이 수렴할 조건 −1 < 공비 ≤ 1을 써서 정수 r 세기", axis={"c": "−5~5", "k": "2~6", "묻는 것": "개수 / 최댓값"}, disc="수렴 조건 −1 < 공비 ≤ 1에서 1은 포함, −1은 제외임을 정확히 쓰는가", diff=2,
        params=[{"name": "c", "values": {"int": [-5, 5]}}, {"name": "k", "values": {"int": [2, 6]}}, {"name": "s", "values": {"in": ["cnt", "max"]}}],
        table={"key": "s", "rows": {"cnt": {"ASK": "정수 r의 개수", "w": 1}, "max": {"ASK": "정수 r의 최댓값", "w": 0}}},
        derive={"lo": "c - k", "hi": "c + k", "nc": "-c", "ans": "w*(2*k) + (1 - w)*(c + k)"},
        constraints=["ans != 0", "ans not in (c, k, lo, hi)"], cost=["c", "k", "lo", "hi", "ans"], verify=["hi - lo == 2*k"],
        q="등비수열 {{[[pow(frac(r {sgn(nc)}, {k}), n)]]}}이 수렴하도록 하는 {ASK}를 구하시오.", answer="{ans}",
        sol1="등비수열 {{rⁿ}}은 −1 < r ≤ 1일 때 수렴한다(r = 1이면 1로 수렴, r = −1이면 진동). 공비 (r {sgn(nc)})/{k}에 대해 −1 < (r {sgn(nc)})/{k} ≤ 1을 풀면 {lo} < r ≤ {hi}이다.",
        sol2=[("수렴 조건: −1 < 공비 ≤ 1", "등비수열의 수렴"), ("−1 < [[frac(r {sgn(nc)}, {k})]] ≤ 1 → −{k} < r {sgn(nc)} ≤ {k} → {lo} < r ≤ {hi}", "부등식"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["r = {hi}이면 공비 1(수렴), r = {lo}이면 공비 −1(진동)이므로 {hi}는 포함하고 {lo}는 제외한다. 따라서 {ASK}는 {ans}이다.", "{lo} < r ≤ {hi}", "{ASK} {ans}"],
        model="수렴 조건 −1 < (r {sgn(nc)})/{k} ≤ 1에서 {lo} < r ≤ {hi}이므로 {ASK}는 {ans}이다.",
        rubric=[("수렴 조건", 3, "{lo} < r ≤ {hi}{eul(hi)} 얻었다.", "−1을 포함했거나 1을 제외했으면 1점."), ("답", 2, "{ASK} {ans}{eul(ans)} 구했다.", "세기 실수면 1점.")],
        pitfalls=[("수렴 조건을 −1 ≤ r ≤ 1로 둠", "수렴 조건", "부분"), ("r = 1을 제외", "수렴 조건", "부분"), ("정수 개수 세기 실수", "답", "부분")])


def _sl3_rows():
    out = {}
    kinds = [("frac(1, n(n + 1))", lambda n: Fraction(1, n * (n + 1)), "[[frac(1, n)]] − [[frac(1, n + 1)]]", "1 − [[frac(1, n + 1)]] → 1"),
             ("frac(1, (2n − 1)(2n + 1))", lambda n: Fraction(1, (2 * n - 1) * (2 * n + 1)), "[[frac(1,2)]]([[frac(1, 2n − 1)]] − [[frac(1, 2n + 1)]])", "[[frac(1,2)]](1 − [[frac(1, 2n + 1)]]) → [[frac(1,2)]]"),
             ("frac(1, n(n + 2))", lambda n: Fraction(1, n * (n + 2)), "[[frac(1,2)]]([[frac(1, n)]] − [[frac(1, n + 2)]])", "[[frac(1,2)]](1 + [[frac(1,2)]] − [[frac(1, n + 1)]] − [[frac(1, n + 2)]]) → [[frac(3,4)]]"),
             ("frac(1, (n + 1)(n + 2))", lambda n: Fraction(1, (n + 1) * (n + 2)), "[[frac(1, n + 1)]] − [[frac(1, n + 2)]]", "[[frac(1,2)]] − [[frac(1, n + 2)]] → [[frac(1,2)]]"),
             ("frac(1, (n + 2)(n + 3))", lambda n: Fraction(1, (n + 2) * (n + 3)), "[[frac(1, n + 2)]] − [[frac(1, n + 3)]]", "[[frac(1,3)]] − [[frac(1, n + 3)]] → [[frac(1,3)]]"),
             ("frac(1, n(n + 3))", lambda n: Fraction(1, n * (n + 3)), "[[frac(1,3)]]([[frac(1, n)]] − [[frac(1, n + 3)]])", "[[frac(1,3)]](1 + [[frac(1,2)]] + [[frac(1,3)]]) → [[frac(11,18)]]"),
             ("frac(1, (3n − 2)(3n + 1))", lambda n: Fraction(1, (3 * n - 2) * (3 * n + 1)), "[[frac(1,3)]]([[frac(1, 3n − 2)]] − [[frac(1, 3n + 1)]])", "[[frac(1,3)]](1 − [[frac(1, 3n + 1)]]) → [[frac(1,3)]]")]
    for m in (1, 2, 3, 4, 6, 12):
        for expr, fn, part, tel in kinds:
            # 무한급수 값 = m × lim 부분합 (sympy 로 확인)
            base = {"frac(1, n(n + 1))": Fraction(1), "frac(1, (2n − 1)(2n + 1))": Fraction(1, 2), "frac(1, n(n + 2))": Fraction(3, 4), "frac(1, (n + 1)(n + 2))": Fraction(1, 2), "frac(1, (n + 2)(n + 3))": Fraction(1, 3), "frac(1, n(n + 3))": Fraction(11, 18), "frac(1, (3n − 2)(3n + 1))": Fraction(1, 3)}[expr]
            v = m * base
            inner = expr if m == 1 else f"frac({m}, {expr[len('frac(1, '):-1]})"
            q = f"[[sum(n, 1, inf, {inner})]]"
            r = _row(q, v, EXPR=q, PART=(part if m == 1 else f"{m} × ({part})"), TEL=tel, M=m)
            if r: out[f"{m}_{expr}"] = r
    return out


SL3_ROWS = _sl3_rows()


def sl_t3():
    return T(SL, 3, SL_B, title="급수의 합 — 부분분수와 부분합의 극한",
        skill="일반항을 부분분수로 나눠 부분합 Sₙ을 구하고 n → ∞의 극한으로 급수의 합 구하기", axis={"일반항": "1/(n(n+1)), 1/((2n−1)(2n+1)), 1/(n(n+2)) 등 7가지 × 상수배"}, disc="급수의 합은 부분합의 극한임을 알고 소거 후 남는 항의 극한을 취하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SL3_ROWS)}}], table={"key": "f", "rows": SL3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="급수 {EXPR}의 합을 구하시오.", answer="{ans}",
        sol1="급수의 합은 부분합 Sₙ = a₁ + a₂ + ⋯ + aₙ의 극한이다. 일반항을 부분분수로 나누면 이웃한 항이 소거되어 Sₙ이 간단한 식이 되고, n → ∞에서 1/n 꼴의 항이 0으로 간다.",
        sol2=[("일반항 = {PART}", "부분분수"), ("Sₙ = {TEL}", "부분합의 극한"), ("급수의 합 = {ans}", None, ("{ans}", "합"))],
        sol3=["부분합의 처음 몇 개(S₁, S₂)를 직접 더해 공식과 맞는지 확인한다. 따라서 급수의 합은 {ans}이다.", "{TEL}", "합 {ans}"],
        model="일반항 = {PART}이므로 Sₙ = {TEL}. 따라서 급수의 합은 {ans}이다.",
        rubric=[("부분분수·부분합", 3, "Sₙ = {TEL} 꼴로 구했다.", "부분분수 계수를 빠뜨렸으면 1점."), ("극한", 2, "{ans}{eul(ans)} 구했다.", "남는 항의 극한 실수면 1점.")],
        pitfalls=[("부분합을 구하지 않고 일반항의 극한(0)을 답함", "부분분수·부분합", "불인정"), ("부분분수 계수(½, ⅓) 누락", "부분분수·부분합", "부분"), ("남는 항 처리 실수", "극한", "부분")])


def _sl4_rows():
    out = {}
    for a in (1, 2, 3, 4, 5, 6, 8, 9, 12):
        for rn, rd in ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (-1, 2), (-1, 3), (-2, 3), (2, 5), (-3, 4)):
            r = Fraction(rn, rd)
            v = a / (1 - r)
            rs = f"frac({rn},{rd})" if rn > 0 else f"-frac({-rn},{rd})"
            rd_ = f"[[{rs}]]"
            q = f"[[sum(n, 1, inf, {a} pow({rs}, n − 1))]]" if a > 1 else f"[[sum(n, 1, inf, pow({rs}, n − 1))]]"
            row = _row(q, v, EXPR=q, A=a, RS=rd_, KIND="첫째항 a, 공비 r", STEP=f"첫째항 {a}, 공비 {rd_} (|r| < 1이므로 수렴)", RES=f"[[frac(a, 1 − r)]] = [[frac({a}, 1 − {rs})]] = {_fm(v)}".replace("1 − -", "1 + "))
            if row: out[f"g{a}_{rn}_{rd}"] = row
            v2 = a * r / (1 - r)
            q2 = f"[[sum(n, 1, inf, {a} pow({rs}, n))]]" if a > 1 else f"[[sum(n, 1, inf, pow({rs}, n))]]"
            row2 = _row(q2, v2, EXPR=q2, A=a, RS=rd_, KIND="첫째항 ar, 공비 r", STEP=f"첫째항 {a} × {rd_} = {_fm(a * r)}, 공비 {rd_}", RES=f"[[frac(a, 1 − r)]] = [[frac({a * r}, 1 − {rs})]] = {_fm(v2)}".replace("1 − -", "1 + "))
            if row2: out[f"h{a}_{rn}_{rd}"] = row2
    for ab in range(10, 100):
        if ab % 11 == 0 or ab % 10 == 0:
            continue
        f = Fraction(ab, 99)
        v = f.numerator + f.denominator
        q = f"순환소수 0.{ab // 10}{ab % 10}{ab // 10}{ab % 10}{ab // 10}{ab % 10}⋯을 등비급수를 이용해 기약분수 [[frac(a, b)]]로 나타낼 때, a + b의 값을 구하시오."
        row = _row(q, v, EXPR=q, A=ab, RS="[[frac(1,100)]]", KIND="순환소수 → 등비급수", STEP=f"0.{ab:02d}{ab:02d}⋯ = [[frac({ab}, 100)]] + [[frac({ab}, 10000)]] + ⋯ (첫째항 {ab}/100, 공비 1/100)", RES=f"[[frac(frac({ab},100), 1 − frac(1,100))]] = [[frac({ab}, 99)]] = {_fm(f)}, a + b = {v}")
        if row: out[f"d{ab}"] = row
    return _pick(out, 330)


SL4_ROWS = _sl4_rows()


def sl_t4():
    return T(SL, 4, SL_B, title="등비급수의 합 — a/(1 − r)와 순환소수",
        skill="|r| < 1인 등비급수의 합 a/(1 − r)를 쓰고, 순환소수를 등비급수로 보아 분수로 바꾸기", axis={"첫째항": "1~12", "공비": "±1/2, ±1/3, 2/3, …", "순환소수": "0.ȧḃ"}, disc="첫째항과 공비를 정확히 읽고(n − 1 vs n) 수렴 조건을 확인한 뒤 공식을 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SL4_ROWS)}}], table={"key": "f", "rows": SL4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}" if False else "{Q}", answer="{ans}",
        sol1="첫째항 a, 공비 r인 등비급수는 |r| < 1일 때 수렴하고 합은 [[frac(a, 1 − r)]]이다. 지수가 n − 1이면 첫째항이 a, 지수가 n이면 첫째항이 ar임에 주의한다({KIND}).",
        sol2=[("{STEP}", "첫째항·공비"), ("수렴 조건 |r| < 1 확인", "수렴"), ("{RES}", None, ("{ans}", "합"))],
        sol3=["처음 두세 항을 더한 값이 합보다 작고 합에 가까워지는지 확인한다. 따라서 합은 {ans}이다.", "{RES}", "합 {ans}"],
        model="{STEP}이므로 {RES}. 따라서 합은 {ans}이다.",
        rubric=[("첫째항·공비", 3, "{STEP} 꼴로 읽었다.", "첫째항을 잘못 읽었으면 1점."), ("합", 2, "{ans}{eul(ans)} 구했다.", "공식 분모 1 − r 실수면 1점.")],
        pitfalls=[("지수가 n인데 첫째항을 a로 둠", "첫째항·공비", "불인정"), ("공식을 a/(r − 1)로 씀", "합", "불인정"), ("순환소수의 공비를 1/10으로 둠(두 자리 순환)", "첫째항·공비", "부분")])


def _sl4_fix(t):
    for k, row in t["table"]["rows"].items():
        row["Q"] = row["EXPR"] if k.startswith("d") else f"등비급수 {row['EXPR']}의 합을 구하시오."
    return t


def _sl5_rows():
    out = {}
    for S1 in (4, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 64):
        for rn, rd, desc in ((1, 2, "각 변의 중점을 이어 만든 정사각형(넓이가 절반)"), (1, 4, "각 변의 길이를 절반으로 줄인 닮은 도형(넓이가 1/4)"), (4, 9, "각 변의 길이를 2/3배로 줄인 닮은 도형(넓이가 4/9)"), (1, 3, "넓이가 1/3씩 줄어드는 도형")):
            r = Fraction(rn, rd)
            v = S1 / (1 - r)
            q = f"넓이가 {S1}인 도형 S₁에서 시작하여 {desc}을 차례로 만들어 S₂, S₃, ⋯을 얻는다. 모든 도형의 넓이의 합 S₁ + S₂ + S₃ + ⋯을 구하시오."
            row = _row(q, v, Q=q, S1=S1, RS=f"[[frac({rn},{rd})]]", RES=f"[[frac({S1}, 1 − frac({rn},{rd}))]] = {_fm(v)}", S2=_fm(S1 * r))
            if row: out[f"{S1}_{rn}_{rd}"] = row
    return out


SL5_ROWS = _sl5_rows()


def sl_t5():
    return T(SL, 5, SL_B, title="등비급수의 활용 — 닮은 도형의 넓이의 합",
        skill="넓이가 일정한 비로 줄어드는 도형의 넓이의 합을 등비급수 S₁/(1 − r)로 구하기", axis={"S₁": "4~64", "비": "1/2, 1/4, 4/9, 1/3"}, disc="넓이의 비(길이비의 제곱)를 공비로 잡는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SL5_ROWS)}}], table={"key": "f", "rows": SL5_ROWS},
        derive={"ans": "VN/VD"}, cost=["S1", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="닮은 도형이 반복되면 넓이는 등비수열을 이룬다. 길이의 비가 k이면 넓이의 비는 k²이다. 첫째항 S₁ = {S1}, 공비 {RS}이므로 등비급수의 합 S₁/(1 − r)를 쓴다.",
        sol2=[("S₁ = {S1}, S₂ = {S2}, 공비 r = {RS}", "넓이의 비"), ("|r| < 1이므로 수렴, 합 = [[frac(S1, 1 − r)]]", "등비급수"), ("{RES}", None, ("{ans}", "합"))],
        sol3=["S₂/S₁ = {S2}/{S1}이 공비 {RS}와 같은지 확인한다. 따라서 합은 {ans}이다.", "{RES}", "합 {ans}"],
        model="넓이는 첫째항 {S1}, 공비 {RS}인 등비수열이므로 합은 {RES}이다. 따라서 답은 {ans}이다.",
        rubric=[("공비", 3, "넓이의 공비 {RS}{eul(S1)} 잡았다.", "길이의 비를 공비로 썼으면 인정하지 않는다."), ("합", 2, "{ans}{eul(ans)} 구했다.", "공식 실수면 1점.")],
        pitfalls=[("길이의 비를 넓이의 공비로 씀", "공비", "불인정"), ("첫째항을 S₂로 둠", "합", "부분"), ("1 − r 계산 실수", "합", "부분")])


SL_SEED = SEED(SL, category="해석", title="수열의 극한과 급수 — 극한값·등비수열 수렴 조건·부분분수 급수·등비급수(순환소수)·닮은 도형의 넓이 합", unit_id="h3-1", concept_ids=["h3-1-01", "h3-1-02", "h3-1-03", "h3-1-04"],
               schema_name="수열의 극한과 급수", note="극한값·급수 합은 파이썬에서 계산(VN/VD). 순환소수는 두 자리 순환만.",
               templates=[sl_t1(), sl_t2(), sl_t3(), _sl4_fix(sl_t4()), sl_t5()])


# ═══════════════════════════════════════════════════════════════════ 2. 여러 가지 미분법
DC = "h3-1-diff2"
DC_B = {**HS, "prereq": ["미분계수", "지수·로그·삼각함수"], "ops": ["미분법"], "traps": ["합성함수 안쪽 미분 누락", "몫의 미분 순서"], "tags": ["지수로그 극한", "삼각 극한", "미분법"]}


def _dc1_rows():
    out = {}
    for a in range(1, 7):
        for b in range(1, 7):
            if a == b:
                continue
            v = Fraction(a, b)
            for kind, q, step in (("exp", f"[[lim(x, 0, frac(pow(e, {_sc(a)}x) − 1, {_sc(b)}x))]]", f"[[frac(pow(e, {_sc(a)}x) − 1, {_sc(a)}x)]] × [[frac({a}, {b})]], [[lim(t, 0, frac(pow(e, t) − 1, t))]] = 1"),
                                  ("ln", f"[[lim(x, 0, frac(ln(1 + {_sc(a)}x), {_sc(b)}x))]]", f"[[frac(ln(1 + {_sc(a)}x), {_sc(a)}x)]] × [[frac({a}, {b})]], [[lim(t, 0, frac(ln(1 + t), t))]] = 1"),
                                  ("mix", f"[[lim(x, 0, frac(pow(e, {_sc(a)}x) − 1, ln(1 + {_sc(b)}x)))]]", f"[[frac(pow(e, {_sc(a)}x) − 1, {_sc(a)}x)]] × [[frac({_sc(b)}x, ln(1 + {_sc(b)}x))]] × [[frac({a}, {b})]]")):
                r = _row(q, v, EXPR=q, KIND={"exp": "(eˣ − 1)/x → 1", "ln": "ln(1 + x)/x → 1", "mix": "두 기본 극한 결합"}[kind], STEP=step, RES=f"1 × [[frac({a}, {b})]] = {_fm(v)}")
                if r: out[f"{kind}{a}_{b}"] = r
    return _pick(out, 330)


DC1_ROWS = _dc1_rows()


def dc_t1():
    return T(DC, 1, DC_B, title="지수·로그함수의 극한 — (eˣ − 1)/x, ln(1 + x)/x",
        skill="lim (eᵃˣ − 1)/(bx) = a/b, lim ln(1 + ax)/(bx) = a/b를 기본 극한으로 계산하기", axis={"a, b": "1~6", "형태": "지수 / 로그 / 혼합"}, disc="기본 극한 꼴로 맞추기 위해 분모·분자에 같은 것을 곱하고 나누는가", diff=2,
        params=[{"name": "f", "values": {"in": list(DC1_ROWS)}}], table={"key": "f", "rows": DC1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="기본 극한 [[lim(x, 0, frac(pow(e, x) − 1, x))]] = 1, [[lim(x, 0, frac(ln(1 + x), x))]] = 1을 쓴다. 지수·진수의 계수 ax를 분모에도 만들어 (기본 극한) × (계수의 비) 꼴로 바꾼다. 이 문제는 {KIND} 유형이다.",
        sol2=[("{KIND}", "기본 극한"), ("{STEP}", "꼴 맞추기"), ("{RES}", None, ("{ans}", "극한값"))],
        sol3=["기본 극한이 1이 되도록 맞춘 뒤 남는 계수의 비만 확인한다. 따라서 극한값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 극한값은 {RES}이다.",
        rubric=[("꼴 맞추기", 3, "{STEP} 꼴로 변형했다.", "계수를 맞추지 않고 1로 두었으면 1점."), ("극한값", 2, "{ans}{eul(ans)} 구했다.", "비를 거꾸로 두었으면 인정하지 않는다.")],
        pitfalls=[("(eᵃˣ − 1)/x → 1로 둠(계수 a 누락)", "꼴 맞추기", "불인정"), ("a/b를 b/a로 뒤집음", "극한값", "불인정"), ("ln(1 + ax)를 ln(ax)로 봄", "꼴 맞추기", "불인정")])


def _dc2_rows():
    out = {}
    for a in range(1, 7):
        for b in range(1, 7):
            if a == b:
                continue
            v = Fraction(a, b)
            for kind, q, step in (("sin", f"[[lim(x, 0, frac(sin({_sc(a)}x), {_sc(b)}x))]]", f"[[frac(sin({_sc(a)}x), {_sc(a)}x)]] × [[frac({a}, {b})]]"),
                                  ("tan", f"[[lim(x, 0, frac(tan({_sc(a)}x), {_sc(b)}x))]]", f"[[frac(tan({_sc(a)}x), {_sc(a)}x)]] × [[frac({a}, {b})]]"),
                                  ("ss", f"[[lim(x, 0, frac(sin({_sc(a)}x), sin({_sc(b)}x)))]]", f"[[frac(sin({_sc(a)}x), {_sc(a)}x)]] × [[frac({_sc(b)}x, sin({_sc(b)}x))]] × [[frac({a}, {b})]]"),
                                  ("ts", f"[[lim(x, 0, frac(tan({_sc(a)}x), sin({_sc(b)}x)))]]", f"[[frac(tan({_sc(a)}x), {_sc(a)}x)]] × [[frac({_sc(b)}x, sin({_sc(b)}x))]] × [[frac({a}, {b})]]")):
                r = _row(q, v, EXPR=q, KIND="sin x/x → 1, tan x/x → 1", STEP=step, RES=f"1 × [[frac({a}, {b})]] = {_fm(v)}")
                if r: out[f"{kind}{a}_{b}"] = r
    for a in range(1, 6):
        for b in range(1, 5):
            v = Fraction(a * a, 2 * b)
            q = f"[[lim(x, 0, frac(1 − cos({_sc(a)}x), {_sc(b)}pow(x,2)))]]"
            r = _row(q, v, EXPR=q, KIND="1 − cos x = 2sin²(x/2) 또는 (1 − cos x)(1 + cos x) = sin²x", STEP=f"[[frac(1 − cos({_sc(a)}x), {_sc(b)}pow(x,2))]] = [[frac(pow(sin({_sc(a)}x), 2), {_sc(b)}pow(x,2)(1 + cos({_sc(a)}x)))]] → [[frac({a * a}, {b} × 2)]]", RES=f"[[frac({a * a}, {2 * b})]] = {_fm(v)}")
            if r: out[f"cos{a}_{b}"] = r
    return _pick(out, 330)


DC2_ROWS = _dc2_rows()


def dc_t2():
    return T(DC, 2, DC_B, title="삼각함수의 극한 — sin x/x, tan x/x, (1 − cos x)/x²",
        skill="lim sin(ax)/(bx) = a/b 등 기본 극한으로 계수의 비를 읽고, 1 − cos x는 sin²x/(1 + cos x)로 바꾸기", axis={"a, b": "1~6", "형태": "sin / tan / sin·sin / tan·sin / 1 − cos"}, disc="기본 극한 꼴로 맞춰 계수의 비를 정확히 남기는가", diff=2,
        params=[{"name": "f", "values": {"in": list(DC2_ROWS)}}], table={"key": "f", "rows": DC2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="기본 극한 [[lim(x, 0, frac(sin(x), x))]] = 1, [[lim(x, 0, frac(tan(x), x))]] = 1을 쓴다. 각의 계수 ax를 분모에도 만들어 기본 극한 × (계수의 비) 꼴로 바꾼다({KIND}).",
        sol2=[("{KIND}", "기본 극한"), ("{STEP}", "꼴 맞추기"), ("{RES}", None, ("{ans}", "극한값"))],
        sol3=["x → 0에서 sin(ax) ≈ ax, tan(ax) ≈ ax로 어림해 계수의 비와 맞는지 확인한다. 따라서 극한값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 극한값은 {RES}이다.",
        rubric=[("꼴 맞추기", 3, "{STEP} 꼴로 변형했다.", "계수를 맞추지 않았으면 1점."), ("극한값", 2, "{ans}{eul(ans)} 구했다.", "비를 거꾸로 두었으면 인정하지 않는다.")],
        pitfalls=[("sin(ax)/x → 1로 둠", "꼴 맞추기", "불인정"), ("(1 − cos x)/x² → 0으로 봄", "꼴 맞추기", "불인정"), ("a/b를 뒤집음", "극한값", "불인정")])


def _dc3_rows():
    out = {}
    fams = []      # (문면 f(x) 표기(마커 포함), sympy 식, x0, 규칙, 도함수 표기)
    for a in NZ(-3, 3):
        for b in NZ(-3, 3):
            fams.append((f"({_sc(a)}x {_sg(b)})[[pow(e, x)]]", (a * X + b) * sp.exp(X), 0, "곱의 미분법 (uv)' = u'v + uv'", f"f'(x) = {_sc(a)}eˣ + ({_sc(a)}x {_sg(b)})eˣ"))
            fams.append((f"[[pow(e, {_sc(a)}x) sin({_sc(b)}x)]]", sp.exp(a * X) * sp.sin(b * X), 0, "곱의 미분법 (uv)' = u'v + uv'", f"f'(x) = {_sc(a)}e^({_sc(a)}x) sin({_sc(b)}x) {_sgc(b)}e^({_sc(a)}x) cos({_sc(b)}x)"))
            fams.append((f"[[frac({_sc(a)}x {_sg(b)}, pow(x,2) + 1)]]", (a * X + b) / (X ** 2 + 1), 1, "몫의 미분법 (u/v)' = (u'v − uv')/v²", f"f'(x) = [[frac({_sc(a)}(pow(x,2) + 1) − ({_sc(a)}x {_sg(b)}) × 2x, pow(pow(x,2) + 1, 2))]]"))
            fams.append((f"[[ln({_sc(a)}pow(x,2) {_sg(b)}x + 1)]]", sp.log(a * X ** 2 + b * X + 1), 0, "합성함수의 미분법 (ln u)' = u'/u", f"f'(x) = [[frac({2 * a}x {_sg(b)}, {_sc(a)}pow(x,2) {_sg(b)}x + 1)]]"))
    for a in NZ(-3, 3):
        for b in NZ(-4, 4):
            for n in (3, 4, 5):
                fams.append((f"[[pow({_sc(a)}x {_sg(b)}, {n})]]", (a * X + b) ** n, 0, "합성함수의 미분법 (uⁿ)' = nuⁿ⁻¹u'", f"f'(x) = {n}({_sc(a)}x {_sg(b)})^{n - 1} × ({a}) = {n * a}({_sc(a)}x {_sg(b)})^{n - 1}"))
    for a in NZ(-3, 3):
        for b in NZ(-3, 3):
            fams.append((f"[[sin({_sc(a)}x) cos({_sc(b)}x)]]", sp.sin(a * X) * sp.cos(b * X), 0, "곱의 미분법", f"f'(x) = {_sc(a)}cos({_sc(a)}x)cos({_sc(b)}x) {_sgc(-b)}sin({_sc(a)}x)sin({_sc(b)}x)"))
            fams.append((f"[[tan({_sc(a)}x) + pow(e, {_sc(b)}x)]]", sp.tan(a * X) + sp.exp(b * X), 0, "(tan x)' = sec²x, (eᵏˣ)' = keᵏˣ", f"f'(x) = {_sc(a)}sec²({_sc(a)}x) {_sgc(b)}e^({_sc(b)}x)"))
    for fx, fexpr, x0, law, dfs in fams:
        d = sp.diff(fexpr, X).subs(X, x0)
        v = _rat(d)
        if v is None or v == 0:
            continue
        q = f"함수 f(x) = {fx}에 대하여 f'({x0})의 값을 구하시오."
        r = _row(q, v, Q=q, LAW=law, DFS=dfs, KIND="미분법")
        if r: out[f"f{len(out)}"] = r
    for a in NZ(-3, 3):
        for b in NZ(-4, 4):
            for t0 in (1, 2, -1, -2):
                v = Fraction(3 * t0 ** 2 + b, 2 * t0)
                q = f"매개변수 t로 나타낸 곡선 x = [[pow(t,2) {_sg(a)}]], y = [[pow(t,3) {_sg(b)}t]]에 대하여 t = {t0}일 때 [[dydx(y, x)]]의 값을 구하시오."
                r = _row(q, v, Q=q, LAW="매개변수 미분법 dy/dx = (dy/dt)/(dx/dt)", DFS=f"dx/dt = 2t, dy/dt = 3t² {_sg(b)} → [[dydx(y, x)]] = [[frac(3pow(t,2) {_sg(b)}, 2t)]]", KIND="매개변수")
                if r: out[f"p{a}_{b}_{t0}"] = r
    for (p, qv, rr) in ((3, 4, 5), (4, 3, 5), (-3, 4, 5), (3, -4, 5), (5, 12, 13), (12, 5, 13), (-5, 12, 13), (6, 8, 10), (8, -6, 10), (8, 15, 17), (15, 8, 17), (-8, 15, 17)):
        v = Fraction(-p, qv)
        q = f"곡선 [[pow(x,2) + pow(y,2) = {rr * rr}]] 위의 점 ({p}, {qv})에서의 [[dydx(y, x)]]의 값을 구하시오."
        r = _row(q, v, Q=q, LAW="음함수의 미분법 — 양변을 x로 미분: 2x + 2y·y' = 0", DFS=f"[[dydx(y, x)]] = [[-frac(x, y)]], 점 ({p}, {qv}) 대입", KIND="음함수")
        if r: out[f"i{p}_{qv}"] = r
    for (p, qv) in ((1, 2), (2, 1), (1, -1), (-1, 2), (2, -3), (1, 3), (3, 1), (-2, 1), (2, 3), (3, -2)):
        c = p ** 3 + qv ** 3
        v = Fraction(-p * p, qv * qv)
        q = f"곡선 [[pow(x,3) + pow(y,3) = {c}]] 위의 점 ({p}, {qv})에서의 [[dydx(y, x)]]의 값을 구하시오."
        r = _row(q, v, Q=q, LAW="음함수의 미분법 — 양변을 x로 미분: 3x² + 3y²·y' = 0", DFS=f"[[dydx(y, x)]] = [[-frac(pow(x,2), pow(y,2))]], 점 ({p}, {qv}) 대입", KIND="음함수")
        if r: out[f"j{p}_{qv}"] = r
    for a in range(0, 7):          # f'(x) = 3x² + a ≥ 0 → 단조, 역함수 존재
        for b in NZ(-5, 5):
            for x0 in (1, 2, -1):
                fp = 3 * x0 * x0 + a
                if fp <= 0:
                    continue
                y0 = x0 ** 3 + a * x0 + b
                v = Fraction(1, fp)
                fx = f"[[pow(x,3) {(_sgc(a) + 'x ') if a else ''}{_sg(b)}]]"
                q = f"함수 f(x) = {fx}의 역함수를 g(x)라 할 때, g'({y0})의 값을 구하시오."
                r = _row(q, v, Q=q, LAW="역함수의 미분법 g'(y₀) = 1/f'(x₀) (f(x₀) = y₀)", DFS=f"f({x0}) = {y0}이므로 x₀ = {x0}, f'(x) = 3x² {_sg(a) if a else ''}, f'({x0}) = {fp}".replace("3x² ,", "3x²,"), KIND="역함수")
                if r: out[f"v{a}_{b}_{x0}"] = r
    return _pick(out, 330)


DC3_ROWS = _dc3_rows()


def dc_t3():
    return T(DC, 3, DC_B, title="여러 가지 미분법 — 곱·몫·합성·매개변수·음함수·역함수",
        skill="미분법의 규칙을 골라 도함수(또는 dy/dx)를 구하고 주어진 점에서의 값 계산하기", axis={"규칙": "곱 / 몫 / 합성 / 매개변수 / 음함수 / 역함수", "점": "x = 0, 1 또는 주어진 점"}, disc="함수의 구조에 맞는 미분법을 고르고 안쪽 미분·역수 관계를 빠뜨리지 않는가", diff=3,
        params=[{"name": "f", "values": {"in": list(DC3_ROWS)}}], table={"key": "f", "rows": DC3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 함수의 구조(곱·몫·합성·매개변수·음함수·역함수)에 맞는 규칙을 고른 뒤 주어진 점을 대입한다.",
        sol2=[("{LAW}", "미분법 고르기"), ("{DFS}", "도함수"), ("대입: {ans}", None, ("{ans}", "값"))],
        sol3=["안쪽 함수의 미분(합성), u'v + uv'의 두 항(곱), 분모의 제곱(몫), 역수 관계(역함수)를 빠뜨리지 않았는지 확인한다. 따라서 값은 {ans}이다.", "{DFS}", "답 {ans}"],
        model="{LAW}에 따라 {DFS}이고, 주어진 점을 대입하면 {ans}이다.",
        rubric=[("미분법", 3, "{DFS} 꼴로 도함수를 구했다.", "한 항을 빠뜨렸으면 1점."), ("대입", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("합성함수에서 안쪽 미분을 빠뜨림", "미분법", "불인정"), ("몫의 미분에서 분자의 순서를 바꿈", "미분법", "불인정"), ("역함수의 미분계수를 f'(x₀)로 답함(역수 아님)", "대입", "불인정")])


def _dc4_rows():
    out = {}
    curves = [("pow(e, x)", sp.exp(X), 0), ("ln(x)", sp.log(X), 1), ("x pow(e, x)", X * sp.exp(X), 0), ("pow(e, x)(x + 1)", sp.exp(X) * (X + 1), 0), ("x ln(x)", X * sp.log(X), 1), ("sin(x) + cos(x)", sp.sin(X) + sp.cos(X), 0),
              ("pow(e, 2x)", sp.exp(2 * X), 0), ("ln(x) + x", sp.log(X) + X, 1), ("pow(e, x) − x", sp.exp(X) - X, 0), ("frac(x, x + 1)", X / (X + 1), 0), ("frac(2x, pow(x,2) + 1)", 2 * X / (X ** 2 + 1), 0), ("ln(2x + 1)", sp.log(2 * X + 1), 0), ("ln(pow(x,2) + 1)", sp.log(X ** 2 + 1), 1), ("pow(e, x) sin(x)", sp.exp(X) * sp.sin(X), 0), ("tan(x) + 1", sp.tan(X) + 1, 0)]
    for k in (1, 2, 3, -1, -2):
        for cs, ce, x0 in curves:
            f = k * ce
            y0, m = _rat(f.subs(X, x0)), _rat(sp.diff(f, X).subs(X, x0))
            if y0 is None or m is None or m == 0:
                continue
            n = y0 - m * x0
            multi = " + " in cs or " − " in cs
            disp = cs if k == 1 else ((f"-({cs})" if multi else f"-{cs}") if k == -1 else (f"{k}({cs})" if multi else f"{k} {cs}"))
            for kk, ask, v in (("sum", "m + n", m + n), ("y", "y절편", n), ("x", "x절편", -n / m)):
                if v == 0:
                    continue
                q = f"곡선 y = [[{disp}]] 위의 점 ({x0}, {_fm(y0)})에서의 접선 {ask}"
                r = _row(q, v, CURVE=disp, X0=x0, Y0=_fm(y0), M=_fm(m), MC=("" if m == 1 else ("-" if m == -1 else _fm(m))), NN=_fm(n), NS=(f"+ {_fm(n)}" if n > 0 else f"− {_fm(-n)}"), ASK=ask, KIND=kk)
                if r: out[f"{k}_{cs}_{kk}"] = r
    return _pick(out, 300)


DC4_ROWS = _dc4_rows()


def dc_t4():
    return T(DC, 4, DC_B, title="접선의 방정식 — 지수·로그·삼각·분수함수",
        skill="접점에서의 미분계수를 기울기로 하여 y − y₀ = f'(x₀)(x − x₀)를 세우고 절편 읽기", axis={"곡선": "eˣ, ln x, xeˣ, sin x + cos x, x/(x+1) 등 15가지 × 상수배", "묻는 것": "m + n / y절편 / x절편"}, disc="여러 가지 미분법으로 기울기를 구해 접점을 지나는 직선을 세우는가", diff=3,
        params=[{"name": "f", "values": {"in": list(DC4_ROWS)}}], table={"key": "f", "rows": DC4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="접선의 기울기는 접점에서의 미분계수 f'({X0}) = {M}이고, 접선은 접점 ({X0}, {Y0})를 지나므로 y − {pn(Y0)} = {M}(x − {pn(X0)}), 즉 y = {MC}x {NS}이다.",
        sol2=[("f'({X0}) = {M}", "기울기"), ("y = {MC}x {NS} (y절편 {NN}, x절편 = −n/m)", "접선"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["접선에 x = {X0}를 넣으면 {Y0}{ika(Y0)} 나와 접점을 지난다. 따라서 {ASK} = {ans}이다.", "y = {MC}x {NS}", "{ASK} = {ans}"],
        model="기울기 f'({X0}) = {M}, 접점 ({X0}, {Y0})이므로 접선은 y = {MC}x {NS}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("기울기·접선", 3, "m = {M}, 접선 y = {MC}x {NS}{eul(NN)} 세웠다.", "미분 실수면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "절편 계산 실수면 1점.")],
        pitfalls=[("접점의 y좌표를 0으로 둠", "기울기·접선", "불인정"), ("(xeˣ)'을 eˣ로 둠(곱의 미분 누락)", "기울기·접선", "불인정"), ("x절편·y절편 혼동", "답", "부분")])


def _dc4_fix(t):
    for k, row in t["table"]["rows"].items():
        row["Q"] = f"곡선 y = [[{row['CURVE']}]] 위의 점 ({row['X0']}, {row['Y0']})에서의 접선의 방정식이 y = mx + n일 때, {'상수 m, n에 대하여 m + n의 값' if row['KIND'] == 'sum' else ('이 접선의 y절편' if row['KIND'] == 'y' else '이 접선의 x절편')}을 구하시오."
    return t


def _dc5_rows():
    out = {}
    for a in (1, 4, 9, 16, 25, 36, 49, 64):
        s = int(math.isqrt(a))
        v = 2 * s
        q = f"x > 0에서 함수 f(x) = x + [[frac({a}, x)]]의 극솟값"
        r = _row(q, v, Q=f"x > 0에서 함수 f(x) = x + [[frac({a}, x)]]의 극솟값을 구하시오.", DF=f"f'(x) = 1 − [[frac({a}, pow(x,2))]] = [[frac(pow(x,2) − {a}, pow(x,2))]]", CRIT=f"f'(x) = 0에서 x = {s} (x > 0), x < {s}에서 f' < 0, x > {s}에서 f' > 0이므로 극소", RES=f"f({s}) = {s} + {s} = {v}", ASK="극솟값")
        if r: out[f"a{a}"] = r
        v2 = Fraction(1, 2 * s)
        q2 = f"함수 f(x) = [[frac(x, pow(x,2) + {a})]]의 극댓값"
        r2 = _row(q2, v2, Q=f"함수 f(x) = [[frac(x, pow(x,2) + {a})]]의 극댓값을 구하시오.", DF=f"f'(x) = [[frac({a} − pow(x,2), pow(pow(x,2) + {a}, 2))]]", CRIT=f"f'(x) = 0에서 x = ±{s}, x = {s}에서 f'의 부호가 + → −이므로 극대", RES=f"f({s}) = [[frac({s}, {2 * a})]] = {_fm(v2)}", ASK="극댓값")
        if r2: out[f"b{a}"] = r2
    for kk in range(1, 13):
        v = -kk * kk
        q = f"함수 f(x) = [[pow(e, 2x)]] − {2 * kk}[[pow(e, x)]]의 극솟값"
        r = _row(q, v, Q=f"함수 f(x) = [[pow(e, 2x)]] − {2 * kk}[[pow(e, x)]]의 극솟값을 구하시오.", DF=f"f'(x) = 2[[pow(e, 2x)]] − {2 * kk}[[pow(e, x)]] = 2[[pow(e, x)]]([[pow(e, x)]] − {kk})", CRIT=f"f'(x) = 0에서 [[pow(e, x)]] = {kk}, 즉 x = ln {kk}; 그 좌우에서 f'의 부호가 − → +이므로 극소", RES=f"f(ln {kk}) = {kk}² − {2 * kk} × {kk} = {v}", ASK="극솟값")
        if r: out[f"c{kk}"] = r
    for a in (1, 4, 9, 16, 25, 36, 49):
        s = int(math.isqrt(a))
        v = 2 * s
        q = f"x > 0에서 함수 f(x) = x² + [[frac({a}, pow(x,2))]]의 극솟값"
        r = _row(q, v, Q=f"x > 0에서 함수 f(x) = x² + [[frac({a}, pow(x,2))]]의 극솟값을 구하시오.", DF=f"f'(x) = 2x − [[frac({2 * a}, pow(x,3))]] = [[frac(2(pow(x,4) − {a}), pow(x,3))]]", CRIT=f"f'(x) = 0에서 x⁴ = {a}, x = [[sqrt({s})]] (x > 0)이고 좌우에서 f'의 부호가 − → +이므로 극소", RES=f"f([[sqrt({s})]]) = {s} + {s} = {v}", ASK="극솟값")
        if r: out[f"e{a}"] = r
    for a in range(1, 13):
        for b in range(1, 13):
            # f(x) = a x + b/x (x>0): min 2√(ab)
            s2 = a * b
            s = int(math.isqrt(s2))
            if s * s != s2:
                continue
            v = 2 * s
            q = f"x > 0에서 함수 f(x) = {a}x + [[frac({b}, x)]]의 극솟값"
            r = _row(q, v, Q=f"x > 0에서 함수 f(x) = {_sc(a)}x + [[frac({b}, x)]]의 극솟값을 구하시오.", DF=f"f'(x) = {a} − [[frac({b}, pow(x,2))]]", CRIT=f"f'(x) = 0에서 x² = [[frac({b}, {a})]], x = {_fm(Fraction(s, a))} (x > 0)이고 좌우에서 f'의 부호가 − → +이므로 극소", RES=f"f({_fm(Fraction(s, a))}) = {s} + {s} = {v}", ASK="극솟값")
            if r: out[f"d{a}_{b}"] = r
    return out


DC5_ROWS = _dc5_rows()


def dc_t5():
    return T(DC, 5, DC_B, title="여러 가지 함수의 극값 — 분수·지수함수",
        skill="f'(x) = 0의 근 좌우에서 부호 변화를 확인해 극댓값·극솟값 구하기", axis={"함수": "x + a/x, x/(x² + a), e²ˣ − 2keˣ, ax + b/x", "묻는 것": "극솟값 / 극댓값"}, disc="정의역 조건(x > 0)을 지키고 부호 변화로 극대·극소를 판단하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(DC5_ROWS)}}], table={"key": "f", "rows": DC5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="극값은 f'(x) = 0이 되는 점 중 좌우에서 f'의 부호가 바뀌는 점에서 생긴다. 도함수를 구해 부호를 조사한다: {DF}.",
        sol2=[("{DF}", "도함수"), ("{CRIT}", "부호 변화"), ("{RES}", None, ("{ans}", "{ASK}"))],
        sol3=["극점 좌우의 값을 넣어 f'의 부호가 실제로 바뀌는지 확인한다. 따라서 {ASK}은 {ans}이다.", "{CRIT}", "{ASK} {ans}"],
        model="{DF}, {CRIT}. {RES}이므로 {ASK}은 {ans}이다.",
        rubric=[("도함수·극점", 3, "{DF} 꼴로 구하고 극점을 찾았다.", "부호 변화 확인이 없으면 1점."), ("극값", 2, "{ASK} {ans}{eul(ans)} 구했다.", "함숫값 계산 실수면 1점.")],
        pitfalls=[("f'(x) = 0의 근을 극값으로 답함", "극값", "불인정"), ("정의역 밖의 근을 채택(x < 0)", "도함수·극점", "부분"), ("e^(2 ln k) 계산 실수", "극값", "부분")])


DC_SEED = SEED(DC, category="해석", title="여러 가지 미분법 — 지수로그 극한·삼각 극한·미분법(곱·몫·합성·매개변수·음함수·역함수)·접선·극값", unit_id="h3-1", concept_ids=["h3-1-05", "h3-1-06", "h3-1-07", "h3-1-08", "h3-1-09", "h3-1-10", "h3-1-11", "h3-1-12"],
               schema_name="여러 가지 함수의 미분", note="도함수 값은 sympy 로 계산해 유리수인 것만 행에 넣었다. e·π 는 마커 안 상수(e, pi).",
               templates=[dc_t1(), dc_t2(), dc_t3(), _dc4_fix(dc_t4()), dc_t5()])


# ═══════════════════════════════════════════════════════════════════ 3. 여러 가지 적분법
IC = "h3-1-integ2"
IC_B = {**HS, "prereq": ["정적분", "미분법"], "ops": ["적분법"], "traps": ["치환 후 적분 구간", "부분적분의 u·v 선택"], "tags": ["치환적분", "부분적분", "정적분과 급수", "넓이"]}


def _ic1_rows():
    out = {}
    items = []
    for a in (2, 3, 4, 5, 8, 9):
        items.append(("0", f"ln({a})", "pow(e, x)", a - 1, "eˣ의 원시함수는 eˣ", f"[[pow(e, ln({a}))]] − [[pow(e, 0)]] = {a} − 1"))
        items.append(("0", f"ln({a})", "pow(e, 2x)", Fraction(a * a - 1, 2), "e²ˣ의 원시함수는 ½e²ˣ", f"[[frac(1,2)]]([[pow(e, 2ln({a}))]] − 1) = [[frac(1,2)]]({a * a} − 1)"))
    for k in (1, 2, 3, 4):
        items.append(("1", f"pow(e, {k})" if k > 1 else "e", "frac(1, x)", k, "1/x의 원시함수는 ln|x|", f"ln [[pow(e, {k})]] − ln 1 = {k}"))
    items.append(("0", "pi", "sin(x)", 2, "sin x의 원시함수는 −cos x", "−cos π + cos 0 = 2"))
    items.append(("0", "frac(pi, 2)", "cos(x)", 1, "cos x의 원시함수는 sin x", "sin [[frac(pi, 2)]] − sin 0 = 1"))
    items.append(("0", "frac(pi, 4)", "pow(sec(x), 2)", 1, "sec²x의 원시함수는 tan x", "tan [[frac(pi, 4)]] − tan 0 = 1"))
    items.append(("0", "frac(pi, 2)", "sin(2x)", 1, "sin 2x의 원시함수는 −½cos 2x", "[[frac(1,2)]](−cos π + cos 0) = 1"))
    items.append(("0", "frac(pi, 6)", "cos(3x)", Fraction(1, 3), "cos 3x의 원시함수는 ⅓sin 3x", "[[frac(1,3)]](sin [[frac(pi, 2)]] − sin 0) = [[frac(1,3)]]"))
    items.append(("0", "frac(pi, 3)", "sin(3x)", Fraction(2, 3), "sin 3x의 원시함수는 −⅓cos 3x", "[[frac(1,3)]](−cos π + cos 0) = [[frac(2,3)]]"))
    for lo, hi, integrand, v, law, step in items:
        for c in (1, 2, 3, 4, 5, 6):
            e2 = f"dinteg({lo}, {hi}, {_sc(c)}{integrand}, x)" if integrand[0] != "p" or c == 1 else f"dinteg({lo}, {hi}, {c} {integrand}, x)"
            if c > 1 and integrand.startswith(("sin", "cos", "frac")):
                e2 = f"dinteg({lo}, {hi}, {c} {integrand}, x)"
            q = f"[[{e2}]]의 값"
            r = _row(q, c * Fraction(v), EXPR=f"[[{e2}]]", LAW=law, STEP=(step if c == 1 else f"{c} × ({step})"))
            if r: out[f"i{len(out)}"] = r
    return _pick(out, 300)


IC1_ROWS = _ic1_rows()


def ic_t1():
    return T(IC, 1, IC_B, title="여러 가지 함수의 정적분 — 지수·로그·삼각",
        skill="eˣ, 1/x, sin x, cos x, sec²x의 원시함수를 알고 정적분 계산하기", axis={"피적분함수": "eˣ, e²ˣ, 1/x, c sin x, c cos x, c sec²x, c sin 2x", "구간": "[0, ln a], [1, eᵏ], [0, π] 등"}, disc="원시함수를 정확히 알고 e^(ln a) = a, 삼각함수 특수각 값을 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(IC1_ROWS)}}], table={"key": "f", "rows": IC1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="{LAW}. 원시함수 F(x)를 구해 F(위끝) − F(아래끝)을 계산한다. e^(ln a) = a, ln e = 1, 특수각의 삼각함수 값을 쓴다.",
        sol2=[("{LAW}", "원시함수"), ("{STEP}", "위끝 − 아래끝"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["원시함수를 미분하면 피적분함수가 되는지 확인한다. 따라서 값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} = {ans}이다.",
        rubric=[("원시함수", 3, "{LAW}{ro(ans)} 원시함수를 세웠다.", "부호(−cos x)를 틀리면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "e^(ln a), 특수각 값 실수면 1점.")],
        pitfalls=[("sin x의 원시함수를 cos x로 둠", "원시함수", "불인정"), ("e²ˣ의 원시함수에서 ½을 빠뜨림", "원시함수", "부분"), ("e^(ln a)를 그대로 둠", "계산", "부분")])


def _ic2_rows():
    out = {}
    for a in (1, 2, 3):
        for n in (2, 3, 4):
            v = Fraction((1 + a) ** (n + 1) - a ** (n + 1), n + 1)
            expr = f"dinteg(0, 1, 2x pow(pow(x,2) + {a}, {n}), x)"
            r = _row(f"[[{expr}]]", v, EXPR=f"[[{expr}]]", SUB=f"x² + {a} = t로 놓으면 2x dx = dt, x: 0 → 1일 때 t: {a} → {a + 1}", NEW=f"[[dinteg({a}, {a + 1}, pow(t, {n}), t)]]", RES=f"[[frac(1, {n + 1})]]([[pow({a + 1}, {n + 1})]] − [[pow({a}, {n + 1})]]) = {_fm(v)}")
            if r: out[f"p{a}_{n}"] = r
    for k in (1, 2, 3, 4, 5):
        v = Fraction(1, k + 1)
        for c in (1, 2, 3, 6):
            vc = c * v
            expr = f"dinteg(1, e, {_sc(c)}frac(pow(ln(x), {k}), x), x)"
            r = _row(f"[[{expr}]]", vc, EXPR=f"[[{expr}]]", SUB=f"ln x = t로 놓으면 (1/x)dx = dt, x: 1 → e일 때 t: 0 → 1", NEW=f"{_sc(c)}[[dinteg(0, 1, pow(t, {k}), t)]]", RES=f"{c} × [[frac(1, {k + 1})]] = {_fm(vc)}")
            if r: out[f"l{k}_{c}"] = r
            expr2 = f"dinteg(0, frac(pi, 2), {_sc(c)}pow(sin(x), {k}) cos(x), x)"
            r2 = _row(f"[[{expr2}]]", vc, EXPR=f"[[{expr2}]]", SUB=f"sin x = t로 놓으면 cos x dx = dt, x: 0 → π/2일 때 t: 0 → 1", NEW=f"{_sc(c)}[[dinteg(0, 1, pow(t, {k}), t)]]", RES=f"{c} × [[frac(1, {k + 1})]] = {_fm(vc)}")
            if r2: out[f"s{k}_{c}"] = r2
            expr3 = f"dinteg(0, frac(pi, 2), {_sc(c)}pow(cos(x), {k}) sin(x), x)"
            r3 = _row(f"[[{expr3}]]", vc, EXPR=f"[[{expr3}]]", SUB=f"cos x = t로 놓으면 −sin x dx = dt, x: 0 → π/2일 때 t: 1 → 0", NEW=f"{_sc(c)}[[dinteg(0, 1, pow(t, {k}), t)]]", RES=f"{c} × [[frac(1, {k + 1})]] = {_fm(vc)}")
            if r3: out[f"c{k}_{c}"] = r3
    for a in (1, 2, 3, 4):
        # e^x (e^x + a)^n 형태: t = e^x + a, x: 0→ln2 → t: 1+a → 2+a
        for n in (1, 2, 3):
            v = Fraction((2 + a) ** (n + 1) - (1 + a) ** (n + 1), n + 1)
            expr = f"dinteg(0, ln(2), pow(e, x) pow(pow(e, x) + {a}, {n}), x)"
            r = _row(f"[[{expr}]]", v, EXPR=f"[[{expr}]]", SUB=f"eˣ + {a} = t로 놓으면 eˣ dx = dt, x: 0 → ln 2일 때 t: {1 + a} → {2 + a}", NEW=f"[[dinteg({1 + a}, {2 + a}, pow(t, {n}), t)]]", RES=f"[[frac(1, {n + 1})]]([[pow({2 + a}, {n + 1})]] − [[pow({1 + a}, {n + 1})]]) = {_fm(v)}")
            if r: out[f"e{a}_{n}"] = r
    return _pick(out, 300)


IC2_ROWS = _ic2_rows()


def ic_t2():
    return T(IC, 2, IC_B, title="치환적분법 — 안쪽 함수를 t로 놓기",
        skill="f(g(x))g'(x) 꼴을 찾아 g(x) = t로 치환하고 적분 구간도 t의 값으로 바꾸기", axis={"형태": "2x(x² + a)ⁿ, (ln x)ᵏ/x, sinᵏx cos x, cosᵏx sin x, eˣ(eˣ + a)ⁿ"}, disc="치환 후 dx와 구간을 함께 바꾸는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IC2_ROWS)}}], table={"key": "f", "rows": IC2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="피적분함수에 (안쪽 함수)와 (안쪽 함수의 도함수)가 함께 있으면 안쪽 함수를 t로 치환한다. {SUB}. 구간을 바꾼 뒤 t에 대한 정적분으로 계산한다.",
        sol2=[("{SUB}", "치환"), ("= {NEW}", "t의 정적분"), ("{RES}", None, ("{ans}", "값"))],
        sol3=["치환한 뒤 적분 구간을 t의 값으로 바꾸었는지, dt = g'(x)dx의 계수를 맞췄는지 확인한다. 따라서 값은 {ans}이다.", "{NEW}", "답 {ans}"],
        model="{SUB}이므로 주어진 정적분은 {NEW} = {RES}이다. 따라서 값은 {ans}이다.",
        rubric=[("치환·구간", 3, "{NEW} 꼴로 바꿨다.", "구간을 바꾸지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "거듭제곱 계산 실수면 1점.")],
        pitfalls=[("치환 후 적분 구간을 그대로 둠", "치환·구간", "불인정"), ("dt = g'(x)dx의 계수를 빠뜨림", "치환·구간", "부분"), ("cos x = t 치환에서 부호(−)로 구간이 뒤집힘을 놓침", "계산", "부분")])


def _ic3_rows():
    out = {}
    for c in (1, 2, 3, 4, 5, 6):
        for d in NZ(-6, 6):
            items = [(f"dinteg(0, 1, {_sc(c)}x pow(e, x) {_sg(d)}, x)", c + d, "u = x, v' = eˣ (상수항은 따로 적분)", f"{_sc(c)}([x eˣ]₀¹ − [[dinteg(0, 1, pow(e, x), x)]]) {_sg(d)} = {_sc(c)}(e − (e − 1)) {_sg(d)}", f"{c} {_sg(d)}"),
                     (f"dinteg(1, e, {_sc(c)}ln(x) + frac({d}, x), x)" if d > 0 else f"dinteg(1, e, {_sc(c)}ln(x) − frac({-d}, x), x)", c + d, "u = ln x, v' = 1 (1/x 항은 ln|x|로 적분)", f"{_sc(c)}([x ln x]₁ᵉ − [[dinteg(1, e, 1, x)]]) {_sgc(d)}[ln x]₁ᵉ = {_sc(c)}(e − (e − 1)) {_sg(d)}", f"{c} {_sg(d)}"),
                     (f"dinteg(0, frac(pi, 2), {_sc(c)}x sin(x) {_sgc(d)}cos(x), x)", c + d, "u = x, v' = sin x (cos x 항은 sin x로 적분)", f"{_sc(c)}([−x cos x]₀^(π/2) + [[dinteg(0, frac(pi, 2), cos(x), x)]]) {_sgc(d)}[sin x]₀^(π/2) = {_sc(c)}(0 + 1) {_sg(d)}", f"{c} {_sg(d)}")]
            for expr, v, uv, step, res in items:
                r = _row(f"[[{expr}]]", v, EXPR=f"[[{expr}]]", UV=uv, STEP=step, RES=f"{res} = {v}")
                if r: out[f"{c}_{d}_{expr[:24]}"] = r
        expr = f"dinteg(0, pi, {_sc(c)}x cos(x), x)"
        r = _row(f"[[{expr}]]", -2 * c, EXPR=f"[[{expr}]]", UV="u = x, v' = cos x", STEP=f"{_sc(c)}([x sin x]₀^π − [[dinteg(0, pi, sin(x), x)]]) = {_sc(c)}(0 − 2)", RES=f"{c} × (−2) = {-2 * c}")
        if r: out[f"{c}_cos"] = r
    return _pick(out, 300)


IC3_ROWS = _ic3_rows()


def ic_t3():
    return T(IC, 3, IC_B, title="부분적분법 — ∫uv' = uv − ∫u'v",
        skill="다항식 × (지수·삼각), ln x 꼴에서 u, v'를 골라 부분적분하기", axis={"형태": "x eˣ, ln x, x cos x, x sin x × 상수배"}, disc="미분하면 간단해지는 쪽을 u로 잡고 경계값을 정확히 계산하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IC3_ROWS)}}], table={"key": "f", "rows": IC3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="부분적분법 ∫uv'dx = uv − ∫u'v dx에서 미분하면 간단해지는 것(x, ln x)을 u, 적분하기 쉬운 것(eˣ, sin x, cos x, 1)을 v'로 잡는다. 여기서는 {UV}.",
        sol2=[("{UV}", "u, v' 선택"), ("{STEP}", "부분적분"), ("{RES}", None, ("{ans}", "값"))],
        sol3=["uv의 경계값과 남은 적분의 부호를 다시 확인한다. 따라서 값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{UV}로 부분적분하면 {STEP}이므로 {RES}이다. 따라서 값은 {ans}이다.",
        rubric=[("부분적분", 3, "{STEP} 꼴로 계산했다.", "u, v'를 바꿔 잡아 더 복잡해졌으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "경계값 실수면 1점.")],
        pitfalls=[("ln x를 v'로 잡음", "부분적분", "불인정"), ("uv − ∫u'v의 부호를 +로 둠", "부분적분", "불인정"), ("경계값 대입 실수", "계산", "부분")])


def _ic4_rows():
    out = {}
    for m in (1, 2, 3, 4):
        for kind in ("01", "12", "02"):
            if kind == "01":
                expr = f"lim(n, inf, sum(k, 1, n, frac(pow(k, {m}), pow(n, {m + 1}))))" if m > 1 else "lim(n, inf, sum(k, 1, n, frac(k, pow(n, 2))))"
                v = Fraction(1, m + 1)
                integ = f"[[dinteg(0, 1, pow(x, {m}), x)]]"
                step = f"[[frac(1, n)]] × [[sum(k, 1, n, pow(frac(k, n), {m}))]] 꼴이므로 x = k/n, dx = 1/n, 구간 [0, 1]"
            elif kind == "12":
                expr = f"lim(n, inf, frac(1, n) sum(k, 1, n, pow(1 + frac(k, n), {m})))"
                v = Fraction(2 ** (m + 1) - 1, m + 1)
                integ = f"[[dinteg(1, 2, pow(x, {m}), x)]]"
                step = "x = 1 + k/n, dx = 1/n, 구간 [1, 2]"
            else:
                expr = f"lim(n, inf, frac(2, n) sum(k, 1, n, pow(frac(2k, n), {m})))"
                v = Fraction(2 ** (m + 1), m + 1)
                integ = f"[[dinteg(0, 2, pow(x, {m}), x)]]"
                step = "x = 2k/n, dx = 2/n, 구간 [0, 2]"
            for c in (1, 2, 3, 6):
                vc = c * v
                e2 = expr if c == 1 else expr.replace("lim(n, inf, ", f"lim(n, inf, {c} ", 1)
                r = _row(f"[[{e2}]]", vc, EXPR=f"[[{e2}]]", STEP=step, INT=(integ if c == 1 else f"{c}{integ}"), RES=f"{c} × {_fm(v)} = {_fm(vc)}" if c > 1 else f"= {_fm(v)}")
                if r: out[f"{m}_{kind}_{c}"] = r
    return out


IC4_ROWS = _ic4_rows()


def ic_t4():
    return T(IC, 4, IC_B, title="정적분과 급수의 합 — lim ∑ f(xₖ)Δx",
        skill="합의 극한을 x = a + k(b − a)/n, Δx = (b − a)/n으로 읽어 정적분으로 바꾸기", axis={"f": "xᵐ (m = 1, 2, 3)", "구간": "[0, 1], [1, 2], [0, 2]", "상수배": "1~6"}, disc="k/n 꼴을 x로, 1/n 꼴을 dx로 읽어 구간을 정확히 잡는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IC4_ROWS)}}], table={"key": "f", "rows": IC4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="구분구적법을 거꾸로 읽는다: [[lim(n, inf, sum(k, 1, n, f(a + frac(k(b − a), n)) frac(b − a, n)))]] = [[dinteg(a, b, f(x), x)]]. {STEP}이므로 주어진 극한은 {INT}이다.",
        sol2=[("{STEP}", "x, dx 읽기"), ("= {INT}", "정적분으로"), ("{RES}", None, ("{ans}", "값"))],
        sol3=["n이 클 때의 합을 직사각형 넓이의 합으로 보아 구간과 함수가 맞는지 확인한다. 따라서 값은 {ans}이다.", "{INT}", "답 {ans}"],
        model="{STEP}이므로 극한은 {INT}이고 그 값은 {RES}이다. 따라서 답은 {ans}이다.",
        rubric=[("정적분으로 옮기기", 3, "{INT} 꼴로 옮겼다.", "구간을 잘못 잡았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "적분 계산 실수면 1점.")],
        pitfalls=[("구간을 항상 [0, 1]로 둠", "정적분으로 옮기기", "불인정"), ("Δx = 2/n을 1/n으로 봄", "정적분으로 옮기기", "부분"), ("적분 계산 실수", "계산", "부분")])


def _ic5_rows():
    out = {}
    items = [("[[pow(e, x)]]", "x = 0, x = ln 3", Fraction(2), "dinteg(0, ln(3), pow(e, x), x)", "= [[pow(e, ln(3))]] − 1 = 3 − 1"), ("[[pow(e, x)]]", "x = 0, x = ln 5", Fraction(4), "dinteg(0, ln(5), pow(e, x), x)", "= 5 − 1"),
             ("[[frac(1, x)]]", "x = 1, x = e", Fraction(1), "dinteg(1, e, frac(1, x), x)", "= ln e − ln 1 = 1"), ("[[frac(1, x)]]", "x = 1, x = e²", Fraction(2), "dinteg(1, pow(e, 2), frac(1, x), x)", "= ln e² = 2"), ("[[frac(1, x)]]", "x = e, x = e³", Fraction(2), "dinteg(e, pow(e, 3), frac(1, x), x)", "= 3 − 1 = 2"),
             ("[[sin(x)]]", "x = 0, x = π", Fraction(2), "dinteg(0, pi, sin(x), x)", "= −cos π + cos 0 = 2"), ("[[cos(x)]]", "x = 0, x = [[frac(pi, 2)]]", Fraction(1), "dinteg(0, frac(pi, 2), cos(x), x)", "= sin [[frac(pi, 2)]] − sin 0 = 1"), ("[[sin(x)]]", "x = 0, x = 2π", Fraction(4), "2 dinteg(0, pi, sin(x), x)", "= 2 × 2 = 4 (x축 아래 부분은 부호를 바꿔 더함)"),
             ("[[sqrt(x)]]", "x = 0, x = 4", Fraction(16, 3), "dinteg(0, 4, sqrt(x), x)", "= [[frac(2,3)]] × [[pow(4, frac(3,2))]] = [[frac(16,3)]]"), ("[[sqrt(x)]]", "x = 0, x = 9", Fraction(18), "dinteg(0, 9, sqrt(x), x)", "= [[frac(2,3)]] × 27 = 18"), ("[[sqrt(x)]]", "x = 1, x = 4", Fraction(14, 3), "dinteg(1, 4, sqrt(x), x)", "= [[frac(2,3)]](8 − 1) = [[frac(14,3)]]"),
             ("[[frac(1, pow(x,2))]]", "x = 1, x = 2", Fraction(1, 2), "dinteg(1, 2, frac(1, pow(x,2)), x)", "= −[[frac(1,2)]] + 1 = [[frac(1,2)]]"), ("[[frac(1, pow(x,2))]]", "x = 1, x = 4", Fraction(3, 4), "dinteg(1, 4, frac(1, pow(x,2)), x)", "= −[[frac(1,4)]] + 1 = [[frac(3,4)]]"), ("[[frac(1, pow(x,2))]]", "x = 2, x = 6", Fraction(1, 3), "dinteg(2, 6, frac(1, pow(x,2)), x)", "= −[[frac(1,6)]] + [[frac(1,2)]] = [[frac(1,3)]]"),
             ("[[ln(x)]]", "x = 1, x = e", Fraction(1), "dinteg(1, e, ln(x), x)", "= [x ln x − x]₁ᵉ = (e − e) − (0 − 1) = 1"), ("[[pow(e, 2x)]]", "x = 0, x = ln 2", Fraction(3, 2), "dinteg(0, ln(2), pow(e, 2x), x)", "= [[frac(1,2)]](4 − 1) = [[frac(3,2)]]"), ("[[pow(e, -x)]]", "x = 0, x = ln 2", Fraction(1, 2), "dinteg(0, ln(2), pow(e, -x), x)", "= −[[frac(1,2)]] + 1 = [[frac(1,2)]]"),
             ("[[sin(2x)]]", "x = 0, x = [[frac(pi, 2)]]", Fraction(1), "dinteg(0, frac(pi, 2), sin(2x), x)", "= [[frac(1,2)]](−cos π + 1) = 1"), ("[[pow(sec(x), 2)]]", "x = 0, x = [[frac(pi, 4)]]", Fraction(1), "dinteg(0, frac(pi, 4), pow(sec(x), 2), x)", "= tan [[frac(pi, 4)]] − 0 = 1"), ("[[frac(2, x)]]", "x = 1, x = e", Fraction(2), "dinteg(1, e, frac(2, x), x)", "= 2 ln e = 2")]
    for c in (1, 2, 3):
        for curve, lines, v, integ, step in items:
            vc = c * v
            cs = curve if c == 1 else f"{c}{curve}" if not curve.startswith("[[frac") else f"{c}{curve}"
            q = f"곡선 y = {cs}, x축 및 두 직선 {lines}로 둘러싸인 부분의 넓이"
            r = _row(q, vc, Q=f"곡선 y = {cs}, x축 및 두 직선 {lines}{'로' if lines.endswith(']]') else _ro(lines)} 둘러싸인 부분의 넓이를 구하시오.", INT=(f"[[{integ}]]" if c == 1 else f"{c}[[{integ}]]"), STEP=(step if c == 1 else f"{c} × ({step[2:]})"), CURVE=cs)
            if r: out[f"{c}_{len(out)}"] = r
    return out


IC5_ROWS = _ic5_rows()


def ic_t5():
    return T(IC, 5, IC_B, title="넓이 — 지수·로그·삼각·무리함수와 x축 사이",
        skill="구간에서 함수의 부호를 확인하고 ∫|f(x)|dx로 넓이 구하기", axis={"곡선": "eˣ, 1/x, sin x, cos x, √x, 1/x², ln x, e²ˣ, sec²x × 상수배", "구간": "ln a, eᵏ, π 등"}, disc="x축 아래 부분의 부호를 처리하고 지수·로그의 특수값을 정확히 계산하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IC5_ROWS)}}], table={"key": "f", "rows": IC5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="곡선과 x축 사이의 넓이는 구간에서 |f(x)|를 적분한 것이다. 구간에서 f(x) ≥ 0이면 그대로, 음수인 부분이 있으면 부호를 바꿔 더한다. 넓이 = {INT}.",
        sol2=[("구간에서의 부호 확인 → 넓이 = {INT}", "적분 세우기"), ("{STEP}", "계산"), ("넓이 = {ans}", None, ("{ans}", "넓이"))],
        sol3=["계산 결과가 양수인지, 원시함수를 미분하면 피적분함수가 되는지 확인한다. 따라서 넓이는 {ans}이다.", "{INT}", "넓이 {ans}"],
        model="넓이 = {INT} {STEP}. 따라서 넓이는 {ans}이다.",
        rubric=[("적분 세우기", 3, "{INT} 꼴로 세웠다.", "x축 아래 부분의 부호를 바꾸지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "특수값 계산 실수면 1점.")],
        pitfalls=[("sin x를 0에서 2π까지 그대로 적분해 0으로 답함", "적분 세우기", "불인정"), ("e^(ln a)를 그대로 둠", "계산", "부분"), ("√x의 원시함수 계수 2/3 실수", "계산", "부분")])


def _ic6_rows():
    out = {}
    for a in range(1, 6):
        for b in range(a + 1, 7):
            # v(t) = (t − a)(t − b) 의 3배: 3t² − 3(a+b)t + 3ab, 0 ≤ t ≤ b
            p, qv = -3 * (a + b), 3 * a * b
            vt = f"3t² {'−' if p < 0 else '+'} {abs(p)}t + {qv}"
            pos = lambda T_: Fraction(T_) ** 3 + Fraction(p, 2) * T_ ** 2 + qv * T_  # noqa: E731
            disp = pos(b) - pos(0)
            dist = abs(pos(a) - pos(0)) + abs(pos(b) - pos(a))
            for kk, ask, v, expl in (("disp", f"t = 0에서 t = {b}까지 점 P의 위치의 변화량", disp, f"위치의 변화량 = [[dinteg(0, {b}, v(t), t)]]"), ("dist", f"t = 0에서 t = {b}까지 점 P가 움직인 거리", dist, f"움직인 거리 = [[dinteg(0, {b}, abs(v(t)), t)]], v(t) = 3(t − {a})(t − {b})의 부호가 t = {a}에서 바뀌므로 [0, {a}]와 [{a}, {b}]로 나눠 절댓값을 취한다")):
                q = f"수직선 위를 움직이는 점 P의 시각 t에서의 속도가 v(t) = {vt}일 때, {ask}"
                r = _row(q, v, Q=f"수직선 위를 움직이는 점 P의 시각 t(t ≥ 0)에서의 속도가 v(t) = {vt}일 때, {ask}를 구하시오.", VT=vt, EXPL=expl, ASK=ask, VAL=f"{_fm(v)}")
                if r: out[f"p{a}_{b}_{kk}"] = r
    for c in (1, 2, 3, 4):
        for kk, ask, v, expl, vt in (("s2", "t = 0에서 t = 2π까지 점 P가 움직인 거리", 4 * c, f"[[dinteg(0, 2pi, abs({_sc(c)}sin(t)), t)]] = 2[[dinteg(0, pi, {_sc(c)}sin(t), t)]] = 2 × {2 * c}", f"{_sc(c)}sin t"), ("s1", "t = 0에서 t = π까지 점 P의 위치의 변화량", 2 * c, f"[[dinteg(0, pi, {_sc(c)}sin(t), t)]] = {c}(−cos π + cos 0)", f"{_sc(c)}sin t"), ("c1", "t = 0에서 t = π까지 점 P가 움직인 거리", 2 * c, f"[[dinteg(0, pi, abs({_sc(c)}cos(t)), t)]] = 2[[dinteg(0, frac(pi, 2), {_sc(c)}cos(t), t)]] = 2 × {c} = {2 * c}", f"{_sc(c)}cos t")):
            q = f"속도가 v(t) = {vt}일 때, {ask}"
            r = _row(q, v, Q=f"수직선 위를 움직이는 점 P의 시각 t(t ≥ 0)에서의 속도가 v(t) = {vt}일 때, {ask}를 구하시오.", VT=vt, EXPL=expl, ASK=ask, VAL=f"{v}")
            if r: out[f"t{c}_{kk}"] = r
    return out


IC6_ROWS = _ic6_rows()


def ic_t6():
    return T(IC, 6, IC_B, title="속도와 거리 — 위치의 변화량과 움직인 거리",
        skill="위치의 변화량은 ∫v dt, 움직인 거리는 ∫|v| dt로 구분해 계산하기", axis={"v(t)": "3(t − a)(t − b) / c sin t / c cos t", "묻는 것": "변화량 / 거리"}, disc="속도의 부호가 바뀌는 구간을 나눠 절댓값을 취하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IC6_ROWS)}}], table={"key": "f", "rows": IC6_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="시각 a에서 b까지 위치의 변화량은 [[dinteg(a, b, v(t), t)]], 움직인 거리는 [[dinteg(a, b, abs(v(t)), t)]]이다. 거리를 구할 때는 v(t)의 부호가 바뀌는 시각에서 구간을 나눈다.",
        sol2=[("v(t) = {VT}", "속도"), ("{EXPL}", "적분 세우기"), ("= {VAL}", None, ("{ans}", "{ASK}"))],
        sol3=["움직인 거리는 위치의 변화량의 절댓값보다 작을 수 없음을 확인한다. 따라서 {ASK}는 {ans}이다.", "{EXPL}", "답 {ans}"],
        model="{EXPL} = {VAL}. 따라서 {ASK}는 {ans}이다.",
        rubric=[("적분 세우기", 3, "{EXPL} 꼴로 세웠다.", "거리에서 절댓값을 빠뜨렸으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "구간 나누기 실수면 1점.")],
        pitfalls=[("움직인 거리를 ∫v dt로 계산", "적분 세우기", "불인정"), ("부호가 바뀌는 시각을 찾지 않음", "적분 세우기", "부분"), ("적분 계산 실수", "계산", "부분")])


IC_SEED = SEED(IC, category="해석", title="여러 가지 적분법 — 기본 정적분·치환적분·부분적분·정적분과 급수·넓이·속도와 거리", unit_id="h3-1", concept_ids=["h3-1-13", "h3-1-14", "h3-1-15", "h3-1-16", "h3-1-17", "h3-1-18"],
               schema_name="여러 가지 함수의 적분", note="값이 유리수가 되는 구간(ln a, eᵏ, π 등)만 골랐다. 부분적분은 4가지 기본형 × 상수배.",
               templates=[ic_t1(), ic_t2(), ic_t3(), ic_t4(), ic_t5(), ic_t6()])


if __name__ == "__main__":
    run(SL_SEED, DC_SEED, IC_SEED)
