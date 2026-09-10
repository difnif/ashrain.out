#!/usr/bin/env python3
# tools/ci_select.py — push-items 워크플로의 "무엇을 빌드·반영할지" 결정 (HANDOFF-시드변형-v1 §8-2, 09-11)
#
#   GitHub Actions 에서 itemfactory/ 를 작업 폴더로 실행하고, 결과를 $GITHUB_OUTPUT 형식으로 찍는다.
#     seeds=seeds/m1-2-mean.json seeds/m2-2-centroid.json   ← 빌드 인자(빈 값이면 뒤 단계를 건너뛴다)
#     status=draft                                          ← 업서트 status
#     replace=                                              ← 교체할 틀 목록(dispatch 입력 그대로, push 는 항상 빈 값)
#     mode=changed|all|none|dispatch                        ← 로그용
#
# 규칙
#   · workflow_dispatch : 입력 그대로 (seeds 기본 seeds/*.json · status · replace_templates).
#   · push(main)        : status 는 draft 고정, 교체 없음(추가만).
#       - 엔진이 바뀌었으면 전체 빌드 — itemfactory/genkit/**, itemfactory/mathir.py, itemfactory/tools/pitfalls.py
#       - before 커밋을 알 수 없으면(브랜치 생성·force push·diff 실패) 전체 빌드
#       - 아니면 그 push 에서 추가·수정된 시드(itemfactory/seeds/*.json, 지금도 존재하는 것)만
#       - 시드 삭제·이름 변경만 있었으면 빌드하지 않는다(seeds 빈 값). 옛 문항 정리는 dispatch 의 replace_templates 로.
#
#   로컬 시험:  GITHUB_EVENT_NAME=push BEFORE=<sha> AFTER=<sha> python tools/ci_select.py

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # itemfactory/
ROOT = HERE.parent                                     # 저장소 루트
SEED_DIR = "itemfactory/seeds/"
ENGINE_PREFIX = ("itemfactory/genkit/",)
ENGINE_FILES = {"itemfactory/mathir.py", "itemfactory/tools/pitfalls.py"}
ZERO = "0" * 40


def changed_files(before: str, after: str) -> list[str] | None:
    """before..after 에서 바뀐 경로(저장소 루트 기준). 구할 수 없으면 None."""
    if not before or not after or before == ZERO:
        return None
    try:
        out = subprocess.run(["git", "diff", "--name-only", before, after, "--", "itemfactory"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def select(event: str, before: str, after: str, in_seeds: str, in_status: str, in_replace: str) -> dict:
    if event == "workflow_dispatch":
        return {"seeds": (in_seeds or "").strip() or "seeds/*.json",
                "status": (in_status or "draft").strip() or "draft",
                "replace": " ".join((in_replace or "").replace(",", " ").split()),
                "mode": "dispatch"}
    # push
    files = changed_files(before, after)
    if files is None:
        return {"seeds": "seeds/*.json", "status": "draft", "replace": "", "mode": "all (diff 불가)"}
    if any(f.startswith(ENGINE_PREFIX) or f in ENGINE_FILES for f in files):
        return {"seeds": "seeds/*.json", "status": "draft", "replace": "", "mode": "all (엔진 변경)"}
    seeds = sorted({f for f in files if f.startswith(SEED_DIR) and f.endswith(".json") and (ROOT / f).is_file()})
    if not seeds:
        return {"seeds": "", "status": "draft", "replace": "", "mode": "none (빌드할 시드 없음 — 삭제·이름 변경만)"}
    return {"seeds": " ".join("seeds/" + Path(f).name for f in seeds), "status": "draft", "replace": "",
            "mode": f"changed ({len(seeds)}개 시드)"}


def main() -> None:
    env = os.environ.get
    sel = select(env("GITHUB_EVENT_NAME", "push"), env("BEFORE", ""), env("AFTER", ""),
                 env("INPUT_SEEDS", ""), env("INPUT_STATUS", ""), env("INPUT_REPLACE", ""))
    lines = [f"{k}={v}" for k, v in sel.items()]
    print("\n".join(lines))
    out = env("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
    print(f"\n[ci_select] {sel['mode']} · status={sel['status']} · seeds={sel['seeds'] or '(없음)'}"
          + (f" · replace={sel['replace']}" if sel["replace"] else ""), file=sys.stderr)


if __name__ == "__main__":
    main()
