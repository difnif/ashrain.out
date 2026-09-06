# -*- coding: utf-8 -*-
# v1.5 재작업 집계·보고서·장부 갱신: out/v15/REWORK_REPORT.md, PROGRESS.md(재작업 절), ZIPS_STATUS.md(헤더 한 줄)
import json, glob, os, collections, datetime, importlib.util, sys, re
sys.path.insert(0, "/root/esc"); import mathir as m14
spec = importlib.util.spec_from_file_location("m15", "/root/esc/mathir_v15.py"); m15 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m15)
def ok14(o):
    if m14.parse_text(o["question"])[2]: return False
    for c in (o["choices"] or []):
        if m14.parse_text(c)[2]: return False
    if o["answer"] is not None:
        try: m14.parse_answer(str(o["answer"]))
        except Exception: return False
    if o["figure"] and m14.check_figure(o["figure"]): return False
    return True
batches = {os.path.basename(f)[5:7]: json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob("rework/batch*.json"))}
src = {}
for b, L in batches.items():
    for x in L: src.setdefault(x["id"], (b, x))          # 첫 등장 batch(원 보류 사유)
fin, rev, ext = {}, {}, []
for f in sorted(glob.glob("out/v15/*.rework_final.json")):
    z = os.path.basename(f).replace(".rework_final.json", ""); L = json.load(open(f, encoding="utf-8"))
    for x in L: x["v14_ok"] = ok14(x["final"]); fin[x["id"]] = (z, x)
    json.dump(L, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for f in sorted(glob.glob("out/v15/*.rework_review.json")):
    z = os.path.basename(f).replace(".rework_review.json", "")
    for x in json.load(open(f, encoding="utf-8")): rev[x["id"]] = (z, x)
for f in sorted(glob.glob("out/v15/*.rework_extra.json")):
    z = os.path.basename(f).replace(".rework_extra.json", "")
    for x in json.load(open(f, encoding="utf-8")): ext.append((z, x))
assert len(fin) + len(rev) == len(src) == 712 and not (set(fin) & set(rev)), (len(fin), len(rev), len(src))
n14 = sum(1 for z, x in fin.values() if x["v14_ok"])
tags = collections.Counter(t for z, x in fin.values() for t in x["final"]["pattern_tags"] if t != "v15재작업")
first = {}
for l in open("PROGRESS.md", encoding="utf-8"):
    if l.startswith("| esc_"):
        c = [t.strip() for t in l.strip().strip("|").split("|")]
        first[c[0]] = (int(c[1].replace("문항", "")), int(c[2].split("(")[0].replace("통과", "")), int(c[3].replace("보류", "")))
pz = collections.OrderedDict()
for z in first:
    pz[z] = (first[z], sum(1 for i, (zz, x) in fin.items() if zz == z), sum(1 for i, (zz, x) in rev.items() if zz == z))
tot_n = sum(v[0][0] for v in pz.values()); tot_p1 = sum(v[0][1] for v in pz.values()); tot_r1 = sum(v[0][2] for v in pz.values())
# 회수 경로(마지막으로 처리한 batch) 집계
last_batch = {}
for b, L in batches.items():
    for x in L: last_batch[x["id"]] = b
by_round = collections.Counter(("r1(batch00~10)" if last_batch[i] <= "10" else "r2(batch11~14)") for i in fin)
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d %H:%M KST")
R = [f"# v1.5 재작업 보고 — 보류 712건 (갱신 {now})\n",
     "- 대상: 1차 전사(v1.4)에서 보류된 712건 전부(`out\\{zip}.review.json`). 검산 기준: `mathir_v15.py` **r2**(제안 패치 — `improvements/` 교체용, 명세 `MATHIR_V15_CHANGES.md`). 이미지 근거로 텍스트 혼합 부분을 v1.5 표기(`cases`, `app`, `seg(A'B')`, `angle(F'PF)`, `vec(OP1)`, `point3`, `cdots`, `box`, `xbar` … + r2: `op`, `nota`, `idx`, `tr`, `dig`, 문자 `recdec`, `a'`, 원문자·양의 부호 답)로 고쳤고, 답은 초안 값을 유지했다(새로 채운 답은 note에 근거).",
     f"- 결과: **통과 {len(fin)} / 잔여 보류 {len(rev)}** (1라운드 batch00~10에서 {by_round['r1(batch00~10)']}, 2라운드 batch11~14에서 {by_round['r2(batch11~14)']}). 전체 4,421문항 기준 통과 {tot_p1 + len(fin)}({(tot_p1 + len(fin))/4421*100:.1f}%) · 보류 {len(rev)}({len(rev)/4421*100:.1f}%).",
     f"- 통과 {len(fin)}건 중 **{n14}건은 v1.4로도 검산 통과**(`v14_ok: true`) → 패치 전 반영 가능. 나머지 {len(fin) - n14}건은 v1.5(r2) 전용 → `mathir.py`·`mathir.js` 패치 뒤 반영. 반영용 병합 파일은 `reflect\\v14\\`·`reflect\\v15\\`(단원별).",
     f"- 둘째 문항 {len(ext)}건(`{{zip}}.rework_extra.json`, 한 이미지 두 문항의 id 없는 쪽을 완전 전사, 검산 통과 {sum(1 for z, x in ext if x['status'] == 'ok')}) → id 발급 후 삽입.",
     "- 태그(pattern_tags): " + ", ".join(f"`{k}` {v}" for k, v in tags.most_common()) + ".",
     "- 산출: `out\\v15\\{zip}.rework_final.json`(반영용, `final`은 final.json과 같은 형식, `rework_note`·`v14_ok`) / `.rework_review.json`(잔여 보류) / `.rework_extra.json`(둘째 문항) / `figs\\*.png`(image 도형 자산 18개, src는 `figs/…`).",
     "- 재현 자료(`tools_v15\\`): `GUIDE_REWORK.md`(SOP, r2 절 포함) · `build_rework.py` · `rework\\batch00~14.json` · `rework_batch00~14.py` · `make_report.py` · `mathir_v15.py`.\n",
     "## 묶음별 결과\n\n| batch | 항목 | 통과 | 잔여 보류 | 비고 |\n|---|---|---|---|---|"]
note = {"11": "사용자 정의 연산·기호, 프라임 상수", "12": "문자 순환소수·자릿수, 답 기호 ㉠㉡㉢, 양의 부호 답, 한글 조건 경우나눔", "13": "그림 선지·그림 정보(image 자산), 이미지 잘림", "14": "한 이미지 두 문항(둘째 문항은 extra)"}
for b, L in batches.items():
    ids = [x["id"] for x in L]
    if b <= "10":
        a = sum(1 for i in ids if i in fin and last_batch[i] == b); r = len(ids) - a
        R.append(f"| {b} | {len(L)} | {a} | {r} | 1라운드(잔여 {r}건은 batch11~14로) |")
    else:
        a = sum(1 for i in ids if i in fin); r = sum(1 for i in ids if i in rev)
        R.append(f"| {b} | {len(L)} | {a} | {r} | 2라운드: {note[b]} |")
R.append(f"| 합계(고유 712) | 712 | {len(fin)} | {len(rev)} | |\n")
R.append(f"## 잔여 보류 {len(rev)}건 (사용자 결정: 그대로 둠)\n")
for i, (z, x) in rev.items(): R.append(f"- {z} · {i[:8]} — {x['reason'][:140]}")
R.append("\n## zip별 (1차 → 재작업 후)\n\n| zip | 문항 | 1차 통과 | 1차 보류 | 재작업 통과 | 잔여 보류 | 최종 통과 |\n|---|---|---|---|---|---|---|")
for z, ((n, p1, r1), a, r) in pz.items(): R.append(f"| {z} | {n} | {p1} | {r1} | {a} | {r} | {p1 + a} |")
R.append(f"| 합계 | {tot_n} | {tot_p1} | {tot_r1} | {len(fin)} | {len(rev)} | {tot_p1 + len(fin)} |")
open("out/v15/REWORK_REPORT.md", "w", encoding="utf-8").write("\n".join(R) + "\n")
P = open("PROGRESS.md", encoding="utf-8").read()
if "## v1.5 재작업" in P: P = P.split("## v1.5 재작업")[0].rstrip() + "\n"
S = [f"\n## v1.5 재작업 ({now})\n",
     f"- 보류 712건을 `mathir_v15.py`(r2) 문법으로 재전사: **통과 {len(fin)} · 잔여 보류 {len(rev)}**(사용자 결정: 그대로 둠). 둘째 문항 {len(ext)}건은 `.rework_extra.json`(id 발급 후 삽입). 산출 `out\\v15\\`, 보고 `out\\v15\\REWORK_REPORT.md`, 반영용 병합 파일 `reflect\\`.",
     f"- 통과 {len(fin)} 중 v1.4로도 검산 통과 {n14}건(`v14_ok`) — 패치 전 반영 가능. 나머지 {len(fin) - n14}건은 v1.5 r2 패치(mathir.py·mathir.js) 적용 뒤 반영.",
     f"- 전체 집계(재작업 반영): 4,421문항 중 통과 {tot_p1 + len(fin)}({(tot_p1 + len(fin))/4421*100:.1f}%) · 보류 {len(rev)}.\n"]
open("PROGRESS.md", "w", encoding="utf-8").write(P + "\n".join(S))
Z = open("ZIPS_STATUS.md", encoding="utf-8").read().split("\n")
Z[0] = f"# ZIP 처리 현황 ({now})"
line = f"- v1.5 재작업(보류 712건): 통과 {len(fin)} · 잔여 보류 {len(rev)}(그대로 둠) · 둘째 문항 {len(ext)} → 전체 통과 {tot_p1 + len(fin)}({(tot_p1 + len(fin))/4421*100:.1f}%) · 보류 {len(rev)}. 산출 `out\\v15\\`, 반영 파일 `reflect\\` (`out\\v15\\REWORK_REPORT.md` 참조)"
k = next((i for i, l in enumerate(Z) if "v1.5 재작업" in l), None)
if k is None: Z.insert(next(i for i, l in enumerate(Z) if l.startswith("- 산출물")) + 1, line)
else: Z[k] = line
open("ZIPS_STATUS.md", "w", encoding="utf-8").write("\n".join(Z))
print(f"final {len(fin)} (v14_ok {n14}) review {len(rev)} extra {len(ext)} | 전체 통과 {tot_p1 + len(fin)} | tags {dict(tags)} | rounds {dict(by_round)}")
