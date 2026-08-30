// 마루 — 자녀의 공부를 지켜보는 곳 (세세한 모니터링 아님)
// 매칭 강사가 보내는 보고서·숙제·알림장이 쌓이고, 넘겨받은 문제를 자녀에게 출제 → 응답 후 풀이·오답 확인.
import { useState } from "react";
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Maru() {
  const [st, setSt] = useState("ready"); // ready → sent → done (문제 꾸러미 데모 상태)
  return (
    <Page title="마루">
      <Card title="강사가 건넨 것들">
        <Row main="여덟 번째 보고서" sub="8월 넷째 주 · 닮음비를 지나는 중" right={<Chip tone="ac">보고서</Chip>} />
        <Row main="알림장 — 다음 주 진도" sub="이차방정식 들어가요 · 준비물 없음" right={<Chip>알림장</Chip>} />
        <Row main="숙제 — 근의 공식 15문항" sub="어제 배부 · 12/15 제출" right={<Chip tone="ok">숙제</Chip>} />
      </Card>
      <Card title="문제 꾸러미 — 직접 확인해보세요">
        <Row main="판별식 확인 3문항" sub="강사: 이 부분만 한번 짚어봐 주세요" right={
          st === "ready" ? <button className="d-btn pri" style={{ padding: "6px 10px" }} onClick={() => setSt("sent")}>자녀에게 출제</button>
          : st === "sent" ? <button className="d-btn" style={{ padding: "6px 10px" }} onClick={() => setSt("done")}>응답 대기…</button>
          : <Chip tone="ok">응답 완료</Chip>} />
        {st === "done" && (
          <div className="d-vault" style={{ marginTop: 10 }}>
            <p className="d-sub" style={{ marginBottom: 6 }}>자녀 응답 — 2/3 정답</p>
            <p className="d-note">3번 오답 · 풀이 과정에서 D=0 케이스를 두 근으로 셌어요. 풀이 전문은 펼쳐서 볼 수 있어요.</p>
          </div>
        )}
      </Card>
      <p className="d-note">점수판이 아니라 마루예요 — 강사가 골라 건넨 것만 이 위에 놓여요.</p>
    </Page>
  );
}
