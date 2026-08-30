// 마이페이지 — 등급(현감~) · 산식 · 심사 · 검증 · 이용권
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function My() {
  return (
    <Page title="마이페이지">
      <Card title="직급">
        <Row main="현감" sub="일반 강사 · 현재" right={<Chip tone="ac">현재</Chip>} />
        <Row main="현령" sub="다음 단계 — 심사 필요" right={<Chip tone="warn">심사 가능</Chip>} />
        <Row main="군수 · 부사 → 목사 · 부윤" sub="학원 강사 → 원장 트랙" right={<Chip>잠김</Chip>} />
      </Card>
      <Card title="산식 — 매칭 학생 수 × 예측 적중률">
        <div className="d-stats">
          <Stat label="매칭 학생" value="3명" /><Stat label="적중률" value="—" /><Stat label="점수" value="—" />
        </div>
        <button className="d-btn" style={{ marginTop: 10 }}>승진 심사 신청</button>
      </Card>
      <Card title="검증">
        <Row main="강사등록증" sub="서류 심사로 실명 활동 자격(2층)" right={<Chip tone="warn">미제출</Chip>} />
      </Card>
      <Card title="이용권">
        <Row main="사무 (행정)" sub="학생·숙제·발신" right={<Chip tone="ok">무료</Chip>} />
        <Row main="서무 + 문서고 (코퍼스)" sub="가격·구성 [미결]" right={<Chip tone="warn">유료</Chip>} />
      </Card>
    </Page>
  );
}
