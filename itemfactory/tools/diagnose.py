# itemfactory/tools/diagnose.py — 탈락 통계 → 처방 (v1.0)
#
# genkit 이 남긴 리포트를 읽어, 통과율이 낮은 틀에 **무엇을 어떻게 고치라고** 알려 준다.
# 원칙(설계문서 v0.1 §4): 제약은 필터가 아니라 생성 규칙에 내장한다.
#   값을 자유롭게 뽑고 더러우면 버리기 → 통과율 18%
#   처음부터 조건을 만족하는 꼴로 생성   → 통과율 92%
#
#   python tools/diagnose.py                 # out/gen 의 모든 리포트
#   python tools/diagnose.py --min 0.5       # 통과율 50% 미만만
#   python tools/diagnose.py --json          # 기계용 출력

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

# 사유 패턴 → (진단, 처방)
RX = [
    (r"G1:.*%\s*\(?[^=]*\)?\s*==\s*0",
     "정수해 조건을 사후에 걸러내고 있다",
     "파라미터를 '조건을 이미 만족하는 꼴'로 생성하라. 예: (2*r*th) % 360 == 0 대신 "
     "th 를 360의 약수로 고정하고 r 을 그 몫의 배수로 뽑는다 → params 에 base 파라미터를 두고 derive 에서 r = base * k."),
    (r"G1:.*파생값 .* 계산 실패",
     "퇴화 파라미터(0으로 나눔·복소수)가 도메인에 들어 있다",
     "그 조합이 애초에 뽑히지 않도록 params 의 범위를 좁혀라. derive 는 constraints 보다 먼저 계산되므로 "
     "'divide by zero' 를 constraints 로 막을 수 없다."),
    (r"G1:제약 위반 .*!=",
     "서로 달라야 하는 값이 같아지는 조합이 많다",
     "두 파라미터를 독립으로 뽑지 말고 차이를 파라미터로 두어라. 예: a, b 대신 a 와 k(=b-a)."),
    (r"G1:제약 위반 .*(<=|>=|<|>)",
     "부등식 제약을 사후에 걸러내고 있다",
     "params 의 범위 자체를 좁혀라. 범위를 좁혀도 공간이 목표의 3배 이상이면 손해가 없다."),
    (r"G3:.*R-01",
     "오답의 겉모양(정수/분수)이 정답과 달라 계산 없이 배제된다",
     "오답 식을 정답과 같은 꼴이 되도록 설계하라(정답이 정수면 오답도 정수). "
     "또는 distractor_fmt 로 표기를 맞춰라."),
    (r"G3:.*R-02",
     "퇴화 파라미터에서 서로 다른 오개념이 같은 값으로 붕괴한다",
     "붕괴에 안전한 오답(값이 파라미터에 확실히 의존하는 것)을 distractors 앞쪽에 배치하고, "
     "붕괴가 잦은 구간은 constraints 로 제외하라."),
    (r"G3:.*R-03",
     "오답 값이 발문에 이미 나온 수다",
     "오답 식을 바꾸거나, 그 값이 발문에 나오지 않는 파라미터 구간으로 제한하라."),
    (r"G3:.*R-05|G3:.*정답이 문면",
     "정답이 발문에 그대로 노출된다",
     "그 조합을 constraints 로 제외하라(예: kl != r, c != a)."),
    (r"G3:.*쓸 수 있는 오답이",
     "오답 후보가 모자란다",
     "distractors 를 6~8개로 늘려라. 4개만 두면 하나만 탈락해도 문항이 통째로 버려진다."),
    (r"G4:.*도형",
     "도형 인자가 정규 스키마를 벗어났다",
     "figspec.SPEC 의 필수·선택 인자만 쓰고, 숫자는 숫자로(문자열 금지), 좌표는 [x, y] 로."),
    (r"G4:",
     "MathIR 문법 오류",
     "[[ ]] 마커 안의 식이 v1.5 문법인지 확인하라. 한국어 단위는 마커 밖에 둔다."),
    (r"G5:.*해설 단수",
     "기하/비기하 판정과 해설 단수가 어긋난다",
     "시드의 geometry 를 명시하고, 기하면 sol3 를 두지 말 것(2단), 비기하면 sol3 를 둘 것(3단)."),
    (r"G5:",
     "형식·라벨 규격 위반",
     "SEEDSPEC.md 의 필수 항목(난이도 1~5, 통제 어휘, 오개념 코드 등록)을 확인하라."),
    (r"DUP:문면\+보기 동일",
     "수치가 그림에만 있어 문면이 서로 같다",
     "발문에 수치를 함께 써라. DB의 content_key 가 문면+보기 기준이라 그림만 다른 문항은 병합된다."),
    (r"DUP:",
     "같은 문항이 반복 생성된다",
     "params 가 실제로 다른 문항을 만드는지 확인하라(쓰이지 않는 파라미터가 있으면 공간만 부풀고 중복이 난다)."),
]


def prescribe(reason: str):
    for pat, diag, fix in RX:
        if re.search(pat, reason):
            return diag, fix
    return "분류되지 않은 사유", "리포트의 원문을 보고 시드를 검토하라."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(HERE / "out" / "gen"))
    ap.add_argument("--min", type=float, default=0.6, help="이 통과율 미만인 틀만 진단 (기본 0.6)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    out = []
    for f in sorted(Path(a.dir).glob("*_report.json")):
        rep = json.loads(f.read_text(encoding="utf-8"))
        for tid, st in rep["per_template"].items():
            tried = st["ok"] + st["rej"]
            rate = st["ok"] / tried if tried else 0
            entry = {"seed": rep["seed_id"], "template": tid, "space": st["space"],
                     "ok": st["ok"], "rej": st["rej"], "rate": round(rate, 3),
                     "headroom": round(st["space"] / max(1, st["target"]), 1), "advice": []}
            for why, cnt in sorted(st["by_gate"].items(), key=lambda kv: -kv[1])[:4]:
                diag, fix = prescribe(why)
                entry["advice"].append({"n": cnt, "reason": why, "diagnosis": diag, "fix": fix})
            out.append(entry)

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    bad = [e for e in out if e["rate"] < a.min]
    print(f"틀 {len(out)}개 중 통과율 {a.min:.0%} 미만 {len(bad)}개\n")
    for e in sorted(out, key=lambda x: x["rate"]):
        mark = "⚠" if e["rate"] < a.min else "·"
        print(f"{mark} {e['template']:<28} 통과 {e['ok']:>4}/{e['ok']+e['rej']:<5} ({e['rate']:>5.1%}) "
              f"· 공간 {e['space']} (목표의 {e['headroom']}배)")
        if e["rate"] >= a.min:
            continue
        for ad in e["advice"]:
            print(f"    [{ad['n']:>4}건] {ad['diagnosis']}")
            print(f"           → {ad['fix']}")
        print()
    if not bad:
        print("모든 틀이 기준 통과율을 넘었다. 타율이 낮아도 공간이 넉넉하면 손해는 없다.")


if __name__ == "__main__":
    main()
