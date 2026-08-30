// 월례 설문 — 제출 여부만 기계 체크 · 공개/비공개 문항 시각 분리 (3층)
import { Page, Card, Chip } from "../../../shared/demo";

const Q = [
  ["이번 달 학생에게 효과 있었던 학습 팁 하나", "공개", true],
  ["개념 설명 때 자주 쓰는 비유가 있다면", "공개", true],
  ["플랫폼 사용 만족도 (1~5)", "비공개", false],
  ["개선이 필요한 기능", "비공개", false],
];

export default function Survey() {
  return (
    <Page title="8월 월례 설문" right={<Chip tone="down">미제출</Chip>}>
      <p className="d-note">환급 조건은 매월 1회 제출 — 품질 심사는 없어요. 공개 문항만 익명으로 신문 팁 지면에 실려요.</p>
      {Q.map(([q, t, pub], i) => (
        <Card key={i}>
          <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 8 }}>
            <span className="d-main" style={{ fontSize: 13 }}>{i + 1}. {q}</span>
            <span className="d-sp" /><Chip tone={pub ? "ac" : ""}>{t}</Chip>
          </div>
          <textarea className="d-in" placeholder={pub ? "익명 공개 — 다른 강사·학생에게 보여요" : "운영 데이터 — 공개되지 않아요"} />
        </Card>
      ))}
      <button className="d-btn pri full">제출</button>
    </Page>
  );
}
