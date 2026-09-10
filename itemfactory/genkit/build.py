# genkit/build.py — 시드 명세 → 수치변주 실체화 → 5관문 → 산출 (v1.0)
#
#   python -m genkit.build seeds/m1-1-numline-midpoint.json --n 120
#   python -m genkit.build seeds/*.json --n 120 --outdir out/gen
#   python -m genkit.build seeds/*.json --n 120 --push --status draft   # 승인 후에만
#
# 산출
#   out/gen/<seed_id>_pool.json     통과 문항 (반영용 payload)
#   out/gen/<seed_id>_report.json   틀별 통계 + 관문별 탈락 사유
#   out/gen/_summary.json           전체 요약
#
# DB에는 --push 를 줄 때만 쓴다. 기본은 드라이런.

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import re
import socket
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from genkit import expr as E                     # noqa: E402
from genkit import figspec, gates, labels as LB, rules as R, rubric as RB  # noqa: E402
from genkit.gates import Reject                  # noqa: E402

BUILDER_VERSION = "genkit-1.1"     # 1.1: 파라미터 공간 순회를 곱셈 순열로 (접두사 대표성)


# ---------------------------------------------------------------- 키
def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


def strict_key(template_id, idx):
    """엄격 키 — 설계문서 v0.1 §1. template_id:param_index 라 유일성이 수학적으로 보장된다."""
    return f"{template_id}:{idx}"


def surface_key(q, ch, fig=None):
    """표면 키 — 문면+보기+도형 해시. 틀 사이의 우연 충돌 방어용."""
    base = q + " " + (json.dumps(ch, ensure_ascii=False) if ch else "")
    if fig:
        base += " " + json.dumps(fig, ensure_ascii=False, sort_keys=True)
    return hashlib.md5(_norm(base).encode()).hexdigest()


def math_key(template_id, values):
    """의미 키 — 표면이 달라도 수학이 같으면 같은 값. 거부 기준이 아니라 다양성 예산."""
    body = "|".join(str(v) for v in values)
    return hashlib.md5(f"{template_id}|{body}".encode()).hexdigest()[:16]


def struct_key(q, ch, fig=None):
    base = q + " " + (json.dumps(ch, ensure_ascii=False) if ch else "")
    if fig:
        base += " " + json.dumps(fig, ensure_ascii=False, sort_keys=True)
    return hashlib.md5(_norm(re.sub(r"\d+(?:\.\d+)?", "#", base)).encode()).hexdigest()


# ---------------------------------------------------------------- 해설 조립
GEO_TITLES = ["도형 읽기", "계산·결론"]
GEN_TITLES = ["방침", "전개", "확인"]


def _figs(tpl, key, env):
    """해설 단계에 붙는 도식. 문항 도형과 같은 문법이되 해설 전용 fn(journey·passing·bar·steps)도 허용."""
    raw = tpl.get(key)
    if not raw:
        return None
    figs = E.fill_num(json.loads(json.dumps(raw)), env)
    for f in figs:
        a = f.get("args") or {}
        for k, v in list(a.items()):
            if isinstance(v, float) and abs(v - round(v)) < 1e-9:
                a[k] = int(round(v))
    errs = figspec.check_figure_spec(figs, where="solution")
    if errs:
        raise Reject("G5", f"해설 도식 스키마 위반 {errs[:2]}")
    return figs


def _anim(tpl, key, env, n_steps=None):
    """단계별 애니메이션 큐. sol1_anim/sol3_anim 은 큐 배열 하나, sol2_anim 은 단계별 큐 배열의 배열."""
    raw = tpl.get(key)
    if not raw:
        return None
    cues = E.fill(json.loads(json.dumps(raw)), env)
    # 큐 키 정리 — 표 파생으로 빈 문자열이 된 자리(예: {par4})는 버린다
    def _clean(st):
        out = []
        for c in (st or []):
            k = c.get("k")
            if isinstance(k, list):
                k = [x for x in k if x]
                if not k:
                    continue
                c = {**c, "k": k if len(k) > 1 else k[0]}
            elif not k:
                continue
            out.append(c)
        return out
    if isinstance(cues, list) and cues and all(isinstance(x, list) for x in cues):
        cues = [_clean(st) for st in cues]
    elif isinstance(cues, list):
        cues = _clean(cues)
    if n_steps is None:                     # 단일 텍스트 단계 — 큐 하나([{..}]) 또는 순차 큐([[..],[..]])
        if isinstance(cues, list) and cues and isinstance(cues[0], list):
            return cues
        return [cues]
    out = list(cues) + [[] for _ in range(max(0, n_steps - len(cues)))]
    return out[:n_steps]


def assemble_solution(tpl, env, answer_text, geometry, kind="활용"):
    s1 = E.fill(tpl.get("sol1", ""), env)
    s2 = [E.fill(x, env) for x in (tpl.get("sol2") or [])]
    s3 = E.fill(tpl.get("sol3", ""), env) if tpl.get("sol3") else ""
    f1, f2, f3 = _figs(tpl, "sol1_fig", env), _figs(tpl, "sol2_fig", env), _figs(tpl, "sol3_fig", env)
    a1, a2, a3 = _anim(tpl, "sol1_anim", env), _anim(tpl, "sol2_anim", env, len(s2)), _anim(tpl, "sol3_anim", env)
    if geometry:
        if s3:
            raise Reject("G5", "기하 문항은 2단 해설 — sol3를 두지 말 것")
        levels = [{"level": 1, "title": GEO_TITLES[0], "text": s1, "figure": f1, "anim": a1},
                  {"level": 2, "title": GEO_TITLES[1], "steps": s2, "figure": f2, "anim": a2}]
        check = E.fill(tpl["sol_check"], {**env, "ans": answer_text}) if tpl.get("sol_check") else f"답: {answer_text}"
        sol = {"levels": levels, "outline": s1, "steps": s2, "check": check, "check_auto": True}
    else:
        if not s3:
            raise Reject("G5", "비기하 문항은 3단 해설 — sol3(확인)이 필요")
        levels = [{"level": 1, "title": GEN_TITLES[0], "text": s1, "figure": f1, "anim": a1},
                  {"level": 2, "title": GEN_TITLES[1], "steps": s2, "figure": f2, "anim": a2},
                  {"level": 3, "title": GEN_TITLES[2], "text": s3, "figure": f3, "anim": a3}]
        sol = {"levels": levels, "outline": s1, "steps": s2, "check": s3, "check_auto": False}
    sol["model_answer"] = _model_answer(tpl, env, s1, s2, s3, answer_text)
    sol["rubric"] = _rubric(tpl, env, s1, s2, s3, answer_text, geometry, kind=kind)
    return sol


def _model_answer(tpl, env, s1, s2, s3, answer_text):
    """서술형 답안 예시 — 학생이 그대로 옮겨 써도 되는 흐름글."""
    if tpl.get("model_answer"):
        return E.fill(tpl["model_answer"], env)
    body = " ".join(x.rstrip(".") + "." for x in s2)
    tail = f" 따라서 답은 {answer_text}이다."
    return (s1.rstrip() + " " + body + tail).strip()


def _rubric(tpl, env, s1, s2, s3, answer_text, geometry, kind="활용"):
    """채점기준표 v3 — 핵심 요소 5~8점(수행 수준) + 실수거리(checks) + 채점 원칙 (genkit/rubric.py)."""
    pit = [{"text": E.fill(p["text"], env), "on": p.get("on"), "effect": p.get("effect")} for p in (tpl.get("pitfalls") or [])]
    has_unit = bool(re.search(r"(km|cm|\bm\b|\bg\b|°|개|%|시간|분|초|원)", " ".join(tpl.get("answer_alt") or []) + " " + tpl.get("question", "")))
    if tpl.get("rubric"):
        items = []
        for i, r in enumerate(tpl["rubric"], 1):
            items.append({"no": i, "element": E.fill(r["element"], env),
                          "points": r["points"], "criterion": E.fill(r["criterion"], env),
                          "partial": E.fill(r.get("partial", ""), env) or None})
        return RB.normalize(items, kind=kind, pitfalls=pit, total=tpl.get("rubric_total"), has_unit=has_unit)
    pts = tpl.get("rubric_points") or {}
    items = [{"no": 1, "element": "풀이 방침 세우기", "points": pts.get("plan", 2),
              "criterion": s1, "partial": None}]
    for i, st in enumerate(s2, 1):
        items.append({"no": len(items) + 1, "element": f"전개 {i}단계", "points": pts.get("step", 2),
                      "criterion": st, "partial": None})
    items.append({"no": len(items) + 1, "element": "답 제시",
                  "points": pts.get("answer", 2),
                  "criterion": f"최종 답 {answer_text}을(를) 단위와 함께 바르게 썼다.", "partial": None})
    return RB.normalize(items, kind=kind, pitfalls=pit, total=tpl.get("rubric_total"), has_unit=has_unit)


# ---------------------------------------------------------------- 문항 하나
def build_one(seed, tpl, idx, ctx0=None):
    params = tpl["params"]
    env = E.params_at(params, idx)
    # 표 파생 — 문자열 파라미터(모서리 이름 등)에 딸린 값들을 행 단위로 붙인다.
    #   "table": {"key": "c", "rows": {"AB|0": {"e": "AB", "skew": "CG, DH, EH, FG", ...}, ...}}
    for tb in ([tpl["table"]] if isinstance(tpl.get("table"), dict) else (tpl.get("table") or [])):
        key = str(env.get(tb["key"]))
        row = (tb.get("rows") or {}).get(key)
        if row is None:
            raise Reject("G1", f"표 {tb['key']}={key!r} 행 없음")
        env.update(row)
    # 파생값
    for k, v in (tpl.get("derive") or {}).items():
        try:
            env[k] = E.evaluate(v, env)
        except Exception as ex:                          # noqa: BLE001
            raise Reject("G1", f"파생값 {k} 계산 실패 ({str(ex)[:60]})") from ex
    gates.g1_constraints(tpl, env)                      # 이른 탈락 — 비싼 조립 전에

    question = E.fill(tpl["question"], env)
    answer = E.fill(tpl["answer"], env)
    answer_val = None
    try:
        if tpl.get("answer_var"):                       # 답이 π·단위를 포함할 때: 수치는 이 변수로
            answer_val = env[tpl["answer_var"]]
        elif re.fullmatch(r"\{[^{}]+\}", tpl["answer"].strip()):
            answer_val = E.evaluate(tpl["answer"].strip()[1:-1], env)
    except Exception:                                    # noqa: BLE001
        answer_val = None

    figs = None
    if tpl.get("figure"):
        figs = json.loads(json.dumps(tpl["figure"]))
        figs = E.fill_num(figs, env)
        for f in figs:
            a = f.get("args") or {}
            for k, v in list(a.items()):
                if isinstance(v, float) and abs(v - round(v)) < 1e-9:
                    a[k] = int(round(v))

    geometry = tpl.get("geometry", seed.get("geometry"))
    if geometry is None:
        geometry = figspec.is_geometry(figs, tpl.get("tags"))

    # ── 난이도 비용 (설계문서 v0.1 §1) — 주어진 값(src)도 중간값에 포함(R-04)
    cost_src = tpl.get("cost_values")
    cost_vals = [E.evaluate(x, env) for x in cost_src] if cost_src else list(env.values())
    cost, cost_level = R.cost_and_level(cost_vals)

    dmap, choices = {}, None
    q_nums = R.numbers_in(question)
    ans_shape = R.shape_of(answer_val) if answer_val is not None else None
    if tpl["qtype"] == "choice":
        ds = tpl.get("distractors") or []
        vals, out, dropped = {}, [], []
        for d in ds:
            try:
                v = E.evaluate(d["expr"], env)
            except E.ExprError as ex:
                raise Reject("G3", f"오답 식 평가 실패 {d['expr']} ({ex})") from ex
            fmt = d.get("fmt") or tpl.get("distractor_fmt")
            txt = fmt.replace("{v}", E.show(v, marker=False)) if fmt else E.show(v)
            if txt == answer or txt in vals:
                dropped.append("R-02 값 붕괴(정답·다른 오답과 같아짐)")
                continue
            if ans_shape and R.shape_of(v) != ans_shape:     # R-01 겉모양 불일치
                dropped.append(f"R-01 겉모양 {R.shape_of(v)}≠{ans_shape}")
                continue
            if isinstance(v, (int, Fraction)) and Fraction(v) in q_nums:   # R-03 문면의 수
                dropped.append("R-03 문면에 이미 나온 수")
                continue
            vals[txt] = True
            out.append((txt, d.get("misconception")))
        if len(out) < 4:
            raise Reject("G3", f"쓸 수 있는 오답이 {len(out)}개 — 5지선다 불가 ({'; '.join(dropped[:3])})")
        out = out[:4]
        pick = [answer] + [t for t, _ in out]
        pick = sorted(pick, key=lambda s: (_sortkey(s), s))
        choices = pick
        dmap = {t: mc for t, mc in out}

    item = {
        "question": question, "answer": answer,
        "answer_alt": [E.fill(x, env) for x in (tpl.get("answer_alt") or [])],
        "choices": choices, "qtype": tpl["qtype"], "figure": figs,
        "_distractor_map": dmap,
    }
    # R-05 정답이 문면에 그대로 노출
    if tpl["qtype"] == "short" and isinstance(answer_val, (int, Fraction)) and Fraction(answer_val) in q_nums:
        raise Reject("G3", "R-05 정답이 문면에 그대로 노출됨")

    item["solution"] = assemble_solution(tpl, env, answer, geometry, kind=seed.get("category") or ("도형" if geometry else "활용"))
    mk_src = tpl.get("math_key_values") or (list((tpl.get("derive") or {}).keys()) + (["__ans"] if answer_val is not None else []))
    mk_vals = []
    for k in mk_src:
        mk_vals.append(answer_val if k == "__ans" else (env.get(k) if k in env else E.evaluate(k, env)))
    item["_math_key"] = math_key(tpl["id"], mk_vals)
    item["_cost"] = cost
    item["_cost_level"] = cost_level
    ctx = dict(ctx0 or {})
    ctx.update({"idx": idx, "answer_val": answer_val,
                "content_key": strict_key(tpl["id"], idx),
                "struct_key": struct_key(item["question"], item["choices"], item.get("figure")),
                "gates": {"G1": True, "G2": None, "G3": None, "G4": None, "G5": None}})
    lab = LB.auto_labels(item, tpl, seed, env, ctx)
    gates.g2_resolve(tpl, env, answer_val); ctx["gates"]["G2"] = True
    gates.g3_distractors(item, tpl); ctx["gates"]["G3"] = True
    gates.g4_mathir(item); ctx["gates"]["G4"] = True
    gates.g5_shape(item, tpl, geometry, lab); ctx["gates"]["G5"] = True
    lab["L11_verify"] = ctx["gates"]
    return item, lab, env


def _sortkey(s):
    try:
        import mathir
        node, _ = mathir.parse(re.fullmatch(r"\[\[(.+)\]\]", s, re.S).group(1) if s.startswith("[[") else s)
        return (0, float(mathir.ev(node)))
    except Exception:                                    # noqa: BLE001
        return (1, 0.0)


# ---------------------------------------------------------------- 시드 하나
def build_seed(seed, n_per_template, site):
    run_id = f"{seed['seed_id']}-{time.strftime('%Y%m%d-%H%M%S')}"
    accepted, rejects = [], []
    stat = {}
    for tpl in seed["templates"]:
        space = E.space_size(tpl["params"])
        target = min(n_per_template, tpl.get("pool_target", n_per_template))
        st = {"target": target, "space": space, "ok": 0, "rej": 0, "by_gate": Counter(), "samples": []}
        seen, dbkeys = set(), set()
        ctx0 = {"space": space, "site": site, "at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "builder": BUILDER_VERSION}
        tried = 0
        budget = max(target * 12, target + 200)
        for idx in _stream(space, budget):
            if st["ok"] >= target or tried >= budget:
                break
            tried += 1
            try:
                item, lab, env = build_one(seed, tpl, idx, ctx0)
            except Reject as r:
                st["rej"] += 1
                st["by_gate"][f"{r.gate}:{r.reason[:60]}"] += 1
                rejects.append({"run_id": run_id, "seed_id": seed["seed_id"], "template_id": tpl["id"],
                                "param_index": idx, "reason": f"{r.gate}: {r.reason}"})
                continue
            except Exception as ex:                       # noqa: BLE001
                st["rej"] += 1
                st["by_gate"][f"EX:{type(ex).__name__}: {str(ex)[:50]}"] += 1
                continue
            sk = surface_key(item["question"], item["choices"], item.get("figure"))
            if sk in seen:                      # 같은 틀 안에서는 전단사 색인이라 원래 안 나온다
                st["rej"] += 1
                st["by_gate"]["DUP:표면 완전중복"] += 1
                continue
            seen.add(sk)
            # 도형에만 수치가 있으면 문면+보기가 같아진다 → 옛 DB content_key 정의에서 병합됨
            if item.get("figure"):
                plain = surface_key(item["question"], item["choices"])
                if plain in dbkeys:
                    st["rej"] += 1
                    st["by_gate"]["DUP:문면+보기 동일(도형만 다름) — 수치를 문면에도 넣을 것"] += 1
                    rejects.append({"run_id": run_id, "seed_id": seed["seed_id"], "template_id": tpl["id"],
                                    "param_index": idx, "reason": "DUP: 문면+보기 동일(도형만 다름)"})
                    continue
                dbkeys.add(plain)
            accepted.append(payload(seed, tpl, item, lab, idx, sk, site))
            st["ok"] += 1
            if len(st["samples"]) < 3:
                st["samples"].append({"idx": idx, "q": item["question"], "a": item["answer"]})
        stat[tpl["id"]] = st
    return accepted, rejects, stat, run_id


def _stream(space, k):
    """파라미터 공간을 '곱셈 순열'로 훑는다 — idx_i = (i·g) mod space, gcd(g, space) = 1 (황금비 근처의 g).

    예전 방식(균등 격자 even_spread 를 앞에서부터)은 목표 수에 닿으면 조기 종료하므로 공간의 앞 15% 안팎만 쓰였고,
    그 결과 가장 느리게 변하는 첫 파라미터(맥락·부등호 종류 등)는 첫 값 하나만 나왔다(09-09 세션 1 관찰: 나이 t1 맥락 4개 중 1개,
    부등식 t3 '≤'만…). 또 격자 간격이 마지막 파라미터의 도메인 크기와 같으면(예: 11) 그 값이 전혀 변하지 않았다.
    곱셈 순열은 전단사이며(param_index 는 그대로 idx), g 가 space 와 서로소라 낮은 자릿수(빠른 파라미터)의 모든 조합을
    빠짐없이 순환하고 높은 자릿수(느린 파라미터)도 몇 걸음 안에 고르게 퍼진다 — 어느 접두사를 잘라도 대표성이 있다."""
    if space <= 2:
        yield from range(space)
        return
    g = max(2, int(round(space * 0.6180339887)))
    while math.gcd(g, space) != 1:
        g += 1
    for i in range(space):
        yield (i * g) % space


def payload(seed, tpl, item, lab, idx, sk, site):
    return {
        "test_type": seed.get("test_type", "concept_set"),
        "unit_id": seed["unit_id"], "concept_ids": seed.get("concept_ids", []),
        "qtype": item["qtype"], "difficulty": tpl["difficulty"],
        "question": item["question"], "choices": item["choices"],
        "answer": item["answer"], "answer_alt": item["answer_alt"],
        "points": tpl.get("points", 4),
        "time_limit": tpl.get("time_limit"),
        "tags": LB.flat_tags(lab),
        "solution": item["solution"],
        "figure": item["figure"],
        "labels": lab,
        "source": "seed",
        "category": seed.get("category"),
        "struct_key": struct_key(item["question"], item["choices"], item.get("figure")),
        "item_key": strict_key(tpl["id"], idx),       # 엄격 키 (unique) — content_key는 DB가 생성
        "template_id": tpl["id"],
        "param_index": idx,
        "math_key": item["_math_key"],
        "cost": item["_cost"],
        "prereq": tpl.get("prereq", []),
        "flag": None,
        "surface_key": sk,
        "gen_meta": {"seed": seed["seed_id"], "tpl": tpl["id"], "idx": idx,
                     "bv": BUILDER_VERSION, "site": site,
                     "schema_id": seed.get("schema_id"),
                     "source_item_ids": seed.get("source_item_ids", []),
                     "verified": True},
    }


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="시드 명세로 문항을 실체화하고 5관문으로 검산한다")
    ap.add_argument("seeds", nargs="+", help="시드 JSON 경로 (glob 가능)")
    ap.add_argument("--n", type=int, default=60, help="틀당 목표 문항 수 (기본 60)")
    ap.add_argument("--outdir", default=str(HERE / "out" / "gen"))
    ap.add_argument("--site", default=socket.gethostname())
    ap.add_argument("--push", action="store_true", help="DB(test_items) 업서트 — 승인 후에만")
    ap.add_argument("--status", default="draft", choices=["draft", "live"])
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    paths = []
    for p in a.seeds:
        paths += sorted(glob.glob(p)) or [p]
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    summary = {"builder": BUILDER_VERSION, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "seeds": []}
    total_ok = total_rej = 0

    for p in paths:
        seed = json.loads(Path(p).read_text(encoding="utf-8"))
        acc, rej, stat, run_id = build_seed(seed, a.n, a.site)
        total_ok += len(acc)
        total_rej += len(rej)
        (out / f"{seed['seed_id']}_pool.json").write_text(json.dumps(acc, ensure_ascii=False, indent=1), encoding="utf-8")
        rep = {"run_id": run_id, "seed_id": seed["seed_id"], "title": seed.get("title"),
               "accepted": len(acc), "rejected": len(rej),
               "per_template": {k: {**v, "by_gate": dict(v["by_gate"])} for k, v in stat.items()}}
        (out / f"{seed['seed_id']}_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
        summary["seeds"].append(rep)
        if not a.quiet:
            print(f"\n== {seed['seed_id']} · {seed.get('title','')} ==")
            for tid, s in stat.items():
                print(f"  {tid:<26} 공간 {s['space']:>7} · 목표 {s['target']:>4} · 통과 {s['ok']:>4} · 탈락 {s['rej']:>4}")
                for why, c in s["by_gate"].most_common(4):
                    print(f"      · {c:>4}건  {why}")
    (out / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n합계: 통과 {total_ok} · 탈락 {total_rej}  → {out}")

    if a.push:
        push(out, a.status)
    else:
        print("(드라이런 — DB에 쓰지 않았다. 반영하려면 --push)")


def push(outdir: Path, status: str):
    try:
        from supabase import create_client
    except ImportError:
        sys.exit("supabase 패키지 필요: pip install supabase --break-system-packages")
    for p in (HERE / ".env", Path.cwd() / ".env"):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
    n = 0
    for f in sorted(Path(outdir).glob("*_pool.json")):
        rows = json.loads(f.read_text(encoding="utf-8"))
        for r in rows:
            r.pop("surface_key", None)
            r.pop("category", None)          # test_items 에 없는 열(도형/활용/연산 분류) — 문항 태그에 이미 들어 있다
            r["status"] = status
        for i in range(0, len(rows), 200):
            sb.table("test_items").upsert(rows[i:i + 200], on_conflict="item_key",
                                          ignore_duplicates=True).execute()
        n += len(rows)
    print(f"  DB 업서트 시도 {n}건 (status={status})")


if __name__ == "__main__":
    main()
