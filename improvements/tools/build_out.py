# -*- coding: utf-8 -*-
# 산출물 빌더: ITEMS(전사 초안) + 판정 규칙 → out/{zip}.final.json / out/{zip}.review.json
# 규칙(파일럿 결정 2026-09-03):
#  - 4관문 불통과 → review
#  - (2026-09-03 22:05 규칙1 해제) quick_answer 불일치는 review 사유가 아님 → 4관문·needs_review만 통과하면
#    {zip}.final_qamismatch.json 으로 따로 분류(형식은 final과 동일, 반영 가능). 불일치 사실은 note로만 기록
#  - 장식 그림은 fn "unsupported"로 final, 복합 기하 도형(needs_review 플래그) → review
#  - 문법 한계(needs_review 플래그) → review
#  - (2026-09-04 규칙2 완화) needs_review 사유가 "도형 표현 불가"만인 항목은 review 대신 {zip}.final_figrelax.json 으로 따로 분류
#    (unsupported+raw 설명을 final로 인정, 형식은 final과 동일, pattern_tags에 "도형완화")
import sys, json, os, importlib, datetime
sys.path.insert(0, "/root/esc")
import mathir

def gates(item, answer):
    errs = []
    _, _, e1 = mathir.parse_text(item["question"])
    if e1: errs.append(("①question", e1))
    for k, c in enumerate(item.get("choices") or []):
        _, _, e2 = mathir.parse_text(c)
        if e2: errs.append((f"②choice{k+1}", e2))
    if answer is not None:
        try: mathir.parse_answer(answer)
        except Exception as ex: errs.append(("③answer", str(ex)))
    if item.get("figure"):
        e4 = mathir.check_figure(item["figure"])
        if e4: errs.append(("④figure", e4))
    qa = item.get("quick_answer")
    if qa is not None and mathir.check_equation_answer(item["question"], str(qa)) is False:
        errs.append(("⑤quick_answer 대입", False))
    return errs

FIG_ONLY_MARK = ("도형 표현 불가", "도형표현불가", "도형 표현불가")
NON_FIG_MARK = ("문법", "조각", "프라임", "첨자", "적용 표기", "잘림", "흐림", "그리스", "텍스트 혼합", "prime", "합성", "역함수", "미도출", "판독", "대응", "복수", "별개 문항", "id 1개", "id는 1개", "검산")

def fig_only(reason):
    """needs_review 문자열이 도형 표현 불가 사유만으로 이루어졌는지"""
    if not reason: return False
    parts = [p.strip() for p in reason.replace("；", "/").split("/") if p.strip()]
    if not parts: return False
    for p in parts:
        if not any(m in p for m in FIG_ONLY_MARK): return False
        if any(m in p for m in NON_FIG_MARK): return False
    return True

def norm_ans(s):
    """비교용 정규화: 선지 기호 ↔ 숫자, 공백 제거"""
    if s is None: return None
    s = str(s).strip()
    circ = "①②③④⑤⑥⑦⑧⑨⑩"
    if s in circ: return str(circ.index(s) + 1)
    return s.replace(" ", "")

def build(zipname, ITEMS, manifest):
    full_ids = {it["id"][:8]: it["id"] for it in manifest["items"]}
    by_id = {it["id"]: it for it in manifest["items"]}
    final, review, final_qa, final_fig = [], [], [], []
    for it in ITEMS:
        it["id"] = full_ids.get(it["id"][:8], it["id"])
        m = by_id[it["id"]]
        it["quick_answer"] = m.get("quick_answer")  # manifest가 단일 원천
        answer = it.get("answer", it.get("derived_answer"))
        errs = gates(it, answer)
        reasons = []
        if errs: reasons.append("검산 불통과: " + "; ".join(f"{g} {e}" for g, e in errs))
        qa = it["quick_answer"]
        qa_mismatch = qa is not None and answer is not None and norm_ans(qa) != norm_ans(answer)
        fig_relaxed = False
        if it.get("needs_review"):
            if fig_only(it["needs_review"]) and not errs:
                fig_relaxed = True
            else:
                reasons.append(it["needs_review"])
        obj = {
            "seq": m["seq"], "qtype": it["qtype"], "question": it["question"],
            "choices": it.get("choices"), "answer": answer,
            "difficulty_est": it.get("difficulty_est"), "has_math": True,
            "has_figure": bool(it.get("figure")), "figure": it.get("figure") or None,
            "unit_id": it.get("unit_id", m["unit_id"]), "concept_main": None,
            "concept_subs": [], "pattern_tags": [], "confidence": it.get("confidence", 0.9),
        }
        if qa_mismatch:
            obj["pattern_tags"] = ["빠른정답불일치"]
        if fig_relaxed:
            obj["pattern_tags"] = obj["pattern_tags"] + ["도형완화"]
        if reasons:
            if qa_mismatch: reasons.append(f"(참고) 빠른정답 불일치: 전사·풀이 답 {answer} vs 빠른정답 {qa}")
            review.append({"id": it["id"], "image": m["image"],
                           "reason": " / ".join(reasons) + ((" — " + it["note"]) if it.get("note") else ""),
                           "draft": obj})
        elif fig_relaxed:
            final_fig.append({"id": it["id"], "final": obj,
                              "fig_note": it["needs_review"] + ((" — " + it["note"]) if it.get("note") else "")
                              + ((f" / 빠른정답 불일치: {answer} vs {qa}") if qa_mismatch else "")})
        elif qa_mismatch:
            final_qa.append({"id": it["id"], "final": obj,
                             "qa_note": f"전사·풀이 답 {answer} vs 빠른정답 {qa}" + ((" — " + it["note"]) if it.get("note") else "")})
        else:
            final.append({"id": it["id"], "final": obj})
    os.makedirs("/root/esc/out", exist_ok=True)
    with open(f"/root/esc/out/{zipname}.final.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=1)
    with open(f"/root/esc/out/{zipname}.review.json", "w", encoding="utf-8") as f:
        json.dump(review, f, ensure_ascii=False, indent=1)
    with open(f"/root/esc/out/{zipname}.final_qamismatch.json", "w", encoding="utf-8") as f:
        json.dump(final_qa, f, ensure_ascii=False, indent=1)
    with open(f"/root/esc/out/{zipname}.final_figrelax.json", "w", encoding="utf-8") as f:
        json.dump(final_fig, f, ensure_ascii=False, indent=1)
    return final, review, final_qa, final_fig

if __name__ == "__main__":
    zipname, modname = sys.argv[1], sys.argv[2]
    mod = importlib.import_module(modname)
    manifest = json.load(open(f"/root/esc/work/{zipname}/manifest.json", encoding="utf-8"))
    final, review, final_qa, final_fig = build(zipname, mod.ITEMS, manifest)
    n = len(manifest["items"])
    ids_done = {x["id"] for x in final} | {x["id"] for x in review} | {x["id"] for x in final_qa} | {x["id"] for x in final_fig}
    missing = [it["id"] for it in manifest["items"] if it["id"] not in ids_done]
    print(f"{zipname}: manifest {n} | final {len(final)} | final_qamismatch {len(final_qa)} | final_figrelax {len(final_fig)} | review {len(review)} | missing {len(missing)} {missing}")
    for r in review: print("  R", r["id"][:8], r["draft"]["seq"], "|", r["reason"][:110])
    for x in final: print("  F", x["id"][:8], x["final"]["seq"], x["final"]["qtype"], "ans=", x["final"]["answer"])
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
    print(f"| {zipname} | 문항 {n} | 통과 {len(final) + len(final_qa) + len(final_fig)} (빠른정답불일치 {len(final_qa)}, 도형완화 {len(final_fig)}) | 보류 {len(review)} | {now} |")
