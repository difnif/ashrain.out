// 서무 1 — 풀이과정 메모앱 · md 스펙 대기
// 연결점: corpus_solutions · 해설 티어(L1/L2/L3) 체계 — 강사의 풀이가 코퍼스로.
import { Card, Row, Chip } from "../../../shared/demo";

export default function SolutionMemo() {
  return (
    <>
      <Card title="최근 메모">
        <Row main="이차방정식 활용 — 속력 문제" sub="어제 · 3단계 풀이 · 줄 독립 원칙" right={<Chip tone="ac">L1</Chip>} />
        <Row main="닮음비 서술형" sub="3일 전 · 채점 기준 메모 포함" right={<Chip>L2</Chip>} />
      </Card>
      <div className="d-vault" style={{ marginTop: 12 }}>
        <p className="d-sub">📄 스펙 문서(md) 대기 중 — 도착하면 이 작업실이 본모습을 갖춰요.</p>
      </div>
    </>
  );
}
