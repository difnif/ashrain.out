// 계약 — 목록 · 새 계약(전자문서) · 보관함(궤) (2층+)
import { useState } from "react";
import { Page, Card, Row, Chip, Tabs } from "../../../shared/demo";

export default function Contracts() {
  const [tab, setTab] = useState("l");
  return (
    <Page title="계약">
      <Tabs cur={tab} onSel={setTab} items={[["l", "목록"], ["n", "새 계약"], ["v", "보관함"]]} />
      {tab === "l" && (
        <Card>
          <Row main="김하늘" sub="3개월차 · 8월분 결제 완료" right={<Chip tone="ok">활성</Chip>} />
          <Row main="이도윤" sub="1개월차 · 첫 계약(작성료 무료)" right={<Chip tone="ok">활성</Chip>} />
          <Row main="박서준" sub="제안 발송 — 학생·보호자 승인 대기" right={<Chip tone="warn">제안 중</Chip>} />
          <Row main="최유나" sub="6개월 유지 후 종료 · 기록은 학생 흔적에 귀속" right={<Chip>종료</Chip>} />
        </Card>
      )}
      {tab === "n" && (
        <Card title="계약 제안 작성">
          <p className="d-lbl">학생</p>
          <input className="d-in" placeholder="이름 또는 고유번호로 검색" />
          <p className="d-lbl">수업 내용</p>
          <input className="d-in" placeholder="예: 주 2회 · 중2 수학 정규" />
          <p className="d-lbl">기간</p>
          <div className="d-grid2">
            <input className="d-in" placeholder="시작일" /><input className="d-in" placeholder="종료일(선택)" />
          </div>
          <p className="d-note" style={{ margin: "10px 0" }}>첫 계약은 작성료 전액 무료. 이후 결제 발생 월에만 4,000원 — 수업료 금액은 플랫폼이 알 필요 없어요. 미성년 학생은 보호자 동의 절차가 자동으로 붙어요.</p>
          <button className="d-btn pri full">제안 보내기</button>
        </Card>
      )}
      {tab === "v" && (
        <>
          <Card title="내 보관함 — 실적으로 해금">
            <Row main="서안" sub="현재 사용 중" right={<Chip tone="ac">사용 중</Chip>} />
            <Row main="문갑" sub="계약 유지 12개월 누적 시 해금" right={<Chip>잠김</Chip>} />
            <Row main="나전함" sub="36개월 누적 시 해금" right={<Chip>잠김</Chip>} />
          </Card>
          <p className="d-note">궤는 코스메틱, 문서는 평등 — 등급은 효력·열람권에 아무 영향이 없어요.</p>
        </>
      )}
    </Page>
  );
}
