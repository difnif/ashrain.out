# ashrain.out — 스키마 적합도 시험기 (mine_fit.py, v1.0 — 마이닝 2단)
# 위치: itemfactory/mine_fit.py
#
# draft 스키마가 자기 씨드를 실제로 재현하는지 기계 검증한다 (P2·P3의 집행자):
#   ① 씨드 표본(정답 보유 ≤5)에서 하이쿠가 변수 바인딩 추출 {주어진 값들, 구하는 변수}
#   ② sympy가 관계식계에 대입·풀이 → 씨드 정답 재현 채점
#   ③ 특이점 조건("v1 != v2" 등)을 위반시켜 정말 불성립하는지 반례 확인
#   → fit 성적표 기록, 재현율 80%↑(2문항↑)이면 fit_ok, 아니면 fit_fail
#
# 사용:
#   python mine_fit.py run all            # draft 전체 시험
#   python mine_fit.py run m1-1 --limit 5 # 파일럿
#   python mine_fit.py run all --redo     # fit_fail 재시험 포함
#   python mine_fit.py report             # 상태 집계
#   python mine_fit.py selftest           # 오프라인 자가시험 (API·DB 불필요)
# 준비: pip install sympy  ·  .env는 mine_schemas와 동일

import argparse, json, os, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import sympy as sp

HAIKU = "claude-haiku-4-5"

SYS_B = """너는 수학 문항의 변수 바인딩 추출기다. 스키마의 변수 역할과 문항을 보고,
문항에 주어진 값과 구하는 변수를 JSON 하나로만 출력한다. JSON 밖 텍스트 금지.

출력: {"given":{"v1":"4","k":"1/3"},"target":"d","skip":false,"why":""}
규칙:
- 값은 숫자 문자열: 정수 "4", 분수 "1/3", 소수 "0.5". 단위 환산 필요하면 환산해서 (20분→"1/3" 시간).
- target은 스키마 변수 중 정확히 하나. 문항이 스키마 구조와 안 맞으면 {"skip":true,"why":"사유"}.
- 스키마에 없는 변수를 만들지 말 것."""


# ── MathIR 관계식 → sympy ─────────────────────────────────────
FUNS = {"frac": (2, "(({0})/({1}))"), "mixed": (3, "(({0})+(({1})/({2})))"),
        "pow": (2, "(({0})**({1}))"), "root": (2, "(({1})**(1/({0})))"),
        "sqrt": (1, "sqrt({0})"), "abs": (1, "Abs({0})")}

def _split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            if ch == "(": depth += 1
            if ch == ")": depth -= 1
            cur += ch
    out.append(cur)
    return out

def _expand(s):
    for name, (n, tpl) in FUNS.items():
        while True:
            m = re.search(r"\b" + name + r"\(", s)
            if not m: break
            i, depth, j = m.end(), 1, m.end()
            while j < len(s) and depth:
                if s[j] == "(": depth += 1
                elif s[j] == ")": depth -= 1
                j += 1
            args = _split_args(s[i:j-1])
            if len(args) != n: raise ValueError(f"{name} 인자 {len(args)}")
            s = s[:m.start()] + tpl.format(*[_expand(a) for a in args]) + s[j:]
    return s

def ir_expr(s):
    t = _expand(s.strip())
    t = re.sub(r"(\d)\s*([a-zA-Z(])", r"\1*\2", t)   # 2x → 2*x
    t = t.replace(")(", ")*(")
    return sp.sympify(t, rational=True)

def ir_eq(s):
    if re.search(r"(!=|<=|>=|<|>)", s):
        return None                                   # 제약식은 풀이 대상 아님
    L, R = s.split("=", 1)
    return sp.Eq(ir_expr(L), ir_expr(R))

def num(s):
    return sp.nsimplify(sp.sympify(str(s), rational=True))


# ── 핵심 채점 ────────────────────────────────────────────────
def solve_case(relations, given, target):
    eqs = []
    for r in relations:
        try:
            e = ir_eq(str(r))
        except Exception:
            continue
        if e is not None:
            eqs.append(e)
    if not eqs: return None, "관계식 없음"
    sub = {sp.Symbol(k): num(v) for k, v in given.items()}
    eqs = [e.subs(sub) for e in eqs]
    tgt = sp.Symbol(target)
    free = sorted({s for e in eqs for s in e.free_symbols}, key=str)
    if tgt not in free: return None, "target 소거됨"
    try:
        sols = sp.solve(eqs, free, dict=True)
    except Exception as e:
        return None, f"solve 실패 {e}"
    vals = []
    for d in (sols if isinstance(sols, list) else [sols]):
        if tgt in d and not d[tgt].free_symbols:
            vals.append(sp.nsimplify(d[tgt]))
    return (vals or None), (None if vals else "해 없음")

def check_answer(vals, ans_str):
    m = re.search(r"[-+]?[\d./]+", str(ans_str).replace("frac(", "").replace(",", "/").replace(")", ""))
    if not m: return None
    try:
        target = num(m.group(0))
    except Exception:
        return None
    return any(sp.simplify(v - target) == 0 for v in vals)

def check_singularity(relations, cond, given, target):
    """검증 통과한 실제 바인딩 위에서 'A != B'를 위반시켜 정말 모순이 나는지"""
    m = re.match(r"\s*([A-Za-z]\w*)\s*!=\s*([A-Za-z0-9]\w*)\s*", str(cond))
    if not m: return None
    A, B = m.group(1), m.group(2)
    g2 = dict(given)
    if B in ("0",) and A in g2:
        g2[A] = "0"
    elif A in g2 and B in g2:
        g2[B] = g2[A]
    elif A in g2 and not re.match(r"\d", B):
        g2[B] = g2[A]
    else:
        return "미확인(주어진 값 아님)"
    vals, err = solve_case(relations, g2, target)
    return "확인" if vals is None else "재검토(위반해도 해 존재)"


# ── API·DB 배선 ──────────────────────────────────────────────
def call_haiku(system, user):
    import requests
    key = os.environ.get("ANTHROPIC_API_KEY")
    headers = {"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"}
    ws = os.environ.get("ANTHROPIC_WORKSPACE_ID")
    if ws: headers["anthropic-workspace-id"] = ws
    r = requests.post("https://api.anthropic.com/v1/messages", timeout=120, headers=headers,
                      json={"model": HAIKU, "max_tokens": 500,
                            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                            "messages": [{"role": "user", "content": user}]})
    j = r.json()
    if r.status_code != 200:
        raise RuntimeError(j.get("error", {}).get("message", f"api {r.status_code}"))
    return "".join(b.get("text", "") for b in j.get("content", []))


def fit_schema(sb, sc):
    rels = [r for r in (sc.get("relations") or [])]
    if not rels or (sc.get("grade") or "") == "C":
        return None                                   # 시험 비대상
    ids = sc.get("seed_ids") or []
    items = []
    if ids:
        items = sb.table("corpus_items").select("id,question,answer") \
            .in_("id", ids).not_.is_("answer", "null").limit(12).execute().data or []
    items = [i for i in items if str(i.get("answer") or "").strip()][:5]
    detail, passed, tested = [], 0, 0
    ok_case = None
    roles = json.dumps(sc.get("roles") or {}, ensure_ascii=False)
    for it in items:
        try:
            out = call_haiku(SYS_B, f"[스키마 변수] {roles}\n[관계식] {rels}\n[문항] {it['question']}\n[이 문항의 답] {it['answer']}")
            b = json.loads(re.search(r"\{[\s\S]*\}", out).group(0))
            if b.get("skip"):
                detail.append({"ok": None, "why": b.get("why", "skip")}); continue
            vals, err = solve_case(rels, b.get("given") or {}, b.get("target") or "")
            if vals is None:
                tested += 1; detail.append({"ok": False, "why": err}); continue
            ok = check_answer(vals, it["answer"])
            if ok is None:
                detail.append({"ok": None, "why": "답 비수치"}); continue
            tested += 1; passed += ok
            if ok and ok_case is None:
                ok_case = (b.get("given") or {}, b.get("target"))
            detail.append({"ok": bool(ok), "target": b.get("target"),
                           "got": [str(v) for v in vals[:3]], "ans": str(it["answer"])[:40]})
        except Exception as e:
            detail.append({"ok": None, "why": str(e)[:60]})
        time.sleep(0.2)
    sing = []
    if ok_case:
        for c in (sc.get("conditions") or {}).get("singularities", [])[:4]:
            v = check_singularity(rels, c, ok_case[0], ok_case[1])
            if v: sing.append({"cond": str(c)[:50], "res": v})
    fit = {"tested": tested, "passed": passed, "detail": detail, "singularities": sing}
    status = sc["status"]
    if tested >= 2:
        status = "fit_ok" if passed / tested >= 0.8 else "fit_fail"
    sb.table("schemas").update({"fit": fit, "status": status}).eq("id", sc["id"]).execute()
    return tested, passed, status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "report", "selftest"])
    ap.add_argument("unit", nargs="?", default="all")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--redo", action="store_true")
    a = ap.parse_args()

    if a.cmd == "selftest":
        rels = ["d = v1*t1", "d = v2*t2", "t2 - t1 = k"]
        vals, _ = solve_case(rels, {"v1": "3", "v2": "2", "k": "1"}, "d")
        assert vals and check_answer(vals, "6") is True, vals
        assert check_singularity(rels, "v1 != v2", {"v1": "3", "v2": "2", "k": "1"}, "d") == "확인"
        vals2, _ = solve_case(["y = frac(x,4) + 3"], {"x": "8"}, "y")
        assert vals2 and check_answer(vals2, "5"), vals2
        print("자가시험 통과 — 재풀이·채점·반례확인 정상")
        return

    from transcribe_local import load_env, get_client
    load_env(); sb = get_client()

    if a.cmd == "report":
        rows = sb.table("schemas").select("status").execute().data or []
        c = {}
        for r in rows: c[r["status"]] = c.get(r["status"], 0) + 1
        print(" · ".join(f"{k} {v}" for k, v in sorted(c.items())) or "스키마 없음")
        return

    st = ["draft", "fit_fail"] if a.redo else ["draft"]
    q = sb.table("schemas").select("*").in_("status", st).order("unit_id")
    if a.unit != "all": q = q.eq("unit_id", a.unit)
    rows = q.limit(a.limit or 100000).execute().data or []
    print(f"시험 대상 {len(rows)}스키마")
    okc = failc = skipc = 0
    for i, sc in enumerate(rows, 1):
        try:
            r = fit_schema(sb, sc)
            if r is None:
                skipc += 1; continue
            tested, passed, status = r
            mark = "✓" if status == "fit_ok" else ("✗" if status == "fit_fail" else "·")
            okc += status == "fit_ok"; failc += status == "fit_fail"
            print(f"  [{i}/{len(rows)}] {mark} {sc['unit_id']} 「{sc['src_tag'][:24]}」 재현 {passed}/{tested}")
        except Exception as e:
            print(f"  ! {sc['unit_id']} 「{sc['src_tag'][:24]}」 오류 — {str(e)[:60]}")
    print(f"\nfit_ok {okc} · fit_fail {failc} · 비대상(C급 등) {skipc} — 승인대에서 fit_ok부터 도장")


if __name__ == "__main__":
    main()
