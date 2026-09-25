#!/usr/bin/env python3
# tools/dbpush.py — 생성 풀(out/gen/*_pool.json) → Supabase test_items 반영 (HANDOFF-시드변형-v1 §8-3, 09-11)
#
#   python tools/dbpush.py out/gen --status draft
#   python tools/dbpush.py out/gen --status draft --replace-templates "m1-2-mean-t2 m2-2-centroid-*"
#   python tools/dbpush.py out/gen --dry-run              # DB 를 읽기만 하고 쓰지 않는다(계획·건수만)
#   python tools/dbpush.py out/gen --update-templates "m3-1-quad-build-t1 h2-2-lim-*"   # 제자리 갱신
#   python tools/dbpush.py out/gen --replace-templates "m1-2-mean-t2 @m3-1-quad-build-t1"  # 같은 뜻 — '@' 붙인 틀은 제자리 갱신
#
# genkit.build 의 --push(있는 문항은 건너뛰고 없는 것만 추가)와 같은 뜻이되 CI 용으로 세 가지를 더 한다.
#   ① 교체 모드 --replace-templates : 지정한 틀의 **draft 행만** 먼저 지운다. live 행은 절대 지우지 않는다
#      (live 문항의 교체는 Park 의 결정). `m2-2-centroid-*` 처럼 끝의 * 로 시드의 틀 전부를 고를 수 있다.
#      자동(push) 트리거는 이 옵션을 쓰지 않는다 — 추가만.
#   ② DB 에 이미 있는 item_key 를 먼저 읽어 **새 행만** 올린다(전체 재빌드를 올려도 전송량은 새 문항만큼).
#      올릴 때도 ON CONFLICT (item_key) DO NOTHING 이라 경쟁 상황에서도 덮어쓰지 않는다.
#   ③ 200행 묶음이 23505(유니크 위반)로 실패하면 한 행씩 다시 올려 문제 행만 건너뛰고 기록한다.
#      대표적 원인 = (test_type, content_key) 중복: 같은 문면이 **다른 item_key** 로 이미 있음
#      → 틀의 파라미터 공간이 바뀌어 색인(param_index)이 밀린 것. 끝까지 올린 뒤 종료 코드 1 로 알린다.
#      → 정리하려면 Actions 의 Run workflow 에서 replace_templates 에 그 틀을 적고 다시 실행.
#   ④ 제자리 갱신 --update-templates (09-25) — Actions 의 Run workflow 에서는 replace_templates 칸에 `@틀` 로 적는다
#      (워크플로 파일은 자동화 봇이 고칠 수 없어서 입력칸을 새로 만들지 않았다): 지정한 틀에서 DB 에 **이미 있는** 행(item_key 일치)을
#      live·draft 가리지 않고 새 빌드 내용으로 덮어쓴다. id·status·source·created_at 은 그대로 → 푼 기록(attempts 등)이
#      끊기지 않고, live 는 live 로 남는다. 바뀌는 열 = UPDATE_COLS, updated_at = 지금.
#      새 빌드에 없는 옛 행(파라미터 조합을 뺀 경우)은 draft 면 지우고, live 면 status='retired' 로 내린다
#      (지우지 않으므로 푼 기록은 남고, 학생 화면·「틀별」 집계에서는 빠진다. 되살리려면 status 를 live 로).
#      새 빌드에만 있는 행은 --status 로 추가(②와 같음). 문면이 다른 행과 같아져 23505 가 나면 그 행만 건너뛰고 알린다.
#
#   비밀: SUPABASE_URL · SUPABASE_SERVICE_KEY (GitHub secrets; 로컬은 itemfactory/.env 도 읽는다 — 클라이언트 코드 금지).
#   요약은 $GITHUB_STEP_SUMMARY(있으면)에 표로 남긴다.

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # itemfactory/
BATCH = 200
PAGE = 1000                                             # PostgREST max-rows 기본값
DROP_COLS = ("surface_key", "category")                 # test_items 에 없는 열 (build.py push 와 동일)
# 제자리 갱신이 덮어쓰는 열 — 식별·상태·출처·생성 시각(id, item_key, template_id, param_index, test_type, status, source,
# created_at)은 바꾸지 않는다. content_key 는 DB 생성 열이라 question·choices·figure 를 따라 저절로 바뀐다.
UPDATE_COLS = ("unit_id", "concept_ids", "qtype", "difficulty", "question", "choices", "answer", "answer_alt",
               "points", "time_limit", "tags", "solution", "figure", "labels", "struct_key", "math_key", "cost",
               "prereq", "flag", "gen_meta")
# ON CONFLICT 전에 후보 행의 NOT NULL 을 검사하므로, 갱신 묶음에도 식별 열은 같은 값으로 실어 보낸다(바뀌지 않음).
KEY_COLS = ("item_key", "test_type", "template_id", "param_index", "source")


# ---------------------------------------------------------------- 연결
def load_env() -> None:
    for p in (HERE / ".env", Path.cwd() / ".env"):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def connect():
    try:
        from supabase import create_client
    except ImportError:
        sys.exit("supabase 패키지 필요: pip install supabase")
    load_env()
    url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        sys.exit("SUPABASE_URL · SUPABASE_SERVICE_KEY 가 없다")
    return create_client(url, key)


def _api_error():
    from postgrest import APIError
    return APIError


# ---------------------------------------------------------------- ① 교체(draft 삭제)
PATTERN = re.compile(r"^[mh][1-3]-[1-3]-[a-z0-9]+(?:-[a-z0-9]+)*-(?:t\d+|\*)$")   # m1-2-mean-t2 · m2-2-centroid-* · h3-1-seqlim-* (09-15: 고등부 h 접두 허용) · h3-3-vecfig-t1 (09-26: 단원 번호 3 허용)


def parse_patterns(spec: str) -> list[str]:
    pats = [s for s in (spec or "").replace(",", " ").split() if s]
    for p in pats:
        if not PATTERN.match(p):
            sys.exit(f"replace_templates 항목이 이상하다: {p!r} — 'm1-2-mean-t2' 또는 'm1-2-mean-*'(h3-1-seqlim-* 처럼 고등부 h 접두도 됨) 꼴만 받는다")
    return pats


def _tpl_filter(q, pat: str):
    return q.like("template_id", pat[:-1] + "%") if pat.endswith("*") else q.eq("template_id", pat)


def delete_drafts(sb, pat: str, dry: bool) -> int:
    """pat 에 맞는 틀의 draft·seed 행을 지운다. live 는 건드리지 않는다. 지운(지울) 행 수를 돌려준다."""
    q = sb.table("test_items").select("id", count="exact", head=True).eq("status", "draft").eq("source", "seed")
    n = _tpl_filter(q, pat).execute().count or 0
    if n and not dry:
        d = sb.table("test_items").delete(returning="minimal").eq("status", "draft").eq("source", "seed")
        _tpl_filter(d, pat).execute()
    return n


# ---------------------------------------------------------------- ② 있는 키 읽기
def existing_keys(sb, template_ids: list[str]) -> dict[str, str]:
    """틀들의 DB 행 item_key → status."""
    have: dict[str, str] = {}
    ids = sorted(set(template_ids))
    for i in range(0, len(ids), 40):
        chunk, off = ids[i:i + 40], 0
        while True:
            rows = (sb.table("test_items").select("item_key,status").in_("template_id", chunk)
                    .order("item_key").range(off, off + PAGE - 1).execute().data) or []
            have.update({r["item_key"]: r.get("status") for r in rows if r.get("item_key")})
            if len(rows) < PAGE:
                break
            off += PAGE
    return have


def _matches(tid: str, pats: list[str]) -> bool:
    return any(tid.startswith(p[:-1]) if p.endswith("*") else tid == p for p in pats)


# ---------------------------------------------------------------- ③ 업서트
def _upsert(sb, rows):
    return sb.table("test_items").upsert(rows, on_conflict="item_key", ignore_duplicates=True,
                                         returning="minimal").execute()


def push_rows(sb, rows: list[dict], status: str, dry: bool):
    """새 행만 올린다. 돌려주는 값: (올린 수, 건너뛴 [(item_key, 사유)])."""
    APIError = _api_error()
    for r in rows:
        for c in DROP_COLS:
            r.pop(c, None)
        r["status"] = status
    added, skipped = 0, []
    if dry:
        return len(rows), skipped
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i + BATCH]
        try:
            _upsert(sb, batch)
            added += len(batch)
            continue
        except APIError as ex:
            if ex.code != "23505":
                raise
        for r in batch:                                  # 묶음이 유니크 위반 → 한 행씩
            try:
                _upsert(sb, [r])
                added += 1
            except APIError as ex:
                if ex.code != "23505":
                    raise
                why = "content 중복(같은 문면이 다른 item_key 로 있음)" if "content" in (ex.message or "") \
                    else (ex.message or "unique violation")[:120]
                skipped.append((r["item_key"], why))
    return added, skipped


# ---------------------------------------------------------------- ④ 제자리 갱신
def _merge(sb, rows):
    return sb.table("test_items").upsert(rows, on_conflict="item_key", ignore_duplicates=False,
                                         returning="minimal").execute()


def update_rows(sb, rows: list[dict], dry: bool):
    """DB 에 이미 있는 행을 제자리에서 덮어쓴다. 돌려주는 값: (갱신 수, 건너뛴 [(item_key, 사유)])."""
    APIError = _api_error()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    payload = [{**{c: r.get(c) for c in KEY_COLS}, **{c: r.get(c) for c in UPDATE_COLS if c in r}, "updated_at": now}
               for r in rows]
    done, skipped = 0, []
    if dry:
        return len(payload), skipped
    for i in range(0, len(payload), BATCH):
        batch = payload[i:i + BATCH]
        try:
            _merge(sb, batch)
            done += len(batch)
            continue
        except APIError as ex:
            if ex.code != "23505":
                raise
        for r in batch:
            try:
                _merge(sb, [r])
                done += 1
            except APIError as ex:
                if ex.code != "23505":
                    raise
                skipped.append((r["item_key"], "갱신하면 문면이 다른 행과 같아짐(content 중복)"))
    return done, skipped


def retire_keys(sb, keys: list[str], dry: bool) -> int:
    """새 빌드에 없는 live 행을 status='retired' 로 내린다(행은 남김)."""
    if dry or not keys:
        return len(keys)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for i in range(0, len(keys), 100):
        (sb.table("test_items").update({"status": "retired", "updated_at": now}, returning="minimal")
         .eq("status", "live").in_("item_key", keys[i:i + 100]).execute())
    return len(keys)


def delete_keys(sb, keys: list[str], dry: bool) -> int:
    """draft 인 옛 행만 item_key 로 지운다."""
    if dry or not keys:
        return len(keys)
    for i in range(0, len(keys), 100):
        sb.table("test_items").delete(returning="minimal").eq("status", "draft").in_("item_key", keys[i:i + 100]).execute()
    return len(keys)


# ---------------------------------------------------------------- 실행
def main() -> None:
    ap = argparse.ArgumentParser(description="생성 풀을 test_items 에 반영한다(있는 문항은 건너뜀)")
    ap.add_argument("outdir", nargs="?", default=str(HERE / "out" / "gen"))
    ap.add_argument("--status", default="draft", choices=["draft", "live"])
    ap.add_argument("--replace-templates", default="", help="draft 행을 먼저 지울 틀 (공백·쉼표 구분, 끝 * 허용)")
    ap.add_argument("--update-templates", default="", help="이미 있는 행을 제자리 갱신할 틀 (공백·쉼표 구분, 끝 * 허용)")
    ap.add_argument("--dry-run", action="store_true", help="읽기만 — 삭제·업서트를 하지 않는다")
    a = ap.parse_args()

    pools = sorted(Path(a.outdir).glob("*_pool.json"))
    if not pools:
        sys.exit(f"풀이 없다: {a.outdir}/*_pool.json")
    rows: list[dict] = []
    for f in pools:
        rows += json.loads(f.read_text(encoding="utf-8"))
    by_tpl = Counter(r["template_id"] for r in rows)
    print(f"풀 {len(pools)}개 · {len(rows)}행 · 틀 {len(by_tpl)}개 (status={a.status}{' · DRY RUN' if a.dry_run else ''})")

    sb = connect()
    t0 = time.time()

    # replace_templates 칸의 '@틀' = 제자리 갱신 (Run workflow 입력칸 하나로 둘 다 받는다)
    toks = (a.replace_templates or "").replace(",", " ").split()
    a.replace_templates = " ".join(t for t in toks if not t.startswith("@"))
    a.update_templates = " ".join([*(a.update_templates or "").replace(",", " ").split(), *(t[1:] for t in toks if t.startswith("@"))])

    rpats, upats = parse_patterns(a.replace_templates), parse_patterns(a.update_templates)   # 둘 다 먼저 검사 — 하나라도 이상하면 아무것도 안 함

    # ① 교체
    deleted: dict[str, int] = {}
    for pat in rpats:
        deleted[pat] = delete_drafts(sb, pat, a.dry_run)
        print(f"  교체: {pat:<28} draft {deleted[pat]:>5}행 {'삭제 예정' if a.dry_run else '삭제'}")

    # ② 있는 키
    have = existing_keys(sb, list(by_tpl))
    new_rows = [r for r in rows if r["item_key"] not in have]
    print(f"  DB 에 이미 있음 {len(rows) - len(new_rows)}행 · 새로 올릴 것 {len(new_rows)}행")

    # ④ 제자리 갱신 (추가보다 먼저 — 갱신으로 비는 문면에 새 행이 들어갈 수 있게)
    updated, u_skipped, stale_live, stale_draft = 0, [], [], []
    if upats:
        built = {r["item_key"] for r in rows}
        upd = [r for r in rows if r["item_key"] in have and _matches(r["template_id"], upats)]
        n_live = sum(1 for r in upd if have[r["item_key"]] == "live")
        stale = [k for k, st in have.items() if k not in built and _matches(k.rsplit(":", 1)[0], upats)]
        stale_live = sorted(k for k in stale if have[k] == "live")
        stale_draft = sorted(k for k in stale if have[k] == "draft")          # retired 는 그대로 둔다
        updated, u_skipped = update_rows(sb, upd, a.dry_run)
        delete_keys(sb, stale_draft, a.dry_run)
        retire_keys(sb, stale_live, a.dry_run)
        print(f"  제자리 갱신 {'예정 ' if a.dry_run else ''}{updated}행(live {n_live}) · 건너뜀 {len(u_skipped)} · "
              f"빌드에 없는 옛 행: draft {len(stale_draft)} {'삭제 예정' if a.dry_run else '삭제'} / live {len(stale_live)} "
              f"{'retired 예정' if a.dry_run else 'retired 로 내림'}")

    # ③ 업서트
    added, skipped = push_rows(sb, new_rows, a.status, a.dry_run)
    new_by_tpl = Counter(r["template_id"] for r in new_rows)
    skip_by_tpl = Counter(k.rsplit(":", 1)[0] for k, _ in skipped)
    print(f"  {'올릴' if a.dry_run else '올림'} {added}행 · 건너뜀 {len(skipped)}행 · {time.time() - t0:.0f}s")

    # 요약
    lines = ["| 틀 | 풀 | 이미 있음 | 추가 | 건너뜀 |", "|---|---:|---:|---:|---:|"]
    for t in sorted(by_tpl):
        n_new = new_by_tpl.get(t, 0)
        lines.append(f"| {t} | {by_tpl[t]} | {by_tpl[t] - n_new} | {n_new - skip_by_tpl.get(t, 0)} | {skip_by_tpl.get(t, 0)} |")
    head = (f"## push-items · status={a.status}{' · DRY RUN' if a.dry_run else ''}\n\n"
            f"풀 {len(rows)}행 / 이미 있음 {len(rows) - len(new_rows)} / 추가 {added} / 건너뜀 {len(skipped)}"
            + (f" / draft 삭제 {sum(deleted.values())}" if deleted else "")
            + (f" / 제자리 갱신 {updated} (건너뜀 {len(u_skipped)}, 빌드에 없는 옛 행 draft {len(stale_draft)} 삭제 · live {len(stale_live)} retired)" if upats else "")
            + "\n"
            + ("".join(f"\n- 교체 `{p}` → draft {n}행 {'삭제 예정' if a.dry_run else '삭제'}" for p, n in deleted.items()) + "\n" if deleted else ""))
    tail = ""
    if skipped:
        tail = ("\n> ⚠️ 건너뛴 행은 **같은 문면이 다른 item_key 로 이미 있는** 경우다(틀의 파라미터 공간이 바뀌어 색인이 밀림). "
                "Run workflow 에서 `replace_templates` 에 그 틀을 적어 옛 draft 를 정리한 뒤 다시 실행한다.\n\n"
                + "\n".join(f"- `{k}` — {why}" for k, why in skipped[:30])
                + (f"\n- … 외 {len(skipped) - 30}행" if len(skipped) > 30 else "") + "\n")
    if u_skipped or stale_live:
        tail += ("\n> ⚠️ 제자리 갱신에서 확인할 것\n\n"
                 + "".join(f"- 건너뜀 `{k}` — {why}\n" for k, why in u_skipped[:30])
                 + "".join(f"- 새 빌드에 없는 live 행 `{k}` — status='retired' 로 내림(학생 화면에서 빠짐, 행·기록은 남음)\n" for k in stale_live[:30]))
    md = head + "\n" + "\n".join(lines) + "\n" + tail
    summ = os.environ.get("GITHUB_STEP_SUMMARY")
    if summ:
        with open(summ, "a", encoding="utf-8") as fh:
            fh.write(md + "\n")
    else:
        print("\n" + md)
    if u_skipped:
        print(f"::warning::제자리 갱신에서 {len(u_skipped)}행을 건너뛰었다(갱신하면 문면이 다른 행과 같아짐)")
    if stale_live:
        print(f"::notice::새 빌드에 없는 live 행 {len(stale_live)}개를 retired 로 내렸다")
    if skipped:
        print(f"::warning::content 중복으로 {len(skipped)}행을 건너뛰었다 — replace_templates 로 정리 필요 "
              f"({', '.join(sorted(skip_by_tpl))})")
    if skipped or u_skipped:
        sys.exit(1)


if __name__ == "__main__":
    main()
