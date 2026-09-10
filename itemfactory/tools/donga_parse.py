# itemfactory/tools/donga_parse.py — 동아출판 22개정 「서술형 문제」 문항·해설·채점기준 구조화 (v1.0)
#
#   python itemfactory/tools/donga_parse.py <hwp5text 출력 txt 폴더> <out.json>
#
# 입력은 hwp5text.py 로 뽑은 텍스트 쌍  "…_서술형문제_N단원.txt" / "…_N단원_해설.txt".
# 출력 항목 = {grade, unit, no, points, stem, subq:[{label, points, text}], answer, solution:[…], rubric:[{step, text, points}]}
#   · 문제 파일: 문항 번호 줄("12") 다음부터 "[표]" 앞까지가 지문. 지문 끝의 "[N점]" 이 배점. "(1) … [k점]" 은 소문항.
#   · 해설 파일: "N [그림] 답" 줄로 문항 시작, 이어 "답" 줄, 풀이 줄(⟦CDOTS⟧➊ 표시), "[표]" 뒤 "채점 기준/배점/➊ 문구/k점…".
# 용도: 채점기준 배점 배분·요소 끊기 참고 전용 (문항 복제·서비스 노출 금지).
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CIRC = "➊➋➌➍➎➏➐➑➒➓"
_PTS = re.compile(r"\[(\d+)점\]")
_SUBQ = re.compile(r"^\((\d)\)\s*(.*)$")
_ITEM_HDR = re.compile(r"^(?:\[그림\]\s*)*(\d{1,2})(?:\s*\[그림\])*$")
_SOL_HDR = re.compile(r"^(?:\[그림\]\s*)*(\d{1,2})(?:\s+(.*)|)$")


def parse_problems(txt: str) -> dict[int, dict]:
    lines = [l.rstrip() for l in txt.splitlines()]
    items, cur, setno, lastno = {}, None, 0, 0
    for l in lines:
        s = l.strip()
        m = _ITEM_HDR.match(s)
        if m and (int(m.group(1)) in (lastno + 1, lastno + 2) or (int(m.group(1)) == 1 and lastno > 1)):
            if int(m.group(1)) == 1:
                setno += 1
            lastno = int(m.group(1))
            cur = {"no": (setno, lastno), "lines": []}
            items[cur["no"]] = cur
            continue
        if cur is not None:
            cur["lines"].append(l)
    out = {}
    for no, it in items.items():
        body, subq, seen_tbl = [], [], False
        for l in it["lines"]:
            s = l.strip()
            if s.startswith("[표]"):
                seen_tbl = True
            if seen_tbl and s in ("[그림]", "답"):
                continue
            if s in ("답",):
                continue
            if re.match(r"^\d\.\d ", s) or s.startswith("학년") or s == "이름" or re.match(r"^\d [가-힣]", s) or s == "[그림]":
                continue
            m = _SUBQ.match(s)
            if m:
                subq.append({"label": f"({m.group(1)})", "text": m.group(2)})
                continue
            if subq and not s.startswith("[표]"):
                subq[-1]["text"] += " " + s
                continue
            if not s.startswith("[표]"):
                body.append(s)
        stem = " ".join(body).strip()
        pts = _PTS.findall(stem)
        points = int(pts[-1]) if pts else None
        stem = _PTS.sub("", stem).strip()
        for q in subq:
            p = _PTS.findall(q["text"])
            q["points"] = int(p[-1]) if p else None
            q["text"] = _PTS.sub("", q["text"]).strip()
        out[no] = {"set": no[0], "no": no[1], "points": points, "stem": stem, "subq": subq}
    return out


def parse_solutions(txt: str) -> dict[int, dict]:
    lines = [l.rstrip() for l in txt.splitlines()]
    sols, cur, prev, setno, lastno = {}, None, None, 0, 0
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        m = _SOL_HDR.match(s)
        if m and (int(m.group(1)) in (lastno + 1, lastno + 2) or (int(m.group(1)) == 1 and lastno > 1)) \
                and (i + 1 < len(lines)) and (lines[i + 1].strip() in ("답", "[그림]") or "[그림]" in s):
            if int(m.group(1)) == 1:
                setno += 1
            lastno = int(m.group(1))
            prev = cur
            cur = {"no": (setno, lastno), "answer": re.sub(r"^\[그림\]\s*", "", (m.group(2) or "")).strip(), "solution": [], "rubric": [], "_mode": "sol", "_tgt": None}
            sols[(setno, lastno)] = cur
            i += 1
            continue
        if cur is not None:
            if s == "답":
                pass
            elif s == "채점 기준":
                # 표 본문이 다음 문항 머리 뒤에 늦게 나오는 경우(HWP 레코드 순서): 현 문항에 풀이가 아직 없고
                # 앞 문항에 채점기준이 없으면 앞 문항의 표다.
                tgt = cur
                if not cur["solution"] and prev is not None and not prev["rubric"]:
                    tgt = prev
                cur["_mode"], cur["_tgt"] = "tbl", tgt
            elif cur["_mode"] == "tbl":
                tgt = cur["_tgt"]
                if s == "배점":
                    pass
                elif s and s[0] in CIRC:
                    tgt["rubric"].append({"step": CIRC.index(s[0]) + 1, "text": s[1:].strip(), "points": None})
                elif re.fullmatch(r"\d+점", s) and tgt["rubric"] and tgt["rubric"][-1]["points"] is None:
                    tgt["rubric"][-1]["points"] = int(s[:-1])
                elif s and tgt["rubric"] and tgt["rubric"][-1]["points"] is None:
                    tgt["rubric"][-1]["text"] += " " + s
                elif s and s != "[표]":
                    cur["_mode"] = "sol"
                    cur["solution"].append(s)
            elif s and s not in ("[그림]", "[표]"):
                cur["solution"].append(s)
        i += 1
    for c in sols.values():
        c.pop("_mode", None)
        c.pop("_tgt", None)
        if c["answer"] in ("", "[그림]"):
            c["answer"] = None
    return sols


def merge(problems: dict, solutions: dict, grade: int, unit: int) -> list[dict]:
    out = []
    for no in sorted(problems):
        p = problems[no]
        s = solutions.get(no, {})
        rub = s.get("rubric", [])
        out.append({"grade": grade, "unit": unit, "set": p["set"], "no": p["no"], "points": p["points"], "stem": p["stem"],
                    "subq": p["subq"], "answer": s.get("answer"), "solution": s.get("solution", []),
                    "rubric": rub, "rubric_sum": sum(r["points"] or 0 for r in rub)})
    return out


def main(folder: str, out: str):
    fd = Path(folder)
    allitems = []
    for pf in sorted(fd.glob("*서술형문제_*단원.txt")):
        m = re.search(r"수학(\d)_서술형문제_(\d)단원", pf.name)
        grade, unit = int(m.group(1)), int(m.group(2))
        sf = pf.with_name(pf.name.replace("단원.txt", "단원_해설.txt"))
        probs = parse_problems(pf.read_text(encoding="utf-8"))
        sols = parse_solutions(sf.read_text(encoding="utf-8")) if sf.exists() else {}
        items = merge(probs, sols, grade, unit)
        ok = sum(1 for it in items if it["rubric"] and it["points"] == it["rubric_sum"])
        print(f"{grade}-{unit}: 문항 {len(items):3d} · 해설 {len(sols):3d} · 배점=채점기준합 {ok:3d}")
        allitems += items
    Path(out).write_text(json.dumps(allitems, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", len(allitems), "→", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
