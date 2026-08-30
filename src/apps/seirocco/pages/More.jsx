// 더보기
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function More({ isAdmin }) {
  return (
    <Page title="더보기">
      <Card>
        <Row main="하소" sub="공통 광장 — 익명 고민" onClick={() => (location.hash = "#/haso")} />
        <Row main="방" sub="공통 광장 — 신문 벽" onClick={() => (location.hash = "#/bang")} />
        <Row main="마이페이지" sub="직급 · 검증 · 이용권" onClick={() => (location.hash = "#/my")} />
        <Row main="문의" sub="운영자 채널" onClick={() => (location.hash = "#/support")} />
        {isAdmin && <Row main="폰트 창고" sub="UI 서체 수집처" right={<Chip tone="warn">관리자</Chip>} onClick={() => (location.hash = "#/fonts")} />}
      </Card>
    </Page>
  );
}
