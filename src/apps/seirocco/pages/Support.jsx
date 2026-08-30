// 문의 — 운영자 채널 (전층)
import { Page, Card } from "../../../shared/demo";

export default function Support() {
  return (
    <Page title="문의">
      <Card>
        <p className="d-lbl">내용</p>
        <textarea className="d-in" placeholder="불편한 점, 제안, 오류 제보 — 무엇이든 좋아요" />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>보내기</button>
      </Card>
      <Card title="내 문의">
        <p className="d-note">아직 보낸 문의가 없어요.</p>
      </Card>
    </Page>
  );
}
