# itemfactory/tools/audit.py — 산출된 문항 풀을 시드와 무관하게 다시 검사한다 (v1.0)
#
# genkit의 관문은 '만들면서' 검사한다. 이 감사는 **다 만들어진 JSON만 보고** 다시 검사한다.
# (같은 코드로 두 번 확인하는 것을 피하려고, 여기서는 시드·파라미터를 쓰지 않는다.)
#
#   python tools/audit.py out/gen

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import mathir                                   # noqa: E402
from genkit import figspec                      # noqa: E402
from genkit.labels import MISCONCEPTIONS, validate_labels   # noqa: E402

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out/gen")
problems = Counter()
detail = defaultdict(list)
n = 0
dbkeys = defaultdict(list)
localkeys = defaultdict(list)
seen_item = set()


def bad(code, item, msg=""):
    problems[code] += 1
    if len(detail[code]) < 5:
        detail[code].append(f"{item.get('gen_meta', {}).get('tpl')}#{item.get('gen_meta', {}).get('idx')} {msg}")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


for f in sorted(OUT.glob("*_pool.json")):
    for it in json.loads(f.read_text(encoding="utf-8")):
        n += 1
        # 1. 문법
        for field, code in (("question", "A1-문면문법"),):
            _, _, errs = mathir.parse_text(it[field])
            if errs:
                bad(code, it, str(errs[:1]))
        for c in it.get("choices") or []:
            _, _, e = mathir.parse_text(c)
            if e:
                bad("A2-보기문법", it, c)
        try:
            mathir.parse_answer(it["answer"])
        except Exception as ex:                          # noqa: BLE001
            bad("A3-정답파싱", it, f"{it['answer']} {ex}")
        for s in (it.get("solution") or {}).get("steps", []):
            _, _, e = mathir.parse_text(s)
            if e:
                bad("A4-해설문법", it, s[:40])

        # 2. 보기
        ch = it.get("choices")
        if it["qtype"] == "choice":
            if not ch or len(ch) != 5 or len(set(ch)) != 5:
                bad("B1-보기구성", it)
            elif it["answer"] not in ch:
                bad("B2-정답없음", it)
            dm = (it.get("labels") or {}).get("L42_distractor_map") or {}
            for c in ch or []:
                if c == it["answer"]:
                    continue
                if dm.get(c) not in MISCONCEPTIONS:
                    bad("B3-오개념미사상", it, c)
            # 표기 일관성 — 정답만 다른 꼴이면 형식으로 찍힌다
            pat = lambda s: ("marker" if s.startswith("[[") else "plain")            # noqa: E731
            # 정답만 표기 꼴이 다르면 형식으로 찍힌다 (섞여 있는 것 자체는 무방)
            if ch and sum(1 for c in ch if pat(c) == pat(it["answer"])) == 1:
                bad("B4-정답표기가유일", it, str(ch))
        elif ch:
            bad("B5-단답에보기", it)

        # 3. 도형
        errs = figspec.check_figure_spec(it.get("figure"))
        if errs:
            bad("C1-도형스키마", it, errs[0])
        declared = (it.get("labels") or {}).get("geometry")
        auto = figspec.is_geometry(it.get("figure"), it.get("tags"))
        geo = auto if declared is None else declared
        lv = len((it.get("solution") or {}).get("levels") or [])
        if geo and lv != 2:
            bad("D1-기하인데3단", it)
        if not geo and lv != 3:
            bad("D2-비기하인데2단", it)
        if declared is not None and declared != auto:
            bad("D3-기하판정불일치(경고)", it, f"선언={declared} 자동={auto}")

        # 4. 라벨
        le = validate_labels(it.get("labels") or {})
        if le:
            bad("E1-라벨규격", it, le[0])

        # 5. 중복 — 로컬(문면+보기+도형) / DB(문면+보기)
        if it.get("item_key") in seen_item:
            bad("G1-item_key중복", it, it["item_key"])
        seen_item.add(it.get("item_key"))
        base = norm(it["question"] + " " + (json.dumps(ch, ensure_ascii=False) if ch else ""))
        dbkeys[base].append(it["gen_meta"]["tpl"])
        localkeys[base + " " + json.dumps(it.get("figure"), ensure_ascii=False, sort_keys=True)].append(1)

        # 6. 답이 문면에 그대로 노출되는지 (거저 주는 문항)
        ans = re.sub(r"^\[\[|\]\]$", "", str(it["answer"]))
        if it["qtype"] == "short" and re.fullmatch(r"-?\d+", ans) and re.search(rf"(?<![\d\-\u2212]){re.escape(ans)}(?!\d)", it["question"]):
            bad("F1-답이문면에노출", it, f"answer={ans}")

dup_db = {k: v for k, v in dbkeys.items() if len(v) > 1}
dup_local = {k: v for k, v in localkeys.items() if len(v) > 1}

print(f"감사 대상 {n}건 ({OUT})\n")
if not problems and not dup_db and not dup_local:
    print("  문제 없음")
for code, c in problems.most_common():
    print(f"  {code:<18} {c:>5}건   예: {detail[code][0] if detail[code] else ''}")
print(f"\n  중복(로컬 키: 문면+보기+도형)  {len(dup_local)}건")
print(f"  중복(DB 키:  문면+보기)        {len(dup_db)}건  ← 0이 아니면 DB 반영 시 병합·삭제된다")
if dup_db:
    k = next(iter(dup_db))
    print(f"     예: {k[:90]}…  ({len(dup_db[k])}건)")
hard = {k: v for k, v in problems.items() if "경고" not in k}
sys.exit(1 if (hard or dup_db) else 0)
