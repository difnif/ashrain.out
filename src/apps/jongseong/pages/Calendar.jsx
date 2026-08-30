// 일정 — 시험 D-day + 상담 신청(→세이로코)
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Calendar() {
  return (
    <Page title="일정">
      <Card title="다가오는 일정">
        <Row main="2학기 중간고사" sub="9월 1일 (월)" right={<Chip tone="down">D-2</Chip>} />
        <Row main="학원 휴강일" sub="9월 12일 (금) — 추석 연휴" right={<Chip>D-13</Chip>} />
      </Card>
      <Card title="상담 신청">
        <p className="d-lbl">희망 시간대</p>
        <select className="d-in"><option>평일 저녁 (19~21시)</option><option>주말 오전</option><option>강사님 편한 시간</option></select>
        <p className="d-lbl">남기고 싶은 말 (선택)</p>
        <textarea className="d-in" placeholder="상담에서 나누고 싶은 주제가 있다면" />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>신청 — 담당 강사에게 전달돼요</button>
      </Card>
    </Page>
  );
}
