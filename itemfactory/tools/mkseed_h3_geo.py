# itemfactory/tools/mkseed_h3_geo.py — 고3 기하 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h3_geo.py
#     → seeds/h3-3-conic.json  (이차곡선: 포물선·타원·쌍곡선의 초점·준선·축·점근선, 접선(점·기울기), 5틀)
#     → seeds/h3-3-space.json  (공간도형·공간좌표: 삼수선·정사영, 두 점 사이 거리·대칭, 내분점, 구, 4틀)
#     → seeds/h3-3-vec.json    (벡터: 성분 연산, 크기·위치벡터, 내적, 두 벡터가 이루는 각, 직선·평면, 5틀)
#   값은 파이썬으로 계산해 행(VN/VD)에 굽는다(도형 없음, 계산형). 각은 [[deg(n)]] 답.
from __future__ import annotations

import itertools
import math
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260922)


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _fi(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})"


def _sg(c):
    """이항 부호 붙인 항 — '+ 3' / '− 3' / '' (0)."""
    f = Fraction(c)
    if f == 0:
        return ""
    return f"{'+' if f > 0 else '−'} {_fm(abs(f))}"


def _sgv(c, var):
    """'+ 3x' / '− x' / '' 꼴(계수 1 생략)."""
    f = Fraction(c)
    if f == 0:
        return ""
    a = abs(f)
    return f"{'+' if f > 0 else '−'} {'' if a == 1 else _fm(a)}{var}"


def _co(c):
    """선행 계수 — '' / '-' / '3' / '[[frac(1,2)]]'."""
    f = Fraction(c)
    if f == 1:
        return ""
    if f == -1:
        return "-"
    return _fm(f)


def _lin(m, n):
    """y = mx + n 문자열."""
    s = f"y = {_co(m)}x"
    if m == 0:
        s = "y ="
    return (s + " " + _sg(n)).rstrip() if n != 0 else s


def _pt(*c):
    return "(" + ", ".join(str(v) for v in c) + ")"


def _vc(*c):
    return "[[vcomp(" + ", ".join(str(v) for v in c) + ")]]"


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


def _isq(v):
    f = Fraction(v)
    a, b = math.isqrt(f.numerator), math.isqrt(f.denominator)
    return Fraction(a, b) if a * a == f.numerator and b * b == f.denominator else None


TRI = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (9, 12, 15), (12, 9, 15), (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25), (12, 16, 20), (16, 12, 20), (20, 21, 29), (21, 20, 29)]
QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (2, 6, 9, 11), (4, 4, 7, 9), (3, 4, 12, 13), (2, 4, 4, 6), (6, 6, 7, 11), (2, 5, 14, 15), (1, 6, 18, 19)]


# ═══════════════════════════════════════════════════════════════════ 1. 이차곡선
CN = "h3-3-conic"
CN_B = {**HS, "prereq": ["도형의 방정식"], "ops": ["이차곡선"], "traps": ["y² = 4px에서 p는 4로 나눈 값", "타원 c² = a² − b², 쌍곡선 c² = a² + b²"], "tags": ["포물선", "타원", "쌍곡선", "접선"]}


def _cn1_rows():
    out = {}
    for p in NZ(-4, 4):
        fp = 4 * p
        ey, ex = f"[[pow(y,2) = {fp}x]]", f"[[pow(x,2) = {fp}y]]"
        law_y = "포물선 y² = 4px의 초점은 (p, 0), 준선은 x = −p"
        law_x = "포물선 x² = 4py의 초점은 (0, p), 준선은 y = −p"
        base = f"4p = {fp}이므로 p = {p}"
        q = f"포물선 y² = {fp}x"
        for kk, v, Q, law, step, ask in (
            ("fx", p, f"포물선 {ey}의 초점의 x좌표를 구하시오.", law_y, f"{base}, 초점은 ({p}, 0)", "초점의 x좌표"),
            ("dx", -p, f"포물선 {ey}의 준선의 방정식이 x = k일 때, 상수 k의 값을 구하시오.", law_y, f"{base}, 준선은 x = −p = {-p}", "준선 x = k의 k"),
            ("dd", 2 * abs(p), f"포물선 {ey}의 초점과 준선 사이의 거리를 구하시오.", law_y, f"{base}, 초점 ({p}, 0)과 준선 x = {-p} 사이의 거리는 |{p} − ({-p})| = {2 * abs(p)}", "초점과 준선 사이의 거리"),
            ("fy", p, f"포물선 {ex}의 초점의 y좌표를 구하시오.", law_x, f"{base}, 초점은 (0, {p})", "초점의 y좌표"),
            ("dy", -p, f"포물선 {ex}의 준선의 방정식이 y = k일 때, 상수 k의 값을 구하시오.", law_x, f"{base}, 준선은 y = −p = {-p}", "준선 y = k의 k"),
        ):
            r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask)
            if r: out[f"{kk}{p}"] = r
        if p > 0:
            for t in (1, 2, 3):
                x1 = p * t * t
                r = _row(f"{q} x = {x1}", x1 + p, Q=f"포물선 {ey} 위의 점 P의 x좌표가 {x1}일 때, 점 P와 이 포물선의 초점 사이의 거리를 구하시오.", LAW="포물선 위의 점에서 초점까지의 거리는 준선까지의 거리와 같다", STEP=f"{base}, 준선은 x = {-p}이므로 점 P에서 준선까지의 거리는 {x1} − ({-p}) = {x1 + p}", ASK="점 P와 초점 사이의 거리")
                if r: out[f"pf{p}_{t}"] = r
        for h in NZ(-3, 3):
            for k in NZ(-3, 3):
                e = f"[[pow(y {_sg(-k)}, 2) = {fp}(x {_sg(-h)})]]"
                q2 = f"포물선 (y − {k})² = {fp}(x − {h})"
                r = _row(q2, h + p + k, Q=f"포물선 {e}의 초점의 좌표를 (α, β)라 할 때, α + β의 값을 구하시오.", LAW="포물선 y² = 4px를 x축 방향으로 h, y축 방향으로 k만큼 평행이동하면 초점은 (p + h, k)", STEP=f"{base}, 초점은 ({p} + ({h}), {k}) = ({h + p}, {k})", ASK="초점의 좌표의 합 α + β")
                if r: out[f"tr{p}_{h}_{k}"] = r
                r2 = _row(q2, h - p, Q=f"포물선 {e}의 준선의 방정식이 x = c일 때, 상수 c의 값을 구하시오.", LAW="포물선 y² = 4px를 x축 방향으로 h, y축 방향으로 k만큼 평행이동하면 준선은 x = −p + h", STEP=f"{base}, 준선은 x = {-p} + ({h}) = {h - p}", ASK="준선 x = c의 c")
                if r2: out[f"td{p}_{h}_{k}"] = r2
    return _pick(out, 330)


CN1_ROWS = _cn1_rows()


def cn_t1():
    return T(CN, 1, CN_B, title="포물선 — 초점·준선·정의",
        skill="y² = 4px, x² = 4py 꼴에서 p를 읽어 초점·준선을 구하고, 평행이동한 포물선과 정의(초점까지 거리 = 준선까지 거리)를 쓰기", axis={"4p": "±4~±16", "묻는 것": "초점 좌표 / 준선 / 초점-준선 거리 / 점과 초점 사이 거리 / 평행이동"}, disc="4p에서 p를 정확히 읽고 준선의 부호를 반대로 잡는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CN1_ROWS)}}], table={"key": "f", "rows": CN1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "포물선의 정의"), ("{STEP}", "p 읽기"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["초점과 준선이 꼭짓점을 기준으로 서로 반대쪽에 같은 거리 |p|만큼 있는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("p 읽기", 2, "{STEP} 꼴로 p를 구했다.", "4p를 p로 두었으면 인정하지 않는다."), ("값 구하기", 3, "{ans}{eul(ans)} 구했다.", "초점과 준선의 부호를 바꿨으면 1점.")],
        pitfalls=[("4p를 p로 읽음(y² = 8x에서 p = 8)", "p 읽기", "불인정"), ("준선을 x = p로 둠", "값 구하기", "부분"), ("x² = 4py의 초점을 (p, 0)으로 둠", "값 구하기", "불인정")])


EL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (25, 24, 7), (25, 7, 24), (17, 15, 8), (17, 8, 15), (15, 12, 9), (15, 9, 12), (20, 16, 12), (20, 12, 16), (25, 20, 15), (25, 15, 20)]
HY = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (15, 8, 17), (9, 12, 15), (12, 9, 15), (7, 24, 25), (24, 7, 25), (20, 21, 29), (21, 20, 29)]


def _cn2_rows():
    out = {}
    for a, b, c in EL:
        for form in ("h", "v"):
            e = f"[[frac(pow(x,2), {a * a}) + frac(pow(y,2), {b * b}) = 1]]" if form == "h" else f"[[frac(pow(x,2), {b * b}) + frac(pow(y,2), {a * a}) = 1]]"
            axis = "x축" if form == "h" else "y축"
            foci = f"(±{c}, 0)" if form == "h" else f"(0, ±{c})"
            law = f"타원 x²/a² + y²/b² = 1 (a > b > 0)의 초점은 (±c, 0), c² = a² − b², 장축 2a, 단축 2b" if form == "h" else "타원 x²/b² + y²/a² = 1 (a > b > 0)의 초점은 (0, ±c), c² = a² − b², 장축 2a(y축 위), 단축 2b"
            base = f"a² = {a * a}, b² = {b * b}이므로 c² = {a * a} − {b * b} = {c * c}, c = {c}"
            q = f"타원 {a} {b} {c} {form}"
            rows = (
                ("ff", 2 * c, f"타원 {e}의 두 초점 사이의 거리를 구하시오.", f"{base}, 초점은 {foci}이므로 초점 사이의 거리는 2c = {2 * c}", "두 초점 사이의 거리"),
                ("maj", 2 * a, f"타원 {e}의 장축의 길이를 구하시오.", f"장축은 {axis} 위에 있고 길이는 2a = 2 × {a} = {2 * a}", "장축의 길이"),
                ("min", 2 * b, f"타원 {e}의 단축의 길이를 구하시오.", f"단축의 길이는 2b = 2 × {b} = {2 * b}", "단축의 길이"),
                ("sum", 2 * a, f"타원 {e} 위의 임의의 점 P와 두 초점 F, F'에 대하여 PF + PF'의 값을 구하시오.", f"타원의 정의에서 PF + PF' = (장축의 길이) = 2a = {2 * a}", "PF + PF'"),
                ("c", c, f"타원 {e}의 두 초점을 F({'c, 0' if form == 'h' else '0, c'}), F'({'-c, 0' if form == 'h' else '0, -c'})이라 할 때, 양수 c의 값을 구하시오.", base, "양수 c"),
            )
            for kk, v, Q, step, ask in rows:
                r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask)
                if r: out[f"{kk}{a}_{b}_{form}"] = r
            for d in range(a - c + 1, a + c):
                if d == a:
                    continue
                r = _row(f"{q} d = {d}", 2 * a - d, Q=f"타원 {e} 위의 점 P와 두 초점 F, F'에 대하여 PF = {d}일 때, 선분 PF'의 길이를 구하시오.", LAW=law, STEP=f"타원의 정의에서 PF + PF' = 2a = {2 * a}이므로 PF' = {2 * a} − {d} = {2 * a - d}", ASK="선분 PF'의 길이")
                if r: out[f"pf{a}_{b}_{form}_{d}"] = r
        # 역: 초점과 거리의 합 → 방정식
        r = _row(f"타원 역 {a} {c}", a * a + b * b, Q=f"두 초점 F({c}, 0), F'(-{c}, 0)으로부터의 거리의 합이 {2 * a}인 타원의 방정식이 [[frac(pow(x,2), A) + frac(pow(y,2), B) = 1]]일 때, A + B의 값을 구하시오.", LAW="거리의 합이 2a이면 장축 2a, c² = a² − b²에서 b²을 구한다", STEP=f"2a = {2 * a}에서 a = {a}, a² = {a * a}, b² = a² − c² = {a * a} − {c * c} = {b * b}", ASK="A + B")
        if r: out[f"inv{a}_{b}"] = r
    return _pick(out, 330)


CN2_ROWS = _cn2_rows()


def cn_t2():
    return T(CN, 2, CN_B, title="타원 — 초점·장축·단축과 정의",
        skill="x²/a² + y²/b² = 1에서 c² = a² − b²로 초점을 구하고 장축·단축, 거리의 합 2a를 쓰기", axis={"(a, b, c)": "피타고라스 쌍 (5,4,3)·(13,12,5)·…", "묻는 것": "초점 사이 거리 / 장축 / 단축 / PF + PF' / PF' / 방정식 역산"}, disc="c² = a² − b²(더하기가 아님)와 장축이 큰 분모 쪽 축에 있음을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CN2_ROWS)}}], table={"key": "f", "rows": CN2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "타원의 성질"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["a > b이고 c < a인지, 초점이 장축 위에 있는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 2, "{STEP} 꼴로 세웠다.", "c² = a² + b²으로 두었으면 인정하지 않는다."), ("값 구하기", 3, "{ans}{eul(ans)} 구했다.", "2배(장축·초점 사이 거리)를 빠뜨렸으면 1점.")],
        pitfalls=[("c² = a² + b²으로 계산", "공식", "불인정"), ("장축의 길이를 a로 답함", "값 구하기", "부분"), ("초점이 있는 축을 반대로 잡음", "공식", "부분")])


def _cn3_rows():
    out = {}
    for a, b, c in HY:
        for form in ("1", "-1"):
            e = f"[[frac(pow(x,2), {a * a}) − frac(pow(y,2), {b * b}) = {form}]]"
            law = "쌍곡선 x²/a² − y²/b² = 1의 초점은 (±c, 0), c² = a² + b², 주축 2a, 점근선 y = ±(b/a)x" if form == "1" else "쌍곡선 x²/a² − y²/b² = −1의 초점은 (0, ±c), c² = a² + b², 주축 2b(y축 위), 점근선 y = ±(b/a)x"
            base = f"a² = {a * a}, b² = {b * b}이므로 c² = {a * a} + {b * b} = {c * c}, c = {c}"
            foci = f"(±{c}, 0)" if form == "1" else f"(0, ±{c})"
            main = 2 * a if form == "1" else 2 * b
            q = f"쌍곡선 {a} {b} {c} {form}"
            rows = (
                ("ff", 2 * c, f"쌍곡선 {e}의 두 초점 사이의 거리를 구하시오.", f"{base}, 초점은 {foci}이므로 초점 사이의 거리는 2c = {2 * c}", "두 초점 사이의 거리"),
                ("main", main, f"쌍곡선 {e}의 주축의 길이를 구하시오.", f"주축은 {'x축' if form == '1' else 'y축'} 위에 있고 길이는 2 × {main // 2} = {main}", "주축의 길이"),
                ("asym", Fraction(b, a), f"쌍곡선 {e}의 점근선의 방정식이 y = ±mx (m > 0)일 때, m의 값을 구하시오.", f"점근선은 y = ±(b/a)x = ±{_fm(Fraction(b, a))}x", "점근선의 기울기 m"),
                ("diff", main, f"쌍곡선 {e} 위의 임의의 점 P와 두 초점 F, F'에 대하여 |PF − PF'|의 값을 구하시오.", f"쌍곡선의 정의에서 |PF − PF'| = (주축의 길이) = {main}", "|PF − PF'|"),
                ("c", c, f"쌍곡선 {e}의 두 초점을 F({'c, 0' if form == '1' else '0, c'}), F'({'-c, 0' if form == '1' else '0, -c'})이라 할 때, 양수 c의 값을 구하시오.", base, "양수 c"),
            )
            for kk, v, Q, step, ask in rows:
                r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask)
                if r: out[f"{kk}{a}_{b}_{form}"] = r
        r = _row(f"쌍곡선 역 {a} {b} {c}", a * a + b * b, Q=f"두 초점 F({c}, 0), F'(-{c}, 0)으로부터의 거리의 차가 {2 * a}인 쌍곡선의 방정식이 [[frac(pow(x,2), A) − frac(pow(y,2), B) = 1]]일 때, A + B의 값을 구하시오.", LAW="거리의 차가 2a이면 주축 2a, c² = a² + b²에서 b²을 구한다", STEP=f"2a = {2 * a}에서 a = {a}, a² = {a * a}, b² = c² − a² = {c * c} − {a * a} = {b * b}", ASK="A + B")
        if r: out[f"inv{a}_{b}"] = r
    return _pick(out, 330)


CN3_ROWS = _cn3_rows()


def cn_t3():
    return T(CN, 3, CN_B, title="쌍곡선 — 초점·주축·점근선과 정의",
        skill="x²/a² − y²/b² = ±1에서 c² = a² + b²로 초점을 구하고 주축, 점근선 y = ±(b/a)x, 거리의 차 2a를 쓰기", axis={"(a, b, c)": "피타고라스 삼조 (3,4,5)·(5,12,13)·…", "우변": "1 / −1", "묻는 것": "초점 사이 거리 / 주축 / 점근선 기울기 / |PF − PF'| / 방정식 역산"}, disc="c² = a² + b²와 우변이 −1이면 초점이 y축 위에 있음을 아는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CN3_ROWS)}}], table={"key": "f", "rows": CN3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "쌍곡선의 성질"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["c > a, c > b인지, 점근선의 기울기가 b/a(우변 부호와 무관)인지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 2, "{STEP} 꼴로 세웠다.", "c² = a² − b²으로 두었으면 인정하지 않는다."), ("값 구하기", 3, "{ans}{eul(ans)} 구했다.", "우변 −1일 때 주축을 x축 위로 잡았으면 1점.")],
        pitfalls=[("c² = a² − b²으로 계산", "공식", "불인정"), ("우변이 −1일 때 초점을 x축 위로 둠", "값 구하기", "불인정"), ("점근선 기울기를 a/b로 둠", "값 구하기", "부분")])


def _cn4_rows():
    out = {}
    # 포물선 y² = 4px 위의 점 (pt², 2pt): 접선 y₁y = 2p(x + x₁) → 기울기 1/t, x절편 −x₁, y절편 pt
    for p in NZ(-3, 3):
        for t in (-3, -2, -1, 1, 2, 3):
            x1, y1 = p * t * t, 2 * p * t
            m, n = Fraction(1, t), Fraction(p * t)
            e = f"[[pow(y,2) = {4 * p}x]]"
            law = "포물선 y² = 4px 위의 점 (x₁, y₁)에서의 접선의 방정식은 y₁y = 2p(x + x₁)"
            step = f"{y1}y = {2 * p}(x {_sg(x1)}) 즉 {_lin(m, n)}"
            q = f"포물선 y² = {4 * p}x 위의 점 ({x1}, {y1}) 접선"
            for kk, v, ask in (("m", m, "기울기"), ("xi", Fraction(-x1), "x절편"), ("yi", n, "y절편"), ("mn", m + n, "m + n")):
                Q = f"포물선 {e} 위의 점 ({x1}, {y1})에서의 접선의 {ask}를 구하시오." if kk != "mn" else f"포물선 {e} 위의 점 ({x1}, {y1})에서의 접선의 방정식이 y = mx + n일 때, 상수 m, n에 대하여 m + n의 값을 구하시오."
                r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask if kk == "mn" else f"접선의 {ask}")
                if r: out[f"p{kk}{p}_{t}"] = r
    # 타원 x²/a² + y²/b² = 1 위의 점: x₁x/a² + y₁y/b² = 1
    for (mm, nn, kk_) in ((3, 4, 5), (4, 3, 5)):
        for i in (1, 2, 3, 4):
            for j in (1, 2, 3, 4):
                if i == j:
                    continue
                a, b = kk_ * i, kk_ * j
                for sx in (1, -1):
                    for sy in (1, -1):
                        x1, y1 = sx * i * mm, sy * j * nn
                        e = f"[[frac(pow(x,2), {a * a}) + frac(pow(y,2), {b * b}) = 1]]"
                        law = "타원 x²/a² + y²/b² = 1 위의 점 (x₁, y₁)에서의 접선의 방정식은 x₁x/a² + y₁y/b² = 1"
                        m = Fraction(-b * b * x1, a * a * y1); n = Fraction(b * b, y1)
                        step = f"[[frac({x1}x, {a * a}) {'+' if y1 > 0 else '−'} frac({abs(y1)}y, {b * b}) = 1]] 즉 {_lin(m, n)}"
                        q = f"타원 {a} {b} 점 ({x1}, {y1}) 접선"
                        for kk, v, ask in (("m", m, "기울기"), ("xi", Fraction(a * a, x1), "x절편"), ("yi", n, "y절편"), ("mn", m + n, "m + n")):
                            Q = f"타원 {e} 위의 점 ({x1}, {y1})에서의 접선의 {ask}를 구하시오." if kk != "mn" else f"타원 {e} 위의 점 ({x1}, {y1})에서의 접선의 방정식이 y = mx + n일 때, 상수 m, n에 대하여 m + n의 값을 구하시오."
                            r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask if kk == "mn" else f"접선의 {ask}")
                            if r: out[f"e{kk}{a}_{b}_{x1}_{y1}"] = r
    # 쌍곡선 x²/a² − y²/b² = 1 위의 점: x₁x/a² − y₁y/b² = 1
    for (kk_, nn, mm) in ((5, 4, 3), (5, 3, 4), (13, 12, 5)):
        for i in (1, 2, 3):
            for j in (1, 2, 3):
                a, b = mm * i, mm * j
                if a > 20 or b > 20:
                    continue
                for sx in (1, -1):
                    for sy in (1, -1):
                        x1, y1 = sx * i * kk_, sy * j * nn
                        e = f"[[frac(pow(x,2), {a * a}) − frac(pow(y,2), {b * b}) = 1]]"
                        law = "쌍곡선 x²/a² − y²/b² = 1 위의 점 (x₁, y₁)에서의 접선의 방정식은 x₁x/a² − y₁y/b² = 1"
                        m = Fraction(b * b * x1, a * a * y1); n = Fraction(-b * b, y1)
                        step = f"[[frac({x1}x, {a * a}) {'−' if y1 > 0 else '+'} frac({abs(y1)}y, {b * b}) = 1]] 즉 {_lin(m, n)}"
                        q = f"쌍곡선 {a} {b} 점 ({x1}, {y1}) 접선"
                        for kk, v, ask in (("m", m, "기울기"), ("xi", Fraction(a * a, x1), "x절편"), ("yi", n, "y절편"), ("mn", m + n, "m + n")):
                            Q = f"쌍곡선 {e} 위의 점 ({x1}, {y1})에서의 접선의 {ask}를 구하시오." if kk != "mn" else f"쌍곡선 {e} 위의 점 ({x1}, {y1})에서의 접선의 방정식이 y = mx + n일 때, 상수 m, n에 대하여 m + n의 값을 구하시오."
                            r = _row(q, v, Q=Q, LAW=law, STEP=step, ASK=ask if kk == "mn" else f"접선의 {ask}")
                            if r: out[f"h{kk}{a}_{b}_{x1}_{y1}"] = r
    return _pick(out, 330)


CN4_ROWS = _cn4_rows()


def cn_t4():
    return T(CN, 4, CN_B, title="이차곡선 위의 점에서의 접선",
        skill="포물선 y₁y = 2p(x + x₁), 타원 x₁x/a² + y₁y/b² = 1, 쌍곡선 x₁x/a² − y₁y/b² = 1로 접선을 세우고 기울기·절편 구하기", axis={"곡선": "포물선 / 타원 / 쌍곡선", "묻는 것": "기울기 / x절편 / y절편 / m + n"}, disc="접점의 좌표를 공식에 정확히 대입하고 절편을 구하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CN4_ROWS)}}], table={"key": "f", "rows": CN4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 접점의 좌표를 대입해 접선의 방정식을 만들고 {ASK}를 읽는다.",
        sol2=[("{LAW}", "접선 공식"), ("{STEP}", "대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["접점이 실제로 곡선 위에 있는지, 접선이 접점을 지나는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("접선 세우기", 3, "{STEP} 꼴로 세웠다.", "x₁, y₁을 바꿔 대입했으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "절편·기울기 계산 실수면 1점.")],
        pitfalls=[("x²을 x₁x로 바꾸지 않고 미분 없이 기울기를 추측", "접선 세우기", "불인정"), ("포물선 접선에서 2p 대신 4p 사용", "접선 세우기", "부분"), ("절편을 구할 때 부호 실수", "값 구하기", "부분")])


def _cn5_rows():
    out = {}
    ms = [Fraction(v) for v in (1, -1, 2, -2, 3, -3)] + [Fraction(1, 2), Fraction(-1, 2), Fraction(3, 2), Fraction(-3, 2)]
    for p in NZ(-3, 3):
        for m in ms:
            n = Fraction(p) / m
            q = f"포물선 y² = {4 * p}x 기울기 {m}"
            r = _row(q, n, Q=f"포물선 [[pow(y,2) = {4 * p}x]]에 접하고 기울기가 {_fm(m)}인 직선의 y절편을 구하시오.", LAW="포물선 y² = 4px에 접하고 기울기가 m인 직선의 방정식은 y = mx + p/m", STEP=f"p = {p}, m = {_fm(m)}이므로 접선은 {_lin(m, n)}", ASK="접선의 y절편")
            if r: out[f"p{p}_{m}"] = r
            n2 = -p * m * m
            r2 = _row(f"포물선 x² = {4 * p}y 기울기 {m}", n2, Q=f"포물선 [[pow(x,2) = {4 * p}y]]에 접하고 기울기가 {_fm(m)}인 직선의 y절편을 구하시오.", LAW="포물선 x² = 4py에 접하고 기울기가 m인 직선의 방정식은 y = mx − pm²", STEP=f"p = {p}, m = {_fm(m)}이므로 접선은 {_lin(m, n2)}", ASK="접선의 y절편")
            if r2: out[f"x{p}_{m}"] = r2
    for a in range(1, 14):
        for b in range(1, 14):
            if a == b:
                continue
            for m in (1, -1, 2, -2, 3, -3):
                s2 = a * a * m * m + b * b
                s = math.isqrt(s2)
                if s * s == s2:
                    q = f"타원 {a} {b} 기울기 {m}"
                    r = _row(q, s, Q=f"타원 [[frac(pow(x,2), {a * a}) + frac(pow(y,2), {b * b}) = 1]]에 접하고 기울기가 {m}인 두 직선의 방정식이 y = {_co(m)}x ± k (k > 0)일 때, k의 값을 구하시오.", LAW="타원 x²/a² + y²/b² = 1에 접하고 기울기가 m인 직선은 y = mx ± √(a²m² + b²)", STEP=f"a²m² + b² = {a * a} × {m * m} + {b * b} = {s2}이므로 k = [[sqrt({s2})]] = {s}", ASK="k")
                    if r: out[f"e{a}_{b}_{m}"] = r
                    r2 = _row(q, -s2, Q=f"타원 [[frac(pow(x,2), {a * a}) + frac(pow(y,2), {b * b}) = 1]]에 접하고 기울기가 {m}인 두 직선의 y절편의 곱을 구하시오.", LAW="타원 x²/a² + y²/b² = 1에 접하고 기울기가 m인 직선은 y = mx ± √(a²m² + b²)", STEP=f"y절편은 ±[[sqrt({s2})]] = ±{s}이므로 곱은 −{s2}", ASK="두 y절편의 곱")
                    if r2: out[f"ep{a}_{b}_{m}"] = r2
                s2 = a * a * m * m - b * b
                if s2 > 0:
                    s = math.isqrt(s2)
                    if s * s == s2:
                        q = f"쌍곡선 {a} {b} 기울기 {m}"
                        r = _row(q, s, Q=f"쌍곡선 [[frac(pow(x,2), {a * a}) − frac(pow(y,2), {b * b}) = 1]]에 접하고 기울기가 {m}인 두 직선의 방정식이 y = {_co(m)}x ± k (k > 0)일 때, k의 값을 구하시오.", LAW="쌍곡선 x²/a² − y²/b² = 1에 접하고 기울기가 m인 직선은 y = mx ± √(a²m² − b²)", STEP=f"a²m² − b² = {a * a} × {m * m} − {b * b} = {s2}이므로 k = [[sqrt({s2})]] = {s}", ASK="k")
                        if r: out[f"h{a}_{b}_{m}"] = r
    return _pick(out, 330)


CN5_ROWS = _cn5_rows()


def cn_t5():
    return T(CN, 5, CN_B, title="기울기가 주어진 이차곡선의 접선",
        skill="기울기 m인 접선 y = mx + p/m (포물선), y = mx ± √(a²m² + b²) (타원), y = mx ± √(a²m² − b²) (쌍곡선) 쓰기", axis={"곡선": "포물선(y², x²) / 타원 / 쌍곡선", "m": "±1~±3, ±1/2, ±3/2"}, disc="곡선별 접선 공식을 구분해 쓰고 근호 안의 부호(+, −)를 맞추는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CN5_ROWS)}}], table={"key": "f", "rows": CN5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 주어진 곡선의 p 또는 a², b²과 기울기 m을 공식에 대입한다.",
        sol2=[("{LAW}", "접선 공식"), ("{STEP}", "대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["판별식 D = 0으로 접선 조건을 세워도 같은 결과가 나오는지 확인할 수 있다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "근호 안의 부호를 반대로 썼으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("포물선 x² = 4py에 y² = 4px 공식을 적용", "공식", "불인정"), ("쌍곡선에서 a²m² + b²으로 둠", "공식", "불인정"), ("제곱근 계산 실수", "값 구하기", "부분")])


CN_SEED = SEED(CN, category="도형", title="이차곡선 — 포물선·타원·쌍곡선의 초점·준선·축·점근선과 접선", unit_id="h3-3", concept_ids=["h3-3-01", "h3-3-02", "h3-3-03", "h3-3-04", "h3-3-05", "h3-3-06", "h3-3-07"],
               schema_name="이차곡선", note="초점 거리 c가 정수가 되는 피타고라스 쌍만 사용. 접선은 접점(격자점)·기울기 조건 두 가지, 값은 파이썬으로 계산.",
               templates=[cn_t1(), cn_t2(), cn_t3(), cn_t4(), cn_t5()])


# ═══════════════════════════════════════════════════════════════════ 2. 공간도형과 공간좌표
SP = "h3-3-space"
SP_B = {**HS, "prereq": ["피타고라스 정리", "평면좌표"], "ops": ["공간도형"], "traps": ["삼수선의 정리에서 수직인 선분 찾기", "정사영 넓이 S cos θ"], "tags": ["삼수선", "정사영", "공간좌표", "구"]}


def _sp1_rows():
    out = {}
    for a, b, c in TRI:
        q = f"삼수선 PH = {a} HQ = {b}"
        r = _row(q, c, Q=f"평면 α 위에 있지 않은 점 P에서 평면 α에 내린 수선의 발을 H, 점 H에서 평면 α 위의 직선 l에 내린 수선의 발을 Q라 하자. PH = {a}, HQ = {b}일 때, 점 P와 직선 l 사이의 거리를 구하시오.", LAW="삼수선의 정리: PH ⊥ α, HQ ⊥ l이면 PQ ⊥ l이므로 선분 PQ의 길이가 점 P와 직선 l 사이의 거리", STEP=f"삼각형 PHQ는 ∠PHQ = 90°인 직각삼각형이므로 PQ = [[sqrt(pow({a},2) + pow({b},2))]] = [[sqrt({a * a + b * b})]] = {c}", ASK="점 P와 직선 l 사이의 거리")
        if r: out[f"t{a}_{b}"] = r
        r2 = _row(f"삼수선 PQ = {c} PH = {a}", b, Q=f"평면 α 위에 있지 않은 점 P에서 평면 α에 내린 수선의 발을 H, 점 H에서 평면 α 위의 직선 l에 내린 수선의 발을 Q라 하자. PH = {a}이고 점 P와 직선 l 사이의 거리가 {c}일 때, 선분 HQ의 길이를 구하시오.", LAW="삼수선의 정리: PH ⊥ α, HQ ⊥ l이면 PQ ⊥ l이므로 PQ = (점 P와 직선 l 사이의 거리)", STEP=f"PQ = {c}, 직각삼각형 PHQ에서 HQ = [[sqrt(pow({c},2) − pow({a},2))]] = [[sqrt({c * c - a * a})]] = {b}", ASK="선분 HQ의 길이")
        if r2: out[f"u{a}_{c}"] = r2
    for S in range(4, 41, 2):
        q = f"정사영 넓이 {S} 60도"
        r = _row(q, S // 2, Q=f"넓이가 {S}인 삼각형 ABC가 평면 α와 이루는 각의 크기가 60°일 때, 삼각형 ABC의 평면 α 위로의 정사영의 넓이를 구하시오.", LAW="정사영의 넓이 S' = S cos θ (θ는 두 평면이 이루는 각)", STEP=f"S' = {S} × cos 60° = {S} × [[frac(1,2)]] = {S // 2}", ASK="정사영의 넓이")
        if r: out[f"pr{S}"] = r
        r2 = _row(f"정사영 넓이가 {S} 60도", 2 * S, Q=f"삼각형 ABC의 평면 α 위로의 정사영의 넓이가 {S}이고, 삼각형 ABC가 평면 α와 이루는 각의 크기가 60°일 때, 삼각형 ABC의 넓이를 구하시오.", LAW="정사영의 넓이 S' = S cos θ이므로 S = S'/cos θ", STEP=f"S = {S} ÷ cos 60° = {S} ÷ [[frac(1,2)]] = {2 * S}", ASK="삼각형 ABC의 넓이")
        if r2: out[f"pi{S}"] = r2
    for S in range(6, 31):
        for Sp in range(2, S):
            v = Fraction(Sp, S)
            if v.denominator > 12:
                continue
            q = f"넓이 {S} 정사영 {Sp} cos"
            r = _row(q, v, Q=f"넓이가 {S}인 평면도형의 평면 α 위로의 정사영의 넓이가 {Sp}이다. 이 도형이 놓인 평면과 평면 α가 이루는 각의 크기를 θ라 할 때, cos θ의 값을 구하시오.", LAW="정사영의 넓이 S' = S cos θ이므로 cos θ = S'/S", STEP=f"cos θ = [[frac({Sp}, {S})]] = {_fm(v)}", ASK="cos θ")
            if r: out[f"c{S}_{Sp}"] = r
    for L in range(4, 31, 2):
        q = f"선분 길이 {L} 정사영 60도"
        r = _row(q, L // 2, Q=f"길이가 {L}인 선분 AB가 평면 α와 이루는 각의 크기가 60°일 때, 선분 AB의 평면 α 위로의 정사영의 길이를 구하시오.", LAW="선분의 정사영의 길이 = (선분의 길이) × cos θ", STEP=f"{L} × cos 60° = {L} × [[frac(1,2)]] = {L // 2}", ASK="정사영의 길이")
        if r: out[f"l{L}"] = r
        r2 = _row(f"직선 평면 30도 거리 {L // 2}", L, Q=f"직선 l이 평면 α와 이루는 각의 크기가 30°이고, 직선 l 위의 점 P와 평면 α 사이의 거리가 {L // 2}이다. 직선 l과 평면 α의 교점을 A라 할 때, 선분 PA의 길이를 구하시오.", LAW="점 P에서 α에 내린 수선의 발을 H라 하면 ∠PAH = 30°이고 PH = PA sin 30°", STEP=f"PA = PH ÷ sin 30° = {L // 2} ÷ [[frac(1,2)]] = {L}", ASK="선분 PA의 길이")
        if r2: out[f"d{L}"] = r2
    return _pick(out, 330)


SP1_ROWS = _sp1_rows()


def sp_t1():
    return T(SP, 1, SP_B, title="삼수선의 정리와 정사영",
        skill="삼수선의 정리로 수직인 선분을 찾아 직각삼각형을 만들고, 정사영의 넓이·길이 S cos θ를 쓰기", axis={"상황": "삼수선(PH, HQ → PQ) / 정사영 넓이 (60°, cos θ 역산) / 선분·직선의 정사영", "값": "피타고라스 삼조·짝수 넓이"}, disc="어느 선분이 수직인지(PQ ⊥ l) 판단하고 cos θ를 곱하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SP1_ROWS)}}], table={"key": "f", "rows": SP1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "정리"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["직각이 되는 꼭짓점을 그림으로 확인하고, 정사영은 원래 도형보다 작은지(cos θ ≤ 1) 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("정리 적용", 3, "{STEP} 꼴로 세웠다.", "수직인 선분을 잘못 잡았으면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("PQ ⊥ l을 모르고 PH를 거리로 답함", "정리 적용", "불인정"), ("정사영 넓이에 sin θ를 곱함", "정리 적용", "불인정"), ("cos 60° = √3/2로 둠", "값 구하기", "불인정")])


def _rnd3(lo=-5, hi=5):
    return tuple(rng.randint(lo, hi) for _ in range(3))


def _sp2_rows():
    out = {}
    for dx, dy, dz, d in QUAD:
        for _ in range(10):
            A = _rnd3()
            sg = [rng.choice((1, -1)) for _ in range(3)]
            perm = list((dx, dy, dz)); rng.shuffle(perm)
            B = tuple(A[i] + sg[i] * perm[i] for i in range(3))
            if max(abs(v) for v in B) > 9:
                continue
            q = f"두 점 {_pt(*A)} {_pt(*B)} 거리"
            r = _row(q, d, Q=f"두 점 A{_pt(*A)}, B{_pt(*B)} 사이의 거리를 구하시오.", LAW="두 점 (x₁, y₁, z₁), (x₂, y₂, z₂) 사이의 거리는 √((x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²)", STEP=f"AB = [[sqrt(pow({B[0] - A[0]},2) + pow({B[1] - A[1]},2) + pow({B[2] - A[2]},2))]] = [[sqrt({d * d})]] = {d}", ASK="두 점 사이의 거리")
            if r: out[f"ab{A}_{B}"] = r
    for _ in range(120):
        a, b, c = _rnd3(-6, 6)
        if 0 in (a, b, c):
            continue
        P = _pt(a, b, c)
        q = f"점 P{P}"
        r = _row(q, 2 * abs(c), Q=f"점 P{P}{_eul(str(c))} xy평면에 대하여 대칭이동한 점을 Q라 할 때, 선분 PQ의 길이를 구하시오.", LAW="xy평면에 대한 대칭점은 z좌표의 부호만 바뀐다: (x, y, −z)", STEP=f"Q({a}, {b}, {-c})이므로 PQ = |{c} − ({-c})| = {2 * abs(c)}", ASK="선분 PQ의 길이")
        if r: out[f"sxy{P}"] = r
        r2 = _row(q, abs(c), Q=f"점 P{P}{_wa(str(c))} xy평면 사이의 거리를 구하시오.", LAW="점 (a, b, c)와 xy평면 사이의 거리는 |c|", STEP=f"점 P에서 xy평면에 내린 수선의 발은 ({a}, {b}, 0)이므로 거리는 |{c}| = {abs(c)}", ASK="점 P와 xy평면 사이의 거리")
        if r2: out[f"dxy{P}"] = r2
        r3 = _row(q, a + b - c, Q=f"점 P{P}{_eul(str(c))} xy평면에 대하여 대칭이동한 점을 Q(p, q, r)라 할 때, p + q + r의 값을 구하시오.", LAW="xy평면에 대한 대칭점은 z좌표의 부호만 바뀐다: (x, y, −z)", STEP=f"Q({a}, {b}, {-c})이므로 p + q + r = {a} + ({b}) + ({-c}) = {a + b - c}", ASK="p + q + r")
        if r3: out[f"sq{P}"] = r3
        r4 = _row(q, -a - b + c, Q=f"점 P{P}{_eul(str(c))} z축에 대하여 대칭이동한 점을 Q(p, q, r)라 할 때, p + q + r의 값을 구하시오.", LAW="z축에 대한 대칭점은 x, y좌표의 부호가 바뀐다: (−x, −y, z)", STEP=f"Q({-a}, {-b}, {c})이므로 p + q + r = {-a} + ({-b}) + ({c}) = {-a - b + c}", ASK="p + q + r")
        if r4: out[f"sz{P}"] = r4
    for x, y, h in TRI[:10]:
        for _ in range(3):
            c = rng.randint(-5, 5)
            sx, sy = rng.choice((1, -1)), rng.choice((1, -1))
            P = _pt(sx * x, sy * y, c)
            q = f"점 P{P} z축"
            r = _row(q, h, Q=f"점 P{P}{_wa(str(c))} z축 사이의 거리를 구하시오.", LAW="점 (a, b, c)와 z축 사이의 거리는 수선의 발 (0, 0, c)까지의 거리 √(a² + b²)", STEP=f"[[sqrt(pow({sx * x},2) + pow({sy * y},2))]] = [[sqrt({h * h})]] = {h}", ASK="점 P와 z축 사이의 거리")
            if r: out[f"dz{P}"] = r
            P2 = _pt(c, sx * x, sy * y)
            r2 = _row(f"점 P{P2} x축", h, Q=f"점 P{P2}에서 x축에 내린 수선의 발을 H라 할 때, 선분 PH의 길이를 구하시오.", LAW="점 (a, b, c)에서 x축에 내린 수선의 발은 (a, 0, 0)", STEP=f"H({c}, 0, 0)이므로 PH = [[sqrt(pow({sx * x},2) + pow({sy * y},2))]] = [[sqrt({h * h})]] = {h}", ASK="선분 PH의 길이")
            if r2: out[f"dx{P2}"] = r2
    return _pick(out, 330)


SP2_ROWS = _sp2_rows()


def sp_t2():
    return T(SP, 2, SP_B, title="공간좌표 — 두 점 사이의 거리·대칭점·좌표축과의 거리",
        skill="공간에서 두 점 사이의 거리 공식, 좌표평면·좌표축에 대한 대칭점, 점과 좌표축 사이의 거리 구하기", axis={"묻는 것": "두 점 사이 거리 / 대칭점 좌표 합 / 좌표평면·좌표축까지 거리", "값": "피타고라스 사조 (1,2,2,3)·(2,3,6,7)·…"}, disc="대칭이동에서 부호가 바뀌는 좌표를 정확히 고르고 거리 공식을 3차원으로 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SP2_ROWS)}}], table={"key": "f", "rows": SP2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "공식"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["부호가 바뀌는 좌표의 개수(평면 대칭 1개, 축 대칭 2개, 원점 대칭 3개)를 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 2, "{STEP} 꼴로 세웠다.", "거리 공식에 한 좌표를 빠뜨렸으면 1점."), ("값 구하기", 3, "{ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("xy평면 대칭에서 x, y의 부호를 바꿈", "공식", "불인정"), ("z축까지의 거리를 |c|로 둠", "공식", "불인정"), ("제곱근 계산 실수", "값 구하기", "부분")])


def _sp3_rows():
    out = {}
    for m, n in ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4), (4, 1), (3, 4), (4, 3), (2, 5), (5, 2), (5, 3), (3, 5)):
        for _ in range(20):
            A = _rnd3(-4, 4)
            d = tuple(rng.choice((-2, -1, 1, 2)) for _ in range(3))
            B = tuple(A[i] + (m + n) * d[i] for i in range(3))
            if max(abs(v) for v in B) > 12:
                continue
            P = tuple(A[i] + m * d[i] for i in range(3))
            q = f"내분 {_pt(*A)} {_pt(*B)} {m}:{n}"
            r = _row(q, sum(P), Q=f"두 점 A{_pt(*A)}, B{_pt(*B)}에 대하여 선분 AB를 {m} : {n}{_ro(n)} 내분하는 점을 P(x, y, z)라 할 때, x + y + z의 값을 구하시오.", LAW="선분 AB를 m : n으로 내분하는 점은 ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n), (mz₂ + nz₁)/(m + n))", STEP=f"P = ([[frac({m} × ({B[0]}) + {n} × ({A[0]}), {m + n})]], [[frac({m} × ({B[1]}) + {n} × ({A[1]}), {m + n})]], [[frac({m} × ({B[2]}) + {n} × ({A[2]}), {m + n})]]) = {_pt(*P)}", ASK="x + y + z")
            if r: out[f"in{A}_{B}_{m}_{n}"] = r
            if m != n and (m * (m + n)) % (m - n) == 0:
                k = m * (m + n) // (m - n)
                Qp = tuple(A[i] + k * d[i] for i in range(3))
                if max(abs(v) for v in Qp) <= 30:
                    r2 = _row(q, sum(Qp), Q=f"두 점 A{_pt(*A)}, B{_pt(*B)}에 대하여 선분 AB를 {m} : {n}{_ro(n)} 외분하는 점을 Q(x, y, z)라 할 때, x + y + z의 값을 구하시오.", LAW="선분 AB를 m : n으로 외분하는 점은 ((mx₂ − nx₁)/(m − n), (my₂ − ny₁)/(m − n), (mz₂ − nz₁)/(m − n))", STEP=f"Q = ([[frac({m} × ({B[0]}) − {n} × ({A[0]}), {m - n})]], [[frac({m} × ({B[1]}) − {n} × ({A[1]}), {m - n})]], [[frac({m} × ({B[2]}) − {n} × ({A[2]}), {m - n})]]) = {_pt(*Qp)}", ASK="x + y + z")
                    if r2: out[f"ex{A}_{B}_{m}_{n}"] = r2
    for _ in range(160):
        G = _rnd3(-3, 3)
        A = _rnd3(-6, 6); B = _rnd3(-6, 6)
        C = tuple(3 * G[i] - A[i] - B[i] for i in range(3))
        if max(abs(v) for v in C) > 9 or A == B or B == C or A == C:
            continue
        q = f"무게중심 {_pt(*A)} {_pt(*B)} {_pt(*C)}"
        r = _row(q, sum(G), Q=f"세 점 A{_pt(*A)}, B{_pt(*B)}, C{_pt(*C)}{_eul(str(C[2]))} 꼭짓점으로 하는 삼각형 ABC의 무게중심을 G(x, y, z)라 할 때, x + y + z의 값을 구하시오.", LAW="삼각형의 무게중심은 세 꼭짓점의 좌표의 평균 ((x₁ + x₂ + x₃)/3, (y₁ + y₂ + y₃)/3, (z₁ + z₂ + z₃)/3)", STEP=f"G = ([[frac({A[0]} + ({B[0]}) + ({C[0]}), 3)]], [[frac({A[1]} + ({B[1]}) + ({C[1]}), 3)]], [[frac({A[2]} + ({B[2]}) + ({C[2]}), 3)]]) = {_pt(*G)}", ASK="x + y + z")
        if r: out[f"g{A}_{B}_{C}"] = r
        M = tuple(Fraction(A[i] + B[i], 2) for i in range(3))
        if all(v.denominator == 1 for v in M):
            r2 = _row(f"중점 {_pt(*A)} {_pt(*B)}", sum(M), Q=f"두 점 A{_pt(*A)}, B{_pt(*B)}에 대하여 선분 AB의 중점을 M(x, y, z)라 할 때, x + y + z의 값을 구하시오.", LAW="선분 AB의 중점은 ((x₁ + x₂)/2, (y₁ + y₂)/2, (z₁ + z₂)/2)", STEP=f"M = ([[frac({A[0]} + ({B[0]}), 2)]], [[frac({A[1]} + ({B[1]}), 2)]], [[frac({A[2]} + ({B[2]}), 2)]]) = {_pt(*(int(v) for v in M))}", ASK="x + y + z")
            if r2: out[f"m{A}_{B}"] = r2
    return _pick(out, 330)


SP3_ROWS = _sp3_rows()


def sp_t3():
    return T(SP, 3, SP_B, title="공간에서 선분의 내분점·외분점·중점·무게중심",
        skill="공간좌표에서 내분점·외분점·중점·무게중심의 좌표를 공식으로 구해 좌표의 합 계산하기", axis={"묻는 것": "내분점 / 외분점 / 중점 / 무게중심", "m : n": "1:1~5:3"}, disc="내분·외분 공식에서 m, n의 자리를 바꾸지 않고 세 좌표 모두에 적용하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SP3_ROWS)}}], table={"key": "f", "rows": SP3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 세 좌표 각각에 같은 공식을 적용한 뒤 더한다.",
        sol2=[("{LAW}", "공식"), ("{STEP}", "대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["내분점이 두 점 사이에 있는지(각 좌표가 두 끝점 사이 값인지), 외분점은 바깥에 있는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 2, "{STEP} 꼴로 세웠다.", "m과 n을 바꿔 대입했으면 1점."), ("값 구하기", 3, "{ans}{eul(ans)} 구했다.", "한 좌표만 틀렸으면 2점.")],
        pitfalls=[("m, n을 바꿔 (mx₁ + nx₂)/(m + n)으로 계산", "공식", "불인정"), ("외분점 분모를 m + n으로 둠", "공식", "불인정"), ("z좌표를 빠뜨림", "값 구하기", "부분")])


def _pw(var, c):
    """(var − c)² 마커 조각 — c = 0 이면 var²."""
    return f"pow({var} {_sg(-c)}, 2)" if c != 0 else f"pow({var},2)"


def _sph(a, b, c, d):
    """구 x² + y² + z² − 2ax − 2by − 2cz + d = 0 마커."""
    return f"[[pow(x,2) + pow(y,2) + pow(z,2) {_sgv(-2 * a, 'x')} {_sgv(-2 * b, 'y')} {_sgv(-2 * c, 'z')} {_sg(d)} = 0]]".replace("  ", " ")


def _sp4_rows():
    out = {}
    for _ in range(220):
        a, b, c = _rnd3(-4, 4)
        r_ = rng.randint(1, 6)
        d = a * a + b * b + c * c - r_ * r_
        if (a, b, c) == (0, 0, 0):
            continue
        e = _sph(a, b, c, d)
        q = f"구 {a} {b} {c} d={d}"
        r = _row(q, r_, Q=f"구 {e}의 반지름의 길이를 구하시오.", LAW="x² + y² + z² − 2ax − 2by − 2cz + d = 0을 (x − a)² + (y − b)² + (z − c)² = a² + b² + c² − d 꼴로 고친다", STEP=f"[[{_pw('x', a)} + {_pw('y', b)} + {_pw('z', c)} = {r_ * r_}]]이므로 중심 {_pt(a, b, c)}, 반지름 [[sqrt({r_ * r_})]] = {r_}", ASK="반지름의 길이")
        if r: out[f"r{a}_{b}_{c}_{r_}"] = r
        r2 = _row(q, a + b + c, Q=f"구 {e}의 중심의 좌표를 (p, q, r)라 할 때, p + q + r의 값을 구하시오.", LAW="x² + y² + z² − 2ax − 2by − 2cz + d = 0의 중심은 (a, b, c), 반지름은 √(a² + b² + c² − d)", STEP=f"[[{_pw('x', a)} + {_pw('y', b)} + {_pw('z', c)} = {r_ * r_}]]이므로 중심은 {_pt(a, b, c)}", ASK="p + q + r")
        if r2: out[f"c{a}_{b}_{c}_{r_}"] = r2
    for _ in range(90):
        a, b, c = _rnd3(-5, 5)
        if c == 0:
            continue
        q = f"중심 {_pt(a, b, c)} xy평면 접"
        r = _row(q, abs(c), Q=f"중심이 {_pt(a, b, c)}이고 xy평면에 접하는 구의 반지름의 길이를 구하시오.", LAW="좌표평면에 접하는 구의 반지름은 중심에서 그 평면까지의 거리", STEP=f"중심 {_pt(a, b, c)}와 xy평면 사이의 거리는 |{c}| = {abs(c)}", ASK="반지름의 길이")
        if r: out[f"t{a}_{b}_{c}"] = r
    for x, y, h in TRI[:12]:
        for _ in range(3):
            a, b = rng.randint(-4, 4), rng.randint(-4, 4)
            sc = rng.choice((1, -1))
            e = f"[[{_pw('x', a)} + {_pw('y', b)} + {_pw('z', sc * x)} = {h * h}]]"
            q = f"구 중심 {_pt(a, b, sc * x)} r={h} xy평면 교선"
            r = _row(q, y, Q=f"구 {e}{_wa(str(h * h))} xy평면이 만나서 생기는 원의 반지름의 길이를 구하시오.", LAW="구의 중심에서 평면까지의 거리 d, 반지름 r이면 교선인 원의 반지름은 √(r² − d²)", STEP=f"중심 {_pt(a, b, sc * x)}에서 xy평면까지의 거리는 {x}이므로 원의 반지름은 [[sqrt(pow({h},2) − pow({x},2))]] = [[sqrt({y * y})]] = {y}", ASK="원의 반지름의 길이")
            if r: out[f"x{a}_{b}_{sc * x}_{h}"] = r
    for dx, dy, dz, d in QUAD:
        if d % 2:
            continue
        for _ in range(4):
            A = _rnd3(-5, 5)
            sg = [rng.choice((1, -1)) for _ in range(3)]
            perm = list((dx, dy, dz)); rng.shuffle(perm)
            B = tuple(A[i] + sg[i] * perm[i] for i in range(3))
            if max(abs(v) for v in B) > 9:
                continue
            q = f"지름 {_pt(*A)} {_pt(*B)}"
            r = _row(q, d // 2, Q=f"두 점 A{_pt(*A)}, B{_pt(*B)}{_eul(str(B[2]))} 지름의 양 끝 점으로 하는 구의 반지름의 길이를 구하시오.", LAW="지름의 양 끝 점이 A, B이면 반지름은 AB/2, 중심은 AB의 중점", STEP=f"AB = [[sqrt(pow({B[0] - A[0]},2) + pow({B[1] - A[1]},2) + pow({B[2] - A[2]},2))]] = [[sqrt({d * d})]] = {d}이므로 반지름은 {d // 2}", ASK="반지름의 길이")
            if r: out[f"d{A}_{B}"] = r
    return _pick(out, 330)


SP4_ROWS = _sp4_rows()


def sp_t4():
    return T(SP, 4, SP_B, title="구의 방정식 — 중심·반지름과 평면과의 교선",
        skill="일반형을 표준형으로 고쳐 구의 중심·반지름을 읽고, 좌표평면에 접하는 조건과 교선인 원의 반지름 √(r² − d²) 구하기", axis={"묻는 것": "반지름 / 중심 좌표 합 / 좌표평면 접 / xy평면과의 교선 원 / 지름의 양 끝 점", "값": "r ≤ 6, 피타고라스 삼조"}, disc="완전제곱으로 고칠 때 −2a의 절반을 쓰고, 교선의 반지름에 피타고라스 정리를 쓰는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SP4_ROWS)}}], table={"key": "f", "rows": SP4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "구의 방정식"), ("{STEP}", "표준형·계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["반지름이 양수인지(a² + b² + c² − d > 0), 교선의 반지름이 구의 반지름보다 작은지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("표준형", 3, "{STEP} 꼴로 고쳤다.", "중심의 부호를 반대로 잡았으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("중심을 (−a, −b, −c)로 둠", "표준형", "불인정"), ("반지름을 a² + b² + c² − d로 둠(제곱근 빠뜨림)", "값 구하기", "불인정"), ("교선의 반지름을 구의 반지름으로 답함", "값 구하기", "불인정")])


SP_SEED = SEED(SP, category="도형", title="공간도형과 공간좌표 — 삼수선·정사영, 두 점 사이의 거리·대칭, 내분점, 구의 방정식", unit_id="h3-3", concept_ids=["h3-3-08", "h3-3-09", "h3-3-10", "h3-3-11", "h3-3-12", "h3-3-13"],
               schema_name="공간도형·공간좌표", note="도형 없이 계산형. 거리는 피타고라스 사조(1,2,2,3)·(2,3,6,7)…로 정수, 정사영은 60°(cos = 1/2)와 cos θ 역산만.",
               templates=[sp_t1(), sp_t2(), sp_t3(), sp_t4()])


# ═══════════════════════════════════════════════════════════════════ 3. 벡터
VC = "h3-3-vec"
VC_B = {**HS, "prereq": ["평면좌표", "삼각비"], "ops": ["벡터"], "traps": ["내적은 스칼라", "|a + b|² = |a|² + 2a·b + |b|²"], "tags": ["벡터의 연산", "위치벡터", "내적", "직선과 평면"]}


def _rnd2(lo=-5, hi=5):
    return (rng.randint(lo, hi), rng.randint(lo, hi))


def _vexpr(k, l):
    """k a + l b 마커 (k, l 정수) — 계수와 vec 사이 띄어쓰기."""
    def term(c, v):
        return v if c == 1 else f"-{v}" if c == -1 else f"{c} {v}"
    s = term(k, "vec(a)") if k != 0 else ""
    if l != 0:
        if s:
            s += f" {'+' if l > 0 else '−'} {term(abs(l), 'vec(b)')}"
        else:
            s = term(l, "vec(b)")
    return f"[[{s}]]"


def _vc1_rows():
    out = {}
    for _ in range(160):
        a, b = _rnd2(), _rnd2()
        if a == (0, 0) or b == (0, 0) or a == b:
            continue
        k, l = rng.choice((2, 3, -1, -2, 1)), rng.choice((1, -1, 2, -2, 3))
        v = (k * a[0] + l * b[0], k * a[1] + l * b[1])
        q = f"a{a} b{b} {k}a+{l}b"
        r = _row(q, sum(v), Q=f"두 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}에 대하여 벡터 {_vexpr(k, l)}의 모든 성분의 합을 구하시오.", LAW="벡터의 실수배·덧셈은 성분별로 계산한다: k(a₁, a₂) + l(b₁, b₂) = (ka₁ + lb₁, ka₂ + lb₂)", STEP=f"{_vexpr(k, l)} = ({k} × ({a[0]}) + ({l}) × ({b[0]}), {k} × ({a[1]}) + ({l}) × ({b[1]})) = {_pt(*v)}", ASK="모든 성분의 합")
        if r: out[f"c{a}_{b}_{k}_{l}"] = r
    for x, y, h in TRI:
        for _ in range(8):
            a = _rnd2(-6, 6)
            sx, sy = rng.choice((1, -1)), rng.choice((1, -1))
            tgt = (sx * x, sy * y)
            k, l = rng.choice(((1, 1), (1, -1), (2, -1), (1, 2), (2, 1)))
            # k a + l b = tgt → b = (tgt − k a)/l
            bx, by = Fraction(tgt[0] - k * a[0], l), Fraction(tgt[1] - k * a[1], l)
            if bx.denominator != 1 or by.denominator != 1 or max(abs(bx), abs(by)) > 12:
                continue
            b = (int(bx), int(by))
            if b == (0, 0) or a == b:
                continue
            q = f"a{a} b{b} |{k}a+{l}b|"
            r = _row(q, h, Q=f"두 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}에 대하여 [[abs({_vexpr(k, l)[2:-2]})]]의 값을 구하시오.", LAW="먼저 성분으로 벡터를 구한 뒤 크기 |(x, y)| = √(x² + y²)를 계산한다", STEP=f"{_vexpr(k, l)} = {_pt(*tgt)}이므로 크기는 [[sqrt(pow({tgt[0]},2) + pow({tgt[1]},2))]] = [[sqrt({h * h})]] = {h}", ASK="벡터의 크기")
            if r: out[f"n{a}_{b}_{k}_{l}"] = r
    for _ in range(140):
        b, c = _rnd2(-4, 4), _rnd2(-4, 4)
        if b == (0, 0) or c == (0, 0) or b[0] * c[1] - b[1] * c[0] == 0:
            continue
        t = rng.choice((-3, -2, -1, 1, 2, 3))
        s_ = rng.choice((1, 2, -1, 3))
        a = (s_ * c[0] - t * b[0], s_ * c[1] - t * b[1])
        if max(abs(v) for v in a) > 12 or a == (0, 0):
            continue
        q = f"a{a} b{b} c{c} 평행"
        r = _row(q, t, Q=f"세 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}, [[vec(c)]] = {_vc(*c)}에 대하여 [[vec(a) + t vec(b)]]와 [[vec(c)]]가 서로 평행할 때, 실수 t의 값을 구하시오.", LAW="두 벡터 (p, q), (r, s)가 평행하면 (p, q) = k(r, s), 즉 ps − qr = 0", STEP=f"[[vec(a) + t vec(b)]] = ({a[0]} {_sgv(b[0], 't')}, {a[1]} {_sgv(b[1], 't')})이고 [[vec(c)]] = {_vc(*c)}이므로 ({a[0]} {_sgv(b[0], 't')}) × ({c[1]}) − ({a[1]} {_sgv(b[1], 't')}) × ({c[0]}) = 0에서 t = {t}", ASK="실수 t")
        if r: out[f"p{a}_{b}_{c}"] = r
    for dx, dy, dz, d in QUAD:
        for _ in range(3):
            sg = [rng.choice((1, -1)) for _ in range(3)]
            perm = list((dx, dy, dz)); rng.shuffle(perm)
            a = tuple(sg[i] * perm[i] for i in range(3))
            q = f"3D a{a} 크기"
            r = _row(q, d, Q=f"공간벡터 [[vec(a)]] = {_vc(*a)}의 크기 [[abs(vec(a))]]의 값을 구하시오.", LAW="공간벡터 (a₁, a₂, a₃)의 크기는 √(a₁² + a₂² + a₃²)", STEP=f"[[abs(vec(a))]] = [[sqrt(pow({a[0]},2) + pow({a[1]},2) + pow({a[2]},2))]] = [[sqrt({d * d})]] = {d}", ASK="벡터의 크기")
            if r: out[f"s{a}"] = r
    for _ in range(90):
        x, y = _rnd2(-6, 6)
        a2, b1 = rng.randint(-5, 5), rng.randint(-5, 5)
        k, l = rng.choice(((2, -1), (1, 1), (3, -2), (1, -2), (2, 1)))
        # a = (x, a2), b = (b1, y): k a + l b = (kx + l b1, k a2 + l y)
        res = (k * x + l * b1, k * a2 + l * y)
        if x + y == 0:
            continue
        q = f"미지수 a=(x,{a2}) b=({b1},y) {k}a+{l}b={res}"
        r = _row(q, x + y, Q=f"두 벡터 [[vec(a)]] = [[vcomp(x, {a2})]], [[vec(b)]] = [[vcomp({b1}, y)]]에 대하여 {_vexpr(k, l)} = {_vc(*res)}일 때, x + y의 값을 구하시오.", LAW="두 벡터가 같으면 대응하는 성분이 각각 같다", STEP=f"{_vexpr(k, l)} = ({_co(k)}x {_sg(l * b1)}, {k * a2} {_sgv(l, 'y')}) = {_vc(*res)}에서 x = {x}, y = {y}", ASK="x + y")
        if r: out[f"u{x}_{y}_{a2}_{b1}_{k}_{l}"] = r
    return _pick(out, 330)


VC1_ROWS = _vc1_rows()


def vc_t1():
    return T(VC, 1, VC_B, title="벡터의 성분 연산 — 실수배·합·크기·평행 조건",
        skill="성분으로 ka + lb를 계산하고, 크기 √(x² + y²), 평행 조건(성분의 비례)과 성분 비교로 미지수를 구하기", axis={"묻는 것": "성분의 합 / 크기 / 평행 조건 t / 미지수 x + y / 공간벡터 크기", "값": "성분 −6~6, 크기는 피타고라스 삼조·사조"}, disc="성분별로 정확히 계산하고 크기에 제곱근을 취하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(VC1_ROWS)}}], table={"key": "f", "rows": VC1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "성분 연산"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["성분을 좌표평면에 그려 방향과 길이가 그럴듯한지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("성분 계산", 3, "{STEP} 꼴로 계산했다.", "실수배를 한 성분에만 적용했으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "부호·제곱근 실수면 1점.")],
        pitfalls=[("실수배를 한 성분에만 곱함", "성분 계산", "불인정"), ("크기를 x² + y²(제곱근 없이)으로 둠", "값 구하기", "불인정"), ("평행 조건을 내적 = 0으로 둠", "성분 계산", "불인정")])


def _vc2_rows():
    out = {}
    for p in range(2, 9):
        for q_ in range(2, 9):
            for th, cs, cn in ((60, Fraction(1, 2), "cos 60° = 1/2"), (90, Fraction(0), "cos 90° = 0"), (120, Fraction(-1, 2), "cos 120° = −1/2")):
                dot = p * q_ * cs
                sp = p * p + q_ * q_ + 2 * dot
                sm = p * p + q_ * q_ - 2 * dot
                q = f"|a|={p} |b|={q_} {th}도"
                law = f"|a + b|² = |a|² + 2a·b + |b|², a·b = |a||b|cos θ ({cn})"
                r = _row(q, sp, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}이고 두 벡터가 이루는 각의 크기가 {th}°일 때, [[pow(abs(vec(a) + vec(b)), 2)]]의 값을 구하시오.", LAW=law, STEP=f"[[dot(vec(a), vec(b))]] = {p} × {q_} × ({_fm(cs)}) = {_fm(dot)}이므로 |a + b|² = {p * p} + 2 × ({_fm(dot)}) + {q_ * q_} = {sp}", ASK="|a + b|²")
                if r: out[f"sp{p}_{q_}_{th}"] = r
                r2 = _row(q, sm, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}이고 두 벡터가 이루는 각의 크기가 {th}°일 때, [[pow(abs(vec(a) − vec(b)), 2)]]의 값을 구하시오.", LAW=law.replace("+ 2a·b", "− 2a·b").replace("|a + b|", "|a − b|"), STEP=f"[[dot(vec(a), vec(b))]] = {p} × {q_} × ({_fm(cs)}) = {_fm(dot)}이므로 |a − b|² = {p * p} − 2 × ({_fm(dot)}) + {q_ * q_} = {sm}", ASK="|a − b|²")
                if r2: out[f"sm{p}_{q_}_{th}"] = r2
                for val, nm in ((sp, "+"), (sm, "−")):
                    rt = math.isqrt(int(val))
                    if rt * rt == val and rt not in (p, q_):
                        r3 = _row(q, rt, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}이고 두 벡터가 이루는 각의 크기가 {th}°일 때, [[abs(vec(a) {nm} vec(b))]]의 값을 구하시오.", LAW=law if nm == "+" else law.replace("+ 2a·b", "− 2a·b").replace("|a + b|", "|a − b|"), STEP=f"|a {nm} b|² = {p * p} {'+' if nm == '+' else '−'} 2 × ({_fm(dot)}) + {q_ * q_} = {val}이므로 |a {nm} b| = [[sqrt({val})]] = {rt}", ASK=f"|a {nm} b|")
                        if r3: out[f"rt{p}_{q_}_{th}_{nm}"] = r3
    for m, n in ((1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3)):
        for _ in range(8):
            A = _rnd2(-4, 4)
            d = (rng.choice((-2, -1, 1, 2)), rng.choice((-2, -1, 1, 2)))
            B = (A[0] + (m + n) * d[0], A[1] + (m + n) * d[1])
            if max(abs(v) for v in B) > 12:
                continue
            P = (A[0] + m * d[0], A[1] + m * d[1])
            q = f"위치벡터 내분 {A} {B} {m}:{n}"
            r = _row(q, sum(P), Q=f"두 점 A, B의 위치벡터가 각각 [[vec(a)]] = {_vc(*A)}, [[vec(b)]] = {_vc(*B)}이다. 선분 AB를 {m} : {n}{_ro(n)} 내분하는 점 P의 위치벡터 [[vec(p)]]의 모든 성분의 합을 구하시오.", LAW="선분 AB를 m : n으로 내분하는 점의 위치벡터는 (n a + m b)/(m + n)", STEP=f"[[vec(p)]] = [[frac({n} vec(a) + {m} vec(b), {m + n})]] = ([[frac({n} × ({A[0]}) + {m} × ({B[0]}), {m + n})]], [[frac({n} × ({A[1]}) + {m} × ({B[1]}), {m + n})]]) = {_pt(*P)}", ASK="성분의 합")
            if r: out[f"in{A}_{B}_{m}_{n}"] = r
    for _ in range(40):
        G = _rnd2(-3, 3)
        A, B = _rnd2(-6, 6), _rnd2(-6, 6)
        C = (3 * G[0] - A[0] - B[0], 3 * G[1] - A[1] - B[1])
        if max(abs(v) for v in C) > 9 or A == B or B == C or A == C:
            continue
        q = f"무게중심 위치벡터 {A} {B} {C}"
        r = _row(q, sum(G), Q=f"세 점 A, B, C의 위치벡터가 각각 [[vec(a)]] = {_vc(*A)}, [[vec(b)]] = {_vc(*B)}, [[vec(c)]] = {_vc(*C)}일 때, 삼각형 ABC의 무게중심 G의 위치벡터 [[vec(g)]]의 모든 성분의 합을 구하시오.", LAW="삼각형 ABC의 무게중심의 위치벡터는 (a + b + c)/3", STEP=f"[[vec(g)]] = [[frac(vec(a) + vec(b) + vec(c), 3)]] = ([[frac({A[0]} + ({B[0]}) + ({C[0]}), 3)]], [[frac({A[1]} + ({B[1]}) + ({C[1]}), 3)]]) = {_pt(*G)}", ASK="성분의 합")
        if r: out[f"g{A}_{B}_{C}"] = r
    for p in range(1, 8):
        for q_ in range(1, 8):
            for dot in range(-12, 13):
                if abs(dot) > p * q_ or dot == 0:
                    continue
                v = p * p + q_ * q_ - 2 * dot
                if v <= 0:
                    continue
                q = f"|a|={p} |b|={q_} a·b={dot} |a−b|²"
                r = _row(q, v, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}, [[dot(vec(a), vec(b))]] = {dot}일 때, [[pow(abs(vec(a) − vec(b)), 2)]]의 값을 구하시오.", LAW="|a − b|² = (a − b)·(a − b) = |a|² − 2a·b + |b|²", STEP=f"|a − b|² = {p * p} − 2 × ({dot}) + {q_ * q_} = {v}", ASK="|a − b|²")
                if r: out[f"db{p}_{q_}_{dot}"] = r
    return _pick(out, 330)


VC2_ROWS = _vc2_rows()


def vc_t2():
    return T(VC, 2, VC_B, title="벡터의 크기와 위치벡터 — |a ± b|², 내분점·무게중심",
        skill="|a ± b|² = |a|² ± 2a·b + |b|²과 a·b = |a||b|cos θ로 크기를 구하고, 위치벡터로 내분점·무게중심 계산하기", axis={"묻는 것": "|a + b|² / |a − b|² / |a ± b| / 내분점 위치벡터 성분 합 / 무게중심", "각": "60°, 90°, 120°"}, disc="크기의 제곱을 내적으로 전개하고 2a·b 항의 부호를 맞추는가", diff=3,
        params=[{"name": "f", "values": {"in": list(VC2_ROWS)}}], table={"key": "f", "rows": VC2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "전개·공식"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["|a + b| ≤ |a| + |b|, |a − b| ≥ ||a| − |b||를 만족하는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("전개", 3, "{STEP} 꼴로 세웠다.", "2a·b 항을 빠뜨렸으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "cos 값·부호 실수면 1점.")],
        pitfalls=[("|a + b| = |a| + |b|로 둠", "전개", "불인정"), ("2a·b의 부호를 반대로 함", "전개", "부분"), ("내분점 공식에서 m, n을 바꿈", "값 구하기", "불인정")])


def _vc3_rows():
    out = {}
    for _ in range(60):
        a, b = _rnd2(), _rnd2()
        if a == (0, 0) or b == (0, 0):
            continue
        dot = a[0] * b[0] + a[1] * b[1]
        q = f"a{a} b{b} 내적"
        r = _row(q, dot, Q=f"두 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}에 대하여 [[dot(vec(a), vec(b))]]의 값을 구하시오.", LAW="내적: (a₁, a₂)·(b₁, b₂) = a₁b₁ + a₂b₂", STEP=f"[[dot(vec(a), vec(b))]] = {a[0]} × ({b[0]}) + ({a[1]}) × ({b[1]}) = {dot}", ASK="내적의 값")
        if r: out[f"d{a}_{b}"] = r
    for _ in range(40):
        a = _rnd3(-4, 4); b = _rnd3(-4, 4)
        if a == (0, 0, 0) or b == (0, 0, 0):
            continue
        dot = sum(a[i] * b[i] for i in range(3))
        q = f"3D a{a} b{b} 내적"
        r = _row(q, dot, Q=f"두 공간벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}에 대하여 [[dot(vec(a), vec(b))]]의 값을 구하시오.", LAW="내적: (a₁, a₂, a₃)·(b₁, b₂, b₃) = a₁b₁ + a₂b₂ + a₃b₃", STEP=f"[[dot(vec(a), vec(b))]] = {a[0]} × ({b[0]}) + ({a[1]}) × ({b[1]}) + ({a[2]}) × ({b[2]}) = {dot}", ASK="내적의 값")
        if r: out[f"d3{a}_{b}"] = r
    for _ in range(60):
        a1, a2, b1 = rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(-5, 5)
        k = rng.randint(-6, 6)
        if a2 == 0 or (a1, a2) == (0, 0):
            continue
        # 수직: a1 b1 + a2 k = 0 → k = -a1 b1 / a2
        kp = Fraction(-a1 * b1, a2)
        if kp.denominator == 1 and kp != 0 and b1 != 0:
            q = f"a({a1},{a2}) b({b1},k) 수직"
            r = _row(q, kp, Q=f"두 벡터 [[vec(a)]] = {_vc(a1, a2)}, [[vec(b)]] = [[vcomp({b1}, k)]]가 서로 수직일 때, 실수 k의 값을 구하시오.", LAW="두 벡터가 수직이면 내적이 0: a₁b₁ + a₂b₂ = 0", STEP=f"{a1} × ({b1}) + ({a2}) × k = 0에서 k = {_fm(kp)}", ASK="실수 k")
            if r: out[f"pk{a1}_{a2}_{b1}"] = r
        # 평행: a1 k − a2 b1 = 0 → k = a2 b1 / a1
        if a1 != 0:
            kl = Fraction(a2 * b1, a1)
            if kl.denominator == 1 and kl != 0 and b1 != 0:
                q = f"a({a1},{a2}) b({b1},k) 평행"
                r = _row(q, kl, Q=f"두 벡터 [[vec(a)]] = {_vc(a1, a2)}, [[vec(b)]] = [[vcomp({b1}, k)]]가 서로 평행할 때, 실수 k의 값을 구하시오.", LAW="두 벡터가 평행하면 성분이 비례한다: a₁ : b₁ = a₂ : b₂, 즉 a₁b₂ − a₂b₁ = 0", STEP=f"{a1} × k − ({a2}) × ({b1}) = 0에서 k = {_fm(kl)}", ASK="실수 k")
                if r: out[f"pl{a1}_{a2}_{b1}"] = r
        # a·b = k 주어짐 → 미지수 x: a1 b1 + a2 x = k
        x = rng.randint(-5, 5)
        val = a1 * b1 + a2 * x
        if x != 0:
            q = f"a({a1},{a2}) b({b1},x) 내적={val}"
            r = _row(q, x, Q=f"두 벡터 [[vec(a)]] = {_vc(a1, a2)}, [[vec(b)]] = [[vcomp({b1}, x)]]에 대하여 [[dot(vec(a), vec(b))]] = {val}일 때, 실수 x의 값을 구하시오.", LAW="내적: (a₁, a₂)·(b₁, b₂) = a₁b₁ + a₂b₂", STEP=f"{a1} × ({b1}) + ({a2}) × x = {val}에서 {_co(a2)}x = {val - a1 * b1}, x = {x}", ASK="실수 x")
            if r: out[f"px{a1}_{a2}_{b1}_{x}"] = r
    T2 = [(3, 4), (4, 3), (-3, 4), (3, -4), (5, 12), (12, 5), (-5, 12), (8, 15), (15, 8), (6, 8), (8, -6), (-4, 3)]
    for a in T2:
        for b in T2:
            if a == b or a == (-b[0], -b[1]):
                continue
            na, nb = math.isqrt(a[0] ** 2 + a[1] ** 2), math.isqrt(b[0] ** 2 + b[1] ** 2)
            dot = a[0] * b[0] + a[1] * b[1]
            if dot == 0:
                continue
            cs = Fraction(dot, na * nb)
            q = f"a{a} b{b} cos"
            r = _row(q, cs, Q=f"두 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}{_ika(str(b[-1]))} 이루는 각의 크기를 θ라 할 때, cos θ의 값을 구하시오.", LAW="cos θ = (a·b)/(|a||b|)", STEP=f"[[dot(vec(a), vec(b))]] = {dot}, [[abs(vec(a))]] = {na}, [[abs(vec(b))]] = {nb}이므로 cos θ = [[frac({dot}, {na * nb})]] = {_fm(cs)}", ASK="cos θ")
            if r: out[f"cs{a}_{b}"] = r
    for p in range(1, 8):
        for q_ in range(1, 8):
            for s_ in range(1, 15):
                dot2 = s_ * s_ - p * p - q_ * q_
                if dot2 % 2 or abs(dot2 // 2) > p * q_ or dot2 == 0:
                    continue
                dot = dot2 // 2
                q = f"|a|={p} |b|={q_} |a+b|={s_}"
                r = _row(q, dot, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}, [[abs(vec(a) + vec(b))]] = {s_}일 때, [[dot(vec(a), vec(b))]]의 값을 구하시오.", LAW="|a + b|² = |a|² + 2a·b + |b|²에서 a·b = (|a + b|² − |a|² − |b|²)/2", STEP=f"[[dot(vec(a), vec(b))]] = [[frac({s_ * s_} − {p * p} − {q_ * q_}, 2)]] = {dot}", ASK="내적의 값")
                if r: out[f"ab{p}_{q_}_{s_}"] = r
    for p in range(1, 9):
        for q_ in range(1, 9):
            if p == q_:
                continue
            q = f"|a|={p} |b|={q_} (a+b)(a−b)"
            r = _row(q, p * p - q_ * q_, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}일 때, [[dot((vec(a) + vec(b)), (vec(a) − vec(b)))]]의 값을 구하시오.", LAW="(a + b)·(a − b) = |a|² − |b|² (내적의 분배법칙, a·b = b·a)", STEP=f"(a + b)·(a − b) = {p * p} − {q_ * q_} = {p * p - q_ * q_}", ASK="내적의 값")
            if r: out[f"pm{p}_{q_}"] = r
    return _pick(out, 330)


VC3_ROWS = _vc3_rows()


def vc_t3():
    return T(VC, 3, VC_B, title="벡터의 내적 — 성분 계산·수직과 평행 조건·cos θ",
        skill="성분으로 내적을 계산하고, 수직(a·b = 0)·평행(성분 비례) 조건과 cos θ = a·b/(|a||b|), 크기와 내적의 관계 쓰기", axis={"묻는 것": "a·b / 수직·평행 조건 k / 미지수 x / cos θ / |a + b|에서 a·b / (a + b)·(a − b)", "값": "성분 −5~5, 크기는 피타고라스 삼조"}, disc="내적이 스칼라임을 알고 수직은 내적 0, 평행은 성분 비례로 구분하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(VC3_ROWS)}}], table={"key": "f", "rows": VC3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "내적의 정의·성질"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["|a·b| ≤ |a||b|인지, cos θ가 −1과 1 사이인지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("식 세우기", 3, "{STEP} 꼴로 세웠다.", "수직과 평행 조건을 바꿔 썼으면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "부호·약분 실수면 1점.")],
        pitfalls=[("수직 조건을 성분 비례로 둠", "식 세우기", "불인정"), ("내적을 벡터 (a₁b₁, a₂b₂)로 둠", "식 세우기", "불인정"), ("cos θ 분모에 |a||b| 대신 |a|² 사용", "값 구하기", "부분")])


def _vc4_rows():
    out = {}
    P2 = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (2, -1), (-1, 2), (3, -1), (2, 3), (3, 2), (1, -2), (-2, 1), (-1, -1), (2, 2), (3, 3), (-3, 1)]
    def ang(a, b):
        dot = sum(x * y for x, y in zip(a, b)); na2 = sum(x * x for x in a); nb2 = sum(x * x for x in b)
        if dot == 0: return 90
        c2 = Fraction(dot * dot, na2 * nb2)
        for th, v in ((0, Fraction(1)), (45, Fraction(1, 2)), (60, Fraction(1, 4)), (30, Fraction(3, 4))):
            if c2 == v:
                return th if dot > 0 else 180 - th
        return None
    for a in P2:
        for b in P2:
            if a == b:
                continue
            th = ang(a, b)
            if th is None or th in (0, 180):
                continue
            dot = a[0] * b[0] + a[1] * b[1]; na2 = a[0] ** 2 + a[1] ** 2; nb2 = b[0] ** 2 + b[1] ** 2
            q = f"각 a{a} b{b}"
            r = _row(q, th, Q=f"두 벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}{_ika(str(b[-1]))} 이루는 각의 크기를 구하시오.", LAW="cos θ = (a·b)/(|a||b|) (0° ≤ θ ≤ 180°)", STEP=f"[[dot(vec(a), vec(b))]] = {dot}, [[abs(vec(a))]] = [[sqrt({na2})]], [[abs(vec(b))]] = [[sqrt({nb2})]]이므로 cos θ = [[frac({dot}, sqrt({na2 * nb2}))]] = {_cosd(th)}", ASK="두 벡터가 이루는 각")
            if r: out[f"2d{a}_{b}"] = r
    P3 = [(1, 1, 0), (1, 0, 1), (0, 1, 1), (1, -1, 0), (-1, 0, 1), (0, 1, -1), (1, 1, 1), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 2), (2, 1, -2), (-2, 2, 1), (2, 2, 1), (1, 1, -1)]
    for a in P3:
        for b in P3:
            if a == b:
                continue
            th = ang(a, b)
            if th is None or th in (0, 180):
                continue
            dot = sum(x * y for x, y in zip(a, b)); na2 = sum(x * x for x in a); nb2 = sum(x * x for x in b)
            q = f"각 3D a{a} b{b}"
            r = _row(q, th, Q=f"두 공간벡터 [[vec(a)]] = {_vc(*a)}, [[vec(b)]] = {_vc(*b)}{_ika(str(b[-1]))} 이루는 각의 크기를 구하시오.", LAW="cos θ = (a·b)/(|a||b|) (0° ≤ θ ≤ 180°)", STEP=f"[[dot(vec(a), vec(b))]] = {dot}, [[abs(vec(a))]] = [[sqrt({na2})]], [[abs(vec(b))]] = [[sqrt({nb2})]]이므로 cos θ = [[frac({dot}, sqrt({na2 * nb2}))]] = {_cosd(th)}", ASK="두 벡터가 이루는 각")
            if r: out[f"3d{a}_{b}"] = r
    for p in range(1, 7):
        for q_ in range(1, 7):
            for th, cs in ((60, Fraction(1, 2)), (120, Fraction(-1, 2)), (90, Fraction(0)), (0, Fraction(1)), (180, Fraction(-1))):
                dot = p * q_ * cs
                if dot.denominator != 1 or th in (0, 180):
                    continue
                dot = int(dot)
                q = f"|a|={p} |b|={q_} a·b={dot} 각"
                r = _row(q, th, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}, [[dot(vec(a), vec(b))]] = {dot}일 때, 두 벡터가 이루는 각의 크기를 구하시오.", LAW="cos θ = (a·b)/(|a||b|) (0° ≤ θ ≤ 180°)", STEP=f"cos θ = [[frac({dot}, {p * q_})]] = {_cosd(th)}", ASK="두 벡터가 이루는 각")
                if r: out[f"n{p}_{q_}_{th}"] = r
                # |a + b| 주어짐 → 각
                s2 = p * p + q_ * q_ + 2 * dot
                s_ = math.isqrt(s2)
                if s_ * s_ == s2 and s_ > 0:
                    r2 = _row(f"|a|={p} |b|={q_} |a+b|={s_} 각", th, Q=f"두 벡터 [[vec(a)]], [[vec(b)]]에 대하여 [[abs(vec(a))]] = {p}, [[abs(vec(b))]] = {q_}, [[abs(vec(a) + vec(b))]] = {s_}일 때, 두 벡터가 이루는 각의 크기를 구하시오.", LAW="|a + b|² = |a|² + 2a·b + |b|²에서 a·b를 구한 뒤 cos θ = (a·b)/(|a||b|)", STEP=f"{s_ * s_} = {p * p} + 2a·b + {q_ * q_}에서 a·b = {dot}, cos θ = [[frac({dot}, {p * q_})]] = {_cosd(th)}", ASK="두 벡터가 이루는 각")
                    if r2: out[f"s{p}_{q_}_{th}"] = r2
    return _pick(out, 330)


def _cosd(th):
    return {30: "[[frac(sqrt(3), 2)]]", 45: "[[frac(sqrt(2), 2)]]", 60: "[[frac(1,2)]]", 90: "0", 120: "[[-frac(1,2)]]", 135: "[[-frac(sqrt(2), 2)]]", 150: "[[-frac(sqrt(3), 2)]]"}[th]


VC4_ROWS = _vc4_rows()


def vc_t4():
    return T(VC, 4, VC_B, title="두 벡터가 이루는 각",
        skill="cos θ = a·b/(|a||b|)로 두 벡터가 이루는 각(30°·45°·60°·90°·120°·135°·150°)을 구하기", axis={"주어진 것": "성분(평면·공간) / 크기와 내적 / 크기와 |a + b|", "각": "30°~150°"}, disc="내적의 부호로 예각·둔각을 구분하고 cos 값에서 각을 정확히 읽는가", diff=3,
        params=[{"name": "f", "values": {"in": list(VC4_ROWS)}}], table={"key": "f", "rows": VC4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="[[deg({ans})]]",
        sol1="{LAW}. 내적과 크기를 구해 cos θ를 계산하고 0° ≤ θ ≤ 180°에서 θ를 읽는다.",
        sol2=[("{LAW}", "내적과 각"), ("{STEP}", "계산"), ("θ = {ans}°", None, ("{ans}", "θ"))],
        sol3=["내적이 음수면 둔각, 양수면 예각, 0이면 직각인지 확인한다. 따라서 θ = {ans}°이다.", "{STEP}", "답 {ans}°"],
        model="{LAW}. {STEP}이므로 θ = {ans}°이다.",
        rubric=[("cos θ 구하기", 3, "{STEP} 꼴로 세웠다.", "분모를 |a||b|가 아닌 값으로 두었으면 1점."), ("각 읽기", 2, "θ = {ans}°를 구했다.", "예각·둔각을 바꿨으면 1점.")],
        pitfalls=[("cos θ가 음수인데 예각으로 답함", "각 읽기", "불인정"), ("|a||b| 대신 |a|²|b|²으로 나눔", "cos θ 구하기", "불인정"), ("cos 60° = √3/2로 둠", "각 읽기", "불인정")])


DIRS = [(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 3, 6), (3, 6, 2), (6, 2, 3), (1, 4, 8), (4, 8, 1), (4, 4, 7), (2, 6, 9), (3, 4, 12)]


def _ln(var, c, d):
    """(var − c)/d 마커 조각 — d = 1 이면 var − c 만."""
    inner = f"{var} {_sg(-c)}".strip()
    return inner if d == 1 else f"[[frac({inner}, {d})]]"


def _line(P, u):
    return f"{_ln('x', P[0], u[0])} = {_ln('y', P[1], u[1])} = {_ln('z', P[2], u[2])}"


def _lastc(s):
    """조사 판정용 마지막 글자 — 마커 닫힘 ']]'·괄호를 벗긴다."""
    t = s.rstrip("]) ")
    return t[-1] if t else s


def _lead(v):
    """첫 성분(0이 아닌)이 양수가 되도록 부호를 맞춘 벡터."""
    for x in v:
        if x != 0:
            return tuple(y if x > 0 else -y for y in v)
    return tuple(v)


def _plane(n, d):
    tail = f"+ {d}" if isinstance(d, str) else _sg(d)
    s = f"{_co(n[0])}x {_sgv(n[1], 'y')} {_sgv(n[2], 'z')} {tail} = 0".replace("  ", " ")
    return s


def _vc5_rows():
    out = {}
    for u in DIRS:
        for v in DIRS:
            if u == v:
                continue
            for _ in range(2):
                su = _lead(tuple(x * rng.choice((1, -1)) for x in u)); sv = _lead(tuple(x * rng.choice((1, -1)) for x in v))
                nu, nv = math.isqrt(sum(x * x for x in su)), math.isqrt(sum(x * x for x in sv))
                dot = sum(x * y for x, y in zip(su, sv))
                if dot == 0 or abs(dot) == nu * nv or any(abs(x) == 1 for x in su) or any(abs(x) == 1 for x in sv):
                    continue
                P, Qp = _rnd3(-3, 3), _rnd3(-3, 3)
                cs = Fraction(abs(dot), nu * nv)
                q = f"두 직선 각 {su} {sv}"
                r = _row(q, cs, Q=f"두 직선 {_line(P, su)}, {_line(Qp, sv)}{_ika(_lastc(_line(Qp, sv)))} 이루는 각의 크기를 θ라 할 때, cos θ의 값을 구하시오.", LAW="두 직선이 이루는 각은 방향벡터 u, v로 cos θ = |u·v|/(|u||v|) (0° ≤ θ ≤ 90°)", STEP=f"방향벡터 {_vc(*su)}, {_vc(*sv)}에서 u·v = {dot}, |u| = {nu}, |v| = {nv}이므로 cos θ = [[frac({abs(dot)}, {nu * nv})]] = {_fm(cs)}", ASK="cos θ")
                if r: out[f"ll{su}_{sv}_{P}"] = r
    for n in DIRS:
        for _ in range(10):
            sn = _lead(tuple(x * rng.choice((1, -1)) for x in n))
            P = _rnd3(-3, 3)
            s_ = rng.choice((1, 2, -1, -2))
            u = _lead(tuple(s_ * x for x in sn))
            s_ = u[0] // sn[0]                       # _lead 로 부호가 바뀌었을 수 있으므로 다시 계산
            idx = rng.randint(0, 2)
            k = u[idx]
            d = rng.randint(-5, 5)
            shown = list(u); shown[idx] = "k"
            if any(abs(x) == 1 for x in u):
                continue
            line = f"{_ln('x', P[0], shown[0])} = {_ln('y', P[1], shown[1])} = {_ln('z', P[2], shown[2])}"
            q = f"직선 평면 수직 {sn} k={k}"
            r = _row(q, k, Q=f"직선 {line}{_ika(_lastc(line))} 평면 {_plane(sn, d)}에 수직일 때, 상수 k의 값을 구하시오.", LAW="직선이 평면에 수직이면 직선의 방향벡터와 평면의 법선벡터가 평행하다", STEP=f"방향벡터 {_vc(*shown)}과 법선벡터 {_vc(*sn)}이 평행하므로 {_vc(*shown)} = {s_} × {_vc(*sn)}에서 k = {k}", ASK="상수 k")
            if r: out[f"lp{sn}_{P}_{idx}_{s_}"] = r
            # 평행: u·n = 0
            u2 = list(_rnd3(-4, 4))
            j = rng.randint(0, 2)
            others = sum(u2[i] * sn[i] for i in range(3) if i != j)
            kk = Fraction(-others, sn[j])
            if kk.denominator != 1 or kk == 0:
                continue
            shown2 = list(u2); shown2[j] = "k"
            if any(x == 0 for i, x in enumerate(u2) if i != j):
                continue
            line2 = f"{_ln('x', P[0], shown2[0])} = {_ln('y', P[1], shown2[1])} = {_ln('z', P[2], shown2[2])}"
            q2 = f"직선 평면 평행 {sn} {u2} k={kk}"
            r2 = _row(q2, kk, Q=f"직선 {line2}{_ika(_lastc(line2))} 평면 {_plane(sn, d)}과 평행할 때, 상수 k의 값을 구하시오. (단, 직선은 평면 위에 있지 않다.)", LAW="직선이 평면과 평행하면 직선의 방향벡터와 평면의 법선벡터가 수직: u·n = 0", STEP=f"방향벡터 {_vc(*shown2)}과 법선벡터 {_vc(*sn)}의 내적이 0이므로 " + " + ".join(f"({shown2[i]}) × ({sn[i]})" for i in range(3)) + f" = 0에서 k = {int(kk)}", ASK="상수 k")
            if r2: out[f"pl{sn}_{P}_{j}_{tuple(u2)}"] = r2
    for n in DIRS:
        for _ in range(9):
            sn = _lead(tuple(x * rng.choice((1, -1)) for x in n))
            nn = math.isqrt(sum(x * x for x in sn))
            P = _rnd3(-5, 5)
            d = rng.randint(-9, 9)
            val = sum(sn[i] * P[i] for i in range(3)) + d
            if val == 0:
                continue
            dist = Fraction(abs(val), nn)
            terms = " + ".join(f"{f'({sn[i]})' if sn[i] < 0 else sn[i]} × ({P[i]})" for i in range(3)) + f" {_sg(d)}"
            tail = "" if (dist.numerator == abs(val) and dist.denominator == nn) else f" = {_fm(dist)}"
            sub = f"[[frac(abs({terms.strip()}), sqrt(pow({sn[0]},2) + pow({sn[1]},2) + pow({sn[2]},2)))]] = [[frac({abs(val)}, {nn})]]{tail}"
            q = f"점 평면 거리 {P} {sn} {d}"
            r = _row(q, dist, Q=f"점 {_pt(*P)}{_wa(str(P[2]))} 평면 {_plane(sn, d)} 사이의 거리를 구하시오.", LAW="점 (x₁, y₁, z₁)과 평면 ax + by + cz + d = 0 사이의 거리는 |ax₁ + by₁ + cz₁ + d|/√(a² + b² + c²)", STEP=sub, ASK="점과 평면 사이의 거리")
            if r: out[f"dp{P}_{sn}_{d}"] = r
            r2 = _row(q, dist, Q=f"중심이 {_pt(*P)}인 구가 평면 {_plane(sn, d)}에 접할 때, 이 구의 반지름의 길이를 구하시오.", LAW="구가 평면에 접하면 반지름은 중심에서 평면까지의 거리", STEP=f"반지름 = {sub}", ASK="반지름의 길이")
            if r2: out[f"sp{P}_{sn}_{d}"] = r2
            if dist.denominator == 1:
                for x, y, h in TRI:
                    if x == dist:
                        e = f"[[{_pw('x', P[0])} + {_pw('y', P[1])} + {_pw('z', P[2])} = {h * h}]]"
                        r3 = _row(f"구 평면 교선 {P} {sn} {d} r={h}", y, Q=f"구 {e}{_wa(str(h * h))} 평면 {_plane(sn, d)}이 만나서 생기는 원의 반지름의 길이를 구하시오.", LAW="중심에서 평면까지의 거리 d, 구의 반지름 r이면 교선인 원의 반지름은 √(r² − d²)", STEP=f"중심 {_pt(*P)}에서 평면까지의 거리는 [[frac({abs(val)}, {nn})]] = {x}이므로 원의 반지름은 [[sqrt(pow({h},2) − pow({x},2))]] = {y}", ASK="원의 반지름의 길이")
                        if r3: out[f"cr{P}_{sn}_{d}_{h}"] = r3
                        break
    for _ in range(80):
        n = _lead(_rnd3(-4, 4)); P = _rnd3(-4, 4)
        if 0 in n:
            continue
        D = -sum(n[i] * P[i] for i in range(3))
        if D == 0:
            continue
        q = f"평면 법선 {n} 점 {P}"
        r = _row(q, D, Q=f"점 {_pt(*P)}{_eul(str(P[2]))} 지나고 법선벡터가 {_vc(*n)}인 평면의 방정식이 {_plane(n, 'D')}일 때, 상수 D의 값을 구하시오.", LAW="법선벡터 (a, b, c)인 평면은 ax + by + cz + D = 0 꼴이고, 지나는 점을 대입해 D를 구한다", STEP=f"{n[0]} × ({P[0]}) + ({n[1]}) × ({P[1]}) + ({n[2]}) × ({P[2]}) + D = 0에서 D = {D}", ASK="상수 D")
        if r: out[f"pn{n}_{P}"] = r
    return _pick(out, 330)


VC5_ROWS = _vc5_rows()


def vc_t5():
    return T(VC, 5, VC_B, title="공간에서 직선과 평면의 방정식 — 각·수직·평행·거리·구",
        skill="직선의 방향벡터와 평면의 법선벡터로 각·수직·평행 조건을 세우고, 점과 평면 사이의 거리·구와 평면의 관계 계산하기", axis={"묻는 것": "두 직선의 cos θ / 수직·평행 조건 k / 점과 평면 거리 / 접하는 구 반지름 / 교선 원 반지름 / 평면의 방정식 D", "값": "방향·법선벡터는 (1,2,2)·(2,3,6)… 크기가 정수"}, disc="방향벡터·법선벡터를 정확히 읽고 수직(평행 벡터)·평행(내적 0) 조건을 구분하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(VC5_ROWS)}}], table={"key": "f", "rows": VC5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {ASK}를 묻는다.",
        sol2=[("{LAW}", "방향벡터·법선벡터"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["직선 ⊥ 평면이면 방향벡터 ∥ 법선벡터, 직선 ∥ 평면이면 방향벡터 ⊥ 법선벡터임을 다시 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("조건 세우기", 3, "{STEP} 꼴로 세웠다.", "수직과 평행 조건을 바꿨으면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("직선 ⊥ 평면을 방향벡터·법선벡터 = 0으로 둠", "조건 세우기", "불인정"), ("거리 공식에서 절댓값·제곱근을 빠뜨림", "값 구하기", "불인정"), ("분모 (x − a)/l에서 방향벡터를 (a, b, c)로 읽음", "조건 세우기", "불인정")])


VC_SEED = SEED(VC, category="도형", title="벡터 — 성분 연산·크기와 위치벡터·내적·두 벡터가 이루는 각·직선과 평면", unit_id="h3-3", concept_ids=["h3-3-14", "h3-3-15", "h3-3-16", "h3-3-17", "h3-3-18", "h3-3-19", "h3-3-20", "h3-3-21"],
               schema_name="벡터", note="vec/vcomp/dot/abs 마커. 각은 [[deg(n)]] 답(30°~150°), cos θ 는 분수. 직선·평면은 방향·법선벡터의 크기가 정수인 사조만.",
               templates=[vc_t1(), vc_t2(), vc_t3(), vc_t4(), vc_t5()])


if __name__ == "__main__":
    run(CN_SEED, SP_SEED, VC_SEED)
