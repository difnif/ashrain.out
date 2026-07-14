import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 연산 관리 (v0.2.2)
// src/components/AdminCalc.jsx — Calc.jsx의 🛠 관리자 화면에서 사용.
// ① 파일 등록: calc_problems_m1.json / m2.json 업로드 → 검증 → 미리보기 → 등록(청크 upsert)
// ② 문제 관리: 유닛별 문항 수 확인 · 유닛 삭제(문제 함께 삭제)

const CHUNK = 500;
const TYPES = ["calc", "ox", "choice"];

const CSS = `
.ac-tabs { display:flex; gap:6px; margin-bottom:14px; }
.ac-tab { flex:1; padding:9px 0; border-radius:10px; border:1px solid var(--bd); background:var(--card);
  color:var(--mut); font-size:13px; cursor:pointer; }
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
`;

export default function AdminCalc({ say }) {
  const [tab, setTab] = useState("file");           // file | manage
  const [parsed, setParsed] = useState(null);       // {units, problems, fileName}
  const [errors, setErrors] = useState([]);
  const [busy, setBusy] = useState(false);
  const [prog, setProg] = useState(null);           // {done, total}
  const [rows, setRows] = useState(null);           // 관리 탭: [{unit, count}]
  const [armId, setArmId] = useState(null);         // 삭제 2단 확인 대상

  useEffect(() => { if (tab === "manage") loadManage(); }, [tab]);

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

  // ── ① 파일 선택 → 파싱·검증 ──
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

  // ── ② 등록 (upsert, 500행 청크) ──
  async function register() {
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
      setProg({ done: 0, total: pRows.length });
      for (let i = 0; i < pRows.length; i += CHUNK) {
        const { error } = await supabase.from("calc_problems")
          .upsert(pRows.slice(i, i + CHUNK), { onConflict: "id" });
        if (error) throw new Error(`문항 등록 실패 (${i + 1}번째~): ` + error.message);
        setProg({ done: Math.min(i + CHUNK, pRows.length), total: pRows.length });
      }
      say(`✅ 등록 완료 — 유닛 ${parsed.units.length}개 · 문항 ${pRows.length}개`);
      setParsed(null); setProg(null);
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

  // 미리보기 요약
  const summary = parsed ? (() => {
    const byUnit = {};
    parsed.problems.forEach((p) => { byUnit[p.unitId] = (byUnit[p.unitId] || 0) + 1; });
    return Object.entries(byUnit);
  })() : [];

  return (
    <div>
      <style>{CSS}</style>
      <div className="ac-tabs">
        <button className={"ac-tab" + (tab === "file" ? " on" : "")} onClick={() => setTab("file")}>📂 파일 등록</button>
        <button className={"ac-tab" + (tab === "manage" ? " on" : "")} onClick={() => setTab("manage")}>🗂 문제 관리</button>
      </div>

      {tab === "file" && (
        <>
          <div className="ac-box">
            <label className="ac-file">
              {parsed ? `📄 ${parsed.fileName}` : "탭해서 문제 JSON 파일 선택 (calc_problems_m1.json 등)"}
              <input type="file" accept=".json,application/json" onChange={onFile} style={{ display: "none" }} />
            </label>
            <p className="ac-mini">
              형식: {'{ units: […], problems: […] }'} — 같은 id는 덮어쓰기(upsert)라 재등록해도 안전해요.
              m1 → m2 순서로 하나씩 올려 주세요.
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
              <button className="ac-go" disabled={busy} onClick={register}>
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
