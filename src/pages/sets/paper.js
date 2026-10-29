// ashrain.out — 컨셉 문제 「종이처럼 풀기」: 문제지 그대로 펼친 화면 (shadow DOM · 순수 DOM)
//
// 인쇄용 문제지 HTML(public/concept-sets/<범주>/print/NN-problems.html — PDF 를 찍은 바로 그 문서)을 shadow DOM 에 넣어
// PDF 보듯 쪽을 넘겨 본다. 앱 CSS 와 섞이지 않게 문서 CSS 는 printdoc.scopeCss 로 body 자리(.csx-p)에 감싸 넣는다.
// 글꼴(@font-face)은 shadow 안에서 안 먹으므로 문서의 글꼴 링크는 바깥 document.head 에 단다(ensureLinks).
//
// 손대는 곳
//   · 문항 칸(.q) 누르기 → onCell(no) — 답 시트(손글씨 · 타자)를 연다. 괄호만이 아니라 칸 전체가 누르는 자리(휴대폰에서 작다).
//   · 보기 고르기 문항의 <보기> 줄(ㄱ. ㄴ. …) 누르기 → onPick(no, "ㄱ") — 빨간 색연필 체크, 다시 누르면 해제, 여럿 가능.
//   · render(state) 가 괄호 안 답(타자 글씨 · 손글씨 SVG), 체크, 채점 표시(빨간 동그라미 · 빗금 · 정답)를 다시 그린다.
import { scopeCss } from "./printdoc.js";
import { inkSvg, hasInk } from "./ink.js";

export const PAGE_W_PX = 210 * 96 / 25.4;   // 쪽 너비 210 mm(본문 184 + 여백 26) — 화면 CSS 의 .pg 상자
const RED = "#d42a3c";
const PENCIL = "#2c3a52";

export const PAPER_CSS = `
:host { display: block; }
.csx-p { min-width: max-content; }
.q { cursor: pointer; -webkit-tap-highlight-color: transparent; transition: background-color .2s; }
.q:active { background-color: rgba(13, 148, 136, .07); }
.q.cs-on { background-color: rgba(255, 214, 102, .2); box-shadow: inset 0 0 0 .55mm rgba(234, 160, 0, .6); }
.pg { position: relative; }
.q .qh .no { position: relative; }
.q .ans { position: relative; }
.q .ans i { position: relative; height: 5.2mm; vertical-align: bottom; border-radius: .9mm; }
.q.cs-empty .ans i { background: rgba(255, 214, 102, .32); box-shadow: inset 0 -.25mm 0 rgba(176, 122, 46, .45); }
.cs-typed { position: absolute; left: 0; right: 0; bottom: -.2mm; text-align: center; white-space: nowrap; line-height: 1;
  font-family: 'Gaegu', 'Nanum Pen Script', cursive; font-weight: 700; font-size: 14pt; color: ${PENCIL}; letter-spacing: .02em; }
.cs-typed .fr { font-size: .78em; vertical-align: -.35em; }
.cs-typed .fr .n { border-bottom-width: .3mm; }
.cs-ink { position: absolute; left: 50%; bottom: -.4mm; transform: translateX(-50%); overflow: visible; }
.q .box p.cs-pk { position: relative; cursor: pointer; border-radius: .8mm; }
.q .box p.cs-pk:active { background: rgba(212, 42, 60, .06); }
.cs-check { position: absolute; left: -2.4mm; top: -2.6mm; width: 7.2mm; height: 7.2mm; overflow: visible; pointer-events: none; }
.cs-mark { position: absolute; overflow: visible; pointer-events: none; }
.cs-key { position: absolute; right: 3.2mm; bottom: 6.4mm; white-space: nowrap; line-height: 1; transform: rotate(-3deg);
  font-family: 'Gaegu', cursive; font-weight: 700; font-size: 12.5pt; color: ${RED}; pointer-events: none; }
.cs-key .fr { font-size: .8em; vertical-align: -.35em; }
.cs-key .fr .n { border-bottom-color: ${RED}; }
.cs-read { position: absolute; left: 3mm; bottom: 1.4mm; font: 600 7.2pt 'Noto Sans KR', sans-serif; color: #7a7a7a; pointer-events: none; }
.cs-read b { color: #333; }
.cs-unread { color: #c26a00; }
.cs-score { position: absolute; right: 7mm; top: 1.2mm; line-height: 1; transform: rotate(-7deg); pointer-events: none;
  font-family: 'Gaegu', cursive; font-weight: 700; font-size: 31pt; color: ${RED}; }
.cs-score small { font-size: .55em; margin-left: .6mm; }
@media (hover: hover) { .q:hover { background-color: rgba(13, 148, 136, .045); } }
`;

const PENCIL_DEFS = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="cs-pencil" x="-30%" y="-30%" width="160%" height="160%">
<feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="7" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="1.3" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.5" result="g"/>
<feComposite in="d" in2="g" operator="in"/></filter></defs></svg>`;

// 손으로 그은 듯한 표시들 (24×24 · 40×40 상자)
const CHECK_D = "M3.4 12.4c1.7 1.3 3.6 3.8 5.1 6.9 2.8-6.6 7.1-12.6 12.6-16.2";
const CIRCLE_D = "M31.5 8.6C26 3.2 12.6 3.4 7 12.3 2.6 19.6 7.4 33.4 20.4 35.3c10.6 1.4 17.2-6.8 15.9-16-.8-5.8-5.6-10.8-12-12.2";
const SLASH_D = "M8.5 33.5C15 25.5 22.5 15.5 32.5 5.5";

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
/** 손 글씨처럼 보일 답 글자 — 분수는 위아래 */
export function answerTextHtml(raw) {
  const s = String(raw ?? "").trim();
  const m = s.match(/^(\d+)\s*\/\s*(\d+)$/);
  if (m) return `<span class="fr"><span class="n">${m[1]}</span><span class="d">${m[2]}</span></span>`;
  return esc(s);
}
const seedRot = (a, b = 0) => (((a * 37 + b * 17) % 13) - 6) * 1.1;   // 표시마다 살짝 다른 기울기(늘 같은 값)

function svgMark(cls, d, view, style, sw = 2.6) {
  return `<svg class="${cls}" viewBox="0 0 ${view} ${view}" style="${style}" aria-hidden="true"><path d="${d}" fill="none" stroke="${RED}" `
    + `stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" opacity=".92" filter="url(#cs-pencil)"/></svg>`;
}

/** 문서 글꼴 링크를 바깥 문서에 (한 번씩) */
export function ensureLinks(links, doc = document) {
  for (const href of links || []) {
    if ([...doc.querySelectorAll("link[rel=stylesheet]")].some((l) => l.getAttribute("href") === href)) continue;
    const l = doc.createElement("link");
    l.rel = "stylesheet"; l.href = href;
    doc.head.appendChild(l);
  }
}

export class Paper {
  /**
   * host: shadow 를 붙일 요소. doc: printdoc.splitDoc 결과. set: 세트 JSON.
   * on: { cell(no), pick(no, label) }
   */
  constructor(host, doc, set, on = {}) {
    this.host = host;
    this.set = set;
    this.on = on;
    this.root = host.shadowRoot || host.attachShadow({ mode: "open" });
    const css = doc.css.map((c) => scopeCss(c, ".csx-p")).join("\n");
    this.root.innerHTML = `<style>${css}</style><style>${PAPER_CSS}</style>${PENCIL_DEFS}<div class="csx-p">${doc.body}</div>`;
    this.wrap = this.root.querySelector(".csx-p");
    this.byNo = new Map();
    for (const it of set.items) {
      const q = this.root.getElementById ? this.root.getElementById(it.id) : this.root.querySelector(`#${CSS.escape(it.id)}`);
      if (!q) continue;
      const cell = { it, q, no: q.querySelector(".qh .no"), ans: q.querySelector(".ans"), slot: q.querySelector(".ans i"), picks: [] };
      if (it.a?.k === "pick") {
        for (const p of q.querySelectorAll(".box p")) {
          const lab = (p.textContent || "").trim().charAt(0);
          if (/[ㄱ-ㅎ]/.test(lab)) { p.classList.add("cs-pk"); p.dataset.pk = lab; cell.picks.push({ p, lab }); }
        }
      }
      q.dataset.no = it.no;
      this.byNo.set(it.no, cell);
    }
    this.firstPage = this.root.querySelector(".pg");
    this.onClick = (e) => {
      const q = e.target.closest?.(".q[data-no]");
      if (!q) return;
      const no = Number(q.dataset.no);
      const pk = e.target.closest?.("p.cs-pk");
      if (pk && this.on.pick) { this.on.pick(no, pk.dataset.pk); return; }
      if (this.on.cell) this.on.cell(no);
    };
    this.root.addEventListener("click", this.onClick);
  }

  destroy() { this.root.removeEventListener("click", this.onClick); }

  setZoom(z) { this.wrap.style.zoom = String(z); }

  cell(no) { return this.byNo.get(no) || null; }

  /** 그 문항으로 화면을 옮긴다 */
  reveal(no, block = "center") {
    const c = this.byNo.get(no);
    c?.q?.scrollIntoView?.({ behavior: "smooth", block });
  }

  /**
   * state: { answers, graded?: { rows }, reads?, active? }
   *   graded 가 있으면 채점 표시(빨간 동그라미 · 빗금 · 정답 · 판독 글자)와 점수를 그린다.
   */
  render(state) {
    const { answers = {}, graded = null, reads = {}, active = null } = state || {};
    const rows = graded ? Object.fromEntries(graded.rows.map((r) => [r.no, r])) : null;
    for (const [no, c] of this.byNo) {
      const ans = answers[no];
      // 괄호 안
      let html = "";
      const filled = !!ans && ((ans.k === "text" && String(ans.raw || "").trim()) || (ans.k === "pick" && ans.sel?.length) || (ans.k === "ink" && hasInk(ans)));
      if (filled) {
        if (ans.k === "text") html = `<span class="cs-typed">${answerTextHtml(ans.raw)}</span>`;
        else if (ans.k === "pick") html = `<span class="cs-typed">${esc(ans.sel.join(", "))}</span>`;
        else {
          const svg = inkSvg(ans, { color: PENCIL, width: 1.05 });
          const m = svg.match(/data-w="([\d.]+)" data-h="([\d.]+)"/);
          const w = m ? +m[1] : 100, h = m ? +m[2] : 40;
          const maxH = ans.lay === "frac" ? 12.5 : 7.4, maxW = 27;             // mm
          const k = Math.min(maxH / h, maxW / w);
          html = svg.replace('class="cs-ink"', `class="cs-ink" style="width:${(w * k).toFixed(2)}mm;height:${(h * k).toFixed(2)}mm"`);
        }
      }
      if (c.slot && c.slot.dataset.html !== html) { c.slot.innerHTML = html; c.slot.dataset.html = html; }
      c.q.classList.toggle("cs-empty", !filled && !rows);
      c.q.classList.toggle("cs-on", active === no);
      // 보기 체크(빨간 색연필)
      const sel = ans?.k === "pick" ? ans.sel : [];
      for (const { p, lab } of c.picks) {
        const on = sel.includes(lab);
        const has = !!p.querySelector(":scope > .cs-check");
        if (on && !has) p.insertAdjacentHTML("afterbegin", svgMark("cs-check", CHECK_D, 24, `transform:rotate(${seedRot(no, lab.charCodeAt(0))}deg)`));
        if (!on && has) p.querySelector(":scope > .cs-check").remove();
      }
      // 채점 표시
      const r = rows?.[no];
      const key = r ? `${r.status}|${r.raw}|${reads[no] ?? ""}` : "";
      if (c.q.dataset.grade !== key) {
        c.q.querySelectorAll(".cs-mark,.cs-key,.cs-read").forEach((el) => el.remove());
        if (r) {
          const rot = seedRot(no, 3);
          if (r.status === "ok") c.no?.insertAdjacentHTML("beforeend", svgMark("cs-mark", CIRCLE_D, 40, `left:-3.6mm;top:-3.4mm;width:10.6mm;height:10.6mm;transform:rotate(${rot}deg)`, 2.4));
          else if (r.status === "wrong" || r.status === "blank") {
            c.no?.insertAdjacentHTML("beforeend", svgMark("cs-mark", SLASH_D, 40, `left:-2.4mm;top:-3mm;width:9.6mm;height:9.6mm;transform:rotate(${rot}deg)`, 2.6));
            c.q.insertAdjacentHTML("beforeend", `<span class="cs-key">${r.status === "blank" ? "답 " : "→ "}${answerTextHtml(rawAnswer(c.it))}</span>`);
          } else if (r.status === "unread") {
            c.q.insertAdjacentHTML("beforeend", `<span class="cs-read cs-unread">손글씨를 읽지 못했어요 — 눌러서 확인</span>`);
          }
          if (ans?.k === "ink" && reads[no]) c.q.insertAdjacentHTML("beforeend", `<span class="cs-read">읽은 답 <b>${esc(reads[no])}</b></span>`);
        }
        c.q.dataset.grade = key;
      }
    }
    // 점수(첫 쪽 오른쪽 위)
    const sk = graded ? `${graded.score}/${graded.n}` : "";
    if (this.firstPage && this.firstPage.dataset.score !== sk) {
      this.firstPage.querySelector(":scope > .cs-score")?.remove();
      if (graded) this.firstPage.insertAdjacentHTML("afterbegin", `<div class="cs-score">${graded.score}<small>/${graded.n}</small></div>`);
      this.firstPage.dataset.score = sk;
    }
  }
}

/** 문항의 정답 쓰는 꼴(분수 · 정수 · 보기) — conceptsets.rawOf 와 같다(이 파일만 따로 쓸 수 있게) */
function rawAnswer(it) {
  const a = it?.a || {};
  if (a.k === "frac") return a.d === 1 ? String(a.n) : `${a.n}/${a.d}`;
  if (a.k === "pick") return (a.v || []).join(", ");
  if (a.k === "pair") return `${a.v[0]}, ${a.v[1]}`;
  return String(a.v);
}
