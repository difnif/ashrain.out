// 문서고 — 유저 수집 문제 DB (코퍼스 계열 · 유료) — 가격 [미결]
import { Card, Row, Chip } from "../../../shared/demo";

export default function Munseogo() {
  return (
    <>
      <div style={{ display: "flex", gap: 6, marginBottom: 4 }}>
        <Chip tone="warn">코퍼스 · 유료</Chip>
      </div>
      <Card title="내가 모은 문제">
        <Row main="이차방정식 활용 — 변형 7제" sub="8월 수집 · 태그: 근의 공식, 실생활" right={<Chip tone="ac">7</Chip>} />
        <Row main="닮음비 서술형 묶음" sub="7월 수집 · 태그: 서술형" right={<Chip tone="ac">4</Chip>} />
        <Row main="+ 문제 수집하기" sub="촬영·업로드·타 자료 참조로 나만의 DB를 쌓아요" />
      </Card>
      <p className="d-note" style={{ marginTop: 12 }}>여기 쌓인 문제는 당신의 재산이에요 — 수업·숙제·꾸러미로 바로 흘려보낼 수 있어요.</p>
    </>
  );
}
