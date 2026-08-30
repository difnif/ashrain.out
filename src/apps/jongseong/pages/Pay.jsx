// 결제 — 수강 결제(웹 결제) · 내역
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Pay() {
  return (
    <Page title="결제">
      <Card title="이번 달 수강">
        <Row main="중2 수학 정규 · 주 2회" sub="담당: 박재우 강사 · 9월분" right={<Chip tone="warn">결제 대기</Chip>} />
        <button className="d-btn pri full" style={{ marginTop: 8 }}>웹으로 결제하기</button>
        <p className="d-note" style={{ marginTop: 8 }}>결제는 웹 결제창에서 진행돼요. 계약 조건은 계약서에서 언제든 확인할 수 있어요.</p>
      </Card>
      <Card title="결제 내역">
        <Row main="8월분 수강료" sub="8월 1일 · 카드" right={<Chip tone="ok">완료</Chip>} />
        <Row main="7월분 수강료" sub="7월 1일 · 카드" right={<Chip tone="ok">완료</Chip>} />
      </Card>
    </Page>
  );
}
