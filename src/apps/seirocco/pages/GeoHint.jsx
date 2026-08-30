// 서무 3 — 도형 힌트 표시 습관 · md 스펙 대기
// 연결점: 지오 힌트 체계(G코드 · 만족 밴드) — 힌트는 풀이의 파생 뷰.
import { Card, Row, Chip } from "../../../shared/demo";

export default function GeoHint() {
  return (
    <>
      <Card title="내 힌트 표시">
        <Row main="보조선 — 평행선 긋기" sub="G-12 · 이번 주 9회" right={<Chip tone="ac">G-12</Chip>} />
        <Row main="닮음 표시 — 대응각 점찍기" sub="G-07 · 이번 주 6회" right={<Chip>G-07</Chip>} />
      </Card>
      <div className="d-vault" style={{ marginTop: 12 }}>
        <p className="d-sub">📄 스펙 문서(md) 대기 중.</p>
      </div>
    </>
  );
}
