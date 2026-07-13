import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";

// ashrain.out — 관리자 개념 등록/삭제 화면 (patch v0.1.7)
// 이 파일 하나만 src/components/AdminConcepts.jsx 에 덮어쓰면 됩니다.
// - 등록: JSON 파일 선택(권장, 여러 개 동시 가능) 또는 붙여넣기 → 검증 후 저장(같은 id는 덮어쓰기), 채택 QnA는 중복 자동 건너뜀
// - 삭제: 등록된 개념 목록에서 버튼으로 삭제(연결된 QnA도 함께 삭제됨)
// - 백업: concepts + concept_qna 전체를 JSON 파일로 내려받기

const UNIT_LABEL = {
  "m1-1": "중1 1학기",
  "m1-2": "중1 2학기",
  "m2-1": "중2 1학기",
  "m2-2": "중2 2학기",
};

const BLOCK_TYPES = ["text", "definition", "warning", "check", "image"];

function validateConcepts(input) {
  const arr = Array.isArray(input) ? input : [input];
  const errors = [];
  const seenIds = new Set();
  arr.forEach((c, i) => {
    const tag = c && c.id ? c.id : `#${i + 1}`;
    if (!c || typeof c !== "object" || Array.isArray(c)) {
      errors.push(`${tag}: 개념이 객체 형태가 아닙니다.`);
      return;
    }
    if (!c.id) errors.push(`${tag}: id가 없습니다.`);
    if (!(c.unitId || c.unit_id)) errors.push(`${tag}: unitId가 없습니다.`);
    if (!c.title) errors.push(`${tag}: title이 없습니다.`);
    if (c.id) {
      if (seenIds.has(c.id)) errors.push(`${tag}: 같은 id가 두 번 들어 있습니다.`);
      seenIds.add(c.id);
    }
    if (!Array.isArray(c.blocks) || c.blocks.length === 0) {
      errors.push(`${tag}: blocks가 비어 있습니다.`);
    }
    const blockIds = new Set();
    (Array.isArray(c.blocks) ? c.blocks : []).forEach((b, j) => {
      const bt = b && b.id ? b.id : `${j + 1}번째 블록`;
      if (!b || typeof b !== "object") {
        errors.push(`${tag}: ${bt}이(가) 객체가 아닙니다.`);
        return;
      }
      if (!b.id) errors.push(`${tag}: ${j + 1}번째 블록에 id가 없습니다.`);
      else if (blockIds.has(b.id)) errors.push(`${tag}: 블록 id "${b.id}"가 중복입니다.`);
      else blockIds.add(b.id);
      if (!b.type) errors.push(`${tag}: 블록 ${bt}에 type이 없습니다.`);
      else if (!BLOCK_TYPES.includes(b.type)) errors.push(`${tag}: 블록 ${bt}의 type "${b.type}"을 알 수 없습니다.`);
    });
    (Array.isArray(c.qna) ? c.qna : []).forEach((q, j) => {
      const anchor = q && (q.anchor ?? q.block_id);
      if (anchor && !blockIds.has(anchor)) {
        errors.push(`${tag}: QnA ${j + 1}의 anchor("${anchor}")에 해당하는 블록이 없습니다.`);
      }
      if (!q || !(q.q ?? q.question)) errors.push(`${tag}: QnA ${j + 1}에 질문이 없습니다.`);
      if (!q || !(q.a ?? q.answer)) errors.push(`${tag}: QnA ${j + 1}에 답변이 없습니다.`);
    });
  });
  return { list: arr, errors };
}

export default function AdminConcepts() {
  const [text, setText] = useState("");
  const [list, setList] = useState([]);
  const [isAdmin, setIsAdmin] = useState(null);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const fileRef = useRef(null);

  const load = () =>
    supabase
      .from("concepts")
      .select("id, unit_id, title, sort_order")
      .order("unit_id", { ascending: true })
      .order("sort_order", { ascending: true })
      .then(({ data, error }) => {
        if (!error) setList(data || []);
      });

  useEffect(() => {
    load();
    supabase.auth.getUser().then(({ data }) => {
      if (!data?.user) return setIsAdmin(false);
      supabase
        .from("profiles")
        .select("role")
        .eq("id", data.user.id)
        .single()
        .then(({ data: p }) => setIsAdmin(p?.role === "admin"));
    });
  }, []);

  async function submit() {
    setMsg("");
    setErr("");
    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch (e) {
      setErr(
        "JSON 형식 오류: " +
          e.message +
          (text.length > 5000
            ? "\n붙여넣은 내용이 중간에 잘렸을 수 있습니다(현재 " +
              text.length.toLocaleString() +
              "자). 아래 '파일에서 불러오기'로 JSON 파일을 직접 선택하면 잘림 없이 등록됩니다."
            : "")
      );
      return;
    }
    await saveItems(parsed);
  }

  async function handleFiles(e) {
    const files = Array.from(e.target.files || []);
    e.target.value = ""; // 같은 파일 재선택 허용
    if (!files.length) return;
    setMsg("");
    setErr("");
    const merged = [];
    const problems = [];
    for (const f of files) {
      try {
        const raw = await f.text();
        const parsed = JSON.parse(raw);
        merged.push(...(Array.isArray(parsed) ? parsed : [parsed]));
      } catch (ex) {
        problems.push(f.name + ": " + ex.message);
      }
    }
    if (problems.length) {
      setErr("파일을 읽지 못했습니다.\n" + problems.join("\n"));
      return;
    }
    await saveItems(merged);
  }

  async function saveItems(parsed) {
    const { list: items, errors } = validateConcepts(parsed);
    if (errors.length) {
      setErr("저장 전 검증에서 문제를 찾았습니다.\n" + errors.join("\n"));
      return;
    }
    setBusy(true);
    const rows = items.map((c) => ({
      id: c.id,
      unit_id: c.unitId ?? c.unit_id,
      title: c.title,
      subtitle: c.subtitle ?? null,
      sort_order: c.order ?? c.sort_order ?? 0,
      blocks: c.blocks ?? [],
      cover: c.cover ?? null,
      updated_at: new Date().toISOString(),
    }));
    const { data: saved, error } = await supabase.from("concepts").upsert(rows).select("id");
    if (error) {
      setBusy(false);
      setErr("개념 저장 실패: " + error.message);
      return;
    }
    if (!saved || saved.length === 0) {
      setBusy(false);
      setErr("저장되지 않았습니다. 관리자 계정으로 로그인했는지 확인해 주세요.");
      return;
    }

    // 채택 QnA 등록 — 이미 있는 (개념, 블록, 질문) 조합은 건너뜀 (재붙여넣기 시 중복 방지)
    const qnaAll = items.flatMap((c) =>
      (c.qna || []).map((q) => ({
        concept_id: c.id,
        block_id: q.anchor ?? q.block_id ?? null,
        question: q.q ?? q.question,
        answer: q.a ?? q.answer,
        status: q.status ?? "adopted",
      }))
    );
    let qnaMsg = "";
    let qnaFailed = false;
    if (qnaAll.length) {
      const ids = [...new Set(qnaAll.map((q) => q.concept_id))];
      const { data: existing, error: exErr } = await supabase
        .from("concept_qna")
        .select("concept_id, block_id, question")
        .in("concept_id", ids);
      if (exErr) {
        qnaMsg = " · QnA 조회 실패: " + exErr.message;
        qnaFailed = true;
      } else {
        const keyOf = (q) => `${q.concept_id}|${q.block_id ?? ""}|${q.question}`;
        const have = new Set((existing || []).map(keyOf));
        const fresh = qnaAll.filter((q) => !have.has(keyOf(q)));
        if (fresh.length) {
          const { error: insErr } = await supabase.from("concept_qna").insert(fresh);
          if (insErr) {
            qnaMsg =
              " · 개념은 저장됐지만 QnA " +
              fresh.length +
              "건 등록에 실패했습니다: " +
              insErr.message +
              " — 동봉된 SQL(2026-07_qna_admin_insert.sql)을 Supabase SQL Editor에서 한 번 실행하면 해결됩니다.";
            qnaFailed = true;
          } else {
            qnaMsg = " · 새 QnA " + fresh.length + "건 등록";
          }
        } else {
          qnaMsg = " · QnA는 모두 이미 등록되어 있어 건너뜀";
        }
      }
    }
    setBusy(false);
    const head = "개념 " + rows.length + "건 저장 완료";
    if (qnaFailed) {
      setErr(head + qnaMsg);
    } else {
      setMsg(head + qnaMsg);
      setText("");
    }
    load();
  }

  async function removeConcept(c) {
    const ok = window.confirm(
      "「" + c.title + "」(" + c.id + ") 개념을 삭제할까요?\n연결된 학생 질문(QnA)도 함께 삭제되고, 되돌릴 수 없습니다."
    );
    if (!ok) return;
    setBusy(true);
    setMsg("");
    setErr("");
    const { data, error } = await supabase.from("concepts").delete().eq("id", c.id).select("id");
    setBusy(false);
    if (error) {
      setErr("삭제 실패: " + error.message);
      return;
    }
    if (!data || data.length === 0) {
      setErr("삭제되지 않았습니다. 관리자 계정으로 로그인했는지 확인해 주세요.");
      return;
    }
    setMsg("「" + c.title + "」 삭제 완료");
    load();
  }

  async function doExport() {
    setErr("");
    setMsg("백업 파일을 만드는 중…");
    const [{ data: cs, error: e1 }, { data: qs, error: e2 }] = await Promise.all([
      supabase.from("concepts").select("*").order("unit_id").order("sort_order"),
      supabase.from("concept_qna").select("*").order("created_at"),
    ]);
    if (e1 || e2) {
      setMsg("");
      setErr("백업 실패: " + (e1 || e2).message);
      return;
    }
    const blob = new Blob(
      [JSON.stringify({ exportedAt: new Date().toISOString(), concepts: cs, qna: qs }, null, 2)],
      { type: "application/json" }
    );
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ashrain-concepts-backup-" + new Date().toISOString().slice(0, 10) + ".json";
    a.click();
    URL.revokeObjectURL(a.href);
    setMsg("백업 파일을 내려받았습니다.");
  }

  const groups = {};
  list.forEach((c) => {
    (groups[c.unit_id] = groups[c.unit_id] || []).push(c);
  });
  const unitKeys = Object.keys(groups).sort();

  return (
    <div className="acx-wrap">
      <style>{CSS}</style>
      <div className="acx-head">
        <span className="acx-back" onClick={() => (location.hash = "")}>← 홈</span>
        <h1 className="acx-h1">📚 개념 등록</h1>
      </div>

      {isAdmin === false && (
        <p className="acx-note">관리자 계정이 아니면 저장·삭제가 되지 않습니다. 관리자로 로그인해 주세요.</p>
      )}

      <div className="acx-card">
        <p className="acx-desc">
          <b>파일에서 불러오기</b>로 개념 JSON 파일을 선택하면 바로 검증·저장됩니다(여러 파일 동시 선택 가능).
          모바일에서는 복사·붙여넣기 시 긴 내용이 잘릴 수 있어 파일 선택을 권장해요.
          직접 붙여넣기도 가능하며, 같은 id는 덮어쓰기되고 이미 있는 QnA는 자동으로 건너뜁니다.
        </p>
        <input
          ref={fileRef}
          type="file"
          accept=".json,application/json"
          multiple
          style={{ display: "none" }}
          onChange={handleFiles}
        />
        <div className="acx-row">
          <button className="acx-btn acx-pri" onClick={() => fileRef.current?.click()} disabled={busy}>
            파일에서 불러오기
          </button>
        </div>
        <textarea
          className="acx-ta"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder='{"id":"m1-1-03","unitId":"m1-1","title":"소인수분해", ... } 또는 [ {...}, {...} ]'
        />
        <div className="acx-row">
          <button className="acx-btn acx-pri" onClick={submit} disabled={busy || !text.trim()}>
            검증 후 저장
          </button>
          <button className="acx-btn acx-sec" onClick={doExport} disabled={busy}>
            전체 백업(JSON 내려받기)
          </button>
        </div>
        {msg && <p className="acx-msg">{msg}</p>}
        {err && <p className="acx-msg acx-err">{err}</p>}
      </div>

      <div className="acx-card">
        <p className="acx-desc">
          등록된 개념 <b>{list.length}개</b>. 삭제하면 연결된 학생 질문(QnA)도 함께 지워집니다.
        </p>
        {unitKeys.length === 0 && <p className="acx-empty">아직 등록된 개념이 없습니다.</p>}
        {unitKeys.map((u) => (
          <div key={u} className="acx-group">
            <h2 className="acx-h2">
              {UNIT_LABEL[u] || u} <span className="acx-count">{groups[u].length}개</span>
            </h2>
            {groups[u].map((c) => (
              <div key={c.id} className="acx-item">
                <span className="acx-order">{String(c.sort_order).padStart(2, "0")}</span>
                <span className="acx-title">{c.title}</span>
                <span className="acx-id">{c.id}</span>
                <button className="acx-btn acx-del" onClick={() => removeConcept(c)} disabled={busy}>
                  삭제
                </button>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

const CSS = `
.acx-wrap { max-width: 760px; margin: 0 auto; padding: 24px 16px 64px; }
.acx-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 16px; }
.acx-h1 { font-size: 1.35rem; margin: 0; }
.acx-back { cursor: pointer; opacity: .65; font-size: .9rem; }
.acx-back:hover { opacity: 1; }
.acx-note { font-size: .85rem; padding: 10px 14px; border-radius: 10px;
  background: rgba(244, 118, 92, .12); border: 1px solid rgba(244, 118, 92, .35); }
.acx-card { border: 1px solid rgba(127,127,127,.22); background: rgba(127,127,127,.05);
  border-radius: 14px; padding: 16px; margin-bottom: 18px; }
.acx-desc { font-size: .88rem; opacity: .8; margin: 0 0 10px; line-height: 1.55; }
.acx-ta { width: 100%; box-sizing: border-box; min-height: 180px; resize: vertical;
  font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .82rem; line-height: 1.5;
  padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(127,127,127,.3);
  background: rgba(255,255,255,.55); color: inherit; }
[data-theme="dark"] .acx-ta { background: rgba(0,0,0,.25); }
.acx-row { display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
.acx-btn { border-radius: 10px; padding: 8px 14px; font-size: .88rem; cursor: pointer;
  border: 1px solid rgba(127,127,127,.3); background: rgba(127,127,127,.08); color: inherit; }
.acx-btn:disabled { opacity: .45; cursor: default; }
.acx-pri { background: rgba(20,164,148,.16); border-color: rgba(20,164,148,.5); }
.acx-pri:not(:disabled):hover { background: rgba(20,164,148,.26); }
.acx-sec:not(:disabled):hover { background: rgba(127,127,127,.15); }
.acx-del { padding: 4px 10px; font-size: .8rem;
  background: rgba(244, 99, 99, .1); border-color: rgba(244, 99, 99, .4); }
.acx-del:not(:disabled):hover { background: rgba(244, 99, 99, .2); }
.acx-msg { font-size: .85rem; margin: 10px 0 0; white-space: pre-wrap; color: #16a08f; }
.acx-err { color: #e05252; }
.acx-empty { font-size: .85rem; opacity: .6; }
.acx-group { margin-top: 14px; }
.acx-h2 { font-size: .95rem; margin: 0 0 6px; opacity: .85; }
.acx-count { font-size: .78rem; opacity: .55; font-weight: normal; margin-left: 6px; }
.acx-item { display: flex; align-items: center; gap: 10px; padding: 7px 10px;
  border-radius: 10px; }
.acx-item:hover { background: rgba(127,127,127,.08); }
.acx-order { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .78rem;
  opacity: .55; width: 22px; text-align: right; }
.acx-title { flex: 1; font-size: .92rem; }
.acx-id { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .75rem; opacity: .45; }
`;
