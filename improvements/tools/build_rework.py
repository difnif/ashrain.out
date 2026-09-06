# -*- coding: utf-8 -*-
# 보류 재작업 빌더 (v1.5 문법 기준): rework 항목 → out/v15/{zip}.rework_final.json / out/v15/{zip}.rework_review.json
# 검산은 mathir_v15.py로 수행. 원래 review.json은 건드리지 않는다(v1.5 적용 뒤 반영용 별도 산출).
# r2(2026-09-05): ① 같은 id가 final↔review 사이를 옮겨가면 반대쪽 파일에서 제거  ② 항목 tags → pattern_tags 추가
#   ③ EXTRAS(한 이미지 두 문항의 둘째 문항, id 미발급) → out/v15/{zip}.rework_extra.json  ④ figure image의 src 파일 존재 검사(out/v15/figs/)
import sys, json, os, importlib.util, datetime, glob
spec = importlib.util.spec_from_file_location("mathir15", "/root/esc/mathir_v15.py")
mathir = importlib.util.module_from_spec(spec); spec.loader.exec_module(mathir)
OUT = "/root/esc/out/v15"

def gates(item, answer):
    errs = []
    _, _, e1 = mathir.parse_text(item["question"])
    if e1: errs.append(("①question", e1))
    for k, c in enumerate(item.get("choices") or []):
        _, _, e2 = mathir.parse_text(c)
        if e2: errs.append((f"②choice{k+1}", e2))
    if answer is not None:
        try: mathir.parse_answer(str(answer))
        except Exception as ex: errs.append(("③answer", str(ex)))
    if item.get("figure"):
        e4 = mathir.check_figure(item["figure"])
        if e4: errs.append(("④figure", e4))
        for fg in item["figure"]:
            if fg.get("fn") == "image":
                src = (fg.get("args") or {}).get("src", "")
                if not src or not os.path.exists(os.path.join(OUT, src)):
                    errs.append(("④figure", f"image src 파일 없음: {src} (out/v15/{src} 에 저장 필요)"))
    if item.get("qtype") == "choice" and len(item.get("choices") or []) != 5: errs.append(("②choices", "5개가 아님"))
    return errs

def _obj(it, base, answer, tags):
    return {"seq": base["seq"], "qtype": it["qtype"], "question": it["question"], "choices": it.get("choices"),
            "answer": answer, "difficulty_est": it.get("difficulty_est", base["difficulty_est"]), "has_math": True,
            "has_figure": bool(it.get("figure")), "figure": it.get("figure") or None,
            "unit_id": it.get("unit_id", base["unit_id"]), "concept_main": None, "concept_subs": [],
            "pattern_tags": ["v15재작업"] + [t for t in tags if t], "confidence": it.get("confidence", 0.85)}

def build(batch_mod):
    mod = importlib.import_module(batch_mod)
    src = {x["id"]: x for f in sorted(glob.glob("/root/esc/rework/batch*.json")) for x in json.load(open(f, encoding="utf-8"))}
    def resolve(i):
        if i in src: return i
        cands = [k for k in src if k.startswith(i)]
        assert len(cands) == 1, f"id 매칭 실패 {i}"
        return cands[0]
    by_zip = {}
    for it in mod.ITEMS:
        it["id"] = resolve(it["id"]); base = src[it["id"]]
        zn = base["zip"]
        answer = it.get("answer", it.get("derived_answer", base["answer"]))
        errs = gates(it, answer)
        obj = _obj(it, base, answer, it.get("tags") or [])
        rec = by_zip.setdefault(zn, {"final": [], "review": [], "extra": []})
        if errs or it.get("needs_review"):
            reason = ("검산 불통과: " + "; ".join(f"{g} {e}" for g, e in errs) + " / " if errs else "") + (it.get("needs_review") or "")
            rec["review"].append({"id": it["id"], "image": os.path.relpath(base["image"], f"/root/esc/work/{zn}"), "reason": reason + ((" — " + it["note"]) if it.get("note") else ""), "draft": obj})
        else:
            rec["final"].append({"id": it["id"], "final": obj, "rework_note": base["reason"][:160] + ((" → " + it["note"]) if it.get("note") else "")})
    for ex in getattr(mod, "EXTRAS", []):
        pid = resolve(ex["parent_id"]); base = src[pid]; zn = base["zip"]
        answer = ex.get("answer")
        errs = gates(ex, answer)
        obj = _obj(ex, base, answer, ["두문항_둘째", *(ex.get("tags") or [])])
        rec = by_zip.setdefault(zn, {"final": [], "review": [], "extra": []})
        rec["extra"].append({"parent_id": pid, "image": os.path.relpath(base["image"], f"/root/esc/work/{zn}"), "position": ex.get("position", ""),
                             "status": "review" if (errs or ex.get("needs_review")) else "ok",
                             "reason": ("검산 불통과: " + "; ".join(f"{g} {e}" for g, e in errs) + " / " if errs else "") + (ex.get("needs_review") or ""),
                             "draft": obj, "note": ex.get("note", "")})
    os.makedirs(OUT, exist_ok=True)
    for zn, rec in by_zip.items():
        touched = {x["id"] for x in rec["final"]} | {x["id"] for x in rec["review"]}
        for kind in ("final", "review"):
            p = f"{OUT}/{zn}.rework_{kind}.json"
            old = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
            merged = [x for x in old if x["id"] not in touched] + rec[kind]      # r2①: 양쪽 파일에서 제거 후 추가
            json.dump(merged, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if rec["extra"]:
            p = f"{OUT}/{zn}.rework_extra.json"
            old = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
            pids = {x["parent_id"] for x in rec["extra"]}
            merged = [x for x in old if x["parent_id"] not in pids] + rec["extra"]
            json.dump(merged, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return by_zip

if __name__ == "__main__":
    batch_mod = sys.argv[1]
    by_zip = build(batch_mod)
    nf = sum(len(r["final"]) for r in by_zip.values()); nr = sum(len(r["review"]) for r in by_zip.values())
    ne = sum(len(r["extra"]) for r in by_zip.values()); neb = sum(1 for r in by_zip.values() for x in r["extra"] if x["status"] != "ok")
    print(f"{batch_mod}: 재작업 {nf + nr} | 통과 {nf} | 잔여 보류 {nr}" + (f" | 둘째 문항(extra) {ne} (검산 불통과 {neb})" if ne else ""))
    for zn, r in by_zip.items():
        for x in r["review"]: print("  R", zn, x["id"][:8], "|", x["reason"][:120])
        for x in r["extra"]:
            if x["status"] != "ok": print("  E", zn, x["parent_id"][:8], "|", x["reason"][:120])
