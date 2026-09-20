// 학습 도구 탭 (#/tools) — 열린 도구 5종 + 개발 중 3종(하단) (셸이 상·하단을 그린다)
// 2026-09-20 재편(사용자 확정): 찍어서 배우기(촬영 모듈) 기능들을 상위로 꺼내고,
// 서술형은 사진 촬영→인식→채점·첨삭(촬영 모듈)으로 교체, 스피드 연산은 삭제,
// 오답노트·질문하기·찰칵 채점(구 사진 채점)은 개발 중으로 하단 배치.
// sub: '' | essay | hint | read | mark | check — 서브탭이 고른 도구만 크게(무신사식 필터).

export const TOOLS_OPEN = [
  { key: "essay", ic: "📝", nm: "서술형 채점·첨삭", ds: "문제와 내 풀이를 사진으로 찍으면 알아보고, 기준표로 채점하고 첨삭까지 해줘요.", to: "#/solve/photo/essay" },
  { key: "hint",  ic: "🗝️", nm: "사진 힌트", ds: "막힌 문제를 찍으면 답 대신 첫걸음을 알려줘요.", to: "#/learn/hint" },
  { key: "read",  ic: "🔍", nm: "문장 해설", ds: "문제를 찍으면 단서마다 형광펜을 긋고, 무엇을 구하는지 정리해줘요.", to: "#/solve/photo/read" },
  { key: "mark",  ic: "✍️", nm: "표시 연습", ds: "동그라미·밑줄·빗금을 어디에 칠지 차례대로 보여주고, 직접 표시하며 연습해요.", to: "#/solve/photo/mark" },
  { key: "check", ic: "🔬", nm: "풀이과정 검사", ds: "푼 페이지를 통째로 찍으면 연결고리·암산·실수 습관을 진단해줘요.", to: "#/solve/photo/check" },
];

export const TOOLS_DEV = [
  { key: "wrong", ic: "📕", nm: "오답노트", ds: "틀린 문제가 자동으로 모여 다시 푸는 공간이에요." },
  { key: "ask",   ic: "💬", nm: "질문하기", ds: "개념·문항에서 바로 질문하고 답변을 받는 기능이에요." },
  { key: "omr",   ic: "📸", nm: "찰칵 채점", ds: "시험지를 뽑아 풀고 답안 카드를 찍으면 자동 채점되는 기능이에요." },
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
.tl-sec { margin: 16px 2px 8px; font-size: 12px; font-weight: 800; color: var(--muted); }
.tl-card.dev { opacity: .62; cursor: default; }
.tl-card.dev .nm { display: flex; align-items: center; gap: 6px; }
.tl-devb { flex: none; font-size: 9px; font-weight: 900; letter-spacing: .5px; color: #fff; background: #94A3B8;
  border-radius: 999px; padding: 2px 7px; }
.tl-dark .tl-devb { background: #475569; }
.tl-note { font-size: 12px; color: var(--muted); margin: 10px 2px 0; line-height: 1.6; }
`;

function OpenCard({ t, big = false }) {
  return (
    <button className={"tl-card" + (big ? " big" : "")} onClick={() => (location.hash = t.to)}>
      <span className="ic">{t.ic}</span>
      <span className="nm">{t.nm}</span>
      <span className="ds">{t.ds}</span>
      {big && <span className="tl-go">바로 시작 →</span>}
    </button>
  );
}

function DevCard({ t }) {
  return (
    <div className="tl-card dev" aria-disabled="true">
      <span className="ic">{t.ic}</span>
      <span className="nm">{t.nm} <span className="tl-devb">개발중</span></span>
      <span className="ds">{t.ds}</span>
    </div>
  );
}

export default function Tools({ sub = "", theme = "light" }) {
  const key = (sub || "").split("?")[0].split("/")[0];
  const one = TOOLS_OPEN.find((t) => t.key === key) || null;
  return (
    <div className={`tl-root tl-${theme}`}>
      <style>{CSS}</style>
      <div className="tl-wrap">
        {one ? (
          <div className="tl-grid"><OpenCard t={one} big /></div>
        ) : (
          <>
            <div className="tl-grid">
              {TOOLS_OPEN.map((t) => <OpenCard key={t.key} t={t} />)}
            </div>
            <p className="tl-sec">🚧 개발 중인 기능 — 준비되면 여기서 열려요</p>
            <div className="tl-grid">
              {TOOLS_DEV.map((t) => <DevCard key={t.key} t={t} />)}
            </div>
            <p className="tl-note">하단 가운데 우물을 눌러도 사진 도구들을 바로 열 수 있어요. 공부(개념·연습문제)는 「공부하기」 탭에 있어요.</p>
          </>
        )}
      </div>
    </div>
  );
}
