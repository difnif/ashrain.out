// ashrain.out — 촬영 모듈 순수 도우미 (DOM 없음). 단서 문구 찾기 · 끊어 읽기 문자열 · 신호등 합치기 · 제목.
export const CRITERIA = ["충실성", "논리성", "명료성", "간결성", "독창성"];

export const stripMarker = (s) => String(s || "").replace(/\[\[|\]\]/g, "");
/** 기록 제목 — 문항 앞 40자 */
export const titleOf = (q) => { const s = stripMarker(q).replace(/\s+/g, " ").trim(); return s.length > 40 ? s.slice(0, 40) + "…" : s; };

const norm = (s) => String(s || "").replace(/\[\[|\]\]/g, "").replace(/[−–]/g, "-").replace(/\s+/g, "");
const TAIL = /(에서는|으로는|에서|으로|보다|부터|까지|이고|이며|일때|인|은|는|이|가|을|를|의|에|로|와|과|도|만)$/;

/** 단서 문구를 문장 토큰 위에서 찾는다 → {t0,t1} (공백·마커 무시, 끝 조사·문장부호는 눈감아 준다). 못 찾으면 null */
export function findSpan(tokens, clue) {
  const owner = []; let hay = "";
  for (const t of tokens || []) { const n = norm(t.text); for (let k = 0; k < n.length; k++) owner.push(t.i); hay += n; }
  let needle = norm(clue);
  if (needle.length < 2) return null;
  let at = hay.indexOf(needle);
  if (at < 0) {
    const n2 = needle.replace(/[,.:;!?。]+$/, "").replace(TAIL, "");
    if (n2.length >= 2) { at = hay.indexOf(n2); if (at >= 0) needle = n2; }
  }
  if (at < 0) return null;
  const t0 = owner[at], t1 = owner[at + needle.length - 1];
  if (t0 == null || t1 == null) return null;
  return { t0, t1 };
}

/** 빗금 자리마다 " ／ " 를 넣은 끊어 읽기 문자열 (마커는 그대로 두어 MathText 로 그린다) */
export function cutText(tokens, marks) {
  const pts = new Set((marks || []).filter((m) => m.kind === "point" && m.func === "BOUND").map((m) => m.t0));
  const list = tokens || [];
  let out = "";
  for (let k = 0; k < list.length; k++) {
    const t = list[k]; out += t.text;
    if (!pts.has(t.i)) continue;
    const nx = list[k + 1];
    out += " ／" + (nx && (nx.kind === "space" || nx.kind === "newline") ? "" : " ");   // 원문 공백은 그대로, 빗금만 끼운다
  }
  return out.replace(/( ／ ?){2,}/g, " ／ ").replace(/ ／ ?$/, "");
}

/** 여러 문항의 신호등을 문서 하나로 — 평균 점수(초록 0 · 노랑 1 · 빨강 2): 1.2 이상 빨강, 0.4 이상 노랑 */
export function aggregateLights(list) {
  const rank = { green: 0, yellow: 1, red: 2 };
  const out = {};
  for (const k of CRITERIA) {
    const ls = (list || []).map((r) => r?.criteria?.[k]?.light).filter((l) => l in rank);
    if (!ls.length) { out[k] = { light: null, why: "" }; continue; }
    const n = { green: 0, yellow: 0, red: 0 }; for (const l of ls) n[l]++;
    const avg = ls.reduce((s, l) => s + rank[l], 0) / ls.length;
    out[k] = { light: avg >= 1.2 ? "red" : avg >= 0.4 ? "yellow" : "green", why: `초록 ${n.green} · 노랑 ${n.yellow} · 빨강 ${n.red}` };
  }
  return out;
}
