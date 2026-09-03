# ashrain.out — MathIR 파서·렌더·평가기 (mathir.py, v1.5 제안판 — 2026-09-04, mathir.js 동형 패치 필수)
# v1.5 (함수표 추가 + 소규모 파서 확장, v1.4 문법은 전부 그대로 통과):
#   ① cases(식1, 조건1, 식2, 조건2, …) 경우 나눔 정의   ② app(F, x, …) 파생 함수 적용: app(prime(f), x)=f′(x), app(comp(f,g), x)=(f∘g)(x), app(inv(f), 2), app(sub(S,1), t)
#   ③ iter(f, n, x) = fⁿ(x)   ④ 그리스 문자 함수 적용 alpha(t)   ⑤ 기하 라벨에 첨자·프라임 허용: seg(O1A), angle(A'PB), tri(P1P2P3)  (' 토큰 추가)
#   ⑥ xbar(X)=X̄, hat(p)=p̂, box(1)=□(가), 상수 cdots=⋯, GREEK에 sigma 추가·그리스 문자 표시   ⑦ point3 렉서 버그 수정(point+3 분리)   ⑧ FIGS에 image(src)·scene(pts) 추가
# v1.4 (답 표기층만 확장, 핵심 문법 불변 — mathir.js 동형 패치 필수):
#   ① 낱말 답에 ㄱ~ㅎ(합답형)·①~⑳(선지) 허용   ② '21°' → deg(21)
#   ③ '[[식]]단위'·'49.5 kg'·'frac(24,7) cm'·'72pi cm³' → 식 + unit 주석 (π→pi, ○× 낱말)   ④ 'a = 5, b = -1' / 'a < 0 and b > 0' → set(모두 성립)
#   ⑤ '좌변: [[x + 3y]]' 같은 라벨 접두 제거
# 위치: itemfactory/mathir.py
# 역할: [[ ]] 혼합문 분해 → 닫힌 문법 파싱(V-01·02·08) → 정식 직렬화(왕복 V-04)
#       → 표시 문자열(유니코드) → 정밀 평가(검산 V-03: 유리수 정확, 무리수 1e-9)
#       → figure 스키마(V-05) → 학년 경보(V-09)
# 함수표 FUNCS가 단일 원천 — 스펙 문서와 1:1.

from fractions import Fraction
import math, re

# ---------------------------------------------------------------- 함수표 (이름: (최소인자, 최대인자, 학년, 부류))
FUNCS = {
    # 1.1 수·연산
    "frac": (2, 2, "m1", "num"), "mixed": (3, 3, "m1", "num"), "pow": (2, 2, "m1", "num"),
    "sqrt": (1, 1, "m3", "num"), "root": (2, 2, "m3", "num"), "abs": (1, 1, "m1", "num"),
    "recdec": (2, 2, "m2", "num"), "floor": (1, 1, "h1", "num"), "fact": (1, 1, "h1", "num"),
    "max": (2, 2, "m1", "num"), "min": (2, 2, "m1", "num"), "ratio": (2, 3, "m1", "sym"),
    "pct": (1, 1, "m1", "num"), "deg": (1, 1, "m1", "num"), "dms": (2, 3, "m1", "num"),
    "pm": (1, 2, "m1", "sym"),
    # 1.2 기하 기호
    "seg": (1, 1, "m1", "sym"), "line": (1, 1, "m1", "sym"), "ray": (1, 1, "m1", "sym"),
    "arc": (1, 1, "m1", "sym"), "angle": (1, 1, "m1", "sym"), "tri": (1, 1, "m1", "sym"),
    "quad": (1, 1, "m1", "sym"), "par": (2, 2, "m1", "sym"), "perp": (2, 2, "m1", "sym"),
    "cong": (2, 2, "m2", "sym"), "sim": (2, 2, "m2", "sym"),
    "point": (2, 2, "m1", "sym"), "point3": (3, 3, "h3", "sym"),
    "vec": (1, 1, "h3", "sym"), "vcomp": (2, 3, "h3", "sym"), "dot": (2, 2, "h3", "sym"),
    # 1.3 집합·명제·복소
    "set": (0, 99, "h1", "sym"), "setb": (2, 2, "h1", "sym"),
    "mat": (3, 99, "h1", "sym"),
    "in": (2, 2, "h1", "sym"), "notin": (2, 2, "h1", "sym"),
    "subset": (2, 2, "h1", "sym"), "nsubset": (2, 2, "h1", "sym"),
    "union": (2, 2, "h1", "sym"), "inter": (2, 2, "h1", "sym"),
    "comp": (1, 2, "h1", "sym"),          # 1=여집합, 2=합성함수(h2)
    "card": (1, 1, "h1", "sym"), "imp": (2, 2, "h1", "sym"), "iff": (2, 2, "h1", "sym"),
    "neg": (1, 1, "h1", "sym"), "itv": (3, 3, "h1", "sym"), "conj": (1, 1, "h1", "sym"),
    # 1.4 지수로그·삼각
    "log": (1, 2, "h2", "num"), "ln": (1, 1, "h3", "num"),
    "sin": (1, 1, "h2", "num"), "cos": (1, 1, "h2", "num"), "tan": (1, 1, "h2", "num"),
    "csc": (1, 1, "h2", "num"), "sec": (1, 1, "h2", "num"), "cot": (1, 1, "h2", "num"),
    # 1.5 수열·극한·미적
    "sub": (2, 3, "h1", "sym"), "sum": (4, 4, "h2", "num"),   # 2인자=수열 첨자, 3인자=행렬 성분
    "lim": (3, 4, "h2", "num"), "prime": (1, 2, "h2", "sym"), "dydx": (2, 2, "h2", "sym"),
    "integ": (2, 2, "h3", "sym"), "dinteg": (4, 4, "h3", "num"), "inv": (1, 1, "h1", "sym"),
    # 1.6 경우의 수·확통
    "perm": (2, 2, "h1", "num"), "comb": (2, 2, "h1", "num"),
    "pperm": (2, 2, "h1", "num"), "hcomb": (2, 2, "h1", "num"),
    "prob": (1, 1, "h3", "sym"), "cprob": (2, 2, "h3", "sym"),
    "ev": (1, 1, "h3", "sym"), "var": (1, 1, "h3", "sym"), "sd": (1, 1, "h3", "sym"),
    "binomd": (2, 2, "h3", "sym"), "normald": (2, 2, "h3", "sym"),
    # 1.7 v1.5 추가
    "cases": (2, 8, "h1", "sym"),      # 경우 나눔: (식, 조건) 쌍 — 짝수 인자
    "app": (2, 6, "h1", "sym"),        # 파생 함수 적용: app(F, x, …)
    "iter": (3, 3, "h2", "sym"),       # 거듭 합성 fⁿ(x)
    "xbar": (1, 1, "h3", "sym"), "hat": (1, 1, "h3", "sym"),
    "box": (1, 1, "m1", "sym"),        # 빈칸 상자 □(가)
}
LABEL_FNS = ("seg", "line", "ray", "arc", "angle", "tri", "quad", "vec")
CONSTS = {"pi": math.pi, "e": math.e, "inf": math.inf, "empty": None, "i": None, "cdots": None}
GREEK = {"alpha", "beta", "gamma", "delta", "theta", "lam", "mu", "omega", "phi", "sigma"}
GREEK_DISP = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "theta": "θ", "lam": "λ", "mu": "μ", "omega": "ω", "phi": "φ", "sigma": "σ"}
_BOX = "가나다라마바사아자차카타파하"
GRADE_ORD = {"m1": 1, "m2": 2, "m3": 3, "h1": 4, "h2": 5, "h3": 6}

FIGS = {  # figure DSL: 필수 인자 키 (존재 검사)
    "numline": ["min", "max"], "coordplane": ["x", "y"], "table": ["rows"],
    "hist": ["bins", "counts"], "stemleaf": ["stems"], "crossing": ["angles"],
    "parallel": ["angles"], "tri": ["v"], "rect": ["w", "h"], "polygon": ["n"],
    "circle": ["r"], "sector": ["r", "angle"], "solid": ["kind"], "net": ["kind"],
    "boxplot": ["values"], "scatter": ["points"], "venn": ["sets"], "tree": ["levels"],
    "funcgraph": ["expr"], "unitcircle": [], "conic": ["kind"], "vecfig": ["vectors"],
    "space": [], "normcurve": ["m", "v"], "unsupported": ["raw"],
    "image": ["src"], "scene": ["pts"],   # v1.5: 도형 이미지 자산 / 선언형 장면(점·선분·원·표시)
}
FIG_STAGE = {"numline": 1, "coordplane": 1, "table": 1, "hist": 1}  # 1=●, 없으면 ◐○

class MathIRError(ValueError):
    def __init__(self, code, msg, pos=None):
        super().__init__(f"{code}: {msg}" + (f" @{pos}" if pos is not None else ""))
        self.code, self.pos = code, pos

# ---------------------------------------------------------------- 토크나이저
_TOKEN = re.compile(r"""
    (?P<num>\d+\.\d+|\d+)
  | (?P<id>[A-Za-z][A-Za-z]*)
  | (?P<op><=|>=|!=|[=<>+\-*/(),|'])
  | (?P<sp>\s+)
""", re.X)
_OPMAP = {"<=": "≤", ">=": "≥", "!=": "≠", "*": "×", "/": "÷"}

def _lex(s):
    s = s.replace("−", "-").replace("×", "*").replace("÷", "/").replace("≤", "<=").replace("≥", ">=").replace("≠", "!=")
    out, i = [], 0
    while i < len(s):
        m = _TOKEN.match(s, i)
        if not m:
            raise MathIRError("V-01", f"허용되지 않는 문자 '{s[i]}'", i)
        i = m.end()
        if m.lastgroup == "sp":
            continue
        kind = m.lastgroup
        val = m.group()
        if kind == "id" and i < len(s) and s[i].isdigit() and (val + s[i]) in FUNCS:   # v1.5⑦ point3
            val += s[i]; i += 1
        if kind == "op" and val in _OPMAP:
            val = _OPMAP[val]
        out.append((kind, val, m.start()))
    return out

# ---------------------------------------------------------------- 파서 (하강)
class _P:
    def __init__(self, toks, grade_hint=None):
        self.t, self.i = toks, 0
        self.max_grade = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None, None)

    def take(self):
        tok = self.peek(); self.i += 1; return tok

    def expect(self, val):
        k, v, p = self.take()
        if v != val:
            raise MathIRError("V-01", f"'{val}' 필요, '{v}' 발견", p)

    def parse(self):
        node = self.rel()
        if self.i < len(self.t):
            raise MathIRError("V-01", f"잉여 토큰 '{self.peek()[1]}'", self.peek()[2])
        return node

    def rel(self):                      # 관계 연쇄: a = b, 1 < x ≤ 3
        left = self.add()
        parts, ops = [left], []
        while self.peek()[1] in ("=", "<", ">", "≤", "≥", "≠"):
            ops.append(self.take()[1])
            parts.append(self.add())
        if not ops:
            return left
        return {"t": "rel", "ops": ops, "args": parts}

    def add(self):
        node = self.mul()
        while self.peek()[1] in ("+", "-"):
            op = self.take()[1]
            node = {"t": "bin", "op": op, "a": node, "b": self.mul()}
        return node

    def mul(self):
        node = self.unary()
        while True:
            k, v, p = self.peek()
            if v in ("×", "÷"):
                self.take()
                node = {"t": "bin", "op": v, "a": node, "b": self.unary()}
            elif k in ("num", "id") or v == "(":     # 병치 곱
                if k == "num" and node["t"] == "num":
                    raise MathIRError("V-01", "숫자 병치 불가", p)
                node = {"t": "bin", "op": "×", "a": node, "b": self.unary()}
            else:
                return node

    def unary(self):
        if self.peek()[1] == "-":
            self.take()
            return {"t": "neg", "a": self.unary()}
        return self.primary()

    def primary(self):
        k, v, p = self.take()
        if v == "(":
            inner = self.rel()
            self.expect(")")
            return {"t": "paren", "a": inner}
        if k == "num":
            return {"t": "num", "v": v}
        if k == "id":
            if self.peek()[1] == "(":
                return self.call(v, p)
            if v in CONSTS:
                return {"t": "const", "v": v}
            if len(v) == 1 or v in GREEK:
                return {"t": "var", "v": v}
            raise MathIRError("V-01", f"미지의 식별자 '{v}'", p)
        raise MathIRError("V-01", f"예상치 못한 토큰 '{v}'", p)

    def call(self, name, pos):
        self.expect("(")
        args = []
        if self.peek()[1] != ")":
            while True:
                if name in LABEL_FNS and (self.peek()[0] in ("id", "num") or self.peek()[1] == "'"):
                    lab = ""                                            # 점 라벨 나열형 (v1.5⑤ 첨자·프라임 허용)
                    while self.peek()[0] in ("id", "num") or self.peek()[1] == "'":
                        lab += self.take()[1]
                    args.append({"t": "label", "v": lab})
                elif name == "lim" and len(args) == 3 and self.peek()[1] in ("+", "-"):
                    args.append({"t": "label", "v": self.take()[1]})
                elif name == "itv" and len(args) == 2:
                    k, v, p = self.take()
                    args.append({"t": "label", "v": v})
                else:
                    args.append(self.rel())
                if self.peek()[1] == ",":
                    self.take(); continue
                break
        self.expect(")")
        if name in FUNCS:
            lo, hi, grade, _ = FUNCS[name]
            if not (lo <= len(args) <= hi):
                raise MathIRError("V-02" if len(args) in (lo, hi) or True else "V-08",
                                  f"{name} 인자 {len(args)}개 — 허용 {lo}~{hi}", pos)
            if name == "cases" and len(args) % 2:
                raise MathIRError("V-02", "cases 인자는 (식, 조건) 쌍이어야 함", pos)
            self.max_grade = max(self.max_grade, GRADE_ORD[grade])
            return {"t": "fn", "f": name, "args": args}
        if len(name) == 1 or name in GREEK:             # 함수 적용 f(x), v1.5④ alpha(t)
            self.max_grade = max(self.max_grade, GRADE_ORD["h1"])
            return {"t": "apply", "f": name, "args": args}
        raise MathIRError("V-01", f"미지의 함수 '{name}'", pos)

def parse(src, grade_hint=None):
    p = _P(_lex(src))
    node = p.parse()
    return node, p.max_grade

# ---------------------------------------------------------------- 정식 직렬화 (왕복용)
def to_ir(n):
    t = n["t"]
    if t == "num": return n["v"]
    if t == "var" or t == "const": return n["v"]
    if t == "label": return n["v"]
    if t == "neg": return "-" + to_ir(n["a"])
    if t == "paren": return "(" + to_ir(n["a"]) + ")"
    if t == "bin":
        op = {"×": " × ", "÷" : " ÷ ", "+": " + ", "-": " - "}[n["op"]]
        return to_ir(n["a"]) + op + to_ir(n["b"])
    if t == "rel":
        out = to_ir(n["args"][0])
        for op, arg in zip(n["ops"], n["args"][1:]):
            out += f" {op} " + to_ir(arg)
        return out
    if t in ("fn", "apply"):
        return n["f"] + "(" + ", ".join(to_ir(a) for a in n["args"]) + ")"
    raise MathIRError("V-04", f"직렬화 불가 노드 {t}")

# ---------------------------------------------------------------- 표시 렌더 (유니코드)
_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def _atom(n):
    return n["t"] in ("num", "var", "const", "label", "fn", "apply", "paren")

def _wrap(n):
    s = disp(n)
    return s if _atom(n) else "(" + s + ")"

def _over(s, mark):
    return "".join(c + mark for c in s)

def disp(n):
    t = n["t"]
    if t == "num": return n["v"]
    if t == "const": return {"pi": "π", "e": "e", "inf": "∞", "i": "i", "empty": "∅", "cdots": "⋯"}[n["v"]]
    if t == "var": return GREEK_DISP.get(n["v"], n["v"])
    if t == "label": return re.sub(r"\d+", lambda m: m.group().translate(_SUB), n["v"]).replace("'", "′")
    if t == "neg": return "−" + _wrap(n["a"])
    if t == "paren": return "(" + disp(n["a"]) + ")"
    if t == "bin":
        if n["op"] == "×":
            a, b = disp(n["a"]), _wrap(n["b"]) if n["b"]["t"] == "neg" else disp(n["b"])
            join = "" if (n["b"]["t"] in ("var", "fn", "apply", "paren", "const") and n["a"]["t"] in ("num", "var")) else " × "
            return _wrap(n["a"]) + join + (b if join == "" else _wrap(n["b"]))
        if n["op"] == "÷": return _wrap(n["a"]) + " ÷ " + _wrap(n["b"])
        op = "−" if n["op"] == "-" else n["op"]
        return disp(n["a"]) + f" {op} " + (_wrap(n["b"]) if n["b"]["t"] == "neg" else disp(n["b"]))
    if t == "rel":
        out = disp(n["args"][0])
        for op, arg in zip(n["ops"], n["args"][1:]):
            out += f" {op} " + disp(arg)
        return out
    if t == "apply":
        return GREEK_DISP.get(n["f"], n["f"]) + "(" + ", ".join(disp(a) for a in n["args"]) + ")"
    f, a = n["f"], n["args"]
    D = disp
    if f == "mat":
        try:
            r, c = int(a[0]["v"]), int(a[1]["v"])
            cells = [D(x) for x in a[2:]]
            rows = [" ".join(cells[i * c:(i + 1) * c]) for i in range(r)]
            return "(" + " ; ".join(rows) + ")"
        except Exception:
            return "mat(" + ", ".join(D(x) for x in a) + ")"
    if f == "frac": return _wrap(a[0]) + "/" + _wrap(a[1])
    if f == "mixed": return D(a[0]) + " " + D(a[1]) + "/" + D(a[2])
    if f == "pow":
        ex = to_ir(a[1]).replace(" ", "")
        return _wrap(a[0]) + (ex.translate(_SUP) if re.fullmatch(r"-?\d+", ex) else "^(" + D(a[1]) + ")")
    if f == "sqrt": return "√" + _wrap(a[0])
    if f == "root": return to_ir(a[0]).translate(_SUP) + "√" + _wrap(a[1])
    if f == "abs": return "|" + D(a[0]) + "|"
    if f == "recdec":
        rep = D(a[1])
        return D(a[0]) + (rep[0] + "\u0307" + (rep[1:-1] + rep[-1] + "\u0307" if len(rep) > 1 else ""))
    if f == "floor": return "[" + D(a[0]) + "]"
    if f == "fact": return _wrap(a[0]) + "!"
    if f in ("max", "min"): return f + "(" + D(a[0]) + ", " + D(a[1]) + ")"
    if f == "ratio": return " : ".join(D(x) for x in a)
    if f == "pct": return D(a[0]) + "%"
    if f == "deg": return D(a[0]) + "°"
    if f == "dms": return D(a[0]) + "°" + D(a[1]) + "′" + (D(a[2]) + "″" if len(a) > 2 else "")
    if f == "pm": return "±" + _wrap(a[0]) if len(a) == 1 else _wrap(a[0]) + " ± " + _wrap(a[1])
    if f in ("seg", "line", "ray", "arc"):
        s = "".join(D(x) for x in a)
        return {"seg": _over(s, "\u0305"), "line": _over(s, "\u0305"),
                "ray": _over(s, "\u20d7"), "arc": _over(s, "\u0361")}[f]
    if f == "angle": return "∠" + "".join(D(x) for x in a)
    if f == "tri": return "△" + "".join(D(x) for x in a)
    if f == "quad": return "□" + "".join(D(x) for x in a)
    if f == "par": return D(a[0]) + " ∥ " + D(a[1])
    if f == "perp": return D(a[0]) + " ⊥ " + D(a[1])
    if f == "cong": return D(a[0]) + " ≡ " + D(a[1])
    if f == "sim": return D(a[0]) + " ∽ " + D(a[1])
    if f in ("point", "point3", "vcomp"): return "(" + ", ".join(D(x) for x in a) + ")"
    if f == "vec": return _over("".join(D(x) for x in a), "\u20d7")
    if f == "dot": return D(a[0]) + " · " + D(a[1])
    if f == "set": return "{" + ", ".join(D(x) for x in a) + "}"
    if f == "setb": return "{" + D(a[0]) + " | " + D(a[1]) + "}"
    if f == "in": return D(a[0]) + " ∈ " + D(a[1])
    if f == "notin": return D(a[0]) + " ∉ " + D(a[1])
    if f == "subset": return D(a[0]) + " ⊂ " + D(a[1])
    if f == "nsubset": return D(a[0]) + " ⊄ " + D(a[1])
    if f == "union": return D(a[0]) + " ∪ " + D(a[1])
    if f == "inter": return D(a[0]) + " ∩ " + D(a[1])
    if f == "comp": return _wrap(a[0]) + "ᶜ" if len(a) == 1 else D(a[0]) + "∘" + D(a[1])
    if f == "card": return "n(" + D(a[0]) + ")"
    if f == "imp": return D(a[0]) + " → " + D(a[1])
    if f == "iff": return D(a[0]) + " ↔ " + D(a[1])
    if f == "neg": return "~" + _wrap(a[0])
    if f == "itv":
        br = {"cc": "[]", "co": "[)", "oc": "(]", "oo": "()"}[a[2]["v"]]
        return br[0] + D(a[0]) + ", " + D(a[1]) + br[1]
    if f == "conj": return _over(D(a[0]), "\u0305")
    if f == "log": return "log " + _wrap(a[0]) if len(a) == 1 else "log" + to_ir(a[0]).translate(_SUB) + " " + _wrap(a[1]) if re.fullmatch(r"\d+", to_ir(a[0])) else "log_(" + D(a[0]) + ") " + _wrap(a[1])
    if f == "ln": return "ln " + _wrap(a[0])
    if f in ("sin", "cos", "tan", "csc", "sec", "cot"): return f + " " + _wrap(a[0])
    if f == "sub":
        if len(a) == 3: return D(a[0]) + "[" + D(a[1]) + "," + D(a[2]) + "]"
        ix = to_ir(a[1]).replace(" ", "")
        return D(a[0]) + (ix.translate(_SUB) if re.fullmatch(r"\d+", ix) else "_" + _wrap(a[1]))
    if f == "sum": return "Σ[" + D(a[0]) + "=" + D(a[1]) + ".." + D(a[2]) + "] " + _wrap(a[3])
    if f == "lim":
        side = a[3]["v"] if len(a) > 3 else ""
        return "lim[" + D(a[0]) + "→" + D(a[1]) + ("⁺" if side == "+" else "⁻" if side == "-" else "") + "] " + _wrap(a[2])
    if f == "prime": return _wrap(a[0]) + ("′" if len(a) == 1 or to_ir(a[1]) == "1" else "″")
    if f == "dydx": return "d" + D(a[0]) + "/d" + D(a[1])
    if f == "integ": return "∫ " + D(a[0]) + " d" + D(a[1])
    if f == "dinteg": return "∫[" + D(a[0]) + ".." + D(a[1]) + "] " + D(a[2]) + " d" + D(a[3])
    if f == "inv": return _wrap(a[0]) + "⁻¹"
    if f in ("perm", "comb", "pperm", "hcomb"):
        L = {"perm": "P", "comb": "C", "pperm": "Π", "hcomb": "H"}[f]
        n1, n2 = to_ir(a[0]), to_ir(a[1])
        if re.fullmatch(r"\d+", n1) and re.fullmatch(r"\d+", n2):
            return n1.translate(_SUB) + L + n2.translate(_SUB)
        return f"{n1}{L}{n2}"
    if f == "prob": return "P(" + D(a[0]) + ")"
    if f == "cprob": return "P(" + D(a[0]) + " | " + D(a[1]) + ")"
    if f == "ev": return "E(" + D(a[0]) + ")"
    if f == "var": return "V(" + D(a[0]) + ")"
    if f == "sd": return "σ(" + D(a[0]) + ")"
    if f == "binomd": return "B(" + D(a[0]) + ", " + D(a[1]) + ")"
    if f == "normald": return "N(" + D(a[0]) + ", " + D(a[1]) + ")"
    # ---- v1.5
    if f == "cases": return "{" + " ; ".join(D(a[i]) + " (" + D(a[i + 1]) + ")" for i in range(0, len(a), 2)) + "}"
    if f == "app":
        F = a[0]
        head = D(F) if (F["t"] in ("var", "label") or (F["t"] == "fn" and F["f"] in ("prime", "inv", "sub", "iter", "xbar", "hat"))) else "(" + D(F) + ")"
        return head + "(" + ", ".join(D(x) for x in a[1:]) + ")"
    if f == "iter":
        ex = to_ir(a[1]).replace(" ", "")
        return _wrap(a[0]) + (ex.translate(_SUP) if re.fullmatch(r"-?\d+", ex) else "^(" + D(a[1]) + ")") + "(" + D(a[2]) + ")"
    if f == "xbar": return D(a[0]) + "\u0304"
    if f == "hat": return D(a[0]) + "\u0302"
    if f == "box":
        k = to_ir(a[0])
        return "□(" + (_BOX[int(k) - 1] if re.fullmatch(r"\d+", k) and 1 <= int(k) <= len(_BOX) else D(a[0])) + ")"
    return to_ir(n)   # 표시 규칙 미정의 → 정식 IR로 폴백

# ---------------------------------------------------------------- 평가기 (검산용)
def _num(v):
    return Fraction(v) if re.fullmatch(r"\d+", v) else Fraction(v)

def ev(n, env=None):
    """유리 연산은 Fraction 정확값, 무리·초월은 float. 평가 불가(기호류)는 MathIRError."""
    env = env or {}
    t = n["t"]
    if t == "num": return Fraction(n["v"]) if "." not in n["v"] else Fraction(n["v"])
    if t == "var":
        if n["v"] in env: return env[n["v"]]
        raise MathIRError("V-03", f"미지 변수 {n['v']}")
    if t == "const":
        v = CONSTS[n["v"]]
        if v is None: raise MathIRError("V-03", f"평가 불가 상수 {n['v']}")
        return v
    if t == "paren": return ev(n["a"], env)
    if t == "neg": return -ev(n["a"], env)
    if t == "bin":
        A, B = ev(n["a"], env), ev(n["b"], env)
        if n["op"] == "+": return A + B
        if n["op"] == "-": return A - B
        if n["op"] == "×": return A * B
        if n["op"] == "÷": return A / B
    if t == "fn":
        f, a = n["f"], n["args"]
        E = lambda k: ev(a[k], env)
        if f == "frac": return E(0) / E(1)
        if f == "mixed": return E(0) + E(1) / E(2)
        if f == "pow":
            b_, e_ = E(0), E(1)
            if isinstance(b_, Fraction) and isinstance(e_, Fraction) and e_.denominator == 1:
                return b_ ** e_.numerator
            return float(b_) ** float(e_)
        if f == "sqrt": return math.sqrt(float(E(0)))
        if f == "root": return float(E(1)) ** (1.0 / float(E(0)))
        if f == "abs": return abs(E(0))
        if f == "recdec":
            pre, rep = to_ir(a[0]), to_ir(a[1])
            base = Fraction(pre)
            dec = len(pre.split(".")[1]) if "." in pre else 0
            return base + Fraction(int(rep), (10 ** len(rep) - 1) * 10 ** dec)
        if f == "floor": return Fraction(math.floor(float(E(0))))
        if f == "fact": return Fraction(math.factorial(int(E(0))))
        if f == "max": return max(E(0), E(1))
        if f == "min": return min(E(0), E(1))
        if f == "pct": return E(0) / 100
        if f == "deg": return E(0)
        if f == "dms": return E(0) + E(1) / 60 + (E(2) / 3600 if len(a) > 2 else 0)
        if f == "log": return math.log10(float(E(0))) if len(a) == 1 else math.log(float(E(1)), float(E(0)))
        if f == "ln": return math.log(float(E(0)))
        if f in ("sin", "cos", "tan"): return getattr(math, f)(float(E(0)))
        if f == "perm": n_, r_ = int(E(0)), int(E(1)); return Fraction(math.perm(n_, r_))
        if f == "comb": n_, r_ = int(E(0)), int(E(1)); return Fraction(math.comb(n_, r_))
        if f == "pperm": return Fraction(int(E(0)) ** int(E(1)))
        if f == "hcomb": n_, r_ = int(E(0)), int(E(1)); return Fraction(math.comb(n_ + r_ - 1, r_))
        if f == "sum":
            k = a[0]["v"]; lo, hi = int(ev(a[1], env)), int(ev(a[2], env))
            tot = Fraction(0)
            for kv in range(lo, hi + 1):
                tot += ev(a[3], {**env, k: Fraction(kv)})
            return tot
        if f == "dinteg":                       # 수치 적분 (검산용 심프슨)
            x = a[3]["v"]; lo, hi = float(ev(a[0], env)), float(ev(a[1], env))
            N = 2000; h = (hi - lo) / N; s = 0.0
            for j in range(N + 1):
                w = 1 if j in (0, N) else (4 if j % 2 else 2)
                s += w * float(ev(a[2], {**env, x: Fraction(lo + j * h).limit_denominator(10**9)}))
            return s * h / 3
    raise MathIRError("V-03", f"평가 불가 노드 {n.get('f', t)}")

def close(a, b, tol=1e-9):
    if isinstance(a, Fraction) and isinstance(b, Fraction):
        return a == b
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)), abs(float(b)))

# ---------------------------------------------------------------- 혼합문·검증 진입점
_MARK = re.compile(r"\[\[(.*?)\]\]", re.S)

def parse_text(text, grade_hint=None):
    """혼합문 → [{'kind':'text'|'ir','raw','node'?,'ir'?,'disp'?}], max_grade, 오류 리스트"""
    segs, errs, mg, last = [], [], 0, 0
    for m in _MARK.finditer(text):
        if m.start() > last:
            segs.append({"kind": "text", "raw": text[last:m.start()]})
        src = m.group(1).strip()
        try:
            node, g = parse(src)
            rt, _ = parse(to_ir(node))
            if to_ir(rt) != to_ir(node):
                errs.append({"code": "V-04", "src": src})
            segs.append({"kind": "ir", "raw": src, "node": node, "ir": to_ir(node), "disp": disp(node)})
            mg = max(mg, g)
        except MathIRError as e:
            errs.append({"code": e.code, "src": src, "msg": str(e)})
            segs.append({"kind": "text", "raw": m.group(0)})
        last = m.end()
    if last < len(text):
        segs.append({"kind": "text", "raw": text[last:]})
    if grade_hint and mg > GRADE_ORD.get(grade_hint[:2], 9):
        errs.append({"code": "V-09", "msg": f"학년 힌트 {grade_hint} 초과 문법"})
    return segs, mg, errs

def render_text(text):
    segs, _, _ = parse_text(text)
    return "".join(s["disp"] if s["kind"] == "ir" else s["raw"] for s in segs)

# v1.4③ 단위 꼬리: 답 끝의 단위 토큰(길이·넓이·부피·질량·시간·개수 등)을 떼어 unit 주석으로 보관
_UNITS = r"(?:cm³|cm²|m³|m²|km²|mm²|cm3|cm2|m3|m2|km|cm|mm|m|kg|g|L|mL|%|개|명|원|시간|분|초|번|살|점|회|장|권|마리|가지|자루|송이|그루|대|병|봉지|통|칸)"

def _split_unit(s):
    s = re.sub(r"\s*pow\((cm|m|km|mm),\s*([23])\)$", lambda m: " " + m.group(1) + ("²" if m.group(2) == "2" else "³"), s)
    m = re.fullmatch(r"(.+?)\s*(" + _UNITS + r")", s, re.S)
    if m and m.group(1).strip():
        return m.group(1).strip(), m.group(2)
    return s, None

def _parse_answer_one(s):
    s = s.strip()
    s = re.sub(r"^[가-힣]{1,4}\s*[:：]\s*", "", s)          # v1.4⑤ '좌변:' 라벨 접두 제거
    unit = None
    m = re.fullmatch(r"\[\[(.+)\]\]\s*(" + _UNITS + r")?", s, re.S)   # [[마커]] 관용 탈피 (+ 단위 꼬리)
    if m:
        s, unit = m.group(1).strip(), m.group(2)
    else:
        s, unit = _split_unit(s)                                          # '49.5 kg' · 'frac(24,7) cm' · '500*pi cm³'
    s = re.sub(r"(\d+(?:\.\d+)?)\s*°", r"deg(\1)", s)         # v1.4② 각도
    s = s.replace("π", "pi")
    s = re.sub(r"(\d)\s*pi\b", r"\1*pi", s)                     # '72pi' → 72*pi
    try:
        node, _ = parse(s)
        out = {"kind": "ir", "node": node}
        if unit: out["unit"] = unit
        return out
    except MathIRError:
        if re.fullmatch(r"[가-힣ㄱ-ㅎ①-⑳○×A-Za-z0-9 ,·~]+", s):   # v1.4① 합답형·선지·○× 기호
            return {"kind": "word", "v": s}
        raise

def parse_answer(s):
    s = s.strip()
    parts = re.split(r"\s*(?:또는|\|)\s*", s)
    if len(parts) >= 2:
        return {"kind": "set", "items": [_parse_answer_one(p) for p in parts if p.strip()]}
    # v1.4④ 병립 답: 'a = 5, b = -1' · 'a < 0 and b > 0' — 각 조각이 관계식/식으로 파싱될 때만 set
    conj = re.split(r"\s*,\s*|\s+and\s+", s)
    if len(conj) >= 2 and all(c.strip() for c in conj):
        try:
            its = [_parse_answer_one(c) for c in conj]
            if all(it["kind"] == "ir" for it in its):
                return {"kind": "set", "items": its}
        except MathIRError:
            pass
    return _parse_answer_one(s)

def check_equation_answer(question_text, answer_str):
    """답이 'x = 값' 꼴이면 문제문 속 관계식들에 대입해 성립 확인. (True/False/None=검산 불가)"""
    def one(node, rels):
        if node["t"] != "rel" or node["ops"] != ["="] or node["args"][0]["t"] != "var":
            return None
        var, val = node["args"][0]["v"], ev(node["args"][1])
        oks = []
        for r in rels:
            try:
                vals = [ev(p, {var: val}) for p in r["args"]]
                oks.append(all(close(vals[k], vals[k + 1]) for k in range(len(vals) - 1)))
            except MathIRError:
                continue
        return all(oks) if oks else None
    try:
        ans = parse_answer(answer_str)
        segs, _, errs = parse_text(question_text)
        if errs: return None
        rels = [s["node"] for s in segs if s["kind"] == "ir" and s["node"]["t"] == "rel" and "=" in s["node"]["ops"]]
        if not rels: return None
        nodes = [it["node"] for it in ans["items"] if it["kind"] == "ir"] if ans["kind"] == "set" \
                else ([ans["node"]] if ans["kind"] == "ir" else [])
        if not nodes: return None
        rs = [one(n, rels) for n in nodes]           # 복수 해: 모든 근이 성립해야 참
        if any(r is False for r in rs): return False
        if any(r is None for r in rs): return None
        return True
    except MathIRError:
        return None

def check_figure(fig_list):
    errs = []
    for i, f in enumerate(fig_list or []):
        fn = f.get("fn")
        if fn not in FIGS:
            errs.append({"code": "V-05", "i": i, "msg": f"미지 도형 함수 {fn}"})
            continue
        for k in FIGS[fn]:
            if k not in (f.get("args") or {}):
                errs.append({"code": "V-05", "i": i, "msg": f"{fn}.{k} 누락"})
    return errs

# ---------------------------------------------------------------- 자가 시험
if __name__ == "__main__":
    T = [
        ("frac(1,2) + frac(1,3)", "1/2 + 1/3", Fraction(5, 6)),
        ("pow(-2,3) + 10", "(−2)³ + 10", Fraction(2)),
        ("mixed(2,1,3) × 6", None, Fraction(14)),
        ("recdec(0.2,45)", None, Fraction(2, 10) + Fraction(45, 990)),
        ("fact(5) ÷ fact(3)", None, Fraction(20)),
        ("perm(5,2) + comb(5,2)", "₅P₂ + ₅C₂", Fraction(30)),
        ("hcomb(3,2)", None, Fraction(6)),
        ("sum(k,1,10,k)", None, Fraction(55)),
        ("dms(35,30)", None, Fraction(71, 2)),
    ]
    for src, d, val in T:
        n, g = parse(src)
        rt, _ = parse(to_ir(n))
        assert to_ir(rt) == to_ir(n), "왕복 실패 " + src
        if d: assert disp(n) == d, f"표시 {disp(n)!r} != {d!r}"
        assert close(ev(n), val), f"평가 {src}: {ev(n)} != {val}"
    for src in ["log(2,8)", "lim(x,inf,frac(1,x))", "dinteg(0,1,pow(x,2),x)",
                "sin(frac(pi,6))", "abs(-7)"]:
        n, _ = parse(src)
        parse(to_ir(n))
    assert close(ev(parse("log(2,8)")[0]), 3)
    assert close(ev(parse("dinteg(0,1,pow(x,2),x)")[0]), 1 / 3, 1e-6)
    assert close(ev(parse("sin(frac(pi,6))")[0]), 0.5)
    segs, mg, errs = parse_text("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.")
    assert not errs and mg == GRADE_ORD["m1"]
    assert render_text("[[pow(x,2) - 4 = 0]]") == "x² − 4 = 0"
    assert check_equation_answer("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.", "x = 8") is True
    assert check_equation_answer("일차방정식 [[frac(x,2) - 3 = frac(x,4) - 1]] 을 푸시오.", "x = 7") is False
    assert check_equation_answer("[[3x + 2 = 11]]", "x = 3") is True
    _, _, e9 = parse_text("[[lim(x,0,frac(1,x))]]", grade_hint="m1")
    assert any(x["code"] == "V-09" for x in e9)
    try:
        parse("frak(1,2)")
        assert False
    except MathIRError as e:
        assert e.code == "V-01"
    try:
        parse("frac(1)")
        assert False
    except MathIRError:
        pass
    assert not check_figure([{"fn": "numline", "args": {"min": -5, "max": 5}}])
    assert check_figure([{"fn": "banana", "args": {}}])
    # ---- v1.5 자가 시험
    for src, d in [("cases(pow(3,x) + 1, x <= 1, 9 - 3 log(3,x), x > 1)", "{3^(x) + 1 (x ≤ 1) ; 9 − 3log₃ x (x > 1)}"),
                   ("app(prime(f), x)", "f′(x)"), ("app(comp(f, g), x)", "(f∘g)(x)"), ("app(inv(f), 2)", "f⁻¹(2)"),
                   ("app(sub(S, 1), t)", "S₁(t)"), ("alpha(t) + beta(t) = 5", "α(t) + β(t) = 5"),
                   ("iter(f, 3, x)", "f³(x)"), ("xbar(X)", "X\u0304"), ("hat(p)", "p\u0302"), ("box(1)", "□(가)"),
                   ("angle(A'PB)", "∠A′PB"), ("tri(P1P2P3)", "△P₁P₂P₃"), ("point3(1, 2, 3)", "(1, 2, 3)"),
                   ("sub(a,1) + cdots + sub(a,n)", "a₁ + ⋯ + a_n"), ("sigma", "σ")]:
        n, _ = parse(src); rt, _ = parse(to_ir(n))
        assert to_ir(rt) == to_ir(n), "v1.5 왕복 실패 " + src
        assert disp(n) == d, f"v1.5 표시 {disp(n)!r} != {d!r} ({src})"
    n, _ = parse("seg(O1A) = 21"); assert "₁" in disp(n) and to_ir(parse(to_ir(n))[0]) == to_ir(n)
    try:
        parse("cases(x, x > 0, y)"); assert False
    except MathIRError as e:
        assert e.code == "V-02"
    assert not check_figure([{"fn": "image", "args": {"src": "figs/x.png", "raw": "설명"}}])
    assert check_figure([{"fn": "image", "args": {}}])
    _, _, e = parse_text("[[f(x) = cases(pow(x,2), x < 1, 2x - 1, x >= 1)]]에서 [[app(prime(f), 3)]]의 값은?")
    assert not e
    print("mathir.py 자가 시험 전부 통과")
