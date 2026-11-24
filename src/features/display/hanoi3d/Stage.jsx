// ashrain.out — 교실 모니터 「하노이의 탑」 3D 무대: 캔버스 (hanoi3d/Stage.jsx)
// 액자(frames/hanoiframe.jsx)가 3D 로 볼 때만 늦게 들여온다(React.lazy) — three.js 는 이때 처음 내려받는다.
// 엔진은 스스로 돌며(최대 60fps) 시계를 clock() 으로 읽는다. React 는 설정(원판 · 기둥 · 세트 · 빠르기 · 밝기)이 바뀔 때만 알린다.
// WebGL 을 못 쓰거나 그리다 오류가 나면 onFail 을 불러 2D 로 돌아가게 한다. 첫 그림을 그리면 onReady.
// onEngine(엔진 | null) — 액자가 엔진을 바로 부른다(로봇 모드 카메라 샷 · 두 손가락 따라가기 · 화면 점에서 로봇 찾기). 자주 바뀌는 것이라 React 를 거치지 않는다.
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createHanoiEngine } from "./engine.js";

export default function HanoiStage3D({ cfg, theme = "dark", clock, paused, onFail, onReady, onEngine }) {
  const ref = useRef(null);
  const eng = useRef(null);
  const clk = useRef(clock);
  clk.current = clock;
  const failCb = useRef(onFail);
  failCb.current = onFail;
  const readyCb = useRef(onReady);
  readyCb.current = onReady;
  const engCb = useRef(onEngine);
  engCb.current = onEngine;
  const [shown, setShown] = useState(false);

  useLayoutEffect(() => {
    try {
      eng.current = createHanoiEngine(ref.current, {
        theme, getElapsed: () => clk.current(), onError: (e) => failCb.current?.(e),
        onFirstFrame: () => { setShown(true); readyCb.current?.(); },
      });
      eng.current.setConfig(cfg);
      engCb.current?.(eng.current);
      if (typeof window !== "undefined") window.__hanoi3d = eng.current;   // 화면 점검용(품질 · 그리기 수 · 샷)
    } catch (e) {
      failCb.current?.(e);
    }
    return () => {
      engCb.current?.(null);
      try { eng.current?.dispose(); } catch { /* 이미 사라짐 */ }
      if (typeof window !== "undefined" && window.__hanoi3d === eng.current) window.__hanoi3d = null;
      eng.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect(() => { eng.current?.setConfig(cfg); }, [cfg]);
  useEffect(() => { eng.current?.setTheme(theme); }, [theme]);
  useEffect(() => { eng.current?.setPaused(paused); }, [paused]);

  // 첫 그림이 나올 때까지 투명 — 밑의 평면 그림이 보이다가 부드럽게 바뀐다
  return <canvas ref={ref} className="dsp-3d" aria-hidden="true" style={{ opacity: shown ? 1 : 0, transition: "opacity .7s ease" }} />;
}
