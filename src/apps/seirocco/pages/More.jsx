// 더보기 — 부속 화면 진입
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function More({ isAdmin }) {
  return (
    <Page title="더보기">
      <Card>
        <Row main="AI 학생 면담" sub="오개념 진단 훈련 · 승진 심사 재사용" right={<Chip>1층</Chip>} onClick={() => (location.hash = "#/interview")} />
        <Row main="승진" sub="직급 · 산식 · 심사" right={<Chip>2층</Chip>} onClick={() => (location.hash = "#/career")} />
        <Row main="월례 설문" sub="환급 조건 — 이번 달 미제출" right={<Chip tone="down">D-1</Chip>} onClick={() => (location.hash = "#/survey")} />
        <Row main="강사 검증" sub="서류 심사로 2층 진입" right={<Chip tone="warn">미제출</Chip>} onClick={() => (location.hash = "#/verify")} />
        <Row main="문의" sub="운영자 채널" onClick={() => (location.hash = "#/support")} />
        {isAdmin && <Row main="폰트 창고" sub="UI 서체 수집처" right={<Chip tone="warn">관리자</Chip>} onClick={() => (location.hash = "#/fonts")} />}
      </Card>
    </Page>
  );
}
