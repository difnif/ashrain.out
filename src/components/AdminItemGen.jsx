// ashrain.out — 테스트 문항 생성기 (v1.1, 관리자 전용, #/admin/itemgen)
// v1.1: ③ JSON 등록 탭 — MD 방(하이쿠·소넷·오푸스)이나 Fable이 만든 문항 JSON을 붙여넣어 일괄 등록
// 탭 ①문항 생성: 모델·범위·형식 지정 → /api/genItems → 미리보기(KaTeX)·편집·선별 → test_items 저장(draft)
// 탭 ②풀이 붙이기: solution 없는 문항 로드 → 오푸스/페이블로 풀이 생성 → 병합 저장
import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { UNIT_NAME } from "../lib/qcode";

const CSS = `
.ig-root { min-height: 100vh; padding: 18px 12px 80px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ig-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; }
.ig-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#1B1E24; --inbd:#2A2E36; }
.ig-wrap { max-width: 760px; margin: 0 auto; }
.ig-top { display:flex; align-items:center; gap:10px; margin-bottom:12px; }
.ig-h { color:var(--ink); font-size:18px; font-weight:800; margin:0; flex:1; }
.ig-back { color:var(--mut); font-size:13px; cursor:pointer; text-decoration:underline; }
.ig-tabs { display:flex; gap:6px; margin-bottom:14px; }
.ig-tab { background:transparent; border:1px solid var(--inbd); border-radius:999px; color:var(--mut);
  font-size:13px; font-weight:700; padding:8px 14px; cursor:pointer; }
.ig-tab.on { border-color:var(--ac); color:var(--ac); }
.ig-card { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:14px; margin-bottom:12px; }
.ig-lab { font-size:12px; font-weight:800; color:var(--mut); margin:10px 0 5px; }
.ig-lab:first-child { margin-top:0; }
.ig-row { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
.ig-sel, .ig-inp { background:var(--in); border:1px solid var(--inbd); border-radius:10px; color:var(--ink);
  font-size:13px; padding:9px 10px; box-sizing:border-box; }
.ig-inp { width:100%; }
.ig-ta { width:100%; min-height:74px; resize:vertical; background:var(--in); border:1px solid var(--inbd);
  border-radius:10px; color:var(--ink); font-size:13px; padding:9px 10px; box-sizing:border-box; line-height:1.6; }
.ig-chip { background:transparent; border:1px solid var(--inbd); border-radius:999px; color:var(--mut);
  font-size:12px; font-weight:700; padding:6px 11px; cursor:pointer; }
.ig-chip.on { border-color:var(--ac); color:var(--ac); }
.ig-btn { border:none; border-radius:11px; font-size:14px; font-weight:800; padding:11px 18px; cursor:pointer; }
.ig-ok { background:var(--ac); color:#fff; }
.ig-ghost { background:transparent; color:var(--mut); border:1px solid var(--bd); }
.ig-warn { color:#DC2626; font-size:12.5px; margin:8px 0 0; }
.ig-sum { font-size:12.5px; color:var(--mut); margin:0 0 8px; }
/* 문항 카드 */
.qi { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:12px; margin-bottom:10px; }
.qi.off { opacity:.42; }
.qi-hd { display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:7px; }
.qi-b { font-size:10.5px; font-weight:800; border-radius:6px; padding:2px 7px; background:var(--in);
  color:var(--mut); border:1px solid var(--inbd); }
.qi-b.hot { color:var(--ac); border-color:var(--ac); }
.qi-b.red { color:#DC2626; border-color:#DC2626; }
.qi-q { font-size:14px; color:var(--ink); line-height:1.7; margin:0 0 7px; word-break:keep-all; }
.qi-ch { font-size:13px; color:var(--ink); line-height:1.8; margin:0 0 6px 4px; }
.qi-a { font-size:12.5px; color:var(--ac); font-weight:800; margin:0 0 4px; }
.qi-sol { font-size:12.5px; color:var(--mut); line-height:1.7; background:var(--in); border-radius:10px;
  padding:8px 10px; margin-top:6px; }
.qi-ft { display:flex; gap:6px; margin-top:8px; }
.katex { font-size:1.02em; }
`;

const MODEL_OPT = [
  ["haiku", "하이쿠 (연산·저난도)"], ["sonnet", "소넷 (일반 문항)"],
  ["opus", "오푸스 (풀이·상위)"], ["fable", "페이블 (고난도·풀이)"],
];
const TEST_OPT = [
  ["concept_set", "개념 묶음"], ["unit", "단원"], ["calc", "연산"], ["sangwa", "산과(증명·서술)"],
  ["mock", "실전 모의고사"], ["ash", "Ash TEST"], ["rain", "Rain TEST"], ["out", "Out TEST"],
];
const QT_OPT = [["choice", "5지선다"], ["short", "단답"], ["ox", "OX"], ["proof", "증명"], ["essay", "서술"]];

/* ── KaTeX 프리뷰: $...$ 구간만 렌더, 실패 시 원문 그대로 ── */
let katexP = null;
function loadKatex() {
  if (!katexP) katexP = (async () => {
    if (!document.getElementById("katex-css")) {
      const l = document.createElement("link"); l.id = "katex-css"; l.rel = "stylesheet";
      l.href = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"; document.head.appendChild(l);
    }
    const m = await import(/* @vite-ignore */ "https://cdn.jsdelivr.net/npm/katex@0.16.11/+esm");
    return m.default || m;
  })().catch(() => null);
  return katexP;
}
function MathText({ text }) {
  const [k, setK] = useState(null);
  useEffect(() => { if (/\$/.test(text || "")) loadKatex().then(setK); }, [text]);
  const parts = useMemo(() => String(text || "").split(/(\$[^$]+\$)/g), [text]);
  return (
    <span>{parts.map((p, i) => {
      if (p.startsWith("$") && p.endsWith("$") && k) {
        try { return <span key={i} dangerouslySetInnerHTML={{ __html: k.renderToString(p.slice(1, -1), { throwOnError: false }) }} />; }
        catch { return <span key={i}>{p}</span>; }
      }
      return <span key={i}>{p}</span>;
    })}</span>
  );
}

/* ── 문항 미리보기 카드 ── */
function ItemCard({ it, off, onToggle, onEdit }) {
  return (
    <div className={"qi" + (off ? " off" : "")}>
      <div className="qi-hd">
        <span className="qi-b hot">{it.qtype}</span>
        <span className="qi-b">난이도 {it.difficulty}</span>
        <span className="qi-b">{it.points}점</span>
        {it.time_limit ? <span className="qi-b">{it.time_limit}초</span> : null}
        {(it.tags || []).map((t, i) => <span key={i} className="qi-b">#{t}</span>)}
        {(it._warns || []).map((w, i) => <span key={i} className="qi-b red">⚠ {w}</span>)}
      </div>
      <p className="qi-q"><MathText text={it.question} /></p>
      {it.choices && <p className="qi-ch">{it.choices.map((c, i) => (
        <span key={i}>{"①②③④⑤"[i]} <MathText text={String(c)} />&nbsp;&nbsp;</span>))}</p>}
      <p className="qi-a">답: <MathText text={String(it.answer)} />{it.answer_alt?.length ? `  (동치: ${it.answer_alt.join(", ")})` : ""}</p>
      {it.solution && (
        <div className="qi-sol">
          <b>💡 {it.solution.outline}</b>
          {(it.solution.steps || []).map((s, i) => <div key={i}>· <MathText text={s} /></div>)}
          {it.solution.check && <div style={{ marginTop: 3 }}>✔ <MathText text={it.solution.check} /></div>}
        </div>
      )}
      <div className="qi-ft">
        {onToggle && <button className="ig-chip" onClick={onToggle}>{off ? "포함" : "제외"}</button>}
        {onEdit && <button className="ig-chip" onClick={onEdit}>✎ JSON 수정</button>}
      </div>
    </div>
  );
}

export default function AdminItemGen({ theme = "light" }) {
  const [allowed, setAllowed] = useState(null);
  const [tab, setTab] = useState("gen");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  // ── 생성 폼 ──
  const [f, setF] = useState({ model: "sonnet", testType: "concept_set", unit: "m1-1",
    qtypes: ["choice", "short"], count: 5, difficulty: "2~3", latex: false, withSolution: false,
    refText: "", extra: "" });
  const [concepts, setConcepts] = useState([]);       // {id,title} of unit
  const [selC, setSelC] = useState([]);               // 선택 개념 id
  const [out, setOut] = useState(null);               // { items, excl:Set }
  const [editI, setEditI] = useState(null);           // 수정 중 index
  const [editTxt, setEditTxt] = useState("");

  // ── 풀이 탭 ──
  const [sf, setSf] = useState({ model: "opus", testType: "", unit: "" });
  const [pool, setPool] = useState(null);             // solution 없는 문항들
  const [selP, setSelP] = useState(new Set());
  const [sOut, setSOut] = useState(null);

  // ── JSON 등록 탭 ──
  const [regTxt, setRegTxt] = useState("");
  const [regSrc, setRegSrc] = useState("gen:fable");
  const [regOut, setRegOut] = useState(null);          // { items, excl:Set }

  useEffect(() => {
    (async () => {
      const { data: { user } } = await supabase.auth.getUser();
      const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).maybeSingle();
      setAllowed(prof?.role === "admin");
    })();
  }, []);

  useEffect(() => {
    (async () => {
      const { data } = await supabase.from("concepts").select("id, title")
        .like("id", f.unit + "-%").order("id");
      setConcepts(data || []); setSelC([]);
    })();
  }, [f.unit]);

  const authFetch = async (body) => {
    const { data: sess } = await supabase.auth.getSession();
    const token = sess?.session?.access_token;
    if (!token) throw new Error("로그인 세션이 없어요");
    const res = await fetch("/api/genItems", {
      method: "POST",
      headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
      body: JSON.stringify(body),
    });
    const j = await res.json();
    if (!res.ok) throw new Error(j?.error || `호출 실패 (${res.status})`);
    return j;
  };

  /* ══ 탭 ①: 문항 생성 ══ */
  const gen = async () => {
    if (busy) return; setBusy(true); setMsg(""); setOut(null);
    try {
      const titles = concepts.filter((c) => selC.includes(c.id)).map((c) => c.title);
      const j = await authFetch({ mode: "items", model: f.model, testType: f.testType,
        unitId: f.unit, unitName: UNIT_NAME[f.unit], conceptIds: selC, conceptTitles: titles,
        qtypes: f.qtypes.join(", "), count: f.count, difficulty: f.difficulty,
        latex: f.latex, withSolution: f.withSolution, refText: f.refText, extra: f.extra });
      const excl = new Set();
      j.items.forEach((it, i) => { if ((it._warns || []).length) excl.add(i); });
      setOut({ items: j.items, excl });
      setMsg(`생성 ${j.items.length}건 · 자동 제외(경고) ${excl.size}건 · 파손 폐기 ${j.dropped}건`);
    } catch (e) { setMsg("⚠ " + e.message); }
    setBusy(false);
  };
  const saveGen = async () => {
    if (!out || busy) return;
    const list = out.items.filter((_, i) => !out.excl.has(i));
    if (!list.length) { setMsg("⚠ 저장할 문항이 없어요"); return; }
    setBusy(true);
    try {
      const rows = list.map((it) => ({
        test_type: f.testType, unit_id: f.unit, concept_ids: selC,
        qtype: it.qtype, difficulty: it.difficulty, question: it.question,
        choices: it.choices || null, answer: String(it.answer),
        answer_alt: it.answer_alt || [], points: it.points, time_limit: it.time_limit,
        tags: it.tags || [], solution: it.solution || null,
        source: "gen:" + f.model, status: "draft",
        gen_meta: { latex: f.latex, difficulty_req: f.difficulty },
      }));
      const { error } = await supabase.from("test_items").insert(rows);
      if (error) throw error;
      setMsg(`✅ ${rows.length}문항 저장(draft) 완료`); setOut(null);
    } catch (e) { setMsg("⚠ 저장 실패: " + e.message); }
    setBusy(false);
  };
  const applyEdit = () => {
    try {
      const v = JSON.parse(editTxt);
      setOut((o) => ({ ...o, items: o.items.map((it, i) => i === editI ? { ...v, _warns: [] } : it) }));
      setEditI(null);
    } catch { setMsg("⚠ JSON 형식이 아니에요"); }
  };

  /* ══ 탭 ②: 풀이 붙이기 ══ */
  const loadPool = async () => {
    setBusy(true); setMsg(""); setSOut(null); setSelP(new Set());
    let q = supabase.from("test_items").select("*").is("solution", null)
      .order("created_at", { ascending: false }).limit(20);
    if (sf.testType) q = q.eq("test_type", sf.testType);
    if (sf.unit) q = q.eq("unit_id", sf.unit);
    const { data, error } = await q;
    if (error) setMsg("⚠ " + error.message); else setPool(data || []);
    setBusy(false);
  };
  const genSol = async () => {
    const ids = [...selP]; if (!ids.length || busy) return;
    setBusy(true); setMsg(""); setSOut(null);
    try {
      const items = pool.filter((p) => selP.has(p.id)).map((p) => ({
        id: p.id, qtype: p.qtype, question: p.question, choices: p.choices,
        answer: p.answer, difficulty: p.difficulty }));
      const j = await authFetch({ mode: "solutions", model: sf.model, latex: true, items });
      setSOut(j.items); setMsg(`풀이 생성 ${j.items.length}건 — 확인 후 저장`);
    } catch (e) { setMsg("⚠ " + e.message); }
    setBusy(false);
  };
  const saveSol = async () => {
    if (!sOut || busy) return; setBusy(true);
    try {
      let n = 0;
      for (const it of sOut) {
        if (!it.id || !it.solution) continue;
        const { error } = await supabase.from("test_items")
          .update({ solution: it.solution, source: undefined }).eq("id", it.id);
        if (!error) n++;
      }
      setMsg(`✅ 풀이 ${n}건 저장 완료`); setSOut(null); loadPool();
    } catch (e) { setMsg("⚠ " + e.message); }
    setBusy(false);
  };

  /* ══ 탭 ③: JSON 등록 ══ */
  const regParse = () => {
    setMsg(""); setRegOut(null);
    try {
      let t = regTxt.trim().replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "");
      let arr = JSON.parse(t);
      if (!Array.isArray(arr)) arr = [arr];
      const items = []; const excl = new Set();
      arr.forEach((it) => {
        if (!it || typeof it.question !== "string" || !it.question.trim()) return;
        const warns = [];
        if (!["choice","short","ox","proof","essay"].includes(it.qtype)) { it.qtype = "short"; warns.push("qtype 보정"); }
        if (it.qtype === "choice") {
          if (!Array.isArray(it.choices) || it.choices.length !== 5) warns.push("보기 5개 아님");
          else if (it.choices.filter((c) => String(c) === String(it.answer)).length !== 1) warns.push("answer≠보기");
        } else it.choices = null;
        if (it.answer == null || String(it.answer).trim() === "") warns.push("answer 없음");
        const blob = JSON.stringify(it);
        if (((blob.match(/\$/g) || []).length) % 2 === 1) warns.push("$ 짝 안 맞음");
        items.push({ ...it, answer_alt: it.answer_alt || [], tags: it.tags || [],
          points: it.points || 4, difficulty: it.difficulty || 2,
          time_limit: it.time_limit ?? null, solution: it.solution || null, _warns: warns });
        if (warns.length) excl.add(items.length - 1);
      });
      if (!items.length) { setMsg("⚠ 읽을 수 있는 문항이 없어요"); return; }
      setRegOut({ items, excl });
      setMsg(`불러오기 ${items.length}건 · 경고 자동 제외 ${excl.size}건 — 종류·단원·개념을 확인하고 저장하세요`);
    } catch { setMsg("⚠ JSON 형식이 아니에요 (배열인지, 따옴표·쉼표 확인)"); }
  };
  const saveReg = async () => {
    if (!regOut || busy) return;
    const list = regOut.items.filter((_, i) => !regOut.excl.has(i));
    if (!list.length) { setMsg("⚠ 저장할 문항이 없어요"); return; }
    setBusy(true);
    try {
      const rows = list.map((it) => ({
        test_type: f.testType, unit_id: f.unit, concept_ids: selC,
        qtype: it.qtype, difficulty: it.difficulty, question: it.question,
        choices: it.choices || null, answer: String(it.answer),
        answer_alt: it.answer_alt || [], points: it.points, time_limit: it.time_limit,
        tags: it.tags || [], solution: it.solution || null,
        source: regSrc, status: "draft", gen_meta: { via: "json-paste" },
      }));
      const { error } = await supabase.from("test_items").insert(rows);
      if (error) throw error;
      setMsg(`✅ ${rows.length}문항 저장(draft) 완료`); setRegOut(null); setRegTxt("");
    } catch (e) { setMsg("⚠ 저장 실패: " + e.message); }
    setBusy(false);
  };

  if (allowed === false) return (
    <div className={`ig-root ig-${theme}`}><style>{CSS}</style>
      <p style={{ color: "var(--mut)", textAlign: "center", paddingTop: 40 }}>관리자 전용 화면입니다.</p></div>
  );

  return (
    <div className={`ig-root ig-${theme}`}>
      <style>{CSS}</style>
      <div className="ig-wrap">
        <div className="ig-top">
          <h1 className="ig-h">🧪 테스트 문항 생성기</h1>
          <span className="ig-back" onClick={() => (location.hash = "")}>← 홈</span>
        </div>
        <div className="ig-tabs">
          <button className={"ig-tab" + (tab === "gen" ? " on" : "")} onClick={() => setTab("gen")}>① 문항 생성</button>
          <button className={"ig-tab" + (tab === "sol" ? " on" : "")} onClick={() => { setTab("sol"); if (!pool) loadPool(); }}>② 풀이 붙이기</button>
          <button className={"ig-tab" + (tab === "reg" ? " on" : "")} onClick={() => setTab("reg")}>③ JSON 등록</button>
        </div>

        {tab === "gen" && (
          <>
            <div className="ig-card">
              <p className="ig-lab">모델 · 테스트 종류</p>
              <div className="ig-row">
                <select className="ig-sel" value={f.model} onChange={(e) => setF((s) => ({ ...s, model: e.target.value }))}>
                  {MODEL_OPT.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
                <select className="ig-sel" value={f.testType} onChange={(e) => setF((s) => ({ ...s, testType: e.target.value }))}>
                  {TEST_OPT.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
                <select className="ig-sel" value={f.unit} onChange={(e) => setF((s) => ({ ...s, unit: e.target.value }))}>
                  {Object.entries(UNIT_NAME).map(([u, n]) => <option key={u} value={u}>{n}</option>)}
                </select>
              </div>
              <p className="ig-lab">개념 범위 (선택 없으면 단원 전체 기준)</p>
              <div className="ig-row">
                {concepts.map((c) => (
                  <button key={c.id} className={"ig-chip" + (selC.includes(c.id) ? " on" : "")}
                    onClick={() => setSelC((s) => s.includes(c.id) ? s.filter((x) => x !== c.id) : [...s, c.id])}>
                    {c.id.split("-").pop()} {c.title}</button>
                ))}
              </div>
              <p className="ig-lab">문항형 · 개수 · 난이도</p>
              <div className="ig-row">
                {QT_OPT.map(([v, l]) => (
                  <button key={v} className={"ig-chip" + (f.qtypes.includes(v) ? " on" : "")}
                    onClick={() => setF((s) => ({ ...s, qtypes: s.qtypes.includes(v) ? s.qtypes.filter((x) => x !== v) : [...s.qtypes, v] }))}>{l}</button>
                ))}
                <select className="ig-sel" value={f.count} onChange={(e) => setF((s) => ({ ...s, count: +e.target.value }))}>
                  {[3, 5, 8, 10].map((n) => <option key={n} value={n}>{n}문항</option>)}
                </select>
                <input className="ig-sel" style={{ width: 90 }} value={f.difficulty}
                  onChange={(e) => setF((s) => ({ ...s, difficulty: e.target.value }))} placeholder="난이도 2~3" />
              </div>
              <div className="ig-row" style={{ marginTop: 8 }}>
                <button className={"ig-chip" + (f.latex ? " on" : "")}
                  onClick={() => setF((s) => ({ ...s, latex: !s.latex }))}>고급 수식 $LaTeX$ 허용</button>
                <button className={"ig-chip" + (f.withSolution ? " on" : "")}
                  onClick={() => setF((s) => ({ ...s, withSolution: !s.withSolution }))}>풀이 동시 생성</button>
              </div>
              <p className="ig-lab">참고 자료 발췌 (자료실 문서에서 복사 — 유형·범위 기준)</p>
              <textarea className="ig-ta" value={f.refText} onChange={(e) => setF((s) => ({ ...s, refText: e.target.value }))}
                placeholder="예: 스피드 문제 PDF의 해당 단원 문항 몇 개, 또는 개념서 요점" />
              <p className="ig-lab">추가 지시 (선택)</p>
              <input className="ig-inp" value={f.extra} onChange={(e) => setF((s) => ({ ...s, extra: e.target.value }))}
                placeholder="예: 분수 계수 포함, 도형 문제 제외" />
              <div className="ig-row" style={{ marginTop: 12 }}>
                <button className="ig-btn ig-ok" disabled={busy} onClick={gen}>{busy ? "생성 중…" : "⚡ 생성"}</button>
                {out && <button className="ig-btn ig-ghost" disabled={busy} onClick={saveGen}>
                  💾 저장 ({out.items.length - out.excl.size}건 → draft)</button>}
              </div>
              {msg && <p className={msg.startsWith("⚠") ? "ig-warn" : "ig-sum"} style={{ marginTop: 8 }}>{msg}</p>}
            </div>

            {out && out.items.map((it, i) => editI === i ? (
              <div key={i} className="ig-card">
                <textarea className="ig-ta" style={{ minHeight: 180 }} value={editTxt}
                  onChange={(e) => setEditTxt(e.target.value)} />
                <div className="ig-row" style={{ marginTop: 8 }}>
                  <button className="ig-btn ig-ok" onClick={applyEdit}>적용</button>
                  <button className="ig-btn ig-ghost" onClick={() => setEditI(null)}>취소</button>
                </div>
              </div>
            ) : (
              <ItemCard key={i} it={it} off={out.excl.has(i)}
                onToggle={() => setOut((o) => { const e = new Set(o.excl); e.has(i) ? e.delete(i) : e.add(i); return { ...o, excl: e }; })}
                onEdit={() => { setEditI(i); setEditTxt(JSON.stringify({ ...it, _warns: undefined }, null, 2)); }} />
            ))}
          </>
        )}

        {tab === "sol" && (
          <>
            <div className="ig-card">
              <p className="ig-lab">대상 필터 · 모델</p>
              <div className="ig-row">
                <select className="ig-sel" value={sf.testType} onChange={(e) => setSf((s) => ({ ...s, testType: e.target.value }))}>
                  <option value="">전체 종류</option>
                  {TEST_OPT.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
                <select className="ig-sel" value={sf.unit} onChange={(e) => setSf((s) => ({ ...s, unit: e.target.value }))}>
                  <option value="">전체 단원</option>
                  {Object.entries(UNIT_NAME).map(([u, n]) => <option key={u} value={u}>{n}</option>)}
                </select>
                <select className="ig-sel" value={sf.model} onChange={(e) => setSf((s) => ({ ...s, model: e.target.value }))}>
                  <option value="opus">오푸스</option><option value="fable">페이블</option>
                </select>
                <button className="ig-btn ig-ghost" disabled={busy} onClick={loadPool}>🔄 풀이 없는 문항 불러오기</button>
              </div>
              {pool && <p className="ig-sum" style={{ marginTop: 8 }}>대상 {pool.length}건 — 카드를 눌러 선택 (한 번에 최대 10건)</p>}
              <div className="ig-row" style={{ marginTop: 8 }}>
                <button className="ig-btn ig-ok" disabled={busy || !selP.size} onClick={genSol}>
                  {busy ? "생성 중…" : `⚡ 풀이 생성 (${selP.size}건)`}</button>
                {sOut && <button className="ig-btn ig-ghost" disabled={busy} onClick={saveSol}>💾 풀이 저장</button>}
              </div>
              {msg && <p className={msg.startsWith("⚠") ? "ig-warn" : "ig-sum"} style={{ marginTop: 8 }}>{msg}</p>}
            </div>
            {sOut ? sOut.map((it, i) => <ItemCard key={i} it={it} />)
              : (pool || []).map((p) => (
                <div key={p.id} onClick={() => setSelP((s) => { const n = new Set(s);
                  n.has(p.id) ? n.delete(p.id) : n.size < 10 && n.add(p.id); return n; })}
                  style={{ cursor: "pointer", outline: selP.has(p.id) ? "2px solid var(--ac)" : "none",
                    borderRadius: 14, marginBottom: 10 }}>
                  <ItemCard it={p} />
                </div>
              ))}
          </>
        )}

        {tab === "reg" && (
          <>
            <div className="ig-card">
              <p className="ig-lab">등록 메타 — 종류 · 단원 · 개념 · 출처</p>
              <div className="ig-row">
                <select className="ig-sel" value={f.testType} onChange={(e) => setF((s) => ({ ...s, testType: e.target.value }))}>
                  {TEST_OPT.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
                <select className="ig-sel" value={f.unit} onChange={(e) => setF((s) => ({ ...s, unit: e.target.value }))}>
                  {Object.entries(UNIT_NAME).map(([u, n]) => <option key={u} value={u}>{n}</option>)}
                </select>
                <select className="ig-sel" value={regSrc} onChange={(e) => setRegSrc(e.target.value)}>
                  <option value="gen:fable">출처: 페이블</option><option value="md:haiku">출처: 하이쿠 방</option>
                  <option value="md:sonnet">출처: 소넷 방</option><option value="md:opus">출처: 오푸스 방</option>
                  <option value="manual">출처: 직접 작성</option>
                </select>
              </div>
              <div className="ig-row" style={{ marginTop: 6 }}>
                {concepts.map((c) => (
                  <button key={c.id} className={"ig-chip" + (selC.includes(c.id) ? " on" : "")}
                    onClick={() => setSelC((s) => s.includes(c.id) ? s.filter((x) => x !== c.id) : [...s, c.id])}>
                    {c.id.split("-").pop()} {c.title}</button>
                ))}
              </div>
              <p className="ig-lab">문항 JSON 배열 붙여넣기</p>
              <textarea className="ig-ta" style={{ minHeight: 140 }} value={regTxt}
                onChange={(e) => setRegTxt(e.target.value)} placeholder='[ { "qtype": "short", ... }, ... ]' />
              <div className="ig-row" style={{ marginTop: 10 }}>
                <button className="ig-btn ig-ok" disabled={busy || !regTxt.trim()} onClick={regParse}>🔎 불러오기</button>
                {regOut && <button className="ig-btn ig-ghost" disabled={busy} onClick={saveReg}>
                  💾 저장 ({regOut.items.length - regOut.excl.size}건 → draft)</button>}
              </div>
              {msg && <p className={msg.startsWith("⚠") ? "ig-warn" : "ig-sum"} style={{ marginTop: 8 }}>{msg}</p>}
            </div>
            {regOut && regOut.items.map((it, i) => (
              <ItemCard key={i} it={it} off={regOut.excl.has(i)}
                onToggle={() => setRegOut((o) => { const e = new Set(o.excl); e.has(i) ? e.delete(i) : e.add(i); return { ...o, excl: e }; })} />
            ))}
          </>
        )}
      </div>
    </div>
  );
}
