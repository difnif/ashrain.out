# 개념 카드 「움직이는 예제」 → public/concept-av/<단원>.json · cvgen/places.json
#   python3 export.py              모든 단원
#   python3 export.py m1-1 h2-2    몇 단원만(places.json 은 늘 전부 — 다른 단원은 이전 것을 그대로 둔다)
# 단원 파일: u_<단원>.py 의 build(U) 가 U.ex(...) 로 예제를 더한다. 만든 json 은 손으로 고치지 않는다.
import json, os, re, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cv import Unit, REPO, SKIP

UNITS = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"]
OUT = os.path.join(REPO, "public", "concept-av")
PLACES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "places.json")


SUP = str.maketrans("0123456789+−-=()nxyabcdkmptrisehlouvgfzw", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁼⁽⁾ⁿˣʸᵃᵇᶜᵈᵏᵐᵖᵗʳⁱˢᵉʰˡᵒᵘᵛᵍᶠᶻʷ")
SUP_OK = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿˣʸᵃᵇᶜᵈᵏᵐᵖᵗʳⁱˢᵉʰˡᵒᵘᵛᵍᶠᶻʷ")
SUB = str.maketrans("0123456789+−-=()nxyabikmrejhlstpouv", "₀₁₂₃₄₅₆₇₈₉₊₋₋₌₍₎ₙₓᵧₐbᵢₖₘᵣₑⱼₕₗₛₜₚₒᵤᵥ")
SUB_OK = set("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₙₓᵧₐbᵢₖₘᵣₑⱼₕₗₛₜₚₒᵤᵥ")


def _group(s, i):
    """s[i] == '{' — 짝 맞는 '}' 까지의 안쪽과 다음 위치"""
    d, j = 0, i
    while j < len(s):
        d += {"{": 1, "}": -1}.get(s[j], 0)
        if d == 0:
            return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def plain(s):
    """판서 문법(분수 {a/b} · ^{2} · _{1} · √{x} · ⃗{a}) → 글자만 있는 한 줄(카드 머리 · 읽어 주기용)"""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch in "^_√⃗" and i + 1 < len(s) and s[i + 1] == "{":
            inner, i = _group(s, i + 1)
            t = plain(inner)
            if ch == "^":
                sup = t.replace(" ", "").translate(SUP)            # 4 − r → ⁴⁻ʳ
                out.append(sup if all(c in SUP_OK for c in sup) else f"^({t})")
            elif ch == "_":
                sub = t.replace(" ", "").translate(SUB)
                out.append(sub if all(c in SUB_OK for c in sub) else f"({t})")   # lim_{h→0} → lim(h→0)
            elif ch == "√":
                out.append("√" + (t if re.fullmatch(r"[\w.]+", t) else f"({t})"))
            else:
                out.append(t + "⃗")
            continue
        if ch == "{":
            inner, i = _group(s, i)
            d, cut = 0, -1
            for j, c in enumerate(inner):
                d += {"{": 1, "}": -1}.get(c, 0)
                if c == "/" and d == 0:
                    cut = j
                    break
            if cut < 0:
                out.append(plain(inner))
            else:
                a, b = plain(inner[:cut]), plain(inner[cut + 1:])
                wrap = lambda x: x if re.fullmatch(r"[\w.√²³⁰¹⁴-⁹ⁿ⃗]+", x) else f"({x})"
                fr = f"{wrap(a)}/{wrap(b)}"
                out.append(f"({fr})" if s[i:i + 1] in ("'", "^") else fr)   # {f/g}' → (f/g)'
            continue
        out.append(ch)
        i += 1
    return "".join(out).replace("**", "").replace("==", "")


def card_fields(it):
    """머지된 재생 카드(components/ConceptAv.jsx)가 쓰는 칸 — 카드 머리(title) · 고르는 칩(tab) · 판의 번호 없음(no)"""
    k = it["id"].rsplit("-", 1)[1]
    it["title"] = plain(it["plan"])
    it["tab"] = f"예제 {k}"
    it["no"] = ""
    return it


def build(u):
    mod = importlib.import_module("u_" + u.replace("-", "_"))
    U = Unit(u)
    mod.build(U)
    for it in U.items.values():
        card_fields(it)
    return U


def main(argv):
    only = [a for a in argv if not a.startswith("-")]
    units = only or UNITS
    os.makedirs(OUT, exist_ok=True)
    places = json.load(open(PLACES, encoding="utf-8")) if os.path.exists(PLACES) else {}
    total, checks = 0, 0
    for u in units:
        try:
            U = build(u)
        except ModuleNotFoundError as e:
            if e.name == "u_" + u.replace("-", "_"):
                print(f"{u}: 아직")
                continue
            raise
        for k in [k for k, v in places.items() if v["cid"].startswith(u + "-")]:
            del places[k]
        places.update(U.places)
        data = {"unit": u, "v": 1, "items": U.items}
        with open(os.path.join(OUT, f"{u}.json"), "w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, separators=(",", ":"))
        cids = sorted({it["cid"] for it in U.items.values()})
        total += len(U.items)
        checks += U.checks
        print(f"{u}: 예제 {len(U.items)} · 개념 {len(cids)} · 검산 {U.checks}")
    assert not any(v["cid"] in SKIP for v in places.values())
    with open(PLACES, "w", encoding="utf-8") as fp:
        json.dump(dict(sorted(places.items())), fp, ensure_ascii=False, indent=0)
    print(f"합계: 예제 {total} · 검산 {checks} · 자리 {len(places)}")


if __name__ == "__main__":
    main(sys.argv[1:])
