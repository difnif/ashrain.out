# itemfactory/tools/seedlib.py — 시드 생성 스크립트 공용 헬퍼 (v1.0 · 2026-09-09)
#
#   from seedlib import sub_all, with_pitfalls, dump, COMMON_APPLY
#
# mkseed_motion.py / mkseed_position.py 에 흩어져 있던 것들을 모았다. 생성 스크립트는
#   모델 정의 → 틀 조립 → with_pitfalls → dump  순서로 쓴다 (실수거리는 pitfalls.py 등록부가 단일 원천).
from __future__ import annotations

import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(HERE, "..", "seeds")


def sub_all(obj, rep: dict):
    """문자열(중첩 구조 포함) 안의 자리표시자를 통째로 치환한다 — 틀 사이의 공통 문장 재사용용."""
    if isinstance(obj, str):
        for a, b in rep.items():
            obj = obj.replace(a, b)
        return obj
    if isinstance(obj, list):
        return [sub_all(x, rep) for x in obj]
    if isinstance(obj, dict):
        return {k: sub_all(v, rep) for k, v in obj.items()}
    return obj


_JOSA_RE = re.compile(r"\{([A-Za-z_][A-Za-z_0-9]*)\}(으로|은|는|이|가|을|를|과|와|로)(?=[\s,.!?)]|$)")
_JOSA_FN = {"은": "eun", "는": "eun", "이": "ika", "가": "ika", "을": "eul", "를": "eul", "과": "wa", "와": "wa", "으로": "ro", "로": "ro"}


def fix_josa(obj):
    """`{name}는` → `{name}{eun(name)}` 처럼 자리표시자 바로 뒤의 조사를 조사 함수로 바꾼다 (문자열 파라미터·수치 모두)."""
    if isinstance(obj, str):
        return _JOSA_RE.sub(lambda m: "{%s}{%s(%s)}" % (m.group(1), _JOSA_FN[m.group(2)], m.group(1)), obj)
    if isinstance(obj, list):
        return [fix_josa(x) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in ("id", "seed_id", "relation", "verify", "constraints", "derive", "params", "table") else fix_josa(v)) for k, v in obj.items()}
    return obj


def _pitfalls_registry():
    spec = importlib.util.spec_from_file_location("pitfalls", os.path.join(HERE, "pitfalls.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.P


def with_pitfalls(seed: dict, *, strict: bool = True) -> dict:
    """틀별 실수거리를 tools/pitfalls.py 등록부에서 가져와 붙인다. 등록이 없으면 (strict) 예외 — G5에서 떨어지기 전에 잡는다.
    조사 자동 보정(fix_josa)도 여기서 한 번에 한다."""
    P = _pitfalls_registry()
    seed["templates"] = [fix_josa(t) for t in seed["templates"]]
    for t in seed["templates"]:
        if t["id"] in P:
            t["pitfalls"] = P[t["id"]]
        elif strict:
            raise SystemExit(f"pitfalls.py 에 {t['id']} 등록이 없다 — 실수거리 2~4개를 먼저 등록할 것")
    return seed


def dump(seed: dict, path: str | None = None) -> str:
    path = path or os.path.join(SEEDS, seed["seed_id"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("→", os.path.relpath(path))
    return path


def steps(lines: list) -> list:
    """해설 판서 도식 한 개 — [{"fn":"steps","args":{"lines":[…]}}]"""
    return [{"fn": "steps", "args": {"lines": lines}}]


def bar(rows: list) -> list:
    """부분·전체 막대 도식 — rows = [{"name","total","parts":[{"label","value","fill"?}]}]"""
    return [{"fn": "bar", "args": {"rows": rows}}]


def table(head: list, rows: list, caption: str | None = None) -> list:
    a = {"head": head, "rows": rows}
    if caption:
        a["caption"] = caption
    return [{"fn": "table", "args": a}]


def numline(lo, hi, points: list, segments: list | None = None) -> list:
    a = {"min": lo, "max": hi, "points": points}
    if segments:
        a["segments"] = segments
    return [{"fn": "numline", "args": a}]


def hl(*keys, keep: bool = False):
    k = list(keys) if len(keys) > 1 else keys[0]
    c = {"act": "hl", "k": k}
    if keep:
        c["keep"] = True
    return c


def reveal(i: int):
    return {"act": "reveal", "k": f"line:{i}"}


# 활용(문장제) 틀의 공통 라벨
COMMON_APPLY = {
    "process": "문제해결",
    "context": "생활맥락",
    "ops": ["방정식", "사칙"],
    "time_limit": 120,
    "points": 5,
}
