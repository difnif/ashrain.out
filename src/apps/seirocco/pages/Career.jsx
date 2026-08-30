// 승진 — 직급 사다리 · 산식 · 심사 (2층)
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Career() {
  return (
    <Page title="승진">
      <Card title="직급">
        <Row main="현감" sub="일반 강사 · 현재" right={<Chip tone="ac">현재</Chip>} />
        <Row main="현령" sub="다음 단계 — 심사 필요" right={<Chip tone="warn">심사 가능</Chip>} />
        <Row main="군수 · 부사" sub="학원 강사 트랙" right={<Chip>잠김</Chip>} />
        <Row main="목사 · 부윤" sub="원장 트랙" right={<Chip>잠김</Chip>} />
      </Card>
      <Card title="산식 — 매칭 학생 수 × 예측 적중률">
        <div className="d-stats">
          <Stat label="매칭 학생" value="4명" /><Stat label="적중률" value="85%" /><Stat label="점수" value="3.40" />
        </div>
        <p className="d-note" style={{ marginTop: 8 }}>공식 기록은 검증(2층)부터, 적중률은 계약 관계에서만 쌓여요.</p>
      </Card>
      <Card title="승진 심사">
        <p className="d-note" style={{ marginBottom: 10 }}>AI 학생 면담으로 진단 역량을 확인해요 — 온보딩 때와 같은 방식.</p>
        <button className="d-btn pri">심사 신청</button>
      </Card>
    </Page>
  );
}
