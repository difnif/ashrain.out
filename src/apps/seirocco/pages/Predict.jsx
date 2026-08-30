// 예측–확인 루프 — 문항별 정오·오개념 예측 → OMR 대조 → 적중률 (3층)
import { useState } from "react";
import { Page, Card, Row, Chip, Stat } from "../../../shared/demo";

export default function Predict() {
  const [grid, setGrid] = useState(Array(20).fill(0)); // 0 미입력 1 정답예측 2 오답예측
  const toggle = (i) => setGrid((g) => g.map((v, j) => (j === i ? (v + 1) % 3 : v)));
  return (
    <Page title="예측–확인">
      <Card title="시험 선택">
        <select className="d-in"><option>중간 대비 3회차 (D-2) — 김하늘</option><option>중간 대비 2회차 (완료)</option></select>
      </Card>
      <Card title="문항별 예측 — 정(○)/오(×) 토글">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 6 }}>
          {grid.map((v, i) => (
            <button key={i} className={"d-cell" + (v === 1 ? " o" : v === 2 ? " x" : "")} onClick={() => toggle(i)}>
              {i + 1}{v === 1 ? " ○" : v === 2 ? " ×" : ""}
            </button>
          ))}
        </div>
        <p className="d-lbl" style={{ marginTop: 10 }}>오답 예측 문항의 오개념 태그</p>
        <select className="d-in"><option>D-04 완전제곱식 부호 실수</option><option>D-11 판별식 케이스 혼동</option></select>
        <button className="d-btn pri full" style={{ marginTop: 10 }}>예측 저장</button>
      </Card>
      <Card title="지난 대조 — 2회차">
        <div className="d-stats" style={{ marginBottom: 8 }}>
          <Stat label="적중" value="17/20" /><Stat label="적중률" value="85%" /><Stat label="오개념 적중" value="2/3" />
        </div>
        <Row main="7번 — 예측 ○ / 실제 ×" sub="예상 못 한 오답 · 계산 실수" right={<Chip tone="down">빗나감</Chip>} />
        <Row main="12번 — 예측 ×(D-04) / 실제 ×(D-04)" sub="오개념까지 적중" right={<Chip tone="ok">적중</Chip>} />
      </Card>
      <Card title="적중률 히스토리">
        <Row main="2회차" sub="8/21" right={<Chip tone="ok">85%</Chip>} />
        <Row main="1회차" sub="8/07" right={<Chip>70%</Chip>} />
      </Card>
    </Page>
  );
}
