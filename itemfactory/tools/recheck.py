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
    # ── m1-2 통계 2 (09-11): 도수분포표 — 도수는 발문 '차례로 …' 에서, 계급 경계는 표(figure) 에서 되읽는다
    if tid.startswith("m1-2-freq-table-t1"):
        N = Fraction(re.search(r"(\d+)명의", q).group(1)); fs = _freq_list(q)
        return N - sum(fs)
    if tid.startswith("m1-2-freq-table-t2"):
        N = Fraction(re.search(r"(\d+)명의", q).group(1)); rows = _ft_rows(it)
        m = re.search(r"(\d+(?:\.\d+)?) ?(?:분|km|점|회|쪽) (이상|미만)인 학생", q); b, d = Fraction(m.group(1)), m.group(2)
        cnt = sum(f for lo, hi, f in rows if (lo >= b if d == "이상" else hi <= b))
        return 100 * cnt / N
    if tid.startswith("m1-2-freq-table-t3"):
        rows = _ft_rows(it); lo, hi, _ = max(rows, key=lambda r: r[2]); return (lo + hi) / 2
    if tid.startswith("m1-2-freq-table-t4"):
        N = Fraction(re.search(r"(\d+)명의", q).group(1)); fs = _freq_list(q)
        p = Fraction(re.search(r"전체의 (\d+) %", q).group(1)); A = N * p / 100
        return N - sum(fs) - A
    if tid.startswith("m1-2-freq-table-t5"):
        rows = _ft_rows(it); k = int(re.search(r"(\d+)번째", q).group(1)); acc = 0
        for lo, hi, f in reversed(rows):
            acc += f
            if k <= acc:
                return (lo + hi) / 2
        return None
    # ── 상대도수 (09-11) — 소수는 발문에서 그대로 읽는다
    if tid.startswith("m1-2-relative-freq-t1"):
        N = Fraction(re.search(r"(\d+)명의", q).group(1)); fs = _freq_list(q); rows = _ft_rows(it)
        lo = Fraction(re.search(r"(\d+(?:\.\d+)?) ?(?:분|km|점|회|쪽) 이상", q).group(1))
        fj = next(f for l, h, f in rows if l == lo)
        return fj / N
    if tid.startswith("m1-2-relative-freq-t2"):
        f = Fraction(re.search(r"도수는 (\d+)명이고", q).group(1)); r = Fraction(re.search(r"상대도수는 (\d*\.?\d+)", q).group(1))
        return f / r
    if tid.startswith("m1-2-relative-freq-t3") or tid.startswith("m1-2-relative-freq-t4"):
        fs = [Fraction(x) for x in re.findall(r"(\d+)명", q)]
        rs = re.search(r"상대도수는 차례로 (.+?)일 때", q).group(1).split(", ")
        N = fs[0] / Fraction(rs[0])
        return N * Fraction(rs[1]) if tid.startswith("m1-2-relative-freq-t3") else fs[1] / N
    if tid.startswith("m1-2-relative-freq-t5"):
        na, nb, fa, fb = [Fraction(x) for x in re.findall(r"(\d+)명", q)][:4]
        return (fa / na) / (fb / nb)
    # ── 중앙값·최빈값 (09-11) — 대괄호 안의 자료를 되읽는다 (x 는 미지수)
    if tid.startswith("m1-2-median-mode"):
        data = _bracket_data(q); known = sorted(v for v in data if v is not None)
        if tid.startswith("m1-2-median-mode-t1"):
            vals = sorted(data); med = vals[3]; mode = Counter(vals).most_common(1)[0][0]; return med + mode
        if tid.startswith("m1-2-median-mode-t2"):
            vals = sorted(data); return (vals[2] + vals[3]) / 2
        if tid.startswith("m1-2-median-mode-t3"):
            v = Counter(known).most_common(1)[0][0]; return 6 * v - sum(known)
        if tid.startswith("m1-2-median-mode-t4"):
            m = Fraction(re.search(r"중앙값이 (\d*\.?\d+)", q).group(1)); x = 2 * m - known[2]
            vals = sorted(known + [x]); return x if (vals[2] + vals[3]) / 2 == m and known[2] < x < known[3] else None
        if tid.startswith("m1-2-median-mode-t5"):
            m = Fraction(re.search(r"평균이 (\d*\.?\d+)", q).group(1)); x = 7 * m - sum(known)
            vals = sorted(known + [x]); return vals[3]
    # ── 다면체 세기 (09-11) — 이름(칠각기둥)·종류를 되읽어 F·E·V 를 다시 센다
    if tid.startswith("m1-2-polyhedron"):
        kind = "각뿔대" if "각뿔대" in q else ("각뿔" if "각뿔" in q else "각기둥")
        nb, ap = (1, 1) if kind == "각뿔" else (2, 0)
        FEV = lambda nn: {"면": nb + nn, "모서리": nn * nb + nn, "꼭짓점": nn * nb + ap, "밑면인 다각형의 변": nn}   # noqa: E731
        ask = re.search(r"의 (면|모서리|꼭짓점|밑면인 다각형의 변)의 개수를 구하시오", q)
        kn = lambda: _kor_polygon(re.sub(r"각(?:기둥|뿔대|뿔)", "각형", q))   # noqa: E731 — '칠각기둥' → '칠각형' 으로 되읽기
        if tid.startswith("m1-2-polyhedron-t1"):
            return Fraction(FEV(kn())[ask.group(1)])
        if tid.startswith("m1-2-polyhedron-t2"):
            g = re.search(r"(면|모서리|꼭짓점)의 개수가 (\d+)인", q); key, gv = g.group(1), int(g.group(2))
            nn = next((k for k in range(3, 16) if FEV(k)[key] == gv), None)
            return Fraction(FEV(nn)[ask.group(1)]) if nn else None
        if tid.startswith("m1-2-polyhedron-t3"):
            d = FEV(kn()); v, e, f = d["꼭짓점"], d["모서리"], d["면"]
            ex = re.search(r"때, (.+?)의 값을", q).group(1).replace("−", "-")
            return Fraction(eval(ex, {"__builtins__": {}}, {"v": v, "e": e, "f": f}))   # noqa: S307 — v·e·f·부호만 있는 식
        if tid.startswith("m1-2-polyhedron-t4"):
            T = int(re.search(r"v \+ e \+ f = (\d+)", q).group(1))
            nn = next((k for k in range(3, 16) if sum(FEV(k)[x] for x in ("면", "모서리", "꼭짓점")) == T), None)
            return Fraction(FEV(nn)[ask.group(1)]) if nn else None
        if tid.startswith("m1-2-polyhedron-t5"):
            g = re.search(r"모서리의 개수는 (꼭짓점|면)의 개수보다 (\d+)만큼", q); key, dd = g.group(1), int(g.group(2))
            nn = next((k for k in range(3, 16) if FEV(k)["모서리"] - FEV(k)[key] == dd), None)
            return Fraction(FEV(nn)[ask.group(1)]) if nn else None
    # ── 각기둥·각뿔 (09-11)
    if tid.startswith("m1-2-prism-pyramid-t1") or tid.startswith("m1-2-prism-pyramid-t2"):
        c, a, b, h = [Fraction(x) for x in re.findall(r"(\d+) cm", q)][:4]
        return a * b + (a + b + c) * h if tid.startswith("m1-2-prism-pyramid-t1") else a * b * h / 2
    if tid.startswith("m1-2-prism-pyramid-t3"):
        A = Fraction(re.search(r"밑넓이가 (\d+)", q).group(1)); V = Fraction(re.search(r"부피가 (\d+)", q).group(1)); return V / A
    if tid.startswith("m1-2-prism-pyramid-t4"):
        a, sl = [Fraction(x) for x in re.findall(r"(\d+) cm", q)][:2]; return a * a + 2 * a * sl
    if tid.startswith("m1-2-prism-pyramid-t5"):
        A, a, H, h = [Fraction(x) for x in re.findall(r"(\d+) cm", q)][:4]; return A * A * H / 3 - a * a * h / 3
    if tid.startswith("m1-2-prism-pyramid-t6"):
        a, h, p, qq = [Fraction(x) for x in re.findall(r"(\d+) cm", q)][:4]; return a * a * h / (3 * p * qq)
    # ── 정다각형 외각 (09-11)
    if tid.startswith("m1-2-polygon-exterior"):
        def by_n(nn, q=q):
            ask = re.search(r"정다각형의 (.+?)[을를] 구하시오", q).group(1)
            if ask.startswith("변의 개수"): return Fraction(nn)
            if ask.startswith("대각선"): return Fraction(nn * (nn - 3), 2)
            if ask.startswith("한 내각"): return Fraction(180 - Fraction(360, nn))
            if ask.startswith("한 외각"): return Fraction(360, nn)
            return Fraction(180 * (nn - 2))
        if tid.startswith("m1-2-polygon-exterior-t1"):
            return Fraction(360, _kor_polygon(q))
        if tid.startswith("m1-2-polygon-exterior-t2"):
            ext = int(re.search(r"\[\[deg\((\d+)\)\]\]", q).group(1)); return by_n(360 // ext) if 360 % ext == 0 else None
        if tid.startswith("m1-2-polygon-exterior-t3"):
            m = re.search(r"비가 (\d+) : (\d+)", q); a, b = int(m.group(1)), int(m.group(2)); ext = Fraction(180 * b, a + b)
            return by_n(int(360 / ext)) if ext.denominator == 1 and 360 % int(ext) == 0 else None
        if tid.startswith("m1-2-polygon-exterior-t4"):
            return 360 - sum(Fraction(v) for v in re.findall(r"\[\[deg\((\d+)\)\]\]", q))
        if tid.startswith("m1-2-polygon-exterior-t5"):
            inn = int(re.search(r"\[\[deg\((\d+)\)\]\]", q).group(1)); ext = 180 - inn
            return by_n(360 // ext) if 360 % ext == 0 else None
    # ── 호의 길이 비례 (09-11)
    if tid.startswith("m1-2-arc-ratio-t1") or tid.startswith("m1-2-arc-ratio-t5"):
        l1, l2 = [Fraction(v) for v in re.findall(r"(\d+) cm", q)][:2]; _, t1 = _given_angle(q); return t1 * l2 / l1
    if tid.startswith("m1-2-arc-ratio-t2"):
        l1 = Fraction(re.search(r"(\d+) cm", q).group(1)); degs = [Fraction(v) for v in re.findall(r"\[\[deg\((\d+)\)\]\]", q)]; return l1 * degs[1] / degs[0]
    if tid.startswith("m1-2-arc-ratio-t3"):
        m = re.search(r"= (\d+) : (\d+)", q); a, b = Fraction(m.group(1)), Fraction(m.group(2))
        return 180 * a / (a + b) if _asked_angle(q) == "AOC" else 180 * b / (a + b)
    if tid.startswith("m1-2-arc-ratio-t4"):
        m = re.search(r"= (\d+) : (\d+) : (\d+)", q); a, b, c = [Fraction(m.group(i)) for i in (1, 2, 3)]
        part = {"AOB": a, "BOC": b, "COA": c}[_asked_angle(q)]; return 360 * part / (a + b + c)
    # ── 선분의 중점 (09-11) — 토막(AB/4·AB/6) 위치로 다시 센다
    if tid.startswith("m1-2-segment-mid"):
        X = _asked_seg(q)
        if tid.startswith("m1-2-segment-mid-t1"):
            L = _after(q, "[[seg(AB)]] = "); second = re.search(r"\[\[seg\(([A-Z]{2})\)\]\]의 중점이다\. \[\[seg\(AB\)\]\]", q).group(1)
            pos = {"A": 0, "M": 2, "B": 4, "N": 3 if second == "MB" else 1}
            return L / 4 * abs(pos[X[0]] - pos[X[1]])
        if tid.startswith("m1-2-segment-mid-t2"):
            L = _after(q, "[[seg(AB)]] = "); second = re.search(r"점 M은 \[\[seg\(([A-Z]{2})\)\]\]의 중점", q).group(1)
            pos = {"A": 0, "P": 2, "Q": 4, "B": 6, "M": {"PQ": 3, "AP": 1, "QB": 5}[second]}
            return L / 6 * abs(pos[X[0]] - pos[X[1]])
        if tid.startswith("m1-2-segment-mid-t3"):
            g = re.search(r"\[\[seg\(([A-Z]{2})\)\]\] = (\d+) cm", q); k = Fraction(g.group(2))
            pos = {"A": 0, "N": 1, "M": 2, "B": 4}
            return k * abs(pos[X[0]] - pos[X[1]])                                        # 주어진 토막(NM·AN)은 언제나 1토막
        if tid.startswith("m1-2-segment-mid-t4"):
            a, b = _segs(q)["AB"], _segs(q)["BC"]; return (a + b) / 2
        if tid.startswith("m1-2-segment-mid-t5"):
            a, mn = _segs(q)["AB"], _segs(q)["MN"]; return 2 * (mn - a / 2)
    # ── 세션 5 (09-13): m1-1 수와 연산 기본 — 소인수분해·최대공약수/최소공배수·유리수 계산
    if tid.startswith("m1-1-prime-factor"):
        if tid.startswith("m1-1-prime-factor-t1"):
            m = re.match(r"(\d+)[을를] 소인수분해하면 (\d+)ᵃ × (\d+)ᵇ × c .*?일 때, (.+?)의 값", q)
            N, p, pq = int(m.group(1)), int(m.group(2)), int(m.group(3)); f = _fac(N)
            a, b = f.get(p, 0), f.get(pq, 0); rest = [x for x in f if x not in (p, pq)]
            if len(rest) != 1 or f[rest[0]] != 1: return None
            c = rest[0]; qt = m.group(4)
            return Fraction({"a + b + c": a + b + c, "a × b × c": a * b * c, "c − a − b": c - a - b}[qt])
        if tid.startswith("m1-1-prime-factor-t2"):
            return Fraction(_ndiv(int(re.match(r"(\d+)의 약수", q).group(1))))
        if tid.startswith("m1-1-prime-factor-t3"):
            return Fraction(_ndiv(_facval(q.split("의 약수")[0])))
        if tid.startswith("m1-1-prime-factor-t4"):
            N = int(re.match(r"(\d+)에 자연수", q).group(1)); x = 1
            for pp, e in _fac(N).items():
                if e % 2: x *= pp
            return Fraction(x)
        if tid.startswith("m1-1-prime-factor-t5"):
            expr, D = q.split("의 약수의 개수가 ")[0], int(re.search(r"개수가 (\d+)일", q).group(1)); M = 1
            for term in expr.split(" × "):
                if "ᵃ" in term: continue
                M *= _sup(re.sub(r"^\d+", "", term)) + 1
            return Fraction(D, M) - 1 if D % M == 0 else None
        if tid.startswith("m1-1-prime-factor-t6"):
            N = int(re.match(r"(\d+)의", q).group(1)); f = _fac(N)
            return Fraction(sum(f)) if "합" in q else Fraction(len(f))
    if tid.startswith("m1-1-gcd-lcm-basic"):
        if tid.startswith(("m1-1-gcd-lcm-basic-t1", "m1-1-gcd-lcm-basic-t2", "m1-1-gcd-lcm-basic-t3")):
            m = re.match(r"두 수 (.+?), (.+?)의 (최대공약수|공약수|최소공배수)", q); A, B = _facval(m.group(1)), _facval(m.group(2))
            return Fraction({"최대공약수": math.gcd(A, B), "공약수": _ndiv(math.gcd(A, B)), "최소공배수": A * B // math.gcd(A, B)}[m.group(3)])
        if tid.startswith("m1-1-gcd-lcm-basic-t4"):
            m = re.match(r"두 수 (.+?), (.+?)의 최대공약수가 (.+?), 최소공배수가 (.+?)일 때", q)
            FA, FB, FG, FL = [_facmap(m.group(i)) for i in (1, 2, 3, 4)]
            pa = [pp for pp, e in FA.items() if e == "a"][0]; pb = [pp for pp, e in FB.items() if e == "b"][0]
            a = FG.get(pa, 0) + FL.get(pa, 0) - FB.get(pa, 0); b = FG.get(pb, 0) + FL.get(pb, 0) - FA.get(pb, 0)
            return Fraction(a + b)
        if tid.startswith("m1-1-gcd-lcm-basic-t5"):
            m = re.match(r"어떤 자연수로 (\d+)[을를] 나누면 (\d+)[이가] 남고, (\d+)[을를] 나누면 (\d+)[이가] 남는다", q)
            A, r1, B, r2 = [int(m.group(i)) for i in (1, 2, 3, 4)]; g = math.gcd(A - r1, B - r2)
            return Fraction(g) if g > max(r1, r2) else None
        if tid.startswith("m1-1-gcd-lcm-basic-t6"):
            m = re.match(r"(\d+), (\d+), (\d+) 중 어느 수로 나누어도 나머지가 (\d+)인", q); a, b, c, r = [int(m.group(i)) for i in (1, 2, 3, 4)]
            return Fraction(math.lcm(a, b, c) + r)
        if tid.startswith("m1-1-gcd-lcm-basic-t7"):
            fr = re.findall(r"\[\[frac\((\d+),(\d+)\)\]\]", q); (n1, d1), (n2, d2) = [(int(x), int(y)) for x, y in fr[:2]]
            return Fraction(math.lcm(d1, d2), math.gcd(n1, n2))
    if tid.startswith("m1-1-rational-ops"):
        if tid.startswith("m1-1-rational-ops-t1"):
            m = re.match(r"\((-\d+)\)([²³]) × (\d+) ([+−]) (\d+) ÷ \((-\d+)\)", q)
            na, k, b, op, c, nd = int(m.group(1)), _sup(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5)), int(m.group(6))
            t = Fraction(na ** k * b); qq = Fraction(c, nd)
            return t + qq if op == "+" else t - qq
        if tid.startswith("m1-1-rational-ops-t2"):
            m = re.match(r"\(-\[\[frac\((\d+),(\d+)\)\]\]\)² × (\d+) ([+−]) \[\[frac\((\d+),(\d+)\)\]\] ÷ \(-\[\[frac\((\d+),(\d+)\)\]\]\)", q)
            a, b, e, op, c, d, f, h = [m.group(i) for i in range(1, 9)]
            t = Fraction(int(a) ** 2, int(b) ** 2) * int(e); qq = Fraction(int(c), int(d)) / (-Fraction(int(f), int(h)))
            return t + qq if op == "+" else t - qq
        if tid.startswith("m1-1-rational-ops-t3"):
            m = re.match(r"어떤 수(?:에서|에|를) (\d+)(?:를|로) (곱해야|나누어야|더해야|빼야) 할 것을 잘못하여 \d+(?:를|로) (나누었더니|곱했더니|뺐더니|더했더니) (\d+)[이가] 되었다", q)
            a, cr, wr, b = int(m.group(1)), m.group(2), m.group(3), Fraction(m.group(4))
            x = {"나누었더니": b * a, "곱했더니": b / a, "뺐더니": b + a, "더했더니": b - a}[wr]
            return {"곱해야": x * a, "나누어야": x / a, "더해야": x + a, "빼야": x - a}[cr]
        if tid.startswith("m1-1-rational-ops-t4"):
            m = re.match(r"(-?)\[\[frac\((\d+),(\d+)\)\]\]의 역수를 x, (-?\d+)의 역수를 y라 할 때, (.+?)의 값", q)
            x = Fraction(int(m.group(3)), int(m.group(2))) * (-1 if m.group(1) else 1); y = Fraction(1, int(m.group(4)))
            return {"x + y": x + y, "x − y": x - y, "xy": x * y}[m.group(5)]
        if tid.startswith("m1-1-rational-ops-t5"):
            m = re.match(r"(-?\d+)보다 (-?\d+)만큼 큰 수를 x, (-?\d+)보다 (-?\d+)만큼 작은 수를 y라 할 때, (.+?)의 값", q)
            a, b, c, d = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]; x, y = a + b, c - d
            return {"x + y": x + y, "x − y": x - y, "y − x": y - x}[m.group(5)]
    # ── 세션 5 (09-13): m1-1 문자와 식·방정식 — 식(문자열) 답은 check_linexpr 가 맡는다
    if tid.startswith("m1-1-expr-value"):
        if tid.startswith("m1-1-expr-value-t1"):
            m = re.match(r"x = (-?\d+)일 때, (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)의 값", q)
            a, p = Fraction(m.group(1)), _coef(m.group(2)); qv = _coef(m.group(4)) * (1 if m.group(3) == "+" else -1); r = int(m.group(6)) * (1 if m.group(5) == "+" else -1)
            return p * a * a + qv * a + r
        if tid.startswith("m1-1-expr-value-t2"):
            m = re.match(r"x = \[\[(-?)frac\((\d+),(\d+)\)\]\]일 때, (\d+)x² ([+−]) \[\[frac\(1,x\)\]\]", q)
            X = Fraction(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1); c = int(m.group(4)); o = 1 if m.group(5) == "+" else -1
            return c * X * X + o / X
        if tid.startswith("m1-1-expr-value-t3"):
            tail = q.split("이다. ", 1)[1]
            X = Fraction(re.search(r"(?:기온이|섭씨온도가|정가가|휘발유가|높이가|택시로|이 버스가) (-?\d+)", tail).group(1))
            if "소리의 속력" in q: return 331 + Fraction(3, 5) * X
            if "화씨" in q: return Fraction(9, 5) * X + 32
            if "판매 가격" in q: return Fraction(4, 5) * X
            if "휘발유" in q: return 15 * X
            if "택시" in q: return 4800 + 1000 * X
            if "고속버스" in q: return 80 * X
            return 25 - 6 * X
        if tid.startswith("m1-1-expr-value-t4"):
            m = re.match(r"a = (-?\d+), b = (-?\d+)일 때, (.+?)의 값", q); a, b = Fraction(m.group(1)), Fraction(m.group(2))
            e = m.group(3).replace("−", "-").replace("²", "**2").replace("ab", "a*b")
            e = re.sub(r"(\d)([ab])", r"\1*\2", e)
            return Fraction(eval(e, {"__builtins__": {}}, {"a": a, "b": b}))   # noqa: S307 — 문면의 a, b, 숫자, 연산자만
    if tid.startswith("m1-1-linear-expr-t1") or tid.startswith("m1-1-linear-expr-t2"):
        import mathir
        m = re.match(r"(.+?)[을를] 간단히 하였을 때, (.+?)[을를] 구하시오", q); expr = m.group(1).replace("−", "-").replace("[[", "").replace("]]", "")
        f = lambda x: Fraction(mathir.ev(mathir.parse(expr)[0], {"x": x}))   # noqa: E731
        A, B = f(1) - f(0), f(0); ask = m.group(2)
        return A + B if "합" in ask else (A if "계수" in ask else B)
    if tid.startswith("m1-1-eq-solution"):
        if tid.startswith("m1-1-eq-solution-t1"):
            m = re.match(r"등식 ax ([+−]) (\d+) = (-?\d*)x ([+−]) (\d*)b가 .*?대하여 (.+?)의 값", q)
            mv = int(m.group(2)) * (1 if m.group(1) == "+" else -1); a = _coef(m.group(3)); k = _coef(m.group(5)) * (1 if m.group(4) == "+" else -1); b = Fraction(mv) / k
            return {"a + b": a + b, "a − b": a - b, "ab": a * b}[m.group(6)]
        if tid.startswith("m1-1-eq-solution-t2"):
            m = re.match(r"x에 대한 일차방정식 (-?\d*)x ([+−]) a = (-?\d+)의 해가 x = (-?\d+)일 때", q)
            p, sa, r, k = _coef(m.group(1)), (1 if m.group(2) == "+" else -1), Fraction(m.group(3)), Fraction(m.group(4))
            return (r - p * k) / sa
        if tid.startswith("m1-1-eq-solution-t3"):
            m = re.match(r"x에 대한 일차방정식 ax ([+−]) (\d+) = (-?\d+)의 해가 x = (-?\d+)일 때", q)
            qv = int(m.group(2)) * (1 if m.group(1) == "+" else -1); r, k = Fraction(m.group(3)), Fraction(m.group(4)); return (r - qv) / k
        if tid.startswith("m1-1-eq-solution-t4"):
            m = re.match(r"두 일차방정식 (-?\d*)x ([+−]) (\d+) = (-?\d+), (-?\d*)x − a = (-?\d+)의 해가 서로 같을 때", q)
            p = _coef(m.group(1)); qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); r = Fraction(m.group(4)); sv = _coef(m.group(5)); t = Fraction(m.group(6))
            x0 = (r - qv) / p; return sv * x0 - t
    if tid.startswith("m1-1-linear-eq-const"):
        if tid.startswith("m1-1-linear-eq-const-t1"):
            m = re.match(r"x에 대한 일차방정식 (-?\d*)x ([+−]) (\d+) = (-?\d+)의 해가 일차방정식 (-?\d*)x \+ a = (-?\d+)의 해의 (\d+)배일 때", q)
            p = _coef(m.group(1)); qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); r = Fraction(m.group(4)); sv = _coef(m.group(5)); t = Fraction(m.group(6)); mult = int(m.group(7))
            x1 = (r - qv) / p; x2 = x1 / mult; return t - sv * x2
        if tid.startswith("m1-1-linear-eq-const-t2"):
            m = re.match(r"x에 대한 일차방정식 (\d+)x − (\d+) = a의 해가 자연수", q); p, qv = int(m.group(1)), int(m.group(2))
            return Fraction(sum(1 for a in range(10, 100) if (a + qv) % p == 0 and (a + qv) // p >= 1))
        if tid.startswith("m1-1-linear-eq-const-t3"):
            m = re.match(r"x에 대한 방정식 (-?\d*)x ([+−]) (\d+) = \(a ([+−]) (\d+)\)x ([+−]) (\d+)의 해가 없을 때", q)
            p = _coef(m.group(1)); k = int(m.group(5)) * (1 if m.group(4) == "+" else -1)
            qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); rv = int(m.group(7)) * (1 if m.group(6) == "+" else -1)
            return p - k if qv != rv else None
        if tid.startswith("m1-1-linear-eq-const-t4"):
            m = re.match(r"x에 대한 방정식 (-?\d*)x ([+−]) (\d+) = \(a ([+−]) (\d+)\)x ([+−]) (\d*)b의 해가 무수히 많을 때, .*?대하여 (.+?)의 값", q)
            p = _coef(m.group(1)); qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); k = int(m.group(5)) * (1 if m.group(4) == "+" else -1)
            kb = _coef(m.group(7)) * (1 if m.group(6) == "+" else -1); a = p - k; b = Fraction(qv) / kb
            return {"a + b": a + b, "a − b": a - b, "ab": a * b}[m.group(8)]
    if tid.startswith("m1-1-eq-apply-2"):
        if tid.startswith("m1-1-eq-apply-2-t1"):
            m = re.search(r"원가의 (\d+) %의 이익을 붙여 정가를 정하고, 정가에서 (\d+) %를 할인하여 팔았더니 (\d+)원의 이익", q)
            p, qv, r = [int(m.group(i)) for i in (1, 2, 3)]; return Fraction(r * 10000, (100 + p) * (100 - qv) - 10000)
        if tid.startswith("m1-1-eq-apply-2-t2"):
            m = re.search(r"A가 혼자 하면 (\d+)일, B가 혼자 하면 (\d+)일이 걸린다. 이 일을 A가 혼자 (\d+)일 동안", q)
            a, b, c = [int(m.group(i)) for i in (1, 2, 3)]; return Fraction(b * (a - c), a)
        if tid.startswith("m1-1-eq-apply-2-t3"):
            m = re.search(r"세로의 길이보다 (\d+) cm 더 긴 직사각형의 둘레의 길이가 (\d+) cm일 때, 이 직사각형의 (가로|세로)", q)
            d, P = int(m.group(1)), int(m.group(2)); x = Fraction(P - 2 * d, 4); return x + d if m.group(3) == "가로" else x
        if tid.startswith("m1-1-eq-apply-2-t4"):
            m = re.search(r"윗변의 길이가 (\d+) cm, 높이가 (\d+) cm인 사다리꼴의 넓이가 (\d+) cm²", q)
            a, h, S = [int(m.group(i)) for i in (1, 2, 3)]; return Fraction(2 * S, h) - a
    # ── 세션 5 (09-13): m1-1 좌표평면·정비례/반비례
    if tid.startswith("m1-1-coordinate"):
        if tid.startswith("m1-1-coordinate-t1"):
            m = re.match(r"두 순서쌍 \((-?\d*)a ([+−]) (\d+), (-?\d+)\), \((-?\d+), (-?\d*)b ([+−]) (\d+)\)[이가] 서로 같을 때, (.+?)의 값", q)
            p = _coef(m.group(1)); qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); r = Fraction(m.group(4)); sv = Fraction(m.group(5))
            t = _coef(m.group(6)); u = int(m.group(8)) * (1 if m.group(7) == "+" else -1)
            a, b = (sv - qv) / p, (r - u) / t
            return {"a + b": a + b, "a − b": a - b, "ab": a * b}[m.group(9)]
        if tid.startswith("m1-1-coordinate-t2"):
            m = re.match(r"점 \((-?\d+), (-?\d+)\)[와과] (x축|y축|원점)에 대하여 대칭인 점의 좌표가 \(a, b\)일 때, (.+?)의 값", q)
            x, y = Fraction(m.group(1)), Fraction(m.group(2)); ax = m.group(3)
            a, b = (x if ax == "x축" else -x), (y if ax == "y축" else -y)
            return {"a + b": a + b, "a − b": a - b, "ab": a * b}[m.group(4)]
        if tid.startswith("m1-1-coordinate-t3"):
            m = re.match(r"점 \(a, b\)가 제(\d)사분면 위의 점일 때, 점 \((.+?), (.+?)\)[는은] 제n사분면", q)
            k = int(m.group(1)); sa, sb = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}[k]
            def sg(e):
                e = e.replace("−", "-"); neg = e.startswith("-"); e = e.lstrip("-"); v = 1
                for ch in e.replace("²", "2"):
                    pass
                cnt_a = e.count("a"); cnt_b = e.count("b"); sq_a = "a²" in e; sq_b = "b²" in e
                v = (1 if sq_a else sa ** cnt_a) * (1 if sq_b else sb ** cnt_b)
                return -v if neg else v
            s1, s2 = sg(m.group(2)), sg(m.group(3))
            return Fraction({(1, 1): 1, (-1, 1): 2, (-1, -1): 3, (1, -1): 4}[(s1, s2)])
        if tid.startswith("m1-1-coordinate-t4"):
            pts = [(Fraction(x), Fraction(y)) for x, y in re.findall(r"\((-?\d+), (-?\d+)\)", q)]; A, B, C = pts[:3]
            return abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])) / 2
        if tid.startswith("m1-1-coordinate-t5"):
            m = re.match(r"점 \((-?\d*)a ([+−]) (\d+), (-?\d*)a ([+−]) (\d+)\)[이가] (x축|y축) 위의 점일 때, 이 점의 (x좌표|y좌표)", q)
            p = _coef(m.group(1)); qv = int(m.group(3)) * (1 if m.group(2) == "+" else -1); r = _coef(m.group(4)); sv = int(m.group(6)) * (1 if m.group(5) == "+" else -1)
            a = -Fraction(sv) / r if m.group(7) == "x축" else -Fraction(qv) / p
            return p * a + qv if m.group(8) == "x좌표" else r * a + sv
    if tid.startswith("m1-1-proportion"):
        if tid.startswith("m1-1-proportion-t1") or tid.startswith("m1-1-proportion-t2"):
            m = re.match(r"y가 x에 (정비례|반비례)하고, x = (-?\d+)일 때 y = (-?\d+)이다. x = (-?\d+)일 때", q)
            x1, y1, x2 = Fraction(m.group(2)), Fraction(m.group(3)), Fraction(m.group(4))
            return y1 / x1 * x2 if m.group(1) == "정비례" else x1 * y1 / x2
        if tid.startswith("m1-1-proportion-t3"):
            m = re.match(r"(정비례|반비례) 관계 .*?그래프가 점 \((-?\d+), (-?\d+)\)", q); p, qv = Fraction(m.group(2)), Fraction(m.group(3))
            return qv / p if m.group(1) == "정비례" else p * qv
        if tid.startswith("m1-1-proportion-t4"):
            m = re.match(r"(정비례|반비례) 관계 .*?두 점 \((-?\d+), (-?\d+)\), \(k, (-?\d+)\)", q); p, qv, r = Fraction(m.group(2)), Fraction(m.group(3)), Fraction(m.group(4))
            return r / (qv / p) if m.group(1) == "정비례" else (p * qv) / r
        if tid.startswith("m1-1-proportion-t5"):
            m = re.match(r"정비례 관계 y = (-?\d*)x의 그래프 위의 점 A의 x좌표가 (-?\d+)이다", q); a = _coef(m.group(1)); p = Fraction(m.group(2))
            return abs(p) * abs(a * p) / 2
        if tid.startswith("m1-1-proportion-t6") or tid.startswith("m1-1-proportion-t7"):
            m = re.match(r"반비례 관계 y = \[\[frac\((-?\d+),x\)\]\]의 그래프 위의 .*?(직사각형 OAPB|삼각형 OAP)의 넓이", q); k = int(m.group(1))
            return Fraction(abs(k)) / (2 if "삼각형" in m.group(2) else 1)
    # ── 세션 5 (09-13): m1-2 잔여 — 삼각형 각 2·평행선 접기·색칠 부분·세 변 조건·구 응용
    if tid.startswith("m1-2-tri-angle-2"):
        if tid.startswith("m1-2-tri-angle-2-t1"):
            m = re.search(r"= (\d+) : (\d+) : (\d+)일 때, (.+?)의 크기", q); a, b, c = [Fraction(m.group(i)) for i in (1, 2, 3)]; s = a + b + c
            ask = m.group(4); vals = {"A": 180 * a / s, "B": 180 * b / s, "C": 180 * c / s}
            return max(vals.values()) if "가장" in ask else vals[re.search(r"angle\(([ABC])\)", ask).group(1)]
        if tid.startswith("m1-2-tri-angle-2-t2"):
            a = Fraction(re.search(r"\[\[angle\(A\) = deg\((\d+)\)\]\]", q).group(1)); return 3 * a if "DCE" in _asked_angle(q) else 2 * a
        if tid.startswith("m1-2-tri-angle-2-t3"):
            g, v = _given1(q); return 90 + v / 2 if g == "A" else 2 * (v - 90)
    if tid.startswith("m1-2-parallel-fold"):
        given = {m.group(1): Fraction(m.group(2)) for m in re.finditer(r"\[\[angle\(([A-Z]+)\) = deg\((\d+)\)\]\]", q)}
        ask = _asked_angle(q)
        if tid.startswith(("m1-2-parallel-fold-t1", "m1-2-parallel-fold-t2", "m1-2-parallel-fold-t3", "m1-2-parallel-fold-t4")):
            a, x, c, d = given.get("QPB"), given.get("PBC"), given.get("BCQ"), given.get("RQC")      # a + c = x + d
            return {"PBC": lambda: a + c - d, "QPB": lambda: x + d - c, "BCQ": lambda: x + d - a, "RQC": lambda: a + c - x}[ask]()
        g, v = _given1(q)
        return 180 - 2 * v if g == "DEF" else (180 - v) / 2
    if tid.startswith("m1-2-sector-shade"):
        if tid.startswith("m1-2-sector-shade-t1") or tid.startswith("m1-2-sector-shade-t2"):
            th = Fraction(re.search(r"\[\[deg\((\d+)\)\]\]", q).group(1)); R, r = [Fraction(v) for v in re.findall(r"(\d+) cm", q)][:2]
            if tid.startswith("m1-2-sector-shade-t1"): return (R * R - r * r) * th / 360
            return 2 * (R + r) * th / 360 + 2 * (R - r)
        if tid.startswith("m1-2-sector-shade-t3"):
            a = Fraction(re.search(r"한 변의 길이가 (\d+) cm", q).group(1)); return a * a + a * a / 4
        if tid.startswith("m1-2-sector-shade-t4"):
            d1, d2 = [Fraction(v) for v in re.findall(r"= (\d+) cm", q)][:2]; return (d1 / 2) * (d2 / 2)
    if tid.startswith("m1-2-tri-sides"):
        a, b = [Fraction(v) for v in re.findall(r"(\d+) cm", q)][:2]
        return 2 * min(a, b) - 1 if tid.startswith("m1-2-tri-sides-t1") else 2 * max(a, b)
    if tid.startswith("m1-2-sphere-apply"):
        if tid.startswith("m1-2-sphere-apply-t1"):
            r = Fraction(re.search(r"반지름의 길이가 (\d+) cm인 구", q).group(1))
            return 2 * r ** 3 if "원기둥의 부피" in q else Fraction(2, 3) * r ** 3
        if tid.startswith("m1-2-sphere-apply-t2"):
            R, r = [Fraction(v) for v in re.findall(r"(\d+) cm", q)][:2]; return (R / r) ** 3
        if tid.startswith("m1-2-sphere-apply-t3"):
            R = Fraction(re.search(r"밑면의 반지름의 길이가 (\d+) cm", q).group(1)); r = Fraction(re.search(r"반지름의 길이가 (\d+) cm인 구", q).group(1))
            return Fraction(4, 3) * r ** 3 / (R * R)
        if tid.startswith("m1-2-sphere-apply-t4"):
            r = Fraction(re.search(r"반지름의 길이가 (\d+) cm인 반구", q).group(1)); R = Fraction(re.search(r"밑면의 반지름의 길이가 (\d+) cm", q).group(1))
            return Fraction(2, 3) * r ** 3 / (R * R)
    # ── 세션 5 (09-13): m2-1 수와 식 — 순환소수·단항식·다항식 (mkseed_m2_number.py)
    if tid.startswith("m2-1-repeating-decimal"):
        if tid.startswith(("m2-1-repeating-decimal-t1", "m2-1-repeating-decimal-t2")):
            m = re.search(r"\[\[frac\((\d+),(\d+)\)\]\]", q); P, Q = int(m.group(1)), int(m.group(2)); nn = int(re.search(r"소수점 아래 (\d+)번째", q).group(1))
            return Fraction((10 ** nn * P // Q) % 10)
        if tid.startswith("m2-1-repeating-decimal-t3"):
            rep = re.search(r"\[\[recdec\(0, (\d+)\)\]\]", q).group(1); v = Fraction(int(rep), 10 ** len(rep) - 1)
            return v.denominator + v.numerator if "a + b" in q else v.denominator - v.numerator
        if tid.startswith("m2-1-repeating-decimal-t4"):
            m = re.search(r"\[\[recdec\((\d+), (\d+), (\d+)\)\]\]", q); i, pre, cyc = m.group(1), m.group(2), m.group(3)
            v = int(i) + Fraction(int(pre), 10 ** len(pre)) + Fraction(int(cyc), (10 ** len(cyc) - 1) * 10 ** len(pre))
            return v.denominator + v.numerator if "a + b" in q else v.denominator - v.numerator
        if tid.startswith(("m2-1-repeating-decimal-t5", "m2-1-repeating-decimal-t6")):
            m = re.search(r"\[\[frac\((\d+),(\d+)\)\]\]", q); return Fraction(_strip25(Fraction(int(m.group(1)), int(m.group(2))).denominator))
        if tid.startswith("m2-1-repeating-decimal-t7"):
            B = int(re.search(r"x가 (\d+) 이하", q).group(1)); N = int(re.search(r"\[\[frac\(x, (\d+)\)\]\]", q).group(1)); return Fraction(B // _strip25(N))
        if tid.startswith("m2-1-repeating-decimal-t8"):
            A = int(re.search(r"\[\[frac\((\d+), ", q).group(1)); return Fraction(sum(1 for x in range(1, 10) if A % _strip25(x) == 0))
    if tid.startswith("m2-1-monomial-t1"):
        m = re.match(r"\((-?\d*)x([⁰¹²³⁴⁵⁶⁷⁸⁹]*)y\)([⁰¹²³⁴⁵⁶⁷⁸⁹]*) × \((-?\d*)xy([⁰¹²³⁴⁵⁶⁷⁸⁹]*)\)", q)
        p, mm, k, qq, nn = _coef(m.group(1)), _sup(m.group(2)), _sup(m.group(3)), _coef(m.group(4)), _sup(m.group(5))
        return p ** k * qq + (mm * k + 1) + (k + nn)
    if tid.startswith("m2-1-monomial-t2"):
        m = re.match(r"\((-?\d*)x([⁰¹²³⁴⁵⁶⁷⁸⁹]*)y([⁰¹²³⁴⁵⁶⁷⁸⁹]*)\)([⁰¹²³⁴⁵⁶⁷⁸⁹]*) ÷ \((-?\d*)x([⁰¹²³⁴⁵⁶⁷⁸⁹]*)y([⁰¹²³⁴⁵⁶⁷⁸⁹]*)\)", q)
        p, mm, nn, k, qq, ss, tt = _coef(m.group(1)), _sup(m.group(2)), _sup(m.group(3)), _sup(m.group(4)), _coef(m.group(5)), _sup(m.group(6)), _sup(m.group(7))
        return p ** k / qq + (mm * k - ss) + (nn * k - tt)
    if tid.startswith(("m2-1-polynomial-t1", "m2-1-polynomial-t3")):
        import sympy as sp
        body = re.match(r"(.+?)[을를] (?:전개하여 )?간단히 하였을 때", q).group(1); e = sp.Poly(sp.expand(_sy(body)), sp.Symbol("x"))
        c = {2: Fraction(str(e.coeff_monomial(sp.Symbol("x") ** 2))), 1: Fraction(str(e.coeff_monomial(sp.Symbol("x")))), 0: Fraction(str(e.coeff_monomial(1)))}
        return c[2] + c[1] if "합을" in q else (c[2] if "x²의 계수를" in q else (c[1] if "x의 계수를" in q else c[0]))
    if tid.startswith("m2-1-polynomial-t2"):
        import sympy as sp
        body = re.match(r"(.+?)를 간단히 하였을 때", q).group(1); e = sp.expand(_sy(body)); x, y = sp.Symbol("x"), sp.Symbol("y")
        cx, cy = Fraction(str(e.coeff(x))), Fraction(str(e.coeff(y)))
        return cx + cy if "합을" in q else (cx if "x의 계수를" in q else cy)
    if tid.startswith("m2-1-polynomial-t6"):
        import sympy as sp
        m = re.match(r"x = (-?\d+), y = (-?\d+)일 때, \((\[\[.+?\]\])\) ÷ (\S+)의 값", q); x, y = sp.Symbol("x"), sp.Symbol("y")
        v = sp.cancel(_sy(m.group(3)) / _sy(m.group(4))).subs({x: int(m.group(1)), y: int(m.group(2))}); return Fraction(str(v))
    # ── 세션 5 (09-13): m2-1 부등식 — 성질·풀이 2·활용 (mkseed_m2_ineq.py)
    if tid.startswith("m2-1-ineq-property"):
        if tid.startswith(("m2-1-ineq-property-t1", "m2-1-ineq-property-t2", "m2-1-ineq-property-t4")):
            m = re.match(r"(-?\d+) ([≤<]) x ([≤<]) (-?\d+)일 때, (.+?)의 값", q); a, XL, XR, b, ex = Fraction(m.group(1)), m.group(2), m.group(3), Fraction(m.group(4)), m.group(5)
            mm = re.match(r"(-?\d*)x ([+−]) (\d+)$", ex); m2 = re.match(r"\[\[frac\(x, (\d+)\)\]\] ([+−]) (\d+)$", ex)
            if mm:
                p = _coef(mm.group(1)); qv = Fraction(mm.group(3)) * (1 if mm.group(2) == "+" else -1)
            else:
                p = Fraction(1, int(m2.group(1))); qv = Fraction(m2.group(3)) * (1 if m2.group(2) == "+" else -1)
            ea, eb = p * a + qv, p * b + qv; lo, hi = min(ea, eb), max(ea, eb)
            if tid.startswith("m2-1-ineq-property-t2"):
                loinc, hiinc = (XL == "≤", XR == "≤") if p > 0 else (XR == "≤", XL == "≤")
                first = math.ceil(lo) + (0 if loinc or math.ceil(lo) != lo else 1); last = math.floor(hi) - (0 if hiinc or math.floor(hi) != hi else 1)
                return Fraction(last - first + 1)
            return hi + lo if "m + n" in q else hi - lo
        m = re.match(r"(-?\d+) ≤ x ≤ (-?\d+)일 때, (-?\d*)x \+ k의 (최댓값|최솟값)이 (-?\d+)이다", q); a, b, p, mx, V = Fraction(m.group(1)), Fraction(m.group(2)), _coef(m.group(3)), m.group(4), Fraction(m.group(5))
        xe = (b if p > 0 else a) if mx == "최댓값" else (a if p > 0 else b); return V - p * xe
    if tid.startswith("m2-1-ineq-solve-2-t4"):
        m = re.match(r"x에 대한 일차부등식 \[\[frac\(x − a, (\d+)\)\]\] [<>≤≥] (-?\d+)의 해가 x [<>≤≥] (-?\d+)일 때", q); return Fraction(m.group(3)) - Fraction(m.group(2)) * Fraction(m.group(1))
    if tid.startswith("m2-1-ineq-solve-2-t5"):
        m = re.match(r"두 일차부등식 (\d+)x ([+−]) (\d+) [<>≤≥] (-?\d+)[와과] (-?\d*)x \+ a [<>≤≥] (-?\d+)의 해가", q)
        p, qv, r, u, t = Fraction(m.group(1)), Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1), Fraction(m.group(4)), _coef(m.group(5)), Fraction(m.group(6))
        x0 = (r - qv) / p; return t - u * x0
    # ── 세션 5 (09-13): m2-1 연립방정식 — 풀이·활용 2 (mkseed_m2_system.py)
    if tid.startswith("m2-1-sys-solve"):
        ask = (lambda X, Y: X + Y if ("m + n" in q or "a + b" in q) else (X - Y if ("m − n" in q or "a − b" in q) else X * Y))
        if tid.startswith(("m2-1-sys-solve-t1", "m2-1-sys-solve-t2")):
            m = re.match(r"연립방정식 (.+?), (.+?)의 해가", q); e1, e2 = m.group(1), m.group(2)
            if tid.startswith("m2-1-sys-solve-t2"):
                mm = re.match(r"y = (-?\d*)x ([+−]) (\d+)$", e1); A = (-_coef(mm.group(1)), Fraction(1), Fraction(mm.group(3)) * (1 if mm.group(2) == "+" else -1))
            else:
                A = _lineq(e1)
            X, Y = _solve2(A, _lineq(e2)); return ask(X, Y)
        if tid.startswith("m2-1-sys-solve-t3"):
            m = re.match(r"연립방정식 ax \+ by = (-?\d+), bx − ay = (-?\d+)의 해가 x = (-?\d+), y = (-?\d+)", q); c1, c2, x0, y0 = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            A, B = _solve2((x0, y0, c1), (-y0, x0, c2)); return ask(A, B)
        if tid.startswith("m2-1-sys-solve-t4"):
            m = re.match(r"연립방정식 (.+?), ax (.+?) = (-?\d+)의 해와 연립방정식 (.+?), (-?\d*)x \+ by = (-?\d+)의 해가", q)
            X, Y = _solve2(_lineq(m.group(1)), _lineq(m.group(4))); q3 = _lineq("x " + m.group(2) + " = 0")[1]
            A = (Fraction(m.group(3)) - q3 * Y) / X; B = (Fraction(m.group(6)) - _coef(m.group(5)) * X) / Y; return ask(A, B)
        if tid.startswith("m2-1-sys-solve-t5"):
            m = re.search(r"일차방정식 (-?\d*)x \+ (\d*)y = (\d+)의 해의 개수", q); a, b, c = int(_coef(m.group(1))), int(_coef(m.group(2))), int(m.group(3))
            return Fraction(sum(1 for x in range(1, c) if c - a * x > 0 and (c - a * x) % b == 0))
        if tid.startswith("m2-1-sys-solve-t6"):
            m = re.match(r"방정식 (.+?) = (.+?) = (-?\d+)의 해가", q); t = m.group(3)
            X, Y = _solve2(_lineq(m.group(1) + " = " + t), _lineq(m.group(2) + " = " + t)); return ask(X, Y)
        if tid.startswith("m2-1-sys-solve-t7"):
            m = re.match(r"연립방정식 ax \+ by = (-?\d+), bx − ay = (-?\d+)에서 .+? 해가 x = (-?\d+), y = (-?\d+)이었다", q); c1, c2, pv, qv = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            A, B = _solve2((qv, pv, c1), (pv, -qv, c2)); X, Y = _solve2((A, B, c1), (B, -A, c2)); return ask(X, Y)
    if tid.startswith("m2-1-sys-apply-2"):
        if tid.startswith("m2-1-sys-apply-2-t1"):
            m = re.search(r"집에서 (\d+) km 떨어진 .+? 시속 (\d+) km로 걷다가 .+? 시속 (\d+) km로 뛰어서 모두 (\d+)분", q); D, a, b, T = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            X, Y = _solve2((1, 1, D), (60 / a, 60 / b, T)); return X if "걸은 거리" in q else Y
        if tid.startswith("m2-1-sys-apply-2-t2"):
            m = re.search(r"A가 (\d+)일 동안 한 다음 B가 (\d+)일 동안 하면 끝나고, A가 (\d+)일 동안 한 다음 B가 (\d+)일 동안 해도 끝난다. 이 일을 (A|B) 혼자", q)
            pv, qv, r, sv = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]; A, B = _solve2((pv, qv, 1), (r, sv, 1)); return 1 / (A if m.group(5) == "A" else B)
        if tid.startswith("m2-1-sys-apply-2-t3"):
            m = re.search(r"학생 (\d+)명이 본 .+? 전체 평균은 (\d+)점이고, 남학생의 평균은 (\d+)점, 여학생의 평균은 (\d+)점", q); n, M, a, b = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            X, Y = _solve2((1, 1, n), (a, b, M * n)); return X if "남학생은 몇 명" in q else Y
        if tid.startswith("m2-1-sys-apply-2-t4"):
            m = re.search(r"둘레의 길이가 (\d+) m인 .+? 둘레를 (\S+?)[와과] (\S+?)[이가] 같은 지점.+?반대 방향으로 돌면 (\d+)분.+?같은 방향으로 돌면 (\d+)분.+?빠를 때, (\S+?)의 속력은", q)
            L, t1, t2 = Fraction(m.group(1)), Fraction(m.group(4)), Fraction(m.group(5)); X, Y = _solve2((1, 1, L / t1), (1, -1, L / t2)); return X if m.group(6) == m.group(2) else Y
        if tid.startswith("m2-1-sys-apply-2-t5"):
            m = re.search(r"(\d+)%의 소금물과 (\d+)%의 소금물을 섞어서 (\d+)%의 소금물 (\d+) g을 만들려고 한다. (\d+)%의 소금물은", q); pv, qv, r, W, askp = [Fraction(m.group(i)) for i in (1, 2, 3, 4, 5)]
            X, Y = _solve2((1, 1, W), (pv, qv, r * W)); return X if askp == pv else Y
        if tid.startswith("m2-1-sys-apply-2-t6"):
            m = re.search(r"어른이 (\d+)원, 어린이가 (\d+)원이다. .+? 합하여 (\d+)명이 입장하는 데 모두 (\d+)원", q); a, b, n, T = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            X, Y = _solve2((1, 1, n), (a, b, T)); return X if "어른는 몇 명" in q or "어른은 몇 명" in q else Y
    # ── 세션 5 (09-13): m2-1 함수·일차함수 (mkseed_m2_func.py)
    if tid.startswith("m2-1-func-value"):
        if tid.startswith("m2-1-func-value-t1"):
            m = re.match(r"함수 f\(x\) = (-?\d*)x ([+−]) (\d+)에 대하여 f\((-?\d+)\) ([+−]) f\((-?\d+)\)", q); a = _coef(m.group(1)); b = Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1)
            fp, fq = a * Fraction(m.group(4)) + b, a * Fraction(m.group(6)) + b; return fp + fq if m.group(5) == "+" else fp - fq
        if tid.startswith("m2-1-func-value-t2"):
            m = re.match(r"함수 f\(x\) = \[\[frac\(a, x\)\]\] ([+−]) (\d+)에서 f\((-?\d+)\) = (-?\d+)", q); c = Fraction(m.group(2)) * (1 if m.group(1) == "+" else -1)
            return (Fraction(m.group(4)) - c) * Fraction(m.group(3))
        if tid.startswith("m2-1-func-value-t3"):
            m = re.match(r"함수 f\(x\) = ax \+ b에 대하여 f\((-?\d+)\) = (-?\d+), f\((-?\d+)\) = (-?\d+)일 때, .+?(a \+ b|a − b|ab)의 값", q)
            p, v1, qv, v2 = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]; a = (v2 - v1) / (qv - p); b = v1 - a * p
            return a + b if m.group(5) == "a + b" else (a - b if m.group(5) == "a − b" else a * b)
        m = re.match(r"함수 f\(x\) = (-?\d*)x \+ b에 대하여 f\((-?\d+)\) = (-?\d+)일 때, f\((-?\d+)\)", q); a = _coef(m.group(1)); b = Fraction(m.group(3)) - a * Fraction(m.group(2))
        return a * Fraction(m.group(4)) + b
    if tid.startswith("m2-1-line-props"):
        if tid.startswith("m2-1-line-props-t1"):
            m = re.match(r"일차함수 y = (-?\d*)x의 그래프를 y축의 방향으로 (-?\d+)만큼 평행이동한 그래프가 점 \((-?\d+), m\)", q); return _coef(m.group(1)) * Fraction(m.group(3)) + Fraction(m.group(2))
        if tid.startswith("m2-1-line-props-t2"):
            m = re.match(r"일차함수 y = (-?\d*)x의 그래프를 y축의 방향으로 k만큼 평행이동한 그래프가 점 \((-?\d+), (-?\d+)\)", q); return Fraction(m.group(3)) - _coef(m.group(1)) * Fraction(m.group(2))
        if tid.startswith("m2-1-line-props-t3"):
            m = re.match(r"일차함수 y = (-?\d*)x ([+−]) (\d+)의 그래프의 x절편을 p, y절편을 q라 할 때, (p \+ q|pq)", q); a = _coef(m.group(1)); b = Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1)
            p, qv = -b / a, b; return p + qv if m.group(4) == "p + q" else p * qv
        if tid.startswith("m2-1-line-props-t4"):
            m = re.match(r"두 일차함수 y = (-?\d*)x ([+−]) (\d+)[와과] y = \((-?\d*)k ([+−]) (\d+)\)x", q); a = _coef(m.group(1)); c = _coef(m.group(4)); d = Fraction(m.group(6)) * (1 if m.group(5) == "+" else -1)
            return (a - d) / c
        if tid.startswith("m2-1-line-props-t5"):
            m = re.match(r"일차함수 y = (-?\d*)x ([+−]) (\d+)의 그래프와 x축, y축", q); a = _coef(m.group(1)); b = Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1)
            return abs(b / a) * abs(b) / 2
        m = re.match(r"x절편이 (-?\d+), y절편이 (-?\d+)인", q); return -Fraction(m.group(2)) / Fraction(m.group(1))
    if tid.startswith("m2-1-line-apply"):
        if tid.startswith("m2-1-line-apply-t1"):
            m = re.match(r"(\d+) L의 물이 들어 있는 물통에 매분 (\d+) L씩 물을 (넣는다|뺀다).+?물의 양이 (\d+) L가 되는", q); V0, r, T = Fraction(m.group(1)), Fraction(m.group(2)), Fraction(m.group(4))
            return (T - V0) / r if m.group(3) == "넣는다" else (V0 - T) / r
        if tid.startswith("m2-1-line-apply-t2"):
            m = re.match(r"길이가 (\d+) cm인 양초에 불을 붙이면 (\d+)분마다 (\d+) cm씩 짧아진다.+?남은 길이가 (\d+) cm가 되는", q); L0, t, d, R = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]; return (L0 - R) * t / d
        if tid.startswith("m2-1-line-apply-t3"):
            m = re.match(r"지면의 기온이 (\d+) ℃이고, 높이가 1 km 높아질 때마다 기온은 (\d+) ℃씩.+?높이가 (\d+) km인 곳", q); return Fraction(m.group(1)) - Fraction(m.group(2)) * Fraction(m.group(3))
        if tid.startswith("m2-1-line-apply-t4"):
            m = re.search(r"\[\[seg\(AB\)\]\] = (\d+) cm, \[\[seg\(BC\)\]\] = (\d+) cm.+?매초 (\d+) cm.+?넓이가 (\d+) cm²가 되는", q); a, v, S = Fraction(m.group(1)), Fraction(m.group(3)), Fraction(m.group(4)); return 2 * S / (a * v)
        m = re.match(r"어떤 용수철에 (\d+) g의 추를 매달면 길이가 (\d+) cm가 되고, (\d+) g의 추를 매달면 길이가 (\d+) cm가 된다.+?(\d+) g의 추를 매달면", q); w1, L1, w2, L2, w3 = [Fraction(m.group(i)) for i in (1, 2, 3, 4, 5)]
        a = (L2 - L1) / (w2 - w1); return L1 + a * (w3 - w1)
    if tid.startswith("m2-1-line-intersect"):
        if tid.startswith("m2-1-line-intersect-t1"):
            m = re.match(r"일차방정식 (-?\d*)x ([+−]) (\d*)y ([+−]) (\d+) = 0의 그래프의 기울기를 p, y절편을 q라 할 때, (p \+ q|pq)", q); a = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); c = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            p, qv = -a / b, -c / b; return p + qv if m.group(6) == "p + q" else p * qv
        if tid.startswith("m2-1-line-intersect-t2"):
            m = re.match(r"두 직선 (.+?), (.+?)의 교점의 좌표가 \(p, q\)일 때, (p \+ q|pq)", q); X, Y = _solve2(_lineq(m.group(1)), _lineq(m.group(2))); return X + Y if m.group(3) == "p + q" else X * Y
        if tid.startswith("m2-1-line-intersect-t3"):
            m = re.match(r"연립방정식 (-?\d*)x ([+−]) (\d*)y = (-?\d+), ax ([+−]) (\d*)y = b의 해가 무수히 많을 때", q); p = _coef(m.group(1)); qv = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); r = Fraction(m.group(4))
            kq = _coef(m.group(6)) * (1 if m.group(5) == "+" else -1); k = kq / qv; return k * p + k * r
        if tid.startswith("m2-1-line-intersect-t4"):
            m = re.match(r"연립방정식 (-?\d*)x ([+−]) (\d*)y = (-?\d+), ax ([+−]) (\d*)y = (-?\d+)의 해가 없을 때", q); p = _coef(m.group(1)); qv = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1)
            kq = _coef(m.group(6)) * (1 if m.group(5) == "+" else -1); return kq / qv * p
        if tid.startswith("m2-1-line-intersect-t5"):
            m = re.match(r"세 직선 (.+?), (.+?), ax − y = (-?\d+)[이가] 한 점에서", q); X, Y = _solve2(_lineq(m.group(1)), _lineq(m.group(2))); return (Fraction(m.group(3)) + Y) / X
        m = re.search(r"\((-?\d*)k ([+−]) (\d+), (-?\d+)\), \((-?\d*)k ([+−]) (\d+), (-?\d+)\)", q) or re.search(r"\((-?\d+), (-?\d*)k ([+−]) (\d+)\), \((-?\d+), (-?\d*)k ([+−]) (\d+)\)", q)
        g = m.groups()
        if tid.startswith("m2-1-line-intersect-t6"):
            c1, d1, c2, d2 = _coef(g[0]), Fraction(g[2]) * (1 if g[1] == "+" else -1), _coef(g[4]), Fraction(g[6]) * (1 if g[5] == "+" else -1)
        else:
            c1, d1, c2, d2 = _coef(g[1]), Fraction(g[3]) * (1 if g[2] == "+" else -1), _coef(g[5]), Fraction(g[7]) * (1 if g[6] == "+" else -1)
        return (d2 - d1) / (c1 - c2)
    if tid.startswith("m2-1-ineq-apply"):
        if tid.startswith("m2-1-ineq-apply-t1"):
            m = re.search(r"(\d+)점, (\d+)점, (\d+)점을 받았다. 네 번째 시험까지의 평균이 (\d+)점 이상", q); return 4 * Fraction(m.group(4)) - sum(Fraction(m.group(i)) for i in (1, 2, 3))
        if tid.startswith("m2-1-ineq-apply-t2"):
            m = re.search(r"(\d+)원인 .+?(\d+)원인 .+? 합하여 (\d+)\S* 사려고 한다. 전체 금액이 (\d+)원 이하", q); a, b, nn, B = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            return Fraction(math.floor((B - a * nn) / (b - a)))
        if tid.startswith("m2-1-ineq-apply-t3"):
            m = re.search(r"출발까지 (\d+)분이 남아 있다. 시속 (\d+) km로 .+? 사는 데 (\d+)분이 걸린다", q); T, v, sv = [Fraction(m.group(i)) for i in (1, 2, 3)]; return v * (T - sv) / 120
        if tid.startswith("m2-1-ineq-apply-t5"):
            m = re.search(r"한 번에 (\d+) kg까지 .+? 몸무게가 (\d+) kg인 사람이 한 개에 (\d+) kg인", q); W, pv, w = [Fraction(m.group(i)) for i in (1, 2, 3)]; return Fraction(math.floor((W - pv) / w))
    if tid.startswith("m3-1-factor"):
        if tid == "m3-1-factor-t1":
            m = re.match(r"식 (.+?)[이가] 완전제곱식이 될 때, (□ 안에 알맞은 수|□ 안에 알맞은 양수)", q); e = m.group(1)
            mc = re.fullmatch(r"(\d*)x² ([+−]) (\d+)x \+ □", e); mk = re.fullmatch(r"(\d*)x² \+ □x \+ (\d+)", e)
            if mc:
                pp = _isqrt(_coef(mc.group(1))); return (Fraction(mc.group(3)) / (2 * pp)) ** 2
            pp = _isqrt(_coef(mk.group(1))); qq = _isqrt(Fraction(mk.group(2))); return 2 * pp * qq
        if tid == "m3-1-factor-t2":
            m = re.match(r"x² ([+−]) (\d*)x ([+−]) (\d+)[을를] 인수분해하면", q); b = _coef(m.group(2)) * (1 if m.group(1) == "+" else -1); c = Fraction(m.group(4)) * (1 if m.group(3) == "+" else -1)
            return _isqrt(b * b - 4 * c)
        if tid == "m3-1-factor-t3":
            m = re.match(r"(-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)[을를] 인수분해하면", q); A = _coef(m.group(1)); B = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); C = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            sols = {a + b + c + d for a in range(1, 4) for c in range(a, 4) for b in range(-6, 7) for d in range(-6, 7) if b and d and a * c == A and a * d + b * c == B and b * d == C and math.gcd(a, b) == 1 and math.gcd(c, d) == 1}
            return Fraction(sols.pop()) if len(sols) == 1 else None
        if tid == "m3-1-factor-t4":
            m = re.match(r"(.+?)[을를] 인수분해하면 (a\(x \+ b\)²|a\(x \+ b\)\(x − b\))일 때", q); e = m.group(1)
            ms = re.fullmatch(r"(\d+)x² ([+−]) (\d+)x \+ (\d+)", e); md = re.fullmatch(r"(\d+)x² − (\d+)", e)
            if ms:
                k = Fraction(ms.group(1)); bb = Fraction(ms.group(3)) * (1 if ms.group(2) == "+" else -1) / (2 * k); return k + bb
            k = Fraction(md.group(1)); return k + _isqrt(Fraction(md.group(2)) / k)
        if tid == "m3-1-factor-t5":
            m = re.match(r"\(x ([+−]) (\d+)\)² ([+−]) (\d*)\(x [+−] \d+\) ([+−]) (\d+)[을를] 인수분해하면", q); a = Fraction(m.group(2)) * (1 if m.group(1) == "+" else -1); b = _coef(m.group(4)) * (1 if m.group(3) == "+" else -1); c = Fraction(m.group(6)) * (1 if m.group(5) == "+" else -1)
            return a * a + a * b + c
        if tid == "m3-1-factor-t6":
            m = re.match(r"x = (\d+) \+ \[\[sqrt\((\d+)\)\]\], y = (\d+) − \[\[sqrt\((\d+)\)\]\]일 때, (.+?)[을를] 구하시오", q); c, a = Fraction(m.group(1)), Fraction(m.group(2)); ask = m.group(5)
            if m.group(3) != m.group(1) or m.group(4) != m.group(2): return None
            if ask.startswith("x² + 2xy + y²"): return 4 * c * c
            if ask.startswith("x² − y²"): return 4 * c
            return 2 * (c * c - a)
    if tid.startswith("m3-1-quad-solve"):
        if tid == "m3-1-quad-solve-t2":
            m = re.match(r"이차방정식 x² \+ ax ([+−]) (\d+) = 0의 한 근이 (-?\d+)일 때", q); c = Fraction(m.group(2)) * (1 if m.group(1) == "+" else -1); pp = Fraction(m.group(3))
            A = -(pp * pp + c) / pp; qq = c / pp; return A * qq
        if tid == "m3-1-quad-solve-t3":
            m = re.match(r"이차방정식 (-?\d*)\(x ([+−]) (\d+)\)² = (\d+)의 해가", q); A = _coef(m.group(1)); pp = -Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1); k = Fraction(m.group(4)) / A
            return pp + k if k.denominator == 1 else None
        if tid == "m3-1-quad-solve-t4":
            m = re.match(r"이차방정식 x² ([+−]) (\d*)x ([+−]) (\d+) = 0을 완전제곱식", q); b = _coef(m.group(2)) * (1 if m.group(1) == "+" else -1); c = Fraction(m.group(4)) * (1 if m.group(3) == "+" else -1)
            mm = b / 2; D = mm * mm - c; return -mm + D
        if tid == "m3-1-quad-solve-t5":
            m = re.match(r"이차방정식 (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 두 근 중 큰 근이", q); a = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); c = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            D = b * b - 4 * a * c; return -b + D + 2 * a if D > 1 and _sqfree(int(D))[0] == 1 else None
        if tid == "m3-1-quad-solve-t6":
            m = re.match(r"이차방정식 (.+?) = 0이 중근을 가질 때, (상수 k|양수 k)", q); e = m.group(1)
            mc = re.fullmatch(r"(\d*)x² ([+−]) (\d+)x \+ k", e); mk = re.fullmatch(r"(\d*)x² \+ kx \+ (\d+)", e)
            if mc:
                pp = _isqrt(_coef(mc.group(1))); return (Fraction(mc.group(3)) / (2 * pp)) ** 2
            pp = _isqrt(_coef(mk.group(1))); qq = _isqrt(Fraction(mk.group(2))); return 2 * pp * qq
    if tid.startswith("m3-1-quad-apply"):
        if tid == "m3-1-quad-apply-t1":
            m = re.match(r"연속한 두 자연수의 제곱의 합이 (\d+)일 때, (두 수 중 큰 수|두 수 중 작은 수)", q); S = int(m.group(1))
            for nn in range(1, 100):
                if nn * nn + (nn + 1) ** 2 == S: return Fraction(nn + (1 if m.group(2).endswith("큰 수") else 0))
            return None
        if tid == "m3-1-quad-apply-t2":
            m = re.match(r"차가 (\d+)이고 곱이 (\d+)인 두 자연수가 있다. (두 수 중 큰 수|두 수 중 작은 수)", q); d, P = int(m.group(1)), int(m.group(2))
            for a in range(1, 200):
                if a * (a + d) == P: return Fraction(a + (d if m.group(3).endswith("큰 수") else 0))
            return None
        if tid == "m3-1-quad-apply-t3":
            m = re.search(r" (\d+)\S+ 학생들에게 남김없이 똑같이 나누어 주었더니 한 학생이 받은 \S+ 수가 학생 수보다 (\d+)만큼 (적었다|많았다)", q); P, d = int(m.group(1)), int(m.group(2)); sg = -1 if m.group(3) == "적었다" else 1
            for x in range(1, 200):
                if x * (x + sg * d) == P: return Fraction(x)
            return None
        if tid == "m3-1-quad-apply-t4":
            m = re.match(r"가로의 길이가 세로의 길이보다 (\d+) cm 긴 직사각형의 넓이가 (\d+) cm²일 때, 이 직사각형의 (세로의 길이|가로의 길이)", q); d, S = int(m.group(1)), int(m.group(2))
            for a in range(1, 200):
                if a * (a + d) == S: return Fraction(a + (d if m.group(3).startswith("가로") else 0))
            return None
        if tid == "m3-1-quad-apply-t5":
            m = re.match(r"정사각형의 각 변의 길이를 (\d+) cm씩 늘였더니 넓이가 (\d+) cm²", q); d, S = int(m.group(1)), Fraction(m.group(2)); r = _isqrt(S); return r - d if r else None
        if tid == "m3-1-quad-apply-t6":
            m = re.match(r"가로의 길이가 (\d+) m, 세로의 길이가 (\d+) m인 직사각형 모양의 땅에 .+? 넓이가 (\d+) m²", q); W, H, R = int(m.group(1)), int(m.group(2)), int(m.group(3))
            xs = [x for x in range(1, min(W, H)) if (W - x) * (H - x) == R]; return Fraction(xs[0]) if len(xs) == 1 else None
        if tid == "m3-1-quad-apply-t7":
            m = re.match(r"지면에서 초속 (\d+) m로 .+?높이가 (처음으로|두 번째로) (\d+) m가 되는", q); v, H = int(m.group(1)), int(m.group(3))
            ts = [t for t in range(0, 100) if v * t - 5 * t * t == H]; return Fraction(ts[0] if m.group(2) == "처음으로" else ts[-1]) if len(ts) == 2 else None
        if tid == "m3-1-quad-apply-t8":
            D = int(re.match(r"대각선의 총 개수가 (\d+)인 다각형", q).group(1))
            for nn in range(3, 100):
                if nn * (nn - 3) == 2 * D: return Fraction(nn)
            return None
    if tid.startswith("m3-1-quad-func-apply"):
        if tid == "m3-1-quad-func-apply-t1":
            m = re.match(r"이차함수 y = (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)의 (최댓값|최솟값)", q); a = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); c = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            if (a < 0) != (m.group(6) == "최댓값"): return None
            return c - b * b / (4 * a)
        if tid == "m3-1-quad-func-apply-t2":
            m = re.match(r"이차함수 y = (-?\d*)x² ([+−]) (\d*)x \+ c의 (최댓값|최솟값)이 (-?\d+)일 때", q); a = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); M = Fraction(m.group(5))
            if (a < 0) != (m.group(4) == "최댓값"): return None
            return M + b * b / (4 * a)
        if tid == "m3-1-quad-func-apply-t3":
            L = Fraction(re.match(r"둘레의 길이가 (\d+) cm인 직사각형", q).group(1)); return (L / 4) ** 2
        m = re.match(r"지면에서 초속 (\d+) m로 .+?h = (\d+)t − 5t².+?이 물체의 (최고 높이|최고 높이에 도달하는 시각)[을를]", q); v = Fraction(m.group(1))
        if m.group(2) != m.group(1): return None
        return v * v / 20 if m.group(3) == "최고 높이" else v / 10
    if tid.startswith("m3-1-quad-func"):
        if tid == "m3-1-quad-func-t1":
            m = re.match(r"이차함수 y = ax²의 그래프가 점 \((-?\d+), (-?\d+)\)를 지날 때, 상수 a", q); pp, qq = Fraction(m.group(1)), Fraction(m.group(2)); return qq / (pp * pp)
        if tid == "m3-1-quad-func-t2":
            m = re.match(r"이차함수 y = ax²의 그래프가 두 점 \((-?\d+), (-?\d+)\), \((-?\d+), k\)를 지날 때", q); pp, qq, mm = [Fraction(m.group(i)) for i in (1, 2, 3)]; return qq / (pp * pp) * mm * mm
        if tid == "m3-1-quad-func-t3":
            m = re.match(r"이차함수 y = (-?\d*)x²의 그래프를 x축의 방향으로 (-?\d+)만큼, y축의 방향으로 (-?\d+)만큼 평행이동한 그래프가 점 \((-?\d+), k\)", q); a = _coef(m.group(1)); pp, qq, mm = [Fraction(m.group(i)) for i in (2, 3, 4)]
            return a * (mm - pp) ** 2 + qq
        if tid == "m3-1-quad-func-t4":
            m = re.match(r"이차함수 y = (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)의 그래프의 꼭짓점의 좌표가 \(p, q\)일 때, (p \+ q|pq)", q); a = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1); c = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            pp = -b / (2 * a); qq = c - b * b / (4 * a); return pp + qq if m.group(6) == "p + q" else pp * qq
        if tid == "m3-1-quad-func-t5":
            m = re.match(r"이차함수 y = (-?\d*)\(x ([+−]) (\d+)\)² ([+−]) (\d+)의 그래프가 x축과 만나는 두 점에 대하여 (두 점 사이의 거리|두 점의 x좌표의 곱)", q); a = _coef(m.group(1)); pp = -Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1); qq = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            s_ = _isqrt(-qq / a)
            if s_ is None: return None
            return 2 * s_ if m.group(6) == "두 점 사이의 거리" else (pp - s_) * (pp + s_)
        if tid == "m3-1-quad-func-t6":
            m = re.match(r"이차함수 y = (-?\d*)\(x ([+−]) (\d+)\)² ([+−]) (\d+)의 그래프가 y축과 만나는 점", q); a = _coef(m.group(1)); pp = -Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1); qq = Fraction(m.group(5)) * (1 if m.group(4) == "+" else -1)
            return a * pp * pp + qq
        m = re.match(r"꼭짓점의 좌표가 \((-?\d+), (-?\d+)\)이고 점 \((-?\d+), (-?\d+)\)을 지나는 이차함수", q); pp, qq, mm, nn = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
        a = (nn - qq) / (mm - pp) ** 2; return a - 2 * a * pp + a * pp * pp + qq
    if tid.startswith("m3-2-trig-basic"):
        if tid == "m3-2-trig-basic-t1":
            sides = {k: Fraction(v) for k, v in re.findall(r"\[\[seg\((AB|BC|AC)\)\]\] = (\d+)", q)}
            if "AB" not in sides: sides["AB"] = _isqrt(sides["BC"] ** 2 + sides["AC"] ** 2)
            if "BC" not in sides: sides["BC"] = _isqrt(sides["AB"] ** 2 - sides["AC"] ** 2)
            if "AC" not in sides: sides["AC"] = _isqrt(sides["AB"] ** 2 - sides["BC"] ** 2)
            F = re.search(r"일 때, (sin|cos|tan) (A|B)의 값", q); f, v = F.group(1), F.group(2)
            a, b, c = sides["BC"], sides["AC"], sides["AB"]
            return {("sin", "A"): a / c, ("cos", "A"): b / c, ("tan", "A"): a / b, ("sin", "B"): b / c, ("cos", "B"): a / c, ("tan", "B"): b / a}[(f, v)]
        if tid == "m3-2-trig-basic-t2":
            m = re.search(r"(sin|cos|tan) A = \[\[frac\((\d+), (\d+)\)\]\]일 때, (.+?)의 값", q); f, n1, n2, ask = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
            if f == "sin": a, c = n1, n2; b = _isqrt(c * c - a * a)
            elif f == "cos": b, c = n1, n2; a = _isqrt(c * c - b * b)
            else: a, b = n1, n2; c = _isqrt(a * a + b * b)
            V = {"sin A": Fraction(a) / c, "cos A": Fraction(b) / c, "tan A": Fraction(a) / b}
            mm = re.fullmatch(r"(sin A|cos A|tan A)(?: ([+×]) (sin A|cos A|tan A))?", ask)
            if not mm.group(2): return V[mm.group(1)]
            return V[mm.group(1)] + V[mm.group(3)] if mm.group(2) == "+" else V[mm.group(1)] * V[mm.group(3)]
        if tid == "m3-2-trig-basic-t3":
            m = re.match(r"(sin|cos|tan) (\d+)° ([+−×÷]) (sin|cos|tan) (\d+)°의 값", q); fn = {"sin": math.sin, "cos": math.cos, "tan": math.tan}
            v1, v2 = fn[m.group(1)](math.radians(int(m.group(2)))), fn[m.group(4)](math.radians(int(m.group(5)))); op = m.group(3)
            r = v1 + v2 if op == "+" else v1 - v2 if op == "−" else v1 * v2 if op == "×" else v1 / v2
            return Fraction(r).limit_denominator(1000)
        if tid == "m3-2-trig-basic-t4":
            m = re.search(r"(sin|cos|tan) (x|\(x [+−] \d+°\)|2x) = (.+?)[을를] 만족하는 x", q); f, arg, vtxt = m.group(1), m.group(2), m.group(3)
            target = _mval(vtxt); fn = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[f]
            th = next((t for t in (30, 45, 60) if abs(fn(math.radians(t)) - target) < 1e-6), None)
            if th is None: return None
            if arg == "x": return Fraction(th)
            if arg == "2x": return Fraction(th, 2)
            ma = re.fullmatch(r"\(x ([+−]) (\d+)°\)", arg); return Fraction(th - int(ma.group(2))) if ma.group(1) == "+" else Fraction(th + int(ma.group(2)))
        m = re.search(r"\[\[angle\(A\)\]\] = \[\[deg\((\d+)\)\]\]인 직각삼각형 ABC에서 (빗변 AB|이웃변 AC)의 길이가 (\d+)일 때 \[\[seg\((BC|AC)\)\]\]의 길이를 구하시오. \(sin \d+° = ([\d.]+), cos \d+° = ([\d.]+), tan \d+° = ([\d.]+)\)", q)
        h = Fraction(m.group(3)); S, C, T = Fraction(m.group(5)), Fraction(m.group(6)), Fraction(m.group(7))
        if m.group(2) == "빗변 AB": return h * S if m.group(4) == "BC" else h * C
        return h * T
    if tid.startswith("m3-2-circle-chord-tangent"):
        if tid == "m3-2-circle-chord-tangent-t1":
            r = re.search(r"반지름의 길이가 (\d+)", q); ab = re.search(r"\[\[seg\(AB\)\]\] = (\d+)", q); om = re.search(r"\[\[seg\(OM\)\]\] = (\d+)", q)
            if r and om: return 2 * _isqrt(int(r.group(1)) ** 2 - int(om.group(1)) ** 2)
            if ab and om: return _isqrt(int(om.group(1)) ** 2 + (int(ab.group(1)) // 2) ** 2)
            return _isqrt(int(r.group(1)) ** 2 - (int(ab.group(1)) // 2) ** 2)
        if tid == "m3-2-circle-chord-tangent-t2":
            r = re.search(r"반지름의 길이가 (\d+)", q); pa = re.search(r"\[\[seg\(PA\)\]\] = (\d+)", q); op = re.search(r"\[\[seg\(OP\)\]\] = (\d+)", q)
            if r and op: return _isqrt(int(op.group(1)) ** 2 - int(r.group(1)) ** 2)
            if pa and op: return _isqrt(int(op.group(1)) ** 2 - int(pa.group(1)) ** 2)
            return _isqrt(int(r.group(1)) ** 2 + int(pa.group(1)) ** 2)
        if tid == "m3-2-circle-chord-tangent-t3":
            m = re.search(r"\[\[angle\((APB|AOB)\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\((AOB|APB|PAB)\)\]\]", q); gq, gv, xq = m.group(1), Fraction(m.group(2)), m.group(3)
            if xq == "PAB": return (180 - gv) / 2 if gq == "APB" else None
            return 180 - gv
        if tid == "m3-2-circle-chord-tangent-t4":
            m = re.search(r"\[\[seg\(AB\)\]\] = (\d+), \[\[seg\(BC\)\]\] = (\d+), \[\[seg\(CA\)\]\] = (\d+)일 때, \[\[seg\((AD|BE|CF)\)\]\]", q); c, a, b = [Fraction(m.group(i)) for i in (1, 2, 3)]
            return {"AD": (b + c - a) / 2, "BE": (a + c - b) / 2, "CF": (a + b - c) / 2}[m.group(4)]
        sides = {k: Fraction(v) for k, v in re.findall(r"\[\[seg\((AB|BC|CD|DA)\)\]\] = (\d+)", q)}; ask = re.search(r"일 때, \[\[seg\((AB|BC|CD|DA)\)\]\]의 길이", q).group(1)
        if ask == "AB": return sides["BC"] + sides["DA"] - sides["CD"]
        if ask == "CD": return sides["BC"] + sides["DA"] - sides["AB"]
        if ask == "BC": return sides["AB"] + sides["CD"] - sides["DA"]
        return sides["AB"] + sides["CD"] - sides["BC"]
    if tid.startswith("m3-2-circle-angle"):
        if tid == "m3-2-circle-angle-t1":
            m = re.search(r"\[\[angle\((AOB|APB)\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\((APB|AOB)\)\]\]", q); gv = Fraction(m.group(2))
            return gv / 2 if m.group(1) == "AOB" else 2 * gv
        if tid == "m3-2-circle-angle-t2":
            m = re.search(r"\[\[angle\((CAB|ABC)\)\]\] = \[\[deg\((\d+)\)\]\]", q); return 90 - Fraction(m.group(2))
        if tid == "m3-2-circle-angle-t3":
            m = re.search(r"\[\[angle\((A|B)\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\((BCD|ADC)\)\]\]", q); return 180 - Fraction(m.group(2))
        if tid == "m3-2-circle-angle-t4":
            m = re.search(r"\[\[angle\(BAT\)\]\] = \[\[deg\((\d+)\)\]\], \[\[angle\((ABC|BAC)\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\((BAC|ABC)\)\]\]", q)
            if m.group(2) == m.group(4): return None
            return 180 - Fraction(m.group(1)) - Fraction(m.group(3))
        if tid == "m3-2-circle-angle-t6":
            m = re.search(r"\[\[angle\(DCE\)\]\] = \[\[deg\((\d+)\)\]\], \[\[angle\(ABD\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\(ADB\)\]\]", q); return 180 - Fraction(m.group(1)) - Fraction(m.group(2))
        m = re.search(r"호 CD의 길이의 (\d+)배이다. \[\[angle\((CQD|APB)\)\]\] = \[\[deg\((\d+)\)\]\]일 때, \[\[angle\((APB|CQD)\)\]\]", q); n, gq, gv = int(m.group(1)), m.group(2), Fraction(m.group(3))
        return gv * n if gq == "CQD" else gv / n
    if tid.startswith("m3-2-stat"):
        if tid == "m3-2-stat-t1":
            m = re.search(r"평균이 (\d+)\S*일 때, x의 값[을를] 구하시오.  \[ (.+?) \]", q); mean = int(m.group(1)); items = [t.strip() for t in m.group(2).split(",")]
            known = [int(t) for t in items if t != "x"]; return Fraction(mean * len(items) - sum(known))
        if tid == "m3-2-stat-t2":
            m = re.search(r"(a \+ b|a − b)의 값을 구하시오.  \[ (.+?) \]", q); vals = sorted(int(t) for t in m.group(2).split(",")); n = len(vals)
            med = Fraction(vals[n // 2]) if n % 2 else Fraction(vals[n // 2 - 1] + vals[n // 2], 2)
            cnt = {v: vals.count(v) for v in set(vals)}; mode = max(cnt, key=lambda v: (cnt[v], -v)); return med + mode if m.group(1) == "a + b" else med - mode
        if tid == "m3-2-stat-t3":
            m = re.search(r"평균이 (\d+)점일 때, (x의 값|학생 ([A-E])의 점수)[을를] 구하시오.  \[ (.+?) \]", q); mean = int(m.group(1)); cells = [t.split(":")[1].strip() for t in m.group(4).split(",")]
            known = [int(t) for t in cells if t != "x"]; x = -sum(known)
            if m.group(2) == "x의 값": return Fraction(x)
            d = cells["ABCDE".index(m.group(3))]; return Fraction(mean + (x if d == "x" else int(d)))
        if tid == "m3-2-stat-t4":
            m = re.search(r"이 자료의 (분산|표준편차)[을를] 구하시오.  \[ (.+?) \]", q); vals = [int(t) for t in m.group(2).split(",")]; n = len(vals); mean = Fraction(sum(vals), n)
            var = sum((v - mean) ** 2 for v in vals) / n; return var if m.group(1) == "분산" else _isqrt(var)
        m = re.search(r"평균이 (\d+), 분산이 (\d+)일 때, 변량 (.+?)의 (평균|분산|표준편차)[을를] 구하시오", q); mean, var, tr, ask = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
        first = tr.split(",")[0].strip()
        mk_ = re.fullmatch(r"(\d*)a(?: \+ (\d+))?", first); k = int(mk_.group(1)) if mk_.group(1) else 1; c = int(mk_.group(2)) if mk_.group(2) else 0
        if ask == "평균": return Fraction(k * mean + c)
        return Fraction(k * k * var) if ask == "분산" else _isqrt(k * k * var)
    if tid.startswith("h1-1-poly-t"):
        if tid == "h1-1-poly-t1":
            m = re.match(r"\(x ([+−]) (\d+)\)\(x² ([+−]) (\d*)x ([+−]) (\d+)\)을 전개했을 때, (x²|x)의 계수", q); a = _sv(m.group(1), m.group(2)); b = _sv(m.group(3), m.group(4) or "1"); c = _sv(m.group(5), m.group(6))
            return a + b if m.group(7) == "x²" else a * b + c
        if tid == "h1-1-poly-t2":
            m = re.match(r"다항식 x³ ([+−]) (\d*)x² ([+−]) (\d*)x ([+−]) (\d+)[을를] x ([+−]) (\d+)(?:으로|로) 나누었을 때", q); a = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4) or "1"); c = _sv(m.group(5), m.group(6)); pv = -_sv(m.group(7), m.group(8))
            return pv ** 3 + a * pv * pv + b * pv + c
        if tid == "h1-1-poly-t3":
            m = re.search(r"= (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)[이가] x에 대한 항등식", q); pp = _coef(m.group(1)); qq = _sv(m.group(2), m.group(3) or "1"); r = _sv(m.group(4), m.group(5)); return 4 * pp + 2 * qq + r
        if tid == "h1-1-poly-t4":
            m = re.search(r"x − 1로 나눈 나머지가 (-?\d+), x \+ 1로 나눈 나머지가 (-?\d+)일 때, 상수 a, b에 대하여 (a \+ b|ab)", q); r1, r2 = Fraction(m.group(1)), Fraction(m.group(2)); a = (r1 + r2) / 2; b = (r1 - r2) / 2 - 1
            return a + b if m.group(3) == "a + b" else a * b
        if tid == "h1-1-poly-t5":
            m = re.search(r"x³ \+ ax² \+ bx ([+−]) (\d+)[이가] \(x ([+−]) (\d+)\)\(x ([+−]) (\d+)\)로 나누어떨어질 때", q); c = _sv(m.group(1), m.group(2)); p1 = -_sv(m.group(3), m.group(4)); p2 = -_sv(m.group(5), m.group(6))
            # p1³ + a p1² + b p1 + c = 0, p2³ + a p2² + b p2 + c = 0
            det = p1 * p1 * p2 - p2 * p2 * p1
            a = ((-(p1 ** 3) - c) * p2 - (-(p2 ** 3) - c) * p1) / det; b = (p1 * p1 * (-(p2 ** 3) - c) - p2 * p2 * (-(p1 ** 3) - c)) / det
            return a + b
        m = re.match(r"삼차방정식 x³ ([+−]) (\d*)x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 (가장 큰 근|세 근의 제곱의 합)", q); a = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4) or "1"); c = _sv(m.group(5), m.group(6))
        roots = [x for x in range(-12, 13) if x ** 3 + a * x * x + b * x + c == 0]
        if len(roots) != 3: return None
        return Fraction(max(roots)) if m.group(7) == "가장 큰 근" else Fraction(sum(x * x for x in roots))
    if tid.startswith("h1-1-complex"):
        if tid == "h1-1-complex-t1":
            m = re.match(r"\((-?\d+) ([+−]) (\d*)i\)\((-?\d+) ([+−]) (\d*)i\) = p \+ qi", q); a, b, c, d = Fraction(m.group(1)), _sv(m.group(2), m.group(3) or "1"), Fraction(m.group(4)), _sv(m.group(5), m.group(6) or "1"); return (a * c - b * d) + (a * d + b * c)
        if tid == "h1-1-complex-t2":
            m = re.match(r"\[\[frac\((-?\d+) ([+−]) (\d*)i, (-?\d+) ([+−]) (\d*)i\)\]\] = p \+ qi일 때, 실수 p, q에 대하여 (p \+ q|p|q)의 값", q); a, b, c, d = Fraction(m.group(1)), _sv(m.group(2), m.group(3) or "1"), Fraction(m.group(4)), _sv(m.group(5), m.group(6) or "1")
            n = c * c + d * d; pv, qv = (a * c + b * d) / n, (b * c - a * d) / n; return {"p": pv, "q": qv, "p + q": pv + qv}[m.group(7)]
        if tid == "h1-1-complex-t3":
            m = re.match(r"\(1 \+ i\)\^(\d+)의 값", q)
            if m: n = int(m.group(1)); return Fraction((-4) ** (n // 4)) if n % 4 == 0 else None
            n = int(re.search(r"pow\(frac\(1 \+ i, 1 − i\), (\d+)\)", q).group(1)); return Fraction(2 if n % 4 == 0 else -2) if n % 2 == 0 else Fraction(0)
        if tid == "h1-1-complex-t4":
            m = re.match(r"복소수 \((-?\d+) ([+−]) (\d*)i\)\((-?\d+) \+ xi\)가 (실수|순허수)", q); a, b, c = Fraction(m.group(1)), _sv(m.group(2), m.group(3) or "1"), Fraction(m.group(4))
            return -b * c / a if m.group(5) == "실수" else a * c / b
        m = re.match(r"복소수 z = (-?\d+) ([+−]) (\d*)i에 대하여 (.+?)의 값", q); a, b = Fraction(m.group(1)), _sv(m.group(2), m.group(3) or "1"); ask = m.group(4)
        sm, pr = 2 * a, a * a + b * b
        return sm + pr if "+ z[[conj" in ask else (sm if ask.startswith("z + ") else pr)
    if tid.startswith("h1-1-quad-"):
        if tid == "h1-1-quad-t2":
            m = re.match(r"이차방정식 x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 두 근을 α, β라 할 때, (.+?)의 값", q); b = _sv(m.group(1), m.group(2) or "1"); c = _sv(m.group(3), m.group(4)); s_, pv = -b, c; ask = m.group(5)
            if ask == "α² + β²": return s_ * s_ - 2 * pv
            if ask == "(α − β)²": return s_ * s_ - 4 * pv
            return s_ / pv
        if tid == "h1-1-quad-t3":
            m = re.match(r"이차방정식 x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 두 근을 α, β라 할 때, 두 근이 (.+?)인 이차방정식", q); b = _sv(m.group(1), m.group(2) or "1"); c = _sv(m.group(3), m.group(4)); s_, pv = -b, c; new = m.group(5)
            if new.startswith("α + 1"): ns, npd = s_ + 2, pv + s_ + 1
            elif new.startswith("α − 1"): ns, npd = s_ - 2, pv - s_ + 1
            else: ns, npd = 2 * s_, 4 * pv
            return -ns + npd
        if tid in ("h1-1-quad-t4", "h1-1-quad-t6"):
            m = re.search(r"한 근이 (-?\d+) \+ (\[\[sqrt\((\d+)\)\]\]|(\d+)i)일 때", q); pp = Fraction(m.group(1))
            if m.group(3): qv = Fraction(m.group(3)); return -2 * pp + pp * pp - qv
            qv = Fraction(m.group(4)); return -2 * pp + pp * pp + qv * qv
        if tid == "h1-1-quad-t5":
            m = re.match(r"이차방정식 x² ([+−]) (\d*)x \+ k = 0의 두 근의 차가 (\d+)일 때", q); b = _sv(m.group(1), m.group(2) or "1"); d = Fraction(m.group(3)); s_ = -b; return (s_ * s_ - d * d) / 4
    if tid.startswith("h1-1-quadfn"):
        if tid == "h1-1-quadfn-t2":
            m = re.match(r"직선 y = (-?\d*)x \+ k가 이차함수 y = x² ([+−]) (\d*)x ([+−]) (\d+)의 그래프에 접할 때", q); mm = _coef(m.group(1)); a = _sv(m.group(2), m.group(3) or "1"); b = _sv(m.group(4), m.group(5)); return b - (a - mm) ** 2 / 4
        if tid in ("h1-1-quadfn-t3", "h1-1-quadfn-t4"):
            m = re.match(r"(-?\d+) ≤ x ≤ (-?\d+)에서 이차함수 y = (-?\d*)x² ([+−]) (\d*)x ([+−]) (\d+)의 (최댓값|최솟값)", q); lo, hi = Fraction(m.group(1)), Fraction(m.group(2)); A = _coef(m.group(3)); b = _sv(m.group(4), m.group(5) or "1"); c = _sv(m.group(6), m.group(7))
            f = lambda x: A * x * x + b * x + c; vx = -b / (2 * A); cands = [f(lo), f(hi)] + ([f(vx)] if lo <= vx <= hi else [])
            return max(cands) if m.group(8) == "최댓값" else min(cands)
    if tid.startswith("h1-1-poly-eq"):
        if tid == "h1-1-poly-eq-t1":
            m = re.match(r"삼차방정식 x³ ([+−]) (\d*)x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 세 근을 α, β, γ라 할 때, (.+?)의 값", q); a = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4) or "1"); c = _sv(m.group(5), m.group(6))
            s1, s2, s3 = -a, b, -c; return s1 * s1 - 2 * s2 if m.group(7).startswith("α²") else s2 / s3
        if tid == "h1-1-poly-eq-t2":
            m = re.match(r"사차방정식 x⁴ ([+−]) (\d*)x² ([+−]) (\d+) = 0의 (모든 양의 근의 합|모든 근의 제곱의 합)", q); a = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4))
            ts = [t_ for t_ in range(1, 60) if t_ * t_ + a * t_ + b == 0]
            if len(ts) != 2: return None
            rs = [_isqrt(t_) for t_ in ts]
            if None in rs: return None
            return rs[0] + rs[1] if m.group(5).startswith("모든 양") else 2 * (ts[0] + ts[1])
        if tid == "h1-1-poly-eq-t3":
            m = re.match(r"연립방정식 y = x ([+−]) (\d+), x² \+ y² = (\d+)의 해", q); a = _sv(m.group(1), m.group(2)); b = Fraction(m.group(3))
            xs = [x for x in range(-30, 31) if 2 * x * x + 2 * a * x + a * a - b == 0]
            return max(2 * x + a for x in xs) if len(xs) == 2 else None
        if tid == "h1-1-poly-eq-t4":
            m = re.match(r"삼차방정식 x³ ([+−]) (\d*)x² ([+−]) (\d*)x ([+−]) (\d+) = 0의 세 근을 α, β, γ라 할 때, \(α \+ 1\)", q); a = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4) or "1"); c = _sv(m.group(5), m.group(6)); return 1 - a + b - c
        m = re.match(r"연립방정식 x \+ y = (-?\d+), x² \+ y² = (-?\d+)의 해 \(x, y\)에 대하여 (xy|\(x − y\)²)의 값", q); s_, t_ = Fraction(m.group(1)), Fraction(m.group(2)); pv = (s_ * s_ - t_) / 2
        return pv if m.group(3) == "xy" else s_ * s_ - 4 * pv
    if tid.startswith("h1-1-ineq"):
        if tid == "h1-1-ineq-t1":
            m = re.match(r"연립부등식 (\d+)x ([+−]) (\d+) > (-?\d+), (\d+)x ([+−]) (\d+) ≤ (-?\d+)[을를] 만족시키는 정수", q); k1, c1, r1, k2, c2, r2 = Fraction(m.group(1)), _sv(m.group(2), m.group(3)), Fraction(m.group(4)), Fraction(m.group(5)), _sv(m.group(6), m.group(7)), Fraction(m.group(8))
            lo, hi = (r1 - c1) / k1, (r2 - c2) / k2; return Fraction(sum(1 for x in range(-100, 101) if x > lo and x <= hi))
        if tid == "h1-1-ineq-t2":
            m = re.match(r"부등식 \[\[abs\((\d+)x ([+−]) (\d+)\)\]\] < (\d+)[을를] 만족시키는 정수", q); a, b, c = Fraction(m.group(1)), _sv(m.group(2), m.group(3)), Fraction(m.group(4))
            return Fraction(sum(1 for x in range(-100, 101) if abs(a * x + b) < c))
        if tid == "h1-1-ineq-t4":
            m = re.match(r"이차부등식 x² \+ ax \+ b ≤ 0의 해가 (-?\d+) ≤ x ≤ (-?\d+)일 때", q); pp, qq = Fraction(m.group(1)), Fraction(m.group(2)); return -(pp + qq) + pp * qq
        if tid == "h1-1-ineq-t5":
            m = re.match(r"연립부등식 x² ([+−]) (\d*)x ([+−]) (\d+) < 0, x ≥ (-?\d+)[을를] 만족시키는 정수", q); b = _sv(m.group(1), m.group(2) or "1"); c = _sv(m.group(3), m.group(4)); c2 = Fraction(m.group(5))
            return Fraction(sum(1 for x in range(-100, 101) if x * x + b * x + c < 0 and x >= c2))
    if tid.startswith("h1-1-count"):
        if tid == "h1-1-count-t1":
            m = re.match(r"티셔츠 (\d+)종류, 바지 (\d+)종류, 신발 (\d+)종류", q)
            if m: return Fraction(int(m.group(1)) * int(m.group(2)) * int(m.group(3)))
            m = re.search(r"눈의 수의 합이 (\d+) 또는 (\d+)[이가] 되는", q); return Fraction(sum(1 for i in range(1, 7) for j in range(1, 7) if i + j in (int(m.group(1)), int(m.group(2)))))
        if tid == "h1-1-count-t2":
            m = re.match(r"(\d+)명의 학생 중에서 (\d+)명을 뽑아 일렬로", q); n, r_ = int(m.group(1)), int(m.group(2)); return Fraction(math.perm(n, r_))
        if tid == "h1-1-count-t3":
            m = re.match(r"(\d+)명의 학생을 일렬로 세울 때, (특정 2명이 서로 이웃하도록|특정 2명이 양 끝에 서도록|특정 2명이 서로 이웃하지 않도록)", q); n = int(m.group(1)); k = m.group(2)
            return Fraction(2 * math.factorial(n - 1) if "서로 이웃하도록" in k else 2 * math.factorial(n - 2) if "양 끝" in k else math.factorial(n) - 2 * math.factorial(n - 1))
        if tid == "h1-1-count-t4":
            m = re.match(r"(\d+)명의 학생 중에서 대표 (\d+)명", q)
            if m: return Fraction(math.comb(int(m.group(1)), int(m.group(2))))
            m = re.match(r"남학생 (\d+)명, 여학생 (\d+)명 중에서 남학생 2명과 여학생 1명", q); return Fraction(math.comb(int(m.group(1)), 2) * int(m.group(2)))
        m = re.match(r"(\d+)각형의 대각선", q)
        if m: n = int(m.group(1)); return Fraction(math.comb(n, 2) - n)
        m = re.match(r"원 위의 서로 다른 (\d+)개의 점 중 3개", q)
        if m: return Fraction(math.comb(int(m.group(1)), 3))
        m = re.match(r"(\d+)명 중에서 특정한 한 명을 반드시 포함하여 (\d+)명", q); return Fraction(math.comb(int(m.group(1)) - 1, int(m.group(2)) - 1))
    if tid.startswith("h1-1-matrix"):
        M = re.findall(r"\[\[mat\(2, 2, (.+?)\)\]\]", q)
        if tid == "h1-1-matrix-t1":
            e = [x.strip() for x in M[1].split(",")]; s_, d = Fraction(e[0]), Fraction(e[3]); x, y = (s_ + d) / 2, (s_ - d) / 2
            return x * y if re.search(r"xy의 값", q) else x + y
        A = [Fraction(x.strip()) for x in M[0].split(",")]
        if tid == "h1-1-matrix-t2":
            B = [Fraction(x.strip()) for x in M[1].split(",")]; m = re.search(r"행렬 (-?\d*)A ([+−]) (\d*)B의 (모든 성분의 합|\(1, 2\) 성분)", q); k = _coef(m.group(1)); l = _sv(m.group(2), m.group(3) or "1")
            C = [k * A[i] + l * B[i] for i in range(4)]; return sum(C) if m.group(4).startswith("모든") else C[1]
        if tid == "h1-1-matrix-t3":
            B = [Fraction(x.strip()) for x in M[1].split(",")]
        else:
            B = A
        C = [A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3], A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3]]
        ask = re.search(r"의 (\(1, 1\) 성분|\(2, 1\) 성분|모든 성분의 합)[을를] 구하시오", q).group(1)
        return C[0] if ask.startswith("(1, 1)") else C[2] if ask.startswith("(2, 1)") else sum(C)
    if tid.startswith("h1-2-coord"):
        P = [(Fraction(x), Fraction(y)) for x, y in re.findall(r"\((-?\d+), (-?\d+)\)", q)]
        if tid == "h1-2-coord-t1":
            m = re.search(r"선분 AB를 (\d+) : (\d+)(?:으로|로) 내분", q); mm, nn = Fraction(m.group(1)), Fraction(m.group(2)); (x1, y1), (x2, y2) = P[:2]
            return (mm * x2 + nn * x1) / (mm + nn) + (mm * y2 + nn * y1) / (mm + nn)
        if tid == "h1-2-coord-t2":
            (x1, y1), (x2, y2) = P[:2]; return _isqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if tid == "h1-2-coord-t3":
            m = re.match(r"두 직선 ax ([+−]) (\d*)y [+−] \d+ = 0, (-?\d*)x ([+−]) (\d*)y [+−] \d+ = 0이 서로 (평행|수직)일 때", q); b = _sv(m.group(1), m.group(2) or "1"); p = _coef(m.group(3)); qq = _sv(m.group(4), m.group(5) or "1")
            return b * p / qq if m.group(6) == "평행" else -b * qq / p
        if tid == "h1-2-coord-t4":
            m = re.search(r"직선 (\d+)x \+ (\d+)y ([+−]) (\d+) = 0 사이의 거리", q); A, B, c = Fraction(m.group(1)), Fraction(m.group(2)), _sv(m.group(3), m.group(4)); (x0, y0) = P[0]
            N = _isqrt(A * A + B * B)
            return None if N is None else abs(A * x0 + B * y0 + c) / N
        if tid == "h1-2-coord-t5":
            (x1, y1), (x2, y2) = P[:2]; x3 = Fraction(re.search(r"C\((-?\d+), k\)", q).group(1)); return y1 + (y2 - y1) * (x3 - x1) / (x2 - x1)
    if tid.startswith("h1-2-circle") or tid.startswith("h1-2-transform"):
        def std(s):
            m = re.search(r"\(x ([+−]) (\d+)\)² \+ \(y ([+−]) (\d+)\)² = (\d+)", s)
            return (-_sv(m.group(1), m.group(2)), -_sv(m.group(3), m.group(4)), Fraction(m.group(5))) if m else None
        sym = {"x축": lambda x, y: (x, -y), "y축": lambda x, y: (-x, y), "원점": lambda x, y: (-x, -y), "직선 y = x": lambda x, y: (y, x)}
        if tid == "h1-2-circle-t1":
            m = re.match(r"원 x² \+ y² ([+−]) (\d*)x ([+−]) (\d*)y ([+−]) (\d+) = 0의", q); A = _sv(m.group(1), m.group(2) or "1"); B = _sv(m.group(3), m.group(4) or "1"); C = _sv(m.group(5), m.group(6))
            p, qq = -A / 2, -B / 2; r = _isqrt(p * p + qq * qq - C)
            if r is None: return None
            return p + qq + r if "a + b + r의 값" in q else r
        if tid == "h1-2-circle-t2":
            p, qq, r2 = std(q); r = _isqrt(r2); m = re.search(r"직선 (\d+)x \+ (\d+)y \+ k = 0이 접할", q); A, B = Fraction(m.group(1)), Fraction(m.group(2)); N = _isqrt(A * A + B * B)
            if r is None or N is None: return None
            ks = [v for v in (N * r - A * p - B * qq, -N * r - A * p - B * qq) if v > 0]
            return ks[0] if len(ks) == 1 else None
        if tid == "h1-2-circle-t3":
            m = re.match(r"점 P\((-?\d+), (-?\d+)\)에서", q); px, py = Fraction(m.group(1)), Fraction(m.group(2)); p, qq, r2 = std(q); return _isqrt((px - p) ** 2 + (py - qq) ** 2 - r2)
        if tid == "h1-2-circle-t4":
            m = re.match(r"두 점 A\((-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+)\)를 지름", q); x1, y1, x2, y2 = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]
            p, qq = (x1 + x2) / 2, (y1 + y2) / 2; r2 = ((x2 - x1) ** 2 + (y2 - y1) ** 2) / 4; return -2 * p - 2 * qq + p * p + qq * qq - r2
        if tid == "h1-2-circle-t5":
            m = re.match(r"원 x² \+ y² = (\d+) 위의 점 \((-?\d+), (-?\d+)\)에서의 접선의 (x절편|y절편)", q); r2, x1, y1 = Fraction(m.group(1)), Fraction(m.group(2)), Fraction(m.group(3))
            if x1 * x1 + y1 * y1 != r2: return None
            return r2 / x1 if m.group(4) == "x절편" else r2 / y1
        if tid == "h1-2-transform-t1":
            p, qq, r2 = std(q); m = re.search(r"x축의 방향으로 (-?\d+)만큼, y축의 방향으로 (-?\d+)만큼", q); mm, nn = Fraction(m.group(1)), Fraction(m.group(2)); return (p + mm) ** 2 + (qq + nn) ** 2 - r2
        if tid == "h1-2-transform-t2":
            m = re.match(r"점 \((-?\d+), (-?\d+)\)[을를] (x축|y축|원점|직선 y = x)에 대하여 대칭이동", q); x2, y2 = sym[m.group(3)](Fraction(m.group(1)), Fraction(m.group(2))); return x2 - y2
        if tid == "h1-2-transform-t3":
            m = re.match(r"직선 y = (-?\d*)x ([+−]) (\d+)[을를] (x축|y축|원점|직선 y = x)에 대하여 대칭이동", q); mm = _coef(m.group(1)); nn = _sv(m.group(2), m.group(3)); k = m.group(4)
            a2, b2 = {"x축": (-mm, -nn), "y축": (-mm, nn), "원점": (mm, -nn), "직선 y = x": (1 / mm, -nn / mm)}[k]; return a2 + b2
        if tid == "h1-2-transform-t4":
            p, qq, r2 = std(q); m = re.search(r"x축의 방향으로 (-?\d+)만큼, y축의 방향으로 (-?\d+)만큼 평행이동한 후 (x축|y축|원점|직선 y = x)에 대하여", q)
            x2, y2 = sym[m.group(3)](p + Fraction(m.group(1)), qq + Fraction(m.group(2))); return x2 + y2
    if tid.startswith("h1-2-set") or tid.startswith("h1-2-logic") or tid.startswith("h1-2-func") or tid.startswith("h1-2-ratfn"):
        return _h12b(tid, q)
    if tid.startswith("h2-1-exp") or tid.startswith("h2-1-log"):
        return _h21(tid, q)
    if tid.startswith("h3-3-solid") or tid.startswith("h3-3-conicfig") or tid.startswith("h3-3-vecfig") or tid.startswith("h2-1-trigfig"):
        return _hf(tid, q)
    if tid.startswith("h2-1-trig"):
        return _h21t(tid, q)
    if tid.startswith("h2-1-seq"):
        return _h21s(tid, q)
    if tid.startswith("h2-2-diffapp") or tid.startswith("h2-2-integ"):
        return _h22b(tid, q)
    if tid.startswith("h3-1-"):
        return _h31(tid, q)
    if tid.startswith("h3-2-"):
        return _h32(tid, q)
    if tid.startswith("h3-3-"):
        return _h33(tid, q)
    if tid.startswith("h2-1-induct") or tid.startswith("m3-2-scatter"):
        return _hx(tid, q)
    if tid.startswith("h2-2-lim") or tid.startswith("h2-2-diff"):
        return _h22a(tid, q)
    if tid.startswith("m3-1-sqrt-basic"):
        if tid.startswith("m3-1-sqrt-basic-t1"):
            k = int(re.search(r"\[\[sqrt\((\d+)x\)\]\]", q).group(1)); return Fraction(_sqfree(k)[1])
        if tid.startswith("m3-1-sqrt-basic-t2"):
            m = re.search(r"\[\[sqrt\((\d+) − x\)\]\]가 자연수가 되도록 하는 (자연수 x의 개수|가장 작은 자연수 x의 값)", q); a = int(m.group(1))
            sq = [t * t for t in range(1, a) if t * t < a]; return Fraction(len(sq)) if m.group(2).startswith("자연수 x의 개수") else Fraction(a - max(sq))
        if tid.startswith("m3-1-sqrt-basic-t3"):
            m = re.search(r"\[\[sqrt\((\d+)\)\]\] < n < \[\[sqrt\((\d+)\)\]\]", q); a, b = int(m.group(1)), int(m.group(2)); return Fraction(sum(1 for t in range(1, b) if a < t * t < b))
        if tid.startswith("m3-1-sqrt-basic-t4"):
            m = re.search(r"sqrt\(pow\(-(\d+), 2\)\)\]\] \+ \[\[pow\(-sqrt\((\d+)\), 2\)\]\] − \[\[sqrt\(pow\((\d+), 2\)\)\]\] − \[\[pow\(sqrt\((\d+)\), 2\)\]\]", q); a, b, c, d = [int(m.group(i)) for i in (1, 2, 3, 4)]; return Fraction(a + b - c - d)
        m = re.search(r"(-?\d+) \+ \[\[sqrt\((\d+)\)\]\]의 정수 부분", q); return Fraction(int(m.group(1)) + math.isqrt(int(m.group(2))))
    if tid.startswith("m3-1-sqrt-ops"):
        if tid.startswith("m3-1-sqrt-ops-t1"):
            n = int(re.search(r"\[\[sqrt\((\d+)\)\]\][을를] a", q).group(1)); A, B = _sqfree(n); return Fraction(A + B)
        if tid.startswith("m3-1-sqrt-ops-t2"):
            m = re.search(r"\[\[(\d*)\*?sqrt\((\d+)\)\]\] × \[\[(\d*)\*?sqrt\((\d+)\)\]\] = k", q); p, a, qq, b = _coef(m.group(1)), int(m.group(2)), _coef(m.group(3)), int(m.group(4))
            c, mm = _sqfree(a * b); return p * qq * c + mm
        if tid.startswith("m3-1-sqrt-ops-t3"):
            m = re.search(r"\[\[frac\((\d+), sqrt\((\d+)\)\)\]\]의 분모를 유리화", q); p, n = int(m.group(1)), int(m.group(2)); s_, mm = _sqfree(n)
            f = Fraction(p, s_ * mm); return Fraction(f.numerator + mm + f.denominator)
        if tid.startswith("m3-1-sqrt-ops-t4"):
            m = re.search(r"\[\[sqrt\((\d+)\)\]\] \+ \[\[sqrt\((\d+)\)\]\] − \[\[sqrt\((\d+)\)\]\] = k\[\[sqrt\((\d+)\)\]\]", q); n1, n2, n3, mm = [int(m.group(i)) for i in (1, 2, 3, 4)]
            cs = [_sqfree(n) for n in (n1, n2, n3)]
            if any(c[1] != mm for c in cs): return None
            return Fraction(cs[0][0] + cs[1][0] - cs[2][0])
        m = re.search(r"\[\[sqrt\((\d+)\)\]\]\(\[\[sqrt\((\d+)\)\]\] − \[\[sqrt\((\d+)\)\]\]\) = p \+ q\[\[sqrt\((\d+)\)\]\]", q); a, b, c, mm = [int(m.group(i)) for i in (1, 2, 3, 4)]
        p = _isqrt(a * b); qc, qm = _sqfree(a * c)
        if p is None or qm != mm: return None
        return p - qc
    if tid.startswith("m3-1-mult-formula"):
        if tid == "m3-1-mult-formula-t1":
            m = re.match(r"\((-?\d*)x ([+−]) (\d+)(y?)\)\((-?\d*)x ([+−]) (\d+)(y?)\)의 전개식에서 (x|xy)의 계수", q); a = _coef(m.group(1)); b = Fraction(m.group(3)) * (1 if m.group(2) == "+" else -1); c = _coef(m.group(5)); d = Fraction(m.group(7)) * (1 if m.group(6) == "+" else -1)
            if (m.group(9) == "xy") != (m.group(4) == "y"): return None
            return a * d + b * c
        if tid.startswith("m3-1-mult-formula-t2"):
            A = int(re.search(r"(\d+)²을 계산", q).group(1)); return Fraction(A * A)
        if tid.startswith("m3-1-mult-formula-t3") or tid.startswith("m3-1-mult-formula-t4"):
            m = re.search(r"(\d+) × (\d+)[을를] 계산", q); return Fraction(int(m.group(1)) * int(m.group(2)))
        if tid.startswith("m3-1-mult-formula-t5"):
            m = re.search(r"\[\[pow\((\d*)\*?sqrt\((\d+)\) ([+−]) (\d+), 2\)\]\] = m \+ n\[\[sqrt\((\d+)\)\]\]", q); p, a, qq = _coef(m.group(1)), int(m.group(2)), Fraction(m.group(4)) * (1 if m.group(3) == "+" else -1)
            if int(m.group(5)) != a: return None
            return p * p * a + qq * qq + 2 * p * qq
        if tid.startswith("m3-1-mult-formula-t6"):
            m = re.search(r"\[\[frac\((\d+), (.+?)\)\]\]의 분모를 유리화하여 p \+ q\[\[sqrt\((\d+)\)\]\]", q); c, den, a = int(m.group(1)), m.group(2), int(m.group(3))
            mr = re.fullmatch(r"sqrt\((\d+)\) ([+−]) (\d+)", den); mn = re.fullmatch(r"(\d+) ([+−]) sqrt\((\d+)\)", den)
            if mr:
                if int(mr.group(1)) != a: return None
                b = int(mr.group(3)); sg = 1 if mr.group(2) == "+" else -1; D = a - b * b       # c(√a − s b)/(a − b²)
                return Fraction(-sg * c * b, D) + Fraction(c, D)
            if int(mn.group(3)) != a: return None
            b = int(mn.group(1)); sg = 1 if mn.group(2) == "+" else -1; D = b * b - a            # c(b − s√a)/(b² − a)
            return Fraction(c * b, D) + Fraction(-sg * c, D)
        if tid.startswith("m3-1-mult-formula-t7"):
            m = re.match(r"x ([+−]) y = (-?\d+), xy = (-?\d+)일 때, (x² \+ y²|\(x − y\)²|\(x \+ y\)²)의 값", q); s_, pv = Fraction(m.group(2)), Fraction(m.group(3)); plus = m.group(1) == "+"; ask = m.group(4)
            if ask == "x² + y²": return s_ * s_ - 2 * pv if plus else s_ * s_ + 2 * pv
            if ask == "(x − y)²": return s_ * s_ - 4 * pv if plus else None
            return s_ * s_ + 4 * pv if not plus else None
        if tid.startswith("m3-1-mult-formula-t8"):
            m = re.match(r"x ([+−]) \[\[frac\(1, x\)\]\] = (-?\d+)일 때, (.+?)의 값", q); s_ = Fraction(m.group(2)); plus = m.group(1) == "+"; ask = m.group(3)
            if ask == "x² + [[frac(1, pow(x,2))]]": return s_ * s_ - 2 if plus else s_ * s_ + 2
            if ask == "[[pow(x − frac(1, x), 2)]]": return s_ * s_ - 4 if plus else None
            return s_ * s_ + 4 if (not plus and ask == "[[pow(x + frac(1, x), 2)]]") else None
        if tid.startswith("m3-1-mult-formula-t9"):
            m = re.match(r"x² ([+−]) (\d+)x ([+−]) 1 = 0일 때, x² \+ \[\[frac\(1, pow\(x,2\)\)\]\]", q); s_ = Fraction(m.group(2)); return s_ * s_ - 2 if m.group(3) == "+" else s_ * s_ + 2
        m = re.match(r"x = (\d+) ([+−]) \[\[sqrt\((\d+)\)\]\]일 때, x² − (\d+)x ([+−]) (\d+)의 값", q); c, a, c2 = int(m.group(1)), int(m.group(3)), int(m.group(4)); e = Fraction(m.group(6)) * (1 if m.group(5) == "+" else -1)
        if c2 != 2 * c: return None
        return a - c * c + e
    return "skip"


def _sqfree(n):
    a, b = 1, n
    p = 2
    while p * p <= b:
        while b % (p * p) == 0:
            b //= p * p
            a *= p
        p += 1
    return a, b


def _lin(text):
    """일차식 문자열 → (x의 계수, 상수항) — mathir 로 x = 0, 1 에서 값을 읽는다."""
    import mathir
    node = mathir.parse(text.replace("−", "-"))[0]
    f0 = Fraction(mathir.ev(node, {"x": Fraction(0)})); f1 = Fraction(mathir.ev(node, {"x": Fraction(1)}))
    return f1 - f0, f0


def check_linexpr(it):
    """식이 답인 틀(m1-1-linear-expr-t3·t4·t5): 발문에서 식을 되읽어 답과 계수를 대조. True/False, 해당 없으면 None."""
    tid, q = it["template_id"], it["question"]
    if not tid.startswith(("m1-1-linear-expr-t3", "m1-1-linear-expr-t4", "m1-1-linear-expr-t5")):
        return None
    try:
        if tid.startswith("m1-1-linear-expr-t3"):
            m = re.match(r"어떤 식(?:에서|에) (.+?)[을를] (더해야|빼야) 할 것을 잘못하여 (.+?)[을를] (뺐더니|더했더니) (.+?)[이가] 되었다", q)
            A, B = _lin(m.group(1)), _lin(m.group(5)); i = 1 if m.group(2) == "더해야" else -1
            want = (B[0] + 2 * i * A[0], B[1] + 2 * i * A[1])
        elif tid.startswith("m1-1-linear-expr-t4"):
            m = re.match(r"가로의 길이가 \((.+?)\) cm, 세로의 길이가 \((.+?)\) cm인 직사각형", q); W, H = _lin(m.group(1)), _lin(m.group(2))
            want = (2 * (W[0] + H[0]), 2 * (W[1] + H[1]))
        else:
            m = re.match(r"(.+?)[을를] 간단히 하시오", q); want = _lin(m.group(1))
        return _lin(it["answer"]) == want
    except Exception:                                   # noqa: BLE001
        return False


def check_m3str(it):
    """문자열 답 틀(m3-1): 일차식(x + q)·근 두 개(x = p 또는 x = q)·범위(k < T). True/False, 해당 없으면 None."""
    tid, q, a = it["template_id"], it["question"], it["answer"]
    if tid == "m3-1-factor-t7":
        m = re.match(r"넓이가 x² \+ (\d+)x \+ (\d+)인 직사각형의 가로의 길이가 x \+ (\d+)일 때", q); b, c, pp = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return pp * (b - pp) == c and _lin(a) == (Fraction(1), Fraction(b - pp))
    if tid == "m3-1-quad-solve-t1":
        m = re.match(r"이차방정식 x² ([+−]) (\d*)x ([+−]) (\d+) = 0을 푸시오", q); b = _coef(m.group(2)) * (1 if m.group(1) == "+" else -1); c = Fraction(m.group(4)) * (1 if m.group(3) == "+" else -1)
        roots = sorted(Fraction(x) for x in re.findall(r"x = (-?\d+)", a))
        return len(roots) == 2 and roots[0] + roots[1] == -b and roots[0] * roots[1] == c
    if tid == "m3-1-quad-solve-t7":
        m = re.match(r"이차방정식 (-?\d*)x² ([+−]) (\d*)x \+ k = 0이 (서로 다른 두 근을 가질|근을 갖지 않을|근을 가질) 때", q); A = _coef(m.group(1)); b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1)
        T = b * b / (4 * A); op = {"서로 다른 두 근을 가질": "<", "근을 갖지 않을": ">", "근을 가질": "≤"}[m.group(4)]
        ma = re.fullmatch(r"k ([<>≤]) (-?\d+)", a)
        return bool(ma) and ma.group(1) == op and Fraction(ma.group(2)) == T
    if tid == "m3-1-quad-solve-t8":
        m = re.search(r"x = (-?\d+) 또는 x = (-?\d+)[을를] 얻었고, .+?x = (-?\d+) 또는 x = (-?\d+)[을를] 얻었다", q); pp, qq, u, v = [int(m.group(i)) for i in (1, 2, 3, 4)]
        S, P = pp + qq, u * v; roots = sorted(int(x) for x in re.findall(r"x = (-?\d+)", a))
        return len(roots) == 2 and roots[0] + roots[1] == S and roots[0] * roots[1] == P
    return None


def _mval(text):
    """마커 문자열('[[3*sqrt(3)]]'·'12'·'[[frac(sqrt(3), 2)]]') → float"""
    import mathir
    t = re.sub(r"^\[\[|\]\]$", "", text.strip())
    node, _ = mathir.parse(t)
    return float(mathir.ev(node))


def _sp(f, th):
    return {"sin": math.sin, "cos": math.cos, "tan": math.tan}[f](math.radians(th))


def check_m3trig(it):
    """무리수 답 틀(m3-2 삼각비의 활용): 발문에서 되읽어 float 비교. True/False, 해당 없으면 None."""
    tid, q, a = it["template_id"], it["question"], it["answer"]
    if not tid.startswith("m3-2-trig-apply"):
        return None
    try:
        av = _mval(a)
        if tid == "m3-2-trig-apply-t1":
            m = re.search(r"\[\[angle\(B\)\]\] = \[\[deg\((\d+)\)\]\]인 직각삼각형 ABC에서 \[\[seg\((AB|BC|AC)\)\]\] = (.+?)일 때, \[\[seg\((AB|BC|AC)\)\]\]의 길이", q); th = int(m.group(1)); G, X = m.group(2), m.group(4); gv = _mval(m.group(3))
            unit = {"BC": math.cos(math.radians(th)), "AC": math.sin(math.radians(th)), "AB": 1.0}
            want = gv / unit[G] * unit[X]
        elif tid == "m3-2-trig-apply-t2":
            m = re.search(r"거리가 (\d+) m이고, .+? 올려다본 각의 크기가 (\d+)°", q)
            if m: want = int(m.group(1)) * _sp("tan", int(m.group(2)))
            else:
                m = re.search(r"길이가 (\d+) m인 사다리 .+? 각의 크기가 (\d+)°", q); want = int(m.group(1)) * _sp("sin", int(m.group(2)))
        elif tid == "m3-2-trig-apply-t3":
            m = re.search(r"\[\[seg\(BC\)\]\] = (\d+), \[\[seg\(CA\)\]\] = (\d+), \[\[angle\(C\)\]\] = \[\[deg\((\d+)\)\]\]", q); want = 0.5 * int(m.group(1)) * int(m.group(2)) * _sp("sin", int(m.group(3)))
        elif tid == "m3-2-trig-apply-t4":
            m = re.search(r"\[\[seg\(AB\)\]\] = (.+?), \[\[seg\(BC\)\]\] = (\d+), \[\[angle\(B\)\]\] = \[\[deg\((\d+)\)\]\]", q); c, a_, th = _mval(m.group(1)), int(m.group(2)), int(m.group(3))
            want = math.sqrt(c * c + a_ * a_ - 2 * a_ * c * math.cos(math.radians(th)))
        else:
            m = re.search(r"\[\[seg\(AB\)\]\] = (\d+), \[\[seg\(AD\)\]\] = (\d+), \[\[angle\(A\)\]\] = \[\[deg\((\d+)\)\]\]인 평행사변형", q)
            if m: want = int(m.group(1)) * int(m.group(2)) * _sp("sin", int(m.group(3)))
            else:
                m = re.search(r"두 대각선의 길이가 (\d+), (\d+)이고 두 대각선이 이루는 각의 크기가 (\d+)°", q); want = 0.5 * int(m.group(1)) * int(m.group(2)) * _sp("sin", int(m.group(3)))
        return abs(want - av) < 1e-6
    except Exception:                                   # noqa: BLE001
        return False


def _sv(sign, digits):
    """'−', '3' → −3 (부호 문자 + 절댓값)"""
    return Fraction(digits) * (1 if sign == "+" else -1)


def _sets(q):
    """[[set(…)]] 마커를 원소 목록(문자열)으로."""
    return [[e.strip() for e in m.split(",")] for m in re.findall(r"\[\[set\((.*?)\)\]\]", q)]


def _lin2(s):
    """'-3x − 5' / 'x + 3' / '2x' → (a, b)"""
    m = re.fullmatch(r"(-?\d*)x(?: ([+−]) (\d+))?", s.strip())
    if not m: return None
    return _coef(m.group(1)), (_sv(m.group(2), m.group(3)) if m.group(2) else Fraction(0))


def _h12b(tid, q):
    """h1-2 집합·명제·함수·유리무리함수 — 발문에서 다시 푼다."""
    if tid == "h1-2-set-t1":
        els = _sets(q)[0]; n = len(els); m = re.search(r"\]\]의 (.+?)를 구하시오", q); cond = m.group(1)
        if cond == "부분집합의 개수": return Fraction(2 ** n)
        if cond == "진부분집합의 개수": return Fraction(2 ** n - 1)
        if re.match(r"\S+, \S+[을를] 모두 원소로 갖는", cond): return Fraction(2 ** (n - 2))
        if re.match(r"\S+[은는] 원소로 갖고 \S+[은는] 원소로 갖지 않는", cond): return Fraction(2 ** (n - 2))
        if re.match(r"\S+[을를] 원소로 갖(는|지 않는) 부분집합", cond): return Fraction(2 ** (n - 1))
        return None
    if tid == "h1-2-set-t2":
        m = re.match(r"두 집합 A, B에 대하여 n\(A\) = (\d+), n\(B\) = (\d+), n\(A ([∩∪]) B\) = (\d+)일 때, n\(A ([∩∪−]) B\)의 값", q); a, b, g = Fraction(m.group(1)), Fraction(m.group(2)), Fraction(m.group(4))
        c = g if m.group(3) == "∩" else a + b - g; u = a + b - c
        return {"∪": u, "∩": c, "−": a - c}[m.group(5)]
    if tid == "h1-2-set-t3":
        m = re.match(r"어느 반 학생 (\d+)명 중에서 .+?이 (\d+)명, .+?이 (\d+)명, .+? 모두 좋아하는 학생이 (\d+)명이다\. (.+?)를 구하시오", q); N, a, b, c = [Fraction(m.group(i)) for i in (1, 2, 3, 4)]; ask = m.group(5)
        if "적어도 하나" in ask: return a + b - c
        if "모두 좋아하지 않는" in ask: return N - (a + b - c)
        if "만 좋아하는" in ask: return a - c
        return None
    if tid == "h1-2-set-t4":
        A, B = [{int(e) for e in s} for s in _sets(q)[:2]]; U = set(range(1, 10)); ask = re.search(r"에 대하여 (.+?)의 모든 원소의 합", q).group(1)
        res = {"Aᶜ ∩ B": B - A, "(A ∪ B)ᶜ": U - A - B, "A − B": A - B, "A ∩ Bᶜ": A - B, "(A ∩ B)ᶜ": U - (A & B)}.get(ask)
        return None if res is None else Fraction(sum(res))
    if tid == "h1-2-set-t5":
        m = re.match(r"(\d+)의 양의 약수 전체의 집합을 A, (\d+)의 양의 약수 전체의 집합을 B라 할 때, n\(A ([∩∪−]) B\)", q)
        if m:
            n1, n2 = int(m.group(1)), int(m.group(2)); A = {d for d in range(1, n1 + 1) if n1 % d == 0}; B = {d for d in range(1, n2 + 1) if n2 % d == 0}
        else:
            m = re.match(r"(\d+) 이하의 자연수 중 (\d+)의 배수 전체의 집합을 A, (\d+)의 배수 전체의 집합을 B라 할 때, n\(A ([∩∪−]) B\)", q); lim, p, r_ = int(m.group(1)), int(m.group(2)), int(m.group(3))
            A = {x for x in range(1, lim + 1) if x % p == 0}; B = {x for x in range(1, lim + 1) if x % r_ == 0}
        op = m.group(m.lastindex); return Fraction(len({"∩": A & B, "∪": A | B, "−": A - B}[op]))
    if tid == "h1-2-logic-t1":
        m = re.match(r"(\d+) 이하의 자연수 전체의 집합 U에서 조건 p: '(.+?)'의 진리집합을 P라 할 때, (P|Pᶜ)의 (모든 원소의 합|원소의 개수)[을를] 구하시오", q); N = int(m.group(1)); cond = m.group(2); U = list(range(1, N + 1))
        mq = re.fullmatch(r"x² − (\d+)x \+ (\d+) = 0", cond); md = re.fullmatch(r"x는 (\d+)의 약수이다", cond); ma = re.fullmatch(r"\[\[abs\(x − (\d+)\)\]\] ≤ (\d+)", cond)
        if mq: s_, p_ = int(mq.group(1)), int(mq.group(2)); P = [x for x in U if x * x - s_ * x + p_ == 0]
        elif md: k = int(md.group(1)); P = [x for x in U if k % x == 0]
        elif ma: c, w = int(ma.group(1)), int(ma.group(2)); P = [x for x in U if abs(x - c) <= w]
        else: return None
        S = P if m.group(3) == "P" else [x for x in U if x not in P]
        return Fraction(sum(S) if m.group(4).startswith("모든") else len(S))
    if tid == "h1-2-logic-t2":
        m = re.match(r"명제 '(모든|어떤) 실수 x에 대하여 x² ([+−]) (2?)kx \+ (\d+) (>|≥|<) 0이다\.'가 참이 되도록 하는 (정수 k의 개수|자연수 k의 최솟값)", q); c = int(m.group(4)); two = m.group(3) == "2"
        if m.group(1) == "모든":
            if m.group(5) == ">": return Fraction(sum(1 for k in range(-400, 401) if (k * k < c if two else k * k < 4 * c)))
            return Fraction(sum(1 for k in range(-400, 401) if k * k <= c))
        return Fraction(next(k for k in range(1, 400) if (k * k > c if two else k * k > 4 * c)))
    if tid == "h1-2-logic-t3":
        m = re.match(r"실수 x에 대한 두 조건 p: \[\[abs\(x ([+−]) (\d+)\)\]\] ≤ k, q: (-?\d+) ≤ x ≤ (-?\d+)에 대하여 p가 q이기 위한 (충분|필요)조건", q); a = -_sv(m.group(1), m.group(2)); lo, hi = Fraction(m.group(3)), Fraction(m.group(4))
        d1, d2 = a - lo, hi - a
        return min(d1, d2) if m.group(5) == "충분" else max(d1, d2)
    if tid == "h1-2-logic-t4":
        m = re.match(r"x > (\d+)일 때, (.+?)의 최솟값", q); p = int(m.group(1)); e = m.group(2)
        m1 = re.fullmatch(r"(\d*)x \+ \[\[frac\((\d+), x\)\]\]", e); m2 = re.fullmatch(r"x \+ \[\[frac\((\d+), x − (\d+)\)\]\]", e); m3 = re.fullmatch(r"\[\[frac\(\(x \+ (\d+)\)\(x \+ (\d+)\), x\)\]\]", e)
        if m1: A, B = int(m1.group(1) or "1"), int(m1.group(2)); r = _isqrt(A * B); return None if r is None else 2 * r
        if m2: B, pp = int(m2.group(1)), int(m2.group(2)); r = _isqrt(B); return None if r is None or pp != p else pp + 2 * r
        if m3: a, b = int(m3.group(1)), int(m3.group(2)); r = _isqrt(a * b); return None if r is None else a + b + 2 * r
        return None
    if tid == "h1-2-logic-t5":
        m = re.match(r"x > 0, y > 0이고 (.+?)일 때, (.+?)의 (최솟값|최댓값)", q); cond, ask = m.group(1), m.group(2)
        mc = re.fullmatch(r"xy = (\d+)", cond)
        if mc:
            c = int(mc.group(1)); ma = re.fullmatch(r"(\d*)x \+ (\d*)y", ask); A, B = int(ma.group(1) or "1"), int(ma.group(2) or "1"); r = _isqrt(A * B * c); return None if r is None else 2 * r
        ms = re.fullmatch(r"(\d*)x \+ (\d*)y = (\d+)", cond)
        if ms and ask == "xy":
            A, B, s_ = int(ms.group(1) or "1"), int(ms.group(2) or "1"), int(ms.group(3)); return Fraction(s_ * s_, 4 * A * B)
        mh = re.fullmatch(r"\[\[frac\((\d+), x\)\]\] \+ \[\[frac\((\d+), y\)\]\] = 1", cond)
        if mh and ask == "x + y":
            ra, rb = _isqrt(int(mh.group(1))), _isqrt(int(mh.group(2))); return None if ra is None or rb is None else (ra + rb) ** 2
        return None
    if tid == "h1-2-func-t1":
        m = re.match(r"함수 f\(x\) = ax \+ b에 대하여 f\((-?\d+)\) = (-?\d+), f\((-?\d+)\) = (-?\d+)일 때, f\((-?\d+)\)의 값", q); x1, v1, x2, v2, x3 = [Fraction(m.group(i)) for i in (1, 2, 3, 4, 5)]
        a = (v2 - v1) / (x2 - x1); b = v1 - a * x1; return a * x3 + b
    if tid == "h1-2-func-t2":
        m = re.match(r"두 함수 f\(x\) = (.+?), g\(x\) = x² ([+−]) (\d+)에 대하여 \((f∘g|g∘f|f∘f)\)\((-?\d+)\)의 값", q); a, b = _lin2(m.group(1)); c = _sv(m.group(2), m.group(3)); k = Fraction(m.group(5))
        f = lambda x: a * x + b; g = lambda x: x * x + c  # noqa: E731
        return {"f∘g": f(g(k)), "g∘f": g(f(k)), "f∘f": f(f(k))}[m.group(4)]
    if tid == "h1-2-func-t3":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 f⁻¹\((-?\d+)\)의 값", q); a, b = _lin2(m.group(1)); k = Fraction(m.group(2)); return (k - b) / a
    if tid == "h1-2-func-t4":
        m = re.match(r"두 함수 f\(x\) = (.+?), g\(x\) = x ([+−]) (\d+)에 대하여 \((f∘g|g∘f)\)⁻¹\((-?\d+)\)의 값", q); a, b = _lin2(m.group(1)); c = _sv(m.group(2), m.group(3)); k = Fraction(m.group(5))
        return (k - b) / a - c if m.group(4) == "f∘g" else (k - b - c) / a
    if tid == "h1-2-func-t5":
        X, Y = _sets(q)[:2]; m_, n_ = len(X), len(Y); kind = re.search(r"에 대하여 X에서 (X|Y)로의 (.+?)의 개수", q).group(2)
        return Fraction({"함수": n_ ** m_, "상수함수": n_, "일대일함수": math.perm(n_, m_) if n_ >= m_ else 0, "일대일대응": math.factorial(m_) if n_ == m_ else 0}[kind])
    if tid == "h1-2-ratfn-t1":
        m = re.match(r"함수 y = \[\[frac\((.+?), x ([+−]) (\d+)\)\]\]의 그래프의 두 점근선의 교점의 좌표를 \(p, q\)라 할 때, (p \+ q|pq)의 값", q); a, b = _lin2(m.group(1)); c = _sv(m.group(2), m.group(3))
        p, qq = -c, a; return p + qq if m.group(4) == "p + q" else p * qq
    if tid == "h1-2-ratfn-t2":
        m = re.match(r"함수 y = \[\[frac\((-?\d+), x\)\]\]의 그래프를 x축의 방향으로 (-?\d+)만큼, y축의 방향으로 (-?\d+)만큼 평행이동", q); k, mm, nn = [Fraction(m.group(i)) for i in (1, 2, 3)]
        return nn + (k - mm * nn) - mm
    if tid == "h1-2-ratfn-t3":
        m = re.match(r"함수 y = \[\[frac\((.+?), x ([+−]) (\d+)\)\]\]의 그래프는 함수 y = \[\[frac\(k, x\)\]\]", q); a, b = _lin2(m.group(1)); c = _sv(m.group(2), m.group(3))
        return (b - a * c) + (-c) + a
    if tid == "h1-2-ratfn-t4":
        m = re.match(r"함수 y = \[\[sqrt\((.+?)\)\]\] ([+−]) (\d+)의 정의역이 \[\[setb\(x, x ([≥≤]) p\)\]\]", q); a, b = _lin2(m.group(1)); c = _sv(m.group(2), m.group(3))
        if (a > 0) != (m.group(4) == "≥"): return None
        return -b / a + c
    if tid == "h1-2-ratfn-t5":
        m = re.match(r"함수 y = \[\[sqrt\((-?\d*)x\)\]\]의 그래프를 x축의 방향으로 (-?\d+)만큼, y축의 방향으로 (-?\d+)만큼 평행이동", q); a = _coef(m.group(1)); mm, nn = Fraction(m.group(2)), Fraction(m.group(3))
        return -a * mm + nn
    return None


def _mk(src):
    """마커 안 식(pow/root/sqrt/frac/log/정수·소수)을 정확한 값으로 — 유리수면 Fraction, 아니면 float. 실패 시 None."""
    src = src.strip()
    if src.startswith("[[") and src.endswith("]]"):
        src = src[2:-2].strip()
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", src)
    if m:
        return Fraction(src)
    if src.startswith("-"):
        v = _mk(src[1:]); return None if v is None else -v
    m = re.fullmatch(r"(\w+)\((.*)\)", src)
    if not m:
        return None
    fn, inner = m.group(1), m.group(2)
    args, depth, cur = [], 0, ""
    for ch in inner:
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == "," and depth == 0:
            args.append(cur); cur = ""
        else:
            cur += ch
    args.append(cur)
    vs = [_mk(a) for a in args]
    if any(v is None for v in vs):
        return None
    if fn == "frac" and len(vs) == 2: return Fraction(vs[0]) / Fraction(vs[1]) if all(isinstance(v, Fraction) for v in vs) else vs[0] / vs[1]
    if fn == "pow" and len(vs) == 2:
        mr = re.fullmatch(r"root\((\d+), (-?\d+)\)", args[0].strip())
        if mr and isinstance(vs[1], Fraction) and vs[1].denominator == 1:      # (ⁿ√v)ᵏ = ⁿ√(vᵏ) 을 정확히
            return _rootf(Fraction(int(mr.group(2))) ** int(vs[1]), int(mr.group(1)))
        b, e = vs
        if isinstance(b, Fraction) and isinstance(e, Fraction):
            if e.denominator == 1: return b ** int(e)
            r = _rootf(b, e.denominator); return None if r is None else r ** e.numerator
        return float(b) ** float(e)
    if fn == "sqrt" and len(vs) == 1: return _rootf(vs[0], 2) if isinstance(vs[0], Fraction) else math.sqrt(vs[0])
    if fn == "root" and len(vs) == 2: return _rootf(vs[1], int(vs[0])) if isinstance(vs[1], Fraction) else vs[1] ** (1 / float(vs[0]))
    if fn == "log":
        if len(vs) == 1: return _ratf(math.log10(float(vs[0])))
        return _ratf(math.log(float(vs[1])) / math.log(float(vs[0])))
    return None


def _rootf(v, n):
    """v의 n제곱근 — 유리수로 떨어지면 Fraction, 아니면 float(음수 밑은 홀수 n만)."""
    v = Fraction(v)
    if v < 0:
        if n % 2 == 0: return None
        r = _rootf(-v, n); return None if r is None else -r
    for num in range(0, 3000):
        if num ** n == v.numerator:
            for den in range(1, 3000):
                if den ** n == v.denominator:
                    return Fraction(num, den)
            break
    return float(v) ** (1 / n)


def _ratf(x):
    f = Fraction(x).limit_denominator(1000)
    return f if abs(float(f) - x) < 1e-9 else x


def _h21(tid, q):
    """h2-1 지수·로그 — 발문에서 다시 푼다."""
    if tid == "h2-1-exp-t1":
        m = re.match(r"(.+?) = \[\[pow\((\d+), k\)\]\]일 때", q); base = int(m.group(2)); lhs = m.group(1)
        parts = re.split(r" ([×÷]) ", lhs); val = _mk(parts[0])
        for op, t in zip(parts[1::2], parts[2::2]):
            v = _mk(t); val = val * v if op == "×" else val / v
        return _ratf(math.log(float(val)) / math.log(base))
    if tid == "h2-1-exp-t2":
        m = re.match(r"(\[\[.+?\]\]) ([×÷+−]) (\[\[.+?\]\])의 값", q); a, b = _mk(m.group(1)), _mk(m.group(3)); op = m.group(2)
        v = {"×": a * b, "÷": a / b, "+": a + b, "−": a - b}[op]
        return v if isinstance(v, Fraction) else _ratf(float(v))
    if tid == "h2-1-exp-t3":
        m = re.match(r"함수 y = \[\[pow\((\d+), x − m\)\]\] ([+−]) (\d+)의 그래프가 점 \((-?\d+), (-?\d+)\)를 지날 때", q); a = int(m.group(1)); n = _sv(m.group(2), m.group(3)); p, qq = Fraction(m.group(4)), Fraction(m.group(5))
        e = _ratf(math.log(float(qq - n)) / math.log(a)); return p - e
    if tid == "h2-1-exp-t4":
        m = re.match(r"(-?\d+) ≤ x ≤ (-?\d+)에서 함수 y = \[\[pow\((.+?), x\)\]\] ([+−]) (\d+)의 최댓값을 M, 최솟값을 m이라 할 때, (M \+ m|M − m)의 값", q); lo, hi = int(m.group(1)), int(m.group(2)); base = _mk(m.group(3)); k = _sv(m.group(4), m.group(5))
        vs = [base ** x + k for x in range(lo, hi + 1)]; M, mm = max(vs), min(vs)
        return M + mm if m.group(6) == "M + m" else M - mm
    if tid == "h2-1-exp-t5":
        m = re.match(r"방정식 (.+?)의 (해|모든 해의 합|모든 해의 곱)[을를] 구하시오", q); e, ask = m.group(1), m.group(2)
        mq = re.fullmatch(r"\[\[pow\((\d+), x\)\]\] − (\d+) × \[\[pow\((\d+), x\)\]\] \+ (\d+) = 0", e)
        if mq:
            sq, s_, b, p_ = [int(mq.group(i)) for i in (1, 2, 3, 4)]
            if sq != b * b: return None
            ts = [t for t in range(1, 2000) if t * t - s_ * t + p_ == 0]; xs = [_ratf(math.log(t) / math.log(b)) for t in ts]
            if len(xs) != 2: return None
            return sum(xs) if ask.endswith("합") else xs[0] * xs[1]
        me = re.fullmatch(r"\[\[pow\((\d+), x(?: ([+−]) (\d+))?\)\]\] = \[\[pow\((\d+), x(?: ([+−]) (\d+))?\)\]\]", e)
        if me:
            A, B = int(me.group(1)), int(me.group(4)); u = _sv(me.group(2), me.group(3)) if me.group(2) else Fraction(0); v = _sv(me.group(5), me.group(6)) if me.group(5) else Fraction(0)
            def _ie(x, b):
                r = _ratf(math.log(x) / math.log(b)); return isinstance(r, Fraction) and r.denominator == 1
            base = next((b for b in (2, 3, 5, 7) if _ie(A, b) and _ie(B, b)), None)
            if base is None: return None
            p_, q_ = _ratf(math.log(A) / math.log(base)), _ratf(math.log(B) / math.log(base))
            return (q_ * v - p_ * u) / (p_ - q_)
        return None
    if tid == "h2-1-exp-t6":
        m = re.match(r"부등식 (.+?)[을를] 만족시키는 (자연수|정수) x의 개수를 구하시오", q); e, kind = m.group(1), m.group(2)
        ma = re.fullmatch(r"\[\[pow\((\d+), x(?: − (\d+))?\)\]\] (≤|<) (\d+)", e)
        if ma:
            a, c, rhs = int(ma.group(1)), int(ma.group(2) or 0), int(ma.group(4)); ee = _ratf(math.log(rhs) / math.log(a))
            return Fraction(sum(1 for x in range(1, 200) if (x - c <= ee if ma.group(3) == "≤" else x - c < ee)))
        mh = re.fullmatch(r"\[\[pow\(frac\(1,(\d+)\), x(?: − (\d+))?\)\]\] ≥ \[\[frac\(1, (\d+)\)\]\]", e)
        if mh:
            a, c, rhs = int(mh.group(1)), int(mh.group(2) or 0), int(mh.group(3)); ee = _ratf(math.log(rhs) / math.log(a))
            return Fraction(sum(1 for x in range(1, 200) if x - c <= ee))
        mq = re.fullmatch(r"\[\[pow\((\d+), x\)\]\] − (\d+) × \[\[pow\((\d+), x\)\]\] \+ (\d+) (≤|<) 0", e)
        if mq:
            sq, s_, b, p_ = [int(mq.group(i)) for i in (1, 2, 3, 4)]; op = mq.group(5)
            return Fraction(sum(1 for x in range(-10, 30) if (((b ** x) ** 2 - s_ * b ** x + p_) <= 0 if op == "≤" else ((b ** x) ** 2 - s_ * b ** x + p_) < 0)))
        return None
    if tid == "h2-1-log-t1":
        m = re.match(r"(\[\[.+?\]\]) ([+−]) (\[\[.+?\]\])의 값", q); a, b = _mk(m.group(1)), _mk(m.group(3)); return a + b if m.group(2) == "+" else a - b
    if tid == "h2-1-log-t2":
        m = re.match(r"(\[\[.+?\]\]) ([+−×]) (\[\[.+?\]\])의 값", q); a, b = _mk(m.group(1)), _mk(m.group(3)); op = m.group(2)
        v = a + b if op == "+" else a - b if op == "−" else a * b
        return _ratf(float(v)) if not isinstance(v, Fraction) else v
    if tid == "h2-1-log-t3":
        L2, L3 = Fraction("0.3010"), Fraction("0.4771"); L5 = 1 - L2
        mv = re.search(r"log (\d+)의 값을 구하시오", q)
        if mv:
            N = int(mv.group(1)); p = q_ = r = 0
            while N % 2 == 0: N //= 2; p += 1
            while N % 3 == 0: N //= 3; q_ += 1
            while N % 5 == 0: N //= 5; r += 1
            return None if N != 1 else p * L2 + q_ * L3 + r * L5
        md = re.search(r"\[\[pow\((.+?), (\d+)\)\]\][은는이가]? ?몇 자리의 자연수", q)
        if md:
            base, n = md.group(1), int(md.group(2)); L = {"2": L2, "3": L3, "6": L2 + L3, "12": 2 * L2 + L3, "15": L3 + L5}.get(base)
            return None if L is None else Fraction(math.floor(n * L) + 1)
        ms = re.search(r"\[\[pow\((.+?), (\d+)\)\]\]을 소수로 나타낼 때", q)
        if ms:
            base, n = ms.group(1), int(ms.group(2)); L = {"frac(1,2)": -L2, "0.3": L3 - 1, "frac(1,3)": -L3}.get(base)
            return None if L is None else Fraction(-math.floor(n * L))
        return None
    if tid == "h2-1-log-t4":
        m = re.match(r"함수 y = \[\[log\((\d+), x ([+−]) (\d+)\)\]\] \+ n의 그래프가 점 \((-?\d+), (-?\d+)\)를 지날 때", q); a = int(m.group(1)); mm = -_sv(m.group(2), m.group(3)); p, qq = Fraction(m.group(4)), Fraction(m.group(5))
        return qq - _ratf(math.log(float(p - mm)) / math.log(a))
    if tid == "h2-1-log-t5":
        m = re.match(r"방정식 (.+?)의 (해|모든 해의 합|모든 해의 곱)[을를] 구하시오", q); e, ask = m.group(1), m.group(2)
        ma = re.fullmatch(r"\[\[log\((\d+), x(?: − (\d+))?\)\]\] \+ \[\[log\((\d+), x \+ (\d+)\)\]\] = (\d+)", e)
        if ma:
            a, p, qv, ee = int(ma.group(1)), int(ma.group(2) or 0), int(ma.group(4)), int(ma.group(5)); xs = [x for x in range(p + 1, 500) if (x - p) * (x + qv) == a ** ee]
            return Fraction(xs[0]) if len(xs) == 1 else None
        mt = re.fullmatch(r"\[\[pow\(log\((\d+), x\), 2\)\]\] − (\d+)\[\[log\((\d+), x\)\]\](?: \+ (\d+))? = 0", e)
        if mt:
            a, s_, pr = int(mt.group(1)), int(mt.group(2)), int(mt.group(4) or 0); ts = [t for t in range(0, 50) if t * t - s_ * t + pr == 0]
            if len(ts) != 2: return None
            return Fraction(a ** ts[0] * a ** ts[1]) if ask.endswith("곱") else Fraction(a ** ts[0] + a ** ts[1])
        mb = re.fullmatch(r"\[\[log\((\d+), x\)\]\] = \[\[log\((\d+), x \+ (\d+)\)\]\]", e)
        if mb:
            a, sq, c = int(mb.group(1)), int(mb.group(2)), int(mb.group(3))
            if sq != a * a: return None
            xs = [x for x in range(1, 500) if x * x == x + c]; return Fraction(xs[0]) if len(xs) == 1 else None
        return None
    if tid == "h2-1-log-t6":
        m = re.match(r"부등식 (.+?)[을를] 만족시키는 (자연수 x의 개수|정수 x의 최댓값|정수 x의 최솟값|정수 x의 개수)[을를] 구하시오", q); e, ask = m.group(1), m.group(2)
        def pick(xs):
            if not xs: return None
            return Fraction(len(xs)) if ask.endswith("개수") else Fraction(max(xs)) if ask.endswith("최댓값") else Fraction(min(xs))
        ma = re.fullmatch(r"\[\[log\((\d+), x(?: − (\d+))?\)\]\] ≤ (\d+)", e)
        if ma:
            a, p, ee = int(ma.group(1)), int(ma.group(2) or 0), int(ma.group(3)); return pick([x for x in range(1, 2000) if x - p > 0 and x - p <= a ** ee])
        mh = re.fullmatch(r"\[\[log\(frac\(1,(\d+)\), x(?: − (\d+))?\)\]\] ≥ −(\d+)", e)
        if mh:
            a, p, ee = int(mh.group(1)), int(mh.group(2) or 0), int(mh.group(3)); return pick([x for x in range(1, 2000) if x - p > 0 and x - p <= a ** ee])
        mt = re.fullmatch(r"\[\[pow\(log\((\d+), x\), 2\)\]\] − (\d+)\[\[log\((\d+), x\)\]\](?: \+ (\d+))? ≤ 0", e)
        if mt:
            a, s_, pr = int(mt.group(1)), int(mt.group(2)), int(mt.group(4) or 0); ts = sorted(t for t in range(0, 50) if t * t - s_ * t + pr == 0)
            if len(ts) != 2: return None
            return pick([x for x in range(1, 5000) if a ** ts[0] <= x <= a ** ts[1]])
        mc = re.fullmatch(r"\[\[log\((\d+), x(?: − (\d+))?\)\]\] ≤ \[\[log\((\d+), 2x − (\d+)\)\]\]", e)
        if mc:
            p, r_ = int(mc.group(2) or 0), int(mc.group(4)); return pick([x for x in range(-50, 200) if x - p > 0 and 2 * x - r_ > 0 and x - p <= 2 * x - r_][:1])
        return None
    return None


def _angv(src):
    """deg(150) / frac(5pi, 6) / pi / 2pi / 0 → 라디안(float)"""
    src = src.strip()
    m = re.fullmatch(r"deg\((-?\d+)\)", src)
    if m: return math.radians(int(m.group(1)))
    m = re.fullmatch(r"frac\((\d*)pi, (\d+)\)", src)
    if m: return math.pi * int(m.group(1) or "1") / int(m.group(2))
    m = re.fullmatch(r"(\d*)pi", src)
    if m: return math.pi * int(m.group(1) or "1")
    if src == "0": return 0.0
    return None


def _h21t(tid, q):
    """h2-1 삼각함수 — 발문에서 다시 푼다."""
    if tid == "h2-1-trig-t1":
        m = re.match(r"(\d+)°를 호도법으로", q)
        if m: f = Fraction(int(m.group(1)), 180); return Fraction(f.numerator + f.denominator)
        m = re.match(r"\[\[(.+?)\]\][을를] 육십분법으로", q); v = _angv(m.group(1)); return None if v is None else _ratf(math.degrees(v))
    if tid == "h2-1-trig-t2":
        m = re.match(r"반지름의 길이가 (\d+), 중심각의 크기가 \[\[(.+?)\]\]인 부채꼴의 (호의 길이|넓이)", q); r = int(m.group(1)); th = _angv(m.group(2)) / math.pi
        return _ratf(r * th) if m.group(3) == "호의 길이" else _ratf(r * r * th / 2)
    if tid == "h2-1-trig-t3":
        expr = q.split("의 값")[0]; parts = re.split(r" ([+−]) ", expr); total = None
        for i, part in enumerate([parts[0]] + parts[2::2]):
            mm = re.fullmatch(r"\[\[(sin|cos|tan)\((.+)\)\]\]", part); ang = _angv(mm.group(2)); fv = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[mm.group(1)](ang)
            v = Fraction(round(fv * 2)) / 2 if abs(fv * 2 - round(fv * 2)) < 1e-9 else None
            if v is None: return None
            total = v if i == 0 else (total + v if parts[2 * i - 1] == "+" else total - v)
        return total
    if tid == "h2-1-trig-t4":
        m = re.match(r"sin θ ([+−]) cos θ = (\[\[.+?\]\]|-?\d+)일 때, (sin θ cos θ|sin³θ \+ cos³θ)의 값", q)
        if m:
            sv = _mk(m.group(2)); p = (sv * sv - 1) / 2 if m.group(1) == "+" else (1 - sv * sv) / 2
            return p if m.group(3) == "sin θ cos θ" else sv ** 3 - 3 * sv * p
        m = re.match(r"θ가 제(\d)사분면의 각이고 (sin|cos) θ = (\[\[.+?\]\]|-?\d+)일 때, (sin|cos|tan) θ의 값", q); Q = int(m.group(1)); gv = _mk(m.group(3)); given, ask = m.group(2), m.group(4)
        o2 = 1 - gv * gv; r = _isqrt(o2.numerator); rd = _isqrt(o2.denominator)
        if r is None or rd is None: return None
        ov = Fraction(r, rd) * (1 if (Q in (1, 2) if given == "cos" else Q in (1, 4)) else -1)   # 나머지 값의 부호: given이 cos이면 sin의 부호(1·2), sin이면 cos의 부호(1·4)
        sinv, cosv = (gv, ov) if given == "sin" else (ov, gv)
        return {"sin": sinv, "cos": cosv, "tan": sinv / cosv}[ask]
    if tid == "h2-1-trig-t5":
        m = re.match(r"주기가 (.+?)이고 최댓값이 (-?\d+), 최솟값이 (-?\d+)인 함수 y = a (sin|cos) bx \+ c에 대하여 (a \+ b \+ c|abc)의 값", q); per = m.group(1); M, mm = int(m.group(2)), int(m.group(3))
        pv = _angv(per[2:-2]) if per.startswith("[[") else _angv(per.replace("π", "pi")); b = _ratf(2 * math.pi / pv); a = Fraction(M - mm, 2); c = Fraction(M + mm, 2)
        return a + b + c if m.group(5) == "a + b + c" else a * b * c
    if tid == "h2-1-trig-t6":
        m = re.match(r"삼각형 ABC에서 b = (\d+), c = (\d+), A = \[\[deg\((\d+)\)\]\]일 때, (a의 값|삼각형 ABC의 넓이)", q)
        if m:
            b, c, A = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if m.group(4) == "a의 값": return _isqrt(b * b + c * c - 2 * b * c * Fraction(round(math.cos(math.radians(A)) * 2), 2))
            return Fraction(b * c, 2) * Fraction(round(math.sin(math.radians(A)) * 2), 2)
        m = re.match(r"삼각형 ABC에서 a = (\d+), b = (\d+), c = (\d+)일 때, cos A의 값", q); a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3)); return Fraction(b * b + c * c - a * a, 2 * b * c)
    if tid == "h2-1-trig-t7":
        m = re.match(r"삼각형 ABC에서 sin A : sin B : sin C = (\d+) : (\d+) : (\d+)일 때, 각 C의 크기", q); x, y, z = int(m.group(1)), int(m.group(2)), int(m.group(3))
        cv = (x * x + y * y - z * z) / (2 * x * y); return _ratf(math.degrees(math.acos(cv)))
    return None


_SUBD = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def _sumk(expr, n):
    """∑ 안의 식(문자 k) 을 k = 1..n 에서 더한다 — pow/frac/sqrt 마커 문법을 파이썬 식으로."""
    e = expr.replace("−", "-").replace("×", "*")
    e = re.sub(r"pow\(([^,]+), ([^)]+)\)", r"((\1)**(\2))", e)
    e = re.sub(r"frac\(", "_frac(", e); e = re.sub(r"sqrt\(", "_sqrt(", e)
    e = re.sub(r"(\d)(k|\()", r"\1*\2", e); e = re.sub(r"(k|\))\(", r"\1*(", e); e = re.sub(r"\)k", ")*k", e)
    total, fl = Fraction(0), False
    for k in range(1, n + 1):
        v = eval(e, {"__builtins__": {}}, {"k": Fraction(k), "_frac": lambda a, b: a / b, "_sqrt": lambda x: _rootf(x, 2)})  # noqa: S307
        if isinstance(v, Fraction): total += v
        else: total = float(total) + v; fl = True
    return _ratf(float(total)) if fl else total


def _h21s(tid, q):
    """h2-1 수열 — 발문에서 다시 푼다."""
    if tid == "h2-1-seq-t1":
        m = re.match(r"등차수열 \{aₙ\}에 대하여 a([₀-₉]+) = (-?\d+), a([₀-₉]+) = (-?\d+)일 때, a([₀-₉]+)의 값", q); p, u, qn, v, r = int(m.group(1).translate(_SUBD)), Fraction(m.group(2)), int(m.group(3).translate(_SUBD)), Fraction(m.group(4)), int(m.group(5).translate(_SUBD))
        d = (v - u) / (qn - p); return u + (r - p) * d
    if tid == "h2-1-seq-t2":
        m = re.match(r"첫째항이 (-?\d+), 공차가 (-?\d+)인 등차수열 \{aₙ\}의 첫째항부터 제(\d+)항까지의 합", q); a, d, n = [Fraction(m.group(i)) for i in (1, 2, 3)]; return n * (2 * a + (n - 1) * d) / 2
    if tid == "h2-1-seq-t3":
        m = re.match(r"등비수열 \{aₙ\}에 대하여 a([₀-₉]+) = (-?\d+), a([₀-₉]+) = (-?\d+)일 때, a([₀-₉]+)의 값", q); p, u, qn, v, s_ = int(m.group(1).translate(_SUBD)), Fraction(m.group(2)), int(m.group(3).translate(_SUBD)), Fraction(m.group(4)), int(m.group(5).translate(_SUBD))
        rs = [r for r in (2, 3, -2, -3, Fraction(1, 2), Fraction(-1, 2)) if u * r ** (qn - p) == v]
        return u * rs[0] ** (s_ - p) if len(rs) == 1 else None
    if tid == "h2-1-seq-t4":
        m = re.match(r"첫째항이 (-?\d+), 공비가 (\[\[.+?\]\]|-?\d+)인 등비수열의 첫째항부터 제(\d+)항까지의 합", q); a = Fraction(m.group(1)); r = _mk(m.group(2)); n = int(m.group(3)); return a * (r ** n - 1) / (r - 1)
    if tid == "h2-1-seq-t5" or tid == "h2-1-seq-t7":
        m = re.match(r"\[\[sum\(k, 1, (\d+), (.+)\)\]\]의 값", q); return _sumk(m.group(2), int(m.group(1)))
    if tid == "h2-1-seq-t6":
        m = re.match(r"수열 \{aₙ\}의 첫째항부터 제n항까지의 합 Sₙ이 Sₙ = (-?\d*)n² ([+−]) (\d*)n ([+−]) (\d+)일 때, a([₀-₉]+)의 값", q); A = _coef(m.group(1)); B = _sv(m.group(2), m.group(3) or "1"); C = _sv(m.group(4), m.group(5)); n = int(m.group(6).translate(_SUBD))
        S = lambda k: A * k * k + B * k + C  # noqa: E731
        return S(1) if n == 1 else S(n) - S(n - 1)
    if tid == "h2-1-seq-t8":
        m = re.match(r"수열 \{aₙ\}이 (.+?) \(n = 1, 2, 3, ⋯\)로 정의될 때, a([₀-₉]+)의 값", q); desc = m.group(1); M = int(m.group(2).translate(_SUBD))
        mf = re.fullmatch(r"a₁ = (-?\d+), a₂ = (-?\d+), aₙ₊₂ = aₙ₊₁ \+ aₙ", desc)
        if mf:
            seq = [Fraction(mf.group(1)), Fraction(mf.group(2))]
            while len(seq) < M: seq.append(seq[-1] + seq[-2])
            return seq[-1]
        mr = re.fullmatch(r"a₁ = (-?\d+), aₙ₊₁ = (.+)", desc); a = Fraction(mr.group(1)); rule = mr.group(2).replace("−", "-").replace("ⁿ", "**n").replace("²", "**2")
        rule = re.sub(r"(\d)aₙ", r"\1*a", rule).replace("aₙ", "a"); rule = re.sub(r"(\d)n", r"\1*n", rule)
        cur = a
        for n in range(1, M):
            cur = Fraction(eval(rule, {"__builtins__": {}}, {"a": cur, "n": Fraction(n)}))  # noqa: S307
        return cur
    return None


_SUPD = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def _sym(src):
    """마커 안 문법(pow/frac/sqrt/inf, 위첨자, 암시적 곱)을 sympy 식으로."""
    import sympy as sp
    e = src.replace("−", "-").replace("×", "*")
    e = re.sub(r"([xhtfF])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: f"{m.group(1)}**{m.group(2).translate(_SUPD)}", e)
    e = re.sub(r"pow\(([^,()]+|\([^()]*\)|[^,]+?), ?([^()]+)\)", r"((\1)**(\2))", e)
    e = e.replace("frac(", "_frac(").replace("inf", "oo")
    e = re.sub(r"(\d)\s*([a-zA-Z(])", r"\1*\2", e); e = re.sub(r"(\))\s*([a-zA-Z(])", r"\1*\2", e); e = re.sub(r"([xht])\s*\(", r"\1*(", e)
    e = re.sub(r"\b(sqrt|_frac)\*\(", r"\1(", e)
    x, h, t = sp.symbols("x h t")
    return sp.sympify(e, locals={"_frac": lambda a, b: a / b, "x": x, "h": h, "t": t, "oo": sp.oo})


def _spv(v):
    import sympy as sp
    v = sp.nsimplify(v)
    if v.is_Rational: return Fraction(int(v.p), int(v.q))
    return _ratf(float(v))


def _polyq(text):
    """'x³ − 3x² − 5x' 같은 본문 다항식 → sympy"""
    return _sym(text)


def _h22a(tid, q):
    import sympy as sp
    x = sp.Symbol("x")
    if tid == "h2-2-lim-t1":
        m = re.match(r"\[\[lim\((\w), (-?\w+), (.+)\)\]\]의 값", q); var = sp.Symbol(m.group(1)); pt = sp.oo if m.group(2) == "inf" else sp.Integer(m.group(2)); e = _sym(m.group(3))
        return _spv(sp.limit(e, var, pt))
    if tid == "h2-2-lim-t2":
        m = re.match(r"함수 f\(x\)에 대하여 \[\[lim\(x, (\d+), frac\(f\(x\), x − \d+\)\)\]\] = (-?\d+)일 때, \[\[lim\(x, \d+, frac\((.+)\)\)\]\]의 값", q); a = int(m.group(1)); L = Fraction(m.group(2)); body = m.group(3)
        mm = re.fullmatch(r"\(x ([+−]) (\d+)\) f\(x\), x − \d+", body)
        if mm: return (a + _sv(mm.group(1), mm.group(2))) * L
        if body.startswith("(pow(x,2)"): return 2 * a * L
        if body.startswith("f(x), (x −"): return L / (2 * a)
        return None
    if tid == "h2-2-lim-t3":
        m = re.match(r"\[\[lim\(x, (-?\d+), frac\(pow\(x,2\) \+ a x \+ b, x [+−] \d+\)\)\]\] = (-?\d+)일 때, 상수 a, b에 대하여 (a \+ b|ab|b − a)의 값", q); p = int(m.group(1)); L = int(m.group(2)); qv = p - L
        a, b = -(p + qv), p * qv; return Fraction({"a + b": a + b, "ab": a * b, "b − a": b - a}[m.group(3)])
    if tid == "h2-2-lim-t4":
        m = re.match(r"함수 f\(x\) = \[\[cases\(frac\((.+?), x ([+−]) (\d+)\), x ≠ (-?\d+), k, x = -?\d+\)\]\]가", q); num = _sym(m.group(1)); p = int(m.group(4)); den = x - _sv(m.group(2), m.group(3)) * -1
        return _spv(sp.limit(num / (x + _sv(m.group(2), m.group(3))), x, p))
    if tid == "h2-2-lim-t5":
        m = re.match(r"함수 f\(x\) = x³ ([+−]) (\d*)x ([+−]) (\d+) − k에 대하여 방정식 f\(x\) = 0이 열린구간 \((-?\d+), (-?\d+)\)에서", q); c = _sv(m.group(1), m.group(2) or "1"); d = _sv(m.group(3), m.group(4)); p, p1 = int(m.group(5)), int(m.group(6))
        f = lambda t: t ** 3 + c * t + d  # noqa: E731
        return Fraction(f(p1) - f(p) - 1)
    if tid == "h2-2-lim-t6":
        m = re.match(r"함수 f\(x\) = \[\[cases\(pow\(x,2\) ([+−]) (\d+), x ≥ (-?\d+), (.+?), x < -?\d+\)\]\]에 대하여", q); a = _sv(m.group(1), m.group(2)); p = int(m.group(3)); g = _sym(m.group(4))
        return Fraction(p * p) + a + _spv(g.subs(x, p))
    if tid == "h2-2-lim-t7":
        m = re.match(r"함수 f\(x\) = \[\[cases\(pow\(x,2\) \+ a, x ≥ (-?\d+), (.+?), x < -?\d+\)\]\]가", q); p = int(m.group(1)); g = _sym(m.group(2)); return _spv(g.subs(x, p)) - p * p
    if tid == "h2-2-diff-t1":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 \[\[lim\(h, 0, frac\((.+), h\)\)\]\]의 값", q); f = _polyq(m.group(1)); body = m.group(2)
        h = sp.Symbol("h"); expr = _sym(body)
        fl = sp.Lambda(x, f); expr = expr.replace(sp.Function("f"), fl)
        return _spv(sp.limit(expr / h, h, 0))
    if tid == "h2-2-diff-t7":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 \[\[lim\(x, (-?\d+), frac\((.+)\)\)\]\]의 값", q); f = _polyq(m.group(1)); p = int(m.group(2)); body = m.group(3)
        num, den = body.rsplit(", ", 1); num_e = _sym(num).replace(sp.Function("f"), sp.Lambda(x, f)); den_e = _sym(den)
        return _spv(sp.limit(num_e / den_e, x, p))
    if tid == "h2-2-diff-t2":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 f'\((-?\d+)\)의 값", q); f = _polyq(m.group(1)); return _spv(sp.diff(f, x).subs(x, int(m.group(2))))
    if tid == "h2-2-diff-t3":
        m = re.match(r"곡선 y = (.+?) 위의 점 \((-?\d+), (-?\d+)\)에서의 접선의 방정식이 y = mx \+ n일 때, 상수 m, n에 대하여 (m \+ n|n)의 값", q); f = _polyq(m.group(1)); p = int(m.group(2))
        if _spv(f.subs(x, p)) != Fraction(m.group(3)): return None
        mm = _spv(sp.diff(f, x).subs(x, p)); n = Fraction(m.group(3)) - mm * p
        return mm + n if m.group(4) == "m + n" else n
    if tid == "h2-2-diff-t4":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 닫힌구간 \[(-?\d+), (-?\d+)\]에서 (평균값 정리|롤의 정리)", q); f = _polyq(m.group(1)); p, qq = int(m.group(2)), int(m.group(3))
        avg = (f.subs(x, qq) - f.subs(x, p)) / (qq - p); cs = sp.solve(sp.Eq(sp.diff(f, x), avg), x); cs = [c for c in cs if p < c < qq]
        return _spv(cs[0]) if len(cs) == 1 else None
    if tid == "h2-2-diff-t5":
        m = re.match(r"함수 f\(x\) = (.+?)[가이] 감소하는 구간이 \[α, β\]일 때, (α \+ β|β − α)의 값", q); f = _polyq(m.group(1)); rs = sorted(sp.solve(sp.diff(f, x), x))
        if len(rs) != 2: return None
        return _spv(rs[0] + rs[1]) if m.group(2) == "α + β" else _spv(rs[1] - rs[0])
    if tid == "h2-2-diff-t6":
        m = re.match(r"함수 f\(x\) = (.+?)의 (극댓값|극솟값|극댓값과 극솟값의 차|극댓값과 극솟값의 합)[을를] 구하시오", q); f = _polyq(m.group(1)); rs = sorted(sp.solve(sp.diff(f, x), x))
        if len(rs) != 2: return None
        M, mn = _spv(f.subs(x, rs[0])), _spv(f.subs(x, rs[1]))
        return {"극댓값": M, "극솟값": mn, "극댓값과 극솟값의 차": M - mn, "극댓값과 극솟값의 합": M + mn}[m.group(2)]
    return None


def _h22b(tid, q):
    import sympy as sp
    x, t = sp.symbols("x t")
    if tid == "h2-2-diffapp-t1":
        m = re.match(r"닫힌구간 \[(-?\d+), (-?\d+)\]에서 함수 f\(x\) = (.+?)의 (최댓값|최솟값|최댓값과 최솟값의 합)[을를] 구하시오", q); lo, hi = int(m.group(1)), int(m.group(2)); f = _polyq(m.group(3))
        pts = [lo, hi] + [r for r in sp.solve(sp.diff(f, x), x) if r.is_real and lo < r < hi]; vals = [f.subs(x, p) for p in pts]; M, mn = _spv(max(vals)), _spv(min(vals))
        return {"최댓값": M, "최솟값": mn, "최댓값과 최솟값의 합": M + mn}[m.group(4)]
    if tid == "h2-2-diffapp-t2":
        m = re.match(r"방정식 (.+?) = k가 (서로 다른 세 실근을 갖도록 하는 정수 k의 개수|오직 하나의 실근을 갖도록 하는 정수 k의 최솟값|서로 다른 두 실근을 갖는 모든 k의 값의 합)[을를] 구하시오", q); f = _polyq(m.group(1)); rs = sorted(sp.solve(sp.diff(f, x), x))
        if len(rs) != 2: return None
        M, mn = _spv(f.subs(x, rs[0])), _spv(f.subs(x, rs[1]))
        return {"서로 다른 세 실근을 갖도록 하는 정수 k의 개수": M - mn - 1, "오직 하나의 실근을 갖도록 하는 정수 k의 최솟값": M + 1, "서로 다른 두 실근을 갖는 모든 k의 값의 합": M + mn}[m.group(2)]
    if tid == "h2-2-diffapp-t3":
        m = re.match(r"함수 f\(x\) = x³ \+ ax² \+ (\d+)x가 (극값을 갖지 않도록 하는 정수 a의 개수|극값을 갖도록 하는 자연수 a의 최솟값)", q); b = int(m.group(1))
        if m.group(2).startswith("극값을 갖지"): return Fraction(sum(1 for a in range(-200, 201) if a * a - 3 * b <= 0))
        return Fraction(next(a for a in range(1, 400) if a * a - 3 * b > 0))
    if tid == "h2-2-diffapp-t4":
        m = re.match(r"함수 f\(x\) = x³ \+ ax² \+ bx가 x = (-?\d+)에서 극댓값, x = (-?\d+)에서 극솟값을 가질 때, 상수 a, b에 대하여 (a \+ b|ab|a − b)의 값", q); r1, r2 = int(m.group(1)), int(m.group(2))
        a = Fraction(-3 * (r1 + r2), 2); b = Fraction(3 * r1 * r2); return {"a + b": a + b, "ab": a * b, "a − b": a - b}[m.group(3)]
    if tid == "h2-2-diffapp-t5":
        m = re.match(r"수직선 위를 움직이는 점 P의 시각 t에서의 위치 x가 x = (.+?)일 때, (.+?)[을를] 구하시오", q); xt = _polyq(m.group(1)); ask = m.group(2); v = sp.diff(xt, t); a = sp.diff(v, t)
        mm = re.fullmatch(r"t = (\d+)에서의 (속도|가속도)", ask)
        if mm: t0 = int(mm.group(1)); return _spv((v if mm.group(2) == "속도" else a).subs(t, t0))
        rs = sorted(r for r in sp.solve(v, t) if r.is_real)
        if ask.startswith("처음으로"): return _spv(next(r for r in rs if r > 0))
        if ask.startswith("속도가 0"): return _spv(sum(rs))
        return None
    if tid == "h2-2-diffapp-t6":
        m = re.match(r"한 변의 길이가 (\d+)인 정사각형", q)
        if m: L = int(m.group(1)); return Fraction(2 * (L // 3) ** 3) if L % 3 == 0 else None
        m = re.match(r"두 양수 x, y에 대하여 x \+ y = (\d+)일 때, x²y의 최댓값", q); s_ = int(m.group(1)); return Fraction(4 * s_ ** 3, 27)
    if tid == "h2-2-integ-t1":
        m = re.match(r"함수 f\(x\)의 도함수가 f'\(x\) = (.+?)이고 f\((-?\d+)\) = (-?\d+)일 때, f\((-?\d+)\)의 값", q); fp = _polyq(m.group(1)); p, v, qq = int(m.group(2)), int(m.group(3)), int(m.group(4))
        F = sp.integrate(fp, x); C = v - F.subs(x, p); return _spv(F.subs(x, qq) + C)
    if tid == "h2-2-integ-t2":
        m = re.match(r"\[\[dinteg\((-?\d+), (-?\d+), (.+), x\)\]\]의 값", q); return _spv(sp.integrate(_sym(m.group(3)), (x, int(m.group(1)), int(m.group(2)))))
    if tid == "h2-2-integ-t3":
        mo = re.fullmatch(r"\[\[dinteg\((-?\d+), (-?\d+), ([^\[\]]+), x\)\]\]의 값을 구하시오\.", q)
        if mo: return _spv(sp.integrate(_sym(mo.group(3)), (x, int(mo.group(1)), int(mo.group(2)))))
        ml = re.match(r"\[\[dinteg\(1, 3, f\(x\), x\)\]\] = (-?\d+), \[\[dinteg\(1, 3, g\(x\), x\)\]\] = (-?\d+)일 때, \[\[dinteg\(1, 3, (-?\d*)f\(x\) ([+−]) (\d*)g\(x\), x\)\]\]", q)
        if ml: fa, ga = int(ml.group(1)), int(ml.group(2)); c1 = _coef(ml.group(3)); c2 = _sv(ml.group(4), ml.group(5) or "1"); return c1 * fa + c2 * ga
        mc = re.match(r"\[\[dinteg\((-?\d+), (-?\d+), f\(x\), x\)\]\] = (-?\d+), \[\[dinteg\((-?\d+), (-?\d+), f\(x\), x\)\]\] = (-?\d+)일 때, \[\[dinteg\((-?\d+), (-?\d+), f\(x\), x\)\]\]", q)
        if mc and mc.group(2) == mc.group(4) and mc.group(1) == mc.group(7) and mc.group(5) == mc.group(8): return Fraction(int(mc.group(3)) + int(mc.group(6)))
        return None
    if tid == "h2-2-integ-t4":
        mk = re.match(r"함수 f\(x\) = (.+?) ([+−]) (\d*)\[\[dinteg\(0, 1, f\(t\), t\)\]\]일 때, f\(1\)의 값", q)
        if mk:
            P = _polyq(mk.group(1)); c = _sv(mk.group(2), mk.group(3) or "1"); ip = _spv(sp.integrate(P, (x, 0, 1))); k = ip / (1 - c); return _spv(P.subs(x, 1)) + c * k
        md = re.match(r"함수 F\(x\) = \[\[dinteg\((-?\d+), x, (.+?), t\)\]\]에 대하여 F'\((-?\d+)\)의 값", q); return _spv(_sym(md.group(2)).subs(t, int(md.group(3))))
    if tid in ("h2-2-integ-t5", "h2-2-integ-t6"):
        m = re.match(r"곡선 y = (.+?)[와과] x축으로 둘러싸인 부분의 넓이", q)
        if m:
            f = _polyq(m.group(1)); rs = sorted(r for r in sp.solve(f, x) if r.is_real); return _spv(sp.integrate(abs(f), (x, rs[0], rs[-1]))) if len(rs) == 2 else None
        m = re.match(r"곡선 y = (.+?)[와과] 직선 y = (.+?)(?:으로|로) 둘러싸인 부분의 넓이", q)
        if m:
            d = _polyq(m.group(1)) - _polyq(m.group(2)); rs = sorted(r for r in sp.solve(d, x) if r.is_real); return _spv(sp.integrate(abs(d), (x, rs[0], rs[-1]))) if len(rs) == 2 else None
        m = re.match(r"곡선 y = (.+?), x축 및 직선 x = (\d+)(?:으로|로) 둘러싸인 부분의 넓이", q)
        if m: f = _polyq(m.group(1)); a = int(m.group(2)); return _spv(sp.integrate(abs(f), (x, 0, a)))
        m = re.match(r"곡선 y = x³, x축 및 두 직선 x = -(\d+), x = (\d+)(?:으로|로) 둘러싸인", q)
        if m: a = int(m.group(2)); return _spv(sp.integrate(abs(x ** 3), (x, -a, a)))
        m = re.match(r"두 곡선 y = (.+?)[와과] y = (.+?)(?:으로|로) 둘러싸인 부분의 넓이", q)
        if m:
            d = _polyq(m.group(1)) - _polyq(m.group(2)); rs = sorted(r for r in sp.solve(d, x) if r.is_real); return _spv(sp.integrate(abs(d), (x, rs[0], rs[-1]))) if len(rs) == 2 else None
        return None
    return None


def _sym2(src):
    """h3 마커 문법 → sympy (지수·로그·삼각·합·극한 포함)."""
    import sympy as sp
    e = src.replace("−", "-").replace("×", "*").replace("π", "pi")
    e = re.sub(r"([a-zA-Z0-9)])([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: f"{m.group(1)}**{m.group(2).translate(_SUPD)}", e)
    e = e.replace("frac(", "_frac(").replace("inf", "oo")
    e = re.sub(r"(\d)\s*([a-zA-Z_(])", r"\1*\2", e)
    e = re.sub(r"(\))\s+([a-zA-Z_(])", r"\1*\2", e)
    e = re.sub(r"(\))\(", r"\1*(", e)
    e = re.sub(r"\b([xntk])\s*\(", r"\1*(", e)
    e = re.sub(r"\b([xntk])\s+(pow|sin|cos|tan|ln|sqrt|_frac|e\b)", r"\1*\2", e)
    e = re.sub(r"\b(sqrt|_frac|pow|sin|cos|tan|sec|ln|abs)\*\(", r"\1(", e)
    x, n, k, t = sp.symbols("x n k t")
    loc = {"_frac": lambda a, b: a / b, "x": x, "n": n, "k": k, "t": t, "oo": sp.oo, "e": sp.E, "pi": sp.pi, "ln": sp.log, "sec": sp.sec, "pow": lambda a, b: a ** b}
    return sp.sympify(e, locals=loc)


def _targs(inner):
    """괄호 깊이를 고려해 최상위 쉼표로 인자 나누기"""
    args, depth, cur = [], 0, ""
    for ch in inner:
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == "," and depth == 0:
            args.append(cur.strip()); cur = ""
        else:
            cur += ch
    args.append(cur.strip())
    return args


def _h31(tid, q):
    import sympy as sp
    x, n, k, t = sp.symbols("x n k t")
    if tid == "h3-1-seqlim-t1":
        m = re.match(r"\[\[lim\(n, inf, (.+)\)\]\]의 값", q); return _spv(sp.limit(_sym2(m.group(1)), n, sp.oo))
    if tid == "h3-1-seqlim-t2":
        m = re.match(r"등비수열 \{\[\[pow\(frac\(r ([+−]) (\d+), (\d+)\), n\)\]\]\}이 수렴하도록 하는 (정수 r의 개수|정수 r의 최댓값)", q); c = -_sv(m.group(1), m.group(2)); kk = int(m.group(3))
        rs = [r for r in range(-100, 101) if -1 < Fraction(r - c, kk) <= 1]; return Fraction(len(rs)) if m.group(4).endswith("개수") else Fraction(max(rs))
    if tid == "h3-1-seqlim-t3":
        m = re.match(r"급수 \[\[sum\(n, 1, inf, (.+)\)\]\]의 합", q); e = _sym2(m.group(1)); return _spv(sp.summation(e, (n, 1, sp.oo)))
    if tid == "h3-1-seqlim-t4":
        m = re.match(r"등비급수 \[\[sum\(n, 1, inf, (.+)\)\]\]의 합", q)
        if m: return _spv(sp.summation(_sym2(m.group(1)), (n, 1, sp.oo)))
        m = re.match(r"순환소수 0\.(\d\d)", q); f = Fraction(int(m.group(1)), 99); return Fraction(f.numerator + f.denominator)
    if tid == "h3-1-seqlim-t5":
        m = re.match(r"넓이가 (\d+)인 도형 S₁에서 시작하여 (.+?)을 차례로", q); S1 = int(m.group(1)); d = m.group(2)
        r = Fraction(1, 4) if "1/4" in d else Fraction(4, 9) if "4/9" in d else Fraction(1, 3) if "1/3" in d else Fraction(1, 2); return S1 / (1 - r)
    if tid in ("h3-1-diff2-t1", "h3-1-diff2-t2"):
        m = re.match(r"\[\[lim\(x, 0, (.+)\)\]\]의 값", q); return _spv(sp.limit(_sym2(m.group(1)), x, 0))
    if tid == "h3-1-diff2-t3":
        m = re.match(r"함수 f\(x\) = (.+?)에 대하여 f'\((-?\d+)\)의 값", q)
        if m:
            fx = m.group(1); mm = re.fullmatch(r"\((.+?)\)\[\[pow\(e, x\)\]\]", fx); f = _sym2(mm.group(1)) * sp.exp(x) if mm else _sym2(fx[2:-2])
            return _spv(sp.diff(f, x).subs(x, int(m.group(2))))
        m = re.match(r"매개변수 t로 나타낸 곡선 x = \[\[(.+?)\]\], y = \[\[(.+?)\]\]에 대하여 t = (-?\d+)일 때", q)
        if m: xt, yt, t0 = _sym2(m.group(1)), _sym2(m.group(2)), int(m.group(3)); return _spv((sp.diff(yt, t) / sp.diff(xt, t)).subs(t, t0))
        m = re.match(r"곡선 \[\[(.+?) = (\d+)\]\] 위의 점 \((-?\d+), (-?\d+)\)에서의", q)
        if m:
            y = sp.Symbol("y"); F = _sym2(m.group(1).replace("y", "Y")).subs(sp.Symbol("Y"), y) - int(m.group(2)); dydx = -sp.diff(F, x) / sp.diff(F, y); return _spv(dydx.subs({x: int(m.group(3)), y: int(m.group(4))}))
        m = re.match(r"함수 f\(x\) = \[\[(.+?)\]\]의 역함수를 g\(x\)라 할 때, g'\((-?\d+)\)의 값", q); f = _sym2(m.group(1)); y0 = int(m.group(2))
        xs = [r for r in sp.solve(sp.Eq(f, y0), x) if r.is_real]
        return _spv(1 / sp.diff(f, x).subs(x, xs[0])) if len(xs) == 1 else None
    if tid == "h3-1-diff2-t4":
        m = re.match(r"곡선 y = \[\[(.+?)\]\] 위의 점 \((-?\d+), (.+?)\)에서의 접선의 방정식이 y = mx \+ n일 때, (상수 m, n에 대하여 m \+ n의 값|이 접선의 y절편|이 접선의 x절편)", q); f = _sym2(m.group(1)); x0 = int(m.group(2)); y0 = _spv(f.subs(x, x0)); mm = _spv(sp.diff(f, x).subs(x, x0)); nn = y0 - mm * x0
        return mm + nn if m.group(4).startswith("상수") else nn if "y절편" in m.group(4) else -nn / mm
    if tid == "h3-1-diff2-t5":
        m = re.match(r"(?:x > 0에서 )?함수 f\(x\) = (.+?)의 (극솟값|극댓값)[을를] 구하시오", q); fx = m.group(1)
        fx = re.sub(r"\[\[(.+?)\]\]", r"(\1)", fx); f = _sym2(fx); cs = [c for c in sp.solve(sp.diff(f, x), x) if c.is_real and (c > 0 if "x > 0" in q else True)]
        vals = [f.subs(x, c) for c in cs]; d2 = [sp.diff(f, x, 2).subs(x, c) for c in cs]
        want = [v for v, dd in zip(vals, d2) if (dd > 0 if m.group(2) == "극솟값" else dd < 0)]
        return _spv(want[0]) if len(want) == 1 else None
    if tid in ("h3-1-integ2-t1", "h3-1-integ2-t2", "h3-1-integ2-t3"):
        m = re.match(r"\[\[dinteg\((.+)\)\]\]의 값", q); lo, hi, body, var = _targs(m.group(1)); return _spv(sp.integrate(_sym2(body), (x, _sym2(lo), _sym2(hi))))
    if tid == "h3-1-integ2-t4":
        m = re.match(r"\[\[lim\(n, inf, (.+)\)\]\]의 값", q)
        body = m.group(1)
        mm = re.fullmatch(r"(?:(\d+) )?sum\(k, 1, n, (.+)\)", body)
        if mm:
            c = int(mm.group(1) or 1); f = _sym2(mm.group(2)); val = c * sp.limit(sp.summation(f, (k, 1, n)), n, sp.oo); return _spv(val)
        mm = re.fullmatch(r"(?:(\d+) )?frac\((\d+), n\) sum\(k, 1, n, (.+)\)", body)
        if mm:
            c = int(mm.group(1) or 1); w = int(mm.group(2)); f = _sym2(mm.group(3)); val = c * sp.limit(sp.summation(f * sp.Rational(w) / n, (k, 1, n)), n, sp.oo); return _spv(val)
        return None
    if tid == "h3-1-integ2-t5":
        m = re.match(r"곡선 y = (.+?), x축 및 두 직선 x = (.+?), x = (.+?)(?:으로|로) 둘러싸인", q); fx = re.sub(r"\[\[(.+?)\]\]", r"(\1)", m.group(1)); f = _sym2(fx)
        fixln = lambda z: re.sub(r"ln (\d+)", r"ln(\1)", z.strip("[]"))  # noqa: E731
        lo = _sym2(fixln(m.group(2))); hi = _sym2(fixln(m.group(3)))
        val = sp.integrate(sp.Abs(f), (x, lo, hi))
        if val.has(sp.Abs) or not val.is_number: val = sp.Integral(sp.Abs(f), (x, lo, hi)).evalf(30)
        return _spv(sp.simplify(val))
    if tid == "h3-1-integ2-t6":
        m = re.match(r"수직선 위를 움직이는 점 P의 시각 t\(t ≥ 0\)에서의 속도가 v\(t\) = (.+?)일 때, t = 0에서 t = (.+?)까지 점 P(가 움직인 거리|의 위치의 변화량)", q); v = _sym2(m.group(1).replace("sin t", "sin(t)").replace("cos t", "cos(t)")); hi = _sym2(m.group(2))
        val = sp.integrate(sp.Abs(v) if m.group(3).startswith("가") else v, (t, 0, hi))
        if not val.is_number or val.has(sp.Abs): val = sp.Integral(sp.Abs(v) if m.group(3).startswith("가") else v, (t, 0, hi)).evalf(30)
        return _spv(sp.simplify(val))
    return None


def _pv(s):
    """확률값 문자열 — [[frac(a,b)]] 또는 정수/소수."""
    return _mk(s.strip())


def _h32(tid, q):
    """h3-2 확률과 통계 — 발문에서 다시 푼다."""
    C = math.comb
    if tid == "h3-2-count-t1":
        m = re.match(r"(\d+)명의 학생이 원탁에 둘러앉는 경우의 수", q)
        if m: return Fraction(math.factorial(int(m.group(1)) - 1))
        m = re.match(r"(\d+)명의 학생이 원탁에 둘러앉을 때, 특정한 2명이 서로 이웃", q)
        if m: return Fraction(2 * math.factorial(int(m.group(1)) - 2))
        m = re.match(r"(\d+)명의 학생이 (\d+)개의 동아리 중 하나에 각각 가입", q)
        if m: return Fraction(int(m.group(2)) ** int(m.group(1)))
        m = re.match(r"서로 다른 (\d+)개의 문자에서 중복을 허락하여 (\d+)개를 택해 일렬로", q)
        if m: return Fraction(int(m.group(1)) ** int(m.group(2)))
        return None
    if tid == "h3-2-count-t2":
        m = re.match(r"(\d+)개의 문자 ([a-z, ]+)를 모두 일렬로", q)
        if m:
            letters = [c for c in m.group(2).split(", ")]; v = math.factorial(len(letters))
            for c in set(letters): v //= math.factorial(letters.count(c))
            return Fraction(v) if len(letters) == int(m.group(1)) else None
        m = re.search(r"오른쪽으로 (\d+)칸, 위쪽으로 (\d+)칸", q)
        if m: a, b = int(m.group(1)), int(m.group(2)); return Fraction(C(a + b, a))
        return None
    if tid == "h3-2-count-t3":
        m = re.match(r"서로 다른 (\d+)종류의 과일 중에서 중복을 허락하여 (\d+)개", q)
        if m: n_, r_ = int(m.group(1)), int(m.group(2)); return Fraction(C(n_ + r_ - 1, r_))
        m = re.match(r"방정식 ([a-z + ]+) = (\d+)[을를] 만족시키는 (양의 정수|음이 아닌 정수)", q)
        if m:
            k = len(m.group(1).split(" + ")); s = int(m.group(2))
            return Fraction(C(s - 1, k - 1)) if m.group(3) == "양의 정수" else Fraction(C(s + k - 1, k - 1))
        return None
    if tid == "h3-2-count-t4":
        m = re.match(r"\[\[pow\(x ([+−]) (\d+), (\d+)\)\]\]의 전개식에서 (?:\[\[pow\(x,(\d+)\)\]\]|x)의 계수", q)
        if m:
            a = _sv(m.group(1), m.group(2)); n_ = int(m.group(3)); k = int(m.group(4) or 1); return C(n_, k) * a ** (n_ - k)
        m = re.match(r"\[\[comb\((\d+), (\d)\)\]\] \+ \[\[comb\(\d+, \d\)\]\]", q)
        if m: n_ = int(m.group(1)); return Fraction(2 ** n_) if m.group(2) == "0" else Fraction(2 ** (n_ - 1))
        return None
    if tid == "h3-2-prob-t1":
        m = re.match(r"서로 다른 두 개의 주사위를 동시에 던질 때, (.+?)(?:일|) 확률", q)
        if m:
            d = m.group(1); pairs = [(i, j) for i in range(1, 7) for j in range(1, 7)]
            mm = re.fullmatch(r"두 눈의 수의 합이 (\d+)의 배수", d)
            if mm: f = lambda i, j: (i + j) % int(mm.group(1)) == 0  # noqa: E731
            elif (mm := re.fullmatch(r"두 눈의 수의 합이 (\d+) 이상", d)): f = lambda i, j: i + j >= int(mm.group(1))  # noqa: E731
            elif (mm := re.fullmatch(r"두 눈의 수의 합이 (\d+)", d)): f = lambda i, j: i + j == int(mm.group(1))  # noqa: E731
            elif (mm := re.fullmatch(r"두 눈의 수의 곱이 (\d+)", d)): f = lambda i, j: i * j == int(mm.group(1))  # noqa: E731
            elif d == "두 눈의 수의 곱이 홀수": f = lambda i, j: (i * j) % 2 == 1  # noqa: E731
            elif d == "두 눈의 수가 서로 같을": f = lambda i, j: i == j  # noqa: E731
            elif (mm := re.fullmatch(r"두 눈의 수의 차가 (\d+)", d)): f = lambda i, j: abs(i - j) == int(mm.group(1))  # noqa: E731
            else: return None
            return Fraction(sum(1 for i, j in pairs if f(i, j)), 36)
        m = re.match(r"흰 공 (\d+)개와 검은 공 (\d+)개가 들어 있는 주머니에서 임의로 (\d+)개의 공을 동시에 꺼낼 때, (\d+)개 모두 흰 공일 확률", q)
        if m: w, b, k = int(m.group(1)), int(m.group(2)), int(m.group(3)); return Fraction(C(w, k), C(w + b, k))
        return None
    if tid in ("h3-2-prob-t2", "h3-2-prob-t4"):
        m = re.match(r"한 번의 시행에서 사건 A가 일어날 확률이 (\[\[.+?\]\])이다\. 이 시행을 (\d+)번 독립적으로 반복할 때, 사건 A가 적어도 한 번", q)
        if m: p = _pv(m.group(1)); return 1 - (1 - p) ** int(m.group(2))
        given = {k: _pv(v) for k, v in re.findall(r"\[\[prob\((.+?)\)\]\] = (\[\[.+?\]\]|\d+)(?=,|일 때)", q)}
        ask = re.search(r"일 때, (?:\[\[prob\((.+?)\)\]\]의 값|(두 사건이 모두 일어나지 않을 확률))", q)
        if not ask: return None
        PA, PB = given.get("A"), given.get("B")
        if "서로 독립" in q:
            if ask.group(1) == "inter(A, B)": return PA * PB
            if ask.group(1) == "B": return given["inter(A, B)"] / PA
            if ask.group(1) == "union(A, B)": return PA + PB - PA * PB
            if ask.group(2): return (1 - PA) * (1 - PB)
            return None
        if "서로 배반사건" in q: PAB = Fraction(0)
        elif "inter(A, B)" in given: PAB = given["inter(A, B)"]
        else: PAB = PA + PB - given["union(A, B)"]
        PU = PA + PB - PAB
        if ask.group(1) == "inter(A, B)": return PAB
        if ask.group(1) == "union(A, B)": return PU
        if ask.group(1) == "inter(comp(A), comp(B))": return 1 - PU
        return None
    if tid == "h3-2-prob-t3":
        m = re.match(r"어느 학급 학생 (\d+)명 중 남학생은 (\d+)명, 여학생은 (\d+)명이다\. 안경을 쓴 남학생은 (\d+)명, 안경을 쓴 여학생은 (\d+)명이다\. 이 학급에서 임의로 뽑은 한 학생이 (.+?)일 때 (.+?)일 확률", q)
        tot, M, F, gM, gF = (int(m.group(i)) for i in range(1, 6))
        if M + F != tot: return None
        cnt = {("남", "안경"): gM, ("남", "무"): M - gM, ("여", "안경"): gF, ("여", "무"): F - gF}
        def sel(s):
            if s == "남학생": return lambda g, e: g == "남"
            if s == "여학생": return lambda g, e: g == "여"
            if s == "안경을 쓴 학생": return lambda g, e: e == "안경"
            if s == "안경을 쓰지 않은 학생": return lambda g, e: e == "무"
            return None
        fa, fb = sel(m.group(6)), sel(m.group(7))
        if fa is None or fb is None: return None
        na = sum(v for (g, e), v in cnt.items() if fa(g, e)); nab = sum(v for (g, e), v in cnt.items() if fa(g, e) and fb(g, e))
        return Fraction(nab, na)
    if tid == "h3-2-prob-t5":
        m = re.match(r"한 번의 시행에서 사건 A가 일어날 확률이 (\[\[.+?\]\])이다\. 이 시행을 (\d+)번 독립적으로 반복할 때, 사건 A가 (정확히 (\d+)번|(\d+)번 이상) 일어날 확률", q)
        p = _pv(m.group(1)); n_ = int(m.group(2))
        if m.group(4): k = int(m.group(4)); return C(n_, k) * p ** k * (1 - p) ** (n_ - k)
        k = int(m.group(5)); return sum(C(n_, j) * p ** j * (1 - p) ** (n_ - j) for j in range(k, n_ + 1))
    if tid == "h3-2-stat-t1":
        m = re.search(r"\[\[mat\(2, (\d+), X, (.+?), P\(X = x\), (.+)\)\]\]$", q); c = int(m.group(1)) - 1
        xs = [Fraction(v) for v in m.group(2).split(", ")]; ps = [_pv(v) for v in _targs(m.group(3))]
        if len(xs) != c or len(ps) != c or sum(ps) != 1: return None
        E = sum(x * p for x, p in zip(xs, ps)); V = sum(x * x * p for x, p in zip(xs, ps)) - E * E
        ask = re.search(r"\[\[(ev|var)\((.+?)\)\]\]의 값", q); fn, arg = ask.group(1), ask.group(2)
        if arg == "X": a, b = 1, 0
        else:
            mm = re.fullmatch(r"(-?\d*)X(?: ([+−]) (\d+))?", arg); a = _coef(mm.group(1)); b = _sv(mm.group(2), mm.group(3)) if mm.group(2) else 0
        return a * E + b if fn == "ev" else a * a * V
    if tid == "h3-2-stat-t2":
        m = re.search(r"\[\[binomd\((\d+), (.+?)\)\]\]을 따를 때, \[\[(ev|var|sd)\((.+?)\)\]\]의 값", q); n_ = int(m.group(1)); p = _pv(m.group(2)); E = n_ * p; V = n_ * p * (1 - p)
        fn, arg = m.group(3), m.group(4)
        if fn == "ev" and arg == "X": return E
        if fn == "var" and arg == "X": return V
        if fn == "sd" and arg == "X": r = _rootf(V, 2); return r if isinstance(r, Fraction) else None
        if fn == "var" and arg == "2X + 1": return 4 * V
        return None
    if tid == "h3-2-stat-t3":
        m = re.match(r"확률변수 X가 정규분포 \[\[normald\((\d+), pow\((\d+),2\)\)\]\]을 따를 때, P\((\d+) ≤ X ≤ (\d+)\)의 값", q); mu, sd, a, b = (int(m.group(i)) for i in range(1, 5))
        z1, z2 = Fraction(a - mu, sd), Fraction(b - mu, sd)
        tbl = {Fraction(z): Fraction(v) for z, v in re.findall(r"P\(0 ≤ Z ≤ ([\d.]+)\) = ([\d.]+)", q)}
        def area(z):
            if z == 0: return Fraction(0)
            return tbl.get(abs(z))
        A1, A2 = area(z1), area(z2)
        if A1 is None or A2 is None: return None
        return A1 + A2 if z1 * z2 <= 0 else abs(A2 - A1)
    if tid == "h3-2-stat-t4":
        m = re.match(r"정규분포 \[\[normald\((\d+), pow\((\d+),2\)\)\]\]을 따르는 모집단에서 크기가 (\d+)인 표본을 임의추출할 때, 표본평균 X̄에 대하여 (E|V|σ)\(X̄\)의 값", q); mu, sd, n_ = (int(m.group(i)) for i in range(1, 4))
        if m.group(4) == "E": return Fraction(mu)
        if m.group(4) == "V": return Fraction(sd * sd, n_)
        r = _rootf(Fraction(sd * sd, n_), 2); return r if isinstance(r, Fraction) else None
    if tid == "h3-2-stat-t5":
        z = Fraction(re.search(r"P\(\|Z\| ≤ ([\d.]+)\)", q).group(1))
        m = re.match(r"모표준편차가 (\d+)인 정규모집단에서 크기가 (\d+)인 표본을 임의추출하여 모평균 m을 신뢰도 (\d+)%로 추정할 때, 신뢰구간의 길이", q)
        if m:
            sd, n_ = int(m.group(1)), int(m.group(2)); sn = _isqrt(Fraction(n_)); return None if sn is None else 2 * z * Fraction(sd) / sn
        m = re.match(r"모표준편차가 (\d+)인 정규모집단에서 크기가 (\d+)인 표본을 임의추출하여 얻은 표본평균이 (\d+)이다\. 모평균 m에 대한 신뢰도 (\d+)%의 신뢰구간이 a ≤ m ≤ b일 때, (a|b)의 값", q)
        if m:
            sd, n_, xb = int(m.group(1)), int(m.group(2)), int(m.group(3)); sn = _isqrt(Fraction(n_))
            if sn is None: return None
            half = z * Fraction(sd) / sn; return xb + half if m.group(5) == "b" else xb - half
        return None
    if tid == "h3-2-stat-t6":
        m = re.match(r"모비율이 (\[\[.+?\]\])인 모집단에서 크기가 (\d+)인 표본을 임의추출할 때, 표본비율 p̂에 대하여 (E|V|σ)\(p̂\)의 값", q)
        if m:
            p = _pv(m.group(1)); n_ = int(m.group(2)); V = p * (1 - p) / n_
            if m.group(3) == "E": return p
            if m.group(3) == "V": return V
            r = _rootf(V, 2); return r if isinstance(r, Fraction) else None
        m = re.match(r"크기가 (\d+)인 표본에서 표본비율이 (\[\[.+?\]\])일 때, 모비율 p에 대한 신뢰도 95%의 신뢰구간의 길이", q)
        if m:
            n_ = int(m.group(1)); p = _pv(m.group(2)); r = _rootf(p * (1 - p) / n_, 2)
            return None if not isinstance(r, Fraction) else 2 * Fraction("1.96") * r
        return None
    return None


def _pts3(q):
    return [tuple(Fraction(v) for v in m) for m in re.findall(r"\((-?\d+), (-?\d+), (-?\d+)\)", q)]


def _vcs(q):
    return [tuple(Fraction(v) for v in m.split(", ")) for m in re.findall(r"vcomp\(([-\d, ]+)\)", q)]


def _sqr(v):
    """정확한 제곱근(유리수) 또는 None."""
    r = _rootf(Fraction(v), 2)
    return r if isinstance(r, Fraction) else None


def _plane3(text):
    """'ax + by + cz + d = 0' → (a, b, c, d) (계수 1 생략·부호 허용)."""
    m = re.search(r"(-?\d*)x ([+-]) (\d*)y ([+-]) (\d*)z(?: ([+-]) (\d+))? = 0", text)
    if not m:
        return None
    a = _coef(m.group(1)); b = _sv(m.group(2), m.group(3) or "1"); c = _sv(m.group(4), m.group(5) or "1"); d = _sv(m.group(6), m.group(7)) if m.group(6) else Fraction(0)
    return a, b, c, d


def _dirs(text):
    """직선 '(x − a)/l = (y − b)/m = (z − c)/n' 마커에서 (l, m, n) 목록 — k 는 None."""
    out = []
    for var, den in re.findall(r"frac\(([xyz])(?: [+-] \d+)?, (-?\d+|k)\)", text):
        out.append(None if den == "k" else Fraction(den))
    return out


def _h33(tid, q):
    """h3-3 기하 — 발문에서 다시 푼다."""
    q = q.replace("−", "-")
    if tid == "h3-3-conic-t1":
        m = re.match(r"포물선 \[\[pow\(([xy]),2\) = (-?\d+)([xy])\]\]", q)
        if m:
            p = Fraction(int(m.group(2)), 4)
            if "초점의 x좌표" in q or "초점의 y좌표" in q: return p
            if "준선의 방정식" in q: return -p
            if "초점과 준선 사이의 거리" in q: return 2 * abs(p)
            mm = re.search(r"점 P의 x좌표가 (-?\d+)일 때", q); return Fraction(mm.group(1)) + p
        m = re.match(r"포물선 \[\[pow\(y ([+-]) (\d+), 2\) = (-?\d+)\(x ([+-]) (\d+)\)\]\]", q)
        k = -_sv(m.group(1), m.group(2)); p = Fraction(int(m.group(3)), 4); h = -_sv(m.group(4), m.group(5))
        return h + p + k if "초점의 좌표" in q else h - p
    if tid in ("h3-3-conic-t2", "h3-3-conic-t3"):
        m = re.search(r"두 초점 F\((\d+), 0\), F'\(-\d+, 0\)으로부터의 거리의 (합|차)[가이] (\d+)인", q)
        if m:
            c = Fraction(m.group(1)); a = Fraction(m.group(3)) / 2
            b2 = a * a - c * c if m.group(2) == "합" else c * c - a * a
            return a * a + b2
        m = re.search(r"frac\(pow\(x,2\), (\d+)\) ([+-]) frac\(pow\(y,2\), (\d+)\) = (-?1)", q); A, B = Fraction(m.group(1)), Fraction(m.group(3)); rhs = m.group(4)
        if m.group(2) == "+":
            a2, b2 = max(A, B), min(A, B); a, b, c = _sqr(a2), _sqr(b2), _sqr(a2 - b2)
            main = 2 * a
        else:
            a, b, c = _sqr(A), _sqr(B), _sqr(A + B)
            main = 2 * a if rhs == "1" else 2 * b
        if None in (a, b, c): return None
        if "두 초점 사이의 거리" in q: return 2 * c
        if "장축의 길이" in q or "주축의 길이" in q: return main
        if "단축의 길이" in q: return 2 * b
        if "PF + PF'의 값" in q or "|PF - PF'|의 값" in q: return main
        if "양수 c의 값" in q: return c
        if "점근선" in q: return b / a
        mm = re.search(r"PF = (\d+)일 때, 선분 PF'", q)
        if mm: return 2 * a - Fraction(mm.group(1))
        return None
    if tid == "h3-3-conic-t4":
        mm = re.search(r"위의 점 \((-?\d+), (-?\d+)\)에서의 접선", q); x1, y1 = Fraction(mm.group(1)), Fraction(mm.group(2))
        m = re.match(r"포물선 \[\[pow\(y,2\) = (-?\d+)x\]\]", q)
        if m:
            p = Fraction(int(m.group(1)), 4); slope = 2 * p / y1; n = 2 * p * x1 / y1; xi = -x1
        else:
            m = re.search(r"frac\(pow\(x,2\), (\d+)\) ([+-]) frac\(pow\(y,2\), (\d+)\) = 1", q); A, B = Fraction(m.group(1)), Fraction(m.group(3))
            if m.group(2) == "+": slope = -(B * x1) / (A * y1); n = B / y1
            else: slope = (B * x1) / (A * y1); n = -B / y1
            xi = A / x1
        if "기울기" in q: return slope
        if "x절편" in q: return xi
        if "y절편" in q: return n
        if "m + n" in q: return slope + n
        return None
    if tid == "h3-3-conic-t5":
        mm = re.search(r"기울기가 (\[\[.+?\]\]|-?\d+)인", q); mv = _mk(mm.group(1))
        m = re.match(r"포물선 \[\[pow\(([xy]),2\) = (-?\d+)([xy])\]\]", q)
        if m:
            p = Fraction(int(m.group(2)), 4); return p / mv if m.group(1) == "y" else -p * mv * mv
        m = re.search(r"frac\(pow\(x,2\), (\d+)\) ([+-]) frac\(pow\(y,2\), (\d+)\) = 1", q); A, B = Fraction(m.group(1)), Fraction(m.group(3))
        s2 = A * mv * mv + B if m.group(2) == "+" else A * mv * mv - B
        if "y절편의 곱" in q: return -s2
        return _sqr(s2)
    if tid == "h3-3-space-t1":
        m = re.search(r"PH = (\d+), HQ = (\d+)일 때", q)
        if m: return _sqr(Fraction(m.group(1)) ** 2 + Fraction(m.group(2)) ** 2)
        m = re.search(r"PH = (\d+)이고 점 P와 직선 l 사이의 거리가 (\d+)일 때", q)
        if m: return _sqr(Fraction(m.group(2)) ** 2 - Fraction(m.group(1)) ** 2)
        m = re.match(r"넓이가 (\d+)인 삼각형 ABC가 평면 α와 이루는 각의 크기가 60°", q)
        if m: return Fraction(m.group(1)) / 2
        m = re.match(r"삼각형 ABC의 평면 α 위로의 정사영의 넓이가 (\d+)이고", q)
        if m: return 2 * Fraction(m.group(1))
        m = re.match(r"넓이가 (\d+)인 평면도형의 평면 α 위로의 정사영의 넓이가 (\d+)이다", q)
        if m: return Fraction(m.group(2)) / Fraction(m.group(1))
        m = re.match(r"길이가 (\d+)인 선분 AB가 평면 α와 이루는 각의 크기가 60°", q)
        if m: return Fraction(m.group(1)) / 2
        m = re.search(r"각의 크기가 30°이고, 직선 l 위의 점 P와 평면 α 사이의 거리가 (\d+)이다", q)
        if m: return 2 * Fraction(m.group(1))
        return None
    if tid == "h3-3-space-t2":
        P = _pts3(q)
        if q.startswith("두 점"):
            A, B = P[:2]; return _sqr(sum((B[i] - A[i]) ** 2 for i in range(3)))
        a, b, c = P[0]
        if "xy평면에 대하여 대칭이동한 점을 Q라 할 때, 선분 PQ" in q: return 2 * abs(c)
        if "xy평면 사이의 거리" in q: return abs(c)
        if "xy평면에 대하여 대칭이동한 점을 Q(p, q, r)" in q: return a + b - c
        if "z축에 대하여 대칭이동한 점을 Q(p, q, r)" in q: return -a - b + c
        if "z축 사이의 거리" in q: return _sqr(a * a + b * b)
        if "x축에 내린 수선의 발" in q: return _sqr(b * b + c * c)
        return None
    if tid == "h3-3-space-t3":
        P = _pts3(q)
        m = re.search(r"선분 AB를 (\d+) : (\d+)(?:으로|로) (내분|외분)", q)
        if m:
            mm, nn = Fraction(m.group(1)), Fraction(m.group(2)); A, B = P[:2]
            if m.group(3) == "내분": return sum((mm * B[i] + nn * A[i]) / (mm + nn) for i in range(3))
            return sum((mm * B[i] - nn * A[i]) / (mm - nn) for i in range(3))
        if "중점" in q: A, B = P[:2]; return sum((A[i] + B[i]) / 2 for i in range(3))
        if "무게중심" in q: A, B, C = P[:3]; return sum((A[i] + B[i] + C[i]) / 3 for i in range(3))
        return None
    if tid == "h3-3-space-t4":
        m = re.match(r"구 \[\[pow\(x,2\) \+ pow\(y,2\) \+ pow\(z,2\)(.*?) = 0\]\]", q)
        if m:
            rest = m.group(1); co = {"x": Fraction(0), "y": Fraction(0), "z": Fraction(0)}; d = Fraction(0)
            for sg, num, var in re.findall(r"([+-]) (\d*)([xyz]?)", rest):
                if var: co[var] = _sv(sg, num or "1")
                elif num: d = _sv(sg, num)
            ctr = tuple(-co[v] / 2 for v in "xyz"); r2 = sum(t * t for t in ctr) - d
            return _sqr(r2) if "반지름" in q else sum(ctr)
        m = re.match(r"중심이 \((-?\d+), (-?\d+), (-?\d+)\)이고 xy평면에 접하는 구", q)
        if m: return abs(Fraction(m.group(3)))
        m = re.match(r"구 \[\[(.+?) = (\d+)\]\](?:과|와) xy평면이 만나서", q)
        if m:
            R2 = Fraction(m.group(2)); mz = re.search(r"pow\(z(?: ([+-]) (\d+))?, ?2\)", m.group(1)); cz = -_sv(mz.group(1), mz.group(2)) if mz.group(1) else Fraction(0)
            return _sqr(R2 - cz * cz)
        m = re.match(r"두 점 A\((-?\d+), (-?\d+), (-?\d+)\), B\((-?\d+), (-?\d+), (-?\d+)\)[을를] 지름", q)
        if m:
            A = tuple(Fraction(m.group(i)) for i in (1, 2, 3)); B = tuple(Fraction(m.group(i)) for i in (4, 5, 6)); dd = _sqr(sum((B[i] - A[i]) ** 2 for i in range(3)))
            return None if dd is None else dd / 2
        return None
    if tid == "h3-3-vec-t1":
        V = _vcs(q)
        m = re.search(r"\[\[(?:abs\()?(-?\d*) ?vec\(a\) ([+-]) (\d*) ?vec\(b\)\)?\]\]", q)
        if m and "성분의 합" in q or (m and "abs(" in q and "의 값" in q and "vcomp(x" not in q):
            k = _coef(m.group(1)); l = _sv(m.group(2), m.group(3) or "1"); a, b = V[0], V[1]
            w = tuple(k * a[i] + l * b[i] for i in range(2))
            return sum(w) if "성분의 합" in q else _sqr(w[0] ** 2 + w[1] ** 2)
        if "서로 평행할 때, 실수 t" in q:
            a, b, c = V[:3]; den = b[0] * c[1] - b[1] * c[0]
            return None if den == 0 else (a[1] * c[0] - a[0] * c[1]) / den
        if q.startswith("공간벡터"): a = V[0]; return _sqr(sum(t * t for t in a))
        mm = re.search(r"\[\[vec\(a\)\]\] = \[\[vcomp\(x, (-?\d+)\)\]\], \[\[vec\(b\)\]\] = \[\[vcomp\((-?\d+), y\)\]\]에 대하여 \[\[(-?\d*) ?vec\(a\) ([+-]) (\d*) ?vec\(b\)\]\] = \[\[vcomp\((-?\d+), (-?\d+)\)\]\]", q)
        if mm:
            a2, b1 = Fraction(mm.group(1)), Fraction(mm.group(2)); k = _coef(mm.group(3)); l = _sv(mm.group(4), mm.group(5) or "1"); r0, r1 = Fraction(mm.group(6)), Fraction(mm.group(7))
            x = (r0 - l * b1) / k; y = (r1 - k * a2) / l; return x + y
        return None
    if tid == "h3-3-vec-t2":
        m = re.search(r"\[\[abs\(vec\(a\)\)\]\] = (\d+), \[\[abs\(vec\(b\)\)\]\] = (\d+)", q)
        if m:
            p, r = Fraction(m.group(1)), Fraction(m.group(2))
            mm = re.search(r"각의 크기가 (\d+)°", q)
            if mm: th = int(mm.group(1)); dot = p * r * {60: Fraction(1, 2), 90: Fraction(0), 120: Fraction(-1, 2)}[th]
            else: dot = Fraction(re.search(r"\[\[dot\(vec\(a\), vec\(b\)\)\]\] = (-?\d+)", q).group(1))
            sgn = 1 if re.search(r"vec\(a\) \+ vec\(b\)", q) else -1
            v = p * p + 2 * sgn * dot + r * r
            return v if "pow(abs" in q else _sqr(v)
        V = _vcs(q)
        m = re.search(r"선분 AB를 (\d+) : (\d+)(?:으로|로) 내분", q)
        if m: mm, nn = Fraction(m.group(1)), Fraction(m.group(2)); A, B = V[:2]; return sum((nn * A[i] + mm * B[i]) / (mm + nn) for i in range(2))
        if "무게중심" in q: A, B, C = V[:3]; return sum((A[i] + B[i] + C[i]) / 3 for i in range(2))
        return None
    if tid == "h3-3-vec-t3":
        m = re.search(r"\[\[abs\(vec\(a\)\)\]\] = (\d+), \[\[abs\(vec\(b\)\)\]\] = (\d+)", q)
        if m:
            p, r = Fraction(m.group(1)), Fraction(m.group(2))
            mm = re.search(r"\[\[abs\(vec\(a\) \+ vec\(b\)\)\]\] = (\d+)", q)
            if mm: return (Fraction(mm.group(1)) ** 2 - p * p - r * r) / 2
            return p * p - r * r
        V = _vcs(q)
        if "서로 수직" in q or "서로 평행" in q or "실수 x" in q:
            mm = re.search(r"\[\[vec\(a\)\]\] = \[\[vcomp\((-?\d+), (-?\d+)\)\]\], \[\[vec\(b\)\]\] = \[\[vcomp\((-?\d+), [kx]\)\]\]", q); a1, a2, b1 = (Fraction(mm.group(i)) for i in (1, 2, 3))
            if "서로 수직" in q: return -a1 * b1 / a2
            if "서로 평행" in q: return a2 * b1 / a1
            val = Fraction(re.search(r"\[\[dot\(vec\(a\), vec\(b\)\)\]\] = (-?\d+)일 때", q).group(1)); return (val - a1 * b1) / a2
        a, b = V[:2]; dot = sum(a[i] * b[i] for i in range(len(a)))
        if "cos θ" in q:
            na, nb = _sqr(sum(t * t for t in a)), _sqr(sum(t * t for t in b)); return None if None in (na, nb) else dot / (na * nb)
        return dot
    if tid == "h3-3-vec-t4":
        m = re.search(r"\[\[abs\(vec\(a\)\)\]\] = (\d+), \[\[abs\(vec\(b\)\)\]\] = (\d+)", q)
        if m:
            p, r = Fraction(m.group(1)), Fraction(m.group(2))
            mm = re.search(r"\[\[dot\(vec\(a\), vec\(b\)\)\]\] = (-?\d+)", q)
            if mm: dot = Fraction(mm.group(1))
            else: s_ = Fraction(re.search(r"\[\[abs\(vec\(a\) \+ vec\(b\)\)\]\] = (\d+)", q).group(1)); dot = (s_ * s_ - p * p - r * r) / 2
            c2 = dot * dot / (p * p * r * r)
        else:
            V = _vcs(q); a, b = V[:2]; dot = sum(a[i] * b[i] for i in range(len(a))); c2 = dot * dot / (sum(t * t for t in a) * sum(t * t for t in b))
        if dot == 0: return Fraction(90)
        base = {Fraction(1): 0, Fraction(3, 4): 30, Fraction(1, 2): 45, Fraction(1, 4): 60}.get(c2)
        if base is None: return None
        return Fraction(base if dot > 0 else 180 - base)
    if tid == "h3-3-vec-t5":
        pl = _plane3(q)
        if q.startswith("두 직선"):
            ds = _dirs(q); u, v = ds[:3], ds[3:6]
            if None in u or None in v: return None
            nu, nv = _sqr(sum(t * t for t in u)), _sqr(sum(t * t for t in v)); dot = sum(u[i] * v[i] for i in range(3))
            return None if None in (nu, nv) else abs(dot) / (nu * nv)
        if q.startswith("직선"):
            ds = _dirs(q)[:3]; n = pl[:3]; j = ds.index(None)
            if "수직일 때" in q:
                i = (j + 1) % 3; s_ = ds[i] / n[i]; return s_ * n[j]
            others = sum(ds[i] * n[i] for i in range(3) if i != j); return -others / n[j]
        if q.startswith("점") and "지나고 법선벡터" in q:
            P = _pts3(q)[0]; n = _vcs(q)[0]; return -sum(n[i] * P[i] for i in range(3))
        P = _pts3(q)
        if q.startswith("점") or q.startswith("중심이"):
            x0 = P[0]; a, b, c, d = pl; nn = _sqr(a * a + b * b + c * c); val = a * x0[0] + b * x0[1] + c * x0[2] + d
            return None if nn is None else abs(val) / nn
        m = re.match(r"구 \[\[(.+?) = (\d+)\]\]", q)
        if m:
            R2 = Fraction(m.group(2)); ctr = []
            for var in "xyz":
                mv = re.search(r"pow\(" + var + r"(?: ([+-]) (\d+))?, ?2\)", m.group(1)); ctr.append(-_sv(mv.group(1), mv.group(2)) if mv.group(1) else Fraction(0))
            a, b, c, d = pl; nn = _sqr(a * a + b * b + c * c); val = a * ctr[0] + b * ctr[1] + c * ctr[2] + d
            if nn is None: return None
            dist = abs(val) / nn; return _sqr(R2 - dist * dist)
        return None
    return None


# ── 세션 5c: 보류 유형(귀납법·역/대우/귀류법·산점도) 검산 ────────────────────────────
_SUPMAP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵏ⁺⁻", "0123456789nk+-")


def _supexpr(text):
    """평문 식(위첨자··· 포함) → sympy. '2ⁿ − 1', 'n(n + 1)', '2ᵏ⁺¹ + 3ᵏ⁻¹', '(k + 1)³'"""
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    t = text.replace("−", "-").replace("·", "*").replace("×", "*").replace("⋯", "")
    t = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵏ⁺⁻]+)", lambda m: "**(" + m.group(1).translate(_SUPMAP) + ")", t)
    t = re.sub(r"\[\[(.+?)\]\]", lambda m: "(" + str(_sym2(m.group(1))) + ")", t)
    return parse_expr(t, transformations=standard_transformations + (implicit_multiplication_application,), local_dict={"n": sp.Symbol("n"), "k": sp.Symbol("k")})


def _lneg(s):
    """조건의 부정 — mkseed_h_extra.neg 와 같은 규칙."""
    rel = {">": "≤", "<": "≥", "≥": "<", "≤": ">", "=": "≠", "≠": "="}
    m = re.fullmatch(r"(.+?) ([<>≤≥=≠]) (.+)", s)
    if m: return f"{m.group(1)} {rel[m.group(2)]} {m.group(3)}"
    if s.endswith("짝수"): return s[:-2] + "홀수"
    if s.endswith("홀수"): return s[:-2] + "짝수"
    if s.endswith(" 아니"): return s[:-4]
    return s + ("이" if _has_jong(s[-1]) else "가") + " 아니"


def _lsent(p, q):
    return p + ("면 " if p.endswith("아니") else "이면 ") + q + ("다" if q.endswith("아니") else "이다")


def _lsplit(S):
    m = re.fullmatch(r"(.+?)(?:이면|면) (.+?)(?:이다|다)", S)
    return (m.group(1), m.group(2)) if m else None


_CONTRA_ASSUME = {
    "√2는 무리수이다": "√2는 유리수이다", "√3은 무리수이다": "√3은 유리수이다", "√5는 무리수이다": "√5는 유리수이다",
    "1 + √2는 무리수이다": "1 + √2는 유리수이다", "2√3은 무리수이다": "2√3은 유리수이다",
    "자연수 n에 대하여 n²이 짝수이면 n은 짝수이다": "n은 홀수이다",
    "자연수 n에 대하여 n²이 3의 배수이면 n은 3의 배수이다": "n은 3의 배수가 아니다",
    "실수 a, b에 대하여 a + b > 0이면 a > 0 또는 b > 0이다": "a ≤ 0이고 b ≤ 0이다",
    "실수 a, b에 대하여 ab = 0이면 a = 0 또는 b = 0이다": "a ≠ 0이고 b ≠ 0이다",
    "소수는 무한히 많다": "소수는 유한개이다",
    "실수 x에 대하여 x² = 2이면 x는 무리수이다": "x는 유리수이다",
    "자연수 n에 대하여 n² + n은 홀수가 아니다": "n² + n은 홀수이다",
    "실수 x에 대하여 x + [[frac(1, x)]] ≥ 2이면 x > 0이다 (단, x ≠ 0)": "x < 0이다",
    "정수 a, b에 대하여 a² + b²이 홀수이면 a, b 중 하나만 홀수이다": "a, b가 모두 홀수이거나 모두 짝수이다",
}


def _opts(q):
    """'A. … B. … ' 보기 → {글자: 문장}"""
    seg = q[q.index("A. "):]
    parts = re.split(r"\s(?=[B-E]\. )", seg)
    return {p[0]: p[3:].strip().rstrip(".") for p in parts if len(p) > 3 and p[1] == "."}



# ── 그림이 있는 고등부 틀(세션 5c) — 발문의 치수·좌표에서 다시 푼다 ────────────────────────────
def _box_pts(q):
    """'AB = w, AD = d, AE = h인 직육면체 ABCD-EFGH' → 꼭짓점 좌표 (figsvg wire 배치)."""
    m = re.search(r"AB = (\d+), AD = (\d+), AE = (\d+)인 직육면체 ABCD-EFGH", q)
    if not m:
        return None
    w, d, h = (Fraction(m.group(i)) for i in (1, 2, 3))
    return {"A": (0, h, 0), "B": (w, h, 0), "C": (w, h, d), "D": (0, h, d), "E": (0, 0, 0), "F": (w, 0, 0), "G": (w, 0, d), "H": (0, 0, d)}


def _v3(P, a, b):
    return tuple(P[b][i] - P[a][i] for i in range(3))


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _d3(u, v):
    return sum(u[i] * v[i] for i in range(3))


def _plane_n(P, name):
    return _cross(_v3(P, name[0], name[1]), _v3(P, name[0], name[2]))


def _hf(tid, q):
    """h3-3-solid · h3-3-conicfig · h3-3-vecfig · h2-1-trigfig — 발문에서 다시 푼다."""
    q = q.replace("−", "-")
    if tid.startswith("h3-3-solid"):
        P = _box_pts(q)
        if P is None:
            return None
        m = re.search(r"선분 ([A-H])([A-H])의 길이", q)
        if m and tid.endswith("t1"):
            u = _v3(P, m.group(1), m.group(2)); return _sqr(_d3(u, u))
        m = re.search(r"꼭짓점 ([A-H])와 직선 ([A-H])([A-H]) 사이의 거리", q)
        if m:
            X, Y, Z = m.groups(); u, v = _v3(P, Y, X), _v3(P, Y, Z)
            return _sqr((_d3(u, u) * _d3(v, v) - _d3(u, v) ** 2) / _d3(v, v))
        m = re.search(r"꼭짓점 ([A-H])와 평면 ([A-H]{4}) 사이의 거리", q)
        if m:
            X, pl = m.groups(); n = _plane_n(P, pl); u = _v3(P, pl[0], X)
            return _sqr(Fraction(_d3(u, n) ** 2, _d3(n, n)))
        m = re.search(r"(삼각형|사각형) ([A-H]{3,4})의 평면 ([A-H]{4}) 위로의 정사영의 넓이", q)
        if m:
            fig, pl = m.group(2), m.group(3)
            const = [i for i in range(3) if len({P[v][i] for v in pl}) == 1]
            if len(const) != 1:
                return None
            ij = [i for i in range(3) if i != const[0]]
            pts = [(P[v][ij[0]], P[v][ij[1]]) for v in fig]
            s2 = sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts)))
            return abs(Fraction(s2)) / 2
        m = re.search(r"두 평면 ([A-H]{4})[와과] ([A-H]{4})가 이루는 각의 크기를 θ라 할 때, (cos|tan) θ의 값", q)
        if m:
            n1, n2 = _plane_n(P, m.group(1)), _plane_n(P, m.group(2))
            c2 = Fraction(_d3(n1, n2) ** 2, _d3(n1, n1) * _d3(n2, n2))
            return _sqr(c2) if m.group(3) == "cos" else _sqr((1 - c2) / c2)
        return None
    if tid.startswith("h3-3-conicfig-t1"):
        m = re.search(r"포물선 \[\[pow\(y,2\) = (\d+)x\]\]", q); p = Fraction(int(m.group(1)), 4)
        pts = re.findall(r"([AB])\((-?\d+), (-?\d+)\)", q)
        if len(pts) != 2 or any(Fraction(y) ** 2 != 4 * p * Fraction(x) for _, x, y in pts):
            return None
        AF, BF = (Fraction(x) + p for _, x, _y in pts)
        if "AF + BF" in q: return AF + BF
        if "AF × BF" in q: return AF * BF
        if "|AF - BF|" in q: return abs(AF - BF)
        return None
    if tid.startswith("h3-3-conicfig-t2") or tid.startswith("h3-3-conicfig-t3"):
        m = re.search(r"frac\(pow\(x,2\), (\d+)\) ([+-]) frac\(pow\(y,2\), (\d+)\) = 1", q); A, B = Fraction(m.group(1)), Fraction(m.group(3)); ell = m.group(2) == "+"
        mc = re.search(r"F\((\d+), 0\), F'\(-(\d+), 0\)", q); c = Fraction(mc.group(1))
        if ell:
            a2, b2 = max(A, B), min(A, B)
            if a2 - b2 != c * c: return None
        else:
            a2, b2 = A, B
            if A + B != c * c: return None
        a = _sqr(a2)
        if a is None: return None
        mm = re.search(r"점 P의 x좌표가 (\d+)일 때, 선분 PF의 길이", q)
        if mm:
            x = Fraction(mm.group(1)); y2 = b2 * (1 - x * x / a2) if ell else b2 * (x * x / a2 - 1)
            return _sqr(y2)
        mk = re.search(r"PF(')? = (\d+)일 때", q); k = Fraction(mk.group(2)) if mk else None
        if "둘레의 길이" in q:
            return 2 * a + 2 * c if ell else 2 * k + 2 * a + 2 * c
        if mk and ("선분 PF'의 길이" in q or "선분 PF의 길이" in q):
            return 2 * a - k if ell else k + 2 * a
        return None
    if tid.startswith("h3-3-vecfig"):
        m = re.search(r"vec\(a\)\]\] = \[\[vcomp\((-?\d+), (-?\d+)\)\]\], \[\[vec\(b\)\]\] = \[\[vcomp\((-?\d+), (-?\d+)\)\]\]", q)
        a = (Fraction(m.group(1)), Fraction(m.group(2))); b = (Fraction(m.group(3)), Fraction(m.group(4)))
        s = (a[0] + b[0], a[1] + b[1]); dot = a[0] * b[0] + a[1] * b[1]
        na2, nb2, ns2 = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2, s[0] ** 2 + s[1] ** 2
        if "모든 성분의 합" in q: return s[0] + s[1]
        if "[[dot(vec(a), vec(b))]]의 값" in q: return dot
        if "[[pow(abs(vec(a) + vec(b)), 2)]]" in q: return ns2
        if "[[dot((vec(a) + vec(b)), (vec(a) - vec(b)))]]" in q: return na2 - nb2
        if "[[abs(vec(a) + vec(b))]]의 값" in q: return _sqr(ns2)
        if "[[abs(vec(a))]] cos θ의 값" in q:
            nb = _sqr(nb2); return dot / nb if nb else None
        if "cos θ의 값" in q:
            na, nb = _sqr(na2), _sqr(nb2); return dot / (na * nb) if na and nb else None
        return None
    if tid.startswith("h2-1-trigfig"):
        m = re.search(r"최댓값이 (-?\d+), 최솟값이 (-?\d+)이고 주기가 (.+?)일 때, 상수 a, b, c에 대하여 (.+?)의 값", q)
        M, mn, per, ask = Fraction(m.group(1)), Fraction(m.group(2)), m.group(3), m.group(4)
        tpi = {"π": Fraction(1), "2π": Fraction(2), "[[frac(pi, 2)]]": Fraction(1, 2), "4π": Fraction(4), "3π": Fraction(3)}.get(per)
        if tpi is None: return None
        a, c, b = (M - mn) / 2, (M + mn) / 2, 2 / tpi
        return {"a + b + c": a + b + c, "abc": a * b * c, "ab": a * b, "b + c": b + c}.get(ask)
    return None

def check_letters(it):
    """보기 글자(A~E) 답 틀: 역·이·대우 / 참인 대우 / 귀류법 가정 / 산점도 상관. True/False, 해당 없으면 None."""
    tid, q, a = it["template_id"], it["question"], it["answer"]
    if tid.startswith("h1-2-logic2-t1") or tid.startswith("h1-2-logic2-t2"):
        m = re.match(r"명제 '(.+?)'(?:의 (역|이|대우)를|가 참일 때)", q)
        if not m: return False
        pq = _lsplit(m.group(1))
        if not pq: return False
        p, qq = pq; np_, nq = _lneg(p), _lneg(qq)
        want = {"역": _lsent(qq, p), "이": _lsent(np_, nq), "대우": _lsent(nq, np_)}[m.group(2) or "대우"]
        opts = _opts(q)
        return opts.get(a) == want
    if tid.startswith("h1-2-logic2-t3"):
        m = re.match(r"명제 '(.+?)'를 귀류법으로", q)
        want = _CONTRA_ASSUME.get(m.group(1)) if m else None
        return want is not None and _opts(q).get(a) == want
    if tid.startswith("m3-2-scatter-t1"):
        pts = [(int(x), int(y)) for x, y in re.findall(r"\((\d+), (\d+)\)", q)]
        n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
        sxy = sum((p[0] - mx) * (p[1] - my) for p in pts); sxx = sum((p[0] - mx) ** 2 for p in pts); syy = sum((p[1] - my) ** 2 for p in pts)
        r = sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0
        want = "양의 상관관계가 있다" if r > 0.5 else "음의 상관관계가 있다" if r < -0.5 else "상관관계가 없다" if abs(r) < 0.3 else None
        return want is not None and _opts(q).get(a) == want
    return None


def _hx(tid, q):
    """h2-1-induct · m3-2-scatter 수 답 — 발문에서 다시 푼다."""
    import sympy as sp
    n, k = sp.symbols("n k")
    if tid == "h2-1-induct-t1":
        m = re.search(r"등식 (.+?) 이 성립함을", q); lhs, rhs = m.group(1).rsplit(" = ", 1); R = _supexpr(rhs)
        f = lambda a: sp.nsimplify(R.subs(n, a + 1) - R.subs(n, a))  # noqa: E731
        g = lambda b: sp.nsimplify(R.subs(n, b + 1))  # noqa: E731
        mm = re.search(r"f\((\d+)\) ([+×]) g\((\d+)\)의 값", q); A, B = int(mm.group(1)), int(mm.group(3))
        v = f(A) + g(B) if mm.group(2) == "+" else f(A) * g(B); return _spv(v)
    if tid == "h2-1-induct-t2":
        m = re.search(r"명제 '(.+?)[은는] (\d+)의 배수이다'", q); P = _supexpr(m.group(1))
        mm = re.search(r"= (\d+)\(.+?\) \+ \(가\)", q); mult = int(mm.group(1)) if mm else 1
        f = lambda a: sp.nsimplify(P.subs(n, a + 1) - mult * P.subs(n, a))  # noqa: E731
        mm = re.search(r"f\((\d+)\)(?: \+ f\((\d+)\))?의 값", q); v = f(int(mm.group(1))) + (f(int(mm.group(2))) if mm.group(2) else 0); return _spv(v)
    if tid == "h2-1-induct-t3":
        m = re.search(r"부등식 (.+?) 이 성립함을", q); lhs, rhs = m.group(1).split(" > "); R = _supexpr(rhs)
        mm = re.search(r"양변에 (.+?)[을를] 곱하면", q); c = _supexpr(mm.group(1))
        f = lambda a: sp.nsimplify((c * R.subs(n, k)).subs(k, a) - R.subs(n, a + 1))  # noqa: E731
        mm = re.search(r"f\((\d+)\)(?: \+ f\((\d+)\))?의 값", q); v = f(int(mm.group(1))) + (f(int(mm.group(2))) if mm.group(2) else 0); return _spv(v)
    if tid.startswith("m3-2-scatter-t2") or tid.startswith("m3-2-scatter-t3"):
        pts = [(int(x), int(y)) for x, y in re.findall(r"\((\d+), (\d+)\)", q)]; N = len(pts)
        m = re.search(r"모두 (\d+)점 이상인 학생 수", q)
        if m: a = int(m.group(1)); return Fraction(sum(1 for x, y in pts if x >= a and y >= a))
        if re.search(r"점수가 .+? 점수보다 높은 학생 수를 구하시오", q): return Fraction(sum(1 for x, y in pts if y > x))
        m = re.search(r"점수가 (\d+)점 미만인 학생 수", q)
        if m: a = int(m.group(1)); return Fraction(sum(1 for x, y in pts if x < a))
        if "점수가 같은 학생 수" in q: return Fraction(sum(1 for x, y in pts if x == y))
        if "p − q의 값" in q: return Fraction(sum(1 for x, y in pts if y > x) - sum(1 for x, y in pts if y < x))
        if "합이 150점 이상인 학생은 전체의 몇 %" in q: return Fraction(sum(1 for x, y in pts if x + y >= 150) * 100, N)
        if "점수의 평균" in q: return Fraction(sum(x for x, y in pts), N)
        return None
    return None


def check_hs(it):
    """고등부 문자열 답(범위) 틀. True/False, 해당 없으면 None."""
    tid, q, a = it["template_id"], it["question"], it["answer"]
    if tid == "h1-1-quad-t1":
        m = re.match(r"x에 대한 이차방정식 x² \+ \(k ([+−]) (\d+)\)x \+ (\d+) = 0이 서로 다른 두 허근", q); b = _sv(m.group(1), m.group(2)); c = Fraction(m.group(3)); r = _isqrt(c)
        if r is None: return False
        lo, hi = -2 * r - b, 2 * r - b; ma = re.fullmatch(r"(-?\d+) < k < (-?\d+)", a)
        return bool(ma) and Fraction(ma.group(1)) == lo and Fraction(ma.group(2)) == hi
    if tid == "h1-1-ineq-t3":
        m = re.match(r"이차부등식 x² ([+−]) (\d*)x ([+−]) (\d+) (<|≥) 0의 해", q); b = _sv(m.group(1), m.group(2) or "1"); c = _sv(m.group(3), m.group(4))
        rs = sorted(x for x in range(-30, 31) if x * x + b * x + c == 0)
        if len(rs) != 2: return False
        want = f"{rs[0]} < x < {rs[1]}" if m.group(5) == "<" else f"x ≤ {rs[0]} 또는 x ≥ {rs[1]}"
        return a == want
    if tid == "h1-1-ineq-t6":
        m = re.match(r"모든 실수 x에 대하여 부등식 x² \+ \(k ([+−]) (\d+)\)x \+ (\d+) > 0이 성립", q); b = _sv(m.group(1), m.group(2)); c = Fraction(m.group(3)); r_ = _isqrt(c)
        if r_ is None: return False
        ma = re.fullmatch(r"(-?\d+) < k < (-?\d+)", a); return bool(ma) and Fraction(ma.group(1)) == -2 * r_ - b and Fraction(ma.group(2)) == 2 * r_ - b
    if tid == "h1-1-quadfn-t1":
        m = re.match(r"이차함수 y = x² ([+−]) (\d*)x ([+−]) (\d+)의 그래프와 직선 y = (-?\d*)x \+ k가 (만나지 않을|서로 다른 두 점에서 만날) 때", q); av = _sv(m.group(1), m.group(2) or "1"); b = _sv(m.group(3), m.group(4)); mm = _coef(m.group(5))
        T = b - (av - mm) ** 2 / 4; op = "<" if m.group(6) == "만나지 않을" else ">"; ma = re.fullmatch(r"k ([<>]) (-?\d+)", a)
        return bool(ma) and ma.group(1) == op and Fraction(ma.group(2)) == T
    return None


def _strip25(n):
    n = int(n)
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5
    return n


_SUP_STAR = {ord(a): f"**{d} " for a, d in zip("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")}


def _sy(text):
    """평문·마커 식 → sympy 식. 위첨자·pow·frac·−·×·÷ 를 파이썬 문법으로 바꾸고 암시적 곱(3x, xy, 2(…))을 허용한다."""
    import sympy as sp
    from sympy.parsing.sympy_parser import implicit_multiplication_application, parse_expr, standard_transformations
    t = re.sub(r"\[\[|\]\]", "", text).replace("−", "-").replace("×", "*").replace("÷", "/").translate(_SUP_STAR)
    t = re.sub(r"pow\(([a-z]),\s*(\d+)\)", r"\1**\2 ", t)
    t = re.sub(r"frac\(([^()]*?),\s*([^()]*?)\)", r"((\1)/(\2))", t)
    t = t.replace("□", "BOX")
    return parse_expr(t, transformations=standard_transformations + (implicit_multiplication_application,), local_dict={"x": sp.Symbol("x"), "y": sp.Symbol("y")})


def check_polyexpr(it):
    """식이 답인 m2-1 틀(단항식 □·잘못 계산, 다항식 잘못 계산·도형의 변): 발문을 sympy 로 되읽어 답과 대조. True/False, 해당 없으면 None."""
    tid, q = it["template_id"], it["question"]
    if not tid.startswith(("m2-1-monomial-t3", "m2-1-monomial-t4", "m2-1-monomial-t5", "m2-1-polynomial-t4", "m2-1-polynomial-t5")):
        return None
    import sympy as sp
    try:
        if tid.startswith("m2-1-monomial-t3"):
            m = re.match(r"□ × \((.+?)\) = (\[\[.+?\]\])일 때", q); want = _sy(m.group(2)) / _sy(m.group(1))
        elif tid.startswith("m2-1-monomial-t4"):
            m = re.match(r"(\[\[.+?\]\]) ÷ □ = (.+?)일 때", q); want = _sy(m.group(1)) / _sy(m.group(2))
        elif tid.startswith("m2-1-monomial-t5"):
            m = re.match(r"어떤 단항식을 (.+?)[으]?로 나누어야 할 것을 잘못하여 곱했더니 (\[\[.+?\]\])이 되었다", q); want = _sy(m.group(2)) / _sy(m.group(1)) ** 2
        elif tid.startswith("m2-1-polynomial-t4"):
            m = re.match(r"어떤 다항식(?:에서|에) (.+?)[을를] (더해야|빼야) 할 것을 잘못하여 (.+?)[을를] (뺐더니|더했더니) (.+?)[이가] 되었다", q)
            A, B = _sy(m.group(1)), _sy(m.group(5)); i = 1 if m.group(2) == "더해야" else -1; want = B + 2 * i * A
        else:
            m = re.match(r"넓이가 (\[\[.+?\]\])인 (직사각형|삼각형|평행사변형)의 .+?가 (\S+)일 때", q)
            want = (2 if m.group(2) == "삼각형" else 1) * _sy(m.group(1)) / _sy(m.group(3))
        return sp.simplify(sp.cancel(want - _sy(it["answer"]))) == 0
    except Exception:                                   # noqa: BLE001
        return False


def check_ineq2(it):
    """m2-1-ineq-solve-2-t3(a의 범위)·m2-1-ineq-apply-t4(x의 범위): 발문에서 되읽어 문자열 답과 대조."""
    tid, q = it["template_id"], it["question"]
    if not tid.startswith(("m2-1-ineq-solve-2-t3", "m2-1-ineq-apply-t4")):
        return None
    try:
        if tid.startswith("m2-1-ineq-solve-2-t3"):
            m = re.match(r"x에 대한 일차부등식 (\d+)x − a ([≤<]) (\d*)x ([+−]) (\d+)[을를] 만족하는 자연수 x가 (\d+)개", q)
            p, op, qv, r, n = int(m.group(1)), m.group(2), int(_coef(m.group(3))), int(m.group(5)) * (1 if m.group(4) == "+" else -1), int(m.group(6))
            if p - qv != 1:
                return False
            lo, hi = n - r, n + 1 - r
            want = f"{lo} ≤ a < {hi}" if op == "≤" else f"{lo} < a ≤ {hi}"
        else:
            m = re.match(r".+?가 (\d+) cm이고 .+?x cm인 (삼각형|직사각형)의 넓이가 (\d+) cm²(.+?), x의 값의 범위", q)
            b, kk, A = int(m.group(1)), 2 if m.group(2) == "삼각형" else 1, int(m.group(3)); k = Fraction(kk * A, b)
            want = f"x {'≥' if '이상' in m.group(4) else '>'} {k.numerator if k.denominator == 1 else k}"
        return re.sub(r"\s+", " ", it["answer"]).strip() == want
    except Exception:                                   # noqa: BLE001
        return False


def _lineq(text):
    """'2x − 3y = 5' / 'x + y = 5' / 'ax + 2y = 7'(a는 무시) → (x의 계수, y의 계수, 상수)"""
    m = re.match(r"\s*(-?\d*)x ([+−]) (\d*)y = (-?\d+)\s*$", text.replace("−", "−"))
    if not m:
        raise ValueError(text)
    b = _coef(m.group(3)) * (1 if m.group(2) == "+" else -1)
    return (_coef(m.group(1)), b, Fraction(m.group(4)))


def _solve2(e1, e2):
    """두 일차식 (a, b, c): ax + by = c 를 크래머 공식으로 푼다."""
    a1, b1, c1 = [Fraction(v) for v in e1]; a2, b2, c2 = [Fraction(v) for v in e2]
    d = a1 * b2 - a2 * b1
    return (c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d


def _fac(n):
    d, m, p = {}, n, 2
    while p * p <= m:
        while m % p == 0:
            m //= p; d[p] = d.get(p, 0) + 1
        p += 1
    if m > 1: d[m] = d.get(m, 0) + 1
    return d


def _ndiv(n):
    out = 1
    for e in _fac(n).values(): out *= e + 1
    return out


def _facmap(s):
    """'2ᵃ × 3² × 5' → {2: 'a', 3: 2, 5: 1} (위첨자 되읽기, 미지수 지수는 문자)."""
    out = {}
    for term in s.strip().split(" × "):
        m = re.fullmatch(r"(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]*|ᵃ|ᵇ)", term.strip())
        e = m.group(2)
        out[int(m.group(1))] = "a" if e == "ᵃ" else ("b" if e == "ᵇ" else _sup(e))
    return out


def _facval(s):
    v = 1
    for p, e in _facmap(s).items(): v *= p ** e
    return v


def _bracket_data(q):
    """'[ 12, 15, x, 9 ]' → [12, 15, None, 9]."""
    m = re.search(r"\[ (.+?) \]", q)
    return [None if t.strip() == "x" else Fraction(t.strip()) for t in m.group(1).split(",")] if m else []


def _freq_list(q):
    """'각 계급의 도수가 차례로 3명, 5명, A명, 4명, 2명일 때' → 발문에 적힌 도수(문자는 건너뜀)."""
    m = re.search(r"차례로 (.+?)(?:일 때|이고)", q)
    return [Fraction(x) for x in re.findall(r"(\d+)명", m.group(1))] if m else []


def _ft_rows(it):
    """도수분포표 figure → [(lo, hi, 도수)] — 합계 행·문자 도수 행은 뺀다."""
    out = []
    for f in it.get("figure") or []:
        if f.get("fn") != "table":
            continue
        for r in f["args"]["rows"]:
            m = re.match(r"(\d+(?:\.\d+)?) 이상 ~ (\d+(?:\.\d+)?) 미만", str(r[0]))
            if m and re.fullmatch(r"\d+", str(r[1])):
                out.append((Fraction(m.group(1)), Fraction(m.group(2)), Fraction(str(r[1]))))
    return out


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


def _given1(q):
    """'[[angle(X) = deg(v)]]' 한 마커 꼴의 마지막 주어진 각 → (이름, 값)."""
    m = re.findall(r"\[\[angle\(([A-Z]+)\) = deg\((\d+)\)\]\]", q)
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
    if not it["template_id"].startswith(("m2-1-ineq-solve-t1", "m2-1-ineq-solve-t2", "m2-1-ineq-solve-2-t1", "m2-1-ineq-solve-2-t2")):
        return None
    import mathir
    m = re.search(r"일차부등식 (.+?) ([<>≤≥]) (.+?)[을를] 푸시오", it["question"])
    if not m:
        return False
    strip = lambda t: re.sub(r"\[\[|\]\]", "", t)          # noqa: E731 — 분수 마커는 벗기고 mathir 식으로
    L, R = mathir.parse(strip(m.group(1)))[0], mathir.parse(strip(m.group(3)))[0]
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
            if isinstance(a.get("angle"), (int, float)) and "중심각" in it["question"]:
                qn = nums(it["question"])
                if qn and qn[0] != a["angle"]:
                    bad("F2-sector 각≠문면", it, f"{a['angle']} vs {qn[0]}")
        elif fn == "numline":
            for p in a.get("points", []) or []:
                if not (a["min"] <= p["x"] <= a["max"]):
                    bad("F3-numline 점이 범위 밖", it, str(p))
        elif fn == "coordplane":
            lines = a.get("lines", []) or []
            for ln in lines:
                if "points" in ln and len(lines) == 1 and len(ln["points"]) == 2 and ln.get("style") != "dashed":   # 직선 하나에 점들이 놓인 틀만 (다각형·수선은 제외)
                    (x1, y1), (x2, y2) = ln["points"][:2]
                    for p in a.get("points", []) or []:
                        x, y = p["coord"]
                        if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) > 1e-6:      # 09-13: 분수 좌표(소수 변환)의 오차 허용
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
    if m3 and not re.search(r"×\s*\(?-?1\)?\s*[+−=),]", m3.group(0)):   # 'a × 1 + b'·'a × 1 = a'·'(3 × 2 × 1)'·'2 × x × 1, 즉' 대입·계승 문맥은 허용
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
        if pos is None:
            pos = check_linexpr(it)
        if pos is None:
            pos = check_polyexpr(it)
        if pos is None:
            pos = check_ineq2(it)
        if pos is None:
            pos = check_m3str(it)
        if pos is None:
            pos = check_m3trig(it)
        if pos is None:
            pos = check_hs(it)
        if pos is None:
            pos = check_letters(it)
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
