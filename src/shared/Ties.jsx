// src/shared/Ties.jsx — 인연: 유저 검색(인연 찾기) → 연 맺기
// 유형: 지연(기본) · 혈연(자녀). 일종의 즐겨찾기 — 아궁이·정안수·선물·전서구의 "받는 이"가 이 목록에서 나온다.
// 혈연으로 미성년을 맺으면 보호자 동의 절차(guardian_consents)가 이어서 붙는다(배선은 추후).
import { useState } from "react";
import { Card, Row, Chip } from "./demo";

export default function Ties({ emphasizeChild }) {
  const [q, setQ] = useState("");
  const [tied, setTied] = useState(false);
  const [kind, setKind] = useState(emphasizeChild ? "blood" : "ji");
  return (
    <>
      <Card title="인연 찾기">
        <div style={{ display: "flex", gap: 8 }}>
          <input className="d-in" placeholder="닉네임·아이디로 검색" value={q}
            onChange={(e) => { setQ(e.target.value); setTied(false); }} />
          <button className="d-btn">찾기</button>
        </div>
        {q && (
          <Row main="하늘" sub="학생 · 중2 · ashrain"
            right={tied ? <Chip tone="ok">{kind === "blood" ? "혈연" : "지연"} 맺음</Chip> : (
              <span style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <select className="d-in" style={{ width: "auto", padding: "5px 8px", fontSize: 12 }}
                  value={kind} onChange={(e) => setKind(e.target.value)}>
                  <option value="ji">지연</option>
                  <option value="blood">혈연</option>
                </select>
                <button className="d-btn pri" style={{ padding: "5px 9px" }} onClick={() => setTied(true)}>연 맺기</button>
              </span>
            )} />
        )}
        {emphasizeChild && (
          <p className="d-note" style={{ marginTop: 8 }}>자녀는 <b>혈연</b>으로 맺어요 — 미성년이면 보호자 동의 절차가 이어서 붙어요.</p>
        )}
      </Card>
      <Card title="내 인연">
        <Row main="하늘" sub="학생 · 중2" right={<Chip tone="ac">혈연</Chip>} />
        <Row main="버들 어머니" sub="학부모 · 하소에서 맺음" right={<Chip>지연</Chip>} />
      </Card>
      <p className="d-note">인연은 즐겨찾기예요 — 선물·전서구·아궁이의 받는 이가 여기서 나와요. [미결] 미성년 검색 노출 범위 · 연결 코드 병행 여부.</p>
    </>
  );
}
