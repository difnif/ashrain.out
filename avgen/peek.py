# 문항 글 훑어보기: python3 peek.py 모듈 함수 [단계마다 몇 개]
import sys, importlib
mod, fn = sys.argv[1:3]
k = int(sys.argv[3]) if len(sys.argv) > 3 else 2
S = getattr(importlib.import_module(mod), fn)()
for st in range(1, 6):
    its = [it for it in S.items if it["st"] == st][:k]
    for it in its:
        print(f"[{st}] {it['no']}. {it['q']}  ⇒ {it['ans']} (ap {it['ap']}, {it['omr']})")
        print(f"     방침: {it['plan']}")
        for ln in it["lines"]:
            print(f"     · {(ln.get('pre') + ': ') if ln.get('pre') else ''}{ln['s']}{('   ['+ln['memo']+']') if ln.get('memo') else ''}")
