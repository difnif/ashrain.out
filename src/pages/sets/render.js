// ashrain.out — 컨셉 문제: 문항 · 3단 해설(움직이는 판서 + 도식) HTML — 순수 함수 (node 테스트 가능)
//
// 데이터는 생성기(guard-daily tk_export.py)가 만든 정적 JSON 이다(사용자 입력이 아니다). 그래도 <script> · on* 속성 ·
// javascript: 주소는 걸러서 넣는다.
//
// 해설 마크업은 figanim 계약을 따른다:
//   .lv.anim-level[data-anim='[[큐…]…]'] > .fig-stage > (.fig-steps > .fig-line[data-k=line:i] > .fig-hint[data-k=hint:i]) + 도식
//   도식(SVG · 표)의 강조 단위는 data-k / data-ka(별칭) — 생성기가 붙여 둔 키를 큐가 짚는다.
//   1× = 단계당 2.4초 · 그림을 누르면 멈춤 · 1.5× · 진행바 — 화면에 45% 이상 들어오면 저절로 재생(figanim.mountAll).

export const ACCENT = "#d1495b";
export const LV_COLOR = { 하: "#6f8f75", 중: "#b07a2e", 상: "#a3463e" };   // 문제지 · 해설지와 같은 색
export const STAGE_TITLES = ["방침", "전개", "확인"];

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
export { esc };

/** 생성기 HTML 조각을 넣기 전에 위험한 것만 걷어 낸다 */
export function safeHtml(s) {
  return String(s ?? "")
    .replace(/<\s*(script|iframe|object|embed|style)\b[\s\S]*?<\s*\/\s*\1\s*>/gi, "")
    .replace(/<\s*(script|iframe|object|embed|style|link|meta|base)\b[^>]*>/gi, "")
    .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, "")
    .replace(/(href|src|xlink:href)\s*=\s*("|')\s*javascript:[^"']*\2/gi, "$1=$2#$2");
}

let svgSeq = 0;
/**
 * 생성기 SVG(가로·세로 mm) → 화면용: 가로를 k 배 px 로(최대 100%), 세로는 viewBox 비율.
 * 한 화면에 SVG 가 여럿이라 marker id(ah 등)가 겹치지 않게 접미사를 붙인다.
 */
export function scaleSvg(svg, k = 1.3) {
  const sfx = `-c${(++svgSeq).toString(36)}`;
  let s = String(svg || "");
  const ids = [...new Set([...s.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))];
  for (const id of ids) {
    const re = id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    s = s.replace(new RegExp(`(\\sid=")${re}(")`, "g"), `$1${id}${sfx}$2`)
      .replace(new RegExp(`url\\(#${re}\\)`, "g"), `url(#${id}${sfx})`)
      .replace(new RegExp(`(href=")#${re}(")`, "g"), `$1#${id}${sfx}$2`);
  }
  return s.replace(/<svg\b([^>]*)>/, (m, attrs) => {
    const w = attrs.match(/\swidth="([\d.]+)mm"/);
    if (!w) return m;
    const px = (+w[1]) * 3.7795 * k;
    const a = attrs.replace(/\swidth="[^"]*"/, "").replace(/\sheight="[^"]*"/, "");
    return `<svg${a} style="width:${px.toFixed(1)}px;max-width:100%;height:auto">`;
  });
}

/** 문항 머리: 번호 · 난이도 · 장면 · 유형 */
export function headHtml(it, { showType = true } = {}) {
  const lv = it.lv || "";
  return `<span class="cs-no">${esc(it.no)}</span>`
    + `<span class="cs-lv" style="background:${LV_COLOR[lv] || "#777"}">${esc(lv)}</span>`
    + (it.sp ? `<span class="cs-sp">${esc(it.sp)}</span>` : "")
    + (showType && it.ty ? `<span class="cs-ty">${safeHtml(it.ty)}</span>` : "");
}

/** 문항 본문: 발문 → 보기 → 표 → 그림 (문제지와 같은 차례) */
export function questionHtml(it) {
  let h = `<div class="cs-qt">${safeHtml(it.q)}</div>`;
  if (Array.isArray(it.box) && it.box.length) {
    h += `<div class="cs-box"><span class="cs-box-h">보기</span>${it.box.map((b) => `<p>${safeHtml(b)}</p>`).join("")}</div>`;
  }
  if (Array.isArray(it.rows) && it.rows.length) {
    h += `<table class="cs-rows"><tbody>${it.rows.map((r) => `<tr>${(Array.isArray(r) ? r : [r]).map((c, i) => (i === 0 ? `<th>${safeHtml(c)}</th>` : `<td>${safeHtml(c)}</td>`)).join("")}</tr>`).join("")}</tbody></table>`;
  }
  if (it.fig) h += `<div class="fig-stage cs-qfig">${scaleSvg(safeHtml(it.fig), 1.35)}</div>`;
  return h;
}

/** 정답 HTML (분수는 위아래) */
export function answerHtml(it) {
  return safeHtml(it?.a?.t || "") || esc(it?.a?.v ?? "");
}

/** 판서: 줄마다 작은 빨간 메모(라벨) + 식 */
export function boardHtml(board) {
  const lines = (Array.isArray(board) ? board : []).map((b, i) => {
    const hint = b && b.h ? `<span class="fig-hint" data-k="hint:${i}">${safeHtml(b.h)}</span>` : "";
    return `<div class="fig-line" data-k="line:${i}">${hint}<span class="cs-bt">${safeHtml(b?.t ?? b)}</span></div>`;
  }).join("");
  return `<div class="fig-steps cs-board">${lines}</div>`;
}

/** 도식(SVG 또는 표) — 표는 행마다 data-k="row:i" · 머리 head · 결과 res */
export function diagramHtml(dg) {
  if (!dg) return "";
  const s = safeHtml(dg);
  return `<div class="cs-dg">${/^\s*<svg\b/i.test(s) ? scaleSvg(s, 1.4) : s}</div>`;
}

/**
 * 3단 해설 — 방침(포지티브 · 네거티브 → 전략) · 전개(판서 + 도식, 움직임) · 확인 → 모범 답안 · 채점 기준.
 * opts.anim=false 면 움직임 없이(인쇄 · 미리보기) 그린다.
 */
export function solutionHtml(it, opts = {}) {
  const s = it?.s || {};
  const anim = opts.anim !== false && Array.isArray(s.anim) && s.anim.length ? s.anim : null;
  const plan = `<div class="lv cs-st"><div class="lv-title"><span class="cs-tg t1">방침</span><span class="cs-tgs">규칙을 나눠 읽고 셀 길을 정해요</span></div>`
    + `<p><span class="cs-pn">포지티브</span> ${safeHtml(s.pos)}</p>`
    + `<p><span class="cs-ng">네거티브</span> ${safeHtml(s.neg)}</p>`
    + `<p class="cs-plan">→ ${safeHtml(s.plan)}</p></div>`;
  const stage = `<div class="fig-stage cs-stage">${boardHtml(s.board && s.board.length ? s.board : (s.steps || []).map((t) => ({ h: "", t })))}${diagramHtml(s.dg)}</div>`;
  const dev = `<div class="lv cs-st${anim ? " anim-level" : ""}"${anim ? ` data-anim="${esc(JSON.stringify(anim))}"` : ""}>`
    + `<div class="lv-title"><span class="cs-tg t2">전개</span><span class="cs-tgs">${anim ? "그림을 누르면 멈추고, 다시 누르면 이어서 움직여요" : "식을 세워 계산해요"}</span></div>`
    + stage + `</div>`;
  const check = `<div class="lv cs-st"><div class="lv-title"><span class="cs-tg t3">확인</span><span class="cs-tgs">다른 길로 다시 봐요</span></div><p>${safeHtml(s.check)}</p></div>`;
  const model = s.model ? `<div class="ma cs-ma"><b>모범 답안</b>${safeHtml(s.model)}</div>` : "";
  return `<div class="isol cs-sol">${plan}${dev}${check}${model}${rubricHtml(it)}</div>`;
}

/** 채점 기준(요소 · 비중) · 못 채운 것 · 감점 */
export function rubricHtml(it) {
  const s = it?.s || {};
  const rub = Array.isArray(s.rub) ? s.rub : [];
  if (!rub.length) return "";
  const C = "①②③④⑤⑥";
  const rows = rub.map(([e, pc], i) => `<tr><td class="cs-rn">${C[i] || i + 1}</td><td>${safeHtml(e)}</td><td class="cs-pc">${esc(pc)}%</td></tr>`).join("");
  const miss = (s.miss || []).map(([t, el]) => `<li>${safeHtml(t)} <span class="cs-el">→ ${esc(el)} 요소를 못 채움</span></li>`).join("");
  const ded = (s.ded || []).map(([t, p]) => `${safeHtml(t)} −${esc(p)}`).join(" · ");
  return `<details class="cs-rub"><summary>채점 기준 · 자주 하는 실수</summary>`
    + `<table class="cs-rt"><thead><tr><th></th><th>반드시 들어갈 요소</th><th>비중</th></tr></thead><tbody>${rows}</tbody></table>`
    + (miss ? `<div class="cs-miss"><b>못 채운 것</b><ul>${miss}</ul></div>` : "")
    + (ded ? `<div class="cs-ded"><b>감점</b> ${ded}</div>` : "")
    + `<p class="cs-rnote">배점은 시험지를 만들 때 정해요 — 요소 점수 = 배점 × 비중. 개념 오류는 감점이 아니라 그 요소를 못 채운 것으로 봐요.</p>`
    + `</details>`;
}

/** 큐가 짚는 키가 렌더 결과에 모두 있는지 (테스트 · 개발 확인용) */
export function missingCueKeys(it, html = solutionHtml(it)) {
  const out = [];
  for (const step of it?.s?.anim || []) for (const c of step || []) {
    for (const k of Array.isArray(c.k) ? c.k : [c.k]) {
      if (!html.includes(`data-k="${k}"`) && !new RegExp(`data-ka="([^"]*\\s)?${k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(\\s[^"]*)?"`).test(html)) out.push(k);
    }
  }
  return [...new Set(out)];
}
