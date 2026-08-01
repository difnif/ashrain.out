// ashrain.out — 질문 검토 (v2.0)
// 흐름: 대기(pending) → 채택(adopted=답변 예정, 게시판 공개) → 답변 완료(answered, 단락 말풍선 노출)
import { useEffect, useState, useCallback } from "react";
import { supabase } from "../supabaseClient";
import { reviewQna } from "../lib/concepts";
import { qcode } from "../lib/qcode";

const CSS = `
.aq-root { min-height: 100vh; padding: 20px 14px; box-sizing: border-box;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.aq-light { background:#EDEFF2; --ink:#1F2937; --mut:#8A929C; --card:#fff; --bd:#DFE3E8; --ac:#0DA95F; }
.aq-dark  { background:#0B0C0F; --ink:#E2E8F0; --mut:#6B7280; --card:#15171C; --bd:#23262D; --ac:#FFE03C; }
.aq-wrap { max-width: 768px; margin: 0 auto; }
.aq-h { color: var(--ink); font-size: 19px; margin: 0 0 4px; }
.aq-sub { color: var(--mut); font-size: 12.5px; margin: 0 0 14px; }
.aq-tabs { display: flex; gap: 6px; margin-bottom: 14px; }
.aq-tab { background: transparent; border: 1px solid var(--bd); border-radius: 999px; color: var(--mut);
  font-size: 12.5px; font-weight: 700; padding: 7px 13px; cursor: pointer; }
.aq-tab.on { border-color: var(--ac); color: var(--ac); }
.aq-item { background: var(--card); border: 1px solid var(--bd); border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; }
.aq-meta { font-size: 11.5px; color: var(--mut); margin: 0 0 4px; }
.aq-code { font-weight: 800; letter-spacing: .5px; }
.aq-q { color: var(--ink); font-size: 14.5px; font-weight: 700; margin: 0 0 8px; white-space: pre-wrap; }
.aq-a { color: var(--ink); font-size: 13.5px; background: rgba(13,169,95,.08); border: 1px solid var(--bd);
  border-radius: 8px; padding: 10px; margin: 0 0 8px; white-space: pre-wrap; }
.aq-ta { width: 100%; box-sizing: border-box; min-height: 70px; background: transparent; border: 1px solid var(--bd);
  border-radius: 8px; color: var(--ink); font-size: 13.5px; padding: 10px; outline: none; resize: vertical; }
.aq-row { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
.aq-btn { border: none; border-radius: 8px; font-size: 13px; font-weight: 700; padding: 9px 14px; cursor: pointer; }
.aq-adopt { background: transparent; color: var(--ac); border: 1px solid var(--ac); }
.aq-done { background: var(--ac); color: #fff; }
.aq-dark .aq-done { color: #14140F; }
.aq-done:disabled { opacity: .45; cursor: default; }
.aq-discard { background: transparent; color: var(--mut); border: 1px solid var(--bd); }
.aq-empty { color: var(--mut); text-align: center; padding: 40px 0; font-size: 14px; }
.aq-back { color: var(--mut); font-size: 12.5px; cursor: pointer; text-decoration: underline; }
`;

const TABS = [
  ["pending", "대기"],
  ["adopted", "답변 예정"],
  ["answered", "답변 완료"],
];

export default function AdminQna({ theme }) {
  const [tab, setTab] = useState("pending");
  const [items, setItems] = useState([]);
  const [answers, setAnswers] = useState({});
  const [allowed, setAllowed] = useState(null);

  const load = useCallback(async () => {
    const { data: { user } } = await supabase.auth.getUser();
    const { data: prof } = await supabase.from("profiles").select("role").eq("id", user?.id).single();
    if (prof?.role !== "admin") { setAllowed(false); return; }
    setAllowed(true);
    const { data } = await supabase.from("concept_qna")
      .select("id, concept_id, block_id, question, answer, status, created_at")
      .eq("status", tab).order("created_at", { ascending: tab === "pending" });
    setItems(data || []);
    setAnswers((a) => {
      const n = { ...a };
      (data || []).forEach((it) => { if (n[it.id] === undefined && it.answer) n[it.id] = it.answer; });
      return n;
    });
  }, [tab]);
  useEffect(() => { load(); }, [load]);

  const act = async (id, patch) => { await reviewQna(id, patch); load(); };

  if (allowed === false) return (
    <div className={`aq-root aq-${theme}`}><style>{CSS}</style>
      <p className="aq-empty">관리자 전용 화면입니다.</p></div>
  );
  return (
    <div className={`aq-root aq-${theme}`}>
      <style>{CSS}</style>
      <div className="aq-wrap">
        <h1 className="aq-h">질문 검토</h1>
        <p className="aq-sub">
          채택 = 답변 예정으로 게시판에 익명 공개 · 답변 완료 = 단락 말풍선에 노출
          &nbsp;<span className="aq-back" onClick={() => (location.hash = "")}>← 홈</span>
          &nbsp;<span className="aq-back" onClick={() => (location.hash = "#/board")}>게시판 보기</span>
        </p>
        <div className="aq-tabs">
          {TABS.map(([k, label]) => (
            <button key={k} className={"aq-tab" + (tab === k ? " on" : "")} onClick={() => setTab(k)}>{label}</button>
          ))}
        </div>
        {items.length === 0 && allowed && <p className="aq-empty">{tab === "pending" ? "대기 중인 질문이 없어요 🎉" : "여기엔 아직 글이 없어요"}</p>}
        {items.map((it) => (
          <div key={it.id} className="aq-item">
            <p className="aq-meta">
              <span className="aq-code">[{qcode(it.concept_id, it.block_id)}]</span>
              &nbsp;{it.concept_id} · {it.block_id} · {new Date(it.created_at).toLocaleString("ko-KR")}
            </p>
            <p className="aq-q">Q. {it.question}</p>
            {tab === "answered" && it.answer && <p className="aq-a">A. {it.answer}</p>}
            <textarea className="aq-ta" placeholder={tab === "answered" ? "답변 수정..." : "답변 작성 (채택만 할 때는 비워둬도 돼요)"}
              value={answers[it.id] || ""}
              onChange={(e) => setAnswers((a) => ({ ...a, [it.id]: e.target.value }))} />
            <div className="aq-row">
              {tab === "pending" && (
                <button className="aq-btn aq-adopt" onClick={() => act(it.id, { status: "adopted" })}>
                  채택 (답변 예정)
                </button>
              )}
              {tab !== "answered" ? (
                <button className="aq-btn aq-done" disabled={!(answers[it.id] || "").trim()}
                  onClick={() => act(it.id, { status: "answered", answer: (answers[it.id] || "").trim() })}>
                  답변 완료로 저장
                </button>
              ) : (
                <button className="aq-btn aq-done" disabled={!(answers[it.id] || "").trim()}
                  onClick={() => act(it.id, { answer: (answers[it.id] || "").trim() })}>
                  답변 수정 저장
                </button>
              )}
              <button className="aq-btn aq-discard" onClick={() => { if (window.confirm("이 질문을 폐기할까요?")) act(it.id, { status: "discarded" }); }}>폐기</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
