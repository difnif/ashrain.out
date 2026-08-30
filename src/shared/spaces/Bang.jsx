// src/shared/spaces/Bang.jsx — 방榜 (공통 공간 · 신문이 붙는 게시벽)
// 세 앱이 공유하는 광장 2. 신문 체계(독후감·논평·에세이·유저 신문)는 타 세션 합의 준용.
import { Page, Card, Row, Chip } from "../demo";

const PAPERS = [
  { k: "독후감", t: "358년을 기다린 한 줄의 증명", s: "『페르마의 마지막 정리』 · 학생", tone: "ac" },
  { k: "논평", t: "숙제는 누구를 위한 것인가", s: "논제 12 · 학생", tone: "warn" },
  { k: "독후감", t: "아이와 같은 책을 읽는다는 것", s: "『수학이 필요한 순간』 · 학부모", tone: "ac" },
  { k: "팁", t: "틀린 문제는 다음날 아침에 다시", s: "월례 설문 공개분 · 익명 강사", tone: "ok" },
];

export default function Bang() {
  return (
    <Page title="방">
      <p className="d-note">발언권은 독서로 벌어요 — 메인 신문이 유일한 광장이고, 학생·학부모·강사의 글이 한 벽에 붙어요.</p>
      <Card title="오늘의 벽">
        {PAPERS.map((p, i) => (
          <Row key={i} main={p.t} sub={p.s} right={<Chip tone={p.tone}>{p.k}</Chip>} />
        ))}
      </Card>
      <p className="d-note">큐레이션은 선별·배치·표제만 — 본문은 손대지 않아요.</p>
    </Page>
  );
}
