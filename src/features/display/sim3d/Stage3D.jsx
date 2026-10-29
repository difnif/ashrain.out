// ashrain.out — 교실 모니터 「3D 축구」: WebGL 캔버스 (sim3d/Stage3D.jsx)
// 재생기(frames/player.jsx)가 3D 를 켤 때만 늦게 들여온다(React.lazy) — three.js 는 이때 처음 내려받는다.
// 캔버스는 화면 전체를 덮고(16:9 무대 바깥 여백까지), 무대 부분이 대본의 시야각과 같게 보이도록 엔진이 맞춘다.
// 그리기는 재생기가 다시 그릴 때마다(같은 시각 t 의 세계를 SVG 글자와 함께) 한 번.
// WebGL 을 못 쓰면 onFail 을 불러 2D 로 돌아가게 한다.
import { useEffect, useLayoutEffect, useRef } from "react";
import { createEngine } from "./engine.js";

export default function Stage3D({ world, theme = "dark", onFail, o = 1 }) {
  const ref = useRef(null);
  const eng = useRef(null);
  const failed = useRef(false);

  // 엔진은 첫 그리기(아래 useLayoutEffect)보다 먼저 만든다 — 같은 컴포넌트의 layout effect 는 적은 차례대로 돈다
  useLayoutEffect(() => {
    try {
      eng.current = createEngine(ref.current, theme);
    } catch (e) {
      failed.current = true;
      onFail?.(e);
    }
    return () => { try { eng.current?.dispose(); } catch { /* 이미 사라짐 */ } eng.current = null; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect(() => { if (eng.current) eng.current.setTheme(theme); }, [theme]);
  useLayoutEffect(() => {
    if (!eng.current || failed.current || !world) return;
    try { eng.current.render(world); }
    catch (e) { failed.current = true; onFail?.(e); }
  });

  return <canvas ref={ref} className="dsp-3d" style={{ opacity: o }} aria-hidden="true" />;
}
