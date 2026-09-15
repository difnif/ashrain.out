# itemfactory/tools/mkseed_h2_trig.py — 고2 수학I 삼각함수 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h2_trig.py
#     → seeds/h2-1-trig.json   (삼각함수: 호도법 변환·부채꼴 호/넓이·특수각 값·삼각함수 사이의 관계·그래프(주기·최대최소)·사인/코사인법칙, 6틀)
#   각도는 deg()·frac(k pi, d) 마커. 부채꼴 답은 [[N * pi]] 꼴(ans = N).
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
from genkit.expr import eul as _eul, ika as _ika  # noqa: E402

rng = random.Random(20260916)


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


def _rad(k, d):
    """kπ/d 마커"""
    if d == 1:
        return "pi" if k == 1 else f"{k}pi"
    return f"frac({'pi' if k == 1 else str(k) + 'pi'}, {d})"


TR = "h2-1-trig"
TR_B = {**HS, "prereq": ["삼각비", "원의 호와 넓이"], "ops": ["삼각함수"], "traps": ["사분면 부호", "호도법과 육십분법 혼동"], "tags": ["삼각함수", "호도법", "사인법칙", "코사인법칙"]}


# ── t1 호도법 변환 ──────────────────────────────────────────────
def _t1_rows():
    out = {}
    for d in (10, 15, 20, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120, 135, 140, 150, 160, 200, 210, 225, 240, 270, 300, 315, 330, 340, 350):
        f = Fraction(d, 180)
        if f.denominator == 1:
            continue
        q = f"{d}°를 호도법으로 나타내면 [[frac(a, b)]]π이다. 서로소인 두 자연수 a, b에 대하여 a + b의 값을 구하시오."
        v = f.numerator + f.denominator
        if Fraction(v) in _nums(q):
            continue
        out[f"d{d}"] = {"DESC": q, "V": v, "EXPL": f"180° = π이므로 1° = [[frac(pi, 180)]], {d}° = {d} × [[frac(pi, 180)]] = [[frac({f.numerator}pi, {f.denominator})]]" if f.numerator > 1 else f"180° = π이므로 1° = [[frac(pi, 180)]], {d}° = {d} × [[frac(pi, 180)]] = [[frac(pi, {f.denominator})]]", "RES": f"a = {f.numerator}, b = {f.denominator}", "KIND": "육십분법 → 호도법"}
    for b in (1, 2, 3, 4, 5, 6, 9, 10, 12, 18):
        for a in range(1, 13):
            if math.gcd(a, b) != 1:
                continue
            deg = Fraction(180 * a, b)
            if deg.denominator != 1 or deg > 360 or (b == 1 and a > 2):
                continue
            mk = f"[[{_rad(a, b)}]]"
            q = f"{mk}{'를' if b == 1 else '을'} 육십분법으로 나타내면 몇 도인지 구하시오."
            if deg in _nums(q):
                continue
            out[f"r{a}_{b}"] = {"DESC": q, "V": int(deg), "EXPL": f"π = 180°이므로 {mk} = [[frac({a}, {b})]] × 180° = {int(deg)}°" if b > 1 else f"π = 180°이므로 {mk} = {a} × 180° = {int(deg)}°", "RES": f"{int(deg)}°", "KIND": "호도법 → 육십분법"}
    return out


T1_ROWS = _t1_rows()


def tr_t1():
    return T(TR, 1, TR_B, title="호도법과 육십분법의 변환",
        skill="180° = π(라디안)임을 써서 도 ↔ 라디안을 바꾸기", axis={"방향": "도→라디안 (a + b) / 라디안→도", "각": "10°~350°, π/6 ~ 2π"}, disc="π = 180°에서 비례식으로 바꾸고 분수를 기약분수로 만드는가", diff=1,
        params=[{"name": "f", "values": {"in": list(T1_ROWS)}}], table={"key": "f", "rows": T1_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{DESC}", answer="{ans}",
        sol1="호도법에서 180° = π이다. 도를 라디안으로 바꾸려면 [[frac(pi, 180)]]을 곱하고, 라디안을 도로 바꾸려면 [[frac(180, pi)]]를 곱한다. 이 문제는 {KIND}이다.",
        sol2=[("180° = π", "변환 기준"), ("{EXPL}", "{KIND}"), ("{RES} → 답 {ans}", None, ("{ans}", "답"))],
        sol3=["거꾸로 바꿔 원래 각이 나오는지 확인한다(예: [[frac(pi, 6)]] × [[frac(180, pi)]] = 30°). 따라서 답은 {ans}이다.", "{RES}", "답 {ans}"],
        model="{EXPL}이므로 {RES}, 답은 {ans}이다.",
        rubric=[("변환", 3, "{EXPL} 꼴로 변환했다.", "π와 180°의 자리를 바꿨으면 인정하지 않는다."), ("답", 2, "{ans}{eul(ans)} 구했다.", "약분하지 않았으면 1점.")],
        pitfalls=[("π를 곱할 것을 나눔", "변환", "불인정"), ("기약분수로 만들지 않음", "답", "부분"), ("a와 b를 바꿔 더함", "답", "부분")])


# ── t2 부채꼴의 호의 길이와 넓이 ──────────────────────────────────
def _pim(v):
    f = Fraction(v)
    return f"[[{f.numerator} * pi]]" if f.denominator == 1 else f"[[frac({f.numerator},{f.denominator}) * pi]]"


def _t2_rows():
    out = {}
    for k, d in ((1, 6), (1, 4), (1, 3), (1, 2), (2, 3), (3, 4), (5, 6), (1, 5), (2, 5), (3, 5), (4, 5), (5, 4), (4, 3), (7, 6), (3, 2), (5, 3), (7, 4), (11, 6), (1, 1), (1, 8), (3, 8), (5, 8), (1, 9), (2, 9), (1, 10), (3, 10)):
        for r in range(2, 21):
            L = Fraction(r * k, d)
            S = Fraction(r * r * k, 2 * d)
            th = f"[[{_rad(k, d)}]]"
            q = f"반지름의 길이가 {r}, 중심각의 크기가 {th}인 부채꼴"
            if L.denominator == 1 and L not in _nums(q):
                out[f"a{k}_{d}_{r}"] = {"TH": th, "R": r, "LS": _pim(L), "SS": _pim(S), "ASK": "호의 길이", "LAW": "l = rθ", "V": int(L)}
            if S.denominator == 1 and S not in _nums(q):
                out[f"s{k}_{d}_{r}"] = {"TH": th, "R": r, "LS": _pim(L), "SS": _pim(S), "ASK": "넓이", "LAW": "S = ½r²θ", "V": int(S)}
    return _pick(out, 330)


T2_ROWS = _t2_rows()


def tr_t2():
    return T(TR, 2, TR_B, title="부채꼴의 호의 길이와 넓이 — l = rθ, S = ½r²θ",
        skill="중심각이 θ(라디안)인 부채꼴에서 호의 길이 l = rθ, 넓이 S = ½r²θ = ½rl 쓰기", axis={"중심각": "π/10 ~ 11π/6", "반지름": "2~20", "묻는 것": "호의 길이 / 넓이"}, disc="라디안 공식을 쓰되 육십분법 공식(θ/360)과 섞지 않는가", diff=2,
        params=[{"name": "f", "values": {"in": list(T2_ROWS)}}], table={"key": "f", "rows": T2_ROWS},
        derive={"ans": "V"}, cost=["R", "ans"], verify=["ans == V"],
        q="반지름의 길이가 {R}, 중심각의 크기가 {TH}인 부채꼴의 {ASK}를 구하시오.", answer="[[{ans} * pi]]",
        sol1="중심각 θ가 라디안이면 호의 길이는 l = rθ, 넓이는 S = ½r²θ이다(라디안이 '반지름의 몇 배'를 뜻하므로 360°로 나누는 과정이 없다). 여기서는 {LAW}를 쓴다.",
        sol2=[("r = {R}, θ = {TH}", "주어진 값"), ("l = rθ = {R} × {TH} = {LS}, S = ½r²θ = {SS}", "공식 대입"), ("{ASK} = [[{ans} * pi]]", None, ("[[{ans} * pi]]", "{ASK}"))],
        sol3=["S = ½rl = ½ × {R} × {LS} = {SS}{ro(R)} 두 공식이 맞아떨어진다. 따라서 {ASK}는 [[{ans} * pi]]이다.", "S = ½rl ✓", "{ASK} [[{ans} * pi]]"],
        model="l = rθ = {R} × {TH} = {LS}, S = ½r²θ = {SS}이므로 {ASK}는 {ans}π이다.",
        rubric=[("공식", 3, "{LAW}에 r = {R}, θ = {TH} 값을 대입했다.", "육십분법 공식과 섞었으면 인정하지 않는다."), ("계산", 2, "[[{ans} * pi]]{eul(ans)} 구했다.", "π 계산 실수면 1점.")],
        pitfalls=[("θ/360을 곱하는 육십분법 공식을 씀", "공식", "불인정"), ("넓이에서 ½을 빠뜨림", "공식", "부분"), ("r²을 r로 둠", "계산", "부분")])


# ── t3 특수각의 삼각함수 값 ──────────────────────────────────────
RADS = {0: "0", 30: "frac(pi, 6)", 45: "frac(pi, 4)", 60: "frac(pi, 3)", 90: "frac(pi, 2)", 120: "frac(2pi, 3)", 135: "frac(3pi, 4)", 150: "frac(5pi, 6)", 180: "pi", 210: "frac(7pi, 6)", 225: "frac(5pi, 4)", 240: "frac(4pi, 3)", 270: "frac(3pi, 2)", 300: "frac(5pi, 3)", 315: "frac(7pi, 4)", 330: "frac(11pi, 6)", 360: "2pi"}
TVALS = [("sin", 0, 0), ("sin", 30, Fraction(1, 2)), ("sin", 90, 1), ("sin", 150, Fraction(1, 2)), ("sin", 180, 0), ("sin", 210, Fraction(-1, 2)), ("sin", 270, -1), ("sin", 330, Fraction(-1, 2)), ("sin", 360, 0),
         ("cos", 0, 1), ("cos", 60, Fraction(1, 2)), ("cos", 90, 0), ("cos", 120, Fraction(-1, 2)), ("cos", 180, -1), ("cos", 240, Fraction(-1, 2)), ("cos", 270, 0), ("cos", 300, Fraction(1, 2)), ("cos", 360, 1),
         ("tan", 0, 0), ("tan", 45, 1), ("tan", 135, -1), ("tan", 180, 0), ("tan", 225, 1), ("tan", 315, -1), ("tan", 360, 0),
         ("sin", -30, Fraction(-1, 2)), ("cos", -60, Fraction(1, 2)), ("tan", -45, -1), ("sin", -90, -1), ("cos", -180, -1), ("sin", 390, Fraction(1, 2)), ("cos", 420, Fraction(1, 2)), ("tan", 405, 1)]
QUAD = {30: "제1사분면", 45: "제1사분면", 60: "제1사분면", 120: "제2사분면", 135: "제2사분면", 150: "제2사분면", 210: "제3사분면", 225: "제3사분면", 240: "제3사분면", 300: "제4사분면", 315: "제4사분면", 330: "제4사분면"}


def _term(fn, deg, rad):
    if rad and deg in RADS:
        return f"[[{fn}({RADS[deg]})]]"
    return f"[[{fn}(deg({deg}))]]"


def _expl(fn, deg, v):
    d = deg % 360
    if d in (0, 90, 180, 270):
        return f"{fn} {deg}° = {_fm(v)} (축 위의 각)"
    ref = min(d % 180, 180 - d % 180)
    return f"{fn} {deg}° = {'−' if v < 0 else ''}{fn} {ref}° = {_fm(v)} ({QUAD.get(d, '')}, 부호 {'−' if v < 0 else '+'})"


def _t3_rows():
    out = {}
    n = len(TVALS)
    tries = 0
    while len(out) < 340 and tries < 20000:
        tries += 1
        cnt = rng.choice((2, 2, 3))
        idx = rng.sample(range(n), cnt)
        rad = rng.random() < 0.45
        terms = [TVALS[i] for i in idx]
        if rad and any(t[1] not in RADS for t in terms):
            continue
        ops = [rng.choice(("+", "−")) for _ in range(cnt - 1)]
        v = Fraction(terms[0][2])
        for op, t in zip(ops, terms[1:]):
            v = v + Fraction(t[2]) if op == "+" else v - Fraction(t[2])
        if v == 0:
            continue
        expr = _term(*terms[0][:2], rad)
        for op, t in zip(ops, terms[1:]):
            expr += f" {op} {_term(t[0], t[1], rad)}"
        if v in _nums(expr) or abs(v) in _nums(expr):
            continue
        key = expr
        if key in out:
            continue
        vals = " , ".join(_expl(t[0], t[1], t[2]) for t in terms)
        calc = _fm(terms[0][2])
        for op, t in zip(ops, terms[1:]):
            calc += f" {op} {_fmp(t[2])}"
        out[f"r{len(out)}"] = {"EXPR": expr, "VALS": vals, "CALC": calc, "VN": v.numerator, "VD": v.denominator}
    return out


T3_ROWS = _t3_rows()


def tr_t3():
    return T(TR, 3, TR_B, title="특수각의 삼각함수 값 — 일반각의 삼각함수",
        skill="각을 사분면으로 분류해 부호를 정하고 예각의 값으로 바꿔 계산하기", axis={"각": "0°~420°, 음의 각 (도·라디안)", "항 수": "2~3"}, disc="사분면에 따른 부호와 축 위의 각의 값(0, ±1)을 정확히 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(T3_ROWS)}}], table={"key": "f", "rows": T3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="일반각의 삼각함수는 단위원 위의 점 (cos θ, sin θ)로 정한다. 각이 놓인 사분면에서 부호를 정하고(사인은 1·2사분면 +, 코사인은 1·4사분면 +, 탄젠트는 1·3사분면 +) 예각으로 바꿔 값을 읽는다. 축 위의 각(0°, 90°, 180°, 270°)은 0 또는 ±1이다.",
        sol2=[("{VALS}", "각 항의 값"), ("{CALC}", "대입"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["각 값의 부호를 사분면과 대조해 확인한다. 따라서 값은 {ans}이다.", "{CALC}", "답 {ans}"],
        model="{VALS}이므로 {CALC} = {ans}이다.",
        rubric=[("각 항의 값", 3, "{VALS}{ro(ans)} 구했다.", "부호가 하나 틀리면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "분수 계산 실수면 1점.")],
        pitfalls=[("사분면 부호를 잘못 정함", "각 항의 값", "불인정"), ("sin 90° = 0 등 축 위의 각 값 혼동", "각 항의 값", "불인정"), ("분수 계산 실수", "계산", "부분")])


# ── t4 삼각함수 사이의 관계 ────────────────────────────────────
def _t4_rows():
    out = {}
    for s in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(2, 3), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(6, 5), Fraction(7, 5), Fraction(1, 7), Fraction(5, 4), Fraction(4, 3), Fraction(7, 6)):
        for sign in (1, -1):
            sv = s * sign
            p = (sv * sv - 1) / 2
            for kind, ask, v in (("p", "sin θ cos θ", p), ("cube", "sin³θ + cos³θ", sv ** 3 - 3 * sv * p)):
                if v == 0:
                    continue
                desc = f"sin θ + cos θ = {_fm(sv)}"
                out[f"s{sv}_{kind}"] = {"DESC": desc, "ASK": ask, "VN": v.numerator, "VD": v.denominator, "LAW": "sin²θ + cos²θ = 1", "STEP": f"양변을 제곱: sin²θ + 2 sin θ cos θ + cos²θ = {_fm(sv * sv)}, 즉 1 + 2 sin θ cos θ = {_fm(sv * sv)}", "RES": f"sin θ cos θ = {_fm(p)}" + ("" if kind == "p" else f", sin³θ + cos³θ = (sin θ + cos θ)³ − 3 sin θ cos θ (sin θ + cos θ) = {_fm(sv ** 3)} − 3 × {_fmp(p)} × {_fmp(sv)} = {_fm(v)}")}
            d = sv
            p2 = (1 - d * d) / 2
            if p2 != 0:
                out[f"d{sv}"] = {"DESC": f"sin θ − cos θ = {_fm(d)}", "ASK": "sin θ cos θ", "VN": p2.numerator, "VD": p2.denominator, "LAW": "sin²θ + cos²θ = 1", "STEP": f"양변을 제곱: sin²θ − 2 sin θ cos θ + cos²θ = {_fm(d * d)}, 즉 1 − 2 sin θ cos θ = {_fm(d * d)}", "RES": f"sin θ cos θ = {_fm(p2)}"}
    for (x, y, r) in ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25), (20, 21, 29), (21, 20, 29)):
        for Q in (1, 2, 3, 4):
            sx = 1 if Q in (1, 4) else -1   # cos 부호
            sy = 1 if Q in (1, 2) else -1   # sin 부호
            sinv, cosv = Fraction(sy * y, r), Fraction(sx * x, r)
            tanv = sinv / cosv
            for given, gv, asks in (("sin", sinv, (("cos θ", cosv), ("tan θ", tanv))), ("cos", cosv, (("sin θ", sinv), ("tan θ", tanv)))):
                for ask, v in asks:
                    desc = f"θ가 제{Q}사분면의 각이고 {given} θ = {_fm(gv)}"
                    other = "cos" if given == "sin" else "sin"
                    ov = cosv if given == "sin" else sinv
                    out[f"q{x}_{y}_{Q}_{given}_{ask[:3]}"] = {"DESC": desc, "ASK": ask, "VN": v.numerator, "VD": v.denominator, "LAW": "sin²θ + cos²θ = 1, tan θ = sin θ / cos θ", "STEP": f"{other}²θ = 1 − {_fm(gv * gv)} = {_fm(1 - gv * gv)}, 제{Q}사분면에서 {other} θ의 부호는 {'+' if ov > 0 else '−'}", "RES": f"{other} θ = {_fm(ov)}, tan θ = sin θ ÷ cos θ = {_fm(sinv)} ÷ {_fmp(cosv)} = {_fm(tanv)}"}
    return _pick(out, 330)


T4_ROWS = _t4_rows()


def tr_t4():
    return T(TR, 4, TR_B, title="삼각함수 사이의 관계 — sin²θ + cos²θ = 1",
        skill="sin θ ± cos θ의 값을 제곱해 sin θ cos θ를 얻거나, 사분면과 한 값에서 나머지 삼각함수 값 구하기", axis={"형태": "합·차의 제곱 / 사분면 + 한 값", "묻는 것": "sin θ cos θ, sin³θ + cos³θ, cos θ, sin θ, tan θ"}, disc="제곱해서 1을 분리하거나 사분면으로 부호를 정하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(T4_ROWS)}}], table={"key": "f", "rows": T4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{DESC}일 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="삼각함수 사이의 관계 {LAW}을 쓴다. 합·차가 주어지면 양변을 제곱해 sin²θ + cos²θ = 1을 분리하고, 사분면과 한 값이 주어지면 제곱 관계로 나머지 값의 크기를 구한 뒤 사분면으로 부호를 정한다.",
        sol2=[("{LAW}", "관계식"), ("{STEP}", "변형"), ("{RES} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["구한 값들이 sin²θ + cos²θ = 1을 만족하는지, 부호가 사분면과 맞는지 확인한다. 따라서 {ASK} = {ans}이다.", "{RES}", "{ASK} = {ans}"],
        model="{STEP}이므로 {RES}. 따라서 {ASK} = {ans}이다.",
        rubric=[("관계식 적용", 3, "{STEP} 꼴로 변형했다.", "제곱하지 않고 값을 나눠 가졌으면 인정하지 않는다."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("(sin θ + cos θ)²을 sin²θ + cos²θ로 전개", "관계식 적용", "불인정"), ("사분면 부호를 잘못 정함", "답", "부분"), ("tan θ = cos θ / sin θ로 뒤집음", "답", "불인정")])


# ── t5 삼각함수의 그래프 ───────────────────────────────────────
PER = {1: "2π", 2: "π", 3: "[[frac(2pi, 3)]]", 4: "[[frac(pi, 2)]]", 5: "[[frac(2pi, 5)]]", 6: "[[frac(pi, 3)]]"}


def tr_t5():
    return T(TR, 5, TR_B, title="삼각함수의 그래프 — 주기·최댓값·최솟값에서 a, b, c 읽기",
        skill="y = a sin bx + c (a > 0, b > 0)에서 최댓값 c + a, 최솟값 c − a, 주기 2π/b임을 써서 상수 정하기", axis={"함수": "sin / cos", "주기": "2π ~ π/3", "최대·최소": "−3~8"}, disc="최댓값과 최솟값의 평균이 c, 차의 절반이 a, 주기 2π/b에서 b를 읽는가", diff=2,
        params=[{"name": "fn", "values": {"in": ["sin", "cos"]}}, {"name": "bk", "values": {"in": [str(i) for i in range(1, 7)]}}, {"name": "M", "values": {"int": [-3, 8]}}, {"name": "m", "values": {"int": [-8, 5]}}, {"name": "k", "values": {"in": ["sum", "prod"]}}],
        table=[{"key": "bk", "rows": {str(i): {"PER": PER[i], "BV": i} for i in range(1, 7)}}, {"key": "k", "rows": {"sum": {"ASK": "a + b + c", "w": 1}, "prod": {"ASK": "abc", "w": 0}}}],
        derive={"b": "BV", "a": "(M - m)/2", "c": "(M + m)/2", "ans": "w*((M - m)/2 + BV + (M + m)/2) + (1 - w)*((M - m)/2*BV*(M + m)/2)"},
        constraints=["M > m", "(M - m) % 2 == 0", "c != 0", "ans != 0", "ans not in (M, m, b, a, c, 2, 3, 5)"], cost=["b", "M", "m", "a", "c", "ans"], verify=["a + c == M", "c - a == m", "a > 0"],
        q="주기가 {PER}이고 최댓값이 {M}, 최솟값이 {m}인 함수 y = a {fn} bx + c에 대하여 {ASK}의 값을 구하시오. (단, a > 0, b > 0이고 a, b, c는 상수이다.)", answer="{ans}",
        sol1="y = a {fn} bx + c(a > 0)는 {fn} bx가 −1에서 1까지 움직이므로 최댓값 c + a, 최솟값 c − a이고, 주기는 [[frac(2pi, b)]]이다. 최댓값과 최솟값을 더하면 2c, 빼면 2a가 나온다.",
        sol2=[("c + a = {M}, c − a = {m} → a = {a}, c = {c}", "최대·최소"), ("[[frac(2pi, b)]] = {PER} → b = {b}", "주기"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["a = {a}, c = {c}이면 최댓값 {c} + {a} = {M}, 최솟값 {c} − {a} = {m}{ika(m)} 되고 b = {b}이면 주기가 {PER}이다. 따라서 {ASK} = {ans}이다.", "a = {a}, b = {b}, c = {c}", "{ASK} = {ans}"],
        model="최댓값 c + a = {M}, 최솟값 c − a = {m}에서 a = {a}, c = {c}, 주기 [[frac(2pi, b)]] = {PER}에서 b = {b}이므로 {ASK} = {ans}이다.",
        rubric=[("a, b, c", 3, "a = {a}, b = {b}, c = {c}{eul(c)} 구했다.", "둘만 맞으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("주기를 2πb로 봄(b가 분모임을 잊음)", "a, b, c", "불인정"), ("최댓값을 a로 봄(c를 빠뜨림)", "a, b, c", "불인정"), ("a를 M − m으로 둠(절반을 잊음)", "a, b, c", "부분")])


# ── t6 사인법칙·코사인법칙 ─────────────────────────────────────
COSROWS = {60: [(3, 8, 7), (5, 8, 7), (7, 15, 13), (8, 15, 13), (5, 21, 19), (16, 21, 19), (8, 3, 7), (8, 5, 7), (15, 7, 13), (15, 8, 13), (21, 5, 19), (21, 16, 19)],
           120: [(3, 5, 7), (5, 3, 7), (5, 16, 19), (16, 5, 19), (7, 8, 13), (8, 7, 13), (9, 15, 21), (15, 9, 21), (6, 10, 14), (10, 6, 14)],
           90: [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17), (9, 12, 15), (7, 24, 25), (24, 7, 25)]}
COSV = {60: "[[frac(1,2)]]", 120: "[[-frac(1,2)]]", 90: "0", 30: "[[frac(sqrt(3),2)]]"}
SINV = {30: "[[frac(1,2)]]", 150: "[[frac(1,2)]]", 90: "1"}


def _t6_rows():
    out = {}
    for A, tri in COSROWS.items():
        for b, c, a in tri:
            desc = f"삼각형 ABC에서 b = {b}, c = {c}, A = [[deg({A})]]"
            if Fraction(a) in _nums(desc):
                continue
            sgn_ = "−" if A < 90 else "+"
            out[f"c{A}_{b}_{c}"] = {"DESC": desc, "ASK": "a의 값", "VN": a, "VD": 1, "LAW": "코사인법칙 a² = b² + c² − 2bc cos A", "STEP": f"a² = {b}² + {c}² − 2 × {b} × {c} × {COSV[A]} = {b * b} + {c * c} {sgn_} {abs(b * c) if A != 90 else 0} = {a * a}" if A != 90 else f"a² = {b}² + {c}² − 2 × {b} × {c} × 0 = {b * b} + {c * c} = {a * a}", "RES": f"a = [[sqrt({a * a})]] = {a} (a > 0)"}
    for a in range(2, 10):
        for b in range(2, 10):
            for c in range(2, 10):
                if not (a < b + c and b < a + c and c < a + b) or (a == b == c):
                    continue
                v = Fraction(b * b + c * c - a * a, 2 * b * c)
                if v == 0 or v.denominator > 60:
                    continue
                desc = f"삼각형 ABC에서 a = {a}, b = {b}, c = {c}"
                out[f"v{a}_{b}_{c}"] = {"DESC": desc, "ASK": "cos A의 값", "VN": v.numerator, "VD": v.denominator, "LAW": "코사인법칙 cos A = (b² + c² − a²)/(2bc)", "STEP": f"cos A = [[frac(pow({b},2) + pow({c},2) − pow({a},2), 2 × {b} × {c})]] = [[frac({b * b + c * c - a * a}, {2 * b * c})]]", "RES": f"약분하면 cos A = {_fm(v)}"}
    for A in (30, 150, 90):
        for b in range(2, 13):
            for c in range(2, 13):
                S = Fraction(b * c, 4) if A != 90 else Fraction(b * c, 2)
                desc = f"삼각형 ABC에서 b = {b}, c = {c}, A = [[deg({A})]]"
                if S.denominator != 1 or S in _nums(desc):
                    continue
                out[f"s{A}_{b}_{c}"] = {"DESC": desc, "ASK": "삼각형 ABC의 넓이", "VN": int(S), "VD": 1, "LAW": "넓이 S = ½bc sin A", "STEP": (f"S = ½ × {b} × {c} × sin {A}° = ½ × {b} × {c} × {SINV[A]}" if A != 90 else f"S = ½ × {b} × {c} × sin 90° = ½ × {b} × {c}"), "RES": f"S = {int(S)}"}
    return _pick(out, 330)


T6_ROWS = _t6_rows()


def tr_t6():
    return T(TR, 6, TR_B, title="사인법칙과 코사인법칙 — 변·각·넓이",
        skill="코사인법칙으로 변이나 cos 값을, 사인법칙의 비로 변의 비를, ½bc sin A로 넓이를 구하기", axis={"묻는 것": "a / cos A / 넓이 / 각 C", "각": "30°, 60°, 90°, 120°, 150°"}, disc="변과 각의 대응(a ↔ A)을 지켜 공식에 대입하고 특수각의 값을 쓰는가", diff=3,
        params=[{"name": "f", "values": {"in": list(T6_ROWS)}}], table={"key": "f", "rows": T6_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{DESC}일 때, {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="삼각형에서 변 a, b, c는 각각 각 A, B, C의 대변이다. 코사인법칙 a² = b² + c² − 2bc cos A는 두 변과 끼인각에서 나머지 변을, 세 변에서 각을 준다. 사인법칙 a/sin A = b/sin B = c/sin C = 2R은 변의 비와 사인의 비가 같음을 뜻하고, 넓이는 S = ½bc sin A이다. 여기서는 {LAW}를 쓴다.",
        sol2=[("{LAW}", "공식 고르기"), ("{STEP}", "대입"), ("{RES} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["변과 각의 대응(대변)을 바꿔 대입하지 않았는지, 특수각의 값(cos 60° = ½, cos 120° = −½, sin 30° = ½)이 맞는지 확인한다. 따라서 {ASK} = {ans}이다.", "{RES}", "{ASK} = {ans}"],
        model="{LAW}에서 {STEP}이므로 {RES}. 따라서 {ASK} = {ans}이다.",
        rubric=[("공식 대입", 3, "{STEP} 꼴로 대입했다.", "대변 대응을 바꿨으면 인정하지 않는다."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "특수각 값 실수면 1점.")],
        pitfalls=[("코사인법칙의 −2bc cos A 부호 실수(둔각)", "공식 대입", "불인정"), ("대변이 아닌 변을 대입", "공식 대입", "불인정"), ("넓이 공식에서 ½을 빠뜨림", "답", "부분")])


T7_TRIPLES = [(3, 5, 7, 120), (7, 8, 13, 120), (5, 16, 19, 120), (9, 15, 21, 120), (7, 33, 37, 120), (11, 24, 31, 120), (16, 39, 49, 120), (6, 10, 14, 120), (14, 16, 26, 120), (10, 32, 38, 120),
              (3, 8, 7, 60), (5, 8, 7, 60), (7, 15, 13, 60), (8, 15, 13, 60), (5, 21, 19, 60), (16, 21, 19, 60), (6, 16, 14, 60), (10, 16, 14, 60), (14, 30, 26, 60), (16, 30, 26, 60), (7, 40, 37, 60), (33, 40, 37, 60), (11, 35, 31, 60), (24, 35, 31, 60), (9, 24, 21, 60), (15, 24, 21, 60),
              (3, 4, 5, 90), (5, 12, 13, 90), (8, 15, 17, 90), (7, 24, 25, 90), (6, 8, 10, 90), (9, 12, 15, 90), (20, 21, 29, 90), (9, 40, 41, 90), (12, 35, 37, 90), (10, 24, 26, 90), (16, 30, 34, 90), (15, 20, 25, 90)]


def _t7_rows():
    out = {}
    for (x0, y0, z0, ang) in T7_TRIPLES:
        assert Fraction(x0 * x0 + y0 * y0 - z0 * z0, 2 * x0 * y0) == {120: Fraction(-1, 2), 60: Fraction(1, 2), 90: Fraction(0)}[ang], (x0, y0, z0)
        # z0 가 특수각의 대변. 두 변의 순서(x, y)·(y, x) × 특수각을 C / A / B 에 두는 배치
        for x, y in ((x0, y0), (y0, x0)):
            for tri, name, other in (((x, y, z0), "C", ("a", "b", "c")), ((z0, x, y), "A", ("b", "c", "a")), ((x, z0, y), "B", ("c", "a", "b"))):
                a_, b_, c_ = tri
                desc = f"삼각형 ABC에서 sin A : sin B : sin C = {a_} : {b_} : {c_}"
                if Fraction(ang) in _nums(desc):
                    continue
                cv = Fraction(x * x + y * y - z0 * z0, 2 * x * y)
                p_, q_, r_ = other   # cos(name) = (p² + q² − r²)/(2pq)
                out[f"r{a_}_{b_}_{c_}_{name}"] = {"DESC": desc, "V": ang, "ANG": name, "LAW": "사인법칙 a : b : c = sin A : sin B : sin C, 코사인법칙",
                                                  "STEP": f"a : b : c = {a_} : {b_} : {c_}이므로 a = {a_}k, b = {b_}k, c = {c_}k로 놓고 cos {name} = ({p_}² + {q_}² − {r_}²)/(2{p_}{q_}) = [[frac({x * x + y * y - z0 * z0}, {2 * x * y})]] = {_fm(cv)}",
                                                  "RES": f"cos {name} = {_fm(cv)}이고 0° < {name} < 180°이므로 {name} = {ang}°"}
    return out


T7_ROWS = _t7_rows()


def tr_t7():
    return T(TR, 7, TR_B, title="사인법칙의 비와 코사인법칙 — 각의 크기",
        skill="sin A : sin B : sin C = a : b : c로 변의 비를 잡고 코사인법칙으로 각을 구하기", axis={"변의 비": "3:5:7, 7:8:13, 3:8:7, 3:4:5 등 38가지 × 배치", "각": "A / B / C = 60°, 90°, 120°"}, disc="사인의 비를 변의 비로 바꾼 뒤 세 변의 코사인법칙으로 각을 결정하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(T7_ROWS)}}], table={"key": "f", "rows": T7_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{DESC}일 때, 각 {ANG}의 크기를 구하시오.", answer="[[deg({ans})]]",
        sol1="사인법칙 a/sin A = b/sin B = c/sin C = 2R에서 a : b : c = sin A : sin B : sin C이다. 따라서 변의 비를 알 수 있고, 세 변의 비에 코사인법칙(구하는 각의 대변을 분자에서 빼는 꼴)을 쓰면 k가 약분되어 각이 정해진다.",
        sol2=[("{LAW}", "공식 고르기"), ("{STEP}", "대입"), ("{RES}", None, ("[[deg({ans})]]", "{ANG}"))],
        sol3=["cos {ANG}의 값이 특수각(½, 0, −½)에 해당하는지, 삼각형의 내각 범위(0° < {ANG} < 180°) 안에서 하나로 정해지는지 확인한다. 따라서 {ANG} = [[deg({ans})]]이다.", "{RES}", "{ANG} = [[deg({ans})]]"],
        model="{LAW}에서 {STEP}이므로 {RES}이다.",
        rubric=[("변의 비", 3, "{STEP} 꼴로 변의 비에 코사인법칙을 썼다.", "사인의 비를 변의 비로 바꾸지 못했으면 인정하지 않는다."), ("각", 2, "{ANG} = [[deg({ans})]]{eul(ans)} 구했다.", "cos 값에서 각을 잘못 읽으면 1점.")],
        pitfalls=[("사인의 비를 각의 비로 봄", "변의 비", "불인정"), ("cos C = −½에서 C = 60°로 읽음", "각", "불인정"), ("가장 큰 변의 대각이 아닌 각을 구함", "각", "부분")])


TR_SEED = SEED(TR, category="함수", title="삼각함수 — 호도법·부채꼴·특수각 값·삼각함수 사이의 관계·그래프·사인/코사인법칙", unit_id="h2-1", concept_ids=["h2-1-08", "h2-1-09", "h2-1-10", "h2-1-11"],
               schema_name="삼각함수와 그 활용", note="각은 deg()/frac(k pi, d) 마커. 부채꼴 답은 [[N * pi]]. 코사인법칙 행은 정수 변이 나오는 60°·90°·120° 삼각형 표.",
               templates=[tr_t1(), tr_t2(), tr_t3(), tr_t4(), tr_t5(), tr_t6(), tr_t7()])


if __name__ == "__main__":
    run(TR_SEED)
