// ashrain.out — 관리자 개념 질문 대화 (v1.1)
// 개념 단락 = 프로젝트 단위. 단락별 대화 목록 + Claude 다회전 대화 + 턴 수정/삭제 + 📌 요청사항 태그 + 전체 다운로드
import { useEffect, useRef, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { getConcept } from "../lib/concepts";
import { api } from "../lib/authx";
import { BlockPreview } from "./ConceptViewer";
import { qcode } from "../lib/qcode";

const CSS = `
.qc-root { min-height:100vh; padding:16px 12px 90px; box-sizing:border-box;
  font-family:'Pretendard Variable',Pretendard,'Malgun Gothic',system-ui,sans-serif; }
.qc-root * { box-sizing:border-box; }
.qc-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; --me:#E7F7EF; }
.qc-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; --me:#1E2A22; }
.qc-wrap { max-width:640px; margin:0 auto; }
.qc-top { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.qc-back { color:var(--mut); font-size:13px; cursor:pointer; text-decoration:underline; white-space:nowrap; }
.qc-h { color:var(--ink); font-size:16px; font-weight:800; margin:0; flex:1; min-width:0;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.qc-card { background:var(--card); border:1px solid var(--bd); border-radius:14px; padding:14px; margin-bottom:10px; }
.qc-sec { font-size:11px; letter-spacing:1.2px; color:var(--mut); font-weight:700; margin:0 0 8px; }
.qc-btabs { display:flex; align-items:center; gap:6px; margin-bottom:10px; }
.qc-btab { background:transparent; border:1px solid var(--inbd); border-radius:8px; color:var(--mut);
  font-size:12.5px; font-weight:700; padding:7px 12px; cursor:pointer; }
.qc-btab.on { border-color:var(--ac); color:var(--ac); }
.qc-copybtn { margin-left:auto; background:var(--in); border:1px solid var(--inbd); border-radius:8px;
  color:var(--mut); font-size:12px; padding:6px 10px; cursor:pointer; white-space:nowrap; }
.qc-bview { max-height:360px; overflow:auto; border:1px solid var(--bd); border-radius:10px; padding:10px 12px; background:var(--in); }
.qc-block pre { white-space:pre-wrap; word-break:break-all; background:var(--in); border:1px solid var(--inbd);
  border-radius:10px; padding:10px; max-height:360px; overflow:auto; font-size:11.5px; color:var(--mut); margin:0; }
.qc-new { width:100%; background:var(--ac); border:none; border-radius:10px; font-weight:800; font-size:14px;
  padding:11px 0; cursor:pointer; margin-bottom:8px; }
.qc-light .qc-new { color:#fff; } .qc-dark .qc-new { color:#14140F; }
.qc-item { display:flex; align-items:center; gap:8px; padding:11px 4px; border-bottom:1px solid var(--bd); cursor:pointer; }
.qc-item:last-child { border-bottom:none; }
.qc-item-t { flex:1; min-width:0; color:var(--ink); font-size:14px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.qc-item-d { color:var(--mut); font-size:11.5px; white-space:nowrap; }
.qc-mini { background:var(--in); border:1px solid var(--inbd); border-radius:8px; color:var(--mut);
  font-size:12px; padding:6px 10px; cursor:pointer; white-space:nowrap; }
.qc-msg { margin-bottom:12px; }
.qc-msg-b { border:1px solid var(--bd); border-radius:12px; padding:10px 12px; font-size:14px;
  line-height:1.65; color:var(--ink); white-space:pre-wrap; word-break:break-word; background:var(--card); }
.qc-me .qc-msg-b { background:var(--me); }
.qc-msg-h { display:flex; align-items:center; gap:8px; margin:0 2px 4px; }
.qc-who { font-size:11.5px; font-weight:800; color:var(--mut); }
.qc-tools { margin-left:auto; display:flex; gap:6px; }
.qc-tool { background:none; border:none; color:var(--mut); font-size:12px; cursor:pointer; padding:2px; }
.qc-edit { width:100%; min-height:90px; background:var(--in); border:1px solid var(--inbd); border-radius:10px;
  color:var(--ink); font-size:14px; padding:10px; outline:none; resize:vertical; }
.qc-inputbar { position:fixed; left:0; right:0; bottom:0; padding:10px 12px calc(10px + env(safe-area-inset-bottom));
  background:var(--card); border-top:1px solid var(--bd); }
.qc-inputrow { max-width:640px; margin:0 auto; display:flex; gap:8px; align-items:flex-end; }
.qc-ta { flex:1; min-height:44px; max-height:140px; background:var(--in); border:1px solid var(--inbd);
  border-radius:12px; color:var(--ink); font-size:14.5px; padding:11px 12px; outline:none; resize:none; }
.qc-send { background:var(--ac); border:none; border-radius:12px; font-weight:800; font-size:14px;
  padding:12px 16px; cursor:pointer; flex-shrink:0; }
.qc-light .qc-send { color:#fff; } .qc-dark .qc-send { color:#14140F; }
.qc-send:disabled { opacity:.5; }
.qc-empty { color:var(--mut); font-size:13.5px; text-align:center; padding:18px 0; }
.qc-req .qc-msg-b { border-color:var(--ac); border-width:1.5px; }
.qc-reqbadge { font-size:11px; font-weight:800; color:var(--ac); border:1px solid var(--ac);
  border-radius:999px; padding:1px 8px; }
.qc-reqtgl { background:var(--in); border:1px solid var(--inbd); border-radius:12px; color:var(--mut);
  font-size:12.5px; font-weight:700; padding:12px 10px; cursor:pointer; flex-shrink:0; white-space:nowrap; }
.qc-reqtgl.on { border-color:var(--ac); color:var(--ac); }
.qc-think { color:var(--mut); font-size:13px; margin:4px 2px 12px; }
`;

const fmtD = (s) => new Date(s).toLocaleDateString("ko-KR", { month: "numeric", day: "numeric" });

export default function AdminConceptChat({ conceptId, blockId, theme = "light" }) {
  const [uid, setUid] = useState(null);
  const [concept, setConcept] = useState(null);
  const [chats, setChats] = useState([]);
  const [cur, setCur] = useState(null);          // 현재 대화 row
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [editing, setEditing] = useState(null);  // { id, text }
  const [reqMode, setReqMode] = useState(false); // 📌 요청사항으로 남기기
  const [bTab, setBTab] = useState("view");      // 단락 미리보기: view | json
  const [copied, setCopied] = useState(false);
  const [err, setErr] = useState("");
  const endRef = useRef(null);

  const block = concept?.blocks?.find((b) => String(b.id) === String(blockId)) || null;
  const blockJson = block ? JSON.stringify(block, null, 1) : "";

  const loadChats = useCallback(async () => {
    const { data } = await supabase.from("concept_chats").select("*")
      .eq("concept_id", conceptId).eq("block_id", blockId)
      .order("updated_at", { ascending: false });
    setChats(data || []);
  }, [conceptId, blockId]);

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => setUid(data?.user?.id || null));
    getConcept(conceptId).then(setConcept).catch(() => setConcept({ id: conceptId, title: "(개념 로드 실패)", blocks: [] }));
    loadChats();
  }, [conceptId, loadChats]);

  useEffect(() => { endRef.current?.scrollIntoView({ block: "end" }); }, [msgs, busy]);

  const openChat = async (row) => {
    setCur(row); setEditing(null); setErr("");
    const { data } = await supabase.from("concept_chat_messages").select("*")
      .eq("chat_id", row.id).order("created_at", { ascending: true });
    setMsgs(data || []);
  };

  const newChat = async () => {
    if (!uid) return;
    const { data, error } = await supabase.from("concept_chats")
      .insert({ concept_id: conceptId, block_id: blockId, created_by: uid })
      .select().single();
    if (error) { setErr("대화 생성 실패: " + error.message); return; }
    setChats((s) => [data, ...s]); setCur(data); setMsgs([]);
  };

  const delChat = async (row) => {
    if (!window.confirm("이 대화를 통째로 삭제할까요? (되돌릴 수 없어요)")) return;
    await supabase.from("concept_chats").delete().eq("id", row.id);
    if (cur?.id === row.id) { setCur(null); setMsgs([]); }
    loadChats();
  };

  const send = async () => {
    const text = input.trim();
    if (!text || busy || !cur) return;
    setErr(""); setBusy(true); setInput("");
    try {
      const { data: um, error: e1 } = await supabase.from("concept_chat_messages")
        .insert({ chat_id: cur.id, role: "user", content: text, tag: reqMode ? "request" : null })
        .select().single();
      if (e1) throw e1;
      const next = [...msgs, um];
      setMsgs(next);
      if (reqMode) {
        // 요청사항은 기록만 남기고 AI 호출은 생략
        const patch = { updated_at: new Date().toISOString() };
        if (!cur.title) patch.title = "📌 " + text.slice(0, 38);
        await supabase.from("concept_chats").update(patch).eq("id", cur.id);
        if (!cur.title) setCur((s) => ({ ...s, title: patch.title }));
        loadChats(); setBusy(false);
        return;
      }
      const r = await api("ai", {
        task: "qchat", concept_id: conceptId, block_id: blockId, block_json: blockJson,
        messages: next.map((m) => ({ role: m.role, content: (m.tag === "request" ? "[요청사항] " : "") + m.content })),
      }, { auth: true });
      const { data: am, error: e2 } = await supabase.from("concept_chat_messages")
        .insert({ chat_id: cur.id, role: "assistant", content: r.reply }).select().single();
      if (e2) throw e2;
      setMsgs((s) => [...s, am]);
      const patch = { updated_at: new Date().toISOString() };
      if (!cur.title) patch.title = text.slice(0, 40);
      await supabase.from("concept_chats").update(patch).eq("id", cur.id);
      if (!cur.title) setCur((s) => ({ ...s, title: patch.title }));
      loadChats();
    } catch (e) { setErr(e.message || String(e)); }
    finally { setBusy(false); }
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

  const copyJson = async () => {
    const txt = block ? JSON.stringify(block, null, 2) : "";
    try { await navigator.clipboard.writeText(txt); }
    catch {
      const ta = document.createElement("textarea");
      ta.value = txt; document.body.appendChild(ta); ta.select();
      document.execCommand("copy"); document.body.removeChild(ta);
    }
    setCopied(true); setTimeout(() => setCopied(false), 1500);
  };

  const download = () => {
    const L = [];
    L.push("# ashrain 개념 단락 대화");
    L.push(`개념: ${conceptId} — ${concept?.title || ""}`);
    L.push(`단락: ${blockId} — ${block?.label || "(단락 없음)"} (질문코드 ${qcode(conceptId, blockId)})`);
    L.push(`내보낸 시각: ${new Date().toLocaleString("ko-KR")}`);
    L.push("");
    L.push("─── 단락 JSON ───");
    L.push(block ? JSON.stringify(block, null, 2) : "(현재 개념에서 이 단락을 찾지 못했어요)");
    L.push("");
    L.push("─── 대화 ───");
    msgs.forEach((m) => {
      L.push("");
      L.push(`[${m.role === "user" ? "원장" : "Claude"}${m.tag === "request" ? " · 📌 요청사항" : ""}]`);
      L.push(m.content);
    });
    const reqs = msgs.filter((m) => m.tag === "request");
    if (reqs.length) {
      L.push(""); L.push("─── 📌 요청사항 모음 (재생성 시 반영) ───");
      reqs.forEach((m, i) => { L.push(`${i + 1}. ${m.content}`); });
    }
    const blob = new Blob([L.join("\n")], { type: "text/plain;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `qchat_${conceptId}_${blockId}_${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(a.href);
  };

  return (
    <div className={`qc-root qc-${theme}`}>
      <style>{CSS}</style>
      <div className="qc-wrap">
        <div className="qc-top">
          <span className="qc-back" onClick={() => (cur ? (setCur(null), setMsgs([])) : (location.hash = `#/c/${encodeURIComponent(conceptId)}`))}>
            ← {cur ? "대화 목록" : "개념으로"}
          </span>
          <h1 className="qc-h">[{qcode(conceptId, blockId)}] {concept?.title || conceptId} · {block?.label || blockId}</h1>
          {cur && <button className="qc-mini" onClick={download}>⬇ 다운로드</button>}
        </div>

        <div className="qc-card qc-block">
          <div className="qc-btabs">
            <button className={"qc-btab" + (bTab === "view" ? " on" : "")} onClick={() => setBTab("view")}>보이는 화면</button>
            <button className={"qc-btab" + (bTab === "json" ? " on" : "")} onClick={() => setBTab("json")}>JSON 코드</button>
            {bTab === "json" && block && (
              <button className="qc-copybtn" onClick={copyJson}>{copied ? "✓ 복사됨" : "📋 복사"}</button>
            )}
          </div>
          {!block && <p className="qc-empty">⚠ 현재 개념에서 이 단락을 찾지 못했어요 (수정/삭제됨). 대화 기록은 그대로 볼 수 있어요.</p>}
          {block && bTab === "view" && <div className="qc-bview"><BlockPreview b={block} theme={theme} /></div>}
          {block && bTab === "json" && <pre>{JSON.stringify(block, null, 2)}</pre>}
        </div>

        {!cur && (
          <div className="qc-card">
            <p className="qc-sec">이 단락의 대화</p>
            <button className="qc-new" onClick={newChat}>+ 새 대화 시작</button>
            {chats.length === 0 && <p className="qc-empty">아직 대화가 없어요. 첫 대화를 시작해 보세요.</p>}
            {chats.map((r) => (
              <div key={r.id} className="qc-item" onClick={() => openChat(r)}>
                <span className="qc-item-t">{r.title || "(제목 없는 대화)"}</span>
                <span className="qc-item-d">{fmtD(r.updated_at)}</span>
                <button className="qc-tool" onClick={(e) => { e.stopPropagation(); delChat(r); }}>🗑</button>
              </div>
            ))}
          </div>
        )}

        {cur && (
          <div>
            {msgs.length === 0 && <p className="qc-empty">이 단락에 대해 무엇이든 물어보세요.<br/>대화는 자동 저장되고, 턴 단위로 수정·삭제할 수 있어요.</p>}
            {msgs.map((m) => (
              <div key={m.id} className={"qc-msg" + (m.role === "user" ? " qc-me" : "") + (m.tag === "request" ? " qc-req" : "")}>
                <div className="qc-msg-h">
                  <span className="qc-who">{m.role === "user" ? "원장" : "Claude"}{m.updated_at ? " · 수정됨" : ""}</span>
                  {m.tag === "request" && <span className="qc-reqbadge">📌 요청사항</span>}
                  <span className="qc-tools">
                    {m.role === "user" && (
                      <button className="qc-tool" title="요청사항 표시/해제" onClick={async () => {
                        const tag = m.tag === "request" ? null : "request";
                        await supabase.from("concept_chat_messages").update({ tag }).eq("id", m.id);
                        setMsgs((s) => s.map((x) => (x.id === m.id ? { ...x, tag } : x)));
                      }}>📌</button>
                    )}
                    <button className="qc-tool" onClick={() => setEditing({ id: m.id, text: m.content })}>✏️</button>
                    <button className="qc-tool" onClick={() => delMsg(m)}>🗑</button>
                  </span>
                </div>
                {editing?.id === m.id ? (
                  <div>
                    <textarea className="qc-edit" value={editing.text}
                      onChange={(e) => setEditing((s) => ({ ...s, text: e.target.value }))} />
                    <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                      <button className="qc-mini" onClick={saveEdit}>저장</button>
                      <button className="qc-mini" onClick={() => setEditing(null)}>취소</button>
                    </div>
                  </div>
                ) : (
                  <div className="qc-msg-b">{m.content}</div>
                )}
              </div>
            ))}
            {busy && <p className="qc-think">Claude가 생각하는 중…</p>}
            {err && <p className="qc-think" style={{ color: "#DC2626" }}>{err}</p>}
            <div ref={endRef} />
          </div>
        )}
      </div>

      {cur && (
        <div className="qc-inputbar">
          <div className="qc-inputrow">
            <button className={"qc-reqtgl" + (reqMode ? " on" : "")} onClick={() => setReqMode((v) => !v)}>📌</button>
            <textarea className="qc-ta" placeholder={reqMode ? "요청사항으로 기록 (AI 응답 없음)" : "꼬리 질문을 이어서 물어보세요"} value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} />
            <button className="qc-send" onClick={send} disabled={busy || !input.trim()}>{busy ? "…" : "보내기"}</button>
          </div>
        </div>
      )}
    </div>
  );
}
