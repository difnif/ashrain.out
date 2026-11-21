# 생성기 시험 — 문항 수 · 검산 수 · 단계별 개수 · 겹침 · 그림 · 글자 길이
import sys, importlib, json, re, time as _t
mod, *fns = sys.argv[1:]
M = importlib.import_module(mod)
for fn in fns:
    t0 = _t.time()
    S = getattr(M, fn)()
    n = len(S.items)
    per = [sum(1 for it in S.items if it["st"] == st) for st in range(1, 6)]
    figs = sum(1 for it in S.items if it.get("fig"))
    qf = sum(1 for it in S.items if it.get("qf"))
    ql = max(len(it["q"]) for it in S.items)
    nl = max(len(it["lines"]) for it in S.items)
    size = len(json.dumps(S.items, ensure_ascii=False))
    print(f"{mod}:{fn} {S.title} | {n}문항 {per} 검산 {S.checks} 그림 {figs} qf {qf} | 물음 최장 {ql}자 · 판서 최다 {nl}줄 · {size // 1024}KB · {(_t.time() - t0):.1f}s")
