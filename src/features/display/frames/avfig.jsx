// ashrain.out — 학년별 해설 인쇄용 그림: 화면 그림(그림 DSL)을 흑백 SVG 글자로 (frames/avfig.jsx)
// 브라우저에서만 쓴다(앱의 인쇄 창 · scripts/av-files.mjs 가 띄운 Chromium) — 글자 폭을 캔버스로 재야 화면과 같은 자리에 놓인다.
//   figSvg(it, "q")   문제 때 모습(문제지 — 그림을 보고 푸는 문항 qf)
//   figSvg(it, "end") 다 푼 모습(해설지)
import { createRoot } from "react-dom/client";
import { flushSync } from "react-dom";
import { FigDsl, FIG_BOX } from "./figdsl.jsx";
import { l10Plan } from "../lin10.js";

/** 흑백 인쇄 팔레트 — 화면 팔레트와 같은 이름, 회색 단계로(칠은 fo 로 옅게 깔린다) */
export const PRINT_C = {
  name: "print", bg: ["#fff", "#fff", "#fff"],
  ink: "#111", soft: "#6a6a6a", faint: "rgba(0,0,0,0.16)", grid: "rgba(0,0,0,0.10)", halo: "#fff", paper: "#fff",
  gold: "#7a7a7a", coral: "#262626", teal: "#4a4a4a", sky: "#333", lilac: "#585858", leaf: "#555",
  wood: "#9a9a9a", woodEdge: "#333", card: "#fff", cardEdge: "#888",
  red: "#222", blue: "#3a3a3a", yellow: "#999", capBg: "#fff", capInk: "#111", bar: "#7a7a7a", fillA: 0.3,
};

const VB = `${FIG_BOX.x0} ${FIG_BOX.y0} ${FIG_BOX.x1 - FIG_BOX.x0} ${FIG_BOX.y1 - FIG_BOX.y0}`;
export function figSvg(it, when = "end", C = PRINT_C) {
  if (!it?.fig || it.fig.kind !== "dsl" || typeof document === "undefined") return "";
  const P = l10Plan(it);
  const t = when === "q" ? Math.max(0, (P.plan?.[0] ?? 2000) - 1) : P.ans + 5000;
  const div = document.createElement("div");
  const root = createRoot(div);
  flushSync(() => root.render(
    <svg xmlns="http://www.w3.org/2000/svg" viewBox={VB} role="img" aria-label={`${it.no}번 그림`}><FigDsl it={it} t={t} C={C} /></svg>,
  ));
  const s = div.innerHTML;
  root.unmount();
  return s;
}
