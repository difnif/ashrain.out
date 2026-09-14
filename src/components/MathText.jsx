// 공용 수식 텍스트 — mathir.renderHtml 로 분수를 상하로 세워 표시한다.
// 입력은 문항/해설의 평문(+ [[마커]]). renderHtml 이 HTML 이스케이프를 포함하므로 그대로 넣어도 안전하다.
import { useEffect, useMemo } from "react";
import { renderHtml, MATH_CSS } from "../lib/mathir";

let injected = false;
export function ensureMathCss() {
  if (injected || typeof document === "undefined") return;
  const st = document.createElement("style");
  st.id = "ash-math-css";
  st.textContent = MATH_CSS;
  document.head.appendChild(st);
  injected = true;
}

const escapeHtml = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

export function mathHtml(text) {
  try { return renderHtml(String(text ?? "")); } catch { return escapeHtml(text); }
}

/** <MathText text="…" as="p" /> — 줄바꿈은 pre-wrap 으로 살린다 */
export default function MathText({ text, as: Tag = "span", className, style, pre = true }) {
  useEffect(ensureMathCss, []);
  const html = useMemo(() => mathHtml(text), [text]);
  return <Tag className={className} style={pre ? { whiteSpace: "pre-wrap", ...style } : style} dangerouslySetInnerHTML={{ __html: html }} />;
}
