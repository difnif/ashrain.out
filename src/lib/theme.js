import { useEffect, useState } from "react";

// 앱 전역 테마: 'light'(비 오는 거리) | 'dark'(재의 밤)
const KEY = "ashrain-theme";

export function useTheme() {
  const [theme, setTheme] = useState(() => localStorage.getItem(KEY) || "light");
  useEffect(() => {
    localStorage.setItem(KEY, theme);
    document.documentElement.dataset.theme = theme;
  }, [theme]);
  return { theme, toggle: () => setTheme((t) => (t === "light" ? "dark" : "light")) };
}
