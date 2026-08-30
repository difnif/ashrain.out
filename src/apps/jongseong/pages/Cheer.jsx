// 응원 — 스티커·정형 문구만. 자유 입력란 없음(점수 언급이 못 들어오게 채널 설계)
import { useState } from "react";
import { Page, Card, Row, Chip } from "../../../shared/demo";

const ST = ["🌱", "🌙", "☔", "🕯", "🧭", "🍀", "📖", "🫶"];
const MSG = ["오늘도 네 걸음을 응원해", "천천히 가도 괜찮아", "늘 네 편이야", "쉬어가도 길은 이어져"];

export default function Cheer() {
  const [s, setS] = useState(null);
  const [m, setM] = useState(null);
  return (
    <Page title="응원 보내기">
      <Card title="스티커 고르기">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 8 }}>
          {ST.map((e, i) => (
            <button key={i} className="d-cell" style={{ fontSize: 22, aspectRatio: "auto", padding: "12px 0",
              borderColor: s === i ? "var(--ac)" : "var(--bd)" }} onClick={() => setS(i)}>{e}</button>
          ))}
        </div>
      </Card>
      <Card title="문구 고르기">
        {MSG.map((t, i) => (
          <Row key={i} main={t} right={m === i ? <Chip tone="ac">선택</Chip> : null} onClick={() => setM(i)} />
        ))}
      </Card>
      <button className="d-btn pri full" disabled={s === null || m === null}
        style={{ opacity: s === null || m === null ? .5 : 1 }}>보내기</button>
      <Card title="보낸 응원">
        <Row main="🌱 오늘도 네 걸음을 응원해" sub="어제 저녁" />
        <Row main="☔ 천천히 가도 괜찮아" sub="지난주 화요일" />
      </Card>
    </Page>
  );
}
