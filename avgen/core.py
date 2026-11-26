# ashrain.out — 학년별 해설 액자 생성기 공용 (core.py)
# 문항 = { no, st, q, ans, plan, planTag?, lines:[{pre?, s, memo?}], fig?, ap, omr }
# 글자는 무대 수식 문법(draw.jsx MText): {분자/분모} · ^{위} · _{아래} · √{속} · ‹강조› · 홀로 선 소문자 = 이탤릭
import re, random, json, math
from fractions import Fraction as Fr

MI = "−"   # 빼기 기호(U+2212)

# ── 수 → 글자 ────────────────────────────────────────────────────────────────
def N(v):
    """정수 · 분수(가분수 그대로) → '3' · '−3' · '{3/4}' · '−{3/4}'"""
    if isinstance(v, float):
        v = Fr(v).limit_denominator(10**6)
    if isinstance(v, Fr):
        if v.denominator == 1:
            v = v.numerator
        else:
            s = "{%d/%d}" % (abs(v.numerator), v.denominator)
            return (MI if v < 0 else "") + s
    v = int(v)
    return (MI + str(-v)) if v < 0 else str(v)

def NP(v):
    """음수면 괄호: (−3)"""
    s = N(v)
    return f"({s})" if s.startswith(MI) else s

def SG(v):
    """부호를 붙여 괄호: (+3) · (−{1/2})"""
    s = N(v)
    return f"({s})" if s.startswith(MI) else f"(+{s})"

def MX(v):
    """양의 분수 → 대분수 '2{1/4}' (진분수는 '{3/4}', 정수는 '3')"""
    v = Fr(v)
    assert v >= 0
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    f = "{%d/%d}" % (r, v.denominator)
    return (str(w) + f) if w else f

def MXu(w, n, d):
    """약분하지 않은 대분수 그대로 — (2, 2, 6) → '2{2/6}'"""
    if n == 0:
        return str(w)
    return (str(w) if w else "") + "{%d/%d}" % (n, d)

def DEC(v):
    """유한소수 → '0.75' (분수도 받음)"""
    v = Fr(v)
    d = v.denominator
    k = 0
    while d % 10 != 0 and d != 1:
        if d % 2 == 0 or d % 5 == 0:
            break
        raise ValueError("유한소수 아님")
    for k in range(0, 12):
        if (v * 10**k).denominator == 1:
            break
    else:
        raise ValueError("유한소수 아님")
    s = f"{abs(v.numerator) * 10**k // v.denominator:0{k + 1}d}"
    if k:
        s = s[:-k] + "." + s[-k:]
    return (MI if v < 0 else "") + s

def com(n):
    """천 단위 쉼표"""
    return f"{n:,}".replace("-", MI)

def sup(e):
    """지수 → 위 첨자 글자"""
    return "^{" + str(e).replace("-", MI) + "}"

def mono(c, var="x", e=1, first=False):
    """항 하나: 계수 c · 문자 var^e → '3x^{2}' · '− x' (first 면 앞 부호를 붙여 쓴다)"""
    c = Fr(c)
    if c == 0:
        return ""
    sgn = MI if c < 0 else "+"
    a = abs(c)
    if e == 0 or not var:
        body = N(a)
    else:
        cs = "" if a == 1 else N(a)
        body = cs + var + ("" if e == 1 else sup(e))
    if first:
        return (MI if c < 0 else "") + body
    return f" {sgn} {body}"

def poly(cs, var="x"):
    """높은 차수부터의 계수 목록 → '2x^{3} − 3x + 1'"""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        if c == 0:
            continue
        out += mono(c, var, deg - i, first=(out == ""))
    return out or "0"

def lin(a, b, var="x"):
    """ax + b"""
    return poly([a, b], var)

# ── 조사 ────────────────────────────────────────────────────────────────────
_NUM_BAT = set("013678")          # 영 일 삼 육 칠 팔 — 받침 있음 (0 은 '영'으로 읽음)
def _has_batchim(w):
    w = str(w)
    m = re.search(r"\{([^{}/]*)/([^{}]*)\}\s*$", w)       # 분수는 분자를 마지막에 읽는다 (4분의 3)
    if m:
        w = m.group(1)
    if re.search(r"(\^\{[^{}]*\}|[²³])$", w):                  # x^{2} → 엑스 제곱 — 받침 있음
        return True
    w = re.sub(r"[\s)\]}'\"’”]+$", "", w)
    if not w:
        return False
    ch = w[-1]
    if "가" <= ch <= "힣":
        return (ord(ch) - 0xAC00) % 28 != 0
    if ch.isdigit():
        return ch in _NUM_BAT
    if ch in "LMNR":
        return True
    return False

def _is_rieul(w):
    w = str(w)
    m = re.search(r"\{([^{}/]*)/([^{}]*)\}\s*$", w)
    if m:
        w = m.group(1)
    w = re.sub(r"[\s)\]}'\"’”]+$", "", w)
    ch = w[-1] if w else ""
    if "가" <= ch <= "힣":
        return (ord(ch) - 0xAC00) % 28 == 8
    return ch in "178L"           # 일 칠 팔 · 엘

def J(w, a, b):
    """J('3', '은', '는') → '3은'"""
    return f"{w}{a if _has_batchim(w) else b}"

def RO(w):
    """(으)로 — ㄹ 받침 · 받침 없음은 '로'"""
    return f"{w}{'으로' if _has_batchim(w) and not _is_rieul(w) else '로'}"

# ── 판서 줄 ──────────────────────────────────────────────────────────────────
def L(s, pre=None, memo=None):
    d = {"s": s}
    if pre:
        d["pre"] = pre
    if memo:
        d["memo"] = memo
    return d

# ── 판서 검산: 「=」로 이은 계산식이 같은 값인지 ───────────────────────────────
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, factorial_notation

TRANS = standard_transformations + (implicit_multiplication_application, factorial_notation)
SYMS = {c: sp.Symbol(c) for c in "abcdkmnpqrstuvwxyz"}
SKIP = re.compile(r"[가-힣]|f\(|g\(|h\(|f'|g'|log|sin|cos|tan|ln|lim|Σ|∫|e\^|α|β|…|⟪|\?|□|△|○|㉠|㉡|%|:|ⁿ|[A-Z]")

def _match(s, i):
    """s[i] == '{' 의 짝 '}' 자리"""
    d = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            d += 1
        elif s[j] == "}":
            d -= 1
            if d == 0:
                return j
    return -1

def to_py(s, mixed=False):
    """무대 수식 글자 → sympy 식 글자 (못 바꾸면 None)"""
    s = s.strip().replace("`", "")
    s = re.sub(r"\s*(cm²|cm³|m²|m³|km²|cm|mm|km|kg|mL|L|g|m)\s*$", "", s)
    s = s.replace("‹", "").replace("›", "").replace("°", "")
    s = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s)      # 천 단위 쉼표
    s = re.sub(r"÷\s*(\d*(?:[a-z](?:\^\{[^{}]*\}|[²³])?)+)", r"÷ (\1)", s)   # ÷ 단항식은 통째로 나눈다(중학교 관례)
    # 조합 기호
    s = re.sub(r"_\{(\d+)\}C_\{(\d+)\}", r"binomial(\1,\2)", s)
    s = re.sub(r"_\{(\d+)\}P_\{(\d+)\}", r"pm(\1,\2)", s)
    s = re.sub(r"_\{(\d+)\}H_\{(\d+)\}", r"binomial(\1+\2-1,\2)", s)
    s = re.sub(r"_\{(\d+)\}Π_\{(\d+)\}", r"(\1)**(\2)", s)
    if SKIP.search(s):
        return None
    out = ""
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "{":
            j = _match(s, i)
            if j < 0:
                return None
            inner = s[i + 1:j]
            k = inner.find("/")
            if k < 0:
                return None
            a, b = to_py(inner[:k], mixed), to_py(inner[k + 1:], mixed)
            if a is None or b is None:
                return None
            frac = f"(({a})/({b}))"
            if mixed and out and out[-1].isdigit():
                m = re.search(r"(\d+)$", out)
                w = m.group(1)
                out = out[:m.start()] + f"({w}+{frac})"
            else:
                out += frac
            i = j + 1
            continue
        if ch == "^" and i + 1 < len(s) and s[i + 1] == "{":
            j = _match(s, i + 1)
            a = to_py(s[i + 2:j], mixed)
            if a is None:
                return None
            out += f"**({a})"
            i = j + 1
            continue
        if ch == "√" and i + 1 < len(s) and s[i + 1] == "{":
            j = _match(s, i + 1)
            a = to_py(s[i + 2:j], mixed)
            if a is None:
                return None
            out += f"sqrt({a})"
            i = j + 1
            continue
        if ch == "√":
            m = re.match(r"√(\d+)", s[i:])
            if not m:
                return None
            out += f"sqrt({m.group(1)})"
            i += len(m.group(0))
            continue
        out += {"−": "-", "×": "*", "÷": "/", "·": "*", "²": "**2", "³": "**3", "[": "(", "]": ")", "π": " pi "}.get(ch, ch)
        i += 1
    out = re.sub(r"(\d+)\.(\d+)", lambda m: f"({int(m.group(1) + m.group(2))}/{10 ** len(m.group(2))})", out)
    out = re.sub(r"!\s+(?=[\d(])", "!*", out)
    if re.search(r"[^0-9a-z+\-*/()., !]", out.replace("binomial", "").replace("sqrt", "").replace("pm", "")):
        return None
    return out

def val(s, mixed=False, sub=None):
    py = to_py(s, mixed)
    if py is None or not py.strip():
        return None
    try:
        e = parse_expr(py, local_dict={**SYMS, "pm": sp.ff, "binomial": sp.binomial, "sqrt": sp.sqrt, "pi": sp.pi}, transformations=TRANS)
    except Exception:
        return None
    if not isinstance(e, sp.Basic):
        return None
    if sub:
        e = e.subs({SYMS[k]: v for k, v in sub.items() if k in SYMS})
    return e

def _num_tail(side):
    """'자연수끼리 2 + 1' → '2 + 1' (한글 앞말 떼기)"""
    m = re.search(r"[가-힣][^가-힣]*$", side)
    if not m:
        return side
    rest = side[m.start() + 1:]
    return rest

def chain_check(s, mixed=False, sub=None, ident=False):
    """판서 한 줄 → (본 등식 수, 틀린 것 목록). → 로 나눈 마디마다 = 로 이은 쪽을 비교한다.
    sub: 문자에 넣을 값(방정식의 해) · ident: 항등식이면 아무 값이나 넣어 본다."""
    checked, bad = 0, []
    for m in re.finditer(r"(\d+) ÷ (\d+) = (\d+) … (\d+)", s):      # 나머지 있는 나눗셈
        a, b, q, r = map(int, m.groups())
        checked += 1
        if not (a == b * q + r and 0 <= r < b):
            bad.append(f"나머지 틀림: {m.group(0)}")
    s = s.replace("≠", "=/=")
    for part in re.split(r"→|⇒|,\s(?=[^)]*(?:\(|$))", s):
        if "=/=" in part:
            continue
        sides = [re.split(r"<|>|≤|≥", x)[0] for x in part.split("=")]
        if len(sides) < 2:
            continue
        vals = []
        for side in sides:
            t = _num_tail(side).strip()
            v = val(t, mixed, sub)
            if v is not None and ident and v.free_symbols:
                v = v.subs({sym: sp.Rational(7, 3) + i for i, sym in enumerate(sorted(v.free_symbols, key=str))})
            vals.append(v if (v is not None and not v.free_symbols) else None)
        for i in range(len(vals) - 1):
            a, b = vals[i], vals[i + 1]
            if a is None or b is None:
                continue
            checked += 1
            if sp.simplify(a - b) != 0:
                bad.append(f"{sides[i].strip()} ≠ {sides[i + 1].strip()}  ({a} vs {b})")
    return checked, bad

# ── 빼기 기호 고르기: 수식 자리의 ASCII '-' → '−'(U+2212) ─────────────────────
def fixminus(t):
    if not isinstance(t, str):
        return t
    t = re.sub(r"−\s?-(?=[\d(a-zA-Z{√])", lambda m: "+" + (" " if " " in m.group(0) else ""), t)   # − -2 → + 2
    t = re.sub(r"\+ -(?=[\d(a-zA-Z{√])", "− ", t)                                                # + -2a → − 2a
    t = re.sub(r"(?<![\w)\]}])-(?=[\d(a-zA-Z{√.])", "−", t)
    return t

# ── 세트 ─────────────────────────────────────────────────────────────────────
class Set:
    def __init__(self, key, title, short, stages, *, mixed=False, pp=10, note="", tips=None, code=None, unit=""):
        self.key, self.title, self.short, self.stages = key, title, short, stages
        self.mixed, self.pp, self.note, self.tips, self.code, self.unit = mixed, pp, note, tips or {}, code, unit
        self.items = []
        self.seen = set()
        self.checks = 0

    def add(self, st, q, ans, plan, lines, fig=None, *, ap=None, omr="num", planTag=None, sub=None, ident=False, key=None, qfig=False, pp=None, dupq=False):
        q, ans, plan, ap = fixminus(q), fixminus(ans), fixminus(plan), fixminus(ap)
        lines = [{k: fixminus(v) for k, v in ln.items()} for ln in lines]
        q = re.sub(r"(\d) (`?(?:cm²|cm³|cm|mm|km|m²|m|kg|g|mL|L|원|개|명|대|장|자루|봉지|시간|분|초|살|권|번째|번|배|칸|묶음|°))", "\\1\u00a0\\2", q)
        k = f"{st}|{key or q}"
        if k in self.seen or (("Q|" + q) in self.seen and not dupq):      # dupq: 자료가 그림에 있는 문항 — 발문이 같아도 그림(key)이 다르면 다른 문항
            return False
        self.seen.add(k)
        self.seen.add("Q|" + q)
        it = {"no": len(self.items) + 1, "st": st, "q": q, "ans": ans, "plan": plan, "lines": lines}
        if planTag:
            it["planTag"] = planTag
        if fig:
            it["fig"] = fig
        it["ap"] = plain(ap) if ap is not None else plain(ans)
        it["omr"] = omr
        if qfig:
            it["qf"] = 1
        # 판서 검산
        for ln in lines:
            c, bad = chain_check(ln["s"], self.mixed, sub, ident)
            assert not bad, f"{self.key} {it['no']} 판서 계산 틀림: {ln['s']} → {bad}"
            self.checks += c
        c, bad = chain_check(plan, self.mixed, sub, ident)
        assert not bad, f"{self.key} {it['no']} 방침 계산 틀림: {plan} → {bad}"
        self.items.append(it)
        return True

    def count(self, st):
        return sum(1 for it in self.items if it["st"] == st)

def plain(s):
    """빠른 정답 · 등록 정보용 글자 — {3/4} → 3/4, 2{1/4} → 2 1/4, ^{2} → ^2"""
    s = re.sub(r"\u20D7\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"√\{(\d+)\}", r"√\1", s)
    s = re.sub(r"√\{([^{}]*)\}", r"√(\1)", s)
    s = re.sub(r"(\d)\{(\d+)/(\d+)\}", r"\1 \2/\3", s)
    def _fr(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        a = a if re.fullmatch(r"[\w−√.^]+", a) else f"({a})"
        b = b if re.fullmatch(r"[\w−√.^]+", b) else f"({b})"
        return f"{a}/{b}"
    s = re.sub(r"\{([^{}]*)/([^{}]*)\}", _fr, s)
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: "^" + (m.group(1) if len(m.group(1)) == 1 else f"({m.group(1)})"), s)
    s = re.sub(r"_\{([^{}]*)\}", r"\1", s)
    s = s.replace("‹", "").replace("›", "").replace("`", "").replace("⟦", "(").replace("⟧", ")")
    return s

SEED_SHIFT = 0          # 회차(주차별 기초 다지기)를 만들 때 같은 생성기에서 새 문항을 뽑으려고 바꾼다 — 0 이면 유형별 문제 세트 그대로

def rng(seed):
    return random.Random(seed + 7919 * SEED_SHIFT)

def fill(S, st, n, gen, tries=4000):
    """gen() 가 add 하면 True — n 개 채울 때까지"""
    k0 = S.count(st)
    t = 0
    while S.count(st) < k0 + n:
        t += 1
        assert t < tries, f"{S.key} {st}단계 생성 실패 ({S.count(st) - k0}/{n})"
        gen()

# ── 단항식 글자 ─────────────────────────────────────────────────────────────
def monom(c, pw, order="abxy", first=True):
    """계수 c · 문자 지수 pw({'a': 2, 'b': 1}) → '−6a^{3}b^{4}' (지수 1 은 생략, 0 인 문자는 뺀다)"""
    c = Fr(c)
    letters = "".join(v + ("" if e == 1 else sup(e)) for v in sorted(pw, key=lambda k: order.index(k) if k in order else 99) for e in [pw[v]] if e)
    a = abs(c)
    cs = "" if (a == 1 and letters) else N(a)
    s = cs + letters
    if first:
        return (MI if c < 0 else "") + s
    return (f" {MI} " if c < 0 else " + ") + s

def sym_poly_str(expr, var="x"):
    """sympy 다항식(한 문자) → '2x^{3} − 3x + 1'"""
    P = sp.Poly(sp.expand(expr), SYMS[var])
    cs = [Fr(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for c in P.all_coeffs()]
    return poly(cs, var)
