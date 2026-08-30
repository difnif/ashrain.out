// 서고 — 시록고의 심장: 기록이 쌓이는 곳. 하위 3고(장서고·문서고·기록고).
import { useEffect, useState } from "react";
import { Page, Tabs } from "../../../shared/demo";
import Jangseogo from "./Jangseogo";
import Munseogo from "./Munseogo";
import Girokgo from "./Girokgo";

export default function Seogo({ param }) {
  const [tab, setTab] = useState(param || "jang");
  useEffect(() => { if (param) setTab(param); }, [param]);
  return (
    <Page title="서고">
      <Tabs cur={tab} onSel={setTab} items={[["jang", "장서고"], ["mun", "문서고"], ["girok", "기록고"]]} />
      {tab === "jang" ? <Jangseogo /> : tab === "mun" ? <Munseogo /> : <Girokgo />}
    </Page>
  );
}
