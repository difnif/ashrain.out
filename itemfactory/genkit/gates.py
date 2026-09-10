# genkit/gates.py — 생성 문항 5관문 검산 (v1.0)
#
# 불통과는 침묵·미저장(P3). 탈락은 사유 코드와 함께 통계로만 남는다.
#
#   G1 성립 제약   파라미터가 문항이 성립하는 범위 안인가
#   G2 독립 재풀이 정답을 만든 식이 아닌 다른 경로로 정답이 재현되는가 (sympy)
#   G3 오답지 충돌 보기끼리 겹치지 않고, 오답이 우연히 정답이 아닌가
#   G4 mathir 왕복 문면·보기·정답·도형이 v1.5 문법으로 무오류인가 (+ 도형 정규 스키마 v1.6)
#   G5 형식·난이도 해설 단수(기하 2단/그 외 3단)·길이·라벨 규격

from __future__ import annotations

import re
from fractions import Fraction

import sympy as sp

import mathir
from . import figspec
from .expr import ExprError, evaluate, truthy
from .labels import validate_labels

# v1.6 확장 — mathir.FIGS 에 아직 없는 정규 도형(scene·quad).
# 앱에 반영할 때 mathir.py / mathir.js 의 FIGS 에도 같은 두 줄을 넣어야 한다.
FIGS_V16 = dict(mathir.FIGS)
FIGS_V16.setdefault("scene", ["pts"])
FIGS_V16.setdefault("quad", ["v"])
# 해설 전용 도식 (손그림 수준) — 문항 본문에는 figspec 가 막는다
FIGS_V16.setdefault("journey", ["stops"])
FIGS_V16.setdefault("passing", ["obj", "span"])
FIGS_V16.setdefault("bar", [])
FIGS_V16.setdefault("steps", ["lines"])
FIGS_V16.setdefault("wire", ["kind"])
FIGS_V16.setdefault("vessel", [])
FIGS_V16.setdefault("river", [])
FIGS_V16.setdefault("mountain", [])


class Reject(Exception):
    def __init__(self, gate, reason):
        super().__init__(f"{gate}: {reason}")
        self.gate = gate
        self.reason = reason


# ---------------------------------------------------------------- G1
def g1_constraints(tpl: dict, env: dict):
    for c in tpl.get("constraints", []) or []:
        try:
            ok = truthy(c, env)
        except ExprError as e:
            raise Reject("G1", f"제약 평가 실패 {c} ({e})") from e
        if not ok:
            raise Reject("G1", f"제약 위반 {c}")
    for k, v in env.items():
        if isinstance(v, float) and (v != v or abs(v) == float("inf")):
            raise Reject("G1", f"{k} 값이 유한하지 않음")


# ---------------------------------------------------------------- G2
def g2_resolve(tpl: dict, env: dict, answer_val):
    """정답을 만든 식과 다른 경로로 정답을 재현한다."""
    did = False
    rel = tpl.get("relation")
    if rel:
        unk = tpl.get("unknown", "X")
        X = sp.Symbol(unk)
        ns = {k: sp.Rational(v) if isinstance(v, (int, Fraction)) else v for k, v in env.items()}
        ns[unk] = X
        try:
            lhs = sp.sympify(rel, locals=ns)
        except Exception as e:                                   # noqa: BLE001
            raise Reject("G2", f"relation 해석 실패: {e}") from e
        sols = sp.solve(sp.Eq(lhs, 0), X)
        sols = [s for s in sols if not s.free_symbols]
        if not sols:
            raise Reject("G2", "relation 의 해가 없음")
        if len(sols) > 1 and not tpl.get("multi_ok"):
            raise Reject("G2", f"해가 유일하지 않음 ({len(sols)}개) — 조건 부족")
        if answer_val is None:
            raise Reject("G2", "정답이 수치가 아니라 relation 대조 불가")
        if not any(abs(float(s) - float(answer_val)) < 1e-9 for s in sols):
            raise Reject("G2", f"재풀이 결과 {sols} ≠ 정답 {answer_val}")
        did = True
    for v in tpl.get("verify", []) or []:
        try:
            ok = truthy(v, {**env, "ans": answer_val})
        except ExprError as e:
            raise Reject("G2", f"verify 평가 실패 {v} ({e})") from e
        if not ok:
            raise Reject("G2", f"verify 불통과 {v}")
        did = True
    if not did:
        raise Reject("G2", "독립 검증 수단 없음 — relation 또는 verify 를 시드에 선언할 것")


# ---------------------------------------------------------------- G3
def _numify(s):
    """보기 문자열 → 수치(가능하면). 비교용."""
    t = str(s).strip()
    m = re.fullmatch(r"\[\[(.+)\]\]", t, re.S)
    if m:
        t = m.group(1).strip()
    try:
        node, _ = mathir.parse(t)
        v = mathir.ev(node)
        return float(v)
    except Exception:                                            # noqa: BLE001
        return None


def g3_distractors(item: dict, tpl: dict):
    ch = item.get("choices")
    if item["qtype"] != "choice":
        if ch:
            raise Reject("G3", "short 인데 보기가 있음")
        return
    if not isinstance(ch, list) or len(ch) != 5:
        raise Reject("G3", f"보기는 5개여야 함 (현재 {len(ch or [])})")
    if len(set(ch)) != 5:
        raise Reject("G3", "보기 문자열 중복")
    if item["answer"] not in ch:
        raise Reject("G3", "정답이 보기에 없음")
    nums = [_numify(c) for c in ch]
    seen = {}
    for c, n in zip(ch, nums):
        if n is None:
            continue
        key = round(n, 9)
        if key in seen:
            raise Reject("G3", f"보기 값 충돌 {seen[key]!r} ≡ {c!r} (표기만 다름)")
        seen[key] = c
    dm = item.get("_distractor_map") or {}
    for c in ch:
        if c == item["answer"]:
            continue
        if c not in dm or not dm[c]:
            raise Reject("G3", f"오답 {c!r}에 오개념 코드가 없음")


# ---------------------------------------------------------------- G4
def g4_mathir(item: dict):
    _, _, errs = mathir.parse_text(item["question"])
    if errs:
        raise Reject("G4", f"문면 문법 오류 {errs[:2]}")
    for c in item.get("choices") or []:
        _, _, e2 = mathir.parse_text(c)
        if e2:
            raise Reject("G4", f"보기 문법 오류 {c!r} {e2[:1]}")
    try:
        mathir.parse_answer(item["answer"])
    except Exception as e:                                       # noqa: BLE001
        raise Reject("G4", f"정답 파싱 실패 {item['answer']!r} ({e})") from e
    figs = item.get("figure") or []
    for i, f in enumerate(figs):
        fn = f.get("fn")
        if fn not in FIGS_V16:
            raise Reject("G4", f"미지 도형 함수 {fn}")
        for k in FIGS_V16[fn]:
            if k not in (f.get("args") or {}):
                raise Reject("G4", f"figure[{i}] {fn}.{k} 누락")
    spec_errs = figspec.check_figure_spec(figs)
    if spec_errs:
        raise Reject("G4", f"도형 정규 스키마 위반 {spec_errs[:2]}")
    sol = item.get("solution") or {}
    for s in sol.get("steps", []):
        _, _, e3 = mathir.parse_text(s)
        if e3:
            raise Reject("G4", f"해설 문법 오류 {e3[:1]}")
    for lv in sol.get("levels") or []:
        for t in ([lv.get("text")] if lv.get("text") else []):
            _, _, e4 = mathir.parse_text(t)
            if e4:
                raise Reject("G4", f"해설 문법 오류 {e4[:1]}")
        if lv.get("figure"):
            fe = figspec.check_figure_spec(lv["figure"], where="solution")
            if fe:
                raise Reject("G4", f"해설 도식 스키마 위반 {fe[:2]}")
            for f in lv["figure"]:
                fn = f.get("fn")
                if fn not in FIGS_V16:
                    raise Reject("G4", f"해설 도식 미지 함수 {fn}")
    if sol.get("model_answer"):
        _, _, e5 = mathir.parse_text(sol["model_answer"])
        if e5:
            raise Reject("G4", f"모범답안 문법 오류 {e5[:1]}")


# ---------------------------------------------------------------- G5
def g5_shape(item: dict, tpl: dict, geometry: bool, labels: dict):
    q = item.get("question", "")
    if not (5 <= len(q) <= 600):
        raise Reject("G5", f"문면 길이 이상 ({len(q)}자)")
    if not str(item.get("answer", "")).strip():
        raise Reject("G5", "정답 비어 있음")
    sol = item.get("solution") or {}
    if not sol.get("outline") or not sol.get("steps"):
        raise Reject("G5", "해설 규격 위반 (outline·steps 필요)")
    if not (1 <= len(sol["steps"]) <= 8):
        raise Reject("G5", f"해설 단계 수 이상 ({len(sol['steps'])})")
    lv = sol.get("levels") or []
    want = 2 if geometry else 3
    if len(lv) != want:
        raise Reject("G5", f"해설 단수 불일치 — {'기하 2단' if geometry else '비기하 3단'}인데 {len(lv)}단")
    if not sol.get("check"):
        raise Reject("G5", "확인(check) 비어 있음")
    d = tpl.get("difficulty")
    if d not in (1, 2, 3, 4, 5):
        raise Reject("G5", f"난이도는 1~5 (현재 {d})")
    t = tpl.get("time_limit")
    if t is not None and not (10 <= t <= 600):
        raise Reject("G5", f"time_limit 범위 이상 ({t})")
    rb = sol.get("rubric") or {}
    if not rb.get("items"):
        raise Reject("G5", "채점기준(rubric)이 비어 있음")
    if not (5 <= rb.get("total", 0) <= 8):
        raise Reject("G5", f"채점 총점은 5~8점 (현재 {rb.get('total')})")
    if sum(r.get("points", 0) for r in rb["items"]) != rb["total"]:
        raise Reject("G5", "채점 요소 배점의 합이 총점과 다름")
    if not rb.get("checks"):
        raise Reject("G5", "실수거리(pitfalls)가 없음 — 틀마다 조심할 실수를 2개 이상 적을 것")
    if any(c.get("element_no") is None for c in rb["checks"]):
        raise Reject("G5", f"실수거리가 가리키는 채점 요소를 찾지 못함 {[c['text'][:20] for c in rb['checks'] if c.get('element_no') is None]}")
    for r in rb["items"]:
        if not r.get("criterion") or not isinstance(r.get("points"), int) or r["points"] <= 0:
            raise Reject("G5", f"채점 항목 규격 위반 {r}")
    if not sol.get("model_answer") or len(sol["model_answer"]) < 20:
        raise Reject("G5", "모범답안(model_answer)이 비었거나 너무 짧음")
    le = validate_labels(labels)
    if le:
        raise Reject("G5", f"라벨 규격 위반 {le[:2]}")


# ---------------------------------------------------------------- 진입점
GATES = ["G1", "G2", "G3", "G4", "G5"]


def run_all(item, tpl, env, geometry, labels, answer_val):
    g1_constraints(tpl, env)
    g2_resolve(tpl, env, answer_val)
    g3_distractors(item, tpl)
    g4_mathir(item)
    g5_shape(item, tpl, geometry, labels)
