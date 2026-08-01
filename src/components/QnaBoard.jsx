// ashrain.out — 질문게시판 (v1.0)
// 채택(답변 예정)·답변 완료 질문을 모두 모아 보여주고, 누구나 댓글 가능 (익명 필명 / 아이디 선택)
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { qcode, penName, UNIT_LETTER, UNIT_NAME } from "../lib/qcode";

const CSS = `
.qb-root { min-height: 100vh; padding: 18px 12px 60px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.qb-root * { box-sizing: border-box; }
.qb-light { background:#EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; --amber:#B45309; }
.qb-dark  { background:#0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; --amber:#FBBF24; }
.qb-wrap { max-width: 720px; margin: 0 auto; }
.qb-top { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.qb-h { color: var(--ink); font-size: 18px; font-weight: 800; margin: 0; flex: 1; }
.qb-back { color: var(--mut); font-size: 13px; cursor: pointer; text-decoration: underline; white-space: nowrap; }
.qb-filters { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.qb-sel { background: var(--card); border: 1px solid var(--bd); border-radius: 10px; color: var(--ink);
  font-size: 13px; padding: 9px 10px; }
.qb-search { flex: 1; min-width: 140px; background: var(--card); border: 1px solid var(--bd); border-radius: 10px;
  color: var(--ink); font-size: 13.5px; padding: 9px 12px; outline: none; }
.qb-item { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 12px 14px;
  margin-bottom: 8px; cursor: pointer; display: flex; align-items: center; gap: 10px; }
.qb-code { font-size: 11px; font-weight: 800; letter-spacing: .5px; color: var(--mut);
  border: 1px solid var(--bd); border-radius: 6px; padding: 3px 6px; white-space: nowrap; }
.qb-qtext { flex: 1; min-width: 0; color: var(--ink); font-size: 14px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.qb-badge { font-size: 11px; font-weight: 800; border-radius: 999px; padding: 3px 9px; white-space: nowrap; }
.qb-done { color: var(--ac); border: 1px solid var(--ac); }
.qb-wait { color: var(--amber); border: 1px solid var(--amber); }
.qb-date { font-size: 11px; color: var(--mut); white-space: nowrap; }
.qb-empty { color: var(--mut); font-size: 13.5px; text-align: center; padding: 30px 0; }
.qb-card { background: var(--card); border: 1px solid var(--bd); border-radius: 14px; padding: 16px; margin-bottom: 10px; }
.qb-meta { font-size: 12px; color: var(--mut); margin: 0 0 6px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.qb-pen { font-weight: 700; }
.qb-goto { color: var(--mut); text-decoration: underline; cursor: pointer; }
.qb-q { color: var(--ink); font-size: 15px; font-weight: 700; margin: 0 0 10px; white-space: pre-wrap; line-height: 1.6; }
.qb-a { color: var(--ink); font-size: 14px; background: rgba(13,169,95,.07); border: 1px solid var(--bd);
  border-radius: 10px; padding: 12px; margin: 0; white-space: pre-wrap; line-height: 1.65; }
.qb-waitmsg { color: var(--amber); font-size: 13px; margin: 0; }
.qb-sec { font-size: 11px; letter-spacing: 1.2px; color: var(--mut); font-weight: 700; margin: 14px 0 8px; }
.qb-cmt { border-top: 1px solid var(--bd); padding: 10px 2px; }
.qb-cmt-h { display: flex; align-items: center; gap: 8px; margin-bottom: 3px; }
.qb-cmt-n { font-size: 12px; font-weight: 800; color: var(--ink); }
.qb-cmt-d { font-size: 10.5px; color: var(--mut); }
.qb-cmt-x { margin-left: auto; background: none; border: none; color: var(--mut); font-size: 11px; cursor: pointer; }
.qb-cmt-c { color: var(--ink); font-size: 13.5px; margin: 0; white-space: pre-wrap; line-height: 1.55; }
.qb-mode { display: flex; gap: 6px; margin-bottom: 8px; align-items: center; flex-wrap: wrap; }
.qb-chip { background: transparent; border: 1px solid var(--inbd); border-radius: 999px; color: var(--mut);
  font-size: 12px; font-weight: 700; padding: 6px 11px; cursor: pointer; }
.qb-chip.on { border-color: var(--ac); color: var(--ac); }
.qb-pv { font-size: 11.5px; color: var(--mut); }
.qb-row { display: flex; gap: 8px; align-items: flex-end; }
.qb-ta { flex: 1; min-height: 44px; background: var(--in); border: 1px solid var(--inbd); border-radius: 10px;
  color: var(--ink); font-size: 13.5px; padding: 10px 12px; outline: none; resize: vertical; }
.qb-send { background: var(--ac); border: none; border-radius: 10px; font-weight: 800; font-size: 13px;
  padding: 11px 14px; cursor: pointer; flex-shrink: 0; }
.qb-light .qb-send { color: #fff; } .qb-dark .qb-send { color: #14140F; }
.qb-send:disabled { opacity: .5; }
`;

const fmtD = (s) => new Date(s).toLocaleDateString("ko-KR", { year: "2-digit", month: "numeric", day: "numeric" });

export default function QnaBoard({ theme = "light", initialId = null }) {
  const [me, setMe] = useState(null); // { uid, username, isAdmin }
  const [items, setItems] = useState([]);
  const [titles, setTitles] = useState({});
  const [sel, setSel] = useState(null);
  const [cmts, setCmts] = useState([]);
  const [cmt, setCmt] = useState("");
  const [mode, setMode] = useState("anon"); // anon | nick
  const [busy, setBusy] = useState(false);
  const [f, setF] = useState({ letter: "", status: "", q: "" });

  useEffect(() => {
    (async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (user) {
        const { data: prof } = await supabase.from("profiles").select("username, role").eq("id", user.id).maybeSingle();
        setMe({ uid: user.id, username: prof?.username || "익명", isAdmin: prof?.role === "admin" });
      }
      const { data } = await supabase.from("concept_qna")
        .select("id, concept_id, block_id, question, answer, status, created_at")
        .in("status", ["adopted", "answered"])
        .order("created_at", { ascending: false }).limit(300);
      setItems(data || []);
      const { data: cs } = await supabase.from("concepts").select("id, title");
      setTitles(Object.fromEntries((cs || []).map((c) => [c.id, c.title])));
      if (initialId) {
        const hit = (data || []).find((x) => x.id === initialId);
        if (hit) openItem(hit);
        else {
          const { data: one } = await supabase.from("concept_qna").select("*").eq("id", initialId).maybeSingle();
          if (one) openItem(one);
        }
      }
    })();
  }, []);

  const openItem = useCallback(async (q) => {
    setSel(q); setCmt("");
    const { data } = await supabase.from("concept_qna_comments")
      .select("*").eq("qna_id", q.id).order("created_at", { ascending: true });
    setCmts(data || []);
  }, []);

  const addCmt = async () => {
    const text = cmt.trim();
    if (!text || !me || !sel || busy) return;
    setBusy(true);
    const display_name = mode === "anon" ? penName(me.uid + ":" + sel.id) : me.username;
    const { data, error } = await supabase.from("concept_qna_comments")
      .insert({ qna_id: sel.id, user_id: me.uid, display_name, content: text }).select().single();
    setBusy(false);
    if (!error) { setCmts((s) => [...s, data]); setCmt(""); }
  };

  const delCmt = async (c) => {
    if (!window.confirm("이 댓글을 삭제할까요?")) return;
    await supabase.from("concept_qna_comments").delete().eq("id", c.id);
    setCmts((s) => s.filter((x) => x.id !== c.id));
  };

  const shown = items.filter((q) =>
    (!f.letter || qcode(q.concept_id, q.block_id).startsWith(f.letter)) &&
    (!f.status || q.status === f.status) &&
    (!f.q || q.question.toLowerCase().includes(f.q.toLowerCase())));

  return (
    <div className={`qb-root qb-${theme}`}>
      <style>{CSS}</style>
      <div className="qb-wrap">
        <div className="qb-top">
          <h1 className="qb-h">📋 질문게시판</h1>
          <span className="qb-back" onClick={() => (sel ? setSel(null) : (location.hash = ""))}>
            ← {sel ? "목록" : "홈"}
          </span>
        </div>

        {!sel && (
          <>
            <div className="qb-filters">
              <select className="qb-sel" value={f.letter} onChange={(e) => setF((s) => ({ ...s, letter: e.target.value }))}>
                <option value="">전체 과정</option>
                {Object.entries(UNIT_LETTER).map(([u, l]) => (
                  <option key={l} value={l}>{l} · {UNIT_NAME[u]}</option>
                ))}
              </select>
              <select className="qb-sel" value={f.status} onChange={(e) => setF((s) => ({ ...s, status: e.target.value }))}>
                <option value="">전체 상태</option>
                <option value="answered">답변 완료</option>
                <option value="adopted">답변 예정</option>
              </select>
              <input className="qb-search" placeholder="질문 검색" value={f.q}
                onChange={(e) => setF((s) => ({ ...s, q: e.target.value }))} />
            </div>
            {shown.length === 0 && <p className="qb-empty">조건에 맞는 질문이 아직 없어요.</p>}
            {shown.map((q) => (
              <div key={q.id} className="qb-item" onClick={() => openItem(q)}>
                <span className="qb-code">{qcode(q.concept_id, q.block_id)}</span>
                <span className="qb-qtext">{q.question}</span>
                <span className={"qb-badge " + (q.status === "answered" ? "qb-done" : "qb-wait")}>
                  {q.status === "answered" ? "답변 완료" : "답변 예정"}
                </span>
                <span className="qb-date">{fmtD(q.created_at)}</span>
              </div>
            ))}
          </>
        )}

        {sel && (
          <div className="qb-card">
            <div className="qb-meta">
              <span className="qb-code">{qcode(sel.concept_id, sel.block_id)}</span>
              <span className="qb-pen">{penName("q:" + sel.id)}</span>
              <span>{fmtD(sel.created_at)}</span>
              <span className="qb-goto" onClick={() => (location.hash = `#/c/${encodeURIComponent(sel.concept_id)}`)}>
                {titles[sel.concept_id] || sel.concept_id} 개념 보러 가기 →
              </span>
            </div>
            <p className="qb-q">Q. {sel.question}</p>
            {sel.status === "answered" && sel.answer
              ? <p className="qb-a">A. {sel.answer}</p>
              : <p className="qb-waitmsg">⏳ 선생님이 답변을 준비하고 있어요</p>}

            <p className="qb-sec">댓글 {cmts.length ? `(${cmts.length})` : ""}</p>
            {cmts.map((c) => (
              <div key={c.id} className="qb-cmt">
                <div className="qb-cmt-h">
                  <span className="qb-cmt-n">{c.display_name}</span>
                  <span className="qb-cmt-d">{fmtD(c.created_at)}</span>
                  {me && (c.user_id === me.uid || me.isAdmin) && (
                    <button className="qb-cmt-x" onClick={() => delCmt(c)}>삭제</button>
                  )}
                </div>
                <p className="qb-cmt-c">{c.content}</p>
              </div>
            ))}

            {me && (
              <div style={{ marginTop: 12 }}>
                <div className="qb-mode">
                  <button className={"qb-chip" + (mode === "anon" ? " on" : "")} onClick={() => setMode("anon")}>🎲 익명 필명</button>
                  <button className={"qb-chip" + (mode === "nick" ? " on" : "")} onClick={() => setMode("nick")}>내 아이디</button>
                  <span className="qb-pv">
                    {mode === "anon" ? `→ "${penName(me.uid + ":" + sel.id)}"(으)로 표시돼요` : `→ "${me.username}"(으)로 표시돼요`}
                  </span>
                </div>
                <div className="qb-row">
                  <textarea className="qb-ta" placeholder="댓글을 남겨보세요" value={cmt}
                    onChange={(e) => setCmt(e.target.value)} />
                  <button className="qb-send" onClick={addCmt} disabled={busy || !cmt.trim()}>등록</button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
