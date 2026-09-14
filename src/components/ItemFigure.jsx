// 문항 도형 — test_items.figure ([{fn,args}]) 를 figsvg 로 그려 종이색 판 위에 올린다.
// figanim 이 강조할 수 있도록 요소의 data-k 키를 그대로 보존한다(dangerouslySetInnerHTML).
import { useMemo } from "react";
import { figureToHtml1 } from "../lib/figsvg";
import "./item.css";

export function figureHtml(figure, width = 320) {
  if (!Array.isArray(figure) || !figure.length) return "";
  let html = "";
  for (const fg of figure) {
    try { html += figureToHtml1(fg, { width }).html || ""; } catch { /* 그릴 수 없는 도형은 침묵 */ }
  }
  return html;
}

export default function ItemFigure({ figure, width = 320, className = "", style }) {
  const html = useMemo(() => figureHtml(figure, width), [figure, width]);
  if (!html) return null;
  return <div className={"fig-stage " + className} style={style} dangerouslySetInnerHTML={{ __html: html }} />;
}
