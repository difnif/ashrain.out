// 사무 — 행정의 방 (무료): 학생 정보 · 숙제 관리 · 학부모 발신(숙제·보고서·알림장)
// 여기서 보낸 것이 학부모 종성의 '마루'에 놓인다.
import { Page, Card, Row, Chip, Tabs } from "../../../shared/demo";
import { useState } from "react";

const STUDENTS = [
  { id: 1, name: "김하늘", g: "중2", sub: "숙제 12/15 제출 · 어제" },
  { id: 2, name: "이도윤", g: "중1", sub: "이번 주 결석 1회" },
  { id: 3, name: "박서준", g: "고1", sub: "새 매칭 · 정보 입력 필요" },
];

function Detail() {
  const [tab, setTab] = useState("i");
  const [sent, setSent] = useState(false);
  return (
    <>
      <Tabs cur={tab} onSel={setTab} items={[["i", "정보"], ["h", "숙제"], ["s", "학부모 발신"]]} />
      {tab === "i" && (
        <Card title="학생 정보">
          <Row main="김하늘 · 중2" sub="○○중학교 · 연락처는 계약 관계에서만 열람" />
          <Row main="담당 시작" sub="2026년 6월 · 3개월차" />
        </Card>
      )}
      {tab === "h" && (
        <Card title="숙제 관리">
          <Row main="근의 공식 연습 15문항" sub="12/15 제출 · 채점 대기 3" right={<Chip tone="warn">채점</Chip>} />
          <Row main="판별식 오답 재풀이" sub="미제출" right={<Chip tone="down">독촉?</Chip>} />
          <button className="d-btn pri full" style={{ marginTop: 8 }}>새 숙제 배부 — 문서고에서 고르기</button>
        </Card>
      )}
      {tab === "s" && (
        <Card title="학부모에게 보내기 — 종성 마루에 놓여요">
          <Row main="주간 보고서 쓰기" sub="템플릿 + 데이터 슬롯 · 자유 작문 아님" right={<Chip tone="ac">보고서</Chip>} />
          <Row main="알림장 쓰기" sub="다음 주 진도·준비물" right={<Chip>알림장</Chip>} />
          <Row main="문제 꾸러미 건네기" sub="가정에서 확인해볼 몇 문항"
            right={sent ? <Chip tone="ok">건넸어요</Chip> : <button className="d-btn pri" style={{ padding: "6px 10px" }} onClick={() => setSent(true)}>건네기</button>} />
        </Card>
      )}
      <button className="d-btn" onClick={() => (location.hash = "#/samu")}>← 학생 목록</button>
    </>
  );
}

export default function Samu({ param }) {
  return (
    <Page title="사무" right={<Chip tone="ok">무료</Chip>}>
      {param ? <Detail /> : (
        <Card title="내 학생">
          {STUDENTS.map((s) => (
            <Row key={s.id} main={s.name + " · " + s.g} sub={s.sub}
              onClick={() => (location.hash = "#/samu/" + s.id)} right={<Chip>열기</Chip>} />
          ))}
        </Card>
      )}
    </Page>
  );
}
