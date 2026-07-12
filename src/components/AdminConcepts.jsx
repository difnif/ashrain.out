import { useState } from "react";
import { upsertConcepts, exportConcepts } from "../lib/concepts";

// 개념 등록/수정 — 채팅 루프에서 받은 JSON을 붙여넣으면 끝.
// 단일 객체 { id, ... } 또는 배열 [ {...}, {...} ] 모두 지원. 같은 id면 덮어쓰기(업서트).

const CSS = `
.ac-root { min-height: 100vh; padding: 20px 14px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ac-light { background:#EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; }
.ac-dark  { background:#0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; }
.ac-wrap { max-width: 768px; margin: 0 auto; }
.ac-h { color: var(--ink); font-size: 19px; margin: 0 0 4px; }
.ac-sub { color: var(--mut); font-size: 12.5px; margin: 0 0 14px; line-height: 1.6; }
.ac-ta { width: 100%; box-sizing: border-box; min-height: 300px; background: var(--card); border: 1px solid var(--bd);
  border-radius: 12px; color: var(--ink); font-size: 12.5px; font-family: monospace; padding: 12px; outline: none; resize: vertical; }
.ac-row { display: flex; gap: 8px; margin-top: 10px; }
.ac-btn { border: none; border-radius: 10px; font-size: 13.5px; font-weight: 700; padding: 11px 16px; cursor: pointer; }
.ac-pri { background: #0DA95F; color: #fff; } .ac-sec { background: var(--card); color: var(--mut); border: 1px solid var(--bd); }
.ac-msg { margin-top: 10px; font-size: 13px; color: #0DA95F; }
.ac-err { color: #DC2626; white-space: pre-wrap; }
.ac-back { color: var(--mut); font-size: 12.5px; cursor: pointer; text-decoration: underline; }
`;

function validate(list) {
  const errs = [];
  list.forEach((c, i) => {
    if (!c.id) errs.push(`[${i}] id 없음`);
    if (!(c.unitId || c.unit_id)) errs.push(`[${c.id || i}] unitId 없음`);
    if (!c.title) errs.push(`[${c.id || i}] title 없음`);
    if (!Array.isArray(c.blocks) || c.blocks.length === 0) errs.push(`[${c.id || i}] blocks가 비어 있음`);
    (c.blocks || []).forEach((b) => {
      if (!b.id || !b.type) errs.push(`[${c.id}] 블록에 id/type 누락`);
    });
  });
  return errs;
}

export default function AdminConcepts({ theme }) {
  const [text, setText] = useState("");
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const submit = async () => {
    setMsg(""); setErr("");
    let parsed;
    try { parsed = JSON.parse(text); }
    catch (e) { setErr("JSON 형식이 아니에요:\n" + e.message); return; }
    const list = Array.isArray(parsed) ? parsed : [parsed];
    const errs = validate(list);
    if (errs.length) { setErr("검증 실패:\n" + errs.join("\n")); return; }
    try {
      const n = await upsertConcepts(list);
      setMsg(`✓ ${n}개 개념 저장 완료! 홈에서 바로 확인할 수 있어요.`);
      setText("");
    } catch (e) { setErr("저장 실패: " + e.message + "\n(관리자 계정인지 확인해 주세요)"); }
  };

  const doExport = async () => {
    try {
      const data = await exportConcepts();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `concepts_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
    } catch (e) { setErr("내보내기 실패: " + e.message); }
  };

  return (
    <div className={`ac-root ac-${theme}`}>
      <style>{CSS}</style>
      <div className="ac-wrap">
        <h1 className="ac-h">개념 등록 · 수정</h1>
        <p className="ac-sub">
          채팅에서 받은 개념 JSON을 붙여넣고 저장하세요. 하나(객체)든 여러 개(배열)든 되고,
          같은 id는 덮어쓰기됩니다. SQL은 더 이상 필요 없어요.
          {" "}<span className="ac-back" onClick={() => (location.hash = "")}>← 홈</span>
        </p>
        <textarea className="ac-ta" value={text} onChange={(e) => setText(e.target.value)}
          placeholder='{"id":"m1-1-02","unitId":"m1-1","title":"거듭제곱", ... } 또는 [ {...}, {...} ]' />
        <div className="ac-row">
          <button className="ac-btn ac-pri" onClick={submit} disabled={!text.trim()}>검증 후 저장</button>
          <button className="ac-btn ac-sec" onClick={doExport}>전체 백업(JSON 내려받기)</button>
        </div>
        {msg && <p className="ac-msg">{msg}</p>}
        {err && <p className="ac-msg ac-err">{err}</p>}
      </div>
    </div>
  );
}
