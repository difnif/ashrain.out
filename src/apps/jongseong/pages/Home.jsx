// 종성 홈 — 안방: 세 화폐 잔고 + 마루 소식 + 하소 · 결제(밥 짓는 소리)가 중심
// 반감시 원칙 유지: 성적·문항 숫자는 없다. 잔고는 화폐일 뿐.
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Home() {
  return (
    <Page title="안녕하세요">
      <div className="d-stats">
        <Stat label="장작" value="240근" />
        <Stat label="연" value="3" />
        <Stat label="전서구" value="21+2" />
      </div>
      <Card title="불씨">
        <div style={{ display: "flex", gap: 8 }}>
          <button className="d-btn pri" style={{ flex: 1 }} onClick={() => (location.hash = "#/firewood")}>밥 짓는 소리 — 장작 들이기</button>
          <button className="d-btn" style={{ flex: 1 }} onClick={() => (location.hash = "#/stoke")}>아궁이에 불 때기</button>
        </div>
      </Card>
      <Card title="마루에 새로 놓인 것">
        <Row main="여덟 번째 보고서" sub="8월 넷째 주 · 담당 강사" right={<Chip tone="ac">새 글</Chip>} onClick={() => (location.hash = "#/maru")} />
        <Row main="문제 꾸러미 — 판별식 확인 3문항" sub="자녀에게 출제해보세요" right={<Chip tone="warn">대기</Chip>} onClick={() => (location.hash = "#/maru")} />
      </Card>
      <Card title="하소">
        <Row main="시험 전날 뭐라고 말해주는 게 좋을까요" sub="익명 · 연 31개 받음" right={<Chip>인기</Chip>} onClick={() => (location.hash = "#/haso")} />
      </Card>
    </Page>
  );
}
