# itemfactory/tools/recheck.py — 독립 검산 + 한국어·표기 품질 검사 (v1.0)
#
# audit.py 가 '규격'을 보는 것이라면, 이 도구는 **내용**을 본다.
#   ① 독립 검산: 시드·파라미터를 쓰지 않고 **발문 텍스트에서 수를 다시 읽어** 답을 재계산한다
#      (설계문서 v0.1 §4 "독립 검산 20,008건 전수 일치"와 같은 정신)
#   ② 도형–문면 정합: scene 삼각형은 좌표에서 각을 실제로 재서 라벨과 대조, sector 각·numline 범위·coordplane 점
#   ③ 한국어 조사·표기: 숫자 뒤 조사, '+ -6', '÷ 1', '1x', '(12)', 마크다운 찌꺼기
#
#   python tools/recheck.py out/gen

import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from genkit.expr import _has_jong   # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out/gen")
prob = Counter()
ex = defaultdict(list)


def bad(code, it, msg=""):
    prob[code] += 1
    if len(ex[code]) < 4:
        ex[code].append(f"{it['template_id']}#{it['param_index']} {msg}")


def nums(text):
    return [Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?:\.\d+)?(?![\d.])", text)]


def ans_val(it):
    a = re.sub(r"^\[\[|\]\]$", "", it["answer"]).strip()
    m = re.fullmatch(r"(-?\d+)\s*\*\s*pi", a)
    if m:
        return Fraction(m.group(1)), "pi"
    m = re.fullmatch(r"deg\((-?\d+)\)", a)
    if m:
        return Fraction(m.group(1)), "deg"
    m = re.fullmatch(r"-?frac\((\d+),(\d+)\)", a)
    if m:
        v = Fraction(int(m.group(1)), int(m.group(2)))
        return (-v if a.startswith("-") else v), "frac"
    try:
        return Fraction(a), "num"
    except ValueError:
        return None, "?"


# ── ① 독립 검산 — 발문에서 수를 읽어 다시 푼다 ─────────────────────────────
def recompute(it):
    tid, q = it["template_id"], it["question"]
    n = nums(q)
    if tid.startswith("m1-1-numline-mid-t1") or tid.startswith("m1-1-numline-mid-t3"):
        a, b = n[0], n[1]; return (a + b) / 2
    if tid.startswith("m1-1-numline-mid-t2"):
        a, m = n[0], n[1]; return 2 * m - a
    if tid.startswith("m1-2-sector-arc-t1"):
        th, r = n[0], n[1]; return 2 * r * th / 360            # π 계수
    if tid.startswith("m1-2-sector-arc-t2"):
        th, kl = n[0], n[1]; return kl * 360 / (2 * th)
    if tid.startswith("m1-2-sector-arc-t3"):
        th, r = n[0], n[1]; return r * r * th / 360
    if tid.startswith("m1-2-tri-angle-t1") or tid.startswith("m1-2-tri-angle-t3"):
        a, b = n[0], n[1]; return 180 - a - b
    if tid.startswith("m1-2-tri-angle-t2"):
        a, e = n[0], n[1]; return e - a
    if tid.startswith("m1-2-cylinder-volume-t1") or tid.startswith("m1-2-cylinder-volume-t3"):
        r, h = n[0], n[1]; return r * r * h
    if tid.startswith("m1-2-cylinder-volume-t2"):
        h, kv = n[0], n[1]
        rr = kv / h; r = int(round(math.sqrt(rr)))
        return Fraction(r) if r * r == rr else None
    if tid.startswith("m1-2-polygon-angles-t1"):
        return 180 * (n[0] - 2)
    if tid.startswith("m1-2-polygon-angles-t2"):
        return n[0] / 180 + 2
    if tid.startswith("m1-2-polygon-angles-t3"):
        k = n[0]; return 180 * (k - 2) / k
    if tid.startswith("m1-1-train-tunnel-t1"):
        B1, t1, B2, t2 = n[0], n[1], n[2], n[3]; return (t1 * B2 - t2 * B1) / (t2 - t1)
    if tid.startswith("m1-1-train-tunnel-t2"):
        B1, t1, B2, t2 = n[0], n[1], n[2], n[3]; return (B2 - B1) / (t2 - t1)
    if tid.startswith("m1-1-mixture-t1") or tid.startswith("m1-1-mixture-t3"):
        p, x, q, y = n[0], n[1], n[2], n[3]; return (p * x + q * y) / (x + y)
    if tid.startswith("m1-1-mixture-t2"):
        p, x, w = n[0], n[1], n[2]; return p * x / (x - w)
    if tid.startswith("m2-1-line-equation-t1"):
        a, px, py = n[0], n[1], n[2]; return py - a * px
    if tid.startswith("m2-1-line-equation-t2"):
        x1, y1, x2, y2 = n[0], n[1], n[2], n[3]; return (y2 - y1) / (x2 - x1)
    if tid.startswith("m1-1-speed-trip-t1"):
        a, b, T = n[0], n[1], n[2]; return T * a * b / (a + b)
    if tid.startswith("m1-1-speed-trip-t2"):
        D, v1, v2, T = n[0], n[1], n[2], n[3]; return v1 * (T * v2 - D) / (v2 - v1)
    if tid.startswith("m1-1-linear-eq-tricks-t1"):
        a, m, b, nn, c = n[0], n[1], n[2], n[3], n[4]; return (c * m * nn + b * m - a * nn) / (m + nn)
    if tid.startswith("m1-1-linear-eq-tricks-t2"):
        A, b, R = n[0], n[1], n[2]; return b + R / A
    if tid.startswith("m2-1-river-boat"):
        D, t1, t2 = n[0], n[1], n[2]; return Fraction(D, 2) * (Fraction(1, t1) + Fraction(1, t2))
    if tid.startswith("m2-1-river-stream"):
        D, t1, t2 = n[0], n[1], n[2]; return Fraction(D, 2) * (Fraction(1, t1) - Fraction(1, t2))
    if tid.startswith("m2-1-mountain-up"):
        a, b, D, T = n[0], n[1], n[2], n[3]; return Fraction(a * (b * T - D), b - a)
    if tid.startswith("m2-1-mountain-down"):
        a, b, D, T = n[0], n[1], n[2], n[3]; return D - Fraction(a * (b * T - D), b - a)
    if tid.startswith("m1-2-parallel-angles"):
        a, c = n[0], n[1]; return a + c
    # ── 09-09 세션 1: 일차방정식 활용 (나이·연속수·과부족·구매)
    if tid.startswith("m1-1-age-t1"):
        F, S, k = n[0], n[1], n[2]; return (F - k * S) / (k - 1)                # F + x = k(S + x)
    if tid.startswith("m1-1-age-t2"):
        T, k, d = n[0], n[1], n[2]; return (T - d) / (k + 1)                    # S + (kS + d) = T
    if tid.startswith("m1-1-age-t3"):
        F, S, k = n[0], n[1], n[2]; return (k * S - F) / (k - 1)                # F − x = k(S − x)
    if tid.startswith("m1-1-consecutive-t1"):
        S = n[0]; m = S / 3; return m + (1 if "가장 큰" in q else -1)
    if tid.startswith("m1-1-consecutive-t2"):
        S = n[0]; m = S / 3; return m + (2 if "가장 큰" in q else -2)
    if tid.startswith("m1-1-consecutive-t3"):
        k, d = n[0], n[1]; x = (1 + d - 2 * k) / (k - 2)                       # k(x+2) = 2x+1+d
        return 3 * x + 3 if "합을 구하" in q else x + 2
    if tid.startswith("m1-1-surplus-t1") or tid.startswith("m1-1-surplus-t2"):
        a, b, c, d = n[0], n[1], n[2], n[3]; x = (b + d) / (c - a)              # ax + b = cx − d
        return x if tid.startswith("m1-1-surplus-t1") else a * x + b
    if tid.startswith("m1-1-surplus-t3"):
        a, b, c, d = n[0], n[1], n[2], n[3]; return (b + c * d) / (c - a)       # ax + b = c(x − d)
    if tid.startswith("m1-1-purchase-t1"):
        pa, pb, nn, T = n[0], n[1], n[2], n[3]; return (T - pb * nn) / (pa - pb)
    if tid.startswith("m1-1-purchase-t2"):
        pa, pb, nn, P, C = n[0], n[1], n[2], n[3], n[4]; x = (P - C - pb * nn) / (pa - pb); return nn - x
    if tid.startswith("m1-1-purchase-t3"):
        pa, pb, k, T = n[0], n[1], n[2], n[3]; return (T - pa * k) / (pa + pb)
    # ── 최대공약수·최소공배수 활용 (문면의 수를 정수로 다시 읽는다)
    if tid.startswith("m1-1-gcd-lcm-apply-t1"):
        a, b = [int(x) for x in re.findall(r"(\d+)분 간격", q)][:2]; return Fraction(a * b // math.gcd(a, b))   # 노선 이름의 숫자(1호선·101번)를 피해 '분 간격' 앞의 수만 읽는다
    if tid.startswith("m1-1-gcd-lcm-apply-t2"):
        a, b = int(n[0]), int(n[1]); L = a * b // math.gcd(a, b)
        return Fraction(L // a if "톱니바퀴 A는" in q else L // b)
    if tid.startswith("m1-1-gcd-lcm-apply-t3") or tid.startswith("m1-1-gcd-lcm-apply-t4"):
        a, b = int(n[0]), int(n[1]); g = math.gcd(a, b)
        return Fraction(g if tid.startswith("m1-1-gcd-lcm-apply-t3") else (a // g) * (b // g))
    if tid.startswith("m1-1-gcd-lcm-apply-t5"):
        G, L = n[0], n[1]; return G * L
    if tid.startswith("m1-1-gcd-lcm-apply-t6"):
        P, G = n[0], n[1]; return P / G
    if tid.startswith("m1-1-gcd-lcm-apply-t7"):
        P, L = n[0], n[1]; return P / L
    # ── 평면도형 (09-09) — 다각형 이름은 한글 수사로 되읽는다
    if tid.startswith("m1-2-polygon-diagonal-t1"):
        nn = _kor_polygon(q)
        if "총 개수" in q: return Fraction(nn * (nn - 3), 2)
        if "삼각형" in q: return nn - 2
        return nn - 3
    if tid.startswith("m1-2-polygon-diagonal-t2"):
        D = n[0]; nn = (3 + math.isqrt(9 + 8 * int(D))) // 2; return Fraction(nn) if nn * (nn - 3) == 2 * D else None
    if tid.startswith("m1-2-polygon-diagonal-t3"):
        k = n[0]; nn = k + 3; return nn if "변의 개수" in q else nn * (nn - 3) / 2
    if tid.startswith("m1-2-polygon-diagonal-t4"):
        S = n[0]; nn = S / 180 + 2; return nn * (nn - 3) / 2
    if tid.startswith("m1-2-angle-basic-t1"):
        a, b = n[0], n[1]; return 180 * a / (a + b) if "angle(AOB)]]의 크기" in q else 180 * b / (a + b)
    if tid.startswith("m1-2-angle-basic-t2"):
        mm = re.findall(r"\((\d*)x \+ (\d+)\)°", q)
        (_, p), (m, qq) = [(Fraction(g[0] or 1), Fraction(g[1])) for g in mm[:2]]
        x = (180 - p - qq) / (m + 1); return x + p                                       # (x+p) + (mx+q) = 180 → ∠AOB
    if tid.startswith("m1-2-angle-basic-t3"):
        mm = re.findall(r"\((\d*)x \+ (\d+)\)°", q)                                    # 계수 1은 'x + b' 로 적힌다
        (a, b), (c, d) = [(Fraction(g[0] or 1), Fraction(g[1])) for g in mm[:2]]
        x = (d - b) / (a - c); return a * x + b                                          # ax+b = cx+d → ∠AOC
    # ── 평균 (09-09)
    if tid.startswith("m1-2-mean-t1"):
        m, v1, v2, v3, v4 = n[-5], n[-4], n[-3], n[-2], n[-1]; return 5 * m - (v1 + v2 + v3 + v4)
    if tid.startswith("m1-2-mean-t2"):
        (n1, m1), (n2, m2) = [(Fraction(u), Fraction(v)) for u, v in re.findall(r"(\d+)명의 [^,]*?평균은 (\d+)", q)][:2]   # '1학년 회원' 의 숫자를 피한다
        return (n1 * m1 + n2 * m2) / (n1 + n2)
    if tid.startswith("m1-2-mean-t3") or tid.startswith("m1-2-mean-t4") or tid.startswith("m1-2-mean-t5"):
        nn, m, M = n[0], n[1], n[2]; return (nn + 1) * M - nn * m
    # ── 입체도형 (09-09)
    if tid.startswith("m1-2-cylinder-surface-t1") or tid.startswith("m1-2-cylinder-surface-t5"):
        r, h = n[0], n[1]; return 2 * r * r + 2 * r * h
    if tid.startswith("m1-2-cylinder-surface-t2"):
        r, S = n[0], n[1]; return (S - 2 * r * r) / (2 * r)
    if tid.startswith("m1-2-cylinder-surface-t3"):
        h, A = n[0], n[1]; return A / (2 * h)
    if tid.startswith("m1-2-cylinder-surface-t4"):
        a, b, c = n[0], n[1], n[2]; return 2 * (a * b + b * c + c * a)
    if tid.startswith("m1-2-cone-t1") or tid.startswith("m1-2-cone-t5"):
        g, h = n[0], n[1]; r = g / 2 if "지름의 길이" in q and "반지름" not in q else g
        return r * r * h / 3
    if tid.startswith("m1-2-cone-t2"):
        r, l = n[0], n[1]; return r * r + r * l
    if tid.startswith("m1-2-cone-t3"):
        r, l = n[0], n[1]; return 360 * r / l
    if tid.startswith("m1-2-cone-t4"):
        a, h = n[0], n[1]; return a * a * h / 3
    if tid.startswith("m1-2-sphere-t1"):
        r = n[0]; return 3 * r * r if "반구" in q else 4 * r * r
    if tid.startswith("m1-2-sphere-t2"):
        g = n[0]; r = g / 2 if q.startswith("지름") else g
        v = Fraction(4, 3) * r * r * r
        return v / 2 if "반구" in q else v
    if tid.startswith("m1-2-sphere-t3"):
        V = n[0]; return V * 2 / 3
    if tid.startswith("m1-1-abs-pair-t1"):
        d = n[0]; return d / 2 if "큰 수를 구하" in q else -d / 2
    if tid.startswith("m1-1-abs-pair-t2"):
        a = n[0]; return 2 * a + 1 if "이하" in q else 2 * a - 1
    if tid.startswith("m1-1-abs-pair-t3"):
        N, de = n[0], n[1]; return 2 * math.floor(N / de) + 1
    # ── 일차부등식 (09-09) — 풀이 t1·t2 는 문자열 답이라 check_ineq 가 맡는다
    if tid.startswith("m2-1-ineq-solve-t3"):
        a, b, c = n[0], n[1], n[2]; bd = (c + b) / a                           # ax − b ≤ c  또는  <
        return Fraction(math.floor(bd)) if "≤" in q else Fraction(math.ceil(bd) - 1)
    if tid.startswith("m2-1-ineq-solve-t4"):
        m = re.search(r"ax ([+−]) (\d+) > (-?\d+)의 해가 x < (-?\d+)", q)
        b = Fraction(m.group(2)) * (1 if m.group(1) == "+" else -1); c, k = Fraction(m.group(3)), Fraction(m.group(4))
        return (c - b) / k                                                      # ax > c − b, 해 x < k ⇒ a = (c − b)/k (< 0)
    if tid.startswith("m2-1-ineq-choice-t1"):
        a, b = [Fraction(x) for x in re.findall(r"(\d+)원", q)][:2]; return Fraction(math.floor(b / a) + 1)   # ax > b
    if tid.startswith("m2-1-ineq-choice-t2"):
        a, f = [Fraction(x) for x in re.findall(r"(\d+)원", q)][:2]; p = Fraction(re.search(r"(\d+)%", q).group(1))
        return Fraction(math.floor(f / (a * p / 100)) + 1)                     # (a − oa)x > f
    if tid.startswith("m2-1-ineq-choice-t3"):
        B, a, f = [Fraction(x) for x in re.findall(r"(\d+)원", q)][:3]; return Fraction(math.floor((B - f) / a))   # ax + f ≤ B
    if tid.startswith("m2-1-ineq-choice-t4"):
        a1, F, a2 = [Fraction(x) for x in re.findall(r"(\d+)원", q)][:3]; return Fraction(math.floor(F / (a1 - a2)) + 1)   # a1 x > F + a2 x
    # ── 연립방정식의 활용 (09-09)
    if tid.startswith("m2-1-sys-apply-t1"):
        s, d = n[0], n[1]; k = d / 9; sg = 1 if "크다" in q else -1                # x + y = s, y − x = ±k
        y = (s + sg * k) / 2; x = s - y; return 10 * x + y
    if tid.startswith("m2-1-sys-apply-t2"):
        nn, p, qq, T = n[0], n[1], n[2], n[3]; return (T + qq * nn) / (p + qq)       # x + y = n, px − qy = T
    if tid.startswith("m2-1-sys-apply-t3"):
        S, a, b = n[0], n[1], n[2]
        m = re.search(r"(\d+)명 (늘었다|줄었다)", q); D = Fraction(m.group(1)); sg = 1 if m.group(2) == "늘었다" else -1
        x = (sg * 100 * D + b * S) / (a + b)                                         # x + y = S, ax/100 − by/100 = ±D
        return x * (1 + a / 100) if re.search(r"올해 [^.]*수를 구하시오", q) else x
    if tid.startswith("m2-1-sys-apply-t4"):
        m1, n1, T1, m2, n2, T2 = n[0], n[1], n[2], n[3], n[4], n[5]; return (T1 * n2 - T2 * n1) / (m1 * n2 - m2 * n1)
    # ── 두 점을 지나는 직선 (09-09)
    if tid.startswith("m2-1-line-two-points-t4"):
        mm = re.search(r"y = (-?\d*)x ([+−]) (\d+)", q); a = _coef(mm.group(1))
        px, py = [Fraction(v) for v in _PT.findall(q)[0]]; return py - a * px
    if tid.startswith("m2-1-line-two-points"):
        (x1, y1), (x2, y2) = [(Fraction(u), Fraction(v)) for u, v in _PT.findall(q)[:2]]
        a = (y2 - y1) / (x2 - x1); b = y1 - a * x1
        if tid.startswith("m2-1-line-two-points-t1"):
            return a + b if "a + b" in q else (a - b if "a − b" in q else a * b)
        if tid.startswith("m2-1-line-two-points-t2"):
            return -b / a if "x절편" in q else b
        k = Fraction(re.search(r"\((-?\d+), m\)", q).group(1)); return a * k + b
    # ── 지수법칙 (09-09) — 위첨자 숫자를 되읽는다
    if tid.startswith("m2-1-exponent-t1"):
        m, nn, p = _sups(q)[:3]; return Fraction(m * nn + p)
    if tid.startswith("m2-1-exponent-t2"):
        m, nn = [int(v) for v in re.findall(r"pow\([xa], (\d+)\)", q)][:2]; return Fraction(m - nn)
    if tid.startswith("m2-1-exponent-t3"):
        m, nn = [int(v) for v in re.findall(r"pow\([xa], (\d+)\)", q)][:2]; return Fraction(nn - m)
    if tid.startswith("m2-1-exponent-t4"):
        mm = re.search(r"\((-?\d*)[xa]([⁰¹²³⁴⁵⁶⁷⁸⁹]*)[yb]([⁰¹²³⁴⁵⁶⁷⁸⁹]*)\)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", q)
        c = _coef(mm.group(1)); i = _sup(mm.group(2)); j = _sup(mm.group(3)); p = _sup(mm.group(4))
        return Fraction(c ** p + i * p + j * p)
    if tid.startswith("m2-1-exponent-t5"):
        lhs = q.split("=")[0]; terms = re.findall(r"(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lhs)
        B, m = int(terms[0][0]), _sup(terms[0][1]); cnt = len(terms)
        k = m
        while B ** k < cnt * B ** m:
            k += 1
        return Fraction(k) if B ** k == cnt * B ** m else None
    # ── 경우의 수 (09-09)
    if tid.startswith("m2-2-counting-t1"):
        a, b = n[0], n[1]; return a * b if "각각 한" in q else a + b
    if tid.startswith("m2-2-counting-t2"):
        nn = int(n[1]); f = nn if "모두 몇" in q else (nn // 2 if "짝수" in q else (nn + 1) // 2); return Fraction(f * (nn - 1))
    if tid.startswith("m2-2-counting-t3"):
        m = int(n[1]); return Fraction(m * m)                                            # 0부터 m: 십의 자리 m × 일의 자리 m
    if tid.startswith("m2-2-counting-t4"):
        nn = int(n[0]); f = math.factorial
        if "맨 앞" in q: return Fraction(f(nn - 1))
        if "이웃" in q: return Fraction(2 * f(nn - 1))
        if "양 끝" in q: return Fraction(2 * f(nn - 2))
        return Fraction(f(nn))
    if tid.startswith("m2-2-counting-t5"):
        nn = int(n[0]); return Fraction(nn * (nn - 1)) if "회장" in q else Fraction(nn * (nn - 1) // 2)
    if tid.startswith("m2-2-counting-t6"):
        k = int(n[0]); return Fraction(min(k - 1, 13 - k)) if "합이" in q else Fraction(2 * (6 - k))
    if tid.startswith("m2-2-counting-t7"):
        m, nn, p = n[0], n[1], n[2]; return m * nn if "거쳐" in q else m * nn + p
    # ── 확률 (09-09) — 답은 분수
    if tid.startswith("m2-2-probability-t1") or tid.startswith("m2-2-probability-t8"):
        N = int(n[1]); k = int(n[-1]); return Fraction(N // k, N)
    if tid.startswith("m2-2-probability-t2"):
        k = int(n[0]); return Fraction(min(k - 1, 13 - k), 36)
    if tid.startswith("m2-2-probability-t3"):
        nn = int(n[0]); return 1 - Fraction(1, 2 ** nn) if "적어도" in q else Fraction(1, 2 ** nn)
    if tid.startswith("m2-2-probability-t4"):
        k = int(n[0]); return 1 - Fraction((k - 1) ** 2, 36)
    if tid.startswith("m2-2-probability-t5"):
        N, a, b = int(n[1]), int(n[3]), int(n[4]); return Fraction(N // a + N // b, N)
    if tid.startswith("m2-2-probability-t6"):
        fr = re.findall(r"frac\((\d+),\s*(\d+)\)", q); p = Fraction(int(fr[0][0]), int(fr[0][1])); r = Fraction(int(fr[1][0]), int(fr[1][1]))
        if "둘 다" in q and ("못할" in q or "실패할" in q or "않을" in q): return (1 - p) * (1 - r)
        if "둘 다" in q: return p * r
        if "적어도" in q: return 1 - (1 - p) * (1 - r)
        return p * (1 - r)                                                             # 한쪽만
    if tid.startswith("m2-2-probability-t7"):
        a, b = int(n[0]), int(n[1]); T = a + b
        return Fraction(a * a, T * T) if "다시 넣은 후" in q else Fraction(a * (a - 1), T * (T - 1))
    # ── m2-2 이등변삼각형 (09-09)
    if tid.startswith("m2-2-isosceles-t1"):
        G, v = _given_angle(q); return (180 - v) / 2 if G == "A" else 180 - 2 * v
    if tid.startswith("m2-2-isosceles-t2"):
        G, v = _given_angle(q); b = v if G == "C" else (180 - v) / 2
        return 3 * b - 180 if _asked_angle(q) == "ABD" else 180 - 2 * b
    if tid.startswith("m2-2-isosceles-t3"):
        k, h = n[0] / 2, n[1]
        return k * h / 2 if "△ABD" in q else (k * h if "△ABC" in q else k)
    if tid.startswith("m2-2-isosceles-t4"):
        _, t = _given_angle(q); a = (180 - 2 * t) / 3
        return (180 - a) / 2 if _asked_angle(q) == "C" else a
    if tid.startswith("m2-2-isosceles-t5"):
        G, v = _given_angle(q); return v / 2 if G == "A" else 2 * v
    # ── m2-2 외심
    if tid.startswith("m2-2-circumcenter-t1"):
        G, v = _given_angle(q); return 2 * v if len(G) == 1 else v / 2                    # 꼭짓점각(A·B·C) ↔ 중심각(BOC·AOC·AOB)
    if tid.startswith("m2-2-circumcenter-t2"):
        m = re.findall(r"\[\[deg\((\d+)\)\]\]", q); return 90 - Fraction(m[0]) - Fraction(m[1])
    if tid.startswith("m2-2-circumcenter-t3"):
        d, m = n[1], n[2]; return d / 2 if "반지름" in q else d + m                                  # n[0]은 deg(90)
    if tid.startswith("m2-2-circumcenter-t4"):
        d = n[1]; return (d / 2) ** 2
    if tid.startswith("m2-2-circumcenter-t5"):
        c, P = n[0], n[1]; R = (P - c) / 2; return R * R if "넓이" in q else 2 * R
    if tid.startswith("m2-2-circumcenter-t6"):
        m = re.search(r"= (\d+) : (\d+)", q); p, qq = Fraction(m.group(1)), Fraction(m.group(2)); aob = 180 * p / (p + qq)
        return aob / 2 if _asked_angle(q) == "C" else 90 - aob / 2
    # ── m2-2 내심
    if tid.startswith("m2-2-incenter-t1"):
        G, v = _given_angle(q); return 90 + v / 2 if len(G) == 1 else 2 * (v - 90)      # 꼭짓점각(A·B·C) ↔ 내심각(BIC·AIC·AIB)
    if tid.startswith("m2-2-incenter-t2"):
        m = re.findall(r"\[\[deg\((\d+)\)\]\]", q); return 90 - Fraction(m[0]) - Fraction(m[1])
    if tid.startswith("m2-2-incenter-t3"):
        g1, g2 = n[0], n[1]; return g1 * g2 / 2 if "넓이를" in q else 2 * g1 / g2
    if tid.startswith("m2-2-incenter-t4"):
        a, b, c = n[1], n[2], n[3]; r = (a + b - c) / 2                                  # n[0]은 deg(90)
        return r if "반지름" in q else (b - r if "seg(AD)]]의 길이" in q else a - r)
    if tid.startswith("m2-2-incenter-t5"):
        c, a, b = n[0], n[1], n[2]; hp = (a + b + c) / 2
        return hp - a if "seg(AD)]]의 길이" in q else (hp - b if "seg(BE)]]의 길이" in q else hp - c)
    if tid.startswith("m2-2-incenter-t6"):
        ta, tb, tc = n[0], n[1], n[2]
        if "둘레" in q: return 2 * (ta + tb + tc)
        return ta + tb if "seg(AB)]]의 길이" in q else (tb + tc if "seg(BC)]]의 길이" in q else tc + ta)
    # ── m2-2 평행사변형 · 여러 가지 사각형 · 피타고라스 (09-09)
    if tid.startswith("m2-2-parallelogram-t1"):
        m = re.search(r"= (\d+) : (\d+)", q); p, qq = Fraction(m.group(1)), Fraction(m.group(2))
        return 180 * p / (p + qq) if _asked_angle(q) == "C" else 180 * qq / (p + qq)
    if tid.startswith("m2-2-parallelogram-t2"):
        segs = _segs(q); P = _after(q, "둘레의 길이가 ")
        if "둘레" in q.split("일 때")[-1]: return 2 * (segs["AB"] + segs["BC"])
        return P / 2 - segs["AB"] if "seg(BC)]]의 길이" in q else P / 2 - segs["BC"]
    if tid.startswith("m2-2-parallelogram-t3"):
        segs = _segs(q); p, qq, c = segs["OA"], segs["OB"], segs["AB"]
        if "△OCD" in q: return p + qq + c
        if "seg(AC)]]의 길이" in q: return 2 * p
        if "seg(BD)]]의 길이" in q: return 2 * qq
        return 2 * p + 2 * qq
    if tid.startswith("m2-2-parallelogram-t4"):
        segs = _segs(q); a, b = segs["AB"], segs["AD"]
        return 2 * a - b if "seg(EF)]]의 길이" in q else b - a
    if tid.startswith("m2-2-parallelogram-t5"):
        g1, g2 = n[0], n[1]; return 2 * (g1 + g2) if "□ABCD의 넓이를" in q else g2 / 2 - g1
    if tid.startswith("m2-2-special-quad-t1"):
        _, t = _given_angle(q); X = _asked_angle(q); return 2 * t if X == "AOB" else (90 - t if X == "OAB" else 180 - 2 * t)
    if tid.startswith("m2-2-special-quad-t2"):
        _, t = _given_angle(q); X = _asked_angle(q); return 90 - t if X == "OCB" else (2 * t if X == "ABC" else 180 - 2 * t)
    if tid.startswith("m2-2-special-quad-t3"):
        _, a = _given_angle(q); return 45 + a if _asked_angle(q) == "BEC" else 90 - a
    if tid.startswith("m2-2-special-quad-t4"):
        segs = _segs(q); a = segs["AB"]
        if "seg(BC)]]의 길이" in q: return a + segs["AD"]
        if "seg(AD)]]의 길이" in q: return segs["BC"] - a
        return 3 * a + 2 * segs["AD"]
    if tid.startswith("m2-2-special-quad-t5"):
        segs = _segs(q); ac = segs["AC"]
        if "넓이를" in q: return ac * segs["BD"] / 2
        return 2 * _after(q, "넓이가 ") / ac
    if tid.startswith("m2-2-pythagoras-t1"):
        segs = _segs(q); X = _asked_seg(q)
        if X == "AB": return _isqrt(segs["BC"] ** 2 + segs["CA"] ** 2)
        if X == "BC": return _isqrt(segs["AB"] ** 2 - segs["CA"] ** 2)
        return _isqrt(segs["AB"] ** 2 - segs["BC"] ** 2)
    if tid.startswith("m2-2-pythagoras-t2"):
        g1, g2 = n[1], n[2]; return g1 + g2 if "seg(AB)]]를 한 변" in q else g2 - g1
    if tid.startswith("m2-2-pythagoras-t4"):
        c, a2 = n[0], n[1]; h = _isqrt(c * c - (a2 / 2) ** 2)
        return h if "seg(AD)]]의 길이" in q else a2 / 2 * h
    if tid.startswith("m2-2-pythagoras-t5"):
        segs = _segs(q)
        if _asked_seg(q) == "BD": return _isqrt(segs["AB"] ** 2 + segs["BC"] ** 2)
        return _isqrt(segs["BD"] ** 2 - segs["BC"] ** 2)
    # ── m2-2 닮음 (09-09)
    if tid.startswith("m2-2-similar-ratio-t1"):
        sg = _segs(q); X = _asked_seg(q)
        return sg["BC"] * sg["DE"] / sg["AB"] if X == "EF" else sg["EF"] * sg["AB"] / sg["DE"]
    if tid.startswith("m2-2-similar-ratio-t2"):
        m = re.search(r"닮음비가 (\d+) : (\d+)", q); u, w = Fraction(m.group(1)), Fraction(m.group(2))
        gv = n[2]; big = "△DEF" in q.split("일 때")[-1]; area = "넓이" in q.split("일 때")[-1]
        r = (w / u) if big else (u / w)
        return gv * (r * r if area else r)
    if tid.startswith("m2-2-similar-ratio-t3"):
        N, d = n[1], n[2]; return d * N / 100 if "실제 거리는" in q else d * 100 / N          # n[0]은 frac(1, N)의 1
    if tid.startswith("m2-2-tri-similar-t1"):
        sg = _segs(q); ab = sg["AD"] + sg["DB"]; ac = sg["AE"] + sg["EC"]; r = sg["AD"] / ac      # △ADE ∽ △ACB
        if abs(r - sg["AE"] / ab) > 0: return None
        return sg["DE"] / r if _asked_seg(q) == "BC" else sg["BC"] * r
    if tid.startswith("m2-2-tri-similar-t2"):
        sg = _segs(q); ad, ae = sg["AD"], sg["AE"]
        if _asked_seg(q) == "CD": ab = sg["AB"]; return ab * ae / ad - ad                 # AC = AB·AE/AD
        ac = sg["AC"]; return ac * ad / ae - ae                                            # AB = AC·AD/AE
    if tid.startswith("m2-2-tri-similar-t3"):
        sg = _segs(q); ch = sg["CH"]
        return _isqrt(sg["BH"] * ch) if _asked_seg(q) == "AH" else sg["AH"] ** 2 / ch
    if tid.startswith("m2-2-tri-similar-t4"):
        sg = _segs(q); oa = sg["OA"]; X = _asked_seg(q)
        if X == "DC": return sg["AB"] * sg["OD"] / oa
        if X == "OB": return sg["OC"] * oa / sg["OD"]
        return oa * sg["DC"] / sg["AB"]
    if tid.startswith("m2-2-parallel-ratio-t1"):
        sg = _segs(q); ad, db = sg["AD"], sg["DB"]; X = _asked_seg(q)
        if X == "EC": return sg["AE"] * db / ad
        if X == "DE": return sg["BC"] * ad / (ad + db)
        return sg["DE"] * (ad + db) / ad
    if tid.startswith("m2-2-parallel-ratio-t2"):
        sg = _segs(q); ab, bc = sg["AB"], sg["BC"]
        return sg["DE"] * bc / ab if _asked_seg(q) == "EF" else sg["EF"] * ab / bc
    if tid.startswith("m2-2-parallel-ratio-t3"):
        sg = _segs(q); return sg["BC"] / 2 if _asked_seg(q) == "DE" else 2 * sg["DE"]
    if tid.startswith("m2-2-parallel-ratio-t4"):
        sg = _segs(q); c, a, b = sg["AB"], sg["BC"], sg["CA"]
        if "둘레" in q: return (a + b + c) / 2
        X = _asked_seg(q); return c / 2 if X == "EF" else (a / 2 if X == "DF" else b / 2)
    if tid.startswith("m2-2-parallel-ratio-t5"):
        sg = _segs(q); p = sg["AC"]
        return p + sg["BD"] if "둘레의 길이를" in q else _after(q, "둘레의 길이가 ") - p
    if tid.startswith("m2-2-centroid-t1"):
        sg = _segs(q); X = _asked_seg(q)
        if "AD" in sg: k = sg["AD"] / 3
        elif "AG" in sg: k = sg["AG"] / 2
        else: k = sg["GD"]
        return 2 * k if X == "AG" else (k if X == "GD" else 3 * k)
    if tid.startswith("m2-2-centroid-t2"):
        gv = n[0]
        if "△ABC의 넓이가" in q: return gv / 3 if "△GBC의 넓이를" in q else gv / 6
        return 6 * gv if "△GBD의 넓이가" in q else 3 * gv
    if tid.startswith("m2-2-centroid-t3"):
        sg = _segs(q); return sg["AC"] / 3 if _asked_seg(q) == "BG" else 3 * sg["BG"]
    if tid.startswith("m2-2-centroid-t4"):
        sg = _segs(q); return sg["BD"] / 6 if _asked_seg(q) == "OE" else 6 * sg["OE"]
    return "skip"


def _segs(q):
    """'[[seg(XY)]] = v cm' 꼴을 전부 모아 {XY: v}."""
    return {m.group(1): Fraction(m.group(2)) for m in re.finditer(r"\[\[seg\(([A-Z]{2})\)\]\] = (\d+(?:\.\d+)?) cm", q)}


def _after(q, key):
    m = re.search(re.escape(key) + r"(\d+(?:\.\d+)?)", q)
    return Fraction(m.group(1)) if m else None


def _asked_seg(q):
    m = re.search(r"\[\[seg\(([A-Z]{2})\)\]\]의 길이", q)
    return m.group(1) if m else None


def _isqrt(v):
    v = Fraction(v)
    if v.denominator != 1 or v < 0:
        return None
    r = math.isqrt(int(v))
    return Fraction(r) if r * r == v else None


def check_judge(it):
    """m2-2-pythagoras-t3: 보기의 세 수로 직각삼각형 판정을 다시 해 문자열 답과 대조."""
    if not it["template_id"].startswith("m2-2-pythagoras-t3"):
        return None
    q = it["question"]
    ok = []
    for m in re.finditer(r"([A-E])\. (\d+), (\d+), (\d+)", q):
        x, y, z = sorted(int(m.group(i)) for i in (2, 3, 4))
        if x * x + y * y == z * z:
            ok.append(m.group(1))
    return it["answer"] == ", ".join(ok)


def _given_angle(q):
    """'[[angle(X)]] = [[deg(v)]]' 꼴의 마지막(주어진) 각 → (이름, 값)."""
    m = re.findall(r"\[\[angle\(([A-Z]+)\)\]\] = \[\[deg\((\d+)\)\]\]", q)
    return (m[-1][0], Fraction(m[-1][1])) if m else (None, None)


def _asked_angle(q):
    m = re.search(r"\[\[angle\(([A-Z]+)\)\]\]의 크기", q)
    return m.group(1) if m else None


_PT = re.compile(r"\((-?\d+), (-?\d+)\)")
_SUPD = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def _sup(s):
    """위첨자 → 정수 (빈 문자열은 지수 1)."""
    return int(s.translate(_SUPD)) if s else 1


def _sups(q):
    return [_sup(s) for s in re.findall(r"[⁰¹²³⁴⁵⁶⁷⁸⁹]+", q)]


def _coef(s):
    """'' → 1, '-' → −1, '-3' → −3 (co() 표기 되읽기)."""
    return Fraction(1) if s == "" else (Fraction(-1) if s == "-" else Fraction(s))


def check_ineq(it):
    """일차부등식 풀이(문자열 답 'x > 3'): 발문의 양변을 mathir 로 다시 읽어 일차식 f = 좌변 − 우변 의 기울기·절편에서 해를 재구성해 답과 대조.
    True/False = 일치 여부, None = 해당 없음."""
    if not it["template_id"].startswith(("m2-1-ineq-solve-t1", "m2-1-ineq-solve-t2")):
        return None
    import mathir
    m = re.search(r"일차부등식 (.+?) ([<>≤≥]) (.+?)[을를] 푸시오", it["question"])
    if not m:
        return False
    L, R = mathir.parse(m.group(1))[0], mathir.parse(m.group(3))[0]
    f = lambda x: Fraction(mathir.ev(L, {"x": x})) - Fraction(mathir.ev(R, {"x": x}))   # noqa: E731
    f0 = f(Fraction(0)); slope = f(Fraction(1)) - f0
    if slope == 0:
        return False
    x0 = -f0 / slope
    op = m.group(2); strict = op in "<>"; want_pos = op in (">", "≥")           # f(x) OP 0
    right = (slope > 0) == want_pos                                              # 해가 오른쪽으로 뻗는가
    fop = (">" if strict else "≥") if right else ("<" if strict else "≤")
    want = f"x {fop} {x0.numerator if x0.denominator == 1 else x0}"
    return re.sub(r"\s+", " ", it["answer"]).strip() == want


_KOR_DIGIT = {"일": 1, "이": 2, "삼": 3, "사": 4, "오": 5, "육": 6, "칠": 7, "팔": 8, "구": 9}


def _kor_polygon(q):
    """'십이각형' → 12 (오~이십각형)."""
    m = re.search(r"([일이삼사오육칠팔구십]+)각형", q)
    w = m.group(1)
    if "십" in w:
        a, b = w.split("십")
        return (_KOR_DIGIT.get(a, 1) if a else 1) * 10 + (_KOR_DIGIT[b] if b else 0)
    return _KOR_DIGIT[w]


# ── ①-b 위치관계(문자열 답) 독립 검산 — 그림 규약을 좌표로 다시 세워 관계를 재계산 ─────────
_P3 = {
    "box": {"A": (0, 2, 0), "B": (3, 2, 0), "C": (3, 2, 2), "D": (0, 2, 2), "E": (0, 0, 0), "F": (3, 0, 0), "G": (3, 0, 2), "H": (0, 0, 2)},
    "triprism": {"A": (0, 2, 0), "B": (3, 2, 0), "C": (1.5, 2, 2), "D": (0, 0, 0), "E": (3, 0, 0), "F": (1.5, 0, 2)},
}
_EDGES = {
    "box": ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"],
    "triprism": ["AB", "BC", "CA", "DE", "EF", "FD", "AD", "BE", "CF"],
}


def _v(P, e): return tuple(P[e[1]][i] - P[e[0]][i] for i in range(3))
def _cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
def _zero(v): return all(abs(x) < 1e-9 for x in v)


def _edge_rel(P, e, f):
    if set(e) & set(f): return "만나는"
    if _zero(_cross(_v(P, e), _v(P, f))): return "평행한"
    return "꼬인"


def _face_rel(P, F, e):
    if set(e) <= set(F): return "포함"
    p = [P[c] for c in F[:3]]
    nrm = _cross(tuple(p[1][i]-p[0][i] for i in range(3)), tuple(p[2][i]-p[0][i] for i in range(3)))
    if _zero(_cross(nrm, _v(P, e))): return "수직인"
    return "평행한"


def check_position(it):
    """True/False = 검산 일치 여부, None = 해당 없음."""
    if not it["template_id"].startswith("m1-2-position"):
        return None
    q = it["question"]
    kind = "triprism" if "삼각기둥" in q else "box"
    P, edges = _P3[kind], _EDGES[kind]
    same = lambda a, b: set(a) == set(b)   # noqa: E731 — 이름 순서가 달라도 같은 모서리
    m = re.search(r"모서리 ([A-H]{2})[와과] (평행한|한 점에서 만나는|꼬인 위치에 있는) 모서리", q)
    if m:
        e, rel = m.group(1), m.group(2).replace("한 점에서 ", "").replace(" 위치에 있는", "")
        hits = [f for f in edges if not same(f, e) and _edge_rel(P, e, f) == rel]
        if it.get("choices"):
            return any(same(it["answer"], f) for f in hits) and sum(1 for c in it["choices"] if any(same(c, f) for f in hits)) == 1
        return str(len(hits)) == it["answer"]
    m = re.search(r"면 ([A-H]{3,4})(?:에 평행한|[와과] 수직인) 모서리", q)
    if m:
        F = m.group(1); rel = "평행한" if "평행한" in q else "수직인"
        hits = [f for f in edges if _face_rel(P, F, f) == rel]
        return any(same(it["answer"], f) for f in hits) and sum(1 for c in it["choices"] if any(same(c, f) for f in hits)) == 1
    return False


# ── ② 도형–문면 정합 ────────────────────────────────────────────────────────
def angle_at(P, at, fr, to):
    ax, ay = P[at]; v1 = (P[fr][0] - ax, P[fr][1] - ay); v2 = (P[to][0] - ax, P[to][1] - ay)
    c = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
    return math.degrees(math.acos(max(-1, min(1, c))))


def check_fig(it):
    for fg in it.get("figure") or []:
        fn, a = fg.get("fn"), fg.get("args") or {}
        if fn == "scene":
            P = a["pts"]
            for arc in (a.get("marks") or {}).get("arc", []) or []:
                lab = str(arc.get("label", ""))
                m = re.fullmatch(r"(\d+)°", lab)
                if not m:
                    continue
                real = angle_at(P, arc["at"], arc["from"], arc["to"])
                if abs(real - int(m.group(1))) > 0.6:
                    bad("F1-scene 각 라벨≠실제각", it, f"{arc['at']} 라벨 {lab} 실제 {real:.1f}")
        elif fn == "sector":
            if isinstance(a.get("angle"), (int, float)):
                qn = nums(it["question"])
                if qn and qn[0] != a["angle"]:
                    bad("F2-sector 각≠문면", it, f"{a['angle']} vs {qn[0]}")
        elif fn == "numline":
            for p in a.get("points", []) or []:
                if not (a["min"] <= p["x"] <= a["max"]):
                    bad("F3-numline 점이 범위 밖", it, str(p))
        elif fn == "coordplane":
            for ln in a.get("lines", []) or []:
                if "points" in ln:
                    (x1, y1), (x2, y2) = ln["points"][:2]
                    for p in a.get("points", []) or []:
                        x, y = p["coord"]
                        if (x2 - x1) * (y - y1) != (y2 - y1) * (x - x1):
                            bad("F4-coordplane 점이 직선 밖", it, str(p))


# ── ③ 한국어·표기 ───────────────────────────────────────────────────────────
JOSA = {"은": True, "는": False, "이": True, "가": False, "을": True, "를": False,
        "과": True, "와": False, "으로": True, "로": False}
_JOSA_RE = re.compile(r"(-?\d+(?:\.\d+)?|π)\s*(은\(는\)|이\(가\)|을\(를\)|\(으\)로|으로|은|는|이|가|을|를|과|와|로)(?=[\s,.…)]|$)")


_PH_RE = re.compile(r"\{[A-Za-z_][A-Za-z_0-9*/+\- ().,]*\}")


def check_text(it, field, text):
    if "**" in text:
        bad("T1-마크다운 찌꺼기", it, field)
    m0 = _PH_RE.search(text)
    if m0:                                   # 표 행 문자열 안의 {k} 등은 채워지지 않는다 — 정적 조각 + 파생값으로 쪼갤 것
        bad("T7-미치환 자리표시자", it, f"{field}: {m0.group(0)}")
    m2 = re.search(r".{0,12}[+\u2212-]\s-\d.{0,6}", text)
    if m2:
        bad("T2-'+ -6' 꼴(괄호 필요)", it, f"{field}: …{m2.group(0)}")
    m3 = re.search(r".{0,10}[÷×]\s*1(?![\d./]).{0,6}", text)
    if m3 and not re.search(r"×\s*\(?-?1\)?\s*[+−=)]", m3.group(0)):   # 'a × 1 + b'·'a × 1 = a'·'(3 × 2 × 1)' 대입·계승 문맥은 허용
        bad("T3-'÷ 1'·'× 1' 항등 연산", it, f"{field}: …{m3.group(0)}")
    if re.search(r"(?<![\d.])1[xyrnb](?![\w])", text):
        bad("T4-'1x' 계수 1", it, field)
    for m in _JOSA_RE.finditer(text):
        num, j = m.group(1), m.group(2)
        if "(" in j:
            bad("T5-조사 미적용 '은(는)'", it, f"{field}: {num}{j}")
            continue
        if num == "π":
            continue
        want = _has_jong(num)
        if j == "로" and want and not num.endswith(("1", "7", "8")):
            bad("T6-조사 불일치", it, f"{field}: {num}{j} → {num}으로"); continue
        if j == "으로" and not want:
            bad("T6-조사 불일치", it, f"{field}: {num}{j} → {num}로"); continue
        if j in ("은", "는", "이", "가", "을", "를", "과", "와") and JOSA[j] != want:
            bad("T6-조사 불일치", it, f"{field}: {num}{j}")


n = 0
for f in sorted(OUT.glob("*_pool.json")):
    for it in json.loads(f.read_text(encoding="utf-8")):
        n += 1
        # ①
        pos = check_position(it)
        if pos is None:
            pos = check_ineq(it)
        if pos is None:
            pos = check_judge(it)
        if pos is not None:
            if not pos:
                bad("R1-독립 검산 불일치", it, f"문자열 답 재계산 ≠ 답 {it['answer']}")
            got = "done"
        else:
            got = recompute(it)
        av, kind = ans_val(it) if got != "done" else (None, None)
        if got == "done":
            pass
        elif got == "skip":
            prob["(검산 규칙 없음)"] += 1
        elif got is None or av is None:
            bad("R0-검산 불가", it, f"answer={it['answer']}")
        elif Fraction(got) != av:
            bad("R1-독립 검산 불일치", it, f"발문 재계산 {got} ≠ 답 {av}")
        # ②
        check_fig(it)
        # ③
        sol = it["solution"]
        check_text(it, "question", it["question"])
        for lv in sol["levels"]:
            check_text(it, lv["title"], lv.get("text") or "")
            for i, st in enumerate(lv.get("steps") or []):
                check_text(it, f"{lv['title']}[{i}]", st)
        check_text(it, "check", sol.get("check") or "")
        check_text(it, "model", sol.get("model_answer") or "")
        for r in sol.get("rubric", {}).get("items", []):
            check_text(it, "rubric", r.get("criterion", "") + " " + (r.get("partial") or ""))
        for c in it.get("choices") or []:
            check_text(it, "choice", c)
        # 정답이 모범답안에 들어 있는가
        atext = re.sub(r"^\[\[|\]\]$", "", it["answer"])
        atext = re.sub(r"\s*\*\s*pi", "π", atext); atext = re.sub(r"deg\((\d+)\)", r"\1°", atext)
        if atext not in (sol.get("model_answer") or ""):
            bad("M1-모범답안에 답 없음", it, atext)
        if abs((it["cost"] or 0) and 0) > 0:
            pass

print(f"내용 검사 {n}건 ({OUT})\n")
for code, c in sorted(prob.items(), key=lambda kv: -kv[1]):
    if code.startswith("("):
        continue
    print(f"  {code:<28} {c:>5}건   예: {ex[code][0] if ex[code] else ''}")
    for e in ex[code][1:3]:
        print(f"  {'':<28}        {e}")
hard = [k for k in prob if k[0] in "RF" and not k.startswith("(")]
print(f"\n  독립 검산 규칙 없는 문항 {prob['(검산 규칙 없음)']}건")
sys.exit(1 if hard else 0)
