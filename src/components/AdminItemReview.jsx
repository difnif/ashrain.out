// ashrain.out — 문항 전수 검토 (AdminItemReview v1.0, 관리자 전용, #/admin/items)
// 목적: 생성·등록된 test_items 전체를 필터로 훑고, 펼쳐 보고, live/draft 전환·삭제·수정필요 표시.
// 삭제는 item_rejects에 사유(manual)로 기록 후 제거 — E-10 "폐기 이유는 남긴다".

import { useEffect, useMemo, useState } from "react";
import { supabase } from "../supabaseClient";

const PAGE = 50;
const D_COLOR = { 1: "#16a34a", 2: "#0d9488", 3: "#d97706", 4: "#ea580c", 5: "#dc2626" };
const D_NAME = { 1: "하", 2: "중하", 3: "중", 4: "중상", 5: "상" };
const CIRC = ["①", "②", "③", "④", "⑤"];

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

  useEffect(() => { (async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) { setMe("no"); return; }
    const { data: p } = await supabase.from("profiles").select("role").eq("id", user.id).single();
    setMe(p?.role === "admin" ? "admin" : "no");
    const { data: cs } = await supabase.from("concepts")
      .select("id,unit_id,title,sort_order").order("unit_id").order("sort_order");
    setConcepts(cs || []);
  })(); }, []);

  useEffect(() => { (async () => {
    if (cid === "all") { setTpls([]); setTpl("all"); return; }
    const { data } = await supabase.from("item_templates")
      .select("template_id,title").eq("concept_id", cid).order("template_id");
    setTpls(data || []); setTpl("all");
  })(); }, [cid]);

  const units = useMemo(
    () => [...new Set(concepts.map((c) => c.unit_id))], [concepts]);
  const conceptOpts = useMemo(
    () => concepts.filter((c) => unit === "all" || c.unit_id === unit), [concepts, unit]);

  function applyFilters(q) {
    if (ttype !== "all") q = q.eq("test_type", ttype);
    if (status !== "all") q = q.eq("status", status);
    if (diff) q = q.eq("difficulty", diff);
    if (qtype !== "all") q = q.eq("qtype", qtype);
    if (cid !== "all") q = q.contains("concept_ids", [cid]);
    else if (unit !== "all") q = q.eq("unit_id", unit);
    if (tpl !== "all") q = q.eq("gen_meta->>tpl", tpl);
    if (needsFix) q = q.contains("tags", ["needs_fix"]);
    if (searchQ) q = q.ilike("question", "%" + searchQ + "%");
    return q;
  }

  async function load(p = page) {
    setBusy(true);
    const { data, count, error } = await applyFilters(
      supabase.from("test_items").select("*", { count: "exact" }))
      .order("created_at", { ascending: false }).order("id")
      .range(p * PAGE, p * PAGE + PAGE - 1);
    const { count: dc } = await applyFilters(
      supabase.from("test_items").select("id", { count: "exact", head: true }))
      .eq("status", "draft");
    setBusy(false);
    if (error) { setMsg("불러오기 실패: " + error.message); return; }
    setRows(data || []); setTotal(count || 0); setNDraft(dc || 0); setOpen(null);
  }

  useEffect(() => { if (me === "admin") { setPage(0); load(0); } },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [me, unit, cid, status, diff, qtype, ttype, tpl, needsFix, searchQ]);

  async function setItemStatus(it, s) {
    const { error } = await supabase.from("test_items").update({ status: s }).eq("id", it.id);
    if (error) { setMsg("상태 변경 실패: " + error.message); return; }
    setRows((r) => r.map((x) => (x.id === it.id ? { ...x, status: s } : x)));
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
    const { error } = await applyFilters(
      supabase.from("test_items").update({ status: to })).eq("status", from);
    setBusy(false);
    if (error) { setMsg("일괄 전환 실패: " + error.message); return; }
    setMsg(`${count}건 → ${to} 완료`); load(page);
  }

  if (me === null) return <div className="irv-wrap">확인 중…</div>;
  if (me === "no") return <div className="irv-wrap">관리자 전용 페이지입니다.</div>;

  const pages = Math.max(1, Math.ceil(total / PAGE));

  return (
    <div className="irv-wrap">
      <style>{CSS}</style>
      <div className="irv-head">
        <h2>문항 검토 <span className="irv-sub">{total}건 · draft {nDraft} / live {total - nDraft}</span></h2>
        <div className="irv-bulk">
          <button className="irv-btn go" disabled={busy} onClick={() => bulkStatus("draft", "live")}>필터 전체 draft → live</button>
          <button className="irv-btn" disabled={busy} onClick={() => bulkStatus("live", "draft")}>live → draft</button>
        </div>
      </div>

      <div className="irv-filters">
        <select value={unit} onChange={(e) => { setUnit(e.target.value); setCid("all"); }}>
          <option value="all">단원 전체</option>
          {units.map((u) => <option key={u} value={u}>{unitLabel(u)}</option>)}
        </select>
        <select value={cid} onChange={(e) => setCid(e.target.value)}>
          <option value="all">개념 전체</option>
          {conceptOpts.map((c) => <option key={c.id} value={c.id}>{c.id.split("-").pop()} {c.title}</option>)}
        </select>
        <select value={ttype} onChange={(e) => setTtype(e.target.value)}>
          {["concept_set", "unit", "calc", "rain", "mock", "out", "all"].map((t) =>
            <option key={t} value={t}>{t === "all" ? "종류 전체" : t}</option>)}
        </select>
        {tpls.length > 0 && (
          <select value={tpl} onChange={(e) => setTpl(e.target.value)}>
            <option value="all">틀 전체</option>
            {tpls.map((t) => <option key={t.template_id} value={t.template_id}>{t.template_id} {t.title}</option>)}
          </select>
        )}
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
              <div className="irv-row" onClick={() => setOpen(isOpen ? null : it.id)}>
                <span className="irv-d" style={{ background: D_COLOR[it.difficulty] || "#64748b" }}>{it.difficulty}</span>
                <span className="irv-tag">{it.qtype}</span>
                <span className={"irv-tag st-" + it.status}>{it.status}</span>
                {g.tpl && <span className="irv-tag tpl">{String(g.tpl).replace(it.concept_ids?.[0] + "-", "")}</span>}
                {fix && <span className="irv-tag fixed">수정필요</span>}
                <span className="irv-q">{(it.question || "").split("\n")[0]}</span>
              </div>
              {isOpen && (
                <div className="irv-detail">
                  <p className="irv-question">{it.question}</p>
                  {it.qtype === "choice" && (it.choices || []).map((c, i) => (
                    <p key={i} className={"irv-choice" + (c === it.answer ? " ans" : "")}>{CIRC[i]} {c}</p>
                  ))}
                  <p className="irv-ans">정답: <b>{it.answer}</b>
                    {(it.answer_alt || []).length > 0 && <span className="irv-alt">  (허용: {it.answer_alt.join(", ")})</span>}</p>
                  {it.solution && (
                    <div className="irv-sol">
                      <p className="irv-sol-o">{it.solution.outline}</p>
                      {(it.solution.steps || []).map((s, i) => <p key={i} className="irv-sol-s">{i + 1}. {s}</p>)}
                      <p className="irv-sol-c">검산 — {it.solution.check}</p>
                    </div>
                  )}
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
.irv-wrap{max-width:860px;margin:0 auto;padding:16px 14px 60px;color:#1e293b}
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
.irv-question{white-space:pre-line;font-size:14.5px;margin:8px 0}
.irv-choice{margin:2px 0;font-size:14px}
.irv-choice.ans{font-weight:700;color:#15803d}
.irv-ans{margin:8px 0 4px;font-size:13.5px}
.irv-alt{color:#64748b;font-size:12.5px}
.irv-sol{background:#f8fafc;border-radius:8px;padding:8px 10px;margin:6px 0}
.irv-sol-o{font-weight:700;font-size:13px;margin:0 0 4px}
.irv-sol-s{margin:2px 0;font-size:13px;white-space:pre-line}
.irv-sol-c{margin:4px 0 0;font-size:12.5px;color:#475569}
.irv-meta{font-size:11.5px;color:#94a3b8;margin:6px 0}
.irv-actions{display:flex;gap:6px}
.irv-empty{text-align:center;color:#94a3b8;padding:30px 0}
.irv-pager{display:flex;justify-content:center;align-items:center;gap:12px;margin-top:12px;font-size:13px}
`;
