# -*- coding: utf-8 -*-
"""
local_pipeline.py — 노트북(RAM만, GPU 불필요)에서 Claude API로 escalated 문항을 재전사하는 로컬 파이프라인.

  준비:  pip install anthropic pillow
         set ANTHROPIC_API_KEY=...            (Windows)  /  export ANTHROPIC_API_KEY=... (mac/linux)
         이 파일과 같은 폴더(또는 --tools)에 mathir.py, GUIDE.md 가 있어야 함.
  실행:  python local_pipeline.py --zip "C:\\Users\\User\\Documents\\esc files\\esc_sonnet_m3-1_1of6.zip"
         python local_pipeline.py --zip-dir "C:\\Users\\User\\Documents\\esc files" --pattern "esc_sonnet_m3-*.zip"
  옵션:  --model claude-sonnet-4-5 (기본; 정확도 우선이면 claude-opus-4-1) --concurrency 4 --out out --resume

  동작:  zip 해제 → manifest 항목마다 [이미지 + 지시문] → 모델이 JSON 항목 생성 → mathir.py 4관문 검산
         → 실패 시 오류 메시지를 돌려주고 1회 재시도 → final / final_qamismatch / review 로 분류 → PROGRESS.md 갱신.
  메모리: 이미지 1장씩 base64로 보내고 결과만 보관하므로 수십 MB면 충분.  중단돼도 --resume 으로 이어서.
"""
import argparse, asyncio, base64, glob, io, json, os, re, sys, time, zipfile, datetime
from pathlib import Path

# ------------------------------------------------------------------ 설정
SCHEMA = {
    "qtype": "choice|short|essay", "question": "…[[수식]]…", "choices": ["5개 문자열 (choice일 때만, 아니면 null)"],
    "derived_answer": "이미지에 답이 있거나 짧은 풀이로 확실할 때만, 아니면 null",
    "figure": "[{fn, args}] 또는 null", "difficulty_est": "1~5 또는 null", "confidence": "0~1",
    "needs_review": "보류 사유 문자열 또는 null", "note": "한 줄", "unit_id": "내용이 명백히 다른 단원일 때만, 아니면 null",
}
CIRC = "①②③④⑤⑥⑦⑧⑨⑩"

def norm_ans(s):
    if s is None: return None
    s = str(s).strip()
    if s in CIRC: return str(CIRC.index(s) + 1)
    return s.replace(" ", "")

def extract_zip(zpath, workdir):
    dst = Path(workdir) / Path(zpath).stem
    dst.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(zpath)
    for info in z.infolist():
        name = info.filename
        if not (info.flag_bits & 0x800):
            try: name = info.filename.encode("cp437").decode("utf-8")
            except Exception: pass
        target = dst / name
        if info.is_dir(): target.mkdir(parents=True, exist_ok=True); continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(z.read(info))
    return dst

def image_block(path, upscale=1):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if upscale != 1: im = im.resize((im.width * upscale, im.height * upscale), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG")
    return {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64.b64encode(buf.getvalue()).decode()}}

def gates(mathir, item):
    errs = []
    _, _, e1 = mathir.parse_text(item.get("question") or "")
    if e1: errs.append(f"question: {e1}")
    for k, c in enumerate(item.get("choices") or []):
        _, _, e2 = mathir.parse_text(c)
        if e2: errs.append(f"choice{k+1}: {e2}")
    if item.get("derived_answer") is not None:
        try: mathir.parse_answer(str(item["derived_answer"]))
        except Exception as ex: errs.append(f"answer: {ex}")
    if item.get("figure"):
        e4 = mathir.check_figure(item["figure"])
        if e4: errs.append(f"figure: {e4}")
    if item.get("qtype") == "choice" and len(item.get("choices") or []) != 5: errs.append("choice인데 choices가 5개가 아님")
    if item.get("qtype") != "choice" and item.get("choices"): errs.append("choice가 아닌데 choices가 있음")
    return errs

def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else None

async def transcribe_one(client, model, guide, mathir, m_item, img_path, sem, retries=3):
    """모델 호출 → 검산 → (실패 시 오류 피드백 1회) → dict 반환"""
    user_text = (f"다음 문항 이미지를 GUIDE의 규칙대로 mathir v1.4 문법으로 전사하고, 아래 키를 가진 JSON 객체 하나만 출력하라(설명 금지).\n"
                 f"키/규칙: {json.dumps(SCHEMA, ensure_ascii=False)}\n"
                 f"manifest: id={m_item['id'][:8]}, seq={m_item['seq']}, unit_id={m_item['unit_id']}, src_tag={m_item.get('src_tag')}\n"
                 f"(quick_answer는 정렬이 어긋난 경우가 많으므로 절대 베끼지 말 것. 이미지가 유일한 근거.)")
    content = [image_block(img_path), {"type": "text", "text": user_text}]
    messages = [{"role": "user", "content": content}]
    async with sem:
        for attempt in range(retries + 1):
            try:
                resp = await client.messages.create(model=model, max_tokens=4000, system=guide, messages=messages)
                text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
                item = parse_json(text)
                if not item: raise ValueError("JSON 없음: " + text[:200])
                errs = gates(mathir, item)
                if not errs: return item
                if attempt >= 1:  # 2번째 실패 → 그대로 반환(review로 감)
                    item["needs_review"] = (item.get("needs_review") or "") + f" / 검산 불통과: {errs}"
                    return item
                messages += [{"role": "assistant", "content": text},
                             {"role": "user", "content": f"mathir 검산 오류: {errs}\n문법을 고쳐 같은 형식의 JSON만 다시 출력하라. 표현할 수 없는 부분은 텍스트 혼합으로 두고 needs_review에 사유를 적어라."}]
            except Exception as ex:  # 레이트리밋 등
                if "rate" in str(ex).lower() or "429" in str(ex) or "overloaded" in str(ex).lower():
                    await asyncio.sleep(15 * (attempt + 1)); continue
                if attempt >= retries: return {"needs_review": f"API 오류: {ex}", "question": "", "qtype": "short", "choices": None}
                await asyncio.sleep(3)
    return {"needs_review": "재시도 초과", "question": "", "qtype": "short", "choices": None}

def classify(m_item, item):
    obj = {"seq": m_item["seq"], "qtype": item.get("qtype", "short"), "question": item.get("question", ""),
           "choices": item.get("choices"), "answer": item.get("derived_answer"),
           "difficulty_est": item.get("difficulty_est"), "has_math": True,
           "has_figure": bool(item.get("figure")), "figure": item.get("figure") or None,
           "unit_id": item.get("unit_id") or m_item["unit_id"], "concept_main": None, "concept_subs": [],
           "pattern_tags": [], "confidence": item.get("confidence", 0.9)}
    qa = m_item.get("quick_answer"); ans = obj["answer"]
    qa_mismatch = qa is not None and ans is not None and norm_ans(qa) != norm_ans(ans)
    if qa_mismatch: obj["pattern_tags"] = ["빠른정답불일치"]
    if item.get("needs_review"):
        return "review", {"id": m_item["id"], "image": m_item["image"], "reason": item["needs_review"] + ((" — " + item["note"]) if item.get("note") else ""), "draft": obj}
    if qa_mismatch:
        return "final_qamismatch", {"id": m_item["id"], "final": obj, "qa_note": f"전사·풀이 답 {ans} vs 빠른정답 {qa}"}
    return "final", {"id": m_item["id"], "final": obj}

async def run_zip(zpath, args, guide, mathir, client):
    zn = Path(zpath).stem
    work = extract_zip(zpath, args.work)
    manifest = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
    outdir = Path(args.out); outdir.mkdir(exist_ok=True)
    cache_path = outdir / f"{zn}.cache.jsonl"          # 항목별 결과 캐시(--resume)
    cache = {}
    if args.resume and cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line); cache[r["id"]] = r["item"]
    sem = asyncio.Semaphore(args.concurrency)
    todo = [it for it in manifest["items"] if it["id"] not in cache]
    print(f"[{zn}] items {len(manifest['items'])}, cached {len(cache)}, todo {len(todo)}")
    async def worker(it):
        item = await transcribe_one(client, args.model, guide, mathir, it, work / it["image"], sem)
        cache[it["id"]] = item
        with open(cache_path, "a", encoding="utf-8") as f: f.write(json.dumps({"id": it["id"], "item": item}, ensure_ascii=False) + "\n")
        print(f"  done {it['id'][:8]} {it['image'].split('/')[-1][:40]}  {'REVIEW' if item.get('needs_review') else 'ok'}")
    await asyncio.gather(*(worker(it) for it in todo))
    buckets = {"final": [], "final_qamismatch": [], "review": []}
    for it in manifest["items"]:
        kind, obj = classify(it, cache[it["id"]]); buckets[kind].append(obj)
    for kind, arr in buckets.items():
        (outdir / f"{zn}.{kind}.json").write_text(json.dumps(arr, ensure_ascii=False, indent=1), encoding="utf-8")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    row = f"| {zn} | 문항 {len(manifest['items'])} | 통과 {len(buckets['final']) + len(buckets['final_qamismatch'])} (빠른정답불일치 {len(buckets['final_qamismatch'])}) | 보류 {len(buckets['review'])} | {now} |"
    prog = Path(args.progress)
    text = prog.read_text(encoding="utf-8") if prog.exists() else "| zip이름 | 문항 n | 통과 n | 보류 n | 완료시각 |\n|---|---|---|---|---|\n"
    text = re.sub(rf"\| {re.escape(zn)} \|.*\n", "", text).rstrip("\n") + "\n" + row + "\n"
    prog.write_text(text, encoding="utf-8")
    print(row)

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip"); ap.add_argument("--zip-dir"); ap.add_argument("--pattern", default="*.zip")
    ap.add_argument("--tools", default=str(Path(__file__).parent)); ap.add_argument("--work", default="work"); ap.add_argument("--out", default="out")
    ap.add_argument("--progress", default="PROGRESS.md"); ap.add_argument("--model", default="claude-sonnet-4-5")
    ap.add_argument("--concurrency", type=int, default=4); ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, args.tools); import mathir  # noqa
    guide = Path(args.tools, "GUIDE.md").read_text(encoding="utf-8")
    guide += "\n\n## 출력 형식\n설명 없이 JSON 객체 하나만 출력한다. 이미지에 없는 내용을 만들지 않는다. quick_answer는 절대 복사하지 않는다."
    from anthropic import AsyncAnthropic
    client = AsyncAnthropic()
    zips = [args.zip] if args.zip else sorted(glob.glob(str(Path(args.zip_dir) / args.pattern)))
    for z in zips:
        await run_zip(z, args, guide, mathir, client)

if __name__ == "__main__":
    asyncio.run(main())
