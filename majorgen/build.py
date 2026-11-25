#!/usr/bin/env python3
# 시록고 「전공 수학」 서가 — 책 데이터 생성기 (서고 › 전공 수학 · src/apps/seirocco/pages/MajorMath.jsx 가 읽는다)
#   python3 majorgen/build.py            모든 책(b_<책 id>.py)
#   python3 majorgen/build.py calc econ  고른 책만 다시 쓰기(목록 index.json 은 늘 전부로)
# 출력: public/majors/index.json · public/majors/<책 id>.json — DB 를 쓰지 않는다(새 표 없음).
# 글 문법: 평문 + **굵게** + MathIR 표식 [[frac(a,b)]] · [[sum(k,1,n,k)]] · [[dinteg(0,1,pow(x,2),x)]] · [[mat(2,2,a,b,c,d)]] …
#   (src/lib/mathir.js — 표식 안에서 나눗셈은 frac, 거듭제곱은 pow. 평문의 1/2 · x/5 는 화면에서 상하로 선다.)
#   빼기는 「−」(U+2212). 평문에 x^2 · a_n 꼴을 쓰지 않는다(위아래 첨자는 ² ³ ⁿ ₀ ₁ 같은 글자로 — 식이 든 지수만 e^(rt) 처럼 괄호로).
# 책: BOOK(id, 제목, 부제, tone=…, who=…, intro=…) 다음에 CH(제목, 요약, 블록 …) 를 차례로.
#   블록 — S(소제목, 문단 …, eq=[공식 줄 …]) · EX(물음, [풀이 줄 …], 답) · PR(물음, 답, hint=…)
import importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "public", "majors")
ORDER = ["calc", "econ", "trade", "mech", "astro", "elec", "data", "phys", "stat"]
TONES = {"teal", "amber", "coral", "violet", "sky", "rose", "lime", "indigo", "slate"}
if __name__ == "__main__":                        # b_*.py 의 「from build import …」가 이 모듈을 쓰도록
    sys.modules.setdefault("build", sys.modules["__main__"])
sys.path.insert(0, HERE)

BOOKS = {}
_cur = [None]


def BOOK(id, title, sub, *, tone, who, intro):
    assert id in ORDER, id
    BOOKS[id] = {"id": id, "title": title, "sub": sub, "tone": tone, "who": who, "intro": intro, "chapters": []}
    _cur[0] = id


def CH(title, summary, *blocks):
    b = BOOKS[_cur[0]]
    b["chapters"].append({"n": len(b["chapters"]) + 1, "title": title, "sum": summary, "blocks": list(blocks)})


def S(h, *p, eq=None):
    return {"k": "s", "h": h, "p": list(p), "eq": list(eq or [])}


def EX(q, steps, ans):
    return {"k": "ex", "q": q, "steps": list(steps), "ans": ans}


def PR(q, ans, hint=""):
    return {"k": "pr", "q": q, "ans": ans, "hint": hint}


# ── 글 검사 ──
MARK = re.compile(r"\[\[[\s\S]*?\]\]")


def texts(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, list):
        return [s for v in x for s in texts(v)]
    if isinstance(x, dict):
        return [s for k, v in x.items() if k not in ("k", "tone", "id") for s in texts(v)]
    return []


def problems(b):
    p, tag = [], b["id"]
    if b["tone"] not in TONES:
        p.append(f"{tag}: tone {b['tone']}")
    if not (5 <= len(b["chapters"]) <= 9):
        p.append(f"{tag}: 장 {len(b['chapters'])}개")
    for c in b["chapters"]:
        t = f"{tag} {c['n']}장"
        ks = [x["k"] for x in c["blocks"]]
        if "s" not in ks: p.append(f"{t}: 이론 단락 없음")
        if "ex" not in ks: p.append(f"{t}: 예제 없음")
        for x in c["blocks"]:
            if x["k"] == "ex" and (len(x["steps"]) < 2 or not x["ans"]): p.append(f"{t}: 예제 풀이 · 답")
            if x["k"] == "pr" and not x["ans"]: p.append(f"{t}: 연습 답")
            if x["k"] == "s" and not x["p"]: p.append(f"{t}: 「{x['h']}」 문단 없음")
    for s in texts(b):
        plain = MARK.sub("", s)
        if s.count("[[") != s.count("]]"): p.append(f"{tag}: [[ ]] 짝 — {s[:40]}")
        if plain.count("**") % 2: p.append(f"{tag}: ** 짝 — {s[:40]}")
        if re.search(r"(^|[\s(=,\[])-\d", plain) or " - " in plain: p.append(f"{tag}: ASCII 빼기 — {s[:40]}")
        if re.search(r"\^(?!\()", plain) or re.search(r"[A-Za-z0-9)]_[A-Za-z0-9{(]", plain): p.append(f"{tag}: 평문에 ^ · _ — {s[:40]}")
        if re.search(r"\d\s*\*\s*\d", plain.replace("**", "")): p.append(f"{tag}: * 곱하기 — {s[:40]}")
    return p


def main(only):
    for bid in ORDER:
        path = os.path.join(HERE, f"b_{bid}.py")
        if os.path.exists(path):
            importlib.import_module(f"b_{bid}")
    bad = [x for b in BOOKS.values() for x in problems(b)]
    if bad:
        print("\n".join(bad))
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    have = [bid for bid in ORDER if bid in BOOKS]
    for bid in have:
        if only and bid not in only:
            continue
        with open(os.path.join(OUT, f"{bid}.json"), "w", encoding="utf-8") as f:
            json.dump(BOOKS[bid], f, ensure_ascii=False, indent=1)
    idx = []
    for bid in have:
        b = BOOKS[bid]
        n_ex = sum(1 for c in b["chapters"] for x in c["blocks"] if x["k"] == "ex")
        n_pr = sum(1 for c in b["chapters"] for x in c["blocks"] if x["k"] == "pr")
        idx.append({"id": bid, "title": b["title"], "sub": b["sub"], "tone": b["tone"], "who": b["who"],
                    "chapters": [c["title"] for c in b["chapters"]], "ex": n_ex, "pr": n_pr})
        print(f"{bid}: 장 {len(b['chapters'])} · 예제 {n_ex} · 연습 {n_pr}")
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"v": 1, "books": idx}, f, ensure_ascii=False, indent=1)
    print(f"합계: 책 {len(have)} · 장 {sum(len(BOOKS[b]['chapters']) for b in have)}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
