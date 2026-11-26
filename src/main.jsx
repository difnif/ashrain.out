import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./shared/theme/tokens.css";

// 새 판이 올라간 뒤, 그전에 열어 둔 화면이 옛 조각 파일(…-해시.js)을 불러오다 실패하면
// (「Failed to fetch dynamically imported module」) 한 번 새로고침해 새 판을 받는다.
// 1분 안에 또 실패하면 되풀이하지 않고 오류를 그대로 보인다. 저장 안 된 채점이 있으면 브라우저가 떠날지 먼저 묻는다.
window.addEventListener("vite:preloadError", (e) => {
  let last = 0;
  try { last = Number(sessionStorage.getItem("ash:reloadNewBuild") || 0); } catch { /* 저장 공간 없음 */ }
  if (Date.now() - last < 60000) return;
  e.preventDefault();
  try { sessionStorage.setItem("ash:reloadNewBuild", String(Date.now())); } catch { /* */ }
  window.location.reload();
});

createRoot(document.getElementById("root")).render(
  <React.StrictMode><App /></React.StrictMode>
);
