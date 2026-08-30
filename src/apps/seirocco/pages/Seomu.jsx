// 서무 — 코퍼스를 쌓는 작업실 (유료 계열 · 가격 [미결])
// 세 작업실 각각 md 스펙 문서 대기 중 — 도착하면 해당 파일만 교체.
import { useEffect, useState } from "react";
import { Page, Tabs, Chip } from "../../../shared/demo";
import SolutionMemo from "./SolutionMemo";
import Marking from "./Marking";
import GeoHint from "./GeoHint";

export default function Seomu({ param }) {
  const [tab, setTab] = useState(param || "sol");
  useEffect(() => { if (param) setTab(param); }, [param]);
  return (
    <Page title="서무" right={<Chip tone="warn">코퍼스 · 유료</Chip>}>
      <p className="d-note">여기서 남긴 것은 전부 당신의 코퍼스가 돼요 — 풀이의 결, 표시의 습관, 힌트의 감각.</p>
      <Tabs cur={tab} onSel={setTab} items={[["sol", "풀이 메모"], ["mark", "문제 표시"], ["geo", "도형 힌트"]]} />
      {tab === "sol" ? <SolutionMemo /> : tab === "mark" ? <Marking /> : <GeoHint />}
    </Page>
  );
}
