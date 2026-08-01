// ashrain.out — 질문대화 목록 (v1.0, 관리자 전용)
// 플로팅 질문챗에서 자동 저장된 관리자 대화를 열람·선택·삭제·JSON 내보내기
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { getConcept } from "../lib/concepts";
import { qcode, UNIT_LETTER, UNIT_NAME } from "../lib/qcode";
import { BlockPreview } from "./ConceptViewer";

const CSS = `
.ah-root { min-height: 100vh; padding: 18px 12px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.ah-root * { box-sizing: border-box; }
.ah-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; --me:#E7F7EF; }
.ah-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; --me:#1E2A22; }
.ah-wrap { max-width: 760px; margin: 0 auto; }
.ah-top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.ah-h { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.ah-back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; white-space: nowrap; }
.ah-filters { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.ah-sel { background: var(--card); border: 1px solid var(--bd); border-radius: 10px; color: var(--ink); font-size: 13px; padding: 9px 10px; }
.ah-search { flex: 1; min-width: 140px; background: var(--card); border: 1px solid var(--bd); border-radius: 10px;
  color: var(--ink); font-size: 13.5px; padding: 9px 12px; outline: none; }
.ah-bar { display: flex; align-items: center; gap: 8px; background: var(--card); border: 1px solid var(--ac);
  border-radius: 12px; padding: 9px 12px; margin-bottom: 10px; font-size: 13px; color: var(--ink); }
.ah-act { border: none; border-radius: 8px; font-size: 12.5px; font-weight: 800; padding: 8px 12px; cursor: pointer; }
.ah-exp { background: var(--ac); }
.ah-light .ah-exp { color: #fff; } .ah-dark .ah-exp { color: #14140F; }
.ah-del { background: transparent; color: var(--mut); border: 1px solid var(--bd); }
.ah-item { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 11px 13px;
  margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
.ah-chk { width: 17px; height: 17px; accent-color: var(--ac); cursor: pointer; flex-shrink: 0; }
.ah-code { font-size: 11px; font-weight: 800; letter-spacing: .5px; color: var(--mut);
  border: 1px solid var(--bd); border-radius: 6px; padding: 3px 6px; white-space: nowrap; }
.ah-main { flex: 1; min-width: 0; cursor: pointer; }
.ah-t { color: var(--ink); font-size: 14px; font-weight: 700; margin: 0;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ah-c { color: var(--mut); font-size: 11.5px; margin: 2px 0 0;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ah-date { font-size: 11px; color: var(--mut); white-space: nowrap; }
.ah-empty { color: var(--mut); font-size: 13.5px; text-align: center; padding: 34px 0; }
.ah-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 14px 16px; margin-bottom: 10px; }
.ah-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.ah-mini { background: var(--in); border: 1px solid var(--inbd); border-radius: 8px; color: var(--mut);
  font-size: 12px; padding: 6px 10px; cursor: pointer; white-space: nowrap; }
.ah-goto { color: var(--mut); font-size: 12px; text-decoration: underline; cursor: pointer; }
.ah-block details { font-size: 12.5px; color: var(--mut); margin-bottom: 12px; }
.ah-block summary { cursor: pointer; color: var(--ink); font-weight: 700; font-size: 13px; }
.ah-bview { max-height: 300px; overflow: auto; border: 1px solid var(--bd); border-radius: 10px;
  padding: 8px 10px; background: var(--in); margin-top: 8px; }
.ah-msg { margin-bottom: 12px; }
.ah-msg-h { display: flex; align-items: center; gap: 8px; margin: 0 2px 4px; }
.ah-who { font-size: 11.5px; font-weight: 800; color: var(--mut); }
.ah-reqbadge { font-size: 10.5px; font-weight: 800; color: var(--ac); border: 1px solid var(--ac);
  border-radius: 999px; padding: 1px 7px; }
.ah-tools { margin-left: auto; display: flex; gap: 6px; }
.ah-tool { background: none; border: none; color: var(--mut); font-size: 12px; cursor: pointer; padding: 2px; }
.ah-b { border: 1px solid var(--bd); border-radius: 12px; padding: 10px 12px; font-size: 14px;
  line-height: 1.65; color: var(--ink); white-space: pre-wrap; word-break: break-word; background: var(--in); }
.ah-me .ah-b { background: var(--me); }
.ah-edit { width: 100%; min-height: 90px; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 14px; padding: 10px; outline: none; resize: vertical; }
`;

const fmtD = (s) => new Date(s).toLocaleDateString("ko-KR", { year: "2-digit", month: "numeric", day: "numeric" });

export default function AdminChats({ theme = "light" }) {
  const [allowed, setAllowed] = useState(null);
  const [items, setItems] = useState([]);
  const [titles, setTitles] = useState({});
  const [checked, setChecked] = useState(new Set());
  const [f, setF] = useState({ letter: "", q: "" });
  const [sel, setSel] = useState(null);
  const [msgs, setMsgs] = useState([]);
  const [editing, setEditing] = useState(null);
  const [selConcept, setSelConcept] = useState(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    const { data } = await supabase.from("concept_chats").select("*")
      .order("updated_at", { ascending: false }).limit(300);
    setItems(data || []);
  }, []);

  useEffect(() => {
    (async () => {
      const { data: { user } } = await supabase.auth.getUser();
      const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).maybeSingle();
      if (prof?.role !== "admin") { setAllowed(false); return; }
      setAllowed(true);
      load();
      const { data: cs } = await supabase.from("concepts").select("id, title");
      setTitles(Object.fromEntries((cs || []).map((c) => [c.id, c.title])));
    })();
  }, [load]);

  const shown = items.filter((r) =>
    (!f.letter || qcode(r.concept_id, r.block_id).startsWith(f.letter)) &&
    (!f.q || (r.title || "").toLowerCase().includes(f.q.toLowerCase()) || r.concept_id.includes(f.q)));

  const toggle = (id) => setChecked((s) => { const n = new Set(s); n.has(id) ? n.delete(id) : n.add(id); return n; });

  const openItem = async (r) => {
    setSel(r); setEditing(null); setSelConcept(null);
    const { data } = await supabase.from("concept_chat_messages").select("*")
      .eq("chat_id", r.id).order("created_at", { ascending: true });
    setMsgs(data || []);
    getConcept(r.concept_id).then(setSelConcept).catch(() => setSelConcept(null));
  };

  const buildExport = async (rows) => {
    const conceptCache = {};
    const chats = [];
    for (const r of rows) {
      const { data: ms } = await supabase.from("concept_chat_messages").select("role, content, tag, created_at")
        .eq("chat_id", r.id).order("created_at", { ascending: true });
      if (!conceptCache[r.concept_id]) {
        conceptCache[r.concept_id] = await getConcept(r.concept_id).catch(() => null);
      }
      const con = conceptCache[r.concept_id];
      const blk = con?.blocks?.find((b) => String(b.id) === String(r.block_id)) || null;
      chats.push({
        id: r.id, q_code: qcode(r.concept_id, r.block_id),
        concept_id: r.concept_id, concept_title: con?.title || titles[r.concept_id] || "",
        block_id: r.block_id, block: blk,
        title: r.title, created_at: r.created_at,
        requests: (ms || []).filter((m) => m.tag === "request").map((m) => m.content),
        messages: ms || [],
      });
    }
    return { exported_at: new Date().toISOString(), count: chats.length, chats };
  };

  const exportChats = async (rows) => {
    if (!rows.length || busy) return;
    setBusy(true);
    const data = await buildExport(rows);
    setBusy(false);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `ashrain-chats-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  const delChats = async (ids) => {
    if (!ids.length) return;
    if (!window.confirm(`대화 ${ids.length}개를 삭제할까요? (되돌릴 수 없어요)`)) return;
    await supabase.from("concept_chats").delete().in("id", ids);
    setChecked(new Set()); setSel(null); load();
  };

  const saveEdit = async () => {
    const t = editing.text.trim();
    if (!t) return;
    await supabase.from("concept_chat_messages")
      .update({ content: t, updated_at: new Date().toISOString() }).eq("id", editing.id);
    setMsgs((s) => s.map((m) => (m.id === editing.id ? { ...m, content: t } : m)));
    setEditing(null);
  };
  const delMsg = async (m) => {
    if (!window.confirm("이 턴을 삭제할까요?")) return;
    await supabase.from("concept_chat_messages").delete().eq("id", m.id);
    setMsgs((s) => s.filter((x) => x.id !== m.id));
  };

  if (allowed === false) return (
    <div className={`ah-root ah-${theme}`}><style>{CSS}</style>
      <p className="ah-empty">관리자 전용 화면입니다.</p></div>
  );

  const selBlock = sel && selConcept?.blocks?.find((b) => String(b.id) === String(sel.block_id));

  return (
    <div className={`ah-root ah-${theme}`}>
      <style>{CSS}</style>
      <div className="ah-wrap">
        <div className="ah-top">
          <h1 className="ah-h">🗂 질문대화</h1>
          <span className="ah-back" onClick={() => (sel ? setSel(null) : (location.hash = ""))}>← {sel ? "목록" : "홈"}</span>
        </div>

        {!sel && (
          <>
            <div className="ah-filters">
              <select className="ah-sel" value={f.letter} onChange={(e) => setF((s) => ({ ...s, letter: e.target.value }))}>
                <option value="">전체 과정</option>
                {Object.entries(UNIT_LETTER).map(([u, l]) => <option key={l} value={l}>{l} · {UNIT_NAME[u]}</option>)}
              </select>
              <input className="ah-search" placeholder="대화 제목·개념 id 검색" value={f.q}
                onChange={(e) => setF((s) => ({ ...s, q: e.target.value }))} />
            </div>
            {checked.size > 0 && (
              <div className="ah-bar">
                <b>{checked.size}개 선택</b>
                <button className="ah-act ah-exp" disabled={busy}
                  onClick={() => exportChats(items.filter((r) => checked.has(r.id)))}>{busy ? "내보내는 중…" : "⬇ JSON 내보내기"}</button>
                <button className="ah-act ah-del" onClick={() => delChats([...checked])}>🗑 삭제</button>
              </div>
            )}
            {shown.length === 0 && <p className="ah-empty">저장된 대화가 아직 없어요.<br/>개념 단락의 물음표에서 대화하면 자동으로 쌓여요.</p>}
            {shown.map((r) => (
              <div key={r.id} className="ah-item">
                <input type="checkbox" className="ah-chk" checked={checked.has(r.id)} onChange={() => toggle(r.id)} />
                <span className="ah-code">{qcode(r.concept_id, r.block_id)}</span>
                <div className="ah-main" onClick={() => openItem(r)}>
                  <p className="ah-t">{r.title || "(제목 없는 대화)"}</p>
                  <p className="ah-c">{titles[r.concept_id] || r.concept_id} · {r.block_id}</p>
                </div>
                <span className="ah-date">{fmtD(r.updated_at)}</span>
              </div>
            ))}
          </>
        )}

        {sel && (
          <div className="ah-card">
            <div className="ah-meta">
              <span className="ah-code">{qcode(sel.concept_id, sel.block_id)}</span>
              <span className="ah-goto" onClick={() => (location.hash = `#/c/${encodeURIComponent(sel.concept_id)}`)}>
                {titles[sel.concept_id] || sel.concept_id} 개념으로 →
              </span>
              <span style={{ flex: 1 }} />
              <button className="ah-mini" disabled={busy} onClick={() => exportChats([sel])}>⬇ 이 대화 JSON</button>
              <button className="ah-mini" onClick={() => delChats([sel.id])}>🗑 삭제</button>
            </div>
            <div className="ah-block">
              <details>
                <summary>단락 미리보기 {selBlock ? "" : "(단락을 찾지 못함)"}</summary>
                {selBlock && <div className="ah-bview"><BlockPreview b={selBlock} theme={theme} /></div>}
              </details>
            </div>
            {msgs.map((m) => (
              <div key={m.id} className={"ah-msg" + (m.role === "user" ? " ah-me" : "")}>
                <div className="ah-msg-h">
                  <span className="ah-who">{m.role === "user" ? "원장" : "Claude"}{m.updated_at ? " · 수정됨" : ""}</span>
                  {m.tag === "request" && <span className="ah-reqbadge">📌 요청사항</span>}
                  <span className="ah-tools">
                    <button className="ah-tool" onClick={() => setEditing({ id: m.id, text: m.content })}>✏️</button>
                    <button className="ah-tool" onClick={() => delMsg(m)}>🗑</button>
                  </span>
                </div>
                {editing?.id === m.id ? (
                  <div>
                    <textarea className="ah-edit" value={editing.text}
                      onChange={(e) => setEditing((s) => ({ ...s, text: e.target.value }))} />
                    <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                      <button className="ah-mini" onClick={saveEdit}>저장</button>
                      <button className="ah-mini" onClick={() => setEditing(null)}>취소</button>
                    </div>
                  </div>
                ) : (
                  <div className="ah-b">{m.content}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
