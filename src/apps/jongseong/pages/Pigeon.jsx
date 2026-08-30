// 전서구 — 유저 간 자유 대화·상담의 소통권
// 매월 32마리 지급(축적 없음) · 남은 것은 월말 4마리→상급 1마리 자동 합성 · 대화 열 때마다 1마리 소모
// 등급 수·고급 전서구 수신 보상은 [미결]
import { useState } from "react";
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Pigeon() {
  const [gate, setGate] = useState("basic");
  const [expose, setExpose] = useState(true);
  return (
    <Page title="전서구">
      <div className="d-stats">
        <Stat label="이달 지급" value="32" />
        <Stat label="남은 기본" value="21" />
        <Stat label="상급 (합성)" value="2" />
      </div>
      <Card title="합성 규칙">
        <p className="d-note">쓰고 남은 전서구는 다음 달로 넘어가지 않아요. 대신 월말에 4마리가 한 마리의 상급 전서구로 몸을 바꿔요 — 21마리면 상급 5, 나머지 1은 하늘로.</p>
      </Card>
      <Card title="내가 받는 문턱">
        <p className="d-lbl">이 등급 이상의 전서구만 내 앞에 앉아요</p>
        <select className="d-in" value={gate} onChange={(e) => setGate(e.target.value)}>
          <option value="basic">기본 — 누구든 환영</option>
          <option value="g2">2급 이상</option>
          <option value="g3">3급 이상 — 조용히 지내고 싶어요</option>
        </select>
        <label className="d-sub" style={{ display: "flex", gap: 6, marginTop: 10, alignItems: "center" }}>
          <input type="checkbox" checked={expose} onChange={(e) => setExpose(e.target.checked)} />
          높은 등급 전서구를 먼저 보이게 (우선 노출) — 끄면 도착 순서대로
        </label>
      </Card>
      <p className="d-note">등급 개수와 고급 전서구를 많이 받은 이의 보상은 아직 정하지 않았어요 [미결]. 하소에서 마음 맞는 이에게 전서구를 보내 대화를 열어요 — 방은 30일 뒤 스스로 닫혀요.</p>
    </Page>
  );
}
