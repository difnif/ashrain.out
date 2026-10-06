// ashrain.out — 빠른 정답지 · 서술형 해설 웹 렌더러 (경로 /answerswebview 전용)
// 해설 데이터: src/data/answerKeySol.js (SOL[id]) — 원본 해설지 이미지를 보고 옮긴 것.
// 수식은 앱 공용 mathir.renderHtml(MathText 의 mathHtml)로 그리고, 그림은 이 파일의 작은 SVG 그리기(figure)로 그린다.
// 공용 엔진(mathir.js·figsvg.js)은 읽기만 하고 고치지 않는다.
//
// 데이터 모양
//   SOL[id] = { b: [블록…], a: "답(mathir 혼합문)", r: [[단계번호, "채점기준", "비율"]…], rh?: ["단계","채점기준","비율"] }
//   블록: "문장"                                   — 한 줄
//         { s: "문장", m: 1, tag: "㉠", i: 1 }      — m = 오른쪽 단계 표시 ❶, tag = 식 꼬리표 ··· ㉠, i = 들여쓰기 칸 수
//         { sys: [["식", "㉠"], ["식", "㉡"]], pre: "즉, ", post: "의 해는", m: 1, i: 0 }   — 연립(중괄호)
//         { fig: { v: [xmin, ymin, xmax, ymax], w: 280, e: [그리기 요소…] } }               — 그림(아래 figure 참고)
//   문장은 mathir 혼합문: 평문 + [[수식]] 마커. 마커 밖 평문의 "x/5" 같은 짧은 분수도 상하로 선다(renderHtml 규칙).
import { useEffect, useMemo } from "react";
import { mathHtml, ensureMathCss } from "../components/MathText";

const CIRC = ["", "❶", "❷", "❸", "❹", "❺", "❻"];

const CSS = `
.aks { font-size: 15.5px; line-height: 1.75; color: #1D1F24; word-break: keep-all; overflow-wrap: anywhere; }
.aks .akm { font-family: 'Times New Roman', 'Noto Serif', 'Nimbus Roman', 'DejaVu Serif', serif; font-size: 1.07em; }
.aks .akm i { font-style: italic; }
.aks .nw { white-space: nowrap; }
.aks .mf > .mn { align-self: stretch; text-align: center; }
.aks .ov { text-decoration: overline; text-decoration-thickness: 1px; text-underline-offset: 0; padding-top: .08em; }
.aks-sys.one > .aks-rows { grid-template-columns: auto; }
.aks .akm .akm { font-size: 1em; }
.aks .mf { font-family: 'Times New Roman', 'Noto Serif', 'Nimbus Roman', 'DejaVu Serif', serif; }
.aks-num { font-weight: 800; font-size: 20px; color: var(--cur, #2F8A5F); margin: 0 0 4px; letter-spacing: -.02em; }
.aks-row { display: flex; align-items: flex-end; align-items: last baseline; gap: 10px; min-height: 1.75em; }
.aks-row + .aks-row { margin-top: 2px; }
.aks-txt { flex: 1 1 auto; min-width: 0; white-space: pre-wrap; }
.aks-m { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 4px; color: var(--cur, #2F8A5F); font-size: 15px; white-space: nowrap; padding-top: 1px; }
.aks-m b { font-weight: 400; color: #555; letter-spacing: 1px; }
.aks-tag { white-space: nowrap; margin-left: 1.4em; }
.aks-tag b { font-weight: 400; color: #555; letter-spacing: 1px; margin-right: .3em; }
.aks-sys { display: inline-flex; align-items: center; vertical-align: middle; margin: 2px 0; }
.aks-sys > .aks-br { font-size: 2.4em; line-height: .9; font-weight: 200; margin-right: .1em; transform: scaleX(.8); }
.aks-sys > .aks-rows { display: inline-grid; grid-template-columns: auto auto; column-gap: 1.2em; row-gap: .05em; align-items: baseline; }
.aks-sys .aks-rt { white-space: nowrap; }
.aks-sys .aks-rt b { font-weight: 400; color: #555; letter-spacing: 1px; margin-right: .3em; }
.aks-fig { display: flex; justify-content: center; margin: 10px 0 12px; }
.aks-fig svg { max-width: 100%; height: auto; overflow: visible; }
.aks-ans { display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin: 10px 0 14px; }
.aks-ans i { font-style: normal; font-size: 12px; font-weight: 700; color: var(--cur, #2F8A5F); border: 1.5px solid currentColor; border-radius: 4px; padding: 0 4px; line-height: 1.5; }
.aks-ans span { font-size: 16.5px; }
.aks-rub { width: 100%; border-collapse: collapse; font-size: 13.5px; line-height: 1.55; margin-top: 4px; }
.aks-rub th { background: #EFEFEC; font-weight: 600; padding: 6px 6px; border-top: 1.5px solid #333; border-bottom: 1px solid #999; }
.aks-rub td { padding: 7px 8px; border-bottom: 1px solid #C9C9C4; vertical-align: middle; }
.aks-rub td:first-child { text-align: center; color: var(--cur, #2F8A5F); width: 3.2em; font-size: 15px; }
.aks-rub td:last-child { text-align: center; width: 4.2em; white-space: nowrap; }
.aks-rub tr:last-child td { border-bottom: 1.5px solid #333; }
`;

let cssIn = false;
function ensureCss() {
  ensureMathCss();
  if (cssIn || typeof document === "undefined") return;
  const st = document.createElement("style");
  st.id = "aks-css";
  st.textContent = CSS;
  document.head.appendChild(st);
  cssIn = true;
}

// 교과서 조판처럼: 수식은 명조 계열·소문자 변수 기울임·연산자 앞뒤 좁은 간격, 대문자(점 이름)·단위(cm, m…)는 바로 세움.
// mathHtml(= mathir.renderHtml)을 마커·평문 조각별로 그대로 쓰고, 그 결과의 글자 마디에만 꾸밈을 더한다(분수·괄호 규칙은 그대로).
const UNIT_WORDS = new Set(["cm", "mm", "km", "kg", "mL", "m", "g", "L"]);
const ENT = /(&[#a-zA-Z0-9]+;)/;
function styleText(html, inMarker) {
  return html.split(/(<[^>]+>)/).map((part) => {
    if (!part || part.startsWith("<")) return part;
    return part.split(ENT).map((t) => {
      if (!t || ENT.test(t)) return t;
      if (inMarker) return t.replace(/[a-z]/g, "<i>$&</i>").replace(/ /g, "\u2005")
        .replace(/(?:[A-Z0-9′']\u0305)+/g, (m) => `<span class="ov">${m.replace(/\u0305/g, "")}</span>`);
      // 평문: 영문·숫자·수식 기호 덩어리만 명조로, 그 안의 변수(소문자) 기울임 — 단위 낱말은 바로
      t = t.replace(/ ([=×÷+−≤≥≠]) /g, "\u2005$1\u2005");
      return t.replace(/[0-9A-Za-z([{−-][0-9A-Za-z.,+\-−×÷=<>≤≥≠%°′″²³()[\]{}:\u2005 ]*[0-9A-Za-z)\]}%°²³]|[0-9A-Za-z]|[=×÷+−≤≥≠]/g, (run) =>
        `<span class="akm">${run.replace(/[A-Za-z]+/g, (w) => (UNIT_WORDS.has(w) || /^[A-Z]+$/.test(w)) ? w : w.replace(/[a-z]/g, "<i>$&</i>"))}</span>`);
    }).join("");
  }).join("");
}
// 수식 한 덩어리는 줄을 바꾸지 않되, 교과서처럼 관계 기호(=, ≤, ≥, <, >, ≠) 뒤에서만 다음 줄로 넘길 수 있게 한다
function breakAfterRel(html) {
  const visible = html.replace(/<[^>]+>/g, "").replace(/&[#a-zA-Z0-9]+;/g, "x").replace(/\s/g, "");
  const parts = visible.length > 14 ? html.split(/(\u2005(?:=|≤|≥|≠|&lt;|&gt;)\u2005)/) : [html];
  if (parts.length === 1) return `<span class="nw">${html}</span>`;
  let out = "";
  for (let i = 0; i < parts.length; i += 2) out += `<span class="nw">${parts[i]}${parts[i + 1] ? parts[i + 1].trimEnd() : ""}</span>${parts[i + 1] ? "<wbr>\u2005" : ""}`;
  return out;
}
const UNIT_TAIL = "(?:cm²|cm³|m²|cm|mm|km|kg|mL|m|g|L|°C|명|원|점|개|대|시간|분|초|살|권|자루|가지)";
function glue(s) {   // ∴ 와 다음 식, 수와 단위, 식과 '(단위)' 사이에서 줄이 갈리지 않게
  return s.replace(/∴ /g, "∴\u00a0")
    .replace(new RegExp(`(\\d) (${UNIT_TAIL})(?![A-Za-z])`, "g"), "$1\u00a0$2")
    .replace(new RegExp(`\\]\\] \\((${UNIT_TAIL})\\)`, "g"), "]]\u00a0($1)");
}
function richHtml(s) {
  return glue(String(s ?? "")).split(/(\[\[[\s\S]*?\]\])/).map((p, i) =>
    !p ? "" : i % 2 ? `<span class="akm">${breakAfterRel(styleText(mathHtml(p), true))}</span>` : styleText(mathHtml(p), false)).join("");
}
const H = (s) => ({ __html: richHtml(s) });

function Mark({ m }) {
  if (!m) return null;
  return <span className="aks-m"><b>···</b>{CIRC[m] || m}</span>;
}

function Sys({ blk }) {
  return (
    <>
      {blk.pre ? <span dangerouslySetInnerHTML={H(blk.pre)} /> : null}
      <span className={"aks-sys" + (blk.sys.some(([, t]) => t) ? "" : " one")}>
        <span className="aks-br">{"{"}</span>
        <span className="aks-rows">
          {blk.sys.map(([e, t], k) => (
            <span key={k} style={{ display: "contents" }}>
              <span dangerouslySetInnerHTML={H(e)} />
              {blk.sys.some(([, x]) => x) ? <span className="aks-rt">{t ? <><b>···</b>{t}</> : null}</span> : null}
            </span>
          ))}
        </span>
      </span>
      {blk.post ? <span dangerouslySetInnerHTML={H(blk.post)} /> : null}
    </>
  );
}

// ---------------------------------------------------------------- 그림 (작은 SVG 그리기 — 수학 좌표, y 위쪽)
// fig = { v: [xmin, ymin, xmax, ymax], w: 280, e: [요소…] }
// 요소: ["ax", {x:[x0,x1], y:[y0,y1], o:true|"r"|false}]  축(화살표·x·y·O — "r" 이면 O 를 y축 오른쪽에)
//       ["ln", [x1,y1], [x2,y2], {d:1 점선, w:굵기, c:"a" 강조색}]
//       ["pl", [[x,y]…], 옵션]  꺾은선      ["pg", [[x,y]…], {f:"g"|"p"|"b"|"o", s:0 테두리없음}]  다각형
//       ["tx", [x,y], "글자", {a:"s"|"m"|"e", dx, dy, z:크기}]   글자 — "{분자/분모}"는 상하 분수, "−" 그대로
//       ["dt", [x,y]]  점        ["ci", [cx,cy], r, 옵션]  원        ["ar", [cx,cy], r, 시작°, 끝°, 옵션]  호
//       ["ra", 꼭짓점, 점1, 점2, 크기px]  직각 표시        ["av", [x1,y1], [x2,y2], 옵션]  화살표
//       옵션 c: "a"(강조색) 또는 CSS 색, f: "g"|"p"|"b"|"o"|"y" 또는 CSS 색, d: 1 점선 · 2 잔점선, h: 1 글자 흰 테두리(선 위 글자)
const FILL = { g: "rgba(88,180,100,.38)", p: "rgba(236,110,140,.36)", b: "rgba(60,170,200,.36)", o: "rgba(245,166,35,.3)", y: "rgba(240,200,40,.35)" };
const R2 = (n) => Math.round(n * 100) / 100;

function fracLabel(x, y, s, anchor, size, key) {
  // "{n/d}" 토큰을 상하 분수로 — tspan 으로 위·아래를 쌓고 가로줄을 긋는다
  const parts = String(s).split(/(\{[^{}]+\/[^{}]+\})/).filter((p) => p !== "");
  const cw = (t) => [...t].reduce((w, ch) => w + size * (ch === " " ? 0.25 : /[=+−\-<>×]/.test(ch) ? 0.58 : /[a-z]/.test(ch) ? 0.46 : /[0-9]/.test(ch) ? 0.5 : /[A-Z]/.test(ch) ? 0.68 : /[\x20-\x7e]/.test(ch) ? 0.4 : 0.95), 0);
  const items = parts.map((p) => {
    const m = p.match(/^\{([^{}]+)\/([^{}]+)\}$/);
    if (m) { const w = Math.max(cw(m[1]), cw(m[2])) * 0.82 + 3; return { f: true, n: m[1], d: m[2], w }; }
    return { f: false, t: p, w: cw(p) };
  });
  const total = items.reduce((w, it) => w + it.w, 0);
  let cx = anchor === "s" ? x : anchor === "e" ? x - total : x - total / 2;
  const out = [];
  items.forEach((it, i) => {
    if (it.f) {
      const mx = cx + it.w / 2, fs = size * 0.82;
      out.push(<text key={key + "n" + i} x={R2(mx)} y={R2(y - fs * 0.62)} textAnchor="middle" fontSize={fs} fill="currentColor">{it.n}</text>);
      out.push(<line key={key + "l" + i} x1={R2(cx + 1)} x2={R2(cx + it.w - 1)} y1={R2(y - fs * 0.38)} y2={R2(y - fs * 0.38)} stroke="currentColor" strokeWidth="0.9" />);
      out.push(<text key={key + "d" + i} x={R2(mx)} y={R2(y + fs * 0.62)} textAnchor="middle" fontSize={fs} fill="currentColor">{it.d}</text>);
    } else {
      const runs = it.t.split(/([A-Za-z]+)/).filter((r) => r !== "");
      out.push(<text key={key + "t" + i} x={R2(cx)} y={R2(y)} textAnchor="start" fontSize={size} fill="currentColor" style={{ whiteSpace: "pre" }}>
        {runs.map((r, j) => (/^[a-z]+$/.test(r) && !UNIT_WORDS.has(r)) ? <tspan key={j} fontStyle="italic">{r}</tspan> : r)}</text>);
    }
    cx += it.w;
  });
  return out;
}

export function Figure({ fig }) {
  const [xmin, ymin, xmax, ymax] = fig.v;
  const W = fig.w || 280;
  const sc = W / (xmax - xmin);
  const Hh = (ymax - ymin) * sc;
  const X = (x) => R2((x - xmin) * sc);
  const Y = (y) => R2((ymax - y) * sc);
  const col = (c) => (c === "a" ? "var(--cur, #2F8A5F)" : c || "currentColor");
  const stroke = (o = {}) => ({ stroke: col(o.c), strokeWidth: o.w || 1.3, strokeDasharray: o.d ? (o.d === 2 ? "2 2.5" : "4 3") : undefined, fill: "none", strokeLinecap: "round", strokeLinejoin: "round" });
  const els = [];
  fig.e.forEach((el, i) => {
    const [t] = el;
    const k = "e" + i;
    if (t === "ax") {
      const o = el[1] || {};
      const [x0, x1] = o.x, [y0, y1] = o.y;
      const head = (x, y, dir) => {
        const s = 5, pts = dir === "r" ? [[x, y], [x - s, y - 3], [x - s, y + 3]] : [[x, y], [x - 3, y + s], [x + 3, y + s]];
        return <polygon key={k + dir} points={pts.map((p) => p.join(",")).join(" ")} fill="currentColor" />;
      };
      els.push(<line key={k + "x"} x1={X(x0)} y1={Y(0)} x2={X(x1)} y2={Y(0)} stroke="currentColor" strokeWidth="1.1" />);
      els.push(<line key={k + "y"} x1={X(0)} y1={Y(y0)} x2={X(0)} y2={Y(y1)} stroke="currentColor" strokeWidth="1.1" />);
      els.push(head(X(x1), Y(0), "r"), head(X(0), Y(y1), "u"));
      els.push(<text key={k + "xl"} x={X(x1) + 4} y={Y(0) + 13} fontSize="12" fill="currentColor" fontStyle="italic">x</text>);
      els.push(<text key={k + "yl"} x={X(0) - 10} y={Y(y1) + 6} fontSize="12" fill="currentColor" fontStyle="italic" textAnchor="middle">y</text>);
      if (o.o !== false) els.push(<text key={k + "o"} x={o.o === "r" ? X(0) + 3 : X(0) - 3} y={Y(0) + 13} fontSize="11.5" fill="currentColor" textAnchor={o.o === "r" ? "start" : "end"}>O</text>);
    } else if (t === "ln") {
      els.push(<line key={k} x1={X(el[1][0])} y1={Y(el[1][1])} x2={X(el[2][0])} y2={Y(el[2][1])} {...stroke(el[3])} />);
    } else if (t === "pl") {
      els.push(<polyline key={k} points={el[1].map(([x, y]) => `${X(x)},${Y(y)}`).join(" ")} {...stroke(el[2])} />);
    } else if (t === "pg") {
      const o = el[2] || {};
      els.push(<polygon key={k} points={el[1].map(([x, y]) => `${X(x)},${Y(y)}`).join(" ")} {...stroke(o)} fill={FILL[o.f] || o.f || "none"} stroke={o.s === 0 ? "none" : stroke(o).stroke} />);
    } else if (t === "tx") {
      const o = el[3] || {};
      const z = o.z || 12;
      const x = X(el[1][0]) + (o.dx || 0), y = Y(el[1][1]) + (o.dy || 0) + z * 0.35;
      const halo = o.h ? { stroke: "#fff", strokeWidth: 3.2, paintOrder: "stroke", strokeLinejoin: "round" } : {};
      els.push(<g key={k} fill={col(o.c)} color={col(o.c)} fontWeight={o.b ? 700 : undefined} style={halo}>{fracLabel(x, y, el[2], o.a || "m", z, k)}</g>);
    } else if (t === "dt") {
      els.push(<circle key={k} cx={X(el[1][0])} cy={Y(el[1][1])} r={(el[2] && el[2].r) || 2.4} fill={col(el[2] && el[2].c)} />);
    } else if (t === "ci") {
      els.push(<circle key={k} cx={X(el[1][0])} cy={Y(el[1][1])} r={R2(el[2] * sc)} {...stroke(el[3])} fill={el[3] && el[3].f ? (FILL[el[3].f] || el[3].f) : "none"} />);
    } else if (t === "ar") {
      const [cx, cy] = el[1], r = el[2], a0 = el[3] * Math.PI / 180, a1 = el[4] * Math.PI / 180;
      const p0 = [X(cx + r * Math.cos(a0)), Y(cy + r * Math.sin(a0))], p1 = [X(cx + r * Math.cos(a1)), Y(cy + r * Math.sin(a1))];
      const large = Math.abs(el[4] - el[3]) > 180 ? 1 : 0, sweep = el[4] > el[3] ? 0 : 1;
      els.push(<path key={k} d={`M${p0[0]} ${p0[1]} A${R2(r * sc)} ${R2(r * sc)} 0 ${large} ${sweep} ${p1[0]} ${p1[1]}`} {...stroke(el[5])} />);
    } else if (t === "ra") {
      const v = [X(el[1][0]), Y(el[1][1])], a = [X(el[2][0]), Y(el[2][1])], b = [X(el[3][0]), Y(el[3][1])], s = el[4] || 7;
      const u = (p) => { const dx = p[0] - v[0], dy = p[1] - v[1], d = Math.hypot(dx, dy) || 1; return [dx / d, dy / d]; };
      const ua = u(a), ub = u(b);
      els.push(<polyline key={k} points={`${R2(v[0] + ua[0] * s)},${R2(v[1] + ua[1] * s)} ${R2(v[0] + (ua[0] + ub[0]) * s)},${R2(v[1] + (ua[1] + ub[1]) * s)} ${R2(v[0] + ub[0] * s)},${R2(v[1] + ub[1] * s)}`} fill="none" stroke="currentColor" strokeWidth="1" />);
    } else if (t === "av") {
      const x1 = X(el[1][0]), y1 = Y(el[1][1]), x2 = X(el[2][0]), y2 = Y(el[2][1]);
      const d = Math.hypot(x2 - x1, y2 - y1) || 1, ux = (x2 - x1) / d, uy = (y2 - y1) / d, s = 5;
      els.push(<line key={k} x1={x1} y1={y1} x2={x2} y2={y2} {...stroke(el[3])} />);
      els.push(<polygon key={k + "h"} points={`${x2},${y2} ${R2(x2 - ux * s - uy * 2.6)},${R2(y2 - uy * s + ux * 2.6)} ${R2(x2 - ux * s + uy * 2.6)},${R2(y2 - uy * s - ux * 2.6)}`} fill="currentColor" />);
    }
  });
  return (
    <div className="aks-fig">
      <svg viewBox={`-14 -14 ${R2(W + 28)} ${R2(Hh + 28)}`} width={R2(W + 28)} height={R2(Hh + 28)} role="img"
        fontFamily="'Times New Roman', 'Noto Serif', 'Nimbus Roman', serif">{els}</svg>
    </div>
  );
}

function Block({ blk }) {
  if (typeof blk === "string") blk = { s: blk };
  if (blk.fig) return <Figure fig={blk.fig} />;
  const pad = blk.i ? { paddingLeft: `${blk.i * 1.2}em` } : undefined;
  return (
    <div className="aks-row" style={pad}>
      <div className="aks-txt">
        {blk.sys ? <Sys blk={blk} /> : <span dangerouslySetInnerHTML={H(blk.s)} />}
        {blk.tag ? <span className="aks-tag"><b>···</b>{blk.tag}</span> : null}
      </div>
      <Mark m={blk.m} />
    </div>
  );
}

export default function SolView({ num, sol }) {
  useEffect(ensureCss, []);
  const head = sol.rh || ["단계", "채점기준", "비율"];
  const blocks = useMemo(() => sol.b, [sol]);
  return (
    <div className="aks">
      <p className="aks-num">{num}</p>
      {blocks.map((b, i) => <Block key={i} blk={b} />)}
      <div className="aks-ans"><i>답</i><span dangerouslySetInnerHTML={H(sol.a)} /></div>
      <table className="aks-rub">
        <thead><tr>{head.map((h) => <th key={h}>{h}</th>)}</tr></thead>
        <tbody>
          {sol.r.map(([st, txt, pct], i) => (
            <tr key={i}><td>{CIRC[st] || st}</td>{txt && typeof txt === "object" ? <td><Sys blk={txt} /></td> : <td dangerouslySetInnerHTML={H(txt)} />}<td>{pct}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
