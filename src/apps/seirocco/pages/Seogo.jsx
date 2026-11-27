// 서고 — 시록고의 심장: 기록이 쌓이는 곳. 하위 3고(장서고·문서고·기록고) + 전공 수학 서가(대학 전공 수학 — 분야별 서가, 읽기 전용).
// 탭을 누르면 주소(#/seogo/<탭>)가 바뀐다 — 전공 수학은 #/seogo/jeon/<책>/<장> 까지 깊이 들어간다(MajorMath.jsx).
import { useEffect, useState } from "react";
import { Page, Tabs, go } from "../../../shared/demo";
import Jangseogo from "./Jangseogo";
import Munseogo from "./Munseogo";
import Girokgo from "./Girokgo";
import MajorMath from "./MajorMath";

const TABS = [["jang", "장서고"], ["mun", "문서고"], ["girok", "기록고"], ["jeon", "전공 수학"]];

export default function Seogo({ param }) {
  const [tab, setTab] = useState(param || "jang");
  useEffect(() => { if (param) setTab(param); }, [param]);
  const pick = (k) => { setTab(k); go("#/seogo/" + k); };
  return (
    <Page title="서고">
      <Tabs cur={tab} onSel={pick} items={TABS} />
      {tab === "jang" ? <Jangseogo /> : tab === "mun" ? <Munseogo /> : tab === "jeon" ? <MajorMath /> : <Girokgo />}
    </Page>
  );
}
