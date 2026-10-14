// 서술형 평가 화면 스타일 (/e — 학생앱 셸 밖 단독 페이지라 자기 색 토큰을 가진다)
export const ASSESS_CSS = `
.as-root { min-height: 100vh; background: var(--bg); color: var(--ink); -webkit-tap-highlight-color: transparent;
  font-family: 'Pretendard Variable', Pretendard, 'Malgun Gothic', system-ui, sans-serif; font-size: 15px; line-height: 1.5; }
.as-root * { box-sizing: border-box; }
.as-light { --bg:#F2F1EC; --card:#fff; --ink:#1D1F24; --mut:#6B6E76; --bd:#E2E0DA; --soft:#ECEBE6; --ac:#0D7C70; --ac2:#E7F4F1;
  --ok:#15803D; --okbg:#E8F5EC; --warn:#B45309; --warnbg:#FEF3E2; --bad:#B91C1C; --badbg:#FDECEC; --shadow:0 1px 2px rgba(0,0,0,.06); }
.as-dark { --bg:#14161A; --card:#1E2026; --ink:#ECEBE7; --mut:#9A9CA4; --bd:#2E3038; --soft:#262830; --ac:#5EEAD4; --ac2:#173A36;
  --ok:#4ADE80; --okbg:#173322; --warn:#FBBF24; --warnbg:#3A2E12; --bad:#F87171; --badbg:#3A1A1A; --shadow:none; color-scheme: dark; }
.as-wrap { max-width: 640px; margin: 0 auto; padding: 10px 16px 64px; }
.as-top { position: sticky; top: 0; z-index: 20; background: var(--bg); display: flex; align-items: center; gap: 8px;
  padding: 10px 0 8px; border-bottom: 1px solid var(--bd); margin-bottom: 12px; }
.as-ic { width: 34px; height: 34px; flex: none; border-radius: 10px; background: var(--card); border: 1px solid var(--bd);
  color: var(--ink); font-size: 15px; cursor: pointer; }
.as-tt { flex: 1; min-width: 0; }
.as-tt b { display: block; font-size: 15px; font-weight: 800; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.as-tt small { display: block; font-size: 11.5px; color: var(--mut); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.as-card { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 16px; box-shadow: var(--shadow); margin-bottom: 12px; }
.as-card h2 { margin: 0 0 6px; font-size: 18px; font-weight: 800; letter-spacing: -.01em; }
.as-card h3 { margin: 0 0 8px; font-size: 14.5px; font-weight: 800; }
.as-mut { color: var(--mut); font-size: 13px; }
.as-small { font-size: 12px; color: var(--mut); line-height: 1.6; }
.as-kick { font-size: 11.5px; font-weight: 800; letter-spacing: .08em; color: var(--ac); margin: 0 0 4px; }
.as-facts { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0 2px; }
.as-chip { display: inline-flex; align-items: center; gap: 5px; font-size: 12px; font-weight: 700; padding: 5px 10px;
  border-radius: 999px; background: var(--soft); color: var(--ink); }
.as-btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; border: 1.5px solid var(--bd); background: var(--card);
  color: var(--ink); font: inherit; font-weight: 800; font-size: 14px; padding: 11px 16px; border-radius: 12px; cursor: pointer; }
.as-btn.pri { background: var(--ac); border-color: var(--ac); color: #fff; }
.as-dark .as-btn.pri { color: #06302A; }
.as-btn.ghost { background: transparent; border-color: transparent; color: var(--mut); }
.as-btn.wide { width: 100%; }
.as-btn:disabled { opacity: .45; cursor: default; }
.as-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.as-row > .as-btn { flex: 1 1 140px; }
.as-note { display: flex; gap: 8px; align-items: flex-start; padding: 10px 12px; border-radius: 12px; font-size: 13px; line-height: 1.55; margin-top: 10px; }
.as-note.ok { background: var(--okbg); color: var(--ok); }
.as-note.warn { background: var(--warnbg); color: var(--warn); }
.as-note.bad { background: var(--badbg); color: var(--bad); }
.as-note.info { background: var(--ac2); color: var(--ink); }
.as-note b { font-weight: 800; }
.as-list { display: flex; flex-direction: column; gap: 8px; }
.as-item { display: flex; align-items: center; gap: 10px; width: 100%; text-align: left; background: var(--card); border: 1px solid var(--bd);
  border-radius: 14px; padding: 12px 14px; color: var(--ink); font: inherit; cursor: pointer; }
.as-item .ic { flex: none; font-size: 20px; }
.as-item .tx { flex: 1; min-width: 0; }
.as-item .tx b { display: block; font-size: 14.5px; font-weight: 800; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.as-item .tx small { display: block; font-size: 12px; color: var(--mut); }
.as-item .rt { flex: none; font-size: 12.5px; font-weight: 800; color: var(--ac); }
.as-new { display: inline-block; font-size: 10px; font-weight: 900; color: #fff; background: #EF4444; border-radius: 999px; padding: 1px 6px; margin-left: 6px; vertical-align: 2px; }
.as-sec { font-size: 12.5px; font-weight: 800; color: var(--mut); margin: 18px 2px 8px; }
/* 문제 열람 */
.as-q { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 14px 15px; margin-bottom: 10px; }
.as-qh { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.as-qn { flex: none; background: var(--ink); color: var(--card); font-weight: 900; font-size: 12.5px; border-radius: 8px; padding: 3px 9px; }
.as-qt { font-size: 12px; font-weight: 700; color: var(--mut); }
.as-qp { margin-left: auto; font-size: 11.5px; color: var(--mut); }
.as-qbody { font-size: 15.5px; line-height: 1.75; }
.as-qbody .ask { font-weight: 800; margin-top: 8px; }
.as-qbody .conds { margin: 8px 0 0; padding: 8px 12px; border-radius: 10px; background: var(--soft); list-style: none; }
.as-fig { margin: 10px auto 2px; display: flex; justify-content: center; }
.as-fig img { max-width: min(100%, 300px); height: auto; background: #fff; border-radius: 8px; padding: 6px; }
.as-els { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 10px; }
.as-els span { font-size: 11.5px; font-weight: 700; color: var(--mut); border: 1px solid var(--bd); border-radius: 999px; padding: 3px 8px; }
.as-check { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-radius: 14px; border: 1.5px solid var(--bd); background: var(--card);
  font-weight: 700; font-size: 14px; cursor: pointer; margin-top: 4px; }
.as-check input { width: 20px; height: 20px; accent-color: var(--ac); }
/* 촬영 */
.as-steps { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding: 2px 0 10px; }
.as-steps::-webkit-scrollbar { display: none; }
.as-st { flex: none; min-width: 42px; height: 42px; border-radius: 12px; border: 1.5px solid var(--bd); background: var(--card); color: var(--mut);
  font: inherit; font-weight: 800; font-size: 13px; display: flex; flex-direction: column; align-items: center; justify-content: center; line-height: 1.05; cursor: pointer; position: relative; }
.as-st small { font-size: 9.5px; font-weight: 700; }
.as-st.cur { border-color: var(--ac); color: var(--ac); box-shadow: 0 0 0 3px var(--ac2); }
.as-st.done { background: var(--okbg); border-color: transparent; color: var(--ok); }
.as-st.busy { background: var(--ac2); border-color: transparent; color: var(--ink); }
.as-st.err { background: var(--badbg); border-color: transparent; color: var(--bad); }
.as-st.busy::after { content: ""; position: absolute; top: 4px; right: 4px; width: 6px; height: 6px; border-radius: 50%; background: var(--ac); animation: as-pulse 1.1s ease-in-out infinite; }
@keyframes as-pulse { 0%,100% { opacity: 1 } 50% { opacity: .25 } }
.as-shoot { display: grid; grid-template-columns: 96px 1fr; gap: 14px; align-items: start; }
.as-art { width: 96px; height: 136px; display: block; color: var(--ink); }
.as-gl { margin: 6px 0 0; padding: 0 0 0 18px; font-size: 13.5px; line-height: 1.6; }
.as-gl li { margin: 2px 0; }
.as-cam { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; width: 100%; min-height: 108px; margin-top: 14px;
  border: 2px dashed var(--ac); border-radius: 16px; background: var(--ac2); color: var(--ink); font: inherit; cursor: pointer; }
.as-cam .ic { font-size: 30px; line-height: 1; }
.as-cam b { font-size: 16px; font-weight: 900; }
.as-cam small { font-size: 12px; color: var(--mut); }
.as-flash { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 14px; background: var(--okbg); color: var(--ok); margin-top: 12px; font-weight: 800; }
.as-flash img { width: 52px; height: 74px; object-fit: cover; border-radius: 6px; border: 1px solid var(--bd); background: #fff; }
.as-busy { display: flex; align-items: center; gap: 10px; padding: 14px; color: var(--mut); font-size: 14px; }
.as-sp { width: 18px; height: 18px; border-radius: 50%; border: 2.5px solid var(--bd); border-top-color: var(--ac); animation: as-spin .8s linear infinite; flex: none; }
@keyframes as-spin { to { transform: rotate(360deg) } }
.as-prog { height: 8px; border-radius: 999px; background: var(--soft); overflow: hidden; margin: 10px 0 4px; }
.as-prog > i { display: block; height: 100%; background: var(--ac); border-radius: 999px; transition: width .4s ease; }
/* 2쪽 확인 */
.as-form { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
.as-form label { display: flex; flex-direction: column; gap: 4px; font-size: 12px; font-weight: 800; color: var(--mut); }
.as-form label.full { grid-column: 1 / -1; }
.as-form input, .as-form select { font: inherit; font-size: 15px; padding: 10px 12px; border-radius: 10px; border: 1.5px solid var(--bd); background: var(--card); color: var(--ink); }
/* 결과 */
.as-score { display: flex; align-items: baseline; gap: 6px; }
.as-score b { font-size: 40px; font-weight: 900; letter-spacing: -.02em; line-height: 1; }
.as-score span { font-size: 16px; font-weight: 800; color: var(--mut); }
.as-res { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 14px 15px; margin-bottom: 10px; }
.as-res .hd { display: flex; align-items: center; gap: 8px; }
.as-res .hd .pt { margin-left: auto; font-size: 18px; font-weight: 900; }
.as-res .hd .pt small { font-size: 12px; color: var(--mut); font-weight: 700; }
.as-els2 { display: flex; flex-direction: column; gap: 6px; margin-top: 10px; }
.as-el { display: grid; grid-template-columns: 1fr auto; gap: 2px 10px; padding: 8px 10px; border-radius: 10px; background: var(--soft); font-size: 13px; }
.as-el b { font-weight: 800; }
.as-el .g { font-weight: 900; text-align: right; }
.as-el .r { grid-column: 1 / -1; font-size: 12px; color: var(--mut); line-height: 1.5; }
.as-fb { margin: 10px 0 0; padding: 10px 12px; border-left: 3px solid var(--ac); background: var(--ac2); border-radius: 0 10px 10px 0; font-size: 13.5px; line-height: 1.6; }
.as-read { margin-top: 10px; }
.as-read summary { cursor: pointer; font-size: 12.5px; font-weight: 800; color: var(--mut); }
.as-read .bx { margin-top: 6px; padding: 8px 10px; border: 1px dashed var(--bd); border-radius: 10px; font-size: 13px; line-height: 1.6;
  font-family: 'Noto Sans KR', 'Pretendard Variable', system-ui, sans-serif; }
.as-read .bx i { font-style: normal; font-size: 11px; font-weight: 800; color: var(--mut); display: block; margin-bottom: 2px; }
.as-read .st { text-decoration: line-through; color: var(--mut); }
.as-key { margin-top: 10px; padding: 10px 12px; border-radius: 10px; border: 1.5px solid var(--ok); background: var(--okbg); font-size: 13.5px; line-height: 1.7; }
.as-key b { color: var(--ok); }
.as-flag { margin-top: 8px; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.as-flag input { flex: 1 1 180px; font: inherit; font-size: 13px; padding: 8px 10px; border-radius: 10px; border: 1.5px solid var(--bd); background: var(--card); color: var(--ink); }
.as-tiny { font-size: 12px; padding: 7px 11px; border-radius: 10px; }
.as-err { padding: 28px 18px; text-align: center; }
.as-err .ic { font-size: 34px; }
`;
