// 더보기 — 종성의 나머지 방들
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function More({ isAdmin }) {
  return (
    <Page title="더보기">
      <Card>
        <Row main="밥 짓는 소리" sub="장작·구독권 결제" right={<Chip tone="ac">결제</Chip>} onClick={() => (location.hash = "#/firewood")} />
        <Row main="아궁이에 불 때기" sub="자녀에게 장작 선물" onClick={() => (location.hash = "#/stoke")} />
        <Row main="정안수 떠놓는 곳" sub="구독권 지정 선물 · 스킨" onClick={() => (location.hash = "#/offering")} />
        <Row main="글 읽는 소리" sub="학부모 서재 — 글로 연을 벌어요" onClick={() => (location.hash = "#/reading")} />
        <Row main="백돌길" sub="아이들 사이에서 반짝인 것들" onClick={() => (location.hash = "#/baekdol")} />
        <Row main="전서구" sub="대화 문턱·합성 관리" onClick={() => (location.hash = "#/pigeon")} />
        <Row main="마이페이지" sub="계정 · 인연(자녀 등록)" onClick={() => (location.hash = "#/my")} />
        {isAdmin && <Row main="녹음 창고" sub="음성 자산 보관처" right={<Chip tone="warn">관리자</Chip>} onClick={() => (location.hash = "#/vault")} />}
      </Card>
    </Page>
  );
}
