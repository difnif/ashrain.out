// 시록고 「강사도구」 — PC 강사도구를 웹으로 옮긴 것 (2026-11-23)
// 화면은 tt/ui.js(PC 화면 그대로), 자료는 Supabase(tt_* 표 · teacher-tool 저장 공간의 <uid>/tt/), PDF 일은 tt/engine (브라우저 안).
// 해시: #/tt/today[/날짜] · #/tt/grade[/코드[/학생]] · #/tt/convert · #/tt/register · #/tt/class · #/tt/students · #/tt/prints · #/tt/print/코드 · #/tt/export · #/tt/log · #/tt/import
//       #/tt/inbox (vFlat 등에서 「공유 → 강사도구」로 받은 스캔본 — public/tt-sw.js 가 연다)
import { useEffect, useRef } from "react";
import "./tt/tt.css";

const SKELETON = `
<header class="top">
  <div class="brand">강사도구 <span class="brand-sub">웹</span></div>
  <nav class="tabs" id="tt-tabs">
    <a href="#/tt/today" data-tab="today">오늘</a>
    <a href="#/tt/convert" data-tab="convert">매쓰플랫 변환</a>
    <a href="#/tt/register" data-tab="register">프린트 등록</a>
    <a href="#/tt/grade" data-tab="grade">채점</a>
    <a href="#/tt/class" data-tab="class">수업 기록</a>
    <a href="#/tt/students" data-tab="students">학생</a>
    <a href="#/tt/prints" data-tab="prints">프린트함</a>
    <a href="#/tt/books" data-tab="books">교재</a>
    <a href="#/tt/export" data-tab="export">내보내기</a>
    <a href="#/tt/log" data-tab="log">업무 기록</a>
    <a href="#/tt/import" data-tab="import" class="tt-mig">옮겨 오기</a>
    <a href="#/tt/inbox" data-tab="inbox" id="tt-inboxTab" class="tt-inbox" hidden>받은 스캔본</a>
  </nav>
  <form class="codebox" id="tt-codeForm" autocomplete="off">
    <input id="tt-codeInput" placeholder="프린트 코드" maxlength="9" aria-label="프린트 코드">
    <button type="submit">채점 열기</button>
  </form>
</header>
<main id="tt-view"></main>
<div id="tt-modal" class="modal" hidden><div class="modal-box" id="tt-modalBox"></div></div>
<div id="tt-toast" class="toast" hidden></div>`;

export default function TeacherTool() {
  const ref = useRef(null);
  useEffect(() => {
    const root = ref.current;
    root.innerHTML = SKELETON;
    if (!/^#\/tt\/./.test(location.hash)) history.replaceState(null, "", "#/tt/today");      // 처음 열면 「오늘」(결석부 · 확인할 것)
    let off = null, dead = false;
    import("./tt/ui.js").then(({ mountTeacherTool }) => {
      if (!dead) off = mountTeacherTool(root);
    }).catch((e) => {
      const v = root.querySelector("#tt-view");
      if (v) v.innerHTML = `<div class="card"><h2>강사도구를 열지 못했어요</h2><p class="sub">${String(e && e.message || e)}</p></div>`;
    });
    return () => { dead = true; if (off) off(); root.innerHTML = ""; };
  }, []);
  return <div ref={ref} className="tt-root" />;
}
