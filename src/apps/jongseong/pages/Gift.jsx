// 선물 — 숍 카탈로그(디지털 재화) → 자녀에게
import { Page, Card, Chip } from "../../../shared/demo";

const ITEMS = [
  ["카드 스킨 · 먹빛", "1,200P"], ["OMR 시트 스킨", "900P"],
  ["오답노트 표지 · 한지", "1,500P"], ["프로필 테두리 · 금박", "2,000P"],
];

export default function Gift() {
  return (
    <Page title="선물">
      <p className="d-note">기능이 아니라 꾸밈을 선물해요 — 학습 유불리와 무관해요.</p>
      <div className="d-grid2">
        {ITEMS.map(([n, p], i) => (
          <Card key={i}>
            <div style={{ height: 54, background: "var(--in)", borderRadius: 8, marginBottom: 10 }} />
            <p className="d-main" style={{ fontSize: 13 }}>{n}</p>
            <div style={{ display: "flex", alignItems: "center", marginTop: 6 }}>
              <Chip tone="ac">{p}</Chip><span className="d-sp" />
              <button className="d-btn" style={{ padding: "6px 10px" }}>선물</button>
            </div>
          </Card>
        ))}
      </div>
    </Page>
  );
}
