// 학습 도구 탭 (#/tools) — 보조 기능 8종 모음 (셸이 상·하단을 그린다)
// sub: '' | wrong | ask | omr | hint | read | mark | essay | calc — 서브탭이 고른 도구만 크게 보여준다(무신사식 필터).
export const TOOLS = [
  { key: "wrong", ic: "📕", nm: "오답노트", ds: "틀린 문제를 모아 다시 풀고 정리해요. 세트·시험에서 틀린 문항이 자동으로 쌓여요.", to: "#/learn/wrong" },
  { key: "ask",   ic: "💬", nm: "질문하기", ds: "개념 단락이나 문항에서 바로 질문하고, 답변을 게시판에서 확인해요.", to: "#/board/qna" },
  { key: "omr",   ic: "📷", nm: "사진 채점", ds: "시험지를 뽑아 풀고 답안 카드를 찍으면 자동으로 채점돼요.", to: "#/solve/omr" },
  { key: "hint",  ic: "🗝️", nm: "사진 힌트", ds: "막힌 문제를 찍으면 답 대신 첫걸음을 알려줘요.", to: "#/learn/hint" },
  { key: "read",  ic: "🔍", nm: "문장 해설", ds: "문제 문장에서 숫자·척도·단서 경계를 짚고 무엇을 구하는지 정리해요.", to: "#/solve/read" },
  { key: "mark",  ic: "✍️", nm: "표시 연습", ds: "동그라미·밑줄·빗금으로 문제에 표시하는 습관을 연습해요.", to: "#/solve/mark" },
  { key: "essay", ic: "📝", nm: "서술형 자가채점", ds: "풀이를 쓰고 채점 기준표로 스스로 점수를 매겨 봐요.", to: "#/solve/essay" },
  { key: "calc",  ic: "🧮", nm: "스피드 연산", ds: "제한 시간 안에 연산을 푸는 훈련이에요.", to: "#/learn/calc" },
  { key: "photo", ic: "📸", nm: "찍어서 배우기", ds: "문제를 찍으면 문장 이해·표시 연습·서술형 채점·풀이과정 검사로 이어져요. 하단 우물을 눌러도 열려요.", to: "#/solve/photo" },
];

const CSS = `
.tl-root { min-height: 100vh; padding: 12px 14px 96px; box-sizing: border-box; background: var(--pbg);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; color: var(--text); }
.tl-root * { box-sizing: border-box; }
.tl-light { --pbg:#EDEFF2; --text:#1F2937; --muted:#8A929C; --surface:#fff; --border:#DFE3E8; --accent:#0D9488; }
.tl-dark { --pbg:#0B0C0F; --text:#E2E8F0; --muted:#8A929C; --surface:#15171C; --border:#23262D; --accent:#5EEAD4; }
.tl-wrap { max-width: 680px; margin: 0 auto; }
.tl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
@media (max-width: 380px) { .tl-grid { grid-template-columns: 1fr; } }
.tl-card { display: flex; flex-direction: column; gap: 5px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 14px 13px; text-align: left; color: var(--text); cursor: pointer; font-family: inherit; }
.tl-card .ic { font-size: 20px; }
.tl-card .nm { font-size: 13.5px; font-weight: 800; }
.tl-card .ds { font-size: 11px; color: var(--muted); line-height: 1.55; }
.tl-card.big { grid-column: 1 / -1; padding: 18px 16px; }
.tl-card.big .ic { font-size: 26px; }
.tl-card.big .nm { font-size: 16px; }
.tl-card.big .ds { font-size: 12.5px; line-height: 1.65; }
.tl-go { align-self: flex-start; margin-top: 8px; background: var(--accent); border: none; border-radius: 999px;
  color: #fff; font-size: 12.5px; font-weight: 800; padding: 8px 16px; cursor: pointer; font-family: inherit; }
.tl-dark .tl-go { color: #08302B; }
.tl-note { font-size: 12px; color: var(--muted); margin: 10px 2px 0; line-height: 1.6; }
`;

export default function Tools({ sub = "", theme = "light" }) {
  const key = (sub || "").split("?")[0].split("/")[0];
  const one = TOOLS.find((t) => t.key === key) || null;
  const list = one ? [one] : TOOLS;
  return (
    <div className={`tl-root tl-${theme}`}>
      <style>{CSS}</style>
      <div className="tl-wrap">
        <div className="tl-grid">
          {list.map((t) => (
            <button key={t.key} className={"tl-card" + (one ? " big" : "")}
              onClick={() => (location.hash = t.to)}>
              <span className="ic">{t.ic}</span>
              <span className="nm">{t.nm}</span>
              <span className="ds">{t.ds}</span>
              {one && <span className="tl-go">바로 시작 →</span>}
            </button>
          ))}
        </div>
        {!one && <p className="tl-note">공부(개념·연습문제·시험)는 아래 「공부하기」 탭에, 여기는 공부를 돕는 도구들이에요.</p>}
      </div>
    </div>
  );
}
