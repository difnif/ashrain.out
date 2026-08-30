// 더보기
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function More({ isAdmin }) {
  return (
    <Page title="더보기">
      <Card>
        <Row main="게시판" sub="익명 편지 커뮤니티" onClick={() => (location.hash = "#/board")} />
        <Row main="결제" sub="수강 결제 · 내역" right={<Chip tone="warn">9월분 대기</Chip>} onClick={() => (location.hash = "#/pay")} />
        <Row main="선물" sub="스킨·표지 카탈로그" onClick={() => (location.hash = "#/gift")} />
        <Row main="설문" sub="선택 참여" onClick={() => (location.hash = "#/survey")} />
        <Row main="자녀 연결" sub="연결 코드로 등록" onClick={() => (location.hash = "#/link")} />
        {isAdmin && <Row main="녹음 창고" sub="음성 자산 보관처(추후)" right={<Chip tone="warn">관리자</Chip>} onClick={() => (location.hash = "#/vault")} />}
      </Card>
    </Page>
  );
}
