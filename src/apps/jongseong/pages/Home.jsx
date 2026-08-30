// 종성 홈 — 숫자 없는 홈: 서신 · D-day · 응원 · 선물
import { Page, Card, Chip } from "../../../shared/demo";

export default function Home() {
  return (
    <Page title="안녕하세요">
      <Card title="이번 주 서신">
        <p className="d-serif" style={{ fontSize: 14.5, margin: 0 }}>
          이번 주는 닮음비를 지났습니다. 오답노트에 스스로 단 메모가 눈에 띄게 늘었습니다…
        </p>
        <button className="d-btn" style={{ marginTop: 12 }} onClick={() => (location.hash = "#/letters/1")}>이어 읽기</button>
      </Card>
      <Card title="다가오는 일정">
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <Chip tone="down">D-2</Chip>
          <span className="d-main">2학기 중간고사</span>
          <span className="d-sp" />
          <button className="d-btn" onClick={() => (location.hash = "#/calendar")}>일정 보기</button>
        </div>
      </Card>
      <Card title="응원 한 마디">
        <p className="d-note" style={{ marginBottom: 10 }}>점수 이야기 없이, 마음만 보내는 채널이에요.</p>
        <button className="d-btn pri" onClick={() => (location.hash = "#/cheer")}>응원 보내기</button>
      </Card>
      <Card title="선물">
        <p className="d-note" style={{ marginBottom: 10 }}>카드 스킨·오답노트 표지 같은 작은 선물로 마음을 전해요.</p>
        <button className="d-btn" onClick={() => (location.hash = "#/gift")}>선물 고르기</button>
      </Card>
    </Page>
  );
}
