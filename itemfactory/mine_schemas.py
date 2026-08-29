# ashrain.out — 스키마 마이닝 러너 (mine_schemas.py, v1.0 — 1단: 채굴)
# 위치: itemfactory/mine_schemas.py
#
# 코퍼스를 (단원 × 매쓰플랫 유형명) 그룹으로 묶어, 그룹당 표본 ≤10문항을 소넷에 보여
# {관계식계(MathIR)·변수 역할·변주 축·암묵 제약·성립 조건·등급}을 추출하고
# 관계식은 mathir로 즉석 문법 검증 후 schemas 테이블에 적재한다.
# 적합도 시험(sympy 재풀이)·특이점 반례탐색은 2단(mine_fit.py)에서.
#
# 사용:
#   python mine_schemas.py plan                    # 그룹 분포 보고 (API 0원)
#   python mine_schemas.py mine m1-1 --limit 5     # 파일럿: m1-1에서 5그룹만
#   python mine_schemas.py mine m1-1               # 단원 전체
#   python mine_schemas.py mine all                # 전 단원 (이미 채굴된 그룹은 건너뜀)
# 준비: itemfactory/.env 에 ANTHROPIC_API_KEY=sk-ant-... 한 줄 추가

import argparse, json, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mathir  # noqa: E402
from transcribe_local import load_env, get_client  # noqa: E402

try:
    import requests
except ImportError:
    sys.exit("pip install requests 필요")

MODEL = "claude-sonnet-4-5"
PRICE_IN, PRICE_OUT = 3, 15  # $/MTok

SYS_M = """너는 수학 문항 스키마 채굴자다. 같은 유형의 문항 표본을 보고, 그 유형의 생성 스키마를 JSON 하나로 출력한다. JSON 밖 텍스트 금지.

출력 규격:
{"name":"스키마 이름(간결한 한국어)",
 "grade":"A|B|C",
 "grade_why":"한 줄 근거",
 "relations":["d = v*t","t1 + t2 = T"],
 "roles":{"d":"거리(km)","v":"속력(km/h)","t":"시간(h)"},
 "axes":[{"axis":"구하는 것 순환","values":["d 미지","v 미지","t 미지","왕복 t2 미지"]},
         {"axis":"수치 범위","values":["정수 해","분수 해 허용"]}],
 "implicit":["v > 0","t > 0","해는 양수"],
 "conditions":{"declarations":["문면에 반드시: 'x에 대한 일차방정식' 같은 필수 선언(있다면)"],
               "singularities":["a != 0 (a=0이면 불성립)"],
               "uniqueness":["해가 유일하기 위한 조건"]},
 "notes":"표본에서 관찰된 특징·주의점 한두 줄"}

규칙:
- relations는 MathIR 문법만: 숫자, 변수, + - * / = != < > <= >=, 괄호, 병치곱,
  함수 frac mixed pow sqrt root abs recdec floor fact max min ratio pct log ln sin cos tan
  sum lim prime perm comb prob 등. 유니코드 수학기호·LaTeX 금지. 관계 하나당 문자열 하나.
- grade 판정: A = 관계식계로 완전 포착, 역할 순환 변주가 그대로 먹힘 (문장제 대부분).
  B = 구조 파라미터형 — 관계는 있으나 변주 축이 유형 고유 (약수 개수, 규칙 찾기, 그래프 해석).
  C = 스키마 저항 — 진위, 증명, 작도, 자료 해석. C면 relations는 비워도 되고 notes에 사유.
- conditions는 이 유형의 '소거 오류 요소': 빠지면 문제가 불성립하는 것들. 없으면 빈 배열.
- 표본에 없는 것을 지어내지 말 것. 표본이 이질적이면 notes에 "혼합 유형 의심" 표기."""


def anthropic(messages, system, max_tokens=2500):
    import os
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("itemfactory/.env 에 ANTHROPIC_API_KEY=... 추가 필요")
    r = requests.post("https://api.anthropic.com/v1/messages", timeout=180, headers={
        "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01",
    }, json={"model": MODEL, "max_tokens": max_tokens,
             "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
             "messages": messages})
    j = r.json()
    if r.status_code != 200:
        raise RuntimeError(j.get("error", {}).get("message", f"api {r.status_code}"))
    u = j.get("usage", {})
    cost = (u.get("input_tokens", 0) * PRICE_IN + u.get("cache_creation_input_tokens", 0) * PRICE_IN * 1.25
            + u.get("cache_read_input_tokens", 0) * PRICE_IN * 0.1 + u.get("output_tokens", 0) * PRICE_OUT) / 1e6
    return "".join(b.get("text", "") for b in j.get("content", [])), cost


def groups(sb, unit=None):
    """(unit_id, src_tag) 그룹 분포 — active 문항만"""
    out, page = {}, 0
    q = sb.table("corpus_items").select("id,unit_id,src_tags,p_correct").eq("status", "active")
    if unit:
        q = q.eq("unit_id", unit)
    while True:
        rows = q.range(page * 1000, page * 1000 + 999).execute().data or []
        for r in rows:
            tag = (r.get("src_tags") or [None])[0]
            if not tag or not r.get("unit_id"):
                continue
            out.setdefault((r["unit_id"], tag), []).append(r)
        if len(rows) < 1000:
            break
        page += 1
    return out


def pick_sample(sb, unit, tag, cap=10):
    rows = sb.table("corpus_items").select("id,question,choices,answer,p_correct,difficulty_est") \
        .eq("status", "active").eq("unit_id", unit).contains("src_tags", [tag]) \
        .order("p_correct", desc=False).limit(60).execute().data or []
    if len(rows) <= cap:
        return rows
    step = max(1, len(rows) // cap)          # 정답률 스펙트럼 고르게
    return rows[::step][:cap]


def mine_group(sb, unit, tag, items):
    lines = []
    for i, r in enumerate(items, 1):
        ch = (" / 보기: " + " | ".join(map(str, r["choices"]))) if r.get("choices") else ""
        an = f" / 답: {r['answer']}" if r.get("answer") else ""
        pc = f" (정답률 {r['p_correct']}%)" if r.get("p_correct") is not None else ""
        lines.append(f"[{i}]{pc} {r['question']}{ch}{an}")
    user = f"단원 {unit} · 유형 「{tag}」 표본 {len(items)}문항:\n" + "\n".join(lines)
    text, cost = anthropic([{"role": "user", "content": user}], SYS_M)
    m = re.search(r"\{[\s\S]*\}", text)
    if not m:
        raise RuntimeError("JSON 없음")
    sc = json.loads(m.group(0))
    errs = 0
    for rel in sc.get("relations") or []:
        try:
            mathir.parse_answer(str(rel))
        except mathir.MathIRError:
            errs += 1
    row = {"unit_id": unit, "src_tag": tag, "name": sc.get("name"),
           "grade": (sc.get("grade") or "").upper()[:1] or None, "status": "draft",
           "relations": sc.get("relations"), "roles": sc.get("roles"), "axes": sc.get("axes"),
           "implicit": sc.get("implicit"), "conditions": sc.get("conditions"),
           "ir_errs": errs, "n_items": len(items),
           "seed_ids": [r["id"] for r in items],
           "note": sc.get("notes"), "model": MODEL}
    sb.table("schemas").upsert(row, on_conflict="unit_id,src_tag").execute()
    return sc, errs, cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["plan", "mine"])
    ap.add_argument("unit", nargs="?", default=None, help="m1-1 … h3-3 또는 all")
    ap.add_argument("--limit", type=int, default=None, help="이번에 처리할 그룹 수 상한")
    ap.add_argument("--redo", action="store_true", help="이미 채굴된 그룹도 다시")
    ap.add_argument("--tag", default=None, help="유형명 부분 일치 필터 (예: --tag 거리)")
    a = ap.parse_args()
    load_env()
    sb = get_client()

    if a.cmd == "plan":
        g = groups(sb, None if a.unit in (None, "all") else a.unit)
        by_unit = {}
        for (u, t), rows in g.items():
            by_unit.setdefault(u, []).append((t, len(rows)))
        total = 0
        for u in sorted(by_unit):
            ts = sorted(by_unit[u], key=lambda x: -x[1])
            total += len(ts)
            print(f"{u}: 유형 {len(ts)}개 · 문항 {sum(n for _, n in ts)} · 최대 「{ts[0][0]}」({ts[0][1]})")
        est = total * 0.035
        print(f"\n총 그룹 {total} — 채굴 예상 비용 ~${est:.0f} (소넷, 캐시 감안)")
        return

    unit = a.unit
    if not unit:
        sys.exit("mine에는 단원 인자 필요 (m1-1 … 또는 all)")
    done = {(r["unit_id"], r["src_tag"]) for r in
            (sb.table("schemas").select("unit_id,src_tag").execute().data or [])} if not a.redo else set()
    g = groups(sb, None if unit == "all" else unit)
    todo = [(k, v) for k, v in sorted(g.items(), key=lambda kv: -len(kv[1])) if k not in done]
    if a.tag:
        todo = [(k, v) for k, v in todo if a.tag in k[1]]
    if a.limit:
        todo = todo[:a.limit]
    print(f"채굴 대상 {len(todo)}그룹 (건너뜀 {len(g) - len(todo)})")
    spent, ok = 0.0, 0
    for (u, tag), rows in todo:
        try:
            items = pick_sample(sb, u, tag)
            sc, errs, cost = mine_group(sb, u, tag, items)
            spent += cost
            ok += 1
            flag = f" ⚠IR오류 {errs}" if errs else ""
            print(f"  [{ok}/{len(todo)}] {u} 「{tag}」 → {sc.get('grade')}급 · {sc.get('name')}{flag} · ${cost:.3f}")
        except Exception as e:
            print(f"  ✗ {u} 「{tag}」 실패 — {e}")
        time.sleep(0.4)
    print(f"\n완료 {ok}/{len(todo)} · 지출 ${spent:.2f} — 승인은 #/admin/schemas 에서")


if __name__ == "__main__":
    main()
