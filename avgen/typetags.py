# 유형별 문제 세트의 유형(단계)마다 — 교과서 단원 꼬리표 · 프린트 코드 → src/features/display/basics/typetags.js
#   유형 = 단원의 한 단계(20문항). 학생앱 목록에 유형마다 한 줄(#/av/<단원>.<단계>), 유형마다 따로 프린트(문제지 · 해설지 · 빠른 정답 · OMR).
#   교과서 단원은 weeks.py 의 TAG(주차별 회차가 쓰는 단계 → 교과서 단원), 코드는 tcodes.json 에 고정(단원 · 회차 코드와 겹치지 않게).
#   python3 typetags.py
import json, os, secrets
from export import REG, CODES, ALPHA, OUT_JS
import weeks

HERE = os.path.dirname(os.path.abspath(__file__))
TCODES = os.path.join(HERE, "tcodes.json")
WCODES = os.path.join(HERE, "wcodes.json")


def main():
    cj = json.load(open(CODES))
    wj = json.load(open(WCODES)) if os.path.exists(WCODES) else {}
    tj = json.load(open(TCODES)) if os.path.exists(TCODES) else {}
    used = set(cj.values()) | set(wj.values()) | set(tj.values())
    rows = []
    for e in REG:
        sid = e[0]
        tag = weeks.TAG[sid]
        cells = []
        for st in range(1, 6):
            k = f"{sid}.{st}"
            if k not in tj:
                while True:
                    c = "".join(secrets.choice(ALPHA) for _ in range(6))
                    if c not in used:
                        break
                tj[k] = c
                used.add(c)
            cells.append(f'{st}: [{json.dumps(tag[st], ensure_ascii=False)}, "{tj[k]}"]')
        rows.append(f'  {json.dumps(sid)}: {{ {", ".join(cells)} }}')
    json.dump(tj, open(TCODES, "w"), indent=1)
    assert len(set(tj.values())) == len(tj) and not (set(tj.values()) & (set(cj.values()) | set(wj.values()))), "코드 겹침"
    src = f"""// ashrain.out — 유형별 문제 세트의 유형(단계)마다 교과서 단원 · 프린트 코드 (basics/typetags.js) — 생성기(avgen/typetags.py)가 만든 파일(손으로 고치지 말 것)
// 유형 = 단원의 한 단계(20문항) — 학생앱 목록에 유형마다 한 줄(#/av/<단원>.<단계>) · 유형마다 따로 프린트(코드는 단원 코드와 다르다).
//   TYPE_TAGS[단원][단계] = [교과서 단원("<학기>:<이름>", lib/units.js), 프린트 코드 6글자]
export const TYPE_TAGS = {{
{",\n".join(rows)},
}};
"""
    open(f"{OUT_JS}/typetags.js", "w").write(src)
    print(f"유형 {len(rows) * 5}가지 · 코드 {len(tj)}개 → {OUT_JS}/typetags.js")


if __name__ == "__main__":
    main()
