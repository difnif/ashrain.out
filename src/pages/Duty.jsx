// src/pages/Duty.jsx — 조교 (학생앱 신규 · 데모)
// 보직 6방 = 아바타 직업(수평) · 좌수·별감 = 향임 트랙(수직) · 1층 상주
import { Kit, Page, Card, Row, Chip } from "../shared/demo";
import { navigatePath } from "../shared/roles";

const DUTIES = [
  ["병방", "연산 훈련 조교", "연산 관문 30회 달성 시 해금", true],
  ["형방", "채점 보조", "OMR 채점 10회", false],
  ["예방", "개념 설명 도우미", "개념 카드 100장 열람", true],
  ["이방", "조 편성·신입 안내", "출석 30일", false],
  ["호방", "출석·포인트", "포인트 5,000P 누적", false],
  ["공방", "자료·꾸미기", "숍 아이템 3종 보유", false],
];

export default function Duty() {
  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <Page title="조교">
          <Card title="보직 — 자유 선택 (포인트로 변경)">
            {DUTIES.map(([n, r, c, open], i) => (
              <Row key={i} main={n + " · " + r} sub={open ? "해금됨 — 선택 가능" : c}
                right={i === 0 ? <Chip tone="ac">선택 중</Chip> : open ? <Chip tone="ok">해금</Chip> : <Chip>잠김</Chip>} />
            ))}
          </Card>
          <Card title="향임 트랙 — 좌수·별감">
            <p className="d-main" style={{ fontSize: 13, marginBottom: 8 }}>별감까지 40%</p>
            <div className="d-bar"><i style={{ width: "40%" }} /></div>
            <p className="d-sub" style={{ marginTop: 8 }}>연산 관문 · 조교 활동 · 아웃테스트로 올라가요. 성인 산식과는 별개.</p>
          </Card>
          <Card title="조교 작업실">
            <p className="d-note" style={{ marginBottom: 10 }}>조교가 되면 세이로코 제한 모드가 열려요 — 또래 개인 데이터에는 접근할 수 없어요.</p>
            <button className="d-btn pri" onClick={() => navigatePath("/seirocco")}>세이로코 열기</button>
          </Card>
        </Page>
      </div>
    </div>
  );
}
