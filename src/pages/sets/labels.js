// ashrain.out — 컨셉 문제: 짧은 이름표 (순수)
export const LEVELS = ["하", "중", "상"];
export const LEVEL_NAME = { 하: "기본", 중: "발전", 상: "심화" };

/** 답 꼴 안내 — 입력 칸 위 한 줄 */
export function kindLabel(item) {
  const a = item?.a || {};
  if (a.k === "frac") return "확률은 기약분수로 — 분자와 분모를 칸에 써요 (0 · 1 은 분자 칸에만)";
  if (a.k === "pick") return "옳은 것을 모두 골라요";
  if (a.k === "pair") return `${(a.l || []).join(" · ")}을 차례로 써요`;
  return a.u ? `수만 써요 (단위 ${a.u}는 빼고)` : "수만 써요";
}

/** OMR 칸 종류 이름 */
export function omrKindName(kind) {
  return kind === "frac" ? "분수" : kind === "pick" ? "보기" : kind === "pair" ? "두 수" : "정수";
}

/** OMR 판독 경고 */
export function flagName(flag) {
  return flag === "double" ? "한 자리에 두 개 칠함" : flag === "gap" ? "숫자 사이가 비었어요" : flag === "weak" ? "흐리게 칠함" : "";
}

/** 판독 실패 이유 → 안내 */
export function reasonText(reason, extra = {}) {
  switch (reason) {
    case "markers": return "네 모서리의 검은 네모를 찾지 못했어요 — 카드 전체가 나오게, 위에서 똑바로 다시 찍어 주세요";
    case "orient": return "카드 방향을 알아보지 못했어요 — 왼쪽 위 검은 네모 옆 막대가 보이게 다시 찍어 주세요";
    case "warp": return "카드를 펴지 못했어요 — 조금 떨어져서 다시 찍어 주세요";
    case "other-set": return `다른 세트의 OMR 카드예요${extra.set ? ` (${String(extra.set).padStart(2, "0")}번 세트)` : ""} — 이 세트의 카드를 찍어 주세요`;
    case "band": return "몇 쪽인지 읽지 못했어요 — 아래에서 쪽을 골라 주세요";
    default: return "사진을 읽지 못했어요 — 다시 찍어 주세요";
  }
}
