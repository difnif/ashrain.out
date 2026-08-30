// 자녀 연결 — 보호자 동의 인프라 재사용 예정
import { Page, Card } from "../../../shared/demo";

export default function Link() {
  return (
    <Page title="자녀 연결">
      <Card>
        <p className="d-lbl">자녀 확인 코드</p>
        <input className="d-in" placeholder="자녀 앱 마이페이지의 연결 코드" />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>연결 요청</button>
        <p className="d-note" style={{ marginTop: 10 }}>연결이 확인되면 주간 서신·응원·일정이 열려요. 미성년 동의 절차와 같은 안전 장치를 써요.</p>
      </Card>
    </Page>
  );
}
