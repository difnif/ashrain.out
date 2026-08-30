// 서무 1 — 필기 순서 메모앱 (기획 v0.1 반영)
// 본질: 녹화가 아니라 판서 시퀀스 "저작". 획 순서만 기록(P1), 세션 없음(P2), 지우기는 파괴적(P3).
// 코퍼스 생산에 과금하지 않는다(P8) — 작성·저장 무료, 해금·소비 측이 유료.
// 개발 순서 F1(기록)→F5(수정)→F2(포스트잇)→F3(강조)→F4(덧칠) · 0주차 필감 스파이크 선행.
import { Card, Row, Chip } from "../../../shared/demo";

export default function SolutionMemo() {
  return (
    <>
      <div className="d-tabs" style={{ marginBottom: 4 }}>
        <Chip tone="ok">생산 무료 · P8</Chip>
        <Chip>순서가 유일한 축</Chip>
        <Chip>세션 없음</Chip>
      </div>
      <Card title="내 판서 문서">
        <Row main="이차방정식 활용 — 속력" sub="기록본 · 획 214 · 어제" right={<Chip>기록</Chip>} />
        <Row main="닮음비 서술형 시범" sub="풀편집 · 포스트잇 3 · 발행됨" right={<Chip tone="ac">발행</Chip>} />
        <button className="d-btn pri full" style={{ marginTop: 8 }}>새 기록 — 쓰면 순서가 남아요</button>
      </Card>
      <Card title="마찰 계기판 — 이 숫자가 코퍼스를 결정해요">
        <Row main="문서당 기록 시간" sub="목표 3분 이내" right={<Chip tone="ok">2:40</Chip>} />
        <Row main="풀편집 시간" sub="목표 10분 이내 · 문서의 ~10%만" right={<Chip>—</Chip>} />
      </Card>
      <p className="d-note">지면 해설이 못 담는 것 — 자리 비워두기(예약), 위로 복귀, 표시 습관 — 이 여기 남아요. 5주차 게이트: "전략 카드가 나오는가, 받아쓰기인가."</p>
    </>
  );
}
