// #/solve/* 해시 → 화면. App.jsx 는 이 라우터만 안다.
//   #/solve                      허브
//   #/solve/set[/<conceptId>]    개념별 문항 세트 풀기
//   #/solve/item/<itemId>        문항 하나 다시 풀기 (?from=wrong)
//   #/solve/practice             예제·유제 개념 고르기 → #/p/<conceptId>
//   #/solve/omr[/new|/grade[/<code>]]  사진 채점
//   #/solve/read[/<itemId>]      문장 해설
//   #/solve/mark[/<itemId>]      표시 연습
//   #/solve/essay[/<itemId>]     서술형 자가채점
//   #/solve/ask/<itemId>         문항 질문하기
import { lazy, Suspense } from "react";
import Solve, { PracticePick } from "./Solve";

const ItemPlay = lazy(() => import("./ItemPlay"));
const Omr = lazy(() => import("./Omr"));
const Read = lazy(() => import("./Read"));
const Mark = lazy(() => import("./Mark"));
const Essay = lazy(() => import("./Essay"));
const AskItem = lazy(() => import("./AskItem"));

const clean = (s) => (s ? decodeURIComponent(s.split("?")[0]) : undefined);

export default function SolveRouter({ hash, theme }) {
  const path = hash.replace(/^#\/solve\/?/, "").split("?")[0];
  const [seg, ...rest] = path.split("/");
  const id = clean(rest[0]);
  let el;
  switch (seg) {
    case "": case undefined: el = <Solve />; break;
    case "set": el = <ItemPlay conceptId={id} hash={hash} />; break;
    case "item": el = <ItemPlay itemId={id} hash={hash} />; break;
    case "practice": el = <PracticePick />; break;
    case "omr": el = <Omr sub={rest.join("/")} hash={hash} />; break;
    case "read": el = <Read itemId={id} />; break;
    case "mark": el = <Mark itemId={id} />; break;
    case "essay": el = <Essay itemId={id} />; break;
    case "ask": el = <AskItem itemId={id} theme={theme} />; break;
    default: el = <Solve />;
  }
  return <Suspense fallback={<div className="sv-wrap sv-muted">불러오는 중…</div>}>{el}</Suspense>;
}
