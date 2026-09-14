// 문항 질문하기 (#/solve/ask/<itemId>) — 기존 QuestionChat(개념 단락 질문)을 문항에 얹는다.
// block 은 문항 요약(정답·해설 없음). 선생님께 남기면 concept_qna 에 block_id "item:<id>" 로 들어간다.
import { useEffect, useState } from "react";
import { supabase } from "../../supabaseClient";
import QuestionChat from "../../components/QuestionChat";
import ItemQuestion from "../../components/ItemQuestion";
import SolveShell from "./SolveShell";
import { readAskItem } from "../../lib/ask";
import { fetchItem } from "../../lib/items";
import "./solve.css";

export default function AskItem({ itemId, theme }) {
  const [item, setItem] = useState(undefined);
  const [isAdmin, setIsAdmin] = useState(false);
  const [open, setOpen] = useState(true);

  useEffect(() => {
    let alive = true;
    (async () => {
      let it = null;
      const cached = readAskItem(itemId);
      try { it = await fetchItem(itemId); } catch { it = null; }
      if (!it && cached) it = { id: cached.id, question: cached.question, choices: cached.choices, qtype: cached.qtype, concept_ids: cached.concept_id ? [cached.concept_id] : [], unit_id: cached.unit_id };
      if (alive) setItem(it);
      const { data } = await supabase.auth.getUser();
      if (!data?.user || !alive) return;
      const { data: p } = await supabase.from("profiles").select("role").eq("id", data.user.id).maybeSingle();
      if (alive) setIsAdmin(p?.role === "admin");
    })();
    return () => { alive = false; };
  }, [itemId]);

  const back = () => { if (history.length > 1) history.back(); else location.hash = "#/solve"; };

  if (item === undefined) return <SolveShell title="질문하기"><div className="sv-muted">문항을 불러오는 중…</div></SolveShell>;
  if (!item) return <SolveShell title="질문하기"><div className="sv-empty">지금은 볼 수 없는 문항이에요.</div></SolveShell>;

  const conceptId = item.concept_ids?.[0] || "unknown";
  const block = {
    id: `item:${item.id}`,
    type: "item",
    label: "문항 질문",
    question: item.question,
    choices: Array.isArray(item.choices) ? item.choices : undefined,
    lines: [item.question],
  };

  return (
    <SolveShell title="질문하기" sub="이 문항에 대해 AI에게 묻거나 선생님께 남길 수 있어요. 답을 대신 풀어 주지는 않아요." back={null}
      right={<button className="sv-back" onClick={back}>← 돌아가기</button>}>
      <div className="sv-card">
        <ItemQuestion item={item} compact />
      </div>
      {!open && <button className="sv-btn pri full" onClick={() => setOpen(true)}>다시 질문하기</button>}
      {open && (
        <QuestionChat conceptId={conceptId} block={block} theme={theme} isAdmin={isAdmin}
          onClose={() => { setOpen(false); back(); }} />
      )}
    </SolveShell>
  );
}
