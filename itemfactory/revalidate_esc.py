# ashrain.out — 상위 대기 공짜 회수기 (revalidate_esc.py, v1.1)
# 위치: itemfactory/revalidate_esc.py
#
# 대기(escalated) 문항의 저장된 초안을 "새 문법(mathir v1.3: 또는·마커·행렬·sub확장)"으로
# 재검증해서, 통과분을 API 호출 없이 active로 승격한다. 답이 비어 있으면
# 자료의 빠른정답(corpus_docs.answers)에서 대입 검산 후 백필까지.
#
# v1.1 수술 3종:
#   ① check_figure 계약 일치 — 오류 "목록" 반환 함수임. v1.0은 (ok,_) 튜플 언패킹이라
#      정상 도형(빈 목록)에서 즉사했음. 이제 목록이 비어있지 않으면 불통과.
#   ② 승격-잠식 방지 — offset 페이지는 승격할수록 집합이 줄어 뒷줄을 건너뜀.
#      id 키셋 페이지로 교체(마지막 id 다음부터), 건너뜀 구조적 불가.
#   ③ verify 광역 예외 가드 — 초안 쓰레기 데이터 한 건이 전체 실행을 못 죽이게.
#
# 사용:  python revalidate_esc.py           # 전량
#        python revalidate_esc.py m3-1      # 단원 한정
# 준비:  git pull (mathir.py v1.3 필수) — API 키 불필요, 지출 0원

import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mathir
from transcribe_local import load_env, get_client


def verify(a):
    if not a or not str(a.get("question") or "").strip():
        return False
    try:
        _, _, errs = mathir.parse_text(str(a.get("question") or ""))
        if errs: return False
        for ch in (a.get("choices") or []):
            _, _, e2 = mathir.parse_text(str(ch))
            if e2: return False
        if a.get("answer"):
            mathir.parse_answer(str(a["answer"]))
        if a.get("figure"):
            if mathir.check_figure(a["figure"]):  # 오류 목록이 차 있으면 불통과
                return False
        return True
    except mathir.MathIRError:
        return False
    except Exception:
        return False


def main():
    unit = sys.argv[1] if len(sys.argv) > 1 else None
    load_env(); sb = get_client()
    amap_cache = {}
    revived = filled = seen = 0
    last_id = None
    while True:
        q = sb.table("corpus_items").select("id,doc_id,seq,answer,drafts,question,unit_id") \
            .eq("status", "escalated").order("id").limit(500)
        if unit: q = q.eq("unit_id", unit)
        if last_id: q = q.gt("id", last_id)
        rows = q.execute().data or []
        if not rows: break
        for r in rows:
            seen += 1
            a = (r.get("drafts") or {}).get("a")
            if not verify(a):
                continue
            patch = {"status": "active"}
            ans = r.get("answer") or a.get("answer")
            if not ans and r.get("doc_id"):
                if r["doc_id"] not in amap_cache:
                    d = sb.table("corpus_docs").select("answers").eq("id", r["doc_id"]).single().execute().data
                    amap_cache[r["doc_id"]] = (d or {}).get("answers") or {}
                cand = amap_cache[r["doc_id"]].get(str(r.get("seq")))
                if cand:
                    try:
                        mathir.parse_answer(str(cand))
                        chk = mathir.check_equation_answer(str(r.get("question") or a.get("question") or ""), str(cand))
                        if chk is not False:
                            ans = cand; filled += 1
                    except mathir.MathIRError:
                        pass
            if ans: patch["answer"] = str(ans)
            sb.table("corpus_items").update(patch).eq("id", r["id"]).execute()
            revived += 1
            if revived % 100 == 0:
                print(f"  …회수 {revived} (검토 {seen})")
        last_id = rows[-1]["id"]
        if len(rows) < 500: break
    print(f"\n완료 — 검토 {seen} · 회수 {revived} · 답 백필 {filled}  (지출 0원)")
    print("회수분은 미분류 상태 — 분류 보완 스크립트에서 일괄 처리 예정")


if __name__ == "__main__":
    main()
