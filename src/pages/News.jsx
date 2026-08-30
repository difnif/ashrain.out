// src/pages/News.jsx — 신문 (학생앱 신규 · 데모)
// #/news 피드 · #/news/post/:id 글 · #/news/write 쓰기 · #/news/tips 팁 지면
// 헌법: 발언권은 독서로 번다. AI 큐레이션은 선별·배치·표제만 — 본문 무수정.
import { useState } from "react";
import { Kit, Page, Card, Row, Chip, Tabs } from "../shared/demo";

const FEED = [
  { k: "독후감", t: "358년을 기다린 한 줄의 증명", s: "『페르마의 마지막 정리』 · 라별의등대", tone: "ac" },
  { k: "논평", t: "숙제는 누구를 위한 것인가", s: "논제 12 · 익명버들", tone: "warn" },
  { k: "독후감", t: "수학이 아름답다는 말의 뜻", s: "『수학이 필요한 순간』 · 밤길걷기", tone: "ac" },
  { k: "에세이", t: "OOTD — 교복 위에 걸치는 계절", s: "패션 도서 5편 게이트 통과 · 서고지기", tone: "ok" },
];

function Feed() {
  return (
    <Card>
      {FEED.map((p, i) => (
        <Row key={i} main={p.t} sub={p.s} right={<Chip tone={p.tone}>{p.k}</Chip>}
          onClick={() => (location.hash = "#/news/post/1")} />
      ))}
    </Card>
  );
}

function Post() {
  return (
    <>
      <Card>
        <Chip tone="ac">독후감</Chip>
        <p className="d-main" style={{ fontSize: 15, margin: "10px 0 4px" }}>358년을 기다린 한 줄의 증명</p>
        <p className="d-sub" style={{ marginBottom: 12 }}>라별의등대 · 8월 12일</p>
        <p className="d-note" style={{ fontSize: 13.5, color: "var(--ink)" }}>
          한 문제를 358년 동안 붙잡은 사람들의 이야기를 읽고, 나는 내가 5분 만에 포기했던 문제들을 떠올렸다…
        </p>
        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <button className="d-btn">👍 12</button><span className="d-sp" />
          <button className="d-btn" style={{ color: "var(--mut)" }}>신고</button>
        </div>
      </Card>
      <button className="d-btn" onClick={() => (location.hash = "#/news")}>← 신문으로</button>
    </>
  );
}

function Write() {
  const [kind, setKind] = useState("r");
  return (
    <>
      <Tabs cur={kind} onSel={setKind} items={[["r", "독후감"], ["c", "논평"]]} />
      {kind === "r" ? (
        <Card>
          <p className="d-note">독후감은 서재의 폼으로 써요 — 제출하면 신문 게재 자격이 생겨요.</p>
          <button className="d-btn pri" style={{ marginTop: 10 }} onClick={() => (location.hash = "#/library/write")}>서재에서 쓰기</button>
        </Card>
      ) : (
        <Card>
          <p className="d-lbl">논제 선택</p>
          <select className="d-in">
            <option>12. 숙제는 누구를 위한 것인가</option>
            <option>07. 시험은 공정한가</option>
            <option>21. AI에게 배우는 것은 배움인가</option>
          </select>
          <p className="d-lbl">본문</p>
          <textarea className="d-in" placeholder="논평은 무조건 공개돼요" />
          <label className="d-sub" style={{ display: "flex", gap: 6, margin: "8px 0" }}>
            <input type="checkbox" /> 이미지는 직접 촬영·제작했어요 (표지 촬영 가능 · 본문 페이지 불가)
          </label>
          <button className="d-btn pri full">게시</button>
        </Card>
      )}
    </>
  );
}

function TipsPage() {
  return (
    <Card title="이달의 팁 — 월례 설문 공개분 (익명)">
      <Row main="틀린 문제는 다음날 아침에 다시" sub="어느 강사의 팁" right={<Chip tone="ac">지도</Chip>} />
      <Row main="개념 카드를 소리 내어 읽게 해요" sub="어느 강사의 팁" right={<Chip tone="ac">지도</Chip>} />
      <Row main="시험 전날엔 새 문제 금지" sub="어느 학부모의 팁" right={<Chip>가정</Chip>} />
    </Card>
  );
}

export default function News({ hash }) {
  const sub = hash.split("/")[2] || "";
  const title = sub === "write" ? "글쓰기" : sub === "tips" ? "팁 지면" : sub === "post" ? "글" : "신문";
  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <Page title={title}
          right={sub === "" ? (
            <span style={{ display: "flex", gap: 6 }}>
              <button className="d-btn" onClick={() => (location.hash = "#/news/tips")}>팁</button>
              <button className="d-btn pri" onClick={() => (location.hash = "#/news/write")}>쓰기</button>
            </span>
          ) : null}>
          {sub === "post" ? <Post /> : sub === "write" ? <Write /> : sub === "tips" ? <TipsPage /> : <Feed />}
          {sub === "" && <p className="d-note">발언권은 독서로 벌어요 — 메인 신문이 유일한 광장이에요.</p>}
        </Page>
      </div>
    </div>
  );
}
