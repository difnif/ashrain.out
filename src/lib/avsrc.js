// ashrain.out — 프린트가 있는 시청각 콘텐츠 하나를 key 로 찾기 (lib/avsrc.js) — 순수 도우미
// 유형별 문제 세트(e-ten) · 유형(e-ten.3) · 주차별 회차(w-e3-07a) — 셋 다 문제지 · 해설지 · 빠른 정답 · OMR 프린트가 있다(frames/docsmenu.jsx).
//   쓰는 곳: 학생앱 목록에서 꾹 눌러 프린트 받기(components/AvPrintSheet.jsx) · 듀얼 모드 「문제 풀이 해설 전부」(frames/allspec.jsx).
//   해설 액자(그래프 그리기 · 10단계 계산 · 그래프와 넓이 · 경우의 수와 확률 100제)는 프린트 문서가 없어 null.
//   { key, kind: "unit" | "type" | "week", meta() 머리 정보 | null, set() 문항 | null, ready() 다 들어왔나, load() → Promise }
import { basicOf, basicCached, loadBasic } from "../features/display/basics/index.js";
import { parseWeekId, weekMetaCached, weekCached, loadWeekIndex, loadWeek } from "../features/display/weeks/index.js";
import { parseTypeKey, typeMeta, typeCached, loadType } from "./avtypes.js";

export function avSource(key) {
  const k = String(key ?? "");
  const w = parseWeekId(k);
  if (w) {
    return { key: k, kind: "week", meta: () => weekMetaCached(k), set: () => weekCached(k),
      ready: () => !!(weekMetaCached(k) && weekCached(k)), load: () => Promise.all([loadWeekIndex(w.gk), loadWeek(k)]).then(() => weekCached(k)) };
  }
  if (parseTypeKey(k)) return { key: k, kind: "type", meta: () => typeMeta(k), set: () => typeCached(k), ready: () => !!typeCached(k), load: () => loadType(k) };
  if (basicOf(k)) return { key: k, kind: "unit", meta: () => basicOf(k), set: () => basicCached(k), ready: () => !!basicCached(k), load: () => loadBasic(k) };
  return null;
}
/** 프린트를 받을 수 있나 */
export const hasPrint = (key) => !!avSource(key);
