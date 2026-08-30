// 아궁이에 불 때기 — 자녀에게 장작 선물 (하염없이 장작 넣는 애니메이션)
import { useState } from "react";
import { Page, Card, Chip } from "../../../shared/demo";

const CSS = `
.ag-scene{position:relative;height:130px;background:var(--in);border-radius:12px;overflow:hidden;margin-bottom:12px}
.ag-fire{position:absolute;left:50%;bottom:6px;transform:translateX(-50%);font-size:36px;animation:agf 1.6s ease-in-out infinite}
.ag-log{position:absolute;bottom:30px;font-size:22px;animation:agl 1.6s linear infinite}
.ag-log.l2{animation-delay:.8s}
.ag-glow{position:absolute;left:50%;bottom:0;width:120px;height:60px;transform:translateX(-50%);
  background:radial-gradient(ellipse at bottom, var(--ac) 0%, transparent 70%);opacity:.25;animation:agf 1.6s ease-in-out infinite}
@keyframes agl{0%{left:-10%;opacity:0}12%{opacity:1}68%{left:44%;opacity:1;transform:scale(1)}84%{left:49%;opacity:0;transform:scale(.5)}100%{left:49%;opacity:0}}
@keyframes agf{0%,100%{transform:translateX(-50%) scale(1)}50%{transform:translateX(-50%) scale(1.14)}}
`;

export default function Stoke() {
  const [n, setN] = useState(20);
  return (
    <Page title="아궁이에 불 때기" right={<Chip tone="ac">보유 장작 240근</Chip>}>
      <style>{CSS}</style>
      <Card title="아이의 아궁이">
        <div className="ag-scene">
          <div className="ag-glow" />
          <span className="ag-log">🪵</span>
          <span className="ag-log l2">🪵</span>
          <span className="ag-fire">🔥</span>
        </div>
        <p className="d-lbl">몇 근 넣을까요</p>
        <div style={{ display: "flex", gap: 8 }}>
          <input className="d-in" style={{ flex: 1 }} inputMode="numeric" value={n}
            onChange={(e) => setN(e.target.value.replace(/\D/g, ""))} />
          <button className="d-btn pri">불 때기</button>
        </div>
        <p className="d-note" style={{ marginTop: 10 }}>넣은 장작은 아이의 잔고로 옮겨가요 — 아이는 그걸로 자기 숍을 돌아다녀요.</p>
      </Card>
    </Page>
  );
}
