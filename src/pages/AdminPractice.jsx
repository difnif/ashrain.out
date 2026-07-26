// src/pages/AdminPractice.jsx — 예제·유제 세트 관리 (해시 라우트: #/admin/practice, admin 전용)
// 세트 JSON 파일을 여러 개 선택해 일괄 등록 — 단일 세트 { concept_id, ... } / 배열 [ {...}, ... ] / 묶음 { "sets": [ {...}, ... ] } 모두 지원
import { useEffect, useRef, useState } from "react";
import { supabase } from "../lib/authx";
import { listConcepts } from "../lib/concepts";

export default function AdminPractice() {
  const [ok, setOk] = useState(null);
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState([]);
  const [rows, setRows] = useState([]);
  const [concepts, setConcepts] = useState([]);
  const fileRef = useRef(null);

  useEffect(() => {
    (async () => {
      const { data: s } = await supabase.auth.getSession();
      if (!s?.session) { setOk(false); return; }
      const { data: p } = await supabase.from("profiles")
        .select("role").eq("id", s.session.user.id).maybeSingle();
      setOk(p?.role === "admin");
      if (p?.role === "admin") load();
    })();
  }, []);

  const load = async () => {
    const [{ data }, cs] = await Promise.all([
      supabase.from("practice_sets")
        .select("concept_id, title, problems, updated_at")
        .order("concept_id"),
      listConcepts().catch(() => []),
    ]);
    setRows(data || []);
    setConcepts(cs || []);
  };

  const conceptTitle = (id) => concepts.find((c) => c.id === id)?.title || null;

  const validate = (j) => {
    if (!j || typeof j !== "object") return "JSON 객체가 아님";
    if (!j.concept_id || typeof j.concept_id !== "string") return "concept_id 없음";
    if (!Array.isArray(j.problems) || j.problems.length === 0) return "problems 배열이 비어 있음";
    for (const p of j.problems) {
      if (!p.id) return "문제에 id 없음";
      if (!Array.isArray(p.text) || !p.text.length) return `${p.id}: text 배열 없음`;
      const hasSteps = Array.isArray(p.steps) && p.steps.length;
      const hasMethods = Array.isArray(p.methods) && p.methods.length
        && p.methods.every((m) => Array.isArray(m.steps) && m.steps.length);
      if (!hasSteps && !hasMethods) return `${p.id}: steps 또는 methods 필요`;
      if (!p.answer || !Array.isArray(p.answer.accept) || !p.answer.accept.length) return `${p.id}: answer.accept 필요`;
    }
    return null;
  };

  const pickFiles = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;
    setBusy(true);
    const out = [];
    const { data: s } = await supabase.auth.getSession();
    for (const f of files) {
      try {
        const j = JSON.parse(await f.text());
        const sets = Array.isArray(j) ? j : Array.isArray(j?.sets) ? j.sets : [j];
        if (!sets.length) { out.push(`✗ ${f.name}: 세트가 없음`); continue; }
        for (const set of sets) {
          const why = validate(set);
          if (why) { out.push(`✗ ${f.name} › ${set?.concept_id || "?"}: ${why}`); continue; }
          const { error } = await supabase.from("practice_sets").upsert({
            concept_id: set.concept_id,
            title: set.title || "",
            problems: set.problems,
            updated_by: s?.session?.user?.id || null,
            updated_at: new Date().toISOString(),
          });
          if (error) { out.push(`✗ ${f.name} › ${set.concept_id}: ${error.message}`); continue; }
          const linked = conceptTitle(set.concept_id);
          out.push(`✓ ${f.name} › ${set.concept_id} · ${set.problems.length}문제${linked ? ` · 개념 연결됨(${linked})` : " · ⚠ 개념 미연결(#/p/ 직접 접근만 가능)"}`);
        }
      } catch (err) {
        out.push(`✗ ${f.name}: JSON 해석 실패 (${err.message})`);
      }
    }
    setLog(out);
    setBusy(false);
    if (fileRef.current) fileRef.current.value = "";
    load();
  };

  const removeSet = async (cid) => {
    if (!window.confirm(`${cid} 세트를 삭제할까요? 학생 진행도 기록은 남습니다.`)) return;
    await supabase.from("practice_sets").delete().eq("concept_id", cid);
    load();
  };

  const copyIds = async () => {
    const text = concepts.map((c) => `${c.id}\t${c.unit_id}\t${c.title}`).join("\n");
    try { await navigator.clipboard.writeText(text); alert(`개념 ${concepts.length}개 id를 복사했어요.`); }
    catch { alert("복사 실패 — 데스크톱에서 시도해주세요."); }
  };

  if (ok === null) return null;
  if (ok === false) return <div className="ap-wrap"><Style /><p className="ap-err">관리자만 접근할 수 있어요.</p></div>;

  const covered = new Set(rows.map((r) => r.concept_id));
  const uncovered = concepts.filter((c) => !covered.has(c.id));

  return (
    <div className="ap-wrap"><Style />
      <h2 className="ap-title">예제·유제 세트 관리</h2>

      <div className="ap-card">
        <div className="ap-row ap-between">
          <h3 className="ap-sub">세트 등록 (JSON 파일)</h3>
          <button className="ap-btn" onClick={copyIds}>개념 id 목록 복사</button>
        </div>
        <input ref={fileRef} type="file" accept=".json,application/json" multiple
          onChange={pickFiles} disabled={busy} className="ap-file" />
        {log.map((l, i) => (
          <p key={i} className={"ap-log" + (l.startsWith("✓") ? " good" : " bad")}>{l}</p>
        ))}
      </div>

      <div className="ap-card">
        <h3 className="ap-sub">등록된 세트 {rows.length}개 · 미등록 개념 {uncovered.length}개</h3>
        {rows.map((r) => (
          <div className="ap-item" key={r.concept_id}>
            <div className="ap-item-main">
              <b>{r.concept_id}</b>
              <span className="ap-item-sub">
                {conceptTitle(r.concept_id) || r.title || "—"} · {Array.isArray(r.problems) ? r.problems.length : 0}문제
                {" · "}{new Date(r.updated_at).toLocaleDateString("ko-KR")}
              </span>
            </div>
            <div className="ap-row">
              <a className="ap-btn ap-mini" href={`#/p/${encodeURIComponent(r.concept_id)}`}>미리보기</a>
              <button className="ap-btn ap-mini" onClick={() => removeSet(r.concept_id)}>삭제</button>
            </div>
          </div>
        ))}
        {rows.length === 0 && <p className="ap-hint">아직 등록된 세트가 없어요. 위에서 JSON 파일을 올려주세요.</p>}
      </div>
    </div>
  );
}

function Style() {
  return (
    <style>{`
      .ap-wrap{max-width:560px;margin:0 auto;padding:20px 16px 48px;color:var(--text,#1c1c1e)}
      .ap-title{margin:4px 0 12px;font-size:22px}
      .ap-sub{margin:0;font-size:15px}
      .ap-card{background:var(--surface,#fff);border:1px solid var(--border,#e5e7eb);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
      .ap-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
      .ap-between{justify-content:space-between}
      .ap-btn{padding:9px 12px;border-radius:10px;border:1px solid var(--border,#d6d9de);background:var(--surface,#fff);font-size:13px;color:inherit;text-decoration:none}
      .ap-mini{padding:6px 10px;font-size:12px}
      .ap-file{font-size:13px}
      .ap-log{font-size:12.5px;margin:0}
      .ap-log.good{color:var(--good,#16a34a)} .ap-log.bad{color:var(--bad,#dc2626)}
      .ap-item{border-top:1px solid var(--border,#eef0f3);padding:10px 0 8px;display:flex;justify-content:space-between;gap:8px;align-items:center}
      .ap-item-main{min-width:0;display:flex;flex-direction:column}
      .ap-item-sub{font-size:12px;color:var(--muted,#8a8f98)}
      .ap-hint{font-size:12.5px;color:var(--muted,#8a8f98);margin:0}
      .ap-err{font-size:13px;color:var(--bad,#dc2626);text-align:center}
    `}</style>
  );
}
