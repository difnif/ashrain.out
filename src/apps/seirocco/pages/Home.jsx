// 시록고 홈 — 기록하는 자의 책상: 이번 주 쌓인 기록 + 사무 할 일 + 광장
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Home({ isAssistant }) {
  if (isAssistant) return (
    <Page title="오늘">
      <Card title="조교 모드">
        <p className="d-note">광장(하소·방)과 문의만 열려 있어요. 학생앱 활동은 그대로 향임 실적에 쌓여요.</p>
      </Card>
    </Page>
  );
  return (
    <Page title="오늘">
      <div className="d-stats">
        <Stat label="이번 주 풀이 메모" value="12" />
        <Stat label="표시 기록" value="58" />
        <Stat label="수집 문제" value="7" />
        <Stat label="채점 대기" value="3" />
      </div>
      <Card title="기록 (서무 · 코퍼스)">
        <Row main="어제 남긴 풀이 메모 이어쓰기" sub="이차방정식 활용 — 속력" right={<Chip tone="warn">유료</Chip>} onClick={() => (location.hash = "#/seomu/sol")} />
      </Card>
      <Card title="사무 (무료)">
        <Row main="채점 대기 3건" sub="김하늘 · 근의 공식 연습" right={<Chip tone="ok">무료</Chip>} onClick={() => (location.hash = "#/samu/1")} />
        <Row main="주간 보고서 쓸 차례" sub="이번 주 마루 발신 전" onClick={() => (location.hash = "#/samu/1")} />
      </Card>
      <Card title="광장">
        <Row main="하소 — 날아든 연" sub="시험 전날 뭐라고 말해주는 게 좋을까요" onClick={() => (location.hash = "#/haso")} />
        <Row main="방 — 오늘의 벽" sub="틀린 문제는 다음날 아침에 다시" onClick={() => (location.hash = "#/bang")} />
      </Card>
    </Page>
  );
}
