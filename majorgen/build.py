#!/usr/bin/env python3
# 시록고 「전공 수학」 서가 v2 — 책 데이터 생성기 (서고 › 전공 수학 · src/apps/seirocco/pages/MajorMath.jsx 가 읽는다)
#   python3 majorgen/build.py            모든 책(b_<책 id>.py)
#   python3 majorgen/build.py calc ode   고른 책만 다시 쓰기(목록 index.json 은 늘 전부로)
# 출력: public/majors/index.json · public/majors/<책 id>.json — DB 를 쓰지 않는다(새 표 없음).
#
# 글 문법: 평문 + **굵게** + MathIR 표식 [[frac(a,b)]] · [[sum(k,1,n,k)]] · [[dinteg(0,1,pow(x,2),x)]] · [[mat(2,2,a,b,c,d)]] …
#   (src/lib/mathir.js — 표식 안에서 나눗셈은 frac, 거듭제곱은 pow. 평문의 1/2 · x/5 는 화면에서 상하로 선다.)
#   빼기는 「−」(U+2212). 평문에 x^2 · a_n 꼴을 쓰지 않는다(위아래 첨자는 ² ³ ⁿ ₀ ₁ 같은 글자로 — 식이 든 지수만 e^(rt) 처럼 괄호로).
#
# 책 = BOOK(id, 제목, 부제, tone=…, field=…, who=…, intro=…, pre=[먼저 볼 책 id …], v=2) 다음에 CH(…) 를 차례로.
# 장 = CH(제목, 요약, 블록 …, goals=[이 장의 목표 …], terms=[(우리말, 영어, 뜻) …], recap=[한 장 요약 …], pre=[먼저 볼 장 "책:장" …])
# 블록
#   S(소제목, 문단 …, eq=[공식 줄 …])          이론 단락
#   WHY(소제목, 문단 …)                         💡 왜 그럴까 — 직관 · 그림으로 보는 이유
#   DEF(용어, 영어, 문단 …, eq=[…])             📘 정의
#   THM(이름, 내용, proof=[증명 줄 …], eq=[…])   📐 정리 — 증명은 접어 둔다
#   ANIM(종류, 소제목, 보는 법, 값=…)            🎬 움직이는 그림(src/apps/seirocco/pages/majors/anims) — 종류는 ANIMS 목록
#   EX(물음, [풀이 줄 …], 답, note=풀이 포인트)  예제 — 한 줄씩 펼친다
#   PR(물음, 답, hint=…, sol=[풀이 줄 …])        연습 — 힌트 · 답 · 풀이
#   WARN(실수 …)                                ⚠ 흔한 실수 — 「틀린 생각 → 바른 생각」
#   USE(소제목, 문단 …)                         🏭 현장에서 — 이 수학이 실제로 쓰이는 곳
#   TBL(소제목, [머리 칸 …], [[칸 …] …])          표
#   CODE(소제목, 언어, 코드, note=…)            코드(평문 검사 없이 그대로 — 데이터 · 정보 책)
import importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "public", "majors")

# 분야 — 서가의 칸 차례
FIELDS = [
    ("base", "대학수학", "모든 전공의 바탕 — 미적분 · 선형대수 · 미분방정식 · 확률"),
    ("eng", "공학", "기계 · 전자 · 제어 · 신호 · 우주"),
    ("sci", "자연과학 · 의생명", "물리 · 화학 · 생명 · 지구"),
    ("info", "정보 · 데이터 · 인공지능", "알고리즘 · 머신러닝 · 데이터 · 암호"),
    ("soc", "경제 · 경영", "경제 · 무역 · 금융 · 게임 · 경영과학"),
    ("art", "예술 · 디자인", "음악 · 건축 · 디자인"),
]
FIELD_IDS = [f[0] for f in FIELDS]
# 책 차례(서가 차례) — 파일이 있는 책만 싣는다
ORDER = [
    "calc", "mvc", "linalg", "ode", "prob", "stat", "discrete", "analysis", "complex", "numer", "optim",
    "phys", "mech", "elec", "control", "signal", "astro", "chem", "bio", "earth",
    "algo", "ml", "data", "info",
    "econ", "trade", "finance", "game", "orsci",
    "music", "design",
]
TONES = {"teal", "amber", "coral", "violet", "sky", "rose", "lime", "indigo", "slate"}
# 움직이는 그림 종류 — src/apps/seirocco/pages/majors/anims/index.js 의 KINDS 와 같아야 한다(검산이 맞춘다)
ANIMS_FILE = os.path.join(REPO, "src", "apps", "seirocco", "pages", "majors", "anims", "kinds.json")

if __name__ == "__main__":                        # b_*.py 의 「from build import …」가 이 모듈을 쓰도록
    sys.modules.setdefault("build", sys.modules["__main__"])
sys.path.insert(0, HERE)

BOOKS = {}
_cur = [None]


def BOOK(id, title, sub, *, tone, who, intro, field="base", pre=(), v=1):
    assert id in ORDER, id
    assert field in FIELD_IDS, field
    BOOKS[id] = {"id": id, "v": v, "title": title, "sub": sub, "tone": tone, "field": field, "who": who,
                 "intro": intro, "pre": list(pre), "chapters": []}
    _cur[0] = id


def CH(title, summary, *blocks, goals=(), terms=(), recap=(), pre=()):
    b = BOOKS[_cur[0]]
    ch = {"n": len(b["chapters"]) + 1, "title": title, "sum": summary, "blocks": list(blocks)}
    if goals: ch["goals"] = list(goals)
    if terms: ch["terms"] = [list(t) for t in terms]
    if recap: ch["recap"] = list(recap)
    if pre: ch["pre"] = list(pre)
    b["chapters"].append(ch)


def S(h, *p, eq=None):
    return {"k": "s", "h": h, "p": list(p), "eq": list(eq or [])}


def WHY(h, *p):
    return {"k": "why", "h": h, "p": list(p)}


def DEF(term, en, *p, eq=None):
    return {"k": "def", "term": term, "en": en, "p": list(p), "eq": list(eq or [])}


def THM(name, stmt, proof=(), eq=None):
    return {"k": "thm", "name": name, "stmt": stmt, "proof": list(proof), "eq": list(eq or [])}


def ANIM(_kind, _h, _cap, **params):          # 값 이름(h · fn · m …)이 소제목 인자와 겹치지 않도록
    return {"k": "anim", "kind": _kind, "h": _h, "cap": _cap, "p": params}


def EX(q, steps, ans, note=""):
    x = {"k": "ex", "q": q, "steps": list(steps), "ans": ans}
    if note: x["note"] = note
    return x


def PR(q, ans, hint="", sol=()):
    x = {"k": "pr", "q": q, "ans": ans, "hint": hint}
    if sol: x["sol"] = list(sol)
    return x


def WARN(*items):
    return {"k": "warn", "items": list(items)}


def USE(h, *p):
    return {"k": "use", "h": h, "p": list(p)}


def TBL(h, head, rows):
    return {"k": "tbl", "h": h, "head": list(head), "rows": [list(r) for r in rows]}


def CODE(h, lang, code, note=""):
    x = {"k": "code", "h": h, "lang": lang, "code": code.strip("\n")}
    if note: x["note"] = note
    return x


# ── 글 검사 ──
MARK = re.compile(r"\[\[[\s\S]*?\]\]")
SKIP_KEYS = ("k", "tone", "id", "kind", "lang", "code", "field", "pre", "v")


def texts(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, list):
        return [s for v in x for s in texts(v)]
    if isinstance(x, dict):
        out = []
        for k, v in x.items():
            if k in SKIP_KEYS or (k == "p" and isinstance(v, dict)):   # 움직이는 그림의 값(p)은 글이 아니다
                continue
            out += texts(v)
        return out
    return []


def text_problems(tag, s):
    p = []
    plain = MARK.sub("", s)
    if s.count("[[") != s.count("]]"): p.append(f"{tag}: [[ ]] 짝 — {s[:40]}")
    if plain.count("**") % 2: p.append(f"{tag}: ** 짝 — {s[:40]}")
    if re.search(r"(^|[\s(=,\[])-\d", plain) or " - " in plain: p.append(f"{tag}: ASCII 빼기 — {s[:40]}")
    if re.search(r"\^(?!\()", plain) or re.search(r"[A-Za-z0-9)]_[A-Za-z0-9{(]", plain): p.append(f"{tag}: 평문에 ^ · _ — {s[:40]}")
    if re.search(r"\d\s*\*\s*\d", plain.replace("**", "")): p.append(f"{tag}: * 곱하기 — {s[:40]}")
    if re.search(r"\b(undefined|NaN|None|TODO)\b", s): p.append(f"{tag}: 빈 값 — {s[:40]}")
    return p


def load_kinds():
    try:
        with open(ANIMS_FILE, encoding="utf-8") as f:
            return set(json.load(f)["kinds"])
    except FileNotFoundError:
        return set()


def problems(b, kinds):
    p, tag = [], b["id"]
    if b["tone"] not in TONES:
        p.append(f"{tag}: tone {b['tone']}")
    if not (5 <= len(b["chapters"]) <= 10):
        p.append(f"{tag}: 장 {len(b['chapters'])}개")
    for pre in b["pre"]:
        if pre not in ORDER: p.append(f"{tag}: 먼저 볼 책 {pre}")
    v2 = b.get("v", 1) >= 2
    for c in b["chapters"]:
        t = f"{tag} {c['n']}장"
        ks = [x["k"] for x in c["blocks"]]
        if "s" not in ks and "def" not in ks: p.append(f"{t}: 이론 단락 없음")
        if "ex" not in ks: p.append(f"{t}: 예제 없음")
        if v2:
            if len(c.get("goals", [])) < 3: p.append(f"{t}: 목표 3개 이상")
            if len(c.get("terms", [])) < 4: p.append(f"{t}: 용어 4개 이상")
            if len(c.get("recap", [])) < 3: p.append(f"{t}: 요약 3줄 이상")
            if ks.count("ex") < 2: p.append(f"{t}: 예제 2개 이상")
            if ks.count("pr") < 3: p.append(f"{t}: 연습 3개 이상")
            if "anim" not in ks: p.append(f"{t}: 움직이는 그림 없음")
            if "why" not in ks: p.append(f"{t}: 「왜 그럴까」 없음")
            if "warn" not in ks: p.append(f"{t}: 흔한 실수 없음")
            for term in c.get("terms", []):
                if len(term) != 3 or not all(term): p.append(f"{t}: 용어 꼴 {term}")
        for x in c["blocks"]:
            k = x["k"]
            if k == "ex" and (len(x["steps"]) < 2 or not x["ans"]): p.append(f"{t}: 예제 풀이 · 답")
            if k == "pr":
                if not x["ans"]: p.append(f"{t}: 연습 답")
                if v2 and len(x.get("sol", [])) < 1: p.append(f"{t}: 연습 풀이 없음 — {x['q'][:30]}")
            if k in ("s", "why", "use") and not x["p"]: p.append(f"{t}: 「{x['h']}」 문단 없음")
            if k == "def" and not (x["term"] and x["p"]): p.append(f"{t}: 정의 꼴")
            if k == "thm" and not (x["name"] and x["stmt"]): p.append(f"{t}: 정리 꼴")
            if k == "warn" and not x["items"]: p.append(f"{t}: 흔한 실수 비었음")
            if k == "tbl":
                w = len(x["head"])
                if not x["rows"] or any(len(r) != w for r in x["rows"]): p.append(f"{t}: 표 「{x['h']}」 칸 수")
            if k == "anim":
                if kinds and x["kind"] not in kinds: p.append(f"{t}: 움직이는 그림 종류 {x['kind']}")
                if not x["cap"]: p.append(f"{t}: 움직이는 그림 「{x['h']}」 보는 법 없음")
    for s in texts({k: v for k, v in b.items() if k != "chapters"}):
        p += text_problems(tag, s)
    for c in b["chapters"]:
        for s in texts({k: v for k, v in c.items() if k != "blocks"}):
            p += text_problems(tag, s)
        for x in c["blocks"]:
            if x["k"] == "code":
                for s in [x["h"], x.get("note", "")]:
                    p += text_problems(tag, s)
                continue
            if x["k"] == "anim":
                for s in [x["h"], x["cap"]]:
                    p += text_problems(tag, s)
                continue
            for s in texts(x):
                p += text_problems(tag, s)
    return p


def stats(b):
    cnt = lambda k: sum(1 for c in b["chapters"] for x in c["blocks"] if x["k"] == k)
    return {"ex": cnt("ex"), "pr": cnt("pr"), "anim": cnt("anim"), "thm": cnt("thm"), "def": cnt("def")}


def main(only):
    for bid in ORDER:
        path = os.path.join(HERE, f"b_{bid}.py")
        if os.path.exists(path):
            importlib.import_module(f"b_{bid}")
    kinds = load_kinds()
    bad = [x for b in BOOKS.values() for x in problems(b, kinds)]
    if bad:
        print("\n".join(bad[:80]))
        print(f"… 문제 {len(bad)}개")
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    have = [bid for bid in ORDER if bid in BOOKS]
    for bid in have:
        if only and bid not in only:
            continue
        with open(os.path.join(OUT, f"{bid}.json"), "w", encoding="utf-8") as f:
            json.dump(BOOKS[bid], f, ensure_ascii=False, separators=(",", ":"))
    # 남은 옛 책 파일 정리(이름이 바뀐 책)
    for fn in os.listdir(OUT):
        if fn.endswith(".json") and fn != "index.json" and fn[:-5] not in have:
            os.remove(os.path.join(OUT, fn))
    idx = []
    for bid in have:
        b = BOOKS[bid]
        st = stats(b)
        terms = sorted({t[0] for c in b["chapters"] for t in c.get("terms", [])} |
                       {t[1] for c in b["chapters"] for t in c.get("terms", [])})
        idx.append({"id": bid, "v": b.get("v", 1), "title": b["title"], "sub": b["sub"], "tone": b["tone"], "field": b["field"],
                    "who": b["who"], "pre": b["pre"], "chapters": [c["title"] for c in b["chapters"]], **st, "terms": terms})
        print(f"{bid}: 장 {len(b['chapters'])} · 예제 {st['ex']} · 연습 {st['pr']} · 그림 {st['anim']} · 정리 {st['thm']}")
    fields = [{"id": f, "title": t, "sub": s} for f, t, s in FIELDS if any(BOOKS[b]["field"] == f for b in have)]
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"v": 2, "fields": fields, "books": idx}, f, ensure_ascii=False, separators=(",", ":"))
    tot = lambda k: sum(stats(BOOKS[b])[k] for b in have)
    print(f"합계: 책 {len(have)} · 장 {sum(len(BOOKS[b]['chapters']) for b in have)} · 예제 {tot('ex')} · 연습 {tot('pr')} · 그림 {tot('anim')}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
