import { useEffect, useState, useSyncExternalStore } from "react";

// 앱 전역 테마: 'dark'(기본) | 'light'
// v2: 인스턴스별 useState → 모듈 공유 스토어. 어디서 토글해도 전 컴포넌트가 함께 바뀐다.
const KEY = "ashrain-theme";

let current = "dark";
try { current = localStorage.getItem(KEY) === "light" ? "light" : "dark"; } catch { /* 저장소를 못 쓰는 창 — 기본 다크 */ }
const subs = new Set();

const HAS_DOM = typeof document !== "undefined" && typeof window !== "undefined";   // 노드(시험 · 서버 그리기)에서도 불러올 수 있게

function apply(t) {
  current = t;
  try { localStorage.setItem(KEY, t); } catch { /* 저장 못 해도 이 창에서는 바뀐다 */ }
  if (HAS_DOM) document.documentElement.dataset.theme = t;
  subs.forEach((fn) => fn(t));
}

// 첫 로드 시 문서에 반영 + 다른 탭과 동기화
if (HAS_DOM) {
  document.documentElement.dataset.theme = current;
  window.addEventListener("storage", (e) => {
    if (e.key === KEY && e.newValue && e.newValue !== current) apply(e.newValue);
  });
}

export function useTheme() {
  const [theme, setTheme] = useState(current);
  useEffect(() => {
    subs.add(setTheme);
    setTheme(current);                 // 구독 전에 바뀐 값 따라잡기
    return () => subs.delete(setTheme);
  }, []);
  return { theme, toggle: () => apply(current === "light" ? "dark" : "light") };
}

// ── 테마 단추 자리 ───────────────────────────────────────────────────────────
// 화면 맨 위 막대(셸 상단 · 기능 막대)나 제 테마 단추가 있는 화면은 「자리」로 등록한다.
// 자리가 하나도 없을 때만 오른쪽 위에 떠 있는 단추(components/ThemeToggle.jsx 의 ThemeDock)가 나온다 — 단추가 둘 겹쳐 보이지 않게.
let hosts = 0;
const hostSubs = new Set();
const hostEmit = () => hostSubs.forEach((fn) => fn());

/** 이 컴포넌트가 떠 있는 동안 「테마 단추가 이미 있다」고 알린다 (active=false 면 알리지 않음) */
export function useThemeHost(active = true) {
  useEffect(() => {
    if (!active) return undefined;
    hosts += 1; hostEmit();
    return () => { hosts -= 1; hostEmit(); };
  }, [active]);
}

/** 지금 떠 있는 테마 단추 자리 수 */
export function useThemeHostCount() {
  return useSyncExternalStore(
    (fn) => { hostSubs.add(fn); return () => hostSubs.delete(fn); },
    () => hosts,
    () => 0,
  );
}
