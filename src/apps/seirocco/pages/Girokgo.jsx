// 기록고 — 독후감·논평·에세이 (무료 · 글은 방榜에 게시 가능)
import { Card, Row, Chip } from "../../../shared/demo";

export default function Girokgo() {
  return (
    <>
      <Card title="내 기록">
        <Row main="설명이 짧아질 때 배움이 길어진다" sub="에세이 · 8월 19일 · 방에 게시됨" right={<Chip tone="ac">게시</Chip>} />
        <Row main="『가르칠 수 있는 용기』를 읽고" sub="독후감 · 8월 5일" right={<Chip>보관</Chip>} />
        <button className="d-btn pri full" style={{ marginTop: 10 }}>새 기록 쓰기</button>
      </Card>
      <p className="d-note" style={{ marginTop: 12 }}>강사의 글도 같은 벽(방)에 붙어요 — 학생·학부모와 한 광장.</p>
    </>
  );
}
