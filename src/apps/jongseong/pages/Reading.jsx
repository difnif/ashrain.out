// 글 읽는 소리 — 학부모의 서재: 대출 + 독후감·논평·에세이. 글을 쓰면 '연'이 쌓인다.
// 작성 폼 구조(발산→수렴, 인용 서랍 격리)는 타 세션 합의 준용.
import { useState } from "react";
import { Page, Card, Row, Chip, Tabs } from "../../../shared/demo";

export default function Reading() {
  const [tab, setTab] = useState("b");
  return (
    <Page title="글 읽는 소리" right={<Chip tone="ac">보유 연 3</Chip>}>
      <Tabs cur={tab} onSel={setTab} items={[["b", "서가"], ["w", "내 글"]]} />
      {tab === "b" ? (
        <Card title="대출 가능한 책">
          <Row main="수학이 필요한 순간" sub="김민형 · 권장도서" right={<Chip>서가</Chip>} />
          <Row main="어떻게 말해줘야 할까" sub="오은영 · 학부모 권장" right={<Chip tone="warn">대출 중</Chip>} />
          <Row main="페르마의 마지막 정리" sub="사이먼 싱" right={<Chip>서가</Chip>} />
        </Card>
      ) : (
        <Card title="내 글 — 한 편마다 연 1개">
          <Row main="아이와 같은 책을 읽는다는 것" sub="독후감 · 8월 20일 · 방에 게시됨" right={<Chip tone="ac">연 +1</Chip>} />
          <Row main="숙제를 대신 봐주지 않기로 했다" sub="에세이 · 8월 11일" right={<Chip tone="ac">연 +1</Chip>} />
          <button className="d-btn pri full" style={{ marginTop: 10 }}>새 글 쓰기</button>
        </Card>
      )}
      <p className="d-note">연은 하소에 고민을 날려 보낼 때 쓰여요 — 발언권은 읽고 쓴 만큼.</p>
    </Page>
  );
}
