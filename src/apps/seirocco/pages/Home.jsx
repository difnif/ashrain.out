// 세이로코 홈 — 오늘: 새 흔적 · 마감 · 계약 요약
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Home({ isAssistant }) {
  if (isAssistant) return (
    <Page title="오늘">
      <Card title="조교 모드">
        <p className="d-note">1층 기능만 열려 있어요. AI 학생 면담으로 진단 훈련을 이어가고, 학생앱 활동은 그대로 실적에 쌓여요.</p>
      </Card>
    </Page>
  );
  return (
    <Page title="오늘">
      <div className="d-stats">
        <Stat label="활성 계약" value="4" />
        <Stat label="새 흔적" value="12" />
        <Stat label="예측 마감" value="D-2" />
        <Stat label="이달 설문" value="미제출" />
      </div>
      <Card title="새 흔적">
        <Row main="김하늘 · 오답노트 3건 추가" sub="이차방정식 근의 공식 · 어제 21:40" right={<Chip tone="ac">보기</Chip>} onClick={() => (location.hash = "#/students/1")} />
        <Row main="이도윤 · 스피드 연산 2세트" sub="정답률 78% · 오늘 07:55" right={<Chip>보기</Chip>} onClick={() => (location.hash = "#/students/2")} />
        <Row main="박서준 · 문제 세트 제출" sub="함수의 그래프 · 오늘 08:10" right={<Chip>보기</Chip>} onClick={() => (location.hash = "#/students/3")} />
      </Card>
      <Card title="할 일">
        <Row main="중간 대비 3회차 예측 입력" sub="시험일 D-2 — 마감 전 문항별 예측을 남겨두세요" right={<Chip tone="warn">D-2</Chip>} onClick={() => (location.hash = "#/predict")} />
        <Row main="8월 월례 설문" sub="제출 여부만 확인해요 — 환급 조건" right={<Chip tone="down">미제출</Chip>} onClick={() => (location.hash = "#/survey")} />
      </Card>
    </Page>
  );
}
