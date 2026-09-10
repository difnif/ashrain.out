# genkit/rubric.py — 서술형 채점기준 v3 (v1.2)
#
# 참고 자료: 경기도교육청 「2026 중등 정기시험 논술형 평가 도구(수학과)」·「2025 중등 교과별 논술형 평가 문항(수학)」·
#            「2025 경기 논술형 평가 도구 2차(수학)」의 채점기준표(채점 요소 × 수행 수준)와 '채점 시 유의점'.
#            발췌·분석은 itemfactory/reference/gyeonggi/ 에 있다.
#
# 규칙 (Park, 2026-09-07 확정 · 09-08 보정 · 09-08 저녁 동아출판 855문항 통계로 재보정)
#   · 배점은 문항당 5~8점. 핵심 채점 요소 2~4개에만 점수를 두고, 요소마다 수행 수준(정확 / 부분 / 0)을 적는다.
#     2요소 5점 · 3요소 7점(**활용은 8점: 식 세우기 3 | 해 구하기 3 | 답 구하기 2** — 동아출판 표준형) · 4요소 8점.
#   · **논리 전제형 실수거리는 요소로 승격**(pitfall `as_element: true`): "구하는 수는 (a, b의 공배수)+1 꼴임" 처럼
#     빠지면 풀이 자체가 서지 않는 진술은 동아·교육청 모두 감점이 아니라 첫 요소(최대 배점)로 둔다. reference/donga/README.md.
#     — 교육청 채점기준표의 '채점 요소 | 배점 | 수행 수준' 구조와 같다. 0점 수준은 언제나 "무응답 또는 그 외 오답".
#   · **감점 요인 = 그 문항에서 조심해야 할 실수거리**(checks). 빠지면 논리가 끊기는 진술, 선후가 뒤바뀌기 쉬운 성질,
#     바꿔 쓰기 쉬운 두 값 같은 것들을 시드가 틀마다 적는다(`pitfalls`). 채점자는 이걸 보고 해당 요소를 부분/불인정으로 매긴다.
#     일반적인 감점표(계산 실수 −1 같은 것)는 두지 않는다 — 그런 것은 아래 '채점 원칙'이 다룬다.
#   · 채점 원칙(principles)은 교육청 유의점에서 반복되는 것 다섯 가지를 공통으로 붙인다.
#
# 시드 형식
#   "rubric":  [{"element", "points", "criterion", "partial"?}, …]   ← 핵심 요소만 (검토·답 제시·단위 요소는 걸러진다)
#   "pitfalls": [{"text": "…", "on": "요소 이름 일부", "effect": "부분" | "불인정"}, …]
#   "rubric_total": 5~8 (선택)
from __future__ import annotations

import math
import re

MIN_TOTAL, MAX_TOTAL = 5, 8
ZERO_LEVEL = "무응답 또는 그 외 오답"
# 점수 요소에서 걸러 내는 것들 (v2 이전 시드 호환) — 이들은 요소가 아니라 채점 원칙·실수거리로 다룬다
_DROP = ("검토", "확인", "답 제시", "답만", "단위")

# 공통 채점 원칙 — 경기도교육청 자료의 '채점 시 유의점'에서 반복되는 것
PRINCIPLES = [
    "예시 답안과 풀이 방법이 다르더라도 수학적으로 타당하고 논리적 오류가 없으면 정답으로 인정한다.",
    "앞 단계의 오류를 그대로 이어받아 뒤 단계를 옳게 수행했으면, 뒤 단계는 독립적으로 인정한다.",
    "개념 이해의 오류와 단순 계산 실수·필기 실수(오타)를 구분해 채점하며, 단순 필기 실수는 감점하지 않는다.",
    "풀이 과정을 서술하는 요소는 과정 없이 결과만 쓴 경우 인정하지 않는다.",
    "단위 표기는 성취기준이 단위 자체가 아니면 채점에 반영하지 않는다.",
]


def _target(n_items: int, kind: str = "활용") -> int:
    """핵심 요소 개수 → 총점. 2개 5점 · 3개 7점(활용 8점) · 4개 이상 8점."""
    if n_items <= 2:
        return 5
    if n_items == 3:
        return MAX_TOTAL if kind == "활용" else 7
    return MAX_TOTAL


def _rescale(points: list, target: int) -> list:
    """비례 배분 + 최대 나머지법. 모든 요소는 최소 1점."""
    tot = sum(points) or 1
    raw = [p * target / tot for p in points]
    base = [max(1, math.floor(r)) for r in raw]
    while sum(base) > target:                       # 최소 1점 보장 때문에 넘친 경우
        i = max(range(len(base)), key=lambda j: base[j])
        base[i] -= 1
    rem = target - sum(base)
    order = sorted(range(len(raw)), key=lambda j: -(raw[j] - math.floor(raw[j])))
    for j in order[:rem]:
        base[j] += 1
    return base


def _scale_partial(text: str | None, old: int, new: int) -> str | None:
    """부분점수 문구의 'N점' 을 새 배점 비율로 고친다 (최소 1점, 새 배점 미만)."""
    if not text:
        return None

    def rep(m):
        n = int(m.group(1))
        k = max(1, min(new - 1 if new > 1 else 1, round(n * new / old))) if old else 1
        return f"{k}점"
    return re.sub(r"(\d+)점", rep, text)


def _default_partial(points: int) -> str | None:
    """부분 수준 문구가 없을 때 — 배점이 2 이상이면 일반 문구."""
    if points <= 1:
        return None
    return f"과정의 일부만 옳거나 근거 서술이 부족하면 {max(1, points // 2)}점."


def normalize(items: list, *, kind: str = "활용", pitfalls: list | None = None, total: int | None = None,
              has_unit: bool = True) -> dict:
    """요소 배열 → v3 채점기준. items[i] = {element, points, criterion, partial?} · pitfalls[i] = {text, on?, effect?}"""
    core = [dict(r) for r in items
            if not any(k in str(r.get("element", "")) for k in _DROP) and str(r.get("element", "")).strip() != "답"]
    if not core:                                    # 전부 걸러졌으면 원본 유지
        core = [dict(r) for r in items]
    # 논리 전제형 실수거리 → 첫 요소로 승격 (배점은 기존 요소 최대치와 같게, 이후 비례 배분)
    promoted = [p for p in (pitfalls or []) if p.get("as_element")]
    pitfalls = [p for p in (pitfalls or []) if not p.get("as_element")]
    top = max((int(r.get("points", 1)) for r in core), default=3)
    for p in reversed(promoted):
        core.insert(0, {"element": p.get("element") or p["text"], "points": top,
                        "criterion": p.get("criterion") or f"{p['text']} — 이 진술(근거)을 풀이에 적었다.",
                        "partial": p.get("partial")})
    target = total or _target(len(core), kind)
    target = max(MIN_TOTAL, min(MAX_TOTAL, target))
    olds = [int(r.get("points", 1)) for r in core]
    news = _rescale(olds, target)
    out = []
    for i, (r, o, n) in enumerate(zip(core, olds, news), 1):
        out.append({"no": i, "element": r["element"], "points": n, "criterion": r["criterion"],
                    "partial": _scale_partial(r.get("partial"), o, n) or _default_partial(n),
                    "zero": ZERO_LEVEL})
    checks = []
    for p in (pitfalls or []):
        on = str(p.get("on") or "")
        no = next((x["no"] for x in out if on and on in x["element"]), None)
        eff = p.get("effect") or "부분"
        checks.append({"text": p["text"], "element_no": no, "effect": eff})
    principles = [x for x in PRINCIPLES if has_unit or "단위" not in x]
    return {"total": target, "items": out, "checks": checks, "principles": principles}
