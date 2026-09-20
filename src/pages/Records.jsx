// 기록 탭 (#/records) — 촬영 학습 기록(기기 보관소)을 셸(탭바) 안에서 본다.
// 구 게시판 탭 자리(사용자 확정 2026-09-20). 게시판(#/board)은 라우트만 잠들어 있고,
// 종성(학부모앱) 작업 때 정교화해서 다시 연다.
import PhotoMine from "./photo/PhotoMine";
import "./solve/solve.css";

const CSS = `
.rc-root { min-height: 100vh; padding: 14px 14px 96px; box-sizing: border-box; color: var(--text);
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; }
.rc-wrap { max-width: 680px; margin: 0 auto; }
.rc-h { margin: 2px 2px 12px; font-size: 17px; font-weight: 800; }
`;

export default function Records() {
  return (
    <div className="rc-root">
      <style>{CSS}</style>
      <div className="rc-wrap">
        <p className="rc-h">🗂 기록</p>
        <PhotoMine embed />
      </div>
    </div>
  );
}
