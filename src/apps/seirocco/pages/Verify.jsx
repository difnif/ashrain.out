// 강사 검증 — 서류 심사로 2층 진입 (1층)
import { Page, Card, Chip } from "../../../shared/demo";

export default function Verify() {
  return (
    <Page title="강사 검증" right={<Chip tone="warn">미제출</Chip>}>
      <Card title="서류 제출">
        <div className="d-vault" style={{ textAlign: "center", padding: "26px 12px" }}>
          <p className="d-main" style={{ marginBottom: 4 }}>강사등록증 업로드</p>
          <p className="d-sub">JPG · PDF — 운영자가 확인 후 승인해요 (1~2일)</p>
        </div>
        <button className="d-btn pri full" style={{ marginTop: 10 }}>파일 선택</button>
      </Card>
      <p className="d-note">검증(2층)을 통과하면 실명 활동·승진 기록이 시작돼요. 학생 데이터 열람은 검증이 아니라 계약(3층)에 붙어요.</p>
    </Page>
  );
}
