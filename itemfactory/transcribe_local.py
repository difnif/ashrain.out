# ashrain.out — 로컬 전사 워커 (transcribe_local.py, v1.0)
# 위치: itemfactory/transcribe_local.py
#
# 역할: runner='local'인 전사 작업을 집 PC GPU(Ollama)로 처리 — API 비용 0.
#   큐 클레임(claim_job_page 공유) → Ollama 비전 전사 → mathir 기계 심판(V-01~05·09)
#   → 실패 문항 오류 피드백 재시도 1회 → 잔여는 상위 대기(수동 큐 zip 루프와 호환)
#   답지 페이지 → corpus_docs.answers 병합 / 해설 페이지 → corpus_solutions 적재(공공자료 문체 표본)
#
# 워치독:
#   · VRAM 경고 — 사용률이 임계(기본 90%) 초과 시 윈도우 경고창
#   · 롤 감지 — LeagueClient 실행 시 자동 일시정지 + 알림창, 종료 시 자동 재개 + 알림
#   · 가동 시간대 — --hours 23-08 형식이면 그 시간대에만 가동
#
# 사용:
#   python transcribe_local.py                     # 상시 가동 (워치독 켜짐)
#   python transcribe_local.py --hours 23-08      # 밤에만
#   python transcribe_local.py --model qwen2.5vl:7b --parallel 2
#   python transcribe_local.py --once             # 한 페이지만 처리하고 종료 (동작 확인용)
#
# 준비물: Ollama 설치 + `ollama pull qwen2.5vl:7b` + itemfactory/.env (기존 그대로)

import argparse, base64, ctypes, json, re, subprocess, sys, threading, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mathir  # noqa: E402  (같은 폴더의 mathir.py)

try:
    import requests
except ImportError:
    sys.exit("requests 패키지 필요: pip install requests")

OLLAMA = "http://localhost:11434/api/chat"

SYS_T = """너는 수학 문제지 전사기다. 이미지 속 내용을 JSON으로만 출력한다. JSON 밖 텍스트 금지.

■ 페이지 종류에 따라 출력이 다르다
1) 문항이 실린 문제지 페이지 → 문항 배열:
[{"seq":문항번호,"qtype":"choice|short|proof|essay","question":"...","choices":[...]|null,
"answer":"...(지면에 없으면 null)","difficulty_est":1~5,"has_figure":true|false,"figure":[도형함수]|null}]
2) 답만 표·나열로 모인 답지 페이지 → {"answer_sheet":{"1":"x = 3","2":"frac(1,2)"}}
3) 풀이 과정 서술 중심의 해설 페이지 → {"solution_sheet":[{"seq":1,"text":"해설 전문"}]}

■ 수식 표기 — MathIR 닫힌 문법 (목록 밖 토큰 금지)
- 문장 속 수식은 [[ ... ]]로 감싸고 그 안은 MathIR만. 단순 숫자·단위(3 cm)는 평문. 유니코드 수식문자·LaTeX 금지.
- 기본: 숫자, 변수, + - * / = != < > <= >=, 괄호, 병치곱(2x, 3(x+1)).
- 함수: frac mixed pow sqrt root abs recdec floor fact max min ratio pct deg dms pm
  seg line ray arc angle tri quad par perp cong sim point point3 vec vcomp dot
  set setb in notin subset nsubset union inter comp card imp iff neg itv conj
  log ln sin cos tan csc sec cot sub sum lim prime dydx integ dinteg inv
  perm comb pperm hcomb prob cprob ev var sd binomd normald | 상수 pi e i inf empty
- answer는 마커 없이 IR 하나("x = 8") 또는 한국어 낱말("소수"). 해설 text 속 수식도 [[ ]] 규칙.

■ figure — 함수 호출 배열만: numline coordplane table hist stemleaf crossing parallel tri rect polygon
circle sector solid net boxplot scatter venn tree funcgraph unitcircle conic vecfig space normcurve
표현 불가 시 {"fn":"unsupported","args":{"raw":"짧은 서술"}}
원문 그대로(오탈자 포함), 머리말·페이지번호 무시. JSON 문자열 안 백슬래시는 \\\\ 이스케이프."""


# ---------------------------------------------------------------- env·db (factory.py와 동일 관례)
def load_env():
    for p in (HERE / ".env", Path.cwd() / ".env"):
        if p.exists():
            import os
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_client():
    import os
    from supabase import create_client
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("SUPABASE_URL / SUPABASE_SERVICE_KEY 필요 (itemfactory/.env)")
    return create_client(url, key)


# ---------------------------------------------------------------- 워치독
def alert(msg, title="ashrain 로컬 워커"):
    print(f"⚠ {msg}")
    if sys.platform == "win32":
        threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, msg, title, 0x1040),
                         daemon=True).start()


def vram_pct():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                              "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=5)
        used, total = out.stdout.strip().split("\n")[0].split(",")
        return 100.0 * float(used) / float(total)
    except Exception:
        return None


def lol_running():
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq LeagueClient.exe"],
                             capture_output=True, text=True, timeout=5)
        return "LeagueClient" in out.stdout
    except Exception:
        return False


class Watchdog:
    def __init__(self, vram_limit):
        self.vram_limit = vram_limit
        self.paused_by_lol = False
        self._warned_vram = 0

    def gate(self):
        """가동 가능하면 True. 롤 감지 시 종료까지 대기."""
        if sys.platform == "win32" and lol_running():
            if not self.paused_by_lol:
                self.paused_by_lol = True
                alert("리그 오브 레전드 감지 — 로컬 전사를 일시정지합니다.\n게임 종료 시 자동 재개돼요.")
            while lol_running():
                time.sleep(10)
            self.paused_by_lol = False
            alert("게임 종료 감지 — 로컬 전사를 재개합니다.")
        p = vram_pct()
        if p is not None and p >= self.vram_limit and time.time() - self._warned_vram > 300:
            self._warned_vram = time.time()
            alert(f"VRAM 사용률 {p:.0f}% — 임계({self.vram_limit}%) 초과.\n다른 GPU 프로그램을 확인하세요.")
        return True


def in_hours(spec):
    if not spec:
        return True
    a, b = (int(x) for x in spec.split("-"))
    h = datetime.now().hour
    return (a <= h or h < b) if a > b else (a <= h < b)


# ---------------------------------------------------------------- Ollama
def ollama_chat(model, prompt, image_b64=None, max_retry=2):
    msg = {"role": "user", "content": prompt}
    if image_b64:
        msg["images"] = [image_b64]
    for k in range(max_retry):
        try:
            r = requests.post(OLLAMA, json={
                "model": model, "stream": False, "keep_alive": "30m",
                "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 3000},
                "messages": [{"role": "system", "content": SYS_T}, msg],
            }, timeout=600)
            r.raise_for_status()
            return r.json()["message"]["content"]
        except requests.ConnectionError:
            sys.exit("Ollama 미실행 — 먼저 Ollama를 켜주세요 (설치: ollama.com)")
        except Exception as e:
            if k == max_retry - 1:
                raise
            print(f"  · ollama 재시도 ({e})")
            time.sleep(3)


def _json_any(text):
    m = re.search(r"\{[\s\S]*\}|\[[\s\S]*\]", text)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


# ---------------------------------------------------------------- 문항 심판 (러너 v2와 동일 규칙)
def verify_item(it, grade_hint):
    errs = []
    segs, _, e1 = mathir.parse_text(str(it.get("question") or ""), grade_hint)
    errs += [{**e, "at": "question"} for e in e1]
    for i, c in enumerate(it.get("choices") or []):
        _, _, e2 = mathir.parse_text(str(c))
        errs += [{**e, "at": f"choice{i+1}"} for e in e2]
    ans = it.get("answer")
    if ans is not None and str(ans).strip():
        try:
            mathir.parse_answer(str(ans))
        except mathir.MathIRError as e:
            errs.append({"code": e.code, "at": "answer", "msg": str(e)})
    errs += [{**e, "at": "figure"} for e in mathir.check_figure(it.get("figure") or [])]
    if not errs and ans is not None and str(ans).strip():
        if mathir.check_equation_answer(str(it.get("question") or ""), str(ans)) is False:
            errs.append({"code": "V-03", "at": "answer", "msg": "답 대입 불일치"})
    return errs


# ---------------------------------------------------------------- 페이지 처리
def process_page(sb, job, pg, model):
    img = sb.storage.from_("corpus").download(pg["storage_path"])
    b64 = base64.b64encode(img).decode()
    out = _json_any(ollama_chat(model, "이 페이지를 전사해라.", b64))
    if out is None:
        raise RuntimeError("JSON 파싱 실패")

    # ── 답지 페이지
    if isinstance(out, dict) and "answer_sheet" in out:
        clean = {}
        for k, v in (out["answer_sheet"] or {}).items():
            try:
                mathir.parse_answer(str(v))
                clean[str(k)] = str(v)
            except mathir.MathIRError:
                pass
        if clean:
            cur = sb.table("corpus_docs").select("answers").eq("id", job["doc_id"]).single().execute().data
            merged = {**(cur.get("answers") or {}), **clean}
            sb.table("corpus_docs").update({"answers": merged}).eq("id", job["doc_id"]).execute()
        _log(sb, job, pg, 0, "answer_sheet", model, True, [])
        return 0, 0

    # ── 해설 페이지 → corpus_solutions
    if isinstance(out, dict) and "solution_sheet" in out:
        rows = []
        for s in out["solution_sheet"] or []:
            txt = str(s.get("text") or "").strip()
            if len(txt) < 5:
                continue
            _, _, errs = mathir.parse_text(txt)
            rows.append({"doc_id": job["doc_id"], "page": pg["page"], "seq": s.get("seq"),
                         "text": txt, "ir_errs": len(errs), "model": model})
        if rows:
            sb.table("corpus_solutions").insert(rows).execute()
        _log(sb, job, pg, 0, "solution_sheet", model, True, [])
        return len(rows), 0

    if not isinstance(out, list):
        raise RuntimeError("규격 외 출력")

    # ── 문제지 페이지
    mu = re.match(r"^[mh]\d-\d", job.get("unit_hint") or "")
    unit = mu.group(0) if mu else None
    items, esc = [], 0
    for raw in out:
        it = raw
        errs = verify_item(it, job.get("unit_hint"))
        if errs:                                       # 오류 피드백 재시도 1회
            fb = "\n".join(f"{e['code']}@{e['at']}{(' [['+e['src']+']]') if e.get('src') else ''}: {e.get('msg','')}"
                           for e in errs[:6])
            t = ollama_chat(model,
                f"문항 {it.get('seq')}번만 다시 전사해 '단일 객체'로 출력해라. 이전 시도의 문법 오류:\n{fb}\n이전 시도: {json.dumps(it, ensure_ascii=False)}", b64)
            fixed = _json_any(t)
            if isinstance(fixed, dict):
                e2 = verify_item(fixed, job.get("unit_hint"))
                if len(e2) < len(errs):
                    it, errs = fixed, e2
        escal = bool(errs)
        if escal:
            esc += 1
        has_math = "[[" in str(it.get("question") or "") or any("[[" in str(c) for c in (it.get("choices") or []))
        items.append({
            "doc_id": job["doc_id"], "page": pg["page"], "seq": it.get("seq"),
            "unit_id": unit,
            "qtype": it.get("qtype") or "short", "question": str(it.get("question") or ""),
            "choices": it.get("choices") or None, "answer": it.get("answer"),
            "difficulty_est": it.get("difficulty_est"),
            "has_math": has_math, "has_figure": bool(it.get("figure")),
            "figure": it.get("figure") or None, "cluster_key": None,
            "model_final": "local" if not escal else "queue",
            "agree": not escal, "status": "escalated" if escal else "active",
            "drafts": {"a": it, "b": None, "diff": [e["code"] for e in errs]} if escal else None,
            "concept_main": None, "concept_subs": [], "concept_ids": [],
            "pattern_tags": [], "confidence": 0 if escal else None,
        })
        _log(sb, job, pg, it.get("seq"), "local", model, not escal, [e["code"] for e in errs])

    saved = [x for x in items if len(re.sub(r"\s+", " ", x["question"]).strip()) >= 5]
    if any(x["status"] == "escalated" for x in saved):
        try:
            data = sb.storage.from_("corpus").download(pg["storage_path"])
            sb.storage.from_("corpus").upload(f"esc/{job['doc_id']}/p{pg['page']}.jpg", data,
                                              {"content-type": "image/jpeg"})
        except Exception:
            pass
    if saved:
        sb.table("corpus_items").upsert(saved, on_conflict="content_key", ignore_duplicates=True).execute()
    return len(saved), esc


def _log(sb, job, pg, seq, role, model, agree, diff):
    try:
        sb.table("transcribe_runs").insert({"doc_id": job["doc_id"], "page": pg["page"], "seq": seq or 0,
                                            "cluster_key": None, "role": role, "model": model,
                                            "agree": agree, "diff_fields": diff, "adopted": agree}).execute()
    except Exception:
        pass


# ---------------------------------------------------------------- 메인 루프
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen2.5vl:7b")
    ap.add_argument("--hours", default=None, help="가동 시간대, 예: 23-08")
    ap.add_argument("--vram-limit", type=float, default=90.0)
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args()

    load_env()
    sb = get_client()
    wd = Watchdog(a.vram_limit)
    print(f"로컬 워커 가동 — 모델 {a.model}"
          + (f" · 시간대 {a.hours}" if a.hours else "") + f" · VRAM 임계 {a.vram_limit}%")

    # 지난 세션의 미완(doing) 회수
    try:
        jobs = sb.table("transcribe_jobs").select("id").eq("runner", "local").eq("status", "running").execute().data or []
        for j in jobs:
            sb.table("transcribe_job_pages").update({"status": "pending"}).eq("job_id", j["id"]).eq("status", "doing").execute()
    except Exception:
        pass

    idle_note = False
    while True:
        if not in_hours(a.hours):
            if not idle_note:
                print("· 가동 시간대 밖 — 대기"); idle_note = True
            time.sleep(60); continue
        wd.gate()
        jobs = sb.table("transcribe_jobs").select("*").eq("runner", "local").eq("status", "running")\
                 .order("created_at").execute().data or []
        pg = None
        for job in jobs:
            r = sb.rpc("claim_job_page", {"p_job": job["id"]}).execute()
            if r.data:
                pg = r.data[0]; break
        if not pg:
            if not idle_note:
                print("· 대기 중인 로컬 작업 없음 — 60초 후 재확인"); idle_note = True
            time.sleep(60); continue
        idle_note = False

        t0 = time.time()
        try:
            saved, esc = process_page(sb, job, pg, a.model)
            sb.table("transcribe_job_pages").update({"status": "done", "saved": saved, "arbitrated": esc,
                                                     "updated_at": "now()"}).eq("id", pg["id"]).execute()
            print(f"[{datetime.now():%H:%M}] {job['title'][:14]} p.{pg['page']} — 문항 {saved} · 대기 {esc} · {time.time()-t0:.0f}초")
        except Exception as e:
            sb.table("transcribe_job_pages").update({"status": "error", "error": str(e)[:300],
                                                     "updated_at": "now()"}).eq("id", pg["id"]).execute()
            print(f"[{datetime.now():%H:%M}] p.{pg['page']} 실패 — {e}")
        sb.table("transcribe_jobs").update({"updated_at": "now()"}).eq("id", job["id"]).execute()

        # 페이지 소진 시 작업 마감 (분류는 별도 — 로컬 작업도 클라우드 분류를 태우려면 화면에서 전환)
        left = sb.table("transcribe_job_pages").select("id", count="exact").eq("job_id", job["id"])\
                 .eq("status", "pending").execute().count or 0
        doing = sb.table("transcribe_job_pages").select("id", count="exact").eq("job_id", job["id"])\
                  .eq("status", "doing").execute().count or 0
        if left == 0 and doing == 0:
            print(f"== 페이지 소진: {job['title']} — 분류·마감은 코퍼스 화면을 열어두면 클라우드가 처리 ==")
        if a.once:
            break


if __name__ == "__main__":
    main()
