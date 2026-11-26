# 주차별 기초 다지기 — 학년마다 52주 × 주 2회 = 104회차(회차마다 20문항: 5단계 × 4문항)
#   python3 weeks.py              모든 학년
#   python3 weeks.py e3 m2        몇 학년만
# 회차 문항은 단원 생성기(g_*.py)를 SEED_SHIFT 를 바꿔 다시 돌려 새로 뽑는다 — 유형별 문제 세트(SEED_SHIFT 0)와 겹치지 않고, 학년 안에서도 발문이 겹치지 않는다.
# 학년 달력: 1 ~ 20주 1학기 · 21 ~ 25주 여름방학(복습 6 · 예습 4) · 26 ~ 45주 2학기 · 46 ~ 52주 겨울방학(복습 8 · 예습 6). 1주 = 3월 첫 주.
import json, os, sys, importlib, secrets, re, math
sys.path.insert(0, os.path.dirname(__file__))
import core
from export import REG, CODES, ALPHA

REPO = os.environ.get("ASHRAIN_REPO") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))      # 레포 뿌리(avgen/ 의 한 단계 위)
OUT = f"{REPO}/public/av-weeks"
WCODES = os.path.join(os.path.dirname(__file__), "wcodes.json")

# ── 교과서 단원(학기마다 차례대로) ─────────────────────────────────────────────
CURR = {
    "e1-1": ["9까지의 수", "여러 가지 모양", "덧셈과 뺄셈", "비교하기", "50까지의 수"],
    "e1-2": ["100까지의 수", "덧셈과 뺄셈", "모양과 시각", "규칙 찾기"],
    "e2-1": ["세 자리 수", "여러 가지 도형", "덧셈과 뺄셈", "길이 재기", "분류하기", "곱셈"],
    "e2-2": ["네 자리 수", "곱셈구구", "길이 재기", "시각과 시간", "표와 그래프", "규칙 찾기"],
    "e3-1": ["덧셈과 뺄셈", "평면도형", "나눗셈", "곱셈", "길이와 시간", "분수와 소수"],
    "e3-2": ["곱셈", "나눗셈", "원", "분수", "들이와 무게", "자료의 정리"],
    "e4-1": ["큰 수", "각도", "곱셈과 나눗셈", "평면도형의 이동", "막대그래프", "규칙 찾기"],
    "e4-2": ["분수의 덧셈과 뺄셈", "삼각형", "소수의 덧셈과 뺄셈", "사각형", "꺾은선그래프", "다각형"],
    "e5-1": ["자연수의 혼합 계산", "약수와 배수", "규칙과 대응", "약분과 통분", "분수의 덧셈과 뺄셈", "다각형의 둘레와 넓이"],
    "e5-2": ["수의 범위와 어림하기", "분수의 곱셈", "합동과 대칭", "소수의 곱셈", "직육면체", "평균과 가능성"],
    "e6-1": ["분수의 나눗셈", "각기둥과 각뿔", "소수의 나눗셈", "비와 비율", "여러 가지 그래프", "직육면체의 부피와 겉넓이"],
    "e6-2": ["분수의 나눗셈", "소수의 나눗셈", "공간과 입체", "비례식과 비례배분", "원의 넓이", "원기둥, 원뿔, 구"],
    "m1-1": ["소인수분해", "정수와 유리수", "문자와 식", "좌표평면과 그래프"],
    "m1-2": ["기본 도형과 작도", "평면도형", "입체도형", "자료의 정리와 해석"],
    "m2-1": ["수와 식의 계산", "부등식과 연립방정식", "일차함수"],
    "m2-2": ["도형의 성질", "도형의 닮음과 피타고라스 정리", "확률"],
    "m3-1": ["제곱근과 실수", "다항식의 곱셈과 인수분해", "이차방정식", "이차함수"],
    "m3-2": ["삼각비", "원의 성질", "통계"],
    "h1-1": ["다항식", "방정식과 부등식", "경우의 수", "행렬"],
    "h1-2": ["도형의 방정식", "집합과 명제", "함수"],
    "h2-1": ["지수함수와 로그함수", "삼각함수", "수열"],
    "h2-2": ["함수의 극한과 연속", "미분", "적분"],
    "h3-1": ["수열의 극한", "미분법", "적분법"],
    "h3-2": ["경우의 수", "확률", "통계"],
    "h3-3": ["이차곡선", "공간도형과 공간좌표", "벡터"],
}
# 학년 → (1학기 단원들, 2학기 단원들, 다음 학년 1학기 단원들) — "학기:단원"
def T(term, names=None):
    return [f"{term}:{n}" for n in (names or CURR[term])]
GRADES = [
    ("e1", "초1", "초등", T("e1-1"), T("e1-2"), T("e2-1")),
    ("e2", "초2", "초등", T("e2-1"), T("e2-2"), T("e3-1")),
    ("e3", "초3", "초등", T("e3-1"), T("e3-2"), T("e4-1")),
    ("e4", "초4", "초등", T("e4-1"), T("e4-2"), T("e5-1")),
    ("e5", "초5", "초등", T("e5-1"), T("e5-2"), T("e6-1")),
    ("e6", "초6", "초등", T("e6-1"), T("e6-2"), T("m1-1")),
    ("m1", "중1", "중등", T("m1-1"), T("m1-2"), T("m2-1")),
    ("m2", "중2", "중등", T("m2-1"), T("m2-2"), T("m3-1")),
    ("m3", "중3", "중등", T("m3-1"), T("m3-2"), T("h1-1")),
    ("h1", "고1", "고등", T("h1-1"), T("h1-2"), T("h2-1")),
    ("h2", "고2", "고등", T("h2-1"), T("h2-2"), T("h3-1") + T("h3-2")),
    ("h3", "고3", "고등", T("h3-1") + T("h3-2", ["경우의 수", "확률"]), T("h3-2", ["통계"]) + T("h3-3"), []),
]

# ── 생성기 단계 → 교과서 단원 ──────────────────────────────────────────────────
def same(unit):
    return {i: unit for i in range(1, 6)}
TAG = {
    "e-ten": {1: "e1-1:덧셈과 뺄셈", 2: "e1-2:덧셈과 뺄셈", 3: "e1-2:덧셈과 뺄셈", 4: "e1-2:덧셈과 뺄셈", 5: "e1-2:덧셈과 뺄셈"},
    "e-hund": {1: "e1-2:100까지의 수", 2: "e1-2:100까지의 수", 3: "e1-2:100까지의 수", 4: "e1-2:덧셈과 뺄셈", 5: "e1-2:덧셈과 뺄셈"},
    "e-col": same("e2-1:덧셈과 뺄셈"),
    "e-add": same("e3-1:덧셈과 뺄셈"),
    "e-sub": same("e3-1:덧셈과 뺄셈"),
    "e-rel": {1: "e2-1:덧셈과 뺄셈", 2: "e2-1:덧셈과 뺄셈", 3: "e3-1:덧셈과 뺄셈", 4: "e3-1:나눗셈", 5: "e3-1:나눗셈"},
    "e-word": {1: "e2-1:덧셈과 뺄셈", 2: "e2-1:덧셈과 뺄셈", 3: "e2-2:곱셈구구", 4: "e3-1:나눗셈", 5: "e3-2:나눗셈"},
    "e-big": {1: "e2-2:네 자리 수", 2: "e4-1:큰 수", 3: "e4-1:큰 수", 4: "e4-1:큰 수", 5: "e4-1:큰 수"},
    "e-time": {1: "e1-2:모양과 시각", 2: "e2-2:시각과 시간", 3: "e3-1:길이와 시간", 4: "e2-2:시각과 시간", 5: "e3-1:길이와 시간"},
    "e-unit": {1: "e3-1:길이와 시간", 2: "e3-1:길이와 시간", 3: "e3-1:길이와 시간", 4: "e3-2:들이와 무게", 5: "e3-2:들이와 무게"},
    "e-times": {1: "e2-1:곱셈", 2: "e2-2:곱셈구구", 3: "e2-2:곱셈구구", 4: "e2-2:곱셈구구", 5: "e2-2:곱셈구구"},
    "e-area3": {1: "e3-1:곱셈", 2: "e3-1:곱셈", 3: "e3-2:곱셈", 4: "e3-2:곱셈", 5: "e3-2:곱셈"},
    "e-mul": {1: "e3-1:곱셈", 2: "e3-2:곱셈", 3: "e3-2:곱셈", 4: "e3-2:곱셈", 5: "e4-1:곱셈과 나눗셈"},
    "e-div3": {1: "e3-1:나눗셈", 2: "e3-2:나눗셈", 3: "e3-2:나눗셈", 4: "e3-2:나눗셈", 5: "e3-2:나눗셈"},
    "e-div": {1: "e3-2:나눗셈", 2: "e3-2:나눗셈", 3: "e3-2:나눗셈", 4: "e4-1:곱셈과 나눗셈", 5: "e4-1:곱셈과 나눗셈"},
    "e-mix": same("e5-1:자연수의 혼합 계산"),
    "e-gcd": same("e5-1:약수와 배수"),
    "e-fsize": {1: "e3-1:분수와 소수", 2: "e3-1:분수와 소수", 3: "e3-2:분수", 4: "e5-1:약분과 통분", 5: "e5-1:약분과 통분"},
    "e-frac4": same("e4-2:분수의 덧셈과 뺄셈"),
    "e-red": {1: "e5-1:약분과 통분", 2: "e5-1:약분과 통분", 3: "e5-1:분수의 덧셈과 뺄셈", 4: "e5-1:분수의 덧셈과 뺄셈", 5: "e5-1:분수의 덧셈과 뺄셈"},
    "e-fmul": same("e5-2:분수의 곱셈"),
    "e-fdiv": {1: "e6-1:분수의 나눗셈", 2: "e6-1:분수의 나눗셈", 3: "e6-2:분수의 나눗셈", 4: "e6-2:분수의 나눗셈", 5: "e6-2:분수의 나눗셈"},
    "e-dec": {1: "e3-1:분수와 소수", 2: "e4-2:소수의 덧셈과 뺄셈", 3: "e4-2:소수의 덧셈과 뺄셈", 4: "e4-2:소수의 덧셈과 뺄셈", 5: "e4-2:소수의 덧셈과 뺄셈"},
    "e-dadd": same("e4-2:소수의 덧셈과 뺄셈"),
    "e-dmul": same("e5-2:소수의 곱셈"),
    "e-ddiv": {1: "e6-1:소수의 나눗셈", 2: "e6-1:소수의 나눗셈", 3: "e6-1:소수의 나눗셈", 4: "e6-2:소수의 나눗셈", 5: "e6-2:소수의 나눗셈"},
    "e-fdec": {1: "e4-2:소수의 덧셈과 뺄셈", 2: "e5-1:약분과 통분", 3: "e5-1:약분과 통분", 4: "e5-1:약분과 통분", 5: "e6-1:소수의 나눗셈"},
    "e-angle": same("e4-1:각도"),
    "e-shape": {1: "e4-2:삼각형", 2: "e4-2:삼각형", 3: "e4-2:사각형", 4: "e4-2:사각형", 5: "e4-2:사각형"},
    "e-poly5": same("e5-1:다각형의 둘레와 넓이"),
    "e-circle": {1: "e3-2:원", 2: "e6-2:원의 넓이", 3: "e6-2:원의 넓이", 4: "e6-2:원의 넓이", 5: "e6-2:원의 넓이"},
    "e-box": {1: "e5-2:직육면체", 2: "e5-2:직육면체", 3: "e6-1:직육면체의 부피와 겉넓이", 4: "e6-1:직육면체의 부피와 겉넓이", 5: "e6-1:직육면체의 부피와 겉넓이"},
    "e-prism": same("e6-1:각기둥과 각뿔"),
    "e-rule": {1: "e2-2:규칙 찾기", 2: "e4-1:규칙 찾기", 3: "e4-1:규칙 찾기", 4: "e5-1:규칙과 대응", 5: "e5-1:규칙과 대응"},
    "e-avg": {1: "e5-2:수의 범위와 어림하기", 2: "e5-2:수의 범위와 어림하기", 3: "e5-2:평균과 가능성", 4: "e5-2:평균과 가능성", 5: "e5-2:평균과 가능성"},
    "e-ratio": {1: "e6-1:비와 비율", 2: "e6-2:비례식과 비례배분", 3: "e6-2:비례식과 비례배분", 4: "e6-2:비례식과 비례배분", 5: "e6-1:비와 비율"},
    "m-prime": same("m1-1:소인수분해"), "m-int": same("m1-1:정수와 유리수"),
    "m-expr": same("m1-1:문자와 식"), "m-eq1": same("m1-1:문자와 식"),
    "m-coord": same("m1-1:좌표평면과 그래프"), "m-prop": same("m1-1:좌표평면과 그래프"),
    "m-angle": same("m1-2:기본 도형과 작도"), "m-pgon": same("m1-2:평면도형"), "m-sector": same("m1-2:평면도형"),
    "m-solid": same("m1-2:입체도형"),
    "m-stat": {1: "m1-2:자료의 정리와 해석", 2: "m1-2:자료의 정리와 해석", 3: "m1-2:자료의 정리와 해석", 4: "m3-2:통계", 5: "m3-2:통계"},
    "m-rec": same("m2-1:수와 식의 계산"), "m-exp": same("m2-1:수와 식의 계산"), "m-calc": same("m2-1:수와 식의 계산"),
    "m-ineq": same("m2-1:부등식과 연립방정식"), "m-sys": same("m2-1:부등식과 연립방정식"), "m-lin": same("m2-1:일차함수"),
    "m-iso": same("m2-2:도형의 성질"), "m-quad": same("m2-2:도형의 성질"),
    "m-sim": same("m2-2:도형의 닮음과 피타고라스 정리"),
    "m-pyth": {1: "m2-2:도형의 닮음과 피타고라스 정리", 2: "m2-2:도형의 닮음과 피타고라스 정리", 3: "m2-2:도형의 닮음과 피타고라스 정리", 4: "m3-1:제곱근과 실수", 5: "m3-1:제곱근과 실수"},
    "m-count": same("m2-2:확률"), "m-prob": same("m2-2:확률"),
    "m-root": same("m3-1:제곱근과 실수"),
    "m-expand": same("m3-1:다항식의 곱셈과 인수분해"), "m-fact": same("m3-1:다항식의 곱셈과 인수분해"),
    "m-qeq": same("m3-1:이차방정식"), "m-parab": same("m3-1:이차함수"),
    "m-trig": same("m3-2:삼각비"), "m-circ": same("m3-2:원의 성질"),
    "h-poly": same("h1-1:다항식"), "h-ident": same("h1-1:다항식"), "h-rem": same("h1-1:다항식"),
    "h-cplx": same("h1-1:방정식과 부등식"), "h-disc": same("h1-1:방정식과 부등식"), "h-qmax": same("h1-1:방정식과 부등식"),
    "h-eqs": same("h1-1:방정식과 부등식"), "h-ineqs": same("h1-1:방정식과 부등식"),
    "h-perm": same("h1-1:경우의 수"), "h-matrix": same("h1-1:행렬"),
    "h-line": same("h1-2:도형의 방정식"), "h-circle": same("h1-2:도형의 방정식"), "h-move": same("h1-2:도형의 방정식"),
    "h-set": same("h1-2:집합과 명제"), "h-func": same("h1-2:함수"), "h-ratf": same("h1-2:함수"),
    "h-explog": same("h2-1:지수함수와 로그함수"), "h-expg": same("h2-1:지수함수와 로그함수"),
    "h-trig": same("h2-1:삼각함수"), "h-law": same("h2-1:삼각함수"),
    "h-seq": same("h2-1:수열"), "h-sigma": same("h2-1:수열"),
    "h-lim": same("h2-2:함수의 극한과 연속"), "h-diff": same("h2-2:미분"), "h-int": same("h2-2:적분"), "h-iarea": same("h2-2:적분"),
    "h-count": same("h3-2:경우의 수"), "h-prob": same("h3-2:확률"), "h-dist": same("h3-2:통계"),
    "h-slim": same("h3-1:수열의 극한"), "h-diff2": same("h3-1:미분법"), "h-int2": same("h3-1:적분법"),
    "h-conic": same("h3-3:이차곡선"), "h-vec": same("h3-3:벡터"),
}
EXTRA = {}      # 새 생성기(g_ex.py 등)가 등록하는 TAG — {id: (모듈:함수, {단계: 단원})}
try:
    from weeks_extra import EXTRA
except ImportError:
    pass

SRC = {e[0]: e[3] for e in REG}
for k, (src, tag) in EXTRA.items():
    SRC[k] = src
    TAG[k] = tag
ORDER = {e[0]: i for i, e in enumerate(REG)}
for i, k in enumerate(EXTRA):
    ORDER[k] = 1000 + i

# 단원 → [(생성기 id, 단계)] — 쉬운 차례(단계 번호 → 등록 차례)
STAGES = {}
for sid, tag in TAG.items():
    for st, u in tag.items():
        STAGES.setdefault(u, []).append((sid, st))
for u in STAGES:
    STAGES[u].sort(key=lambda x: (x[1], ORDER.get(x[0], 9999)))

# ── 문항 샘 — 생성기를 SEED_SHIFT 를 바꿔 다시 돌린 결과 ──────────────────────────
_RUNS = {}
_META = {}
def run(sid, shift):
    k = (sid, shift)
    if k not in _RUNS:
        mod, fn = SRC[sid].split(":")
        core.SEED_SHIFT = shift
        try:
            S = getattr(importlib.import_module(mod), fn)()
            _RUNS[k] = S
            _META.setdefault(sid, S)
        except AssertionError:
            _RUNS[k] = None
        finally:
            core.SEED_SHIFT = 0
    return _RUNS[k]

def qkey(it):
    """겹침 판정 — 자료가 그림에 있는 문항(qf)은 발문이 같아도 그림이 다르면 다른 문항"""
    return it["q"] + ("|" + json.dumps(it.get("fig"), ensure_ascii=False, sort_keys=True) if it.get("qf") else "")

CUR = {}        # (sid, st) → 다음에 볼 (shift, index)
def take(sid, st, n, used, ok):
    """생성기 sid 의 st 단계에서 아직 쓰지 않은(발문) 문항 n 개"""
    out = []
    if (sid, st) in DRY:
        return out
    shift, idx = CUR.get((sid, st), (1, 0))
    idle = 0
    while len(out) < n:
        S = run(sid, shift)
        items = [it for it in S.items if it["st"] == st] if S else []
        before = len(out)
        while idx < len(items) and len(out) < n:
            it = items[idx]
            idx += 1
            k = qkey(it)
            if k in used or not ok(it):
                continue
            used.add(k)
            out.append(it)
        if len(out) < n:
            idle = idle + 1 if len(out) == before else 0
            shift, idx = shift + 1, 0
            if idle >= 6:                       # 새 발문이 더 나오지 않는 좁은 생성기 — 말랐다
                DRY.add((sid, st))
                break
    CUR[(sid, st)] = (shift, idx)
    return out

DRY = set()

def meta_of(sid):
    if sid not in _META:
        run(sid, 1)
        if sid not in _META:
            core.SEED_SHIFT = 0
            mod, fn = SRC[sid].split(":")
            _META[sid] = getattr(importlib.import_module(mod), fn)()
    return _META[sid]

def stage_name(sid, st):
    return meta_of(sid).stages[st]

# ── 회차 짜기 ────────────────────────────────────────────────────────────────
def unit_name(u):
    return u.split(":", 1)[1]

TERM_KO = {"e1-1": "초1-1", "e1-2": "초1-2", "e2-1": "초2-1", "e2-2": "초2-2", "e3-1": "초3-1", "e3-2": "초3-2", "e4-1": "초4-1", "e4-2": "초4-2",
           "e5-1": "초5-1", "e5-2": "초5-2", "e6-1": "초6-1", "e6-2": "초6-2", "m1-1": "중1-1", "m1-2": "중1-2", "m2-1": "중2-1", "m2-2": "중2-2",
           "m3-1": "중3-1", "m3-2": "중3-2", "h1-1": "공통수학1", "h1-2": "공통수학2", "h2-1": "대수", "h2-2": "미적분1", "h3-1": "미적분2",
           "h3-2": "확률과 통계", "h3-3": "기하"}

def allocate(units, total):
    """단원마다 회차 수 — 생성기 단계가 많을수록 더(단원마다 2 ~ 12), 합이 total"""
    cov = [u for u in units if STAGES.get(u)]
    if not cov:
        return {}
    w = {u: min(max(len(STAGES[u]), 2), 8) for u in cov}
    W = sum(w.values())
    n = {u: max(2, round(total * w[u] / W)) for u in cov}
    while sum(n.values()) > total:
        u = max(cov, key=lambda x: (n[x] - total * w[x] / W, n[x]))
        n[u] -= 1
    while sum(n.values()) < total:
        u = max(cov, key=lambda x: (total * w[x] / W - n[x], -n[x]))
        n[u] += 1
    return n

def unit_plan(u, k):
    """단원 u 를 k 회차로 — [(종류, [(sid, st) × 5])]"""
    L = STAGES[u]
    g = len(L)
    out = []
    kp = k - 1 if k >= 3 else k
    for j in range(kp):
        a = j * g // kp
        b = max(a + 1, (j + 1) * g // kp)
        seg = L[a:b]
        prev = L[a - 1] if a > 0 else None
        slots = ([prev] if prev and len(seg) < 5 else [])
        while len(slots) < 5:
            slots.extend(seg)
        slots = sorted(slots[:5], key=lambda x: L.index(x))
        kind = "개념" if j == 0 else ("응용" if (j == kp - 1 and kp >= 3) else "연습")
        out.append((kind, slots))
    if k >= 3:
        out.append(("마무리", [L[round(i * (g - 1) / 4)] for i in range(5)]))
    return out[:k]

def mix_plan(units, n, kind, easy=False):
    """여러 단원을 섞은 n 회차 — 회차마다 단원 셋 정도, 단계 다섯"""
    cov = [u for u in units if STAGES.get(u)]
    if not cov:
        return []
    out = []
    per = max(1, math.ceil(len(cov) / n)) if kind == "복습" else 1
    for j in range(n):
        if kind == "복습":
            us = [cov[(j * per + i) % len(cov)] for i in range(min(3, len(cov)))]
            if per == 1:
                us = [cov[(j + i * max(1, len(cov) // 3)) % len(cov)] for i in range(min(3, len(cov)))]
        else:
            us = [cov[j % len(cov)]]
        slots = []
        for i in range(5):
            u = us[i % len(us)]
            L = STAGES[u]
            if easy:
                slots.append(L[min(i // len(us), len(L) - 1)])
            else:
                slots.append(L[round(((i // len(us)) + 1) * (len(L) - 1) / 2) % len(L)] if len(L) > 1 else L[0])
        out.append((kind, sorted(slots, key=lambda x: (us.index(TAG[x[0]][x[1]]) if TAG[x[0]][x[1]] in us else 9, x[1]))))
    return out

def year_plan(t1, t2, nxt):
    """104 회차 — [(기간, 단원 또는 단원들, 종류, slots)]"""
    plan = []
    for period, units, total in (("1학기", t1, 40), ("2학기", t2, 40)):
        n = allocate(units, total)
        body = []
        for u in units:
            if u in n:
                for kind, slots in unit_plan(u, n[u]):
                    body.append((period, u, kind, slots))
        plan.append(body)
    s1, s2 = plan
    summer = [("여름방학", None, k, sl) for k, sl in mix_plan(t1, 6, "복습")] + [("여름방학", None, k, sl) for k, sl in mix_plan(t2, 4, "예습", easy=True)]
    if nxt:
        winter = [("겨울방학", None, k, sl) for k, sl in mix_plan(t1 + t2, 8, "복습")] + [("겨울방학", None, k, sl) for k, sl in mix_plan(nxt, 6, "예습", easy=True)]
    else:
        winter = [("겨울방학", None, k, sl) for k, sl in mix_plan(t1 + t2, 14, "복습")]
    return s1 + summer + s2 + winter

# ── 만들기 ───────────────────────────────────────────────────────────────────
def no_root(it):
    return "√" not in json.dumps(it, ensure_ascii=False)

def build_grade(gk, gname, level, t1, t2, nxt, codes, used_all):
    plan = year_plan(t1, t2, nxt)
    assert len(plan) == 104, (gk, len(plan))
    ok = no_root if gk in ("m1", "m2") else (lambda it: True)
    metas = []
    os.makedirs(f"{OUT}/{gk}", exist_ok=True)
    seq = {}
    for i, (period, u, kind, slots) in enumerate(plan):
        week, slot = 1 + i // 2, "AB"[i % 2]
        sid = f"w-{gk}-{week:02d}{slot.lower()}"
        items, stages, tips = [], {}, {}
        srcs = []
        for stn, (src, st) in enumerate(slots, 1):
            got = take(src, st, 4, used_all, ok)
            if len(got) < 4:                    # 마른 단계 — 같은 단원의 가까운 단계에서 채운다
                u0 = TAG[src][st]
                L = STAGES[u0]
                i0 = L.index((src, st))
                for src2, st2 in sorted(L, key=lambda x: abs(L.index(x) - i0)):
                    if len(got) >= 4:
                        break
                    if (src2, st2) != (src, st):
                        got += take(src2, st2, 4 - len(got), used_all, ok)
                if len(got) < 4:
                    for u2 in [TAG[a][b] for a, b in slots] + list(STAGES):
                        for src2, st2 in STAGES.get(u2, []):
                            if len(got) >= 4 or not src2.startswith(src[0]):
                                break
                            got += take(src2, st2, 4 - len(got), used_all, ok)
                        if len(got) >= 4:
                            break
                assert len(got) == 4, (sid, src, st)
            M = meta_of(src)
            stages[stn] = M.stages[st]
            tips[str(stn)] = M.tips.get(st, M.tips.get(str(st), ""))
            for it in got:
                it2 = dict(it)
                it2["no"] = len(items) + 1
                it2["st"] = stn
                items.append(it2)
            if src not in srcs:
                srcs.append(src)
        units = sorted({TAG[s][st] for s, st in slots}, key=lambda x: [TAG[s][st] for s, st in slots].index(x))
        main = u or units[0]
        if u:
            seq[u] = seq.get(u, 0) + 1
        names = []
        for stn in range(1, 6):
            if stages[stn] not in names:
                names.append(stages[stn])
        if kind in ("복습", "예습"):
            title = (" · ".join(unit_name(x) for x in units[:3])) + (" 복습" if kind == "복습" else " 미리 보기")
        elif kind == "마무리":
            title = f"{unit_name(main)} 마무리"
        else:
            focus = [n for n in names if n != names[0]] if kind != "개념" and len(names) > 1 else names
            title = " · ".join(focus[:2])
        M0 = meta_of(srcs[0])
        pp = max(6, min(10, M0.pp))
        code = codes.get(sid) or "".join(secrets.choice(ALPHA) for _ in range(6))
        codes[sid] = code
        meta = {"id": sid, "gk": gk, "grade": gname, "level": level, "span": gname, "period": period, "week": week, "slot": slot,
                "unit": main, "units": units, "kind": kind, "title": title, "short": f"{gname}-{week}주{slot}",
                "desc": f"{TERM_KO[main.split(':')[0]]} · {unit_name(main)} — " + " → ".join(names[:4]),
                "n": len(items), "code": code, "stages": {str(k): v for k, v in stages.items()}, "src": srcs}
        if u:
            meta["seq"] = seq[u]
        data = {"id": sid, "pp": pp, "note": M0.note, "tips": tips, "items": items}
        json.dump(data, open(f"{OUT}/{gk}/{sid}.json", "w"), ensure_ascii=False, separators=(",", ":"))
        metas.append(meta)
    gaps = [u for u in t1 + t2 if not STAGES.get(u)]
    head = {"gk": gk, "grade": gname, "level": level, "n": len(metas), "gaps": gaps, "sessions": metas}
    json.dump(head, open(f"{OUT}/{gk}/index.json", "w"), ensure_ascii=False, separators=(",", ":"))
    return head

def main(only=None):
    codes = json.load(open(WCODES)) if os.path.exists(WCODES) else {}
    old = json.load(open(CODES)) if os.path.exists(CODES) else {}
    tcodes = os.path.join(os.path.dirname(__file__), "tcodes.json")              # 유형 코드(typetags.py)와도 겹치지 않게
    taken = set(old.values()) | (set(json.load(open(tcodes)).values()) if os.path.exists(tcodes) else set())
    heads = []
    for g in GRADES:
        if only and g[0] not in only:
            continue
        used = set()
        h = build_grade(*g, codes, used)
        _RUNS.clear()
        dup = [c for c in codes.values() if c in taken]
        assert not dup, dup[:3]
        assert len(set(codes.values())) == len(codes), "회차 코드 겹침"
        heads.append(h)
        n_items = sum(m["n"] for m in h["sessions"])
        print(f"  {g[0]} {g[1]} 104회차 · {n_items}문항 · 빈 단원 {len(h['gaps'])} {h['gaps'][:6]}")
        json.dump(codes, open(WCODES, "w"), indent=0)
    return heads

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
