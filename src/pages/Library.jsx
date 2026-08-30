// src/pages/Library.jsx — 서재 (학생앱 신규 · 데모)
// #/library 서가(소장|저작) · #/library/write 독후감 · #/library/book/:id 책 상세
import { useState } from "react";
import { Kit, Page, Card, Row, Chip, Tabs } from "../shared/demo";

const BOOKS = [
  { id: 1, t: "수학이 필요한 순간", a: "김민형", st: ["서가", ""] },
  { id: 2, t: "페르마의 마지막 정리", a: "사이먼 싱", st: ["대출 중", "warn"] },
  { id: 3, t: "미움받을 용기", a: "기시미 이치로", st: ["서가", ""] },
  { id: 4, t: "이상한 나라의 수학자", a: "—", st: ["예약 1", "ac"] },
];

function Shelf() {
  const [tab, setTab] = useState("own");
  return (
    <>
      <Card>
        <p className="d-note">서재를 처음 쓰면 글쓰기 품질 향상과 AI 첨삭 개발에 활용된다는 안내에 동의해요. <button className="d-btn" style={{ padding: "4px 9px", marginLeft: 6 }}>동의 내용 보기</button></p>
      </Card>
      <Tabs cur={tab} onSel={setTab} items={[["own", "소장"], ["write", "저작"]]} />
      {tab === "own" ? (
        <Card>
          {BOOKS.map((b) => (
            <Row key={b.id} main={b.t} sub={b.a} right={<Chip tone={b.st[1]}>{b.st[0]}</Chip>}
              onClick={() => (location.hash = "#/library/book/" + b.id)} />
          ))}
        </Card>
      ) : (
        <Card>
          <Row main="『페르마의 마지막 정리』 독후감" sub="8월 12일 · 신문 게재됨" right={<Chip tone="ac">게재</Chip>} />
          <Row main="여름 방학 일기 초고" sub="8월 3일 · 나만 보기" right={<Chip>비공개</Chip>} />
        </Card>
      )}
    </>
  );
}

function Write() {
  return (
    <>
      <Card title="1단계 — 떠오른 키워드 (발산)">
        <div className="d-tabs">
          <Chip tone="ac">증명</Chip><Chip tone="ac">358년</Chip><Chip tone="ac">집념</Chip>
          <input className="d-in" style={{ width: 120 }} placeholder="+ 키워드" />
        </div>
      </Card>
      <Card title="2단계 — 키워드를 이어 설명하기 (수렴)">
        <textarea className="d-in" placeholder="고른 키워드들이 왜 남았는지, 책의 어느 장면과 이어지는지 풀어써요" />
      </Card>
      <Card title="서랍 — 비공개 보관">
        <div className="d-vault">
          <p className="d-sub" style={{ marginBottom: 8 }}>🔒 인용·사진은 여기에만 — 공개면에는 내 글만 실려요</p>
          <textarea className="d-in" placeholder="기억하고 싶은 문장 옮겨 적기" />
          <button className="d-btn" style={{ marginTop: 8 }}>표지 사진 추가</button>
        </div>
      </Card>
      <div style={{ display: "flex", gap: 8 }}>
        <button className="d-btn" onClick={() => (location.hash = "#/library")}>← 서재로</button>
        <button className="d-btn pri" style={{ flex: 1 }}>제출 — 신문 게재 자격</button>
      </div>
    </>
  );
}

function Book() {
  return (
    <>
      <Card>
        <p className="d-main" style={{ fontSize: 15 }}>페르마의 마지막 정리</p>
        <p className="d-sub" style={{ margin: "4px 0 12px" }}>사이먼 싱 · 권장도서 · 태그: 수학사, 끈기</p>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="d-btn pri">대출 신청</button>
          <button className="d-btn" onClick={() => (location.hash = "#/library/write")}>독후감 쓰기</button>
        </div>
      </Card>
      <button className="d-btn" onClick={() => (location.hash = "#/library")}>← 서재로</button>
    </>
  );
}

export default function Library({ hash }) {
  const sub = hash.split("/")[2] || "";
  return (
    <div className="ap-shell">
      <Kit />
      <div className="ap-wrap">
        <Page title={sub === "write" ? "독후감 쓰기" : sub === "book" ? "책" : "서재"}
          right={sub === "" ? <button className="d-btn pri" onClick={() => (location.hash = "#/library/write")}>독후감 쓰기</button> : null}>
          {sub === "write" ? <Write /> : sub === "book" ? <Book /> : <Shelf />}
        </Page>
      </div>
    </div>
  );
}
