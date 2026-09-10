# genkit/labels.py — 문항 라벨 (v2.0 · 라벨 레지스트리 L-01~L-47 정합)
#
# 근거 문서
#   · 「문항 · 유저 라벨 / 분석 알고리즘 리스트업 v2」 (2026-08-19) — L-01~38 / U-01~39 / A-01~28
#   · 「문항 생성 시스템 설계 문서 v0.1」 (2026-08-22) — cost·math_key·오답=오개념함수·θ/b 분리
#
# 원칙 (레지스트리 문서 그대로)
#   · 파일럿 차단 요소는 A군(L-01~12)뿐. B군은 소급 가능, C군·U군은 별도 테이블.
#   · L-06(예상) / L-25(실측)는 **영구 분리** — 여기서는 L-06만 쓴다. 덮어쓰지 않는다.
#   · 라벨 키는 `L06_difficulty_prior` 처럼 **ID + 이름** 으로 둔다 (레지스트리 대조 가능).
#
# 이 파일이 채우는 것: A군 L-01~11 · B군 L-13~24 · 신규 후보 L-39~47.
# C군(L-25~38)은 유저 데이터가 있어야 하므로 `item_stats` / `segment_stats` 쪽에서 채운다.

from __future__ import annotations

import re
from fractions import Fraction

from .rules import cost_of, shape_of

# ---------------------------------------------------------------- 신규 후보 라벨 (레지스트리 추가 제안)
NEW_LABELS = {
    "L-39": "표상 — 문항이 어떤 형태로 제시되는가 (식/수직선/좌표/표/그래프/평면도형/입체도형/글/자료)",
    "L-40": "인지 과정 — 개념이해/절차수행/추론/문제해결/표현",
    "L-41": "맥락 — 무맥락/생활맥락/기하맥락/자료맥락",
    "L-42": "오답↔오개념 사상 — 보기 원문 → 오개념 코드 (A-10 오개념 프로파일의 직접 입력)",
    "L-43": "변별 목표 — 이 문항이 가르려는 능력 경계 (A-02 템플릿 성적표 대조용)",
    "L-44": "변주축 좌표 — schemas.axes 의 어느 칸인지 (A-04 구간 난이도 지도)",
    "L-45": "출처 — schema_id + 유형 참조한 원문항 id (복제 아님을 추적)",
    "L-46": "math_key — 의미 키. 표면이 달라도 수학이 같으면 같은 값 (다양성 예산)",
    "L-47": "cost — 중간 계산값 비용. L-06 난이도의 산출 근거 (cost→b 회귀의 입력)",
    "L-48": "해설 단수 — 기하 2단 / 그 외 3단",
    "L-49": "채점기준 배점 총점 — 서술형 채점 루브릭",
}

# ---------------------------------------------------------------- 통제 어휘
PROCESS = ["개념이해", "절차수행", "추론", "문제해결", "표현"]                      # L-40
REPRESENTATION = ["식", "수직선", "좌표", "표", "그래프", "평면도형", "입체도형", "글", "자료"]  # L-39
CONTEXT = ["무맥락", "생활맥락", "기하맥락", "자료맥락"]                              # L-41
ANSWER_TYPE = ["정수", "분수", "소수", "식", "좌표", "집합", "단어", "여러값"]        # L-08
ITEM_FORM = ["객관식", "단답", "서술", "증명"]                                       # L-07
OPS = ["사칙", "지수", "근호", "인수분해", "방정식", "부등식", "비례", "백분율",
       "함수", "각도", "넓이", "부피", "통계", "확률"]                               # L-14
TRAPS = ["부호", "단위", "조건누락", "역연산", "구하는대상혼동", "제곱누락", "평균오용"]  # L-21

# ---------------------------------------------------------------- 오개념 코드표 (L-20·L-42)
# 설계문서 v0.1 §1 "오답 = 오개념 함수" — 학생의 선택이 곧 진단이 된다.
# 새 코드는 반드시 여기 먼저 등록하고 시드에서 코드로만 참조한다(자유 문자열 금지).
MISCONCEPTIONS = {
    # 수와 연산
    "MC-SIGN-01": "음수 부호를 빠뜨림",
    "MC-SIGN-02": "뺄셈에서 부호를 바꾸지 않음 (a-(-b))",
    "MC-ORDER-01": "연산 순서 무시 (곱셈·나눗셈 우선 안 함)",
    "MC-FRAC-01": "분모끼리·분자끼리 더함",
    "MC-FRAC-02": "통분하지 않고 계산",
    "MC-FRAC-03": "역수를 취하지 않고 분수 나눗셈",
    "MC-DEC-01": "소수점 자리 어긋남",
    "MC-ABS-01": "절댓값을 부호 제거로만 이해",
    "MC-MID-01": "중점 대신 두 수의 합/차를 씀",
    "MC-DIST-01": "거리에서 절댓값을 취하지 않음",
    # 문자와 식
    "MC-ALG-01": "동류항이 아닌 항을 합침",
    "MC-ALG-02": "괄호 앞 음수를 분배하지 않음",
    "MC-ALG-03": "계수와 차수를 혼동",
    "MC-EQ-01": "이항할 때 부호를 바꾸지 않음",
    "MC-EQ-02": "양변에 같은 연산을 하지 않음",
    # 함수·그래프
    "MC-FUN-01": "기울기와 y절편을 바꿔 읽음",
    "MC-FUN-02": "x의 증가량과 y의 증가량을 뒤집음",
    "MC-FUN-03": "정비례와 반비례를 혼동",
    # 기하
    "MC-GEO-01": "넓이 공식에 밑변·높이가 아닌 변을 넣음",
    "MC-GEO-02": "반지름과 지름을 혼동",
    "MC-GEO-03": "닮음비와 넓이비를 같게 봄 (제곱 누락)",
    "MC-GEO-04": "겉넓이와 부피를 혼동 (차원 혼동)",
    "MC-GEO-05": "각의 합 성질을 잘못 적용 (삼각형 180°)",
    "MC-GEO-06": "π를 빠뜨리거나 3으로 대체",
    "MC-SECT-01": "중심각 비율을 곱하지 않고 원 전체로 계산",
    "MC-SECT-02": "부채꼴의 호의 길이와 넓이를 바꿔 씀",
    "MC-POLY-01": "다각형 내각의 합에서 (n-2)를 n으로 씀",
    "MC-POLY-02": "내각의 합과 한 내각을 혼동 (n으로 나누지 않음)",
    "MC-TRI-01": "삼각형 세 내각의 합을 360°로 봄",
    "MC-TRI-02": "외각을 이웃한 내각과 같다고 봄",
    "MC-CYL-01": "원기둥 부피에서 반지름을 제곱하지 않음",
    "MC-CYL-02": "지름을 반지름으로 그대로 씀",
    "MC-CYL-03": "원기둥 겉넓이에서 밑면을 하나만 셈",
    "MC-CYL-04": "옆면 직사각형의 가로를 원주 2πr가 아니라 지름·반지름으로 씀",
    "MC-CONE-01": "뿔의 부피에 1/3을 곱하지 않음 (기둥의 부피로 계산)",
    "MC-CONE-02": "원뿔 옆넓이에서 모선 대신 높이를 씀",
    "MC-SPH-01": "구의 부피 4/3 또는 겉넓이 4를 빠뜨림",
    "MC-DIAG-01": "대각선 개수에서 2로 나누지 않음 (두 번 셈)",
    "MC-DIAG-02": "한 꼭짓점에서 그을 수 있는 대각선을 n − 2 로 봄 (n − 3 이 맞음)",
    "MC-ANG-01": "평각을 360°로 봄 (180°가 맞음)",
    "MC-ANG-02": "맞꼭지각이 아닌 이웃한 각을 같다고 봄",
    "MC-MEAN-01": "평균에서 합을 개수로 나누지 않거나 개수를 잘못 셈",
    "MC-MEAN-02": "두 집단의 평균을 인원수와 무관하게 단순 평균 냄",
    "MC-INEQ-01": "음수로 나눌 때 부등호의 방향을 바꾸지 않음",
    "MC-INEQ-02": "이항할 때 부호를 바꾸지 않음 (부등식)",
    "MC-INEQ-03": "부등호 방향이 반대인 해를 고름",
    "MC-EXP-01": "지수법칙에서 지수끼리 곱함 (aᵐ × aⁿ = aᵐⁿ 으로)",
    "MC-EXP-02": "거듭제곱의 거듭제곱에서 지수를 더함 ((aᵐ)ⁿ = aᵐ⁺ⁿ 으로)",
    "MC-EXP-03": "나눗셈에서 지수를 나눔 (aᵐ ÷ aⁿ = aᵐ÷ⁿ 으로)",
    "MC-EXP-04": "곱의 거듭제곱에서 계수에 지수를 적용하지 않음",
    "MC-DIGIT-01": "두 자리 수를 10a + b 가 아니라 ab(곱)나 a + b 로 씀",
    "MC-PCT-01": "증감률을 각 집단이 아니라 전체에 적용함",
    # 공간 — 위치관계
    "MC-POS-01": "만나지 않으면 모두 평행이라고 봄 (꼬인 위치를 평행으로)",
    "MC-POS-02": "한 점에서 만나는 모서리를 꼬인 위치(또는 평행)로 봄",
    "MC-POS-03": "면에 포함된 모서리를 면과 평행하다고 봄",
    "MC-POS-04": "면과 수직인 모서리와 면에 평행한 모서리를 혼동",
    # 통계·확률
    "MC-STAT-01": "도수와 상대도수를 혼동",
    "MC-STAT-02": "평균 대신 중앙값(또는 반대)",
    "MC-PROB-01": "전체 경우의 수를 잘못 셈",
    # 활용 유형
    "MC-TRAIN-01": "통과 거리에 기차 길이를 더하지 않음",
    "MC-CONC-01": "농도를 두 농도의 단순 평균으로 계산",
    # 절차·부주의
    "MC-CALC-01": "단순 계산 실수",
    "MC-UNIT-01": "단위 환산 누락 (분↔시간, cm↔m)",
    "MC-READ-01": "구하는 대상을 잘못 읽음 (중간값을 답으로)",
}

_HANGUL = re.compile(r"[가-힣]")
_DEC = re.compile(r"\d+\.\d+")
_FIG_REPR = {
    "numline": "수직선", "coordplane": "좌표", "funcgraph": "그래프", "scatter": "자료",
    "table": "표", "hist": "자료", "stemleaf": "자료", "boxplot": "자료",
    "scene": "평면도형", "tri": "평면도형", "quad": "평면도형", "polygon": "평면도형",
    "rect": "평면도형", "circle": "평면도형", "sector": "평면도형",
    "crossing": "평면도형", "parallel": "평면도형", "point": "좌표",
    "solid": "입체도형", "net": "입체도형", "wire": "입체도형", "venn": "자료", "tree": "자료",
    "journey": "글", "passing": "글", "river": "글", "mountain": "글",
}
_OP_HINTS = [
    ("근호", r"sqrt\(|root\(|√"),
    ("지수", r"pow\(|\^|제곱|세제곱|거듭제곱"),
    ("인수분해", r"인수분해|소인수|약수|배수"),
    ("방정식", r"방정식|이항|미지수"),
    ("부등식", r"부등식|이상이|이하이|초과|미만"),
    ("비례", r"비례|닮음비|정비례|반비례"),
    ("백분율", r"%|퍼센트|농도|할인"),
    ("함수", r"함수|기울기|절편|그래프|좌표"),
    ("각도", r"각도|∠|deg\(|°|내각|외각|각의 크기"),
    ("넓이", r"넓이|겉넓이"),
    ("부피", r"부피|들이|용량"),
    ("통계", r"평균|중앙값|최빈값|도수|상대도수|분산|표준편차"),
    ("확률", r"확률|경우의 수"),
]


def item_form(qtype, answer_type):                                              # L-07
    if qtype == "choice":
        return "객관식"
    if answer_type in ("단어",) or qtype == "essay":
        return "서술"
    return "단답"


def answer_type(ans: str) -> str:                                               # L-08
    s = str(ans).strip()
    if re.fullmatch(r"-?\d+", s):
        return "정수"
    if "frac(" in s:
        return "분수"
    if _DEC.fullmatch(s.replace("[[", "").replace("]]", "")):
        return "소수"
    if s.startswith("point(") or re.fullmatch(r"\(\s*-?\d+\s*,\s*-?\d+\s*\)", s):
        return "좌표"
    if "set(" in s:
        return "집합"
    if "또는" in s or "|" in s:
        return "여러값"
    if _HANGUL.search(s) or re.fullmatch(r"[A-Z]{2,4}", s):    # 모서리·면 이름(AB, ABCD)도 '단어'
        return "단어"
    return "식"


def numeric_load(env: dict, question: str) -> dict:                             # L-16
    vals = [v for v in env.values() if isinstance(v, (int, float, Fraction))]
    mag = max([abs(float(v)) for v in vals], default=0)
    return {
        "magnitude": ("한자리" if mag < 10 else "두자리" if mag < 100 else "세자리이상"),
        "negative": any(float(v) < 0 for v in vals) or bool(re.search(r"(?<![\d)])-\s?\d", question)),
        "fraction": any(isinstance(v, Fraction) and v.denominator != 1 for v in vals) or "frac(" in question,
        "decimal": bool(_DEC.search(question)),
        "max_cost": max([cost_of(v) for v in vals], default=0),
    }


def detect_ops(text: str, declared=None) -> list:                               # L-14
    if declared:
        return [o for o in declared if o in OPS]
    found = [name for name, pat in _OP_HINTS if re.search(pat, text)]
    return found or ["사칙"]


def answer_traits(answer_val, ans_type) -> list:                                # L-22
    t = [ans_type]
    if answer_val is None:
        return t
    try:
        f = float(answer_val)
    except (TypeError, ValueError):
        return t
    if abs(f) < 1e-12:
        t.append("답이 0")
    if abs(f - 1) < 1e-12:
        t.append("답이 1")
    if f < 0:
        t.append("답이 음수")
    if abs(f) >= 1000:
        t.append("답이 큰 수")
    if shape_of(answer_val) == "분수":
        t.append("답이 분수")
    return t


def param_bucket(idx: int, space: int) -> str:                                  # L-23
    if space <= 1:
        return "단일"
    if idx <= 0 or idx >= space - 1:
        return "경계"          # ★ 검수 표본에 반드시 포함해야 하는 구간 (R-06)
    r = idx / (space - 1)
    return "하위" if r < 1 / 3 else ("중위" if r < 2 / 3 else "상위")


def auto_labels(item: dict, tpl: dict, seed: dict, env: dict, ctx: dict) -> dict:
    """문항 하나에 붙일 라벨. ctx = {idx, space, site, at, gates, builder}"""
    figs = item.get("figure") or []
    fns = [f.get("fn") for f in figs if isinstance(f, dict)]
    reprs = sorted({_FIG_REPR.get(f, "글") for f in fns})
    if not reprs:
        reprs = ["글"] if _HANGUL.search(item["question"]) else ["식"]
    sol = item.get("solution") or {}
    steps = sol.get("steps") or []
    at = answer_type(item.get("answer", ""))
    body = item["question"] + " " + " ".join(steps)

    return {
        "registry": "labels-v2",
        # ── A군 출생 라벨 (L-01~11)
        "L01_cid": seed.get("concept_ids", []),
        "L02_template_id": tpl.get("id"),
        "L03_param_index": ctx["idx"],
        "L04_content_key": ctx["content_key"],
        "L05_struct_key": ctx["struct_key"],
        "L06_difficulty_prior": tpl.get("difficulty"),
        "L07_item_form": item_form(item.get("qtype"), at),
        "L08_answer_type": at,
        "L09_builder": {"model": "fable-chat", "builder": ctx["builder"], "seed": seed.get("seed_id")},
        "L10_made_at": {"at": ctx["at"], "site": ctx["site"]},
        "L11_verify": ctx["gates"],
        # ── B군 파생 라벨 (L-13~24)
        "L13_steps_n": len(steps),
        "L14_ops": detect_ops(body, tpl.get("ops")),
        "L15_prereq": tpl.get("prereq", []),
        "L16_numeric": numeric_load(env, item["question"]),
        "L17_stem_len": len(item["question"]),
        "L18_narrative": bool(tpl.get("context") and tpl["context"] != "무맥락"),
        "L19_needs_figure": bool(fns),
        "L20_distractor_rule": sorted({c for c in (item.get("_distractor_map") or {}).values() if c}),
        "L21_traps": [t for t in (tpl.get("traps") or []) if t in TRAPS],
        "L22_answer_traits": answer_traits(ctx.get("answer_val"), at),
        "L23_param_bucket": param_bucket(ctx["idx"], ctx["space"]),
        "L24_time_est": tpl.get("time_limit"),
        # ── 신규 후보 (L-39~49)
        "L39_representation": reprs,
        "L40_process": tpl.get("process", "절차수행"),
        "L41_context": tpl.get("context", "기하맥락" if any(r.endswith("도형") for r in reprs) else "무맥락"),
        "L42_distractor_map": item.get("_distractor_map", {}),
        "L43_discriminates": tpl.get("discriminates"),
        "L44_variant_axis": tpl.get("variant_axis", {}),
        "L45_source": {"schema_id": seed.get("schema_id"), "items": seed.get("source_item_ids", [])},
        "L46_math_key": item.get("_math_key"),
        "L47_cost": {"cost": item.get("_cost"), "level": item.get("_cost_level")},
        "L48_solution_levels": len(sol.get("levels") or []),
        "L49_rubric_total": (sol.get("rubric") or {}).get("total"),
        # 편의 필드 (감사·검수에서 참조)
        "geometry": bool(sol.get("check_auto")),
        "figure_fns": fns,
    }


def validate_labels(lab: dict) -> list:
    e = []
    if lab.get("L40_process") not in PROCESS:
        e.append(f"L40 process는 {PROCESS} 중 하나 (받은 값: {lab.get('L40_process')})")
    if lab.get("L41_context") not in CONTEXT:
        e.append(f"L41 context는 {CONTEXT} 중 하나 (받은 값: {lab.get('L41_context')})")
    for r in lab.get("L39_representation", []):
        if r not in REPRESENTATION:
            e.append(f"L39 representation에 미등록 값 {r}")
    if lab.get("L08_answer_type") not in ANSWER_TYPE:
        e.append(f"L08 answer_type 미등록 {lab.get('L08_answer_type')}")
    if lab.get("L07_item_form") not in ITEM_FORM:
        e.append(f"L07 item_form 미등록 {lab.get('L07_item_form')}")
    for o in lab.get("L14_ops", []):
        if o not in OPS:
            e.append(f"L14 ops에 미등록 값 {o}")
    for code in lab.get("L20_distractor_rule", []):
        if code not in MISCONCEPTIONS:
            e.append(f"미등록 오개념 코드 {code} — labels.MISCONCEPTIONS에 먼저 등록할 것")
    if lab.get("L07_item_form") == "객관식" and not lab.get("L42_distractor_map"):
        e.append("객관식인데 오답↔오개념 사상이 없음 — 진단 신호를 못 걷는다")
    if not lab.get("L01_cid"):
        e.append("L01 concept_ids 비어 있음")
    if lab.get("L06_difficulty_prior") not in (1, 2, 3, 4, 5):
        e.append("L06 난이도는 1~5")
    return e


def flat_tags(lab: dict) -> list:
    """test_items.tags 로 넣을 납작한 태그 (기존 앱 호환 · 검색용)."""
    n = lab.get("L16_numeric", {})
    t = [f"process:{lab.get('L40_process')}", f"ctx:{lab.get('L41_context')}",
         f"form:{lab.get('L07_item_form')}", f"ans:{lab.get('L08_answer_type')}",
         f"steps:{lab.get('L13_steps_n')}", f"bucket:{lab.get('L23_param_bucket')}",
         f"cost:{(lab.get('L47_cost') or {}).get('cost')}"]
    t += [f"repr:{r}" for r in lab.get("L39_representation", [])]
    t += [f"op:{o}" for o in lab.get("L14_ops", [])]
    t += [f"fig:{f}" for f in lab.get("figure_fns", [])]
    t += [f"trap:{x}" for x in lab.get("L21_traps", [])]
    if n.get("negative"):
        t.append("load:음수")
    if n.get("fraction"):
        t.append("load:분수")
    t.append(f"load:{n.get('magnitude')}")
    t += lab.get("L20_distractor_rule", [])
    return [x for x in t if x and not x.endswith("None")]
