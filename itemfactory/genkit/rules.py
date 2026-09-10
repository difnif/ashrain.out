# genkit/rules.py — 누적 검증 규칙 (v1.0)
#
# 설계문서 v0.1 §4 "검산이 잡은 버그 4건"을 규칙으로 굳힌 것.
# 새 버그가 나오면 여기에 규칙으로 추가한다 — 문항을 고치는 게 아니라 규칙을 고친다.
#
#   R-01 오답 겉모양 일치      정답이 정수면 오답도 정수 (분수 오답은 계산 없이 배제됨)
#   R-02 오답 값 붕괴 금지     퇴화 파라미터(m=1 등)에서 서로 다른 오개념이 같은 값이 되는 것
#   R-03 오답 ≠ 문면의 수      발문에 그대로 나온 수를 오답으로 쓰지 않는다
#   R-04 비용 계산에 src 포함  주어진 값도 중간값 목록에 넣어야 난이도가 맞다
#   R-05 정답이 문면에 노출 금지
#   R-06 경계 표본 필수        검수는 파라미터 공간의 양끝을 반드시 포함한다 (도구 쪽 규칙)

from __future__ import annotations

import re
from fractions import Fraction

_NUM_IN_TEXT = re.compile(r"(?<![\d.])-?\d+(?:\.\d+)?(?![\d.])")


def shape_of(v) -> str:
    """겉모양 — 정수 / 분수 / 소수 / 그 밖. R-01."""
    if isinstance(v, bool):
        return "기타"
    if isinstance(v, int):
        return "정수"
    if isinstance(v, Fraction):
        return "정수" if v.denominator == 1 else "분수"
    if isinstance(v, float):
        return "정수" if abs(v - round(v)) < 1e-9 else "소수"
    return "기타"


def numbers_in(text: str) -> set:
    """발문에 등장하는 수 (R-03·R-05 용)."""
    out = set()
    for m in _NUM_IN_TEXT.finditer(str(text or "")):
        try:
            out.add(Fraction(m.group(0)))
        except ValueError:
            pass
    return out


def cost_of(v) -> int:
    """중간값 하나의 계산 비용. 설계문서 v0.1 §1 — 정수는 자릿수, 분수는 max(분자 자릿수, 분모/4)."""
    if isinstance(v, bool) or v is None:
        return 0
    if isinstance(v, float):
        v = Fraction(v).limit_denominator(1000)
    if isinstance(v, int):
        return max(1, len(str(abs(int(v)))))
    if isinstance(v, Fraction):
        if v.denominator == 1:
            return max(1, len(str(abs(v.numerator))))
        return max(len(str(abs(v.numerator))), (v.denominator + 3) // 4)
    return 0


def cost_and_level(values) -> tuple:
    """cost = max(중간값별 비용) → 1~5 난이도. cost<=2 하 / 3 중 / >=4 상."""
    costs = [cost_of(v) for v in values]
    cost = max(costs) if costs else 0
    if cost <= 1:
        lv = 1
    elif cost == 2:
        lv = 2
    elif cost == 3:
        lv = 3
    elif cost == 4:
        lv = 4
    else:
        lv = 5
    return cost, lv
