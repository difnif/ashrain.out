// ashrain.out — 질문챗 (v1.0)
// 물음표 → 하단 시트: 질문 입력 → [AI에게 바로 / 선생님께 남기기 / 비슷한 질문 찾기]
// AI 대화는 현재 전면 무료 (안전 한도만 서버에서 관리, 유료 세팅은 추후)
import { useEffect, useRef, useState } from "react";
import { supabase } from "../supabaseClient";
import { askQuestion } from "../lib/concepts";
import { api } from "../lib/authx";
import { qcode } from "../lib/qcode";

const CSS = `
.qch-dim { position: fixed; inset: 0; background: rgba(0,0,0,.35); z-index: 60; }
.qch-sheet { position: fixed; left: 0; right: 0; bottom: 0; z-index: 61; max-width: 640px; margin: 0 auto;
  background: var(--card); border: 1px solid var(--bd); border-bottom: none; border-radius: 18px 18px 0 0;
  display: flex; flex-direction: column; max-height: 74vh;
  animation: qchUp .22s ease-out; box-shadow: 0 -8px 30px rgba(0,0,0,.18);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
@keyframes qchUp { from { transform: translateY(40px); opacity: .4; } to { transform: translateY(0); opacity: 1; } }
.qch-light { --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0DA95F; --in:#F4F6F8; --inbd:#D3D9DF; --me:#E7F7EF; }
.qch-dark  { --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#FFE03C; --in:#101116; --inbd:#2B2E36; --me:#1E2A22; }
.qch-head { display: flex; align-items: center; gap: 8px; padding: 13px 16px 10px; border-bottom: 1px solid var(--bd); }
.qch-code { font-size: 11px; font-weight: 800; letter-spacing: .5px; color: var(--mut);
  border: 1px solid var(--bd); border-radius: 6px; padding: 3px 6px; }
.qch-t { flex: 1; min-width: 0; color: var(--ink); font-size: 14px; font-weight: 800;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.qch-x { background: none; border: none; color: var(--mut); font-size: 17px; cursor: pointer; padding: 2px 4px; }
.qch-body { flex: 1; overflow-y: auto; padding: 14px 16px; }
.qch-m { margin-bottom: 10px; display: flex; }
.qch-m.me { justify-content: flex-end; }
.qch-b { max-width: 86%; border: 1px solid var(--bd); border-radius: 13px; padding: 9px 12px;
  font-size: 14px; line-height: 1.6; color: var(--ink); white-space: pre-wrap; word-break: break-word; background: var(--in); }
.qch-m.me .qch-b { background: var(--me); }
.qch-who { display: block; font-size: 10.5px; font-weight: 800; color: var(--mut); margin-bottom: 2px; }
.qch-chips { display: flex; flex-wrap: wrap; gap: 7px; margin: 2px 0 12px; }
.qch-chip { background: var(--card); border: 1.5px solid var(--ac); border-radius: 999px; color: var(--ac);
  font-size: 12.5px; font-weight: 800; padding: 8px 13px; cursor: pointer; }
.qch-chip.sub { border-color: var(--inbd); color: var(--mut); font-weight: 700; }
.qch-sim { border: 1px solid var(--bd); border-radius: 11px; padding: 10px 12px; margin-bottom: 8px; cursor: pointer;
  display: flex; align-items: center; gap: 8px; background: var(--card); }
.qch-sim-q { flex: 1; min-width: 0; color: var(--ink); font-size: 13px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.qch-sim-s { font-size: 10.5px; font-weight: 800; color: var(--ac); white-space: nowrap; }
.qch-think { color: var(--mut); font-size: 12.5px; margin: 2px 0 10px; }
.qch-inbar { display: flex; gap: 8px; align-items: flex-end; padding: 10px 14px calc(12px + env(safe-area-inset-bottom));
  border-top: 1px solid var(--bd); }
.qch-ta { flex: 1; min-height: 42px; max-height: 120px; background: var(--in); border: 1px solid var(--inbd);
  border-radius: 12px; color: var(--ink); font-size: 14.5px; padding: 10px 12px; outline: none; resize: none; box-sizing: border-box; }
.qch-send { background: var(--ac); border: none; border-radius: 12px; font-weight: 800; font-size: 14px;
  padding: 11px 15px; cursor: pointer; flex-shrink: 0; }
.qch-light .qch-send { color: #fff; } .qch-dark .qch-send { color: #14140F; }
.qch-send:disabled { opacity: .5; }
`;

let seq = 0;
const mk = (kind, text, extra) => ({ id: ++seq, kind, text, ...extra });

export default function QuestionChat({ conceptId, block, theme = "light", answered = [], onClose }) {
  const code = qcode(conceptId, block?.id);
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [aiMode, setAiMode] = useState(false);   // 이후 입력이 AI 대화로 이어짐
  const [firstQ, setFirstQ] = useState("");
  const [hist, setHist] = useState([]);          // AI용 { role, content }
  const endRef = useRef(null);

  useEffect(() => {
    const first = [mk("bot", `이 단락에서 무엇이 궁금한가요?\n편하게 물어보세요 😊`)];
    if (answered.length) first.push(mk("chips", "", { chips: [["seen", `💬 이 단락의 질문 ${answered.length}개 보기`]], sub: true }));
    setMsgs(first);
  }, []); // eslint-disable-line

  useEffect(() => { endRef.current?.scrollIntoView({ block: "end" }); }, [msgs, busy]);

  const push = (...m) => setMsgs((s) => [...s, ...m]);

  const callAI = async (history) => {
    setBusy(true);
    try {
      const r = await api("ai", {
        task: "ask", concept_id: conceptId, block_id: block.id, q_code: code,
        block_json: JSON.stringify(block), messages: history,
      }, { auth: true });
      setHist([...history, { role: "assistant", content: r.reply }]);
      push(mk("ai", r.reply), mk("chips", "", { chips: [["teacher2", "👨‍🏫 이 내용, 선생님께도 남기기"]], sub: true }));
    } catch (e) {
      push(mk("bot", "⚠ " + e.message));
    } finally { setBusy(false); }
  };

  const send = () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    push(mk("me", text));
    if (aiMode) {
      const h = [...hist, { role: "user", content: text }];
      setHist(h); callAI(h);
    } else {
      setFirstQ(text);
      push(mk("bot", "어떻게 도와드릴까요?"),
        mk("chips", "", { chips: [["ai", "🤖 AI에게 바로 물어보기"], ["teacher", "👨‍🏫 선생님께 남기기"], ["similar", "🔍 비슷한 질문 찾기"]] }));
    }
  };

  const onChip = async (key) => {
    setMsgs((s) => s.filter((m) => m.kind !== "chips")); // 선택지 정리
    if (key === "ai") {
      setAiMode(true);
      const h = [{ role: "user", content: firstQ }];
      setHist(h); await callAI(h);
    }
    if (key === "teacher" || key === "teacher2") {
      try {
        await askQuestion(conceptId, block.id, firstQ);
        push(mk("bot", "선생님께 전달했어요! ✉️\n채택되면 질문게시판에 익명 질문글로 올라와요."));
      } catch (e) { push(mk("bot", "⚠ 전달 실패: " + e.message)); }
    }
    if (key === "similar" || key === "seen") {
      const { data } = await supabase.from("concept_qna")
        .select("id, block_id, question, status")
        .eq("concept_id", conceptId).in("status", ["adopted", "answered"]).limit(100);
      let list = data || [];
      if (key === "seen") list = list.filter((q) => String(q.block_id) === String(block.id));
      else {
        const words = firstQ.split(/\s+/).filter((w) => w.length >= 2);
        list = list.map((q) => ({ ...q,
          _s: (String(q.block_id) === String(block.id) ? 3 : 0) + words.filter((w) => q.question.includes(w)).length,
        })).sort((a, b) => b._s - a._s).filter((q) => q._s > 0);
      }
      list = list.slice(0, 5);
      if (!list.length) {
        push(mk("bot", key === "seen" ? "아직 이 단락에 등록된 질문이 없어요." : "비슷한 질문을 찾지 못했어요. 대신 —"),
          mk("chips", "", { chips: [["ai", "🤖 AI에게 물어보기"], ["teacher", "👨‍🏫 선생님께 남기기"]] }));
      } else {
        push(mk("sim", "", { list }));
        if (key === "similar") push(mk("chips", "", { chips: [["ai", "🤖 그래도 AI에게 물어보기"], ["teacher", "👨‍🏫 선생님께 남기기"]], sub: true }));
      }
    }
  };

  return (
    <>
      <div className="qch-dim" onClick={onClose} />
      <div className={`qch-sheet qch-${theme}`}>
        <style>{CSS}</style>
        <div className="qch-head">
          <span className="qch-code">{code}</span>
          <span className="qch-t">{block?.label || "질문하기"}</span>
          <button className="qch-x" onClick={onClose}>✕</button>
        </div>
        <div className="qch-body">
          {msgs.map((m) => {
            if (m.kind === "chips") return (
              <div key={m.id} className="qch-chips">
                {m.chips.map(([k, label]) => (
                  <button key={k} className={"qch-chip" + (m.sub ? " sub" : "")} onClick={() => onChip(k)}>{label}</button>
                ))}
              </div>
            );
            if (m.kind === "sim") return (
              <div key={m.id}>
                {m.list.map((q) => (
                  <div key={q.id} className="qch-sim" onClick={() => { onClose(); location.hash = `#/board/${q.id}`; }}>
                    <span className="qch-sim-q">{q.question}</span>
                    <span className="qch-sim-s">{q.status === "answered" ? "답변 완료" : "답변 예정"}</span>
                  </div>
                ))}
              </div>
            );
            const me = m.kind === "me";
            return (
              <div key={m.id} className={"qch-m" + (me ? " me" : "")}>
                <div className="qch-b">
                  {m.kind === "ai" && <span className="qch-who">🤖 AI 도우미</span>}
                  {m.text}
                </div>
              </div>
            );
          })}
          {busy && <p className="qch-think">AI가 생각하는 중…</p>}
          <div ref={endRef} />
        </div>
        <div className="qch-inbar">
          <textarea className="qch-ta" value={input}
            placeholder={aiMode ? "꼬리 질문을 이어서 물어보세요" : "궁금한 점을 적어보세요"}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }} />
          <button className="qch-send" onClick={send} disabled={busy || !input.trim()}>보내기</button>
        </div>
      </div>
    </>
  );
}
