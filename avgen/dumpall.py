# 등록표 단원 전부(또는 고른 것) → /tmp/cv/all/<id>.json (그림 맞춤 점검용)
import sys, json, importlib
from export import REG
only = set(sys.argv[1:])
for e in REG:
    sid, span, icon, src, desc, old, unit = e
    if only and sid not in only and not any(sid.startswith(o) for o in only):
        continue
    mod, fn = src.split(":")
    try:
        S = getattr(importlib.import_module(mod), fn)()
    except (ModuleNotFoundError, AttributeError) as ex:
        print("아직", sid, src, ex)
        continue
    json.dump({"title": S.title, "stages": S.stages, "items": S.items}, open(f"/tmp/cv/all/{sid}.json", "w"), ensure_ascii=False)
print("ok")
