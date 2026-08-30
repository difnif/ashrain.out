// AI 학생 면담 — 심어진 오개념 진단 훈련 (1층 · 온보딩/승진 심사 재사용)
import { Page, Card, Chip } from "../../../shared/demo";

const CHAT = [
  ["ai", "선생님, 이차방정식에서 이항하면 부호를 왜 바꿔요? 그냥 옮기면 안 돼요?"],
  ["me", "양변에 같은 걸 더한다고 생각해보자. -3을 옮기는 게 아니라 +3을 양변에 하는 거야."],
  ["ai", "아 그럼 x²=9면 x=3이죠? 답 하나 맞죠?"],
  ["me", "음수도 제곱하면 9가 되지 않을까?"],
];

export default function Interview() {
  return (
    <Page title="AI 학생 면담">
      <Card title="면담 중 — 가상 학생 ‘민준’">
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {CHAT.map(([w, t], i) => (
            <div key={i} style={{
              alignSelf: w === "me" ? "flex-end" : "flex-start", maxWidth: "82%",
              background: w === "me" ? "var(--in)" : "var(--card)",
              border: "1px solid var(--bd)", borderRadius: 12, padding: "9px 12px", fontSize: 13.5, lineHeight: 1.6,
            }}>{t}</div>
          ))}
        </div>
        <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
          <input className="d-in" placeholder="질문하거나 설명해보세요" />
          <button className="d-btn">전송</button>
        </div>
      </Card>
      <Card title="진단 제출">
        <p className="d-lbl">이 학생에게 심어진 오개념은?</p>
        <select className="d-in">
          <option>D-07 음의 제곱근 누락</option><option>D-04 완전제곱식 부호 실수</option><option>D-11 판별식 케이스 혼동</option>
        </select>
        <button className="d-btn pri full" style={{ marginTop: 10 }}>진단 제출</button>
      </Card>
      <p className="d-note">온보딩과 승진 심사에 같은 면담이 쓰여요. 오개념 시드는 세션 종료까지 비공개.</p>
    </Page>
  );
}
