// ashrain.out — 교실 모니터: 장면 설정 (params.js) — JSX 없음
// 장면이 controls 를 가지면(구슬 수·단계·문 개수 …) 화면 위쪽에 설정 칩이 뜬다.
//   controls: [{ key, label, kind: "step" | "seg", options: [값 | [값, 이름]], def, fmt?(값) → 글자, unit? }]
//   dur 은 수 또는 설정을 받는 함수 dur(P) — 설정에 따라 길이가 달라지는 장면(구슬 2000개 …)
export const optVal = (o) => (Array.isArray(o) ? o[0] : o);

/** 저장된 값 가운데 고를 수 있는 것만, 나머지는 기본값 */
export function paramsOf(pair, prm) {
  const P = {};
  for (const c of pair.controls || []) {
    const v = prm?.[pair.key]?.[c.key];
    P[c.key] = c.options.some((o) => optVal(o) === v) ? v : c.def;
  }
  return P;
}
/** 장면 길이(ms) — 설정에 따라 다를 수 있다 */
export const durOf = (pair, P) => (typeof pair.dur === "function" ? pair.dur(P || paramsOf(pair, null)) : pair.dur);
/** 설정 조합(검산용): 기본값 + 설정마다 처음·끝 값 */
export function paramCases(pair) {
  const base = paramsOf(pair, null), out = [base];
  for (const c of pair.controls || []) {
    for (const o of [c.options[0], c.options.at(-1)]) {
      const v = optVal(o);
      if (v !== base[c.key]) out.push({ ...base, [c.key]: v });
    }
  }
  return out;
}
