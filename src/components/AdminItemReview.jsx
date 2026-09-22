// ashrain.out — 문항 전수 검토 (AdminItemReview v1.1, 관리자 전용, #/admin/items)
// 목적: 생성·등록된 test_items 전체를 필터로 훑고, 펼쳐 보고, live/draft 전환·삭제·수정필요 표시.
// 삭제는 item_rejects에 사유(manual)로 기록 후 제거 — E-10 "폐기 이유는 남긴다".
// v1.1 (09-21): ① 목록은 가벼운 열만 받고(해설·그림은 펼칠 때) 건수는 따로 센다 — 예전엔 select * + 정확한 건수 + 정렬을
//   한 문장으로 해서 138k 행에서 DB 의 8초 제한에 걸렸다("canceling statement due to statement timeout").
//   ② 문항·보기·정답·해설·그림을 학생이 보는 그대로(MathText·도형·괄호 규칙) 보여 준다. ③ 일괄 전환은 1,000건씩 나눠 한다.
// v1.2 (09-22): 「틀별 보기」 — 검토는 틀 단위로 한다(같은 틀은 숫자만 다르다). 틀마다 개념·draft/live 수·표본 발문·이 틀이 재는 것을
//   한 줄로 보여 주고 [문항 보기]·[draft → live]·[live → draft] 를 바로 누른다. 집계는 supabase/2026-09_template_stats.sql 의
//   admin_template_stats() (없으면 안내만). 틀 필터도 이 목록에서 채운다(item_templates 표에는 시드 틀이 없다).

import { useEffect, useMemo, useState } from "react";
import { supabase } from "../supabaseClient";
import ItemQuestion from "./ItemQuestion";
import MathText, { mathHtml } from "./MathText";
import { figureHtml } from "./ItemFigure";
import { solutionLevels } from "../lib/items";
import { bustStudyCache } from "../lib/studyCache";

const PAGE = 50;
const UNIT_ORDER = ["m1-1", "m1-2", "m2-1", "m2-2", "m3-1", "m3-2", "h1-1", "h1-2", "h2-1", "h2-2", "h3-1", "h3-2", "h3-3"];
const unitRank = (u) => { const i = UNIT_ORDER.indexOf(u); return i < 0 ? 99 : i; };
const tplNo = (id) => { const m = /-t(\d+)$/.exec(id || ""); return m ? Number(m[1]) : 0; };
// 목록에 필요한 열만 — solution·figure(jsonb, 행당 수 KB)는 펼칠 때 따로 받는다
const LIST_COLS = "id,test_type,unit_id,concept_ids,qtype,difficulty,question,choices,answer,answer_alt,tags,source,status,gen_meta,created_at,template_id,param_index,content_key,struct_key";
const BULK = 1000;
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

/** 해설(levels 또는 outline/steps/check) → HTML — ItemView 와 같은 마크업(.isol .lv) */
function solutionHtml(item) {
  const levels = solutionLevels(item);
  const html = levels.map((lv, i) => {
    const l = lv && typeof lv === "object" ? lv : {};
    const steps = Array.isArray(l.steps) ? l.steps.filter((x) => x != null && String(x).trim() !== "") : [];
    const text = steps.length ? "" : String(l.text ?? "").trim();
    const fig = figureHtml(l.figure, 320);
    const title = l.title || ["방침", "전개", "확인"][i] || `${i + 1}단계`;
    if (!fig && !steps.length && !text) return "";
    return `<div class="lv"><div class="lv-title">${esc(title)}</div>${fig ? `<div class="fig-stage">${fig}</div>` : ""}`
      + (steps.length ? `<ol>${steps.map((x) => `<li>${mathHtml(x)}</li>`).join("")}</ol>` : `<p>${mathHtml(text)}</p>`) + `</div>`;
  }).join("");
  const rub = item?.solution?.rubric;
  const items = Array.isArray(rub?.items) ? rub.items : [];
  if (!items.length) return html;
  const rows = items.map((r) => `<tr><td>${esc(r.element)}<span class="irv-pt">${esc(r.points)}점</span></td><td>${mathHtml(r.criterion)}${r.partial ? `<span class="irv-partial">${mathHtml(r.partial)}</span>` : ""}</td></tr>`).join("");
  const pits = Array.isArray(rub.checks) ? rub.checks.map((c) => `<li>${mathHtml(c.text)}${c.effect ? ` <span class="irv-eff">(${esc(c.effect)})</span>` : ""}</li>`).join("") : "";
  return html + `<div class="lv"><div class="lv-title">채점기준${rub.total != null ? ` · ${esc(rub.total)}점` : ""}</div><table class="irv-rubric"><tbody>${rows}</tbody></table>${pits ? `<ul class="irv-pits">${pits}</ul>` : ""}</div>`;
}
const D_COLOR = { 1: "#16a34a", 2: "#0d9488", 3: "#d97706", 4: "#ea580c", 5: "#dc2626" };
const D_NAME = { 1: "하", 2: "중하", 3: "중", 4: "중상", 5: "상" };

function unitLabel(u) {
  if (!u) return u;
  const m = u.match(/^([mh])(\d)-(\d)$/);
  if (!m) return u;
  return (m[1] === "m" ? "중" : "고") + m[2] + "-" + m[3];
}

export default function AdminItemReview() {
  const [me, setMe] = useState(null);            // 'admin' | 'no' | null(확인 중)
  const [concepts, setConcepts] = useState([]);
  const [tpls, setTpls] = useState([]);

  // 필터
  const [unit, setUnit] = useState("all");
  const [cid, setCid] = useState("all");
  const [status, setStatus] = useState("all");
  const [diff, setDiff] = useState(0);
  const [qtype, setQtype] = useState("all");
  const [ttype, setTtype] = useState("concept_set");
  const [tpl, setTpl] = useState("all");
  const [needsFix, setNeedsFix] = useState(false);
  const [search, setSearch] = useState("");
  const [searchQ, setSearchQ] = useState("");

  // 목록
  const [rows, setRows] = useState([]);
  const [total, setTotal] = useState(0);
  const [nDraft, setNDraft] = useState(0);
  const [page, setPage] = useState(0);
  const [open, setOpen] = useState(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  // 틀별 보기
  const [view, setView] = useState("items");      // "items" | "tpls"
  const [stats, setStats] = useState(null);       // admin_template_stats() 결과 (null = 아직)
  const [statsErr, setStatsErr] = useState("");
  const [tUnit, setTUnit] = useState("all");
  const [tOnlyDraft, setTOnlyDraft] = useState(true);
  const [tSearch, setTSearch] = useState("");

  useEffect(() => { (async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) { setMe("no"); return; }
    const { data: p } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    setMe(p?.role === "admin" ? "admin" : "no");
    const { data: cs } = await supabase.from("concepts")
      .select("id,unit_id,title,sort_order").order("unit_id").order("sort_order");
    setConcepts(cs || []);
  })(); }, []);

  // 개념을 고르면 그 개념의 틀 목록(틀별 집계에서) — 집계가 없으면 item_templates 표(옛 틀)에서
  useEffect(() => { (async () => {
    if (cid === "all") { setTpls([]); return; }
    if (stats) { setTpls(stats.filter((r) => r.concept_id === cid).map((r) => ({ template_id: r.template_id, title: r.discriminates || "" }))); return; }
    const { data } = await supabase.from("item_templates")
      .select("template_id,title").eq("concept_id", cid).order("template_id");
    setTpls(data || []);
  })(); }, [cid, stats]);
  useEffect(() => { if (tpl !== "all" && !tpls.some((t) => t.template_id === tpl) && cid !== "all" && stats) setTpl("all"); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [tpls]);

  const units = useMemo(
    () => [...new Set(concepts.map((c) => c.unit_id))], [concepts]);
  const conceptOpts = useMemo(
    () => concepts.filter((c) => unit === "all" || c.unit_id === unit), [concepts, unit]);
  const conceptTitle = useMemo(() => Object.fromEntries(concepts.map((c) => [c.id, c.title])), [concepts]);
  const conceptOrder = useMemo(() => Object.fromEntries(concepts.map((c) => [c.id, c.sort_order])), [concepts]);

  async function loadStats() {
    setStatsErr("");
    const { data, error } = await supabase.rpc("admin_template_stats");
    if (error) { setStatsErr(/PGRST202|does not exist|not find/i.test(error.message) ? "집계 함수가 아직 없습니다 — supabase/2026-09_template_stats.sql 을 적용하면 보입니다." : "집계 실패: " + error.message); setStats([]); return; }
    const rows = (data || []).map((r) => ({ ...r, n_draft: Number(r.n_draft), n_live: Number(r.n_live) }));
    rows.sort((a, b) => unitRank(a.unit_id) - unitRank(b.unit_id) || (conceptOrder[a.concept_id] ?? 999) - (conceptOrder[b.concept_id] ?? 999)
      || String(a.concept_id).localeCompare(String(b.concept_id)) || tplNo(a.template_id) - tplNo(b.template_id) || a.template_id.localeCompare(b.template_id));
    setStats(rows);
  }
  useEffect(() => { if (me === "admin" && view === "tpls" && stats === null) loadStats(); },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, view]);

  const tplRows = useMemo(() => {
    if (!stats) return [];
    const q = tSearch.trim().toLowerCase();
    return stats.filter((r) => (tUnit === "all" || r.unit_id === tUnit) && (!tOnlyDraft || r.n_draft > 0)
      && (!q || [r.template_id, r.discriminates, r.sample_q, conceptTitle[r.concept_id]].some((x) => String(x || "").toLowerCase().includes(q))));
  }, [stats, tUnit, tOnlyDraft, tSearch, conceptTitle]);

  // 틀별 보기 → 그 틀의 문항 목록으로
  function showTemplate(r) {
    setUnit(r.unit_id); setCid(r.concept_id); setTpl(r.template_id); setStatus("all"); setNeedsFix(false); setSearch(""); setSearchQ("");
    setView("items");
  }

  // 틀 하나의 draft ↔ live — 1,000건씩
  async function flipTemplate(r, from, to) {
    const n = from === "draft" ? r.n_draft : r.n_live;
    if (!n) return;
    if (!window.confirm(`${r.template_id} 의 ${from} ${n}건을 ${to}로 전환할까요?`)) return;
    setBusy(true);
    let done = 0, lastFirst = null;
    while (done < n) {
      const { data, error } = await supabase.from("test_items").select("id").eq("template_id", r.template_id).eq("status", from).order("id").limit(BULK);
      if (error) { setMsg(`전환 실패(${done}건까지 됨): ` + error.message); break; }
      if (!data?.length) break;
      if (data[0].id === lastFirst) { setMsg(`전환이 진행되지 않습니다(${done}건까지 됨) — 권한을 확인하세요`); break; }
      lastFirst = data[0].id;
      const { error: e2 } = await supabase.from("test_items").update({ status: to }).in("id", data.map((x) => x.id));
      if (e2) { setMsg(`전환 실패(${done}건까지 됨): ` + e2.message); break; }
      done += data.length;
    }
    setBusy(false);
    if (done >= n) setMsg(`${r.template_id}: ${done}건 → ${to}`);
    setStats((st) => (st || []).map((x) => (x.template_id !== r.template_id ? x
      : { ...x, n_draft: x.n_draft + (to === "draft" ? done : -done), n_live: x.n_live + (to === "live" ? done : -done) })));
    bustStudyCache();
  }

  function applyFilters(q) {
    if (ttype !== "all") q = q.eq("test_type", ttype);
    if (status !== "all") q = q.eq("status", status);
    if (diff) q = q.eq("difficulty", diff);
    if (qtype !== "all") q = q.eq("qtype", qtype);
    if (cid !== "all") q = q.contains("concept_ids", [cid]);
    else if (unit !== "all") q = q.eq("unit_id", unit);
    if (tpl !== "all") q = q.eq("template_id", tpl);
    if (needsFix) q = q.contains("tags", ["needs_fix"]);
    if (searchQ) q = q.ilike("question", "%" + searchQ + "%");
    return q;
  }

  async function load(p = page, keepMsg = false) {
    setBusy(true); if (!keepMsg) setMsg("");
    const [list, tot, dr] = await Promise.all([
      applyFilters(supabase.from("test_items").select(LIST_COLS))
        .order("created_at", { ascending: false }).order("id").range(p * PAGE, p * PAGE + PAGE - 1),
      applyFilters(supabase.from("test_items").select("id", { count: "exact", head: true })),
      applyFilters(supabase.from("test_items").select("id", { count: "exact", head: true })).eq("status", "draft"),
    ]);
    setBusy(false);
    const error = list.error || tot.error || dr.error;
    if (error) { setMsg("불러오기 실패: " + error.message); return; }
    setRows(list.data || []); setTotal(tot.count || 0); setNDraft(dr.count || 0); setOpen(null);
  }

  // 펼칠 때 해설·그림을 받아 행에 붙인다 (한 번만)
  async function openItem(it) {
    if (open === it.id) { setOpen(null); return; }
    setOpen(it.id);
    if (it._full) return;
    const { data, error } = await supabase.from("test_items").select("solution,figure").eq("id", it.id).single();
    if (error) { setMsg("해설 불러오기 실패: " + error.message); return; }
    setRows((r) => r.map((x) => (x.id === it.id ? { ...x, ...data, _full: true } : x)));
  }

  useEffect(() => { if (me === "admin") { setPage(0); load(0); } },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, unit, cid, status, diff, qtype, ttype, tpl, needsFix, searchQ]);

  async function setItemStatus(it, s) {
    const { error } = await supabase.from("test_items").update({ status: s }).eq("id", it.id);
    if (error) { setMsg("상태 변경 실패: " + error.message); return; }
    setRows((r) => r.map((x) => (x.id === it.id ? { ...x, status: s } : x)));
    bustStudyCache();
  }

  async function toggleFix(it) {
    const has = (it.tags || []).includes("needs_fix");
    const tags = has ? it.tags.filter((t) => t !== "needs_fix") : [...(it.tags || []), "needs_fix"];
    const { error } = await supabase.from("test_items").update({ tags }).eq("id", it.id);
    if (error) { setMsg("태그 실패: " + error.message); return; }
    setRows((r) => r.map((x) => (x.id === it.id ? { ...x, tags } : x)));
  }

  async function removeItem(it) {
    if (!window.confirm("이 문항을 폐기할까요? (item_rejects에 기록 후 삭제)")) return;
    const g = it.gen_meta || {};
    await supabase.from("item_rejects").insert({
      concept_id: (it.concept_ids || [])[0] || null,
      template_id: g.tpl || null, param_index: g.idx ?? null,
      content_key: it.content_key || null, struct_key: it.struct_key || null,
      reason: "manual", question: (it.question || "").slice(0, 200), site: "admin",
    });
    const { error } = await supabase.from("test_items").delete().eq("id", it.id);
    if (error) { setMsg("삭제 실패: " + error.message); return; }
    setRows((r) => r.filter((x) => x.id !== it.id)); setTotal((t) => t - 1);
  }

  async function bulkStatus(from, to) {
    const { count } = await applyFilters(
      supabase.from("test_items").select("id", { count: "exact", head: true }))
      .eq("status", from);
    if (!count) { setMsg(`${from} 상태인 문항이 없습니다.`); return; }
    if (!window.confirm(`현재 필터의 ${from} ${count}건을 ${to}로 전환할까요?`)) return;
    setBusy(true);
    let done = 0, lastFirst = null;
    while (done < count) {
      const { data, error } = await applyFilters(supabase.from("test_items").select("id")).eq("status", from).order("id").limit(BULK);
      if (error) { setMsg(`일괄 전환 실패(${done}건까지 됨): ` + error.message); break; }
      if (!data?.length) break;
      if (data[0].id === lastFirst) { setMsg(`일괄 전환이 진행되지 않습니다(${done}건까지 됨) — 권한을 확인하세요`); break; }
      lastFirst = data[0].id;
      const { error: e2 } = await supabase.from("test_items").update({ status: to }).in("id", data.map((r) => r.id));
      if (e2) { setMsg(`일괄 전환 실패(${done}건까지 됨): ` + e2.message); break; }
      done += data.length; setMsg(`전환 중 ${done} / ${count}`);
    }
    setBusy(false);
    if (done >= count) setMsg(`${done}건 → ${to} 완료`);
    bustStudyCache();
    setStats(null);
    load(page, true);
  }

  if (me === null) return <div className="irv-wrap">확인 중…</div>;
  if (me === "no") return <div className="irv-wrap">관리자 전용 페이지입니다.</div>;

  const pages = Math.max(1, Math.ceil(total / PAGE));

  const tSum = tplRows.reduce((a, r) => ({ d: a.d + r.n_draft, l: a.l + r.n_live }), { d: 0, l: 0 });
  const tUnits = stats ? [...new Set(stats.map((r) => r.unit_id))].sort((a, b) => unitRank(a) - unitRank(b)) : [];

  if (view === "tpls") {
    let lastCid = null;
    return (
      <div className="irv-wrap">
        <style>{CSS}</style>
        <div className="irv-head">
          <h2>문항 검토 <span className="irv-sub">틀 {tplRows.length}개 · draft {tSum.d} / live {tSum.l}</span></h2>
          <div className="irv-bulk">
            <button className="irv-chip" onClick={() => setView("items")}>문항</button>
            <button className="irv-chip on">틀별</button>
          </div>
        </div>
        <div className="irv-filters">
          <select value={tUnit} onChange={(e) => setTUnit(e.target.value)}>
            <option value="all">학기 전체</option>
            {tUnits.map((u) => <option key={u} value={u}>{unitLabel(u)}</option>)}
          </select>
          <button className={"irv-chip" + (tOnlyDraft ? " on" : "")} onClick={() => setTOnlyDraft(!tOnlyDraft)}>draft 있는 틀만</button>
          <input className="irv-search" value={tSearch} placeholder="틀 · 개념 · 발문 검색" onChange={(e) => setTSearch(e.target.value)} />
          <button className="irv-btn" disabled={busy} onClick={() => { setStats(null); loadStats(); }}>다시 세기</button>
          {msg && <span className="irv-msg">{msg}</span>}
        </div>
        {stats === null && !statsErr && <p className="irv-empty">틀별로 세는 중…</p>}
        {statsErr && <p className="irv-msg">{statsErr}</p>}
        <div className="irv-tpls">
          {tplRows.map((r) => {
            const head = r.concept_id !== lastCid; lastCid = r.concept_id;
            const cRows = head ? tplRows.filter((x) => x.concept_id === r.concept_id) : null;
            return (
              <div key={r.template_id}>
                {head && (
                  <div className="irv-cgroup">
                    <span className="irv-cg-id">{unitLabel(r.unit_id)} · {String(r.concept_id).split("-").pop()}</span>
                    <span className="irv-cg-title">{conceptTitle[r.concept_id] || r.concept_id}</span>
                    <span className="irv-cg-n">틀 {cRows.length} · draft {cRows.reduce((a, x) => a + x.n_draft, 0)} / live {cRows.reduce((a, x) => a + x.n_live, 0)}</span>
                  </div>
                )}
                <div className={"irv-tpl" + (r.n_draft ? " has-draft" : "")}>
                  <div className="irv-tpl-row">
                    <span className="irv-tag tpl">{r.template_id.replace(r.concept_id + "-", "").replace(/^(.+)-t(\d+)$/, "$1 · t$2")}</span>
                    <span className="irv-d" style={{ background: D_COLOR[r.difficulty] || "#64748b" }}>{r.difficulty}</span>
                    <span className="irv-tag">{r.qtype}</span>
                    {r.geometry && <span className="irv-tag">기하</span>}
                    {r.has_figure && <span className="irv-tag">그림</span>}
                    <span className="irv-tpl-n"><b className={r.n_draft ? "st-draft" : ""}>draft {r.n_draft}</b> · live {r.n_live}</span>
                  </div>
                  <div className="irv-tpl-q"><MathText text={String(r.sample_q || "").replace(/\n/g, " ")} pre={false} /></div>
                  {r.discriminates && <div className="irv-tpl-dis">재는 것: {r.discriminates}</div>}
                  <div className="irv-tpl-act">
                    <button className="irv-btn" onClick={() => showTemplate(r)}>문항 보기</button>
                    {r.n_draft > 0 && <button className="irv-btn go" disabled={busy} onClick={() => flipTemplate(r, "draft", "live")}>draft → live ({r.n_draft})</button>}
                    {r.n_live > 0 && <button className="irv-btn" disabled={busy} onClick={() => flipTemplate(r, "live", "draft")}>live → draft</button>}
                  </div>
                </div>
              </div>
            );
          })}
          {stats && !tplRows.length && <p className="irv-empty">조건에 맞는 틀이 없습니다.</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="irv-wrap">
      <style>{CSS}</style>
      <div className="irv-head">
        <h2>문항 검토 <span className="irv-sub">{total}건 · draft {nDraft} / live {total - nDraft}</span></h2>
        <div className="irv-bulk">
          <button className="irv-chip on">문항</button>
          <button className="irv-chip" onClick={() => setView("tpls")}>틀별</button>
          <button className="irv-btn go" disabled={busy} onClick={() => bulkStatus("draft", "live")}>필터 전체 draft → live</button>
          <button className="irv-btn" disabled={busy} onClick={() => bulkStatus("live", "draft")}>live → draft</button>
        </div>
      </div>

      <div className="irv-filters">
        <select value={unit} onChange={(e) => { setUnit(e.target.value); setCid("all"); setTpl("all"); }}>
          <option value="all">단원 전체</option>
          {units.map((u) => <option key={u} value={u}>{unitLabel(u)}</option>)}
        </select>
        <select value={cid} onChange={(e) => { setCid(e.target.value); setTpl("all"); }}>
          <option value="all">개념 전체</option>
          {conceptOpts.map((c) => <option key={c.id} value={c.id}>{c.id.split("-").pop()} {c.title}</option>)}
        </select>
        <select value={ttype} onChange={(e) => setTtype(e.target.value)}>
          {["concept_set", "unit", "calc", "rain", "mock", "out", "all"].map((t) =>
            <option key={t} value={t}>{t === "all" ? "종류 전체" : t}</option>)}
        </select>
        {(tpls.length > 0 || tpl !== "all") && (
          <select value={tpl} onChange={(e) => setTpl(e.target.value)}>
            <option value="all">틀 전체</option>
            {tpls.map((t) => <option key={t.template_id} value={t.template_id}>{t.template_id}{t.title ? " — " + String(t.title).slice(0, 40) : ""}</option>)}
            {tpl !== "all" && !tpls.some((t) => t.template_id === tpl) && <option value={tpl}>{tpl}</option>}
          </select>
        )}
        {tpl !== "all" && <button className="irv-chip on" onClick={() => setTpl("all")}>틀 {tpl} ×</button>}
      </div>

      <div className="irv-filters">
        {["all", "draft", "live"].map((s) => (
          <button key={s} className={"irv-chip" + (status === s ? " on" : "")}
            onClick={() => setStatus(s)}>{s === "all" ? "상태 전체" : s}</button>
        ))}
        <span className="irv-gap" />
        {[0, 1, 2, 3, 4, 5].map((d) => (
          <button key={d} className={"irv-chip" + (diff === d ? " on" : "")}
            onClick={() => setDiff(d)}>{d === 0 ? "난이도 전체" : `${d} ${D_NAME[d]}`}</button>
        ))}
        <span className="irv-gap" />
        {["all", "choice", "short"].map((t) => (
          <button key={t} className={"irv-chip" + (qtype === t ? " on" : "")}
            onClick={() => setQtype(t)}>{t === "all" ? "문항형 전체" : t}</button>
        ))}
        <button className={"irv-chip fix" + (needsFix ? " on" : "")}
          onClick={() => setNeedsFix(!needsFix)}>수정필요만</button>
      </div>

      <div className="irv-filters">
        <input className="irv-search" value={search} placeholder="문제 본문 검색"
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && setSearchQ(search.trim())} />
        <button className="irv-btn" onClick={() => setSearchQ(search.trim())}>검색</button>
        {searchQ && <button className="irv-btn" onClick={() => { setSearch(""); setSearchQ(""); }}>지움</button>}
        {msg && <span className="irv-msg">{msg}</span>}
      </div>

      <div className="irv-list">
        {rows.map((it) => {
          const g = it.gen_meta || {};
          const isOpen = open === it.id;
          const fix = (it.tags || []).includes("needs_fix");
          return (
            <div key={it.id} className={"irv-item" + (isOpen ? " open" : "")}>
              <div className="irv-row" onClick={() => openItem(it)}>
                <span className="irv-d" style={{ background: D_COLOR[it.difficulty] || "#64748b" }}>{it.difficulty}</span>
                <span className="irv-tag">{it.qtype}</span>
                <span className={"irv-tag st-" + it.status}>{it.status}</span>
                {g.tpl && <span className="irv-tag tpl">{String(g.tpl).replace(it.concept_ids?.[0] + "-", "")}</span>}
                {fix && <span className="irv-tag fixed">수정필요</span>}
                <span className="irv-q">{(it.question || "").replace(/\[\[|\]\]/g, "").split("\n")[0]}</span>
              </div>
              {isOpen && (
                <div className="irv-detail">
                  <ItemQuestion item={it} reveal={true} figWidth={320} />
                  <p className="irv-ans">정답: <b><MathText text={it.answer} /></b>
                    {(it.answer_alt || []).length > 0 && <span className="irv-alt">  (허용: {it.answer_alt.join(", ")})</span>}</p>
                  {it._full
                    ? (it.solution
                      ? <div className="isol irv-sol" dangerouslySetInnerHTML={{ __html: solutionHtml(it) }} />
                      : <p className="irv-nosol">해설 없음</p>)
                    : <p className="irv-nosol">해설 불러오는 중…</p>}
                  <p className="irv-meta">
                    {(it.concept_ids || []).join(", ")} · {g.tpl}#{g.idx} · {it.source} · {g.site || "-"} · {String(it.created_at).slice(0, 16).replace("T", " ")}
                  </p>
                  <div className="irv-actions">
                    {it.status === "draft"
                      ? <button className="irv-btn go" onClick={() => setItemStatus(it, "live")}>live로</button>
                      : <button className="irv-btn" onClick={() => setItemStatus(it, "draft")}>draft로</button>}
                    <button className={"irv-btn" + (fix ? " warn" : "")} onClick={() => toggleFix(it)}>{fix ? "수정필요 해제" : "수정필요"}</button>
                    <button className="irv-btn danger" onClick={() => removeItem(it)}>폐기</button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
        {!rows.length && !busy && <p className="irv-empty">조건에 맞는 문항이 없습니다.</p>}
      </div>

      <div className="irv-pager">
        <button className="irv-btn" disabled={page === 0} onClick={() => { setPage(page - 1); load(page - 1); }}>‹</button>
        <span>{page + 1} / {pages}</span>
        <button className="irv-btn" disabled={page + 1 >= pages} onClick={() => { setPage(page + 1); load(page + 1); }}>›</button>
      </div>
    </div>
  );
}

const CSS = `
.irv-wrap{max-width:860px;margin:0 auto;padding:16px 14px 60px;color:#1e293b;--ink:#1e293b;--muted:#64748b;--border:#e2e8f0;--surface:#fff;--surface2:#f8fafc;--accent:#0f766e}
.irv-detail .iq{margin-top:4px}
.irv-nosol{font-size:13px;color:#64748b;margin:8px 0}
.irv-rubric{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:4px}
.irv-rubric td{border-top:1px solid #e2e8f0;padding:6px 4px;vertical-align:top}
.irv-rubric td:first-child{white-space:nowrap;font-weight:700;width:28%}
.irv-rubric .irv-pt{display:block;font-weight:400;color:#64748b;font-size:11.5px}
.irv-rubric .irv-partial{display:block;color:#64748b;font-size:11.5px;margin-top:2px}
.irv-pits{margin:6px 0 0 18px;padding:0;font-size:12.5px;color:#475569}
.irv-pits .irv-eff{color:#b45309}
.irv-tpls{margin-top:8px}
.irv-cgroup{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin:16px 0 6px;padding-bottom:4px;border-bottom:2px solid #0f172a}
.irv-cg-id{font-size:12px;color:#64748b;font-variant-numeric:tabular-nums}
.irv-cg-title{font-weight:800;font-size:15px}
.irv-cg-n{font-size:12px;color:#64748b;margin-left:auto}
.irv-tpl{border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;margin:6px 0;background:#fff}
.irv-tpl.has-draft{border-color:#fbbf24;background:#fffdf5}
.irv-tpl-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.irv-tpl-n{margin-left:auto;font-size:12.5px;color:#475569}
.irv-tpl-n .st-draft{color:#b45309}
.irv-tpl-q{font-size:13.5px;line-height:1.5;margin:6px 0 2px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.irv-tpl-dis{font-size:12px;color:#64748b;line-height:1.45;margin:2px 0 4px}
.irv-tpl-act{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.irv-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.irv-head h2{margin:6px 0;font-size:20px}
.irv-sub{font-size:13px;color:#64748b;font-weight:400;margin-left:8px}
.irv-bulk{display:flex;gap:6px}
.irv-filters{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;align-items:center}
.irv-filters select{padding:6px 8px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font-size:13px}
.irv-chip{padding:5px 10px;border:1px solid #cbd5e1;border-radius:999px;background:#fff;font-size:12.5px;cursor:pointer}
.irv-chip.on{background:#0f172a;color:#fff;border-color:#0f172a}
.irv-chip.fix.on{background:#b45309;border-color:#b45309}
.irv-gap{width:6px}
.irv-search{flex:1;min-width:160px;padding:7px 10px;border:1px solid #cbd5e1;border-radius:8px;font-size:13px}
.irv-btn{padding:6px 11px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font-size:12.5px;cursor:pointer}
.irv-btn.go{background:#16a34a;border-color:#16a34a;color:#fff}
.irv-btn.warn{background:#b45309;border-color:#b45309;color:#fff}
.irv-btn.danger{border-color:#dc2626;color:#dc2626}
.irv-btn:disabled{opacity:.45;cursor:default}
.irv-msg{font-size:12.5px;color:#b45309}
.irv-list{margin-top:6px}
.irv-item{border:1px solid #e2e8f0;border-radius:10px;margin-bottom:6px;background:#fff;overflow:hidden}
.irv-item.open{border-color:#94a3b8}
.irv-row{display:flex;align-items:center;gap:6px;padding:8px 10px;cursor:pointer}
.irv-d{width:20px;height:20px;border-radius:6px;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:none}
.irv-tag{font-size:11px;border:1px solid #e2e8f0;border-radius:5px;padding:1px 5px;color:#475569;flex:none}
.irv-tag.st-live{color:#15803d;border-color:#86efac;background:#f0fdf4}
.irv-tag.st-draft{color:#64748b;background:#f8fafc}
.irv-tag.tpl{color:#1d4ed8;border-color:#bfdbfe}
.irv-tag.fixed{color:#b45309;border-color:#fcd34d;background:#fffbeb}
.irv-q{font-size:13.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.irv-detail{padding:4px 12px 12px;border-top:1px dashed #e2e8f0}
.irv-ans{margin:8px 0 4px;font-size:13.5px}
.irv-alt{color:#64748b;font-size:12.5px}
.irv-sol{background:#f8fafc;border-radius:8px;padding:8px 10px;margin:6px 0}
.irv-meta{font-size:11.5px;color:#94a3b8;margin:6px 0}
.irv-actions{display:flex;gap:6px}
.irv-empty{text-align:center;color:#94a3b8;padding:30px 0}
.irv-pager{display:flex;justify-content:center;align-items:center;gap:12px;margin-top:12px;font-size:13px}
`;
