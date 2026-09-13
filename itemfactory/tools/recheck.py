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
    return "skip"


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
        if pos is None:
            pos = check_linexpr(it)
        if pos is None:
            pos = check_polyexpr(it)
        if pos is None:
            pos = check_ineq2(it)
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
