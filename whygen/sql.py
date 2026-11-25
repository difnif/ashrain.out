# 개념 카드 「💡 왜 그럴까?」 단락 → DB(concepts.blocks) SQL (whygen/sql.py)
#   python3 whygen/sql.py check-data              자료(w_<학기>.py)만 검사 — 줄 수 · 굵게/칠하기 짝 · ASCII 빼기 · 중1 · 중2 의 √ · 길이
#   python3 whygen/sql.py apply <학기|all>         넣기 — 개념마다 「꼭 조심할 것」(warning) 단락 바로 앞에(없으면 「바로 확인」 앞, 그것도 없으면 맨 끝)
#                                                이미 있으면 줄만 새로(같은 단락 id 그대로) · 몇 번 돌려도 같다 · 넣은 개념마다 빼기 검산(md5)
#   python3 whygen/sql.py rollback <학기|all>      빼기 — 이 생성기가 넣은 단락(src "why")만 지운다
#   python3 whygen/sql.py check <학기|all>         확인 — 자료의 개념마다 단락이 꼭 하나 · 자리(warning 앞) · 줄이 자료와 같은지(맞으면 total 한 줄만)
# 단락 = { id: b<지금 가장 큰 번호 + 1>, icon 💡, type text, label 「왜 그럴까?」, src "why", lines, style { size md · tone slate · width full }, figure null }
#   개념에 「왜 그럴까?」 단락이 처음부터 있으면(src 없음) 넣지 않고 건너뛴다(겹치지 않게).
#   — h1-1-14(「왜 더하고, 왜 곱할까?」) · m2-2-12(b2 · b3 안의 「왜 더할까? · 왜 곱할까?」)는 2026-11-25 먼저 따로 넣었다 — 이 생성기는 건드리지 않는다.
# 글은 개념 본문(Rich — **굵게** · ==칠하기== · [[tone:글]])과 같은 문법. 수식은 유니코드(x² · −3 · 2/3), 중1 · 중2 는 √ 를 쓰지 않는다.
# 현황(2026-11-26): 중1 ~ 고3 개념 259개 중 256개에 넣었다(빠진 셋 = h1-1-14 · m2-2-12 따로 넣음, m3-1-19 원래 단락 있음).
#   자료 파일은 중1-1(w_m1_1.py)만 저장소에 있고, 나머지 학기 글은 DB(concepts.blocks 의 src "why" 단락)에만 있다 —
#   고칠 때는 관리자 개념 편집(AdminConcepts)에서 그 단락을 고치거나, apply 와 같은 DO 블록을 MCP 로 돌린다(줄만 새로 바뀐다).
#   check <학기|all> 은 자료 없이도 모든 개념의 자리 · 꼴 · 글 규칙을 본다.
import importlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
UNITS = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"]
LABEL = "왜 그럴까?"
DONE_ELSEWHERE = {"h1-1-14", "m2-2-12"}
BLOCK = {"icon": {"kind": "emoji", "value": "💡"}, "type": "text", "label": LABEL, "src": "why",
         "style": {"size": "md", "tone": "slate", "width": "full"}, "figure": None}
# 이 생성기가 넣은 단락의 표 — src: "why"(화면은 모른 척한다). 같은 이름(「왜 그럴까?」)의 단락을 처음부터 가진 개념(m3-1-19 b3)이 있어
#   고르기 · 빼기는 반드시 이 표로 한다(이름으로 고르면 원래 단락까지 건드린다 — 2026-11-25 m3-1-19 를 백업에서 되살렸다).
MINE = "z.b->>'src' = 'why'"


def load(u):
    try:
        mod = importlib.import_module("w_" + u.replace("-", "_"))
    except ModuleNotFoundError:
        return {}
    return mod.WHY


def problems(u, why):
    out = []
    for cid, lines in why.items():
        tag = f"{cid}"
        if not re.fullmatch(rf"{u}-\d{{2}}", cid):
            out.append(f"{tag}: 학기 {u} 의 개념 id 가 아님")
        if cid in DONE_ELSEWHERE:
            out.append(f"{tag}: 이미 따로 넣은 개념")
        if not (2 <= len(lines) <= 4):
            out.append(f"{tag}: 줄 {len(lines)}개(2 ~ 4)")
        if not lines or not lines[0].startswith("**왜"):
            out.append(f"{tag}: 첫 줄은 「**왜 …?**」로 시작")
        for i, s in enumerate(lines):
            t = f"{tag} 줄{i + 1}"
            if not isinstance(s, str) or not s.strip():
                out.append(f"{t}: 빈 줄"); continue
            if s.count("**") % 2: out.append(f"{t}: ** 짝이 안 맞음")
            if s.count("==") % 2: out.append(f"{t}: == 짝이 안 맞음")
            if re.search(r"(^|[\s(=,])-(\d|[a-zA-Z])", s) or " - " in s: out.append(f"{t}: ASCII 빼기(−)")
            if re.search(r"\d\s*\*\s*\d", s.replace("**", "")): out.append(f"{t}: * 곱하기(×)")
            if u[:2] in ("m1", "m2") and "√" in s: out.append(f"{t}: 중1 · 중2 에 √")
            if len(s) > 260: out.append(f"{t}: 너무 김({len(s)}자)")
            if "[[" in s and not re.search(r"\[\[(teal|amber|coral|slate|blue|green|violet|rose):[^\]]+\]\]", s):
                out.append(f"{t}: [[ ]] 는 [[tone:글]] 만")
    return out


def q(s):
    return "'" + s.replace("'", "''") + "'"


def lit(lines):
    return "array[" + ", ".join(q(x) for x in lines) + "]"


HEAD = """do $$
declare r record; oi int; pos int; nid text; blk jsonb; ln jsonb; m0 text; m1 text; added int := 0; renewed int := 0;
begin
for r in select * from (values
"""


def tail():
    base = json.dumps(BLOCK, ensure_ascii=False)
    return f""") v(cid, lines) loop
  if not exists (select 1 from concepts where id = r.cid) then raise exception '개념 없음: %', r.cid; end if;
  if r.cid in ('h1-1-14', 'm2-2-12') then raise exception '이미 따로 넣은 개념: %', r.cid; end if;
  ln := to_jsonb(r.lines);
  oi := null;
  select z.ord - 1 into oi from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord) where c.id = r.cid and {MINE};
  if oi is null and exists (select 1 from concepts c, jsonb_array_elements(c.blocks) z(b) where c.id = r.cid and z.b->>'label' = {q(LABEL)}) then
    raise notice '% — 원래 「{LABEL}」 단락이 있어 건너뜀', r.cid; continue;
  end if;
  if oi is not null then
    update concepts set blocks = jsonb_set(blocks, array[oi::text, 'lines'], ln), updated_at = now() where id = r.cid and blocks->oi->'lines' is distinct from ln;
    if found then renewed := renewed + 1; end if;
    continue;
  end if;
  select coalesce(
    (select min(z.ord) - 1 from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord) where c.id = r.cid and z.b->>'type' = 'warning'),
    (select min(z.ord) - 1 from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord) where c.id = r.cid and z.b->>'type' = 'check'),
    (select jsonb_array_length(blocks) from concepts where id = r.cid)) into pos;
  select 'b' || (coalesce(max((substring(z.b->>'id' from '^b(\\d+)$'))::int), 0) + 1) into nid from concepts c, jsonb_array_elements(c.blocks) z(b) where c.id = r.cid;
  blk := jsonb_build_object('id', nid, 'lines', ln) || {q(base)}::jsonb;
  select md5(blocks::text) into m0 from concepts where id = r.cid;
  update concepts set blocks = (select jsonb_agg(e order by o) from (select z.b as e, z.ord::numeric as o from jsonb_array_elements(blocks) with ordinality z(b, ord)
    union all select blk, pos + 0.5) s), updated_at = now() where id = r.cid;
  select md5(({back_expr()})::text) into m1 from concepts c where c.id = r.cid;
  if m1 is distinct from m0 then raise exception '빼기 검산 어긋남: %', r.cid; end if;
  added := added + 1;
end loop;
raise notice '「{LABEL}」 — 넣음 %, 줄 새로 %', added, renewed;
end $$;
"""


def apply_sql(u, why):
    rows = ",\n".join(f"({q(cid)}, {lit(lines)})" for cid, lines in sorted(why.items()))
    return f"-- 「💡 {LABEL}」 단락 넣기 — {u} {len(why)}개념 (whygen/sql.py apply)\n" + HEAD + rows + "\n" + tail()


def back_expr():
    return (f"select coalesce(jsonb_agg(z.b order by z.ord), '[]'::jsonb) from jsonb_array_elements(c.blocks) with ordinality z(b, ord) "
            f"where not coalesce({MINE}, false)")


def scope(arg):
    return UNITS if arg in (None, "all") else [arg]


def rollback_sql(units):
    pat = " or ".join(f"c.unit_id = {q(u)}" for u in units)
    return f"""-- 「💡 {LABEL}」 단락 빼기 — {', '.join(units)} (whygen/sql.py rollback)
update concepts c set blocks = ({back_expr()}), updated_at = now()
where ({pat}) and exists (select 1 from jsonb_array_elements(c.blocks) z(b) where {MINE});
"""


def check_sql(units, data):
    pat = ", ".join(q(u) for u in units)
    have = [(cid, lines) for u in units for cid, lines in sorted(data[u].items())]
    vals = ",\n    ".join(f"({q(cid)}, {q(json.dumps(lines, ensure_ascii=False))}::jsonb)" for cid, lines in have) or "(null, null)"
    return f"""-- 「💡 {LABEL}」 단락 확인 (whygen/sql.py check) — 문제가 있는 것만 나온다(total 한 줄만 = 모두 맞음)
--   모든 개념(h1-1-14 · m2-2-12 빼고)에 꼭 하나 · warning(없으면 check) 바로 앞 · text 단락 b<n> · 줄 2 ~ 4 · 첫 줄 「**왜」 · 굵게/칠하기 짝 · ASCII 빼기 없음 · 중1 · 중2 √ 없음 · 줄 260자 안
--   자료 파일(w_<학기>.py)이 있는 학기는 줄이 자료와 같은지도
with v(cid, lines) as (values
    {vals}
), got as (
  select c.id as cid, c.unit_id as u, z.ord, z.b,
         (select min(w.ord) from jsonb_array_elements(c.blocks) with ordinality w(b, ord) where w.b->>'type' in ('warning', 'check')) as stop
  from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord)
  where c.unit_id in ({pat}) and {MINE}
), want as (select c.id as cid from concepts c where c.unit_id in ({pat}) and c.id not in ('h1-1-14', 'm2-2-12')
    and not exists (select 1 from jsonb_array_elements(c.blocks) z(b) where z.b->>'label' = {q(LABEL)} and z.b->>'src' is null)),
ln as (select got.cid, got.u, l.i, l.s from got, jsonb_array_elements_text(got.b->'lines') with ordinality l(s, i))
select 'missing' as problem, want.cid, null::text as detail from want where not exists (select 1 from got where got.cid = want.cid)
union all select 'twice', cid, count(*)::text from got group by cid having count(*) > 1
union all select 'place', cid, ord || ' / ' || stop from got where stop is not null and ord <> stop - 1
union all select 'shape', cid, b->>'id' from got where b->>'type' <> 'text' or b->>'id' !~ '^b\\d+$'
union all select 'count', cid, jsonb_array_length(b->'lines')::text from got where jsonb_array_length(b->'lines') not between 2 and 4
union all select 'first', cid, left(b->'lines'->>0, 20) from got where b->'lines'->>0 not like '**왜%'
union all select 'bold', cid, i::text from ln where ((length(s) - length(replace(s, '**', ''))) / 2) % 2 = 1
union all select 'hl', cid, i::text from ln where ((length(s) - length(replace(s, '==', ''))) / 2) % 2 = 1
union all select 'minus', cid, i::text from ln where s ~ '(^|[[:space:](=,])-[0-9A-Za-z]' or s like '% - %'
union all select 'root', cid, i::text from ln where u ~ '^m[12]-' and s like '%√%'
union all select 'long', cid, i || ' · ' || length(s) from ln where length(s) > 260
union all select 'lines', got.cid, null from got join v using (cid) where got.b->'lines' is distinct from v.lines
union all select 'total', null, count(*)::text from got
order by 1, 2;
"""


if __name__ == "__main__":
    what = (sys.argv[1:] or ["check-data"])[0]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    units = scope(arg)
    data = {u: load(u) for u in units}
    bad = [p for u in units for p in problems(u, data[u])]
    if what == "check-data":
        n = sum(len(d) for d in data.values())
        for u in units:
            if data[u]: print(f"{u}: {len(data[u])}개념")
        print(f"합계 {n}개념 · 문제 {len(bad)}")
        for p in bad: print("  ", p)
        sys.exit(1 if bad else 0)
    if bad:
        sys.exit("자료에 문제가 있다 — python3 whygen/sql.py check-data")
    if what == "apply":
        sys.stdout.write("\n".join(apply_sql(u, data[u]) for u in units if data[u]))
    elif what == "rollback":
        sys.stdout.write(rollback_sql(units))
    elif what == "check":
        sys.stdout.write(check_sql(units, data))
