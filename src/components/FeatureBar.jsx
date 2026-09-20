// 기능 페이지 상단 바 — 셸(탭바·서브탭)이 사라진 화면의 유일한 이동 수단.
// ⌂(대시보드 복귀, 앱 전환 토글 없음) · ←(뒤로) · 제목 · 기능별 컨텍스트 버튼(actions).
// props
//   theme    'light' | 'dark'
//   title    문자열 (필수) · sub: 제목 옆 작은 보조 텍스트
//   back     해시 문자열("#/study") 또는 함수. 없으면 history.back(), 히스토리가 없으면 대시보드
//   actions  ReactNode — <button className="fb-act">…</button> 나 <FbAct> 를 나열
// 사용: <FeatureBar theme={theme} title="정수와 유리수" back="#/study/concept"
//         actions={<FbAct pri onClick={…}>🔁 복습</FbAct>} />
export default function FeatureBar({ theme = "light", title, sub, back, actions }) {
  const goBack = () => {
    if (typeof back === "function") return back();
    if (typeof back === "string") { location.hash = back; return; }
    if (window.history.length > 1) window.history.back();
    else location.hash = "";
  };
  return (
    <div className={"fb fb-" + theme}>
      <style>{FB_CSS}</style>
      <div className="fb-in">
        <button className="fb-ic" title="대시보드로" aria-label="대시보드로" onClick={() => (location.hash = "")}>⌂</button>
        <button className="fb-ic" title="뒤로" aria-label="뒤로" onClick={goBack}>←</button>
        <span className="fb-title">{title}{sub && <span className="fb-sub"> · {sub}</span>}</span>
        {actions}
      </div>
    </div>
  );
}

/** 컨텍스트 버튼 — pri 면 강조색 */
export function FbAct({ pri, onClick, title, children }) {
  return (
    <button className={"fb-act" + (pri ? " pri" : "")} onClick={onClick} title={title}>{children}</button>
  );
}

const FB_CSS = `
.fb { position: sticky; top: 0; z-index: 60; font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.fb * { box-sizing: border-box; }
.fb-light { background: #EDEFF2; --card:#fff; --bd:#DFE3E8; --ink:#1F2937; --mut:#8A929C; --ac:#0D9488; }
.fb-dark  { background: #0B0C0F; --card:#15171C; --bd:#23262D; --ink:#E2E8F0; --mut:#6B7280; --ac:#5EEAD4; }
.fb-in { max-width: 680px; margin: 0 auto; display: flex; align-items: center; gap: 6px; padding: 8px 12px; border-bottom: 1px solid var(--bd); }
.fb-ic { width: 34px; height: 34px; flex: none; border-radius: 10px; background: var(--card); border: 1px solid var(--bd);
  color: var(--ink); font-size: 15px; cursor: pointer; }
.fb-title { flex: 1; min-width: 0; font-size: 14.5px; font-weight: 800; color: var(--ink);
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fb-sub { font-size: 12px; font-weight: 600; color: var(--mut); }
.fb-act { flex: none; height: 34px; border-radius: 999px; background: var(--card); border: 1px solid var(--bd);
  color: var(--ink); font-size: 12px; font-weight: 700; padding: 0 12px; cursor: pointer; }
.fb-act.pri { background: var(--ac); border-color: var(--ac); color: #fff; }
.fb-dark .fb-act.pri { color: #08302B; }
`;
