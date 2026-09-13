# itemfactory/tools/hsseed.py — 고등부 시드 생성 공용 헬퍼 (v1.0 · 2026-09-13 세션 5)
#
#   from hsseed import T, SEED, run
#   t = T("h1-1-poly", 1, BASE, title=…, skill=…, axis={…}, disc=…, diff=2,
#         params=[…], derive={…}, constraints=[…], cost=[…], verify=[…],
#         q="…", answer="{ans}",
#         sol1="…", sol2=[("식", "힌트", ("표시할 조각", "메모")), ("식2", "힌트2")], sol3=["확인 문장", "도식 한 줄", "도식 두 줄"],
#         model="…", rubric=[("요소", 3, "기준", "부분"), ("요소2", 2, "기준", "부분")],
#         pitfalls=[("실수", "요소", "불인정"), …])
#   sol2 의 각 항목은 (text, hint?, mark?) — 도식(steps)과 애니메이션을 자동으로 만든다. sol3 는 [본문, 도식1, 도식2].
#   비기하 3단 해설 규격. 기하(그림) 틀은 geo=True 로 넘기면 sol3 → sol_check 로 옮긴다.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402,F401


def T(seed_id, no, base, *, title, skill, axis, disc, diff, params, q, answer, sol1, sol2, sol3, model, rubric, pitfalls,
      table=None, derive=None, constraints=None, cost=None, ans_var="ans", verify=None, answer_alt=None, figure=None, sol1_fig=None, sol1_anim=None, geo=False, **extra):
    t = dict(base)
    t.update(extra)
    t["id"] = f"{seed_id}-t{no}"
    t.update(title=title, skill=skill, variant_axis=axis, discriminates=disc, difficulty=diff, params=params, question=q, answer=answer, answer_alt=answer_alt or [])
    if table is not None:
        t["table"] = table
    if derive:
        t["derive"] = derive
    if constraints:
        t["constraints"] = constraints
    if cost:
        t["cost_values"] = cost
    if ans_var:
        t["answer_var"] = ans_var
    if verify:
        t["verify"] = verify
    if figure is not None:
        t["figure"] = figure
    if sol1_fig is not None:
        t["sol1_fig"] = sol1_fig
    if sol1_anim is not None:
        t["sol1_anim"] = sol1_anim
    t["sol1"] = sol1
    lines, fig, anim = [], [], []
    for i, item in enumerate(sol2):
        text, hint, mark = (list(item) + [None, None])[:3] if isinstance(item, (list, tuple)) else (item, None, None)
        lines.append(text)
        d = {"text": text}
        keys = [f"hint:{i}"] if hint else []
        if hint:
            d["hint"] = hint
        if mark:
            d["marks"] = [{"on": mark[0], "note": mark[1]}]
            keys.append(f"mark:{i}-0")
        fig.append(d)
        anim.append([reveal(i)] + ([hl(*keys)] if keys else []))
    t["sol2"], t["sol2_fig"], t["sol2_anim"] = lines, steps(fig), anim
    body, l1, l2 = (list(sol3) + [None, None])[:3]
    if geo:
        t["sol_check"] = body
        t["geometry"] = True
    else:
        t["sol3"] = body
        t["sol3_fig"] = steps([x for x in (l1, l2) if x])
        t["sol3_anim"] = [[reveal(i)] for i in range(len([x for x in (l1, l2) if x]))]
        t["geometry"] = False
    t["model_answer"] = model
    fix = lambda e: "값 구하기" if e.strip() == "답" else e          # noqa: E731 — '답' 은 rubric.normalize 가 걸러내는 예약어
    t["rubric"] = [{"element": fix(e), "points": p, "criterion": c, "partial": pa} for (e, p, c, pa) in rubric]
    t["rubric_total"] = sum(p for (_, p, _, _) in rubric)
    t["pitfalls"] = [{"text": a, "on": fix(b), "effect": c} for (a, b, c) in pitfalls]
    return t


def SEED(seed_id, *, category, title, unit_id, concept_ids, schema_name, note, templates, geometry=False):
    return {"seed_id": seed_id, "category": category, "title": title, "unit_id": unit_id, "concept_ids": concept_ids,
            "schema_id": None, "schema_name": schema_name, "source_item_ids": [], "note": note, "geometry": geometry, "templates": templates}


def run(*seeds):
    for seed in seeds:
        with_pitfalls(seed, strict=False)       # 실수거리는 틀 안에 inline — 등록부(pitfalls.py)에는 tools/pitfalls_sync.py 로 모은다
        dump(seed)


NZ = lambda lo, hi: [v for v in range(lo, hi + 1) if v != 0]  # noqa: E731
HS = {"process": "절차수행", "context": "무맥락", "time_limit": 100, "points": 4, "qtype": "short", "pool_target": 300}
