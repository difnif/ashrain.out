# ashrain.out — 문항 틀: m1-1-01 소수와 합성수 (v1.0)
# 위치: itemfactory/templates/m1_1_01.py
# 근거 자료: concepts.m1-1-01 카드 (정의: 약수 2개=소수 / 3개 이상=합성수, 주의: 1은 어느 쪽도 아님,
#           짝수 소수는 2뿐, 홀수 합성수 존재) — 표현·범위를 카드 어법에 맞춤.

import math

CID = "m1-1-01"
TITLE = "소수와 합성수"


# ---------------------------------------------------------------- 수학 유틸
def _sieve(n):
    s = [True] * (n + 1)
    s[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i:: i] = [False] * len(s[i * i:: i])
    return s

_S = _sieve(300)
PRIMES_150 = [i for i in range(2, 151) if _S[i]]                     # 35개
PI = [0] * 301                                                        # PI[n] = n 이하 소수 개수
for _i in range(1, 301):
    PI[_i] = PI[_i - 1] + (1 if _S[_i] else 0)

def _is_prime(n):
    return _S[n]

def _eul(n):
    """숫자 읽기 끝소리 기준 을/를 — 0·1·3·6·7·8(받침 있음)→을, 2·4·5·9→를."""
    return "을" if int(str(n)[-1]) in (0, 1, 3, 6, 7, 8) else "를"

def _smallest_factor(n):
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return d
    return n

# 함정형 홀수 합성수 24개 (9=3², 49=7², 91=7×13, 119=7×17, 121=11², 133=7×19, 143=11×13 …)
ODD_COMPS = [9, 15, 21, 25, 27, 33, 35, 39, 49, 51, 55, 57,
             63, 65, 77, 85, 87, 91, 95, 117, 119, 121, 133, 143]

def _comb_unrank(n, k, r):
    """C(n,k) 사전식 순위 r → 오름차순 인덱스 조합 (전단사)."""
    out, x = [], 0
    for j in range(k):
        c = x
        while True:
            cnt = math.comb(n - 1 - c, k - 1 - j)
            if r < cnt:
                break
            r -= cnt
            c += 1
        out.append(c)
        x = c + 1
    return out

_C244 = math.comb(len(ODD_COMPS), 4)          # 10626


# ---------------------------------------------------------------- T1 판별 (short, 난이도1)
def _t1_params(i):
    return {"N": 2 + i}                        # 2..199

def _t1_render(p):
    N = p["N"]
    if _is_prime(N):
        ans, sol = "소수", {
            "outline": "약수가 정확히 2개인지 확인한다",
            "steps": [f"2, 3, 5, 7, …의 소수로 {N}{_eul(N)} 차례로 나눠 본다",
                      f"√{N} 이하의 어떤 소수로도 나누어떨어지지 않는다",
                      f"약수가 1과 {N}뿐(2개)이므로 소수"],
            "check": f"약수 나열: 1, {N} — 정확히 2개",
        }
    else:
        a = _smallest_factor(N)
        ans, sol = "합성수", {
            "outline": "1과 자기 자신 외의 약수를 하나 찾는다",
            "steps": [f"{N} = {a} × {N // a} 로 나누어떨어진다",
                      f"1과 {N} 외에 {a}라는 약수가 더 있다",
                      "약수가 3개 이상이므로 합성수"],
            "check": f"약수에 1, {a}, {N}이 포함 — 3개 이상",
        }
    return {"question": f"다음 수가 소수인지 합성수인지 쓰시오.\n{N}",
            "answer": ans, "answer_alt": [], "solution": sol, "ans_type": "단어"}

def _t1_verify(item, p):
    N = p["N"]
    assert 2 <= N <= 199
    assert (item["answer"] == "소수") == _is_prime(N)


# ---------------------------------------------------------------- T2 보기 고르기 (choice, 난이도2)
def _t2_params(i):
    p = PRIMES_150[i // _C244]
    comps = [ODD_COMPS[j] for j in _comb_unrank(len(ODD_COMPS), 4, i % _C244)]
    return {"p": p, "comps": comps}

def _t2_render(pr):
    p, comps = pr["p"], pr["comps"]
    nums = sorted([p] + comps)
    steps = []
    for c in sorted(comps):
        a = _smallest_factor(c)
        steps.append(f"{c} = {a} × {c // a} → 합성수")
    steps.append(f"{p}는 1과 {p} 외의 약수가 없다 → 소수")
    return {"question": "다음 중 소수인 것은?",
            "choices": [str(n) for n in nums],
            "answer": str(p), "answer_alt": [],
            "solution": {"outline": "각 수를 나누어 보아 약수가 2개뿐인 수를 가려낸다",
                         "steps": steps,
                         "check": f"{p}의 약수는 1, {p}뿐 — 정확히 2개"},
            "ans_type": "보기값"}

def _t2_verify(item, pr):
    p, comps = pr["p"], pr["comps"]
    assert _is_prime(p)
    assert all(not _is_prime(c) and c % 2 == 1 for c in comps)
    assert len(set([p] + comps)) == 5
    assert item["answer"] == str(p) and item["answer"] in item["choices"]


# ---------------------------------------------------------------- T3 소수 개수 (short, 난이도2)
def _t3_params(i):
    return {"N": 10 + i}                       # 10..60

def _t3_render(p):
    N = p["N"]
    primes = [k for k in range(2, N + 1) if _is_prime(k)]
    cnt = len(primes)
    return {"question": f"1부터 {N}까지의 자연수 중에서 소수는 모두 몇 개인지 구하시오.",
            "answer": str(cnt), "answer_alt": [f"{cnt}개"],
            "solution": {"outline": "소수를 빠짐없이 나열해 센다",
                         "steps": [f"{N} 이하의 소수: " + ", ".join(map(str, primes)),
                                   "1은 소수가 아니므로 세지 않는다",
                                   f"모두 {cnt}개"],
                         "check": f"나열한 수가 전부 약수 2개짜리인지 훑기 — {cnt}개"},
            "ans_type": "정수"}

def _t3_verify(item, p):
    assert int(item["answer"]) == PI[p["N"]]


# ---------------------------------------------------------------- T4 개념 진위 (choice, 난이도3)
TRUES = [
    ("가장 작은 소수는 2이다", "1은 소수가 아니므로 2가 최소"),
    ("짝수인 소수는 2뿐이다", "다른 짝수는 모두 2로 나누어떨어진다"),
    ("소수의 약수는 정확히 2개이다", "1과 자기 자신"),
    ("1은 소수도 아니고 합성수도 아니다", "약수가 1개뿐"),
    ("합성수는 약수가 3개 이상이다", "1과 자기 자신 외의 약수가 더 있다"),
    ("10 이하의 소수는 모두 4개이다", "2, 3, 5, 7"),
]
FALSES = [
    ("1은 소수이다", "1은 약수가 1개뿐 — 소수도 합성수도 아니다"),
    ("모든 소수는 홀수이다", "2는 짝수인 소수다"),
    ("서로 다른 두 소수의 곱은 소수이다", "2 × 3 = 6은 합성수다"),
    ("홀수는 모두 소수이다", "9 = 3 × 3은 홀수인 합성수다"),
    ("가장 작은 합성수는 6이다", "4 = 2 × 2가 더 작다"),
    ("연속한 두 자연수가 모두 소수인 경우는 없다", "2와 3은 연속한 소수다"),
    ("모든 합성수는 짝수이다", "9, 15는 홀수인 합성수다"),
    ("20 이하의 소수는 모두 9개이다", "2, 3, 5, 7, 11, 13, 17, 19의 8개다"),
]
_C84 = math.comb(len(FALSES), 4)               # 70

def _t4_params(i):
    t_idx = i // _C84
    fs = _comb_unrank(len(FALSES), 4, i % _C84)
    return {"t": t_idx, "fs": fs, "rot": i % 5}

def _t4_render(p):
    true_s = TRUES[p["t"]]
    false_s = [FALSES[j] for j in p["fs"]]
    ordered = [true_s] + false_s
    r = p["rot"]
    ordered = ordered[r:] + ordered[:r]
    steps = [f"'{s}' — {why} → {'참' if (s, why) == true_s else '거짓'}"
             for (s, why) in ordered]
    return {"question": "소수와 합성수에 대한 설명으로 옳은 것은?",
            "choices": [s for (s, _) in ordered],
            "answer": true_s[0], "answer_alt": [],
            "solution": {"outline": "문장마다 반례가 있는지 하나씩 검증한다",
                         "steps": steps,
                         "check": f"반례가 하나라도 있으면 거짓 — 참은 '{true_s[0]}' 하나뿐"},
            "ans_type": "보기문장"}

def _t4_verify(item, p):
    assert item["answer"] == TRUES[p["t"]][0]
    false_texts = {s for (s, _) in FALSES}
    others = [c for c in item["choices"] if c != item["answer"]]
    assert len(others) == 4 and all(c in false_texts for c in others)
    assert len(set(item["choices"])) == 5


# ---------------------------------------------------------------- 등록
TEMPLATES = [
    {"id": "m1-1-01-t1", "title": "소수·합성수 판별", "qtype": "short", "difficulty": 1,
     "time_limit": 30, "tags": ["소수판별"], "pool_target": 120, "space": 198,
     "spec": {"desc": "N(2~199)이 소수인지 합성수인지 판별"},
     "params_at": _t1_params, "render": _t1_render, "verify": _t1_verify},
    {"id": "m1-1-01-t2", "title": "보기에서 소수 고르기", "qtype": "choice", "difficulty": 2,
     "time_limit": 60, "tags": ["소수판별", "보기고르기"], "pool_target": 160, "space": len(PRIMES_150) * _C244,
     "spec": {"desc": "소수 1개 + 함정형 홀수 합성수 4개 중 소수 고르기"},
     "params_at": _t2_params, "render": _t2_render, "verify": _t2_verify},
    {"id": "m1-1-01-t3", "title": "소수의 개수 세기", "qtype": "short", "difficulty": 2,
     "time_limit": 60, "tags": ["소수개수"], "pool_target": 51, "space": 51,
     "spec": {"desc": "1~N(10~60) 중 소수의 개수"},
     "params_at": _t3_params, "render": _t3_render, "verify": _t3_verify},
    {"id": "m1-1-01-t4", "title": "개념 진위 판단", "qtype": "choice", "difficulty": 3,
     "time_limit": 90, "tags": ["개념진위"], "pool_target": 69, "space": len(TRUES) * _C84,
     "spec": {"desc": "참 1문장 + 거짓 4문장에서 옳은 것 고르기"},
     "params_at": _t4_params, "render": _t4_render, "verify": _t4_verify},
]
