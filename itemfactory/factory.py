# ashrain.out — 문항 공장 엔진 (factory.py, v1.0)
# 위치: itemfactory/factory.py
#
# 역할(로컬 전용): 틀(템플릿) 열거 → 3중 검증(검산·제약·중복) → 서빙 풀 추출 → test_items 업서트.
# 라벨은 출생 정보만 부착(cid·난이도·gen_meta). 분석·재분류는 앱/배치 쪽 별도 층 담당.
#
# 사용법:
#   python factory.py m1-1-01                  # 드라이런 — out/ 에 JSON만 생성 (DB 안 건드림)
#   python factory.py m1-1-01 --push           # DB 업서트 (.env 필요)
#   python factory.py m1-1-01 --pool 400       # 서빙 풀 크기 (기본 400)
#   python factory.py m1-1-01 --status live    # 적재 상태 (기본 draft)
#   python factory.py m1-1-01 --site 학원      # 생성 사이트 태그 (기본 호스트명)
#
# .env (itemfactory/.env — 절대 커밋 금지):
#   SUPABASE_URL=https://xxxx.supabase.co
#   SUPABASE_SERVICE_KEY=eyJ...

import argparse, hashlib, importlib.util, json, os, re, socket, sys, time
from pathlib import Path

BUILDER_VERSION = "factory-1.0"
HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- env / db
def load_env():
    for p in (HERE / ".env", Path.cwd() / ".env"):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_client():
    try:
        from supabase import create_client
    except ImportError:
        sys.exit("supabase 패키지 필요: pip install supabase --break-system-packages")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("SUPABASE_URL / SUPABASE_SERVICE_KEY 필요 (itemfactory/.env)")
    return create_client(url, key)


def fetch_existing(sb, test_type):
    """같은 test_type의 기존 문항 전량 (페이지네이션)."""
    rows, i = [], 0
    while True:
        r = (sb.table("test_items")
               .select("id,question,choices,source,gen_meta")
               .eq("test_type", test_type)
               .range(i, i + 999).execute())
        batch = r.data or []
        rows += batch
        if len(batch) < 1000:
            break
        i += 1000
    return rows


# ---------------------------------------------------------------- keys
def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def local_content_key(question, choices):
    """로컬 동일성 키 — 문제문 + 보기. (DB의 content_key와 별개 계산이지만 같은 정신)"""
    base = question + " " + (json.dumps(choices, ensure_ascii=False) if choices else "")
    return hashlib.md5(_norm(base).encode("utf-8")).hexdigest()


def struct_key(question, choices):
    """구조 키 — 수치를 #로 마스킹. 수치만 다른 유사 문항 탐지용."""
    base = question + " " + (json.dumps(choices, ensure_ascii=False) if choices else "")
    base = re.sub(r"\d+(?:\.\d+)?", "#", base)
    return hashlib.md5(_norm(base).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- checks
def generic_checks(item, qtype):
    q = item.get("question", "")
    assert isinstance(q, str) and 5 <= len(q) <= 600, "question 길이 이상"
    assert isinstance(item.get("answer"), str) and item["answer"].strip(), "answer 비어 있음"
    sol = item.get("solution")
    assert isinstance(sol, dict) and sol.get("outline") and sol.get("steps") and sol.get("check"), "solution 규격 위반"
    assert 1 <= len(sol["steps"]) <= 8, "solution.steps 수 이상"
    if qtype == "choice":
        ch = item.get("choices")
        assert isinstance(ch, list) and len(ch) == 5, "choice는 보기 5개"
        assert len(set(ch)) == 5, "보기 중복"
        assert item["answer"] in ch, "정답이 보기에 없음"
    else:
        assert item.get("choices") in (None, []), "short에 choices 존재"


# ---------------------------------------------------------------- sampling
def even_spread(space, k):
    return [(i * space) // k for i in range(k)]


def candidate_stream(space, k):
    """균등 표집 인덱스 먼저, 부족분(탈락 대체)은 나머지 인덱스를 오름차순으로."""
    first = even_spread(space, min(k, space))
    seen = set(first)
    yield from first
    for i in range(space):
        if i not in seen:
            yield i


def allocate(templates, pool):
    pts = [max(1, t.get("pool_target", 1)) for t in templates]
    total = sum(pts)
    tgt = [min(t["space"], round(pool * p / total)) for t, p in zip(templates, pts)]
    # 부족분 재배분 (여유 있는 틀에)
    j = 0
    while sum(tgt) < pool and any(templates[i]["space"] > tgt[i] for i in range(len(tgt))):
        if templates[j]["space"] > tgt[j]:
            tgt[j] += 1
        j = (j + 1) % len(tgt)
    # 초과분 축소 (큰 것부터)
    while sum(tgt) > pool:
        j = max(range(len(tgt)), key=lambda i: tgt[i])
        tgt[j] -= 1
    return tgt


# ---------------------------------------------------------------- main build
def load_template_module(cid):
    path = HERE / "templates" / (cid.replace("-", "_") + ".py")
    if not path.exists():
        sys.exit(f"틀 파일 없음: {path} — 채팅에서 '{cid} 틀 줘'로 요청")
    spec = importlib.util.spec_from_file_location(f"tpl_{cid}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(cid, pool, test_type, status, site, push):
    load_env()
    mod = load_template_module(cid)
    templates = mod.TEMPLATES
    unit_id = cid.rsplit("-", 1)[0]
    run_id = f"{cid}-{time.strftime('%Y%m%d-%H%M%S')}"

    # 기존 문항 (중복 대조용)
    existing = []
    sb = None
    if push or (os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY")):
        try:
            sb = get_client()
            existing = fetch_existing(sb, test_type)
        except SystemExit:
            raise
        except Exception as e:
            if push:
                sys.exit(f"DB 접속 실패: {e}")
            print(f"· DB 대조 생략 (접속 불가: {e})")
    else:
        print("· .env 없음 — DB 대조 생략 (드라이런)")

    ex_content, ex_struct = {}, {}
    for row in existing:
        ck = local_content_key(row["question"], row.get("choices"))
        sk = struct_key(row["question"], row.get("choices"))
        ex_content.setdefault(ck, row)
        ex_struct.setdefault(sk, []).append(row)

    targets = allocate(templates, pool)
    accepted, review, rejects = [], [], []
    seen_content = set()
    stat = {t["id"]: {"target": tg, "ok": 0, "rej": 0, "rev": 0} for t, tg in zip(templates, targets)}

    for t, tgt in zip(templates, targets):
        got = 0
        for idx in candidate_stream(t["space"], max(tgt * 3, tgt + 20)):
            if got >= tgt:
                break
            try:
                params = t["params_at"](idx)
                item = t["render"](params)
                t["verify"](item, params)
                generic_checks(item, t["qtype"])
            except AssertionError as e:
                rejects.append(_reject(run_id, cid, t, idx, None, None, f"verify_fail: {e}", None, site))
                stat[t["id"]]["rej"] += 1
                continue

            ck = local_content_key(item["question"], item.get("choices"))
            sk = struct_key(item["question"], item.get("choices"))

            if ck in seen_content:  # 세션 내 완전 중복 (이론상 없어야 정상)
                rejects.append(_reject(run_id, cid, t, idx, ck, sk, "dup_exact_session", None, site))
                stat[t["id"]]["rej"] += 1
                continue
            if ck in ex_content:    # DB 완전 중복 → 자동 폐기 + 사유 기록 (E-10)
                rejects.append(_reject(run_id, cid, t, idx, ck, sk, "dup_exact", ex_content[ck]["id"], site))
                stat[t["id"]]["rej"] += 1
                continue

            # 구조 유사 — 같은 틀 밖(다른 출처·다른 틀)과 겹칠 때만 검토 대상
            outside = [r for r in ex_struct.get(sk, [])
                       if not (r.get("source") == "template"
                               and (r.get("gen_meta") or {}).get("tpl") == t["id"])]
            payload = _payload(item, t, cid, unit_id, test_type, status, site, idx, sk)
            if outside:
                review.append({"payload": payload, "similar_to": outside[0]["id"],
                               "similar_question": outside[0]["question"][:120]})
                stat[t["id"]]["rev"] += 1
                continue

            seen_content.add(ck)
            accepted.append(payload)
            stat[t["id"]]["ok"] += 1
            got += 1

    # ---------------- 산출
    outdir = HERE / "out"
    outdir.mkdir(exist_ok=True)
    (outdir / f"{cid}_pool.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=1), encoding="utf-8")
    if review:
        (outdir / f"{cid}_review.json").write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
    report = {"run_id": run_id, "cid": cid, "pool": pool, "per_template": stat,
              "accepted": len(accepted), "review": len(review), "rejected": len(rejects)}
    (outdir / f"{cid}_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n== {cid} {getattr(mod, 'TITLE', '')} · run {run_id} ==")
    for tid, s in stat.items():
        print(f"  {tid:<14} 목표 {s['target']:>4} · 적재 {s['ok']:>4} · 검토 {s['rev']:>3} · 폐기 {s['rej']:>3}")
    print(f"  합계: 적재 {len(accepted)} / 검토 {len(review)} / 폐기 {len(rejects)}")

    # ---------------- push
    if push:
        n0 = _count_concept(sb, test_type, cid)
        for i in range(0, len(accepted), 200):
            sb.table("test_items").upsert(
                accepted[i:i + 200], on_conflict="test_type,content_key",
                ignore_duplicates=True).execute()
        if rejects:
            for i in range(0, len(rejects), 200):
                sb.table("item_rejects").insert(rejects[i:i + 200]).execute()
        _register_templates(sb, templates, targets, cid, test_type)
        n1 = _count_concept(sb, test_type, cid)
        print(f"  DB 반영: {cid} 문항 {n0} → {n1} (+{n1 - n0}) · 폐기 기록 {len(rejects)}건 · 틀 {len(templates)}개 등록")
        if review:
            print(f"  ⚠ 검토 대기 {len(review)}건 → out/{cid}_review.json (푸시 안 함)")
    else:
        print(f"  (드라이런 — out/{cid}_pool.json 확인 후 --push)")


def _payload(item, t, cid, unit_id, test_type, status, site, idx, sk):
    return {
        "test_type": test_type, "unit_id": unit_id, "concept_ids": [cid],
        "qtype": t["qtype"], "difficulty": t["difficulty"],
        "question": item["question"], "choices": item.get("choices"),
        "answer": item["answer"], "answer_alt": item.get("answer_alt", []),
        "time_limit": t.get("time_limit"), "tags": t.get("tags", []),
        "solution": item["solution"], "source": "template", "status": status,
        "struct_key": sk,
        "gen_meta": {"tpl": t["id"], "idx": idx, "bv": BUILDER_VERSION,
                     "model": "fable-chat", "site": site,
                     "ans_type": item.get("ans_type"), "verified": True},
    }


def _reject(run_id, cid, t, idx, ck, sk, reason, similar_to, site):
    return {"run_id": run_id, "concept_id": cid, "template_id": t["id"],
            "param_index": idx, "content_key": ck, "struct_key": sk,
            "reason": reason, "similar_to": similar_to, "question": None, "site": site}


def _register_templates(sb, templates, targets, cid, test_type):
    rows = []
    for t, tg in zip(templates, targets):
        rows.append({"template_id": t["id"], "concept_id": cid, "test_type": test_type,
                     "qtype": t["qtype"], "difficulty": t["difficulty"],
                     "title": t.get("title", ""), "spec": t.get("spec", {}),
                     "param_space": t["space"], "pool_target": tg,
                     "builder_version": BUILDER_VERSION, "status": "active"})
    sb.table("item_templates").upsert(rows, on_conflict="template_id").execute()


def _count_concept(sb, test_type, cid):
    r = (sb.table("test_items").select("id", count="exact")
           .eq("test_type", test_type).contains("concept_ids", [cid]).execute())
    return r.count or 0


# ---------------------------------------------------------------- cli
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cid")
    ap.add_argument("--pool", type=int, default=400)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--test-type", default="concept_set")
    ap.add_argument("--status", default="draft", choices=["draft", "live"])
    ap.add_argument("--site", default=socket.gethostname())
    a = ap.parse_args()
    build(a.cid, a.pool, a.test_type, a.status, a.site, a.push)
