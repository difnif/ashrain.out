# 생성기 → /tmp/cv/<fn>.json (그려 보기용)
import sys, importlib, json
mod, fn = sys.argv[1:3]
S = getattr(importlib.import_module(mod), fn)()
json.dump({"title": S.title, "stages": S.stages, "items": S.items}, open(f"/tmp/cv/{fn}.json", "w"), ensure_ascii=False)
print(f"/tmp/cv/{fn}.json")
