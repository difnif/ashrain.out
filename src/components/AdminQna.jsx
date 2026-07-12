import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { reviewQna } from "../lib/concepts";

const CSS = `
.aq-root { min-height: 100vh; padding: 20px 14px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.aq-light { background:#EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; }
.aq-dark  { background:#0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; }
.aq-wrap { max-width: 768px; margin: 0 auto; }
.aq-h { color: var(--ink); font-size: 19px; margin: 0 0 4px; }
.aq-sub { color: var(--mut); font-size: 12.5px; margin: 0 0 16px; }
.aq-item { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; }
.aq-meta { font-size: 11.5px; color: var(--mut); margin: 0 0 4px; }
.aq-q { color: var(--ink); font-size: 14.5px; font-weight: 700; margin: 0 0 8px; }
.aq-ta { width: 100%; box-sizing: border-box; min-height: 70px; background: transparent; border: 1px solid var(--bd);
  border-radius: 8px; color: var(--ink); font-size: 13.5px; padding: 10px; outline: none; resize: vertical; }
.aq-row { display: flex; gap: 8px; margin-top: 8px; }
.aq-btn { border: none; border-radius: 8px; font-size: 13px; font-weight: 700; padding: 9px 14px; cursor: pointer; }
.aq-adopt { background: #0DA95F; color: #fff; } .aq-discard { background: transparent; color: var(--mut); border: 1px solid var(--bd); }
.aq-empty { color: var(--mut); text-align: center; padding: 40px 0; font-size: 14px; }
.aq-back { color: var(--mut); font-size: 12.5px; cursor: pointer; text-decoration: underline; }
`;

export default function AdminQna({ theme }) {
  const [items, setItems] = useState([]);
  const [answers, setAnswers] = useState({});
  const [allowed, setAllowed] = useState(null);

  const load = useCallback(async () => {
    const { data: { user } } = await supabase.auth.getUser();
    const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).single();
    if (prof?.role !== "admin") { setAllowed(false); return; }
    setAllowed(true);
    const { data } = await supabase.from("concept_qna")
      .select("id, concept_id, block_id, question, created_at")
      .eq("status", "pending").order("created_at");
    setItems(data || []);
  }, []);
  useEffect(() => { load(); }, [load]);

  const act = async (id, status) => {
    await reviewQna(id, { status, answer: status === "adopted" ? (answers[id] || "") : null });
    load();
  };

  if (allowed === false) return (
    <div className={`aq-root aq-${theme}`}><style>{CSS}</style>
      <p className="aq-empty">관리자 전용 화면입니다.</p></div>
  );
  return (
    <div className={`aq-root aq-${theme}`}>
      <style>{CSS}</style>
      <div className="aq-wrap">
        <h1 className="aq-h">질문 검토</h1>
        <p className="aq-sub">답변을 쓰고 채택하면 학생 화면 말풍선에 바로 올라갑니다. <span className="aq-back" onClick={() => (location.hash = "")}>← 홈</span></p>
        {items.length === 0 && allowed && <p className="aq-empty">대기 중인 질문이 없어요 🎉</p>}
        {items.map((it) => (
          <div key={it.id} className="aq-item">
            <p className="aq-meta">{it.concept_id} · {it.block_id} · {new Date(it.created_at).toLocaleString("ko-KR")}</p>
            <p className="aq-q">Q. {it.question}</p>
            <textarea className="aq-ta" placeholder="답변 작성..." value={answers[it.id] || ""}
              onChange={(e) => setAnswers((a) => ({ ...a, [it.id]: e.target.value }))} />
            <div className="aq-row">
              <button className="aq-btn aq-adopt" onClick={() => act(it.id, "adopted")}
                disabled={!(answers[it.id] || "").trim()}>답변 채택</button>
              <button className="aq-btn aq-discard" onClick={() => act(it.id, "discarded")}>폐기</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
