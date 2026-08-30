// 주간 서신 — 점수표가 아닌 서사. 검증 템플릿 + 데이터 슬롯(LLM 자유 작문 금지)
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Letters({ param }) {
  if (param) return (
    <Page title="여덟 번째 서신" right={<Chip>8월 넷째 주</Chip>}>
      <Card>
        <div className="d-serif" style={{ fontSize: 14.5 }}>
          <p>이번 주는 도형의 닮음을 지나 닮음비에 닿았습니다. 새로 만난 개념은 둘, 다시 꺼내 본 개념은 셋이었습니다.</p>
          <p>오답노트에는 세 문제가 새로 들어왔습니다. 그중 한 문제 곁에 스스로 단 메모가 있었습니다 — 틀린 이유를 자기 말로 적어 두는 습관이 자라고 있습니다.</p>
        </div>
        <div style={{ borderTop: "1px solid var(--bd)", marginTop: 14, paddingTop: 12,
          display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ color: "var(--ac)", fontSize: 13 }}>“질문이 좋아지고 있습니다.”</span>
          <span className="d-sp" />
          <span className="d-sub">— 담당 강사</span>
        </div>
      </Card>
      <button className="d-btn" onClick={() => (location.hash = "#/letters")}>← 목록</button>
    </Page>
  );
  return (
    <Page title="주간 서신">
      <Card>
        <Row main="여덟 번째 서신" sub="8월 넷째 주 · 닮음비" right={<Chip tone="ac">새 서신</Chip>} onClick={() => (location.hash = "#/letters/1")} />
        <Row main="일곱 번째 서신" sub="8월 셋째 주 · 도형의 닮음" onClick={() => (location.hash = "#/letters/1")} />
        <Row main="여섯 번째 서신" sub="8월 둘째 주 · 삼각형의 성질" onClick={() => (location.hash = "#/letters/1")} />
      </Card>
    </Page>
  );
}
