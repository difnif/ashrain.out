// 장서고 — 대출 가능한 책 (무료)
import { Card, Row, Chip, go } from "../../../shared/demo";

export default function Jangseogo() {
  return (
    <>
      <Card title="서가">
        <Row main="수학이 필요한 순간" sub="김민형 · 권장도서" right={<Chip>서가</Chip>} />
        <Row main="가르칠 수 있는 용기" sub="파커 파머" right={<Chip tone="warn">대출 중</Chip>} />
        <Row main="페르마의 마지막 정리" sub="사이먼 싱" right={<Chip>서가</Chip>} />
        <Row main="수학의 정석 (1966 초판 영인)" sub="소장 자료 · 열람만" right={<Chip tone="ac">귀중서</Chip>} />
      </Card>
      <Card title="전공 수학 서가">
        <Row main="대학 전공 수학 9권 — 바로 읽기" sub="대학수학 · 경제수학 · 무역학 · 기계공학 · 천문공학 · 전자공학 · 데이터 공학 · 물리학 · 통계학"
          right={<Chip tone="ok">열람</Chip>} onClick={() => go("#/seogo/jeon")} />
      </Card>
      <p className="d-note" style={{ marginTop: 12 }}>빌리고, 돌려놓고, 기록이 남아요.</p>
    </>
  );
}
