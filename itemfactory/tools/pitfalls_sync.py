# itemfactory/tools/pitfalls_sync.py — 시드 JSON 안의 inline pitfalls 를 등록부(tools/pitfalls.py 의 P)에 모은다 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/pitfalls_sync.py            → seeds/*.json 의 틀 중 등록부에 없는 것을 tools/pitfalls.py 의 P 끝에 덧붙인다
#   python itemfactory/tools/pitfalls_sync.py --check    → 덧붙이지 않고 빠진 틀만 센다 (CI 용, 빠진 것이 있으면 exit 1)
#
# 고등부(mkseed_h*.py)·m3 시드는 hsseed.T(..., pitfalls=[...]) 로 틀 안에 실수거리를 inline 으로 쓴다(with_pitfalls(strict=False)).
# 등록부(pitfalls.py)는 "시드 → pitfalls 주입"의 단일 출처로 남겨 두므로, 이 스크립트로 inline 것을 등록부에 옮겨 둘 다 같은 내용을 갖게 한다.
# 이미 등록된 틀은 건드리지 않는다(등록부가 우선). 시드별로 주석 머리를 붙여 어느 생성기에서 왔는지 남긴다.
from __future__ import annotations

import glob
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(HERE, "..", "seeds")
REG = os.path.join(HERE, "pitfalls.py")
ANCHOR = "}\n\n\ndef inject():"


def _registry():
    spec = importlib.util.spec_from_file_location("pitfalls_reg", REG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.P


def _pyq(s):
    return json.dumps(s, ensure_ascii=False)


def collect(P):
    """등록부에 없는 (seed_id, [(tid, pitfalls)]) 목록 — 시드 파일 순."""
    out = []
    for path in sorted(glob.glob(os.path.join(SEEDS, "*.json"))):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        rows = [(t["id"], t["pitfalls"]) for t in d["templates"] if t.get("pitfalls") and t["id"] not in P]
        if rows:
            out.append((d["seed_id"], d.get("title", ""), os.path.basename(path), rows))
    return out


def render(seed_id, title, fname, rows):
    lines = [f"    # ── {seed_id} {title.split(' — ')[0]} ({fname} · pitfalls_sync) ────────────────────────"]
    for tid, pf in rows:
        lines.append(f"    {_pyq(tid)}: [")
        for p in pf:
            lines.append(f"        {{\"text\": {_pyq(p['text'])}, \"on\": {_pyq(p['on'])}, \"effect\": {_pyq(p['effect'])}}},")
        lines.append("    ],")
    return "\n".join(lines) + "\n"


def main(check=False):
    P = _registry()
    todo = collect(P)
    n = sum(len(rows) for *_, rows in todo)
    if check:
        for seed_id, _, fname, rows in todo:
            print(f"  {seed_id:<18} 등록부에 없는 틀 {len(rows)}개  ({fname})")
        print(f"등록부에 없는 틀 {n}개")
        sys.exit(1 if n else 0)
    if not n:
        print("등록부와 시드가 이미 일치한다 (덧붙일 틀 없음)")
        return
    with open(REG, encoding="utf-8") as f:
        src = f.read()
    assert src.count(ANCHOR) == 1, "pitfalls.py 의 P 닫는 위치를 찾지 못했다"
    block = "".join(render(*t) for t in todo)
    src = src.replace(ANCHOR, block + ANCHOR)
    with open(REG, "w", encoding="utf-8") as f:
        f.write(src)
    P2 = _registry()
    assert all(tid in P2 for *_, rows in todo for tid, _ in rows)
    for seed_id, _, fname, rows in todo:
        print(f"  + {seed_id:<18} {len(rows)}틀  ({fname})")
    print(f"등록부에 {n}틀 덧붙임 → {os.path.relpath(REG)}")


if __name__ == "__main__":
    main(check="--check" in sys.argv)
