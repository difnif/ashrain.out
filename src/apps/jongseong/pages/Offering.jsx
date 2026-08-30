// 정안수 떠놓는 곳 — 구독권을 자녀에게 지정해 올리는 곳
// 종교 스킨 아이템으로 이름·풍경이 바뀐다: 기도 드리는 곳 · 108배 하는 곳
import { useState } from "react";
import { Page, Card, Row, Chip } from "../../../shared/demo";

const SKINS = [
  ["water", "정안수 떠놓는 곳", "🫖 기본"],
  ["pray", "기도 드리는 곳", "🕯 스킨 · 800근"],
  ["bow", "108배 하는 곳", "🪷 스킨 · 800근"],
];

export default function Offering() {
  const [skin, setSkin] = useState("water");
  const title = SKINS.find((s) => s[0] === skin)[1];
  return (
    <Page title={title}>
      <Card title="구독권 올리기">
        <p className="d-lbl">자녀</p>
        <select className="d-in"><option>하늘 (중2)</option></select>
        <p className="d-lbl">구독권</p>
        <select className="d-in"><option>기능 열쇠 · 1개월</option><option>기능 열쇠 · 3개월</option></select>
        <button className="d-btn pri full" style={{ marginTop: 10 }}>올리기</button>
        <p className="d-note" style={{ marginTop: 10 }}>매일 같은 자리에서 올리는 마음 — 아이에겐 구독이 열렸다는 사실만 전해져요.</p>
      </Card>
      <Card title="자리 바꾸기 (스킨)">
        {SKINS.map(([k, name, tag]) => (
          <Row key={k} main={name} sub={tag}
            right={skin === k ? <Chip tone="ac">사용 중</Chip> : <button className="d-btn" style={{ padding: "5px 9px" }} onClick={() => setSkin(k)}>바꾸기</button>} />
        ))}
      </Card>
    </Page>
  );
}
