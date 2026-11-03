// ashrain.out — 문항 분포 (관리자, #/admin/items 의 「분포」 보기 · 2026-11-04)
// 산과(서술형) 문항이 어느 단원·개념에 몰려 있는지 본다. 기본은 test_type = 'sangwa'.
//   · 단원별: 학기 → 대단원(src/data/chapters.js) → 개념. 문항이 있는 대단원은 개념을 모두 펼쳐 0인 개념도 보인다(빈 곳 찾기).
//   · 개념별: 유형(틀) 수가 많은 개념부터 한 줄씩.
// 막대는 유형(틀) 수 기준 — 문항 수는 틀마다 파라미터 공간 크기에 따라 달라서 "얼마나 자주 서술형으로 나오나"를 재기엔 틀 수가 낫다.
// 개념을 누르면 그 개념·종류로 걸러진 문항 목록(문항 보기)으로 간다.
import { useEffect, useMemo, useState } from "react";
import { supabase } from "../supabaseClient";
import { chapterOf } from "../data/chapters";

const UNIT_ORDER = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"];
const UNIT_TITLE = {
  "m1-1": "중1 1학기", "m1-2": "중1 2학기", "m2-1": "중2 1학기", "m2-2": "중2 2학기", "m3-1": "중3 1학기", "m3-2": "중3 2학기",
  "h1-1": "공통수학1", "h1-2": "공통수학2", "h2-1": "대수", "h2-2": "미적분1", "h3-1": "미적분2", "h3-2": "확률과 통계", "h3-3": "기하",
};
const TYPES = [["sangwa", "산과(서술형)"], ["concept_set", "개념 묶음"], ["unit", "단원"], ["calc", "연산"], ["mock", "모의고사"]];
const PAGE = 1000;

const empty = () => ({ n: 0, live: 0, draft: 0, tpls: new Set() });
function add(acc, r) {
  acc.n += 1;
  if (r.status === "live") acc.live += 1; else if (r.status === "draft") acc.draft += 1;
  if (r.template_id) acc.tpls.add(r.template_id);
}

export default function AdminSangwaDist({ concepts, onOpen, onBack }) {
  const [tt, setTt] = useState("sangwa");
  const [mode, setMode] = useState("unit");          // "unit" | "concept"
  const [rows, setRows] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    let alive = true;
    setRows(null); setErr("");
    (async () => {
      const out = [];
      for (let from = 0; ; from += PAGE) {
        const { data, error } = await supabase.from("test_items")
          .select("template_id,unit_id,concept_ids,status")
          .eq("test_type", tt).order("template_id").order("param_index").range(from, from + PAGE - 1);
        if (error) { if (alive) setErr("불러오지 못했습니다: " + error.message); return; }
        out.push(...(data || []));
        if (!data || data.length < PAGE || out.length >= 20000) break;
      }
      if (alive) setRows(out);
    })();
    return () => { alive = false; };
  }, [tt]);

  const cById = useMemo(() => Object.fromEntries((concepts || []).map((c) => [c.id, c])), [concepts]);

  // 개념별 집계 — 문항의 첫 개념(주 개념)으로 센다
  const byConcept = useMemo(() => {
    const m = {};
    for (const r of rows || []) {
      const cid = (r.concept_ids || [])[0];
      if (!cid) continue;
      add((m[cid] = m[cid] || empty()), r);
    }
    return m;
  }, [rows]);

  const total = useMemo(() => {
    const t = empty();
    for (const r of rows || []) add(t, r);
    return { ...t, nC: Object.keys(byConcept).length };
  }, [rows, byConcept]);

  // 단원별: 학기 → 대단원 → 개념 (문항이 있는 학기만)
  const tree = useMemo(() => {
    const units = [...new Set(Object.keys(byConcept).map((cid) => chapterOf(cid).unit || cById[cid]?.unit_id).filter(Boolean))]
      .sort((a, b) => UNIT_ORDER.indexOf(a) - UNIT_ORDER.indexOf(b));
    return units.map((u) => {
      const cs = (concepts || []).filter((c) => c.unit_id === u).sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0));
      const chMap = new Map();
      for (const c of cs) {
        const ch = chapterOf(c.id);
        if (!chMap.has(ch.idx)) chMap.set(ch.idx, { name: ch.name, idx: ch.idx, concepts: [], acc: empty() });
        const g = chMap.get(ch.idx);
        const a = byConcept[c.id];
        g.concepts.push({ c, a });
        if (a) { g.acc.n += a.n; g.acc.live += a.live; g.acc.draft += a.draft; a.tpls.forEach((t) => g.acc.tpls.add(t)); }
      }
      const chapters = [...chMap.values()].sort((a, b) => a.idx - b.idx);
      const acc = empty();
      chapters.forEach((g) => { acc.n += g.acc.n; acc.live += g.acc.live; acc.draft += g.acc.draft; g.acc.tpls.forEach((t) => acc.tpls.add(t)); });
      return { u, chapters, acc };
    });
  }, [byConcept, concepts, cById]);

  const ranked = useMemo(() => Object.entries(byConcept)
    .map(([cid, a]) => ({ cid, a, c: cById[cid] }))
    .sort((x, y) => y.a.tpls.size - x.a.tpls.size || y.a.n - x.a.n
      || UNIT_ORDER.indexOf(x.c?.unit_id) - UNIT_ORDER.indexOf(y.c?.unit_id) || (x.c?.sort_order ?? 0) - (y.c?.sort_order ?? 0)),
  [byConcept, cById]);

  const maxT = Math.max(1, ...Object.values(byConcept).map((a) => a.tpls.size));
  const maxChT = Math.max(1, ...tree.flatMap((u) => u.chapters.map((g) => g.acc.tpls.size)));

  const nums = (a) => (
    <span className="sgd-n">유형 <b>{a.tpls.size}</b> · 문항 {a.n}{a.draft ? <span className="sgd-dr"> (draft {a.draft})</span> : null}</span>
  );
  const bar = (v, max) => <span className="sgd-bar"><i style={{ width: `${Math.round((v / max) * 100)}%` }} /></span>;
  const open = (cid) => { const c = cById[cid]; onOpen?.(cid, c?.unit_id || chapterOf(cid).unit, tt); };

  return (
    <div className="irv-wrap">
      <style>{CSS}</style>
      <div className="irv-head">
        <h2>문항 분포 <span className="irv-sub">{rows ? `${TYPES.find((t) => t[0] === tt)?.[1] || tt} · 문항 ${total.n} · 유형 ${total.tpls.size} · 개념 ${total.nC}` : "세는 중…"}</span></h2>
        <div className="irv-bulk">
          <button className="irv-chip" onClick={onBack}>문항</button>
          <button className="irv-chip on">분포</button>
        </div>
      </div>
      <div className="irv-filters">
        <select value={tt} onChange={(e) => setTt(e.target.value)}>
          {TYPES.map(([k, l]) => <option key={k} value={k}>{l}</option>)}
        </select>
        <button className={"irv-chip" + (mode === "unit" ? " on" : "")} onClick={() => setMode("unit")}>단원별</button>
        <button className={"irv-chip" + (mode === "concept" ? " on" : "")} onClick={() => setMode("concept")}>개념별</button>
        {rows && total.draft > 0 && <span className="irv-msg">draft {total.draft}건은 학생 화면에 아직 안 보입니다</span>}
      </div>
      {err && <p className="irv-msg">{err}</p>}
      {rows === null && !err && <p className="irv-empty">세는 중…</p>}
      {rows && !rows.length && <p className="irv-empty">이 종류의 문항이 아직 없습니다.</p>}

      {rows && rows.length > 0 && mode === "unit" && tree.map(({ u, chapters, acc }) => (
        <section key={u} className="sgd-unit">
          <div className="irv-cgroup">
            <span className="irv-cg-title">{UNIT_TITLE[u] || u}</span>
            <span className="irv-cg-n">{nums(acc)}</span>
          </div>
          {chapters.map((g) => (
            <div key={g.idx} className={"sgd-ch" + (g.acc.n ? "" : " zero")}>
              <div className="sgd-row sgd-chrow">
                <span className="sgd-name">{g.name}</span>
                {bar(g.acc.tpls.size, maxChT)}
                {nums(g.acc)}
              </div>
              {g.acc.n > 0 && g.concepts.map(({ c, a }) => (
                <button key={c.id} className={"sgd-row sgd-crow" + (a ? "" : " zero")} disabled={!a} onClick={() => open(c.id)}>
                  <span className="sgd-name"><span className="sgd-no">{c.id.split("-").pop()}</span>{c.title}</span>
                  {bar(a ? a.tpls.size : 0, maxT)}
                  {a ? nums(a) : <span className="sgd-n">—</span>}
                </button>
              ))}
            </div>
          ))}
        </section>
      ))}

      {rows && rows.length > 0 && mode === "concept" && (
        <div className="sgd-list">
          {ranked.map(({ cid, a, c }, i) => (
            <button key={cid} className="sgd-row sgd-crow" onClick={() => open(cid)}>
              <span className="sgd-name">
                <span className="sgd-rank">{i + 1}</span>
                <span className="sgd-where">{UNIT_TITLE[c?.unit_id] || c?.unit_id} · {chapterOf(cid).name}</span>
                {c?.title || cid}
              </span>
              {bar(a.tpls.size, maxT)}
              {nums(a)}
            </button>
          ))}
        </div>
      )}
      {rows && rows.length > 0 && <p className="sgd-foot">막대는 유형(틀) 수 기준이에요. 개념을 누르면 그 개념의 문항 목록으로 갑니다.</p>}
    </div>
  );
}

const CSS = `
.sgd-unit{margin-bottom:8px}
.sgd-ch{margin:4px 0 10px}
.sgd-row{display:grid;grid-template-columns:minmax(0,1fr) 120px 210px;align-items:center;gap:10px;width:100%;text-align:left;border:none;background:none;padding:6px 4px;font:inherit;color:inherit}
.sgd-chrow{font-weight:800;font-size:14.5px;border-bottom:1px solid #e2e8f0}
.sgd-crow{font-size:13.5px;padding-left:14px;cursor:pointer;border-radius:8px}
.sgd-crow:hover:not(:disabled){background:#f1f5f9}
.sgd-crow:disabled{cursor:default}
.sgd-row.zero,.sgd-ch.zero .sgd-chrow{color:#94a3b8}
.sgd-name{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sgd-no{display:inline-block;min-width:22px;color:#64748b;font-variant-numeric:tabular-nums}
.sgd-rank{display:inline-block;min-width:22px;color:#0f766e;font-weight:800}
.sgd-where{font-size:11.5px;color:#64748b;margin-right:6px}
.sgd-bar{height:8px;border-radius:999px;background:#f1f5f9;overflow:hidden}
.sgd-bar i{display:block;height:100%;background:#0f766e;border-radius:999px}
.sgd-n{font-size:12.5px;color:#475569;white-space:nowrap;font-variant-numeric:tabular-nums;text-align:right}
.sgd-dr{color:#b45309}
.sgd-list{margin-top:6px}
.sgd-foot{font-size:12px;color:#94a3b8;margin-top:14px}
@media (max-width:560px){.sgd-row{grid-template-columns:minmax(0,1fr) 64px}.sgd-row .sgd-n{grid-column:1 / -1;padding-left:22px;text-align:left}}
`;
