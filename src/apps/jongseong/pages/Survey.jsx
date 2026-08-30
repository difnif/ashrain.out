// 학부모 설문 — 선택 참여
import { Page, Card } from "../../../shared/demo";

export default function Survey() {
  return (
    <Page title="설문">
      <p className="d-note">선택 참여예요 — 답하신 내용 중 공개 문항만 익명으로 팁 지면에 실릴 수 있어요.</p>
      <Card title="이번 달 문항">
        <p className="d-lbl">1. 집에서 효과 있었던 공부 습관 하나 (공개)</p>
        <textarea className="d-in" />
        <p className="d-lbl">2. 앱에서 아쉬운 점 (비공개)</p>
        <textarea className="d-in" />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>제출</button>
      </Card>
    </Page>
  );
}
