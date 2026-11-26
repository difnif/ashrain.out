// 다크/라이트 전환 단추 — 어느 화면에서든 맨 위에 하나.
//   <ThemeToggle className="…" />  위 막대(셸 상단 ShellTop · 기능 막대 FeatureBar) 오른쪽 끝에 넣는 단추. 막대의 단추 모양(className)을 그대로 쓴다.
//   <ThemeDock />                  막대가 없는 화면의 맨 위 오른쪽 단추 — App 에 한 번만 둔다.
//                                  막대 단추나 제 테마 단추가 있는 화면(로그인 · 교실 모니터 무대)이 하나라도 떠 있으면 숨는다(lib/theme useThemeHost).
//                                  화면에 고정(fixed)하지 않고 문서 맨 위에 둔다(absolute) — 내리면 함께 올라가 그 화면의 고정 머리줄
//                                  (예: 빠른 정답지의 단원 고르기 줄)을 가리지 않고, 전체 화면 창(해설 시트 · 팝업, z-index 50~)이 열리면 그 밑에 깔린다.
// 세이로코 · 종성(한지 단일 테마)은 다크가 없어 단추를 두지 않는다 — 떠 있는 단추도 학생앱(data-app="ashrain")에서만.
// 아이콘은 「누르면 바뀔 모드」: 다크일 때 해 · 라이트일 때 달 (로그인 화면 「🌙 다크 / 🌧 라이트」 단추와 같은 뜻).
import { useEffect, useState } from "react";
import { useTheme, useThemeHost, useThemeHostCount } from "../lib/theme";

const Sun = () => (
  <svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" focusable="false">
    <circle cx="12" cy="12" r="4.3" fill="currentColor" />
    <g stroke="currentColor" strokeWidth="2" strokeLinecap="round">
      <path d="M12 2.6v2.3M12 19.1v2.3M2.6 12h2.3M19.1 12h2.3M5.35 5.35l1.6 1.6M17.05 17.05l1.6 1.6M5.35 18.65l1.6-1.6M17.05 6.95l1.6-1.6" />
    </g>
  </svg>
);
const Moon = () => (
  <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false">
    <path d="M20.6 14.7A8.7 8.7 0 0 1 9.3 3.4a8.7 8.7 0 1 0 11.3 11.3z" fill="currentColor" />
  </svg>
);

const CSS = `
.thm-btn { display: inline-flex; align-items: center; justify-content: center; padding: 0; cursor: pointer;
  -webkit-tap-highlight-color: transparent; line-height: 1; }
.thm-btn svg { display: block; pointer-events: none; }
.thm-dock { position: absolute; z-index: 40; top: calc(8px + env(safe-area-inset-top, 0px)); right: calc(8px + env(safe-area-inset-right, 0px));
  width: 36px; height: 36px; border-radius: 999px; border: 1px solid; box-sizing: border-box;
  -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); box-shadow: 0 2px 10px rgba(0,0,0,.18); }
html[data-theme="dark"] .thm-dock { background: rgba(21,23,28,.8); border-color: #2B2E36; color: #F2D06B; }
html[data-theme="light"] .thm-dock { background: rgba(255,255,255,.88); border-color: #D9DEE4; color: #334155; }
.thm-dock:active { transform: scale(.94); }
@media print { .thm-dock { display: none; } }
`;

/** 단추 자체 — 자리 등록 없이(떠 있는 단추가 쓴다) */
export function ThemeButton({ className = "", style }) {
  const { theme, toggle } = useTheme();
  const toLight = theme === "dark";
  const label = toLight ? "라이트 모드로 바꾸기" : "다크 모드로 바꾸기";
  return (
    <>
      <style>{CSS}</style>
      <button type="button" className={("thm-btn " + className).trim()} style={style} onClick={toggle}
        aria-label={label} title={label} data-theme-toggle={theme}>
        {toLight ? <Sun /> : <Moon />}
      </button>
    </>
  );
}

/** 막대 안 단추 — 이 단추가 떠 있는 동안 떠 있는 단추(ThemeDock)는 숨는다 */
export default function ThemeToggle(props) {
  useThemeHost();
  return <ThemeButton {...props} />;
}

/** 지금 문서의 앱(data-app) — PathRouter 가 경로에 따라 바꾼다 */
function useDataApp() {
  const read = () => (typeof document !== "undefined" && document.documentElement.dataset.app) || "ashrain";
  const [app, setApp] = useState(read);
  useEffect(() => {
    const ob = new MutationObserver(() => setApp(read()));
    ob.observe(document.documentElement, { attributes: true, attributeFilter: ["data-app"] });
    setApp(read());
    return () => ob.disconnect();
  }, []);
  return app;
}

/** 막대가 없는 화면의 오른쪽 위 단추 */
export function ThemeDock() {
  const hosts = useThemeHostCount();
  const app = useDataApp();
  if (hosts > 0 || app !== "ashrain") return null;
  return <ThemeButton className="thm-dock" />;
}
