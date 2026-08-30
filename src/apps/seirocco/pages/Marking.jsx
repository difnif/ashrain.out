// 서무 2 — 문제 표시 습관 · md 스펙 대기
// 연결점: 문제 표시 연습(학생) 스펙 — 강사의 표시 습관이 지도 코퍼스로.
import { Card, Row, Chip } from "../../../shared/demo";

export default function Marking() {
  return (
    <>
      <Card title="내 표시 기록">
        <Row main="조건 밑줄 → 구하는 것 동그라미" sub="이번 주 41회 기록" right={<Chip tone="ac">패턴</Chip>} />
        <Row main="단위 표시 삼각형" sub="이번 주 17회" right={<Chip>패턴</Chip>} />
      </Card>
      <div className="d-vault" style={{ marginTop: 12 }}>
        <p className="d-sub">📄 스펙 문서(md) 대기 중.</p>
      </div>
    </>
  );
}
