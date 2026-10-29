// ashrain.out — 컨셉 문제: 바로 인쇄 (문제지 · 해설지 · OMR 카드를 골라 한 번에)
//
// 문제지 · 해설지는 PDF 와 같은 HTML(public/concept-sets/<범주>/print/NN-*.html)을 가져와 쓴다 — 쪽 나눔이 PDF 와 같다.
//   · 하나만 고르면 그 HTML 을 그대로 연다(여백 · 쪽 번호까지 PDF 와 똑같이).
//   · 여럿을 고르면 한 문서로 합친다. 두 문서의 CSS 가 서로 덮지 않게 문서마다 선택자를 감싸고(.csx-p / .csx-s — body 자리),
//     쪽 여백은 문제지 기준 12·13·13·13 mm 하나로 둔다. 해설지는 원래 가로 182 mm 라 좌우 1 mm 를 안에서 비운다.
//     쪽 번호는 합친 문서 안에서 이어진다.
// OMR 카드는 grid.js 가 그린 SVG(184 × 272 mm) — 쪽 여백 12·13·13·13 mm 에 꼭 맞는다.
// 창은 클릭하는 순간 먼저 열고(팝업 차단 회피) 내용은 불러온 뒤 채운다. 글꼴이 다 오면 인쇄 창을 띄운다.

export const PAGE_CSS = "@page{size:A4;margin:12mm 13mm 13mm 13mm;@bottom-center{content:counter(page);font-size:8px;color:#555;letter-spacing:2px}}";
export const OMR_PAGE_CSS = "@page{size:A4;margin:12mm 13mm 13mm 13mm}";
export const OMR_FONTS = [
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/400.css",
  "https://cdn.jsdelivr.net/npm/@fontsource/noto-sans-kr@5.3.1/700.css",
];

const escHtml = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// ── CSS 감싸기 ────────────────────────────────────────────────────────────────
/** 블록 끝 찾기 (중괄호 짝) — 문자열 안의 중괄호는 생성기 CSS 에 없다(content:counter(page) 정도) */
function blockEnd(css, open) {
  let depth = 0;
  for (let i = open; i < css.length; i++) {
    const ch = css[i];
    if (ch === "\"" || ch === "'") { const j = css.indexOf(ch, i + 1); if (j < 0) return css.length - 1; i = j; continue; }
    if (ch === "{") depth++;
    else if (ch === "}") { depth--; if (depth === 0) return i; }
  }
  return css.length - 1;
}

function scopeSelector(sel, scope) {
  const t = sel.trim();
  if (!t) return "";
  if (t === scope || t.startsWith(scope + " ") || t.startsWith(scope + ".") || t.startsWith(scope + ":") || t.startsWith(scope + ">")) return t;
  if (/^(html|body|:root)$/i.test(t)) return scope;
  const m = t.match(/^(html|body|:root)\s*(>|\s)\s*(.+)$/i);
  if (m) return `${scope} ${m[3]}`;
  if (/^(html|body)[.:#[]/i.test(t)) return scope + t.replace(/^(html|body)/i, "");
  return `${scope} ${t}`;
}

/**
 * 스타일시트의 모든 선택자 앞에 scope 를 붙인다. html · body · :root 는 scope 자신으로.
 * @page 는 버리고(합친 문서가 하나를 둔다) @media · @supports 는 안쪽까지, @font-face · @keyframes 는 그대로.
 */
export function scopeCss(css, scope) {
  const src = String(css || "").replace(/\/\*[\s\S]*?\*\//g, "");
  let out = "", i = 0;
  while (i < src.length) {
    const open = src.indexOf("{", i);
    if (open < 0) break;
    const head = src.slice(i, open).trim();
    const end = blockEnd(src, open);
    const body = src.slice(open + 1, end);
    if (head.startsWith("@")) {
      const at = head.slice(1).split(/[\s({]/)[0].toLowerCase();
      if (at === "page") { /* 버림 */ }
      else if (at === "media" || at === "supports" || at === "container" || at === "layer") out += `${head}{${scopeCss(body, scope)}}`;
      else out += `${head}{${body}}`;
    } else if (head) {
      const sels = head.split(",").map((s) => scopeSelector(s, scope)).filter(Boolean);
      if (sels.length) out += `${[...new Set(sels)].join(",")}{${body.trim()}}`;
    }
    i = end + 1;
  }
  // 블록 밖에 남은 @import 같은 줄은 버린다(생성기 CSS 에 없다)
  return out;
}

// ── 문서 나누기 ───────────────────────────────────────────────────────────────
/** 인쇄용 HTML → { links:[href], css:[문자열], body } (style · script 는 body 에서 뺀다) */
export function splitDoc(html) {
  const s = String(html || "");
  const links = [...s.matchAll(/<link\b[^>]*rel=["']?stylesheet["']?[^>]*>/gi)]
    .map((m) => (m[0].match(/href=["']([^"']+)["']/i) || [])[1]).filter(Boolean);
  const css = [...s.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]);
  const bi = s.search(/<body\b/i);
  let body = bi >= 0 ? s.slice(s.indexOf(">", bi) + 1) : s;
  body = body.replace(/<\/body>[\s\S]*$/i, "").replace(/<\/html>\s*$/i, "")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, "").replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "");
  return { links, css, body };
}

/** 인쇄 창에서 글꼴이 다 온 뒤 인쇄 — 자동 인쇄가 막혀도 화면 위 버튼으로 다시 */
export const PRINT_SCRIPT = `<script>(function(){var done=false;function go(){if(done)return;done=true;setTimeout(function(){try{window.focus()}catch(e){}window.print()},300)}
function ready(){var f=document.fonts;if(!f||!f.ready){go();return}requestAnimationFrame(function(){requestAnimationFrame(function(){f.ready.then(go,go)})});setTimeout(go,6000)}
if(document.readyState==="complete")ready();else window.addEventListener("load",ready);
var b=document.getElementById("cs-print-btn");if(b)b.addEventListener("click",function(){window.print()});})();</scr` + `ipt>`;
const PRINT_BTN = `<button id="cs-print-btn" type="button">🖨 인쇄하기</button>`;
const PRINT_BTN_CSS = "#cs-print-btn{position:fixed;right:14px;bottom:14px;z-index:9;font:700 15px/1 system-ui,sans-serif;padding:12px 18px;border-radius:999px;border:0;background:#0D9488;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.25);cursor:pointer}@media print{#cs-print-btn{display:none}}";

/**
 * 인쇄할 문서 하나로 합치기.
 * parts: [{ kind:"doc", cls:"cs-p"|"cs-s", html }] · [{ kind:"omr", html: cardHtml(card) }]
 * 문서가 하나뿐이면 그 문서를 그대로 쓴다(원래 @page · 쪽 번호).
 */
export function composePrint(parts, title = "인쇄") {
  const list = (parts || []).filter((p) => p && p.html);
  if (!list.length) return "";
  const head = (extra) => `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escHtml(title)}</title>${extra}`;
  if (list.length === 1 && list[0].kind === "doc") {
    const h = String(list[0].html);
    const inj = `<style>${PRINT_BTN_CSS}</style>`;
    let doc = /<\/head>/i.test(h) ? h.replace(/<\/head>/i, `${inj}</head>`) : inj + h;
    doc = doc.replace(/<title>[\s\S]*?<\/title>/i, `<title>${escHtml(title)}</title>`);
    return /<\/body>/i.test(doc) ? doc.replace(/<\/body>/i, `${PRINT_BTN}${PRINT_SCRIPT}</body>`) : doc + PRINT_BTN + PRINT_SCRIPT;
  }
  const links = new Set();
  const styles = [];
  const bodies = [];
  let onlyOmr = true;
  list.forEach((p, i) => {
    const brk = i > 0 ? " cs-brk" : "";
    if (p.kind === "omr") {
      OMR_FONTS.forEach((u) => links.add(u));
      bodies.push(`<div class="cs-omr${brk}">${p.html}</div>`);
      return;
    }
    onlyOmr = false;
    // body 자리를 대신할 바깥 상자(.csx-p/.csx-s) — 원래 문서의 body > div.cs-p 짜임을 그대로 두어야
    // em 단위 자간처럼 body 글자 크기로 계산돼 물려받는 값이 같다(해설지 줄바꿈이 PDF 와 같아진다)
    const outer = p.cls === "cs-s" ? "csx-s" : "csx-p";
    const d = splitDoc(p.html);
    d.links.forEach((u) => links.add(u));
    styles.push(d.css.map((c) => scopeCss(c, "." + outer)).join("\n"));
    bodies.push(`<div class="cs-doc ${outer}${brk}">${d.body}</div>`);
  });
  const base = `${onlyOmr ? OMR_PAGE_CSS : PAGE_CSS}html,body{margin:0;padding:0;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}`
    + ".cs-brk{break-before:page;page-break-before:always}"
    + "@media print{div.cs-doc.csx-s{padding:0 1mm}}"   // 해설지는 가로 182 mm — 감싼 CSS 의 html,body{padding:0}(.csx-s) 보다 세게
    + "@media screen{html{background:#e9e9e9}body{padding:6mm 0 18mm}.cs-omr .omr-pg{margin:0 auto 6mm;box-shadow:0 1px 6px rgba(0,0,0,.18);box-sizing:content-box;padding:12mm 13mm 13mm}}"
    + PRINT_BTN_CSS;
  return head([...links].map((u) => `<link rel="stylesheet" href="${escHtml(u)}">`).join("")
    + `<style>${base}</style>` + styles.map((c) => `<style>${c}</style>`).join(""))
    + `</head><body>${bodies.join("")}${PRINT_BTN}${PRINT_SCRIPT}</body></html>`;
}

// ── 창 ────────────────────────────────────────────────────────────────────────
/** 클릭 직후(동기)에 부른다 — 팝업 차단을 피하려고 빈 창을 먼저 연다 */
export function openPrintWindow() {
  try {
    const win = window.open("", "_blank");
    if (!win) return null;
    win.document.open();
    win.document.write(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>인쇄 준비</title></head><body style="font-family:system-ui,sans-serif;color:#555;padding:28px;line-height:1.7">인쇄할 내용을 준비하는 중이에요…</body></html>`);
    win.document.close();
    return win;
  } catch { return null; }
}
export function fillPrintWindow(win, html) {
  win.document.open();
  win.document.write(html);
  win.document.close();
}
export function failPrintWindow(win, msg) {
  try {
    win.document.open();
    win.document.write(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>인쇄</title></head><body style="font-family:system-ui,sans-serif;color:#b42318;padding:28px;line-height:1.7">${escHtml(msg)}<br><br><span style="color:#555">이 창을 닫고 다시 시도해 주세요.</span></body></html>`);
    win.document.close();
  } catch { /* 창이 닫혔다 */ }
}
