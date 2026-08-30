// 밥 짓는 소리 — 결제: 기본 포인트 '장작' 구매 + 구독권
// 장작 100근 = 10,000원 (근당 100원) · 한 번에 1~1,000근
// 이스터에그: 1,000근 입력 시 나무꾼이 말리고, 그래도 사면 어머니가 축원한다.
import { useState } from "react";
import { Page, Card, Row, Chip } from "../../../shared/demo";

export default function Firewood() {
  const [n, setN] = useState(100);
  const [bought, setBought] = useState(false);
  const v = Math.max(1, Math.min(1000, Number(n) || 1));
  const max = v === 1000;
  return (
    <Page title="밥 짓는 소리" right={<Chip tone="ac">보유 장작 240근</Chip>}>
      <Card title="장작 들이기">
        <p className="d-lbl">몇 근 들일까요 (1~1,000근 · 100근 = 10,000원)</p>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input className="d-in" style={{ flex: 1 }} inputMode="numeric" value={n}
            onChange={(e) => { setN(e.target.value.replace(/\D/g, "")); setBought(false); }} />
          <span className="d-main" style={{ whiteSpace: "nowrap" }}>{(v * 100).toLocaleString()}원</span>
        </div>
        <div className="d-tabs" style={{ marginTop: 8 }}>
          {[10, 100, 500, 1000].map((q) => (
            <button key={q} className={"d-tab" + (v === q ? " on" : "")} onClick={() => { setN(String(q)); setBought(false); }}>{q}근</button>
          ))}
        </div>

        {max && !bought && (
          <div className="d-vault" style={{ marginTop: 12, display: "flex", gap: 12, alignItems: "center" }}>
            <span style={{ fontSize: 30 }}>🪵🧑‍🌾</span>
            <div>
              <p className="d-main" style={{ fontSize: 13 }}>지게 가득 나무를 진 나무꾼</p>
              <p className="d-sub">“이렇게 많이 구매하지 않으셔도 됩니다.”</p>
            </div>
          </div>
        )}
        {max && bought && (
          <div className="d-vault" style={{ marginTop: 12, display: "flex", gap: 12, alignItems: "center", borderColor: "var(--ac)" }}>
            <span style={{ fontSize: 30 }}>🤱</span>
            <div>
              <p className="d-main" style={{ fontSize: 13 }}>배냇저고리의 아이를 안은 어머니</p>
              <p className="d-sub">“천근만근이어도 훨훨 날아갈 것 같은 하루가 되시길 바라요.”</p>
            </div>
          </div>
        )}

        <button className="d-btn pri full" style={{ marginTop: 12 }} onClick={() => setBought(true)}>
          {bought && !max ? "들였어요 (데모)" : "웹으로 결제하기"}
        </button>
      </Card>
      <Card title="구독권">
        <Row main="기능 열쇠 · 월 구독" sub="잠긴 기능을 여는 구독권 — 자녀 지정은 정안수 떠놓는 곳에서" right={<Chip>준비 중</Chip>} />
      </Card>
      <p className="d-note">장작은 이 생태계의 기본 불씨예요 — 선물(아궁이), 전서구, 숍이 전부 장작으로 돌아가요.</p>
    </Page>
  );
}
