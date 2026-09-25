# genkit/expr.py — 시드 명세의 식 평가와 수치 표시 (v1.3 · 09-13: 문자열 속 분수는 마커로 · sgt·sub 추가)
#
# 시드는 파이썬 코드가 아니라 JSON이다. 그 안의 식은 여기서만 평가되고,
# 허용 심볼 밖의 것은 예외로 떨어진다(임의 코드 실행 차단).

from __future__ import annotations

import math
import re
from fractions import Fraction

import sympy as sp

# ---------------------------------------------------------------- 허용 함수
_ALLOWED = {
    "abs": sp.Abs, "Abs": sp.Abs, "min": sp.Min, "max": sp.Max,
    "sqrt": sp.sqrt, "gcd": sp.gcd, "lcm": sp.lcm,
    "floor": sp.floor, "ceiling": sp.ceiling, "ceil": sp.ceiling,
    "Rational": sp.Rational, "Integer": sp.Integer,
    "sign": sp.sign, "factorial": sp.factorial,
    "binomial": sp.binomial, "isprime": sp.isprime,
    "pi": sp.pi, "E": sp.E,
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "log": sp.log,
    "Eq": sp.Eq, "And": sp.And, "Or": sp.Or, "Not": sp.Not,
}
_JOSA_NAMES = ("eul", "eun", "ika", "ro", "wa", "ida", "co", "sgn", "pn", "dec", "dv", "sgt", "sub")
_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_KEYWORDS = {"in", "not", "and", "or", "if", "else", "True", "False"}   # 문자열 파라미터 판별용 (ans in skew 등)
_SAFE_CHARS = re.compile(r"^[0-9A-Za-z_+\-*/%().,<>=!&| \t]*$")


class ExprError(Exception):
    pass


def _check(src: str, env: dict):
    if not _SAFE_CHARS.match(src):
        raise ExprError(f"허용되지 않는 문자: {src!r}")
    for nm in set(_NAME_RE.findall(src)):
        if nm in _ALLOWED or nm in env or nm in _JOSA_NAMES or nm in _KEYWORDS:
            continue
        raise ExprError(f"미허용 이름 {nm!r} (식: {src})")


def evaluate(src: str, env: dict):
    """식 하나를 평가해 Fraction/int/bool/float 로 돌려준다."""
    src = str(src).strip()
    _check(src, env)
    ns = dict(_ALLOWED)
    for nm in _JOSA_NAMES:
        ns[nm] = globals()[nm]
    for k, v in env.items():
        ns[k] = sp.Rational(v) if isinstance(v, (int, Fraction)) else v
    try:
        val = eval(src, {"__builtins__": {}}, ns)  # noqa: S307 — 위 _check 로 이름·문자 제한
    except ExprError:
        raise
    except Exception as e:                                      # noqa: BLE001
        raise ExprError(f"평가 실패 {src!r}: {e}") from e
    return _pyify(val)


def _pyify(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, sp.logic.boolalg.BooleanAtom):
        return bool(v)
    if isinstance(v, (int, float, Fraction)):
        return v
    if isinstance(v, sp.Expr):
        if v.free_symbols:
            raise ExprError(f"미지수가 남음: {v}")
        if v.is_Integer:
            return int(v)
        if v.is_Rational:
            return Fraction(int(sp.numer(v)), int(sp.denom(v)))
        f = float(v)
        return f
    return v


def truthy(src: str, env: dict) -> bool:
    v = evaluate(src, env)
    if isinstance(v, bool):
        return v
    return bool(v)


# ---------------------------------------------------------------- 수치 표시
def show(v, *, marker: bool = True) -> str:
    """값 → 문항에 넣을 문자열. 분수·근호는 MathIR 마커로 감싼다."""
    if isinstance(v, bool):
        return "참" if v else "거짓"
    if isinstance(v, str):
        return v
    if isinstance(v, int):
        return str(v)
    if isinstance(v, Fraction):
        if v.denominator == 1:
            return str(v.numerator)
        sgn = "-" if v < 0 else ""
        a, b = abs(v.numerator), v.denominator
        body = f"frac({a},{b})"
        body = f"-{body}" if sgn else body
        return f"[[{body}]]" if marker else body
    if isinstance(v, float):
        if abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        s = f"{v:.4f}".rstrip("0").rstrip(".")
        return s
    return str(v)


_SUB_RE = re.compile(r"\{([^{}]+)\}")


def fill(text, env: dict):
    """문자열(혹은 중첩 구조) 안의 {식}을 평가해 채운다. 이스케이프는 {{ }}."""
    if isinstance(text, list):
        return [fill(t, env) for t in text]
    if isinstance(text, dict):
        return {k: fill(v, env) for k, v in text.items()}
    if not isinstance(text, str):
        return text
    if "{" not in text:
        return fix_mark_josa(text)
    out = _SUB_RE.sub(lambda m: show(evaluate(m.group(1), env)), text.replace("{{", "\x00").replace("}}", "\x01"))
    return fix_mark_josa(out.replace("\x00", "{").replace("\x01", "}"))


# 채운 뒤 마지막 손질 (09-25) — ① 계수 0 인 항 지우기 ② 분수·근호 뒤 조사 자동 보정.
# 분수·근호 뒤 조사 자동 보정 — 시드 문자열에 '[[frac(1,5)]]를'·'3/2로' 처럼 조사가 박혀 있어도
# 읽는 소리('오분의 일' → 을, '이분의 삼' → 으로)대로 고쳐 쓴다. 조사 바로 뒤가 띄어쓰기·문장부호·끝일 때만(이다·이고 등은 건드리지 않음).
_MARK_JOSA_RE = re.compile(r"(\[\[-?(?:frac|sqrt)\([^\[\]]*\)\]\]|(?<![\w.])-?\d+/\d+)(으로|은|는|이|가|을|를|과|와|로)(?=[\s,.…)]|$)")


_ZERO_TERM = re.compile(r"\s[+\u2212-]\s0([a-z])(?![\w(²³⁴])")      # 'x² + 0x − 9' → 'x² − 9' (계수 0 인 항)


def fix_mark_josa(text: str) -> str:
    if " 0" in text:
        text = _ZERO_TERM.sub("", text)
    if "/" not in text and "[[" not in text:
        return text
    fn = {"은": eun, "는": eun, "이": ika, "가": ika, "을": eul, "를": eul, "과": wa, "와": wa, "으로": ro, "로": ro}
    return _MARK_JOSA_RE.sub(lambda m: m.group(1) + fn[m.group(2)](m.group(1)), text)


def fill_num(text, env: dict):
    """{식}을 '숫자 그대로'(마커 없이) 채운다 — 도형 인자용."""
    if isinstance(text, list):
        return [fill_num(t, env) for t in text]
    if isinstance(text, dict):
        return {k: fill_num(v, env) for k, v in text.items()}
    if not isinstance(text, str):
        return text
    m = _SUB_RE.fullmatch(text.strip())
    if m:                                   # 통째로 하나의 식이면 수치 자체를 돌려준다
        v = evaluate(m.group(1), env)
        if isinstance(v, Fraction):
            return int(v) if v.denominator == 1 else float(v)
        return v
    if "{" not in text:
        return text
    # 문자열 일부에 끼어드는 값 — 정수·소수는 그대로, 분수는 [[frac]] 마커 (판서 줄·라벨의 renderHtml 이 마커만 세로 분수로 그린다)
    return _SUB_RE.sub(lambda mm: show(evaluate(mm.group(1), env), marker=True), text)



# ---------------------------------------------------------------- 조사 (한국어)
_JONG = {"0", "1", "3", "6", "7", "8"}      # 숫자 읽기 끝소리에 받침이 있는 것


_FRAC_TAIL = re.compile(r"\[\[\s*-?\s*frac\(\s*(.+?)\s*,[^\]]*\)\s*\]\]\s*$")    # [[frac(a,b)]] — 'b분의 a'
_SQRT_TAIL = re.compile(r"\[\[\s*-?\s*sqrt\(\s*(.+?)\s*\)\s*\]\]\s*$")          # [[sqrt(n)]] — '루트 n'


def _tail(v) -> str:
    """조사를 고를 때 **마지막으로 읽히는** 부분. 분수는 'b분의 a' 라 분자, 근호는 '루트 n' 이라 n (09-25)."""
    t = str(v).strip()
    m = _FRAC_TAIL.search(t) or _SQRT_TAIL.search(t)
    if m:
        t = m.group(1)
    m = re.search(r"(\S+)/[^\s/]+\)*$", t)    # 끝이 분수(11/2 · (x + 1)/2)면 '이분의 십일' — 분자로 읽는다.
    if m:                                    # 괄호 속 설명('(1/x 항은 … 적분)')처럼 분수가 끝이 아니면 건드리지 않는다
        t = m.group(1)
    return t.rstrip(")")


def _has_jong(v) -> bool:
    t = _tail(v)
    m = re.search(r"(\d)\s*$", t)
    if m:
        return m.group(1) in _JONG
    if t and "\uac00" <= t[-1] <= "\ud7a3":
        return (ord(t[-1]) - 0xAC00) % 28 != 0
    if t and t[-1].isalpha() and t[-1].isascii():          # 영문자 이름(모서리 AB, 점 F …) — 읽는 소리 기준
        return t[-1].upper() in _LATIN_JONG
    return True


_LATIN_JONG = set("LMNR")        # 엘·엠·엔·알 → 받침 있음. 그 외(에이·비·씨·에프·엑스…)는 끝소리가 모음


def eul(v):  return "\uc744" if _has_jong(v) else "\ub97c"      # 을/를
def eun(v):  return "\uc740" if _has_jong(v) else "\ub294"      # 은/는
def ika(v):  return "\uc774" if _has_jong(v) else "\uac00"      # 이/가
def ro(v):   return "\uc73c\ub85c" if (_has_jong(v) and not _tail(v).rstrip(")").upper().endswith(("1", "7", "8", "L", "R"))) else "\ub85c"   # 로/으로 (ㄹ 받침은 '로')
def wa(v):   return "\uacfc" if _has_jong(v) else "\uc640"      # 과/와
def ida(v):  return "\uc774\ub2e4" if _has_jong(v) else "\ub2e4"  # 이다/다


def co(v):
    """계수 표기 — 1이면 빈 문자열, -1이면 '-'. `{co(k)}x` 로 쓰면 '1x' 가 나오지 않는다."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    if f == 1:
        return ""
    if f == -1:
        return "-"
    return show(f, marker=True)          # 분수 계수는 마커 — '[[frac(4,3)]]x'


def dec(v):
    """소수 표기 — 분수를 8.5 처럼. 하위권용 문장에서 frac 마커 대신 쓴다."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    if f.denominator == 1:
        return str(f.numerator)
    x = float(f)
    t = f"{x:.4f}".rstrip("0").rstrip(".")
    return t


def dv(a, b):
    """나눗셈 표기 — 'a ÷ b = q'. 나누는 수가 1이면 '÷ 1'을 쓰지 않고 몫만 남긴다."""
    try:
        fa, fb = Fraction(a), Fraction(b)
    except (TypeError, ValueError):
        return f"{a} ÷ {b}"
    q = show(fa / fb, marker=True) if fb else "?"
    if fb == 1:
        return q
    return f"{show(fa, marker=True)} ÷ {show(fb, marker=True)} = {q}"


def pn(v):
    """음수만 괄호로 감싼다 — '(-6)' / '12'. 식 안에서 뺄셈·덧셈 뒤에 쓴다."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    t = show(f, marker=True)             # 분수는 마커 — '([[-frac(2,3)]])'
    return f"({t})" if f < 0 else t


def sgn(v):
    """부호 붙은 항 — 양수면 '+ 3', 음수면 '- 3'."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    return ("\u2212 " if f < 0 else "+ ") + show(abs(f), marker=True)


_SUBS = str.maketrans("0123456789-", "₀₁₂₃₄₅₆₇₈₉₋")


def sub(v):
    """아래 첨자 — `a{sub(n)}` 이 'a₁₀' 으로 나온다 (수열의 항 번호). 수가 아니면 그대로."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    return (str(f.numerator) if f.denominator == 1 else str(f)).translate(_SUBS)


def sgt(v):
    """문자 앞의 부호 붙은 계수 — `{sgt(b)}x` 가 '+ x'·'− x'·'+ 3x'·'− 3x' 로 나온다 (계수 ±1 에서 '1x' 를 피한다)."""
    try:
        f = Fraction(v)
    except (TypeError, ValueError):
        return str(v)
    s = "\u2212 " if f < 0 else "+ "
    return s if abs(f) == 1 else s + show(abs(f), marker=True)


# ---------------------------------------------------------------- 파라미터 공간
def param_domain(p: dict):
    """파라미터 하나의 값 목록. {'int':[lo,hi]} | {'in':[…]} | {'step':[lo,hi,step]}"""
    v = p.get("values", p)
    if "in" in v:
        return list(v["in"])
    if "int" in v:
        lo, hi = v["int"]
        return list(range(int(lo), int(hi) + 1))
    if "step" in v:
        lo, hi, st = v["step"]
        n, out, x = 0, [], Fraction(str(lo))
        st = Fraction(str(st))
        while x <= Fraction(str(hi)) and n < 10000:
            out.append(x if x.denominator != 1 else int(x))
            x += st
            n += 1
        return out
    raise ExprError(f"파라미터 정의를 이해할 수 없음: {p}")


def space_size(params: list) -> int:
    n = 1
    for p in params:
        n *= max(1, len(param_domain(p)))
    return n


def params_at(params: list, idx: int) -> dict:
    """전단사 색인 — 같은 idx면 언제나 같은 파라미터 (혼합 진법)."""
    env, rest = {}, idx
    for p in reversed(params):
        dom = param_domain(p)
        env[p["name"]] = dom[rest % len(dom)]
        rest //= len(dom)
    return env


def even_spread(space: int, k: int):
    if k >= space:
        return list(range(space))
    return [(i * space) // k for i in range(k)]
