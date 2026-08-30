// 게시판 — 익명 편지 커뮤니티 (상호 익명 · 1층)
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Board() {
  return (
    <Page title="게시판">
      <p className="d-note">서로 익명이에요. 같은 자리에서 기다리는 분들의 이야기.</p>
      <Card>
        <Row main="중2 아이, 요즘 말수가 줄었어요" sub="익명 · 댓글 4 · 어제" right={<Chip>고민</Chip>} />
        <Row main="시험 전날 뭐라고 말해주세요?" sub="익명 · 댓글 7 · 2일 전" right={<Chip tone="ac">인기</Chip>} />
        <Row main="오답노트를 같이 봐도 될까요" sub="익명 · 댓글 2 · 3일 전" right={<Chip>질문</Chip>} />
      </Card>
      <Card title="편지 쓰기">
        <textarea className="d-in" placeholder="익명으로 올라가요. 아이 실명·학교명은 적지 말아주세요." />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>올리기</button>
      </Card>
    </Page>
  );
}
