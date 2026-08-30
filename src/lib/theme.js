import { useEffect, useState } from "react";

// 앱 전역 테마: 'dark'(기본) | 'light'
// v2: 인스턴스별 useState → 모듈 공유 스토어. 어디서 토글해도 전 컴포넌트가 함께 바뀐다.
const KEY = "ashrain-theme";

let current = localStorage.getItem(KEY) || "dark";
const subs = new Set();

function apply(t) {
  current = t;
  localStorage.setItem(KEY, t);
  document.documentElement.dataset.theme = t;
  subs.forEach((fn) => fn(t));
}

// 첫 로드 시 문서에 반영 + 다른 탭과 동기화
document.documentElement.dataset.theme = current;
window.addEventListener("storage", (e) => {
  if (e.key === KEY && e.newValue && e.newValue !== current) apply(e.newValue);
});

export function useTheme() {
  const [theme, setTheme] = useState(current);
  useEffect(() => {
    subs.add(setTheme);
    return () => subs.delete(setTheme);
  }, []);
  return { theme, toggle: () => apply(current === "light" ? "dark" : "light") };
}
