# 개념 카드 「▶ 움직이는 예시」 → DB(concepts.blocks)에 [[av:<예시 id>]] 글줄을 넣는 SQL (sql.py)
#   python3 sql.py apply      넣기 — places.json 의 자리마다(이미 있으면 건너뜀 · 몇 번 돌려도 같다)
#   python3 sql.py rollback   빼기 — 학기 파일 예시의 [[av:…]] 줄을 모두 지운다(정의 · 주의 단락에 이 줄 때문에 새로 생긴 lines 는 통째로)
#   python3 sql.py check      확인 — 자리마다 그 단락 · 그 줄 뒤에 꼭 하나 있는지 · 남는 줄은 없는지(맞으면 total 한 줄만 나온다)
#   python3 sql.py migrate    옛 표식 [[fig:av-<id>]](2026-11-25 처음 넣은 꼴)을 [[av:<id>]] 로 바꾼다 — 한 번 돌렸다(256자리)
# 카드는 components/ConceptAv.jsx — ConceptViewer 가 글줄 「[[av:…]]」 자리에 놓고, 예시는 public/concept-av/<학기>.json 에서 받는다(lib/conceptAv.js avUnitOf).
#   이 줄을 모르는 옛 앱(머지 전)은 avMarker 가 빈 목록을 돌려 아무것도 그리지 않는다 — 먼저 넣어 두어도 안전하다.
# 자리 = { cid, bid, after } — 글 단락(text)은 lines[after] 바로 뒤(바로 뒤가 [[fig:…]] 씬 줄이면 그 씬 다음),
#   after = −1 이면 단락 lines 끝에 덧붙인다(정의 · 주의 단락은 lines 가 없으면 만든다 — ConceptViewer 가 그 자리에 그린다).
# 넣기는 한 덩어리(DO 블록 — 하나라도 어긋나면 전부 취소)로 돌고, 넣은 개념마다 「빼기를 하면 넣기 전과 똑같아지는지」(md5)를 그 자리에서 검산한다.
# 경우의 수와 확률(m2-2-12 ~ 14)은 코드 안 예시(lib/conceptAv.js CONCEPT_AV) 몫 — 넣지 않는다.
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLACES = os.path.join(HERE, "places.json")
SKIP = ("m2-2-12", "m2-2-13", "m2-2-14")

# 학기 파일 예시의 글줄 — [[av:<개념 id>-<번호>]](코드 안 예시 [[av:c12-sum]] 같은 줄은 건드리지 않는다)
MK = r"^\[\[av:[emh][1-6]-[1-3]-[0-9]{2}-[0-9]+\]\]$"
# 빼기 — 한 개념의 blocks(c.blocks)에서 그 줄을 지운 것
BACK = """(select jsonb_agg(
    case
      when jsonb_typeof(b->'lines') = 'array' and exists (select 1 from jsonb_array_elements_text(b->'lines') v where v ~ '@MK@') then
        case
          when b->>'type' <> 'text' and not exists (select 1 from jsonb_array_elements_text(b->'lines') v where v !~ '@MK@') then b - 'lines'
          else jsonb_set(b, '{lines}', (select coalesce(jsonb_agg(v order by o), '[]'::jsonb) from jsonb_array_elements(b->'lines') with ordinality y(v, o)
                                         where not (jsonb_typeof(v) = 'string' and (v #>> '{}') ~ '@MK@')))
        end
      else b
    end order by ord)
  from jsonb_array_elements(c.blocks) with ordinality z(b, ord))""".replace("@MK@", MK)


def rows():
    P = json.load(open(PLACES, encoding="utf-8"))
    out = []
    for iid, p in sorted(P.items()):
        assert p["cid"] not in SKIP, iid
        assert re.fullmatch(r"[emh][1-6]-[1-3]-\d{2}-\d+", iid) and iid.startswith(p["cid"] + "-"), iid
        assert re.fullmatch(r"b\d+", p["bid"]) and isinstance(p["after"], int) and p["after"] >= -1, iid
        out.append((p["cid"], p["bid"], p["after"], iid))
    return out


def values(rs):
    return ",\n    ".join(f"('{c}', '{b}', {a}, '{i}')" for c, b, a, i in rs)


def apply_sql(rs):
    return f"""-- 움직이는 예시 글줄 넣기 — {len(rs)}자리 (cvgen/sql.py apply)
do $$
declare
  r record; pos int; blk jsonb; lns jsonb; k int; n int; mk text; m0 text; m1 text;
  added int := 0; skipped int := 0;
begin
  for r in select * from (values
    {values(rs)}
  ) v(cid, bid, aft, iid) order by cid, iid loop
    if r.cid in ({", ".join(f"'{s}'" for s in SKIP)}) then raise exception '% — 경우의 수와 확률(m2-2-12 ~ 14)은 다른 방 몫', r.cid; end if;
    mk := '[[av:' || r.iid || ']]';
    pos := null; blk := null;
    select z.ord - 1, z.b into pos, blk
      from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord)
      where c.id = r.cid and z.b->>'id' = r.bid;
    if pos is null then raise exception '단락 없음: % %', r.cid, r.bid; end if;
    if (select strpos(blocks::text, mk) from concepts where id = r.cid) > 0 then skipped := skipped + 1; continue; end if;
    lns := coalesce(blk->'lines', '[]'::jsonb);
    if jsonb_typeof(lns) <> 'array' then raise exception 'lines 가 배열이 아님: % %', r.cid, r.bid; end if;
    n := jsonb_array_length(lns);
    if r.aft < 0 then
      k := n - 1;
    else
      if r.aft >= n then raise exception '자리 넘침: % % after % / 줄 %', r.cid, r.bid, r.aft, n; end if;
      k := r.aft;
      while k + 1 < n and (lns->>(k + 1)) like '[[fig:%' loop k := k + 1; end loop;
    end if;
    select coalesce(jsonb_agg(e order by o), '[]'::jsonb) into lns from (
      select x.e, x.o::numeric as o from jsonb_array_elements(lns) with ordinality x(e, o)
      union all select to_jsonb(mk), k + 1.5) s;
    select md5(blocks::text) into m0 from concepts where id = r.cid;
    update concepts set blocks = jsonb_set(blocks, array[pos::text, 'lines'], lns, true), updated_at = now() where id = r.cid;
    select md5({BACK.replace(chr(10), chr(10) + "    ")}::text) into m1 from concepts c where c.id = r.cid;
    if m1 is distinct from m0 then raise exception '빼기 검산 어긋남: %', r.cid; end if;
    added := added + 1;
  end loop;
  raise notice '움직이는 예시 글줄 — 넣음 %, 이미 있음 %', added, skipped;
end $$;
"""


def rollback_sql():
    return f"""-- 움직이는 예시 글줄 빼기 — 학기 파일 예시의 [[av:…]] 줄 모두 (cvgen/sql.py rollback)
update concepts c set blocks = {BACK}, updated_at = now()
where strpos(c.blocks::text, '[[av:') > 0;
"""


def migrate_sql():
    return """-- 옛 표식 [[fig:av-<id>]] → [[av:<id>]] (cvgen/sql.py migrate) — 2026-11-25 한 번 돌림(256자리)
update concepts set blocks = replace(blocks::text, '[[fig:av-', '[[av:')::jsonb, updated_at = now()
where strpos(blocks::text, '[[fig:av-') > 0;
"""


def check_sql(rs):
    return f"""-- 움직이는 예시 글줄 확인 (cvgen/sql.py check) — 문제가 있는 자리만 나온다(total 한 줄만 = 모두 맞음)
with v(cid, bid, aft, iid) as (values
    {values(rs)}
), got as (
  select c.id as cid, z.b->>'id' as bid, z.b->>'type' as type, y.o - 1 as idx, y.v #>> '{{}}' as line,
         lag(y.v #>> '{{}}') over (partition by c.id, z.ord order by y.o) as prev,
         jsonb_array_length(z.b->'lines') as n
  from concepts c, jsonb_array_elements(c.blocks) with ordinality z(b, ord), jsonb_array_elements(z.b->'lines') with ordinality y(v, o)
  where jsonb_typeof(z.b->'lines') = 'array'
), av as (select * from got where line ~ '{MK}' or line like '[[fig:av-%')
select 'missing' as problem, v.cid, v.iid, null::text as detail from v
  where not exists (select 1 from av where av.cid = v.cid and av.bid = v.bid and av.line = '[[av:' || v.iid || ']]')
union all
select 'extra', av.cid, av.line, av.bid from av
  where not exists (select 1 from v where av.cid = v.cid and av.bid = v.bid and av.line = '[[av:' || v.iid || ']]')
union all
select 'twice', av.cid, av.line, count(*)::text from av group by av.cid, av.line having count(*) > 1
union all
select 'place', av.cid, v.iid, av.type || ' idx ' || av.idx || ' / ' || av.n || ' prev ' || coalesce(left(av.prev, 24), '-') from av join v
  on av.cid = v.cid and av.bid = v.bid and av.line = '[[av:' || v.iid || ']]'
  where (v.aft < 0 and av.idx <> av.n - 1) or (v.aft >= 0 and av.idx <= v.aft)
union all
select 'skip-room', av.cid, av.line, null from av where av.cid in ({", ".join(f"'{s}'" for s in SKIP)})
union all
select 'total', null, count(*)::text, count(distinct cid)::text from av
order by 1, 2;
"""


if __name__ == "__main__":
    what = (sys.argv[1:] or ["apply"])[0]
    rs = rows()
    sys.stdout.write({"apply": lambda: apply_sql(rs), "rollback": rollback_sql, "check": lambda: check_sql(rs), "migrate": migrate_sql}[what]())
