import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { GEN_UNITS, generateProblems } from "../lib/calcGen";
import AdminMaterials from "./AdminMaterials";

// ashrain.out — 연산 관리 (v0.3.0)
// [v0.3.0] 📄 자료 탭 추가 — 문제 PDF를 AI가 분해해 자료 등록 (AdminMaterials.jsx, api/ai.js 필요)
// src/components/AdminCalc.jsx — Calc.jsx의 🛠 관리자 화면에서 사용.
// [v0.2.3 변경] 🤖 AI 생성 탭 추가: 문제지 PDF → 페이지 골라(최대 3장) 이미지 전송 →
//   AI가 유형 분석 후 "신규" 문항 생성 → 미리보기에서 항목별 제외 → 등록 (origin: ai)
//   서버: 레포 최상단 api/genCalc.js + Vercel 환경변수 ANTHROPIC_API_KEY 필요
// ① 파일 등록 ② 규칙 생성(calcGen.js) ③ AI 생성 ④ 관리

const CHUNK = 500;
const TYPES = ["calc", "ox", "choice"];
const GEN_COUNTS = [50, 100, 200, 500];
const AI_COUNTS = [10, 20, 30];
const PDFJS = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174";

let pdfjsReady = null;
function loadPdfJs() {
  if (window.pdfjsLib) return Promise.resolve(window.pdfjsLib);
  if (pdfjsReady) return pdfjsReady;
  pdfjsReady = new Promise((res, rej) => {
    const s = document.createElement("script");
    s.src = `${PDFJS}/pdf.min.js`;
    s.onload = () => {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = `${PDFJS}/pdf.worker.min.js`;
      res(window.pdfjsLib);
    };
    s.onerror = () => rej(new Error("pdf.js 로드 실패 — 네트워크를 확인해 주세요"));
    document.head.appendChild(s);
  });
  return pdfjsReady;
}

const CSS = `
.ac-tabs { display:flex; gap:6px; margin-bottom:14px; }
.ac-tab { flex:1; padding:9px 0; border-radius:10px; border:1px solid var(--bd); background:var(--card);
  color:var(--mut); font-size:12px; cursor:pointer; }
.ac-tab.on { color:var(--ac); border-color:var(--ac); font-weight:800; }
.ac-box { background:var(--card); border:1px solid var(--bd); border-radius:12px; padding:14px; margin-bottom:10px; }
.ac-file { display:block; width:100%; box-sizing:border-box; padding:22px 12px; border:1.5px dashed var(--bd);
  border-radius:12px; background:transparent; color:var(--mut); font-size:13.5px; text-align:center; cursor:pointer; }
.ac-mini { font-size:12.5px; color:var(--mut); line-height:1.7; margin:8px 0 0; }
.ac-err { border:1px solid #E5484D; border-radius:10px; padding:10px 12px; margin-top:10px; }
.ac-err p { margin:0 0 4px; font-size:12.5px; color:#E5484D; }
.ac-ok { font-size:13px; color:var(--ink); margin:0 0 6px; }
.ac-row { display:flex; justify-content:space-between; align-items:center; padding:9px 2px;
  border-bottom:1px solid var(--bd); font-size:13.5px; color:var(--ink); gap:8px; }
.ac-row:last-child { border-bottom:none; }
.ac-row span { color:var(--mut); font-size:12.5px; white-space:nowrap; }
.ac-sample { font-size:12.5px; color:var(--mut); line-height:1.7; margin:4px 0 0; white-space:pre-line; word-break:keep-all; }
.ac-go { width:100%; padding:12px; border-radius:11px; border:1px solid var(--ac); background:transparent;
  color:var(--ac); font-weight:800; font-size:14px; cursor:pointer; margin-top:10px; }
.ac-go:disabled { opacity:.45; cursor:default; }
.ac-bar { height:8px; border-radius:999px; background:var(--bd); overflow:hidden; margin-top:10px; }
.ac-fill { height:100%; background:var(--ac); transition:width .25s; }
.ac-del { border:1px solid var(--bd); background:transparent; color:var(--mut); border-radius:8px;
  padding:6px 10px; font-size:12px; cursor:pointer; white-space:nowrap; }
.ac-del.arm { border-color:#E5484D; color:#E5484D; font-weight:800; }
.ac-empty { color:var(--mut); font-size:13px; text-align:center; padding:22px 0; }
.ac-sec { font-size:12.5px; color:var(--mut); font-weight:700; margin:10px 0 6px; }
.ac-chips { display:flex; flex-wrap:wrap; gap:6px; }
.ac-chip { border:1px solid var(--bd); background:var(--card); color:var(--mut); border-radius:999px;
  padding:7px 12px; font-size:12.5px; cursor:pointer; }
.ac-chip.on { color:var(--ac); border-color:var(--ac); font-weight:800; }
.ac-thumbs { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
.ac-th { position:relative; border:2px solid var(--bd); border-radius:8px; padding:0; background:none; cursor:pointer; }
.ac-th img { display:block; width:74px; border-radius:6px; }
.ac-th.on { border-color:var(--ac); }
.ac-th i { position:absolute; top:2px; right:4px; font-style:normal; font-size:11px; color:var(--ac); font-weight:800; }
.ac-th b { position:absolute; bottom:2px; left:5px; font-size:10.5px; color:var(--mut); }
.ac-item { border:1px solid var(--bd); border-radius:11px; padding:10px 12px; margin-bottom:8px; }
.ac-item.off { opacity:.4; }
.ac-item p { margin:0; font-size:13px; color:var(--ink); white-space:pre-line; word-break:keep-all; line-height:1.6; }
.ac-item small { display:block; color:var(--mut); font-size:12px; margin-top:4px; line-height:1.6; }
.ac-item .warn { color:#E5484D; }
.ac-ex { margin-top:6px; border:1px solid var(--bd); background:transparent; color:var(--mut);
  border-radius:7px; padding:4px 9px; font-size:11.5px; cursor:pointer; }
`;

export default function AdminCalc({ say }) {
  const [tab, setTab] = useState("file");           // file | gen | ai | manage
  // 파일 등록
  const [parsed, setParsed] = useState(null);
  const [errors, setErrors] = useState([]);
  // 공용 업로드
  const [busy, setBusy] = useState(false);
  const [prog, setProg] = useState(null);
  // 규칙 생성
  const [genUnit, setGenUnit] = useState(null);
  const [genCount, setGenCount] = useState(100);
  const [genOut, setGenOut] = useState(null);
  // AI 생성
  const [dbUnits, setDbUnits] = useState(null);
  const [aiUnit, setAiUnit] = useState(null);
  const [aiCount, setAiCount] = useState(20);
  const [aiName, setAiName] = useState(null);
  const [thumbs, setThumbs] = useState([]);
  const [thumbProg, setThumbProg] = useState(null);
  const [aiSel, setAiSel] = useState([]);
  const [aiOut, setAiOut] = useState(null);         // {problems, excl:Set, model, dropped}
  const docRef = useRef(null);
  const fileTokenRef = useRef(0);
  // 관리
  const [rows, setRows] = useState(null);
  const [armId, setArmId] = useState(null);

  useEffect(() => { if (tab === "manage") loadManage(); }, [tab]);
  useEffect(() => {
    if ((tab === "ai" || tab === "gen") && dbUnits === null)
      supabase.from("calc_units").select("*").order("sort").then(({ data }) => setDbUnits(data || []));
  }, [tab, dbUnits]);

  async function loadManage() {
    setRows(null);
    const { data: us, error } = await supabase.from("calc_units").select("*").order("sort");
    if (error) { say("유닛 로드 실패: " + error.message); setRows([]); return; }
    const out = [];
    for (const u of us || []) {
      const { count } = await supabase.from("calc_problems")
        .select("id", { count: "exact", head: true }).eq("calc_unit", u.id);
      out.push({ unit: u, count: count ?? 0 });
    }
    setRows(out);
  }

  async function upsertProblems(pRows) {
    setProg({ done: 0, total: pRows.length });
    for (let i = 0; i < pRows.length; i += CHUNK) {
      const { error } = await supabase.from("calc_problems")
        .upsert(pRows.slice(i, i + CHUNK), { onConflict: "id" });
      if (error) throw new Error(`문항 등록 실패 (${i + 1}번째~): ` + error.message);
      setProg({ done: Math.min(i + CHUNK, pRows.length), total: pRows.length });
    }
  }

  // ══════════ ① 파일 등록 ══════════
  async function onFile(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    setParsed(null); setErrors([]); setProg(null);
    let obj;
    try { obj = JSON.parse(await f.text()); }
    catch (err) { setErrors(["JSON 파싱 실패: " + err.message]); return; }

    const errs = [];
    const units = Array.isArray(obj.units) ? obj.units : [];
    const problems = Array.isArray(obj.problems) ? obj.problems : [];
    if (!units.length && !problems.length) errs.push("units / problems 배열이 없습니다");

    const { data: exist } = await supabase.from("calc_units").select("id");
    const known = new Set([...(exist || []).map((u) => u.id), ...units.map((u) => u.id)]);

    units.forEach((u, i) => {
      if (!u.id || !u.name || !u.grade || !u.unitId || u.sort == null)
        errs.push(`units[${i}] 필수 필드(id·name·grade·unitId·sort) 누락`);
    });
    const seen = new Set();
    problems.forEach((p, i) => {
      const tag = `problems[${i}]${p.id ? ` (${p.id})` : ""}`;
      if (!p.id) errs.push(`${tag} id 없음`);
      else if (seen.has(p.id)) errs.push(`${tag} id 중복`);
      seen.add(p.id);
      if (!known.has(p.unitId)) errs.push(`${tag} unitId '${p.unitId}' — 이 파일/DB에 없는 유닛`);
      if (!TYPES.includes(p.type)) errs.push(`${tag} type '${p.type}' 오류`);
      if (!p.question || p.answer == null || p.answer === "") errs.push(`${tag} question/answer 누락`);
      if (p.type === "choice" && (!Array.isArray(p.choices) || p.choices.length !== 5))
        errs.push(`${tag} choice인데 보기 5개가 아님`);
      if (![1, 2, 3].includes(p.difficulty)) errs.push(`${tag} difficulty는 1~3`);
      if (!(p.timeLimit > 0)) errs.push(`${tag} timeLimit > 0 필요`);
    });

    if (errs.length) { setErrors(errs); return; }
    setParsed({ units, problems, fileName: f.name });
  }

  async function registerFile() {
    if (!parsed || busy) return;
    setBusy(true);
    try {
      if (parsed.units.length) {
        const uRows = parsed.units.map((u) => ({
          id: u.id, name: u.name, grade: u.grade, unit_id: u.unitId, sort: u.sort,
        }));
        const { error } = await supabase.from("calc_units").upsert(uRows, { onConflict: "id" });
        if (error) throw new Error("유닛 등록 실패: " + error.message);
      }
      const pRows = parsed.problems.map((p) => ({
        id: p.id, calc_unit: p.unitId, type: p.type, question: p.question,
        answer: String(p.answer), choices: p.choices || null,
        difficulty: p.difficulty, time_limit: p.timeLimit, origin: "rule",
      }));
      await upsertProblems(pRows);
      say(`✅ 등록 완료 — 유닛 ${parsed.units.length}개 · 문항 ${pRows.length}개`);
      setParsed(null); setProg(null);
    } catch (err) { say(err.message); }
    setBusy(false);
  }

  // ══════════ ② 규칙 생성 ══════════
  async function runGenerate() {
    if (!genUnit || busy) return;
    setBusy(true); setGenOut(null); setProg(null);
    try {
      const { data: exist, error } = await supabase.from("calc_problems")
        .select("id, question, choices").eq("calc_unit", genUnit);
      if (error) throw new Error("기존 문제 조회 실패: " + error.message);
      await new Promise((r) => setTimeout(r, 30));
      const out = generateProblems(genUnit, genCount, Date.now(), exist || []);
      if (out.error) throw new Error(out.error);
      setGenOut(out);
      if (out.problems.length < out.requested)
        say(`중복 제외 후 ${out.problems.length}개가 만들어졌어요 (요청 ${out.requested}개)`);
    } catch (err) { say(err.message); }
    setBusy(false);
  }

  async function registerGen() {
    if (!genOut?.problems?.length || busy) return;
    setBusy(true);
    try {
      const pRows = genOut.problems.map((p) => ({
        id: p.id, calc_unit: p.unitId, type: p.type, question: p.question,
        answer: String(p.answer), choices: p.choices || null,
        difficulty: p.difficulty, time_limit: p.timeLimit, origin: "rule",
      }));
      await upsertProblems(pRows);
      say(`✅ ${pRows.length}문항을 ${genUnit} 유닛에 추가했어요`);
      setGenOut(null); setProg(null);
    } catch (err) { say(err.message); }
    setBusy(false);
  }

  const genStats = genOut ? (() => {
    const t = { calc: 0, ox: 0, choice: 0 }, d = { 1: 0, 2: 0, 3: 0 };
    genOut.problems.forEach((p) => { t[p.type]++; d[p.difficulty]++; });
    return { t, d };
  })() : null;

  // ══════════ ③ AI 생성 ══════════
  async function onAiPdf(e) {
    const f = e.target.files?.[0];
    e.target.value = "";
    if (!f) return;
    const token = ++fileTokenRef.current;
    setAiName(f.name); setThumbs([]); setAiSel([]); setAiOut(null); setThumbProg({ done: 0, total: 0 });
    try {
      const pdfjs = await loadPdfJs();
      const buf = await f.arrayBuffer();
      const doc = await pdfjs.getDocument({ data: buf }).promise;
      if (token !== fileTokenRef.current) return;
      docRef.current = doc;
      setThumbProg({ done: 0, total: doc.numPages });
      for (let i = 1; i <= doc.numPages; i++) {
        if (token !== fileTokenRef.current) return;
        const page = await doc.getPage(i);
        const vp0 = page.getViewport({ scale: 1 });
        const vp = page.getViewport({ scale: 74 / vp0.width });
        const cv = document.createElement("canvas");
        cv.width = vp.width; cv.height = vp.height;
        await page.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
        const url = cv.toDataURL("image/jpeg", 0.6);
        setThumbs((t) => [...t, { n: i, url }]);
        setThumbProg({ done: i, total: doc.numPages });
      }
    } catch (err) { say("PDF 열기 실패: " + err.message); setAiName(null); }
  }

  function toggleSel(n) {
    setAiSel((s) => s.includes(n) ? s.filter((x) => x !== n)
      : s.length >= 3 ? (say("페이지는 최대 3장까지 보낼 수 있어요"), s) : [...s, n]);
  }

  async function renderFull(n) {
    const page = await docRef.current.getPage(n);
    const vp0 = page.getViewport({ scale: 1 });
    const vp = page.getViewport({ scale: 1200 / vp0.width });
    const cv = document.createElement("canvas");
    cv.width = vp.width; cv.height = vp.height;
    await page.render({ canvasContext: cv.getContext("2d"), viewport: vp }).promise;
    let url = cv.toDataURL("image/jpeg", 0.8);
    if (url.length > 950000) url = cv.toDataURL("image/jpeg", 0.6);
    return url.split(",")[1];
  }

  async function callAi() {
    if (!aiUnit || aiSel.length === 0 || busy) return;
    setBusy(true); setAiOut(null); setProg(null);
    try {
      const { data: sess } = await supabase.auth.getSession();
      const token = sess?.session?.access_token;
      if (!token) throw new Error("로그인 세션이 없어요");
      const pages = [];
      for (const n of [...aiSel].sort((a, b) => a - b)) pages.push(await renderFull(n));
      const unitRow = (dbUnits || []).find((u) => u.id === aiUnit);
      const res = await fetch("/api/genCalc", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${token}` },
        body: JSON.stringify({ pages, unitId: aiUnit, unitName: unitRow?.name, count: aiCount }),
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.error || `호출 실패 (${res.status})`);
      // 클라이언트 구조 검증 → 경고 항목은 기본 제외
      const excl = new Set();
      (json.problems || []).forEach((p, i) => {
        const bad =
          (p.type === "choice" && (!p.choices || p.choices.filter((c) => c === p.answer).length !== 1)) ||
          /−/.test(p.answer) || !p.question?.trim();
        if (bad) excl.add(i);
      });
      setAiOut({ problems: json.problems || [], excl, model: json.model, dropped: json.dropped || 0 });
      if (!json.problems?.length) say("생성된 문항이 없어요 — 페이지를 바꿔 다시 시도해 보세요");
    } catch (err) { say(err.message); }
    setBusy(false);
  }

  function toggleExcl(i) {
    setAiOut((o) => {
      const excl = new Set(o.excl);
      excl.has(i) ? excl.delete(i) : excl.add(i);
      return { ...o, excl };
    });
  }

  async function registerAi() {
    if (!aiOut || busy) return;
    const list = aiOut.problems.filter((_, i) => !aiOut.excl.has(i));
    if (!list.length) { say("등록할 문항이 없어요"); return; }
    setBusy(true);
    try {
      const stamp = Date.now().toString(36);
      const pRows = list.map((p, i) => ({
        id: `${aiUnit}-ai${stamp}-${String(i + 1).padStart(2, "0")}`,
        calc_unit: aiUnit, type: p.type, question: p.question,
        answer: String(p.answer), choices: p.choices || null,
        difficulty: p.difficulty, time_limit: p.timeLimit, origin: "ai",
      }));
      await upsertProblems(pRows);
      say(`✅ AI 생성 ${pRows.length}문항을 등록했어요`);
      setAiOut(null); setProg(null);
    } catch (err) { say(err.message); }
    setBusy(false);
  }

  async function delUnit(id) {
    if (armId !== id) { setArmId(id); setTimeout(() => setArmId((v) => (v === id ? null : v)), 3000); return; }
    setArmId(null);
    const { error } = await supabase.from("calc_units").delete().eq("id", id);
    if (error) { say("삭제 실패: " + error.message); return; }
    say("유닛과 문제를 삭제했어요");
    loadManage();
  }

  const summary = parsed ? (() => {
    const byUnit = {};
    parsed.problems.forEach((p) => { byUnit[p.unitId] = (byUnit[p.unitId] || 0) + 1; });
    return Object.entries(byUnit);
  })() : [];
  const genGrades = [...new Set(GEN_UNITS.map((u) => u.grade))];
  const dbGrades = dbUnits ? [...new Set(dbUnits.map((u) => u.grade || "기타"))] : [];
  const aiIncluded = aiOut ? aiOut.problems.length - aiOut.excl.size : 0;

  return (
    <div>
      <style>{CSS}</style>
      <div className="ac-tabs">
        <button className={"ac-tab" + (tab === "file" ? " on" : "")} onClick={() => setTab("file")}>📂 파일</button>
        <button className={"ac-tab" + (tab === "gen" ? " on" : "")} onClick={() => setTab("gen")}>🎲 생성</button>
        <button className={"ac-tab" + (tab === "ai" ? " on" : "")} onClick={() => setTab("ai")}>🤖 AI</button>
        <button className={"ac-tab" + (tab === "mat" ? " on" : "")} onClick={() => setTab("mat")}>📄 자료</button>
        <button className={"ac-tab" + (tab === "manage" ? " on" : "")} onClick={() => setTab("manage")}>🗂 관리</button>
      </div>

      {/* ══════════ 파일 등록 ══════════ */}
      {tab === "file" && (
        <>
          <div className="ac-box">
            <label className="ac-file">
              {parsed ? `📄 ${parsed.fileName}` : "탭해서 문제 JSON 파일 선택 (calc_problems_m1.json 등)"}
              <input type="file" accept=".json,application/json" onChange={onFile} style={{ display: "none" }} />
            </label>
            <p className="ac-mini">
              형식: {'{ units: […], problems: […] }'} — 같은 id는 덮어쓰기(upsert)라 재등록해도 안전해요.
            </p>
          </div>
          {errors.length > 0 && (
            <div className="ac-err">
              <p><b>검증 실패 — {errors.length}건</b></p>
              {errors.slice(0, 10).map((e, i) => <p key={i}>· {e}</p>)}
              {errors.length > 10 && <p>… 외 {errors.length - 10}건</p>}
            </div>
          )}
          {parsed && (
            <div className="ac-box">
              <p className="ac-ok"><b>검증 통과</b> — 유닛 {parsed.units.length}개 · 문항 {parsed.problems.length}개</p>
              {summary.map(([u, n]) => (
                <div key={u} className="ac-row"><b>{u}</b><span>{n}문항</span></div>
              ))}
              <p className="ac-sample">
                {"샘플:\n" + parsed.problems.slice(0, 3).map((p) => `· [${p.type}] ${p.question}`).join("\n")}
              </p>
              <button className="ac-go" disabled={busy} onClick={registerFile}>
                {busy ? "등록 중…" : "⬆️ 이 파일 등록하기"}
              </button>
              {prog && (
                <>
                  <div className="ac-bar"><div className="ac-fill" style={{ width: `${(prog.done / prog.total) * 100}%` }} /></div>
                  <p className="ac-mini">{prog.done} / {prog.total} 문항 업로드…</p>
                </>
              )}
            </div>
          )}
        </>
      )}

      {/* ══════════ 규칙 생성 ══════════ */}
      {tab === "gen" && (
        <>
          <div className="ac-box">
            {genGrades.map((g) => (
              <div key={g}>
                <p className="ac-sec">{g}</p>
                <div className="ac-chips">
                  {GEN_UNITS.filter((u) => u.grade === g).map((u) => (
                    <button key={u.id} className={"ac-chip" + (genUnit === u.id ? " on" : "")}
                      onClick={() => { setGenUnit(u.id); setGenOut(null); }}>{u.name}</button>
                  ))}
                </div>
              </div>
            ))}
            <p className="ac-sec">생성 개수</p>
            <div className="ac-chips">
              {GEN_COUNTS.map((n) => (
                <button key={n} className={"ac-chip" + (genCount === n ? " on" : "")}
                  onClick={() => setGenCount(n)}>{n}개</button>
              ))}
            </div>
            <button className="ac-go" disabled={!genUnit || busy} onClick={runGenerate}>
              {busy && !genOut ? "생성 중…" : "🎲 새 문항 생성하기"}
            </button>
            <p className="ac-mini">
              기존 문제와 겹치지 않게 자동으로 걸러지고, 문항 번호도 이어붙어요.
              생성 즉시 등록되는 게 아니라 아래 미리보기 확인 후 등록합니다.
            </p>
          </div>
          {genOut && (
            <div className="ac-box">
              <p className="ac-ok"><b>{genOut.problems.length}문항 생성됨</b>
                {genOut.problems.length < genOut.requested ? ` (요청 ${genOut.requested}개 중 — 중복 제외)` : ""}</p>
              <div className="ac-row"><b>유형</b>
                <span>calc {genStats.t.calc} · choice {genStats.t.choice} · ox {genStats.t.ox}</span></div>
              <div className="ac-row"><b>난이도</b>
                <span>쉬움 {genStats.d[1]} · 보통 {genStats.d[2]} · 도전 {genStats.d[3]}</span></div>
              <p className="ac-sample">
                {"샘플:\n" + genOut.problems.slice(0, 5).map((p) => `· [${p.type}] ${p.question} → ${p.answer}`).join("\n")}
              </p>
              <button className="ac-go" disabled={busy} onClick={registerGen}>
                {busy ? "등록 중…" : `⬆️ ${genOut.problems.length}문항 등록하기`}
              </button>
              {prog && (
                <>
                  <div className="ac-bar"><div className="ac-fill" style={{ width: `${(prog.done / prog.total) * 100}%` }} /></div>
                  <p className="ac-mini">{prog.done} / {prog.total} 문항 업로드…</p>
                </>
              )}
            </div>
          )}
        </>
      )}

      {/* ══════════ AI 생성 ══════════ */}
      {tab === "ai" && (
        <>
          <div className="ac-box">
            <p className="ac-sec">어느 유닛에 추가할까요?</p>
            {dbUnits === null && <p className="ac-empty">유닛 불러오는 중…</p>}
            {dbGrades.map((g) => (
              <div key={g}>
                <p className="ac-sec">{g}</p>
                <div className="ac-chips">
                  {dbUnits.filter((u) => (u.grade || "기타") === g).map((u) => (
                    <button key={u.id} className={"ac-chip" + (aiUnit === u.id ? " on" : "")}
                      onClick={() => setAiUnit(u.id)}>{u.name}</button>
                  ))}
                </div>
              </div>
            ))}
            <p className="ac-sec">생성 개수</p>
            <div className="ac-chips">
              {AI_COUNTS.map((n) => (
                <button key={n} className={"ac-chip" + (aiCount === n ? " on" : "")}
                  onClick={() => setAiCount(n)}>{n}개</button>
              ))}
            </div>
            <label className="ac-file" style={{ marginTop: 12 }}>
              {aiName ? `📄 ${aiName}` : "탭해서 문제지 PDF 선택"}
              <input type="file" accept=".pdf,application/pdf" onChange={onAiPdf} style={{ display: "none" }} />
            </label>
            {thumbProg && thumbProg.total > 0 && thumbProg.done < thumbProg.total && (
              <p className="ac-mini">페이지 준비 중… {thumbProg.done} / {thumbProg.total}</p>
            )}
            {thumbs.length > 0 && (
              <>
                <p className="ac-mini">유형이 보이는 "문제" 페이지를 최대 3장 골라 주세요 (해설 페이지 말고요).</p>
                <div className="ac-thumbs">
                  {thumbs.map((t) => (
                    <button key={t.n} className={"ac-th" + (aiSel.includes(t.n) ? " on" : "")} onClick={() => toggleSel(t.n)}>
                      <img src={t.url} alt={`p${t.n}`} />
                      <b>{t.n}</b>
                      {aiSel.includes(t.n) && <i>✓</i>}
                    </button>
                  ))}
                </div>
              </>
            )}
            <button className="ac-go" disabled={!aiUnit || aiSel.length === 0 || busy} onClick={callAi}>
              {busy && !aiOut ? "AI가 유형 분석·출제 중… (30~60초)" : `🤖 선택한 ${aiSel.length}장으로 생성하기`}
            </button>
            <p className="ac-mini">
              AI는 페이지의 "유형"만 참고해 완전히 새로운 문제를 만들어요. 원본 복제는 프롬프트로 금지되어 있어요.
            </p>
          </div>

          {aiOut && (
            <div className="ac-box">
              <p className="ac-ok"><b>{aiOut.problems.length}문항 생성됨</b> · 등록 대상 {aiIncluded}개
                {aiOut.excl.size > 0 ? ` (자동/수동 제외 ${aiOut.excl.size}개)` : ""}</p>
              <p className="ac-mini" style={{ marginTop: 0 }}>
                항목을 탭하면 제외/포함이 바뀌어요. AI 생성 문제는 등록 전에 답을 한 번 훑어봐 주세요.
              </p>
              {aiOut.problems.map((p, i) => (
                <div key={i} className={"ac-item" + (aiOut.excl.has(i) ? " off" : "")} onClick={() => toggleExcl(i)}>
                  <p>{p.question}</p>
                  <small>
                    [{p.type}] 답: {p.answer}
                    {p.choices ? ` · 보기: ${p.choices.join(" / ")}` : ""}
                    {" · 난이도 " + p.difficulty + " · " + p.timeLimit + "초"}
                  </small>
                  {aiOut.excl.has(i) && <small className="warn">제외됨 — 탭하면 다시 포함</small>}
                </div>
              ))}
              <button className="ac-go" disabled={busy || aiIncluded === 0} onClick={(e) => { e.stopPropagation(); registerAi(); }}>
                {busy ? "등록 중…" : `⬆️ ${aiIncluded}문항 등록하기 (AI 표시로 저장)`}
              </button>
              {prog && (
                <>
                  <div className="ac-bar"><div className="ac-fill" style={{ width: `${(prog.done / prog.total) * 100}%` }} /></div>
                  <p className="ac-mini">{prog.done} / {prog.total} 문항 업로드…</p>
                </>
              )}
            </div>
          )}
        </>
      )}

      {/* ══════════ 자료 등록 ══════════ */}
      {tab === "mat" && <AdminMaterials say={say} />}

      {/* ══════════ 관리 ══════════ */}
      {tab === "manage" && (
        <div className="ac-box">
          {rows === null && <p className="ac-empty">불러오는 중…</p>}
          {rows !== null && rows.length === 0 && <p className="ac-empty">등록된 유닛이 없어요</p>}
          {rows !== null && rows.map(({ unit, count }) => (
            <div key={unit.id} className="ac-row">
              <div>
                <b>{unit.name}</b>
                <span style={{ display: "block" }}>{unit.id} · {unit.grade} · {count}문항</span>
              </div>
              <button className={"ac-del" + (armId === unit.id ? " arm" : "")} onClick={() => delUnit(unit.id)}>
                {armId === unit.id ? "정말 삭제?" : "삭제"}
              </button>
            </div>
          ))}
          <p className="ac-mini">유닛을 삭제하면 그 유닛의 문제와 기록이 함께 삭제돼요(복구 불가).</p>
        </div>
      )}
    </div>
  );
}
