# 초등 개념 카드 생성기 (elemgen/build.py)
#   python3 elemgen/build.py            모든 학년(g1.py ~ g6.py 에 있는 것)
#   python3 elemgen/build.py e3-2 e4-1   몇 학기만(색인 index.json 은 늘 전부)
# 만드는 것
#   public/concepts/elem/<학기>.json  — 관리자 개념 등록(AdminConcepts)이 그대로 받는 꼴: [{ id, unitId, title, subtitle, order, blocks }]
#   public/concepts/elem/index.json   — { v, units: [학기 …], count } — 관리자 「기본 제공 초등 개념 등록」 단추가 읽는다
#   public/concept-av/<학기>.json      — 개념마다 「▶ 움직이는 예시」 하나(기본기 해설 생성기 avgen 의 문항을 골라 그대로 쓴다)
# 개념 id = <학기>-<단원 번호><차례> (예: e3-2-51 = 초3-2 다섯째 단원 「들이와 무게」의 첫 개념), sort_order 도 같은 수(51) —
#   src/lib/chapters.js 의 초등 대단원 구간(10k ~ 10k + 9)과 맞는다.
# 카드: 왜 필요할까? → 📖 낱말 풀이(뜻 · 이름의 까닭 · 예문) → 핵심 정의 → 이렇게 해요(+ 움직이는 예시) → 💡 왜 그럴까? → ⚠️ 꼭 조심할 것 → ✅ 바로 확인
# 글 규칙: 개념 본문(Rich — **굵게** · ==칠하기== · [[tone:글]])과 같은 문법 · 빼기는 − · 곱하기는 × · 초등이라 √ · 문자식 없음.
import importlib, json, os, re, sys

if __name__ == "__main__":                       # g1.py ~ g6.py 의 「from build import C」가 이 모듈(같은 ALL)을 쓰도록
    sys.modules.setdefault("build", sys.modules["__main__"])

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "avgen"))
sys.path.insert(0, os.path.join(REPO, "cvgen"))

OUT_C = os.path.join(REPO, "public", "concepts", "elem")
OUT_AV = os.path.join(REPO, "public", "concept-av")
UNITS = ["e1-1", "e1-2", "e2-1", "e2-2", "e3-1", "e3-2", "e4-1", "e4-2", "e5-1", "e5-2", "e6-1", "e6-2"]
CH = {  # src/lib/chapters.js 와 같은 차례
    "e1-1": ["9까지의 수", "여러 가지 모양", "덧셈과 뺄셈", "비교하기", "50까지의 수"],
    "e1-2": ["100까지의 수", "덧셈과 뺄셈", "모양과 시각", "규칙 찾기"],
    "e2-1": ["세 자리 수", "여러 가지 도형", "덧셈과 뺄셈", "길이 재기", "분류하기", "곱셈"],
    "e2-2": ["네 자리 수", "곱셈구구", "길이 재기", "시각과 시간", "표와 그래프", "규칙 찾기"],
    "e3-1": ["덧셈과 뺄셈", "평면도형", "나눗셈", "곱셈", "길이와 시간", "분수와 소수"],
    "e3-2": ["곱셈", "나눗셈", "원", "분수", "들이와 무게", "자료의 정리"],
    "e4-1": ["큰 수", "각도", "곱셈과 나눗셈", "평면도형의 이동", "막대그래프", "규칙 찾기"],
    "e4-2": ["분수의 덧셈과 뺄셈", "삼각형", "소수의 덧셈과 뺄셈", "사각형", "꺾은선그래프", "다각형"],
    "e5-1": ["자연수의 혼합 계산", "약수와 배수", "규칙과 대응", "약분과 통분", "분수의 덧셈과 뺄셈", "다각형의 둘레와 넓이"],
    "e5-2": ["수의 범위와 어림하기", "분수의 곱셈", "합동과 대칭", "소수의 곱셈", "직육면체", "평균과 가능성"],
    "e6-1": ["분수의 나눗셈", "각기둥과 각뿔", "소수의 나눗셈", "비와 비율", "여러 가지 그래프", "직육면체의 부피와 겉넓이"],
    "e6-2": ["분수의 나눗셈", "소수의 나눗셈", "공간과 입체", "비례식과 비례배분", "원의 넓이", "원기둥, 원뿔, 구"],
}
ALL = []


def C(unit, ch, k, title, sub, *, need, words, defs, how, why, warn, check, av=None, how_label="이렇게 해요"):
    """개념 하나 — ch: 단원 번호(1부터) · k: 단원 안 차례(1부터)
    av: (생성기 id, 단계, 그 단계에서 몇 번째 그림 문항) 하나, 또는 그런 것의 목록(카드 하나에 예제 1 · 예제 2 … 칩으로), 또는 None"""
    avs = [av] if isinstance(av, tuple) else list(av or [])
    ALL.append(dict(unit=unit, ch=ch, k=k, title=title, sub=sub, need=need, words=words, defs=defs, how=how,
                    how_label=how_label, why=why, warn=warn, check=check, av=avs))


def S(tone, size="md", width="full"):
    return {"size": size, "tone": tone, "width": width}


def icon(e):
    return {"kind": "emoji", "value": e}


def card(c):
    cid = f"{c['unit']}-{c['ch']}{c['k']}"
    bs, n = [], 0

    def nid():
        nonlocal n
        n += 1
        return f"b{n}"

    bs.append({"id": nid(), "icon": icon("🔍"), "type": "text", "label": "왜 필요할까?", "lines": c["need"], "style": S("slate")})
    wl = []
    for w in c["words"]:
        word, mean, why, ex = (list(w) + [""] * 4)[:4]
        s = f"**{word}** — {mean}"
        if why:
            s += f" · {why}"
        if ex:
            s += f" · 예) {ex}"
        wl.append(s)
    bs.append({"id": nid(), "icon": icon("📖"), "type": "text", "label": "낱말 풀이", "lines": wl, "style": S("amber")})
    tones = ["teal", "amber", "violet"]
    for i, d in enumerate(c["defs"]):
        term, hanja, text, chips, chipLabel = (list(d) + [""] * 5)[:5]
        bs.append({"id": nid(), "icon": icon("🎯"), "type": "definition", "label": "핵심 정의", "term": term, "hanja": hanja or "",
                   "text": text, "chips": chips or [], "chipLabel": chipLabel or "", "style": S(tones[i % 3], width="half" if len(c["defs"]) > 1 else "full")})
    mk = "[[av:" + ",".join(f"{cid}-{j + 1}" for j in range(len(c["av"]))) + "]]"
    lines = [mk if ln == "AV" else ln for ln in c["how"]] if c["av"] else [ln for ln in c["how"] if ln != "AV"]
    if c["av"] and "AV" not in c["how"]:
        lines.append(mk)
    bs.append({"id": nid(), "icon": icon("📢"), "type": "text", "label": c["how_label"], "lines": lines, "style": S("violet")})
    bs.append({"id": nid(), "src": "why", "icon": icon("💡"), "type": "text", "label": "왜 그럴까?", "lines": c["why"], "style": S("slate"), "figure": None})
    bs.append({"id": nid(), "icon": icon("⚠️"), "type": "warning", "label": "꼭 조심할 것", "items": c["warn"], "style": S("coral")})
    q, ans = c["check"]
    tns = ["teal", "amber", "violet", "coral"]
    bs.append({"id": nid(), "icon": icon("✅"), "type": "check", "label": "바로 확인", "question": q,
               "answer": [{"group": g, "nums": v, "tone": tns[i % 4]} for i, (g, v) in enumerate(ans)], "style": S("teal")})
    return {"id": cid, "unitId": c["unit"], "title": c["title"], "subtitle": c["sub"], "order": c["ch"] * 10 + c["k"], "blocks": bs}


# ── 글 검사 ──
def text_of(c):
    out = list(c["need"]) + [x for w in c["words"] for x in w] + list(c["how"]) + list(c["why"]) + list(c["warn"]) + [c["check"][0]]
    for d in c["defs"]:
        out += [d[0], d[2]] + list(d[3] or []) + [d[4] if len(d) > 4 else ""]
    out += [x for g in c["check"][1] for x in g] + [c["title"], c["sub"]]
    return [s for s in out if isinstance(s, str)]


def problems(c):
    tag = f"{c['unit']}-{c['ch']}{c['k']}"
    p = []
    if not (1 <= c["ch"] <= len(CH[c["unit"]])):
        p.append(f"{tag}: 단원 번호 {c['ch']}")
    if not (1 <= c["k"] <= 9):
        p.append(f"{tag}: 차례 {c['k']}")
    if not c["why"] or not c["why"][0].startswith("**왜"):
        p.append(f"{tag}: 왜 그럴까? 첫 줄은 「**왜 …?**」")
    for s in text_of(c):
        if s.count("**") % 2: p.append(f"{tag}: ** 짝 — {s[:30]}")
        if s.count("==") % 2: p.append(f"{tag}: == 짝 — {s[:30]}")
        if re.search(r"(^|[\s(=,])-\d", s) or " - " in s: p.append(f"{tag}: ASCII 빼기 — {s[:30]}")
        if "√" in s: p.append(f"{tag}: 초등에 √ — {s[:30]}")
        if re.search(r"\d\s*\*\s*\d", s.replace("**", "")): p.append(f"{tag}: * 곱하기 — {s[:30]}")
    if len(set(c["av"])) != len(c["av"]): p.append(f"{tag}: 같은 움직이는 예시를 두 번 골랐어요")
    if len(c["words"]) < 2: p.append(f"{tag}: 낱말 풀이 2개 이상")
    if not c["defs"]: p.append(f"{tag}: 핵심 정의 없음")
    if not c["warn"]: p.append(f"{tag}: 꼭 조심할 것 없음")
    if not c["check"][1]: p.append(f"{tag}: 바로 확인 답 없음")
    return p


# ── 움직이는 예시 — 기본기 해설 생성기에서 고른다 ──
_SETS = {}
_MODS = {}


def _load(path, name):
    """이름이 겹치는 모듈(avgen/export.py · cvgen/export.py)을 파일 경로로 따로 읽는다"""
    if name not in _MODS:
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _MODS[name] = m
    return _MODS[name]


def gen_set(gid):
    if gid in _SETS:
        return _SETS[gid]
    AREG = _load(os.path.join(REPO, "avgen", "export.py"), "av_export").REG
    from weeks_extra import EXTRA                # avgen/weeks_extra.py
    reg = {r[0]: r[3] for r in AREG}
    reg.update({k: v[0] for k, v in EXTRA.items()})
    mod, fn = reg[gid].split(":")
    S_ = getattr(importlib.import_module(mod), fn)()
    _SETS[gid] = S_
    return S_


def _has_final(ch):
    return "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 != 0


def _josa(x):
    """기본기 해설 생성기 글의 조사 실수 몇 가지를 이 사본에서만 고친다(생성기는 그대로 둔다) — 예: 꼭짓점는 → 꼭짓점은, 다온가 → 다온이"""
    if isinstance(x, str):
        x = x.replace("꼭짓점는", "꼭짓점은").replace("꼭짓점를", "꼭짓점을")
        PEOPLE = _load(os.path.join(REPO, "avgen", "kit.py"), "av_kit").PEOPLE
        for nm in PEOPLE:
            if _has_final(nm[-1]):
                for wrong, right in (("가", "이"), ("는", "은"), ("를", "을"), ("와", "과")):
                    x = re.sub(re.escape(nm) + wrong + r"(?=[\s,.)])", nm + right, x)
        return x
    if isinstance(x, list):
        return [_josa(v) for v in x]
    if isinstance(x, dict):
        return {k: _josa(v) for k, v in x.items()}
    return x


def av_item(c, j=0):
    _plain = _load(os.path.join(REPO, "cvgen", "export.py"), "cv_export").plain   # 판서 문법 → 평문(카드 머리)
    gid, st, k = c["av"][j]
    S_ = gen_set(gid)
    pool = [it for it in S_.items if it["st"] == st]
    figs = [it for it in pool if it.get("fig")]
    use = figs if len(figs) > k else pool
    it = json.loads(json.dumps(use[min(k, len(use) - 1)]))
    cid = f"{c['unit']}-{c['ch']}{c['k']}"
    out = {"id": f"{cid}-{j + 1}", "cid": cid, "q": _josa(it["q"]), "plan": _josa(it["plan"]), "lines": _josa(it["lines"]), "ans": _josa(it["ans"])}
    if it.get("planTag"):
        out["planTag"] = it["planTag"]
    if it.get("fig"):
        out["fig"] = it["fig"]
    out["title"] = _plain(it["plan"])
    out["tab"] = f"예제 {j + 1}"
    out["no"] = ""
    out["src"] = f"{gid}.{st}"
    return out


def load_grades():
    for g in range(1, 7):
        p = os.path.join(HERE, f"g{g}.py")
        if os.path.exists(p):
            importlib.import_module(f"g{g}")


def main(only):
    load_grades()
    bad = [x for c in ALL for x in problems(c)]
    ids = [f"{c['unit']}-{c['ch']}{c['k']}" for c in ALL]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        bad.append(f"id 겹침: {sorted(dup)}")
    if bad:
        print("\n".join(bad))
        sys.exit(1)
    os.makedirs(OUT_C, exist_ok=True)
    os.makedirs(OUT_AV, exist_ok=True)
    have = [u for u in UNITS if any(c["unit"] == u for c in ALL)]
    for u in have:
        if only and u not in only:
            continue
        cs = sorted([c for c in ALL if c["unit"] == u], key=lambda c: (c["ch"], c["k"]))
        cards = [card(c) for c in cs]
        with open(os.path.join(OUT_C, f"{u}.json"), "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=1)
        items = {}
        for c in cs:
            for j in range(len(c["av"])):
                it = av_item(c, j)
                items[it["id"]] = it
        if items:
            with open(os.path.join(OUT_AV, f"{u}.json"), "w", encoding="utf-8") as f:
                json.dump({"unit": u, "v": 1, "items": items}, f, ensure_ascii=False, separators=(",", ":"))
        print(f"{u}: 개념 {len(cards)} · 움직이는 예시 {len(items)}")
    count = 0
    for u in have:
        with open(os.path.join(OUT_C, f"{u}.json"), encoding="utf-8") as f:
            count += len(json.load(f))
    with open(os.path.join(OUT_C, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"v": 1, "units": have, "count": count}, f, ensure_ascii=False)
    print(f"합계: 학기 {len(have)} · 개념 {count}")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
