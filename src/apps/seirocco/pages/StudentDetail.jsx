// 학생 상세 — 타임라인 · 오답노트 · 처방 · 과제 (3층)
import { useState } from "react";
import { Page, Card, Row, Chip, Tabs } from "../../../shared/demo";

export default function StudentDetail({ param }) {
  const [tab, setTab] = useState("t");
  return (
    <Page title={"김하늘 · 중2"} right={<Chip tone="ok">계약 3개월차</Chip>}>
      <Tabs cur={tab} onSel={setTab}
        items={[["t", "타임라인"], ["w", "오답노트"], ["p", "처방"], ["h", "과제"]]} />
      {tab === "t" && (
        <Card title="흔적 타임라인">
          <Row main="오답노트 3건 추가" sub="이차방정식 근의 공식 · 어제 21:40" right={<Chip tone="down">D-04</Chip>} />
          <Row main="스피드 연산 2세트" sub="정답률 82% · 평균 4.1초 · 어제 20:12" />
          <Row main="개념 카드 열람" sub="m3-1-07 판별식 · 어제 19:58" />
          <Row main="힌트 사용 1회" sub="G-12 보조선 힌트 · 그저께" right={<Chip>L1</Chip>} />
          <Row main="문제 세트 제출" sub="12/15 정답 · 3일 전" />
        </Card>
      )}
      {tab === "w" && (
        <Card title="오답노트">
          <Row main="x² - 6x + 2 = 0 의 근" sub="완전제곱식 변형에서 부호 실수" right={<Chip tone="down">D-04</Chip>} />
          <Row main="판별식과 근의 개수" sub="D=0 케이스를 두 근으로 셈" right={<Chip tone="down">D-11</Chip>} />
        </Card>
      )}
      {tab === "p" && (
        <Card title="처방 조립">
          <p className="d-note" style={{ marginBottom: 8 }}>선수 개념을 골라 재학습 커리큘럼을 직접 조립해요 — 자동 처방은 없어요.</p>
          <div className="d-tabs">
            <Chip tone="ac">완전제곱식 m3-1-05</Chip>
            <Chip tone="ac">인수분해 기초 m2-2-03</Chip>
            <Chip>+ 개념 추가</Chip>
          </div>
          <button className="d-btn pri" style={{ marginTop: 12 }}>처방 보내기</button>
        </Card>
      )}
      {tab === "h" && (
        <Card title="과제">
          <Row main="근의 공식 연습 15문항" sub="HomeworkCapture · 12/15 제출" right={<Chip tone="ok">채점됨</Chip>} />
          <Row main="판별식 오답 재풀이" sub="어제 배부 · 미제출" right={<Chip tone="warn">대기</Chip>} />
        </Card>
      )}
    </Page>
  );
}
