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
        <Row main="대학 전공 수학 — 분야별 서가" sub="미적분학 · 선형대수 · 미분방정식 · 확률 · 통계에서 공학 · 자연과학 · 데이터 · 경제까지 — 움직이는 그림 · 풀이가 있는 연습"
          right={<Chip tone="ok">열람</Chip>} onClick={() => go("#/seogo/jeon")} />
      </Card>
      <p className="d-note" style={{ marginTop: 12 }}>빌리고, 돌려놓고, 기록이 남아요.</p>
    </>
  );
}
